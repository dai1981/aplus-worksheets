# -*- coding: utf-8 -*-
"""
UK Year 9 Maths: Rounding and Error Intervals (KS3 Number)
  python3 tools/gen_uk_maths_y9_rounding_and_error_intervals.py
Rounding to significant figures and decimal places, error intervals for rounded and truncated values,
and upper and lower bounds in simple calculations.
Wrong answers come from real mistakes: dropping the placeholder zeros (45,678 to 2 s.f. as 46), counting
leading zeros as significant, using ≤ at both ends of an error interval, and halving the wrong unit.
"""
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from uk_ks3 import num, B, S, make, lesson, collect, T, ordinal

R = random.Random(91501)
X = "<i>x</i>"
LE, LT = "≤", "&lt;"


def fmt(d):
    """Decimal -> string with commas for the whole part, keeping the decimals as given."""
    d = Decimal(d)
    sign = "−" if d < 0 else ""
    d = abs(d)
    s = format(d, "f")
    if "." in s:
        a, b = s.split(".")
    else:
        a, b = s, ""
    a = "{:,}".format(int(a))
    return sign + a + ("." + b if b else "")


def sf(d, n):
    d = Decimal(d)
    if d == 0:
        return d
    e = d.adjusted()
    q = Decimal(1).scaleb(e - n + 1)
    if e - n + 1 < 0:
        out = d.quantize(q, rounding=ROUND_HALF_UP)
        if out.adjusted() > e:
            out = out.quantize(Decimal(1).scaleb(out.adjusted() - n + 1))
        return out
    return (d / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q


def clean(d):
    """Remove exponent notation, keep trailing zeros that matter for decimals."""
    d = Decimal(d)
    if d == d.to_integral():
        return Decimal(int(d))
    return d


def sfname(n):
    return "%d significant figure%s" % (n, "" if n == 1 else "s")


def pick(right, c):
    out = []
    for x in c:
        if x != right and x not in out:
            out.append(x)
    return out[:3]


# ------------------------------------------------------------ set 1: significant figures, whole and large numbers
def one_sf_big(r):
    digits = r.randint(4, 7)
    v = r.randint(10 ** (digits - 1), 10 ** digits - 1)
    if r.random() < 0.3:
        v = Decimal(v) / Decimal(10 ** r.randint(1, 2))
    n = r.randint(1, 3)
    v = Decimal(v)
    ans = clean(sf(v, n))
    if ans == clean(v):
        return None
    q = "Round %s to %s." % (B(fmt(v)), sfname(n))
    right = fmt(ans)
    lead = str(int(ans))
    sig = lead.rstrip("0") or "0"
    truncd = clean(Decimal(str(v)).quantize(Decimal(1).scaleb(v.adjusted() - n + 1), rounding=ROUND_DOWN)) if v.adjusted() - n + 1 < 0 else clean((v / Decimal(1).scaleb(v.adjusted() - n + 1)).to_integral_value(rounding=ROUND_DOWN) * Decimal(1).scaleb(v.adjusted() - n + 1))
    wr = [fmt(Decimal(sig)) if Decimal(sig) != ans else fmt(ans * 10), fmt(truncd) if truncd != ans else fmt(ans + Decimal(1).scaleb(v.adjusted() - n + 1)),
          fmt(clean(sf(v, n + 1))) if clean(sf(v, n + 1)) != ans else fmt(ans * 10),
          fmt(v.quantize(Decimal(1), rounding=ROUND_HALF_UP)) if v != v.to_integral() else fmt(ans / 10)]
    e = "The %s significant figure is in the %s column. Look at the next digit to decide whether to round up. Keep the place-value zeros: <b>%s</b>." % (
        ordinal(n), place_name(v.adjusted() - n + 1), right)
    return T(q, right, pick(right, wr), e)


def place_name(p):
    return {6: "millions", 5: "hundred thousands", 4: "ten thousands", 3: "thousands", 2: "hundreds", 1: "tens", 0: "ones",
            -1: "tenths", -2: "hundredths", -3: "thousandths", -4: "ten-thousandths", -5: "hundred-thousandths"}[p]


# ------------------------------------------------------------ set 2: small decimals and decimal places
def one_small(r):
    if r.random() < 0.55:
        zeros = r.randint(1, 3)
        body = r.randint(1000, 9999)
        v = Decimal(body) / Decimal(10 ** (4 + zeros))
        n = r.randint(1, 2)
        ans = sf(v, n)
        q = "Round %s to %s." % (B(fmt(v)), sfname(n))
        right = fmt(ans)
        wr = [fmt(v.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)), fmt(sf(v, n + 1)),
              fmt(v.quantize(Decimal(1).scaleb(v.adjusted() - n + 1), rounding=ROUND_DOWN)) if v.quantize(Decimal(1).scaleb(v.adjusted() - n + 1), rounding=ROUND_DOWN) != ans else fmt(ans + Decimal(1).scaleb(v.adjusted() - n + 1)),
              fmt(ans * 10)]
        e = "Leading zeros are not significant. The first significant figure is %s, in the %s. <b>%s</b>." % (
            str(body)[0], place_name(v.adjusted()), right)
        return T(q, right, pick(right, wr), e)
    v = Decimal(r.randint(10000, 999999)) / Decimal(10 ** r.randint(3, 4))
    n = r.randint(1, 3)
    ans = v.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)
    if ans == v:
        return None
    q = "Round %s to %d decimal place%s." % (B(fmt(v)), n, "" if n == 1 else "s")
    right = fmt(ans)
    wr = [fmt(v.quantize(Decimal(1).scaleb(-n), rounding=ROUND_DOWN)) if v.quantize(Decimal(1).scaleb(-n), rounding=ROUND_DOWN) != ans else fmt(ans + Decimal(1).scaleb(-n)),
          fmt(sf(v, n)), fmt(v.quantize(Decimal(1).scaleb(-n - 1), rounding=ROUND_HALF_UP)), fmt(ans - Decimal(1).scaleb(-n))]
    e = "Keep %d digit%s after the decimal point and look at the next digit: <b>%s</b>." % (n, "" if n == 1 else "s", right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 3: error intervals for whole-number rounding
def one_ei(r):
    unit = r.choice([1, 10, 100, 1000, 5])
    names = {1: "the nearest whole number", 10: "the nearest 10", 100: "the nearest 100", 1000: "the nearest 1,000", 5: "the nearest 5"}
    v = unit * r.randint(3, 90 if unit < 1000 else 60)
    half = Decimal(unit) / 2
    lo, hi = Decimal(v) - half, Decimal(v) + half
    ctx = r.choice(["A number %s" % X, "The length %s cm" % X, "The mass %s g" % X])
    q = "%s is rounded to %s. The result is %s. What is the error interval for %s?" % (ctx, names[unit], fmt(v), X)
    right = "%s %s %s %s %s" % (fmt(lo), LE, X, LT, fmt(hi))
    wr = ["%s %s %s %s %s" % (fmt(lo), LE, X, LE, fmt(hi)), "%s %s %s %s %s" % (fmt(v - unit), LE, X, LT, fmt(v + unit)),
          "%s %s %s %s %s" % (fmt(Decimal(v) - half / 10 if unit == 1 else Decimal(v) - unit / Decimal(20) if unit >= 10 else Decimal(v) - Decimal("0.05")), LE, X, LT, fmt(Decimal(v) + (half / 10 if unit == 1 else unit / Decimal(20) if unit >= 10 else Decimal("0.05")))),
          "%s %s %s %s %s" % (fmt(lo), LT, X, LE, fmt(hi))]
    e = "Half of %s is %s. The lower bound is %s − %s and the upper bound is %s + %s. The upper bound itself would round up, so use %s: <b>%s</b>." % (
        fmt(unit), fmt(half), fmt(v), fmt(half), fmt(v), fmt(half), LT, right)
    return T(q, right, pick(right, wr), e)


# ------------------------------------------------------------ set 4: decimals, significant figures and truncation
def one_ei2(r):
    k = r.randint(0, 2)
    if k == 0:
        dp = r.randint(1, 2)
        v = Decimal(r.randint(11, 999)) / Decimal(10 ** dp)
        half = Decimal(5) / Decimal(10 ** (dp + 1))
        q = "%s = %s, correct to %d decimal place%s. What is the error interval for %s?" % (X, fmt(v), dp, "" if dp == 1 else "s", X)
        lo, hi = v - half, v + half
        right = "%s %s %s %s %s" % (fmt(lo), LE, X, LT, fmt(hi))
        step = Decimal(1) / Decimal(10 ** dp)
        wr = ["%s %s %s %s %s" % (fmt(v - step), LE, X, LT, fmt(v + step)), "%s %s %s %s %s" % (fmt(lo), LE, X, LE, fmt(hi)),
              "%s %s %s %s %s" % (fmt(v), LE, X, LT, fmt(v + step))]
        e = "Half of %s is %s. <b>%s</b>." % (fmt(step), fmt(half), right)
        return T(q, right, wr, e)
    if k == 1:
        n = r.randint(1, 2)
        v = Decimal(r.randint(1, 9) * 10 ** (n - 1) + r.randint(0, 10 ** (n - 1) - 1) if n > 1 else r.randint(1, 9)) * Decimal(10) ** r.randint(1, 3)
        v = sf(v, n)
        unit = Decimal(1).scaleb(v.adjusted() - n + 1)
        half = unit / 2
        q = "%s = %s, correct to %s. What is the error interval for %s?" % (X, fmt(clean(v)), sfname(n), X)
        right = "%s %s %s %s %s" % (fmt(clean(v - half)), LE, X, LT, fmt(clean(v + half)))
        wr = ["%s %s %s %s %s" % (fmt(clean(v - unit)), LE, X, LT, fmt(clean(v + unit))), "%s %s %s %s %s" % (fmt(clean(v - half)), LE, X, LE, fmt(clean(v + half))),
              "%s %s %s %s %s" % (fmt(clean(v - Decimal("0.5"))), LE, X, LT, fmt(clean(v + Decimal("0.5"))))]
        e = "To %s, %s is rounded to the nearest %s. Half of that is %s: <b>%s</b>." % (sfname(n), fmt(clean(v)), fmt(clean(unit)), fmt(clean(half)), right)
        return T(q, right, pick(right, wr), e)
    dp = r.randint(0, 1)
    if dp == 0:
        v = Decimal(r.randint(3, 99))
        q = "%s is truncated to a whole number. The result is %s. What is the error interval for %s?" % (X, fmt(v), X)
        step = Decimal(1)
    else:
        v = Decimal(r.randint(11, 199)) / 10
        q = "%s is truncated to 1 decimal place. The result is %s. What is the error interval for %s?" % (X, fmt(v), X)
        step = Decimal("0.1")
    right = "%s %s %s %s %s" % (fmt(v), LE, X, LT, fmt(v + step))
    wr = ["%s %s %s %s %s" % (fmt(v - step / 2), LE, X, LT, fmt(v + step / 2)), "%s %s %s %s %s" % (fmt(v - step), LT, X, LE, fmt(v)),
          "%s %s %s %s %s" % (fmt(v), LE, X, LE, fmt(v + step))]
    e = "Truncating chops off digits without rounding, so %s is at least %s and less than %s: <b>%s</b>." % (X, fmt(v), fmt(v + step), right)
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A rope is 12 m long, to the nearest metre. What is the shortest it could be?", "11.5 m", ["11 m", "11.9 m", "11.95 m"],
         "Half of 1 m is 0.5 m, so the lower bound is 12 − 0.5 = <b>11.5 m</b>."),
        ("A square has side 6 cm, to the nearest cm. What is the upper bound of its perimeter?", "26 cm", ["24 cm", "28 cm", "25 cm"],
         "The side is less than 6.5 cm, so the perimeter is less than 4 × 6.5 = <b>26 cm</b>."),
        ("A square has side 6 cm, to the nearest cm. What is the lower bound of its area?", "30.25 cm²", ["36 cm²", "30 cm²", "25 cm²"],
         "The side is at least 5.5 cm: 5.5² = <b>30.25 cm²</b>."),
        ("A lift can carry 600 kg. Eight people each weigh 75 kg, to the nearest kg. What is the greatest total mass they could have?", "604 kg", ["600 kg", "608 kg", "596 kg"],
         "Upper bound of each: 75.5 kg. 8 × 75.5 = <b>604 kg</b>, so the lift might be overloaded."),
        ("Estimate 4.87 × 21.3 by rounding each number to 1 significant figure.", "100", ["84", "103.7", "80"],
         "5 × 20 = <b>100</b>."),
        ("Estimate 598 ÷ 0.31 by rounding each number to 1 significant figure.", "2,000", ["200", "1,800", "180"],
         "600 ÷ 0.3 = <b>2,000</b>."),
        ("Estimate <span class='fr'><span class='fn'>39.8 × 5.1</span><span class='fd'>0.49</span></span> by rounding to 1 significant figure.", "400", ["40", "200", "4,000"],
         "40 × 5 = 200, and 200 ÷ 0.5 = <b>400</b>."),
        ("How many significant figures does 0.00720 have?", "3", ["6", "2", "5"],
         "Leading zeros do not count; the trailing zero after 72 does: 7, 2, 0 is <b>3</b>."),
        ("What is 0.04962 rounded to 2 significant figures?", "0.050", ["0.05", "0.049", "0.04"],
         "The first two significant figures are 4 and 9; the next digit is 6, so 49 rounds up to 50: <b>0.050</b>. Keep the final zero to show 2 s.f."),
        ("The population of a town is 45,000 to 2 significant figures. What is the smallest it could be?", "44,500", ["44,000", "44,999", "40,000"],
         "To 2 s.f. it is rounded to the nearest 1,000. Half is 500: 45,000 − 500 = <b>44,500</b>."),
        ("A car travels 100 km, to the nearest km, in 2 hours, to the nearest hour. What is the upper bound of its average speed?", "67 km/h (to the nearest whole number)", ["50 km/h (to the nearest whole number)", "40 km/h (to the nearest whole number)", "60 km/h (to the nearest whole number)"],
         "Greatest speed = greatest distance ÷ least time = 100.5 ÷ 1.5 = <b>67 km/h</b>. Using 99.5 ÷ 2.5 gives the least speed, about 40 km/h."),
        ("A shelf is 80 cm long, to the nearest cm. Books are 4 cm thick, to the nearest mm. Can 20 books always fit?", "No, the books could be up to 81 cm in total", ["Yes, 20 × 4 = 80", "Yes, always", "No, never"],
         "Shelf could be 79.5 cm. Books could be 4.05 cm each: 20 × 4.05 = 81 cm. <b>No</b>, they might not fit."),
        ("Which is the error interval for a number that rounds to 3.6 to 1 decimal place?", "3.55 ≤ <i>x</i> &lt; 3.65", ["3.5 ≤ <i>x</i> &lt; 3.7", "3.55 ≤ <i>x</i> ≤ 3.65", "3.6 ≤ <i>x</i> &lt; 3.7"],
         "Half of 0.1 is 0.05: <b>3.55 ≤ <i>x</i> &lt; 3.65</b>."),
        ("Why is the upper bound written with &lt; and not ≤?", "Because the upper bound itself would round up", ["Because it is bigger", "It is just a convention with no reason", "Because the lower bound uses &lt; too"],
         "For example 6.5 rounds to 7, not 6, so 6.5 is not included: <b>because the upper bound itself would round up</b>."),
        ("A rectangle is 8 cm by 5 cm, both to the nearest cm. What is the lower bound of its area?", "33.75 cm²", ["40 cm²", "35 cm²", "30 cm²"],
         "7.5 × 4.5 = <b>33.75 cm²</b>."),
        ("Round 299,700 to 2 significant figures.", "300,000", ["30", "290,000", "299,000"],
         "The first two figures are 2 and 9; the next is 9, so 29 rounds up to 30, then add the zeros: <b>300,000</b>."),
        ("A time of 9.8 seconds is truncated to 1 decimal place. What is the greatest the real time could be?", "Just under 9.9 seconds", ["9.85 seconds", "9.8 seconds exactly", "10 seconds"],
         "Truncating means it is at least 9.8 and less than 9.9: <b>just under 9.9 seconds</b>."),
        ("Leo rounds 0.0306 to 1 significant figure and writes 0. What should the answer be?", "0.03", ["0.031", "0.04", "0.3"],
         "The first significant figure is 3 (in the hundredths). <b>0.03</b>."),
        ("A bag holds 25 kg to the nearest kg. How many bags of 25 kg are needed for a load of exactly 500 kg, in the worst case?", "21", ["20", "19", "22"],
         "The least a bag might hold is 24.5 kg. 500 ÷ 24.5 = 20.4…, so in the worst case <b>21</b> bags are needed."),
        ("Which number is 7,850 rounded to 2 significant figures?", "7,900", ["7,800", "79", "8,000"],
         "The first two figures are 7 and 8; the next is 5, so round up: <b>7,900</b>."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p><b>Significant figures</b> start at the first non-zero digit. To round, look at the next digit: 5 or more rounds up. "
        "Keep the place-value zeros: 45,678 to 2 s.f. is 46,000, not 46. Leading zeros in a decimal are not significant: 0.00456 to 2 s.f. is 0.0046.</p>"
        "<p>An <b>error interval</b> shows all the values that round to a given number. If <i>x</i> rounds to 70 to the nearest 10, "
        "add and subtract half of 10: 65 ≤ <i>x</i> &lt; 75. If a number is <b>truncated</b>, digits are chopped off, so 3.7 truncated "
        "to 1 d.p. gives 3.7 ≤ <i>x</i> &lt; 3.8.</p>",
        [("Round 0.06372 to 2 s.f.", ["The first significant figure is 6; the next digit after 63 is 7."], "0.064"),
         ("<i>x</i> = 400 to the nearest 100.", ["Half of 100 is 50."], "350 ≤ <i>x</i> &lt; 450"),
         ("<i>x</i> = 2.4 to 1 d.p.", ["Half of 0.1 is 0.05."], "2.35 ≤ <i>x</i> &lt; 2.45")],
        ["Dropping the zeros when rounding a large number: 3,847 to 1 s.f. is 4,000, not 4.",
         "Counting leading zeros as significant figures.",
         "Writing ≤ at both ends of an error interval. The upper bound uses &lt;.",
         "Using the full unit instead of half of it: 70 to the nearest 10 is not 60 ≤ <i>x</i> &lt; 80."])


def main():
    sets = [S("Significant figures", collect(one_sf_big, 20, R)),
            S("Small decimals and decimal places", collect(one_small, 20, R)),
            S("Error intervals", collect(one_ei, 20, R)),
            S("Error intervals with decimals and truncation", collect(one_ei2, 20, R)),
            S("Bounds and estimation problems", problems())]
    make(9, "rounding-and-error-intervals", 15, "N",
         "Rounding and Error Intervals",
         "Year 9 Rounding Worksheets: Significant Figures, Error Intervals, Truncation and Bounds",
         "Error Intervals",
         "Round numbers and measures to an appropriate degree of accuracy (for example, to a number of decimal places or "
         "significant figures); use inequality notation to specify simple error intervals due to truncation or rounding.",
         "Free Year 9 rounding worksheets: significant figures, decimal places, error intervals for rounding and truncation, "
         "upper and lower bounds, and estimation. 100 questions with answers.",
         "For an error interval, add and subtract half of the unit you rounded to.",
         "The lower bound uses ≤ and the upper bound uses <.",
         body(),
         [("What are significant figures?", "The digits of a number starting from the first non-zero digit. 0.0305 has 3 significant figures: 3, 0 and 5."),
          ("What is an error interval?", "The range of values a number could have been before it was rounded or truncated, written with inequalities such as 65 ≤ x < 75."),
          ("How do I find an error interval for rounding?", "Halve the unit you rounded to. Subtract it for the lower bound and add it for the upper bound."),
          ("What is the difference between rounding and truncating?", "Rounding goes to the nearest value. Truncating just chops off digits, so 3.79 truncated to 1 d.p. is 3.7.")],
         sets, R)


if __name__ == "__main__":
    main()
