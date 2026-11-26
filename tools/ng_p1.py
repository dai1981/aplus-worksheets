# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 1 (NERDC 9-Year Basic Education Curriculum). Numbers 0 to 100, adding and taking away to 20.
Very short sentences and pictures in almost every question.
  python3 tools/ng_p1.py [number …]      seed = 150100 + number, reused modules 1559NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex, le
import ng_low as L


def money(fn):
    def f(r):
        L.LEVEL["MAX"] = 100
        return fn(r)
    f.__name__ = fn.__name__
    return f


def units():
    cnt = mod("gen_uk_maths_y1_counting", 155901)
    c120 = mod("gen_us_math_g1_count_120", 155902)
    pv = mod("gen_us_math_g1_place_value", 155903)
    cmp1 = mod("gen_us_math_g1_compare", 155904)
    st = mod("gen_uk_maths_y1_counting_in_steps", 155905)
    nb = mod("gen_uk_maths_y1_number_bonds", 155906)
    as1 = mod("gen_uk_maths_y1_add_sub", 155907)
    a20 = mod("gen_us_math_g1_add_sub_20", 155908)
    a3 = mod("gen_us_math_g1_add_three", 155909)
    strat = mod("gen_us_math_g1_strategies", 155910)
    wp = mod("gen_us_math_g1_word_problems", 155911)
    hq = mod("gen_uk_maths_y1_halves_quarters", 155912)
    hf = mod("gen_us_math_g1_halves_fourths", 155913)
    dat = mod("gen_us_math_g1_data", 155914)
    me = mod("gen_uk_maths_y1_measuring", 155915)
    usme = mod("gen_us_math_g1_measuring", 155916)
    ti = mod("gen_uk_maths_y1_time", 155917)
    ust = mod("gen_us_math_g1_time", 155918)
    sh = mod("gen_uk_maths_y1_shapes", 155919)
    ussh = mod("gen_us_math_g1_shapes", 155920)
    st2 = mod("gen_uk_maths_y2_statistics", 155921)
    l20, l100 = le(20), le(100)
    J = lambda r: wp.Ctx(r, wp.JOIN)
    Pc = lambda r: wp.Ctx(r, wp.PARTS)
    Cc = lambda r: wp.Ctx(r, wp.CMP)

    return [
        U("counting-objects", "N", "Count objects from 1 to 20; match numbers to groups of objects; read and write numbers 0 to 20.",
          "Counting Objects up to 20", "Counting Objects",
          "Free Primary 1 maths worksheets on counting objects up to 20 with pictures, one more and one less, and counting in real life. 100 questions with answers.",
          "Touch each object once", "The last number you say is how many.",
          [("Count the objects", [rs(cnt, "set_count", 6, l20), co(L.p1_count, 14)]), ("Count the pictures", [rs(c120, "set_objects", 3, l20), co(L.p1_count, 17)]), ("One more, one less", [rs(cnt, "set_more_less", 6, l20), co(L.p1_next, 14, l20)]),
           ("Count across", [rs(cnt, "set_across", 4, l20), co(L.p1_count, 16)]), ("Counting around us", [rs(cnt, "set_life", 20, l20)])],
          ul(["Point to each object and say one number for each.", "The last number you say tells you how many there are.", "One more means the next number. One less means the number before."]),
          [ex("Count: ● ● ● ● ● ●", ["1, 2, 3, 4, 5, 6"], "6")],
          [["Counting an object twice", "Touch each one only once."], ["Missing an object", "Cross them out as you count."], ["Saying the numbers too fast", "Say one number for each object."]],
          [("What comes after 9?", "10."), ("What is one less than 15?", "14."), ("How do I count quickly?", "Count in groups of 2 or 5.")]),

        U("numbers-up-to-100", "N", "Count, read and write numbers up to 100; find numbers before, after and between; use a hundred square.",
          "Numbers up to 100", "Numbers up to 100",
          "Free Primary 1 maths worksheets on numbers up to 100: counting on, what comes next, numbers before and after, the hundred square and number stories. 100 questions with answers.",
          "Count on: add 1 each time", "After 29 comes 30.",
          [("What comes next?", [rs(c120, "set_next", 9, l100), co(L.p1_next, 11)]), ("Hundred square", [co(L.p1_chart, 20)]), ("Number words", [rs(c120, "set_words", 13, l100), co(L.p1_word, 7)]),
           ("Compare numbers", [rs(cnt, "set_compare", 20, l100)]), ("Number stories", [rs(c120, "set_stories", 20, l100)])],
          ul(["Count on from any number: 47, 48, 49, 50.", "After 9 units, the tens go up: 39, 40.", "On a hundred square, each row is 10 more than the row above."]),
          [ex("What comes after 59?", ["9 units, then a new ten"], "60")],
          [["Saying twenty-ten", "After 29 comes 30."], ["Writing 13 for 31", "Thirty-one is 3 tens and 1 unit."], ["Skipping numbers", "Say every number."]],
          [("What comes after 99?", "100."), ("What is between 40 and 42?", "41."), ("How many tens are in 100?", "10.")]),

        U("tens-and-units", "N", "Identify tens and units in numbers up to 99; use bundles and blocks; write numbers as tens and units.",
          "Tens and Units (Place Value)", "Tens and Units",
          "Free Primary 1 maths worksheets on place value: tens and units with blocks and bundles of sticks, teen numbers, digits and decades. 100 questions with answers.",
          "Tens on the left, units on the right", "34 = 3 tens and 4 units.",
          [("Count the blocks", [rs(pv, "set_blocks", 20, l100)]), ("Teen numbers", [rs(pv, "set_teens", 12, l100), co(L.p1_rods, 8)]), ("Tens and units digits", [rs(pv, "set_digits", 20, l100)]),
           ("Groups of ten", [rs(pv, "set_decades", 10, l100), co(L.p1_rods, 10)]), ("Place value stories", [co(L.p1_tu_word, 20)])],
          ul(["10 units make 1 ten.", "In 34, the 3 means 3 tens (30) and the 4 means 4 units.", "Teen numbers have 1 ten: 16 = 1 ten and 6 units."]),
          [ex("5 tens and 2 units", ["50 + 2"], "52")],
          [["Mixing up the digits", "The tens digit is first."], ["Writing 502 for 5 tens and 2 units", "It is 52."], ["Counting blocks one by one", "Count the tens first."]],
          [("How many units in 1 ten?", "10."), ("What is 7 tens?", "70."), ("What is the tens digit of 85?", "8.")]),

        U("comparing-numbers", "N", "Compare numbers up to 100 using more than, less than and equal to; arrange numbers in order.",
          "Comparing Numbers: More, Less and Equal", "Comparing Numbers",
          "Free Primary 1 maths worksheets on comparing numbers up to 100: more than, less than, equal to, the signs &gt;, &lt; and =, and putting numbers in order. 100 questions with answers.",
          "Look at the tens first", "&gt; is more than, &lt; is less than.",
          [("Compare blocks", [rs(cmp1, "set_blocks", 20, l100)]), ("Tens and units", [rs(cmp1, "set_places", 20, l100)]), ("Use &gt;, &lt; and =", [rs(cmp1, "set_symbols", 15, l100), co(L.p1_cmp, 5)]),
           ("Put in order", [rs(cmp1, "set_order", 20, l100)]), ("Comparing stories", [rs(cmp1, "set_words", 20, l100)])],
          ul(["Look at the tens first. The number with more tens is bigger.", "If the tens are the same, look at the units.", "&gt; means is more than. &lt; means is less than. = means is the same as."]),
          [ex("Compare 47 and 74", ["4 tens is less than 7 tens"], "47 &lt; 74")],
          [["Looking at the units first", "Look at the tens first."], ["Turning the sign the wrong way", "The open mouth eats the bigger number."], ["Thinking 19 is more than 21", "21 has more tens."]],
          [("What does = mean?", "Is the same as."), ("Which is more, 60 or 59?", "60."), ("How do I order numbers?", "Start with the smallest.")]),

        U("counting-in-2s-5s-and-10s", "N", "Count in 2s, 5s and 10s; count groups of objects; find missing numbers in counting patterns.",
          "Counting in 2s, 5s and 10s", "Counting in 2s, 5s and 10s",
          "Free Primary 1 maths worksheets on counting in 2s, 5s and 10s with pictures of pairs, hands and bundles, groups and counting stories. 100 questions with answers.",
          "Add the same number each time", "2, 4, 6, 8, 10",
          [("Count in 2s", [rs(st, "set_twos", 15), co(L.p1_twos, 5)]), ("Count in 5s", [rs(st, "set_fives", 15), co(L.p1_twos, 5)]), ("Count in 10s", [rs(st, "set_tens", 15), co(L.p1_twos, 5)]),
           ("Count the groups", [rs(st, "set_groups", 16), co(L.p1_rods, 4)]), ("Counting stories", [rs(st, "set_stories", 20)])],
          ul(["Count in 2s: 2, 4, 6, 8, 10.", "Count in 5s: 5, 10, 15, 20.", "Count in 10s: 10, 20, 30, 40."]),
          [ex("How many eyes do 4 children have?", ["2, 4, 6, 8"], "8")],
          [["Counting in 1s", "Jump by the same number."], ["Missing a jump", "Count the groups too."], ["Stopping too soon", "Count every group."]],
          [("How many fingers on 3 hands?", "15."), ("What comes after 30 in 10s?", "40."), ("Why count in 2s?", "To count pairs quickly.")]),

        U("addition", "O", "Add numbers up to 20 using objects, number lines and number bonds; add three small numbers.",
          "Addition up to 20", "Addition",
          "Free Primary 1 maths worksheets on addition up to 20: adding with pictures, number bonds to 10 and 20, making 10, doubles and adding three numbers. 100 questions with answers.",
          "Put together to add", "Start with the bigger number and count on.",
          [("Add to 10", [rs(a20, "set_add10", 20, l20)]), ("Number bonds to 10", [rs(nb, "set_frames", 10, l20), rs(nb, "set_pairs", 10, l20)]), ("Make 10", [rs(a20, "set_make10", 14, l20), co(L.p1_ten, 6)]),
           ("Doubles", [rs(a20, "set_doubles", 20, l20)]), ("Add three numbers", [rs(a3, "set_pictures", 10, l20), rs(a3, "set_within_20", 10, l20)])],
          ul(["Adding means putting together. 4 + 3 = 7.", "Count on from the bigger number: 8 + 3 → 9, 10, 11.", "Number bonds to 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6, 5 + 5."]),
          [ex("6 + 5", ["Start at 6, count on 5"], "11")],
          [["Counting the first number again", "Start counting after the first number."], ["Starting from the smaller number", "Start with the bigger one."], ["Forgetting a number", "Add all the numbers."]],
          [("What is a double?", "A number added to itself, like 4 + 4."), ("What is 0 + 7?", "7."), ("Does 3 + 5 equal 5 + 3?", "Yes, both are 8.")]),

        U("subtraction", "O", "Subtract numbers up to 20 by taking away and counting back; find the difference; use related addition facts.",
          "Subtraction up to 20", "Subtraction",
          "Free Primary 1 maths worksheets on subtraction up to 20: taking away with pictures, counting back, missing numbers and number sentences. 100 questions with answers.",
          "Take away to subtract", "Count back on a number line.",
          [("Take away", [rs(a20, "set_sub10", 20, l20)]), ("Subtract to 20", [rs(a20, "set_sub20", 20, l20)]), ("Subtraction from bonds", [rs(nb, "set_subtraction", 13, l20), co(L.p1_sub, 7)]),
           ("Number sentences", [rs(as1, "set_sentences", 15, l20), co(L.p1_bond, 5)]), ("Missing numbers", [rs(as1, "set_missing", 20, l20)])],
          ul(["Subtracting means taking away. 9 − 4 = 5.", "Count back on a number line: 12 − 3 → 11, 10, 9.", "Use addition to help: 6 + 4 = 10, so 10 − 4 = 6."]),
          [ex("15 − 6", ["Count back 6 from 15"], "9")],
          [["Counting the start number", "Start counting back from the next number."], ["Taking away the bigger number", "In 9 − 4 we take 4 from 9."], ["Adding instead of taking away", "Look at the sign: − means take away."]],
          [("What is 10 − 10?", "0."), ("What is 8 − 0?", "8."), ("How can addition help?", "If 5 + 3 = 8, then 8 − 3 = 5.")]),

        U("addition-and-subtraction-word-problems", "O", "Solve simple word problems on adding and taking away numbers up to 20.",
          "Addition and Subtraction Stories", "Word Problems",
          "Free Primary 1 maths worksheets on addition and subtraction stories up to 20: putting together, taking away, parts of a whole and comparing. 100 questions with answers.",
          "Put together: add. Take away: subtract.", "Read the story slowly.",
          [("Join and take away", [rs(wp, "set_result", 20, l20, J=J)]), ("Parts and the whole", [rs(wp, "set_parts", 20, l20, Pc=Pc)]), ("How many more?", [rs(wp, "set_compare", 20, l20, Cc=Cc)]),
           ("Bonds stories", [rs(nb, "set_stories", 20, l20)]), ("Adding stories", [rs(a3, "set_word_problems", 10, l20), rs(as1, "set_words", 10, l20)])],
          ul(["Read the story and find the numbers.", "If things are put together, add. If things are taken away, subtract.", "How many more? Subtract the smaller number from the bigger number."]),
          [ex("Tolu has 8 mangoes. She eats 3. How many are left?", ["8 − 3"], "5 mangoes")],
          [["Adding when some are taken away", "Left means take away."], ["Forgetting what we are counting", "Say the answer with the word: 5 mangoes."], ["Using the wrong numbers", "Look again at the story."]],
          [("What does left mean?", "What is still there after some go away."), ("What does altogether mean?", "Add them."), ("How do I check?", "Use counters or fingers.")]),

        U("halves-and-quarters", "N", "Identify halves and quarters of shapes and objects; share objects into two and four equal groups.",
          "Halves and Quarters", "Halves and Quarters",
          "Free Primary 1 maths worksheets on halves and quarters: equal parts, half of a shape, quarter of a shape, half and quarter of a group, and stories. 100 questions with answers.",
          "Half: 2 equal parts", "Quarter: 4 equal parts.",
          [("Equal parts", [rs(hq, "set_equal", 10), rs(hf, "set_equal", 10)]), ("Halves", [rs(hq, "set_halves", 20)]), ("Quarters", [rs(hq, "set_quarters", 10), rs(hf, "set_fourths", 10)]),
           ("Half and quarter of a group", [rs(hq, "set_amounts", 20)]), ("Stories", [rs(hq, "set_stories", 10), rs(hf, "set_stories", 10)])],
          ul(["A half is one of 2 equal parts.", "A quarter is one of 4 equal parts.", "To find half of 8 sweets, share them into 2 equal groups: 4 each."]),
          [ex("Half of 10", ["Share into 2 groups"], "5")],
          [["Parts that are not equal", "Halves must be the same size."], ["Thinking a quarter is bigger than a half", "A quarter is smaller."], ["Counting all the parts", "A half is just one part."]],
          [("How many halves make one whole?", "2."), ("How many quarters make one whole?", "4."), ("What is half of 6?", "3.")]),

        U("sorting-and-pictograms", "S", "Sort and classify objects by colour, shape and size; count and record data; read simple pictograms.",
          "Sorting, Classifying and Pictograms", "Sorting and Pictograms",
          "Free Primary 1 maths worksheets on sorting and classifying objects, tally marks, picture graphs and simple bar graphs. 100 questions with answers.",
          "Sort things that are the same", "Count each group.",
          [("Sort the objects", [rs(dat, "set_sort", 20)]), ("Tally marks", [rs(dat, "set_tally", 10), rs(st2, "set_tally", 10)]), ("Picture graphs", [rs(dat, "set_picture", 20)]),
           ("Bar graphs", [rs(dat, "set_bar", 20)]), ("Answer questions", [rs(dat, "set_word", 20)])],
          ul(["Sorting means putting things that are alike together, for example by colour, shape or size.", "Count each group and write the number.", "A picture graph shows how many in each group."]),
          [ex("Sort: red ball, blue ball, red cup", ["Red things: 2"], "2 red, 1 blue")],
          [["Putting one thing in two groups", "Each thing goes in one group."], ["Miscounting the pictures", "Touch each one once."], ["Reading the wrong row", "Follow the row with your finger."]],
          [("What is sorting?", "Putting things that are alike together."), ("What is a tally?", "A mark for each thing counted."), ("Which group has most?", "The one with the biggest number.")]),

        U("money", "M", "Recognise Nigerian coins and notes up to ₦100; count small amounts of money; buy and give change.",
          "Money: Naira Coins and Notes", "Money",
          "Free Primary 1 maths worksheets on Nigerian money with pictures: naira coins and notes up to ₦100, which is worth more, counting money and simple shopping. 100 questions with answers.",
          "₦ means naira", "Count the biggest note first.",
          [("Name the money", [co(money(L.mo_name), 7), co(money(L.mo_which), 13)]), ("Which is worth more?", [co(money(L.mo_which), 7), co(money(L.mo_make), 5), co(money(L.mo_count), 8)]),
           ("Count the money", [co(money(L.mo_count), 20)]), ("Shopping", [co(money(L.mo_add), 20)]), ("Change", [co(money(L.mo_change), 20)])],
          ul(["Nigerian money is called naira (₦).", "We have coins (₦1 and ₦2) and notes (₦5, ₦10, ₦20, ₦50, ₦100).", "To count money, start with the biggest and count on."]),
          [ex("₦50 + ₦20 + ₦5", ["Count on"], "₦75")],
          [["Counting how many notes", "Count what each note is worth."], ["Thinking a big note means a big number", "Read the number on it."], ["Adding when finding change", "Change: take away."]],
          [("What is our money called?", "The naira."), ("Which is more, ₦10 or ₦20?", "₦20."), ("How many ₦10 notes make ₦20?", "2.")]),

        U("length-and-capacity", "M", "Compare lengths (long, short, tall) and capacities (full, empty, holds more, holds less); measure using hand spans, steps and cups.",
          "Length and Capacity: Comparing and Measuring", "Length and Capacity",
          "Free Primary 1 maths worksheets on comparing length, height, weight and capacity, measuring with hand spans, steps and cups, and simple problems. 100 questions with answers.",
          "Line up the ends to compare", "Full holds the most; empty holds nothing.",
          [("Longer or shorter?", [rs(me, "set_compare", 10), rs(usme, "set_compare", 10)]), ("Put in order", [rs(usme, "set_order", 20)]), ("Measure with units", [rs(me, "set_units", 10), rs(usme, "set_units", 10)]),
           ("Heavier or lighter?", [rs(me, "set_mass", 20)]), ("Holds more or less?", [rs(me, "set_capacity", 20)])],
          ul(["To compare lengths, line up the ends. The one that sticks out more is longer.", "We can measure with hand spans, steps, sticks or cubes.", "A container that holds more water has a bigger capacity."]),
          [ex("A pencil is 6 cubes long; a crayon is 4 cubes long", ["6 is more than 4"], "The pencil is longer")],
          [["Not lining up the ends", "Start at the same place."], ["Leaving gaps when measuring", "Put the units end to end."], ["Thinking tall means holds more", "Check by pouring."]],
          [("What is longer, a ruler or a pencil?", "Usually a ruler."), ("What does empty mean?", "Nothing inside."), ("Which is heavier, a book or a feather?", "A book.")]),

        U("time", "M", "Tell the time to the hour and half hour; name the days of the week; put daily events in order.",
          "Time: O'clock, Half Past and Days of the Week", "Time",
          "Free Primary 1 maths worksheets on time: o'clock and half past, matching clocks, the days of the week, and morning, afternoon and night. 100 questions with answers.",
          "Long hand at 12: o'clock", "Long hand at 6: half past.",
          [("O'clock", [rs(ti, "set_oclock", 10), rs(ust, "set_hour", 10)]), ("Half past", [rs(ti, "set_half", 10), rs(ust, "set_half", 10)]), ("Match the time", [rs(ust, "set_match", 20)]),
           ("Days of the week", [rs(ti, "set_calendar", 20)]), ("My day", [rs(ti, "set_order", 10), rs(ti, "set_life", 10)])],
          ul(["The short hand shows the hour. The long hand shows the minutes.", "When the long hand points to 12, it is o'clock. When it points to 6, it is half past.",
              "There are 7 days in a week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."]),
          [ex("Short hand at 8, long hand at 12", ["o'clock"], "8 o'clock")],
          [["Mixing up the hands", "The short hand is the hour."], ["Saying 12 o'clock for half past", "The long hand at 6 is half past."], ["Forgetting a day", "Say the days in order."]],
          [("How many days are in a week?", "7."), ("What day comes after Friday?", "Saturday."), ("When do we have breakfast?", "In the morning.")]),

        U("shapes", "G", "Identify basic shapes (circle, triangle, square, rectangle) and solid shapes (cube, cuboid, cylinder, cone, sphere); find shapes around us.",
          "Shapes: Flat and Solid", "Shapes",
          "Free Primary 1 maths worksheets on shapes: circles, triangles, squares and rectangles, flat and solid shapes, cubes, cylinders and spheres, and shapes around us. 100 questions with answers.",
          "Count the sides", "Flat shapes and solid shapes.",
          [("Flat shapes", [rs(sh, "set_name2d", 20)]), ("Same shape", [rs(sh, "set_same", 20)]), ("Solid shapes", [rs(sh, "set_name3d", 20)]),
           ("Flat or solid?", [rs(sh, "set_flat_solid", 20)]), ("Shapes around us", [rs(sh, "set_world", 20)])],
          ul(["A circle is round. A triangle has 3 sides. A square has 4 equal sides. A rectangle has 2 long and 2 short sides.", "Solid shapes: cube (like a dice), cuboid (like a box), cylinder (like a tin), cone, sphere (like a ball).",
              "We see shapes all around us."]),
          [ex("A shape with 3 sides", ["Count the sides"], "Triangle")],
          [["Calling a rectangle a square", "A square has 4 equal sides."], ["Calling a ball a circle", "A ball is a sphere."], ["Counting a corner as a side", "Sides are the straight lines."]],
          [("What shape is a wheel?", "A circle."), ("What shape is a tin of tomato paste?", "A cylinder."), ("How many sides has a square?", "4.")]),
    ]


if __name__ == "__main__":
    main("primary-1", "Primary 1", units, 150100)
