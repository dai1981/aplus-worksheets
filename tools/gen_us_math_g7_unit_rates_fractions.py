# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Unit Rates with Fractions (7.RP.A.1)
  python tools/gen_us_math_g7_unit_rates_fractions.py
Unit rates from ratios of fractions (complex fractions), such as 1/2 mile in 1/4 hour.
Wrong answers come from real mistakes: dividing in the wrong order (time ÷ distance),
multiplying the two fractions instead of dividing, and dividing only the numerators.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, table, example, write_unit, fr)

R = random.Random(71101)
UPDATED = "2026-11-09"


def q(v):
    """Simplest form; mixed numbers above 1; whole numbers plain."""
    v = F(v)
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    if w == 0:
        return fr(r, v.denominator)
    return "%d %s" % (w, fr(r, v.denominator))


def rq(v):
    """Reciprocal-style fraction, kept improper: 4/3, not 1 1/3."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else fr(v.numerator, v.denominator)


def unit_for(w, unit):
    """1 cup, not 1 cups."""
    if w == 1 and unit.endswith("s") and unit.strip() not in ("mph",):
        return unit[:-1]
    return unit


def plural(what):
    if what.startswith("of ") or what.endswith("s"):
        return what
    return {"inch": "inches"}.get(what, what + "s")


def money(v):
    s_ = num(F(v))
    if "." in s_:
        a_, b_ = s_.split(".")
        s_ = a_ + "." + (b_ + "0")[:2]
    return "$" + s_


def mc(question, v, ws, e, unit=""):
    v = F(v)
    d = v.denominator
    extra = [v * 2, v / 2, v + 1]
    cands = []
    for w in list(ws) + extra:
        w = F(w)
        if w > 0 and w != v:
            cands.append((q(w) + unit_for(w, unit), w))
    return mcq(question, (q(v) + unit_for(v, unit), v), cands, e)


def rate_item(a, b, what, per, unit_label, text_):
    """a of `what` in b of `per`: rate = a ÷ b."""
    a, b = F(a), F(b)
    r = a / b
    e = "Unit rate = %s ÷ %s = %s × %s = %s %s per %s." % (q(a), q(b), q(a), rq(1 / b), q(r), plural(what) if r != 1 else what, per)
    e += " Not %s: that divides the %ss by the %s, the wrong way round." % (q(b / a), per, plural(what)) if b / a != r else ""
    return mc(text_, r, [b / a, a * b, F(a.numerator, b.numerator) if b.numerator else r + 1], e, unit_label)


# ------------------------------------------------------------ set 1
def set_whole():
    its = []
    cases = [  # (amount, time, question)
        (F(1, 2), 2, "A snail crawls %s meter in 2 minutes. How many meters does it crawl per minute?", "meters", "minute", " m"),
        (6, F(1, 2), "A printer prints 6 pages in %s minute. How many pages per minute?", "pages", "minute", " pages"),
        (10, F(2, 3), "A runner goes 10 laps in %s hour. How many laps per hour?", "laps", "hour", " laps"),
        (F(3, 4), 3, "A plant grows %s inch in 3 weeks. How many inches per week?", "inches", "week", " in."),
        (5, F(1, 4), "A machine fills 5 bottles in %s minute. How many bottles per minute?", "bottles", "minute", " bottles"),
        (F(2, 5), 4, "A tap drips %s liter in 4 hours. How many liters per hour?", "liters", "hour", " L"),
        (12, F(3, 4), "Leo reads 12 pages in %s hour. How many pages per hour?", "pages", "hour", " pages"),
        (F(9, 10), 3, "A worker paints %s of a fence in 3 hours. What fraction of the fence per hour?", "of the fence", "hour", ""),
        (8, F(2, 5), "A pump moves 8 gallons in %s minute. How many gallons per minute?", "gallons", "minute", " gal"),
        (F(5, 6), 5, "A recipe uses %s cup of sugar for 5 muffins. How much sugar per muffin?", "cups", "muffin", " cup"),
    ]
    for a, b, t, what, per, u in cases:
        its.append(rate_item(a, b, what, per, u, t % (q(a) if isinstance(a, F) and a.denominator > 1 else q(b))))
    # what is a unit rate
    its.append(mcq("What is a unit rate?", ("A rate for 1 unit of the second amount, like miles per 1 hour", "a"),
                   [("Any fraction less than 1", "b"), ("A rate where both numbers are whole numbers", "c"), ("The total amount", "d")],
                   "A unit rate tells how much for 1 unit: 60 miles per 1 hour, $3 per 1 pound."))
    its.append(mcq("To find miles per hour, which do you divide?", ("miles ÷ hours", "a"), [("hours ÷ miles", "b"), ("miles × hours", "c"), ("miles + hours", "d")],
                   "The rate is the first unit per the second unit: miles ÷ hours."))
    its.append(mcq("Which is the same as %s?" % B("%s ÷ %s" % (fr(1, 2), fr(1, 4))), ("%s × 4" % fr(1, 2), "a"),
                   [("%s × %s" % (fr(1, 2), fr(1, 4)), "b"), ("2 × %s" % fr(1, 4), "c"), ("%s ÷ 4" % fr(1, 2), "d")],
                   "Dividing by a fraction is the same as multiplying by its reciprocal: ÷ 1/4 is × 4."))
    for a, b in [(F(1, 2), F(1, 4)), (F(2, 3), F(1, 6)), (F(3, 4), F(3, 8)), (F(1, 3), F(1, 2)), (F(5, 6), F(5, 12)), (F(1, 4), F(2, 3)), (F(7, 8), F(1, 4))]:
        r = a / b
        its.append(mc("Find %s." % B("%s ÷ %s" % (q(a), q(b))), r, [b / a, a * b, F(a.numerator, b.numerator)],
                      "Multiply by the reciprocal: %s × %s = %s. Not %s: that multiplies without flipping." % (q(a), rq(1 / b), q(r), q(a * b))))
    return {"title": "Dividing fractions for a unit rate", "items": its[:20]}


# ------------------------------------------------------------ set 2
def set_complex():
    its = []
    cases = [(F(1, 2), F(1, 4), "mile", "hour", "Maya walks %s mile in %s hour. What is her speed in miles per hour?", " mph"),
             (F(3, 4), F(1, 2), "mile", "hour", "A turtle swims %s mile in %s hour. How many miles per hour is that?", " mph"),
             (F(2, 3), F(1, 3), "cup", "batch", "A recipe uses %s cup of flour for %s batch. How many cups for 1 batch?", " cups"),
             (F(1, 4), F(1, 6), "gallon", "minute", "A hose fills %s gallon in %s minute. How many gallons per minute?", " gal"),
             (F(5, 8), F(1, 4), "pound", "dollar", "You get %s pound of nuts for %s dollar. How many pounds per dollar?", " lb"),
             (F(3, 5), F(3, 4), "kilometer", "hour", "A hiker walks %s kilometer in %s hour. How many kilometers per hour?", " km"),
             (F(1, 3), F(2, 3), "wall", "hour", "A painter paints %s of a wall in %s hour. How much of the wall per hour?", ""),
             (F(7, 10), F(1, 5), "liter", "minute", "A tank fills %s liter in %s minute. How many liters per minute?", " L"),
             (F(2, 5), F(1, 10), "mile", "minute", "A cyclist rides %s mile in %s minute. How many miles per minute?", " miles"),
             (F(1, 6), F(1, 4), "lawn", "hour", "Eli mows %s of a lawn in %s hour. How much of the lawn per hour?", ""),
             (F(9, 10), F(3, 10), "page", "minute", "A scanner scans %s page in %s minute. How many pages per minute?", " pages"),
             (F(3, 8), F(3, 4), "mile", "hour", "A slow robot moves %s mile in %s hour. How many miles per hour?", " mph"),
             (F(4, 5), F(2, 5), "pizza", "person", "%s of a pizza is shared by %s of the group. How much pizza per whole group?", " pizza"),
             (F(5, 6), F(2, 3), "mile", "hour", "A goat walks %s mile in %s hour. How many miles per hour?", " mph"),
             (F(1, 2), F(3, 4), "page", "minute", "Zoe types %s page in %s minute. How many pages per minute?", " page"),
             (F(3, 2), F(1, 2), "mile", "hour", "A boat travels %s miles in %s hour. How many miles per hour?", " mph"),
             (F(5, 4), F(5, 6), "cup", "batch", "Bread uses %s cups of water for %s batch. How many cups per batch?", " cups"),
             (F(2, 3), F(4, 9), "acre", "day", "A farmer plows %s acre in %s day. How many acres per day?", " acres"),
             (F(1, 8), F(1, 2), "inch", "week", "A vine grows %s inch in %s week. How many inches per week?", " in."),
             (F(9, 4), F(3, 4), "mile", "hour", "A jogger runs %s miles in %s hour. How many miles per hour?", " mph")]
    for a, b, what, per, t, u in cases:
        its.append(rate_item(a, b, what, per, u, t % (q(a), q(b))))
    its[12] = rate_item(F(4, 5), F(2, 5), "pound", "dollar", " lb", "You can buy %s pound of cheese for %s dollar. How many pounds per dollar?" % (q(F(4, 5)), q(F(2, 5))))
    return {"title": "Complex fractions: fraction ÷ fraction", "items": its}


# ------------------------------------------------------------ set 3
def set_compare():
    its = []
    pairs = [((F(1, 2), F(1, 4)), (F(3, 4), F(1, 2)), "Ava", "Ben", "miles", "hour"),
             ((F(2, 3), F(1, 3)), (F(5, 6), F(1, 2)), "Pump A", "Pump B", "gallons", "minute"),
             ((F(3, 4), F(1, 2)), (F(1, 2), F(1, 4)), "Kai", "Mia", "laps", "minute"),
             ((F(3, 5), F(1, 5)), (F(4, 5), F(2, 5)), "Printer A", "Printer B", "pages", "second"),
             ((F(1, 3), F(1, 6)), (F(1, 4), F(1, 12)), "Grace", "Omar", "miles", "minute"),
             ((F(5, 8), F(1, 4)), (F(3, 4), F(1, 3)), "Robot A", "Robot B", "meters", "second")]
    for (a1, b1), (a2, b2), n1, n2, what, per in pairs:
        r1, r2 = a1 / b1, a2 / b2
        if r1 == r2:
            continue
        fast = n1 if r1 > r2 else n2
        slow = n2 if fast == n1 else n1
        sg = lambda v, w: w[:-1] if v <= 1 else w
        its.append(mcq("%s does %s %s in %s %s. %s does %s %s in %s %s. Who has the greater unit rate?" % (
            n1, q(a1), sg(a1, what), q(b1), per, n2, q(a2), sg(a2, what), q(b2), per), (fast, "f"),
            [(slow, "s"), ("They are the same", "e"), ("It cannot be told", "c")],
            "%s: %s ÷ %s = %s %s per %s. %s: %s ÷ %s = %s %s per %s. %s is greater." % (
                n1, q(a1), q(b1), q(r1), what, per, n2, q(a2), q(b2), q(r2), what, per, q(max(r1, r2)))))
    # best buy
    buys = [("cereal", F(3, 4), F("3"), F(1, 2), F("2.4")), ("rice", F(5, 2), F("5"), F(3, 2), F("3.6")), ("cheese", F(1, 2), F("4"), F(3, 4), F("5.4"))]
    for item, w1, p1, w2, p2 in buys:
        u1, u2 = p1 / w1, p2 / w2
        lb = lambda w_: "pound" if w_ <= 1 else "pounds"
        better = "%s %s for %s" % (q(w1), lb(w1), money(p1)) if u1 < u2 else "%s %s for %s" % (q(w2), lb(w2), money(p2))
        worse = "%s %s for %s" % (q(w2), lb(w2), money(p2)) if u1 < u2 else "%s %s for %s" % (q(w1), lb(w1), money(p1))
        its.append(mcq("Which is the better buy for %s?" % item, (better, "b"), [(worse, "w"), ("They cost the same per pound", "s"), ("The bigger package is always better", "g")],
                       "Find the price per pound. %s ÷ %s = %s per pound. %s ÷ %s = %s per pound. The lower price per pound is the better buy." % (
                           num(p1), q(w1), money(u1), num(p2), q(w2), money(u2))))
    for a, b, k in [(F(1, 2), F(1, 3), 4), (F(3, 4), F(1, 4), 5), (F(2, 3), F(1, 6), F(3, 2)), (F(5, 6), F(1, 3), 2), (F(1, 4), F(1, 8), F(5, 2)),
                    (F(3, 5), F(3, 10), 6), (F(7, 8), F(1, 2), 4), (F(2, 5), F(1, 5), F(7, 2)), (F(1, 3), F(1, 9), 3), (F(4, 9), F(2, 3), 6),
                    (F(9, 10), F(3, 5), 2)]:
        r = a / b
        tot = r * k
        its.append(mc("A machine makes %s of a part in %s hour. At this rate, how many parts does it make in %s hours?" % (q(a), q(b), q(k)), tot,
                      [a * k, r + k, F(k) / r],
                      "Unit rate: %s ÷ %s = %s parts per hour. %s × %s = %s parts." % (q(a), q(b), q(r), q(r), q(k), q(tot)), " parts"))
    return {"title": "Compare rates and use them", "items": its[:20]}


# ------------------------------------------------------------ set 4
def set_mixed_units():
    its = []
    cases = [(F(5, 2), F(1, 2), "A car uses %s gallons of gas in %s hour. How many gallons per hour?", " gal"),
             (F(7, 2), F(7, 4), "Ana jogs %s miles in %s hours. How many miles per hour?", " mph"),
             (F(15, 4), F(5, 4), "A train goes %s miles in %s minutes. How many miles per minute?", " miles"),
             (F(10, 3), F(5, 6), "A baker uses %s cups of flour for %s of a batch. How many cups per batch?", " cups"),
             (F(9, 2), F(3, 2), "A sprinkler uses %s gallons in %s minutes. How many gallons per minute?", " gal"),
             (F(11, 4), F(1, 2), "Sam walks %s miles in %s hour. How many miles per hour?", " mph"),
             (F(8, 3), F(4, 3), "A painter uses %s gallons of paint for %s rooms. How many gallons per room?", " gal"),
             (F(25, 4), F(5, 2), "A farmer picks %s bushels in %s hours. How many bushels per hour?", " bushels"),
             (F(7, 3), F(7, 6), "A cook uses %s pounds of beef for %s batches. How many pounds per batch?", " lb"),
             (F(13, 2), F(13, 4), "A cyclist rides %s km in %s minutes. How many km per minute?", " km")]
    for a, b, t, u in cases:
        r = a / b
        its.append(mc(t % (q(a), q(b)), r, [b / a, a * b, a - b], "%s ÷ %s = %s × %s = %s." % (q(a), q(b), rq(a), rq(1 / b), q(r)), u))
    for amt, rate, t, u in [(12, F(3, 4), "A printer prints %s pages per minute. How many minutes does it take to print 12 pages?", " min"),
                            (5, F(5, 4), "A hiker walks %s miles per hour. How long does it take to walk 5 miles?", " hours"),
                            (6, F(3, 2), "A tap fills %s gallons per minute. How many minutes to fill 6 gallons?", " min"),
                            (F(9, 2), F(3, 4), "A recipe uses %s cup of oil per batch. How many batches can you make with 4 1/2 cups?", " batches"),
                            (10, F(5, 3), "A snail moves %s feet per hour. How many hours to move 10 feet?", " hours")]:
        tm = F(amt) / rate
        txt = t % q(rate)
        if "4 1/2" in txt:
            txt = txt.replace("4 1/2", q(F(9, 2)))
        its.append(mc(txt, tm, [F(amt) * rate, rate / F(amt), tm + 2], "Time = amount ÷ rate = %s ÷ %s = %s." % (q(amt), q(rate), q(tm)), u))
    its.append(mcq("A recipe uses 3/4 cup of milk for every 1/2 cup of flour. Which is the unit rate of milk per cup of flour?",
                   ("%s cups" % q(F(3, 2)), "a"), [("%s cup" % q(F(2, 3)), "b"), ("%s cup" % q(F(3, 8)), "c"), ("%s cups" % q(F(5, 4)), "d")],
                   "3/4 ÷ 1/2 = 3/4 × 2 = 1 1/2 cups of milk per cup of flour."))
    its.append(mcq("A rate is 2/3 mile per 1/6 hour. Which is an equivalent rate?", ("4 miles per hour", "a"),
                   [("%s mile per hour" % q(F(1, 9)), "b"), ("%s mile per hour" % q(F(1, 4)), "c"), ("3 miles per hour", "d")],
                   "2/3 ÷ 1/6 = 2/3 × 6 = 4 miles per hour."))
    its.append(mcq("A graph of distance vs. time passes through (1/2, 3). What is the unit rate?", ("6 per 1", "a"),
                   [("%s per 1" % q(F(1, 6)), "b"), ("%s per 1" % q(F(3, 2)), "c"), ("3 per 1", "d")],
                   "Unit rate = y ÷ x = 3 ÷ 1/2 = 6."))
    its.append(mcq("Water fills 1/5 of a tank in 1/3 hour. How long will it take to fill the whole tank?", ("%s hours" % q(F(5, 3)), "a"),
                   [("%s hour" % q(F(3, 5)), "b"), ("%s hour" % q(F(1, 15)), "c"), ("5 hours", "d")],
                   "Rate = 1/5 ÷ 1/3 = 3/5 tank per hour. Time = 1 ÷ 3/5 = 5/3 = 1 2/3 hours."))
    its.append(mcq("Which situation has a unit rate of 2?", ("%s mile in %s hour" % (q(F(1, 2)), q(F(1, 4))), "a"),
                   [("%s mile in %s hour" % (q(F(1, 4)), q(F(1, 2))), "b"), ("%s mile in %s hour" % (q(F(1, 3)), q(F(1, 3))), "c"),
                    ("%s mile in %s hour" % (q(F(2, 3)), q(F(1, 2))), "d")],
                   "1/2 ÷ 1/4 = 2. 1/4 ÷ 1/2 = 1/2, 1/3 ÷ 1/3 = 1 and 2/3 ÷ 1/2 = 4/3."))
    return {"title": "Mixed numbers and using rates", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)
    data = [
        ("%s jogs %s mile in %s hour. How far does %s jog in 1 hour?", F(3, 4), F(1, 6), " miles", "mile"),
        ("%s uses %s cup of paint to cover %s of a poster. How much paint is needed for the whole poster?", F(1, 3), F(2, 3), " cup", "cup"),
        ("%s reads %s of a book in %s hour. How much of the book does %s read per hour?", F(1, 5), F(2, 3), " of the book", "book"),
        ("%s pours %s liter of juice into %s of a pitcher. How many liters fill the whole pitcher?", F(3, 4), F(1, 2), " L", "liter"),
        ("%s cleans %s of a room in %s hour. How much of the room per hour?", F(2, 5), F(1, 2), " of the room", "room"),
    ]
    for t, a, b, u, what in data:
        name, he, his = P.next()
        if t.count("%s") == 4:
            text_ = t % (name, q(a), q(b), he)
        else:
            text_ = t % (name, q(a), q(b))
        r = a / b
        its.append(mc(text_, r, [b / a, a * b, a + b], "Divide: %s ÷ %s = %s × %s = %s." % (q(a), q(b), q(a), rq(1 / b), q(r)), u))
    more = [
        ("A car travels 45 miles in %s hour. What is its speed in miles per hour?" % q(F(3, 4)), 60, [F(135, 4), F(3, 4) / 45 + 0, 48], " mph"),
        ("A shower uses 5 gallons in %s minutes. How many gallons per minute?" % q(F(5, 2)), 2, [F(1, 2), F(25, 2), F(5, 2)], " gal"),
        ("A plane flies 1,200 miles in %s hours. How many miles per hour?" % q(F(5, 2)), 480, [3000, 600, 400], " mph"),
        ("A worker earns $54 for %s hours of work. How much per hour?" % q(F(9, 2)), 12, [243, 18, 9], ""),
        ("A garden hose fills a %s-gallon bucket in %s minute. How many gallons per minute?" % (q(F(5, 2)), q(F(1, 2))), 5, [F(5, 4), F(1, 5), 2], " gal"),
        ("A recipe needs %s cup of sugar for every %s cup of butter. How much sugar for 1 cup of butter?" % (q(F(2, 3)), q(F(1, 3))), 2, [F(2, 9), F(1, 2), 1], " cups"),
        ("A spider climbs %s meter in %s minute. At this rate, how far does it climb in 10 minutes?" % (q(F(1, 5)), q(F(1, 2))), 4, [1, F(1, 25), 20], " m"),
        ("Kai fills %s of a pool in %s hours. How long to fill the whole pool?" % (q(F(1, 4)), q(F(3, 2))), 6, [F(3, 8), F(1, 6), 4], " hours"),
        ("A ribbon %s yards long is cut into pieces %s yard long. How many pieces?" % (q(F(15, 4)), q(F(3, 4))), 5, [F(45, 16), F(1, 5), 4], " pieces"),
        ("A bird flies %s mile in %s minute. How many miles in 1 hour (60 minutes)?" % (q(F(1, 3)), q(F(1, 2))), 40, [10, F(2, 3), 20], " miles"),
        ("A store sells %s pound of grapes for $2. What is the price per pound?" % q(F(2, 3)), 3, [6, F("1.5"), 2], ""),
        ("A machine wraps %s of the gifts in %s hour. How long to wrap all of them?" % (q(F(3, 5)), q(F(3, 4))), F(5, 4), [F(4, 5), F(9, 20), 2], " hours"),
        ("Mia walks %s mile to school in %s hour. Ben walks %s mile in %s hour. How much faster is Ben, in miles per hour?" % (
            q(F(1, 2)), q(F(1, 4)), q(F(3, 4)), q(F(1, 4))), 1, [3, 2, F(1, 4)], " mph"),
        ("A faucet drips %s cup in %s hour. How many cups in a day (24 hours)?" % (q(F(1, 8)), q(F(1, 2))), 6, [F(3, 2), 3, F(1, 4)], " cups"),
        ("Paint costs $%s for %s gallon. How much for 3 gallons?" % ("9", q(F(3, 4))), 36, [F("20.25"), 12, F("6.75")], ""),
    ]
    for t, v, ws, u in more:
        if u == "":
            it = mcq(t, (money(v), F(v)), [(money(w), F(w)) for w in ws if F(w) != F(v)], "")
        else:
            it = mc(t, v, ws, "", u)
        its.append(it)
    explain = {0: "45 ÷ 3/4 = 45 × 4/3 = 60 mph.", 1: "5 ÷ 5/2 = 5 × 2/5 = 2 gallons per minute.", 2: "1,200 ÷ 5/2 = 1,200 × 2/5 = 480 mph.",
               3: "54 ÷ 9/2 = 54 × 2/9 = $12 per hour.", 4: "5/2 ÷ 1/2 = 5/2 × 2 = 5 gallons per minute.", 5: "2/3 ÷ 1/3 = 2 cups of sugar per cup of butter.",
               6: "1/5 ÷ 1/2 = 2/5 meter per minute. 2/5 × 10 = 4 meters.", 7: "1/4 ÷ 3/2 = 1/6 pool per hour, so the whole pool takes 6 hours.",
               8: "15/4 ÷ 3/4 = 15/4 × 4/3 = 5 pieces.", 9: "1/3 ÷ 1/2 = 2/3 mile per minute. 2/3 × 60 = 40 miles.",
               10: "2 ÷ 2/3 = 2 × 3/2 = $3 per pound. Not $6: that multiplies by 3 instead of 3/2.", 11: "3/5 ÷ 3/4 = 4/5 of the gifts per hour. 1 ÷ 4/5 = 5/4 = 1 1/4 hours.",
               12: "Mia: 1/2 ÷ 1/4 = 2 mph. Ben: 3/4 ÷ 1/4 = 3 mph. 3 − 2 = 1 mph faster.", 13: "1/8 ÷ 1/2 = 1/4 cup per hour. 1/4 × 24 = 6 cups.",
               14: "9 ÷ 3/4 = 9 × 4/3 = $12 per gallon. 12 × 3 = $36."}
    for k, e in explain.items():
        its[5 + k]["e"] = e
    return {"title": "Word problems", "items": its}


def body():
    rows = [["1/2 mile in 1/4 hour", "1/2 ÷ 1/4", "1/2 × 4", "2 miles per hour"],
            ["2/3 cup for 1/3 batch", "2/3 ÷ 1/3", "2/3 × 3", "2 cups per batch"],
            ["3/4 mile in 1/2 hour", "3/4 ÷ 1/2", "3/4 × 2", "1 1/2 miles per hour"]]
    return ("<h2>Unit rates with fractions</h2><p>A <b>unit rate</b> tells how much for <b>1</b> unit, like miles per 1 hour. "
            "Divide the first amount by the second. When the amounts are fractions, you get a <b>complex fraction</b>, a fraction divided by a fraction. "
            "Divide by multiplying by the reciprocal.</p>"
            + table(["Rate", "Divide", "Multiply by the reciprocal", "Unit rate"], rows)
            + example("Maya walks " + fr(1, 2) + " mile in " + fr(1, 4) + " hour. What is her speed?",
                      ["Miles ÷ hours: " + fr(1, 2) + " ÷ " + fr(1, 4) + ".", "Multiply by the reciprocal: " + fr(1, 2) + " × 4 = 2."], "2 miles per hour")
            + example("A painter covers " + fr(1, 3) + " of a wall in " + fr(2, 3) + " hour. How much per hour?",
                      [fr(1, 3) + " ÷ " + fr(2, 3) + " = " + fr(1, 3) + " × " + fr(3, 2) + " = " + fr(1, 2) + "."], fr(1, 2) + " of the wall per hour")
            + "<h2>Common mistakes</h2><ul><li>Dividing the wrong way: miles per hour is miles ÷ hours, not hours ÷ miles.</li>"
            "<li>Multiplying the fractions: " + fr(1, 2) + " ÷ " + fr(1, 4) + " is 2, not " + fr(1, 8) + ".</li>"
            "<li>Forgetting that a unit rate is for 1 unit: always divide by the second amount.</li></ul>")


def main():
    sets = [set_whole(), set_complex(), set_compare(), set_mixed_units(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "unit-rates-with-fractions",
        "title": "Unit Rates with Fractions",
        "seo_title": "Grade 7 Unit Rates with Fractions Worksheets: Complex Fractions and Rate Word Problems",
        "short_title": "Unit rates with fractions",
        "domain": "Ratios & Proportional Relationships",
        "standard_code": "7.RP.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/RP/A/1/",
        "standard_text": "Compute unit rates associated with ratios of fractions, including ratios of lengths, areas and other quantities measured in like or different units. For example, if a person walks 1/2 mile in each 1/4 hour, compute the unit rate as the complex fraction 1/2/1/4 miles per hour, equivalently 2 miles per hour.",
        "meta_desc": "Free Grade 7 unit rates with fractions worksheets: divide fractions to find unit rates, complex fractions, compare rates, best buys and real-world rate problems. 100 practice questions with an answer key.",
        "key_big": "Unit rate = first amount ÷ second amount. With fractions, multiply by the reciprocal.",
        "key_sub": "1/2 mile in 1/4 hour: 1/2 ÷ 1/4 = 1/2 × 4 = 2 miles per hour.",
        "body_html": body(),
        "faq": [
            {"q": "What is a unit rate?", "a": "A rate for one unit of the second amount, such as 60 miles per 1 hour or $3 per 1 pound."},
            {"q": "How do you find a unit rate with fractions?", "a": "Divide the first amount by the second. To divide by a fraction, multiply by its reciprocal: 1/2 ÷ 1/4 = 1/2 × 4 = 2."},
            {"q": "What is a complex fraction?", "a": "A fraction with a fraction in the numerator, the denominator or both, like (1/2)/(1/4). It means 1/2 ÷ 1/4."},
            {"q": "How do I compare two rates?", "a": "Find both unit rates and compare them. For prices, the lower price per unit is the better buy."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 11,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
