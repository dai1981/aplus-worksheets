# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 2 (NERDC 9-Year Basic Education Curriculum). Numbers up to 200; very short sentences and many pictures.
  python3 tools/ng_p2.py [number …]      seed = 150200 + number, reused modules 1549NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex, le
import ng_p4a as A4
import ng_low as L


def money(fn):
    def f(r):
        L.LEVEL["MAX"] = 500
        return fn(r)
    f.__name__ = fn.__name__
    return f


def units():
    pv = mod("gen_uk_maths_y2_place_value", 154901)
    uspv = mod("gen_us_math_g2_place_value", 154902)
    cmp2 = mod("gen_us_math_g2_compare", 154903)
    cn = mod("gen_uk_maths_y2_counting", 154904)
    sk = mod("gen_us_math_g2_skip_counting", 154905)
    oe = mod("gen_us_math_g2_odd_even", 154906)
    asb = mod("gen_uk_maths_y2_add_sub", 154907)
    us100 = mod("gen_us_math_g2_add_sub_100", 154908)
    nb = mod("gen_uk_maths_y2_number_bonds", 154909)
    fa = mod("gen_us_math_g2_facts", 154910)
    wp = mod("gen_us_math_g2_word_problems", 154911)
    md = mod("gen_uk_maths_y2_mult_div", 154912)
    tt = mod("gen_uk_maths_y2_times_tables", 154913)
    arr = mod("gen_us_math_g2_arrays", 154914)
    fr = mod("gen_uk_maths_y2_fractions", 154915)
    sh = mod("gen_us_math_g2_shares", 154916)
    me = mod("gen_uk_maths_y2_measuring", 154917)
    usme = mod("gen_us_math_g2_measuring", 154918)
    lp = mod("gen_us_math_g2_length_problems", 154919)
    me1 = mod("gen_uk_maths_y1_measuring", 154920)
    ti = mod("gen_uk_maths_y2_time", 154921)
    ust = mod("gen_us_math_g2_time", 154922)
    shp = mod("gen_uk_maths_y2_shapes", 154923)
    ussh = mod("gen_us_math_g2_shapes", 154924)
    st = mod("gen_uk_maths_y2_statistics", 154925)
    usg = mod("gen_us_math_g2_graphs", 154926)
    lim = le(200)

    return [
        U("numbers-up-to-200", "N", "Count, read and write numbers up to 200; identify tens and units; compare and order numbers.",
          "Numbers up to 200: Tens and Units", "Numbers up to 200",
          "Free Primary 2 maths worksheets on numbers up to 200: tens and units, reading and writing numbers, place value with blocks, and comparing numbers. 100 questions with answers.",
          "Tens and units", "In 46, the 4 means 4 tens.",
          [("Tens and units", [rs(pv, "set_tens_ones", 9, lim), rs(cmp2, "set_blocks", 11, lim)]), ("Count the blocks", [rs(uspv, "set_blocks", 20, lim)]), ("Numbers in words", [rs(pv, "set_words", 6, lim), rs(cmp2, "set_places", 14, lim)]),
           ("Break up numbers", [rs(pv, "set_partition", 13, lim), rs(uspv, "set_expanded", 7, lim)]), ("Bigger or smaller?", [rs(pv, "set_compare", 10, lim), rs(cmp2, "set_symbols", 10, lim)])],
          ul(["A two-digit number has tens and units. 46 = 4 tens and 6 units.", "10 units make 1 ten. 10 tens make 1 hundred.", "To compare, look at the tens first."]),
          [ex("3 tens and 5 units", ["30 + 5"], "35"), ex("Which is bigger, 58 or 85?", ["8 tens is more than 5 tens"], "85")],
          [["Writing 305 for 3 tens and 5 units", "It is 35."], ["Mixing up 58 and 85", "The first digit is the tens."], ["Looking at the units first", "Look at the tens first."]],
          [("What is 10 tens?", "100."), ("How many tens are in 70?", "7."), ("What comes after 199?", "200.")]),

        U("counting-in-2s-5s-and-10s", "N", "Count forwards and backwards in 2s, 3s, 5s and 10s; find missing numbers in a number pattern.",
          "Counting in 2s, 3s, 5s and 10s", "Skip Counting",
          "Free Primary 2 maths worksheets on skip counting: count in 2s, 3s, 5s and 10s, find missing numbers and solve counting stories. 100 questions with answers.",
          "Add the same number each time", "2, 4, 6, 8, 10 …",
          [("Count in 2s and 5s", [rs(cn, "set_twos_fives", 20)]), ("Count in 3s", [rs(cn, "set_threes", 20)]), ("Count in 10s", [rs(cn, "set_tens", 20)]),
           ("Missing numbers", [rs(cn, "set_missing", 20)]), ("Counting stories", [rs(cn, "set_stories", 10), rs(sk, "set_stories", 10, lim)])],
          ul(["Counting in 2s: 2, 4, 6, 8, 10, …", "Counting in 5s: 5, 10, 15, 20, …", "Counting in 10s: 10, 20, 30, 40, …"]),
          [ex("5, 10, 15, ?", ["Add 5"], "20")],
          [["Adding 1 instead of the step", "Add the same step each time."], ["Missing a number", "Say the numbers out loud."], ["Counting back the wrong way", "Counting back means take away."]],
          [("Why count in 2s?", "To count pairs quickly, like shoes and eyes."), ("What comes after 45 in 5s?", "50."), ("Why count in 10s?", "To count big numbers quickly.")]),

        U("odd-and-even-numbers", "N", "Identify odd and even numbers; make pairs; find odd and even numbers in a list.",
          "Odd and Even Numbers", "Odd and Even",
          "Free Primary 2 maths worksheets on odd and even numbers: making pairs, the units digit, doubles and odd and even stories. 100 questions with answers.",
          "Even numbers make pairs", "Even: 0, 2, 4, 6, 8. Odd: 1, 3, 5, 7, 9.",
          [("Make pairs", [rs(oe, "set_pairs", 20, lim)]), ("Look at the units", [rs(oe, "set_ones_digit", 20, lim)]), ("Doubles are even", [rs(oe, "set_doubles", 20, lim)]),
           ("Adding odd and even", [rs(oe, "set_sums", 20, lim)]), ("Odd and even stories", [rs(oe, "set_stories", 20, lim)])],
          ul(["An even number can be put into pairs with none left over.", "An odd number has one left over.", "Look at the units digit: 0, 2, 4, 6 and 8 are even; 1, 3, 5, 7 and 9 are odd."]),
          [ex("Is 17 odd or even?", ["Units digit 7"], "Odd")],
          [["Looking at the tens digit", "Only the units digit matters."], ["Thinking 0 is odd", "0 is even."], ["Thinking big numbers are even", "Check the units digit."]],
          [("Is 100 even?", "Yes."), ("What is odd + odd?", "Even: 3 + 5 = 8."), ("Are doubles even?", "Yes, always.")]),

        U("addition", "O", "Add 2-digit numbers with and without exchanging; know addition facts to 20; add three numbers.",
          "Addition of 2-Digit Numbers", "Addition",
          "Free Primary 2 maths worksheets on addition: addition facts to 20, adding tens, adding 2-digit numbers with and without exchanging, and adding three numbers. 100 questions with answers.",
          "Add the units, then the tens", "10 units = 1 ten.",
          [("Facts to 20", [rs(fa, "set_ten_frames", 10), rs(fa, "set_make_ten", 10)]), ("Add units", [rs(asb, "set_ones", 20, lim)]), ("Add tens", [rs(asb, "set_tens", 20, lim)]),
           ("Add 2-digit numbers", [rs(us100, "set_add", 20, lim)]), ("Add three numbers", [rs(asb, "set_three", 20, lim)])],
          ul(["Add the units first. Then add the tens.", "If the units make 10 or more, exchange 10 units for 1 ten.", "You can add numbers in any order: 7 + 5 = 5 + 7."]),
          [ex("27 + 15", ["7 + 5 = 12, write 2, carry 1", "2 + 1 + 1 = 4"], "42")],
          [["Forgetting the carried ten", "Add it to the tens."], ["Adding tens to units", "Tens under tens, units under units."], ["Counting on from the wrong number", "Start from the bigger number."]],
          [("What is a sum?", "The answer to an addition."), ("What are doubles?", "Adding a number to itself, like 6 + 6."), ("Can I add in any order?", "Yes.")]),

        U("subtraction", "O", "Subtract 2-digit numbers with and without exchanging; know subtraction facts to 20; check subtraction by addition.",
          "Subtraction of 2-Digit Numbers", "Subtraction",
          "Free Primary 2 maths worksheets on subtraction: facts to 20, fact families, subtracting tens, subtracting 2-digit numbers and checking with addition. 100 questions with answers.",
          "Take away the units, then the tens", "Check: answer + number taken = first number.",
          [("Subtraction facts", [rs(fa, "set_subtract", 20)]), ("Fact families", [rs(nb, "set_fact_families", 20)]), ("Subtract 2-digit numbers", [rs(us100, "set_sub", 20, lim)]),
           ("Subtract with exchanging", [rs(asb, "set_two", 20, lim)]), ("Check with addition", [rs(nb, "set_order_inverse", 20, lim)])],
          ul(["Take away the units first, then the tens.", "If there are not enough units, exchange 1 ten for 10 units.", "Check your answer by adding."]),
          [ex("43 − 18", ["Exchange: 13 − 8 = 5", "3 − 1 = 2"], "25")],
          [["Taking the small digit from the big one", "In 43 − 18 do 13 − 8, not 8 − 3."], ["Forgetting to exchange", "Cross out the ten and write one less."], ["Subtracting in the wrong order", "The bigger number comes first."]],
          [("What is the difference?", "The answer to a subtraction."), ("How do I check?", "Add the answer and the number you took away."), ("What is 20 − 20?", "0.")]),

        U("addition-and-subtraction-word-problems", "O", "Solve word problems on addition and subtraction of numbers up to 100.",
          "Addition and Subtraction Word Problems", "Word Problems",
          "Free Primary 2 maths worksheets on addition and subtraction word problems up to 100: altogether, how many left, how many more and missing numbers. 100 questions with answers.",
          "Altogether: add. Left: take away.", "Read the story two times.",
          [("Add or take away?", [rs(wp, "set_result", 20, lim)]), ("Parts and the whole", [rs(wp, "set_parts", 20, lim)]), ("Stories", [rs(asb, "set_words", 20, lim)]),
           ("Number bonds stories", [rs(nb, "set_words", 16, lim), rs(fa, "set_stories", 4, lim)]), ("Missing numbers", [rs(us100, "set_missing", 20, lim)])],
          ul(["Read the story. Find the numbers.", "Altogether and in all mean add. Left and how many more mean subtract.", "Write a number sentence and solve it."]),
          [ex("Ada has 35 sweets. She gives away 12. How many are left?", ["35 − 12"], "23 sweets")],
          [["Adding when things are taken away", "Left means take away."], ["Forgetting the unit", "Write sweets, pupils or naira."], ["Using the wrong numbers", "Underline the numbers."]],
          [("What does altogether mean?", "Add them up."), ("What does left mean?", "Take away."), ("Should I check my answer?", "Yes. Does it make sense?")]),

        U("multiplication", "O", "Understand multiplication as repeated addition and equal groups; use arrays; know the 2, 5 and 10 times tables.",
          "Multiplication: Equal Groups and Times Tables", "Multiplication",
          "Free Primary 2 maths worksheets on multiplication: equal groups, repeated addition, arrays and the 2, 5 and 10 times tables. 100 questions with answers.",
          "3 × 4 means 3 groups of 4", "Multiplication is repeated addition.",
          [("Equal groups", [rs(md, "set_groups", 15), rs(arr, "set_add_rows", 5)]), ("Arrays", [rs(md, "set_arrays", 10), rs(arr, "set_rows_cols", 10)]), ("2 times table", [rs(tt, "set_two", 20)]),
           ("5 times table", [rs(tt, "set_five", 20)]), ("10 times table", [rs(tt, "set_ten", 20)])],
          ul(["3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12.", "An array shows rows and columns. 2 rows of 5 = 2 × 5 = 10.", "Learn the 2, 5 and 10 times tables by counting in 2s, 5s and 10s."]),
          [ex("4 groups of 5", ["5 + 5 + 5 + 5"], "4 × 5 = 20")],
          [["Adding the two numbers", "3 × 4 = 12, not 7."], ["Groups that are not equal", "Every group must be the same."], ["Counting rows only", "Count the rows and the columns."]],
          [("What is 1 × 7?", "7."), ("What is 0 × 5?", "0."), ("Is 2 × 5 the same as 5 × 2?", "Yes, both are 10.")]),

        U("division", "O", "Share objects equally; make equal groups; relate division to multiplication; solve simple division problems.",
          "Division: Sharing Equally and Grouping", "Division",
          "Free Primary 2 maths worksheets on division: sharing equally, making equal groups, division facts for 2, 5 and 10, and division stories. 100 questions with answers.",
          "Share equally", "12 ÷ 3 = 4: 12 shared into 3 groups is 4 each.",
          [("Share and group", [rs(md, "set_share_group", 20)]), ("True or false?", [rs(md, "set_statements", 20)]), ("Division stories", [rs(md, "set_story", 20)]),
           ("Share sweets", [co(A4.div_share, 20, le(60))]), ("Multiply or divide?", [rs(tt, "set_words", 20)])],
          ul(["Division means sharing equally. 10 ÷ 2 = 5: 10 sweets shared by 2 children is 5 each.", "Division also means making equal groups: 10 ÷ 2 = 5 groups of 2.", "Use the times tables to divide."]),
          [ex("15 oranges shared by 5 children", ["15 ÷ 5"], "3 each")],
          [["Unequal sharing", "Everyone gets the same."], ["Mixing up the numbers", "The big number is shared."], ["Forgetting to check", "Multiply to check: 3 × 5 = 15."]],
          [("What is the sign for divide?", "÷."), ("What is 20 ÷ 10?", "2."), ("Is sharing the same as dividing?", "Yes.")]),

        U("fractions", "N", "Identify halves, quarters and thirds of shapes and groups of objects; find half and a quarter of a number.",
          "Fractions: Halves, Quarters and Thirds", "Fractions",
          "Free Primary 2 maths worksheets on fractions: halves, quarters and thirds of shapes and groups, and half and quarter of a number. 100 questions with answers.",
          "Equal parts", "Half: 2 equal parts. Quarter: 4 equal parts.",
          [("Equal parts", [rs(fr, "set_parts", 10), rs(sh, "set_equal", 10)]), ("Quarters", [rs(fr, "set_quarters", 20)]), ("Fractions of shapes", [rs(sh, "set_names", 20)]),
           ("Fractions of groups", [rs(fr, "set_objects", 20)]), ("Half and quarter of a number", [rs(fr, "set_quantity", 20)])],
          ul(["A half is one of 2 equal parts: 1/2.", "A quarter is one of 4 equal parts: 1/4. A third is one of 3 equal parts: 1/3.", "Half of 8 is 4. A quarter of 8 is 2."]),
          [ex("Half of 12", ["12 ÷ 2"], "6")],
          [["Parts that are not equal", "Halves must be the same size."], ["Thinking 1/4 is bigger than 1/2", "More parts are smaller parts."], ["Counting all the parts", "1/4 is just one part."]],
          [("How many halves make a whole?", "Two."), ("How many quarters make a whole?", "Four."), ("Which is bigger, a half or a quarter?", "A half.")]),

        U("money", "M", "Recognise naira notes and coins; count money up to ₦500; add amounts of money; give change.",
          "Money: Naira Notes and Coins", "Money",
          "Free Primary 2 maths worksheets on Nigerian money: naira notes and coins up to ₦500, counting money, which is worth more, shopping and change. 100 questions with answers.",
          "Count the biggest note first", "Change = money paid − price.",
          [("Name the money", [co(money(L.mo_name), 7), co(money(L.mo_which), 13)]), ("Count the money", [co(money(L.mo_count), 20)]), ("Shopping", [co(money(L.mo_add), 20)]),
           ("Change", [co(money(L.mo_change), 20)]), ("Buy more than one", [co(money(L.mo_mult), 14), co(money(L.mo_make), 6)])],
          ul(["Our money is the naira (₦). We have coins (₦1, ₦2) and notes (₦5, ₦10, ₦20, ₦50, ₦100, ₦200, ₦500).", "Count the note with the biggest value first, then count on.", "Change is what you get back."]),
          [ex("₦100 + ₦50 + ₦20", ["Count on"], "₦170")],
          [["Counting the number of notes", "Count the value of each note."], ["Adding to find change", "Take away to find change."], ["Forgetting ₦", "Write the naira sign."]],
          [("Which is worth more, ₦20 or ₦50?", "₦50."), ("How many ₦10 make ₦50?", "Five."), ("What is change?", "Money you get back.")]),

        U("length", "M", "Compare and measure lengths using non-standard units and centimetres and metres; solve length problems.",
          "Length: Measuring in Centimetres and Metres", "Length",
          "Free Primary 2 maths worksheets on length: comparing lengths, measuring with a ruler in centimetres, metres, and length word problems. 100 questions with answers.",
          "Start at 0 on the ruler", "Short things in cm, long things in m.",
          [("Units of length", [rs(me1, "set_units", 10), rs(me1, "set_compare", 10)]), ("Read the ruler", [rs(me, "set_length", 20)]), ("Longer and shorter", [rs(usme, "set_longer", 20)]),
           ("Length problems", [rs(lp, "set_join", 10), rs(lp, "set_take_compare", 10)]), ("Jumps on a number line", [rs(lp, "set_jumps", 20)])],
          ul(["We measure length with a ruler or a tape measure.", "Short things are measured in centimetres (cm). Long things are measured in metres (m).", "Put the 0 of the ruler at the end of the object."]),
          [ex("A ribbon is 25 cm. Another is 18 cm.", ["25 − 18"], "7 cm longer")],
          [["Starting at 1 on the ruler", "Start at 0."], ["Using cm for a long road", "Use metres or kilometres."], ["Not lining up the ends", "Line up one end at 0."]],
          [("What do we use to measure length?", "A ruler or a tape measure."), ("How many cm in 1 m?", "100."), ("What is longer, 1 m or 50 cm?", "1 m.")]),

        U("weight-and-capacity", "M", "Compare weights and capacities; read simple scales in kilograms and litres; solve simple problems.",
          "Weight and Capacity", "Weight and Capacity",
          "Free Primary 2 maths worksheets on weight and capacity: heavier and lighter, kilograms, reading scales, full and empty, and litres. 100 questions with answers.",
          "Heavier goes down on a balance", "Capacity: how much a container holds.",
          [("Heavier or lighter?", [rs(me1, "set_mass", 20)]), ("Read the scale", [rs(me, "set_mass", 20)]), ("Full and empty", [rs(me1, "set_capacity", 20)]),
           ("Litres", [rs(me, "set_capacity", 20)]), ("Problems", [rs(me, "set_story", 20)])],
          ul(["On a balance, the heavier side goes down.", "We weigh heavy things in kilograms (kg).", "Capacity is how much a container holds. We measure it in litres (l)."]),
          [ex("A bucket holds 10 litres. A cup holds less.", ["The bucket holds more"], "The bucket")],
          [["Thinking big things are always heavy", "Weigh them to check."], ["Reading the wrong mark", "Count the marks carefully."], ["Thinking a tall cup holds more", "A wide one may hold more."]],
          [("Which is heavier, a yam or a pencil?", "A yam."), ("What is a litre?", "A unit for measuring liquids."), ("What does kg mean?", "Kilogram.")]),

        U("time", "M", "Tell the time to the hour, half hour and quarter hour; know the days of the week.",
          "Telling the Time: Hours, Half Hours and Quarters", "Time",
          "Free Primary 2 maths worksheets on telling the time: o'clock, half past, quarter past and quarter to, matching clocks and time problems. 100 questions with answers.",
          "Long hand at 12: o'clock", "Long hand at 6: half past.",
          [("O'clock and half past", [rs(ust, "set_hour_half", 20)]), ("Quarter past and quarter to", [rs(ti, "set_quarters", 20)]), ("Minutes past", [rs(ti, "set_past", 20)]),
           ("Match the clocks", [rs(ti, "set_match", 20)]), ("Time problems", [rs(ti, "set_problems", 20)])],
          ul(["The short hand shows the hour. The long hand shows the minutes.", "When the long hand points to 12, it is o'clock. When it points to 6, it is half past.",
              "When the long hand points to 3, it is quarter past. When it points to 9, it is quarter to."]),
          [ex("Short hand between 7 and 8, long hand at 6", ["Half past"], "half past 7")],
          [["Mixing up the hands", "The short hand is the hour."], ["Reading quarter to as quarter past", "Quarter to is before the hour."], ["Saying 6 o'clock for half past", "The long hand at 6 means half past."]],
          [("How many minutes in an hour?", "60."), ("How many minutes in half an hour?", "30."), ("When do we go to school?", "In the morning.")]),

        U("shapes", "G", "Identify and describe 2D shapes and 3D shapes; count sides, corners and faces; find shapes in the environment.",
          "2D and 3D Shapes", "Shapes",
          "Free Primary 2 maths worksheets on shapes: circles, triangles, squares and rectangles, sides and corners, cubes, cuboids, cylinders, cones and spheres, and faces. 100 questions with answers.",
          "Flat shapes are 2D, solid shapes are 3D", "Count the sides and corners.",
          [("2D shapes", [rs(shp, "set_2d", 20)]), ("Name the shape", [rs(ussh, "set_name", 20)]), ("3D shapes", [rs(shp, "set_3d", 20)]),
           ("Faces", [rs(shp, "set_faces", 20)]), ("Shapes around us", [rs(ussh, "set_world", 20)])],
          ul(["2D shapes are flat: circle, triangle, square, rectangle.", "3D shapes are solid: cube, cuboid, cylinder, cone, sphere.", "A triangle has 3 sides and 3 corners. A square has 4 equal sides."]),
          [ex("A shape with 4 sides, 2 long and 2 short", ["4 square corners"], "Rectangle")],
          [["Calling a cube a square", "A cube is solid."], ["Thinking a circle has corners", "A circle has no corners."], ["Mixing up cone and cylinder", "A cone has a point."]],
          [("How many sides has a triangle?", "3."), ("What shape is a ball?", "A sphere."), ("What shape is a tin of milk?", "A cylinder.")]),

        U("pictograms", "S", "Collect data using tally marks; read and make pictograms and block graphs; answer questions from the data.",
          "Pictograms and Tally Charts", "Pictograms",
          "Free Primary 2 maths worksheets on data: tally marks, pictograms where one picture stands for one or more things, block graphs and data questions. 100 questions with answers.",
          "One picture can stand for 2 or more", "Read the key.",
          [("Tally marks", [rs(st, "set_tally", 20)]), ("Pictograms", [rs(st, "set_pic1", 20)]), ("Pictograms with a key", [rs(st, "set_pic_key", 20)]),
           ("Block graphs", [rs(st, "set_block_table", 20)]), ("Picture graphs", [rs(usg, "set_picture", 20)])],
          ul(["A tally mark | stands for one thing. Five is drawn as |||| with a line across.", "A pictogram uses pictures. The key tells what one picture means.", "Count and compare: which has the most? which has the least?"]),
          [ex("Key: 1 picture = 2 children. Rice has 3 pictures", ["3 × 2"], "6 children")],
          [["Forgetting the key", "Use the key."], ["Counting tallies one by one", "Count in fives."], ["Reading the wrong row", "Use your finger to follow the row."]],
          [("What is a tally?", "A mark to count things."), ("What is a pictogram?", "A chart with pictures."), ("What does most mean?", "The biggest number.")]),
    ]


if __name__ == "__main__":
    main("primary-2", "Primary 2", units, 150200)
