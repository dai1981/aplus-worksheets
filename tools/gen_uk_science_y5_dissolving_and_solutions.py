# -*- coding: utf-8 -*-
"""
UK Year 5 science: Dissolving and Solutions (Properties and changes of materials)
  python tools/gen_uk_science_y5_dissolving_and_solutions.py
Soluble and insoluble materials, solute, solvent and solution, what makes things dissolve faster (heat, stirring,
smaller pieces), how much dissolves before a solution is saturated, mass is kept when dissolving, and getting the solid
back by evaporating.
Wrong answers come from real mistakes: "dissolved sugar has disappeared", "dissolving is the same as melting",
"mass goes down when salt dissolves", "sand dissolves if you stir long enough".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61505)
R = U.R
P = People(R)

SOL = ["salt", "sugar", "instant coffee granules", "bath salts", "bicarbonate of soda", "jelly cubes (in hot water)", "powdered drink mix"]
INS = ["sand", "chalk powder", "flour", "pepper", "rice", "marbles", "gravel", "sawdust", "cooking oil"]


def g_sol():
    k = R.random() < 0.5
    m = R.choice(SOL if k else INS)
    if not once(("so", m)):
        return None
    if k:
        return item("%s: soluble or insoluble in water?" % m.capitalize(), "soluble: it dissolves", ["insoluble: it does not dissolve", "it melts instead", "it turns into a gas"],
                    "%s dissolves to make a solution." % m.capitalize())
    return item("%s: soluble or insoluble in water?" % m.capitalize(), "insoluble: it does not dissolve", ["soluble: it dissolves", "it melts instead", "it turns into a gas"],
                "%s does not dissolve, even when stirred." % m.capitalize())


def g_pick():
    k = R.random() < 0.5
    if k:
        a = R.choice(SOL)
        w = R.sample(INS, 3)
        q = "Which of these will dissolve in water"
    else:
        a = R.choice(INS)
        w = R.sample(SOL, 3)
        q = "Which of these will NOT dissolve in water"
    if not once(("pk", k, a), 2):
        return None
    o = sorted([a] + w)
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, "Soluble materials dissolve; insoluble ones do not.")


def g_rate():
    who = P.next()[0]
    kind = R.choice(["temp", "stir", "size"])
    if kind == "temp":
        lab, head = ["10 °C", "20 °C", "40 °C", "60 °C"], "Water temperature"
        base = R.choice([200, 180, 240])
        vals = [base, int(base * 0.7), int(base * 0.4), int(base * 0.2)]
        rule = "The warmer the water, the faster the sugar dissolves."
        var = "the temperature of the water"
    elif kind == "stir":
        lab, head = ["not stirred", "stirred slowly", "stirred quickly"], "Stirring"
        base = R.choice([300, 240, 270])
        vals = [base, int(base * 0.5), int(base * 0.25)]
        rule = "The more the water is stirred, the faster the sugar dissolves."
        var = "how much the water was stirred"
    else:
        lab, head = ["sugar cube", "granulated sugar", "caster sugar", "icing sugar"], "Type of sugar"
        base = R.choice([200, 160, 180])
        vals = [base, int(base * 0.5), int(base * 0.3), int(base * 0.15)]
        rule = "The smaller the pieces, the faster the sugar dissolves."
        var = "the size of the sugar pieces"
    vals = [v + R.choice([-4, 0, 4]) for v in vals]
    k = R.choice(["read", "read", "fast", "rule", "var"])
    ri = R.randrange(len(lab))
    if not once(("ra", kind, k, ri if k == "read" else 0, tuple(vals))) or (k in ("rule", "var") and not once(("rk", kind, k), 2)):
        return None
    tab = table([head, "Time to dissolve (s)"], [[a, str(b)] for a, b in zip(lab, vals)])
    intro = tab + "%s timed how long 5 g of sugar took to dissolve in 100 ml of water. " % who
    if k == "read":
        g = "%d s" % vals[ri]
        ph = {"temp": "in water at %s", "stir": "when it was %s", "size": "for the %s"}[kind] % lab[ri]
        return item(intro + "How long did the sugar take to dissolve %s?" % ph, g, uniq(g, ["%d s" % v for v in vals] + ["%d s" % (vals[ri] + 20)]), "Read the row.")
    if k == "fast":
        a = lab[vals.index(min(vals))]
        return item(intro + "Which dissolved fastest?", a, [x for x in lab if x != a] + (["They all took the same time."] if len(lab) == 3 else []), "The shortest time is the fastest.")
    if k == "rule":
        return item(intro + "What do the results show?", rule, ["It makes no difference.", rule.replace("faster", "slower"), "Sugar only dissolves in cold water."], "Look at how the times change.")
    return item(intro + "Which variable did %s change?" % who, var, ["the time to dissolve", "the amount of sugar", "the amount of water"], "Only one variable changes.")


def g_sat():
    who = P.next()[0]
    temps = [20, 40, 60, 80]
    base = {20: 200, 40: 240, 60: 290, 80: 360}
    salt = R.random() < 0.4
    if salt:
        vals = [36, 37, 37, 38]
        name = "salt"
    else:
        vals = [base[t] + R.choice([-5, 0, 5]) for t in temps]
        name = "sugar"
    k = R.choice(["read", "more", "trend"])
    ri = R.randrange(4)
    if not once(("sa", name, tuple(vals), k, ri)) or (k == "trend" and not once(("st", name), 2)):
        return None
    tab = table(["Water temperature (°C)", "Most %s that dissolves in 100 ml (g)" % name], [[str(a), str(b)] for a, b in zip(temps, vals)])
    intro = tab + "%s found the most %s that would dissolve before no more could dissolve. " % (who, name)
    if k == "read":
        g = "%d g" % vals[ri]
        return item(intro + "How much %s dissolved at %d °C?" % (name, temps[ri]), g, uniq(g, ["%d g" % v for v in vals] + ["%d g" % (vals[ri] + 10)]), "Read the row.")
    if k == "more":
        d = vals[3] - vals[0]
        g = "%d g" % d
        return item(intro + "How much more %s dissolved at 80 °C than at 20 °C?" % name, g, uniq(g, ["%d g" % vals[3], "%d g" % vals[0], "%d g" % (d + 10), "%d g" % (vals[3] + vals[0])]), "%d − %d = %d g." % (vals[3], vals[0], d))
    if salt:
        return item(intro + "What do the results show about salt?", "Warmer water dissolves only a little more salt.", ["Warm water dissolves much more salt.", "Salt does not dissolve.", "Cold water dissolves the most salt."], "The numbers hardly change.")
    return item(intro + "What do the results show about sugar?", "Warmer water can dissolve more sugar.", ["Warmer water dissolves less sugar.", "Temperature makes no difference.", "Sugar only dissolves at 80 °C."], "The numbers go up.")


def g_mass():
    w = R.choice([100, 150, 200, 250, 300])
    s = R.choice([5, 10, 15, 20, 25, 30])
    if not once(("ms", w, s)):
        return None
    g = "%d g" % (w + s)
    thing = R.choice(["salt", "sugar"])
    return item("%d g of water and %d g of %s are mixed until all the %s dissolves. What is the mass of the solution?" % (w, s, thing, thing), g,
                uniq(g, ["%d g" % w, "%d g" % (w - s), "%d g" % s, "%d g" % (w + 2 * s)]), "Dissolving does not destroy anything: %d + %d = %d g." % (w, s, w + s))


B1 = bank([
    ("What is a solution?", "a liquid with a substance dissolved in it, such as salty water", ["a mixture of sand and water", "a frozen liquid", "a type of gas"], "You cannot see the dissolved substance."),
    ("In salty water, what is the solute?", "the salt", ["the water", "the cup", "the spoon"], "The solute is what dissolves."),
    ("In salty water, what is the solvent?", "the water", ["the salt", "the air", "the sand"], "The solvent does the dissolving."),
    ("When sugar dissolves in tea, where does it go?", "It breaks into tiny pieces spread through the tea; it is still there.", ["It disappears completely.", "It turns into water.", "It sinks as sugar lumps."], "You can still taste it."),
    ("Is dissolving the same as melting?", "No. Dissolving needs a liquid; melting needs heat.", ["Yes, they are the same.", "Yes, but only for ice.", "No, melting needs a liquid."], "Sugar dissolves in tea; butter melts in a pan."),
    ("What is a saturated solution?", "a solution in which no more solid can dissolve", ["a solution with nothing dissolved", "a frozen solution", "any cold drink"], "Extra solid sinks to the bottom."),
    ("How can you get salt back from salty water?", "by evaporating the water", ["by filtering it", "by using a magnet", "by sieving it"], "The salt is left behind."),
    ("Which of these makes sugar dissolve faster?", "using warmer water", ["using colder water", "using bigger lumps", "not stirring"], "Heat speeds up dissolving."),
])
B5 = bank([
    ("How could you show that dissolved salt is still in the water?", "Evaporate the water and see the salt left behind.", ["Look at the clear water.", "Filter it.", "Freeze it."], "Evidence it is still there."),
    ("Why do sugar cubes dissolve more slowly than caster sugar?", "Cubes have less surface touching the water.", ["Cubes are not sugar.", "Caster sugar is warmer.", "Cubes are insoluble."], "Smaller pieces, more surface."),
    ("In a dissolving test, why use the same amount of water each time?", "so the only variable changed is the one being tested", ["to make it quicker", "because water is expensive", "it does not matter"], "Fair test."),
    ("A pupil says salt 'disappears' in water. How could you weigh to show it does not?", "Weigh the water and salt before and after mixing: the total mass stays the same.", ["Weigh only the salt afterwards.", "Weigh the empty cup.", "Weigh the spoon."], "Mass is conserved."),
    ("Why does hot chocolate powder dissolve better in hot milk than cold milk?", "Warmer liquids dissolve solids faster and can hold more.", ["Cold milk is insoluble.", "Hot milk is thicker.", "Powder only melts."], "Temperature."),
])


def body():
    think = ("<p><b>Soluble materials dissolve to make a solution; insoluble ones do not.</b></p>"
             "<ul><li>Solute (what dissolves) + solvent (the liquid) = solution. The solute is still there, just in tiny pieces.</li>"
             "<li>Warmer water, stirring and smaller pieces make dissolving faster. A saturated solution can dissolve no more.</li>"
             "<li>Mass is kept: 100 g water + 10 g salt = 110 g. Evaporating the water gets the solid back.</li></ul>")
    ex = [("200 g water + 15 g sugar. Mass of solution?", ["Nothing is lost"], "215 g"),
          ("Sugar cube or caster sugar: faster?", ["Smaller pieces dissolve faster"], "caster sugar")]
    mist = ["Thinking dissolved sugar has disappeared.", "Confusing dissolving with melting.", "Thinking mass goes down when something dissolves."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Soluble or insoluble?", B1 + [(g_sol, 8), (g_pick, 4)]),
        ("Solutions", [(g_sol, 8), (g_pick, 6), (g_mass, 6)]),
        ("Dissolving faster", [(g_rate, 20)]),
        ("How much dissolves", [(g_sat, 14), (g_mass, 6)]),
        ("Investigating dissolving", B5 + [(g_rate, 8), (g_sat, 4), (g_mass, 3)]),
    ])
    make_uk(5, "dissolving-and-solutions", 5, "Properties and changes of materials",
            "Know that some materials will dissolve in liquid to form a solution, and describe how to recover a substance from a solution.",
            "Dissolving and Solutions",
            "Year 5 Science: Dissolving and Solutions Worksheets (Soluble, Insoluble, Saturated)",
            "Dissolving",
            "Free Year 5 science worksheets on dissolving: soluble and insoluble materials, solute, solvent and solution, what speeds up dissolving, saturated solutions and conservation of mass. 100 questions with answers.",
            "Dissolved does not mean gone.",
            "The solute spreads through the solvent; heat, stirring and small pieces speed it up.",
            body(),
            [("What happens when something dissolves?", "It breaks into pieces too small to see and spreads through the liquid. It is still there: you can taste it and get it back by evaporating the water."),
             ("How can you make sugar dissolve faster?", "Use warmer water, stir it, or use smaller pieces such as caster sugar instead of sugar cubes."),
             ("Does mass change when something dissolves?", "No. The mass of the solution equals the mass of the water plus the mass of the solid that dissolved.")],
            sets)


if __name__ == "__main__":
    main()
