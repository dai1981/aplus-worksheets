# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / SSS 3 (NERDC Senior Secondary School General Mathematics; the year of WAEC and NECO).
  python3 tools/ng_s3.py [number …]      seed = 170300 + number, reused modules 1739NN
"""
from ng_unit import mod, co, cx, ul, U, main, example as ex
import ng_p5a as A
import ng_ja as J
import ng_sa as S
from ng_s1 import TH_S


def units():
    rad = mod("gen_us_math_a1_simplifying_radicals", 173901)
    ns = mod("gen_in_maths_c9_number_systems", 173902)
    mo = mod("gen_us_math_pc_matrix_operations", 173903)
    dt = mod("gen_us_math_pc_determinants_and_inverse_matrices", 173904)
    sgm = mod("gen_sg_maths_s4_matrices", 173905)
    inm = mod("gen_in_maths_c12_matrices", 173906)
    cg = mod("gen_sg_maths_s3_coordinate_geometry", 173907)
    dm = mod("gen_us_math_ge_distance_and_midpoint_formulas", 173908)
    sl = mod("gen_in_maths_c11_straight_lines", 173909)
    pp = mod("gen_us_math_ge_slopes_of_parallel_and_perpendicular_lines", 173910)
    ld = mod("gen_in_maths_c11_limits_and_derivatives", 173911)
    ad = mod("gen_in_maths_c12_application_of_derivatives", 173912)
    ig = mod("gen_in_maths_c12_integrals", 173913)
    ai = mod("gen_in_maths_c12_application_of_integrals", 173914)
    vc = mod("gen_sg_maths_s4_vectors", 173915)
    vg = mod("gen_sg_maths_s4_vector_geometry", 173916)
    pv = mod("gen_us_math_pc_vectors", 173917)
    vo = mod("gen_us_math_pc_vector_operations", 173918)
    rt = mod("gen_us_math_ge_rigid_transformations", 173919)
    tr8 = mod("gen_uk_maths_y8_transformations", 173920)
    pc = mod("gen_us_math_pc_permutations_and_combinations", 173921)
    ipc = mod("gen_in_maths_c11_permutations_and_combinations", 173922)

    return [
        U("surds", "N", "Simplify surds; add, subtract, multiply and divide surds; rationalise the denominator.",
          "Surds: Simplifying and Rationalising", "Surds",
          "Free SSS 3 maths worksheets on surds: simplifying, adding and subtracting, multiplying, and rationalising the denominator. 100 questions with answers.",
          "√ab = √a × √b", "Rationalise: multiply top and bottom by the surd.",
          [("Simplify surds", [cx(rad.one_simp, 20)]), ("Add and subtract", [cx(rad.one_add, 20)]), ("Multiply surds", [cx(rad.one_mul, 20)]),
           ("Rationalise the denominator", [cx(ns.one_rat, 20)]), ("Operations with surds", [cx(ns.one_ops, 12), cx(rad.one_var, 8)])],
          ul(["Find the biggest square factor: √72 = √36 × √2 = 6√2.", "Only like surds can be added: 3√2 + 5√2 = 8√2.",
              "To rationalise 1/(a + √b), multiply top and bottom by a − √b."]),
          [ex("√50 + √18", ["5√2 + 3√2"], "8√2"), ex("6/√3", ["× √3/√3"], "2√3")],
          [["√(a + b) = √a + √b", "That is false: √(9 + 16) = 5, not 7."], ["Adding unlike surds", "√2 + √3 cannot be simplified."], ["Forgetting to multiply the top when rationalising", "Multiply top and bottom."]],
          [("What is a surd?", "A root that is not a whole number, like √2."), ("What is √3 × √3?", "3."), ("What is the conjugate of 2 + √5?", "2 − √5.")]),

        U("matrices-and-determinants", "A", "Add, subtract and multiply matrices; find the determinant and inverse of a 2 × 2 matrix; solve simultaneous equations with matrices.",
          "Matrices and Determinants", "Matrices",
          "Free SSS 3 maths worksheets on matrices: order, addition, scalar and matrix multiplication, determinants, inverse matrices and solving equations. 100 questions with answers.",
          "det of (a b; c d) = ad − bc", "Inverse = 1/det × (d −b; −c a)",
          [("Order and equal matrices", [cx(mo.one_dim, 10), cx(inm.one_eq, 10)]), ("Add, subtract and scalar", [cx(mo.one_add, 10), cx(mo.one_scal, 10)]),
           ("Multiply matrices", [cx(mo.one_mul, 14), cx(inm.one_trans, 6)]), ("Determinants", [cx(dt.one_d2, 14), cx(dt.one_d3, 6)]), ("Inverse and equations", [cx(dt.one_inv, 10), cx(dt.one_sys, 10)])],
          ul(["A matrix of order m × n has m rows and n columns. Add only matrices of the same order.", "To multiply, take row × column: multiply in pairs and add.",
              "For a 2 × 2 matrix, the determinant is ad − bc. If it is 0, there is no inverse."]),
          [ex("det (3 2; 1 4)", ["3 × 4 − 2 × 1"], "10")],
          [["Multiplying matching entries", "Use row × column."], ["Thinking AB = BA", "Matrix multiplication is not commutative."], ["Forgetting to swap a and d in the inverse", "Swap a and d, change the signs of b and c."]],
          [("When can two matrices be multiplied?", "When the columns of the first = the rows of the second."), ("What is a singular matrix?", "One with determinant 0."), ("What is the identity matrix?", "(1 0; 0 1); IA = A.")]),

        U("coordinate-geometry", "G", "Find the distance between two points, the midpoint and the gradient of a line; find the equation of a straight line; use parallel and perpendicular lines.",
          "Coordinate Geometry of Straight Lines", "Coordinate Geometry",
          "Free SSS 3 maths worksheets on coordinate geometry: distance, midpoint, gradient, equation of a line, parallel and perpendicular lines. 100 questions with answers.",
          "Gradient = (y₂ − y₁) ÷ (x₂ − x₁)", "Perpendicular gradients multiply to −1.",
          [("Distance between points", [cx(cg.one_len, 10), cx(dm.one_dist, 10)]), ("Midpoints", [cx(dm.one_mid, 20)]), ("Gradient", [cx(cg.one_grad, 12), cx(sl.one_slope, 8)]),
           ("Equation of a line", [cx(cg.one_eq, 10), cx(sl.one_eq, 10)]), ("Parallel and perpendicular lines", [cx(pp.one_par, 8), cx(pp.one_perp, 8), cx(cg.one_geo, 4)])],
          ul(["Distance = √((x₂ − x₁)² + (y₂ − y₁)²). Midpoint = ((x₁ + x₂)/2, (y₁ + y₂)/2).", "The equation of a line is y = mx + c, or y − y₁ = m(x − x₁) through (x₁, y₁).",
              "Parallel lines have equal gradients; perpendicular gradients multiply to −1."]),
          [ex("A(1, 2), B(7, 10)", ["Gradient 8/6", "Distance √(36 + 64)"], "m = 4/3, AB = 10")],
          [["Subtracting in a different order on top and bottom", "Keep the same order."], ["Forgetting the negative reciprocal", "Perpendicular to 2 is −1/2."], ["Adding in the distance formula", "Subtract the coordinates."]],
          [("What is the gradient of a horizontal line?", "0."), ("What is the y-intercept?", "Where the line meets the y-axis (x = 0)."), ("Are y = 3x + 1 and y = 3x − 4 parallel?", "Yes.")]),

        U("differentiation", "C", "Find limits; differentiate from first principles; differentiate polynomials and simple functions using the power rule and the chain rule.",
          "Differentiation: Limits and Rules", "Differentiation",
          "Free SSS 3 maths worksheets on introductory calculus: limits, first principles, the power rule, derivatives at a point and the chain rule. 100 questions with answers.",
          "d/dx (xⁿ) = nxⁿ⁻¹", "Multiply by the power, then take 1 from it.",
          [("Limits", [cx(ld.lim_sub, 10), cx(ld.lim_fact, 10)]), ("First principles", [cx(ld.dfirst, 20)]), ("The power rule", [co(S.d_power, 12), cx(ld.dpoly, 8)]),
           ("Gradient at a point", [co(S.d_point, 20)]), ("Negative powers and the chain rule", [co(S.d_rule, 20)])],
          ul(["dy/dx is the gradient of the curve at any point.", "d/dx(axⁿ) = naxⁿ⁻¹; the derivative of a constant is 0.",
              "To find the gradient at a point, put its x-value into dy/dx."]),
          [ex("y = 3x² − 5x + 2", ["6x − 5"], "dy/dx = 6x − 5")],
          [["Not taking 1 from the power", "x³ → 3x²."], ["Keeping the constant", "A constant differentiates to 0."], ["Putting x into y instead of dy/dx", "Gradient uses dy/dx."]],
          [("What is the derivative of 5x?", "5."), ("What does dy/dx = 0 mean?", "The tangent is horizontal: a turning point."), ("What is first principles?", "Finding the derivative as the limit of (f(x + h) − f(x)) ÷ h.")]),

        U("applications-of-differentiation", "C", "Find turning points and say whether they are maxima or minima; find equations of tangents; solve rate of change, velocity and optimisation problems.",
          "Applications of Differentiation", "Applications of Calculus",
          "Free SSS 3 maths worksheets on applications of differentiation: turning points, maxima and minima, tangents, velocity and acceleration, and rates of change. 100 questions with answers.",
          "At a turning point dy/dx = 0", "d²y/dx² > 0: minimum; &lt; 0: maximum",
          [("Turning points", [co(S.d_stat, 20)]), ("Equation of a tangent", [co(S.d_tangent, 20)]), ("Velocity and acceleration", [co(S.d_motion, 20)]),
           ("Increasing and decreasing", [cx(ad.one_incr, 12), cx(ad.one_ext, 8)]), ("Rates and optimisation", [cx(ad.one_rate, 8), cx(ad.one_abs, 8), cx(ad.one_opt, 4)])],
          ul(["Set dy/dx = 0 and solve to find the x-values of the turning points.", "Use the second derivative: positive means a minimum, negative means a maximum.",
              "If s is distance, v = ds/dt is velocity and a = dv/dt is acceleration."]),
          [ex("y = x² − 6x + 5", ["2x − 6 = 0, x = 3", "y = −4"], "Minimum at (3, −4)")],
          [["Giving only x for a turning point", "Find y too."], ["Mixing up maximum and minimum", "Check the sign of d²y/dx²."], ["Using the curve’s y for the tangent gradient", "Gradient = dy/dx at that point."]],
          [("What is a stationary point?", "A point where dy/dx = 0."), ("What is velocity when the body stops?", "0."), ("How do I find a maximum area?", "Write the area as a function, differentiate and set it to 0.")]),

        U("integration", "C", "Integrate polynomials; evaluate definite integrals; find the area under a curve; find a curve from its gradient.",
          "Integration and Area under a Curve", "Integration",
          "Free SSS 3 maths worksheets on integration: indefinite integrals, the constant c, definite integrals, area under a curve and finding a curve from its gradient. 100 questions with answers.",
          "∫xⁿ dx = xⁿ⁺¹/(n + 1) + c", "Add 1 to the power and divide by it.",
          [("Indefinite integrals", [co(S.i_power, 14), cx(ig.one_power, 6)]), ("Definite integrals", [co(S.i_def, 14), cx(ig.one_def, 6)]), ("Area under a curve", [co(S.i_area, 12), cx(ai.one_line, 8)]),
           ("Finding the curve", [co(S.i_curve, 20)]), ("Integration problems", [cx(ig.one_std, 8), cx(ai.one_par, 6), co(S.i_def, 6)])],
          ul(["Integration is the reverse of differentiation.", "For an indefinite integral, add the constant c.",
              "For a definite integral, integrate, put in the top limit, then subtract the value at the bottom limit."]),
          [ex("∫₁³ 2x dx", ["[x²] from 1 to 3", "9 − 1"], "8")],
          [["Forgetting + c", "Every indefinite integral needs + c."], ["Multiplying by the new power", "Divide by it."], ["Subtracting in the wrong order", "Top limit minus bottom limit."]],
          [("What is ∫5 dx?", "5x + c."), ("What does a definite integral give?", "The area under the curve (above the x-axis)."), ("Why is there a constant c?", "Many curves have the same gradient; c picks one of them.")]),

        U("longitude-and-latitude", "M", "Find differences in latitude and longitude; find distances along meridians and parallels of latitude; find the radius of a parallel; solve time and longitude problems.",
          "Longitude and Latitude: The Earth as a Sphere", "Longitude and Latitude",
          "Free SSS 3 maths worksheets on longitude and latitude: difference in longitude, distances along a meridian and a parallel of latitude, radius of a parallel and local time. 100 questions with answers.",
          "Along a parallel: θ/360 × 2πR cos α", "Along a meridian: θ/360 × 2πR",
          [("Difference in longitude", [co(S.ll_diff, 20)]), ("Along a meridian", [co(S.ll_meridian, 20)]), ("Radius of a parallel", [co(S.ll_radius, 3), co(S.ll_parallel, 17)]),
           ("Along a parallel", [co(S.ll_parallel, 20)]), ("Longitude and time", [co(S.ll_time, 20)])],
          ul(["Lines of latitude run east–west; lines of longitude (meridians) run north–south.", "On the same meridian, distance = (difference in latitude)/360 × 2πR.",
              "On a parallel of latitude α, the radius is R cos α, so distance = θ/360 × 2πR cos α."]),
          [ex("15°E and 45°W", ["One E, one W: add"], "Difference 60°")],
          [["Subtracting when one is east and one is west", "Add them."], ["Using R on a parallel", "Use R cos α."], ["Moving the clock the wrong way", "East is ahead; west is behind."]],
          [("What is the radius of the earth?", "About 6,400 km."), ("What is the equator?", "Latitude 0°."), ("How many hours is 15° of longitude?", "1 hour.")]),

        U("vectors", "V", "Use column vectors; add, subtract and multiply vectors by scalars; find magnitude and direction; use position vectors and vector geometry.",
          "Vectors in a Plane", "Vectors",
          "Free SSS 3 maths worksheets on vectors: column vectors, addition and subtraction, scalar multiples, magnitude, position vectors and vector geometry. 100 questions with answers.",
          "|(x, y)| = √(x² + y²)", "AB = OB − OA",
          [("Column vectors", [cx(vc.one_grid, 20)]), ("Add, subtract and multiply", [cx(vc.one_ops, 12), cx(vo.one_add, 8)]), ("Magnitude and direction", [cx(vc.one_mag, 12), cx(pv.one_mag, 8)]),
           ("Position vectors", [cx(vc.one_pos, 12), cx(vc.one_par, 8)]), ("Vector geometry", [cx(vg.one_basic, 10), cx(vg.one_ratio, 10)])],
          ul(["A vector has size and direction; a column vector shows the move across and up.", "Add vectors by adding the tops and bottoms.",
              "The magnitude is the length: |(3, 4)| = 5."]),
          [ex("a = (2, 5), b = (−1, 3)", ["(2 − 1, 5 + 3)"], "a + b = (1, 8)")],
          [["Writing a vector as a fraction", "A column vector has no line."], ["AB = OA − OB", "AB = OB − OA."], ["Forgetting the square root in the magnitude", "|v| = √(x² + y²)."]],
          [("What is a unit vector?", "A vector of length 1."), ("When are two vectors parallel?", "When one is a multiple of the other."), ("What is the zero vector?", "(0, 0).")]),

        U("transformations", "V", "Describe and carry out translations, reflections, rotations and enlargements on the Cartesian plane.",
          "Transformations: Translation, Reflection, Rotation and Enlargement", "Transformations",
          "Free SSS 3 maths worksheets on transformations: translations, reflections in lines, rotations about the origin and enlargements with scale factors. 100 questions with answers.",
          "Reflection in y = x swaps the coordinates", "(x, y) → (y, x)",
          [("Translations", [cx(rt.one_tr, 10), cx(tr8.one_translate, 10)]), ("Reflections", [cx(rt.one_ref, 10), cx(tr8.one_reflect, 10)]), ("Rotations", [cx(rt.one_rot, 10), cx(tr8.one_rotate, 10)]),
           ("Enlargements", [cx(tr8.one_enlarge, 20)]), ("Which transformation?", [cx(rt.one_id, 14), cx(rt.one_sym, 6)])],
          ul(["A translation moves every point by the same vector.", "Reflection in the x-axis: (x, y) → (x, −y); in the y-axis: (x, y) → (−x, y).",
              "Rotation 90° anticlockwise about O: (x, y) → (−y, x). Enlargement scale factor k from O: (x, y) → (kx, ky)."]),
          [ex("Rotate (3, 1) by 180° about O", ["(x, y) → (−x, −y)"], "(−3, −1)")],
          [["Mixing clockwise and anticlockwise", "90° clockwise: (x, y) → (y, −x)."], ["Enlarging from the wrong centre", "Measure from the centre."], ["Changing size in a rotation", "Rotations keep the size."]],
          [("Which transformations keep the size?", "Translation, reflection and rotation."), ("What does a negative scale factor do?", "It enlarges and turns the shape upside down through the centre."), ("What is the image of (2, 5) in y = x?", "(5, 2).")]),

        U("commercial-arithmetic", "N", "Solve problems on compound interest, depreciation, shares and dividends, income tax, VAT, hire purchase, annuities and loans.",
          "Commercial Arithmetic: Shares, Tax and Loans", "Commercial Arithmetic",
          "Free SSS 3 maths worksheets on commercial arithmetic in naira: compound interest, depreciation, shares and dividends, income tax, VAT, hire purchase and annuities. 100 questions with answers.",
          "Dividend = rate × value of shares", "VAT is 7.5% in Nigeria.",
          [("Compound interest and depreciation", [co(J.compound, 10), co(J.depreciation, 10)]), ("Shares and dividends", [co(S.c_shares, 12), co(S.c_buy_shares, 8)]),
           ("Income tax and VAT", [co(S.c_income_tax, 12), co(A.vat, 8)]), ("Hire purchase and loans", [co(A.hire, 10), co(S.c_amortise, 10)]), ("Annuities and savings", [co(S.c_annuity, 12), co(J.compound, 8)])],
          ul(["Amount with compound interest = P(1 + r/100)ⁿ; depreciation uses (1 − r/100)ⁿ.", "A dividend is the share of profit paid on the nominal value of shares.",
              "Income tax is charged on the taxable income: income − allowances."]),
          [ex("1,000 shares of ₦2 at a 10% dividend", ["10% of ₦2,000"], "₦200")],
          [["Using the market price for the dividend", "Dividends are on the nominal value."], ["Taxing the whole income", "Take off the allowances first."], ["Simple interest in compound problems", "Multiply by the multiplier each year."]],
          [("What is an annuity?", "Equal payments made at regular times, growing with interest."), ("What is VAT?", "A tax added to the price of goods and services."), ("What is hire purchase?", "Paying a deposit, then instalments.")]),

        U("permutations-and-combinations", "S", "Use factorials; count arrangements (permutations) and selections (combinations); use them to find probabilities.",
          "Permutations and Combinations", "Permutations and Combinations",
          "Free SSS 3 maths worksheets on permutations and combinations: factorials, nPr, nCr, the counting principle and probability. 100 questions with answers.",
          "Order matters: permutation", "Order does not matter: combination",
          [("Factorials and counting", [cx(ipc.one_fact, 10), cx(pc.one_fcp, 10)]), ("Permutations", [cx(ipc.one_npr, 12), cx(pc.one_perm, 8)]), ("Combinations", [cx(ipc.one_ncr, 12), cx(pc.one_comb, 8)]),
           ("Which one?", [cx(pc.one_which, 10), cx(ipc.one_word, 10)]), ("Probability with counting", [cx(pc.one_prob, 20)])],
          ul(["n! = n × (n − 1) × … × 2 × 1.", "ⁿPᵣ = n! ÷ (n − r)! counts arrangements where order matters.",
              "ⁿCᵣ = n! ÷ (r!(n − r)!) counts selections where order does not matter."]),
          [ex("Choose 2 prefects from 5 pupils", ["⁵C₂ = 5 × 4 ÷ 2"], "10 ways")],
          [["Using a permutation for a committee", "A committee is a combination."], ["Thinking 0! = 0", "0! = 1."], ["Adding instead of multiplying choices", "Multiply the choices at each stage."]],
          [("How many ways can 4 books be arranged?", "4! = 24."), ("What is ⁶C₂?", "15."), ("Is ⁿCᵣ = ⁿCₙ₋ᵣ?", "Yes.")]),
    ]


if __name__ == "__main__":
    main("sss-3", "SSS 3", units, 170300, th=TH_S)
