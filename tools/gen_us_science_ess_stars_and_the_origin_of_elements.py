# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Stars and the Origin of Elements (HS-ESS1-3)
  python tools/gen_us_science_ess_stars_and_the_origin_of_elements.py
Communicate scientific ideas about the way stars, over their life cycle, produce elements.
Where elements come from (Big Bang, ordinary stars, massive stars, supernovae and neutron-star mergers), helium-capture
fusion (3 ⁴He → ¹²C …), star life cycles, reading spectral lines to find a star's elements, and star color and temperature.
Wrong answers come from real mistakes: "all elements were made in the Big Bang", "stars fuse iron to get energy",
"red stars are the hottest", "the Sun will become a black hole".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90403)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SRC = ["the Big Bang", "fusion in ordinary stars like the Sun and red giants", "fusion in the cores of massive stars", "supernovae and neutron-star mergers"]
ELS = [("hydrogen", 0), ("most helium", 0), ("carbon", 1), ("nitrogen", 1), ("oxygen", 2), ("neon", 2), ("silicon", 2), ("magnesium", 2), ("iron", 2), ("sulfur", 2),
       ("gold", 3), ("silver", 3), ("uranium", 3), ("platinum", 3), ("lead", 3), ("iodine", 3)]


@safe
def g_where():
    e, k = R.choice(ELS)
    if not once(("wh", e)):
        return None
    if e == "carbon" or e == "nitrogen":
        a = SRC[1]
    else:
        a = SRC[k]
    return item("Where was most of the %s in the universe made?" % e, a, [x for x in SRC if x != a],
                "Big Bang: H, He. Stars: He → C, N, O. Massive stars: up to iron. Heavier than iron: supernovae and neutron-star mergers.")


NAMES = {6: ("carbon", "C"), 8: ("oxygen", "O"), 10: ("neon", "Ne"), 12: ("magnesium", "Mg"), 14: ("silicon", "Si"), 16: ("sulfur", "S"), 18: ("argon", "Ar"), 20: ("calcium", "Ca")}


@safe
def g_fuse():
    n = R.randint(3, 10)
    k = R.choice(["el", "A"])
    if not once(("fs", n, k)):
        return None
    z, a = 2 * n, 4 * n
    nm, sym = NAMES[z]
    if k == "el":
        w = [NAMES[x][0] for x in NAMES if x != z]
        return item("In a massive star, %d helium-4 nuclei (2 protons each) are built up into one nucleus. Which element is it?" % n, nm, R.sample(w, 3),
                    "%d × 2 = %d protons → %s." % (n, z, nm))
    g = "%s-%d" % (nm, a)
    return item("In a star, %d helium-4 nuclei combine step by step. What nucleus forms?" % n, g, uniq(g, ["%s-%d" % (nm, a + 2), "%s-%d" % (nm, z), "%s-%d" % (NAMES[z + 2][0] if z + 2 in NAMES else "carbon", a), "%s-%d" % (nm, a - 4)]),
                "Mass number 4 × %d = %d; atomic number 2 × %d = %d (%s)." % (n, a, n, z, nm))


LIFE_S = ["nebula", "main-sequence star", "red giant", "planetary nebula", "white dwarf"]
LIFE_M = ["nebula", "main-sequence star", "red supergiant", "supernova", "neutron star or black hole"]


@safe
def g_stage():
    big = R.random() < 0.5
    seq = LIFE_M if big else LIFE_S
    i = R.randint(0, 3)
    before = R.random() < 0.5
    if not once(("st", big, i, before)):
        return None
    who = "a star more than about 8 times the Sun's mass" if big else "a Sun-like star"
    other = [x for x in LIFE_S + LIFE_M if x != seq[i + 1] and x != seq[i]]
    if before:
        return item("In the life of %s, what stage comes just before the %s stage?" % (who, seq[i + 1]), seq[i], R.sample(sorted(set(x for x in LIFE_S + LIFE_M if x not in (seq[i], seq[i + 1]))), 3),
                    " → ".join(seq) + ".")
    return item("In the life of %s, what comes right after the %s stage?" % (who, seq[i]), seq[i + 1], R.sample(sorted(set(other)), 3), " → ".join(seq) + ".")


LINES = {"hydrogen": [410, 434, 486, 656], "helium": [447, 502, 588, 668], "sodium": [589, 590], "calcium": [393, 397]}


@safe
def g_spec():
    who = P.next()[0]
    have = sorted(R.sample(sorted(LINES), R.choice([2, 2, 3])))
    k = R.choice(["in", "out"])
    a = R.choice(have) if k == "in" else R.choice([e for e in sorted(LINES) if e not in have])
    if not once(("sp", tuple(have), k, a)):
        return None
    seen = sorted(set(l for e in have for l in LINES[e]))
    if any(l in seen for e in LINES if e not in have for l in LINES[e]):
        return None
    tab = table(["Element", "Lines in the lab (nm)"], [[e, ", ".join(map(str, LINES[e]))] for e in sorted(LINES)])
    q = tab + "%s's star shows dark lines at %s nm. " % (who, ", ".join(map(str, seen)))
    if k == "in":
        return item(q + "Which element is in the star?", a, ([e for e in sorted(LINES) if e not in have] + ["iron", "gold"])[:3], "Every line of the element matches.")
    return item(q + "Which element is NOT found in the star's spectrum?", a, (have + ["They are all present."])[:3], "None of its lines appear.")


COLS = [("blue", 25000), ("blue-white", 12000), ("white", 8000), ("yellow", 5800), ("orange", 4500), ("red", 3200)]


@safe
def g_color():
    a, b = R.sample(COLS, 2)
    k = R.choice(["hot", "cool"])
    if not once(("cl", tuple(sorted((a[0], b[0]))), k)):
        return None
    hot, cool = (a, b) if a[1] > b[1] else (b, a)
    first, second = sorted([a, b])
    A = lambda c: ("an " if c[0] in "aeiou" else "a ") + c
    if k == "hot":
        return item("Which star has the hotter surface: %s star or %s star?" % (A(first[0]), A(second[0])), "the %s star" % hot[0], ["the %s star" % cool[0], "They are the same temperature.", "Color does not depend on temperature."],
                    "Hot stars glow blue; cool stars glow red.")
    return item("Which star is cooler: %s star or %s star?" % (A(first[0]), A(second[0])), "the %s star" % cool[0], ["the %s star" % hot[0], "They are the same temperature.", "Color does not depend on temperature."],
                "%s ≈ %s K; %s ≈ %s K." % (hot[0], num(hot[1]), cool[0], num(cool[1])))


B1 = bank([
    ("Which elements were made mostly in the Big Bang?", "hydrogen and helium", ["carbon and oxygen", "iron and nickel", "gold and uranium"], "Lightest elements."),
    ("Why do massive stars stop fusing at iron?", "Fusing iron uses up energy instead of releasing it.", ["Iron is too light.", "Iron is a gas.", "They run out of hydrogen first."], "Energy peak at iron."),
    ("What is a supernova?", "the explosion of a massive star at the end of its life", ["the birth of a star", "a small planet", "a type of nebula only"], "Makes and spreads heavy elements."),
    ("Why do astronomers say 'we are made of star stuff'?", "The carbon, oxygen and other elements in our bodies were made in stars.", ["Humans glow.", "Stars are made of people.", "Only hydrogen is in our bodies."], "Stellar nucleosynthesis."),
    ("How do scientists know what elements are in a distant star?", "by matching dark lines in the star's spectrum to lab spectra", ["by sending a probe", "by the star's size", "by its distance"], "Spectroscopy."),
    ("What will the Sun become at the end of its life?", "a white dwarf", ["a black hole", "a neutron star", "a supernova"], "Not massive enough."),
    ("What fuels a main-sequence star?", "hydrogen fusing into helium in its core", ["helium fusing into iron", "burning coal", "uranium fission"], "Main sequence."),
    ("Where did the gold in jewelry come from?", "neutron-star mergers and supernovae", ["the Big Bang", "the Sun's core", "Earth's mantle forming it"], "Rapid neutron capture."),
])
B5 = bank([
    ("Why are old stars mostly hydrogen and helium with few heavy elements?", "They formed before many stars had made and spread heavier elements.", ["Old stars destroy heavy elements.", "Heavy elements sink out.", "Old stars are cooler."], "Chemical evolution of galaxies."),
    ("Why does the solar system contain heavy elements like iron and uranium?", "It formed from gas enriched by earlier generations of stars.", ["The Sun made them all.", "They came from the Big Bang.", "Earth makes them inside."], "Recycled material."),
    ("In 2017, astronomers saw two neutron stars merge and detected heavy elements. What did this show?", "Neutron-star mergers make heavy elements like gold.", ["Gold is made on planets.", "Neutron stars contain no matter.", "Only supernovae make elements."], "Gravitational waves + light."),
    ("Why do spectral lines of a distant galaxy match lab elements but appear shifted?", "The galaxy is moving away, so the lines are redshifted.", ["The elements are different there.", "The telescope is broken.", "Light changes color randomly."], "Same physics everywhere."),
    ("A star's spectrum shows strong iron lines. What can you infer?", "It formed from gas that earlier stars had enriched with iron.", ["It is making gold now.", "It is a Big Bang star.", "It has no hydrogen."], "Metal-rich star."),
])


def body():
    think = ("<p><b>Stars make the elements, layer by layer.</b></p>"
             "<ul><li>Big Bang: hydrogen and helium. Ordinary stars: helium, then carbon and oxygen in red giants.</li>"
             "<li>Massive stars fuse heavier elements up to iron. Heavier elements (gold, uranium) form in supernovae and neutron-star mergers.</li>"
             "<li>Spectra reveal a star's elements; color shows temperature (blue hot, red cool).</li></ul>")
    ex = [("3 helium-4 nuclei fuse. Product?", ["3 × 2 = 6 protons", "3 × 4 = 12"], "carbon-12"),
          ("Where was the gold on Earth made?", ["Heavier than iron"], "neutron-star mergers and supernovae")]
    mist = ["Thinking all elements came from the Big Bang.", "Thinking stars get energy by fusing iron.", "Thinking red stars are the hottest."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Where elements come from", B1 + [(g_where, 12)]),
        ("Fusion in stars", [(g_fuse, 10), (g_stage, 10)]),
        ("Star life cycles", [(g_stage, 4), (g_color, 12), (g_fuse, 4)]),
        ("Reading spectra", [(g_spec, 16), (g_color, 4)]),
        ("Evidence from stars", B5 + [(g_spec, 8), (g_color, 6), (g_fuse, 1)]),
    ])
    make("earth-and-space-science", "stars-and-the-origin-of-elements", 3, "HS-ESS1-3",
         "Communicate scientific ideas about the way stars, over their life cycle, produce elements.",
         "Stars and the Origin of Elements",
         "Stars and Elements Worksheets: Fusion, Life Cycles, Supernovae and Spectra (Earth Science)",
         "Stars and Elements",
         "Free high school Earth and space science worksheets on stars and the origin of elements (NGSS HS-ESS1-3): fusion in stars, star life cycles, supernovae, spectra and star color. 100 questions with answers.",
         "Stars make the elements.",
         "Fusion builds elements up to iron; supernovae and neutron-star mergers make heavier ones.",
         body(),
         [("Where do the elements come from?", "Hydrogen and helium came from the Big Bang. Stars fused heavier elements up to iron. Elements heavier than iron came mostly from supernovae and neutron-star mergers."),
          ("Why does fusion stop at iron?", "Fusing nuclei lighter than iron releases energy, but fusing iron uses energy, so a star's core cannot keep going."),
          ("How do we know what stars are made of?", "Each element absorbs light at its own set of wavelengths, so the dark lines in a star's spectrum show which elements are present.")],
         sets)


if __name__ == "__main__":
    main()
