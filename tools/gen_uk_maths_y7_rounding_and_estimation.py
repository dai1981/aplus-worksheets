# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Rounding and Estimation (KS3 Number)
  python3 tools/gen_uk_maths_y7_rounding_and_estimation.py
Rounding to decimal places and significant figures, estimating calculations by rounding to 1 significant
figure, and problems. Wrong answers come from real mistakes: cutting off instead of rounding, counting
the leading zeros as significant, dropping the place-holder zeros, and rounding to the wrong place.
"""
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, gbp

R = random.Random(70601)


def D(v):
    return Decimal(str(float(v))) if not isinstance(v, Decimal) else v


def rdp(v, k, mode=ROUND_HALF_UP):
    return F(str(D(v).quantize(Decimal(1).scaleb(-k), rounding=mode)))


def rsf(v, k, mode=ROUND_HALF_UP):
    d = D(v)
    if d == 0:
        return F(0)
    e = d.adjusted()
    return F(str(d.quantize(Decimal(1).scaleb(e - k + 1), rounding=mode)))


def ordinal(k):
    return {1: "1 decimal place", 2: "2 decimal places", 3: "3 decimal places"}[k]


def sfw(k):
    return "%d significant figure%s" % (k, "" if k == 1 else "s")


# ------------------------------------------------------------ set 1: decimal places
def one_dp(r):
    k = r.choice([1, 1, 2, 2, 3])
    whole = r.randint(0, 60)
    digits = k + r.randint(1, 2)
    v = F(whole) + F(r.randint(1, 10 ** digits - 1), 10 ** digits)
    ans = rdp(v, k)
    cut = rdp(v, k, ROUND_DOWN)
    if ans == v:
        return None
    up = ans != cut
    wr = [(cut, k), (rdp(v, k - 1), k - 1), (rdp(v, k + 1), k + 1) if digits > k + 1 else None,
          (ans + F(1, 10 ** k), k), (ans - F(1, 10 ** k), k)]
    q = "Round %s to %s." % (B(num(v)), ordinal(k))
    e = ("Look at the next digit after the %s decimal place. It is %s, so round %s: <b>%s</b>."
         % (["", "1st", "2nd", "3rd"][k], "5 or more" if up else "4 or less", "up" if up else "down", fmt_dp(ans, k)))
    cands = [(fmt_dp(w, p), fmt_dp(w, p)) for w, p in [x for x in wr if x] if fmt_dp(w, p) != fmt_dp(ans, k)]
    return mcq(q, (fmt_dp(ans, k), fmt_dp(ans, k)), cands, e)


def fmt_dp(v, k):
    """Show with exactly k decimal places (2.40 keeps its zero)."""
    s = str(D(v).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP)) if k > 0 else num(v)
    ip, _, fp = s.partition(".")
    return "{:,}".format(int(ip)) + ("." + fp if fp else "")


def one_dp_zero(r):
    """Cases where the answer ends in 0: 3.996 to 2 dp = 4.00."""
    k = r.choice([1, 2])
    base = F(r.randint(1, 30))
    v = base - F(r.randint(1, 4), 10 ** (k + 1))
    ans = rdp(v, k)
    if ans != base:
        return None
    q = "Round %s to %s." % (B(num(v)), ordinal(k))
    shown = fmt_dp(ans, k)
    wr = [num(base), fmt_dp(rdp(v, k, ROUND_DOWN), k), fmt_dp(base - 1, k) if base > 1 else fmt_dp(base + 1, k)]
    e = "Rounding up carries into the next column. Keep the zero%s to show %s: <b>%s</b>." % ("s" if k > 1 else "", ordinal(k), shown)
    return T(q, shown, [w for w in wr if w != shown], e)


# ------------------------------------------------------------ set 2: significant figures
def one_sf(r):
    k = r.choice([1, 1, 2, 2, 3])
    kind = r.choice(["big", "big", "small", "dec"])
    if kind == "big":
        v = F(r.randint(1000, 99999))
    elif kind == "small":
        v = F(r.randint(1001, 9999), r.choice([10 ** 5, 10 ** 6]))
    else:
        v = F(r.randint(1001, 99999), r.choice([100, 1000]))
    ans = rsf(v, k)
    cut = rsf(v, k, ROUND_DOWN)
    if ans == v:
        return None
    digs = num(ans).replace(",", "").replace(".", "").lstrip("0")
    if ans.denominator > 1 and len(digs) < k:
        return None
    if ans == cut:
        cut = rsf(v, k, ROUND_DOWN) + (rsf(v, k) - rsf(v, k + 1) if False else 0)
    wr = [cut if cut != ans else None]
    if kind == "big":
        drop = ans
        while drop.denominator == 1 and drop % 10 == 0 and drop:
            drop /= 10
        wr.append(drop)          # dropped place-holder zeros
        wr.append(rsf(v, k + 1))
    elif kind == "small":
        wr.append(rdp(v, k))     # counted leading zeros
        wr.append(rsf(v, k + 1))
    else:
        wr.append(rdp(v, k))
        wr.append(rsf(v, k + 1))
    step = F(10) ** (D(v).adjusted() - k + 1) if D(v).adjusted() - k + 1 >= 0 else F(1, 10 ** (k - 1 - D(v).adjusted()))
    wr.append(ans - step if ans > cut else ans + step)
    q = "Round %s to %s." % (B(num(v)), sfw(k))
    e = ("Start counting at the first non-zero digit. Look at the digit after the %s: round %s. <b>%s</b>%s." %
         (sfw(k).replace("figures", "figure").replace("1 significant figure", "1st significant figure"),
          "up" if ans > cut else "down", num(ans),
          " (keep the zeros as place holders)" if kind == "big" else ""))
    return QN(q, ans, [w for w in wr if w], e, near=())


# ------------------------------------------------------------ set 3: estimating calculations
def one_est(r):
    form = r.randint(0, 3)
    a = F(r.randint(11, 99)) / r.choice([1, 10])
    b = F(r.randint(11, 99)) / r.choice([1, 10])
    if form == 0:
        ra, rb = rsf(a, 1), rsf(b, 1)
        est = ra * rb
        q = "Estimate %s by rounding each number to 1 significant figure." % B("%s × %s" % (num(a), num(b)))
        exact = a * b
        wr = [rdp(exact, 0), rsf(a, 1, ROUND_DOWN) * rsf(b, 1, ROUND_DOWN), est * 10]
        e = "%s ≈ %s and %s ≈ %s, so the estimate is %s × %s = <b>%s</b>." % (num(a), num(ra), num(b), num(rb), num(ra), num(rb), num(est))
    elif form == 1:
        ra, rb = rsf(a, 1), rsf(b, 1)
        if ra % rb and rb % ra == 0:
            return None
        if F(ra / rb).denominator > 10 or not ra / rb:
            return None
        est = ra / rb
        if est.denominator not in (1, 2, 4, 5, 10):
            return None
        q = "Estimate %s by rounding each number to 1 significant figure." % B("%s ÷ %s" % (num(a), num(b)))
        wr = [rb / ra, ra * rb, est * 10]
        e = "%s ≈ %s and %s ≈ %s, so the estimate is %s ÷ %s = <b>%s</b>." % (num(a), num(ra), num(b), num(rb), num(ra), num(rb), num(est))
    elif form == 2:
        c = F(r.randint(11, 49), 10)
        ra, rb, rc = rsf(a, 1), rsf(b, 1), rsf(c, 1)
        if (ra + rb) % rc:
            return None
        est = (ra + rb) / rc
        q = "Estimate %s by rounding each number to 1 significant figure." % B(
            "<span class='fr'><span class='fn'>%s + %s</span><span class='fd'>%s</span></span>" % (num(a), num(b), num(c)))
        wr = [ra + rb / rc if (rb / rc).denominator == 1 else ra + rb, ra + rb, est * 2]
        e = "≈ (%s + %s) ÷ %s = %s ÷ %s = <b>%s</b>." % (num(ra), num(rb), num(rc), num(ra + rb), num(rc), num(est))
    else:
        ra = rsf(a, 1)
        sq = r.choice([F(r.randint(15, 99))])
        root = {16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9}
        near = min(root, key=lambda x: abs(x - sq))
        if abs(near - sq) > 3:
            return None
        est = ra * root[near]
        q = "Estimate %s." % B("%s × √%s" % (num(a), num(sq)))
        wr = [ra * sq, ra * sq / 2, est + ra]
        e = "%s ≈ %s and √%s ≈ √%d = %d, so the estimate is <b>%s</b>." % (num(a), num(ra), num(sq), near, root[near], num(est))
    if est == 0 or est.denominator not in (1, 2, 4, 5, 10):
        return None
    return QN(q, est, [w for w in wr if w is not None], e)


# ------------------------------------------------------------ set 4: mixed rounding
def one_mixed(r):
    v = F(r.randint(10001, 99999), r.choice([10, 100, 1000]))
    target = r.choice(["nearest whole number", "nearest 10", "nearest 100", "1 decimal place", "1 significant figure", "2 significant figures"])
    fn = {"nearest whole number": lambda x: rdp(x, 0), "nearest 10": lambda x: rsf(x, len(str(int(x))) - 1),
          "nearest 100": lambda x: rsf(x, len(str(int(x))) - 2), "1 decimal place": lambda x: rdp(x, 1),
          "1 significant figure": lambda x: rsf(x, 1), "2 significant figures": lambda x: rsf(x, 2)}
    ans = fn[target](v)
    others = [fn[t](v) for t in fn if t != target]
    others = [o for o in others if o != ans and o != 0]
    if (target == "nearest 100" and v < 1000) or (target == "nearest 10" and v < 100):
        return None
    if len(set(others)) < 3:
        return None
    if target == "1 decimal place":
        return mcq("Round %s to the %s." % (B(num(v)), target) if "nearest" in target else "Round %s to %s." % (B(num(v)), target),
                   (fmt_dp(ans, 1), ans), [(num(o), o) for o in others], "Rounded to %s: <b>%s</b>." % (target, fmt_dp(ans, 1)))
    q = ("Round %s to the %s." if "nearest" in target else "Round %s to %s.") % (B(num(v)), target)
    return QN(q, ans, others, "Rounded to %s: <b>%s</b>. Check which column you are rounding to before you look at the next digit." % (target, num(ans)))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for n, item, price in [(19, "tickets", F("4.95")), (31, "T-shirts", F("8.10")), (48, "books", F("2.99")), (21, "meals", F("11.80")),
                           (9, "sandwiches", F("3.15"))]:
        rn, rp = rsf(n, 1), rsf(price, 1)
        est = rn * rp
        q = "Estimate the cost of %d %s at %s each." % (n, item, gbp(price))
        e = "%d ≈ %s and %s ≈ %s, so about %s × %s = <b>%s</b>." % (n, num(rn), gbp(price), gbp(rp), num(rn), gbp(rp), gbp(est))
        its.append(mcq(q, (gbp(est), est), [(gbp(w), w) for w in [est * 10, rn + rp, est / 10, est + rp] if w != est], e))
    for q, ans, wr, e in [
            ("A bag of sugar weighs 2.347 kg. Round this to 1 decimal place.", "2.3 kg", ["2.4 kg", "2.35 kg", "2 kg"],
             "The digit after the 3 is 4, so round down: <b>2.3 kg</b>."),
            ("A pupil's height is 1.685 m. Round this to 2 decimal places.", "1.69 m", ["1.68 m", "1.7 m", "1.685 m"],
             "The digit after the 8 is 5, so round up: <b>1.69 m</b>."),
            ("A runner's time is 12.96 seconds. Round this to 1 decimal place.", "13.0 seconds", ["12.9 seconds", "13 seconds", "12.10 seconds"],
             "The digit after the 9 is 6, so round up. 12.9 becomes 13.0. Keep the .0 to show 1 decimal place: <b>13.0 seconds</b>."),
            ("A test tube holds 0.4851 litres. Round this to 2 significant figures.", "0.49 litres", ["0.48 litres", "0.5 litres", "0.485 litres"],
             "The significant figures start at 4. The 2nd is 8 and the next digit is 5, so round up: <b>0.49 litres</b>.")]:
        its.append(T(q, ans, wr, e))
    for pop, k, ans_txt, wr in [(48_372, 1, "50,000", ["48,000", "40,000", "5"]),
                                (2_651_809, 2, "2,700,000", ["2,600,000", "27", "2,650,000"]),
                                (736_492, 2, "740,000", ["730,000", "74", "736,000"])]:
        its.append(T("A town has a population of %s. Round this to %s." % (num(pop), sfw(k)), ans_txt, wr,
                     "Keep %d significant figure%s and replace the rest with zeros: <b>%s</b>." % (k, "" if k == 1 else "s", ans_txt)))
    data = [("Mia works out 38.7 × 21.4 and gets 8,281.8. Use an estimate to decide if this is sensible.",
             "No, it should be about 800", ["Yes, it is about 8,000", "No, it should be about 80", "Yes, it is exactly right"],
             "38.7 × 21.4 ≈ 40 × 20 = 800, so 8,281.8 is about 10 times too big. (The answer is 828.18.)"),
            ("Which is the best estimate for 0.48 × 61?", "30", ["3", "300", "24"], "0.48 ≈ 0.5 and 61 ≈ 60, so 0.5 × 60 = <b>30</b>."),
            ("Which is the best estimate for 812 ÷ 3.9?", "200", ["20", "2,000", "320"], "812 ≈ 800 and 3.9 ≈ 4, so 800 ÷ 4 = <b>200</b>."),
            ("A car travels 297 miles on 9.8 gallons of fuel. Estimate the miles per gallon.", "30", ["3", "300", "29.7"],
             "297 ≈ 300 and 9.8 ≈ 10, so 300 ÷ 10 = <b>30</b> miles per gallon."),
            ("Estimate the area of a room 4.85 m by 3.12 m.", "15 m²", ["16 m²", "12 m²", "20 m²"], "4.85 ≈ 5 and 3.12 ≈ 3, so 5 × 3 = <b>15 m²</b>."),
            ("Estimate 6.1² + √99.", "46", ["36", "48", "135"], "6.1² ≈ 6² = 36 and √99 ≈ √100 = 10, so 36 + 10 = <b>46</b>."),
            ("Round 0.00762 to 1 significant figure.", "0.008", ["0.007", "0.01", "0.00762"], "The first significant figure is the 7 (zeros at the start do not count). The next digit is 6, so round up: <b>0.008</b>."),
            ("Round 9.97 to 1 decimal place.", "10.0", ["9.9", "10", "9.10"], "9.97 rounds up to 10.0. Keep the .0 to show 1 decimal place.")]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>To round, find the last digit you keep, then look at the <b>next</b> digit: 5 or more, round up; 4 or less, keep it.</p>"
        "<p><b>Decimal places</b> are counted after the point. <b>Significant figures</b> are counted from the first "
        "non-zero digit. When you round a big number, fill the gaps with zeros: 48,372 to 1 s.f. is 50,000.</p>"
        "<p>To <b>estimate</b>, round each number to 1 significant figure, then calculate.</p>",
        [("Round 0.04851 to 2 significant figures.", ["The first significant figure is 4, the second is 8.", "The next digit is 5, so round up."], "0.049"),
         ("Estimate 38.7 × 21.4.", ["38.7 ≈ 40 and 21.4 ≈ 20.", "40 × 20 = 800."], "800")],
        ["Cutting off digits instead of rounding: 2.347 to 1 d.p. is 2.3, but 2.36 is 2.4.",
         "Counting zeros at the start as significant figures: 0.0076 to 1 s.f. is 0.008.",
         "Dropping place-holder zeros: 48,372 to 1 s.f. is 50,000, not 5.",
         "Leaving off a final zero: 9.97 to 1 d.p. is 10.0, not 10."])


def main():
    sets = [S("Rounding to decimal places", collect(one_dp, 15, R) + collect(one_dp_zero, 5, R)),
            S("Rounding to significant figures", collect(one_sf, 20, R)),
            S("Choosing the right rounding", collect(one_mixed, 20, R)),
            S("Estimating calculations", collect(one_est, 20, R)),
            S("Problems", problems())]
    make(7, "rounding-and-estimation", 6, "N",
         "Rounding and Estimation: Decimal Places and Significant Figures",
         "Year 7 Rounding Worksheets: Decimal Places, Significant Figures and Estimating Calculations",
         "Rounding and estimation",
         "Round numbers and measures to an appropriate degree of accuracy (for example, to a number of decimal places or "
         "significant figures); use approximation through rounding to estimate answers and calculate possible resulting errors.",
         "Free Year 7 rounding worksheets: round to decimal places and significant figures, choose the right rounding, "
         "and estimate calculations by rounding to 1 significant figure. 100 questions with answers.",
         "Round to 1 significant figure to estimate: 38.7 × 21.4 ≈ 40 × 20 = 800.",
         "Significant figures start at the first non-zero digit. Keep place-holder zeros: 48,372 ≈ 50,000.",
         body(),
         [("What is the difference between decimal places and significant figures?", "Decimal places are counted after the decimal point. Significant figures are counted from the first non-zero digit, which may be before the point."),
          ("Are zeros significant figures?", "Zeros at the start, as in 0.0076, are not. Zeros between other digits, as in 4,05, are. Zeros at the end of a rounded whole number are place holders."),
          ("Why do we estimate?", "To check that a calculator answer is sensible. If 38.7 × 21.4 should be about 800, then 8,281.8 must be wrong."),
          ("What do I do when the next digit is 5?", "Round up. 2.45 to 1 decimal place is 2.5.")],
         sets, R)


if __name__ == "__main__":
    main()
