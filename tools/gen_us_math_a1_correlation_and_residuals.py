# -*- coding: utf-8 -*-
"""
US Algebra 1: Scatter Plots, Correlation and Residuals (Common Core S-ID.B.6, S-ID.C.7, S-ID.C.8, S-ID.C.9)
  python3 tools/gen_us_math_a1_correlation_and_residuals.py
Reading the direction and strength of an association from a scatter plot, the correlation coefficient r,
using and interpreting a line of best fit (slope and intercept in context, predictions), residuals and residual
plots, and correlation versus causation.
Wrong answers come from real mistakes: thinking a negative r means a weak relationship, computing a residual as
predicted − actual, reading the slope as the starting value, trusting predictions far outside the data, and
assuming correlation proves cause.
"""
import random
from fractions import Fraction as F
from us_hs import num, B, S, make, lesson, collect, T, QN, fig, dec
from g8_common import grid_svg
from ws_common import BLUE, RED

R = random.Random(92001)


def nv(v):
    v = F(v)
    return num(v) if v.denominator == 1 else dec(v)


# ------------------------------------------------------------ set 1: scatter plots
def scatter(r, kind):
    pts = []
    xs = r.sample(range(1, 12), 9)
    for x in xs:
        if kind == "pos_strong":
            y = 1 + 0.8 * x + r.uniform(-0.6, 0.6)
        elif kind == "pos_weak":
            y = 2 + 0.5 * x + r.uniform(-2.5, 2.5)
        elif kind == "neg_strong":
            y = 11 - 0.85 * x + r.uniform(-0.6, 0.6)
        elif kind == "neg_weak":
            y = 9 - 0.5 * x + r.uniform(-2.5, 2.5)
        else:
            y = r.uniform(1, 11)
        y = max(0.5, min(11.5, y))
        pts.append((F(round(x * 2), 2), F(round(y * 2), 2), "", BLUE))
    return grid_svg(0, 12, points=pts, unit=20, label="scatter plot")


LABELS = {"pos_strong": "Strong positive", "pos_weak": "Weak positive", "neg_strong": "Strong negative", "neg_weak": "Weak negative", "none": "No correlation"}


def one_scatter(r):
    kind = r.choice(list(LABELS))
    q = "Describe the correlation shown in the scatter plot.%s" % fig(scatter(r, kind))
    right = LABELS[kind]
    wr = [v for k, v in LABELS.items() if k != kind]
    r.shuffle(wr)
    e = {"pos_strong": "The points rise from left to right and lie close to a line: <b>strong positive</b>.",
         "pos_weak": "The points rise from left to right but are spread out: <b>weak positive</b>.",
         "neg_strong": "The points fall from left to right and lie close to a line: <b>strong negative</b>.",
         "neg_weak": "The points fall from left to right but are spread out: <b>weak negative</b>.",
         "none": "There is no upward or downward pattern: <b>no correlation</b>."}[kind]
    return T(q, right, wr[:3], e)


# ------------------------------------------------------------ set 2: the correlation coefficient
def one_r(r):
    kind = r.choice(["describe", "describe", "strongest", "match"])
    if kind == "describe":
        v = r.choice([0.95, 0.88, 0.62, 0.35, 0.05, -0.08, -0.41, -0.67, -0.91, -0.98])
        q = "The correlation coefficient of a data set is %s. Which describes the relationship?" % B(("−%s" % str(abs(v))[1:] if v < 0 else str(v)[1:]).replace("−", "−0", 0) if False else (("−" if v < 0 else "") + ("%.2f" % abs(v)).lstrip("0")))
        q = "The correlation coefficient of a data set is <i>r</i> = %s. Which describes the relationship?" % (("−" if v < 0 else "") + "%.2f" % abs(v))
        a = abs(v)
        strength = "strong" if a >= 0.8 else ("moderate" if a >= 0.5 else ("weak" if a >= 0.25 else "little or no"))
        if strength == "little or no":
            right = "Little or no linear correlation"
        else:
            right = "%s %s linear correlation" % (strength.capitalize(), "positive" if v > 0 else "negative")
        opts = ["Strong positive linear correlation", "Strong negative linear correlation", "Weak positive linear correlation", "Weak negative linear correlation",
                "Moderate positive linear correlation", "Moderate negative linear correlation", "Little or no linear correlation"]
        wr = [o for o in opts if o != right]
        if v < 0:
            wr.sort(key=lambda o: 0 if ("positive" in o and strength in o.lower()) else 1)
        wr.sort()
        if v < 0 and strength != "little or no":
            flip = right.replace("negative", "positive")
            wr = [flip] + [w for w in wr if w != flip]
        e = "The sign of <i>r</i> gives the direction and its size (close to 1 or −1 is strong, close to 0 is weak) gives the strength: <b>%s</b>." % right.lower()
        return T(q, right, wr[:3], e)
    if kind == "strongest":
        vals = r.sample([0.92, -0.95, 0.4, -0.3, 0.75, -0.6, 0.1, -0.85], 4)
        best = max(vals, key=abs)
        fmt = lambda v: ("−" if v < 0 else "") + "%.2f" % abs(v)
        q = "Which correlation coefficient shows the strongest linear relationship?"
        return T(q, "<i>r</i> = " + fmt(best), ["<i>r</i> = " + fmt(v) for v in vals if v != best], "Strength depends on the size of <i>r</i>, not its sign. |%s| is the largest: <b><i>r</i> = %s</b>." % (fmt(best), fmt(best)))
    pairs = [("Height and shoe size of adults", "<i>r</i> = 0.81"), ("Hours of TV watched and test score", "<i>r</i> = −0.45"),
             ("Outside temperature and heating bill", "<i>r</i> = −0.89"), ("Shoe size and birthday month", "<i>r</i> = 0.02")]
    ctx, right = r.choice(pairs)
    wr = [b for a, b in pairs if b != right]
    return T("Which correlation coefficient best fits this pair of variables: %s?" % (ctx[0].lower() + ctx[1:]), right, wr,
             "Think about whether one goes up as the other goes up (positive), goes down (negative) or is unrelated (near 0): <b>%s</b>." % right)


# ------------------------------------------------------------ set 3: line of best fit
CTX = [("<i>y</i> = 2.5<i>x</i> + 40", "hours studied", "test score", 2.5, 40, "points", "hour"),
       ("<i>y</i> = 1.2<i>x</i> + 3", "age of a tree in years", "height in feet", 1.2, 3, "feet", "year"),
       ("<i>y</i> = −0.8<i>x</i> + 95", "minutes of a game played", "phone battery percent", -0.8, 95, "percent", "minute"),
       ("<i>y</i> = 12<i>x</i> + 150", "number of ads", "weekly sales in dollars", 12, 150, "dollars", "ad"),
       ("<i>y</i> = −3.5<i>x</i> + 70", "outside temperature in °F", "hot drinks sold", -3.5, 70, "drinks", "degree")]


def one_fit(r):
    eq, xn, yn, m, b, yu, xu = r.choice(CTX)
    kind = r.choice(["slope", "int", "predict", "predict"])
    head = "A line of best fit for %s (<i>x</i>) and %s (<i>y</i>) is %s." % (xn, yn, B(eq))
    if kind == "slope":
        q = head + " What does the slope mean?"
        right = "For each extra %s, the %s %s by about %s %s" % (xu, yn, "increases" if m > 0 else "decreases", nv(abs(F(str(m)))), yu)
        wr = ["The %s is %s when <i>x</i> = 0" % (yn, nv(F(str(m)))), "For each extra %s, the %s %s by about %s %s" % (xu, yn, "decreases" if m > 0 else "increases", nv(abs(F(str(m)))), yu),
              "For each extra %s, the %s changes by about %s %s" % (xu, yn, nv(b), yu)]
        e = "The slope is the change in <i>y</i> for each 1 unit increase in <i>x</i>: <b>%s</b>." % right.lower()
        return T(q, right, wr, e)
    if kind == "int":
        q = head + " What does the <i>y</i>-intercept mean?"
        right = "The predicted %s when %s is 0 is %s" % (yn, xn, nv(b))
        wr = ["The %s goes up by %s each time" % (yn, nv(b)), "The predicted %s when %s is 0 is %s" % (yn, xn, nv(F(str(m)))), "The largest possible %s is %s" % (yn, nv(b))]
        e = "The <i>y</i>-intercept is the predicted value of <i>y</i> when <i>x</i> = 0: <b>%s</b>." % nv(b)
        return T(q, right, wr, e)
    x = r.randint(2, 12)
    y = F(str(m)) * x + b
    q = head + " Predict the %s when <i>x</i> = %d." % (yn, x)
    ms = ("−" if m < 0 else "") + nv(abs(F(str(m))))
    e = "Substitute <i>x</i> = %d: %s × %d + %s = <b>%s</b>." % (x, ms, x, nv(b), nv(y))
    return QN(q, y, [F(str(m)) * (x + 1) + b, F(str(m)) + x * b if abs(F(str(m)) + x * b) < 5000 else y + 10, (y - b) / x + b * 0 + x], e, fmt=nv, near=(10, -10, 5))


# ------------------------------------------------------------ set 4: residuals
def one_res(r):
    kind = r.choice(["calc", "calc", "calc", "sign", "plot"])
    if kind == "calc":
        m, b = r.choice([2, 3, 4, F(3, 2), F(5, 2)]), r.randint(5, 30)
        x = r.randint(2, 10)
        pred = m * x + b
        act = pred + r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 6])
        q = "The line of best fit is %s. A data point is %s. What is its residual?" % (B("<i>ŷ</i> = %s<i>x</i> + %s" % (nv(m), num(b))), B("(%s, %s)" % (num(x), nv(act))))
        res = act - pred
        e = "Predicted <i>ŷ</i> = %s × %d + %d = %s. Residual = actual − predicted = %s − %s = <b>%s</b>." % (nv(m), x, b, nv(pred), nv(act), nv(pred), nv(res))
        return QN(q, res, [-res, act, pred], e, fmt=nv)
    if kind == "sign":
        q = "A data point has a negative residual. Where is it compared with the line of best fit?"
        return T(q, "Below the line", ["Above the line", "On the line", "To the left of the line"], "Residual = actual − predicted. Negative means the actual value is smaller: <b>below the line</b>.")
    pat = r.choice(["random", "curve"])
    if pat == "random":
        q = "A residual plot shows points scattered randomly above and below zero with no pattern. What does this suggest?"
        return T(q, "A linear model is a good fit", ["A linear model is a poor fit", "There is no correlation", "Every prediction is exact"], "Random residuals mean the line captures the pattern: <b>a linear model fits well</b>.")
    q = "A residual plot shows a clear U-shaped pattern. What does this suggest?"
    return T(q, "A linear model is not a good fit; the data is curved", ["A linear model is a good fit", "The correlation is strong and linear", "The residuals are all zero"],
             "A pattern in the residuals means the line misses the shape of the data: <b>a curve would fit better</b>.")


# ------------------------------------------------------------ set 5: causation and reasoning
def problems():
    data = [
        ("Ice cream sales and drowning incidents have a strong positive correlation. Which conclusion is best?", "Both probably rise in hot weather; ice cream does not cause drowning",
         ["Eating ice cream causes drowning", "Drowning causes ice cream sales", "The correlation must be a mistake"], "A third variable (hot weather) affects both. <b>Correlation does not prove causation.</b>"),
        ("Which situation is most likely to show causation, not just correlation?", "The more hours a heater runs, the more electricity is used", ["Students with bigger feet read better", "Towns with more churches have more crime", "People who own boats live longer"],
         "Running a heater directly uses electricity: <b>a cause</b>. The others are linked by other variables, such as age or population."),
        ("A line of best fit for children aged 2–10 predicts height from age. Should it be used to predict the height of a 40-year-old?", "No, 40 is far outside the data (extrapolation)", ["Yes, the line works for all ages", "Yes, if the correlation is strong", "No, because the slope is positive"],
         "Predicting far outside the data range is risky: people stop growing. <b>No.</b>"),
        ("What is interpolation?", "Predicting within the range of the data", ["Predicting beyond the range of the data", "Finding a residual", "Calculating r"], "<b>Interpolation</b> predicts inside the data's range; extrapolation goes outside it."),
        ("The correlation between two variables is −0.92. Which statement is true?", "As one increases, the other tends to decrease, and the relationship is strong", ["The relationship is weak because r is negative", "One variable causes the other", "There is no relationship"],
         "The sign shows direction (negative) and |−0.92| is close to 1: <b>strong and negative</b>."),
        ("Which value of <i>r</i> is impossible?", "1.3", ["−1", "0", "0.99"], "<i>r</i> is always between −1 and 1, so <b>1.3</b> is impossible."),
        ("A residual is +6. What does it mean?", "The actual value is 6 more than the line predicted", ["The line predicted 6 more than the actual value", "The slope is 6", "The point is 6 units to the right"], "Residual = actual − predicted = +6: <b>the actual value is 6 above the prediction</b>."),
        ("Two lines are fitted to the same data. Line A's residuals are mostly between −1 and 1; line B's are between −5 and 5. Which fits better?", "Line A", ["Line B", "They fit equally well", "You cannot tell from residuals"], "Smaller residuals mean the predictions are closer to the data: <b>line A</b>."),
        ("A study finds that students who eat breakfast get higher grades. What is the best conclusion?", "There is an association, but other factors may explain it", ["Eating breakfast causes higher grades", "Higher grades cause students to eat breakfast", "There is no relationship"],
         "An observational study shows <b>association, not cause</b>. Home routines, sleep and other factors may be involved."),
        ("A scatter plot's points rise steeply and lie almost exactly on a line. Which value of <i>r</i> fits best?", "0.98", ["0.30", "−0.98", "0"], "Rising and very close to a line: <b><i>r</i> ≈ 0.98</b>."),
        ("If <i>r</i> = 0, which statement is true?", "There is no linear relationship", ["There is no relationship of any kind", "All points are on a horizontal line", "The variables are equal"], "<i>r</i> measures <b>linear</b> relationships only. A curved pattern can still give <i>r</i> ≈ 0."),
        ("The equation <i>ŷ</i> = 15<i>x</i> + 200 predicts monthly sales <i>ŷ</i> from advertising dollars <i>x</i> (in hundreds). If $400 is spent on ads, what are the predicted sales?", "$260", ["$6,200", "$215", "$600"], "<i>x</i> = 4: 15 × 4 + 200 = <b>$260</b>."),
        ("A line of best fit has slope 0. What does that suggest?", "<i>x</i> does not help predict <i>y</i>", ["A perfect positive relationship", "A perfect negative relationship", "All residuals are 0"], "A flat line predicts the same <i>y</i> for every <i>x</i>: <b><i>x</i> does not help predict <i>y</i></b>."),
        ("Which is the best reason to look at a residual plot?", "To check whether a linear model is appropriate", ["To find the mean of the data", "To find the median", "To make the correlation stronger"], "Patterns in a residual plot show whether <b>a line is the right model</b>."),
        ("Countries with more TVs per person have longer life expectancy. Should a government buy TVs to help people live longer?", "No, wealth is a likely hidden factor", ["Yes, TVs cause longer lives", "Yes, the correlation is strong", "No, the correlation is negative"],
         "Richer countries have both more TVs and better health care. <b>Correlation is not causation.</b>"),
        ("The correlation between hours of practice and free-throw percentage is 0.7. Which word describes it?", "Moderate to strong positive", ["Weak negative", "Perfect", "No correlation"], "0.7 is positive and fairly close to 1: <b>moderate to strong positive</b>."),
        ("A data point is (5, 30) and the line predicts 34 at <i>x</i> = 5. What is the residual?", "−4", ["4", "34", "30"], "Residual = actual − predicted = 30 − 34 = <b>−4</b>."),
        ("What does it mean if all residuals are positive?", "The line is too low for every point", ["The line fits perfectly", "The line is too high for every point", "The correlation is negative"], "Positive residuals mean every point is above the line: <b>the line is too low</b>; a better line would be higher."),
        ("Which pair of variables would most likely have a negative correlation?", "Car age and resale value", ["Height and weight", "Study time and test scores", "Temperature and ice cream sales"], "Older cars are usually worth less: <b>negative</b>."),
        ("A scientist runs a controlled experiment where only one variable is changed. Why can she claim cause and effect?", "Other factors were kept the same", ["The sample was large", "The correlation was positive", "She used a scatter plot"], "In a controlled experiment, <b>other factors are held constant</b>, so changes can be linked to the one variable changed."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


def body():
    return lesson(
        "<p>A <b>scatter plot</b> shows the relationship between two variables. If the points rise, the correlation is <b>positive</b>; if they fall, it is "
        "<b>negative</b>. The closer they are to a straight line, the <b>stronger</b> it is.</p>"
        "<p>The <b>correlation coefficient</b> <i>r</i> is between −1 and 1. Its sign gives the direction and its size gives the strength: |<i>r</i>| near 1 is strong, near 0 is weak.</p>"
        "<p>A <b>residual</b> = actual − predicted. Residuals scattered randomly around 0 mean a line is a good model. "
        "<b>Correlation does not mean causation</b>: a third variable may affect both.</p>",
        [("A line of best fit is <i>ŷ</i> = 3<i>x</i> + 10. Find the residual for (4, 25).", ["Predicted: 3 × 4 + 10 = 22.", "25 − 22."], "3"),
         ("<i>r</i> = −0.85. Describe the correlation.", ["Negative sign: one goes down as the other goes up.", "0.85 is close to 1."], "Strong negative")],
        ["Thinking a negative <i>r</i> means a weak relationship. −0.9 is strong.",
         "Finding the residual as predicted − actual. It is actual − predicted.",
         "Reading the slope as the starting value. The slope is the change per unit of <i>x</i>.",
         "Assuming that correlation proves one variable causes the other."])


def main():
    sets = [S("Describe a scatter plot", collect(one_scatter, 20, R)),
            S("The correlation coefficient", collect(one_r, 20, R)),
            S("Lines of best fit in context", collect(one_fit, 20, R)),
            S("Residuals", collect(one_res, 20, R)),
            S("Correlation and causation", problems())]
    make("correlation-and-residuals", 20, "S-ID.C.8",
         "Scatter Plots, Correlation and Residuals",
         "Algebra 1 Correlation Worksheets: Scatter Plots, Correlation Coefficient, Residuals and Causation (Free, Answer Key)",
         "Correlation and residuals",
         "Compute (using technology) and interpret the correlation coefficient of a linear fit.",
         "Free Algebra 1 worksheets on scatter plots and correlation (S-ID.B.6, S-ID.C.7–9): describe correlation, interpret the correlation "
         "coefficient r, use and interpret lines of best fit, calculate residuals and tell correlation from causation. 100 questions with an answer key.",
         "r is between −1 and 1: the sign is the direction, the size is the strength.",
         "Residual = actual − predicted. Correlation does not prove causation.",
         body(),
         [("What does the correlation coefficient tell you?", "r measures the direction and strength of a linear relationship. It is between −1 and 1; values near ±1 are strong and values near 0 are weak."),
          ("How do you calculate a residual?", "Subtract the predicted value from the actual value: residual = actual y − predicted y."),
          ("What does a good residual plot look like?", "Points scattered randomly above and below zero with no pattern. A curve in the residuals means a line is not a good model."),
          ("Why doesn't correlation prove causation?", "Two variables can move together because of a third variable or by chance. Only a controlled experiment can show cause and effect.")],
         sets, R, domain="Statistics")


if __name__ == "__main__":
    main()
