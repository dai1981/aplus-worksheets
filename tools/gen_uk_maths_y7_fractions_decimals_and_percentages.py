# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Fractions, Decimals and Percentages (KS3 Number)
  python3 tools/gen_uk_maths_y7_fractions_decimals_and_percentages.py
Converting between fractions, decimals and percentages, ordering a mixed list, and test-score and
comparison problems. Wrong answers come from real mistakes: writing 3/8 as 0.38, 0.4 as 4%, 0.07 as 7/10,
and not simplifying.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, fr, table

R = random.Random(70701)


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
    e = "%d ÷ %d = <b>%s</b>. (Or make the denominator 10, 100 or 1,000 first.)" % (v.numerator, v.denominator, num(v))
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


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for name, score, out in [("Amelia", 17, 20), ("Harry", 21, 25), ("Zara", 36, 40), ("Leo", 42, 50), ("Isla", 7, 8), ("Theo", 13, 20)]:
        v = F(score, out)
        q = "%s scored %d out of %d in a test. What percentage is this?" % (name, score, out)
        e = "%d/%d = %s = <b>%s</b>." % (score, out, num(v), pct(v))
        its.append(mcq(q, (pct(v), v), [(num(w) + "%", w) for w in [F(score), F(100 - out + score), F(out - score) * 100 / out, v * 100 + 5] if w != v * 100], e))
    for a, b in [((17, 20), (21, 25)), ((7, 8), (43, 50)), ((3, 5), (13, 20)), ((18, 25), (37, 50))]:
        va, vb = F(*a), F(*b)
        best = "Test A" if va > vb else "Test B"
        q = "Ruby scored %d out of %d in Test A and %d out of %d in Test B. In which test did she do better?" % (a[0], a[1], b[0], b[1])
        e = "Test A: %s. Test B: %s. So <b>%s</b>." % (pct(va), pct(vb), best)
        its.append(T(q, best, ["Test B" if best == "Test A" else "Test A", "They are the same", "You cannot tell"], e))
    data = [
        ("In a class, 3/5 of the pupils walk to school. What percentage is this?", "60%", ["35%", "3.5%", "0.6%"], "3/5 = 6/10 = <b>60%</b>."),
        ("45% of the pupils in a school are boys. What fraction are girls? Give it in its simplest form.", fr(11, 20), [fr(9, 20), fr(55, 10), fr(45, 100)], "Girls: 100% − 45% = 55% = 55/100 = <b>11/20</b>."),
        ("A shop has “1/4 off” and another has “20% off”. Which is the bigger discount?", "1/4 off", ["20% off", "They are the same", "You cannot tell"], "1/4 = 25%, which is more than 20%, so <b>1/4 off</b>."),
        ("A jug is 0.35 full. What percentage of the jug is empty?", "65%", ["35%", "0.65%", "3.5%"], "0.35 = 35% full, so 100% − 35% = <b>65%</b> is empty."),
        ("Which of these is the same as 0.125?", fr(1, 8), [fr(1, 25), fr(125, 100), "12.5"], "0.125 = 125/1000 = <b>1/8</b>."),
        ("A battery shows 0.4 charged. What does the percentage display show?", "40%", ["4%", "0.4%", "400%"], "0.4 × 100 = <b>40%</b>."),
        ("2/5 of a garden is lawn and 30% is patio. What percentage is left?", "30%", ["68%", "70%", "40%"], "2/5 = 40%. 40% + 30% = 70%, so 100% − 70% = <b>30%</b> is left."),
        ("Which list is in order from smallest to largest?", "0.3, 1/3, 35%", ["1/3, 0.3, 35%", "35%, 1/3, 0.3", "0.3, 35%, 1/3"], "0.3 = 0.3, 1/3 = 0.333…, 35% = 0.35. So <b>0.3, 1/3, 35%</b>."),
        ("Which decimal is the same as 120%?", "1.2", ["0.12", "12", fr(12, 1000)], "120% = 120/100 = <b>1.2</b>. More than 100% means more than the whole."),
        ("A survey says 0.08 of people cycle to work. Write this as a percentage.", "8%", ["0.8%", "80%", "0.08%"], "0.08 × 100 = <b>8%</b>."),
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
            S("Writing percentages", collect(one_2p, 20, R)),
            S("Equivalent values and ordering", collect(one_equiv, 10, R) + collect(one_order, 10, R)),
            S("Problems", problems())]
    make(7, "fractions-decimals-and-percentages", 7, "N",
         "Fractions, Decimals and Percentages: Converting and Ordering",
         "Year 7 Fractions, Decimals and Percentages Worksheets: Converting, Comparing and Ordering FDP",
         "Fractions, decimals and percentages",
         "Work interchangeably with terminating decimals and their corresponding fractions (such as 3.5 and 7/2 or 0.375 "
         "and 3/8); define percentage as ‘number of parts per hundred’, interpret percentages and percentage changes as a "
         "fraction or a decimal, and compare two quantities using percentages.",
         "Free Year 7 worksheets on fractions, decimals and percentages: convert between FDP, write in simplest form, "
         "compare and order mixed lists, and test-score problems. 100 questions with answers.",
         "Fraction → decimal: divide. Decimal → percentage: × 100. Percentage → fraction: over 100, then simplify.",
         "To compare a mix of fractions, decimals and percentages, change them all to decimals.",
         body(),
         [("How do you turn a fraction into a percentage?", "Divide the numerator by the denominator to get a decimal, then multiply by 100. 3/8 = 0.375 = 37.5%."),
          ("How do you write a percentage as a fraction?", "Write it over 100 and simplify. 45% = 45/100 = 9/20."),
          ("How do I order fractions, decimals and percentages?", "Change them all into the same form, usually decimals, then compare."),
          ("Can a percentage be more than 100%?", "Yes. 120% means 1.2 times the whole amount.")],
         sets, R)


if __name__ == "__main__":
    main()
