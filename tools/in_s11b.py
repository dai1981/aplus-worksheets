# -*- coding: utf-8 -*-
"""Class 11 Biology (NCERT Biology, 19 chapters): question tables, banks and UNITS()."""
from in_sci import _R
from in_srs import ch, A, B, SU, pairs, odd_one, tq, nf, al_bio as BI
from in_s11c import SUBS

BIO = "Biology"
XSUB = [("Mr ", "molar mass "), ("Mr)", "molar mass)"), (" dm³ min⁻¹", " L min⁻¹"), ("cm³", "mL"), ("dm³", "L")]


def T(f, *kinds):
    g0 = A(f, *kinds)

    def g():
        it = g0()
        if not it:
            return None
        sub = lambda t: _s(t)
        it["q"], it["e"], it["c"] = sub(it["q"]), sub(it["e"]), [sub(c) for c in it["c"]]
        return it
    g.__name__ = g0.__name__
    return g


def _s(t):
    for a, b in XSUB + SUBS:
        t = t.replace(a, b)
    return t


FAM = {}


def OD(groups, q="Which of these is %s?", qn="Which of these is NOT %s?"):
    """odd-one-out maker; an item may appear in only one group. FAM[id(groups)] = [[labels], …] keeps wrong answers in the same family when it can."""
    allx = [x for v in groups.values() for x in v]
    assert len(allx) == len(set(allx)), [x for x in allx if allx.count(x) > 1]
    fams = FAM.get(id(groups)) or [list(groups)]

    def f():
        R = _R[0]
        lab = R.choice(sorted(groups))
        fam = [k for fm in fams if lab in fm for k in fm]
        near = sorted({x for k in fam if k != lab for x in groups[k]})
        far = sorted({x for k, v in groups.items() if k not in fam for x in v})
        cap = lambda a: a[0].upper() + a[1:]
        if R.random() < 0.5 and len(groups[lab]) >= 3:
            a = R.choice(near or far)
            return tq(qn % lab, a, R.sample(groups[lab], 3), "“%s” is not %s; the other three are." % (cap(a), lab))
        a = R.choice(groups[lab])
        pool = near if len(near) >= 3 else near + R.sample(far, 3 - len(near))
        return tq(q % lab, a, R.sample(pool, 3), "“%s” is %s." % (cap(a), lab))
    return f


def PR(rows, fwd, back=None, pool=None):
    return pairs(rows, fwd, back, pool)


# =================================================================== 1 the living world
G1 = {"a defining feature of all living things": ["metabolism", "cellular organisation", "consciousness (response to stimuli)", "made of one or more cells"],
      "a taxonomic category (rank)": ["kingdom", "phylum", "class", "order", "family", "genus", "species"],
      "a taxonomic aid": ["herbarium", "botanical garden", "museum", "zoological park", "key", "monograph", "flora", "manual"],
      "a thing that grows only by adding material from outside": ["a salt crystal", "a sand dune", "a mountain", "a snowball rolling downhill"]}
P1 = [("Mangifera indica", "mango"), ("Solanum tuberosum", "potato"), ("Panthera leo", "lion"), ("Homo sapiens", "human"), ("Musca domestica", "housefly"), ("Triticum aestivum", "wheat"),
      ("Panthera tigris", "tiger"), ("Felis catus", "cat"), ("Solanum melongena", "brinjal"), ("Pisum sativum", "pea"), ("Oryza sativa", "rice"), ("Zea mays", "maize"),
      ("Canis familiaris", "dog"), ("Columba livia", "pigeon"), ("Gossypium hirsutum", "cotton")]
P1b = [("herbarium", "a store of pressed, dried and labelled plant specimens on sheets"), ("botanical garden", "a garden of living plants grown and labelled for study"),
       ("museum", "a collection of preserved plant and animal specimens"), ("zoological park", "a place where wild animals are kept in protected surroundings like their natural habitat"),
       ("key", "a tool that identifies organisms using pairs of contrasting characters"), ("flora", "an account of the plant species found in an area"),
       ("monograph", "information about any one taxon"), ("manual", "a book that helps identify the species in an area")]
B1 = [("Who proposed the system of binomial nomenclature?", "Carolus Linnaeus", ["Charles Darwin", "R. H. Whittaker", "Ernst Mayr"], "Each organism gets a genus name and a species epithet."),
      ("How should a scientific name be written when printed?", "in italics, genus with a capital letter and species epithet in small letters", ["all in capitals", "underlined in capitals", "with both words capitalised in plain type"], "e.g. <i>Mangifera indica</i>."),
      ("Which is the basic unit of classification?", "species", ["genus", "family", "kingdom"], "Members can interbreed to produce fertile offspring."),
      ("In <i>Mangifera indica</i>, what does 'indica' stand for?", "the specific epithet", ["the genus", "the family", "the order"], "Mangifera is the genus."),
      ("Which is the correct order from the highest to the lowest category?", "kingdom, phylum, class, order, family, genus, species", ["species, genus, family, order, class, phylum, kingdom", "kingdom, class, phylum, order, family, genus, species", "kingdom, phylum, order, class, family, genus, species"], "Remember: King Philip Came Over For Good Soup."),
      ("Which is a property of living things but NOT of non-living things?", "metabolism", ["growth by accumulation", "having mass", "moving when pushed"], "Mountains and crystals can grow from outside."),
      ("Why is growth not a defining property of living things?", "non-living things such as mountains and crystals can also grow by accumulation", ["living things never grow", "only plants grow", "growth stops in all organisms"], "Growth in living things is from inside."),
      ("Why is reproduction not a defining property of living things?", "some living organisms, such as mules and worker bees, cannot reproduce", ["all non-living things reproduce", "only animals reproduce", "reproduction is metabolism"], "Metabolism and cellular organisation are defining."),
      ("What does ICBN stand for?", "International Code for Botanical Nomenclature", ["Indian Council of Biology and Nature", "International Centre for Biological Names", "International Code for Biological Naming"], "Plants are named by ICBN; animals by ICZN."),
      ("What does ICZN stand for?", "International Code of Zoological Nomenclature", ["International Council of Zoos and Nature", "Indian Code of Zoological Names", "International Centre for Zoology Names"], "It sets the rules for naming animals."),
      ("Which category includes related genera?", "family", ["order", "class", "species"], "e.g. Felidae includes Panthera and Felis."),
      ("Which category includes related orders?", "class", ["family", "phylum", "genus"], "e.g. Mammalia includes Primata and Carnivora."),
      ("Which famous herbarium is in Howrah (Kolkata)?", "the Indian Botanical Garden herbarium", ["the National Zoological Park", "the Lalbagh Botanical Garden, Bengaluru", "the Lloyd Botanical Garden, Darjeeling"], "It is one of the largest herbaria in India."),
      ("What is a taxon?", "a group of organisms at any level of the hierarchy", ["a single organism", "only a species", "a key"], "e.g. the genus <i>Panthera</i> is a taxon."),
      ("Which is a living thing that cannot reproduce?", "a mule", ["a dog", "a mango tree", "a bacterium"], "A mule is sterile.")]


# =================================================================== 2 biological classification
G2 = {"in kingdom Monera": ["bacteria", "cyanobacteria", "mycoplasma", "archaebacteria", "Nostoc", "Anabaena", "Lactobacillus"],
      "in kingdom Protista": ["Amoeba", "Paramoecium", "diatoms", "Euglena", "Plasmodium", "dinoflagellates", "Trypanosoma", "slime moulds"],
      "in kingdom Fungi": ["yeast", "Penicillium", "mushroom (Agaricus)", "Rhizopus", "Albugo", "bread mould", "Aspergillus", "Puccinia (wheat rust)", "Ustilago (smut)"],
      "a disease caused by a virus": ["AIDS", "mumps", "smallpox", "herpes", "influenza", "tobacco mosaic disease"],
      "a disease caused by a protozoan": ["malaria", "sleeping sickness", "amoebic dysentery"],
      "a disease caused by bacteria": ["cholera", "typhoid", "tetanus", "citrus canker"]}
P2 = [("Monera", "prokaryotic, mostly unicellular, with a cell wall of peptidoglycan"), ("Protista", "unicellular eukaryotes"), ("Fungi", "heterotrophic eukaryotes with a cell wall of chitin"),
      ("Plantae", "multicellular eukaryotes with a cellulose cell wall that make their own food"), ("Animalia", "multicellular eukaryotes with no cell wall that ingest food")]
P2b = [("Phycomycetes", "Rhizopus and Albugo"), ("Ascomycetes", "Penicillium, Aspergillus and yeast"), ("Basidiomycetes", "mushrooms, bracket fungi and smuts"), ("Deuteromycetes", "Alternaria and Trichoderma")]
B2 = [("Who proposed the five-kingdom classification?", "R. H. Whittaker", ["Carolus Linnaeus", "Aristotle", "D. J. Ivanowsky"], "Monera, Protista, Fungi, Plantae and Animalia (1969)."),
      ("Which organisms live in extreme habitats such as hot springs and salt marshes?", "archaebacteria", ["cyanobacteria", "fungi", "slime moulds"], "Their cell wall structure differs from other bacteria."),
      ("Which bacteria produce methane (biogas) in the guts of cows?", "methanogens", ["halophiles", "thermoacidophiles", "cyanobacteria"], "They are archaebacteria."),
      ("What are heterocysts in cyanobacteria used for?", "fixing atmospheric nitrogen", ["photosynthesis", "reproduction", "movement"], "e.g. Nostoc and Anabaena."),
      ("Which are the smallest living cells and have no cell wall?", "mycoplasma", ["viruses", "yeast", "diatoms"], "They can survive without oxygen."),
      ("What is the cell wall of diatoms made of?", "silica, forming two overlapping halves", ["chitin", "cellulose only", "peptidoglycan"], "Their deposits form diatomaceous earth."),
      ("Which protists cause red tides?", "dinoflagellates such as Gonyaulax", ["diatoms", "Euglena", "slime moulds"], "They can release toxins that kill fish."),
      ("Who discovered viruses?", "D. J. Ivanowsky", ["M. W. Beijerinck", "W. M. Stanley", "T. O. Diener"], "From tobacco mosaic disease."),
      ("What are viroids?", "free RNA without a protein coat that cause disease", ["proteins that cause disease", "bacteria without walls", "very small fungi"], "Found by T. O. Diener; cause potato spindle tuber disease."),
      ("What are prions?", "abnormally folded proteins that cause disease", ["free RNA", "small bacteria", "virus coats"], "e.g. mad cow disease (BSE)."),
      ("What is a lichen?", "a symbiotic association of an alga and a fungus", ["a kind of moss", "a bacterium", "a virus"], "They are pollution indicators."),
      ("What is the genetic material of bacteriophages usually?", "double-stranded DNA", ["single-stranded RNA", "protein", "lipid"], "Plant viruses usually have single-stranded RNA."),
      ("Why are fungi called saprophytes?", "they absorb food from dead and decaying matter", ["they make their own food", "they eat other animals", "they only live in water"], "They are important decomposers."),
      ("Which kingdom has members that are euglenoids, with a pellicle and a flagellum?", "Protista", ["Monera", "Fungi", "Plantae"], "Euglena photosynthesises in light."),
      ("What is the main drawback of the two-kingdom classification?", "it puts prokaryotes and eukaryotes, unicellular and multicellular, together", ["it has too many kingdoms", "it ignores plants", "it uses Latin"], "Bacteria, fungi and plants were all in Plantae.")]


# =================================================================== 3 plant kingdom
G3 = {"an alga": ["Spirogyra", "Chlamydomonas", "Volvox", "Ulothrix", "Laminaria", "Fucus", "Polysiphonia", "Gracilaria"],
      "a bryophyte": ["Funaria", "Marchantia", "Riccia", "Sphagnum", "Polytrichum"],
      "a pteridophyte": ["Selaginella", "Equisetum", "Pteris", "Dryopteris", "Adiantum", "Lycopodium"],
      "a gymnosperm": ["Pinus", "Cycas", "Cedrus", "Ginkgo", "Sequoia"]}
P3 = [("Chlorophyceae", "green algae, with chlorophyll a and b, storing starch"), ("Phaeophyceae", "brown algae, with fucoxanthin, storing laminarin and mannitol"),
      ("Rhodophyceae", "red algae, with r-phycoerythrin, storing floridean starch")]
P3b = [("bryophytes", "the amphibians of the plant kingdom"), ("pteridophytes", "the first land plants with vascular tissue (xylem and phloem)"),
       ("gymnosperms", "plants with naked seeds, not enclosed in an ovary"), ("angiosperms", "flowering plants with seeds enclosed in fruits")]
B3 = [("Which is the dominant phase of the life cycle in bryophytes?", "the gametophyte", ["the sporophyte", "both equally", "neither"], "The sporophyte grows on the gametophyte."),
      ("Which is the dominant phase in pteridophytes?", "the sporophyte", ["the gametophyte", "the protonema", "the prothallus"], "The gametophyte is a small prothallus."),
      ("Which agar-producing alga is used in growing microbes?", "Gelidium or Gracilaria (red algae)", ["Spirogyra", "Chlorella", "Fucus"], "Agar is used in culture media and ice creams."),
      ("Which alga is a rich protein food supplement, even for space travellers?", "Chlorella", ["Spirogyra", "Fucus", "Gelidium"], "It is unicellular and fast-growing."),
      ("Which moss forms peat used as fuel and as packing material?", "Sphagnum", ["Funaria", "Marchantia", "Riccia"], "It holds a lot of water."),
      ("What is heterospory?", "producing two kinds of spores, large megaspores and small microspores", ["producing one kind of spore", "having no spores", "making seeds without spores"], "e.g. Selaginella and Salvinia; a step towards seeds."),
      ("What is the ploidy of the endosperm in angiosperms?", "triploid (3n)", ["haploid (n)", "diploid (2n)", "tetraploid (4n)"], "It forms from the fusion of a male gamete with two polar nuclei."),
      ("What is the endosperm of gymnosperms?", "haploid female gametophyte tissue", ["triploid tissue", "diploid sporophyte tissue", "seed coat"], "There is no double fertilisation."),
      ("What is double fertilisation?", "one male gamete fuses with the egg and another with the polar nuclei", ["two eggs are fertilised", "fertilisation happens twice a year", "self- and cross-fertilisation together"], "It is unique to angiosperms."),
      ("Which gymnosperm has coralloid roots with nitrogen-fixing cyanobacteria?", "Cycas", ["Pinus", "Ginkgo", "Cedrus"], "Pinus has mycorrhiza instead."),
      ("What is the tallest tree species?", "Sequoia (redwood), a gymnosperm", ["Eucalyptus, an angiosperm", "Pinus", "Cycas"], "Some are over 100 m tall."),
      ("What is a haplontic life cycle?", "the sporophyte is only the one-celled zygote; the gametophyte is dominant", ["the sporophyte is dominant", "both phases are equal", "there are no gametes"], "Seen in Volvox, Spirogyra and some Chlamydomonas."),
      ("Which algae have the pigment fucoxanthin?", "brown algae (Phaeophyceae)", ["green algae", "red algae", "blue-green algae"], "It gives the olive-green to brown colour."),
      ("In which group do vascular tissues first appear?", "pteridophytes", ["bryophytes", "algae", "fungi"], "They have true roots, stems and leaves."),
      ("What is the protonema?", "the first, alga-like stage of a moss gametophyte", ["the sporophyte of a fern", "a seed coat", "a kind of root"], "It grows from a spore.")]


# =================================================================== 4 animal kingdom
G4 = {"in phylum Porifera": ["Sycon", "Spongilla", "Euspongia"], "in phylum Cnidaria": ["Hydra", "Aurelia (jellyfish)", "Physalia (Portuguese man-of-war)", "Adamsia (sea anemone)", "Gorgonia (sea fan)"],
      "in phylum Platyhelminthes": ["Taenia (tapeworm)", "Fasciola (liver fluke)", "Planaria"], "in phylum Aschelminthes": ["Ascaris (roundworm)", "Wuchereria (filaria worm)", "Ancylostoma (hookworm)"],
      "in phylum Annelida": ["Nereis", "Pheretima (earthworm)", "Hirudinaria (leech)"], "in phylum Arthropoda": ["Apis (honey bee)", "Anopheles (mosquito)", "Limulus (king crab)", "Bombyx (silkworm)", "Laccifer (lac insect)", "Locusta (locust)"],
      "in phylum Mollusca": ["Pila (apple snail)", "Pinctada (pearl oyster)", "Sepia (cuttlefish)", "Loligo (squid)", "Octopus"], "in phylum Echinodermata": ["Asterias (starfish)", "Echinus (sea urchin)", "Antedon (sea lily)", "Ophiura (brittle star)"]}
G4b = {"a mammal": ["platypus", "kangaroo", "bat", "whale", "dolphin", "elephant"], "a bird": ["crow", "pigeon", "parrot", "ostrich", "peacock", "penguin"],
       "a reptile": ["chameleon", "crocodile", "turtle", "cobra", "Hemidactylus (wall lizard)"], "an amphibian": ["frog", "toad", "salamander", "Ichthyophis (limbless amphibian)"],
       "a bony fish (Osteichthyes)": ["rohu (Labeo)", "catla", "seahorse (Hippocampus)", "flying fish (Exocoetus)"], "a cartilaginous fish (Chondrichthyes)": ["shark (Scoliodon)", "sting ray (Trygon)", "electric ray (Torpedo)", "saw fish (Pristis)"]}
P4 = [("Porifera", "the cellular level of organisation"), ("Cnidaria", "the tissue level of organisation and cnidoblasts (stinging cells)"), ("Platyhelminthes", "flat bodies and flame cells"),
      ("Annelida", "metameric segmentation and nephridia"), ("Arthropoda", "jointed appendages and a chitinous exoskeleton"), ("Mollusca", "a soft body covered by a calcareous shell and a mantle"),
      ("Echinodermata", "a water vascular system and spiny skin"), ("Hemichordata", "a stomochord and proboscis gland, as in Balanoglossus"), ("Ctenophora", "comb plates and bioluminescence")]
B4 = [("Which is the largest phylum of the animal kingdom?", "Arthropoda", ["Mollusca", "Chordata", "Annelida"], "About two-thirds of all named species are arthropods."),
      ("Which animals are diploblastic?", "cnidarians and ctenophores", ["flatworms", "earthworms", "insects"], "They have only ectoderm and endoderm."),
      ("What is a pseudocoelomate?", "an animal whose body cavity is not lined by mesoderm all round", ["an animal with no body cavity", "an animal with a true coelom", "a chordate"], "e.g. roundworms (Aschelminthes)."),
      ("Which animals show radial symmetry as adults?", "cnidarians and echinoderms", ["insects", "mammals", "flatworms"], "Echinoderm larvae are bilaterally symmetrical."),
      ("What are the three basic chordate features?", "a notochord, a dorsal hollow nerve cord and pharyngeal gill slits", ["a backbone, lungs and fins", "a shell, mantle and foot", "jointed legs, antennae and wings"], "All appear at some stage of life."),
      ("Which chordates have a notochord only in the larval tail?", "urochordates (tunicates)", ["cephalochordates", "vertebrates", "hemichordates"], "e.g. Ascidia and Salpa."),
      ("Which class of vertebrates is cold-blooded and has a three-chambered heart, with moist skin?", "Amphibia", ["Reptilia", "Aves", "Mammalia"], "Most reptiles also have three chambers, but dry scaly skin."),
      ("Which mammal lays eggs?", "the platypus (Ornithorhynchus)", ["the kangaroo", "the bat", "the whale"], "It is a monotreme."),
      ("What are cnidoblasts used for?", "anchoring, defence and catching prey", ["breathing", "excretion", "reproduction"], "They contain stinging capsules."),
      ("Which animals have flame cells for excretion?", "flatworms (Platyhelminthes)", ["earthworms", "insects", "mammals"], "Flame cells also help in osmoregulation."),
      ("What is metagenesis?", "alternation between polyp and medusa forms", ["moulting", "metamorphosis of a tadpole", "segmentation"], "e.g. Obelia."),
      ("Which phylum has a water vascular system for movement and feeding?", "Echinodermata", ["Mollusca", "Cnidaria", "Annelida"], "It moves by many small water-filled tubes (podia)."),
      ("Which birds have pneumatic bones?", "all birds", ["only flightless birds", "no birds", "only penguins"], "Hollow bones make them light."),
      ("What kind of heart do crocodiles have?", "a four-chambered heart", ["a two-chambered heart", "a three-chambered heart", "no heart"], "Crocodiles are the exception among reptiles."),
      ("What is the excretory organ of insects?", "Malpighian tubules", ["nephridia", "flame cells", "kidneys"], "They remove waste into the gut.")]


# =================================================================== 5 morphology of flowering plants
G5 = {"a modified root": ["carrot (storage)", "turnip (storage)", "sweet potato (storage)", "prop roots of banyan", "stilt roots of maize", "pneumatophores of Rhizophora"],
      "a modified stem": ["potato tuber", "ginger rhizome", "onion bulb", "Opuntia (cladode)", "tendrils of cucumber", "thorns of Bougainvillea", "runner of grass"],
      "a modified leaf": ["tendrils of pea", "spines of cactus", "pitcher of pitcher plant", "fleshy leaves of onion", "phyllode of Australian Acacia"],
      "a dicot plant": ["mango", "mustard", "sunflower", "China rose", "gram", "neem", "brinjal"], "a monocot plant": ["wheat", "maize", "lily", "banana", "coconut palm", "rice", "sugarcane"],
      "in family Fabaceae": ["soyabean", "groundnut", "lucerne", "sweet pea"], "in family Solanaceae": ["tomato", "potato plant", "chilli", "petunia"], "in family Liliaceae": ["tulip", "Aloe", "Asparagus", "onion plant"]}
P5 = [("Fabaceae", "pea, gram and soyabean: papilionaceous flowers, vexillary aestivation, legume fruit"), ("Solanaceae", "potato, tomato and brinjal: swollen placenta, berry or capsule"),
      ("Liliaceae", "onion, lily and Aloe: monocots with perianth (tepals)")]
P5b = [("valvate aestivation", "sepals or petals just touch at the edges, as in Calotropis"), ("twisted aestivation", "each petal overlaps the next on one side, as in China rose"),
       ("imbricate aestivation", "the margins overlap irregularly, as in Cassia and gulmohur"), ("vexillary aestivation", "a large standard petal overlaps two wings, which overlap two keel petals, as in pea"),
       ("marginal placentation", "ovules on a ridge along one side of a one-chambered ovary, as in pea"), ("axile placentation", "ovules on a central axis in a many-chambered ovary, as in China rose, tomato and lemon"),
       ("parietal placentation", "ovules on the inner wall of the ovary, as in mustard and Argemone"), ("basal placentation", "a single ovule at the base of the ovary, as in sunflower and marigold"),
       ("free central placentation", "ovules on a central axis with no septa, as in Dianthus and Primrose")]
B5 = [("Which root system do dicots usually have?", "a tap root system", ["a fibrous root system", "adventitious roots only", "no roots"], "The primary root goes on growing."),
      ("Which plant has a fibrous root system?", "wheat", ["mustard", "pea", "mango"], "Monocots like wheat have fibrous roots."),
      ("Which venation do monocot leaves usually have?", "parallel venation", ["reticulate venation", "no venation", "pinnate venation only"], "Dicot leaves usually have reticulate venation."),
      ("What is a hypogynous flower?", "one in which the ovary is superior", ["one in which the ovary is inferior", "one with no ovary", "one with half-inferior ovary"], "e.g. mustard, China rose and brinjal."),
      ("What is an epigynous flower?", "one in which the ovary is inferior", ["one in which the ovary is superior", "one with no petals", "a male flower"], "e.g. guava, cucumber and sunflower ray florets."),
      ("What are stamens attached to petals called?", "epipetalous", ["epiphyllous", "polyadelphous", "monoadelphous"], "e.g. brinjal."),
      ("What does the term 'monoadelphous' mean?", "stamens united into one bundle by their filaments", ["one stamen only", "stamens fused to petals", "stamens in two bundles"], "e.g. China rose."),
      ("Which is a parthenocarpic fruit?", "banana", ["mango", "pea", "wheat"], "It develops without fertilisation."),
      ("What type of fruit is mango?", "a drupe", ["a berry", "a legume", "a capsule"], "It has a hard stony endocarp."),
      ("What is the edible part of a coconut?", "the endosperm", ["the pericarp", "the cotyledon", "the seed coat"], "Coconut water is liquid endosperm."),
      ("What is the outer covering of the seed of maize that is fused with the fruit wall?", "the seed coat fused with pericarp (a caryopsis grain)", ["the aleurone layer only", "the scutellum", "the coleoptile"], "Maize grain is a fruit."),
      ("What is the cotyledon of a grass seed called?", "the scutellum", ["the coleorhiza", "the plumule", "the hilum"], "It is a single large shield-shaped cotyledon."),
      ("What is phyllotaxy?", "the pattern in which leaves are arranged on a stem", ["the shape of a leaf", "the veins of a leaf", "the falling of leaves"], "Alternate, opposite or whorled."),
      ("Which phyllotaxy does Alstonia have?", "whorled", ["alternate", "opposite", "spiral"], "More than two leaves at each node."),
      ("What is a racemose inflorescence?", "one in which the main axis keeps growing and flowers form laterally", ["one ending in a flower", "a single flower", "one with no flowers"], "Flowers open from the base upward.")]


# =================================================================== 6 anatomy of flowering plants
G6 = {"a primary meristem": ["shoot apical meristem", "root apical meristem", "intercalary meristem"], "a simple permanent tissue": ["parenchyma", "collenchyma", "sclerenchyma"],
      "a conducting element of xylem": ["tracheids", "vessels"], "a part of the epidermal tissue system": ["root hairs", "trichomes", "stomata", "cuticle"],
      "a part of the ground tissue system": ["cortex", "pericycle", "pith", "medullary rays"], "a part of the vascular tissue system": ["xylem", "phloem", "vascular cambium (in dicots)"], "a part of phloem found in angiosperms": ["sieve tube elements", "companion cells"], "a lateral meristem": ["fascicular vascular cambium", "interfascicular cambium", "phellogen"]}
P6 = [("dicot root", "radial vascular bundles, 2–4 xylem bundles and a small pith"), ("monocot root", "radial vascular bundles, more than six xylem bundles and a large pith"),
      ("dicot stem", "vascular bundles in a ring, conjoint, open, with cambium"), ("monocot stem", "scattered vascular bundles, conjoint and closed, with a bundle sheath")]
P6b = [("sclerenchyma", "dead cells with thick lignified walls that give mechanical support"), ("collenchyma", "living cells thickened at the corners with cellulose and pectin"),
       ("parenchyma", "thin-walled living cells used for storage and photosynthesis"), ("xylem", "conducting water and minerals from roots"), ("phloem", "transporting food from leaves"),
       ("companion cells", "specialised parenchyma cells linked to sieve tubes"), ("lenticels", "openings in the bark for gas exchange"), ("bulliform cells", "large empty cells in grass leaves that make them roll up in dry weather"),
       ("guard cells", "cells that open and close the stomatal pore"), ("cuticle", "a waxy layer on the epidermis that cuts water loss"), ("phellem", "cork, the dead outer layer of bark"),
       ("phellogen", "the cork cambium that makes cork and secondary cortex"), ("hypodermis", "the layers just below the epidermis, of collenchyma in dicot stems"),
       ("endodermis", "the innermost layer of the cortex, with Casparian strips in roots"), ("pericycle", "the layer just inside the endodermis that gives rise to lateral roots"),
       ("medullary rays", "parenchyma cells between the vascular bundles of a dicot stem"), ("spongy parenchyma", "loosely arranged cells with air spaces in the lower part of a dicot leaf"),
       ("palisade parenchyma", "tall, closely packed cells with many chloroplasts below the upper epidermis")]
B6 = [("What does the vascular cambium produce?", "secondary xylem on the inside and secondary phloem on the outside", ["only cork", "only primary tissues", "root hairs"], "This causes growth in girth."),
      ("What is the periderm made of?", "phellem (cork), phellogen (cork cambium) and phelloderm", ["xylem and phloem", "epidermis and cortex", "pith and medullary rays"], "It replaces the epidermis in older stems."),
      ("What are annual rings?", "rings of spring wood and autumn wood formed each year", ["the rings of the bark only", "pith cells", "the vascular bundles of monocots"], "They are used to estimate a tree's age."),
      ("What is heartwood?", "the dark central wood made of dead xylem filled with tannins and resins", ["the living outer wood", "the bark", "the cambium"], "It is durable and no longer conducts water."),
      ("What is sapwood?", "the light-coloured outer wood that still conducts water", ["the dead central wood", "the bark", "the pith"], "Also called alburnum."),
      ("What is endarch xylem?", "protoxylem towards the centre and metaxylem towards the outside", ["protoxylem towards the outside", "no protoxylem", "phloem inside xylem"], "Found in stems; roots are exarch."),
      ("Which layer in the root has Casparian strips?", "the endodermis", ["the epidermis", "the pericycle", "the pith"], "Suberin blocks water from moving through the walls."),
      ("From which tissue do lateral roots arise?", "the pericycle", ["the endodermis", "the epidermis", "the cortex"], "It also helps form vascular cambium in roots."),
      ("What is a dorsiventral leaf?", "a leaf with palisade on the upper side and spongy tissue below, as in dicots", ["a leaf with the same tissue on both sides", "a monocot leaf", "a leaf with no veins"], "Isobilateral leaves (grasses) differ."),
      ("Which cells guard the stomata of grasses?", "dumb-bell shaped guard cells", ["bean-shaped guard cells", "root hairs", "bulliform cells"], "Dicots have bean-shaped guard cells."),
      ("Which plants have no secondary growth usually?", "monocots", ["dicots", "gymnosperms", "trees"], "They lack a vascular cambium."),
      ("What is the function of the pericycle in roots?", "it gives rise to lateral roots", ["it stores water", "it makes chlorophyll", "it absorbs light"], "It lies just inside the endodermis."),
      ("Which elements of xylem are found mainly in angiosperms?", "vessels", ["tracheids", "sieve tubes", "companion cells"], "Gymnosperms lack vessels."),
      ("Which part of phloem is absent in gymnosperms?", "companion cells (and sieve tubes)", ["phloem parenchyma", "albuminous cells", "phloem fibres in all"], "They have albuminous cells and sieve cells."),
      ("What is the outermost layer of the primary plant body?", "the epidermis", ["the cortex", "the pericycle", "the endodermis"], "It is covered by cuticle in shoots.")]


# =================================================================== 7 structural organisation in animals (frog)
G7 = {"an epithelial tissue": ["squamous epithelium", "cuboidal epithelium", "columnar epithelium", "ciliated epithelium", "compound epithelium"],
      "a connective tissue": ["bone", "cartilage", "blood", "areolar tissue", "adipose tissue", "tendon", "ligament"],
      "a muscle tissue": ["skeletal muscle", "smooth muscle", "cardiac muscle"], "a cell junction": ["tight junction", "adhering junction", "gap junction"],
      "a feature of the frog": ["a three-chambered heart", "external fertilisation", "a tadpole larva", "breathing through the skin in water", "a nictitating membrane over the eye"]}
P7 = [("squamous epithelium", "the walls of blood vessels and air sacs of lungs"), ("cuboidal epithelium", "the ducts of glands and the tubular parts of nephrons"),
      ("ciliated epithelium", "the bronchioles and fallopian tubes"), ("compound epithelium", "the dry surface of the skin, the moist lining of the mouth and pharynx"),
      ("tendon", "connecting a skeletal muscle to a bone"), ("ligament", "connecting a bone to another bone"), ("adipose tissue", "storing fat below the skin"),
      ("cardiac muscle", "the wall of the heart"), ("smooth muscle", "the wall of the stomach and intestine"), ("neural tissue", "carrying messages as nerve impulses"),
      ("columnar epithelium", "the lining of the stomach and intestine, with tall cells"), ("areolar tissue", "just beneath the skin, as a support framework"),
      ("cartilage", "the tip of the nose, the outer ear and between the vertebrae"), ("blood", "transporting substances round the body in a fluid matrix")]
B7 = [("What is the scientific name of the common Indian frog?", "Rana tigrina", ["Bufo melanostictus", "Hyla arborea", "Ichthyophis glutinosa"], "It is used in NCERT as the example."),
      ("How does a frog breathe in water?", "through its moist skin (cutaneous respiration)", ["through gills", "through lungs only", "it does not breathe in water"], "On land it also uses its lungs and buccal cavity."),
      ("Why is the frog called cold-blooded?", "its body temperature changes with the environment (poikilothermic)", ["it lives in cold water", "its blood is cold", "it hibernates"], "It goes into winter sleep (hibernation)."),
      ("How many chambers does a frog's heart have?", "three: two atria and one ventricle", ["two", "four", "one"], "There is also a sinus venosus and conus arteriosus."),
      ("What is the main nitrogenous waste of a frog?", "urea (it is ureotelic)", ["ammonia", "uric acid", "creatinine only"], "Tadpoles excrete ammonia."),
      ("Which junctions stop substances from leaking across a tissue?", "tight junctions", ["gap junctions", "adhering junctions", "desmosomes only"], "Gap junctions let ions and small molecules pass between cells."),
      ("What do gap junctions do?", "they connect the cytoplasm of neighbouring cells for rapid transfer of ions and small molecules", ["they stop leakage", "they hold cells together", "they make mucus"], "Found in cardiac muscle."),
      ("Which cells of the neural tissue support and protect neurons?", "neuroglia", ["osteocytes", "chondrocytes", "erythrocytes"], "They make up more than half the volume of neural tissue."),
      ("Which connective tissue has a fluid matrix?", "blood", ["bone", "cartilage", "tendon"], "Plasma is its matrix."),
      ("What is the hard matrix of bone made of?", "calcium salts and collagen fibres", ["chitin", "cellulose", "keratin only"], "Osteocytes lie in spaces called lacunae."),
      ("Which glands release secretions through ducts?", "exocrine glands", ["endocrine glands", "all glands", "no glands"], "e.g. salivary glands and mucus glands."),
      ("How does fertilisation take place in frogs?", "externally, in water", ["internally", "in the egg after laying on land", "by budding"], "Development includes a tadpole stage (metamorphosis)."),
      ("Which muscle is voluntary and striated?", "skeletal muscle", ["smooth muscle", "cardiac muscle", "none"], "It is attached to bones."),
      ("Which muscle is involuntary and striated?", "cardiac muscle", ["skeletal muscle", "smooth muscle", "none"], "It has intercalated discs."),
      ("What does a male frog have that a female does not?", "vocal sacs and a copulatory pad on the first digit of the forelimb", ["a cloaca", "kidneys", "lungs"], "These help the male call and hold the female.")]


# =================================================================== 8 cell: the unit of life
G8 = {"a membrane-bound organelle": ["mitochondrion", "chloroplast", "Golgi apparatus", "endoplasmic reticulum", "lysosome", "peroxisome (a microbody)"],
      "a structure with no membrane around it": ["ribosome", "centriole", "nucleolus", "microtubule"],
      "found only in prokaryotic cells": ["mesosome", "nucleoid", "pili", "fimbriae"]}
P8 = [("mitochondria", "the site of aerobic respiration (the powerhouse of the cell)"), ("ribosomes", "the site of protein synthesis"), ("Golgi apparatus", "packaging and secretion of materials, and forming glycoproteins and glycolipids"),
      ("lysosomes", "digesting materials with hydrolytic enzymes"), ("smooth endoplasmic reticulum", "making lipids and steroid hormones"), ("rough endoplasmic reticulum", "making and secreting proteins"),
      ("chloroplasts", "photosynthesis"), ("centrioles", "forming the spindle during animal cell division and the bases of cilia"), ("nucleolus", "making ribosomal RNA"),
      ("vacuole", "storing water, sap and waste, and keeping the cell turgid"), ("chromoplasts", "giving colour to fruits and flowers"), ("leucoplasts", "storing starch, oils and proteins")]
B8 = [("Who first saw and described a living cell?", "Anton von Leeuwenhoek", ["Robert Hooke", "Robert Brown", "Rudolf Virchow"], "Hooke saw dead cork cells."),
      ("Who discovered the nucleus?", "Robert Brown", ["Robert Hooke", "Matthias Schleiden", "Theodor Schwann"], "In 1831."),
      ("Who explained that all cells arise from pre-existing cells (omnis cellula-e cellula)?", "Rudolf Virchow", ["Schleiden", "Schwann", "Hooke"], "This completed the cell theory."),
      ("What is the fluid mosaic model of the plasma membrane?", "a lipid bilayer in which proteins float, with the lipid able to move sideways", ["a rigid protein layer", "a sheet of cellulose", "a layer of DNA"], "Proposed by Singer and Nicolson (1972)."),
      ("Which ribosomes are found in prokaryotes?", "70S", ["80S", "60S", "90S"], "Eukaryotes have 80S in the cytoplasm."),
      ("What does the 'S' in 70S ribosome stand for?", "the Svedberg unit, a measure of sedimentation", ["the size in micrometres", "sugar", "subunit number"], "It depends on size and shape."),
      ("Which organelles contain their own DNA and ribosomes?", "mitochondria and chloroplasts", ["Golgi bodies and lysosomes", "ribosomes and centrioles", "vacuoles and lysosomes"], "They are semi-autonomous."),
      ("What is the folded inner membrane of mitochondria called?", "cristae", ["thylakoids", "grana", "cisternae"], "They increase the surface area."),
      ("What are the stacks of thylakoids in a chloroplast called?", "grana", ["cristae", "stroma", "cisternae"], "The fluid around them is the stroma."),
      ("What is the cell wall of plants mainly made of?", "cellulose", ["chitin", "peptidoglycan", "protein"], "Fungal walls are mainly chitin."),
      ("What is a metacentric chromosome?", "one with the centromere in the middle and two equal arms", ["one with the centromere at the end", "one with no centromere", "one with very unequal arms"], "Telocentric chromosomes have a terminal centromere."),
      ("What is the shape of the cilia and flagella axoneme in cross-section?", "9 + 2 arrangement of microtubules", ["9 + 0", "9 + 3", "a single tube"], "Nine outer doublets and two central singlets."),
      ("Which bacterial structure helps attach to surfaces and other cells?", "pili and fimbriae", ["flagellum only", "mesosome", "nucleoid"], "Flagella are for movement."),
      ("Which part of the cell is the largest cell in the human body?", "the ovum", ["the nerve cell", "the red blood cell", "the white blood cell"], "The longest cell is the nerve cell."),
      ("Which organelles are called suicidal bags?", "lysosomes", ["ribosomes", "vacuoles", "peroxisomes"], "Their enzymes can digest the cell itself."),
      ("What is the space between the two layers of the nuclear envelope called?", "the perinuclear space", ["the nucleolus", "the stroma", "the matrix"], "The envelope has nuclear pores.")]


# =================================================================== 9 biomolecules
G9 = {"a polysaccharide": ["starch", "cellulose", "glycogen", "chitin", "inulin"], "a monosaccharide": ["glucose", "fructose", "galactose", "ribose"],
      "an amino acid": ["glycine", "alanine", "serine", "tryptophan", "lysine", "glutamic acid"], "a nitrogen base in nucleic acids": ["adenine", "guanine", "cytosine", "thymine", "uracil"],
      "a lipid": ["lecithin (a phospholipid)", "palmitic acid", "glycerol trioleate (an oil)", "cholesterol"]}
P9 = [("oxidoreductases", "catalysing oxidation and reduction between two substrates"), ("transferases", "transferring a group from one substrate to another"), ("hydrolases", "breaking bonds by adding water"),
      ("lyases", "removing groups without hydrolysis, leaving double bonds"), ("isomerases", "converting one isomer into another"), ("ligases", "joining two compounds together, such as C–O or C–N bonds")]
P9b = [("haem in haemoglobin", "a prosthetic group"), ("NAD and NADP", "coenzymes"), ("zinc in carboxypeptidase", "a metal ion cofactor"), ("malonate inhibiting succinic dehydrogenase", "competitive inhibition")]
B9 = [("Which bond joins amino acids in a protein?", "the peptide bond", ["the glycosidic bond", "the phosphodiester bond", "the ester bond"], "It forms between –COOH and –NH₂ with loss of water."),
      ("Which bond joins monosaccharides in a polysaccharide?", "the glycosidic bond", ["the peptide bond", "the hydrogen bond only", "the ionic bond"], "It forms by dehydration."),
      ("Which bond joins nucleotides in a nucleic acid?", "the phosphodiester bond", ["the peptide bond", "the glycosidic bond", "the disulphide bond"], "It links the sugar of one nucleotide to the phosphate of the next."),
      ("What is the most abundant protein in animals?", "collagen", ["RuBisCO", "haemoglobin", "insulin"], "RuBisCO is the most abundant protein in the biosphere."),
      ("What is the most abundant protein in the whole biosphere?", "RuBisCO", ["collagen", "keratin", "myosin"], "It fixes CO₂ in photosynthesis."),
      ("What is the primary structure of a protein?", "the sequence of amino acids", ["the helix shape", "the folding of the chain", "the joining of several chains"], "It is read from the N-terminal end."),
      ("Which level of protein structure does haemoglobin show with its four subunits?", "quaternary structure", ["primary structure only", "secondary structure only", "no structure"], "Two α and two β chains."),
      ("Why do enzymes speed up reactions?", "they lower the activation energy", ["they raise the temperature", "they change ΔG", "they are used up"], "They form an enzyme–substrate complex."),
      ("What happens to most enzymes at very high temperature?", "they are denatured and stop working", ["they work faster forever", "they become fats", "they divide"], "Their active site changes shape."),
      ("What is a nucleoside?", "a nitrogen base joined to a sugar", ["a base, sugar and phosphate", "a phosphate and sugar only", "an amino acid"], "Add a phosphate to get a nucleotide."),
      ("Which polysaccharide is a branched storage form in animals?", "glycogen", ["cellulose", "starch", "chitin"], "It is stored in liver and muscle."),
      ("Which polysaccharide forms the exoskeleton of arthropods?", "chitin", ["cellulose", "glycogen", "starch"], "It is a complex polysaccharide with nitrogen."),
      ("Which turns blue-black with iodine?", "starch", ["cellulose", "glucose", "glycogen"], "Iodine sits inside the starch helix."),
      ("What is the acid-insoluble fraction of a cell mostly made of?", "macromolecules: proteins, nucleic acids, polysaccharides and lipids", ["small molecules only", "salts", "water"], "Lipids come in it because membranes break into vesicles."),
      ("What is the Michaelis constant K<sub>m</sub>?", "the substrate concentration at which the rate is half of V<sub>max</sub>", ["the highest rate", "the enzyme concentration", "the temperature for best activity"], "A low K<sub>m</sub> means high affinity."),
      ("Which is a saturated fatty acid?", "palmitic acid", ["oleic acid", "linoleic acid", "arachidonic acid"], "It has no C=C double bonds.")]


# =================================================================== 10 cell cycle and cell division
STAGES = [("prophase", "chromatin condenses into chromosomes and the spindle begins to form"), ("metaphase", "chromosomes line up at the equator (metaphase plate)"),
          ("anaphase", "the centromeres split and sister chromatids move to opposite poles"), ("telophase", "nuclear envelopes and nucleoli re-form round each set of chromosomes"),
          ("G₁ phase", "the cell grows but its DNA does not replicate"), ("S phase", "DNA replicates and the amount of DNA doubles"), ("G₂ phase", "proteins are made for mitosis while the cell keeps growing"),
          ("cytokinesis", "the cytoplasm divides to form two daughter cells")]
MEI = [("leptotene", "chromosomes become visible as thin threads"), ("zygotene", "homologous chromosomes pair up (synapsis) to form bivalents"), ("pachytene", "crossing over takes place at recombination nodules"),
       ("diplotene", "the synaptonemal complex dissolves and chiasmata are seen"), ("diakinesis", "chiasmata terminalise and the nuclear envelope breaks down"), ("anaphase I", "homologous chromosomes separate while sister chromatids stay together"),
       ("anaphase II", "sister chromatids separate as the centromere splits")]
B10 = [("How long does a typical human cell cycle take in culture?", "about 24 hours", ["about 90 minutes", "about one week", "about one year"], "Yeast takes only about 90 minutes."),
       ("What is the G₀ phase?", "a quiescent stage where cells stop dividing but stay metabolically active", ["a stage of DNA replication", "a part of mitosis", "the death of a cell"], "e.g. heart cells."),
       ("Which division is called equational division?", "mitosis", ["meiosis I", "binary fission only", "amitosis"], "The chromosome number stays the same."),
       ("Which division is called reductional division?", "meiosis I", ["mitosis", "meiosis II", "cytokinesis"], "The chromosome number is halved."),
       ("How does cytokinesis happen in plant cells?", "a cell plate forms in the middle and grows outward", ["a furrow forms from the outside", "the cell bursts", "the nucleus divides only"], "Animal cells form a cleavage furrow."),
       ("What is the significance of mitosis?", "growth, repair and keeping the chromosome number the same", ["making gametes", "halving the chromosome number", "creating genetic variation by crossing over"], "It replaces worn-out cells."),
       ("What is the significance of meiosis?", "it halves the chromosome number for gametes and creates variation", ["it repairs tissues", "it makes clones", "it doubles the chromosomes"], "Fertilisation restores the diploid number."),
       ("At which stage are chromosomes best studied?", "metaphase", ["prophase", "interphase", "telophase"], "They are most condensed then."),
       ("Which enzyme helps crossing over?", "recombinase", ["amylase", "ligase only", "helicase only"], "Crossing over is between non-sister chromatids."),
       ("What is the longest phase of meiosis I prophase in oocytes of some vertebrates?", "diplotene, which can last months or years", ["leptotene", "zygotene", "diakinesis"], "Oocytes stay in diplotene for a long time."),
       ("How many chromatids are present in a bivalent?", "four", ["two", "one", "eight"], "A bivalent is a pair of homologous chromosomes, each with two chromatids."),
       ("What happens to the DNA content in the S phase?", "it doubles from 2C to 4C", ["it halves", "it stays the same", "it becomes 8C"], "The chromosome number stays 2n."),
       ("What is karyokinesis?", "division of the nucleus", ["division of the cytoplasm", "growth of the cell", "death of the cell"], "Cytokinesis follows it."),
       ("Which cells keep dividing throughout life in plants?", "meristems", ["xylem vessels", "cork cells", "sieve tubes"], "e.g. root and shoot tips."),
       ("What forms the spindle in animal cells?", "microtubules organised by centrioles", ["actin only", "the nucleolus", "the cell wall"], "Plant cells form a spindle without centrioles.")]


# =================================================================== 11 photosynthesis
G11 = {"a C₄ plant": ["maize", "sugarcane", "sorghum", "Amaranthus", "pearl millet (bajra)"], "a C₃ plant": ["wheat", "rice", "potato", "mango", "pea", "soybean", "tomato"],
       "a step of the light reaction": ["photolysis of water", "excitation of chlorophyll by light", "electron flow from PS II to PS I", "ATP synthesis by chemiosmosis"],
       "a step of the Calvin cycle": ["carboxylation of RuBP", "reduction of 3-PGA to triose phosphate", "regeneration of RuBP"],
       "a product of the light reaction": ["ATP", "NADPH", "oxygen"], "an accessory pigment": ["chlorophyll b", "xanthophylls", "carotenoids"]}
P11 = [("PS I", "a reaction centre chlorophyll a absorbing best at 700 nm (P700)"), ("PS II", "a reaction centre chlorophyll a absorbing best at 680 nm (P680)"),
       ("RuBisCO", "the enzyme that fixes CO₂ onto RuBP"), ("PEP carboxylase", "the enzyme that fixes CO₂ in mesophyll cells of C₄ plants"), ("Kranz anatomy", "large bundle-sheath cells around the veins of C₄ leaves"),
       ("photolysis", "the splitting of water that releases oxygen"), ("photorespiration", "RuBisCO binding O₂ instead of CO₂, wasting energy"), ("Calvin cycle", "the cycle in the stroma that fixes CO₂ into sugar")]
B11 = [("Where do the light reactions of photosynthesis take place?", "in the thylakoid membranes (grana)", ["in the stroma", "in the cytoplasm", "in the mitochondria"], "The dark reactions are in the stroma."),
       ("Where does the Calvin cycle take place?", "in the stroma of the chloroplast", ["in the thylakoids", "in the mitochondria", "in the nucleus"], "It uses ATP and NADPH."),
       ("What is the first stable product of the Calvin (C₃) cycle?", "3-phosphoglyceric acid (PGA)", ["oxaloacetic acid", "glucose", "pyruvate"], "It has three carbons."),
       ("What is the first stable product in C₄ plants?", "oxaloacetic acid (OAA)", ["PGA", "glucose", "malic acid only"], "It has four carbons."),
       ("What is the primary CO₂ acceptor in C₄ plants?", "phosphoenolpyruvate (PEP)", ["RuBP", "PGA", "glucose"], "PEP carboxylase fixes CO₂ in mesophyll cells."),
       ("How many ATP and NADPH are needed to fix one molecule of CO₂ in the Calvin cycle?", "3 ATP and 2 NADPH", ["2 ATP and 3 NADPH", "1 ATP and 1 NADPH", "6 ATP and 6 NADPH"], "Six turns make one glucose: 18 ATP and 12 NADPH."),
       ("Where does the oxygen given out in photosynthesis come from?", "water", ["carbon dioxide", "glucose", "chlorophyll"], "Shown with heavy-oxygen isotopes."),
       ("Who showed with a bell jar, a mouse and a candle that plants restore 'bad' air?", "Joseph Priestley", ["Jan Ingenhousz", "Julius von Sachs", "T. W. Engelmann"], "In 1770."),
       ("Who showed that sunlight is needed for plants to purify air?", "Jan Ingenhousz", ["Joseph Priestley", "Cornelius van Niel", "Melvin Calvin"], "He used an aquatic plant in light and dark."),
       ("What does chemiosmosis in chloroplasts need?", "a proton gradient across the thylakoid membrane and ATP synthase", ["glucose", "oxygen gas", "a cell wall"], "Protons flow out through ATP synthase."),
       ("Which photosystem is used in cyclic photophosphorylation?", "only PS I", ["only PS II", "both PS I and PS II", "neither"], "It makes ATP but no NADPH or O₂."),
       ("Why do C₄ plants show almost no photorespiration?", "CO₂ is concentrated around RuBisCO in the bundle sheath", ["they have no RuBisCO", "they grow at night", "they have no chlorophyll"], "So RuBisCO works as a carboxylase."),
       ("What is the law of limiting factors?", "the rate is limited by the factor that is nearest its minimum value", ["the largest factor controls the rate", "light never limits", "all factors are equal"], "Proposed by Blackman."),
       ("Which wavelengths of light are absorbed most by chlorophyll a?", "blue and red", ["green", "yellow", "infrared"], "Green is reflected."),
       ("What is the Z scheme?", "the zig-zag path of electrons from PS II to PS I in non-cyclic photophosphorylation", ["the Calvin cycle", "the Krebs cycle", "photorespiration"], "Electrons go up in energy twice.")]


# =================================================================== 12 respiration in plants
P12 = [("glycolysis", "the cytoplasm"), ("the Krebs cycle", "the mitochondrial matrix"), ("the electron transport chain", "the inner mitochondrial membrane"), ("fermentation", "the cytoplasm, without oxygen")]
G12 = {"an end product of glycolysis": ["pyruvic acid", "a net 2 ATP", "2 NADH in the cytoplasm"], "made in the Krebs cycle": ["citric acid", "FADH₂", "GTP", "α-ketoglutaric acid"],
       "a product of anaerobic respiration": ["ethanol (in yeast)", "lactic acid (in muscle)"],
       "a part of the electron transport system": ["NADH dehydrogenase (complex I)", "cytochrome bc₁ complex (complex III)", "cytochrome c oxidase (complex IV)", "ubiquinone", "cytochrome c"]}
B12 = [("What is the net gain of ATP from glycolysis of one glucose?", "2 ATP", ["4 ATP", "36 ATP", "38 ATP"], "4 are made but 2 are used."),
       ("What is the end product of glycolysis?", "pyruvic acid", ["acetyl CoA", "citric acid", "lactic acid"], "Glucose → 2 pyruvic acid."),
       ("What is formed when pyruvate enters the mitochondrion?", "acetyl CoA, with release of CO₂ and NADH", ["citric acid directly", "lactic acid", "glucose"], "This is oxidative decarboxylation."),
       ("What is the first product of the Krebs cycle?", "citric acid", ["oxaloacetic acid", "pyruvic acid", "malic acid"], "Acetyl CoA + oxaloacetic acid → citric acid."),
       ("What is the final electron acceptor in aerobic respiration?", "oxygen", ["NAD⁺", "CO₂", "glucose"], "It forms water."),
       ("Which enzyme makes ATP in the inner mitochondrial membrane?", "ATP synthase (complex V)", ["RuBisCO", "amylase", "lipase"], "Protons flow through it."),
       ("What happens in human muscles during heavy exercise when oxygen is short?", "pyruvic acid is reduced to lactic acid", ["ethanol is formed", "fat is made", "glucose is stored"], "This causes fatigue."),
       ("Which organism makes ethanol and CO₂ by fermentation?", "yeast", ["human muscle", "a mango leaf", "a frog"], "Used in making bread and alcohol."),
       ("What is the respiratory quotient (RQ) of carbohydrates?", "1.0", ["0.7", "0.9", "4.0"], "CO₂ given out = O₂ taken in."),
       ("What is the RQ of fats such as tripalmitin?", "about 0.7", ["1.0", "about 1.3", "about 4.0"], "Fats need more oxygen to burn."),
       ("Why is respiration called an amphibolic pathway?", "it is used both for breaking down and for building molecules", ["it happens in water and on land", "it only breaks down", "it only builds up"], "Intermediates are used to make fats and proteins."),
       ("How many ATP are made from one NADH in the electron transport chain (NCERT value)?", "3 ATP", ["2 ATP", "1 ATP", "6 ATP"], "One FADH₂ gives 2 ATP."),
       ("What is the maximum net gain of ATP from one glucose in aerobic respiration (NCERT)?", "38 ATP", ["2 ATP", "8 ATP", "18 ATP"], "This is a theoretical value."),
       ("Which is used in respiration if carbohydrates run out?", "fats and then proteins", ["only water", "only DNA", "cellulose"], "Fats enter as acetyl CoA, proteins as amino acids.")]


def atp(k=None):
    R = _R[0]
    k = k or ch(["pyr", "gly", "aer", "co2", "turns", "ets"])
    n = R.randint(1, 10)
    g = "%d molecule%s of glucose" % (n, "" if n == 1 else "s")
    if k == "pyr":
        return A0("How many molecules of pyruvic acid are formed from %s in glycolysis?" % g, 2 * n, [n, 4 * n, 3 * n], "", "Each glucose gives 2 pyruvic acid: 2 × %d = <b>%d</b>." % (n, 2 * n))
    if k == "gly":
        return A0("What is the net gain of ATP when %s are broken down by glycolysis alone?" % g, 2 * n, [4 * n, 38 * n, n], " ATP", "Net 2 ATP per glucose (4 made, 2 used): <b>%d ATP</b>." % (2 * n))
    if k == "aer":
        return A0("What is the maximum net ATP (NCERT value) from the complete aerobic respiration of %s?" % g, 38 * n, [36 * n if n > 1 else 36, 2 * n, 34 * n], " ATP", "38 ATP per glucose: 38 × %d = <b>%d ATP</b>." % (n, 38 * n))
    if k == "co2":
        return A0("How many molecules of CO₂ are released in the complete aerobic respiration of %s?" % g, 6 * n, [2 * n, 3 * n, 12 * n], "", "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O: <b>%d</b>." % (6 * n))
    if k == "turns":
        return A0("How many turns of the Krebs cycle are needed to oxidise %s completely?" % g, 2 * n, [n, 6 * n, 4 * n], "", "Each glucose gives 2 acetyl CoA, so 2 turns: <b>%d</b>." % (2 * n))
    x, y = R.randint(1, 10), R.randint(1, 5)
    return A0("In the electron transport system, how many ATP are made from %d NADH and %d FADH₂ (NCERT values)?" % (x, y), 3 * x + 2 * y, [2 * x + 3 * y, 3 * (x + y), 2 * (x + y)], " ATP",
              "Each NADH gives 3 ATP and each FADH₂ gives 2: 3 × %d + 2 × %d = <b>%d ATP</b>." % (x, y, 3 * x + 2 * y))


# =================================================================== 13 plant growth and development
P13 = [("auxin", "apical dominance and root initiation on stem cuttings"), ("gibberellin", "stem elongation and bolting in cabbage"), ("cytokinin", "cell division and delaying leaf senescence"),
       ("ethylene", "fruit ripening and leaf fall"), ("abscisic acid", "closing stomata and seed dormancy (the stress hormone)")]
G13b = {"an effect of auxin": ["apical dominance", "rooting of stem cuttings", "parthenocarpy in tomato", "phototropism (bending towards light)"],
        "an effect of gibberellin": ["bolting in cabbage", "elongation of grape stalks", "breaking seed dormancy", "speeding up malting in brewing", "lengthening sugarcane stems"],
        "an effect of cytokinin": ["delaying leaf senescence", "growth of lateral shoots", "formation of new leaves and chloroplasts", "promoting cell division"],
        "an effect of ethylene": ["fruit ripening", "abscission of leaves and flowers", "horizontal growth of seedlings", "flowering in pineapple"],
        "an effect of abscisic acid": ["closing stomata", "seed dormancy", "tolerance to stress such as drought"]}
P13b = [("2,4-D", "killing broad-leaved weeds"), ("ethephon", "hastening fruit ripening and flowering in pineapple"), ("GA₃", "increasing the length of grape stalks and sugarcane stems"),
        ("NAA", "rooting of stem cuttings")]
G13 = {"a short day plant": ["chrysanthemum", "soybean", "tobacco (Maryland mammoth)", "rice"], "a long day plant": ["wheat", "spinach", "radish", "lettuce"], "a day-neutral plant": ["tomato", "cucumber", "sunflower", "chilli (pepper)"]}
B13 = [("Which hormone was first isolated from human urine?", "auxin", ["gibberellin", "cytokinin", "ethylene"], "Auxin means 'to grow'."),
       ("Which hormone was discovered from the 'bakanae' disease of rice?", "gibberellin", ["auxin", "abscisic acid", "ethylene"], "Gibberella fujikuroi caused tall seedlings."),
       ("Which hormone is a gas?", "ethylene", ["auxin", "cytokinin", "gibberellin"], "It speeds ripening."),
       ("What is apical dominance?", "the growing shoot tip stops lateral buds from growing", ["roots grow faster than shoots", "leaves fall in autumn", "seeds stay dormant"], "Removing the tip (as in tea plants) gives a bushy plant."),
       ("What is vernalisation?", "promotion of flowering by a period of low temperature", ["flowering in long days", "ripening of fruit", "growth towards light"], "e.g. winter wheat and biennials."),
       ("What is photoperiodism?", "the response of plants to the relative lengths of day and night", ["growth towards light", "movement of leaves", "bending of roots"], "It controls flowering."),
       ("Where is the stimulus for photoperiodic flowering perceived?", "in the leaves", ["in the roots", "in the shoot tips only", "in the flowers"], "A hormone then moves to the shoot tip."),
       ("What is the sigmoid growth curve?", "an S-shaped curve with lag, log (exponential) and stationary phases", ["a straight line", "a falling curve", "a circle"], "Seen in cells, tissues and organs."),
       ("What is dedifferentiation?", "differentiated cells regaining the ability to divide", ["cells dying", "cells becoming specialised", "seeds germinating"], "e.g. formation of cork cambium from parenchyma."),
       ("Which hormone helps seeds stay dormant?", "abscisic acid", ["gibberellin", "cytokinin", "auxin"], "Gibberellins break dormancy."),
       ("Which hormone causes bolting in cabbage?", "gibberellin", ["auxin", "ethylene", "abscisic acid"], "Bolting is rapid stem growth before flowering."),
       ("What is the arithmetic growth equation?", "L<sub>t</sub> = L₀ + rt", ["W<sub>t</sub> = W₀e<sup>rt</sup>", "L = rt²", "W = W₀ − rt"], "Only one daughter cell keeps dividing."),
       ("What is heterophylly?", "different shapes of leaves on the same plant", ["the same leaf in all plants", "leaves falling", "no leaves"], "e.g. buttercup in water and in air."),
       ("Which hormone is called the stress hormone?", "abscisic acid", ["ethylene", "auxin", "cytokinin"], "It helps plants survive drought."),
       ("Which hormone is found in coconut milk and maize kernels?", "cytokinins (zeatin)", ["auxin", "abscisic acid", "ethylene"], "Kinetin was first found in autoclaved herring sperm DNA.")]


# =================================================================== 14 breathing and exchange of gases
G10 = {"an event of prophase I of meiosis": ["synapsis of homologous chromosomes", "crossing over", "formation of chiasmata", "terminalisation of chiasmata"],
       "an event of interphase": ["DNA replication", "duplication of the centriole", "synthesis of proteins for division", "growth of the cell"],
       "an event of mitotic anaphase": ["splitting of the centromeres", "sister chromatids moving to opposite poles"],
       "an event of telophase": ["re-formation of the nuclear envelope", "reappearance of the nucleolus", "chromosomes uncoiling at the poles"]}
G14 = {"a part of the conducting zone": ["nostrils", "pharynx", "larynx", "trachea", "bronchi"], "a part of the exchange (respiratory) zone": ["alveoli", "alveolar ducts", "respiratory bronchioles"],
       "a respiratory disorder": ["asthma", "emphysema", "silicosis", "bronchitis"], "a muscle used in breathing": ["diaphragm", "external intercostal muscles", "internal intercostal muscles", "abdominal muscles"]}
G18 = {"a part of the forebrain": ["cerebrum", "thalamus", "hypothalamus", "corpus callosum"], "a part of the hindbrain": ["pons", "cerebellum", "medulla oblongata"],
       "a part of the eye": ["retina", "cornea", "iris", "lens", "ciliary body", "sclera", "choroid", "aqueous humour"], "a part of the ear": ["cochlea", "tympanic membrane", "malleus", "semicircular canals", "Eustachian tube", "stapes", "incus", "organ of Corti"],
       "a part of the midbrain": ["corpora quadrigemina", "cerebral aqueduct"]}
G19 = {"a hormone of the anterior pituitary": ["growth hormone", "prolactin", "TSH", "ACTH", "LH", "FSH"], "a hormone released from the posterior pituitary": ["oxytocin", "vasopressin (ADH)"],
       "a hormone of the pancreas": ["insulin", "glucagon"], "a hormone of the adrenal gland": ["adrenaline", "noradrenaline", "cortisol", "aldosterone"],
       "a hormone of the thyroid gland": ["thyroxine (T₄)", "triiodothyronine (T₃)", "thyrocalcitonin"],
       "a hormone of the gonads": ["testosterone", "oestrogen", "progesterone", "relaxin"], "a gastrointestinal hormone": ["gastrin", "secretin", "cholecystokinin (CCK)", "GIP"]}
LUNG = [("tidal volume", 500), ("inspiratory reserve volume", 2750), ("expiratory reserve volume", 1100), ("residual volume", 1200)]


def lungvol(k=None):
    R = _R[0]
    tv, irv, erv, rv = [R.randrange(a, b, 50) for a, b in [(450, 550), (2500, 3100), (1000, 1250), (1100, 1300)]]
    k = k or ch(["vc", "ic", "ec", "frc", "tlc", "mv"])
    txt = "In a healthy adult, TV = %d mL, IRV = %d mL, ERV = %d mL and RV = %d mL." % (tv, irv, erv, rv)
    if k == "mv":
        rate = R.randint(12, 16)
        return A0("A person breathes %d times a minute with a tidal volume of %d mL. How much air does he breathe in each minute?" % (rate, tv), rate * tv,
                  [rate * tv / 2, tv, rate + tv], " mL", "Pulmonary ventilation = rate × TV = %d × %d = <b>%s mL</b>." % (rate, tv, nf(rate * tv)))
    d = {"vc": ("vital capacity", erv + tv + irv, "ERV + TV + IRV", [tv + irv, erv + tv + irv + rv, irv + erv]), "ic": ("inspiratory capacity", tv + irv, "TV + IRV", [tv + erv, erv + tv + irv, irv]),
         "ec": ("expiratory capacity", tv + erv, "TV + ERV", [tv + irv, erv + rv, erv]), "frc": ("functional residual capacity", erv + rv, "ERV + RV", [erv + tv, rv, tv + rv]),
         "tlc": ("total lung capacity", erv + tv + irv + rv, "RV + ERV + TV + IRV", [erv + tv + irv, tv + irv + rv, erv + rv])}[k]
    return A0("%s What is the %s?" % (txt, d[0]), d[1], d[3], " mL", "%s = %s = <b>%s mL</b>." % (d[0][0].upper() + d[0][1:], d[2], nf(d[1])))


def A0(q, v, w, u, e):
    import uk_alsci
    return uk_alsci.nq(q, v, w, u, e)


B14 = [("Where does gas exchange take place in the lungs?", "in the alveoli", ["in the trachea", "in the bronchi", "in the larynx"], "Their walls are one cell thick."),
       ("Which muscle contracts and flattens during inspiration?", "the diaphragm", ["the abdominal muscles", "the internal intercostals", "the heart"], "The external intercostals also contract."),
       ("What is the partial pressure of oxygen in alveolar air?", "about 104 mm Hg", ["about 40 mm Hg", "about 159 mm Hg", "about 0 mm Hg"], "Deoxygenated blood has about 40 mm Hg."),
       ("What percentage of oxygen is carried by haemoglobin as oxyhaemoglobin?", "about 97%", ["about 3%", "about 50%", "about 7%"], "About 3% is dissolved in plasma."),
       ("How is most carbon dioxide carried in the blood?", "as bicarbonate ions (about 70%)", ["dissolved in plasma (about 70%)", "as carbaminohaemoglobin (about 70%)", "as carbonic acid gas"], "20–25% is carbaminohaemoglobin and about 7% is dissolved."),
       ("Which enzyme in red blood cells converts CO₂ and water to carbonic acid?", "carbonic anhydrase", ["amylase", "pepsin", "lipase"], "It is very fast."),
       ("Which part of the brain is the respiratory rhythm centre?", "the medulla oblongata", ["the cerebrum", "the cerebellum", "the hypothalamus"], "The pneumotaxic centre in the pons can moderate it."),
       ("What shifts the oxygen dissociation curve to the right?", "high pCO₂, high H⁺ (low pH) and high temperature", ["low pCO₂", "low temperature", "high pH"], "Oxygen is released more easily in tissues."),
       ("What is emphysema?", "a disease in which the alveolar walls are damaged, reducing the surface area", ["inflammation of the bronchi", "a lung infection by bacteria", "a heart disease"], "Cigarette smoking is a major cause."),
       ("What is asthma?", "difficulty in breathing due to inflammation of the bronchi and bronchioles", ["loss of alveolar walls", "a heart attack", "a kidney disease"], "It causes wheezing."),
       ("What is the sigmoid curve that plots % saturation of haemoglobin against pO₂ called?", "the oxygen dissociation curve", ["the growth curve", "the ECG", "the spirogram"], "It is S-shaped."),
       ("Which structure stops food from entering the windpipe?", "the epiglottis", ["the glottis", "the larynx", "the uvula"], "It is a flap of cartilage."),
       ("What are the C-shaped rings in the trachea made of?", "cartilage", ["bone", "muscle", "ligament"], "They keep the trachea open."),
       ("Which instrument measures lung volumes?", "a spirometer", ["a sphygmomanometer", "a stethoscope", "a thermometer"], "It traces a spirogram."),
       ("What is an occupational respiratory disorder?", "lung damage caused by long exposure to dust at work, as in stone grinding", ["asthma from pollen", "a cold", "emphysema from smoking only"], "Masks protect workers.")]


# =================================================================== 15 body fluids and circulation
G15 = {"a granulocyte": ["neutrophil", "eosinophil", "basophil"], "an agranulocyte": ["lymphocyte", "monocyte"], "a plasma protein": ["albumin", "globulin", "fibrinogen"]}
P15 = [("neutrophils", "the most abundant white blood cells (60–65%), phagocytic"), ("eosinophils", "resisting infections and allergic reactions"), ("basophils", "secreting histamine, serotonin and heparin"),
       ("lymphocytes", "B and T cells of the immune response"), ("monocytes", "becoming macrophages that engulf germs"), ("platelets", "releasing factors that help blood clot"),
       ("fibrinogen", "forming fibrin threads in clotting"), ("SA node", "the pacemaker that starts each heartbeat"), ("AV node", "passing the impulse from the atria to the ventricles"),
       ("bundle of His", "carrying the impulse down the interventricular septum")]
BLOOD = [("A", "antigen A", "anti-B", "A and O"), ("B", "antigen B", "anti-A", "B and O"), ("AB", "antigens A and B", "no antibodies", "all groups (universal recipient)"), ("O", "no antigens", "anti-A and anti-B", "only O")]
B15 = [("What is the normal blood pressure of a healthy adult?", "120/80 mm Hg", ["80/120 mm Hg", "140/90 mm Hg", "100/50 mm Hg"], "Systolic over diastolic."),
       ("How many heartbeats does a healthy adult have each minute at rest?", "about 72", ["about 20", "about 150", "about 200"], "It is set by the SA node."),
       ("What is the stroke volume of a healthy adult heart?", "about 70 mL", ["about 5 L", "about 7 mL", "about 700 mL"], "Cardiac output = 72 × 70 mL ≈ 5 L per minute."),
       ("Which sound of the heart is 'lub'?", "the closing of the tricuspid and bicuspid (AV) valves", ["the closing of the semilunar valves", "the opening of the valves", "blood hitting the aorta"], "'Dub' is the closing of the semilunar valves."),
       ("What does the P-wave of an ECG show?", "depolarisation of the atria", ["depolarisation of the ventricles", "repolarisation of the ventricles", "the closing of valves"], "QRS shows ventricular depolarisation; T shows ventricular repolarisation."),
       ("Which blood group is the universal donor?", "O negative (O)", ["AB", "A", "B"], "Its cells carry no A or B antigen."),
       ("Which condition can occur when an Rh-negative mother carries an Rh-positive baby for the second time?", "erythroblastosis foetalis", ["haemophilia", "anaemia from diet", "leukaemia"], "Her anti-Rh antibodies destroy the baby's red cells."),
       ("Which type of circulation do fishes have?", "single circulation", ["double circulation", "no circulation", "open circulation"], "Blood passes through the heart once per circuit."),
       ("What is double circulation?", "blood passes through the heart twice in one complete circuit: pulmonary and systemic", ["blood flows in two directions", "two hearts", "blood and lymph together"], "Found in birds and mammals."),
       ("Which is the hepatic portal system?", "veins that carry blood from the intestine to the liver before it returns to the heart", ["arteries to the brain", "the coronary arteries", "veins from the legs"], "The liver processes absorbed food."),
       ("What is the life span of a red blood cell?", "about 120 days", ["about 12 days", "about 1 year", "about 3 days"], "They are destroyed in the spleen."),
       ("What is lymph?", "tissue fluid in lymph vessels, containing lymphocytes", ["blood with red cells", "a hormone", "plasma with platelets"], "It returns fluid to the blood."),
       ("What is angina pectoris?", "acute chest pain when not enough oxygen reaches the heart muscle", ["high blood pressure", "a valve problem", "a blood cancer"], "It is a warning sign of heart disease."),
       ("What is atherosclerosis (coronary artery disease)?", "narrowing of the arteries by deposits of calcium, fat and cholesterol", ["infection of the heart", "rapid heartbeat", "low blood pressure"], "It can lead to a heart attack."),
       ("How many litres of blood does a healthy adult have?", "about 5 litres", ["about 1 litre", "about 10 litres", "about 50 litres"], "Plasma is about 55% of it.")]


# =================================================================== 16 excretory products
G16 = {"ammonotelic": ["bony fishes", "tadpoles", "aquatic amphibians", "aquatic insects"], "ureotelic": ["humans", "frogs (adults)", "mammals", "marine fishes"],
       "uricotelic": ["birds", "reptiles", "land snails", "land insects such as cockroaches"]}
G16b = {"a part of the nephron found in the cortex": ["glomerulus", "Bowman's capsule", "proximal convoluted tubule", "distal convoluted tubule"],
        "a kidney disorder": ["renal calculi (kidney stones)", "glomerulonephritis", "uraemia", "renal failure"],
        "an excretory structure of an invertebrate": ["flame cells", "nephridia", "Malpighian tubules", "antennal (green) glands"]}
P16 = [("Bowman's capsule", "the cup-shaped part of the nephron around the glomerulus"), ("glomerulus", "the tuft of capillaries where ultrafiltration happens"),
       ("proximal convoluted tubule (PCT)", "the part that reabsorbs nearly all glucose, amino acids and 70–80% of salts and water"), ("loop of Henle", "the part that keeps the medulla salty so concentrated urine can form"),
       ("distal convoluted tubule (DCT)", "the part where conditional reabsorption of Na⁺ and water takes place"), ("collecting duct", "the part where water is reabsorbed under the control of ADH"),
       ("juxtaglomerular apparatus", "the cells that release renin when blood pressure falls"), ("ADH (vasopressin)", "the hormone that increases water reabsorption"),
       ("aldosterone", "the hormone that increases Na⁺ reabsorption in the DCT"), ("ANF", "the factor from the heart that widens blood vessels and lowers blood pressure")]
B16 = [("How much glomerular filtrate do the kidneys form each day?", "about 180 litres", ["about 1.5 litres", "about 18 litres", "about 1,800 litres"], "GFR is about 125 mL per minute."),
       ("How much urine does a healthy adult pass each day?", "about 1 to 1.5 litres", ["about 180 litres", "about 10 litres", "about 0.1 litre"], "Over 99% of the filtrate is reabsorbed."),
       ("What is the glomerular filtration rate (GFR) of a healthy person?", "about 125 mL per minute", ["about 12 mL per minute", "about 1.25 L per minute", "about 1,250 mL per minute"], "180 L per day."),
       ("What are the excretory organs of earthworms?", "nephridia", ["flame cells", "Malpighian tubules", "kidneys"], "Flatworms have flame cells."),
       ("What are the excretory organs of insects such as cockroaches?", "Malpighian tubules", ["nephridia", "flame cells", "green glands"], "Prawns have antennal (green) glands."),
       ("What is the counter-current mechanism?", "flow in opposite directions in the loop of Henle and vasa recta that keeps the medulla concentrated", ["flow of blood in arteries", "flow of urine to the bladder", "flow of air in the lungs"], "It lets mammals make concentrated urine."),
       ("What is micturition?", "the process of passing urine", ["filtration in the glomerulus", "making urea in the liver", "reabsorption of water"], "It is a reflex controlled by the nervous system."),
       ("Where is urea made in the body?", "in the liver", ["in the kidneys", "in the bladder", "in the lungs"], "By the ornithine cycle."),
       ("What does glycosuria mean?", "glucose in the urine", ["ketones in the urine", "blood in the urine", "too much urine"], "It is a sign of diabetes mellitus."),
       ("What is haemodialysis?", "removing urea from blood with an artificial kidney", ["a kidney transplant", "making urine", "a blood test"], "Used in kidney failure (uraemia)."),
       ("What are renal calculi?", "stones in the kidney, often of calcium oxalate", ["kidney infections", "kidney cancer", "excess urine"], "Glomerulonephritis is inflammation of the glomeruli."),
       ("Which part of the nephron is impermeable to water?", "the ascending limb of the loop of Henle", ["the descending limb", "the PCT", "the collecting duct with ADH"], "It actively moves salt out."),
       ("Which hormone system acts when blood pressure falls?", "the renin–angiotensin–aldosterone system", ["insulin–glucagon", "thyroxine", "ADH only"], "Angiotensin II narrows blood vessels."),
       ("Besides the kidneys, which organ removes CO₂?", "the lungs", ["the liver", "the stomach", "the heart"], "Skin also removes some salts in sweat."),
       ("Why is ammonia excreted only by aquatic animals?", "it is very toxic and needs a lot of water to remove it", ["it is not toxic", "it is a solid", "land animals cannot make it"], "Uric acid needs the least water.")]


def gfr(k=None):
    R = _R[0]
    k = k or ch(["day", "urine", "pct", "hour"])
    g = R.randrange(100, 141, 5)
    if k == "day":
        return A0("A person's glomerular filtration rate is %d mL per minute. How many litres of filtrate are formed in a day?" % g, g * 1440 / 1000, [g * 60 / 1000, g * 24 / 1000, g * 1440], " L",
                  "%d mL × 1440 minutes = %s mL = <b>%s L</b>." % (g, nf(g * 1440), nf(g * 1440 / 1000)))
    if k == "hour":
        return A0("A person's glomerular filtration rate is %d mL per minute. How much filtrate is formed in one hour?" % g, g * 60, [g * 24, g / 60, g * 1440], " mL", "%d mL × 60 = <b>%s mL</b>." % (g, nf(g * 60)))
    f = R.randrange(150, 191, 5)
    p = R.choice([99, 99.2, 99.4, 99.5])
    u = f * (100 - p) / 100
    if k == "urine":
        return A0("The kidneys form %d L of filtrate in a day and %s%% of it is reabsorbed. How much urine is passed?" % (f, nf(p)), u, [f * p / 100, f - p, f * (100 - p)], " L", "Urine = %d × %s%% = <b>%s L</b>." % (f, nf(100 - p), nf(u)))
    uu = R.choice([1.0, 1.2, 1.5, 1.8])
    return A0("The kidneys form %d L of filtrate and %s L of urine in a day. What percentage of the filtrate is reabsorbed?" % (f, nf(uu)), (f - uu) / f * 100, [uu / f * 100, f - uu, (f - uu) / f], "%",
              "Reabsorbed = (%d − %s) ÷ %d × 100 = <b>%s%%</b>." % (f, nf(uu), f, nf((f - uu) / f * 100)))


# =================================================================== 17 locomotion and movement
G17 = {"a part of the axial skeleton": ["skull", "vertebral column", "sternum", "ribs", "hyoid bone", "ear ossicles"],
       "a part of the appendicular skeleton": ["femur", "humerus", "scapula", "pelvic girdle", "patella", "radius", "ulna", "tibia", "fibula", "clavicle", "carpals"],
       "a protein of the muscle fibre": ["actin", "myosin", "troponin", "tropomyosin"], "a type of movement in cells": ["amoeboid movement", "ciliary movement", "flagellar movement"],
       "a disorder of muscles or bones": ["arthritis", "osteoporosis", "gout", "tetany", "myasthenia gravis", "muscular dystrophy"]}
P17 = [("ball and socket joint", "the shoulder and hip"), ("hinge joint", "the knee and elbow"), ("pivot joint", "the atlas and axis"), ("gliding joint", "the carpals"),
       ("saddle joint", "the carpal and metacarpal of the thumb"), ("fibrous (immovable) joint", "the sutures of the skull"), ("cartilaginous joint", "the vertebrae")]
P17b = [("myasthenia gravis", "an autoimmune disorder affecting the neuromuscular junction"), ("muscular dystrophy", "a genetic disorder in which skeletal muscle gradually wastes away"),
        ("tetany", "rapid spasms in muscle due to low Ca²⁺ in body fluid"), ("arthritis", "inflammation of joints"), ("osteoporosis", "loss of bone mass with age, often due to low oestrogen"),
        ("gout", "inflammation of joints due to deposits of uric acid crystals")]
B17 = [("How many bones are there in the adult human skeleton?", "206", ["300", "106", "212"], "80 axial and 126 appendicular."),
       ("How many pairs of ribs do humans have?", "12 pairs", ["10 pairs", "14 pairs", "24 pairs"], "The last two pairs are floating ribs."),
       ("How many vertebrae are there in the human vertebral column?", "26", ["33", "24", "30"], "Some fuse to form the sacrum and coccyx."),
       ("What is the functional unit of a myofibril?", "the sarcomere", ["the actin filament", "the tendon", "the nucleus"], "It runs from one Z line to the next."),
       ("What happens to the I-band during muscle contraction?", "it shortens", ["it gets longer", "it stays the same", "it disappears and reappears"], "The A-band stays the same length."),
       ("Which ion binds to troponin to start muscle contraction?", "Ca²⁺", ["Na⁺", "K⁺", "Cl⁻"], "It uncovers the binding sites on actin."),
       ("Which theory explains muscle contraction?", "the sliding filament theory", ["the lock-and-key theory", "the cell theory", "the germ theory"], "Thin filaments slide over thick filaments."),
       ("What is the thick filament of a sarcomere made of?", "myosin", ["actin", "troponin", "tropomyosin"], "Myosin heads form cross-bridges."),
       ("Which muscle fibres are called red fibres?", "fibres rich in myoglobin and mitochondria", ["fibres with little myoglobin", "smooth muscle fibres", "cardiac fibres only"], "They are suited to aerobic work."),
       ("Which type of movement do macrophages and leucocytes show?", "amoeboid movement", ["ciliary movement", "muscular movement", "flagellar movement"], "Using pseudopodia."),
       ("Where is ciliary movement seen in humans?", "in the trachea and fallopian tubes", ["in skeletal muscle", "in the heart", "in bones"], "Cilia sweep mucus and move the ovum."),
       ("Which is the only movable bone of the skull?", "the mandible (lower jaw)", ["the maxilla", "the frontal bone", "the nasal bone"], "It forms a joint with the temporal bone."),
       ("How many bones are there in the human skull?", "22", ["8", "14", "29"], "8 cranial and 14 facial bones."),
       ("Which molecule supplies energy for the myosin head to move?", "ATP", ["glucose directly", "oxygen", "Ca²⁺"], "The myosin head has ATPase activity."),
       ("Which girdle joins the lower limbs to the axial skeleton?", "the pelvic girdle", ["the pectoral girdle", "the rib cage", "the skull"], "It has two coxal bones.")]


# =================================================================== 18 neural control and coordination
P18 = [("cerebrum", "thinking, memory, intelligence and voluntary actions"), ("cerebellum", "balance and coordination of movements"), ("medulla oblongata", "breathing, heartbeat and gastric secretions"),
       ("hypothalamus", "body temperature, hunger and thirst, and releasing hormones"), ("corpus callosum", "connecting the two cerebral hemispheres"), ("pons", "connecting different regions of the brain and helping control breathing"),
       ("thalamus", "relaying sensory and motor signals"), ("limbic system", "emotions and behaviour such as fear and pleasure")]
P18b = [("rods", "dim light (twilight) vision, with rhodopsin"), ("cones", "daylight and colour vision"), ("fovea", "the point of sharpest vision, with only cones"), ("blind spot", "the place where the optic nerve leaves the eye, with no photoreceptors"),
        ("cochlea", "hearing, with the organ of Corti"), ("semicircular canals", "balance during movement"), ("ear ossicles", "malleus, incus and stapes, which pass vibrations to the inner ear")]
B18 = [("What is the resting membrane potential of a neuron?", "about −70 mV", ["about +70 mV", "about 0 mV", "about −7 V"], "The inside is negative compared with the outside."),
       ("Which ions rush into an axon during depolarisation?", "Na⁺", ["K⁺", "Cl⁻", "Ca²⁺ only"], "The inside becomes positive."),
       ("What keeps the resting potential by moving 3 Na⁺ out and 2 K⁺ in?", "the sodium–potassium pump", ["the synapse", "the myelin sheath", "the dendrite"], "It uses ATP."),
       ("Why do impulses travel faster in myelinated fibres?", "they jump from one node of Ranvier to the next (saltatory conduction)", ["the axon is shorter", "there is no membrane", "they move in both directions"], "The myelin sheath insulates the axon."),
       ("Which chemical is a common neurotransmitter?", "acetylcholine", ["insulin", "thyroxine", "haemoglobin"], "It crosses the synaptic cleft."),
       ("What is a reflex action?", "a quick, automatic response to a stimulus controlled by the spinal cord", ["a voluntary action", "a learned skill", "a hormone action"], "e.g. pulling the hand away from a hot object."),
       ("What does a reflex arc need at the least?", "a receptor, an afferent neuron, the spinal cord, an efferent neuron and an effector", ["only the brain", "only a muscle", "only a hormone"], "The knee-jerk reflex is an example."),
       ("Which cells form the myelin sheath in the peripheral nervous system?", "Schwann cells", ["red blood cells", "osteocytes", "neuroglia of the brain only"], "Gaps between them are nodes of Ranvier."),
       ("Which part of the nervous system is the brain and spinal cord?", "the central nervous system", ["the peripheral nervous system", "the autonomic system only", "the somatic system"], "Nerves outside it are the PNS."),
       ("Which division of the autonomic nervous system prepares the body for 'fight or flight'?", "the sympathetic nervous system", ["the parasympathetic nervous system", "the somatic system", "the CNS"], "The parasympathetic system calms the body."),
       ("What covers and protects the brain?", "three layers of meninges: dura mater, arachnoid and pia mater", ["the skin only", "bone marrow", "a mucous membrane"], "The skull also protects it."),
       ("Where in the eye is the image formed?", "on the retina", ["on the cornea", "on the lens", "on the iris"], "Photoreceptors convert light to impulses."),
       ("Which part of the eye controls the amount of light entering?", "the iris (by changing the size of the pupil)", ["the lens", "the retina", "the cornea"], "The pupil is the hole in the iris."),
       ("What is the gap between two neurons called?", "the synaptic cleft", ["the node of Ranvier", "the axon hillock", "the dendrite"], "Neurotransmitters cross it."),
       ("Which type of neuron carries impulses from the CNS to muscles?", "motor (efferent) neurons", ["sensory (afferent) neurons", "interneurons only", "receptors"], "Sensory neurons carry impulses to the CNS.")]


# =================================================================== 19 chemical coordination
P19 = [("insulin", "the pancreas (β-cells)", "lowering blood glucose"), ("glucagon", "the pancreas (α-cells)", "raising blood glucose"), ("thyroxine", "the thyroid", "controlling the basal metabolic rate"),
       ("adrenaline", "the adrenal medulla", "the emergency (fight or flight) response"), ("cortisol", "the adrenal cortex", "raising blood glucose and reducing inflammation"),
       ("parathyroid hormone", "the parathyroid glands", "raising the Ca²⁺ level in the blood"), ("thyrocalcitonin", "the thyroid", "lowering the Ca²⁺ level in the blood"),
       ("melatonin", "the pineal gland", "the daily (24-hour) rhythm of sleep and wakefulness"), ("growth hormone", "the anterior pituitary", "body growth"),
       ("oxytocin", "the posterior pituitary (made in the hypothalamus)", "contraction of the uterus during childbirth and milk ejection"),
       ("testosterone", "the Leydig cells of the testis", "male secondary sexual characters"), ("thymosins", "the thymus", "development of T-lymphocytes"),
       ("progesterone", "the corpus luteum", "maintaining pregnancy"), ("ANF", "the atrial wall of the heart", "lowering blood pressure")]
DIS = [("diabetes mellitus", "too little insulin"), ("goitre", "too little iodine and thyroxine"), ("cretinism", "too little thyroid hormone in children"), ("gigantism", "too much growth hormone in children"),
       ("acromegaly", "too much growth hormone in adults"), ("Addison's disease", "too little hormone from the adrenal cortex"), ("Graves' disease (exophthalmic goitre)", "too much thyroid hormone"),
       ("diabetes insipidus", "too little ADH (vasopressin)"), ("pituitary dwarfism", "too little growth hormone in children")]
B19 = [("Which gland is called the master gland?", "the pituitary gland", ["the thyroid gland", "the adrenal gland", "the pancreas"], "It controls many other glands, though the hypothalamus controls it."),
       ("Which gland is both an exocrine and an endocrine gland?", "the pancreas", ["the thyroid", "the pituitary", "the adrenal gland"], "It makes digestive juice and hormones."),
       ("Which hormones are made in the hypothalamus but stored in the posterior pituitary?", "oxytocin and vasopressin (ADH)", ["insulin and glucagon", "thyroxine and calcitonin", "GH and prolactin"], "They travel down nerve axons."),
       ("Which hormone is called the 'fight or flight' hormone?", "adrenaline", ["insulin", "melatonin", "thyroxine"], "It raises heartbeat and blood glucose."),
       ("Which element is needed to make thyroxine?", "iodine", ["iron", "calcium", "sodium"], "Lack of it causes goitre."),
       ("How do steroid hormones act on target cells?", "they enter the cell and bind receptors inside, changing gene expression", ["they stay outside the cell", "they make the cell burst", "they act only on bones"], "e.g. cortisol and oestrogen."),
       ("How do protein hormones such as insulin act on target cells?", "they bind receptors on the membrane and use second messengers such as cAMP", ["they enter the nucleus", "they are stored in fat", "they act as enzymes in blood"], "They cannot cross the membrane."),
       ("Which hormone is called the hormone of pregnancy?", "progesterone", ["oestrogen", "oxytocin", "prolactin"], "It keeps the uterus lining ready."),
       ("Which hormone controls the secretion of gastric juice?", "gastrin", ["secretin", "insulin", "thyroxine"], "It is made by the stomach wall."),
       ("Which hormone acts on the exocrine pancreas to release water and bicarbonate ions?", "secretin", ["gastrin", "cholecystokinin", "insulin"], "It is made in the duodenum."),
       ("Which part of the body controls the pituitary by releasing hormones?", "the hypothalamus", ["the cerebellum", "the thyroid", "the pancreas"], "It links the nervous and endocrine systems."),
       ("What is the role of glucocorticoids such as cortisol?", "raising blood glucose (gluconeogenesis) and suppressing inflammation", ["lowering blood glucose", "controlling Ca²⁺", "making melanin"], "They are made in the adrenal cortex."),
       ("What is the hormone made by the pineal gland?", "melatonin", ["thymosin", "adrenaline", "insulin"], "It controls the sleep–wake cycle."),
       ("Which gland shrinks (degenerates) in old people, reducing immunity?", "the thymus", ["the thyroid", "the adrenal", "the pituitary"], "It is large in children.")]


def _fam(g, *fams):
    FAM[id(g)] = [list(x) for x in fams]


_fam(G1, ["a defining feature of all living things", "a thing that grows only by adding material from outside"], ["a taxonomic category (rank)"], ["a taxonomic aid"])
_fam(G2, ["in kingdom Monera", "in kingdom Protista", "in kingdom Fungi"], ["a disease caused by a virus", "a disease caused by a protozoan", "a disease caused by bacteria"])
_fam(G5, ["a modified root", "a modified stem", "a modified leaf"], ["a dicot plant", "a monocot plant"], ["in family Fabaceae", "in family Solanaceae", "in family Liliaceae"])
_fam(G6, ["a primary meristem", "a simple permanent tissue", "a conducting element of xylem", "a part of phloem found in angiosperms", "a lateral meristem"],
     ["a part of the epidermal tissue system", "a part of the ground tissue system", "a part of the vascular tissue system"])
_fam(G7, ["an epithelial tissue", "a connective tissue", "a muscle tissue"], ["a cell junction"], ["a feature of the frog"])
_fam(G11, ["a C₄ plant", "a C₃ plant"], ["a step of the light reaction", "a step of the Calvin cycle", "a product of the light reaction", "an accessory pigment"])
_fam(G14, ["a part of the conducting zone", "a part of the exchange (respiratory) zone"], ["a respiratory disorder"], ["a muscle used in breathing"])
_fam(G16b, ["a part of the nephron found in the cortex"], ["a kidney disorder"], ["an excretory structure of an invertebrate"])
_fam(G17, ["a part of the axial skeleton", "a part of the appendicular skeleton"], ["a protein of the muscle fibre"], ["a type of movement in cells"], ["a disorder of muscles or bones"])
_fam(G18, ["a part of the forebrain", "a part of the hindbrain", "a part of the midbrain"], ["a part of the eye", "a part of the ear"])


def UNITS():
    b = {k: B(globals()["B%d" % k]) for k in range(1, 20)}
    od = {k: OD(globals()["G%s" % k]) for k in ("1", "2", "3", "4", "4b", "5", "6", "7", "8", "9", "10", "11", "12", "13", "13b", "14", "15", "16", "16b", "17", "18", "19")}
    ab = lambda r: [(x, y, "%s: %s." % (x, y)) for x, y in r]
    p1 = PR(P1, "What is the common name of <i>%s</i>?", "Which is the scientific name for %s?")
    p1b = PR(ab(P1b), "What is a %s?", "Which taxonomic aid is %s?")
    p2 = PR(P2, "Which description fits kingdom %s?", "Which kingdom has members that are %s?")
    p2b = PR(P2b, "Which fungi belong to %s?", "To which class of fungi do %s belong?")
    p3 = PR(P3, "Which description fits %s?", "Which class of algae is described as %s?", pool=["blue-green algae, prokaryotes with chlorophyll a", "mosses with no vascular tissue"])
    p3b = PR([(y, x) for x, y in P3b], "Which plants are called %s?", "Which group of plants is described as %s?")
    p4 = PR(P4, "Which feature is typical of phylum %s?", "Which phylum shows %s?")
    p5 = PR(P5, "Which description fits family %s?", "Which family is described as %s?", pool=["mustard and radish: cruciform flowers, siliqua fruit", "sunflower and marigold: heads of florets"])
    p5b = PR(P5b, "What is %s?", "Which term describes this: %s?")
    p6 = PR(P6, "Which description fits a %s?", "In which organ is this seen: %s?")
    p6b = PR(P6b, "Which description fits %s?", "Which tissue or structure is described as %s?")
    p7 = PR(P7, "Where is %s found, or what does it do?", "Which tissue matches this description: %s?")
    p8 = PR(P8, "What is the main function of %s?", "Which organelle is responsible for %s?")
    p9 = PR(P9, "What do %s do?", "Which class of enzymes is responsible for %s?")
    p9b = PR(P9b, "What is %s an example of?", None, pool=["a substrate", "an end product", "a hydrolase"])
    st = PR(STAGES, "What happens in %s?", "In which stage of the cell cycle does this happen: %s?")
    mei = PR(MEI, "What happens in %s of meiosis?", "In which stage of meiosis does this happen: %s?")
    p11 = PR(P11, "What is %s?", "What is the name for %s?")
    p12 = PR(P12, "Where in the cell does %s take place?", None, pool=["the nucleus", "the chloroplast", "the Golgi apparatus"])
    p13 = PR(P13, "Which effect is caused by %s?", "Which plant hormone causes %s?")
    p13b = PR(P13b, "What is %s used for in agriculture?", "Which chemical is used for %s?")
    p15 = PR(P15, "What is the role of %s?", "Which part of the blood or heart is responsible for %s?")
    bl = PR([(g, a, "Blood group %s: %s on the red cells, %s in the plasma." % (g, a, ab_)) for g, a, ab_, _ in BLOOD], "Which antigen is on the red blood cells of a person with blood group %s?", "Which blood group has %s on its red blood cells?")
    bl2 = PR([(g, ab_, "Blood group %s has %s in the plasma." % (g, ab_)) for g, a, ab_, _ in BLOOD], "Which antibodies are in the plasma of blood group %s?", "Which blood group has %s in its plasma?")
    p16 = PR(P16, "What is the %s?", "Which term matches this description: %s?")
    p17 = PR(P17, "Where is a %s found in the body?", "Which type of joint is found in %s?")
    p17b = PR(P17b, "What is %s?", "Which disorder is %s?")
    p18 = PR(P18, "Which function is controlled by the %s?", "Which part of the brain controls %s?")
    p18b = PR(P18b, "What is the role of the %s?", "Which part of the eye or ear is responsible for %s?")
    p19 = PR([(h, s, "%s is made in %s." % (h[0].upper() + h[1:], s)) for h, s, f in P19], "Which gland secretes %s?", None)
    p19b = PR([(h, f, "%s: %s." % (h[0].upper() + h[1:], f)) for h, s, f in P19], "What is the main role of %s?", "Which hormone is responsible for %s?")
    dis = PR(DIS, "What causes %s?", "Which disorder is caused by %s?")
    return [
        SU(BIO, 24, "the-living-world", 1,
           "Biodiversity; need for classification; three domains of life; taxonomy and systematics; concept of species and taxonomical hierarchy; binomial nomenclature; tools for study of taxonomy – museums, zoological parks, herbaria, botanical gardens.",
           "The Living World", "the living world",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 1 The Living World: features of living things, taxonomic categories, binomial nomenclature and taxonomic aids. 100 questions with answers.",
           "Metabolism and cellular organisation define life.", "Kingdom → phylum → class → order → family → genus → species.",
           "<p>Growth and reproduction are not defining features of life, because crystals grow and mules cannot reproduce; metabolism, cellular organisation and consciousness are. Taxonomy identifies, names and classifies organisms into a hierarchy of categories from kingdom down to species.</p>"
           "<p>Binomial nomenclature (Linnaeus) gives each organism a genus name and a specific epithet, printed in italics: <i>Mangifera indica</i>. Herbaria, botanical gardens, museums, zoological parks and keys are taxonomic aids.</p>",
           [("<i>Panthera leo</i>: genus?", ["first word"], "Panthera"), ("Category above family?", ["order"], "order")],
           ["Capitalising the species epithet.", "Saying growth defines life.", "Mixing up order and class."],
           [("Why is metabolism a defining feature of life?", "Every living thing carries out chemical reactions in its cells, and no non-living thing does."),
            ("What is binomial nomenclature?", "Naming each species with two words, a genus name and a specific epithet, as Linnaeus proposed.")],
           lambda: [("Features of living things", [(od["1"], 14), (b[1], 6)]), ("Taxonomic categories", [(T(BI.m_taxa), 8), (od["1"], 10), (b[1], 2)]),
                    ("Binomial nomenclature", [(p1, 16), (b[1], 2), (od["1"], 2)]), ("Taxonomic aids", [(p1b, 12), (od["1"], 8)]), ("Mixed questions", [(od["1"], 12), (p1, 6), (b[1], 2)])]),
        SU(BIO, 25, "biological-classification", 2,
           "Five kingdom classification; salient features and classification of Monera, Protista and Fungi into major groups; lichens; viruses and viroids.",
           "Biological Classification", "biological classification",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 2 Biological Classification: the five kingdoms, bacteria, protists, fungi, lichens, viruses, viroids and diseases they cause. 100 questions with answers.",
           "Five kingdoms: Monera, Protista, Fungi, Plantae, Animalia.", "Viruses are not truly living outside a host cell.",
           "<p>Whittaker's five kingdoms are based on cell structure, body organisation, mode of nutrition and reproduction. Monera are prokaryotes (bacteria, cyanobacteria, archaebacteria, mycoplasma). Protista are unicellular eukaryotes such as diatoms, dinoflagellates, Euglena and protozoans.</p>"
           "<p>Fungi are heterotrophs with chitin walls, grouped into phycomycetes, ascomycetes, basidiomycetes and deuteromycetes. Lichens are alga + fungus. Viruses are nucleoprotein particles that multiply only in host cells; viroids are bare RNA and prions are misfolded proteins.</p>",
           [("Penicillium: which class?", ["sac fungi"], "Ascomycetes"), ("Malaria is caused by?", ["a protozoan"], "Plasmodium")],
           ["Putting viruses in Monera.", "Calling fungi plants.", "Confusing viroids (RNA) with prions (protein)."],
           [("Why are viruses not placed in any kingdom?", "They are not cells and cannot reproduce or show metabolism outside a host cell."),
            ("What is a lichen?", "A close partnership of an alga, which makes food, and a fungus, which gives shelter and absorbs water.")],
           lambda: [("The five kingdoms", [(p2, 7), (b[2], 6), (od["2"], 7)]), ("Monera and Protista", [(od["2"], 16), (b[2], 4)]), ("Fungi", [(p2b, 6), (od["2"], 14)]),
                    ("Viruses and diseases", [(od["2"], 18), (b[2], 2)]), ("Mixed questions", [(od["2"], 20)])]),
        SU(BIO, 26, "plant-kingdom", 3,
           "Classification of plants into major groups; salient and distinguishing features and a few examples of algae, bryophytes, pteridophytes and gymnosperms.",
           "Plant Kingdom", "plant kingdom",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 3 Plant Kingdom: algae, bryophytes, pteridophytes, gymnosperms and angiosperms, their features, examples and life cycles. 100 questions with answers.",
           "Algae → bryophytes → pteridophytes → gymnosperms → angiosperms.", "Bryophytes: gametophyte dominant; pteridophytes onwards: sporophyte dominant.",
           "<p>Algae are simple, mostly aquatic plants: green (Chlorophyceae), brown (Phaeophyceae) and red (Rhodophyceae). Bryophytes (mosses, liverworts) are the amphibians of plants with a dominant gametophyte. Pteridophytes (ferns, horsetails) are the first plants with xylem and phloem and a dominant sporophyte.</p>"
           "<p>Gymnosperms (Pinus, Cycas) bear naked seeds; angiosperms bear seeds inside fruits and show double fertilisation, forming a triploid endosperm. Heterospory in Selaginella was a step towards the seed habit.</p>",
           [("Funaria is a?", ["moss"], "bryophyte"), ("Endosperm ploidy in angiosperms?", ["two polar nuclei + one male gamete"], "3n")],
           ["Calling the fern plant a gametophyte.", "Saying gymnosperms have fruits.", "Mixing up brown and red algae pigments."],
           [("Why are bryophytes called the amphibians of the plant kingdom?", "They live on land but need water for their sperm to swim to the egg."),
            ("What is double fertilisation?", "In angiosperms one male gamete fuses with the egg and the other with the two polar nuclei, forming the zygote and the triploid endosperm.")],
           lambda: [("Algae", [(od["3"], 14), (p3, 2), (b[3], 4)]), ("Bryophytes and pteridophytes", [(od["3"], 14), (b[3], 4), (p3b, 2)]), ("Gymnosperms and angiosperms", [(p3b, 4), (b[3], 4), (od["3"], 12)]),
                    ("Life cycles", [(od["3"], 20)]), ("Mixed questions", [(od["3"], 20)])]),
        SU(BIO, 27, "animal-kingdom", 4,
           "Salient features and classification of animals, non-chordates up to phyla level and chordates up to class level (salient features and at least two examples of each category).",
           "Animal Kingdom", "animal kingdom",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 4 Animal Kingdom: levels of organisation, symmetry, coelom, the non-chordate phyla and the classes of vertebrates with examples. 100 questions with answers.",
           "Animals are grouped by organisation, symmetry, germ layers and coelom.", "Chordates have a notochord, a dorsal nerve cord and gill slits.",
           "<p>Animals are classified by level of organisation (cellular, tissue, organ), symmetry (radial or bilateral), germ layers (diploblastic or triploblastic), body cavity (acoelomate, pseudocoelomate, coelomate) and segmentation. Non-chordate phyla run from Porifera to Hemichordata; Arthropoda is the largest.</p>"
           "<p>Chordates have a notochord, a dorsal hollow nerve cord and pharyngeal gill slits. Vertebrate classes include cartilaginous and bony fishes, amphibians, reptiles, birds and mammals.</p>",
           [("Earthworm phylum?", ["segmented"], "Annelida"), ("Shark class?", ["cartilage skeleton"], "Chondrichthyes")],
           ["Calling a starfish a fish.", "Calling Ascaris an annelid.", "Saying all reptiles have three-chambered hearts (crocodiles have four)."],
           [("What is the largest animal phylum?", "Arthropoda, with about two-thirds of all named species."),
            ("What are the three basic features of chordates?", "A notochord, a dorsal hollow nerve cord and paired pharyngeal gill slits.")],
           lambda: [("Basis of classification", [(b[4], 8), (p4, 6), (od["4"], 6)]), ("Non-chordates", [(od["4"], 16), (p4, 4)]), ("Non-chordate features", [(p4, 4), (b[4], 4), (od["4"], 12)]),
                    ("Chordates", [(od["4b"], 20)]), ("Mixed questions", [(od["4"], 6), (od["4b"], 14)])]),
        SU(BIO, 28, "morphology-of-flowering-plants", 5,
           "Morphology of different parts of flowering plants: root, stem, leaf, inflorescence, flower, fruit and seed. Description of family Solanaceae.",
           "Morphology of Flowering Plants", "morphology of flowering plants",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 5 Morphology of Flowering Plants: roots, stems and leaves and their modifications, inflorescence, flowers, aestivation, placentation, fruits, seeds and families. 100 questions with answers.",
           "Root, stem and leaf can all be modified.", "Aestivation is how petals are arranged in a bud; placentation is how ovules are arranged in an ovary.",
           "<p>Dicots usually have tap roots and reticulate venation; monocots have fibrous roots and parallel venation. Roots, stems and leaves are modified for storage, support, climbing and protection: carrots are roots, potatoes are stems and pea tendrils are leaves.</p>"
           "<p>A flower is described by its symmetry, ovary position (hypogynous, perigynous, epigynous), aestivation (valvate, twisted, imbricate, vexillary) and placentation. Families such as Fabaceae, Solanaceae and Liliaceae are known by their floral features.</p>",
           [("Potato is a modified?", ["it has eyes (nodes)"], "stem"), ("Placentation in pea?", ["one-chambered ovary"], "marginal")],
           ["Calling potato a root.", "Mixing up twisted and imbricate aestivation.", "Calling a coconut's water the fruit wall."],
           [("How can we tell that a potato is a stem?", "It has nodes (eyes) with buds that grow into new shoots."),
            ("What is placentation?", "The arrangement of ovules inside the ovary, such as marginal, axile, parietal, basal or free central.")],
           lambda: [("Roots, stems and leaves", [(b[5], 6), (od["5"], 14)]), ("Modifications", [(od["5"], 18), (b[5], 2)]), ("Flowers and aestivation", [(p5b, 10), (b[5], 4), (od["5"], 6)]),
                    ("Families", [(p5, 1), (p5b, 4), (od["5"], 15)]), ("Mixed questions", [(od["5"], 20)])]),
        SU(BIO, 29, "anatomy-of-flowering-plants", 6,
           "Anatomy and functions of tissue systems in dicots and monocots.",
           "Anatomy of Flowering Plants", "anatomy of flowering plants",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 6 Anatomy of Flowering Plants: meristems, simple and complex tissues, tissue systems, dicot and monocot roots, stems and leaves, and secondary growth. 100 questions with answers.",
           "Meristems divide; permanent tissues do not.", "Dicot stems have a ring of open bundles; monocot stems have scattered closed bundles.",
           "<p>Meristems (apical, intercalary and lateral) make new cells. Permanent tissues are simple (parenchyma, collenchyma, sclerenchyma) or complex (xylem and phloem). There are three tissue systems: epidermal, ground and vascular.</p>"
           "<p>In dicot stems the vascular bundles are in a ring and have cambium, so they grow in girth (secondary growth), making annual rings and bark. Monocot stems have scattered bundles with no cambium. Roots have radial bundles and an endodermis with Casparian strips.</p>",
           [("Xylem in a root: protoxylem where?", ["outside"], "exarch"), ("Monocot stem bundles?", ["no cambium"], "scattered, closed")],
           ["Calling sclerenchyma living.", "Saying monocots have secondary growth.", "Mixing up heartwood and sapwood."],
           [("Why do dicot stems grow thicker but monocot stems usually do not?", "Dicot vascular bundles have a cambium that adds secondary xylem and phloem; monocot bundles are closed."),
            ("What are annual rings?", "Rings of spring wood and autumn wood laid down each year by the cambium; counting them gives a tree's age.")],
           lambda: [("Meristems and simple tissues", [(od["6"], 12), (p6b, 4), (b[6], 4)]), ("Complex tissues", [(od["6"], 10), (p6b, 8), (b[6], 2)]), ("Roots, stems and leaves", [(p6, 6), (b[6], 4), (od["6"], 4), (p6b, 6)]),
                    ("Secondary growth", [(b[6], 2), (p6b, 6), (od["6"], 12)]), ("Mixed questions", [(od["6"], 16), (p6b, 4)])]),
        SU(BIO, 30, "structural-organisation-in-animals", 7,
           "Animal tissues; morphology, anatomy and functions of different systems (digestive, circulatory, respiratory, nervous and reproductive) of an insect (cockroach) and frog (brief account only).",
           "Structural Organisation in Animals", "structural organisation in animals",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 7 Structural Organisation in Animals: epithelial, connective, muscular and neural tissues, cell junctions, and the frog. 100 questions with answers.",
           "Four animal tissues: epithelial, connective, muscular, neural.", "Structure suits function in every tissue.",
           "<p>Epithelia cover surfaces and line cavities: squamous, cuboidal, columnar, ciliated and compound. Connective tissues (areolar, adipose, tendon, ligament, cartilage, bone, blood) support and link other tissues. Muscle may be skeletal, smooth or cardiac, and neural tissue carries impulses. Cells are linked by tight, adhering and gap junctions.</p>"
           "<p>The frog (<i>Rana tigrina</i>) is cold-blooded, breathes through its skin in water, has a three-chambered heart, excretes urea and has external fertilisation with a tadpole stage.</p>",
           [("Tissue lining air sacs?", ["thin, flat"], "squamous epithelium"), ("Frog heart chambers?", ["2 atria, 1 ventricle"], "3")],
           ["Calling blood an epithelium.", "Mixing up tendons and ligaments.", "Saying the frog has a four-chambered heart."],
           [("What is the difference between a tendon and a ligament?", "A tendon joins muscle to bone; a ligament joins bone to bone."),
            ("How does a frog breathe in water?", "Through its moist skin, which is richly supplied with blood vessels.")],
           lambda: [("Epithelial tissue", [(od["7"], 10), (p7, 6), (b[7], 4)]), ("Connective tissue", [(od["7"], 10), (p7, 6), (b[7], 4)]), ("Muscle and neural tissue", [(od["7"], 12), (p7, 4), (b[7], 4)]),
                    ("The frog", [(od["7"], 20)]), ("Mixed questions", [(od["7"], 16), (p7, 4)])]),
        SU(BIO, 31, "cell-the-unit-of-life", 8,
           "Cell theory and cell as the basic unit of life; structure of prokaryotic and eukaryotic cells; plant cell and animal cell; cell envelope, cell membrane, cell wall; cell organelles – structure and function; endomembrane system, endoplasmic reticulum, Golgi bodies, lysosomes, vacuoles; mitochondria, ribosomes, plastids, microbodies; cytoskeleton, cilia, flagella, centrioles; nucleus.",
           "Cell: The Unit of Life", "the cell",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 8 Cell: The Unit of Life: cell theory, prokaryotic and eukaryotic cells, the plasma membrane, cell organelles and their functions, and the nucleus. 100 questions with answers.",
           "All living things are made of cells; cells come from cells.", "Each organelle has a job: mitochondria respire, ribosomes make proteins.",
           "<p>The cell theory (Schleiden, Schwann, Virchow) says all organisms are made of cells and new cells come from existing cells. Prokaryotic cells (bacteria) have no nuclear membrane and 70S ribosomes; eukaryotic cells have a nucleus and membrane-bound organelles. The plasma membrane is a fluid mosaic of lipids and proteins.</p>"
           "<p>The endomembrane system (ER, Golgi, lysosomes, vacuoles) makes, packs and digests materials. Mitochondria and chloroplasts have their own DNA. Ribosomes, centrioles and the cytoskeleton have no membrane.</p>",
           [("Organelle for protein synthesis?", ["rRNA + protein"], "ribosome"), ("Prokaryote ribosomes?", ["smaller"], "70S")],
           ["Saying ribosomes have a membrane.", "Saying animal cells have cell walls.", "Mixing up cristae and grana."],
           [("Why are mitochondria called the powerhouse of the cell?", "They carry out aerobic respiration and make most of the cell's ATP."),
            ("What is the fluid mosaic model?", "The plasma membrane is a fluid lipid bilayer with proteins floating in it, as Singer and Nicolson proposed.")],
           lambda: [("Cell theory and cell types", [(b[8], 8), (od["8"], 8), (T(BI.m_mag), 4)]), ("Membranes and organelles", [(od["8"], 12), (p8, 8)]), ("Functions of organelles", [(p8, 12), (b[8], 4), (T(BI.m_mag), 4)]),
                    ("Measuring cells", [(T(BI.m_mag), 20)]), ("Mixed questions", [(od["8"], 10), (T(BI.m_mag), 10)])]),
        SU(BIO, 32, "biomolecules", 9,
           "Chemical constituents of living cells: biomolecules – structure and function of proteins, carbohydrates, lipids and nucleic acids; enzymes – types, properties, enzyme action.",
           "Biomolecules", "biomolecules",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 9 Biomolecules: carbohydrates, proteins, lipids, nucleic acids, the bonds that join them, and enzymes, their classes and action. 100 questions with answers.",
           "Macromolecules are polymers of small units.", "Enzymes lower the activation energy.",
           "<p>Living cells contain small molecules (sugars, amino acids, nucleotides, fatty acids) and macromolecules (polysaccharides, proteins, nucleic acids; lipids also come in the acid-insoluble fraction). Monomers join by glycosidic, peptide and phosphodiester bonds, each made by losing water.</p>"
           "<p>Enzymes are mostly proteins that lower activation energy by forming an enzyme–substrate complex. They work best at an optimum temperature and pH and are classified into six classes. Cofactors may be prosthetic groups, coenzymes or metal ions.</p>",
           [("Bond in proteins?", ["between amino acids"], "peptide bond"), ("Enzyme class that adds water to split bonds?", ["hydrolysis"], "hydrolases")],
           ["Calling lipids polymers in the strict sense.", "Saying enzymes change ΔG.", "Confusing nucleosides and nucleotides."],
           [("Why do enzymes speed up reactions?", "They provide a different path with a lower activation energy, so more molecules can react."),
            ("Which bonds join the monomers of macromolecules?", "Glycosidic bonds in polysaccharides, peptide bonds in proteins and phosphodiester bonds in nucleic acids.")],
           lambda: [("Carbohydrates and lipids", [(od["9"], 12), (b[9], 6), (T(BI.m_cond), 2)]), ("Proteins", [(T(BI.m_cond), 10), (od["9"], 6), (b[9], 4)]), ("Nucleic acids", [(od["9"], 8), (T(BI.m_chargaff), 10), (b[9], 2)]),
                    ("Enzymes", [(p9, 8), (p9b, 2), (T(BI.m_rate), 10)]), ("Mixed questions", [(od["9"], 14), (T(BI.m_cond), 6)])]),
        SU(BIO, 33, "cell-cycle-and-cell-division", 10,
           "Cell cycle, mitosis, meiosis and their significance.",
           "Cell Cycle and Cell Division", "cell cycle and cell division",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 10 Cell Cycle and Cell Division: interphase, the stages of mitosis, cytokinesis, meiosis I and II, crossing over and chromosome numbers. 100 questions with answers.",
           "Interphase (G₁, S, G₂) → M phase.", "Mitosis keeps the chromosome number; meiosis halves it.",
           "<p>The cell cycle has interphase (G₁ growth, S DNA replication, G₂ preparation) and the M phase (mitosis and cytokinesis). Mitosis has prophase, metaphase, anaphase and telophase; it gives two identical diploid cells for growth and repair.</p>"
           "<p>Meiosis has two divisions: meiosis I separates homologous chromosomes (reductional) after crossing over in pachytene; meiosis II separates sister chromatids. It forms four haploid cells and creates variation.</p>",
           [("Phase when DNA doubles?", ["synthesis"], "S phase"), ("2n = 46. Gamete?", ["halved"], "23")],
           ["Saying the chromosome number doubles in S phase.", "Putting crossing over in metaphase.", "Calling meiosis II reductional."],
           [("What is the difference between mitosis and meiosis?", "Mitosis gives two diploid cells identical to the parent; meiosis gives four haploid cells that differ genetically."),
            ("When does crossing over happen?", "In pachytene of prophase I, between non-sister chromatids of homologous chromosomes.")],
           lambda: [("The cell cycle", [(st, 6), (b[10], 6), (od["10"], 8)]), ("Mitosis", [(st, 6), (b[10], 4), (T(BI.m_mitotic), 10)]), ("Meiosis", [(mei, 10), (b[10], 2), (od["10"], 8)]),
                    ("Chromosome numbers", [(T(BI.m_meiosis), 14), (T(BI.m_mitotic), 6)]), ("Mixed questions", [(od["10"], 12), (T(BI.m_meiosis), 8)])]),
        SU(BIO, 34, "photosynthesis-in-higher-plants", 11,
           "Photosynthesis as a means of autotrophic nutrition; site of photosynthesis, pigments involved in photosynthesis (elementary idea); photochemical and biosynthetic phases of photosynthesis; cyclic and non-cyclic photophosphorylation; chemiosmotic hypothesis; photorespiration; C₃ and C₄ pathways; factors affecting photosynthesis.",
           "Photosynthesis in Higher Plants", "photosynthesis",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 11 Photosynthesis in Higher Plants: early experiments, pigments, light reactions, photosystems, the Calvin cycle, C₄ plants, photorespiration and limiting factors. 100 questions with answers.",
           "Light reactions make ATP, NADPH and O₂; the Calvin cycle uses them to fix CO₂.", "C₄ plants avoid photorespiration.",
           "<p>Photosynthesis happens in chloroplasts. In the light reactions on the thylakoids, PS II and PS I absorb light, water is split (giving O₂), and ATP and NADPH are made by non-cyclic photophosphorylation; ATP forms by chemiosmosis.</p>"
           "<p>The Calvin cycle in the stroma fixes CO₂ onto RuBP with RuBisCO; the first product is 3-PGA, and each CO₂ needs 3 ATP and 2 NADPH. C₄ plants such as maize first fix CO₂ into oxaloacetate with PEP carboxylase and have Kranz anatomy, so they waste little energy on photorespiration.</p>",
           [("First product of C₃ cycle?", ["3 carbons"], "PGA"), ("ATP per CO₂ fixed?", ["3 ATP + 2 NADPH"], "3")],
           ["Saying the oxygen comes from CO₂.", "Putting the Calvin cycle in the thylakoids.", "Calling wheat a C₄ plant."],
           [("Where does the oxygen released in photosynthesis come from?", "From the splitting of water (photolysis) in PS II."),
            ("Why are C₄ plants more efficient in hot, bright places?", "They concentrate CO₂ around RuBisCO in bundle-sheath cells, so photorespiration hardly happens.")],
           lambda: [("Early experiments and pigments", [(b[11], 8), (T(BI.m_energy, "rf"), 8), (p11, 4)]), ("Light reactions", [(p11, 4), (od["11"], 12), (b[11], 4)]), ("The Calvin cycle", [(od["11"], 16), (p11, 4)]),
                    ("C₄ plants and photorespiration", [(od["11"], 20)]), ("Mixed questions", [(od["11"], 14), (T(BI.m_energy, "rf"), 6)])]),
        SU(BIO, 35, "respiration-in-plants", 12,
           "Exchange of gases; cellular respiration – glycolysis, fermentation (anaerobic), TCA cycle and electron transport system (aerobic); energy relations – number of ATP molecules generated; amphibolic pathways; respiratory quotient.",
           "Respiration in Plants", "respiration in plants",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 12 Respiration in Plants: glycolysis, fermentation, the Krebs cycle, the electron transport system, ATP yield, amphibolic pathways and respiratory quotient. 100 questions with answers.",
           "Glycolysis → link reaction → Krebs cycle → ETS.", "RQ = CO₂ given out ÷ O₂ taken in.",
           "<p>Glycolysis in the cytoplasm splits glucose into two pyruvic acid, with a net gain of 2 ATP and 2 NADH. Without oxygen, pyruvic acid becomes ethanol and CO₂ (yeast) or lactic acid (muscle). With oxygen it is oxidised to acetyl CoA, which enters the Krebs cycle in the mitochondrial matrix.</p>"
           "<p>NADH and FADH₂ pass electrons along the electron transport system on the inner mitochondrial membrane to oxygen, and ATP synthase makes ATP (about 38 per glucose in theory). Respiration is amphibolic. The respiratory quotient is 1.0 for carbohydrates and about 0.7 for fats.</p>",
           [("Net ATP from glycolysis?", ["4 made, 2 used"], "2"), ("RQ of glucose?", ["6 CO₂ ÷ 6 O₂"], "1")],
           ["Putting glycolysis in the mitochondria.", "Saying fermentation makes as much ATP as aerobic respiration.", "Inverting the RQ fraction."],
           [("What is the respiratory quotient?", "The ratio of the volume of CO₂ given out to the volume of O₂ used in respiration."),
            ("Why is respiration called amphibolic?", "Its pathway is used both to break down food (catabolism) and to supply intermediates for making fats and proteins (anabolism).")],
           lambda: [("Glycolysis and fermentation", [(b[12], 6), (od["12"], 6), (p12, 2), (K(atp, "pyr", "gly"), 6)]), ("The Krebs cycle", [(od["12"], 10), (b[12], 4), (K(atp, "co2", "turns"), 6)]),
                    ("The electron transport system", [(K(atp, "ets", "aer"), 14), (od["12"], 6)]), ("Respiratory quotient", [(T(BI.m_energy, "rq"), 20)]), ("Mixed questions", [(T(BI.m_energy, "rq"), 10), (od["12"], 6), (K(atp, "pyr", "gly", "aer", "co2", "turns", "ets"), 4)])]),
        SU(BIO, 36, "plant-growth-and-development", 13,
           "Seed germination; phases of plant growth and plant growth rate; conditions of growth; differentiation, dedifferentiation and redifferentiation; sequence of developmental processes in a plant cell; plant growth regulators – auxin, gibberellin, cytokinin, ethylene, ABA.",
           "Plant Growth and Development", "plant growth and development",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 13 Plant Growth and Development: growth phases and curves, differentiation, the five plant hormones and their uses, photoperiodism and vernalisation. 100 questions with answers.",
           "Five plant growth regulators: auxin, gibberellin, cytokinin, ethylene, ABA.", "Growth follows a sigmoid curve.",
           "<p>Plant growth is indeterminate and happens at meristems. Growth may be arithmetic or geometric and usually follows an S-shaped (sigmoid) curve with lag, log and stationary phases. Cells differentiate, can dedifferentiate to divide again, and then redifferentiate.</p>"
           "<p>Growth regulators control development: auxins (apical dominance, rooting), gibberellins (stem elongation, bolting), cytokinins (cell division, delaying senescence), ethylene (ripening) and abscisic acid (dormancy, closing stomata). Photoperiodism and vernalisation control flowering.</p>",
           [("Hormone for fruit ripening?", ["a gas"], "ethylene"), ("Cabbage bolting?", ["stem elongation"], "gibberellin")],
           ["Calling ABA a growth promoter.", "Saying photoperiod is sensed by the flower.", "Mixing up auxin and cytokinin."],
           [("What is apical dominance?", "The growing shoot tip, through auxin, stops the lateral buds below it from growing."),
            ("What is vernalisation?", "Promoting flowering by exposing plants to a period of low temperature.")],
           lambda: [("Growth and its phases", [(b[13], 6), (od["13b"], 14)]), ("Plant hormones", [(p13, 6), (b[13], 4), (od["13b"], 10)]), ("Uses of plant hormones", [(p13b, 6), (od["13b"], 14)]),
                    ("Photoperiodism and vernalisation", [(od["13"], 18), (b[13], 2)]), ("Mixed questions", [(od["13"], 10), (od["13b"], 10)])]),
        SU(BIO, 37, "breathing-and-exchange-of-gases", 14,
           "Respiratory organs in animals (recall only); respiratory system in humans; mechanism of breathing and its regulation in humans – exchange of gases, transport of gases and regulation of respiration, respiratory volume; disorders related to respiration – asthma, emphysema, occupational respiratory disorders.",
           "Breathing and Exchange of Gases", "breathing and exchange of gases",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 14 Breathing and Exchange of Gases: the human respiratory system, mechanism of breathing, lung volumes and capacities, gas exchange, transport of gases and disorders. 100 questions with answers.",
           "Vital capacity = ERV + TV + IRV.", "Most CO₂ travels as bicarbonate; most O₂ as oxyhaemoglobin.",
           "<p>Air passes through the nose, pharynx, larynx, trachea, bronchi and bronchioles to the alveoli. Breathing in, the diaphragm and external intercostal muscles contract and the lung volume rises. Lung volumes are measured with a spirometer: TV ≈ 500 mL, IRV ≈ 2500–3000 mL, ERV ≈ 1000–1100 mL and RV ≈ 1100–1200 mL.</p>"
           "<p>Gases diffuse by partial pressure difference across the thin alveolar wall. About 97% of O₂ is carried as oxyhaemoglobin; CO₂ is carried mostly as bicarbonate. The medulla sets the breathing rhythm.</p>",
           [("TV 500, IRV 2500, ERV 1000. VC?", ["ERV + TV + IRV"], "4000 mL"), ("12 breaths × 500 mL?", ["rate × TV"], "6000 mL per minute")],
           ["Adding RV to vital capacity.", "Saying most CO₂ is carried by haemoglobin.", "Saying the diaphragm relaxes during inspiration."],
           [("What is vital capacity?", "The largest volume of air a person can breathe out after the deepest breath in: ERV + TV + IRV."),
            ("How is carbon dioxide carried in the blood?", "About 70% as bicarbonate, 20–25% as carbaminohaemoglobin and about 7% dissolved in plasma.")],
           lambda: [("The respiratory system", [(b[14], 8), (od["14"], 12)]), ("Lung volumes", [(K(lungvol, "vc", "ic", "ec"), 20)]), ("Lung capacities", [(K(lungvol, "frc", "tlc", "mv"), 16), (b[14], 4)]),
                    ("Exchange and transport of gases", [(od["14"], 18), (K(lungvol, "mv"), 2)]), ("Mixed questions", [(K(lungvol, "vc", "ic", "ec", "frc", "tlc", "mv"), 20)])]),
        SU(BIO, 38, "body-fluids-and-circulation", 15,
           "Composition of blood, blood groups, coagulation of blood; composition of lymph and its function; human circulatory system – structure of human heart and blood vessels; cardiac cycle, cardiac output, ECG; double circulation; regulation of cardiac activity; disorders of circulatory system – hypertension, coronary artery disease, angina pectoris, heart failure.",
           "Body Fluids and Circulation", "body fluids and circulation",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 15 Body Fluids and Circulation: blood cells, plasma, blood groups, clotting, lymph, the heart, cardiac cycle, cardiac output, ECG, double circulation and disorders. 100 questions with answers.",
           "Cardiac output = heart rate × stroke volume.", "Blood flows twice through the heart in one circuit.",
           "<p>Blood is plasma (55%) with red cells, white cells and platelets. ABO groups depend on antigens A and B on red cells; Rh mismatch can cause erythroblastosis foetalis. Clotting needs platelets, Ca²⁺ and fibrinogen turning into fibrin.</p>"
           "<p>The human heart has four chambers; the SA node starts each beat, passed on by the AV node and bundle of His. At rest the heart beats about 72 times a minute with a stroke volume of about 70 mL, so cardiac output is about 5 L/min. The ECG shows P (atria), QRS (ventricles) and T waves.</p>",
           [("72 beats × 70 mL?", ["HR × SV"], "5040 mL/min"), ("Universal recipient?", ["no antibodies"], "AB")],
           ["Calling AB the universal donor.", "Thinking the P-wave is ventricular.", "Mixing up the SA and AV nodes."],
           [("What is cardiac output?", "The volume of blood each ventricle pumps per minute: heart rate × stroke volume, about 5 litres at rest."),
            ("Why is group O a universal donor?", "Its red cells carry no A or B antigens, so they are not clumped by anti-A or anti-B antibodies.")],
           lambda: [("Blood and its cells", [(od["15"], 8), (p15, 8), (b[15], 4)]), ("Blood groups", [(bl, 6), (bl2, 6), (b[15], 4), (T(BI.m_cardiac), 4)]), ("The heart and its conduction", [(p15, 8), (b[15], 4), (T(BI.m_cardiac), 8)]),
                    ("Cardiac cycle and output", [(T(BI.m_cardiac), 20)]), ("Mixed questions", [(od["15"], 4), (T(BI.m_cardiac), 16)])]),
        SU(BIO, 39, "excretory-products-and-their-elimination", 16,
           "Modes of excretion – ammonotelism, ureotelism, uricotelism; human excretory system – structure and function; urine formation, osmoregulation; regulation of kidney function – renin–angiotensin, atrial natriuretic factor, ADH and diabetes insipidus; role of other organs in excretion; disorders – uraemia, renal failure, renal calculi, nephritis; dialysis and artificial kidney, kidney transplant.",
           "Excretory Products and their Elimination", "excretion",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 16 Excretory Products and their Elimination: ammonotelic, ureotelic and uricotelic animals, the nephron, urine formation, the counter-current mechanism, hormones and kidney disorders. 100 questions with answers.",
           "Filtration → reabsorption → secretion in the nephron.", "ADH, aldosterone and ANF regulate the kidney.",
           "<p>Animals excrete ammonia (aquatic animals), urea (mammals, adult frogs) or uric acid (birds, reptiles, insects). The human kidney has about a million nephrons. Blood is filtered in the glomerulus (about 180 L of filtrate a day, GFR 125 mL/min), and the tubules reabsorb most of it, leaving about 1.5 L of urine.</p>"
           "<p>The counter-current mechanism of the loop of Henle and vasa recta keeps the medulla salty so concentrated urine can form. ADH increases water reabsorption; the renin–angiotensin–aldosterone system raises blood pressure; ANF lowers it.</p>",
           [("Birds excrete mainly?", ["least water"], "uric acid"), ("Hormone that saves water?", ["vasopressin"], "ADH")],
           ["Saying urea is made in the kidney.", "Saying the ascending limb lets water out.", "Calling humans uricotelic."],
           [("Why do birds excrete uric acid?", "It is insoluble and not very toxic, so it can be removed with very little water."),
            ("What does ADH do?", "It makes the DCT and collecting duct more permeable to water, so more water is reabsorbed and urine is concentrated.")],
           lambda: [("Modes of excretion", [(od["16"], 14), (b[16], 6)]), ("The nephron", [(p16, 10), (od["16b"], 6), (b[16], 4)]), ("Urine formation", [(K(gfr, "day", "urine", "pct", "hour"), 14), (b[16], 2), (p16, 4)]),
                    ("Regulation and disorders", [(od["16b"], 12), (od["16"], 8)]), ("Mixed questions", [(K(gfr, "day", "urine", "pct", "hour"), 12), (od["16b"], 6), (od["16"], 2)])]),
        SU(BIO, 40, "locomotion-and-movement", 17,
           "Types of movement – amoeboid, ciliary, flagellar, muscular; skeletal muscle, contractile proteins and muscle contraction; skeletal system and its functions; joints; disorders of muscular and skeletal system – myasthenia gravis, tetany, muscular dystrophy, arthritis, osteoporosis, gout.",
           "Locomotion and Movement", "locomotion and movement",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 17 Locomotion and Movement: types of movement, the sarcomere, sliding filament theory, the human skeleton, joints and disorders of muscles and bones. 100 questions with answers.",
           "Thin (actin) filaments slide over thick (myosin) filaments.", "206 bones: 80 axial and 126 appendicular.",
           "<p>Cells move by amoeboid, ciliary, flagellar or muscular movement. A skeletal muscle fibre has myofibrils made of sarcomeres with thin actin and thick myosin filaments. A nerve impulse releases Ca²⁺, which binds troponin; myosin heads then pull actin inwards using ATP, shortening the sarcomere.</p>"
           "<p>The adult skeleton has 206 bones: the axial skeleton (skull, vertebral column, sternum, ribs) and the appendicular skeleton (limbs and girdles). Joints may be fibrous, cartilaginous or synovial (ball and socket, hinge, pivot, gliding, saddle).</p>",
           [("Joint in the knee?", ["moves one way"], "hinge"), ("Ion that starts contraction?", ["binds troponin"], "Ca²⁺")],
           ["Saying the A-band shortens.", "Calling the femur part of the axial skeleton.", "Mixing up gout and osteoporosis."],
           [("What is the sliding filament theory?", "Muscles contract as the thin actin filaments slide over the thick myosin filaments, shortening each sarcomere."),
            ("How many bones are in the human skeleton?", "206 in an adult: 80 in the axial skeleton and 126 in the appendicular skeleton.")],
           lambda: [("Types of movement and muscle", [(b[17], 8), (p17b, 4), (od["17"], 8)]), ("Muscle contraction", [(b[17], 4), (od["17"], 16)]), ("The skeleton", [(od["17"], 20)]),
                    ("Joints", [(p17, 10), (od["17"], 10)]), ("Disorders and mixed questions", [(p17b, 5), (od["17"], 15)])]),
        SU(BIO, 41, "neural-control-and-coordination", 18,
           "Neuron and nerves; nervous system in humans – central, peripheral and visceral nervous system; generation and conduction of nerve impulse; reflex action; sensory perception; sense organs; elementary structure and functions of eye and ear.",
           "Neural Control and Coordination", "neural control and coordination",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 18 Neural Control and Coordination: neurons, resting and action potentials, synapses, the brain, reflex action, the eye and the ear. 100 questions with answers.",
           "Resting potential −70 mV; Na⁺ in during an impulse.", "Each part of the brain has its own job.",
           "<p>A neuron has dendrites, a cell body and an axon. At rest the inside is about −70 mV, kept by the Na⁺/K⁺ pump. A stimulus opens Na⁺ channels (depolarisation), then K⁺ leaves (repolarisation); in myelinated fibres the impulse jumps between nodes of Ranvier. At a synapse a neurotransmitter such as acetylcholine crosses the cleft.</p>"
           "<p>The brain has the forebrain (cerebrum, thalamus, hypothalamus), midbrain and hindbrain (pons, cerebellum, medulla). Reflexes are fast automatic responses through the spinal cord. The eye has rods and cones in the retina; the ear's cochlea is for hearing and the semicircular canals for balance.</p>",
           [("Part of brain for balance?", ["hindbrain"], "cerebellum"), ("Ion entering during an impulse?", ["depolarisation"], "Na⁺")],
           ["Saying K⁺ enters during depolarisation.", "Calling the medulla the seat of thinking.", "Saying cones work best in dim light."],
           [("What is the resting potential?", "The voltage across a resting neuron's membrane, about −70 mV inside compared with outside."),
            ("What is a reflex action?", "A rapid, automatic response to a stimulus, usually through the spinal cord without the brain deciding.")],
           lambda: [("Neurons and impulses", [(b[18], 8), (T(BI.m_nerve, "speed", "freq"), 12)]), ("Synapses and reflexes", [(b[18], 4), (T(BI.m_nerve, "speed", "freq"), 8), (od["18"], 8)]), ("The brain", [(p18, 12), (od["18"], 8)]),
                    ("The eye and the ear", [(p18b, 10), (od["18"], 10)]), ("Mixed questions", [(od["18"], 12), (T(BI.m_nerve, "speed", "freq"), 8)])]),
        SU(BIO, 42, "chemical-coordination-and-integration", 19,
           "Endocrine glands and hormones; human endocrine system – hypothalamus, pituitary, pineal, thyroid, parathyroid, adrenal, pancreas, gonads; mechanism of hormone action (elementary idea); role of hormones as messengers and regulators; hypo- and hyperactivity and related disorders.",
           "Chemical Coordination and Integration", "chemical coordination",
           "Free CBSE Class 11 Biology worksheets for NCERT Chapter 19 Chemical Coordination and Integration: endocrine glands, the hormones they secrete, their roles, how hormones act, and disorders of too much or too little hormone. 100 questions with answers.",
           "Each endocrine gland releases hormones into the blood.", "Too much or too little hormone causes disease.",
           "<p>Endocrine glands are ductless and release hormones into the blood. The hypothalamus controls the pituitary, which controls the thyroid, adrenal cortex and gonads. The thyroid makes thyroxine (metabolic rate) and calcitonin; the parathyroids raise blood Ca²⁺; the pancreas makes insulin and glucagon; the adrenal medulla makes adrenaline.</p>"
           "<p>Protein hormones bind membrane receptors and use second messengers such as cAMP; steroid hormones enter the cell and act on genes. Lack of insulin causes diabetes mellitus, lack of iodine causes goitre, and too much growth hormone causes gigantism or acromegaly.</p>",
           [("Gland that makes insulin?", ["β-cells"], "pancreas"), ("Low iodine causes?", ["thyroid swells"], "goitre")],
           ["Calling insulin a steroid.", "Saying the posterior pituitary makes oxytocin itself.", "Mixing up gigantism and acromegaly."],
           [("Why is the pituitary called the master gland?", "Its hormones control several other endocrine glands, though it is itself controlled by the hypothalamus."),
            ("How do steroid hormones act?", "They pass through the cell membrane and bind receptors inside the cell, changing which genes are expressed.")],
           lambda: [("Endocrine glands", [(p19, 10), (b[19], 6), (od["19"], 4)]), ("Hormones and their roles", [(p19b, 14), (od["19"], 6)]), ("How hormones act", [(b[19], 5), (p19b, 6), (od["19"], 9)]),
                    ("Disorders", [(dis, 14), (od["19"], 6)]), ("Mixed questions", [(od["19"], 20)])]),
    ]


def K(f, *kinds):
    return lambda: f(ch(kinds))
