# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U02: slow and rapid changes to Earth's surface.
  python tools/gen_au_science_y5_slow_and_rapid_changes_to_earths_surface.py
Fast changes (earthquakes, landslides, floods, storm surges, volcanic eruptions) and slow changes (weathering, canyons,
moving dunes), with Australian events: the Newcastle earthquake, the Thredbo landslide, Cyclone Tracy, Mount Gambier.
Reuses the US Grade 2 fast/slow makers and the US Grade 4 natural hazard makers with Australian names.
Wrong answers come from real mistakes: thinking all big changes are slow, thinking people can stop earthquakes, and mixing
up the cause of a change with its effect.
"""
from au_sci import AU, seed_of, make_au, tq, pool

YEAR, SORT = 5, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

G2 = "gen_us_science_g2_fast_and_slow_earth_changes"
HZ = "gen_us_science_g4_natural_hazards"
us2_which = src(G2, "g_which")
us2_source = src(G2, "g_source", drop=["feet", "foot"])
us2_pic = src(G2, "g_pic")
us2_b5 = src.B(G2, "B5", drop=["foot", "feet", "Grand Canyon"])
hz_what = src(HZ, "g_what", drop=["tornado", "hurricane"])
hz_which = src(HZ, "g_which", drop=["tornado", "hurricane"])
hz_b1 = src.B(HZ, "B1")
hz_b5 = src.B(HZ, "B5")

EV = [("an earthquake", "fast", "seconds to minutes", "cracks the ground and can make buildings fall"),
      ("a landslide", "fast", "minutes", "moves soil and rock down a slope"),
      ("a flash flood", "fast", "hours", "washes away soil and leaves mud behind"),
      ("a volcanic eruption", "fast", "hours to days", "covers the land with lava and ash"),
      ("a storm surge in a cyclone", "fast", "hours", "washes away beaches and sand dunes"),
      ("a tsunami", "fast", "minutes to hours", "floods the coast and carries away sand"),
      ("a rockfall from a cliff", "fast", "seconds", "drops boulders at the bottom of the cliff"),
      ("a sinkhole opening", "fast", "minutes", "makes a sudden hole in the ground"),
      ("a river carving a gorge", "slow", "thousands to millions of years", "makes a deep valley"),
      ("wind wearing down a rock", "slow", "thousands of years", "smooths and shapes the rock"),
      ("a sand dune moving inland", "slow", "many years", "buries the land behind it"),
      ("waves wearing back a cliff", "slow", "hundreds to thousands of years", "moves the coastline inland"),
      ("a mountain range wearing down", "slow", "millions of years", "makes the mountains lower and rounder"),
      ("mud building up at a river mouth", "slow", "hundreds of years", "makes new land at the coast"),
      ("water dissolving a limestone cave", "slow", "thousands of years", "makes caves and tunnels underground"),
      ("tree roots cracking a rock", "slow", "many years", "breaks the rock into pieces")]


def g_fs():
    e, sp, t, eff = R.choice(EV)
    return tq("Is %s a fast change or a slow change to Earth's surface?" % e, sp,
              ["slow" if sp == "fast" else "fast", "no change at all", "a change only in the air"],
              "%s takes %s." % (e[0].upper() + e[1:], t))


def g_time():
    e, sp, t, eff = R.choice(EV)
    w = sorted({x[2] for x in EV if (x[1] != sp)} - {t})
    near = sorted({x[2] for x in EV if x[1] == sp and x[2] != t})
    ws = R.sample(w, 2) + R.sample(near, 1) if near else R.sample(w, 3)
    return tq("About how long does %s take to change the land?" % e, t, ws, "It is a %s change." % sp)


def g_effect():
    e, sp, t, eff = R.choice(EV)
    w = sorted({x[3] for x in EV if x[0] != e})
    return tq("How does %s change Earth's surface?" % e, "It " + eff + ".", ["It " + x + "." for x in R.sample(w, 3)],
              "%s %s." % (e[0].upper() + e[1:], eff))


AUE = [("In 1989 the ground shook in Newcastle, New South Wales, and buildings were damaged in seconds.", "an earthquake"),
       ("In 1997 a hillside above Thredbo village slid down in a few seconds after water soaked the soil.", "a landslide"),
       ("In 1974 Cyclone Tracy hit Darwin with very strong winds and big waves.", "a tropical cyclone"),
       ("Mount Gambier in South Australia formed when hot, melted rock came out of the ground thousands of years ago.", "a volcanic eruption"),
       ("In 2022 heavy rain made the Wilsons River rise quickly and cover the streets of Lismore.", "a flood"),
       ("Rocks often break off the sandstone cliffs at Sydney's beaches and land on the rocks below.", "a rockfall"),
       ("In 2011 Brisbane River water rose and covered many suburbs in mud.", "a flood"),
       ("In 2016 huge storm waves washed away sand and parts of backyards at Collaroy Beach.", "a storm surge")]


def g_au():
    s, k = R.choice(AUE)
    w = sorted(({x[1] for x in AUE} | {"slow weathering", "a drought"}) - {k} - ({"a storm surge", "a tropical cyclone"} if k in ("a storm surge", "a tropical cyclone") else set()))
    return tq("%s What kind of event was this?" % s, k, R.sample([x for x in w if x != k], 3), "This was a rapid change to Earth's surface.")


POOL1 = pool(R, [
    ("Which of these changes Earth's surface fastest?", "a landslide", ["a river carving a gorge", "wind smoothing a rock", "a mountain wearing down"], "A landslide can happen in minutes."),
    ("Which of these changes Earth's surface slowest?", "a mountain range wearing down", ["an earthquake", "a flash flood", "a rockfall"], "This takes millions of years."),
    ("Can people stop earthquakes from happening?", "No, but they can build stronger buildings to reduce damage.", ["Yes, by building walls.", "Yes, by planting trees.", "Yes, by digging holes."], "We can plan for hazards but not stop them."),
    ("Why are landslides more likely after very heavy rain?", "Water makes the soil heavy and slippery.", ["Rain makes rocks lighter.", "Rain dries out the hill.", "Rain makes the ground freeze."], "Wet soil slides more easily."),
    ("What is a natural hazard?", "a natural event that can harm people or property", ["a factory making pollution", "a rubbish tip", "a new road"], "Earthquakes, floods and cyclones are natural hazards."),
    ("Which kind of change made most of Australia's landforms, such as Uluru?", "slow weathering and erosion over millions of years", ["one big earthquake", "a single flood", "a volcanic eruption last century"], "Australia's landscape is very old and worn down."),
    ("Does Australia have active volcanoes on the mainland today?", "No. The last eruptions on the mainland were thousands of years ago.", ["Yes, many erupt every year.", "Yes, Uluru is a volcano.", "Yes, in every state."], "Mount Gambier and Tower Hill erupted thousands of years ago."),
    ("Why can a cyclone change a beach quickly?", "Strong winds push big waves that carry away sand.", ["Cyclones only bring sunshine.", "Cyclones freeze the sand.", "Cyclones make the beach grow."], "Storm surges cause rapid erosion."),
    ("How can a flood change the land quickly?", "It erodes soil and drops mud in new places.", ["It turns rock into lava.", "It builds mountains.", "It makes caves in seconds."], "Floods cause both erosion and deposition."),
    ("Which of these is the effect of an earthquake, not its cause?", "cracked roads", ["moving plates of rock deep underground", "stress building up in rock", "rock slipping along a fault"], "The cause is underground; the effect is what we see."),
])
POOL5 = pool(R, [
    ("Mia compares two photos of a cliff taken 60 years apart. The cliff has moved back 3 m. How much did it move each 20 years, on average?", "1 m", ["3 m", "20 m", "60 m"], "3 m ÷ 3 = 1 m each 20 years. This is a slow change."),
    ("Jack shakes a tray with two model buildings. One is tall and thin, one is short and wide. Which is more likely to fall?", "the tall, thin one", ["the short, wide one", "both the same", "neither"], "A wide base is more stable."),
    ("Ruby says, 'Big changes to the land are always slow.' Which example shows she is wrong?", "A landslide can move a whole hillside in minutes.", ["A canyon takes millions of years.", "Dunes move slowly.", "Rock weathers slowly."], "Some big changes are rapid."),
    ("A town measures how high the river rises during a storm every 30 minutes. What can this data help them do?", "warn people before a flood", ["stop the rain", "make the river shorter", "stop the clouds"], "Data helps plan for hazards."),
    ("Which evidence shows a slow change to the land?", "rock layers worn down over thousands of years", ["a video of lava flowing", "photos of a landslide on a road", "a news report about an earthquake"], "Slow changes need evidence from long times."),
    ("Ella makes a model hill of wet sand and dry sand. She pours the same water on both. What is she testing?", "whether wet soil slides more easily", ["whether sand is yellow", "how heavy the tray is", "whether water evaporates"], "The variable is how wet the sand is."),
    ("Scientists put sensors on a hill that is slowly moving. Why?", "to warn people if the movement speeds up", ["to make the hill move", "to measure rainfall only", "to stop the hill moving"], "Monitoring helps reduce harm."),
    ("Which is the best way to keep people safe from storm surges at the coast?", "keep houses back from the beach and keep dunes covered with plants", ["build houses on the sand at the water's edge", "remove plants from dunes", "dig sand away from the beach"], "Dunes and plants absorb wave energy."),
])


def main():
    sets = U.sets([
        ("Fast or slow?", [(g_fs, 8), (us2_which, 8), (POOL1, 4)]),
        ("How long does it take?", [(g_time, 9), (us2_source, 6), (us2_pic, 3), (POOL1, 2)]),
        ("Rapid events", [(g_effect, 10), (g_au, 6), (hz_b1, 4)]),
        ("Reducing damage", [(hz_what, 8), (hz_which, 7), (POOL1, 3), (hz_b1, 2)]),
        ("Evidence and investigations", [(POOL5, 8), (hz_b5, 5), (us2_b5, 2), (g_au, 2), (us2_which, 3)]),
    ])
    make_au(YEAR, "slow-and-rapid-changes-to-earths-surface", SORT, "AC9S5U02", "Earth and space sciences",
            "Describe how weathering, erosion, transportation and deposition cause slow or rapid change to Earth's surface "
            "(Australian Curriculum v9.0 Science content description).",
            "Slow and Rapid Changes to Earth's Surface", "Slow and rapid changes",
            "Free Year 5 science worksheets on slow and rapid changes to Earth's surface: earthquakes, landslides, floods, cyclones and "
            "slow weathering, with Australian examples. 100 questions with answers.",
            "Some changes take seconds, others millions of years.", "Earthquakes and landslides are fast; weathering and canyons are slow.",
            "<p><b>Earth's surface changes all the time, some quickly and some very slowly.</b></p><ul>"
            "<li>Rapid changes take seconds to days: earthquakes, landslides, floods, storm surges, volcanic eruptions.</li>"
            "<li>Slow changes take years to millions of years: weathering, rivers carving gorges, dunes moving, mountains wearing down.</li>"
            "<li>People cannot stop natural hazards, but they can reduce the damage with warnings, stronger buildings and careful planning.</li></ul>",
            [("Thredbo, 1997: a hillside slid in seconds. Fast or slow?", ["it happened in seconds"], "fast (a landslide)"),
             ("A river makes a gorge. How long?", ["the water wears away rock a little at a time"], "thousands to millions of years")],
            ["Thinking that big changes are always slow.", "Thinking people can stop earthquakes or cyclones.",
             "Mixing up the cause of a change (rock slipping underground) with its effect (cracked roads)."],
            [("What are some rapid changes to Earth's surface?", "Earthquakes, landslides, floods, tsunamis, storm surges during cyclones and volcanic eruptions can change the land in seconds, hours or days."),
             ("Why does Australia have so few earthquakes and volcanoes?", "Australia is in the middle of a large plate of rock, far from the edges where most earthquakes and volcanoes happen. Small earthquakes still happen, such as the Newcastle earthquake in 1989."),
             ("How do people reduce damage from natural hazards?", "They use warning systems, build stronger buildings, avoid building on flood plains and steep loose slopes, and keep sand dunes covered with plants.")],
            sets)


if __name__ == "__main__":
    main()
