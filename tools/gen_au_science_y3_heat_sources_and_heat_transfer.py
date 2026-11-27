# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, AC9S3U03: sources of heat and how heat moves from hotter to colder objects;
conductors and insulators of heat.
  python tools/gen_au_science_y3_heat_sources_and_heat_transfer.py
Reuses the SG Primary 4 heat makers with Australian names, plus own Australian contexts (a metal slide in summer, beach sand,
a barbecue, solar hot water, an esky).
Wrong answers come from real mistakes: thinking "cold" flows into warm things, thinking a jumper makes its own heat, and thinking
metal feels cold because it is colder than wood in the same room.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

HT = "gen_sg_science_p4_heat_and_temperature"
HC = "gen_sg_science_p4_heat_conductors_and_insulators"
ht_flow = limit(src(HT, "g_flow"), 8)
ht_mix = src(HT, "g_mix")
ht_read = src(HT, "g_read")
ht_b1 = src.B(HT, "B1")
ht_b2 = src.B(HT, "B2")
ht_b5 = src.B(HT, "B5")
hc_ice = src(HC, "g_ice")
hc_rod = limit(src(HC, "g_rod"), 4)
hc_use = src(HC, "g_use")
hc_b1 = src.B(HC, "B1")
hc_b2 = src.B(HC, "B2")
hc_b3 = src.B(HC, "B3")
hc_b5 = src.B(HC, "B5")

SRC = ["the Sun", "a campfire", "a barbecue", "an electric heater", "a stove", "a candle flame", "your body", "rubbing your hands together", "a toaster", "a hair dryer"]
NOT = ["an ice block", "a glass of cold water", "a fridge", "a block of wood at room temperature", "a cold metal spoon", "snow", "an esky full of ice", "a fan"]


def g_src():
    if R.random() < 0.5:
        a = R.choice(SRC)
        return tq("Which of these is a source of heat?", a, R.sample(NOT, 3), "A heat source gives off heat: the Sun, fire, electric heaters and even your body.")
    a = R.choice(NOT)
    return tq("Which of these is NOT a source of heat?", a, R.sample(SRC, 3), "%s%s does not give off heat." % (a[0].upper(), a[1:]))


POOL1 = pool(R, [
    ("Which way does heat always move?", "from a hotter object to a colder object", ["from a colder object to a hotter object", "only upwards", "only from metal"], "Cold does not flow; heat moves out of hot things."),
    ("What is the main source of heat for Earth?", "the Sun", ["the Moon", "volcanoes only", "the wind"], "Sunlight warms the land, sea and air."),
    ("Why does a metal slide feel very hot on a summer afternoon?", "The Sun heats the metal and metal passes heat quickly into your skin.", ["Metal makes its own heat.", "Metal is always hot.", "The slide is near a heater."], "Metal is a good conductor of heat."),
    ("Why does beach sand feel hotter than the water on a sunny day?", "Sand heats up faster than water in the sun.", ["Water is a heat source.", "Sand makes its own heat.", "The water is far from the Sun."], "Different materials heat up at different rates."),
    ("How does an esky keep drinks cold?", "Its walls are insulators that slow heat moving in from outside.", ["It makes cold air.", "Its walls are good conductors.", "It is magnetic."], "Insulators slow heat movement."),
    ("Why does a woollen jumper keep you warm?", "It is an insulator that slows heat leaving your body.", ["It makes its own heat.", "It conducts heat away quickly.", "It is a heat source."], "Your body is the heat source."),
    ("Why do saucepans often have plastic or wooden handles?", "Plastic and wood are poor conductors, so the handle stays cool.", ["They look nice.", "They make the pan heavier.", "They conduct heat quickly."], "Insulators protect your hand."),
    ("What does a solar hot water system use to heat water?", "energy from the Sun", ["energy from the Moon", "cold air", "ice"], "Many Australian roofs have solar panels or solar hot water."),
    ("When you hold an ice block, what happens to the heat in your hand?", "Heat moves from your hand into the ice block.", ["Cold moves from the ice into your hand.", "Nothing moves.", "Heat moves from the ice to your hand."], "That is why your hand feels cold."),
    ("Which tool measures how hot something is?", "a thermometer", ["a ruler", "a stopwatch", "a magnet"], "Temperature is measured in degrees Celsius (°C)."),
])
POOL5 = pool(R, [
    ("Mia puts thermometers in water in a black can and a white can in the sun. After 30 minutes: black 41 °C, white 33 °C. What can she conclude?", "Black cans heat up more in the sun.", ["White cans heat up more.", "Colour makes no difference.", "The Sun cools black cans."], "Dark colours absorb more sunlight."),
    ("In Mia's test, what should she keep the same?", "the amount of water, the size of the cans and the time in the sun", ["the colour of the cans", "nothing", "only the thermometers"], "Change only the colour."),
    ("Jack wraps ice cubes in foil, wool and paper and times how long each takes to melt: 25, 70 and 40 minutes. Which is the best insulator?", "wool", ["foil", "paper", "they are all the same"], "The longest time means heat moved in most slowly."),
    ("Ruby wants to keep a hot pie warm for lunch. Which is the best choice?", "wrap it in a thick tea towel inside an insulated bag", ["put it on a metal tray in the wind", "put it in the fridge", "leave it uncovered"], "Insulators slow heat loss."),
])


def main():
    sets = U.sets([
        ("Heat sources", [(g_src, 8), (POOL1, 6), (ht_b1, 4), (ht_read, 2)]),
        ("Heat moves", [(ht_flow, 8), (ht_b2, 5), (ht_mix, 3), (POOL1, 4)]),
        ("Conductors and insulators", [(hc_use, 8), (hc_b1, 5), (hc_b2, 4), (hc_b3, 3)]),
        ("Keeping warm and cool", [(hc_b3, 3), (hc_ice, 4), (POOL1, 0), (ht_read, 5), (g_src, 4), (hc_use, 4)]),
        ("Investigations", [(POOL5, 4), (hc_rod, 4), (hc_b5, 4), (ht_b5, 4), (hc_ice, 1), (ht_mix, 2), (g_src, 1)]),
    ])
    make_au(YEAR, "heat-sources-and-heat-transfer", SORT, "AC9S3U03", "Physical sciences",
            "Identify sources of heat energy and describe how heat moves through and between objects, including conductors and "
            "insulators (summary of the Australian Curriculum v9.0 Science content description).",
            "Heat Sources and Heat Transfer", "Heat sources and heat transfer",
            "Free Year 3 science worksheets on heat: sources of heat, how heat moves from hot to cold, reading thermometers, and conductors "
            "and insulators such as metal, wood, wool and an esky. 100 questions with answers.",
            "Heat moves from hot to cold.", "Conductors let heat move quickly; insulators slow it down.",
            "<p><b>Heat always moves from a hotter object to a colder one.</b></p><ul>"
            "<li>Heat sources give off heat: the Sun, fire, a barbecue, a heater, your body.</li>"
            "<li>Metals are good conductors: heat moves through them quickly.</li>"
            "<li>Wood, plastic, wool and air are insulators: they slow heat moving, keeping hot things hot and cold things cold.</li></ul>",
            [("Ice block in your hand. Which way does heat move?", ["your hand is warmer"], "from your hand to the ice"),
             ("Best handle for a frying pan?", ["the handle must not get hot"], "wood or plastic (an insulator)")],
            ["Thinking 'cold' flows into things (heat flows out of them).", "Thinking a jumper makes its own heat.",
             "Thinking metal is colder than wood in the same room (it only feels colder because it conducts heat away)."],
            [("Which way does heat move?", "Heat moves from a hotter object or place to a colder one until they are the same temperature."),
             ("What is the difference between a conductor and an insulator of heat?", "A conductor, such as metal, lets heat move through it quickly. An insulator, such as wood, plastic or wool, slows heat down."),
             ("Why does metal feel colder than wood in the same room?", "Both are at the same temperature, but metal conducts heat away from your hand faster, so it feels colder.")],
            sets)


if __name__ == "__main__":
    main()
