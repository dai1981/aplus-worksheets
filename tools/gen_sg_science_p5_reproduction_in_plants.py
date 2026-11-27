# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Reproduction in plants (Cycles)
  python tools/gen_sg_science_p5_reproduction_in_plants.py
Flowering plants reproduce by seeds: pollination (pollen from the anther to the stigma, by insects or wind),
fertilisation (the male and female reproductive cells join in the ovule), the ovule becomes a seed and the ovary becomes a fruit.
Seeds are dispersed by wind, water, animals and splitting (explosive action). Ferns and mosses reproduce by spores.
Singapore plants (angsana, lalang, coconut, sea almond, love grass, balsam, rubber tree, saga) are used for dispersal;
UK Year 5 flower-part and dispersal-distance questions are reused with Singapore names ("pistil" for the female part).
Wrong answers come from real mistakes: "pollination and fertilisation are the same", "the petals become the fruit",
"the stigma makes pollen", "all fruits are dispersed by animals", "seeds dispersed by wind are heavy".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63501)
R = U.R
P = People(R)
REP = [(r"\bcarpels?\b", "pistil"), (r"\bCarpels?\b", "Pistil")]
DROP = ["asexual", "cutting", "runner", "bulb", "tuber", "plantlet", "sycamore", "goosegrass", "cleavers", "thistle", "cherry", "conker", "horse chestnut",
        "squirrel", "winter", "nectary", "dandelion", "acorn", "blackberr", "burdock", "poppy", "hen", "cockerel", "starfish", "lime seed"]
RP = use(U, "gen_uk_science_y5_reproduction_in_plants_and_animals", rep=REP, drop=DROP)
FL = use(U, "gen_uk_science_y3_flowers_pollination_and_seeds", rep=REP, drop=DROP)

DISP = {"wind": [("angsana", "wing-like structure"), ("lalang", "hair-like structures"), ("shorea (meranti)", "wing-like structures"),
                 ("cotton (kapok) tree", "fluffy hairs"), ("African tulip tree", "papery wings")],
        "water": [("coconut", "fibrous husk that traps air"), ("sea almond", "fibrous, spongy husk"), ("pong pong", "fibrous husk"), ("lotus", "spongy seed head")],
        "animals": [("love grass", "hooks that stick to fur and clothes"), ("mango", "juicy flesh that animals eat"), ("rambutan", "sweet, juicy flesh"),
                    ("chiku", "sweet, soft flesh"), ("tomato", "juicy flesh with small seeds")],
        "splitting": [("balsam", "fruit that bursts open when touched"), ("rubber tree", "dry fruit that splits open with a pop"), ("saga", "pod that twists and splits open")]}
HOW = {"wind": "by wind", "water": "by water", "animals": "by animals", "splitting": "by splitting (explosive action)"}
FEAT_W = {"wind": "They are small and light, with wings or hairs.", "water": "They have a fibrous husk that traps air, so they float.",
          "animals": "They are juicy and eaten, or have hooks that catch on fur.", "splitting": "The dry fruit splits open and flings the seeds out."}


def g_disp():
    m = R.choice(sorted(DISP))
    p, f = R.choice(DISP[m])
    k = R.choice(["how", "which", "feat"])
    if not once(("dp", p, k)):
        return None
    if k == "how":
        return item("How are the seeds or fruits of the %s dispersed?" % p, HOW[m], [HOW[x] for x in sorted(HOW) if x != m],
                    "Feature of the %s: %s. %s" % (p, f, FEAT_W[m]))
    if k == "which":
        others = [R.choice(DISP[x])[0] for x in sorted(DISP) if x != m]
        return item("Which of these plants has its seeds dispersed %s?" % HOW[m], "the " + p, ["the " + o for o in others], FEAT_W[m])
    return item("A fruit has a %s. How is it most likely dispersed?" % f, HOW[m], [HOW[x] for x in sorted(HOW) if x != m], FEAT_W[m])


PARTS = [("anther", "makes pollen", "male"), ("filament", "holds up the anther", "male"), ("stigma", "receives pollen; it is often sticky", "female"),
         ("style", "connects the stigma to the ovary", "female"), ("ovary", "contains the ovules and becomes the fruit", "female"),
         ("ovule", "contains the female reproductive cell and becomes the seed", "female"), ("petal", "is often brightly coloured to attract insects", None),
         ("sepal", "protects the flower when it is a bud", None)]


def g_part():
    n, job, sex = R.choice(PARTS)
    k = R.choice(["job", "name", "sex"])
    if k == "sex" and not sex:
        return None
    if not once(("pt", n, k)):
        return None
    others = [x for x in PARTS if x[0] != n]
    if k == "job":
        return item("What does the %s of a flower do?" % n, "It " + job + ".", ["It " + x[1] + "." for x in R.sample(others, 3)], "The %s %s." % (n, job))
    if k == "name":
        return item("Which part of a flower %s?" % job, "the " + n, ["the " + x[0] for x in R.sample(others, 3)], "The %s %s." % (n, job))
    return item("Is the %s part of the male or the female part of a flower?" % n, "the %s part (%s)" % (sex, "stamen" if sex == "male" else "pistil"),
                ["the %s part (%s)" % ("female" if sex == "male" else "male", "pistil" if sex == "male" else "stamen"), "neither: it is a petal", "neither: it is a sepal"],
                "The stamen (anther and filament) is male; the pistil (stigma, style and ovary) is female.")


STEPS = ["Pollen is carried from the anther to the stigma (pollination).", "A pollen tube grows down the style to the ovule.",
         "The male reproductive cell joins with the female reproductive cell in the ovule (fertilisation).",
         "The ovule develops into a seed and the ovary develops into a fruit.", "The seeds are dispersed and germinate into new plants."]


def g_step():
    i = R.randrange(len(STEPS) - 1)
    k = R.choice(["next", "before"])
    if not once(("st", i, k)):
        return None
    if k == "next":
        return item("<i>%s</i> What happens next?" % STEPS[i], STEPS[i + 1], [x for j, x in enumerate(STEPS) if j not in (i, i + 1)][:3],
                    "Pollination → fertilisation → seed and fruit → dispersal → germination.")
    return item("<i>%s</i> What happened just before this?" % STEPS[i + 1], STEPS[i], [x for j, x in enumerate(STEPS) if j not in (i, i + 1)][:3],
                "Pollination → fertilisation → seed and fruit → dispersal → germination.")


def g_poll():
    feats = [("large, brightly coloured petals", "insects"), ("a sweet scent and nectar", "insects"), ("sticky or spiky pollen grains", "insects"),
             ("small, dull petals and no scent", "wind"), ("light, smooth pollen made in large amounts", "wind"), ("feathery stigmas that hang outside the flower", "wind"),
             ("anthers that hang outside the flower on long filaments", "wind")]
    f, a = R.choice(feats)
    if not once(("pl", f)):
        return None
    return item("A flower has %s. How is it most likely pollinated?" % f, "by %s" % a, ["by %s" % ("wind" if a == "insects" else "insects"), "by water only", "it does not need pollination"],
                "Insect-pollinated flowers attract insects; wind-pollinated flowers make light pollen that is blown about.")


def g_dist():
    seeds = {"angsana fruit": (300, 420), "lalang seed": (400, 520), "mango seed": (20, 40), "balsam seed": (60, 90), "paper model with large wings": (250, 350),
             "paper model with small wings": (120, 180)}
    pick = R.sample(sorted(seeds), 3)
    d = [R.randint(*seeds[x]) for x in pick]
    k = R.choice(["far", "why", "var", "fan"])
    if not once(("ds", k), 1 if k in ("var", "fan") else 3):
        return None
    tb = table(["Seed or fruit", "Distance travelled from a fan (cm)"], [[x, str(v)] for x, v in zip(pick, d)])
    q0 = "%s dropped seeds and fruits from the same height in front of a fan.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(d, pick))
    if k == "far":
        return item(q0 + "Which travelled the furthest?", s[-1][1], [x for _, x in s[:-1]] + ["they all travelled the same distance"], "Compare the distances.")
    if k == "why":
        return item(q0 + "Why did the %s travel the furthest?" % s[-1][1], "It is light and has wings or hairs that catch the wind.",
                    ["It is the heaviest.", "It is juicy.", "It has hooks."], "Seeds dispersed by wind are small and light, with wings or hairs.")
    if k == "var":
        return item(q0 + "What was changed in this experiment?", "the type of seed or fruit", ["the height they were dropped from", "the speed of the fan", "the distance travelled"],
                    "Only the seed or fruit was changed.")
    return item(q0 + "Why was the fan kept at the same speed?", "so that the test was fair", ["to make the seeds heavier", "to make the seeds germinate", "to make the seeds juicy"],
                "Only one variable should be changed.")


B1 = bank([
    ("What is pollination?", "the transfer of pollen from the anther to the stigma", ["the joining of male and female reproductive cells", "the spreading of seeds", "the growth of a seed into a seedling"], "Pollination comes before fertilisation."),
    ("What is fertilisation?", "the joining of the male reproductive cell and the female reproductive cell", ["the transfer of pollen", "the spreading of seeds", "the falling of petals"], "It takes place in the ovule."),
    ("After fertilisation, what does the ovary develop into?", "a fruit", ["a seed", "a flower", "a root"], "The ovules inside become the seeds."),
    ("After fertilisation, what does the ovule develop into?", "a seed", ["a fruit", "a petal", "pollen"], "Each fertilised ovule becomes one seed."),
    ("Which part of the flower is the male part?", "the stamen", ["the pistil", "the sepal", "the petal"], "The stamen is the anther and the filament."),
    ("Which part of the flower is the female part?", "the pistil", ["the stamen", "the sepal", "the anther"], "The pistil is the stigma, style and ovary."),
    ("Why is seed dispersal important?", "Young plants grow away from the parent and do not compete for light, water and space.", ["It makes the parent plant bigger.", "It stops the seeds from germinating.", "It makes more flowers."], "Overcrowding means less light, water and space for each plant."),
    ("How do ferns and mosses reproduce?", "by spores", ["by seeds", "by fruits", "by flowers"], "Ferns make spores under their leaves."),
])
B2 = bank([
    ("A watermelon has many seeds. What does this tell us about its flower?", "Many ovules were fertilised.", ["Its flower had many petals.", "Its flower had many stigmas.", "It was not pollinated."], "Each seed came from a fertilised ovule."),
    ("Why do the petals of a flower wither after fertilisation?", "They are no longer needed to attract insects.", ["They turn into seeds.", "They become the fruit.", "They protect the seed."], "The ovary grows into the fruit instead."),
    ("Which statement about pollination and fertilisation is correct?", "Pollination happens first, then fertilisation.", ["Fertilisation happens first.", "They are the same thing.", "Only fertilisation needs pollen."], "Pollen must reach the stigma before fertilisation can happen."),
    ("Why do insect-pollinated flowers have nectar?", "to attract insects, which pick up pollen while feeding", ["to make the seeds sweet", "to feed the flower", "to keep the flower warm"], "Insects carry pollen to other flowers."),
    ("Why do wind-pollinated flowers produce large amounts of pollen?", "Most of the pollen is blown away and never reaches a stigma.", ["The pollen is food for insects.", "The pollen becomes the seeds.", "They have no anthers."], "Producing a lot increases the chance of pollination."),
    ("Why might a fruit tree in a greenhouse with no insects produce very few fruits?", "Few flowers are pollinated.", ["It gets too much light.", "It gets too much water.", "Its roots are too long."], "Without pollination there is no fertilisation."),
    ("What does a pollen grain contain?", "the male reproductive cell", ["the female reproductive cell", "a seed", "food for the fruit"], "The female reproductive cell is in the ovule."),
    ("Which happens to the ovary wall as the fruit forms?", "It grows and may become fleshy or dry.", ["It turns into petals.", "It becomes the seed coat only.", "It falls off with the petals."], "Mangoes have fleshy fruit walls; balsam pods are dry."),
])
B3 = bank([
    ("Why are coconuts often found growing on beaches?", "The fibrous husk traps air, so coconuts float and are carried by the sea.", ["Coconuts are dropped by birds.", "Coconuts explode.", "The wind blows them there."], "Coconuts are dispersed by water."),
    ("Why do seeds dispersed by animals often have juicy, brightly coloured fruits?", "to attract animals to eat them", ["to float on water", "to be carried by wind", "to split open"], "The seeds pass out in the animal's droppings far away."),
    ("Love grass seeds stick to your socks after a walk in a field. How are they dispersed?", "by animals (and people), with hooks", ["by wind", "by water", "by splitting"], "The tiny hooks catch on fur and clothes."),
    ("Why does a balsam fruit burst open when touched?", "to fling its seeds away from the parent plant", ["to attract insects", "to take in water", "to make food"], "This is dispersal by splitting (explosive action)."),
    ("Why do wind-dispersed seeds need to be light?", "so that they can be carried far by the wind", ["so that animals eat them", "so that they sink", "so that they burst open"], "Heavy seeds fall near the parent."),
    ("Which feature would most help a fruit to float?", "a fibrous husk with air spaces", ["juicy flesh", "hooks", "a heavy, hard shell with no air"], "Trapped air makes the fruit float."),
    ("A seed with wings fell 20 m from its parent tree. A seed of the same size without wings fell 3 m away. What does this show?", "Wings help seeds to be carried further by the wind.", ["Wings make seeds heavier.", "Seeds without wings are dispersed by animals.", "Wings stop seeds from moving."], "Wings increase the surface area to catch the wind."),
])
B4 = bank([
    ("Where are the spores of a fern found?", "in spore cases on the underside of its leaves", ["inside its fruits", "in its flowers", "in its roots"], "The brown dots under fern leaves are spore cases."),
    ("Which of these plants does NOT produce flowers?", "a fern", ["a hibiscus", "a balsam", "a rain tree"], "Ferns and mosses reproduce by spores."),
    ("Which condition helps spores to grow into new ferns?", "a damp, shady place", ["a hot, dry place", "a freezer", "a sealed dark box with no water"], "Ferns and mosses grow well in damp places."),
    ("A papaya fruit has hundreds of seeds. How many ovules were fertilised?", "about the same number as the number of seeds", ["only one", "none", "more than ten times the number of seeds"], "Each seed comes from one fertilised ovule."),
    ("A mango fruit has one seed. What does this tell us about its ovary?", "Only one ovule developed into a seed.", ["The flower had one petal.", "The flower was not pollinated.", "The fruit grew from the stigma."], "One fertilised ovule gives one seed."),
    ("Why do some plants make many seeds?", "Many seeds may be eaten or land in poor places, so making many helps some survive.", ["Plants cannot count.", "All seeds always grow.", "Seeds are needed to make food."], "Only some seeds land in good places to grow."),
    ("Which shows the correct order?", "pollination → fertilisation → seed and fruit formation → seed dispersal → germination", ["fertilisation → pollination → germination → seed dispersal", "seed dispersal → pollination → fertilisation → germination", "germination → fertilisation → pollination → seed dispersal"], "Each step needs the one before it."),
    ("Which statement about pollen is correct?", "It is made in the anther and contains the male reproductive cell.", ["It is made in the ovary.", "It becomes the fruit.", "It contains the female reproductive cell."], "The ovule contains the female reproductive cell."),
    ("Which part of the fruit protects the seeds?", "the fruit wall, which develops from the ovary wall", ["the petals", "the stamen", "the stigma"], "The fruit protects the seeds and helps disperse them."),
])
B5 = bank([
    ("Siti covered some hibiscus flowers with plastic bags before they opened. Why did these flowers produce no fruits?", "Insects could not reach them, so they were not pollinated.", ["They got no light.", "They got too much water.", "The bags made the petals fall."], "No pollination means no fertilisation."),
    ("Ravi removed the anthers from a flower and covered it. Why did it not develop into a fruit?", "No pollen could reach the stigma.", ["It had no petals.", "It had no ovary.", "It had no sepals."], "Removing the anthers stops self-pollination."),
    ("Mei Ling made paper models of seeds with wings of different lengths and dropped them from 2 m. What was she investigating?", "how wing length affects the time taken for the seed to fall", ["how heavy the paper is", "how fast seeds germinate", "how insects pollinate flowers"], "A seed that falls slowly can be carried further by the wind."),
    ("Why should each paper model be dropped three times?", "to get more reliable results", ["to make it heavier", "to make it fall faster", "to change the variable"], "Taking an average reduces errors."),
    ("A pupil found that seeds which fell further from the parent tree grew into taller seedlings. What is the most likely reason?", "They had less competition for light, water and space.", ["They were heavier.", "They had more petals.", "They grew in the dark."], "Seeds near the parent are shaded."),
    ("Which of these would show that a fruit is dispersed by water?", "It floats in a tank of water for a week.", ["It sinks at once.", "It sticks to cloth.", "It bursts open when dry."], "Floating fruits can be carried by rivers and the sea."),
])


def body():
    think = ("<p><b>Flowering plants reproduce by seeds.</b></p>"
             "<ul><li><b>Pollination</b>: pollen moves from the anther to the stigma (by insects or wind).</li>"
             "<li><b>Fertilisation</b>: the male reproductive cell (from the pollen) joins the female reproductive cell in the ovule.</li>"
             "<li>The ovule becomes a <b>seed</b>; the ovary becomes a <b>fruit</b>.</li>"
             "<li>Seeds are <b>dispersed</b> by wind, water, animals or splitting, so new plants do not compete with the parent.</li>"
             "<li>Ferns and mosses reproduce by <b>spores</b>.</li></ul>")
    ex = [("A flower is covered so no insects reach it. What happens?", ["No pollen reaches the stigma", "No fertilisation"], "No fruit or seeds form."),
          ("A coconut is found on a beach far from any tree. How did it get there?", ["Its husk traps air", "It floats"], "By water.")]
    mist = ["Mixing up pollination and fertilisation. Pollination is the transfer of pollen; fertilisation is the joining of the reproductive cells.",
            "Thinking the petals become the fruit. The ovary becomes the fruit.",
            "Thinking the stigma makes pollen. The anther makes pollen.",
            "Thinking all fruits are dispersed by animals. Look at the features: wings, husk, hooks or splitting pods."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Parts of a flower", B1 + [(g_part, 9), (FL.g_fpart, 3)]),
        ("Pollination and fertilisation", B2 + [(g_step, 6), (g_poll, 6)]),
        ("Seed dispersal", B3 + [(g_disp, 13)]),
        ("Spores, seeds and fruits", B4 + [(g_disp, 5), (g_part, 3), (g_poll, 1), (g_step, 2)]),
        ("PSLE-style experiments", B5 + RP.B5 + [(g_dist, 5), (RP.g_dist, 4), (g_disp, 3)]),
    ])
    make_sg(5, "reproduction-in-plants", 1, "Cycles", "Cycles in plants and animals (Reproduction in plants)",
            "Identify the parts of a flower and their functions in reproduction. Describe the processes of pollination, fertilisation (the fusion of the male and "
            "female reproductive cells), seed and fruit formation, and seed dispersal by wind, water, animals and splitting. Recognise that some plants reproduce "
            "by spores (summary of the MOE Primary Science Syllabus).",
            "Reproduction in Plants",
            "Primary 5 Science: Reproduction in Plants Worksheets (with Answers)",
            "Reproduction in plants",
            "Free Primary 5 science worksheets for Singapore pupils on reproduction in plants: flower parts, pollination, fertilisation, fruits and seeds, seed dispersal and spores. 100 questions with answers.",
            "Pollination, fertilisation, seeds, dispersal.",
            "The ovule becomes a seed; the ovary becomes a fruit.",
            body(),
            [("What is the difference between pollination and fertilisation?", "Pollination is the transfer of pollen from the anther to the stigma. Fertilisation is the joining of the male and female reproductive cells in the ovule, which happens after pollination."),
             ("Which part of the flower becomes the fruit?", "The ovary becomes the fruit, and the fertilised ovules inside it become the seeds."),
             ("How are seeds dispersed?", "By wind (light, with wings or hairs), by water (fibrous husk that floats), by animals (juicy fruits or hooks) and by splitting (dry fruits that burst open).")],
            sets)


if __name__ == "__main__":
    main()
