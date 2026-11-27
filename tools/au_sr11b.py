# -*- coding: utf-8 -*-
"""Year 11 Biology (Australian Curriculum: Senior Secondary Biology, Units 1 and 2) for au_sr.build."""
from au_sr import SR

BIO = "Biology"

# ------------------------------------------------------------------ Unit 1: describing biodiversity
DIV = [
    ("What is biodiversity?", "the variety of life at the genetic, species and ecosystem levels", ["the number of animals in an area", "the total mass of plants in an ecosystem", "the number of endangered species in a country"], "Biodiversity includes genetic, species and ecosystem diversity."),
    ("What is genetic diversity?", "the variety of alleles and genes within a species", ["the number of different species in an area", "the variety of habitats in a region", "the number of individuals in a population"], "Genetic diversity is variation inside one species."),
    ("What is species diversity?", "the number of species in an area and how evenly the individuals are spread among them", ["the number of individuals of one species", "the variety of alleles in a population", "the variety of ecosystems in a region"], "Species diversity takes in richness and evenness."),
    ("What is ecosystem diversity?", "the variety of habitats, communities and ecological processes in a region", ["the number of species in one quadrat", "the variety of alleles in one species", "the size of the largest ecosystem"], "A region with reef, mangrove and seagrass has high ecosystem diversity."),
    ("What is species richness?", "the number of different species in an area", ["how evenly individuals are spread among species", "the total number of individuals", "the number of endemic species"], "Richness counts species; evenness compares their numbers."),
    ("What is species evenness?", "how similar the population sizes of the different species are", ["the number of different species", "the total biomass of the community", "the number of individuals of the rarest species"], "A community where one species dominates has low evenness."),
    ("Two sites each have 5 species. At site A each species has about 20 individuals; at site B one species has 90 and the rest have 2 or 3. Which is more diverse?", "site A, because it has the same richness and higher evenness", ["site B, because it has more individuals of one species", "they are equally diverse because richness is the same", "site B, because dominance means a healthier community"], "Same richness, higher evenness = higher diversity."),
    ("What is an endemic species?", "a species found naturally in only one region", ["a species introduced by people", "a species found on every continent", "a species that is extinct in the wild"], "About 87% of Australian mammals are endemic."),
    ("Which statement about Australia's biodiversity is correct?", "most of its mammals, reptiles and flowering plants are found nowhere else", ["it has fewer endemic species than most countries", "all its species arrived after European settlement", "it has no marsupials"], "Long isolation after Gondwana broke up led to high endemism."),
    ("Why does Australia have so many endemic species?", "it was isolated for tens of millions of years after it separated from Gondwana", ["it has the coldest climate on Earth", "it has the most rainfall of any continent", "species cannot migrate in deserts"], "Isolation allowed lineages such as marsupials to diversify."),
    ("What is a biodiversity hotspot?", "a region with very many endemic species that has lost much of its original habitat", ["a region with high temperatures", "a place where a single species is very common", "a national park"], "South-west Western Australia is a recognised hotspot."),
    ("Which Australian region is a recognised global biodiversity hotspot?", "south-west Western Australia", ["the Nullarbor Plain", "the Simpson Desert", "Bass Strait"], "It has thousands of endemic plant species."),
    ("Which is an example of ecosystem diversity on the Queensland coast?", "coral reef, seagrass meadow, mangrove forest and rainforest in one region", ["many kangaroos in one paddock", "different colours of one species of butterfly", "one crop planted over a large area"], "Ecosystem diversity is the variety of ecosystems."),
    ("Why is high genetic diversity important to a population?", "some individuals are more likely to survive a new disease or change", ["it stops all mutations", "it makes every individual identical", "it increases the population's size immediately"], "Variation is the raw material for natural selection."),
    ("Which population is most at risk from a new disease?", "a small, inbred population with low genetic diversity", ["a large population with many alleles", "a population of a widespread species", "a population with high immigration"], "Tasmanian devils have low genetic diversity, which helped facial tumour disease spread."),
    ("Tasmanian devils have very low genetic diversity. Why has this made devil facial tumour disease worse?", "their immune systems do not recognise tumour cells from other devils as foreign", ["the disease is caused by a mutation in the climate", "low diversity makes them grow too fast", "it means they cannot reproduce"], "Similar genes mean the tumour cells are not rejected."),
    ("What does ‘ecosystem services’ mean?", "the benefits people get from ecosystems, such as clean water, pollination and food", ["work done by park rangers", "money paid to visit a national park", "the number of species in an ecosystem"], "Mangroves protect coasts and act as fish nurseries."),
    ("Which is an ecosystem service of mangroves?", "protecting coastlines from erosion and providing nurseries for fish", ["producing most of the oxygen for cities", "removing salt from the ocean", "creating coal"], "Mangrove roots trap sediment and shelter young fish."),
    ("Which of these is the greatest current threat to Australian biodiversity?", "habitat loss and invasive species", ["volcanic eruptions", "too much genetic diversity", "earthquakes"], "Land clearing, foxes, cats and weeds have driven many extinctions."),
    ("How have feral cats and red foxes affected Australian mammals?", "they have caused the extinction of many small and medium-sized mammals", ["they have increased native mammal numbers", "they only eat insects", "they compete only with plants"], "Australia has the world's worst modern rate of mammal extinction."),
]
CLASS = [
    ("What are the three domains of life?", "Bacteria, Archaea and Eukarya", ["Animals, Plants and Fungi", "Prokaryotes, Viruses and Eukaryotes", "Monera, Protista and Fungi"], "The three-domain system is based on rRNA sequences."),
    ("Which domain includes all organisms with a nucleus?", "Eukarya", ["Bacteria", "Archaea", "Monera"], "Animals, plants, fungi and protists are eukaryotes."),
    ("Which domain includes many organisms that live in extreme environments such as hot springs?", "Archaea", ["Eukarya", "Fungi", "Plantae"], "Archaea are prokaryotes but differ from bacteria in their membranes and rRNA."),
    ("What evidence led to the three-domain system?", "comparisons of ribosomal RNA sequences", ["the shape of cells under a light microscope", "the colour of colonies", "whether organisms can move"], "rRNA showed Archaea are as different from Bacteria as from eukaryotes."),
    ("What is the correct order of taxa from largest to smallest?", "domain, kingdom, phylum, class, order, family, genus, species", ["kingdom, domain, phylum, class, order, family, genus, species", "domain, kingdom, class, phylum, family, order, genus, species", "species, genus, family, order, class, phylum, kingdom, domain"], "Each taxon is nested inside the one above."),
    ("What is the binomial name of the koala?", "<i>Phascolarctos cinereus</i>", ["<i>Cinereus phascolarctos</i>", "<i>Phascolarctus koala</i>", "Koala cinereus"], "Genus capitalised, species lower case, both in italics."),
    ("In <i>Macropus giganteus</i> (eastern grey kangaroo), what does <i>Macropus</i> name?", "the genus", ["the species", "the family", "the order"], "The first word of a binomial name is the genus."),
    ("Why do scientists use binomial names rather than common names?", "each species has one unique name understood worldwide", ["common names are always wrong", "binomial names describe the colour of the species", "binomial names are shorter"], "A ‘magpie’ in Australia and in Europe are different birds."),
    ("Which definition of a species is used for organisms that reproduce sexually?", "a group that can interbreed in nature to produce fertile offspring", ["a group of organisms that look the same", "all organisms that live in one habitat", "a group of organisms with the same diet"], "This is the biological species concept."),
    ("A horse and a donkey produce a mule, which is sterile. What does this show?", "horses and donkeys are separate species", ["horses and donkeys are the same species", "mules are a new species", "donkeys are a subspecies of horse"], "Hybrids are not fertile, so the parents are different species."),
    ("Why is the biological species concept hard to use for bacteria?", "they reproduce asexually, so interbreeding cannot be tested", ["they are too large to study", "they have no DNA", "they all belong to one species"], "Other concepts (genetic, morphological) are used instead."),
    ("What does a dichotomous key do?", "identifies organisms by a series of choices between two features", ["shows how energy flows through an ecosystem", "measures the size of a population", "lists organisms in order of size"], "Each step splits the group into two."),
    ("Which feature is best for a dichotomous key?", "a feature that does not change, such as number of legs", ["the time of day the organism was seen", "whether the organism is moving", "its colour after it has died"], "Use features that are fixed and easy to observe."),
    ("Which group of mammals lays eggs?", "monotremes, such as the platypus and echidnas", ["marsupials, such as kangaroos", "placental mammals, such as dingoes", "bats"], "Monotremes are found only in Australia and New Guinea."),
    ("What feature defines marsupials?", "young are born very small and usually develop in a pouch", ["they lay eggs with shells", "they have no hair", "they have a long placental pregnancy"], "Kangaroos, koalas and wombats are marsupials."),
    ("Which statement about classification is correct?", "organisms in the same genus are more closely related than organisms in the same order", ["organisms in the same kingdom are always the same species", "a family contains several orders", "a class is smaller than a genus"], "Lower taxa share more features."),
    ("A cladogram shows that kangaroos and koalas share a more recent common ancestor than kangaroos and platypuses. What does this mean?", "kangaroos are more closely related to koalas than to platypuses", ["platypuses evolved from kangaroos", "koalas are older than kangaroos", "kangaroos and platypuses are the same species"], "A more recent common ancestor means a closer relationship."),
    ("Why is DNA sequencing now used to classify organisms?", "it shows relationships that are hidden by similar or different body shapes", ["it is cheaper than looking at organisms", "it removes the need for names", "every species has identical DNA"], "Convergent evolution can make unrelated organisms look alike."),
]
SAMP = [
    ("When is a quadrat the best sampling method?", "for plants or slow-moving animals in an area", ["for fast-moving birds", "for fish in deep water", "for animals that are active only at night"], "Quadrats sample a fixed area."),
    ("When is a belt transect used?", "to show how a community changes along an environmental gradient", ["to count every organism in a forest", "to measure the age of a tree", "to catch flying insects"], "A transect across a rocky shore shows zonation."),
    ("Why are quadrats placed at random?", "to avoid bias in choosing where to sample", ["to make the work faster", "to make sure the rarest species is found", "so each quadrat has the same number of species"], "Random positions come from random-number coordinates."),
    ("Which method is used to estimate the population of a mobile animal such as a skink?", "capture–mark–recapture", ["a quadrat", "a line transect of plants", "counting every animal"], "Lincoln index: N = (n₁ × n₂) ÷ m₂."),
    ("Which assumption is made in capture–mark–recapture?", "marked animals mix back into the population and are not harmed by the mark", ["no animals are born during the whole year", "all animals are caught the first time", "marked animals are easier to catch"], "Marks must not affect survival or behaviour."),
    ("What does percentage cover measure?", "the proportion of a quadrat's area covered by one species", ["the number of individuals in a quadrat", "the height of the tallest plant", "the number of species in the area"], "Useful for grasses and mosses that are hard to count."),
    ("Why are many quadrats used instead of one?", "the mean of many samples is more representative of the whole area", ["one quadrat is always too big", "to make sure the results are identical", "each quadrat must hold a different species"], "More samples reduce the effect of chance."),
    ("A student uses a pitfall trap. What is it for?", "catching small ground-dwelling invertebrates", ["sampling trees", "counting birds", "measuring soil pH"], "Pitfall traps are checked often so animals are not harmed."),
    ("Which tool is used to sample invertebrates in long grass?", "a sweep net", ["a quadrat", "a light meter", "a clinometer"], "Sweep nets are swung through vegetation."),
    ("What is the purpose of a remote sensing camera (camera trap) in ecology?", "recording shy or night-active animals without disturbing them", ["counting plants in a quadrat", "measuring the abiotic factors of a site", "catching animals for marking"], "Camera traps are widely used for quolls and bandicoots."),
    ("What is environmental DNA (eDNA) sampling?", "detecting species from DNA left in water or soil", ["counting animals by their footprints", "sampling plants with a quadrat", "photographing birds"], "eDNA can detect platypuses in a creek."),
    ("Which abiotic factor is measured with a light meter on a transect?", "light intensity", ["soil pH", "humidity", "wind direction"], "Abiotic data help explain the pattern of organisms."),
]


def u1(X):
    return [
        ("Levels of biodiversity", [(X.pool(DIV), 18), (X.ch("in_s12b", "biodiversity-and-conservation", 1), 2)]),
        ("Classification and naming", [(X.pool(CLASS), 14), (X.ch("in_s11b", "the-living-world", 2), 2), (X.ch("in_s11b", "the-living-world", 3), 4)]),
        ("Sampling methods", [(X.pool(SAMP), 8), (X.ch("al_bio", "genetics-populations-and-evolution", 5, 13), 12)]),
        ("Simpson's index of diversity", [(X.ch("al_bio", "genetic-information-and-variation", 5, 12), 20)]),
        ("Investigating biodiversity", [(X.ch("al_bio", "genetic-information-and-variation", 5, 12), 8), (X.ch("al_bio", "genetics-populations-and-evolution", 5, 13), 6),
                                        (X.pool(DIV), 2), (X.pool(SAMP), 2), (X.pool(CLASS), 2)]),
    ]


# ------------------------------------------------------------------ Unit 1: ecosystem dynamics
INTER = [
    ("A remora fish attaches to a shark and eats scraps of its food; the shark is not affected. What is this relationship?", "commensalism", ["mutualism", "parasitism", "predation"], "One benefits, the other is unaffected."),
    ("Clownfish shelter in sea anemones and keep them clean; the anemone's stinging cells protect the fish. What is this relationship?", "mutualism", ["commensalism", "parasitism", "competition"], "Both species benefit."),
    ("Reef-building corals and the algae (zooxanthellae) in their tissues both benefit. What is this relationship?", "mutualism", ["parasitism", "commensalism", "amensalism"], "The algae give sugars; the coral gives shelter and nutrients."),
    ("A tick feeds on the blood of a bandicoot. What is this relationship?", "parasitism", ["mutualism", "commensalism", "predation"], "The parasite benefits and the host is harmed."),
    ("Mistletoe takes water and minerals from a eucalyptus. What is the mistletoe?", "a parasite", ["a decomposer", "a mutualist", "a predator"], "Mistletoes are partial parasites of trees."),
    ("Two species of honeyeater feed on the same flowers. What is this?", "interspecific competition", ["intraspecific competition", "mutualism", "commensalism"], "Competition between different species."),
    ("Male kangaroos fight for mates. What is this?", "intraspecific competition", ["interspecific competition", "predation", "mutualism"], "Competition within one species."),
    ("What is a keystone species?", "a species whose effect on its ecosystem is much larger than its numbers suggest", ["the most common species in an ecosystem", "the largest species in a food web", "a species found only in one place"], "Removing it changes the whole community."),
    ("Dingoes control kangaroo and fox numbers in some areas. What role does this suggest dingoes play?", "a keystone (apex) predator", ["a decomposer", "a producer", "a parasite"], "Apex predators shape the whole food web."),
    ("What is an ecological niche?", "the role of a species, including what it eats, where it lives and how it interacts with others", ["the place where a species lives only", "the number of individuals of a species", "the food chain a species belongs to"], "The habitat is only part of the niche."),
    ("What does the competitive exclusion principle state?", "two species cannot share exactly the same niche for long in one place", ["all species compete equally", "predators always outcompete prey", "competition increases both populations"], "One species will outcompete the other."),
    ("What is primary succession?", "colonisation of bare rock or new land where there was no soil", ["regrowth of a forest after a bushfire", "the death of an ecosystem", "the arrival of predators in a new area"], "Lichens and mosses are pioneer species."),
    ("What is secondary succession?", "regrowth of a community where soil remains after a disturbance such as fire", ["colonisation of new volcanic rock", "a food chain with two consumers", "the migration of birds"], "It is faster because soil and seeds are already there."),
    ("Why do many Australian plants, such as banksias, depend on fire?", "heat or smoke triggers their seeds to be released or to germinate", ["fire kills all competitors forever", "fire adds nitrogen gas to the air", "their leaves need ash to photosynthesise"], "Many species are adapted to particular fire regimes."),
    ("What is a pioneer species?", "the first organism to colonise bare ground, such as lichen", ["the largest tree in a forest", "the top predator", "a species brought by people"], "Pioneers start to form soil."),
    ("What is the carrying capacity of an environment?", "the largest population it can support for a long time", ["the number of species it contains", "the fastest rate at which a population can grow", "the total energy entering it"], "Limited by food, water, space and other resources."),
    ("Which factor is density-dependent?", "competition for food", ["a severe frost", "a bushfire", "a flood"], "Its effect grows as the population becomes denser."),
    ("Which factor is density-independent?", "a drought", ["disease spreading through a crowded colony", "competition for nest hollows", "predation that increases with prey numbers"], "Drought affects a population whatever its density."),
    ("Rabbits were released in Australia in 1859 and spread rapidly. Why did their population grow so fast?", "they had plenty of food and few predators or diseases", ["they were the native predator", "the climate was too cold for them", "they competed with no plants"], "Myxoma virus and calicivirus were later released to control them."),
    ("Which interaction is shown when a lyrebird and a bandicoot both dig in the leaf litter for the same insects?", "interspecific competition", ["mutualism", "commensalism", "parasitism"], "Two species use the same limited resource."),
    ("Yellow-tailed black cockatoos rip open branches to eat beetle larvae. What is the relationship between the cockatoo and the larvae?", "predation", ["mutualism", "commensalism", "parasitism"], "The predator kills and eats its prey."),
    ("Mycorrhizal fungi grow around plant roots, getting sugars and giving the plant phosphate. What is this relationship?", "mutualism", ["parasitism", "commensalism", "competition"], "Many Australian plants rely on mycorrhizae in poor soils."),
    ("A predator–prey graph shows the predator population peaking after the prey population. Why?", "predators increase only after there is plenty of prey, then fall when prey run short", ["predators breed faster than prey", "the prey eat the predators", "the two populations are not linked"], "The cycles are linked but out of step."),
    ("Cane toads were introduced to Queensland in 1935. Why have they harmed native predators?", "the toads are toxic and predators such as quolls die after eating them", ["toads eat all the eucalyptus leaves", "toads are parasites of kangaroos", "toads pollinate weeds"], "Northern quoll numbers dropped as toads spread."),
]
FLOW = [
    ("Why is energy lost between trophic levels?", "much is used in respiration and released as heat, and some is in undigested waste", ["energy is destroyed at each level", "all the energy is stored as biomass", "consumers make energy from food"], "Typically only about 10% passes to the next level."),
    ("Which process returns nutrients from dead organisms to the soil?", "decomposition by bacteria and fungi", ["photosynthesis", "transpiration", "predation"], "Decomposers recycle matter, not energy."),
    ("Why do food chains rarely have more than four or five links?", "too little energy is left at the top to support another level", ["predators are too big", "there is too much biomass at the top", "plants cannot support more than one consumer"], "Energy decreases at each trophic level."),
    ("Which statement about matter and energy in ecosystems is correct?", "matter is recycled, but energy flows through and is lost as heat", ["energy is recycled, but matter is lost", "both are recycled", "neither is recycled"], "Energy enters as sunlight and leaves as heat."),
    ("What does a pyramid of biomass show?", "the dry mass of organisms at each trophic level", ["the number of organisms at each level", "the energy used in respiration", "the age of each organism"], "Biomass is measured per unit area."),
    ("A single eucalyptus supports thousands of caterpillars. What shape is the pyramid of numbers?", "inverted at the base (one producer, many consumers)", ["upright", "a perfect rectangle", "it cannot be drawn"], "Pyramids of numbers can be inverted; pyramids of energy cannot."),
    ("Which pyramid can never be inverted?", "a pyramid of energy", ["a pyramid of numbers", "a pyramid of biomass", "a pyramid of age"], "Energy always decreases up the levels."),
    ("What is the role of producers?", "converting light energy into chemical energy in organic molecules", ["breaking down dead material", "eating herbivores", "releasing all their energy as heat"], "Producers fix energy by photosynthesis."),
    ("What is a trophic level?", "a feeding position in a food chain", ["the height of an organism", "the number of organisms in a habitat", "a type of habitat"], "Producers are level 1, herbivores level 2."),
    ("In a food web, what happens to the number of crickets if most of the frogs that eat them are removed?", "crickets increase at first", ["crickets decrease at once", "crickets are not affected", "crickets become producers"], "Less predation lets the prey population grow."),
]


def u2(X):
    return [
        ("Interactions and niches", [(X.pool(INTER), 14), (X.gen("gen_us_science_bio_ecosystem_stability_and_biodiversity", "g_succ"), 3), (X.ch("in_s12b", "organisms-and-populations", 4), 3)]),
        ("Energy flow and trophic levels", [(X.pool(FLOW), 6), (X.ch("in_s12b", "ecosystem", 4), 14)]),
        ("Productivity and efficiency", [(X.ch("in_s12b", "ecosystem", 3), 10), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 4, 13), 6), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 5, 13), 4)]),
        ("Population growth and carrying capacity", [(X.ch("in_s12b", "organisms-and-populations", 2), 10), (X.gen("gen_us_science_bio_populations_and_carrying_capacity", "g_logistic"), 6), (X.pool(INTER), 4)]),
        ("Ecosystem change and succession", [(X.pool(INTER), 6), (X.pool(FLOW), 2), (X.ch("in_s12b", "ecosystem", 5, drop=["always upright"]), 6), (X.ch("in_s12b", "organisms-and-populations", 2), 6)]),
    ]


# ------------------------------------------------------------------ Unit 2: cells
MEMB = [
    ("What is the fluid mosaic model?", "a phospholipid bilayer with proteins that can move within it", ["a rigid wall of cellulose", "a single layer of protein", "a layer of DNA around the cell"], "Proteins float in a fluid bilayer."),
    ("Why do phospholipids form a bilayer in water?", "their phosphate heads are hydrophilic and their fatty acid tails are hydrophobic", ["both ends are hydrophobic", "both ends are hydrophilic", "they bond to cellulose"], "Tails face inwards away from water."),
    ("What is diffusion?", "net movement of particles from a higher to a lower concentration", ["movement against a concentration gradient using ATP", "movement of water only", "movement of large particles in vesicles"], "Diffusion is passive."),
    ("What is osmosis?", "net movement of water across a partially permeable membrane from a dilute to a more concentrated solution", ["movement of salt across a membrane", "active uptake of water", "movement of any particle from high to low concentration"], "Water moves towards the higher solute concentration."),
    ("What is facilitated diffusion?", "passive movement through channel or carrier proteins", ["movement using ATP", "movement through the phospholipids only", "engulfing particles"], "Glucose and ions often need protein channels."),
    ("What is active transport?", "movement against a concentration gradient using carrier proteins and ATP", ["movement down a gradient with no energy", "movement of water by osmosis", "diffusion through the bilayer"], "Root hair cells take up mineral ions this way."),
    ("Which process moves large particles out of a cell in vesicles?", "exocytosis", ["endocytosis", "osmosis", "diffusion"], "Vesicles fuse with the membrane to release their contents."),
    ("How does a white blood cell take in a bacterium?", "phagocytosis, a type of endocytosis", ["exocytosis", "osmosis", "facilitated diffusion"], "The membrane surrounds the particle."),
    ("A red blood cell is placed in pure water. What happens?", "water enters by osmosis and the cell may burst", ["water leaves and the cell shrinks", "nothing happens", "the cell wall stops it bursting"], "Animal cells have no cell wall."),
    ("A plant cell is placed in a concentrated salt solution. What happens?", "water leaves and the cell becomes plasmolysed", ["water enters and the cell bursts", "the cell wall dissolves", "the cell takes in salt by osmosis"], "The membrane pulls away from the cell wall."),
    ("Which molecule can diffuse directly through the phospholipid bilayer?", "oxygen", ["glucose", "sodium ions", "proteins"], "Small, non-polar molecules pass easily."),
    ("Which factor increases the rate of diffusion?", "a larger surface area", ["a thicker membrane", "a smaller concentration difference", "a lower temperature"], "Fick's law: rate ∝ area × difference ÷ thickness."),
    ("Why must cells stay small?", "as a cell grows, its surface area to volume ratio falls, so exchange becomes too slow", ["large cells cannot hold DNA", "large cells are too heavy", "small cells need more energy"], "Volume grows faster than surface area."),
    ("Which statement compares prokaryotic and eukaryotic cells correctly?", "only eukaryotic cells have a nucleus and membrane-bound organelles", ["only prokaryotic cells have ribosomes", "eukaryotic cells are always smaller", "prokaryotic cells have mitochondria"], "Both have a membrane, cytoplasm, ribosomes and DNA."),
    ("What is the evidence that mitochondria were once free-living bacteria?", "they have their own circular DNA, 70S ribosomes and a double membrane", ["they are found in every prokaryote", "they make glucose", "they are bigger than the nucleus"], "This is the endosymbiotic theory."),
    ("Which structure is found in plant cells but not animal cells?", "a cellulose cell wall", ["a cell membrane", "mitochondria", "ribosomes"], "Plant cells also have chloroplasts and a large vacuole."),
]


def u3(X):
    return [
        ("Prokaryotic and eukaryotic cells", [(X.ch("al_bio", "cells-and-the-immune-system", 1, 12), 12), (X.ch("in_s11b", "cell-the-unit-of-life", 2), 6), (X.pool(MEMB), 2)]),
        ("Organelles and their functions", [(X.ch("in_s11b", "cell-the-unit-of-life", 3), 14), (X.ch("in_s11b", "cell-the-unit-of-life", 1), 6)]),
        ("Microscopy and magnification", [(X.ch("al_bio", "cells-and-the-immune-system", 2, 12), 20)]),
        ("Membranes and transport", [(X.pool(MEMB), 10), (X.ch("al_bio", "cells-and-the-immune-system", 3, 12), 10)]),
        ("Surface area to volume ratio", [(X.ch("al_bio", "exchange-and-transport", 1, 12), 18), (X.pool(MEMB), 2)]),
    ]


# ------------------------------------------------------------------ Unit 2: energy in cells
ENER = [
    ("What is the word equation for photosynthesis?", "carbon dioxide + water → glucose + oxygen (in light, with chlorophyll)", ["glucose + oxygen → carbon dioxide + water", "glucose → lactate", "oxygen + water → glucose + carbon dioxide"], "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂."),
    ("What is the word equation for aerobic respiration?", "glucose + oxygen → carbon dioxide + water (+ ATP)", ["carbon dioxide + water → glucose + oxygen", "glucose → ethanol + carbon dioxide", "glucose → lactate"], "It releases energy as ATP."),
    ("Where do the light-dependent reactions of photosynthesis take place?", "on the thylakoid membranes of the chloroplast", ["in the stroma", "in the mitochondrial matrix", "in the cytoplasm"], "Chlorophyll is in the thylakoids."),
    ("Where does the Calvin cycle (light-independent reactions) take place?", "in the stroma of the chloroplast", ["on the thylakoid membranes", "in the nucleus", "in the cristae of mitochondria"], "CO₂ is fixed by the enzyme RuBisCO."),
    ("What do the light-dependent reactions supply to the Calvin cycle?", "ATP and NADPH", ["glucose and oxygen", "carbon dioxide and water", "pyruvate"], "Water is split and oxygen is released."),
    ("Where does glycolysis take place?", "in the cytoplasm", ["in the mitochondrial matrix", "on the cristae", "in the chloroplast"], "Glucose is split into two pyruvate."),
    ("Where does the electron transport chain of aerobic respiration take place?", "on the inner membrane (cristae) of the mitochondrion", ["in the cytoplasm", "in the stroma", "in the nucleus"], "Most ATP is made here."),
    ("About how many ATP are made from one glucose in aerobic respiration?", "about 30–38", ["2", "4", "about 1000"], "Anaerobic respiration gives only 2."),
    ("What is made in anaerobic respiration in human muscle?", "lactate (lactic acid)", ["ethanol and carbon dioxide", "glucose", "oxygen"], "Yeast makes ethanol and CO₂ instead."),
    ("Why is anaerobic respiration much less efficient than aerobic respiration?", "glucose is only partly broken down, so much less ATP is made", ["it uses more oxygen", "it makes no ATP at all", "it happens in the mitochondria"], "Energy is left in lactate or ethanol."),
    ("What is the role of ATP in cells?", "it carries energy from respiration to reactions that need it", ["it stores genetic information", "it is a structural protein", "it is the main component of membranes"], "ATP → ADP + Pi releases energy."),
    ("What is an enzyme?", "a protein that is a biological catalyst", ["a carbohydrate that stores energy", "a lipid in the cell membrane", "a hormone that controls growth"], "Enzymes speed up reactions and are not used up."),
    ("Why does each enzyme work on only one substrate?", "the active site has a shape that fits only that substrate", ["enzymes are too large for other substrates", "all substrates have the same shape", "enzymes are used up after one reaction"], "Lock-and-key and induced-fit models."),
    ("What happens to an enzyme at a very high temperature?", "it is denatured: the active site changes shape and the substrate no longer fits", ["it works faster and faster", "it becomes a new enzyme", "it is unchanged"], "Bonds holding the shape break."),
    ("Why does the rate of an enzyme reaction rise between 10 °C and 35 °C?", "molecules have more kinetic energy, so enzyme–substrate collisions are more frequent", ["the enzyme is denatured", "the substrate is used up", "the pH falls"], "Above the optimum, denaturation takes over."),
    ("A competitive inhibitor slows an enzyme. How does it work?", "it has a similar shape to the substrate and blocks the active site", ["it changes the temperature", "it destroys the substrate", "it binds to DNA"], "Adding more substrate reduces its effect."),
    ("Which factor would NOT increase the rate of photosynthesis in a plant already in bright light at 25 °C with low CO₂?", "more light", ["more carbon dioxide", "a slightly warmer temperature up to the optimum", "more chlorophyll in the leaves"], "When CO₂ is limiting, extra light makes no difference."),
    ("What is a limiting factor?", "the factor that is in shortest supply and so controls the rate", ["the factor that is present in excess", "a factor that stops a reaction for ever", "the temperature at which an enzyme denatures"], "Light, CO₂ and temperature limit photosynthesis."),
]


def u4(X):
    return [
        ("Enzymes", [(X.pool(ENER), 4), (X.ch("al_bio", "biological-molecules", 2, 12), 8), (X.ch("in_s11b", "biomolecules", 4), 8)]),
        ("Photosynthesis", [(X.pool(ENER), 4), (X.ch("in_s11b", "photosynthesis-in-higher-plants", 2), 12), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 1, 13), 4)]),
        ("Cellular respiration", [(X.pool(ENER), 4), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 2, 13), 6), (X.ch("in_s11b", "respiration-in-plants", 1), 10)]),
        ("ATP and comparing the processes", [(X.pool(ENER), 4), (X.ch("in_s11b", "respiration-in-plants", 1), 8), (X.ch("in_s11b", "photosynthesis-in-higher-plants", 2), 8)]),
        ("Investigating enzymes and photosynthesis", [(X.ch("al_bio", "biological-molecules", 2, 12), 10), (X.ch("al_bio", "photosynthesis-respiration-and-energy-transfer", 1, 13), 10)]),
    ]


# ------------------------------------------------------------------ Unit 2: multicellular organisms
MULTI = [
    ("What is the correct order of organisation in a multicellular organism?", "cells → tissues → organs → systems → organism", ["tissues → cells → organs → systems", "organs → tissues → cells → systems", "cells → organs → tissues → systems"], "Specialised cells form tissues."),
    ("What is cell differentiation?", "a cell becoming specialised for one function by switching on particular genes", ["a cell dividing into two", "a cell losing all its DNA", "two cells joining together"], "All body cells have the same genes but use different ones."),
    ("What is a stem cell?", "an unspecialised cell that can divide and become specialised cells", ["a cell found only in plant stems", "a fully specialised muscle cell", "a cell with no nucleus"], "Embryonic stem cells can form any cell type."),
    ("Why do multicellular organisms need transport systems?", "their small surface area to volume ratio means diffusion alone is too slow", ["each cell can make its own oxygen", "they have a larger surface area to volume ratio than single cells", "their cells do not need nutrients"], "Blood and xylem carry materials over long distances."),
    ("How are alveoli adapted for gas exchange?", "a huge surface area, walls one cell thick and a rich blood supply", ["thick walls to stop damage", "few capillaries", "a small surface area"], "Short diffusion distance and a steep gradient."),
    ("How are the villi of the small intestine adapted?", "they have a large surface area, thin walls and many capillaries", ["they are thick and waxy", "they have few blood vessels", "they release digestive enzymes into the blood"], "Microvilli increase the area further."),
    ("Which blood vessels carry blood away from the heart at high pressure?", "arteries", ["veins", "capillaries", "lymph vessels"], "Arteries have thick, elastic walls."),
    ("Why do veins have valves?", "to stop blood flowing backwards at low pressure", ["to raise blood pressure", "to make red blood cells", "to exchange gases"], "Skeletal muscles squeeze veins to push blood."),
    ("Why does the left ventricle have a thicker wall than the right ventricle?", "it pumps blood all round the body, which needs higher pressure", ["it receives blood from the lungs", "it holds more blood", "it pumps deoxygenated blood"], "The right ventricle pumps only to the lungs."),
    ("What is the double circulation of mammals?", "blood passes through the heart twice in each full circuit: to the lungs and to the body", ["blood goes to the lungs twice", "there are two hearts", "blood moves in both directions in each vessel"], "It keeps pressure high in the body circuit."),
    ("What does xylem carry in a plant?", "water and mineral ions from the roots to the leaves", ["sugars from the leaves to the roots", "oxygen to the roots", "hormones only"], "Xylem vessels are dead, hollow tubes."),
    ("What does phloem carry?", "sugars and other organic substances, in both directions (translocation)", ["water from roots to leaves only", "carbon dioxide", "mineral ions only"], "Sieve tubes and companion cells."),
    ("What drives the movement of water up the xylem?", "transpiration: evaporation from leaves pulls a column of water up (cohesion–tension)", ["active pumping by the xylem", "gravity", "photosynthesis in the roots"], "Water molecules stick together (cohesion)."),
    ("Which change increases the rate of transpiration?", "a hot, dry, windy day", ["a humid, still day", "closing the stomata", "a cold night"], "Evaporation is faster in dry, warm, moving air."),
    ("How do guard cells control water loss?", "they change shape to open or close the stomata", ["they make the leaf waxy", "they pump water into the xylem", "they absorb carbon dioxide only"], "Stomata close when the plant is short of water."),
    ("Many Australian plants, such as eucalyptus, have tough leaves that hang vertically. How does this help?", "it reduces heating and water loss in strong midday sun", ["it increases water loss", "it lets the plant absorb more water through its leaves", "it attracts more pollinators"], "Hanging leaves receive less direct midday sun."),
    ("Which digestive enzyme breaks down starch?", "amylase", ["protease", "lipase", "bile"], "Amylase is made in the salivary glands and pancreas."),
    ("Which enzyme breaks down proteins in the stomach?", "pepsin, a protease that works best in acid", ["amylase", "lipase", "maltase"], "Stomach acid gives a pH of about 2."),
    ("What are the products of fat digestion?", "fatty acids and glycerol", ["amino acids", "glucose", "nucleotides"], "Lipase breaks down lipids."),
    ("Why does the stomach make hydrochloric acid?", "it kills many microorganisms and gives the low pH that pepsin needs", ["it digests starch", "it absorbs water", "it neutralises bile"], "Mucus protects the stomach wall."),
    ("Where is most water absorbed from the gut?", "the small intestine, with more absorbed in the large intestine", ["the stomach", "the oesophagus", "the mouth"], "The colon absorbs the remaining water."),
    ("Why are digested food molecules such as glucose absorbed by active transport as well as diffusion?", "so they can be absorbed even when their concentration in the gut is lower than in the blood", ["because they are too big to diffuse", "because diffusion needs ATP", "because active transport is slower"], "Active transport works against the gradient."),
    ("What is the role of the lacteal in a villus?", "it absorbs fatty acids and glycerol into the lymph", ["it absorbs glucose into the blood", "it makes digestive enzymes", "it stores bile"], "Each villus has a lacteal and capillaries."),
    ("What is the role of bile in digestion?", "it emulsifies fats into small droplets so lipase can work faster", ["it digests proteins", "it absorbs glucose", "it neutralises stomach acid only"], "Bile is made in the liver and stored in the gall bladder."),
]


def u5(X):
    return [
        ("Specialised cells and organisation", [(X.pool(MULTI), 4), (X.gen("gen_us_science_bio_levels_of_organization", "g_level"), 6), (X.gen("gen_us_science_bio_levels_of_organization", "g_sys"), 4), (X.ch("al_bio", "exchange-and-transport", 1, 12), 6)]),
        ("Gas exchange", [(X.ch("al_bio", "exchange-and-transport", 2, 12), 12), (X.ch("in_s11b", "breathing-and-exchange-of-gases", 1), 5), (X.pool(MULTI), 3)]),
        ("The heart and circulation", [(X.ch("al_bio", "exchange-and-transport", 3, 12), 12), (X.ch("al_bio", "exchange-and-transport", 4, 12), 5), (X.pool(MULTI), 3)]),
        ("Digestion and absorption", [(X.pool(MULTI), 8), (X.gen("gen_uk_science_y8_food_and_digestion", "g_enz"), 5), (X.ch("al_bio", "exchange-and-transport", 1, 12), 7)]),
        ("Transport in plants", [(X.ch("al_bio", "exchange-and-transport", 5, 12), 16), (X.pool(MULTI), 4)]),
    ]


def UNITS():
    return [
        SR(BIO, 1, 1, "biodiversity-and-classification", "Describing biodiversity",
           "Biodiversity at the genetic, species and ecosystem levels; classification systems, binomial nomenclature and dichotomous keys; sampling with quadrats, transects and capture–recapture; and diversity indices.",
           "Biodiversity, Classification and Sampling", "biodiversity and classification",
           "Free Year 11 Biology worksheets on biodiversity: genetic, species and ecosystem diversity, the three domains, binomial names, keys, quadrats, capture–recapture and Simpson's index. 100 questions with answers.",
           "Diversity = richness + evenness.", "Simpson's index: D = 1 − Σn(n − 1) ÷ N(N − 1). Closer to 1 = more diverse.",
           "<p>Biodiversity is the variety of life at three levels: <b>genetic</b> (alleles within a species), <b>species</b> (how many species and how evenly they are spread) and <b>ecosystem</b> (the variety of habitats). Australia's long isolation gives it very high endemism.</p>"
           "<p>Organisms are grouped into three domains (Bacteria, Archaea, Eukarya) and then kingdom, phylum, class, order, family, genus and species. Each species has a binomial name such as <i>Phascolarctos cinereus</i>.</p>"
           "<p>Sample plants with random quadrats and gradients with transects; estimate mobile animals with capture–mark–recapture, N = (n₁ × n₂) ÷ m₂.</p>",
           [("Quadrats: A 10, B 5, C 5. Find Simpson's index.", ["N = 20, Σn(n − 1) = 90 + 20 + 20 = 130", "D = 1 − 130 ÷ (20 × 19)"], "0.658"),
            ("30 skinks marked; later 20 caught, 4 marked. Population?", ["N = 30 × 20 ÷ 4"], "150")],
           ["Thinking more individuals means more diversity: evenness matters too.", "Writing the binomial name with a capital letter for the species.", "Placing quadrats where the plants look interesting instead of at random."],
           [("What does Simpson's index tell you?", "How diverse a community is, from 0 (one species) towards 1 (many species with similar numbers). It combines richness and evenness."),
            ("Why is Australian biodiversity so unusual?", "Australia was isolated for tens of millions of years, so most of its mammals, reptiles and flowering plants are endemic: found nowhere else.")],
           u1),
        SR(BIO, 1, 2, "ecosystem-dynamics", "Ecosystem dynamics",
           "Interactions between organisms (predation, competition, symbiosis); keystone species and niches; energy flow, trophic levels and productivity; population growth and carrying capacity; succession and the effects of disturbance and introduced species.",
           "Ecosystem Dynamics: Interactions, Energy and Populations", "ecosystem dynamics",
           "Free Year 11 Biology worksheets on ecosystem dynamics: symbiosis, keystone species, energy flow, productivity, the 10% rule, population growth, carrying capacity and succession. 100 questions with answers.",
           "Energy flows through ecosystems; matter cycles.", "About 10% of energy passes to the next trophic level.",
           "<p>Organisms interact by predation, competition and symbiosis (mutualism, commensalism, parasitism). A <b>keystone species</b>, such as an apex predator, has a large effect on its community.</p>"
           "<p>Producers fix energy; at each trophic level most energy is used in respiration and lost as heat, so only about 10% passes on. Net primary productivity = gross primary productivity − respiration.</p>"
           "<p>Populations grow until limiting factors hold them near the <b>carrying capacity</b>. After disturbance, communities change by succession.</p>",
           [("Producers fix 20 000 kJ. How much reaches the secondary consumers (10% rule)?", ["20 000 × 0.1 = 2000 kJ (primary)", "2000 × 0.1"], "200 kJ"),
            ("GPP = 5000, respiration = 3000 (kJ m⁻² yr⁻¹). NPP?", ["NPP = GPP − R"], "2000 kJ m⁻² yr⁻¹")],
           ["Saying energy is recycled: only matter is recycled.", "Mixing up commensalism (one unaffected) and mutualism (both benefit).", "Thinking a population keeps growing forever: limiting factors set a carrying capacity."],
           [("What is the difference between gross and net primary productivity?", "GPP is all the energy fixed by producers; NPP is what is left after their respiration, available to consumers."),
            ("What makes a species a keystone species?", "Its effect on the ecosystem is far larger than its numbers suggest; removing it changes the whole community, as with apex predators or reef-building corals.")],
           u2),
        SR(BIO, 2, 3, "cells-and-membranes", "Cells as the basis of life",
           "Prokaryotic and eukaryotic cells; organelles and their functions; measuring cells with microscopes; the fluid mosaic model; diffusion, osmosis, facilitated diffusion, active transport and bulk transport; surface area to volume ratio.",
           "Cells, Organelles and Membrane Transport", "cells and membranes",
           "Free Year 11 Biology worksheets on cells: prokaryotes and eukaryotes, organelles, magnification, the fluid mosaic model, diffusion, osmosis, active transport and SA:V ratio. 100 questions with answers.",
           "Magnification = image size ÷ actual size.", "Convert to the same unit first: 1 mm = 1000 µm.",
           "<p>Prokaryotic cells (bacteria, archaea) have no nucleus or membrane-bound organelles; eukaryotic cells do. Organelles divide the work: mitochondria release energy, ribosomes make proteins, chloroplasts photosynthesise.</p>"
           "<p>The membrane is a phospholipid bilayer with proteins (fluid mosaic model). Substances cross by <b>diffusion</b>, <b>osmosis</b> (water), facilitated diffusion, <b>active transport</b> (needs ATP) and endo- or exocytosis.</p>"
           "<p>As a cell gets bigger its surface area to volume ratio falls, so exchange becomes too slow; that is why cells are small.</p>",
           [("An image 30 mm long shows a cell 15 µm long. Magnification?", ["30 mm = 30 000 µm", "30 000 ÷ 15"], "×2000"),
            ("Cube with 2 cm sides: SA:V?", ["SA = 6 × 4 = 24 cm²", "V = 8 cm³", "24 ÷ 8"], "3 : 1")],
           ["Forgetting to convert mm to µm before dividing.", "Saying water moves by osmosis towards the more dilute solution: it moves to the more concentrated one.", "Calling active transport ‘diffusion with energy’: it moves substances against the gradient."],
           [("What is the difference between osmosis and diffusion?", "Both are passive. Osmosis is the diffusion of water through a partially permeable membrane; diffusion can be any particle."),
            ("Why do large cells have trouble exchanging materials?", "Volume increases faster than surface area, so each unit of volume has less membrane for exchange.")],
           u3),
        SR(BIO, 2, 4, "enzymes-photosynthesis-and-respiration", "Cells as the basis of life",
           "Enzymes as biological catalysts and the factors that affect their activity; photosynthesis (light-dependent reactions and the Calvin cycle); aerobic and anaerobic respiration; ATP as the energy currency of cells; limiting factors.",
           "Enzymes, Photosynthesis and Cellular Respiration", "enzymes photosynthesis and respiration",
           "Free Year 11 Biology worksheets on enzymes, photosynthesis and respiration: active sites, denaturation, inhibitors, light reactions, the Calvin cycle, glycolysis, ATP and limiting factors. 100 questions with answers.",
           "Photosynthesis stores energy; respiration releases it as ATP.", "Enzymes are proteins: too hot and the active site changes shape.",
           "<p>Enzymes speed up reactions; the substrate fits the active site. Rate rises with temperature up to an optimum, then the enzyme is denatured. pH, substrate concentration and inhibitors also matter.</p>"
           "<p><b>Photosynthesis</b>: light-dependent reactions on the thylakoids make ATP and NADPH; the Calvin cycle in the stroma fixes CO₂ into sugars. <b>Aerobic respiration</b>: glycolysis (cytoplasm), Krebs cycle and electron transport chain (mitochondria) give about 30–38 ATP per glucose; anaerobic respiration gives 2.</p>",
           [("Rate 20 units at 25 °C, 30 units at 35 °C. Percentage increase?", ["(30 − 20) ÷ 20 × 100"], "50%"),
            ("Pigment moves 3.0 cm; solvent 8.0 cm. Rf?", ["3.0 ÷ 8.0"], "0.375")],
           ["Saying enzymes are ‘killed’ by heat: they are denatured (they were never alive).", "Thinking plants do not respire: they respire all the time.", "Placing glycolysis in the mitochondria: it happens in the cytoplasm."],
           [("Why is photosynthesis called the reverse of respiration?", "Photosynthesis uses CO₂ and water to make glucose and oxygen, storing energy; respiration uses glucose and oxygen to make CO₂ and water, releasing energy as ATP."),
            ("What is a limiting factor?", "The factor in shortest supply, which controls the rate: for photosynthesis it may be light, CO₂ or temperature.")],
           u4),
        SR(BIO, 2, 5, "multicellular-organisms", "Multicellular organisms",
           "Cell specialisation and the levels of organisation; exchange surfaces; gas exchange, digestion and circulation in animals; the heart and blood vessels; transport of water and sugars in plants (xylem, phloem and transpiration).",
           "Multicellular Organisms: Exchange and Transport Systems", "multicellular organisms",
           "Free Year 11 Biology worksheets on multicellular organisms: specialised cells, gas exchange, digestion, the heart and circulation, cardiac output, xylem, phloem and transpiration. 100 questions with answers.",
           "Big organisms need exchange surfaces and transport systems.", "Cardiac output = stroke volume × heart rate.",
           "<p>Multicellular organisms have specialised cells organised into tissues, organs and systems. Their small surface area to volume ratio means they need large exchange surfaces (alveoli, villi, root hairs, leaves) and transport systems.</p>"
           "<p>In mammals the heart pumps blood in a double circulation; arteries carry it at high pressure, capillaries exchange materials and veins (with valves) return it. In plants, xylem carries water pulled up by transpiration and phloem carries sugars.</p>",
           [("Stroke volume 70 mL, heart rate 72 beats/min. Cardiac output?", ["70 × 72 = 5040 mL/min"], "5.04 L/min"),
            ("Tidal volume 0.5 L, 15 breaths per minute. Ventilation rate?", ["0.5 × 15"], "7.5 L/min")],
           ["Saying arteries carry oxygenated blood and veins deoxygenated: the pulmonary vessels are the other way round.", "Thinking xylem carries sugar: that is phloem.", "Forgetting that plants exchange gases through stomata, not only by diffusion through the whole leaf."],
           [("How are exchange surfaces adapted?", "A large surface area, a thin barrier (short diffusion distance) and a steep concentration gradient kept by blood flow or ventilation."),
            ("What makes water move up a tall tree?", "Transpiration: water evaporates from the leaves and pulls a continuous column of water up the xylem, because water molecules stick together (cohesion–tension).")],
           u5),
    ]
