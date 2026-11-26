# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Protecting Earth's Resources (5-ESS3-1)
  python tools/gen_us_science_g5_protecting_earths_resources.py
Human activities affect land, water, air and living things. Communities use science ideas to
protect them: reduce, reuse and recycle; clean wastewater; plant trees and cover crops to stop
erosion; protect habitats; use renewable energy and public transportation.
Questions match problems to solutions and use data about water, energy and waste.
Wrong answers come from real mistakes: "recycling and reusing are the same", "renewable means
it never runs out even if wasted", "one person's choices never matter".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People, GREEN

U = Unit(50116)
R = U.R
P = People(R)

PROBLEMS = [
    ("Soil washes off a farm field into a river after heavy rain.", "Plant cover crops and rows of trees to hold the soil.", "land and water"),
    ("A city's air is smoggy from car exhaust.", "Add bus lines and bike lanes so fewer people drive.", "air"),
    ("A landfill is filling up quickly.", "Start a recycling and composting program.", "land"),
    ("Wastewater from homes flows into a lake.", "Build a treatment plant that cleans wastewater before it is released.", "water"),
    ("A forest is cut down and animals lose their homes.", "Replant trees and protect part of the forest as a park.", "living things"),
    ("Plastic bags are blowing into the ocean and hurting sea turtles.", "Use reusable cloth bags and ban single-use plastic bags.", "water and living things"),
    ("A town burns coal to make electricity, polluting the air.", "Build wind turbines and solar panels.", "air"),
    ("Fertilizer runoff makes algae grow over a pond.", "Leave strips of plants along the water and use less fertilizer.", "water"),
    ("A town's wells are running low in summer.", "Fix leaks and water lawns less often.", "water"),
    ("Deer are hit by cars where a highway cuts through their habitat.", "Build a wildlife bridge over the highway.", "living things"),
    ("Factories release smoke with harmful gases.", "Put filters (scrubbers) on smokestacks.", "air"),
    ("A beach is covered with litter after summer weekends.", "Add trash and recycling bins and hold clean-up days.", "land and water"),
]
REDUCE = ["turning off the water while brushing your teeth", "printing on both sides of the paper", "turning off lights in empty rooms", "buying fewer items with plastic packaging", "walking to school instead of being driven"]
REUSE = ["using a refillable water bottle", "turning an old jar into a pencil holder", "donating outgrown clothes", "using the back of old paper for drawing", "packing lunch in a reusable box"]
RECYCLE = ["putting aluminum cans in the recycling bin", "taking glass bottles to be made into new glass", "sending old newspapers to make new paper", "recycling plastic bottles into fleece jackets"]


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ makers
def g_solution():
    pr, sol, _ = R.choice(PROBLEMS)
    w = [s for p, s, _ in PROBLEMS if s != sol]
    return item(pr + " Which solution best addresses this problem?", sol, R.sample(w, 3), "This solution deals with the cause of the problem. " + sol)


def g_resource():
    pr, sol, res = R.choice(PROBLEMS)
    if "trees" in sol.lower() or "plants" in sol.lower():
        return None              # plants protect several resources at once: no single answer
    opts = ["land", "water", "air", "living things", "land and water", "water and living things"]
    w = [o for o in opts if o != res and not (set(o.split(" and ")) & set(res.split(" and ")) and len(o.split(" and ")) + len(res.split(" and ")) > 2)]
    if len(w) < 3:
        return None
    return item("A community does this: %s Which resource does it mainly protect?" % sol, res, R.sample(w, 3), "This mainly protects %s." % res)


def g_rrr():
    k = R.choice(["reduce", "reuse", "recycle"])
    ex = R.choice({"reduce": REDUCE, "reuse": REUSE, "recycle": RECYCLE}[k])
    return item("Which of the three R's is %s?" % ex, k, [z for z in ["reduce", "reuse", "recycle"] if z != k] + ["replace"],
                {"reduce": "Reducing means using less in the first place.", "reuse": "Reusing means using something again for the same or a new job.",
                 "recycle": "Recycling means breaking a material down to make new products."}[k])


def g_shower():
    a = R.choice([10, 12, 15, 20])
    b = R.choice([4, 5, 6, 8])
    r = R.choice([8, 9, 10])
    d = R.choice([7, 30])
    save = (a - b) * r * d
    p = P.next()
    return item("A shower uses about %d liters of water per minute. %s cuts %s shower from %d minutes to %d minutes. How much water does that save in %d days?" % (r, p[0], p[2], a, b, d),
                "{:,} liters".format(save), ["{:,} liters".format((a - b) * r), "{:,} liters".format(a * r * d), "{:,} liters".format((a - b) * d)],
                "(%d − %d) × %d × %d = %s liters." % (a, b, r, d, "{:,}".format(save)))


def g_bulb():
    old, new = R.choice([(60, 9), (60, 10), (100, 15), (75, 11), (40, 6)])
    n = R.choice([4, 5, 6, 8, 10])
    return item("An old bulb uses %d watts and an LED bulb that gives the same light uses %d watts. A school replaces %d old bulbs with LEDs. How many fewer watts are used when they are all on?" % (old, new, n),
                str((old - new) * n), [str(old - new), str(old * n), str((old + new) * n)], "(%d − %d) × %d = %d watts. Using less electricity means less fuel burned at power plants." % (old, new, n, (old - new) * n))


def g_waste():
    wk = [R.randint(40, 70)]
    for _ in range(3):
        wk.append(wk[-1] - R.randint(4, 12))
    ch = bar_chart(["Week 1", "Week 2", "Week 3", "Week 4"], wk, "kg", "bar graph of trash thrown away each week", ymax=(wk[0] // 20 + 1) * 20, step=20, col=GREEN, w=300)
    p = P.next()
    return item(fig(ch) + "%s's class started recycling and composting in week 1. How much less trash did they throw away in week 4 than in week 1?" % p[0],
                "%d kg" % (wk[0] - wk[3]), ["%d kg" % wk[3], "%d kg" % wk[0], "%d kg" % (wk[0] - wk[1])], "%d − %d = %d kg." % (wk[0], wk[3], wk[0] - wk[3]))


def g_renew():
    ren = ["wind", "sunlight", "flowing water", "heat from inside Earth (geothermal)"]
    non = ["coal", "oil", "natural gas", "gasoline"]
    if R.random() < 0.5:
        a = R.choice(ren)
        return item("Which energy source is renewable?", a, R.sample(non, 3), cap(a) + " is renewed by nature and does not run out. Coal, oil and gas take millions of years to form.")
    a = R.choice(non)
    return item("Which energy source is <b>not</b> renewable?", a, R.sample(ren, 3), cap(a) + " formed over millions of years and will run out; burning it also pollutes the air.")


B1 = bank([
    ("What is a natural resource?", "something from nature that people use, like water, soil, air or trees", ["something made only in factories", "a kind of plastic", "anything in a store"],
     "Natural resources come from Earth's systems."),
    ("Which is the best example of reducing?", "turning off the water while you brush your teeth", ["putting a can in a recycling bin", "using a jar as a vase", "making paper from old paper"],
     "Reducing means using less."),
    ("How is reusing different from recycling?", "Reusing uses an item again as it is; recycling breaks it down to make new products.", ["They mean exactly the same thing.", "Recycling uses less energy than reusing always.", "Reusing means throwing it away."],
     "A refilled bottle is reused; a melted-down bottle is recycled."),
    ("How do trees help protect soil?", "Their roots hold the soil in place.", ["They make the soil wetter so it washes away.", "They push soil into rivers.", "They eat the soil."],
     "Roots and fallen leaves keep rain and wind from carrying soil away."),
    ("Why does a city treat wastewater before releasing it into a river?", "to remove pollution that would harm living things and drinking water", ["to make the river saltier", "to make the water warmer", "so the river flows faster"],
     "Wastewater treatment uses science to clean the water."),
    ("Which change reduces air pollution in a city?", "more people riding buses, trains or bikes", ["more cars on the road", "burning more trash", "cutting down street trees"],
     "Fewer cars burning gasoline means cleaner air."),
    ("What is a renewable energy source?", "a source that nature replaces, like sunlight or wind", ["coal", "gasoline", "natural gas"],
     "Renewable sources do not run out the way fossil fuels do."),
    ("Why are national parks and wildlife refuges important?", "They protect habitats so plants and animals can survive.", ["They make room for more roads.", "They are used to store trash.", "They stop rain from falling."],
     "Protected land keeps ecosystems healthy."),
    ("Why should people avoid pouring paint or oil down a storm drain?", "Storm drains often flow straight into rivers and lakes.", ["Storm drains go to a treatment plant every time.", "Paint helps fish grow.", "It cleans the drain."],
     "Pollution in storm drains can reach water that animals and people use."),
    ("Which action protects the ocean most directly?", "keeping plastic trash out of rivers and beaches", ["planting a garden far from water", "turning off a light", "reading a book"],
     "Much ocean plastic comes from rivers and beaches."),
])
B5 = bank([
    ("A town wants to know if its new recycling program works. What should it measure?", "the amount of trash sent to the landfill before and after", ["the color of the bins", "the number of trucks painted", "how many people like the program"],
     "Data before and after the change show whether less waste goes to the landfill."),
    ("Students test whether plant roots stop erosion. They pour water on a tray of bare soil and a tray of soil with grass. Which result supports the idea?", "Less soil washes off the tray with grass.", ["More soil washes off the grass tray.", "Both trays lose the same amount.", "The water disappears."],
     "Roots hold soil, so less is carried away."),
    ("Which is the best evidence that a city's clean-air plan worked?", "Air quality measurements improved over several years.", ["The city made a new logo.", "One day was sunny.", "People said they liked the air."],
     "Measured data over time are strong evidence."),
    ("Why do some cities build wetlands next to farms?", "Wetland plants trap soil and fertilizer before they reach rivers.", ["Wetlands make more fertilizer.", "Wetlands dry out rivers.", "Wetlands attract more cars."],
     "Wetlands act like natural filters."),
    ("A school installs solar panels. Which problem does this help with?", "It reduces the electricity made by burning fossil fuels.", ["It increases trash.", "It uses more water.", "It cuts down trees."],
     "Solar panels make electricity without burning fuel."),
    ("Which statement about individual actions is most accurate?", "Small actions by many people can add up to a big difference.", ["One person's actions never matter.", "Only governments can help.", "Protecting resources is not needed."],
     "If thousands of families save water, the total saved is huge."),
    ("A community bans cutting trees near a river. What is the most likely result?", "Less erosion and cleaner, cooler water for fish.", ["More soil in the river.", "Fewer fish because there is shade.", "The river dries up."],
     "Tree roots hold the banks and shade keeps the water cool."),
])


def body():
    rows = [["Land", "recycling, composting, planting trees, cover crops"], ["Water", "treating wastewater, saving water, plant strips along rivers"],
            ["Air", "public transportation, clean energy, filters on smokestacks"], ["Living things", "parks, wildlife crossings, replanting habitats"]]
    think = ("<p>People use natural resources: land, water, air and living things. Our activities can harm them, but communities use "
             "<b>science ideas</b> to protect them.</p>" + table(["Resource", "Ways communities protect it"], rows)
             + "<p>At home and school we can help with the three R's: <b>reduce</b> (use less), <b>reuse</b> (use again) and <b>recycle</b> (make into something new).</p>")
    ex = [("Soil washes off a farm into a river. What could help?", ["Roots hold soil.", "Plant cover crops or rows of trees."], "Plant cover crops and trees."),
          ("A 60-watt bulb is replaced by a 9-watt LED. How many watts are saved?", ["60 − 9"], "51 watts")]
    mist = ["Thinking reusing and recycling are the same.",
            "Thinking renewable means it is fine to waste.",
            "Thinking one person's choices never matter. Many small actions add up.",
            "Choosing a solution that does not address the cause of the problem."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Natural resources", B1 + [(g_rrr, 6), (g_renew, 4)]),
        ("Problems and solutions", [(g_solution, 11), (g_resource, 5), (g_renew, 4)]),
        ("Reduce, reuse, recycle and energy", [(g_rrr, 8), (g_renew, 6), (g_bulb, 6)]),
        ("Using data", [(g_shower, 7), (g_bulb, 6), (g_waste, 7)]),
        ("Communities in action", B5 + [g_solution, g_waste, g_shower, g_resource]),
    ])
    make("grade-5", "protecting-earths-resources", 16, "5-ESS3-1",
         "Obtain and combine information about ways individual communities use science ideas to protect the Earth's resources and environment.",
         "Protecting Earth's Resources",
         "Grade 5 Protecting Earth's Resources Worksheets: Reduce, Reuse, Recycle and Clean Energy",
         "Protecting Resources",
         "Free Grade 5 science worksheets on protecting Earth's resources (NGSS 5-ESS3-1): how communities protect land, water, air and living things, the three R's, renewable energy and data on water and energy saving. 100 practice questions with answers.",
         "Communities use science to protect land, water, air and living things.",
         "Reduce, reuse and recycle; clean wastewater; plant trees to stop erosion; protect habitats; and use clean energy.",
         body(),
         [("How do communities protect Earth's resources?", "They recycle and compost, treat wastewater, plant trees to stop erosion, protect habitats in parks, and use public transportation and clean energy."),
          ("What is the difference between reduce, reuse and recycle?", "Reduce means use less. Reuse means use something again. Recycle means break a material down to make new products."),
          ("What are renewable energy sources?", "Sources that nature replaces, such as sunlight, wind, flowing water and geothermal heat."),
          ("Can kids help protect the environment?", "Yes. Saving water and electricity, reusing items and recycling all add up when many people do them.")],
         sets)


if __name__ == "__main__":
    main()
