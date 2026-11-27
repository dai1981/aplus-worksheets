# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U02: the form and function of reproductive cells and organs in animals and
plants, fertilisation, and how sexual and asexual reproduction help species survive.
  python tools/gen_au_science_y9_reproduction.py
Reuses the UK Year 7 human and plant reproduction makers, the SG Secondary 2 human reproductive system makers and the US Grade 8
reproduction makers with Australian names, plus own questions on Australian examples (coral spawning, marsupials, monotremes,
wattle seeds and bushfire).
Wrong answers come from real mistakes: thinking sexual reproduction needs only one parent, mixing up the ovary and the uterus,
and thinking asexual offspring vary.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

HR = "gen_uk_science_y7_human_reproduction"
PR = "gen_uk_science_y7_plant_reproduction"
S2 = "gen_sg_science_s2_human_sexual_reproductive_system"
AS = "gen_us_science_g8_asexual_and_sexual_reproduction"
PA = "gen_us_science_g8_plant_and_animal_reproduction"
NO = ["contracept", "condom", "sexually transmitted", "STI", "acorn", "recessive", "allele", "What is the job of", r"What does the [a-z ()]+ do\?"]
h_part = src(HR, "g_part", drop=NO)
h_step = src(HR, "g_step", drop=NO)
h_voc = limit(src(HR, "g_voc", drop=NO), 6)
h_gest = limit(src(HR, "g_gest", drop=NO), 3)
h_b1 = src.B(HR, "B1", drop=NO)
h_b5 = src.B(HR, "B5", drop=NO)
p_fall = limit(src(PR, "g_fall", drop=NO), 6)
p_sex = src(PR, "g_sex", drop=NO)
p_b1 = src.B(PR, "B1", drop=NO)
p_b5 = src.B(PR, "B5", drop=NO)
s_part = limit(src(S2, "g_part", drop=NO), 6)
s_cycle = src(S2, "g_cycle", drop=NO)
a_kind = limit(src(AS, "g_kind", drop=NO), 8)
a_b1 = src.B(AS, "B1", drop=NO)
a_b5 = src.B(AS, "B5", drop=NO)
g_str = limit(src(PA, "g_str", drop=NO), 6)
g_ge = src(PA, "g_ge", drop=NO)

POOL1 = pool(R, [
    ("What is the main difference between sexual and asexual reproduction?", "Sexual reproduction joins two gametes from two parents; asexual reproduction needs only one parent.", ["Asexual reproduction needs two parents.", "Sexual reproduction makes identical offspring.", "There is no difference."], "Sexual offspring vary; asexual offspring are clones."),
    ("Why are offspring from sexual reproduction different from each other?", "They get a different mix of genes from each parent.", ["They are clones.", "They have no genes.", "They copy only the mother."], "Variation helps a species survive change."),
    ("What is an advantage of asexual reproduction?", "It is fast and needs only one parent.", ["It makes lots of variation.", "It needs two parents.", "It always produces seeds."], "Strawberry runners spread quickly."),
    ("What is a disadvantage of asexual reproduction?", "All offspring are identical, so one disease can kill them all.", ["It is too slow.", "It needs a partner.", "Offspring vary too much."], "Banana plantations are at risk for this reason."),
    ("What are the male and female gametes in humans?", "sperm and egg (ovum)", ["testis and ovary", "pollen and ovule", "embryo and foetus"], "Gametes are sex cells."),
    ("What are the male and female gametes in a flowering plant?", "pollen nucleus and ovule (egg cell)", ["anther and stigma", "petal and sepal", "seed and fruit"], "Pollen carries the male gamete."),
    ("Each year, corals on the Great Barrier Reef release eggs and sperm into the water on the same nights. Why?", "to make fertilisation more likely", ["to avoid fertilisation", "because they reproduce asexually", "to feed fish only"], "Mass spawning puts many gametes together."),
    ("A red kangaroo joey is born tiny and grows in its mother's pouch. What kind of mammal is a kangaroo?", "a marsupial", ["a monotreme", "a placental mammal", "a reptile"], "Marsupials carry young in a pouch."),
    ("The platypus and echidna are mammals that lay eggs. What are they called?", "monotremes", ["marsupials", "reptiles", "placental mammals"], "Australia is home to all living monotremes except the long-beaked echidnas of New Guinea."),
    ("Many wattle seeds only sprout after a bushfire. How does this help the species survive?", "Seeds grow when there is space, light and nutrients after the fire.", ["Fire kills all seeds.", "Wattles reproduce only asexually.", "Seeds need snow to sprout."], "Many Australian plants are adapted to fire."),
    ("Where does fertilisation usually happen in humans?", "in the oviduct (fallopian tube)", ["in the uterus wall", "in the ovary", "in the vagina"], "The fertilised egg then moves to the uterus."),
    ("What is the job of the placenta?", "to pass oxygen and nutrients from the mother's blood to the foetus and remove wastes", ["to make sperm", "to make eggs", "to protect the baby from all germs"], "The blood of mother and foetus do not mix."),
])
POOL5 = pool(R, [
    ("Mia takes cuttings from a geranium and puts them in water. After two weeks, roots grow. What kind of reproduction is this?", "asexual (vegetative) reproduction", ["sexual reproduction", "pollination", "fertilisation"], "The new plants are clones."),
    ("Jack counts pollen grains that germinate in sugar solutions of 0%, 5%, 10% and 15%. What is the independent variable?", "the sugar concentration", ["the number that germinate", "the type of microscope", "the slide"], "He changes the sugar concentration."),
    ("Ruby compares bean seeds germinating at 5 °C, 15 °C and 25 °C. Most sprout at 25 °C. What can she conclude?", "Warmth (up to 25 °C) helps bean seeds germinate.", ["Seeds need no water.", "Cold is best for all seeds.", "Temperature has no effect."], "Repeat with more seeds to check."),
    ("Kai dissects a flower and finds six stamens around one carpel. Which part makes pollen?", "the anther, at the top of each stamen", ["the stigma", "the ovary", "the petal"], "The stigma catches pollen."),
    ("Ella says a banana plantation of clones is at risk from a new fungus. Why?", "All plants have the same genes, so none may resist it.", ["Clones resist all diseases.", "Fungi cannot infect bananas.", "Clones grow too slowly."], "Lack of variation is risky."),
    ("Noah measures the length of a human embryo and foetus: 1 cm at 8 weeks, 6 cm at 12 weeks and 16 cm at 20 weeks. What does the data show?", "It grows faster as the pregnancy goes on.", ["It stops growing.", "It shrinks.", "It grows the same amount each week."], "Growth speeds up after the organs form."),
    ("Zara grows yeast in warm sugar water and sees buds forming on cells. What kind of reproduction is this?", "asexual reproduction by budding", ["sexual reproduction", "seed dispersal", "pollination"], "Each bud becomes a new cell."),
    ("Amelia covers some flowers on a tomato plant with paper bags so insects cannot reach them. What is she testing?", "whether insects are needed for pollination and fruit", ["whether bags make tomatoes red", "how tall the plant grows", "whether tomatoes need soil"], "Compare covered and uncovered flowers."),
    ("Harper grows new potato plants from pieces of potato with 'eyes'. How will the new plants compare with the parent?", "genetically identical to the parent", ["a mix of two parents", "completely different", "unable to grow"], "This is asexual reproduction."),
    ("Liam wants to test which way of dispersing seeds travels furthest. Which fair test could he use?", "drop different seeds from the same height in front of the same fan and measure the distance", ["drop seeds from different heights", "use different fans for each seed", "only test one seed"], "Keep everything the same except the seed."),
])


def main():
    sets = U.sets([
        ("Sexual and asexual reproduction", [(POOL1, 6), (a_kind, 7), (a_b1, 4), (p_sex, 3)]),
        ("Human reproductive organs", [(h_part, 6), (s_part, 5), (h_voc, 4), (s_cycle, 3), (POOL1, 2)]),
        ("Fertilisation and development", [(h_step, 6), (h_gest, 3), (h_b1, 4), (POOL1, 3), (s_cycle, 2), (h_voc, 2)]),
        ("Plant reproduction", [(g_str, 6), (p_fall, 5), (p_b1, 4), (g_ge, 3), (POOL1, 2)]),
        ("Investigations", [(POOL5, 9), (p_b5, 3), (h_b5, 3), (a_b5, 3), (a_kind, 1), (g_str, 2), (g_ge, 1)]),
    ])
    make_au(YEAR, "reproduction", SORT, "AC9S9U02", "Biological sciences",
            "Describe the form and function of reproductive cells and organs in animals and plants, and analyse how the processes of "
            "sexual and asexual reproduction enable survival of the species (summary of the Australian Curriculum v9.0 Science content description).",
            "Reproduction in Plants and Animals", "Reproduction",
            "Free Year 9 science worksheets on reproduction: sexual and asexual reproduction, gametes, human reproductive organs, "
            "fertilisation and development, flowers, pollination and seeds. 100 questions with answers.",
            "Sexual = variation; asexual = clones.", "Sexual reproduction mixes genes from two parents; asexual reproduction copies one parent.",
            "<p><b>Reproduction makes new individuals so a species survives.</b></p><ul>"
            "<li>Sexual reproduction: a male and a female gamete join (fertilisation). Offspring vary, which helps when conditions change.</li>"
            "<li>Asexual reproduction: one parent, no gametes (runners, cuttings, budding). Fast, but offspring are identical clones.</li>"
            "<li>Flowers: anthers make pollen, the stigma catches it, and the ovule in the ovary becomes a seed after fertilisation.</li></ul>",
            [("Strawberry runner: sexual or asexual?", ["one parent", "clone"], "asexual"),
             ("Where is the egg fertilised?", ["egg leaves the ovary", "meets sperm in the oviduct"], "the oviduct")],
            ["Thinking sexual reproduction needs only one parent.", "Mixing up the ovary (makes eggs) and the uterus (where the baby grows).",
             "Thinking offspring from asexual reproduction are all different."],
            [("Why do many species use both kinds of reproduction?", "Asexual reproduction is fast when conditions are good. Sexual reproduction creates variation that helps the species survive when conditions change."),
             ("What is the difference between pollination and fertilisation?", "Pollination is pollen landing on the stigma. Fertilisation happens later, when the male gamete from the pollen joins the egg in the ovule."),
             ("How are marsupials different from placental mammals?", "Marsupials, such as kangaroos, give birth to tiny young that grow in a pouch. Placental mammals grow inside the uterus with a placenta until they are more developed.")],
            sets)


if __name__ == "__main__":
    main()
