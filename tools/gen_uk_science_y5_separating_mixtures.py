# -*- coding: utf-8 -*-
"""
UK Year 5 science: Separating Mixtures (Properties and changes of materials)
  python tools/gen_uk_science_y5_separating_mixtures.py
Choosing how to separate mixtures using what we know about solids, liquids and gases: sieving, filtering, evaporating
and using a magnet; separating a mixture of several materials in the right order; and how much solid is recovered.
Wrong answers come from real mistakes: "filtering removes dissolved salt", "a magnet picks up aluminium",
"evaporating destroys the salt", "a sieve can separate sugar from water".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61506)
R = U.R
P = People(R)

M_SIEVE = "sieving"
M_FILT = "filtering"
M_EVAP = "evaporating"
M_MAG = "using a magnet"
METHODS = [M_SIEVE, M_FILT, M_EVAP, M_MAG]
MIX = [("sand and water", M_FILT, "sand is insoluble and is caught by the filter paper"), ("salt and water", M_EVAP, "salt is dissolved, so the water must evaporate"),
       ("gravel and sand", M_SIEVE, "the gravel pieces are bigger than the holes"), ("iron filings and sand", M_MAG, "iron is magnetic; sand is not"),
       ("rice and flour", M_SIEVE, "the flour is fine enough to pass through"), ("chalk powder and water", M_FILT, "chalk is insoluble"),
       ("sugar and water", M_EVAP, "sugar is dissolved"), ("steel pins and sawdust", M_MAG, "steel is magnetic"), ("pebbles and soil", M_SIEVE, "pebbles are large"),
       ("muddy water", M_FILT, "mud is made of insoluble bits"), ("sea water (to get the salt)", M_EVAP, "salt is dissolved in sea water"),
       ("paperclips and marbles", M_MAG, "steel paperclips are magnetic; glass marbles are not"), ("peas and water", M_SIEVE, "peas are much bigger than the holes in a colander or sieve"),
       ("tea leaves and tea", M_FILT, "the leaves do not dissolve")]


def g_mix():
    m, a, why = R.choice(MIX)
    if not once(("mx", m)):
        return None
    return item("Which is the best way to separate %s?" % m, a, [x for x in METHODS if x != a], "Use %s because %s." % (a, why))


WHAT = [(M_SIEVE, "solids with different-sized pieces"), (M_FILT, "an insoluble solid from a liquid"), (M_EVAP, "a dissolved solid from a liquid"), (M_MAG, "a magnetic metal from other materials")]


def g_what():
    me, w = R.choice(WHAT)
    k = R.random() < 0.5
    if not once(("wh", me, k)):
        return None
    if k:
        return item("What can %s separate?" % me, w, [x[1] for x in WHAT if x[0] != me], "Each method uses a different property.")
    return item("Which method separates %s?" % w, me, [x for x in METHODS if x != me], "Each method uses a different property.")


STEPS = ["Use a magnet to remove the iron filings.", "Add water and stir so the salt dissolves.", "Filter to catch the sand.", "Evaporate the water to get the salt back."]


def g_multi():
    k = R.choice(["first", "next", "last", "why"])
    i = R.randrange(3)
    if not once(("mu", k, i if k == "next" else 0)):
        return None
    intro = "A mixture contains sand, salt and iron filings. "
    if k == "first":
        return item(intro + "Which step is a good first step?", STEPS[0], STEPS[1:], "Take out the magnetic iron first, while everything is dry.")
    if k == "last":
        return item(intro + "Which step comes last?", STEPS[3], STEPS[:3], "Evaporating leaves the dissolved salt behind at the end.")
    if k == "next":
        return item(intro + "After this step: \"%s\" What should you do next?" % STEPS[i], STEPS[i + 1], [x for x in STEPS if x not in (STEPS[i], STEPS[i + 1])],
                    "Magnet → dissolve → filter → evaporate.")
    return item(intro + "Why is water added and stirred before filtering?", "so the salt dissolves and passes through the filter, leaving the sand", ["to make the sand dissolve", "to make the iron rust", "to make the salt magnetic"],
                "Only the dissolved salt goes through the filter paper.")


def g_rec():
    who = P.next()[0]
    s = R.choice([5, 8, 10, 12, 15, 20, 25])
    w = R.choice([50, 100, 150, 200])
    k = R.choice(["salt", "sand"])
    if not once(("rc", s, w, k)):
        return None
    if k == "salt":
        g = "%d g" % s
        return item("%s dissolves %d g of salt in %d g of water, then evaporates all the water. About how much salt is left?" % (who, s, w), g,
                    uniq(g, ["0 g", "%d g" % (s + w), "%d g" % w, "%d g" % (s // 2 if s % 2 == 0 else s - 1)]), "Evaporating removes only the water; all the salt is left.")
    g = "%d g" % s
    return item("%s mixes %d g of sand with %d g of water, filters it and dries the sand. About how much sand is collected?" % (who, s, w), g,
                uniq(g, ["0 g", "%d g" % (s + w), "%d g" % w, "%d g" % (s * 2)]), "The sand does not dissolve, so all of it is caught by the filter.")


TERMS = [("the residue", "the solid left in the filter paper"), ("the filtrate", "the liquid that passes through the filter"), ("a funnel", "holds the filter paper over a beaker"),
         ("filter paper", "has tiny holes that let liquid through but trap insoluble bits"), ("an evaporating dish", "a shallow dish heated so water evaporates"),
         ("a sieve", "a mesh with holes that let small pieces through")]


def g_term():
    t, d = R.choice(TERMS)
    k = R.random() < 0.5
    if not once(("tm", t, k)):
        return None
    if k:
        return item("In separating mixtures, what is %s?" % t, d, R.sample([x[1] for x in TERMS if x[0] != t], 3), "%s: %s." % (t.capitalize(), d))
    return item("Which word or piece of equipment matches this: %s?" % d, t, R.sample([x[0] for x in TERMS if x[0] != t], 3), "%s: %s." % (t.capitalize(), d))


KINDS = {"magnet": ["iron filings", "steel paperclips"], "sieve": ["gravel", "pebbles", "dried peas"], "filter": ["sand", "chalk powder"], "evaporate": ["salt", "sugar"]}
METH = {"magnet": "a magnet", "sieve": "a sieve", "filter": "filtering (after sieving, using a magnet and adding water)", "evaporate": "evaporating the water (after adding water and filtering)"}


def g_plan():
    ks = R.sample(sorted(KINDS), 3)
    parts = {k: R.choice(KINDS[k]) for k in ks}
    k = R.choice(ks)
    if not once(("pl", tuple(sorted(parts.values())), k)):
        return None
    names = sorted(parts.values())
    others = [parts[x] for x in ks if x != k] + ["nothing"]
    return item("A dry mixture contains %s, %s and %s. Which part is separated out by %s?" % (names[0], names[1], names[2], METH[k]), parts[k], others,
                {"magnet": "Only the magnetic metal is attracted.", "sieve": "Only the big pieces are too large to pass through.",
                 "filter": "The insoluble solid is caught in the filter paper.", "evaporate": "The dissolved solid is left when the water evaporates."}[k])


B1 = bank([
    ("What is a mixture?", "two or more materials mixed together but not joined", ["a single pure material", "a new material made by burning", "a type of magnet"], "Mixtures can be separated."),
    ("Can filtering separate salt from salty water?", "No. Dissolved salt passes through the filter paper.", ["Yes, the salt stays in the paper.", "Yes, if you filter twice.", "Only if the water is cold."], "Use evaporation."),
    ("Which metals does a magnet attract?", "iron, steel, nickel and cobalt", ["all metals", "aluminium and copper", "gold and silver"], "Most metals are not magnetic."),
    ("Why does evaporating leave salt behind?", "The water turns into a gas but the salt does not.", ["The salt is destroyed.", "The salt turns into water.", "The heat makes new salt."], "Salt has a much higher boiling point."),
    ("Which equipment do you need to filter?", "a funnel and filter paper", ["a magnet and a ruler", "a thermometer and a stopwatch", "a sieve and a magnet"], "Paper traps the solid."),
    ("What kind of change is dissolving salt in water?", "a reversible change", ["an irreversible change", "a burning change", "a magnetic change"], "You can get the salt back."),
    ("Why can a sieve not separate sugar from water?", "The dissolved sugar pieces are far too small to be caught.", ["Sieves only work on metal.", "Sugar is magnetic.", "Water blocks the holes."], "Dissolved pieces are tiny."),
    ("How is salt made from sea water in hot countries?", "Sea water is left in shallow pools until the Sun evaporates the water.", ["Sea water is filtered.", "Salt is picked out with a magnet.", "Sea water is frozen."], "Salt pans."),
])
B5 = bank([
    ("How could you check that filtered water still contains dissolved salt?", "Evaporate a little and see if salt is left.", ["Look to see if it is clear.", "Filter it again.", "Put a magnet in it."], "Test for the solute."),
    ("Why should you not taste mixtures in science lessons?", "They may be unsafe or contaminated.", ["They all taste the same.", "Tasting makes them separate.", "It is a fair test."], "Safety."),
    ("A recycling plant has steel and aluminium cans mixed together. How can they be separated?", "with a large magnet, which picks up the steel cans", ["with a sieve", "by filtering", "by dissolving them"], "Use properties."),
    ("Why is a coffee filter used when making coffee?", "It lets the coffee drink through but traps the insoluble grounds.", ["It dissolves the coffee.", "It makes coffee magnetic.", "It evaporates the water."], "Everyday filtering."),
    ("Why might filtering not get all the mud out of very muddy water?", "Some bits are very tiny and pass through the paper.", ["Mud is magnetic.", "Mud dissolves completely.", "Filter paper is waterproof."], "Limits of a method."),
])


def body():
    think = ("<p><b>Choose a separating method using the properties of the materials.</b></p>"
             "<ul><li>Sieving: solids with different-sized pieces. Magnet: magnetic metals (iron, steel).</li>"
             "<li>Filtering: an insoluble solid from a liquid (sand from water). Evaporating: a dissolved solid from a liquid (salt from water).</li>"
             "<li>For sand, salt and iron: magnet → add water and stir → filter → evaporate.</li></ul>")
    ex = [("Salt and water?", ["Salt is dissolved"], "evaporate the water"),
          ("Gravel and sand?", ["Different-sized pieces"], "sieve")]
    mist = ["Thinking filtering removes dissolved salt.", "Thinking a magnet picks up all metals.", "Thinking evaporating destroys the salt."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Methods", B1 + [(g_what, 6), (g_mix, 6)]),
        ("Choosing a method", [(g_mix, 8), (g_what, 2), (g_term, 10)]),
        ("Several steps", [(g_multi, 6), (g_term, 2), (g_rec, 12)]),
        ("Planning a separation", [(g_plan, 12), (g_rec, 8)]),
        ("Thinking it through", B5 + [(g_plan, 7), (g_rec, 8)]),
    ])
    make_uk(5, "separating-mixtures", 6, "Properties and changes of materials",
            "Use knowledge of solids, liquids and gases to decide how mixtures might be separated, including through filtering, sieving and evaporating.",
            "Separating Mixtures",
            "Year 5 Science: Separating Mixtures Worksheets (Sieving, Filtering, Evaporating)",
            "Separating Mixtures",
            "Free Year 5 science worksheets on separating mixtures: sieving, filtering, evaporating and magnets, separating a mixture in steps, and recovering materials. 100 questions with answers.",
            "Pick the method that fits the materials.",
            "Sieve sizes, filter insoluble bits, evaporate dissolved ones, use a magnet for iron.",
            body(),
            [("How do you separate sand from water?", "Filter it. The insoluble sand is caught by the filter paper and the water passes through."),
             ("How do you get salt back from salt water?", "Evaporate the water by heating it or leaving it in a warm place. The salt is left behind."),
             ("How would you separate sand, salt and iron filings?", "Use a magnet to take out the iron, add water and stir to dissolve the salt, filter out the sand, then evaporate the water to get the salt.")],
            sets)


if __name__ == "__main__":
    main()
