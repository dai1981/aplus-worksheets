# -*- coding: utf-8 -*-
"""
US Grade 7 Science: Human Impact on the Environment (MS-ESS3-3, MS-ESS3-4)
  python tools/gen_us_science_g7_human_impact_on_the_environment.py
Apply scientific principles to design a method for monitoring and minimizing a human impact on the environment
(water pollution, air pollution, habitat loss, trash), and construct an argument that increases in human population
and per-capita consumption of natural resources impact Earth's systems. Total impact = population x use per person.
Wrong answers come from real mistakes: "only population matters, not how much each person uses",
"one person's choices never matter", "monitoring is not needed once a solution is built".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People, comma

U = Unit(70117)
R = U.R
P = People(R)


def g_total():
    who = P.next()[0]
    pop = R.choice([1000, 2000, 5000, 10000, 20000])
    per = R.choice([2, 3, 4, 5])
    thing = R.choice([("kg of trash per person each day", "kg of trash each day"), ("liters of gasoline per person each week", "liters each week"),
                      ("kg of plastic per person each month", "kg each month")])
    tot = pop * per
    k = R.choice(["total", "double", "cut"])
    if k == "total":
        return item("%s's town has %s people. Each person makes about %d %s. About how much does the town make in all?" % (who, comma(pop), per, thing[0]), "%s %s" % (comma(tot), thing[1]),
                    ["%s %s" % (comma(pop), thing[1]), "%s %s" % (comma(pop + per), thing[1]), "%s %s" % (comma(tot * 10), thing[1])], "%s × %d = %s." % (comma(pop), per, comma(tot)))
    if k == "double":
        return item("%s's town has %s people who each use %d %s. If the population doubles and each person uses the same amount, what is the new total?" % (who, comma(pop), per, thing[0]),
                    "%s %s" % (comma(tot * 2), thing[1]), ["%s %s" % (comma(tot), thing[1]), "%s %s" % (comma(tot * 4), thing[1]), "%s %s" % (comma(pop * 2), thing[1])],
                    "Twice the people × the same use = twice the total.")
    if per < 2:
        return None
    return item("%s's town has %s people who each use %d %s. If everyone cuts use in half, what is the new total?" % (who, comma(pop), per, thing[0]),
                "%s %s" % (comma(tot // 2), thing[1]) if tot % 2 == 0 else None, ["%s %s" % (comma(tot), thing[1]), "%s %s" % (comma(pop // 2), thing[1]), "%s %s" % (comma(tot * 2), thing[1])],
                "Halving use per person halves the total, even with the same population.")


IMPACT = [("Fertilizer runs off farms into a river.", "algae blooms that use up oxygen and kill fish", "planting grass buffer strips along the river and using less fertilizer"),
          ("Rainwater carries oil and trash from parking lots into streams.", "polluted streams", "rain gardens and permeable pavement that soak up runoff"),
          ("Cars and factories burn fossil fuels.", "air pollution and more carbon dioxide", "public transit, electric vehicles and cleaner power"),
          ("Forests are cleared for new houses.", "habitat loss for animals", "keeping protected green spaces and wildlife corridors"),
          ("Plastic bags blow into the ocean.", "animals swallowing or getting tangled in plastic", "reusable bags and bans on single-use plastic"),
          ("A factory releases hot water into a lake.", "warmer water with less oxygen for fish", "cooling the water in ponds before it is released")]


def g_impact():
    act, harm, fix = R.choice(IMPACT)
    who = P.next()[0]
    if R.random() < 0.5:
        return item("%s observes: “%s” What impact can this have?" % (who, act), harm, R.sample([i[1] for i in IMPACT if i[1] != harm], 3), "Human activities can change Earth's systems.")
    return item("%s's class studies this problem: “%s” Which solution would best reduce the impact?" % (who, act), fix, R.sample([i[2] for i in IMPACT if i[2] != fix], 3),
                "A good solution targets the cause of the impact.")


def g_monitor():
    who = P.next()[0]
    cases = [("whether a rain garden reduces stream pollution", "measure pollution in the stream before and after the rain garden is built"),
             ("whether a new bus line reduces air pollution", "measure air quality and traffic for several months before and after"),
             ("whether a recycling program reduces trash", "weigh the trash sent to the landfill each week before and after"),
             ("whether fewer fish die after a farm uses less fertilizer", "count fish and measure oxygen in the river over several years"),
             ("whether a wildlife bridge reduces animal deaths", "count animals hit on the road before and after the bridge")]
    goal, a = R.choice(cases)
    return item("%s wants to know %s. What is the best way to monitor this?" % (who, goal), a,
                ["ask one neighbor what they think", "check once on a single day", "assume it works without data"], "Monitoring uses measurements over time, before and after.")


def g_graph():
    yrs = ["1950", "1970", "1990", "2010", "2020"]
    popn = [2.5, 3.7, 5.3, 6.9, 7.8]
    who = P.next()[0]
    ch = bar_chart(yrs, popn, "billions of people", "bar graph of world population", ymax=8, step=2, w=320)
    k = R.choice(["trend", "diff", "claim"])
    if k == "trend":
        return item(fig(ch) + "What trend does %s's graph of world population show?" % who, "The human population has increased a lot since 1950.",
                    ["It has decreased.", "It has stayed the same.", "It went up and then down to 1950 levels."], "From 2.5 billion to 7.8 billion.")
    if k == "diff":
        return item(fig(ch) + "Using %s's graph, about how many more people were there in 2020 than in 1950?" % who, "about 5.3 billion", ["about 7.8 billion", "about 2.5 billion", "about 10.3 billion"],
                    "7.8 − 2.5 = 5.3 billion.")
    return item(fig(ch) + "Which claim does %s's graph support best?" % who, "As the population grows, more resources are used unless each person uses less.",
                ["Population growth has no effect on resources.", "Fewer people means more pollution.", "Resource use depends only on the weather."], "Total use = number of people × use per person.")


B1 = bank([
    ("What is per-capita consumption?", "the amount of a resource used per person", ["the total population", "the number of countries", "the amount of rain"], "Per capita means per person."),
    ("Which two things together determine a population's total use of resources?", "the number of people and how much each person uses", ["only the number of people", "only the weather", "only the size of the country"],
     "Total = people × use per person."),
    ("Why is monitoring important after a solution is put in place?", "to check with data whether it actually reduces the impact", ["it is not needed", "to make the solution more expensive", "to stop the solution"],
     "Data shows if it works."),
    ("Which is an example of reducing per-capita consumption?", "turning off lights and taking shorter showers", ["using more plastic bags", "leaving the car running", "buying more single-use items"], "Using less per person."),
    ("How can a growing population affect habitats?", "More land is used for homes, farms and roads.", ["Habitats grow larger.", "Nothing happens.", "Animals get more space."], "Land use increases."),
    ("What is runoff pollution?", "pollution carried by rainwater from land into streams and lakes", ["pollution from airplanes only", "noise from cars", "light at night"], "Fertilizer and oil wash into water."),
    ("Which change helps reduce air pollution?", "using renewable energy instead of burning coal", ["building more coal plants", "driving farther", "burning trash"], "Less burning, cleaner air."),
    ("Can individual choices matter for the environment?", "Yes. Many people making small changes adds up.", ["No, never.", "Only governments matter.", "Only in big cities."], "Per-capita use times many people."),
])
B5 = bank([
    ("Ava's school puts in recycling bins. Landfill trash drops from 400 kg to 250 kg a week. How much less trash is that?", "150 kg a week", ["250 kg", "650 kg", "400 kg"], "400 − 250 = 150 kg."),
    ("Leo argues that a city of 1 million people using 100 liters of water each per day uses more water than a city of 2 million using 40 liters each. Is he right?", "Yes: 100 million liters vs. 80 million liters.", ["No, the bigger city always uses more.", "They use the same amount.", "You cannot compare them."],
     "Multiply people by use per person."),
    ("Mia designs a sensor to measure the cloudiness (turbidity) of a creek after storms. What is she doing?", "monitoring a human impact on water quality", ["causing pollution", "measuring rainfall only", "counting fish"], "Monitoring tracks changes."),
    ("Why should scientists collect data for several years when monitoring a river?", "Natural changes from year to year could hide or exaggerate the effect.", ["One day is enough.", "Rivers never change.", "Data is not useful."],
     "Long-term data is stronger evidence."),
    ("A town's population stays the same, but each person buys twice as much plastic. What happens to the town's plastic waste?", "It doubles.", ["It stays the same.", "It is cut in half.", "It goes to zero."],
     "Per-capita use matters as much as population."),
])


def body():
    think = ("<p>Human activities change Earth's systems: pollution of air and water, habitat loss, trash and more carbon dioxide.</p>"
             "<p>The total impact depends on two things: <b>how many people</b> there are and <b>how much each person uses</b> (per-capita consumption).<br><b>Total use = population × use per person</b></p>"
             "<p>People design solutions to <b>minimize</b> impacts (rain gardens, recycling, public transit, wildlife corridors) and <b>monitor</b> them with data collected before and after, over time.</p>")
    ex = [("5,000 people each make 2 kg of trash a day. Total?", ["5,000 × 2"], "10,000 kg a day"),
          ("How can you check if a rain garden helps a stream?", ["Measure before and after."], "Monitor stream pollution over time.")]
    mist = ["Thinking only population matters, not how much each person uses.",
            "Thinking one person's choices never matter.",
            "Skipping monitoring after a solution is built."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("People and resources", B1 + [(g_total, 12)]),
        ("Population and consumption", [(g_total, 12), (g_graph, 8)]),
        ("Impacts and solutions", [(g_impact, 14), (g_monitor, 6)]),
        ("Monitoring", [(g_monitor, 10), (g_impact, 6), (g_graph, 4)]),
        ("Making arguments", B5 + [g_total, g_impact, g_monitor, g_graph]),
    ])
    make("grade-7", "human-impact-on-the-environment", 17, "MS-ESS3-3",
         "Apply scientific principles to design a method for monitoring and minimizing a human impact on the environment.",
         "Human Impact on the Environment",
         "Grade 7 Human Impact Worksheets: Population, Consumption, Pollution and Solutions",
         "Human Impact",
         "Free middle school science worksheets on human impact on the environment (NGSS MS-ESS3-3, MS-ESS3-4): population growth and per-capita consumption, pollution, solutions and monitoring with data. 100 practice questions with answers.",
         "Total impact = number of people × use per person.",
         "Growing populations and higher consumption increase impacts. Solutions and monitoring can reduce them.",
         body(),
         [("How do population and consumption affect the environment?", "The total impact equals the number of people times how much each person uses. Both a bigger population and more use per person increase the impact."),
          ("How can people reduce their impact?", "By using less per person, recycling, using clean energy and transit, and protecting habitats."),
          ("Why do we monitor solutions?", "Measurements before and after, over time, show whether a solution really reduces the impact.")],
         sets)


if __name__ == "__main__":
    main()
