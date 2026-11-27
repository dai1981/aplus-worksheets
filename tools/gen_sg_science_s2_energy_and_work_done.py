# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Application of Forces and Transfer of Energy (energy and work done)
  python tools/gen_sg_science_s2_energy_and_work_done.py
Forms of energy (kinetic, gravitational potential, elastic potential, chemical potential, thermal, light, sound, electrical, nuclear),
energy conversion and the principle of conservation of energy, the joule, work done = force x distance moved in the direction
of the force, and energy sources (renewable and non-renewable; Singapore's natural gas and solar energy).
Wrong answers come from real mistakes: "energy is used up", "holding a heavy box still is doing work",
"work = force / distance", "solar energy is non-renewable".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64202)
R = U.R
P = People(R)
EP = luse(U, "gen_uk_science_y8_energy_and_power", drop=[r"\bstore", r"loft", r"winter", r"radiator", r"gas boiler"])
WM = luse(U, "gen_uk_science_y9_work_and_moments")

FORMS = [("a moving bus", "kinetic energy"), ("a book on a high shelf", "gravitational potential energy"), ("a stretched catapult", "elastic potential energy"),
         ("a compressed spring", "elastic potential energy"), ("a plate of chicken rice", "chemical potential energy"), ("a car battery", "chemical potential energy"),
         ("a cup of hot teh tarik", "thermal energy"), ("a durian falling from a tree", "kinetic energy"), ("water stored behind a dam", "gravitational potential energy"),
         ("petrol in a car's tank", "chemical potential energy"), ("a ringing school bell", "sound energy"), ("a glowing LED", "light energy"),
         ("a hot iron", "thermal energy"), ("a moving MRT train", "kinetic energy"), ("a diver standing on a high board", "gravitational potential energy"),
         ("the wound-up spring of a toy", "elastic potential energy"), ("a charged handphone battery", "chemical potential energy"), ("a camera flash going off", "light energy")]
FALL = ["kinetic energy", "gravitational potential energy", "elastic potential energy", "chemical potential energy", "thermal energy", "sound energy", "light energy"]


def g_form():
    o, a = R.choice(FORMS)
    if not once(("fm", o)):
        return None
    return item("What is the main form of energy in %s?" % o, a, R.sample([x for x in FALL if x != a], 3), "%s has %s." % (o[0].upper() + o[1:], a))


CONV = [("a torch", "chemical potential energy → electrical energy → light energy and thermal energy"), ("an electric fan", "electrical energy → kinetic energy and sound energy"),
        ("a solar panel", "light energy → electrical energy"), ("a person running", "chemical potential energy → kinetic energy and thermal energy"),
        ("a ball falling from a height", "gravitational potential energy → kinetic energy"), ("a catapult firing a stone", "elastic potential energy → kinetic energy"),
        ("a hairdryer", "electrical energy → thermal energy, kinetic energy and sound energy"), ("a gas stove", "chemical potential energy → thermal energy and light energy"),
        ("a loudspeaker", "electrical energy → sound energy"), ("a bicycle dynamo", "kinetic energy → electrical energy"),
        ("a hydroelectric power station", "gravitational potential energy → kinetic energy → electrical energy"),
        ("an electric kettle", "electrical energy → thermal energy"), ("a bow shooting an arrow", "elastic potential energy → kinetic energy of the arrow"),
        ("a microphone", "sound energy → electrical energy"), ("a wind turbine", "kinetic energy of the wind → electrical energy"),
        ("a car's brakes stopping the car", "kinetic energy → thermal energy and sound energy")]


def g_conv():
    d, a = R.choice(CONV)
    if not once(("cv", d)):
        return None
    return item("Which shows the main energy conversion in %s?" % d, a, R.sample([x[1] for x in CONV if x[1] != a and x[0] != d], 3), "The useful output depends on the job of %s." % d)


def g_cons():
    k = R.choice(["fall", "waste", "bounce"])
    e = R.choice([20, 40, 50, 60, 80, 100, 120, 200])
    if not once(("cs", k, e)) or not once(("csk", k), 3 if k == "bounce" else 8):
        return None
    if k == "fall":
        return item("A ball has %d J of gravitational potential energy at the top of a fall. Ignoring air resistance, how much kinetic energy does it have just before it hits the ground?" % e,
                    "%d J" % e, ["0 J", "%d J" % (e // 2), "%d J" % (2 * e)], "Energy is conserved: all the potential energy becomes kinetic energy.")
    if k == "waste":
        u = R.choice([x for x in (10, 20, 30, 40) if x < e])
        return item("A light bulb receives %d J of electrical energy and gives out %d J of light energy. How much energy is converted to thermal energy?" % (e, u), "%d J" % (e - u),
                    ["%d J" % u, "%d J" % e, "%d J" % (e + u)], "Total energy out = total energy in: %d − %d = %d J." % (e, u, e - u))
    b = R.choice([x for x in (e // 4, e // 2, 3 * e // 4) if x > 0])
    return item("A ball dropped with %d J of potential energy bounces back up with %d J. Where did the rest of the energy go?" % (e, b), "It was converted to thermal and sound energy.",
                ["It was destroyed.", "It was stored in the ground forever as potential energy.", "It became new mass in the ball."], "Energy is not destroyed: %d J is converted to thermal and sound energy." % (e - b))


SRC = [("solar energy", "renewable", "It will not run out, but it depends on sunlight."), ("natural gas", "non-renewable", "It takes millions of years to form."),
       ("coal", "non-renewable", "It is a fossil fuel."), ("wind energy", "renewable", "Wind is replaced naturally."), ("crude oil", "non-renewable", "It is a fossil fuel."),
       ("hydroelectric energy", "renewable", "The water cycle replaces the water."), ("biomass such as wood waste", "renewable", "Plants can be regrown."),
       ("tidal energy", "renewable", "Tides are caused by the Moon every day."), ("geothermal energy", "renewable", "Heat from inside the Earth will last a very long time.")]


def g_src():
    s, a, e = R.choice(SRC)
    if not once(("sr", s)):
        return None
    return item("Is %s a renewable or a non-renewable energy source?" % s, a, [x for x in ["renewable", "non-renewable", "neither, because it is not a source of energy", "both"] if x != a], e)


B1 = bank([
    ("What is the SI unit of energy?", "the joule (J)", ["the newton (N)", "the watt (W)", "the kilogram (kg)"], "Work done is also measured in joules."),
    ("What does the principle of conservation of energy state?", "Energy cannot be created or destroyed; it can only be converted from one form to another.", ["Energy is used up when we use it.", "Energy is created in power stations.", "Energy can only be stored."], "The total energy stays the same."),
    ("When is work done?", "when a force moves an object in the direction of the force", ["whenever a force is applied", "when an object is held still", "only when an object falls"], "No movement in the direction of the force means no work done."),
    ("A student holds a 20 N bag still for 5 minutes. How much work is done on the bag?", "0 J", ["100 J", "20 J", "6000 J"], "The bag does not move, so no work is done on it."),
    ("Which formula gives work done?", "work done = force × distance moved in the direction of the force", ["work done = force ÷ distance", "work done = mass × distance", "work done = force + distance"], "1 J = 1 N × 1 m."),
    ("Where does most of Singapore's electricity come from?", "burning natural gas in power stations", ["coal mines in Singapore", "nuclear power stations", "only solar panels"], "Singapore is adding more solar panels on rooftops and reservoirs."),
    ("Why is Singapore installing floating solar panels on reservoirs such as Tengeh Reservoir?", "Singapore has little land, and solar energy is renewable.", ["Solar panels work only on water.", "To heat the reservoir water.", "Because natural gas is renewable."], "This reduces the use of fossil fuels."),
    ("What is the main energy change when a pendulum swings from its highest point to its lowest point?", "gravitational potential energy → kinetic energy", ["kinetic energy → gravitational potential energy", "chemical energy → light energy", "sound energy → kinetic energy"], "At the lowest point it moves fastest."),
])
B5 = bank([
    ("A crane lifts a 2000 N load through a height of 15 m. How much work is done?", "30 000 J", ["133 J", "2015 J", "3000 J"], "Work = 2000 × 15 = 30 000 J."),
    ("A roller coaster car is at the top of a slope. Why can the next hill not be higher than the first?", "Some energy is converted to thermal and sound energy by friction, so the car has less energy.", ["Energy is created on the way down.", "Gravity is weaker on the second hill.", "The car gains mass."], "Energy is conserved, but not all of it stays useful."),
    ("Which is a disadvantage of burning fossil fuels?", "It releases carbon dioxide, which adds to global warming.", ["They are renewable.", "They give out no energy.", "They are only found in Singapore."], "Burning also releases pollutants."),
    ("Why does a car's engine get hot?", "Some chemical energy in the fuel is converted to thermal energy instead of kinetic energy.", ["Energy is created by the engine.", "The engine absorbs sunlight.", "Petrol is hot when it is pumped in."], "This energy is not useful for moving the car."),
    ("A student pushes a box 3 m along the floor with a force of 50 N. How much work does she do?", "150 J", ["16.7 J", "53 J", "50 J"], "Work = 50 × 3 = 150 J."),
    ("Which statement about a bouncing ball is correct?", "It bounces lower each time because energy is converted to thermal and sound energy.", ["It loses energy that is destroyed.", "It bounces higher each time.", "Its energy stays as potential energy."], "Energy spreads to the surroundings."),
])


def body():
    think = ("<p><b>Energy cannot be created or destroyed. It is converted from one form to another.</b></p>"
             "<ul><li>Forms: kinetic, gravitational potential, elastic potential, chemical potential, thermal, light, sound, electrical, nuclear.</li>"
             "<li>Energy and work are measured in <b>joules (J)</b>.</li>"
             "<li><b>Work done = force × distance moved in the direction of the force.</b> No movement, no work.</li>"
             "<li>Renewable sources (solar, wind, hydroelectric) will not run out; fossil fuels (coal, oil, natural gas) will.</li></ul>")
    ex = [("A 40 N force pushes a trolley 5 m. Work done?", ["40 × 5"], "200 J"),
          ("Energy change in a torch?", ["battery → bulb"], "chemical potential → electrical → light and thermal")]
    mist = ["Saying energy is 'used up'. It is converted, often to thermal energy.", "Thinking holding something still is doing work. Nothing moves, so no work is done.",
            "Dividing force by distance. Work done = force × distance.", "Calling solar energy non-renewable."]
    return lesson(think, ex, mist)


AD = [("solar panels", "They give out no carbon dioxide while making electricity.", "They make no electricity at night and less on cloudy days."),
      ("natural gas", "It gives a steady supply of electricity at any time.", "Burning it releases carbon dioxide, a greenhouse gas."),
      ("wind turbines", "The wind is free and will not run out.", "They make little electricity when the wind is weak."),
      ("hydroelectric dams", "They can make electricity whenever it is needed.", "Building the dam floods land and destroys habitats."),
      ("coal", "It is cheap and gives a lot of energy.", "Burning it releases a lot of carbon dioxide and polluting gases."),
      ("nuclear power", "It releases no carbon dioxide while running.", "It produces dangerous radioactive waste.")]


def _res():
    s, adv, dis = R.choice(AD)
    k = R.choice(["a", "d"])
    if not once(("ad", s, k)):
        return None
    a = adv if k == "a" else dis
    pool = [x[2] if k == "a" else x[1] for x in AD if x[0] != s]
    return item("Which is %s of using %s to make electricity?" % ("an advantage" if k == "a" else "a disadvantage", s), a,
                [dis if k == "a" else adv] + R.sample(pool, 2), "Every energy source has advantages and disadvantages.")


GW = upto(WM.g_work, 20)


def main():
    sets = U.sets([
        ("Forms of energy", B1[:2] + [(g_form, 12), (g_conv, 6)]),
        ("Energy conversion", [(g_conv, 6), (g_cons, 8), (EP.B1[1], 1), (g_src, 1), (B1[7], 1), (g_form, 3)]),
        ("Work done", B1[2:5] + WM.B1[:2] + [(GW, 10), (g_cons, 5)]),
        ("Energy sources", B1[5:7] + [(g_src, 9), (_res, 6), (g_conv, 3)]),
        ("Exam-style questions", B5 + [(GW, 5), (g_cons, 5), (g_form, 2), (g_src, 2)]),
    ])
    make_lss(2, "energy-and-work-done", 2, "Interactions", "Application of Forces and Transfer of Energy (Energy and work done)",
             "State the joule as the SI unit of work and energy; identify work done as the energy transferred when an object moves in the direction of a force; infer that energy "
             "can be converted from one form to another and is conserved; show curiosity about the impact of using different energy sources (summary of the MOE Lower Secondary Science Syllabus).",
             "Energy and Work Done", seo(2, "Energy and Work Done"), "Energy and work done",
             "Free Secondary 2 science worksheets for Singapore students on energy: forms of energy, energy conversion, conservation of energy, work done = force × distance and energy sources. With answers.",
             "Energy is converted, never created or destroyed.", "Work done = force × distance (in J).",
             body(),
             [("Is energy used up?", "No. Energy is converted to other forms, often thermal energy that spreads to the surroundings."),
              ("When is work done?", "When a force moves an object in the direction of the force. Work done = force × distance."),
              ("Is natural gas renewable?", "No. It is a fossil fuel that takes millions of years to form.")],
             sets)


if __name__ == "__main__":
    main()
