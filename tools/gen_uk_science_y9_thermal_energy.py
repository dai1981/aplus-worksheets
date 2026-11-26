# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Thermal Energy and Heat Transfer
  python tools/gen_uk_science_y9_thermal_energy.py
Temperature and thermal energy, heating and thermal equilibrium (the hotter object cools, the cooler one warms),
conduction, convection and radiation, conductors and insulators, insulating homes, and comparing how fast objects heat
and cool. Reuses the thermal-energy and heat-transfer questions of the US Grade 6 units in British English.
Wrong answers come from real mistakes: "cold flows into things", "temperature and thermal energy are the same",
"radiation needs particles", "metal feels cold because it is colder".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61911)
R = U.R
P = People(R)
uk_sci.USED.clear()
TE = adopt_us("gen_us_science_g6_thermal_energy_and_temperature", U)
DH = adopt_us("gen_us_science_g6_designing_to_control_heat_transfer", U)
us_energy, us_mass, us_mat, us_te = ukm(TE.g_energy), ukm(TE.g_mass), ukm(TE.g_material), ukm(TE.g_te)
us_ex, us_kind, us_dmat, us_test = ukm(DH.g_example), ukm(DH.g_kind), ukm(DH.g_material), ukm(DH.g_test)


def g_cool():
    who = P.next()[0]
    t0 = R.choice([80, 85, 90, 95])
    room = R.choice([18, 20, 22])
    drops = [0, R.choice([14, 16, 18]), R.choice([24, 26, 28]), R.choice([32, 34, 36])]
    vals = [t0 - d for d in drops]
    k = R.choice(["first", "why", "final", "pattern", "lid"])
    if not once(("co", t0, tuple(drops), k)) or not once(("co", k), 2 if k in ("why", "final", "pattern", "lid") else 10):
        return None
    tab = table(["Time (min)", "Temperature of tea (°C)"], [[str(t), str(v)] for t, v in zip([0, 5, 10, 15], vals)])
    intro = tab + "%s left a cup of tea to cool in a room at %d °C. " % (who, room)
    if k == "first":
        d = drops[1]
        return item(intro + "By how much did the temperature fall in the first 5 minutes?", "%d °C" % d, uniq("%d °C" % d, ["%d °C" % vals[1], "%d °C" % (drops[2] - drops[1]), "%d °C" % drops[3], "5 °C"]), "%d − %d = %d." % (vals[0], vals[1], d))
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The tea cools fastest at first, then more slowly.", ["It cools at the same rate all the time.", "It cools slowest at first.", "It warms up."], "The difference from room temperature gets smaller.")
    if k == "why":
        return item(intro + "Why does the tea cool down?", "Energy is transferred from the hot tea to the cooler surroundings.", ["Cold flows into the tea.", "The tea loses its temperature into the cup only.", "The tea makes cold."], "Hot to cold.")
    if k == "final":
        return item(intro + "What temperature will the tea reach after a very long time?", "%d °C (room temperature)" % room, ["0 °C", "%d °C" % vals[3], "%d °C" % (room - 10)], "Thermal equilibrium with the room.")
    return item(intro + "How could the tea be kept hot for longer?", "put a lid on it and use an insulated cup", ["stir it in a metal cup", "put it by an open window", "pour it into a wide, shallow dish"], "Reduce heat transfer.")


WAY = [("A metal spoon in hot soup gets hot at the handle.", "conduction"), ("Warm air rises above a radiator and cool air sinks.", "convection"),
       ("You feel warm sitting in sunshine.", "radiation"), ("A pan of water heats up from the bottom as hot water rises.", "convection"),
       ("You feel the heat from a bonfire on your face.", "radiation"), ("Your hand warms up holding a mug of hot chocolate.", "conduction"),
       ("Energy from the Sun reaches the Earth across empty space.", "radiation"), ("A sea breeze blows towards land on a sunny day.", "convection")]


def g_way():
    s, a = R.choice(WAY)
    if not once(("wa", s)):
        return None
    return item("%s Which type of heat transfer is this mainly?" % s, a, [x for x in ["conduction", "convection", "radiation", "evaporation only"] if x != a],
                "Conduction: through solids by particles vibrating. Convection: in liquids and gases as warm fluid rises. Radiation: infrared waves, even through a vacuum.")


B1 = bank([
    ("What is the difference between temperature and thermal energy?", "Temperature measures how hot something is; thermal energy also depends on how much material there is.", ["They are the same thing.", "Thermal energy is measured in °C.", "Temperature is measured in joules."], "A bath at 40 °C has more thermal energy than a cup at 90 °C."),
    ("In which direction is energy transferred when two objects touch?", "from the hotter object to the cooler one", ["from the cooler object to the hotter one", "both ways equally", "it is not transferred"], "Until they reach the same temperature."),
    ("What is thermal equilibrium?", "when objects reach the same temperature and there is no net energy transfer", ["when an object is boiling", "when an object is frozen", "when energy is created"], "No more change."),
    ("Why does a metal bench feel colder than a wooden one on the same day?", "Metal conducts energy away from your hand faster.", ["The metal is colder.", "Wood is warmer than the air.", "Metal makes cold."], "Both are the same temperature."),
    ("Why can radiation travel through space but conduction cannot?", "Radiation is a wave and needs no particles; conduction needs particles.", ["Space is full of particles.", "Conduction is faster.", "Radiation needs air."], "Infrared."),
])
B5 = bank([
    ("Why does loft insulation reduce heating bills?", "It traps air, a poor conductor, so less energy escapes through the roof.", ["It heats the house.", "It reflects the Sun in.", "It conducts heat well."], "Insulation."),
    ("Why do double-glazed windows keep homes warmer?", "The gap between the panes reduces conduction.", ["The glass is thicker so heat is created.", "They let in more cold.", "They conduct heat well."], "Gas or vacuum layer."),
    ("Why are radiators often placed under windows?", "Convection currents spread the warm air around the room.", ["Windows are warm.", "To heat the glass.", "Convection does not happen."], "Warm air rises."),
    ("Why do houses in hot countries often have white walls?", "White surfaces reflect more radiation, so the house stays cooler.", ["White absorbs more radiation.", "White walls conduct heat away.", "Colour has no effect."], "Light surfaces reflect."),
    ("Why does a vacuum flask keep drinks hot?", "The vacuum stops conduction and convection, and shiny walls reduce radiation.", ["It heats the drink.", "The vacuum makes heat.", "It is made of metal only."], "All three reduced."),
])


def body():
    think = ("<p><b>Energy is transferred from hotter places to cooler places.</b></p>"
             "<ul><li>Temperature (°C) measures how hot something is; thermal energy also depends on the amount of material.</li>"
             "<li>Conduction through solids; convection in liquids and gases; radiation as infrared, even through a vacuum.</li>"
             "<li>Insulators (air, foam, wool) slow heat transfer. Objects cool until they reach the temperature of their surroundings.</li></ul>")
    ex = [("Warm air rising from a heater?", ["A gas moves"], "convection"),
          ("Hot tea in a 20 °C room after hours?", ["Thermal equilibrium"], "20 °C")]
    mist = ["Thinking cold flows into things.", "Mixing up temperature and thermal energy.", "Thinking radiation needs particles."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Temperature and thermal energy", B1 + [(us_te, 6), (us_mass, 5), (us_energy, 4)]),
        ("Conduction, convection, radiation", [(g_way, 7), (us_kind, 9), (us_ex, 4)]),
        ("Cooling down", [(g_cool, 13), (us_energy, 5), (us_mat, 2)]),
        ("Conductors and insulators", [(us_dmat, 10), (us_mat, 6), (us_ex, 4)]),
        ("Keeping warm", B5 + [(us_test, 8), (g_cool, 4), (us_kind, 3)]),
    ])
    make_ks3(9, "thermal-energy", 11, "Physics", "Energy",
             "Heating and thermal equilibrium: temperature difference between two objects leading to energy transfer from the hotter to the cooler one, through contact (conduction) or radiation; such transfers tending to reduce the temperature difference: use of insulators; energy changes on changes of state (qualitative); internal energy stored in materials.",
             "Thermal Energy and Heat Transfer",
             "Year 9 Science: Thermal Energy Worksheets (Conduction, Convection, Radiation)",
             "Thermal Energy",
             "Free Year 9 science worksheets on thermal energy: temperature and thermal energy, conduction, convection and radiation, cooling curves, conductors and insulators, and insulating homes. 100 questions with answers.",
             "Energy moves from hot to cold.",
             "Conduction in solids, convection in fluids, radiation through space.",
             body(),
             [("What is the difference between conduction, convection and radiation?", "Conduction passes energy through solids by vibrating particles. Convection carries energy as warm liquid or gas rises. Radiation transfers energy as infrared waves, even through a vacuum."),
              ("Why do hot drinks cool quickly at first?", "The bigger the temperature difference from the surroundings, the faster energy is transferred, so cooling slows as the drink nears room temperature."),
              ("How do insulators work?", "They are poor conductors, often because they trap air, so they slow down the transfer of energy.")],
             sets)


if __name__ == "__main__":
    main()
