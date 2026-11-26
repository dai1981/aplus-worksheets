# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / SSS 1 (NERDC Senior Secondary School General Mathematics; WAEC and NECO syllabus).
  python3 tools/ng_s1.py [number …]      seed = 170100 + number, reused modules 1719NN
"""
from ng_unit import mod, co, cx, ul, U, main, example as ex
import ng_p5a as A
import ng_ja as J
import ng_sa as S

TH_S = {"N": "Number and Numeration", "A": "Algebraic Processes", "M": "Mensuration", "G": "Geometry", "T": "Trigonometry",
        "S": "Statistics and Probability", "C": "Introductory Calculus", "V": "Vectors and Transformation"}


def units():
    ix = mod("gen_uk_maths_y8_indices", 171901)
    sgix = mod("gen_sg_maths_s3_indices", 171902)
    lg = mod("gen_us_math_a2_logarithms_and_their_properties", 171903)
    leq = mod("gen_us_math_a2_exponential_and_logarithmic_equations", 171904)
    sv = mod("gen_sg_maths_s4_sets_and_venn_diagrams", 171905)
    st = mod("gen_in_maths_c11_sets", 171906)
    qe = mod("gen_sg_maths_s2_quadratic_equations", 171907)
    inq = mod("gen_in_maths_c10_quadratic_equations", 171908)
    ar = mod("gen_uk_maths_y9_arcs_and_sectors", 171909)
    inar = mod("gen_in_maths_c10_areas_related_to_circles", 171910)
    vol = mod("gen_uk_maths_y9_volume_of_cylinders_cones_and_spheres", 171911)
    usv = mod("gen_us_math_ge_volume_of_solids", 171912)
    insa = mod("gen_in_maths_c10_surface_areas_and_volumes", 171913)
    tg = mod("gen_uk_maths_y9_trigonometry", 171914)
    intg = mod("gen_in_maths_c10_introduction_to_trigonometry", 171915)
    ap = mod("gen_in_maths_c10_some_applications_of_trigonometry", 171916)
    be = mod("gen_sg_maths_s3_bearings_and_angles_of_elevation", 171917)
    ukb = mod("gen_uk_maths_y9_bearings_and_loci", 171918)
    inst = mod("gen_in_maths_c10_statistics", 171919)
    mmm = mod("gen_sg_maths_s2_mean_median_and_mode", 171920)
    cf = mod("gen_sg_maths_s4_cumulative_frequency_and_box_plots", 171921)
    pr = mod("gen_in_maths_c10_probability", 171922)
    sgp = mod("gen_sg_maths_s2_probability", 171923)
    cp = mod("gen_sg_maths_s4_probability_of_combined_events", 171924)
    std = mod("gen_sg_maths_s3_standard_form", 171925)

    return [
        U("number-bases", "N", "Convert numbers between base ten and other bases; add, subtract and multiply in other bases; solve problems on number bases.",
          "Number Bases: Conversion and Operations", "Number Bases",
          "Free SSS 1 maths worksheets on number bases: converting between base ten, base two and other bases, and adding, subtracting and multiplying in any base. 100 questions with answers.",
          "Each place is a power of the base", "In base 5 the places are 1, 5, 25, 125 …",
          [("Base ten to other bases", [co(A.base_from, 10), co(A.bin_from, 10)]), ("Other bases to base ten", [co(A.base_to, 10), co(A.bin_to, 10)]),
           ("Base to base", [co(J.base_convert, 20)]), ("Add and subtract", [co(J.base_add, 10), co(J.base_sub, 10)]),
           ("Multiply and find the base", [co(J.base_mul, 10), co(J.bin_mul, 4), co(J.base_find, 6)])],
          ul(["To change to base ten, multiply each digit by its place value and add.", "To change from base ten, divide by the base again and again and read the remainders from the bottom up.",
              "To add or subtract in base b, carry or borrow b, not 10."]),
          [ex("Change 231₄ to base ten", ["2 × 16 + 3 × 4 + 1"], "45"), ex("Change 23 to base two", ["23 ÷ 2 … remainders 1, 1, 1, 0, 1"], "10111₂")],
          [["Reading the remainders from the top", "Read them from the bottom up."], ["Carrying 10 in another base", "Carry the base number."], ["Using a digit that is too big", "Base 5 uses only 0 to 4."]],
          [("Why is base two used?", "Computers store numbers with two states, on and off."), ("What is 100₅ in base ten?", "25."), ("How do I check an answer?", "Change both sides to base ten.")]),

        U("modular-arithmetic", "N", "Add, subtract and multiply in modular arithmetic; solve simple congruences; use modular arithmetic for days of the week and clocks.",
          "Modular Arithmetic", "Modular Arithmetic",
          "Free SSS 1 maths worksheets on modular arithmetic: addition, subtraction and multiplication mod n, solving congruences, tables, days of the week and clock problems. 100 questions with answers.",
          "Keep only the remainder", "17 mod 5 = 2, because 17 = 3 × 5 + 2.",
          [("Addition", [co(S.mod_add, 20)]), ("Subtraction", [co(S.mod_sub, 20)]), ("Multiplication", [co(S.mod_mul, 14), co(S.mod_table, 6)]),
           ("Solve the congruence", [co(S.mod_solve, 10), co(S.mod_add_solve, 10)]), ("Days and clocks", [co(S.mod_day, 12), co(S.mod_clock, 8)])],
          ul(["In mod n, every number is replaced by its remainder after dividing by n.", "Do the working as usual, then divide by n and keep the remainder.",
              "A negative answer is made positive by adding n: −2 mod 7 = 5."]),
          [ex("(8 + 9) mod 5", ["17 = 3 × 5 + 2"], "2"), ex("Solve 3x ≡ 1 (mod 5)", ["3 × 2 = 6 ≡ 1"], "x = 2")],
          [["Giving the quotient", "The answer is the remainder."], ["Leaving a negative answer", "Add the modulus until it is between 0 and n − 1."], ["Using 12 o’clock as 0", "On a clock, a remainder of 0 means 12 o’clock."]],
          [("What does ≡ mean?", "Is congruent to: has the same remainder."), ("Where is modular arithmetic used?", "Days of the week, clocks, ISBN and bank check digits."), ("What is 25 mod 7?", "4.")]),

        U("indices-and-standard-form", "N", "Use the laws of indices including negative and fractional indices; solve simple exponential equations; write numbers in standard form.",
          "Indices and Standard Form", "Indices",
          "Free SSS 1 maths worksheets on indices: laws of indices, negative and fractional indices, exponential equations and standard form. 100 questions with answers.",
          "aᵐ × aⁿ = aᵐ⁺ⁿ", "a^(1/n) is the nth root; a⁻ⁿ = 1/aⁿ.",
          [("Laws of indices", [cx(ix.one_mul, 7), cx(ix.one_div, 6), cx(ix.one_pp, 7)]), ("Negative and zero indices", [cx(ix.one_neg, 14), cx(ix.one_eval, 6)]),
           ("Fractional indices", [cx(sgix.one_frac, 20)]), ("Indices in algebra", [cx(sgix.one_alg, 12), cx(ix.one_alg, 8)]),
           ("Standard form", [cx(std.one_big, 7), cx(std.one_small, 7), cx(std.one_md, 6)])],
          ul(["Same base: add indices when multiplying and subtract when dividing.", "A fractional index means a root: 8^(1/3) = 2, 8^(2/3) = 4.",
              "Standard form is A × 10ⁿ with 1 ≤ A &lt; 10."]),
          [ex("27^(2/3)", ["Cube root first: 3", "Then square"], "9"), ex("0.00045 in standard form", ["Move the point 4 places"], "4.5 × 10⁻⁴")],
          [["Multiplying the bases", "2³ × 2⁴ = 2⁷, not 4⁷."], ["Making a negative index negative", "2⁻² = 1/4."], ["Writing 45 × 10³ as standard form", "A must be less than 10: 4.5 × 10⁴."]],
          [("What is any number to the power 0?", "1 (except 0⁰)."), ("What is 16^(−1/2)?", "1/4."), ("Why use standard form?", "It makes very large and very small numbers easy to write and compare.")]),

        U("logarithms", "N", "Change between index and logarithm form; use the laws of logarithms; use given logarithms to find others; solve simple logarithmic equations.",
          "Logarithms: Laws and Equations", "Logarithms",
          "Free SSS 1 maths worksheets on logarithms: index and log form, laws of logarithms, using log 2 and log 3, and solving logarithmic equations. 100 questions with answers.",
          "log_b N = n means bⁿ = N", "log ab = log a + log b",
          [("Index form and log form", [co(S.log_exp, 10), cx(lg.one_conv, 10)]), ("Evaluate logarithms", [co(S.log_eval, 12), cx(lg.one_exp, 8)]),
           ("Laws of logarithms", [co(S.log_laws, 10), cx(lg.one_cob, 10)]), ("Using log 2 and log 3", [co(S.log_given, 14), co(S.log_laws, 6)]),
           ("Logarithmic equations", [co(S.log_solve, 10), cx(leq.one_logeq, 10)])],
          ul(["A logarithm is a power: log₂ 8 = 3 because 2³ = 8.", "log ab = log a + log b, log (a ÷ b) = log a − log b, log aⁿ = n log a.",
              "log 10 = 1 and log 1 = 0 in base ten."]),
          [ex("log 4 + log 25", ["log 100"], "2"), ex("Solve log₃ x = 4", ["x = 3⁴"], "x = 81")],
          [["log (a + b) = log a + log b", "That is false. The law is for a product."], ["Dividing logs: log a ÷ log b", "log a − log b is log (a ÷ b)."], ["Forgetting the base", "log with no base means base ten."]],
          [("What is log₅ 1?", "0."), ("What is log 1000?", "3."), ("Why were log tables used?", "To turn multiplication into addition before calculators.")]),

        U("sets-and-venn-diagrams", "N", "Use set notation; find unions, intersections and complements; draw and use Venn diagrams with two and three sets; solve word problems.",
          "Sets and Venn Diagrams", "Sets",
          "Free SSS 1 maths worksheets on sets: notation, subsets, union, intersection, complement and Venn diagram word problems. 100 questions with answers.",
          "∪ is union, ∩ is intersection", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
          [("Set notation", [cx(sv.one_notation, 10), cx(st.one_roster, 10)]), ("Subsets", [cx(st.one_subsets, 14), cx(st.one_type, 6)]),
           ("Union, intersection and complement", [cx(sv.one_ops, 10), cx(st.one_diff, 10)]), ("Read the Venn diagram", [cx(sv.one_read, 14), cx(sv.one_shade, 6)]),
           ("Venn diagram problems", [cx(st.one_count, 12), cx(sv.one_prob, 8)])],
          ul(["A ∪ B has everything in A or B (or both). A ∩ B has only what is in both.", "A′ (the complement) is everything in the universal set that is not in A.",
              "Fill a Venn diagram from the middle (the intersection) outwards."]),
          [ex("n(A) = 15, n(B) = 12, n(A ∩ B) = 5", ["15 + 12 − 5"], "n(A ∪ B) = 22")],
          [["Counting the intersection twice", "Take it away once."], ["Mixing up ∪ and ∩", "∪ looks like a cup that holds everything."], ["Forgetting the elements outside A and B", "They belong to the universal set."]],
          [("How many subsets does a set of 3 elements have?", "2³ = 8."), ("What is the empty set?", "A set with no elements, written ∅ or { }."), ("What is ξ?", "The universal set.")]),

        U("logical-reasoning", "N", "Recognise simple and compound statements; find negations; write the converse, inverse and contrapositive; find truth values; draw valid conclusions.",
          "Logical Reasoning", "Logical Reasoning",
          "Free SSS 1 maths worksheets on logical reasoning: negation, converse, inverse and contrapositive, truth values with and, or and implies, and valid conclusions. 100 questions with answers.",
          "p ⇒ q is false only when p is true and q is false", "The contrapositive ~q ⇒ ~p means the same as p ⇒ q.",
          [("Negation", [co(S.lg_neg, 12), co(S.lg_truth, 8)]), ("Converse, inverse and contrapositive", [co(S.lg_parts, 20)]), ("Truth values", [co(S.lg_truth, 20)]),
           ("Valid conclusions", [co(S.lg_valid, 12), co(S.lg_parts, 8)]), ("Mixed reasoning", [co(S.lg_parts, 10), co(S.lg_neg, 4), co(S.lg_valid, 6)])],
          ul(["A statement is either true or false. Its negation has the opposite truth value.", "For “if p, then q”: the converse is “if q, then p”; the contrapositive is “if not q, then not p”.",
              "p ∧ q (and) is true only when both are true; p ∨ q (or) is true when at least one is true."]),
          [ex("Negation of “All boys like football.”", ["Not all boys do"], "Some boys do not like football.")],
          [["Thinking the converse is always true", "Only the contrapositive always has the same truth value."], ["Negating “all” as “none”", "The negation of “all” is “some … not”."], ["Thinking p ⇒ q is false when p is false", "It is true whenever p is false."]],
          [("What does ~p mean?", "Not p."), ("Is the contrapositive equivalent to the statement?", "Yes."), ("What is a valid argument?", "One whose conclusion must be true when the premises are true.")]),

        U("quadratic-equations", "A", "Solve quadratic equations by factorisation; form quadratic equations from given roots and from word problems.",
          "Quadratic Equations by Factorisation", "Quadratic Equations",
          "Free SSS 1 maths worksheets on quadratic equations: solving by factorisation, the difference of two squares, forming equations from roots and word problems. 100 questions with answers.",
          "If ab = 0, then a = 0 or b = 0", "x² − 5x + 6 = (x − 2)(x − 3) = 0 gives x = 2 or 3.",
          [("x² + bx + c = 0", [cx(qe.one_monic, 20)]), ("ax² + bx + c = 0", [cx(qe.one_nonmonic, 20)]), ("Special quadratics", [cx(qe.one_special, 10), cx(qe.one_zero, 10)]),
           ("Standard form first", [cx(inq.one_std, 20)]), ("Word problems", [cx(qe.one_prob, 12), cx(inq.one_speed, 8)])],
          ul(["Make one side 0 first.", "Factorise, then set each factor equal to 0.", "Check both answers in the question; a length cannot be negative."]),
          [ex("x² + x − 12 = 0", ["(x + 4)(x − 3) = 0"], "x = −4 or x = 3")],
          [["Dividing by x", "You lose the answer x = 0. Factorise instead."], ["Not making one side 0", "x² + x = 6 must become x² + x − 6 = 0."], ["Wrong signs in the roots", "(x + 4) = 0 gives x = −4."]],
          [("How many roots can a quadratic have?", "At most two."), ("What quadratic has roots 2 and 5?", "x² − 7x + 10 = 0."), ("What if it will not factorise?", "Use the formula or complete the square (SSS 2).")]),

        U("lengths-and-areas-of-plane-shapes", "M", "Find perimeters and areas of plane shapes; find arc lengths, perimeters and areas of sectors and segments of circles.",
          "Arcs, Sectors and Areas of Plane Shapes", "Lengths and Areas",
          "Free SSS 1 maths worksheets on mensuration of plane shapes: circles, arc length, sectors, segments and perimeters. 100 questions with answers.",
          "Arc = θ/360 × 2πr", "Sector area = θ/360 × πr²",
          [("Circles", [cx(inar.one_basic, 12), cx(ar.one_pi, 8)]), ("Arc length", [cx(ar.one_arc, 20)]), ("Area of a sector", [cx(ar.one_area, 20)]),
           ("Perimeter of a sector", [cx(ar.one_perim, 20)]), ("Segments and problems", [cx(inar.one_seg, 10), cx(inar.one_prob, 10)])],
          ul(["A sector is a slice of a circle; its angle θ is a fraction θ/360 of the full turn.", "Arc length = θ/360 × 2πr; sector area = θ/360 × πr².",
              "A segment = sector − triangle."]),
          [ex("r = 7 cm, θ = 90°", ["90/360 × 2 × 22/7 × 7"], "Arc = 11 cm")],
          [["Using the diameter as the radius", "Halve the diameter first."], ["Leaving out the two radii in the perimeter", "Perimeter = arc + 2r."], ["Using 2πr for area", "Area uses πr²."]],
          [("Which value of π should I use?", "Use 22/7 or 3.142 as the question says."), ("What is a minor arc?", "The shorter arc between two points."), ("What is a segment?", "The part between a chord and an arc.")]),

        U("surface-area-and-volume-of-solids", "M", "Find the surface area and volume of cubes, cuboids, cylinders, cones, pyramids and spheres; solve related problems.",
          "Surface Area and Volume of Solids", "Surface Area and Volume",
          "Free SSS 1 maths worksheets on mensuration of solids: volume and surface area of cylinders, cones and spheres, and word problems. 100 questions with answers.",
          "Cylinder: V = πr²h", "Cone: V = ⅓πr²h; sphere: V = 4/3 πr³",
          [("Cylinders", [cx(vol.one_cyl, 20)]), ("Cones", [cx(vol.one_cone, 20)]), ("Spheres", [cx(vol.one_sph, 14), cx(insa.one_sa, 6)]),
           ("Answers in terms of π", [cx(vol.one_pi, 20)]), ("Solid problems", [cx(usv.one_prob, 14), cx(insa.one_sa, 6)])],
          ul(["Volume of a prism or cylinder = area of the cross-section × length.", "A cone or pyramid has one third of the volume of the matching cylinder or prism.",
              "Curved surface area: cylinder 2πrh, cone πrl, sphere 4πr²."]),
          [ex("Cylinder r = 7 cm, h = 10 cm", ["22/7 × 7 × 7 × 10"], "V = 1,540 cm³")],
          [["Using the slant height for the volume of a cone", "Volume uses the vertical height."], ["Forgetting the two ends of a cylinder", "Total surface area = 2πrh + 2πr²."], ["Mixing cm² and cm³", "Area is square units, volume is cubic units."]],
          [("How many litres is 1,000 cm³?", "1 litre."), ("What is the slant height?", "l = √(r² + h²)."), ("Why is the cone ⅓ of the cylinder?", "Three cones of water fill the cylinder with the same base and height.")]),

        U("trigonometric-ratios", "T", "Use sine, cosine and tangent in right-angled triangles to find sides and angles; use the special angles 30°, 45° and 60°.",
          "Trigonometric Ratios: Sine, Cosine and Tangent", "Trigonometric Ratios",
          "Free SSS 1 maths worksheets on trigonometric ratios: SOH CAH TOA, finding sides and angles, and the values for 30°, 45° and 60°. 100 questions with answers.",
          "SOH CAH TOA", "sin = opp/hyp, cos = adj/hyp, tan = opp/adj",
          [("Name the sides", [cx(tg.one_label, 20)]), ("Find a side", [cx(tg.one_side_mul, 20)]), ("Find a side (divide)", [cx(tg.one_side_div, 20)]),
           ("Ratios from a triangle", [cx(intg.one_tri, 10), cx(intg.one_from, 10)]), ("Special angles", [cx(intg.one_val, 14), cx(intg.one_id, 6)])],
          ul(["The hypotenuse is opposite the right angle; the opposite side faces the angle.", "Choose the ratio that uses the side you know and the side you want.",
              "sin 30° = 1/2, cos 60° = 1/2, tan 45° = 1."]),
          [ex("Hypotenuse 10 cm, angle 30°. Opposite?", ["10 × sin 30°"], "5 cm")],
          [["Mixing up the opposite and adjacent sides", "Find the angle first, then label."], ["Using tan for the hypotenuse", "tan does not use the hypotenuse."], ["Calculator in radians", "Set it to degrees."]],
          [("What is sin² θ + cos² θ?", "1."), ("What is tan 60°?", "√3."), ("Can sin θ be more than 1?", "No.")]),

        U("angles-of-elevation-and-depression", "T", "Solve problems on angles of elevation and depression using trigonometric ratios.",
          "Angles of Elevation and Depression", "Elevation and Depression",
          "Free SSS 1 maths worksheets on angles of elevation and depression: heights of buildings and trees, distances and two-angle problems. 100 questions with answers.",
          "Measure from the horizontal", "Elevation looks up; depression looks down.",
          [("Angle of elevation", [cx(be.one_elev, 20)]), ("Angle of depression", [cx(be.one_dep, 20)]), ("Find the height", [cx(ap.one_h, 20)]),
           ("Find the distance", [cx(ap.one_d, 12), cx(ap.one_dep, 8)]), ("Problems", [cx(ap.one_sit, 12), cx(ap.one_two, 8)])],
          ul(["Draw a sketch with the horizontal line and the right angle.", "The angle of depression from the top equals the angle of elevation from the bottom (alternate angles).",
              "Then use tan, sin or cos in the right-angled triangle."]),
          [ex("From 30 m away, a tree top is at 45°", ["h = 30 × tan 45°"], "30 m")],
          [["Measuring from the vertical", "Both angles are from the horizontal."], ["Using the wrong triangle", "Mark the right angle at the foot."], ["Forgetting the observer’s height", "Add it if the question gives it."]],
          [("Are the angles of elevation and depression equal?", "Yes, between the same two points."), ("Which ratio is used most?", "tan, because height and distance are opposite and adjacent."), ("What is a clinometer?", "A tool that measures angles of elevation.")]),

        U("bearings", "T", "Read and draw three-figure bearings; find back bearings; solve problems on bearings and distances.",
          "Bearings", "Bearings",
          "Free SSS 1 maths worksheets on bearings: three-figure bearings, compass directions, back bearings and distance problems. 100 questions with answers.",
          "Measure clockwise from north", "Always use three figures: 045°.",
          [("Read the bearing", [cx(be.one_read, 14), co(A.bearing_read, 6)]), ("Compass directions", [co(A.bearing_name, 8), co(A.bearing_dir, 6), cx(be.one_read, 6)]),
           ("Back bearings", [cx(be.one_back, 14), co(A.bearing_back, 6)]), ("Turns", [co(A.bearing_turn, 12), cx(ukb.one_read, 8)]), ("Bearing problems", [cx(be.one_prob, 20)])],
          ul(["Stand at the first place, face north, and turn clockwise to the second place.", "Write the angle with three figures: 9° is 009°.",
              "Back bearing = bearing ± 180°."]),
          [ex("Bearing of B from A is 060°", ["060° + 180°"], "Bearing of A from B = 240°")],
          [["Measuring anticlockwise", "Bearings are clockwise."], ["Starting from the wrong point", "“From A” means stand at A."], ["Writing 45° instead of 045°", "Use three figures."]],
          [("What bearing is south-west?", "225°."), ("What is a back bearing?", "The bearing for the return journey."), ("Can a bearing be 360°?", "We write 000° for north.")]),

        U("data-presentation", "S", "Present data in frequency tables, bar charts, histograms and pie charts; read and interpret these charts; group data in classes.",
          "Data Presentation: Tables and Charts", "Data Presentation",
          "Free SSS 1 maths worksheets on statistics: frequency tables, grouped data, class marks, histograms and cumulative frequency tables. 100 questions with answers.",
          "Frequency is how many times", "Class mark = (lower + upper) ÷ 2",
          [("Frequency tables", [cx(cf.one_table, 20)]), ("Read the data", [cx(cf.one_list, 20)]), ("Grouped data", [cx(inst.one_direct, 20)]),
           ("Cumulative frequency", [cx(cf.one_curve, 20)]), ("Compare data", [cx(cf.one_cmp, 20)])],
          ul(["Use tally marks to make a frequency table.", "For grouped data, each class has a class interval and a class mark (the middle).",
              "In a pie chart, each item’s angle = frequency ÷ total × 360°."]),
          [ex("Classes 10–19, 20–29", ["(10 + 19) ÷ 2"], "Class mark 14.5")],
          [["Leaving gaps in a histogram", "The bars touch."], ["Adding the class marks", "Multiply each by its frequency first."], ["Pie angles not totalling 360°", "Check the total."]],
          [("What is a histogram?", "A bar chart for grouped data with touching bars."), ("What is a class boundary?", "Halfway between two classes, like 19.5."), ("What is an ogive?", "A cumulative frequency curve.")]),

        U("measures-of-central-tendency", "S", "Find the mean, median and mode of ungrouped and grouped data; use the assumed mean; find missing values from the mean.",
          "Mean, Median and Mode", "Mean, Median and Mode",
          "Free SSS 1 maths worksheets on measures of central tendency: mean, median and mode of lists and frequency tables, assumed mean and the modal class. 100 questions with answers.",
          "Mean = Σfx ÷ Σf", "Median is the middle value in order.",
          [("Median", [cx(mmm.one_median, 20)]), ("Mode and range", [cx(mmm.one_mode_range, 10), cx(inst.one_mode, 10)]), ("Mean of a frequency table", [cx(inst.one_direct, 20)]),
           ("Assumed mean", [cx(inst.one_step, 20)]), ("Averages problems", [co(A.mean_missing, 8), co(A.mean_word, 6), cx(inst.one_med, 6)])],
          ul(["Mean = total of the values ÷ how many values.", "Put the values in order to find the median. With an even number, take the mean of the middle two.",
              "The mode is the most common value; for grouped data, the modal class."]),
          [ex("3, 7, 8, 8, 9", ["Sum 35, 5 values"], "Mean 7, median 8, mode 8")],
          [["Finding the median without ordering", "Put the values in order first."], ["Dividing Σfx by the number of classes", "Divide by Σf."], ["Mixing up mode and frequency", "The mode is the value, not how many."]],
          [("Which average do outliers affect most?", "The mean."), ("Can there be two modes?", "Yes (bimodal)."), ("What is the assumed mean?", "A guessed mean that makes the working easier.")]),

        U("probability", "S", "Find the probability of single events; use the sample space; find probabilities of combined events using addition and multiplication.",
          "Probability", "Probability",
          "Free SSS 1 maths worksheets on probability: single events, dice, cards and bags, sample spaces, and combined events. 100 questions with answers.",
          "P = favourable ÷ possible", "P(not A) = 1 − P(A)",
          [("Single events", [cx(sgp.one_single, 20)]), ("Bags and dice", [cx(pr.one_bag, 14), cx(pr.one_die, 6)]), ("Not happening", [cx(sgp.one_not, 12), cx(sgp.one_scale, 8)]),
           ("Sample spaces", [cx(cp.one_space, 12), cx(sgp.one_space, 8)]), ("Combined events", [cx(cp.one_with, 10), cx(cp.one_without, 10)])],
          ul(["Probability = number of favourable outcomes ÷ number of possible outcomes.", "Probabilities are from 0 (impossible) to 1 (certain).",
              "For two events one after the other, multiply; for “either … or” (mutually exclusive), add."]),
          [ex("A bag has 3 red and 5 blue balls", ["Red: 3 out of 8"], "P(red) = 3/8")],
          [["Adding when you should multiply", "“And then” means multiply."], ["Forgetting that the ball is not replaced", "Take 1 from the total for the second pick."], ["Probability bigger than 1", "Check: it can never be more than 1."]],
          [("What is a sample space?", "The list of all possible outcomes."), ("How many outcomes do two dice have?", "36."), ("What is the probability of an impossible event?", "0.")]),
    ]


if __name__ == "__main__":
    main("sss-1", "SSS 1", units, 170100, th=TH_S)
