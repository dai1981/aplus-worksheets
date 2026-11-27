# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Systems): Transport Systems in Living Things
  python tools/gen_sg_science_s2_transport_systems_in_living_things.py
Arteries, veins and capillaries; xylem (water and mineral salts) and phloem (food) in plants; why multicellular organisms need
transport systems; diffusion of digested food and oxygen in humans and of gases and mineral salts in plants; osmosis in root
hair cells; investigating xylem with dye; harmful effects of drug abuse on the transport system; ethical issues in heart
transplants.
Wrong answers come from real mistakes: "veins carry blood away from the heart", "xylem carries food", "all arteries carry
oxygenated blood to the lungs", "water enters roots by diffusion of salt".
"""
from sg_sci import item, bank, lesson, table
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64209)
R = U.R
P = People(R)
import re
import gen_sg_science_p5_plant_transport_system as PT
import gen_sg_science_p5_respiratory_and_circulatory_systems as RC
for _m in (PT, RC):
    _m.U, _m.R, _m.P = U, R, P
REP = [(r"the water-carrying tubes", "the xylem"), (r"the food-carrying tubes", "the phloem"), (r"water-carrying tubes", "xylem"), (r"food-carrying tubes", "phloem"),
       (r"the tiny openings on leaves", "the stomata"), (r"tiny openings", "stomata")]


def sec(f):
    def g():
        it = f()
        if not it:
            return None
        it = dict(it)
        fx = lambda t: [t := re.sub(a, b, t) for a, b in REP][-1]
        it["q"], it["e"] = fx(it["q"]), fx(it["e"])
        it["c"] = [fx(c) for c in it["c"]]
        return it if len({c.lower() for c in it["c"]}) == 4 else None
    g.__name__ = f.__name__
    return g


RING, DYE, LOSS, WHICH, CARRY, RATE, RECOV = [sec(x) for x in (PT.g_ring, PT.g_dye, PT.g_loss, PT.g_which, RC.g_carry, RC.g_rate, RC.g_recover)]

VES = [("artery", "carries blood away from the heart", "has a thick, muscular, elastic wall to withstand high pressure"),
       ("vein", "carries blood back to the heart", "has a thinner wall and valves to stop blood flowing backwards"),
       ("capillary", "carries blood through the tissues, where substances are exchanged with the cells", "has a wall only one cell thick")]


def g_ves():
    v, j, s = R.choice(VES)
    k = R.choice(["job", "str", "which", "whichs"])
    if not once(("vs", v, k)):
        return None
    art = "an " if v[0] == "a" else "a "
    if k == "job":
        return item("What does %s%s do?" % (art, v), "It " + j + ".", ["It " + x[1] + "." for x in VES if x[0] != v] + ["It makes red blood cells."], "%s%s %s." % (art.capitalize(), v, j))
    if k == "str":
        return item("Which describes %s%s?" % (art, v), "It " + s + ".", ["It " + x[2] + "." for x in VES if x[0] != v] + ["It has no wall at all."], "%s%s %s." % (art.capitalize(), v, s))
    if k == "which":
        return item("Which blood vessel %s?" % j, art + v, [("an " if x[0][0] == "a" else "a ") + x[0] for x in VES if x[0] != v] + ["a xylem vessel"], "%s%s %s." % (art.capitalize(), v, j))
    return item("Which blood vessel %s?" % s, art + v, [("an " if x[0][0] == "a" else "a ") + x[0] for x in VES if x[0] != v] + ["a phloem tube"], "%s%s %s." % (art.capitalize(), v, s))


PL = [("xylem", "transports water and mineral salts from the roots to the leaves"), ("phloem", "transports food (sugars) made in the leaves to other parts of the plant")]
PLQ = [("Water moves up from the roots to the leaves of a balsam plant.", "xylem"), ("Sugar made in the leaves is carried to the fruits of a durian tree.", "phloem"),
       ("Mineral salts absorbed by the roots reach the leaves.", "xylem"), ("Food made in the leaves is stored in the tubers of a tapioca plant.", "phloem"),
       ("Red dye rises up a celery stalk placed in red-coloured water.", "xylem"), ("A ring of bark is removed from a tree and the bark above the ring swells with sugar.", "phloem"),
       ("A rose in blue-coloured water develops blue streaks in its petals.", "xylem"), ("Sugars move from the leaves to the growing shoot tip.", "phloem")]


def g_pl():
    s, a = R.choice(PLQ)
    if not once(("pl", s)):
        return None
    o = "phloem" if a == "xylem" else "xylem"
    return item(s + " Which tissue is involved?", a, [o, "capillaries", "veins"], "Xylem %s; phloem %s." % (PL[0][1], PL[1][1]))


DIF = [("Oxygen moves from the air sacs in the lungs into the blood.", "diffusion"), ("Digested food moves from the small intestine into the blood.", "diffusion"),
       ("Oxygen moves from the blood in capillaries into body cells.", "diffusion"), ("Carbon dioxide moves from body cells into the blood.", "diffusion"),
       ("Water moves from the soil into a root hair cell.", "osmosis"), ("Carbon dioxide enters a leaf through the stomata.", "diffusion"),
       ("Water moves from cell to cell across a root towards the xylem.", "osmosis"), ("Mineral salts move into root hair cells from a higher concentration in the soil.", "diffusion")]


def g_dif():
    s, a = R.choice(DIF)
    if not once(("df", s)):
        return None
    return item(s + " Which process is this?", a, [x for x in ["diffusion", "osmosis", "photosynthesis", "respiration"] if x != a],
                "Diffusion: net movement of particles from a higher to a lower concentration. Osmosis: water moving through a partially permeable membrane.")


def g_sa():
    n = R.choice([1, 2, 3, 4, 5])
    k = R.choice(["sa", "vol", "ratio"])
    if not once(("sa", n, k)):
        return None
    sa, v = 6 * n * n, n ** 3
    tb = "A cube has sides of %d cm. " % n
    if k == "sa":
        return item(tb + "What is its surface area?", "%d cm²" % sa, ["%d cm²" % (4 * n * n), "%d cm²" % v, "%d cm²" % (6 * n)], "6 × %d × %d = %d cm²." % (n, n, sa))
    if k == "vol":
        return item(tb + "What is its volume?", "%d cm³" % v, ["%d cm³" % sa, "%d cm³" % (3 * n), "%d cm³" % (n * n)] if v != n * n else ["%d cm³" % sa, "%d cm³" % (3 * n), "%d cm³" % (n + 2)], "%d × %d × %d = %d cm³." % (n, n, n, v))
    r = sa / v
    rs = ("%g" % r) + " : 1"
    return item(tb + "What is its surface area to volume ratio?", rs, ["%g : 1" % (v / sa), "%g : 1" % (r * 2), "%g : 1" % (r + 1)],
                "%d ÷ %d = %g. Larger organisms have a smaller ratio, so they need a transport system." % (sa, v, r))


EXS = [("Oxygen enters the blood.", "the air sacs of the lungs"), ("Digested food enters the blood.", "the villi of the small intestine"),
       ("Water enters a plant.", "the root hair cells"), ("Carbon dioxide enters a leaf.", "the stomata of the leaf"),
       ("Oxygen and glucose pass from the blood to muscle cells.", "the capillaries in the muscles"), ("Water vapour leaves a plant.", "the stomata of the leaf")]


def g_ex():
    s, a = R.choice(EXS)
    if not once(("ex", s)):
        return None
    return item(s + " Where does this mainly happen?", a, R.sample(sorted({x[1] for x in EXS if x[1] != a}), 3), "Exchange surfaces are large and thin for fast diffusion.")


B1 = bank([
    ("Why do large multicellular organisms need a transport system?", "Diffusion alone is too slow to supply substances to cells deep inside a large body.", ["Their cells do not need oxygen.", "Diffusion is faster in large organisms.", "They have no cells."], "A small surface area to volume ratio makes diffusion too slow."),
    ("Why is a capillary wall only one cell thick?", "so that substances can diffuse quickly between the blood and the cells", ["to make it strong", "to stop blood flowing", "to store food"], "A short diffusion distance speeds up exchange."),
    ("Which blood vessels have valves?", "veins", ["arteries", "capillaries", "xylem vessels"], "Valves stop blood flowing backwards at low pressure."),
    ("How does water enter a root hair cell?", "by osmosis, from the soil water into the cell", ["by diffusion of salt", "through the leaves", "by photosynthesis"], "The root hair gives a large surface area."),
    ("Why are root hair cells long and thin?", "to give a large surface area for absorbing water and mineral salts", ["to make food", "to store sugar", "to carry messages"], "They have no chloroplasts."),
    ("What does the blood carry around the body?", "oxygen, digested food, carbon dioxide and other wastes", ["only water", "only oxygen", "only food"], "Blood is the transport medium in humans."),
    ("How can drug abuse harm the transport system?", "Some drugs raise blood pressure and heart rate and can damage the heart and blood vessels.", ["Drugs make the heart stronger.", "Drugs clean the arteries.", "Drugs have no effect on blood."], "Smoking also narrows arteries."),
    ("Which is an ethical issue in heart transplants?", "deciding who should receive a donated heart when there are not enough donors", ["choosing the colour of the heart", "how fast blood flows", "the size of capillaries"], "Consent from the donor or family is also important."),
])
B5 = bank([
    ("A student puts a balsam plant in red-coloured water. After a day, she cuts across the stem. Where is the red colour?", "in the xylem", ["in the phloem", "in the whole stem evenly", "in the roots only"], "Xylem carries water up the stem."),
    ("Why does the blood in an artery spurt out when it is cut, but blood in a vein flows out slowly?", "Blood in arteries is under much higher pressure.", ["Veins have thicker walls.", "Arteries have valves.", "Veins carry more blood."], "Arteries carry blood pumped by the heart."),
    ("Why do plants wilt if their roots are damaged?", "Less water can be absorbed and carried up the xylem.", ["The phloem carries too much water.", "The leaves make too much food.", "The stem becomes harder."], "Water keeps cells firm."),
    ("An amoeba is a single cell. Why does it not need a transport system?", "It has a large surface area to volume ratio, so diffusion is fast enough.", ["It does not need oxygen.", "It has blood vessels.", "It is a plant."], "Substances only need to travel a short distance."),
    ("A person's capillaries are damaged. Which process is most affected?", "the exchange of oxygen and food with body cells", ["the pumping of the heart", "the making of bile", "the chewing of food"], "Exchange happens across capillary walls."),
    ("Why are farmers told not to over-fertilise? Too much fertiliser in the soil can", "make the soil water more concentrated than the cell sap, so water leaves the roots by osmosis", ["make the plants grow forever", "turn xylem into phloem", "stop photosynthesis in animals"], "The plants may wilt."),
])


def body():
    think = ("<p><b>Large organisms need transport systems because diffusion alone is too slow.</b></p>"
             "<ul><li><b>Arteries</b> carry blood away from the heart (thick walls, high pressure). <b>Veins</b> carry blood back (valves). <b>Capillaries</b> are one cell thick for exchange.</li>"
             "<li><b>Xylem</b> carries water and mineral salts up from the roots. <b>Phloem</b> carries food (sugars) from the leaves.</li>"
             "<li>Oxygen and digested food reach cells by <b>diffusion</b>. Water enters root hairs by <b>osmosis</b>.</li>"
             "<li>Drug abuse can damage the heart and blood vessels.</li></ul>")
    ex = [("Which vessel carries blood back to the heart?", ["It has valves"], "a vein"),
          ("A celery stalk in red water: where does the red go?", ["Water travels up"], "the xylem")]
    mist = ["Saying veins carry blood away from the heart.", "Saying xylem carries food. Xylem carries water; phloem carries food.",
            "Thinking diffusion alone is enough for a large body.", "Saying water enters roots by diffusion of salt. It enters by osmosis."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Why we need transport systems", B1[:1] + B1[5:6] + [(g_sa, 8), (g_dif, 4), (g_ves, 4), (B1[1], 1)]),
        ("Blood vessels", B1[2:3] + [(g_ves, 8), (CARRY, 6), (RATE, 3), (g_dif, 2)]),
        ("Transport in plants", B1[3:5] + [(g_pl, 6), (WHICH, 4), (RING, 4), (DYE, 4)]),
        ("Diffusion and osmosis", [(g_dif, 6), (g_sa, 4), (g_pl, 2), (LOSS, 4), (RECOV, 3), (CARRY, 1), (g_ex, 3)]),
        ("Exam-style questions", B5 + B1[6:] + [(g_ves, 2), (DYE, 3), (RING, 2), (RATE, 3), (RECOV, 2), (g_ex, 2)]),
    ])
    make_lss(2, "transport-systems-in-living-things", 9, "Systems", "Transport Systems in Living Things",
             "Describe the functions of arteries, veins and capillaries and of xylem and phloem; explain the need for transport systems in multicellular organisms; explain how diffusion "
             "moves digested food and oxygen in humans and gases and mineral salts in plants, and that osmosis helps roots absorb water; recognise the harmful effects of drug abuse and "
             "ethical issues in heart transplants (summary of the MOE Lower Secondary Science Syllabus).",
             "Transport Systems in Living Things", seo(2, "Transport Systems in Humans and Plants"), "Transport systems",
             "Free Secondary 2 science worksheets for Singapore students on transport systems: arteries, veins and capillaries, xylem and phloem, diffusion, osmosis and surface area to volume ratio. With answers.",
             "Diffusion is too slow for a large body.", "Arteries away, veins back; xylem water, phloem food.",
             body(),
             [("What is the difference between arteries and veins?", "Arteries carry blood away from the heart at high pressure and have thick walls. Veins carry blood back to the heart and have valves."),
              ("What do xylem and phloem carry?", "Xylem carries water and mineral salts from the roots. Phloem carries food made in the leaves."),
              ("How does water enter a plant's roots?", "By osmosis, through the partially permeable membranes of root hair cells.")],
             sets)


if __name__ == "__main__":
    main()
