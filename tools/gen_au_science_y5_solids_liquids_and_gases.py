# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U04: the particle model explains the properties of solids, liquids and gases.
  python tools/gen_au_science_y5_solids_liquids_and_gases.py
Own particle diagrams (regular pattern / close but jumbled / far apart) plus the UK Year 4, US Grade 5 and SG Primary 4
states-of-matter makers with Australian names.
Wrong answers come from real mistakes: thinking gases have no mass, that particles in a solid do not move at all,
that a liquid's particles are far apart, and that sugar "disappears" when it dissolves.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 5, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

UK = "gen_uk_science_y4_solids_liquids_and_gases"
US = "gen_us_science_g5_matter_is_made_of_particles"
SG = "gen_sg_science_p4_matter"
uk_state = limit(src(UK, "g_state"), 6)
uk_pick = limit(src(UK, "g_pick"), 5)
uk_prop = src(UK, "g_prop")
uk_part = src(UK, "g_part")
uk_mass = limit(src(UK, "g_mass"), 2)
uk_b1 = src.B(UK, "B1")
uk_b5 = src.B(UK, "B5")
us_b1 = src.B(US, "B1")
us_b2 = src.B(US, "B2")
us_b3 = src.B(US, "B3")
us_b5 = src.B(US, "B5")
us_smell = limit(src(US, "g_smell"), 2)
us_tank = limit(src(US, "g_tank"), 2)
sg_prop = src(SG, "g_prop")
sg_syr = src(SG, "g_syr")
sg_b2 = src.B(SG, "B2")


def box(kind, label):
    pts = []
    if kind == "solid":
        for r in range(5):
            for c in range(6):
                pts.append((14 + c * 18, 14 + r * 18))
    elif kind == "liquid":
        for r in range(4):
            for c in range(6):
                pts.append((14 + c * 18 + R.choice([-3, 0, 3]) + (6 if r % 2 else 0), 34 + r * 17 + R.choice([-3, 0, 3])))
    else:
        cells = [(x, y) for x in (18, 52, 86, 110) for y in (18, 52, 86)]
        pts = [(x + R.choice([-6, 0, 6]) - (8 if x == 110 else 0), y + R.choice([-6, 0, 6])) for x, y in R.sample(cells, 7)]
    dots = "".join("<circle cx='%d' cy='%d' r='7' fill='#5b8def' stroke='#2a4f9c'/>" % p for p in pts)
    return ("<g><rect x='2' y='2' width='120' height='100' fill='#fff' stroke='#333' stroke-width='2'/>%s"
            "<text x='62' y='122' text-anchor='middle' font-size='15' font-weight='bold'>%s</text></g>" % (dots, label))


DESC = {"solid": "a solid: particles close together in a regular pattern, vibrating on the spot",
        "liquid": "a liquid: particles close together but jumbled, sliding past each other",
        "gas": "a gas: particles far apart, moving quickly in all directions"}
WRONG = ["a gas: particles packed tightly in rows", "a solid: particles far apart and not moving", "a liquid: particles far apart, moving quickly"]


def g_box():
    order = R.sample(["solid", "liquid", "gas"], 3)
    svg = "<svg viewBox='0 0 400 130' width='400' role='img' aria-label='three particle diagrams A, B and C'>%s</svg>" % "".join(
        "<g transform='translate(%d,0)'>%s</g>" % (8 + i * 132, box(k, "ABC"[i])) for i, k in enumerate(order))
    i = R.randrange(3)
    k = order[i]
    w = [DESC[x] for x in order if x != k] + [x for x in WRONG if not x.startswith("a " + k)][:1]
    return tq("%s<br>What does diagram %s show?" % (svg, "ABC"[i]), DESC[k], w, "Solids: regular pattern. Liquids: close but jumbled. Gases: far apart.")


def g_which():
    order = R.sample(["solid", "liquid", "gas"], 3)
    svg = "<svg viewBox='0 0 400 130' width='400' role='img' aria-label='three particle diagrams A, B and C'>%s</svg>" % "".join(
        "<g transform='translate(%d,0)'>%s</g>" % (8 + i * 132, box(k, "ABC"[i])) for i, k in enumerate(order))
    k = R.choice(["solid", "liquid", "gas"])
    what = {"solid": "ice", "liquid": "water in a glass", "gas": "water vapour (steam)"}[k]
    return tq("%s<br>Which diagram shows the particles in %s?" % (svg, what), "diagram " + "ABC"[order.index(k)],
              ["diagram " + "ABC"[j] for j in range(3) if order[j] != k] + ["none of them: %s has no particles" % what.split(" (")[0]],
              "Ice is a solid, liquid water is a liquid, water vapour is a gas.")


PROPS = [("keep their own shape", "solids"), ("have a fixed volume but take the shape of their container", "liquids"),
         ("spread out to fill any container", "gases"), ("can be poured", "liquids"), ("can be squashed (compressed) easily", "gases"),
         ("can be held in your hand and do not flow", "solids")]
WHY = {"solids": "the particles are held in fixed places", "liquids": "the particles are close but can slide past each other",
       "gases": "the particles are far apart and move freely"}


def g_why():
    p, s = R.choice(PROPS)
    w = [v for k, v in WHY.items() if k != s] + ["the particles have no mass"]
    return tq("%s %s. Which idea about particles explains this?" % (s.capitalize(), p), WHY[s], w,
              "Particle model: %s, because %s." % (s, WHY[s]))


POOL1 = pool(R, [
    ("What is all matter made of?", "tiny particles that are too small to see", ["air", "water", "light"], "Solids, liquids and gases are all made of particles."),
    ("Do the particles in a solid move?", "Yes, they vibrate on the spot.", ["No, they never move.", "Yes, they move freely around the room.", "Only when the solid is cold."], "They vibrate but stay in place."),
    ("What happens to particles when a solid is heated?", "They vibrate faster and move further apart.", ["They get smaller.", "They stop moving.", "They disappear."], "Heating gives the particles more energy."),
    ("Why does a gas spread through a whole room?", "Its particles move quickly in all directions with lots of space between them.", ["Its particles are joined together.", "Gas particles are larger than solid particles.", "Gases are pulled by gravity to fill rooms."], "This is why we can smell a barbecue from far away."),
    ("A bike tyre is pumped up. Where do the extra air particles go?", "They are squashed closer together inside the tyre.", ["They disappear.", "They turn into a liquid.", "They get smaller."], "Gases can be compressed."),
    ("Which state of matter has particles that are furthest apart?", "a gas", ["a solid", "a liquid", "all the same"], "Gas particles have lots of space between them."),
    ("Why does honey flow more slowly than water?", "Honey's particles do not slide past each other as easily.", ["Honey is a solid.", "Honey has no particles.", "Water is a gas."], "Both are liquids, but they flow at different rates."),
    ("Is sand a solid or a liquid?", "a solid: each grain keeps its shape", ["a liquid, because it can be poured", "a gas", "it is not matter"], "Tiny solid grains can be poured, but each grain is solid."),
])
POOL5 = pool(R, [
    ("Mia weighs a flat beach ball (150 g), then pumps it up and weighs it again. What will the scale most likely show?", "a little more than 150 g", ["exactly 150 g", "less than 150 g", "0 g"], "Air has mass."),
    ("Jack pushes the plunger of a sealed syringe of air and then a sealed syringe of water. What happens?", "The air can be squashed; the water hardly moves.", ["The water can be squashed; the air cannot.", "Both squash the same.", "Neither can move."], "Gas particles have space between them; liquid particles do not."),
    ("Ruby puts a drop of food colouring in hot water and in cold water. Which result is most likely?", "It spreads faster in the hot water.", ["It spreads faster in the cold water.", "It does not spread in either.", "It spreads at the same rate."], "Particles move faster in hot water."),
    ("Kai wants to test which liquid flows fastest down a ramp. What should he keep the same?", "the amount of each liquid, the ramp and its slope", ["the type of liquid", "nothing", "only the colour of the liquids"], "Only the liquid should change."),
    ("Ella tests four liquids. Time to flow down a ramp: water 2 s, oil 6 s, honey 40 s, dishwashing liquid 15 s. Which flows most slowly?", "honey", ["water", "oil", "dishwashing liquid"], "The longest time means the slowest flow."),
    ("Using Ella's results, which list orders the liquids from fastest to slowest?", "water, oil, dishwashing liquid, honey", ["honey, dishwashing liquid, oil, water", "oil, water, honey, dishwashing liquid", "water, honey, oil, dishwashing liquid"], "Shorter times mean faster flow."),
])


def main():
    sets = U.sets([
        ("Solid, liquid or gas?", [(uk_state, 6), (uk_pick, 5), (uk_prop, 4), (sg_prop, 3), (POOL1, 2)]),
        ("Particle diagrams", [(g_box, 6), (g_which, 5), (uk_part, 5), (POOL1, 4)]),
        ("Explaining properties", [(g_why, 8), (us_b2, 6), (sg_b2, 3), (POOL1, 2), (uk_prop, 1)]),
        ("Gases have mass", [(uk_b1, 5), (us_b1, 5), (sg_syr, 4), (us_tank, 2), (uk_mass, 2), (us_smell, 2)]),
        ("Investigations", [(POOL5, 6), (uk_b5, 4), (us_b3, 4), (us_b5, 4), (g_box, 2)]),
    ])
    make_au(YEAR, "solids-liquids-and-gases", SORT, "AC9S5U04", "Chemical sciences",
            "Explain the observable properties of solids, liquids and gases by modelling the motion and arrangement of particles "
            "(Australian Curriculum v9.0 Science content description).",
            "Solids, Liquids and Gases", "Solids, liquids and gases",
            "Free Year 5 science worksheets on solids, liquids and gases and the particle model: particle diagrams, why liquids pour, "
            "why gases spread and squash, and why air has mass. 100 questions with answers.",
            "Particles explain solids, liquids and gases.", "How close the particles are and how they move explains each state.",
            "<p><b>All matter is made of tiny particles that are always moving.</b></p><ul>"
            "<li>Solid: particles close together in a regular pattern, vibrating on the spot, so solids keep their shape.</li>"
            "<li>Liquid: particles close together but jumbled, sliding past each other, so liquids pour and take the shape of their container.</li>"
            "<li>Gas: particles far apart and moving fast, so gases spread out and can be squashed. Gases still have mass.</li></ul>",
            [("Why can water be poured but ice cannot?", ["ice particles are held in place", "water particles slide past each other"], "water is a liquid"),
             ("A tyre is pumped up. What happens to the air particles?", ["more particles go in", "they are pushed closer together"], "they are compressed")],
            ["Thinking gases have no mass.", "Thinking particles in a solid do not move at all (they vibrate).",
             "Drawing liquid particles far apart (they are close together, like a solid, but jumbled)."],
            [("What is the particle model?", "It is the idea that all matter is made of tiny moving particles. How close they are and how they move explains whether something is a solid, a liquid or a gas."),
             ("Does air have mass?", "Yes. A ball or tyre gets a little heavier when it is pumped full of air, and a full scuba tank weighs more than an empty one."),
             ("Why can gases be squashed but liquids cannot?", "Gas particles have lots of space between them, so they can be pushed closer. Liquid particles are already touching, so liquids hardly squash at all.")],
            sets)


if __name__ == "__main__":
    main()
