# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Coevolution of Life and Earth (HS-ESS2-7)
  python tools/gen_us_science_ess_coevolution_of_life_and_earth.py
Construct an argument based on evidence about the simultaneous coevolution of Earth's systems and life on Earth.
How life changed Earth (oxygen from cyanobacteria, banded iron, the ozone layer, soils, limestone, coal) and how Earth
changed life (oxygen allowing animals, ozone allowing land life, ice ages, impacts, moving continents), the timeline,
and oxygen data.
Wrong answers come from real mistakes: "Earth always had oxygen", "life only adapts and never changes Earth",
"animals made the first oxygen", "dinosaurs and the first life lived at the same time".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90413)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


LIFE2EARTH = [("Cyanobacteria began photosynthesis in the oceans.", "Oxygen built up in the oceans and atmosphere."),
              ("Oxygen from microbes reacted with iron dissolved in seawater.", "Banded iron formations were deposited on the seafloor."),
              ("Oxygen made by microbes rose high into the atmosphere, where UV light turned some of it into ozone.", "An ozone layer formed that blocks harmful UV."),
              ("Plants spread onto land and their roots broke up rock.", "Soils formed and rock weathering sped up, pulling CO₂ from the air."),
              ("Corals and shelled plankton built skeletons from calcium carbonate.", "Thick layers of limestone and chalk formed."),
              ("Huge swamp forests grew and were buried before they decayed.", "Coal deposits formed and atmospheric CO₂ dropped."),
              ("Beavers built dams across streams.", "Wetlands and ponds formed, changing water flow."),
              ("Mangrove forests trapped mud along tropical coasts.", "Coastlines were protected and new land built up.")]
EARTH2LIFE = [("Oxygen in the air rose to high levels.", "Large, active animals that need lots of oxygen could evolve."),
              ("An ozone layer formed in the upper atmosphere.", "Living things could survive on land, safe from strong UV."),
              ("An asteroid struck Earth 66 million years ago.", "Non-bird dinosaurs went extinct and mammals spread."),
              ("Continents drifted apart.", "Populations were separated and evolved into different species."),
              ("Ice ages lowered sea level and opened land bridges.", "Animals and people migrated between continents."),
              ("Volcanic eruptions released huge amounts of CO₂ 252 million years ago.", "Rapid warming and ocean changes caused the largest mass extinction.")]


@safe
def g_l2e():
    s, a = R.choice(LIFE2EARTH)
    k = R.random() < 0.6
    if not once(("le", s, k)):
        return None
    if k:
        return item("%s How did this change Earth's systems?" % s, a, R.sample([x[1] for x in LIFE2EARTH if x[1] != a], 3), "Life changes the atmosphere, oceans and rocks.")
    return item("Which change in living things caused this: %s" % a, s, R.sample([x[0] for x in LIFE2EARTH if x[0] != s], 3), "Match the cause in the biosphere.")


@safe
def g_e2l():
    s, a = R.choice(EARTH2LIFE)
    k = R.random() < 0.6
    if not once(("el", s, k)):
        return None
    if k:
        return item("%s How did this affect life?" % s, a, R.sample([x[1] for x in EARTH2LIFE if x[1] != a], 3), "Changes in Earth's systems shape evolution.")
    return item("Which change to Earth led to this: %s" % a, s, R.sample([x[0] for x in EARTH2LIFE if x[0] != s], 3), "Match the Earth change.")


TL = [("the first single-celled life", 3.7), ("the first oxygen-making cyanobacteria", 2.7), ("the Great Oxidation Event", 2.4), ("the first complex (eukaryotic) cells", 1.8),
      ("the first animals", 0.6), ("the first land plants", 0.47), ("the first forests", 0.38), ("the first dinosaurs", 0.23), ("the asteroid that ended the dinosaurs", 0.066)]


@safe
def g_tl():
    a, b = R.sample(TL, 2)
    if not once(("tl", tuple(sorted((a[0], b[0]))))):
        return None
    first, second = sorted([a, b])
    old = a if a[1] > b[1] else b
    new = b if old is a else a
    return item("Which came first: %s, or %s?" % (first[0], second[0]), old[0], [new[0], "They happened at the same time.", "Neither has happened yet."],
                "%s: about %s billion years ago; %s: about %s billion years ago." % (old[0][0].upper() + old[0][1:], num(old[1], 3), new[0], num(new[1], 3)))


@safe
def g_oxy():
    who = P.next()[0]
    tab = table(["Billion years ago", "Oxygen in the atmosphere (% of today's level)"], [["3.0", "less than 0.001"], ["2.2", "about 1"], ["1.0", "about 2"], ["0.6", "about 20"], ["0.3", "about 150"], ["0", "100"]])
    k = R.choice(["first", "animals", "peak", "cause", "now", "jump", "times", "gap"])
    if not once(("ox", k, who)) or not once(("oxk", k), 2):
        return None
    if k == "first":
        return item(tab + "According to %s's table, when did oxygen first rise noticeably?" % who, "between 3.0 and 2.2 billion years ago", ["in the last 1 million years", "4.5 billion years ago", "it never rose"], "The Great Oxidation Event, about 2.4 billion years ago.")
    if k == "animals":
        return item(tab + "Animals appear in the fossil record about 0.6 billion years ago. What does %s's table suggest about why?" % who, "Oxygen had risen enough to support larger, active organisms.",
                    ["Oxygen dropped to zero.", "Animals made the first oxygen.", "Oxygen has no effect on animals."], "Timing of evidence supports the claim.")
    if k == "peak":
        return item(tab + "In %s's table, when was oxygen higher than today?" % who, "about 0.3 billion years ago", ["3.0 billion years ago", "2.2 billion years ago", "never"], "The Carboniferous: huge forests and giant insects.")
    if k == "jump":
        return item(tab + "In %s's table, between which times did oxygen rise from about 2%% to about 20%% of today's level?" % who, "between 1.0 and 0.6 billion years ago",
                    ["between 3.0 and 2.2 billion years ago", "between 0.3 billion years ago and today", "between 2.2 and 1.0 billion years ago"], "This second rise came just before animals appear.")
    if k == "times":
        return item(tab + "About how many times today's oxygen level was there 0.3 billion years ago, in %s's table?" % who, "about 1.5 times", ["about 150 times", "about 0.15 times", "about 15 times"], "150% = 1.5 × today.")
    if k == "gap":
        return item(tab + "Oxygen first rose about 2.4 billion years ago, and animals appeared about 0.6 billion years ago. About how long did animals take to appear, according to %s's notes?" % who, "about 1.8 billion years",
                    ["about 3.0 billion years", "about 0.6 billion years", "about 18 million years"], "2.4 − 0.6 = 1.8 billion years.")
    if k == "cause":
        return item(tab + "What most likely caused the first rise of oxygen in %s's table?" % who, "photosynthesis by cyanobacteria", ["volcanic eruptions", "meteorite impacts", "animal breathing"], "Life changed the atmosphere.")
    return item(tab + "How does oxygen today compare with 3.0 billion years ago in %s's table?" % who, "It is far higher today.", ["It is lower today.", "It is the same.", "There was more oxygen then."], "From almost none to about 21% of air.")


@safe
def g_cls():
    rows = [(c, "Life changed Earth's systems.") for c, _ in LIFE2EARTH] + [(c, "Earth's systems changed life.") for c, _ in EARTH2LIFE]
    c, t = R.choice(rows)
    if not once(("cl", c)):
        return None
    o = "Earth's systems changed life." if t.startswith("Life") else "Life changed Earth's systems."
    return item("Which direction of coevolution does this show? %s" % c, t, [o, "Neither changed the other.", "The two changes were unrelated."], "Ask: is the cause living things, or Earth's systems?")


B1 = bank([
    ("What is coevolution of Earth and life?", "Life and Earth's systems change each other over time.", ["Life adapts but never changes Earth.", "Earth never changes.", "Only rocks evolve."], "Two-way changes."),
    ("Where did most of the oxygen in Earth's air come from?", "photosynthesis by microbes and plants", ["volcanoes", "the Sun", "meteorites"], "Biosphere → atmosphere."),
    ("Did early Earth's atmosphere have much oxygen?", "No. It had almost no free oxygen.", ["Yes, about 21%.", "Yes, more than today.", "It was pure oxygen."], "Before cyanobacteria."),
    ("Why did life on land only become common after the ozone layer formed?", "Ozone blocks harmful ultraviolet radiation.", ["Ozone gave food.", "Ozone made rain.", "Ozone warmed the land."], "UV protection."),
    ("How do plant roots change rock?", "They break and chemically weather rock, helping form soil.", ["They make rock harder.", "They have no effect.", "They turn rock into metal."], "Biological weathering."),
    ("What are banded iron formations evidence of?", "oxygen starting to build up in the oceans", ["ancient forests", "dinosaur nests", "volcanic ash"], "Rusting seas."),
    ("How did the first forests affect atmospheric CO₂?", "They pulled CO₂ from the air and buried carbon as coal.", ["They added CO₂.", "They had no effect.", "They made methane only."], "Carbon storage."),
    ("What do stromatolites show?", "Mats of microbes lived in shallow seas billions of years ago.", ["Dinosaurs lived in deserts.", "Early life lived on land.", "Plants were the first life."], "Early life evidence."),
])
B5 = bank([
    ("A student claims oxygen in the air came from volcanoes. Which evidence best argues against this?", "Volcanoes release little oxygen gas; oxygen rose only after photosynthesizing microbes appeared.",
     ["Volcanoes are hot.", "Oxygen is invisible.", "Plants do not exist."], "Evidence-based argument."),
    ("Why do scientists study Mars and Venus when thinking about Earth's coevolution?", "Their atmospheres show what a planet without abundant life may look like.", ["They have forests.", "They have oceans of oxygen.", "They are younger than the Sun."], "Comparison."),
    ("Coral reefs are dying in warm, acidic water. How could this change Earth's systems?", "Less limestone would form and coasts would lose protection from waves.", ["Nothing would change.", "More limestone would form.", "Oceans would cool."], "Biosphere → geosphere."),
    ("Which evidence best supports that land plants sped up rock weathering?", "Soil and sediment layers changed sharply when plant fossils appear.", ["Plants are green.", "Rocks are older than plants.", "Plants need water."], "Rock record."),
    ("How did the mass extinction 66 million years ago show Earth changing life?", "An asteroid impact changed climate quickly, wiping out many groups.", ["Dinosaurs evolved into rocks.", "Mammals caused the impact.", "Life changed the asteroid."], "Geosphere/space → biosphere."),
])


def body():
    think = ("<p><b>Life and Earth have changed each other for billions of years.</b></p>"
             "<ul><li>Life → Earth: cyanobacteria made oxygen (banded iron, ozone layer); plants made soil and coal; corals made limestone.</li>"
             "<li>Earth → life: oxygen and ozone allowed animals and land life; impacts, eruptions, ice ages and drifting continents drove extinctions and new species.</li>"
             "<li>Arguments use evidence from rocks, fossils and the timing of events.</li></ul>")
    ex = [("Banded iron formations appear ~2.4 billion years ago. What do they show?", ["Iron rusted out of seawater"], "oxygen was building up"),
          ("Land plants spread. Effect on CO₂?", ["More weathering and buried carbon"], "CO₂ fell")]
    mist = ["Thinking Earth always had oxygen.", "Thinking life only adapts and never changes Earth.", "Thinking animals made the first oxygen."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Life changes Earth", B1 + [(g_l2e, 12)]),
        ("Earth changes life", [(g_e2l, 10), (g_l2e, 4), (g_tl, 6)]),
        ("Timeline of coevolution", [(g_tl, 16), (g_oxy, 4)]),
        ("Oxygen evidence", [(g_oxy, 8), (g_tl, 6), (g_e2l, 2), (g_cls, 4)]),
        ("Building an argument", B5 + [(g_tl, 4), (g_oxy, 3), (g_cls, 8)]),
    ])
    make("earth-and-space-science", "coevolution-of-life-and-earth", 13, "HS-ESS2-7",
         "Construct an argument based on evidence about the simultaneous coevolution of Earth's systems and life on Earth.",
         "Coevolution of Life and Earth",
         "Coevolution of Life and Earth Worksheets: Oxygen, Ozone and Mass Extinctions (Earth Science)",
         "Life and Earth",
         "Free high school Earth and space science worksheets on the coevolution of life and Earth (NGSS HS-ESS2-7): oxygen from cyanobacteria, banded iron, ozone, soils, extinctions and the timeline of life. 100 questions with answers.",
         "Life and Earth change each other.",
         "Microbes made oxygen; oxygen, ozone and impacts then shaped what could live.",
         body(),
         [("What does coevolution of life and Earth mean?", "Living things change Earth's air, water and rocks, and those changes in turn affect which living things can survive and evolve."),
          ("Where did Earth's oxygen come from?", "From photosynthesis, first by cyanobacteria in the oceans starting about 2.7 billion years ago, and later by algae and plants."),
          ("How did the ozone layer help life?", "Ozone formed from oxygen and blocks harmful ultraviolet light, which made it possible for plants and animals to live on land.")],
         sets)


if __name__ == "__main__":
    main()
