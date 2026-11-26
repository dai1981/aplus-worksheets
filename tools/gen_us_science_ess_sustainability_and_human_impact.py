# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Sustainability and Human Impact (HS-ESS3-3, HS-ESS3-4)
  python tools/gen_us_science_ess_sustainability_and_human_impact.py
Simple simulations of resource use (a fishery with growth and harvest, population and doubling time, resource use per
person), and technologies that reduce human impacts on natural systems (scrubbers, catalytic converters, drip
irrigation, wildlife crossings) with before-and-after data.
Wrong answers come from real mistakes: "any harvest is sustainable", "growth adds the same amount every year",
"a solution with no side effects exists", "percent reduction = before − after".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90415)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


@safe
def g_fish():
    who = P.next()[0]
    s = R.choice([2000, 4000, 5000, 8000, 10000, 12000, 20000])
    r = R.choice([10, 15, 20, 25, 30])
    h = s * R.choice([5, 10, 15, 20, 25, 30, 40]) // 100
    grow = s * r // 100
    nxt = s + grow - h
    k = R.choice(["next", "next", "sust", "max"])
    if not once(("fi", s, r, h if k != "max" else 0, k)):
        return None
    head = "In %s's fishery model, a lake has %s fish. The fish population grows %d%% per year, and %s fish are caught each year." % (who, num(s), r, num(h))
    if k == "next":
        g = "%s fish" % num(nxt)
        return item(head + " How many fish are there after one year?", g, uniq(g, ["%s fish" % num(s + grow), "%s fish" % num(s - h), "%s fish" % num(s + h - grow), "%s fish" % num(nxt + 2 * h)]),
                    "%s + %s − %s = %s." % (num(s), num(grow), num(h), num(nxt)))
    if k == "sust":
        if h < grow:
            g = "Yes. The catch is less than the growth, so the population increases."
        elif h == grow:
            g = "Yes. The catch equals the growth, so the population stays steady."
        else:
            g = "No. The catch is more than the growth, so the population shrinks."
        return item(head + " Is this catch sustainable?", g,
                    uniq(g, ["Yes. The catch is less than the growth, so the population increases.", "Yes. The catch equals the growth, so the population stays steady.",
                             "No. The catch is more than the growth, so the population shrinks.", "It cannot be known from growth and catch."]), "Growth = %s fish per year." % num(grow))
    g = "%s fish per year" % num(grow)
    return item("A lake has %s fish, growing %d%% per year. What is the largest yearly catch that keeps the population from shrinking?" % (num(s), r), g,
                uniq(g, ["%s fish per year" % num(s), "%s fish per year" % num(grow * 2), "%d fish per year" % r, "%s fish per year" % num(s - grow)]), "%d%% of %s = %s." % (r, num(s), num(grow)))


@safe
def g_pop():
    r = R.choice([0.5, 1, 1.4, 2, 2.5, 3.5, 5, 7])
    k = R.choice(["dt", "pop"])
    if not once(("po", r, k)):
        return None
    dt = 70 / r
    if k == "dt":
        yr = lambda v: "about %s year%s" % (num(v, 3), "" if num(v, 3) == "1" else "s")
        g = yr(dt)
        return item("A country's population grows %s%% per year. Using the rule of 70, about how long will it take to double?" % num(r, 2), g,
                    uniq(g, [yr(r * 70), yr(round(100 / r)), yr(dt / 2), yr(dt * 2)]), "70 ÷ %s ≈ %s years." % (num(r, 2), num(dt, 3)))
    if dt != int(dt) or r < 1:
        return None
    p0 = R.choice([2, 3, 5, 8, 10, 20])
    n = R.choice([2, 3])
    if dt * n > 100:
        return None
    g = "%s million" % num(p0 * 2 ** n)
    return item("A city of %d million people grows %s%% per year, so it doubles about every %d years. About how many people will live there after %d years?" % (p0, num(r, 2), dt, dt * n), g,
                uniq(g, ["%s million" % num(p0 * 2 * n), "%s million" % num(p0 + 2 * n), "%s million" % num(p0 * 2 ** (n + 1)), "%s million" % num(p0)]),
                "%d doublings: %d × %d = %s million. Growth speeds up over time." % (n, p0, 2 ** n, num(p0 * 2 ** n)))


@safe
def g_foot():
    who = P.next()[0]
    res = R.choice([("water", "liters", " per day", [100, 150, 200, 300, 400]), ("electricity", "kWh", " per year", [2000, 3000, 4000, 5000, 6000]),
                    ("cropland", "hectares", "", [0.2, 0.25, 0.4, 0.5])])
    name, u0, per, vals = res
    unit = u0 + per
    ph = "%s %s of %s%s" % (num(use_ := R.choice(vals), 3), u0, name, per)
    use = use_
    pop = R.choice([10000, 20000, 50000, 80000, 100000])
    k = R.choice(["total", "cut"])
    if not once(("ft", name, use, pop, k)):
        return None
    tot = use * pop
    if k == "total":
        g = "%s %s" % (num(tot), unit)
        return item("In %s's town model, each of %s people uses %s. What is the total use?" % (who, num(pop), ph), g,
                    uniq(g, ["%s %s" % (num(tot * 10), unit), "%s %s" % (num(tot / 10, 3), unit), "%s %s" % (num(tot / 100, 3), unit)]),
                    "%s × %s = %s." % (num(pop), num(use, 3), num(tot)))
    cut = R.choice([10, 20, 25, 50])
    g = "%s %s" % (num(tot * (100 - cut) / 100), unit)
    return item("In a town of %s people, each person uses %s. If every person cuts use by %d%%, what is the new total?" % (num(pop), ph, cut), g,
                uniq(g, ["%s %s" % (num(tot * cut / 100), unit), "%s %s" % (num(tot), unit), "%s %s" % (num(use * (100 - cut) / 100, 3), unit), "%s %s" % (num(tot * (100 + cut) / 100), unit)]),
                "%s × %s%% = %s." % (num(tot), num(100 - cut), g))


SOL = [("sulfur dioxide from coal plants causing acid rain", "scrubbers in smokestacks"), ("car exhaust releasing carbon monoxide and smog gases", "catalytic converters"),
       ("farms wasting water through flood irrigation", "drip irrigation"), ("sewage polluting rivers", "wastewater treatment plants"),
       ("dams blocking salmon from swimming upstream", "fish ladders"), ("soil washing off steep farm fields", "terraces and contour plowing"),
       ("highways cutting animals off from their habitat", "wildlife crossings over or under roads"), ("fertilizer runoff causing dead zones", "cover crops and buffer strips of plants"),
       ("landfill chemicals leaking into groundwater", "plastic liners and leachate collection"), ("oil spills from tankers", "double-hulled tankers")]


@safe
def g_sol():
    p, s = R.choice(SOL)
    k = R.random() < 0.55
    if not once(("so", p, k)):
        return None
    if k:
        return item("Which technology is designed to reduce this impact: %s?" % p, s, R.sample([x[1] for x in SOL if x[1] != s], 3), "Engineers design solutions that reduce harm to natural systems.")
    return item("Which human impact are %s designed to reduce?" % s, p, R.sample([x[0] for x in SOL if x[0] != p], 3), "Match the solution to the problem.")


@safe
def g_red():
    who = P.next()[0]
    thing = R.choice([("a coal plant's sulfur dioxide", "tonnes per day", "scrubbers"), ("a farm's water use", "million liters per year", "drip irrigation"),
                      ("deer killed on a highway", "per year", "wildlife crossings"), ("nitrogen in a river", "mg per liter", "buffer strips"),
                      ("a city's landfill waste", "thousand tonnes per year", "a recycling program")])
    what, unit, sol = thing
    before = R.choice([20, 40, 50, 60, 80, 120, 200, 250])
    pct = R.choice([10, 20, 25, 40, 50, 60, 75, 80, 90])
    after = before * (100 - pct) / 100
    if after != int(after) or not once(("rd", what, before, pct)):
        return None
    tab = table(["", "Before", "After"], [["%s (%s)" % (what[0].upper() + what[1:], unit), num(before), num(after)]])
    k = R.choice(["pct", "pct", "cmp"])
    if k == "pct":
        g = "%d%%" % pct
        return item(tab + "%s measured %s before and after adding %s. By what percent did it go down?" % (who, what, sol), g,
                    uniq(g, ["%s%%" % num(before - after), "%s%%" % num(100 - pct), "%s%%" % num(100 * before / after, 3), "%s%%" % num(after)]),
                    "(%s − %s) ÷ %s × 100 = %d%%." % (num(before), num(after), num(before), pct))
    g = "%s %s" % (num(before - after), unit)
    return item(tab + "How much did %s go down after %s added %s?" % (what, who, sol), g,
                uniq(g, ["%s %s" % (num(after), unit), "%s %s" % (num(before), unit), "%d%%" % (100 - pct), "%s %s" % (num(before + after), unit)]), "%s − %s = %s." % (num(before), num(after), num(before - after)))


B1 = bank([
    ("What does sustainable mean?", "meeting people's needs now without using up resources needed in the future", ["using resources as fast as possible", "never using any resources", "only using fossil fuels"], "Long-term balance."),
    ("A fish population grows by 500 fish per year. Which yearly catch is sustainable?", "500 fish or fewer", ["any number", "1,000 fish", "all of the fish"], "Catch ≤ growth."),
    ("How does a growing human population affect biodiversity?", "More land and resources are used, which can destroy habitats.", ["It always increases biodiversity.", "It has no effect.", "It only affects the ocean."], "Habitat loss."),
    ("Why do scientists use computer simulations of resource use?", "to test what might happen under different choices before it happens", ["to make the resource larger", "because experiments are illegal", "to stop population growth"], "Models predict outcomes."),
    ("What happens when a resource is used faster than it is replaced?", "It runs down and may collapse.", ["It grows faster.", "It stays the same.", "It turns renewable."], "Overuse."),
    ("Which choice reduces the impact of a growing city on water supplies?", "fixing leaks and using water-saving fixtures", ["watering lawns at noon", "building more swimming pools", "letting taps run"], "Conservation."),
    ("Why is protecting biodiversity important for people?", "Healthy ecosystems provide food, clean water, medicines and pollination.", ["It is not important.", "Only zoos need it.", "It only matters for tourism."], "Ecosystem services."),
    ("What did the collapse of the Atlantic cod fishery in the 1990s show?", "Catching more fish than the population can replace can destroy a fishery.", ["Fish never run out.", "Cod became renewable.", "Fishing has no effect."], "Real case."),
])
B5 = bank([
    ("A town adds scrubbers to its coal plant. What is a trade-off of this solution?", "It costs money and energy to run, but cuts acid rain.", ["It has no costs at all.", "It makes more sulfur dioxide.", "It stops all CO₂."], "Every solution has trade-offs."),
    ("How could engineers refine a wildlife crossing that few animals use?", "Add fencing that guides animals to it and plant native cover on it.", ["Remove it.", "Paint it bright red.", "Build it farther from habitat."], "Refine with data."),
    ("Which data would best show that drip irrigation helps a farm?", "water used and crop yield measured before and after", ["the color of the pipes", "the farmer's age", "the price of tractors"], "Evaluate with evidence."),
    ("A fishery model shows the stock falling every year. Which change would most likely make it sustainable?", "Lower the yearly catch below the yearly growth.", ["Catch more fish.", "Stop counting fish.", "Add more boats."], "Use the model."),
    ("Why might a solution that works in one place not work in another?", "Climate, ecosystems, costs and people's needs differ between places.", ["Science only works in one place.", "All places are identical.", "Solutions never work."], "Context matters."),
])


def body():
    think = ("<p><b>Use resources no faster than nature can replace them.</b></p>"
             "<ul><li>Fishery model: next year = stock + growth − catch. A catch is sustainable if it is no more than the growth.</li>"
             "<li>Growing populations use more resources: total = use per person × people. Rule of 70: doubling time ≈ 70 ÷ growth rate (%).</li>"
             "<li>Technologies (scrubbers, catalytic converters, drip irrigation, wildlife crossings) reduce impacts. Judge them with data: percent reduction = (before − after) ÷ before × 100.</li></ul>")
    ex = [("10,000 fish, grow 20%, catch 1,500. Next year?", ["10,000 + 2,000 − 1,500"], "10,500 fish"),
          ("Pollution 80 → 20 tonnes. Percent reduction?", ["(80 − 20) ÷ 80 × 100"], "75%")]
    mist = ["Thinking any catch is sustainable as long as fish remain.", "Thinking population grows by the same amount every year.", "Using before − after as the percent reduction."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("People and resources", B1 + [(g_foot, 6), (g_sol, 6)]),
        ("Simulating a fishery", [(g_fish, 14), (g_foot, 6)]),
        ("Population and resource use", [(g_pop, 12), (g_foot, 8)]),
        ("Reducing human impacts", [(g_sol, 12), (g_red, 8)]),
        ("Evaluating solutions", B5 + [(g_red, 8), (g_fish, 4), (g_pop, 3)]),
    ])
    make("earth-and-space-science", "sustainability-and-human-impact", 15, "HS-ESS3-3, HS-ESS3-4",
         "Create a computational simulation to illustrate the relationships among management of natural resources, the sustainability of human populations, and biodiversity. "
         "Evaluate or refine a technological solution that reduces impacts of human activities on natural systems.",
         "Sustainability and Human Impact",
         "Sustainability Worksheets: Fishery Models, Population and Human Impact (Earth Science)",
         "Sustainability",
         "Free high school Earth and space science worksheets on sustainability and human impact (NGSS HS-ESS3-3, HS-ESS3-4): fishery models, population growth, resource use and technologies that reduce pollution. 100 questions with answers.",
         "Take no more than nature replaces.",
         "Model resource use, then test solutions with before-and-after data.",
         body(),
         [("What makes a fishery sustainable?", "The yearly catch is no more than the number of fish the population adds each year, so the stock does not shrink over time."),
          ("How does population growth affect resources?", "Total use is the use per person times the number of people, so a growing population uses more water, land and energy unless each person uses less."),
          ("How do engineers judge a solution to pollution?", "They measure the problem before and after the solution, calculate the percent reduction, and weigh the benefits against costs and side effects.")],
         sets)


if __name__ == "__main__":
    main()
