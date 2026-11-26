# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Biology): Photosynthesis
  python tools/gen_uk_science_y8_photosynthesis.py
The word equation for photosynthesis, where it happens (chloroplasts, chlorophyll), the adaptations of leaves, stomata
and gas exchange in plants, testing a leaf for starch, factors that affect the rate (light, carbon dioxide, temperature),
minerals plants need, and the dependence of almost all life on photosynthesis.
Reuses the input/output, pondweed and leaf questions of the US Grade 7 unit in British English.
Wrong answers come from real mistakes: "plants get their food from the soil", "plants breathe in carbon dioxide instead
of respiring", "oxygen is an input", "plants photosynthesise at night".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61804)
R = U.R
P = People(R)
uk_sci.USED.clear()
PH = adopt_us("gen_us_science_g7_photosynthesis", U)
us_io, us_elodea, us_leaf = ukm(PH.g_io), ukm(PH.g_elodea), ukm(PH.g_leaf)

ROLE = [("carbon dioxide", "a reactant (input)", "taken in from the air through the stomata"), ("water", "a reactant (input)", "taken up by the roots"),
        ("light", "the energy source", "absorbed by chlorophyll"), ("glucose", "a product (output)", "used for respiration or stored as starch"),
        ("oxygen", "a product (output)", "released through the stomata")]


def g_role():
    s, r, how = R.choice(ROLE)
    k = R.random() < 0.5
    if not once(("ro", s, k)):
        return None
    if k:
        return item("In photosynthesis, what is %s?" % s, r, [x for x in ["a reactant (input)", "a product (output)", "the energy source", "a waste that stops the reaction"] if x != r],
                    "Carbon dioxide + water → glucose + oxygen, using light energy.")
    return item("Which substance in photosynthesis is %s?" % how, s, R.sample([x[0] for x in ROLE if x[0] != s] + ["nitrogen"], 3), "Each substance has a role.")


LEAF = [("Leaves are broad and flat.", "They have a large surface area to absorb light."), ("Leaves are thin.", "Carbon dioxide only has a short distance to diffuse to the cells."),
        ("Palisade cells are near the top of the leaf.", "They get the most light."), ("Palisade cells contain many chloroplasts.", "They can absorb lots of light for photosynthesis."),
        ("The lower surface has many stomata.", "Carbon dioxide can diffuse in and oxygen can diffuse out."), ("Guard cells surround each stoma.", "They open and close the stoma to control water loss."),
        ("The spongy layer has air spaces.", "Gases can move easily between the cells."), ("Leaves have veins (xylem and phloem).", "They bring water and carry away sugars."),
        ("The upper surface has a waxy layer.", "It reduces water loss.")]


def g_leafad():
    s, a = R.choice(LEAF)
    if not once(("la", s)):
        return None
    near = {"Guard cells surround each stoma.", "The upper surface has a waxy layer.", "The lower surface has many stomata.", "The spongy layer has air spaces.", "Leaves are thin."}
    pool = [x[1] for x in LEAF if x[1] != a and not (s in near and x[0] in near)]
    return item("%s How does this help the leaf?" % s, a, R.sample(pool, 3), "Leaf structure fits its job.")


STARCH = ["Boil the leaf in water to kill it and break the cell membranes.", "Put the leaf in hot ethanol to remove the green chlorophyll.",
          "Rinse the leaf in warm water to soften it.", "Spread the leaf on a tile and add iodine solution."]


def g_starch():
    k = R.choice(["first", "eth", "iod", "after", "order", "var"])
    if not once(("st", k)):
        return None
    if k == "first":
        return item("What is the first step in testing a leaf for starch?", STARCH[0], STARCH[1:], "Kill the leaf first.")
    if k == "eth":
        return item("Why is the leaf put in hot ethanol?", "to remove the chlorophyll so the colour change can be seen", ["to add starch", "to make it green", "to feed the leaf"], "Ethanol is flammable: heat it in a water bath.")
    if k == "iod":
        return item("What colour does iodine turn where there is starch?", "blue-black", ["orange-brown", "green", "milky white"], "No starch: it stays orange-brown.")
    if k == "after":
        return item("What comes straight after removing the chlorophyll with ethanol?", STARCH[2], [STARCH[0], STARCH[3], "Put the leaf back on the plant."], "Ethanol makes it brittle.")
    if k == "order":
        return item("Why must ethanol never be heated over a flame?", "It is flammable, so it is heated in a hot water bath.", ["It freezes.", "It turns into iodine.", "It is not flammable."], "Safety.")
    return item("A variegated leaf is green and white. After the starch test, which parts turn blue-black?", "only the parts that were green", ["only the white parts", "the whole leaf", "none of it"], "Only green parts have chlorophyll.")


def g_rate():
    who = P.next()[0]
    d = [10, 20, 30, 40, 50]
    top = R.choice([40, 44, 48, 52, 56, 60])
    v = [top, round(top * 0.55), round(top * 0.3), round(top * 0.18), round(top * 0.1)]
    k = R.choice(["fast", "pattern", "why", "ctrl", "diff", "iv"])
    if not once(("ra", top, k)) or not once(("ra", k), 6 if k == "diff" else 2):
        return None
    tab = table(["Distance of lamp (cm)", "Bubbles of oxygen per minute"], [[str(a), str(b)] for a, b in zip(d, v)])
    intro = tab + "%s moved a lamp away from some pondweed. " % who
    if k == "fast":
        return item(intro + "At which distance was photosynthesis fastest?", "10 cm", ["%d cm" % x for x in d[1:4]], "Most bubbles.")
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The further the lamp, the slower the rate of photosynthesis.", ["The further the lamp, the faster the rate.", "Distance has no effect.", "The rate is fastest at 50 cm."], "Less light, less photosynthesis.")
    if k == "why":
        return item(intro + "Why did the rate fall as the lamp moved away?", "Less light reached the plant.", ["The water got colder.", "There was more carbon dioxide.", "The plant stopped respiring."], "Light intensity is a limiting factor.")
    if k == "ctrl":
        return item(intro + "Which variable must be kept the same?", "the temperature of the water", ["the distance of the lamp", "the number of bubbles", "the time of reading only"], "Lamps can warm the water: use a heat shield.")
    if k == "iv":
        return item(intro + "What is the independent variable?", "the distance of the lamp", ["the number of bubbles", "the type of pondweed", "the temperature"], "What is changed.")
    g = str(v[0] - v[2])
    return item(intro + "How many more bubbles per minute were there at 10 cm than at 30 cm?", g, uniq(g, [str(v[0]), str(v[2]), str(v[0] + v[2]), str(v[0] - v[1])]), "%d − %d = %s." % (v[0], v[2], g))


MIN = [("nitrates", "to make proteins for growth", "poor growth and yellow older leaves"), ("phosphates", "for healthy roots", "poor root growth and purple leaves"),
       ("potassium", "for healthy leaves and flowers", "yellow leaves with dead patches"), ("magnesium", "to make chlorophyll", "yellow leaves")]


def g_min():
    m, use, lack = R.choice(MIN)
    k = R.random() < 0.5
    if not once(("mi", m, k)):
        return None
    if k:
        return item("Why do plants need %s from the soil?" % m, use, R.sample([x[1] for x in MIN if x[1] != use], 3), "Minerals are taken up dissolved in water by the roots.")
    return item("Which mineral do plants need %s?" % use, m, R.sample([x[0] for x in MIN if x[0] != m], 3), "Fertilisers contain these minerals.")


VS = [("uses oxygen", "respiration"), ("releases oxygen", "photosynthesis"), ("needs light", "photosynthesis"), ("happens in all living cells", "respiration"),
      ("releases energy from glucose", "respiration"), ("makes glucose", "photosynthesis"), ("produces carbon dioxide", "respiration"),
      ("takes in carbon dioxide", "photosynthesis"), ("happens in the mitochondria", "respiration"), ("happens in the chloroplasts", "photosynthesis"),
      ("happens in a green leaf in daylight", "both"), ("happens in a root cell", "respiration"), ("happens in a green leaf at night", "respiration")]


def g_vs():
    f, a = R.choice(VS)
    if not once(("vs", f)):
        return None
    return item("Which process %s: photosynthesis, respiration, both or neither?" % f, a, [x for x in ["photosynthesis", "respiration", "both", "neither"] if x != a],
                "Photosynthesis needs light and chloroplasts; respiration happens in every living cell all the time.")


HCI = [("pondweed in bright light", "purple", "Photosynthesis takes in more carbon dioxide than respiration gives out."),
       ("pondweed in the dark", "yellow", "Only respiration happens, so carbon dioxide builds up."),
       ("no living thing (control) in the light", "red (no change)", "Nothing changes the carbon dioxide level."),
       ("pondweed in dim light", "red (no change)", "Photosynthesis and respiration balance."),
       ("a water snail in the light", "yellow", "The snail respires but cannot photosynthesise.")]


def g_hci():
    s, a, e = R.choice(HCI)
    if not once(("hc", s)):
        return None
    tab = table(["Indicator colour", "Carbon dioxide level"], [["yellow", "high"], ["red", "normal (as in air)"], ["purple", "low"]])
    return item(tab + "Hydrogencarbonate indicator is red at the start. A tube contains %s. What colour will the indicator be after a few hours?" % s, a,
                [x for x in ["purple", "yellow", "red (no change)", "blue-black"] if x != a], e)


B1 = bank([
    ("What is the word equation for photosynthesis?", "carbon dioxide + water → glucose + oxygen", ["glucose + oxygen → carbon dioxide + water", "oxygen + water → glucose + carbon dioxide", "glucose → ethanol + carbon dioxide"], "Light is needed; chlorophyll absorbs it."),
    ("Where in a plant cell does photosynthesis happen?", "in the chloroplasts", ["in the nucleus", "in the vacuole", "in the cell wall"], "They contain chlorophyll."),
    ("What is the job of chlorophyll?", "to absorb light energy", ["to store water", "to make the cell wall", "to release carbon dioxide"], "It is green."),
    ("Where does a plant get most of its mass from?", "carbon dioxide from the air (and water)", ["the soil", "fertiliser only", "sunlight"], "Not from the soil."),
    ("Which gas do plants give out during photosynthesis?", "oxygen", ["carbon dioxide", "nitrogen", "hydrogen"], "A product."),
    ("Why are leaves green?", "They contain chlorophyll.", ["They contain starch.", "They reflect all light.", "They are full of water."], "Chlorophyll reflects green light."),
    ("How is glucose stored in plants?", "as starch", ["as fat only", "as oxygen", "as chlorophyll"], "Starch is insoluble."),
    ("How does water reach the leaves?", "through the xylem from the roots", ["through the stomata", "through the phloem from the leaves", "from the air"], "Root hair cells absorb it."),
    ("What are stomata?", "tiny holes in a leaf that let gases in and out", ["green cells", "roots", "seeds"], "Mostly on the lower surface."),
])
B5 = bank([
    ("Why do almost all food chains depend on photosynthesis?", "Plants make the food that the energy in every food chain starts from.", ["Animals make their own glucose.", "Food chains start with the soil.", "Photosynthesis happens in animals too."], "Producers."),
    ("Why do plants photosynthesise only in the light but respire all the time?", "Photosynthesis needs light energy; respiration happens in all living cells.", ["Plants stop respiring at night.", "Respiration needs light.", "Plants never respire."], "Both processes."),
    ("Why do farmers sometimes add extra carbon dioxide to greenhouses?", "Carbon dioxide can limit the rate of photosynthesis, so more of it gives faster growth.", ["Plants breathe it out.", "It makes the greenhouse cooler.", "It kills all pests."], "Limiting factors."),
    ("A plant is kept in the dark for two days and then tested for starch. What is the result?", "No starch: iodine stays orange-brown.", ["Lots of starch: blue-black.", "The leaf turns red.", "The leaf makes oxygen."], "Destarching."),
    ("Why do plants in a dark cupboard turn pale and yellow?", "Without light they cannot make chlorophyll or photosynthesise.", ["They have too much water.", "They are respiring too slowly.", "Dark makes chlorophyll red."], "Light is needed."),
    ("Why do some farmers heat their greenhouses in winter?", "A higher temperature speeds up photosynthesis, up to a point.", ["Heat adds carbon dioxide only.", "Plants need to be hot to respire.", "It stops photosynthesis."], "Temperature is a limiting factor."),
    ("What happens to photosynthesis if the temperature gets very high (over about 45 °C)?", "It slows down because the enzymes are damaged.", ["It keeps getting faster.", "It turns into respiration.", "It makes more chlorophyll."], "Enzymes in chloroplasts."),
    ("How do photosynthesis and respiration keep the air balanced?", "Photosynthesis removes carbon dioxide and adds oxygen; respiration does the opposite.", ["Both add carbon dioxide.", "Both remove oxygen.", "Neither affects the air."], "The carbon cycle."),
    ("Why is cutting down large areas of forest a problem for the air?", "Fewer trees take in carbon dioxide, so more stays in the atmosphere.", ["Trees make carbon dioxide.", "Forests have no effect on air.", "It adds oxygen."], "Deforestation."),
    ("Why does a fertiliser bag list nitrogen, phosphorus and potassium (NPK)?", "They are the main minerals plants need for healthy growth.", ["They are made by photosynthesis.", "They are types of chlorophyll.", "They are poisons for weeds."], "Minerals."),
    ("What are algae?", "simple organisms that photosynthesise, often in water", ["animals that eat plants", "a type of fungus", "bacteria that make carbon dioxide"], "They make much of the world's oxygen."),
    ("Why do plants grow less well in winter?", "There is less light and it is colder, so photosynthesis is slower.", ["There is more carbon dioxide.", "They stop respiring.", "The soil disappears."], "Limiting factors."),
    ("What does a plant use glucose for?", "respiration, making cellulose for cell walls and storing as starch", ["only making oxygen", "nothing", "making chlorophyll from light"], "Many uses."),
    ("Why does a photosynthesis rate stop rising when light gets very bright?", "Something else, such as carbon dioxide or temperature, becomes the limiting factor.", ["The plant dies.", "Light stops being energy.", "Chlorophyll turns red."], "Limiting factors."),
])


def body():
    think = ("<p><b>Plants make their own food by photosynthesis.</b></p>"
             "<ul><li>carbon dioxide + water → glucose + oxygen (light energy is absorbed by chlorophyll in chloroplasts).</li>"
             "<li>Leaves are broad and thin, with stomata for gas exchange and palisade cells full of chloroplasts.</li>"
             "<li>Light, carbon dioxide and temperature affect the rate. Plants also need minerals such as nitrates from the soil.</li></ul>")
    ex = [("Lamp moved further away. Rate?", ["Less light"], "slower"),
          ("Is oxygen a reactant or a product?", ["Look at the equation"], "a product")]
    mist = ["Thinking plants get their food from the soil.", "Thinking oxygen is an input.", "Thinking plants do not respire."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("The equation", B1 + [(g_role, 6), (us_io, 5)]),
        ("Leaves", [(g_leafad, 8), (g_min, 6), (us_leaf, 2), (us_io, 4)]),
        ("Starch and gases", [(g_starch, 5), (g_hci, 5), (g_vs, 6), (g_role, 3), (us_leaf, 1)]),
        ("Rate of photosynthesis", [(g_rate, 13), (us_elodea, 2), (g_vs, 5), (g_role, 2)]),
        ("Plants and life", B5 + [(g_vs, 2), (g_rate, 2), (g_starch, 1), (us_elodea, 1), (g_min, 2), (us_io, 1)]),
    ])
    make_ks3(8, "photosynthesis", 4, "Biology", "Material cycles and energy",
             "The reactants in, and products of, photosynthesis, and a word summary for photosynthesis; the dependence of almost all life on Earth on the ability of photosynthetic organisms, such as plants and algae, to use sunlight in photosynthesis to build organic molecules that are an essential energy store and to maintain levels of oxygen and carbon dioxide in the atmosphere; the adaptations of leaves for photosynthesis; the role of leaf stomata in gas exchange in plants; plants making carbohydrates in photosynthesis and gaining mineral nutrients and water from the soil via their roots.",
             "Photosynthesis",
             "Year 8 Science: Photosynthesis Worksheets (Word Equation, Leaves, Starch Test)",
             "Photosynthesis",
             "Free Year 8 science worksheets on photosynthesis: the word equation, chloroplasts, leaf adaptations, stomata, the starch test, the rate of photosynthesis and minerals. 100 questions with answers.",
             "Plants make glucose from carbon dioxide and water.",
             "Light energy is absorbed by chlorophyll; oxygen is given off.",
             body(),
             [("What is the word equation for photosynthesis?", "Carbon dioxide + water → glucose + oxygen. Light energy is needed and is absorbed by chlorophyll."),
              ("How do you test a leaf for starch?", "Boil it in water, warm it in ethanol in a water bath to remove the chlorophyll, rinse it, then add iodine. Blue-black means starch."),
              ("What affects the rate of photosynthesis?", "Light intensity, carbon dioxide concentration and temperature. The one in shortest supply limits the rate.")],
             sets)


if __name__ == "__main__":
    main()
