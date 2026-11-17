# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Volume and Capacity of Right Prisms (Australian Curriculum v9.0: AC9M8M02)
  python3 tools/gen_au_maths_y8_volume_and_capacity.py
Converting between units of volume and capacity (cm³, mL, L, m³, kL), the capacity of rectangular prisms in
litres, prisms with composite cross-sections, missing dimensions and depths, and problems.
Wrong answers come from real mistakes: using 100 or 1000 the wrong way, forgetting that 1 m³ = 1000 L, adding the
dimensions, and finding the area of the cross-section but not multiplying by the length.
"""
import random
from fractions import Fraction as F
from au_hs import num, B, S, make, lesson, collect, QN, T, fig, dec
from gen_au_maths_y7_volume_of_prisms import cuboid_svg

R = random.Random(81001)


def n(v):
    v = F(v)
    return num(v) if v.denominator == 1 else dec(v)


# ------------------------------------------------------------ set 1: converting units
def one_conv(r):
    kind = r.choice(["cm3_ml", "l_cm3", "ml_l", "m3_l", "m3_kl", "l_ml", "kl_l"])
    if kind == "cm3_ml":
        v = r.choice([250, 375, 600, 1200, 45, 80])
        return QN("How many millilitres is %s?" % B("%s cm³" % num(v)), v, [v * 1000, F(v, 1000), v * 10], "1 cm³ holds 1 mL, so %s cm³ = <b>%s mL</b>." % (num(v), num(v)), unit=" mL", near=(100, -100))
    if kind == "l_cm3":
        v = F(r.choice([2, 3, 5, 15, 25, 12])) / r.choice([1, 2, 4])
        if (v * 1000).denominator != 1:
            return None
        return QN("How many cm³ is %s?" % B("%s L" % n(v)), v * 1000, [v * 100, v * 1000000, v * 10], "1 L = 1000 cm³, so %s L = <b>%s cm³</b>." % (n(v), num(v * 1000)), fmt=n, unit=" cm³", near=(1000, -1000))
    if kind == "ml_l":
        v = r.choice([1500, 2250, 750, 600, 3400, 125, 12500])
        return QN("Write %s in litres." % B("%s mL" % num(v)), F(v, 1000), [F(v, 100), v * 1000, F(v, 10)], "Divide by 1000: %s mL = <b>%s L</b>." % (num(v), n(F(v, 1000))), fmt=n, unit=" L", near=(F(1, 10), -F(1, 10)))
    if kind == "m3_l":
        v = F(r.choice([2, 3, 6, 15, 24, 5, 9, 12])) / r.choice([1, 2, 10])
        if (v * 1000).denominator != 1:
            return None
        return QN("How many litres does %s of water fill?" % B("%s m³" % n(v)), v * 1000, [v * 100, v * 1000000, v], "1 m³ = 1000 L, so %s m³ = <b>%s L</b>." % (n(v), num(v * 1000)), fmt=n, unit=" L", near=(1000, -1000))
    if kind == "m3_kl":
        v = F(r.choice([3, 8, 12, 45, 60, 25, 7])) / r.choice([1, 2])
        return QN("How many kilolitres is %s?" % B("%s m³" % n(v)), v, [v * 1000, v / 1000, v * 100], "1 m³ = 1 kL, so %s m³ = <b>%s kL</b>." % (n(v), n(v)), fmt=n, unit=" kL", near=(1, -1, 10))
    if kind == "l_ml":
        v = F(r.choice([3, 7, 11, 13, 9, 1])) / r.choice([2, 4, 5, 10])
        return QN("Write %s in millilitres." % B("%s L" % n(v)), v * 1000, [v * 100, v * 10, v / 1000], "Multiply by 1000: %s L = <b>%s mL</b>." % (n(v), num(v * 1000)), fmt=n, unit=" mL", near=(100, -100))
    v = F(r.choice([3, 7, 12, 25, 45])) / r.choice([1, 2, 10])
    return QN("Write %s in litres." % B("%s kL" % n(v)), v * 1000, [v * 100, v / 1000, v * 10], "1 kL = 1000 L, so %s kL = <b>%s L</b>." % (n(v), num(v * 1000)), fmt=n, unit=" L", near=(1000, -1000))


# ------------------------------------------------------------ set 2: capacity of rectangular prisms
def one_cap(r):
    if r.random() < 0.55:
        l, w, h = r.choice([20, 25, 30, 40, 50, 60]), r.choice([10, 15, 20, 25, 30]), r.choice([10, 15, 20, 25, 30, 40])
        if len({l, w, h}) < 3:
            return None
        V = l * w * h
        thing = r.choice(["fish tank", "storage box", "esky", "planter box"])
        q = "A %s is a rectangular prism. What is its capacity in litres?%s" % (thing, fig(cuboid_svg(l, w, h)))
        e = "Volume = %d × %d × %d = %s cm³. 1000 cm³ = 1 L, so %s ÷ 1000 = <b>%s L</b>." % (l, w, h, num(V), num(V), n(F(V, 1000)))
        return QN(q, F(V, 1000), [V, F(V, 100), F(l + w + h)], e, fmt=n, unit=" L", near=(1, -1, F(1, 2)))
    thing = r.choice(["water tank", "sandpit", "garden bed", "concrete slab"])
    l, w = r.choice([2, 3, 4, 5, 6, 8]), r.choice([1, 2, 3, 4])
    h = F(r.choice({"water tank": [1, 2, 3, 15, 12], "sandpit": [3, 4, 5], "garden bed": [3, 4, 5, 6], "concrete slab": [1, 15, 2]}[thing]),
          1 if thing == "water tank" and r.random() < 0.4 else 10)
    if thing == "water tank" and h > 2 or thing == "concrete slab" and h > F(1, 5):
        return None
    if l <= w:
        return None
    V = l * w * h
    unit = "kL" if thing == "water tank" else "m³"
    q = "A %s is %d m long, %d m wide and %s m deep. What is its %s?" % (thing, l, w, n(h), "capacity in kilolitres" if unit == "kL" else "volume in m³")
    e = "Volume = %d × %d × %s = <b>%s %s</b>%s." % (l, w, n(h), n(V), unit, " (1 m³ = 1 kL)" if unit == "kL" else "")
    return QN(q, V, [V * 1000, l + w + h, 2 * (l * w + w * h + l * h)], e, fmt=n, unit=" " + unit, near=(1, -1, 2))


# ------------------------------------------------------------ set 3: composite cross-sections
def one_cross(r):
    kind = r.choice(["L", "trap", "T"])
    L = r.choice([5, 8, 10, 12, 15, 20])
    if kind == "L":
        W_, H_ = r.randint(6, 12), r.randint(5, 10)
        cw, ch = r.randint(2, W_ - 3), r.randint(2, H_ - 2)
        A = W_ * H_ - cw * ch
        q = ("A prism is %d cm long. Its cross-section is an L-shape: a %d cm by %d cm rectangle with a %d cm by %d cm "
             "rectangle cut from one corner. What is the volume of the prism?" % (L, W_, H_, cw, ch))
        e = "Cross-section = %d × %d − %d × %d = %d cm². Volume = %d × %d = <b>%s cm³</b>." % (W_, H_, cw, ch, A, A, L, num(A * L))
        return QN(q, A * L, [W_ * H_ * L, A, (W_ * H_ + cw * ch) * L], e, unit=" cm³", near=(L, -L, 10))
    if kind == "trap":
        a, b, h = r.randint(3, 8), r.randint(9, 16), r.randint(3, 8)
        A = F((a + b) * h, 2)
        q = ("A prism is %d cm long. Its cross-section is a trapezium with parallel sides %d cm and %d cm and a "
             "perpendicular height of %d cm. What is its volume?" % (L, a, b, h))
        e = "Cross-section = ½ × (%d + %d) × %d = %s cm². Volume = %s × %d = <b>%s cm³</b>." % (a, b, h, num(A), num(A), L, num(A * L))
        return QN(q, A * L, [(a + b) * h * L, A, a * b * h * L if a * b * h * L < 20000 else A * L * 2], e, unit=" cm³", near=(L, -L, 10))
    a, b, c, d = r.randint(8, 14), r.randint(2, 4), r.randint(2, 4), r.randint(4, 9)
    if c >= a - 2:
        return None
    A = a * b + c * d
    q = ("A prism is %d cm long. Its cross-section is a T-shape: a %d cm by %d cm bar on top of a %d cm by %d cm stem. "
         "What is its volume?" % (L, a, b, c, d))
    e = "Cross-section = %d × %d + %d × %d = %d cm². Volume = %d × %d = <b>%s cm³</b>." % (a, b, c, d, A, A, L, num(A * L))
    return QN(q, A * L, [A, (a + b + c + d) * L, a * b * c * d], e, unit=" cm³", near=(L, -L, 10))


# ------------------------------------------------------------ set 4: missing dimensions and depth
def one_missing(r):
    kind = r.choice(["depth", "height", "time", "length"])
    if kind == "depth":
        l, w = r.choice([40, 50, 60, 80]), r.choice([20, 25, 30, 40])
        d = r.choice([5, 10, 12, 15, 20, 25])
        Lw = F(l * w * d, 1000)
        q = "A fish tank has a base %d cm by %d cm. %s litres of water are poured in. How deep is the water?" % (l, w, n(Lw))
        e = "%s L = %s cm³. Depth = %s ÷ (%d × %d) = %s ÷ %s = <b>%d cm</b>." % (n(Lw), num(l * w * d), num(l * w * d), l, w, num(l * w * d), num(l * w), d)
        return QN(q, d, [F(Lw * 1000, l), F(Lw, l * w) * 100 if F(Lw, l * w) * 100 != d else d * 10, d * 10], e, unit=" cm", near=(1, -1, 5))
    if kind == "height":
        l, w, h = r.randint(3, 12), r.randint(2, 9), r.randint(2, 12)
        if len({l, w, h}) < 3:
            return None
        V = l * w * h
        q = "A rectangular prism has a volume of %s cm³, a length of %d cm and a width of %d cm. What is its height?" % (num(V), l, w)
        e = "Height = %s ÷ (%d × %d) = %s ÷ %d = <b>%d cm</b>." % (num(V), l, w, num(V), l * w, h)
        return QN(q, h, [V - l - w, F(V, l + w) if V % (l + w) == 0 else V // l, l * w], e, unit=" cm")
    if kind == "time":
        kl = r.choice([12, 18, 24, 30, 45, 50, 60])
        rate = r.choice([10, 15, 20, 25, 30])
        mins = F(kl * 1000, rate)
        if mins.denominator != 1 or mins % 60:
            return None
        hrs = mins / 60
        q = "A pool holds %d kL of water. A hose fills it at %d L per minute. How many hours does it take to fill?" % (kl, rate)
        e = "%d kL = %s L. %s ÷ %d = %s minutes = <b>%s hours</b>." % (kl, num(kl * 1000), num(kl * 1000), rate, num(mins), num(hrs))
        return QN(q, hrs, [mins, F(kl, rate), hrs * 60 / 100 if hrs * 60 / 100 != hrs else hrs * 2], e, fmt=n, unit=" hours", near=(1, -1, 2))
    A = r.choice([12, 15, 18, 20, 24, 30, 36])
    l = r.randint(4, 15)
    V = A * l
    q = "A prism has a cross-section of area %d cm² and a volume of %s cm³. How long is it?" % (A, num(V))
    e = "Length = volume ÷ area of cross-section = %s ÷ %d = <b>%d cm</b>." % (num(V), A, l)
    return QN(q, l, [V - A, V * A if V * A < 9000 else l * 10, F(V, 2 * A) if V % (2 * A) == 0 else l + 3], e, unit=" cm")


# ------------------------------------------------------------ set 5: problems
def problems():
    data = [
        ("A rainwater tank is a rectangular prism 2 m long, 1 m wide and 1.5 m high. How many litres does it hold?", "3000 L", ["300 L", "3 L", "4.5 L"], "2 × 1 × 1.5 = 3 m³ = <b>3000 L</b>."),
        ("A backyard pool is 8 m by 4 m and 1.5 m deep everywhere. How many kilolitres of water fill it?", "48 kL", ["13.5 kL", "48 000 kL", "480 kL"], "8 × 4 × 1.5 = 48 m³ = <b>48 kL</b>."),
        ("A juice carton is 6 cm by 4 cm by 10 cm. How many millilitres can it hold?", "240 mL", ["24 mL", "2400 mL", "20 mL"], "6 × 4 × 10 = 240 cm³ = <b>240 mL</b>."),
        ("How many 250 mL glasses can be filled from a 2 L bottle?", "8", ["80", "5", "4"], "2 L = 2000 mL. 2000 ÷ 250 = <b>8</b>."),
        ("A concrete path is 10 m long, 1.2 m wide and 0.1 m thick. How much concrete is needed?", "1.2 m³", ["12 m³", "120 m³", "11.3 m³"], "10 × 1.2 × 0.1 = <b>1.2 m³</b>."),
        ("A cube has a volume of 64 cm³. What is the length of each edge?", "4 cm", ["8 cm", "16 cm", "21.3 cm"], "4 × 4 × 4 = 64, so the edge is <b>4 cm</b>."),
        ("Which is the greatest capacity?", "1.2 L", ["950 mL", "1000 cm³", "0.9 L"], "In mL: 1200, 950, 1000 and 900. The greatest is <b>1.2 L</b>."),
        ("A water trough is a triangular prism 2 m long. Its cross-section has a base of 0.6 m and a height of 0.5 m. How many litres does it hold?", "300 L", ["600 L", "3000 L", "0.3 L"],
         "Cross-section = ½ × 0.6 × 0.5 = 0.15 m². Volume = 0.15 × 2 = 0.3 m³ = <b>300 L</b>."),
        ("A shower uses 9 L of water per minute. How many kilolitres does a 10-minute shower every day use in 30 days?", "2.7 kL", ["27 kL", "270 kL", "0.27 kL"], "9 × 10 × 30 = 2700 L = <b>2.7 kL</b>."),
        ("A box is 30 cm by 20 cm by 10 cm. How many 10 cm cubes fit inside?", "6", ["60", "600", "3"], "3 × 2 × 1 = <b>6</b> cubes."),
        ("What happens to the volume of a rectangular prism if every edge is doubled?", "It is 8 times as big", ["It doubles", "It is 4 times as big", "It is 6 times as big"], "2 × 2 × 2 = 8, so the volume is <b>8 times</b> as big."),
        ("A fish tank holds 60 L when full. It is 50 cm long and 30 cm wide. How tall is it?", "40 cm", ["4 cm", "400 cm", "20 cm"], "60 L = 60 000 cm³. 60 000 ÷ (50 × 30) = 60 000 ÷ 1500 = <b>40 cm</b>."),
        ("1 mL of water has a mass of 1 g. What is the mass of the water in a full 2 L bottle?", "2 kg", ["200 g", "20 kg", "2 g"], "2 L = 2000 mL, so 2000 g = <b>2 kg</b>."),
        ("How many cm³ are in 1 m³?", "1 000 000", ["1000", "100", "10 000"], "1 m³ = 100 cm × 100 cm × 100 cm = <b>1 000 000 cm³</b>."),
        ("A dam holds 12 ML (megalitres). How many kilolitres is this?", "12 000 kL", ["1200 kL", "12 kL", "120 kL"], "1 ML = 1000 kL, so 12 ML = <b>12 000 kL</b>."),
        ("A rectangular prism has a volume of 120 cm³. Which could be its dimensions?", "4 cm × 5 cm × 6 cm", ["10 cm × 10 cm × 2 cm", "40 cm × 40 cm × 40 cm", "12 cm × 10 cm × 10 cm"], "4 × 5 × 6 = <b>120</b>."),
        ("A school drink bottle holds 750 mL. How many full bottles can be filled from a 15 L water cooler?", "20", ["2", "200", "11"], "15 L = 15 000 mL. 15 000 ÷ 750 = <b>20</b>."),
        ("A garden bed is 3 m by 1.5 m and needs soil 0.4 m deep. Soil costs $60 per m³. How much does the soil cost?", "$108", ["$270", "$1.80", "$4.90"], "3 × 1.5 × 0.4 = 1.8 m³. 1.8 × $60 = <b>$108</b>."),
        ("A tank is half full with 450 L. What is its full capacity in m³?", "0.9 m³", ["0.45 m³", "900 m³", "9 m³"], "Full = 900 L = <b>0.9 m³</b>."),
        ("A prism's cross-section has an area of 24 cm². It is 1 m long. What is its volume?", "2400 cm³", ["24 cm³", "240 cm³", "24 000 cm³"], "1 m = 100 cm. 24 × 100 = <b>2400 cm³</b>."),
    ]
    out = []
    for q, a, w, e in data:
        f = lambda t: t.replace(" 000", " 000")
        out.append(T(f(q), f(a), [f(x) for x in w], f(e)))
    return out


def body():
    return lesson(
        "<p>Volume of any right prism = <b>area of the cross-section × length</b>. For a rectangular prism this is length × width × height.</p>"
        "<p><b>Capacity</b> is how much a container holds. Link volume and capacity with: "
        "<b>1 cm³ = 1 mL</b>, <b>1000 cm³ = 1 L</b> and <b>1 m³ = 1000 L = 1 kL</b>.</p>",
        [("Find the capacity in litres of a tank 50 cm by 30 cm by 40 cm.", ["50 × 30 × 40 = 60 000 cm³.", "60 000 ÷ 1000."], "60 L"),
         ("A pool is 10 m by 5 m by 1.2 m deep. How many kilolitres does it hold?", ["10 × 5 × 1.2 = 60 m³.", "1 m³ = 1 kL."], "60 kL")],
        ["Dividing by 100 instead of 1000 when changing cm³ to litres.",
         "Forgetting that 1 m³ is 1000 L, not 100 L.",
         "Adding the dimensions instead of multiplying them.",
         "Finding the area of the cross-section but not multiplying by the length."]).replace(" 000", " 000")


def main():
    sets = [S("Units of volume and capacity", collect(one_conv, 20, R)),
            S("Capacity of rectangular prisms", collect(one_cap, 20, R)),
            S("Prisms with composite cross-sections", collect(one_cross, 20, R)),
            S("Missing dimensions and depths", collect(one_missing, 20, R)),
            S("Volume and capacity problems", problems())]
    make(8, "volume-and-capacity", 10, "AC9M8M02",
         "Volume and Capacity of Prisms: cm³, mL, Litres and Kilolitres",
         "Year 8 Volume and Capacity Worksheets: Prisms, Litres and Kilolitres (Free, Answer Key)",
         "Volume and capacity",
         "solve problems involving the volume and capacity of right prisms using appropriate units",
         "Free Year 8 maths worksheets on volume and capacity for the Australian Curriculum (AC9M8M02): converting cm³, mL, L, m³ "
         "and kL, capacity of tanks and pools, prisms with composite cross-sections and missing dimensions. 100 questions with an answer key.",
         "1 cm³ = 1 mL, 1000 cm³ = 1 L and 1 m³ = 1000 L = 1 kL.",
         "Volume of a prism = area of the cross-section × length.",
         body(),
         [("What is the difference between volume and capacity?", "Volume is the space an object takes up. Capacity is how much a container can hold. They are linked: 1 cm³ holds 1 mL."),
          ("How many litres are in a cubic metre?", "1000 litres, which is 1 kilolitre."),
          ("How do I find the capacity of a tank in litres?", "Find the volume in cm³ and divide by 1000, or find it in m³ and multiply by 1000."),
          ("How do I find the volume of a prism with an L-shaped cross-section?", "Find the area of the L-shape (split it into rectangles), then multiply by the length of the prism.")],
         sets, R)


if __name__ == "__main__":
    main()
