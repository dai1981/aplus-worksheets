# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Man's impact on the environment (Interactions)
  python tools/gen_sg_science_p6_mans_impact_on_the_environment.py
People change the environment: clearing forests, polluting air, water and land, and burning fuels that add
carbon dioxide and cause global warming. People can also protect it: the 3Rs (reduce, reuse, recycle),
nature reserves (Sungei Buloh, Central Catchment), planting trees and saving water and electricity.
Singapore context: Semakau Landfill, NEWater, the haze, blue recycling bins, bring-your-own-bag.
Wrong answers come from real mistakes: "recycling is the same as reusing", "cutting down forests only affects
the trees", "global warming is caused by the hole in the ozone layer".
US Grade 7 human impact and UK Year 4 changing environments makers are reused.
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63609)
R = U.R
P = People(R)
HI = use(U, "gen_us_science_g7_human_impact_on_the_environment", rep=[("transit", "transport"), ("program", "programme")],
         drop=["stream", "rain garden", "wildlife bridge", "lake", "billion", "petrol", "farm", "fertilizer", "fertiliser"])
CE = use(U, "gen_uk_science_y4_changing_environments", drop=["autumn", "hedgerow", "meadow", "wood.", "a wood", "farmland", "bird boxes", "Moon", "orangutan"])

R3 = {
    "reduce": ["bringing your own bag to the supermarket", "printing on both sides of the paper", "switching off the lights when you leave a room",
               "buying drinks in large bottles instead of many small ones", "taking a shorter shower", "saying no to a plastic straw", "buying only the food your family will eat"],
    "reuse": ["using an empty jam jar to store buttons", "filling a water bottle again every day", "giving old clothes to a younger cousin",
              "using old newspapers to wrap fragile things", "turning a plastic bottle into a plant pot", "using the back of old worksheets for rough work", "passing old textbooks to pupils in the next class"],
    "recycle": ["putting drink cans into the blue recycling bin", "sending old newspapers to be made into new paper", "collecting glass bottles so they can be melted and made into new glass",
                "taking old phones to an e-waste bin", "putting used paper cartons into the recycling bin", "sending plastic bottles to be made into new plastic", "turning food waste into compost for plants"],
}
POL = {
    "air pollution": ["smoke from factory chimneys", "exhaust fumes from cars and buses", "burning forests that cause haze", "burning rubbish in the open", "smoke from a ship's engine at sea"],
    "water pollution": ["oil spilled from a ship", "rubbish thrown into a canal", "chemicals from a factory poured into a river", "detergent washed into a drain", "paint washed into a monsoon drain"],
    "land pollution": ["litter left on a beach", "old batteries thrown into the soil", "rubbish dumped in a forest", "plastic bags left in a park", "old furniture dumped at the back of a block of flats"],
    "noise pollution": ["construction work all night", "loud music played near a nature reserve", "aircraft taking off near homes", "honking horns in heavy traffic", "fireworks set off near a bird sanctuary"],
}
GOOD = [("Volunteers plant mangrove saplings along the coast.", True), ("A nature reserve is set up to protect a forest.", True),
        ("Pupils pick up litter at East Coast Park.", True), ("A park connector with trees links two parks.", True),
        ("People release unwanted pet terrapins into a reservoir.", False), ("A forest is cleared to build a factory.", False),
        ("A canal is lined with concrete and its plants removed.", False), ("Fishermen use nets that also catch turtles.", False),
        ("Green roofs with plants are built on top of buildings.", True), ("Bright lights are left on all night near a beach where turtles nest.", False),
        ("A town builds more cycling paths so people drive less.", True), ("Coral reefs are damaged by boats dropping anchors on them.", False),
        ("Nest boxes for hornbills are put up in a park.", True), ("Rubbish is thrown into a monsoon drain.", False)]


def g_3r():
    k = R.choice(sorted(R3))
    act = R.choice(R3[k])
    if not once(("3r", act)):
        return None
    return item("Which of the 3Rs is shown by %s?" % act, k, [x for x in ["reduce", "reuse", "recycle", "none of these"] if x != k],
                {"reduce": "Reduce means using less in the first place.", "reuse": "Reuse means using something again without changing what it is made of.",
                 "recycle": "Recycle means the material is made into something new."}[k])


def g_pol():
    k = R.choice(sorted(POL))
    c = R.choice(POL[k])
    if not once(("po", c)):
        return None
    return item("Which kind of pollution is caused by %s?" % c, k, [x for x in sorted(POL) if x != k], "The pollutant goes into the %s." % k.split()[0] if k != "noise pollution" else "Loud sounds disturb people and animals.")


def g_cause():
    k = R.choice(sorted(POL))
    c = R.choice(POL[k])
    if not once(("pc", c)):
        return None
    others = [R.choice(POL[o]) for o in sorted(POL) if o != k]
    return item("Which of these causes %s?" % k, c, others, "%s%s leads to %s." % (c[0].upper(), c[1:], k))


def g_good():
    s, ok = R.choice(GOOD)
    if not once(("gd", s)):
        return None
    a = "It helps living things." if ok else "It harms living things."
    return item(s + " What is the most likely effect on the environment?", a,
                ["It harms living things." if ok else "It helps living things.", "It has no effect on living things.", "It only changes the weather."],
                "Protecting habitats helps living things; destroying or polluting them causes harm." if ok else "This destroys or disturbs a habitat, so living things are harmed.")


def g_waste():
    nm, he, his = P.next()
    k = R.choice(["week", "save"])
    d = R.choice([1.2, 1.5, 2, 2.5, 3, 3.5, 4])
    ds = ("%g" % d)
    if k == "week":
        if not once(("ww", d)):
            return None
        a = d * 7
        return item("%s's family throws away %s kg of rubbish a day. How much rubbish is this in one week?" % (nm, ds), "%g kg" % a,
                    ["%g kg" % (d + 7), "%g kg" % (d * 5), "%g kg" % (d * 30)], "%s kg × 7 days = %g kg." % (ds, a))
    p = R.choice([20, 25, 40, 50])
    if not once(("ws", d, p)):
        return None
    w = d * 10
    a = w * p / 100
    return item("%s's family throws away %g kg of rubbish in 10 days. If they recycle %d%% of it instead, how much less rubbish goes to be burnt?" % (nm, w, p), "%g kg" % a,
                ["%g kg" % (w - a), "%g kg" % (w + a), "%g kg" % p], "%d%% of %g kg = %g kg." % (p, w, a))


B1 = bank([
    ("Which of these is caused by man?", "clearing a forest to build houses", ["a tree falling in a storm", "a river flooding after heavy rain", "leaves rotting on the forest floor"], "People change the environment in many ways."),
    ("How does cutting down forests affect animals?", "They lose their food and shelter.", ["They get more food.", "Nothing happens to them.", "They make their own food."], "Clearing forests destroys habitats."),
    ("Why does cutting down many trees increase the amount of carbon dioxide in the air?", "Fewer trees take in carbon dioxide for photosynthesis.", ["Trees give out carbon dioxide only.", "Cut trees make oxygen.", "Carbon dioxide comes from the soil."], "Burning the trees also releases carbon dioxide."),
    ("What does 'reduce' mean in the 3Rs?", "using less of something", ["using something again", "making something new from old material", "throwing things away"], "Reduce is the best of the 3Rs."),
    ("What is the difference between reusing and recycling?", "Reusing uses an object again; recycling makes the material into something new.", ["They mean the same.", "Reusing makes new things.", "Recycling means throwing things away."], "A jam jar used again is reused; a melted jar is recycled."),
    ("Where does much of Singapore's rubbish ash go after the rubbish is burnt?", "Semakau Landfill", ["Sungei Buloh Wetland Reserve", "the reservoirs", "the MRT tunnels"], "Semakau Landfill is filling up, so we need to reduce waste."),
    ("What causes the haze that sometimes reaches Singapore?", "smoke from forests and peatland being burnt in the region", ["fog from the sea", "steam from the reservoirs", "dust from the Moon"], "It is a form of air pollution."),
    ("Which of these helps to conserve water?", "turning off the tap while brushing your teeth", ["washing the car with a running hose", "leaving a leaking tap", "taking very long showers"], "Singapore also uses NEWater and desalinated water."),
])
B2 = bank([
    ("What is global warming?", "the slow rise in the average temperature of the Earth", ["the hole in the ozone layer", "a very hot day", "the heat from a fire"], "It is mainly caused by more greenhouse gases in the air."),
    ("Which gas is mainly linked to global warming?", "carbon dioxide", ["oxygen", "nitrogen", "water vapour from kettles"], "Burning fuels releases carbon dioxide."),
    ("How can burning less fuel help the environment?", "Less carbon dioxide and fewer harmful gases go into the air.", ["It makes more oxygen.", "It makes the Sun cooler.", "It increases the haze."], "Taking the MRT instead of a car burns less fuel per person."),
    ("Why is a rise in sea levels a problem for Singapore?", "Low-lying coastal land could be flooded.", ["The sea would become fresh water.", "There would be more land.", "It would stop the rain."], "Melting ice and warmer water raise sea levels."),
    ("Why should plastic bags not be thrown into the sea?", "Turtles may swallow them and die.", ["They help fish to breathe.", "They dissolve quickly.", "They make the water cleaner."], "Plastic takes hundreds of years to break down."),
    ("Which action helps to save electricity?", "setting the air-conditioner to 25 °C and closing the windows", ["leaving the TV on standby all night", "opening the fridge door often", "keeping lights on in empty rooms"], "Making electricity usually means burning fuel."),
    ("Why are nature reserves such as Sungei Buloh important?", "They protect habitats so plants and animals can survive.", ["They are places to dump rubbish.", "They are only for building houses.", "They make the weather hotter."], "Conservation keeps many populations alive."),
    ("Oil spilled from a ship coats the feathers of seabirds. What happens to the birds?", "They cannot fly or keep warm, and may die.", ["They fly faster.", "They get more food.", "Nothing happens."], "Oil spills are water pollution."),
])
B3 = bank([
    ("Why does Singapore encourage people to bring their own bags when shopping?", "to reduce the number of plastic bags thrown away", ["to make shopping faster", "to recycle more cans", "to increase the haze"], "This is an example of 'reduce'."),
    ("Which of these is a renewable source of energy that does not pollute the air?", "solar energy from panels on HDB rooftops", ["burning coal", "burning petrol", "burning natural gas"], "Solar panels change light energy into electrical energy."),
    ("Why are electric buses better for the air in a city than diesel buses?", "They do not give out exhaust fumes on the road.", ["They are bigger.", "They use more fuel.", "They make the air hotter."], "Fewer exhaust fumes means cleaner air."),
    ("Which of these is an example of conserving a habitat?", "keeping Bukit Timah Nature Reserve protected", ["clearing a forest for a car park", "filling in a pond to build a road", "draining a mangrove swamp"], "Protected areas keep habitats safe."),
    ("What happens to the population of animals when their habitat is destroyed?", "It decreases because they lose food and shelter.", ["It increases.", "It stays the same.", "They make new food."], "Animals depend on their habitat."),
    ("Why should used batteries be put into the e-waste bins instead of the rubbish chute?", "They contain chemicals that can pollute the land and water.", ["They are too heavy.", "They can be eaten by birds.", "They make the bin smell."], "Batteries can be recycled to recover metals."),
])
B5 = bank([
    ("A canal had many fish. After a factory poured waste into it, many fish died. Which is the most likely reason?", "The waste polluted the water and reduced the oxygen in it.", ["The fish ate too much.", "The water became too clean.", "The fish grew too big."], "Pollution harms the organisms in the habitat."),
    ("A forest next to a stream was cleared. After heavy rain, the stream became muddy. Why?", "Without tree roots, the soil was washed into the stream.", ["The trees made the stream clean.", "Rain is always muddy.", "Animals dug the soil."], "Roots hold soil in place; this is soil erosion."),
    ("A school collected 40 kg of paper for recycling each month. How does this help the environment?", "Fewer trees need to be cut down to make new paper.", ["More rubbish goes to the landfill.", "It uses more trees.", "It makes the paper heavier."], "Recycling saves raw materials."),
    ("Which change would best reduce the amount of rubbish sent to Semakau Landfill?", "Families reduce, reuse and recycle more of their waste.", ["Families buy more packaged food.", "Families throw recyclables into the rubbish bin.", "Families burn rubbish at home."], "Less waste means less ash."),
    ("Why does planting trees in a city help to cool it?", "Trees give shade and lose water vapour from their leaves.", ["Trees make the Sun weaker.", "Trees give out cold air.", "Trees stop the wind."], "Green spaces are cooler than bare concrete."),
    ("Mangrove trees along a coast were cut down. Which is the most likely result?", "The coast is worn away more by waves, and animals lose their habitat.", ["More mudskippers live there.", "The waves become smaller.", "Nothing changes."], "Mangroves protect coasts and are habitats."),
])


def body():
    think = ("<p><b>People can harm the environment, but people can also protect it.</b></p>"
             "<ul><li><b>Harm</b>: clearing forests destroys habitats; air, water and land pollution harm living things.</li>"
             "<li>Burning fuels adds <b>carbon dioxide</b> to the air. This leads to <b>global warming</b>.</li>"
             "<li><b>The 3Rs</b>: reduce (use less), reuse (use again), recycle (make into something new).</li>"
             "<li><b>Conservation</b>: nature reserves, planting trees, saving water and electricity.</li></ul>")
    ex = [("Using an empty jam jar to store buttons is which of the 3Rs?", ["The jar is used again, not made into something new"], "reuse"),
          ("Why does clearing a forest harm animals?", ["Think about food and shelter"], "They lose their habitat, food and shelter.")]
    mist = ["Mixing up reuse and recycle. Recycling makes the material into something new.",
            "Thinking clearing a forest only affects the trees. The animals lose their habitat too.",
            "Saying global warming is caused by the hole in the ozone layer. It is mainly caused by more carbon dioxide.",
            "Thinking rubbish that is burnt disappears. The ash still goes to Semakau Landfill."]
    return lesson(think, ex, mist)


IM = upto(HI.g_impact, 8)
MO = upto(HI.g_monitor, 3)
EF = upto(CE.g_eff, 5)
W = upto(g_waste, 6)


def main():
    sets = U.sets([
        ("How people change the environment", B1 + [(g_good, 6), (IM, 4)]),
        ("Pollution", [(g_pol, 8), (g_cause, 6), (IM, 4), (EF, 2)]),
        ("The 3Rs", [(g_3r, 12), (W, 4), (g_good, 4)]),
        ("Global warming and conservation", B2 + B3[:3] + [(g_3r, 3), (g_pol, 2), (g_cause, 3), (g_good, 1)]),
        ("PSLE-style questions", B5 + B3[3:] + [(g_cause, 4), (g_3r, 3), (W, 2), (g_good, 2), (g_pol, 2), (MO, 2)]),
    ])
    make_sg(6, "mans-impact-on-the-environment", 9, "Interactions", "Interactions within the environment (Man's impact on the environment)",
            "Recognise how man's activities, such as clearing forests, pollution and burning fuels, affect the environment and living things, and how man can conserve the environment "
            "through the 3Rs (reduce, reuse, recycle), conservation of habitats and saving resources (summary of the MOE Primary Science Syllabus).",
            "Man's Impact on the Environment",
            "Primary 6 Science: Man's Impact on the Environment Worksheets (3Rs, PSLE Practice)",
            "Man's impact on the environment",
            "Free Primary 6 science worksheets for Singapore pupils on man's impact on the environment: deforestation, pollution, global warming, the 3Rs and conservation. PSLE practice with answers.",
            "People can harm or protect the environment.",
            "Reduce, reuse and recycle to cut waste.",
            body(),
            [("What are the 3Rs?", "Reduce (use less), reuse (use again) and recycle (make old materials into new things)."),
             ("How does cutting down forests affect the environment?", "Animals lose their habitats, soil is washed away, and fewer trees take in carbon dioxide."),
             ("What causes global warming?", "Mainly more carbon dioxide and other greenhouse gases in the air from burning fuels and clearing forests.")],
            sets)


if __name__ == "__main__":
    main()
