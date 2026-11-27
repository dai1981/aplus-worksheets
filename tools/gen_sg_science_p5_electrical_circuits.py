# -*- coding: utf-8 -*-
"""
Singapore Primary 5 science: Electrical circuits (Energy)
  python tools/gen_sg_science_p5_electrical_circuits.py
An electric current flows only in a closed circuit. Components: batteries, bulbs, wires and switches.
Bulbs in series share the current (dimmer; if one fuses, all go out); bulbs in parallel are each as bright as one bulb alone
(if one fuses, the others stay lit). More batteries in series make the bulbs brighter; batteries in parallel give the same
brightness but last longer. Using electricity safely and wisely. Circuit diagrams are drawn with uk_sci_pics; UK Year 4 and
Year 6 circuit questions are reused with Singapore names (no voltage or decibels).
Wrong answers come from real mistakes: "a bulb lights with one wire", "two bulbs in parallel are dimmer than one",
"if one bulb in parallel fuses, all go out", "an open switch lets current flow".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto
import uk_sci_pics as K

U = Unit(63508)
R = U.R
P = People(R)
REP = [(r"\b\d+p coins?\b", "10-cent coin"), (r"lolly stick", "ice-cream stick")]
DROP = ["volt", " V ", " V.", "dB", "decibel", "winter", "snow", "mains electricity comes", "power station"]
EA = use(U, "gen_uk_science_y4_electrical_appliances_and_circuits", rep=REP, drop=DROP)
CS = use(U, "gen_uk_science_y6_circuits_and_switches", rep=REP, drop=DROP)
BV = use(U, "gen_uk_science_y6_brightness_and_voltage", rep=REP, drop=DROP)


def fig(svg):
    return "<div class='qfig'>%s</div>" % svg


def draw(cells, lamps, par):
    """cells in series on the top wire; lamps in series on the bottom wire, or each in its own parallel branch"""
    if par:
        return K.parallel([["cell"] * cells] + [["lamp"] for _ in range(lamps)])
    return K.circuit(["cell"] * cells, ["lamp"] * lamps)


def bright(cells, lamps, par):
    """brightness of each bulb, in the simple rule pupils use: cells in series push harder; bulbs in series share"""
    return (cells / float(lamps)) ** 2 if not par else float(cells ** 2)


def g_cmp():
    a = (R.randint(1, 3), R.randint(1, 3), R.random() < 0.4)
    b = (R.randint(1, 3), R.randint(1, 3), R.random() < 0.4)
    if a == b or (a[1] == 1 and a[2]) or (b[1] == 1 and b[2]):
        return None
    ba, bb = bright(*a), bright(*b)
    if not once(("cp", a, b)) or not once(("cpn",), 16):
        return None
    if abs(ba - bb) < 1e-9:
        ans, w = "They are equally bright.", ["the bulbs in circuit A", "the bulbs in circuit B", "None of the bulbs light."]
    elif ba > bb:
        ans, w = "the bulbs in circuit A", ["the bulbs in circuit B", "They are equally bright.", "None of the bulbs light."]
    else:
        ans, w = "the bulbs in circuit B", ["the bulbs in circuit A", "They are equally bright.", "None of the bulbs light."]

    def say(c):
        return "%d batter%s and %d bulb%s%s" % (c[0], "y" if c[0] == 1 else "ies", c[1], "" if c[1] == 1 else "s",
                                                " in parallel" if c[2] else (" in series" if c[1] > 1 else ""))
    q = ("<div class='qfig'><b>Circuit A</b><br>%s</div><div class='qfig'><b>Circuit B</b><br>%s</div>"
         "Circuit A has %s. Circuit B has %s. All the batteries and bulbs are the same. In which circuit is each bulb brighter?") % (
        draw(*a), draw(*b), say(a), say(b))
    return item(q, ans, w, "More batteries in series make bulbs brighter. Bulbs in series share and are dimmer; each bulb in parallel is as bright as one bulb alone.")


def g_fuse():
    n = R.randint(2, 4)
    par = R.choice([True, False])
    if not once(("fu", n, par)):
        return None
    if par:
        a = "%d bulb%s" % (n - 1, "" if n == 2 else "s")
        w = ["0 bulbs", "%d bulbs" % n if n > 1 else "1 bulb", "only half of them"]
        e = "In parallel, each bulb has its own path, so the others stay lit."
    else:
        a = "0 bulbs"
        w = ["%d bulb%s" % (n - 1, "" if n == 2 else "s"), "%d bulbs" % n, "only half of them"]
        e = "In series, there is only one path. When one bulb fuses, the circuit is broken and all the bulbs go out."
    return item("%s<br>%d identical bulbs are connected %s to a battery, as shown. One bulb fuses. How many bulbs stay lit?" % (fig(draw(1, n, par)), n, "in parallel" if par else "in series"),
                a, w, e)


def g_switch():
    n = R.randint(2, 4)
    sw = R.sample(range(n), R.randint(1, n - 1))
    br = [["cell"]] + [["lamp", "switch_open"] if i in sw else ["lamp"] for i in range(n)]
    if not once(("sw", n, len(sw))):
        return None
    lit = n - len(sw)
    return item("%s<br>This circuit has %d bulbs. How many bulbs light up?" % (fig(K.parallel(br)), n), str(lit), [str(x) for x in range(0, n + 1) if x != lit][:3],
                "A bulb in a branch with an open switch does not light. The other branches are complete circuits.")


def g_closed():
    k = R.choice(["open", "closed", "gap", "nocell"])
    if not once(("cl", k)):
        return None
    if k == "open":
        svg = K.circuit(["cell", "switch_open"], ["lamp"])
        a = "No. The open switch makes a gap, so the circuit is not closed."
    elif k == "closed":
        svg = K.circuit(["cell", "switch_closed"], ["lamp"])
        a = "Yes. It is a closed circuit."
    elif k == "gap":
        svg = K.circuit(["cell", "gap"], ["lamp"])
        a = "No. There is a gap in the wires."
    else:
        svg = K.circuit(["switch_closed"], ["lamp"])
        a = "No. There is no battery to make the current flow."
    w = [x for x in ["Yes. It is a closed circuit.", "No. The open switch makes a gap, so the circuit is not closed.", "No. There is a gap in the wires.",
                     "No. There is no battery to make the current flow."] if x != a]
    return item("%s<br>Will the bulb light up?" % fig(svg), a, w, "Current flows only in a closed circuit with a source of electricity.")


CONV = [("an electric fan", "kinetic energy"), ("a bulb", "light energy and heat energy"), ("a buzzer", "sound energy"), ("an electric kettle", "heat energy"),
        ("a radio", "sound energy"), ("a toy car motor", "kinetic energy"), ("an iron", "heat energy"), ("a hair dryer", "heat energy and kinetic energy")]
FORMS = ["kinetic energy", "light energy and heat energy", "sound energy", "heat energy", "chemical potential energy", "heat energy and kinetic energy"]


def g_conv():
    a, f = R.choice(CONV)
    if not once(("cv", a)):
        return None
    return item("%s changes electrical energy mainly into which form of energy?" % (a[0].upper() + a[1:]), f, R.sample([x for x in FORMS if x not in f and f not in x], 3),
                "%s gives out %s." % (a[0].upper() + a[1:], f))


SAVE = ["switching off lights when leaving a room", "setting the air-conditioner to 25 °C", "using energy-saving LED bulbs", "unplugging chargers that are not in use",
        "using a fan instead of an air-conditioner", "drying clothes in the sun instead of a dryer"]
WASTE = ["leaving the television on in an empty room", "opening the fridge door for a long time", "setting the air-conditioner to 18 °C",
         "leaving lights on during the day", "charging a phone that is already full overnight", "using a dryer for one T-shirt"]


def g_save():
    k = R.choice(["s", "w"])
    a = R.choice(SAVE if k == "s" else WASTE)
    if not once(("sv", a)):
        return None
    return item("Which of these %s electricity?" % ("saves" if k == "s" else "wastes"), a, R.sample(WASTE if k == "s" else SAVE, 3),
                "Saving electricity saves money and reduces the burning of fuels in power stations.")


B1 = bank([
    ("What is needed for an electric current to flow?", "a closed circuit with a source of electricity such as a battery", ["a bulb only", "an open switch", "one wire only"], "The circuit must be a complete loop."),
    ("What does a switch do in a circuit?", "It opens or closes the circuit.", ["It makes the battery stronger.", "It stores electricity.", "It makes the bulb brighter."], "A closed switch lets current flow."),
    ("What is an open circuit?", "a circuit with a gap, so no current flows", ["a circuit that works", "a circuit with many bulbs", "a circuit with no wires at all"], "A switch that is off makes an open circuit."),
    ("What is the function of a battery in a circuit?", "It provides the electrical energy that makes the current flow.", ["It lights up.", "It makes a sound.", "It breaks the circuit."], "Batteries are the source of electricity."),
    ("Which form of energy does a bulb change electrical energy into?", "light energy and heat energy", ["sound energy only", "kinetic energy only", "chemical energy only"], "Bulbs get warm when they are lit."),
    ("Which form of energy does a buzzer give out?", "sound energy", ["light energy only", "chemical energy only", "no energy"], "A buzzer changes electrical energy into sound."),
    ("Which form of energy is stored in a battery?", "chemical potential energy", ["light energy", "sound energy", "kinetic energy"], "The battery changes it into electrical energy."),
    ("Why do batteries stop working after some time?", "The chemicals inside are used up.", ["The wires melt.", "The bulbs take the batteries.", "Electricity leaks into the air."], "Used batteries should be recycled."),
])
B2 = bank([
    ("Two bulbs are connected in series. One bulb fuses. What happens to the other bulb?", "It goes out.", ["It becomes brighter.", "It stays lit as before.", "It becomes dimmer but stays lit."], "In series there is only one path for the current."),
    ("Two bulbs are connected in parallel. One bulb fuses. What happens to the other bulb?", "It stays lit.", ["It goes out.", "It becomes dimmer.", "It flickers and goes out."], "Each bulb in parallel has its own path."),
    ("Why are the lights in a house connected in parallel?", "Each light can be switched on and off on its own, and one fused bulb does not affect the others.", ["They are brighter in series.", "Parallel circuits use no electricity.", "They are cheaper to switch off together."], "Homes use parallel circuits."),
    ("What happens to the brightness of bulbs when more bulbs are added in series?", "The bulbs become dimmer.", ["The bulbs become brighter.", "The brightness does not change.", "The bulbs go out."], "Bulbs in series share the electrical energy."),
    ("What happens to the brightness of a bulb when more batteries are added in series?", "The bulb becomes brighter.", ["The bulb becomes dimmer.", "The brightness does not change.", "The bulb goes out at once."], "More batteries in series push a bigger current."),
    ("Two batteries are connected in parallel to one bulb. How does the bulb compare with a bulb lit by one battery?", "It is equally bright, but the batteries last longer.", ["It is twice as bright.", "It is dimmer.", "It does not light."], "Batteries in parallel share the work."),
    ("A torch has two batteries in series. One battery is put in the wrong way round. What happens?", "The bulb does not light or is very dim.", ["The bulb is brighter.", "Nothing changes.", "The torch becomes a magnet."], "The batteries push against each other."),
    ("Why does a torch need a closed switch to work?", "The switch completes the circuit so current can flow.", ["The switch makes light.", "The switch stores energy.", "The switch cools the bulb."], "An open switch leaves a gap."),
])
B3 = bank([
    ("Why should we not touch switches with wet hands?", "Water can conduct electricity and we may get an electric shock.", ["Water damages the paint.", "Switches do not work with wet hands.", "Our hands will get cold."], "Always dry your hands first."),
    ("Why should we not overload a power socket with many plugs?", "The wires can overheat and cause a fire.", ["The lights will become brighter.", "The plugs will become magnets.", "It saves electricity."], "Too much current makes wires hot."),
    ("Why should we never poke a metal object into a power socket?", "Metal conducts electricity and can give a deadly electric shock.", ["Metal blocks the electricity.", "The socket will break only.", "It is safe if the object is small."], "Mains electricity is very dangerous."),
    ("Why should frayed electrical wires be replaced?", "The bare wire can give an electric shock or start a fire.", ["They look untidy.", "They use less electricity.", "They make appliances brighter."], "The plastic covering is an insulator for safety."),
    ("Why is it good to save electricity?", "Most electricity in Singapore is made by burning natural gas, so saving it saves money and reduces pollution.", ["Electricity never runs out, so it does not matter.", "Saving electricity makes bulbs brighter.", "It makes batteries heavier."], "Power stations burn fuels to make electricity."),
])
B5 = bank([
    ("Siti tested how the number of batteries in series affects the brightness of a bulb. What should she change?", "the number of batteries", ["the type of bulb", "the length of the wires", "the type of switch"], "Change only one variable."),
    ("Why should Siti use the same type of bulb each time?", "so that only the number of batteries affects the brightness", ["so that the bulb is brighter", "so that the batteries last longer", "to make the circuit open"], "This makes the test fair."),
    ("Ravi used a light sensor to measure the brightness of the bulb. Why is this better than using his eyes?", "It gives a number, so small differences can be measured.", ["Eyes cannot see bulbs.", "Sensors make the bulb brighter.", "It is quicker to guess."], "Measurements are more accurate than guesses."),
    ("Mei Ling's bulb did not light. The battery and bulb were working. What is the most likely reason?", "There was a gap or a loose wire in the circuit.", ["The bulb was too bright.", "The wires were too short.", "The circuit was closed."], "Check for gaps in the circuit."),
    ("A pupil wants one switch to turn off only one of two bulbs. How should the bulbs be connected?", "in parallel, with the switch in the branch of that bulb", ["in series with one switch", "with no switch", "with the switch next to the battery"], "A switch in one branch controls only that branch."),
])


def body():
    think = ("<p><b>An electric current flows only in a closed circuit.</b></p>"
             "<ul><li>A circuit needs a source (battery), wires, and components such as bulbs; a <b>switch</b> opens or closes the circuit.</li>"
             "<li><b>Bulbs in series</b> are dimmer, and if one fuses, all go out.</li>"
             "<li><b>Bulbs in parallel</b> are each as bright as one bulb alone, and if one fuses, the others stay lit.</li>"
             "<li>More batteries in series make bulbs brighter. Batteries in parallel give the same brightness but last longer.</li></ul>")
    ex = [("Three bulbs are in parallel. One fuses. How many stay lit?", ["Each bulb has its own path", "The other two paths are still closed"], "2 bulbs."),
          ("A second battery is added in series. What happens to the bulb?", ["More batteries in series push more current"], "It becomes brighter.")]
    mist = ["Thinking a bulb can light with one wire. The circuit must be a closed loop.",
            "Thinking bulbs in parallel are dimmer than one bulb. Each is as bright as one bulb alone.",
            "Thinking all bulbs go out when one bulb in parallel fuses.",
            "Thinking an open switch lets current flow."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Closed circuits", B1 + [(g_closed, 4), (CS.g_work, 4), (EA.g_txt, 2), (EA.g_part, 2)]),
        ("Series and parallel", B2 + [(g_fuse, 5), (g_switch, 4), (CS.g_two, 3)]),
        ("Brightness of bulbs", [(g_cmp, 7), (BV.g_chg, 5), (BV.g_cmp, 3), (g_fuse, 3), (g_switch, 2)]),
        ("Using electricity safely and wisely", B3 + EA.B1 + EA.B5 + [(g_save, 5), (g_conv, 3), (EA.g_app, 2), (CS.g_fault, 1)]),
        ("PSLE-style questions", B5 + CS.B5 + [(g_cmp, 4), (g_conv, 3), (CS.g_fault, 2), (g_switch, 2), (CS.g_two, 2)]),
    ])
    make_sg(5, "electrical-circuits", 8, "Energy", "Energy forms and uses (Electrical systems: circuits)",
            "Recognise that an electric current flows only in a closed circuit and identify the components of a circuit (batteries, bulbs, wires and switches). "
            "Investigate the effect of the number and arrangement of batteries and bulbs (in series and in parallel) on the brightness of bulbs, and show an "
            "understanding of the safe and wise use of electricity (summary of the MOE Primary Science Syllabus).",
            "Electrical Circuits",
            "Primary 5 Science: Electrical Circuits Worksheets – Series and Parallel (with Answers)",
            "Electrical circuits",
            "Free Primary 5 science worksheets for Singapore pupils on electrical circuits: closed circuits, switches, bulbs and batteries in series and parallel, brightness, and electrical safety. 100 questions with answers.",
            "Current flows only in a closed circuit.",
            "Series or parallel changes how bright the bulbs are.",
            body(),
            [("What is the difference between series and parallel circuits?", "In series, the components are on one path, so if one bulb fuses all go out. In parallel, each bulb has its own path, so the others stay lit."),
             ("Are bulbs in parallel brighter than bulbs in series?", "Yes. Each bulb in parallel is as bright as one bulb alone, while bulbs in series share the electrical energy and are dimmer."),
             ("Why are home lights connected in parallel?", "So that each light can be switched on and off separately, and one fused bulb does not turn off the others.")],
            sets)


if __name__ == "__main__":
    main()
