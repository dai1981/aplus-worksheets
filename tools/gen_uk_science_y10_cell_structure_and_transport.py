# -*- coding: utf-8 -*-
"""
UK Year 10 science (KS4, GCSE Combined Science Biology): Cell Structure and Transport
  python tools/gen_uk_science_y10_cell_structure_and_transport.py
Eukaryotic and prokaryotic cells, sub-cellular structures and their functions, microscopy and magnification
(image size ÷ real size, mm and µm), diffusion, osmosis (with potato-cylinder data) and active transport.
Reuses the organelle and microscope questions of the Year 7 unit (new seed).
Wrong answers come from real mistakes: "bacteria have a nucleus", "osmosis is the movement of solute",
"active transport needs no energy", "magnification = real size ÷ image size".
"""
from uk_sci import item, bank, table, once
from uk_ks4 import U4, build
from sci_phys import uniq

U, R, P, us = U4(62001)
y7_org, y7_where, y7_mic = us.uk("gen_uk_science_y7_cells", "g_org"), us.uk("gen_uk_science_y7_cells", "g_where"), us.uk("gen_uk_science_y7_cells", "g_mic")

FEAT = [("a nucleus", "eukaryotic cells only"), ("a cell membrane", "both"), ("cytoplasm", "both"), ("ribosomes", "both"), ("plasmids", "prokaryotic cells only"),
        ("a single loop of DNA free in the cytoplasm", "prokaryotic cells only"), ("mitochondria", "eukaryotic cells only"), ("chloroplasts", "some eukaryotic cells only (plants and algae)")]


def g_pro():
    f, a = R.choice(FEAT)
    if not once(("pr", f)):
        return None
    return item("Which cells contain %s?" % f, a, [x for x in ["eukaryotic cells only", "prokaryotic cells only", "both", "some eukaryotic cells only (plants and algae)", "neither"] if x != a][:3],
                "Prokaryotes (bacteria) have no nucleus: their DNA is a loop, with extra plasmids.")


def g_mag():
    k = R.choice(["M", "real", "image"])
    real_um = R.choice([2, 5, 10, 20, 25, 40, 50, 80, 100])
    m = R.choice([100, 200, 400, 500, 1000, 1500, 2000])
    img_mm = real_um * m / 1000
    if img_mm != int(img_mm) and img_mm * 10 != int(img_mm * 10) or img_mm > 100 or img_mm < 1 or not once(("mg", k, real_um, m)):
        return None
    im = ("%g" % img_mm)
    if k == "M":
        g = "×{:,}".format(m)
        return item("A cell is %d µm long. In a drawing it is %s mm long. What is the magnification? (1 mm = 1,000 µm)" % (real_um, im), g,
                    uniq(g, ["×{:,}".format(int(m / 1000)) if m >= 1000 else "×%g" % (m / 1000), "×{:,}".format(m * 10), "×%s" % im, "×{:,}".format(m // 10)]),
                    "Convert: %s mm = {:,} µm. Magnification = image ÷ real = {:,} ÷ %d = %d.".format(int(img_mm * 1000), int(img_mm * 1000)) % (im, real_um, m))
    if k == "real":
        g = "%d µm" % real_um
        return item("Under a magnification of ×{:,}, an image of a cell is %s mm long. What is the real length of the cell?".format(m) % im, g,
                    uniq(g, ["%g µm" % (img_mm * m), "%g mm" % (img_mm * m), "%g µm" % (real_um * 10), "%g µm" % (real_um / 10)]),
                    "Real size = image ÷ magnification = {:,} µm ÷ {:,} = %d µm.".format(int(img_mm * 1000), m) % real_um)
    g = "%s mm" % im
    return item("A cell %d µm long is viewed at ×{:,}. How long is the image in millimetres?".format(m) % real_um, g,
                uniq(g, ["{:,} mm".format(real_um * m), "%g mm" % (img_mm * 10), "%g mm" % (img_mm / 10), "%d mm" % real_um]), "Image = real × magnification = {:,} µm = %s mm.".format(real_um * m) % im)


MOVE = [("Oxygen moves from the alveoli into the blood.", "diffusion"), ("Water moves into a plant root hair cell from the soil.", "osmosis"),
        ("Mineral ions move into root hair cells from soil where they are less concentrated.", "active transport"), ("Carbon dioxide moves into a leaf through the stomata.", "diffusion"),
        ("Glucose is absorbed from the small intestine into the blood against a concentration gradient.", "active transport"), ("A red blood cell placed in pure water swells.", "osmosis"),
        ("Urea moves from cells into the blood plasma.", "diffusion"), ("Potato cells in strong sugar solution become flaccid.", "osmosis")]


def g_move():
    s, a = R.choice(MOVE)
    if not once(("mv", s)):
        return None
    return item("%s Which process is this?" % s, a, [x for x in ["diffusion", "osmosis", "active transport", "respiration"] if x != a],
                "Diffusion: particles from high to low concentration. Osmosis: water through a partially permeable membrane. Active transport: against the gradient, using energy.")


def g_osm():
    who = P.next()[0]
    conc = [0.0, 0.2, 0.4, 0.6, 0.8]
    cross = R.choice([0.2, 0.4])
    slope = R.choice([20, 25, 30])
    ch = [round(slope * (cross - c), 0) for c in conc]
    k = R.choice(["gain", "lose", "equal", "why", "pct"])
    if not once(("os", cross, slope, k)):
        return None
    tab = table(["Sugar solution (mol/dm³)", "Change in mass of potato (%)"], [["%g" % c, ("+" if v > 0 else ("−" if v < 0 else "")) + "%d" % abs(v)] for c, v in zip(conc, ch)])
    intro = tab + "%s left potato cylinders in sugar solutions for a day. " % who
    if k == "gain":
        return item(intro + "Why did the cylinder in pure water (0 mol/dm³) gain mass?", "Water moved into the potato cells by osmosis.", ["Sugar moved into the cells.", "The cells respired faster.", "Water moved out of the cells."], "Water moves from dilute to concentrated solution.")
    if k == "lose":
        return item(intro + "Why did the cylinder in 0.8 mol/dm³ solution lose mass?", "Water moved out of the cells by osmosis into the more concentrated solution.", ["Sugar moved out of the cells.", "The potato dissolved.", "Water moved into the cells."], "Osmosis out of the cells.")
    if k == "equal":
        g = "about %g mol/dm³" % cross
        return item(intro + "Estimate the concentration of the solution inside the potato cells.", g, ["about %g mol/dm³" % c for c in conc if c != cross][:3], "Where there is no change in mass, the concentrations are equal.")
    if k == "why":
        return item(intro + "Why is percentage change in mass used instead of change in mass?", "The cylinders may start with different masses, so percentages compare them fairly.", ["It is easier to measure.", "Mass cannot be measured.", "It makes the numbers bigger."], "Fair comparison.")
    m0 = R.choice([2.0, 2.5, 4.0, 5.0])
    m1 = round(m0 * (1 + ch[0] / 100), 2)
    g = "%+d%%" % ch[0]
    return item("A potato cylinder's mass went from %g g to %g g. What is the percentage change in mass?" % (m0, m1), g.replace("+", "+"),
                uniq(g, ["%+d%%" % (-ch[0]), "%g%%" % round(m1 - m0, 2), "%d%%" % round(m1 / m0 * 100), "%+d%%" % (ch[0] * 2)]), "(%g − %g) ÷ %g × 100 = %+d%%." % (m1, m0, m0, ch[0]))


B1 = bank([
    ("What is a eukaryotic cell?", "a cell with its genetic material inside a nucleus, such as animal and plant cells", ["a cell with no nucleus", "a bacterial cell", "a virus"], "Prokaryotes are bacteria."),
    ("How big is a typical bacterial cell compared with an animal cell?", "much smaller (about 1–10 µm compared with 10–100 µm)", ["much bigger", "the same size", "a million times bigger"], "Orders of magnitude."),
    ("What is the job of ribosomes?", "to make proteins", ["to release energy", "to control the cell", "to store water"], "Protein synthesis."),
    ("Why can an electron microscope show more detail than a light microscope?", "It has a much higher resolution and magnification.", ["It uses brighter light.", "It is bigger.", "It shows living cells in colour."], "Sub-cellular structures."),
    ("What are plasmids?", "small rings of DNA found in bacteria", ["the cell walls of plants", "energy stores", "types of ribosome"], "Used in genetic engineering."),
])
B5 = bank([
    ("Which factor does not increase the rate of diffusion?", "a smaller surface area", ["a bigger concentration gradient", "a higher temperature", "a larger surface area"], "Surface area, gradient and temperature."),
    ("Why do single-celled organisms not need transport systems?", "They have a large surface area to volume ratio, so diffusion is fast enough.", ["They do not need oxygen.", "They are too large.", "They have no membrane."], "Surface area : volume."),
    ("Why does active transport need energy?", "It moves substances against a concentration gradient.", ["It moves substances down the gradient.", "It only moves water.", "It happens outside cells."], "Energy from respiration."),
    ("Why do root hair cells have many mitochondria?", "to release energy for active transport of mineral ions", ["to photosynthesise", "to store starch", "to make the cell green"], "Specialised cells."),
    ("How are the villi in the small intestine adapted for absorption?", "a large surface area, thin walls and a good blood supply", ["thick walls and few capillaries", "no surface area", "cell walls of cellulose"], "Exchange surfaces."),
])

if __name__ == "__main__":
  build(U, 10, "cell-structure-and-transport", 1, "Biology", "Cell biology",
      "Cells as the basic structural unit of all organisms; similarities and differences between plant and animal cells; eukaryotic and prokaryotic cells; the function of sub-cellular structures; how specialised cells are adapted; the use of light and electron microscopes, magnification and resolution; the importance of cell differentiation; required processes of diffusion, osmosis and active transport across membranes.",
      "Cell Structure and Transport", "Cell Structure and Transport",
      "Free Year 10 GCSE Combined Science worksheets on cell structure and transport: eukaryotic and prokaryotic cells, microscopy and magnification, diffusion, osmosis and active transport. 100 questions with answers.",
      "Osmosis moves water; active transport needs energy.",
      "Magnification = image size ÷ real size; 1 mm = 1,000 µm.",
      "<p><b>All living things are made of cells.</b></p><ul><li>Eukaryotic cells have a nucleus; prokaryotic cells (bacteria) have a loop of DNA and plasmids instead.</li>"
      "<li>Magnification = image size ÷ real size. Convert to the same units first (1 mm = 1,000 µm).</li>"
      "<li>Diffusion: particles from high to low concentration. Osmosis: water across a partially permeable membrane. Active transport: against the gradient, using energy from respiration.</li></ul>",
      [("Image 5 mm, cell 25 µm. Magnification?", ["5 mm = 5,000 µm", "5,000 ÷ 25"], "×200"), ("Mineral ions into a root against the gradient?", ["Needs energy"], "active transport")],
      ["Thinking bacteria have a nucleus.", "Dividing real size by image size.", "Thinking osmosis moves solute particles."],
      [("What is the difference between eukaryotic and prokaryotic cells?", "Eukaryotic cells (animals, plants, fungi) keep their DNA in a nucleus. Prokaryotic cells (bacteria) are smaller, with a single loop of DNA and small rings called plasmids."),
       ("How do you calculate magnification?", "Magnification = image size ÷ real size, with both in the same units. Remember 1 mm = 1,000 µm."),
       ("What is the difference between diffusion, osmosis and active transport?", "Diffusion moves particles from high to low concentration. Osmosis is the diffusion of water across a partially permeable membrane. Active transport moves substances against a concentration gradient and needs energy.")],
      [("Cells", B1 + [(g_pro, 7), (y7_org, 5), (y7_where, 3)]),
       ("Microscopy", [(g_mag, 14), (y7_mic, 6)]),
       ("Diffusion and osmosis", [(g_move, 7), (g_osm, 13)]),
       ("Potato osmosis practical", [(g_osm, 10), (g_mag, 6), (y7_org, 4)]),
       ("Exchange surfaces", B5 + [(g_mag, 8), (g_osm, 2)])])
