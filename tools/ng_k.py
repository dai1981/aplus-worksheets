# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Kindergarten (the year before Primary 1, age 5 to 6; also called Nursery 2 or KG).
Numbers to 10 (counting to 20), very short sentences and a picture in almost every question.
  python3 tools/ng_k.py [number …]      seed = 150000 + number, reused modules 1580NN
"""
from ng_unit import mod, co, rs, ul, U, main, example as ex, le, both
import ng_low as L

TH_K = {"N": "Number and Numeration", "O": "Basic Operations", "A": "Patterns", "M": "Measurement", "G": "Shapes and Space", "S": "Sorting and Data"}
AUS = r"koala|kookaburra|wombat|footy|kangaroo|emu|possum|ute|cricket|swimming"


def money(fn):
    def f(r):
        L.LEVEL["MAX"] = 50
        return fn(r)
    f.__name__ = fn.__name__
    return f


def noaus(it):
    import re
    t = it["q"] + " " + " ".join(it["c"]) + " " + it.get("e", "")
    return not re.search(AUS, t, re.I) and not re.search(r"\b1 (?:red |blue |green |yellow )?(?:dots|ducks|apples|stars|balls|buttons|cups|hearts|flowers|bugs|ladybirds|fish)\b(?! are)", re.sub(r"<[^>]+>", "", t))


def units():
    c20 = mod("gen_us_math_gk_counting_to_20", 158001)
    wr = mod("gen_us_math_gk_writing_numbers_0_to_20", 158002)
    sub = mod("gen_au_maths_f_subitising", 158003)
    n20 = mod("gen_au_maths_f_numbers_to_20", 158004)
    cmp_ = mod("gen_us_math_gk_comparing_numbers", 158005)
    cc = mod("gen_au_maths_f_counting_and_comparing", 158006)
    od = mod("gen_sg_maths_p1_ordinal_numbers", 158007)
    dec = mod("gen_us_math_gk_decompose_numbers_to_10", 158008)
    m10 = mod("gen_us_math_gk_make_10", 158009)
    ppw = mod("gen_au_maths_f_part_part_whole", 158010)
    ad = mod("gen_us_math_gk_addition_within_10", 158011)
    sb = mod("gen_us_math_gk_subtraction_within_10", 158012)
    at = mod("gen_au_maths_f_adding_and_taking_away", 158013)
    a5 = mod("gen_us_math_gk_add_and_subtract_within_5", 158014)
    sh = mod("gen_au_maths_f_sharing_and_grouping", 158015)
    cl = mod("gen_us_math_gk_compare_length_and_weight", 158016)
    clm = mod("gen_au_maths_f_comparing_length_mass_capacity", 158017)
    dt = mod("gen_au_maths_f_days_and_times_of_day", 158018)
    sp = mod("gen_us_math_gk_2d_and_3d_shapes", 158019)
    ash = mod("gen_au_maths_f_shapes", 158020)
    pos = mod("gen_us_math_gk_positions", 158021)
    apos = mod("gen_au_maths_f_position", 158022)
    pat = mod("gen_au_maths_f_repeating_patterns", 158023)
    so = mod("gen_us_math_gk_sort_and_count", 158024)
    sd = mod("gen_au_maths_f_sorting_and_data", 158025)
    l10, l20 = both(le(10), noaus), both(le(20), noaus)
    na = noaus

    return [
        U("counting-to-10", "N", "Count objects up to 10; say how many; recognise small groups at a glance; match numbers to groups.",
          "Counting to 10", "Counting to 10",
          "Free kindergarten maths worksheets for Nigeria: count objects to 10, dice and ten frames, and how many at a glance. 100 picture questions with answers.",
          "Touch each one and say one number", "The last number you say tells how many.",
          [("Count 1 to 5", [rs(c20, "set_1_to_5", 14, l10), co(L.p1_count, 6, le(5))]), ("Count 6 to 10", [rs(c20, "set_6_to_10", 14, l10), co(L.p1_count, 6, le(10))]),
           ("Dice and dots", [rs(sub, "set_dice", 12, l10), rs(sub, "set_groups", 8, l10)]), ("Ten frames", [rs(sub, "set_frames", 12, l10), rs(sub, "set_parts", 8, l10)]),
           ("How many?", [rs(c20, "set_ideas", 8, l10), rs(sub, "set_find", 6, l10), co(L.p1_count, 6, le(10))])],
          ul(["Point to each thing and say one number.", "Do not count a thing two times.", "The last number you say is how many."]),
          [ex("Count the stars: ★ ★ ★ ★", ["1, 2, 3, 4"], "4")],
          [["Counting one thing two times", "Touch each thing only once."], ["Missing a thing", "Count in a line, from left to right."], ["Saying the numbers too fast", "One number for each thing."]],
          [("What comes after 9?", "10."), ("How can I count quickly?", "See small groups like 2 and 3 at a glance, then put them together."), ("What is a ten frame?", "A box with 10 spaces. A full ten frame shows 10.")]),

        U("numbers-to-20", "N", "Say, read and write numbers 0 to 20; know the order of numbers; find the number before and after.",
          "Numbers to 20", "Numbers to 20",
          "Free kindergarten maths worksheets for Nigeria: read and write numbers to 20, number names, what comes next, and teen numbers. 100 questions with answers.",
          "Numbers go up by one each time", "11 to 19 are 10 and some more.",
          [("Numbers 0 to 10", [rs(wr, "set_0_to_5", 10, l20), rs(wr, "set_6_to_10", 10, l20)]), ("Numbers 11 to 20", [rs(wr, "set_11_to_20", 12, l20), rs(n20, "set_count", 8, l20)]),
           ("Number names", [rs(wr, "set_names", 20, l20)]), ("What comes next?", [rs(n20, "set_order", 12, l20), co(L.p1_next, 8, l20)]),
           ("Teen numbers", [rs(n20, "set_teens", 12, l20), rs(c20, "set_11_to_20", 8, l20)])],
          ul(["Count on: 1, 2, 3, 4, 5 … up to 20.", "The number after is one more. The number before is one less.", "13 is 10 and 3 more."]),
          [ex("What comes after 14?", ["14, 15"], "15")],
          [["Writing 12 as 21", "The 1 (one ten) comes first: 12."], ["Mixing up 13 and 30", "Thirteen is 13. Thirty is 30."], ["Missing a number", "Say every number in order."]],
          [("How do I write eleven?", "11: a 1 and a 1."), ("What is one less than 20?", "19."), ("Why is 15 a teen number?", "It is 10 and 5 more, and its name ends in -teen.")]),

        U("comparing-numbers", "N", "Compare two groups and two numbers up to 10; use more, fewer, less and the same.",
          "Comparing Numbers: More, Fewer and the Same", "Comparing Numbers",
          "Free kindergarten maths worksheets for Nigeria: compare groups and numbers to 10 with more, fewer and the same. 100 picture questions with answers.",
          "Match them one to one", "The group with things left over has more.",
          [("Which row has more?", [rs(cmp_, "set_rows", 20, l10)]), ("Which box has fewer?", [rs(cmp_, "set_boxes", 20, l10)]),
           ("The same", [rs(cmp_, "set_same", 14, l10), rs(cc, "set_rows", 6, l10)]), ("Bigger numbers", [rs(cmp_, "set_numbers", 14, l10), rs(cc, "set_most", 6, l10)]),
           ("Number stories", [rs(cmp_, "set_stories", 14, l10), rs(cc, "set_story", 6, l10)])],
          ul(["Put the things in two lines, one under the other.", "The line that is left over has more.", "If nothing is left over, they are the same."]),
          [ex("Which is more, 6 or 4?", ["6 comes after 4 when we count"], "6")],
          [["Choosing the longer line", "Big things can make a line long. Count them."], ["Mixing up more and fewer", "Fewer means not as many."], ["Forgetting the same", "Same means equal: no one is left over."]],
          [("What does fewer mean?", "Not as many."), ("Is 7 more than 5?", "Yes. 7 comes after 5."), ("How do I check?", "Match one to one, or count both groups.")]),

        U("ordinal-numbers", "N", "Use first, second, third … tenth to give the position of people and things in a line.",
          "Ordinal Numbers: First, Second, Third", "Ordinal Numbers",
          "Free kindergarten maths worksheets for Nigeria: first, second, third up to tenth, 1st, 2nd and 3rd, and position in a line. 100 picture questions with answers.",
          "First is at the front", "Then second, third, fourth … tenth.",
          [("Who is in the line?", [rs(od, "set_queue", 20, na)]), ("1st, 2nd, 3rd", [rs(od, "set_symbols", 20, na)]),
           ("From the left, from the right", [rs(od, "set_left_right", 20, na)]), ("Before and after", [rs(od, "set_before_after", 20, na)]),
           ("Position words", [rs(od, "set_word", 14, na), rs(od, "set_queue", 6, na)])],
          ul(["Find the front of the line first.", "The first one is at the front. Then second, third and so on.", "1st means first, 2nd means second, 3rd means third."]),
          [ex("Ada, Musa and Tola stand in a line. Ada is at the front. Who is first?", ["Ada is at the front"], "Ada")],
          [["Counting from the wrong end", "Look for the front first."], ["Mixing up 3 and third", "3 tells how many. Third tells where."], ["Saying twoth", "We say second, not twoth."]],
          [("What comes after third?", "Fourth."), ("What does 5th mean?", "Fifth."), ("Is the last one in a line of 4 the fourth?", "Yes.")]),

        U("number-bonds-to-10", "O", "Break numbers up to 10 into two parts in different ways; find the missing part; make 10.",
          "Number Bonds to 10", "Number Bonds to 10",
          "Free kindergarten maths worksheets for Nigeria: number bonds and ways to make 5 and 10, part-part-whole and missing parts. 100 picture questions with answers.",
          "Two parts make the whole", "5 is 2 and 3, or 4 and 1, or 5 and 0.",
          [("Two colours", [rs(dec, "set_colours", 20, l10)]), ("Number bonds", [rs(dec, "set_bonds", 12, l10), rs(ppw, "set_bonds", 8, l10)]),
           ("Hidden parts", [rs(ppw, "set_hidden", 12, l10), rs(dec, "set_box", 8, l10)]), ("Make 10", [rs(m10, "set_fill", 10, l10), rs(m10, "set_missing", 10, l10)]),
           ("Ways and stories", [rs(dec, "set_ways", 8, l10), rs(m10, "set_pairs", 6, l10), rs(dec, "set_stories", 6, l10)])],
          ul(["The whole is the big number. The parts are the two small numbers.", "Part + part = whole.", "If you know the whole and one part, count on to find the other part."]),
          [ex("7 is 3 and what?", ["Count on from 3: 4, 5, 6, 7", "That is 4 more"], "4")],
          [["Adding the whole and the part", "The missing part is smaller than the whole."], ["Forgetting 0", "10 and 0 also make 10."], ["Counting the first part again", "Start after it: 3, then 4, 5, 6, 7."]],
          [("What makes 10 with 6?", "4."), ("How many ways can I make 5?", "0 and 5, 1 and 4, 2 and 3 (and the other way round)."), ("Why learn bonds to 10?", "They help you add and take away fast.")]),

        U("adding-to-10", "O", "Put two groups together and count how many altogether; add within 10 with pictures, ten frames and a number line.",
          "Adding to 10", "Adding to 10",
          "Free kindergarten maths worksheets for Nigeria: add within 10 with pictures, ten frames, number lines and short stories. 100 questions with answers.",
          "Put them together and count", "3 and 2 more make 5.",
          [("Put groups together", [rs(ad, "set_groups", 14, l10), rs(at, "set_join", 6, l10)]), ("Ten frames", [rs(ad, "set_frames", 14, l10), co(L.p1_add, 6, l10)]),
           ("Hop on the line", [rs(ad, "set_line", 20, l10)]), ("Number sentences", [rs(ad, "set_sentences", 12, l10), rs(a5, "set_add", 8, l10)]),
           ("Adding stories", [rs(ad, "set_stories", 14, l10), rs(at, "set_story", 6, l10)])],
          ul(["Put the two groups together.", "Count all of them, or start at the bigger number and count on.", "3 + 2 = 5 means 3 and 2 more make 5."]),
          [ex("4 + 3 = ?", ["Start at 4", "Count on 3: 5, 6, 7"], "7")],
          [["Counting the first number again", "Start after it: 4, then 5, 6, 7."], ["Taking away instead of adding", "Plus (+) means put together."], ["Forgetting some objects", "Touch each one as you count."]],
          [("What does + mean?", "Put together; add."), ("What is 5 + 5?", "10."), ("Is 2 + 6 the same as 6 + 2?", "Yes. Both make 8.")]),

        U("taking-away-within-10", "O", "Take away from a group and count how many are left; subtract within 10 with pictures, ten frames and a number line.",
          "Taking Away within 10", "Taking Away within 10",
          "Free kindergarten maths worksheets for Nigeria: take away within 10 with crossed-out pictures, ten frames, number lines and stories. 100 questions with answers.",
          "Cross out and count what is left", "7 take away 2 leaves 5.",
          [("Cross them out", [rs(sb, "set_cross", 14, l10), rs(at, "set_take", 6, l10)]), ("Ten frames", [rs(sb, "set_frames", 20, l10)]),
           ("Hop back on the line", [rs(sb, "set_line", 20, l10)]), ("Number sentences", [rs(sb, "set_sentences", 12, l10), rs(a5, "set_sub", 8, l10)]),
           ("Take-away stories", [rs(sb, "set_stories", 14, l10), rs(a5, "set_stories", 6, l10)])],
          ul(["Start with the whole group.", "Cross out the ones that go away.", "Count the ones that are left. 6 − 2 = 4."]),
          [ex("8 − 3 = ?", ["Start at 8", "Count back 3: 7, 6, 5"], "5")],
          [["Adding instead of taking away", "Minus (−) means take away."], ["Counting the crossed-out ones", "Count only the ones that are left."], ["Counting back from the wrong place", "Start counting back after 8: 7, 6, 5."]],
          [("What does − mean?", "Take away."), ("What is 10 − 10?", "0. None are left."), ("How do I check?", "Add back: 5 + 3 = 8.")]),

        U("sharing-and-grouping", "O", "Share objects equally between two or more people; make equal groups and count them.",
          "Sharing and Grouping", "Sharing and Grouping",
          "Free kindergarten maths worksheets for Nigeria: share fairly, make equal groups and count groups with pictures. 100 questions with answers.",
          "Fair shares are the same", "Give one to each, again and again.",
          [("Share them out", [rs(sh, "set_share", 20, l20)]), ("Is it fair?", [rs(sh, "set_fair", 20, l20)]), ("Equal groups", [rs(sh, "set_groups", 20, l20)]),
           ("Count the groups", [rs(sh, "set_count", 20, l20)]), ("Sharing stories", [rs(sh, "set_story", 20, l20)])],
          ul(["Give one to each person, then one more to each, until none are left.", "Fair means everyone gets the same number.", "Equal groups have the same number in each group."]),
          [ex("Share 6 oranges between 2 children.", ["Give one each: 1, 1", "Again: 2, 2", "Again: 3, 3"], "3 each")],
          [["Giving more to one person", "Check that each one has the same."], ["Leaving some out", "Share until none are left."], ["Counting the people, not the things", "Count the things each person gets."]],
          [("What is a fair share?", "Everyone gets the same number."), ("Can 5 sweets be shared fairly by 2?", "No. 1 is left over."), ("How do I share?", "Give one to each, again and again.")]),

        U("naira-money", "M", "Know Nigerian coins and notes up to ₦50; say which is worth more; count small amounts; buy things and find change.",
          "Naira Money: Coins and Notes", "Naira Money",
          "Free kindergarten maths worksheets for Nigeria: name naira coins and notes, which is worth more, count money to ₦50 and buy things. 100 questions with answers.",
          "Look at the number on the money", "A ₦20 note is worth more than a ₦5 coin.",
          [("Name the money", [co(money(L.mo_name), 6), co(money(L.mo_which), 6), co(money(L.mo_count), 8)]), ("Which is more?", [co(money(L.mo_which), 6), co(money(L.mo_count), 14)]),
           ("Count the money", [co(money(L.mo_count), 20)]), ("Making amounts", [co(money(L.mo_make), 6), co(money(L.mo_count), 14)]),
           ("Buying things", [co(money(L.mo_add), 14), co(money(L.mo_change), 6)])],
          ul(["The number on a coin or note tells how much it is worth.", "A big coin is not always worth more. Read the number.", "To count money, start with the biggest one and count on."]),
          [ex("A ₦10 note and a ₦5 coin. How much?", ["Start with ₦10", "Count on 5: ₦15"], "₦15")],
          [["Counting the coins, not the naira", "Two coins can be ₦7, not 2."], ["Thinking a bigger coin is worth more", "Read the number on it."], ["Forgetting the ₦ sign", "Write ₦15, not just 15."]],
          [("Which coins are there?", "₦1 and ₦2 coins; ₦5 and more are notes or coins."), ("Is ₦10 more than ₦5?", "Yes."), ("How do I count money?", "Start with the biggest and count on.")]),

        U("comparing-length-weight-and-capacity", "M", "Compare two or more things by length, height, weight and capacity; use longer, shorter, taller, heavier, lighter, holds more.",
          "Long and Short, Heavy and Light", "Length, Weight and Capacity",
          "Free kindergarten maths worksheets for Nigeria: longer and shorter, taller, heavier and lighter, and which holds more. 100 picture questions with answers.",
          "Line them up at one end", "Then see which goes further.",
          [("Longer or shorter?", [rs(cl, "set_two", 12, l10), rs(clm, "set_length", 8, l10)]), ("Put them in order", [rs(cl, "set_four", 14, l10), rs(clm, "set_height", 6, l10)]),
           ("Towers", [rs(cl, "set_towers", 20, l10)]), ("Heavy or light?", [rs(cl, "set_balance", 12, l10), rs(clm, "set_mass", 8, l10)]),
           ("Which holds more?", [rs(clm, "set_capacity", 12, l10), rs(cl, "set_words", 8, l10)])],
          ul(["Line things up at the same start.", "The one that goes further is longer or taller.", "On a balance, the heavy side goes down."]),
          [ex("A pencil and a ruler start at the same place. The ruler goes further.", ["The ruler is longer"], "The ruler")],
          [["Not starting at the same place", "Line up the ends first."], ["Thinking big means heavy", "A big balloon is light. Use a balance."], ["Mixing up tall and long", "Tall is for standing up. Long is for lying down."]],
          [("What does heavier mean?", "It weighs more."), ("How do I compare length?", "Put the ends together and look at the other ends."), ("Which holds more, a bucket or a cup?", "A bucket.")]),

        U("days-and-times-of-day", "M", "Know morning, afternoon, evening and night; the days of the week; and the order of daily events.",
          "Days of the Week and Times of Day", "Days and Times of Day",
          "Free kindergarten maths worksheets for Nigeria: morning, afternoon and night, the order of daily events and the days of the week. 100 questions with answers.",
          "Morning, afternoon, evening, night", "A week has 7 days.",
          [("Look at the sky", [rs(dt, "set_sky", 20, na)]), ("When do we do it?", [rs(dt, "set_when", 20, na)]), ("What comes first?", [rs(dt, "set_order", 20, na)]),
           ("Days of the week", [rs(dt, "set_days", 20, na)]), ("Yesterday, today, tomorrow", [rs(dt, "set_yt", 20, na)])],
          ul(["We wake up in the morning and sleep at night.", "The days are Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday.", "Yesterday was before today. Tomorrow comes after today."]),
          [ex("Today is Tuesday. What day is tomorrow?", ["Tuesday, then Wednesday"], "Wednesday")],
          [["Mixing up yesterday and tomorrow", "Yesterday has gone. Tomorrow is coming."], ["Missing a day", "Say all 7 days in order."], ["Putting events in the wrong order", "Think: what do you do first?"]],
          [("How many days are in a week?", "7."), ("What comes after Friday?", "Saturday."), ("When is the sun high in the sky?", "In the afternoon.")]),

        U("shapes", "G", "Name and describe flat shapes (circle, triangle, square, rectangle) and solid shapes (cube, ball, box, cone, cylinder); count sides and corners.",
          "Shapes: Flat and Solid", "Shapes",
          "Free kindergarten maths worksheets for Nigeria: circles, triangles, squares and rectangles, solid shapes, sides and corners, and shapes around us. 100 picture questions with answers.",
          "Count the sides and corners", "A triangle has 3 sides. A square has 4.",
          [("Flat shapes", [rs(sp, "set_flat", 12, na), rs(ash, "set_name", 8, na)]), ("Solid shapes", [rs(sp, "set_solid", 20, na)]),
           ("Find the shape", [rs(sp, "set_find", 12, na), rs(ash, "set_find", 8, na)]), ("Sides and corners", [rs(sp, "set_sides", 12, na), rs(ash, "set_sides", 8, na)]),
           ("Shapes around us", [rs(sp, "set_around", 12, na), rs(ash, "set_env", 8, na)])],
          ul(["Flat shapes are drawn on paper. Solid shapes can be held.", "Count the straight sides and the corners.", "A circle has no corners."]),
          [ex("How many sides does a triangle have?", ["Count: 1, 2, 3"], "3")],
          [["Calling a rectangle a square", "A square has 4 sides the same length."], ["Thinking a turned square is a new shape", "Turning does not change the shape."], ["Mixing up a circle and a ball", "A circle is flat. A ball is solid."]],
          [("What shape is a football?", "A sphere (a ball)."), ("How many corners does a square have?", "4."), ("What shape is a tin of milk?", "A cylinder.")]),

        U("position-and-direction", "G", "Use position words: above, below, on, under, in, next to, between, in front of, behind, left and right.",
          "Position Words: Above, Below, In Front, Behind", "Position and Direction",
          "Free kindergarten maths worksheets for Nigeria: above and below, in and on, next to and between, in front and behind, left and right. 100 picture questions with answers.",
          "Where is it?", "Use words like above, under and next to.",
          [("Above and below", [rs(pos, "set_above", 14, na), rs(apos, "set_shelf", 6, na)]), ("Next to and between", [rs(pos, "set_next", 14, na), rs(apos, "set_line", 6, na)]),
           ("In front and behind", [rs(pos, "set_front", 14, na), rs(apos, "set_table", 6, na)]), ("In, on and under", [rs(apos, "set_box", 14, na), rs(apos, "set_words", 6, na)]),
           ("Left, right and turns", [rs(pos, "set_turn", 12, na), rs(pos, "set_shapes", 8, na)])],
          ul(["Above means higher. Below means lower.", "Between means in the middle of two things.", "Your left hand and your right hand help you with left and right."]),
          [ex("The cat is under the table. Is the cat above or below the table?", ["Under means lower"], "Below")],
          [["Mixing up left and right", "Hold up your left hand: it makes an L."], ["Mixing up in and on", "In is inside. On is on top."], ["Forgetting between", "Between needs two things, one on each side."]],
          [("What is the opposite of above?", "Below."), ("What does next to mean?", "Beside; very close."), ("What is between 2 and 4?", "3.")]),

        U("patterns", "A", "Copy, continue and make repeating patterns of colours, shapes and objects; find the missing part and the part that repeats.",
          "Repeating Patterns", "Patterns",
          "Free kindergarten maths worksheets for Nigeria: copy, continue and complete repeating patterns of colours and shapes. 100 picture questions with answers.",
          "Find the part that repeats", "Red, blue, red, blue … comes again and again.",
          [("AB patterns", [rs(pat, "set_ab", 20, na)]), ("Harder patterns", [rs(pat, "set_harder", 20, na)]), ("The part that repeats", [rs(pat, "set_unit", 20, na)]),
           ("What is missing?", [rs(pat, "set_missing", 20, na)]), ("Same pattern, new way", [rs(pat, "set_ways", 20, na)])],
          ul(["Say the pattern out loud.", "Find the part that comes again and again.", "Then say what comes next."]),
          [ex("○ △ ○ △ ○ ?", ["The part that repeats is ○ △", "After ○ comes △"], "△")],
          [["Looking only at the last one", "Look at the whole pattern."], ["Missing an ABB pattern", "Say it: ○ △ △, ○ △ △."], ["Starting again in the wrong place", "Point and say each one."]],
          [("What is a pattern?", "Something that repeats in the same order."), ("What comes after red, blue, red, blue?", "Red."), ("Can a pattern use sounds?", "Yes: clap, stamp, clap, stamp.")]),

        U("sorting-and-data", "S", "Sort objects by colour, shape, size or kind; count each group; read simple picture graphs and tally marks.",
          "Sorting and Counting", "Sorting and Data",
          "Free kindergarten maths worksheets for Nigeria: sort by colour, shape and size, find the odd one out, and read picture graphs. 100 questions with answers.",
          "Put things that are the same together", "Then count each group.",
          [("Sort and count", [rs(so, "set_count", 12, l10), rs(sd, "set_count", 8, l10)]), ("Which has the most?", [rs(so, "set_most", 12, l10), rs(sd, "set_compare", 8, l10)]),
           ("Sort by shape", [rs(so, "set_shapes", 12, l10), rs(sd, "set_rules", 8, l10)]), ("Odd one out", [rs(so, "set_odd", 20, l10)]),
           ("Picture graphs", [rs(sd, "set_read", 12, l10), rs(so, "set_stories", 8, l10)])],
          ul(["Choose a rule: colour, shape, size or kind.", "Put the things that match the rule together.", "Count each group to see which has the most."]),
          [ex("Sort: ● ■ ● ● ■. How many circles?", ["Circles: ● ● ●"], "3")],
          [["Using two rules at once", "Sort by one rule at a time."], ["Counting a thing in two groups", "Each thing goes in one group only."], ["Reading the graph from the wrong side", "Count the pictures in each row."]],
          [("What does sort mean?", "Put things that are alike together."), ("What is the odd one out?", "The one that does not belong."), ("What is a picture graph?", "A chart that uses pictures to show how many.")]),
    ]


if __name__ == "__main__":
    main("kindergarten", "Kindergarten", units, 150000, th=TH_K)
