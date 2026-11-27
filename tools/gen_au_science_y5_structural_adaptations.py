# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U01: structural features of living things that help them survive in their habitat.
  python tools/gen_au_science_y5_structural_adaptations.py
Australian animals and plants (thorny devil, echidna, koala, kangaroo, platypus, bilby, banksia, spinifex, mangroves ...) plus
UK Year 6 adaptation makers with Australian names. Wrong answers come from real mistakes: "an animal grows a feature because it
needs it", "every feature is for keeping warm", mixing up structural features (body parts) and behaviours.
"""
from au_sci import AU, seed_of, make_au, tq, pool, rows

YEAR, SORT = 5, 1
U, R, P, src = AU(seed_of(YEAR, SORT))

uk_ad = src("gen_uk_science_y6_adaptation_and_evolution", "g_ad")
uk_hab = src("gen_uk_science_y6_adaptation_and_evolution", "g_hab", drop=["mountain goat"])

FEAT = [("thorny devil", "grooved skin between its spines", "to carry dew and rain to its mouth in the dry desert"),
        ("echidna", "sharp spines", "to protect it from predators such as dingoes"),
        ("echidna", "a long, sticky tongue", "to lick up ants and termites from their nests"),
        ("koala", "two thumbs on each front paw", "to grip eucalyptus branches"),
        ("red kangaroo", "long, strong back legs", "to hop long distances to find food and water"),
        ("red kangaroo", "a long, thick tail", "to balance while hopping"),
        ("platypus", "webbed front feet", "to push through the water when it swims"),
        ("platypus", "a sensitive bill", "to detect small animals in muddy water"),
        ("bilby", "very large ears", "to lose heat and hear predators at night"),
        ("wombat", "a backward-facing pouch", "to stop soil getting on the joey when the mother digs"),
        ("sugar glider", "a skin flap between its front and back legs", "to glide from tree to tree"),
        ("pelican", "a large throat pouch", "to scoop up fish from the water"),
        ("emu", "long, strong legs", "to run fast across open plains"),
        ("saltwater crocodile", "eyes and nostrils on top of its head", "to see and breathe while almost hidden underwater"),
        ("spinifex hopping mouse", "long back legs and a long tail", "to leap away from predators in the sand dunes"),
        ("banksia", "hard, woody seed pods", "to protect the seeds until a bushfire opens them"),
        ("eucalyptus", "thick, waxy leaves that hang down", "to lose less water and avoid the hot midday sun"),
        ("spinifex plant", "spiky, rolled-up leaves", "to lose less water in the hot desert"),
        ("grey mangrove", "breathing roots that stick up out of the mud", "to take in air when the roots are in salty, waterlogged mud"),
        ("saltbush", "grey, hairy leaves", "to reflect sunlight and lose less water"),
        ("desert oak", "very long roots", "to reach water deep underground"),
        ("water lily", "large, flat floating leaves", "to catch sunlight on the surface of the pond")]


def art(x):
    return ("an " if x[0] in "aeiou" and not x.startswith(("eu", "uni", "use")) else "a ") + x


def g_feat():
    o, f, h = R.choice(FEAT)
    k = R.choice(["how", "which", "who"])
    others = [x for x in FEAT if x[0] != o]
    if k == "how":
        return tq("%s has %s. How does this feature help it survive?" % (art(o).capitalize(), f), h,
                  [x[2] for x in R.sample(others, 3)], "This is a structural adaptation: a body part that helps the %s survive." % o)
    if k == "which":
        return tq("Which structural feature helps %s survive in its habitat?" % art(o), f, [x[1] for x in R.sample(others, 3)],
                  "The %s has %s %s." % (o, f, h))
    w = sorted({x[0] for x in others})
    return tq("Which living thing has %s %s?" % (f, h), art(o), [art(x) for x in R.sample(w, 3)],
              "Each living thing's features fit its own habitat.")


SB = [("long back legs for hopping", "structural"), ("a thick layer of fat (blubber)", "structural"), ("sharp claws for digging", "structural"),
      ("coming out only at night", "behavioural"), ("moving to cooler burrows during the day", "behavioural"), ("licking its forearms to cool down", "behavioural"),
      ("living in a group (a mob)", "behavioural"), ("migrating to warmer waters to breed", "behavioural"), ("a waxy coating on its leaves", "structural"),
      ("camouflage colours on its skin", "structural"), ("playing dead when attacked", "behavioural"), ("webbed feet", "structural"),
      ("building a nest high in a tree", "behavioural"), ("large ears that lose heat", "structural")]


def g_sb():
    f, t = R.choice(SB)
    return tq("Is %s a structural feature or a behaviour?" % f, "a " + t + " adaptation", ["a behavioural adaptation" if t == "structural" else "a structural adaptation",
              "not an adaptation", "a life cycle stage"], "Structural adaptations are body parts; behavioural adaptations are things an animal does.")


HAB = [("hot, dry desert", ["water-storing stems", "deep or spreading roots", "small or spiky leaves", "pale colours that reflect heat"]),
       ("cold ocean", ["a thick layer of blubber", "waterproof feathers or fur", "a streamlined body"]),
       ("rainforest", ["large leaves to catch dim light", "climbing tendrils", "gripping hands or tails"]),
       ("muddy, salty shore", ["breathing roots above the mud", "leaves that get rid of salt", "seeds that float"])]


def g_hab():
    h, fs = R.choice(HAB)
    a = R.choice(fs)
    w = [R.choice(x[1]) for x in HAB if x[0] != h]
    return tq("Which feature would most help a living thing survive in a %s?" % h, a, w, "Features fit the conditions of the habitat.")


POOL1 = pool(R, [
    ("What is a structural adaptation?", "a body part or feature that helps a living thing survive", ["something an animal learns to do", "a change in the weather", "a type of food"], "Examples: a kangaroo's tail, a koala's thumbs."),
    ("Why do many desert animals have large ears?", "Blood flowing through the ears loses heat, keeping the animal cool.", ["to store water", "to dig burrows", "to catch insects"], "Bilbies have large ears."),
    ("Why do echidnas have spines?", "to protect them from predators", ["to keep them cool", "to help them swim", "to catch fish"], "They curl into a spiky ball."),
    ("Why is the platypus bill so useful?", "It senses small electrical signals from prey in muddy water.", ["It stores fat.", "It cracks hard nuts.", "It keeps the platypus warm."], "The platypus closes its eyes underwater."),
    ("A plant has thick, waxy leaves. In which habitat is it most likely to live?", "a hot, dry place", ["a shady rainforest floor", "a freshwater pond", "a snowy mountain top only"], "Wax reduces water loss."),
    ("Why do some gum trees have leaves that hang down?", "Less of the leaf faces the hot midday sun, so less water is lost.", ["to catch more rain", "so koalas cannot eat them", "to make more seeds"], "This reduces heat and water loss."),
    ("How do the woody pods of banksias help them survive bushfires?", "The pods protect seeds and open after a fire.", ["They put out the fire.", "They stop leaves burning.", "They make the tree grow faster."], "New plants grow after the fire."),
    ("A sugar glider has skin flaps between its legs. What does this help it do?", "glide between trees", ["dig burrows", "swim quickly", "store food"], "Gliding saves energy and escapes predators."),
    ("Why does a kangaroo have a strong tail?", "to balance and to lean on like a fifth leg", ["to keep flies away only", "to store water", "to swim"], "The tail helps with hopping and resting."),
    ("A fish has a streamlined body. How does this help?", "It moves through water easily.", ["It keeps it warm.", "It helps it see in the dark.", "It helps it breathe air."], "Less water pushes against it."),
])
POOL5 = pool(R, [
    ("Ruby says, 'The camel grew a hump because it needed to store fat.' Why is this not correct?", "Features are inherited; animals with useful features survive and pass them on.", ["Camels store water, not fat.", "The hump grows every summer.", "Camels do not live in deserts."], "Living things do not grow new parts because they need them."),
    ("A new animal has thick fur, small ears and white colour. Which habitat suits it best?", "a cold, snowy place", ["a hot desert", "a tropical reef", "a muddy shore"], "Thick fur keeps it warm; white is camouflage in snow."),
    ("Two kinds of plants grow in a desert. One has wide, thin leaves and one has small, spiky leaves. Which survives better?", "the plant with small, spiky leaves", ["the plant with wide, thin leaves", "both the same", "neither can grow"], "Smaller leaves lose less water."),
    ("Why do frogs in the outback burrow underground in dry seasons?", "to stay cool and moist until rain comes", ["to find snow", "to lay eggs in the sand", "to escape the rain"], "This is a behaviour, helped by their body features."),
    ("Which pair matches a feature to its use correctly?", "pelican: throat pouch for scooping fish", ["koala: long legs for hopping", "emu: webbed feet for swimming", "echidna: wings for gliding"], "Match the feature to the job."),
    ("Mia tests how leaf shape affects water loss using paper leaves. What should she keep the same?", "the total area of paper, the temperature and the wind", ["the shape of the leaves", "only the colour", "nothing"], "Change one thing; keep the others the same."),
])


def main():
    sets = U.sets([
        ("What is an adaptation?", [(POOL1, 6), (g_sb, 6), (g_feat, 8)]),
        ("Australian animals and plants", [(g_feat, 14), (uk_ad, 4), (POOL1, 2)]),
        ("Features around the world", [(g_feat, 8), (g_hab, 6), (uk_ad, 3), (POOL1, 2), (uk_hab, 1)]),
        ("Habitats and features", [(g_hab, 6), (uk_hab, 5), (uk_ad, 4), (g_sb, 4), (POOL5, 1)]),
        ("Investigations and explanations", [(POOL5, 5), (g_feat, 8), (uk_ad, 4), (g_sb, 3)]),
    ])
    make_au(YEAR, "structural-adaptations", SORT, "AC9S5U01", "Biological sciences",
            "Examine how particular structural features and behaviours of living things enable their survival in specific habitats "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Structural Adaptations", "Structural adaptations",
            "Free Year 5 science worksheets on structural adaptations: how the body parts of Australian animals and plants help them survive in "
            "deserts, rainforests, oceans and mangroves. 100 questions with answers.",
            "Body parts fit the habitat.", "Structural adaptations are features a living thing is born with.",
            "<p><b>A structural adaptation is a body part that helps a living thing survive.</b></p><ul>"
            "<li>Look at the habitat first: is it hot, dry, cold, wet, salty or dark?</li>"
            "<li>Then match the feature: a thorny devil's grooved skin collects water; a koala's two thumbs grip branches; banksia pods open after fire.</li>"
            "<li>Behavioural adaptations are things a living thing does, such as coming out at night.</li></ul>",
            [("Bilby with large ears in the desert. Why?", ["the desert is hot", "ears lose heat and hear predators"], "keeps cool, hears danger"),
             ("Spiky, rolled-up leaves. Habitat?", ["small leaf area loses less water"], "hot, dry desert")],
            ["Saying an animal grows a feature because it needs it.", "Mixing up structural features (body parts) and behaviours (actions).",
             "Thinking every feature is for keeping warm."],
            [("What is the difference between a structural and a behavioural adaptation?", "A structural adaptation is a body part, such as a kangaroo's tail. A behavioural adaptation is something a living thing does, such as a bilby coming out at night."),
             ("How are desert plants adapted?", "Many have small, spiky or waxy leaves that lose less water, deep or spreading roots to collect water, and stems that store water."),
             ("Why do Australian animals have such different features?", "They live in many habitats, from deserts to rainforests and reefs. Over a long time, living things with features that suit their habitat survive and reproduce.")],
            sets)


if __name__ == "__main__":
    main()
