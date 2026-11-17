# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Fractions, decimals and percentages (Australian Curriculum v9.0: AC9M7N04)
  python3 tools/gen_au_maths_y7_fractions_decimals_and_percentages.py
Equivalent fractions, decimals and percentages, rational numbers on a number line (including negatives and
mixed numerals), ordering a mixed list, and test-score and discount problems.
Wrong answers come from real mistakes: writing 3/8 as 0.38, 0.4 as 4%, 0.07 as 7/10, not simplifying,
and counting the tick marks instead of the spaces on a number line.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, table, svg_wrap, line, text, fig, INK, RED, MINUS

R = random.Random(70301)


def frc(v):
    v = F(v)
    return fr(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)


def pct(v):
    return num(F(v) * 100) + "%"


GOOD = [F(n, d) for d in (2, 4, 5, 8, 10, 20, 25, 40, 50) for n in range(1, d) if F(n, d).denominator == d]


# ------------------------------------------------------------ set 1: fraction -> decimal
def one_f2d(r):
    v = r.choice(GOOD)
    if v.denominator == 10:
        return None
    wr = [F("%d.%d" % (v.numerator // 1, v.denominator)) if v.numerator < 10 else None,     # 3/8 -> 3.8
          F(v.numerator, 10) if v.numerator < 10 else F(v.numerator, 100),                   # 3/8 -> 0.3
          F(int("%d%d" % (v.numerator, v.denominator)), 10 ** len("%d%d" % (v.numerator, v.denominator)))]  # 0.38
    q = "Write %s as a decimal." % B(frc(v))
    e = "%d ÷ %d = <b>%s</b>. (Or make the denominator 10, 100 or 1000 first.)" % (v.numerator, v.denominator, num(v))
    return QN(q, v, wr, e, near=(F(1, 10), F(-1, 10), F(1, 100)))


# ------------------------------------------------------------ set 2: decimal / percentage -> fraction
def one_d2f(r):
    v = r.choice(GOOD)
    as_pct = r.random() < 0.45
    if as_pct and (v * 100).denominator != 1:
        return None
    shown = pct(v) if as_pct else num(v)
    k = len(num(v).split(".")[1]) if not as_pct else 2
    den = 100 if as_pct else 10 ** k
    unsimp = "%s" % fr(int(v * den), den)
    wr = []
    if F(int(v * den), den).denominator != den:
        wr.append(unsimp)                                # not simplified
    wr.append(fr(int(v * den), 10 if den == 100 else 100))     # wrong place value
    wr.append(fr(v.denominator, v.numerator) if v.numerator > 1 else fr(int(v * den), den * 10))
    wr.append(fr(v.numerator + 1, v.denominator))
    wr = [w for w in wr if w != frc(v)]
    q = "Write %s as a fraction in its simplest form." % B(shown)
    e = "%s = %s. Divide top and bottom by %d: <b>%s</b>." % (
        shown, unsimp, den // v.denominator if den % v.denominator == 0 else 1, frc(v))
    return T(q, frc(v), wr[:3], e)


# ------------------------------------------------------------ set 3: to percentages
def one_2p(r):
    if r.random() < 0.5:
        v = r.choice(GOOD + [F(3, 2), F(5, 4), F(6, 5)])
        q = "Write %s as a percentage." % B(frc(v))
        wr = [F(v.numerator, 100), F(v.numerator * 100, v.denominator * 10) if v * 10 != v else None, F(v.numerator + v.denominator, 100)]
        e = "%s = %s, and %s × 100 = <b>%s</b>." % (frc(v), num(v), num(v), pct(v))
    else:
        v = r.choice([F(x, 1000) for x in (5, 35, 75, 125, 405)] + [F(x, 100) for x in (3, 7, 45, 60, 99, 120, 250)] + [F(x, 10) for x in (4, 9, 12)])
        q = "Write %s as a percentage." % B(num(v))
        wr = [v, v * 10, v * 1000]
        e = "Multiply by 100: %s × 100 = <b>%s</b>." % (num(v), pct(v))
    return mcq(q, (pct(v), v), [(pct(w / 100), w / 100) if False else (num(w) + "%", w / 100) for w in wr if w is not None and w / 100 != v], e)


# ------------------------------------------------------------ set 4: ordering
def one_order(r):
    vals = r.sample(GOOD, 4)
    if len({v for v in vals}) < 4:
        return None
    forms = r.sample(["f", "d", "p", "f", "p"], 4)
    shown = [(frc(v) if f == "f" else num(v) if f == "d" else pct(v), v) for v, f in zip(vals, forms)]
    kind = r.choice(["largest", "smallest"])
    ans = max(vals) if kind == "largest" else min(vals)
    if sorted(vals)[-1] - sorted(vals)[-2] < F(1, 100) and kind == "largest":
        return None
    right = [s for s, v in shown if v == ans][0]
    q = "Which is the %s?" % B(kind)
    e = "Change them all to decimals: %s. The %s is <b>%s</b>." % (", ".join("%s = %s" % (s, num(v)) for s, v in shown), kind, right)
    return T(q, right, [s for s, v in shown if v != ans], e)


def one_equiv(r):
    v = r.choice(GOOD)
    sets = [frc(v), num(v), pct(v)]
    have = r.randrange(3)
    want = r.choice([i for i in range(3) if i != have])
    names = ["fraction", "decimal", "percentage"]
    right = sets[want]
    if want == 0:
        wr = [fr(int(v * 100), 10) if (v * 100).denominator == 1 else None, fr(v.numerator, v.denominator * 10), fr(v.denominator, v.numerator),
              fr(v.numerator + 1, v.denominator)]
    elif want == 1:
        wr = [num(v * 10), num(v / 10), num(v * 100)]
    else:
        wr = [num(v) + "%", num(v * 10) + "%", num(v * 1000) + "%"]
    wr = [w for w in wr if w and w != right]
    q = "Which is equal to %s?" % B(sets[have])
    e = "%s = %s = %s, so the answer is <b>%s</b>." % (sets[0], sets[1], sets[2], right)
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 4: number lines
def nl_svg(lo, hi, parts, mark, labels):
    """Number line from lo to hi (Fractions) split into parts; arrow at mark; labels: list of values to label."""
    W, x0, x1, y = 460, 30, 430, 60
    X = lambda v: x0 + float((v - lo) / (hi - lo)) * (x1 - x0)
    s = [line(x0 - 8, y, x1 + 8, y, INK, 2)]
    for i in range(parts + 1):
        v = lo + (hi - lo) * F(i, parts)
        big = v in labels
        s.append(line(X(v), y - (10 if big else 6), X(v), y + (10 if big else 6), INK, 2 if big else 1.5))
        if big:
            s.append(text(X(v), y + 28, num(v) if v.denominator == 1 else frc(v), 14))
    s.append("<path d='M%.1f %d l-7 -14 l14 0 Z' fill='%s'/>" % (X(mark), y - 12, RED))
    s.append(text(X(mark), y - 30, "?", 16, col=RED))
    return svg_wrap(W, 100, "".join(s), "number line")


def one_nl(r):
    kind = r.choice(["dec", "dec", "frac", "mixed", "neg"])
    if kind == "dec":
        lo = F(r.randint(0, 3))
        parts = 10
        k = r.randint(1, 9)
        v = lo + F(k, 10)
        q = fig(nl_svg(lo, lo + 1, parts, v, [lo, lo + 1])) + "What number is the arrow pointing to?"
        return QN(q, v, [lo + F(k, 100), lo + F(k + 1, 10), lo + k], "Each small space is 0.1. Count %d space%s from %s: <b>%s</b>." % (k, "" if k == 1 else "s", num(lo), num(v)),
                  near=(F(1, 10), F(-1, 10)))
    if kind == "frac":
        d = r.choice([3, 4, 5, 6, 8])
        k = r.randint(1, d - 1)
        if F(k, d).denominator != d:
            return None
        v = F(k, d)
        q = fig(nl_svg(F(0), F(1), d, v, [F(0), F(1)])) + "What fraction is the arrow pointing to?"
        right = frc(v)
        wr = [fr(k, d + 1), fr(k + 1, d) if k + 1 < d else fr(k - 1, d), fr(d, k) if k > 1 else fr(k, 10)]
        return T(q, right, wr, "From 0 to 1 is split into %d equal spaces, so each space is %s. The arrow is %d spaces along: <b>%s</b>." % (d, fr(1, d), k, right))
    if kind == "mixed":
        w = r.randint(1, 3)
        d = r.choice([2, 4, 5])
        k = r.randint(1, d - 1)
        if F(k, d).denominator != d:
            return None
        v = w + F(k, d)
        q = fig(nl_svg(F(w), F(w + 1), d, v, [F(w), F(w + 1)])) + "What number is the arrow pointing to? Give it as a decimal."
        return QN(q, v, [w + F(k, 10), w + F(k, d) * 10 / 10 + F(1, 10), F(w * 10 + k, 10) + 1], "Each space is %s = %s. %d + %s = <b>%s</b>." % (fr(1, d), num(F(1, d)), w, num(F(k, d)), num(v)),
                  near=(F(1, 10), F(-1, 10)))
    d = r.choice([2, 4, 5, 10])
    k = r.randint(1, d - 1)
    if F(k, d).denominator != d:
        return None
    v = -F(k, d)
    q = fig(nl_svg(F(-1), F(1), 2 * d, v, [F(-1), F(0), F(1)])) + "What number is the arrow pointing to? Give it as a decimal."
    return QN(q, v, [-v, F(-1) + F(k, d), v - F(1, d)], "Each space is %s. The arrow is %d space%s to the left of 0, so it is <b>%s</b>." % (
        num(F(1, d)), k, "" if k == 1 else "s", num(v)), near=(F(1, 10), F(-1, 10)))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = collect(one_order, 6, R)
    for name, score, out in [("Charlotte", 18, 20), ("Lachlan", 22, 25), ("Mei", 33, 40), ("Hamish", 41, 50), ("Priya", 15, 16), ("Tom", 11, 20)]:
        v = F(score, out)
        q = "%s scored %d out of %d on a quiz. What percentage is this?" % (name, score, out)
        e = "%d/%d = %s = <b>%s</b>." % (score, out, num(v), pct(v))
        its.append(mcq(q, (pct(v), v), [(num(w) + "%", w) for w in [F(score), F(100 - out + score), F(out - score) * 100 / out, v * 100 + 5] if w != v * 100], e))
    data = [
        ("In a class, 3/4 of the students catch the bus. What percentage is this?", "75%", ["34%", "3.4%", "0.75%"], "3/4 = 75/100 = <b>75%</b>."),
        ("35% of the students at a school play a summer sport. What fraction do not? Give it in its simplest form.", fr(13, 20), [fr(7, 20), fr(65, 10), fr(35, 100)], "100% − 35% = 65% = 65/100 = <b>13/20</b>."),
        ("One shop has “1/5 off” and another has “25% off”. Which is the bigger discount?", "25% off", ["1/5 off", "They are the same", "You cannot tell"], "1/5 = 20%, which is less than 25%, so <b>25% off</b>."),
        ("A water tank is 0.45 full. What percentage of the tank is empty?", "55%", ["45%", "0.55%", "5.5%"], "0.45 = 45% full, so 100% − 45% = <b>55%</b> is empty."),
        ("A phone battery shows 0.6 charged. What does the percentage display show?", "60%", ["6%", "0.6%", "600%"], "0.6 × 100 = <b>60%</b>."),
        ("Which decimal is the same as 150%?", "1.5", ["0.15", "15", "0.015"], "150% = 150/100 = <b>1.5</b>. More than 100% means more than the whole."),
        ("Which number is halfway between 0.3 and 0.4 on a number line?", "0.35", ["0.34", "0.305", "3.5"], "0.3 = 0.30 and 0.4 = 0.40, so halfway is <b>0.35</b>."),
        ("Which is closer to 1 on a number line: 7/8 or 0.9?", "0.9", ["7/8", "They are the same distance", "You cannot tell"], "7/8 = 0.875, which is 0.125 from 1. 0.9 is 0.1 from 1, so <b>0.9</b> is closer."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>Fractions, decimals and percentages are three ways to write the same amount. <b>Percent</b> means “out of 100”.</p>"
        + table(["Fraction", "Decimal", "Percentage"],
                [[fr(1, 2), "0.5", "50%"], [fr(1, 4), "0.25", "25%"], [fr(3, 4), "0.75", "75%"], [fr(1, 5), "0.2", "20%"],
                 [fr(1, 8), "0.125", "12.5%"], [fr(1, 10), "0.1", "10%"]])
        + "<p>Fraction → decimal: divide the top by the bottom. Decimal → percentage: × 100. "
        "Percentage → fraction: write over 100 and simplify.</p>",
        [("Write 3/8 as a decimal and a percentage.", ["3 ÷ 8 = 0.375.", "0.375 × 100 = 37.5%."], "0.375 and 37.5%"),
         ("Write 0.35 as a fraction in its simplest form.", ["0.35 = 35/100.", "Divide top and bottom by 5."], "7/20"),
         ("Which is larger, 3/5 or 0.58?", ["3/5 = 0.6.", "0.6 is larger than 0.58."], "3/5")],
        ["Writing the digits of a fraction as a decimal: 3/8 is 0.375, not 0.38 or 3.8.",
         "Forgetting to multiply by 100: 0.4 is 40%, not 4% or 0.4%.",
         "Mixing up tenths and hundredths: 0.07 is 7/100, not 7/10.",
         "Not simplifying: 0.35 = 35/100 = 7/20."])


def main():
    sets = [S("Fractions to decimals", collect(one_f2d, 20, R)),
            S("Decimals and percentages to fractions", collect(one_d2f, 20, R)),
            S("Writing percentages", collect(one_2p, 14, R) + collect(one_equiv, 6, R)),
            S("Rational numbers on a number line", collect(one_nl, 20, R)),
            S("Ordering, equivalence and problems", problems())]
    make(7, "fractions-decimals-and-percentages", 3, "AC9M7N04",
         "Fractions, Decimals and Percentages: Equivalent Forms and Number Lines",
         "Year 7 Fractions, Decimals and Percentages Worksheets: Converting, Number Lines and Ordering (Free, Answer Key)",
         "Fractions, decimals and percentages",
         "find equivalent representations of rational numbers and represent rational numbers on a number line",
         "Free Year 7 maths worksheets on fractions, decimals and percentages for the Australian Curriculum (AC9M7N04): "
         "converting between forms, simplest form, rational numbers on a number line, ordering and problems. 100 questions with an answer key.",
         "Fraction → decimal: divide. Decimal → percentage: × 100. Percentage → fraction: over 100, then simplify.",
         "On a number line, find what each small space is worth before you count.",
         body(),
         [("How do you turn a fraction into a percentage?", "Divide the numerator by the denominator to get a decimal, then multiply by 100. 3/8 = 0.375 = 37.5%."),
          ("How do you write a percentage as a fraction?", "Write it over 100 and simplify. 45% = 45/100 = 9/20."),
          ("How do I order fractions, decimals and percentages?", "Change them all into the same form, usually decimals, then compare."),
          ("Can a percentage be more than 100%?", "Yes. 120% means 1.2 times the whole amount.")],
         sets, R)


if __name__ == "__main__":
    main()
