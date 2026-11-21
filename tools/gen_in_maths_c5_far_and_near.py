# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 5: Far and Near (Length and Distance)
Kilometres, metres, centimetres and millimetres: converting, comparing and solving distance problems (UK Year 5, AU Year 5 and Ontario Grade 5 set makers)."""
from in_prim import unit, mod, rn, co, le, mcq, Kid
from in_common import comma

OBJ = [("the length of a pencil", "cm"), ("the thickness of a coin", "mm"), ("the distance from Delhi to Agra", "km"), ("the length of a classroom", "m"),
       ("the width of a fingernail", "mm"), ("the height of a door", "m"), ("the length of a cricket pitch", "m"), ("the distance a train travels in a day", "km"),
       ("the length of an ant", "mm"), ("the width of a notebook", "cm"), ("the height of a coconut tree", "m"), ("the length of a river", "km"),
       ("the length of a grain of rice", "mm"), ("the length of a spoon", "cm"), ("the distance between two cities", "km"), ("the length of a school bus", "m")]
UN = {"mm": "millimetres (mm)", "cm": "centimetres (cm)", "m": "metres (m)", "km": "kilometres (km)"}


def one_unit(r):
    o, u = r.choice(OBJ)
    return mcq("Which unit is best for measuring %s?" % o, UN[u], [UN[x] for x in UN if x != u],
               "%s is best measured in <b>%s</b>." % (o[0].upper() + o[1:], UN[u]))


def one_conv(r):
    k = r.randrange(6)
    if k == 0:
        a = r.randint(2, 15) * 1000 + r.choice([250, 500, 750, r.randint(1, 9) * 100])
        return mcq("Convert. %s m = ☐ km ☐ m" % comma(a), "%d km %d m" % (a // 1000, a % 1000), ["%d km %d m" % (a // 100, a % 100) if a % 100 else "%d km" % (a // 100), "%d km %d m" % (a // 1000 + 1, a % 1000), "%d km" % (a // 1000)],
                   "1,000 m = 1 km, so %s m = <b>%d km %d m</b>." % (comma(a), a // 1000, a % 1000))
    if k == 1:
        a, b = r.randint(1, 9), r.randint(1, 99) * 10 + r.randint(0, 9)
        t = a * 1000 + b
        return mcq("Convert. %d km %d m = ☐ m" % (a, b), comma(t) + " m", [comma(a * 100 + b) + " m", comma(a * 1000 + b * 10) + " m", comma(a + b) + " m"],
                   "%d km = %s m. %s + %d = <b>%s m</b>." % (a, comma(a * 1000), comma(a * 1000), b, comma(t)))
    if k == 2:
        a, b = r.randint(1, 12), r.randint(5, 95)
        return mcq("Convert. %d m %d cm = ☐ cm" % (a, b), "%d cm" % (a * 100 + b), ["%d cm" % (a * 10 + b), "%s cm" % comma(a * 1000 + b), "%d cm" % (a + b)],
                   "%d m = %d cm. %d + %d = <b>%d cm</b>." % (a, a * 100, a * 100, b, a * 100 + b))
    if k == 3:
        a, b = r.randint(2, 30), r.randint(1, 9)
        return mcq("Convert. %d cm %d mm = ☐ mm" % (a, b), "%d mm" % (a * 10 + b), ["%d mm" % (a * 100 + b), "%d mm" % (a + b), "%d mm" % (a * 10)],
                   "%d cm = %d mm. %d + %d = <b>%d mm</b>." % (a, a * 10, a * 10, b, a * 10 + b))
    if k == 4:
        h = r.choice([1, 3, 5, 7, 9]) * 500 + r.randint(0, 1) * 10000
        h = max(h, 1500)
        return mcq("Write %s m in kilometres." % comma(h), "%g km" % (h / 1000), ["%g km" % (h / 100), "%g km" % (h / 10000), "%d km" % (h // 1000)],
                   "Divide by 1,000: %s m = <b>%g km</b>." % (comma(h), h / 1000))
    a = r.randint(2, 40) * 100 + r.choice([5, 25, 50, 75, r.randint(1, 9) * 10])
    return mcq("Write %s cm in metres and centimetres." % comma(a), "%d m %d cm" % (a // 100, a % 100), ["%d m %d cm" % (a // 10, a % 10) if a % 10 else "%d m" % (a // 10),
               "%d m %d cm" % (a // 100 + 1, a % 100), "%d m" % (a // 100)], "100 cm = 1 m, so %s cm = <b>%d m %d cm</b>." % (comma(a), a // 100, a % 100))


def one_cmp(r):
    for _ in range(50):
        k = r.randrange(3)
        if k == 0:
            km, m = r.randint(1, 9), r.randint(1, 9) * 100
            other = km * 1000 + m + r.choice([-1, 1]) * r.choice([50, 100, 200, 400])
            A, B, va, vb = "%d km %d m" % (km, m), "%s m" % comma(other), km * 1000 + m, other
            why = "%s = %s m." % (A, comma(va))
        elif k == 1:
            mm, cm = r.randint(1, 9) * 10 + r.randint(1, 9), 0
            cm = mm // 10 + r.choice([-1, 1])
            A, B, va, vb = "%d mm" % mm, "%d cm" % cm, mm, cm * 10
            why = "%d cm = %d mm." % (cm, cm * 10)
        else:
            mt, c = r.randint(1, 5), r.randint(10, 90)
            other = mt * 100 + c + r.choice([-1, 1]) * r.choice([5, 10, 20, 30])
            A, B, va, vb = "%d m %d cm" % (mt, c), "%d cm" % other, mt * 100 + c, other
            why = "%s = %d cm." % (A, va)
        if va != vb and vb > 0:
            break
    big = A if va > vb else B
    if r.random() < 0.5:
        A, B = B, A
    return mcq("Which is longer: %s or %s?" % (A, B), big, [A if big == B else B, "They are the same", "You cannot compare them"],
               "%s So <b>%s</b> is longer." % (why, big))


TRIPS = [("Mumbai", "Pune", 150), ("Chennai", "Puducherry", 150), ("Delhi", "Jaipur", 280), ("Kolkata", "Digha", 185), ("Bengaluru", "Mysuru", 145),
         ("Lucknow", "Kanpur", 90), ("Ahmedabad", "Vadodara", 110), ("Hyderabad", "Warangal", 145), ("Delhi", "Agra", 230), ("Chennai", "Vellore", 140)]


def one_trip(r):
    k = Kid(r).next()
    a, b, D = r.choice(TRIPS)
    t = r.randrange(4)
    if t == 0:
        x, y = r.randint(12, 95) * 1000 + r.choice([0, 250, 500]), r.randint(3, 40) * 1000 + r.choice([0, 250, 750])
        tot = x + y
        return mcq("%s’s family drives %s m before lunch and %s m after lunch. How many kilometres is that in all?" % (k["n"], comma(x), comma(y)), "%g km" % (tot / 1000),
                   ["%g km" % (abs(x - y) / 1000), "%g km" % (tot / 100), "%s km" % comma(tot)], "%s + %s = %s m = <b>%g km</b>." % (comma(x), comma(y), comma(tot), tot / 1000))
    if t == 1:
        d = D
        return mcq("It is about %d km from %s to %s. %s goes there and comes back the same way. How far does %s travel?" % (d, a, b, k["n"], k["he"]), "%d km" % (2 * d),
                   ["%d km" % d, "%d km" % (2 * d + 10), "%d km" % (d // 2)], "There and back is 2 × %d = <b>%d km</b>." % (d, 2 * d))
    if t == 2:
        d = D
        g = r.randint(3, d // 10 - 2) * 10 + r.randint(1, 9)
        return mcq("The road from %s to %s is %d km long. The bus has gone %d km. How far is left?" % (a, b, d, g), "%d km" % (d - g),
                   ["%d km" % (d + g), "%d km" % (d - g + 10), "%d km" % g], "%d − %d = <b>%d km</b>." % (d, g, d - g))
    lap, n = r.choice([200, 250, 400, 500]), r.randint(3, 10)
    return mcq("A school track is %d m round. %s runs %d rounds. How far does %s run?" % (lap, k["n"], n, k["he"]), "%s m" % comma(lap * n),
               ["%s m" % comma(lap + n), "%s m" % comma(lap * (n - 1)), "%s m" % comma(lap * n * 10)], "%d × %d = <b>%s m</b> (%g km)." % (lap, n, comma(lap * n), lap * n / 1000))

uk = mod("gen_uk_maths_y5_converting_units", 605050)
ca = mod("gen_caon_math_g5_metric", 605052)
unit(5, "far-and-near", 5, "M", 5, "Far and Near", "Length and Distance", "length and distance",
     "Measurement of length and distance: estimating, converting between km, m, cm and mm, and solving problems on distances (summary of NCERT Maths Mela Class 5)",
     "Class 5 Far and Near worksheet (Maths Mela Chapter 5): km, m, cm and mm, converting, comparing and distance problems. 100 questions with answers.",
     "1 km = 1,000 m.", "Convert to the same unit before comparing.",
     "<ul><li>1 km = 1,000 m, 1 m = 100 cm, 1 cm = 10 mm.</li><li>2.5 km = 2,500 m; 3 m 40 cm = 340 cm.</li></ul>",
     [('Which is farther: 2,400 m or 2 km 300 m?', ['2 km 300 m = 2,300 m'], '2,400 m')],
     [['Using 100 m = 1 km', '1,000 m make 1 km.'], ['Comparing different units', 'Change to the same unit first.']],
     [('How do I change km to m?', 'Multiply by 1,000.'), ('How do I change cm to m?', 'Divide by 100.')],
     [('Choose the unit', [co(one_unit, 14), rn(ca, "set_length", 6)]),
      ('Convert length', [rn(uk, "set_length", 14), co(one_conv, 6)]),
      ('Metres and kilometres', [co(one_conv, 20)]),
      ('Compare lengths', [co(one_cmp, 20)]),
      ('Distance problems', [co(one_trip, 20)])], 60505)
