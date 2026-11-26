# -*- coding: utf-8 -*-
"""
UK Year 4 science: Solids, Liquids and Gases (States of matter)
  python tools/gen_uk_science_y4_solids_liquids_and_gases.py
Comparing and grouping materials as solids, liquids or gases; the properties of each state (shape, flowing, being
squashed); how the particles are arranged; tricky materials such as sand, honey and air; gases have mass.
Wrong answers come from real mistakes: "sand is a liquid because it pours", "gases have no mass", "a sponge is
squashed so solids can be compressed", "honey is a solid because it is thick".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61407)
R = U.R
P = People(R)

MAT = {"solid": ["ice", "a wooden spoon", "a stone", "sand", "sugar", "salt", "a coin", "chocolate (at room temperature)", "flour", "a glass marble", "butter (from the fridge)"],
       "liquid": ["water", "milk", "orange juice", "honey", "cooking oil", "shampoo", "vinegar", "melted chocolate", "lemonade"],
       "gas": ["steam", "air", "oxygen", "carbon dioxide", "helium in a balloon", "the bubbles in a fizzy drink", "water vapour", "the air inside a football"]}
TRICK = {"sand": "Each grain is a hard solid that keeps its shape; the grains just pour.", "sugar": "Each grain is a solid; the grains pour.",
         "flour": "Tiny solid grains pour, but each keeps its shape.", "salt": "Salt grains are tiny solids.",
         "honey": "It flows slowly, but it flows and takes the shape of its container.", "the bubbles in a fizzy drink": "The bubbles are carbon dioxide gas."}


def g_state():
    st = R.choice(sorted(MAT))
    m = R.choice(MAT[st])
    if not once(("st", m)):
        return None
    return item("Is %s a solid, a liquid or a gas?" % m, "a " + st, ["a " + x for x in sorted(MAT) if x != st] + ["none of these"],
                TRICK.get(m, "%s is a %s." % (m[0].upper() + m[1:], st)))


def g_pick():
    st = R.choice(sorted(MAT))
    a = R.choice(MAT[st])
    w = [R.choice(MAT[x]) for x in sorted(MAT) if x != st] + [R.choice(MAT[R.choice([x for x in sorted(MAT) if x != st])])]
    w = list(dict.fromkeys(w))
    if len(w) < 3 or not once(("pk", st, a), 2):
        return None
    w = w[:3]
    o = sorted([a] + w)
    return item("Which of these is a %s: %s or %s?" % (st, ", ".join(o[:3]), o[3]), a, w, TRICK.get(a, "%s is a %s." % (a[0].upper() + a[1:], st)))


PROP = [("keeps its own shape", "solids"), ("can be held in your hand without a container", "solids"), ("cannot be squashed into a smaller space", "solids and liquids"),
        ("flows and takes the shape of its container", "liquids"), ("forms a puddle when spilt", "liquids"), ("keeps the same volume but changes shape", "liquids"),
        ("spreads out to fill any container", "gases"), ("can be squashed into a smaller space", "gases"), ("escapes from an open container", "gases")]


def g_prop():
    p, a = R.choice(PROP)
    if not once(("pr", p)):
        return None
    opts = ["solids", "liquids", "gases", "solids and liquids"]
    return item("Which state of matter %s?" % p if a != "solids and liquids" else "Which states of matter %s?" % p, a, [x for x in opts if x != a],
                "Solids keep their shape; liquids flow; gases spread out and can be squashed.")


PART = [("solid", "packed closely in a regular pattern, vibrating on the spot"), ("liquid", "close together but able to slide past each other"),
        ("gas", "far apart and moving quickly in all directions")]


def g_part():
    st, d = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pt", st, k)):
        return None
    if k:
        return item("How are the particles arranged in a %s?" % st, d, [x[1] for x in PART if x[0] != st] + ["there are no particles"], "Everything is made of tiny particles.")
    return item("In which state are the particles %s?" % d, "a " + st, ["a " + x[0] for x in PART if x[0] != st] + ["none of them"], "Everything is made of tiny particles.")


def g_mass():
    who = P.next()[0]
    a = R.choice([520, 530, 540, 550, 560, 570])
    b = round(a - R.choice([1, 1.5, 2, 2.5, 3]), 1)
    if not once(("ma", a, b)):
        return None
    d = round(a - b, 1)
    from sci_phys import num
    g = "%s g" % num(d, 2)
    return item("%s weighs a sealed bottle of fizzy drink: %s g. After opening it and letting the bubbles escape for a day, it weighs %s g. How much mass of gas escaped?" % (who, num(a, 2), num(b, 2)), g,
                uniq(g, ["%s g" % num(a, 2), "%s g" % num(b, 2), "0 g", "%s g" % num(a + b, 2)]), "%s − %s = %s g. Gases have mass." % (num(a, 2), num(b, 2), num(d, 2)))


B1 = bank([
    ("What are the three states of matter?", "solid, liquid and gas", ["hot, warm and cold", "hard, soft and runny", "metal, wood and plastic"], "Everything is one of these."),
    ("Why is sand called a solid even though it pours?", "Each grain is a solid that keeps its shape.", ["It is really a liquid.", "It is a gas.", "Sand is not a material."], "Look at one grain."),
    ("Is honey a liquid?", "Yes. It flows slowly and takes the shape of its container.", ["No, it is a solid because it is thick.", "No, it is a gas.", "Only when it is cold."], "Viscous liquids flow slowly."),
    ("Do gases have mass?", "Yes, they have mass even though we cannot see most of them.", ["No, gases weigh nothing.", "Only steam has mass.", "Only in space."], "An inflated ball weighs more than a flat one."),
    ("Which state of matter can be squashed easily?", "gas", ["solid", "liquid", "none of them"], "Particles are far apart."),
    ("Why can you pour water but not a stone?", "Liquid particles can slide past each other; solid particles are held in place.", ["Stones are heavier.", "Water is a gas.", "Stones are wet."], "Particles explain properties."),
    ("What is air made of?", "a mixture of gases, mostly nitrogen and oxygen", ["only oxygen", "water", "nothing at all"], "About 78% nitrogen and 21% oxygen."),
    ("What happens to a gas let out of a bottle?", "It spreads out to fill the room.", ["It falls to the floor as a puddle.", "It keeps the bottle's shape.", "It turns into a solid."], "Gases fill any space."),
])
B5 = bank([
    ("A sponge gets smaller when squeezed. Does this mean solids can be squashed?", "No. The air in the holes is squeezed out; the solid itself does not shrink.", ["Yes, all solids can be squashed.", "Yes, sponges are liquids.", "No, sponges are gases."], "Think about what is in the holes."),
    ("How could you show that air takes up space?", "Push an upside-down cup into water: the air stops the water filling it.", ["Weigh a cup.", "Pour air into a jug.", "Look at the sky."], "Gases take up space."),
    ("Why is toothpaste hard to classify?", "It holds its shape a little but flows when squeezed, so it has properties of solids and liquids.", ["It is clearly a gas.", "It has no properties.", "It is always a liquid."], "Some materials are tricky."),
    ("How could you show that a gas has mass?", "Weigh a flat football, pump it up, and weigh it again.", ["Look at the ball.", "Bounce the ball.", "Paint the ball."], "More air, more mass."),
    ("Why does a smell spread across a room?", "Gas particles move and spread out in all directions.", ["Solid particles fly around.", "Liquids float in air.", "Smells are not made of particles."], "Gas particles move freely."),
])


def body():
    think = ("<p><b>Materials can be solids, liquids or gases.</b></p>"
             "<ul><li>Solids keep their shape and cannot be squashed. Liquids flow and take the shape of their container. Gases spread out to fill any space and can be squashed.</li>"
             "<li>Particles: packed and fixed in solids; close but sliding in liquids; far apart and fast in gases.</li>"
             "<li>Tricky ones: sand and sugar are solids (each grain keeps its shape); honey is a liquid; gases have mass.</li></ul>")
    ex = [("Sand pours. Solid or liquid?", ["Each grain keeps its shape"], "solid"),
          ("A gas is let out of a jar. What happens?", ["Gas particles spread out"], "it fills the room")]
    mist = ["Thinking sand is a liquid because it pours.", "Thinking gases have no mass.", "Thinking honey is a solid because it is thick."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Three states", B1 + [(g_state, 12)]),
        ("Grouping materials", [(g_state, 10), (g_pick, 10)]),
        ("Properties", [(g_prop, 9), (g_part, 6), (g_pick, 5)]),
        ("Tricky materials", [(g_pick, 10), (g_mass, 10)]),
        ("Thinking about matter", B5 + [(g_mass, 6), (g_state, 4), (g_pick, 5)]),
    ])
    make_uk(4, "solids-liquids-and-gases", 7, "States of matter",
            "Compare and group materials together, according to whether they are solids, liquids or gases.",
            "Solids, Liquids and Gases",
            "Year 4 Science: Solids, Liquids and Gases Worksheets (States of Matter)",
            "Solids, Liquids and Gases",
            "Free Year 4 science worksheets on solids, liquids and gases: grouping materials, properties of each state, particles, tricky materials and the mass of gases. 100 questions with answers.",
            "Solid, liquid or gas?",
            "Solids keep their shape, liquids flow, gases spread out to fill a space.",
            body(),
            [("What is the difference between solids, liquids and gases?", "Solids keep their own shape. Liquids flow and take the shape of their container. Gases spread out to fill any container and can be squashed."),
             ("Is sand a solid or a liquid?", "A solid. It pours, but each grain is a tiny solid that keeps its shape."),
             ("Do gases weigh anything?", "Yes. Gases have mass. A pumped-up ball weighs more than a flat one, and a fizzy drink gets lighter as its gas escapes.")],
            sets)


if __name__ == "__main__":
    main()
