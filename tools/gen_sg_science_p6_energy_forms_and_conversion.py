# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Energy forms and conversion (Energy)
  python tools/gen_sg_science_p6_energy_forms_and_conversion.py
Forms of energy: kinetic, potential (gravitational, elastic, chemical), light, heat, sound and electrical.
Energy can be converted from one form to another but cannot be created or destroyed. The Sun is the main source of energy
for the Earth: food, fossil fuels and wind all get their energy from the Sun. Using energy wisely.
US Grade 4 energy-conversion questions are reused with Singapore terms (electrical energy, kinetic energy).
Wrong answers come from real mistakes: "energy is used up", "a ball at the top of a slide has no energy",
"a battery stores electrical energy", "food energy comes from the soil", "a stretched rubber band has kinetic energy".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63602)
R = U.R
P = People(R)
REP = [(r"\belectric energy\b", "electrical energy"), (r"\bmotion\b", "kinetic energy"), (r"\bMotion\b", "Kinetic energy")]
EC = use(U, "gen_us_science_g4_energy_conversions", rep=REP, drop=["new matter", "cold", "engineer", "criteri", "constraint"])

def en(f):
    """US answers say 'light', 'sound', 'heat'; Singapore says 'light energy' and so on"""
    import re

    def fix(c):
        return " → ".join(re.sub(r"^(light|sound|heat)$", r"\1 energy", x.strip()) for x in c.split(" → "))

    def g():
        it = f()
        if not it:
            return None
        it = dict(it)
        it["c"] = [fix(c) for c in it["c"]]
        return it if len(set(it["c"])) == 4 else None
    g.__name__ = f.__name__
    return g


for _n in ("g_out", "g_in", "g_which", "g_chain"):
    globals()["EC_" + _n] = en(getattr(EC, _n))
EC_B1 = [en(f) for f in EC.B1]

FORMS = ["kinetic energy", "gravitational potential energy", "elastic potential energy", "chemical potential energy",
         "light energy", "heat energy", "sound energy", "electrical energy"]
SIT = [("a durian hanging high on a tree", "gravitational potential energy"), ("a pupil standing at the top of a slide", "gravitational potential energy"),
       ("water held behind a dam", "gravitational potential energy"), ("a book on a high shelf", "gravitational potential energy"),
       ("a stretched rubber band", "elastic potential energy"), ("a compressed spring in a toy", "elastic potential energy"),
       ("the bent bow of an archer, ready to shoot", "elastic potential energy"), ("a wound-up spring in a toy car", "elastic potential energy"),
       ("a battery", "chemical potential energy"), ("a plate of chicken rice", "chemical potential energy"), ("petrol in a car's tank", "chemical potential energy"),
       ("a piece of charcoal for a barbecue", "chemical potential energy"), ("a moving MRT train", "kinetic energy"), ("a ball rolling down a slope", "kinetic energy"),
       ("the blades of a spinning fan", "kinetic energy"), ("a running dog", "kinetic energy"), ("the glow of a torch", "light energy"),
       ("the ringing of a school bell", "sound energy"), ("the warmth from a gas stove", "heat energy"), ("the current in a wire to a lamp", "electrical energy")]


def g_form():
    s, a = R.choice(SIT)
    if not once(("fm", s)):
        return None
    w = [x for x in FORMS if x != a]
    if "potential" in a:
        w = [x for x in w if "potential" in x] + ["kinetic energy"]
    else:
        w = R.sample(w, 3)
    return item("Which form of energy does %s mainly have?" % s, a, w[:3],
                {"gravitational potential energy": "It is raised above the ground.", "elastic potential energy": "It is stretched, bent or compressed.",
                 "chemical potential energy": "Energy is stored in the substances in it.", "kinetic energy": "It is moving."}.get(a, "This is %s." % a))


CONV = [("A pupil rubs her hands together and they feel warm.", "kinetic energy → heat energy"),
        ("A ball falls from a table to the floor.", "gravitational potential energy → kinetic energy"),
        ("A catapult shoots a stone.", "elastic potential energy → kinetic energy"),
        ("A pupil eats breakfast and then runs to school.", "chemical potential energy → kinetic energy"),
        ("A solar panel on an HDB rooftop produces electricity.", "light energy → electrical energy"),
        ("A plant makes food in its leaves.", "light energy → chemical potential energy"),
        ("A battery powers a torch.", "chemical potential energy → electrical energy → light energy"),
        ("A wind turbine turns to produce electricity.", "kinetic energy → electrical energy"),
        ("A pupil cycles up a slope and stops at the top.", "chemical potential energy → kinetic energy → gravitational potential energy"),
        ("Water flows down from a dam and turns a generator.", "gravitational potential energy → kinetic energy → electrical energy"),
        ("A candle burns.", "chemical potential energy → light energy and heat energy"),
        ("A wound-up toy car runs across the floor.", "elastic potential energy → kinetic energy")]


def g_conv():
    s, a = R.choice(CONV)
    if not once(("cv", s)):
        return None
    parts = a.split(" → ")
    rev = " → ".join(parts[::-1])
    w = [rev]
    others = [x for _, x in CONV if x != a and x != rev]
    R.shuffle(others)
    w += others[:2]
    return item("%s Which shows the main energy conversion?" % s, a, w, "%s: %s." % (s.rstrip("."), a))


def g_ball():
    h = [20, 40, 60, 80, 100]
    b = [int(x * R.choice([0.5, 0.55, 0.6])) for x in h]
    k = R.choice(["trend", "read", "why", "where", "pred"])
    if not once(("bl", k), 1):
        return None
    tb = table(["Height dropped from (cm)", "Height of first bounce (cm)"], [[str(x), str(y)] for x, y in zip(h, b)])
    q0 = "%s dropped the same ball from different heights and measured how high it bounced.<br>%s" % (P.next()[0], tb)
    if k == "trend":
        return item(q0 + "What does the table show?", "The higher the ball is dropped from, the higher it bounces.",
                    ["The higher the ball is dropped from, the lower it bounces.", "The bounce height is always 100 cm.", "The height makes no difference."],
                    "More gravitational potential energy at the start means more kinetic energy when it lands.")
    if k == "read":
        return item(q0 + "How high did the ball bounce when dropped from 60 cm?", "%d cm" % b[2], ["%d cm" % x for x in (b[1], b[3], 60)], "Read the row for 60 cm.")
    if k == "why":
        return item(q0 + "Why does the ball never bounce back to the height it was dropped from?", "Some energy is converted into heat and sound energy when it hits the floor.",
                    ["Energy is destroyed when it hits the floor.", "Gravity stops working.", "The ball gains energy from the floor."], "Energy is not lost; some changes into forms that are not useful here.")
    if k == "where":
        return item(q0 + "At which point does the ball have the most gravitational potential energy?", "just before it is released",
                    ["just before it hits the floor", "while it is touching the floor", "halfway down"], "It is highest then.")
    return item(q0 + "Predict the bounce height if the ball is dropped from 120 cm.", "about %d cm" % int(120 * b[4] / 100.0),
                ["about 120 cm", "about %d cm" % b[0], "0 cm"], "The bounce height is about the same fraction of the drop height each time.")


SUN = [("the energy in the rice we eat", "The rice plant used light energy from the Sun to make food."),
       ("the energy in a chicken drumstick", "The chicken ate plants, which got their energy from the Sun."),
       ("the energy in petrol", "Petrol comes from living things of long ago, which got their energy from the Sun."),
       ("the energy of the wind", "The Sun heats the land and air unevenly, which causes wind."),
       ("the electricity from a solar panel", "The solar panel converts light energy from the Sun.")]


def g_sun():
    t, e = R.choice(SUN)
    if not once(("sn", t)):
        return None
    return item("Where did %s first come from?" % t, "the Sun", ["the soil", "the Moon", "the power station"], e)


B1 = bank([
    ("What is energy?", "the ability to do work or make things move or change", ["a kind of matter", "a force", "a type of food"], "Energy makes things happen."),
    ("What is the main source of energy for the Earth?", "the Sun", ["the Moon", "electricity", "the wind"], "Plants, animals, food and fuels all depend on the Sun."),
    ("Which form of energy does a moving object have?", "kinetic energy", ["potential energy only", "sound energy", "chemical potential energy"], "The faster it moves, the more kinetic energy it has."),
    ("Which form of energy is stored in food and batteries?", "chemical potential energy", ["kinetic energy", "elastic potential energy", "light energy"], "It is released when the food is used by the body or the battery is used."),
    ("An object is lifted higher. What happens to its gravitational potential energy?", "It increases.", ["It decreases.", "It stays the same.", "It turns into light energy."], "The higher it is, the more gravitational potential energy it has."),
    ("Can energy be created or destroyed?", "No. It can only be converted from one form to another.", ["Yes, power stations create it.", "Yes, it is used up.", "Only in batteries."], "The total amount of energy stays the same."),
    ("Which form of energy is in a stretched rubber band?", "elastic potential energy", ["kinetic energy", "gravitational potential energy", "chemical potential energy"], "Stretching stores energy."),
    ("Why do we need energy?", "to move, grow and keep our bodies working", ["only to keep warm", "only to sleep", "we do not need energy"], "Living things need energy for life processes."),
])
B2 = bank([
    ("What happens to the kinetic energy of a cyclist who stops by braking?", "It is converted mostly into heat energy in the brakes and wheels.", ["It is destroyed.", "It disappears into the air.", "It turns into chemical potential energy in the bicycle."], "The brakes get warm."),
    ("Why does a light bulb get warm when it is switched on?", "Some electrical energy is converted into heat energy, not just light energy.", ["Light energy is always cold.", "The bulb makes new energy.", "Heat flows from the room into the bulb."], "Bulbs give off light and heat."),
    ("An LED bulb and a filament bulb give the same amount of light. The LED bulb stays cooler. Why is the LED bulb better?", "Less electrical energy is wasted as heat.", ["It makes more heat.", "It creates its own energy.", "It needs no electricity."], "Less waste means less electricity used."),
    ("A pupil swings on a swing. At which point does she have the most kinetic energy?", "at the lowest point of the swing", ["at the highest point", "when she stops", "when she gets off"], "She moves fastest at the bottom."),
    ("A pupil swings on a swing. At which point does she have the most gravitational potential energy?", "at the highest point of the swing", ["at the lowest point", "halfway down", "when she is moving fastest"], "She is highest then."),
    ("Why does a swing slowly stop if no one pushes it?", "Some energy is converted into heat and sound energy by friction and air resistance.", ["Energy is destroyed.", "Gravity disappears.", "It runs out of potential energy forever."], "Energy is converted into less useful forms."),
    ("Which energy conversion happens in a radio?", "electrical energy → sound energy", ["sound energy → electrical energy", "light energy → sound energy", "kinetic energy → light energy"], "The speaker gives out sound."),
    ("Which energy conversion happens in a microphone?", "sound energy → electrical energy", ["electrical energy → sound energy", "light energy → sound energy", "heat energy → light energy"], "It is the opposite of a speaker."),
])
B3 = bank([
    ("Why should we switch off lights when we leave a room?", "to save electrical energy and reduce the burning of fuels in power stations", ["to make the bulb cooler only", "to create more energy", "because lights use no energy"], "Most electricity in Singapore is made by burning natural gas."),
    ("Which source of energy is renewable?", "sunlight", ["coal", "natural gas", "petrol"], "Sunlight will not run out; fossil fuels will."),
    ("Why does Singapore install solar panels on HDB rooftops?", "Sunlight is renewable and Singapore gets a lot of it.", ["Solar panels make wind.", "Solar panels create energy from nothing.", "Rooftops are always cold."], "Solar energy reduces the use of fuels."),
    ("Which energy conversion happens when a pupil plays the guitar?", "kinetic energy → sound energy", ["sound energy → kinetic energy", "light energy → sound energy", "heat energy → sound energy"], "The moving strings make sound."),
    ("What happens to the energy of a falling coconut just before it hits the ground?", "Most of its gravitational potential energy has been converted into kinetic energy.", ["It has gained gravitational potential energy.", "It has no energy.", "Its energy has been destroyed."], "It speeds up as it falls."),
    ("Why does a toy car with a wound-up spring stop after a while?", "Its elastic potential energy has all been converted into kinetic, heat and sound energy.", ["Its energy was destroyed.", "Gravity pulled the energy out.", "It made new energy."], "Energy changes form; it is not used up."),
])
B5 = bank([
    ("Siti released a toy car from different heights on a ramp and measured how far it travelled. What was she investigating?", "how the starting height affects how far the car travels", ["how heavy the car is", "how loud the car is", "how bright the car is"], "A higher start gives more gravitational potential energy."),
    ("In Siti's experiment, which should be kept the same?", "the car and the surface of the ramp", ["the starting height", "the distance travelled", "the time of the day only"], "Only the starting height should change."),
    ("Ravi stretched a rubber band by different lengths to launch a paper ball. The ball went further when the band was stretched more. Why?", "More elastic potential energy was stored and converted into kinetic energy.", ["The band created energy.", "The ball became lighter.", "Gravity was weaker."], "More stretch stores more energy."),
    ("A pupil touched a bulb after it had been on for 10 minutes. It was hot. What can she conclude?", "Some electrical energy was converted into heat energy.", ["The bulb creates heat from nothing.", "The bulb is broken.", "Light energy is the same as heat energy."], "Bulbs waste some energy as heat."),
    ("Mei Ling recorded the temperature of two bulbs giving the same light: Bulb A 80 °C, Bulb B 35 °C. Which bulb wastes less energy as heat?", "Bulb B", ["Bulb A", "both the same", "neither wastes energy"], "The cooler bulb converts less electrical energy into heat."),
])


def body():
    think = ("<p><b>Energy can be converted from one form to another, but it cannot be created or destroyed.</b></p>"
             "<ul><li><b>Kinetic energy</b>: energy of a moving object.</li>"
             "<li><b>Potential energy</b>: stored energy: gravitational (raised up), elastic (stretched or compressed), chemical (in food, fuels, batteries).</li>"
             "<li>Other forms: light, heat, sound and electrical energy.</li>"
             "<li>The <b>Sun</b> is the main source of energy for the Earth.</li></ul>")
    ex = [("A ball is dropped from a height. What conversion happens?", ["At the top it has gravitational potential energy", "As it falls it speeds up"], "Gravitational potential energy → kinetic energy."),
          ("Where does the energy in our food come from?", ["Plants use light to make food", "Animals eat plants"], "The Sun.")]
    mist = ["Saying energy is 'used up'. It is converted into other forms, often heat.",
            "Thinking an object at rest at a height has no energy. It has gravitational potential energy.",
            "Thinking a battery stores electrical energy. It stores chemical potential energy.",
            "Mixing up kinetic and potential energy for a stretched rubber band (it has elastic potential energy)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Forms of energy", B1 + [(g_form, 10), (g_sun, 2)]),
        ("Energy conversions", B2 + [(g_conv, 6), (EC_g_out, 3), (EC_g_in, 3)]),
        ("Energy in daily life", B3 + [(g_form, 5), (g_conv, 4), (EC_g_which, 3), (g_sun, 2)]),
        ("Tracing energy", [(EC_g_chain, 5), (g_conv, 2), (g_sun, 1), (EC_g_out, 4), (EC_g_in, 3), (EC_g_which, 3), (g_form, 2)]),
        ("PSLE-style experiments", B5 + EC_B1 + [(g_ball, 5), (g_form, 3), (EC_g_chain, 3)]),
    ])
    make_sg(6, "energy-forms-and-conversion", 2, "Energy", "Energy forms and uses (Energy conversion)",
            "Recognise the different forms of energy: kinetic energy, potential energy (gravitational, elastic and chemical), light, heat, sound and electrical energy. "
            "Recognise that energy can be converted from one form to another, that it cannot be created or destroyed, and that the Sun is the main source of energy. "
            "Show an understanding of the need to use energy wisely (summary of the MOE Primary Science Syllabus).",
            "Energy Forms and Conversion",
            "Primary 6 Science: Energy Forms and Conversion Worksheets (PSLE Practice with Answers)",
            "Energy forms and conversion",
            "Free Primary 6 science worksheets for Singapore pupils on forms of energy and energy conversion: kinetic and potential energy, light, heat, sound and electrical energy. PSLE practice with answers.",
            "Energy changes form; it is never used up.",
            "Kinetic, potential, light, heat, sound and electrical energy.",
            body(),
            [("What are the forms of energy in Primary 6?", "Kinetic energy, potential energy (gravitational, elastic and chemical), light, heat, sound and electrical energy."),
             ("Is energy used up?", "No. Energy cannot be created or destroyed. It is converted into other forms, often heat and sound, which are less useful."),
             ("What energy does a battery store?", "A battery stores chemical potential energy, which is converted into electrical energy when it is used in a circuit.")],
            sets)


if __name__ == "__main__":
    main()
