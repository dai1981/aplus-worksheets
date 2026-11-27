# -*- coding: utf-8 -*-
"""Ontario Grade 10 science: SNC2D Academic (2008). Built with caon_hs."""
from caon_hs import HU

G = "gen_us_science_"

ADAPT = [
    ("Which action is mitigation of climate change (reducing its cause)?", "replacing coal power with wind and solar power", ["building sea walls", "planting heat-tolerant crops", "setting up cooling centres in heat waves"], "Mitigation cuts greenhouse gas emissions; adaptation prepares for the effects."),
    ("Which action is adaptation to climate change?", "designing storm sewers for heavier rainfall", ["using electric buses", "insulating homes to burn less gas", "capturing methane from landfills"], "Adaptation reduces the damage from changes that are already happening."),
    ("What is the purpose of the Paris Agreement?", "to keep global warming well below 2 °C above pre-industrial levels", ["to ban all cars by next year", "to stop the ozone hole", "to measure earthquakes"], "Countries set their own targets for cutting emissions."),
    ("What does carbon pricing do?", "it puts a cost on greenhouse gas emissions so that cleaner choices become cheaper", ["it pays people to burn more fuel", "it removes carbon from the ocean", "it bans all fossil fuels at once"], "A price signal encourages lower-emission products and technology."),
    ("Why is a heat wave more dangerous in a city than in the countryside?", "pavement and buildings absorb heat and cities stay warmer at night (the urban heat island)", ["cities are closer to the Sun", "cities have more snow", "there is no air in cities"], "Trees, green roofs and light-coloured surfaces can cool a city."),
    ("Why are many Canadian winter roads in the North open for fewer days than before?", "warmer winters make the ice thinner and the season shorter", ["the snow is too deep", "the roads are closed for repairs", "there is less traffic"], "Ice roads link many remote communities to supplies."),
    ("How does climate change increase the risk of forest fires in Canada?", "hotter, drier summers dry out trees and soil and lengthen the fire season", ["it makes forests wetter", "it stops lightning", "it removes oxygen from the air"], "Recent fire seasons in Canada have burned record areas."),
    ("Which change in Canada's oceans is caused by extra carbon dioxide?", "ocean acidification, which makes it harder for shellfish to build shells", ["the oceans becoming fresh water", "tides stopping", "the oceans turning alkaline"], "CO₂ dissolves to form carbonic acid, lowering the pH of sea water."),
    ("What is a carbon capture and storage system?", "technology that traps CO₂ from a factory or power plant and stores it underground", ["a tree nursery", "a solar panel", "a car's exhaust pipe"], "It stops some CO₂ from reaching the atmosphere."),
    ("Which personal choice cuts household greenhouse gas emissions?", "improving insulation and using a heat pump", ["leaving lights on", "using a gas-powered leaf blower", "keeping the furnace at a higher setting"], "Heating is a large part of energy use in Canadian homes."),
    ("Why are scientists concerned about melting glaciers in the Rocky Mountains?", "they supply rivers in summer, so less ice means less water later in the year", ["they stop earthquakes", "they keep the ocean salty", "they block the wind"], "Glacier meltwater feeds rivers used for drinking water, farms and hydroelectricity."),
    ("What is a climate model?", "a computer simulation that uses physics and data to predict future climate", ["a list of weather records", "a thermometer outside a school", "a map of countries"], "Models are tested by checking how well they reproduce the past climate."),
    ("Why do scientists use ice cores to study past climate?", "air bubbles and layers in the ice record past temperatures and CO₂ levels", ["ice cores show future weather", "ice cores contain fossils of dinosaurs", "ice cores measure earthquakes"], "Ice cores from Antarctica go back about 800 000 years."),
    ("Which change shows that a warmer climate affects living things?", "spring flowers blooming and birds migrating earlier than in the past", ["the number of days in a year changing", "the Moon's phases changing", "the speed of light changing"], "These are called phenology changes."),
    ("Why do warmer winters help the mountain pine beetle spread?", "fewer beetles are killed by extreme cold", ["the beetles need snow to survive", "warm weather makes trees grow faster", "the beetles eat ice"], "The beetle has killed large areas of pine forest in western Canada."),
    ("What is the difference between mitigation and adaptation?", "mitigation reduces the cause of climate change; adaptation reduces its harm", ["they mean the same thing", "mitigation only happens in cities", "adaptation means doing nothing"], "Both are needed."),
]

EYE = [
    ("Which part of the eye focuses light onto the retina?", "the lens (with help from the cornea)", ["the pupil", "the iris", "the optic nerve"], "The cornea does most of the bending; the lens adjusts the focus."),
    ("What does the iris do?", "it controls the size of the pupil and so how much light enters", ["it focuses the image", "it detects colour", "it carries signals to the brain"], "In bright light the pupil gets smaller."),
    ("Where is the image formed in a healthy eye?", "on the retina", ["on the cornea", "on the lens", "in the pupil"], "The image on the retina is real and upside down; the brain turns it the right way up."),
    ("A person who is near-sighted (myopia) needs which lens?", "a diverging (concave) lens", ["a converging (convex) lens", "a plane mirror", "a prism"], "Myopia focuses light in front of the retina; a diverging lens moves the focus back."),
    ("A person who is far-sighted (hyperopia) needs which lens?", "a converging (convex) lens", ["a diverging (concave) lens", "a coloured filter", "a plane mirror"], "The focus is behind the retina; a converging lens moves it forward."),
    ("Which device uses a converging lens to make a real image on a sensor?", "a camera", ["a periscope", "a car's side mirror", "a kaleidoscope"], "Like the eye, a camera focuses a real, inverted image."),
    ("Which device uses two converging lenses to see very small objects?", "a compound microscope", ["a magnifying mirror", "a periscope", "a car headlight"], "The objective lens makes a real image that the eyepiece magnifies."),
    ("What does laser eye surgery change?", "the shape of the cornea, so light focuses on the retina", ["the colour of the iris", "the length of the optic nerve", "the size of the pupil"], "Reshaping the cornea changes how much it bends light."),
    ("Which type of lens is a magnifying glass?", "a converging lens", ["a diverging lens", "a plane lens", "a concave mirror"], "An object inside the focal length gives an upright, enlarged virtual image."),
    ("Why do optical fibres carry light around corners?", "light reflects totally inside the fibre again and again", ["light bends because of gravity", "the fibre makes its own light", "light slows down to zero"], "Total internal reflection traps the light in the core."),
    ("What is the image in a camera or the eye like?", "real and inverted", ["virtual and upright", "virtual and inverted", "real and upright"], "Real images can be focused on a screen or sensor."),
    ("What is the blind spot of the eye?", "the place where the optic nerve leaves the retina, with no light receptors", ["the centre of the lens", "the coloured part of the eye", "the front of the cornea"], "We do not notice it because the brain fills in the gap."),
]


ACIDRAIN = [
    ("Which gases cause acid precipitation?", "sulfur dioxide and nitrogen oxides", ["oxygen and nitrogen", "carbon monoxide and helium", "argon and neon"], "They react with water in the air to form sulfuric and nitric acids."),
    ("Normal rain has a pH of about 5.6. Why is it slightly acidic?", "carbon dioxide dissolves in rainwater to form a weak acid", ["rain contains vinegar", "rain picks up salt from the ocean", "lightning makes rain basic"], "Carbonic acid gives clean rain a pH near 5.6; acid rain is below that."),
    ("Rain samples have these pH values: 5.6, 4.2, 5.5, 6.0. Which sample is the most acidic?", "4.2", ["5.6", "5.5", "6.0"], "The lower the pH, the more acidic the sample."),
    ("Why are lakes on the Canadian Shield easily harmed by acid rain?", "the granite bedrock has little limestone to neutralize the acid", ["they are too deep", "they freeze every winter", "they contain salt water"], "Lakes on limestone are buffered; lakes on granite are not."),
    ("How can lime help a lake damaged by acid rain?", "calcium carbonate neutralizes the acid and raises the pH", ["it makes the water colder", "it adds oxygen to the water", "it kills the algae"], "Liming is a short-term fix; cutting emissions is the long-term solution."),
    ("Which technology on a coal-burning power plant reduces acid rain?", "scrubbers that remove sulfur dioxide from the exhaust", ["taller chimneys only", "solar panels on the roof", "painting the chimney white"], "Scrubbers spray a base such as limestone slurry through the exhaust gases."),
    ("What does acid rain do to marble and limestone statues?", "it reacts with the calcium carbonate and slowly dissolves them", ["it makes them harder", "it turns them into metal", "it has no effect on stone"], "CaCO₃ + acid → salt + water + carbon dioxide."),
    ("Which source releases most nitrogen oxides in cities?", "car and truck engines", ["trees", "lakes", "solar panels"], "High temperatures in engines make nitrogen and oxygen in air react."),
    ("Why can acid rain harm fish?", "low pH damages their gills and releases toxic aluminum from the soil into the water", ["it makes the water too salty", "it raises the water temperature", "it adds too much oxygen"], "Many fish eggs cannot hatch below about pH 5."),
    ("Why did acid rain in Ontario decrease after the 1980s?", "laws in Canada and the United States cut sulfur dioxide emissions from smelters and power plants", ["it stopped raining", "lakes became saltier", "people stopped using electricity"], "Sudbury's smelters and power plants added controls and taller stacks with scrubbers."),
    ("A lake's pH drops from 6.5 to 4.5. How many times more acidic is it?", "100 times", ["2 times", "20 times", "1000 times"], "Each pH unit is a factor of 10, so two units is 10 × 10 = 100."),
    ("How does acid rain harm forests?", "it washes nutrients out of the soil and damages leaves and needles", ["it adds extra nitrogen that makes trees taller", "it makes the soil basic", "it protects trees from insects"], "Weakened trees are more easily hurt by cold, pests and disease."),
]


def optics(kind):
    """mirror and lens equation, Ontario convention: 1/f = 1/do + 1/di, real is positive, M = −di/do = hi/ho"""
    def factory(R):
        from au_sci import nq

        def g():
            it = g1()
            if it:
                it["e"] = it["e"].replace("-", "−")
            return it

        def g1():
            dev = R.choice(["concave mirror", "convex mirror"] if kind == "mirror" else ["converging lens", "diverging lens"])
            neg = dev in ("convex mirror", "diverging lens")
            f = R.choice([5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0])
            fs = -f if neg else f
            do = R.choice([6, 9, 12, 15, 18, 20, 24, 30, 36, 40, 45, 50, 60])
            if abs(do - f) < 1:
                return None
            di = 1 / (1 / fs - 1 / do)
            M = -di / do
            k = R.choice(["di", "di", "M", "hi", "f"])
            fs_txt = ("−%g" % f) if neg else ("%g" % f)
            where = "in front of the mirror" if kind == "mirror" else "from the lens"
            if k == "di":
                q = "An object is %d cm %s a %s with a focal length of %s cm. Use 1/f = 1/d₀ + 1/dᵢ to find the image distance dᵢ." % (do, where if kind == "lens" else "in front of", dev, fs_txt)
                q = q.replace("cm in front of a", "cm in front of a").replace("cm from the lens a", "cm from a")
                e = "1/dᵢ = 1/f − 1/d₀ = 1/(%s) − 1/%d, so dᵢ = <b>%.3g cm</b>. %s" % (fs_txt, do, di, "A positive dᵢ is a real image." if di > 0 else "A negative dᵢ is a virtual image.")
                return nq(q, di, [1 / (1 / fs + 1 / do), -di, do - fs], " cm", e)
            if k == "M":
                q = "A %s (f = %s cm) forms an image of an object placed %d cm away. What is the magnification? (M = −dᵢ/d₀)" % (dev, fs_txt, do)
                e = "dᵢ = %.3g cm, so M = −dᵢ/d₀ = −(%.3g) ÷ %d = <b>%.3g</b>. %s" % (di, di, do, M, "M is negative: the image is inverted." if M < 0 else "M is positive: the image is upright.")
                return nq(q, M, [-M, do / di if di else 2, di / do + 1], "", e)
            if k == "hi":
                ho = R.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0])
                hi = M * ho
                q = "An object %g cm tall is %d cm from a %s (f = %s cm). How tall is the image? (A negative height means inverted.)" % (ho, do, dev, fs_txt)
                e = "dᵢ = %.3g cm, M = −dᵢ/d₀ = %.3g, so hᵢ = M × h₀ = <b>%.3g cm</b>." % (di, M, hi)
                return nq(q, hi, [-hi, ho * do / di if di else ho * 2, ho], " cm", e)
            q = "A %s forms an image %.3g cm %s when the object is %d cm away. What is the focal length?" % (
                dev, abs(di), ("behind the mirror (virtual)" if di < 0 else "in front of the mirror (real)") if kind == "mirror" else ("on the same side as the object (virtual)" if di < 0 else "on the other side (real)"), do)
            e = "With dᵢ = %.3g cm: 1/f = 1/%d + 1/(%.3g), so f = <b>%.3g cm</b>." % (di, do, di, fs)
            return nq(q, fs, [-fs, do + di, 1 / (1 / do - 1 / di) if abs(do - di) > 0.01 else fs * 2], " cm", e)
        g.__name__ = "optics_" + kind
        return g
    return factory


def UNITS():
    return [
        HU("SNC2D", "B", 1, "cells-and-cell-division", "B3.1, B3.2, B3.3",
           "Animal and plant cell structure and the functions of organelles; the cell cycle and mitosis; the importance of cell division for growth and repair; "
           "cancer as uncontrolled cell division; stem cells and cell specialization; and using a microscope.",
           "Cells and Cell Division", "cells and cell division",
           "Free Grade 10 Science (SNC2D) worksheets on cells and cell division: organelles, microscopes and magnification, the cell cycle, the stages of mitosis, cancer and stem cells. 100 questions with answers.",
           "Mitosis makes two identical cells for growth and repair.", "Prophase, metaphase, anaphase, telophase, then cytokinesis.",
           "<p>Animal and plant cells both have a nucleus (DNA), cytoplasm, a cell membrane, mitochondria (respiration) and ribosomes. "
           "Plant cells also have a cell wall, chloroplasts and a large central vacuole. Magnification = image size ÷ actual size.</p>"
           "<p>In the cell cycle, the cell grows and copies its DNA in interphase, then divides in mitosis: prophase (chromosomes condense), metaphase (they line up), anaphase (chromatids separate), "
           "telophase (two nuclei form), followed by cytokinesis. Cancer is cell division that is no longer controlled. Stem cells are unspecialized cells that can become many kinds of cells.</p>",
           [("A cell is 0.02 mm across. Its image is 10 mm. Magnification?", ["10 ÷ 0.02"], "×500"),
            ("In which stage do chromosomes line up across the middle?", ["Think 'M' for middle."], "metaphase")],
           ["Saying mitosis halves the chromosome number: it keeps it the same.", "Forgetting that plant cells also have mitochondria.", "Mixing up the cell membrane and the cell wall."],
           [("Why is the cell cycle checked at checkpoints?", "So that damaged DNA is repaired or the cell is destroyed before it divides; failures can lead to cancer."),
            ("Where are stem cells found?", "In embryos and in some adult tissues such as bone marrow.")],
           lambda X: [
               ("Cell structure", [(X.gen("gen_uk_science_y10_cell_structure_and_transport", "g_pro"), 6), (X.ch("al_bio", "cells-and-the-immune-system", 1, 12), 8), (X.gen(G + "g6_parts_of_a_cell", "g_job"), 6)]),
               ("Microscopes and magnification", [(X.ch("al_bio", "cells-and-the-immune-system", 2, 12), 8), (X.gen("gen_uk_science_y10_cell_structure_and_transport", "g_mag"), 6), (X.gen(G + "g6_cells_and_cell_theory", "g_mag"), 6)]),
               ("The cell cycle", [(X.gen(G + "bio_cell_division_and_differentiation", "g_phase"), 6), (X.gen(G + "bio_cell_division_and_differentiation", "g_order"), 5), (X.ch("in_s11b", "cell-cycle-and-cell-division", 1), 9)]),
               ("Mitosis", [(X.ch("in_s11b", "cell-cycle-and-cell-division", 2), 10), (X.gen(G + "bio_cell_division_and_differentiation", "g_chrom"), 5), (X.gen(G + "bio_cell_division_and_differentiation", "g_count"), 5)]),
               ("Cancer, stem cells and specialization", [(X.gen("gen_uk_science_y10_cell_division", "g_stem"), 5), (X.gen("gen_uk_science_y10_cell_division", "g_use"), 4), (X.gen(G + "bio_cell_division_and_differentiation", "g_diff"), 5), (X.ch("al_bio", "gene-expression-and-biotechnology", 1, 13), 6)]),
           ]),
        HU("SNC2D", "B", 2, "tissues-organs-and-systems", "B3.4, B3.5, B3.6",
           "Specialized cells and the four types of animal tissue; organs and organ systems (digestive, respiratory, circulatory) and how they interact; "
           "plant tissues, organs and systems; and medical technologies.",
           "Tissues, Organs and Systems", "tissues, organs and systems",
           "Free Grade 10 Science (SNC2D) worksheets on tissues, organs and systems: specialized cells, levels of organization, the digestive, respiratory and circulatory systems, and plant tissues. 100 questions with answers.",
           "Cell → tissue → organ → organ system → organism.", "Organ systems work together to keep the body alive.",
           "<p>Cells with the same job form a tissue. Animals have four tissue types: epithelial (covers), connective (supports, such as bone and blood), muscle (moves) and nerve (signals). "
           "Tissues form organs such as the stomach, and organs work together in systems.</p>"
           "<p>The digestive system breaks food down and absorbs nutrients; the respiratory system takes in oxygen and removes carbon dioxide; the circulatory system carries them around the body. "
           "Plants have dermal, ground and vascular tissue; their organs are roots, stems, leaves and flowers, organized into the root system and the shoot system.</p>",
           [("Put in order: organ, cell, organ system, tissue.", ["Smallest first"], "cell, tissue, organ, organ system"),
            ("Which two systems work together to get oxygen to the muscles?", ["One takes in oxygen, one carries it."], "respiratory and circulatory")],
           ["Calling blood an organ: it is a connective tissue.", "Thinking organ systems work alone.", "Saying plants have no tissues."],
           [("Why are red blood cells specialized?", "They have no nucleus and are full of hemoglobin, so they carry as much oxygen as possible."),
            ("What does xylem tissue do?", "It carries water and minerals from the roots to the leaves.")],
           lambda X: [
               ("Specialized cells and tissues", [(X.gen("gen_sg_science_s3_cell_structure_and_organisation", "g_spec"), 6), (X.gen("gen_sg_science_s3_cell_structure_and_organisation", "g_level"), 4), (X.ch("in_s11b", "structural-organisation-in-animals", 1), 5), (X.ch("in_s11b", "structural-organisation-in-animals", 3), 5)]),
               ("Organs and organ systems", [(X.gen(G + "bio_levels_of_organization", "g_level"), 5), (X.gen(G + "bio_levels_of_organization", "g_order"), 4), (X.gen(G + "bio_levels_of_organization", "g_sys"), 5), (X.gen(G + "bio_levels_of_organization", "g_inter"), 3), (X.gen(G + "g6_body_systems", "g_job"), 3)]),
               ("The digestive and respiratory systems", [(X.gen("gen_sg_science_s2_human_digestive_system", "g_org"), 4), (X.gen("gen_sg_science_s2_human_digestive_system", "g_dig"), 4), (X.gen("gen_uk_science_y8_breathing_and_gas_exchange", "g_path"), 4), (X.gen("gen_uk_science_y8_breathing_and_gas_exchange", "g_job"), 4), (X.gen("gen_uk_science_y8_food_and_digestion", "g_enz"), 4)]),
               ("The circulatory system", [(X.gen("gen_sg_science_s3_transport_in_humans", "g_ves"), 6), (X.gen("gen_sg_science_s3_transport_in_humans", "g_hr"), 5), (X.gen("gen_sg_science_s3_transport_in_humans", "g_route"), 5), (X.gen("gen_sg_science_s2_transport_systems_in_living_things", "g_ves"), 4)]),
               ("Plant tissues and organs", [(X.gen("gen_sg_science_s2_transport_systems_in_living_things", "g_pl"), 5), (X.ch("in_s11b", "anatomy-of-flowering-plants", 1), 7), (X.gen("gen_sg_science_s3_nutrition_and_transport_in_flowering_plants", "g_xp"), 4), (X.gen("gen_uk_science_y8_photosynthesis", "g_leafad"), 4)]),
           ]),
        HU("SNC2D", "C", 3, "chemical-reactions-and-equations", "C3.1, C3.2, C3.3, C3.4",
           "Naming and writing formulas for ionic and molecular compounds; word, skeleton and balanced chemical equations; the law of conservation of mass; "
           "and the four main types of reaction: synthesis, decomposition, single displacement and double displacement.",
           "Chemical Reactions and Equations", "chemical reactions and equations",
           "Free Grade 10 Science (SNC2D) worksheets on chemical reactions: naming compounds, writing formulas, word and skeleton equations, balancing equations, conservation of mass and types of reactions. 100 questions with answers.",
           "Mass is conserved: the atoms on each side of an equation must match.", "Synthesis, decomposition, single and double displacement.",
           "<p>Name ionic compounds metal first, then the non-metal ending in -ide (sodium chloride, NaCl). Cross the ion charges to write formulas (Al³⁺ and O²⁻ give Al₂O₃). "
           "Molecular compounds use prefixes: carbon dioxide (CO₂), dinitrogen tetroxide (N₂O₄).</p>"
           "<p>A word equation names the substances; a skeleton equation uses formulas; a balanced equation adds coefficients so atoms are conserved. "
           "The four types are synthesis (A + B → AB), decomposition (AB → A + B), single displacement (A + BC → AC + B) and double displacement (AB + CD → AD + CB).</p>",
           [("Formula of calcium chloride?", ["Ca²⁺ and Cl⁻", "Two Cl⁻ for each Ca²⁺"], "CaCl₂"),
            ("Balance: Na + Cl₂ → NaCl", ["2 Cl on the left, so 2 NaCl", "Then 2 Na"], "2Na + Cl₂ → 2NaCl")],
           ["Using prefixes for ionic compounds (it is calcium chloride, not calcium dichloride).", "Changing subscripts to balance an equation.", "Forgetting that oxygen, hydrogen and chlorine gases are diatomic."],
           [("What is the law of conservation of mass?", "In a chemical reaction the total mass of the reactants equals the total mass of the products."),
            ("Why does a burning candle seem to lose mass?", "Gases (carbon dioxide and water vapour) escape into the air; in a closed container the mass stays the same.")],
           lambda X: [
               ("Names and formulas", [(X.gen(G + "chem_chemical_bonding", "g_name"), 7), (X.gen(G + "chem_chemical_bonding", "g_formula"), 6), (X.gen("gen_sg_science_s3_chemical_bonding_and_structure", "g_formula"), 7)]),
               ("Word and skeleton equations", [(X.gen(G + "g7_conservation_of_atoms", "g_balanced"), 6), (X.gen(G + "g7_conservation_of_atoms", "g_missing"), 6), (X.gen(G + "chem_balancing_chemical_equations", "g_count"), 8)]),
               ("Balancing equations", [(X.gen(G + "chem_balancing_chemical_equations", "g_check"), 6), (X.gen(G + "chem_balancing_chemical_equations", "g_pick"), 7), (X.gen(G + "chem_balancing_chemical_equations", "g_missing"), 7)]),
               ("Types of reactions", [(X.gen(G + "chem_types_of_chemical_reactions", "g_type"), 10), (X.gen(G + "chem_types_of_chemical_reactions", "g_prod"), 6), (X.gen("gen_sg_science_s2_chemical_changes", "g_type"), 4)]),
               ("Conservation of mass", [(X.gen(G + "chem_balancing_chemical_equations", "g_mass"), 7), (X.gen(G + "g7_conservation_of_atoms", "g_mass"), 6), (X.gen("gen_sg_science_s2_chemical_changes", "g_mass"), 4), (X.gen("gen_uk_science_y8_chemical_reactions", "g_cons"), 3)]),
           ]),
        HU("SNC2D", "C", 4, "acids-and-bases", "C3.5, C3.6, C3.7",
           "The properties of acids and bases; the pH scale and indicators; neutralization; reactions of acids with metals and carbonates; "
           "and acids and bases in the environment, including acid precipitation.",
           "Acids and Bases", "acids and bases",
           "Free Grade 10 Science (SNC2D) worksheets on acids and bases: properties, the pH scale, indicators, neutralization, salts, reactions with metals and carbonates, and acid rain. 100 questions with answers.",
           "pH below 7 is acidic, 7 is neutral, above 7 is basic.", "Acid + base → salt + water.",
           "<p>Acids taste sour, turn blue litmus red and react with many metals to give hydrogen gas. Bases taste bitter, feel slippery and turn red litmus blue. "
           "The pH scale runs from 0 to 14; each step is a tenfold change in acidity.</p>"
           "<p>In neutralization, an acid and a base react to form a salt and water (HCl + NaOH → NaCl + H₂O). Acids react with carbonates to give a salt, water and carbon dioxide. "
           "Sulfur dioxide and nitrogen oxides from burning fuels form acid precipitation, which harms lakes, forests and buildings; limestone neutralizes it.</p>",
           [("Products of HCl + KOH?", ["Acid + base → salt + water"], "KCl and H₂O"),
            ("A lake goes from pH 6 to pH 5. How much more acidic is it?", ["One pH step = ×10"], "10 times")],
           ["Thinking a pH of 6 is ten times less acidic than pH 5 but calling it basic.", "Saying all salts are sodium chloride.", "Thinking a strong acid and a concentrated acid are the same."],
           [("How do farmers fix acidic soil?", "They add lime (calcium carbonate or calcium oxide), which neutralizes the acid."),
            ("Why do antacids work?", "They are weak bases that neutralize extra stomach acid.")],
           lambda X: [
               ("Properties of acids and bases", [(X.gen("gen_sg_science_s2_acids_and_alkalis", "g_lit"), 6), (X.gen("gen_sg_science_s2_acids_and_alkalis", "g_nat"), 5), (X.gen("gen_sg_science_s3_acid_base_chemistry", "g_strong"), 5), (X.gen("gen_uk_science_y8_metals_and_non_metals", "g_acid"), 4)]),
               ("The pH scale and indicators", [(X.gen("gen_sg_science_s2_acids_and_alkalis", "g_ph"), 10), (X.gen("gen_uk_science_y10_chemical_changes", "g_ph"), 5), (X.gen("gen_sg_science_s3_acid_base_chemistry", "g_sol"), 5)]),
               ("Neutralization and salts", [(X.gen("gen_sg_science_s3_acid_base_chemistry", "g_prod"), 10), (X.gen("gen_uk_science_y10_chemical_changes", "g_salt"), 10)]),
               ("Acids in the environment", [(X.pool(ACIDRAIN), 9), (X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_poll"), 4), (X.gen(G + "ess_carbon_cycle_and_earth_systems", "g_ph"), 3), (X.gen("gen_uk_science_y8_metals_and_non_metals", "g_nmox"), 4)]),
               ("Reactions of acids", [(X.gen("gen_sg_science_s2_acids_and_alkalis", "g_rx"), 8), (X.gen("gen_sg_science_s3_acid_base_chemistry", "g_ox"), 4), (X.gen("gen_sg_science_s3_qualitative_analysis", "g_an"), 4), (X.gen("gen_uk_science_y8_metals_and_non_metals", "g_oxide"), 4)]),
           ]),
        HU("SNC2D", "D", 5, "climate-change", "D3.1, D3.2, D3.3, D3.4",
           "The difference between weather and climate; the greenhouse effect; heat transfer in the atmosphere and the oceans; the carbon cycle and carbon sinks; "
           "feedback loops such as albedo; and natural and human causes of climate change.",
           "Climate Change", "climate change",
           "Free Grade 10 Science (SNC2D) worksheets on climate change: weather and climate, the greenhouse effect, heat transfer by the atmosphere and oceans, carbon sinks, albedo and feedback loops. 100 questions with answers.",
           "Climate is the average weather over about 30 years.", "Greenhouse gases absorb infrared energy given off by Earth.",
           "<p>Weather is what happens day to day; climate is the long-term pattern. Earth's climate depends on the balance between energy coming in from the Sun and infrared energy going out. "
           "Greenhouse gases absorb some outgoing infrared energy and send part of it back, keeping Earth warm.</p>"
           "<p>The atmosphere and oceans move heat from the equator towards the poles by winds and ocean currents. Carbon moves between the air, oceans, rocks and living things; "
           "forests and oceans are carbon sinks. Feedback loops change the size of warming: melting snow and ice lower the albedo, so more sunlight is absorbed (a positive feedback).</p>",
           [("Fresh snow reflects about 80% of sunlight; open water about 6%. What happens when sea ice melts?", ["More sunlight is absorbed."], "warming speeds up (positive feedback)"),
            ("Is 'it rained today in Toronto' weather or climate?", ["One day, one place"], "weather")],
           ["Confusing weather and climate.", "Saying the ozone hole causes global warming.", "Thinking all feedback loops make warming worse: negative feedbacks reduce it."],
           [("What is albedo?", "The fraction of sunlight a surface reflects. Snow has a high albedo; dark forests and oceans have a low albedo."),
            ("Why does the ocean affect climate?", "Water stores huge amounts of heat and currents carry it around the planet, which keeps coastal climates milder.")],
           lambda X: [
               ("Weather and climate", [(X.gen(G + "g6_air_masses_and_weather", "g_mass"), 5), (X.gen(G + "g6_air_masses_and_weather", "g_front"), 5), (X.gen(G + "g6_global_temperature_and_climate_change", "g_temp"), 5), (X.gen(G + "g6_global_temperature_and_climate_change", "g_evid"), 5)]),
               ("The greenhouse effect", [(X.gen(G + "ess_climate_and_energy_flow", "g_eff"), 6), (X.gen(G + "ess_climate_and_energy_flow", "g_budget"), 4), (X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_ghg"), 5), (X.gen("gen_uk_science_y8_the_atmosphere_and_climate", "g_cc"), 5)]),
               ("Heat transfer by air and oceans", [(X.gen(G + "g6_ocean_and_atmosphere_circulation", "g_current"), 6), (X.gen(G + "g6_ocean_and_atmosphere_circulation", "g_wind"), 3), (X.gen(G + "g6_ocean_and_atmosphere_circulation", "g_table"), 3), (X.gen("gen_sg_science_s3_thermal_processes", "g_way"), 4), (X.gen(G + "ess_climate_and_energy_flow", "g_scale"), 4)]),
               ("The carbon cycle and carbon sinks", [(X.gen(G + "ess_carbon_cycle_and_earth_systems", "g_res"), 5), (X.gen(G + "ess_carbon_cycle_and_earth_systems", "g_flux"), 5), (X.gen(G + "ess_carbon_cycle_and_earth_systems", "g_budget"), 5), (X.gen(G + "ess_carbon_cycle_and_earth_systems", "g_keel"), 5)]),
               ("Feedback loops", [(X.gen(G + "ess_feedbacks_in_earth_systems", "g_fb"), 6), (X.gen(G + "ess_feedbacks_in_earth_systems", "g_sys"), 4), (X.gen(G + "ess_feedbacks_in_earth_systems", "g_alb"), 6), (X.gen(G + "ess_feedbacks_in_earth_systems", "g_data"), 4)]),
           ]),
        HU("SNC2D", "D", 6, "climate-change-impacts-and-solutions", "D1.1, D1.2, D3.5, D3.6",
           "Evidence and indicators of climate change; its impacts on the environment and on people in Canada and the world; "
           "and ways to reduce greenhouse gas emissions (mitigation) and to cope with the changes (adaptation).",
           "Climate Change Impacts and Solutions", "climate change impacts and solutions",
           "Free Grade 10 Science (SNC2D) worksheets on climate change impacts and solutions: temperature and CO₂ data, sea level and ice, impacts in Canada, carbon footprints, mitigation and adaptation. 100 questions with answers.",
           "Rising CO₂ and temperatures change ecosystems, oceans and communities.", "Mitigation reduces emissions; adaptation reduces harm.",
           "<p>Evidence of climate change includes higher average temperatures, rising CO₂ (now more than 420 ppm), shrinking glaciers and Arctic sea ice, rising sea level and ocean acidification. "
           "Ice cores and tree rings show how the climate changed in the past.</p>"
           "<p>In Canada, impacts include longer fire seasons, thawing permafrost, shorter ice-road seasons, heavier rainfall and new pests. "
           "Mitigation cuts emissions (clean electricity, transit, efficient buildings, carbon pricing); adaptation prepares for change (flood protection, heat plans, new crop varieties).</p>",
           [("CO₂ rose from 340 ppm in 1980 to 420 ppm in 2020. Average rise per year?", ["80 ppm ÷ 40 years"], "2 ppm per year"),
            ("Is building a sea wall mitigation or adaptation?", ["It protects against the effect, not the cause."], "adaptation")],
           ["Thinking one cold winter disproves climate change.", "Saying melting sea ice is the main cause of sea-level rise: melting land ice and warming water are.", "Mixing up mitigation and adaptation."],
           [("Why does sea level rise as the ocean warms?", "Water expands when it warms, and melting land ice adds more water."),
            ("What is ocean acidification?", "The fall in ocean pH as sea water absorbs extra CO₂, which makes it harder for shellfish and corals to build shells.")],
           lambda X: [
               ("Evidence and indicators", [(X.gen(G + "ess_climate_change_data_and_models", "g_rate"), 5), (X.gen(G + "ess_climate_change_data_and_models", "g_sea"), 5), (X.gen(G + "ess_climate_change_data_and_models", "g_ice"), 5), (X.gen("gen_uk_science_y8_the_atmosphere_and_climate", "g_ppm"), 5)]),
               ("Climate models and predictions", [(X.gen(G + "ess_climate_change_data_and_models", "g_fc"), 6), (X.gen(G + "ess_climate_change_data_and_models", "g_scen"), 6), (X.pool(ADAPT[11:14]), 3), (X.gen(G + "g6_global_temperature_and_climate_change", "g_co2"), 5)]),
               ("Impacts on people and ecosystems", [(X.gen(G + "ess_climate_change_data_and_models", "g_imp"), 6), (X.pool(ADAPT[4:8] + ADAPT[10:11] + ADAPT[14:15]), 6), (X.gen(G + "ess_coevolution_of_life_and_earth", "g_l2e"), 4), (X.gen("gen_uk_science_y8_the_atmosphere_and_climate", "g_ff"), 4)]),
               ("Carbon footprints and sources", [(X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_foot"), 7), (X.gen(G + "ess_sustainability_and_human_impact", "g_foot"), 7), (X.gen("gen_uk_science_y8_the_atmosphere_and_climate", "g_src"), 6)]),
               ("Mitigation and adaptation", [(X.pool(ADAPT[:4] + ADAPT[8:10] + ADAPT[15:]), 7), (X.gen(G + "ess_sustainability_and_human_impact", "g_red"), 7), (X.gen(G + "ess_sustainability_and_human_impact", "g_sol"), 6)]),
           ]),
        HU("SNC2D", "E", 7, "light-and-reflection", "E3.1, E3.2, E3.3, E3.4",
           "The properties and sources of light; the electromagnetic spectrum; the laws of reflection; images in plane mirrors; "
           "and images formed by concave and convex mirrors, using ray diagrams and the mirror and magnification equations.",
           "Light and Reflection", "light and reflection",
           "Free Grade 10 Science (SNC2D) worksheets on light and reflection: sources of light, the electromagnetic spectrum, the law of reflection, plane mirrors, concave and convex mirrors and the mirror equation. 100 questions with answers.",
           "Angle of incidence = angle of reflection, measured from the normal.", "Mirror equation: 1/f = 1/d₀ + 1/dᵢ.",
           "<p>Light travels in straight lines at 3.00 × 10⁸ m/s in a vacuum. Visible light is a small part of the electromagnetic spectrum, between infrared and ultraviolet. "
           "When light reflects, the angle of incidence equals the angle of reflection, both measured from the normal.</p>"
           "<p>A plane mirror makes a virtual, upright image the same size as the object and as far behind the mirror as the object is in front. "
           "A concave (converging) mirror can make real or virtual images; a convex (diverging) mirror always makes a smaller, upright, virtual image. Use 1/f = 1/d₀ + 1/dᵢ and M = h<sub>i</sub>/h<sub>o</sub> = −dᵢ/d₀.</p>",
           [("A ray hits a mirror at 35° to the normal. Angle of reflection?", ["Equal to the angle of incidence"], "35°"),
            ("A concave mirror has f = 10 cm. An object is 30 cm away. Image distance?", ["1/dᵢ = 1/10 − 1/30 = 2/30"], "15 cm")],
           ["Measuring angles from the mirror surface instead of the normal.", "Thinking an image in a plane mirror is on the mirror's surface.", "Forgetting that convex mirrors only make virtual images."],
           [("Why are convex mirrors used in stores and on cars?", "They give a wide field of view, although the images are smaller."),
            ("What is a real image?", "An image formed where light rays actually meet, so it can be shown on a screen.")],
           lambda X: [
               ("Properties and sources of light", [(X.gen("gen_sg_science_s1_ray_model_of_light", "g_use"), 5), (X.gen("gen_sg_science_s1_ray_model_of_light", "g_em"), 5), (X.gen(G + "g8_light_and_sound_waves", "g_what"), 5), (X.gen(G + "g8_light_and_sound_waves", "g_mat"), 5)]),
               ("The electromagnetic spectrum", [(X.gen("gen_sg_science_s3_electromagnetic_spectrum", "g_use"), 6), (X.gen("gen_sg_science_s3_electromagnetic_spectrum", "g_order"), 5), (X.gen("gen_sg_science_s3_electromagnetic_spectrum", "g_harm"), 4), (X.gen("gen_uk_science_y11_waves_and_the_electromagnetic_spectrum", "g_order"), 5)]),
               ("The law of reflection", [(X.gen("gen_sg_science_s1_ray_model_of_light", "g_ang"), 10), (X.gen("gen_sg_science_s3_light", "g_refl"), 10)]),
               ("Plane mirrors", [(X.gen("gen_sg_science_s1_ray_model_of_light", "g_img"), 7), (X.gen("gen_sg_science_s1_ray_model_of_light", "g_dist"), 6), (X.gen("gen_sg_science_s3_light", "g_mirror"), 7)]),
               ("Curved mirrors", [(X.f(optics("mirror")), 20)]),
           ]),
        HU("SNC2D", "E", 8, "refraction-and-lenses", "E3.5, E3.6, E3.7, E2.1",
           "Refraction and the index of refraction; total internal reflection and the critical angle; images formed by converging and diverging lenses, using ray diagrams and the thin lens equation; "
           "and optical devices and the human eye.",
           "Refraction and Lenses", "refraction and lenses",
           "Free Grade 10 Science (SNC2D) worksheets on refraction and lenses: the index of refraction, Snell's law, total internal reflection, converging and diverging lenses, the thin lens equation and the eye. 100 questions with answers.",
           "n = c/v: light slows down and bends in a denser medium.", "Thin lens equation: 1/f = 1/d₀ + 1/dᵢ.",
           "<p>Light bends (refracts) when it changes speed at a boundary. The index of refraction n = c/v (water 1.33, glass about 1.50). "
           "Going into a medium with a higher n, light bends towards the normal; going into a lower n, it bends away. Past the critical angle, it is totally internally reflected.</p>"
           "<p>A converging (convex) lens brings parallel rays to a focus; a diverging (concave) lens spreads them out. "
           "Use ray diagrams or 1/f = 1/d₀ + 1/dᵢ and M = −dᵢ/d₀. The eye uses its cornea and lens to focus a real, inverted image on the retina; glasses correct near- and far-sightedness.</p>",
           [("Light travels at 2.0 × 10⁸ m/s in a plastic. Index of refraction?", ["n = 3.0 × 10⁸ ÷ 2.0 × 10⁸"], "1.5"),
            ("A converging lens, f = 5.0 cm, object at 15 cm. Image distance?", ["1/dᵢ = 1/5 − 1/15 = 2/15"], "7.5 cm")],
           ["Bending the ray the wrong way at the boundary.", "Thinking total internal reflection happens going into a denser medium.", "Using a converging lens to correct near-sightedness."],
           [("Why does a straw look bent in a glass of water?", "Light from the straw refracts as it leaves the water, so the straw appears in a different place."),
            ("Why do diamonds sparkle?", "Their high index of refraction gives a small critical angle, so light is reflected many times inside.")],
           lambda X: [
               ("Refraction", [(X.gen("gen_sg_science_s1_ray_model_of_light", "g_refr"), 6), (X.gen(G + "g8_light_and_sound_waves", "g_refr"), 6), (X.gen("gen_sg_science_s3_light", "g_snell"), 8)]),
               ("The index of refraction", [(X.ch("in_s12p", "electromagnetic-waves", 3), 12), (X.ch("al_phys", "waves-and-optics", 2, 12), 8)]),
               ("Total internal reflection", [(X.gen("gen_sg_science_s3_light", "g_crit"), 10), (X.ch("in_s12p", "ray-optics-and-optical-instruments", 2), 10)]),
               ("Converging and diverging lenses", [(X.gen("gen_sg_science_s3_light", "g_lens"), 6), (X.gen("gen_sg_science_s3_light", "g_fl"), 4), (X.f(optics("lens")), 10)]),
               ("The eye and optical devices", [(X.pool(EYE), 10), (X.ch("in_s12p", "ray-optics-and-optical-instruments", 5), 6), (X.ch("in_s12p", "ray-optics-and-optical-instruments", 4), 4)]),
           ]),
    ]
