# -*- coding: utf-8 -*-
"""
British Columbia Grade 8 Math: Expressions and Substitution
(BC Mathematics Curriculum, Grade 8 — Patterning: expressions – writing and evaluating using substitution)
  python3 tools/gen_cabc_math_g8_expressions.py
Writing expressions from words (sum, difference, product, quotient, “less than”, brackets), evaluating with
whole numbers (order of operations, squares, formulas), with integers (sign rules), with fractions and decimals,
and word problems with cost formulas in BC contexts (kayak and bike rentals, BC Ferries, ski rentals).
Wrong choices come from real mistakes: reading 3x as 3 + x or as the two-digit number 35, writing “8 less than m”
as 8 − m, dropping brackets, sign errors with negative numbers ((−3)(−2) = −6, (−3)^2 = −9, 6 − (−2) = 4),
working left to right instead of following the order of operations, adding tops and bottoms of fractions,
and misplacing the decimal point.
Every answer is checked in code with fractions.Fraction; expressions are compared at several values.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English. Real minus sign −.
"""
import json, math, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-8")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
SIGN = "#fdf6dc"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
M = "−"


# ------------------------------------------------------------ numbers
def n(v):
    """BC style: 4536, 10 000 (no-break space), decimals with a point, real minus sign."""
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
    """Fraction in simplest form as HTML: 5/6, −2 1/2, 9."""
    v = Fr(v)
    if v.denominator == 1:
        return n(v)
    sg = M if v < 0 else ""
    w, r = divmod(abs(v.numerator), v.denominator)
    return sg + ("%d" % w + NBSP if w else "") + fr(r, v.denominator)


def money(v):
    v = Fr(v)
    c = v * 100
    assert c.denominator == 1, v
    assert c.numerator % 5 == 0, v   # no pennies
    w, r = divmod(abs(c.numerator), 100)
    return (M if v < 0 else "") + "$%s.%02d" % (n(w), r)


def plain(s):
    return re.sub(r"<[^>]+>", " ", s).replace(NBSP, " ").strip()


# ------------------------------------------------------------ expressions
# Plain syntax: "3x + 5", "x^2", "2(x + 5)", "[n|5]" is the fraction n over 5, "-" is a minus sign.
def _one(t):
    t = t.replace("-", M).replace("*", "×")
    t = re.sub(r"[A-Za-z]", lambda m: "<i>%s</i>" % m.group(), t)
    return re.sub(r"\^(\d)", r"<sup>\1</sup>", t)


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
    """Text with expressions in braces: 'Evaluate {3x + 5}' -> the braces become X(...)."""
    return re.sub(r"\{([^{}]*)\}", lambda m: X(m.group(1)), s.replace(" - ", " " + M + " "))


def ev(expr_, **env):
    """Exact value of a plain expression with the letters given in env."""
    t = re.sub(r"\[([^|\]]*)\|([^\]]*)\]", r"((\1)/(\2))", expr_)
    t = t.replace(M, "-").replace("×", "*").replace("^", "**").replace(" ", "")
    t = re.sub(r"\d+(\.\d+)?", lambda m: "Q('%s')" % m.group(), t)
    t = re.sub(r"(\)|[a-z])(?=[a-zQ(])", r"\1*", t)
    e = {"Q": Fr}
    for k, v in env.items():
        e[k] = Fr(v)
    return eval(t, {"__builtins__": {}}, e)


def same(a, b):
    letters = sorted(set(re.findall(r"[a-z]", a + b)))
    for v in (2, 3, 7, Fr(1, 2), -5):
        env = {L: v + i for i, L in enumerate(letters)}
        if ev(a, **env) != ev(b, **env):
            return False
    return True


# ------------------------------------------------------------ choices
def mcq(q, correct, cands, e, rnd, disp=None):
    """correct and cands are numbers shown with disp, or HTML strings. Equal values are rejected."""
    if disp is not None:
        cv, cs = Fr(correct), disp(correct)
    else:
        cv, cs = None, correct
    seen, vals, pick = {plain(cs)}, {cv}, []
    for c in cands:
        if disp is not None:
            c = Fr(c)
            assert c not in vals, (q, c)
            vals.add(c)
            c = disp(c)
        assert plain(c) not in seen, (q, c)
        seen.add(plain(c))
        pick.append(c)
    assert len(pick) == 3, (q, cs, cands)
    ch = pick + [cs]
    rnd.shuffle(ch)
    return {"q": q, "c": ch, "a": ch.index(cs), "e": e}


def emcq(q, good, bad, e, rnd, src=None):
    """Expression choices (plain syntax). good must equal src (when given); wrong ones must not be equivalent."""
    if src is not None:
        assert same(good, src), (src, good)
    for b in bad:
        assert not same(good, b), (good, b)
    return mcq(q, X(good), [X(b) for b in bad], e, rnd)


def cond(env, disp):
    return " and ".join("{%s} = %s" % (k, disp(v)) for k, v in env.items())


def evq(s_, env, wrong, e, rnd, disp=n, vdisp=None, check=None):
    """'Evaluate s_ when ...' with the answer worked out in code."""
    env = {k: Fr(v) for k, v in env.items()}
    ans = ev(s_, **env)
    if check is not None:
        assert ans == Fr(check), (s_, ans, check)
    q = E("Evaluate {%s} when %s." % (s_, cond(env, vdisp or disp)))
    return mcq(q, ans, [Fr(w) for w in wrong], E(e), rnd, disp)


# ------------------------------------------------------------ pictures
def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", bold=True, col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def it(v):
    return "<tspan font-style='italic'>%s</tspan>" % v


def sign_svg(title, lines, label):
    """A price sign: a title and up to 2 lines of prices."""
    W = 236
    H = 34 + 26 * len(lines) + 10
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='3'/>" % (W - 6, H - 6, SIGN, GREEN)]
    s.append("<rect x='3' y='3' width='%d' height='30' rx='10' fill='%s'/>" % (W - 6, GREEN))
    s.append("<rect x='3' y='20' width='%d' height='13' fill='%s'/>" % (W - 6, GREEN))
    s.append(text(W / 2, 24, title, 17, col="#ffffff"))
    for i, ln in enumerate(lines):
        s.append(text(W / 2, 56 + 26 * i, ln, 17))
    return svg_wrap(W, H, "".join(s), label)


def rect_svg(top, side, label, w=150, h=70):
    L, T = 78, 28
    s = ["<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (L, T, w, h, FILL, GREEN)]
    s.append(text(L + w / 2, T - 9, top, 16))
    s.append(text(L - 8, T + h / 2 + 6, side, 16, "end"))
    return svg_wrap(L + w + 8, T + h + 6, "".join(s), label)


def tri_svg(base, height, label):
    """Triangle with a dashed height line; base labelled below, height labelled beside the dashed line."""
    A, B, C = (20, 110), (240, 110), (80, 20)
    s = ["<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2'/>" % (A + B + C + (FILL, GREEN))]
    s.append("<line x1='80' y1='20' x2='80' y2='110' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % INK)
    s.append("<polyline points='80,100 90,100 90,110' fill='none' stroke='%s' stroke-width='1.5'/>" % INK)
    s.append(text(130, 135, base, 16))
    s.append(text(96, 92, height, 16, "start"))
    return svg_wrap(258, 142, "".join(s), label)


def subst_svg(label):
    """Lesson figure: 3x + 5 with x = 4 put into a bracket."""
    s = []
    s.append(text(150, 26, "3" + it("x") + " + 5", 22))
    s.append(text(262, 26, it("x") + " = 4", 17, col=GREEN))
    s.append("<line x1='150' y1='38' x2='150' y2='66' stroke='%s' stroke-width='2.5'/>" % GREEN)
    s.append("<polygon points='143,62 157,62 150,74' fill='%s'/>" % GREEN)
    s.append("<rect x='98' y='80' width='34' height='34' rx='4' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN))
    s.append(text(68, 105, "3 ×", 22))
    s.append(text(115, 105, "4", 22, col=GREEN))
    s.append(text(140, 105, "+ 5 = 12 + 5 = 17", 22, "start"))
    return svg_wrap(340, 124, "".join(s), label)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for x in s["items"]:
            x["q"] = rx.sub("<svg data-pf='lg' ", x["q"])
    return u


# ============================================================ set 1: write expressions from words
def set_write(rnd):
    its = []
    its.append((0, mcq(E("What does {3x} mean?"), "3 × " + X("x"),
                       ["3 + " + X("x"), X("x") + " ÷ 3", "a two-digit number, like 35"],
                       E("A number written next to a variable means multiply: {3x} = 3 × {x}. "
                         "It is not 3 + {x}, and when {x} = 5 it is 15, not 35."), rnd)))
    rows = [
        (0, "the sum of a number {n} and 7", "n + 7", ["7n", "n - 7", "7 - n"],
         "“Sum” means add: {n + 7}. ({7n} is a product, not a sum.)"),
        (0, "6 more than a number {x}", "x + 6", ["6x", "x - 6", "6 - x"],
         "“6 more than {x}” means add 6 to {x}: {x + 6}. ({6x} means 6 × {x}.)"),
        (0, "the product of 4 and a number {y}", "4y", ["4 + y", "y - 4", "[y|4]"],
         "“Product” means multiply: 4 × {y} = {4y}. ({4 + y} is a sum.)"),
        (0, "8 less than a number {m}", "m - 8", ["8 - m", "8m", "m + 8"],
         "Start with {m} and take 8 away: {m - 8}. The order matters: {8 - m} means “{m} less than 8”."),
        (1, "a number {x} decreased by 3", "x - 3", ["3 - x", "3x", "x + 3"],
         "“Decreased by 3” means subtract 3 from {x}: {x - 3}. ({3 - x} subtracts in the wrong order.)"),
        (1, "twice a number {k}", "2k", ["k + 2", "k^2", "k - 2"],
         "“Twice” means 2 times: {2k}. ({k^2} means {k} × {k}, not 2 × {k}.)"),
        (1, "the quotient of a number {n} and 5", "[n|5]", ["5n", "[5|n]", "n - 5"],
         "“Quotient” means divide, in the order given: {n} ÷ 5 = {[n|5]}. ({[5|n]} divides in the wrong order.)"),
        (1, "10 subtracted from a number {x}", "x - 10", ["10 - x", "10x", "-10x"],
         "Start with {x} and subtract 10: {x - 10}. ({10 - x} puts the numbers in the order they are read, which is wrong here.)"),
        (1, "a number {n} multiplied by {-2}", "-2n", ["n - 2", "-2 + n", "2n"],
         "Multiply {n} by " + M + "2: {-2n}. ({n - 2} subtracts 2 instead of multiplying.)"),
        (2, "5 more than 3 times a number {x}", "3x + 5", ["3 + x + 5", "3(x + 5)", "8x"],
         "3 times {x} is {3x}, then add 5: {3x + 5}. ({3 + x + 5} reads {3x} as 3 + {x}. {3(x + 5)} multiplies the 5 too.)"),
        (2, "5 less than 3 times a number {p}", "3p - 5", ["5 - 3p", "3(p - 5)", "3 + p - 5"],
         "3 times {p} is {3p}; 5 less than that is {3p - 5}. ({5 - 3p} subtracts in the wrong order.)"),
        (2, "half of a number {w}, minus 4", "[w|2] - 4", ["2w - 4", "[w - 4|2]", "4 - [w|2]"],
         "Half of {w} is {[w|2]}; then subtract 4: {[w|2] - 4}. ({2w} is double, not half.)"),
        (2, "7 times the sum of a number {x} and 2", "7(x + 2)", ["7x + 2", "7 + x + 2", "9x"],
         "Find the sum first, so it goes in brackets: {7(x + 2)}. ({7x + 2} multiplies only {x} by 7.)"),
        (3, "the difference of a number {y} and 9, divided by 4", "[y - 9|4]", ["[y|4] - 9", "[9 - y|4]", "4(y - 9)"],
         "The difference {y - 9} is found first, then divided by 4: {[y - 9|4]}. ({[y|4] - 9} divides only {y}.)"),
    ]
    for t, words, good, bad, e in rows:
        its.append((t, emcq(E("Which expression means “" + words + "”?"), good, bad, E(e), rnd)))
    rows = [
        (0, "Chloe earns $15 an hour babysitting. Which expression gives what she earns in {h} hours?",
         "15h", ["15 + h", "[h|15]", "[15|h]"],
         "Each hour adds $15, so {h} hours give 15 × {h} = {15h}. ({15 + h} adds only one $15.)"),
        (2, "Ava has {x} stickers. Mateo has 4 fewer than 3 times as many stickers as Ava. Which expression gives the number of stickers Mateo has?",
         "3x - 4", ["4 - 3x", "3(x - 4)", "3x + 4"],
         "3 times as many as Ava is {3x}; 4 fewer is {3x - 4}. ({3x + 4} means 4 more, not 4 fewer.)"),
        (1, "The temperature on Grouse Mountain is {t} °C. Overnight it drops 6 °C. Which expression gives the new temperature?",
         "t - 6", ["6 - t", "-6t", "t + 6"],
         "A drop of 6 °C means subtract 6: {t - 6}. ({-6t} multiplies instead of subtracting.)"),
    ]
    for t, q, good, bad, e in rows:
        its.append((t, emcq(E(q), good, bad, E(e), rnd)))
    assert same("4n - 1", "4n + -1") and not same("4n - 1", "4(n - 1)") and not same("4n - 1", "1 - 4n")
    its.append((3, mcq(E("Which words describe {4n - 1}?"), "1 less than the product of 4 and " + X("n"),
                       ["4 times the difference of " + X("n") + " and 1",
                        "the product of 4 and " + X("n") + ", subtracted from 1",
                        "the sum of 4, " + X("n") + " and " + M + "1"],
                       E("{4n} is the product of 4 and {n}, and {- 1} takes 1 away from it. "
                         "“4 times the difference” would be {4(n - 1)}, and “subtracted from 1” would be {1 - 4n}."), rnd)))
    assert not same("2(x + 5)", "2x + 5") and not same("2(x + 5)", "x + 7") and not same("2(x + 5)", "2(x - 5)")
    its.append((3, mcq(E("Which words describe {2(x + 5)}?"), "twice the sum of " + X("x") + " and 5",
                       ["5 more than twice " + X("x"), "2 more than the sum of " + X("x") + " and 5",
                        "twice the difference of " + X("x") + " and 5"],
                       E("The brackets show that {x + 5} is found first, then doubled. "
                         "“5 more than twice {x}” would be {2x + 5}, with no brackets."), rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Write expressions from words", "items": [x for _, x in its]}


# ============================================================ set 2: evaluate with whole numbers
def set_whole(rnd):
    its = []
    rows = [
        (0, "3x", {"x": 5}, [8, 35, 125],
         "{3x} means 3 × {x}: 3 × 5 = 15. (8 adds 3 + 5. 35 writes the 3 and the 5 side by side.)"),
        (0, "4n + 3", {"n": 6}, [13, 36, 49],
         "4 × 6 = 24, then 24 + 3 = 27. (13 adds 4 + 6 + 3. 36 works out 4 × (6 + 3). 49 reads {4n} as 46.)"),
        (0, "5x - 2", {"x": 4}, [7, 10, 52],
         "5 × 4 = 20, then 20 " + M + " 2 = 18. (7 adds 5 + 4 first. 10 works out 5 × (4 " + M + " 2). 52 reads {5x} as 54.)"),
        (0, "20 - 3y", {"y": 4}, [68, 13, 16],
         "Multiply first: 3 × 4 = 12. Then 20 " + M + " 12 = 8. (68 subtracts first: 17 × 4. 13 reads {3y} as 3 + 4.)"),
        (1, "2a + 3b", {"a": 5, "b": 4}, [14, 23, 59],
         "2 × 5 = 10 and 3 × 4 = 12, so 10 + 12 = 22. (23 swaps the values of {a} and {b}. 14 adds every number.)"),
        (1, "x^2 + 1", {"x": 6}, [13, 49, 7],
         "{x^2} = 6 × 6 = 36, then 36 + 1 = 37. (13 reads {x^2} as {2x}. 49 works out (6 + 1)<sup>2</sup>.)"),
        (1, "4(x + 3)", {"x": 5}, [23, 12, 60],
         "Brackets first: 5 + 3 = 8. Then 4 × 8 = 32. (23 multiplies only the 5 by 4. 60 multiplies 4 × 5 × 3.)"),
        (1, "[x|3] + 7", {"x": 12}, [19, 43, 4],
         "12 ÷ 3 = 4, then 4 + 7 = 11. (19 forgets to divide. 43 multiplies by 3 instead. 4 forgets the + 7.)"),
        (1, "[n + 6|2]", {"n": 10}, [11, 13, 32],
         "The fraction bar groups the top: 10 + 6 = 16, then 16 ÷ 2 = 8. (11 divides only {n} by 2. 13 divides only the 6.)"),
        (2, "3p + 2q - 5", {"p": 4, "q": 7}, [24, 11, 26],
         "3 × 4 = 12 and 2 × 7 = 14. Then 12 + 14 " + M + " 5 = 21. (24 swaps {p} and {q}. 26 forgets the " + M + " 5.)"),
        (2, "ab - 4", {"a": 6, "b": 3}, [5, 59, 18],
         "{ab} means {a} × {b} = 6 × 3 = 18. Then 18 " + M + " 4 = 14. (5 adds 6 + 3. 59 reads {ab} as 63.)"),
        (2, "2x^2", {"x": 3}, [36, 12, 6],
         "Square first: 3<sup>2</sup> = 9. Then 2 × 9 = 18. (36 squares 2 × 3. 12 works out 2 × 3 × 2.)"),
        (2, "5(2k - 1)", {"k": 4}, [39, 7, 45],
         "Brackets first: 2 × 4 " + M + " 1 = 7. Then 5 × 7 = 35. (39 multiplies only the 2{k} by 5. 7 forgets the 5. 45 adds the 1.)"),
        (2, "100 - 4m", {"m": 15}, [1440, 81, 60],
         "4 × 15 = 60, then 100 " + M + " 60 = 40. (1440 subtracts first: 96 × 15. 81 reads {4m} as 4 + 15.)"),
        (3, "[3x|4]", {"x": 8}, [24, 2, 11],
         "3 × 8 = 24, then 24 ÷ 4 = 6. (24 forgets to divide by 4. 2 forgets to multiply by 3.)"),
        (3, "x^2 - 2x", {"x": 5}, [0, 115, 35],
         "5<sup>2</sup> = 25 and 2 × 5 = 10. Then 25 " + M + " 10 = 15. (0 reads {x^2} as {2x}. 35 adds the 10.)"),
        (3, "(x + y)^2", {"x": 2, "y": 3}, [13, 10, 11],
         "Brackets first: 2 + 3 = 5. Then 5<sup>2</sup> = 25. (13 squares each number: 4 + 9. 10 doubles instead of squaring.)"),
        (3, "12 - x + 3", {"x": 5}, [4, 20, 7],
         "Add and subtract from left to right: 12 " + M + " 5 = 7, then 7 + 3 = 10. (4 adds 5 + 3 first. 7 forgets the + 3.)"),
    ]
    for t, s_, env, wrong, e in rows:
        its.append((t, evq(s_, env, wrong, e, rnd)))
    cm = lambda v: n(v) + NBSP + "cm"
    svg = rect_svg(it("l") + " = 9 cm", it("w") + " = 4 cm", "rectangle with length l = 9 cm and width w = 4 cm")
    assert ev("2l + 2w", l=9, w=4) == 26
    its.append((3, mcq(fig(svg) + E("The perimeter of a rectangle is {P} = {2l + 2w}. What is {P} for this rectangle?"), 26,
                       [13, 36, 22],
                       E("2 × 9 + 2 × 4 = 18 + 8 = 26, so 26" + NBSP + "cm. (13" + NBSP + "cm adds only two sides. "
                         "36 is 9 × 4, the area. 22 doubles only the length.)"), rnd, cm)))
    svg = tri_svg(it("b") + " = 10 cm", it("h") + " = 7 cm", "triangle with base b = 10 cm and height h = 7 cm")
    assert ev("[bh|2]", b=10, h=7) == 35
    its.append((3, mcq(fig(svg) + E("The area of a triangle is {A} = {[bh|2]}. What is {A} for this triangle?"), 35,
                       [70, 17, 34],
                       E("10 × 7 = 70, then 70 ÷ 2 = 35, so 35" + NBSP + "cm<sup>2</sup>. (70 forgets to divide by 2. "
                         "17 adds 10 + 7 instead of multiplying. 34 doubles 10 + 7.)"), rnd,
                       lambda v: n(v) + NBSP + "cm<sup>2</sup>")))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate with whole numbers", "items": [x for _, x in its]}


# ============================================================ set 3: evaluate with integers
def set_integers(rnd):
    its = []
    rows = [
        (0, "x - 7", {"x": -3}, [4, -4, 10],
         M + "3 " + M + " 7 = " + M + "10. Going down 7 from " + M + "3 gives " + M + "10. (" + M + "4 and 4 work out 7 " + M + " 3 instead.)"),
        (0, "-4x", {"x": -5}, [-20, -9, 1],
         M + "4 × (" + M + "5) = 20. A negative times a negative is positive. (" + M + "20 is a sign error. " + M + "9 adds instead of multiplying. 1 subtracts.)"),
        (0, "3n + 5", {"n": -4}, [17, 4, -17],
         "3 × (" + M + "4) = " + M + "12. Then " + M + "12 + 5 = " + M + "7. (17 uses +12. 4 reads {3n} as 3 + {n}.)"),
        (0, "6 - x", {"x": -2}, [4, -8, -4],
         "6 " + M + " (" + M + "2) = 6 + 2 = 8. Subtracting a negative is adding. (4 works out 6 " + M + " 2.)"),
        (1, "-x + 9", {"x": -6}, [3, -15, -3],
         "{-x} is the opposite of {x}. The opposite of " + M + "6 is 6, so 6 + 9 = 15. (3 uses " + M + "6 for {-x}.)"),
        (1, "x^2", {"x": -7}, [-49, -14, 14],
         "(" + M + "7)<sup>2</sup> = (" + M + "7) × (" + M + "7) = 49. (" + M + "49 is a sign error. " + M + "14 and 14 double instead of squaring.)"),
        (1, "-x^2", {"x": 3}, [9, -6, 6],
         "Square first, then take the opposite: 3<sup>2</sup> = 9, so {-x^2} = " + M + "9. (9 squares " + M + "3 instead.)"),
        (1, "ab", {"a": -3, "b": -8}, [-24, -11, 5],
         "(" + M + "3) × (" + M + "8) = 24. Negative × negative is positive. (" + M + "11 adds instead of multiplying.)"),
        (1, "5 - 2y", {"y": -3}, [-1, -9, -11],
         "2 × (" + M + "3) = " + M + "6. Then 5 " + M + " (" + M + "6) = 11. (" + M + "1 works out 5 " + M + " 6. " + M + "9 subtracts first: 3 × (" + M + "3).)"),
        (2, "2x - 3y", {"x": -1, "y": 4}, [10, -10, 14],
         "2 × (" + M + "1) = " + M + "2 and 3 × 4 = 12. Then " + M + "2 " + M + " 12 = " + M + "14. (10 works out " + M + "2 + 12. " + M + "10 uses 2 for 2{x}.)"),
        (2, "4(x - 3)", {"x": -2}, [-11, 20, 4],
         "Brackets first: " + M + "2 " + M + " 3 = " + M + "5. Then 4 × (" + M + "5) = " + M + "20. (" + M + "11 multiplies only {x} by 4. 4 uses 1 for " + M + "2 " + M + " 3.)"),
        (2, "[x|-4] + 1", {"x": 12}, [4, -4, -3],
         "12 ÷ (" + M + "4) = " + M + "3. Then " + M + "3 + 1 = " + M + "2. (4 makes the quotient positive. " + M + "3 forgets the + 1.)"),
        (2, "x^2 - 3x", {"x": -2}, [-2, -10, 2],
         "(" + M + "2)<sup>2</sup> = 4 and 3 × (" + M + "2) = " + M + "6. Then 4 " + M + " (" + M + "6) = 10. "
         "(" + M + "2 works out 4 " + M + " 6. " + M + "10 uses " + M + "4 for the square.)"),
        (2, "-3(a + b)", {"a": 5, "b": -9}, [-12, -42, 42],
         "Brackets first: 5 + (" + M + "9) = " + M + "4. Then " + M + "3 × (" + M + "4) = 12. (" + M + "12 is a sign error. " + M + "42 uses 5 + 9.)"),
        (3, "y^3 + 1", {"y": -2}, [9, -5, -9],
         "(" + M + "2)<sup>3</sup> = (" + M + "2) × (" + M + "2) × (" + M + "2) = " + M + "8. Then " + M + "8 + 1 = " + M + "7. "
         "(9 uses +8. " + M + "5 reads {y^3} as {3y}.)"),
        (3, "-2m + 3n", {"m": -4, "n": -5}, [-23, 23, 7],
         M + "2 × (" + M + "4) = 8 and 3 × (" + M + "5) = " + M + "15. Then 8 + (" + M + "15) = " + M + "7. (" + M + "23 uses " + M + "8 for " + M + "2{m}.)"),
        (3, "[a - b|2]", {"a": -3, "b": 7}, [2, -2, 5],
         "Top first: " + M + "3 " + M + " 7 = " + M + "10. Then " + M + "10 ÷ 2 = " + M + "5. (2 works out " + M + "3 + 7. 5 is a sign error.)"),
        (3, "10 - x^2", {"x": -4}, [26, 18, 6],
         "(" + M + "4)<sup>2</sup> = 16. Then 10 " + M + " 16 = " + M + "6. (26 uses " + M + "16 for the square. 18 reads {x^2} as {2x}.)"),
    ]
    for t, s_, env, wrong, e in rows:
        its.append((t, evq(s_, env, wrong, e, rnd)))
    assert ev("1.8C + 32".replace("C", "c"), c=-10) == 14
    its.append((3, mcq(E("In Whistler the temperature is " + M + "10" + NBSP + "°C. The formula {F} = 1.8{C} + 32 changes degrees Celsius to "
                         "degrees Fahrenheit. What is the temperature in degrees Fahrenheit?"), 14, [50, 22, -14],
                       E("1.8 × (" + M + "10) = " + M + "18. Then " + M + "18 + 32 = 14, so 14" + NBSP + "°F. "
                         "(50 uses +18. 22 reads 1.8{C} as 1.8 + {C}: " + M + "10 + 32.)"),
                       rnd, lambda v: n(v) + NBSP + "°F")))
    good, bad = "4x + 2", ["-4x + 2", "4x - 2", "2x + 4"]
    assert ev(good, x=-2) == -6 and all(ev(b, x=-2) != -6 for b in bad)
    its.append((3, emcq(E("Which expression has a value of " + M + "6 when {x} = " + M + "2?"), good, bad,
                        E("Check each one: " + "; ".join("{%s} = %s" % (b, n(ev(b, x=-2))) for b in [good] + bad) +
                          ". Only {4x + 2} gives " + M + "6."), rnd)))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate with integers", "items": [x for _, x in its]}


# ============================================================ set 4: evaluate with fractions and decimals
def set_fracdec(rnd):
    its = []
    rows = [
        (0, "0.5x", {"x": 18}, [36, "18.5", 90],
         "0.5 × 18 = 9 (half of 18). (36 divides by 0.5 instead. 18.5 reads 0.5{x} as 0.5 + {x}.)"),
        (0, "2.5n", {"n": 4}, ["6.5", "8.5", 100],
         "2.5 × 4 = 10. (6.5 adds. 8.5 multiplies only the 2 by 4. 100 forgets the decimal point: 25 × 4.)"),
        (0, "x + 1.4", {"x": "2.7"}, ["3.11", "1.3", "3.78"],
         "Line up the decimal points: 2.7 + 1.4 = 4.1. (3.11 adds the tenths as 7 + 4 = 11 without carrying.)"),
        (1, "3y - 1.2", {"y": "0.8"}, ["-1.2", "2.6", "22.8"],
         "3 × 0.8 = 2.4. Then 2.4 " + M + " 1.2 = 1.2. (" + M + "1.2 works out 3 × (0.8 " + M + " 1.2). "
         "22.8 uses 3 × 8.)"),
        (1, "4x + 0.6", {"x": "-0.5"}, ["2.6", "-2.6", "4.1"],
         "4 × (" + M + "0.5) = " + M + "2. Then " + M + "2 + 0.6 = " + M + "1.4. (2.6 uses +2. 4.1 reads 4{x} as 4 + {x}.)"),
        (1, "1.2a - b", {"a": 5, "b": "2.5"}, ["8.5", "3.7", 3],
         "1.2 × 5 = 6. Then 6 " + M + " 2.5 = 3.5. (8.5 adds the 2.5. 3 works out 1.2 × (5 " + M + " 2.5).)"),
        (2, "0.2x - 1", {"x": -15}, [2, -2, -16],
         "0.2 × (" + M + "15) = " + M + "3. Then " + M + "3 " + M + " 1 = " + M + "4. (2 uses +3. " + M + "16 forgets the 0.2.)"),
        (2, "x^2", {"x": "0.3"}, ["0.9", "0.6", "0.009"],
         "0.3 × 0.3 = 0.09: 3 × 3 = 9, with 2 decimal places. (0.9 has too few decimal places. 0.6 doubles instead of squaring.)"),
        (2, "1.5(x - 2)", {"x": 6}, [7, 4, -6],
         "Brackets first: 6 " + M + " 2 = 4. Then 1.5 × 4 = 6. (7 multiplies only {x}: 9 " + M + " 2. 4 forgets the 1.5. " + M + "6 subtracts in the wrong order: 1.5 × (2 " + M + " 6).)"),
    ]
    for t, s_, env, wrong, e in rows:
        its.append((t, evq(s_, env, wrong, e, rnd)))
    rows = [
        (0, "[1|2]x", {"x": 14}, [28, Fr(29, 2), Fr(1, 28)],
         "{[1|2]} × 14 = 14 ÷ 2 = 7. (28 multiplies by 2. 14" + NBSP + "{[1|2]} adds {[1|2]} + 14.)"),
        (1, "[2|3]n", {"n": 21}, [Fr(63, 2), 7, 42],
         "21 ÷ 3 = 7, then 7 × 2 = 14. (7 forgets to multiply by 2. 42 forgets to divide by 3. 31" + NBSP + "{[1|2]} multiplies by {[3|2]}.)"),
        (1, "x + [3|4]", {"x": Fr(1, 2)}, [Fr(4, 6), Fr(3, 8), Fr(1, 4)],
         "Use a common denominator: {[2|4]} + {[3|4]} = {[5|4]} = 1" + NBSP + "{[1|4]}. "
         "({[4|6]} adds the tops and the bottoms. {[3|8]} multiplies.)"),
        (2, "2y - [1|3]", {"y": Fr(5, 6)}, [Fr(1, 2), 2, Fr(-4, 3)],
         "2 × {[5|6]} = {[10|6]} = {[5|3]}. Then {[5|3]} " + M + " {[1|3]} = {[4|3]} = 1" + NBSP + "{[1|3]}. "
         "({[1|2]} forgets the 2. 2 adds the {[1|3]}.)"),
        (2, "3 - x", {"x": Fr(2, 5)}, [Fr(1, 5), 1, Fr(17, 5)],
         "3 = 2" + NBSP + "{[5|5]}, so 2" + NBSP + "{[5|5]} " + M + " {[2|5]} = 2" + NBSP + "{[3|5]}. "
         "({[1|5]} subtracts only the tops. 3" + NBSP + "{[2|5]} adds.)"),
        (2, "-[3|4]x", {"x": -8}, [-6, Fr(-32, 3), Fr(32, 3)],
         "8 ÷ 4 = 2, then 2 × 3 = 6. Negative × negative is positive, so the answer is 6. (" + M + "6 is a sign error. "
         "10" + NBSP + "{[2|3]} multiplies by {[4|3]}.)"),
        (3, "[x|y]", {"x": -9, "y": 6}, [Fr(3, 2), Fr(-2, 3), -54],
         M + "9 ÷ 6 = " + M + "{[9|6]} = " + M + "1" + NBSP + "{[1|2]}. (1" + NBSP + "{[1|2]} is a sign error. " +
         M + "{[2|3]} divides in the wrong order. " + M + "54 multiplies.)"),
        (3, "a^2", {"a": Fr(2, 3)}, [Fr(4, 3), Fr(2, 9), Fr(2, 3)],
         "{[2|3]} × {[2|3]} = {[4|9]}: square the top and the bottom. ({[4|3]} squares only the top. {[2|9]} squares only the bottom.)"),
        (3, "[x|2] + [x|3]", {"x": 12}, [Fr(12, 5), 24, Fr(24, 5)],
         "12 ÷ 2 = 6 and 12 ÷ 3 = 4. Then 6 + 4 = 10. ({[12|5]} adds the denominators. 24 multiplies 6 × 4.)"),
        (3, "ab", {"a": Fr(3, 4), "b": Fr(-2, 9)}, [Fr(1, 6), Fr(-5, 13), Fr(-27, 8)],
         "{[3|4]} × (" + M + "{[2|9]}) = " + M + "{[6|36]} = " + M + "{[1|6]}. Positive × negative is negative. "
         "({[1|6]} is a sign error. " + M + "{[5|13]} adds the tops and the bottoms. " + M + "{[27|8]} divides.)"),
    ]
    for t, s_, env, wrong, e in rows:
        its.append((t, evq(s_, env, wrong, e, rnd, rat)))
    assert 6 * Fr(3, 4) - Fr(5, 2) == 2
    its.append((3, mcq(E("Evaluate {6x} " + M + " 2.5 when {x} = {[3|4]}."), 2, [7, Fr(-7, 4), Fr(7, 2)],
                       E("6 × {[3|4]} = {[18|4]} = 4.5. Then 4.5 " + M + " 2.5 = 2. (7 adds the 2.5. " +
                         M + "1.75 multiplies the top and the bottom by 6: {[18|24]} = 0.75. 3.5 forgets {x}: 6 " + M + " 2.5.)"),
                       rnd, n)))
    its.sort(key=lambda t: t[0])
    return {"title": "Evaluate with fractions and decimals", "items": [x for _, x in its]}


# ============================================================ set 5: word problems with cost formulas
def set_cost(rnd):
    its = []
    sg = sign_svg("Kayak rental", ["$15.00 to start", "+ $12.00 per hour"], "price sign: kayak rental $15 to start plus $12 per hour")
    assert ev("12h + 15", h=3) == 51
    its.append((0, mcq(fig(sg) + E("The cost in dollars to rent a kayak in Deep Cove for {h} hours is {C} = {12h + 15}. "
                                   "What does a 3-hour rental cost?"), 51, [81, 30, 57],
                       E("12 × 3 = 36, then 36 + 15 = 51, so $51.00. ($81.00 multiplies 27 × 3. $30.00 reads 12{h} as 12 + 3. "
                         "$57.00 multiplies the $15 by 3 instead.)"), rnd, money)))
    its.append((0, emcq(E("Bike rental at Stanley Park costs $8 to start plus $6 for each hour. Which expression gives the cost "
                          "in dollars for {h} hours?"), "6h + 8", ["8h + 6", "14h", "h + 14"],
                        E("$6 for each hour is {6h}; add the $8 start fee once: {6h + 8}. ({8h + 6} mixes up the two prices. "
                          "{h + 14} reads 6{h} as 6 + {h}.)"), rnd)))
    assert ev("6h + 8", h=4) == 32
    its.append((0, mcq(E("The bike rental costs {6h + 8} dollars for {h} hours. What does a 4-hour rental cost?"), 32,
                       [56, 38, 18],
                       E("6 × 4 = 24, then 24 + 8 = 32, so $32.00. ($56.00 works out 14 × 4. $38.00 uses 8 × 4 + 6. "
                         "$18.00 adds 6 + 4 + 8.)"), rnd, money)))
    its.append((0, emcq(E("A pizza costs $14, and delivery is $5 for the whole order. Which expression gives the cost in dollars "
                          "of {p} pizzas with delivery?"), "14p + 5", ["5p + 14", "19p", "p + 19"],
                        E("{p} pizzas cost {14p}; delivery is added once: {14p + 5}. ({19p} charges delivery for every pizza.)"), rnd)))
    assert ev("3.5 + 2k", k=8) == Fr(39, 2)
    its.append((1, mcq(E("A taxi in Victoria charges $3.50 to start plus $2.00 for each kilometre. The cost in dollars is "
                         "{C} = 3.5 + {2k} for {k} kilometres. What does an 8" + NBSP + "km ride cost?"), Fr(39, 2),
                       [44, Fr(27, 2), 30],
                       E("2 × 8 = 16, then 3.50 + 16 = 19.50, so $19.50. ($44.00 works out 5.50 × 8. "
                         "$13.50 reads 2{k} as 2 + 8. $30.00 multiplies the $3.50 by 8.)"), rnd, money)))
    assert ev("45d + 10", d=3) == 145
    its.append((1, mcq(E("Ski rental in Whistler costs $45 a day plus a $10 helmet fee for the whole rental: {C} = {45d + 10}. "
                         "What do 3 days cost?"), 145, [165, 58, 135],
                       E("45 × 3 = 135, then 135 + 10 = 145, so $145.00. ($165.00 charges the helmet fee every day. "
                         "$135.00 forgets the helmet fee.)"), rnd, money)))
    sg = sign_svg("BC Ferries trip", ["$65.00 for a car", "+ $19.00 per person"], "price sign: ferry trip $65 for a car plus $19 per person")
    assert ev("19p + 65", p=4) == 141
    its.append((1, mcq(fig(sg) + E("A family drives onto a ferry to Vancouver Island. The cost in dollars is {C} = {19p + 65} "
                                   "for {p} people. What does the trip cost for 4 people?"), 141, [336, 88, 279],
                       E("19 × 4 = 76, then 76 + 65 = 141, so $141.00. ($336.00 works out 84 × 4. $88.00 reads 19{p} as 19 + 4. "
                         "$279.00 multiplies the car fare by 4 instead.)"), rnd, money)))
    its.append((1, emcq(E("A pool pass costs $40, and then each visit costs $2.50. Which expression gives the cost in dollars "
                          "for {v} visits?"), "2.5v + 40", ["40v + 2.5", "42.5v", "v + 42.5"],
                        E("Each visit is $2.50, so {v} visits cost 2.5{v}; the pass is added once: 2.5{v} + 40."), rnd)))
    assert ev("2.5v + 40", v=12) == 70
    its.append((1, mcq(E("The pool costs 2.5{v} + 40 dollars for {v} visits. What do 12 visits cost?"), 70,
                       [Fr(965, 2), 510, Fr(109, 2)],
                       E("2.5 × 12 = 30, then 30 + 40 = 70, so $70.00. ($510.00 works out 42.5 × 12. "
                         "$54.50 adds 2.5 + 12 + 40. $482.50 multiplies the pass by 12.)"), rnd, money)))
    assert ev("28t + 6", t=5) == 146
    its.append((2, mcq(E("Concert tickets cost $28 each plus a $6 fee for the order: {C} = {28t + 6}. What do 5 tickets cost?"), 146,
                       [170, 39, 140],
                       E("28 × 5 = 140, then 140 + 6 = 146, so $146.00. ($170.00 charges the fee on every ticket. "
                         "$140.00 forgets the fee.)"), rnd, money)))
    its.append((2, emcq(E("For the Terry Fox Run, the Grade 8 class spends $30 on supplies and sells cookies for $2 each. "
                          "Which expression gives their profit in dollars for {c} cookies?"), "2c - 30", ["30 - 2c", "2c + 30", "28c"],
                        E("Money in: {2c}. Money out: 30. Profit = {2c - 30}. ({30 - 2c} subtracts in the wrong order. "
                          "{2c + 30} adds the cost instead of subtracting it.)"), rnd)))
    assert ev("2c - 30", c=12) == -6
    its.append((2, mcq(E("The class’s profit is {2c - 30} dollars for {c} cookies. What is the profit if they sell only 12 cookies?"), -6,
                       [54, 6, -54],
                       E("2 × 12 = 24, then 24 " + M + " 30 = " + M + "6. A profit of " + M + "$6.00 means they lost $6.00. "
                         "($54.00 adds the 30. $6.00 drops the minus sign.)"), rnd, money)))
    assert ev("50 - 6.5s", s=4) == 24
    its.append((2, mcq(E("Owen has a $50 gift card for a smoothie shop. Each smoothie costs $6.50, so the amount left is "
                         "{B} = 50 " + M + " 6.5{s} after {s} smoothies. How much is left after 4 smoothies?"), 24,
                       [76, Fr(79, 2), 174],
                       E("6.5 × 4 = 26, then 50 " + M + " 26 = 24, so $24.00. ($76.00 adds the 26. "
                         "$39.50 reads 6.5{s} as 6.5 + 4. $174.00 subtracts first: 43.5 × 4.)"), rnd, money)))
    assert ev("0.75a", a=8) == 6
    its.append((2, mcq(E("Apples cost $0.75 each at a Kelowna fruit stand. The cost in dollars is 0.75{a} for {a} apples. "
                         "What do 8 apples cost?"), 6, [Fr(35, 4), 60, Fr(3, 5)],
                       E("0.75 × 8 = 6, so $6.00. ($8.75 adds 0.75 + 8. $60.00 and $0.60 put the decimal point in the wrong place.)"),
                       rnd, money)))
    assert ev("35 + 0.2d", d=45) == 44
    its.append((2, mcq(E("A phone plan costs $35 a month plus $0.20 for each megabyte of data over the limit: {C} = 35 + 0.2{d}. "
                         "What is the bill when {d} = 45?"), 44, [Fr(401, 5), 1584, 125],
                       E("0.2 × 45 = 9, then 35 + 9 = 44, so $44.00. ($80.20 reads 0.2{d} as 0.2 + 45. "
                         "$1584.00 works out 35.2 × 45. $125.00 uses 2 × 45 instead of 0.2 × 45.)"), rnd, money)))
    its.append((3, emcq(E("At a hockey game, an adult ticket costs {x} dollars and a student ticket costs $4 less. Which expression "
                          "gives the cost of 3 adult tickets and 2 student tickets?"), "5x - 8", ["5x - 4", "5x + 8", "5x - 12"],
                        E("Adults: {3x}. Students: {2(x - 4)} = {2x - 8}. Total: {5x - 8}. ({5x - 4} takes $4 off only once. {5x - 12} takes $4 off the 3 adult tickets instead.)"),
                        rnd, "3x + 2(x - 4)")))
    assert ev("5x - 8", x=18) == 82
    its.append((3, mcq(E("The hockey tickets cost {5x - 8} dollars. What is the total when an adult ticket costs $18?"), 82,
                       [86, 98, 78],
                       E("5 × 18 = 90, then 90 " + M + " 8 = 82, so $82.00. ($86.00 uses {5x - 4}. $98.00 adds the 8. "
                         "$78.00 uses {5x - 12}.)"), rnd, money)))
    assert all(ev("6h + 14", h=h) == c for h, c in [(1, 20), (2, 26), (3, 32)])
    its.append((3, emcq(E("A canoe rental on the Fraser River costs $20 for 1 hour, $26 for 2 hours and $32 for 3 hours. "
                          "Which expression gives the cost in dollars for {h} hours?"), "6h + 14", ["20h", "6h + 20", "14h + 6"],
                        E("Each extra hour adds $6, so the expression has {6h}. For 1 hour: 6 + ? = 20, so the start fee is $14: "
                          "{6h + 14}. Check: 6 × 3 + 14 = 32. ({6h + 20} gives $26 for 1 hour.)"), rnd)))
    assert ev("8h + 10", h=4) == 42 and ev("10h", h=4) == 40
    its.append((3, mcq(E("Plan A for a paddleboard costs {8h + 10} dollars and Plan B costs {10h} dollars for {h} hours. "
                         "Which plan is cheaper for 4 hours, and by how much?"),
                       "Plan B, by $2.00", ["Plan A, by $2.00", "Plan B, by $8.00", "They cost the same"],
                       E("Plan A: 8 × 4 + 10 = 42. Plan B: 10 × 4 = 40. Plan B is cheaper by $42.00 " + M + " $40.00 = $2.00."), rnd)))
    assert ev("12s + 18h", s=10, h=5) == 210
    its.append((3, mcq(E("Team T-shirts cost $12 each and hoodies cost $18 each, so an order costs {12s + 18h} dollars. "
                         "What does an order of 10 T-shirts and 5 hoodies cost?"), 210, [240, 45, 450],
                       E("12 × 10 = 120 and 18 × 5 = 90. Then 120 + 90 = 210, so $210.00. ($240.00 swaps {s} and {h}. "
                         "$45.00 adds every number. $450.00 works out 30 × 15.)"), rnd, money)))
    its.sort(key=lambda t: t[0])
    return {"title": "Cost formula word problems", "items": [x for _, x in its]}


# ============================================================ lesson
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def body_html():
    f1 = subst_svg("substitution: 3x + 5 with x = 4 gives 3 × (4) + 5 = 17")
    f2 = sign_svg("Kayak rental", ["$15.00 to start", "+ $12.00 per hour"], "price sign: kayak rental $15 to start plus $12 per hour")
    return E(
        "<h2>Write expressions from words</h2>"
        "<p>An <b>expression</b> uses numbers, variables and operations, like {3x + 5}. "
        "A number next to a variable means multiply: {3x} = 3 × {x}.</p>" +
        table(["Words", "Expression"], [
            ["the sum of {n} and 7", "{n + 7}"],
            ["8 less than {m}", "{m - 8}"],
            ["the product of 4 and {y}", "{4y}"],
            ["the quotient of {n} and 5", "{[n|5]}"],
            ["7 times the sum of {x} and 2", "{7(x + 2)}"],
        ]) +
        "<p>“Less than” and “subtracted from” switch the order: “8 less than {m}” is {m - 8}, not {8 - m}.</p>"
        "<h2>Evaluate by substitution</h2>"
        "<p>To <b>evaluate</b> an expression, replace each variable with its value in brackets. "
        "Then follow the order of operations: brackets, exponents, × and ÷, then + and " + M + ".</p>"
        "<figure class='sn-fig'>" + f1 +
        "<figcaption>Put 4 in place of {x}. {3x} becomes 3 × 4, not 34 and not 3 + 4.</figcaption></figure>" +
        ex("Example 1", "Evaluate {2a + 3b} when {a} = 5 and {b} = 4.",
           "2 × 5 = 10 and 3 × 4 = 12. Then 10 + 12 = 22.", "22") +
        ex("Example 2", "Evaluate {5 - 2y} when {y} = " + M + "3.",
           "2 × (" + M + "3) = " + M + "6. Then 5 " + M + " (" + M + "6) = 5 + 6 = 11.", "11") +
        ex("Example 3", "Evaluate {2y} " + M + " {[1|3]} when {y} = {[5|6]}.",
           "2 × {[5|6]} = {[10|6]} = {[5|3]}. Then {[5|3]} " + M + " {[1|3]} = {[4|3]}.", "1" + NBSP + "{[1|3]}") +
        "<h2>Cost formulas</h2>"
        "<p>Many prices have a start fee plus a price for each hour or item. The price per hour is the coefficient, "
        "and the start fee is the constant.</p>"
        "<figure class='sn-fig'>" + f2 +
        "<figcaption>The cost in dollars for {h} hours is {C} = {12h + 15}.</figcaption></figure>" +
        ex("Example 4", "Use {C} = {12h + 15} to find the cost of a 3-hour kayak rental.",
           "12 × 3 = 36. Then 36 + 15 = 51.", "$51.00") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["{3x} = 3 + {x}, or 35 when {x} = 5", "{3x} means 3 × {x}: 3 × 5 = 15"],
            ["“8 less than {m}” = {8 - m}", "Start with {m} and take 8 away: {m - 8}"],
            ["4 × (" + M + "5) = 20", "Positive × negative is negative: " + M + "20"],
            ["(" + M + "3)<sup>2</sup> = " + M + "9", "(" + M + "3) × (" + M + "3) = 9"],
            ["6 " + M + " (" + M + "2) = 4", "Subtracting a negative is adding: 6 + 2 = 8"],
            ["{20 - 3y} = 17{y}", "Multiply before you subtract: 20 " + M + " 3 × 4 = 8"],
        ]))


FAQ = [
    {"q": "What does substitution mean in Grade 8 math?",
     "a": "Substitution means replacing a variable with a number and then working out the value. For 3x + 5 when x = 4, write 3 × (4) + 5 = 17."},
    {"q": "Does 3x mean 3 + x?",
     "a": "No. A number next to a variable means multiply, so 3x = 3 × x. When x = 5, 3x is 15, not 8 and not 35."},
    {"q": "How do you evaluate an expression with a negative number?",
     "a": "Put the negative number in brackets and use the integer sign rules. For 5 − 2y when y = −3: 2 × (−3) = −6, and 5 − (−6) = 11."},
    {"q": "Are expressions and substitution in the BC Grade 8 math curriculum?",
     "a": "Yes. The BC Grade 8 Patterning standards include writing expressions and evaluating them using substitution, with whole numbers, integers, fractions and decimals."},
]


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for x, t in zip(s["items"], targets):
            c = x["c"]
            c[x["a"]], c[t] = c[t], c[x["a"]]
            x["a"] = t


def gen_unit():
    rnd = random.Random(58806)
    sets = [set_write(rnd), set_whole(rnd), set_integers(rnd), set_fracdec(rnd), set_cost(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(x["a"] for x in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for x in s["items"]:
            assert len({plain(c) for c in x["c"]}) == 4, x
            assert x["e"]
            assert x["q"].count("<svg") <= 1
            k = x["q"] + "|" + "|".join(sorted(x["c"]))
            assert k not in seen, x["q"]
            seen.add(k)
    return {
        "country": "ca-bc", "subject": "math", "grade": "grade-8", "slug": "expressions-and-substitution", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 8 Expressions and Substitution",
        "seo_title": "Grade 8 Expressions and Substitution Worksheets: Free Math with Answer Key (BC Curriculum)",
        "short_title": "Expressions and Substitution",
        "domain": "Patterning",
        "standard_code": "Grade 8: Patterning",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/8/core",
        "standard_text": "Expressions – writing and evaluating using substitution",
        "meta_desc": "Free Grade 8 math worksheets on expressions and substitution for the BC curriculum: writing expressions from words, evaluating with whole numbers, integers, fractions and decimals, and cost formula word problems. 100 questions with an answer key.",
        "key_big": "To evaluate, put the value in brackets in place of the variable, then follow the order of operations.",
        "key_sub": "3x means 3 × x, so when x = −2, 3x + 5 = 3 × (−2) + 5 = −1. “8 less than m” is m − 8, not 8 − m.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "substitution")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
