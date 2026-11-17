# -*- coding: utf-8 -*-
"""
UK Year 8 Maths: Units and Scale Drawings (KS3 Ratio, proportion and rates of change)
  python3 tools/gen_uk_maths_y8_units_and_scale_drawings.py
Converting metric units of length, mass and capacity; converting units of area and volume; scale drawings
and map scales; approximate metric–imperial conversions; and problems.
Wrong answers come from real mistakes: multiplying instead of dividing, using 100 for every conversion,
using 100 instead of 10,000 for cm² to m², and forgetting to convert cm to km on a map.
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T

R = random.Random(81701)
CONV = [("km", "m", 1000), ("m", "cm", 100), ("cm", "mm", 10), ("m", "mm", 1000), ("kg", "g", 1000), ("t", "kg", 1000),
        ("litres", "ml", 1000), ("litres", "cl", 100), ("cl", "ml", 10)]


# ------------------------------------------------------------ set 1: metric conversions
def one_metric(r):
    big, small, k = r.choice(CONV)
    v = F(r.randint(1, 999), r.choice([1, 10, 100]))
    if r.random() < 0.5:
        ans = v * k
        q = "Convert %s into %s." % (B("%s %s" % (num(v), big)), small)
        e = "1 %s = %s %s, so multiply by %s: <b>%s %s</b>." % (big.rstrip("s") if big == "litres" else big, num(k), small, num(k), num(ans), small)
        wr = [v / k, v * k / 10 if k != 10 else v * 100, v * k * 10]
    else:
        v = F(r.randint(5, 9999), r.choice([1, 10]))
        ans = v / k
        q = "Convert %s into %s." % (B("%s %s" % (num(v), small)), big)
        e = "Divide by %s: <b>%s %s</b>." % (num(k), num(ans), big)
        wr = [v * k, v / (k * 10), v / (k / 10) if k != 10 else v / 100]
    unit = " " + (small if ans == v * k else big)
    return QN(q, ans, [w for w in wr if F(w).denominator <= 10 ** 6 and w > 0], e, unit=unit, near=())


# ------------------------------------------------------------ set 2: area and volume units
def one_av(r):
    kind = r.randint(0, 4)
    if kind == 0:
        v = r.choice([2, 3, 5, F(3, 2), F(1, 2), F(5, 2), 4, 7])
        q = "Convert %s into cm²." % B("%s m²" % num(v))
        return QN(q, v * 10000, [v * 100, v * 1000, v * 1000000], "1 m² = 100 cm × 100 cm = 10,000 cm². %s × 10,000 = <b>%s cm²</b>." % (num(v), num(v * 10000)), unit=" cm²", near=())
    if kind == 1:
        v = r.choice([25000, 4000, 80000, 150000, 7500, 30000])
        q = "Convert %s into m²." % B("%s cm²" % num(v))
        return QN(q, F(v, 10000), [F(v, 100), F(v, 1000), v * 10000], "Divide by 10,000: <b>%s m²</b>." % num(F(v, 10000)), unit=" m²", near=())
    if kind == 2:
        v = r.choice([2, 5, 8, 12, 15, 30])
        q = "Convert %s into mm²." % B("%d cm²" % v)
        return QN(q, v * 100, [v * 10, v * 1000, F(v, 100)], "1 cm² = 10 mm × 10 mm = 100 mm². <b>%s mm²</b>." % num(v * 100), unit=" mm²", near=())
    if kind == 3:
        v = r.choice([2, 3, F(5, 2), F(1, 2), 4, 6])
        q = "Convert %s into cm³." % B("%s m³" % num(v))
        return QN(q, v * 1000000, [v * 100, v * 10000, v * 1000], "1 m³ = 100 × 100 × 100 = 1,000,000 cm³. <b>%s cm³</b>." % num(v * 1000000), unit=" cm³", near=())
    v = r.choice([3000, 500, 12500, 750, 2400, 45000])
    q = "A container holds %s cm³. How many litres is this?" % num(v)
    return QN(q, F(v, 1000), [F(v, 100), v * 1000, F(v, 10000)], "1,000 cm³ = 1 litre. %s ÷ 1,000 = <b>%s litres</b>." % (num(v), num(F(v, 1000))), unit=" litres", near=())


# ------------------------------------------------------------ set 3: map scales
def one_map(r):
    scale = r.choice([10000, 25000, 50000, 100000, 200000, 500000])
    if r.random() < 0.6:
        cm = F(r.randint(2, 30), r.choice([1, 2]))
        km = cm * scale / 100000
        q = "A map has a scale of 1 : %s. Two places are %s cm apart on the map. How far apart are they in real life?" % (num(scale), num(cm))
        e = "%s × %s = %s cm. 100,000 cm = 1 km, so this is <b>%s km</b>." % (num(cm), num(scale), num(cm * scale), num(km))
        return QN(q, km, [km * 10, km / 10, km * 100], e, unit=" km", near=())
    km = r.choice([1, 2, 3, 5, 10, 15, 20, 25, 40])
    cm = F(km * 100000, scale)
    if cm > 60 or cm.denominator > 10:
        return None
    q = "A map has a scale of 1 : %s. Two towns are %d km apart. How far apart are they on the map?" % (num(scale), km)
    e = "%d km = %s cm. %s ÷ %s = <b>%s cm</b>." % (km, num(km * 100000), num(km * 100000), num(scale), num(cm))
    return QN(q, cm, [cm * 10, cm / 10, F(km * scale, 100000)], e, unit=" cm", near=())


def one_scale(r):
    k = r.choice([20, 50, 100, 200, 25, 40])
    if r.random() < 0.5:
        draw = F(r.randint(2, 20), r.choice([1, 2]))
        real_cm = draw * k
        real_m = real_cm / 100
        q = "A scale drawing uses a scale of 1 : %d. A wall is %s cm long on the drawing. How long is the real wall?" % (k, num(draw))
        e = "%s × %d = %s cm = <b>%s m</b>." % (num(draw), k, num(real_cm), num(real_m))
        return QN(q, real_m, [real_cm, real_m * 10, F(draw, k) * 100 if F(draw, k) * 100 != real_m else real_m + 1], e, unit=" m", near=())
    real = r.choice([3, 4, 5, 6, 8, 10, 12, F(5, 2), F(15, 2)])
    draw = F(real * 100, k)
    if draw.denominator > 10:
        return None
    q = "A room is %s m long. It is drawn using a scale of 1 : %d. How long is it on the drawing?" % (num(real), k)
    e = "%s m = %s cm. %s ÷ %d = <b>%s cm</b>." % (num(real), num(real * 100), num(real * 100), k, num(draw))
    return QN(q, draw, [real * k, F(real, k), draw * 10], e, unit=" cm", near=())


# ------------------------------------------------------------ set 4: metric and imperial
IMP = [("inches", "cm", F(5, 2), "1 inch ≈ 2.5 cm"), ("miles", "km", F(8, 5), "5 miles ≈ 8 km"), ("kg", "pounds (lb)", F(11, 5), "1 kg ≈ 2.2 lb"),
       ("gallons", "litres", F(9, 2), "1 gallon ≈ 4.5 litres"), ("feet", "cm", 30, "1 foot ≈ 30 cm"), ("pints", "litres", F(57, 100), "1 pint ≈ 0.57 litres")]


def one_imperial(r):
    a, b, k, fact = r.choice(IMP)
    v = r.choice([2, 4, 5, 10, 12, 15, 20, 25, 40, 50])
    if r.random() < 0.6:
        ans = v * k
        q = "Use %s to convert %s into %s." % (fact, B("%d %s" % (v, a)), b)
        e = "%d × %s = <b>%s %s</b>." % (v, num(k), num(ans), b)
        return QN(q, ans, [F(v) / k, v + k, ans * 10], e, unit=" " + b, near=())
    ans = F(v)
    w = v * k
    q = "Use %s to convert %s into %s." % (fact, B("%s %s" % (num(w), b)), a)
    e = "%s ÷ %s = <b>%d %s</b>." % (num(w), num(k), v, a)
    return QN(q, ans, [w * k, w - k, ans * 10], e, unit=" " + a, near=())


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    data = [
        ("A recipe needs 750 g of flour. Flour is sold in 1.5 kg bags. How many recipes can be made from one bag?", "2", ["5", "1", "0.5"], "1.5 kg = 1,500 g. 1,500 ÷ 750 = <b>2</b>."),
        ("A jug holds 2 litres. How many 250 ml glasses can be filled?", "8", ["80", "4", "125"], "2 litres = 2,000 ml. 2,000 ÷ 250 = <b>8</b>."),
        ("A floor is 4 m by 3 m. What is its area in cm²?", "120,000 cm²", ["1,200 cm²", "12,000 cm²", "1,200,000 cm²"], "12 m² × 10,000 = <b>120,000 cm²</b>."),
        ("A model car is made to a scale of 1 : 40. The real car is 4.4 m long. How long is the model?", "11 cm", ["176 cm", "1.1 cm", "110 cm"], "4.4 m = 440 cm. 440 ÷ 40 = <b>11 cm</b>."),
        ("On a 1 : 50,000 map, a footpath is 7 cm long. How long is it in real life?", "3.5 km", ["35 km", "350 m", "0.35 km"], "7 × 50,000 = 350,000 cm = <b>3.5 km</b>."),
        ("Which is longer: 3 miles or 5 km? (5 miles ≈ 8 km)", "5 km is longer", ["3 miles is longer", "They are the same", "You cannot tell"], "3 miles ≈ 4.8 km, which is less than 5 km. So <b>5 km is longer</b>."),
        ("A runner covers 400 m in each lap. How many laps make 10 km?", "25", ["4", "250", "2.5"], "10 km = 10,000 m. 10,000 ÷ 400 = <b>25</b>."),
        ("A bottle holds 75 cl. How many ml is this?", "750 ml", ["75 ml", "7.5 ml", "7,500 ml"], "1 cl = 10 ml, so 75 cl = <b>750 ml</b>."),
        ("A plan has a scale of 1 cm to 2 m. A garden is 9 cm by 6 cm on the plan. What is the real area?", "216 m²", ["54 m²", "108 m²", "30 m²"], "Real size 18 m by 12 m. 18 × 12 = <b>216 m²</b>."),
        ("A cube has edges of 2 m. What is its volume in cm³?", "8,000,000 cm³", ["8 cm³", "800 cm³", "80,000 cm³"], "8 m³ × 1,000,000 = <b>8,000,000 cm³</b>."),
        ("Which is the heaviest?", "1.2 kg", ["950 g", "1,150 g", "0.9 kg"], "In grams: 1,200, 950, 1,150 and 900. So <b>1.2 kg</b>."),
        ("A lorry can carry 3.5 tonnes. Each crate weighs 250 kg. How many crates can it carry?", "14", ["140", "1", "7"], "3.5 t = 3,500 kg. 3,500 ÷ 250 = <b>14</b>."),
        ("A scale drawing of a classroom uses 1 : 100. On the drawing it is 8 cm long. How long is the classroom?", "8 m", ["80 m", "0.8 m", "800 m"], "8 × 100 = 800 cm = <b>8 m</b>."),
        ("A map scale says 2 cm represents 5 km. Two villages are 7 cm apart. How far apart are they?", "17.5 km", ["35 km", "14 km", "2.8 km"], "1 cm = 2.5 km. 7 × 2.5 = <b>17.5 km</b>."),
        ("A car's fuel tank holds 12 gallons. About how many litres is this? (1 gallon ≈ 4.5 litres)", "54 litres", ["2.7 litres", "16.5 litres", "540 litres"], "12 × 4.5 = <b>54 litres</b>."),
        ("A 1 : 25,000 map has 4 cm grid squares. How long is the side of one square in real life?", "1 km", ["100 m", "10 km", "25 m"], "4 × 25,000 = 100,000 cm = <b>1 km</b>."),
        ("A field has an area of 3 hectares. 1 hectare = 10,000 m². What is the area in m²?", "30,000 m²", ["3,000 m²", "300 m²", "300,000 m²"], "3 × 10,000 = <b>30,000 m²</b>."),
        ("Sort from smallest to largest: 0.45 m, 42 cm, 460 mm.", "42 cm, 0.45 m, 460 mm", ["0.45 m, 42 cm, 460 mm", "460 mm, 0.45 m, 42 cm", "42 cm, 460 mm, 0.45 m"], "In cm: 45, 42, 46. So <b>42 cm, 0.45 m, 460 mm</b>."),
        ("A tap drips 5 ml every minute. How many litres is this in one day?", "7.2 litres", ["72 litres", "0.72 litres", "300 litres"], "5 × 60 × 24 = 7,200 ml = <b>7.2 litres</b>."),
        ("Ava is 5 feet tall. About how tall is she in cm? (1 foot ≈ 30 cm)", "150 cm", ["35 cm", "6 cm", "1,500 cm"], "5 × 30 = <b>150 cm</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>Metric units: 1 km = 1,000 m, 1 m = 100 cm, 1 cm = 10 mm, 1 kg = 1,000 g, 1 litre = 1,000 ml. "
        "To change to a <b>smaller</b> unit, multiply; to a <b>larger</b> unit, divide.</p>"
        "<p>Area and volume units are different: 1 m² = 10,000 cm² and 1 m³ = 1,000,000 cm³. 1,000 cm³ = 1 litre.</p>"
        "<p>A scale of 1 : 50,000 means 1 cm on the map is 50,000 cm (500 m) in real life.</p>",
        [("Convert 3.5 kg into grams.", ["Multiply by 1,000."], "3,500 g"),
         ("Convert 2.5 m² into cm².", ["Multiply by 10,000."], "25,000 cm²"),
         ("On a 1 : 25,000 map, two places are 6 cm apart. Find the real distance.", ["6 × 25,000 = 150,000 cm.", "÷ 100,000 for km."], "1.5 km")],
        ["Multiplying when you should divide: 2,500 g is 2.5 kg, not 2,500,000 kg.",
         "Using 100 for every conversion: there are 1,000 m in a km and 1,000 g in a kg.",
         "Using 100 for cm² to m². It is 10,000.",
         "Leaving a map distance in cm instead of converting to m or km."])


def main():
    sets = [S("Metric conversions", collect(one_metric, 20, R)),
            S("Area, volume and capacity units", collect(one_av, 20, R)),
            S("Map scales", collect(one_map, 20, R)),
            S("Scale drawings and imperial units", collect(one_scale, 10, R) + collect(one_imperial, 10, R)),
            S("Problems", problems())]
    make(8, "units-and-scale-drawings", 17, "R",
         "Units of Measure, Map Scales and Scale Drawings",
         "Year 8 Units and Scale Drawings Worksheets: Metric Conversions, Area and Volume Units, Map Scales and Imperial",
         "Units and scale drawings",
         "Change freely between related standard units (for example time, length, area, volume/capacity, mass); use scale "
         "factors, scale diagrams and maps.",
         "Free Year 8 worksheets on units and scales: metric conversions, converting area and volume units, map scales, "
         "scale drawings and approximate imperial conversions. 100 questions with answers.",
         "To a smaller unit, multiply. To a larger unit, divide. 1 m² = 10,000 cm².",
         "On a 1 : 50,000 map, 1 cm is 50,000 cm = 0.5 km in real life.",
         body(),
         [("How many cm² are in a m²?", "10,000, because 1 m² is 100 cm by 100 cm."),
          ("How do I use a map scale?", "Multiply the map distance by the scale number, then convert the answer from cm to m or km."),
          ("How many cm³ make a litre?", "1,000 cm³ = 1 litre, and 1 cm³ = 1 ml."),
          ("What are useful imperial conversions?", "1 inch ≈ 2.5 cm, 1 foot ≈ 30 cm, 5 miles ≈ 8 km, 1 kg ≈ 2.2 lb and 1 gallon ≈ 4.5 litres.")],
         sets, R)


if __name__ == "__main__":
    main()
