# -*- coding: utf-8 -*-
"""
US Grade 4 Math: Line Plots with Fractions (4.MD.B.4)
  python tools/gen_us_math_g4_line_plots_fractions.py
All amounts are whole numbers of EIGHTHS (v): 11 means 1 3/8.
Line plots are marked in halves (step 4), fourths (step 2) or eighths (step 1); each mark is
labeled in simplest form (1/8, 1/4, 3/8, 1/2 ...).
Sums and differences keep the largest denominator of the labels involved (3/4 - 1/4 = 2/4,
3/4 - 3/8 = 3/8), like the add-and-subtract-fractions unit; a choice never repeats the value
of the correct answer in another form.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]
TEACHERS = ["Ms. Lee", "Mr. Diaz", "Mrs. Patel", "Ms. Brown", "Mr. Kim", "Mrs. Green"]
WORD = {2: "halves", 4: "fourths", 8: "eighths"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (a, b)


def mx(w, n, d):
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def parts(v, d=None):
    """v eighths -> (whole, numerator, denominator). d=None: simplest form. Falls back to
    eighths when v cannot be written with denominator d."""
    w, r = divmod(v, 8)
    if r == 0:
        return w, 0, d or 1
    if d is None:
        g = gcd(r, 8)
        return w, r // g, 8 // g
    k = 8 // d
    if r % k:
        return w, r, 8
    return w, r // k, d


def num(v, d=None):
    return mx(*parts(v, d))


def den(v):
    """Denominator of the simplest form (1 for whole numbers)."""
    return parts(v)[2]


def dd(*vs):
    """Denominator to work in: the largest denominator among the labels."""
    return max([den(v) for v in vs] + [2])


def plain(v):
    w, n, d = parts(v)
    if n == 0:
        return str(w)
    return ("%d and %d/%d" % (w, n, d)) if w else "%d/%d" % (n, d)


IN = ("inch", "inches", "in")


def amt(v, U=IN, d=None):
    return "%s %s" % (num(v, d), U[0] if v <= 8 else U[1])


def chv(v, U=IN, d=None):
    """Choice (html, value) for v eighths."""
    if U[2]:
        s = num(v, d) + " " + U[2]
    else:
        s = amt(v, U, d)
    return (s, Fraction(v, 8))


def chx(w, n, d, U=IN):
    """Choice with any denominator (for 'added the denominators' mistakes)."""
    val = Fraction(w) + Fraction(n, d)
    unit = U[2] or (U[0] if val <= 1 else U[1])
    return (mx(w, n, d) + " " + unit, val)


def nword(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


def xs(n):
    return nword(n, "X", "X's")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd, same_value_ok=True):
    """correct and cands are (html, value) pairs or plain strings. A candidate with the same
    value as the correct answer is never used (it would also be right)."""
    if isinstance(correct, tuple):
        cs, cv = correct
    else:
        cs, cv = str(correct), None
    seen = {cs}
    vals = set()
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, tuple):
            s, v = c
            if v is not None and (v <= 0 or (cv is not None and v == cv)):
                continue
            if v in vals and not same_value_ok:
                continue
            vals.add(v)
        else:
            s = str(c)
        if s in seen or not s:
            continue
        seen.add(s)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_n(q, correct, cands, e, rnd):
    cands = [c for c in cands if c is not None and c > 0 and c != correct]
    return mcq(q, correct, cands, e, rnd)


def mcq_v(q, v, cands, e, rnd, U=IN, d=None):
    """Answer v eighths; cands are eighths values or ready (html, value) tuples."""
    cc = []
    for c in cands:
        if c is None:
            continue
        cc.append(c if isinstance(c, tuple) else (chv(c, U, d) if c > 0 else None))
    return mcq(q, chv(v, U, d), cc, e, rnd)


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
    """Tag pictures that must print larger so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def balance(sets, rnd):
    """Move the correct choice so each position (A to D) is the answer 5 times in every set."""
    for st in sets:
        pos = [0, 1, 2, 3] * 5
        rnd.shuffle(pos)
        for it, t in zip(st["items"], pos):
            ch = it["c"]
            ch[it["a"]], ch[t] = ch[t], ch[it["a"]]
            it["a"] = t


# ------------------------------------------------------------ line plot picture
FS, FS2 = 19, 14          # label size; the stacked fraction digits are 14


def svg_num(x, y, v, color=INK):
    """Label for v eighths (simplest form) centered on x, baseline y."""
    w, n, d = parts(v)
    cw = 0.6 * FS
    ws = str(w) if (w or not n) else ""
    ww = len(ws) * cw
    fw = (0.62 * FS2 + 4) if n else 0
    gap = 3 if (ws and n) else 0
    x0 = x - (ww + gap + fw) / 2
    s = []
    if ws:
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s'>%s</text>" % (x0, y, FS, color, ws))
    if n:
        xf = x0 + ww + gap + fw / 2
        ym = y - 0.36 * FS
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (xf, ym - 2, FS2, color, n))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>"
                 % (xf - fw / 2, ym, xf + fw / 2, ym, color))
        s.append("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                 % (xf, ym + 2 + 0.72 * FS2, FS2, color, d))
    return "".join(s)


def plot_svg(start, step, counts, title="Length (inches)", what="lengths in inches"):
    n = len(counts)
    mxc = max(max(counts), 1)
    pad = 32
    gap = max(52, int(300 / (n - 1)))
    W = int(2 * pad + gap * (n - 1))
    Y = 30 + 16 * (mxc - 1)
    H = Y + 66
    X = lambda i: pad + gap * i
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (pad - 18, Y, W - pad + 18, Y, INK)]
    for i in range(n):
        x = X(i)
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.8'/>" % (x, Y - 6, x, Y + 6, INK))
        s.append(svg_num(x, Y + 31, start + i * step))
        for k in range(counts[i]):
            cy = Y - 18 - 16 * k
            s.append("<path d='M%d %d L%d %d M%d %d L%d %d' stroke='%s' stroke-width='2.4' stroke-linecap='round'/>"
                     % (x - 6, cy - 6, x + 6, cy + 6, x - 6, cy + 6, x + 6, cy - 6, GREEN))
    s.append("<text x='%d' y='%d' font-size='14' fill='%s' text-anchor='middle'>%s</text>" % (W / 2, Y + 60, INK, title))
    lab = "line plot of %s from %s to %s marked in %s" % (what, plain(start), plain(start + step * (n - 1)), WORD[8 // step])
    return svg_wrap(W, H, "".join(s), lab)


# ------------------------------------------------------------ data
# what was measured: (plural, singular, smallest, largest) in eighths of an inch
CTX = [("beetles", "beetle", 4, 20), ("crickets", "cricket", 4, 16), ("grasshoppers", "grasshopper", 8, 24),
       ("caterpillars", "caterpillar", 6, 20), ("leaves", "leaf", 12, 40), ("shells", "shell", 4, 24),
       ("feathers", "feather", 16, 48), ("earthworms", "earthworm", 16, 40), ("twigs", "twig", 24, 56),
       ("crayons", "crayon", 20, 32), ("pencils", "pencil", 24, 56), ("acorns", "acorn", 6, 14),
       ("pine cones", "pine cone", 16, 40), ("snail shells", "snail shell", 4, 14), ("ribbon pieces", "ribbon piece", 8, 40),
       ("seed pods", "seed pod", 8, 24), ("paper clips", "paper clip", 6, 16), ("ants", "ant", 1, 8)]


class Ctx:
    def __init__(self, rnd):
        self.pool = CTX[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self, need=0):
        while True:
            c = self.pool[self.i % len(self.pool)]
            self.i += 1
            if c[3] - c[2] >= need:
                return c


def n_for(step, rnd):
    return rnd.choice({1: [6, 7, 8], 2: [5, 6, 7], 4: [4, 5]}[step])


def make_plot(rnd, lo, hi, step, n, ok=lambda c: True, tot=(7, 16)):
    starts = [s for s in range(lo, hi - step * (n - 1) + 1) if s % step == 0 and s > 0]
    assert starts, (lo, hi, step, n)
    for _ in range(6000):
        s = rnd.choice(starts)
        peak = rnd.randrange(n)
        counts = []
        for i in range(n):
            d = abs(i - peak)
            counts.append(max(0, rnd.choice([4, 5, 3, 4]) - d + rnd.choice([-1, 0, 0, 1])))
        counts = [min(c, 5) for c in counts]
        t = sum(counts)
        ends_ok = not (counts[0] == 0 and counts[1] == 0) and not (counts[-1] == 0 and counts[-2] == 0)
        if tot[0] <= t <= tot[1] and ends_ok and ok(counts):
            return s, step, counts
    raise RuntimeError("no plot %s %s %s %s" % (lo, hi, step, n))


def ctx_plot(rnd, C, step, ok=lambda c: True, n=None, tot=(7, 16)):
    n = n or n_for(step, rnd)
    ctx = C.next(step * (n - 1))
    s, st, cn = make_plot(rnd, ctx[2], ctx[3], step, n, ok, tot)
    return ctx, s, st, cn


def vals(s, st, cn):
    return [s + i * st for i in range(len(cn))]


def unique_max(c):
    return c.count(max(c)) == 1


def data_list(rnd, s, st, cn):
    d = []
    for i, c in enumerate(cn):
        d += [s + i * st] * c
    rnd.shuffle(d)
    return d


def intro(P, ctx, rnd):
    pl = ctx[0]
    if rnd.random() < 0.5:
        n, he, his = P.next()
        return "%s measured some %s. The line plot shows the lengths." % (n, pl), (n, he)
    t = TEACHERS[rnd.randrange(len(TEACHERS))]
    return "%s's class measured some %s. The line plot shows the lengths." % (t, pl), ("the class", "they")


def look_alike(v, V):
    """A mark that is easy to mix up with v: same numerator, other denominator (3/8 and 3/4)."""
    w, n, d = parts(v)
    for u in V:
        if u == v:
            continue
        w2, n2, d2 = parts(u)
        if n and n2 == n and w2 == w and d2 != d:
            return u
    return None


# ------------------------------------------------------------ explanations
def conv(vs, d):
    """'1/4 = 2/8' for each label that has to be renamed to denominator d."""
    out = []
    for v in sorted(set(vs)):
        if v % 8 and den(v) != d:
            out.append("%s = %s" % (num(v), num(v, d)))
    if not out:
        return ""
    return "Write them in %s: %s. " % (WORD[d], " and ".join(out))


def e_sub(N1, N2, d, unit=""):
    """N1 - N2 pieces of 1/d, explained."""
    u = (" " + unit) if unit else ""
    w1, f1 = divmod(N1, d)
    w2, f2 = divmod(N2, d)
    ans = mx((N1 - N2) // d, (N1 - N2) % d, d)
    if w1 == 0 and w2 == 0:
        return ("Subtract the numerators: %d − %d = %d. Keep the denominator %d: <b>%s%s</b>."
                % (f1, f2, f1 - f2, d, ans, u))
    if f1 == 0 and w2 == 0 and w1 == 1:
        return "Write 1 as %s. Then %s − %s = <b>%s%s</b>." % (fr(d, d), fr(d, d), fr(f2, d), ans, u)
    if f1 >= f2:
        t = ("Subtract the fractions: %s − %s = %s. " % (fr(f1, d), fr(f2, d), fr(f1 - f2, d) if f1 > f2 else "0")) if f2 else ""
        t += ("Subtract the whole numbers: %d − %d = %d. " % (w1, w2, w1 - w2)) if w2 else "The whole number stays %d. " % w1
        return t + "The answer is <b>%s%s</b>." % (ans, u)
    if f1 == 0:
        t = "There is no fraction to take %s from, so rename 1 whole: %d = %s. " % (fr(f2, d), w1, mx(w1 - 1, d, d))
    else:
        t = ("%s is less than %s, so rename 1 whole as %s: %s = %s. "
             % (fr(f1, d), fr(f2, d), fr(d, d), mx(w1, f1, d), mx(w1 - 1, d + f1, d)))
    t += "Subtract the fractions: %s − %s = %s. " % (fr(d + f1, d), fr(f2, d), fr(d + f1 - f2, d))
    if w1 - 1 or w2:
        t += "Subtract the whole numbers: %d − %d = %d. " % (w1 - 1, w2, w1 - 1 - w2)
    return t + "The answer is <b>%s%s</b>." % (ans, u)


def e_total(terms, d, unit=""):
    """Add the eighths values in terms, working in denominator d."""
    u = (" " + unit) if unit else ""
    k = 8 // d
    Ns = [t // k for t in terms]
    ws = [n // d for n in Ns]
    fs = [n % d for n in Ns]
    S, W = sum(fs), sum(ws)
    T = sum(Ns)
    ans = mx(T // d, T % d, d)
    if W == 0:
        t = "Add the numerators: %s = %d. Keep the denominator %d: " % (" + ".join(map(str, fs)), S, d)
        if S > d and S % d:
            return t + "%s. That is more than 1: %s = <b>%s%s</b>." % (fr(S, d), fr(S, d), ans, u)
        if S % d == 0:
            return t + "%s = <b>%s%s</b>." % (fr(S, d), ans, u)
        return t + "<b>%s%s</b>." % (ans, u)
    nz = [f for f in fs if f]
    t = "Add the fractions: %s = %s. " % (" + ".join(fr(f, d) for f in nz), fr(S, d)) if nz else ""
    wz = [w for w in ws if w]
    t += ("Add the whole numbers: %s = %d. " % (" + ".join(map(str, wz)), W)) if len(wz) > 1 else "The whole number is %d. " % W
    if S >= d:
        extra = mx(S // d, S % d, d)
        t += "%s = %s, so %d + %s = <b>%s%s</b>." % (fr(S, d), extra, W, extra, ans, u)
    elif S:
        t += "Put them together: <b>%s%s</b>." % (ans, u)
    else:
        t += "The total is <b>%s%s</b>." % (ans, u)
    return t


def e_diff(hi, lo, U=IN, intro_txt="", d=None):
    d = d or dd(hi, lo)
    k = 8 // d
    D = hi - lo
    return intro_txt + conv([hi, lo], d) + "Subtract: %s − %s. " % (num(hi, d), num(lo, d)) + e_sub(
        hi // k, lo // k, d, U[0] if D <= 8 else U[1])


def diff_cands(hi, lo, st, ends=None, d=None):
    """Wrong differences (eighths) from real mistakes."""
    d = d or dd(hi, lo)
    k = 8 // d
    D = hi - lo
    c = []
    if ends and ends != (hi, lo):
        c.append(ends[0] - ends[1])                 # used the ends of the number line
    c.append(D + st)                                # counted the marks, not the spaces
    w1, f1 = divmod(hi // k, d)
    w2, f2 = divmod(lo // k, d)
    if f1 < f2:
        c.append(((w1 - w2) * d + (f2 - f1)) * k)   # took the smaller fraction from the bigger one
        c.append(((w1 - w2) * d + (d + f1 - f2)) * k)   # renamed but kept the whole number
    c.append(hi + lo)                               # added instead of subtracting
    c.append(D - st)
    c.append(D + 8)
    return c


# ============================================================ set 1: read a line plot
def set_read(rnd, P, C):
    its = []
    plan = [("count", 1), ("most", 1), ("total", 1), ("eq", 1), ("longest", 1), ("count", 2), ("longer", 1),
            ("shortest", 1), ("eq", 1), ("most", 2), ("total", 4), ("count", 1), ("longer", 2), ("longest", 2),
            ("eq", 1), ("most", 1), ("shortest", 2), ("count", 4), ("total", 1), ("look", 1)]
    used_eq = set()
    for kind, st in plan:
        if kind == "count":
            ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: any(c[i] >= 2 for i in range(1, len(c) - 1)))
            V = vals(s, st, cn)
            i = rnd.choice([i for i in range(1, len(cn) - 1) if cn[i] >= 2])
            v, c = V[i], cn[i]
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are %s long?" % (ctx[0], amt(v))
            e = ("Find %s on the number line. Count only the X's in that column: %d. "
                 "Do not count the X's above the marks next to it." % (num(v), c))
            its.append(mcq_n(q, c, [cn[i - 1], cn[i + 1], sum(cn), c + 1, c - 1], e, rnd))
        elif kind == "look":
            # 3/8 and 3/4 are both on the plot: easy to mix up
            for _ in range(500):
                ctx, s, st, cn = ctx_plot(rnd, C, 1, n=7)
                V = vals(s, st, cn)
                pairs = [(i, V.index(look_alike(V[i], V))) for i in range(len(V))
                         if V[i] % 8 and den(V[i]) == 8 and look_alike(V[i], V) is not None]
                pairs = [(i, j) for i, j in pairs if cn[i] >= 1 and cn[j] >= 1 and cn[i] != cn[j]]
                if pairs:
                    break
            i, j = pairs[0]
            v, c = V[i], cn[i]
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are %s long?" % (ctx[0], amt(v))
            e = ("Read the labels carefully: %s and %s are different marks. Find %s and count the X's above it: %d."
                 % (num(v), num(V[j]), num(v), c))
            its.append(mcq_n(q, c, [cn[j], cn[i - 1] if i else None, cn[i + 1] if i + 1 < len(cn) else None, sum(cn), c + 1], e, rnd))
        elif kind == "eq":
            for _ in range(500):
                ctx, s, st, cn = ctx_plot(rnd, C, 1)
                V = vals(s, st, cn)
                idx = [i for i in range(1, len(cn) - 1) if V[i] % 8 and den(V[i]) < 8 and cn[i] >= 1
                       and V[i] % 8 not in used_eq]
                if idx:
                    break
            i = rnd.choice(idx)
            v, c = V[i], cn[i]
            used_eq.add(v % 8)
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are %s long?" % (ctx[0], amt(v, IN, 8))
            e = ("The marks are labeled in simplest form. %s = %s, so look at the mark labeled %s. "
                 "Count the X's above it: %d." % (num(v, 8), num(v), num(v), c))
            its.append(mcq_n(q, c, [cn[i - 1], cn[i + 1], sum(cn), c + 1, c - 1, c + 2], e, rnd))
        elif kind == "most":
            ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: unique_max(c) and c.index(max(c)) != len(c) - 1 and c[-1] > 0)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            order = sorted(range(len(cn)), key=lambda k: -cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            first = min(k for k in range(len(cn)) if cn[k])
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " Which length is the most common?"
            e = ("The most common length has the tallest stack of X's. The stack above %s has %d X's, more than any other."
                 % (num(V[m]), cn[m]))
            its.append(mcq_v(q, V[m], [V[order[1]], V[last], V[first], V[m] + st, V[m] - st], e, rnd))
        elif kind == "total":
            ctx, s, st, cn = ctx_plot(rnd, C, st)
            tot = sum(cn)
            cols = sum(1 for x in cn if x)
            txt, who = intro(P, ctx, rnd)
            if who[0] == "the class":
                ask = " How many %s did the class measure in all?" % ctx[0]
            else:
                ask = " How many %s did %s measure in all?" % (ctx[0], who[0])
            q = fig(plot_svg(s, st, cn)) + txt + ask
            e = ("Each X is one %s. Add the X's in every column: %s = %d." %
                 (ctx[1], " + ".join(str(x) for x in cn if x), tot))
            its.append(mcq_n(q, tot, [len(cn), cols, max(cn), tot - 1, tot + 1], e, rnd))
        elif kind == "longest":
            ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: c[-1] == 0 and c[-2] > 0 and c[0] > 0 and unique_max(c)
                                      and c.index(max(c)) != len(c) - 2)
            V = vals(s, st, cn)
            last = max(k for k in range(len(cn)) if cn[k])
            m = cn.index(max(cn))
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How long is the longest %s?" % ctx[1]
            e = ("Look for the X that is farthest to the right: it is above %s. "
                 "The mark %s has no X, so no %s is that long." % (num(V[last]), num(V[-1]), ctx[1]))
            its.append(mcq_v(q, V[last], [V[-1], V[m], V[last] - st, V[0]], e, rnd))
        elif kind == "shortest":
            ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: c[0] == 0 and c[1] > 0 and c[-1] > 0 and unique_max(c)
                                      and c.index(max(c)) != 1)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How long is the shortest %s?" % ctx[1]
            e = ("Look for the X that is farthest to the left: it is above %s. "
                 "The first mark, %s, has no X, so no %s is that short." % (num(V[1]), num(V[0]), ctx[1]))
            its.append(mcq_v(q, V[1], [V[0], V[m], V[2], V[-1]], e, rnd))
        else:  # longer
            ctx, s, st, cn = ctx_plot(rnd, C, st)
            V = vals(s, st, cn)
            opts = [k for k in range(1, len(cn) - 2) if cn[k] > 0 and sum(1 for x in cn[k + 1:] if x) >= 2]
            k = rnd.choice(opts)
            ans = sum(cn[k + 1:])
            txt, who = intro(P, ctx, rnd)
            q = fig(plot_svg(s, st, cn)) + txt + " How many %s are longer than %s?" % (ctx[0], amt(V[k]))
            right = [x for x in cn[k + 1:] if x]
            e = ("Longer means to the right of %s. Do not count the X's above %s itself. "
                 "Add the X's to the right: %s = %d." % (num(V[k]), num(V[k]), " + ".join(str(x) for x in right), ans))
            its.append(mcq_n(q, ans, [ans + cn[k], cn[k + 1], sum(cn[:k]), sum(cn[:k + 1]), ans + 1, ans - 1], e, rnd))
    return {"title": "Read a line plot with fractions", "items": its}


# ============================================================ set 2: make a line plot
def list_html(d, forms=None):
    forms = forms or {}
    return ", ".join(num(v, forms.get(i)) for i, v in enumerate(d))


def set_make(rnd, P, C):
    its = []
    # A: one X is missing (5)
    for st in [1, 1, 2, 1, 1]:
        ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: c[0] > 0 and c[-1] > 0, n=6 if st == 1 else 5, tot=(6, 10))
        V = vals(s, st, cn)
        d = data_list(rnd, s, st, cn)
        k = rnd.choice([i for i in range(len(cn)) if cn[i] >= 1])
        shown = cn[:]
        shown[k] -= 1
        n, he, his = P.next()
        q = (fig(plot_svg(s, st, shown)) +
             "%s measured %d %s. The lengths in inches are: %s. %s made this line plot but forgot one X. "
             "Where does the missing X go?" % (n, len(d), ctx[0], list_html(d), cap(he)))
        e = ("Count how many times each length is in the list. %s is in the list %s, "
             % (num(V[k]), "once" if cn[k] == 1 else "%d times" % cn[k]) +
             ("but the plot has no X above it. " if shown[k] == 0 else
              "but the plot shows only %s above it. " % xs(shown[k])) +
             "The missing X goes above %s." % num(V[k]))
        top = shown.index(max(shown))
        cand = [look_alike(V[k], V), V[top], V[k] + st if k + 1 < len(cn) else None, V[k] - st if k > 0 else None] + V
        its.append(mcq_v(q, V[k], cand, e, rnd))
    # B: how many X's from a list that mixes 1/4 and 2/8 (4)
    for j in range(4):
        for _ in range(500):
            ctx, s, st, cn = ctx_plot(rnd, C, 1, n=6, tot=(7, 10))
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if V[i] % 8 and den(V[i]) < 8 and cn[i] >= 2]
            if idx:
                break
        i = rnd.choice(idx)
        d = data_list(rnd, s, st, cn)
        pos = [p for p, x in enumerate(d) if x == V[i]]
        forms = {pos[0]: 8}                                      # at least one in eighths, one in simplest form
        for p in pos[2:]:
            if rnd.random() < 0.5:
                forms[p] = 8
        n8 = len(forms)
        ns = cn[i] - n8
        t = TEACHERS[j % len(TEACHERS)]
        q = ("%s's class measured %d %s. The lengths in inches are: %s. The class makes a line plot marked in eighths, "
             "with each mark labeled in simplest form. How many X's go above %s?" % (t, len(d), ctx[0], list_html(d, forms), num(V[i])))
        tm = lambda m: "once" if m == 1 else "%d times" % m
        e = ("%s = %s, so both go above the same mark. In the list, %s appears %s and %s appears %s: %d + %d = %d X's."
             % (num(V[i], 8), num(V[i]), num(V[i]), tm(ns), num(V[i], 8), tm(n8), ns, n8, cn[i]))
        nb = [cn[x] for x in (i - 1, i + 1) if 0 <= x < len(cn)]
        its.append(mcq_n(q, cn[i], [ns, n8] + nb + [cn[i] + 1, len(d)], e, rnd))
    # C: which scale (3)
    n, he, his = P.next()
    d = [10, 12, 9, 14, 11, 12, 13]
    q = ("%s measured 7 crickets. The lengths in inches are: %s. Which scale should the line plot use so every length has a mark?"
         % (n, list_html(d)))
    e = ("Some lengths, like %s and %s, are eighths of an inch. Halves and fourths have no mark for them, "
         "so the number line must be marked in eighths." % (num(9), num(13)))
    its.append(mcq(q, "eighths of an inch", ["fourths of an inch", "halves of an inch", "whole inches"], e, rnd))
    for dl, ticks, odd in [([12, 14, 18, 16, 20, 15], [12, 14, 16, 18, 20], 15), ([6, 4, 10, 8, 3, 6], [2, 4, 6, 8, 10], 3)]:
        n, he, his = P.next()
        q = ("%s measured 6 %s: %s inches. %s makes a line plot marked in fourths: %s. Which length has no mark on this line plot?"
             % (n, "acorns" if dl[0] > 8 else "snail shells", list_html(dl), cap(he), ", ".join(num(v) for v in ticks)))
        e = ("A fourths scale only has marks at 0, %s, %s, %s, 1 and so on. %s is an eighth, so it falls between two marks. "
             "The line plot needs to be marked in eighths." % (fr(1, 4), fr(1, 2), fr(3, 4), num(odd)))
        others = [v for v in dl if v != odd]
        its.append(mcq_v(q, odd, others, e, rnd))
    # D: which data set matches the plot (4)
    for st in [1, 2, 1, 1]:
        for _ in range(500):
            ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: c[0] > 0 and c[-1] > 0 and max(c) >= 2, n=5, tot=(5, 6))
            V = vals(s, st, cn)
            data = sorted(data_list(rnd, s, st, cn))
            if len(set(data)) >= 3:
                break
        right = data[:]
        wrong = []
        # read an eighth as a fourth (3/8 -> 3/4) or a fourth as an eighth (1/4 -> 1/8)
        swap = {1: 2, 3: 6, 2: 1, 6: 3}                    # 1/8 <-> 1/4, 3/8 <-> 3/4
        ps = [i for i, x in enumerate(data) if x % 8 in swap]
        if ps:
            w4 = data[:]
            p = ps[-1]
            w4[p] = data[p] - data[p] % 8 + swap[data[p] % 8]
            wrong.append(sorted(w4))
        # moved one X to the next mark
        p = rnd.choice([p for p in range(len(data)) if data[p] + st <= V[-1]])
        w1 = data[:]
        w1[p] += st
        wrong.append(sorted(w1))
        # one X left out
        p = rnd.randrange(len(data))
        wrong.append(data[:p] + data[p + 1:])
        # a column counted with one X too many
        p = rnd.choice([i for i in range(len(cn)) if cn[i]])
        wrong.append(sorted(data + [V[p]]))
        txt, who = intro(P, ctx, rnd)
        q = fig(plot_svg(s, st, cn)) + txt + " Which list of lengths (in inches) matches the line plot?"
        e = ("Read each X: %s. That is %d lengths, the same as the %d X's on the plot."
             % (", ".join("%s above %s" % (xs(cn[i]), num(V[i])) for i in range(len(cn)) if cn[i]), len(data), len(data)))
        its.append(mcq(q, ", ".join(num(v) for v in right), [", ".join(num(v) for v in w) for w in wrong], e, rnd))
    # E: a length written another way (4)
    used_e = set()
    for form in ["eighths", "eighths", "improper", "improper"]:
        for _ in range(500):
            if form == "eighths":
                ctx, s, st, cn = ctx_plot(rnd, C, 1, n=7)
                V = vals(s, st, cn)
                idx = [i for i in range(1, len(V) - 1) if V[i] % 8 and den(V[i]) < 8 and V[i] % 8 not in used_e]
            else:
                ctx, s, st, cn = ctx_plot(rnd, C, 1, n=7)
                V = vals(s, st, cn)
                idx = [i for i in range(1, len(V) - 1) if 8 < V[i] < 16 and (V[i] % 2) == (len(its) % 2)]
            if idx and ctx[1] not in ("ant",):
                break
        i = rnd.choice(idx)
        v = V[i]
        used_e.add(v % 8)
        n, he, his = P.next()
        if form == "eighths":
            shown = num(v, 8)
            e = ("%s = %s (divide the top and bottom by %d). The mark is labeled %s, so the X goes there."
                 % (num(v, 8), num(v), 8 // den(v), num(v)))
        else:
            shown = fr(v, 8)
            e = ("%s is more than 1: %s = %s + %s = 1 %s" % (fr(v, 8), fr(v, 8), fr(8, 8), fr(v - 8, 8), fr(v - 8, 8)) +
                 (" = %s" % num(v) if den(v) < 8 else "") + ". The X goes above %s." % num(v))
        q = (fig(plot_svg(s, st, cn)) + "%s made this line plot of %s lengths. Then %s measured one more %s. It is %s inch%s long. "
             "Above which mark should %s draw the X?" % (n, ctx[1], he, ctx[1], shown, "es" if v > 8 else "", he))
        cand = [2 * v if 2 * v <= V[-1] else None, v - 1, v + 1, v // 2 if v // 2 >= V[0] else None, v - 2, v + 2]
        cand = [x for x in cand if x is not None and V[0] <= x <= V[-1]]
        its.append(mcq(q, (num(v), Fraction(v, 8)), [(num(x), Fraction(x, 8)) for x in cand], e, rnd))
    return {"title": "Make a line plot from data", "items": its}


# ============================================================ set 3: longest minus shortest
def set_diff(rnd, P, C):
    its = []
    # A: plot, longest - shortest (10)
    plan = [(1, False), (1, True), (2, False), (1, False), (1, True), (2, True), (1, False), (1, True), (2, False), (1, False)]
    used = set()
    for st, gaps in plan:
        for _ in range(800):
            if gaps:
                ok = lambda c: (c[0] == 0) != (c[-1] == 0)
            else:
                ok = lambda c: c[0] > 0 and c[-1] > 0
            ctx, s, st, cn = ctx_plot(rnd, C, st, ok)
            V = vals(s, st, cn)
            first = min(k for k in range(len(cn)) if cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            lo, hi = V[first], V[last]
            key = (lo, hi)
            if key not in used and hi - lo != 8:
                break
        used.add(key)
        txt, who = intro(P, ctx, rnd)
        q = fig(plot_svg(s, st, cn)) + txt + " How much longer is the longest %s than the shortest %s?" % (ctx[1], ctx[1])
        d = 8 // st
        e = e_diff(hi, lo, IN, "Longest: %s. Shortest: %s. " % (amt(hi), amt(lo)) +
                   ("Use the X's, not the ends of the number line. " if gaps else ""), d)
        its.append(mcq_v(q, hi - lo, diff_cands(hi, lo, st, (V[-1], V[0]), d), e, rnd, IN, d))
    # B: plot, most common minus shortest (4)
    for st in [1, 1, 2, 1]:
        ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: unique_max(c) and c.index(max(c)) >= 2 and c[0] > 0)
        V = vals(s, st, cn)
        m = cn.index(max(cn))
        hi, lo = V[m], V[0]
        txt, who = intro(P, ctx, rnd)
        q = (fig(plot_svg(s, st, cn)) + txt +
             " How much longer is the most common length than the shortest length?")
        d = 8 // st
        e = e_diff(hi, lo, IN, "Most common: %s (the tallest stack). Shortest: %s. " % (amt(hi), amt(lo)), d)
        last = max(k for k in range(len(cn)) if cn[k])
        cand = [(str(cn[m] - cn[0]) + " in", Fraction(cn[m] - cn[0])) if cn[m] - cn[0] else None,  # subtracted the X's
                V[last] - lo] + diff_cands(hi, lo, st, None, d)
        its.append(mcq_v(q, hi - lo, cand, e, rnd, IN, d))
    # C: from a list, lengths written in different forms (4)
    lists = [("bean sprouts", [6, 3, 7, 4, 2], {0: 8}), ("crayons", [26, 29, 24, 31, 28, 27], {}),
             ("seed pods", [14, 9, 20, 12, 17], {2: 8}), ("leaves", [22, 28, 19, 25, 30, 20], {1: 8, 4: 4})]
    for pl, dl, forms in lists:
        n, he, his = P.next()
        lo, hi = min(dl), max(dl)
        d = dd(*dl) if forms else dd(hi, lo)
        d = max(d, max(forms.values()) if forms else 2)
        q = ("%s measured %d %s. The lengths in inches are: %s. What is the difference between the longest and the shortest?"
             % (n, len(dl), pl, list_html(dl, forms)))
        e = ("Find the longest, %s, and the shortest, %s. Do not just use the first and last numbers in the list. "
             % (amt(hi), amt(lo)))
        k = 8 // d
        e += conv([hi, lo], d) + "Subtract: %s − %s. " % (num(hi, d), num(lo, d)) + e_sub(hi // k, lo // k, d, "inch" if hi - lo <= 8 else "inches")
        fl = abs(dl[0] - dl[-1])
        its.append(mcq_v(q, hi - lo, [fl] + diff_cands(hi, lo, 1), e, rnd, IN, d))
    # D: work backward (2)
    for sg, lo, D in [("feather", 21, 7), ("twig", 34, 5)]:
        n, he, his = P.next()
        hi = lo + D
        q = ("%s's longest %s is %s longer than %s shortest %s. The shortest %s is %s long. How long is the longest %s?"
             % (n, sg, amt(D), his, sg, sg, amt(lo), sg))
        w1, f1 = divmod(lo, 8)
        S = f1 + D
        e = ("Longer means add: %s + %s. Add the fractions: %s + %s = %s" % (num(lo), num(D), fr(f1, 8), fr(D, 8), fr(S, 8)))
        if S >= 8:
            e += " = %s. So %d + %s = <b>%s</b>." % (num(S), w1, num(S), amt(hi))
        else:
            e += ". So the longest is <b>%s</b>." % amt(hi)
        w0, n0, d0 = parts(lo)
        cand = [w1 * 8 + n0 + D if d0 != 8 else None,                     # 1/4 + 5/8 read as 6/8
                lo - D, (mx(w1, S, 16) + " in", Fraction(w1) + Fraction(S, 16)), D + 8 * w1 if S >= 8 else None,
                hi - 8 if S >= 8 else None, hi + 8, hi + 1]
        its.append(mcq_v(q, hi, cand, e, rnd))
    return {"title": "Difference between the longest and shortest", "items": its}


# ============================================================ set 4: add measurements from a line plot
def whole_ch(k, U):
    return (amt(8 * k, U) if not U[2] else "%d %s" % (k, U[2]), Fraction(k))


def total_cands(v, k, V, cn, i, U=IN):
    """Wrong totals for k X's at v."""
    w, n, d = parts(v)
    T = k * v
    c = [v, whole_ch(k, U)]                                           # one of them / the number of X's
    if w == 0:
        c.append(chx(0, k * n, k * d, U))                             # added the denominators too
    if T % 8 and T > 8:
        c.append(T % 8)                                               # dropped the whole number
    for j in (i - 1, i + 1):
        if 0 <= j < len(cn) and cn[j] and cn[j] != k:
            c.append(cn[j] * v)                                       # counted the X's next to it
    la = look_alike(v, V)
    if la:
        c.append(k * la)
    c += [(k + 1) * v, (k - 1) * v if k > 2 else None]
    return c


def set_total(rnd, P, C):
    its = []
    # A: all the X's at one length (8)
    for st in [1, 1, 2, 1, 4, 1, 2, 1]:
        for _ in range(800):
            ctx, s, st, cn = ctx_plot(rnd, C, st)
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if cn[i] >= 2 and V[i] % 8 and cn[i] * V[i] >= 6]
            if idx:
                break
        i = rnd.choice(idx)
        v, k = V[i], cn[i]
        txt, who = intro(P, ctx, rnd)
        q = (fig(plot_svg(s, st, cn)) + txt +
             " The %s that are %s long are put end to end. What is their total length?" % (ctx[0], amt(v)))
        d = den(v)
        e = ("There are %s above %s, so add %s %d times. " % (xs(k), num(v), num(v), k)) + e_total([v] * k, d, "inch" if k * v <= 8 else "inches")
        its.append(mcq_v(q, k * v, total_cands(v, k, V, cn, i), e, rnd, IN, d))
    # B: two lengths together (5)
    for st in [1, 1, 2, 1, 1]:
        for _ in range(800):
            ctx, s, st, cn = ctx_plot(rnd, C, st, n=6)
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if cn[i] >= 1 and V[i] % 8]
            if len(idx) >= 2:
                a, b = sorted(rnd.sample(idx, 2))
                if den(V[a]) != den(V[b]) and cn[a] + cn[b] <= 5 and cn[a] + cn[b] >= 3:
                    break
        va, vb, ka, kb = V[a], V[b], cn[a], cn[b]
        d = dd(va, vb)
        terms = [va] * ka + [vb] * kb
        T = sum(terms)
        txt, who = intro(P, ctx, rnd)
        q = (fig(plot_svg(s, st, cn)) + txt +
             " What is the total length of all the %s that are %s or %s long?" % (ctx[0], amt(va), amt(vb)))
        e = ("The plot has %s above %s and %s above %s. " % (xs(ka), num(va), xs(kb), num(vb)) +
             conv([va, vb], d) + e_total(terms, d, "inch" if T <= 8 else "inches"))
        # mistakes: one of each, only one column, numerators added without renaming, X's as inches
        wa, na, da = parts(va)
        wb, nb, db = parts(vb)
        cand = [va + vb, (str(ka + kb) + " in", Fraction(ka + kb)), ka * va, kb * vb, T - vb, T + va]
        bad = ka * (wa * 8 + na) + kb * (wb * 8 + nb)          # added the numerators without renaming 1/4 as 2/8
        if bad != T and d == 8:
            cand.insert(1, bad)
        its.append(mcq_v(q, T, cand, e, rnd, IN, d))
    # C: total of every measurement (3)
    for st in [2, 1, 2]:
        ctx, s, st, cn = ctx_plot(rnd, C, st, lambda c: sum(1 for x in c if x) == 3, n=4 if st == 2 else 5, tot=(4, 5))
        V = vals(s, st, cn)
        terms = [V[i] for i in range(len(cn)) for _ in range(cn[i])]
        d = dd(*terms)
        T = sum(terms)
        txt, who = intro(P, ctx, rnd)
        q = fig(plot_svg(s, st, cn)) + txt + " What is the total length of all the %s?" % ctx[0]
        e = ("Add one length for each X: %s. " % " + ".join(num(t) for t in terms) + conv(terms, d) +
             e_total(terms, d, "inches"))
        once = sum(V[i] for i in range(len(cn)) if cn[i])
        cand = [once, (str(len(terms)) + " in", Fraction(len(terms))), T - terms[0], T - terms[-1], T + 8, T - 8]
        its.append(mcq_v(q, T, cand, e, rnd, IN, d))
    # D: which expression (4)
    for st in [1, 2, 1, 1]:
        for _ in range(800):
            ctx, s, st, cn = ctx_plot(rnd, C, st, n=6)
            V = vals(s, st, cn)
            idx = [i for i in range(1, len(cn) - 1) if 2 <= cn[i] <= 4 and V[i] % 8 and cn[i - 1] != cn[i] and cn[i + 1] != cn[i]]
            if idx:
                break
        i = rnd.choice(idx)
        v, k = V[i], cn[i]
        rep = lambda x, m: " + ".join([num(x)] * m)
        txt, who = intro(P, ctx, rnd)
        q = (fig(plot_svg(s, st, cn)) + txt +
             " Which shows the total length of the %s that are %s long?" % (ctx[0], amt(v)))
        e = "Each X above %s is one %s that is %s long. There are %s, so add %s %d times." % (
            num(v), ctx[1], amt(v), xs(k), num(v), k)
        w, n, dn = parts(v)
        cand = [rep(v, cn[i - 1]) if cn[i - 1] else None, rep(v, cn[i + 1]) if cn[i + 1] else None,
                rep(V[i + 1], k), rep(V[i - 1], k), rep(v, k + 1), rep(v, k - 1) if k > 2 else None]
        its.append(mcq(q, rep(v, k), cand, e, rnd))
    return {"title": "Add measurements from a line plot", "items": its}


# ============================================================ set 5: word problems
INW = ("inch", "inches", None)
YD = ("yard", "yards", None)
CUP = ("cup", "cups", None)
FT = ("foot", "feet", None)
LB = ("pound", "pounds", None)

WCTX = {
    "beetles": dict(U=INW, title="Length (inches)", what="beetle lengths in inches",
                    intro="Students measured the beetles in a science class insect collection. The line plot shows their lengths.",
                    diff="How much longer is the longest beetle than the shortest beetle?",
                    one="beetle", tot="If all the beetles that are %s long were lined up end to end, how long would the line be?"),
    "rain": dict(U=INW, title="Rainfall (inches)", what="daily rainfall in inches",
                 intro="The line plot shows how much rain fell each day for %d days. Each X is one day.",
                 diff="How much more rain fell on the wettest day than on the driest day?",
                 one="day", tot="How much rain fell in all on the days with %s of rain?",
                 more="How many more days had %s of rain than %s of rain?"),
    "ribbon": dict(U=YD, title="Length (yards)", what="ribbon lengths in yards",
                   intro="%s cut ribbon pieces for a craft fair. The line plot shows the length of each piece.",
                   diff="How much longer is the longest piece than the shortest piece?",
                   one="piece", tot="%s sews all the pieces that are %s long end to end. How long is the new ribbon?",
                   two="%s uses all the pieces that are %s or %s long. How many yards of ribbon is that?"),
    "juice": dict(U=CUP, title="Juice (cups)", what="amounts of juice in cups",
                  intro="%s poured juice into %d glasses. The line plot shows how much juice is in each glass.",
                  diff="How much more juice is in the fullest glass than in the glass with the least juice?",
                  one="glass", tot="How much juice is in all the glasses that have %s of juice?",
                  two="How much juice is in all the glasses that have %s or %s of juice?"),
    "pencils": dict(U=INW, title="Length (inches)", what="pencil lengths in inches",
                    intro="The students in %s's class measured their pencils. The line plot shows the lengths.",
                    diff="How much longer is the longest pencil than the shortest pencil?",
                    one="pencil", tot="If the pencils that are %s long were laid end to end, how long would the row be?"),
    "plants": dict(U=INW, title="Height (inches)", what="plant heights in inches",
                   intro="%s grew bean plants. The line plot shows how tall each plant is after one week.",
                   diff="How much taller is the tallest plant than the shortest plant?",
                   one="plant", more="How many more plants are %s tall than %s tall?"),
    "frogs": dict(U=FT, title="Jump length (feet)", what="frog jump lengths in feet",
                  intro="At a frog jumping contest, each X shows the length of one jump.",
                  diff="How much farther was the longest jump than the shortest jump?",
                  one="jump", tot="Add all the jumps that were %s long. What is their total length?",
                  more="How many more jumps were %s long than %s long?"),
    "trail": dict(U=LB, title="Weight (pounds)", what="bag weights in pounds",
                  intro="%s filled bags of trail mix for a hike. The line plot shows the weight of each bag.",
                  diff="How much heavier is the heaviest bag than the lightest bag?",
                  one="bag", tot="What is the total weight of the bags that weigh %s each?",
                  two="What is the total weight of all the bags that weigh %s or %s?"),
}


def w_plot(rnd, name, s, st, cn, P):
    c = WCTX[name]
    who = P.next()
    t = c["intro"]
    if name == "rain":
        t = t % sum(cn)
    elif name == "juice":
        t = t % (who[0], sum(cn))
    elif name == "pencils":
        t = t % TEACHERS[rnd.randrange(len(TEACHERS))]
    elif "%s" in t:
        t = t % who[0]
    return fig(plot_svg(s, st, cn, c["title"], c["what"])) + t + " ", who


def U_of(name):
    return WCTX[name]["U"]


def unit(v, U):
    return U[0] if v <= 8 else U[1]


def set_words(rnd, P):
    its = []
    # (kind, context, start, step, counts, extra)
    specs = [
        ("diff", "beetles", 3, 1, [1, 2, 4, 3, 0, 2, 1, 0], None),
        ("tot", "rain", 2, 2, [3, 4, 2, 1, 1], 1),
        ("diff", "juice", 2, 2, [0, 2, 3, 3, 1, 1], None),
        ("more", "plants", 12, 1, [1, 2, 4, 2, 3, 1, 1], (2, 4)),
        ("tot", "ribbon", 3, 1, [2, 3, 1, 2, 0, 1], 0),
        ("share", "juice", 2, 2, [3, 1, 1, 1], 3),
        ("diff", "frogs", 20, 2, [1, 2, 3, 2, 0, 1], None),
        ("two", "trail", 2, 1, [1, 2, 3, 2, 1, 1, 0], (1, 3)),
        ("tot", "pencils", 34, 1, [1, 1, 2, 3, 2, 1], 3),
        ("diff", "rain", 1, 1, [2, 3, 2, 1, 1, 0, 1], None),
        ("more", "frogs", 24, 4, [2, 4, 3, 1], (1, 3)),
        ("tot", "trail", 4, 2, [1, 3, 2, 2, 1], 1),
        ("two", "ribbon", 8, 2, [1, 2, 2, 3, 1], (2, 4)),
        ("diff", "pencils", 38, 1, [2, 1, 3, 0, 2, 2, 1], None),
        ("share", "water", 4, 4, [3, 2, 3], 4),
        ("tot", "frogs", 20, 2, [1, 2, 3, 3, 1], 3),
        ("more", "rain", 2, 2, [4, 3, 2, 1, 2], (0, 3)),
        ("two", "juice", 2, 2, [1, 2, 3, 2], (1, 3)),
        ("diff", "plants", 21, 1, [0, 1, 2, 3, 2, 1, 2], None),
        ("tot", "beetles", 6, 1, [1, 2, 3, 2, 1, 1], 1),
    ]
    for kind, name, s, st, cn, ext in specs:
        V = vals(s, st, cn)
        if kind == "share":
            n, he, his = P.next()
            if name == "juice":
                T = sum(V[i] * cn[i] for i in range(len(cn)))
                m = ext
                lead = ("%s poured juice into %d glasses. The line plot shows how much juice is in each glass. "
                        % (n, sum(cn)))
                q = (fig(plot_svg(s, st, cn, "Juice (cups)", "amounts of juice in cups")) + lead +
                     "%s pours all the juice into one pitcher and shares it equally among %d friends. "
                     "How many cups does each friend get?" % (cap(he), m))
                Uw = CUP
            else:
                T = sum(V[i] * cn[i] for i in range(len(cn)))
                m = ext
                lead = ("%s's science class filled %d beakers with water. The line plot shows how much water is in each beaker. "
                        % (TEACHERS[rnd.randrange(len(TEACHERS))], sum(cn)))
                q = (fig(plot_svg(s, st, cn, "Water (cups)", "amounts of water in cups")) + lead +
                     "If all the water were poured together and then shared equally among %d bottles, how much water would be in each bottle?" % m)
                Uw = CUP
            terms = [V[i] for i in range(len(cn)) for _ in range(cn[i])]
            assert T % 8 == 0 and (T // 8) % m == 0, (name, T)
            each = T // m
            d = dd(*terms)
            e = ("First find the total. " + e_total(terms, d, "cups") + " Then share %d cups equally: %d ÷ %d = <b>%s</b>."
                 % (T // 8, T // 8, m, amt(each, Uw)))
            e = e.replace("<b>%s cups</b>. Then" % num(T, d), "%s cups. Then" % num(T, d))
            cand = [T, V[cn.index(max(cn))], whole_ch(sum(cn), CUP),
                    each + 8, each - 8 if each > 8 else None]
            its.append(mcq_v(q, each, cand, e, rnd, Uw))
            continue
        c = WCTX[name]
        U = c["U"]
        lead, who = w_plot(rnd, name, s, st, cn, P)
        if kind == "diff":
            first = min(k for k in range(len(cn)) if cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            lo, hi = V[first], V[last]
            d = 8 // st
            k = 8 // d
            q = lead + c["diff"]
            e = ("Find the X farthest to the right, %s, and farthest to the left, %s. " % (amt(hi, U), amt(lo, U)) +
                 conv([hi, lo], d) + "Subtract: %s − %s. " % (num(hi, d), num(lo, d)) + e_sub(hi // k, lo // k, d, unit(hi - lo, U)))
            its.append(mcq_v(q, hi - lo, diff_cands(hi, lo, st, (V[-1], V[0]), d), e, rnd, U, d))
        elif kind == "tot":
            i = ext
            v, kk = V[i], cn[i]
            T = kk * v
            if name == "ribbon":
                q = lead + c["tot"] % (cap(who[1]), amt(v, U))
            else:
                q = lead + c["tot"] % amt(v, U)
            d = den(v)
            e = ("There are %s above %s. Add %s %d times. " % (xs(kk), num(v), num(v), kk) + e_total([v] * kk, d, unit(T, U)))
            its.append(mcq_v(q, T, total_cands(v, kk, V, cn, i, U), e, rnd, U, d))
        elif kind == "two":
            a, b = ext
            va, vb, ka, kb = V[a], V[b], cn[a], cn[b]
            d = dd(va, vb)
            terms = [va] * ka + [vb] * kb
            T = sum(terms)
            if name == "ribbon":
                q = lead + c["two"] % (cap(who[1]), amt(va, U), amt(vb, U))
            else:
                q = lead + c["two"] % (amt(va, U), amt(vb, U))
            e = ("The plot has %s above %s and %s above %s. " % (xs(ka), num(va), xs(kb), num(vb)) +
                 conv([va, vb], d) + e_total(terms, d, unit(T, U)))
            cand = [va + vb, ka * va, kb * vb, T - vb, T + va, T + 8]
            its.append(mcq_v(q, T, cand, e, rnd, U, d))
        else:  # more
            a, b = ext
            ka, kb = cn[a], cn[b]
            if ka < kb:
                a, b, ka, kb = b, a, kb, ka
            q = lead + c["more"] % (amt(V[a], U), amt(V[b], U))
            e = ("Count the X's above %s: %d. Count the X's above %s: %d. “How many more” means subtract: %d − %d = <b>%d</b>."
                 % (num(V[a]), ka, num(V[b]), kb, ka, kb, ka - kb))
            its.append(mcq_n(q, ka - kb, [ka + kb, ka, kb, ka - kb + 1, ka - kb - 1], e, rnd))
    return {"title": "Line plot word problems", "items": its}


# ============================================================ lesson
LESSON_START = 2
LESSON_COUNTS = [1, 3, 2, 1, 0, 2, 1]          # 1/4 to 1 inch, by eighths
LESSON_LIST = [4, 3, 8, 2, 7, 3, 4, 5, 3, 7]   # same data, in a jumbled order


def body_html():
    V = [LESSON_START + i for i in range(len(LESSON_COUNTS))]
    assert sorted(LESSON_LIST) == [V[i] for i in range(len(V)) for _ in range(LESSON_COUNTS[i])]
    forms = {0: 8, 3: 8}                                         # 4/8 and 2/8 written in eighths
    plot = plot_svg(LESSON_START, 1, LESSON_COUNTS, what="10 beetle lengths in inches")
    return (
        "<h2>What a line plot shows</h2>"
        "<p>A line plot is a number line with an <b>X</b> for each measurement. "
        "When a length repeats, the X's stack up. The number line can be marked in halves, fourths or <b>eighths</b> of a unit.</p>"
        "<p>On an eighths scale, the marks are " + ", ".join(num(v) for v in range(1, 9)) +
        ". Some marks are labeled in simplest form: " + fr(2, 8) + " is written " + fr(1, 4) + ", " + fr(4, 8) + " is " + fr(1, 2) +
        " and " + fr(6, 8) + " is " + fr(3, 4) + ".</p>"
        "<h2>Make a line plot</h2>"
        "<p>A class measured 10 beetles. The lengths in inches are: " + list_html(LESSON_LIST, forms) + ".</p>"
        "<p>Some lengths are eighths, so mark the number line in eighths. Then put one X above the mark for each length. "
        + fr(4, 8) + " goes above " + fr(1, 2) + ", and " + fr(2, 8) + " goes above " + fr(1, 4) + ".</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>10 lengths, 10 X's. The mark " + fr(3, 4) + " has no X, because no beetle is " + fr(3, 4) + " inch long.</figcaption></figure>" +
        table(["Same length", "Where it goes"], [
            [fr(2, 8) + " = " + fr(1, 4), "the mark labeled " + fr(1, 4)],
            [fr(4, 8) + " = " + fr(1, 2), "the mark labeled " + fr(1, 2)],
            [fr(6, 8) + " = " + fr(3, 4), "the mark labeled " + fr(3, 4)],
            [fr(8, 8) + " = 1", "the mark labeled 1"],
        ]) +
        "<h2>Find a difference</h2>"
        "<p>To compare two lengths, subtract. To compare the longest and the shortest, use the X's farthest to the right and to the left.</p>" +
        ex("Example", "How much longer is the longest beetle than the shortest beetle?",
           "Longest: 1 inch. Shortest: " + fr(1, 4) + " inch. Write both in eighths: 1 = " + fr(8, 8) + " and " + fr(1, 4) + " = " +
           fr(2, 8) + ". " + fr(8, 8) + " − " + fr(2, 8) + " = " + fr(6, 8) + ".", fr(6, 8) + " inch") +
        "<h2>Find a total</h2>"
        "<p>Each X is one measurement. To find the total length of the X's above one mark, add that length once for every X.</p>" +
        ex("Example", "The 3 beetles that are " + fr(3, 8) + " inch long are put end to end. How long is the row?",
           fr(3, 8) + " + " + fr(3, 8) + " + " + fr(3, 8) + " = " + fr(9, 8) + ". " + fr(8, 8) + " is 1 whole, so " +
           fr(9, 8) + " = 1 " + fr(1, 8) + ".", "1 " + fr(1, 8) + " inches") +
        ex("Example", "What is the total length of the beetles that are " + fr(1, 2) + " inch or " + fr(5, 8) + " inch long?",
           "2 X's above " + fr(1, 2) + " and 1 X above " + fr(5, 8) + ". Write " + fr(1, 2) + " as " + fr(4, 8) + ": " +
           fr(4, 8) + " + " + fr(4, 8) + " + " + fr(5, 8) + " = " + fr(13, 8) + " = 1 " + fr(5, 8) + ".", "1 " + fr(5, 8) + " inches") +
        "<p>On this page, answers keep the denominator of the problem: " + fr(4, 8) + " is right, and so is " + fr(1, 2) + ".</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Reading " + fr(3, 8) + " as " + fr(3, 4), "Look at the bottom number. Eighths are smaller pieces than fourths"],
            ["Putting " + fr(2, 8) + " at a new mark", fr(2, 8) + " = " + fr(1, 4) + ", so it goes above " + fr(1, 4)],
            ["Using the ends of the number line as the longest and shortest", "Use the X's farthest to the right and left"],
            ["Adding the denominators: " + fr(3, 8) + " + " + fr(3, 8) + " = " + fr(6, 16), "The pieces stay eighths: " + fr(6, 8)],
            ["Adding " + fr(1, 4) + " + " + fr(3, 8) + " as " + fr(4, 8), "Rename first: " + fr(2, 8) + " + " + fr(3, 8) + " = " + fr(5, 8)],
            ["Using the number of X's as the length", "Each X stands for one measurement. Add the lengths, not the X's"],
        ])
    )


FAQ = [
    {"q": "What is a line plot with fractions in 4th grade?",
     "a": "It is a number line marked in halves, fourths or eighths, with one X above the mark for each measurement. Students use it to find the most common length, the difference between lengths and the total of the measurements."},
    {"q": "How do you make a line plot with eighths?",
     "a": "Draw a number line with a mark for every eighth from the smallest to the largest value, labeling marks like 2/8 as 1/4. Then put one X above the mark for each measurement."},
    {"q": "How do you find the difference between the longest and shortest on a line plot?",
     "a": "Find the X farthest to the right and the X farthest to the left, then subtract. For 1 inch and 1/4 inch, write them as 8/8 and 2/8, so the difference is 6/8 inch."},
    {"q": "How do you find the total of the measurements at one mark?",
     "a": "Add that length once for each X above it. Three X's above 3/8 inch give 3/8 + 3/8 + 3/8 = 9/8, which is 1 1/8 inches."},
]


def gen_unit():
    rnd = random.Random(118)
    P = People(rnd)
    C = Ctx(rnd)
    sets = [set_read(rnd, P, C), set_make(rnd, P, C), set_diff(rnd, P, C), set_total(rnd, P, C), set_words(rnd, P)]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    balance(sets, rnd)
    return {
        "country": "us", "subject": "math", "grade": "grade-4", "slug": "line-plots-fractions", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Plots with Fractions: Halves, Fourths and Eighths",
        "seo_title": "Grade 4 Line Plots with Fractions Worksheets: Make and Read Line Plots in Eighths, Add and Subtract Measurements",
        "short_title": "Line Plots with Fractions",
        "domain": "Measurement and Data",
        "standard_code": "4.MD.B.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/4/MD/B/4/",
        "standard_text": "Make a line plot to display a data set of measurements in fractions of a unit (1/2, 1/4, 1/8). Solve problems involving addition and subtraction of fractions by using information presented in line plots. For example, from a line plot find and interpret the difference in length between the longest and shortest specimens in an insect collection.",
        "meta_desc": "Free Grade 4 line plot worksheets with fractions: read and make line plots in halves, fourths and eighths, find the difference between the longest and shortest, add measurements and solve word problems. 100 practice questions with answers.",
        "key_big": "One X for each measurement. Subtract to compare, add to find a total.",
        "key_sub": "Mark the number line in eighths when the data has eighths, and put 2/8 above 1/4. The difference between the longest and shortest uses the X's farthest right and left, not the ends of the line.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "line plot")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
