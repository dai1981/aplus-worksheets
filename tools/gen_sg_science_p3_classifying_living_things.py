# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Classifying living things (Diversity)
  python tools/gen_sg_science_p3_classifying_living_things.py
Living things are grouped into plants (flowering and non-flowering), animals, fungi and bacteria.
Animals are grouped by their characteristics: mammals, birds, fish, amphibians, reptiles and insects.
Fungi cannot make their own food and reproduce by spores; bacteria can only be seen with a microscope.
Wrong answers come from real mistakes: "a whale is a fish", "a spider is an insect", "a bat is a bird",
"a mushroom is a plant", "all bacteria are harmful", "a fern has flowers".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63302)
R = U.R
P = People(R)
CL = use(U, "gen_uk_science_y6_classifying_living_things", drop=["crustacean", "mollusc", "arachnid", "vertebrate", "micro-organism", "slow worm"])
GR = use(U, "gen_uk_science_y4_grouping_living_things", drop=["crustacean", "mollusc", "arachnid", "vertebrate"])

AN = {"mammal": ["cat", "goat", "otter", "bat", "whale", "dolphin", "cow", "long-tailed macaque", "pangolin", "squirrel", "mousedeer", "elephant", "dugong"],
      "bird": ["mynah", "sparrow", "kingfisher", "chicken", "penguin", "ostrich", "eagle", "owl", "hornbill", "parrot", "duck", "pigeon"],
      "fish": ["guppy", "goldfish", "shark", "seahorse", "catfish", "tilapia", "clownfish", "stingray"],
      "reptile": ["gecko", "monitor lizard", "crocodile", "turtle", "python", "chameleon", "cobra", "tortoise"],
      "amphibian": ["frog", "toad", "salamander"],
      "insect": ["butterfly", "ant", "bee", "mosquito", "grasshopper", "beetle", "dragonfly", "cockroach", "housefly", "moth", "ladybird"]}
PL = {"mammal": "mammals", "bird": "birds", "fish": "fish", "reptile": "reptiles", "amphibian": "amphibians", "insect": "insects"}
GROUPS = list(AN)
FEAT = {"mammal": ["has hair or fur", "feeds its young with milk", "gives birth to young alive"],
        "bird": ["has feathers", "has a beak and two wings", "lays eggs with hard shells"],
        "fish": ["has scales and fins", "breathes through gills all its life", "lives in water and lays eggs"],
        "reptile": ["has dry, scaly skin", "breathes through lungs and lays eggs with leathery shells on land"],
        "amphibian": ["has moist skin without scales", "lays eggs in water and its young breathe through gills"],
        "insect": ["has three body parts and six legs", "has a pair of feelers (antennae) and three body parts"]}
TRICK = {"whale": "A whale breathes with lungs and feeds its young with milk, so it is a mammal, not a fish.",
         "dolphin": "A dolphin breathes air and feeds its young with milk, so it is a mammal.",
         "bat": "A bat flies but has fur and feeds its young with milk, so it is a mammal, not a bird.",
         "penguin": "A penguin cannot fly but has feathers and a beak, so it is a bird.",
         "ostrich": "An ostrich cannot fly but has feathers, so it is a bird.",
         "dugong": "A dugong lives in the sea but feeds its young with milk, so it is a mammal.",
         "seahorse": "A seahorse does not look like most fish, but it has fins and gills, so it is a fish.",
         "turtle": "A turtle lives in water but has dry, scaly skin and lungs, so it is a reptile.",
         "pangolin": "A pangolin has scales, but it also has hair and feeds its young with milk, so it is a mammal."}
NOT_INSECT = [("spider", "eight legs and two body parts"), ("centipede", "many legs"), ("millipede", "many legs"), ("earthworm", "no legs"),
              ("snail", "no legs and a shell"), ("scorpion", "eight legs"), ("crab", "ten legs")]


def an(name):
    return ("an " if name[0] in "aeio" else "a ") + name


def g_group():
    g = R.choice(GROUPS)
    a = R.choice(AN[g])
    if not once(("gr", a)):
        return None
    w = [PL[x] for x in GROUPS if x != g]
    if a in TRICK:
        e = TRICK[a]
    else:
        e = "%s %s, so it belongs to the %s." % (cap1(an(a)), FEAT[g][0], PL[g])
    if a in ("whale", "dolphin", "dugong"):
        w = ["fish"] + [x for x in w if x != "fish"][:2]
    elif a in ("bat",):
        w = ["birds"] + [x for x in w if x != "birds"][:2]
    else:
        w = R.sample(w, 3)
    return item("Which group of animals does %s belong to?" % an(a), PL[g], w, e)


def cap1(s):
    return s[0].upper() + s[1:]


def g_which():
    g = R.choice(GROUPS)
    a = R.choice(AN[g])
    if not once(("wh", g, a)):
        return None
    others = R.sample([x for x in GROUPS if x != g], 3)
    w = [R.choice(AN[x]) for x in others]
    return item("Which of these animals is %s?" % ("an " + g if g[0] in "aeio" else "a " + g), a, w,
                "%s %s." % (cap1(an(a)), FEAT[g][0]))


def g_feat():
    g = R.choice(GROUPS)
    f = R.choice(FEAT[g])
    if not once(("ft", f)):
        return None
    return item("An animal %s. Which group does it most likely belong to?" % f, PL[g], R.sample([PL[x] for x in GROUPS if x != g], 3),
                "An animal that %s belongs to the %s." % (f, PL[g]))


def g_odd():
    g = R.choice(GROUPS)
    same = R.sample(AN[g], 3)
    og = R.choice([x for x in GROUPS if x != g])
    o = R.choice(AN[og])
    if not once(("od", g, og)):
        return None
    c = same + [o]
    R.shuffle(c)
    return item("Which animal does NOT belong to the same group as the others: %s?" % ", ".join(c), o, same,
                "The others are %s. %s belongs to the %s." % (PL[g], cap1(an(o)), PL[og]))


def g_notins():
    a, why = R.choice(NOT_INSECT)
    if not once(("ni", a)):
        return None
    ins = R.sample(AN["insect"], 3)
    return item("Which of these is NOT an insect: %s?" % ", ".join(sorted(ins + [a])), "the " + a, ["the " + x for x in ins],
                "Insects have three body parts and six legs. The %s has %s." % (a, why))


KINGDOMS = {"plants": ["a fern", "a moss", "a hibiscus plant", "a rain tree", "a pandan plant", "a durian tree", "a money plant", "a grass plant"],
            "animals": ["a gecko", "a mynah", "a jellyfish", "a snail", "an earthworm", "a starfish", "an ant", "a frog"],
            "fungi": ["a mushroom", "bread mould", "yeast", "a bracket fungus", "the mould on an orange"],
            "bacteria": ["the bacteria in yoghurt", "the bacteria that cause food poisoning", "the bacteria in our gut", "the bacteria that cause tooth decay"]}


def g_king():
    k = R.choice(list(KINGDOMS))
    a = R.choice(KINGDOMS[k])
    if not once(("kg", a)):
        return None
    w = [x for x in KINGDOMS if x != k]
    e = {"plants": "Plants are green and make their own food.", "animals": "Animals feed on other living things and most can move from place to place.",
         "fungi": "Fungi cannot make their own food. They feed on dead or decaying matter and reproduce by spores.",
         "bacteria": "Bacteria are living things too small to be seen without a microscope."}[k]
    return item("Which group of living things does %s belong to?" % a, k, w, e)


FLOWERING = ["hibiscus", "balsam", "rain tree", "rice plant", "orchid", "sunflower", "durian tree", "mango tree", "lalang grass", "water lily", "bougainvillea"]
NONFLOW = [("bird's nest fern", "spores"), ("staghorn fern", "spores"), ("moss", "spores"), ("maidenhair fern", "spores")]


def g_plant():
    k = R.choice(["f", "n", "n"])
    if k == "f":
        a = R.choice(FLOWERING)
        if not once(("pl", a)):
            return None
        return item("Is a %s a flowering or a non-flowering plant?" % a, "flowering", ["non-flowering", "a fungus", "an animal"],
                    "It makes flowers, which become fruits with seeds.")
    a, how = R.choice(NONFLOW)
    if not once(("pl", a)):
        return None
    return item("How does a %s reproduce?" % a, "by %s" % how, ["by flowers and fruits", "by laying eggs", "by giving birth"],
                "A %s is a non-flowering plant. It reproduces by %s." % (a, how))


def g_key():
    rows = [("1a", "Has feathers", "go to A"), ("1b", "Has no feathers", "go to 2"), ("2a", "Has fur", "go to B"), ("2b", "Has no fur", "go to 3"),
            ("3a", "Has dry, scaly skin", "go to C"), ("3b", "Has moist skin", "go to D")]
    ans = {"A": "mynah", "B": "cat", "C": "gecko", "D": "frog"}
    L = R.choice("ABCD")
    if not once(("ky", L)):
        return None
    tb = table(["Step", "Question", "Then"], [list(r) for r in rows])
    return item("Look at the classification key.<br>%sWhich animal could be %s?" % (tb, L), ans[L], [ans[x] for x in "ABCD" if x != L],
                "Follow the key one step at a time: %s." % {"A": "it has feathers", "B": "no feathers, but it has fur",
                                                       "C": "no feathers, no fur, dry scaly skin", "D": "no feathers, no fur, moist skin"}[L])


B1 = bank([
    ("Into which four groups can living things be classified?", "plants, animals, fungi and bacteria", ["plants, animals, rocks and water", "animals, toys, plants and fungi", "mammals, birds, fish and insects"], "Rocks and water are not living."),
    ("Why do we classify living things?", "to group them by their characteristics so they are easier to study", ["to make them grow faster", "to count how many there are", "to keep them as pets"], "Living things with the same characteristics are put in the same group."),
    ("Which characteristic do all birds have?", "feathers", ["the ability to fly", "living in trees", "eating worms"], "Penguins and ostriches cannot fly, but all birds have feathers."),
    ("Which characteristic do all mammals have?", "hair or fur", ["four legs", "the ability to swim", "a tail"], "Whales and humans also have some hair."),
    ("How do fish breathe?", "through gills", ["through lungs", "through their skin only", "through their fins"], "Gills take in air dissolved in water."),
    ("How many legs does an insect have?", "6", ["4", "8", "10"], "All insects have six legs."),
    ("How many body parts does an insect have?", "3", ["2", "4", "6"], "Head, thorax and abdomen."),
    ("Which group of plants makes flowers?", "flowering plants", ["ferns", "mosses", "fungi"], "Ferns and mosses are non-flowering plants."),
])
B2 = bank([
    ("A spider has eight legs and two body parts. Is it an insect?", "No. Insects have six legs and three body parts.", ["Yes, because it is small.", "Yes, because it has legs.", "No, because it cannot fly."], "A spider is not an insect."),
    ("A bat can fly. Why is it classified as a mammal?", "It has fur and feeds its young with milk.", ["It has feathers.", "It lays eggs.", "It has scales."], "Flying does not make an animal a bird."),
    ("A whale lives in the sea. Why is it NOT a fish?", "It breathes with lungs and feeds its young with milk.", ["It is too big to be a fish.", "It has no tail.", "It cannot swim."], "Whales are mammals."),
    ("A frog lays its eggs in water. Its tadpoles breathe through gills. Which group is it in?", "amphibians", ["fish", "reptiles", "insects"], "Amphibians have moist skin and young that live in water."),
    ("A gecko has dry, scaly skin and lays eggs on land. Which group is it in?", "reptiles", ["amphibians", "mammals", "insects"], "Reptiles have dry, scaly skin."),
    ("Which of these is a mammal that lays eggs?", "a platypus", ["a chicken", "a crocodile", "a frog"], "The platypus is a rare mammal that lays eggs, but it feeds its young with milk."),
    ("Which of these animals can fly but is NOT a bird?", "a butterfly", ["a sparrow", "an eagle", "a pigeon"], "A butterfly is an insect."),
    ("Which of these animals is a fish?", "a seahorse", ["a dolphin", "a turtle", "a dugong"], "A seahorse has fins and gills."),
])
B3 = bank([
    ("Why is a mushroom NOT a plant?", "It is not green and cannot make its own food.", ["It has no leaves, so it is an animal.", "It is too small.", "It grows in the dark, so it is non-living."], "A mushroom is a fungus."),
    ("How do fungi such as mushrooms reproduce?", "by spores", ["by seeds", "by laying eggs", "by flowers"], "Fungi make tiny spores."),
    ("Where do fungi get their food?", "from dead or decaying matter", ["from sunlight", "from rocks", "by making it in green leaves"], "Fungi feed on things such as dead leaves, bread or fruit."),
    ("Which condition helps bread mould to grow fastest?", "a warm, damp place", ["a cold, dry place", "a freezer", "a hot oven"], "Fungi grow well in warm, moist places."),
    ("Why do we need a microscope to see bacteria?", "Bacteria are too small to be seen with our eyes.", ["Bacteria are invisible in the day.", "Bacteria only come out at night.", "Bacteria are made of glass."], "Most bacteria are made of just one tiny cell."),
    ("Which statement about bacteria is correct?", "Some bacteria are useful and some are harmful.", ["All bacteria are harmful.", "All bacteria are useful.", "Bacteria are not living."], "Bacteria in yoghurt are useful; bacteria that cause food poisoning are harmful."),
    ("Which of these is made with the help of yeast?", "bread", ["salt", "sugar", "rice"], "Yeast, a fungus, makes bread dough rise."),
    ("Which of these is made with the help of bacteria?", "yoghurt", ["bread", "salt", "ice"], "Bacteria turn milk into yoghurt."),
    ("Which group of living things can make its own food?", "plants", ["fungi", "animals", "bacteria that cause disease"], "Plants are green and make food using sunlight."),
])
B5 = bank([
    ("Siti found a living thing in a damp forest. It is not green, has no leaves and grows on a dead log. Which group is it most likely in?", "fungi", ["plants", "animals", "bacteria"], "It feeds on the dead log, like a fungus."),
    ("Ravi found a plant with no flowers. Under its leaves are rows of brown dots. What are the dots?", "spore cases", ["seeds", "insect eggs", "fruits"], "Ferns make spores in brown spore cases under their leaves."),
    ("An animal has six legs, three body parts and a pair of wings. Which group is it in?", "insects", ["birds", "mammals", "reptiles"], "Insects have six legs and three body parts. Many also have wings."),
    ("Ahmad left two slices of bread for a week: one in a warm, damp cupboard and one in a fridge. Which slice had more mould?", "the slice in the warm, damp cupboard", ["the slice in the fridge", "both the same", "neither slice"], "Mould grows faster where it is warm and damp."),
    ("Why are the slices of bread in a mould experiment kept the same size and type?", "so that the test is fair", ["so that the mould grows slower", "to make the bread taste better", "so that the bread stays dry"], "Only one thing (the place) should be different."),
    ("A pupil sorted animals into two groups: Group A (mynah, chicken, owl) and Group B (bat, cat, goat). What is the most likely way she sorted them?", "has feathers / has fur", ["can fly / cannot fly", "lives in water / lives on land", "lays eggs / has no legs"], "Bats fly but are in Group B, so flying is not the rule."),
    ("A pupil sorted animals into Group A (frog, toad, salamander) and Group B (gecko, crocodile, cobra). What is the most likely way she sorted them?", "moist skin / dry, scaly skin", ["has legs / has no legs", "lives in water / lives on land", "lays eggs / gives birth"], "Amphibians have moist skin; reptiles have dry, scaly skin."),
    ("Mei Ling put a drop of yoghurt under a microscope and saw tiny rod-shaped living things. What were they most likely?", "bacteria", ["fungi such as mushrooms", "plant cells from fruit", "insect eggs"], "Yoghurt is made with the help of bacteria."),
    ("Which characteristic would best tell a fish from a dolphin?", "gills or lungs", ["living in water", "having a tail", "swimming fast"], "Fish breathe with gills; dolphins breathe air with lungs."),
])


def body():
    think = ("<p><b>Living things are grouped by their characteristics: plants, animals, fungi and bacteria.</b></p>"
             "<ul><li><b>Plants</b>: flowering plants (make flowers and seeds) and non-flowering plants such as ferns and mosses (make spores).</li>"
             "<li><b>Animals</b>: mammals (fur, milk), birds (feathers), fish (scales, gills), amphibians (moist skin), reptiles (dry, scaly skin), insects (6 legs, 3 body parts).</li>"
             "<li><b>Fungi</b>: mushrooms, moulds and yeast. They cannot make food and reproduce by spores.</li>"
             "<li><b>Bacteria</b>: too small to see without a microscope. Some are useful, some are harmful.</li></ul>")
    ex = [("A bat can fly. Is it a bird?", ["Check the body covering: it has fur", "It feeds its young with milk"], "No, it is a mammal."),
          ("A mushroom grows on a dead log. Is it a plant?", ["It is not green", "It feeds on the dead log and makes spores"], "No, it is a fungus.")]
    mist = ["Classifying by where an animal lives or how it moves. A whale is not a fish and a bat is not a bird.",
            "Thinking a spider is an insect. It has eight legs and two body parts.",
            "Thinking mushrooms are plants. They are fungi and cannot make food.",
            "Thinking all bacteria are harmful. Some help to make yoghurt and keep us healthy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Groups of living things", B1 + [(g_king, 5), (g_group, 4), (g_plant, 3)]),
        ("Groups of animals", B2 + [(g_group, 5), (g_which, 5), (g_feat, 2)]),
        ("Plants, fungi and bacteria", B3 + [(g_king, 5), (g_plant, 4), (CL.g_repro, 2)]),
        ("Sorting and keys", [(g_odd, 5), (g_notins, 4), (g_key, 3), (g_feat, 3), (GR.g_carroll, 3), (g_which, 2), (CL.g_char, 2)]),
        ("PSLE-style classification", B5 + [(g_odd, 4), (g_group, 3), (CL.g_char, 2), (g_notins, 2)]),
    ])
    make_sg(3, "classifying-living-things", 2, "Diversity", "Diversity of living and non-living things (Classification of living things)",
            "Classify living things into broad groups: plants (flowering and non-flowering), animals, fungi and bacteria, based on their characteristics. "
            "Observe that fungi do not make their own food and that some bacteria are useful and some are harmful (summary of the MOE Primary Science Syllabus).",
            "Classifying Living Things",
            "Primary 3 Science: Classifying Living Things Worksheets (with Answers)",
            "Classifying living things",
            "Free Primary 3 science worksheets for Singapore pupils on classifying living things: plants, animals, fungi and bacteria, mammals, birds, fish, amphibians, reptiles and insects. 100 questions with answers.",
            "Group living things by what they have in common.",
            "Plants, animals, fungi and bacteria; then mammals, birds, fish and more.",
            body(),
            [("Is a mushroom a plant?", "No. A mushroom is a fungus. It is not green, cannot make its own food and reproduces by spores."),
             ("Why is a whale a mammal and not a fish?", "A whale breathes with lungs, has a little hair and feeds its young with milk. Fish breathe through gills."),
             ("Are all bacteria harmful?", "No. Some bacteria help us make yoghurt and live in our gut, while others cause diseases such as food poisoning.")],
            sets)


if __name__ == "__main__":
    main()
