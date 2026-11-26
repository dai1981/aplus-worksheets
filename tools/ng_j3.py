# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / JSS 3 (NERDC Upper Basic Education Curriculum; the year of the BECE).
  python3 tools/ng_j3.py [number …]      seed = 160300 + number, reused modules 1639NN
"""
from ng_unit import mod, co, cx, rs, ul, U, main, example as ex
import ng_p5a as A
import ng_ja as J


def units():
    ix = mod("gen_uk_maths_y8_indices", 163901)
    sgix = mod("gen_sg_maths_s3_indices", 163902)
    dip = mod("gen_uk_maths_y8_direct_and_inverse_proportion", 163903)
    q9 = mod("gen_uk_maths_y9_expanding_and_factorising_quadratics", 163904)
    sgq = mod("gen_sg_maths_s2_expansion_and_factorisation", 163905)
    sim = mod("gen_uk_maths_y9_simultaneous_equations", 163906)
    sgsim = mod("gen_sg_maths_s2_simultaneous_equations", 163907)
    cs = mod("gen_uk_maths_y8_changing_the_subject_of_a_formula", 163908)
    sgcs = mod("gen_sg_maths_s2_changing_the_subject_of_a_formula", 163909)
    sub = mod("gen_uk_maths_y7_algebraic_notation_and_substitution", 163910)
    ine = mod("gen_uk_maths_y8_inequalities", 163911)
    sgine = mod("gen_sg_maths_s2_linear_inequalities", 163912)
    sc = mod("gen_uk_maths_y9_similarity_and_congruence", 163913)
    tr8 = mod("gen_uk_maths_y8_transformations", 163914)
    sgsc = mod("gen_sg_maths_s2_congruence_and_similarity", 163915)
    tg = mod("gen_uk_maths_y9_trigonometry", 163916)
    sgtg = mod("gen_sg_maths_s2_trigonometric_ratios", 163917)
    vs = mod("gen_uk_maths_y9_volume_of_cylinders_cones_and_spheres", 163918)
    sgvs = mod("gen_sg_maths_s2_volume_of_cones_and_spheres", 163919)
    br = mod("gen_uk_maths_y9_bearings_and_loci", 163920)
    sgbr = mod("gen_sg_maths_s3_bearings_and_angles_of_elevation", 163921)
    ft = mod("gen_uk_maths_y8_frequency_tables_and_charts", 163922)
    sgfq = mod("gen_sg_maths_s2_frequency_tables_and_grouped_data", 163923)
    sl = mod("gen_sg_maths_s2_stem_and_leaf_diagrams", 163924)
    sgav = mod("gen_sg_maths_s2_mean_median_and_mode", 163925)
    pr8 = mod("gen_uk_maths_y8_probability_of_combined_events", 163926)
    pr7 = mod("gen_uk_maths_y7_probability", 163927)
    arc = mod("gen_uk_maths_y9_arcs_and_sectors", 163928)
    sgarc = mod("gen_sg_maths_s3_arc_length_sector_area_and_radians", 163929)
    ci8 = mod("gen_uk_maths_y8_circles", 163930)
    sgms = mod("gen_sg_maths_s2_map_scales", 163931)

    return [
        U("indices", "N", "Use the laws of indices for multiplication, division and powers; use zero and negative indices; evaluate expressions with indices.",
          "Indices: Laws of Indices", "Indices",
          "Free JSS 3 maths worksheets on indices: multiplying and dividing powers, power of a power, zero and negative indices, fractional indices and evaluating. 100 questions with answers.",
          "aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ", "(aᵐ)ⁿ = aᵐⁿ, a⁰ = 1",
          [("Multiply powers", [cx(ix.one_mul, 20)]), ("Divide powers", [cx(ix.one_div, 20)]), ("Power of a power", [cx(ix.one_pp, 20)]),
           ("Zero and negative indices", [cx(ix.one_neg, 10), cx(ix.one_eval, 10)]), ("Indices in algebra", [cx(ix.one_alg, 10), cx(sgix.one_alg, 10)])],
          ul(["When you multiply powers of the same base, add the indices: 2³ × 2⁴ = 2⁷.", "When you divide, subtract the indices: 5⁶ ÷ 5² = 5⁴. A power of a power: multiply the indices.",
              "a⁰ = 1 and a⁻ⁿ = 1 ÷ aⁿ: 3⁻² = 1/9."]),
          [ex("x⁵ × x³ ÷ x²", ["5 + 3 − 2"], "x⁶"), ex("(2³)²", ["3 × 2"], "2⁶ = 64")],
          [["Multiplying the indices when multiplying powers", "Add them."], ["Thinking a⁰ = 0", "a⁰ = 1."], ["Making a negative index a negative number", "2⁻³ = 1/8, not −8."]],
          [("What is the base in 5⁴?", "5."), ("What is 10⁻¹?", "0.1."), ("Do the laws work for different bases?", "No, only for the same base.")]),

        U("compound-interest-and-depreciation", "O", "Calculate compound interest and the amount after several years; calculate depreciation; compare simple and compound interest; solve percentage problems.",
          "Compound Interest and Depreciation", "Compound Interest",
          "Free JSS 3 maths worksheets on commercial arithmetic in naira: compound interest, depreciation, percentage increase and decrease and reverse percentages. 100 questions with answers.",
          "Amount = P × (1 + R/100)ⁿ", "Depreciation: × (1 − R/100) each year.",
          [("Compound interest", [co(J.compound, 20)]), ("Depreciation", [co(J.depreciation, 20)]), ("Percentage change", [co(J.pct_change, 20)]),
           ("Cost price from selling price", [co(J.reverse_pct, 20)]), ("Simple interest", [co(A.si, 20)])],
          ul(["With compound interest, the interest is added each year and earns interest too.", "Amount after n years = P × (1 + R/100)ⁿ. Compound interest = amount − principal.",
              "Depreciation is the loss of value each year: value = P × (1 − R/100)ⁿ."]),
          [ex("₦50,000 at 10% for 2 years", ["50,000 × 1.1 × 1.1"], "₦60,500 (interest ₦10,500)")],
          [["Using simple interest for compound interest", "Multiply by the multiplier each year."], ["Adding the rate n times", "Multiply, don't add."], ["Giving the amount for the interest", "Interest = amount − principal."]],
          [("Which grows faster, simple or compound interest?", "Compound interest."), ("What is depreciation?", "The fall in value of things like cars and machines."), ("What is a multiplier for 8% growth?", "1.08.")]),

        U("variation", "A", "Solve problems on direct, inverse, joint and partial variation; find the constant of variation; write equations of variation.",
          "Variation: Direct and Inverse", "Variation",
          "Free JSS 3 maths worksheets on variation: direct and inverse variation, the constant k, variation with squares and word problems. 100 questions with answers.",
          "Direct: y = kx. Inverse: y = k/x", "Find k first.",
          [("Direct variation", [co(J.variation, 20)]), ("Inverse variation", [cx(dip.one_inverse, 20)]), ("Which variation?", [cx(dip.one_which, 20)]),
           ("Formulas", [cx(dip.one_formula, 20)]), ("Word problems", [co(J.variation_word, 20)])],
          ul(["y varies directly as x: y = kx. If x is multiplied by 3, so is y.", "y varies inversely as x: y = k ÷ x, so xy = k.",
              "Always find the constant k from the given values first, then use it."]),
          [ex("y ∝ x, y = 12 when x = 3. Find y when x = 5", ["k = 4"], "y = 20")],
          [["Using direct variation when one quantity goes down", "That is inverse."], ["Forgetting to find k", "Find k from the first pair."], ["Squaring k instead of x", "y = kx² squares x only."]],
          [("What does ∝ mean?", "Varies as (is proportional to)."), ("Give an example of inverse variation", "Time and speed for a fixed journey."), ("What is joint variation?", "y depends on two quantities, like y = kxz.")]),

        U("factorisation-of-quadratic-expressions", "A", "Expand two binomials; factorise quadratic expressions; factorise the difference of two squares.",
          "Factorisation of Quadratic Expressions", "Factorising Quadratics",
          "Free JSS 3 maths worksheets on quadratics: expanding two brackets, perfect squares, factorising x² + bx + c and the difference of two squares. 100 questions with answers.",
          "x² + bx + c = (x + p)(x + q)", "p + q = b and pq = c",
          [("Expand two brackets", [cx(q9.one_expand, 20)]), ("Perfect squares", [cx(q9.one_square, 20)]), ("Factorise: positive terms", [cx(q9.one_fact_pos, 20)]),
           ("Factorise: negative terms", [cx(q9.one_fact_neg, 20)]), ("Mixed", [cx(sgq.one_fact_pos, 10), cx(sgq.one_fact_neg, 10)])],
          ul(["(x + 3)(x + 4) = x² + 7x + 12.", "To factorise x² + bx + c, find two numbers that multiply to c and add to b.",
              "The difference of two squares: a² − b² = (a + b)(a − b)."]),
          [ex("x² − x − 12", ["−4 × 3 = −12, −4 + 3 = −1"], "(x − 4)(x + 3)"), ex("x² − 49", ["Difference of two squares"], "(x + 7)(x − 7)")],
          [["Getting the signs wrong", "Check by expanding."], ["Forgetting the middle term", "(x + 3)² = x² + 6x + 9."], ["Stopping at a common factor", "Factorise fully."]],
          [("What is a quadratic?", "An expression with x² as the highest power."), ("How do I check?", "Multiply the brackets back out."), ("Can every quadratic be factorised?", "Not with whole numbers.")]),

        U("simultaneous-linear-equations", "A", "Solve simultaneous linear equations in two unknowns by elimination and substitution; solve word problems.",
          "Simultaneous Linear Equations", "Simultaneous Equations",
          "Free JSS 3 maths worksheets on simultaneous equations: elimination by adding or subtracting, multiplying first, substitution and word problems. 100 questions with answers.",
          "Eliminate one letter", "Then substitute back.",
          [("Add to eliminate", [cx(sim.one_add, 20)]), ("Subtract to eliminate", [cx(sim.one_sub, 20)]), ("Multiply first", [cx(sim.one_mult, 20)]),
           ("Substitution", [cx(sim.one_subst, 20)]), ("Mixed", [cx(sgsim.one_add, 5), cx(sgsim.one_sub, 5), cx(sgsim.one_mult, 5), cx(sgsim.one_subst, 5)])],
          ul(["Make the coefficients of one letter the same, then add or subtract the equations to eliminate it.", "Solve for the other letter, then substitute back to find the first one.",
              "Check the answer in both equations."]),
          [ex("x + y = 10, x − y = 4", ["Add: 2x = 14"], "x = 7, y = 3")],
          [["Adding when the signs are the same", "Subtract when the coefficients have the same sign."], ["Multiplying only one side", "Multiply every term."], ["Checking in one equation only", "Check both."]],
          [("How many solutions are there?", "Usually one pair (x, y)."), ("What is substitution?", "Replacing a letter by an expression equal to it."), ("Where are they used?", "Problems with two unknown prices or numbers.")]),

        U("change-of-subject-of-formula", "A", "Substitute values into formulae; make a given letter the subject of a formula.",
          "Change of Subject of a Formula", "Change of Subject",
          "Free JSS 3 maths worksheets on formulae: substituting values and changing the subject of a formula, including formulas with squares and fractions. 100 questions with answers.",
          "Undo the operations in reverse order", "Do the same to both sides.",
          [("Substitute", [cx(sub.one_sub, 10), cx(sub.one_sub_neg, 10)]), ("Change the subject", [cx(cs.one_step, 20)]), ("More formulas", [cx(sgcs.one_step, 20)]),
           ("Formulas from words", [cx(sub.one_context, 10), cx(sub.one_words, 10)]), ("Mixed practice", [cx(cs.one_step, 10), cx(sgcs.one_step, 10)])],
          ul(["The subject is the letter on its own on one side: in v = u + at, v is the subject.", "To change the subject, undo the operations on the new subject, doing the same to both sides.",
              "Example: v = u + at → v − u = at → t = (v − u) ÷ a."]),
          [ex("Make r the subject of A = πr²", ["r² = A ÷ π"], "r = √(A ÷ π)")],
          [["Undoing in the wrong order", "Undo + and − first."], ["Changing only one side", "Keep the balance."], ["Forgetting brackets", "t = (v − u) ÷ a, not v − u ÷ a."]],
          [("What is a formula?", "A rule that connects quantities, such as A = lb."), ("Why change the subject?", "To work out a different quantity."), ("What is the inverse of squaring?", "Square root.")]),

        U("linear-inequalities", "A", "Solve linear inequalities in one variable; show solutions on a number line; list integer solutions.",
          "Linear Inequalities", "Linear Inequalities",
          "Free JSS 3 maths worksheets on inequalities: reading inequality signs, number lines, listing integers and solving linear inequalities. 100 questions with answers.",
          "Solve like an equation", "Multiply or divide by a negative: flip the sign.",
          [("Number lines", [cx(ine.one_nl, 20)]), ("List the integers", [cx(ine.one_list, 20)]), ("Solve", [cx(ine.one_solve, 20)]),
           ("Harder inequalities", [cx(ine.one_hard, 20)]), ("Mixed", [cx(sgine.one_solve, 10), cx(sgine.one_list, 10)])],
          ul(["&lt; less than, &gt; greater than, ≤ less than or equal to, ≥ greater than or equal to.", "Solve an inequality like an equation: 3x + 2 &lt; 14 → 3x &lt; 12 → x &lt; 4.",
              "If you multiply or divide by a negative number, reverse the inequality sign."]),
          [ex("−2x ≥ 8", ["Divide by −2 and flip"], "x ≤ −4")],
          [["Not flipping the sign for negatives", "−x &gt; 3 means x &lt; −3."], ["Open and closed circles", "Closed for ≤ and ≥, open for &lt; and &gt;."], ["Including the end point wrongly", "x &lt; 4 does not include 4."]],
          [("What is an integer?", "A whole number: …, −2, −1, 0, 1, 2, …"), ("What does ≤ mean?", "Less than or equal to."), ("Can an inequality have many solutions?", "Yes, often infinitely many.")]),

        U("similar-shapes", "G", "Identify similar and congruent shapes; find scale factors; find missing lengths in similar triangles; enlarge shapes.",
          "Similar Shapes and Enlargement", "Similar Shapes",
          "Free JSS 3 maths worksheets on similarity: congruent and similar shapes, scale factors, missing sides in similar triangles and enlargement. 100 questions with answers.",
          "Similar: same shape, sides in the same ratio", "Scale factor = new length ÷ old length",
          [("Congruent shapes and reflections", [cx(sc.one_congruence, 11), cx(tr8.one_reflect, 9)]), ("Scale factor", [cx(sc.one_sf, 20)]), ("Similar triangles", [cx(sc.one_tri, 10), cx(sgsc.one_tri, 10)]),
           ("Are they similar?", [cx(sc.one_check, 20)]), ("Enlargement", [cx(tr8.one_enlarge, 20)])],
          ul(["Congruent shapes are exactly the same shape and size. Similar shapes have the same shape; their sides are in the same ratio.", "Scale factor = length on the new shape ÷ matching length on the old shape.",
              "In similar triangles the corresponding angles are equal."]),
          [ex("Sides 4 cm and 6 cm; matching side on the big triangle 10 cm", ["Scale factor 2.5"], "6 × 2.5 = 15 cm")],
          [["Matching the wrong sides", "Match sides opposite equal angles."], ["Adding instead of multiplying", "Multiply by the scale factor."], ["Thinking all rectangles are similar", "Check the ratio of the sides."]],
          [("Are all circles similar?", "Yes."), ("What is enlargement?", "Making a shape bigger or smaller by a scale factor."), ("Are congruent shapes similar?", "Yes, with scale factor 1.")]),

        U("trigonometry", "G", "Label the sides of a right-angled triangle; use sine, cosine and tangent to find sides and angles.",
          "Trigonometry: Sine, Cosine and Tangent", "Trigonometry",
          "Free JSS 3 maths worksheets on trigonometry: opposite, adjacent and hypotenuse, sin, cos and tan, finding sides and angles in right-angled triangles. 100 questions with answers.",
          "SOH CAH TOA", "sin = O/H, cos = A/H, tan = O/A",
          [("Label the sides", [cx(tg.one_label, 20)]), ("Find a side (multiply)", [cx(tg.one_side_mul, 20)]), ("Find a side (divide)", [cx(tg.one_side_div, 20)]),
           ("Find an angle", [cx(tg.one_angle, 20)]), ("Mixed", [cx(sgtg.one_side_mul, 7), cx(sgtg.one_side_div, 6), cx(sgtg.one_angle, 7)])],
          ul(["The hypotenuse is opposite the right angle. The opposite side is opposite the angle θ. The adjacent side is next to θ.",
              "sin θ = opposite ÷ hypotenuse, cos θ = adjacent ÷ hypotenuse, tan θ = opposite ÷ adjacent (SOH CAH TOA).", "To find an angle, use the inverse: θ = tan⁻¹(opposite ÷ adjacent)."]),
          [ex("Hypotenuse 10 cm, angle 30°, find the opposite side", ["sin 30° = 0.5"], "5 cm")],
          [["Mixing up adjacent and hypotenuse", "The hypotenuse is always the longest side."], ["Calculator in radians", "Use degrees."], ["Using sin to find an angle", "Use sin⁻¹."]],
          [("What is tan 45°?", "1."), ("Where is trigonometry used?", "In building, surveying and navigation."), ("Is sin ever bigger than 1?", "No, for a right-angled triangle.")]),

        U("area-and-volume-of-solids", "G", "Find the volume and surface area of cylinders, cones and spheres; solve problems with solids.",
          "Volume of Cylinders, Cones and Spheres", "Volume of Solids",
          "Free JSS 3 maths worksheets on mensuration of solids: volume of cylinders, cones and spheres, answers in terms of π, and problems. 100 questions with answers.",
          "Cone: ⅓πr²h, sphere: ⁴⁄₃πr³", "Cylinder: πr²h",
          [("Cylinders", [cx(vs.one_cyl, 10), cx(sgvs.one_cyl, 10)]), ("Cones", [cx(vs.one_cone, 10), cx(sgvs.one_cone, 10)]), ("Spheres", [cx(vs.one_sph, 10), cx(sgvs.one_sph, 10)]),
           ("In terms of π", [cx(vs.one_pi, 10), cx(sgvs.one_pi, 10)]), ("Mixed", [cx(vs.one_cyl, 7), cx(vs.one_cone, 7), cx(vs.one_sph, 6)])],
          ul(["Volume of a cylinder = πr²h.", "Volume of a cone = ⅓πr²h. It is one third of the cylinder with the same base and height.", "Volume of a sphere = ⁴⁄₃πr³."]),
          [ex("Cone with r = 3 cm, h = 7 cm (π = 22/7)", ["⅓ × 22/7 × 9 × 7"], "66 cm³")],
          [["Forgetting the ⅓ for a cone", "A cone is one third of a cylinder."], ["Using the diameter", "Halve it to get the radius."], ["Cubing the radius for a cylinder", "Cylinder uses r², sphere uses r³."]],
          [("What is a hemisphere?", "Half a sphere."), ("Which holds more, a cone or a cylinder of the same size?", "The cylinder, three times as much."), ("What units for volume?", "Cubic units like cm³.")]),

        U("arcs-and-sectors", "G", "Find the length of an arc and the area of a sector of a circle; find the perimeter of a sector.",
          "Arcs and Sectors of Circles", "Arcs and Sectors",
          "Free JSS 3 maths worksheets on circles: circumference and area, arc length, sector area and the perimeter of a sector. 100 questions with answers.",
          "Arc = θ/360 × 2πr", "Sector = θ/360 × πr²",
          [("Circumference and area", [cx(ci8.one_circ, 10), cx(ci8.one_area, 10)]), ("Arc length", [cx(arc.one_arc, 20)]), ("Sector area", [cx(arc.one_area, 20)]),
           ("Perimeter of a sector", [cx(arc.one_perim, 20)]), ("In terms of π", [cx(arc.one_pi, 20)])],
          ul(["An arc is part of the circumference. Arc length = θ ÷ 360 × 2πr.", "A sector is a slice of the circle. Sector area = θ ÷ 360 × πr².",
              "The perimeter of a sector = arc length + 2 radii."]),
          [ex("Sector of radius 7 cm and angle 90°", ["Arc = ¼ × 44 = 11 cm"], "Area = ¼ × 154 = 38.5 cm²")],
          [["Forgetting the two radii in the perimeter", "Add 2r to the arc."], ["Using 180° instead of 360°", "A full turn is 360°."], ["Using the diameter", "Use the radius."]],
          [("What is a semicircle?", "A sector with angle 180°."), ("What is a quadrant?", "A sector with angle 90°."), ("What is a chord?", "A straight line joining two points on a circle.")]),

        U("bearings-and-distances", "G", "Read and use three-figure bearings; find back bearings; solve problems on bearings and distances, angles of elevation and depression, and scale drawings.",
          "Bearings and Distances", "Bearings and Distances",
          "Free JSS 3 maths worksheets on bearings: three-figure bearings, back bearings, compass directions, angles of elevation and depression, and map scales. 100 questions with answers.",
          "Bearings: clockwise from north, three figures", "Back bearing = bearing ± 180°",
          [("Read bearings", [cx(br.one_read, 10), co(A.bearing_read, 10)]), ("Back bearings", [co(A.bearing_back, 20)]), ("Compass directions", [co(A.bearing_dir, 8), co(A.bearing_name, 8), co(A.bearing_turn, 4)]),
           ("Elevation and depression", [cx(sgbr.one_elev, 10), cx(sgbr.one_dep, 10)]), ("Map scales", [cx(sgms.one_actual, 10), cx(sgms.one_map, 10)])],
          ul(["A bearing is measured clockwise from north and written with three figures: 045°, 230°.", "The back bearing is the bearing for the return journey: add or subtract 180°.",
              "The angle of elevation is measured up from the horizontal; the angle of depression is measured down from the horizontal."]),
          [ex("Bearing of B from A is 065°", ["65 + 180"], "Bearing of A from B is 245°")],
          [["Measuring from east", "Always start from north."], ["Writing 65° instead of 065°", "Use three figures."], ["Mixing up elevation and depression", "Elevation looks up; depression looks down."]],
          [("What is the bearing of west?", "270°."), ("What is a scale of 1 : 50,000?", "1 cm on the map is 50,000 cm (0.5 km) on the ground."), ("Who uses bearings?", "Pilots, sailors and surveyors.")]),

        U("data-presentation", "S", "Present data in grouped frequency tables, pie charts and stem-and-leaf diagrams; read and interpret statistical diagrams.",
          "Data Presentation: Grouped Data, Pie Charts and Stem-and-Leaf", "Data Presentation",
          "Free JSS 3 maths worksheets on data presentation: grouped frequency tables, pie charts, stem-and-leaf diagrams and reading statistical diagrams. 100 questions with answers.",
          "Pie chart angle = f ÷ total × 360°", "Stem: tens, leaf: units",
          [("Grouped frequency tables", [cx(ft.one_grouped, 10), cx(sgfq.one_grouped, 10)]), ("Pie charts", [cx(ft.one_pie, 10), cx(sgfq.one_pie, 10)]), ("Read stem-and-leaf", [cx(sl.one_read, 20)]),
           ("Median and mode from stem-and-leaf", [cx(sl.one_medmode, 20)]), ("Range and mean", [cx(sl.one_rangemean, 20)])],
          ul(["A grouped frequency table puts data into classes such as 10–19, 20–29.", "In a pie chart, the angle for each group = frequency ÷ total × 360°.",
              "A stem-and-leaf diagram keeps the actual data: the stem is the tens digit and the leaf is the units digit."]),
          [ex("Stem 3 | leaves 2 5 8", ["32, 35, 38"], "three values in the 30s")],
          [["Forgetting the key", "Read the key: 3 | 2 means 32."], ["Using class width as frequency", "Read the frequency column."], ["Angles not adding to 360°", "Check the total."]],
          [("What is a class interval?", "A group of values, such as 20–29."), ("Why use a stem-and-leaf diagram?", "It shows the shape of data and keeps every value."), ("What is a histogram?", "A bar chart for grouped data with no gaps.")]),

        U("measures-of-central-tendency", "S", "Find the mean, median and mode of ungrouped and grouped data; find the range; compare data sets.",
          "Mean, Median and Mode of Grouped Data", "Measures of Central Tendency",
          "Free JSS 3 maths worksheets on averages: mean, median and mode from frequency tables, estimated mean of grouped data, missing values and comparing data. 100 questions with answers.",
          "Mean = Σfx ÷ Σf", "Grouped data: use the class mid-points.",
          [("Mean from a frequency table", [cx(ft.one_mean, 20)]), ("Median, mode and range", [cx(ft.one_mmr, 20)]), ("Grouped mean", [cx(sgfq.one_mean, 10), cx(sgfq.one_mmr, 10)]),
           ("Missing values", [cx(sgav.one_missing, 20)]), ("Compare data", [cx(sgav.one_compare, 10), cx(sgav.one_mode_range, 10)])],
          ul(["Mean from a table = Σfx ÷ Σf.", "For grouped data, use the mid-point of each class as x. The answer is an estimate.",
              "The median is the middle value; the mode is the most common value; the range is highest − lowest."]),
          [ex("Classes 10–19 (f 4), 20–29 (f 6)", ["Mid-points 14.5 and 24.5", "(58 + 147) ÷ 10"], "Estimated mean 20.5")],
          [["Using class limits instead of mid-points", "Use the mid-point."], ["Dividing by the number of classes", "Divide by Σf."], ["Thinking the estimate is exact", "Grouped data gives an estimate."]],
          [("Why is the grouped mean an estimate?", "We do not know the exact values in each class."), ("What is the modal class?", "The class with the highest frequency."), ("Which average ignores extreme values?", "The median.")]),

        U("probability", "S", "Find the probability of combined events using sample spaces, tree diagrams, Venn diagrams and two-way tables.",
          "Probability of Combined Events", "Probability",
          "Free JSS 3 maths worksheets on probability: two dice, coins and spinners, listing outcomes, Venn diagrams and two-way tables. 100 questions with answers.",
          "List all outcomes", "P(A and B) = P(A) × P(B) for independent events.",
          [("Two dice", [cx(pr8.one_dice, 20)]), ("Coins and spinners", [cx(pr8.one_coin_spinner, 20)]), ("Listing outcomes", [cx(pr8.one_list, 20)]),
           ("Venn diagrams", [cx(pr8.one_venn, 20)]), ("Two-way tables", [cx(pr8.one_twoway, 10), cx(pr7.one_not, 10)])],
          ul(["For two events, list all the outcomes in a table (sample space). Two dice give 36 outcomes.", "For independent events, P(A and B) = P(A) × P(B).",
              "In a Venn diagram or two-way table, count the outcomes in the region you need and divide by the total."]),
          [ex("Two coins: P(two heads)", ["HH, HT, TH, TT"], "1/4")],
          [["Counting 11 outcomes for two dice", "There are 6 × 6 = 36."], ["Adding when you should multiply", "And means multiply for independent events."], ["Using the wrong total", "Check the total in the table."]],
          [("What are independent events?", "Events where one does not affect the other."), ("What is a sample space?", "A list or table of all outcomes."), ("What is P(A) + P(not A)?", "1.")]),
    ]


if __name__ == "__main__":
    main("jss-3", "JSS 3", units, 160300)
