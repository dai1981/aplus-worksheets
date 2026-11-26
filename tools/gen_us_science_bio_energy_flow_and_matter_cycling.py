# -*- coding: utf-8 -*-
"""
US High School Biology: Energy Flow and Matter Cycling in Ecosystems (HS-LS2-3, HS-LS2-4)
  python tools/gen_us_science_bio_energy_flow_and_matter_cycling.py
Construct and revise an explanation for the cycling of matter and flow of energy in aerobic and anaerobic conditions,
and use a mathematical representation to support claims for the cycling of matter and flow of energy among organisms.
Trophic levels, the 10% rule, energy pyramids, where the other 90% goes (heat from respiration, waste), matter is
recycled while energy is not, and decomposers.
Wrong answers come from real mistakes: "energy is recycled", "each level gets 90%", "top predators have the most energy".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, svg_wrap, comma, People
from ws_common import text, INK

U = Unit(90109)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


CHAINS = [["grass", "grasshoppers", "mice", "snakes", "hawks"], ["phytoplankton", "zooplankton", "small fish", "tuna", "sharks"],
          ["oak leaves", "caterpillars", "songbirds", "foxes", "eagles"], ["algae", "snails", "crayfish", "raccoons", "bobcats"],
          ["seeds", "chipmunks", "weasels", "owls", "none"]]
LVL = ["producer", "primary consumer", "secondary consumer", "tertiary consumer", "quaternary consumer"]


def pyramid(chain, vals):
    s = ""
    n = len(vals)
    for i, (c, v) in enumerate(zip(chain, vals)):
        w = 380 - i * 70
        y = 20 + (n - 1 - i) * 34
        s += "<rect x='%d' y='%d' width='%d' height='30' fill='%s' stroke='%s' stroke-width='1.3'/>" % (200 - w / 2, y, w, ["#b8d99a", "#f6d98a", "#f3b685", "#e8968a", "#c9a0d6"][i], INK)
        s += text(200, y + 20, "%s: %s kJ" % (c, comma(v)), 12)
    return svg_wrap(400, 30 + n * 34, s, "energy pyramid: " + ", ".join("%s %s kJ" % (c, comma(v)) for c, v in zip(chain, vals)))


def g_ten():
    ch = R.choice(CHAINS[:4])
    base = R.choice([1000, 2000, 5000, 10000, 20000, 50000, 100000])
    lv = R.randint(1, 3)
    if not once((ch[0], base, lv)):
        return None
    a = base // 10 ** lv
    return item("The %s capture %s kJ of energy. Using the 10%% rule, about how much reaches the %s?" % (ch[0], comma(base), ch[lv]), "%s kJ" % comma(a),
                ["%s kJ" % comma(base * 9 // 10), "%s kJ" % comma(a * 10 if lv > 1 else base // 2), "%s kJ" % comma(base - 10 * lv)], "Divide by 10 for each step: %d step%s." % (lv, "" if lv == 1 else "s"))


def g_pyr():
    ch = R.choice(CHAINS[:4])
    base = R.choice([10000, 20000, 50000])
    vals = [base // 10 ** i for i in range(4)]
    k = R.choice(["missing", "pct", "why", "top"])
    if not once((ch[0], base, k)):
        return None
    if k == "missing":
        i = R.randint(1, 3)
        v2 = list(vals)
        hidden = v2[i]
        s = pyramid(ch[:4], v2).replace("%s: %s kJ" % (ch[i], comma(hidden)), "%s: ? kJ" % ch[i])
        return item(fig(s) + "Use the 10%% rule. How much energy reaches the %s?" % ch[i], "%s kJ" % comma(hidden), ["%s kJ" % comma(hidden * 10), "%s kJ" % comma(hidden * 9), "%s kJ" % comma(max(1, hidden // 2))],
                    "%s ÷ 10 = %s." % (comma(vals[i - 1]), comma(hidden)))
    pic = fig(pyramid(ch[:4], vals))
    if k == "pct":
        return item(pic + "What percent of the energy at one level passes to the next level?", "about 10%", ["about 90%", "about 50%", "100%"], "%s → %s." % (comma(vals[0]), comma(vals[1])))
    if k == "why":
        return item(pic + "Where does most of the energy at each level go?", "It is lost as heat from cellular respiration and in waste.", ["It is recycled back to the producers.", "It turns into matter.", "It stays stored forever in the top level."],
                    "About 90% is used or lost each step.")
    return item(pic + "Why are there few %s compared with %s?" % (ch[3], ch[0]), "Little energy reaches the top of the pyramid.", ["Top predators eat less often.", "Producers make energy from nothing.", "Energy increases up the pyramid."],
                "Less energy supports fewer animals.")


def g_lvl():
    ch = R.choice(CHAINS)
    i = R.randrange(4)
    if not once((ch[0], i)):
        return None
    return item("Food chain: %s. What trophic level are the %s?" % (" → ".join(ch[:4]), ch[i]), LVL[i], [l for l in LVL[:4] if l != LVL[i]], "Count from the producer.")


ROLE = [("Bacteria and fungi break down a fallen log.", "decomposers"), ("Algae make sugar using sunlight.", "producers"), ("A deer eats grass.", "primary consumers"),
        ("A wolf eats a deer.", "secondary consumers"), ("Mushrooms grow on dead leaves and return nutrients to the soil.", "decomposers"), ("Phytoplankton capture light in the ocean.", "producers")]


def g_role():
    s, a = R.choice(ROLE)
    if not once(s):
        return None
    return item("%s What role do they play?" % s, a, [x for x in ["producers", "primary consumers", "secondary consumers", "decomposers"] if x != a], "Producers, consumers and decomposers.")


MATTER = [("What happens to the carbon in a dead tree?", "Decomposers release it as CO<sub>2</sub>, which plants can use again.", ["It disappears.", "It turns into energy.", "It stays in the log forever."]),
          ("Is energy recycled in an ecosystem?", "No. Energy flows through and leaves as heat; matter is recycled.", ["Yes, all of it.", "Yes, by decomposers.", "Only at night."]),
          ("Which process puts carbon from the air into living things?", "photosynthesis", ["cellular respiration", "decomposition", "burning"]),
          ("Which processes return carbon to the air?", "cellular respiration and decomposition", ["photosynthesis only", "only volcanoes", "evaporation"]),
          ("In a swamp with little oxygen, how do some bacteria break down matter?", "anaerobic respiration, which can release methane", ["photosynthesis", "they cannot break it down at all", "using light"]),
          ("Where do the atoms in your body come from?", "from the food you eat, which came from plants and the air", ["from sunlight", "from nowhere", "only from water"])]


def g_matter():
    q, a, w = R.choice(MATTER)
    if not once(q):
        return None
    return item(q, a, w, "Matter cycles; energy flows one way.")


B1 = bank([
    ("What is the original source of energy for most ecosystems?", "the sun", ["the soil", "water", "decomposers"], "Producers capture sunlight."),
    ("What is a producer?", "an organism that makes its own food", ["an animal that eats plants", "an organism that breaks down dead things", "a top predator"], "Plants and algae."),
    ("What is the 10% rule?", "only about 10% of energy passes to the next trophic level", ["10% of energy is lost at each level", "animals eat 10% of the time", "10% of organisms are producers"], "About 90% is lost."),
    ("Why do food chains rarely have more than 4 or 5 levels?", "There is too little energy left at higher levels.", ["Animals cannot count.", "Plants stop growing.", "Decomposers eat the top."], "Energy runs out."),
    ("What do decomposers do?", "break down dead matter and recycle nutrients", ["make food from sunlight", "hunt top predators", "store energy forever"], "Fungi and bacteria."),
    ("Which level of an energy pyramid has the most energy?", "producers", ["top predators", "secondary consumers", "decomposers"], "The base is the widest."),
    ("How is matter different from energy in ecosystems?", "Matter cycles; energy flows one way.", ["Both cycle.", "Both flow one way.", "Neither moves."], "Key idea."),
    ("What form does most lost energy take?", "heat", ["new matter", "light", "sound"], "From respiration."),
])
B5 = bank([
    ("A field makes 50,000 kJ of plant energy. How much might reach hawks at the 4th level?", "about 50 kJ", ["about 5,000 kJ", "about 500 kJ", "about 45,000 kJ"], "50,000 → 5,000 → 500 → 50."),
    ("Why is eating plants more energy-efficient for people than eating beef?", "Less energy is lost when eating lower on the food chain.", ["Plants have no energy.", "Beef has more energy than the grass it ate.", "Cows make energy."], "Fewer steps."),
    ("A pond's decomposers are removed. What happens over time?", "Dead matter builds up and nutrients are not recycled.", ["Plants grow faster.", "Energy is recycled instead.", "Nothing changes."], "Decomposers recycle."),
    ("A model shows carbon atoms moving from grass to a rabbit to CO<sub>2</sub> in the air. Which process released the CO<sub>2</sub>?", "cellular respiration", ["photosynthesis", "transcription", "osmosis"], "Respiration releases CO2."),
    ("Snakes get 400 kJ from mice. About how much energy did the mice get from grass?", "about 4,000 kJ", ["about 40 kJ", "about 400 kJ", "about 440 kJ"], "400 × 10 = 4,000."),
])


def body():
    think = ("<div class='qfig'>%s</div><p><b>Energy flows up and is lost; matter cycles.</b></p>"
             "<ul><li>About 10%% of the energy passes to the next level; about 90%% leaves as heat and waste.</li>"
             "<li>Carbon and nitrogen cycle through producers, consumers, decomposers and the air.</li></ul>") % pyramid(CHAINS[0][:4], [10000, 1000, 100, 10])
    ex = [("Grass: 20,000 kJ. Energy for mice (3rd level)?", ["÷10 twice", "20,000 → 2,000 → 200"], "200 kJ"),
          ("Why are hawks rare?", ["Little energy at the top"], "Not enough energy to support many")]
    mist = ["Thinking energy is recycled. Matter is recycled; energy is lost as heat.", "Passing on 90% instead of 10%.", "Thinking top predators have the most energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Food chains and trophic levels", B1 + [(g_lvl, 8), (g_role, 4)]),
        ("The 10% rule", [(g_ten, 14), (g_lvl, 6)]),
        ("Energy pyramids", [(g_pyr, 14), (g_role, 2), (g_ten, 4)]),
        ("Cycling matter", [(g_matter, 6), (g_pyr, 8), (g_ten, 6)]),
        ("Ecosystem models", B5 + [(g_ten, 8), (g_pyr, 4), (g_lvl, 3)]),
    ])
    make("biology", "energy-flow-and-matter-cycling", 9, "HS-LS2-3, HS-LS2-4",
         "Construct and revise an explanation based on evidence for the cycling of matter and flow of energy in aerobic and anaerobic conditions. "
         "Use mathematical representations to support claims for the cycling of matter and flow of energy among organisms in an ecosystem.",
         "Energy Flow and Matter Cycling",
         "Energy Pyramid Worksheets: Trophic Levels and the 10% Rule (High School Biology)",
         "Energy Flow",
         "Free high school biology worksheets on energy flow in ecosystems (NGSS HS-LS2-3, HS-LS2-4): trophic levels, the 10% rule, energy pyramids, decomposers and matter cycling. 100 questions with answers.",
         "Energy flows; matter cycles.",
         "About 10% of the energy passes to each higher level.",
         body(),
         [("What is the 10% rule?", "About 10% of the energy at one trophic level is passed to the next; the rest is used for life processes and lost as heat."),
          ("Why is energy lost at each level?", "Organisms use most of the energy in cellular respiration, which releases heat, and some is lost in waste."),
          ("How is matter recycled?", "Decomposers break down dead organisms and waste, returning carbon, nitrogen and other nutrients to the air and soil.")],
         sets)


if __name__ == "__main__":
    main()
