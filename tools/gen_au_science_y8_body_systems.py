# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 8, AC9S8U02: multicellular organisms are organised into cells, tissues, organs and
systems; the digestive, circulatory and respiratory systems work together to supply cells with nutrients and oxygen.
  python tools/gen_au_science_y8_body_systems.py
Reuses the US Grade 6 body-system makers, the UK Year 8 digestion and breathing makers, the UK Year 6 circulatory makers and the
SG Secondary 2 transport makers with Australian names.
Wrong answers come from real mistakes: thinking arteries always carry oxygen-rich blood, thinking digestion happens only in the
stomach, and thinking the lungs pump air by themselves.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 8, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

BS = "gen_us_science_g6_body_systems"
DG = "gen_uk_science_y8_food_and_digestion"
BR = "gen_uk_science_y8_breathing_and_gas_exchange"
CI = "gen_uk_science_y6_the_circulatory_system"
TR = "gen_sg_science_s2_transport_systems_in_living_things"
b_inter = src(BS, "g_inter")
b_job = src(BS, "g_job")
b_level = limit(src(BS, "g_level"), 6)
b_organ = limit(src(BS, "g_organ"), 6)
d_def = src(DG, "g_def")
d_enz = src(DG, "g_enz")
d_need = limit(src(DG, "g_need"), 4)
d_b1 = src.B(DG, "B1")
r_job = limit(src(BR, "g_job"), 6)
r_mech = src(BR, "g_mech")
r_path = src(BR, "g_path")
r_adapt = src(BR, "g_adapt")
r_b1 = src.B(BR, "B1")
r_b5 = src.B(BR, "B5")
c_part = limit(src(CI, "g_part"), 6)
c_loop = src(CI, "g_loop")
c_oxy = src(CI, "g_oxy")
c_b5 = src.B(CI, "B5")
t_ves = src(TR, "g_ves")
t_b1 = src.B(TR, "B1")

POOL5 = pool(R, [
    ("Mia measures her pulse: 72 beats per minute at rest and 140 after running. Why does it rise?", "Muscles need more oxygen and glucose, so the heart pumps faster.", ["The heart gets tired.", "Blood gets thicker.", "The lungs stop working."], "The circulatory and respiratory systems work together."),
    ("Jack counts his breaths: 14 per minute at rest, 30 after skipping. Which systems are working together?", "the respiratory and circulatory systems", ["the digestive and skeletal systems only", "the nervous system only", "no systems"], "More oxygen in, more carbon dioxide out."),
    ("Ruby models digestion by squeezing bread in a stocking. What does the stocking represent?", "the small intestine", ["the heart", "the lungs", "the brain"], "Small, digested particles pass through the walls."),
    ("Kai uses a model of the lungs with balloons and a rubber sheet. What does pulling the sheet down represent?", "the diaphragm contracting so we breathe in", ["breathing out", "the heart beating", "food being swallowed"], "Lower pressure in the chest draws air in."),
    ("Why do scientists use models of body systems?", "Real organs are hard to see working, so models show how they function.", ["Models are always perfect.", "Organs do not exist.", "Models replace experiments."], "Every model has limits."),
    ("Ella says the small intestine is short because it is called 'small'. What is correct?", "It is long (about 6 m) but narrow.", ["It is about 6 cm long.", "It is shorter than the large intestine.", "It is the same as the stomach."], "'Small' refers to its width."),
])


def main():
    sets = U.sets([
        ("Levels of organisation", [(b_level, 6), (b_organ, 6), (b_job, 5), (b_inter, 3)]),
        ("The digestive system", [(d_def, 6), (d_enz, 5), (d_need, 3), (d_b1, 6)]),
        ("The respiratory system", [(r_job, 6), (r_mech, 5), (r_path, 4), (r_adapt, 3), (r_b1, 2)]),
        ("The circulatory system", [(c_part, 6), (c_loop, 4), (c_oxy, 3), (t_ves, 5), (t_b1, 2)]),
        ("Systems working together", [(POOL5, 6), (b_inter, 4), (r_b5, 4), (c_b5, 4), (b_job, 2)]),
    ])
    make_au(YEAR, "body-systems", SORT, "AC9S8U02", "Biological sciences",
            "Describe the structure and function of a multicellular system, including how cells, tissues and organs work together, and "
            "how the digestive, respiratory and circulatory systems interact (summary of the Australian Curriculum v9.0 Science content description).",
            "Body Systems", "Body systems",
            "Free Year 8 science worksheets on body systems: cells, tissues, organs and systems, and how the digestive, respiratory and "
            "circulatory systems work together. 100 questions with answers.",
            "Cells → tissues → organs → systems.", "Digestion, breathing and circulation together deliver nutrients and oxygen to every cell.",
            "<p><b>In multicellular organisms, cells form tissues, tissues form organs, and organs form systems.</b></p><ul>"
            "<li>Digestive system: breaks food into small molecules that are absorbed in the small intestine.</li>"
            "<li>Respiratory system: the diaphragm and rib muscles move air in and out; oxygen diffuses into the blood in the alveoli.</li>"
            "<li>Circulatory system: the heart pumps blood through arteries, capillaries and veins to every cell, carrying oxygen and nutrients.</li></ul>",
            [("Order from smallest: organ, cell, system, tissue", ["cells make tissues", "tissues make organs"], "cell, tissue, organ, system"),
             ("Where are nutrients absorbed into the blood?", ["the walls are thin with villi"], "the small intestine")],
            ["Thinking arteries always carry oxygen-rich blood (the pulmonary artery does not).", "Thinking digestion happens only in the stomach.",
             "Thinking the lungs pump air by themselves (the diaphragm and rib muscles do the work)."],
            [("How do the digestive and circulatory systems work together?", "The digestive system breaks food into small molecules. They are absorbed into the blood in the small intestine and the circulatory system carries them to all cells."),
             ("What happens in the alveoli?", "Oxygen diffuses from the air in the alveoli into the blood, and carbon dioxide diffuses from the blood into the alveoli to be breathed out."),
             ("Why does your heart rate rise during exercise?", "Muscles need more oxygen and glucose for respiration, so the heart pumps faster and you breathe faster.")],
            sets)


if __name__ == "__main__":
    main()
