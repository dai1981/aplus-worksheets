# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Energy in Food Comes from the Sun (5-PS3-1)
  python tools/gen_us_science_g5_energy_in_food.py
Plants capture energy from sunlight and store it in the food they make (sugar). Animals get that
energy by eating plants or other animals, and use it for body repair, growth, motion and to keep warm.
Tracing any food back along a food chain leads to a plant, and the plant's energy came from the sun.
Wrong answers come from real mistakes: "plants get energy from the soil", "energy comes from water",
"meat-eaters do not depend on the sun", "food gives matter but not energy".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, text, arrow, rect, table, People, INK
import sci_foodweb as FW

U = Unit(50107)
R = U.R
P = People(R)
USES = ["body repair", "growth", "motion", "keeping warm"]
ACTS = [("A rabbit runs away from a fox.", "motion"), ("A kitten gets bigger and heavier each week.", "growth"), ("A scrape on Leo's knee heals.", "body repair"),
        ("A penguin keeps its body warm in icy water.", "keeping warm"), ("A deer grows new antlers.", "growth"), ("A bird flaps its wings to fly south.", "motion"),
        ("A lizard's lost tail grows back.", "body repair"), ("A dog shivers on a cold night to stay warm.", "keeping warm"),
        ("A child grows 5 centimeters taller in a year.", "growth"), ("A horse gallops across a field.", "motion"), ("A broken bone mends.", "body repair"),
        ("A polar bear stays warm in the Arctic.", "keeping warm"), ("A tadpole grows legs.", "growth"), ("A cheetah sprints after prey.", "motion")]
FOODS = [("a slice of bread", "wheat"), ("rice", "rice plants"), ("a hamburger", "grass eaten by a cow"), ("milk", "grass eaten by a cow"), ("an egg", "grain eaten by a hen"),
         ("peanut butter", "peanut plants"), ("a glass of orange juice", "orange trees"), ("a cheese stick", "grass eaten by a cow"), ("popcorn", "corn plants"),
         ("a chicken sandwich", "grain eaten by a chicken"), ("a fish stick", "algae eaten by small animals that fish eat"), ("honey", "flowers visited by bees"),
         ("maple syrup", "maple trees"), ("a strawberry", "strawberry plants")]


def cap(s):
    return s[0].upper() + s[1:]


def sun_chain(ch):
    """sun -> chain picture."""
    W = 112 * (len(ch) + 1)
    s = []
    items = ["sun"] + ch
    for i, x in enumerate(items):
        cx = 56 + i * 112
        tw = 7.0 * len(x) + 14
        col = "#ffe58a" if x == "sun" else ("#e3f1df" if x in FW.PLANTS else "#fdf0dc")
        s.append(rect(cx - tw / 2, 12, tw, 26, col, INK, 1.5, 6) + text(cx, 30, x, 13))
        if i:
            px = 56 + (i - 1) * 112 + (7.0 * len(items[i - 1]) + 14) / 2 + 3
            s.append(arrow(px, 25, cx - tw / 2 - 3, 25, "#555555", 2, 8))
    return svg_wrap(W, 50, "".join(s), "energy chain from the sun").replace("<svg ", "<svg data-pf='lg' ", 1)


# ------------------------------------------------------------ makers
def g_use():
    s, u = R.choice(ACTS)
    return item(s + " What is the energy from its food being used for?" if "Leo" not in s and "child" not in s else s + " What is energy from food being used for?",
                u, [x for x in USES if x != u], "Animals use energy from food for body repair, growth, motion and keeping warm. Here it is " + u + ".")


def g_food_source():
    f, src = R.choice(FOODS)
    p = P.next()
    return item("%s has %s for lunch. The energy in it can be traced back to %s. Where did that energy come from first?" % (p[0], f, src),
                "the sun", ["the soil", "the water the plants drank", "the refrigerator"],
                "The plants used sunlight to make their food. The energy moved along to %s." % f)


def g_path():
    w = R.choice(sorted(FW.WEBS))
    ch = R.choice([c for c in FW.chains(w) if 3 <= len(c) <= 4])
    good = "sun → " + " → ".join(ch)
    rev = " → ".join(reversed(ch)) + " → sun"
    nop = "sun → " + " → ".join(ch[1:])
    soil = "soil → " + " → ".join(ch)
    return item("Which shows how energy moves to the %s in the %s?" % (ch[-1], FW.WEBS[w]["name"]), good, [rev, nop, soil],
                "Energy starts in sunlight, is captured by the producer (%s) and passes to each consumer that eats." % ch[0])


def g_chain_pic():
    w = R.choice(sorted(FW.WEBS))
    ch = R.choice([c for c in FW.chains(w) if 3 <= len(c) <= 4])
    k = R.choice(["first", "producer", "plant"])
    q = fig(sun_chain(ch))
    if k == "first":
        return item(q + "In this model, which organism first captures the sun's energy?", ch[0], ch[1:] + ["the sun itself"] if len(ch) == 3 else ch[1:4],
                    "The %s is a producer. It captures sunlight and stores the energy in its food." % ch[0])
    x = ch[-1]
    return item(q + "The %s does not eat plants directly. Does its energy still come from the sun?" % x if FW.kind(w, x) == "carnivore" else
                q + "Where did the energy in the %s's body come from first?" % x,
                "Yes. The %s captured the sun's energy, and it passed along the food chain." % ch[0] if FW.kind(w, x) == "carnivore" else "the sun",
                ["No, meat-eaters get energy only from water.", "No, it makes its own energy.", "No, its energy comes from the soil."] if FW.kind(w, x) == "carnivore" else ["the %s" % ch[0] + "'s roots", "the water", "the soil"],
                "Follow the arrows back: %s ← %s ← sun." % (x, " ← ".join(reversed(ch[:-1]))))


def g_calories():
    a = R.choice([("an apple", 95), ("a banana", 105), ("a slice of bread", 80), ("a cup of milk", 120), ("an egg", 75), ("a granola bar", 190), ("a cup of rice", 205), ("a carrot", 25)])
    b = R.choice([("an apple", 95), ("a banana", 105), ("a slice of bread", 80), ("a cup of milk", 120), ("an egg", 75), ("a granola bar", 190), ("a cup of rice", 205), ("a carrot", 25)])
    if a[1] == b[1]:
        return None
    hi = a if a[1] > b[1] else b
    lo = b if hi is a else a
    d = hi[1] - lo[1]
    return item(table(["Food", "Energy (about, in Calories)"], [[cap(a[0]), str(a[1])], [cap(b[0]), str(b[1])]])
                + "How many more Calories of energy are in %s than in %s?" % (hi[0], lo[0]),
                str(d), [str(hi[1] + lo[1]), str(hi[1]), str(abs(d - 10) if d != 10 else d + 20)],
                "%d − %d = %d Calories. Calories measure the energy stored in food." % (hi[1], lo[1], d))


B1 = bank([
    ("Where does almost all the energy in food come from?", "the sun", ["the soil", "water", "the air"],
     "Plants capture sunlight and store its energy in food. Animals get energy from plants or from animals that ate plants."),
    ("How do plants get the energy they need?", "They capture energy from sunlight to make their own food.", ["They eat insects.", "They take energy from the soil.", "They do not need energy."],
     "Plants use sunlight, carbon dioxide and water to make sugar. The energy is stored in the sugar."),
    ("In what form do plants store the sun's energy?", "in the food they make (sugars)", ["in the soil around them", "in rainwater", "in their shadows"],
     "The sugar and starch in leaves, roots, fruits and seeds hold stored energy."),
    ("Which four things do animals use energy from food for?", "body repair, growth, motion and keeping warm", ["making sunlight, growth, sleep and color", "only motion", "only growth"],
     "These are the four uses named in the standard."),
    ("Why do animals need to eat?", "Food gives them energy and materials to live and grow.", ["Food gives them sunlight.", "Food makes them lighter.", "Only to stay awake."],
     "Animals cannot make food from sunlight, so they must eat."),
    ("A cow eats grass. Where did the energy in the grass come from?", "the sun", ["the cow", "the soil", "the rain"],
     "Grass captured sunlight to make its food."),
    ("Which organism can turn sunlight into stored food energy?", "a sunflower", ["a squirrel", "a mushroom", "a hawk"],
     "Plants are producers. Animals and fungi cannot capture sunlight."),
    ("What is the process plants use to make food from sunlight?", "photosynthesis", ["digestion", "evaporation", "decomposition"],
     "In photosynthesis, plants use light energy to make sugar from carbon dioxide and water."),
    ("A hawk eats a snake that ate a mouse that ate seeds. Which statement is true?", "The hawk's energy first came from the sun.", ["The hawk's energy came from the soil.", "The hawk makes its own energy.", "Only the seeds needed the sun."],
     "Trace it back: hawk ← snake ← mouse ← seeds ← sun."),
    ("You eat a carrot. The carrot's energy is used by your body. Where was that energy stored before you ate it?", "in the carrot's root, as food the plant made", ["in the dirt", "in the water you drank", "in the carrot's color"],
     "The carrot plant stored the sun's energy as sugar in its root."),
])
B5 = bank([
    ("Ava grows two bean plants. One is in a sunny window and one is in a dark closet. After two weeks, the closet plant is pale and weak. What does this show?", "Plants need light to make food.", ["Plants need darkness to grow.", "Plants get energy from the closet.", "Light is bad for plants."],
     "Without light, the plant cannot make the food that stores energy."),
    ("A student says, “A lion doesn't need the sun because it only eats meat.” How would you correct this?", "The animals the lion eats got their energy from plants, which got it from the sun.", ["The student is right.", "Lions eat sunlight.", "Lions make their own food."],
     "Every food chain begins with a producer powered by the sun."),
    ("Why do you feel tired and cold if you skip meals for a long time?", "Your body has less energy from food for motion and warmth.", ["Food makes you colder.", "Your body uses sunlight instead.", "You get too much energy."],
     "Food energy powers motion and keeps the body warm."),
    ("Which model best shows the flow of energy in a meal of rice and fish?", "sun → rice plant → you, and sun → algae → small animals → fish → you", ["soil → rice → you", "you → fish → algae → sun", "water → fish → you"],
     "Both foods trace back to producers that captured sunlight."),
    ("Leo measures the temperature of his hands before and after running. They get warmer. Where did that heat energy come from?", "the energy stored in the food he ate", ["the air around him", "his shoes", "the ground"],
     "Using food energy for motion also releases heat that warms the body."),
    ("Which comparison is correct?", "Plants make food with energy from sunlight; animals get energy by eating.", ["Animals make food from sunlight; plants eat.", "Both get energy from soil.", "Neither needs energy."],
     "Producers make food; consumers eat food."),
])


def body():
    think = ("<p>The energy in all food first came from the <b>sun</b>.</p>"
             "<ul><li><b>Plants</b> capture energy from sunlight and use it to make food (sugar) from carbon dioxide and water. "
             "This is called photosynthesis. The energy is stored in leaves, stems, roots, fruits and seeds.</li>"
             "<li><b>Animals</b> cannot make their own food. They get energy by eating plants, or by eating animals that ate plants.</li>"
             "<li>Animals use that energy for <b>body repair, growth, motion and keeping warm</b>.</li></ul>"
             + figure(sun_chain(["grass", "rabbit", "fox"]), "The fox's energy came from the rabbit, the rabbit's from the grass, and the grass's from the sun."))
    ex = [("A cheetah chases a gazelle that ate grass. Where did the cheetah's energy come from first?", ["cheetah ← gazelle ← grass", "The grass captured sunlight."], "the sun"),
          ("A puppy grows, runs, heals a scratch and stays warm. What gives it the energy for all of this?", ["It cannot make food from sunlight.", "It eats food that stores energy."], "the energy stored in its food")]
    mist = ["Thinking plants get their energy from the soil. Soil gives a few nutrients; the energy comes from sunlight.",
            "Thinking meat-eaters do not depend on the sun. Every food chain begins with a plant.",
            "Thinking food only gives materials. It also gives energy for growth, repair, motion and warmth.",
            "Drawing energy arrows backward. Energy moves from the sun to plants to animals."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy from the sun", B1 + [(g_food_source, 6), (g_use, 4)]),
        ("How animals use energy", [(g_use, 12), (g_food_source, 8)]),
        ("Tracing energy in food chains", [(g_path, 10), (g_chain_pic, 10)]),
        ("Energy in our food", [(g_calories, 8), (g_food_source, 6), (g_chain_pic, 6)]),
        ("Models and evidence", B5 + [g_path, g_use, g_calories, g_chain_pic]),
    ])
    make("grade-5", "energy-in-food", 7, "5-PS3-1",
         "Use models to describe that energy in animals’ food (used for body repair, growth, motion, and to maintain body warmth) was once energy from the sun.",
         "Energy in Food Comes from the Sun",
         "Grade 5 Energy in Food Worksheets: Energy from the Sun, Plants and Animals",
         "Energy in Food",
         "Free Grade 5 science worksheets on energy in food (NGSS 5-PS3-1): plants capture the sun's energy, animals use food for growth, repair, motion and warmth, and food chains that trace energy back to the sun. 100 practice questions with answers.",
         "The energy in all food was once energy from the sun.",
         "Plants capture sunlight and store energy in food. Animals eat it and use the energy for body repair, growth, motion and keeping warm.",
         body(),
         [("Where does the energy in food come from?", "From the sun. Plants capture sunlight and store its energy in the food they make. Animals get the energy by eating plants or animals that ate plants."),
          ("What do animals use energy from food for?", "Body repair, growth, motion and keeping their bodies warm."),
          ("Do meat-eating animals get energy from the sun?", "Yes, indirectly. The animals they eat got their energy from plants, and the plants got it from the sun."),
          ("What is photosynthesis?", "The process plants use to capture light energy and make sugar from carbon dioxide and water. The sugar stores the energy.")],
         sets)


if __name__ == "__main__":
    main()
