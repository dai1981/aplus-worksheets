# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Biology): Plant Reproduction
  python tools/gen_uk_science_y7_plant_reproduction.py
Reproduction in plants, including flower structure, wind and insect pollination, fertilisation, seed and fruit
formation and dispersal, including quantitative investigation of some dispersal mechanisms (falling times of winged
seeds, distances travelled). Reuses the flower, pollination and dispersal questions of the Year 5 unit (new seed).
Wrong answers come from real mistakes: "pollination and fertilisation are the same", "the stigma makes pollen",
"wind-pollinated flowers are brightly coloured", "the ovary becomes the seed".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y5_reproduction_in_plants_and_animals as Y5
from sci_phys import uniq

Y5.U = Unit(61705)
Y5.R = Y5.U.R
Y5.P = People(Y5.R)
uk_sci.USED.clear()
U, R, P = Y5.U, Y5.R, Y5.P

SEX = [("the anther", "male"), ("the filament", "male"), ("the stigma", "female"), ("the style", "female"), ("the ovary", "female"), ("the ovules", "female"),
       ("pollen grains", "male")]


def g_sex():
    p, s = R.choice(SEX)
    if not once(("se", p)):
        return None
    a = "the male part (stamen)" if s == "male" else "the female part (carpel)"
    return item("Is %s part of the male or the female part of a flower?" % p, a, ["the female part (carpel)" if s == "male" else "the male part (stamen)", "neither: it is a petal", "neither: it is a sepal"],
                "Stamen (male) = anther + filament. Carpel (female) = stigma + style + ovary.")


def g_fall():
    who = P.next()[0]
    wings = [2, 3, 4, 5]
    base = R.choice([0.8, 0.9, 1.0])
    step = R.choice([0.3, 0.4, 0.5])
    t = [round(base + step * i, 1) for i in range(4)]
    k = R.choice(["read", "pattern", "long", "fair", "predict"])
    ri = R.randrange(4)
    if not once(("fa", base, step, k, ri if k == "read" else 0)) or (k in ("pattern", "fair") and not once(("fk", k), 2)):
        return None
    tab = table(["Wing length of paper seed (cm)", "Mean time to fall 2 m (s)"], [[str(w), "%.1f" % x] for w, x in zip(wings, t)])
    intro = tab + "%s dropped model sycamore seeds with different wing lengths from 2 m. " % who
    if k == "read":
        g = "%.1f s" % t[ri]
        return item(intro + "What was the mean falling time for wings %d cm long?" % wings[ri], g, uniq(g, ["%.1f s" % x for x in t] + ["%d s" % wings[ri]]), "Read the row.")
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The longer the wings, the longer the seed takes to fall.", ["Longer wings make seeds fall faster.", "Wing length makes no difference.", "All seeds fall in 1 second."],
                    "A slower fall lets the wind carry the seed further.")
    if k == "long":
        return item(intro + "Which wing length would probably let the wind carry the seed furthest?", "5 cm", ["2 cm", "3 cm", "4 cm"], "It falls most slowly.")
    if k == "fair":
        return item(intro + "Which should %s keep the same for a fair test?" % who, "the drop height and the type of paper", ["the wing length", "the falling time", "nothing"], "Only the wing length changes.")
    g = "%.1f s" % round(t[3] + step, 1)
    return item(intro + "If the pattern continues, predict the time for wings 6 cm long.", g, uniq(g, ["%.1f s" % t[3], "%.1f s" % round(t[3] + 2 * step, 1), "6 s", "%.1f s" % t[0]]),
                "Each extra 1 cm adds about %.1f s." % step)


B1 = bank([
    ("What is pollination?", "the transfer of pollen from an anther to a stigma", ["the joining of pollen and ovule nuclei", "the spreading of seeds", "the growth of a seed"], "It comes before fertilisation."),
    ("What is fertilisation in a plant?", "when the pollen nucleus joins with the ovule nucleus", ["when pollen lands on the stigma", "when seeds are dispersed", "when a petal falls off"], "It happens in the ovary."),
    ("What grows down from the pollen grain to reach the ovule?", "a pollen tube", ["a root", "a stamen", "a sepal"], "Through the style."),
    ("After fertilisation, what does the ovule become?", "a seed", ["a fruit", "a petal", "a leaf"], "The ovary becomes the fruit."),
    ("After fertilisation, what does the ovary become?", "a fruit", ["a seed", "a root", "a stamen"], "It surrounds the seeds."),
    ("Why do insect-pollinated flowers have nectar?", "to attract insects, which carry pollen", ["to make seeds heavy", "to keep out the rain", "to stop pollination"], "A reward for insects."),
    ("Why do wind-pollinated flowers make lots of pollen?", "Most pollen blown by the wind never reaches a stigma.", ["Insects eat it all.", "It is very heavy.", "They have no stigmas."], "Chance."),
    ("What is seed dispersal?", "the spreading of seeds away from the parent plant", ["the growth of a seed", "the release of pollen", "the opening of a flower"], "Wind, animals, water, explosion."),
])
B5 = bank([
    ("Why is seed dispersal important?", "It reduces competition with the parent plant for light, water and nutrients.", ["It makes seeds smaller.", "It stops pollination.", "It helps the parent grow taller."], "Less competition."),
    ("Why are the results of a seed-falling test repeated and averaged?", "to make the results more reliable", ["to make the test quicker", "to change the answer", "because the first result is always wrong"], "Repeat readings."),
    ("Why do bees matter to farmers who grow apples and strawberries?", "Bees pollinate the flowers, so fruits form.", ["Bees eat pests only.", "Bees water the crops.", "Bees make the soil richer."], "Pollinators."),
    ("Why might a plant with hooked seeds grow along footpaths?", "Its seeds stick to animal fur and people's clothes and fall off along paths.", ["Wind blows only along paths.", "Footpaths are wet.", "Hooks make seeds heavy."], "Animal dispersal."),
    ("Self-pollination uses pollen from the same plant. What is one disadvantage?", "The offspring vary less.", ["It needs insects.", "It needs wind.", "It cannot make seeds."], "Cross-pollination increases variation."),
])


def body():
    think = ("<p><b>Flowers are the reproductive organs of flowering plants.</b></p>"
             "<ul><li>Stamen (male): anther and filament. Carpel (female): stigma, style and ovary.</li>"
             "<li>Pollination moves pollen to a stigma (by insects or wind). Fertilisation joins the pollen nucleus with an ovule nucleus.</li>"
             "<li>Ovules become seeds and the ovary becomes the fruit. Seeds are dispersed by wind, animals, water or explosion.</li></ul>")
    ex = [("Pollination or fertilisation: pollen lands on the stigma?", ["Transfer of pollen"], "pollination"),
          ("What does the ovary become?", ["It surrounds the seeds"], "the fruit")]
    mist = ["Thinking pollination and fertilisation are the same.", "Thinking the stigma makes pollen.", "Thinking wind-pollinated flowers are brightly coloured."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Flower structure", B1 + [(Y5.g_part, 8), (g_sex, 4)]),
        ("Pollination", [(Y5.g_part, 6), (Y5.g_poll, 8), (g_sex, 3), (Y5.g_step, 3)]),
        ("Fertilisation and seeds", [(Y5.g_step, 7), (Y5.g_disp, 8), (Y5.g_disp2, 5)]),
        ("Dispersal investigations", [(g_fall, 10), (Y5.g_dist, 10)]),
        ("Thinking about plants", B5 + [(g_fall, 6), (Y5.g_dist, 5), (Y5.g_disp2, 4)]),
    ])
    make_ks3(7, "plant-reproduction", 5, "Biology", "Reproduction",
             "Reproduction in plants, including flower structure, wind and insect pollination, fertilisation, seed and fruit formation and dispersal, including quantitative investigation of some dispersal mechanisms.",
             "Plant Reproduction",
             "Year 7 Science: Plant Reproduction Worksheets (Pollination, Fertilisation, Seed Dispersal)",
             "Plant Reproduction",
             "Free Year 7 science worksheets on plant reproduction: flower structure, insect and wind pollination, fertilisation, seeds and fruits, and seed dispersal investigations. 100 questions with answers.",
             "Pollination, then fertilisation, then seeds.",
             "Ovules become seeds; the ovary becomes the fruit.",
             body(),
             [("What is the difference between pollination and fertilisation?", "Pollination is the transfer of pollen to a stigma. Fertilisation happens later, when the pollen nucleus joins with an ovule nucleus inside the ovary."),
              ("How are wind- and insect-pollinated flowers different?", "Insect-pollinated flowers have bright petals, scent and nectar. Wind-pollinated flowers are small and dull, with lots of light pollen and feathery stigmas."),
              ("How are seeds dispersed?", "By wind (sycamore, dandelion), animals (berries, burrs), water (coconut) or by pods bursting open (peas, gorse).")],
             sets)


if __name__ == "__main__":
    main()
