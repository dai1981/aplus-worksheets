# -*- coding: utf-8 -*-
"""
UK Year 4 science: Changing Environments (Living things and their habitats)
  python tools/gen_uk_science_y4_changing_environments.py
Environments change naturally (seasons, floods, storms, droughts) and because of people (building, pollution,
litter, cutting down trees), sometimes for the better (nature reserves, ponds, hedgerows). Effects on living things,
seasonal changes such as hibernation and migration, and wildlife survey data.
Wrong answers come from real mistakes: "all changes are caused by people", "all changes harm wildlife",
"animals can always just move somewhere else", "one year's count shows a trend".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61403)
R = U.R
P = People(R)

CH = [("A river floods after heavy rain.", "natural"), ("A storm blows down old trees.", "natural"), ("A long, dry summer dries up a pond.", "natural"),
      ("Leaves fall from trees in autumn.", "natural"), ("Lightning starts a heath fire.", "natural"), ("A new housing estate is built on a field.", "people"),
      ("Litter is dropped in a park.", "people"), ("A hedgerow is pulled up to make a bigger field.", "people"), ("A factory pours waste into a river.", "people"),
      ("A school digs a wildlife pond.", "people"), ("Volunteers plant trees on bare land.", "people"), ("Farmers spray pesticides on crops.", "people")]


def g_cause():
    s, c = R.choice(CH)
    if not once(("ca", s)):
        return None
    a = "a natural change" if c == "natural" else "a change caused by people"
    return item("%s Is this a natural change or a change caused by people?" % s, a, ["a change caused by people" if c == "natural" else "a natural change", "not a change at all", "a change caused by the Moon"],
                "Some changes happen naturally; others are caused by human activity.")


EFF = [("A pond is filled in to build a car park.", "Frogs and newts lose their habitat."), ("A wildflower meadow is planted.", "More bees and butterflies can find nectar."),
       ("Plastic litter is left on a beach.", "Seabirds and turtles can swallow it or get tangled."), ("Bird boxes are put up in a wood.", "More birds have safe places to nest."),
       ("A hedgerow is planted along a field.", "Birds and small mammals get shelter and food."), ("Oil leaks into the sea.", "Seabirds' feathers get coated and they cannot fly or keep warm."),
       ("Trees in a rainforest are cut down.", "Animals such as orangutans lose their homes and food."), ("Fertiliser runs off fields into a lake.", "Algae grow fast and fish can die from lack of oxygen."),
       ("A road is built through a wood.", "Animals such as badgers and hedgehogs can be killed crossing it."), ("A nature reserve is created on old farmland.", "Rare plants and animals are protected.")]


def is_good(s):
    return any(w in s for w in ("meadow", "Bird boxes", "hedgerow is planted", "nature reserve"))


def g_eff():
    s, e = R.choice(EFF)
    k = R.random() < 0.6
    if not once(("ef", s, k)):
        return None
    pool = [x for x in EFF if x[0] != s and (not is_good(s) or not is_good(x[0]))]
    if k:
        return item("%s What is the most likely effect on living things?" % s, e, [x[1] for x in R.sample(pool, 3)], "Changes to a habitat change what can live there.")
    return item("Which change could cause this: %s" % e, s, [x[0] for x in R.sample(pool, 3)], "Match the cause to the effect.")


def g_good():
    s, e = R.choice(EFF)
    if not once(("gd", s)):
        return None
    good = is_good(s)
    a = "good for wildlife" if good else "harmful to wildlife"
    return item("%s Is this change good for wildlife or harmful to wildlife?" % s, a, ["harmful to wildlife" if good else "good for wildlife", "it has no effect at all", "it only affects the weather"],
                "People can harm habitats, but they can also protect and improve them.")


SEAS = [("hedgehogs", "hibernate through the winter"), ("swallows", "fly south to Africa for the winter"), ("oak trees", "lose their leaves in autumn"),
        ("frogs", "lay frogspawn in ponds in spring"), ("squirrels", "store nuts in autumn"), ("bluebells", "flower in spring in woodlands"),
        ("dormice", "hibernate through the winter"), ("geese", "arrive in Britain from colder places for the winter")]


def g_seas():
    a, d = R.choice(SEAS)
    if not once(("se", a)):
        return None
    return item("How do %s cope with or change through the seasons?" % a, "They " + d + ".", ["They " + x[1] + "." for x in R.sample([x for x in SEAS if x[1] != d], 3)],
                "Living things have ways of surviving the changing seasons.")


def g_survey():
    who = P.next()[0]
    animal = R.choice(["hedgehogs", "house sparrows", "bumblebees", "frogs", "butterflies"])
    years = [2018, 2020, 2022, 2024]
    start = R.choice([40, 48, 52, 60])
    trend = R.choice(["down", "up"])
    st = R.choice([5, 6, 8])
    vals = [start + (st * i if trend == "up" else -st * i) + R.choice([-1, 0, 1]) for i in range(4)]
    k = R.choice(["read", "read", "trend", "diff", "why"])
    ri = R.randrange(4)
    if not once(("sv", animal, tuple(vals), k, ri if k == "read" else 0)) or (k in ("trend", "why") and not once(("sk", k, trend), 2)):
        return None
    tab = table(["Year", "Number of %s counted" % animal], [[str(y), str(v)] for y, v in zip(years, vals)])
    intro = tab + "%s's school counts %s in its grounds every two years. " % (who, animal)
    if k == "read":
        g = str(vals[ri])
        return item(intro + "How many %s were counted in %d?" % (animal, years[ri]), g, uniq(g, [str(v) for v in vals] + [str(vals[ri] + 3)]), "Read the row.")
    if k == "trend":
        a = "The number went down." if trend == "down" else "The number went up."
        return item(intro + "What is the trend in the counts?", a, ["The number went up." if trend == "down" else "The number went down.", "The number stayed the same.", "There is no data."], "Compare the first and last counts.")
    if k == "diff":
        d = abs(vals[3] - vals[0])
        g = str(d)
        return item(intro + "By how many did the count change from 2018 to 2024?", g, uniq(g, [str(vals[3]), str(vals[0]), str(vals[3] + vals[0]), str(d + 4)]), "Subtract the smaller count from the larger.")
    if trend == "down":
        return item(intro + "Which change near the school could explain the fall?", "a new car park built over a wild area", ["a new wildlife pond", "planting a hedgerow", "putting up bug hotels"], "Losing habitat reduces numbers.")
    return item(intro + "Which change near the school could explain the rise?", "planting wildflowers and leaving a wild area", ["covering the field in tarmac", "removing the hedges", "using more pesticides"], "Better habitat increases numbers.")


B1 = bank([
    ("What is an environment?", "the surroundings and conditions where a living thing lives", ["a type of animal", "a kind of food", "the weather on one day"], "Includes air, water, soil and other living things."),
    ("Can environments change naturally?", "Yes, for example through seasons, floods and storms.", ["No, only people change them.", "No, they never change.", "Only at night."], "Natural changes happen all the time."),
    ("Why can changes to environments be dangerous to living things?", "Living things may lose food, water or shelter.", ["They always get more food.", "Living things never need shelter.", "Changes make animals bigger."], "Habitats meet needs."),
    ("What is hibernation?", "a deep sleep through winter to save energy", ["flying south", "growing new fur", "eating more in summer"], "Hedgehogs hibernate."),
    ("What is migration?", "travelling to a different place for part of the year", ["sleeping all winter", "changing colour", "laying eggs"], "Swallows migrate to Africa."),
    ("How can people help wildlife in a school garden?", "plant wildflowers, put up bird boxes and dig a pond", ["cover it in concrete", "use lots of pesticide", "remove all trees"], "Create habitats."),
    ("Why should we not drop litter?", "It can harm or trap animals and spoil habitats.", ["It feeds animals well.", "It helps plants grow.", "It makes no difference."], "Litter is dangerous."),
    ("What is a nature reserve?", "a protected area where wildlife is looked after", ["a zoo", "a shop for pets", "a farm for crops"], "Protects habitats."),
])
B5 = bank([
    ("Why do scientists count wildlife over many years, not just once?", "to see if numbers are really changing over time", ["one count is always enough", "to make the numbers bigger", "because animals hide every other year"], "Trends need data over time."),
    ("Bee numbers are falling. Which action could help?", "planting more flowers and using fewer pesticides", ["cutting down hedges", "covering gardens in gravel", "spraying more chemicals"], "Food and safety for bees."),
    ("Why might a new road include a tunnel for badgers?", "so badgers can cross safely and keep using their habitat", ["to keep cars dry", "to store rubbish", "because badgers like tunnels for fun"], "Reducing harm."),
    ("A pond dries up every summer. Which animals are most affected?", "frogs and newts that need water to breed", ["squirrels in trees", "birds in the sky", "worms deep in soil"], "Water habitats."),
    ("How could you find out if litter affects birds in a park?", "count birds in a littered area and a clean area of the same size over several days", ["ask one person", "count birds once in any place", "look at photos of other parks"], "Fair comparison."),
])


def body():
    think = ("<p><b>Environments change, and this can help or harm living things.</b></p>"
             "<ul><li>Natural changes: seasons, floods, storms, droughts. Changes caused by people: building, pollution, litter, cutting down trees.</li>"
             "<li>People can also improve habitats: nature reserves, ponds, hedgerows, bird boxes, wildflowers.</li>"
             "<li>Living things cope with seasons by hibernating, migrating or losing leaves. Surveys over many years show trends.</li></ul>")
    ex = [("A pond is filled in. Effect?", ["Pond animals lose their habitat"], "frogs and newts must move or die"),
          ("Counts 50, 44, 38, 32. Trend?", ["Each count is lower"], "going down")]
    mist = ["Thinking all changes are caused by people.", "Thinking all changes harm wildlife.", "Using one year's count to show a trend."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Changing environments", B1 + [(g_cause, 12)]),
        ("Effects on living things", [(g_eff, 14), (g_good, 6)]),
        ("Seasons", [(g_seas, 8), (g_good, 4), (g_survey, 8)]),
        ("Wildlife surveys", [(g_survey, 20)]),
        ("Protecting habitats", B5 + [(g_survey, 10), (g_eff, 5)]),
    ])
    make_uk(4, "changing-environments", 3, "Living things and their habitats",
            "Recognise that environments can change and that this can sometimes pose dangers to living things.",
            "Changing Environments",
            "Year 4 Science: Changing Environments Worksheets (Habitats, Pollution, Wildlife Surveys)",
            "Changing Environments",
            "Free Year 4 science worksheets on changing environments: natural and human changes, effects on habitats, seasons, hibernation and migration, and wildlife survey data. 100 questions with answers.",
            "Environments change; living things are affected.",
            "Some changes harm habitats, others protect them.",
            body(),
            [("How do environments change?", "Naturally, through seasons, floods, storms and droughts, and because of people, through building, pollution, litter and cutting down trees."),
             ("How can changes be dangerous to living things?", "Animals and plants can lose their food, water or shelter, be poisoned by pollution, or be killed by traffic."),
             ("How can people help?", "By creating nature reserves, ponds and hedgerows, planting wildflowers, putting up bird boxes and not dropping litter.")],
            sets)


if __name__ == "__main__":
    main()
