# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Rates (Australian Curriculum v9.0: AC9M8M05)
  python3 tools/gen_au_maths_y8_rates.py
Writing and simplifying rates, speed, distance and time, converting rates (km/h and m/s, per minute and per
hour), best buys by unit price, and problems such as fuel use and heart rates.
Wrong answers come from real mistakes: dividing the wrong way, treating minutes as decimals of an hour,
choosing the cheapest pack instead of the best value, and multiplying when converting should divide.
"""
import random
from fractions import Fraction as F
from au_hs import num, B, S, make, lesson, collect, QN, T, aud, dec

R = random.Random(81301)


def n(v):
    v = F(v)
    return num(v) if v.denominator == 1 else dec(v)


def hm(h):
    h = F(h)
    whole = int(h)
    mins = (h - whole) * 60
    parts = []
    if whole:
        parts.append("%d hour%s" % (whole, "" if whole == 1 else "s"))
    if mins:
        parts.append("%s minute%s" % (num(mins), "" if mins == 1 else "s"))
    return " ".join(parts) if parts else "0 minutes"


# ------------------------------------------------------------ set 1: unit rates
RATES = [
    ("A tap fills a %d L bucket in %d minutes.", "L/min", (10, 30), (2, 6)),
    ("A printer prints %d pages in %d minutes.", "pages/min", (60, 240), (3, 8)),
    ("Lachlan earns $%d for %d hours of work.", "$/h", (90, 260), (4, 10)),
    ("A heart beats %d times in %d minutes.", "beats/min", (140, 360), (2, 5)),
    ("A car uses %d L of fuel for %d00 km.", "L/100 km", (14, 48), (2, 6)),
    ("A shop sells %d kg of bananas for $%d.", "kg per $", None, None),
]


def one_unit(r):
    kind = r.randint(0, 4)
    tmpl, unit, (lo, hi), (tlo, thi) = RATES[kind]
    t = r.randint(tlo, thi)
    rate = r.randint(max(2, lo // t), hi // t)
    if kind == 2:
        rate = r.choice([22, 24, 25, 26, 28, 30, 32, 35])
    if kind == 4:
        rate = F(r.choice([6, 7, 8, 9, 10, 11, 12]))
    total = rate * t
    q = (tmpl % (total, t)) + " What is the rate in %s?" % B(unit)
    if kind == 2:
        q = (tmpl % (total, t)) + " What is his hourly rate of pay?"
        e = "Divide: $%s ÷ %d = <b>%s per hour</b>." % (num(total), t, aud(rate))
        return QN(q, rate, [total - t, total * t if total * t < 5000 else total + t, F(total, t + 1) if F(total, t + 1).denominator == 1 else None], e, fmt=aud, unit=" per hour")
    e = "Divide: %s ÷ %d = <b>%s %s</b>." % (num(total), t, num(rate), unit)
    return QN(q, rate, [F(t, total) if F(t, total) * 100 >= 1 else None, total * t if total * t < 5000 else total + t, total - t], e, unit=" " + unit)


# ------------------------------------------------------------ set 2: speed, distance and time
def one_sdt(r):
    kind = r.randint(0, 2)
    s = r.choice([5, 12, 15, 20, 40, 48, 50, 60, 64, 72, 80, 90, 100, 110])
    t = r.choice([F(1, 2), F(3, 4), 1, F(3, 2), 2, F(5, 2), 3, F(5, 4)])
    d = s * t
    if d.denominator != 1:
        return None
    who = "walker" if s <= 6 else "cyclist" if s <= 20 else r.choice(["car", "bus"]) if s <= 100 else "train"
    if kind == 0:
        q = "A %s travels %s km in %s. What is its average speed?" % (who, num(d), hm(t))
        wrong_dec = int(t) + (t - int(t)) * 60 / 100
        e = "Speed = distance ÷ time = %s ÷ %s = <b>%s km/h</b>." % (num(d), n(t), num(s))
        return QN(q, s, [d / wrong_dec if wrong_dec != t else None, d * t, F(t, d) * 100], e, unit=" km/h")
    if kind == 1:
        q = "A %s travels at %d km/h for %s. How far does it go?" % (who, s, hm(t))
        wrong_dec = int(t) + (t - int(t)) * 60 / 100
        e = "Distance = speed × time = %d × %s = <b>%s km</b>." % (s, n(t), num(d))
        return QN(q, d, [s * wrong_dec if wrong_dec != t else None, F(s) / t, s + t * 60], e, unit=" km")
    q = "A %s travels %s km at %d km/h. How long does the trip take?" % (who, num(d), s)
    right = hm(t)
    wrongs = [hm(t + 1), hm(t * 2), hm(t + F(1, 4))]
    if t != int(t):
        wrongs.insert(0, "%s hours" % n(t) if False else (("%d hour%s " % (int(t), "" if int(t) == 1 else "s") if int(t) else "") + "%d minutes" % int((t - int(t)) * 100)))
    e = "Time = distance ÷ speed = %s ÷ %d = %s hours = <b>%s</b>." % (num(d), s, n(t), right)
    return T(q, right, list(dict.fromkeys(w for w in wrongs if w != right))[:3], e)


# ------------------------------------------------------------ set 3: converting rates
def one_conv(r):
    kind = r.randint(0, 3)
    if kind == 0:
        kmh = r.choice([18, 36, 54, 72, 90, 108])
        ms = F(kmh * 1000, 3600)
        q = "Convert %s into metres per second." % B("%d km/h" % kmh)
        e = "%d km/h = %s m in 3600 s. %s ÷ 3600 = <b>%s m/s</b>." % (kmh, num(kmh * 1000), num(kmh * 1000), num(ms))
        return QN(q, ms, [kmh * F(36, 10), F(kmh, 60), F(kmh * 1000, 60)], e, unit=" m/s")
    if kind == 1:
        ms = r.choice([5, 10, 15, 20, 25, 30])
        kmh = ms * F(36, 10)
        q = "Convert %s into kilometres per hour." % B("%d m/s" % ms)
        e = "%d m/s × 3600 = %s m per hour = <b>%s km/h</b>." % (ms, num(ms * 3600), num(kmh))
        return QN(q, kmh, [F(ms * 10, 36), ms * 60, ms * 1000], e, unit=" km/h")
    if kind == 2:
        per_min = r.choice([12, 15, 18, 20, 25, 30, 45])
        q = "A pump moves %s. How many litres is this per hour?" % B("%d L per minute" % per_min)
        e = "There are 60 minutes in an hour: %d × 60 = <b>%s L/h</b>." % (per_min, num(per_min * 60))
        return QN(q, per_min * 60, [per_min * 100, F(per_min, 60), per_min * 24], e, unit=" L/h", near=(60, -60, 120))
    per_h = r.choice([30, 36, 42, 48, 54, 60])
    q = "A worker is paid %s. How much is this per minute?" % B("$%d per hour" % per_h)
    e = "%d ÷ 60 = <b>%s per minute</b>." % (per_h, aud(F(per_h, 60)))
    return QN(q, F(per_h, 60), [F(per_h, 100), per_h * 60, F(per_h, 6)], e, fmt=lambda v: aud(v) if F(v) >= 1 else "%dc" % int(round(F(v) * 100)), near=(F(1, 10), F(-1, 10)))


# ------------------------------------------------------------ set 4: best buys
ITEMS = [("Rice", "kg", [1, 2, 5], (250, 1200)), ("Yoghurt", "g", [500, 1000], (300, 900)),
         ("Orange juice", "L", [2, 3], (300, 900)), ("Cereal", "g", [500, 750], (400, 900)),
         ("Laundry liquid", "L", [1, 4], (600, 2600)), ("Coffee", "g", [200, 500], (900, 2600))]


def one_best(r):
    it, u, sizes, (lo, hi) = r.choice(ITEMS)
    s1, s2 = sizes[0], r.choice(sizes[1:])
    p1 = r.randint(lo // 10, hi // 10) * 10
    base = 100 if u == "g" else 1
    up1 = F(p1, s1) * base
    better_big = r.random() < 0.6
    for _ in range(60):
        f = r.uniform(0.75, 0.93) if better_big else r.uniform(1.07, 1.25)
        p2 = int(round(float(up1 * s2 / base) * f / 5.0)) * 5
        up2 = F(p2, s2) * base
        if p2 > p1 and up2 != up1 and ((up2 < up1) == better_big):
            break
    else:
        return None
    lab = lambda s: "1 kg" if (u, s) == ("g", 1000) else "%s %s" % (num(s), u)
    q = "%s comes in two sizes: %s for %s, or %s for %s. Which is better value?" % (it, lab(s1), aud(F(p1, 100)), lab(s2), aud(F(p2, 100)))
    right = "The %s pack" % lab(s2 if better_big else s1)
    other = "The %s pack" % lab(s1 if better_big else s2)
    per = "per %s %s" % (num(base), u) if base != 1 else "per %s" % u

    def pp(x):
        x = F(x) / 100
        c = int(round(float(x) * 100))
        return "$%d.%02d" % divmod(c, 100) if c >= 100 else "%dc" % c
    e = "Compare the price %s: %s and %s. <b>%s</b> costs less %s." % (per, pp(up1), pp(up2), right, per)
    return T(q, right, [other, "They are the same value", "You cannot tell without more information"], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A car uses 7.5 L of fuel per 100 km. How much fuel does it use on a 360 km trip?", "27 L", ["48 L", "2.7 L", "13.5 L"], "360 ÷ 100 = 3.6. 3.6 × 7.5 = <b>27 L</b>."),
        ("Fuel costs $1.90 per litre. How much does it cost to fill a 50 L tank?", "$95", ["$26.32", "$9.50", "$51.90"], "50 × 1.90 = <b>$95</b>."),
        ("Mia's heart beats 18 times in 15 seconds. What is her heart rate in beats per minute?", "72", ["270", "18", "60"], "There are 4 lots of 15 s in a minute: 18 × 4 = <b>72</b> beats per minute."),
        ("A train travels 240 km in 2 hours 30 minutes. What is its average speed?", "96 km/h", ["104 km/h", "120 km/h", "80 km/h"], "2 h 30 min = 2.5 h. 240 ÷ 2.5 = <b>96 km/h</b>."),
        ("A cyclist rides at 24 km/h for 40 minutes. How far does she ride?", "16 km", ["9.6 km", "960 km", "6 km"], "40 minutes = ⅔ hour. 24 × ⅔ = <b>16 km</b>."),
        ("Which is faster: 20 m/s or 70 km/h?", "20 m/s", ["70 km/h", "They are the same", "You cannot compare them"], "20 m/s = 72 km/h, which is faster than 70 km/h. So <b>20 m/s</b>."),
        ("A school uses 4500 L of water in 3 days. At this rate, how much does it use in a 5-day week?", "7500 L", ["1500 L", "22 500 L", "6000 L"], "4500 ÷ 3 = 1500 L per day. 1500 × 5 = <b>7500 L</b>."),
        ("Tomatoes cost $8.40 for 1.2 kg. What is the price per kilogram?", "$7", ["$10.08", "$8.40", "$6.80"], "8.40 ÷ 1.2 = <b>$7</b> per kg."),
        ("A phone plan gives 40 GB of data for $35 a month. Another gives 25 GB for $25. Which costs less per GB?", "The 40 GB plan", ["The 25 GB plan", "They cost the same per GB", "You cannot tell"],
         "40 GB: 35 ÷ 40 = 87.5c per GB. 25 GB: 25 ÷ 25 = $1 per GB. <b>The 40 GB plan</b>."),
        ("A Brisbane to Sydney flight covers 750 km in 1 hour 15 minutes. What is the average speed?", "600 km/h", ["650 km/h", "937.5 km/h", "500 km/h"], "1 h 15 min = 1.25 h. 750 ÷ 1.25 = <b>600 km/h</b>."),
        ("A bricklayer lays 45 bricks in 15 minutes. How many bricks does he lay in 2 hours at the same rate?", "360", ["90", "675", "180"], "3 bricks per minute × 120 minutes = <b>360</b>."),
        ("A runner's pace is 5 minutes per kilometre. How long does she take to run 10 km?", "50 minutes", ["2 minutes", "15 minutes", "1 hour 5 minutes"], "5 × 10 = <b>50 minutes</b>."),
        ("A runner's pace is 5 minutes per kilometre. What is her speed in km/h?", "12 km/h", ["5 km/h", "20 km/h", "300 km/h"], "In 60 minutes she runs 60 ÷ 5 = <b>12 km</b>, so 12 km/h."),
        ("Petrol costs $1.85 per litre at one station and $1.79 at another. How much is saved on 60 L at the cheaper station?", "$3.60", ["$0.06", "$36", "$107.40"], "6c per litre × 60 = 360c = <b>$3.60</b>."),
        ("A tap leaks 1 drop per second. 20 drops make 1 mL. How many litres leak in one day?", "4.32 L", ["86.4 L", "43.2 L", "0.432 L"], "86 400 drops ÷ 20 = 4320 mL = <b>4.32 L</b>."),
        ("Which rate is written in simplest form?", "$15 per hour", ["$45 per 3 hours", "$30 per 2 hours", "$150 per 10 hours"], "A unit rate compares to 1 unit: <b>$15 per hour</b>."),
        ("An electrician charges $90 per hour. A job takes 2 hours 20 minutes. What is the cost?", "$210", ["$198", "$180", "$270"], "2 h 20 min = 2⅓ h. 90 × 2⅓ = <b>$210</b>."),
        ("A car travels at 100 km/h. How many metres does it travel in one second, to the nearest metre?", "28 m", ["100 m", "2 m", "360 m"], "100 000 m ÷ 3600 s = 27.8 m/s ≈ <b>28 m</b>."),
        ("Ethan types 240 words in 4 minutes. Zara types 330 words in 6 minutes. Who types faster?", "Ethan", ["Zara", "They type at the same rate", "You cannot tell"], "Ethan: 60 words per minute. Zara: 55 words per minute. <b>Ethan</b> is faster."),
        ("A 2 L bottle of milk costs $3.10 and a 3 L bottle costs $4.50. What is the saving per litre with the 3 L bottle?", "5c", ["$1.40", "15c", "50c"], "2 L: $1.55 per litre. 3 L: $1.50 per litre. Saving <b>5c</b> per litre."),
    ]
    f = lambda t: t.replace("86 400", "86 400").replace("22 500", "22 500").replace("100 000", "100 000")
    return [T(f(q), f(a), [f(x) for x in w], f(e)) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>rate</b> compares two quantities with <b>different units</b>, such as km/h, $/kg or L/min. "
        "A <b>unit rate</b> compares to 1 unit: divide the first quantity by the second.</p>"
        "<p>Speed = distance ÷ time, distance = speed × time, time = distance ÷ speed. "
        "Change minutes to hours by dividing by 60: 45 minutes = 0.75 hours, not 0.45.</p>"
        "<p>To find the <b>best buy</b>, compare the price for the same amount of each pack.</p>",
        [("A car travels 210 km in 3 hours. Find its average speed.", ["210 ÷ 3 = 70."], "70 km/h"),
         ("Convert 72 km/h into m/s.", ["72 km/h = 72 000 m in 3600 s.", "72 000 ÷ 3600."], "20 m/s"),
         ("Which is better value: 500 g for $4.50 or 1 kg for $8.40?", ["$0.90 per 100 g and $0.84 per 100 g."], "The 1 kg pack")],
        ["Dividing the wrong way: $45 for 3 hours is $15 per hour, not 0.07 hours per dollar.",
         "Treating minutes as decimals: 1 hour 30 minutes is 1.5 hours, not 1.3 hours.",
         "Choosing the cheapest pack instead of the cheapest price per unit.",
         "Multiplying by 3.6 to change km/h to m/s. Divide by 3.6."]).replace("72 000", "72 000")


def main():
    sets = [S("Unit rates", collect(one_unit, 20, R)),
            S("Speed, distance and time", collect(one_sdt, 20, R)),
            S("Converting rates", collect(one_conv, 20, R)),
            S("Best buys", collect(one_best, 20, R)),
            S("Rate problems", problems())]
    make(8, "rates", 13, "AC9M8M05",
         "Rates: Unit Rates, Speed and Best Buys",
         "Year 8 Rates Worksheets: Unit Rates, Speed, Distance and Time and Best Buys (Free, Answer Key)",
         "Rates",
         "recognise and use rates to solve problems involving the comparison of 2 related quantities of different units of measure",
         "Free Year 8 maths worksheets on rates for the Australian Curriculum (AC9M8M05): unit rates, speed, distance and time, "
         "converting km/h and m/s, best buys and fuel problems. 100 questions with an answer key.",
         "A rate compares two quantities with different units, such as km/h or $/kg.",
         "Speed = distance ÷ time. To compare value, find the price for the same amount.",
         body(),
         [("What is a rate in maths?", "A rate compares two quantities measured in different units, such as 60 km per hour or $4 per kilogram."),
          ("What is a unit rate?", "A rate for 1 unit of the second quantity. $45 for 3 hours is a unit rate of $15 per hour."),
          ("How do I convert km/h to m/s?", "Multiply by 1000 to get metres and divide by 3600 to get seconds, which is the same as dividing by 3.6."),
          ("How do I work out the best buy?", "Find the price per unit (or per 100 g) for each pack. The lower unit price is the better value.")],
         sets, R)


if __name__ == "__main__":
    main()
