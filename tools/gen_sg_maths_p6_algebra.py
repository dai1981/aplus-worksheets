# -*- coding: utf-8 -*-
"""
Singapore Primary 6 Maths: Algebra (MOE 2021 Primary Mathematics Syllabus, Standard Mathematics)
  python3 tools/gen_sg_maths_p6_algebra.py
Using a letter for an unknown number, writing and reading simple algebraic expressions, simplifying linear
expressions without brackets, evaluating by substitution, solving simple linear equations with whole number
coefficients, and PSLE-style word problems (model method, before-and-after, units and parts).
Wrong choices come from real mistakes: 3n read as 3 + n or as the 2-digit number 34 when n = 4, 4a + 3 = 7a,
n/4 written as 4/n, "8 less than y" written as 8 − y, sign errors when collecting like terms, working in the
wrong order when solving (3x + 5 = 20 gives 8 1/3 or 15), and giving the wrong person's amount in a model.
Every answer is checked in code with fractions.Fraction; expressions are compared at several values.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-6")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
EXTRA = "#f6dcc0"
ORANGE = "#d9822b"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """MOE style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
    v = Fr(v)
    neg = v < 0
    v = abs(v)
    for k in range(0, 6):
        t = v * 10 ** k
        if t.denominator == 1:
            w, r = divmod(t.numerator, 10 ** k)
            s = str(w)
            if len(s) >= 5:
                g = []
                while s:
                    g.insert(0, s[-3:])
                    s = s[:-3]
                s = NBSP.join(g)
            if k:
                s += "." + str(r).rjust(k, "0")
            return (M if neg else "") + s
    raise ValueError(v)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (a, b)


def rat(v):
    """Whole number, terminating decimal (up to 2 dp) or mixed number."""
    v = Fr(v)
    if v.denominator == 1:
        return n(v)
    if (v * 100).denominator == 1:
        return n(v)
    sg = M if v < 0 else ""
    w, r = divmod(abs(v.numerator), v.denominator)
    return sg + ("%d" % w + NBSP if w else "") + fr(r, v.denominator)


def sgd(v):
    """Singapore money: 85¢, $4, $4.50."""
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1 and c.numerator > 0 and c.numerator % 5 == 0, v
    c = c.numerator
    if c < 100:
        return "%d¢" % c
    if c % 100 == 0:
        return "$" + n(c // 100)
    return "$%s.%02d" % (n(c // 100), c % 100)


def plain(s):
    s = s.replace("<span class='fd'>", "/")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s).replace(NBSP, " ")).strip()


# ------------------------------------------------------------ expressions
# Plain syntax: "3x + 5", "[n|4]" is the fraction n over 4, "-" is a minus sign.
def _one(t):
    t = t.replace("-", M).replace("*", "×")
    return re.sub(r"[A-Za-z]", lambda m: "<i>%s</i>" % m.group(), t)


def X(s):
    out = []
    for p in re.split(r"(\[[^\]]*\])", s):
        if p.startswith("["):
            a, b = p[1:-1].split("|")
            out.append(fr(_one(a), _one(b)))
        else:
            out.append(_one(p))
    return "".join(out)


def E(s):
    """Text with expressions in braces: 'Simplify {3n + 5}' -> the braces become X(...)."""
    return re.sub(r"\{([^{}]*)\}", lambda m: X(m.group(1)), s.replace(" - ", " " + M + " "))


def ev(expr_, **env):
    """Exact value of a plain expression with the letters given in env."""
    t = re.sub(r"\[([^|\]]*)\|([^\]]*)\]", r"((\1)/(\2))", expr_)
    t = t.replace(M, "-").replace("×", "*").replace("÷", "/").replace(" ", "")
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Q('%s')" % m.group(), t)
    t = re.sub(r"(\)|[a-z])(?=[a-zQ(])", r"\1*", t)
    e = {"Q": Fr}
    for k, v in env.items():
        e[k] = Fr(v)
    return eval(t, {"__builtins__": {}}, e)


def same(a, b):
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2), 11):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, disp=None):
    """Correct first; positions are spread later by balance(). Equal values and equal texts are rejected."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, str(correct)
    seen, vals, pick = {plain(cs)}, {cv}, []
    for c in cands:
        if disp is not None:
            c = Fr(c)
            assert c not in vals, (q, c)
            vals.add(c)
            c = disp(c)
        c = str(c)
        assert plain(c) not in seen, (q, c)
        seen.add(plain(c))
        pick.append(c)
    assert len(pick) == 3, (q, cs, cands)
    return {"q": q, "c": [cs] + pick, "a": 0, "e": e}


def emcq(q, good, bad, e, src):
    """Expression choices (plain syntax). good must equal src; no two choices may be equivalent."""
    assert same(good, src), (src, good)
    allx = [good] + bad
    for i in range(4):
        for j in range(i + 1, 4):
            assert not same(allx[i], allx[j]), (allx[i], allx[j])
    return mcq(E(q), X(good), [X(b) for b in bad], E(e))


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it_, t in zip(s["items"], targets):
            c = it_["c"]
            wrong = [x for i, x in enumerate(c) if i != it_["a"]]
            rnd.shuffle(wrong)
            right = c[it_["a"]]
            it_["c"] = wrong[:t] + [right] + wrong[t:]
            it_["a"] = t


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def svgm(t):
    """SVG text with single letters in italics (tspan, no HTML tags in SVG)."""
    t = t.replace("-", M)
    return re.sub(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", r"<tspan font-style='italic'>\1</tspan>", t)


def tw(t, fs):
    return len(re.sub(r"<[^>]+>", "", t)) * fs * 0.58


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK, math_=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, svgm(t) if math_ else t))


def bar_svg(rows, label, unit=46, top=None, bottom=None, total=None):
    """Bar model. rows: [(name, [(units, text, style)])], style 'u' (unit) or 'x' (extra part).
    top: (u0, u1, text) bracket over row 0; bottom: (u0, u1, text) bracket under the last row;
    total: text beside a bracket on the right that spans all the rows."""
    BH, GAP = 34, 16
    namew = max(tw(r[0], 16) for r in rows) + 12
    x0 = 6 + namew
    y0 = 6 + (30 if top else 0)
    s = []
    maxw = 0
    for i, (name, segs) in enumerate(rows):
        y = y0 + i * (BH + GAP)
        s.append(text(x0 - 8, y + BH / 2 + 6, name, 16, "end"))
        x = x0
        for u, t, st in segs:
            w = u * unit
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, w, BH, FILL if st == "u" else EXTRA, GREEN if st == "u" else ORANGE))
            if t:
                s.append(text(x + w / 2, y + BH / 2 + 6, t, 16))
            x += w
        maxw = max(maxw, x - x0)
    ylast = y0 + (len(rows) - 1) * (BH + GAP)
    H = ylast + BH + 6
    if top:
        a, b, t = top
        xa, xb = x0 + a * unit, x0 + b * unit
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, y0 - 4, xa, y0 - 12, xb, y0 - 12, xb, y0 - 4, INK))
        s.append(text((xa + xb) / 2, y0 - 17, t, 16, col=RED if t == "?" else INK))
    if bottom:
        a, b, t = bottom
        xa, xb = x0 + a * unit, x0 + b * unit
        yb = ylast + BH
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d L%.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                 % (xa, yb + 4, xa, yb + 12, xb, yb + 12, xb, yb + 4, INK))
        s.append(text((xa + xb) / 2, yb + 30, t, 16, col=RED if t == "?" else INK))
        H = yb + 36
    W = x0 + maxw + 6
    if total:
        xr = x0 + maxw + 8
        ya, yb = y0, ylast + BH
        ym = (ya + yb) / 2
        s.append("<path d='M%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f' "
                 "fill='none' stroke='%s' stroke-width='2'/>"
                 % (xr, ya, xr + 8, ya, xr + 8, ya + 8, xr + 8, ym - 6, xr + 14, ym, xr + 8, ym + 6,
                    xr + 8, yb - 8, xr + 8, yb, xr, yb, INK))
        s.append(text(xr + 20, ym + 6, total, 16, "start", col=RED if total == "?" else INK))
        W = xr + 20 + tw(total, 16) + 8
    return svg_wrap(W, H, "".join(s), "bar model: " + label)


def rect_svg(top, side, label, w=150, h=70):
    L, T = 12, 28
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, top, 16))
    s.append(text(L + w + 8, T + h / 2 + 6, side, 16, "start"))
    return svg_wrap(L + w + 8 + tw(side, 16) + 8, T + h + 6, "".join(s), label)


def tri_svg(a, b, c, label):
    """Triangle; a = left side, b = right side, c = base."""
    A, B, C = (60, 112), (250, 112), (110, 14)
    s = ["<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2'/>" % (A + B + C + (FILL, GREEN))]
    s.append(text(78, 62, a, 16, "end"))
    s.append(text(188, 58, b, 16, "start"))
    s.append(text(155, 134, c, 16))
    W = max(188 + tw(b, 16), 260) + 8
    return svg_wrap(W, 142, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for x in s["items"]:
            x["q"] = rx.sub("<svg data-pf='lg' ", x["q"])
    return u


# ============================================================ set 1: write and read expressions
def set_write():
    its = []
    A = its.append

    A(emcq("Write an expression for <b>5 more than {n}</b>.", "n + 5", ["5n", "n - 5", "5 - n"],
           "5 more than {n} means add 5 to {n}: <b>{n + 5}</b>. {5n} means 5 × {n}, which is not the same.",
           "n + 5"))
    A(emcq("Write an expression for <b>3 times {n}</b>.", "3n", ["n + 3", "[n|3]", "3 - n"],
           "3 times {n} is 3 × {n}. We leave out the × sign and write the number first: <b>{3n}</b>.",
           "3*n"))
    A(emcq("Write an expression for <b>{n} divided by 4</b>.", "[n|4]", ["[4|n]", "4n", "n - 4"],
           "{n} ÷ 4 is written as a fraction with {n} on top: <b>{[n|4]}</b>. {[4|n]} means 4 ÷ {n}, the wrong way round.",
           "n/4"))
    A(emcq("Write an expression for <b>subtract 7 from {p}</b>.", "p - 7", ["7 - p", "p + 7", "7p"],
           "Start with {p} and take away 7: <b>{p - 7}</b>. {7 - p} takes {p} away from 7.", "p - 7"))
    A(emcq("Write an expression for <b>8 less than {y}</b>.", "y - 8", ["8 - y", "y + 8", "8y"],
           "8 less than {y} means start with {y} and take away 8: <b>{y - 8}</b>. "
           "A common mistake is to write the numbers in the order they are read: {8 - y}.", "y - 8"))
    A(emcq("Write an expression for <b>the product of 6 and {k}</b>.", "6k", ["6 + k", "k - 6", "[k|6]"],
           "Product means multiply: 6 × {k} = <b>{6k}</b>.", "6*k"))
    A(emcq("Write an expression for <b>take {m} away from 20</b>.", "20 - m", ["m - 20", "20m", "20 + m"],
           "Start with 20 and take {m} away: <b>{20 - m}</b>.", "20 - m"))
    A(emcq("Write an expression for <b>1 less than twice {n}</b>.", "2n - 1", ["1 - 2n", "2n + 1", "n - 1"],
           "Twice {n} is {2n}. 1 less than that is <b>{2n - 1}</b>. {n - 1} forgets to double {n}.", "2*n - 1"))
    A(mcq(E("What does {3n} mean?"), "3 × " + X("n"), ["3 + " + X("n"), "30 + " + X("n"), X("n") + " ÷ 3"],
          E("A number written next to a letter means multiply: <b>{3n} = 3 × {n}</b>. If {n} = 4, then {3n} = 12, not 34 and not 7.")))
    A(emcq("Which expression is the same as <b>{y + y + y + y}</b>?", "4y", ["y + 4", "3y", "5y"],
           "There are 4 groups of {y}, so {y + y + y + y} = <b>{4y}</b>. {y + 4} adds the number 4 instead.", "y+y+y+y"))
    A(mcq(E("Which means the same as {[n|4]}?"), X("n ÷ 4"), [X("4 ÷ n"), X("n × 4"), X("n - 4")],
          E("A fraction bar means divide: {[n|4]} = <b>{n} ÷ 4</b>. {[4|n]} would be 4 ÷ {n}.")))
    A(mcq(E("Which words match <b>{10 - k}</b>?"), E("{k} subtracted from 10"),
          [E("10 subtracted from {k}"), E("10 times {k}"), E("{k} added to 10")],
          E("{10 - k} starts with 10 and takes {k} away: <b>{k} subtracted from 10</b>. "
            "“10 subtracted from {k}” would be {k - 10}.")))
    # value of 3n when n = 4
    assert ev("3n", n=4) == 12
    A(mcq(E("Ravi says that when {n} = 4, {3n} = 34. What is the correct value of {3n}?"), 12, [34, 7, 43],
          E("{3n} means 3 × {n} = 3 × 4 = <b>12</b>. Ravi wrote 3 and 4 side by side, which is wrong."), n))
    A(emcq("A pen costs ${k}. What is the cost of 6 pens, in dollars?", "6k", ["k + 6", "[k|6]", "[6|k]"],
           "Each pen costs ${k}, so 6 pens cost 6 × {k} = <b>${6k}</b>. {k + 6} adds $6 instead of multiplying.", "6*k"))
    A(emcq("Siti is {w} years old. Her brother is 3 years older than Siti. How old is her brother?",
           "w + 3", ["w - 3", "3w", "3 - w"],
           "Older means more years: <b>{w + 3}</b>. {w - 3} would make him younger.", "w + 3"))
    A(emcq("A ribbon is {m} cm long. Mrs Lim cuts it into 3 equal pieces. How long is each piece, in centimetres?",
           "[m|3]", ["[3|m]", "3m", "m - 3"],
           "Cutting into 3 equal pieces means dividing by 3: <b>{[m|3]}</b> cm. {3m} would make each piece longer than the ribbon.",
           "m/3"))
    A(emcq("Ali had $20. He spent ${y} at the bookshop. How much money did he have left, in dollars?",
           "20 - y", ["y - 20", "20 + y", "[20|y]"],
           "Start with $20 and take away ${y}: <b>{20 - y}</b> dollars. {y - 20} is the wrong way round.", "20 - y"))
    A(emcq("Mrs Ng buys 5 boxes with {n} oranges in each box. She gives away 2 oranges. How many oranges does she have left?",
           "5n - 2", ["2 - 5n", "5n + 2", "n + 3"],
           "5 boxes of {n} oranges is {5n} oranges. She gives away 2, so she has <b>{5n - 2}</b> left. "
           "{n + 3} adds 5 and takes away 2 instead of multiplying by 5.", "5*n - 2"))
    # bar model: 4 times as many
    f = bar_svg([("Mei Ling", [(1, "p", "u")]), ("Jun Jie", [(1, "p", "u"), (1, "p", "u"), (1, "p", "u"), (1, "p", "u")])],
                "Mei Ling 1 unit p, Jun Jie 4 units p, the question mark covers 3 units", bottom=(1, 4, "?"))
    A(emcq(fig(f) + "Mei Ling has {p} stickers. Jun Jie has 4 times as many stickers as Mei Ling. "
           "How many more stickers does Jun Jie have than Mei Ling?", "3p", ["4p", "p + 4", "5p"],
           "Jun Jie has 4 units and Mei Ling has 1 unit. The difference is 4 " + M + " 1 = 3 units: <b>{3p}</b>. "
           "{4p} is how many Jun Jie has; {5p} is how many they have altogether.", "4*p - p"))
    A(emcq("Mr Tan is {t} years old now. What was his age 9 years ago?", "t - 9", ["t + 9", "9 - t", "9t"],
           "9 years ago he was 9 years younger: <b>{t - 9}</b>. {t + 9} is his age in 9 years’ time.", "t - 9"))
    order = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 11, 7, 13, 14, 15, 16, 19, 17, 18]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Write and read expressions", "items": its}


# ============================================================ set 2: simplify
def set_simplify():
    its = []
    A = its.append

    def sx(src, good, bad, e, pre=""):
        A(emcq(pre + "Simplify <b>{%s}</b>." % src, good, bad, e, src))

    sx("a + a + a", "3a", ["a + 3", "2a", "4a"],
       "There are 3 groups of {a}: {a + a + a} = <b>{3a}</b>. It is not {a + 3}.")
    sx("4a + 3a", "7a", ["12a", "7", "a"],
       "4 groups of {a} and 3 more groups of {a} make 7 groups of {a}: <b>{7a}</b>. Add the numbers in front; do not multiply them (not {12a}).")
    sx("9b - 4b", "5b", ["13b", "5", "36b"],
       "9 groups of {b} take away 4 groups of {b} leave <b>{5b}</b>. Keep the letter: the answer is not just 5.")
    sx("6k - k", "5k", ["6", "5", "7k"],
       "{k} means 1{k}. So {6k - k} = 6{k} " + M + " 1{k} = <b>{5k}</b>. It is not 6: only one {k} is taken away.")
    sx("4a + 3a - 2", "7a - 2", ["5a", "7a + 2", "9a"],
       "Collect the {a} terms: {4a + 3a} = {7a}. The number 2 is not a like term, so it stays: <b>{7a - 2}</b>. "
       "{5a} wrongly takes 2 away from {7a}.")
    A(mcq(E("Which is <b>{4a + 3}</b> in its simplest form?"), E("{4a + 3}"), [E("{7a}"), "7", E("{12a}")],
          E("{4a} and 3 are not like terms: one has the letter {a} and the other is a number. So <b>{4a + 3}</b> cannot be "
            "simplified. {4a + 3} = {7a} is a very common mistake. Check with {a} = 10: {4a + 3} = 43 but {7a} = 70.")))
    sx("8m + 2 - 3m", "5m + 2", ["11m + 2", "7m", "5m - 2"],
       "{8m - 3m} = {5m}. Then add the 2: <b>{5m + 2}</b>. The minus sign belongs to {3m}, so it is not {11m + 2}.")
    sx("7 + 2n + 5", "2n + 12", ["14n", "9n + 5", "2n + 2"],
       "Collect the numbers: 7 + 5 = 12. The {n} term is {2n}. So <b>{2n + 12}</b>. {14n} wrongly puts everything together.")
    sx("10p - 4 - 3p", "7p - 4", ["13p - 4", "3p", "7p + 4"],
       "{10p - 3p} = {7p}. The " + M + " 4 stays: <b>{7p - 4}</b>. {13p - 4} adds {3p} instead of taking it away.")
    sx("3x + 5x - 2x", "6x", ["10x", "8x - 2", "6"],
       "3 + 5 " + M + " 2 = 6, so <b>{6x}</b>. {10x} adds the {2x}. {8x - 2} forgets that 2{x} has a letter.")
    sx("5b + 3 - 2b + 6", "3b + 9", ["7b + 9", "3b - 3", "12b"],
       "Collect like terms. {b} terms: {5b - 2b} = {3b}. Numbers: 3 + 6 = 9. So <b>{3b + 9}</b>. "
       "{3b - 3} wrongly takes away the 6 as well: the minus sign is only in front of {2b}.")
    sx("9y - 2 + y + 7", "10y + 5", ["9y + 5", "10y + 9", "15y"],
       "{9y + y} = {10y} ({y} is 1{y}). Numbers: " + M + "2 + 7 = 5. So <b>{10y + 5}</b>. {9y + 5} forgets the {y}.")
    sx("12 + 4a - 5 + a", "5a + 7", ["4a + 7", "5a + 17", "12a"],
       "{a} terms: {4a + a} = {5a}. Numbers: 12 " + M + " 5 = 7. So <b>{5a + 7}</b>. {5a + 17} adds 5 instead of taking it away.")
    sx("6c - 2c + 4 - 1", "4c + 3", ["8c + 3", "4c + 5", "7c"],
       "{6c - 2c} = {4c} and 4 " + M + " 1 = 3. So <b>{4c + 3}</b>. {7c} puts the numbers and letters together.")
    A(emcq("Which expression is equal to <b>{5n}</b>?", "2n + 3n", ["2n + 3", "7n - 3", "n + 5"],
           "{2n + 3n} = <b>{5n}</b>. {2n + 3} cannot be simplified to {5n} because 3 has no {n}.", "5*n"))
    A(mcq(E("Which expression <b>cannot</b> be simplified?"), E("{3k + 2}"), [E("{3k + 2k}"), E("{5k - k}"), E("{k + k}")],
          E("<b>{3k + 2}</b> has a {k} term and a number, which are not like terms. The others simplify to {5k}, {4k} and {2k}.")))
    sx("15w - 6 - 9w + 2", "6w - 4", ["6w - 8", "24w - 4", "6w + 4"],
       "{w} terms: {15w - 9w} = {6w}. Numbers: " + M + "6 + 2 = " + M + "4. So <b>{6w - 4}</b>. {6w - 8} subtracts the 2.")
    sx("20 + 8h - 3h - 15", "5h + 5", ["11h + 5", "5h + 35", "10h"],
       "{8h - 3h} = {5h} and 20 " + M + " 15 = 5. So <b>{5h + 5}</b>. {5h + 35} adds the 15 instead of subtracting it.")
    # rectangle perimeter
    f = rect_svg("3a cm", "5 cm", "rectangle 3a cm by 5 cm")
    A(emcq(fig(f) + "A rectangle is {3a} cm long and 5 cm wide. Find its perimeter in simplest form, in centimetres.",
           "6a + 10", ["3a + 5", "16a", "15a"],
           "Perimeter = {3a + 5 + 3a + 5} = <b>{6a + 10}</b> cm. {3a + 5} goes only halfway round. "
           "{15a} is the area (3{a} × 5). {16a} wrongly adds the numbers and letters together.", "3a + 5 + 3a + 5"))
    f = tri_svg("m cm", "2m cm", "9 cm", "triangle with sides m cm, 2m cm and 9 cm")
    A(emcq(fig(f) + "The sides of a triangle are {m} cm, {2m} cm and 9 cm. Find its perimeter in simplest form, in centimetres.",
           "3m + 9", ["12m", "2m + 9", "3m"],
           "Perimeter = {m + 2m + 9} = <b>{3m + 9}</b> cm. {2m + 9} forgets that {m} is 1{m}. {3m} leaves out the 9 cm.",
           "m + 2m + 9"))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 11, 12, 13, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Simplify expressions", "items": its}


# ============================================================ set 3: evaluate by substitution
def set_evaluate():
    its = []
    A = its.append

    def cond(env):
        return " and ".join("{%s} = %s" % (k, n(v)) for k, v in env.items())

    def evq(s_, env, wrong, e, check, unit_=None):
        env = {k: Fr(v) for k, v in env.items()}
        ans = ev(s_, **env)
        assert ans == Fr(check), (s_, ans, check)
        q = E("Find the value of <b>{%s}</b> when %s." % (s_, cond(env)))
        A(mcq(q, ans, wrong, E(e), rat))

    evq("n + 9", {"n": 6}, [3, 54, 69], "Replace {n} with 6: 6 + 9 = <b>15</b>. 54 multiplies instead of adding. 69 writes 6 and 9 side by side.", 15)
    evq("4n", {"n": 7}, [47, 11, 74], "{4n} means 4 × {n}: 4 × 7 = <b>28</b>. Not 47: do not write 4 and 7 side by side. Not 11: do not add.", 28)
    evq("3a + 2", {"a": 5}, [37, 21, 10],
        "Multiply first: 3 × 5 = 15. Then add 2: <b>17</b>. 37 reads {3a} as 35. 21 adds 5 + 2 first.", 17)
    evq("[y|2]", {"y": 8}, [16, 6, Fr(1, 4)],
        "{[y|2]} means {y} ÷ 2: 8 ÷ 2 = <b>4</b>. 16 multiplies. 0.25 is 2 ÷ 8, the wrong way round.", 4)
    evq("5k - 4", {"k": 9}, [91, 25, 10],
        "5 × 9 = 45, then 45 " + M + " 4 = <b>41</b>. 91 reads {5k} as 95. 25 subtracts first: 5 × (9 " + M + " 4).", 41)
    evq("20 - 3p", {"p": 4}, [68, 13, 32],
        "Multiply first: 3 × 4 = 12. Then 20 " + M + " 12 = <b>8</b>. 68 works from left to right: 20 " + M + " 3 = 17, 17 × 4. "
        "32 adds 12 instead of subtracting.", 8)
    evq("7x - 2x", {"x": 3}, [5, 21, 19],
        "Simplify first: {7x - 2x} = {5x}. 5 × 3 = <b>15</b>. Or: 21 " + M + " 6 = 15. 19 does 21 " + M + " 2, forgetting the {x} in {2x}.", 15)
    evq("3n - 5", {"n": 10}, [305, 15, 8],
        "3 × 10 = 30, then 30 " + M + " 5 = <b>25</b>. 305 reads {3n} as 310. 15 subtracts first: 3 × (10 " + M + " 5).", 25)
    evq("[m|3] + 5", {"m": 12}, [Fr(3, 2), 41, 4],
        "Divide first: 12 ÷ 3 = 4. Then 4 + 5 = <b>9</b>. 1.5 adds first: 12 ÷ 8. 41 multiplies by 3. 4 forgets to add 5.", 9)
    evq("2y + 3y", {"y": 6}, [11, 5, 18],
        "{2y + 3y} = {5y} = 5 × 6 = <b>30</b>. 11 adds 2 + 3 + 6. 18 works out only {3y}.", 30)
    evq("18 - [c|2]", {"c": 4}, [7, 14, 20],
        "{[c|2]} = 4 ÷ 2 = 2. Then 18 " + M + " 2 = <b>16</b>. 7 subtracts first: (18 " + M + " 4) ÷ 2. 14 takes away 4, not 4 ÷ 2.", 16)
    evq("4r + 3 - r", {"r": 5}, [23, 7, 28],
        "Simplify: {4r - r} = {3r}, so {3r + 3} = 15 + 3 = <b>18</b>. 23 forgets the " + M + " {r}. 28 adds {r} instead of subtracting it.", 18)
    evq("100 - 7n", {"n": 8}, [744, 22, 156],
        "7 × 8 = 56, then 100 " + M + " 56 = <b>44</b>. 744 works from left to right. 22 reads {7n} as 78.", 44)
    evq("4a + b", {"a": 2, "b": 5}, [47, 28, 11],
        "4 × 2 = 8, then 8 + 5 = <b>13</b>. 28 adds first: 4 × 7. 11 adds 4 + 2 + 5.", 13)
    evq("3a - b", {"a": 6, "b": 2}, [34, 12, 7],
        "3 × 6 = 18, then 18 " + M + " 2 = <b>16</b>. 34 reads {3a} as 36. 12 subtracts first: 3 × 4.", 16)
    evq("5q - 2p", {"p": 3, "q": 7}, [43, 41, 33],
        "5 × 7 = 35 and 2 × 3 = 6. 35 " + M + " 6 = <b>29</b>. 43 reads them as 75 " + M + " 32. 41 adds 6. 33 forgets the {p}.", 29)
    # which is greatest when n = 3
    vals = {"20 - n": 17, "5n": 15, "n + 13": 16, "4n": 12}
    for k_, v in vals.items():
        assert ev(k_, n=3) == v
    A(mcq(E("When {n} = 3, which expression has the <b>greatest</b> value?"), E("{20 - n}"), [E("{5n}"), E("{n + 13}"), E("{4n}")],
          E("Work out each one: 20 " + M + " 3 = <b>17</b>, 5 × 3 = 15, 3 + 13 = 16, 4 × 3 = 12. "
            "Multiplying does not always give the biggest value.")))
    vals = {"2k + 2": 10, "k + 2": 6, "3k": 12, "20 - k": 16}
    for k_, v in vals.items():
        assert ev(k_, k=4) == v
    A(mcq(E("When {k} = 4, which expression has a value of 10?"), E("{2k + 2}"), [E("{k + 2}"), E("{3k}"), E("{20 - k}")],
          E("2 × 4 + 2 = 8 + 2 = <b>10</b>. The others give 6, 12 and 16.")))
    # rectangle
    f = rect_svg("2x cm", "7 cm", "rectangle 2x cm by 7 cm")
    assert ev("2*(2x + 7)", x=5) == 34
    A(mcq(fig(f) + E("A rectangle is {2x} cm long and 7 cm wide. Its perimeter is {4x + 14} cm. Find the perimeter when {x} = 5."),
          "34 cm", ["17 cm", "70 cm", "64 cm"],
          E("4 × 5 + 14 = 20 + 14 = <b>34 cm</b>. 17 cm goes only halfway round. 70 is the area (10 × 7), not the perimeter. "
            "64 cm reads {2x} as 25.")))
    assert ev("4t + 5", t=3) == 17
    A(mcq(E("Hiring a bicycle at East Coast Park costs {4t + 5} dollars for {t} hours. Find the cost for 3 hours."),
          sgd(17), [sgd(32), sgd(48), sgd(12)],
          E("4 × 3 = 12, then 12 + 5 = <b>$17</b>. $32 adds first: 4 × 8. $48 reads {4t} as 43. $12 forgets the $5.")))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 17, 13, 14, 15, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Evaluate by substitution", "items": its}


# ============================================================ set 4: solve simple equations
def solve(lhs, rhs, var):
    """Unique solution among Fractions k/d, checked by brute force."""
    cands = {Fr(k, d) for k in range(-50, 2500) for d in (1, 2, 3, 4, 5, 6, 10)}
    sol = [c for c in cands if ev(lhs, **{var: c}) == Fr(rhs)]
    assert len(sol) == 1, (lhs, rhs, sol)
    return sol[0]


def set_solve():
    its = []
    A = its.append

    def eq(lhs, rhs, var, ans, wrong, e):
        assert solve(lhs, rhs, var) == Fr(ans), (lhs, ans)
        q = E("Solve <b>{%s} = %s</b>. What is the value of {%s}?" % (lhs, n(rhs), var))
        A(mcq(q, Fr(ans), [Fr(w) for w in wrong], E(e), rat))

    eq("x + 8", 15, "x", 7, [23, 13, 120],
       "Take away 8 from both sides: {x} = 15 " + M + " 8 = <b>7</b>. Check: 7 + 8 = 15. 23 adds 8 instead. 13 takes 5 from 8 instead of renaming.")
    eq("y - 6", 14, "y", 20, [8, 84, 14],
       "Add 6 to both sides: {y} = 14 + 6 = <b>20</b>. Check: 20 " + M + " 6 = 14. 8 subtracts instead of adding.")
    eq("4n", 28, "n", 7, [24, 112, 32],
       "{4n} = 4 × {n}. Divide both sides by 4: {n} = 28 ÷ 4 = <b>7</b>. 24 subtracts 4 instead of dividing.")
    eq("7x", 63, "x", 9, [56, 441, 70],
       "Divide both sides by 7: {x} = 63 ÷ 7 = <b>9</b>. Check: 7 × 9 = 63. 441 multiplies instead.")
    eq("[m|5]", 6, "m", 30, [Fr(6, 5), 11, 1],
       "{[m|5]} = 6 means {m} ÷ 5 = 6. Multiply both sides by 5: {m} = <b>30</b>. 1.2 divides 6 by 5 instead.")
    eq("50 - x", 18, "x", 32, [68, 48, 42],
       "50 take away {x} leaves 18, so {x} = 50 " + M + " 18 = <b>32</b>. Check: 50 " + M + " 32 = 18. "
       "48 forgets to rename 1 ten as 10 ones.")
    eq("3x + 5", 20, "x", 5, [Fr(25, 3), 15, 65],
       "Take away 5 first: {3x} = 15. Then divide by 3: {x} = <b>5</b>. Check: 3 × 5 + 5 = 20. "
       "8 " + fr(1, 3) + " adds 5 instead of subtracting. 15 forgets to divide by 3.")
    eq("2y - 3", 11, "y", 7, [4, 14, 19],
       "Add 3 first: {2y} = 14. Then divide by 2: {y} = <b>7</b>. 4 subtracts 3 instead of adding. 14 forgets to divide.")
    eq("5k + 6", 41, "k", 7, [Fr(47, 5), 35, 211],
       "Take away 6: {5k} = 35. Divide by 5: {k} = <b>7</b>. 9.4 adds 6 instead of subtracting. 35 forgets to divide.")
    eq("4a - 7", 25, "a", 8, [Fr(9, 2), 32, 93],
       "Add 7: {4a} = 32. Divide by 4: {a} = <b>8</b>. 4.5 subtracts 7 instead of adding. 32 forgets to divide.")
    eq("6 + 2p", 30, "p", 12, [18, 24, 4],
       "Take away 6: {2p} = 24. Divide by 2: {p} = <b>12</b>. 18 adds 6. 4 reads {2p} as 20 + {p}.")
    eq("[n|3] + 4", 10, "n", 18, [42, 6, 2],
       "Take away 4: {[n|3]} = 6. Multiply by 3: {n} = <b>18</b>. 42 adds 4 instead of subtracting. 2 divides 6 by 3 instead of multiplying.")
    eq("[x|4] - 3", 5, "x", 32, [2, 8, Fr(1, 2)],
       "Add 3: {[x|4]} = 8. Multiply by 4: {x} = <b>32</b>. 8 forgets to multiply. 2 divides 8 by 4 instead.")
    eq("3x + 2x", 35, "x", 7, [16, 175, 30],
       "Simplify first: {3x + 2x} = {5x}. {5x} = 35, so {x} = <b>7</b>. 16 treats {3x + 2x} as 3 + {2x}. 175 multiplies.")
    eq("8y - 3y + 2", 27, "y", 5, [Fr(27, 5), Fr(29, 5), 25],
       "Simplify: {5y + 2} = 27. Take away 2: {5y} = 25. Divide by 5: {y} = <b>5</b>. 5.4 forgets the 2. 5.8 adds 2 instead of subtracting.")
    # which value makes it true
    assert solve("4x + 9", 33, "x") == 6
    A(mcq(E("Which value of {x} makes <b>{4x + 9} = 33</b> true?"), 6, [Fr(21, 2), 24, 141],
          E("Try it: 4 × 6 + 9 = 24 + 9 = 33. So {x} = <b>6</b>. 10.5 adds 9 instead of subtracting. 24 forgets to divide by 4."), rat))
    # word to equation
    A(emcq("I think of a number {n}. I multiply it by 6 and then subtract 5. The answer is 43. Which equation shows this?",
           "6n - 5", ["6 - 5n", "6n + 5", "5n - 6"],
           "Multiply {n} by 6 to get {6n}, then subtract 5: <b>{6n - 5} = 43</b>. {5n - 6} swaps the 6 and the 5.", "6*n - 5"))
    its[-1]["c"] = [c + " = 43" for c in its[-1]["c"]]
    # model for 3x + 4 = 19
    f = bar_svg([("", [(1, "x", "u"), (1, "x", "u"), (1, "x", "u"), (1, "4", "x")])], "3 units x and 4, total 19",
                top=(0, 4, "19"))
    assert solve("3x + 4", 19, "x") == 5
    A(mcq(fig(f) + E("The model shows <b>{3x + 4} = 19</b>. What is the value of {x}?"), 5, [Fr(23, 3), 15, 61],
          E("Take away the 4: 3 units = 19 " + M + " 4 = 15. 1 unit = 15 ÷ 3 = 5, so {x} = <b>5</b>. "
            "15 is 3 units, not 1 unit. 7 " + fr(2, 3) + " adds the 4 instead of taking it away."), rat))
    # find 5m
    m_ = solve("2m + 7", 19, "m")
    assert m_ == 6 and 5 * m_ == 30
    A(mcq(E("If {2m + 7} = 19, what is the value of {5m}?"), 30, [6, 56, 11],
          E("First find {m}: {2m} = 12, so {m} = 6. Then {5m} = 5 × 6 = <b>30</b>. 6 stops too early. 56 reads {5m} as 56. "
            "11 adds 5 + 6."), rat))
    k_ = solve("3k - 4", 26, "k")
    assert k_ == 10
    A(mcq(E("If {3k - 4} = 26, what is the value of {k + 12}?"), 22, [10, 42, 30],
          E("{3k} = 30, so {k} = 10. Then {k + 12} = <b>22</b>. 10 stops too early. 42 uses 30 for {k}: 30 is {3k}, not {k}."), rat))
    order = [0, 1, 2, 3, 4, 5, 16, 6, 7, 8, 9, 10, 11, 12, 17, 13, 14, 15, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "Solve simple equations", "items": its}


# ============================================================ set 5: PSLE-style word problems
def set_words():
    its = []
    A = its.append

    A(emcq("Mrs Lim buys {k} pens at $2 each and a file that costs $5. What is the total cost, in dollars?",
           "2k + 5", ["7k", "5k + 2", "2k - 5"],
           "{k} pens cost 2 × {k} = {2k} dollars. Add the file: <b>{2k + 5}</b>. {7k} wrongly joins 2{k} and 5.",
           "2*k + 5"))
    A(emcq("A pen costs ${k}. A notebook costs $3 more than the pen. Ali buys 2 pens and 1 notebook. "
           "What is the total cost, in dollars?", "3k + 3", ["2k + 3", "3k + 6", "6k"],
           "2 pens cost {2k}. The notebook costs {k + 3}. Total: {2k + k + 3} = <b>{3k + 3}</b>. "
           "{2k + 3} forgets that the notebook also costs {k}.", "2*k + (k + 3)"))
    f = bar_svg([("Siti", [(1, "n", "u")]), ("Wei Ming", [(1, "n", "u"), (1, "n", "u"), (1, "n", "u")])],
                "before: Siti 1 unit n, Wei Ming 3 units n")
    A(emcq(fig(f) + "Siti has {n} stickers. Wei Ming has 3 times as many stickers as Siti. Then Wei Ming gives 8 stickers to Siti. "
           "How many stickers does Wei Ming have now?", "3n - 8", ["3n + 8", "n + 8", "3n - 16"],
           "Before, Wei Ming has 3 units, {3n}. He gives away 8, so he has <b>{3n - 8}</b>. {n + 8} is how many Siti has now.",
           "3*n - 8"))
    before = (20, 60)
    after = (20 + 8, 60 - 8)
    assert after[1] - after[0] == 24
    A(mcq("Siti has 20 stickers. Wei Ming has 3 times as many stickers as Siti. Wei Ming gives 8 stickers to Siti. "
          "How many more stickers does Wei Ming have than Siti now?", 24, [40, 32, 80],
          "Before: Siti 20, Wei Ming 60. After: Wei Ming 60 " + M + " 8 = 52, Siti 20 + 8 = 28. 52 " + M + " 28 = <b>24</b>. "
          "40 is the difference before. 32 forgets that Siti gets the 8 stickers. 80 is the total.", rat))
    A(emcq("Mdm Wong had $50. She bought 4 kg of rambutans at ${y} per kg. How much money did she have left, in dollars?",
           "50 - 4y", ["4y - 50", "46y", "50 + 4y"],
           "4 kg cost 4 × {y} = {4y} dollars. Money left: <b>{50 - 4y}</b>. {46y} wrongly joins 50 and {4y}.", "50 - 4*y"))
    y = 9
    assert 50 - 4 * y == 14
    A(mcq(E("Mdm Wong had $50. She bought 4 kg of rambutans at ${y} per kg. Find the money she had left when {y} = 9."),
          sgd(14), [sgd(86), sgd(5), sgd(36)],
          E("Money left = {50 - 4y} = 50 " + M + " 4 × 9 = 50 " + M + " 36 = <b>$14</b>. $86 adds instead. "
            "$5 reads {4y} as 45. $36 is what she spent.")))
    A(emcq("Ali is {y} years old. His father is 4 times as old as Ali. What will be the sum of their ages in 5 years’ time?",
           "5y + 10", ["5y + 5", "4y + 5", "5y"],
           "Now: Ali {y}, father {4y}. In 5 years: {y + 5} and {4y + 5}. Sum: <b>{5y + 10}</b>. "
           "{5y + 5} adds the 5 years to only one person.", "(y + 5) + (4*y + 5)"))
    A(emcq("Mr Rahman is {m} years old. His son is 28 years younger than him. How old will his son be in 6 years’ time?",
           "m - 22", ["m - 34", "m + 34", "22 - m"],
           "The son is {m - 28} now. In 6 years: {m - 28 + 6} = <b>{m - 22}</b>. {m - 34} takes away the 6 years instead of adding.",
           "m - 28 + 6"))
    A(emcq("The length of a rectangular garden is 3 times its breadth. The breadth is {b} m. What is the perimeter, in metres?",
           "8b", ["4b", "6b", "3b + 2"],
           "Length {3b}, breadth {b}. Perimeter = {3b + b + 3b + b} = <b>{8b}</b>. {4b} goes only halfway round. "
           "{6b} adds the two lengths only.", "3*b + b + 3*b + b"))
    # model: 3 times as many, total 56
    f = bar_svg([("Xin Yi", [(1, "n", "u")]), ("Hui Min", [(1, "n", "u"), (1, "n", "u"), (1, "n", "u")])],
                "Xin Yi 1 unit, Hui Min 3 units, total 56", total="56")
    assert solve("n + 3n", 56, "n") == 14
    A(mcq(fig(f) + E("Xin Yi has {n} beads. Hui Min has 3 times as many beads as Xin Yi. They have 56 beads altogether. "
                     "Find the value of {n}."), 14, [42, Fr(56, 3), 28],
          E("{n + 3n} = 56, so 4 units = 56 and 1 unit = 56 ÷ 4 = 14. {n} = <b>14</b>. 42 is how many Hui Min has. "
            "18 " + fr(2, 3) + " divides by 3, but there are 4 units altogether."), rat))
    # Kumar 12 more than Raju, total 80
    f = bar_svg([("Raju", [(1.6, "r", "u")]), ("Kumar", [(1.6, "r", "u"), (0.8, "12", "x")])],
                "Raju r, Kumar r and 12 more, total 80", total="80")
    A(emcq(fig(f) + "Kumar has 12 more marbles than Raju. They have 80 marbles altogether. Raju has {r} marbles. "
           "Which equation is correct?", "2r + 12", ["r + 12", "12r", "2r - 12"],
           "Raju has {r} and Kumar has {r + 12}. Together: {r + r + 12} = <b>{2r + 12} = 80</b>. "
           "{r + 12} is only Kumar’s marbles.", "r + (r + 12)"))
    its[-1]["c"] = [c + " = 80" for c in its[-1]["c"]]
    assert solve("2r + 12", 80, "r") == 34
    A(mcq("Kumar has 12 more marbles than Raju. They have 80 marbles altogether. How many marbles does Raju have?",
          34, [46, 68, 40],
          "Take away the extra 12: 80 " + M + " 12 = 68. 2 units = 68, so 1 unit = <b>34</b>. "
          "46 is Kumar’s marbles. 68 forgets to divide by 2. 40 shares 80 equally and ignores the 12.", rat))
    A(emcq("An adult ticket costs ${a}. A child ticket costs $8 less than an adult ticket. "
           "Mr Kumar buys 2 adult tickets and 3 child tickets. What is the total cost, in dollars?",
           "5a - 24", ["5a - 8", "5a + 24", "5a - 16"],
           "2 adult tickets cost {2a}. 3 child tickets cost {3a} minus 3 × $8 = $24, so {3a - 24}. Total: <b>{5a - 24}</b>. "
           "{5a - 8} takes away $8 only once, but each of the 3 child tickets is $8 less.", "2*a + 3*(a - 8)"))
    assert ev("2*a + 3*(a - 8)", a=20) == 76
    A(mcq("An adult ticket costs $20. A child ticket costs $8 less than an adult ticket. "
          "Mrs Ng buys 2 adult tickets and 3 child tickets. How much does she pay?",
          sgd(76), [sgd(92), sgd(124), sgd(84)],
          "A child ticket costs $20 " + M + " $8 = $12. 2 × $20 + 3 × $12 = $40 + $36 = <b>$76</b>. "
          "$92 takes away $8 only once. $84 takes away $8 for only 2 children."))
    A(emcq("A plate of chicken rice costs ${c} and a drink costs $1.50. Farah buys 3 plates of chicken rice and 2 drinks. "
           "She pays with a $20 note. How much change does she get, in dollars?",
           "17 - 3c", ["3c - 17", "18.5 - 3c", "17 + 3c"],
           "She spends {3c} + 2 × 1.50 = {3c} + 3 dollars. Change: 20 " + M + " {3c} " + M + " 3 = <b>{17 - 3c}</b>. "
           "{18.5 - 3c} counts only 1 drink.", "20 - (3*c + 3)"))
    # before-and-after: halves
    x_ = solve("[x + 18|2]", 30, "x")
    assert x_ == 42
    A(mcq("Jun Jie had some stamps. He bought 18 more stamps. Then he gave half of all his stamps to his brother. "
          "He had 30 stamps left. How many stamps did he have at first?", 42, [78, 12, 48],
          "Work backwards. Before giving half away he had 30 × 2 = 60. Before buying 18 he had 60 " + M + " 18 = <b>42</b>. "
          "78 adds the 18 instead of taking it away. 12 forgets to double."))
    # Priya and Devi
    f = bar_svg([("Priya", [(1, "x", "u"), (1, "x", "u"), (1, "x", "u")]), ("Devi", [(1, "x", "u"), (1, "x", "u"), (0.9, "$15", "x")])],
                "Priya 3 units x, Devi 2 units x and $15, total $165", total="$165")
    x_ = solve("3x + 2x + 15", 165, "x")
    assert x_ == 30 and 2 * x_ + 15 == 75
    A(mcq(fig(f) + "The model shows the money that Priya and Devi saved. They saved $165 altogether. How much did Devi save?",
          sgd(75), [sgd(90), sgd(30), sgd(36)],
          E("5 units + $15 = $165, so 5 units = $150 and 1 unit = $30. Devi saved 2 × $30 + $15 = <b>$75</b>. "
            "$90 is Priya’s savings. $30 is 1 unit. $36 is 1 unit if you add the $15 instead of taking it away."), None))
    # consecutive numbers
    n_ = solve("n + n + 1 + n + 2", 72, "n")
    assert n_ == 23
    A(mcq(E("The sum of three consecutive whole numbers is 72. The smallest number is {n}. What is the largest number?"),
          25, [23, 24, 26],
          E("The numbers are {n}, {n + 1} and {n + 2}. {3n + 3} = 72, so {3n} = 69 and {n} = 23. "
            "The largest is 23 + 2 = <b>25</b>. 23 is the smallest and 24 is the middle number."), rat))
    p_ = solve("6p - 2p", 6, "p")
    assert p_ == Fr(3, 2)
    A(mcq(E("Pens cost ${p} each. Ethan bought 6 pens and Ryan bought 2 pens. Ethan paid $6 more than Ryan. "
            "Find the cost of 1 pen."), sgd(Fr(3, 2)), [sgd(1), sgd(3), sgd(Fr(3, 4))],
          E("Ethan bought 6 " + M + " 2 = 4 more pens. {4p} = 6, so {p} = 6 ÷ 4 = <b>$1.50</b>. "
            "$1 divides by 6, $3 divides by 2 and 75¢ divides by 8 (6 + 2).")))
    m_ = solve("4m + 2*(m - 1)", 22, "m")
    assert m_ == 4
    A(mcq(E("At the school canteen, a bowl of noodles costs ${m} and a cup of drink costs $1 less than a bowl of noodles. "
            "Hafiz bought 4 bowls of noodles and 2 cups of drink for $22 altogether. How much does a bowl of noodles cost?"),
          sgd(4), [sgd(3), sgd(Fr(11, 2)), sgd(Fr(7, 2))],
          E("4 bowls cost {4m}. 2 drinks cost {2m} minus $2. Total: {6m - 2} = 22. So {6m} = 24 and {m} = <b>$4</b>. "
            "$3 is the drink. $5.50 forgets the drinks (22 ÷ 4). $3.50 takes away only $1 instead of $2.")))
    order = [0, 1, 4, 5, 6, 7, 8, 2, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20 and len(set(order)) == 20
    return {"title": "PSLE-style word problems", "items": its}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    f1 = bar_svg([("n + 5", [(1.4, "n", "u"), (0.8, "5", "x")]), ("3n", [(1.4, "n", "u"), (1.4, "n", "u"), (1.4, "n", "u")])],
                 "n + 5 is n and 5 more; 3n is 3 units of n")
    f2 = bar_svg([("", [(1, "x", "u"), (1, "x", "u"), (1, "x", "u"), (1, "5", "x")])], "3 units x and 5, total 20",
                 top=(0, 4, "20"))
    return E(
        "<h2>A letter stands for an unknown number</h2>"
        "<p>In algebra, a letter such as {n} stands for a number we do not know yet. "
        "A number written next to a letter means multiply: {3n} = 3 × {n}. A fraction bar means divide: {[n|4]} = {n} ÷ 4.</p>" +
        table(["Words", "Expression"], [
            ["5 more than {n}", "{n + 5}"],
            ["3 times {n}", "{3n}"],
            ["{n} divided by 4", "{[n|4]}"],
            ["8 less than {y}", "{y - 8}"],
            ["1 less than twice {n}", "{2n - 1}"],
        ]) +
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>{n + 5} is {n} and 5 more. {3n} is 3 units of {n}.</figcaption></figure>"
        "<h2>Simplify: collect like terms</h2>"
        "<p>Terms with the same letter are <b>like terms</b>. Add or subtract the numbers in front of the letter. "
        "Numbers without a letter are collected on their own. Each sign belongs to the term after it.</p>" +
        ex("Example 1", "Simplify {4a + 3a - 2}.", "{4a + 3a} = {7a}. The 2 has no letter, so it stays.", "{7a - 2}") +
        ex("Example 2", "Simplify {5b + 3 - 2b + 6}.",
           "{b} terms: {5b - 2b} = {3b}. Numbers: 3 + 6 = 9.", "{3b + 9}") +
        "<p>{4a + 3} cannot be simplified. It is not {7a}: when {a} = 10, {4a + 3} = 43 but {7a} = 70.</p>"
        "<h2>Evaluate by substitution</h2>"
        "<p>Replace the letter with its value. Multiply or divide <b>before</b> you add or subtract.</p>" +
        ex("Example 3", "Find the value of {5k - 4} when {k} = 9.", "5 × 9 = 45. Then 45 " + M + " 4 = 41.", "41") +
        "<h2>Solve simple equations</h2>"
        "<p>An equation says two things are equal. Undo the steps one at a time, doing the same to both sides. "
        "Check your answer by putting it back in.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>{3x + 5} = 20. Take away the 5: 3 units = 15, so 1 unit = 5.</figcaption></figure>" +
        ex("Example 4", "Solve {3x + 5} = 20.",
           "Take away 5 from both sides: {3x} = 15. Divide both sides by 3: {x} = 5. Check: 3 × 5 + 5 = 20.", "{x} = 5") +
        ex("Example 5", "A pen costs $3. Siti buys {k} pens and a file that costs $4. Write the total cost. "
           "Then find the total cost when {k} = 6.",
           "{k} pens cost {3k} dollars, so the total is {3k + 4} dollars. When {k} = 6: 3 × 6 + 4 = 22.", "{3k + 4} dollars; $22") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["{3n} = 3 + {n}, or 34 when {n} = 4", "{3n} means 3 × {n} = 12"],
            ["{4a + 3} = {7a}", "{4a} and 3 are not like terms; leave it as {4a + 3}"],
            ["{5b + 3 - 2b + 6} = {3b - 3}", "The minus sign belongs only to {2b}: {3b + 9}"],
            ["{n} ÷ 4 written as {[4|n]}", "The number being divided goes on top: {[n|4]}"],
            ["“8 less than {y}” written as {8 - y}", "Start with {y} and take 8 away: {y - 8}"],
            ["{3x + 5} = 20 gives {x} = 8 " + fr(1, 3), "Take away 5 first, then divide by 3: {x} = 5"],
        ]))


FAQ = [
    {"q": "What algebra is taught in P6 maths?",
     "a": "Primary 6 students use a letter to stand for an unknown number, write and simplify simple expressions such as 4a + 3a − 2, find their value by substitution and solve simple equations such as 3x + 5 = 20."},
    {"q": "Is algebra tested in the PSLE?",
     "a": "Yes. Algebra is part of the P6 MOE syllabus, so PSLE questions may ask students to write an expression for a cost, simplify an expression, find its value or solve an equation in a word problem."},
    {"q": "How do I explain 3n to my child?",
     "a": "Tell your child that 3n means 3 × n, or 3 groups of n. If n = 4, then 3n = 12, not 34 and not 7."},
    {"q": "What is the most common mistake in P6 algebra?",
     "a": "The most common mistake is joining unlike terms, such as writing 4a + 3 as 7a. Only terms with the same letter can be added, so 4a + 3 stays as it is."},
]


def gen():
    rnd = random.Random(66806)
    sets = [set_write(), set_simplify(), set_evaluate(), set_solve(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(x["a"] for x in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for x in s["items"]:
            assert len(set(plain(c) for c in x["c"])) == 4, x
            assert x["q"].count("<svg") <= 1
            assert x["q"] not in seen, x["q"]
            assert "{" not in x["q"] + x["e"] + "".join(x["c"]), x
            seen.add(x["q"])
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-6", "slug": "algebra", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 6 Algebra: Expressions and Simple Equations",
        "seo_title": "P6 Algebra Worksheets: Free Primary 6 Maths with Answers (MOE Syllabus, PSLE Practice)",
        "short_title": "Algebra",
        "domain": "Number and Algebra",
        "standard_code": "Primary 6: Algebra",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Using a letter to represent an unknown number; simple algebraic expressions; simplifying linear expressions excluding brackets; evaluating by substitution; simple linear equations with whole number coefficients",
        "meta_desc": "Free P6 algebra practice: write, simplify and evaluate expressions, solve simple equations and PSLE-style word problems. 100 questions with answers.",
        "key_big": "A letter stands for a number: 3n means 3 × n, so when n = 4, 3n = 12.",
        "key_sub": "Simplify by collecting like terms: 5b + 3 − 2b + 6 = 3b + 9.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "algebra.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
