# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Place Value and Ordering (KS3 Number)
  python3 tools/gen_uk_maths_y7_place_value_and_ordering.py
Value of a digit in integers and decimals, multiplying and dividing by 10, 100 and 1,000,
ordering decimals and negative numbers, and the symbols < and >.
Wrong answers come from real mistakes: reading the digit instead of its value, moving the digits the
wrong number of places, thinking a longer decimal is bigger, and ordering negatives by size of the digits.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, People, T, table, MINUS

R = random.Random(70101)
P = People(R)
PLACES = [(F(10000), "ten thousands"), (F(1000), "thousands"), (F(100), "hundreds"), (F(10), "tens"), (F(1), "ones"),
          (F(1, 10), "tenths"), (F(1, 100), "hundredths"), (F(1, 1000), "thousandths")]


def show_bold(digits, k, n_int):
    """digits: list over PLACES window; bold digit k. n_int: how many are before the point."""
    s = ""
    ip = "".join(str(d) for d in digits[:n_int])
    fp = "".join(str(d) for d in digits[n_int:])
    # commas for the integer part
    parts = []
    for i, ch in enumerate(ip):
        if i and (len(ip) - i) % 3 == 0:
            parts.append(",")
        parts.append(("<b><u>%s</u></b>" % ch) if i == k else ch)
    s = "".join(parts)
    if fp:
        s += "." + "".join(("<b><u>%s</u></b>" % ch) if n_int + i == k else ch for i, ch in enumerate(fp))
    return s


# ------------------------------------------------------------ set 1: value of a digit
def one_digit(r):
    n_int = r.choice([2, 3, 4, 5])
    n_dec = r.choice([1, 2, 3]) if n_int < 5 else r.choice([1, 2])
    ds = r.sample(range(1, 10), n_int + n_dec)
    window = PLACES[5 - n_int: 5 + n_dec]
    k = r.randrange(n_int + n_dec)
    d = ds[k]
    if d == 1:
        return None
    val = d * window[k][0]
    q = "What is the value of the underlined digit in %s?" % B(show_bold(ds, k, n_int))
    wrong = [F(d), val * 10, val / 10, val / 100 if val < 1 else val * 100]
    e = "The %s is in the <b>%s</b> column, so it is worth %s × %s = <b>%s</b>." % (
        d, window[k][1], d, num(window[k][0]), num(val))
    return mcq(q, (num(val), val), [(num(w), w) for w in wrong if w != val], e)


# ------------------------------------------------------------ set 2: × and ÷ by 10, 100, 1000
def one_scale(r):
    x = F(r.choice([347, 52, 6081, 905, 1264, 78, 4003, 39]), r.choice([1, 10, 100, 1000]))
    if x < F(1, 100) or x > 5000:
        return None
    p = r.choice([10, 100, 1000])
    mult = r.random() < 0.5
    ans = x * p if mult else x / p
    if ans.denominator > 10000 or ans > 100000:
        return None
    zeros = len(str(p)) - 1
    q = "Work out %s." % B("%s %s %s" % (num(x), "×" if mult else "÷", num(p)))
    other = [x * p / 10, x * p * 10, x / p] if mult else [x / p * 10, x / p / 10, x * p]
    e = ("%s by %s moves every digit %d place%s to the %s." % ("Multiplying" if mult else "Dividing", num(p), zeros,
         "" if zeros == 1 else "s", "left (the number gets bigger)" if mult else "right (the number gets smaller)")
         + " The answer is <b>%s</b>." % num(ans))
    cands = [(num(w), w) for w in other if w != ans and num(w)]
    return mcq(q, (num(ans), ans), cands, e)


# ------------------------------------------------------------ set 3: ordering decimals
def one_order(r):
    base = r.choice([0, 0, 1, 2, 3])
    a = F(base) + F(r.randint(1, 9), 10)
    vals = {a, F(base) + F(r.randint(10, 99), 100), F(base) + F(r.randint(100, 999), 1000), F(base) + F(r.randint(1, 9), 100)}
    vals = sorted(vals)
    if len(vals) < 4:
        return None
    kind = r.choice(["largest", "smallest", "largest"])
    ans = vals[-1] if kind == "largest" else vals[0]
    longest = max(vals, key=lambda v: len(num(v)))
    if longest == ans:
        return None
    q = "Which number is the %s?" % B(kind)
    e = ("Line up the decimal points and compare the tenths first, then the hundredths. "
         "In order: %s. The %s is <b>%s</b>. More digits does not mean bigger." % (", ".join(num(v) for v in vals), kind, num(ans)))
    return mcq(q, (num(ans), ans), [(num(w), w) for w in vals if w != ans], e)


def one_order_list(r):
    whole = r.randint(0, 4)
    vals = set()
    while len(vals) < 4:
        dp = r.choice([1, 2, 3])
        vals.add(F(whole) + F(r.randint(1, 10 ** dp - 1), 10 ** dp))
    vals = sorted(vals)
    if all(len(num(a)) == len(num(b)) for a in vals for b in vals):
        return None
    right = ", ".join(num(v) for v in vals)
    by_len = sorted(vals, key=lambda v: (len(num(v)), v))
    rev = ", ".join(num(v) for v in reversed(vals))
    swap = vals[:]
    swap[1], swap[2] = swap[2], swap[1]
    wr = [", ".join(num(v) for v in by_len), rev, ", ".join(num(v) for v in swap)]
    wr = [w for w in wr if w != right]
    if len(set(wr)) < 3:
        return None
    shuffled = vals[:]
    r.shuffle(shuffled)
    q = "Put these numbers in order, %s first: %s" % (B("smallest"), ", ".join(num(v) for v in shuffled))
    e = "Compare the tenths, then hundredths, then thousandths (write 0s to make them the same length if it helps). Order: <b>%s</b>." % right
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 4: negatives and < >
def stmt(a, b, sym):
    return "%s %s %s" % (num(a), sym, num(b))


def true_sym(a, b):
    return "&lt;" if a < b else "&gt;"


def false_sym(a, b):
    return "&gt;" if a < b else "&lt;"


def one_ineq(r):
    pairs = []
    while len(pairs) < 4:
        kind = r.choice(["nn", "nn", "nd", "pn", "dd"])
        if kind == "nn":
            a, b = -r.randint(1, 15), -r.randint(1, 15)
        elif kind == "nd":
            a, b = -F(r.randint(11, 99), 10), -F(r.randint(11, 99), 10)
        elif kind == "pn":
            a, b = r.randint(1, 9), -r.randint(10, 30)
        else:
            a, b = F(r.randint(1, 9), 10), F(r.randint(10, 99), 100)
        if a == b or abs(a - b) > 20:
            continue
        pairs.append((F(a), F(b)))
    right = stmt(pairs[0][0], pairs[0][1], true_sym(*pairs[0]))
    wr = [stmt(a, b, false_sym(a, b)) for a, b in pairs[1:]]
    q = "Which statement is %s?" % B("true")
    a, b = pairs[0]
    e = "On a number line, %s is to the %s of %s, so <b>%s</b>." % (num(a), "left" if a < b else "right", num(b), right)
    if a < 0 and b < 0:
        e += " With negative numbers, the one further from zero is smaller."
    if len(set(wr)) < 3:
        return None
    return T(q, right, wr, e)


def one_neg_order(r):
    vals = sorted(set(F(x) for x in r.sample(range(-12, 9), 5)))
    if not any(v < 0 for v in vals[:2]):
        return None
    if r.random() < 0.5:
        vals = [v if v.denominator == 1 and r.random() < 0.6 else v - F(5, 10) for v in vals]
        vals = sorted(set(vals))
    if len(vals) < 4:
        return None
    vals = vals[:4] if len(vals) > 4 else vals
    right = ", ".join(num(v) for v in vals)
    by_abs = sorted(vals, key=lambda v: (abs(v), v))
    rev = ", ".join(num(v) for v in reversed(vals))
    neg_wrong = sorted([v for v in vals if v < 0], reverse=True) + sorted([v for v in vals if v >= 0])
    wr = [", ".join(num(v) for v in by_abs), rev, ", ".join(num(v) for v in neg_wrong)]
    wr = [w for w in wr if w != right]
    if len(set(wr)) < 3:
        return None
    sh = vals[:]
    r.shuffle(sh)
    q = "Order from %s to %s: %s" % (B("smallest"), B("largest"), ", ".join(num(v) for v in sh))
    e = "Negative numbers come first, and the one furthest from zero is the smallest. Order: <b>%s</b>." % right
    return T(q, right, wr, e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    # coldest / warmest
    for city_t in [(["Leeds", "Oslo", "Moscow", "Paris"], [-3, -8, -15, 2]),
                   (["Glasgow", "Helsinki", "Rome", "Warsaw"], [1, -11, 9, -6]),
                   (["Aberdeen", "Reykjavik", "Berlin", "Madrid"], [-2, -5, -1, 7])]:
        names, ts = city_t
        lo = min(ts)
        q = "At midnight the temperatures were: %s. Which city was the %s?" % (
            ", ".join("%s %s °C" % (n, num(t)) for n, t in zip(names, ts)), B("coldest"))
        right = names[ts.index(lo)]
        e = "The coldest is the lowest temperature. %s °C is the smallest number, so <b>%s</b>." % (num(lo), right)
        its.append(T(q, right, [n for n in names if n != right], e))
    for names, ts in [(["Cardiff", "Moscow", "Dublin", "Montreal"], [-1, -9, 3, -12]),
                      (["York", "Stockholm", "Lisbon", "Toronto"], [-4, -7, 11, -13])]:
        q = "Temperatures: %s. Which city was the %s?" % (", ".join("%s %s °C" % (n, num(t)) for n, t in zip(names, ts)),
                                                          B("warmest"))
        right = names[ts.index(max(ts))]
        e = "The warmest is the highest temperature: <b>%s</b>." % right
        its.append(T(q, right, [n for n in names if n != right], e))
    # race times: fastest is smallest
    for times in [[12.45, 12.5, 12.405, 12.54], [9.8, 9.75, 9.805, 9.708], [58.3, 58.29, 58.03, 58.309]]:
        n, _, _ = P.next()
        ppl = [P.next()[0] for _ in range(4)]
        tv = [F(str(t)) for t in times]
        best = min(tv)
        q = "In a race the times in seconds were: %s. Who was %s?" % (
            ", ".join("%s %s s" % (p, num(t)) for p, t in zip(ppl, tv)), B("fastest"))
        right = ppl[tv.index(best)]
        e = "The fastest runner has the smallest time. %s is the smallest, so <b>%s</b>." % (num(best), right)
        its.append(T(q, right, [p for p in ppl if p != right], e))
    # heights in metres
    for hs in [[1.6, 1.58, 1.625, 1.065], [1.42, 1.4, 1.408, 1.39]]:
        ppl = [P.next()[0] for _ in range(4)]
        hv = [F(str(h)) for h in hs]
        q = "Heights: %s. Who is the %s?" % (", ".join("%s %s m" % (p, num(h)) for p, h in zip(ppl, hv)), B("tallest"))
        right = ppl[hv.index(max(hv))]
        e = "Compare tenths, then hundredths: %s m is the greatest, so <b>%s</b>." % (num(max(hv)), right)
        its.append(T(q, right, [p for p in ppl if p != right], e))
    # bank balance
    for bal, ch in [(-25, 40), (-60, 15), (30, -45), (-12, -20)]:
        nb = bal + ch
        name, he, his = P.next()
        q = "%s's bank balance is %s£%d. %s %s £%d. What is %s balance now?" % (
            name, MINUS if bal < 0 else "", abs(bal), cap(he), "pays in" if ch > 0 else "spends", abs(ch), his)
        f = lambda v: (MINUS if v < 0 else "") + "£%d" % abs(v)
        wr = [bal - ch, -nb if nb else None, abs(bal) + abs(ch)]
        e = "%s %s %d = <b>%s</b>." % (num(bal), "+" if ch > 0 else MINUS, abs(ch), f(nb))
        its.append(mcq(q, (f(nb), nb), [(f(w), w) for w in wr if w is not None and w != nb] + [(f(nb + 10), nb + 10)], e))
    # scale x10
    for item, each, n in [("pencil", F("0.35"), 100), ("stamp", F("0.85"), 1000), ("ticket", F("12.5"), 10),
                          ("book", F("6.99"), 100), ("badge", F("1.2"), 1000), ("rubber", F("0.4"), 10)]:
        tot = each * n
        q = "One %s costs %s. How much do %s %ss cost?" % (item, gbp(each), num(n), item)
        wr = [tot / 10, tot * 10, tot / 100, tot * 100]
        e = "Multiply by %s: move the digits %d places left. %s × %s = <b>%s</b>." % (num(n), len(str(n)) - 1, gbp(each), num(n), gbp(tot))
        its.append(mcq(q, (gbp(tot), tot), [(gbp(w), w) for w in wr if w != tot], e))
    return its


def cap(s):
    return s[0].upper() + s[1:]


def gbp(v):
    from uk_ks3 import gbp as g
    return g(v)


def body():
    return lesson(
        "<p>Each column is worth 10 times the column to its right. After the decimal point come tenths, hundredths and thousandths.</p>"
        + table(["Thousands", "Hundreds", "Tens", "Ones", ".", "Tenths", "Hundredths", "Thousandths"],
                [["4", "3", "7", "2", ".", "6", "0", "5"]])
        + "<p>In 4,372.605 the 6 is worth 0.6 and the 5 is worth 0.005.</p>"
        "<p>To compare decimals, line up the decimal points and compare from the left. On a number line, numbers get "
        "smaller as you go left, so −8 &lt; −3.</p>",
        [("Order 0.6, 0.45, 0.508 and 0.09 from smallest to largest.",
          ["Write them with the same number of decimal places: 0.600, 0.450, 0.508, 0.090.",
           "Compare: 0.090 &lt; 0.450 &lt; 0.508 &lt; 0.600."], "0.09, 0.45, 0.508, 0.6"),
         ("Work out 3.47 × 100.", ["× 100 moves every digit 2 places to the left."], "347"),
         ("Which is smaller, −7 or −3?", ["−7 is further left on the number line."], "−7")],
        ["Thinking 0.508 is bigger than 0.6 because it has more digits.",
         "Moving the decimal point the wrong way: 34.7 ÷ 10 is 3.47, not 347.",
         "Saying −7 is bigger than −3 because 7 is bigger than 3.",
         "Giving the digit instead of its value: in 5.07 the 7 is worth 0.07, not 7."])


def main():
    sets = [S("Value of a digit", collect(one_digit, 20, R)),
            S("Multiply and divide by 10, 100 and 1,000", collect(one_scale, 20, R)),
            S("Ordering decimals", collect(one_order, 10, R) + collect(one_order_list, 10, R)),
            S("Negative numbers, < and >", collect(one_ineq, 12, R) + collect(one_neg_order, 8, R)),
            S("Problems in context", problems())]
    make(7, "place-value-and-ordering", 1, "N",
         "Place Value and Ordering: Decimals and Negative Numbers",
         "Year 7 Place Value Worksheets: Decimals, Negative Numbers, × and ÷ by 10, 100, 1,000 and Ordering",
         "Place value and ordering",
         "Understand and use place value for decimals, measures and integers of any size; order positive and negative "
         "integers, decimals and fractions; use the number line as a model for ordering of the real numbers; use the "
         "symbols =, ≠, <, >, ≤, ≥.",
         "Free Year 7 maths worksheets on place value and ordering: the value of digits in decimals, multiplying and dividing "
         "by 10, 100 and 1,000, ordering decimals and negative numbers, and using < and >. 100 questions with answers.",
         "Line up the decimal points and compare from the left: 0.6 is bigger than 0.508.",
         "On the number line, left is smaller: −7 < −3. Multiplying by 10 moves digits one place left.",
         body(),
         [("How do you order decimals?", "Line up the decimal points, fill gaps with zeros so they have the same number of decimal places, then compare digit by digit from the left."),
          ("Which is bigger, −5 or −2?", "−2 is bigger. It is closer to zero and further right on the number line."),
          ("What happens when you multiply by 100?", "Every digit moves two places to the left, so 3.47 × 100 = 347."),
          ("What does the symbol < mean?", "It means “is less than”. The small end points to the smaller number: 3 < 8.")],
         sets, R)


if __name__ == "__main__":
    main()
