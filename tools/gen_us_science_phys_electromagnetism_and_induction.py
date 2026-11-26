# -*- coding: utf-8 -*-
"""
US High School Physics: Electromagnetism and Induction (HS-PS2-5)
  python tools/gen_us_science_phys_electromagnetism_and_induction.py
Plan and conduct an investigation to provide evidence that an electric current can produce a magnetic field and that a
changing magnetic field can produce an electric current.
Magnetic fields around wires and coils, electromagnets (turns, current, iron core), electromagnetic induction
(moving magnets and coils, faster motion, more turns), and devices: motors, generators, transformers, speakers.
Wrong answers come from real mistakes: "a still magnet in a coil makes current", "electromagnets work without
current", "a generator makes energy from nothing", "a motor and a generator do the same job".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90307)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


EM = [("adds more turns of wire to the coil", "stronger"), ("increases the current", "stronger"), ("puts an iron nail inside the coil", "stronger"),
      ("uses fewer turns of wire", "weaker"), ("uses a weaker battery", "weaker"), ("removes the iron core", "weaker"), ("switches off the current", "no longer magnetic"),
      ("reverses the battery", "the same strength, but the poles swap"), ("uses two batteries in series instead of one", "stronger"), ("winds the coil more loosely with the same number of turns", "weaker")]


@safe
def g_em():
    who = P.next()[0]
    if R.random() < 0.45:
        up = R.choice([x for x in EM if x[1] == "stronger"])
        downs = R.sample([x for x in EM if x[1] != "stronger"], 3)
        if not once(("emb", up[0], tuple(sorted(d[0] for d in downs)))):
            return None
        return item("%s wants a stronger electromagnet. Which change should %s make?" % (who, who), up[0].replace("adds", "add").replace("increases", "increase").replace("puts", "put").replace("uses", "use"),
                    [d[0].replace("uses", "use").replace("removes", "remove").replace("switches", "switch").replace("reverses", "reverse").replace("winds", "wind") for d in downs],
                    "More current, more turns or an iron core make it stronger.")
    s, a = R.choice(EM)
    if not once(("em", s)):
        return None
    opts = ["stronger", "weaker", "no longer magnetic", "the same strength, but the poles swap", "unchanged"]
    return item("%s builds an electromagnet and then %s. How does the electromagnet change?" % (who, s), a, R.sample([o for o in opts if o != a], 3),
                "Strength depends on current, number of turns and the core.")


IND = [("A magnet is pushed into a coil connected to a meter.", "A current is induced."), ("A magnet rests still inside a coil.", "No current is induced."),
       ("The magnet is pulled out of the coil.", "A current is induced in the opposite direction."), ("The magnet is pushed in twice as fast.", "A larger current is induced."),
       ("A coil with more turns is used with the same magnet motion.", "A larger current is induced."), ("The coil is moved over a still magnet.", "A current is induced."),
       ("A stronger magnet is moved at the same speed.", "A larger current is induced."), ("A wire is moved parallel to the magnetic field lines.", "No current is induced."),
       ("The current in a nearby coil is switched on.", "A brief current is induced."), ("A steady current flows in a nearby coil.", "No current is induced.")]


@safe
def g_ind():
    s, a = R.choice(IND)
    k = R.random() < 0.6
    if not once(("in", s, k)):
        return None
    if not k:
        yes = not a.startswith("No")
        return item("%s Is a current induced in the coil?" % s, "Yes, because the magnetic field through the coil changes." if yes else "No, because the magnetic field through the coil does not change.",
                    ["No, because the magnetic field through the coil does not change." if yes else "Yes, because the magnetic field through the coil changes.", "Yes, any magnet near a coil makes current.", "No, coils never carry induced current."],
                    "Only a changing field induces current.")
    return item("%s What does the meter show?" % s, a, R.sample(sorted({x[1] for x in IND if x[1] != a}), 3), "Current is induced only when the magnetic field through the coil changes.")


DEV = [("electric motor", "Current in a coil in a magnetic field feels a force that makes it spin."), ("generator", "A spinning coil in a magnetic field has a current induced in it."),
       ("transformer", "A changing current in one coil induces a current in another coil."), ("loudspeaker", "A changing current in a coil makes it push a cone back and forth."),
       ("electric guitar pickup", "A vibrating steel string changes the magnetic field in a coil and induces a current."), ("induction cooktop", "A changing magnetic field induces currents in the metal pan, which heat it."),
       ("wireless phone charger", "A changing magnetic field from a coil in the pad induces a current in a coil in the phone."), ("junkyard crane magnet", "A large current in a coil makes a strong magnetic field that can be switched off.")]


@safe
def g_dev():
    d, p = R.choice(DEV)
    k = R.random() < 0.55
    if not once(("dv", d, k)):
        return None
    if k:
        return item("How does a %s work?" % d, p, R.sample([x[1] for x in DEV if x[1] != p], 3), "Electricity and magnetism are linked.")
    return item("Which device works like this? “%s”" % p, d, R.sample([x[0] for x in DEV if x[0] != d], 3), "Match the device to the principle.")


@safe
def g_data():
    who = P.next()[0]
    var = R.choice(["turns", "current"])
    if var == "turns":
        xs = [10, 20, 30, 40, 50]
        per = R.choice([1, 2, 3, 4, 5])
        head = "Turns of wire"
    else:
        xs = [0.5, 1.0, 1.5, 2.0, 2.5]
        per = R.choice([2, 3, 4, 5, 6])
        head = "Current (A)"
    ys = [int(round(x * per / (5 if var == "turns" else 0.5))) for x in xs]
    k = R.choice(["trend", "read", "pred", "ctrl"])
    if not once(("dt", var, per, k)) or (k in ("trend", "ctrl") and not once(("dk", k), 3)):
        return None
    tab = table([head, "Paper clips picked up"], [[num(x), str(y)] for x, y in zip(xs, ys)])
    if k == "trend":
        return item(tab + "What do %s's results show?" % who, "More %s makes a stronger electromagnet." % ("turns" if var == "turns" else "current"),
                    ["More %s makes a weaker electromagnet." % ("turns" if var == "turns" else "current"), "The electromagnet's strength never changes.", "Paper clips repel the coil."], "The clip count rises steadily.")
    if k == "read":
        i = R.randrange(5)
        g = str(ys[i])
        return item(tab + "How many clips did %s's electromagnet pick up at %s?" % (who, num(xs[i]) + (" turns" if var == "turns" else " A")), g, uniq(g, [str(y) for y in ys] + [str(ys[i] + 1)]), "Read the row.")
    if k == "pred":
        nx = xs[-1] + (xs[1] - xs[0])
        ny = ys[-1] + (ys[1] - ys[0])
        g = "about %d" % ny
        return item(tab + "Predict the number of clips for %s." % (num(nx) + (" turns" if var == "turns" else " A")), g, uniq(g, ["about %d" % ys[-1], "about %d" % (ys[-1] * 2), "about 0", "about %d" % (ny + 5)]),
                    "Each step adds about %d clips." % (ys[1] - ys[0]))
    ctrl = "the current and the nail" if var == "turns" else "the number of turns and the nail"
    return item(tab + "In %s's test, what should stay the same in every trial?" % who, ctrl, ["the %s" % ("number of turns" if var == "turns" else "current"), "the number of paper clips picked up", "nothing"],
                "Change only the variable you are testing.")


B1 = bank([
    ("What does an electric current in a wire produce?", "a magnetic field around the wire", ["an electric field only", "a sound wave", "nothing"], "Oersted's discovery."),
    ("What is an electromagnet?", "a coil of wire that becomes a magnet when current flows", ["a permanent bar magnet", "a battery", "a type of motor brush"], "Can be switched on and off."),
    ("What is electromagnetic induction?", "making a current by changing the magnetic field through a coil", ["making a magnet with a battery", "heating a wire", "charging by rubbing"], "Faraday's discovery."),
    ("What does a generator change into electrical energy?", "kinetic (motion) energy", ["chemical energy", "light energy", "nothing; it creates energy"], "Spinning coils."),
    ("What does an electric motor change electrical energy into?", "kinetic (motion) energy", ["chemical energy", "nuclear energy", "light only"], "Current + field → force."),
    ("Why does a compass needle move near a wire with current?", "The current makes a magnetic field that pushes on the needle.", ["The wire is hot.", "The wire is made of iron.", "Compasses detect electricity directly."], "Current → field."),
    ("What does a transformer do?", "changes the voltage of alternating current", ["stores energy like a battery", "turns AC into light", "makes current from heat"], "Needs changing current."),
    ("Why must transformers use alternating current?", "Only a changing current makes a changing magnetic field that induces current.", ["AC is safer to touch.", "DC is too strong.", "AC has no magnetic field."], "Induction needs change."),
])
B5 = bank([
    ("A student moves a magnet into a coil and sees no reading. Which change would most likely give a reading?", "move the magnet faster or use a coil with more turns", ["hold the magnet still", "use a plastic magnet", "remove the meter"], "Faster change → more current."),
    ("Why do power plants spin huge coils inside magnets?", "To induce large electric currents by changing the magnetic field.", ["To cool the magnets.", "To store electricity.", "To make the magnets stronger."], "Generators."),
    ("How could you show that a current makes a magnetic field?", "Place a compass near a wire and switch the current on and off.", ["Measure the wire's mass.", "Shine light on the wire.", "Heat the wire."], "Oersted's experiment."),
    ("Maglev trains float above the track. What makes this possible?", "Strong electromagnets repel and attract magnets in the track.", ["Air pressure only.", "Gravity is switched off.", "Static electricity."], "Electromagnetism."),
    ("A bike light powered by a wheel generator gets brighter when you ride faster. Why?", "The magnetic field in the coil changes faster, inducing more current.", ["The battery charges.", "The bulb gets hotter from friction.", "The wheel stores light."], "Rate of change."),
])


def body():
    think = ("<p><b>Electricity and magnetism are two sides of one force.</b></p>"
             "<ul><li>A current makes a magnetic field. A coil with an iron core is an electromagnet; more turns or more current make it stronger.</li>"
             "<li>A changing magnetic field through a coil induces a current. Faster change, stronger magnet or more turns → more current.</li>"
             "<li>Motors: current → motion. Generators: motion → current. Transformers: changing current → current in a second coil.</li></ul>")
    ex = [("Magnet held still in a coil. Current?", ["The field is not changing"], "none"),
          ("Double the turns on an electromagnet?", ["More turns → stronger field"], "stronger")]
    mist = ["Thinking a still magnet in a coil makes a current.", "Thinking a generator creates energy from nothing.", "Mixing up motors and generators."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Current makes magnetism", B1 + [(g_em, 7), (g_dev, 5)]),
        ("Electromagnets", [(g_data, 10), (g_em, 4), (g_ind, 6)]),
        ("Induction", [(g_ind, 6), (g_dev, 6), (g_data, 8)]),
        ("Motors and generators", [(g_dev, 4), (g_ind, 6), (g_em, 6), (g_data, 4)]),
        ("Investigating electromagnetism", B5 + [(g_data, 8), (g_em, 7)]),
    ])
    make("physics", "electromagnetism-and-induction", 7, "HS-PS2-5",
         "Plan and conduct an investigation to provide evidence that an electric current can produce a magnetic field and that a changing magnetic field can produce an electric current.",
         "Electromagnetism and Induction",
         "Electromagnetism Worksheets: Electromagnets, Induction, Motors and Generators (Physics)",
         "Electromagnetism",
         "Free high school physics worksheets on electromagnetism (NGSS HS-PS2-5): magnetic fields from currents, electromagnets, electromagnetic induction, motors, generators and transformers. 100 questions with answers.",
         "Currents make fields; changing fields make currents.",
         "Electromagnets, motors, generators and transformers all use this link.",
         body(),
         [("How does an electric current make a magnetic field?", "Moving charges in a wire create a magnetic field around it. Winding the wire into a coil concentrates the field."),
          ("What is electromagnetic induction?", "When the magnetic field through a coil changes, a current is induced in the coil. A faster change gives a larger current."),
          ("What is the difference between a motor and a generator?", "A motor uses current in a magnetic field to make motion. A generator uses motion in a magnetic field to make current.")],
         sets)


if __name__ == "__main__":
    main()
