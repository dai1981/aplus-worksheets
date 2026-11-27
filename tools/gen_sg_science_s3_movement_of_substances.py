# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Biology (6093), Topic 2: Movement of Substances
  python tools/gen_sg_science_s3_movement_of_substances.py
Diffusion, osmosis (in terms of water potential and a partially permeable membrane) and active transport; effects of solutions on
plant and animal cells (turgid, flaccid, plasmolysed; swelling and bursting, crenation); percentage change in mass of plant tissue;
surface area to volume ratio; factors affecting the rate of diffusion.
UK KS4 transport makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "water moves to a higher water potential", "osmosis is the movement of solutes",
"plant cells burst in pure water", "active transport needs no energy", "a larger cube has a larger surface area to volume ratio".
"""
from sg_ol import OL, seed_of, make_ol, nq, tq, rows, pool, ex

LV, SUBJ, SORT = 3, "Biology", 20
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

uk_osm = src("gen_uk_science_y10_cell_structure_and_transport", "g_osm")
uk_move = src("gen_uk_science_y10_cell_structure_and_transport", "g_move")

DEF = [("diffusion", "the net movement of particles from a region of higher concentration to a region of lower concentration, down a concentration gradient"),
       ("osmosis", "the net movement of water molecules from a region of higher water potential to a region of lower water potential through a partially permeable membrane"),
       ("active transport", "the movement of particles against a concentration gradient, using energy from respiration")]
g_def = rows(R, DEF, "Which statement defines %s?", "Which process is this: %s?", extra=("the movement of solute particles through a fully permeable membrane",))

CELLS = [("a plant cell in pure water", "It becomes turgid: water enters, the vacuole swells and the cell wall stops it bursting."),
         ("a plant cell in a concentrated sugar solution", "It becomes plasmolysed: water leaves and the cell membrane pulls away from the cell wall."),
         ("a red blood cell in pure water", "It swells and bursts, because it has no cell wall."),
         ("a red blood cell in a concentrated salt solution", "It shrinks and becomes crenated (wrinkled)."),
         ("a plant cell in a solution with the same water potential as its cell sap", "There is no net movement of water, so it stays the same."),
         ("a red blood cell in blood plasma", "There is no net movement of water, so it keeps its normal shape.")]
g_cells = rows(R, CELLS, "What happens to %s?", "Which cell is described? “%s”")


def g_pct():
    m0 = R.choice([2.40, 2.50, 3.20, 4.00, 4.80, 5.00, 6.40, 8.00])
    pc = R.choice([-25, -20, -15, -12.5, -10, -5, 5, 10, 12.5, 15, 20, 25])
    m1 = round(m0 * (1 + pc / 100), 2)
    pc = round((m1 - m0) / m0 * 100, 1)
    if pc == 0:
        return None
    d = m1 - m0
    sgn = "+" if pc > 0 else "−"
    a = "%s%s%%" % (sgn, ex(abs(pc)))
    wr = ["%s%s%%" % ("−" if pc > 0 else "+", ex(abs(pc))), "%s%s%%" % (sgn, ex(round(abs(d) / m1 * 100, 1))), "%s%s%%" % (sgn, ex(round(abs(d), 2)))]
    if len({a} | set(wr)) < 4:
        return None
    return tq("A potato strip had a mass of %.2f g. After 30 minutes in a solution its mass was %.2f g. What is the percentage change in mass?" % (m0, m1), a, wr,
              "Percentage change = (final − initial) ÷ initial × 100 = %s%.2f ÷ %.2f × 100. %s" % ("" if d > 0 else "−", abs(d), m0,
               "Water entered by osmosis: the solution had a higher water potential." if d > 0 else "Water left by osmosis: the solution had a lower water potential."))


def g_sav():
    a, b, c = sorted(R.sample([1, 2, 3, 4, 5, 6, 8, 10], 1) * 3 if R.random() < 0.4 else [R.choice([1, 2, 4]), R.choice([2, 3, 4, 5]), R.choice([5, 6, 8, 10])])
    sa, v = 2 * (a * b + b * c + a * c), a * b * c
    shape = "a cube of agar with sides of %d cm" % a if a == b == c else "a block of agar measuring %d cm × %d cm × %d cm" % (a, b, c)
    return nq("What is the surface area to volume ratio of %s?" % shape, sa / v, [v / sa, sa, sa / v / 2], " : 1",
              "Surface area = %d cm²; volume = %d cm³; ratio = %d ÷ %d. Smaller blocks have a larger ratio." % (sa, v, sa, v))


def g_wp():
    x, y = sorted(R.sample([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0], 2))
    k = R.random() < 0.5
    a_, b_ = (x, y) if k else (y, x)
    to = "from A to B" if a_ < b_ else "from B to A"
    return tq("Two sucrose solutions are separated by a partially permeable membrane: A is %s mol/dm³ and B is %s mol/dm³. Which way does water move overall?" % (ex(a_), ex(b_)),
              to, [x_ for x_ in ("from A to B", "from B to A", "no net movement", "sucrose moves from B to A" if to == "from A to B" else "sucrose moves from A to B") if x_ != to],
              "The more dilute solution has the higher water potential; water moves by osmosis to the more concentrated solution.")


def g_strip():
    sap = R.choice([0.2, 0.3, 0.4, 0.5])
    c = R.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0])
    a = "It gains mass." if c < sap else ("It loses mass." if c > sap else "Its mass stays about the same.")
    return tq("The cell sap of a potato is equivalent to %s mol/dm³ sucrose. A strip is left in %s mol/dm³ sucrose. What happens to its mass?" % (ex(sap), ex(c)), a,
              [x for x in ("It gains mass.", "It loses mass.", "Its mass stays about the same.", "It dissolves.") if x != a],
              "Water moves from the higher water potential (more dilute) to the lower water potential (more concentrated).")


FACT = [("a steeper concentration gradient", "faster"), ("a higher temperature", "faster"), ("a larger surface area", "faster"),
        ("a thicker membrane (longer diffusion distance)", "slower"), ("a lower temperature", "slower"), ("a shallower concentration gradient", "slower"),
        ("a shorter diffusion distance", "faster")]


def g_fact():
    f, a = R.choice(FACT)
    return tq("How does %s affect the rate of diffusion?" % f, a, [x for x in ("faster", "slower", "no change", "diffusion stops") if x != a],
              "Diffusion is faster with a steeper gradient, larger surface area, higher temperature and a shorter distance.")


POOL1 = pool(R, [
    ("Water moves by osmosis from solution A to solution B. What does this tell you?", "A has a higher water potential than B.", ["A has a lower water potential than B.", "A has more solute than B.", "A and B have the same water potential."], "Water moves down a water potential gradient."),
    ("Which has the highest water potential?", "pure water", ["a dilute sugar solution", "a concentrated sugar solution", "a saturated salt solution"], "Adding solute lowers the water potential."),
    ("Why does active transport need energy?", "It moves substances against a concentration gradient.", ["It moves substances down a gradient.", "It moves only water.", "It happens only in dead cells."], "Energy comes from respiration in mitochondria."),
    ("Root hair cells absorb mineral ions from soil where the ions are less concentrated. Which process is used?", "active transport", ["diffusion", "osmosis", "transpiration"], "They have many mitochondria."),
    ("What is a partially permeable membrane?", "a membrane that lets small molecules such as water through but not larger solute molecules", ["a membrane that lets everything through", "a membrane that lets nothing through", "a cellulose cell wall"], "The cell membrane and Visking tubing are examples."),
    ("Why do plant cells not burst in pure water?", "The cell wall resists the pressure of the swelling vacuole.", ["Water cannot enter plant cells.", "The vacuole pumps water out.", "Plant cells have no membrane."], "The cell becomes turgid."),
    ("Why is turgidity important to a plant?", "It keeps the cells firm and supports non-woody parts such as leaves.", ["It stops photosynthesis.", "It lets the plant absorb sugar.", "It makes the cells divide."], "A plant that loses water wilts."),
    ("Which process moves oxygen from the alveoli into the blood?", "diffusion", ["osmosis", "active transport", "transpiration"], "Oxygen is more concentrated in the alveoli."),
    ("Why does a small organism not need a transport system?", "It has a large surface area to volume ratio, so diffusion is fast enough.", ["It needs no oxygen.", "It has a small surface area to volume ratio.", "It makes its own oxygen."], "Large organisms need lungs and blood."),
    ("Visking tubing filled with sugar solution is placed in water. What happens?", "Water enters by osmosis and the tubing swells.", ["Sugar leaves and the tubing shrinks.", "Nothing happens.", "Water leaves by osmosis."], "Sugar molecules are too large to pass through."),
])
POOL5 = pool(R, [
    ("Potato strips lose mass in 0.6 mol/dm³ sucrose and gain mass in 0.2 mol/dm³ sucrose. What is the likely concentration of the cell sap?", "between 0.2 and 0.6 mol/dm³", ["less than 0.2 mol/dm³", "more than 0.6 mol/dm³", "exactly 0 mol/dm³"], "No net change where the water potentials are equal."),
    ("Why is percentage change in mass used to compare potato strips?", "The strips may start with different masses.", ["It is quicker to calculate.", "The strips all start at 1 g.", "Mass cannot be measured directly."], "It allows a fair comparison."),
    ("Why are potato strips blotted dry before weighing?", "to remove surface solution so only the mass of the tissue is measured", ["to kill the cells", "to add water", "to stop osmosis completely"], "Excess liquid adds mass."),
    ("Why do fruit and vegetables kept in salt or sugar last longer?", "Bacteria lose water by osmosis and cannot grow.", ["Salt kills all enzymes.", "Sugar adds oxygen.", "Bacteria gain water and burst."], "Used to preserve salted fish and jam."),
    ("Why should a person not drink seawater when thirsty?", "Seawater has a lower water potential than body fluids, so cells lose water.", ["Seawater has no water potential.", "Seawater contains no water.", "Seawater has a higher water potential."], "The kidneys need extra water to remove the salt."),
    ("Agar cubes containing indicator are put in acid. The 1 cm cube changes colour faster than the 2 cm cube. Why?", "The smaller cube has a larger surface area to volume ratio and a shorter distance to the centre.", ["The smaller cube contains more indicator.", "The larger cube absorbs less acid in total.", "The acid is stronger near the small cube."], "Ratio: 6 : 1 versus 3 : 1."),
    ("Cyanide stops respiration. Which process in root hair cells would stop?", "active transport of mineral ions", ["osmosis of water", "diffusion of oxygen", "transpiration"], "Active transport needs energy from respiration."),
    ("A plant cell is plasmolysed. What fills the space between the cell wall and the membrane?", "the external solution", ["air", "cell sap", "cytoplasm"], "The cell wall is fully permeable."),
])


def main():
    sets = U.sets([
        ("Diffusion, osmosis and active transport", [(g_def, 3), (uk_move, 6), (POOL1, 6), (g_fact, 5)]),
        ("Osmosis and water potential", [(g_cells, 8), (POOL1, 3), (g_wp, 9)]),
        ("Potato strip experiments", [(g_pct, 8), (uk_osm, 5), (g_strip, 7)]),
        ("Surface area and rate of diffusion", [(g_sav, 10), (g_fact, 2), (g_cells, 2), (uk_move, 2), (POOL5, 2), (g_wp, 2)]),
        ("Exam-style questions", [(POOL5, 6), (uk_osm, 4), (g_pct, 5), (g_strip, 3), (g_sav, 2)]),
    ])
    make_ol(LV, SUBJ, "movement-of-substances", SORT, "Movement of Substances",
            "Define diffusion and describe its importance to living organisms; define osmosis in terms of water potential and a partially permeable membrane and "
            "describe the effects of solutions of different water potentials on plant and animal cells; define active transport and describe its importance, such "
            "as the uptake of mineral ions by root hair cells; relate surface area to volume ratio to the rate of diffusion (summary of the Singapore-Cambridge "
            "O-Level Biology 6093 syllabus).",
            "Movement of Substances", "Movement of substances",
            "Free Secondary 3 O-Level Biology worksheets on movement of substances: diffusion, osmosis, water potential, active transport, potato strip experiments and "
            "surface area to volume ratio. 100 questions with answers.",
            "Water moves from high to low water potential.", "Active transport goes against the gradient and needs energy.",
            "<p><b>Three ways substances move in and out of cells.</b></p><ul>"
            "<li>Diffusion: net movement from higher to lower concentration. No energy.</li>"
            "<li>Osmosis: water moves from higher to lower water potential through a partially permeable membrane. Pure water has the highest water potential.</li>"
            "<li>Active transport: against the concentration gradient, using energy from respiration.</li>"
            "<li>Percentage change in mass = (final − initial) ÷ initial × 100. Smaller objects have a larger surface area to volume ratio.</li></ul>",
            [("4.00 g potato becomes 3.60 g. % change?", ["(3.60 − 4.00) ÷ 4.00 × 100"], "−10%"),
             ("Red blood cell in pure water?", ["water enters by osmosis", "no cell wall"], "swells and bursts")],
            ["Saying water moves to a higher water potential.", "Calling osmosis the movement of solute.", "Saying plant cells burst in pure water.",
             "Dividing by the final mass in percentage change."],
            [("What is the difference between diffusion and osmosis?", "Diffusion is the net movement of any particles down a concentration gradient. Osmosis is only the movement of water, from a higher to a lower water potential, through a partially permeable membrane."),
             ("What happens to plant cells in a concentrated solution?", "Water leaves by osmosis, the vacuole shrinks and the membrane pulls away from the cell wall: the cell is plasmolysed."),
             ("Why does active transport need energy?", "It moves particles against their concentration gradient, so energy from respiration is needed.")],
            sets)


if __name__ == "__main__":
    main()
