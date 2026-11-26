# -*- coding: utf-8 -*-
"""Class 9 Science, Unit II Organization in the Living World (NCERT chapters 5–6) and Unit IV Food; Food Production (chapter 12): question makers."""
from uk_alsci import tq, once_maker
from in_sci import pairs, _R, U, K


def ch(xs):
    return _R[0].choice(xs)


def odd_one(groups, q, qn=None, e=None):
    """'Which of these is <label>?' — one member of a group and three from the others; qn asks for the one that is not"""
    def f():
        R = _R[0]
        lab = R.choice(sorted(groups))
        others = sorted({x for k, v in groups.items() if k != lab for x in v})
        if qn and R.random() < 0.5 and len(groups[lab]) >= 3:
            a = R.choice(others)
            return tq(qn % lab, a, R.sample(groups[lab], 3), "%s is not %s; the others are." % (a[0].upper() + a[1:], lab))
        a = R.choice(groups[lab])
        return tq(q % lab, a, R.sample(others, 3), (e or "%s is %s.") % (a[0].upper() + a[1:], lab))
    return f


def c_osm2(k=None):
    R = _R[0]
    cell = R.choice(["an onion peel cell", "a red blood cell", "a root hair cell", "a potato cell", "a cheek cell", "a cell of a cucumber slice", "a leaf cell of Rhoeo"])
    c = R.choice([0.5, 0.8, 0.9, 1, 1.5, 2, 3, 4, 5])
    o = R.choice([0, 0.2, 0.5, 0.9, 1, 2, 3, 5, 8, 10, 15])
    if o == c:
        a, kind = "there is no net movement of water", "isotonic"
    elif o < c:
        a, kind = "water moves into the cell", "hypotonic"
    else:
        a, kind = "water moves out of the cell", "hypertonic"
    w = [x for x in ["water moves into the cell", "water moves out of the cell", "there is no net movement of water", "salt moves into the cell to balance it"] if x != a]
    sol = "pure water" if o == 0 else "a %s%% salt solution" % ("{:g}".format(o))
    return tq("The cell sap of %s is about %s%% salt. It is placed in %s. What happens by osmosis?" % (cell, "{:g}".format(c), sol), a, w,
              "The outside solution is %s (%s than the cell), so <b>%s</b>." % (kind, "the same concentration" if o == c else "more dilute" if o < c else "more concentrated", a))


CELLTYPE = {"a prokaryote": ["a bacterium", "blue-green algae (cyanobacteria)", "Mycoplasma", "E. coli", "Rhizobium"],
            "a eukaryote": ["Amoeba", "yeast", "an onion peel cell", "a human cheek cell", "Paramecium", "Euglena", "Chlamydomonas"]}
UNIMULTI = {"a unicellular organism": ["Amoeba", "Paramecium", "Chlamydomonas", "a bacterium", "Euglena", "yeast"],
            "a multicellular organism": ["a mushroom", "Hydra", "a frog", "a mango tree", "a human", "Spirogyra", "an earthworm"]}
PLANI = {"found in plant cells but not in animal cells": ["a cellulose cell wall", "chloroplasts", "a large central vacuole", "plastids"],
         "found in both plant and animal cells": ["the nucleus", "mitochondria", "ribosomes", "the plasma membrane", "the Golgi apparatus", "the endoplasmic reticulum", "cytoplasm"],
         "found in animal cells but usually not in plant cells": ["centrioles (centrosome)"]}


# =================================================================== Chapter 5: the fundamental unit of life
ORG = [("the nucleus", "controlling the activities of the cell and carrying the genes on chromosomes"), ("mitochondria", "releasing energy as ATP by cellular respiration"),
       ("chloroplasts", "photosynthesis, using the green pigment chlorophyll"), ("ribosomes", "making proteins"), ("the rough endoplasmic reticulum", "carrying ribosomes and helping to make proteins"),
       ("the smooth endoplasmic reticulum", "making fats (lipids) and helping to detoxify poisons and drugs"), ("the Golgi apparatus", "storing, modifying and packaging products into vesicles"),
       ("lysosomes", "digesting worn-out parts and foreign material; they are called the 'suicide bags' of the cell"), ("vacuoles", "storing water, food, waste and keeping the plant cell turgid"),
       ("the plasma membrane", "letting only some substances in and out (selectively permeable)"), ("the cell wall", "giving the plant cell strength and a fixed shape"),
       ("plastids", "storing starch, oils or pigments, or carrying out photosynthesis"), ("leucoplasts", "storing starch, oils and proteins (they are colourless)"),
       ("chromosomes", "carrying genetic information as DNA"), ("cytoplasm", "holding the organelles in a jelly-like fluid where many reactions take place"), ("the nucleolus", "helping to make ribosomes inside the nucleus"),
       ("the nuclear membrane", "separating the nucleus from the cytoplasm, with pores to let materials through"), ("centrosome", "helping in cell division in animal cells")]
OSM = [("a red blood cell placed in pure water (a hypotonic solution)", "it swells and may burst"), ("a red blood cell placed in a strong salt solution (a hypertonic solution)", "it shrinks"),
       ("a red blood cell placed in a solution of the same concentration (isotonic)", "it stays the same size"), ("a raisin placed in plain water", "it swells as water enters"),
       ("a plant cell placed in a concentrated sugar solution", "it loses water and the cytoplasm shrinks away from the wall (plasmolysis)"),
       ("a plant cell placed in pure water", "it becomes turgid but does not burst, because of the cell wall"), ("a de-shelled egg placed in pure water", "it swells as water enters"),
       ("a de-shelled egg placed in a concentrated salt solution", "it shrinks as water leaves"), ("a slice of raw potato placed in strong salt water", "it becomes soft and limp"),
       ("a cucumber slice sprinkled with salt", "water comes out of it"), ("a dried grape left in thick sugar syrup", "it stays shrunken")]
HIST = [("Robert Hooke", "discovered cells in a slice of cork in 1665"), ("Antonie van Leeuwenhoek", "first saw free-living cells in pond water with an improved microscope"),
        ("Robert Brown", "discovered the nucleus in 1831"), ("J. E. Purkinje", "coined the term 'protoplasm' in 1839"),
        ("Schleiden and Schwann", "proposed the cell theory: all plants and animals are made of cells"), ("Rudolf Virchow", "said that all cells arise from pre-existing cells")]
CELL = [("Who first saw cells?", "Robert Hooke, in a thin slice of cork", ["Charles Darwin", "Isaac Newton", "Gregor Mendel"], "He called them cells because they looked like small rooms."),
        ("What is the basic structural and functional unit of life?", "the cell", ["the tissue", "the organ", "the atom"], "All living things are made of cells."),
        ("Which organism is made of a single cell?", "Amoeba", ["a frog", "a mango tree", "a cow"], "Paramecium and bacteria are also unicellular."),
        ("Which is found in a plant cell but not in an animal cell?", "a cell wall made of cellulose", ["a nucleus", "mitochondria", "a plasma membrane"], "Plant cells also have chloroplasts and a large vacuole."),
        ("Which organelle is called the powerhouse of the cell?", "mitochondria", ["ribosomes", "Golgi apparatus", "lysosomes"], "They release energy as ATP."),
        ("Which organelle is called the 'suicide bag' of the cell?", "the lysosome", ["the vacuole", "the nucleus", "the ribosome"], "Its enzymes can digest the cell's own parts when the cell is damaged."),
        ("Which organelles have their own DNA and ribosomes?", "mitochondria and plastids", ["lysosomes and vacuoles", "Golgi apparatus and ER", "nucleolus and ribosomes"], "They can make some of their own proteins."),
        ("What is osmosis?", "the movement of water through a selectively permeable membrane from a dilute to a concentrated solution", ["the movement of any substance from high to low concentration in air", "the burning of food", "the making of proteins"], "It is a special kind of diffusion."),
        ("What is diffusion?", "the movement of a substance from a region of high concentration to low concentration", ["the movement of water only through a membrane", "the use of energy to move substances", "the splitting of cells"], "Carbon dioxide and oxygen move by diffusion."),
        ("What is endocytosis?", "the flexible membrane engulfing food or other material from outside", ["the movement of water into a cell", "the splitting of a cell", "the making of proteins"], "Amoeba takes in food this way."),
        ("What is plasmolysis?", "the shrinking of the cytoplasm away from the cell wall when a plant cell loses water", ["the bursting of an animal cell", "the division of the nucleus", "the formation of a cell wall"], "It happens in a hypertonic solution."),
        ("What are prokaryotic cells?", "cells without a well-defined nucleus and without membrane-bound organelles", ["cells with a nuclear membrane", "plant cells only", "animal cells only"], "Bacteria are prokaryotes."),
        ("What is the nucleoid?", "the region with genetic material in a prokaryotic cell, with no nuclear membrane", ["the nucleus of a plant cell", "a vacuole", "a type of ribosome"], "Eukaryotic cells have a true nucleus."),
        ("Which kind of cell division makes cells for growth and repair?", "mitosis", ["meiosis", "fertilisation", "osmosis"], "It gives two identical daughter cells."),
        ("Which kind of cell division makes gametes?", "meiosis", ["mitosis", "budding", "osmosis"], "It halves the number of chromosomes."),
        ("How many daughter cells does meiosis give?", "four, each with half the number of chromosomes", ["two identical cells", "one cell", "eight cells"], "Mitosis gives two identical cells."),
        ("What is the cell wall of plants mainly made of?", "cellulose", ["protein", "fat", "starch"], "Fungal cell walls are made of chitin."),
        ("Why is the plasma membrane called selectively permeable?", "it lets some substances pass but not others", ["it lets every substance pass", "it lets nothing pass", "it is made of cellulose"], "It controls what enters and leaves."),
        ("What is the plasma membrane made of?", "lipids and proteins", ["cellulose only", "starch", "DNA"], "It is flexible."),
        ("Which organelle forms lysosomes?", "the Golgi apparatus", ["mitochondria", "ribosomes", "the nucleus"], "It packages materials into vesicles."),
        ("Why are plant vacuoles larger than animal vacuoles?", "they store water and keep the cell turgid", ["plants have no cytoplasm", "they make energy", "they make proteins"], "In mature plant cells the vacuole can fill most of the cell."),
        ("What is the coloured pigment in chromoplasts?", "pigments other than chlorophyll, such as the red and yellow of fruits and flowers", ["chlorophyll only", "haemoglobin", "melanin only"], "Chloroplasts contain chlorophyll."),
        ("What would happen if the plasma membrane broke down?", "the contents would leak out and the cell would die", ["the cell would grow faster", "nothing would happen", "it would become a plant cell"], "The membrane keeps the cell's contents together."),
        ("Which of these cells has a definite nucleus (is eukaryotic)?", "an onion peel cell", ["a bacterium", "blue-green algae (cyanobacteria)", "Mycoplasma"], "Bacteria and cyanobacteria are prokaryotes."),
        ("What is membrane biogenesis?", "the making of the cell membrane, helped by proteins and lipids made in the ER", ["the splitting of a cell", "the digestion of food", "the making of DNA"], "The ER sends proteins and lipids to the membrane."),
        ("What do we call the material inside a cell, including the cytoplasm and nucleus?", "protoplasm", ["plasma", "cell wall", "nucleoid"], "The term was coined by Purkinje."),
        ("Which stain is used to see the nucleus of an onion peel cell?", "safranin or iodine", ["chlorophyll", "starch", "sugar"], "Methylene blue is used for cheek cells."),
        ("Which is the largest cell in the human body?", "the female egg (ovum)", ["the red blood cell", "the skin cell", "the nerve cell body"], "The longest cell is the nerve cell.")]


# =================================================================== Chapter 6: tissues
PTIS = [("apical meristem", "increasing the length of the stem and the root"), ("lateral meristem (cambium)", "increasing the girth (thickness) of the stem or root"),
        ("intercalary meristem", "growth at the base of leaves or the internodes"), ("parenchyma", "storing food, with thin walls and loosely packed cells"),
        ("chlorenchyma", "photosynthesis, as it contains chlorophyll"), ("aerenchyma", "helping aquatic plants float, using large air cavities"),
        ("collenchyma", "flexibility in leaves and stems, with cells thickened at the corners"), ("sclerenchyma", "hardness and strength, with dead cells and lignin in their walls"),
        ("epidermis", "protecting the plant as the outer layer of cells, often with a waxy cuticle"), ("cork", "protecting older stems; its dead cells have suberin, which keeps out water and gases"),
        ("xylem", "carrying water and minerals up from the roots"), ("phloem", "carrying food from the leaves to other parts of the plant"),
        ("tracheids and vessels", "carrying water as the tube-like cells of xylem"), ("sieve tubes", "carrying food as the tube cells of phloem with perforated walls"),
        ("companion cells", "living cells next to sieve tubes that help them work"), ("guard cells", "opening and closing the stomata"), ("xylem fibres", "giving support (they are dead cells in the xylem)")]
ATIS = [("squamous epithelium", "lining the mouth, blood vessels and lung alveoli as a thin, flat layer"), ("stratified squamous epithelium", "preventing wear and tear in the skin with several layers of cells"),
        ("columnar epithelium", "helping absorption as tall cells lining the inner wall of the intestine"), ("ciliated columnar epithelium", "pushing mucus forward in the respiratory tract with hair-like cilia"),
        ("cuboidal epithelium", "lining kidney tubules and salivary gland ducts with cube-shaped cells"), ("glandular epithelium", "secreting substances such as sweat and saliva"),
        ("blood", "carrying gases, food, hormones and wastes around the body as a fluid"), ("bone", "forming the hard skeleton, with a matrix of calcium and phosphorus"),
        ("cartilage", "smoothing bone surfaces at joints; found in the nose, ear and trachea"), ("ligament", "connecting bone to bone, with some elasticity"),
        ("tendon", "connecting muscle to bone, with great strength but little flexibility"), ("areolar tissue", "filling the space inside organs and supporting them; found between skin and muscles"),
        ("adipose tissue", "storing fat below the skin and acting as an insulator"), ("striated (voluntary) muscle", "moving the limbs; its cells are long, unbranched and multinucleate"),
        ("smooth (unstriated) muscle", "involuntary movements in the stomach, intestine and blood vessels"), ("cardiac muscle", "rhythmic contraction of the heart all through life"),
        ("nerve tissue (neurons)", "carrying messages as electrical impulses")]
TIS = [("What is a tissue?", "a group of cells similar in structure that work together to perform a function", ["a single cell", "an organ system", "a group of organs"], "Blood, bone and xylem are tissues."),
       ("Why do plants have more supportive tissue than animals?", "they are stationary and must stand upright", ["they move about", "they have no cells", "they do not grow"], "Much of this tissue is dead."),
       ("Where are meristems found?", "at the growing tips of roots and stems, and in the cambium", ["only in leaves", "only in flowers", "only in seeds"], "Their cells divide actively."),
       ("Why do meristematic cells lack vacuoles?", "they divide actively and have dense cytoplasm", ["they are dead", "they store water", "they are very large"], "Vacuoles are found in mature cells."),
       ("What is a permanent tissue?", "cells that have lost the ability to divide and have a fixed role", ["cells that keep dividing", "only dead cells", "only blood"], "They form by differentiation."),
       ("What is differentiation?", "the process by which cells take a permanent shape, size and function", ["cell division", "osmosis", "photosynthesis"], "Meristem cells differentiate into permanent tissues."),
       ("Which plant tissue is made of dead cells?", "sclerenchyma", ["parenchyma", "collenchyma", "meristem"], "The husk of a coconut is sclerenchyma."),
       ("What are the four components of xylem?", "tracheids, vessels, xylem parenchyma and xylem fibres", ["sieve tubes, companion cells, phloem fibres and phloem parenchyma", "only vessels", "guard cells and stomata"], "Phloem has sieve tubes, companion cells, phloem parenchyma and phloem fibres."),
       ("Which part of phloem is made of dead cells?", "phloem fibres", ["sieve tubes", "companion cells", "phloem parenchyma"], "The other parts of phloem are living."),
       ("What substance makes cork impervious to gases and water?", "suberin", ["lignin", "cellulose", "chitin"], "Lignin hardens sclerenchyma."),
       ("What are stomata used for?", "exchange of gases with the air and transpiration", ["absorbing water from the soil", "carrying food", "making seeds"], "Guard cells open and close them."),
       ("What does the waxy cuticle on leaves do?", "it reduces water loss", ["it helps photosynthesis", "it makes the leaf heavy", "it carries water"], "Desert plants have a thick cuticle."),
       ("Which is the fluid part of blood called?", "plasma", ["platelets", "red blood cells", "lymph"], "Red cells, white cells and platelets float in the plasma."),
       ("Which blood cells help in clotting?", "platelets", ["red blood cells", "white blood cells", "plasma"], "White blood cells fight infection."),
       ("What is the function of red blood cells?", "carrying oxygen using haemoglobin", ["fighting germs", "clotting blood", "making hormones"], "They have no nucleus in mammals."),
       ("Why is cardiac muscle different from voluntary muscle?", "it contracts rhythmically all through life without tiring and without our control", ["it is controlled by our will", "it is found in the arms", "its cells are multinucleate and unbranched"], "Its cells are branched and uninucleate."),
       ("What is the shape of smooth muscle cells?", "long and spindle-shaped with one nucleus", ["branched with one nucleus", "cylindrical with many nuclei", "round"], "They are found in the iris of the eye and the gut."),
       ("What are the parts of a neuron?", "a cell body with a nucleus, dendrites and an axon", ["a nucleus and a cell wall", "a chloroplast and a vacuole", "only an axon"], "A neuron can be up to a metre long."),
       ("What is a nerve?", "many nerve fibres bound together by connective tissue", ["a single cell", "a muscle", "a bone"], "Nerves carry messages around the body."),
       ("Which tissue lines the inside of the trachea and moves dust out?", "ciliated columnar epithelium", ["cardiac muscle", "adipose tissue", "bone"], "The cilia sweep mucus upwards."),
       ("Which tissue stores fat in our body?", "adipose tissue", ["areolar tissue", "bone", "blood"], "It also works as an insulator."),
       ("What would happen if the ligaments at a joint were damaged?", "the bones would not stay firmly joined and the joint would be weak", ["the muscles would stop working", "the blood would not clot", "the bone would melt"], "Ligaments join bone to bone."),
       ("What does lignin do in plant cells?", "it acts like cement and hardens the cell walls", ["it makes food", "it stores water", "it makes the cells divide"], "It is found in sclerenchyma."),
       ("Which tissue helps aquatic plants float?", "aerenchyma", ["sclerenchyma", "collenchyma", "cork"], "It has big air cavities.")]
PLOC = [("the husk of a coconut", "sclerenchyma"), ("the stalk of a leaf", "collenchyma"), ("the bark of a tree", "cork"), ("the root tip", "apical meristem"),
        ("the cambium between xylem and phloem", "lateral meristem (cambium)"), ("the green tissue of a leaf", "chlorenchyma"), ("the stem of a lotus or water hyacinth", "aerenchyma"),
        ("the base of grass leaves", "intercalary meristem"), ("the veins of a leaf carrying water", "xylem"), ("the hard shell of a walnut", "sclerenchyma"), ("the pith of a stem", "parenchyma"),
        ("the outermost layer of a leaf", "epidermis"), ("the growing tip of a shoot", "apical meristem"), ("the tubes carrying sugar down from the leaves", "phloem"), ("the starch-storing cortex of a root", "parenchyma"), ("the fibres of jute", "sclerenchyma")]
ALOC = [("the lining of blood vessels and the lung alveoli", "squamous epithelium"), ("the outer layer of the skin", "stratified squamous epithelium"),
        ("the inner lining of the small intestine", "columnar epithelium"), ("the lining of the kidney tubules", "cuboidal epithelium"), ("the walls of the heart", "cardiac muscle"),
        ("the biceps of the upper arm", "striated (voluntary) muscle"), ("the walls of the stomach and intestine", "smooth (unstriated) muscle"), ("the tip of the nose and the ear", "cartilage"),
        ("the brain and the spinal cord", "nerve tissue (neurons)"), ("below the skin, storing fat", "adipose tissue"), ("between the skin and muscles", "areolar tissue"), ("the inner lining of the trachea", "ciliated columnar epithelium"), ("the sweat glands of the skin", "glandular epithelium"),
        ("the knee, holding the thigh bone to the shin bone", "ligament"), ("the heel, joining the calf muscle to the heel bone", "tendon"), ("the skeleton", "bone"),
        ("the iris of the eye and the ureters", "smooth (unstriated) muscle"), ("the thigh muscles", "striated (voluntary) muscle"), ("the blood vessels, flowing through them", "blood")]


# =================================================================== Chapter 12: improvement in food resources
CROPS = {"a cereal": ["wheat", "rice (paddy)", "maize", "millets", "sorghum (jowar)", "barley"], "a pulse": ["gram (chana)", "pea", "black gram (urad)", "green gram (moong)", "pigeon pea (arhar)", "lentil (masoor)"],
         "an oilseed": ["soybean", "groundnut", "sesame (til)", "castor", "mustard", "linseed", "sunflower"], "a fodder crop": ["berseem", "oats grown for cattle", "sudan grass"]}
SEASON = {"a kharif (rainy season) crop": ["paddy", "soybean", "pigeon pea", "maize", "cotton", "green gram", "black gram"],
          "a rabi (winter season) crop": ["wheat", "gram", "peas", "mustard", "linseed", "barley"]}
NUTS = {"a macronutrient (needed in large amounts)": ["nitrogen", "phosphorus", "potassium", "calcium", "magnesium", "sulphur"],
        "a micronutrient (needed in small amounts)": ["iron", "manganese", "boron", "zinc", "copper", "molybdenum", "chlorine"]}
PRACT = [("mixed cropping", "growing two or more crops together on the same piece of land at the same time"), ("intercropping", "growing two or more crops in rows in a definite pattern on the same field"),
         ("crop rotation", "growing different crops on a piece of land one after another in a planned order"), ("hybridisation", "crossing genetically different plants to get better varieties"),
         ("green manuring", "growing plants such as sun hemp and then ploughing them into the soil"), ("vermicompost", "compost made by using earthworms to break down plant and animal waste"),
         ("organic farming", "farming with little or no chemical fertilisers, pesticides or herbicides"), ("apiculture", "keeping bees for honey and wax"),
         ("pisciculture (fish farming)", "rearing fish in ponds or tanks"), ("mariculture", "culturing marine fish such as mullets and pearl spots in sea water"),
         ("composite fish culture", "growing five or six fish species that feed at different levels in one pond"), ("broiler rearing", "raising poultry birds for meat"),
         ("layer rearing", "raising hens for eggs"), ("poultry farming", "raising domestic fowl for eggs and meat"), ("pasturage", "the flowers available to bees for collecting nectar and pollen")]
ANIM = [("Jersey", "an exotic (foreign) cattle breed chosen for long lactation"), ("Brown Swiss", "an exotic cattle breed chosen for high milk yield"),
        ("Red Sindhi", "a local (Indian) cattle breed with good disease resistance"), ("Sahiwal", "a local (Indian) cattle breed with good disease resistance"),
        ("Aseel", "an indigenous (Indian) breed of poultry"), ("Leghorn", "an exotic breed of poultry used for eggs"),
        ("catla", "a fish that feeds at the surface in composite fish culture"), ("rohu", "a fish that feeds in the middle zone of the pond"),
        ("mrigal", "a fish that feeds at the bottom of the pond"), ("grass carp", "a fish that feeds on weeds"), ("silver carp", "a fish that feeds at the surface"),
        ("Apis cerana indica", "the common Indian bee"), ("Apis mellifera", "the Italian bee, which gives more honey and stings less"), ("Apis dorsata", "the rock bee")]
FOOD = [("What was the green revolution?", "a large increase in food-grain production", ["an increase in milk production", "planting more forests", "growing more flowers"], "It came from better seeds, fertilisers and irrigation."),
        ("What was the white revolution?", "a large increase in milk production", ["an increase in food-grain production", "an increase in fish production", "a rise in cotton production"], "It is linked to Operation Flood."),
        ("Which is a major source of protein among crops?", "pulses", ["cereals", "vegetables", "fodder"], "Cereals mainly give carbohydrates."),
        ("Why are manures better than fertilisers for the soil in the long run?", "they add organic matter and improve soil structure", ["they act faster", "they are always cheaper", "they contain only nitrogen"], "Too much fertiliser harms soil life and water."),
        ("Why are fertilisers harmful if overused?", "they can pollute water and reduce soil fertility over time", ["they give no nutrients", "they make crops grow too slowly", "they kill only weeds"], "They should be used carefully."),
        ("What are weeds?", "unwanted plants that compete with crops for food, space and light", ["useful wild plants", "plant diseases", "pests that eat crops"], "Xanthium and Parthenium are weeds."),
        ("Which is a way to control pests?", "using resistant varieties and pesticides carefully", ["adding more water", "growing only one crop for many years", "leaving harvested grain wet"], "Pests may also be controlled biologically."),
        ("Why must grain be dried before storage?", "moisture encourages fungi, insects and bacteria", ["dry grain weighs more", "wet grain cannot be sold", "drying adds nutrients"], "Cleaning and fumigation also help."),
        ("Which are the main sources of irrigation in India?", "wells, canals, rivers and tanks", ["only rain", "only the sea", "only glaciers"], "Rainwater harvesting adds to them."),
        ("Why is crop rotation useful?", "it keeps the soil fertile and reduces pests", ["it uses more water", "it needs more fertilisers", "it lowers yields"], "Legumes in the rotation add nitrogen."),
        ("Why are leguminous crops good for the soil?", "bacteria in their root nodules fix nitrogen", ["they take all nutrients out", "they are poisonous to pests", "they grow without water"], "Pulses are legumes."),
        ("What is the main advantage of mixed cropping?", "it reduces the risk of total crop failure", ["it always doubles the yield", "it uses no water", "it removes all pests"], "If one crop fails, the other may survive."),
        ("What are the desirable traits in fodder crops?", "tall plants with profuse branching", ["dwarf plants with few leaves", "plants with thorns", "plants that need no light"], "Cereals are often bred to be dwarf."),
        ("What is the purpose of an animal shelter for dairy animals?", "to protect them from rain, heat and cold and keep them clean", ["to make them grow wool", "to make them stop eating", "to make them lay eggs"], "Floors should slope to stay dry."),
        ("What is roughage in cattle feed?", "fibre-rich food such as hay and straw", ["protein-rich food only", "medicines", "water"], "Concentrates are rich in protein and other nutrients."),
        ("What is the main source of protein in a broiler's diet?", "a protein-rich feed with adequate fat", ["only grass", "only water", "only sugar"], "Broilers also need vitamins A and K."),
        ("What is the difference between capture fishing and culture fishery?", "capture fishing takes fish from natural sources; culture fishery rears them in ponds or the sea", ["they are the same", "capture fishing rears fish in tanks", "culture fishery uses nets in rivers only"], "Mariculture is a type of culture fishery."),
        ("What is a problem with composite fish culture?", "many fish breed only in the monsoon, so pure seed is hard to get", ["the fish compete for food", "it needs no water", "it uses only one species"], "Hormones are now used to induce breeding."),
        ("What decides the quality and taste of honey?", "the pasturage, the flowers available to the bees", ["the size of the hive", "the colour of the bees", "the time of day"], "Bees collect nectar and pollen from flowers."),
        ("What are photoperiods in crop growth?", "the duration of sunlight a crop receives, which affects flowering", ["the number of seeds sown", "the amount of rain", "the type of soil"], "Different crops need different photoperiods."),
        ("Which crop gives us fibre for clothes?", "cotton", ["wheat", "gram", "mustard"], "Jute is another fibre crop."),
        ("What is an important aim of crop variety improvement?", "higher yield, better quality and resistance to diseases", ["making crops need more water", "making crops grow slower", "removing all seeds"], "Wider adaptability is another aim."),
        ("Which practice adds nitrogen to soil without chemicals?", "growing leguminous plants", ["burning crop stubble", "using more water", "growing the same crop every year"], "Root-nodule bacteria fix nitrogen."),
        ("Why are exotic and local cattle breeds crossed?", "to get animals with both high milk yield and disease resistance", ["to make the animals smaller", "to stop lactation", "to make them eat less"], "Jersey × Sahiwal is an example."),
        ("What is the main source of nutrients for plants?", "the soil (and air and water for carbon, hydrogen and oxygen)", ["only sunlight", "only rain", "only fertilisers"], "There are 16 nutrients essential for plants."),
        ("Which is a biotic factor that causes crop losses?", "insects and pests", ["drought", "cold", "frost"], "Drought and frost are abiotic factors."),
        ("Which is an abiotic factor that causes crop losses?", "flood", ["rodents", "fungi", "insects"], "Living causes are biotic.")]


def UNITS9b():
    OL, FD = "Organization in the Living World", "Food; Food Production"
    b = {n: once_maker(v) for n, v in [("cell", CELL), ("tis", TIS), ("food", FOOD)]}
    org = pairs(ORG, "What is the job of %s in a cell?", "Which part of the cell does this: %s?")
    osm = pairs(OSM, "What happens to %s?")
    hist = pairs(HIST, "What did %s do?", "Who %s?")
    ptis = pairs(PTIS, "What is the role of %s in a plant?", "Which plant tissue is responsible for %s?")
    atis = pairs(ATIS, "What is the role of %s?", "Which animal tissue is described here: %s?")
    ploc = pairs(PLOC, "Which plant tissue is mainly found in %s?")
    aloc = pairs(ALOC, "Which tissue is found in %s?")
    crop = odd_one(CROPS, "Which of these is %s?", "Which of these is not %s?")
    season = odd_one(SEASON, "Which of these is %s?", "Which of these is not %s?")
    nut = odd_one(NUTS, "Which of these plant nutrients is %s?", "Which of these plant nutrients is not %s?")
    ctype = odd_one(CELLTYPE, "Which of these is %s?", "Which of these is not %s?")
    um = odd_one(UNIMULTI, "Which of these is %s?", "Which of these is not %s?")
    plani = odd_one(PLANI, "Which of these is %s?")
    pr = pairs(PRACT, "What is %s?", "What is the name for %s?")
    an = pairs(ANIM, "What is %s?", "Which of these is %s?")
    return [
        U(5, "the-fundamental-unit-of-life", 5, OL,
          "Cell – basic unit of life: prokaryotic and eukaryotic cells, multicellular organisms; cell membrane and cell wall, cell organelles and cell inclusions; chloroplast, mitochondria, vacuoles, endoplasmic reticulum, Golgi apparatus; nucleus, chromosomes – basic structure, number.",
          "The Fundamental Unit of Life", "the fundamental unit of life",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 5: cell theory, the plasma membrane, osmosis and diffusion, the cell wall, the nucleus, organelles such as mitochondria and plastids, and prokaryotic and eukaryotic cells. 100 questions with answers.",
          "The cell is the basic unit of life.", "Mitochondria release energy; chloroplasts make food.",
          "<p>All living things are made of cells, and every cell comes from an existing cell. A cell has a plasma membrane, cytoplasm and a nucleus with chromosomes. Plant cells also have a cellulose cell wall, plastids such as chloroplasts and a large vacuole.</p>"
          "<p>Water moves across the selectively permeable membrane by osmosis: a cell swells in a dilute (hypotonic) solution and shrinks in a concentrated (hypertonic) one. Organelles share the work: mitochondria release energy, ribosomes make proteins, the Golgi apparatus packages them and lysosomes digest waste. Prokaryotes such as bacteria have no nuclear membrane.</p>",
          [("A plant cell in strong salt solution?", ["water leaves by osmosis"], "plasmolysis: the cytoplasm shrinks from the wall"), ("Which organelle makes proteins?", ["the site of protein synthesis"], "ribosomes")],
          ["Thinking osmosis moves solute particles rather than water.", "Saying animal cells have a cell wall.", "Calling bacteria eukaryotes."],
          [("What is the difference between prokaryotic and eukaryotic cells?", "Prokaryotic cells (bacteria) have no nuclear membrane and no membrane-bound organelles; eukaryotic cells have a true nucleus and organelles."),
           ("Why are lysosomes called suicide bags?", "If the cell is damaged, they can burst and their enzymes digest the cell itself.")],
          lambda: [("Organelles and their jobs", [(org, 20)]), ("Membrane, osmosis and diffusion", [(osm, 8), (c_osm2, 12)]), ("Discovering the cell and cell types", [(hist, 8), (ctype, 6), (um, 6)]),
                   ("Plant cells and animal cells", [(plani, 8), (b["cell"], 12)]), ("Mixed problems", [(org, 10), (b["cell"], 6), (c_osm2, 4)])]),
        U(6, "tissues", 6, OL,
          "Tissues, organs, organ system, organism. Structure and functions of animal and plant tissues (only four types of tissues in animals; meristematic and permanent tissues in plants).",
          "Tissues", "tissues",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 6: meristematic and permanent plant tissues, xylem and phloem, and epithelial, connective, muscular and nervous tissues in animals. 100 questions with answers.",
          "A tissue is a group of similar cells doing one job.", "Plants: meristem and permanent tissue. Animals: four types.",
          "<p>Plants have meristematic tissue, which keeps dividing at root and shoot tips (apical), in the cambium (lateral) and at the base of leaves (intercalary), and permanent tissue. Simple permanent tissues are parenchyma, collenchyma and sclerenchyma; complex tissues are xylem (water) and phloem (food).</p>"
          "<p>Animals have four kinds of tissue: epithelial (covering and lining), connective (blood, bone, cartilage, ligament, tendon, areolar and adipose), muscular (striated, smooth and cardiac) and nervous tissue made of neurons.</p>",
          [("Which tissue joins muscle to bone?", ["strong, little flexibility"], "a tendon"), ("Which tissue makes a stem thicker?", ["cambium divides sideways"], "lateral meristem")],
          ["Mixing up ligaments (bone to bone) and tendons (muscle to bone).", "Saying xylem carries food.", "Calling sclerenchyma a living tissue."],
          [("What is the difference between xylem and phloem?", "Xylem carries water and minerals upwards; phloem carries food made in the leaves to all parts of the plant."),
           ("What are the three kinds of muscle?", "Striated (voluntary) muscle in limbs, smooth (involuntary) muscle in organs such as the stomach, and cardiac muscle in the heart.")],
          lambda: [("Meristematic tissue", [(ptis, 14), (ploc, 6)]), ("Permanent plant tissue", [(ptis, 14), (b["tis"], 6)]), ("Epithelial and connective tissue", [(atis, 14), (aloc, 6)]),
                   ("Muscle and nerve tissue", [(atis, 12), (b["tis"], 8)]), ("Mixed problems", [(aloc, 6), (ploc, 6), (b["tis"], 4), (atis, 4)])]),
        U(12, "improvement-in-food-resources", 12, FD,
          "Plant and animal breeding and selection for quality improvement and management; use of fertilizers and manures; protection from pests and diseases; organic farming.",
          "Improvement in Food Resources", "improvement in food resources",
          "Free CBSE Class 9 Science worksheets for NCERT Chapter 12: kharif and rabi crops, crop variety improvement, nutrients, manures and fertilisers, cropping patterns, crop protection, and animal husbandry: cattle, poultry, fish and bees. 100 questions with answers.",
          "Better seeds, good care and protection raise food production.", "Kharif crops grow in the rainy season; rabi crops in winter.",
          "<p>Food production is raised by improving crop varieties (hybridisation for yield, quality and disease resistance), managing crops (nutrients, manures and fertilisers, irrigation and cropping patterns such as mixed cropping, intercropping and crop rotation) and protecting crops from weeds, pests, diseases and damage in storage.</p>"
          "<p>Animal husbandry looks after dairy animals, poultry, fish and bees. Exotic and Indian breeds are crossed to combine high yield with disease resistance; composite fish culture keeps species that feed at different levels in one pond.</p>",
          [("Is wheat a kharif or rabi crop?", ["sown in winter"], "rabi"), ("Which fish feeds at the bottom in composite culture?", ["catla surface, rohu middle"], "mrigal (or common carp)")],
          ["Calling paddy a rabi crop.", "Thinking fertilisers improve soil structure like manure.", "Mixing up mixed cropping and intercropping."],
          [("What is the difference between manure and fertiliser?", "Manure is natural organic matter that improves soil structure; fertilisers are factory-made chemicals that give specific nutrients quickly."),
           ("What is composite fish culture?", "Rearing five or six fish species that feed in different zones of the pond, so all the food in the pond is used.")],
          lambda: [("Crops and seasons", [(crop, 12), (season, 8)]), ("Nutrients, manures and fertilisers", [(nut, 10), (b["food"], 10)]), ("Farming practices", [(pr, 20)]),
                   ("Animal husbandry", [(an, 14), (b["food"], 6)]), ("Mixed problems", [(crop, 6), (season, 4), (b["food"], 4), (an, 4), (nut, 2)])]),
    ]
