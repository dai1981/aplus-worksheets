# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 5 (NERDC 9-Year Basic Education Curriculum; first, second and third term order of the scheme of work).
  python3 tools/ng_p5.py [number …]      seed = 150500 + number, reused modules 1519NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex, le
import ng_p4a as A4
import ng_p5a as A


def units():
    uk6p = mod("gen_uk_maths_y6_place_value", 151901)
    uk5p = mod("gen_uk_maths_y5_place_value", 151902)
    sgn = mod("gen_sg_maths_p5_numbers", 151903)
    rn5 = mod("gen_uk_maths_y5_roman_numerals", 151904)
    rn4 = mod("gen_uk_maths_y4_roman_numerals", 151905)
    uka = mod("gen_uk_maths_y5_column_add_sub", 151906)
    ukm = mod("gen_uk_maths_y5_multiplication", 151907)
    ukd = mod("gen_uk_maths_y5_short_division", 151908)
    usd = mod("gen_us_math_g5_division", 151909)
    ukf5 = mod("gen_uk_maths_y5_factors_primes", 151910)
    ukf6 = mod("gen_uk_maths_y6_factors_primes", 151911)
    uke = mod("gen_uk_maths_y5_equivalent_fractions", 151912)
    uks6 = mod("gen_uk_maths_y6_simplify_compare_fractions", 151913)
    ukr = mod("gen_uk_maths_y6_ratio", 151914)
    uaf = mod("gen_uk_maths_y5_add_sub_fractions", 151915)
    usaf = mod("gen_us_math_g5_add_sub_fractions", 151916)
    umf = mod("gen_uk_maths_y5_multiply_fractions", 151917)
    udf = mod("gen_uk_maths_y6_mult_div_fractions", 151918)
    usdf = mod("gen_us_math_g5_divide_fractions", 151919)
    ukro = mod("gen_uk_maths_y5_rounding", 151920)
    sgx = mod("gen_sg_maths_p5_multiply_divide_by_10", 151921)
    usdp = mod("gen_us_math_g5_decimal_place_value", 151922)
    usad = mod("gen_us_math_g5_add_sub_decimals", 151923)
    usmd = mod("gen_us_math_g5_mul_div_decimals", 151924)
    sgpc = mod("gen_sg_maths_p5_percentage", 151925)
    ukdp = mod("gen_uk_maths_y5_decimals_percentages", 151926)
    uk6a = mod("gen_uk_maths_y6_algebra", 151927)
    ukap = mod("gen_uk_maths_y5_area_perimeter", 151928)
    usv = mod("gen_us_math_g5_volume", 151929)
    sgv = mod("gen_sg_maths_p5_volume", 151930)
    ukc = mod("gen_uk_maths_y5_converting_units", 151931)
    ukan = mod("gen_uk_maths_y5_angles", 151932)
    sgan = mod("gen_sg_maths_p5_angles", 151933)
    uscf = mod("gen_us_math_g5_classify_figures", 151934)
    sgtr = mod("gen_sg_maths_p5_triangles", 151935)
    sgq = mod("gen_sg_maths_p5_quadrilaterals", 151936)
    ukcn = mod("gen_uk_maths_y6_circles_nets", 151937)
    uklg = mod("gen_uk_maths_y5_line_graphs_tables", 151938)
    ukpl = mod("gen_uk_maths_y6_pie_line", 151939)
    ukst = mod("gen_uk_maths_y3_statistics", 151940)
    ukmn = mod("gen_uk_maths_y6_mean", 151941)
    uks3 = mod("gen_uk_maths_y3_shapes", 151942)

    return [
        U("whole-numbers-up-to-millions", "N", "Count, read and write whole numbers up to millions in figures and in words; give the place value of digits; compare and order large numbers.",
          "Whole Numbers up to Millions: Place Value, Reading and Writing", "Whole Numbers up to Millions",
          "Free Primary 5 maths worksheets on whole numbers up to millions: place value, the value of a digit, numbers in figures and words, comparing and ordering. 100 questions with answers.",
          "Value = digit × place", "Split big numbers into groups of three digits.",
          [("Place value up to millions", [rs(uk6p, "set_value", 20)]), ("Value of a digit", [rs(uk5p, "set_value", 20)]),
           ("Read and write large numbers", [rs(uk5p, "set_count", 10), rs(sgn, "set_write", 10)]), ("Compare and order", [rs(uk6p, "set_compare", 10), rs(uk5p, "set_compare", 10)]),
           ("Large numbers in real life", [rs(sgn, "set_life", 10), rs(uk6p, "set_words", 10)])],
          ul(["Group the digits in threes from the right: millions, thousands, units. 4,382,105 = 4 million, 382 thousand, 105.",
              "The value of a digit = the digit × its place. In 4,382,105 the 8 is worth 80,000.",
              "To compare, first count the digits. If they have the same number of digits, compare from the left."]),
          [ex("Value of 3 in 6,305,218", ["3 is in the hundred thousands place"], "300,000"), ex("Write 2,040,600 in words", ["2 million, 40 thousand, 600"], "two million, forty thousand, six hundred")],
          [["Reading the comma as a decimal point", "The commas only group the digits; 2,040,600 is a whole number."], ["Forgetting zeros", "Two million and forty thousand is 2,040,000, not 2,40,000."], ["Comparing from the right", "Always compare from the biggest place."]],
          [("How many zeros are in one million?", "Six: 1,000,000."), ("What comes after 999,999?", "One million, 1,000,000."), ("Where are large numbers used?", "Populations of states and cities, money in a bank and distances in space.")]),

        U("roman-numerals", "N", "Read and write Roman numerals up to M (1,000) and beyond; convert between Roman numerals and Hindu-Arabic numerals; add and subtract numbers written in Roman numerals.",
          "Roman Numerals: Reading, Writing and Converting", "Roman Numerals",
          "Free Primary 5 maths worksheets on Roman numerals: the symbols I, V, X, L, C, D and M, reading and writing numbers up to 3,000, converting and simple sums. 100 questions with answers.",
          "Big to small: add. Small before big: subtract.", "IV 4, IX 9, XL 40, XC 90, CD 400, CM 900",
          [("Roman symbols", [rs(rn5, "set_symbols", 15), rs(rn4, "set_symbols", 5)]), ("Read Roman numerals", [rs(rn5, "set_read", 20)]), ("Write Roman numerals", [rs(rn5, "set_write", 5), co(A4.rm_write, 15)]),
           ("Add and subtract", [rs(rn4, "set_calc", 20)]), ("Roman numerals around us", [rs(rn5, "set_life", 20)])],
          ul(["I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1,000.", "Write the thousands, then the hundreds, tens and units: 1,846 = M + DCCC + XL + VI = MDCCCXLVI.",
              "Only I, X and C go in front of a bigger symbol to subtract, and never more than one."]),
          [ex("Write 949", ["900 = CM, 40 = XL, 9 = IX"], "CMXLIX"), ex("MCCXV", ["1,000 + 200 + 10 + 5"], "1,215")],
          [["Writing IC for 99", "99 = 90 + 9 = XCIX."], ["Repeating a symbol four times", "4 is IV, not IIII; 40 is XL, not XXXX."], ["Adding a small symbol in front", "In IX the I is taken away: 10 − 1 = 9."]],
          [("Is there a Roman numeral for zero?", "No. The Romans had no symbol for zero."), ("Where do we see Roman numerals?", "On clocks, in book chapters, and in the names of kings such as Elizabeth II."), ("What is the biggest symbol?", "M, which is 1,000.")]),

        U("addition-and-subtraction", "O", "Add and subtract whole numbers with up to seven digits, with and without exchanging; check answers by the inverse operation; solve word problems.",
          "Addition and Subtraction of Large Numbers", "Addition and Subtraction",
          "Free Primary 5 maths worksheets on adding and subtracting large whole numbers in columns, mental strategies, checking answers and word problems. 100 questions with answers.",
          "Line up the units", "Check: answer + number taken away = first number.",
          [("Column addition", [rs(uka, "set_add", 20)]), ("Column subtraction", [rs(uka, "set_sub", 20)]), ("Mental strategies", [rs(uka, "set_mental", 20)]),
           ("Check the answer", [rs(uka, "set_check", 20)]), ("Word problems", [rs(uka, "set_story", 20)])],
          ul(["Write the numbers in columns so that units are under units, tens under tens and so on.", "Add or subtract from the right. Exchange 10 of one place for 1 of the next place when you need to.",
              "Check a subtraction by adding: 7,415 − 2,638 = 4,777 because 4,777 + 2,638 = 7,415."]),
          [ex("45,286 + 37,915", ["6 + 5 = 11, write 1 carry 1", "… work left"], "83,201"), ex("60,004 − 2,385", ["Exchange across the zeros"], "57,619")],
          [["Not lining up the units", "Write the numbers from the right."], ["Taking the smaller digit from the bigger one", "In 52 − 38 you must exchange: 12 − 8, not 8 − 2."], ["Forgetting a carried 1", "Write the carried 1 small above the next column."]],
          [("What is the inverse of addition?", "Subtraction. Use it to check your answer."), ("What does exchanging mean?", "Changing 1 ten for 10 units, 1 hundred for 10 tens, and so on."), ("How do I check a sum quickly?", "Round the numbers and estimate.")]),

        U("multiplication-and-division", "O", "Multiply whole numbers by 2- and 3-digit numbers; divide by 1- and 2-digit numbers with and without remainders; solve word problems.",
          "Multiplication and Division of Whole Numbers", "Multiplication and Division",
          "Free Primary 5 maths worksheets on long multiplication, short and long division, remainders and multiplication and division word problems. 100 questions with answers.",
          "Division is the inverse of multiplication", "Check: quotient × divisor + remainder = number.",
          [("Short multiplication", [rs(ukm, "set_short", 20)]), ("Long multiplication", [rs(ukm, "set_2x2", 10), rs(ukm, "set_big", 10)]),
           ("Short division", [rs(ukd, "set_exact", 10), rs(ukd, "set_rem3", 10)]), ("Dividing by 2-digit numbers", [rs(usd, "set_two_digit", 20)]),
           ("Word problems", [rs(ukm, "set_story", 10), rs(ukd, "set_story", 10)])],
          ul(["For 346 × 27, find 346 × 7 and 346 × 20, then add the two answers.", "In division, share from the biggest place. Write any remainder at the end.",
              "Check: 254 ÷ 7 = 36 remainder 2, because 36 × 7 + 2 = 254."]),
          [ex("346 × 27", ["346 × 7 = 2,422", "346 × 20 = 6,920"], "9,342"), ex("918 ÷ 6", ["9 ÷ 6 = 1 r 3, 31 ÷ 6 = 5 r 1, 18 ÷ 6 = 3"], "153")],
          [["Forgetting the 0 when multiplying by tens", "346 × 20: write a 0 first, then multiply by 2."], ["A remainder bigger than the divisor", "If the remainder is not smaller than the divisor, the quotient is too small."], ["Dropping a zero in the quotient", "In 612 ÷ 6 = 102, write the 0 in the tens place."]],
          [("What is a quotient?", "The answer to a division."), ("What is a product?", "The answer to a multiplication."), ("How do I check a division?", "Multiply the quotient by the divisor and add the remainder.")]),

        U("prime-numbers-factors-and-multiples", "N", "Identify prime numbers up to 100; find factors and multiples; find the LCM and HCF of numbers; solve problems on LCM and HCF.",
          "Prime Numbers, Factors, Multiples, LCM and HCF", "Prime Numbers, LCM and HCF",
          "Free Primary 5 maths worksheets on prime numbers, factors and multiples, the lowest common multiple (LCM) and the highest common factor (HCF), with word problems. 100 questions with answers.",
          "A prime has exactly two factors", "LCM: smallest shared multiple. HCF: biggest shared factor.",
          [("Factors", [rs(ukf5, "set_factors", 20)]), ("Prime numbers", [rs(ukf5, "set_primes", 20)]), ("Multiples and LCM", [rs(ukf5, "set_multiples", 10), rs(ukf6, "set_lcm", 10)]),
           ("Common factors and HCF", [rs(ukf6, "set_hcf", 20)]), ("LCM and HCF problems", [co(A4.lcm_word, 10), co(A4.hcf_word, 10)])],
          ul(["A factor divides a number exactly. A multiple is in the number's times table.", "A prime number has exactly two factors: 1 and itself (2, 3, 5, 7, 11, …). 1 is not prime.",
              "LCM is the smallest number that is a multiple of each number. HCF is the biggest number that is a factor of each number."]),
          [ex("LCM of 6 and 8", ["Multiples of 8: 8, 16, 24", "24 is a multiple of 6"], "24"), ex("HCF of 18 and 24", ["Factors of 18: 1, 2, 3, 6, 9, 18", "6 also divides 24"], "6")],
          [["Calling 1 a prime number", "1 has only one factor, so it is not prime."], ["Mixing up LCM and HCF", "LCM is big (a multiple); HCF is small (a factor)."], ["Thinking all odd numbers are prime", "9, 15 and 21 are odd but not prime."]],
          [("Is 2 a prime number?", "Yes. It is the only even prime."), ("When do we use LCM?", "When things happen together again, such as two bells that ring at different times."), ("When do we use HCF?", "When we cut or share things into the largest equal groups.")]),

        U("fractions", "N", "Identify proper, improper fractions and mixed numbers; find equivalent fractions; reduce fractions to their lowest terms; compare and order fractions.",
          "Fractions: Equivalent Fractions, Lowest Terms and Ordering", "Fractions",
          "Free Primary 5 maths worksheets on fractions: equivalent fractions, lowest terms, improper fractions and mixed numbers, and comparing and ordering fractions. 100 questions with answers.",
          "Multiply or divide top and bottom by the same number", "Compare with a common denominator.",
          [("Equivalent fractions in pictures", [rs(uke, "set_diagrams", 20)]), ("Missing numbers", [rs(uke, "set_missing", 20)]), ("Lowest terms", [rs(uks6, "set_simplify", 20)]),
           ("Improper fractions and mixed numbers", [rs(uke, "set_mixed", 10), rs(uks6, "set_mixed", 10)]), ("Compare and order fractions", [rs(uke, "set_compare", 10), rs(uks6, "set_compare", 10)])],
          ul(["Equivalent fractions have the same value: 2/3 = 4/6 = 8/12.", "To reduce to lowest terms, divide the numerator and denominator by their HCF.",
              "To compare fractions, change them to the same denominator, then compare the numerators."]),
          [ex("Reduce 18/24", ["HCF is 6"], "3/4"), ex("Which is bigger, 3/5 or 2/3?", ["9/15 and 10/15"], "2/3")],
          [["Multiplying only the top", "Do the same to the numerator and the denominator."], ["Thinking a bigger denominator means a bigger fraction", "1/8 is smaller than 1/4."], ["Stopping before the lowest terms", "Keep dividing until only 1 divides both."]],
          [("What is an improper fraction?", "One whose numerator is bigger than or equal to its denominator, such as 7/4."), ("What is a mixed number?", "A whole number and a fraction, such as 1 3/4."), ("What is the lowest term of 10/15?", "2/3.")]),

        U("ratio", "N", "Express quantities as ratios; write ratios in their simplest form; share quantities in a given ratio; solve simple proportion problems.",
          "Ratio: Simplest Form, Sharing and Proportion", "Ratio",
          "Free Primary 5 maths worksheets on ratio: writing ratios, simplest form, sharing money and things in a ratio, and simple proportion. 100 questions with answers.",
          "Ratio compares parts", "Share: add the parts, then find one part.",
          [("Ratios in pictures", [rs(ukr, "set_pictures", 20)]), ("Simplest form", [co(A.ratio_simplify, 20)]), ("Ratio in a class", [co(A.ratio_class, 20)]),
           ("Sharing in a ratio", [co(A.ratio_share, 10), rs(ukr, "set_sharing", 10)]), ("Proportion", [co(A.proportion, 10), rs(ukr, "set_scaling", 10)])],
          ul(["A ratio compares two amounts. 3 boys to 5 girls is written 3 : 5. The order matters.", "Simplify a ratio by dividing both parts by the same number: 12 : 18 = 2 : 3.",
              "To share in a ratio, add the parts, find the value of one part, then multiply."]),
          [ex("Share ₦12,000 in the ratio 1 : 3", ["4 parts, one part = ₦3,000"], "₦3,000 and ₦9,000"), ex("Simplify 15 : 25", ["Divide by 5"], "3 : 5")],
          [["Writing the ratio the wrong way round", "Boys to girls means boys first."], ["Dividing by only one part", "In 2 : 3 there are 5 parts in all."], ["Not simplifying fully", "8 : 12 = 2 : 3, not 4 : 6."]],
          [("Is 2 : 3 the same as 3 : 2?", "No. The order of the parts matters."), ("Does a ratio have units?", "No. Both parts must be in the same unit, then the unit is dropped."), ("What is proportion?", "When two amounts grow at the same rate, such as cost and number of items.")]),

        U("adding-and-subtracting-fractions", "O", "Add and subtract fractions with like and unlike denominators, including mixed numbers; solve word problems on fractions.",
          "Adding and Subtracting Fractions and Mixed Numbers", "Adding and Subtracting Fractions",
          "Free Primary 5 maths worksheets on adding and subtracting fractions with the same and different denominators, mixed numbers and fraction word problems. 100 questions with answers.",
          "Same denominator first", "Add or subtract the numerators only.",
          [("Same denominator", [rs(uaf, "set_same", 20)]), ("Related denominators", [rs(uaf, "set_related", 20)]), ("Different denominators", [rs(usaf, "set_add", 20)]),
           ("Mixed numbers", [rs(uaf, "set_mixed", 20)]), ("Word problems", [rs(uaf, "set_words", 10), rs(usaf, "set_words", 10)])],
          ul(["With the same denominator, add or subtract the numerators and keep the denominator: 2/7 + 3/7 = 5/7.",
              "With different denominators, change to equivalent fractions using the LCM: 1/2 + 1/3 = 3/6 + 2/6 = 5/6.", "For mixed numbers, work with the wholes and the fractions, or change to improper fractions first."]),
          [ex("3/4 + 1/6", ["LCM of 4 and 6 is 12", "9/12 + 2/12"], "11/12"), ex("2 1/2 − 1 3/4", ["5/2 − 7/4 = 10/4 − 7/4"], "3/4")],
          [["Adding the denominators", "1/2 + 1/3 is not 2/5."], ["Forgetting to change both fractions", "Both must have the common denominator."], ["Leaving an improper answer", "Write 9/8 as 1 1/8."]],
          [("Why do the denominators have to be the same?", "You can only add parts of the same size."), ("How do I find a common denominator?", "Use the LCM of the denominators."), ("Should I simplify?", "Yes, always give the answer in its lowest terms.")]),

        U("multiplying-and-dividing-fractions", "O", "Multiply fractions by whole numbers and by fractions; divide fractions by whole numbers and by fractions; find a fraction of a quantity.",
          "Multiplying and Dividing Fractions", "Multiplying and Dividing Fractions",
          "Free Primary 5 maths worksheets on multiplying and dividing fractions: fraction of an amount, fraction × whole number, fraction × fraction, division of fractions and word problems. 100 questions with answers.",
          "Multiply tops, multiply bottoms", "To divide, turn the second fraction upside down and multiply.",
          [("Fraction × whole number", [rs(umf, "set_repeat", 20)]), ("Fraction of an amount", [rs(umf, "set_amounts", 10), rs(udf, "set_amounts", 10)]), ("Fraction × fraction", [rs(udf, "set_rule", 20)]),
           ("Dividing fractions", [rs(udf, "set_divide", 10), rs(usdf, "set_compute", 10)]), ("Word problems", [rs(umf, "set_words", 10), rs(udf, "set_words", 10)])],
          ul(["Fraction × fraction: multiply the numerators and multiply the denominators: 2/3 × 3/5 = 6/15 = 2/5.", "Of means multiply: 3/4 of 20 = 20 ÷ 4 × 3 = 15.",
              "To divide by a fraction, multiply by its reciprocal (turn it upside down): 3/4 ÷ 1/2 = 3/4 × 2/1 = 1 1/2."]),
          [ex("2/5 × 15", ["15 ÷ 5 × 2"], "6"), ex("5/6 ÷ 2/3", ["5/6 × 3/2 = 15/12"], "1 1/4")],
          [["Turning the first fraction upside down", "Only the fraction you divide by is turned over."], ["Multiplying the whole number by the denominator", "2/5 × 15 = 30/5 = 6, not 2/75."], ["Expecting multiplying to make bigger", "Multiplying by a fraction less than 1 makes a number smaller."]],
          [("What is a reciprocal?", "A fraction turned upside down: the reciprocal of 2/3 is 3/2."), ("Why does dividing by 1/2 double a number?", "There are two halves in every whole."), ("Can I cancel before multiplying?", "Yes. It makes the numbers smaller.")]),

        U("squares-and-square-roots", "N", "Find the squares of whole numbers; identify perfect squares; find square roots of perfect squares by factors; solve problems on squares and square roots.",
          "Squares and Square Roots", "Squares and Square Roots",
          "Free Primary 5 maths worksheets on square numbers, perfect squares and square roots of whole numbers, with word problems on square gardens and tiles. 100 questions with answers.",
          "5² = 5 × 5 = 25", "√25 = 5 because 5 × 5 = 25.",
          [("Square numbers", [rs(ukf5, "set_squares", 20)]), ("Find the square", [co(A4.sq_of, 20)]), ("Perfect squares", [co(A4.sq_perfect, 20)]),
           ("Square roots", [co(A4.sq_root, 20)]), ("Problems", [co(A4.sq_word, 10), co(A4.sq_sum, 10)])],
          ul(["The square of a number is the number times itself: 7² = 7 × 7 = 49.", "Perfect squares are 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, …",
              "The square root (√) undoes squaring: √64 = 8. Use factors in pairs: 144 = 12 × 12, so √144 = 12."]),
          [ex("√196", ["196 = 2 × 2 × 7 × 7 = 14 × 14"], "14"), ex("A square garden has sides of 9 m", ["Area = 9 × 9"], "81 m²")],
          [["Writing 6² = 12", "6² means 6 × 6 = 36, not 6 × 2."], ["Halving to find a square root", "√36 = 6, not 18."], ["Thinking every number has a whole-number root", "√20 is not a whole number."]],
          [("Is 1 a square number?", "Yes, 1 × 1 = 1."), ("Why are they called square numbers?", "That many dots can make a square."), ("What is the square root of 100?", "10.")]),

        U("estimation-and-rounding", "N", "Round whole numbers to the nearest ten, hundred, thousand and million; estimate sums, differences, products and quotients; use the number line.",
          "Estimation and Rounding of Large Numbers", "Estimation and Rounding",
          "Free Primary 5 maths worksheets on rounding to the nearest 10, 100, 1,000, 10,000 and 100,000, estimating answers and checking with estimates. 100 questions with answers.",
          "Look at the next digit: 5 or more, round up", "Estimate by rounding first.",
          [("Round to 10, 100 and 1,000", [rs(ukro, "set_small", 20)]), ("Round to 10,000", [rs(ukro, "set_tenk", 20)]), ("Round to 100,000", [rs(ukro, "set_hundredk", 20)]),
           ("Estimate calculations", [rs(sgx, "set_estimate", 20)]), ("Rounding in real life", [rs(ukro, "set_words", 20)])],
          ul(["To round, look at the digit to the right of the place you are rounding to. If it is 5 or more, round up; if it is 4 or less, round down.",
              "Estimate by rounding each number first: 4,867 + 3,214 ≈ 5,000 + 3,000 = 8,000.", "On a number line, a rounded number is the nearest marked number."]),
          [ex("Round 647,382 to the nearest 10,000", ["Next digit 7 → round up"], "650,000"), ex("Estimate 49 × 31", ["50 × 30"], "1,500")],
          [["Looking at the wrong digit", "Look only at the digit just to the right."], ["Changing the digits after the rounding place to other numbers", "They all become zeros."], ["Thinking an estimate must be exact", "An estimate is close, not exact."]],
          [("Why do we estimate?", "To check that an answer is sensible."), ("What is 35 rounded to the nearest ten?", "40, because 5 rounds up."), ("Is ≈ the same as =?", "No. ≈ means is about equal to.")]),

        U("decimals", "N", "Read and write decimals to three places; give the place value of decimal digits; compare, order and round decimals; add, subtract and multiply decimals.",
          "Decimals: Place Value, Comparing and Calculating", "Decimals",
          "Free Primary 5 maths worksheets on decimals: tenths, hundredths and thousandths, comparing and rounding decimals, and adding, subtracting and multiplying decimals. 100 questions with answers.",
          "Line up the decimal points", "0.5 = 5 tenths, 0.05 = 5 hundredths.",
          [("Decimal place value", [rs(usdp, "set_value", 12), rs(usdp, "set_forms", 8)]), ("Compare and round", [rs(usdp, "set_compare", 10), rs(usdp, "set_round", 10)]), ("Add decimals", [rs(usad, "set_line_up", 20)]),
           ("Subtract decimals", [rs(usad, "set_subtract", 20)]), ("Multiply decimals", [rs(usmd, "set_mul_whole", 14), co(A4.dec_mul1, 6)])],
          ul(["After the decimal point come tenths, hundredths and thousandths: in 3.476 the 7 is 7 hundredths.", "To compare decimals, line up the points and compare from the left: 0.6 &gt; 0.58.",
              "Line up the decimal points to add or subtract. Fill empty places with zeros."]),
          [ex("4.6 + 2.75", ["4.60 + 2.75"], "7.35"), ex("Round 6.384 to 1 decimal place", ["Next digit 8"], "6.4")],
          [["Thinking 0.58 &gt; 0.6 because 58 &gt; 6", "0.6 = 0.60, which is bigger than 0.58."], ["Lining up the last digits", "Line up the decimal points."], ["Losing the point in the answer", "Put the point in the answer under the other points."]],
          [("What is a decimal?", "A way of writing tenths, hundredths and thousandths after a point."), ("Is 0.50 the same as 0.5?", "Yes. A zero at the end does not change the value."), ("Where do we use decimals?", "In money, measuring and sports times.")]),

        U("percentages", "N", "Change fractions and decimals to percentages and percentages to fractions; find a percentage of a quantity; express one quantity as a percentage of another.",
          "Percentages: Fractions, Decimals and Percentages of Amounts", "Percentages",
          "Free Primary 5 maths worksheets on percentages: changing fractions and decimals to percentages, finding a percentage of an amount and test scores as percentages. 100 questions with answers.",
          "Per cent means out of 100", "50% = 1/2, 25% = 1/4, 10% = 1/10",
          [("Out of 100", [rs(sgpc, "set_hundred", 15), rs(ukdp, "set_fractions", 5)]), ("Fractions, decimals and percentages", [rs(sgpc, "set_convert", 10), rs(ukdp, "set_percent", 10)]), ("Percentage of an amount", [rs(sgpc, "set_of", 10), co(A.pct_of, 10)]),
           ("As a percentage", [co(A.pct_what, 20)]), ("Percentage problems", [co(A.pct_class, 10), rs(sgpc, "set_words", 10)])],
          ul(["Per cent (%) means out of 100: 35% = 35/100 = 0.35.", "To change a fraction to a percentage, multiply by 100: 3/4 × 100 = 75%.",
              "To find a percentage of an amount, divide by 100 and multiply: 20% of ₦4,500 = ₦900."]),
          [ex("18 out of 25 as a percentage", ["18 ÷ 25 × 100"], "72%"), ex("15% of ₦8,000", ["8,000 ÷ 100 × 15"], "₦1,200")],
          [["Writing 0.4 as 4%", "0.4 = 40/100 = 40%."], ["Dividing by the wrong number", "Score ÷ total × 100."], ["Thinking a percentage can never be more than 100", "It can, for example 150% of a number."]],
          [("What is 100%?", "The whole amount."), ("Why use percentages?", "They make it easy to compare, such as test scores out of different totals."), ("What is 1%?", "One hundredth of the whole.")]),

        U("algebraic-processes", "A", "Use letters and boxes for unknown numbers; write open sentences from word problems; solve simple equations involving the four operations.",
          "Algebraic Processes: Open Sentences and Simple Equations", "Open Sentences and Equations",
          "Free Primary 5 maths worksheets on open sentences and simple equations: finding the missing number, writing equations from word problems and solving them. 100 questions with answers.",
          "Do the same to both sides", "Undo the operation to find the unknown.",
          [("Missing numbers", [co(A4.os_box, 20)]), ("Write the open sentence", [co(A4.os_write, 20)]), ("Solve the equation", [co(A4.os_solve, 20)]),
           ("Is it true?", [co(A4.os_true, 20)]), ("Equations in real life", [rs(uk6a, "set_equations", 20)])],
          ul(["A letter or a box stands for an unknown number: x + 7 = 15.", "Undo the operation: in x + 7 = 15, take 7 from both sides, so x = 8.",
              "Check by putting your answer back: 8 + 7 = 15, so it is correct."]),
          [ex("3n = 27", ["Divide both sides by 3"], "n = 9"), ex("y − 14 = 30", ["Add 14 to both sides"], "y = 44")],
          [["Doing the operation instead of undoing it", "x + 7 = 15 means x = 15 − 7."], ["Reading 3n as 3 + n", "3n means 3 × n."], ["Not checking the answer", "Put the number back into the sentence."]],
          [("What is an open sentence?", "A number sentence with a missing number, such as □ + 9 = 20."), ("Why do we use letters?", "A letter can stand for any unknown number."), ("What is an equation?", "A sentence that says two things are equal.")]),

        U("commercial-arithmetic", "O", "Solve problems on money: profit and loss, simple interest, discount and commission; calculate profit and loss per cent.",
          "Commercial Arithmetic: Profit, Loss, Simple Interest, Discount and Commission", "Profit, Interest, Discount and Commission",
          "Free Primary 5 maths worksheets on money in naira: profit and loss, profit per cent, simple interest, discount and commission. 100 questions with answers.",
          "I = P × R × T ÷ 100", "Profit = selling price − cost price.",
          [("Profit and loss", [co(A4.mo_profit, 20)]), ("Profit and loss per cent", [co(A.profit_pct, 20)]), ("Simple interest", [co(A.si, 20)]),
           ("Discount", [co(A.discount, 20)]), ("Commission", [co(A.commission, 20)])],
          ul(["Profit = selling price − cost price. Loss = cost price − selling price.", "Profit per cent = profit ÷ cost price × 100.",
              "Simple interest I = P × R × T ÷ 100, where P is the principal, R the rate per cent and T the time in years.",
              "A discount is money taken off the marked price. A commission is a part of the sales paid to the seller."]),
          [ex("Interest on ₦50,000 at 8% for 3 years", ["50,000 × 8 × 3 ÷ 100"], "₦12,000"), ex("10% discount on ₦25,000", ["25,000 ÷ 10 = 2,500"], "Pay ₦22,500")],
          [["Dividing by the selling price for profit per cent", "Always divide by the cost price."], ["Forgetting to add the interest to get the amount", "Amount = principal + interest."], ["Giving the discount instead of the price to pay", "Price to pay = marked price − discount."]],
          [("What is the principal?", "The money saved or borrowed."), ("What does per annum mean?", "Per year."), ("Who gets commission?", "Agents and sales people, on what they sell.")]),

        U("perimeter-and-area", "M", "Find the perimeter of regular and irregular plane shapes; find the area of squares, rectangles and composite shapes; solve problems on area and perimeter.",
          "Perimeter and Area of Plane Shapes", "Perimeter and Area",
          "Free Primary 5 maths worksheets on perimeter and area: rectangles, squares and composite shapes, estimating area and word problems. 100 questions with answers.",
          "Perimeter: add the sides. Area: length × breadth.", "Area is in square units (cm², m²).",
          [("Perimeter", [rs(ukap, "set_perimeter", 20)]), ("Area of rectangles", [rs(ukap, "set_rect_area", 20)]), ("Composite shapes", [rs(ukap, "set_composite_area", 20)]),
           ("Estimate area", [rs(ukap, "set_estimate", 20)]), ("Problems", [rs(ukap, "set_story", 20)])],
          ul(["Perimeter is the distance all the way round a shape: add the lengths of all the sides.", "Area is the space inside a shape. Area of a rectangle = length × breadth; of a square = side × side.",
              "Split a composite (L-shaped) shape into rectangles, find each area and add."]),
          [ex("Rectangle 12 m by 7 m", ["Perimeter = 2 × (12 + 7)", "Area = 12 × 7"], "38 m and 84 m²")],
          [["Mixing up perimeter and area", "Perimeter is a length (m); area is in square units (m²)."], ["Adding only two sides", "A rectangle has four sides."], ["Counting a side twice in a composite shape", "Mark the sides as you add them."]],
          [("Can two shapes have the same area but different perimeters?", "Yes: 4 × 4 and 8 × 2 both have area 16."), ("What is a hectare?", "10,000 m², used for farms."), ("Why is area in square units?", "We count how many unit squares cover the shape.")]),

        U("volume-and-capacity", "M", "Find the volume of cubes and cuboids by counting cubes and by formula; relate volume to capacity in litres; solve problems on volume and capacity.",
          "Volume and Capacity of Cubes and Cuboids", "Volume and Capacity",
          "Free Primary 5 maths worksheets on volume of cubes and cuboids, cubic units, the formula length × breadth × height, litres and millilitres, and tank problems. 100 questions with answers.",
          "Volume = length × breadth × height", "1,000 cm³ = 1 litre",
          [("Count the cubes", [rs(sgv, "set_count", 20)]), ("Use the formula", [rs(usv, "set_formula", 20)]), ("Find a missing length", [rs(usv, "set_missing", 20)]),
           ("Litres and millilitres", [rs(sgv, "set_litres", 20)]), ("Tanks and containers", [rs(sgv, "set_tanks", 20)])],
          ul(["Volume is the space inside a solid. It is measured in cubic units: cm³ and m³.", "Volume of a cuboid = length × breadth × height. Volume of a cube = side × side × side.",
              "Capacity is how much a container holds. 1 cm³ = 1 ml and 1,000 cm³ = 1 litre."]),
          [ex("Cuboid 8 cm by 5 cm by 3 cm", ["8 × 5 × 3"], "120 cm³"), ex("A tank holds 6,000 cm³", ["6,000 ÷ 1,000"], "6 litres")],
          [["Adding the lengths", "Multiply the three lengths."], ["Writing cm² for volume", "Volume is in cm³."], ["Forgetting to change units", "All lengths must be in the same unit."]],
          [("What is the difference between volume and capacity?", "Volume is the space a solid takes up; capacity is how much a container can hold."), ("How many ml are in a litre?", "1,000 ml."), ("What is a cubic centimetre?", "The space taken by a cube with sides of 1 cm.")]),

        U("time", "M", "Read and write time in the 12-hour and 24-hour clock; convert units of time; find the duration of events and the time an event starts or ends.",
          "Time: 12-Hour and 24-Hour Clock, Durations and Units of Time", "Time",
          "Free Primary 5 maths worksheets on time: 12-hour and 24-hour clock, changing units of time, how long a journey takes and when an event ends. 100 questions with answers.",
          "1 hour = 60 minutes", "p.m. times: add 12 hours for the 24-hour clock.",
          [("24-hour clock", [co(A.t_24, 20)]), ("Units of time", [co(A.t_conv, 20)]), ("How long?", [co(A.t_dur, 20)]),
           ("When does it end?", [co(A.t_end, 20)]), ("Time problems", [rs(ukc, "set_time", 20)])],
          ul(["The 24-hour clock counts from 00:00 (midnight) to 23:59. For p.m. times add 12: 3:45 p.m. = 15:45.", "1 minute = 60 seconds, 1 hour = 60 minutes, 1 day = 24 hours, 1 week = 7 days, 1 year = 12 months.",
              "To find how long something takes, count on to the next hour, then on to the end time."]),
          [ex("A bus leaves at 7:40 a.m. and arrives at 10:15 a.m.", ["7:40 → 8:00 is 20 min, 8:00 → 10:00 is 2 h, 10:00 → 10:15 is 15 min"], "2 h 35 min")],
          [["Treating time like ordinary numbers", "There are 60 minutes in an hour, not 100."], ["Adding 12 to a.m. times", "Only p.m. times change: 9:00 a.m. = 09:00."], ["Mixing up 12:00 noon and midnight", "12:00 noon = 12:00; midnight = 00:00."]],
          [("Why use the 24-hour clock?", "It does not need a.m. and p.m., so timetables are clear."), ("How many days are in a leap year?", "366."), ("What is 00:00?", "Midnight.")]),

        U("temperature", "M", "Read temperature on a thermometer in degrees Celsius; find rises and falls in temperature; compare temperatures in towns and find the average temperature.",
          "Temperature in Degrees Celsius", "Temperature",
          "Free Primary 5 maths worksheets on temperature: reading a thermometer, degrees Celsius, rises and falls in temperature, temperatures of Nigerian cities and average temperature. 100 questions with answers.",
          "Temperature is measured in °C", "Water freezes at 0 °C and boils at 100 °C.",
          [("Read the thermometer", [co(A.temp_read, 20)]), ("Facts about temperature", [co(A.temp_fact, 8), co(A.temp_change, 12)]), ("Rise in temperature", [co(A.temp_diff, 20)]),
           ("Rise and fall", [co(A.temp_change, 20)]), ("Average temperature", [co(A.temp_avg, 20)])],
          ul(["Temperature tells us how hot or cold something is. We measure it with a thermometer in degrees Celsius (°C).",
              "Find the value of each small mark before you read the scale.", "A rise in temperature: add. A fall in temperature: subtract. Difference = higher − lower."]),
          [ex("From 23 °C at dawn to 34 °C at noon", ["34 − 23"], "a rise of 11 °C")],
          [["Reading the wrong mark", "Count how many degrees each small mark stands for."], ["Adding for a fall in temperature", "A fall means take away."], ["Writing °F", "In Nigeria we use degrees Celsius, °C."]],
          [("What is the normal body temperature?", "About 37 °C."), ("Why is it cold in harmattan mornings?", "Dry harmattan winds make nights and mornings cooler."), ("What is a clinical thermometer?", "A thermometer for taking body temperature.")]),

        U("bearings-and-directions", "G", "Identify the eight points of the compass; measure turns in degrees; give and use three-figure bearings; find back bearings.",
          "Directions, Turns and Three-Figure Bearings", "Bearings and Directions",
          "Free Primary 5 maths worksheets on directions and bearings: the eight compass points, turning through angles, three-figure bearings and back bearings. 100 questions with answers.",
          "Bearings start at north and go clockwise", "Always use three figures: 045°, 270°.",
          [("Compass points", [co(A4.cp_turn, 12), co(A4.cp_opposite, 8)]), ("Bearings of compass points", [co(A.bearing_dir, 8), co(A.bearing_name, 8), co(A.bearing_back, 4)]),
           ("Read the bearing", [co(A.bearing_read, 20)]), ("Turning", [co(A.bearing_turn, 20)]), ("Back bearings", [co(A.bearing_back, 20)])],
          ul(["The four main points are north, east, south and west. Between them are north-east, south-east, south-west and north-west.",
              "A bearing is an angle measured clockwise from north. It is written with three figures: east is 090°.", "The back bearing is the bearing for the return journey: add 180° if the bearing is less than 180°, otherwise subtract 180°."]),
          [ex("Bearing of south-west", ["South is 180°, south-west is 45° more"], "225°"), ex("Back bearing of 070°", ["70 + 180"], "250°")],
          [["Measuring anticlockwise", "Bearings always go clockwise from north."], ["Writing 45° instead of 045°", "A bearing has three figures."], ["Forgetting the 180° for the way back", "Back bearing = bearing ± 180°."]],
          [("Where does the sun rise?", "In the east."), ("How many degrees in a full turn?", "360°."), ("Who uses bearings?", "Pilots, sailors and map readers.")]),

        U("angles", "G", "Measure and draw angles with a protractor; name acute, right, obtuse and reflex angles; find angles on a straight line, at a point and in a triangle.",
          "Angles: Measuring, Types and Angle Facts", "Angles",
          "Free Primary 5 maths worksheets on angles: acute, right, obtuse and reflex angles, using a protractor, angles on a straight line, angles at a point and angles in a triangle. 100 questions with answers.",
          "Straight line 180°, full turn 360°", "Angles in a triangle add up to 180°.",
          [("Types of angle", [rs(ukan, "set_types", 20)]), ("Use a protractor", [rs(ukan, "set_protractor", 20)]), ("Angles on a straight line", [rs(sgan, "set_line", 20)]),
           ("Angles at a point", [rs(sgan, "set_point", 10), rs(sgan, "set_vertical", 10)]), ("Angles in shapes", [rs(sgtr, "set_sum", 20)])],
          ul(["Acute: less than 90°. Right: exactly 90°. Obtuse: between 90° and 180°. Reflex: between 180° and 360°.", "Angles on a straight line add up to 180°. Angles at a point add up to 360°.",
              "The three angles in a triangle add up to 180°."]),
          [ex("Two angles on a line: 115° and x", ["180 − 115"], "x = 65°"), ex("Triangle with 50° and 70°", ["180 − 50 − 70"], "60°")],
          [["Reading the wrong scale on the protractor", "Start from the 0 on the arm of the angle."], ["Using 360° for a straight line", "A straight line is 180°."], ["Thinking a longer arm means a bigger angle", "The size is the amount of turn."]],
          [("What is a reflex angle?", "An angle bigger than 180° and smaller than 360°."), ("How many right angles make a straight line?", "Two."), ("What tool measures angles?", "A protractor.")]),

        U("plane-shapes", "G", "Identify and describe the properties of triangles and quadrilaterals; classify triangles by sides and angles; classify quadrilaterals by their properties.",
          "Plane Shapes: Triangles and Quadrilaterals", "Plane Shapes",
          "Free Primary 5 maths worksheets on plane shapes: equilateral, isosceles, scalene and right-angled triangles, squares, rectangles, parallelograms, rhombuses, trapeziums and kites. 100 questions with answers.",
          "Count sides, look at angles", "A square is a special rectangle.",
          [("Triangles", [rs(uscf, "set_triangles", 20)]), ("Classify triangles", [rs(sgtr, "set_classify", 20)]), ("Quadrilaterals", [rs(uscf, "set_quads", 20)]),
           ("Properties of quadrilaterals", [rs(sgq, "set_properties", 20)]), ("Families of shapes", [rs(uscf, "set_hierarchy", 20)])],
          ul(["Triangles: equilateral (3 equal sides), isosceles (2 equal sides), scalene (no equal sides), right-angled (one 90° angle).",
              "Quadrilaterals have 4 sides: square, rectangle, parallelogram, rhombus, trapezium and kite.", "A square is also a rectangle and a rhombus, because it has all their properties."]),
          [ex("4 equal sides, no right angles", ["Opposite sides parallel"], "Rhombus")],
          [["Thinking a square is not a rectangle", "A square has 4 right angles, so it is a rectangle."], ["Mixing up rhombus and kite", "A rhombus has 4 equal sides; a kite has 2 pairs of equal sides next to each other."], ["Calling any 4-sided shape a square", "Check the sides and angles."]],
          [("What is a polygon?", "A closed flat shape with straight sides."), ("How many sides does a hexagon have?", "Six."), ("What is a trapezium?", "A quadrilateral with one pair of parallel sides.")]),

        U("three-dimensional-shapes", "G", "Identify cubes, cuboids, cylinders, cones, spheres, pyramids and prisms; count faces, edges and vertices; match solids to their nets.",
          "Three-Dimensional Shapes and Their Nets", "3D Shapes and Nets",
          "Free Primary 5 maths worksheets on 3D shapes: cubes, cuboids, cylinders, cones, spheres, prisms and pyramids, faces, edges and vertices, and nets. 100 questions with answers.",
          "Faces, edges, vertices", "A net folds up to make a solid.",
          [("Name the solid", [rs(uks3, "set_name3d", 20)]), ("Faces, edges and vertices", [co(A4.fev, 20)]), ("Solids and their faces", [rs(ukcn, "set_solids", 20)]),
           ("Nets", [rs(ukcn, "set_nets", 20)]), ("Solids around us", [co(A4.obj3d, 20)])],
          ul(["A face is a flat or curved surface, an edge is where two faces meet and a vertex is a corner.", "A cuboid has 6 rectangular faces, 12 edges and 8 vertices. A triangular prism has 5 faces.",
              "A net is a flat shape that folds to make a solid. A cube has 11 different nets."]),
          [ex("Square-based pyramid", ["1 square + 4 triangles"], "5 faces, 8 edges, 5 vertices")],
          [["Counting hidden edges twice", "Count each edge once."], ["Calling a cylinder a circle", "A circle is flat; a cylinder is solid."], ["Thinking every 6 squares make a cube net", "Fold it in your mind and check that no faces overlap."]],
          [("What solid is a tin of tomato paste?", "A cylinder."), ("What is a prism?", "A solid with the same cross-section all along its length."), ("Does a sphere have edges?", "No.")]),

        U("length-and-weight", "M", "Convert between units of length (mm, cm, m, km) and weight (g, kg, tonnes); add and subtract measures; solve word problems on length and weight.",
          "Length and Weight: Units and Conversions", "Length and Weight",
          "Free Primary 5 maths worksheets on measurement: converting millimetres, centimetres, metres and kilometres, grams, kilograms and tonnes, and measurement word problems. 100 questions with answers.",
          "1 km = 1,000 m, 1 kg = 1,000 g", "Big unit to small unit: multiply.",
          [("Units of length", [rs(ukc, "set_length", 15), co(A4.len_conv, 5)]), ("Mass and capacity", [rs(ukc, "set_mass_cap", 20)]), ("Add and subtract lengths", [co(A4.len_addsub, 20)]),
           ("Weight", [co(A4.wt_conv, 10), co(A4.wt_addsub, 10)]), ("Measurement problems", [rs(ukc, "set_story", 20)])],
          ul(["10 mm = 1 cm, 100 cm = 1 m, 1,000 m = 1 km.", "1,000 g = 1 kg, 1,000 kg = 1 tonne.",
              "To change a big unit to a smaller unit, multiply. To change a small unit to a bigger unit, divide."]),
          [ex("3.25 km in metres", ["3.25 × 1,000"], "3,250 m"), ex("4,500 g in kilograms", ["4,500 ÷ 1,000"], "4.5 kg")],
          [["Dividing when you should multiply", "There are more small units, so the number gets bigger."], ["Using 100 for kilometres", "1 km = 1,000 m."], ["Adding measures in different units", "Change them to the same unit first."]],
          [("What is a tonne?", "1,000 kg, used for lorries of cement or yams."), ("Which unit for the distance from Lagos to Abuja?", "Kilometres."), ("Which unit for a pin?", "Millimetres.")]),

        U("binary-numbers", "N", "Count in base two; change base ten numbers to binary numbers and binary numbers to base ten; add and subtract binary numbers.",
          "Binary Numbers (Base Two)", "Binary Numbers",
          "Free Primary 5 maths worksheets on binary numbers: base two place values, changing between base ten and base two, and adding and subtracting binary numbers. 100 questions with answers.",
          "Base two uses only 0 and 1", "Place values: 1, 2, 4, 8, 16, 32, …",
          [("Place values", [co(A.bin_place, 5), co(A.bin_compare, 15)]), ("Binary to base ten", [co(A.bin_to, 20)]), ("Base ten to binary", [co(A.bin_from, 20)]),
           ("Add and subtract", [co(A.bin_add, 10), co(A.bin_sub, 10)]), ("Binary in real life", [co(A.bin_life, 20)])],
          ul(["Base two (binary) uses only the digits 0 and 1. Computers store numbers this way.", "The place values double from the right: 1, 2, 4, 8, 16, 32.",
              "To change to base ten, add the place values where there is a 1. To change to binary, divide by 2 again and again and read the remainders upwards."]),
          [ex("1101₂ to base ten", ["8 + 4 + 0 + 1"], "13"), ex("19 to binary", ["19 = 16 + 2 + 1"], "10011₂")],
          [["Reading remainders from the top", "Read them from the bottom up."], ["Using 10s as place values", "Binary places are 1, 2, 4, 8, …, not 1, 10, 100."], ["Writing 1 + 1 = 2 in binary", "1 + 1 = 10₂: write 0 and carry 1."]],
          [("Why do computers use binary?", "A switch can be on (1) or off (0)."), ("What is 1000₂?", "8."), ("What does the small 2 mean?", "The number is in base two.")]),

        U("data-presentation", "S", "Collect and present data in tables, bar charts, line graphs and pie charts; read and interpret data from charts and tables.",
          "Data Presentation: Tables, Bar Charts, Line Graphs and Pie Charts", "Data Presentation",
          "Free Primary 5 maths worksheets on data presentation: reading tables and timetables, bar charts, line graphs and pie charts. 100 questions with answers.",
          "Read the title, the axes and the scale", "A pie chart shows parts of a whole.",
          [("Bar charts", [rs(ukst, "set_bar", 20)]), ("Line graphs", [rs(uklg, "set_read", 20)]), ("Tables", [rs(uklg, "set_tables", 14), rs(uklg, "set_timetables", 6)]),
           ("Pie charts", [rs(ukpl, "set_fractions", 16), rs(ukpl, "set_amounts", 4)]), ("Pie chart angles", [rs(ukpl, "set_angles", 20)])],
          ul(["A table puts data in rows and columns. A bar chart shows amounts with bars.", "A line graph shows how something changes over time, such as temperature through a day.",
              "A pie chart shows parts of a whole. The whole circle is 360°: half the circle is 180° and a quarter is 90°."]),
          [ex("A quarter of a pie chart of 40 pupils", ["40 ÷ 4"], "10 pupils")],
          [["Not reading the scale", "Each line on the axis may stand for 2, 5 or 10."], ["Reading the wrong bar", "Use a ruler across to the axis."], ["Forgetting the whole pie is 360°", "Use 360° to find the angle of each part."]],
          [("Which chart is best for change over time?", "A line graph."), ("Which chart shows parts of a whole?", "A pie chart."), ("What is data?", "Facts or numbers that we collect.")]),

        U("mean-median-and-mode", "S", "Find the mean, median and mode of a set of data; find the range; solve problems on averages.",
          "Mean, Median and Mode (Measures of Central Tendency)", "Mean, Median and Mode",
          "Free Primary 5 maths worksheets on averages: the mean, the median, the mode and the range of a set of data, with problems on test scores and missing numbers. 100 questions with answers.",
          "Mean = total ÷ number of items", "Median: the middle. Mode: the most common.",
          [("Mean", [co(A.mean_list, 20)]), ("Median", [co(A.median_list, 20)]), ("Mode and range", [co(A.mode_word, 10), co(A.range_list, 10)]),
           ("Average scores", [co(A.mean_word, 20)]), ("Mean problems", [co(A.mean_missing, 10), rs(ukmn, "set_words", 10)])],
          ul(["Mean: add all the values and divide by how many there are.", "Median: arrange the values in order and take the middle one. If there are two middle values, find the number halfway between them.",
              "Mode: the value that appears most often. Range: highest − lowest."]),
          [ex("4, 9, 6, 9, 7", ["Mean = 35 ÷ 5 = 7", "In order 4, 6, 7, 9, 9"], "mean 7, median 7, mode 9")],
          [["Forgetting to order the values for the median", "Arrange them first."], ["Dividing by the wrong number", "Divide by how many values there are."], ["Giving how often for the mode", "The mode is the value itself."]],
          [("What is an average?", "One number that represents a set of data, such as the mean."), ("Can the mean be a decimal?", "Yes."), ("Which average is the most common value?", "The mode.")]),
    ]


if __name__ == "__main__":
    main("primary-5", "Primary 5", units, 150500)
