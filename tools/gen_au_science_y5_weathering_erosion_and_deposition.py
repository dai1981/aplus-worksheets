# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U02: weathering, erosion, transportation and deposition change Earth's surface.
  python tools/gen_au_science_y5_weathering_erosion_and_deposition.py
Australian landforms (Twelve Apostles, Uluru, Wave Rock, the Three Sisters, K'gari sand dunes, the Murray mouth) and
scenarios sorted into the four processes. Reuses the US Grade 4 weathering makers (stream tables, slopes) with Australian names.
Wrong answers come from real mistakes: calling the breaking of rock "erosion", thinking weathering moves the pieces,
forgetting that deposition happens where water or wind slows down.
"""
from au_sci import AU, seed_of, make_au, tq, pool

YEAR, SORT = 5, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

W = "gen_us_science_g4_weathering_and_erosion"
us_b1 = src.B(W, "B1")
us_b5 = src.B(W, "B5")
us_slope = src(W, "g_slope")
us_plants = src(W, "g_plants")
us_water = src(W, "g_water")
us_speed = src("gen_us_science_g2_fast_and_slow_earth_changes", "g_speed")

PROC = ["weathering", "erosion", "transportation", "deposition"]
SC = [("Water seeps into a crack in a rock, freezes, expands and splits the rock.", "weathering"),
      ("A tree root grows into a crack and slowly pushes the rock apart.", "weathering"),
      ("In the desert, rock heats up by day and cools at night until thin layers flake off.", "weathering"),
      ("Rainwater slowly dissolves limestone and makes a cave.", "weathering"),
      ("Lichen growing on a rock slowly breaks down its surface.", "weathering"),
      ("Salt crystals grow in tiny holes in a sea cliff and crumble the sandstone.", "weathering"),
      ("Heavy rain washes soil off a bare hillside.", "erosion"),
      ("Strong wind picks up loose sand from a dune.", "erosion"),
      ("Waves wear away the bottom of a cliff and carry the pieces off.", "erosion"),
      ("A fast creek scrapes sand and pebbles from its banks.", "erosion"),
      ("Cattle trample a riverbank and the soil is washed away.", "erosion"),
      ("A muddy river carries soil many kilometres downstream.", "transportation"),
      ("Dust blown from the outback travels across the sea to New Zealand.", "transportation"),
      ("Pebbles roll and bounce along the bed of a fast river.", "transportation"),
      ("A glacier carries boulders as it slowly moves down a valley.", "transportation"),
      ("Sand is pushed along a beach by waves arriving at an angle.", "transportation"),
      ("A river slows down where it meets the sea and drops mud, forming new land.", "deposition"),
      ("Wind drops sand behind a fence and a small dune forms.", "deposition"),
      ("After a flood, a layer of mud is left on the farm paddocks.", "deposition"),
      ("Sand settles on the inside bend of a river where the water is slow.", "deposition"),
      ("Waves drop sand in a sheltered bay, making a wide beach.", "deposition"),
      ("Layers of sand settle at the bottom of a lake over many years.", "deposition")]


def g_proc():
    s, p = R.choice(SC)
    e = {"weathering": "Weathering breaks rock into smaller pieces where it is.",
         "erosion": "Erosion picks up and removes rock pieces and soil.",
         "transportation": "Transportation carries the pieces to a new place.",
         "deposition": "Deposition drops the pieces when the water, wind or ice slows down."}[p]
    return tq("%s Which process is this?" % s, p, [x for x in PROC if x != p], e)


AG = [("Waves crash against the coast and wear away the cliffs.", "waves"),
      ("Sand blasts against a rock in a dust storm and smooths it.", "wind"),
      ("A creek carves a deep gorge in the hills over thousands of years.", "running water"),
      ("Rocks fall down a steep slope after heavy rain loosens them.", "gravity"),
      ("Long ago, a glacier in Tasmania carved a U-shaped valley.", "ice"),
      ("Sand dunes slowly move inland across the coast.", "wind"),
      ("A flood washes a gully into a paddock.", "running water"),
      ("Pebbles on a beach are rolled smooth by the sea.", "waves"),
      ("A huge chunk of a cliff collapses onto the beach below.", "gravity"),
      ("Frozen water in alpine cracks splits rocks into sharp pieces.", "ice"),
      ("A storm surge washes away the front of a sand dune at the beach.", "waves"),
      ("Red dust from a dry paddock blows over a city.", "wind"),
      ("A river carries mud out to sea after heavy rain.", "running water"),
      ("Loose soil slides down a hillside cut for a new road.", "gravity"),
      ("Rain running off a car park cuts a channel in the dirt beside it.", "running water"),
      ("Waves carve a cave into the bottom of a limestone cliff.", "waves"),
      ("Fine sand is blown off a ploughed field on a windy day.", "wind"),
      ("Boulders tumble down a gorge wall and pile up at the bottom.", "gravity"),
      ("On Kosciuszko, freezing nights crack rocks on the mountain top.", "ice"),
      ("A desert rock is shaped like a mushroom by sand blowing near the ground.", "wind"),
      ("Floodwater digs out the bank of a creek on a bend.", "running water"),
      ("Ocean swell slowly wears down a rock platform.", "waves")]


def g_agent():
    s, a = R.choice(AG)
    w = [x for x in ["waves", "wind", "running water", "gravity", "ice"] if x != a]
    return tq("%s What is mainly causing this change?" % s, a, R.sample(w, 3), "The cause of this change is %s." % a)


LAND = [("the Twelve Apostles in Victoria", "Waves eroded the limestone cliffs, leaving stacks of rock.", "erosion by waves"),
        ("the Three Sisters in the Blue Mountains", "Wind and rain wore away the softer sandstone around them.", "weathering and erosion by wind and rain"),
        ("Wave Rock in Western Australia", "Weathering under the soil and rain shaped the curved granite face.", "weathering by water"),
        ("the sand dunes of K'gari (Fraser Island)", "Wind and waves dropped huge amounts of sand.", "deposition of sand"),
        ("the mouth of the Murray River", "The river slows and drops sand and mud where it meets the sea.", "deposition by a river"),
        ("Kings Canyon in the Northern Territory", "Water and weathering cut deep into the sandstone.", "erosion by water"),
        ("the Jenolan Caves in New South Wales", "Water slowly dissolved the limestone.", "weathering by water (dissolving)"),
        ("the gibber plains in the outback", "Wind blew away the fine sand and left the stones behind.", "erosion by wind"),
        ("London Arch near Port Campbell", "Waves wore away the cliff and made an arch; part of it fell in 1990.", "erosion by waves"),
        ("the Bungle Bungles in Western Australia", "Rain and running water wore the sandstone into rounded domes.", "erosion by water"),
        ("the wide floodplain beside the Hawkesbury River", "Floods dropped layers of mud on the land.", "deposition by floods"),
        ("the Pinnacles in Nambung National Park", "Wind blew away the sand around pillars of limestone.", "erosion by wind")]


def g_land():
    n, why, p = R.choice(LAND)
    w = sorted({x[2] for x in LAND if x[2] != p})
    return tq("Which process mainly formed %s?" % n, p, R.sample(w, 3), why)


ORD = [("rock breaks into pieces", "pieces are picked up", "pieces are carried away", "pieces are dropped")]


def g_order():
    k = R.choice(["first", "second", "third", "last"])
    i = ["first", "second", "third", "last"].index(k)
    return tq("A cliff is changed by weathering, erosion, transportation and deposition. Which step usually comes %s?" % k,
              PROC[i], [x for x in PROC if x != PROC[i]], "The usual order: weathering, erosion, transportation, deposition.")


POOL1 = pool(R, [
    ("Which word means rock breaking into smaller pieces without being moved?", "weathering", ["erosion", "deposition", "transportation"], "Weathering happens in place."),
    ("Which word means dropping sand, mud or pebbles in a new place?", "deposition", ["weathering", "erosion", "evaporation"], "Deposition happens when the moving water or wind slows down."),
    ("Where does a river drop most of its sand and mud?", "where it slows down, such as at its mouth", ["at the fastest part of the river", "at the top of a waterfall", "only during droughts"], "Slow water cannot carry as much."),
    ("Why do pebbles in a river become round?", "They knock against each other and wear away their sharp edges.", ["They melt in the water.", "They grow rounder over time.", "Fish shape them."], "This happens as they are transported."),
    ("Which change happens fastest?", "a landslide after heavy rain", ["a river carving a canyon", "a sea cliff wearing back", "a dune slowly moving inland"], "Some changes take minutes; others take thousands of years."),
    ("Which change is usually slowest?", "wind smoothing a large rock", ["a flood leaving mud", "a rockfall", "a storm washing away a beach"], "Weathering by wind can take thousands of years."),
    ("Why does bare soil erode more than soil covered by grass?", "Roots hold the soil and leaves slow the rain.", ["Grass makes the soil heavier.", "Grass makes the rain warmer.", "Bare soil is always wet."], "Plants protect soil."),
    ("What can farmers plant to reduce wind erosion?", "rows of trees as windbreaks", ["nothing", "more bare paddocks", "plastic flowers"], "Windbreaks slow the wind."),
    ("Which of these is caused by deposition?", "a sandbar at the mouth of a creek", ["a crack in a rock", "a cave in limestone", "a cliff falling into the sea"], "A sandbar forms where sand is dropped."),
    ("Uluru is made of sandstone. How did its surface get its caves and grooves?", "Weathering and erosion over millions of years", ["People carved them", "A single storm", "An earthquake last year"], "These are very slow changes."),
])
POOL5 = pool(R, [
    ("Jack says, 'Weathering and erosion are the same thing.' Which reply is best?", "Weathering breaks rock; erosion moves the pieces away.", ["They are the same.", "Erosion breaks rock; weathering moves it.", "Neither changes the land."], "One breaks, the other moves."),
    ("Mia puts sugar cubes in a jar and shakes it for 2 minutes, then 4, then 6. The cubes get smaller each time. What does this model?", "rocks being worn down as they knock together", ["rocks melting", "plants growing", "volcanoes erupting"], "Shaking models rocks rolling in a river."),
    ("In a stream table, which change would carry the most sand away?", "a steeper slope and more water", ["a flatter slope and less water", "the same slope and no water", "covering the sand with grass"], "Faster water erodes and carries more."),
    ("Chloe pours 500 mL of water on two trays of soil. One is bare; one has grass. The bare tray loses 120 g of soil. Which result is most likely for the grass tray?", "about 20 g", ["about 120 g", "about 300 g", "about 500 g"], "Grass roots hold the soil."),
    ("Which variable should stay the same when testing how slope affects erosion?", "the amount of water poured", ["the slope", "the amount of soil washed away", "nothing"], "Only the slope should change."),
    ("A beach lost 3 m of sand in a big storm. Over the next 6 months it gained 1 m back each 2 months. How wide is it now compared with before the storm?", "the same as before", ["3 m narrower", "6 m wider", "1 m narrower"], "Erosion in the storm, deposition afterwards: 1 m × 3 = 3 m."),
    ("Kai blows through a straw at a pile of sand and gravel. What does he see?", "The fine sand moves further than the gravel.", ["The gravel moves further than the sand.", "Nothing moves.", "The sand turns into gravel."], "Wind can carry light pieces further."),
    ("Ruby photographs a creek bank every month for a year. The bank moves back 40 cm. Which question does this answer?", "How fast is the creek eroding its bank?", ["Why is the water brown?", "How many fish live in the creek?", "What will the weather be tomorrow?"], "Repeated photos measure slow change."),
    ("Ella builds two model sand dunes. She covers one with spinifex grass cuttings and blows a fan at both. What is she testing?", "whether plants reduce wind erosion", ["whether fans use electricity", "whether sand is heavy", "whether grass grows in sand"], "The plants are the variable she changed."),
    ("A stream table has water flowing on a gentle slope. Where will most sand be dropped?", "at the bottom, where the water spreads out and slows", ["at the top, where the water starts", "in the middle of the fastest part", "nowhere"], "Slow water deposits sand."),
])


def main():
    sets = U.sets([
        ("Four processes", [(POOL1, 5), (us_b1, 7), (g_order, 4), (g_proc, 4)]),
        ("What is happening?", [(g_proc, 10), (g_agent, 6), (POOL1, 2), (us_speed, 2)]),
        ("Water, wind, ice and gravity", [(g_agent, 10), (g_proc, 4), (us_plants, 1), (POOL1, 2), (us_speed, 2), (g_land, 1)]),
        ("Australian landforms", [(g_land, 9), (us_b5, 4), (us_speed, 5), (g_proc, 2)]),
        ("Investigations", [(POOL5, 9), (us_slope, 3), (us_water, 1), (us_b5, 1), (us_speed, 4), (g_agent, 2)]),
    ])
    make_au(YEAR, "weathering-erosion-and-deposition", SORT, "AC9S5U02", "Earth and space sciences",
            "Describe how weathering, erosion, transportation and deposition cause slow or rapid change to Earth's surface "
            "(Australian Curriculum v9.0 Science content description).",
            "Weathering, Erosion and Deposition", "Weathering and erosion",
            "Free Year 5 science worksheets on weathering, erosion, transportation and deposition, with Australian landforms such as the "
            "Twelve Apostles and Uluru. 100 questions with answers.",
            "Break, pick up, carry, drop.", "Weathering breaks rock, erosion and transportation move it, deposition drops it.",
            "<p><b>Four processes change the land: weathering, erosion, transportation and deposition.</b></p><ul>"
            "<li>Weathering breaks rock where it is (ice in cracks, roots, heat and cold, water dissolving limestone).</li>"
            "<li>Erosion picks the pieces up; transportation carries them by water, wind, ice, waves or gravity.</li>"
            "<li>Deposition drops them where the water or wind slows down: river mouths, beaches, behind fences.</li></ul>",
            [("Ice splits a rock. Which process?", ["the rock breaks but does not move"], "weathering"),
             ("A river drops mud at its mouth. Which process?", ["the water slows down", "it cannot carry the mud"], "deposition")],
            ["Calling the breaking of rock erosion (that is weathering).", "Thinking deposition happens where water is fastest.",
             "Thinking all changes to the land are slow (landslides and floods are fast)."],
            [("What is the difference between weathering and erosion?", "Weathering breaks rock into smaller pieces where it is. Erosion picks up and moves those pieces away."),
             ("How did the Twelve Apostles form?", "Waves eroded caves in the limestone cliffs. The caves became arches, and when the arches collapsed, stacks of rock were left standing."),
             ("How can people reduce erosion?", "Plant grass and trees, build windbreaks and retaining walls, keep stock away from riverbanks and stay on paths in sand dunes.")],
            sets, allow=("london",))


if __name__ == "__main__":
    main()
