# -*- coding: utf-8 -*-
"""
UK Year 6 science: Brightness and Voltage (Electricity)
  python tools/gen_uk_science_y6_brightness_and_voltage.py
How the number and voltage of cells changes the brightness of lamps, the loudness of buzzers and the speed of motors;
more lamps in a series circuit share the voltage; adding up cell voltages; and reading investigation results.
Wrong answers come from real mistakes: "adding a lamp makes both lamps brighter", "more cells make the lamp dimmer",
"voltage of two 1.5 V cells is 1.5 V", "any number of cells is safe for a lamp".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig
from uk_sci_pics import circuit
from sci_phys import uniq, num

U = Unit(61614)
R = U.R
P = People(R)


def draw(cells, loads):
    top = ["cell"] * cells
    return circuit(top, loads, "circuit with %d cell%s and %d %s" % (cells, "" if cells == 1 else "s", len(loads), loads[0] + ("s" if len(loads) > 1 else "")))


def g_cmp():
    ca, la = R.choice([1, 2, 3]), R.choice([1, 2])
    cb, lb = R.choice([1, 2, 3]), R.choice([1, 2])
    if (ca, la) == (cb, lb) or not once(("cm", ca, la, cb, lb)):
        return None
    ra, rb = ca / la, cb / lb
    a = "A" if ra > rb else "B" if rb > ra else "same"
    ans = {"A": "the lamps in circuit A", "B": "the lamps in circuit B", "same": "They are equally bright."}[a]
    w = [x for x in ["the lamps in circuit A", "the lamps in circuit B", "They are equally bright."] if x != ans] + ["Neither lights up."]
    q = ("<div class='qfig'><b>Circuit A</b><br>%s</div><div class='qfig'><b>Circuit B</b><br>%s</div>" % (draw(ca, ["lamp"] * la), draw(cb, ["lamp"] * lb))
         + "Circuit A has %d cell%s and %d lamp%s. Circuit B has %d cell%s and %d lamp%s. All the cells and lamps are the same. Which lamps are brighter?"
         % (ca, "" if ca == 1 else "s", la, "" if la == 1 else "s", cb, "" if cb == 1 else "s", lb, "" if lb == 1 else "s"))
    e = "Brightness depends on the cells shared between the lamps: A has %d cell%s for %d lamp%s, B has %d for %d." % (ca, "" if ca == 1 else "s", la, "" if la == 1 else "s", cb, lb)
    return item(q, ans, w, e)


CHG = [("add another cell", "lamp", "The lamp gets brighter."), ("take away a cell", "lamp", "The lamp gets dimmer."),
       ("add another lamp in series", "lamp", "Both lamps are dimmer than one lamp was."), ("add another cell", "buzzer", "The buzzer gets louder."),
       ("take away a cell", "buzzer", "The buzzer gets quieter."), ("add another cell", "motor", "The motor spins faster."),
       ("take away a cell", "motor", "The motor spins more slowly."), ("use a higher-voltage battery", "lamp", "The lamp gets brighter."),
       ("open the switch", "lamp", "The lamp goes out."), ("add another buzzer in series", "buzzer", "Both buzzers are quieter.")]


def g_chg():
    c, comp, a = R.choice(CHG)
    n = R.choice([1, 2, 3])
    if not once(("ch", c, comp, n)):
        return None
    opts = {"lamp": ["The lamp gets brighter.", "The lamp gets dimmer.", "Both lamps are dimmer than one lamp was.", "The lamp goes out.", "Nothing changes."],
            "buzzer": ["The buzzer gets louder.", "The buzzer gets quieter.", "Both buzzers are quieter.", "Nothing changes."],
            "motor": ["The motor spins faster.", "The motor spins more slowly.", "The motor goes out like a lamp.", "Nothing changes."]}[comp]
    w = R.sample([x for x in opts if x != a], 3)
    return item("A circuit has %d cell%s, a switch and one %s. The switch is closed. You %s. What happens?" % (n, "" if n == 1 else "s", comp, c), a, w,
                "More cells (more voltage) push more current; sharing with extra components means less each.")


def g_volt():
    k = R.choice(["sum", "how", "mix"])
    if k == "sum":
        n = R.choice([2, 3, 4, 5, 6])
        v = R.choice([1.5, 1.2])
        if not once(("vs", n, v)):
            return None
        g = "%s V" % num(n * v, 2)
        return item("A battery is made of %d cells joined in a line, each %s V. What is its total voltage?" % (n, num(v, 2)), g,
                    uniq(g, ["%s V" % num(v, 2), "%s V" % num(n + v, 2), "%s V" % num(n * v * 2, 2), "%s V" % num(v / n, 2)]), "%d × %s = %s V." % (n, num(v, 2), num(n * v, 2)))
    if k == "how":
        t = R.choice([3, 4.5, 6, 7.5, 9])
        n = int(round(t / 1.5))
        if not once(("vh", t)):
            return None
        g = "%d cells" % n
        return item("How many 1.5 V cells are needed to make %s V?" % num(t, 2), g, uniq(g, ["%d cells" % (n + 1), "%d cells" % (n * 2), "%d cells" % max(1, n - 1), "%s cells" % num(t, 2)]),
                    "%s ÷ 1.5 = %d." % (num(t, 2), n))
    vs = R.sample([1.5, 3, 4.5, 6], 2)
    if vs[0] == vs[1] or not once(("vm", tuple(sorted(vs)))):
        return None
    hi = max(vs)
    g = "the %s V battery" % num(hi, 2)
    return item("The same lamp is connected first to a %s V battery and then to a %s V battery. With which battery is it brighter?" % (num(vs[0], 2), num(vs[1], 2)), g,
                ["the %s V battery" % num(min(vs), 2), "They are equally bright.", "It does not light with either."], "Higher voltage gives a brighter lamp (if the lamp is rated for it).")


def g_inv():
    who = P.next()[0]
    kind = R.choice(["lamp", "buzzer"])
    cells = [1, 2, 3, 4]
    if kind == "lamp":
        base = R.choice([40, 50, 60])
        vals = [base, base * 2 + R.choice([-10, 0, 10]), base * 3 + R.choice([-10, 0, 10]), base * 4 + R.choice([-20, 0, 20])]
        head, unit = "Light sensor reading (lux)", "lux"
    else:
        base = R.choice([50, 55, 60])
        vals = [base, base + R.choice([6, 8]), base + R.choice([12, 14]), base + R.choice([17, 19])]
        head, unit = "Loudness (dB)", "dB"
    k = R.choice(["read", "read", "pattern", "var", "diff"])
    ri = R.randrange(4)
    if not once(("iv", kind, k, ri if k == "read" else 0, tuple(vals))) or (k in ("pattern", "var") and not once(("ik", kind, k), 2)):
        return None
    tab = table(["Number of cells", head], [[str(a), str(b)] for a, b in zip(cells, vals)])
    intro = tab + "%s tested a %s with different numbers of cells. " % (who, kind)
    if k == "read":
        g = "%d %s" % (vals[ri], unit)
        return item(intro + "What was the reading with %d cell%s?" % (cells[ri], "" if ri == 0 else "s"), g, uniq(g, ["%d %s" % (v, unit) for v in vals] + ["%d %s" % (vals[ri] + 5, unit)]),
                    "Read the row for %d cell%s." % (cells[ri], "" if ri == 0 else "s"))
    if k == "pattern":
        a = "The more cells, the brighter the lamp." if kind == "lamp" else "The more cells, the louder the buzzer."
        w = ["The more cells, the dimmer the lamp." if kind == "lamp" else "The more cells, the quieter the buzzer.", "The number of cells makes no difference.", "Only odd numbers of cells work."]
        return item(intro + "What pattern do the results show?", a, w, "The readings go up as cells are added.")
    if k == "var":
        return item(intro + "Which variable did %s change?" % who, "the number of cells", ["the %s reading" % ("light sensor" if kind == "lamp" else "loudness"), "the %s" % kind, "the length of the wires"],
                    "The changed variable goes in the first column.")
    d = vals[3] - vals[0]
    g = "%d %s" % (d, unit)
    return item(intro + "By how much did the reading increase from 1 cell to 4 cells?", g, uniq(g, ["%d %s" % (vals[3], unit), "%d %s" % (vals[0], unit), "%d %s" % (d + 10, unit), "%d %s" % (vals[3] + vals[0], unit)]),
                "%d − %d = %d." % (vals[3], vals[0], d))


B1 = bank([
    ("What does voltage measure?", "how hard the cell pushes the current around the circuit", ["the length of the wires", "how heavy the battery is", "the colour of the bulb"], "Measured in volts (V)."),
    ("What is the voltage of a typical AA cell?", "1.5 V", ["15 V", "230 V", "0.5 V"], "Most small cells are 1.5 V."),
    ("What happens to a lamp when more cells are added in series?", "It gets brighter.", ["It gets dimmer.", "It stays the same.", "It changes colour."], "More voltage, more current."),
    ("What happens to two lamps in series compared with one lamp on the same cell?", "Both are dimmer.", ["Both are brighter.", "One is brighter, one goes out.", "Nothing changes."], "They share the voltage."),
    ("Why can too many cells damage a lamp?", "Too much current makes the filament overheat and break.", ["Cells are too heavy.", "The lamp gets cold.", "Lamps need no electricity."], "The bulb blows."),
    ("What happens to a buzzer when you use a higher-voltage battery?", "It gets louder.", ["It gets quieter.", "It changes into a lamp.", "It stops working."], "More voltage, louder buzz."),
    ("Mains electricity in UK homes is about 230 V. Why should you never experiment with it?", "It is dangerous and can kill.", ["It is too weak.", "It only works at night.", "It is the same as a cell."], "Only use cells in school."),
    ("How does adding a cell affect a motor?", "It spins faster.", ["It spins more slowly.", "It stops forever.", "It glows."], "More voltage."),
])
B5 = bank([
    ("Why should all the lamps be the same type in a brightness investigation?", "so that only the number of cells changes the result", ["to make it look neat", "to save money", "lamps are always the same"], "Control variables."),
    ("Why might a light sensor give better results than your eyes?", "It gives a number, so small differences can be measured fairly.", ["Eyes cannot see light.", "Sensors make the lamp brighter.", "It is quicker to guess."], "Measure, do not guess."),
    ("A torch is dim. What is the most likely cause?", "The cells are running out.", ["The switch is closed.", "The torch is too clean.", "The lamp is too bright."], "Old cells give less voltage."),
    ("How could you make a doorbell buzzer louder?", "use a higher-voltage battery that suits the buzzer", ["add more lamps in series", "use longer, thinner wires", "open the switch"], "More voltage."),
    ("Why do we repeat readings in an electricity investigation?", "to check the results and spot mistakes", ["to make the cells last longer", "because one reading is always wrong", "to make the lamp brighter"], "Reliable results."),
])


def body():
    think = ("<p><b>More voltage makes components work harder; more components share the voltage.</b></p>"
             "<ul><li>Each cell is usually 1.5 V. Cells in a line add up: 3 cells = 4.5 V.</li>"
             "<li>More cells: brighter lamps, louder buzzers, faster motors.</li>"
             "<li>More lamps in series share the voltage, so each one is dimmer. Too many cells can blow a lamp.</li></ul>")
    ex = [("4 cells of 1.5 V. Total?", ["4 × 1.5"], "6 V"),
          ("2 cells, 1 lamp vs 2 cells, 2 lamps. Brighter?", ["One lamp gets all the voltage"], "the single lamp")]
    mist = ["Thinking adding a lamp makes both lamps brighter.", "Thinking two 1.5 V cells give 1.5 V.", "Thinking any number of cells is safe for a lamp."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Cells and voltage", B1 + [(g_volt, 8), (g_chg, 4)]),
        ("Changing a circuit", [(g_chg, 14), (g_volt, 6)]),
        ("Comparing circuits", [(g_cmp, 17), (g_volt, 3)]),
        ("Investigations", [(g_inv, 16), (g_cmp, 4)]),
        ("Thinking it through", B5 + [(g_inv, 10), (g_volt, 3), (g_chg, 2)]),
    ])
    make_uk(6, "brightness-and-voltage", 14, "Electricity",
            "Associate the brightness of a lamp or the volume of a buzzer with the number and voltage of cells used in the circuit.",
            "Brightness and Voltage",
            "Year 6 Science: Brightness and Voltage Worksheets (Cells, Lamps and Buzzers)",
            "Brightness and Voltage",
            "Free Year 6 science worksheets on brightness and voltage: how the number and voltage of cells changes lamp brightness, buzzer volume and motor speed, with circuit comparisons and investigations. 100 questions with answers.",
            "More cells, brighter lamps.",
            "Voltage pushes current; extra lamps in series share it and get dimmer.",
            body(),
            [("Why does adding cells make a lamp brighter?", "Each cell adds voltage, which pushes more current through the lamp, so it glows brighter (up to what the lamp can safely take)."),
             ("Why are two lamps dimmer than one?", "In a series circuit the two lamps share the same voltage from the cells, so each gets less and glows less brightly."),
             ("How do you work out the voltage of a battery?", "Add the voltages of the cells joined in a line. Three 1.5 V cells make 4.5 V.")],
            sets)


if __name__ == "__main__":
    main()
