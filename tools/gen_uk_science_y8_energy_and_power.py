# -*- coding: utf-8 -*-
"""
UK Year 8 science (KS3 Physics): Energy and Power
  python tools/gen_uk_science_y8_energy_and_power.py
Energy stores and transfers, conservation and dissipation of energy, efficiency, power ratings of appliances (W and kW),
energy transferred in kilowatt-hours, the cost of using appliances at home, and renewable and non-renewable energy
resources. Reuses the energy-budget, bounce and transfer questions of the US Grade 8 units in British English.
Wrong answers come from real mistakes: "energy is used up", "a kettle with a higher power uses less energy",
"kWh is a unit of power", "efficiency can be over 100%".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us
from sci_phys import uniq

U = Unit(61813)
R = U.R
P = People(R)
uk_sci.USED.clear()
ET = adopt_us("gen_us_science_g8_energy_transfer_and_motion", U)
us_budget, us_bounce, us_dir = ukm(ET.g_budget), ukm(ET.g_bounce), ukm(ET.g_dir)

APP = [("a kettle", 3), ("an electric oven", 2), ("a hairdryer", 2), ("an electric heater", 3), ("a microwave oven", 1), ("a toaster", 1), ("an iron", 2), ("a washing machine", 2)]
SMALL = [("an LED bulb", 10), ("a laptop", 50), ("a television", 100), ("a games console", 150), ("a phone charger", 5), ("a fridge", 150)]


def money(c):
    return "£%.2f" % (c / 100) if c >= 100 else "%sp" % "{:g}".format(c)


def g_kwh():
    a, p = R.choice(APP)
    t = R.choice([0.25, 0.5, 1, 1.5, 2, 3])
    price = R.choice([24, 25, 26, 28, 30])
    k = R.choice(["kwh", "cost"])
    if not once(("kw", a, t, k)):
        return None
    e = p * t
    ts = "%s hours" % ("{:g}".format(t)) if t != 1 else "1 hour"
    if k == "kwh":
        g = "%s kWh" % "{:g}".format(e)
        return item("%s has a power of %d kW and is used for %s. How much energy does it transfer?" % (a[0].upper() + a[1:], p, ts), g,
                    uniq(g, ["%s kWh" % "{:g}".format(p + t), "%s kWh" % "{:g}".format(p / t), "%d kWh" % p, "%s kWh" % "{:g}".format(e * 10)]), "Energy (kWh) = power (kW) × time (h) = %d × %s." % (p, "{:g}".format(t)))
    c = e * price
    g = money(c)
    return item("%s (%d kW) is used for %s. Electricity costs %dp per kWh. How much does this cost?" % (a[0].upper() + a[1:], p, ts, price), g,
                uniq(g, [money(p * price), money(e + price), money(price), money(c * 10)]), "%s kWh × %dp = %sp%s." % ("{:g}".format(e), price, "{:g}".format(c), " = " + g if c >= 100 else ""))


def g_watt():
    a, w = R.choice(SMALL)
    k = R.choice(["kw", "j", "cmp"])
    if not once(("wa", a, k)):
        return None
    if k == "kw":
        g = "%s kW" % "{:g}".format(w / 1000)
        return item("%s has a power of %d W. What is this in kilowatts?" % (a[0].upper() + a[1:], w), g,
                    uniq(g, ["%s kW" % "{:g}".format(w / 100), "{:,} kW".format(w * 1000), "%d kW" % w, "%s kW" % "{:g}".format(w / 10)]), "1 kW = 1,000 W, so divide by 1,000.")
    if k == "j":
        s = R.choice([10, 30, 60])
        g = "{:,} J".format(w * s)
        return item("%s (%d W) is on for %d seconds. How much energy does it transfer? (1 W = 1 J per second)" % (a[0].upper() + a[1:], w, s), g,
                    uniq(g, ["{:,} J".format(w + s), "{:,} J".format(w), "{:,} J".format(w * s * 10), "%s J" % "{:g}".format(w / s)]), "Energy = power × time = %d × %d." % (w, s))
    b, w2 = R.choice([x for x in APP])
    return item("Which transfers more energy in one hour: %s (%d W) or %s (%d kW)?" % (a, w, b, w2), b, [a, "They transfer the same.", "Neither transfers energy."],
                "%d kW = {:,} W, which is bigger.".format(w2 * 1000) % w2)


STORE = [("a stretched elastic band", "elastic potential"), ("a book on a high shelf", "gravitational potential"), ("a moving car", "kinetic"), ("a battery", "chemical"),
         ("a hot cup of tea", "thermal"), ("food", "chemical"), ("a compressed spring", "elastic potential"), ("a rollercoaster at the top of a hill", "gravitational potential"),
         ("a running athlete", "kinetic"), ("petrol in a car's tank", "chemical")]


def g_store():
    o, s = R.choice(STORE)
    if not once(("so", o)):
        return None
    return item("Which energy store is mainly filled in %s?" % o, "the %s store" % s, ["the %s store" % x for x in R.sample(sorted({y[1] for y in STORE if y[1] != s}), 3)], "Stores: kinetic, gravitational potential, elastic potential, chemical, thermal.")


def g_eff():
    tot = R.choice([100, 200, 400, 500, 1000, 2000])
    pct = R.choice([10, 20, 25, 40, 50, 60, 75, 80, 90])
    use = tot * pct // 100
    k = R.choice(["pct", "waste"])
    if not once(("ef", tot, pct, k)):
        return None
    if k == "pct":
        g = "%d%%" % pct
        return item("A device is supplied with {:,} J of energy and transfers {:,} J usefully. What is its efficiency?".format(tot, use), g,
                    uniq(g, ["%d%%" % (100 - pct), "{:,}%".format(tot // max(use, 1)), "{:,}%".format(use), "%d%%" % min(99, pct + 10)]), "useful ÷ total × 100 = %d%%." % pct)
    g = "{:,} J".format(tot - use)
    return item("A motor is supplied with {:,} J and transfers {:,} J usefully. How much energy is wasted?".format(tot, use), g,
                uniq(g, ["{:,} J".format(use), "{:,} J".format(tot), "{:,} J".format(tot + use), "0 J"]), "Energy is conserved: wasted = total − useful.")


RES = [("wind", True), ("solar", True), ("hydroelectric", True), ("tidal", True), ("geothermal", True), ("biomass (wood from managed forests)", True),
       ("coal", False), ("oil", False), ("natural gas", False), ("nuclear (uranium)", False)]


def g_res():
    r, ren = R.choice(RES)
    if not once(("re", r)):
        return None
    a = "renewable" if ren else "non-renewable"
    return item("Is %s energy renewable or non-renewable?" % r, a, ["renewable" if not ren else "non-renewable", "neither", "both"], "Renewable resources will not run out.")


B1 = bank([
    ("Can energy be created or destroyed?", "No. It can only be transferred from one store to another.", ["Yes, power stations create it.", "Yes, it is used up.", "Only in batteries."], "Conservation of energy."),
    ("What does dissipated energy mean?", "energy that spreads out to the surroundings, usually as heat, and is not useful", ["energy that is destroyed", "energy stored in food", "energy that is created"], "Wasted."),
    ("What is power?", "how quickly energy is transferred", ["how much energy there is", "the cost of electricity", "the size of a device"], "Measured in watts."),
    ("What is the unit of power?", "the watt (W)", ["the joule (J)", "the kilowatt-hour (kWh)", "the newton (N)"], "1 W = 1 J/s."),
    ("What does a kilowatt-hour measure?", "energy", ["power", "time", "current"], "Used on electricity bills."),
])
B5 = bank([
    ("Why can no device be 100% efficient?", "Some energy is always dissipated, for example as heat or sound.", ["Energy is destroyed.", "Devices create energy.", "It can be if it is new."], "Waste is unavoidable."),
    ("How can a home reduce heat loss?", "loft insulation, double glazing and draught excluders", ["opening windows in winter", "removing the roof", "painting walls white inside"], "Lower bills."),
    ("Why are LED bulbs cheaper to run than filament bulbs?", "They have a lower power and waste less energy as heat.", ["They are brighter so use more energy.", "They need no electricity.", "They are made of gold."], "Efficiency."),
    ("What is one disadvantage of wind power?", "It does not work when there is no wind.", ["It produces carbon dioxide.", "It will run out.", "It needs coal."], "Reliability."),
    ("Why do fossil fuel power stations add to climate change?", "Burning the fuel releases carbon dioxide.", ["They release oxygen.", "They cool the air.", "They use sunlight."], "Greenhouse gas."),
])


def body():
    think = ("<p><b>Energy is never used up; it is transferred between stores.</b></p>"
             "<ul><li>Stores: kinetic, gravitational potential, elastic potential, chemical, thermal. Some energy is always dissipated as heat.</li>"
             "<li>Power is how fast energy is transferred (watts). Energy (kWh) = power (kW) × time (h); cost = kWh × price.</li>"
             "<li>Efficiency = useful energy ÷ total energy × 100%.</li></ul>")
    ex = [("2 kW heater for 3 hours?", ["2 × 3"], "6 kWh"),
          ("6 kWh at 25p per kWh?", ["6 × 25"], "150p (£1.50)")]
    mist = ["Saying energy is used up.", "Thinking kWh is a unit of power.", "Thinking a device can be more than 100% efficient."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy stores", B1[:2] + [(g_store, 9), (us_dir, 5), (us_bounce, 4)]),
        ("Conservation and efficiency", [(g_eff, 12), (us_budget, 8)]),
        ("Power", B1[2:] + [(g_watt, 12), (g_kwh, 5)]),
        ("Paying for energy", [(g_kwh, 16), (g_watt, 4)]),
        ("Energy resources", B5 + [(g_res, 9), (g_eff, 4), (us_budget, 2)]),
    ])
    make_ks3(8, "energy-and-power", 13, "Physics", "Energy",
             "Calculation of fuel uses and costs in the domestic context: comparing energy values of different foods (from labels) (kJ); comparing power ratings of appliances in watts (W, kW); comparing amounts of energy transferred (J, kJ, kW hour); domestic fuel bills, fuel use and costs; fuels and energy resources. Energy changes and transfers: simple machines give bigger force but at the expense of smaller movement; heating and thermal equilibrium; other processes that involve energy transfer. Changes in systems: energy as a quantity that can be quantified and calculated; the total energy has the same value before and after a change.",
             "Energy and Power",
             "Year 8 Science: Energy and Power Worksheets (Stores, Efficiency, kWh and Costs)",
             "Energy and Power",
             "Free Year 8 science worksheets on energy and power: energy stores, conservation, efficiency, watts and kilowatts, kilowatt-hours, the cost of electricity and energy resources. 100 questions with answers.",
             "Energy (kWh) = power (kW) × time (h).",
             "Energy is conserved; some is always dissipated as heat.",
             body(),
             [("How do you work out the cost of using an appliance?", "Multiply its power in kilowatts by the time in hours to get kilowatt-hours, then multiply by the price per kWh."),
              ("What is efficiency?", "The fraction of the energy supplied that is transferred usefully: useful energy ÷ total energy × 100%."),
              ("What is the difference between power and energy?", "Energy is measured in joules or kilowatt-hours. Power is how fast energy is transferred, measured in watts.")],
             sets)


if __name__ == "__main__":
    main()
