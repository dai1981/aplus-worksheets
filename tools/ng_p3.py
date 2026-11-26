# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 3 (NERDC 9-Year Basic Education Curriculum; first, second and third term order of the scheme of work).
Numbers up to 999. Short sentences and many pictures.
  python3 tools/ng_p3.py [number …]      seed = 150300 + number, reused modules 1539NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex, le
import ng_p4a as A4
import ng_low as L


def money(fn):
    def f(r):
        L.LEVEL["MAX"] = 1000
        return fn(r)
    f.__name__ = fn.__name__
    return f


def units():
    pv = mod("gen_uk_maths_y3_place_value", 153901)
    uspv = mod("gen_us_math_g2_place_value", 153902)
    oe = mod("gen_us_math_g2_odd_even", 153903)
    cmp2 = mod("gen_us_math_g2_compare", 153904)
    fr3 = mod("gen_uk_maths_y3_fractions", 153905)
    usf = mod("gen_us_math_g3_fractions", 153906)
    cas = mod("gen_uk_maths_y3_column_add_sub", 153907)
    usas = mod("gen_us_math_g3_add_sub", 153908)
    mas = mod("gen_uk_maths_y3_mental_add_sub", 153909)
    tf = mod("gen_uk_maths_y3_tenths_fractions", 153910)
    tt = mod("gen_uk_maths_y3_times_tables", 153911)
    md = mod("gen_uk_maths_y3_mult_div", 153912)
    us10 = mod("gen_us_math_g3_multiples_of_10", 153913)
    tt2 = mod("gen_uk_maths_y2_times_tables", 153914)
    me = mod("gen_uk_maths_y3_measuring", 153915)
    usme = mod("gen_us_math_g2_measuring", 153916)
    per = mod("gen_uk_maths_y3_perimeter", 153917)
    ar4 = mod("gen_uk_maths_y4_area_perimeter", 153918)
    usmv = mod("gen_us_math_g3_mass_volume", 153919)
    ti = mod("gen_uk_maths_y3_time", 153920)
    ust = mod("gen_us_math_g3_time", 153921)
    ti1 = mod("gen_uk_maths_y1_time", 153922)
    sh2 = mod("gen_uk_maths_y2_shapes", 153923)
    sh3 = mod("gen_uk_maths_y3_shapes", 153924)
    st = mod("gen_uk_maths_y3_statistics", 153925)
    st2 = mod("gen_uk_maths_y2_statistics", 153926)
    usps = mod("gen_us_math_g3_partition_shapes", 153927)
    usprop = mod("gen_us_math_g3_properties", 153928)
    usw = mod("gen_us_math_g2_word_problems", 153929)
    lim = le(999)

    return [
        U("numbers-up-to-999", "N", "Count, read and write numbers from 1 to 999 in figures and in words; identify the place value of hundreds, tens and units.",
          "Numbers up to 999: Hundreds, Tens and Units", "Numbers up to 999",
          "Free Primary 3 maths worksheets on numbers up to 999: hundreds, tens and units, reading and writing numbers in figures and words, and counting on and back. 100 questions with answers.",
          "Hundreds, tens, units", "In 472 the 4 means 400.",
          [("Hundreds, tens and units", [rs(pv, "set_hto", 20, lim)]), ("Blocks", [rs(uspv, "set_blocks", 20, lim)]), ("Numbers in words", [rs(pv, "set_words", 20, lim)]),
           ("Expanded form", [rs(uspv, "set_expanded", 20, lim)]), ("More and less", [rs(pv, "set_more_less", 15, lim), rs(uspv, "set_hto", 5, lim)])],
          ul(["A three-digit number has hundreds, tens and units: 472 = 4 hundreds, 7 tens and 2 units.", "472 = 400 + 70 + 2. We say four hundred and seventy-two.",
              "A zero keeps a place empty: 305 has 3 hundreds, 0 tens and 5 units."]),
          [ex("What is 6 hundreds, 0 tens and 8 units?", ["600 + 0 + 8"], "608"), ex("Value of 5 in 352", ["5 is in the tens place"], "50")],
          [["Writing 400702 for four hundred and seventy-two", "Write 472."], ["Forgetting the zero", "Three hundred and five is 305, not 35."], ["Mixing up tens and units", "The units digit is on the right."]],
          [("What is the biggest 3-digit number?", "999."), ("What comes after 999?", "1,000."), ("How many tens are in 100?", "Ten.")]),

        U("odd-and-even-numbers-and-comparing", "N", "Identify odd and even numbers; compare numbers up to 999 using the signs > and <; arrange numbers in order.",
          "Odd and Even Numbers; Comparing Numbers", "Odd, Even and Comparing",
          "Free Primary 3 maths worksheets on odd and even numbers and comparing numbers up to 999 with &gt; and &lt;, and putting numbers in order. 100 questions with answers.",
          "Even numbers end in 0, 2, 4, 6, 8", "Compare hundreds first.",
          [("Odd or even?", [rs(oe, "set_ones_digit", 20)]), ("Pairs", [rs(oe, "set_pairs", 20)]), ("Compare with &gt; and &lt;", [rs(cmp2, "set_symbols", 20, lim)]),
           ("Which is bigger?", [rs(pv, "set_compare", 15, lim), rs(cmp2, "set_places", 5, lim)]), ("Put in order", [rs(cmp2, "set_order", 20, lim)])],
          ul(["Even numbers can be put into pairs with none left. They end in 0, 2, 4, 6 or 8.", "Odd numbers end in 1, 3, 5, 7 or 9.",
              "To compare, look at the hundreds first, then the tens, then the units. &gt; means greater than; &lt; means less than."]),
          [ex("Compare 438 and 483", ["Same hundreds, tens: 3 &lt; 8"], "438 &lt; 483")],
          [["Looking only at the units", "Compare the hundreds first."], ["Turning the sign the wrong way", "The open mouth faces the bigger number."], ["Thinking 0 is odd", "0 is even."]],
          [("Is 100 even?", "Yes. It ends in 0."), ("Is the sum of two odd numbers odd or even?", "Even, for example 3 + 5 = 8."), ("What does &lt; mean?", "Is less than.")]),

        U("fractions", "N", "Identify halves, quarters, fifths and sixths of shapes and of collections of objects; find a fraction of a number.",
          "Fractions of Shapes and Groups", "Fractions",
          "Free Primary 3 maths worksheets on fractions: halves, thirds, quarters, fifths and sixths of shapes and groups, and fractions on a number line. 100 questions with answers.",
          "Equal parts", "1/4 means 1 of 4 equal parts.",
          [("Shaded parts", [rs(fr3, "set_shaded", 20)]), ("Fractions of shapes", [rs(usf, "set_shaded", 20)]), ("Fractions of groups", [rs(fr3, "set_objects", 20)]),
           ("Fractions of a number", [rs(tf, "set_amounts", 15), rs(fr3, "set_objects", 5)]), ("Fractions on a number line", [rs(fr3, "set_line", 20)])],
          ul(["A fraction is part of a whole that is cut into equal parts.", "The bottom number tells how many equal parts. The top number tells how many we take.",
              "To find 1/4 of 20, share 20 into 4 equal groups: 20 ÷ 4 = 5."]),
          [ex("1/5 of 30", ["30 ÷ 5"], "6"), ex("A cake cut into 6 equal parts, 1 part eaten", ["1 of 6 parts"], "1/6")],
          [["Parts that are not equal", "Fractions need equal parts."], ["Thinking 1/6 is bigger than 1/4", "More parts means smaller parts."], ["Counting the parts left instead of shaded", "Read the question carefully."]],
          [("What is one half?", "One of two equal parts."), ("Which is bigger, 1/2 or 1/5?", "1/2."), ("What is a numerator?", "The top number of a fraction.")]),

        U("equivalent-and-ordering-fractions", "N", "Identify equivalent fractions using diagrams; compare and order fractions using > and <.",
          "Equivalent Fractions and Ordering Fractions", "Equivalent and Ordering Fractions",
          "Free Primary 3 maths worksheets on equivalent fractions with pictures and comparing and ordering fractions with &gt; and &lt;. 100 questions with answers.",
          "1/2 = 2/4 = 3/6", "Same top number: fewer parts is bigger.",
          [("Equivalent fractions", [rs(fr3, "set_equiv", 20)]), ("Equal fractions in pictures", [rs(usf, "set_equiv", 20)]), ("Compare fractions", [rs(fr3, "set_compare", 20)]),
           ("Which is bigger?", [rs(usf, "set_compare", 20)]), ("Fractions of tenths", [rs(tf, "set_shapes", 10), rs(tf, "set_counting", 10)])],
          ul(["Equivalent fractions show the same amount: 1/2 of a bar is the same as 2/4 of the same bar.", "When the bottom numbers are the same, the bigger top number is the bigger fraction: 3/5 &gt; 2/5.",
              "When the top numbers are the same, the smaller bottom number is the bigger fraction: 1/3 &gt; 1/6."]),
          [ex("Compare 1/4 and 1/6", ["Fourths are bigger than sixths"], "1/4 &gt; 1/6")],
          [["Thinking 1/8 &gt; 1/4 because 8 &gt; 4", "More pieces means each piece is smaller."], ["Using different-sized wholes", "Compare fractions of the same whole."], ["Thinking 2/4 is more than 1/2", "They are equal."]],
          [("Is 2/4 the same as 1/2?", "Yes."), ("What are equivalent fractions?", "Fractions that have the same value."), ("Which is bigger, 3/4 or 1/4?", "3/4.")]),

        U("addition", "O", "Add 3-digit numbers with and without exchanging (carrying); add numbers mentally.",
          "Addition of 3-Digit Numbers", "Addition",
          "Free Primary 3 maths worksheets on adding 3-digit numbers with and without exchanging, column addition and mental addition. 100 questions with answers.",
          "Add units, then tens, then hundreds", "10 units = 1 ten: carry it.",
          [("Add without exchanging", [rs(usas, "set_add1", 20, lim)]), ("Add with exchanging", [rs(usas, "set_add2", 20, lim)]), ("Column addition", [rs(cas, "set_add", 20, lim)]),
           ("Add hundreds", [rs(mas, "set_hundreds", 20, lim)]), ("Add tens and units mentally", [rs(mas, "set_tens", 20, lim)])],
          ul(["Write the numbers in columns: hundreds under hundreds, tens under tens, units under units.", "Start with the units. If the units make 10 or more, carry 1 ten to the tens column.",
              "Do the same for the tens: 10 tens make 1 hundred."]),
          [ex("348 + 275", ["8 + 5 = 13, write 3 carry 1", "4 + 7 + 1 = 12, write 2 carry 1", "3 + 2 + 1 = 6"], "623")],
          [["Forgetting to carry", "Write the carried 1 above the next column."], ["Starting from the left", "Always start with the units."], ["Not lining up the numbers", "Units under units."]],
          [("What does exchanging mean?", "Changing 10 units for 1 ten, or 10 tens for 1 hundred."), ("Does the order of adding matter?", "No. 35 + 12 = 12 + 35."), ("How do I check an addition?", "Subtract one number from the answer.")]),

        U("subtraction", "O", "Subtract 3-digit numbers with and without exchanging (borrowing); check subtraction by addition.",
          "Subtraction of 3-Digit Numbers", "Subtraction",
          "Free Primary 3 maths worksheets on subtracting 3-digit numbers with and without exchanging, column subtraction and checking by addition. 100 questions with answers.",
          "Take away units, then tens, then hundreds", "Not enough? Exchange 1 ten for 10 units.",
          [("Subtract without exchanging", [rs(usas, "set_sub1", 20, lim)]), ("Subtract with exchanging", [rs(usas, "set_sub2", 20, lim)]), ("Column subtraction", [rs(cas, "set_sub1", 20, lim)]),
           ("Subtract mentally", [rs(mas, "set_ones", 20, lim)]), ("Check the answer", [rs(cas, "set_check", 20, lim)])],
          ul(["Write the bigger number on top and line up the columns.", "Start with the units. If the top digit is smaller, exchange 1 ten for 10 units.",
              "Check by adding: the answer + the number taken away = the first number."]),
          [ex("532 − 178", ["Exchange: 12 − 8 = 4", "12 − 7 = 5 (after exchanging a hundred)", "4 − 1 = 3"], "354")],
          [["Taking the smaller digit from the bigger digit", "In 52 − 18 you cannot do 8 − 2; exchange instead."], ["Forgetting the exchanged ten", "Cross out and write one less."], ["Putting the smaller number on top", "The bigger number goes on top."]],
          [("What is the difference between two numbers?", "The answer when you subtract the smaller from the bigger."), ("How do I check?", "Add your answer to the number you took away."), ("Can I subtract in any order?", "No. 9 − 4 is not the same as 4 − 9.")]),

        U("addition-and-subtraction-word-problems", "O", "Solve word problems on addition and subtraction of numbers up to 999.",
          "Addition and Subtraction Word Problems", "Word Problems",
          "Free Primary 3 maths worksheets on addition and subtraction word problems with numbers up to 999: altogether, how many more, how many left and missing numbers. 100 questions with answers.",
          "Altogether: add. Left or difference: subtract.", "Read, think, then work it out.",
          [("Word problems", [rs(cas, "set_story", 14, lim), rs(usw, "set_result", 6, lim)]), ("Story problems", [rs(usas, "set_story", 20, lim)]), ("Mental word problems", [rs(mas, "set_words", 20, lim)]),
           ("Missing numbers", [rs(mas, "set_missing", 20, lim)]), ("Money problems", [co(money(L.mo_add), 10), co(money(L.mo_change), 10)])],
          ul(["Read the problem carefully and find the key words.", "Altogether, in all, total and sum mean add. Left, more than, fewer and difference mean subtract.",
              "Write a number sentence, work it out, and check that the answer makes sense."]),
          [ex("A school has 345 boys and 287 girls. How many pupils?", ["345 + 287"], "632 pupils")],
          [["Adding when the question asks how many more", "How many more means find the difference."], ["Forgetting the units in the answer", "Write pupils, naira or metres."], ["Using the wrong numbers", "Underline the numbers you need."]],
          [("What does difference mean?", "How much bigger one number is than another."), ("Which key words mean add?", "Altogether, total, in all, sum."), ("Should I check my answer?", "Yes, see if it makes sense.")]),

        U("adding-and-subtracting-fractions", "O", "Add and subtract fractions with the same denominator; solve simple word problems.",
          "Adding and Subtracting Fractions with the Same Denominator", "Adding and Subtracting Fractions",
          "Free Primary 3 maths worksheets on adding and subtracting fractions with the same denominator, with pictures and simple word problems. 100 questions with answers.",
          "Same denominator: add or subtract the tops", "The bottom number stays the same.",
          [("Add and subtract fractions", [co(L.fr_same, 20)]), ("Tenths", [rs(tf, "set_add_sub", 20)]), ("What is left?", [co(L.fr_left, 20)]),
           ("Fraction stories", [co(L.fr_same_word, 20)]), ("Fraction word problems", [rs(tf, "set_words", 20)])],
          ul(["When the bottom numbers (denominators) are the same, add or subtract the top numbers (numerators).", "The bottom number does not change: 2/5 + 1/5 = 3/5.",
              "A whole is 4/4, 5/5 or 6/6. To find what is left, subtract from the whole."]),
          [ex("3/8 + 2/8", ["3 + 2 = 5"], "5/8"), ex("5/6 − 4/6", ["5 − 4 = 1"], "1/6")],
          [["Adding the bottom numbers", "2/5 + 1/5 = 3/5, not 3/10."], ["Changing the bottom number", "The size of the parts stays the same."], ["Forgetting that the whole is 1", "6/6 = 1."]],
          [("Why does the denominator stay the same?", "The parts are the same size; we only count more or fewer of them."), ("What is 3/3?", "One whole."), ("Can I add 1/2 and 1/3 this way?", "No. That needs equal denominators first.")]),

        U("multiplication", "O", "Recall multiplication facts up to 9 × 9; multiply 2-digit numbers by 1-digit numbers; multiply three 1-digit numbers; use the property of zero and one.",
          "Multiplication Facts and Multiplying 2-Digit Numbers", "Multiplication",
          "Free Primary 3 maths worksheets on multiplication: times tables up to 9 × 9, multiplying 2-digit numbers by 1-digit numbers, multiplying by 0 and 1, and multiplying three numbers. 100 questions with answers.",
          "Multiplication is repeated addition", "Any number × 0 = 0, any number × 1 = itself.",
          [("Times tables", [rs(tt, "set_three", 7), rs(tt, "set_four", 7), rs(tt, "set_eight", 6)]), ("2, 5 and 10 times tables", [rs(tt2, "set_two", 7), rs(tt2, "set_five", 7), rs(tt2, "set_ten", 6)]),
           ("2-digit × 1-digit", [rs(md, "set_grid", 10), rs(md, "set_short", 10)]), ("Multiply by tens", [rs(us10, "set_facts", 20)]), ("Zero, one and order", [rs(usprop, "set_one_zero", 10), rs(usprop, "set_commutative", 10)])],
          ul(["3 × 4 means 3 groups of 4: 4 + 4 + 4 = 12.", "To multiply 23 × 4, multiply the units and the tens: 3 × 4 = 12 and 20 × 4 = 80, so 23 × 4 = 92.",
              "Any number × 0 = 0. Any number × 1 = the same number. 3 × 5 = 5 × 3."]),
          [ex("36 × 3", ["6 × 3 = 18, write 8 carry 1", "3 × 3 + 1 = 10"], "108"), ex("4 × 2 × 5", ["4 × 2 = 8, 8 × 5"], "40")],
          [["Adding instead of multiplying", "3 × 4 = 12, not 7."], ["Forgetting to carry", "Add the carried number after multiplying the tens."], ["Thinking 7 × 0 = 7", "Zero groups of anything is 0."]],
          [("What is a product?", "The answer to a multiplication."), ("Does the order matter?", "No. 6 × 3 = 3 × 6."), ("How can I learn tables?", "Count in steps and practise every day.")]),

        U("division", "O", "Divide whole numbers up to 48 by 2, 3, 4, 5 and 6 without remainder; relate division to multiplication; solve sharing problems.",
          "Division: Sharing and Grouping", "Division",
          "Free Primary 3 maths worksheets on division: sharing equally, grouping, division facts, dividing 2-digit numbers and division word problems. 100 questions with answers.",
          "Division is sharing equally", "12 ÷ 3 = 4 because 3 × 4 = 12.",
          [("Division facts", [rs(tt, "set_division", 20)]), ("Divide 2-digit numbers", [rs(md, "set_divide", 20)]), ("Share equally", [co(A4.div_share, 20, le(99))]),
           ("Division and multiplication", [rs(tt2, "set_words", 20)]), ("Division stories", [rs(md, "set_story", 20)])],
          ul(["Division means sharing equally or making equal groups.", "Use the times tables: 24 ÷ 4 = 6 because 4 × 6 = 24.",
              "A division can be checked with a multiplication."]),
          [ex("35 oranges shared by 5 children", ["35 ÷ 5"], "7 each")],
          [["Mixing up the numbers", "24 ÷ 4 is not the same as 4 ÷ 24."], ["Unequal sharing", "Every group must have the same number."], ["Forgetting to check", "Multiply back to check."]],
          [("What is the sign for division?", "÷."), ("What is 0 ÷ 5?", "0."), ("How does multiplication help?", "If you know 6 × 7 = 42, you know 42 ÷ 6 = 7.")]),

        U("factors", "N", "Find factors of whole numbers up to 48; find missing factors; tell factors from other numbers.",
          "Factors of Whole Numbers up to 48", "Factors",
          "Free Primary 3 maths worksheets on factors: factors of numbers up to 48, missing factors, all the factors of a number, and numbers that are not factors. 100 questions with answers.",
          "A factor divides exactly", "Factors come in pairs: 3 × 8 = 24.",
          [("Is it a factor?", [co(L.fac_is, 20)]), ("Missing factors", [co(L.fac_missing, 20)]), ("All the factors", [co(L.fac_list, 20)]),
           ("How many factors?", [co(L.fac_count, 20)]), ("Not a factor", [co(L.fac_not, 14), co(L.fac_is, 6)])],
          ul(["A factor of a number divides it exactly, with nothing left over.", "Factors come in pairs: 24 = 1 × 24 = 2 × 12 = 3 × 8 = 4 × 6.",
              "1 is a factor of every number, and every number is a factor of itself."]),
          [ex("Factors of 18", ["1 × 18, 2 × 9, 3 × 6"], "1, 2, 3, 6, 9, 18")],
          [["Forgetting 1 and the number itself", "They are always factors."], ["Listing multiples instead of factors", "Factors are smaller than or equal to the number."], ["Missing a pair", "Try 1, 2, 3, 4, … in order."]],
          [("Is 5 a factor of 30?", "Yes, 30 ÷ 5 = 6."), ("Is 7 a factor of 30?", "No, 30 ÷ 7 leaves a remainder."), ("How many factors does 12 have?", "Six: 1, 2, 3, 4, 6, 12.")]),

        U("money", "M", "Recognise naira notes from ₦5 to ₦1,000; add and subtract amounts of money; give change; multiply simple amounts of money.",
          "Money: Naira Notes, Adding, Change and Shopping", "Money",
          "Free Primary 3 maths worksheets on Nigerian money: naira notes from ₦5 to ₦1,000, counting money, adding prices, giving change and buying more than one item. 100 questions with answers.",
          "Count the biggest note first", "Change = money paid − price.",
          [("Naira notes", [co(money(L.mo_name), 8), co(money(L.mo_which), 12)]), ("Count the money", [co(money(L.mo_count), 20)]), ("Add prices", [co(money(L.mo_add), 20)]),
           ("Change", [co(money(L.mo_change), 20)]), ("Buy more than one", [co(money(L.mo_mult), 20)])],
          ul(["Nigerian money is the naira (₦). Notes include ₦5, ₦10, ₦20, ₦50, ₦100, ₦200, ₦500 and ₦1,000.", "To count money, start with the note of the highest value and count on.",
              "Change is the money you get back: money paid − price."]),
          [ex("₦200 + ₦100 + ₦50 + ₦20", ["Count on from ₦200"], "₦370"), ex("Pay ₦500 for a ₦350 book", ["500 − 350"], "₦150 change")],
          [["Counting notes instead of their values", "Three notes can be worth more than five notes."], ["Adding when finding change", "Change = paid − price."], ["Forgetting the ₦ sign", "Always write ₦."]],
          [("What is the highest naira note?", "₦1,000."), ("How many ₦50 notes make ₦100?", "Two."), ("Why should we check our change?", "To make sure we get the right money back.")]),

        U("length", "M", "Measure and compare lengths in centimetres and metres; estimate lengths; add and subtract lengths.",
          "Length: Centimetres and Metres", "Length",
          "Free Primary 3 maths worksheets on length: measuring with a ruler, centimetres and metres, estimating, comparing and adding lengths. 100 questions with answers.",
          "100 cm = 1 m", "Start measuring from 0.",
          [("Measure with a ruler", [rs(me, "set_length", 20)]), ("Estimate lengths", [co(A4.len_est, 20)]), ("Compare measures", [rs(me, "set_compare", 20)]),
           ("Centimetres and metres", [rs(usme, "set_two_units", 20)]), ("Longer or shorter", [rs(usme, "set_longer", 20)])],
          ul(["We measure short things in centimetres (cm) and long things in metres (m).", "100 cm = 1 m.", "Put the 0 of the ruler at one end of the object."]),
          [ex("A pencil from 0 to 14 on the ruler", ["Read the end"], "14 cm")],
          [["Starting from 1 on the ruler", "Start from 0."], ["Using cm for long distances", "Use metres for a classroom."], ["Mixing cm and m", "Change them to the same unit."]],
          [("How long is a metre?", "About one big step."), ("Which unit for a pencil?", "Centimetres."), ("How many cm in 2 m?", "200 cm.")]),

        U("perimeter-and-area", "M", "Find the perimeter of shapes by adding the lengths of the sides; find the area of shapes by counting squares.",
          "Perimeter and Area", "Perimeter and Area",
          "Free Primary 3 maths worksheets on perimeter (the distance round a shape) and area (counting squares), with grids, rectangles and simple problems. 100 questions with answers.",
          "Perimeter: add all the sides", "Area: count the squares inside.",
          [("Perimeter on a grid", [rs(per, "set_grid", 20)]), ("Add the sides", [rs(per, "set_add", 20)]), ("Perimeter of rectangles", [rs(per, "set_rect", 20)]),
           ("Area by counting squares", [rs(ar4, "set_area", 20)]), ("Area of shapes", [rs(usps, "set_area", 20)])],
          ul(["Perimeter is the distance all the way round a shape. Add the lengths of all the sides.", "Area is the space inside a shape. Count the squares.",
              "A rectangle has two pairs of equal sides."]),
          [ex("Rectangle 5 cm by 3 cm", ["5 + 3 + 5 + 3"], "Perimeter 16 cm")],
          [["Counting squares for perimeter", "Perimeter is the edges, not the squares inside."], ["Missing a side", "Count every side."], ["Forgetting the units", "Perimeter is in cm or m."]],
          [("What is perimeter?", "The distance round a shape."), ("What is area?", "The space a shape covers."), ("Where do we use perimeter?", "To find how much fence goes round a garden.")]),

        U("capacity", "M", "Measure capacity in litres; compare the capacity of containers; read scales on measuring jugs.",
          "Capacity: Litres", "Capacity",
          "Free Primary 3 maths worksheets on capacity: litres and millilitres, reading measuring jugs, comparing containers and capacity problems. 100 questions with answers.",
          "We measure liquids in litres", "1 litre = 1,000 millilitres.",
          [("Read the jug", [rs(me, "set_capacity", 20)]), ("Containers", [rs(usmv, "set_container", 20)]), ("Litres or millilitres?", [rs(usmv, "set_units", 10), co(A4.cap_est, 10)]),
           ("Capacity sums", [co(A4.cap_addsub, 20, lim)]), ("Capacity problems", [rs(usmv, "set_story", 20)])],
          ul(["Capacity is how much a container can hold.", "We measure it in litres (l). Small amounts are in millilitres (ml): 1 litre = 1,000 ml.",
              "Read the scale at the top of the water level."]),
          [ex("A bucket holds 10 litres. How much do 3 buckets hold?", ["10 × 3"], "30 litres")],
          [["Reading the wrong mark", "Find what each mark stands for."], ["Mixing litres and millilitres", "Use the same unit."], ["Thinking a tall container always holds more", "A wide container can hold more."]],
          [("What is a litre?", "A unit for measuring liquids such as water and oil."), ("Which holds more, a cup or a bucket?", "A bucket."), ("Where do we see litres?", "On bottles of water, oil and drinks.")]),

        U("weight", "M", "Measure weight in grams and kilograms; read weighing scales; compare weights; solve simple weight problems.",
          "Weight: Grams and Kilograms", "Weight",
          "Free Primary 3 maths worksheets on weight: grams and kilograms, reading weighing scales, balances, comparing and estimating weights. 100 questions with answers.",
          "1 kilogram = 1,000 grams", "Heavy things in kg, light things in g.",
          [("Read the scale", [rs(me, "set_mass", 20)]), ("Weighing scales", [rs(usmv, "set_scale", 20)]), ("Balances", [rs(usmv, "set_balance", 20)]),
           ("Estimate weights", [co(A4.wt_est, 20)]), ("Weight problems", [rs(me, "set_story", 20)])],
          ul(["We measure weight in grams (g) and kilograms (kg). 1 kg = 1,000 g.", "Light things like a pencil are measured in grams. Heavy things like a bag of rice are in kilograms.",
              "On a balance, the heavier side goes down."]),
          [ex("A bag of rice weighs 5 kg and a bag of beans weighs 3 kg", ["5 + 3"], "8 kg altogether")],
          [["Reading the wrong scale", "Find the value of each mark."], ["Thinking big means heavy", "A big pillow can be light."], ["Mixing g and kg", "Change to the same unit."]],
          [("What weighs about 1 kg?", "A bag of sugar."), ("Which side of a balance goes down?", "The heavier side."), ("How many grams in half a kilogram?", "500 g.")]),

        U("time", "M", "Tell the time to the hour, half hour, quarter hour and five minutes; know the units of time.",
          "Telling the Time", "Time",
          "Free Primary 3 maths worksheets on time: o'clock, half past, quarter past and quarter to, time to five minutes and to the minute, and time problems. 100 questions with answers.",
          "The short hand shows the hour", "The long hand shows the minutes.",
          [("Quarter past and quarter to", [rs(ti, "set_quarters", 20)]), ("Time to five minutes", [rs(ti, "set_fives", 20)]), ("Time to the minute", [rs(ust, "set_one", 20)]),
           ("Facts about time", [rs(ti, "set_facts", 20)]), ("Time problems", [rs(ust, "set_elapsed", 20)])],
          ul(["The short hand points to the hour. The long hand points to the minutes.", "Each number on the clock stands for 5 minutes for the long hand.",
              "Half past = 30 minutes. Quarter past = 15 minutes. Quarter to = 15 minutes before the hour."]),
          [ex("Short hand just past 3, long hand at 9", ["9 × 5 = 45 minutes"], "3:45, quarter to four")],
          [["Mixing up the hands", "The long hand shows minutes."], ["Reading quarter to as quarter past", "Quarter to is before the hour."], ["Counting each number as 1 minute", "Each number is 5 minutes."]],
          [("How many minutes in an hour?", "60."), ("What is half past two?", "2:30."), ("How many hours in a day?", "24.")]),

        U("calendar", "M", "Name the days of the week and the months of the year; read a calendar; find dates and the number of days.",
          "The Calendar: Days, Weeks and Months", "Calendar",
          "Free Primary 3 maths worksheets on the calendar: days of the week, months of the year, days in each month, reading dates and counting days and weeks. 100 questions with answers.",
          "7 days = 1 week, 12 months = 1 year", "30 days have September, April, June and November.",
          [("Days and months", [rs(ti1, "set_calendar", 20)]), ("Days in a month", [co(A4.cal_days, 12), co(A4.cal_after, 8)]), ("What day will it be?", [co(A4.cal_after, 20)]),
           ("How many days?", [co(A4.cal_span, 20)]), ("Order of events", [rs(ti1, "set_order", 20)])],
          ul(["There are 7 days in a week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday.", "There are 12 months in a year, from January to December.",
              "April, June, September and November have 30 days. February has 28 days (29 in a leap year). The others have 31."]),
          [ex("Today is Tuesday. What day is it in 3 days?", ["Wednesday, Thursday, Friday"], "Friday")],
          [["Counting today as one of the days", "Start counting from tomorrow."], ["Thinking every month has 30 days", "Some have 31 and February has 28 or 29."], ["Mixing up the order of months", "Say them in order: January, February, March, …"]],
          [("Which month is Independence Day in Nigeria?", "October (1 October)."), ("How many days in a year?", "365, or 366 in a leap year."), ("What is a fortnight?", "Two weeks, 14 days.")]),

        U("shapes-and-symmetry", "G", "Identify plane shapes and 3D shapes and their properties; find lines of symmetry.",
          "Shapes and Symmetry", "Shapes and Symmetry",
          "Free Primary 3 maths worksheets on shapes: naming 2D shapes, sides and corners, 3D shapes, faces, edges and vertices, and lines of symmetry. 100 questions with answers.",
          "Count sides and corners", "A line of symmetry folds a shape into two matching halves.",
          [("2D shapes", [rs(sh3, "set_2d", 20)]), ("Lines of symmetry", [rs(sh2, "set_symmetry", 20)]), ("3D shapes", [rs(sh3, "set_name3d", 20)]),
           ("Faces, edges and vertices", [rs(sh3, "set_fev", 20)]), ("Shapes around us", [rs(sh2, "set_problems", 20)])],
          ul(["2D shapes are flat: triangle (3 sides), square and rectangle (4 sides), pentagon (5 sides), hexagon (6 sides), circle.", "3D shapes are solid: cube, cuboid, cylinder, cone, sphere and pyramid.",
              "A line of symmetry cuts a shape into two halves that match when folded."]),
          [ex("A square", ["4 equal sides, 4 corners"], "4 lines of symmetry")],
          [["Calling a cube a square", "A cube is solid; a square is flat."], ["Taking a diagonal of a rectangle as a line of symmetry", "Fold it to check."], ["Counting corners twice", "Mark each one."]],
          [("How many sides does a hexagon have?", "Six."), ("Does a circle have corners?", "No."), ("What shape is a football?", "A sphere.")]),

        U("pictograms", "S", "Collect data and make pictograms; read pictograms, tally charts and bar charts; answer questions from data.",
          "Pictograms, Tally Charts and Bar Charts", "Pictograms",
          "Free Primary 3 maths worksheets on data: reading pictograms with a key, tally charts, block graphs and bar charts, and comparing data. 100 questions with answers.",
          "Read the key first", "One picture may stand for more than one thing.",
          [("Pictograms", [rs(st, "set_pictogram", 20)]), ("Pictograms with a key", [rs(st2, "set_pic_key", 20)]), ("Tally charts", [rs(st, "set_tally_table", 20)]),
           ("Bar charts", [rs(st, "set_bar", 20)]), ("Compare the data", [rs(st, "set_compare", 20)])],
          ul(["A pictogram uses pictures to show data. The key tells how many each picture stands for.", "A tally chart uses marks: |||| with a line across is 5.",
              "To compare, find the difference between two amounts."]),
          [ex("Key: 1 picture = 2 pupils. Mangoes has 4 pictures", ["4 × 2"], "8 pupils")],
          [["Ignoring the key", "Multiply by what one picture stands for."], ["Miscounting tally marks", "Count the groups of 5 first."], ["Adding when asked how many more", "Subtract to compare."]],
          [("What is a pictogram?", "A chart that uses pictures."), ("What does a tally mark show?", "One thing counted."), ("Why use a key?", "So one picture can stand for several things.")]),
    ]


if __name__ == "__main__":
    main("primary-3", "Primary 3", units, 150300, max_num=None)
