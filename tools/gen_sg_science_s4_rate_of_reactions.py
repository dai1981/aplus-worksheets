# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Chemistry (6092), Topic 10: Rate of Reactions
  python tools/gen_sg_science_s4_rate_of_reactions.py
Measuring the rate of reaction (gas volume or mass loss against time, time for a precipitate to form), interpreting rate graphs,
the effect of concentration, pressure, surface area (particle size), temperature and catalysts, explained by collision theory
and activation energy; enzymes as biological catalysts.
UK and US rate makers are reused (Singapore names, cm³ for volumes); rate graphs are drawn here.
Wrong answers come from real mistakes: "a catalyst is used up", "larger lumps react faster", "a higher temperature gives more
product", "particles collide harder only, not more often", "the gradient at the end is the fastest".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex, graph, fig

LV, SUBJ, SORT = 4, "Chemistry", 12
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

CM3 = [(r"\bmL\b", "cm³"), (r"\bmilliliters?\b", "cm³")]
uk_cross = src("gen_uk_science_y11_rates_and_equilibrium", "g_cross")
uk_mean = src("gen_uk_science_y11_rates_and_equilibrium", "g_mean")
uk_coll = src("gen_uk_science_y11_rates_and_equilibrium", "g_coll")
us_factor = src("gen_us_science_chem_reaction_rates", "g_factor", rep=CM3)
us_rate = src("gen_us_science_chem_reaction_rates", "g_rate", rep=CM3)


def curve(vmax, k, tmax):
    return [(t, vmax * (1 - math.exp(-k * t))) for t in [i * tmax / 40 for i in range(41)]]


DONE = set()


def g_curve():
    vmax = R.choice([40, 48, 60, 80, 96, 120])
    tend = R.choice([60, 80, 100, 120])
    k = 5 / tend
    tmax = tend * 1.5
    pts = curve(vmax, k, tmax)
    ys = 20 if vmax > 60 else 10
    svg = graph(pts, tmax, ((vmax + ys) // ys) * ys, tmax / 6, ys, "time / s", "volume of gas / cm³", label="rate graph")
    q = fig(svg) + "Magnesium ribbon reacts with excess dilute hydrochloric acid. The graph shows the volume of hydrogen collected. "
    kk = R.choice(["final", "half", "at", "avg", "when", "fast", "why_flat"])
    if kk in ("when", "fast", "why_flat"):
        if kk in DONE:
            return None
        DONE.add(kk)
    if kk in ("at", "avg"):
        t = R.choice([x for x in range(int(tmax / 6), int(tmax), int(tmax / 6)) if x <= tend])
        v = vmax * (1 - math.exp(-k * t))
        if kk == "at":
            return nq(q + "About what volume of hydrogen has been collected after %d s?" % t, v, [vmax, vmax - v, v / 2], " cm³",
                      "Read up from %d s to the curve, then across to the volume axis." % t, sf=2)
        return nq(q + "Using the graph, what is the average rate of reaction over the first %d s?" % t, v / t, [t / v, v, vmax / t], " cm³/s",
                  "Average rate = volume ÷ time = %s ÷ %d." % (trim("%.2g" % v), t), sf=2)
    if kk == "final":
        return nq(q + "What is the total volume of hydrogen made?", vmax, [vmax / 2, tmax, vmax * 2], " cm³", "The graph levels off at %d cm³ when the magnesium is used up." % vmax)
    if kk == "when":
        return tq(q + "When is the reaction fastest?", "at the start", ["at the end", "halfway through", "it is the same throughout"],
                  "The curve is steepest at the start, when the concentration of acid and the amount of magnesium are greatest.")
    if kk == "fast":
        return tq(q + "Why does the graph become less steep as time goes on?", "The magnesium is being used up, so there are fewer collisions per second.",
                  ["The catalyst is used up.", "The temperature rises.", "The acid becomes more concentrated."], "The rate falls as reactants are used up.")
    if kk == "why_flat":
        return tq(q + "Why does the graph become flat?", "The reaction has stopped because the magnesium has all reacted.", ["The gas syringe is full.", "The acid has turned into hydrogen.", "The reaction has become faster."],
                  "The acid is in excess, so the magnesium is the limiting reactant.")
    th = math.log(2) / k
    return nq(q + "About how long does it take to collect half of the total volume of hydrogen?", th, [tend, tmax / 2, th * 2], " s",
              "Half of %d cm³ is %d cm³; read across to the curve and down to the time axis." % (vmax, vmax // 2), sf=2)


CTX = {
    "mg": ("magnesium-acid", "hydrogen", [
        ("using magnesium powder instead of ribbon (same mass)", "faster", "the same", "The powder has a larger surface area, so there are more collisions per second; the amount of magnesium is unchanged."),
        ("using acid at a higher temperature", "faster", "the same", "Particles have more kinetic energy, so more collisions per second have energy at least equal to the activation energy."),
        ("using a more concentrated acid (still in excess)", "faster", "the same", "There are more acid particles per unit volume, so collisions are more frequent; the magnesium still limits the product."),
        ("using half the mass of magnesium ribbon", None, "halved", "The acid is in excess, so the magnesium limits the amount of hydrogen."),
        ("using twice the mass of magnesium ribbon (acid still in excess)", None, "doubled", "More magnesium gives more hydrogen in total."),
        ("with the acid cooled in ice", "slower", "the same", "Fewer particles have enough energy to react, and they collide less often."),
        ("using a more dilute acid (still in excess)", "slower", "the same", "There are fewer acid particles per unit volume, so collisions are less frequent.")]),
    "caco3": ("marble chip", "carbon dioxide", [
        ("using powdered marble instead of large chips (same mass)", "faster", "the same", "Powder has a larger surface area, so there are more collisions per second."),
        ("using larger marble chips (same mass)", "slower", "the same", "Larger chips have a smaller surface area, so there are fewer collisions per second."),
        ("using acid at 50 °C instead of 25 °C", "faster", "the same", "More collisions per second have energy at least equal to the activation energy."),
        ("using half the mass of marble chips (acid still in excess)", None, "halved", "The marble is the limiting reactant."),
        ("using a more dilute acid (still in excess)", "slower", "the same", "There are fewer acid particles per unit volume, so collisions are less frequent."),
        ("using acid at 15 °C instead of 25 °C", "slower", "the same", "Particles have less energy and collide less often.")]),
    "h2o2": ("hydrogen peroxide", "oxygen", [
        ("with manganese(IV) oxide added as a catalyst", "faster", "the same", "A catalyst lowers the activation energy but does not change the amount of hydrogen peroxide that decomposes."),
        ("with a larger mass of the same catalyst powder", "faster", "the same", "More catalyst surface gives more successful collisions per second, but the amount of product is unchanged."),
        ("using the same volume of hydrogen peroxide solution that is twice as concentrated", "faster", "doubled", "More hydrogen peroxide particles per unit volume; twice the concentration gives twice the oxygen."),
        ("using half the volume of the same hydrogen peroxide solution", None, "halved", "There is half as much hydrogen peroxide to decompose."),
        ("with the solution warmed to 40 °C", "faster", "the same", "Higher temperature raises the rate but not the amount of product.")]),
}


def g_chg():
    k = R.choice(sorted(CTX))
    name, gas, rs = CTX[k]
    c, rate, vol, why = R.choice(rs)
    if rate and R.random() < 0.5:
        return tq("The %s experiment is repeated %s. How does the initial rate of reaction change?" % (name, c), rate,
                  [x for x in ("faster", "slower", "no change", "the reaction stops") if x != rate], why)
    return tq("The %s experiment is repeated %s. How does the total volume of %s collected change?" % (name, c, gas), vol,
              [x for x in ("the same", "halved", "doubled", "zero") if x != vol], why)


FACT = [("increasing the concentration of a solution", "More particles per unit volume, so more frequent collisions."),
        ("increasing the pressure of a gas", "Gas particles are closer together, so they collide more often."),
        ("increasing the surface area of a solid (smaller pieces)", "More particles are exposed, so there are more collisions per second."),
        ("increasing the temperature", "Particles move faster and have more energy: more frequent collisions and a larger fraction with energy above the activation energy."),
        ("adding a catalyst", "It provides an alternative pathway with a lower activation energy, so more collisions are effective.")]
g_fact = rows(R, FACT, "Using collision theory, why does %s increase the rate of reaction?", "Which change to a reaction is explained by this? “%s”")

POOL1 = pool(R, [
    ("What is meant by the rate of a reaction?", "how fast reactants are used up or products are formed per unit time", ["the total amount of product", "the temperature of the reaction", "the activation energy"], "Units such as cm³/s or g/s."),
    ("Which two things must happen for particles to react?", "They must collide, with energy at least equal to the activation energy.", ["They must be the same colour.", "They must be in the same state.", "They must be at 100 °C."], "Only effective collisions lead to reaction."),
    ("What is a catalyst?", "a substance that speeds up a reaction without being chemically changed or used up at the end", ["a substance that slows a reaction", "a reactant that is used up", "a product of the reaction"], "It lowers the activation energy."),
    ("What are enzymes?", "biological catalysts made of protein", ["sugars that give energy", "inorganic catalysts", "products of combustion"], "They work best at an optimum temperature and pH."),
    ("Why do enzymes stop working above about 45 °C?", "They are denatured: their shape changes so the substrate no longer fits.", ["They melt.", "They are used up.", "They become catalysts for other reactions."], "Most human enzymes work best near 37 °C."),
    ("How can the rate of a reaction that gives off a gas be measured?", "by collecting the gas in a gas syringe and recording its volume at regular times", ["by weighing the gas syringe", "by measuring the pH once", "by checking the colour once at the end"], "Or by measuring the loss of mass on a balance."),
    ("Why does the mass of a flask of marble chips and acid fall during the reaction?", "Carbon dioxide gas escapes into the air.", ["The marble evaporates.", "The acid boils away.", "Water is destroyed."], "A cotton wool plug lets gas out but stops acid spray."),
    ("In the sodium thiosulfate and acid reaction, how is the rate measured?", "by timing how long it takes for a cross under the flask to disappear as a sulfur precipitate forms", ["by collecting hydrogen", "by measuring a temperature drop", "by weighing the flask"], "Rate ∝ 1/time."),
    ("Why does a lump of calcium carbonate react more slowly than the same mass of powder?", "The lump has a smaller surface area exposed to the acid.", ["The lump has less mass.", "The powder is a different substance.", "The lump is hotter."], "Fewer collisions per second."),
    ("Why is food kept in a refrigerator?", "Lower temperature slows down the reactions that make food go bad.", ["Cold kills all bacteria.", "Cold adds a catalyst.", "Cold removes oxygen."], "Rate falls as temperature falls."),
])
POOL5 = pool(R, [
    ("Why is there a risk of explosions in flour mills and coal mines?", "Fine dust has a very large surface area, so it can burn extremely quickly.", ["Flour is a catalyst.", "Dust has a high activation energy.", "The mills are too cold."], "A spark can ignite the dust cloud."),
    ("Manganese(IV) oxide speeds up the decomposition of hydrogen peroxide. How can you show it is a catalyst?", "Filter, dry and weigh it after the reaction: its mass is unchanged.", ["Show that it changes colour.", "Show that it dissolves.", "Show that more oxygen is made."], "A catalyst is not used up."),
    ("Adding a catalyst to a reaction does not change the total volume of gas collected. Why?", "A catalyst changes only the rate, not the amount of reactants that react.", ["Catalysts are used up.", "Catalysts make more product.", "The gas escapes."], "The same amount of limiting reactant."),
    ("Why does increasing the temperature by 10 °C often roughly double the rate?", "Many more particles have energy greater than the activation energy, and they collide more often.", ["Particles become larger.", "Activation energy is halved.", "Concentration doubles."], "Mostly due to more energetic collisions."),
    ("50 cm³ of gas is collected in the first 20 s. What is the average rate over this time?", "2.5 cm³/s", ["1000 cm³/s", "0.4 cm³/s", "70 cm³/s"], "50 ÷ 20."),
    ("Two experiments use the same mass of zinc with excess acid. Which change gives a graph with a steeper start but the same final volume?", "using zinc powder instead of granules", ["using half the mass of zinc", "using a larger flask", "using a smaller syringe"], "Surface area changes the rate only."),
    ("In industry, why are catalysts important?", "They make reactions faster at lower temperatures, saving energy and cost.", ["They increase the yield of every reaction to 100%.", "They are cheap to throw away.", "They slow reactions down for safety."], "Iron in the Haber process; catalytic converters in cars."),
    ("Hydrogen peroxide decomposes faster in a solution containing liver. Why?", "Liver contains the enzyme catalase, a biological catalyst.", ["Liver adds oxygen.", "Liver heats the solution to boiling.", "Liver removes water."], "Catalase is found in many living cells."),
])


def main():
    sets = U.sets([
        ("Rate of reaction and collision theory", [(POOL1, 7), (g_fact, 6), (uk_coll, 5), (us_factor, 4)]),
        ("Measuring rate", [(uk_mean, 7), (us_rate, 6), (uk_cross, 5), (POOL1, 3)]),
        ("Rate graphs", [(g_curve, 14), (g_chg, 6)]),
        ("Factors affecting rate", [(g_chg, 9), (g_fact, 4), (us_factor, 6), (uk_coll, 3)]),
        ("Catalysts and exam-style questions", [(POOL5, 8), (g_curve, 5), (g_chg, 4), (uk_cross, 3), (us_rate, 3)]),
    ])
    make_ol(LV, SUBJ, "rate-of-reactions", SORT, "Rate of Reactions",
            "Describe practical methods for measuring the rate of a reaction, including collecting gas and measuring changes in mass or the time for a precipitate to "
            "appear; interpret data and graphs from rate experiments; describe and explain the effects of concentration, pressure, surface area (particle size), "
            "temperature and catalysts on the rate of reaction in terms of collision theory and activation energy; describe enzymes as biological catalysts (summary of the "
            "Singapore-Cambridge O-Level Chemistry 6092 syllabus).",
            "Rate of Reactions", "Rate of reactions",
            "Free Secondary 4 O-Level Chemistry worksheets on rate of reactions: measuring rate, rate graphs, collision theory, concentration, surface area, temperature, "
            "catalysts and enzymes. 100 questions with answers.",
            "More effective collisions per second = faster.", "A catalyst lowers the activation energy and is not used up.",
            "<p><b>Particles react when they collide with enough energy.</b></p><ul>"
            "<li>Rate = amount of product formed (or reactant used) ÷ time. The gradient of a volume-time graph is the rate; it is steepest at the start.</li>"
            "<li>Higher concentration, pressure or surface area: more frequent collisions. Higher temperature: more frequent and more energetic collisions.</li>"
            "<li>A catalyst gives a pathway with a lower activation energy. It does not change the amount of product.</li>"
            "<li>The total amount of product depends only on the limiting reactant.</li></ul>",
            [("60 cm³ of gas in 30 s. Average rate?", ["60 ÷ 30"], "2 cm³/s"),
             ("Mg powder instead of ribbon, same mass. Graph?", ["larger surface area: steeper start", "same mass of Mg: same final volume"], "steeper, same final height")],
            ["Thinking a catalyst is used up or makes more product.", "Saying larger lumps react faster.", "Saying a higher temperature makes more product (it only makes it faster).",
             "Explaining temperature only by 'harder collisions' and forgetting the activation energy."],
            [("How does temperature affect the rate of reaction?", "At a higher temperature particles move faster, so they collide more often and a larger fraction of collisions have energy at least equal to the activation energy."),
             ("How does a catalyst work?", "It provides an alternative reaction pathway with a lower activation energy, so more collisions are successful. It is chemically unchanged at the end."),
             ("How do you read a rate graph?", "The steeper the curve, the faster the reaction. Where the curve becomes flat, the reaction has stopped; the final height shows the total amount of product.")],
            sets)


if __name__ == "__main__":
    main()
