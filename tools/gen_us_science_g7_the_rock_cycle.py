# -*- coding: utf-8 -*-
"""
US Grade 7 Science: The Rock Cycle (MS-ESS2-1)
  python tools/gen_us_science_g7_the_rock_cycle.py
Develop a model to describe the cycling of Earth's materials and the flow of energy that drives this process:
igneous (cooling magma/lava), sedimentary (weathering, erosion, deposition, compaction and cementation),
metamorphic (heat and pressure); melting. Energy from Earth's interior drives melting and metamorphism; energy
from the sun drives weathering and erosion (water cycle, wind).
Wrong answers come from real mistakes: "rocks never change", "metamorphic rocks form by melting completely",
"the sun melts rocks into magma", "sedimentary rocks form from cooling lava".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, text, arrow, People, INK

U = Unit(70113)
R = U.R
P = People(R)

ROCK = {"igneous": ("forms when melted rock (magma or lava) cools and hardens", ["granite", "basalt", "obsidian", "pumice"]),
        "sedimentary": ("forms when sediments are deposited in layers, then compacted and cemented", ["sandstone", "limestone", "shale", "conglomerate"]),
        "metamorphic": ("forms when existing rock is changed by heat and pressure without melting", ["marble", "slate", "gneiss", "quartzite"])}
PROC = {("igneous", "sedimentary"): "weathering, erosion, deposition, then compaction and cementation",
        ("sedimentary", "metamorphic"): "heat and pressure deep underground",
        ("metamorphic", "igneous"): "melting into magma, then cooling",
        ("igneous", "metamorphic"): "heat and pressure deep underground",
        ("sedimentary", "igneous"): "melting into magma, then cooling",
        ("metamorphic", "sedimentary"): "weathering, erosion, deposition, then compaction and cementation"}


def g_type():
    k = R.choice(sorted(ROCK))
    how, ex = ROCK[k]
    who = P.next()[0]
    r = R.random()
    if r < 0.4:
        return item("%s finds a rock that %s. What type of rock is it?" % (who, how), k, [x for x in ROCK if x != k] + ["a mineral, not a rock"], "%s rock %s." % (k.capitalize(), how))
    if r < 0.7:
        x = R.choice(ex)
        return item("%s's rock kit has a sample of %s. What type of rock is it?" % (who, x), k, [y for y in ROCK if y != k] + ["a fossil"], "%s is %s." % (x.capitalize(), k))
    return item("%s needs a %s rock for a display. Which sample should %s choose?" % (who, k, who), R.choice(ex), R.sample([e for y in ROCK if y != k for e in ROCK[y][1]], 3),
                "%s rocks include %s." % (k.capitalize(), ", ".join(ex)))


def g_path():
    a, b = R.choice(sorted(PROC))
    who = P.next()[0]
    return item("%s's model shows %s rock changing into %s rock. Which process causes this?" % (who, a, b), PROC[(a, b)],
                R.sample(sorted({v for k_, v in PROC.items() if v != PROC[(a, b)]}) + ["photosynthesis", "freezing water only"], 3), "In the rock cycle, %s rock becomes %s rock by %s." % (a, b, PROC[(a, b)]))


ENER = [("melting rock into magma", "Earth's interior heat"), ("metamorphism (heat and pressure)", "Earth's interior heat"), ("volcanic eruptions", "Earth's interior heat"),
        ("weathering by rain and ice", "the sun (which drives the water cycle)"), ("erosion by wind", "the sun (which heats air unevenly)"), ("rivers carrying sediment downhill", "the sun and gravity")]


def g_energy():
    p, src = R.choice(ENER)
    who = P.next()[0]
    w = ["Earth's interior heat", "the sun (which drives the water cycle)", "the moon", "the sun and gravity", "the sun (which heats air unevenly)"]
    w = [x for x in w if x != src and not (src.startswith("the sun") and x.startswith("the sun"))]
    return item("%s asks what energy source drives %s in the rock cycle. What is the best answer?" % (who, p), src, R.sample(w, 3) if len(w) >= 3 else w + ["static electricity"],
                "Interior heat drives melting and metamorphism; the sun drives weathering and erosion.")


def cycle_svg(hide):
    W, H = 420, 250
    pos = {"igneous": (210, 30), "sedimentary": (80, 200), "metamorphic": (340, 200)}
    s = []
    for k, (x, y) in pos.items():
        t = "?" if k == hide else k.capitalize() + " rock"
        s.append(rect(x - 62, y - 18, 124, 36, "#fff3c4" if k == hide else "#eef4fb", INK, 2, 8) + text(x, y + 5, t, 13))
    s.append(arrow(170, 50, 105, 178, INK, 2, 8) + text(105, 110, "weathering,", 11, "end", weight=400) + text(105, 124, "erosion, deposition", 11, "end", weight=400))
    s.append(arrow(144, 205, 274, 205, INK, 2, 8) + text(209, 228, "heat and pressure", 11, weight=400))
    s.append(arrow(320, 178, 250, 50, INK, 2, 8) + text(312, 110, "melting,", 11, "start", weight=400) + text(312, 124, "cooling", 11, "start", weight=400))
    return svg_wrap(W, H, "".join(s), "a rock cycle diagram with one rock type missing").replace("<svg ", "<svg data-pf='lg' ", 1)


def g_diag():
    k = R.choice(sorted(ROCK))
    who = P.next()[0]
    return item(fig(cycle_svg(k)) + "Which rock type belongs in the box with the question mark in %s's diagram?" % who, k + " rock", [x + " rock" for x in ROCK if x != k] + ["magma"],
                "%s rock %s." % (k.capitalize(), ROCK[k][0]))


B1 = bank([
    ("What is the rock cycle?", "the slow processes that change rocks from one type to another", ["the path of a rolling rock", "a kind of volcano", "the water cycle"], "Rocks are constantly recycled over millions of years."),
    ("What are the three main types of rock?", "igneous, sedimentary and metamorphic", ["hard, soft and medium", "lava, magma and ash", "granite, marble and sand only"], "They form in different ways."),
    ("Which rock type often contains fossils?", "sedimentary", ["igneous", "metamorphic", "volcanic glass"], "Layers of sediment can bury organisms."),
    ("What is the difference between magma and lava?", "Magma is melted rock underground; lava is melted rock on the surface.", ["They are different elements.", "Lava is cold.", "Magma is solid."],
     "Both cool to form igneous rock."),
    ("Does a rock have to melt to become metamorphic?", "No. Heat and pressure change it without melting it.", ["Yes, completely.", "Yes, into lava.", "Only in the ocean."], "If it melts, it becomes magma."),
    ("Which energy drives weathering and erosion?", "energy from the sun", ["Earth's interior heat only", "the moon", "magnetism"], "The sun drives wind and the water cycle."),
    ("Which energy drives melting and metamorphism?", "heat from Earth's interior", ["sunlight", "wind", "ocean waves"], "Deep underground it is very hot."),
    ("Can a rock follow different paths through the rock cycle?", "Yes. Any rock type can become any other type.", ["No, there is only one path.", "Only igneous rocks change.", "Rocks never change."],
     "The cycle has many paths."),
])
B5 = bank([
    ("Ava models sedimentary rock by pressing layers of sand, gravel and glue in a cup. What does the glue stand for?", "natural cement that holds sediments together", ["magma", "heat", "fossils"],
     "Minerals in water cement grains together."),
    ("Leo models metamorphic rock by pressing a ball of layered clay. The layers bend and flatten. What does the pushing stand for?", "pressure deep inside Earth", ["weathering by rain", "melting", "erosion by wind"],
     "Pressure changes rock without melting it."),
    ("Mia compares granite (large crystals) and basalt (tiny crystals). Why are their crystals different sizes?", "Granite cooled slowly underground; basalt cooled quickly on the surface.", ["Granite is younger.", "Basalt melted twice.", "Crystal size is random."],
     "Slow cooling makes large crystals."),
    ("A river carries pebbles from a mountain to a lake. Which part of the rock cycle is this?", "erosion and deposition", ["melting", "metamorphism", "cooling of lava"], "Sediments move and settle."),
    ("Why do we find marble where limestone used to be?", "Heat and pressure changed the limestone into marble.", ["Limestone melted into lava.", "Marble rained down.", "Water dissolved the marble."],
     "Limestone (sedimentary) → marble (metamorphic)."),
])


def body():
    think = ("<p>Rocks are constantly changing in the <b>rock cycle</b>:</p><ul>"
             + "".join("<li><b>%s</b> rock %s (examples: %s).</li>" % (k.capitalize(), v[0], ", ".join(v[1][:3])) for k, v in ROCK.items()) + "</ul>"
             + figure(cycle_svg(None), "Any rock type can become another type.")
             + "<p><b>Energy</b> drives the cycle: heat from <b>Earth's interior</b> melts rock and causes metamorphism; energy from the <b>sun</b> (with gravity) drives weathering, erosion and deposition.</p>")
    ex = [("Lava cools into black glassy rock. What type?", ["Cooling melted rock."], "igneous"),
          ("Shale is heated and squeezed into slate. Which process?", ["Heat and pressure, no melting."], "metamorphism")]
    mist = ["Thinking rocks never change.",
            "Thinking metamorphic rock forms by melting.",
            "Thinking the sun melts rocks into magma. Earth's interior heat does."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Types of rock", B1 + [(g_type, 12)]),
        ("How rocks form", [(g_type, 12), (g_path, 8)]),
        ("Paths through the rock cycle", [(g_path, 12), (g_diag, 8)]),
        ("Energy in the rock cycle", [(g_energy, 12), (g_diag, 4), (g_type, 4)]),
        ("Modeling rocks", B5 + [g_path, g_energy, g_type, g_diag]),
    ])
    make("grade-7", "the-rock-cycle", 13, "MS-ESS2-1",
         "Develop a model to describe the cycling of Earth's materials and the flow of energy that drives this process.",
         "The Rock Cycle",
         "Grade 7 Rock Cycle Worksheets: Igneous, Sedimentary and Metamorphic Rocks",
         "The Rock Cycle",
         "Free middle school science worksheets on the rock cycle (NGSS MS-ESS2-1): igneous, sedimentary and metamorphic rocks, the processes that change them, and the energy from Earth's interior and the sun. 100 practice questions with answers.",
         "Rocks change from one type to another.",
         "Melting and cooling, weathering and deposition, and heat and pressure cycle Earth's materials, driven by Earth's heat and the sun.",
         body(),
         [("What are the three types of rock?", "Igneous (cooled magma or lava), sedimentary (compacted and cemented sediments) and metamorphic (changed by heat and pressure)."),
          ("What energy drives the rock cycle?", "Heat from Earth's interior drives melting and metamorphism; energy from the sun drives weathering and erosion."),
          ("Can a sedimentary rock become igneous?", "Yes. If it is buried deep enough to melt, the magma can cool to form igneous rock.")],
         sets)


if __name__ == "__main__":
    main()
