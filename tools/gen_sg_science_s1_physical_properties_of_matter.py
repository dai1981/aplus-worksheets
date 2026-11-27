# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Diversity): Exploring Diversity of Matter by its Physical Properties
  python tools/gen_sg_science_s1_physical_properties_of_matter.py
Physical properties (electrical and thermal conductivity, melting and boiling point, strength, hardness, flexibility, density),
classifying objects in more than one way, choosing materials from property data, measuring length, mass and volume,
volume by displacement, density = mass / volume (g/cm3, kg/m3) and predicting sinking and floating.
Wrong answers come from real mistakes: "density = volume / mass", "heavy objects always sink", "the displacement volume
is the final reading", "a material that is hard is also strong".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64102)
R = U.R
P = People(R)
PM = luse(U, "gen_uk_science_y7_particles_and_states_of_matter")
MA = luse(U, "gen_uk_science_y9_materials")


def n(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def g_dens():
    k = R.choice(["d", "m", "v"])
    d = R.choice([0.8, 0.9, 1.2, 2, 2.5, 2.7, 4, 7.9, 8.9, 11.3])
    v = R.choice([5, 10, 20, 25, 40, 50])
    m = d * v
    if not once(("dn", k, d, v)) or not once(("dk", k), 7):
        return None
    if k == "d":
        return item("A solid has a mass of %s g and a volume of %d cm³. What is its density?" % (n(m), v), "%s g/cm³" % n(d),
                    ["%s g/cm³" % n(v / m), "%s g/cm³" % n(m * v), "%s g/cm³" % n(m + v)], "Density = mass ÷ volume = %s ÷ %d = %s g/cm³." % (n(m), v, n(d)))
    if k == "m":
        return item("A block has a density of %s g/cm³ and a volume of %d cm³. What is its mass?" % (n(d), v), "%s g" % n(m),
                    ["%s g" % n(v / d), "%s g" % n(d + v), "%s g" % n(d)], "Mass = density × volume = %s × %d = %s g." % (n(d), v, n(m)))
    return item("A stone has a mass of %s g and a density of %s g/cm³. What is its volume?" % (n(m), n(d)), "%d cm³" % v,
                ["%s cm³" % n(m * d), "%s cm³" % n(m + d), "%s cm³" % n(d / m)], "Volume = mass ÷ density = %s ÷ %s = %d cm³." % (n(m), n(d), v))


LIQ = [("water", 1.0), ("cooking oil", 0.92), ("sea water", 1.03), ("glycerine", 1.26)]
OBJ = [("an ice cube", 0.92), ("a cork", 0.24), ("a plastic bottle cap", 0.95), ("a steel nail", 7.9), ("a glass marble", 2.5), ("an aluminium spoon", 2.7),
       ("a wooden block", 0.6), ("a rubber eraser", 1.5), ("a candle", 0.9), ("a coin", 8.9)]


def g_float():
    o, od = R.choice(OBJ)
    l, ld = R.choice(LIQ)
    if abs(od - ld) < 0.03 or not once(("fl", o, l)):
        return None
    lo, hi = "its density is lower than that of %s" % l, "its density is higher than that of %s" % l
    if od < ld:
        a, w = "It floats, because %s." % lo, ["It sinks, because %s." % lo, "It floats, because %s." % hi, "It sinks, because its mass is large."]
    else:
        a, w = "It sinks, because %s." % hi, ["It floats, because %s." % hi, "It sinks, because %s." % lo, "It floats, because its mass is small."]
    return item("The density of the %s is %s g/cm³. The density of %s is %s g/cm³. What happens when %s is put into %s?" % (o[o.index(" ") + 1:], n(od), l, n(ld), o, l), a, w,
                "An object floats if it is less dense than the liquid, and sinks if it is denser.")


def g_disp():
    a = R.choice([20, 30, 40, 50, 60])
    v = R.choice([4, 6, 8, 12, 15, 18, 25])
    nm, he, his = P.next()
    k = R.choice(["v", "d"])
    if not once(("dp", a, v, k)) or not once(("dpk", k), 5):
        return None
    tb = table(["Reading", "Volume (cm³)"], [["Water only", str(a)], ["Water and stone", str(a + v)]])
    if k == "v":
        return item(tb + "%s put a stone into a measuring cylinder of water. What is the volume of the stone?" % nm, "%d cm³" % v,
                    ["%d cm³" % (a + v), "%d cm³" % a, "%d cm³" % (2 * a + v)], "Volume of stone = %d − %d = %d cm³." % (a + v, a, v))
    m = v * R.choice([2, 3])
    return item(tb + "%s put a stone of mass %d g into a measuring cylinder of water. What is the density of the stone?" % (nm, m), "%s g/cm³" % n(m / v),
                ["%s g/cm³" % n(m / (a + v)), "%s g/cm³" % n(v / m), "%s g/cm³" % n(m / a)], "Volume = %d cm³, so density = %d ÷ %d = %s g/cm³." % (v, m, v, n(m / v)))


PROPS = [("conducts electricity", "electrical conductivity"), ("lets heat pass through it easily", "thermal conductivity"), ("can bend without breaking", "flexibility"),
         ("cannot be scratched easily", "hardness"), ("can hold a heavy load without breaking", "strength"), ("changes from solid to liquid at 1538 °C", "melting point"),
         ("has a mass of 7.9 g for every 1 cm³", "density"), ("changes from liquid to gas at 78 °C", "boiling point")]


def g_prop():
    d, a = R.choice(PROPS)
    if not once(("pp", d)):
        return None
    return item("A material %s. Which physical property is being described?" % d, a, R.sample([x[1] for x in PROPS if x[1] != a], 3), "This is the %s of the material." % a)


DATA = [("Material", "Conducts electricity?", "Melting point (°C)", "Density (g/cm³)"),
        ("P", "yes", "660", "2.7"), ("Q", "no", "1700", "2.5"), ("R", "yes", "1085", "8.9"), ("S", "no", "120", "0.95")]
QD = [("Which material is most likely to be glass?", "Q", "It does not conduct electricity and has a high melting point."),
      ("Which material is most suitable for making a light aircraft body?", "P", "It is a metal with a low density."),
      ("Which material is most suitable for electrical wires?", "R", "Copper conducts electricity well."),
      ("Which material would float on water?", "S", "Its density is less than 1 g/cm³."),
      ("Which material is most likely to be a plastic?", "S", "It does not conduct, melts at a low temperature and has a low density."),
      ("Which material is the densest?", "R", "8.9 g/cm³ is the largest density.")]


def g_data():
    q, a, e = R.choice(QD)
    if not once(("da", q)):
        return None
    return item(table(DATA[0], [list(r) for r in DATA[1:]]) + q, "material " + a, ["material " + x for x in "PQRS" if x != a], e)


B1 = bank([
    ("What is the SI unit of mass?", "kilogram (kg)", ["newton (N)", "gram per cubic centimetre (g/cm³)", "litre (l)"], "Mass is measured with an electronic balance."),
    ("Which instrument is best for measuring the volume of a liquid accurately?", "a measuring cylinder", ["a beaker", "a metre rule", "an electronic balance"], "Read at the bottom of the meniscus, at eye level."),
    ("Which is the correct formula for density?", "density = mass ÷ volume", ["density = volume ÷ mass", "density = mass × volume", "density = mass + volume"], "Units: g/cm³ or kg/m³."),
    ("A steel ball and a steel nail are made of the same steel. Which statement is correct?", "They have the same density.", ["The ball has a greater density.", "The nail has a greater density.", "Steel has no density."], "Density depends on the material, not the size."),
    ("Why is copper used for electrical wires?", "It is a good conductor of electricity and is ductile.", ["It is a poor conductor.", "It has a very low melting point.", "It floats on water."], "Ductile means it can be drawn into wires."),
    ("Why are saucepan handles often made of plastic?", "Plastic is a poor conductor of heat.", ["Plastic is a good conductor of heat.", "Plastic is very dense.", "Plastic conducts electricity."], "The handle stays cool to hold."),
    ("Objects can be classified in different ways. A copper wire and a rubber band can both be grouped as", "flexible materials", ["metals", "conductors of electricity", "materials that melt below 0 °C"], "One object can belong to several groups."),
    ("Why should we choose reusable containers instead of disposable plastic ones?", "to reduce waste from materials that are not sustainable", ["because plastic is a metal", "to use more plastic", "because they are always heavier"], "Making informed choices about materials helps the environment."),
])
B5 = bank([
    ("The density of a liquid is 0.8 g/cm³. What is the mass of 250 cm³ of it?", "200 g", ["312.5 g", "250 g", "0.0032 g"], "Mass = 0.8 × 250 = 200 g."),
    ("A 1 kg block of wood and a 1 kg block of iron are put in water. Why does only the iron sink?", "Iron is denser than water; wood is less dense than water.", ["Iron is heavier.", "Wood has a larger mass.", "Water pushes only on wood."], "Both have the same mass; density decides."),
    ("Oil, water and glycerine are poured into a tube. Which liquid ends up at the top?", "oil, because it is the least dense", ["glycerine, because it is the densest", "water, because it is in the middle", "they stay mixed"], "Less dense liquids float on denser ones."),
    ("Why does a hot-air balloon rise?", "The hot air inside is less dense than the cooler air around it.", ["Hot air has no mass.", "The balloon is made of metal.", "Cool air is less dense."], "Heating air makes it expand, so its density decreases."),
    ("A student measured the length of a pencil three times: 12.1 cm, 12.3 cm, 12.2 cm. What should she record?", "the average, 12.2 cm", ["only the largest, 12.3 cm", "only the first, 12.1 cm", "the total, 36.6 cm"], "Repeating and averaging makes the result more reliable."),
    ("Why is the volume of an irregular stone found by displacement and not with a ruler?", "Its shape makes it hard to measure the length, breadth and height.", ["Rulers cannot measure stones.", "Stones have no volume.", "Displacement measures mass."], "The rise in water level equals the volume of the stone."),
])


def body():
    think = ("<p><b>Physical properties can be observed or measured without changing what the substance is.</b></p>"
             "<ul><li>Examples: electrical and thermal conductivity, melting and boiling point, strength, hardness, flexibility and <b>density</b>.</li>"
             "<li><b>Density = mass ÷ volume</b>, in g/cm³ or kg/m³. It depends on the material, not the size.</li>"
             "<li>An object <b>floats</b> in a liquid that is denser than it, and <b>sinks</b> in one that is less dense.</li>"
             "<li>Volume of an irregular object = rise in water level in a measuring cylinder (<b>displacement</b>).</li></ul>")
    ex = [("Mass 54 g, volume 20 cm³. Density?", ["54 ÷ 20"], "2.7 g/cm³"),
          ("Water rises from 40 cm³ to 52 cm³ when a stone is added. Volume of the stone?", ["52 − 40"], "12 cm³")]
    mist = ["Dividing volume by mass. Density = mass ÷ volume.", "Thinking heavy objects always sink. A big log floats; a small coin sinks.",
            "Taking the final reading as the volume of the object. Subtract the first reading.", "Thinking that a hard material is always strong. Glass is hard but brittle."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Physical properties", B1[4:] + [(g_prop, 8), (MA.g_prop, 4), (MA.g_use, 4)]),
        ("Measuring and density", B1[:4] + [(g_dens, 10), (PM.g_dens, 3), (g_disp, 3)]),
        ("Sinking and floating", [(g_float, 12), (g_disp, 4), (g_dens, 4)]),
        ("Choosing materials", [(g_data, 6), (MA.g_use, 4), (MA.g_class, 4), (g_prop, 3), (g_float, 3)]),
        ("Exam-style questions", B5 + [(g_dens, 4), (g_disp, 4), (g_float, 4), (MA.g_prop, 2)]),
    ])
    make_lss(1, "physical-properties-of-matter", 2, "Diversity", "Exploring Diversity of Matter by its Physical Properties",
             "Describe physical properties such as electrical and thermal conductivity, melting and boiling point, strength, hardness, flexibility and density; classify objects "
             "and choose materials using property data; measure length, mass and volume, use displacement for irregular objects, calculate density (mass/volume) and predict "
             "whether an object sinks or floats (summary of the MOE Lower Secondary Science Syllabus).",
             "Physical Properties of Matter and Density", seo(1, "Physical Properties and Density"), "Physical properties",
             "Free Secondary 1 science worksheets for Singapore students on physical properties of matter: conductivity, melting point, hardness, density calculations, displacement and floating. With answers.",
             "Density = mass ÷ volume.", "Less dense than the liquid: it floats. Denser: it sinks.",
             body(),
             [("How do you calculate density?", "Divide the mass by the volume. The unit is g/cm³ or kg/m³."),
              ("How do you find the volume of an irregular object?", "Put it into water in a measuring cylinder. The rise in the water level is its volume."),
              ("Why does ice float on water?", "Ice (0.92 g/cm³) is less dense than water (1.0 g/cm³).")],
             sets)


if __name__ == "__main__":
    main()
