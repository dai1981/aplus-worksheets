# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 6 (NERDC 9-Year Basic Education Curriculum; the year of the Common Entrance examination into JSS 1).
  python3 tools/ng_p6.py [number …]      seed = 150600 + number, reused modules 1529NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex
import ng_p4a as A4
import ng_p5a as A


def units():
    pv = mod("gen_uk_maths_y6_place_value", 152901)
    fp = mod("gen_uk_maths_y6_factors_primes", 152902)
    asf = mod("gen_uk_maths_y6_add_sub_fractions", 152903)
    scf = mod("gen_uk_maths_y6_simplify_compare_fractions", 152904)
    sdf = mod("gen_sg_maths_p6_dividing_fractions", 152905)
    sfw = mod("gen_sg_maths_p6_fraction_word_problems", 152906)
    dc = mod("gen_uk_maths_y6_decimal_calculations", 152907)
    usdo = mod("gen_us_math_g6_decimal_operations", 152908)
    pc = mod("gen_uk_maths_y6_percentages", 152909)
    sgp = mod("gen_sg_maths_p6_percentage", 152910)
    sgr = mod("gen_sg_maths_p6_ratio", 152911)
    sgrw = mod("gen_sg_maths_p6_ratio_word_problems", 152912)
    usx = mod("gen_us_math_g6_exponents", 152913)
    oo = mod("gen_uk_maths_y6_order_of_operations", 152914)
    sga = mod("gen_sg_maths_p6_algebra", 152915)
    usoe = mod("gen_us_math_g6_one_step_equations", 152916)
    cu = mod("gen_uk_maths_y6_converting_units", 152917)
    av = mod("gen_uk_maths_y6_area_volume", 152918)
    usap = mod("gen_us_math_g6_area_polygons", 152919)
    sgc = mod("gen_sg_maths_p6_circles", 152920)
    usv = mod("gen_us_math_g6_volume", 152921)
    sgv = mod("gen_sg_maths_p6_volume", 152922)
    an = mod("gen_uk_maths_y6_angles", 152923)
    sgan = mod("gen_sg_maths_p6_angles", 152924)
    cn = mod("gen_uk_maths_y6_circles_nets", 152925)
    ussa = mod("gen_us_math_g6_surface_area", 152926)
    sgav = mod("gen_sg_maths_p6_average", 152927)
    pl = mod("gen_uk_maths_y6_pie_line", 152928)
    pr = mod("gen_uk_maths_y7_probability", 152929)
    alg = mod("gen_uk_maths_y6_algebra", 152930)
    lg5 = mod("gen_uk_maths_y5_line_graphs_tables", 152932)
    auc = mod("gen_au_maths_y3_chance", 152931)

    return [
        U("whole-numbers-up-to-billions", "N", "Count, read and write whole numbers up to billions; give the place value of digits; compare, order and round large numbers.",
          "Whole Numbers up to Billions: Place Value and Rounding", "Whole Numbers up to Billions",
          "Free Primary 6 maths worksheets on large whole numbers: place value up to billions, reading and writing numbers, comparing and ordering, and rounding. 100 questions with answers.",
          "Units, thousands, millions, billions", "Each comma group has hundreds, tens and units.",
          [("Place value", [rs(pv, "set_value", 20)]), ("Compare and order", [rs(pv, "set_compare", 20)]), ("Rounding", [rs(pv, "set_round", 20)]),
           ("Large numbers in words", [rs(pv, "set_words", 20)]), ("Counting in large steps", [co(A4.wn_more, 10), co(A4.sk_next, 10)])],
          ul(["Group the digits in threes from the right: billions, millions, thousands, units. 3,045,720,000 is three billion, forty-five million, seven hundred and twenty thousand.",
              "1 thousand = 1,000; 1 million = 1,000 thousands; 1 billion = 1,000 millions.", "To round, look at the next digit to the right: 5 or more rounds up."]),
          [ex("Value of 7 in 4,371,256", ["7 is in the ten thousands place"], "70,000"), ex("Round 6,482,900 to the nearest million", ["Next digit 4"], "6,000,000")],
          [["Writing too few zeros", "One billion has nine zeros: 1,000,000,000."], ["Comparing numbers of different lengths from the left", "Count the digits first."], ["Rounding the wrong place", "Underline the place you round to first."]],
          [("How many millions make a billion?", "1,000."), ("What is the population of Nigeria in figures?", "About 230 million, written 230,000,000."), ("Why do we round large numbers?", "To make them easier to read and remember.")]),

        U("number-bases", "N", "Count in base two and other bases; convert numbers from base ten to other bases and from other bases to base ten; add and subtract in base two.",
          "Number Bases: Binary and Other Bases", "Number Bases",
          "Free Primary 6 maths worksheets on number bases: base two (binary), base three, four, five and eight, converting to and from base ten, and binary addition and subtraction. 100 questions with answers.",
          "Base b place values: 1, b, b², b³", "Divide by the base, read the remainders upwards.",
          [("Binary to base ten", [co(A.bin_to, 20)]), ("Base ten to binary", [co(A.bin_from, 20)]), ("Other bases to base ten", [co(A.base_to, 20)]),
           ("Base ten to other bases", [co(A.base_from, 20)]), ("Binary addition and subtraction", [co(A.bin_add, 10), co(A.bin_sub, 10)])],
          ul(["In base ten the place values are 1, 10, 100, 1,000. In base five they are 1, 5, 25, 125. In base two they are 1, 2, 4, 8, 16.",
              "A digit in base b is always less than b: base five uses only 0, 1, 2, 3 and 4.", "To change base ten to another base, divide by the base again and again and read the remainders from the bottom up."]),
          [ex("234₅ to base ten", ["2 × 25 + 3 × 5 + 4"], "69"), ex("29 to base four", ["29 = 1 × 16 + 3 × 4 + 1"], "131₄")],
          [["Using a digit as big as the base", "There is no digit 5 in base five."], ["Reading remainders downwards", "Read them from the last one up."], ["Multiplying by 10 for every place", "Multiply by the base, not by 10."]],
          [("Why is base two used in computers?", "Electric switches are either on (1) or off (0)."), ("What does 101₂ mean?", "1 four, 0 twos and 1 unit: 5."), ("What base do we use every day?", "Base ten.")]),

        U("factors-lcm-and-hcf", "N", "Find factors, multiples and prime factors of whole numbers; find the LCM and HCF of two or three numbers; solve problems on LCM and HCF.",
          "Factors, Prime Factors, LCM and HCF", "Factors, LCM and HCF",
          "Free Primary 6 maths worksheets on factors and prime factors, the lowest common multiple (LCM) and the highest common factor (HCF) of two or three numbers, and word problems. 100 questions with answers.",
          "Prime factors build every number", "HCF divides; LCM is divided by.",
          [("Factors", [rs(fp, "set_factors", 20)]), ("Primes and prime factors", [rs(fp, "set_primes", 20)]), ("HCF", [rs(fp, "set_hcf", 20)]),
           ("LCM", [rs(fp, "set_lcm", 10), co(A4.lcm3, 10)]), ("Problems", [rs(fp, "set_words", 20)])],
          ul(["Every whole number greater than 1 is a product of prime numbers: 60 = 2 × 2 × 3 × 5.", "HCF: multiply the prime factors that the numbers share.",
              "LCM: multiply the highest power of each prime factor that appears."]),
          [ex("HCF and LCM of 24 and 36", ["24 = 2 × 2 × 2 × 3, 36 = 2 × 2 × 3 × 3"], "HCF 12, LCM 72")],
          [["Including 1 as a prime factor", "1 is not prime."], ["Multiplying all the factors for the HCF", "Use only the shared factors."], ["Thinking the LCM is the product", "6 × 8 = 48, but the LCM of 6 and 8 is 24."]],
          [("What is a prime factor?", "A factor that is a prime number."), ("Is the HCF ever bigger than the numbers?", "No. It is at most the smaller number."), ("When is the LCM the product of the numbers?", "When their HCF is 1.")]),

        U("fractions", "O", "Add, subtract, multiply and divide fractions and mixed numbers; compare and order fractions; solve word problems involving fractions.",
          "Fractions: The Four Operations and Word Problems", "Fractions",
          "Free Primary 6 maths worksheets on fractions: comparing and ordering, adding and subtracting with unlike denominators, multiplying and dividing fractions and mixed numbers, and word problems. 100 questions with answers.",
          "Common denominator to add; reciprocal to divide", "Change mixed numbers to improper fractions first.",
          [("Compare and order", [rs(scf, "set_compare", 20)]), ("Add and subtract", [rs(asf, "set_unrelated", 10), rs(asf, "set_mixed", 10)]), ("Divide fractions", [rs(sdf, "set_frac_by_frac", 10), rs(sdf, "set_mixed", 10)]),
           ("Fraction of a quantity", [rs(sfw, "set_quantity", 14), rs(sfw, "set_compare", 6)]), ("Word problems", [rs(sfw, "set_remainder", 10), rs(sfw, "set_whole", 10)])],
          ul(["To add or subtract, change to a common denominator (use the LCM).", "To multiply, multiply the numerators and the denominators. To divide, multiply by the reciprocal of the second fraction.",
              "In word problems, find what the whole is first, then the fraction of it, or the fraction that is left."]),
          [ex("2 1/3 ÷ 1 3/4", ["7/3 ÷ 7/4 = 7/3 × 4/7"], "4/3 = 1 1/3"), ex("Ade spent 2/5 of ₦5,000", ["5,000 ÷ 5 × 2"], "₦2,000")],
          [["Dividing without changing mixed numbers", "Change them to improper fractions first."], ["Finding the fraction of what is left from the whole", "Read the question: 'of the remainder' means of what is left."], ["Not simplifying", "Give answers in their lowest terms."]],
          [("What is the reciprocal of 3?", "1/3."), ("How do I compare 5/8 and 3/5?", "25/40 and 24/40, so 5/8 is bigger."), ("Why does dividing by a fraction give a bigger answer?", "You are finding how many small parts fit.")]),

        U("decimals", "O", "Add, subtract, multiply and divide decimals; multiply and divide by 10, 100 and 1,000; convert between fractions and decimals; solve word problems.",
          "Decimals: The Four Operations", "Decimals",
          "Free Primary 6 maths worksheets on decimals: multiplying and dividing by powers of ten, adding, subtracting, multiplying and dividing decimals, and word problems. 100 questions with answers.",
          "Count the decimal places", "× 10 moves digits one place left.",
          [("× and ÷ by 10, 100 and 1,000", [rs(dc, "set_powers", 20)]), ("Add and subtract", [rs(dc, "set_add_sub", 20)]), ("Multiply decimals", [rs(dc, "set_multiply", 20)]),
           ("Divide decimals", [rs(dc, "set_divide", 10), rs(usdo, "set_div_dec", 10)]), ("Word problems", [rs(usdo, "set_words", 20)])],
          ul(["Line up the decimal points to add and subtract.", "To multiply, multiply as whole numbers, then count the decimal places in the question: 0.4 × 0.3 = 0.12.",
              "To divide by a decimal, multiply both numbers by 10 or 100 so that you divide by a whole number: 4.8 ÷ 0.6 = 48 ÷ 6 = 8."]),
          [ex("2.5 × 1.4", ["25 × 14 = 350", "2 decimal places"], "3.50 = 3.5"), ex("7.2 ÷ 0.08", ["720 ÷ 8"], "90")],
          [["Putting the point in the wrong place", "Count the decimal places in the question."], ["Thinking multiplying always makes bigger", "× 0.5 halves a number."], ["Moving the point only in one number", "When you divide, move the point in both numbers."]],
          [("What is 0.1 as a fraction?", "1/10."), ("Why do we multiply both numbers by 10 when dividing?", "It does not change the answer, but makes the divisor a whole number."), ("Where do we use decimals?", "In money, measurements and sport times.")]),

        U("percentages", "N", "Convert between fractions, decimals and percentages; find a percentage of a quantity; express one quantity as a percentage of another; find percentage increase and decrease.",
          "Percentages: Of Amounts, Increase and Decrease", "Percentages",
          "Free Primary 6 maths worksheets on percentages: fractions, decimals and percentages, percentage of an amount, one number as a percentage of another, and percentage increase and decrease. 100 questions with answers.",
          "Per cent = out of 100", "Increase: add the percentage. Decrease: take it away.",
          [("Simple percentages", [rs(pc, "set_simple", 20)]), ("Percentage of an amount", [co(A.pct_of, 20)]), ("As a percentage", [rs(pc, "set_what", 10), co(A.pct_what, 10)]),
           ("Increase", [rs(sgp, "set_increase", 14), rs(sgp, "set_whole", 6)]), ("Decrease", [rs(sgp, "set_decrease", 14), rs(sgp, "set_review", 6)])],
          ul(["Percent means out of 100: 45% = 45/100 = 0.45.", "To find 15% of an amount, find 10% and 5% and add, or multiply by 15 and divide by 100.",
              "Percentage increase or decrease = change ÷ original × 100."]),
          [ex("Price of ₦8,000 goes up by 15%", ["15% of 8,000 = 1,200"], "₦9,200"), ex("From 50 to 40", ["Change 10, 10 ÷ 50 × 100"], "a 20% decrease")],
          [["Dividing by the new number", "Always divide by the original amount."], ["Adding percentages of different amounts", "Each percentage is of its own amount."], ["Writing 0.05 as 50%", "0.05 = 5%."]],
          [("What is 100%?", "The whole amount."), ("Is a 50% increase then a 50% decrease the same as no change?", "No. 100 → 150 → 75."), ("How do I find 1%?", "Divide by 100.")]),

        U("ratio-and-proportion", "N", "Write and simplify ratios; share quantities in a given ratio; solve problems on direct and inverse proportion.",
          "Ratio and Proportion", "Ratio and Proportion",
          "Free Primary 6 maths worksheets on ratio and proportion: simplifying ratios, sharing in a ratio, direct proportion with costs and inverse proportion with workers and days. 100 questions with answers.",
          "Ratio compares; proportion scales", "More workers, fewer days: inverse proportion.",
          [("Writing ratios", [rs(sgr, "set_writing", 20)]), ("Equivalent ratios", [rs(sgr, "set_equivalent", 10), co(A.ratio_simplify, 10)]), ("Sharing in a ratio", [co(A.ratio_share, 10), rs(sgrw, "set_share", 10)]),
           ("Direct proportion", [co(A.proportion, 20)]), ("Inverse proportion", [co(A.inverse_prop, 20)])],
          ul(["A ratio compares quantities of the same kind: 8 : 12 = 2 : 3.", "Direct proportion: when one quantity doubles, the other doubles too (cost and number of items).",
              "Inverse proportion: when one quantity doubles, the other halves (number of workers and days needed)."]),
          [ex("6 books cost ₦7,200. Cost of 10?", ["One costs ₦1,200"], "₦12,000"), ex("4 men take 9 days. 6 men?", ["4 × 9 = 36 man-days, 36 ÷ 6"], "6 days")],
          [["Using direct proportion for workers and days", "More workers finish sooner."], ["Comparing different units", "Change to the same unit before writing a ratio."], ["Sharing by one part only", "Add all the parts first."]],
          [("What is the unitary method?", "Find the value of one, then multiply."), ("Can a ratio have three parts?", "Yes, such as 2 : 3 : 5."), ("Is speed and time direct or inverse?", "For a fixed distance, it is inverse.")]),

        U("squares-cubes-and-roots", "N", "Find squares and cubes of whole numbers; find square roots and cube roots of perfect squares and cubes; use prime factors to find square roots; solve problems.",
          "Squares, Cubes, Square Roots and Cube Roots", "Squares, Cubes and Roots",
          "Free Primary 6 maths worksheets on squares and cubes, square roots and cube roots, using prime factors to find square roots, and problems on square plots and cube tanks. 100 questions with answers.",
          "n² = n × n, n³ = n × n × n", "√ undoes squaring; ∛ undoes cubing.",
          [("Squares and square roots", [co(A.sq_big, 20)]), ("Cubes", [co(A.cube_of, 11), rs(usx, "set_powers", 9)]), ("Cube roots", [co(A.cube_root, 11), co(A4.sq_root, 9)]),
           ("Square roots by prime factors", [co(A.sq_factor, 15), co(A4.sq_perfect, 5)]), ("Problems", [co(A.sq_cube_word, 20)])],
          ul(["The square of 13 is 13² = 169. The cube of 4 is 4³ = 4 × 4 × 4 = 64.", "√169 = 13 and ∛64 = 4.",
              "To find a square root by prime factors, put the factors in pairs and take one from each pair: 324 = 2 × 2 × 3 × 3 × 3 × 3, so √324 = 2 × 3 × 3 = 18."]),
          [ex("√576", ["576 = 2⁶ × 3² → 2³ × 3"], "24"), ex("∛125", ["5 × 5 × 5 = 125"], "5")],
          [["Writing 4³ = 12", "4³ = 4 × 4 × 4 = 64."], ["Dividing by 2 for a square root", "√64 = 8, not 32."], ["Dividing by 3 for a cube root", "∛27 = 3, not 9."]],
          [("Which numbers are both squares and cubes?", "1, 64, 729, …"), ("Is √2 a whole number?", "No."), ("Where do we use cube roots?", "To find the edge of a cube from its volume.")]),

        U("order-of-operations", "O", "Use the order of operations (BODMAS) to work out expressions with brackets, division, multiplication, addition and subtraction; solve word problems.",
          "Order of Operations (BODMAS)", "BODMAS",
          "Free Primary 6 maths worksheets on BODMAS: brackets first, then division and multiplication, then addition and subtraction, with word problems. 100 questions with answers.",
          "B O D M A S", "÷ and × left to right; + and − left to right.",
          [("× and ÷ before + and −", [rs(oo, "set_precedence", 20)]), ("Brackets first", [rs(oo, "set_brackets", 20)]), ("Left to right", [rs(oo, "set_ltr", 20)]),
           ("Harder brackets", [rs(oo, "set_brackets_large", 20)]), ("Word problems", [rs(oo, "set_words", 20)])],
          ul(["BODMAS: Brackets, Of (powers), Division, Multiplication, Addition, Subtraction.", "Division and multiplication have equal rank: work them from left to right. The same for addition and subtraction.",
              "In a word problem, write one number sentence and use brackets for the part you work out first."]),
          [ex("18 − 4 × 3 + 2", ["4 × 3 = 12", "18 − 12 + 2"], "8"), ex("(18 − 4) × (3 + 2)", ["14 × 5"], "70")],
          [["Working from left to right only", "Do × and ÷ before + and −."], ["Always multiplying before dividing", "÷ and × go left to right."], ["Ignoring brackets", "Brackets always come first."]],
          [("What does the O stand for?", "Of, which means powers or a fraction of."), ("Why do we need BODMAS?", "So that everyone gets the same answer."), ("Is 2 + 3 × 4 = 20?", "No. 3 × 4 = 12, then 2 + 12 = 14.")]),

        U("algebraic-expressions-and-equations", "A", "Write algebraic expressions; simplify expressions by collecting like terms; substitute values; solve simple equations and word problems.",
          "Algebra: Expressions and Simple Equations", "Expressions and Equations",
          "Free Primary 6 maths worksheets on algebra: writing expressions, simplifying like terms, substituting values, solving simple equations and word problems. 100 questions with answers.",
          "Like terms can be added", "Do the same to both sides of an equation.",
          [("Write expressions", [rs(sga, "set_write", 16), rs(usoe, "set_models", 4)]), ("Simplify", [rs(sga, "set_simplify", 20)]), ("Substitute", [rs(sga, "set_evaluate", 16), rs(usoe, "set_substitute", 4)]),
           ("Solve equations", [rs(sga, "set_solve", 20)]), ("Word problems", [rs(usoe, "set_words", 10), rs(sga, "set_words", 10)])],
          ul(["Letters stand for numbers. 3a means 3 × a. a + a + a = 3a.", "Like terms have the same letter: 4x + 2x = 6x, but 4x + 2y cannot be simplified.",
              "To solve an equation, undo each step: 3x + 5 = 20 → 3x = 15 → x = 5."]),
          [ex("Simplify 5p + 3 − 2p + 4", ["5p − 2p = 3p, 3 + 4 = 7"], "3p + 7"), ex("If a = 4, find 3a − 2", ["3 × 4 − 2"], "10")],
          [["Adding unlike terms", "2a + 3b stays as it is."], ["Reading 2a as 2 + a", "2a = 2 × a."], ["Doing a step to one side only", "Do the same to both sides."]],
          [("What is a term?", "A number, a letter or both multiplied, such as 7, x or 5y."), ("What is the coefficient in 7x?", "7."), ("What is an equation?", "Two expressions joined by =.")]),

        U("commercial-arithmetic", "O", "Solve problems on profit and loss per cent, simple interest, discount, commission, VAT and hire purchase using naira.",
          "Commercial Arithmetic: Profit, Interest, Discount, Commission and VAT", "Commercial Arithmetic",
          "Free Primary 6 maths worksheets on commercial arithmetic in naira: profit and loss per cent, simple interest, discount, commission, VAT at 7.5% and hire purchase. 100 questions with answers.",
          "Profit % = profit ÷ cost price × 100", "Simple interest = P × R × T ÷ 100",
          [("Profit and loss per cent", [co(A.profit_pct, 20)]), ("Simple interest", [co(A.si, 20)]), ("Discount", [co(A.discount, 20)]),
           ("Commission and VAT", [co(A.commission, 10), co(A.vat, 10)]), ("Hire purchase", [co(A.hire, 20)])],
          ul(["Profit or loss per cent is always worked on the cost price.", "Simple interest I = PRT ÷ 100. Amount = principal + interest.",
              "VAT in Nigeria is 7.5% of the price. In hire purchase you pay a deposit and then instalments, so you pay more than the cash price."]),
          [ex("Bought ₦40,000, sold ₦46,000", ["Profit ₦6,000", "6,000 ÷ 40,000 × 100"], "15% profit"), ex("VAT on ₦20,000", ["20,000 × 7.5 ÷ 100"], "₦1,500")],
          [["Using the selling price for profit per cent", "Divide by the cost price."], ["Forgetting to add the deposit", "Hire purchase total = deposit + all instalments."], ["Taking the rate per month for per year", "Per annum means per year."]],
          [("What is VAT?", "Value Added Tax, paid on many goods and services."), ("What is a principal?", "Money saved or borrowed."), ("Why is hire purchase more expensive?", "You pay interest for paying slowly.")]),

        U("length-weight-and-capacity", "M", "Convert between units of length, weight and capacity; add, subtract, multiply and divide measures; solve word problems.",
          "Length, Weight and Capacity", "Length, Weight and Capacity",
          "Free Primary 6 maths worksheets on measurement: converting units of length, weight and capacity, calculating with measures and word problems. 100 questions with answers.",
          "Kilo = 1,000, centi = 1/100, milli = 1/1,000", "Change to the same unit first.",
          [("Units of length", [rs(cu, "set_length", 16), co(A4.len_conv, 4)]), ("Weight and capacity", [rs(cu, "set_mass_cap", 20)]), ("Weight calculations", [co(A4.wt_muldiv, 10), co(A4.wt_addsub, 10)]),
           ("Capacity calculations", [co(A4.cap_muldiv, 10), co(A4.cap_conv, 10)]), ("Word problems", [rs(cu, "set_story", 20)])],
          ul(["Length: 10 mm = 1 cm, 100 cm = 1 m, 1,000 m = 1 km.", "Weight: 1,000 g = 1 kg, 1,000 kg = 1 tonne. Capacity: 1,000 ml = 1 litre, 100 cl = 1 litre.",
              "Big unit → small unit: multiply. Small unit → big unit: divide."]),
          [ex("2.4 kg − 750 g", ["2,400 g − 750 g"], "1,650 g = 1.65 kg"), ex("A 5-litre can fills 25 cl cups", ["500 ÷ 25"], "20 cups")],
          [["Mixing units", "Change everything to the same unit first."], ["Using 100 for grams", "1 kg = 1,000 g."], ["Losing the units", "Always write the unit in the answer."]],
          [("How many cl in a litre?", "100."), ("How many grams in half a kilogram?", "500."), ("What is a tonne used for?", "Heavy things such as lorries, cement and crops.")]),

        U("perimeter-and-area", "M", "Find the perimeter and area of squares, rectangles, triangles, parallelograms, trapeziums and composite shapes; solve problems.",
          "Perimeter and Area of Plane Shapes", "Perimeter and Area",
          "Free Primary 6 maths worksheets on area: rectangles, triangles, parallelograms, trapeziums and composite shapes, with word problems. 100 questions with answers.",
          "Triangle: ½ × base × height", "Use the height at right angles to the base.",
          [("Rectangles and squares", [rs(av, "set_rect", 20)]), ("Triangles", [rs(av, "set_tri", 20)]), ("Parallelograms", [rs(av, "set_para", 20)]),
           ("Trapeziums and other quadrilaterals", [rs(usap, "set_quads", 20)]), ("Composite shapes", [rs(usap, "set_composite", 20)])],
          ul(["Area of a rectangle = length × breadth. Area of a parallelogram = base × height.", "Area of a triangle = ½ × base × height.",
              "Area of a trapezium = ½ × (sum of the parallel sides) × height."]),
          [ex("Triangle with base 12 cm and height 7 cm", ["½ × 12 × 7"], "42 cm²"), ex("Trapezium with parallel sides 6 m and 10 m, height 4 m", ["½ × 16 × 4"], "32 m²")],
          [["Using the slanting side as the height", "The height is at right angles to the base."], ["Forgetting the ½ for a triangle", "A triangle is half a parallelogram."], ["Giving area in cm", "Area is in square units."]],
          [("Why is a triangle half of a rectangle?", "A diagonal cuts a rectangle into two equal triangles."), ("What is a hectare?", "10,000 m²."), ("How do I find the area of an L-shape?", "Split it into rectangles.")]),

        U("circles", "M", "Identify the parts of a circle; find the circumference and area of circles using π = 22/7 or 3.14; solve problems with circles.",
          "Circles: Circumference and Area", "Circles",
          "Free Primary 6 maths worksheets on circles: radius, diameter and circumference, the area of a circle, semicircles and composite shapes. 100 questions with answers.",
          "C = πd = 2πr, A = πr²", "π ≈ 22/7 ≈ 3.14",
          [("Parts of a circle", [rs(sgc, "set_parts_of_circles", 20)]), ("Circumference", [rs(sgc, "set_circumference", 20)]), ("Area", [rs(sgc, "set_area", 20)]),
           ("Composite figures", [rs(sgc, "set_composite", 20)]), ("Problems", [rs(sgc, "set_psle", 10), co(A.circ_word, 10)])],
          ul(["The diameter is twice the radius: d = 2r.", "Circumference (the distance round a circle) = π × diameter.",
              "Area of a circle = π × radius × radius. Use π = 22/7 when the radius is a multiple of 7, otherwise 3.14."]),
          [ex("Circle of radius 7 cm", ["C = 2 × 22/7 × 7", "A = 22/7 × 7 × 7"], "C = 44 cm, A = 154 cm²")],
          [["Using the diameter for the area", "Area uses the radius."], ["Forgetting to square the radius", "πr² means π × r × r."], ["Mixing up circumference and area", "Circumference is a length; area is in square units."]],
          [("What is π?", "The number of times the diameter fits round the circumference, about 3.14."), ("What is a semicircle?", "Half a circle."), ("What is a chord?", "A straight line joining two points on a circle.")]),

        U("volume", "M", "Find the volume of cubes and cuboids; find a missing length; convert between cm³, m³ and litres; solve problems on tanks and containers.",
          "Volume of Cubes and Cuboids", "Volume",
          "Free Primary 6 maths worksheets on volume: cubes and cuboids, missing lengths, litres and cubic centimetres, and water tank problems. 100 questions with answers.",
          "V = l × b × h", "1,000 cm³ = 1 litre",
          [("Volume of cuboids", [rs(av, "set_vol", 20)]), ("Use the formula", [rs(usv, "set_formula", 20)]), ("Missing lengths", [rs(sgv, "set_missing", 20)]),
           ("Volume and capacity", [rs(sgv, "set_review", 20)]), ("Tanks", [rs(sgv, "set_tanks", 20)])],
          ul(["Volume of a cuboid = length × breadth × height. Volume of a cube = side³.", "If you know the volume and two lengths, divide to find the third: h = V ÷ (l × b).",
              "1 cm³ holds 1 ml, so 1,000 cm³ = 1 litre and 1 m³ = 1,000 litres."]),
          [ex("Tank 2 m × 1.5 m × 1 m", ["V = 3 m³"], "3,000 litres")],
          [["Adding the sides", "Multiply the three lengths."], ["Mixing cm and m", "Use one unit for all lengths."], ["Writing m² for volume", "Volume is in cubic units."]],
          [("What is the volume of a cube with 10 cm sides?", "1,000 cm³, which is 1 litre."), ("How many litres does 1 m³ hold?", "1,000 litres."), ("What is capacity?", "How much a container holds.")]),

        U("speed-distance-and-time", "M", "Calculate speed, distance and time; find the duration of journeys; use the 24-hour clock in timetables.",
          "Speed, Distance and Time", "Speed, Distance and Time",
          "Free Primary 6 maths worksheets on speed, distance and time: average speed in km/h, distance travelled, time taken, journey times and the 24-hour clock. 100 questions with answers.",
          "Speed = distance ÷ time", "Distance = speed × time, time = distance ÷ speed.",
          [("Speed, distance and time", [co(A.speed, 20)]), ("More speed problems", [co(A.speed, 20)]), ("Journey times", [co(A.t_dur, 20)]),
           ("When will it arrive?", [co(A.t_end, 20)]), ("24-hour clock", [co(A.t_24, 20)])],
          ul(["Average speed = total distance ÷ total time. It is measured in km/h (kilometres per hour).", "Distance = speed × time. Time = distance ÷ speed.",
              "Change minutes to hours before you use the formula: 30 minutes = ½ hour."]),
          [ex("150 km in 2½ hours", ["150 ÷ 2.5"], "60 km/h"), ex("At 80 km/h for 3 hours", ["80 × 3"], "240 km")],
          [["Using 30 minutes as 0.3 hours", "30 minutes = 0.5 hours."], ["Multiplying instead of dividing", "Speed = distance ÷ time."], ["Mixing km and m", "Use km with km/h."]],
          [("What is average speed?", "The steady speed that would cover the same distance in the same time."), ("What does km/h mean?", "Kilometres travelled in one hour."), ("Is a faster car's time shorter?", "Yes, for the same distance.")]),

        U("angles", "G", "Find angles on a straight line, at a point and vertically opposite angles; use the angle sum of triangles and quadrilaterals; find angles in polygons and with parallel lines.",
          "Angles: Lines, Triangles and Polygons", "Angles",
          "Free Primary 6 maths worksheets on angles: angles on a line and at a point, vertically opposite angles, angles in triangles, quadrilaterals and polygons, and parallel lines. 100 questions with answers.",
          "Line 180°, point 360°, triangle 180°", "Quadrilateral 360°",
          [("Angles on a line and at a point", [rs(an, "set_line_point", 20)]), ("Vertically opposite angles", [rs(an, "set_vertical", 20)]), ("Angles in triangles", [rs(an, "set_triangles", 20)]),
           ("Angles in polygons", [rs(an, "set_polygons", 20)]), ("Isosceles triangles and parallel lines", [rs(sgan, "set_iso", 10), rs(sgan, "set_para", 10)])],
          ul(["Angles on a straight line add up to 180°. Angles at a point add up to 360°. Vertically opposite angles are equal.", "The angles in a triangle add up to 180°; in a quadrilateral, 360°.",
              "An isosceles triangle has two equal angles opposite its equal sides."]),
          [ex("Isosceles triangle with top angle 40°", ["(180 − 40) ÷ 2"], "70° each"), ex("Quadrilateral with 90°, 85°, 110°", ["360 − 285"], "75°")],
          [["Using 360° for a triangle", "A triangle is 180°."], ["Adding vertically opposite angles to 180°", "Vertically opposite angles are equal."], ["Finding the wrong equal angles in an isosceles triangle", "The equal angles are at the ends of the base."]],
          [("What is the sum of the angles of a pentagon?", "540°."), ("What is a regular polygon?", "One with all sides and all angles equal."), ("What are parallel lines?", "Lines that never meet.")]),

        U("plane-shapes-and-solids", "G", "Identify properties of plane shapes and solids; name solids from their nets; find the surface area of cubes and cuboids.",
          "Solid Shapes, Nets and Surface Area", "Solids and Nets",
          "Free Primary 6 maths worksheets on solid shapes: cubes, cuboids, prisms, pyramids, cylinders, cones and spheres, nets and the surface area of cuboids. 100 questions with answers.",
          "A net unfolds a solid", "Surface area = total area of all faces.",
          [("Name the solid", [rs(ussa, "set_identify", 14), co(A4.dim23, 6)]), ("Faces of solids", [rs(cn, "set_solids", 20)]), ("Nets", [rs(cn, "set_nets", 20)]),
           ("Faces and their areas", [rs(ussa, "set_faces", 20)]), ("Surface area of boxes", [rs(ussa, "set_boxes", 20)])],
          ul(["A prism has the same cross-section all along; a pyramid comes to a point.", "A net is a flat pattern that folds into a solid.",
              "The surface area of a cuboid is the total area of its 6 faces: 2(lb + bh + lh)."]),
          [ex("Cube with sides of 3 cm", ["6 faces × 9 cm²"], "54 cm²")],
          [["Counting only the faces you can see", "A cuboid always has 6 faces."], ["Confusing surface area and volume", "Surface area is in cm²; volume is in cm³."], ["Thinking a cone is a pyramid", "A cone has a circular base and a curved surface."]],
          [("How many faces does a triangular prism have?", "Five: 2 triangles and 3 rectangles."), ("What is the surface area used for?", "To find how much paper or paint is needed."), ("What solid is a tin of milk?", "A cylinder.")]),

        U("averages", "S", "Find the mean (average) of a set of data; find the total from the average; find a missing value; find how the average changes.",
          "Averages: Mean, Totals and Missing Values", "Averages",
          "Free Primary 6 maths worksheets on averages: finding the mean, the total from the mean, a missing value, and how the average changes when a value is added. 100 questions with answers.",
          "Mean = total ÷ number", "Total = mean × number",
          [("Find the average", [rs(sgav, "set_find", 20)]), ("Find the total", [rs(sgav, "set_total", 20)]), ("Missing values", [rs(sgav, "set_missing", 20)]),
           ("When the average changes", [rs(sgav, "set_change", 20)]), ("Word problems", [rs(sgav, "set_words", 14), co(A.mean_word, 6)])],
          ul(["Average (mean) = total of all values ÷ number of values.", "If you know the average, the total = average × number of values.",
              "To find a missing value, subtract the known values from the total."]),
          [ex("Average of 4 numbers is 15; three are 12, 18, 10", ["Total = 60", "60 − 40"], "20")],
          [["Dividing by the wrong number", "Count every value, including zeros."], ["Forgetting to find the total", "Most average problems start with the total."], ["Thinking the average must be one of the values", "It need not be."]],
          [("What is another name for average?", "The mean."), ("Can the average be a decimal?", "Yes."), ("When is the average used?", "For test scores, rainfall and temperatures.")]),

        U("data-presentation", "S", "Read and interpret pie charts and line graphs; find angles and amounts in pie charts; solve problems from charts.",
          "Pie Charts and Line Graphs", "Pie Charts and Line Graphs",
          "Free Primary 6 maths worksheets on data presentation: pie charts as fractions and angles, amounts from a pie chart, reading line graphs and solving problems. 100 questions with answers.",
          "The whole pie is 360°", "Angle ÷ 360° = fraction of the whole.",
          [("Pie charts and fractions", [rs(pl, "set_fractions", 16), rs(pl, "set_problems", 4)]), ("Amounts from a pie chart", [rs(pl, "set_amounts", 20)]), ("Angles in pie charts", [rs(pl, "set_angles", 20)]),
           ("Line graphs", [rs(pl, "set_line", 14), rs(lg5, "set_read", 6)]), ("Problems", [rs(pl, "set_problems", 14), rs(lg5, "set_words", 6)])],
          ul(["A pie chart shows how a whole is split into parts. The whole circle is 360°.", "Fraction of the whole = angle ÷ 360°. Amount = fraction × total.",
              "A line graph shows change over time. Read the scale on each axis carefully."]),
          [ex("A sector of 90° in a pie chart of 120 pupils", ["90 ÷ 360 = 1/4"], "30 pupils")],
          [["Using 100 instead of 360", "A full turn is 360°."], ["Not using the total", "Amount = fraction × total."], ["Reading between grid lines wrongly", "Find the value of each small square first."]],
          [("Which chart shows parts of a whole?", "A pie chart."), ("How many degrees for half the data?", "180°."), ("Which graph shows change over time?", "A line graph.")]),

        U("probability", "S", "Describe the chance of events using words and numbers from 0 to 1; find the probability of simple events.",
          "Probability: Chance from 0 to 1", "Probability",
          "Free Primary 6 maths worksheets on probability: impossible, unlikely, even chance, likely and certain, probabilities as fractions and simple events with dice, coins and bags. 100 questions with answers.",
          "P = favourable outcomes ÷ all outcomes", "Probabilities go from 0 to 1.",
          [("How likely?", [rs(auc, "set_everyday", 12), co(A4.chance_word, 8)]), ("Spinners and bags", [rs(auc, "set_spinners", 10), rs(auc, "set_bags", 10)]), ("Probability as a fraction", [cx(pr.one_single, 20)]),
           ("Not happening", [cx(pr.one_not, 20)]), ("Probability scale", [cx(pr.one_scale, 20)])],
          ul(["Probability tells us how likely something is. Impossible = 0, certain = 1, even chance = 1/2.", "Probability of an event = number of favourable outcomes ÷ total number of outcomes.",
              "The probability that something does not happen = 1 − the probability that it happens."]),
          [ex("A die shows an even number", ["2, 4, 6 out of 6"], "3/6 = 1/2")],
          [["Giving a probability bigger than 1", "Probabilities are between 0 and 1."], ["Counting outcomes twice", "List the outcomes carefully."], ["Thinking unlikely means impossible", "Unlikely events can still happen."]],
          [("What is the probability of a coin landing heads?", "1/2."), ("Can a probability be 0?", "Yes, if the event is impossible."), ("What is an outcome?", "One possible result.")]),

        U("quantitative-reasoning", "A", "Find rules in number patterns and sequences; find missing numbers in number puzzles; identify the odd one out (quantitative reasoning).",
          "Quantitative Reasoning: Patterns and Missing Numbers", "Quantitative Reasoning",
          "Free Primary 6 maths worksheets on quantitative reasoning for the Common Entrance: number patterns, input–output rules, box puzzles, sequences and the odd one out. 100 questions with answers.",
          "Find the rule, then use it", "Check the rule on every pair.",
          [("Number patterns", [co(A.qr_series, 20)]), ("Input and output", [co(A.qr_rule, 20)]), ("Box puzzles", [co(A.qr_box, 20)]),
           ("Odd one out", [co(A.qr_odd, 20)]), ("Sequences", [rs(alg, "set_sequences", 20)])],
          ul(["Look at how each number changes: add, subtract, multiply, divide or square.", "When a number goes into a rule and comes out changed, find a rule that works for every pair.",
              "Always check your rule on all the examples before you choose the answer."]),
          [ex("3 → 10, 5 → 16, 7 → 22, 9 → ?", ["Rule: × 3 + 1"], "28"), ex("2, 6, 18, 54, ?", ["× 3 each time"], "162")],
          [["Checking only one pair", "A rule must work for all pairs."], ["Looking only at the last two numbers", "Look at the whole pattern."], ["Missing square numbers", "1, 4, 9, 16 are squares."]],
          [("What is quantitative reasoning?", "Thinking about numbers to find patterns and rules."), ("Is it in the Common Entrance?", "Yes, it is a part of many entrance examinations."), ("How can I get better?", "Practise finding rules and check every step.")]),
    ]


if __name__ == "__main__":
    main("primary-6", "Primary 6", units, 150600)
