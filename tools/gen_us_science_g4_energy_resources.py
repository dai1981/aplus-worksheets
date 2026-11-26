# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Energy Resources (4-ESS3-1)
  python tools/gen_us_science_g4_energy_resources.py
Energy and fuels that humans use come from natural sources. Renewable: sun, wind, moving water,
geothermal, biomass. Nonrenewable: coal, oil, natural gas (fossil fuels), uranium. Their use affects
the environment (air pollution, mining, dams change rivers, land for solar/wind farms).
Wrong answers come from real mistakes: "fossil fuels are renewable because there is a lot of them",
"wind energy causes air pollution", "renewable energy has no effects at all".
"""
from sci_common import Unit, item, bank, lesson, make, fig, pie, classifier, People, GREEN, BLUE, RED, GRAY, ORANGE, SUN, BROWN

U = Unit(40115)
R = U.R
P = People(R)

KIND = {"renewable": ["sunlight", "wind", "moving water", "heat from inside Earth (geothermal)", "wood from fast-growing trees", "ocean tides", "ocean waves", "corn grown to make fuel", "a rushing river"],
        "nonrenewable": ["coal", "oil", "natural gas", "uranium", "gasoline made from oil", "propane", "diesel fuel", "jet fuel made from oil", "heating oil"]}
WHY = {"renewable": "It can be replaced naturally in a short time.", "nonrenewable": "It took millions of years to form, so it cannot be replaced quickly."}
k_which, _ = classifier(R, KIND, "Which energy resource is {k}?", "{x}", WHY)


def k_what():
    k = R.choice(sorted(KIND))
    x = R.choice(KIND[k])
    return item(("Are %s renewable or nonrenewable resources?" if x.endswith(("tides", "waves")) else "Is %s a renewable or a nonrenewable resource?") % x, k, ["nonrenewable" if k == "renewable" else "renewable", "neither; it is not an energy resource", "both at once"],
                cap(x) + " is " + k + ". " + WHY[k])


def cap(s):
    return s[0].upper() + s[1:]


SRC = {"sunlight": ("solar panels", "Panels need a lot of land or roof space, and they only work when the sun shines.", "They make no air pollution while working."),
       "wind": ("wind turbines", "Turbines can harm birds and bats, and they need steady wind.", "They make no air pollution while working."),
       "moving water": ("a dam with a power plant", "A dam floods land and blocks fish from swimming up the river.", "It makes no air pollution while working."),
       "coal": ("a coal power plant", "Burning coal pollutes the air, and mining it damages land.", "It can make electricity day and night."),
       "oil": ("gasoline in cars", "Burning gasoline pollutes the air, and oil spills harm ocean life.", "It stores a lot of energy in a small amount."),
       "natural gas": ("a gas stove or gas power plant", "Burning gas pollutes the air, and drilling can harm land and water.", "It can make electricity day and night."),
       "heat inside Earth": ("a geothermal power plant", "It only works in places with hot rock near the surface.", "It makes very little air pollution.")}


def g_effect():
    src = R.choice(sorted(SRC))
    how, bad, good = SRC[src]
    k = R.choice(["bad", "good", "how"])
    if k == "bad":
        w = [SRC[x][1] for x in SRC if x != src and not (src in ("coal", "oil", "natural gas") and x in ("coal", "oil", "natural gas"))]
        return item("People use %s to get energy from %s. Which is a problem with this energy source?" % (how, src), bad, R.sample(w, 3), bad)
    if k == "good":
        w = ["It makes new energy from nothing.", "It never affects the environment in any way.", "It works the same in every place on Earth."] if src not in ("coal", "oil", "natural gas") else \
            ["It makes no air pollution.", "It will never run out.", "It is replaced naturally in a few days."]
        return item("People use %s to get energy from %s. Which is a benefit of this energy source?" % (how, src), good, w, good)
    w = [SRC[x][0] for x in SRC if x != src and not ({x, src} <= {"coal", "natural gas"})]
    return item("Which is used to turn %s into electricity or motion?" % (src if src != "oil" else "oil (as gasoline)"), how, R.sample(w, 3), "Energy from %s is used with %s." % (src, how))


def g_pie():
    vals = R.sample([5, 10, 15, 20, 25, 30, 35, 40], 3)
    last = 100 - sum(vals)
    if last <= 0 or last in vals:
        return None
    vals.append(last)
    R.shuffle(vals)
    a, b, c, d = vals
    parts = [("natural gas", d, ORANGE), ("coal", c, BROWN), ("wind and solar", a, GREEN), ("water (dams)", b, BLUE)]
    town = R.choice(["Riverton", "Hill City", "Lakeview", "Maple Town", "Sandy Bay", "Oak Ridge"])
    ch = pie([("%s (%d%%)" % (n, v), v, col) for n, v, col in parts], "circle graph of %s's electricity sources" % town)
    k = R.choice(["most", "renew", "non"])
    if k == "most":
        best = max(parts, key=lambda t: t[1])[0]
        return item(fig(ch) + "This graph shows where %s gets its electricity. Which source does %s use the most?" % (town, town), best, [p[0] for p in parts if p[0] != best],
                    "%s is the largest part of the circle." % cap(best))
    if k == "renew":
        return item(fig(ch) + "What percent of %s's electricity comes from renewable sources?" % town, "%d%%" % (a + b), [x for x in dict.fromkeys(["%d%%" % a, "%d%%" % (c + d), "%d%%" % b, "%d%%" % (a + c), "100%"]) if x != "%d%%" % (a + b)][:3],
                    "Wind and solar (%d%%) + water (%d%%) = %d%%." % (a, b, a + b))
    return item(fig(ch) + "What percent of %s's electricity comes from fossil fuels?" % town, "%d%%" % (c + d), [x for x in dict.fromkeys(["%d%%" % (a + b), "%d%%" % d, "%d%%" % c, "%d%%" % (b + d), "100%"]) if x != "%d%%" % (c + d)][:3],
                "Coal (%d%%) + natural gas (%d%%) = %d%%." % (c, d, c + d))


B1 = bank([
    ("What is a natural resource?", "something from nature that people use", ["something made only in factories", "a kind of machine", "a type of weather"],
     "Sunlight, wind, water, coal and oil are natural resources."),
    ("What does renewable mean?", "It can be replaced naturally in a short time.", ["It will run out soon.", "It is made in a factory.", "It is always dangerous."],
     "The sun shines and the wind blows again and again."),
    ("What are fossil fuels?", "coal, oil and natural gas formed from ancient living things", ["sunlight and wind", "rocks from volcanoes", "fresh wood from trees"],
     "They formed over millions of years."),
    ("Why are fossil fuels called nonrenewable?", "They take millions of years to form, so we use them faster than they are made.", ["They are made every day.", "They never run out.", "They come from the sun directly."],
     "Once used, they are gone for a very long time."),
    ("Which energy source causes the most air pollution?", "burning coal", ["wind", "sunlight", "moving water"], "Burning fuels releases smoke and gases."),
    ("Most energy resources can be traced back to", "the sun", ["the moon", "the ocean floor only", "the wind only"],
     "Plants used sunlight long ago (fossil fuels); the sun also drives wind and the water cycle."),
    ("Which is a way to save energy at home?", "turning off lights when you leave a room", ["leaving the TV on all night", "opening the fridge often", "running the dryer with one sock"],
     "Using less energy means using fewer resources."),
    ("Does using renewable energy have any effect on the environment?", "Yes, but usually less than fossil fuels, like land used for solar farms.", ["No, never.", "Yes, it pollutes the air more than coal.", "It makes the sun weaker."],
     "Every energy source has some effects."),
])
B5 = bank([
    ("A town is very windy and has open land. Which energy source would be a good choice?", "wind turbines", ["a coal power plant", "a dam (there is no river)", "a geothermal plant (there is no hot rock)"],
     "Use the resource the place has."),
    ("Ava's school wants to use less fossil fuel. Which plan helps most?", "put solar panels on the roof", ["leave all lights on", "buy more gas heaters", "use more paper"],
     "Solar panels use renewable sunlight."),
    ("Leo says solar panels cannot work at night. How can a solar home still have power at night?", "Store extra daytime energy in batteries.", ["Use moonlight only.", "Point the panels at a lamp.", "Solar homes never need power at night."],
     "Batteries store energy for later."),
    ("Why might people be against building a big dam on a river?", "It floods land and blocks fish from swimming upstream.", ["It pollutes the air with smoke.", "It uses up coal.", "It makes the river run uphill."],
     "Dams change the river ecosystem."),
    ("A city gets 80% of its electricity from coal. What could it do to reduce air pollution?", "replace some coal with wind and solar energy", ["build more coal plants", "use more gasoline", "burn more natural gas and coal"],
     "Renewable sources do not burn fuel."),
    ("Mia compares two energy sources. Which question is about an environmental effect?", "Does it pollute the air or harm wildlife?", ["What color is the power plant?", "How tall is the worker?", "What day was it built?"],
     "Environmental effects are about air, water, land and living things."),
])


def body():
    think = ("<p>The energy we use comes from <b>natural resources</b>.</p>"
             "<ul><li><b>Renewable</b> resources are replaced naturally in a short time: sunlight, wind, moving water and heat from inside Earth.</li>"
             "<li><b>Nonrenewable</b> resources take millions of years to form: coal, oil and natural gas (<b>fossil fuels</b>) and uranium.</li></ul>"
             "<p>Using any resource affects the environment. Burning fossil fuels pollutes the air and mining damages land. "
             "Renewable sources make little pollution, but dams change rivers and wind and solar farms need a lot of land.</p>")
    ex = [("Is natural gas renewable or nonrenewable?", ["It is a fossil fuel.", "It took millions of years to form."], "nonrenewable"),
          ("Name one effect of using wind turbines.", ["They make no air pollution.", "They can harm birds and need lots of land."], "They can harm birds.")]
    mist = ["Thinking fossil fuels are renewable because there is a lot of them now.",
            "Thinking wind or solar energy pollutes the air while working.",
            "Thinking renewable energy has no effects at all."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Natural energy resources", B1 + [(k_which, 6), (k_what, 6)]),
        ("Renewable or nonrenewable?", [(k_what, 10), (k_which, 6), (g_effect, 4)]),
        ("Effects on the environment", [(g_effect, 16), (k_what, 4)]),
        ("Energy data", [(g_pie, 12), (g_effect, 8)]),
        ("Choosing energy sources", B5 + [g_effect, g_pie, k_which]),
    ])
    make("grade-4", "energy-resources", 15, "4-ESS3-1",
         "Obtain and combine information to describe that energy and fuels are derived from natural resources and their uses affect the environment.",
         "Energy Resources",
         "Grade 4 Energy Resources Worksheets: Renewable and Nonrenewable Energy and the Environment",
         "Energy Resources",
         "Free Grade 4 science worksheets on energy resources (NGSS 4-ESS3-1): renewable and nonrenewable resources, fossil fuels, solar, wind and water power, environmental effects and energy data. 100 practice questions with answers.",
         "Our energy comes from natural resources.",
         "Renewable resources like sun and wind are replaced quickly. Fossil fuels like coal and oil take millions of years to form.",
         body(),
         [("What is the difference between renewable and nonrenewable resources?", "Renewable resources, like sunlight and wind, are replaced naturally in a short time. Nonrenewable resources, like coal and oil, take millions of years to form."),
          ("How do fossil fuels affect the environment?", "Burning them pollutes the air, and getting them by mining or drilling can damage land and water."),
          ("Do renewable energy sources affect the environment?", "Yes, but usually less. Dams change rivers, and wind and solar farms use a lot of land.")],
         sets)


if __name__ == "__main__":
    main()
