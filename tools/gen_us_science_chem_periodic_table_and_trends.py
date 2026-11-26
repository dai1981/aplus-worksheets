# -*- coding: utf-8 -*-
"""
US High School Chemistry: The Periodic Table and Periodic Trends (HS-PS1-1)
  python tools/gen_us_science_chem_periodic_table_and_trends.py
Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons
in the outermost energy level of atoms.
Groups and periods, families (alkali metals, alkaline earth metals, halogens, noble gases), metals, nonmetals and
metalloids, valence electrons and ion charges, and trends in atomic radius, ionization energy, electronegativity and
reactivity. Every trend comparison is checked against real data (EN, IE, RAD in sci_chem) so exceptions are never asked.
Wrong answers come from real mistakes: "atoms get bigger across a period", "the group number is the period",
"noble gases react easily".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_chem import EL, BY, MAIN, FAMILY, valence, ion_charge, ion, EN, IE, RAD

U = Unit(90202)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def name(e):
    return "%s (%s)" % (e[1], e[0])


def Name(e):
    return name(e)[0].upper() + name(e)[1:]


def g_loc():
    e = R.choice(MAIN + [BY["Fe"], BY["Cu"], BY["Zn"], BY["Ag"]])
    k = R.choice(["group", "period"])
    if not once(("lc", e[0], k)):
        return None
    g, p = e[5], e[6]
    if k == "group":
        w = [str(x) for x in [p, g + 1, g - 1, valence(e) if e in MAIN else g + 2] if x != g and x > 0]
        w = list(dict.fromkeys(w))[:3]
        if len(w) < 3:
            return None
        return item("Which group (column) is %s in?" % name(e), str(g), w, "Columns are groups 1–18.")
    w = [str(x) for x in [g if g <= 7 else p + 2, p + 1, p - 1, p + 2] if x != p and x > 0]
    w = list(dict.fromkeys(w))[:3]
    if len(w) < 3:
        return None
    return item("Which period (row) is %s in?" % name(e), str(p), w, "Rows are periods; the period is the number of occupied shells.")


def g_val():
    e = R.choice([x for x in MAIN if x[0] != "H"])
    k = R.choice(["val", "charge"])
    c = ion_charge(e)
    if k == "charge" and c is None:
        return None
    if not once(("vl", e[0], k)):
        return None
    v = valence(e)
    if k == "val":
        return item("How many valence electrons does %s have? (It is in group %d.)" % (name(e), e[5]), str(v), [str(x) for x in R.sample([x for x in range(1, 9) if x != v and x != e[5]], 3)],
                    "Groups 1–2: same as the group number. Groups 13–18: subtract 10 (helium has 2).")
    ws = ["%+d" % x for x in [-c, c + 1 if c > 0 else c - 1, v if v != c else v + 1, 8 - v] if x != c]
    ws = [w.replace("-", "−") for w in dict.fromkeys(ws)][:3]
    if len(ws) < 3:
        return None
    return item("%s has %d valence electrons. What charge does its ion usually have?" % (Name(e), v), ("%+d" % c).replace("-", "−"), ws,
                "Metals lose electrons (+); nonmetals gain electrons to fill the shell (−).")


def g_fam():
    k = R.choice(["name", "which", "same"])
    if k == "name":
        e = R.choice([x for x in MAIN if x[5] in FAMILY and x[0] != "H"])
        if not once(("fn", e[0])):
            return None
        f = FAMILY[e[5]]
        return item("Which family does %s belong to?" % name(e), f, R.sample([x for x in ["alkali metals", "alkaline earth metals", "halogens", "noble gases", "transition metals"] if x != f], 3),
                    "Group %d is the %s." % (e[5], f))
    if k == "which":
        g = R.choice([1, 2, 17, 18])
        e = R.choice([x for x in MAIN if x[5] == g and x[0] != "H"])
        w = R.sample([x for x in MAIN if x[5] != g and x[0] != "H"], 3)
        if not once(("fw", e[0])):
            return None
        return item("Which element is one of the %s?" % FAMILY[g], name(e), [name(x) for x in w], "%s is in group %d." % (e[1].capitalize(), g))
    e = R.choice([x for x in MAIN if x[0] not in ("H", "He") and x[5] in (1, 2, 16, 17, 18)])
    same = [x for x in MAIN if x[5] == e[5] and x != e and x[0] not in ("H", "He") and x[7] == e[7]]
    if not same:
        return None
    s = R.choice(same)
    w = [x for x in MAIN if x[5] != e[5] and abs(x[2] - e[2]) <= 2 and x[0] != "H"]
    if len(w) < 3 or not once(("fs", e[0], s[0])):
        return None
    return item("Which element has chemical properties most like %s?" % name(e), name(s), [name(x) for x in R.sample(w, 3)], "Same group = same number of valence electrons.")


def g_class():
    e = R.choice([x for x in EL if x[5] != 18])
    k = e[7]
    if not once(("cl", e[0])):
        return None
    return item("Is %s a metal, a nonmetal, a metalloid or a noble gas?" % name(e), k, [x for x in ["metal", "nonmetal", "metalloid", "noble gas"] if x != k],
                "Metals are on the left, nonmetals on the right, metalloids along the staircase.")


PROP = {"rad": ("larger atomic radius", RAD, 1), "ie": ("higher first ionization energy", IE, 1), "en": ("higher electronegativity", EN, 1)}


def trend_ok(a, b, key):
    """a and b in the same group or period, and the real data follow the textbook trend"""
    d = PROP[key][1]
    if a[0] not in d or b[0] not in d or a[0] == "H" or b[0] == "H":
        return False
    if a[5] == b[5]:
        lower = a if a[6] > b[6] else b
        want = lower if key == "rad" else (b if lower is a else a)
    elif a[6] == b[6]:
        if a[5] == 18 or b[5] == 18:
            return False
        right = a if a[5] > b[5] else b
        want = (b if right is a else a) if key == "rad" else right
    else:
        return False
    big = a if d[a[0]] > d[b[0]] else b
    return big is want and abs(d[a[0]] - d[b[0]]) / max(d[a[0]], d[b[0]]) > 0.06


def g_trend():
    key = R.choice(["rad", "ie", "en"])
    a, b = R.sample([x for x in MAIN if x[0] in PROP[key][1]], 2)
    if not trend_ok(a, b, key):
        return None
    d = PROP[key][1]
    big, small = (a, b) if d[a[0]] > d[b[0]] else (b, a)
    if not once(("tr", key, tuple(sorted((a[0], b[0]))))):
        return None
    how = "same group" if a[5] == b[5] else "same period"
    first, second = sorted([big, small], key=lambda x: x[0])
    why = {"rad": {"same group": "More shells down a group.", "same period": "More protons pull the shells in across a period."},
           "ie": {"same group": "Outer electrons are farther from the nucleus down a group, so they are easier to remove.", "same period": "Across a period, more protons hold electrons more tightly."},
           "en": {"same group": "Electronegativity decreases down a group.", "same period": "Electronegativity increases across a period."}}[key][how]
    return item("%s and %s are in the %s. Which has the %s?" % (Name(first), name(second), how, PROP[key][0]), name(big),
                [name(small), "They are exactly the same.", "It cannot be predicted from the periodic table."], why)


def g_react():
    g = R.choice([1, 17])
    a, b = R.sample([x for x in MAIN if x[5] == g and x[0] != "H" and x[6] <= 6], 2)
    if not once(("rc", g, tuple(sorted((a[0], b[0]))))):
        return None
    more = (a if a[6] > b[6] else b) if g == 1 else (a if a[6] < b[6] else b)
    less = b if more is a else a
    return item("Which is more reactive, %s or %s?" % (name(a), name(b)), name(more), [name(less), "They react the same.", "Neither reacts."],
                "Alkali metals get more reactive down the group (easier to lose 1 electron)." if g == 1 else "Halogens get less reactive down the group (harder to gain 1 electron).")


def g_table():
    who = P.next()[0]
    key = R.choice(["rad", "ie"])
    g = R.choice([1, 2, 17])
    els = [x for x in MAIN if x[5] == g and x[0] in PROP[key][1] and x[0] != "H"][:4]
    k = R.choice(["trend", "pred"])
    if not once(("tb", key, g, k)):
        return None
    d = PROP[key][1]
    unit = "pm" if key == "rad" else "kJ/mol"
    tab = table(["Element (group %d)" % g, "%s (%s)" % ("Atomic radius" if key == "rad" else "First ionization energy", unit)], [[name(x), str(d[x[0]])] for x in els])
    if k == "trend":
        a = "It %s down the group." % ("increases" if key == "rad" else "decreases")
        return item(tab + "%s collected %s data for group %d. What is the pattern?" % (who, "atomic radius" if key == "rad" else "ionization energy", g), a, ["It %s down the group." % ("decreases" if key == "rad" else "increases"), "It stays the same.", "It changes at random."],
                    "One more shell each period.")
    nxt = [x for x in MAIN if x[5] == g and x[6] == els[-1][6] + 1]
    if not nxt:
        return None
    n = nxt[0]
    return item(tab + "Using %s's data, what would you predict for %s?" % (who, name(n)), "%s than %d" % ("larger" if key == "rad" else "lower", d[els[-1][0]]),
                ["%s than %d" % ("smaller" if key == "rad" else "higher", d[els[-1][0]]), "exactly %d" % d[els[0][0]], "0"], "Continue the pattern down the group.")


B1 = bank([
    ("What are the rows of the periodic table called?", "periods", ["groups", "families", "columns"], "Rows = periods."),
    ("What are the columns of the periodic table called?", "groups (families)", ["periods", "rows", "series"], "Columns = groups."),
    ("How is the modern periodic table ordered?", "by increasing atomic number", ["by increasing mass only", "alphabetically", "by color"], "Moseley's order by protons."),
    ("Why do noble gases rarely react?", "Their outer shells are full.", ["They have no electrons.", "They are metals.", "They are too heavy."], "Stable electron arrangement."),
    ("Where are metals found on the periodic table?", "on the left and in the middle", ["only on the right", "only at the top", "only in group 18"], "Most elements are metals."),
    ("Which property is typical of metals?", "shiny, good conductors of heat and electricity", ["dull and brittle", "poor conductors", "always gases"], "Metallic properties."),
    ("What is electronegativity?", "how strongly an atom attracts electrons in a bond", ["how many protons it has", "how big it is", "how fast it moves"], "Fluorine is highest."),
    ("What is ionization energy?", "the energy needed to remove an electron from an atom", ["the energy released by a reaction", "the mass of an ion", "the charge of an ion"], "Higher for nonmetals."),
])
B5 = bank([
    ("Mendeleev left gaps in his periodic table. Why?", "He predicted elements that had not been discovered yet.", ["He made mistakes.", "He ran out of space.", "Those elements were radioactive."],
     "Gallium and germanium filled them."),
    ("Sodium and potassium both react with water. What explains this?", "Both have 1 valence electron that is easy to lose.", ["Both are gases.", "Both have 8 valence electrons.", "Both are halogens."], "Group 1."),
    ("Why is fluorine the most reactive nonmetal?", "It is small and strongly attracts one more electron.", ["It is large.", "It has a full shell.", "It is a metal."], "High electronegativity."),
    ("A new element is found below francium in group 1. What would you predict?", "a very reactive metal that forms a +1 ion", ["a noble gas", "a nonmetal with a −1 charge", "an unreactive solid"], "Follow the group trend."),
    ("Why does atomic radius decrease across a period?", "More protons pull the same number of shells closer.", ["Atoms lose shells.", "Neutrons push electrons away.", "Electrons get heavier."], "Increasing nuclear charge."),
])


def body():
    think = ("<p><b>The periodic table is a map of outer electrons.</b></p>"
             "<ul><li>Groups (columns) share valence electrons, so they react alike. Periods (rows) = number of shells.</li>"
             "<li>Down a group: atoms get bigger; ionization energy and electronegativity go down.</li>"
             "<li>Across a period (left to right): atoms get smaller; ionization energy and electronegativity go up.</li></ul>")
    ex = [("Valence electrons in sulfur (group 16)?", ["16 − 10"], "6"),
          ("Larger atom: lithium or cesium (same group)?", ["Cesium has more shells"], "cesium")]
    mist = ["Thinking atoms get bigger from left to right.", "Mixing up groups (columns) and periods (rows).", "Thinking noble gases react easily."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Groups and periods", B1 + [(g_loc, 8), (g_class, 4)]),
        ("Families and valence electrons", [(g_fam, 10), (g_val, 6), (g_class, 4)]),
        ("Ion charges", [(g_val, 12), (g_loc, 4), (g_fam, 4)]),
        ("Periodic trends", [(g_trend, 14), (g_react, 6)]),
        ("Using the table to predict", B5 + [(g_table, 6), (g_trend, 5), (g_react, 4)]),
    ])
    make("chemistry", "periodic-table-and-trends", 2, "HS-PS1-1",
         "Use the periodic table as a model to predict the relative properties of elements based on the patterns of electrons in the outermost energy level of atoms.",
         "The Periodic Table and Periodic Trends",
         "Periodic Table Worksheets: Groups, Valence Electrons and Trends (High School Chemistry)",
         "Periodic Trends",
         "Free high school chemistry worksheets on the periodic table (NGSS HS-PS1-1): groups and periods, families, valence electrons, ion charges and trends in radius, ionization energy and electronegativity. 100 questions with answers.",
         "Outer electrons explain the table.",
         "Elements in a group react alike; size and pull on electrons follow clear trends.",
         body(),
         [("How do you find valence electrons from the periodic table?", "For groups 1 and 2, use the group number. For groups 13 to 18, subtract 10. Helium has 2."),
          ("What are the main periodic trends?", "Atomic radius increases down a group and decreases across a period. Ionization energy and electronegativity do the opposite."),
          ("Why do elements in the same group behave alike?", "They have the same number of valence electrons, and valence electrons control chemical reactions.")],
         sets)


if __name__ == "__main__":
    main()
