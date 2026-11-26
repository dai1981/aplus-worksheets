# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Pressure
  python tools/gen_uk_science_y9_pressure.py
Pressure as force over area (pressure = force ÷ area, N/m² or pascals, and N/cm²), everyday applications (sharp knives,
snowshoes, drawing pins, tractor tyres), atmospheric pressure decreasing with height, pressure in liquids increasing
with depth, upthrust and floating and sinking, and gas pressure explained by particles colliding with the walls.
Wrong answers come from real mistakes: "a bigger area gives a bigger pressure", "pressure is the same as force",
"heavy things always sink", "air pressure increases as you climb".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61908)
R = U.R
P = People(R)
uk_sci.USED.clear()


def f(x):
    x = round(x, 2)
    return "{:,}".format(int(x)) if x == int(x) else "{:,}".format(x)


OBJ = ["a box", "a crate", "a block of wood", "an elephant's foot", "a person standing on one foot", "a car tyre", "a wardrobe", "a statue"]


def g_calc():
    o = R.choice(OBJ)
    k = R.choice(["p", "f", "a"])
    unit = R.choice(["m²", "cm²"])
    if unit == "m²":
        a = R.choice([0.5, 1, 2, 4, 5, 0.25])
        p = R.choice([100, 200, 400, 500, 1000, 2000])
        pu = "N/m²"
    else:
        a = R.choice([2, 4, 5, 10, 20, 25, 50])
        p = R.choice([2, 4, 5, 10, 20, 50])
        pu = "N/cm²"
    fo = p * a
    if fo != int(fo) or not once(("ca", o, k, a, p)):
        return None
    if k == "p":
        g = "%s %s" % (f(p), pu)
        return item("%s pushes down with a force of %s N on an area of %s %s. What pressure does it exert?" % (o[0].upper() + o[1:], f(fo), f(a), unit), g,
                    uniq(g, ["%s %s" % (f(fo * a), pu), "%s %s" % (f(fo + a), pu), "%s %s" % (f(fo), pu), "%s %s" % (f(round(a / fo, 3)), pu) if a / fo >= 0.01 else "%s %s" % (f(p * 2), pu)]),
                    "pressure = force ÷ area = %s ÷ %s = %s %s." % (f(fo), f(a), f(p), pu))
    if k == "f":
        g = "%s N" % f(fo)
        return item("%s exerts a pressure of %s %s on an area of %s %s. What is the force?" % (o[0].upper() + o[1:], f(p), pu, f(a), unit), g,
                    uniq(g, ["%s N" % f(p / a), "%s N" % f(p + a), "%s N" % f(p), "%s N" % f(fo * 10)]), "force = pressure × area = %s × %s." % (f(p), f(a)))
    g = "%s %s" % (f(a), unit)
    return item("A force of %s N gives a pressure of %s %s. What is the area?" % (f(fo), f(p), pu), g,
                uniq(g, ["%s %s" % (f(fo * p), unit), "%s %s" % (f(fo - p), unit) if fo > p else "%s %s" % (f(a * 2), unit), "%s %s" % (f(p), unit), "%s %s" % (f(a * 10), unit)]), "area = force ÷ pressure = %s ÷ %s." % (f(fo), f(p)))


EX = [("Why does a sharp knife cut better than a blunt one?", "The small area of the blade gives a large pressure.", ["The sharp knife is heavier.", "A large area gives a large pressure.", "Sharpness reduces the force."]),
      ("Why do snowshoes stop you sinking into snow?", "They spread your weight over a large area, so the pressure is lower.", ["They make you lighter.", "They increase the pressure.", "They melt the snow."]),
      ("Why does a drawing pin have a sharp point and a wide head?", "The point gives a high pressure on the board; the head gives a low pressure on your thumb.", ["Both ends give the same pressure.", "The head is for decoration.", "The point reduces the force."]),
      ("Why do tractors have wide tyres?", "To spread the weight and reduce the pressure on soft ground.", ["To go faster.", "To increase the pressure.", "To make them heavier."]),
      ("Why does a camel have wide feet?", "They spread its weight so it does not sink into sand.", ["They help it swim.", "They store water.", "They increase pressure."]),
      ("Why do high heels damage some floors more than flat shoes?", "The small heel area gives a much larger pressure.", ["High heels are heavier.", "Flat shoes have a smaller area.", "Pressure does not depend on area."]),
      ("Why is it easier to push a nail into wood point first?", "The small area of the point gives a high pressure.", ["The head is sharper.", "Wood is softer at the point.", "Force is bigger at the point."]),
      ("Why do caterpillar tracks help heavy tanks cross mud?", "The tracks have a large area, so the pressure on the ground is low.", ["They make the tank lighter.", "They grip by increasing pressure.", "Mud is hard."])]


def g_ex():
    q, a, w = R.choice(EX)
    if not once(("ex", q)):
        return None
    return item(q, a, w, "Same force: smaller area → bigger pressure; bigger area → smaller pressure.")


def g_depth():
    who = P.next()[0]
    d = [1, 2, 3, 4]
    per = R.choice([10, 10, 10])
    base = 100
    vals = [base + per * x for x in d]
    k = R.choice(["pattern", "why", "dam", "pred", "diff"])
    if not once(("de", k)):
        return None
    tab = table(["Depth of water (m)", "Pressure (kPa)"], [[str(a), str(b)] for a, b in zip(d, vals)])
    intro = tab + "%s measured the pressure at different depths in a swimming pool. " % who
    if k == "pattern":
        return item(intro + "What does the data show?", "The deeper you go, the greater the pressure.", ["Pressure falls with depth.", "Depth has no effect.", "Pressure is zero underwater."], "More water above pushes down.")
    if k == "why":
        return item(intro + "Why does pressure increase with depth?", "There is more weight of water above pushing down.", ["Water gets lighter deeper down.", "Fish push the water.", "Air pressure increases underwater."], "Weight of the liquid.")
    if k == "dam":
        return item("Why is a dam wall built thicker at the bottom than at the top?", "Water pressure is greatest at the bottom.", ["Water pressure is greatest at the top.", "It looks better.", "Fish need the space."], "Pressure increases with depth.")
    if k == "pred":
        return item(intro + "What would you predict the pressure to be at 5 m?", "%d kPa" % (base + per * 5), ["%d kPa" % vals[3], "%d kPa" % (base + per * 4 - 5), "%d kPa" % (base * 5)], "It rises by %d kPa each metre." % per)
    return item(intro + "By how much does the pressure rise for each extra metre of depth?", "%d kPa" % per, ["%d kPa" % base, "%d kPa" % vals[0], "%d kPa" % (per * 4)], "%d − %d = %d." % (vals[1], vals[0], per))


FLOAT = [("a wooden block", "floats", "Its weight is balanced by the upthrust before it is fully under the water."), ("a steel ball", "sinks", "Its weight is bigger than the upthrust it gets."),
         ("a steel ship", "floats", "Its shape pushes aside a lot of water, so the upthrust equals its weight."), ("a cork", "floats", "It is less dense than water."),
         ("a stone", "sinks", "It is denser than water, so the upthrust is less than its weight."), ("an ice cube", "floats", "Ice is slightly less dense than water.")]


def g_float():
    o, a, e = R.choice(FLOAT)
    k = R.random() < 0.5
    if not once(("fl", o, k)):
        return None
    if k:
        return item("Does %s float or sink in water?" % o, "It " + a + ".", ["It " + ("sinks" if a == "floats" else "floats") + ".", "It hovers halfway.", "It dissolves."], e)
    return item("What is upthrust?", "the upward push of a liquid or gas on an object in it", ["the weight of an object", "the force of friction", "the pressure of air only"], "Floating: upthrust = weight.") if once(("upth",)) else None


GAS = [("the gas is heated", "increases", "The particles move faster and hit the walls harder and more often."),
       ("the gas is cooled", "decreases", "The particles move more slowly and hit the walls less often."),
       ("the gas is squashed into a smaller volume", "increases", "The particles hit the walls more often."),
       ("the container is made bigger", "decreases", "The particles hit the walls less often."),
       ("more gas is pumped in", "increases", "More particles hit the walls each second."),
       ("some gas is let out", "decreases", "Fewer particles hit the walls each second.")]


def g_gas():
    c, a, e = R.choice(GAS)
    if not once(("ga", c)):
        return None
    return item("A gas is in a sealed container. What happens to its pressure if %s?" % c, "It %s." % a, ["It %s." % ("decreases" if a == "increases" else "increases"), "It stays the same.", "It becomes zero."], e)


LIQ = bank([
    ("Why do divers' ears hurt when they swim deep?", "The water pressure on the eardrum increases with depth.", ["The water gets warmer.", "Pressure falls with depth.", "Fish make noise."], "Depth."),
    ("Water spurts out of holes at different heights in a bottle. Which hole squirts furthest?", "the lowest hole", ["the highest hole", "the middle hole", "all the same"], "Greatest pressure at the bottom."),
    ("Why must submarines have very strong hulls?", "The water pressure deep in the ocean is enormous.", ["The water is too cold.", "Fish might bite.", "Air pressure is high underwater."], "Pressure with depth."),
    ("In which direction does pressure in a liquid act?", "in all directions", ["only downwards", "only upwards", "only sideways"], "Pressure acts normal to every surface."),
    ("Why does an object feel lighter in water?", "The upthrust from the water pushes up on it.", ["Water removes its mass.", "Gravity is weaker underwater.", "Water is magnetic."], "Apparent weight."),
    ("A ball weighs 5 N in air and 3 N in water. What is the upthrust?", "2 N", ["8 N", "3 N", "5 N"], "5 − 3 = 2 N."),
    ("A stone weighs 12 N in air and 7 N in water. What is the upthrust?", "5 N", ["19 N", "7 N", "12 N"], "12 − 7 = 5 N."),
    ("Why does a ship float higher in sea water than in fresh water?", "Sea water is denser, so it gives more upthrust for the same volume.", ["Sea water is lighter.", "Salt pushes ships down.", "Fresh water is denser."], "Density of liquid."),
])


B1 = bank([
    ("What is pressure?", "the force acting on each unit of area", ["the same as force", "the mass of an object", "the area of a surface"], "pressure = force ÷ area."),
    ("What is the unit of pressure?", "newtons per square metre (N/m²), also called pascals (Pa)", ["newtons (N)", "kilograms (kg)", "metres (m)"], "1 Pa = 1 N/m²."),
    ("If the same force acts on a smaller area, what happens to the pressure?", "It increases.", ["It decreases.", "It stays the same.", "It becomes zero."], "Inverse relationship."),
    ("What causes the pressure of a gas in a container?", "Particles colliding with the walls of the container", ["Particles staying still", "The colour of the gas", "The weight of the container"], "More collisions, more pressure."),
])
B5 = bank([
    ("What happens to air pressure as you climb a mountain?", "It decreases, because there is less air above you.", ["It increases.", "It stays the same.", "It becomes infinite."], "Thinner air."),
    ("Why do your ears 'pop' on an aeroplane?", "The air pressure outside changes faster than the pressure inside your ear.", ["The plane is noisy.", "Air pressure stays the same.", "Your ears are cold."], "Pressure difference."),
    ("Why does a sealed crisp packet swell at the top of a mountain?", "The outside air pressure is lower, so the air inside pushes the packet out.", ["The crisps expand.", "It gets hotter.", "The air inside increases."], "Lower atmospheric pressure."),
    ("Why does heating a gas in a sealed container increase its pressure?", "The particles move faster and hit the walls harder and more often.", ["The particles get bigger.", "More particles appear.", "The container shrinks."], "Particle model."),
    ("Why do weather forecasters measure air pressure?", "Falling pressure often means rain and wind; high pressure usually means settled weather.", ["Pressure has no link to weather.", "High pressure always means storms.", "To measure temperature."], "Barometers."),
    ("Why is it hard to pull a suction cup off a smooth window?", "The air pressure outside pushes it on, and there is little air behind it.", ["It is glued.", "Glass is magnetic.", "The window pulls it."], "Pressure difference."),
    ("Why do mountaineers sometimes carry oxygen?", "At high altitude the air pressure is low, so each breath contains less oxygen.", ["There is no air on mountains.", "Oxygen keeps them warm.", "To make them lighter."], "Thin air."),
    ("About what is atmospheric pressure at sea level?", "about 100,000 Pa (100 kPa)", ["about 10 Pa", "about 1 Pa", "about 100 Pa"], "The weight of the air above."),
    ("How does a drinking straw work?", "You lower the pressure in the straw and the air pressure outside pushes the drink up.", ["You suck the drink up with force.", "The drink is lighter.", "Water pressure pulls it."], "Atmospheric pressure."),
])


def body():
    think = ("<p><b>Pressure is how concentrated a force is.</b></p>"
             "<ul><li>pressure = force ÷ area (N/m² or Pa). Small area → big pressure; big area → small pressure.</li>"
             "<li>Pressure in a liquid increases with depth. Air pressure decreases with height.</li>"
             "<li>Upthrust is the upward push of a liquid or gas: an object floats when upthrust equals its weight.</li></ul>")
    ex = [("600 N on 2 m²?", ["600 ÷ 2"], "300 N/m²"),
          ("Snowshoes: pressure up or down?", ["Bigger area"], "down")]
    mist = ["Thinking a bigger area gives a bigger pressure.", "Thinking pressure is the same as force.", "Thinking air pressure increases as you climb."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is pressure?", B1 + [(g_calc, 10), (g_ex, 6)]),
        ("Calculating pressure", [(g_calc, 18), (g_ex, 2)]),
        ("Pressure in gases", [(g_gas, 6), (g_calc, 10), (g_depth, 1)] + B5[:3]),
        ("Liquids and floating", LIQ + [(g_depth, 4), (g_float, 6), (g_calc, 2)]),
        ("Air pressure", B5[3:] + [(g_calc, 12), (g_float, 1), (g_depth, 1)]),
    ])
    make_ks3(9, "pressure", 8, "Physics", "Pressure in fluids",
             "Atmospheric pressure, decreases with increase of height as weight of air above decreases with height; pressure in liquids, increasing with depth; upthrust effects, floating and sinking; pressure measured by ratio of force over area – acting normal to any surface.",
             "Pressure",
             "Year 9 Science: Pressure Worksheets (Pressure = Force ÷ Area, Liquids, Upthrust)",
             "Pressure",
             "Free Year 9 science worksheets on pressure: pressure = force ÷ area, everyday examples, pressure in liquids and gases, atmospheric pressure, upthrust and floating. 100 questions with answers.",
             "pressure = force ÷ area",
             "Smaller area means bigger pressure; liquid pressure rises with depth.",
             body(),
             [("How do you calculate pressure?", "Divide the force by the area: pressure = force ÷ area. With force in newtons and area in m², the answer is in N/m² (pascals)."),
              ("Why does pressure increase with depth in water?", "The deeper you go, the more water there is above you, and its weight pushes down harder."),
              ("Why do some objects float?", "The water pushes up with a force called upthrust. If the upthrust can balance the object's weight, it floats.")],
             sets)


if __name__ == "__main__":
    main()
