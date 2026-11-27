# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U05: kinetic and potential energy, energy transfers and transformations, energy
conservation and efficiency, and renewable and non-renewable energy sources in Australia.
  python tools/gen_au_science_y8_energy_transfers_and_transformations.py
Reuses the US Grade 8 kinetic, potential and energy-transfer makers, the UK Year 8 energy makers and the SG Secondary 2 energy
makers with Australian names, plus own questions on Snowy Hydro, rooftop solar and wind farms.
Wrong answers come from real mistakes: thinking energy is used up, thinking kinetic energy doubles when speed doubles, and calling
heat lost to the surroundings "destroyed".
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

KE = "gen_us_science_g8_kinetic_energy"
PE = "gen_us_science_g8_potential_energy"
ET = "gen_us_science_g8_energy_transfer_and_motion"
E8 = "gen_uk_science_y8_energy_and_power"
S2 = "gen_sg_science_s2_energy_and_work_done"
k_calc = limit(src(KE, "g_calc"), 4)
k_scale = limit(src(KE, "g_scale"), 3)
k_b1 = src.B(KE, "B1")
k_b5 = src.B(KE, "B5")
p_calc = limit(src(PE, "g_calc"), 4)
p_trans = limit(src(PE, "g_trans"), 3)
p_b1 = src.B(PE, "B1")
p_b5 = src.B(PE, "B5")
t_bounce = limit(src(ET, "g_bounce"), 3)
t_dir = limit(src(ET, "g_dir"), 4)
t_b1 = src.B(ET, "B1")
e_eff = limit(src(E8, "g_eff"), 4)
e_store = src(E8, "g_store")
e_res = src(E8, "g_res")
e_b5 = src.B(E8, "B5")
s_cons = limit(src(S2, "g_cons"), 3)
s_conv = src(S2, "g_conv")
s_form = src(S2, "g_form")
s_b1 = src.B(S2, "B1")

POOL1 = pool(R, [
    ("What is the law of conservation of energy?", "Energy cannot be created or destroyed, only transferred or transformed.", ["Energy is used up when things move.", "Energy is made by machines.", "Energy disappears as heat."], "Wasted energy spreads into the surroundings."),
    ("What is kinetic energy?", "the energy of a moving object", ["energy stored because of height", "energy stored in food", "energy of a still object"], "Faster or heavier objects have more kinetic energy."),
    ("What is gravitational potential energy?", "energy stored because an object is raised above the ground", ["energy of a moving object", "energy in a battery", "energy of sound"], "Higher and heavier objects store more."),
    ("A car's speed doubles. What happens to its kinetic energy?", "It becomes four times as big.", ["It doubles.", "It stays the same.", "It halves."], "Kinetic energy depends on speed squared."),
    ("Why is a light globe never 100% efficient?", "Some electrical energy is transferred as heat, not light.", ["Energy is destroyed.", "Light globes make energy.", "Light has no energy."], "Useful output is always less than input."),
    ("What energy transformation happens at the Snowy Hydro power stations?", "gravitational potential energy of water → kinetic energy → electrical energy", ["electrical → chemical energy", "light → sound energy", "heat → chemical energy"], "Falling water spins turbines."),
    ("Which energy source is renewable?", "wind", ["coal", "natural gas", "oil"], "Renewable sources are replaced naturally."),
    ("Why are many Australian homes installing rooftop solar panels?", "Sunlight is a renewable source and reduces the need for coal-fired electricity.", ["Solar panels work best at night.", "Solar panels burn coal.", "They make houses cooler only."], "Australia has lots of sunshine."),
    ("A ball is dropped. What happens to its energy as it falls?", "Gravitational potential energy is transformed into kinetic energy.", ["Kinetic energy turns into potential energy.", "Its energy is destroyed.", "It gains chemical energy."], "It speeds up as it falls."),
    ("Where does a bouncing ball's 'lost' energy go?", "It is transferred to the surroundings as heat and sound.", ["It is destroyed.", "It stays in the ball forever.", "It turns into mass."], "Energy is conserved but dissipated."),
])
POOL5 = pool(R, [
    ("Mia drops a ball from 100 cm and measures bounces of 70, 49 and 34 cm. What pattern does she see?", "Each bounce is about 70% of the one before.", ["Each bounce is the same height.", "Each bounce is higher.", "The bounces get 30 cm higher each time."], "About 30% of the energy is transferred away each bounce."),
    ("Jack rolls a trolley down a ramp from different heights and measures its speed at the bottom. What is the independent variable?", "the starting height", ["the speed at the bottom", "the mass of the trolley", "the ramp surface"], "He changes the height."),
    ("A kettle uses 2000 J of electrical energy and 1600 J heats the water. What is its efficiency?", "80%", ["20%", "1600%", "40%"], "Efficiency = useful output ÷ input × 100 = 1600 ÷ 2000 × 100."),
    ("Ruby says a car 'uses up' energy. How could she say this more accurately?", "The car transforms chemical energy in fuel into kinetic energy and heat.", ["The car destroys energy.", "The car makes energy.", "Fuel has no energy."], "Energy changes form."),
    ("Kai designs a marble run. How could he make the marble go faster at the bottom?", "start it higher", ["start it lower", "use a lighter colour", "make the track rougher"], "More height gives more potential energy to transform."),
    ("Which change would make a pendulum lose energy more slowly?", "reduce air resistance and friction at the pivot", ["make it swing in water", "add sandpaper to the pivot", "use a heavier string only"], "Less energy is dissipated."),
])


def main():
    sets = U.sets([
        ("Forms of energy", [(POOL1, 5), (s_form, 6), (e_store, 5), (k_b1, 2), (p_b1, 2)]),
        ("Kinetic and potential energy", [(k_calc, 4), (k_scale, 3), (p_calc, 4), (p_trans, 3), (POOL1, 3), (s_cons, 3)]),
        ("Transfers and transformations", [(s_conv, 6), (t_dir, 4), (t_bounce, 3), (t_b1, 4), (s_b1, 3)]),
        ("Efficiency and energy sources", [(e_eff, 4), (e_res, 6), (POOL1, 2), (e_b5, 4), (s_b1, 2), (s_form, 2)]),
        ("Investigations", [(POOL5, 6), (k_b5, 4), (p_b5, 4), (t_b1, 2), (e_res, 2), (s_conv, 2)]),
    ])
    make_au(YEAR, "energy-transfers-and-transformations", SORT, "AC9S8U05", "Physical sciences",
            "Investigate the transfer and transformation of energy, including kinetic and potential energy, and use energy flow diagrams to "
            "show that energy is conserved (summary of the Australian Curriculum v9.0 Science content description).",
            "Energy Transfers and Transformations", "Energy transfers",
            "Free Year 8 science worksheets on energy: kinetic and potential energy, transfers and transformations, conservation of energy, "
            "efficiency, and renewable energy in Australia. 100 questions with answers.",
            "Energy is never used up, only changed.", "Energy transforms from one form to another; some is always dissipated as heat.",
            "<p><b>Energy cannot be created or destroyed; it is transferred or transformed.</b></p><ul>"
            "<li>Kinetic energy: moving objects (more mass or speed, more energy; doubling speed gives four times the energy).</li>"
            "<li>Gravitational potential energy: raised objects. Falling transforms it into kinetic energy.</li>"
            "<li>Efficiency = useful energy out ÷ energy in × 100%. The rest is dissipated, mostly as heat.</li></ul>",
            [("A kettle: 2000 J in, 1600 J heats water. Efficiency?", ["1600 ÷ 2000 = 0.8"], "80%"),
             ("A dropped ball: which energy increases?", ["it speeds up"], "kinetic")],
            ["Thinking energy is used up.", "Thinking kinetic energy doubles when speed doubles (it is four times).",
             "Calling heat lost to the surroundings 'destroyed' energy."],
            [("What is the difference between energy transfer and transformation?", "A transfer moves energy from one object to another, such as heat from a stove to a pan. A transformation changes it from one form to another, such as chemical to kinetic energy."),
             ("Why are machines never 100% efficient?", "Some energy is always transferred to the surroundings as heat or sound because of friction and resistance."),
             ("How does Snowy Hydro make electricity?", "Water stored high in the mountains has gravitational potential energy. As it falls through pipes it spins turbines that drive generators.")],
            sets)


if __name__ == "__main__":
    main()
