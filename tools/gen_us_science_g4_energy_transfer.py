# -*- coding: utf-8 -*-
"""
US Grade 4 Science: How Energy Moves: Sound, Light and Heat (4-PS3-2)
  python tools/gen_us_science_g4_energy_transfer.py
Energy can be moved from place to place by sound, light, heat and electric currents.
Heat flows from warmer to cooler objects; sound travels as vibrations; light carries energy
from the sun and lamps. Data: temperature tables for cooling and warming.
Wrong answers come from real mistakes: "cold flows into things", "sound can travel through empty
space", "light carries no energy", "a blanket makes heat".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, classifier, People

U = Unit(40102)
R = U.R
P = People(R)

WAYS = {
    "sound": ["A drum is hit and people across the room hear it.", "A guitar string vibrates and the sound reaches your ears.",
              "Thunder rattles the windows.", "A loud speaker makes a paper cup shake.", "A dog's bark carries across the yard.",
              "A bell rings and the sound reaches the classroom."],
    "light": ["Light from the sun reaches Earth through space.", "A lamp lights up a dark room.", "Sunlight makes a solar calculator work.",
              "A flashlight beam shines on a wall.", "A lighthouse beam reaches a ship far out at sea.", "Light from a campfire lets you see the trees."],
    "heat": ["A hot pan warms a metal spoon left in it.", "Your hands warm up around a mug of cocoa.", "An ice cube melts in your hand.",
             "A radiator warms the air in a room.", "A heating pad warms a sore back.", "A warm bath warms your body."],
    "electric current": ["A battery makes a toy car's motor spin.", "A wire carries energy from an outlet to a lamp.", "Power lines bring energy to a school.",
                         "A phone charger fills a battery.", "A wire carries energy from a solar panel to a fan.", "A battery lights a flashlight bulb."],
}
WHY = {"sound": "Sound carries energy as vibrations.", "light": "Light carries energy from a source like the sun or a lamp.",
       "heat": "Heat moves from a warmer object to a cooler one.", "electric current": "An electric current carries energy through wires."}
w_which, w_what = classifier(R, WAYS, "Which is an example of energy moved by {k}?", "{x} How is energy moved here?", WHY,
                             label=lambda k: k if k != "electric current" else "an electric current")


def g_cool():
    t0 = R.randint(70, 90)
    drops = [R.randint(6, 12) for _ in range(4)]
    vals = [t0]
    for d in drops:
        vals.append(vals[-1] - d)
    room = 22
    if vals[-1] <= room + 2:
        return None
    rows = [["%d min" % (5 * i), "%d °C" % v] for i, v in enumerate(vals)]
    k = R.choice(["why", "where", "drop"])
    p = P.next()
    tab = table(["Time", "Temperature of the water"], rows)
    if k == "why":
        return item(tab + "%s leaves a cup of hot water on a table in a %d °C room. Why does the water cool down?" % (p[0], room),
                    "Heat moves from the hot water to the cooler air and table.", ["Cold moves from the air into the water.", "The water makes cold.", "Heat is destroyed."],
                    "Heat always flows from warmer to cooler. The water loses energy to its surroundings.")
    if k == "where":
        return item(tab + "%s's hot water cools in a %d °C room. What temperature will it reach if it sits for a whole day?" % (p[0], room),
                    "about %d °C, the temperature of the room" % room, ["0 °C", "%d °C" % t0, "below %d °C" % (room - 10)],
                    "It loses heat until it is the same temperature as the room. Then no more heat flows.")
    return item(tab + "How many degrees did %s's water cool in the first 20 minutes?" % p[0], "%d degrees" % (vals[0] - vals[4]),
                ["%d degrees" % vals[4], "%d degrees" % (vals[0] - vals[1]), "%d degrees" % vals[0]], "%d − %d = %d degrees." % (vals[0], vals[4], vals[0] - vals[4]))


def g_cups():
    mats = R.sample(["foam", "paper", "metal", "glass", "plastic"], 3)
    order = {"foam": 1, "plastic": 2, "paper": 3, "glass": 4, "metal": 5}
    mats.sort(key=lambda m: order[m])
    ends = sorted(R.sample(range(36, 60), 3), reverse=True)
    rows = [[m + " cup", "%d °C" % e] for m, e in zip(mats, ends)]
    R.shuffle(rows)
    return item(table(["Cup", "Temperature after 30 min"], rows) + "Hot water at 80 °C was poured into three cups. Which cup slowed the movement of heat the most?",
                mats[0] + " cup", [m + " cup" for m in mats[1:]] + ["They all lost heat the same way."],
                "The %s cup kept the water the warmest (%d °C), so heat left it most slowly. It is the best insulator here." % (mats[0], ends[0]))


def g_bar():
    places = R.sample(["black paper", "white paper", "foil", "dark soil", "grass"], 3)
    rank = {"black paper": 6, "dark soil": 5, "grass": 3, "white paper": 2, "foil": 1, "shade": 0}
    places.sort(key=lambda x: -rank[x])
    vals = sorted(R.sample(range(24, 45), 3), reverse=True)
    if "shade" in places:
        pass
    order = list(range(3))
    R.shuffle(order)
    ch = bar_chart([places[i] for i in order], [vals[i] for i in order], "°C", "bar graph of temperatures in the sun", ymax=50, step=10, w=300)
    return item(fig(ch) + "Thermometers were left on different surfaces in the sun for an hour. Which surface took in the most energy from sunlight?",
                places[0], places[1:] + ["They all took in the same amount."], "It reached the highest temperature: %d °C." % vals[0])


B1 = bank([
    ("Which four ways can energy move from place to place?", "sound, light, heat and electric currents", ["only by touching", "only by wind", "only by water"],
     "Energy moves by sound, light, heat and electricity, and with moving objects."),
    ("Which way does heat always flow?", "from a warmer object to a cooler object", ["from a cooler object to a warmer object", "only upward", "only through metal"],
     "Heat moves until both objects are the same temperature."),
    ("You hold an ice cube and your hand feels cold. What is happening?", "Heat moves from your hand into the ice.", ["Cold moves from the ice into your hand.", "The ice makes cold energy.", "Nothing moves."],
     "There is no flow of “cold.” Your hand loses heat to the ice."),
    ("What makes a sound?", "vibrations", ["light", "magnets", "heat only"],
     "A vibrating object, like a drum skin, makes the air vibrate, and the vibrations carry energy."),
    ("Can sound travel through empty space, where there is no air?", "No. Sound needs matter to travel through.", ["Yes, sound travels best in space.", "Only loud sounds can.", "Only at night."],
     "Sound is vibration of matter. With no matter, there is nothing to vibrate."),
    ("How does energy from the sun reach Earth?", "as light", ["as sound", "through wires", "through the air as wind"],
     "Sunlight travels through space and carries energy to Earth."),
    ("A blanket keeps you warm because it", "slows the heat leaving your body", ["makes heat", "adds cold", "makes your body heavier"],
     "A blanket is an insulator. It does not make heat; it traps the heat your body makes."),
    ("Which material lets heat move through it fastest?", "metal", ["wood", "foam", "wool"],
     "Metals are good conductors of heat."),
    ("A louder sound from the same drum means", "the drum was hit harder and carries more energy", ["the drum got smaller", "the sound is slower", "there is less energy"],
     "Hitting harder makes bigger vibrations with more energy."),
    ("Why does a dark shirt feel hotter in the sun than a white shirt?", "Dark colors take in more of the light's energy.", ["Dark shirts are heavier.", "White shirts make cold.", "Dark shirts are closer to the sun."],
     "Light carries energy. Dark materials absorb more of it and warm up more."),
])
B5 = bank([
    ("Ava puts the same amount of hot water in a foam cup and a metal cup. What is she testing?", "which material slows the movement of heat better", ["which cup is heavier", "which cup is taller", "which cup is prettier"],
     "Only the cup material is different."),
    ("Leo places a ruler on a table, presses his ear to it and taps the far end. He hears the tap clearly. What does this show?", "Sound travels through solids.", ["Sound only travels through air.", "Rulers make light.", "Tables block sound."],
     "Sound vibrations travel through solids, liquids and gases."),
    ("Why do pot handles get hot when the handle is metal but not when it is wood?", "Heat moves through metal faster than through wood.", ["Wood makes cold.", "Metal makes its own heat.", "Wood is heavier."],
     "Metal conducts heat; wood insulates."),
    ("Which investigation shows that light carries energy?", "Put a thermometer in sunlight and one in the shade and compare.", ["Ring a bell.", "Weigh a flashlight.", "Rub two sticks together in the dark."],
     "The thermometer in sunlight warms up because light carries energy."),
    ("Mia hits a drum with sand on top. The sand jumps. What does this show?", "The drum skin is vibrating, and the vibrations carry energy.", ["The sand is magnetic.", "The drum is heavy.", "Sound is made of sand."],
     "The vibrations give energy to the sand and make it move."),
    ("Noah wraps one ice cube in foil and one in a wool sock. The ice in the sock melts slower. Why?", "Wool slows heat from moving into the ice.", ["Wool makes cold.", "Foil makes heat.", "Socks are heavier."],
     "Wool is a good insulator."),
])


def body():
    think = ("<p>Energy can move from place to place in several ways:</p>"
             "<ul><li><b>Sound</b>: vibrations travel through air, water or solids.</li>"
             "<li><b>Light</b>: carries energy from the sun or a lamp; it can warm things up.</li>"
             "<li><b>Heat</b>: always moves from a <b>warmer</b> object to a <b>cooler</b> one.</li>"
             "<li><b>Electric current</b>: carries energy through wires.</li></ul>"
             "<p>Some materials (metals) let heat move quickly. Others (foam, wool, wood) slow it down: they are insulators.</p>")
    ex = [("Hot cocoa cools on the table. Where does its energy go?", ["Heat moves from warmer to cooler.", "The air and table are cooler."], "into the air and the table"),
          ("A guitar string is plucked. How does the energy reach your ear?", ["The string vibrates.", "The air vibrates."], "as sound")]
    mist = ["Saying cold moves into things. Heat moves out of the warmer object.",
            "Thinking sound can travel through empty space.",
            "Thinking a blanket makes heat. It slows heat from leaving."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Ways energy moves", B1 + [(w_which, 5), (w_what, 5)]),
        ("Sound, light, heat or electricity?", [(w_which, 10), (w_what, 10)]),
        ("Heat moves from warm to cool", [(g_cool, 12), (g_cups, 8)]),
        ("Light and heat data", [(g_bar, 10), (g_cups, 5), (g_cool, 5)]),
        ("Investigations", B5 + [g_cool, g_cups, g_bar, w_what]),
    ])
    make("grade-4", "energy-transfer", 2, "4-PS3-2",
         "Make observations to provide evidence that energy can be transferred from place to place by sound, light, heat, and electric currents.",
         "How Energy Moves: Sound, Light and Heat",
         "Grade 4 Energy Transfer Worksheets: Sound, Light, Heat and Electric Currents",
         "Energy Transfer",
         "Free Grade 4 science worksheets on energy transfer (NGSS 4-PS3-2): sound vibrations, light from the sun, heat moving from warm to cool, insulators and electric currents, with temperature data. 100 practice questions with answers.",
         "Energy moves by sound, light, heat and electric currents.",
         "Heat always flows from warmer to cooler. Sound is vibration. Light carries energy from the sun and lamps.",
         body(),
         [("How is energy transferred?", "By sound (vibrations), light, heat (from warmer to cooler objects) and electric currents in wires."),
          ("Does cold move into things?", "No. Heat moves out of the warmer object. Your hand feels cold on ice because heat leaves your hand."),
          ("Can sound travel in space?", "No. Sound needs matter such as air, water or a solid to vibrate.")],
         sets)


if __name__ == "__main__":
    main()
