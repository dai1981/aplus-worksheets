# -*- coding: utf-8 -*-
"""
US Grade 6 Science: Designing to Control Heat Transfer (MS-PS3-3)
  python tools/gen_us_science_g6_designing_to_control_heat_transfer.py
Apply scientific principles to design, construct and test a device that minimizes or maximizes thermal
energy transfer: conduction (touching), convection (moving fluids), radiation (light / infrared);
conductors vs. insulators; foam cups, thermoses, coolers, solar ovens, double-pane windows.
Assessment boundary: no calculations of the amount of energy transferred.
Wrong answers come from real mistakes: "cold flows into things", "insulators make heat",
"metal feels cold because it is colder than wood at the same room temperature".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(60107)
R = U.R
P = People(R)

HT = {"conduction": ["a metal spoon getting hot in a pot of soup", "your hand warming an ice cube you hold", "a pan heating up on a stove burner", "a cold floor chilling your bare feet",
                     "a hot iron smoothing a shirt", "a laptop warming your lap"],
      "convection": ["warm air rising from a heater and spreading through a room", "hot water rising and cold water sinking in a pot", "a sea breeze blowing toward land on a sunny day",
                     "warm air rising above a campfire", "a hair dryer blowing hot air", "an oven fan moving hot air around food"],
      "radiation": ["sunlight warming your face", "feeling the heat from a campfire while sitting a few feet away", "a heat lamp keeping food warm",
                    "a black car getting hot in the sun", "the warmth you feel from a glowing toaster", "sunlight warming Earth through empty space"]}
WHY = {"conduction": "Energy moves between objects that are touching.", "convection": "Energy is carried by a moving liquid or gas.",
       "radiation": "Energy travels as light or infrared waves, even through empty space."}


def g_kind():
    k = R.choice(sorted(HT))
    x = R.choice(HT[k])
    p = P.next()
    return item("%s observes %s. Which kind of heat transfer is this mainly?" % (p[0], x), k, [c for c in HT if c != k] + ["insulation"], WHY[k])


def g_example():
    k = R.choice(sorted(HT))
    a = R.choice(HT[k])
    w = [x for c in HT if c != k for x in HT[c]]
    p = P.next()
    return item("%s's teacher asks for an example of %s. Which is the best example?" % (p[0], k), a, R.sample(w, 3), WHY[k])


INS = ["foam", "wool", "air pockets", "plastic", "wood", "cork", "fiberglass", "feathers"]
CON = ["copper", "aluminum", "iron", "steel", "silver"]


def g_material():
    k = R.choice(["ins", "con"])
    p = P.next()
    use = R.choice(["a lunch box that keeps food cold", "a cooler for a picnic", "a cup that keeps cocoa hot", "a pot handle", "oven mitts", "walls of a house"])
    if k == "ins":
        return item("%s is designing %s. Which material would best slow heat transfer?" % (p[0], use), R.choice(INS), R.sample(CON, 3),
                    "Insulators like foam, wool and trapped air slow the transfer of thermal energy.")
    use = R.choice(["the bottom of a cooking pot", "a heat sink that cools a computer chip", "a pan that heats food quickly", "a radiator that warms a room"])
    return item("%s is designing %s. Which material would best transfer heat?" % (p[0], use), R.choice(CON), R.sample(INS, 3),
                "Metals are good conductors of thermal energy.")


def g_test():
    designs = R.sample(["foam cup with lid", "paper cup with lid", "metal cup with lid", "foam cup without lid", "glass jar with lid", "cup wrapped in wool"], 3)
    order = {"foam cup with lid": 6, "cup wrapped in wool": 5, "foam cup without lid": 4, "glass jar with lid": 3, "paper cup with lid": 2, "metal cup with lid": 1}
    designs.sort(key=lambda d: -order[d])
    ends = sorted(R.sample(range(35, 66), 3), reverse=True)
    rows = [[d, "%d °C" % e] for d, e in zip(designs, ends)]
    R.shuffle(rows)
    p = P.next()
    tab = table(["Design", "Temperature after 30 min (started at 80 °C)"], rows)
    k = R.choice(["best", "loss", "crit"])
    if k == "best":
        return item(tab + "%s tested cups to keep hot water hot. Which design transferred the least thermal energy to the room?" % p[0], designs[0],
                    designs[1:] + ["They all lost the same amount."], "It stayed the warmest (%d °C)." % ends[0])
    if k == "loss":
        d = R.randrange(3)
        return item(tab + "How many degrees did the %s cool in %s's test?" % (designs[d], p[0]), "%d °C" % (80 - ends[d]),
                    ["%d °C" % ends[d], "%d °C" % (80 + ends[d]), "%d °C" % (80 - ends[(d + 1) % 3])], "80 − %d = %d °C." % (ends[d], 80 - ends[d]))
    need = R.randint(ends[1] + 1, ends[0])
    return item(tab + "%s's cup must keep water at %d °C or warmer after 30 minutes. Which design meets this criterion?" % (p[0], need), "only the " + designs[0],
                ["only the " + designs[1], "all three", "none of them"], "Only the %s stayed at %d °C or warmer." % (designs[0], need))


B1 = bank([
    ("What are the three ways thermal energy is transferred?", "conduction, convection and radiation", ["melting, freezing and boiling", "pushing, pulling and lifting", "sound, light and magnetism"],
     "These three processes move thermal energy."),
    ("In which direction does thermal energy always move?", "from warmer objects to cooler objects", ["from cooler to warmer objects", "only upward", "only through metal"], "Cold does not flow; heat does."),
    ("Why does a metal bench feel colder than a wooden bench on the same cool day?", "Metal conducts heat away from your skin faster.", ["Metal is always colder.", "Wood makes heat.", "Metal has no particles."],
     "Both are the same temperature, but metal is a better conductor."),
    ("What is an insulator?", "a material that slows the transfer of thermal energy", ["a material that makes heat", "a material that transfers heat quickly", "a kind of thermometer"],
     "Foam, wool and air are good insulators."),
    ("Why does a thermos keep soup hot?", "Its vacuum layer and shiny lining slow conduction, convection and radiation.", ["It makes its own heat.", "It adds cold.", "It is heavy."],
     "A good design slows all three kinds of heat transfer."),
    ("Why do winter coats with puffy filling keep you warm?", "The filling traps air, which is a poor conductor.", ["The filling makes heat.", "The coat blocks cold from coming in.", "The coat is heavy."],
     "Trapped air slows heat leaving your body."),
    ("How does the sun's energy reach Earth?", "by radiation through space", ["by conduction through air", "by convection through space", "through wires"], "Space is empty, so only radiation works."),
    ("Why are double-pane windows better at keeping a house warm?", "The air or gas between the panes slows heat transfer.", ["They let in more cold.", "Glass makes heat.", "They are thicker so cold cannot fit."],
     "The gap is an insulating layer."),
])
B5 = bank([
    ("Ava builds a solar oven. Why does she line it with foil?", "to reflect sunlight onto the food", ["to block all sunlight", "to make the oven heavier", "to cool the food"], "Reflected radiation adds energy."),
    ("Why should Ava cover her solar oven with clear plastic?", "to trap the warm air inside so less heat is lost by convection", ["to let cold air in", "to block sunlight", "to make it lighter"],
     "Clear plastic lets light in but keeps warm air from escaping."),
    ("Leo's cooler must keep ice frozen for 4 hours and cost less than $5. What is the cost limit called?", "a constraint", ["a criterion", "a conclusion", "a variable"],
     "Constraints are limits; criteria are goals."),
    ("Mia tests two cooler designs, but uses more ice in one. Why is this a problem?", "The test is not fair because two things changed.", ["More ice always melts faster.", "There is no problem.", "Coolers do not need ice."],
     "Change only the design, not the amount of ice."),
    ("Which change would make a cup keep a drink cold longer?", "add a lid and wrap it in foam", ["use a thin metal cup", "leave it in the sun", "remove the lid"],
     "Insulation and a lid slow heat moving into the drink."),
])


def body():
    think = ("<p>Thermal energy always moves from <b>warmer</b> to <b>cooler</b> objects, in three ways:</p>"
             "<ul><li><b>Conduction</b>: between objects that touch (a spoon in hot soup).</li>"
             "<li><b>Convection</b>: carried by moving liquids or gases (warm air rising from a heater).</li>"
             "<li><b>Radiation</b>: as light or infrared waves, even through space (sunlight).</li></ul>"
             "<p><b>Conductors</b> (metals) transfer heat quickly. <b>Insulators</b> (foam, wool, trapped air) slow it down. "
             "Engineers use these ideas to design coolers, thermoses, solar ovens and warm houses, and they test designs against <b>criteria</b> and <b>constraints</b>.</p>")
    ex = [("A spoon in hot cocoa gets hot. Which kind of transfer?", ["The spoon touches the cocoa."], "conduction"),
          ("Which keeps ice frozen longer: a metal box or a foam box?", ["Foam is an insulator."], "the foam box")]
    mist = ["Saying cold flows into things. Heat flows out of warmer things.",
            "Thinking insulators make heat. They only slow heat transfer.",
            "Thinking metal is colder than wood at the same room temperature."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Conduction, convection and radiation", B1 + [(g_kind, 6), (g_example, 6)]),
        ("Which kind of transfer?", [(g_kind, 12), (g_example, 8)]),
        ("Conductors and insulators", [(g_material, 14), (g_kind, 6)]),
        ("Testing designs", [(g_test, 14), (g_material, 6)]),
        ("Engineering design", B5 + [g_test, g_material, g_example, g_kind]),
    ])
    make("grade-6", "designing-to-control-heat-transfer", 7, "MS-PS3-3",
         "Apply scientific principles to design, construct, and test a device that either minimizes or maximizes thermal energy transfer.",
         "Designing to Control Heat Transfer",
         "Grade 6 Heat Transfer Worksheets: Conduction, Convection, Radiation and Insulators",
         "Heat Transfer",
         "Free middle school science worksheets on heat transfer (NGSS MS-PS3-3): conduction, convection and radiation, conductors and insulators, and testing cup, cooler and solar oven designs. 100 practice questions with answers.",
         "Heat moves by conduction, convection and radiation.",
         "Insulators slow heat transfer and conductors speed it up. Engineers use them to design coolers, thermoses and solar ovens.",
         body(),
         [("What are conduction, convection and radiation?", "Conduction is heat transfer by touching, convection is heat carried by moving liquids or gases, and radiation is heat carried by light or infrared waves."),
          ("What makes a good insulator?", "Materials that slow heat transfer, like foam, wool, cork and trapped air."),
          ("Why does a metal spoon get hot in soup but a wooden spoon does not?", "Metal is a good conductor, so heat moves through it quickly. Wood is an insulator.")],
         sets)


if __name__ == "__main__":
    main()
