# -*- coding: utf-8 -*-
"""
SG Secondary 1 Maths: Speed, Distance and Time (Sec 1 Ratio, proportion and rates of change)
  python3 gen_sg_maths_s1_rate_and_speed.py
Speed = distance ÷ time, finding distance and time, times in hours and minutes, converting units of speed,
density = mass ÷ volume, and average speed problems.
Wrong answers come from real mistakes: dividing the wrong way, reading 1.5 hours as 1 hour 50 minutes,
using minutes as if they were hours, and averaging two speeds instead of using total distance ÷ total time.
"""
import random
from fractions import Fraction as F
from sg_sec import num, mcq, B, S, make, lesson, collect, QN, T, People

R = random.Random(810700)
P = People(R)


def hm(h):
    """Fraction of hours -> '2 hours 15 minutes'"""
    h = F(h)
    whole = int(h)
    mins = (h - whole) * 60
    parts = []
    if whole:
        parts.append("%d hour%s" % (whole, "" if whole == 1 else "s"))
    if mins:
        parts.append("%s minute%s" % (num(mins), "" if mins == 1 else "s"))
    return " ".join(parts) if parts else "0 minutes"


# ------------------------------------------------------------ set 1: speed
def one_speed(r):
    s = r.choice([4, 5, 12, 15, 20, 30, 40, 45, 50, 60, 64, 70, 80, 90, 120])
    t = r.choice([F(1, 2), 1, F(3, 2), 2, 3, 4, F(5, 2), 5])
    d = s * t
    if F(d).denominator != 1:
        return None
    unit, su = r.choice([("km", "km/h"), ("km", "km/h")])
    who = "walker" if s <= 6 else "cyclist" if s <= 20 else r.choice(["car", "coach"]) if s <= 70 else "train"
    q = "A %s travels %s %s in %s. What is the average speed?" % (who, num(d), unit, hm(t))
    e = "Speed = distance ÷ time = %s ÷ %s = <b>%s %s</b>." % (num(d), num(t), num(s), su)
    return QN(q, s, [F(t) / F(d) * 100 if False else F(d) * F(t), F(d) / (int(t) + F(t - int(t)) * 100 / 60 if t != int(t) else F(t) + 1) if True else None, F(d) - F(t)], e, unit=" " + su)


# ------------------------------------------------------------ set 2: distance and time
def one_dt(r):
    s = r.choice([30, 40, 48, 50, 60, 64, 72, 80, 90, 100])
    if r.random() < 0.5:
        t = r.choice([F(1, 4), F(1, 2), F(3, 4), F(3, 2), F(5, 2), 2, 3, F(4, 3) if s % 3 == 0 else 2])
        d = s * t
        if F(d).denominator != 1:
            return None
        q = "A car travels at %d km/h for %s. How far does it go?" % (s, hm(t))
        e = "Distance = speed × time = %d × %s = <b>%s km</b>." % (s, num(t) if F(t).denominator in (1, 2, 4) else hm(t), num(d))
        mins = (F(t) - int(t)) * 60 + int(t) * 60
        wrong = s * (int(t) + (F(t) - int(t)) * 60 / 100)
        return QN(q, d, [F(s, t), s * mins, wrong if wrong != d else None], e, unit=" km")
    t = r.choice([F(1, 2), F(3, 4), F(3, 2), 2, F(5, 2), 3, F(5, 4)])
    d = s * t
    if F(d).denominator != 1:
        return None
    q = "A train travels %s km at %d km/h. How long does the journey take?" % (num(d), s)
    right = hm(t)
    wrong_dec = F(t)
    wr = [hm(F(s) / F(d)) if F(s) / F(d) != t else hm(t + 1), "%s hours" % num(wrong_dec) if wrong_dec.denominator != 1 and False else
          ("%d hour%s %d minutes" % (int(t), "" if int(t) == 1 else "s", int((t - int(t)) * 100)) if t != int(t) and int(t) else hm(t + F(1, 2))),
          hm(t * 2), hm(t + F(1, 4))]
    e = "Time = distance ÷ speed = %s ÷ %d = %s hours = <b>%s</b>." % (num(d), s, num(t), right)
    wr = [w for w in wr if w != right]
    return T(q, right, list(dict.fromkeys(wr))[:3], e)


# ------------------------------------------------------------ set 3: hours and minutes, unit conversion
def one_units(r):
    kind = r.randint(0, 2)
    if kind == 0:
        h = r.choice([F(3, 2), F(9, 4), F(11, 4), F(1, 4), F(7, 10), F(13, 5), F(5, 4), F(19, 10), F(1, 5), F(31, 10)])
        q = "Write %s hours in hours and minutes." % B(num(h))
        right = hm(h)
        whole = int(h)
        dec = num(h - whole).replace("0.", "")
        wrong1 = "%d hour%s %s minutes" % (whole, "" if whole == 1 else "s", dec) if whole else "%s minutes" % dec
        wrong1 = wrong1 if wrong1 != right else hm(h + F(1, 10))
        e = "%s of an hour = %s × 60 = %s minutes. So <b>%s</b>." % (num(h - whole), num(h - whole), num((h - whole) * 60), right)
        return T(q, right, [wrong1, hm(h + F(1, 4)), hm(h - F(1, 10)) if h > F(1, 2) else hm(h + F(1, 2))], e)
    if kind == 1:
        m = r.choice([15, 30, 45, 12, 6, 48, 36, 90, 75, 24, 54])
        q = "Write %s as a decimal number of hours." % B("%d minutes" % m)
        v = F(m, 60)
        return QN(q, v, [F(m, 100), F(60, m) if F(60, m).denominator <= 4 else None, F(m, 10)], "%d ÷ 60 = <b>%s hours</b>." % (m, num(v)), unit=" hours", near=(F(1, 10), F(-1, 20)))
    kmh = r.choice([36, 72, 18, 54, 90, 108, 144])
    ms = F(kmh * 1000, 3600)
    if r.random() < 0.5:
        q = "Convert %s into m/s." % B("%d km/h" % kmh)
        e = "%d km/h = %s m in 3600 s. %s ÷ 3600 = <b>%s m/s</b>." % (kmh, num(kmh * 1000), num(kmh * 1000), num(ms))
        return QN(q, ms, [kmh * F(36, 10), F(kmh, 60), F(kmh * 1000, 60)], e, unit=" m/s")
    q = "Convert %s into km/h." % B("%s m/s" % num(ms))
    e = "%s m/s × 3600 = %s m per hour = <b>%d km/h</b>." % (num(ms), num(ms * 3600), kmh)
    return QN(q, kmh, [ms / F(36, 10), ms * 60, ms * 1000], e, unit=" km/h")


# ------------------------------------------------------------ set 4: density
def one_density(r):
    rho = r.choice([F(1), F(2), F(19, 2), F(27, 10), F(79, 10), F(11, 10), F(3, 5), F(9, 10), F(4)])
    vol = r.choice([5, 10, 20, 25, 40, 50, 100, 150, 200])
    m = rho * vol
    if F(m).denominator != 1 and F(m * 10).denominator != 1:
        return None
    kind = r.randint(0, 2)
    if kind == 0:
        q = "A block has a mass of %s g and a volume of %d cm³. What is its density?" % (num(m), vol)
        return QN(q, rho, [F(vol) / F(m), F(m) * vol, F(m) - vol if F(m) > vol else None], "Density = mass ÷ volume = %s ÷ %d = <b>%s g/cm³</b>." % (num(m), vol, num(rho)), unit=" g/cm³")
    if kind == 1:
        q = "A metal has a density of %s g/cm³. What is the mass of %d cm³ of it?" % (num(rho), vol)
        return QN(q, m, [F(vol) / rho if (F(vol) / rho).denominator <= 10 else None, rho + vol, F(m) * 10], "Mass = density × volume = %s × %d = <b>%s g</b>." % (num(rho), vol, num(m)), unit=" g")
    q = "A liquid has a density of %s g/cm³. What volume has a mass of %s g?" % (num(rho), num(m))
    return QN(q, vol, [F(m) * rho, F(rho) / F(m) if False else F(m) + rho, vol * 10], "Volume = mass ÷ density = %s ÷ %s = <b>%d cm³</b>." % (num(m), num(rho), vol), unit=" cm³")


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("Wei Ling drives 60 km in 1 hour, then 40 km in 1 hour. What is her average speed for the whole journey?", "50 km/h", ["100 km/h", "40 km/h", "60 km/h"], "Total distance 100 km ÷ total time 2 hours = <b>50 km/h</b>."),
        ("A car travels 90 km at 60 km/h and then 90 km at 90 km/h. What is the average speed?", "72 km/h", ["75 km/h", "150 km/h", "80 km/h"], "Times: 1.5 h and 1 h. Total 180 km ÷ 2.5 h = <b>72 km/h</b>. (Not the mean of 60 and 90.)"),
        ("Ahmad walks 6 km in 1 hour 30 minutes. What is his average speed?", "4 km/h", ["4.6 km/h", "3.9 km/h", "9 km/h"], "1 hour 30 minutes = 1.5 hours. 6 ÷ 1.5 = <b>4 km/h</b>."),
        ("A train leaves at 09:40 and arrives at 11:10. It travels 120 km. What is its average speed?", "80 km/h", ["90 km/h", "60 km/h", "120 km/h"], "Time = 1 hour 30 minutes = 1.5 hours. 120 ÷ 1.5 = <b>80 km/h</b>."),
        ("A cyclist rides at 18 km/h for 40 minutes. How far does she travel?", "12 km", ["720 km", "7.2 km", "27 km"], "40 minutes = 2/3 hour. 18 × 2/3 = <b>12 km</b>."),
        ("Sound travels at 340 m/s. How far does it travel in 5 seconds?", "1700 m", ["68 m", "345 m", "1.7 m"], "340 × 5 = <b>1700 m</b>."),
        ("A plane flies 2100 km at 700 km/h. It leaves at 14:30. When does it land?", "17:30", ["17:00", "16:30", "21:30"], "Time = 2100 ÷ 700 = 3 hours. 14:30 + 3 hours = <b>17:30</b>."),
        ("Which is faster: 20 m/s or 60 km/h?", "20 m/s", ["60 km/h", "They are the same", "You cannot tell"], "20 m/s = 20 × 3.6 = 72 km/h, which is faster than 60 km/h. So <b>20 m/s</b>."),
        ("On a distance–time graph, what does a horizontal line show?", "The object is not moving", ["The object is moving at a steady speed", "The object is speeding up", "The object is coming back"],
         "The distance does not change, so the object is <b>not moving</b> (stationary)."),
        ("On a distance–time graph, what does a steeper straight line show?", "A faster speed", ["A slower speed", "Stopping", "Going backwards"], "The gradient of a distance–time graph is the speed. Steeper means <b>faster</b>."),
        ("Gold has a density of 19.3 g/cm³. What is the mass of a 10 cm³ gold bar?", "193 g", ["1.93 g", "29.3 g", "0.52 g"], "19.3 × 10 = <b>193 g</b>."),
        ("1 cm³ of water has a mass of 1 g. What is the mass of 1 litre of water?", "1 kg", ["100 g", "10 kg", "1 g"], "1 litre = 1000 cm³, so 1000 g = <b>1 kg</b>."),
        ("A runner covers 400 m in 50 seconds. What is her speed in m/s?", "8 m/s", ["0.125 m/s", "20 000 m/s", "450 m/s"], "400 ÷ 50 = <b>8 m/s</b>."),
        ("A snail moves at 3 cm per minute. How long does it take to move 1 m?", "33 minutes 20 seconds", ["33 minutes", "3 minutes 33 seconds", "300 minutes"], "100 ÷ 3 = 33⅓ minutes = <b>33 minutes 20 seconds</b>."),
        ("A coach travels at 55 km/h for 2 hours 12 minutes. How far does it go?", "121 km", ["116.6 km", "110 km", "126.5 km"], "2 hours 12 minutes = 2.2 hours. 55 × 2.2 = <b>121 km</b>."),
        ("Two cars leave the same place in opposite directions at 40 km/h and 50 km/h. How far apart are they after 2 hours?", "180 km", ["20 km", "90 km", "200 km"], "Each hour they move 90 km further apart: 90 × 2 = <b>180 km</b>."),
        ("A ferry crosses 36 km in 45 minutes. What is its average speed in km/h?", "48 km/h", ["0.8 km/h", "27 km/h", "80 km/h"], "45 minutes = 0.75 hours. 36 ÷ 0.75 = <b>48 km/h</b>."),
        ("Which formula gives time?", "time = distance ÷ speed", ["time = speed ÷ distance", "time = speed × distance", "time = distance − speed"], "From speed = distance ÷ time: <b>time = distance ÷ speed</b>."),
        ("A 500 cm³ block of wood has a mass of 350 g. Will it float in water (density 1 g/cm³)?", "Yes, its density is 0.7 g/cm³", ["No, its density is 1.43 g/cm³", "No, it is too heavy", "Yes, its density is 150 g/cm³"],
         "350 ÷ 500 = 0.7 g/cm³, less than water, so <b>it floats</b>."),
        ("A car travels 150 km on Monday in 3 hours and 100 km on Tuesday in 2 hours. On which day was its average speed higher?", "They were the same", ["Monday", "Tuesday", "You cannot tell"], "Both are 50 km/h: <b>the same</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p><b>Speed = distance ÷ time</b>, <b>distance = speed × time</b>, <b>time = distance ÷ speed</b>. "
        "Make sure the units match: for km/h use km and hours.</p>"
        "<p>Minutes must be changed to hours by dividing by 60: 45 minutes = 0.75 hours, and 1.5 hours = 1 hour 30 minutes.</p>"
        "<p><b>Density = mass ÷ volume</b>, usually in g/cm³. <b>Average speed</b> = total distance ÷ total time.</p>",
        [("A car travels 150 km in 2 hours 30 minutes. Find its speed.", ["2 hours 30 minutes = 2.5 hours.", "150 ÷ 2.5 = 60."], "60 km/h"),
         ("Write 2.4 hours in hours and minutes.", ["0.4 × 60 = 24 minutes."], "2 hours 24 minutes"),
         ("Convert 72 km/h into m/s.", ["72 000 m in 3600 s.", "72 000 ÷ 3600 = 20."], "20 m/s")],
        ["Reading 1.5 hours as 1 hour 50 minutes. It is 1 hour 30 minutes.",
         "Using minutes as hours: 40 minutes is 2/3 of an hour, not 0.4.",
         "Dividing the wrong way: time = distance ÷ speed, not speed ÷ distance.",
         "Finding average speed by averaging the speeds instead of total distance ÷ total time."])


def main():
    sets = [S("Finding speed", collect(one_speed, 20, R)),
            S("Finding distance and time", collect(one_dt, 20, R)),
            S("Hours, minutes and speed units", collect(one_units, 20, R)),
            S("Density", collect(one_density, 20, R)),
            S("Problems", problems())]
    make(1, "rate-and-speed", 6, "N4",
         "Rate and Speed: Speed, Distance, Time and Unit Conversion",
         "Secondary 1 Speed, Distance and Time Worksheets: Average Speed, Converting Units and Density",
         "Rate and speed",
         "Use compound units such as speed, unit pricing and density to solve problems; change freely between related "
         "standard units (for example time, length, area, volume/capacity, mass).",
         "Free Secondary 1 speed, distance and time worksheets: find speed, distance and time, convert hours and minutes, "
         "change km/h to m/s, density problems and average speed. 100 questions with answers.",
         "Speed = distance ÷ time. Distance = speed × time. Time = distance ÷ speed.",
         "Change minutes to hours by dividing by 60. Average speed = total distance ÷ total time.",
         body(),
         [("What is the formula for speed?", "Speed = distance ÷ time. Rearranged, distance = speed × time and time = distance ÷ speed."),
          ("How do I change minutes into hours?", "Divide by 60. 45 minutes = 45 ÷ 60 = 0.75 hours."),
          ("How do I convert km/h to m/s?", "Multiply by 1000 to get metres per hour, then divide by 3600. In short, divide by 3.6."),
          ("What is density?", "Density = mass ÷ volume. It tells you how heavy a material is for its size, for example 19.3 g/cm³ for gold.")],
         sets, R)


if __name__ == "__main__":
    main()
