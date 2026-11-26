# -*- coding: utf-8 -*-
"""
UK maths units built from the hand-made makers in uk_gap_own:
GCSE Year 11 (histograms, iteration, algebraic proof, velocity–time graphs, equation of a circle) and
A level Year 12 (proof) and Year 13 (product and quotient rules, hypothesis tests for a normal mean and for correlation).
python3 tools/gen_uk_maths_y11_{slug}.py (or y12 / y13) calls build(slug, year).
"""
import random
import uk_ks3
import uk_gcse
import uk_alevel
import uk_gap_own as O


def U(year, sort, slug, strand, title, short, std, meta, kb, ks, think, ex, mist, faq, spec):
    return dict(year=year, sort=sort, slug=slug, strand=strand, title=title, short=short, std=std, meta=meta, kb=kb, ks=ks,
                think=think, ex=ex, mist=mist, faq=faq, spec=spec)


def units():
    L = []
    # ------------------------------------------------------------------ GCSE Year 11
    L.append(U(11, 5, "equation-of-a-circle", "A", "Equation of a Circle and Tangents", "equation of a circle",
               "Recognise and use the equation of a circle with centre at the origin; find the equation of a tangent to a circle at a given point.",
               "Free Year 11 GCSE maths worksheets on the equation of a circle x² + y² = r²: the radius, points on a circle, gradients of radii and tangents, and equations of tangents. 100 questions with answers.",
               "x² + y² = r² is a circle, centre (0, 0), radius r.", "A tangent is perpendicular to the radius at that point.",
               "<p>Every point (<i>x</i>, <i>y</i>) on a circle with centre the origin and radius <i>r</i> obeys <i>x</i>² + <i>y</i>² = <i>r</i>² (Pythagoras). So <i>x</i>² + <i>y</i>² = 49 has radius 7, not 49.</p>"
               "<p>To find a tangent at P(<i>a</i>, <i>b</i>): the gradient of OP is <i>b</i>/<i>a</i>, the tangent is perpendicular, so its gradient is −<i>a</i>/<i>b</i>. Then use <i>y</i> − <i>b</i> = <i>m</i>(<i>x</i> − <i>a</i>).</p>",
               [("Find the radius of <i>x</i>² + <i>y</i>² = 81.", ["<i>r</i>² = 81"], "9"),
                ("Find the gradient of the tangent to <i>x</i>² + <i>y</i>² = 25 at (3, 4).", ["Gradient of OP = 4/3", "Perpendicular gradient = −1 ÷ 4/3"], "−3/4")],
               ["Giving r² as the radius.", "Using the gradient of the radius for the tangent.", "Forgetting the negative square root when a line crosses the circle."],
               [("What is the equation of a circle with centre the origin?", "x² + y² = r², where r is the radius. It comes from Pythagoras' theorem."),
                ("How do you find the equation of a tangent to a circle?", "Find the gradient of the radius to the point, take the negative reciprocal for the tangent, then use y − b = m(x − a).")],
               [("Radius and equation", [(O.c_basic, 20)]),
                ("Points on a circle", [(O.c_on, 14), (O.c_line, 6)]),
                ("Gradients of radii and tangents", [(O.c_grad, 20)]),
                ("Equations of tangents", [(O.c_tangent, 20)]),
                ("Mixed circle problems", [(O.c_basic, 5), (O.c_on, 5), (O.c_grad, 5), (O.c_tangent, 5)])]))
    L.append(U(11, 13, "histograms", "S", "Histograms with Unequal Class Widths", "histograms",
               "Construct and interpret diagrams for grouped continuous data, including histograms with equal and unequal class intervals.",
               "Free Year 11 GCSE maths worksheets on histograms: frequency density, frequencies from bars, reading histograms with unequal class widths and estimating from them. 100 questions with answers.",
               "Frequency density = frequency ÷ class width.", "On a histogram, the area of a bar shows the frequency.",
               "<p>When the classes have different widths, the height of each bar is the <b>frequency density</b> = frequency ÷ class width. Then the <b>area</b> of a bar is the frequency: frequency = frequency density × class width.</p>"
               "<p>To estimate how many are above a value inside a class, take the fraction of the class width that is above it.</p>",
               [("The class 10 &lt; <i>t</i> ≤ 30 has frequency 24. Find the frequency density.", ["Width = 20", "24 ÷ 20"], "1.2"),
                ("A bar for 30 &lt; <i>t</i> ≤ 35 has frequency density 4. Find the frequency.", ["Width = 5", "4 × 5"], "20")],
               ["Plotting frequency instead of frequency density.", "Multiplying frequency by class width.", "Reading the height of a bar as its frequency."],
               [("What is frequency density?", "Frequency density = frequency ÷ class width. It is the height of each bar on a histogram."),
                ("How do you read a frequency from a histogram?", "Multiply the frequency density (the height) by the class width: the area of the bar is the frequency.")],
               [("Frequency density", [(O.h_fd, 20)]),
                ("Frequency from a bar", [(O.h_freq, 20)]),
                ("Reading histograms", [(O.h_read, 20)]),
                ("Estimating from grouped data", [(O.h_est, 20)]),
                ("Histogram problems", [(O.h_scale, 12), (O.h_highest, 8)])]))
    L.append(U(11, 14, "iteration", "A", "Iteration and Approximate Solutions", "iteration",
               "Find approximate solutions to equations numerically using iteration; use a change of sign to locate a root.",
               "Free Year 11 GCSE maths worksheets on iteration: using iteration formulae, rearranging equations, change of sign and finding solutions to 2 decimal places. 100 questions with answers.",
               "Put each answer back into the formula to get the next one.", "A change of sign shows a solution in between.",
               "<p>An iteration formula such as <i>x</i><sub>n+1</sub> = ∛(2<i>x</i><sub>n</sub> + 5) is made by rearranging an equation (here <i>x</i>³ − 2<i>x</i> − 5 = 0). Start with <i>x</i><sub>0</sub>, work out <i>x</i><sub>1</sub>, put it back in to get <i>x</i><sub>2</sub>, and so on. Use the ANS key on a calculator.</p>"
               "<p>If f(<i>a</i>) and f(<i>b</i>) have different signs, there is a solution of f(<i>x</i>) = 0 between <i>a</i> and <i>b</i>.</p>",
               [("<i>x</i><sub>n+1</sub> = √(3<i>x</i><sub>n</sub> + 4), <i>x</i><sub>0</sub> = 1. Find <i>x</i><sub>1</sub>.", ["√(3 × 1 + 4) = √7"], "2.646"),
                ("f(<i>x</i>) = <i>x</i>³ − 4<i>x</i> − 2. Show there is a root between 2 and 3.", ["f(2) = −2", "f(3) = 13"], "The sign changes, so there is a root between 2 and 3")],
               ["Using x₀ again instead of the new value.", "Rounding too early.", "Changing a sign when rearranging the equation."],
               [("What is an iteration formula?", "A rule that turns one approximation into the next, such as x(n+1) = ∛(2x(n) + 5). The values get closer and closer to a solution."),
                ("How does a change of sign show a solution?", "If f(a) is negative and f(b) is positive (or the other way), the graph crosses the x-axis between a and b, so f(x) = 0 has a solution there.")],
               [("Using an iteration formula", [(O.it_val, 20)]),
                ("Rearranging equations", [(O.it_rearr, 20)]),
                ("Change of sign", [(O.it_sign, 20)]),
                ("Iterating to a solution", [(O.it_conv, 20)]),
                ("Mixed iteration problems", [(O.it_val, 7), (O.it_rearr, 7), (O.it_sign, 6)])]))
    L.append(U(11, 15, "algebraic-proof", "A", "Algebraic Proof", "algebraic proof",
               "Argue mathematically to show algebraic expressions are equivalent, and use algebra to support and construct arguments and proofs.",
               "Free Year 11 GCSE maths worksheets on algebraic proof: odd, even and multiples, consecutive numbers, expanding to prove, counterexamples and completing proofs. 100 questions with answers.",
               "Even = 2n, odd = 2n + 1, multiple of k = k × an integer.", "One counterexample proves a statement false.",
               "<p>Write the numbers in algebra: an even number is 2<i>n</i>, an odd number is 2<i>n</i> + 1, consecutive integers are <i>n</i>, <i>n</i> + 1, <i>n</i> + 2. Expand and simplify, then take out a factor: 6<i>n</i> + 9 = 3(2<i>n</i> + 3) is a multiple of 3.</p>"
               "<p>Checking a few numbers is not a proof. But one counterexample is enough to show a statement is false.</p>",
               [("Prove the sum of three consecutive integers is a multiple of 3.", ["<i>n</i> + (<i>n</i> + 1) + (<i>n</i> + 2) = 3<i>n</i> + 3"], "3(<i>n</i> + 1)"),
                ("Show (<i>n</i> + 3)² − (<i>n</i> − 3)² is a multiple of 12.", ["<i>n</i>² + 6<i>n</i> + 9 − (<i>n</i>² − 6<i>n</i> + 9)"], "12<i>n</i>")],
               ["Testing a few values and calling it a proof.", "Using n and n for two different odd numbers.", "Not taking out the factor at the end."],
               [("How do you write an odd number in algebra?", "2n + 1 (or 2n − 1), where n is an integer. 2n is always even, so 2n + 1 is always odd."),
                ("What is a counterexample?", "One example that makes a statement false. It is enough to disprove the statement.")],
               [("Even, odd and multiples", [(O.p_form, 20)]),
                ("Consecutive numbers", [(O.p_consec, 10), (O.p_odd, 10)]),
                ("Expanding to prove", [(O.p_expand, 20)]),
                ("Counterexamples", [(O.p_counter, 20)]),
                ("Completing a proof", [(O.p_factor, 12), (O.p_odd, 8)])]))
    L.append(U(11, 16, "velocity-time-graphs", "A", "Velocity–Time and Distance–Time Graphs", "velocity–time graphs",
               "Interpret the gradient at a point on a curve as the instantaneous rate of change; calculate or estimate gradients of graphs and areas under graphs (including velocity–time and distance–time graphs) and interpret results in context.",
               "Free Year 11 GCSE maths worksheets on velocity–time graphs: acceleration from the gradient, distance from the area, distance–time graphs and estimating areas with trapezia. 100 questions with answers.",
               "Gradient = acceleration. Area = distance.", "On a distance–time graph, the gradient is the speed.",
               "<p>On a <b>velocity–time</b> graph, the gradient is the acceleration (a downward slope is a deceleration) and the area under the graph is the distance travelled. Split the area into triangles, rectangles and trapezia.</p>"
               "<p>On a <b>distance–time</b> graph, the gradient is the speed and a horizontal line means the object is not moving. For a curve, estimate the area with trapezia.</p>",
               [("A car speeds up from 4 m/s to 16 m/s in 6 s. Find the acceleration.", ["(16 − 4) ÷ 6"], "2 m/s²"),
                ("It does this at a steady rate. Find the distance travelled.", ["½ × (4 + 16) × 6"], "60 m")],
               ["Reading the velocity as the distance.", "Working out time ÷ velocity for the gradient.", "Leaving out the time spent stopped in an average speed."],
               [("What does the area under a velocity–time graph show?", "The distance travelled. Split it into triangles, rectangles and trapezia and add the areas."),
                ("What does the gradient of a velocity–time graph show?", "The acceleration. A negative gradient is a deceleration and a horizontal line means constant velocity.")],
               [("Acceleration", [(O.vt_acc, 20)]),
                ("Distance from the area", [(O.vt_area, 20)]),
                ("Reading velocity–time graphs", [(O.vt_graph_q, 20)]),
                ("Distance–time graphs", [(O.vt_dt, 20)]),
                ("Estimating distance with trapezia", [(O.vt_trap, 20)])]))
    # ------------------------------------------------------------------ A level Year 12
    L.append(U(12, 18, "proof", "P", "Proof: Deduction, Exhaustion, Counterexample and Contradiction", "proof",
               "Understand and use the structure of mathematical proof, proceeding from given assumptions through a series of logical steps to a conclusion; use methods of proof, including proof by deduction, proof by exhaustion and disproof by counterexample; proof by contradiction.",
               "Free Year 12 A level maths worksheets on proof: proof by deduction, proof by exhaustion, disproof by counterexample, completing the square to prove inequalities and proof by contradiction. 100 questions with answers.",
               "A proof must work for every case; one counterexample disproves.", "Contradiction: assume the opposite and reach something impossible.",
               "<p><b>Deduction</b>: start from what you know and use algebra, e.g. <i>n</i>³ − <i>n</i> = (<i>n</i> − 1)<i>n</i>(<i>n</i> + 1). <b>Exhaustion</b>: split into every possible case, e.g. <i>n</i> = 3<i>k</i>, 3<i>k</i> + 1, 3<i>k</i> + 2. <b>Counterexample</b>: one example that makes the statement false.</p>"
               "<p><b>Contradiction</b>: assume the statement is false and show this leads to something impossible. To prove √2 is irrational, assume √2 = <i>a</i>/<i>b</i> in its lowest terms.</p>",
               [("Prove <i>x</i>² − 6<i>x</i> + 10 &gt; 0 for all real <i>x</i>.", ["<i>x</i>² − 6<i>x</i> + 10 = (<i>x</i> − 3)² + 1", "(<i>x</i> − 3)² ≥ 0"], "It is at least 1, so always positive"),
                ("Disprove: <i>n</i>² + <i>n</i> + 11 is always prime.", ["<i>n</i> = 10: 100 + 10 + 11 = 121 = 11²"], "<i>n</i> = 10 is a counterexample")],
               ["Checking a few cases and calling it a proof.", "Assuming what you want to prove in a proof by contradiction.", "Missing a case in a proof by exhaustion."],
               [("What is proof by exhaustion?", "Splitting the problem into a finite number of cases (such as odd and even, or the remainders when dividing by 3) and proving each case."),
                ("How does proof by contradiction work?", "Assume the statement is false, then follow logical steps to something impossible. So the statement must be true.")],
               [("Proof by deduction", [(O.pr_deduct, 20)]),
                ("Proof by exhaustion", [(O.pr_exhaust, 20)]),
                ("Disproof by counterexample", [(O.pr_counter, 20)]),
                ("Completing the square in proofs", [(O.pr_square, 20)]),
                ("Proof by contradiction", [(O.pr_contra, 20)])]))
    # ------------------------------------------------------------------ A level Year 13
    L.append(U(13, 15, "product-and-quotient-rules", "P", "The Product Rule and the Quotient Rule", "product and quotient rules",
               "Differentiate using the product rule, the quotient rule and the chain rule; use differentiation to find gradients, tangents and stationary points.",
               "Free Year 13 A level maths worksheets on the product rule and the quotient rule: differentiating products and quotients of polynomials, eˣ, ln x, sin x and cos x, gradients, stationary points and tangents. 100 questions with answers.",
               "Product: (uv)′ = u′v + uv′.", "Quotient: (u/v)′ = (vu′ − uv′)/v².",
               "<p>For <i>y</i> = <i>uv</i>: d<i>y</i>/d<i>x</i> = <i>u</i>′<i>v</i> + <i>uv</i>′. For <i>y</i> = <i>u</i>/<i>v</i>: d<i>y</i>/d<i>x</i> = (<i>vu</i>′ − <i>uv</i>′)/<i>v</i>². Write down <i>u</i>, <i>v</i>, <i>u</i>′ and <i>v</i>′ first.</p>"
               "<p>Factorise the answer (for example take out e<sup><i>x</i></sup>) to find stationary points: e<sup><i>x</i></sup> is never 0, so set the other factor to 0.</p>",
               [("Differentiate <i>y</i> = <i>x</i>²e<sup><i>x</i></sup>.", ["<i>u</i>′<i>v</i> = 2<i>x</i>e<sup><i>x</i></sup>, <i>uv</i>′ = <i>x</i>²e<sup><i>x</i></sup>"], "<i>x</i>e<sup><i>x</i></sup>(<i>x</i> + 2)"),
                ("Differentiate <i>y</i> = (2<i>x</i> + 1)/(<i>x</i> + 3).", ["[2(<i>x</i> + 3) − 1(2<i>x</i> + 1)]/(<i>x</i> + 3)²"], "5/(<i>x</i> + 3)²")],
               ["Multiplying the two derivatives: (uv)′ is not u′v′.", "Getting the order wrong in the quotient rule (uv′ − vu′).", "Forgetting to square the denominator."],
               [("What is the product rule?", "If y = uv, then dy/dx = u′v + uv′: differentiate one factor at a time and add."),
                ("What is the quotient rule?", "If y = u/v, then dy/dx = (vu′ − uv′)/v². The minus sign means the order matters.")],
               [("The product rule", [(O.pq_prod, 20)]),
                ("The quotient rule", [(O.pq_quot, 20)]),
                ("Gradients at a point", [(O.pq_num, 20)]),
                ("Stationary points", [(O.pq_stat, 20)]),
                ("Tangents", [(O.pq_tan, 20)])]))
    L.append(U(13, 16, "hypothesis-testing-normal-and-correlation", "S", "Hypothesis Tests: the Normal Mean and Correlation", "hypothesis tests for the mean and correlation",
               "Conduct a statistical hypothesis test for the mean of a normal distribution with known, given or assumed variance and interpret the results in context; use a statistical hypothesis test for correlation coefficients (the product moment correlation coefficient).",
               "Free Year 13 A level maths worksheets on hypothesis testing: hypotheses for a normal mean, the distribution of the sample mean, z test statistics, critical regions, conclusions in context and tests for correlation. 100 questions with answers.",
               "Sample mean: X̄ ~ N(μ, σ²/n).", "Compare z (or r) with the critical value and conclude in context.",
               "<p>If <i>X</i> ~ N(μ, σ²), the mean of a sample of size <i>n</i> has <span style='text-decoration:overline'><i>X</i></span> ~ N(μ, σ²/<i>n</i>). The test statistic is <i>z</i> = (<span style='text-decoration:overline'><i>x</i></span> − μ)/(σ/√<i>n</i>). Reject H<sub>0</sub> if <i>z</i> is in the critical region (for example <i>z</i> &gt; 1.6449 for a one-tailed 5% test, |<i>z</i>| &gt; 1.96 for a two-tailed 5% test).</p>"
               "<p>For correlation, H<sub>0</sub>: ρ = 0. Compare the sample value <i>r</i> with the critical value from the table for the sample size.</p>",
               [("μ = 50, σ = 6, <i>n</i> = 36, <span style='text-decoration:overline'><i>x</i></span> = 52. Find <i>z</i>.", ["σ/√<i>n</i> = 1", "(52 − 50) ÷ 1"], "2"),
                ("H<sub>1</sub>: μ &gt; 50 at 5%. Is <i>z</i> = 2 significant?", ["2 &gt; 1.6449"], "Yes: reject H<sub>0</sub>, there is evidence that the mean has increased")],
               ["Dividing by σ instead of σ/√n.", "Using the one-tailed critical value in a two-tailed test.", "Saying the test proves H₁, or writing hypotheses with x̄ or r instead of μ or ρ."],
               [("What is the distribution of the sample mean?", "If X ~ N(μ, σ²), then the sample mean X̄ ~ N(μ, σ²/n), so its standard deviation is σ/√n."),
                ("How do you test for correlation?", "Use H₀: ρ = 0 and H₁: ρ > 0, ρ < 0 or ρ ≠ 0. If |r| is bigger than the critical value for the sample size and significance level, reject H₀.")],
               [("Writing hypotheses", [(O.h_hyp, 12), (O.h_rhyp, 8)]),
                ("The distribution of the sample mean", [(O.h_mean_dist, 20)]),
                ("Test statistics and critical values", [(O.h_z, 12), (O.h_tails, 8)]),
                ("Conclusions and critical regions", [(O.h_dec, 12), (O.h_crit, 8)]),
                ("Testing for correlation", [(O.h_corr, 20)])]))
    return L


def build(slug, year):
    u = next(x for x in units() if x["slug"] == slug and x["year"] == year)
    if year >= 12:
        uk_alevel.unit(u["year"], u["slug"], u["sort"], u["strand"], u["title"], u["short"], u["std"], u["meta"], u["kb"], u["ks"],
                       u["think"], u["ex"], u["mist"], u["faq"], u["spec"], 91000 + year * 100 + u["sort"])
        return
    r = random.Random(91100 + u["sort"])
    seen = set()
    sets = []
    for t, parts in u["spec"]:
        items = []
        for f, k in parts:
            items += uk_alevel._collect(f, k, r, seen)
        assert len(items) == 20, (t, len(items))
        r.shuffle(items)
        sets.append({"title": t, "items": items})
    body = uk_ks3.lesson(u["think"], u["ex"], u["mist"])
    uk_gcse.make_gcse(year, u["slug"], u["sort"], u["strand"], u["title"], u["short"], u["std"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, r)
