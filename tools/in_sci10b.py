# -*- coding: utf-8 -*-
"""Class 10 Science, Unit II World of Living (NCERT chapters 5–8) and Unit V Natural Resources (chapter 13): question makers."""
from fractions import Fraction as F
from uk_alsci import nf, nq, tq, once_maker
from in_sci import pairs, name, _R, U, K


def ch(xs):
    return _R[0].choice(xs)


def fr(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (x.numerator, x.denominator)


# =================================================================== Chapter 5: life processes
ORGAN5 = [("stomata", "exchange of gases and loss of water vapour in leaves"), ("guard cells", "opening and closing the stomatal pore"),
          ("chlorophyll", "absorbing light energy for photosynthesis"), ("villi in the small intestine", "increasing the surface area for absorbing digested food"),
          ("alveoli", "exchange of oxygen and carbon dioxide in the lungs"), ("xylem", "carrying water and minerals from roots to leaves"),
          ("phloem", "carrying food from leaves to other parts of the plant"), ("nephron", "filtering blood to remove waste as urine"),
          ("glomerulus", "a cluster of capillaries where blood is filtered in the kidney"), ("ureter", "carrying urine from the kidney to the urinary bladder"),
          ("urinary bladder", "storing urine"), ("haemoglobin", "carrying oxygen in red blood cells"), ("platelets", "helping blood to clot at a wound"),
          ("valves in the heart", "preventing blood from flowing backwards"), ("the left ventricle", "pumping oxygenated blood to the whole body"),
          ("the right atrium", "receiving deoxygenated blood from the body"), ("arteries", "carrying blood away from the heart at high pressure"),
          ("veins", "bringing blood back to the heart"), ("capillaries", "exchanging materials between blood and cells through thin walls"),
          ("lymph", "carrying digested fat and draining excess tissue fluid back into the blood"), ("the diaphragm", "changing the volume of the chest cavity during breathing"),
          ("rings of cartilage in the trachea", "stopping the air passage from collapsing"), ("the liver", "making bile"), ("the pancreas", "making pancreatic juice with trypsin and lipase"),
          ("the large intestine", "absorbing extra water from undigested food"), ("the anal sphincter", "controlling the removal of undigested waste"),
          ("salivary glands", "making saliva with salivary amylase"), ("the oesophagus", "moving food from the mouth to the stomach by peristalsis"),
          ("root hairs", "taking in water and minerals from the soil"),
          ("the epiglottis", "closing the windpipe when we swallow food"), ("the gall bladder", "storing bile"), ("white blood cells", "fighting infection"),
          ("the trachea", "carrying air from the nose and throat to the lungs"), ("the aorta", "carrying oxygenated blood from the heart to the body"),
          ("the vena cava", "bringing deoxygenated blood from the body to the heart"), ("Bowman's capsule", "collecting the filtrate from the glomerulus"), ("the urethra", "carrying urine out of the body")]
ENZ5 = [("salivary amylase", "the mouth", "starch into sugar"), ("pepsin", "the stomach", "proteins"), ("trypsin", "the pancreas", "proteins"),
        ("lipase", "the pancreas", "emulsified fats into fatty acids and glycerol"), ("hydrochloric acid", "the stomach", "nothing directly: it makes the medium acidic for pepsin"),
        ("bile", "the liver", "nothing directly: it emulsifies fats into small droplets")]
NUT = [("Amoeba", "holozoic: it takes in whole food by pseudopodia"), ("Cuscuta (amar-bel)", "parasitic"), ("ticks and lice", "parasitic"), ("bread mould and mushrooms", "saprotrophic"),
       ("green plants", "autotrophic"), ("Paramecium", "holozoic: cilia sweep food into the cell mouth"), ("tapeworm", "parasitic"), ("human beings", "holozoic")]
HEART = [("crocodiles", "4"), ("lizards", "3"), ("humans", "4"), ("fish", "2"), ("frogs (amphibians)", "3"), ("most reptiles", "3"), ("birds", "4"), ("mammals", "4")]
RESP5 = [("glucose in the cytoplasm of all cells", "pyruvate (a 3-carbon molecule) and a little energy"), ("pyruvate in yeast without oxygen", "ethanol, carbon dioxide and energy"),
         ("pyruvate in muscle cells short of oxygen", "lactic acid and energy"), ("pyruvate in mitochondria with oxygen", "carbon dioxide, water and a lot of energy")]


def c_life(k=None):
    k = k or ch(["enz", "nut", "heart", "resp"])
    if k == "enz":
        e, wh, ac = ch(ENZ5)
        if ch([0, 1]):
            return tq("Where is %s secreted?" % e, wh, [x for x in ["the mouth", "the stomach", "the pancreas", "the liver", "the large intestine"] if x != wh][:3] if wh != "the mouth" else ["the stomach", "the pancreas", "the liver"],
                      "%s is secreted in %s." % (e[0].upper() + e[1:], wh))
        return tq("What does %s act on?" % e, ac, _R[0].sample([x[2] for x in ENZ5 if x[2] != ac and not (x[2] == "proteins" and ac == "proteins")], 3), "%s (from %s) acts on %s." % (e[0].upper() + e[1:], wh, ac))
    if k == "nut":
        o, m = ch(NUT)
        cats = sorted({x[1].split(":")[0] for x in NUT})
        return tq("What is the mode of nutrition of %s?" % o, m.split(":")[0], [c for c in cats if c != m.split(":")[0]], "%s: %s." % (o, m))
    if k == "heart":
        o, n = ch(HEART)
        return tq("How many chambers does the heart of %s have?" % o, n, [x for x in ["1", "2", "3", "4", "5"] if x != n][:3], "Fish 2, amphibians and most reptiles 3, birds and mammals 4 (complete separation of oxygenated and deoxygenated blood).")
    a, b = ch(RESP5)
    return tq("What is formed from %s?" % a, b, [x[1] for x in RESP5 if x[1] != b], "Glucose → pyruvate in the cytoplasm; then ethanol + CO₂ (yeast), lactic acid (muscles), or CO₂ + water in mitochondria.")


LIFE = [("What are the raw materials of photosynthesis?", "carbon dioxide and water", ["oxygen and glucose", "nitrogen and water", "starch and oxygen"], "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂ in sunlight with chlorophyll."),
        ("Which gas is released during photosynthesis?", "oxygen", ["carbon dioxide", "nitrogen", "hydrogen"], "It comes from splitting water."),
        ("How do we test a leaf for starch?", "boil it in alcohol to remove chlorophyll, then add iodine solution", ["add lime water", "add Benedict's solution", "heat it until it burns"], "Starch turns blue-black."),
        ("Why do desert plants open their stomata at night?", "to reduce water loss; they store CO₂ as an acid and use it in the day", ["they photosynthesise at night", "they need oxygen at night", "to absorb water"], "This is how cacti survive."),
        ("Why is the rate of breathing in aquatic animals faster than in land animals?", "there is much less dissolved oxygen in water than in air", ["water is colder", "they are smaller", "they have no lungs"], "Fish take in water through the mouth and pass it over the gills."),
        ("Why do the walls of the left ventricle need to be thick?", "it pumps blood to all parts of the body at high pressure", ["it receives blood from the lungs", "it stores blood", "it makes blood cells"], "The right ventricle pumps only to the lungs."),
        ("What is double circulation?", "blood passes through the heart twice in each cycle of the body", ["blood flows in two directions at once", "there are two hearts", "blood is filtered twice"], "Once to the lungs and once to the body."),
        ("What is transpiration?", "the loss of water vapour from the aerial parts of a plant", ["water uptake by roots", "movement of food in phloem", "making food in leaves"], "It helps pull water up through the xylem."),
        ("What is translocation?", "the transport of food (sucrose) in the phloem", ["transport of water in xylem", "loss of water from leaves", "the opening of stomata"], "It uses energy from ATP."),
        ("Why is the small intestine very long?", "to give enough time and surface for digestion and absorption", ["to store food", "to make bile", "to make blood"], "Herbivores eating grass have a longer small intestine than carnivores."),
        ("What is the role of saliva in digestion?", "salivary amylase breaks down starch into sugar", ["it digests proteins", "it kills all bacteria", "it digests fats"], "Digestion begins in the mouth."),
        ("What happens to the energy released in respiration?", "it is stored as ATP for use by the cell", ["it is lost as light", "it is stored as glucose", "it becomes oxygen"], "ATP is the energy currency of the cell."),
        ("Which organs are the main excretory organs in humans?", "the kidneys", ["the lungs only", "the heart", "the liver only"], "Each kidney has many nephrons."),
        ("How do plants get rid of some waste products?", "they store them in leaves that fall, as resins and gums, or in vacuoles", ["they have kidneys", "they urinate", "they breathe out salt"], "Plants also lose oxygen and water vapour through stomata."),
        ("Why does a person feel muscle cramps after running fast?", "lactic acid builds up when muscles respire without enough oxygen", ["muscles run out of water", "glucose turns into ethanol", "blood stops flowing"], "This is anaerobic respiration."),
        ("What is the function of mucus in the stomach?", "protecting the inner lining from the acid", ["digesting proteins", "making the food acidic", "absorbing food"], "Without it the stomach would be damaged."),
        ("What is peristalsis?", "rhythmic contraction of muscles that pushes food along the gut", ["digestion by enzymes", "absorption of food", "chewing of food"], "It happens all along the alimentary canal."),
        ("Why do red blood cells lack a nucleus in mammals?", "more space for haemoglobin to carry oxygen", ["to make them heavier", "to divide faster", "to fight germs"], "They are disc-shaped too."),
        ("Which blood vessel carries oxygenated blood from the lungs to the heart?", "the pulmonary vein", ["the pulmonary artery", "the vena cava", "the aorta"], "It is a vein that carries oxygenated blood."),
        ("What is the purpose of making urine?", "removing harmful nitrogenous waste such as urea from the blood", ["storing water", "making blood", "digesting food"], "Urine also removes extra water and salts."),
        ("What is selective reabsorption in the kidney?", "useful substances such as glucose and some water are taken back into the blood", ["all water is lost", "proteins are filtered out", "blood cells are removed"], "It happens in the tubule of the nephron."),
        ("Which part of a plant cell contains chlorophyll?", "chloroplasts", ["mitochondria", "the nucleus", "the cell wall"], "Chloroplasts are mainly in leaf cells."),
        ("Which organism makes food from simple inorganic substances?", "an autotroph such as a green plant", ["a heterotroph such as a cow", "a parasite", "a saprophyte"], "Autotrophs use sunlight or chemicals."),
        ("What are the three events in photosynthesis?", "absorbing light, splitting water and reducing CO₂ to carbohydrate", ["eating, digesting and absorbing", "breathing in, breathing out and resting", "filtering, storing and excreting"], "They need not happen one right after another."),
        ("How does the tongue help in digestion?", "it mixes food with saliva and pushes it to the back of the mouth", ["it digests protein", "it makes bile", "it absorbs food"], "Teeth break the food into small pieces."),
        ("Why does the stomach make hydrochloric acid?", "to make the medium acidic so pepsin can work and to kill germs", ["to digest starch", "to make bile", "to absorb water"], "Too much acid causes acidity."),
        ("Why do herbivores have a longer small intestine than carnivores?", "cellulose in grass takes longer to digest", ["they eat more meat", "they are bigger", "they have no stomach"], "Carnivores eat meat, which is easier to digest."),
        ("What is the role of the lungs in the exchange of gases?", "alveoli give a large surface where oxygen enters and CO₂ leaves the blood", ["they pump blood", "they make blood", "they digest food"], "The alveoli are close to many capillaries."),
        ("How do plants exchange gases?", "by diffusion through stomata in leaves and lenticels in stems", ["through roots only", "through flowers", "by lungs"], "At night they give out CO₂ only.")]


# =================================================================== Chapter 6: control and coordination
BRAIN = [("the cerebrum (forebrain)", "thinking, memory and voluntary actions"), ("the cerebellum (hindbrain)", "balance, posture and precise voluntary movements"),
         ("the medulla (hindbrain)", "involuntary actions such as blood pressure, salivation and vomiting"), ("the hypothalamus", "controlling the pituitary gland by releasing hormones"),
         ("the spinal cord", "carrying messages to and from the brain and controlling reflex actions"), ("the pons", "regulating breathing"),
         ("the midbrain", "some reflexes such as the movement of the eyes"), ("the cranium (skull)", "protecting the brain"), ("the vertebral column", "protecting the spinal cord"),
         ("cerebrospinal fluid", "cushioning the brain against shocks")]
HORM = [("thyroxine", "the thyroid gland", "controlling carbohydrate, protein and fat metabolism"), ("insulin", "the pancreas", "lowering the blood sugar level"),
        ("adrenaline", "the adrenal glands", "preparing the body for action in an emergency"), ("growth hormone", "the pituitary gland", "controlling growth of the body"),
        ("testosterone", "the testes", "changes in boys at puberty"), ("oestrogen", "the ovaries", "changes in girls at puberty"),
        ("releasing hormones", "the hypothalamus", "stimulating the pituitary to release hormones"),
        ("parathormone", "the parathyroid glands", "controlling the level of calcium in the blood"), ("thymosin", "the thymus", "helping the immune system develop in children"),
        ("melatonin", "the pineal gland", "regulating sleep and the daily body clock")]
PLANT6 = [("auxin", "promoting cell elongation; it moves to the shaded side of a shoot"), ("gibberellins", "promoting growth of the stem"), ("cytokinins", "promoting cell division"),
          ("abscisic acid", "inhibiting growth and causing wilting of leaves")]
TROP = [("touch (such as a tendril around a support)", "thigmotropism"), ("light", "phototropism"), ("gravity", "geotropism"), ("water", "hydrotropism"), ("chemicals (such as the pollen tube growing to the ovule)", "chemotropism")]
NEURON = [("dendrites", "picking up the message at the nerve ending"), ("the axon", "carrying the electrical impulse away from the cell body"),
          ("the synapse", "the gap where a chemical passes the message to the next cell"), ("the cell body", "containing the nucleus of the neuron"),
          ("receptors", "detecting a stimulus, for example in the skin or tongue"), ("effectors (muscles and glands)", "responding to the message")]


def c_ctrl(k=None):
    k = k or ch(["gland", "hfunc", "def"])
    h, g, f = ch(HORM)
    if k == "gland":
        if ch([0, 1]):
            return tq("Which gland secretes %s?" % h, g, _R[0].sample([x[1] for x in HORM if x[1] != g], 3), "%s is secreted by %s." % (h[0].upper() + h[1:], g))
        return tq("Which hormone is secreted by %s?" % g, h, _R[0].sample([x[0] for x in HORM if x[0] != h], 3), "%s secretes %s." % (g[0].upper() + g[1:], h))
    if k == "hfunc":
        return tq("What is the main job of %s?" % h, f, _R[0].sample([x[2] for x in HORM if x[2] != f], 3), "%s (%s): %s." % (h[0].upper() + h[1:], g, f))
    d = [("goitre (a swollen neck)", "too little iodine for making thyroxine"), ("diabetes", "too little insulin"), ("dwarfism", "too little growth hormone in childhood"),
         ("gigantism", "too much growth hormone in childhood")]
    a, b = ch(d)
    return tq("What causes %s?" % a, b, [x[1] for x in d if x[1] != b], "%s is caused by %s." % (a[0].upper() + a[1:], b))


CTRL = [("What is a reflex action?", "a quick, automatic response to a stimulus, controlled by the spinal cord", ["a slow, thought-out action", "a hormone response", "a plant movement"], "Pulling your hand from a hot object is a reflex."),
        ("What is the path of a reflex arc?", "receptor → sensory neuron → spinal cord (relay) → motor neuron → effector", ["effector → motor neuron → brain → receptor", "brain → receptor → effector", "receptor → brain → hormone"], "The brain is informed but not needed for the response."),
        ("Which part protects the brain?", "the skull (cranium) and fluid-filled membranes", ["the vertebral column only", "the ribs", "the diaphragm"], "The spinal cord is protected by the vertebral column."),
        ("Why does a touch-me-not plant fold its leaves when touched?", "cells change shape by changing the amount of water in them", ["the leaves grow faster", "auxin moves to the leaves", "the plant has nerves"], "This is not growth; it is quick movement."),
        ("Why does a shoot bend towards light?", "auxin collects on the shaded side and makes those cells grow longer", ["light pushes the shoot", "the shoot has muscles", "auxin is made in the roots"], "This is positive phototropism."),
        ("How do tendrils of a pea plant wind round a support?", "the side away from the support grows faster", ["the side touching the support grows faster", "they have muscles", "gravity pulls them"], "This is thigmotropism (response to touch)."),
        ("Why do roots grow downwards?", "they are positively geotropic (they respond to gravity)", ["they need light", "they avoid water", "they are pushed by the stem"], "Shoots are negatively geotropic."),
        ("What is the advantage of a feedback mechanism in hormone control?", "it keeps the amount of hormone at the right level", ["it makes more hormone all the time", "it stops all hormones", "it makes nerves faster"], "For example, high blood sugar triggers insulin release."),
        ("Why is iodised salt recommended?", "iodine is needed to make thyroxine and prevent goitre", ["it makes food tasty", "it stops diabetes", "it helps digestion"], "Thyroxine controls metabolism."),
        ("Why do nervous messages work faster than hormones?", "they travel as electrical impulses along neurons", ["hormones travel through nerves", "hormones are electric", "nerves are thicker than blood vessels"], "Hormones travel in the blood."),
        ("What is the main difference between nervous and hormonal control?", "nerves give fast, short responses; hormones give slower, longer-lasting ones", ["hormones are faster", "nerves work only in plants", "hormones use electrical impulses"], "Both work together to coordinate the body."),
        ("Which part of the brain controls walking in a straight line?", "the cerebellum", ["the medulla", "the cerebrum only", "the spinal cord"], "It coordinates balance and posture."),
        ("What happens at a synapse?", "the impulse releases chemicals that start a new impulse in the next neuron", ["the impulse stops forever", "blood flows to the brain", "a hormone is made"], "This makes sure the message travels one way."),
        ("Which hormone causes the heart to beat faster during fear?", "adrenaline", ["insulin", "thyroxine", "growth hormone"], "It also sends more blood to the muscles."),
        ("Which plant hormone makes leaves fall and stops growth?", "abscisic acid", ["auxin", "gibberellin", "cytokinin"], "It is a growth inhibitor."),
        ("What are involuntary actions?", "actions not under our conscious control, such as heartbeat and breathing", ["actions we think about first", "only reflexes in plants", "walking and writing"], "They are controlled by the medulla."),
        ("What happens to the pupil of the eye in bright light?", "it becomes smaller", ["it becomes larger", "it turns red", "it does not change"], "This is a reflex that protects the retina."),
        ("Why are hormones called chemical messengers?", "they are carried by blood to act on target organs", ["they are electric signals", "they travel along nerves", "they stay in the gland"], "Each acts on a specific target."),
        ("Which gland is called the master gland?", "the pituitary gland", ["the thyroid gland", "the adrenal gland", "the pancreas"], "It controls many other glands."),
        ("What is the difference between voluntary and involuntary muscles?", "voluntary muscles move when we decide; involuntary muscles move on their own", ["there is no difference", "voluntary muscles are only in the heart", "involuntary muscles are only in the legs"], "Heart muscle is involuntary."),
        ("What is a stimulus?", "a change in the surroundings that an organism responds to", ["a type of hormone", "a kind of muscle", "a nerve cell"], "Light, heat and touch are stimuli."),
        ("Which gland is both endocrine and exocrine?", "the pancreas", ["the thyroid", "the pituitary", "the adrenal gland"], "It secretes insulin and pancreatic juice."),
        ("Why does a growing shoot bend away from gravity?", "it is negatively geotropic", ["it is positively geotropic", "it needs no light", "it has no auxin"], "Roots are positively geotropic."),
        ("What happens to muscle cells when a message reaches them?", "proteins in the cells change shape so the muscle contracts", ["the cells divide", "the cells release hormones", "the cells die"], "This is how movement happens."),
        ("Which part of the brain is the main thinking part?", "the cerebrum", ["the medulla", "the cerebellum", "the pons"], "It has areas for sensing, thinking and movement."),
        ("Why is blood sugar kept within a narrow range?", "the body needs a steady supply of glucose; too much or too little is harmful", ["sugar is not needed", "sugar is stored in the brain", "sugar causes goitre"], "Insulin brings it down when it rises."),
        ("How does the pollen tube find the ovule?", "it grows towards chemicals from the ovule (chemotropism)", ["it is pulled by gravity", "it follows light", "it is pushed by wind"], "This is a directional growth response."),
        ("Which hormone helps plants grow taller?", "gibberellin", ["abscisic acid", "insulin", "adrenaline"], "Gibberellins promote stem growth."),
        ("What is the function of the sensory neuron in a reflex arc?", "carrying the message from the receptor to the spinal cord", ["carrying the message to the muscle", "joining two muscles", "making hormones"], "The motor neuron carries it to the effector."),
        ("What is the function of the motor neuron in a reflex arc?", "carrying the message from the spinal cord to the effector", ["carrying the message to the brain only", "detecting the stimulus", "storing memories"], "The effector is a muscle or gland.")]


# =================================================================== Chapter 7: how do organisms reproduce?
REPRO = [("Amoeba", "binary fission (in any plane)"), ("Leishmania", "binary fission (in a definite plane)"), ("Plasmodium (malarial parasite)", "multiple fission"),
         ("Hydra", "budding"), ("yeast", "budding"), ("Planaria", "regeneration"), ("Spirogyra", "fragmentation"), ("Rhizopus (bread mould)", "spore formation"),
         ("Bryophyllum", "vegetative propagation from buds on the leaf margin"), ("potato", "vegetative propagation from buds (eyes) on the tuber"),
         ("rose", "vegetative propagation by cutting and grafting"), ("seedless banana", "only vegetative propagation, because it makes no seeds")]
FLOWER = [("the stamen", "the male part, which makes pollen"), ("the anther", "making pollen grains"), ("the stigma", "receiving pollen grains"),
          ("the style", "connecting the stigma to the ovary, through which the pollen tube grows"), ("the ovary", "containing ovules; it becomes the fruit"),
          ("the ovule", "containing the egg cell; it becomes the seed"), ("the sepals", "protecting the flower in the bud stage"), ("the petals", "attracting insects for pollination"),
          ("the plumule", "the part of the embryo that becomes the shoot"), ("the radicle", "the part of the embryo that becomes the root"), ("the cotyledons", "storing food for the embryo"),
          ("the filament", "holding up the anther"), ("the seed coat", "protecting the embryo inside the seed"), ("nectar", "attracting insects with a sugary liquid")]
HUMAN7 = [("the testes", "making sperm and testosterone"), ("the vas deferens", "carrying sperm from the testes towards the urethra"),
          ("the seminal vesicles and prostate gland", "adding fluid that nourishes sperm and helps them move"), ("the ovaries", "making eggs and the hormone oestrogen"),
          ("the oviduct (fallopian tube)", "the place where fertilisation happens"), ("the uterus", "where the embryo implants and grows"),
          ("the placenta", "passing food and oxygen from mother to embryo and removing wastes"), ("the scrotum", "keeping the testes at a lower temperature than the body"),
          ("the urethra in males", "carrying both urine and sperm out of the body"), ("the vagina", "receiving sperm and forming the birth canal"),
          ("the umbilical cord", "connecting the embryo to the placenta"), ("the egg (ovum)", "the female gamete that fuses with a sperm")]
VEG = [("potato", "a stem tuber with buds (eyes)"), ("ginger", "an underground stem (rhizome)"), ("onion", "a bulb"), ("Bryophyllum", "buds on the leaf margins"),
       ("sweet potato", "a root"), ("sugarcane", "a stem cutting"), ("money plant", "a stem cutting"), ("mango (grafted)", "grafting a shoot onto a rooted plant"), ("jasmine", "layering a branch into the soil")]
CONTRA = [("condoms", "a barrier method that also helps prevent sexually transmitted infections"), ("copper-T", "a device placed in the uterus to prevent pregnancy"),
          ("oral pills", "a hormonal method that changes the hormone balance so eggs are not released"), ("vasectomy", "surgery that blocks the vas deferens in males"),
          ("tubectomy", "surgery that blocks the fallopian tubes in females")]
STI = [("gonorrhoea", "bacteria"), ("syphilis", "bacteria"), ("warts", "a virus"), ("HIV-AIDS", "a virus")]


def c_repro(k=None):
    k = k or ch(["contra", "sti"])
    if k == "contra":
        a, b = ch(CONTRA)
        return tq("What is %s?" % a, b, _R[0].sample([x[1] for x in CONTRA if x[1] != b], 3), "%s: %s." % (a[0].upper() + a[1:], b))
    a, b = ch(STI)
    return tq("What causes %s?" % a, b, [x for x in ["bacteria", "a virus", "a fungus", "a protozoan", "a vitamin deficiency"] if x != b][:3], "Gonorrhoea and syphilis are bacterial; warts and HIV-AIDS are viral.")


REP = [("Why is DNA copying important in reproduction?", "it passes the body design to the offspring, with small variations", ["it makes the parent stronger", "it makes energy", "it stops variation"], "Variation helps a species survive changes."),
       ("Why is variation useful for a species?", "some individuals may survive if the environment changes", ["it makes all offspring identical", "it stops reproduction", "it harms the species"], "It is the basis of evolution."),
       ("What is the advantage of vegetative propagation?", "plants grow faster and are exactly like the parent", ["it needs seeds", "it gives more variation", "it is slower"], "It is used for plants that do not make viable seeds."),
       ("What is pollination?", "the transfer of pollen from an anther to a stigma", ["the joining of the sperm and egg", "the growth of a seed", "the falling of leaves"], "Wind, water and insects carry pollen."),
       ("What is the difference between self-pollination and cross-pollination?", "self: pollen goes to a stigma of the same flower or plant; cross: to another plant", ["self needs insects, cross does not", "there is no difference", "cross happens only in water"], "Cross-pollination gives more variation."),
       ("What happens after fertilisation in a flower?", "the ovule becomes a seed and the ovary becomes a fruit", ["the petals become seeds", "the stigma becomes a fruit", "the anther becomes the seed"], "The zygote grows into the embryo."),
       ("What is germination?", "the growth of a seed into a seedling", ["the making of pollen", "the fall of a fruit", "the drying of a seed"], "It needs water, air and warmth."),
       ("What is puberty?", "the age when reproductive organs mature and sex hormones are released", ["the time of birth", "old age", "the first year of life"], "New hair growth and voice changes happen."),
       ("Why do the walls of the uterus thicken every month?", "to prepare to receive a fertilised egg", ["to make the egg", "to make hormones only", "to store food for the mother"], "If there is no fertilisation, the lining breaks down (menstruation)."),
       ("What is the advantage of sexual reproduction over asexual reproduction?", "it gives more variation in the offspring", ["it is faster", "it needs only one parent", "it makes identical copies"], "Variation helps a species adapt."),
       ("Why is prenatal sex determination banned in India?", "it is misused for female foeticide, harming the sex ratio", ["it is not accurate", "it costs too much", "it is painful"], "A healthy society needs a balanced sex ratio."),
       ("What is a zygote?", "the cell formed when a male and female gamete fuse", ["a male gamete", "an unfertilised egg", "a spore"], "It divides to form the embryo."),
       ("How does Planaria regenerate?", "each cut piece grows into a complete organism using specialised cells", ["it makes seeds", "it makes spores", "it buds from the head only"], "Not all organisms can do this."),
       ("What are spores?", "small structures with a thick wall that can survive harsh conditions and grow into new organisms", ["male gametes", "seeds of flowering plants", "dead cells"], "Rhizopus makes spores in sporangia."),
       ("Why does the number of chromosomes stay the same from parents to offspring?", "gametes have half the number of chromosomes", ["gametes have double the number", "chromosomes are not passed on", "the zygote loses chromosomes"], "Fusion restores the full number."),
       ("What is the function of the pollen tube?", "carrying the male gamete to the ovule", ["carrying water", "making nectar", "protecting the seed"], "It grows down through the style."),
       ("Why are flowers called reproductive parts?", "they contain the male and female reproductive organs", ["they make food", "they absorb water", "they carry water"], "Stamens and pistils are inside the flower."),
       ("What is a unisexual flower?", "a flower with either stamens or a pistil, such as papaya or watermelon", ["a flower with both stamens and pistil", "a flower with no petals", "a flower that never opens"], "Hibiscus and mustard are bisexual."),
       ("How long does a human baby develop in the uterus?", "about nine months", ["about one month", "about three years", "about two weeks"], "Birth happens by rhythmic contraction of the uterus muscles."),
       ("What is tissue culture?", "growing new plants from a few cells of a plant in a nutrient medium", ["growing plants in water only", "growing seeds in soil", "cutting the stem"], "It is used for ornamental plants such as orchids."),
       ("Why does a fertilised egg divide many times?", "to form the embryo with many cells", ["to make pollen", "to make gametes", "to stop growth"], "Cells then specialise to form organs."),
       ("What is menstruation?", "the shedding of the thickened lining of the uterus when there is no fertilisation", ["the release of a sperm", "the making of milk", "the growth of a baby"], "It happens about every 28 days."),
       ("Why does reproduction need energy?", "making new cells and gametes uses energy", ["it releases energy", "it is a passive process", "it needs no materials"], "Organisms grow and repair too."),
       ("What is the number of chromosomes in a human gamete?", "23", ["46", "92", "12"], "Body cells have 46 (23 pairs)."),
       ("What is the number of chromosomes in a human body cell?", "46", ["23", "92", "44"], "The zygote gets 23 from each parent."),
       ("Why can't all organisms reproduce by regeneration?", "only simple organisms have specialised cells that can make every type of tissue", ["regeneration needs seeds", "it is too fast", "it needs two parents"], "Complex animals cannot regrow a whole body.")]


# =================================================================== Chapter 8: heredity
CROSS = [("TT × tt (tall × short pea plants)", "are tall", F(1)), ("Tt × Tt", "are tall", F(3, 4)), ("Tt × Tt", "are short", F(1, 4)), ("Tt × tt", "are short", F(1, 2)),
         ("Tt × Tt", "are pure tall (TT)", F(1, 4)), ("Tt × Tt", "are hybrid tall (Tt)", F(1, 2)), ("RRYY × rryy, F₂ (round yellow × wrinkled green)", "are round and yellow", F(9, 16)),
         ("RRYY × rryy, F₂", "are wrinkled and green", F(1, 16)), ("RRYY × rryy, F₂", "are round and green", F(3, 16)), ("RrYy × RrYy", "are wrinkled and yellow", F(3, 16)),
         ("TT × Tt", "are short", F(0)), ("RR × rr", "are round (F₁)", F(1))]


TRAITS = [("tall", "short", "T"), ("round seeds", "wrinkled seeds", "R"), ("yellow seeds", "green seeds", "Y"), ("violet flowers", "white flowers", "V"),
          ("green pods", "yellow pods", "G"), ("axial flowers", "terminal flowers", "A"), ("inflated pods", "constricted pods", "I")]
MONO = [("XX", "xx"), ("Xx", "Xx"), ("Xx", "xx"), ("XX", "Xx")]


def cross_q():
    """(question, fraction): a random monohybrid or dihybrid pea cross"""
    R = _R[0]
    if R.random() < 0.6:
        d, r, L = R.choice(TRAITS)
        p1, p2 = R.choice(MONO)
        g1, g2 = p1.replace("X", L).replace("x", L.lower()), p2.replace("X", L).replace("x", L.lower())
        kids = [a + b for a in g1 for b in g2]
        ask, fn = R.choice([("show %s" % d, lambda k: L in k), ("show %s" % r, lambda k: L not in k), ("are pure %s (%s%s)" % (d, L, L), lambda k: k == L + L),
                            ("are hybrid (%s%s)" % (L, L.lower()), lambda k: sorted(k) == sorted(L + L.lower()))])
        p = F(sum(1 for k in kids if fn(k)), 4)
        return ("In pea plants, %s (%s) is dominant over %s (%s). A %s plant (%s) is crossed with a %s plant (%s)." % (d, L, r, L.lower(), d if L in g1 else r, g1, d if L in g2 else r, g2)), ask, p
    (d1, r1, L1), (d2, r2, L2) = R.sample(TRAITS, 2)
    ph = R.choice([("%s and %s" % (d1, d2), F(9, 16)), ("%s and %s" % (d1, r2), F(3, 16)), ("%s and %s" % (r1, d2), F(3, 16)), ("%s and %s" % (r1, r2), F(1, 16))])
    return ("Pure-breeding pea plants with %s and %s are crossed with plants with %s and %s. The F₁ plants are self-pollinated to give F₂." % (d1, d2, r1, r2)), "show %s" % ph[0], ph[1]


def c_heredity(k=None):
    k = k or ch(["prob", "count", "sex"])
    alls = [F(0), F(1, 16), F(3, 16), F(1, 4), F(1, 2), F(9, 16), F(3, 4), F(1)]
    if k == "sex":
        rows = [("What is the chance that a baby is a boy?", F(1, 2)), ("A couple has two daughters. What is the chance that their third child is a girl?", F(1, 2)),
                ("What fraction of a father's sperm carry a Y chromosome?", F(1, 2)), ("What fraction of a mother's eggs carry an X chromosome?", F(1))]
        q, p = ch(rows)
        return tq(q, fr(p), [fr(x) for x in [F(1, 4), F(3, 4), F(0), F(1), F(1, 2)] if x != p][:3], "Mothers give X; fathers give X or Y with equal chance, so each child has a ½ chance of being a boy.")
    c, ph, p = cross_q()
    if k == "count":
        n = ch([160, 320, 400, 480, 800, 960, 1000, 1200, 1600, 2000])
        if p in (0, 1):
            return None
        if (p * n).denominator != 1:
            return None
        a = int(p * n)
        return nq("%s If %s offspring are produced, about how many %s?" % (c, "{:,}".format(n), ph.replace("show ", "will show ").replace("are ", "will be ")), a, [n - a, n // 2 if a != n // 2 else n // 4, int(n * F(1, 16)) if a != int(n * F(1, 16)) else n * 3 // 16], "",
                  "Expected fraction %s; %s × %s = <b>%s</b>." % (fr(p), fr(p), "{:,}".format(n), "{:,}".format(a)))
    return tq("%s What fraction of the offspring %s?" % (c, ph), fr(p), [fr(x) for x in _R[0].sample([x for x in alls if x != p], 3)], "Use a Punnett square: %s." % fr(p))


HER = [("What is a gene?", "a section of DNA that carries information for a protein and a trait", ["a whole chromosome", "a cell", "a hormone"], "Genes are on chromosomes."),
       ("Why did Mendel choose pea plants?", "they have clear contrasting traits and are easy to grow and cross", ["they have no traits", "they grow only in winter", "they cannot be crossed"], "Tall and short, round and wrinkled seeds, and so on."),
       ("What is a dominant trait?", "a trait that shows in the F₁ generation even when only one copy is present", ["a trait that never shows", "a trait only in males", "a trait that skips generations always"], "Tallness is dominant over shortness in peas."),
       ("What is a recessive trait?", "a trait that shows only when both copies are the same", ["a trait that always shows", "a trait from the mother only", "a new trait"], "Short pea plants are tt."),
       ("What ratio of tall to short plants did Mendel get in the F₂ generation of a monohybrid cross?", "3 : 1", ["1 : 1", "9 : 3 : 3 : 1", "1 : 2"], "TT, Tt, Tt and tt."),
       ("What ratio did Mendel get in the F₂ generation of a dihybrid cross?", "9 : 3 : 3 : 1", ["3 : 1", "1 : 2 : 1", "1 : 1 : 1 : 1"], "This shows independent inheritance of two traits."),
       ("What does a dihybrid cross show?", "two traits are inherited independently", ["traits always stay together", "one trait only", "traits come from the mother only"], "New combinations appear in F₂."),
       ("Which chromosomes do human females have?", "XX", ["XY", "YY", "XO"], "Males have XY."),
       ("Who decides the sex of a human child?", "the father, depending on whether his sperm carries X or Y", ["the mother", "the environment", "the grandparents"], "The mother always gives an X."),
       ("How is sex decided in some reptiles?", "by the temperature at which the eggs are kept", ["by X and Y chromosomes", "by the food", "by the father only"], "In some turtles warmer eggs become females."),
       ("How do traits get expressed?", "genes control making proteins, such as enzymes, that produce the trait", ["by hormones only", "by the environment only", "by blood type only"], "For example, an enzyme for a plant growth hormone controls height."),
       ("What is the F₁ generation?", "the first generation of offspring from a cross", ["the parents", "the grandparents", "the second set of offspring"], "Self-crossing F₁ gives F₂."),
       ("What is a hybrid?", "an organism with two different alleles for a trait (such as Tt)", ["a pure breeding plant", "a plant with no genes", "a type of mutation"], "It shows the dominant trait."),
       ("How many sets of genes does each child get from its parents?", "two: one from each parent", ["one from the mother only", "four", "one from the father only"], "Each germ cell has one set.")]


# =================================================================== Chapter 13: our environment
CHAINS = [["grass", "grasshopper", "frog", "snake", "eagle"], ["phytoplankton", "zooplankton", "small fish", "large fish"], ["grass", "deer", "lion"],
          ["grass", "rabbit", "fox"], ["plants", "caterpillar", "bird", "hawk"], ["algae", "insect larva", "fish", "kingfisher"], ["grass", "goat", "human"],
          ["grass", "insect", "lizard", "snake"], ["plants", "aphid", "ladybird beetle", "sparrow"], ["paddy plants", "rat", "snake", "hawk"],
          ["phytoplankton", "small crustaceans", "fish", "seal"], ["leaves", "earthworm", "hen", "fox"], ["grass", "cow", "tiger"]]
WASTE = [("vegetable peels", True), ("paper", True), ("cotton cloth", True), ("leather", True), ("wood", True), ("cow dung", True), ("leaves", True), ("tea leaves", True),
         ("plastic bags", False), ("glass bottles", False), ("aluminium cans", False), ("DDT (a pesticide)", False), ("polythene", False), ("styrofoam cups", False), ("nylon", False), ("ball-point pen refills", False)]
LEVEL = ["producers (first trophic level)", "primary consumers (second trophic level)", "secondary consumers (third trophic level)", "tertiary consumers (fourth trophic level)", "quaternary consumers (fifth trophic level)"]


def c_env(k=None):
    k = k or ch(["ten", "level", "waste", "back"])
    if k == "ten":
        e = ch([1000, 2000, 5000, 10000, 20000, 50000, 100000])
        n = ch([2, 3, 4])
        val = e / 10 ** (n - 1)
        return nq("Producers in a food chain hold %s kJ of energy. Using the 10%% law, how much energy reaches the %s level?" % ("{:,}".format(e), ["", "first", "second", "third", "fourth"][n]), val,
                  [e / 10 ** n, e / 10 ** (n - 2) if n > 2 else e / 2, e * 0.1 * n], " kJ", "Only about 10%% passes to the next level: %s × (0.1)<sup>%d</sup> = <b>%s kJ</b>." % ("{:,}".format(e), n - 1, nf(val)))
    if k == "back":
        e = ch([10, 20, 50, 100, 200])
        n = ch([2, 3])
        return nq("A %s in a food chain gets %d kJ of energy. Using the 10%% law, how much energy did the producers hold?" % (["", "", "primary consumer", "secondary consumer"][n], e), e * 10 ** (n - 1),
                  [e * 10 ** n, e * 10 ** (n - 2) * 5 if n > 2 else e * 5, e + 10 * (n - 1)], " kJ", "Multiply by 10 for each step back: <b>%s kJ</b>." % "{:,}".format(e * 10 ** (n - 1)))
    if k == "which":
        c = ch(CHAINS)
        i = _R[0].randrange(len(c))
        return tq("In the food chain %s, which organism is the %s?" % (" → ".join(c), LEVEL[i].split(" (")[0][:-1]), c[i], [x for x in c if x != c[i]][:3] if len(c) >= 4 else [x for x in c if x != c[i]] + ["the Sun"],
                  "Count from the producer: level %d is %s." % (i + 1, c[i]))
    if k == "level":
        c = ch(CHAINS)
        i = _R[0].randrange(len(c))
        q = "In the food chain %s, which trophic level is the %s?" % (" → ".join(c), c[i])
        return tq(q, LEVEL[i], _R[0].sample([x for j, x in enumerate(LEVEL) if j != i and j < len(c) + 1], 3), "Count from the producer: %s is at level %d." % (c[i], i + 1))
    w, bio = ch(WASTE)
    return tq("Is %s biodegradable or non-biodegradable?" % w, "biodegradable" if bio else "non-biodegradable",
              ["non-biodegradable" if bio else "biodegradable", "neither: it is a gas", "it depends on its colour"], "Biodegradable substances are broken down by bacteria and other decomposers; non-biodegradable ones stay for a long time.")


ENV = [("What is an ecosystem?", "all living things in an area together with the non-living parts of their environment", ["only the animals in a forest", "only plants", "a single food chain"], "Ponds, forests and gardens are ecosystems."),
       ("Why are decomposers important?", "they break down dead organisms and return nutrients to the soil", ["they make food from sunlight", "they eat only plants", "they pollute the air"], "Bacteria and fungi are decomposers."),
       ("What is biological magnification?", "the build-up of harmful chemicals at each higher trophic level", ["the growth of plants", "the increase of energy along a food chain", "enlarging an image of a cell"], "Humans at the top get the highest amount of pesticides."),
       ("Why do food chains usually have only three or four trophic levels?", "only about 10% of energy passes on, so little is left for higher levels", ["animals cannot eat more than three times", "plants stop growing", "there are no more animals"], "Energy flow is unidirectional."),
       ("Why is the flow of energy in an ecosystem unidirectional?", "energy passed to a higher level does not come back to a lower level", ["energy goes back to the sun", "plants eat animals", "energy is recycled"], "Nutrients are recycled; energy is not."),
       ("What does ozone in the upper atmosphere do?", "it shields the Earth from harmful ultraviolet radiation from the Sun", ["it makes rain", "it heats the Earth", "it is a poisonous gas everywhere"], "At ground level ozone is a poison."),
       ("What has caused the depletion of the ozone layer?", "chlorofluorocarbons (CFCs) used in refrigerators and sprays", ["carbon dioxide from breathing", "oxygen from plants", "water vapour"], "In 1987 UNEP got countries to freeze CFC production."),
       ("How is ozone formed?", "UV radiation splits O₂ into atoms, which combine with O₂ to form O₃", ["by burning coal", "by plants in the soil", "by the reaction of nitrogen and water"], "O₂ → O + O; O + O₂ → O₃."),
       ("What is a food web?", "many food chains linked together", ["one food chain", "a group of producers", "the energy of the Sun"], "Organisms eat more than one kind of food."),
       ("Why is a garden an artificial ecosystem?", "it is made and looked after by people", ["it has no living things", "it is too small", "it has no soil"], "Crop fields are artificial; forests are natural."),
       ("What are the problems of disposing of non-biodegradable waste?", "it stays in the environment and can harm organisms", ["it rots quickly", "it gives food to plants", "it disappears in a week"], "Reduce, reuse and recycle."),
       ("Which organisms are producers?", "green plants and blue-green algae", ["all animals", "fungi", "bacteria that decay waste"], "They make food by photosynthesis."),
       ("What happens if all the decomposers in an ecosystem die?", "dead matter piles up and nutrients are not returned to the soil", ["plants grow faster", "there is no change", "animals live longer"], "The ecosystem would stop working."),
       ("What is the best way to dispose of kitchen waste?", "make compost from it", ["burn it with plastic", "throw it in a river", "put it in plastic bags in a drain"], "Composting is a biodegradable process."),
       ("Why should we use cloth or jute bags instead of plastic bags?", "they are biodegradable or reusable and cause less pollution", ["they are cheaper to make", "plastic is good for soil", "plastic bags rot quickly"], "Plastic can block drains and harm animals."),
       ("Which of these is a decomposer?", "a mushroom", ["a frog", "grass", "a deer"], "Fungi and bacteria are decomposers."),
       ("What are the abiotic components of an ecosystem?", "non-living parts such as air, water, soil and temperature", ["plants only", "animals only", "decomposers only"], "Biotic components are living."),
       ("What is the original source of energy for almost all ecosystems?", "the Sun", ["the soil", "decomposers", "water"], "Producers capture about 1% of sunlight falling on leaves."),
       ("Which disposal method reduces the volume of non-biodegradable waste in a useful way?", "recycling", ["throwing it in a river", "burying it in farmland", "burning plastic in the open"], "Recycling saves raw materials too.")]


def UNITS10b():
    W, N = "World of Living", "Natural Resources"
    b = {n: once_maker(v) for n, v in [("life", LIFE), ("ctrl", CTRL), ("rep", REP), ("her", HER), ("env", ENV)]}
    org = pairs(ORGAN5, "What is the function of %s?", "Which part of the body or plant does this job: %s?")
    brain = pairs(BRAIN, "What is the job of %s?", "Which part of the nervous system or its protection does this: %s?")
    neur = pairs(NEURON, "What is the job of %s?", "Which part does this job: %s?")
    plant = pairs(PLANT6, "What is the role of the plant hormone %s?", "Which plant hormone is responsible for %s?")
    trop = pairs(TROP, "What is the growth response of a plant part to %s called?", "Which stimulus causes %s?")
    rep = pairs(REPRO, "How does %s reproduce?", "Which organism reproduces by %s?")
    flo = pairs(FLOWER, "What is the job of %s in a flower or seed?", "Which part of a flower or seed does this: %s?")
    veg = pairs(VEG, "Which part is used to grow new %s plants?", "Which plant is grown from %s?")
    hum = pairs(HUMAN7, "What is the job of %s?", "Which part of the human reproductive system does this: %s?")
    return [
        U(5, "life-processes", 5, W,
          "Life processes: 'living being', basic concept of nutrition, respiration, transport and excretion in plants and animals.",
          "Life Processes", "life processes",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 5: nutrition, photosynthesis, digestion, respiration, the heart and blood, transport in plants and excretion. 100 questions with answers.",
          "Nutrition, respiration, transport and excretion keep us alive.", "Glucose → pyruvate → CO₂ + water (with oxygen).",
          "<p>Living things need energy and materials. Plants make food by photosynthesis (CO₂ + water → glucose + O₂ with sunlight and chlorophyll); animals take in food and digest it with enzymes such as amylase, pepsin, trypsin and lipase. Respiration releases energy from glucose: with oxygen it gives CO₂ and water; without oxygen yeast makes ethanol and muscles make lactic acid.</p>"
          "<p>Humans have double circulation: the four-chambered heart pumps blood to the lungs and to the body. Plants move water in xylem and food in phloem. Kidneys filter blood in nephrons to make urine.</p>",
          [("Where is protein digestion started?", ["pepsin works in acid"], "the stomach"),
           ("Products of anaerobic respiration in yeast?", ["pyruvate without oxygen"], "ethanol and carbon dioxide")],
          ["Saying plants do not respire.", "Mixing up xylem (water) and phloem (food).", "Thinking the pulmonary vein carries deoxygenated blood."],
          [("Why is diffusion not enough for oxygen in large animals?", "Diffusion is too slow over long distances, so large animals need lungs and a circulatory system."),
           ("What is the role of the nephron?", "It filters the blood, reabsorbs useful substances and makes urine from the waste.")],
          lambda: [("Nutrition and digestion", [(K(c_life, "enz", "nut"), 12), (b["life"], 8)]), ("Organs and their jobs", [(org, 20)]), ("Respiration and the heart", [(K(c_life, "resp", "heart"), 9), (b["life"], 5), (org, 6)]),
                   ("Transport and excretion", [(org, 14), (b["life"], 6)]), ("Applying ideas", [(b["life"], 4), (org, 11), (K(c_life, "enz", "nut"), 5)])]),
        U(6, "control-and-coordination", 6, W,
          "Control and co-ordination in animals and plants: tropic movements in plants; introduction of plant hormones; control and co-ordination in animals: nervous system; voluntary, involuntary and reflex action; chemical co-ordination: animal hormones.",
          "Control and Coordination", "control and coordination",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 6: neurons, reflex arcs, parts of the brain, plant hormones and tropisms, and human hormones and glands. 100 questions with answers.",
          "Nerves give fast messages; hormones give slow, lasting ones.", "Reflex: receptor → sensory neuron → spinal cord → motor neuron → effector.",
          "<p>In animals, receptors detect stimuli and neurons carry electrical impulses to the brain or spinal cord, which send messages to effectors (muscles and glands). Reflex actions are quick and controlled by the spinal cord. The cerebrum handles thinking, the cerebellum balance, and the medulla involuntary actions.</p>"
          "<p>Hormones are chemical messengers carried in the blood: insulin lowers blood sugar, thyroxine controls metabolism, adrenaline prepares for emergencies. Plants respond by growth (tropisms) controlled by hormones such as auxin, gibberellins, cytokinins and abscisic acid.</p>",
          [("A shoot bends to light. Which hormone?", ["auxin moves to the shaded side"], "auxin"),
           ("Which gland makes insulin?", ["it controls blood sugar"], "the pancreas")],
          ["Thinking reflex actions are controlled by the cerebrum.", "Mixing up phototropism and geotropism.", "Saying hormones travel along nerves."],
          [("How do plants respond without a nervous system?", "By hormones that change growth (tropisms) and by quick changes of water in cells, as in the touch-me-not plant."),
           ("Why is the spinal cord important in reflex actions?", "It processes the message quickly and sends a response without waiting for the brain.")],
          lambda: [("Neurons and reflex action", [(neur, 10), (b["ctrl"], 10)]), ("The human brain", [(brain, 14), (b["ctrl"], 4), (trop, 2)]),
                   ("Plant hormones and tropisms", [(plant, 8), (trop, 7), (b["ctrl"], 5)]), ("Hormones and glands", [(K(c_ctrl, "gland", "hfunc"), 20)]),
                   ("Hormone problems and applying ideas", [(K(c_ctrl, "def"), 4), (K(c_ctrl, "gland", "hfunc"), 6), (b["ctrl"], 6), (brain, 4)])]),
        U(7, "how-do-organisms-reproduce", 7, W,
          "Reproduction in animals and plants (asexual and sexual), reproductive health – need and methods of family planning, safe sex vs HIV/AIDS, child bearing and women's health.",
          "How do Organisms Reproduce?", "how organisms reproduce",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 7: fission, budding, regeneration, spores, vegetative propagation, parts of a flower, human reproduction and reproductive health. 100 questions with answers.",
          "Asexual: one parent, copies. Sexual: two parents, variation.", "Ovule → seed, ovary → fruit after fertilisation.",
          "<p>In asexual reproduction one parent gives offspring almost identical to itself: fission (Amoeba, Leishmania, Plasmodium), budding (Hydra, yeast), regeneration (Planaria), fragmentation (Spirogyra), spores (Rhizopus) and vegetative propagation (potato, Bryophyllum).</p>"
          "<p>In sexual reproduction, gametes with half the chromosomes fuse to form a zygote, giving variation. In flowers, pollen from the anther reaches the stigma, a pollen tube carries the male gamete to the ovule, and after fertilisation the ovule becomes the seed and the ovary the fruit.</p>",
          [("How does Plasmodium reproduce?", ["it divides into many cells at once"], "multiple fission"),
           ("After fertilisation, what does the ovary become?", ["the ovules become seeds inside it"], "the fruit")],
          ["Mixing up pollination and fertilisation.", "Thinking yeast reproduces by fission.", "Saying the ovary becomes the seed."],
          [("Why is variation important?", "It helps some individuals survive if the environment changes, so the species does not die out."),
           ("Where does fertilisation take place in humans?", "In the oviduct (fallopian tube); the embryo then implants in the uterus.")],
          lambda: [("Asexual reproduction", [(rep, 20)]), ("Flowers and seeds", [(flo, 20)]), ("Human reproductive system", [(hum, 14), (b["rep"], 6)]),
                   ("Reproductive health", [(c_repro, 8), (b["rep"], 12)]), ("Vegetative propagation and applying ideas", [(veg, 12), (b["rep"], 4), (rep, 2), (flo, 2)])]),
        U(8, "heredity", 8, W,
          "Heredity: Mendel's contribution – laws for inheritance of traits; sex determination: brief introduction.",
          "Heredity", "heredity",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 8: Mendel's experiments, dominant and recessive traits, monohybrid and dihybrid crosses, Punnett squares and sex determination. 100 questions with answers.",
          "Monohybrid F₂: 3 : 1. Dihybrid F₂: 9 : 3 : 3 : 1.", "The father's X or Y decides the sex of the child.",
          "<p>Each trait is controlled by a pair of genes, one from each parent. A dominant trait (T) shows even with one copy; a recessive trait (t) shows only in tt. Crossing Tt × Tt gives TT : Tt : tt = 1 : 2 : 1, so tall : short = 3 : 1.</p>"
          "<p>A dihybrid cross (two traits) gives 9 : 3 : 3 : 1 in F₂, showing that traits are inherited independently. In humans, mothers give an X chromosome; fathers give X or Y, so each child has a ½ chance of being a boy.</p>",
          [("Tt × Tt: fraction short?", ["only tt is short", "1 box in 4"], "¼"),
           ("1,600 F₂ plants from a dihybrid cross: how many wrinkled green?", ["1/16 × 1,600"], "100")],
          ["Thinking the mother decides the sex of the child.", "Using 3 : 1 for a dihybrid cross.", "Thinking a recessive trait is lost forever."],
          [("What did Mendel's dihybrid cross show?", "That two different traits are inherited independently of each other."),
           ("Why do children look like their parents but not exactly the same?", "They get half their genes from each parent, in new combinations.")],
          lambda: [("Mendel's laws", [(b["her"], 10), (K(c_heredity, "prob"), 10)]), ("Punnett squares", [(K(c_heredity, "prob"), 20)]), ("Counting offspring", [(K(c_heredity, "count"), 20)]),
                   ("Sex determination", [(K(c_heredity, "sex"), 4), (K(c_heredity, "count"), 16)]), ("Mixed problems", [(K(c_heredity, "count"), 10), (K(c_heredity, "prob"), 6), (K(c_heredity, "prob"), 4)])]),
        U(13, "our-environment", 13, N,
          "Our environment: eco-system, environmental problems, ozone depletion, waste production and their solutions; biodegradable and non-biodegradable substances.",
          "Our Environment", "our environment",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 13: ecosystems, food chains and trophic levels, the 10% law, biological magnification, ozone depletion and waste management. 100 questions with answers.",
          "Only about 10% of energy passes to the next level.", "Energy flows one way; nutrients are recycled.",
          "<p>An ecosystem is the living organisms of an area together with its non-living parts. Producers make food; consumers eat them; decomposers return nutrients to the soil. Each step in a food chain is a trophic level.</p>"
          "<p>Only about 10% of the energy at one level reaches the next (the 10% law), so food chains are short. Harmful chemicals build up along a food chain (biological magnification). CFCs have thinned the ozone layer, which protects us from UV radiation. Biodegradable waste is broken down by decomposers; non-biodegradable waste stays for a long time.</p>",
          [("Producers hold 10,000 kJ. Energy for secondary consumers?", ["10,000 → 1,000 → 100"], "100 kJ"),
           ("In grass → deer → lion, the deer is?", ["second level"], "a primary consumer")],
          ["Thinking energy is recycled in an ecosystem.", "Counting trophic levels from the top.", "Calling plastic biodegradable."],
          [("What is the 10% law?", "Only about 10% of the energy at one trophic level is passed on to the next; the rest is used or lost as heat."),
           ("Why is the ozone layer important?", "It absorbs harmful ultraviolet radiation from the Sun, which can cause skin cancer.")],
          lambda: [("Food chains and trophic levels", [(K(c_env, "level"), 20)]), ("The 10% law", [(K(c_env, "ten", "back"), 20)]), ("Ecosystems and decomposers", [(b["env"], 10), (K(c_env, "which"), 10)]),
                   ("Waste and the ozone layer", [(K(c_env, "waste"), 14), (b["env"], 4), (K(c_env, "ten"), 2)]), ("Applying ideas", [(K(c_env, "ten", "back"), 10), (K(c_env, "which", "level"), 10)])]),
    ]
