# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / JSS 2 (NERDC Upper Basic Education Curriculum).
  python3 tools/ng_j2.py [number …]      seed = 160200 + number, reused modules 1629NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex
import ng_p4a as A4
import ng_p5a as A
import ng_ja as J


def units():
    sf = mod("gen_uk_maths_y8_standard_form", 162901)
    sgsf = mod("gen_sg_maths_s3_standard_form", 162902)
    ro9 = mod("gen_uk_maths_y9_rounding_and_error_intervals", 162903)
    ro7 = mod("gen_uk_maths_y7_rounding_and_estimation", 162904)
    pw = mod("gen_uk_maths_y7_powers_and_roots", 162905)
    ng = mod("gen_uk_maths_y7_negative_numbers", 162906)
    sgi = mod("gen_sg_maths_s1_integers_and_the_number_line", 162907)
    pcc = mod("gen_uk_maths_y8_percentage_change_and_interest", 162908)
    ra = mod("gen_uk_maths_y7_ratio_and_proportion", 162909)
    dip = mod("gen_uk_maths_y8_direct_and_inverse_proportion", 162910)
    se = mod("gen_uk_maths_y7_simplifying_expressions", 162911)
    ef = mod("gen_uk_maths_y8_expanding_and_factorising", 162912)
    eq = mod("gen_uk_maths_y8_equations_with_unknowns_on_both_sides", 162913)
    co7 = mod("gen_uk_maths_y7_coordinates_and_straight_line_graphs", 162914)
    lg = mod("gen_uk_maths_y8_linear_graphs", 162915)
    ap = mod("gen_uk_maths_y8_angles_in_parallel_lines_and_polygons", 162916)
    sgap = mod("gen_sg_maths_s1_parallel_lines_and_polygons", 162917)
    pa = mod("gen_uk_maths_y7_perimeter_and_area", 162918)
    ci = mod("gen_uk_maths_y8_circles", 162919)
    vo = mod("gen_uk_maths_y8_volume_and_surface_area_of_prisms", 162920)
    sgvo = mod("gen_sg_maths_s1_volume_and_surface_area_of_prisms_and_cylinders", 162921)
    py = mod("gen_uk_maths_y9_pythagoras_theorem", 162922)
    sgpy = mod("gen_sg_maths_s2_pythagoras_theorem", 162923)
    ft = mod("gen_uk_maths_y8_frequency_tables_and_charts", 162924)
    av = mod("gen_uk_maths_y7_averages_and_range", 162925)
    sgfq = mod("gen_sg_maths_s2_frequency_tables_and_grouped_data", 162926)
    pr7 = mod("gen_uk_maths_y7_probability", 162927)
    pr8 = mod("gen_uk_maths_y8_probability_of_combined_events", 162928)
    sgpr = mod("gen_sg_maths_s2_probability", 162929)

    return [
        U("number-bases", "N", "Convert numbers between base ten and other bases and from one base to another; add, subtract and multiply numbers in bases other than ten.",
          "Number Bases: Conversion and Operations", "Number Bases",
          "Free JSS 2 maths worksheets on number bases: converting between bases, adding, subtracting and multiplying in bases two to eight, and finding an unknown base. 100 questions with answers.",
          "Check every base sum in base ten", "In base b, carry or borrow b.",
          [("Change bases", [co(J.base_convert, 10), co(A.base_from, 10)]), ("Add in other bases", [co(J.base_add, 20)]), ("Subtract in other bases", [co(J.base_sub, 20)]),
           ("Multiply in other bases", [co(J.base_mul, 20)]), ("Find the base", [co(J.base_find, 20)])],
          ul(["In base b the place values are 1, b, b², b³, … and the digits go from 0 to b − 1.", "To change from one base to another, change to base ten first.",
              "To add in base b, carry 1 each time a column reaches b. To subtract, borrow b, not 10."]),
          [ex("243₅ + 134₅", ["3 + 4 = 7 = 12₅: write 2, carry 1", "4 + 3 + 1 = 8 = 13₅", "2 + 1 + 1 = 4"], "432₅"), ex("23 in base b = 17", ["2b + 3 = 17"], "b = 7")],
          [["Carrying 10", "Carry when a column reaches the base."], ["Using a digit equal to the base", "Base 6 has digits 0 to 5 only."], ["Converting directly between two bases", "Go through base ten."]],
          [("Which base uses digits 0 to 7?", "Base eight (octal)."), ("What is 10 in any base b?", "b."), ("How can I check?", "Change everything to base ten.")]),

        U("standard-form", "N", "Write large and small numbers in standard form (A × 10ⁿ); change numbers from standard form to ordinary form; order and calculate with numbers in standard form.",
          "Standard Form (Scientific Notation)", "Standard Form",
          "Free JSS 2 maths worksheets on standard form: writing large and small numbers as A × 10ⁿ, ordinary numbers, ordering and multiplying and dividing in standard form. 100 questions with answers.",
          "A × 10ⁿ with 1 ≤ A < 10", "Small numbers have negative powers.",
          [("Large numbers", [cx(sf.one_big, 20)]), ("Small numbers", [cx(sf.one_small, 20)]), ("Back to ordinary numbers", [cx(sf.one_back, 20)]),
           ("Mixed practice", [cx(sf.one_order, 2), cx(sgsf.one_order, 2), cx(sgsf.one_big, 8), cx(sgsf.one_small, 8)]), ("Multiply and divide", [cx(sf.one_md, 10), cx(sgsf.one_md, 10)])],
          ul(["A number in standard form is A × 10ⁿ where 1 ≤ A &lt; 10 and n is a whole number.", "Large numbers: count how many places the point moves left: 45,000 = 4.5 × 10⁴.",
              "Small numbers: the point moves right and the power is negative: 0.0032 = 3.2 × 10⁻³."]),
          [ex("Write 6,800,000", ["Point moves 6 places"], "6.8 × 10⁶"), ex("(3 × 10⁴) × (2 × 10³)", ["6 × 10⁷"], "6 × 10⁷")],
          [["Writing 45 × 10³", "A must be between 1 and 10: 4.5 × 10⁴."], ["Using a positive power for small numbers", "0.004 = 4 × 10⁻³."], ["Adding the A values when multiplying", "Multiply the A values and add the powers."]],
          [("Why use standard form?", "To write very big or very small numbers neatly."), ("What is 10⁰?", "1."), ("Where is standard form used?", "In science: the distance to the sun, the size of cells.")]),

        U("approximation-and-significant-figures", "N", "Round numbers to a given number of decimal places and significant figures; estimate answers to calculations.",
          "Approximation: Decimal Places and Significant Figures", "Approximation",
          "Free JSS 2 maths worksheets on approximation: significant figures of large and small numbers, decimal places and estimating calculations. 100 questions with answers.",
          "Count significant figures from the first non-zero digit", "Keep place-holding zeros.",
          [("Significant figures", [cx(ro7.one_sf, 20)]), ("Large numbers", [cx(ro9.one_sf_big, 20)]), ("Small numbers", [cx(ro9.one_small, 20)]),
           ("Decimal places", [cx(ro7.one_dp, 10), cx(ro7.one_dp_zero, 10)]), ("Estimate", [cx(ro7.one_est, 20)])],
          ul(["To round to n significant figures, start counting at the first non-zero digit.", "For large numbers keep zeros to hold the places: 386,500 to 2 s.f. is 390,000.",
              "Estimate by rounding each number to 1 significant figure."]),
          [ex("0.007 285 to 2 s.f.", ["First s.f. is 7"], "0.0073"), ex("Estimate 41.2 × 0.48", ["40 × 0.5"], "20")],
          [["Counting leading zeros", "0.0073 has 2 significant figures."], ["Dropping place-holding zeros", "390,000, not 39."], ["Rounding each step", "Round only at the end."]],
          [("How many s.f. in 3,050?", "3 (the last zero only holds a place)."), ("What is 9.96 to 1 d.p.?", "10.0."), ("When do we estimate?", "To check that an answer is sensible.")]),

        U("squares-and-square-roots", "N", "Find squares, cubes, square roots and cube roots of numbers; use prime factors to find square roots; estimate square roots.",
          "Squares, Square Roots, Cubes and Cube Roots", "Squares and Square Roots",
          "Free JSS 2 maths worksheets on squares and square roots, cubes and cube roots, index notation and square roots by prime factors. 100 questions with answers.",
          "√ is the inverse of squaring", "Pair the prime factors for √.",
          [("Squares and cubes", [cx(pw.one_sqcube, 20)]), ("Roots", [cx(pw.one_root, 20)]), ("Index notation", [cx(pw.one_index, 20)]),
           ("Square roots by factors", [co(A.sq_factor, 18), co(A.sq_big, 2)]), ("Mixed", [cx(pw.one_mix, 20)])],
          ul(["A square number is n²; a cube number is n³.", "The square root of 196 is 14 because 14² = 196. Every positive number has two square roots, +14 and −14.",
              "Use prime factors: 576 = 2⁶ × 3², so √576 = 2³ × 3 = 24."]),
          [ex("√1,296", ["2⁴ × 3⁴ → 2² × 3²"], "36")],
          [["Halving for a square root", "√64 = 8."], ["Writing 3³ = 9", "3³ = 27."], ["Forgetting the negative root", "x² = 25 gives x = 5 or x = −5."]],
          [("Is 0 a square number?", "Yes, 0² = 0."), ("What is ∛−8?", "−2."), ("Between which whole numbers is √50?", "7 and 8.")]),

        U("directed-numbers", "O", "Multiply and divide directed numbers; use the rules for signs; solve problems with directed numbers.",
          "Directed Numbers: Multiplication and Division", "Directed Numbers",
          "Free JSS 2 maths worksheets on directed numbers: multiplying and dividing positive and negative numbers, squares of negative numbers and mixed calculations. 100 questions with answers.",
          "Same signs: positive. Different signs: negative.", "(−3) × (−4) = 12",
          [("Multiply", [cx(ng.one_mul, 10), cx(sgi.one_mul, 10)]), ("Divide", [cx(ng.one_div, 10), cx(sgi.one_div, 10)]), ("Squares of negatives", [cx(ng.one_sq, 20)]),
           ("All four operations", [cx(ng.one_mixed, 10), cx(sgi.one_mixed, 10)]), ("Add and subtract", [cx(ng.one_add, 10), cx(ng.one_sub_neg, 10)])],
          ul(["When you multiply or divide two numbers with the same sign, the answer is positive.", "When the signs are different, the answer is negative.",
              "(−5)² = 25, but −5² = −25."]),
          [ex("(−6) × 4", ["Different signs"], "−24"), ex("(−36) ÷ (−9)", ["Same signs"], "4")],
          [["Thinking two negatives make a negative", "(−2) × (−3) = 6."], ["Mixing up −5² and (−5)²", "Brackets matter."], ["Using the × rule for +", "−3 + (−4) = −7."]],
          [("What is (−1) × (−1)?", "1."), ("What is 0 × (−7)?", "0."), ("What is (−2)³?", "−8.")]),

        U("percentages", "N", "Find percentage increase and decrease; use multipliers; find the original amount; solve problems on profit and loss per cent.",
          "Percentages: Increase, Decrease and Profit", "Percentages",
          "Free JSS 2 maths worksheets on percentages: multipliers, percentage increase and decrease, reverse percentages and profit and loss per cent in naira. 100 questions with answers.",
          "Increase by 15%: × 1.15", "Percentage change = change ÷ original × 100",
          [("Multipliers", [cx(pcc.one_mult, 20)]), ("Percentage change", [cx(pcc.one_change, 10), co(J.pct_change, 10)]), ("Original amount", [cx(pcc.one_reverse, 10), co(J.reverse_pct, 10)]),
           ("Profit and loss per cent", [co(A.profit_pct, 20)]), ("Percentages of amounts", [co(A.pct_of, 20)])],
          ul(["To increase by 15%, multiply by 1.15. To decrease by 15%, multiply by 0.85.", "Percentage change = change ÷ original amount × 100.",
              "To find the original amount, divide by the multiplier: after a 20% increase the price is ₦6,000, so the original price is ₦6,000 ÷ 1.2 = ₦5,000."]),
          [ex("₦12,000 decreased by 25%", ["× 0.75"], "₦9,000")],
          [["Dividing by the new amount", "Divide by the original."], ["Taking 20% off the new price to go back", "Divide by 1.2 instead."], ["Writing 5% as × 1.5", "5% increase is × 1.05."]],
          [("What is a multiplier?", "The number you multiply by to change an amount by a percentage."), ("Is a 10% rise then a 10% fall the same price?", "No: × 1.1 × 0.9 = × 0.99."), ("Where are percentages used?", "Prices, interest, results and population growth.")]),

        U("commercial-arithmetic", "O", "Solve problems on simple interest, discount, commission, VAT and hire purchase.",
          "Commercial Arithmetic: Interest, Discount, Commission and VAT", "Commercial Arithmetic",
          "Free JSS 2 maths worksheets on commercial arithmetic in naira: simple interest, discount, commission, VAT at 7.5% and hire purchase. 100 questions with answers.",
          "I = PRT ÷ 100", "VAT in Nigeria is 7.5%.",
          [("Simple interest", [co(A.si, 20)]), ("Discount", [co(A.discount, 20)]), ("Commission", [co(A.commission, 20)]),
           ("VAT", [co(A.vat, 20)]), ("Hire purchase", [co(A.hire, 20)])],
          ul(["Simple interest I = P × R × T ÷ 100. Amount = P + I.", "Discount and commission are percentages of a price or of sales.",
              "VAT (Value Added Tax) is 7.5% of the price. Hire purchase: deposit + instalments."]),
          [ex("Interest on ₦80,000 at 6% for 2 years", ["80,000 × 6 × 2 ÷ 100"], "₦9,600")],
          [["Using months as years", "Change months to years: 6 months = ½ year."], ["Forgetting the deposit", "Include it in the total."], ["Subtracting VAT", "VAT is added to the price."]],
          [("What is the principal?", "The money borrowed or invested."), ("What is commission?", "A payment based on the value of sales."), ("Who collects VAT?", "The government, through sellers.")]),

        U("ratio-and-proportion", "N", "Simplify ratios; share quantities in a given ratio; solve problems on direct and inverse proportion.",
          "Ratio, Direct and Inverse Proportion", "Ratio and Proportion",
          "Free JSS 2 maths worksheets on ratio and proportion: simplifying ratios, sharing in a ratio, direct proportion, inverse proportion and recipes. 100 questions with answers.",
          "Direct: both go up. Inverse: one up, one down.", "Find the value of one part.",
          [("Simplify ratios", [cx(ra.one_simplify, 20)]), ("Share in a ratio", [cx(ra.one_share, 10), co(A.ratio_share, 10)]), ("One part", [cx(ra.one_part, 10), cx(ra.one_frac, 10)]),
           ("Direct proportion", [cx(dip.one_direct, 10), co(A.proportion, 10)]), ("Inverse proportion", [cx(dip.one_inverse, 10), co(A.inverse_prop, 10)])],
          ul(["Simplify a ratio by dividing by the HCF.", "Direct proportion: y = kx. If x doubles, y doubles.", "Inverse proportion: y = k ÷ x. If x doubles, y halves."]),
          [ex("Share ₦45,000 in the ratio 2 : 3 : 4", ["9 parts, one part = ₦5,000"], "₦10,000, ₦15,000, ₦20,000")],
          [["Dividing by the number of people", "Divide by the total number of parts."], ["Using direct proportion for workers and time", "It is inverse."], ["Ratios with different units", "Change to the same unit."]],
          [("What is a rate?", "A ratio of two different quantities, such as km per hour."), ("What is the unitary method?", "Find the value for one, then multiply."), ("Is speed and time direct or inverse?", "Inverse, for a fixed distance.")]),

        U("expansion-and-factorisation", "A", "Expand algebraic expressions with brackets; expand the product of two binomials; factorise expressions by taking out common factors.",
          "Expansion and Factorisation of Algebraic Expressions", "Expansion and Factorisation",
          "Free JSS 2 maths worksheets on algebra: expanding single brackets, simplifying, expanding two brackets and factorising by common factors. 100 questions with answers.",
          "a(b + c) = ab + ac", "Factorising undoes expanding.",
          [("Expand one bracket", [cx(ef.one_single, 10), cx(se.one_expand, 10)]), ("Expand and simplify", [cx(ef.one_simplify, 10), cx(se.one_expand2, 10)]), ("Two brackets", [cx(ef.one_double, 20)]),
           ("Factorise", [cx(ef.one_factor, 10), cx(se.one_factorise, 10)]), ("Like terms", [cx(se.one_like2, 10), cx(se.one_muldiv, 10)])],
          ul(["Multiply every term inside the bracket by the term outside: 3(2x − 5) = 6x − 15.", "(x + 3)(x + 5) = x² + 5x + 3x + 15 = x² + 8x + 15.",
              "To factorise, take out the HCF of the terms: 6x + 9 = 3(2x + 3)."]),
          [ex("Expand 4(3a − 2) − 2(a + 1)", ["12a − 8 − 2a − 2"], "10a − 10"), ex("Factorise 8y² − 12y", ["HCF is 4y"], "4y(2y − 3)")],
          [["Multiplying only the first term", "Multiply every term in the bracket."], ["Sign errors with a negative outside", "−2(a + 1) = −2a − 2."], ["Not taking out the HCF", "Take out the biggest common factor."]],
          [("What is a binomial?", "An expression with two terms, like x + 4."), ("How do I check a factorisation?", "Expand it again."), ("What is x × x?", "x².")]),

        U("linear-equations", "A", "Solve linear equations with the unknown on both sides, with brackets and with fractions; form and solve equations.",
          "Linear Equations", "Linear Equations",
          "Free JSS 2 maths worksheets on linear equations: unknowns on both sides, negative numbers, brackets and fractions, and word problems. 100 questions with answers.",
          "Collect the letters on one side", "Clear fractions by multiplying.",
          [("Unknowns on both sides", [cx(eq.one_basic, 20)]), ("With negative numbers", [cx(eq.one_neg, 20)]), ("With brackets", [cx(eq.one_br, 20)]),
           ("With fractions", [cx(eq.one_frac, 20)]), ("Word problems", [co(J.eq_word, 20)])],
          ul(["Move the letter terms to one side and the numbers to the other by doing the same to both sides.", "Expand brackets first.",
              "To clear fractions, multiply every term by the LCM of the denominators."]),
          [ex("5x − 3 = 2x + 12", ["3x = 15"], "x = 5"), ex("(x + 1)/3 = 4", ["x + 1 = 12"], "x = 11")],
          [["Changing the sign of only one side", "Do the same to both sides."], ["Not multiplying every term", "Multiply each term by the LCM."], ["Dividing before collecting terms", "Collect first, then divide."]],
          [("Can an equation have a fraction answer?", "Yes."), ("How do I check?", "Substitute into both sides."), ("What is a linear equation?", "One with no powers of x above 1.")]),

        U("graphs-of-linear-equations", "A", "Plot points on the Cartesian plane; draw graphs of linear equations from a table of values; find the gradient and intercept.",
          "Graphs of Linear Equations", "Linear Graphs",
          "Free JSS 2 maths worksheets on graphs: coordinates in four quadrants, tables of values, straight-line graphs, gradient and y-intercept. 100 questions with answers.",
          "y = mx + c", "m is the gradient, c is the y-intercept.",
          [("Coordinates", [cx(co7.one_read, 10), cx(co7.one_quadrant, 10)]), ("Tables of values", [cx(co7.one_table, 20)]), ("Is the point on the line?", [cx(co7.one_onl, 20)]),
           ("Gradient and intercept", [cx(lg.one_mc, 10), cx(lg.one_grad, 10)]), ("Read the graph", [cx(lg.one_from_graph, 10), cx(co7.one_lines, 10)])],
          ul(["A point (x, y): go across x, then up y.", "Make a table of values, plot the points and join them with a straight line.",
              "In y = mx + c, m is the gradient (steepness) and c is where the line crosses the y-axis."]),
          [ex("y = 2x − 1 when x = 3", ["2 × 3 − 1"], "y = 5, so (3, 5) is on the line")],
          [["Plotting (y, x)", "x first, then y."], ["Reading the gradient upside down", "Gradient = rise ÷ run."], ["Joining points with curves", "Linear graphs are straight lines."]],
          [("What is the origin?", "The point (0, 0)."), ("What does a negative gradient mean?", "The line slopes down from left to right."), ("What is the graph of y = 3?", "A horizontal line.")]),

        U("angles-in-parallel-lines-and-polygons", "G", "Find corresponding, alternate and co-interior angles with parallel lines; find the sum of interior and exterior angles of polygons.",
          "Angles: Parallel Lines and Polygons", "Angles and Polygons",
          "Free JSS 2 maths worksheets on angles with parallel lines (corresponding, alternate, co-interior), naming polygons and interior and exterior angles of polygons. 100 questions with answers.",
          "Interior sum = (n − 2) × 180°", "Exterior angles add up to 360°.",
          [("Parallel lines", [cx(ap.one_parallel, 10), cx(sgap.one_parallel, 10)]), ("Name the polygon", [cx(ap.one_name, 20)]), ("Interior angle sum", [cx(ap.one_sum, 20)]),
           ("Regular polygons", [cx(ap.one_regular, 20)]), ("Number of sides", [cx(ap.one_sides, 20)])],
          ul(["With parallel lines, corresponding angles are equal, alternate angles are equal and co-interior angles add up to 180°.", "The interior angles of an n-sided polygon add up to (n − 2) × 180°.",
              "The exterior angles of any polygon add up to 360°. In a regular polygon, each exterior angle = 360° ÷ n."]),
          [ex("Each interior angle of a regular hexagon", ["(6 − 2) × 180 = 720", "720 ÷ 6"], "120°")],
          [["Mixing up alternate and co-interior", "Alternate angles are on opposite sides (Z shape)."], ["Using n × 180°", "It is (n − 2) × 180°."], ["Forgetting exterior + interior = 180°", "They lie on a straight line."]],
          [("What is a regular polygon?", "All sides and all angles equal."), ("What is the interior angle sum of a pentagon?", "540°."), ("How many sides has a polygon with exterior angle 40°?", "9.")]),

        U("area-of-plane-shapes", "G", "Find the area of triangles, parallelograms, trapeziums and circles; find the circumference of circles; solve problems.",
          "Area of Plane Shapes and Circles", "Area of Plane Shapes",
          "Free JSS 2 maths worksheets on area: triangles, parallelograms, trapeziums, circumference and area of circles, and composite shapes. 100 questions with answers.",
          "Circle: A = πr², C = 2πr", "Trapezium: ½(a + b)h",
          [("Triangles and rectangles", [cx(pa.one_rt, 20)]), ("Parallelograms and trapeziums", [cx(pa.one_pt, 20)]), ("Circumference", [cx(ci.one_circ, 20)]),
           ("Area of a circle", [cx(ci.one_area, 10), co(A.circ_word, 10)]), ("Composite shapes", [cx(pa.one_comp, 20)])],
          ul(["Area of a triangle = ½ × base × height; parallelogram = base × height; trapezium = ½(a + b)h.", "Circumference = πd = 2πr. Area of a circle = πr².",
              "Use π = 22/7 when the radius is a multiple of 7, otherwise use 3.14 or the π button."]),
          [ex("Circle with diameter 14 cm", ["r = 7", "A = 22/7 × 7 × 7"], "154 cm²")],
          [["Using the diameter in πr²", "Halve it first."], ["Using the slant height", "Use the perpendicular height."], ["Squaring π", "Only the radius is squared."]],
          [("What is π?", "The ratio of circumference to diameter, about 3.14."), ("What is a sector?", "A slice of a circle between two radii."), ("How do I find the area of a ring?", "Big circle − small circle.")]),

        U("volume-of-prisms-and-cylinders", "G", "Find the volume and surface area of cuboids, prisms and cylinders; solve problems with capacity.",
          "Volume and Surface Area of Prisms and Cylinders", "Volume of Prisms and Cylinders",
          "Free JSS 2 maths worksheets on volume and surface area: cuboids, triangular prisms, cylinders and capacity problems. 100 questions with answers.",
          "Prism: V = area of cross-section × length", "Cylinder: V = πr²h",
          [("Cuboids", [cx(vo.one_cuboid, 20)]), ("Prisms", [cx(vo.one_prism, 20)]), ("Cylinders", [cx(vo.one_cyl, 10), cx(sgvo.one_cyl, 10)]),
           ("Surface area", [cx(vo.one_sa, 10), cx(sgvo.one_sa, 10)]), ("Mixed", [cx(sgvo.one_prism, 10), cx(sgvo.one_cuboid, 10)])],
          ul(["The volume of a prism = area of the cross-section × length.", "A cylinder is a prism with a circular cross-section: V = πr²h.", "Surface area is the total area of all the faces."]),
          [ex("Cylinder with r = 7 cm and h = 10 cm", ["22/7 × 49 × 10"], "1,540 cm³")],
          [["Using the diameter as the radius", "r = d ÷ 2."], ["Adding instead of multiplying", "Volume is area × length."], ["Missing faces in surface area", "Count every face."]],
          [("What is a prism?", "A solid with the same cross-section all along its length."), ("How many litres in 1,000 cm³?", "1 litre."), ("Is a cylinder a prism?", "It is like one, with a circular cross-section.")]),

        U("pythagoras-theorem", "G", "Use Pythagoras' theorem to find the hypotenuse and the shorter sides of right-angled triangles; test whether a triangle is right-angled.",
          "Pythagoras' Theorem", "Pythagoras' Theorem",
          "Free JSS 2 maths worksheets on Pythagoras' theorem: finding the hypotenuse, finding a shorter side, answers to decimal places and testing for a right angle. 100 questions with answers.",
          "a² + b² = c²", "c is the hypotenuse, opposite the right angle.",
          [("Find the hypotenuse", [cx(py.one_hyp, 20)]), ("Answers to decimal places", [cx(py.one_hyp_dp, 20)]), ("Find a shorter side", [cx(py.one_short, 10), cx(sgpy.one_short, 10)]),
           ("Is it right-angled?", [cx(py.one_test, 20)]), ("Mixed", [cx(sgpy.one_hyp, 10), cx(sgpy.one_hyp_dp, 10)])],
          ul(["In a right-angled triangle, the square on the hypotenuse equals the sum of the squares on the other two sides: c² = a² + b².",
              "To find a shorter side, subtract: a² = c² − b².", "If a² + b² = c² for three sides, the triangle has a right angle. 3, 4, 5 and 5, 12, 13 are Pythagorean triples."]),
          [ex("Legs 6 cm and 8 cm", ["36 + 64 = 100"], "10 cm"), ex("Hypotenuse 13 m, one side 5 m", ["169 − 25 = 144"], "12 m")],
          [["Adding to find a shorter side", "Subtract from c²."], ["Forgetting the square root", "c² = 100 means c = 10."], ["Using the wrong side as c", "c is opposite the right angle."]],
          [("Who was Pythagoras?", "A Greek mathematician who lived about 2,500 years ago."), ("Does it work for any triangle?", "Only for right-angled triangles."), ("Where is it used?", "In building, carpentry and finding distances.")]),

        U("statistics", "S", "Find the mean, median, mode and range from frequency tables; draw and read pie charts.",
          "Statistics: Frequency Tables and Averages", "Statistics",
          "Free JSS 2 maths worksheets on statistics: mean, median, mode and range from frequency tables, grouped data and pie charts. 100 questions with answers.",
          "Mean = Σfx ÷ Σf", "Mode = value with the highest frequency.",
          [("Mean from a table", [cx(ft.one_mean, 20)]), ("Median, mode and range", [cx(ft.one_mmr, 20)]), ("Grouped data", [cx(ft.one_grouped, 10), cx(sgfq.one_grouped, 10)]),
           ("Pie charts", [cx(ft.one_pie, 20)]), ("Averages", [cx(av.one_mean, 10), cx(av.one_median, 10)])],
          ul(["In a frequency table, multiply each value by its frequency and add: Σfx. Mean = Σfx ÷ Σf.", "The median is the middle value of all the data in order.",
              "For grouped data, the modal class is the class with the highest frequency."]),
          [ex("Scores 1, 2, 3 with frequencies 4, 5, 1", ["Σfx = 4 + 10 + 3 = 17, Σf = 10"], "mean 1.7")],
          [["Dividing by the number of rows", "Divide by the total frequency."], ["Taking the biggest frequency as the mode", "The mode is the value, not the frequency."], ["Not ordering for the median", "Use the cumulative frequency."]],
          [("What is frequency?", "How many times a value occurs."), ("What is a modal class?", "The class with the most data."), ("What is Σ?", "The Greek letter sigma, meaning sum.")]),

        U("probability", "S", "Find the probability of simple events; use the probability scale; find the probability that an event does not happen; list outcomes of two events.",
          "Probability", "Probability",
          "Free JSS 2 maths worksheets on probability: the probability scale, probability of single events, events not happening, sample spaces and two dice. 100 questions with answers.",
          "P(event) = favourable ÷ total", "P(not A) = 1 − P(A)",
          [("Probability scale", [cx(pr7.one_scale, 20)]), ("Single events", [cx(pr7.one_single, 20)]), ("Not happening", [cx(pr7.one_not, 10), cx(sgpr.one_not, 10)]),
           ("Sample spaces", [cx(pr7.one_space, 20)]), ("Two dice", [cx(pr8.one_dice, 20)])],
          ul(["Probability is a number from 0 (impossible) to 1 (certain).", "P(event) = number of favourable outcomes ÷ total number of equally likely outcomes.",
              "The probabilities of all the outcomes add up to 1, so P(not A) = 1 − P(A)."]),
          [ex("A bag has 3 red and 5 blue balls", ["P(red) = 3/8"], "P(not red) = 5/8")],
          [["Probabilities bigger than 1", "Check your answer is between 0 and 1."], ["Not counting all outcomes", "List them in a table."], ["Adding probabilities of the same outcome twice", "Count each outcome once."]],
          [("What is an outcome?", "One possible result."), ("What is a sample space?", "The list of all possible outcomes."), ("What is P(certain)?", "1.")]),
    ]


if __name__ == "__main__":
    main("jss-2", "JSS 2", units, 160200)
