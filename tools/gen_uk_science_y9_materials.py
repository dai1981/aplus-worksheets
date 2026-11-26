# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Chemistry): Materials
  python tools/gen_uk_science_y9_materials.py
The properties of metals, ceramics, polymers and composites (qualitative), choosing materials for a job, natural and
synthetic materials, polymers made from monomers, alloys, and the environmental impact of materials (plastics,
recycling, biodegradable materials). Reuses the polymer, material-choice and synthetic-material questions of the US
units in British English.
Wrong answers come from real mistakes: "ceramics conduct electricity", "all plastics are the same",
"composites are mixtures that can be separated easily", "alloys are compounds".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once, ukm, adopt_us

U = Unit(61906)
R = U.R
P = People(R)
uk_sci.USED.clear()
MS = adopt_us("gen_us_science_chem_molecular_structure_and_materials", U)
SY = adopt_us("gen_us_science_g7_synthetic_materials", U)
_poly, us_job = ukm(MS.g_poly), ukm(MS.g_job)


def us_poly():
    it = _poly()
    return None if it is None or "mol" in it["q"] + it["e"] else it
us_kind, us_src, us_steps, us_imp = ukm(SY.g_kind), ukm(SY.g_source), ukm(SY.g_steps), ukm(SY.g_impact)

CLASS = [("porcelain", "a ceramic"), ("brick", "a ceramic"), ("glass", "a ceramic"), ("pottery", "a ceramic"), ("polythene", "a polymer"), ("PVC", "a polymer"),
         ("nylon", "a polymer"), ("polystyrene", "a polymer"), ("fibreglass", "a composite"), ("reinforced concrete", "a composite"), ("carbon fibre", "a composite"),
         ("plywood", "a composite"), ("steel", "a metal (alloy)"), ("brass", "a metal (alloy)"), ("copper", "a metal")]


def g_class():
    m, c = R.choice(CLASS)
    if not once(("cl", m)):
        return None
    w = [x for x in ["a ceramic", "a polymer", "a composite", "a metal"] if x not in (c, "a metal" if c.startswith("a metal") else "")]
    return item("Which type of material is %s?" % m, c, w[:3], "Ceramics: hard, brittle, insulating. Polymers: long-chain molecules. Composites: two materials combined.")


PROP = [("hard, brittle, heat-resistant and an electrical insulator", "ceramics"), ("flexible, low density, easy to mould and an insulator", "polymers"),
        ("strong, shiny, malleable and a good conductor", "metals"), ("made of two or more materials combined to get the best properties of each", "composites")]


def g_prop():
    p, a = R.choice(PROP)
    k = R.random() < 0.5
    if not once(("pr", p, k)):
        return None
    if k:
        return item("Which group of materials is usually %s?" % p, a, [x[1] for x in PROP if x[1] != a], "Each group has typical properties.")
    return item("What are %s usually like?" % a, p[0].upper() + p[1:] + ".", [x[0][0].upper() + x[0][1:] + "." for x in PROP if x[1] != a], "Each group has typical properties.")


USE = [("the tiles on a space shuttle", "a ceramic, because it resists very high temperatures"), ("a bicycle frame for racing", "carbon fibre, because it is strong and light"),
       ("electrical plug cases", "a hard polymer, because it is an insulator and can be moulded"), ("a saucepan base", "a metal, because it conducts heat well"),
       ("the hull of a small boat", "fibreglass, because it is strong, light and does not rust"), ("a bridge support", "reinforced concrete, because it is strong when squeezed and stretched"),
       ("a dinner plate", "a ceramic, because it is hard and easy to clean"), ("a carrier bag", "polythene, because it is flexible and waterproof")]


def g_use():
    o, a = R.choice(USE)
    if not once(("us", o)):
        return None
    return item("Which material is best for %s?" % o, a, R.sample([x[1] for x in USE if x[1] != a and x[1].split(",")[0] != a.split(",")[0]], 3), "Match the properties to the job.")


B1 = bank([
    ("What is an alloy?", "a mixture of a metal with other elements, which is often stronger", ["a pure metal", "a compound of two non-metals", "a type of plastic"], "Steel, brass, bronze."),
    ("Why are alloys harder than pure metals?", "Different-sized atoms stop the layers sliding easily.", ["They have no atoms.", "They are softer.", "They are compounds."], "Distorted layers."),
    ("What is a polymer?", "a very long molecule made by joining many small molecules (monomers)", ["a single small molecule", "a mixture of metals", "a ceramic"], "Plastics are polymers."),
    ("What is a composite material?", "two or more materials combined to get the best properties of each", ["a pure element", "a single polymer", "a metal ore"], "Reinforced concrete."),
])
B5 = bank([
    ("Why are many plastics a problem in the environment?", "Most are not biodegradable, so they last for hundreds of years.", ["They rot in a week.", "They are made from water.", "They are edible."], "Pollution."),
    ("What does biodegradable mean?", "able to be broken down by microorganisms", ["can be melted", "is made of metal", "never breaks down"], "Compostable."),
    ("Why are plastics sorted by type before recycling?", "Different polymers melt at different temperatures and have different properties.", ["They are all identical.", "To change their colour.", "So they can be burned."], "Recycling codes."),
    ("Why is glass a good choice for a window?", "It is transparent, hard and waterproof.", ["It is flexible.", "It conducts electricity.", "It is a polymer."], "Ceramic."),
])


def body():
    think = ("<p><b>Choose a material by its properties.</b></p>"
             "<ul><li>Metals: strong, malleable, conductors. Ceramics: hard, brittle, heat-resistant insulators.</li>"
             "<li>Polymers: long chains of monomers; light, flexible, insulating. Composites combine two materials.</li>"
             "<li>Alloys are harder than pure metals. Many plastics are not biodegradable, so recycling matters.</li></ul>")
    ex = [("Fibreglass: what type?", ["Glass fibres in a polymer"], "a composite"),
          ("A plug case: which material?", ["Insulator, can be moulded"], "a polymer")]
    mist = ["Thinking ceramics conduct electricity.", "Thinking alloys are compounds.", "Thinking all plastics are the same."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Types of material", B1 + [(g_class, 11), (g_prop, 4), (us_src, 1)]),
        ("Properties and uses", [(g_prop, 3), (g_use, 7), (us_job, 7), (g_class, 3)]),
        ("Polymers", [(us_poly, 11), (us_src, 7), (us_steps, 2)]),
        ("Natural and synthetic", [(us_kind, 12), (us_steps, 6), (us_imp, 2)]),
        ("Materials and the environment", B5 + [(us_imp, 8), (us_kind, 4), (us_poly, 2), (us_job, 2)]),
    ])
    make_ks3(9, "materials", 6, "Chemistry", "Materials",
             "Properties of ceramics, polymers and composites (qualitative); Earth as a source of limited resources and the efficacy of recycling.",
             "Materials",
             "Year 9 Science: Materials Worksheets (Ceramics, Polymers, Composites, Alloys)",
             "Materials",
             "Free Year 9 science worksheets on materials: metals, ceramics, polymers and composites, alloys, choosing materials for a job, natural and synthetic materials, and plastics in the environment. 100 questions with answers.",
             "Choose a material by its properties.",
             "Ceramics are hard and brittle; polymers are long chains; composites combine materials.",
             body(),
             [("What are ceramics, polymers and composites?", "Ceramics (such as pottery and glass) are hard, brittle insulators. Polymers (plastics) are long-chain molecules. Composites combine two materials, like carbon fibre or reinforced concrete."),
              ("Why are alloys used instead of pure metals?", "Mixing in atoms of a different size stops the layers of metal atoms sliding, so alloys are harder and stronger."),
              ("Why is plastic waste a problem?", "Most plastics are not biodegradable, so they build up in landfill and the oceans. Recycling and reducing use help.")],
             sets)


if __name__ == "__main__":
    main()
