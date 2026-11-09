# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Rational Number Word Problems (7.NS.A.3)
  python tools/gen_us_math_g7_rational_number_word_problems.py
Real-world problems with the four operations on integers, decimals and fractions.
Wrong answers come from real mistakes: the wrong sign, choosing the wrong operation
(adding a change instead of subtracting it, multiplying instead of dividing), dividing in the
wrong order, and stopping after the first step of a two-step problem.
"""
import random
import re
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, table, example, write_unit, fr, MINUS)

R = random.Random(71201)
UPDATED = "2026-11-09"
P = People(R)


def n(v):
    v = F(v)
    s = num(v)
    if s is None:
        w, r = divmod(abs(v.numerator), v.denominator)
        s = (MINUS if v < 0 else "") + ((str(w) + " ") if w else "") + fr(r, v.denominator)
    return s


def money(v):
    v = F(v)
    s = num(abs(v))
    if "." in s:
        a, b = s.split(".")
        s = a + "." + (b + "0")[:2]
    return (MINUS if v < 0 else "") + "$" + s


def nf(v):
    """Fraction style: 2 3/4, −1/2, 5."""
    v = F(v)
    w, r = divmod(abs(v.numerator), v.denominator)
    if r == 0:
        return (MINUS if v < 0 else "") + str(w)
    return (MINUS if v < 0 else "") + ((str(w) + " ") if w else "") + fr(r, v.denominator)


SING = {" cups": " cup", " points": " point", " acres": " acre", " inches": " inch", " miles": " mile", " pieces": " piece",
        " bottles": " bottle", " days": " day", " dollars": " dollar", " shirts": " shirt"}


def item(q, v, ws, e, show=None, unit="", st="d"):
    base = nf if st == "f" else n
    show = show or (lambda x: base(x) + (SING.get(unit, unit) if abs(F(x)) <= 1 else unit))
    v = F(v)
    cands = []
    for w in list(ws) + [v + 1, v - 1, v * 2, -v]:
        w = F(w)
        if w != v:
            cands.append((show(w), w))
    return mcq(q, (show(v), v), cands, e)


# ------------------------------------------------------------ set 1: choose the operation
def set_operation():
    its = []
    ops = [("The temperature is −4°F. It rises 9 degrees. Which expression gives the new temperature?", "−4 + 9", ["−4 − 9", "9 − (−4)", "−4 × 9"],
            "Rising means adding: −4 + 9 = 5°F."),
           ("A diver is at −30 feet. She goes down 12 more feet. Which expression gives her new depth?", "−30 + (−12)", ["−30 + 12", "30 − 12", "−30 × 12"],
            "Going down is a negative change: −30 + (−12) = −42 feet."),
           ("The high was 12°F and the low was −5°F. Which expression gives the difference?", "12 − (−5)", ["12 + (−5)", "−5 − 12", "12 × (−5)"],
            "The difference is high − low: 12 − (−5) = 17 degrees."),
           ("A stock lost $3 each day for 5 days. Which expression gives the total change?", "5 × (−3)", ["5 + (−3)", "−3 ÷ 5", "5 − 3"],
            "The same loss 5 times: 5 × (−3) = −15 dollars."),
           ("A total loss of $24 was shared equally by 4 partners. Which expression gives each partner's change?", "−24 ÷ 4", ["−24 × 4", "4 ÷ (−24)", "−24 + 4"],
            "Share means divide: −24 ÷ 4 = −6 dollars each."),
           ("A recipe needs 3/4 cup of milk for each batch. Which expression gives the milk for 6 batches?", "6 × 3/4", ["6 ÷ 3/4", "6 + 3/4", "3/4 ÷ 6"],
            "Six batches of 3/4 cup: 6 × 3/4 = 4 1/2 cups."),
           ("A 6-foot board is cut into pieces 3/4 foot long. Which expression gives the number of pieces?", "6 ÷ 3/4", ["6 × 3/4", "3/4 ÷ 6", "6 − 3/4"],
            "How many 3/4s are in 6? 6 ÷ 3/4 = 8 pieces."),
           ("Your account has −$15. You deposit $40. Which expression gives the new balance?", "−15 + 40", ["−15 − 40", "15 + 40", "40 − 15 − 15"],
            "A deposit adds: −15 + 40 = $25.")]
    for q, good, bad, e in ops:
        its.append(mcq(q, (good, "g"), [(b, b) for b in bad], e))
    # signs of answers
    signs = [("A submarine at −200 m rises 50 m. Is its new position above or below sea level?", "Below sea level (−150 m)",
              ["Above sea level (150 m)", "Below sea level (−250 m)", "At sea level (0 m)"], "−200 + 50 = −150. It is still below sea level."),
             ("You owe $8 to each of 3 friends. What number shows your total change in money?", "−24", ["24", "−11", "−5"], "Owing is negative: 3 × (−8) = −24."),
             ("The temperature fell 2.5°F each hour for 4 hours. What was the total change?", "−10°F", ["10°F", "−6.5°F", "−1.5°F"], "4 × (−2.5) = −10°F."),
             ("A team gained 6 yards, then lost 9 yards. What was the total change?", "−3 yards", ["15 yards", "3 yards", "−15 yards"], "6 + (−9) = −3 yards.")]
    for q, good, bad, e in signs:
        its.append(mcq(q, (good, "g"), [(b, b) for b in bad], e))
    quick = [("The temperature is −7°F and drops 6 degrees. What is the new temperature?", -13, [-1, 1, 13], "−7 + (−6) = −13°F.", "°F"),
             ("An elevator is on floor 3. It goes down 5 floors. Which floor is it on?", -2, [8, 2, -8], "3 + (−5) = −2, two floors below ground.", ""),
             ("A hiker is at 1,200 m and walks down 350 m. What is the new elevation?", 850, [1550, -850, 950], "1,200 − 350 = 850 m.", " m"),
             ("A bird is 25 feet above a pond. A fish is 8 feet below the surface. How far apart are they?", 33, [17, -33, 25], "25 − (−8) = 33 feet.", " ft"),
             ("Your score is −15. You earn 20 points. What is your score?", 5, [-35, 35, -5], "−15 + 20 = 5.", ""),
             ("The low on Monday was −3°C and the low on Tuesday was −11°C. How much colder was Tuesday?", 8, [14, -8, -14], "−3 − (−11) = 8 degrees colder.", "°C"),
             ("A gas tank has 12.5 gallons. A trip uses 7.8 gallons. How much is left?", F("4.7"), [F("20.3"), F("5.3"), F("4.3")], "12.5 − 7.8 = 4.7 gallons.", " gal"),
             ("A bank account changes by −$45 and then by +$62. What is the total change?", 17, [-107, 107, -17], "−45 + 62 = 17, so +$17.", "")]
    for q, v, ws, e, u in quick:
        if u == "" and "$" in q:
            its.append(item(q, v, ws, e, show=money))
        else:
            its.append(item(q, v, ws, e, unit=u))
    return {"title": "Choose the operation", "items": its}


# ------------------------------------------------------------ set 2: integers
def set_integers():
    its = []
    temps = [(-8, 15), (5, -12), (-14, 9), (-3, -7), (11, -20)]
    for a, ch in temps:
        b = a + ch
        word = "rises %d degrees" % ch if ch > 0 else "falls %d degrees" % -ch
        its.append(item("At 6 a.m. it is %s°F. By noon the temperature %s. What is the temperature at noon?" % (n(a), word), b,
                        [a - ch, -b, abs(a) + abs(ch)], "%s + %s = %s°F." % (n(a), ("(%s)" % n(ch)) if ch < 0 else n(ch), n(b)), unit="°F"))
    dists = [(14, -6), (-25, 40), (-3, -18), (120, -45)]
    for a, b in dists:
        d = abs(a - b)
        its.append(item("Point A is at %s m and point B is at %s m on a number line. How far apart are they?" % (n(a), n(b)), d,
                        [abs(a + b), a + b, -d], "Distance = |%s − %s| = |%s| = %s m." % (n(a), ("(%s)" % n(b)) if b < 0 else n(b), n(a - b), n(d)), unit=" m"))
    golf = [([-2, 1, -1, 0, -3], "golf scores (strokes compared to par)"), ([5, -8, 3, -6], "yards gained and lost on four plays")]
    for vals, what in golf:
        s = sum(vals)
        its.append(item("The %s are %s. What is the total?" % (what, ", ".join(n(v) for v in vals)), s,
                        [sum(abs(v) for v in vals), -s, sum(v for v in vals if v > 0)], "Add them in order: the total is %s." % n(s)))
    for loss, days in [(4, 6), (12, 5), (7, 8)]:
        its.append(item("A pond's water level drops %d cm a day for %d days. What is the total change in the level?" % (loss, days), -loss * days,
                        [loss * days, -(loss + days), -loss], "%d × (−%d) = −%d cm." % (days, loss, loss * days), unit=" cm"))
    for tot, k in [(-56, 7), (-90, 6), (-144, 12)]:
        its.append(item("A company lost $%d over %d months, the same amount each month. What was the change each month?" % (abs(tot), k), F(tot, k),
                        [F(-tot, k), tot * k, tot + k], "%s ÷ %d = %s, a loss of %s a month." % (n(tot), k, n(F(tot, k)), money(F(-tot, k))), show=money))
    its.append(item("A diver goes down 8 feet a minute from the surface. Where is she after 6 minutes?", -48, [48, -14, -2], "6 × (−8) = −48 feet.", unit=" ft"))
    its.append(item("The temperature changed by −18°F in 6 hours at a steady rate. What was the change each hour?", -3, [3, -108, -12], "−18 ÷ 6 = −3°F per hour.", unit="°F"))
    its.append(item("Four friends each have a game card balance of −$5. What is their total balance?", -20, [20, -9, -1],
                    "4 × (−5) = −20, so −$20.", show=money))
    return {"title": "Integer word problems", "items": its}


# ------------------------------------------------------------ set 3: decimals
def set_decimals():
    its = []
    shop = [("Ava buys 3 notebooks at $2.45 each. How much does she spend?", F("7.35"), [F("5.45"), F("2.45") * 30, F("0.8166")]),
            ("Gas costs $3.59 a gallon. How much do 12 gallons cost?", F("43.08"), [F("15.59"), F("4.308"), F("430.8")]),
            ("A 4.5 kg bag of rice is split equally into 6 containers. How much rice is in each?", F("0.75"), [F("27"), F("1.5"), F("1.33")]),
            ("A plant was 12.6 cm tall. It grew 0.35 cm a day for 8 days. How tall is it now?", F("15.4"), [F("12.95"), F("2.8"), F("16.4")]),
            ("A runner's times were 12.4 s, 11.9 s and 12.3 s. What is the mean time?", F("12.2"), [F("36.6"), F("12.4"), F("12.1")]),
            ]
    es = ["3 × 2.45 = $7.35.", "12 × 3.59 = $43.08.", "4.5 ÷ 6 = 0.75 kg.", "0.35 × 8 = 2.8 cm. 12.6 + 2.8 = 15.4 cm.", "12.4 + 11.9 + 12.3 = 36.6. 36.6 ÷ 3 = 12.2 s."]
    units = ["$", "$", " kg", " cm", " s"]
    for (q, v, ws), e, u in zip(shop, es, units):
        ws = [w for w in ws if num(F(w)) is not None]
        its.append(item(q, v, ws, e, show=money) if u == "$" else item(q, v, ws, e, unit=u))
    acct = [(F("125.50"), [F("-48.25"), F("-30"), F("62.10")]), (F("-12.40"), [F("50"), F("-8.75")]), (F("80"), [F("-23.99"), F("-23.99"), F("-23.99")])]
    for start, chs in acct:
        end = start + sum(chs)
        desc = ", ".join(("a deposit of " + money(c)) if c > 0 else ("a payment of " + money(-c)) for c in chs)
        its.append(item("An account starts at %s. Then there is %s. What is the balance?" % (money(start), desc), end,
                        [start - sum(chs), start + sum(abs(c) for c in chs), sum(chs)],
                        "%s %s = %s." % (money(start), " ".join(("+ " + money(c)) if c > 0 else ("− " + money(-c)) for c in chs), money(end)), show=money))
    temps = [(F("-2.5"), F("4.8"), "rises"), (F("1.4"), F("3.9"), "falls"), (F("-6.2"), F("1.7"), "falls")]
    for a, c, w in temps:
        b = a + c if w == "rises" else a - c
        its.append(item("The temperature is %s°C. It %s %s degrees. What is the new temperature?" % (n(a), w, n(c)), b,
                        [a - c if w == "rises" else a + c, -b, abs(a) + c], "%s %s %s = %s°C." % (n(a), "+" if w == "rises" else "−", n(c), n(b)), unit="°C"))
    rates = [("A car uses 0.04 gallons of gas per mile. How much gas does it use in 250 miles?", 10, [F("6250"), F("0.1"), 100], "0.04 × 250 = 10 gallons.", " gal"),
             ("A printer uses 2.5 mL of ink per page. How many pages can it print with 60 mL?", 24, [150, F("57.5"), F("2.4")], "60 ÷ 2.5 = 24 pages.", " pages"),
             ("A hose fills a 37.5-liter tank in 2.5 minutes. How many liters per minute?", 15, [F("93.75"), 35, F("1.5")], "37.5 ÷ 2.5 = 15 liters per minute.", " L"),
             ("A store marks down a $24.80 shirt by $6.95. What is the new price?", F("17.85"), [F("31.75"), F("18.85"), F("17.15")], "24.80 − 6.95 = $17.85.", "$"),
             ("A pizza costs $18.60. Four friends split it equally. How much does each pay?", F("4.65"), [F("74.40"), F("14.6"), F("4.6")], "18.60 ÷ 4 = $4.65.", "$"),
             ("A 1.8 m ribbon is cut into pieces 0.15 m long. How many pieces?", 12, [F("0.27"), F("1.2"), 120], "1.8 ÷ 0.15 = 12 pieces.", " pieces"),
             ("A swimmer's lap times went from 48.3 s to 45.9 s. By how much did the time change?", F("-2.4"), [F("2.4"), F("94.2"), F("-3.4")],
              "45.9 − 48.3 = −2.4 s (faster).", " s"),
             ("Ben earns $11.25 an hour and works 6 hours. How much does he earn?", F("67.5"), [F("17.25"), F("675"), F("56.25")],
              "11.25 × 6 = $67.50.", "$"),
             ("A water tank holds 120.6 L. It leaks 0.9 L each hour. How many hours until it is empty?", 134, [F("108.54"), F("121.5"), F("13.4")], "120.6 ÷ 0.9 = 134 hours.", " hours")]
    for q, v, ws, e, u in rates:
        if u == "$":
            its.append(item(q, v, [w for w in ws if num(F(w)) is not None], e, show=money if F(v) * 100 == int(F(v) * 100) else (lambda x: "$" + n(x))))
        else:
            its.append(item(q, v, [w for w in ws if num(F(w)) is not None], e, unit=u))
    return {"title": "Decimal word problems", "items": its[:20]}


# ------------------------------------------------------------ set 4: fractions
def set_fractions():
    its = []
    fq = [("A recipe uses 2/3 cup of sugar. Mia makes 4 batches. How much sugar does she need?", F(8, 3), [F(2, 12), F(14, 3), 6], "4 × 2/3 = 8/3 = 2 2/3 cups.", " cups"),
          ("A 5-yard rope is cut into pieces 5/8 yard long. How many pieces?", 8, [F(25, 8), F(1, 8), F(45, 8)], "5 ÷ 5/8 = 5 × 8/5 = 8 pieces.", " pieces"),
          ("Leo walked 1 3/4 miles, then 2 1/2 miles. How far did he walk?", F(17, 4), [F(13, 4), F(3, 4), F(35, 8)], "1 3/4 + 2 1/2 = 1 3/4 + 2 2/4 = 4 1/4 miles.", " miles"),
          ("A board is 8 1/2 feet long. Kai cuts off 2 3/4 feet. How long is the rest?", F(23, 4), [F(45, 4), F(27, 4), F(21, 4)], "8 1/2 − 2 3/4 = 8 2/4 − 2 3/4 = 5 3/4 feet.", " ft"),
          ("A tank is 3/5 full. 1/4 of the water in it is used. What fraction of the tank is used?", F(3, 20), [F(7, 20), F(12, 5), F(4, 9)], "1/4 of 3/5 = 1/4 × 3/5 = 3/20.", ""),
          ("3/4 of a pizza is shared equally by 3 friends. How much does each get?", F(1, 4), [F(9, 4), F(3, 7), F(4, 9)], "3/4 ÷ 3 = 1/4 of the pizza each.", ""),
          ("The temperature was −2 1/2°F and rose 5 3/4 degrees. What is it now?", F(13, 4), [F(-33, 4), F(33, 4), F(-13, 4)], "−2 1/2 + 5 3/4 = 3 1/4°F.", "°F"),
          ("A hiker is at −1/2 mile below a ridge and climbs 3/4 mile. Where is she compared to the ridge?", F(1, 4), [F(-5, 4), F(5, 4), F(-1, 4)],
           "−1/2 + 3/4 = −2/4 + 3/4 = 1/4 mile above the ridge.", " miles"),
          ("A stock's price changed by −3/8 dollar each day for 4 days. What was the total change?", F(-3, 2), [F(3, 2), F(-3, 32), F(-13, 8)],
           "4 × (−3/8) = −12/8 = −1 1/2 dollars.", " dollars"),
          ("A snail crawls 2/5 meter in 1/2 hour. How far does it crawl in 1 hour?", F(4, 5), [F(1, 5), F(9, 10), F(5, 4)], "2/5 ÷ 1/2 = 2/5 × 2 = 4/5 meter.", " m"),
          ("Ana read 1/3 of a book on Monday and 2/5 on Tuesday. What fraction is left?", F(4, 15), [F(11, 15), F(3, 8), F(5, 8)], "1/3 + 2/5 = 5/15 + 6/15 = 11/15 read. 1 − 11/15 = 4/15 left.", ""),
          ("A water bottle holds 3/4 liter. How many bottles fill a 6-liter jug?", 8, [F(9, 2), F(1, 8), F(27, 4)], "6 ÷ 3/4 = 6 × 4/3 = 8 bottles.", " bottles"),
          ("A garden is 4 1/2 m long and 2 2/3 m wide. What is its area?", 12, [F(43, 6), F(26, 3), F(27, 16)], "4 1/2 × 2 2/3 = 9/2 × 8/3 = 72/6 = 12 m².", " m²"),
          ("A cook uses 1/8 of a bag of flour a day. How many days does 3/4 of a bag last?", 6, [F(3, 32), F(7, 8), F(1, 6)], "3/4 ÷ 1/8 = 3/4 × 8 = 6 days.", " days"),
          ("A diver at −12 1/2 feet rises 4 3/4 feet. What is her new position?", F(-31, 4), [F(-69, 4), F(31, 4), F(-35, 4)], "−12 1/2 + 4 3/4 = −7 3/4 feet.", " ft"),
          ("A loss of 2 1/4 points is split equally over 3 rounds. What is the change each round?", F(-3, 4), [F(3, 4), F(-27, 4), F(-1, 4)], "−2 1/4 ÷ 3 = −9/4 ÷ 3 = −3/4 point.", " points"),
          ("A cake recipe uses 2 1/4 cups of flour. You make 1/3 of the recipe. How much flour do you need?", F(3, 4), [F(27, 4), F(7, 12), F(1, 4)], "1/3 × 2 1/4 = 1/3 × 9/4 = 3/4 cup.", " cups"),
          ("A jogger runs 3 1/3 miles in 2/3 hour. What is her speed?", 5, [F(20, 9), F(11, 3), 2], "3 1/3 ÷ 2/3 = 10/3 × 3/2 = 5 miles per hour.", " mph"),
          ("The level of a lake changed by −1 1/2 inches in March and +3/4 inch in April. What was the total change?", F(-3, 4), [F(-9, 4), F(9, 4), F(3, 4)],
           "−1 1/2 + 3/4 = −6/4 + 3/4 = −3/4 inch.", " inches"),
          ("A 2/3-acre field is split into 4 equal plots. How big is each plot?", F(1, 6), [F(8, 3), F(2, 7), F(3, 8)], "2/3 ÷ 4 = 2/12 = 1/6 acre.", " acre")]
    for q, v, ws, e, u in fq:
        q2 = q
        its.append(item(q2, v, ws, e, unit=u, st="f"))
    return {"title": "Fraction and mixed-number word problems", "items": its}


# ------------------------------------------------------------ set 5: multi-step
def set_multistep():
    its = []
    ms = [
        ("Ruby has $50. She buys 3 books at $8.75 each and a $4.50 bookmark. How much money is left?", F("19.25"), [F("30.75"), F("36.75"), F("14.75")],
         "3 × 8.75 = 26.25. 26.25 + 4.50 = 30.75. 50 − 30.75 = $19.25. Not $30.75: that is what she spent.", "$"),
        ("The temperature at midnight was −6°F. It rose 2.5°F each hour for 6 hours. What was the temperature then?", 9, [-21, 15, F("-3.5")],
         "6 × 2.5 = 15 degrees warmer. −6 + 15 = 9°F.", "°F"),
        ("A diver starts at the surface. She goes down 15 feet, rises 6 feet, then goes down 22 feet. Where is she?", -31, [43, -43, 31],
         "−15 + 6 + (−22) = −31 feet.", " ft"),
        ("A store had 240 shirts. It sold 3/8 of them on Monday and 50 on Tuesday. How many are left?", 100, [190, 150, 140],
         "3/8 × 240 = 90 sold Monday. 240 − 90 − 50 = 100 left.", " shirts"),
        ("A phone plan costs $35 a month plus $0.15 per text. Last month, 120 texts were sent. What was the bill?", 53, [F("35.15"), 18, F("53.15")],
         "0.15 × 120 = $18. 35 + 18 = $53.", "$"),
        ("Omar's account had −$22.50. He deposited $40, then spent $12.75. What is his balance?", F("4.75"), [F("-30.25"), F("75.25"), F("17.5")],
         "−22.50 + 40 − 12.75 = $4.75.", "$"),
        ("A plane is at 32,000 feet. It descends 1,500 feet a minute for 8 minutes. What is its altitude?", 20000, [44000, 30500, 12000],
         "8 × 1,500 = 12,000 feet down. 32,000 − 12,000 = 20,000 feet.", " ft"),
        ("Three friends share a $27.60 bill equally and each adds a $1.50 tip. How much does each pay?", F("10.7"), [F("9.2"), F("29.1"), F("12.2")],
         "27.60 ÷ 3 = 9.20. 9.20 + 1.50 = $10.70.", "$"),
        ("A recipe needs 2 1/4 cups of flour for 12 cookies. How much flour for 30 cookies?", F(45, 8), [F(27, 4), F(9, 2), F(21, 4)],
         "Per cookie: 9/4 ÷ 12 = 3/16 cup. 30 × 3/16 = 90/16 = 5 5/8 cups.", " cups"),
        ("The low temperatures for 5 days were −3, 2, −6, −1 and 3 (°C). What was the mean low?", -1, [-5, 3, F("-2.6")],
         "−3 + 2 − 6 − 1 + 3 = −5. −5 ÷ 5 = −1°C.", "°C"),
        ("A tank holds 60 gallons and is 3/4 full. It drains 2.5 gallons a minute. How long until it is empty?", 18, [24, F("112.5"), 15],
         "3/4 × 60 = 45 gallons. 45 ÷ 2.5 = 18 minutes.", " min"),
        ("A shirt costs $24. It is 25% off, then $3 more is taken off. What is the price?", 15, [21, 18, 3],
         "25% of 24 = 6. 24 − 6 = 18. 18 − 3 = $15.", "$"),
        ("A climber is at 2,450 m. She climbs up 380 m, then down 615 m. What is her elevation?", 2215, [3445, 2685, 1455],
         "2,450 + 380 − 615 = 2,215 m.", " m"),
        ("Maya earns $12.50 an hour. She works 4 hours on Saturday and 3.5 hours on Sunday. She spends $40. How much is left?", F("53.75"), [F("93.75"), F("43.75"), F("63.75")],
         "4 + 3.5 = 7.5 hours. 7.5 × 12.50 = 93.75. 93.75 − 40 = $53.75.", "$"),
        ("A submarine at −180 m rises 2/3 of the way to the surface. What is its new depth?", -60, [-120, 60, -300],
         "2/3 of 180 = 120 m up. −180 + 120 = −60 m.", " m"),
        ("A school raised $1,250. It spent 2/5 on books and $180 on snacks. How much is left?", 570, [750, 320, 930],
         "2/5 × 1,250 = 500. 1,250 − 500 − 180 = $570.", "$"),
        ("A runner ran 3.2 km on Monday, 4 3/4 km on Wednesday and 5.05 km on Friday. How far did she run?", 13, [F("12.95"), F("12.45"), F("13.5")],
         "4 3/4 = 4.75. 3.2 + 4.75 + 5.05 = 13 km.", " km"),
        ("A stock opened at $45.20. It fell $2.35, rose $1.80, then fell $3.15. What was its closing price?", F("41.5"), [F("52.5"), F("47.85"), F("44.65")],
         "45.20 − 2.35 + 1.80 − 3.15 = $41.50.", "$"),
        ("The temperature fell from 8°F to −10°F in 4 1/2 hours at a steady rate. What was the change per hour?", -4, [4, F("-4.5"), -2],
         "Change = −10 − 8 = −18 degrees. −18 ÷ 4 1/2 = −18 ÷ 9/2 = −4°F per hour.", "°F"),
        ("A board 10 1/2 feet long is cut into 6 equal pieces, and 1/4 foot is trimmed from each. How long is each piece now?", F(3, 2), [F(7, 4), F(2, 1), F(5, 4)],
         "10 1/2 ÷ 6 = 21/2 ÷ 6 = 7/4 = 1 3/4 feet. 1 3/4 − 1/4 = 1 1/2 feet.", " ft"),
    ]
    for q, v, ws, e, u in ms:
        if u == "$":
            its.append(item(q, v, [w for w in ws if num(F(w)) is not None], e, show=money))
        else:
            its.append(item(q, v, ws, e, unit=u, st="f" if (F(v).denominator > 1 and num(F(v)) is None) or "cups" in u else "d"))
    return {"title": "Multi-step problems", "items": its}


def body():
    rows = [["Rises, gains, deposits", "add a positive", "−4 + 9 = 5"],
            ["Falls, loses, spends", "add a negative (or subtract)", "−4 + (−6) = −10"],
            ["Difference or distance", "subtract (distance is never negative)", "12 − (−5) = 17"],
            ["The same change many times", "multiply", "5 × (−3) = −15"],
            ["Share or split equally, how many groups", "divide", "−24 ÷ 4 = −6, 6 ÷ " + fr(3, 4) + " = 8"]]
    return ("<h2>Plan, then compute</h2><p>Read the problem and decide what each number means. Give gains a + sign and losses a − sign. "
            "Choose the operation from the words, then use the rules for integers, decimals and fractions.</p>"
            + table(["Words in the problem", "Operation", "Example"], rows)
            + example("The temperature is −6°F. It rises 2.5°F each hour for 6 hours. What is it then?",
                      ["The change is 6 × 2.5 = 15 degrees.", "Add it to the start: −6 + 15 = 9."], "9°F")
            + example("Ruby has $50. She buys 3 books at $8.75 and a $4.50 bookmark. How much is left?",
                      ["Books: 3 × 8.75 = 26.25.", "Spent: 26.25 + 4.50 = 30.75.", "Left: 50 − 30.75 = 19.25."], "$19.25")
            + "<h2>Check your answer</h2><p>Estimate first: 3 books at about $9 is about $27, so about $18 to $20 is left. "
            "Check the sign: is the answer above or below zero, a gain or a loss?</p>"
            + "<h2>Common mistakes</h2><ul><li>Wrong sign: a fall of 6 degrees from −4 is −10, not 2.</li>"
            "<li>Stopping early: the question asks what is left, not what was spent.</li>"
            "<li>Dividing the wrong way: how many " + fr(3, 4) + "-foot pieces in 6 feet is 6 ÷ " + fr(3, 4) + ", not " + fr(3, 4) + " ÷ 6.</li></ul>")


def fx(t):
    """Write 2 1/4 and 3/4 as stacked fractions."""
    t = re.sub(r"(\d+) (\d+)/(\d+)", lambda m: m.group(1) + " " + fr(m.group(2), m.group(3)), t)
    return re.sub(r"(?<![\d/>])(\d+)/(\d+)(?![\d/])", lambda m: fr(m.group(1), m.group(2)), t)


def main():
    sets = [set_operation(), set_integers(), set_decimals(), set_fractions(), set_multistep()]
    for st in sets:
        for it in st["items"]:
            it["q"] = fx(it["q"])
            it["e"] = fx(it["e"])
            it["c"] = [fx(c) for c in it["c"]]
    balance(sets, R)
    unit = {
        "slug": "rational-number-word-problems",
        "title": "Rational Number Word Problems",
        "seo_title": "Grade 7 Rational Number Word Problems Worksheets: Integers, Decimals and Fractions",
        "short_title": "Rational number word problems",
        "domain": "The Number System",
        "standard_code": "7.NS.A.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/NS/A/3/",
        "standard_text": "Solve real-world and mathematical problems involving the four operations with rational numbers.",
        "meta_desc": "Free Grade 7 rational number word problems worksheets: choose the operation, then solve problems with integers, decimals, fractions and mixed numbers, including multi-step problems with money, temperature and elevation. 100 practice questions with an answer key.",
        "key_big": "Give each number a sign, choose the operation from the words, then solve.",
        "key_sub": "Gains are positive and losses are negative. Estimate first and check the sign of your answer.",
        "body_html": body(),
        "faq": [
            {"q": "How do I know which operation to use?", "a": "Look at what the words mean. Rises, gains and deposits add; falls and losses add a negative; the same change many times multiplies; sharing equally divides."},
            {"q": "What is a rational number?", "a": "Any number that can be written as a fraction of two integers, such as −4, 2.5 (5/2) and −3/4."},
            {"q": "How can I check my answer?", "a": "Estimate with rounded numbers, check that the sign makes sense (above or below zero), and make sure you answered the question that was asked."},
            {"q": "How do I solve a multi-step problem?", "a": "Break it into steps. Find each part, write it down, then combine. Ruby's books cost 3 × 8.75 = 26.25, then add the bookmark, then subtract from $50."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 12,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
