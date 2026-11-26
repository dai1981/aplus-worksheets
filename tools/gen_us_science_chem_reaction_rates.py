# -*- coding: utf-8 -*-
"""
US High School Chemistry: Reaction Rates (HS-PS1-5)
  python tools/gen_us_science_chem_reaction_rates.py
Apply scientific principles and evidence to provide an explanation about the effects of changing the temperature or
concentration of the reacting particles on the rate at which a reaction occurs.
Collision theory; temperature, concentration, surface area, pressure and catalysts; average rate from gas volume or
mass loss; reading rate data from experiments.
Wrong answers come from real mistakes: "a catalyst is used up", "higher temperature makes particles bigger",
"a faster reaction makes more product", "a longer time means a faster reaction".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import num

U = Unit(90210)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


CH = [("The acid is heated from 20 °C to 40 °C.", "faster", "Particles move faster, so they collide more often and more collisions have enough energy."),
      ("The acid is cooled in an ice bath.", "slower", "Slower particles collide less often and with less energy."),
      ("A more concentrated acid is used.", "faster", "More particles in the same volume collide more often."),
      ("The acid is diluted with water.", "slower", "Fewer particles per volume means fewer collisions."),
      ("Marble chips are crushed into powder.", "faster", "More surface area exposes more particles to collisions."),
      ("One large lump of zinc is used instead of zinc granules.", "slower", "Less surface area means fewer collisions."),
      ("A catalyst is added.", "faster", "A catalyst gives a path with lower activation energy."),
      ("The gas is squeezed into a smaller container.", "faster", "Higher pressure packs gas particles closer, so they collide more often."),
      ("Food is kept in a refrigerator.", "slower", "Lower temperature slows the reactions that spoil food."),
      ("Enzymes in saliva are added to starch.", "faster", "Enzymes are biological catalysts."),
      ("Charcoal is burned as large lumps instead of small pieces.", "slower", "Less surface area is exposed to oxygen."),
      ("A campfire is fanned to supply more oxygen.", "faster", "Higher oxygen concentration means more collisions."),
      ("Hydrogen peroxide is stored in a cool, dark place.", "slower", "Lower temperature and no light slow its decomposition."),
      ("The reaction mixture is stirred constantly.", "faster", "Stirring brings fresh reactant particles together.")]


def g_factor():
    s, d, why = R.choice(CH)
    k = R.random() < 0.6
    if not once(("ch", s, k)):
        return None
    if k:
        return item("%s What happens to the reaction rate?" % s, "It gets %s." % d, ["It gets %s." % ("slower" if d == "faster" else "faster"), "It stays the same.", "The reaction stops forever."], why)
    w = R.sample([x[2] for x in CH if x[2] != why], 3)
    return item("%s Which explains the change in rate?" % s, why, w, "Collision theory.")


def g_rate():
    who = P.next()[0]
    k = R.choice(["gas", "mass"])
    t = R.choice([10, 20, 25, 30, 40, 50, 60, 80, 100, 120])
    r = R.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 0.25, 0.2]) if k == "gas" else R.choice([0.01, 0.02, 0.05, 0.1])
    v = t * r
    if v != round(v, 1) or not once(("rt", k, t, r)):
        return None
    if k == "gas":
        return item("%s collects %s mL of carbon dioxide in %d s. What is the average rate of gas production?" % (who, num(v), t), "%s mL/s" % num(r),
                    ["%s mL/s" % num(round(t / v, 2)), "%s mL/s" % num(v * t), "%s mL/s" % num(v)], "%s ÷ %d = %s mL/s." % (num(v), t, num(r)))
    return item("A flask on a balance loses %s g of gas in %d s (%s's experiment). What is the average rate of mass loss?" % (num(v), t, who), "%s g/s" % num(r),
                ["%s g/s" % num(round(t / v, 2)), "%s g/s" % num(v * t), "%s g/s" % num(v)], "%s ÷ %d = %s g/s." % (num(v), t, num(r)))


def g_data():
    who = P.next()[0]
    var = R.choice(["temp", "conc"])
    if var == "temp":
        xs = [10, 20, 30, 40, 50]
        base = R.randint(150, 260)
        ys = [base]
        for _ in range(4):
            ys.append(max(5, int(ys[-1] / R.choice([1.8, 2, 2.2]))))
        head = ["Temperature (°C)", "Time for the solution to turn cloudy (s)"]
        lab = "temperature"
        u = " °C"
    else:
        xs = [0.25, 0.5, 1.0, 1.5, 2.0]
        base = R.randint(120, 240)
        ys = [base]
        for i in range(4):
            ys.append(max(5, int(base * xs[0] / xs[i + 1])))
        head = ["Acid concentration (mol/L)", "Time for the magnesium ribbon to disappear (s)"]
        lab = "concentration"
        u = " mol/L"
    k = R.choice(["trend", "fast", "read", "pred"])
    if len(set(ys)) < 5 or not once(("dt", var, tuple(ys), k)) or (k in ("trend", "pred") and not once((var, k), 3)):
        return None
    tab = table(head, [[("%g" % x), str(y)] for x, y in zip(xs, ys)])
    if k == "trend":
        return item(tab + "What do %s's results show?" % who, "As %s increases, the reaction gets faster (less time)." % lab,
                    ["As %s increases, the reaction gets slower." % lab, "%s has no effect on the rate." % lab.capitalize(), "Longer times mean faster reactions."], "Shorter time = faster rate.")
    if k == "fast":
        return item(tab + "In %s's experiment, at which %s was the reaction fastest?" % (who, lab), "%g%s" % (xs[-1], u), ["%g%s" % (xs[0], u), "%g%s" % (xs[2], u), "%g%s" % (xs[1], u)], "The shortest time is the fastest rate.")
    if k == "read":
        i = R.randrange(5)
        return item(tab + "In %s's data, how long did the reaction take at %g%s?" % (who, xs[i], u), "%d s" % ys[i], ["%d s" % ys[(i + 1) % 5], "%d s" % ys[(i + 2) % 5], "%d s" % (ys[i] + 15)],
                    "Read the row.")
    return item(tab + "Predict the time if %s repeats the experiment at a %s higher than %g%s." % (who, lab, xs[-1], u), "less than %d s" % ys[-1], ["more than %d s" % ys[0], "exactly %d s" % ys[0], "between %d and %d s" % (ys[2], ys[0])],
                "The pattern continues: faster, so less time.")


def g_cat():
    s = R.choice([("manganese dioxide speeds up the breakdown of hydrogen peroxide", "It is not used up and can be reused."),
                  ("platinum in a catalytic converter speeds up reactions of car exhaust", "It provides a path with lower activation energy."),
                  ("the enzyme catalase speeds up the breakdown of hydrogen peroxide in cells", "It lowers the activation energy without being used up."),
                  ("iron speeds up the reaction that makes ammonia", "It lets the reaction go fast at a lower temperature, saving energy."),
                  ("the enzyme amylase speeds up the digestion of starch", "Its active site holds the reactant so the reaction needs less energy.")])
    if not once(("ct", s[0])):
        return None
    return item("A catalyst: %s. Which statement about the catalyst is true?" % s[0], s[1], ["It is used up in the reaction.", "It makes more product overall.", "It raises the activation energy."],
                "Catalysts speed reactions without being consumed.")


B1 = bank([
    ("What is a reaction rate?", "how fast reactants are used up or products are made", ["how much product is made in total", "the temperature of a reaction", "the color change"], "Change per unit time."),
    ("According to collision theory, what must happen for particles to react?", "They must collide with enough energy and the right orientation.", ["They must stay still.", "They must be the same size.", "They must be cold."],
     "Effective collisions."),
    ("Why does raising the temperature speed up most reactions?", "More collisions happen, and more of them have enough energy.", ["Particles get bigger.", "Activation energy increases.", "Fewer collisions happen."], "Kinetic energy."),
    ("What does a catalyst do?", "speeds up a reaction by lowering the activation energy", ["gets used up as a reactant", "makes more product", "raises the activation energy"], "Different pathway."),
    ("Why does powdered sugar dissolve and react faster than a sugar cube?", "Powder has more surface area.", ["Powder is hotter.", "Cubes have more particles on the surface.", "Powder is a different chemical."], "Surface area."),
    ("How does increasing concentration affect the rate?", "It increases the rate because collisions are more frequent.", ["It decreases the rate.", "It has no effect.", "It stops the reaction."], "More particles per volume."),
    ("Does a catalyst change how much product forms?", "No. It only makes the reaction reach the end sooner.", ["Yes, it doubles the product.", "Yes, it makes less.", "It turns into product."], "Same yield, faster."),
    ("A reaction finishes in 30 s at one temperature and 60 s at another. Which run was faster?", "the 30 s run", ["the 60 s run", "They were the same.", "It cannot be known."], "Less time = faster."),
])
B5 = bank([
    ("Why do grain silos sometimes explode?", "Fine grain dust has a huge surface area and burns very fast.", ["Grain is a catalyst.", "Silos are cold.", "Grain is a metal."], "Surface area."),
    ("A student tests acid concentration but uses different temperatures in each trial. What is wrong?", "Temperature is a second variable that also changes the rate.", ["Nothing is wrong.", "She should use more acid.", "She should time it once."], "Control variables."),
    ("Why do doctors store some medicines in a refrigerator?", "Cold slows the reactions that break the medicine down.", ["Cold makes medicine stronger.", "Medicine freezes.", "It speeds up the reaction."], "Lower rate."),
    ("Why is a 'disappearing cross' experiment repeated three times?", "To check that the times are reliable and find an average.", ["To make it slower.", "To use more chemicals.", "To change the result."], "Repeat trials."),
    ("Why does a car's catalytic converter work better once the engine is warm?", "Higher temperature makes the reactions on the catalyst faster.", ["Heat destroys pollutants directly.", "Cold catalysts are used up.", "Warm cars make less exhaust."],
     "Temperature and catalysts both raise rate."),
])


def body():
    think = ("<p><b>More effective collisions per second means a faster reaction.</b></p>"
             "<ul><li>Particles must collide with enough energy (activation energy) and the right orientation.</li>"
             "<li>Faster: higher temperature, higher concentration or pressure, more surface area, a catalyst.</li>"
             "<li>Average rate = amount of product (or reactant used) ÷ time.</li></ul>")
    ex = [("60 mL of gas in 30 s. Rate?", ["60 ÷ 30"], "2 mL/s"),
          ("Why does warm acid react faster?", ["Faster particles", "More energetic collisions"], "more effective collisions")]
    mist = ["Thinking a catalyst is used up.", "Thinking a faster reaction makes more product.", "Reading a longer time as a faster reaction."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Collision theory", B1 + [(g_factor, 12)]),
        ("Factors that change the rate", [(g_factor, 12), (g_cat, 4), (g_rate, 4)]),
        ("Calculating rates", [(g_rate, 14), (g_data, 6)]),
        ("Rate experiments", [(g_data, 16), (g_rate, 4)]),
        ("Explaining evidence", B5 + [(g_data, 8), (g_factor, 4), (g_rate, 3)]),
    ])
    make("chemistry", "reaction-rates", 10, "HS-PS1-5",
         "Apply scientific principles and evidence to provide an explanation about the effects of changing the temperature or concentration of the reacting particles on the rate at which a reaction occurs.",
         "Reaction Rates",
         "Reaction Rate Worksheets: Collision Theory, Temperature and Catalysts (High School Chemistry)",
         "Reaction Rates",
         "Free high school chemistry worksheets on reaction rates (NGSS HS-PS1-5): collision theory, temperature, concentration, surface area, catalysts and rate data. 100 questions with answers.",
         "More effective collisions, faster rate.",
         "Temperature, concentration, surface area and catalysts change how fast a reaction goes.",
         body(),
         [("What factors affect reaction rate?", "Temperature, concentration (or pressure for gases), surface area and catalysts."),
          ("How does collision theory explain rates?", "Reactions happen when particles collide with enough energy and the right orientation. Anything that makes these collisions more frequent speeds up the reaction."),
          ("How do you calculate an average rate?", "Divide the amount of product made (or reactant used) by the time taken, for example mL of gas per second.")],
         sets)


if __name__ == "__main__":
    main()
