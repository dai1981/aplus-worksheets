# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U02: the theory of evolution by natural selection, variation, selection
pressures, adaptation and speciation, and the evidence for evolution (fossils, comparative anatomy and DNA).
  python tools/gen_au_science_y10_evolution_and_natural_selection.py
Reuses the US Biology evidence for evolution, natural selection, trait frequency and speciation makers, the US Grade 8 natural
selection makers and the UK Year 9 variation and evolution makers with Australian names, plus own questions on Australian
examples (rabbits and myxomatosis, cane toads, Tasmanian devils, marsupials).
Wrong answers come from real mistakes: thinking individuals evolve during their lifetime, thinking organisms change because
they "need" to, and thinking evolution has a goal.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

EV = "gen_us_science_bio_evidence_for_evolution"
NS = "gen_us_science_bio_natural_selection_and_adaptation"
SP = "gen_us_science_bio_speciation_extinction_and_biodiversity"
TF = "gen_us_science_bio_changes_in_trait_frequency"
G8 = "gen_us_science_g8_natural_selection"
V9 = "gen_uk_science_y9_variation_and_evolution"
e_dna = limit(src(EV, "g_dna"), 5)
e_layer = limit(src(EV, "g_layer"), 5)
e_seq = limit(src(EV, "g_seq"), 4)
e_struct = limit(src(EV, "g_struct"), 5)
e_b1 = src.B(EV, "B1")
e_b5 = src.B(EV, "B5")
n_data = limit(src(NS, "g_data"), 5)
n_factor = src(NS, "g_factor")
n_resist = limit(src(NS, "g_resist"), 5)
n_scen = src(NS, "g_scen")
n_b1 = src.B(NS, "B1")
n_b5 = src.B(NS, "B5")
s_iso = src(SP, "g_iso", drop=["Grand Canyon"])
s_env = limit(src(SP, "g_env"), 5)
t_sel = src(TF, "g_select")
g_which = limit(src(G8, "g_which"), 5)
g_graph = limit(src(G8, "g_graph"), 4)
v_cause = src(V9, "g_cause")
v_var = src(V9, "g_var")
v_ext = src(V9, "g_ext")

POOL1 = pool(R, [
    ("What are the main steps of natural selection?", "variation, selection pressure, survival and reproduction of the best suited, inheritance", ["need, effort, change, success", "individuals change on purpose to survive", "only mutations, nothing else"], "Darwin and Wallace described this in 1858."),
    ("Who proposed the theory of evolution by natural selection?", "Charles Darwin and Alfred Russel Wallace", ["Isaac Newton and Albert Einstein", "Gregor Mendel only", "Louis Pasteur"], "Darwin visited Australia on HMS Beagle in 1836."),
    ("Rabbits in Australia were infected with the myxoma virus in 1950. Within years, more rabbits survived it. Why?", "Rabbits with natural resistance survived and passed it on to their offspring.", ["Rabbits learned to avoid the virus.", "The virus made rabbits stronger on purpose.", "Every rabbit became resistant during its life."], "Resistant genes became more common."),
    ("Some Australian snakes now have smaller heads in areas with cane toads. Why?", "Snakes with small heads cannot swallow big toxic toads, so they survive and breed.", ["Snakes shrank their heads on purpose.", "Cane toads made snakes smaller.", "Small heads are a mutation in every snake."], "This is natural selection in action."),
    ("Some Tasmanian devils now show resistance to devil facial tumour disease. What explains this?", "Devils with resistance genes survived and passed them on.", ["Devils learned to avoid the tumour.", "The disease went away by itself.", "All devils mutated at once."], "Selection is changing the population."),
    ("Why does an individual organism not evolve?", "Evolution is a change in the gene pool of a population over generations.", ["Individuals evolve every day.", "Only old organisms evolve.", "Evolution only happens in plants."], "Populations evolve; individuals do not."),
    ("What is speciation?", "the formation of a new species, often after populations are separated", ["the death of a species", "a mutation in one cell", "a type of reproduction"], "Isolated populations change in different ways."),
    ("What are homologous structures?", "similar structures in different species that come from a common ancestor", ["structures with the same use but different origins", "structures with no use", "identical organs"], "The forelimbs of humans, whales and bats."),
    ("Why do scientists compare DNA sequences between species?", "Closely related species have more similar DNA.", ["DNA is the same in all species.", "DNA shows the age of rocks.", "DNA only shows diet."], "DNA evidence supports common ancestry."),
    ("In undisturbed rock layers, where are the oldest fossils usually found?", "in the lowest layers", ["in the top layers", "in the middle only", "they are spread randomly"], "This is the law of superposition."),
    ("Why do many marsupials live only in Australia?", "Australia was isolated for millions of years, so marsupials evolved into many forms here.", ["Marsupials cannot swim.", "They were brought by people.", "Other continents are too cold."], "Isolation led to adaptive radiation."),
    ("What is a selection pressure?", "a factor in the environment that affects which individuals survive and reproduce", ["a force that changes DNA on purpose", "the pressure of the air", "a type of fossil"], "Predators, disease and climate are examples."),
])
POOL5 = pool(R, [
    ("Mia models natural selection with coloured paper 'moths' on a newspaper background. Which colour will 'survive' best?", "grey moths that match the newspaper", ["bright red moths", "all colours equally", "the biggest moths"], "Camouflage reduces predation."),
    ("Jack grows bacteria on a plate with antibiotic. A few colonies survive and grow. What will their offspring be like?", "mostly resistant to the antibiotic", ["all killed by the antibiotic", "unchanged", "unable to reproduce"], "Resistant bacteria passed on their resistance."),
    ("Ruby graphs the percentage of resistant rabbits from 1950 to 1960. It rises from 5% to 60%. What does this show?", "the resistant trait became more common through natural selection", ["the rabbits learned resistance", "the virus disappeared", "the data is wrong"], "Change in a population over generations."),
    ("Kai compares skulls of different finches with different beaks. What type of evidence is this?", "comparative anatomy", ["fossil dating", "DNA sequencing", "a survey"], "Beak shape matches the food they eat."),
    ("Ella reads that a fossil shows features of both fish and four-legged animals. Why is it important?", "It is a transitional fossil showing a link between groups.", ["It proves fish never existed.", "It shows no evolution happened.", "It is a modern animal."], "Tiktaalik is a famous example."),
    ("Noah counts beak sizes in a bird population before and after a drought when only hard seeds were left. The average beak size increased. Why?", "Birds with larger beaks could crack hard seeds, survived and bred.", ["Birds grew bigger beaks on purpose.", "The drought made beaks grow.", "Small-beaked birds moved away only."], "This happened on the Galápagos Islands."),
    ("Zara reads that farmers who overuse one herbicide find more resistant weeds each year. What should they do?", "rotate different herbicides and control methods", ["use more of the same herbicide", "stop all weeding", "plant more weeds"], "Changing the selection pressure slows resistance."),
    ("Liam uses a model with beans of two colours to show allele frequencies over generations. What does each generation of picking represent?", "selection and reproduction in the population", ["a single mutation", "a fossil", "one organism's life"], "The bean ratio changes over generations."),
])


def main():
    sets = U.sets([
        ("Variation and natural selection", [(POOL1, 6), (v_var, 4), (v_cause, 3), (n_factor, 4), (n_b1, 3)]),
        ("Adaptation and selection pressures", [(n_scen, 6), (n_resist, 5), (t_sel, 4), (g_which, 3), (POOL1, 2)]),
        ("Speciation and extinction", [(s_iso, 5), (s_env, 5), (v_ext, 4), (POOL1, 3), (g_graph, 3)]),
        ("Evidence for evolution", [(e_struct, 5), (e_layer, 4), (e_dna, 4), (e_seq, 3), (e_b1, 3), (POOL1, 1)]),
        ("Investigations", [(POOL5, 7), (n_b5, 4), (e_b5, 4), (n_data, 3), (g_graph, 1), (g_which, 1)]),
    ])
    make_au(YEAR, "evolution-and-natural-selection", SORT, "AC9S10U02", "Biological sciences",
            "Use the theory of evolution by natural selection to explain past and present diversity and analyse the scientific evidence "
            "supporting the theory (summary of the Australian Curriculum v9.0 Science content description).",
            "Evolution and Natural Selection", "Evolution",
            "Free Year 10 science worksheets on evolution: variation, natural selection, adaptation, selection pressures, speciation, "
            "extinction, and evidence from fossils, comparative anatomy and DNA. 100 questions with answers.",
            "Populations evolve, not individuals.", "Individuals with helpful variations survive, reproduce and pass on their genes.",
            "<p><b>Evolution is a change in the inherited traits of a population over many generations.</b></p><ul>"
            "<li>Natural selection: variation exists; a selection pressure acts; the best suited survive and reproduce; their alleles become more common.</li>"
            "<li>Isolated populations can change so much they form new species (speciation).</li>"
            "<li>Evidence: fossils in rock layers, homologous structures, embryos and DNA similarities.</li></ul>",
            [("Myxomatosis 1950: why more resistant rabbits later?", ["some rabbits had resistance", "they survived and bred"], "resistance alleles became common"),
             ("Human arm and whale flipper: same bones. Evidence of?", ["homologous structures"], "a common ancestor")],
            ["Thinking an individual changes during its life to survive.", "Thinking organisms change because they 'need' or 'want' to.",
             "Thinking evolution has a goal or always makes organisms 'better'."],
            [("What is the difference between natural selection and evolution?", "Natural selection is the process: individuals with useful traits survive and reproduce more. Evolution is the result: the population's traits change over generations."),
             ("Why are antibiotic-resistant bacteria a problem?", "When antibiotics are overused, resistant bacteria survive and multiply, so infections become harder to treat."),
             ("What evidence supports evolution?", "Fossils in rock layers, similar bone structures in different species, similar early embryos, and DNA sequences that are more alike in closely related species.")],
            sets)


if __name__ == "__main__":
    main()
