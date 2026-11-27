# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U01: behaviours of living things that help them survive in their habitat.
  python tools/gen_au_science_y5_behavioural_adaptations.py
Australian animals: nocturnal bilbies, burrowing frogs, kangaroos licking their forearms, migrating humpback whales,
hibernating mountain pygmy possums, swooping magpies, frill-necked lizards, bowerbirds ... Southern-hemisphere seasons.
Wrong answers come from real mistakes: mixing up behaviours and body parts, "animals choose to change their bodies",
getting the reason for a behaviour back to front (whales migrate north to warm water in winter, not to cold water).
"""
from au_sci import AU, seed_of, make_au, tq, pool

YEAR, SORT = 5, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

g_sb = src("gen_au_science_y5_structural_adaptations", "g_sb")
uk_ad = src("gen_uk_science_y6_adaptation_and_evolution", "g_ad")

BEH = [("bilby", "comes out only at night (it is nocturnal)", "to avoid the heat of the desert day"),
       ("water-holding frog", "burrows underground and wraps itself in a skin cocoon in the dry season", "to stop drying out until rain comes"),
       ("red kangaroo", "licks its forearms on hot days", "to cool down as the saliva evaporates"),
       ("red kangaroo", "rests in the shade in the middle of the day", "to stay cool and save water"),
       ("humpback whale", "swims north along the east coast in winter", "to give birth in warm waters"),
       ("mountain pygmy possum", "hibernates under the snow in winter", "to save energy when food is scarce"),
       ("echidna", "curls into a spiky ball", "to protect its soft belly from predators"),
       ("frill-necked lizard", "opens its frill and hisses", "to scare off predators"),
       ("blue-tongued lizard", "opens its mouth and shows its blue tongue", "to frighten predators"),
       ("magpie", "swoops at people near its nest in spring", "to protect its eggs and chicks"),
       ("satin bowerbird", "decorates its bower with blue objects", "to attract a mate"),
       ("superb lyrebird", "copies the calls of other birds", "to attract a mate"),
       ("eastern grey kangaroo", "lives in a group called a mob", "so more eyes can watch for danger"),
       ("sea turtle", "returns to the beach where it hatched", "to lay its eggs on a safe, sandy beach"),
       ("short-tailed shearwater", "flies across the Pacific Ocean each year", "to find food when it is winter in Australia"),
       ("wombat", "digs a burrow and stays in it during the day", "to stay cool and safe"),
       ("flying fox", "fans and licks its wings on hot days", "to cool down"),
       ("possum", "sleeps in a tree hollow during the day and feeds at night", "to stay safe from daytime predators"),
       ("platypus", "closes its eyes and ears when it dives", "to keep water out while it finds prey with its bill"),
       ("bogong moth", "flies to cool alpine caves in summer", "to escape the heat of the plains")]


def art(x):
    return ("an " if x[0] in "aeiou" else "a ") + x


def g_why():
    o, b, h = R.choice(BEH)
    others = sorted({x[2] for x in BEH if x[2] != h})
    return tq("%s %s. Why does it do this?" % (art(o).capitalize(), b), h, R.sample(others, 3),
              "This is a behavioural adaptation: something the %s does that helps it survive." % o)


def g_who():
    o, b, h = R.choice(BEH)
    w = sorted({x[0] for x in BEH if x[0] != o})
    return tq("Which animal %s %s?" % (b, h), art(o), [art(x) for x in R.sample(w, 3)], "The %s %s." % (o, b))


def g_what():
    o, b, h = R.choice(BEH)
    w = sorted({x[1] for x in BEH if x[0] != o and x[2] != h})
    if not h.startswith("to "):
        return None
    return tq("Which behaviour helps %s %s?" % (art(o), h[3:]), b, R.sample(w, 3),
              "The %s %s." % (o, b))


NOCT = [("sugar glider", "night"), ("bilby", "night"), ("possum", "night"), ("wombat", "night"), ("powerful owl", "night"), ("flying fox", "night"),
        ("kookaburra", "day"), ("magpie", "day"), ("emu", "day"), ("koala", "night"), ("frill-necked lizard", "day"), ("honeyeater", "day")]


def g_noct():
    o, t = R.choice(NOCT)
    a = "nocturnal (active at night)" if t == "night" else "diurnal (active during the day)"
    w = ["diurnal (active during the day)" if t == "night" else "nocturnal (active at night)", "hibernating all year", "active only in the rain"]
    return tq("Is %s nocturnal or diurnal?" % art(o), a, w, "Nocturnal animals are active at night; diurnal animals are active during the day.")


POOL1 = pool(R, [
    ("What is a behavioural adaptation?", "something a living thing does that helps it survive", ["a body part that helps it survive", "a change in the weather", "the place where it lives"], "Examples: burrowing, migrating, coming out at night."),
    ("Which of these is a behavioural adaptation?", "a bilby coming out at night", ["a bilby's large ears", "a koala's two thumbs", "an echidna's spines"], "Coming out at night is something the bilby does."),
    ("Which of these is a structural adaptation?", "a pelican's throat pouch", ["a whale migrating north", "a magpie swooping", "a wombat staying in its burrow"], "A throat pouch is a body part."),
    ("Why do many desert animals rest in burrows during the day?", "Burrows are cooler and more humid than the surface.", ["Burrows are hotter than the surface.", "There is more food in burrows.", "They cannot see in daylight."], "Underground temperatures change much less."),
    ("Why do some animals migrate?", "to find food, warmer weather or a safe place to breed", ["because they are lost", "to grow new body parts", "to change colour"], "Migration is a long journey made each year."),
    ("What does it mean when an animal hibernates?", "It goes into a deep sleep through the cold months to save energy.", ["It moves to a new country.", "It changes its fur colour.", "It eats more food in winter."], "Its heart rate and body temperature drop."),
    ("Why do magpies swoop in spring?", "They are protecting their eggs and chicks.", ["They are migrating.", "They are looking for water.", "They are hibernating."], "In Australia, spring is September to November."),
    ("Why do kangaroos live in mobs?", "More eyes and ears can spot danger.", ["to keep the grass short", "to dig deeper burrows", "to hibernate together"], "Group living is a behavioural adaptation."),
    ("When do humpback whales swim north along the east coast of Australia?", "in late autumn and winter", ["in summer", "only at night", "in spring only"], "They travel from cold Antarctic waters to warm waters to give birth."),
    ("How does a frill-necked lizard scare away a predator?", "It opens its frill, opens its mouth wide and hisses.", ["It changes colour to bright blue.", "It hibernates.", "It digs a deep burrow."], "Looking bigger can frighten predators."),
    ("Some plants close their flowers at night. Why might this help?", "It protects the pollen from cold and dew.", ["It helps the plant grow roots.", "It makes the plant taller.", "It stops the sun reaching the leaves."], "Plants can respond to their surroundings too."),
    ("A plant's leaves turn to face the sun. How does this help?", "The leaves get more light to make food.", ["The leaves lose more water.", "The plant stops growing.", "The roots get more air."], "Plants use light to make their food."),
])
POOL5 = pool(R, [
    ("Jack says, 'Wombats have strong claws, so digging is a structural adaptation.' What is wrong?", "Claws are structural; digging is the behaviour that uses them.", ["Wombats do not dig.", "Claws are a behaviour.", "Nothing is wrong."], "Body parts and behaviours often work together."),
    ("Ruby counts bilby tracks at 9 am and at 9 pm for a week. She finds many more at night. What can she conclude?", "Bilbies are mostly active at night.", ["Bilbies are mostly active during the day.", "There are no bilbies nearby.", "Bilbies hibernate in summer."], "The data shows when the animals move about."),
    ("A scientist puts a thermometer on the sand and another inside a burrow at 2 pm. Which result is most likely?", "Sand 55 °C, burrow 28 °C", ["Sand 28 °C, burrow 55 °C", "Sand 30 °C, burrow 30 °C", "Sand 10 °C, burrow 40 °C"], "Burrows stay much cooler than the surface on a hot day."),
    ("Mia wants to test whether slaters (woodlice) prefer dark or light places. What should she keep the same?", "the number of slaters, the dampness and the temperature", ["the amount of light", "nothing", "only the size of the box"], "Change only the light; keep everything else the same."),
    ("In Mia's test, 18 of 20 slaters moved to the dark side. What does this suggest?", "Slaters prefer dark places.", ["Slaters prefer light places.", "Slaters cannot move.", "The test shows nothing."], "Dark places are often damp and safe from predators."),
    ("Whales are seen off Hervey Bay mostly from July to October. Which explanation fits best?", "They migrate north to warm water in winter and spring.", ["They live there all year.", "They migrate south to cold water in winter.", "They are lost."], "Use the months: this is Australian winter and spring."),
    ("Why should a fair test of animal behaviour be repeated many times?", "to make sure the result was not just chance", ["to make the animals tired", "to change the variable each time", "repeating is never useful"], "Repeats make results more reliable."),
    ("Which question could be answered by observing animals at a waterhole?", "At what time of day do kangaroos drink?", ["Why do kangaroos have tails?", "How old is the oldest kangaroo?", "What colour is a kangaroo's heart?"], "Choose questions you can test by watching."),
])


def main():
    sets = U.sets([
        ("What is a behavioural adaptation?", [(POOL1, 7), (g_sb, 6), (g_why, 7)]),
        ("Why animals do what they do", [(g_why, 6), (g_who, 8), (POOL1, 2), (g_noct, 4)]),
        ("Night, day and seasons", [(g_noct, 6), (g_what, 7), (POOL1, 2), (g_who, 5)]),
        ("Body parts and behaviours", [(g_sb, 6), (uk_ad, 8), (g_what, 4), (g_why, 2)]),
        ("Investigations and explanations", [(POOL5, 7), (g_who, 5), (g_what, 3), (g_why, 3), (uk_ad, 2)]),
    ])
    make_au(YEAR, "behavioural-adaptations", SORT, "AC9S5U01", "Biological sciences",
            "Examine how particular structural features and behaviours of living things enable their survival in specific habitats "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Behavioural Adaptations", "Behavioural adaptations",
            "Free Year 5 science worksheets on behavioural adaptations: why bilbies come out at night, whales migrate, possums hibernate and "
            "magpies swoop. 100 questions with answers.",
            "Behaviours help living things survive.", "A behavioural adaptation is something a living thing does.",
            "<p><b>A behavioural adaptation is an action that helps a living thing survive.</b></p><ul>"
            "<li>Ask what the problem is: heat, cold, little food, predators or finding a mate.</li>"
            "<li>Then link the behaviour: hiding in a burrow by day, migrating to warm water, hibernating, living in a mob, showing a frill.</li>"
            "<li>Body parts (claws, ears, spines) are structural adaptations. They often work together with behaviours.</li></ul>",
            [("A kangaroo licks its forearms on a hot day. Why?", ["the saliva evaporates", "evaporation takes away heat"], "to cool down"),
             ("Humpback whales swim north in winter. Why?", ["the water further north is warmer", "the calves are born there"], "to give birth in warm water")],
            ["Calling a body part a behaviour (claws are structural; digging is the behaviour).",
             "Forgetting that Australian seasons are opposite to the northern hemisphere (winter is June to August).",
             "Thinking animals change their bodies because they want to."],
            [("What is the difference between nocturnal and diurnal?", "Nocturnal animals, such as bilbies and possums, are active at night. Diurnal animals, such as kookaburras and emus, are active during the day."),
             ("Do plants have behavioural adaptations?", "Yes. Some plants turn their leaves towards the light or close their flowers at night. These are responses to their surroundings."),
             ("Why do humpback whales migrate?", "They feed in cold Antarctic waters in summer, then swim north along the Australian coast in winter to give birth in warmer water.")],
            sets)


if __name__ == "__main__":
    main()
