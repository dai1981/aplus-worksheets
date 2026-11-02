# -*- coding: utf-8 -*-
"""
US Grade 5 Math: Line Plots with Fractions (5.MD.B.2)
  python tools/gen_us_math_g5_line_plots_fractions.py
Plot data are whole numbers of EIGHTHS (v): 11 means 1 3/8. Every mark is labeled in simplest form.
Every computed answer is a fractions.Fraction written in simplest form (Grade 5 operations:
unlike denominators, count x value, total, and "redistribute equally" = total / number of items).
Wrong choices come from real mistakes; a choice never has the same value as the right answer.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace", "Chloe", "Hana"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen", "Max", "Theo"]
TEACHERS = ["Ms. Lee", "Mr. Diaz", "Mrs. Patel", "Ms. Brown", "Mr. Kim", "Mrs. Green"]
WORD = {2: "halves", 4: "fourths", 8: "eighths", 16: "sixteenths"}


# ------------------------------------------------------------ numbers
def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def mx(w, n, d):
    if n == 0:
        return str(w)
    if w == 0:
        return fr(n, d)
    return "%d %s" % (w, fr(n, d))


def show(v):
    """A positive Fraction in simplest form: '3/8', '1 1/4', '2'."""
    w, r = divmod(v.numerator, v.denominator)
    return mx(w, r, v.denominator)


def E(v):
    """v eighths as a Fraction."""
    return F(v, 8)


def num(v):
    """Label for v eighths in simplest form."""
    return show(E(v))


def parts(v):
    f = E(v)
    w, r = divmod(f.numerator, f.denominator)
    return w, r, f.denominator


def plain(v):
    w, n, d = parts(v)
    if n == 0:
        return str(w)
    return ("%d and %d/%d" % (w, n, d)) if w else "%d/%d" % (n, d)


def uw(f, U):
    return U[0] if f <= 1 else U[1]


def amt(f, U):
    """Amount with unit word: '3/8 inch', '1 inch', '1 1/4 inches'."""
    return "%s %s" % (show(f), uw(f, U))


def amt8(v, U):
    """v eighths written in eighths (2/8 inch), for 'written another way' questions."""
    return "%s %s" % (fr(v, 8), uw(E(v), U))


def imp(f, d):
    """f written as an improper fraction (or whole) with denominator d."""
    return fr(f * d, d)


def lcm(*ds):
    out = 1
    for d in ds:
        out = out * d // math.gcd(out, d)
    return out


def cap(s):
    return s[0].upper() + s[1:]


def nword(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


def xs(n):
    return nword(n, "X", "X's")


# ------------------------------------------------------------ explanations
def rename(fs, d):
    """'1 1/4 = 10/8' for each value whose simplest form is not already over d."""
    out = []
    for f in fs:
        if show(f) != imp(f, d) and imp(f, d) not in [o.split(" = ")[-1] for o in out]:
            s = "%s = %s" % (show(f), imp(f, d))
            if s not in out:
                out.append(s)
    if not out:
        return ""
    return "Write them with denominator %d: %s. " % (d, ", ".join(out))


def finish(R, d, U):
    """'= 9/8 = 1 1/8 inches' ending for a result R written over d."""
    t = imp(R, d)
    if show(R) != t:
        t += " = " + show(R)
    return t + " " + uw(R, U)


def e_sub(a, b, U):
    d = lcm(a.denominator, b.denominator)
    if d == 1:
        return "Subtract: %s − %s = <b>%s</b>." % (show(a), show(b), amt(a - b, U))
    return rename([a, b], d) + "Subtract: %s − %s = <b>%s</b>." % (imp(a, d), imp(b, d), finish(a - b, d, U))


def e_add(terms, U):
    d = lcm(*[t.denominator for t in terms])
    return rename(terms, d) + "Add: %s = <b>%s</b>." % (" + ".join(imp(t, d) for t in terms), finish(sum(terms), d, U))


def prod(k, f):
    """'3 × 3/8 = 9/8' (mixed numbers changed to fractions first)."""
    if f.denominator == 1 or k == 1:
        return "%d × %s = %s" % (k, show(f), show(k * f))
    t = "%d × %s = " % (k, show(f))
    if f > 1:
        t += "%d × %s = " % (k, fr(f.numerator, f.denominator))
    t += fr(k * f.numerator, f.denominator)
    if (k * f).denominator == 1:
        t += " = %d" % (k * f)
    return t


def e_products(pairs, U):
    """pairs = [(count, value)]. Multiply each value by its count, then add."""
    T = sum(k * v for k, v in pairs)
    d = lcm(*[v.denominator for k, v in pairs])
    if len(pairs) == 1:
        t = "Multiply: %s. " % prod(*pairs[0])
        k, v = pairs[0]
        R = k * v
        if show(R) != fr(k * v.numerator, v.denominator) and R.denominator > 1:
            t += "%s = %s. " % (fr(k * v.numerator, v.denominator), show(R))
        return t + "The total is <b>%s</b>." % amt(R, U)
    t = "Multiply each value by its number of X's: %s. " % ", ".join(prod(k, v) for k, v in pairs)
    return t + "Add them with denominator %d: %s = <b>%s</b>." % (
        d, " + ".join(imp(k * v, d) for k, v in pairs), finish(T, d, U))


def e_divide(T, n, U):
    """T shared equally by n."""
    R = T / n
    if T.denominator == 1:
        t = "%s ÷ %d = %s" % (show(T), n, fr(T.numerator, n))
    else:
        t = ("Dividing by %d is the same as multiplying by %s: %s × %s = %s"
             % (n, fr(1, n), fr(T.numerator, T.denominator), fr(1, n), fr(T.numerator, T.denominator * n)))
    if T.denominator == 1 and show(R) == fr(T.numerator, n):
        return t + " " + uw(R, U) + "."
    if T.denominator != 1 and show(R) == fr(T.numerator, T.denominator * n):
        return t + " " + uw(R, U) + "."
    return t + " = " + show(R) + " " + uw(R, U) + "."


# ------------------------------------------------------------ helpers
def mcq(q, cs, cands, e, rnd):
    """cs: correct string. cands: strings. Picks the first 3 different ones."""
    seen, pick = {cs}, []
    for c in cands:
        if c is None or c in seen:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def mcq_f(q, R, cands, e, rnd, U=None):
    """R: Fraction answer. cands: Fractions (or None). U: unit word pair or None (bare number)."""
    def s(f):
        return amt(f, U) if U else show(f)
    vals, cc = set(), []
    for c in cands:
        if c is None or c <= 0 or c == R or c in vals:
            continue
        vals.add(c)
        cc.append(s(c))
    return mcq(q, s(R), cc, e, rnd)


def mcq_n(q, n, cands, e, rnd):
    return mcq(q, str(n), [str(c) for c in cands if c is not None and c > 0 and c != n], e, rnd)


def mcq_lab(q, v, cands, e, rnd):
    """Answer is a mark label (eighths v)."""
    return mcq(q, num(v), [num(c) for c in cands if c is not None and c > 0 and c != v], e, rnd)


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
FS, FS2 = 19, 14          # whole-number labels 19, stacked fraction digits 14


def svg_num(x, y, v, color=INK):
    """Label for v eighths (simplest form) centered on x, baseline y."""
    w, n, d = parts(v)
    cw = 0.6 * FS
    ws = str(w) if (w or not n) else ""
    ww = len(ws) * cw
    fw = (0.62 * FS2 * len(str(d)) + 4) if n else 0
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


def plot_svg(start, step, counts, title, what):
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


# ------------------------------------------------------------ contexts
IN = ("inch", "inches")
FT = ("foot", "feet")
YD = ("yard", "yards")
LB = ("pound", "pounds")
L = ("liter", "liters")
CUP = ("cup", "cups")
GAL = ("gallon", "gallons")


def C(**k):
    return k


# lo/hi in eighths. did: what was done ({n} = how many). vp: verb phrase for one value. more: verb phrase "more than".
# tot: "total ... of/in". share: redistribute question (None if it makes no sense).
CTX = [
    C(key="beetles", p="beetles", s="beetle", U=IN, lo=2, hi=14, title="Length (inches)", what="beetle lengths in inches",
      did="measured {n} beetles", nouns="lengths", noun="length", small="shortest",
      vp="are {a} long", more="are longer than {a}", hi_q="How long is the longest beetle?",
      lo_q="How long is the shortest beetle?", diff="How much longer is the longest beetle than the shortest beetle?",
      tot="total length of", share=None),
    C(key="leaves", p="leaves", s="leaf", U=IN, lo=12, hi=36, title="Length (inches)", what="leaf lengths in inches",
      did="measured {n} leaves", nouns="lengths", noun="length", small="shortest",
      vp="are {a} long", more="are longer than {a}", hi_q="How long is the longest leaf?",
      lo_q="How long is the shortest leaf?", diff="How much longer is the longest leaf than the shortest leaf?",
      tot="total length of", share=None),
    C(key="pencils", p="pencils", s="pencil", U=IN, lo=24, hi=56, title="Length (inches)", what="pencil lengths in inches",
      did="measured {n} pencils", nouns="lengths", noun="length", small="shortest",
      vp="are {a} long", more="are longer than {a}", hi_q="How long is the longest pencil?",
      lo_q="How long is the shortest pencil?", diff="How much longer is the longest pencil than the shortest pencil?",
      tot="total length of", share=None),
    C(key="plants", p="bean plants", s="bean plant", U=IN, lo=8, hi=32, title="Height (inches)", what="plant heights in inches",
      did="measured the heights of {n} bean plants", nouns="heights", noun="height", small="shortest",
      vp="are {a} tall", more="are taller than {a}", hi_q="How tall is the tallest bean plant?",
      lo_q="How tall is the shortest bean plant?", diff="How much taller is the tallest bean plant than the shortest bean plant?",
      tot=None, share=None),
    C(key="rain", p="days", s="day", U=IN, lo=1, hi=12, title="Rainfall (inches)", what="daily rainfall in inches",
      did="recorded the rainfall for {n} days", nouns="rainfall amounts", noun="rainfall amount", small="smallest",
      vp="had {a} of rain", more="had more than {a} of rain", hi_q="How much rain fell on the wettest day?",
      lo_q="How much rain fell on the driest day?", diff="How much more rain fell on the wettest day than on the driest day?",
      tot="total rainfall on", share=None),
    C(key="frogs", p="jumps", s="jump", U=FT, lo=12, hi=36, title="Jump length (feet)", what="frog jump lengths in feet",
      did="measured {n} frog jumps", nouns="jump lengths", noun="jump length", small="shortest",
      vp="were {a} long", more="were longer than {a}", hi_q="How long was the longest jump?",
      lo_q="How long was the shortest jump?", diff="How much longer was the longest jump than the shortest jump?",
      tot="total length of", share=None),
    C(key="rocks", p="rocks", s="rock", U=LB, lo=2, hi=16, title="Weight (pounds)", what="rock weights in pounds",
      did="weighed {n} rocks", nouns="weights", noun="weight", small="lightest",
      vp="weigh {a}", more="weigh more than {a}", hi_q="How much does the heaviest rock weigh?",
      lo_q="How much does the lightest rock weigh?", diff="How much heavier is the heaviest rock than the lightest rock?",
      tot="total weight of", share=None),
    C(key="beakers", p="beakers", s="beaker", stuff="water", U=L, lo=1, hi=10, title="Water (liters)", what="amounts of water in liters",
      did="poured water into {n} identical beakers", nouns="amounts", noun="amount", small="smallest",
      vp="hold {a} of water", more="hold more than {a} of water", hi_q="How much water is in the fullest beaker?",
      lo_q="How much water is in the beaker with the least water?",
      diff="How much more water is in the fullest beaker than in the beaker with the least water?",
      tot="total amount of water in",
      share="If all the water were poured together and shared equally among the {n} beakers, how much water would each beaker contain?"),
    C(key="juice", p="glasses", s="glass", stuff="juice", U=CUP, lo=2, hi=10, title="Juice (cups)", what="amounts of juice in cups",
      did="poured juice into {n} glasses", nouns="amounts", noun="amount", small="smallest",
      vp="hold {a} of juice", more="hold more than {a} of juice", hi_q="How much juice is in the fullest glass?",
      lo_q="How much juice is in the glass with the least juice?",
      diff="How much more juice is in the fullest glass than in the glass with the least juice?",
      tot="total amount of juice in",
      share="All the juice is poured into a pitcher and shared equally among the {n} glasses. How much juice will each glass have?"),
    C(key="trail", p="bags", s="bag", stuff="trail mix", U=LB, lo=1, hi=10, title="Trail mix (pounds)", what="bags of trail mix in pounds",
      did="filled {n} bags of trail mix", nouns="weights", noun="weight", small="lightest",
      vp="hold {a} of trail mix", more="hold more than {a} of trail mix", hi_q="How much trail mix is in the fullest bag?",
      lo_q="How much trail mix is in the bag with the least trail mix?",
      diff="How much more trail mix is in the fullest bag than in the bag with the least?",
      tot="total weight of the trail mix in",
      share="All the trail mix is poured together and shared equally among the {n} bags. How much trail mix will each bag hold?"),
    C(key="ribbon", p="pieces", s="piece", U=YD, lo=4, hi=20, title="Ribbon (yards)", what="ribbon lengths in yards",
      did="cut {n} pieces of ribbon", nouns="lengths", noun="length", small="shortest",
      vp="are {a} long", more="are longer than {a}", hi_q="How long is the longest piece?",
      lo_q="How long is the shortest piece?", diff="How much longer is the longest piece than the shortest piece?",
      tot="total length of",
      share="All the pieces are sewn into one long ribbon. Then it is cut into {n} equal pieces. How long is each new piece?"),
    C(key="paint", p="cans", s="can", stuff="paint", U=GAL, lo=1, hi=8, title="Paint (gallons)", what="amounts of paint in gallons",
      did="checked {n} cans of leftover paint", nouns="amounts", noun="amount", small="smallest",
      vp="hold {a} of paint", more="hold more than {a} of paint", hi_q="How much paint is in the fullest can?",
      lo_q="How much paint is in the can with the least paint?",
      diff="How much more paint is in the fullest can than in the can with the least paint?",
      tot="total amount of paint in",
      share="All the paint is poured together and shared equally among the {n} cans. How much paint will each can hold?"),
    C(key="sand", p="jars", s="jar", stuff="sand", U=LB, lo=4, hi=16, title="Sand (pounds)", what="jars of sand in pounds",
      did="filled {n} jars with sand", nouns="weights", noun="weight", small="lightest",
      vp="hold {a} of sand", more="hold more than {a} of sand", hi_q="How much sand is in the fullest jar?",
      lo_q="How much sand is in the jar with the least sand?",
      diff="How much more sand is in the fullest jar than in the jar with the least sand?",
      tot="total weight of the sand in",
      share="All the sand is poured together and shared equally among the {n} jars. How much sand will each jar hold?"),
    C(key="yarn", p="pieces", s="piece", U=YD, lo=6, hi=16, title="Yarn (yards)", what="yarn lengths in yards",
      did="cut {n} pieces of yarn", nouns="lengths", noun="length", small="shortest",
      vp="are {a} long", more="are longer than {a}", hi_q="How long is the longest piece?",
      lo_q="How long is the shortest piece?", diff="How much longer is the longest piece than the shortest piece?",
      tot="total length of",
      share="All the pieces are tied into one long strand. Then it is cut into {n} equal pieces. How long is each new piece?"),
]
BY = {c["key"]: c for c in CTX}


class Ctx:
    def __init__(self, rnd, keys=None):
        self.pool = [c for c in CTX if keys is None or c["key"] in keys]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self, need=0, cond=lambda c: True):
        for _ in range(100):
            c = self.pool[self.i % len(self.pool)]
            self.i += 1
            if c["hi"] - c["lo"] >= need and cond(c):
                return c
        raise RuntimeError("no context")


def who_of(P, rnd):
    if rnd.random() < 0.6:
        n, he, his = P.next()
        return n
    return TEACHERS[rnd.randrange(len(TEACHERS))] + "'s class"


def intro(c, who, n):
    return "%s %s. The line plot shows the %s." % (who, c["did"].format(n=n), c["nouns"])


def vp(c, f):
    return c["vp"].format(a=amt(f, c["U"]))


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
        if tot[0] <= t <= tot[1] and ends_ok and ok(s, counts):
            return s, step, counts
    raise RuntimeError("no plot %s %s %s %s" % (lo, hi, step, n))


def ctx_plot(rnd, CC, step=1, ok=lambda s, c: True, n=None, tot=(7, 16), cond=lambda c: True):
    for _ in range(50):
        n2 = n or rnd.choice({1: [6, 7, 8], 2: [5, 6]}[step])
        c = CC.next(step * (n2 - 1), cond)
        try:
            s, st, cn = make_plot(rnd, c["lo"], c["hi"], step, n2, ok, tot)
            return c, s, st, cn
        except RuntimeError:
            continue
    raise RuntimeError("no ctx plot")


def vals(s, st, cn):
    return [s + i * st for i in range(len(cn))]


def data_list(rnd, s, st, cn):
    d = []
    for i, c in enumerate(cn):
        d += [s + i * st] * c
    rnd.shuffle(d)
    return d


def pic(c, s, st, cn):
    return fig(plot_svg(s, st, cn, c["title"], c["what"]))


def unique_max(c):
    return c.count(max(c)) == 1


def look_alike(v, V):
    """A mark easy to mix up with v: same whole number and numerator, other denominator (3/8 and 3/4)."""
    w, n, d = parts(v)
    for u in V:
        if u == v:
            continue
        w2, n2, d2 = parts(u)
        if n and n2 == n and w2 == w and d2 != d:
            return u
    return None


def unlike(a, b):
    return E(a).denominator != E(b).denominator and E(a).denominator > 1 and E(b).denominator > 1


# ============================================================ set 1: read a line plot
def set_read(rnd, P, CC):
    its = []
    plan = ["count", "most", "all", "eq", "longest", "count", "more", "shortest", "fraction", "eq",
            "most", "all", "fraction", "longest", "eq", "more", "shortest", "count", "fraction", "look"]
    used_eq = set()
    for kind in plan:
        if kind in ("count", "look", "eq"):
            for _ in range(800):
                if kind == "look":
                    c, s, st, cn = ctx_plot(rnd, CC, 1, n=7)
                    V = vals(s, st, cn)
                    idx = [(i, V.index(look_alike(V[i], V))) for i in range(len(V))
                           if parts(V[i])[2] == 8 and look_alike(V[i], V) is not None]
                    idx = [(i, j) for i, j in idx if cn[i] >= 1 and cn[j] >= 1 and cn[i] != cn[j]]
                elif kind == "eq":
                    c, s, st, cn = ctx_plot(rnd, CC, 1)
                    V = vals(s, st, cn)
                    idx = [(i, None) for i in range(1, len(cn) - 1) if V[i] % 8 and parts(V[i])[2] < 8 and cn[i] >= 1
                           and V[i] % 8 not in used_eq]
                else:
                    c, s, st, cn = ctx_plot(rnd, CC, rnd.choice([1, 2]))
                    V = vals(s, st, cn)
                    idx = [(i, None) for i in range(1, len(cn) - 1) if cn[i] >= 2]
                if idx:
                    break
            i, j = rnd.choice(idx)
            v, k = V[i], cn[i]
            who = who_of(P, rnd)
            if kind == "eq":
                used_eq.add(v % 8)
                q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " How many %s %s?" % (
                    c["p"], c["vp"].format(a=amt8(v, c["U"])))
                e = ("The marks are labeled in simplest form. %s = %s, so look at the mark labeled %s. "
                     "Count the X's above it: %d." % (fr(v, 8), num(v), num(v), k))
                its.append(mcq_n(q, k, [cn[i - 1], cn[i + 1], sum(cn), k + 1, k - 1, k + 2], e, rnd))
            elif kind == "look":
                q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " How many %s %s?" % (c["p"], vp(c, E(v)))
                e = ("Read the labels carefully: %s and %s are different marks. Find %s and count the X's above it: %d."
                     % (num(v), num(V[j]), num(v), k))
                its.append(mcq_n(q, k, [cn[j], cn[i - 1] if i else None, cn[i + 1] if i + 1 < len(cn) else None,
                                        sum(cn), k + 1], e, rnd))
            else:
                q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " How many %s %s?" % (c["p"], vp(c, E(v)))
                e = ("Find %s on the number line. Count only the X's in that column: %d." % (num(v), k))
                its.append(mcq_n(q, k, [cn[i - 1], cn[i + 1], sum(cn), k + 1, k - 1], e, rnd))
        elif kind == "most":
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: unique_max(c) and c.index(max(c)) != len(c) - 1 and c[-1] > 0)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            order = sorted(range(len(cn)), key=lambda k: -cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            who = who_of(P, rnd)
            q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " Which %s is the most common?" % c["noun"]
            e = ("The most common value has the tallest stack of X's. The stack above %s has %d X's, more than any other."
                 % (num(V[m]), cn[m]))
            its.append(mcq_f(q, E(V[m]), [E(V[order[1]]), E(V[last]), E(V[0]), E(V[m] + 1), E(V[m] - 1),
                                          F(max(cn))], e, rnd, c["U"]))
        elif kind == "all":
            c, s, st, cn = ctx_plot(rnd, CC, rnd.choice([1, 2]))
            V = vals(s, st, cn)
            tot = sum(cn)
            cols = sum(1 for x in cn if x)
            who = who_of(P, rnd)
            q = (pic(c, s, st, cn) + "%s %s. The line plot shows the %s. How many %s are shown on the line plot?"
                 % (who, c["did"].format(n="some"), c["nouns"], c["p"]))
            e = "Each X is one %s. Add the X's in every column: %s = %d." % (c["s"], " + ".join(str(x) for x in cn if x), tot)
            its.append(mcq_n(q, tot, [len(cn), cols, max(cn), tot - 1, tot + 1], e, rnd))
        elif kind == "longest":
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: c[-1] == 0 and c[-2] > 0 and c[0] > 0 and unique_max(c)
                                    and c.index(max(c)) != len(c) - 2)
            V = vals(s, st, cn)
            last = max(k for k in range(len(cn)) if cn[k])
            m = cn.index(max(cn))
            who = who_of(P, rnd)
            q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " " + c["hi_q"]
            e = ("Look for the X that is farthest to the right: it is above %s. "
                 "The mark %s has no X above it." % (num(V[last]), num(V[-1])))
            its.append(mcq_f(q, E(V[last]), [E(V[-1]), E(V[m]), E(V[last] - 1), E(V[0])], e, rnd, c["U"]))
        elif kind == "shortest":
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: c[0] == 0 and c[1] > 0 and c[-1] > 0 and unique_max(c)
                                    and c.index(max(c)) != 1)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            who = who_of(P, rnd)
            q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " " + c["lo_q"]
            e = ("Look for the X that is farthest to the left: it is above %s. "
                 "The first mark, %s, has no X above it." % (num(V[1]), num(V[0])))
            its.append(mcq_f(q, E(V[1]), [E(V[0]), E(V[m]), E(V[2]), E(V[-1])], e, rnd, c["U"]))
        elif kind == "more":
            c, s, st, cn = ctx_plot(rnd, CC, 1)
            V = vals(s, st, cn)
            opts = [k for k in range(1, len(cn) - 2) if cn[k] > 0 and sum(1 for x in cn[k + 1:] if x) >= 2]
            k = rnd.choice(opts)
            ans = sum(cn[k + 1:])
            who = who_of(P, rnd)
            q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " How many %s %s?" % (c["p"], c["more"].format(a=amt(E(V[k]), c["U"])))
            right = [x for x in cn[k + 1:] if x]
            e = ("Count only the X's to the right of %s. Do not count the X's above %s itself. "
                 "Add the X's to the right: %s = %d." % (num(V[k]), num(V[k]), " + ".join(map(str, right)), ans))
            its.append(mcq_n(q, ans, [ans + cn[k], cn[k + 1], sum(cn[:k]), sum(cn[:k + 1]), ans + 1, ans - 1], e, rnd))
        else:  # fraction of the data
            for _ in range(800):
                c, s, st, cn = ctx_plot(rnd, CC, 1, tot=(8, 12))
                V = vals(s, st, cn)
                N = sum(cn)
                idx = [i for i in range(len(cn)) if cn[i] >= 2 and F(cn[i], N).denominator < N]
                if idx:
                    break
            i = rnd.choice(idx)
            v, k, N = V[i], cn[i], sum(cn)
            R = F(k, N)
            who = who_of(P, rnd)
            q = (pic(c, s, st, cn) + intro(c, who, N) + " What fraction of the %s %s? Write it in simplest form."
                 % (c["p"], vp(c, E(v))))
            e = ("There are %d X's in all, and %d of them are above %s. So the fraction is %s = <b>%s</b>."
                 % (N, k, num(v), fr(k, N), show(R)))
            its.append(mcq_f(q, R, [E(v) if E(v) < 1 else None, F(k, N - k), F(k, len(cn)), F(k + 1, N), F(k, N + 1),
                                    F(k - 1, N)], e, rnd))
    return {"title": "Read a line plot in eighths", "items": its}


# ============================================================ set 2: make a line plot
def list_html(d, forms=None):
    forms = forms or {}
    return ", ".join(fr(v, 8) if forms.get(i) == 8 else num(v) for i, v in enumerate(d))


def unit_pl(c):
    return c["U"][1]


def set_make(rnd, P, CC):
    its = []
    # A: one X is missing (5)
    for st in [1, 1, 2, 1, 1]:
        c, s, st, cn = ctx_plot(rnd, CC, st, lambda s, c: c[0] > 0 and c[-1] > 0, n=6 if st == 1 else 5, tot=(6, 10))
        V = vals(s, st, cn)
        d = data_list(rnd, s, st, cn)
        k = rnd.choice([i for i in range(len(cn)) if cn[i] >= 1])
        shown = cn[:]
        shown[k] -= 1
        who = who_of(P, rnd)
        q = (pic(c, s, st, shown) + "%s %s. The %s in %s are: %s. %s made this line plot but forgot one X. "
             "Where does the missing X go?" % (who, c["did"].format(n=len(d)), c["nouns"], unit_pl(c), list_html(d),
                                               "The class" if "class" in who else who))
        e = ("Count how many times each value is in the list. %s is in the list %s, "
             % (num(V[k]), "once" if cn[k] == 1 else "%d times" % cn[k]) +
             ("but the plot has no X above it. " if shown[k] == 0 else "but the plot shows only %s above it. " % xs(shown[k])) +
             "The missing X goes above %s." % num(V[k]))
        top = shown.index(max(shown))
        cand = [look_alike(V[k], V), V[top], V[k] + st if k + 1 < len(cn) else None, V[k] - st if k > 0 else None] + V
        its.append(mcq_lab(q, V[k], cand, e, rnd))
    # B: how many X's from a list that mixes 1/4 and 2/8 (4)
    for j in range(4):
        for _ in range(800):
            c, s, st, cn = ctx_plot(rnd, CC, 1, n=6, tot=(7, 10))
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if V[i] % 8 and parts(V[i])[2] < 8 and cn[i] >= 2]
            if idx:
                break
        i = rnd.choice(idx)
        d = data_list(rnd, s, st, cn)
        pos = [p for p, x in enumerate(d) if x == V[i]]
        forms = {pos[0]: 8}
        for p in pos[2:]:
            if rnd.random() < 0.5:
                forms[p] = 8
        n8 = len(forms)
        ns = cn[i] - n8
        t = TEACHERS[j % len(TEACHERS)] + "'s class"
        q = ("%s %s. The %s in %s are: %s. The class makes a line plot marked in eighths, "
             "with each mark labeled in simplest form. How many X's go above %s?"
             % (t, c["did"].format(n=len(d)), c["nouns"], unit_pl(c), list_html(d, forms), num(V[i])))
        tm = lambda m: "once" if m == 1 else "%d times" % m
        e = ("%s = %s, so both go above the same mark. In the list, %s appears %s and %s appears %s: %d + %d = %d X's."
             % (fr(V[i], 8), num(V[i]), num(V[i]), tm(ns), fr(V[i], 8), tm(n8), ns, n8, cn[i]))
        nb = [cn[x] for x in (i - 1, i + 1) if 0 <= x < len(cn)]
        its.append(mcq_n(q, cn[i], [ns, n8] + nb + [cn[i] + 1, len(d)], e, rnd))
    # C: which list matches the plot (4)
    for st in [1, 2, 1, 1]:
        for _ in range(800):
            c, s, st, cn = ctx_plot(rnd, CC, st, lambda s, c: c[0] > 0 and c[-1] > 0 and max(c) >= 2, n=5, tot=(5, 6))
            V = vals(s, st, cn)
            data = sorted(data_list(rnd, s, st, cn))
            if len(set(data)) >= 3:
                break
        wrong = []
        swap = {1: 2, 3: 6, 2: 1, 6: 3}                     # 1/8 <-> 1/4, 3/8 <-> 3/4
        ps = [i for i, x in enumerate(data) if x % 8 in swap]
        if ps:
            w4 = data[:]
            p = ps[-1]
            w4[p] = data[p] - data[p] % 8 + swap[data[p] % 8]
            wrong.append(sorted(w4))
        p = rnd.choice([p for p in range(len(data)) if data[p] + st <= V[-1]])
        w1 = data[:]
        w1[p] += st
        wrong.append(sorted(w1))
        p = rnd.randrange(len(data))
        wrong.append(data[:p] + data[p + 1:])
        p = rnd.choice([i for i in range(len(cn)) if cn[i]])
        wrong.append(sorted(data + [V[p]]))
        who = who_of(P, rnd)
        q = pic(c, s, st, cn) + intro(c, who, len(data)) + " Which list (in %s) matches the line plot?" % unit_pl(c)
        e = ("Read each column: %s. That is %d values, the same as the %d X's on the plot."
             % (", ".join("%s above %s" % (xs(cn[i]), num(V[i])) for i in range(len(cn)) if cn[i]), len(data), len(data)))
        its.append(mcq(q, ", ".join(num(v) for v in data), [", ".join(num(v) for v in w) for w in wrong], e, rnd))
    # D: a new value written another way (4)
    used_e = set()
    for form in ["eighths", "improper", "eighths", "improper"]:
        for _ in range(800):
            c, s, st, cn = ctx_plot(rnd, CC, 1, n=7)
            V = vals(s, st, cn)
            if form == "eighths":
                idx = [i for i in range(1, len(V) - 1) if V[i] % 8 and parts(V[i])[2] < 8 and V[i] % 8 not in used_e]
            else:
                idx = [i for i in range(1, len(V) - 1) if 8 < V[i] < 24 and V[i] % 8 and V[i] not in used_e]
            if idx:
                break
        i = rnd.choice(idx)
        v = V[i]
        used_e.add(v % 8 if form == "eighths" else v)
        n, he, his = P.next()
        if form == "eighths":
            e = ("%s = %s (divide the top and bottom by %d). The mark is labeled %s, so the X goes there."
                 % (fr(v, 8), num(v), 8 // parts(v)[2], num(v)))
        else:
            w = v // 8
            e = ("%s is more than 1: 8 eighths make 1 whole, so %s = %d %s" % (fr(v, 8), fr(v, 8), w, fr(v - 8 * w, 8)) +
                 (" = %s" % num(v) if parts(v)[2] < 8 else "") + ". The X goes above %s." % num(v))
        q = (pic(c, s, st, cn) + "%s made this line plot. Then %s added one more value: %s. Above which mark should %s draw the X?"
             % (n, he, amt8(v, c["U"]), he))
        cand = [v - 1, v + 1, v - 8 if form == "improper" else None, v + 8 if form == "improper" else None,
                v - 2, v + 2, look_alike(v, V)]
        cand = [x for x in cand if x is not None and V[0] <= x <= V[-1]]
        its.append(mcq_lab(q, v, cand, e, rnd))
    # E: scale (3)
    n, he, his = P.next()
    dd = [4, 6, 3, 8, 5, 6, 7]
    q = ("%s weighed 7 apples. The weights in pounds are: %s. %s wants a line plot with a mark for every weight. "
         "How should the number line be marked?" % (n, list_html(dd), he.capitalize()))
    e = ("Some weights, like %s and %s, are eighths of a pound. Halves and fourths have no mark for them, "
         "so the number line must be marked in eighths." % (num(3), num(5)))
    assert any(x % 2 for x in dd)
    its.append(mcq(q, "in eighths", ["in fourths", "in halves", "in whole pounds"], e, rnd))
    for dl, ticks, odd, what in [([12, 14, 18, 16, 20, 15], [12, 14, 16, 18, 20], 15, "leaves"),
                                 ([6, 4, 10, 8, 3, 6], [2, 4, 6, 8, 10], 3, "shells")]:
        n, he, his = P.next()
        q = ("%s measured 6 %s: %s inches. %s makes a line plot marked in fourths: %s. Which length has no mark on this line plot?"
             % (n, what, list_html(dl), he.capitalize(), ", ".join(num(v) for v in ticks)))
        e = ("A fourths scale only has marks at 0, %s, %s, %s, 1 and so on. %s is an eighth, so it falls between two marks. "
             "The line plot needs to be marked in eighths." % (fr(1, 4), fr(1, 2), fr(3, 4), num(odd)))
        its.append(mcq_lab(q, odd, [v for v in dl if v != odd], e, rnd))
    return {"title": "Make a line plot from data", "items": its}


# ============================================================ set 3: add and subtract with unlike denominators
def sub_cands(a, b, ends=None):
    """Wrong answers for a - b (Fractions) from real mistakes."""
    c = []
    if ends and ends != (a, b):
        c.append(ends[0] - ends[1])                         # used the ends of the number line
    c.append(a - b + F(1, 8))                               # counted the marks, not the spaces
    wa, na, da = int(a), a - int(a), None
    wb, nb = int(b), b - int(b)
    if na and nb and na.denominator != nb.denominator and na.numerator > nb.numerator:
        # subtracted the numerators without renaming, kept the bigger denominator
        c.append(F(wa - wb) + F(na.numerator - nb.numerator, max(na.denominator, nb.denominator)))
    if na and nb and na.numerator == nb.numerator and wa == wb:
        pass
    if na < nb and na:
        c.append(F(wa - wb) + (nb - na))                    # took the smaller fraction from the bigger one
    c.append(a + b)                                         # added instead
    c.append(a - b - F(1, 8))
    c.append(a - b + 1)
    return c


def add_cands(a, b):
    c = []
    if a < 1 and b < 1:
        c.append(F(a.numerator + b.numerator, a.denominator + b.denominator))   # added tops and bottoms
    if a.denominator != b.denominator:
        c.append(F(a.numerator + b.numerator, max(a.denominator, b.denominator)))  # added tops, no renaming
    c.append(abs(a - b))
    c += [a + b + F(1, 8), a + b - F(1, 8), 2 * max(a, b)]
    return c


def set_unlike(rnd, P, CC):
    its = []
    used = set()
    # A: longest - shortest, labels with different denominators (6)
    for gaps in [False, True, False, True, False, True]:
        for _ in range(2000):
            ok = (lambda s, c: (c[0] == 0) != (c[-1] == 0)) if gaps else (lambda s, c: c[0] > 0 and c[-1] > 0)
            c, s, st, cn = ctx_plot(rnd, CC, 1, ok)
            V = vals(s, st, cn)
            first = min(k for k in range(len(cn)) if cn[k])
            last = max(k for k in range(len(cn)) if cn[k])
            lo, hi = V[first], V[last]
            if (lo, hi) not in used and unlike(lo, hi) and hi - lo != 8:
                break
        used.add((lo, hi))
        who = who_of(P, rnd)
        a, b = E(hi), E(lo)
        q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " " + c["diff"]
        e = ("Greatest: %s. Least: %s. " % (num(hi), num(lo)) +
             ("Use the X's, not the ends of the number line. " if gaps else "") + e_sub(a, b, c["U"]))
        its.append(mcq_f(q, a - b, sub_cands(a, b, (E(V[-1]), E(V[0]))), e, rnd, c["U"]))
    # B: greatest + least together (3)
    for _ in range(3):
        for _ in range(2000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: c[0] > 0 and c[-1] > 0, cond=lambda c: c["tot"])
            V = vals(s, st, cn)
            lo, hi = V[0], V[-1]
            if (lo, hi, "+") not in used and unlike(lo, hi) and E(lo) < 1:
                break
        used.add((lo, hi, "+"))
        who = who_of(P, rnd)
        a, b = E(hi), E(lo)
        q = (pic(c, s, st, cn) + intro(c, who, sum(cn)) +
             " Find the greatest value and the least value on the line plot. What is their sum?")
        e = "Greatest: %s. Least: %s. " % (num(hi), num(lo)) + e_add([a, b], c["U"])
        its.append(mcq_f(q, a + b, add_cands(a, b) + [a - b], e, rnd, c["U"]))
    # C: most common - least (4)
    for _ in range(4):
        for _ in range(2000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: unique_max(c) and c.index(max(c)) >= 2 and c[0] > 0)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            if unlike(V[m], V[0]) and (V[m], V[0]) not in used:
                break
        used.add((V[m], V[0]))
        a, b = E(V[m]), E(V[0])
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, sum(cn)) +
             " What is the difference between the most common %s and the %s %s?" % (c["noun"], c["small"], c["noun"]))
        e = "Most common: %s (the tallest stack). %s: %s. " % (num(V[m]), cap(c["small"]), num(V[0])) + e_sub(a, b, c["U"])
        last = max(k for k in range(len(cn)) if cn[k])
        cand = [F(cn[m] - cn[0]) if cn[m] != cn[0] else None, E(V[last]) - b] + sub_cands(a, b)
        its.append(mcq_f(q, a - b, cand, e, rnd, c["U"]))
    # D: greatest - most common (3)
    for _ in range(3):
        for _ in range(2000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: unique_max(c) and c.index(max(c)) <= len(c) - 3 and c[-1] > 0)
            V = vals(s, st, cn)
            m = cn.index(max(cn))
            if unlike(V[-1], V[m]) and (V[-1], V[m]) not in used:
                break
        used.add((V[-1], V[m]))
        a, b = E(V[-1]), E(V[m])
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, sum(cn)) +
             " How much greater is the greatest value than the most common value?")
        e = "Greatest: %s. Most common: %s (the tallest stack). " % (num(V[-1]), num(V[m])) + e_sub(a, b, c["U"])
        cand = [F(cn[m] - cn[-1]) if cn[m] != cn[-1] else None, a - E(V[0])] + sub_cands(a, b)
        its.append(mcq_f(q, a - b, cand, e, rnd, c["U"]))
    # E: from a list (2)
    lists = [("beetles", [6, 11, 4, 13, 10, 7]), ("ribbon", [14, 9, 20, 12, 17, 18])]
    for key, dl in lists:
        c = BY[key]
        n, he, his = P.next()
        lo, hi = min(dl), max(dl)
        assert unlike(lo, hi)
        a, b = E(hi), E(lo)
        q = ("%s %s. The %s in %s are: %s. What is the difference between the greatest and the least value?"
             % (n, c["did"].format(n=len(dl)), c["nouns"], unit_pl(c), list_html(dl)))
        e = ("Find the greatest, %s, and the least, %s. Do not just use the first and last numbers in the list. "
             % (num(hi), num(lo))) + e_sub(a, b, c["U"])
        its.append(mcq_f(q, a - b, [abs(E(dl[0]) - E(dl[-1]))] + sub_cands(a, b), e, rnd, c["U"]))
    # F: work backward (2)
    for key, lo, D in [("leaves", 18, 6), ("rocks", 5, 12)]:
        c = BY[key]
        n, he, his = P.next()
        a, b = E(lo), E(D)
        q = ("%s's %s are shown on a line plot. The greatest value is %s more than the least value. "
             "The least value is %s. What is the greatest value?" % (n, c["p"], amt(b, c["U"]), amt(a, c["U"])))
        e = "“More than” means add. " + e_add([a, b], c["U"])
        its.append(mcq_f(q, a + b, add_cands(a, b) + [a - b if a > b else b - a], e, rnd, c["U"]))
    return {"title": "Add and subtract with unlike denominators", "items": its}


# ============================================================ set 4: total of all the data
def set_total(rnd, P, CC):
    its = []
    cond = lambda c: c["tot"]
    used = set()
    # A: count x value at one mark (6)
    for _ in range(6):
        for _ in range(2000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, cond=cond)
            V = vals(s, st, cn)
            idx = [i for i in range(len(cn)) if cn[i] >= 2 and V[i] % 8 and cn[i] * V[i] >= 6 and (V[i], cn[i]) not in used]
            if idx:
                break
        i = rnd.choice(idx)
        v, k = E(V[i]), cn[i]
        used.add((V[i], k))
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, sum(cn)) +
             " What is the %s all the %s that %s?" % (c["tot"], c["p"], vp(c, v)))
        e = "There are %s above %s. " % (xs(k), num(V[i])) + e_products([(k, v)], c["U"])
        cand = [v, F(k) + v, F(k), (k + 1) * v, (k - 1) * v]
        for j in (i - 1, i + 1):
            if 0 <= j < len(cn) and cn[j] and cn[j] != k:
                cand.insert(2, cn[j] * v)
        if k * v > 1 and (k * v) % 1:
            cand.insert(1, (k * v) % 1)                         # dropped the whole number
        its.append(mcq_f(q, k * v, cand, e, rnd, c["U"]))
    # B: which expression (3)
    for _ in range(3):
        for _ in range(2000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: sum(1 for x in c if x) == 3 and len(set(x for x in c if x)) == 3,
                                    n=4, tot=(5, 9), cond=cond)
            V = vals(s, st, cn)
            cols = [i for i in range(len(cn)) if cn[i]]
            if tuple(cn) not in used:
                break
        used.add(tuple(cn))
        ks = [cn[i] for i in cols]
        vs = [num(V[i]) for i in cols]
        ex_ = lambda kk: " + ".join("%d × %s" % (a, b) for a, b in zip(kk, vs))
        who = who_of(P, rnd)
        q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " Which expression gives the %s all the %s?" % (c["tot"], c["p"])
        e = ("Each value is counted once for every X above it: %s. So the total is %s." %
             (", ".join("%s above %s" % (xs(a), b) for a, b in zip(ks, vs)), ex_(ks)))
        cand = [" + ".join(vs), ex_(ks[1:] + ks[:1]), ex_(ks[::-1]), "%d × %s" % (sum(ks), vs[-1])]
        its.append(mcq(q, ex_(ks), cand, e, rnd))
    # C: total of every measurement (8)
    for j in range(8):
        for _ in range(4000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: sum(1 for x in c if x) in (3, 4) and s <= 12, n=5, tot=(5, 9), cond=cond)
            V = vals(s, st, cn)
            pairs = [(cn[i], E(V[i])) for i in range(len(cn)) if cn[i]]
            dens = set(v.denominator for k, v in pairs if v.denominator > 1)
            if len(dens) >= 2 and tuple(cn) + (s,) not in used:
                break
        used.add(tuple(cn) + (s,))
        T = sum(k * v for k, v in pairs)
        who = who_of(P, rnd)
        q = pic(c, s, st, cn) + intro(c, who, sum(cn)) + " What is the %s all the %s?" % (c["tot"], c["p"])
        e = e_products(pairs, c["U"])
        once = sum(v for k, v in pairs)
        cand = [once, F(sum(cn)), T - pairs[0][1], T - pairs[-1][1], T + pairs[-1][1], T + 1, T - 1]
        its.append(mcq_f(q, T, cand, e, rnd, c["U"]))
    # D: total of the values greater than a mark (3)
    for _ in range(3):
        for _ in range(4000):
            c, s, st, cn = ctx_plot(rnd, CC, 1, lambda s, c: s <= 11, n=6, cond=cond)
            V = vals(s, st, cn)
            ks = [k for k in range(1, len(cn) - 2) if cn[k] and 2 <= sum(1 for x in cn[k + 1:] if x) <= 3 and V[k] % 8]
            if ks:
                k = rnd.choice(ks)
                pairs = [(cn[i], E(V[i])) for i in range(k + 1, len(cn)) if cn[i]]
                if len(set(v.denominator for _, v in pairs)) >= 2:
                    break
        T = sum(a * v for a, v in pairs)
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, sum(cn)) +
             " What is the %s the %s that %s?" % (c["tot"], c["p"], c["more"].format(a=amt(E(V[k]), c["U"]))))
        e = ("Use only the X's to the right of %s, not the X's above %s. " % (num(V[k]), num(V[k])) +
             e_products(pairs, c["U"]))
        cand = [T + cn[k] * E(V[k]), sum(v for _, v in pairs), F(sum(a for a, _ in pairs)), sum(cn[i] * E(V[i]) for i in range(len(cn)))]
        its.append(mcq_f(q, T, cand, e, rnd, c["U"]))
    return {"title": "Total of all the measurements", "items": its}


# ============================================================ set 5: redistribute equally + multi-step
D8, D16, D32 = {2, 4, 8}, {4, 8, 16}, {16, 32}
SHARE = ["beakers", "juice", "trail", "ribbon", "paint", "sand", "yarn"]
NICE = {2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32}


def share_plot(rnd, c, used, N, dens, whole=False):
    for _ in range(40000):
        n = rnd.choice([4, 5, 6])
        try:
            s, st, cn = make_plot(rnd, c["lo"], c["hi"], 1, n, lambda s, c: c[0] > 0 and c[-1] > 0, tot=(N, N))
        except RuntimeError:
            continue
        V = vals(s, st, cn)
        T = sum(cn[i] * E(V[i]) for i in range(len(cn)))
        R = T / N
        cols = sum(1 for x in cn if x)
        if R.denominator not in dens or (s, tuple(cn)) in used:
            continue
        if whole != (T.denominator == 1):
            continue
        if cols == N or R == E(V[cn.index(max(cn))]) or R == T / cols:
            continue
        used.add((s, tuple(cn)))
        return s, st, cn, V, N, T, R
    raise RuntimeError("no share plot %s %d" % (c["key"], N))


def share_cands(T, N, V, cn, R):
    cols = sum(1 for x in cn if x)
    m = cn.index(max(cn))
    return [T, T / cols, F(N) / T, E(V[m]), (T - E(V[0])) / N, T / (N + 1), (E(V[0]) + E(V[-1])) / 2,
            T / (N - 1), R * 2]


def set_share(rnd, P, CC):
    its = []
    used = set()
    keys = SHARE[:]
    rnd.shuffle(keys)
    # A: redistribute equally (12)
    plan = [(8, D8, True), (6, {2, 3, 6}, True), (8, D16, False), (10, {2, 5, 10}, True), (4, D16, False),
            (12, {3, 4, 6, 12}, True), (8, D32, False), (6, D16, False), (10, D16, False), (8, {32}, False),
            (12, D16 | {32}, False), (4, {32}, False)]
    for (N, dens, wh), key in zip(plan, (keys * 2)[:12]):
        c = BY[key]
        s, st, cn, V, N, T, R = share_plot(rnd, c, used, N, dens, wh)
        who = who_of(P, rnd)
        q = pic(c, s, st, cn) + intro(c, who, N) + " " + c["share"].format(n=N)
        pairs = [(cn[i], E(V[i])) for i in range(len(cn)) if cn[i]]
        e = ("Step 1: find the total. " + strip_b(e_products(pairs, c["U"])) +
             " Step 2: divide by the number of %s, %d (the number of X's, not the number of marks). " % (c["p"], N) +
             bold_end(e_divide(T, N, c["U"]), R, c["U"]))
        its.append(mcq_f(q, R, share_cands(T, N, V, cn, R), e, rnd, c["U"]))
    cont = [k for k in keys if BY[k].get("stuff")]
    # B1: how much less the fullest one would hold (2)
    for key in cont[:2]:
        c = BY[key]
        while True:
            s, st, cn, V, N, T, R = share_plot(rnd, c, used, rnd.choice([6, 8, 10]), D16, False)
            a = E(V[-1])
            if a > R:
                break
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, N) +
             " If all the %s were shared equally among the %d %s, how much less %s would the fullest %s hold than it does now?"
             % (c["stuff"], N, c["p"], c["stuff"], c["s"]))
        pairs = [(cn[i], E(V[i])) for i in range(len(cn)) if cn[i]]
        e = ("Step 1: total. %s Step 2: share. %s Step 3: the fullest %s holds %s now. %s"
             % (strip_b(e_products(pairs, c["U"])), e_divide(T, N, c["U"]), c["s"], amt(a, c["U"]), e_sub(a, R, c["U"])))
        its.append(mcq_f(q, a - R, [R, a, a - E(V[0]), R - E(V[0]), a + R, T - a], e, rnd, c["U"]))
    # B2: how much more the one with the least would hold (2)
    for key in cont[2:4]:
        c = BY[key]
        while True:
            s, st, cn, V, N, T, R = share_plot(rnd, c, used, rnd.choice([6, 8, 10]), D16, False)
            a = E(V[0])
            if R > a:
                break
        who = who_of(P, rnd)
        q = (pic(c, s, st, cn) + intro(c, who, N) +
             " If all the %s were shared equally among the %d %s, how much more %s would the %s with the least %s hold than it does now?"
             % (c["stuff"], N, c["p"], c["stuff"], c["s"], c["stuff"]))
        pairs = [(cn[i], E(V[i])) for i in range(len(cn)) if cn[i]]
        e = ("Step 1: total. %s Step 2: share. %s Step 3: the %s with the least holds %s now. %s"
             % (strip_b(e_products(pairs, c["U"])), e_divide(T, N, c["U"]), c["s"], amt(a, c["U"]), e_sub(R, a, c["U"])))
        its.append(mcq_f(q, R - a, [R, a, E(V[-1]) - R, E(V[-1]) - a, R + a, T - a], e, rnd, c["U"]))
    # B3: how much more is needed so each holds a target amount (2)
    for key, target in [("beakers", F(1, 2)), ("juice", F(1))]:
        c = BY[key]
        while True:
            s, st, cn, V, N, T, R = share_plot(rnd, c, used, rnd.choice([6, 8, 10]), D16 | {2, 3, 5}, rnd.random() < 0.5)
            if E(V[-1]) <= target and T < target * N and T != target * N - T:
                break
        n, he, his = P.next()
        need = target * N - T
        q = (pic(c, s, st, cn) + intro(c, n, N) + " %s wants every %s to hold %s. How much more %s does %s need in all?"
             % (cap(he), c["s"], amt(target, c["U"]), c["stuff"], he))
        pairs = [(cn[i], E(V[i])) for i in range(len(cn)) if cn[i]]
        e = ("Step 1: the goal is %d × %s = %s. Step 2: the %s hold %s now. %s Step 3: %s"
             % (N, show(target), amt(target * N, c["U"]), c["p"], amt(T, c["U"]), strip_b(e_products(pairs, c["U"])),
                e_sub(target * N, T, c["U"])))
        its.append(mcq_f(q, need, [target * N, T, target - R, F(N) - T, need + target, need - target], e, rnd, c["U"]))
    # B4: part of the data shared among friends (2)
    for key, m in [("trail", 3), ("ribbon", 4)]:
        c = BY[key]
        for _ in range(4000):
            s, st, cn = make_plot(rnd, c["lo"], c["hi"], 1, 6, lambda s, c: c[0] > 0 and c[-1] > 0, tot=(8, 12))
            V = vals(s, st, cn)
            k = rnd.choice(range(1, 4))
            pairs = [(cn[i], E(V[i])) for i in range(k + 1, len(cn)) if cn[i]]
            if not pairs or not V[k] % 8 or len(pairs) < 2:
                continue
            T = sum(a * v for a, v in pairs)
            if (T / m).denominator in (2, 4, 8, 16) and T.denominator > 1:
                break
        n, he, his = P.next()
        a_k = amt(E(V[k]), c["U"])
        if key == "trail":
            q = (pic(c, s, st, cn) + intro(c, n, sum(cn)) +
                 " %s pours together the trail mix from the bags that hold more than %s and shares it equally among %d friends. "
                 "How much trail mix does each friend get?" % (n, a_k, m))
        else:
            q = (pic(c, s, st, cn) + intro(c, n, sum(cn)) +
                 " %s sews together the pieces that are longer than %s and cuts the new ribbon into %d equal parts. "
                 "How long is each part?" % (n, a_k, m))
        e = ("Step 1: use only the X's to the right of %s. %s Step 2: divide by %d. %s"
             % (num(V[k]), strip_b(e_products(pairs, c["U"])), m, bold_end(e_divide(T, m, c["U"]), T / m, c["U"])))
        allT = sum(cn[i] * E(V[i]) for i in range(len(cn)))
        its.append(mcq_f(q, T / m, [T, allT / m, (T + cn[k] * E(V[k])) / m, T / sum(a for a, _ in pairs),
                                    sum(v for _, v in pairs) / m], e, rnd, c["U"]))
    assert len(its) == 20, len(its)
    return {"title": "Share equally and word problems", "items": its}


def strip_b(s):
    return s.replace("<b>", "").replace("</b>", "")


def bold_end(t, R, U):
    tail = "%s %s." % (show(R), uw(R, U))
    assert t.endswith(tail), (t, tail)
    return t[:-len(tail)] + "<b>%s</b>." % amt(R, U)


# ============================================================ lesson
LS = 1
LC = [2, 2, 1, 1, 1, 1]          # 1/8 to 3/4 liter: 8 beakers, 3 liters in all, 3/8 liter each


def body_html():
    V = [LS + i for i in range(len(LC))]
    U = L
    pairs = [(LC[i], E(V[i])) for i in range(len(LC))]
    T = sum(k * v for k, v in pairs)
    N = sum(LC)
    assert T == 3 and N == 8 and T / N == F(3, 8)
    plot = plot_svg(LS, 1, LC, "Water (liters)", "water in 8 beakers in liters")
    rows = [[xs(k), num(V[i]), "%d × %s = %s" % (k, num(V[i]), fr(k * V[i], 8))] for i, k in enumerate(LC)]
    rows.append(["8 X's", "", "<b>" + " + ".join(str(k * V[i]) for i, k in enumerate(LC)) + " = 24 eighths = 3 liters</b>"])
    return (
        "<h2>What a line plot shows</h2>"
        "<p>A line plot is a number line with an <b>X</b> for each measurement. "
        "When a value repeats, the X's stack up. Mark the number line in <b>eighths</b> when the data has eighths, "
        "and label each mark in simplest form: " + fr(2, 8) + " is " + fr(1, 4) + ", " + fr(4, 8) + " is " + fr(1, 2) +
        ", " + fr(6, 8) + " is " + fr(3, 4) + ".</p>"
        "<p>A class poured water into 8 identical beakers. The amounts in liters are: " +
        ", ".join(num(v) for v in [3, 1, 6, 2, 4, 1, 5, 2]) + ".</p>"
        "<figure class='sn-fig'>" + plot +
        "<figcaption>8 beakers, 8 X's. Two beakers hold " + fr(1, 8) + " liter and two hold " + fr(1, 4) +
        " liter.</figcaption></figure>"
        "<h2>Find the total of all the data</h2>"
        "<p>Each X is one beaker. For each mark, multiply the <b>number of X's</b> by the <b>value</b>. Then add the results "
        "with a common denominator.</p>" +
        table(["X's", "Value", "Count × value"], rows) +
        "<h2>Redistribute equally</h2>"
        "<p>“If the water were shared equally” means: find the total, then <b>divide by the number of items</b> "
        "(the number of X's).</p>" +
        ex("Example", "If all the water were poured together and shared equally among the 8 beakers, how much water would each beaker contain?",
           "Total: 3 liters. There are 8 beakers, so 3 ÷ 8 = " + fr(3, 8) + ".", fr(3, 8) + " liter") +
        ex("Example", "Another set of 4 beakers holds " + fr(1, 2) + ", " + fr(3, 8) + ", " + fr(3, 8) + " and " + fr(3, 4) +
           " liter. If the water were shared equally, how much would each beaker contain?",
           "Total in eighths: " + fr(4, 8) + " + " + fr(3, 8) + " + " + fr(3, 8) + " + " + fr(6, 8) + " = " + fr(16, 8) +
           " = 2 liters. Then 2 ÷ 4 = " + fr(2, 4) + " = " + fr(1, 2) + ".", fr(1, 2) + " liter") +
        "<p>When the total is not a whole number, multiply by a unit fraction: " + fr(9, 4) + " ÷ 8 = " + fr(9, 4) + " × " +
        fr(1, 8) + " = " + fr(9, 32) + ". Write every answer in simplest form.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Dividing by the number of marks (6)", "Divide by the number of X's (8 beakers)"],
            ["Adding each value once: " + fr(1, 8) + " + " + fr(1, 4) + " + … ", "Multiply each value by its number of X's first"],
            ["Stopping at the total (3 liters)", "“Shared equally” means divide the total by the number of items"],
            ["Adding the denominators: " + fr(1, 2) + " + " + fr(3, 8) + " = " + fr(4, 10), "Rename first: " + fr(4, 8) + " + " + fr(3, 8) + " = " + fr(7, 8)],
            ["Reading " + fr(3, 8) + " as " + fr(3, 4), "Look at the bottom number: eighths are smaller than fourths"],
            ["Using the ends of the number line as the greatest and least", "Use the X's farthest to the right and left"],
        ])
    )


FAQ = [
    {"q": "What is 5.MD.B.2 in 5th grade math?",
     "a": "It asks students to make line plots of measurements in halves, fourths and eighths and to solve problems with the data using fraction operations, such as finding a total or sharing the total equally."},
    {"q": "How do you redistribute equally on a line plot?",
     "a": "Find the total of all the measurements, then divide it by the number of items (X's). For 8 beakers holding 3 liters in all, each beaker would contain 3 ÷ 8 = 3/8 liter."},
    {"q": "How do you find the total of the data on a line plot with fractions?",
     "a": "Multiply each value by the number of X's above it, then add the results using a common denominator. Four X's at 3/8 give 4 × 3/8 = 12/8 = 1 1/2."},
    {"q": "How is the 5th grade line plot standard different from 4th grade?",
     "a": "In 4th grade students add and subtract fractions with like denominators from a line plot. In 5th grade they also use unlike denominators, multiplication and division, such as sharing a total equally."},
]


def gen_unit():
    rnd = random.Random(517)
    P = People(rnd)
    sets = [set_read(rnd, P, Ctx(rnd)), set_make(rnd, P, Ctx(rnd)), set_unlike(rnd, P, Ctx(rnd)),
            set_total(rnd, P, Ctx(rnd)), set_share(rnd, P, Ctx(rnd))]
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    balance(sets, rnd)
    for s in sets:
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
    return {
        "country": "us", "subject": "math", "grade": "grade-5", "slug": "line-plots-fractions", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Line Plots with Fractions: Totals and Fair Shares",
        "seo_title": "Grade 5 Line Plots with Fractions Worksheets: Unlike Denominators, Total of the Data and Redistribute Equally",
        "short_title": "Line Plots with Fractions",
        "domain": "Measurement and Data",
        "standard_code": "5.MD.B.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/5/MD/B/2/",
        "standard_text": "Make a line plot to display a data set of measurements in fractions of a unit (1/2, 1/4, 1/8). Use operations on fractions for this grade to solve problems involving information presented in line plots. For example, given different measurements of liquid in identical beakers, find the amount of liquid each beaker would contain if the total amount in all the beakers were redistributed equally.",
        "meta_desc": "Free Grade 5 line plot worksheets with fractions: read and make line plots in eighths, add and subtract with unlike denominators, find the total of the data with count × value, and redistribute equally (fair share) like the beaker problem. 100 practice questions with answers.",
        "key_big": "Total = each value × its number of X's, added up. Fair share = total ÷ number of X's.",
        "key_sub": "8 beakers holding 3 liters in all: each would contain 3 ÷ 8 = 3/8 liter. Rename to a common denominator before adding or subtracting, and divide by the number of items, not the number of marks.",
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
