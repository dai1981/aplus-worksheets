# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Energy Conversions (4-PS3-4)
  python tools/gen_us_science_g4_energy_conversions.py
Devices change energy from one form to another: electric energy into light, sound, heat or motion;
light into electricity (solar panels); motion into electricity (generators, hand-crank flashlights).
Students apply this to design devices (a solar oven, a rubber-band car, an alarm) with criteria and constraints.
Wrong answers come from real mistakes: "a device makes energy from nothing", "a lamp turns electricity
into sound", "a solar panel makes light".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(40104)
R = U.R
P = People(R)

# device: (energy in, main useful energy out, extra energy out that is wasted or not the main job)
DEV = {
    "a toaster": ("electric", "heat", "light"), "a hair dryer": ("electric", "heat", "sound"), "an electric fan": ("electric", "motion", "sound"),
    "a lamp": ("electric", "light", "heat"), "a doorbell": ("electric", "sound", "heat"), "a blender": ("electric", "motion", "sound"),
    "a speaker": ("electric", "sound", "heat"), "an electric stove": ("electric", "heat", "light"), "a flashlight": ("electric", "light", "heat"),
    "a toy car with a motor": ("electric", "motion", "sound"), "a solar panel": ("light", "electric", "heat"), "a solar calculator": ("light", "electric", None),
    "a wind turbine": ("motion", "electric", "sound"), "a hand-crank flashlight": ("motion", "light", None), "a bike light powered by the wheel": ("motion", "light", None),
    "a microphone": ("sound", "electric", None), "an electric drill": ("electric", "motion", "sound"), "a hot plate": ("electric", "heat", None),
    "a TV screen": ("electric", "light", "sound"), "a phone's ringer": ("electric", "sound", None),
}
NAME = {"electric": "electric energy", "heat": "heat", "light": "light", "sound": "sound", "motion": "motion (energy of motion)"}
SHORT = {"electric": "electric energy", "heat": "heat", "light": "light", "sound": "sound", "motion": "motion"}


def cap(s):
    return s[0].upper() + s[1:]


def g_out():
    d = R.choice([k for k in DEV if DEV[k][0] != DEV[k][1]])
    i, o, x = DEV[d]
    wrong = [SHORT[k] for k in SHORT if k not in (o, x, i)]
    if len(wrong) < 3:
        wrong.append(SHORT[i] + " only, with no change")
    return item("%s changes %s into which main form of energy?" % (cap(d), NAME[i]), SHORT[o], R.sample(wrong, 3),
                "The main job of %s is to make %s." % (d, SHORT[o]))


def g_in():
    d = R.choice([k for k in DEV if DEV[k][0] not in ("electric", DEV[k][1])])
    i, o, x = DEV[d]
    wrong = [SHORT[k] for k in SHORT if k not in (i, o)]
    return item("%s makes %s. Which form of energy goes into it?" % (cap(d), SHORT[o]), SHORT[i] if i != "motion" else "motion (something turns or moves it)",
                R.sample(wrong, 3), "%s changes %s into %s." % (cap(d), SHORT[i], SHORT[o]))


def g_extra():
    d = R.choice([k for k in DEV if DEV[k][2]])
    i, o, x = DEV[d]
    also = {"a doorbell": "motion", "a speaker": "motion", "a hair dryer": "motion", "a toaster": "sound", "a TV screen": "light"}
    wrong = [SHORT[k] for k in SHORT if k not in (o, x, i, "heat", also.get(d))] + ["new matter", "cold"]
    return item("%s changes %s mostly into %s. Which other form of energy does it also give off?" % (cap(d), SHORT[i], SHORT[o]), SHORT[x], R.sample(wrong, 3),
                "Devices are not perfect. %s also gives off some %s." % (cap(d), SHORT[x]))


def g_which():
    i, o = R.choice([("electric", "heat"), ("electric", "light"), ("electric", "motion"), ("electric", "sound"), ("light", "electric"), ("motion", "electric")])
    good = [d for d in DEV if DEV[d][0] == i and DEV[d][1] == o]
    bad = [d for d in DEV if not (DEV[d][0] == i and DEV[d][1] == o) and DEV[d][1] != o]
    return item("Which device changes %s into %s?" % (SHORT[i], SHORT[o]), R.choice(good), R.sample(bad, 3),
                "Look at what goes in (%s) and what comes out (%s)." % (SHORT[i], SHORT[o]))


def g_chain():
    chains = [("A solar panel charges a battery that runs a fan.", "light → electric energy → motion"),
              ("A wind turbine sends electricity to a lamp.", "motion → electric energy → light"),
              ("A hand-crank radio is turned to play music.", "motion → electric energy → sound"),
              ("A solar panel powers a doorbell.", "light → electric energy → sound"),
              ("A battery runs a toy car's motor.", "electric energy → motion"),
              ("A water wheel turns a generator that powers a light bulb.", "motion → electric energy → light"),
              ("Sunlight hits a solar calculator and its screen shows numbers.", "light → electric energy → light"),
              ("A wind turbine charges a battery that runs a heater.", "motion → electric energy → heat")]
    s, a = R.choice(chains)
    others = [c for _, c in chains if c != a]
    bad = [a.replace("light", "SOUND").replace("sound", "light").replace("SOUND", "sound"), " → ".join(reversed(a.split(" → ")))]
    wrong = [w for w in bad if w != a and w not in others]
    wrong += R.sample(others, 3)
    wrong = list(dict.fromkeys(wrong))[:3]
    return item(s + " Which shows the energy changes in order?", a, wrong, "Follow the energy from where it starts to where it ends.")


def g_design():
    goals = [("make a toy car move without batteries", "a rubber band that is wound up", ["a mirror", "a bag of ice", "a paper cup"], "A wound rubber band stores energy that turns into motion."),
             ("warm a hot dog using sunlight", "a box lined with foil and covered with clear plastic", ["a closed black box with no lid", "a fan that blows air", "a bell"], "The foil reflects light onto the food and the plastic traps the heat."),
             ("make an alarm that sounds when a door opens", "a battery, a buzzer and a switch the door pushes", ["a solar oven", "a rubber band car", "a cup of water"], "The switch closes the circuit so electric energy turns into sound."),
             ("light a path at night using energy from the day", "a solar light that charges a battery in sunlight", ["a lamp plugged into a wall all day", "a flashlight with no batteries", "a mirror"], "Light → electric energy (stored) → light at night."),
             ("make a fan spin using wind", "a small wind turbine wired to a motor", ["a solar oven", "a doorbell", "a bag of sand"], "Wind turns the turbine, making electric energy that runs the motor."),
             ("turn on a light by pedaling", "a bike wheel that turns a small generator", ["a bike bell", "a water bottle", "a mirror on the handlebars"], "Pedaling motion → electric energy → light.")]
    g, a, w, e = R.choice(goals)
    p = P.next()
    return item("%s wants to %s. Which design would work best?" % (p[0], g), a, w, e)


def g_test():
    designs = R.sample(["A", "B", "C", "D"], 3)
    temps = sorted(R.sample(range(30, 75), 3), reverse=True)
    rows = [["Oven %s" % d, "%d °C" % t] for d, t in zip(designs, temps)]
    R.shuffle(rows)
    p = P.next()
    k = R.choice(["best", "crit"])
    tab = table(["Solar oven", "Temperature after 30 min"], rows)
    if k == "best":
        return item(tab + "%s tested three solar ovens in the sun. Which design changed the most light into heat?" % p[0], "Oven %s" % designs[0],
                    ["Oven %s" % d for d in designs[1:]] + ["All ovens worked the same."], "Oven %s got the hottest: %d °C." % (designs[0], temps[0]))
    need = R.randint(temps[1] + 1, temps[0])
    return item(tab + "%s's oven must reach at least %d °C to melt cheese. Which oven meets this criterion?" % (p[0], need), "only Oven %s" % designs[0],
                ["only Oven %s" % designs[1], "all three ovens", "none of the ovens"], "Only Oven %s (%d °C) is at least %d °C." % (designs[0], temps[0], need))


B1 = bank([
    ("What does it mean to convert energy?", "to change energy from one form into another", ["to destroy energy", "to make energy from nothing", "to stop energy from moving"],
     "A lamp converts electric energy into light."),
    ("Can a device make energy from nothing?", "No. It changes energy that goes into it into other forms.", ["Yes, if it is new.", "Yes, if it is turned on.", "Only small devices can."],
     "Energy is changed, not made from nothing."),
    ("Why does a light bulb get warm?", "Some electric energy changes into heat, not just light.", ["Light is always cold.", "The bulb makes new energy.", "Heat flows from the room into the bulb."],
     "Devices give off some energy in forms we do not want."),
    ("Which form of energy do solar panels take in?", "light", ["sound", "heat from the ground only", "wind"],
     "Solar panels change light into electric energy."),
    ("What energy change happens in a battery-powered fan?", "electric energy → motion", ["motion → electric energy", "light → sound", "heat → light"],
     "The motor spins the blades."),
    ("What does a generator do?", "changes motion into electric energy", ["changes electric energy into sound", "stores water", "makes light from nothing"],
     "Turning a generator, by hand, wind or water, makes electricity."),
    ("A speaker changes electric energy into", "sound", ["light", "wind", "matter"], "The speaker vibrates and makes sound."),
    ("Which energy change happens when you rub your hands together?", "motion → heat", ["heat → motion", "sound → light", "light → electric energy"],
     "Rubbing changes energy of motion into heat."),
])
B5 = bank([
    ("A design must cost less than $10 and use only paper and tape. These limits are called", "constraints", ["criteria", "results", "variables"],
     "Constraints are limits on a design."),
    ("A solar oven must reach 60 °C. This goal is called a", "criterion", ["constraint", "conclusion", "material"],
     "Criteria tell what the design must do."),
    ("Why do engineers test a design more than once?", "to see if the results are the same and the design is reliable", ["to use up materials", "to change the goal", "to make it heavier"],
     "Repeated tests show if the design really works."),
    ("Mia's rubber-band car rolls 2 meters. How could she make it go farther?", "wind the rubber band more times", ["use a looser rubber band", "add heavy rocks", "take off the wheels"],
     "More winding stores more energy that changes into motion."),
    ("Why is foil used inside a solar oven?", "It reflects light onto the food.", ["It makes electricity.", "It makes the box heavier.", "It blocks all light."],
     "More light reaching the food means more heat."),
    ("Why is the inside of a solar oven often painted black?", "Black takes in light and changes it into heat.", ["Black reflects all light.", "Black makes sound.", "Black keeps the oven cool."],
     "Dark colors absorb more light energy."),
])


def body():
    think = ("<p>Many devices <b>convert</b> (change) energy from one form to another. A device does not make energy from nothing. "
             "It changes the energy that goes into it.</p>"
             "<ul><li>Lamp: electric energy → <b>light</b></li><li>Fan: electric energy → <b>motion</b></li>"
             "<li>Speaker: electric energy → <b>sound</b></li><li>Toaster: electric energy → <b>heat</b></li>"
             "<li>Solar panel: light → <b>electric energy</b></li><li>Wind turbine: motion → <b>electric energy</b></li></ul>"
             "<p>Most devices also give off some energy we do not need, like the heat from a light bulb. "
             "Engineers design devices to meet <b>criteria</b> (what it must do) within <b>constraints</b> (limits like cost and materials).</p>")
    ex = [("What energy change happens in a hair dryer?", ["Electric energy goes in.", "Heat comes out, and the fan moves air."], "electric energy → heat (and motion and sound)"),
          ("A solar panel runs a fan. Show the energy changes.", ["light → electric energy", "electric energy → motion"], "light → electric energy → motion")]
    mist = ["Thinking a device makes energy from nothing.",
            "Mixing up the input and the output: a solar panel takes in light; it does not make light.",
            "Forgetting that devices also give off unwanted heat or sound."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Changing energy from one form to another", B1 + [(g_out, 8), (g_which, 4)]),
        ("What goes in and what comes out", [(g_out, 8), (g_in, 6), (g_which, 6)]),
        ("Extra energy and energy chains", [(g_extra, 10), (g_chain, 6), (g_in, 4)]),
        ("Designing devices", [(g_design, 6), (g_test, 8), (g_chain, 6)]),
        ("Design tests", B5 + [g_test, g_design, g_which, g_extra]),
    ])
    make("grade-4", "energy-conversions", 4, "4-PS3-4",
         "Apply scientific ideas to design, test, and refine a device that converts energy from one form to another.",
         "Energy Conversions",
         "Grade 4 Energy Conversion Worksheets: Devices That Change Energy",
         "Energy Conversions",
         "Free Grade 4 science worksheets on energy conversions (NGSS 4-PS3-4): electric energy into light, sound, heat and motion, solar panels and generators, energy chains and designing a solar oven. 100 practice questions with answers.",
         "Devices change energy from one form into another.",
         "A lamp changes electric energy into light. A solar panel changes light into electric energy. No device makes energy from nothing.",
         body(),
         [("What is an energy conversion?", "It is when energy changes from one form to another, like electric energy into light in a lamp."),
          ("What energy change happens in a solar panel?", "A solar panel changes light into electric energy."),
          ("Why do devices get warm?", "Most devices change some of their energy into heat, even when that is not their main job.")],
         sets)


if __name__ == "__main__":
    main()
