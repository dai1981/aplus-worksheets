# -*- coding: utf-8 -*-
"""
Singapore Secondary 4 O-Level Biology (6093), Topic 13: Reproduction
  python tools/gen_sg_science_s4_reproduction.py
Asexual and sexual reproduction; mitosis and meiosis (diploid and haploid cells, chromosome numbers); sexual reproduction in
flowering plants (parts of a flower, insect and wind pollination, fertilisation, seed and fruit); sexual reproduction in humans
(reproductive systems, the menstrual cycle, fertilisation, implantation, the placenta); sexually transmitted infections such as HIV.
US NGSS meiosis and UK KS3 reproduction makers are reused (Singapore names); the rest is written here.
Wrong answers come from real mistakes: "pollination is fertilisation", "mitosis makes gametes", "the placenta mixes mother's and
fetus's blood", "ovulation happens on day 1", "gametes are diploid".
"""
from sg_ol import OL, seed_of, make_ol, tq, rows, pool

LV, SUBJ, SORT = 4, "Biology", 19
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))

us_num = src("gen_us_science_bio_meiosis_and_genetic_variation", "g_num", drop=["pea plant", "plant body cell"])
uk_step = src("gen_uk_science_y7_human_reproduction", "g_step", rep=[("foetus", "fetus")])

MM = [("the number of daughter cells made", "two", "four"), ("the chromosome number of the daughter cells", "the same as the parent (diploid)", "half of the parent (haploid)"),
      ("whether daughter cells are genetically identical", "identical to each other and the parent", "genetically different"),
      ("where it happens in humans", "in body cells for growth and repair", "in the testes and ovaries to make gametes"),
      ("its role", "growth, repair and asexual reproduction", "making gametes for sexual reproduction")]


def g_mm():
    f, mi, me = R.choice(MM)
    mit = R.random() < 0.5
    a = mi if mit else me
    others = [x[1] for x in MM if x[0] != f] + [x[2] for x in MM if x[0] != f]
    return tq("For %s, what is %s?" % ("mitosis" if mit else "meiosis", f), a, [me if mit else mi] + R.sample(others, 2),
              "Mitosis: 2 identical diploid cells for growth and repair. Meiosis: 4 different haploid gametes.")


FLOWER = [("the anther", "makes pollen grains"), ("the filament", "holds up the anther"), ("the stigma", "receives pollen grains during pollination"),
          ("the style", "joins the stigma to the ovary"), ("the ovary", "contains ovules and becomes the fruit"), ("the ovule", "contains the female gamete and becomes the seed"),
          ("the petals", "attract insects in insect-pollinated flowers"), ("the sepals", "protect the flower bud")]
g_flower = rows(R, FLOWER, "What is the function of %s?", "Which part of a flower %s?")

POLL = [("large, brightly coloured petals", "insect-pollinated"), ("nectar and scent", "insect-pollinated"), ("sticky or spiky pollen grains", "insect-pollinated"),
        ("anthers and stigma inside the flower", "insect-pollinated"), ("small, dull petals or none", "wind-pollinated"), ("large amounts of light, smooth pollen", "wind-pollinated"),
        ("feathery stigmas hanging outside the flower", "wind-pollinated"), ("anthers on long filaments hanging outside", "wind-pollinated")]


def g_poll():
    f, t = R.choice(POLL)
    return tq("A flower has %s. How is it most likely pollinated?" % f, t, [x for x in ("insect-pollinated", "wind-pollinated", "self-fertilised without pollen", "pollinated by water only") if x != t],
              "Insect-pollinated flowers attract insects; wind-pollinated flowers release and catch pollen in the air.")


HUM = [("the testes", "make sperm and testosterone"), ("the sperm duct", "carries sperm from the testis to the urethra"),
       ("the prostate gland and seminal vesicles", "add fluid containing nutrients to sperm"), ("the ovaries", "make eggs and the hormones oestrogen and progesterone"),
       ("the oviduct", "carries the egg to the uterus and is where fertilisation happens"), ("the uterus", "is where the embryo implants and the fetus develops"),
       ("the cervix", "is a ring of muscle at the neck of the uterus"), ("the placenta", "lets oxygen and nutrients pass from mother to fetus and wastes pass back"),
       ("the umbilical cord", "contains blood vessels that link the fetus to the placenta"), ("the amniotic fluid", "protects the fetus from shocks")]
g_hum = rows(R, HUM, "What is the role of %s?", "Which structure has this role: “%s”?")

GAM = [("size", "much smaller than the egg", "large, one of the largest human cells"), ("movement", "swims using a tail (flagellum)", "cannot move by itself; it is moved by cilia in the oviduct"),
       ("number made", "millions made every day", "usually one released each month"), ("food store", "very little stored food", "cytoplasm with a store of food for the early embryo"),
       ("special feature at the front", "an acrosome with enzymes to digest the egg's outer layer", "a jelly coat that changes after one sperm enters")]


def g_gam():
    f, sp, egg = R.choice(GAM)
    s_ = R.random() < 0.5
    a = sp if s_ else egg
    o = [x[1] for x in GAM if x[0] != f] + [x[2] for x in GAM if x[0] != f]
    return tq("Compare human sperm and eggs. For %s, what is the %s?" % ("a sperm cell" if s_ else "an egg cell", f), a, [egg if s_ else sp] + R.sample(o, 2),
              "Sperm: small, many, swim, acrosome. Egg: large, few, food store, moved by cilia.")


def g_cycle():
    k = R.choice(["ov", "mens", "thick", "fert", "oest", "prog"])
    d = {"ov": ("On about which day of a 28-day menstrual cycle does ovulation happen?", "day 14", ["day 1", "day 5", "day 28"], "An egg is released from the ovary about halfway through the cycle."),
         "mens": ("What happens during days 1 to 5 of the menstrual cycle?", "The uterus lining breaks down and is lost (menstruation).", ["An egg is released.", "The lining becomes thickest.", "Fertilisation takes place."], "This happens if no fertilisation occurred."),
         "thick": ("What does oestrogen do in the first half of the menstrual cycle?", "It makes the uterus lining thicken again.", ["It causes menstruation.", "It releases the egg from the oviduct.", "It breaks down the placenta."], "Oestrogen is made by the ovary."),
         "fert": ("During which days of a 28-day cycle is fertilisation most likely?", "around days 11 to 17", ["days 1 to 5", "days 22 to 28", "only on day 1"], "Sperm can survive a few days and the egg about one day."),
         "oest": ("Which hormone is made by the ovaries and repairs the uterus lining after menstruation?", "oestrogen", ["progesterone", "testosterone", "insulin"], "Progesterone keeps the lining thick after ovulation."),
         "prog": ("Which hormone keeps the uterus lining thick after ovulation and during pregnancy?", "progesterone", ["oestrogen", "testosterone", "adrenaline"], "If progesterone falls, the lining breaks down.")}[k]
    return tq(*d)


POOL1 = pool(R, [
    ("What is asexual reproduction?", "reproduction by one parent, giving offspring that are genetically identical to the parent", ["reproduction with two parents", "joining of two gametes", "reproduction that needs pollination"], "It involves mitosis."),
    ("Give one advantage of sexual reproduction.", "It produces genetic variation, so some offspring may survive changes in the environment.", ["It is faster than asexual reproduction.", "Only one parent is needed.", "All offspring are identical."], "Variation is the raw material for natural selection."),
    ("What is pollination?", "the transfer of pollen grains from an anther to a stigma", ["the joining of a male and female gamete", "the growth of a seed", "the release of seeds"], "Fertilisation happens later."),
    ("What is fertilisation in a flowering plant?", "the fusion of a male gamete from a pollen tube with the female gamete in the ovule", ["the transfer of pollen to the stigma", "the opening of the flower", "the dispersal of seeds"], "The pollen tube grows down the style."),
    ("What happens to the ovary and ovules after fertilisation?", "The ovary becomes the fruit and the ovules become seeds.", ["The ovary becomes the seed.", "The ovules become petals.", "The ovary falls off at once."], "The petals wither."),
    ("What is a gamete?", "a sex cell with half the normal number of chromosomes (haploid)", ["a body cell with 46 chromosomes", "a fertilised egg", "a cell made by mitosis for growth"], "Sperm and eggs in humans have 23 chromosomes."),
    ("What is a zygote?", "the diploid cell formed when two gametes fuse", ["a haploid sex cell", "a fruit", "the placenta"], "It divides by mitosis to form an embryo."),
    ("Where does fertilisation normally happen in humans?", "in the oviduct", ["in the uterus", "in the ovary", "in the vagina"], "The embryo then moves to the uterus and implants."),
    ("What is implantation?", "the embryo embedding in the thick lining of the uterus", ["the egg leaving the ovary", "sperm entering the egg", "the baby being born"], "The placenta then forms."),
    ("How is HIV transmitted?", "through sexual contact, sharing needles or from an infected mother to her baby", ["through mosquito bites", "by shaking hands", "by sharing cups"], "HIV attacks lymphocytes and can lead to AIDS."),
])
POOL5 = pool(R, [
    ("Why is it important that the mother's blood does not mix with the fetus's blood?", "The mother's higher blood pressure or a different blood group could harm the fetus.", ["The blood would become too cold.", "The fetus would get too much oxygen.", "The placenta would stop growing."], "Substances are exchanged across a thin barrier by diffusion and active transport."),
    ("Which substances pass from the fetus to the mother across the placenta?", "carbon dioxide and urea", ["oxygen and glucose", "antibodies and amino acids", "red blood cells"], "The mother's kidneys and lungs remove them."),
    ("Why can harmful substances such as nicotine and alcohol affect a fetus?", "They are small molecules that can cross the placenta.", ["They are stored in the amniotic fluid.", "They block the umbilical cord.", "They are too large to cross."], "Viruses such as rubella can also cross."),
    ("Why is meiosis needed before fertilisation?", "Gametes must be haploid so that the zygote has the normal diploid number.", ["To make the gametes identical.", "To repair the gametes.", "To double the chromosome number."], "23 + 23 = 46 in humans."),
    ("A plant has 24 chromosomes in its leaf cells. How many are in its pollen nucleus?", "12", ["24", "48", "6"], "Gametes are haploid."),
    ("Why is a condom effective against HIV?", "It is a barrier that stops body fluids passing between partners.", ["It kills the virus with antibiotics.", "It is a vaccine.", "It makes the person immune."], "There is no cure for HIV, but drugs can control it."),
    ("Why do wind-pollinated flowers make so much pollen?", "Most pollen is lost because the wind carries it in random directions.", ["Insects eat most of it.", "Pollen is used for photosynthesis.", "It attracts more insects."], "Grass and maize are wind-pollinated."),
    ("A strawberry plant grows runners that form new plants. Why are the new plants identical?", "They are produced by asexual reproduction through mitosis.", ["They come from seeds.", "They are made by meiosis.", "They are pollinated by wind."], "These are clones."),
])


def main():
    sets = U.sets([
        ("Mitosis and meiosis", [(g_mm, 7), (us_num, 9), (POOL1, 4)]),
        ("Reproduction in flowering plants", [(g_flower, 10), (g_poll, 6), (POOL1, 4)]),
        ("Human reproductive systems", [(g_hum, 12), (g_gam, 6), (POOL1, 2)]),
        ("The menstrual cycle and pregnancy", [(g_cycle, 5), (uk_step, 6), (g_hum, 5), (POOL5, 4)]),
        ("Exam-style questions", [(POOL5, 4), (us_num, 6), (g_mm, 3), (g_poll, 2), (g_flower, 4), (g_cycle, 1)]),
    ])
    make_ol(LV, SUBJ, "reproduction", SORT, "Reproduction",
            "Distinguish between asexual and sexual reproduction; describe mitosis and meiosis and the roles of haploid and diploid cells; describe the structure of "
            "an insect-pollinated and a wind-pollinated flower, pollination, fertilisation and the formation of seed and fruit; describe the male and female "
            "reproductive systems, the menstrual cycle, fertilisation, implantation and the role of the placenta; describe how HIV is transmitted and ways of "
            "reducing its spread (summary of the Singapore-Cambridge O-Level Biology 6093 syllabus).",
            "Reproduction", "Reproduction",
            "Free Secondary 4 O-Level Biology worksheets on reproduction: mitosis and meiosis, flowers, pollination, fertilisation, human reproductive systems, the "
            "menstrual cycle, the placenta and HIV. 100 questions with answers.",
            "Meiosis makes haploid gametes; fertilisation restores diploid.", "Pollination moves pollen; fertilisation joins gametes.",
            "<p><b>Two kinds of reproduction, two kinds of cell division.</b></p><ul>"
            "<li>Mitosis: 2 identical diploid cells (growth, repair, asexual). Meiosis: 4 different haploid gametes.</li>"
            "<li>Flowers: anther makes pollen → pollination to stigma → pollen tube → fertilisation in the ovule → seed; ovary → fruit.</li>"
            "<li>Humans: egg released on about day 14; fertilisation in the oviduct; implantation in the uterus; placenta for exchange.</li>"
            "<li>HIV spreads through sexual contact, shared needles and from mother to baby.</li></ul>",
            [("Body cell 2n = 18. Gamete?", ["meiosis halves the number"], "9"),
             ("Feathery stigma outside the flower?", ["catches pollen from the air"], "wind-pollinated")],
            ["Saying pollination and fertilisation are the same.", "Saying mitosis makes gametes.", "Saying the mother's and fetus's blood mix.", "Saying gametes are diploid."],
            [("What is the difference between mitosis and meiosis?", "Mitosis gives two genetically identical diploid cells for growth and repair. Meiosis gives four genetically different haploid cells, the gametes."),
             ("What is the difference between pollination and fertilisation?", "Pollination is the transfer of pollen from an anther to a stigma. Fertilisation is the fusion of the male gamete with the female gamete inside the ovule."),
             ("What does the placenta do?", "It lets oxygen, glucose and amino acids diffuse from the mother's blood to the fetus, and carbon dioxide and urea pass back, without the two bloods mixing.")],
            sets)


if __name__ == "__main__":
    main()
