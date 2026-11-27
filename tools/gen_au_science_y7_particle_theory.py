# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 7, AC9S7U05: the particle theory explains the properties of solids, liquids and gases,
changes of state, diffusion, expansion and contraction, and why mass is conserved.
  python tools/gen_au_science_y7_particle_theory.py
Reuses the UK Year 7 particle makers and the SG Secondary 1 particulate-nature makers with Australian names, plus the AU Year 5
particle diagrams. Wrong answers come from real mistakes: thinking particles themselves expand when heated, thinking particles
stop moving in a solid, and thinking mass is lost when a substance melts or evaporates in a sealed container.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 7, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

P7 = "gen_uk_science_y7_particles_and_states_of_matter"
S1 = "gen_sg_science_s1_particulate_nature_of_matter"
p_change = src(P7, "g_change")
p_dens = limit(src(P7, "g_dens"), 2)
p_mass = limit(src(P7, "g_mass"), 2)
p_mp = limit(src(P7, "g_mp"), 5)
p_state = src(P7, "g_state")
p_b1 = src.B(P7, "B1")
p_b5 = src.B(P7, "B5")
s_cons = src(S1, "g_cons")
s_dif = src(S1, "g_dif")
s_exp = src(S1, "g_exp")
s_model = src(S1, "g_model")
s_pc = src(S1, "g_pc")
s_rate = src(S1, "g_rate")
s_b1 = src.B(S1, "B1")
s_b5 = src.B(S1, "B5")
y5_box = src.mod("gen_au_science_y5_solids_liquids_and_gases").g_box

POOL1 = pool(R, [
    ("What does the particle theory say about all matter?", "It is made of tiny particles that are always moving.", ["It is made of one solid piece.", "Its particles only move when heated.", "Only gases are made of particles."], "Particles have spaces between them and attract each other."),
    ("When a solid is heated, what happens to its particles?", "They vibrate faster and move slightly further apart.", ["They get bigger.", "They stop moving.", "They melt into smaller particles."], "The particles do not change size; the spaces grow."),
    ("Why do railway lines have small gaps between sections?", "The steel expands on hot days and needs room.", ["to let water drain", "to save steel", "to make a noise"], "Particles move further apart when heated."),
    ("Why does a smell from a barbecue spread across a park?", "Gas particles move randomly and spread out (diffusion).", ["The smell is pushed by light.", "Particles grow bigger.", "Smells only travel on hot days."], "Diffusion is faster in gases than in liquids."),
    ("What is diffusion?", "the spreading of particles from where there are many to where there are few", ["particles joining together", "a solid melting", "a liquid freezing"], "It happens because particles move randomly."),
    ("Why can a gas be compressed but a liquid hardly can?", "Gas particles have large spaces between them.", ["Liquid particles are bigger.", "Gas particles are smaller than liquid particles.", "Liquids have no particles."], "Pushing the particles closer is easy in a gas."),
    ("What happens to the particles when water boils?", "They gain enough energy to move far apart and escape as a gas.", ["They break into smaller pieces.", "They stop moving.", "They get heavier."], "The particles themselves stay the same."),
    ("Ice melts in a sealed bag. What happens to the mass?", "It stays the same.", ["It decreases.", "It increases.", "It becomes zero."], "No particles are added or lost."),
    ("Why does a balloon shrink on a cold night?", "The air particles move more slowly and the gas contracts.", ["Air escapes through the rubber.", "The particles shrink.", "Cold air pushes it from inside."], "Slower particles hit the walls less hard."),
    ("Which state has particles in fixed positions that vibrate?", "solid", ["liquid", "gas", "none"], "Solids keep their shape."),
])
POOL5 = pool(R, [
    ("Mia puts a drop of food colouring in cold, warm and hot water. Which spreads fastest?", "the hot water", ["the cold water", "the warm water", "all the same"], "Particles move faster at higher temperatures."),
    ("In Mia's test, what should stay the same?", "the size of the drop, the amount of water and the containers", ["the temperature", "nothing", "the time it takes"], "Change only the temperature."),
    ("Jack heats a metal ball that just fits through a ring. After heating it will not pass through. Why?", "The ball expanded as its particles moved further apart.", ["The particles grew bigger.", "The ring shrank in the heat.", "The ball gained mass."], "Heat makes most solids expand."),
    ("Ruby weighs a sealed bottle of water (520 g), freezes it, then weighs it again. What will the scale show?", "520 g", ["more than 520 g", "less than 520 g", "0 g"], "Mass is conserved in a change of state."),
    ("Kai measures the temperature of melting ice every minute: 0, 0, 0, 0 °C, then 2, 5 °C. Why did it stay at 0 °C at first?", "The energy was being used to melt the ice.", ["The thermometer was broken.", "The ice was cooling.", "Heat stopped flowing."], "Temperature stays steady during a change of state."),
    ("Ella says particles in a hot spoon are bigger. How could you explain the real reason the spoon expands?", "The particles move more and take up more space, but stay the same size.", ["The particles really do get bigger.", "New particles are made.", "The spoon gains mass."], "Spacing changes, not particle size."),
])


def main():
    sets = U.sets([
        ("The particle theory", [(POOL1, 5), (s_model, 5), (p_b1, 5), (y5_box, 5)]),
        ("Changes of state", [(p_change, 5), (s_pc, 5), (p_mp, 5), (p_state, 3), (POOL1, 2)]),
        ("Diffusion", [(s_dif, 5), (s_rate, 5), (s_b1, 5), (POOL1, 3), (p_b1, 2)]),
        ("Expansion and mass", [(s_exp, 7), (s_cons, 5), (p_mass, 3), (p_dens, 2), (y5_box, 3)]),
        ("Investigations", [(POOL5, 6), (p_b5, 4), (s_b5, 5), (s_cons, 2), (p_state, 3)]),
    ])
    make_au(YEAR, "particle-theory", SORT, "AC9S7U05", "Chemical sciences",
            "Use particle theory to describe the arrangement of particles in a substance, including the motion of and attraction between "
            "particles, and relate this to the properties of the substance (summary of the Australian Curriculum v9.0 Science content description).",
            "Particle Theory", "Particle theory",
            "Free Year 7 science worksheets on the particle theory: solids, liquids and gases, changes of state, diffusion, expansion and "
            "conservation of mass. 100 questions with answers.",
            "All matter is made of moving particles.", "How close particles are and how fast they move explain each state and change.",
            "<p><b>The particle theory: all matter is made of tiny particles that are always moving and attract each other.</b></p><ul>"
            "<li>Solid: particles packed in fixed positions, vibrating. Liquid: close together but moving past each other. Gas: far apart, moving fast.</li>"
            "<li>Heating gives particles more energy: they move faster and further apart, so substances expand, melt or boil.</li>"
            "<li>Particles do not change size and are not lost in a change of state, so mass stays the same.</li></ul>",
            [("Why does a smell spread through a room?", ["gas particles move randomly", "they spread from high to low concentration"], "diffusion"),
             ("Ice melts in a sealed bag. Mass?", ["no particles are added or lost"], "unchanged")],
            ["Thinking particles themselves expand when heated.", "Thinking particles in a solid do not move.",
             "Thinking mass is lost when a substance melts or evaporates in a sealed container."],
            [("What is the particle theory?", "It is a model that says all matter is made of tiny particles that are always moving, have spaces between them and attract each other."),
             ("Why do substances expand when heated?", "The particles gain energy, move faster and take up more space. The particles themselves stay the same size."),
             ("Why is diffusion faster in gases?", "Gas particles move faster and have more space between them, so they spread out quickly.")],
            sets)


if __name__ == "__main__":
    main()
