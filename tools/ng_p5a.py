# -*- coding: utf-8 -*-
"""
Nigeria Primary 5–6 Mathematics: question makers written for Nigeria (naira, Nigerian names, British spelling).
Each maker takes a random.Random and returns one item (ng_common.mcq); AssertionError means "draw again".
Binary numbers are written 1011₂ (the subscript keeps add_commas away).
"""
import math
from collections import Counter
from fractions import Fraction as F
from ng_common import mcq, comma, naira, fig, fr, Kid, PLACES, svg_wrap, text, GREEN, FILL, INK, RED, BLUE
from ng_p4a import K, ch, dec, frac

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def b2(n):
    return bin(n)[2:] + "₂"


def bs(n, base):
    d = []
    while n:
        d.append(str(n % base))
        n //= base
    return "".join(reversed(d or ["0"])) + str(base).translate(SUB)


# ============================================================ binary numbers
def bin_to(r):
    n = r.randint(5, 63)
    s = bin(n)[2:]
    w = [n + 1, n - 1, int(s[::-1], 2) if s[::-1] != s else n + 2, n * 2, sum(int(c) for c in s), n + 2]
    terms = " + ".join("%s × %d" % (c, 2 ** i) for i, c in reversed(list(enumerate(reversed(s)))))
    return mcq("Change %s to a base ten number." % b2(n), n, [x for x in w if x != n],
               "Multiply each digit by its place value (1, 2, 4, 8, 16, 32): %s = <b>%d</b>." % (terms, n))


def bin_from(r):
    n = r.randint(5, 63)
    s = bin(n)
    w = [b2(n + 1), b2(n - 1), bin(n)[2:][::-1] + "₂" if bin(n)[2:][::-1] != bin(n)[2:] else b2(n + 2), b2(n * 2), b2(n // 2)]
    steps = []
    m = n
    while m:
        steps.append("%d ÷ 2 = %d remainder %d" % (m, m // 2, m % 2))
        m //= 2
    return mcq("Change %d to a binary number (base two)." % n, b2(n), [x for x in w if x != b2(n)],
               "Divide by 2 again and again: %s. Read the remainders from the bottom up: <b>%s</b>." % ("; ".join(steps), b2(n)))


def bin_add(r):
    a, b = r.randint(3, 31), r.randint(3, 31)
    s = a + b
    w = [b2(s + 1), b2(s - 1), bin(a | b)[2:] + "₂" if (a | b) != s else b2(s + 2), b2(s * 2) if s < 32 else b2(s - 2)]
    return mcq("Add in base two: %s + %s" % (b2(a), b2(b)), b2(s), [x for x in w if x != b2(s)],
               "In base two, 1 + 1 = 10₂ (write 0, carry 1). Check: %d + %d = %d, and %d = <b>%s</b>." % (a, b, s, s, b2(s)))


def bin_sub(r):
    a = r.randint(9, 63)
    b = r.randint(2, a - 2)
    d = a - b
    w = [b2(d + 1), b2(d - 1) if d > 1 else b2(d + 3), bin(a ^ b)[2:] + "₂" if (a ^ b) != d else b2(d + 2), b2(d + 2)]
    return mcq("Subtract in base two: %s − %s" % (b2(a), b2(b)), b2(d), [x for x in w if x != b2(d)],
               "Borrow 2 (not 10) from the next place. Check: %d − %d = %d, and %d = <b>%s</b>." % (a, b, d, d, b2(d)))


def bin_place(r):
    k = r.randint(2, 6)
    w = [10 ** k, 2 * k, k, 2 ** (k + 1), 2 ** (k - 1)]
    names = {2: "third", 3: "fourth", 4: "fifth", 5: "sixth", 6: "seventh"}
    return mcq("In a binary number, what is the place value of the %s digit from the right?" % names[k], 2 ** k, [x for x in w if x != 2 ** k],
               "Binary place values double each time: 1, 2, 4, 8, 16, 32, 64. The %s place is <b>%d</b>." % (names[k], 2 ** k))


def bin_compare(r):
    a, b = r.sample(range(5, 64), 2)
    big = max(a, b)
    return mcq("Which is greater: %s or %s? Give the base ten value of the greater number." % (b2(a), b2(b)), big, [min(a, b), big + 1, big * 2, big - 1],
               "%s = %d and %s = %d. The greater is <b>%d</b>." % (b2(a), a, b2(b), b, big))


def bin_life(r):
    k = K(r)
    n = r.randint(6, 30)
    thing = ch(r, ["bulbs", "switches", "lamps"])
    s = bin(n)[2:]
    return mcq("%s uses a row of %s to show numbers in binary: on = 1, off = 0. The row reads %s. Which number is this?" % (k["n"], thing, " ".join("on" if c == "1" else "off" for c in s)),
               n, [n + 1, n - 1, len(s), s.count("1"), n + 2],
               "on/off gives %s. %s = <b>%d</b>." % (b2(n), b2(n), n))


# ============================================================ other bases (Primary 6)
def base_to(r):
    base = ch(r, [3, 4, 5, 8])
    n = r.randint(base + 1, base ** 3 - 1)
    s = bs(n, base)
    digits = s[:-1]
    w = [n + 1, n - 1, n + 2, int(digits, base) + base, sum(int(c) for c in digits) * base]
    terms = " + ".join("%s × %d" % (c, base ** i) for i, c in reversed(list(enumerate(reversed(digits)))))
    return mcq("Change %s to base ten." % s, n, [x for x in w if x != n], "%s = <b>%d</b>." % (terms, n))


def base_from(r):
    base = ch(r, [3, 4, 5, 8])
    n = r.randint(base + 1, base ** 3 - 1)
    s = bs(n, base)
    w = [bs(n + 1, base), bs(n - 1, base), s[:-1][::-1] + str(base).translate(SUB) if s[:-1][::-1] != s[:-1] else bs(n + 2, base), bs(n, base + 1) if base < 8 else bs(n + base, base)]
    steps = []
    m = n
    while m:
        steps.append("%d ÷ %d = %d r %d" % (m, base, m // base, m % base))
        m //= base
    return mcq("Change %d to base %d." % (n, base), s, [x for x in w if x != s],
               "Divide by %d again and again: %s. Read the remainders upwards: <b>%s</b>." % (base, "; ".join(steps), s))


# ============================================================ temperature
def thermo_svg(t, lo=0, hi=50, step=10):
    H = 260
    y = lambda v: 220 - (v - lo) * 190.0 / (hi - lo)
    b = "<rect x='60' y='20' width='24' height='205' rx='12' fill='#fff' stroke='%s' stroke-width='2'/>" % INK
    b += "<circle cx='72' cy='232' r='20' fill='%s' stroke='%s' stroke-width='2'/>" % (RED, INK)
    b += "<rect x='66' y='%.1f' width='12' height='%.1f' fill='%s'/>" % (y(t), 232 - y(t), RED)
    v = lo
    while v <= hi:
        b += "<line x1='84' y1='%.1f' x2='98' y2='%.1f' stroke='%s' stroke-width='2'/>" % (y(v), y(v), INK) + text(124, y(v) + 5, "%d" % v, 14)
        v += step
    v = lo
    while v <= hi:
        b += "<line x1='84' y1='%.1f' x2='91' y2='%.1f' stroke='%s' stroke-width='1'/>" % (y(v), y(v), INK)
        v += step / 5
    b += text(124, 14, "°C", 14)
    return svg_wrap(170, H, b, "thermometer showing %d degrees Celsius" % t)


def temp_read(r):
    t = r.randint(6, 48)
    if t % 10 in (0,):
        raise AssertionError
    return mcq("What temperature does the thermometer show?" + fig(thermo_svg(t)), "%d °C" % t, ["%d °C" % x for x in (t + 2, t - 2, t + 10, t - 1, t + 1) if 0 < x < 50],
               "Each small mark is 2 °C. The red line stops at <b>%d °C</b>." % t)


CITY_T = {"Lagos": (24, 32), "Abuja": (21, 34), "Kano": (18, 38), "Jos": (14, 28), "Maiduguri": (20, 40), "Port Harcourt": (23, 31), "Sokoto": (22, 41), "Enugu": (22, 33)}


def temp_diff(r):
    c = ch(r, sorted(CITY_T))
    lo, hi = CITY_T[c]
    lo += r.randint(-2, 2)
    hi += r.randint(-2, 2)
    d = hi - lo
    return mcq("In %s one day, the lowest temperature was %d °C at dawn and the highest was %d °C in the afternoon. By how many degrees did it rise?" % (c, lo, hi),
               "%d °C" % d, ["%d °C" % x for x in (hi + lo, d + 1, d - 1, d + 10, hi) if x > 0],
               "Rise = highest − lowest = %d − %d = <b>%d °C</b>." % (hi, lo, d))


def temp_change(r):
    t = r.randint(20, 36)
    d = r.randint(2, 9)
    up = r.random() < 0.5
    k = K(r)
    nt = t + d if up else t - d
    when = ch(r, ["By noon", "By 3 p.m.", "An hour later", "After the rain"]) if up else ch(r, ["After the rain", "By night", "In the evening", "At midnight"])
    if up and when == "After the rain":
        when = "By noon"
    return mcq("At 8 a.m. the temperature was %d °C. %s it had %s by %d °C. What was the temperature then?" % (t, when, "risen" if up else "fallen", d),
               "%d °C" % nt, ["%d °C" % x for x in (t - d if up else t + d, nt + 1, nt - 1, d) if x > 0],
               "%s %d °C: %d %s %d = <b>%d °C</b>." % ("Add" if up else "Take away", d, t, "+" if up else "−", d, nt))


def temp_fact(r):
    facts = [("Water boils at", "100 °C", ["0 °C", "37 °C", "50 °C", "212 °C"]), ("Water freezes into ice at", "0 °C", ["100 °C", "10 °C", "32 °C", "−10 °C"]),
             ("The normal temperature of a healthy person is about", "37 °C", ["100 °C", "25 °C", "47 °C", "17 °C"]),
             ("We measure temperature with a", "thermometer", ["ruler", "weighing scale", "measuring jug", "clock"]),
             ("The unit °C is read as", "degrees Celsius", ["degrees centimetre", "decimal Celsius", "centigrams", "Celsius metres"]),
             ("A hot afternoon in Kano in April could be about", "40 °C", ["4 °C", "400 °C", "0 °C", "100 °C"]),
             ("A cool harmattan morning in Jos could be about", "12 °C", ["120 °C", "60 °C", "1 °C", "90 °C"]),
             ("A cold drink from the fridge is about", "5 °C", ["50 °C", "100 °C", "37 °C", "75 °C"])]
    a, good, bad = ch(r, facts)
    return mcq(a + " ____.", good, bad, "<b>%s</b>." % good)


def temp_avg(r):
    vals = [r.randint(26, 36) for _ in range(5)]
    s = sum(vals)
    if s % 5:
        raise AssertionError
    m = s // 5
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    tab = "<table class='sn-table'><tr><th>Day</th>%s</tr><tr><th>°C</th>%s</tr></table>" % ("".join("<td>%s</td>" % d[:3] for d in days), "".join("<td>%d</td>" % v for v in vals))
    return mcq("The midday temperatures in %s for one week are shown. What was the average (mean) temperature?" % ch(r, PLACES) + tab,
               "%d °C" % m, ["%d °C" % x for x in (m + 1, m - 1, max(vals), s) if x > 0],
               "Add them: %s = %d. Divide by 5: <b>%d °C</b>." % (" + ".join(map(str, vals)), s, m))


# ============================================================ money: interest, discount, commission
ITEMS = [("a bag of rice", 50000, 90000), ("a bicycle", 60000, 150000), ("a ceiling fan", 30000, 70000), ("a sewing machine", 80000, 200000),
         ("a pair of shoes", 8000, 25000), ("a school bag", 6000, 18000), ("a television", 150000, 400000), ("a phone", 60000, 250000),
         ("a gas cooker", 90000, 250000), ("a carton of noodles", 9000, 16000), ("a wristwatch", 10000, 40000), ("a blender", 25000, 60000)]


def item(r, step=500):
    name, lo, hi = ch(r, ITEMS)
    return name, r.randint(lo // step, hi // step) * step


def si(r):
    p = ch(r, [10000, 20000, 25000, 40000, 50000, 60000, 80000, 100000, 120000, 150000, 200000])
    rate = ch(r, [2, 3, 4, 5, 6, 8, 10, 12, 15])
    t = r.randint(1, 5)
    i = p * rate * t // 100
    if p * rate * t % 100:
        raise AssertionError
    k = K(r)
    q = r.randint(0, 2)
    w = [naira(p * rate // 100), naira(p + i), naira(i * 2), naira(p * rate * t // 10)]
    if q == 0:
        return mcq("Find the simple interest on %s for %d year%s at %d%% per annum." % (naira(p), t, "" if t == 1 else "s", rate), naira(i), [x for x in w if x != naira(i)],
                   "I = P × R × T ÷ 100 = %s × %d × %d ÷ 100 = <b>%s</b>." % (comma(p), rate, t, naira(i)))
    if q == 1:
        return mcq("%s saves %s in a bank that pays %d%% simple interest per year. How much will %s have after %d year%s (amount)?" % (k["n"], naira(p), rate, k["he"], t, "" if t == 1 else "s"),
                   naira(p + i), [naira(i), naira(p + i * 2), naira(p + p * rate // 100) if t > 1 else naira(p + i + 1000), naira(p - i)],
                   "Interest = %s × %d × %d ÷ 100 = %s. Amount = %s + %s = <b>%s</b>." % (comma(p), rate, t, naira(i), naira(p), naira(i), naira(p + i)))
    return mcq("A loan of %s gives %s simple interest in %d year%s. What is the rate per annum?" % (naira(p), naira(i), t, "" if t == 1 else "s"), "%d%%" % rate,
               ["%d%%" % x for x in (rate * t, rate + 1, rate * 2, rate + 5) if x != rate],
               "R = I × 100 ÷ (P × T) = %s × 100 ÷ (%s × %d) = <b>%d%%</b>." % (comma(i), comma(p), t, rate))


def discount(r):
    name, p = item(r, 1000)
    d = ch(r, [5, 10, 15, 20, 25, 30, 40, 50])
    off = p * d // 100
    if p * d % 100:
        raise AssertionError
    q = r.randint(0, 1)
    if q == 0:
        return mcq("A shop gives %d%% discount on %s marked %s. How much is the discount?" % (d, name, naira(p)), naira(off), [naira(p - off), naira(off * 2), naira(d * 100), naira(off + 500)],
                   "%d%% of %s = %s × %d ÷ 100 = <b>%s</b>." % (d, naira(p), comma(p), d, naira(off)))
    return mcq("%s is marked %s. During a sale there is %d%% off. What is the sale price?" % (name.capitalize(), naira(p), d), naira(p - off), [naira(off), naira(p + off), naira(p - d * 100), naira(p - off - 1000)],
               "Discount = %d%% of %s = %s. Sale price = %s − %s = <b>%s</b>." % (d, naira(p), naira(off), naira(p), naira(off), naira(p - off)))


def commission(r):
    k = K(r)
    sales = r.randint(10, 200) * 5000
    c = ch(r, [2, 3, 4, 5, 8, 10])
    com = sales * c // 100
    what = ch(r, ["cars", "land", "houses", "phones", "insurance", "textbooks"])
    return mcq("%s is paid %d%% commission on every sale of %s. This month %s sold %s worth. How much commission did %s earn?" % (k["n"], c, what, k["he"], naira(sales), k["he"]),
               naira(com), [naira(sales - com), naira(com * 10), naira(c * 1000), naira(com + 5000)],
               "Commission = %d%% of %s = %s × %d ÷ 100 = <b>%s</b>." % (c, naira(sales), comma(sales), c, naira(com)))


def profit_pct(r):
    name, cp = item(r, 1000)
    pc = ch(r, [5, 10, 15, 20, 25, 30, 40, 50])
    gain = r.random() < 0.6
    d = cp * pc // 100
    if cp * pc % 100:
        raise AssertionError
    sp = cp + d if gain else cp - d
    q = r.randint(0, 1)
    word = "profit" if gain else "loss"
    if q == 0:
        return mcq("A trader bought %s for %s and sold it for %s. Find the %s per cent." % (name, naira(cp), naira(sp), word), "%d%%" % pc,
                   ["%d%%" % x for x in (pc + 5, pc * 2, d // 100 if d // 100 != pc else pc + 10, 100 - pc) if x > 0 and x != pc],
                   "%s = %s. %s %% = %s ÷ %s × 100 = <b>%d%%</b> (always divide by the cost price)." % (word.capitalize(), naira(d), word.capitalize(), comma(d), comma(cp), pc))
    return mcq("A trader bought %s for %s and sold it at a %s of %d%%. What was the selling price?" % (name, naira(cp), word, pc), naira(sp),
               [naira(d), naira(cp - d if gain else cp + d), naira(cp + pc * 100 if gain else cp - pc * 100), naira(sp + 1000)],
               "%d%% of %s = %s. Selling price = %s %s %s = <b>%s</b>." % (pc, naira(cp), naira(d), naira(cp), "+" if gain else "−", naira(d), naira(sp)))


def vat(r):
    name, p = item(r, 2000)
    t = p * 75 // 1000
    if p * 75 % 1000:
        raise AssertionError
    return mcq("Value Added Tax (VAT) in Nigeria is 7.5%%. %s costs %s before VAT. How much is the VAT?" % (name.capitalize(), naira(p)), naira(t),
               [naira(p * 75 // 100), naira(p + t), naira(p * 7 // 100), naira(t * 2)],
               "7.5%% of %s = %s × 7.5 ÷ 100 = <b>%s</b>." % (naira(p), comma(p), naira(t)))


def hire(r):
    k = K(r)
    price = r.randint(20, 120) * 5000
    dep = ch(r, [10, 20, 25])
    n = ch(r, [6, 10, 12])
    inst = r.randint(2, 15) * 1000
    dp = price * dep // 100
    total = dp + n * inst
    if total <= price:
        raise AssertionError
    name = ch(r, ["a motorcycle", "a refrigerator", "a generator", "a laptop"])
    return mcq("%s buys %s on hire purchase. %s pays a deposit of %s and %d monthly payments of %s. What is the total %s pays?" % (k["n"], name, k["He"], naira(dp), n, naira(inst), k["he"]),
               naira(total), [naira(n * inst), naira(dp + inst), naira(total + inst), naira(dp * n)],
               "Total = deposit + payments = %s + %d × %s = %s + %s = <b>%s</b>." % (naira(dp), n, naira(inst), naira(dp), naira(n * inst), naira(total)))


# ============================================================ percentages of naira amounts
def pct_of(r):
    p = ch(r, [5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75])
    v = r.randint(4, 120) * 500
    a = v * p // 100
    if v * p % 100:
        raise AssertionError
    k = K(r)
    ctx = ch(r, ["%s spends %d%% of %s pocket money of %s on transport.", "%s gives %d%% of %s savings of %s to %s church." , "%s puts %d%% of %s salary of %s into savings."])
    if "church" in ctx:
        ctx = "%s gives %d%% of %s savings of %s to charity."
    q = ctx % (k["n"], p, k["his"], naira(v)) + " How much is this?"
    return mcq(q, naira(a), [naira(v - a), naira(p * 100), naira(a * 2), naira(a + 500)],
               "%d%% of %s = %d ÷ 100 × %s = <b>%s</b>." % (p, naira(v), p, comma(v), naira(a)))


def pct_what(r):
    tot = ch(r, [20, 25, 40, 50, 80, 200])
    part = r.randint(1, tot - 1)
    if part * 100 % tot:
        raise AssertionError
    p = part * 100 // tot
    k = K(r)
    return mcq("%s scored %d out of %d in a test. What percentage is this?" % (k["n"], part, tot), "%d%%" % p, ["%d%%" % x for x in (part, 100 - p, p + 5, tot - part) if x != p and 0 < x <= 100],
               "%d ÷ %d × 100 = <b>%d%%</b>." % (part, tot, p))


def pct_class(r):
    n = ch(r, [20, 25, 40, 50])
    g = r.randint(5, n - 5)
    if g * 100 % n:
        raise AssertionError
    p = g * 100 // n
    return mcq("A class has %d pupils. %d of them are girls. What percentage are boys?" % (n, g), "%d%%" % (100 - p), ["%d%%" % x for x in (p, n - g, 100 - g, 100 - p + 5) if x != 100 - p and 0 < x <= 100],
               "Boys = %d − %d = %d. %d ÷ %d × 100 = <b>%d%%</b>." % (n, g, n - g, n - g, n, 100 - p))


# ============================================================ bearings (compass angles)
BEAR = [("north", 0), ("north-east", 45), ("east", 90), ("south-east", 135), ("south", 180), ("south-west", 225), ("west", 270), ("north-west", 315)]


def b3(x):
    return "%03d°" % x


def bearing_dir(r):
    d, a = ch(r, BEAR)
    return mcq("What is the three-figure bearing of the direction %s?" % d, b3(a), [b3(x) for x in ((a + 90) % 360, (a + 180) % 360, (360 - a) % 360, (a + 45) % 360) if x != a],
               "Bearings are measured clockwise from north. %s is <b>%s</b>." % (d.capitalize(), b3(a)))


def bearing_name(r):
    d, a = ch(r, BEAR)
    return mcq("Which direction has a bearing of %s?" % b3(a), d.capitalize(), [x.capitalize() for x, b in BEAR if b in ((a + 90) % 360, (a + 180) % 360, (360 - a) % 360, (a + 270) % 360) and x != d],
               "Turn %d° clockwise from north: <b>%s</b>." % (a, d))


def bearing_turn(r):
    d1, a1 = ch(r, BEAR)
    d2, a2 = ch(r, BEAR)
    t = (a2 - a1) % 360
    if t == 0:
        raise AssertionError
    k = K(r)
    return mcq("%s is facing %s. %s turns clockwise until %s faces %s. Through how many degrees does %s turn?" % (k["n"], d1, k["He"], k["he"], d2, k["he"]),
               "%d°" % t, ["%d°" % x for x in (360 - t, t + 45, abs(a2 - a1) if abs(a2 - a1) != t else t + 90, t + 90) if 0 < x < 360 and x != t],
               "From %s (%s) to %s (%s) clockwise: <b>%d°</b>." % (d1, b3(a1), d2, b3(a2), t))


def bearing_back(r):
    a = r.randint(1, 35) * 10
    if a == 180:
        raise AssertionError
    bk = (a + 180) % 360
    return mcq("The bearing of a school from a market is %s. What is the bearing of the market from the school?" % b3(a), b3(bk),
               [b3(x) for x in ((a + 90) % 360, (360 - a) % 360, (a + 270) % 360, abs(180 - a)) if x != bk],
               "The back bearing is 180° more (or less): %d %s 180 = <b>%s</b>." % (a, "+" if a < 180 else "−", b3(bk)))


def bearing_svg(a):
    cx, cy, R = 110, 110, 80
    b = "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (cx, cy, cx, cy - R - 10, INK)
    b += "<path d='M%d %d l-5 10 l10 0 z' fill='%s'/>" % (cx, cy - R - 14, INK) + text(cx, cy - R - 20, "N", 15)
    rad = math.radians(a)
    x, y = cx + R * math.sin(rad), cy - R * math.cos(rad)
    b += "<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, cy, x, y, RED)
    b += "<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK) + text(cx + 30 * math.sin(math.radians(a / 2.0 + 180)), cy - 30 * math.cos(math.radians(a / 2.0 + 180)) + 5, "P", 15) + text(x + 12 * math.sin(rad), y - 12 * math.cos(rad) + 5, "Q", 15)
    sweep = 1 if a > 180 else 0
    rr = 26
    b += "<path d='M%d %d A%d %d 0 %d 1 %.1f %.1f' fill='none' stroke='%s' stroke-width='1.5'/>" % (cx, cy - rr, rr, rr, sweep, cx + rr * math.sin(rad), cy - rr * math.cos(rad), BLUE)
    return svg_wrap(220, 220, b, "bearing of Q from P")


def bearing_read(r):
    a = r.randint(2, 34) * 10 + ch(r, [0, 5])
    if a in (90, 180, 270):
        raise AssertionError
    return mcq("The diagram shows the direction of Q from P, measured clockwise from north. What is the bearing of Q from P?" + fig(bearing_svg(a)),
               b3(a), [b3(x) for x in ((360 - a) % 360, (a + 180) % 360, (a + 90) % 360, abs(90 - a)) if x != a],
               "Measure clockwise from north to the line PQ: <b>%s</b>." % b3(a))


# ============================================================ averages
def median_list(r):
    n = ch(r, [5, 7, 9, 6, 8])
    vals = [r.randint(2, 40) for _ in range(n)]
    s = sorted(vals)
    if n % 2:
        m = s[n // 2]
        e = "Arrange in order: %s. The middle number is <b>%d</b>." % (", ".join(map(str, s)), m)
        ans = m
    else:
        a, b = s[n // 2 - 1], s[n // 2]
        if (a + b) % 2:
            raise AssertionError
        ans = (a + b) // 2
        e = "Arrange in order: %s. The two middle numbers are %d and %d, so the median is (%d + %d) ÷ 2 = <b>%d</b>." % (", ".join(map(str, s)), a, b, a, b, ans)
    w = [vals[n // 2], s[0] + s[-1], round(sum(vals) / n), s[n // 2 + 1], Counter(vals).most_common(1)[0][0]]
    return mcq("Find the median of: %s" % ", ".join(map(str, vals)), ans, [x for x in w if x != ans], e)


def mean_list(r):
    n = r.randint(4, 7)
    m = r.randint(5, 60)
    vals = [m + r.randint(-8, 8) for _ in range(n - 1)]
    last = m * n - sum(vals)
    if not 1 <= last <= 99:
        raise AssertionError
    vals.append(last)
    r.shuffle(vals)
    s = sum(vals)
    w = [s, sorted(vals)[n // 2], m + 1, m - 1, max(vals) - min(vals)]
    return mcq("Find the mean of: %s" % ", ".join(map(str, vals)), m, [x for x in w if x != m],
               "Mean = total ÷ number = %d ÷ %d = <b>%d</b>." % (s, n, m))


def range_list(r):
    vals = [r.randint(3, 90) for _ in range(r.randint(5, 8))]
    rg = max(vals) - min(vals)
    w = [max(vals), max(vals) + min(vals), sorted(vals)[len(vals) // 2], rg + 1, vals[-1] - vals[0] if vals[-1] - vals[0] != rg else rg + 2]
    return mcq("Find the range of: %s" % ", ".join(map(str, vals)), rg, [x for x in w if x != rg and x > 0],
               "Range = highest − lowest = %d − %d = <b>%d</b>." % (max(vals), min(vals), rg))


def mode_word(r):
    shoe = [r.randint(30, 40) for _ in range(r.randint(8, 12))]
    c = Counter(shoe).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        raise AssertionError
    m = c[0][0]
    return mcq("The shoe sizes of some pupils are: %s. What is the modal shoe size?" % ", ".join(map(str, shoe)), m,
               [x for x in (max(shoe), c[0][1], sorted(shoe)[len(shoe) // 2], c[1][0] if len(c) > 1 else m + 1, m + 1) if x != m],
               "%d appears most often (%d times), so the mode is <b>%d</b>." % (m, c[0][1], m))


def mean_word(r):
    k = K(r)
    n = r.randint(3, 6)
    m = r.randint(40, 90)
    sc = [m + r.randint(-12, 12) for _ in range(n - 1)]
    last = m * n - sum(sc)
    if not 20 <= last <= 100:
        raise AssertionError
    sc.append(last)
    subj = ["Mathematics", "English", "Basic Science", "Social Studies", "Yoruba", "Igbo", "Hausa", "Agricultural Science"]
    subs = r.sample(subj, n)
    return mcq("%s's scores were %s. What was %s average score?" % (k["n"], ", ".join("%s %d" % (s, v) for s, v in zip(subs, sc)), k["his"]),
               m, [sum(sc), m + 2, m - 3, sorted(sc)[n // 2] if sorted(sc)[n // 2] != m else m + 5],
               "Total = %d. Average = %d ÷ %d = <b>%d</b>." % (sum(sc), sum(sc), n, m))


def mean_missing(r):
    n = r.randint(4, 6)
    m = r.randint(10, 40)
    vals = [m + r.randint(-6, 6) for _ in range(n - 1)]
    x = m * n - sum(vals)
    if x <= 0:
        raise AssertionError
    return mcq("The mean of %d numbers is %d. %d of them are %s. What is the other number?" % (n, m, n - 1, ", ".join(map(str, vals))), x,
               [m, m * n, x + n, m * (n - 1) - sum(vals) if m * (n - 1) - sum(vals) > 0 else x + 1],
               "Total = %d × %d = %d. Missing = %d − %d = <b>%d</b>." % (m, n, m * n, m * n, sum(vals), x))


# ============================================================ time (Primary 5–6)
def hm(m):
    h, mi = divmod(m % 1440, 60)
    ap = "a.m." if h < 12 else "p.m."
    hh = h % 12 or 12
    return "%d:%02d %s" % (hh, mi, ap)


def h24(m):
    h, mi = divmod(m % 1440, 60)
    return "%02d:%02d" % (h, mi)


def t_24(r):
    m = r.randint(13, 23) * 60 + r.randint(0, 11) * 5
    if r.random() < 0.5:
        return mcq("Write %s in the 24-hour clock." % hm(m), h24(m), [h24(m - 720), h24(m + 60), "%02d:%02d" % (m // 60 + 2, m % 60) if m // 60 < 22 else h24(m - 60), h24(m + 5)],
                   "For p.m. times add 12 hours: <b>%s</b>." % h24(m))
    return mcq("Write %s in the 12-hour clock." % h24(m), hm(m), [hm(m - 720), hm(m - 60), "%d:%02d p.m." % (m // 60 - 10, m % 60), hm(m + 60)],
               "Take away 12 hours and write p.m.: <b>%s</b>." % hm(m))


TRIPS = [("Lagos", "Ibadan", 90, 180), ("Abuja", "Kaduna", 120, 210), ("Enugu", "Onitsha", 60, 150), ("Kano", "Zaria", 90, 160), ("Benin City", "Asaba", 90, 170), ("Port Harcourt", "Owerri", 70, 150)]


def t_dur(r):
    a, b, lo, hi = ch(r, TRIPS)
    st = r.randint(6 * 12, 15 * 12) * 5
    d = r.randint(lo // 5, hi // 5) * 5
    en = st + d
    h, m = divmod(d, 60)
    dd = "%d h %d min" % (h, m) if m else "%d h" % h
    w = ["%d h %d min" % divmod(d + 60, 60), "%d h %d min" % divmod(d + 40, 60), "%d h %d min" % divmod(abs(d - 40), 60), "%d h %d min" % divmod(d + 15, 60)]
    w = [x.replace(" 0 min", "") for x in w]
    return mcq("A bus left %s at %s and reached %s at %s. How long was the journey?" % (a, hm(st), b, hm(en)), dd, w,
               "From %s to %s is <b>%s</b>." % (hm(st), hm(en), dd))


def t_end(r):
    k = K(r)
    st = r.randint(8 * 12, 18 * 12) * 5
    d = r.randint(5, 40) * 5
    act = ch(r, ["a football match", "a church service", "a wedding", "a film", "a quiz competition", "a party", "an end-of-term play"])
    en = st + d
    h, m = divmod(d, 60)
    dd = ("%d hour%s" % (h, "" if h == 1 else "s") if h else "") + (" %d minutes" % m if m else "")
    return mcq("%s started at %s and lasted %s. At what time did it end?" % (act.capitalize(), hm(st), dd.strip()), hm(en), [hm(en + 60), hm(en - 30), hm(st + d % 60 + 100), hm(en + 10)],
               "%s + %s = <b>%s</b>." % (hm(st), dd.strip(), hm(en)))


def t_conv(r):
    q = r.randint(0, 3)
    if q == 0:
        h = r.randint(2, 9)
        m = r.randint(1, 59)
        return mcq("How many minutes are in %d hours %d minutes?" % (h, m), h * 60 + m, [h * 100 + m, h + m, h * 60, h * 60 + m + 60], "%d × 60 + %d = <b>%d</b>." % (h, m, h * 60 + m))
    if q == 1:
        mi = r.randint(70, 500)
        h, m = divmod(mi, 60)
        if not m:
            raise AssertionError
        return mcq("Change %d minutes to hours and minutes." % mi, "%d h %d min" % (h, m), ["%d h %d min" % (mi // 100, mi % 100) if mi % 100 < 60 else "%d h %d min" % (h + 1, m), "%d h %d min" % (h - 1, m + 60) if h > 1 else "%d h" % (h + 2), "%d h %d min" % (h, m + 10) if m < 50 else "%d h" % (h + 3), "%d h %d min" % (h + 1, m)],
                   "%d ÷ 60 = %d remainder %d: <b>%d h %d min</b>." % (mi, h, m, h, m))
    if q == 2:
        w = r.randint(2, 12)
        d = r.randint(1, 6)
        return mcq("How many days are in %d weeks %d days?" % (w, d), w * 7 + d, [w * 10 + d, w + d, w * 7, w * 7 + d + 7], "%d × 7 + %d = <b>%d</b> days." % (w, d, w * 7 + d))
    y = r.randint(2, 6)
    return mcq("How many months are in %d years?" % y, y * 12, [y * 10, y * 52, y * 365, y * 12 + 12], "%d × 12 = <b>%d</b> months." % (y, y * 12))


# ============================================================ speed (Primary 6)
def speed(r):
    s = ch(r, [30, 40, 45, 50, 60, 70, 75, 80, 90, 100])
    t = ch(r, [F(1, 2), 1, F(3, 2), 2, F(5, 2), 3, 4, 5])
    d = s * t
    if d.denominator != 1:
        raise AssertionError
    d = int(d)
    tt = {F(1, 2): "30 minutes", F(3, 2): "1 hour 30 minutes", F(5, 2): "2 hours 30 minutes"}.get(t, "%d hour%s" % (t, "" if t == 1 else "s"))
    a, b, _, _ = ch(r, TRIPS)
    q = r.randint(0, 2)
    veh = ch(r, ["A car", "A bus", "A lorry", "A train"])
    if q == 0:
        return mcq("%s travels at an average speed of %d km/h for %s. How far does it travel?" % (veh, s, tt), "%d km" % d, ["%d km" % x for x in (s + int(t * 10), d + s, s * 2 if s * 2 != d else s * 3, d // 2 if d // 2 else d + 5) if x != d],
                   "Distance = speed × time = %d × %s = <b>%d km</b>." % (s, frac(t) if t.denominator != 1 else str(t), d))
    if q == 1:
        return mcq("%s travels %d km from %s to %s in %s. What is its average speed?" % (veh, d, a, b, tt), "%d km/h" % s, ["%d km/h" % x for x in (d, s + 10, s * 2, s - 5) if x != s and x > 0],
                   "Speed = distance ÷ time = %d ÷ %s = <b>%d km/h</b>." % (d, frac(t) if t.denominator != 1 else str(t), s))
    return mcq("How long does it take to travel %d km at %d km/h?" % (d, s), tt, [x for x in ("%d hours" % (t + 1), "%d hours" % (2 * t + 1) if t.denominator == 1 else "45 minutes", "2 hours" if tt != "2 hours" else "3 hours", "1 hour 15 minutes") if x != tt],
               "Time = distance ÷ speed = %d ÷ %d = <b>%s</b>." % (d, s, tt))


# ============================================================ ratio with naira and real things
def ratio_share(r):
    a, b = r.sample(range(1, 8), 2)
    if math.gcd(a, b) != 1:
        raise AssertionError
    unit = r.randint(2, 60) * 500
    tot = (a + b) * unit
    k1, k2 = K(r), K(r)
    if k1["n"] == k2["n"]:
        raise AssertionError
    return mcq("%s and %s share %s in the ratio %d : %d. How much does %s get?" % (k1["n"], k2["n"], naira(tot), a, b, k1["n"]), naira(a * unit),
               [naira(b * unit), naira(tot // a) if tot % a == 0 else naira(a * unit + 500), naira(unit), naira(tot - unit)],
               "Total parts = %d + %d = %d. One part = %s ÷ %d = %s. %s gets %d × %s = <b>%s</b>." % (a, b, a + b, naira(tot), a + b, naira(unit), k1["n"], a, naira(unit), naira(a * unit)))


def ratio_simplify(r):
    a, b = r.sample(range(1, 10), 2)
    if math.gcd(a, b) != 1:
        raise AssertionError
    k = r.randint(2, 12)
    w = ["%d : %d" % (b, a), "%d : %d" % (a * k // math.gcd(a * k, b), b), "%d : %d" % (a + 1, b + 1), "%d : %d" % (a * 2, b * 2)]
    return mcq("Write %d : %d in its simplest form." % (a * k, b * k), "%d : %d" % (a, b), [x for x in w if x != "%d : %d" % (a, b)],
               "Divide both by %d: <b>%d : %d</b>." % (k, a, b))


def ratio_class(r):
    b, g = r.sample(range(2, 9), 2)
    if math.gcd(b, g) != 1:
        raise AssertionError
    k = r.randint(2, 6)
    q = r.randint(0, 1)
    if q == 0:
        return mcq("In a class the ratio of boys to girls is %d : %d. There are %d boys. How many girls are there?" % (b, g, b * k), g * k, [b * k + g, (b + g) * k, g * k + k, b * g],
                   "One part = %d ÷ %d = %d. Girls = %d × %d = <b>%d</b>." % (b * k, b, k, g, k, g * k))
    return mcq("The ratio of boys to girls in a class is %d : %d. There are %d pupils. How many are boys?" % (b, g, (b + g) * k), b * k, [g * k, (b + g) * k // 2 if (b + g) * k // 2 != b * k else b * k + 1, b * (b + g), b * k + k],
               "Parts = %d. One part = %d ÷ %d = %d. Boys = %d × %d = <b>%d</b>." % (b + g, (b + g) * k, b + g, k, b, k, b * k))


def proportion(r):
    k = K(r)
    n1 = r.randint(2, 6)
    p = r.randint(2, 30) * 50
    n2 = r.randint(n1 + 1, 15)
    thing = ch(r, ["exercise books", "pencils", "oranges", "loaves of bread", "packets of biscuits", "bottles of water"])
    if thing == "loaves of bread":
        p = r.randint(10, 30) * 100
    return mcq("%d %s cost %s. How much will %d %s cost?" % (n1, thing, naira(n1 * p), n2, thing), naira(n2 * p),
               [naira(n1 * p + n2), naira(n2 * p + p), naira(n1 * p * n2), naira((n2 - n1) * p)],
               "One costs %s ÷ %d = %s. %d cost %d × %s = <b>%s</b>." % (naira(n1 * p), n1, naira(p), n2, n2, naira(p), naira(n2 * p)))


def inverse_prop(r):
    w1 = ch(r, [2, 3, 4, 5, 6, 8])
    d1 = ch(r, [3, 4, 6, 8, 10, 12, 15])
    tot = w1 * d1
    ws = [x for x in (2, 3, 4, 5, 6, 8, 10, 12) if tot % x == 0 and x != w1]
    if not ws:
        raise AssertionError
    w2 = ch(r, ws)
    d2 = tot // w2
    job = ch(r, ["build a wall", "weed a farm", "paint a classroom", "dig a well", "harvest a maize farm"])
    return mcq("%d workers can %s in %d days. How many days will %d workers take, working at the same rate?" % (w1, job, d1, w2), d2,
               [d1 * w2 // w1 if d1 * w2 % w1 == 0 else d1 + w2, d1 + w1 - w2 if d1 + w1 - w2 > 0 else d2 + 2, tot, d2 + 1],
               "Total work = %d × %d = %d worker-days. %d ÷ %d = <b>%d days</b>. More workers take fewer days." % (w1, d1, tot, tot, w2, d2))


# ============================================================ squares and cubes (Primary 6)
def cube_of(r):
    n = r.randint(2, 12)
    return mcq("What is %d³ (%d × %d × %d)?" % (n, n, n, n), n ** 3, [3 * n, n * n, n ** 3 + n, (n + 1) ** 3], "%d × %d × %d = <b>%s</b>." % (n, n, n, comma(n ** 3)))


def cube_root(r):
    n = r.randint(2, 12)
    return mcq("What is the cube root of %s (∛%s)?" % (comma(n ** 3), comma(n ** 3)), n, [n ** 3 // 3, n + 1, n - 1, n * n], "%d × %d × %d = %s, so ∛%s = <b>%d</b>." % (n, n, n, comma(n ** 3), comma(n ** 3), n))


def sq_big(r):
    n = r.randint(11, 30)
    if r.random() < 0.5:
        return mcq("What is %d²?" % n, n * n, [2 * n, n * n + n, (n + 1) ** 2, n * n - 10], "%d × %d = <b>%s</b>." % (n, n, comma(n * n)))
    return mcq("Find √%s." % comma(n * n), n, [n * n // 2, n + 1, n - 1, 2 * n], "%d × %d = %s, so √%s = <b>%d</b>." % (n, n, comma(n * n), comma(n * n), n))


def sq_factor(r):
    a, b = r.sample([2, 3, 5, 7], 2)
    i, j = r.randint(1, 2), 1
    root = a ** i * b ** j
    n = root * root
    pf = " × ".join([str(a)] * (2 * i) + [str(b)] * 2)
    return mcq("Use prime factors to find √%s." % comma(n), root, [n // 2, root + a, root * 2, root - b],
               "%s = %s. Take one of each pair: %s = <b>%d</b>." % (comma(n), pf, " × ".join([str(a)] * i + [str(b)]), root))


def sq_cube_word(r):
    q = r.randint(0, 3)
    if q == 0:
        s = r.randint(5, 30)
        return mcq("A square plot of land has an area of %s m². How long is one side?" % comma(s * s), "%d m" % s, ["%d m" % x for x in (s * s // 4, s + 2, 2 * s, s - 1)],
                   "Side = √%s = <b>%d m</b>." % (comma(s * s), s))
    if q == 1:
        s = r.randint(2, 10)
        return mcq("A cube-shaped water tank has a volume of %s m³. How long is each edge?" % comma(s ** 3), "%d m" % s, ["%d m" % x for x in (s * s, s + 1, 3 * s, s ** 3 // 3 if s ** 3 // 3 else s + 2)],
                   "Edge = ∛%s = <b>%d m</b>." % (comma(s ** 3), s))
    if q == 2:
        n = r.randint(5, 25)
        return mcq("%d rows of %d chairs make a square. How many chairs are there?" % (n, n), n * n, [2 * n, n * n + n, 4 * n, n * n - n], "%d² = <b>%d</b>." % (n, n * n))
    s = r.randint(2, 9)
    return mcq("A box is a cube with edges of %d cm. What is its volume?" % s, "%d cm³" % s ** 3, ["%d cm³" % x for x in (s * s, 3 * s, 6 * s * s, s ** 3 + s)] , "%d × %d × %d = <b>%d cm³</b>." % (s, s, s, s ** 3))


# ============================================================ quantitative reasoning
def qr_rule(r):
    a = r.randint(2, 9)
    b = r.randint(-5, 12)
    xs = r.sample(range(1, 15), 4)
    ys = [a * x + b for x in xs]
    if min(ys) <= 0:
        raise AssertionError
    pairs = "; ".join("%d → %d" % (x, y) for x, y in zip(xs[:3], ys[:3]))
    w = [ys[3] + a, ys[3] - 1, a * xs[3], xs[3] + ys[2] - xs[2]]
    rule = "multiply by %d%s" % (a, (" and add %d" % b) if b > 0 else (" and take away %d" % -b) if b < 0 else "")
    return mcq("Find the missing number. %s; %d → ?" % (pairs, xs[3]), ys[3], [x for x in w if x != ys[3]],
               "The rule is %s: %d × %d %s = <b>%d</b>." % (rule, xs[3], a, ("+ %d" % b) if b > 0 else ("− %d" % -b) if b < 0 else "+ 0", ys[3]))


def qr_series(r):
    k = r.randint(0, 3)
    if k == 0:
        a, d = r.randint(2, 30), r.randint(3, 15)
        s = [a + i * d for i in range(6)]
        rule = "add %d each time" % d
    elif k == 1:
        a, m = r.randint(1, 5), ch(r, [2, 3])
        s = [a * m ** i for i in range(6)]
        rule = "multiply by %d each time" % m
    elif k == 2:
        a = r.randint(1, 6)
        s = [(a + i) ** 2 for i in range(6)]
        rule = "they are square numbers"
    else:
        a, d = r.randint(1, 5), r.randint(1, 3)
        s = [a]
        for i in range(5):
            s.append(s[-1] + d + i)
        rule = "the gap grows by 1 each time"
    gap = r.randint(2, 5)
    show = [str(x) if i != gap else "?" for i, x in enumerate(s)]
    ans = s[gap]
    return mcq("Find the missing number: %s" % ", ".join(show), ans, [ans + 1, ans - 1, ans + 2, s[gap - 1] + s[gap + 1] if gap < 5 else ans * 2],
               "The rule: %s. The missing number is <b>%d</b>." % (rule, ans))


def qr_box(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    op = ch(r, ["+", "×"])
    c = a + b if op == "+" else a * b
    x, y = r.randint(2, 12), r.randint(2, 12)
    z = x + y if op == "+" else x * y
    return mcq("In each box the bottom number is made from the two top numbers in the same way. Box 1: %d and %d give %d. Box 2: %d and %d give ?" % (a, b, c, x, y), z,
               [x * y if op == "+" else x + y, z + 1, z - 2, abs(x - y) if abs(x - y) else z + 3],
               "In box 1, %d %s %d = %d. So %d %s %d = <b>%d</b>." % (a, op, b, c, x, op, y, z))


def qr_odd(r):
    k = ch(r, [2, 3, 4, 5, 6, 7, 9])
    xs = r.sample([k * i for i in range(2, 13)], 4)
    odd = k * r.randint(2, 12) + r.randint(1, k - 1)
    return mcq("Which number does not belong with the others: %s?" % ", ".join(map(str, sorted(xs + [odd]))), odd, xs,
               "All the others are multiples of %d. <b>%d</b> is not." % (k, odd))


# ============================================================ circles with π = 22/7 (Primary 6)
def circ_word(r):
    rr = 7 * r.randint(1, 6)
    k = r.randint(0, 4)
    C_ = 2 * 22 * rr // 7
    A_ = 22 * rr * rr // 7
    if k == 0:
        return mcq("A round table top has a radius of %d cm. Find its circumference. (Use π = 22/7.)" % rr, "%d cm" % C_, ["%d cm" % x for x in (C_ // 2, A_, C_ + 7, 2 * rr)],
                   "C = 2πr = 2 × 22/7 × %d = <b>%d cm</b>." % (rr, C_))
    if k == 1:
        return mcq("A circular flower bed has a radius of %d m. Find its area. (Use π = 22/7.)" % rr, "%d m²" % A_, ["%d m²" % x for x in (C_, A_ * 2, 22 * rr // 7 * 2, A_ // 2)],
                   "A = πr² = 22/7 × %d × %d = <b>%d m²</b>." % (rr, rr, A_))
    if k == 2:
        d = 2 * rr
        return mcq("A bicycle wheel has a diameter of %d cm. How far does the bicycle move when the wheel turns once? (Use π = 22/7.)" % d, "%d cm" % C_, ["%d cm" % x for x in (d, A_, C_ * 2, C_ // 2)],
                   "One turn = circumference = πd = 22/7 × %d = <b>%d cm</b>." % (d, C_))
    if k == 3:
        n = r.randint(2, 10)
        return mcq("A wheel of radius %d cm turns %d times. How far does it travel? (Use π = 22/7.)" % (rr, n), "%s cm" % comma(C_ * n), ["%s cm" % comma(x) for x in (C_, A_ * n, C_ * n // 2, C_ * n + C_)],
                   "One turn = 2 × 22/7 × %d = %d cm. %d turns = <b>%s cm</b>." % (rr, C_, n, comma(C_ * n)))
    return mcq("The circumference of a circle is %d cm. What is its radius? (Use π = 22/7.)" % C_, "%d cm" % rr, ["%d cm" % x for x in (2 * rr, C_ // 2, rr + 7, rr * rr)],
               "r = C ÷ (2π) = %d ÷ 44/7 = <b>%d cm</b>." % (C_, rr))
