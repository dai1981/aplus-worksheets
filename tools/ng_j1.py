# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / JSS 1 (NERDC Upper Basic Education Curriculum; first, second and third term order of the scheme of work).
  python3 tools/ng_j1.py [number …]      seed = 160100 + number, reused modules 1619NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex
import ng_p4a as A4
import ng_p5a as A
import ng_ja as J


def units():
    pv = mod("gen_uk_maths_y7_place_value_and_ordering", 161901)
    fm = mod("gen_uk_maths_y7_factors_multiples_and_primes", 161902)
    asf = mod("gen_uk_maths_y7_adding_and_subtracting_fractions", 161903)
    mdf = mod("gen_uk_maths_y7_multiplying_and_dividing_fractions", 161904)
    fdp = mod("gen_uk_maths_y7_fractions_decimals_and_percentages", 161905)
    pc = mod("gen_uk_maths_y7_percentages_of_amounts", 161906)
    ro = mod("gen_uk_maths_y7_rounding_and_estimation", 161907)
    ng = mod("gen_uk_maths_y7_negative_numbers", 161908)
    oo = mod("gen_uk_maths_y7_order_of_operations", 161909)
    an = mod("gen_uk_maths_y7_algebraic_notation_and_substitution", 161910)
    se = mod("gen_uk_maths_y7_simplifying_expressions", 161911)
    eq = mod("gen_uk_maths_y7_solving_equations", 161912)
    sgeq = mod("gen_sg_maths_s1_linear_equations", 161913)
    pa = mod("gen_uk_maths_y7_perimeter_and_area", 161914)
    vo = mod("gen_uk_maths_y8_volume_and_surface_area_of_prisms", 161915)
    ang = mod("gen_uk_maths_y7_angles", 161916)
    sgang = mod("gen_sg_maths_s1_angles_triangles_and_quadrilaterals", 161917)
    cn = mod("gen_uk_maths_y6_circles_nets", 161918)
    cf = mod("gen_us_math_g5_classify_figures", 161919)
    fr8 = mod("gen_uk_maths_y8_frequency_tables_and_charts", 161920)
    pl = mod("gen_uk_maths_y6_pie_line", 161921)
    av = mod("gen_uk_maths_y7_averages_and_range", 161922)
    sgav = mod("gen_sg_maths_s2_mean_median_and_mode", 161923)
    usv = mod("gen_us_math_g6_volume", 161924)
    sgdp = mod("gen_sg_maths_s1_approximation_and_estimation", 161925)
    sgf = mod("gen_sg_maths_s1_primes_hcf_and_lcm", 161926)
    sgi = mod("gen_sg_maths_s1_integers_and_the_number_line", 161927)
    sgv6 = mod("gen_sg_maths_p6_volume", 161928)

    return [
        U("whole-numbers-and-place-value", "N", "Count, read and write whole numbers up to trillions; give the place value of digits; compare and order numbers; use large numbers in everyday life.",
          "Whole Numbers: Place Value, Ordering and Large Numbers", "Whole Numbers and Place Value",
          "Free JSS 1 maths worksheets on whole numbers: place value up to billions, the value of a digit, ×10 and ÷10, ordering numbers and inequality signs. 100 questions with answers.",
          "Value = digit × place value", "Million = 10⁶, billion = 10⁹",
          [("Value of a digit", [cx(pv.one_digit, 20)]), ("Multiplying and dividing by 10, 100, 1,000", [cx(pv.one_scale, 20)]), ("Ordering numbers", [cx(pv.one_order, 10), cx(pv.one_order_list, 10)]),
           ("Inequality signs", [cx(pv.one_ineq, 4), co(A4.cmp_true, 16)]), ("Large numbers", [co(A4.wn_more, 10), co(A4.ord_digits, 10)])],
          ul(["Each place is ten times the place to its right: units, tens, hundreds, thousands, …, millions, billions.", "The value of a digit is the digit × its place value.",
              "Multiplying by 10 moves every digit one place to the left; dividing by 10 moves every digit one place to the right."]),
          [ex("Value of 6 in 3,462,018", ["6 is in the ten thousands place"], "60,000"), ex("4.7 × 1,000", ["Digits move 3 places left"], "4,700")],
          [["Adding a zero to multiply decimals by 10", "4.7 × 10 = 47, not 4.70."], ["Comparing from the right", "Compare from the highest place."], ["Confusing million and billion", "1 billion = 1,000 million."]],
          [("How many zeros in one billion?", "Nine."), ("What does > mean?", "Is greater than."), ("Where do we see large numbers?", "Population figures, budgets and distances.")]),

        U("lcm-and-hcf", "N", "Find factors, multiples and prime factors of whole numbers; write numbers as products of prime factors; find the LCM and HCF; solve problems.",
          "Factors, Prime Factors, LCM and HCF", "LCM and HCF",
          "Free JSS 1 maths worksheets on factors and multiples, prime factorisation, the highest common factor (HCF) and lowest common multiple (LCM), and word problems. 100 questions with answers.",
          "Prime factors give the HCF and LCM", "HCF: shared primes. LCM: all primes, highest powers.",
          [("Factors, multiples and primes", [cx(fm.one_fmp, 20)]), ("Prime factorisation", [cx(fm.one_pf, 20)]), ("HCF", [cx(fm.one_hcf, 10), cx(sgf.one_hcf, 10)]),
           ("LCM", [cx(fm.one_lcm, 10), cx(sgf.one_lcm, 10)]), ("Using prime factors", [cx(fm.one_pf_use, 10), co(A4.lcm_word, 5), co(A4.hcf_word, 5)])],
          ul(["Write a number as a product of prime factors using a factor tree: 72 = 2³ × 3².", "HCF: multiply the prime factors common to all the numbers, using the lowest power.",
              "LCM: multiply every prime factor that appears, using the highest power."]),
          [ex("HCF and LCM of 36 and 60", ["36 = 2² × 3², 60 = 2² × 3 × 5"], "HCF = 12, LCM = 180")],
          [["Including 1 as a prime", "1 is not a prime number."], ["Multiplying all factors for the HCF", "Only the shared ones."], ["Using the lowest power for the LCM", "Use the highest power."]],
          [("What is a prime number?", "A number with exactly two factors, 1 and itself."), ("What is the HCF of two primes?", "1."), ("When is LCM useful?", "For things that repeat, such as bells or buses.")]),

        U("fractions", "O", "Add, subtract, multiply and divide fractions and mixed numbers; find a fraction of a quantity; use BODMAS with fractions.",
          "Fractions: The Four Operations", "Fractions",
          "Free JSS 1 maths worksheets on fractions: adding and subtracting fractions and mixed numbers, multiplying and dividing fractions, reciprocals and fraction of a quantity. 100 questions with answers.",
          "Same denominator to add; reciprocal to divide", "Change mixed numbers to improper fractions.",
          [("Add and subtract", [cx(asf.one_related, 10), cx(asf.one_any, 10)]), ("Mixed numbers", [cx(asf.one_mixed, 10), cx(mdf.one_mul_mixed, 10)]), ("Multiply", [cx(mdf.one_mul, 20)]),
           ("Divide and reciprocals", [cx(mdf.one_recip, 6), cx(mdf.one_div, 14)]), ("Fraction of a quantity", [cx(mdf.one_of, 20)])],
          ul(["To add or subtract, use the LCM of the denominators.", "To multiply, multiply the numerators and the denominators; cancel first if you can.", "To divide, multiply by the reciprocal of the divisor."]),
          [ex("2 1/2 × 1 3/5", ["5/2 × 8/5 = 40/10"], "4"), ex("3/4 ÷ 9/10", ["3/4 × 10/9"], "5/6")],
          [["Adding denominators", "1/3 + 1/4 = 7/12."], ["Turning the wrong fraction upside down", "Only the divisor."], ["Not simplifying", "Always give the lowest terms."]],
          [("What is a reciprocal?", "The fraction turned upside down; 4 has reciprocal 1/4."), ("What is an improper fraction?", "One whose numerator is at least its denominator."), ("Does BODMAS apply to fractions?", "Yes, in the same order.")]),

        U("decimals-and-percentages", "N", "Convert between fractions, decimals and percentages; order fractions, decimals and percentages; find percentages of quantities.",
          "Fractions, Decimals and Percentages", "Decimals and Percentages",
          "Free JSS 1 maths worksheets on converting fractions, decimals and percentages, ordering them, and finding percentages of amounts. 100 questions with answers.",
          "Percent means per hundred", "Fraction → decimal: divide top by bottom.",
          [("Fractions to decimals", [cx(fdp.one_f2d, 20)]), ("Decimals to fractions", [cx(fdp.one_d2f, 20)]), ("Percentages", [cx(fdp.one_2p, 10), cx(fdp.one_equiv, 10)]),
           ("Order them", [cx(fdp.one_order, 4), cx(fdp.one_equiv, 6), co(A.pct_what, 10)]), ("Percentages of amounts", [cx(pc.one_mental, 10), cx(pc.one_as_pct, 10)])],
          ul(["To change a fraction to a decimal, divide the numerator by the denominator: 3/8 = 0.375.", "To change a decimal to a percentage, multiply by 100: 0.375 = 37.5%.",
              "To compare, change them all to decimals or all to percentages."]),
          [ex("Order 0.6, 5/8, 58%", ["0.6, 0.625, 0.58"], "58%, 0.6, 5/8")],
          [["Writing 0.6 as 6%", "0.6 = 60%."], ["Dividing the wrong way", "3/8 means 3 ÷ 8."], ["Comparing digits, not values", "0.58 &lt; 0.6."]],
          [("What is 1/3 as a decimal?", "0.333… (a recurring decimal)."), ("What is 12.5% as a fraction?", "1/8."), ("Why use percentages?", "To compare amounts out of different totals.")]),

        U("estimation-and-approximation", "N", "Round numbers to the nearest whole number, ten, hundred and thousand; approximate to decimal places and significant figures; estimate answers.",
          "Estimation and Approximation: Decimal Places and Significant Figures", "Estimation and Approximation",
          "Free JSS 1 maths worksheets on rounding, decimal places, significant figures and estimating calculations. 100 questions with answers.",
          "Look at the next digit: 5 or more, round up", "Significant figures start at the first non-zero digit.",
          [("Decimal places", [cx(ro.one_dp, 20)]), ("Zeros in decimal places", [cx(ro.one_dp_zero, 10), cx(sgdp.one_dp, 10)]), ("Significant figures", [cx(ro.one_sf, 20)]),
           ("Estimate", [cx(ro.one_est, 20)]), ("Mixed rounding", [cx(ro.one_mixed, 20)])],
          ul(["To round to 2 decimal places, look at the third decimal digit.", "Significant figures are counted from the first non-zero digit: 0.004 72 to 2 s.f. is 0.0047.",
              "To estimate, round each number to 1 significant figure and work it out."]),
          [ex("3.8462 to 2 d.p.", ["Next digit 6"], "3.85"), ex("48,617 to 2 s.f.", ["Next digit 6"], "49,000")],
          [["Dropping zeros that hold place", "48,617 to 2 s.f. is 49,000, not 49."], ["Counting leading zeros as significant", "In 0.0047 the zeros are not significant."], ["Rounding twice", "Look only at the next digit."]],
          [("Why approximate?", "To make numbers simpler and to check answers."), ("What is 2.95 to 1 d.p.?", "3.0."), ("Is 0 ever significant?", "Yes, between or after non-zero digits in a measured value.")]),

        U("number-bases", "N", "Convert numbers from base ten to other bases and from other bases to base ten; add, subtract and multiply binary numbers.",
          "Number Bases: Binary and Other Bases", "Number Bases",
          "Free JSS 1 maths worksheets on number bases: converting between base ten and bases two to eight, and adding, subtracting and multiplying binary numbers. 100 questions with answers.",
          "Place values in base b: 1, b, b², b³", "Binary: 1 + 1 = 10₂",
          [("To base ten", [co(A.bin_to, 10), co(A.base_to, 10)]), ("From base ten", [co(A.bin_from, 10), co(A.base_from, 10)]), ("Binary addition", [co(A.bin_add, 20)]),
           ("Binary subtraction", [co(A.bin_sub, 20)]), ("Binary multiplication", [co(J.bin_mul, 20)])],
          ul(["In base two the place values are 1, 2, 4, 8, 16, 32, … In base five they are 1, 5, 25, 125, …", "To change to base ten, multiply each digit by its place value and add.",
              "To change from base ten, divide by the base repeatedly and read the remainders upwards. In binary, 1 + 1 = 10₂ and 1 + 1 + 1 = 11₂."]),
          [ex("1011₂ + 111₂", ["11 + 7 = 18"], "10010₂"), ex("101₂ × 11₂", ["5 × 3 = 15"], "1111₂")],
          [["Carrying 10 in binary", "Carry when you reach 2."], ["Reading remainders downwards", "Read from the bottom up."], ["Using digits as big as the base", "Base five has no digit 5."]],
          [("Why do computers use binary?", "Circuits are either on (1) or off (0)."), ("What is 10₂?", "2."), ("What is 100₅?", "25.")]),

        U("directed-numbers", "O", "Use directed numbers on a number line; add and subtract positive and negative numbers; solve problems with temperature and money.",
          "Directed Numbers: Adding and Subtracting Integers", "Directed Numbers",
          "Free JSS 1 maths worksheets on directed numbers: the number line, adding and subtracting positive and negative numbers, and problems with temperature and height. 100 questions with answers.",
          "Subtracting a negative = adding", "−3 + 5 = 2",
          [("Add integers", [cx(ng.one_add, 10), cx(sgi.one_add, 10)]), ("Subtract a positive", [cx(ng.one_sub_pos, 20)]), ("Subtract a negative", [cx(ng.one_sub_neg, 20)]),
           ("Ordering directed numbers", [cx(pv.one_neg_order, 20)]), ("Mixed", [cx(ng.one_mixed, 20)])],
          ul(["Numbers to the right on the number line are bigger: −2 &gt; −7.", "Adding a positive number moves right; adding a negative number moves left.",
              "Subtracting a negative number is the same as adding: 4 − (−3) = 4 + 3 = 7."]),
          [ex("−8 + 3", ["Start at −8, move 3 right"], "−5"), ex("−2 − (−6)", ["−2 + 6"], "4")],
          [["Thinking −7 &gt; −2", "−7 is further left, so it is smaller."], ["Subtracting a negative as subtracting", "Two minus signs together make plus."], ["Losing the sign", "Write the sign in the answer."]],
          [("What are directed numbers?", "Numbers with a sign, + or −, that show a direction."), ("Where do we see negative numbers?", "Temperatures below zero, debts and depths below sea level."), ("What is −5 + 5?", "0.")]),

        U("order-of-operations", "O", "Use BODMAS to simplify expressions with brackets, powers, division, multiplication, addition and subtraction.",
          "Order of Operations (BODMAS)", "BODMAS",
          "Free JSS 1 maths worksheets on BODMAS: multiplication and division before addition and subtraction, brackets, powers, negative numbers and placing brackets. 100 questions with answers.",
          "B O D M A S", "Same rank: work left to right.",
          [("× and ÷ first", [cx(oo.one_md, 20)]), ("Brackets", [cx(oo.one_br, 20)]), ("Powers", [cx(oo.one_pow, 20)]),
           ("With negative numbers", [cx(oo.one_neg, 20)]), ("Where do the brackets go?", [cx(oo.one_place, 20)])],
          ul(["Brackets first, then Of (powers), then Division and Multiplication from left to right, then Addition and Subtraction from left to right.",
              "−3² means −(3²) = −9, but (−3)² = 9."]),
          [ex("20 − 3 × 2²", ["2² = 4", "3 × 4 = 12", "20 − 12"], "8")],
          [["Working left to right only", "× and ÷ come before + and −."], ["Squaring before the brackets", "Brackets come first."], ["Doing + before −", "+ and − have equal rank: left to right."]],
          [("What does the O stand for?", "Of, meaning powers (orders)."), ("Is 12 ÷ 4 × 3 = 1?", "No. Left to right: 3 × 3 = 9."), ("Why have rules?", "So everyone gets the same answer.")]),

        U("algebraic-expressions", "A", "Use letters for numbers; write word problems in symbolic terms; simplify expressions by collecting like terms; substitute values.",
          "Algebraic Expressions: Writing, Simplifying and Substituting", "Algebraic Expressions",
          "Free JSS 1 maths worksheets on algebra: writing expressions from words, notation, collecting like terms, multiplying terms, expanding brackets and substitution. 100 questions with answers.",
          "3a means 3 × a", "Only like terms can be added.",
          [("Notation", [cx(an.one_notation, 20)]), ("Words to symbols", [cx(an.one_words, 10), cx(an.one_context, 10)]), ("Collect like terms", [cx(se.one_like1, 10), cx(se.one_like2, 10)]),
           ("Multiply and expand", [cx(se.one_muldiv, 10), cx(se.one_expand, 10)]), ("Substitution", [cx(an.one_sub, 10), cx(an.one_sub_neg, 10)])],
          ul(["In algebra a letter stands for an unknown number. 5n means 5 × n; n² means n × n.", "Like terms have the same letters: 3x + 5x = 8x, but 3x + 5y stays as it is.",
              "To substitute, replace each letter with its value and use BODMAS."]),
          [ex("Simplify 4a + 3b − a + 2b", ["4a − a = 3a, 3b + 2b = 5b"], "3a + 5b"), ex("If x = 3, find 2x² − 1", ["2 × 9 − 1"], "17")],
          [["Adding unlike terms", "2a + 3b cannot be simplified."], ["Writing 2x² as (2x)²", "2x² = 2 × x²."], ["Forgetting the sign in front of a term", "The sign belongs to the term after it."]],
          [("What is a coefficient?", "The number in front of a letter, like 7 in 7y."), ("What is an expression?", "Terms joined by + or −, with no equals sign."), ("Is ab the same as ba?", "Yes.")]),

        U("simple-equations", "A", "Solve simple linear equations by balancing; form equations from word problems and solve them.",
          "Simple Equations", "Simple Equations",
          "Free JSS 1 maths worksheets on simple linear equations: one-step and two-step equations, equations with brackets, and forming and solving equations from word problems. 100 questions with answers.",
          "Keep the balance", "Do the same to both sides.",
          [("Solve the equation", [cx(eq.one_step, 20)]), ("More equations", [cx(sgeq.one_step, 20)]), ("Number puzzles", [co(J.eq_word, 20)]),
           ("Word problems", [co(A4.os_write, 10), co(J.eq_word, 10)]), ("Check the answer", [co(A4.os_true, 10), co(A4.os_solve, 10)])],
          ul(["An equation is like a balance: whatever you do to one side, do to the other.", "Undo the operations in reverse order: 3x − 5 = 16 → 3x = 21 → x = 7.",
              "For a word problem, let the unknown be x, write an equation and solve it. Check the answer in the story."]),
          [ex("5x + 4 = 29", ["5x = 25"], "x = 5"), ex("2(x − 3) = 14", ["x − 3 = 7"], "x = 10")],
          [["Doing different things to the two sides", "Keep the balance."], ["Undoing in the wrong order", "Undo + and − before × and ÷."], ["Not checking", "Put the answer back in the equation."]],
          [("What is the solution of an equation?", "The value of the letter that makes it true."), ("Can x be negative?", "Yes."), ("What is a linear equation?", "One where the letter has power 1.")]),

        U("perimeter-and-area", "G", "Find the perimeter and area of rectangles, squares, triangles, parallelograms and composite shapes.",
          "Perimeter and Area of Plane Shapes", "Perimeter and Area",
          "Free JSS 1 maths worksheets on perimeter and area: rectangles, triangles, parallelograms and composite shapes, with missing lengths. 100 questions with answers.",
          "Triangle = ½ × base × height", "Parallelogram = base × height",
          [("Rectangles and triangles", [cx(pa.one_rt, 20)]), ("Parallelograms and trapeziums", [cx(pa.one_pt, 20)]), ("Perimeter", [cx(pa.one_per, 20)]),
           ("Composite shapes", [cx(pa.one_comp, 20)]), ("Problems", [co(A.circ_word, 10), cx(pa.one_rt, 10)])],
          ul(["Perimeter is the total length of the boundary. Area is the space inside, in square units.", "Rectangle: l × b. Triangle: ½ × b × h. Parallelogram: b × h. Trapezium: ½(a + b)h.",
              "Circle: circumference = 2πr, area = πr² (use π = 22/7 or 3.14)."]),
          [ex("Trapezium with parallel sides 8 cm and 12 cm, height 5 cm", ["½ × 20 × 5"], "50 cm²")],
          [["Using a slant side as the height", "The height is perpendicular to the base."], ["Mixing units", "Change to one unit first."], ["Giving area in cm", "Area is in cm²."]],
          [("What is 1 m² in cm²?", "10,000 cm²."), ("Why is a triangle ½ × b × h?", "It is half of a parallelogram."), ("What is perimeter used for?", "Fencing, borders and frames.")]),

        U("volume-of-cubes-and-cuboids", "G", "Find the volume of cubes and cuboids; find a missing length; change between cm³, m³ and litres.",
          "Volume of Cubes and Cuboids", "Volume",
          "Free JSS 1 maths worksheets on volume: cubes and cuboids, the formula V = l × b × h, missing lengths, capacity in litres and tank problems. 100 questions with answers.",
          "V = l × b × h", "1,000 cm³ = 1 litre",
          [("Volume of cuboids", [cx(vo.one_cuboid, 20)]), ("Use the formula", [rs(usv, "set_formula", 20)]), ("Missing lengths", [rs(usv, "set_missing", 8), cx(vo.one_cuboid, 12)]),
           ("Volume and capacity", [co(A.sq_cube_word, 10), rs(usv, "set_base", 10)]), ("Problems", [rs(sgv6, "set_tanks", 10), rs(sgv6, "set_psle", 10)])],
          ul(["Volume of a cuboid = length × breadth × height. Volume of a cube = l³.", "Volume = area of base × height.", "1 cm³ = 1 ml, 1,000 cm³ = 1 litre, 1 m³ = 1,000 litres."]),
          [ex("Tank 2 m × 1.5 m × 1.2 m", ["3.6 m³"], "3,600 litres")],
          [["Adding the lengths", "Multiply them."], ["Mixed units", "Use one unit."], ["Writing cm² for volume", "Volume is in cm³."]],
          [("What is a cube?", "A cuboid with all edges equal."), ("How many litres in 1 m³?", "1,000."), ("What is capacity?", "How much a container holds.")]),

        U("angles", "G", "Identify types of angles; find angles on a straight line, at a point and vertically opposite angles; use the angle sum of triangles and quadrilaterals.",
          "Angles: Types, Lines and Triangles", "Angles",
          "Free JSS 1 maths worksheets on angles: angles on a straight line, angles at a point, vertically opposite angles, angles in triangles and quadrilaterals. 100 questions with answers.",
          "Line 180°, point 360°", "Triangle 180°, quadrilateral 360°",
          [("Angles on a straight line", [cx(ang.one_line, 20)]), ("Angles at a point", [cx(ang.one_point, 20)]), ("Vertically opposite angles", [cx(ang.one_vopp, 10), cx(ang.one_vopp2, 10)]),
           ("Angles in triangles", [cx(ang.one_tri, 10), cx(sgang.one_tri, 10)]), ("Angles in quadrilaterals", [cx(ang.one_quad, 10), cx(sgang.one_quad, 10)])],
          ul(["Acute &lt; 90°, right = 90°, obtuse between 90° and 180°, reflex between 180° and 360°.", "Angles on a straight line add up to 180°; angles at a point add up to 360°; vertically opposite angles are equal.",
              "Angles in a triangle add up to 180°; in a quadrilateral, 360°."]),
          [ex("Angles 3x and 2x on a straight line", ["5x = 180"], "x = 36°")],
          [["Using 360° for a straight line", "A straight line is 180°."], ["Adding vertically opposite angles", "They are equal."], ["Forgetting the right-angle mark", "A square corner is 90°."]],
          [("What are complementary angles?", "Two angles that add up to 90°."), ("What are supplementary angles?", "Two angles that add up to 180°."), ("What is a reflex angle?", "One between 180° and 360°.")]),

        U("plane-and-solid-shapes", "G", "Identify the properties of plane shapes (triangles and quadrilaterals) and of solids (cubes, cuboids, prisms, pyramids, cylinders, cones and spheres); draw and recognise nets.",
          "Plane Shapes and Solid Shapes", "Plane and Solid Shapes",
          "Free JSS 1 maths worksheets on plane shapes and solids: properties of triangles and quadrilaterals, faces, edges and vertices of solids, and nets. 100 questions with answers.",
          "Plane shapes are flat; solids have 3 dimensions", "Faces, edges, vertices",
          [("Triangles", [rs(cf, "set_triangles", 20)]), ("Quadrilaterals", [rs(cf, "set_quads", 10), rs(cf, "set_hierarchy", 10)]), ("Solids", [rs(cn, "set_solids", 20)]),
           ("Faces, edges and vertices", [co(A4.fev, 20)]), ("Nets", [rs(cn, "set_nets", 20)])],
          ul(["A parallelogram has opposite sides equal and parallel; a rhombus has all four sides equal; a trapezium has one pair of parallel sides.",
              "A cuboid has 6 faces, 12 edges and 8 vertices. A triangular prism has 5 faces, 9 edges and 6 vertices.", "A net is a flat pattern that folds into a solid."]),
          [ex("Square-based pyramid", ["1 square + 4 triangles"], "5 faces, 8 edges, 5 vertices")],
          [["Thinking a square is not a rectangle", "A square is a special rectangle."], ["Counting the same edge twice", "Mark edges as you count."], ["Calling a cone a pyramid", "A cone has a circular base."]],
          [("What is a polygon?", "A closed plane shape with straight sides."), ("How many faces has a cylinder?", "Three: two flat and one curved."), ("What is a vertex?", "A corner.")]),

        U("data-presentation", "S", "Collect data and present it in frequency tables, bar charts and pie charts; read and interpret charts.",
          "Data Presentation: Frequency Tables and Pie Charts", "Data Presentation",
          "Free JSS 1 maths worksheets on data presentation: frequency tables, pie charts as fractions and angles, and reading charts. 100 questions with answers.",
          "Pie chart angle = frequency ÷ total × 360°", "The whole circle is 360°.",
          [("Pie charts", [cx(fr8.one_pie, 20)]), ("Pie charts and fractions", [rs(pl, "set_fractions", 16), rs(pl, "set_problems", 4)]), ("Angles in pie charts", [rs(pl, "set_angles", 20)]),
           ("Amounts from pie charts", [rs(pl, "set_amounts", 20)]), ("Frequency tables", [cx(fr8.one_mean, 10), cx(fr8.one_mmr, 10)])],
          ul(["A frequency table shows how many times each value occurs.", "In a pie chart, the angle for a group = frequency ÷ total × 360°.",
              "To read a pie chart, angle ÷ 360° gives the fraction of the total."]),
          [ex("15 out of 60 pupils walk to school", ["15 ÷ 60 × 360"], "90°")],
          [["Using 100 instead of 360", "A pie chart is a full circle."], ["Forgetting the total", "Divide by the total frequency."], ["Not checking the angles add to 360°", "They must."]],
          [("What is frequency?", "How often something happens."), ("Which chart shows parts of a whole?", "A pie chart."), ("What is raw data?", "Data before it is sorted.")]),

        U("averages", "S", "Find the mean, median, mode and range of data; find a missing value from the mean; compare data sets.",
          "Averages: Mean, Median, Mode and Range", "Averages",
          "Free JSS 1 maths worksheets on averages: mean, median, mode and range, a missing value and comparing two sets of data. 100 questions with answers.",
          "Mean = sum ÷ number", "Median: middle value when in order.",
          [("Mean", [cx(av.one_mean, 20)]), ("Median", [cx(av.one_median, 20)]), ("Mode and range", [cx(av.one_mode_range, 20)]),
           ("Missing values", [cx(av.one_missing, 20)]), ("Averages in real life", [co(A.mean_word, 10), co(A.mean_missing, 10)])],
          ul(["Mean: add the values and divide by how many there are.", "Median: put the values in order; it is the middle one (or halfway between the two middle ones).",
              "Mode: the most common value. Range: highest − lowest; it shows how spread out the data is."]),
          [ex("5, 8, 8, 10, 14", ["Sum 45, 5 values"], "mean 9, median 8, mode 8, range 9")],
          [["Not ordering for the median", "Order the values first."], ["Giving the frequency as the mode", "The mode is the value."], ["Thinking range is an average", "Range measures spread."]],
          [("Which average is best with an extreme value?", "The median."), ("Can there be no mode?", "Yes, if every value appears once."), ("What does a large range mean?", "The data are spread out.")]),
    ]


if __name__ == "__main__":
    main("jss-1", "JSS 1", units, 160100)
