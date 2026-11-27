# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Physics (6091), Topic 17: Magnetism
  python tools/gen_sg_science_s4_magnetism.py
Properties of magnets (north and south poles, like poles repel, unlike poles attract); magnetic and non-magnetic materials;
induced magnetism; temporary (soft iron) and permanent (steel) magnets and their uses; magnetising with a solenoid and d.c.;
magnetic field lines around a bar magnet and between poles; plotting compasses; the Earth's magnetic field.
UK and US magnetism makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "all metals are magnetic", "field lines go from S to N outside a magnet", "attraction
proves an object is a magnet", "soft iron is used for permanent magnets".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 4, "Physics", 5
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_pick = src("gen_uk_science_y11_magnetism_and_electromagnetism", "g_pick")
uk_pole = src("gen_uk_science_y11_magnetism_and_electromagnetism", "g_pole")
us_lines = src("gen_us_science_phys_electric_and_magnetic_fields", "g_lines")
uk_field = src("gen_uk_science_y8_magnetism_and_electromagnets", "g_field")

MAG = [("iron", True), ("steel", True), ("nickel", True), ("cobalt", True), ("copper", False), ("aluminium", False), ("brass", False), ("gold", False),
       ("silver", False), ("lead", False), ("zinc", False), ("tin", False)]


def g_mag():
    if R.random() < 0.5:
        m, a = R.choice(MAG)
        return tq("Is %s a magnetic material?" % m, "Yes" if a else "No", ["No" if a else "Yes", "Only when it is heated", "Only in a liquid state"],
                  "The magnetic materials are iron, steel, nickel and cobalt (and their alloys). Most other metals are non-magnetic.")
    yes = [m for m, a in MAG if a]
    no = [m for m, a in MAG if not a]
    if R.random() < 0.5:
        a = R.choice(yes)
        return tq("Which of these is a magnetic material?", a, R.sample(no, 3), "Iron, steel, nickel and cobalt are magnetic.")
    a = R.choice(no)
    return tq("Which of these is NOT a magnetic material?", a, R.sample(yes, 3), "%s is not attracted by a magnet." % (a[0].upper() + a[1:]))


POLES = [("N", "N", "They repel."), ("S", "S", "They repel."), ("N", "S", "They attract."), ("S", "N", "They attract.")]


def g_poles():
    a, b, ans = R.choice(POLES)
    k = R.choice(["mag", "iron"])
    if k == "mag":
        return tq("The %s pole of one magnet is brought near the %s pole of another. What happens?" % (a, b), ans, ["They attract." if ans == "They repel." else "They repel.", "Nothing happens.", "They both lose their magnetism."],
                  "Like poles repel; unlike poles attract.")
    return tq("The %s pole of a magnet is brought near an unmagnetised iron nail. What happens?" % a, "The nail is attracted.", ["The nail is repelled.", "Nothing happens.", "The nail is attracted only to the S pole."],
              "The nail becomes an induced magnet with the opposite pole nearest, so it is attracted to either pole.")


TP = [("soft iron", "temporary", "easily magnetised and easily loses its magnetism"), ("steel", "permanent", "harder to magnetise but keeps its magnetism")]
USES = [("the core of an electromagnet", "soft iron"), ("a compass needle", "steel"), ("a fridge door magnet", "steel"), ("the core of a transformer", "soft iron"),
        ("the core of a relay or electric bell", "soft iron"), ("a magnet in a loudspeaker", "steel")]


def g_tp():
    k = R.choice(["use", "prop", "prop"])
    if k == "use":
        u, m = R.choice(USES)
        return tq("Which material is best for %s: soft iron or steel?" % u, m, ["soft iron" if m == "steel" else "steel", "copper", "aluminium"],
                  "Soft iron makes temporary magnets (easily magnetised and demagnetised); steel makes permanent magnets.")
    m, t, why = R.choice(TP)
    if R.random() < 0.5:
        return tq("Is %s used to make temporary or permanent magnets?" % m, "%s magnets" % t, ["%s magnets" % ("permanent" if t == "temporary" else "temporary"), "neither: it is non-magnetic", "only electromagnets"],
                  "%s is %s." % (m[0].upper() + m[1:], why))
    return tq("Which material is %s?" % why, m, ["steel" if m == "soft iron" else "soft iron", "copper", "brass"], "%s makes %s magnets." % (m[0].upper() + m[1:], t))


FIELDQ = [("In which direction do magnetic field lines point outside a bar magnet?", "from the north pole to the south pole", ["from the south pole to the north pole", "towards both poles", "in circles around the middle"]),
          ("Where is the magnetic field of a bar magnet strongest?", "near the poles, where the field lines are closest together", ["in the middle of the magnet", "far from the magnet", "the same everywhere"]),
          ("What is a magnetic field?", "a region in which a magnetic pole experiences a force", ["a region where electric charges feel a force", "the space inside a magnet only", "the path of an electric current"]),
          ("What does a plotting compass show when placed in a magnetic field?", "the direction of the field at that point", ["the strength of the field only", "the size of the magnet", "the charge on the magnet"]),
          ("Describe the field between two unlike poles (N facing S) placed close together.", "nearly straight, parallel lines from N to S: a nearly uniform field", ["no field between them", "lines curving away from each other", "circles around each pole"]),
          ("Describe the field between two like poles (N facing N).", "the lines push away from each other, leaving a neutral point midway with no field", ["straight lines from one N to the other", "a uniform field", "circles around the gap"]),
          ("What is a neutral point in a magnetic field?", "a point where the fields cancel, so the resultant field is zero", ["the middle of a magnet", "where the field is strongest", "a point with no magnets nearby"])]


def g_fieldq():
    q, a, w = R.choice(FIELDQ)
    return tq(q, a, w, "Field lines go from N to S outside a magnet; closer lines mean a stronger field.")


POOL1 = pool(R, [
    ("Which test shows that a metal bar is a magnet?", "One end repels a pole of a known magnet.", ["It attracts a known magnet.", "It attracts iron filings only.", "It feels cold."], "Repulsion is the only sure test."),
    ("What is induced magnetism?", "magnetism produced in a magnetic material when it is placed near a magnet", ["magnetism made by heating", "magnetism in copper", "the force between two currents"], "The nail becomes a magnet while near the magnet."),
    ("A freely suspended bar magnet comes to rest. Which way does its north pole point?", "towards the Earth's geographic north", ["towards the Earth's geographic south", "upwards", "east"], "It is a north-seeking pole."),
    ("Why does a compass needle point north?", "It lines up with the Earth's magnetic field.", ["The North Pole is made of iron.", "The Sun pulls it.", "It is attracted by the equator."], "The Earth behaves like a giant bar magnet."),
    ("How can a steel bar be magnetised using electricity?", "Place it inside a solenoid and pass a direct current through the coil.", ["Pass alternating current through the bar.", "Heat it in a flame.", "Hammer it while facing east-west."], "The field of the solenoid magnetises the steel."),
    ("How can a magnet be demagnetised?", "by heating it strongly or hammering it, or by slowly withdrawing it from a solenoid carrying alternating current", ["by passing a direct current through a solenoid around it", "by cooling it in a fridge", "by painting it"], "These disturb the alignment of the magnetic domains."),
    ("What are iron filings used for near a magnet?", "to show the pattern of the magnetic field", ["to measure the strength of the magnet in newtons", "to demagnetise it", "to charge it"], "They line up along the field lines."),
    ("Which statement about magnetic poles is correct?", "Every magnet has both a north and a south pole.", ["A magnet can have just a north pole.", "Cutting a magnet in half separates its poles.", "Poles are always in the middle."], "Cutting a magnet makes two smaller magnets."),
])
POOL5 = pool(R, [
    ("A magnet attracts both ends of a metal bar. What can you conclude?", "The bar is made of a magnetic material but is not a magnet.", ["The bar is a magnet.", "The bar is copper.", "The magnet is broken."], "A magnet would have one end repelled."),
    ("Why is a magnetic keeper (soft iron bar) placed across the poles of a horseshoe magnet in storage?", "It helps the magnet keep its magnetism for longer.", ["It makes the magnet stronger at once.", "It demagnetises the magnet.", "It stops rust."], "It completes the magnetic loop."),
    ("Why are electromagnets in scrapyard cranes made with soft iron cores?", "Soft iron loses its magnetism when the current is switched off, so the scrap can be dropped.", ["Soft iron stays magnetised.", "Soft iron is non-magnetic.", "Soft iron is lighter."], "A steel core would stay magnetised."),
    ("A paper clip hangs from a magnet. A second paper clip hangs from the first. Why?", "The first clip becomes an induced magnet and attracts the second.", ["Paper clips are always magnets.", "Static electricity holds them.", "Gravity is weaker."], "Induced magnetism."),
    ("Why should magnets not be dropped repeatedly on a hard floor?", "Hammering (impacts) can weaken a magnet.", ["They become stronger.", "They lose their poles one at a time.", "They become electrically charged."], "The domains lose alignment."),
    ("A plotting compass is placed east of a bar magnet's N pole (the magnet points north). Which way does the compass point?", "away from the N pole", ["towards the N pole", "towards geographic south always", "it spins round"], "Field lines leave the N pole."),
    ("Two bar magnets are placed with N facing S a short distance apart. Where is the field most uniform?", "in the gap between the poles", ["at the far ends", "behind each magnet", "everywhere outside"], "The lines are parallel there."),
    ("Which material would make the best container to shield an instrument from magnetic fields?", "soft iron", ["copper", "plastic", "aluminium"], "Field lines pass through the soft iron instead."),
])


def main():
    sets = U.sets([
        ("Magnets and magnetic materials", [POOL1, (g_mag, 6), (uk_pick, 4), (g_poles, 3)]),
        ("Poles and induced magnetism", [(g_poles, 6), (uk_pole, 5), (g_mag, 4), POOL1]),
        ("Temporary and permanent magnets", [(g_tp, 9), POOL1, (POOL5, 3), (uk_pick, 3)]),
        ("Magnetic fields", [(g_fieldq, 7), (us_lines, 5), (uk_field, 4), (POOL5, 4)]),
        ("Exam-style questions", [(POOL5, 8), (g_tp, 4), (uk_pick, 4), (g_fieldq, 2), (uk_pole, 2)]),
    ])
    make_ol(LV, SUBJ, "magnetism", SORT, "Magnetism",
            "State the properties of magnets; describe induced magnetism; distinguish between magnetic and non-magnetic materials; describe methods of magnetisation "
            "using a direct current in a solenoid and methods of demagnetisation; distinguish between the properties and uses of temporary (soft iron) and permanent "
            "(steel) magnets; draw the magnetic field pattern around a bar magnet and between two magnets, and describe the use of plotting compasses (summary of the "
            "Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Magnetism", "Magnetism",
            "Free Secondary 4 O-Level Physics worksheets on magnetism: magnetic poles, magnetic materials, induced magnetism, soft iron and steel, magnetisation and magnetic "
            "field patterns. 100 questions with answers.",
            "Like poles repel; unlike poles attract.", "Soft iron: temporary magnets. Steel: permanent magnets.",
            "<p><b>Every magnet has a north pole and a south pole.</b></p><ul>"
            "<li>Like poles repel, unlike poles attract. A magnet attracts magnetic materials (iron, steel, nickel, cobalt) by induced magnetism.</li>"
            "<li>Only repulsion proves that an object is a magnet.</li>"
            "<li>Soft iron is easily magnetised and demagnetised (temporary magnets, electromagnet cores); steel keeps its magnetism (permanent magnets).</li>"
            "<li>Field lines go from N to S outside the magnet and are closest at the poles. A plotting compass shows the field direction.</li></ul>",
            [("A bar is attracted by both poles of a magnet. Is it a magnet?", ["a magnet would repel one pole"], "No: it is a magnetic material"),
             ("Best core for a scrapyard electromagnet?", ["must lose magnetism when switched off"], "soft iron")],
            ["Thinking all metals are magnetic. Copper, aluminium and brass are not.", "Using attraction as proof that something is a magnet.",
             "Drawing field lines from S to N outside a magnet.", "Choosing steel for an electromagnet core."],
            [("Which materials are magnetic?", "Iron, steel, nickel and cobalt, and alloys containing them. Copper, aluminium, brass, gold and plastics are not magnetic."),
             ("What is the difference between soft iron and steel?", "Soft iron is magnetised and demagnetised easily, so it makes temporary magnets; steel is harder to magnetise but keeps its magnetism, so it makes permanent magnets."),
             ("How do you draw the field around a bar magnet?", "Draw lines leaving the north pole and curving round into the south pole, with arrows from N to S and lines closest together near the poles.")],
            sets)


if __name__ == "__main__":
    main()
