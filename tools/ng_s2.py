# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / SSS 2 (NERDC Senior Secondary School General Mathematics; WAEC and NECO syllabus).
  python3 tools/ng_s2.py [number …]      seed = 170200 + number, reused modules 1729NN
"""
from ng_unit import mod, co, cx, ul, U, main, example as ex
import re


def nopi(it):
    return "π" not in re.sub(r"<svg.*?</svg>", "", it["q"] + " ".join(it["c"]), flags=re.S) and "radian" not in it["q"]
import ng_sa as S
from ng_s1 import TH_S


def units():
    rd = mod("gen_uk_maths_y9_rounding_and_error_intervals", 172901)
    apx = mod("gen_in_maths_c10_arithmetic_progressions", 172902)
    sq = mod("gen_in_maths_c11_sequences_and_series", 172903)
    ukq = mod("gen_uk_maths_y9_arithmetic_and_geometric_sequences", 172904)
    uss = mod("gen_us_math_a2_sequences_and_series", 172905)
    qf = mod("gen_sg_maths_s3_quadratic_formula_and_completing_the_square", 172906)
    usq = mod("gen_us_math_a1_quadratic_formula_and_completing_the_square", 172907)
    inq = mod("gen_in_maths_c10_quadratic_equations", 172908)
    sim = mod("gen_uk_maths_y9_simultaneous_equations", 172909)
    ine = mod("gen_us_math_a1_multi_step_and_compound_inequalities", 172910)
    inin = mod("gen_in_maths_c11_linear_inequalities", 172911)
    sgin = mod("gen_sg_maths_s3_simultaneous_linear_inequalities", 172912)
    gin = mod("gen_us_math_a1_systems_of_linear_inequalities", 172913)
    af = mod("gen_sg_maths_s2_algebraic_fractions", 172914)
    re_ = mod("gen_us_math_a2_rational_expressions", 172915)
    sk = mod("gen_sg_maths_s3_sketching_quadratic_graphs", 172916)
    qg = mod("gen_uk_maths_y9_quadratic_graphs", 172917)
    gq = mod("gen_us_math_a1_graphing_quadratic_functions", 172918)
    ac = mod("gen_sg_maths_s3_angle_properties_of_circles", 172919)
    uca = mod("gen_us_math_ge_circle_angles_and_arcs", 172920)
    inc = mod("gen_in_maths_c10_circles", 172921)
    sym = mod("gen_sg_maths_s3_symmetry_properties_of_circles", 172922)
    scr = mod("gen_sg_maths_s3_sine_and_cosine_rules", 172923)
    lsc = mod("gen_us_math_ge_law_of_sines_and_cosines", 172924)
    gsc = mod("gen_us_math_a2_graphs_of_sine_and_cosine", 172925)
    uc = mod("gen_us_math_a2_unit_circle_and_radians", 172926)
    cf = mod("gen_sg_maths_s4_cumulative_frequency_and_box_plots", 172927)
    sd = mod("gen_sg_maths_s4_standard_deviation", 172928)
    ist = mod("gen_in_maths_c11_statistics", 172929)
    bx = mod("gen_us_math_a1_box_plots_and_standard_deviation", 172930)
    cp = mod("gen_sg_maths_s4_probability_of_combined_events", 172931)
    ucp = mod("gen_us_math_ge_conditional_probability", 172932)
    p3 = mod("gen_sg_maths_s4_problems_in_three_dimensions", 172933)
    be = mod("gen_sg_maths_s3_bearings_and_angles_of_elevation", 172934)

    return [
        U("approximation-and-percentage-error", "N", "Round numbers to decimal places and significant figures; find limits of accuracy; calculate percentage error.",
          "Approximation and Percentage Error", "Percentage Error",
          "Free SSS 2 maths worksheets on approximation: significant figures, decimal places, limits of accuracy and percentage error. 100 questions with answers.",
          "Percentage error = error ÷ actual × 100", "The greatest error is half of the unit used.",
          [("Significant figures", [cx(rd.one_sf_big, 10), cx(rd.one_small, 10)]), ("Limits of accuracy", [co(S.pe_limits, 20)]), ("Error intervals", [cx(rd.one_ei, 10), cx(rd.one_ei2, 10)]),
           ("Percentage error", [co(S.pe_basic, 12), co(S.pe_max, 8)]), ("Mixed problems", [cx(rd.one_ei2, 8), co(S.pe_limits, 6), cx(rd.one_sf_big, 6)])],
          ul(["Count significant figures from the first digit that is not zero.", "A value correct to the nearest unit can be up to half a unit too big or too small.",
              "Percentage error = (error ÷ actual value) × 100%."]),
          [ex("A length of 48 cm is measured as 50 cm", ["2 ÷ 48 × 100"], "4.17%")],
          [["Counting the zeros at the front", "0.0045 has 2 significant figures."], ["Dividing by the measured value", "Divide by the actual value."], ["Using the whole unit as the error", "The greatest error is half the unit."]],
          [("What is 0.03049 to 2 s.f.?", "0.030."), ("What are the limits of 6 cm to the nearest cm?", "5.5 cm and 6.5 cm."), ("Why is percentage error useful?", "It compares errors of different sizes fairly.")]),

        U("sequences-and-series", "A", "Find the nth term and the sum of arithmetic and geometric progressions; find means; sum to infinity; solve word problems.",
          "Arithmetic and Geometric Progressions", "Sequences and Series",
          "Free SSS 2 maths worksheets on sequences and series: AP and GP, nth term, sum of n terms, arithmetic and geometric means, sum to infinity and word problems. 100 questions with answers.",
          "AP: Tₙ = a + (n − 1)d", "GP: Tₙ = arⁿ⁻¹, Sₙ = a(rⁿ − 1)/(r − 1)",
          [("AP or GP?", [cx(ukq.one_type, 10), cx(apx.one_ap, 10)]), ("nth term of an AP", [cx(apx.one_nth, 12), cx(apx.one_ad, 8)]), ("Sum of an AP", [cx(apx.one_sum, 14), cx(uss.one_ar, 6)]),
           ("Geometric progressions", [cx(sq.one_nth, 8), cx(ukq.one_geo, 6), cx(uss.one_geo, 6)]), ("Means, sum to infinity and problems", [cx(sq.one_means, 6), cx(uss.one_inf, 6), cx(apx.one_word, 8)])],
          ul(["In an AP you add the same number d each time; in a GP you multiply by the same ratio r.", "AP: Sₙ = n/2 (2a + (n − 1)d). GP: Sₙ = a(rⁿ − 1)/(r − 1).",
              "When −1 &lt; r &lt; 1, the sum to infinity of a GP is a ÷ (1 − r)."]),
          [ex("3, 7, 11, … Find T₂₀", ["a = 3, d = 4", "3 + 19 × 4"], "79")],
          [["Using n instead of n − 1", "T₁ = a, so use (n − 1)d."], ["Finding d the wrong way round", "d = second term − first term."], ["Sum to infinity when |r| ≥ 1", "It only exists when −1 &lt; r &lt; 1."]],
          [("What is the arithmetic mean of 4 and 10?", "7."), ("What is the geometric mean of 4 and 9?", "6."), ("Is 2, 6, 18 an AP or a GP?", "A GP with r = 3.")]),

        U("completing-the-square-and-quadratic-formula", "A", "Solve quadratic equations by completing the square and by the formula; use the discriminant to describe the roots; solve word problems.",
          "Completing the Square and the Quadratic Formula", "Quadratic Formula",
          "Free SSS 2 maths worksheets on quadratic equations: completing the square, the quadratic formula, the discriminant and word problems. 100 questions with answers.",
          "x = (−b ± √(b² − 4ac)) ÷ 2a", "b² − 4ac tells how many real roots.",
          [("Completing the square", [cx(qf.one_cs, 12), cx(usq.one_complete, 8)]), ("The quadratic formula", [cx(inq.one_formula, 12), cx(usq.one_radical, 8)]),
           ("Answers to 2 decimal places", [cx(qf.one_dp, 20)]), ("The discriminant", [cx(usq.one_disc, 10), cx(inq.one_nature, 10)]), ("Word problems", [cx(inq.one_speed, 10), cx(qf.one_sub, 10)])],
          ul(["Write the equation as ax² + bx + c = 0 and read a, b and c with their signs.", "To complete the square, halve the coefficient of x and square it: x² + 6x = (x + 3)² − 9.",
              "b² − 4ac > 0: two roots; = 0: one repeated root; &lt; 0: no real roots."]),
          [ex("x² − 4x − 1 = 0", ["x = (4 ± √20) ÷ 2"], "x = 4.24 or −0.24")],
          [["Losing the sign of b", "−b with b = −4 gives +4."], ["Dividing only √ by 2a", "Divide the whole top by 2a."], ["Forgetting the ± sign", "There are usually two roots."]],
          [("What is the discriminant?", "b² − 4ac."), ("When are the roots equal?", "When b² − 4ac = 0."), ("Which method always works?", "The quadratic formula.")]),

        U("simultaneous-linear-and-quadratic-equations", "A", "Solve simultaneous linear equations; solve one linear and one quadratic equation together; solve word problems.",
          "Simultaneous Linear and Quadratic Equations", "Simultaneous Equations",
          "Free SSS 2 maths worksheets on simultaneous equations: elimination, substitution, one linear and one quadratic equation, and word problems. 100 questions with answers.",
          "Make y the subject, then substitute", "Each x gives its own y.",
          [("Elimination", [cx(sim.one_add, 10), cx(sim.one_sub, 10)]), ("Multiply first", [cx(sim.one_mult, 20)]), ("Substitution", [cx(sim.one_subst, 20)]),
           ("Linear and quadratic", [co(S.lq_solve, 20)]), ("Sum, product and circles", [co(S.lq_sum, 10), co(S.lq_line_circle, 10)])],
          ul(["Two linear equations: add or subtract them to remove one letter.", "One linear and one quadratic: make one letter the subject of the linear equation and put it into the quadratic.",
              "Solve the quadratic and find the matching value of the other letter for each root."]),
          [ex("y = x + 1 and y = x² − 1", ["x² − x − 2 = 0", "x = 2 or −1"], "(2, 3) and (−1, 0)")],
          [["Pairing the x and y values wrongly", "Work out y from each x."], ["Substituting into the quadratic", "Use the linear equation to find y."], ["Stopping at one root", "A line can meet a curve twice."]],
          [("How many solutions can a line and a parabola have?", "0, 1 or 2."), ("What does a solution mean on a graph?", "A point where the graphs cross."), ("Which method is best?", "Substitution when one equation is quadratic.")]),

        U("linear-inequalities", "A", "Solve linear inequalities in one variable; solve simultaneous inequalities; show solutions on a number line and on a graph; solve word problems.",
          "Linear Inequalities and Their Graphs", "Linear Inequalities",
          "Free SSS 2 maths worksheets on inequalities: solving linear inequalities, combined inequalities, number lines, graphs of regions and word problems. 100 questions with answers.",
          "Multiplying by a negative turns the sign round", "−2x > 6 gives x &lt; −3.",
          [("Solve the inequality", [cx(inin.one_solve, 12), cx(ine.one_hard, 8)]), ("Both sides", [cx(ine.one_both, 12), cx(inin.one_sides, 8)]),
           ("Combined inequalities", [cx(ine.one_and, 10), cx(sgin.one_and, 10)]), ("Graphs of regions", [cx(gin.one_point, 10), cx(gin.one_graph2, 10)]),
           ("Integer values and problems", [cx(sgin.one_pair, 10), cx(inin.one_set, 10)])],
          ul(["Solve an inequality like an equation.", "When you multiply or divide by a negative number, reverse the sign.",
              "On a graph, test a point such as (0, 0) to find which side of the line is the region."]),
          [ex("3 − 2x ≤ 9", ["−2x ≤ 6"], "x ≥ −3")],
          [["Not turning the sign", "Turn it when dividing by a negative."], ["Shading the wrong side", "Test a point."], ["Using a solid line for &lt;", "&lt; and > use a broken line."]],
          [("What does ≤ mean?", "Less than or equal to."), ("What integers satisfy −2 &lt; x ≤ 2?", "−1, 0, 1, 2."), ("What is linear programming?", "Finding the best value in a region bounded by inequalities.")]),

        U("algebraic-fractions", "A", "Simplify algebraic fractions; multiply, divide, add and subtract algebraic fractions; solve equations with algebraic fractions.",
          "Algebraic Fractions", "Algebraic Fractions",
          "Free SSS 2 maths worksheets on algebraic fractions: simplifying by factorising, multiplying and dividing, adding and subtracting, and equations. 100 questions with answers.",
          "Factorise first, then cancel", "Cancel factors, never single terms.",
          [("Simplify", [cx(af.one_simp, 12), cx(re_.one_simp, 8)]), ("Multiply and divide", [cx(af.one_md, 12), cx(re_.one_md, 8)]),
           ("Add and subtract", [cx(af.one_num, 12), cx(re_.one_add, 8)]), ("Equations with fractions", [cx(af.one_lin, 20)]), ("Mixed questions", [cx(af.one_mix, 14), cx(re_.one_cx, 6)])],
          ul(["Factorise the top and bottom, then cancel common factors.", "To divide, multiply by the reciprocal of the second fraction.",
              "To add or subtract, use a common denominator."]),
          [ex("(x² − 9) ÷ (x + 3)", ["(x − 3)(x + 3) ÷ (x + 3)"], "x − 3")],
          [["Cancelling terms: (x + 3)/3 = x", "Only factors cancel."], ["Not using a common denominator", "1/x + 1/y = (y + x)/xy."], ["Forgetting the values that make the bottom 0", "The fraction is undefined there."]],
          [("When is a fraction undefined?", "When its denominator is 0."), ("What is 1/x + 2/x?", "3/x."), ("How do I solve an equation with fractions?", "Multiply both sides by the LCM of the denominators.")]),

        U("graphs-of-quadratic-functions", "A", "Draw and read graphs of quadratic functions; find the roots, turning point and axis of symmetry; use graphs to solve equations.",
          "Graphs of Quadratic Functions", "Quadratic Graphs",
          "Free SSS 2 maths worksheets on quadratic graphs: tables of values, roots, turning points, axis of symmetry and solving equations from graphs. 100 questions with answers.",
          "The roots are where the curve cuts the x-axis", "Axis of symmetry: x = −b ÷ 2a",
          [("Tables of values", [cx(qg.one_table, 20)]), ("Read the graph", [cx(qg.one_read, 8), cx(sk.one_match, 12)]), ("Turning points", [cx(sk.one_min, 10), cx(sk.one_max, 10)]),
           ("Roots and symmetry", [cx(sk.one_roots, 10), cx(gq.one_feature, 10)]), ("Solve using the graph", [cx(qg.one_solve, 10), cx(sk.one_graphical, 10)])],
          ul(["Make a table of values and plot the points with a smooth curve.", "If a > 0 the curve has a minimum; if a &lt; 0 it has a maximum.",
              "To solve ax² + bx + c = k, draw y = k and read the x-values where it meets the curve."]),
          [ex("y = x² − 4x + 3", ["Roots x = 1 and 3", "x = (1 + 3) ÷ 2"], "Turning point (2, −1)")],
          [["Joining points with straight lines", "Draw a smooth curve."], ["Squaring a negative wrongly", "(−3)² = 9."], ["Reading y instead of x for roots", "Roots are x-values on the x-axis."]],
          [("What is the shape of a quadratic graph?", "A parabola."), ("What is the y-intercept of y = x² + 2x − 5?", "−5."), ("How many roots can it have?", "0, 1 or 2.")]),

        U("circle-theorems", "G", "Use the angle properties of circles: angle at the centre, angles in the same segment, angle in a semicircle and cyclic quadrilaterals.",
          "Circle Theorems: Angles in a Circle", "Circle Theorems",
          "Free SSS 2 maths worksheets on circle theorems: angle at the centre, same segment, semicircle and cyclic quadrilaterals. 100 questions with answers.",
          "Angle at the centre = 2 × angle at the circumference", "Opposite angles of a cyclic quadrilateral add to 180°.",
          [("Angle at the centre", [cx(ac.one_centre, 14), cx(uca.one_central, 6)]), ("Same segment", [cx(ac.one_same, 14), cx(uca.one_insc, 6)]), ("Angle in a semicircle", [cx(ac.one_semi, 20)]),
           ("Cyclic quadrilaterals", [cx(ac.one_cyc, 14), cx(uca.one_quad, 6)]), ("Mixed circle problems", [cx(ac.one_mix, 20)])],
          ul(["The angle at the centre is twice the angle at the circumference standing on the same arc.", "Angles in the same segment are equal; the angle in a semicircle is 90°.",
              "Opposite angles of a cyclic quadrilateral add up to 180°."]),
          [ex("Angle at the circumference = 35°", ["2 × 35°"], "Angle at the centre = 70°")],
          [["Halving instead of doubling", "The centre angle is the bigger one."], ["Using the wrong arc", "Both angles must stand on the same arc."], ["Calling any quadrilateral cyclic", "All four vertices must be on the circle."]],
          [("What is a cyclic quadrilateral?", "One with all four corners on a circle."), ("What is the angle in a semicircle?", "90°."), ("What is an exterior angle of a cyclic quadrilateral equal to?", "The interior opposite angle.")]),

        U("chords-and-tangents", "G", "Use the properties of chords and tangents: perpendicular from the centre, equal chords, tangent and radius, tangents from a point, alternate segment.",
          "Chords and Tangents of a Circle", "Chords and Tangents",
          "Free SSS 2 maths worksheets on chords and tangents: perpendicular bisectors of chords, equal chords, tangents from an external point and lengths. 100 questions with answers.",
          "A tangent meets the radius at 90°", "Two tangents from one point are equal.",
          [("Perpendicular from the centre", [cx(sym.one_chord, 8), cx(sym.one_dist, 12)]), ("Equal chords", [cx(sym.one_equal, 20)]), ("Tangent and radius", [cx(sym.one_tan, 12), cx(inc.one_len, 8)]),
           ("Tangents from a point", [cx(inc.one_circ, 12), cx(uca.one_tan, 8)]), ("Chord and tangent problems", [cx(sym.one_prob, 10), cx(inc.one_prob, 10)])],
          ul(["The perpendicular from the centre to a chord cuts the chord in half.", "A tangent is at right angles to the radius at the point of contact.",
              "The two tangents from an outside point are equal in length."]),
          [ex("r = 5 cm, distance of chord from centre 3 cm", ["Half chord = √(25 − 9) = 4"], "Chord = 8 cm")],
          [["Forgetting to double the half chord", "The perpendicular gives half the chord."], ["Missing the right angle", "Radius ⟂ tangent."], ["Using Pythagoras without a right angle", "Find the 90° first."]],
          [("What is a tangent?", "A line that touches a circle at one point."), ("Do equal chords lie equally far from the centre?", "Yes."), ("What is the alternate segment theorem?", "The angle between a tangent and a chord equals the angle in the alternate segment.")]),

        U("sine-and-cosine-rules", "T", "Use the sine rule and cosine rule to find sides and angles; find the area of a triangle using ½ab sin C; solve bearing problems.",
          "The Sine Rule and the Cosine Rule", "Sine and Cosine Rules",
          "Free SSS 2 maths worksheets on the sine rule, the cosine rule, the area ½ab sin C and bearing problems. 100 questions with answers.",
          "a/sin A = b/sin B = c/sin C", "a² = b² + c² − 2bc cos A",
          [("Sine rule: sides", [cx(lsc.one_ls_side, 20)]), ("Sine rule: angles", [cx(lsc.one_ls_ang, 20)]), ("Cosine rule", [cx(lsc.one_lc_side, 14), cx(scr.one_obtuse, 6)]),
           ("Area of a triangle", [cx(lsc.one_area, 20)]), ("Problems and bearings", [cx(scr.one_prob, 12), cx(be.one_prob, 8)])],
          ul(["Use the sine rule when you know a side and its opposite angle.", "Use the cosine rule when you know two sides and the angle between them, or all three sides.",
              "Area = ½ab sin C, where C is the angle between sides a and b."]),
          [ex("b = 8, c = 5, A = 60°", ["a² = 64 + 25 − 80 × 0.5"], "a = 7")],
          [["Using the sine rule with no opposite pair", "Use the cosine rule."], ["Forgetting 2bc cos A", "a² = b² + c² − 2bc cos A."], ["Using the wrong angle in ½ab sin C", "Use the angle between a and b."]],
          [("When is the sine rule ambiguous?", "When you are given two sides and a non-included angle."), ("What is cos 90°?", "0, so the cosine rule becomes Pythagoras."), ("Can I use these rules in any triangle?", "Yes, not only right-angled ones.")]),

        U("trigonometric-graphs-and-angles", "T", "Find sine, cosine and tangent of angles from 0° to 360°; use the signs in the four quadrants; draw and read graphs of y = sin x and y = cos x; solve simple trigonometric equations.",
          "Trigonometric Ratios of Any Angle and Their Graphs", "Trigonometric Graphs",
          "Free SSS 2 maths worksheets on trigonometry from 0° to 360°: reference angles, signs in the quadrants, exact values and graphs of sine and cosine. 100 questions with answers.",
          "All Students Take Calculus", "Quadrant 1 all +, 2 sin +, 3 tan +, 4 cos +",
          [("Quadrants and reference angles", [co(S.t_quadrant, 12), cx(uc.one_ref, 8, nopi)]), ("Signs in the quadrants", [co(S.t_sign, 20)]), ("Exact values", [co(S.t_value, 20)]),
           ("Amplitude, period, maximum and minimum", [co(S.t_amp, 12), co(S.t_maxmin, 8)]), ("Solve trigonometric equations", [co(S.t_solve, 14), co(S.t_maxmin, 6)])],
          ul(["For an angle between 90° and 360°, find the reference angle with the x-axis.", "Use the quadrant to give the sign: sin 150° = sin 30° = 1/2, cos 150° = −cos 30°.",
              "y = sin x and y = cos x repeat every 360° and stay between −1 and 1."]),
          [ex("cos 240°", ["Reference angle 60°, quadrant 3"], "−1/2")],
          [["Using the angle with the y-axis", "The reference angle is with the x-axis."], ["Wrong sign", "Use the quadrant rule."], ["Thinking sin x can be 2", "Sine is always between −1 and 1."]],
          [("What is sin 180°?", "0."), ("What is the period of y = sin x?", "360°."), ("What is the maximum of y = 3 sin x?", "3.")]),

        U("bearings-and-distances", "T", "Solve problems on bearings and distances in two and three dimensions using Pythagoras, trigonometric ratios and the sine and cosine rules.",
          "Bearings, Distances and 3D Problems", "Bearings and Distances",
          "Free SSS 2 maths worksheets on bearings and distances: journeys on bearings, distances north and east, and problems in three dimensions. 100 questions with answers.",
          "Draw the north line at every point", "Then use a triangle.",
          [("Bearing journeys", [cx(be.one_prob, 20)]), ("3D diagonals", [cx(p3.one_diag, 20)]), ("Angle with a plane", [cx(p3.one_lp, 20)]), ("Pyramids", [cx(p3.one_pyr, 20)]),
           ("Elevation and bearings in 3D", [cx(p3.one_elev, 10), cx(p3.one_brg, 10)])],
          ul(["Sketch the journey with a north line at each turning point.", "Use alternate angles to find the angle inside the triangle.",
              "In 3D, find a right-angled triangle that contains the length you want."]),
          [ex("Cuboid 3 × 4 × 12", ["√(9 + 16 + 144)"], "Diagonal 13")],
          [["Forgetting the north line at the second point", "Draw one at every point."], ["Using a non-right-angled triangle with SOH CAH TOA", "Use the sine or cosine rule."], ["Mixing up the 3D triangle", "Draw it separately."]],
          [("What is a bearing?", "An angle clockwise from north, with three figures."), ("What is the angle between a line and a plane?", "The angle between the line and its projection on the plane."), ("What is the space diagonal of a cube of side a?", "a√3.")]),

        U("cumulative-frequency", "S", "Draw and read cumulative frequency curves (ogives); find the median, quartiles, interquartile range and percentiles; draw box plots.",
          "Cumulative Frequency, Quartiles and Percentiles", "Cumulative Frequency",
          "Free SSS 2 maths worksheets on cumulative frequency: ogives, median, quartiles, interquartile range, percentiles and box plots. 100 questions with answers.",
          "Median at n/2 on the ogive", "IQR = Q₃ − Q₁",
          [("Cumulative frequency tables", [cx(cf.one_table, 20)]), ("Read the ogive", [cx(cf.one_curve, 20)]), ("Quartiles from a list", [cx(cf.one_list, 20)]),
           ("Box plots", [cx(cf.one_box, 12), cx(bx.one_five, 8)]), ("Compare distributions", [cx(cf.one_cmp, 14), cx(bx.one_box, 6)])],
          ul(["Add the frequencies as you go to make the cumulative frequency.", "Plot each cumulative frequency at the upper class boundary and join with a smooth curve.",
              "Read the median at n/2, Q₁ at n/4 and Q₃ at 3n/4."]),
          [ex("n = 80 on an ogive", ["Median at 40"], "Q₁ at 20, Q₃ at 60")],
          [["Plotting at the class mark", "Plot at the upper boundary."], ["IQR = Q₃ + Q₁", "IQR = Q₃ − Q₁."], ["Reading the y-axis value as the answer", "Read across to the curve, then down."]],
          [("What does the IQR show?", "The spread of the middle half of the data."), ("What is the 90th percentile?", "The value below which 90% of the data lies."), ("What is an ogive?", "A cumulative frequency curve.")]),

        U("measures-of-dispersion", "S", "Find the range, mean deviation, variance and standard deviation of ungrouped and grouped data; compare spreads.",
          "Range, Variance and Standard Deviation", "Measures of Dispersion",
          "Free SSS 2 maths worksheets on measures of dispersion: range, mean deviation, variance and standard deviation for lists and frequency tables. 100 questions with answers.",
          "SD = √(Σ(x − x̄)² ÷ n)", "A bigger SD means more spread.",
          [("Standard deviation of a list", [cx(sd.one_list, 20)]), ("Using Σx and Σx²", [cx(sd.one_sums, 20)]), ("Grouped data", [cx(sd.one_group, 12), cx(ist.one_var, 8)]),
           ("Mean deviation", [cx(ist.one_md, 10), cx(ist.one_mdmed, 10)]), ("Changing and comparing data", [cx(sd.one_change, 10), cx(sd.one_cmp, 10)])],
          ul(["Range = highest − lowest.", "Variance = mean of the squared deviations; standard deviation = √variance.",
              "Adding the same number to every value does not change the SD; multiplying every value by k multiplies the SD by k."]),
          [ex("2, 4, 6", ["Mean 4", "Deviations −2, 0, 2", "(4 + 0 + 4) ÷ 3"], "SD = √(8/3) ≈ 1.63")],
          [["Forgetting to square root the variance", "SD = √variance."], ["Using Σx² ÷ n − x̄ wrongly", "Square the mean: Σx²/n − x̄²."], ["Ignoring the signs of deviations", "Square them so they are all positive."]],
          [("What does a small SD mean?", "The data is close to the mean."), ("Is SD affected by outliers?", "Yes."), ("What is the mean deviation?", "The mean of the distances from the mean.")]),

        U("probability-of-combined-events", "S", "Use the addition and multiplication rules; find probabilities of independent and mutually exclusive events; use tree diagrams, tables and conditional probability.",
          "Probability: Combined Events and Tree Diagrams", "Combined Probability",
          "Free SSS 2 maths worksheets on probability: addition and multiplication rules, with and without replacement, tree diagrams, two-way tables and conditional probability. 100 questions with answers.",
          "And: multiply. Or: add.", "P(A or B) = P(A) + P(B) − P(A and B)",
          [("Rules of probability", [cx(cp.one_rules, 14), cx(ucp.one_add, 6)]), ("With replacement", [cx(cp.one_with, 20)]), ("Without replacement", [cx(cp.one_without, 14), cx(ucp.one_draw, 6)]),
           ("Independent events and tables", [cx(ucp.one_ind, 10), cx(ucp.one_table, 10)]), ("Probability problems", [cx(cp.one_prob, 20)])],
          ul(["Independent events: P(A and B) = P(A) × P(B).", "Mutually exclusive events: P(A or B) = P(A) + P(B).",
              "Without replacement, the second probability has one less in the total."]),
          [ex("Two coins", ["1/2 × 1/2"], "P(two heads) = 1/4")],
          [["Adding when the events happen together", "“And” means multiply."], ["Not changing the total without replacement", "Take 1 from the top and bottom."], ["Counting both orders once", "Red then blue and blue then red are different."]],
          [("What does independent mean?", "One event does not change the chance of the other."), ("What is a tree diagram for?", "Showing two or more events step by step."), ("What is P(A | B)?", "The probability of A given that B has happened.")]),
    ]


if __name__ == "__main__":
    main("sss-2", "SSS 2", units, 170200, th=TH_S)
