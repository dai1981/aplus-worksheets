# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 7: Kinetic Particle Model of Matter
  python tools/gen_sg_science_s3_kinetic_particle_model_of_matter.py
The arrangement, spacing, motion and forces of particles in solids, liquids and gases; how temperature is linked to the average
kinetic energy of the particles; Brownian motion as evidence for moving particles; gas pressure from particles hitting the
walls; how pressure, volume and temperature of a fixed mass of gas affect each other (qualitatively).
UK and SG particle-model makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "particles in a solid do not move", "particles expand when heated", "gas pressure is
caused by particles hitting each other", "the smoke particles in Brownian motion are alive".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto

LV, SUBJ, SORT = 3, "Physics", 7
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_state = src("gen_uk_science_y7_particles_and_states_of_matter", "g_state")
uk_mp = src("gen_uk_science_y7_particles_and_states_of_matter", "g_mp")
sg_dif = src("gen_sg_science_s1_particulate_nature_of_matter", "g_dif")
sg_exp = src("gen_sg_science_s1_particulate_nature_of_matter", "g_exp")

PROP = [("Particles are closely packed in a regular pattern.", "solid"), ("Particles only vibrate about fixed positions.", "solid"),
        ("It has a fixed shape and a fixed volume.", "solid"), ("The forces of attraction between particles are strongest.", "solid"),
        ("Particles are closely packed but in a random arrangement.", "liquid"), ("Particles slide past one another.", "liquid"),
        ("It has a fixed volume but takes the shape of its container.", "liquid"),
        ("Particles are far apart in a random arrangement.", "gas"), ("Particles move randomly at high speeds in all directions.", "gas"),
        ("It has no fixed shape or volume and fills its container.", "gas"), ("It can be compressed easily because there is a lot of space between particles.", "gas"),
        ("The forces of attraction between particles are negligible.", "gas")]


def g_prop():
    q, a = R.choice(PROP)
    return tq("Which state of matter is described? “%s”" % q, a, [x for x in ("solid", "liquid", "gas") if x != a] + ["all three states"],
              "Solid: close, regular, vibrate. Liquid: close, random, slide past each other. Gas: far apart, random, fast.")


PRES = [("A sealed can of gas is heated.", "increases", "The particles move faster, so they hit the walls more often and with more force."),
        ("A bicycle pump's outlet is blocked and the piston is pushed in slowly (constant temperature).", "increases", "The same particles are in a smaller volume, so they hit the walls more often."),
        ("More air is pumped into a car tyre (volume and temperature stay the same).", "increases", "More particles hit the walls each second."),
        ("A sealed syringe of air is put in a fridge.", "decreases", "The particles move more slowly, so they hit the walls less often and with less force."),
        ("The plunger of a sealed syringe of air is pulled out slowly (constant temperature).", "decreases", "The particles are spread over a larger volume, so they hit the walls less often."),
        ("Some air is let out of a basketball (volume and temperature stay the same).", "decreases", "Fewer particles hit the walls each second."),
        ("A sealed balloon of air is left in the hot sun.", "increases", "The particles gain kinetic energy and hit the walls harder and more often, and the balloon expands."),
        ("A sealed metal tin of air is moved from a warm room into cold water.", "decreases", "The particles slow down and hit the walls less often and with less force.")]


def g_pres():
    q, a, why = R.choice(PRES)
    if R.random() < 0.5:
        return tq(q + " What happens to the pressure of the gas?", "It %s." % a, ["It %s." % ("decreases" if a == "increases" else "increases"), "It stays the same.", "It becomes zero."], why)
    wrong = ["The particles themselves get bigger.", "The particles hit each other more often, not the walls.", "The mass of each particle changes."]
    return tq(q + " Why does the pressure %s?" % a[:-1], why, wrong, "Gas pressure comes from particles colliding with the walls of the container.")


TEMP = [("What happens to the particles of a gas when its temperature rises?", "They move faster: their average kinetic energy increases.", ["They get bigger.", "They stop moving.", "They get heavier."]),
        ("What happens to the particles of a solid when it is heated (but does not melt)?", "They vibrate more vigorously about their fixed positions.", ["They start to flow.", "They expand.", "They stop vibrating."]),
        ("Why does a metal rod expand when it is heated?", "The particles vibrate more and move slightly further apart.", ["Each particle expands.", "New particles are made.", "The particles become lighter."]),
        ("What does the temperature of a substance measure?", "the average kinetic energy of its particles", ["the total number of particles", "the size of the particles", "the mass of the substance"]),
        ("Why is a gas easy to compress?", "There are large spaces between its particles.", ["Its particles are soft.", "Its particles shrink.", "It has no particles."]),
        ("Why is a liquid hard to compress?", "Its particles are already close together.", ["Its particles do not move.", "It has strong forces like a solid in a regular pattern.", "It has no mass."]),
        ("Why can a liquid flow?", "Its particles can slide past one another.", ["Its particles are far apart.", "Its particles are fixed.", "It has no forces between particles."]),
        ("Why does a solid have a fixed shape?", "Strong forces hold its particles in fixed positions.", ["Its particles do not move at all.", "Its particles are far apart.", "Its particles are larger."])]


def g_temp():
    q, a, w = R.choice(TEMP)
    return tq(q, a, w, "The kinetic particle model: all matter is made of tiny particles in constant random motion.")


def g_rank():
    k = R.choice(["space", "forces", "speed", "compress"])
    if k == "space":
        return tq("Put the states in order of the spacing between particles, from smallest to largest.", "solid, liquid, gas", ["gas, liquid, solid", "liquid, solid, gas", "solid, gas, liquid"],
                  "Gas particles are much further apart than in solids and liquids.")
    if k == "forces":
        return tq("Put the states in order of the forces of attraction between particles, from strongest to weakest.", "solid, liquid, gas", ["gas, liquid, solid", "liquid, solid, gas", "liquid, gas, solid"],
                  "The forces are strongest in solids and negligible in gases.")
    if k == "speed":
        return tq("At the same temperature, in which state do the particles move fastest and most freely?", "gas", ["solid", "liquid", "the particles all move at the same speed"],
                  "Gas particles move randomly at high speed.")
    return tq("Which state of matter is easiest to compress?", "gas", ["solid", "liquid", "they are all equally easy"], "Gas particles have large spaces between them.")


ASP = {"solid": {"arranged": "closely packed in a regular pattern", "moving": "vibrating about fixed positions", "attracted": "very strong forces of attraction"},
       "liquid": {"arranged": "closely packed in a random arrangement", "moving": "sliding past one another", "attracted": "strong forces of attraction, but weaker than in a solid"},
       "gas": {"arranged": "far apart in a random arrangement", "moving": "moving randomly at high speed", "attracted": "negligible forces of attraction"}}
QA = {"arranged": "How are the particles arranged in %s?", "moving": "How do the particles move in %s?", "attracted": "What are the forces between the particles in %s like?"}


def g_aspect():
    st = R.choice(list(ASP))
    k = R.choice(list(QA))
    a = ASP[st][k]
    wr = [ASP[x][k] for x in ASP if x != st] + [{"arranged": "spread out in a regular pattern", "moving": "not moving at all",
                                                  "attracted": "no forces at all, even when touching"}[k]]
    return tq(QA[k] % ("a " + st if st != "gas" else "a gas"), a, wr, "In a %s the particles are %s, %s, with %s." % (st, ASP[st]["arranged"], ASP[st]["moving"], ASP[st]["attracted"]))


CHG = [("melting", "solid to liquid", "Particles gain energy and break free from fixed positions."), ("freezing", "liquid to solid", "Particles lose energy and settle into fixed positions."),
       ("boiling", "liquid to gas, throughout the liquid at a fixed temperature", "Particles gain enough energy to escape the forces between them."),
       ("evaporation", "liquid to gas, at the surface only, at any temperature", "The most energetic particles escape from the surface."),
       ("condensation", "gas to liquid", "Particles lose energy and come closer together."), ("sublimation", "solid directly to gas", "Particles escape straight from the solid.")]
g_chg = rows(R, CHG, "What is %s?", "What is the name for a change of %s?")


POOL1 = pool(R, [
    ("What is Brownian motion?", "the random, jerky movement of small particles (such as smoke) seen under a microscope", ["the motion of air particles you can see", "the steady flow of a liquid", "the vibration of a solid"], "Evidence that particles of air or water are moving."),
    ("In a smoke cell, what causes the smoke particles to move randomly?", "They are hit unevenly by fast-moving, invisible air particles.", ["They are alive.", "They are heated by the light.", "They repel each other."], "The air particles are too small to see."),
    ("Why do smoke particles move more quickly when the air is warmer?", "The air particles move faster and hit them harder.", ["The smoke particles expand.", "The light is brighter.", "The smoke is lighter."], "Temperature raises kinetic energy."),
    ("Why are the moving air particles in Brownian motion not seen?", "They are far too small to see with a microscope.", ["They are transparent.", "They move too slowly.", "They do not exist."], "Only the larger smoke particles are visible."),
    ("What causes the pressure of a gas in a container?", "particles colliding with the walls of the container", ["particles colliding with each other", "the weight of the container", "particles sticking to the walls"], "Each collision exerts a force on the wall."),
    ("Which observation is evidence that particles move?", "diffusion of a smell through a room", ["a stone sinking in water", "ice floating", "a magnet attracting iron"], "Particles spread from high to low concentration."),
    ("What is diffusion?", "the net movement of particles from a region of high concentration to a region of low concentration", ["the movement of particles from low to high concentration", "a liquid turning into a gas", "particles getting bigger"], "Caused by random particle motion."),
    ("Why does diffusion happen faster in a gas than in a liquid?", "Gas particles move faster and have more space between them.", ["Gas particles are bigger.", "Liquids have no particles.", "Gas particles are heavier."], "More space and faster motion."),
])
POOL5 = pool(R, [
    ("The volume of a fixed mass of gas is halved at constant temperature. What happens to its pressure?", "It increases (it doubles).", ["It halves.", "It stays the same.", "It becomes zero."], "Particles hit the walls twice as often."),
    ("A gas in a sealed rigid container is heated. Which quantity does not change?", "the volume", ["the pressure", "the average speed of the particles", "the temperature"], "A rigid container has a fixed volume."),
    ("Why do car tyre pressures rise after a long drive?", "The air inside gets warmer, so its particles move faster and hit the tyre walls more often and harder.", ["The tyre gets smaller.", "Air leaks in.", "The road pushes on the tyre."], "Pressure rises with temperature at fixed volume."),
    ("Why should an aerosol can never be thrown into a fire?", "The gas inside is heated, its pressure rises and the can may explode.", ["The can melts and drips.", "The gas becomes a liquid.", "The pressure falls and it collapses."], "Fixed volume, rising temperature."),
    ("A gas syringe is sealed. Its plunger moves out when the syringe is warmed. Why?", "The particles move faster and push harder on the plunger, so the gas expands until the pressure balances again.", ["The particles get bigger.", "New particles form.", "The plunger is pulled by gravity."], "Gas expands on heating at constant pressure."),
    ("Why does a balloon left in a cold air-conditioned room shrink a little?", "The gas particles slow down, so the gas pressure falls and the balloon contracts.", ["Air particles leak out at once.", "The particles shrink.", "The rubber gets heavier."], "Cooling lowers kinetic energy."),
    ("In which state are the particles held in a regular lattice?", "solid", ["liquid", "gas", "all states"], "Liquids and gases have random arrangements."),
    ("Ice melts into water at 0 °C. What happens to the particles?", "They gain enough energy to break out of their fixed positions and slide past each other.", ["They get bigger.", "They stop moving.", "They split into atoms."], "Melting: solid to liquid."),
])


def main():
    sets = U.sets([
        ("Solids, liquids and gases", [(g_prop, 9), (g_rank, 4), (uk_state, 4), (g_temp, 3)]),
        ("Particles and temperature", [(g_temp, 6), (g_aspect, 6), (uk_mp, 3), (g_rank, 2), (sg_exp, 3)]),
        ("Brownian motion and diffusion", [POOL1, (sg_dif, 5), (g_chg, 5), (g_aspect, 2)]),
        ("Gas pressure", [(g_pres, 14), POOL1, (POOL5, 3)]),
        ("Exam-style questions", [(POOL5, 8), (g_pres, 3), (g_chg, 4), (uk_mp, 3), (sg_exp, 2)]),
    ])
    make_ol(LV, SUBJ, "kinetic-particle-model-of-matter", SORT, "Kinetic Particle Model of Matter",
            "Compare the properties of solids, liquids and gases; describe qualitatively the molecular structure of solids, liquids and gases in terms of the arrangement, "
            "separation and motion of the particles and the forces between them; infer from Brownian motion that particles are in constant random motion; relate the rise "
            "in temperature of a body to an increase in the average kinetic energy of its particles; explain the pressure of a gas in terms of particles colliding with "
            "the walls, and describe qualitatively the effect of changing temperature and volume on the pressure of a fixed mass of gas (summary of the "
            "Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Kinetic Particle Model of Matter", "Particle model",
            "Free Secondary 3 O-Level Physics worksheets on the kinetic particle model of matter: solids, liquids and gases, temperature and kinetic energy, Brownian motion, "
            "diffusion and gas pressure. 100 questions with answers.",
            "All matter is made of moving particles.", "Gas pressure comes from particles hitting the walls.",
            "<p><b>All matter is made of tiny particles in constant random motion.</b></p><ul>"
            "<li>Solid: close, regular, vibrate about fixed positions, strong forces. Liquid: close, random, slide past each other. Gas: far apart, random, fast, negligible forces.</li>"
            "<li>A higher temperature means a higher average kinetic energy of the particles.</li>"
            "<li>Brownian motion: visible smoke particles jiggle because invisible air particles hit them unevenly.</li>"
            "<li>Gas pressure: particles hit the walls. Hotter gas or smaller volume means more frequent (and harder) collisions, so higher pressure.</li></ul>",
            [("A sealed tin of air is heated. Pressure?", ["particles move faster", "more frequent, harder collisions with the walls"], "increases"),
             ("A syringe of air is pushed in at constant temperature. Pressure?", ["same particles, smaller volume", "more collisions per second"], "increases")],
            ["Thinking the particles themselves expand when heated. They move faster and further apart.",
             "Saying gas pressure is caused by particles hitting each other. It is caused by particles hitting the walls.",
             "Saying particles in a solid do not move. They vibrate.", "Thinking the smoke particles in Brownian motion move by themselves."],
            [("What is the kinetic particle model of matter?", "The idea that all matter is made of tiny particles that are always moving randomly; their arrangement and motion explain the properties of solids, liquids and gases."),
             ("What does Brownian motion show?", "That air (or water) particles are moving randomly, because they knock the visible smoke particles about in a random, jerky way."),
             ("Why does the pressure of a gas rise when it is heated in a closed container?", "The particles gain kinetic energy and move faster, so they hit the walls more often and with greater force.")],
            sets)


if __name__ == "__main__":
    main()
