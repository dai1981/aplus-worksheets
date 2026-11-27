# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Living and non-living things (Diversity)
  python tools/gen_sg_science_p3_living_and_non_living_things.py
Living things need air, food and water, grow, respond to changes and reproduce.
Non-living things do not show all of these. Things that move (a car, a cloud, a fan) are not living just because they move.
UK Year 2 sorting questions are reused with Singapore names (sg_sci.use); Singapore examples and
PSLE-style observation questions (seeds, mealworms, mimosa) are written here.
Wrong answers come from real mistakes: "it moves so it is alive", "a seed is not alive", "plants do not need air".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, People, once, use

U = Unit(63301)
R = U.R
P = People(R)
LD = use(U, "gen_uk_science_y2_living_dead_and_never_alive", drop=["dead", "never alive", "winter", "snow"])

LIVING = ["a hibiscus plant", "a mynah", "a guppy", "a mushroom", "a mango tree", "a gecko", "a mosquito", "a kitten", "a fern", "a durian tree",
          "a monitor lizard", "a sparrow", "a seed", "a snail", "an earthworm", "a moss", "a bread mould", "a pandan plant", "an otter", "a cockroach"]
NONLIVING = ["a rock", "a plastic bottle", "a toy robot", "a ceiling fan", "a bicycle", "a cloud", "a candle flame", "a stone", "a metal spoon",
             "a battery-powered toy dog", "an MRT train", "a kite", "a rubber ball", "a remote-control car", "a river", "a wooden chair",
             "a robot vacuum cleaner", "a balloon", "a television", "a toy windmill"]
MOVES = {"a ceiling fan", "a bicycle", "a cloud", "a candle flame", "a battery-powered toy dog", "an MRT train", "a kite", "a remote-control car",
         "a river", "a robot vacuum cleaner", "a balloon", "a toy windmill", "a toy robot", "a rubber ball"}
STILL = {"a hibiscus plant", "a mushroom", "a mango tree", "a fern", "a durian tree", "a seed", "a moss", "a bread mould", "a pandan plant"}
SHOWS = [("A puppy becomes an adult dog.", "growth"), ("A rain tree seedling becomes a big tree.", "growth"), ("A baby's feet get longer each year.", "growth"),
         ("A caterpillar becomes larger after eating leaves.", "growth"),
         ("A hen lays eggs that hatch into chicks.", "reproduction"), ("A cat gives birth to kittens.", "reproduction"),
         ("A fern makes spores that grow into new ferns.", "reproduction"), ("A balsam plant makes seeds that grow into new plants.", "reproduction"),
         ("A snail pulls into its shell when it is touched.", "response to changes"), ("The leaves of a mimosa plant fold when touched.", "response to changes"),
         ("A pupil blinks when a bright light shines in her eyes.", "response to changes"), ("A plant on a windowsill bends towards the light.", "response to changes"),
         ("A cockroach runs away when the light is switched on.", "response to changes"),
         ("A balsam plant wilts when it is not watered.", "the need for water"), ("A fish dies in a tank of water that has had the air removed.", "the need for air"),
         ("A goat eats grass every day.", "the need for food"), ("A plant in a sealed jar with no air dies.", "the need for air"),
         ("A dog drinks from its bowl after a run.", "the need for water"), ("A mosquito sucks blood to get food.", "the need for food")]
CHARS = [("needs air", "need air"), ("needs food", "need food"), ("needs water", "need water"), ("grows", "grow"),
         ("responds to changes", "respond to changes"), ("reproduces", "reproduce")]


def g_odd():
    k = R.choice(["living", "nonliving"])
    if k == "living":
        a = R.choice(LIVING)
        w = R.sample(NONLIVING, 3)
        q = "Which one of these is a living thing?"
    else:
        a = R.choice(NONLIVING)
        w = R.sample(LIVING, 3)
        q = "Which one of these is a non-living thing?"
    if not once(("od", k, a)):
        return None
    return item(q, a, w, "%s %s." % (a[0].upper() + a[1:], "needs air, food and water, grows and reproduces" if k == "living" else "does not grow or reproduce, even if it moves"))


def g_is():
    a = R.choice(LIVING + NONLIVING)
    if not once(("is", a)):
        return None
    yes, no = "Yes. It needs air, food and water, grows and reproduces.", "No. It does not grow or reproduce."
    wy, wn = "Yes, because it moves.", "No, because it does not move."
    if a in LIVING:
        return item("Is %s a living thing?" % a, yes, [no, wy, wn],
                    "%s is living%s." % (a[0].upper() + a[1:], ", even though it does not move from place to place" if a in STILL else ""))
    return item("Is %s a living thing?" % a, no, [yes, wy, wn],
                "%s is non-living%s." % (a[0].upper() + a[1:], ", even though it moves" if a in MOVES else ""))


def g_show():
    sc, a = R.choice(SHOWS)
    if not once(("sh", sc)):
        return None
    w = [x for x in ["growth", "reproduction", "response to changes", "the need for water", "the need for air", "the need for food"] if x != a]
    if a.startswith("the need"):
        w = [x for x in w if not x.startswith("the need")] + [x for x in w if x.startswith("the need")][:1]
    return item("%s Which characteristic of living things does this show?" % sc, a, R.sample(w, 3),
                "This shows %s." % a)


def g_char():
    c, verb = R.choice(CHARS)
    if not once(("ch", c)):
        return None
    w = R.sample(["moves from place to place", "has legs", "makes a sound", "is green", "has a heart", "breathes through a nose", "is bigger than a person"], 3)
    return item("Which of these is true of ALL living things?", c, w,
                "All living things need air, food and water, grow, respond to changes and reproduce. Not all of them %s." % w[0])


def g_notchar():
    c, verb = R.choice(CHARS)
    thing, why = R.choice([("A ceiling fan", "it moves"), ("A toy robot", "it makes sounds"), ("A fire", "it gets bigger"), ("A car", "it moves and uses fuel"), ("A cloud", "it moves and changes shape")])
    if not once(("nc", thing)):
        return None
    return item("%s is a non-living thing, although %s. Which of these can it NOT do?" % (thing, why), "reproduce",
                ["move", "change its shape or size", "be seen"], "Only living things can reproduce (make young or new plants).")


B1 = bank([
    ("What do living things need to stay alive?", "air, food and water", ["air, sunlight and soil", "food and toys", "water and rocks"], "All living things need air, food and water."),
    ("Which of these shows that a mango tree grows?", "It becomes taller and thicker over the years.", ["It sways in the wind.", "Its leaves are green.", "It has a smell."], "Growing means getting bigger over time."),
    ("Which of these shows that a cat responds to changes?", "It runs away when a dog barks.", ["It has four legs.", "It has fur.", "It is grey."], "Responding means reacting to something around it."),
    ("Which of these shows that a chicken reproduces?", "It lays eggs that hatch into chicks.", ["It walks around the farm.", "It eats grains.", "It has feathers."], "Reproducing means making young."),
    ("How does a plant reproduce?", "It makes seeds or spores that grow into new plants.", ["It moves to a new place.", "It eats food from the soil.", "It cannot reproduce."], "Flowering plants make seeds; ferns and mosses make spores."),
    ("Which living thing does NOT move from place to place?", "a rain tree", ["a dog", "a snail", "a fish"], "Plants are living but do not move from place to place."),
    ("Is a mushroom a living thing?", "Yes. It needs food, water and air, grows and reproduces.", ["No, because it does not move.", "No, because it is not green.", "No, because it has no leaves."], "A mushroom is a fungus. Fungi are living things."),
    ("Is a seed a living thing?", "Yes. It can grow into a new plant when it gets water, air and warmth.", ["No, it looks like a stone.", "No, it does not move.", "No, only the plant is living."], "A seed is alive but resting until it germinates."),
])
B2 = bank([
    ("Why is a fire NOT a living thing, even though it grows bigger?", "It does not reproduce or respond like a living thing.", ["It is too hot.", "It is not green.", "It has no legs."], "A thing must show all the characteristics of living things."),
    ("A toy dog walks and barks. Why is it NOT a living thing?", "It does not need food, grow or reproduce.", ["It is too small.", "It is made in a factory, so it is alive.", "It moves, so it is living."], "Moving and making sounds do not make something alive."),
    ("Which of these is a living thing that cannot move from place to place?", "a pandan plant", ["a cat", "a bicycle", "a cloud"], "Plants are living even though they stay in one place."),
    ("When you touch a mimosa (touch-me-not) plant, its leaves fold up. What does this show?", "Plants respond to changes.", ["Plants need water.", "Plants reproduce.", "Plants are non-living."], "The leaves react to touch."),
    ("A sunflower turns towards the light. Which characteristic of living things does this show?", "responding to changes", ["reproducing", "needing water", "growing bigger"], "The plant reacts to the light."),
    ("Do plants need air?", "Yes. All living things, including plants, need air.", ["No, only animals need air.", "No, plants only need soil.", "Only plants that have flowers need air."], "Plants need air, just like animals."),
    ("A baby grows into an adult. Which characteristic of living things does this show?", "growth", ["response", "reproduction", "needing air"], "Getting bigger and older is growth."),
    ("Which of these is a non-living thing?", "a stone", ["a fern", "a beetle", "a mushroom"], "A stone does not need food or reproduce."),
])
B3 = bank([
    ("A goldfish was put in a tank of boiled and cooled water with no air in it. What would happen?", "It would die because it cannot get the air it needs.", ["It would grow faster.", "It would be fine because it is in water.", "It would turn into a plant."], "Fish need the air dissolved in water."),
    ("Siti kept a potted plant in a dark cupboard and gave it no water for 3 weeks. What most likely happened?", "The plant died.", ["The plant grew taller and greener.", "The plant made more flowers.", "Nothing happened."], "Living things need water to survive."),
    ("Which of these living things lays eggs?", "a chicken", ["a dog", "a cow", "a cat"], "Chickens reproduce by laying eggs; dogs, cows and cats give birth to young."),
    ("Which of these living things gives birth to young alive?", "a goat", ["a chicken", "a frog", "a butterfly"], "Most mammals give birth to live young."),
    ("Which of these shows that a plant needs water?", "A plant that is not watered wilts.", ["A plant is green.", "A plant has roots.", "A plant grows in a pot."], "Without water, a plant wilts and may die."),
    ("Why is a wooden table non-living now?", "It was once part of a tree but no longer grows or reproduces.", ["It was never part of a living thing.", "It is still living.", "It is made of plastic."], "The wood came from a living tree, but the table is not alive."),
    ("Which of these is NOT a characteristic of all living things?", "They can talk.", ["They need air.", "They grow.", "They reproduce."], "Most living things cannot talk."),
])
B5 = bank([
    ("Ravi put green bean seeds on wet cotton wool. After 3 days, roots and shoots appeared. What does this show?", "The seeds are living things that grow.", ["The cotton wool is living.", "The seeds were never alive.", "The water turned into plants."], "The seeds grew into seedlings, so they are living."),
    ("Mei Ling put some mealworms in a box with one dark end and one bright end. Most mealworms moved to the dark end. What does this show?", "Mealworms respond to light.", ["Mealworms need water.", "Mealworms reproduce in the dark.", "Mealworms are non-living."], "The mealworms reacted to the light by moving away."),
    ("Ahmad left a slice of bread in a warm, damp place. After a week, mould grew on it. Which of these is living?", "the mould", ["the bread", "the plastic bag", "the plate"], "Mould is a fungus. It grows and reproduces."),
    ("A pupil sealed a small plant in an airtight jar and another in an open jar. Which plant is likely to stay healthy longer?", "the plant in the open jar", ["the plant in the sealed jar", "both the same", "neither"], "Plants need air to stay alive."),
    ("Two identical guppies were kept in tanks. One was fed; one was not fed for a long time. What does this experiment test?", "whether guppies need food to stay alive", ["whether guppies need light", "whether guppies need water", "whether guppies can talk"], "Only the food was different."),
    ("A pupil watered one balsam plant every day and gave another no water. Everything else was the same. What is she finding out?", "whether plants need water to survive", ["whether plants need soil", "whether plants need air", "whether plants need music"], "Only the water was different."),
    ("Which observation would show that a snail is living?", "It grows bigger over weeks.", ["It has a hard shell.", "It is brown.", "It is found in the garden."], "Growth is a characteristic of living things."),
    ("A pupil put a cardboard box with a hole over a potted plant. After a week, the plant had bent towards the hole. Why?", "The plant responds to light by growing towards it.", ["The plant needs the box.", "The plant moved to find water.", "The box pushed the plant."], "Plants respond to light."),
    ("Jun Jie says a cloud is living because it moves and gets bigger. What is the best reply?", "A cloud does not need food, reproduce or respond like a living thing, so it is non-living.", ["He is right.", "A cloud is living only when it rains.", "A cloud is a plant."], "Moving and changing size are not enough."),
])


def body():
    think = ("<p><b>Living things share some characteristics.</b></p>"
             "<ul><li>They need <b>air, food and water</b>.</li><li>They <b>grow</b>.</li>"
             "<li>They <b>respond to changes</b> around them.</li><li>They <b>reproduce</b> (make young or new plants).</li></ul>"
             "<p>Non-living things do not show all of these, even if they move or make sounds.</p>")
    ex = [("A toy car moves when it is pushed. Is it living?", ["It does not need food or water", "It does not grow or reproduce"], "No, it is non-living."),
          ("A seed is put on wet cotton wool and grows a root. Is it living?", ["It grows", "It can become a new plant"], "Yes, a seed is living.")]
    mist = ["Thinking anything that moves is living. A fan, a cloud and a car move but are non-living.",
            "Thinking plants are non-living because they do not walk. Plants grow, respond and reproduce.",
            "Thinking seeds are dead. A seed is a living thing waiting to grow.",
            "Forgetting that plants also need air."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Living or non-living?", B1 + [(g_is, 6), (g_odd, 6), (LD.g_pick, 3)]),
        ("Characteristics of living things", B2 + [(g_char, 5), (g_show, 6), (LD.g_proc, 4), (g_is, 3)]),
        ("Thinking about tricky cases", B3 + [(g_notchar, 4), (LD.g_trick, 3), (g_is, 5), (g_show, 4), (LD.g_proc, 3)]),
        ("Mixed practice", LD.B1 + [(g_odd, 6), (g_show, 5), (g_is, 5), (LD.g_pick, 4)]),
        ("PSLE-style observations", B5 + LD.B5 + [(LD.g_proc, 3), (g_show, 4), (g_is, 3)]),
    ])
    make_sg(3, "living-and-non-living-things", 1, "Diversity", "Diversity of living and non-living things (General characteristics)",
            "Identify the characteristics of living things: they need air, food and water, grow, respond to changes and reproduce. "
            "Classify things as living and non-living by observing their characteristics (summary of the MOE Primary Science Syllabus).",
            "Living and Non-living Things",
            "Primary 3 Science: Living and Non-living Things Worksheets (with Answers)",
            "Living and non-living",
            "Free Primary 3 science worksheets for Singapore pupils on living and non-living things: needing air, food and water, growth, response and reproduction. 100 questions with answers.",
            "Living things need air, food and water.",
            "They also grow, respond to changes and reproduce.",
            body(),
            [("How do I know if something is living?", "Check whether it needs air, food and water, grows, responds to changes and reproduces. A living thing does all of these."),
             ("Is a plant living if it does not move?", "Yes. Plants grow, respond to light and touch, and reproduce with seeds or spores, even though they do not move from place to place."),
             ("Why is a fire not living?", "A fire can grow and needs air, but it does not reproduce or respond to changes like a living thing.")],
            sets)


if __name__ == "__main__":
    main()
