# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Adaptations (Interactions)
  python tools/gen_sg_science_p6_adaptations.py
An adaptation is a feature or behaviour that helps an organism survive in its habitat: to obtain food, escape from
predators, breathe, move, keep warm or cool, or reduce water loss. Structural adaptations are body parts;
behavioural adaptations are things the organism does.
Singapore examples: mangrove breathing roots and prop roots, mudskippers, pitcher plants, sunbirds, pangolins.
Wrong answers come from real mistakes: "rolling into a ball is a structural adaptation", "breathing roots
take in water", "an animal chooses to grow an adaptation during its life".
UK Year 6 adaptation makers are reused for animals of other habitats (desert, Arctic).
"""
from sg_sci import Unit, item, bank, lesson, make_sg, People, once, use, upto

U = Unit(63608)
R = U.R
P = People(R)
AD = use(U, "gen_uk_science_y6_adaptation_and_evolution", drop=["hump", "otter", "puffin", "finch", "moth", "evolv", "evolution", "inherit"])

S, B = "structural", "behavioural"
# organism, feature (noun phrase, after 'has' / or a verb phrase for behaviour), type, purpose
ADAPT = [
    ("mangrove tree", "breathing roots that stick up out of the mud", S, "to take in air from above the waterlogged mud"),
    ("mangrove tree", "prop roots that spread out above the mud", S, "to support itself in the soft mud"),
    ("mudskipper", "gill chambers that hold water", S, "to breathe when it is out of the water"),
    ("mudskipper", "eyes on the top of its head", S, "to spot predators while it lies in the water"),
    ("pitcher plant", "leaves shaped like jugs that trap insects", S, "to get nutrients that are lacking in the soil"),
    ("water lily", "large, flat leaves that float on the water", S, "to get sunlight at the surface of the pond"),
    ("Hydrilla plant", "air spaces in its stems", S, "to float near the surface where there is more light"),
    ("stick insect", "a body that looks like a twig", S, "to hide from predators"),
    ("fish", "gills", S, "to take in oxygen dissolved in the water"),
    ("duck", "webbed feet", S, "to swim in water"),
    ("eagle", "sharp talons and a hooked beak", S, "to catch and tear its prey"),
    ("olive-backed sunbird", "a long, curved beak", S, "to reach the nectar deep inside flowers"),
    ("frog", "a long, sticky tongue", S, "to catch insects"),
    ("tortoise", "a hard shell", S, "to protect its soft body from predators"),
    ("cactus", "spines instead of leaves", S, "to lose less water"),
    ("pangolin", "rolls itself into a tight ball when attacked", B, "to protect its soft belly from predators"),
    ("millipede", "curls up when it is touched", B, "to protect itself from predators"),
    ("owl", "hunts at night", B, "to catch prey that are active at night"),
    ("spider", "spins a web", B, "to catch insects for food"),
    ("monitor lizard", "lies in the sun in the morning", B, "to warm up its body"),
    ("dog", "pants on a hot day", B, "to lose heat and keep cool"),
    ("small fish", "swims in large groups called schools", B, "to stay safe, because predators find it hard to pick out one fish"),
    ("Pacific golden plover", "flies to Singapore before the winter in the north", B, "to escape the cold and find food"),
    ("earthworm", "moves deeper into the soil in dry weather", B, "to stay in damp soil and avoid drying out"),
]


def says(o, f, t):
    w = a(o)
    w = w[0].upper() + w[1:]
    return ("%s has %s." % (w, f)) if t == S else ("%s %s." % (w, f))


def a(o):
    return ("an " if o[0] in "aeiou" else "a ") + o


def g_purpose():
    o, f, t, p = R.choice(ADAPT)
    if not once(("pu", o, f)):
        return None
    wrong = R.sample(sorted({x[3] for x in ADAPT if x[3] != p and x[0] != o}), 3)
    return item(says(o, f, t) + " How does this help it survive?", "It helps it " + p[3:] + ".", ["It helps it " + w[3:] + "." for w in wrong],
                "This adaptation helps the %s %s." % (o, p[3:]))


def g_type():
    o, f, t, p = R.choice(ADAPT)
    if not once(("ty", o, f)):
        return None
    ot = B if t == S else S
    q = R.choice(sorted({x[3] for x in ADAPT if x[3] != p and x[0] != o}))
    return item(says(o, f, t) + " Which describes this adaptation?", "a %s adaptation %s" % (t, p), ["a %s adaptation %s" % (ot, p), "a %s adaptation %s" % (t, q), "a %s adaptation %s" % (ot, q)],
                "%s is %s, so it is %s adaptation." % ("A body part" if t == S else "Something the animal does", "a feature of its body" if t == S else "a behaviour", "a structural" if t == S else "a behavioural"))


def g_which():
    t = R.choice([S, B])
    ot = B if t == S else S
    pick = R.choice([x for x in ADAPT if x[2] == t])
    if not once(("wh", pick[0], pick[1])):
        return None
    others = R.sample([x for x in ADAPT if x[2] == ot], 3)
    show = lambda x: (("%s with %s" % (a(x[0]), x[1])) if x[2] == S else ("%s that %s" % (a(x[0]), x[1])))
    return item("Which of these is a %s adaptation?" % t, show(pick), [show(x) for x in others],
                "Structural adaptations are body parts. Behavioural adaptations are things an organism does.")


def g_feat():
    o, f, t, p = R.choice([x for x in ADAPT if x[2] == S])
    if not once(("fe", o, f)):
        return None
    others = R.sample([x[1] for x in ADAPT if x[2] == S and x[0] != o and x[3] != p], 3)
    return item("Which feature helps %s %s?" % (a(o), p), f, others, "The %s has %s." % (o, f))


B1 = bank([
    ("What is an adaptation?", "a feature or behaviour that helps an organism survive in its habitat", ["a change in the weather", "a place where an organism lives", "a group of the same organisms"], "Adaptations help organisms get food, escape predators and survive."),
    ("What is a structural adaptation?", "a body part or body feature that helps an organism survive", ["something an animal learns to do", "a change in the habitat", "the food an animal eats"], "Webbed feet and gills are structural adaptations."),
    ("What is a behavioural adaptation?", "something an organism does that helps it survive", ["a body part such as a beak", "the colour of a plant", "the size of a habitat"], "Hunting at night and migrating are behavioural adaptations."),
    ("Why do mangrove trees have breathing roots?", "The waterlogged mud has very little oxygen, so the roots take in air above the mud.", ["To take in more water from the mud", "To catch insects", "To make food in the dark"], "The roots stick up above the mud and the water at low tide."),
    ("Which of these does not help an animal escape from predators?", "a long, curved beak for reaching nectar", ["a body that looks like a twig", "a hard shell", "curling up when touched"], "A curved beak helps a bird obtain food."),
    ("Why does a stick insect look like a twig?", "So that predators find it hard to see it", ["So that it can make food", "So that it can swim", "So that it can keep warm"], "This is called camouflage."),
    ("Some birds have short, strong beaks and others have long, thin beaks. What does this mostly show?", "Their beaks are adapted to the food they eat.", ["The birds are the same species.", "The beaks help them keep warm.", "The beaks do not do anything."], "Seeds need a strong beak; nectar needs a long, thin beak."),
    ("How does the colour of a green grasshopper help it in a school field?", "It blends in with the grass, so birds find it hard to see.", ["It helps it jump higher.", "It helps it make food.", "It keeps it cool."], "Camouflage is a structural adaptation."),
])
B5 = bank([
    ("Pitcher plants grow in poor, sandy soil in Singapore. Why do they trap insects?", "to get nutrients that are lacking in the soil", ["to get water", "to get sunlight", "to protect their roots"], "They still make their own food by photosynthesis."),
    ("A plant has thick, waxy leaves and grows in a hot, dry place. How do the leaves help it?", "They reduce the loss of water.", ["They take in more carbon dioxide.", "They catch insects.", "They help it float."], "A waxy layer slows down water loss."),
    ("An animal has white fur, small ears and a thick layer of fat. Which habitat is it most likely adapted to?", "a very cold place such as the Arctic", ["a hot desert", "a tropical rainforest", "a pond"], "Small ears and thick fat reduce heat loss."),
    ("Ali saw a mudskipper rolling in the mud at low tide. What is the most likely reason?", "to keep its skin wet so it can take in oxygen through its skin", ["to catch birds", "to make food", "to warm itself"], "Mudskippers can take in some oxygen through their wet skin."),
    ("A fish has a flat body and lives on the sea floor. Its colour matches the sand. How does this help it?", "It can hide from predators and wait for prey.", ["It can swim faster.", "It can breathe air.", "It can make its own food."], "The colour is a form of camouflage."),
    ("Why do some birds fly to Singapore from northern countries each year?", "to escape the cold winter and find food", ["to lay eggs in snow", "to grow new feathers only", "because they are lost"], "Migration is a behavioural adaptation."),
    ("A desert animal comes out only at night. Which is the most likely reason?", "to avoid the heat of the day and lose less water", ["to see better in sunlight", "to find snow", "to make food"], "Many desert animals are active at night."),
])


def body():
    think = ("<p><b>An adaptation is a feature or behaviour that helps an organism survive in its habitat.</b></p>"
             "<ul><li><b>Structural adaptations</b> are body parts: gills, webbed feet, breathing roots, a hard shell.</li>"
             "<li><b>Behavioural adaptations</b> are things the organism does: hunting at night, curling up, migrating.</li>"
             "<li>Adaptations help organisms <b>obtain food, escape predators, breathe, move, keep warm or cool, and reduce water loss</b>.</li>"
             "<li>Mangrove trees have breathing roots because the mud has little oxygen, and prop roots to hold them up in soft mud.</li></ul>")
    ex = [("A pangolin rolls into a ball when attacked. Structural or behavioural?", ["It is something the pangolin does"], "behavioural, to protect itself from predators"),
          ("A sunbird has a long, curved beak. How does this help it?", ["Think about what it eats"], "It reaches nectar deep inside flowers.")]
    mist = ["Calling a behaviour (rolling into a ball, hunting at night) a structural adaptation.",
            "Saying breathing roots take in water. They take in air.",
            "Thinking an animal grows an adaptation because it wants or needs it during its life.",
            "Forgetting that plants have adaptations too, such as floating leaves and spines."]
    return lesson(think, ex, mist)


GA = upto(AD.g_ad, 8)
GH = upto(AD.g_hab, 4)


def main():
    sets = U.sets([
        ("What is an adaptation?", B1 + [(g_purpose, 6), (g_feat, 6)]),
        ("How adaptations help", [(g_purpose, 8), (g_feat, 6), (GA, 4), (GH, 2)]),
        ("Structural and behavioural", [(g_type, 10), (g_which, 8), (g_purpose, 2)]),
        ("Plants and animals in their habitats", [(g_type, 6), (g_which, 4), (GA, 4), (GH, 2), (g_feat, 4)]),
        ("PSLE-style questions", B5 + [(g_type, 6), (g_which, 4), (g_purpose, 3)]),
    ])
    make_sg(6, "adaptations", 8, "Interactions", "Interactions within the environment (Adaptations)",
            "Recognise that adaptations are features or behaviours that help organisms survive in their habitats: to obtain food, escape from predators, breathe, move, "
            "and survive in extreme conditions. Distinguish structural and behavioural adaptations in plants and animals (summary of the MOE Primary Science Syllabus).",
            "Adaptations",
            "Primary 6 Science: Adaptations Worksheets (Structural and Behavioural, PSLE Practice)",
            "Adaptations",
            "Free Primary 6 science worksheets for Singapore pupils on adaptations: structural and behavioural adaptations of mangrove trees, mudskippers, pitcher plants and more. PSLE practice with answers.",
            "Adaptations help organisms survive.",
            "Body parts are structural; actions are behavioural.",
            body(),
            [("What is the difference between structural and behavioural adaptations?", "A structural adaptation is a body part, such as gills. A behavioural adaptation is something the organism does, such as hunting at night."),
             ("How are mangrove trees adapted to their habitat?", "Breathing roots take in air from above the mud, and prop roots support the tree in the soft mud."),
             ("Do plants have adaptations?", "Yes. Water lilies have floating leaves, cacti have spines and pitcher plants trap insects.")],
            sets)


if __name__ == "__main__":
    main()
