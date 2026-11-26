# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Natural Resources and Hazards (HS-ESS3-1, HS-ESS3-2)
  python tools/gen_us_science_ess_natural_resources_and_hazards.py
How resources, hazards and climate shape where and how people live; renewable and nonrenewable resources; ore grade;
reducing the risk of natural hazards; and comparing energy and mineral solutions with cost-benefit ratios and
payback time.
Wrong answers come from real mistakes: "oil and coal are renewable", "a cheaper option is always better",
"hazards can be prevented completely", "a higher ore grade needs more rock".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90414)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


WHERE = [("Rich soil left by river floods", "Early farming villages grew along the Nile, Tigris and Euphrates rivers."),
         ("A deep natural harbor", "A port city grew up and became a center of trade."),
         ("Large deposits of coal and iron ore", "Steel-making cities grew nearby during the Industrial Revolution."),
         ("A gold discovery in the hills", "Thousands of people moved in quickly and new towns appeared."),
         ("Long droughts that dried up farmland", "People abandoned farms and migrated to other regions."),
         ("Frequent volcanic ash that weathers into fertile soil", "Farmers settle on the slopes of active volcanoes despite the danger."),
         ("Rising sea level and stronger storm surges", "Some coastal towns are building sea walls or moving inland."),
         ("A large aquifer under dry plains", "Wells made irrigated farming possible in an otherwise dry region.")]


@safe
def g_where():
    s, a = R.choice(WHERE)
    k = R.random() < 0.6
    if not once(("wh", s, k)):
        return None
    if k:
        return item("Natural factor: %s. How did this influence human activity?" % s, a, R.sample([x[1] for x in WHERE if x[1] != a], 3), "Resources, hazards and climate shape where people live.")
    return item("Which natural factor best explains this? %s" % a, s + ".", [x[0] + "." for x in R.sample([x for x in WHERE if x[0] != s], 3)], "Match the human activity to the natural factor.")


RENEW = ["solar energy", "wind energy", "hydroelectric power", "geothermal energy", "tidal energy", "sustainably harvested wood"]
NONRENEW = ["coal", "oil", "natural gas", "uranium", "copper ore", "phosphate rock", "gravel"]


@safe
def g_res():
    k = R.random() < 0.6
    if k:
        a = R.choice(RENEW)
        w = R.sample(NONRENEW, 3)
        if not once(("rn", a, tuple(sorted(w)))) or not once(("rna", a), 3):
            return None
        return item("Which of these is a renewable resource?", a, w, "Renewable resources are replaced by nature on a human time scale.")
    a = R.choice(NONRENEW)
    w = R.sample(RENEW, 3)
    if not once(("nr", a, tuple(sorted(w)))) or not once(("nra", a), 2):
        return None
    return item("Which of these is a nonrenewable resource?", a, w, "Nonrenewable resources form over millions of years or are not replaced at all.")


@safe
def g_ore():
    metal = R.choice(["copper", "zinc", "nickel", "lead"])
    grade = R.choice([0.5, 1, 2, 4, 5])
    t = R.choice([10, 20, 50, 100, 200])
    rock = t * 100 / grade
    if not once(("or", metal, grade, t)):
        return None
    tn = lambda v: "%s tonne%s" % (num(v, 3), "" if num(v, 3) == "1" else "s")
    g = tn(rock)
    return item("An ore is %s%% %s by mass. How much ore must be mined to get %d tonnes of %s?" % (num(grade, 2), metal, t, metal), g,
                uniq(g, [tn(t * grade / 100), tn(t * grade), tn(t / grade), tn(rock * 10)]),
                "%d ÷ %s = %s tonnes. Lower grades need much more rock." % (t, num(grade / 100, 3), num(rock)))


HAZ = [("earthquakes", "building codes that make structures flexible and strong"), ("river floods", "zoning that keeps homes off the floodplain"),
       ("hurricanes", "hurricane-rated roofs and storm shutters"), ("volcanic eruptions", "monitoring gas and ground swelling to warn people"),
       ("tsunamis", "ocean sensors linked to warning sirens"), ("wildfires", "clearing brush to make defensible space around homes"),
       ("landslides", "drainage and retaining walls on steep slopes"), ("droughts", "water conservation and storing water in reservoirs")]


@safe
def g_haz():
    h, m = R.choice(HAZ)
    k = R.random() < 0.55
    if not once(("hz", h, k)):
        return None
    if k:
        return item("Which action best reduces the risk to people from %s?" % h, m, R.sample([x[1] for x in HAZ if x[1] != m], 3), "Hazards cannot be stopped, but their harm can be reduced.")
    return item("A community plans %s. Which hazard is this mainly meant to reduce?" % m, h, R.sample([x[0] for x in HAZ if x[0] != h], 3), "Match the plan to the hazard.")


@safe
def g_cb():
    who = P.next()[0]
    names = R.choice([["Solar farm", "Wind farm", "Gas plant"], ["Recycle copper", "New open-pit mine", "Deep underground mine"],
                      ["Geothermal plant", "Coal plant", "Hydro dam"], ["Rooftop solar", "Better insulation", "New furnace"]])
    rows = []
    for n in names:
        c = R.choice([2, 4, 5, 8, 10, 12, 16, 20])
        b = c * R.choice([0.5, 0.75, 1.25, 1.5, 2, 2.5, 3])
        rows.append((n, c, b))
    ratios = [b / c for _, c, b in rows]
    if len(set(ratios)) < 3 or not once(("cb", tuple(rows))):
        return None
    tab = table(["Option", "Cost (million $)", "Benefit (million $)"], [[n, num(c), num(b, 2)] for n, c, b in rows])
    k = R.choice(["best", "ratio", "cheap"])
    if k == "best":
        a = max(rows, key=lambda r: r[2] / r[1])[0]
        return item(tab + "%s compares three options. Which has the best benefit-to-cost ratio?" % who, a, [r[0] for r in rows if r[0] != a] + ["They are all the same."],
                    "Ratios: " + ", ".join("%s %s" % (n, num(b / c, 2)) for n, c, b in rows) + ".")
    if k == "ratio":
        n, c, b = R.choice(rows)
        g = num(b / c, 2)
        return item(tab + "What is the benefit-to-cost ratio for the \"%s\" option in %s's table?" % (n, who), g, uniq(g, [num(c / b, 2)] + [num(x, 2) for x in (b - c, b + c, b * c) if x > 0]),
                    "%s ÷ %s = %s." % (num(b, 2), num(c), g))
    cheap = min(rows, key=lambda r: r[1])
    best = max(rows, key=lambda r: r[2] / r[1])
    if cheap[0] == best[0]:
        return None
    return item(tab + "%s says, \"%s is the cheapest option, so it is the best choice.\" What is wrong with this claim?" % (who, cheap[0]), "It ignores the benefits; the \"%s\" option has a higher benefit-to-cost ratio." % best[0],
                ["Nothing; the cheapest option is always best.", "The most expensive option is always best.", "Costs do not matter at all."], "Compare benefit ÷ cost, not cost alone.")


@safe
def g_pay():
    what = R.choice(["solar panels on a school", "a heat pump for a home", "LED lights in an office", "insulation in an old house", "a wind turbine on a farm"])
    cost = R.choice([1200, 2400, 3000, 4800, 6000, 9000, 12000, 18000])
    save = R.choice([300, 400, 500, 600, 750, 800, 1000, 1200, 1500, 2000])
    yrs = cost / save
    if yrs != int(yrs) or yrs < 2 or yrs > 20 or not once(("py", cost, save)):
        return None
    g = "%d years" % yrs
    return item("Installing %s costs $%s and saves $%s per year in energy. What is the payback time?" % (what, num(cost), num(save)), g,
                uniq(g, ["%d years" % (yrs * 2), "%s years" % num(save / cost * 100, 1), "%d years" % (yrs + 1), "1 year"]), "$%s ÷ $%s per year = %d years." % (num(cost), num(save), yrs))


B1 = bank([
    ("What is a natural resource?", "a material or source of energy from Earth that people use", ["anything made in a factory", "only gold and silver", "a type of weather"], "Water, soil, minerals, fuels."),
    ("Why are fossil fuels called nonrenewable?", "They take millions of years to form, much longer than people use them.", ["They are made in labs.", "They regrow each year.", "They never run out."], "Time scale."),
    ("Why were many early cities built along rivers?", "Rivers gave fresh water, fertile soil and transport.", ["Rivers keep away all hazards.", "Rivers are always dry.", "Rivers make gold."], "Resources shape settlement."),
    ("Why are mineral resources found only in certain places?", "They form by specific geologic processes, such as magma cooling or sediments collecting.", ["They are spread evenly everywhere.", "People put them there.", "They fall from space every year."], "Uneven distribution."),
    ("Can people stop earthquakes from happening?", "No, but they can reduce the damage with good planning and building design.", ["Yes, with fences.", "Yes, by digging deep holes.", "Yes, by cutting down trees."], "Reduce risk."),
    ("How has climate change affected human activity?", "Droughts, floods and rising seas are changing where people farm and live.", ["It has had no effect.", "It only affects animals.", "It makes all land wetter."], "Climate influences people."),
    ("What does ore grade mean?", "the percent of the useful metal in the rock", ["how hard the rock is", "the color of the rock", "how deep the mine is"], "Higher grade, less rock."),
    ("Why is recycling metals often better than mining new ore?", "It uses less energy and causes less land damage.", ["Recycled metal is weaker.", "Mining has no costs.", "Recycling uses more energy."], "Cost and benefit."),
])
B5 = bank([
    ("When comparing energy solutions, which factors should be included?", "economic, social and environmental costs and benefits", ["only the price of building it", "only how it looks", "only the number of workers"], "Full cost-benefit."),
    ("A coal plant is cheaper to build than a wind farm. Why might a town still choose the wind farm?", "It has no fuel costs and less air pollution over its life.", ["Wind farms run on coal.", "Cheaper is always worse.", "Wind is nonrenewable."], "Long-term benefits."),
    ("Why do engineers consider the risk of hazards when siting a power plant?", "A flood or earthquake could damage it and harm people.", ["Hazards only affect farms.", "Power plants cannot be damaged.", "It is required to make it cheaper."], "Hazards and design."),
    ("Which choice best reduces both mining and waste?", "reducing use and recycling metals", ["opening more mines", "burying old electronics", "using more single-use products"], "Conservation."),
    ("Why might two experts disagree about the best energy option?", "They may weigh costs and benefits differently, such as price versus pollution.", ["One of them cannot do math.", "There is only one fact.", "All options are identical."], "Values and trade-offs."),
])


def body():
    think = ("<p><b>Resources and hazards shape where and how people live.</b></p>"
             "<ul><li>People settle near water, fertile soil, minerals and fuels. Hazards and climate change can force them to adapt or move.</li>"
             "<li>Renewable resources (sun, wind, water) are replaced quickly; nonrenewable ones (coal, oil, gas, ores) are not.</li>"
             "<li>Compare solutions with a benefit-to-cost ratio: benefit ÷ cost. Payback time = cost ÷ yearly savings.</li></ul>")
    ex = [("Cost $8 million, benefit $12 million. Ratio?", ["12 ÷ 8"], "1.5"),
          ("Ore is 2% copper. Rock for 10 t of copper?", ["10 ÷ 0.02"], "500 tonnes")]
    mist = ["Thinking oil and coal are renewable.", "Choosing the cheapest option without comparing benefits.", "Thinking hazards can be prevented completely."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Resources and people", B1 + [(g_where, 8), (g_res, 4)]),
        ("Natural hazards", [(g_haz, 14), (g_where, 6)]),
        ("Renewable or nonrenewable", [(g_res, 12), (g_ore, 8)]),
        ("Cost and benefit", [(g_cb, 14), (g_pay, 6)]),
        ("Choosing solutions", B5 + [(g_cb, 6), (g_pay, 5), (g_ore, 2), (g_haz, 2)]),
    ])
    make("earth-and-space-science", "natural-resources-and-hazards", 14, "HS-ESS3-1, HS-ESS3-2",
         "Construct an explanation based on evidence for how the availability of natural resources, occurrence of natural hazards, and changes in climate have influenced human activity. "
         "Evaluate competing design solutions for developing, managing, and utilizing energy and mineral resources based on cost-benefit ratios.",
         "Natural Resources and Hazards",
         "Natural Resources and Hazards Worksheets: Energy, Ore Grade and Cost-Benefit (Earth Science)",
         "Resources and Hazards",
         "Free high school Earth and space science worksheets on natural resources and hazards (NGSS HS-ESS3-1, HS-ESS3-2): where people live, renewable and nonrenewable resources, ore grade, hazard risk and cost-benefit ratios. 100 questions with answers.",
         "Resources and hazards shape human life.",
         "Compare energy and mineral solutions by their costs and benefits.",
         body(),
         [("How do natural resources influence where people live?", "People settle near fresh water, fertile soil, minerals and energy sources, and move away when droughts, floods or other hazards make a place hard to live in."),
          ("What is the difference between renewable and nonrenewable resources?", "Renewable resources, like sunlight and wind, are replaced naturally on a human time scale. Nonrenewable resources, like coal, oil and metal ores, take millions of years to form."),
          ("How do you compare two energy solutions?", "Add up their costs and benefits, including environmental and social ones, and compare the benefit-to-cost ratios. A higher ratio gives more benefit for each dollar spent.")],
         sets)


if __name__ == "__main__":
    main()
