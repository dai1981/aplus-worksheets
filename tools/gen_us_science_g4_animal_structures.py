# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Animal Structures and Their Functions (4-LS1-1)
  python tools/gen_us_science_g4_animal_structures.py
Animals have internal structures (heart, lungs, gills, stomach, brain, skeleton, muscles) and
external structures (beaks, claws, fur, feathers, shells, scales, webbed feet, fins) that support
survival, growth, behavior and reproduction.
Wrong answers come from real mistakes: "fish breathe with lungs", "the heart helps you think",
"a structure appears because an animal needs it" (avoided: we say "helps", not "grew because").
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(40110)
R = U.R
P = People(R)

ORGAN = {"heart": "pumps blood around the body", "lungs": "take in oxygen from the air", "stomach": "breaks down food",
         "brain": "controls the body and processes information from the senses", "skeleton": "supports the body and protects organs",
         "muscles": "move the bones so the body can move", "gills": "take in oxygen from water", "skull": "protects the brain",
         "ribs": "protect the heart and lungs", "intestines": "take in nutrients from digested food"}
HAS = {"heart": "a heart", "lungs": "lungs", "stomach": "a stomach", "brain": "a brain", "skeleton": "a skeleton", "muscles": "muscles",
       "gills": "gills", "skull": "a skull", "ribs": "ribs", "intestines": "intestines"}
CLASH = [{"lungs", "gills"}, {"skeleton", "ribs"}, {"skeleton", "skull"}, {"skull", "ribs"}, {"stomach", "intestines"}, {"skeleton", "muscles"}]


def ok(a, b):
    return {a, b} not in CLASH


def g_organ():
    k = R.choice(sorted(ORGAN))
    if R.random() < 0.5:
        w = [x for x in ORGAN if x != k and ok(x, k)]
        sg = ORGAN[k].replace("take in", "takes in").replace("protect the", "protects the").replace("move the", "moves the")
        return item("Which internal structure %s?" % sg, "the " + k, ["the " + x for x in R.sample(w, 3)], "The %s %s." % (k, ORGAN[k]))
    w = [ORGAN[x] for x in ORGAN if x != k and ok(x, k)]
    pl = k in ("lungs", "muscles", "gills", "ribs", "intestines")
    sub = "They " if pl else "It "
    fix = lambda t: t if pl else t.replace("take in", "takes in").replace("protect ", "protects ").replace("move the", "moves the")
    fixw = lambda t: (t.replace("takes in", "take in").replace("pumps", "pump").replace("breaks", "break").replace("controls", "control").replace("supports the body and protects", "support the body and protect").replace("protects", "protect")
                      if pl else fix(t))
    return item(("What do the %s do?" if pl else "What does the %s do?") % k, sub + fixw(ORGAN[k]) + ".", [sub + fixw(x) + "." for x in R.sample(w, 3)],
                "The %s %s." % (k, ORGAN[k]))


# (animal, structure, how it helps, wrong structures)
ADAPT = [("a duck", "webbed feet", "swim by pushing water", ["sharp claws for digging", "a long trunk", "a hard shell"]),
         ("an eagle", "a sharp, hooked beak", "tear meat", ["a long, thin beak for sipping nectar", "webbed feet", "a flat bill for straining mud"]),
         ("a hummingbird", "a long, thin beak", "reach nectar deep inside flowers", ["a short, thick beak for cracking seeds", "a hooked beak", "webbed feet"]),
         ("a cardinal", "a short, thick beak", "crack open seeds", ["a long, thin beak", "a hooked beak for tearing meat", "a flat bill"]),
         ("a polar bear", "thick fur and a layer of fat", "stay warm in the Arctic", ["thin fur and big ears", "gills", "a long tail for climbing"]),
         ("a turtle", "a hard shell", "protect its soft body from predators", ["bright feathers", "long legs for running", "gills"]),
         ("a fish", "gills", "take in oxygen from water", ["lungs", "fur", "a beak"]),
         ("a fish", "fins and a tail", "steer and swim", ["claws", "feathers", "a beak"]),
         ("a porcupine", "sharp quills", "keep predators away", ["webbed feet", "a long beak", "gills"]),
         ("a mole", "strong, wide front claws", "dig tunnels underground", ["webbed feet", "long thin legs", "wings"]),
         ("a giraffe", "a very long neck", "reach leaves high in trees", ["a short neck", "a hard shell", "webbed feet"]),
         ("an owl", "large eyes that face forward", "see prey at night", ["tiny eyes on the sides", "gills", "a hard shell"]),
         ("a rabbit", "long ears", "hear predators coming", ["a hard shell", "webbed feet", "a hooked beak"]),
         ("an elephant", "a long trunk", "pick up food and suck up water", ["a short beak", "gills", "webbed feet"]),
         ("a frog", "long, strong back legs", "jump far", ["short legs", "a hard shell", "feathers"]),
         ("a snake", "a jaw that can open very wide", "swallow prey whole", ["sharp hooves", "feathers", "gills"]),
         ("a camel", "wide, flat feet", "walk on soft sand without sinking", ["webbed feet", "sharp claws for climbing", "small hooves"]),
         ("a peacock", "bright tail feathers", "attract a mate", ["dull brown feathers", "gills", "a hard shell"]),
         ("a woodpecker", "a strong, pointed beak", "drill holes in trees to find insects", ["a flat bill", "webbed feet", "a long trunk"]),
         ("a cheetah", "long legs and a flexible spine", "run very fast to catch prey", ["short legs", "a hard shell", "webbed feet"]),
         ("a bat", "large ears", "hear echoes to find insects in the dark", ["a hard shell", "gills", "webbed feet"]),
         ("a kangaroo", "a pouch", "carry and protect its baby", ["gills", "a hard shell", "a beak"]),
         ("a chameleon", "a long, sticky tongue", "catch insects", ["a short, dry tongue", "gills", "webbed feet"]),
         ("a crab", "a hard outer shell and pincers", "protect itself and grab food", ["soft skin", "feathers", "fur"])]
WHY = sorted({a[2] for a in ADAPT})
KIND = {"webbed feet": "growth", "thick fur and a layer of fat": "survival", "bright tail feathers": "reproduction", "a pouch": "reproduction"}


def cap(s):
    return s[0].upper() + s[1:]


def g_which():
    an, st, why, w = R.choice(ADAPT)
    return item("Which structure helps %s %s?" % (an, why), st, w, "%s has %s that help it %s." % (cap(an), st, why))


def g_how():
    an, st, why, w = R.choice(ADAPT)
    others = [x for x in WHY if x != why]
    return item("%s has %s. How does this structure help it?" % (cap(an), st), "It helps it %s." % why, ["It helps it %s." % x for x in R.sample(others, 3)],
                "This structure helps %s %s." % (an, why))


def g_ext():
    pools = {"internal": ["the heart", "the lungs", "the stomach", "the brain", "the skeleton", "the gills", "the muscles", "the intestines"],
             "external": ["a beak", "claws", "fur", "feathers", "a shell", "scales", "fins", "webbed feet", "horns"]}
    k = R.choice(["internal", "external"])
    a = R.choice(pools[k])
    other = "external" if k == "internal" else "internal"
    return item("Which of these is an %s structure (%s the body)?" % (k, "inside" if k == "internal" else "outside"), a, R.sample(pools[other], 3),
                "%s is %s the body." % (cap(a), "inside" if k == "internal" else "on the outside of"))


def g_job():
    rows = [("survival", ["a turtle's shell", "a porcupine's quills", "a polar bear's thick fur", "a snake's sharp fangs", "a skunk's smelly spray"]),
            ("reproduction", ["a peacock's bright feathers", "a kangaroo's pouch", "a frog's loud mating call", "a bird's nest-building behavior"]),
            ("getting food", ["an eagle's hooked beak", "a chameleon's sticky tongue", "a woodpecker's strong beak", "a giraffe's long neck"]),
            ("moving", ["a duck's webbed feet", "a fish's fins", "a frog's strong back legs", "a bird's wings"])]
    k = R.randrange(4)
    name, xs = rows[k]
    x = R.choice(xs)
    w = [r[0] for i, r in enumerate(rows) if i != k]
    return item("%s: which need does this structure mostly help with?" % cap(x), name, w, "%s helps with %s." % (cap(x), name))


B1 = bank([
    ("What is an internal structure?", "a body part inside the animal, like the heart", ["a body part on the outside, like fur", "the animal's home", "the food an animal eats"],
     "Internal = inside. External = outside."),
    ("What is an external structure?", "a body part on the outside, like a beak or claws", ["a body part inside, like the lungs", "the animal's shadow", "a plant the animal eats"],
     "You can see external structures from the outside."),
    ("How do fish take in oxygen?", "through their gills", ["through lungs like ours", "through their fins", "through their scales"],
     "Gills take oxygen out of the water."),
    ("Which structure protects your brain?", "the skull", ["the stomach", "the lungs", "the muscles"], "The skull is a hard case of bone."),
    ("Which structures work together to move your arm?", "bones and muscles", ["lungs and heart", "stomach and skin", "eyes and ears"],
     "Muscles pull on bones to make them move."),
    ("Why do birds have hollow bones?", "Hollow bones are light, which helps birds fly.", ["Hollow bones hold water.", "Hollow bones make birds heavier.", "Birds use them to sing."],
     "Lighter bodies are easier to lift into the air."),
    ("Structures help animals with survival, growth, behavior and", "reproduction (making young)", ["photosynthesis", "making rocks", "changing the weather"],
     "These are the four things named in the standard."),
    ("A bird's feathers help it fly and also", "keep it warm", ["help it breathe under water", "digest food", "make sound"],
     "Feathers trap warm air close to the body."),
])
B5 = bank([
    ("Ava sees a bird with a long, thin beak. What does it most likely eat?", "nectar from flowers", ["large seeds that must be cracked", "fish caught in deep water", "meat torn from prey"],
     "A long, thin beak can reach deep inside flowers."),
    ("Leo finds an animal with webbed feet and waterproof feathers. Where does it most likely live?", "near ponds, lakes or the ocean", ["in a dry desert", "deep underground", "high in dry trees"],
     "Webbed feet and waterproof feathers help with swimming."),
    ("A desert fox has very large ears. Besides hearing, how do large ears help in the desert?", "They let heat leave the body, helping the fox stay cool.", ["They store water.", "They keep the fox warm.", "They help it fly."],
     "Blood flowing through the big ears gives off heat."),
    ("Mia argues that a turtle's shell helps it survive. Which evidence best supports her claim?", "Turtles pull into their shells when a predator comes near.", ["Turtles are green.", "Some turtles live in ponds.", "Turtles lay eggs."],
     "The behavior shows the shell protects the turtle."),
    ("Which structure would help an animal that lives in the snowy Arctic?", "thick fur and wide, furry feet", ["thin skin and big ears", "gills", "a long, thin beak"],
     "Thick fur keeps it warm; wide feet help it walk on snow."),
    ("Why do many prey animals, like deer, have eyes on the sides of their heads?", "to see predators coming from almost every direction", ["to see colors better", "to judge distance when hunting", "to see in the dark only"],
     "Side eyes give a wide view."),
])


def body():
    think = ("<p>Animals have <b>structures</b> (body parts) that help them survive, grow, behave and reproduce.</p>"
             "<ul><li><b>Internal</b> structures are inside: the heart pumps blood, lungs or gills take in oxygen, the stomach breaks down food, the brain controls the body, and the skeleton supports the body.</li>"
             "<li><b>External</b> structures are outside: beaks, claws, fur, feathers, shells, scales, fins and webbed feet.</li></ul>"
             "<p>The shape of a structure tells you about its job. A hooked beak tears meat; a long, thin beak reaches nectar; webbed feet push water.</p>")
    ex = [("How does a polar bear's thick fur help it?", ["The Arctic is very cold.", "Fur traps heat."], "It keeps the bear warm so it can survive."),
          ("Is a fish's gill internal or external, and what does it do?", ["Gills are inside the body behind the head.", "They take oxygen from water."], "internal; takes in oxygen from water")]
    mist = ["Saying fish breathe with lungs. Fish use gills.",
            "Mixing up internal (inside) and external (outside) structures.",
            "Saying an animal grew a structure because it wanted it. Say the structure helps the animal."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Internal and external structures", B1 + [(g_ext, 6), (g_organ, 6)]),
        ("Inside the body", [(g_organ, 12), (g_ext, 8)]),
        ("Structures for food and movement", [(g_which, 10), (g_how, 10)]),
        ("Survival, growth and reproduction", [(g_job, 8), (g_which, 6), (g_how, 6)]),
        ("Making arguments from evidence", B5 + [g_which, g_how, g_job, g_organ]),
    ])
    make("grade-4", "animal-structures", 10, "4-LS1-1",
         "Construct an argument that plants and animals have internal and external structures that function to support survival, growth, behavior, and reproduction.",
         "Animal Structures and Their Functions",
         "Grade 4 Animal Structures Worksheets: Internal and External Structures and Adaptations",
         "Animal Structures",
         "Free Grade 4 science worksheets on animal structures (NGSS 4-LS1-1): internal organs like the heart, lungs and gills, external structures like beaks, claws, fur and shells, and how they help animals survive. 100 practice questions with answers.",
         "Animal structures help them survive, grow and reproduce.",
         "Internal structures like the heart and lungs work inside the body. External structures like beaks, fur and claws work on the outside.",
         body(),
         [("What is the difference between internal and external structures?", "Internal structures are inside the body, like the heart, lungs and stomach. External structures are on the outside, like fur, beaks and claws."),
          ("How do animal structures help them survive?", "They help animals get food, move, stay warm, breathe, protect themselves and raise young."),
          ("How can a bird's beak tell you what it eats?", "A hooked beak tears meat, a short thick beak cracks seeds, and a long thin beak reaches nectar in flowers.")],
         sets)


if __name__ == "__main__":
    main()
