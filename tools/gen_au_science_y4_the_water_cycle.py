# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, AC9S4U02: the water cycle - evaporation, condensation, precipitation, collection,
and how people use water in Australia (dams, rainwater tanks, the Murray-Darling, droughts, water restrictions).
  python tools/gen_au_science_y4_the_water_cycle.py
Reuses the UK Year 4, SG Primary 5 and US Grade 6 water cycle makers with Australian names; Singapore-only places dropped.
Wrong answers come from real mistakes: thinking clouds are water vapour (they are tiny droplets), thinking water disappears when
it evaporates, and mixing up evaporation and condensation.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 4, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

UK = "gen_uk_science_y4_the_water_cycle"
SG = "gen_sg_science_p5_the_water_cycle"
US = "gen_us_science_g6_the_water_cycle"
NS = ["Marina", "Bedok", "NEWater", "reservoir in Singapore", "PUB", "Malaysia", "Johor", "canal"]
uk_dish = limit(src(UK, "g_dish"), 4)
uk_dry = limit(src(UK, "g_dry"), 3)
uk_eve = src(UK, "g_eve")
uk_name = src(UK, "g_name")
uk_next = src(UK, "g_next")
uk_b1 = src.B(UK, "B1")
uk_b5 = src.B(UK, "B5")
sg_save = src(SG, "g_save", drop=NS)
sg_b1 = src.B(SG, "B1")
sg_b3 = src.B(SG, "B3", drop=["In the same model"])
sg_b5 = src.B(SG, "B5")
us_every = src(US, "g_every")
us_label = limit(src(US, "g_label"), 6)
us_proc = src(US, "g_proc")
us_drive = src(US, "g_drive")
us_b1 = src.B(US, "B1")

SC = [("Water in a puddle on the footpath dries up on a hot afternoon.", "evaporation"), ("Water droplets form on the outside of a cold glass of water.", "condensation"),
      ("Fog forms over a river on a cold winter morning.", "condensation"), ("Rain falls on the hills behind Brisbane.", "precipitation"),
      ("Snow falls on the Australian Alps in winter.", "precipitation"), ("Rainwater runs down into a creek and then into a dam.", "collection"),
      ("Water collects in a rainwater tank from the roof.", "collection"), ("Sea water warms in the sun and rises into the air as water vapour.", "evaporation"),
      ("Clouds form as warm, moist air rises over the Great Dividing Range.", "condensation"), ("Hail falls during a summer storm in Sydney.", "precipitation"),
      ("Water soaks into the ground and becomes groundwater.", "collection"), ("Dew forms on the grass at dawn.", "condensation"),
      ("Wet swimmers dry quickly on a windy day at the beach.", "evaporation"), ("Floodwater flows along the Murray River to the sea.", "collection")]


def g_sc():
    st, p = R.choice(SC)
    return tq("%s Which part of the water cycle is this?" % st, p, [x for x in ["evaporation", "condensation", "precipitation", "collection"] if x != p],
              {"evaporation": "Liquid water turns into water vapour (a gas).", "condensation": "Water vapour cools and turns into tiny liquid droplets.",
               "precipitation": "Water falls from clouds as rain, hail or snow.", "collection": "Water gathers in rivers, lakes, oceans, dams and under the ground."}[p])


POOL1 = pool(R, [
    ("Which of these is collection?", "rain filling Warragamba Dam", ["fog over a river", "a puddle drying", "a cloud forming"], "Collection is water gathering in dams, rivers, oceans and underground."),
    ("Why is a river in central Australia often dry for much of the year?", "Little rain falls and the hot sun evaporates the water quickly.", ["The river flows uphill.", "The water turns into sand.", "Rain only falls on the sea."], "Many inland rivers flow only after heavy rain."),
    ("What is water vapour?", "water as a gas", ["water as ice", "a cloud", "rain"], "We cannot see water vapour."),
    ("Does water disappear when a puddle dries up?", "No. It evaporates into the air as water vapour.", ["Yes, it is destroyed.", "It soaks into the Sun.", "It turns into salt."], "The water is still in the air."),
    ("Why is the water cycle called a cycle?", "The same water moves around again and again.", ["It moves in a straight line.", "It happens once.", "It only happens in summer."], "Water is never used up."),
    ("Where is most of Earth's water?", "in the oceans", ["in rivers", "in clouds", "in rainwater tanks"], "About 97% of Earth's water is salty sea water."),
    ("Why do many Australian homes have rainwater tanks?", "to collect and store rain for gardens and toilets", ["to make it rain more", "to store sea water", "to evaporate water"], "Australia is a dry continent."),
    ("What happens to water vapour when it cools?", "It condenses into liquid droplets.", ["It evaporates.", "It turns into salt.", "It disappears."], "Cooling causes condensation."),
    ("Why do towns have water restrictions during a drought?", "There is little rain, so the stored water must last longer.", ["to make it rain", "because water is too cold", "to stop evaporation in winter"], "Saving water helps everyone."),
    ("What is transpiration?", "water leaving plant leaves as water vapour", ["rain falling on plants", "roots making rain", "plants drinking sea water"], "Trees add lots of water vapour to the air."),
])
POOL5 = pool(R, [
    ("Mia covers a bowl of salty water with cling wrap and puts a small cup in the middle. After a day in the sun, fresh water is in the cup. Which processes happened?", "evaporation, then condensation", ["condensation, then evaporation", "precipitation only", "freezing, then melting"], "This is how a solar still works."),
    ("Jack puts 200 mL of water in a dish in the sun and 200 mL in the shade. After a day, the sunny dish has 120 mL left. What would the shady dish most likely have?", "about 170 mL", ["about 50 mL", "about 120 mL", "more than 200 mL"], "Water evaporates faster where it is warmer."),
    ("In Jack's test, what should he keep the same?", "the size of the dishes and the amount of water", ["the place", "the temperature", "nothing"], "Change only sun or shade."),
    ("Ruby wants to find out whether wind makes washing dry faster. Which is the fairest test?", "two identical wet towels, one in front of a fan and one without", ["one wet towel and one dry towel", "a towel and a sock", "two towels in different rooms with different heaters"], "Only the wind should change."),
    ("A rain gauge in Darwin shows 400 mm in January and 0 mm in July. What does this show?", "Darwin has a wet season and a dry season.", ["It rains the same all year.", "The gauge is broken.", "July is the wet season."], "Northern Australia has a wet summer."),
    ("Why does a bathroom mirror fog up after a hot shower?", "Water vapour condenses on the cool mirror.", ["The mirror evaporates.", "Steam is smoke.", "The mirror makes water."], "Warm, moist air cools on the glass."),
])


def main():
    sets = U.sets([
        ("Parts of the water cycle", [(POOL1, 5), (uk_name, 5), (uk_next, 5), (sg_b1, 3), (us_b1, 2)]),
        ("What is happening?", [(g_sc, 10), (uk_eve, 5), (us_every, 5)]),
        ("Water cycle diagrams", [(us_label, 6), (us_proc, 6), (us_drive, 3), (POOL1, 3), (uk_b1, 2)]),
        ("Water in Australia", [(POOL1, 2), (g_sc, 4), (sg_save, 6), (uk_b1, 3), (sg_b3, 3), (uk_dry, 2)]),
        ("Investigations", [(POOL5, 6), (uk_dish, 4), (uk_b5, 4), (sg_b5, 3), (uk_dry, 1), (us_every, 2)]),
    ])
    make_au(YEAR, "the-water-cycle", SORT, "AC9S4U02", "Earth and space sciences",
            "Identify sources of water and describe key processes in the water cycle, including movement of water through the "
            "environment and its use as a resource (summary of the Australian Curriculum v9.0 Science content description).",
            "The Water Cycle", "The water cycle",
            "Free Year 4 science worksheets on the water cycle: evaporation, condensation, precipitation and collection, plus rainwater "
            "tanks, dams and saving water in Australia. 100 questions with answers.",
            "Evaporate, condense, fall, collect.", "The Sun drives the water cycle, and the same water is used again and again.",
            "<p><b>The water cycle moves the same water around again and again.</b></p><ul>"
            "<li>Evaporation: the Sun heats water and it becomes water vapour (a gas). Plants also give off water vapour (transpiration).</li>"
            "<li>Condensation: water vapour cools and forms tiny droplets: clouds, fog and dew.</li>"
            "<li>Precipitation: rain, hail or snow falls. Collection: water gathers in rivers, dams, oceans and under the ground.</li></ul>",
            [("Dew on the grass at dawn. Which process?", ["cool night air", "water vapour turns to liquid"], "condensation"),
             ("A puddle dries up. Where did the water go?", ["it evaporated", "it is water vapour in the air"], "into the air")],
            ["Thinking clouds are water vapour (they are tiny water droplets).", "Thinking water disappears when it evaporates.",
             "Mixing up evaporation (liquid to gas) and condensation (gas to liquid)."],
            [("What are the four main stages of the water cycle?", "Evaporation, condensation, precipitation and collection."),
             ("Why is water important to save in Australia?", "Australia is the driest inhabited continent. Rainfall changes a lot from year to year, so droughts are common."),
             ("Where does the water in a cloud come from?", "It comes from water that evaporated from oceans, lakes, rivers, soil and plants, then cooled and condensed into droplets.")],
            sets)


if __name__ == "__main__":
    main()
