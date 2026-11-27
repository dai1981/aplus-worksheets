# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U05: the law of conservation of energy applied to systems - energy inputs, useful
outputs and wasted energy, Sankey diagrams, efficiency calculations, power, and ways to reduce energy waste.
  python tools/gen_au_science_y9_conservation_of_energy_and_efficiency.py
Reuses the US Physics conservation of energy and energy conversion and efficiency makers and the UK Year 10 energy makers with
Australian names, plus own Sankey diagrams and Australian contexts (coal and solar power, Snowy 2.0, home energy ratings).
Wrong answers come from real mistakes: adding useful and wasted energy to more than the input, giving efficiency over 100%,
and thinking wasted energy is destroyed.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once

YEAR, SORT = 9, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

CE = "gen_us_science_phys_conservation_of_energy"
EF = "gen_us_science_phys_energy_conversion_and_efficiency"
K10 = "gen_uk_science_y10_energy"
c_coast = limit(src(CE, "g_coast"), 4)
c_drop = limit(src(CE, "g_drop"), 4)
c_loss = limit(src(CE, "g_loss"), 5)
c_table = limit(src(CE, "g_table"), 4)
c_b1 = src.B(CE, "B1")
c_b5 = src.B(CE, "B5")
e_conv = limit(src(EF, "g_conv"), 6)
e_eff = limit(src(EF, "g_eff"), 6)
e_power = limit(src(EF, "g_power", drop=["Ω", "Ohm", "resistance"]), 4)
e_elec = limit(src(EF, "g_elec", drop=["Ω", "Ohm", "resistance"]), 4)
e_b1 = src.B(EF, "B1", drop=["Ω", "Ohm"])
e_b5 = src.B(EF, "B5")
k_pow = limit(src(K10, "g_pow"), 4)

DEV = [("an LED globe", "electrical", "light", "heat"), ("a filament globe", "electrical", "light", "heat"),
       ("an electric kettle", "electrical", "thermal energy in the water", "heat to the air and sound"),
       ("a car engine", "chemical (petrol)", "kinetic", "heat and sound"), ("a solar panel", "light", "electrical", "heat"),
       ("an electric motor", "electrical", "kinetic", "heat and sound"), ("a coal-fired power station", "chemical (coal)", "electrical", "heat to the air and water"),
       ("a wind turbine", "kinetic (wind)", "electrical", "heat and sound"), ("a hair dryer", "electrical", "thermal and kinetic (warm air)", "sound")]
EFF = {"an LED globe": [80, 90], "a filament globe": [5, 10], "an electric kettle": [80, 90], "a car engine": [20, 25, 30],
       "a solar panel": [15, 20, 22], "an electric motor": [70, 80, 85], "a coal-fired power station": [30, 35, 40],
       "a wind turbine": [35, 40, 45], "a hair dryer": [85, 90]}


def sankey(inp, use, waste, a, b, c):
    wu = max(8, 220 * use // inp)
    ww = 220 - wu
    return ("<svg viewBox='0 0 520 270' width='520' role='img' aria-label='Sankey diagram'>"
            "<rect x='20' y='20' width='160' height='220' fill='#f6b26b'/>"
            "<text x='100' y='130' text-anchor='middle' font-size='15'>%s</text><text x='100' y='150' text-anchor='middle' font-size='15' font-weight='bold'>%d J</text>"
            "<path d='M180 20 L330 20 L330 %d L180 %d Z' fill='#93c47d'/>"
            "<rect x='330' y='20' width='170' height='%d' fill='#93c47d'/>"
            "<text x='415' y='%d' text-anchor='middle' font-size='14'>useful: %s</text>"
            "<path d='M180 %d L250 %d L250 262 L330 262 L330 %d L180 240 Z' fill='#cccccc'/>"
            "<text x='410' y='%d' text-anchor='middle' font-size='14'>wasted: %s</text></svg>" %
            (a, inp, 20 + wu, 20 + wu, wu, 20 + wu // 2 + 5, b, 20 + wu, 20 + wu, 20 + wu + 4, 20 + wu + ww // 2 + 8, c))


def g_sankey():
    d, i, o, w = R.choice(DEV)
    e = R.choice(EFF[d])
    inp = R.choice([200, 400, 500, 1000, 2000])
    use = inp * e // 100
    waste = inp - use
    k = R.choice(["eff", "waste", "use"])
    if not once(("sk", d, inp, e, k)):
        return None
    if k == "eff":
        svg = sankey(inp, use, waste, i, "%s %d J" % (o, use), "%s ?" % w)
        return tq("%s<br>This Sankey diagram is for %s. What is its efficiency?" % (svg, d), "%d%%" % e,
                  ["%d%%" % (100 - e), "%d%%" % (use * 100 // waste if waste else 0 + 1), "%d%%" % min(99, e + 10)],
                  "Efficiency = useful ÷ input × 100 = %d ÷ %d × 100 = %d%%." % (use, inp, e))
    if k == "waste":
        svg = sankey(inp, use, waste, i, "%s %d J" % (o, use), "%s ? J" % w)
        return tq("%s<br>This Sankey diagram is for %s. How much energy is wasted?" % (svg, d), "%d J" % waste,
                  ["%d J" % (inp + use), "%d J" % use, "%d J" % inp], "Energy is conserved: wasted = %d − %d = %d J." % (inp, use, waste))
    svg = sankey(inp, use, waste, i, "%s ? J" % o, "%s %d J" % (w, waste))
    return tq("%s<br>This Sankey diagram is for %s. How much useful energy does it give out?" % (svg, d), "%d J" % use,
              ["%d J" % (inp + waste), "%d J" % waste, "%d J" % inp], "Useful = input − wasted = %d − %d = %d J." % (inp, waste, use))


def g_dev():
    d, i, o, w = R.choice(DEV)
    k = R.choice(["in", "out"])
    if not once(("dv", d, k)):
        return None
    if k == "in":
        ans, others = i, [x[1] for x in DEV if x[1] != i]
        q = "What is the main energy input for %s?" % d
    elif k == "out":
        ans, others = o, [x[2] for x in DEV if x[2] != o]
        q = "What is the useful energy output of %s?" % d
    else:
        ans, others = w, [x[3] for x in DEV if x[3] != w]
        q = "Where does most of the wasted energy from %s go?" % d
    others = sorted(set(others) - {ans, i, o})
    if len(others) < 3:
        return None
    return tq(q, ans, R.sample(others, 3), "%s: %s in → %s (useful) + %s (wasted)." % (d[0].upper() + d[1:], i, o, w))


POOL1 = pool(R, [
    ("What does the law of conservation of energy say?", "Energy cannot be created or destroyed, only transferred or transformed.", ["Energy is used up in machines.", "Wasted energy disappears.", "Machines can make energy."], "Input = useful output + wasted energy."),
    ("A device takes in 500 J. Which pair of outputs is possible?", "400 J useful and 100 J wasted", ["400 J useful and 200 J wasted", "600 J useful and 0 J wasted", "500 J useful and 100 J wasted"], "Outputs must add to the input."),
    ("Can a machine be more than 100% efficient?", "No, it would have to create energy.", ["Yes, if it is new.", "Yes, solar panels are.", "Only at night."], "Some energy is always wasted."),
    ("Why do LED globes have a higher efficiency than filament globes?", "They waste much less energy as heat.", ["They make more heat.", "They use no electricity.", "They create energy."], "LEDs are about 80–90% efficient."),
    ("What is wasted energy usually transferred as?", "heat to the surroundings, and sometimes sound", ["light only", "chemical energy", "nothing; it is destroyed"], "Friction and resistance cause heating."),
    ("What does a Sankey diagram show?", "how the input energy splits into useful and wasted energy", ["the speed of a car", "the mass of an object", "only the useful energy"], "Arrow widths are in proportion to the energy."),
    ("How does adding insulation to a ceiling improve a home's energy efficiency?", "It reduces heat transfer, so less energy is needed for heating and cooling.", ["It makes heat.", "It increases heat loss.", "It stops electricity."], "Australian homes get star ratings for energy efficiency."),
    ("Snowy 2.0 pumps water uphill when electricity is cheap and releases it later. Why is it not 100% efficient?", "Some energy is lost as heat and sound in the pumps, pipes and turbines.", ["Water creates energy.", "Gravity disappears.", "It is 100% efficient."], "Pumped hydro stores energy as gravitational potential energy."),
    ("Which is the efficiency formula?", "efficiency = useful energy out ÷ total energy in × 100%", ["efficiency = energy in ÷ energy out", "efficiency = wasted ÷ useful", "efficiency = power × time"], "It can also be calculated with power."),
    ("Why does oiling a bike chain increase its efficiency?", "It reduces friction, so less energy is wasted as heat.", ["It adds energy.", "It makes the bike heavier.", "Oil stores kinetic energy."], "Less friction means more useful output."),
])
POOL5 = pool(R, [
    ("Mia measures a kettle using 180 000 J to heat water that gains 150 000 J. What is its efficiency?", "about 83%", ["about 120%", "about 17%", "150%"], "150 000 ÷ 180 000 × 100 ≈ 83%."),
    ("Jack compares how long a bouncing ball keeps bouncing on carpet, wood and concrete. Which variable must he control?", "the drop height and the ball", ["the floor surface", "the number of bounces", "nothing"], "Only the surface should change."),
    ("Ruby drops a ball from 2.0 m and it bounces to 1.5 m. What percentage of its gravitational potential energy is kept?", "75%", ["25%", "150%", "50%"], "Energy is proportional to height: 1.5 ÷ 2.0 = 0.75."),
    ("Kai tests insulated and uninsulated cups of hot water. After 20 min, the insulated cup is 15 °C warmer. What does this show?", "Insulation reduces heat transfer to the surroundings.", ["Insulation adds heat.", "Both cups lost the same energy.", "Heat was destroyed in the plain cup."], "Less energy is wasted."),
    ("Ella's model car rolls down a ramp. At the bottom it has less kinetic energy than the potential energy it had at the top. Where did the rest go?", "heat and sound from friction and air resistance", ["it was destroyed", "it stayed at the top", "it turned into mass"], "Energy is conserved but some is dissipated."),
    ("Noah compares two fridges: one with a 3-star and one with a 6-star energy rating. Which uses less electricity for the same job?", "the 6-star fridge", ["the 3-star fridge", "they use the same", "it cannot be known"], "More stars means more efficient."),
    ("A solar panel receives 1000 J of light energy and gives 200 J of electrical energy. What is its efficiency?", "20%", ["80%", "200%", "5%"], "200 ÷ 1000 × 100 = 20%."),
    ("A data logger shows a pendulum swing getting lower each time. What does this show?", "Energy is gradually transferred to the surroundings.", ["Energy is created each swing.", "Gravity is getting stronger.", "Nothing is happening."], "Air resistance and friction dissipate energy."),
])


def main():
    sets = U.sets([
        ("Conservation of energy", [(POOL1, 5), (c_b1, 4), (c_loss, 4), (e_conv, 4), (c_drop, 3)]),
        ("Energy inputs and outputs", [(g_dev, 10), (e_conv, 2), (e_b1, 4), (POOL1, 2), (c_coast, 2)]),
        ("Sankey diagrams", [(g_sankey, 12), (POOL1, 3), (e_eff, 3), (c_table, 2)]),
        ("Efficiency and power", [(e_eff, 3), (e_power, 4), (k_pow, 4), (e_elec, 3), (g_sankey, 3), (c_table, 2), (c_coast, 1)]),
        ("Investigations", [(POOL5, 8), (c_b5, 4), (e_b5, 4), (c_loss, 1), (c_drop, 1), (g_dev, 2)]),
    ])
    make_au(YEAR, "conservation-of-energy-and-efficiency", SORT, "AC9S9U05", "Physical sciences",
            "Apply the law of conservation of energy to analyse system efficiency in terms of energy inputs, outputs, transfers and "
            "transformations (summary of the Australian Curriculum v9.0 Science content description).",
            "Conservation of Energy and Efficiency", "Energy efficiency",
            "Free Year 9 science worksheets on conservation of energy and efficiency: energy inputs and outputs, Sankey diagrams, "
            "efficiency and power calculations, and reducing energy waste. 100 questions with answers.",
            "Energy in = useful out + wasted.", "Efficiency = useful energy out ÷ energy in × 100%, and it is always less than 100%.",
            "<p><b>Energy is conserved in every system.</b></p><ul>"
            "<li>Total energy in = useful energy out + wasted energy. Wasted energy is usually heat and sound, not destroyed.</li>"
            "<li>Efficiency = useful energy out ÷ total energy in × 100%. No real device reaches 100%.</li>"
            "<li>A Sankey diagram shows the split: the width of each arrow is in proportion to the energy.</li></ul>",
            [("1000 J in, 250 J useful. Wasted? Efficiency?", ["1000 − 250 = 750 J", "250 ÷ 1000 × 100"], "750 J wasted, 25%"),
             ("A car engine: input? useful? wasted?", ["chemical energy in petrol"], "kinetic useful; heat and sound wasted")],
            ["Giving useful + wasted energy that adds to more than the input.", "Calculating an efficiency over 100%.",
             "Saying wasted energy is 'destroyed' or 'used up'."],
            [("What is a Sankey diagram?", "A flow diagram that shows how input energy splits into useful and wasted outputs. The arrow widths are drawn in proportion to the amounts of energy."),
             ("Why is no machine 100% efficient?", "Friction, electrical resistance and sound always transfer some energy to the surroundings as heat or sound."),
             ("How can energy efficiency be improved?", "Reduce friction with lubrication, insulate to reduce heat loss, and choose efficient devices such as LED globes and high star-rated appliances.")],
            sets)


if __name__ == "__main__":
    main()
