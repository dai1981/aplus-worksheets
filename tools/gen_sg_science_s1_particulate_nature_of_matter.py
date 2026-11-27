# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Models): Model of Matter - the Particulate Nature of Matter
  python tools/gen_sg_science_s1_particulate_nature_of_matter.py
Matter is made of tiny, discrete particles in constant, random motion; the arrangement and movement of particles in solids,
liquids and gases; diffusion (net movement from a higher to a lower concentration); expansion and contraction (particles move
further apart, they do not grow); conservation of mass; melting and boiling; Brownian motion.
UK KS3 particle makers are reused.
Wrong answers come from real mistakes: "particles expand when heated", "particles in a solid do not move",
"mass increases when a solid melts", "diffusion only happens in gases".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64107)
R = U.R
P = People(R)
PM = luse(U, "gen_uk_science_y7_particles_and_states_of_matter", drop=[r"dens"])

ST = {"solid": ("closely packed in a fixed, orderly arrangement", "vibrate about fixed positions", "very strong"),
      "liquid": ("close together but not in fixed positions", "slide past one another", "strong"),
      "gas": ("far apart and randomly arranged", "move quickly and randomly in all directions", "very weak")}


def g_model():
    s = R.choice(sorted(ST))
    k = R.choice([0, 1])
    if not once(("md", s, k)):
        return None
    q = ("How are the particles arranged in a %s?" if k == 0 else "How do the particles in a %s move?") % s
    return item(q, ST[s][k][0].upper() + ST[s][k][1:] + ".", [ST[x][k][0].upper() + ST[x][k][1:] + "." for x in sorted(ST) if x != s] + [("They do not move at all." if k else "They are all touching in a gas.")],
                "In a %s, particles are %s and %s." % (s, ST[s][0], ST[s][1]))


EXP = [("A metal lid on a glass jar is held under hot water and then opens easily.", "The metal lid expands more than the glass when heated."),
       ("Gaps are left between sections of a railway track.", "The steel expands on hot days and needs room to expand."),
       ("Power cables sag more on a hot afternoon.", "The cables expand and become longer when heated."),
       ("A dented ping-pong ball pops back into shape in hot water.", "The air particles inside move faster and further apart, pushing the dent out."),
       ("The liquid in a thermometer rises when it is warmed.", "The liquid expands as its particles move further apart."),
       ("A balloon left in the sun gets bigger.", "The air inside expands as its particles move faster and further apart."),
    ("A thick glass cup cracks when boiling water is poured into it.", "The inside of the glass expands faster than the outside."),
    ("Bridges have expansion joints with small gaps.", "The bridge can expand on hot days without buckling."),
       ("Concrete roads are built with gaps filled with soft material.", "The concrete can expand on hot days without cracking.")]


def g_exp():
    s, a = R.choice(EXP)
    if not once(("ex", s)):
        return None
    w = ["The particles themselves become bigger when heated.", "The mass of the substance increases when heated.", "Heat makes new particles form."]
    return item(s + " Which explains this?", a, w, "Particles move faster and further apart when heated; they do not grow and no new particles form.")


DIF = [("A drop of ink is added to a beaker of still water. After an hour the water is evenly coloured.", "ink particles moved from a higher to a lower concentration"),
       ("You can smell durian from the other end of a room.", "durian smell particles diffused through the air"),
       ("A crystal of potassium manganate(VII) is placed in water. A purple colour slowly spreads.", "the purple particles moved from a higher to a lower concentration"),
       ("A tea bag is put into hot water and the colour spreads.", "tea particles diffused into the water"),
       ("A spray of air freshener can soon be smelt across the classroom.", "air freshener particles diffused through the air"),
       ("Oxygen moves from the air in the lungs into the blood.", "oxygen moved from a higher to a lower concentration")]


def g_dif():
    s, a = R.choice(DIF)
    if not once(("df", s)):
        return None
    return item(s + " What is the best explanation?", "Diffusion: " + a + ".",
                ["The particles were pushed by convection only.", "The particles grew bigger and filled the space.", "The water or air particles stopped moving."],
                "Particles are always moving randomly, so there is a net movement from where they are more concentrated to where they are less concentrated.")


def g_rate():
    k = R.choice(["temp", "state", "mass"])
    if not once(("rt", k), 5 if k == "temp" else 1):
        return None
    if k == "temp":
        t1, t2 = R.sample([10, 20, 40, 60, 80], 2)
        hi = max(t1, t2)
        return item("Two identical drops of food colouring are added to water at %d °C and at %d °C. In which beaker does the colour spread faster?" % (t1, t2), "the beaker at %d °C" % hi,
                    ["the beaker at %d °C" % min(t1, t2), "both at the same rate", "neither; colour does not spread"], "At a higher temperature, particles move faster, so diffusion is faster.")
    if k == "state":
        return item("In which state does diffusion happen fastest?", "gas", ["liquid", "solid", "it is the same in all states"], "Gas particles move fastest and are furthest apart.")
    return item("Ammonia gas and hydrogen chloride gas are released at opposite ends of a glass tube. A white ring forms nearer the hydrogen chloride end. What does this show?",
                "Ammonia particles diffuse faster because they are lighter.", ["Hydrogen chloride particles are lighter.", "Both gases diffuse at the same rate.", "The gases do not move."],
                "Lighter particles move faster at the same temperature.")


PC = [("melting", "They gain energy and move out of their fixed positions, but stay close together."),
      ("boiling", "They gain enough energy to escape from the liquid and move far apart."),
      ("freezing", "They lose energy and settle into fixed positions in an orderly arrangement."),
      ("condensation", "They lose energy, slow down and come close together to form a liquid."),
      ("expansion of a solid", "They vibrate more strongly and move slightly further apart."),
      ("contraction of a gas", "They move more slowly and come closer together.")]


def g_pc():
    c, a = R.choice(PC)
    if not once(("pc", c)):
        return None
    return item("Which describes what happens to the particles during %s?" % c, a, R.sample([x[1] for x in PC if x[0] != c], 3), "This is how the particle model explains %s." % c)


OBJS = ["copper block", "steel rod", "aluminium ring", "glass marble", "brass key"]


def g_cons():
    o = R.choice(OBJS)
    m = R.choice([40, 60, 80, 120, 150, 250])
    k = R.choice(["mass", "dens", "vol"])
    if not once(("cs", o, k)) or not once(("csm", m, k)):
        return None
    q = "A %d g %s is heated and expands. " % (m, o)
    if k == "mass":
        return item(q + "What is its mass now?", "%d g" % m, ["%d g" % (m + 5), "%d g" % (m - 5), "%d g" % (2 * m)], "No particles are added or removed, so the mass does not change.")
    if k == "dens":
        return item(q + "What happens to its density?", "It decreases, because the same mass takes up a larger volume.", ["It increases, because the particles get bigger.", "It stays the same, because the mass is the same.", "It increases, because the mass increases."],
                    "Density = mass ÷ volume. The volume increases while the mass stays the same.")
    return item(q + "What happens to the size of its particles?", "They stay the same size.", ["They get bigger.", "They get smaller.", "They melt."], "Only the spaces between the particles increase.")


B1 = bank([
    ("What is the particle model of matter?", "All matter is made of tiny particles that are always moving randomly.", ["Matter is one solid piece.", "Only gases are made of particles.", "Particles are only in living things."], "The particles are too small to see."),
    ("Why can a gas be compressed easily but a solid cannot?", "Gas particles are far apart; solid particles are already closely packed.", ["Gas particles are smaller.", "Solid particles are moving faster.", "Solids have no particles."], "There is a lot of space between gas particles."),
    ("Why does a liquid take the shape of its container?", "Its particles can slide past one another.", ["Its particles are fixed in place.", "It has no particles.", "Its particles expand."], "A liquid has a fixed volume but no fixed shape."),
    ("What happens to the particles of a solid when it melts?", "They gain energy and move out of their fixed positions.", ["They become larger.", "They stop moving.", "They disappear."], "The solid becomes a liquid."),
    ("When ice melts in a sealed bag, what happens to the total mass?", "It stays the same.", ["It increases.", "It decreases.", "It becomes zero."], "No particles are added or removed: mass is conserved."),
    ("What happens to the particles when a gas is cooled?", "They move more slowly and come closer together.", ["They become smaller.", "They move faster.", "They break apart."], "The gas contracts."),
    ("What did Robert Brown observe that supports the particle model?", "Pollen grains in water jiggled randomly.", ["Ice floated on water.", "Light bent in water.", "Iron rusted in air."], "Invisible water particles hit the pollen grains from all sides."),
    ("Why is the particle model called a model?", "It is a simple way to explain how matter behaves, based on evidence.", ["It is a toy.", "It is a photograph of particles.", "It cannot be changed."], "Models are improved when new evidence appears."),
])
B5 = bank([
    ("A metal ball just fits through a ring. After the ball is heated, it cannot pass through. Why?", "The ball expanded because its particles moved further apart.", ["The particles of the ball got bigger.", "The ring shrank when the ball was heated.", "The ball gained mass."], "Particles do not change size."),
    ("Why does the smell of cooking spread faster in a hot kitchen than in a cold one?", "Particles move faster at higher temperatures.", ["Hot air has no particles.", "Cold air is denser so smells move faster.", "Smells only spread by wind."], "Diffusion is faster when particles have more energy."),
    ("A syringe of air is sealed and the plunger is pushed in. Why can it move but a syringe full of water cannot?", "Air particles have large spaces between them; water particles are close together.", ["Water has no particles.", "Air particles are larger.", "Water is a solid."], "Liquids are almost incompressible."),
    ("A bottle of perfume is opened in a corner. Why does it take time to smell it across the room?", "Perfume particles collide with air particles and move in random directions.", ["Perfume particles are very heavy.", "Particles only move in straight lines.", "Smell travels like light."], "Diffusion is not instant."),
    ("Why does a balloon left in an air-conditioned room become smaller?", "The air particles inside move more slowly, so the air contracts.", ["Some particles become smaller.", "The balloon gains mass.", "Cold air expands."], "Cooling makes a gas contract."),
    ("Which diagram best represents a liquid?", "particles touching each other but arranged randomly", ["particles far apart and randomly arranged", "particles in neat rows touching each other", "no particles at all"], "Liquid particles are close but not in fixed positions."),
])


def body():
    think = ("<p><b>All matter is made of tiny, discrete particles that are always moving randomly.</b></p>"
             "<ul><li><b>Solid</b>: closely packed, orderly, vibrate in place. <b>Liquid</b>: close, random, slide past each other. <b>Gas</b>: far apart, move fast in all directions.</li>"
             "<li><b>Diffusion</b>: net movement of particles from a higher to a lower concentration. Faster in gases and at higher temperatures.</li>"
             "<li><b>Expansion</b>: on heating, particles move faster and further apart. They do <b>not</b> get bigger.</li>"
             "<li>Mass is conserved in melting, boiling and expansion: no particles are added or lost.</li></ul>")
    ex = [("Why does a metal rod get longer when heated?", ["Particles vibrate more and move further apart"], "The rod expands; the particles stay the same size."),
          ("Ink spreads in still water. Why?", ["Particles move randomly"], "Diffusion from a higher to a lower concentration.")]
    mist = ["Saying particles expand when heated. The spaces between them increase.", "Saying particles in a solid do not move. They vibrate.",
            "Thinking mass increases when a solid melts or expands.", "Thinking diffusion only happens in gases. It happens in liquids too."]
    return lesson(think, ex, mist)


GM = upto(PM.g_mass, 6)


def main():
    sets = U.sets([
        ("Particles in solids, liquids and gases", B1[:3] + [(g_model, 4), (PM.g_state, 6), (PM.g_change, 3), (PM.g_mp, 3), (B1[7], 1)]),
        ("Diffusion", [(g_dif, 6), (g_rate, 3)] + PM.B1[3:6] + [(g_model, 2), (PM.g_state, 2)] + B1[6:7] + PM.B5[:1] + [(PM.g_change, 1), (GM, 1)]),
        ("Expansion and contraction", [(g_exp, 7), (GM, 2), (g_cons, 5)] + B1[5:6] + [(PM.g_change, 3), (g_rate, 3)]),
        ("Melting, boiling and mass", B1[3:5] + [(PM.g_mp, 6), (GM, 1), (PM.g_change, 3), (g_pc, 6), (g_cons, 3), (g_rate, 1)]),
        ("Exam-style questions", B5 + PM.B5[2:] + [(PM.g_mp, 3), (g_exp, 2), (g_dif, 2), (g_rate, 1), (g_cons, 2), (GM, 1)]),
    ])
    make_lss(1, "particulate-nature-of-matter", 7, "Models", "Model of Matter – the Particulate Nature of Matter",
             "Describe matter as made of tiny, discrete particles in constant and random motion; describe the arrangement and movement of particles in solids, liquids and gases; "
             "explain diffusion as the net movement of particles from a region of higher to a region of lower concentration; use the model to explain expansion, contraction, "
             "conservation of mass, melting and boiling (summary of the MOE Lower Secondary Science Syllabus).",
             "Particulate Nature of Matter", seo(1, "Particle Model of Matter"), "Particle model of matter",
             "Free Secondary 1 science worksheets for Singapore students on the particulate nature of matter: solids, liquids and gases, diffusion, expansion and contraction, and melting and boiling. With answers.",
             "Matter is made of tiny moving particles.", "Heating makes particles move faster and further apart, not bigger.",
             body(),
             [("What is diffusion?", "The net movement of particles from a region of higher concentration to a region of lower concentration."),
              ("Why do things expand when heated?", "The particles move faster and further apart, so the substance takes up more space. The particles do not get bigger."),
              ("Does mass change when ice melts?", "No. The particles are the same; only their arrangement changes.")],
             sets)


if __name__ == "__main__":
    main()
