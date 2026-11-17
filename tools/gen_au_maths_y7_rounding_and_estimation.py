# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Rounding and estimation (Australian Curriculum v9.0: AC9M7N05)
  python3 tools/gen_au_maths_y7_rounding_and_estimation.py
Rounding decimals to a given number of places, rounding to the accuracy that suits the context (cents, cash
rounding to 5c, measurements), estimating calculations with leading-digit rounding, and checking whether
a calculator answer is reasonable.
Wrong answers come from real mistakes: cutting off instead of rounding, rounding to the wrong place,
dropping a final zero (9.97 to 1 d.p. is 10.0), and cash-rounding to the nearest 10c instead of 5c.
"""
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, aud, comma

R = random.Random(70401)


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
    return comma(int(ip)) + ("." + fp if fp else "")


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


# ------------------------------------------------------------ set 3: rounding in context
def one_ctx(r):
    kind = r.choice(["cent", "cash", "cash", "measure", "people"])
    if kind == "cent":
        v = F(r.randint(1001, 99999), 1000)
        ans = rdp(v, 2)
        if ans == v:
            return None
        q = "A calculator shows %s for the cost of some fuel in dollars. What is this to the nearest cent?" % B(num(v))
        wr = [rdp(v, 2, ROUND_DOWN) if rdp(v, 2, ROUND_DOWN) != ans else ans + F(1, 100), rdp(v, 1), rdp(v, 0)]
        return mcq(q, (aud(ans), ans), [(aud(w), w) for w in wr if w != ans], "Cents are 2 decimal places. The next digit decides: <b>%s</b>." % aud(ans))
    if kind == "cash":
        cents = r.randint(101, 4999)
        if cents % 5 == 0:
            return None
        v = F(cents, 100)
        ans = F(int(Decimal(cents) / 5 + Decimal("0.5")) * 5 if cents % 5 != 2.5 else 0, 100)
        last = cents % 10
        ans = F(cents - last + (0 if last in (1, 2) else 5 if last in (3, 4, 6, 7) else 10), 100)
        q = "A shop total is %s. Australia has no 1c or 2c coins, so cash totals are rounded to the nearest 5c. How much do you pay in cash?" % aud(v)
        wr = [rdp(v, 1), ans + F(5, 100) if ans + F(5, 100) != rdp(v, 1) else ans - F(5, 100), ans - F(5, 100) if ans - F(5, 100) != rdp(v, 1) else ans + F(10, 100), rdp(v, 1, ROUND_DOWN)]
        e = "Totals ending in 1c or 2c round down to 0c; 3c, 4c, 6c and 7c round to 5c; 8c and 9c round up. So %s becomes <b>%s</b>." % (aud(v), aud(ans))
        return mcq(q, (aud(ans), ans), [(aud(w), w) for w in wr if w != ans], e)
    if kind == "measure":
        thing, unit, k = r.choice([("a plank of timber", "m", 2), ("a baby's mass", "kg", 1), ("a runner's time", "seconds", 2), ("the rainfall", "mm", 1), ("a parcel", "kg", 1)])
        v = F(r.randint(1001, 9999), 1000) * (10 if unit in ("seconds", "mm") else 1)
        ans = rdp(v, k)
        if ans == v:
            return None
        q = "The measurement of %s is %s %s. Round it to %s." % (thing, num(v), unit, ordinal(k))
        wr = [rdp(v, k, ROUND_DOWN), rdp(v, k + 1), rdp(v, k - 1)]
        return mcq(q, (fmt_dp(ans, k) + " " + unit, ans), [(fmt_dp(w, k if w in (rdp(v, k, ROUND_DOWN),) else (k + 1 if w == rdp(v, k + 1) else k - 1)) + " " + unit, w) for w in wr if w != ans],
                   "Keep %s and look at the next digit: <b>%s %s</b>." % (ordinal(k), fmt_dp(ans, k), unit))
    total = r.randint(100, 400)
    per = r.choice([12, 15, 20, 24, 25, 30, 40, 45, 50, 55])
    if total % per == 0:
        return None
    what = r.choice([("people need to travel. A minibus holds %d people." , "minibuses are needed", "up"), ("muffins are baked. A box holds %d muffins.", "boxes can be filled completely", "down")])
    n_up, n_down = -(-total // per), total // per
    ans = n_up if what[2] == "up" else n_down
    q = ("%d " + what[0] + " How many " + what[1] + "?") % (total, per)
    e = "%d ÷ %d = %s. %s" % (total, per, num(F(total, per)) if F(total, per).denominator in (2, 4, 5, 8, 10, 20, 25, 40, 50) else "%d remainder %d" % (n_down, total % per),
                              "Round <b>up</b> so everyone gets a seat: <b>%d</b>." % ans if what[2] == "up" else "Only full boxes count, so round <b>down</b>: <b>%d</b>." % ans)
    return QN(q, ans, [n_down if ans == n_up else n_up, ans + 2, total // 10], e)


# ------------------------------------------------------------ set 4: estimating calculations
def one_est(r):
    form = r.randint(0, 3)
    a = F(r.randint(11, 99)) / r.choice([1, 10])
    b = F(r.randint(11, 99)) / r.choice([1, 10])
    if any(x.denominator == 1 and x < 10 for x in (a, b)) or any(x.denominator == 1 and x % 10 == 0 for x in (a, b)):
        return None
    if form == 0:
        ra, rb = rsf(a, 1), rsf(b, 1)
        est = ra * rb
        q = "Estimate %s by rounding each number to its leading digit." % B("%s × %s" % (num(a), num(b)))
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
        q = "Estimate %s by rounding each number to its leading digit." % B("%s ÷ %s" % (num(a), num(b)))
        wr = [rb / ra, ra * rb, est * 10]
        e = "%s ≈ %s and %s ≈ %s, so the estimate is %s ÷ %s = <b>%s</b>." % (num(a), num(ra), num(b), num(rb), num(ra), num(rb), num(est))
    elif form == 2:
        c = F(r.randint(11, 49), 10)
        ra, rb, rc = rsf(a, 1), rsf(b, 1), rsf(c, 1)
        if (ra + rb) % rc:
            return None
        est = (ra + rb) / rc
        q = "Estimate %s by rounding each number to its leading digit." % B(
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
    v = F(r.randint(1001, 99999), r.choice([10, 100, 1000]))
    target = r.choice(["nearest whole number", "nearest 10", "nearest 100", "1 decimal place", "2 decimal places"])
    fn = {"nearest whole number": lambda x: rdp(x, 0), "nearest 10": lambda x: rsf(x, len(str(int(x))) - 1),
          "nearest 100": lambda x: rsf(x, len(str(int(x))) - 2), "1 decimal place": lambda x: rdp(x, 1),
          "2 decimal places": lambda x: rdp(x, 2)}
    ans = fn[target](v)
    others = [fn[t](v) for t in fn if t != target]
    others = [o for o in others if o != ans and o != 0]
    if (target == "nearest 100" and v < 1000) or (target == "nearest 10" and v < 100):
        return None
    if len(set(others)) < 3 or (target == "2 decimal places" and v.denominator <= 100):
        return None
    if "decimal" in target:
        k = 1 if target.startswith("1") else 2
        return mcq("Round %s to %s." % (B(num(v)), target),
                   (fmt_dp(ans, k), ans), [(num(o), o) for o in others], "Rounded to %s: <b>%s</b>." % (target, fmt_dp(ans, k)))
    q = ("Round %s to the %s." if "nearest" in target else "Round %s to %s.") % (B(num(v)), target)
    return QN(q, ans, others, "Rounded to %s: <b>%s</b>. Check which column you are rounding to before you look at the next digit." % (target, num(ans)))


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for n, item, price in [(19, "movie tickets", F("21.95")), (32, "school jumpers", F("38.50")), (48, "exercise books", F("2.95")), (21, "pies", F("6.80")),
                           (9, "pool passes", F("7.10"))]:
        rn, rp = rsf(n, 1), rsf(price, 1)
        est = rn * rp
        q = "Estimate the cost of %d %s at %s each." % (n, item, aud(price))
        e = "%d ≈ %s and %s ≈ %s, so about %s × %s = <b>%s</b>." % (n, num(rn), aud(price), aud(rp), num(rn), aud(rp), aud(est))
        its.append(mcq(q, (aud(est), est), [(aud(w), w) for w in [est * 10, rn + rp, est / 10, est + rp] if w != est], e))
    data = [("Isla works out 38.7 × 21.4 on a calculator and gets 8281.8. Use an estimate to decide if this is reasonable.",
             "No, it should be about 800", ["Yes, it is about 8000", "No, it should be about 80", "Yes, it is exactly right"],
             "38.7 × 21.4 ≈ 40 × 20 = 800, so 8281.8 is about 10 times too big. (The answer is 828.18.)"),
            ("Which is the best estimate for 0.48 × 61?", "30", ["3", "300", "24"], "0.48 ≈ 0.5 and 61 ≈ 60, so 0.5 × 60 = <b>30</b>."),
            ("Which is the best estimate for 612 ÷ 2.9?", "200", ["20", "2000", "180"], "612 ≈ 600 and 2.9 ≈ 3, so 600 ÷ 3 = <b>200</b>."),
            ("A car uses 7.9 L of fuel per 100 km. Estimate the fuel used on a 395 km trip from Sydney to Canberra and back... one way.", "32 L", ["3.2 L", "320 L", "8 L"],
             "395 km ≈ 400 km = 4 lots of 100 km, and 7.9 ≈ 8, so about 4 × 8 = <b>32 L</b>."),
            ("Estimate the area of a bedroom 4.85 m by 3.12 m.", "15 m²", ["16 m²", "12 m²", "20 m²"], "4.85 ≈ 5 and 3.12 ≈ 3, so 5 × 3 = <b>15 m²</b>."),
            ("Which accuracy makes most sense for the price of petrol per litre in dollars?", "To the nearest tenth of a cent, such as $1.879", ["To the nearest dollar", "To the nearest $10", "To 6 decimal places"],
             "Petrol prices are shown in cents and tenths of a cent, so <b>to the nearest tenth of a cent</b>."),
            ("Which is the most sensible way to give a person's height?", "To the nearest centimetre, such as 1.62 m", ["To the nearest metre, such as 2 m", "To the nearest millimetre of a millimetre", "To 5 decimal places of a metre"],
             "Heights are usually given <b>to the nearest centimetre</b>."),
            ("Round 9.97 to 1 decimal place.", "10.0", ["9.9", "10", "9.10"], "9.97 rounds up to 10.0. Keep the .0 to show 1 decimal place."),
            ("A recipe needs 0.375 kg of flour. Round this to the nearest tenth of a kilogram.", "0.4 kg", ["0.3 kg", "0.38 kg", "0.37 kg"],
             "The digit after the 3 is 7, so round up: <b>0.4 kg</b>."),
            ("Liam's calculator says 53 ÷ 7 = 7.571428571. What is this to 2 decimal places?", "7.57", ["7.58", "7.5", "7.571"], "The digit after the 7 in the hundredths is 1, so round down: <b>7.57</b>."),
            ("A cash total of $19.98 is rounded to the nearest 5c. What is paid?", "$20", ["$19.95", "$19.90", "$19.98"], "8c rounds up to 10c, so $19.98 becomes <b>$20</b>."),
            ("Estimate 6.1² + 49.3.", "85", ["36", "61", "135"], "6.1² ≈ 6² = 36 and 49.3 ≈ 49, so 36 + 49 = <b>85</b>."),
            ("Mia estimates 297 × 51 as 300 × 50. Is her estimate more or less than the exact answer?", "Less, because 51 was rounded down more than 297 was rounded up", ["More, because 297 was rounded up", "Exactly the same", "You cannot tell"],
             "300 × 50 = 15 000 and 297 × 51 = 15 147, so the estimate is <b>less</b>."),
            ("Which calculation gives the best estimate of 4.92 × 19.6?", "5 × 20", ["4 × 19", "5 × 19", "4 × 20"], "Round each number to its leading digit: <b>5 × 20</b> = 100."),
            ("A bottle holds 1.25 L. Round this to the nearest litre.", "1 L", ["2 L", "1.3 L", "1.2 L"], "The digit after the 1 is 2, so round down: <b>1 L</b>.")]
    data[3] = ("A car uses 7.9 L of fuel per 100 km. Estimate the fuel used on a 395 km trip.", "32 L", ["3.2 L", "320 L", "8 L"],
               "395 km ≈ 400 km = 4 lots of 100 km, and 7.9 ≈ 8, so about 4 × 8 = <b>32 L</b>.")
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>To round, find the last digit you keep, then look at the <b>next</b> digit: 5 or more, round up; 4 or less, keep it.</p>"
        "<p>Choose the accuracy that suits the situation: money to the nearest cent, cash to the nearest 5c (Australia has no 1c or 2c coins), "
        "a height to the nearest centimetre. Sometimes the situation decides: 130 people need 3 buses of 50, not 2.6.</p>"
        "<p>To <b>estimate</b>, round each number to its leading digit, then calculate. Use the estimate to check a calculator answer.</p>",
        [("Round 3.8462 to 2 decimal places.", ["Keep 3.84. The next digit is 6, so round up."], "3.85"),
         ("A cash total is $12.37. What is paid?", ["7c rounds to 5c."], "$12.35"),
         ("Estimate 38.7 × 21.4.", ["38.7 ≈ 40 and 21.4 ≈ 20.", "40 × 20 = 800."], "800")],
        ["Cutting off digits instead of rounding: 2.36 to 1 d.p. is 2.4, not 2.3.",
         "Rounding to the wrong place: check which column you keep before you look at the next digit.",
         "Leaving off a final zero: 9.97 to 1 d.p. is 10.0, not 10.",
         "Rounding down when the situation needs rounding up, such as buses or boxes needed."])


def main():
    sets = [S("Rounding to decimal places", collect(one_dp, 15, R) + collect(one_dp_zero, 5, R)),
            S("Rounding to the place asked", collect(one_mixed, 20, R)),
            S("Rounding in real situations", collect(one_ctx, 20, R)),
            S("Estimating calculations", collect(one_est, 20, R)),
            S("Estimation problems", problems())]
    make(7, "rounding-and-estimation", 4, "AC9M7N05",
         "Rounding and Estimation: Decimals, Money and Checking Answers",
         "Year 7 Rounding and Estimation Worksheets: Decimal Places, Rounding Money and Estimating (Free, Answer Key)",
         "Rounding and estimation",
         "round decimals to a given accuracy appropriate to the context and use appropriate rounding and estimation to check "
         "the reasonableness of solutions",
         "Free Year 7 maths worksheets on rounding and estimation for the Australian Curriculum (AC9M7N05): decimal places, "
         "rounding money to the nearest cent and 5c, estimating calculations and checking answers. 100 questions with an answer key.",
         "Look at the next digit: 5 or more, round up.",
         "Estimate by rounding each number to its leading digit: 38.7 × 21.4 ≈ 40 × 20 = 800.",
         body(),
         [("How do I round to 2 decimal places?", "Keep two digits after the point and look at the third: 5 or more rounds up. 3.846 becomes 3.85."),
          ("Why are cash prices rounded to 5c in Australia?", "There are no 1c or 2c coins, so cash totals are rounded to the nearest 5c. Card payments are not rounded."),
          ("Why do we estimate?", "To check that a calculator answer is reasonable. If 38.7 × 21.4 should be about 800, then 8281.8 must be wrong."),
          ("Should I always round to the nearest whole number in word problems?", "No. If you need enough buses or boxes, round up. If only full boxes count, round down.")],
         sets, R)


if __name__ == "__main__":
    main()
