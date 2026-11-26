# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Life Cycles (3-LS1-1)
  python tools/gen_us_science_g3_life_cycles.py
Organisms have unique and diverse life cycles, but all have birth, growth, reproduction and death in common.
Butterfly (egg, caterpillar/larva, chrysalis/pupa, adult), frog (egg, tadpole, froglet, adult),
grasshopper (egg, nymph, adult), chicken (egg, chick, adult), bean plant (seed, seedling, adult plant,
flower, fruit with seeds), human (baby, child, teen, adult).
Assessment boundary: no details of human reproduction.
Wrong answers come from real mistakes: "a caterpillar is a different animal from the butterfly",
"tadpoles turn into fish", "all animals have the same life cycle", "plants do not have life cycles".
"""
import math
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, text, arrow, People, INK, BLUE

U = Unit(30105)
R = U.R
P = People(R)

CYCLES = {"butterfly": ["egg", "caterpillar (larva)", "chrysalis (pupa)", "adult butterfly"],
          "frog": ["egg", "tadpole", "froglet", "adult frog"],
          "ladybug": ["egg", "larva", "pupa", "adult ladybug"],
          "mosquito": ["egg", "larva", "pupa", "adult mosquito"],
          "grasshopper": ["egg", "nymph", "adult grasshopper"],
          "chicken": ["egg", "chick", "adult chicken"],
          "dragonfly": ["egg", "nymph", "adult dragonfly"],
          "bean plant": ["seed", "seedling", "adult plant", "flower", "bean pod with seeds"],
          "apple tree": ["seed", "seedling", "young tree", "tree with flowers", "apple with seeds"],
          "dog": ["puppy", "young dog", "adult dog"],
          "sea turtle": ["egg", "hatchling", "young turtle", "adult turtle"],
          "salmon": ["egg", "alevin (baby fish)", "young salmon", "adult salmon"]}
ALL = sorted({s for v in CYCLES.values() for s in v})


def cycle_svg(stages, hide=None, label="a life cycle diagram"):
    n = len(stages)
    W, H = 460, 270
    cx, cy, r = 230, 133, 100
    s = []
    pos = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + r * 1.6 * math.cos(a), cy + r * math.sin(a)))
    for i, (x, y) in enumerate(pos):
        t = "?" if i == hide else stages[i].split(" (")[0]
        w = max(70, 8 * len(t) + 20)
        s.append(rect(x - w / 2, y - 16, w, 32, "#eef4fb" if i != hide else "#fff3c4", BLUE, 2, 8) + text(x, y + 5, t, 13))
    for i in range(n):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        f = lambda ux, uy: min(62 / max(abs(ux), 1e-6), 24 / max(abs(uy), 1e-6))
        k = f(dx / L, dy / L)
        sx, sy = x1 + dx / L * k, y1 + dy / L * k
        ex, ey = x2 - dx / L * k, y2 - dy / L * k
        s.append(arrow(sx, sy, ex, ey, INK, 2, 8))
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


def g_next():
    org = R.choice(sorted(CYCLES))
    st = CYCLES[org]
    i = R.randrange(len(st) - 1)
    a = st[i + 1]
    w = [x for x in st if x != a and x != st[i]] + [x for x in ALL if x not in st]
    w = list(dict.fromkeys(w))
    return item("In the life cycle of %s, which stage comes right after the %s?" % (("an " if org[0] in "aeiou" else "a ") + org, st[i].split(" (")[0]), a, R.sample(w[:6], 3) if len(w) >= 3 else w,
                "The %s life cycle: %s." % (org, " → ".join(st)))


def g_missing():
    org = R.choice([o for o in CYCLES if len(CYCLES[o]) >= 3])
    st = CYCLES[org]
    i = R.randrange(len(st))
    a = st[i]
    w = [x for x in ALL if x not in st]
    pic = fig(cycle_svg(st, i, "the life cycle of a %s with one stage missing" % org))
    return item(pic + "This is the life cycle of %s %s. Which stage is missing?" % ("an" if org[0] in "aeiou" else "a", org), a, R.sample(w, 3), "The %s life cycle: %s." % (org, " → ".join(st)))


def g_first():
    org = R.choice(sorted(CYCLES))
    st = CYCLES[org]
    k = R.choice(["first", "last"])
    if k == "first":
        return item("What is the first stage shown in the life cycle of %s?" % (("an " if org[0] in "aeiou" else "a ") + org), st[0], R.sample([x for x in st[1:]] + [x for x in ALL if x not in st], 3),
                    "The %s life cycle starts with the %s." % (org, st[0].split(" (")[0]))
    org = R.choice([o for o in CYCLES if "plant" not in o and "tree" not in o])
    st = CYCLES[org]
    w = st[:-1] + [x for x in ALL if x not in st and x.startswith("adult") is False]
    return item("Which stage of a %s's life cycle can reproduce (make young)?" % org, st[-1], R.sample(st[:-1], min(2, len(st) - 1)) + R.sample([x for x in ALL if x not in st and not x.startswith(("adult", "tree", "bean", "apple"))], 3 - min(2, len(st) - 1)),
                "Adults reproduce. Then the cycle starts again.")


COMPARE = [("butterfly", "grasshopper", "The butterfly has a pupa (chrysalis) stage; the grasshopper does not.", ["They have exactly the same stages.", "The grasshopper has a pupa stage; the butterfly does not.", "Neither one starts as an egg."]),
           ("frog", "chicken", "A frog has a tadpole stage in water; a chicken hatches as a chick that looks like a small adult.", ["Both have a tadpole stage.", "Chickens do not lay eggs.", "Frogs are born as adults."]),
           ("bean plant", "butterfly", "Both have birth, growth, reproduction and death, but the plant starts as a seed and the butterfly as an egg.", ["Plants do not have life cycles.", "They have exactly the same stages.", "The butterfly starts as a seed."]),
           ("dog", "frog", "A puppy looks like a small dog, but a tadpole looks very different from an adult frog.", ["A puppy is a tadpole.", "Both start as seeds.", "A frog has no young stage."]),
           ("ladybug", "dragonfly", "The ladybug has a pupa stage; the dragonfly goes from nymph straight to adult.", ["The dragonfly has a pupa stage.", "Neither lays eggs.", "They have the same stages."])]


def g_compare():
    a, b, ans, w = R.choice(COMPARE)
    if R.random() < 0.5:
        return item("How are the life cycles of a %s and a %s different?" % (a, b), ans, w, ans)
    return item("What do the life cycles of a %s and a %s have in common?" % (a, b), "Both are born, grow, reproduce and die.",
                ["Both have a tadpole stage.", "Both start as seeds.", "Neither one changes as it grows."], "All living things are born, grow, reproduce and die.")


B1 = bank([
    ("What is a life cycle?", "the stages a living thing goes through during its life", ["the path of a bike", "a kind of food chain", "the weather each season"],
     "Every plant and animal has a life cycle."),
    ("What do all life cycles have in common?", "birth, growth, reproduction and death", ["eggs, tadpoles and wings", "seeds and flowers only", "a pupa stage"],
     "The stages are different, but these four parts are the same."),
    ("A caterpillar is", "a young butterfly (larva)", ["a kind of worm that never changes", "a fish", "a plant"], "The caterpillar will become a pupa and then a butterfly."),
    ("A tadpole is", "a young frog", ["a baby fish", "an adult frog", "a kind of insect"], "Tadpoles live in water and breathe with gills."),
    ("What is metamorphosis?", "a big change in body shape during a life cycle", ["growing a little bigger", "eating a lot", "sleeping all winter"],
     "Butterflies and frogs go through metamorphosis."),
    ("Why do living things reproduce?", "so that new living things of their kind keep being born", ["so they can grow bigger", "so they can sleep", "to change color"],
     "Without reproduction, a kind of living thing would die out."),
    ("Do plants have life cycles?", "Yes. A seed grows into a plant that makes flowers and new seeds.", ["No, only animals do.", "Only trees do.", "Only in winter."], "Plants are living things too."),
    ("What does a chrysalis (pupa) do?", "protects the insect while its body changes into an adult", ["eats leaves all day", "lays eggs", "swims in a pond"], "Inside, the caterpillar becomes a butterfly."),
])
B5 = bank([
    ("Ava raises caterpillars in class. After 2 weeks, they make chrysalises. What will most likely come out?", "butterflies", ["caterpillars", "frogs", "beetles"],
     "The pupa stage is followed by the adult."),
    ("Leo plants bean seeds and records the plant every day. What should he expect to see first?", "a small sprout (seedling)", ["beans", "flowers", "a full adult plant"],
     "The seed grows into a seedling first."),
    ("Mia compares a frog and a fish. How can she tell a tadpole is not a fish?", "It grows legs and lungs and becomes a frog.", ["It swims.", "It lives in water.", "It has a tail."],
     "Tadpoles change a lot; fish do not grow legs."),
    ("Why do frogs lay so many eggs?", "Many eggs and tadpoles are eaten, so laying many helps some survive.", ["Frogs like to count.", "Each egg grows into many frogs.", "Eggs keep the pond warm."],
     "Only some young survive to become adults."),
    ("Noah makes a model of a life cycle as a circle with arrows. Why is it a circle?", "The adults make new young, so the cycle starts again.", ["Circles are easier to draw.", "Living things move in circles.", "Life cycles never end for one animal."],
     "Reproduction starts the cycle again."),
])


def body():
    st = CYCLES["butterfly"]
    think = ("<p>A <b>life cycle</b> is the stages a living thing goes through. Every life cycle includes <b>birth</b>, <b>growth</b>, <b>reproduction</b> (making young) and <b>death</b>.</p>"
             + figure(cycle_svg(st, None, "the life cycle of a butterfly"), "Butterfly: egg → caterpillar → chrysalis → adult.")
             + "<p>Life cycles are different: a butterfly and a frog change shape a lot (<b>metamorphosis</b>), a grasshopper goes from egg to nymph to adult, "
             "a puppy looks like a small dog, and a plant goes from seed to seedling to adult plant to flower and fruit.</p>")
    ex = [("What comes after a tadpole?", ["The tadpole grows legs.", "It becomes a froglet."], "froglet"),
          ("What do a bean plant and a chicken have in common?", ["Both are living things."], "Both are born, grow, reproduce and die.")]
    mist = ["Thinking a caterpillar or tadpole is a different animal.",
            "Thinking all animals have the same stages.",
            "Forgetting that plants have life cycles too."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is a life cycle?", B1 + [(g_next, 6), (g_first, 6)]),
        ("Stages in order", [(g_next, 12), (g_first, 8)]),
        ("Life cycle diagrams", [(g_missing, 14), (g_next, 6)]),
        ("Comparing life cycles", [(g_compare, 10), (g_missing, 6), (g_first, 4)]),
        ("Observing life cycles", B5 + [g_missing, g_next, g_compare]),
    ])
    make("grade-3", "life-cycles", 5, "3-LS1-1",
         "Develop models to describe that organisms have unique and diverse life cycles but all have in common birth, growth, reproduction, and death.",
         "Life Cycles of Plants and Animals",
         "Grade 3 Life Cycle Worksheets: Butterflies, Frogs, Plants and More",
         "Life Cycles",
         "Free Grade 3 science worksheets on life cycles (NGSS 3-LS1-1): butterfly, frog, grasshopper, chicken and plant life cycles, metamorphosis, life cycle diagrams and comparing life cycles. 100 practice questions with answers.",
         "All living things are born, grow, reproduce and die.",
         "Life cycles have different stages, like egg, caterpillar, chrysalis and butterfly, but every cycle starts again with reproduction.",
         body(),
         [("What are the stages of a butterfly's life cycle?", "Egg, caterpillar (larva), chrysalis (pupa) and adult butterfly."),
          ("What do all life cycles have in common?", "All living things are born, grow, reproduce and die."),
          ("What is metamorphosis?", "It is a big change in body shape during a life cycle, like a caterpillar becoming a butterfly or a tadpole becoming a frog.")],
         sets)


if __name__ == "__main__":
    main()
