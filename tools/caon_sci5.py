# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 5 (B Human Organ Systems, C Properties of and Changes in Matter,
D Forces Acting on Structures, E Conservation of Energy and Resources). Built by caon_sci.build."""
from caon_sci import CU, tq

SG5R, UK6C, UK8B = "gen_sg_science_p5_respiratory_and_circulatory_systems", "gen_uk_science_y6_the_circulatory_system", "gen_uk_science_y8_breathing_and_gas_exchange"
US6B, UK4D, SG4D = "gen_us_science_g6_body_systems", "gen_uk_science_y4_the_digestive_system", "gen_sg_science_p4_digestive_system"
UK3K, UK6D, UK9H = "gen_uk_science_y3_skeletons_and_muscles", "gen_uk_science_y6_diet_exercise_and_lifestyle", "gen_uk_science_y9_health_and_drugs"
UK3N, US4S = "gen_uk_science_y3_food_and_nutrition", "gen_us_science_g4_senses_and_the_brain"
UK4M, US5P, US5C = "gen_uk_science_y4_solids_liquids_and_gases", "gen_us_science_g5_properties_of_materials", "gen_us_science_g5_physical_and_chemical_changes"
UK5R, AU6R, SG4M = "gen_uk_science_y5_reversible_and_irreversible_changes", "gen_au_science_y6_reversible_and_irreversible_changes", "gen_sg_science_p4_matter"
US5M, UK4S = "gen_us_science_g5_matter_is_made_of_particles", "gen_uk_science_y4_changes_of_state"
US3F, SG6F, UK7F = "gen_us_science_g3_balanced_and_unbalanced_forces", "gen_sg_science_p6_forces_and_their_effects", "gen_uk_science_y7_forces"
US2B, SG2P = "gen_us_science_g2_building_with_small_pieces", "gen_sg_science_s2_forces_and_pressure"
US4R, US4C, SG6E = "gen_us_science_g4_energy_resources", "gen_us_science_g4_energy_conversions", "gen_sg_science_p6_energy_forms_and_conversion"
US5E, US7N, AU9C = "gen_us_science_g5_protecting_earths_resources", "gen_us_science_g7_natural_resources", "gen_au_science_y9_conservation_of_energy_and_efficiency"
UK8E = "gen_uk_science_y8_energy_and_power"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def L(lead, *xs):
    return "<p><b>%s</b></p><ul>%s</ul>" % (lead, ul(*xs))


def s_resp(X):
    pool = X.pool([
        ("Which organ pumps blood around the body?", "the heart", ["the lungs", "the stomach", "the liver"], "The heart is a muscle that pumps blood."),
        ("Where does oxygen pass into the blood?", "in the lungs", ["in the stomach", "in the heart", "in the kidneys"], "Tiny air sacs in the lungs pass oxygen to the blood."),
        ("Which gas do we breathe out more of than we breathe in?", "carbon dioxide", ["oxygen", "nitrogen only", "helium"], "Cells make carbon dioxide as waste."),
        ("What do blood vessels called arteries do?", "carry blood away from the heart", ["carry air to the lungs", "carry food to the stomach", "carry blood toward the heart only"], "Arteries carry blood away; veins bring it back."),
        ("What do veins do?", "carry blood back to the heart", ["carry blood away from the heart", "carry air", "digest food"], "Veins return blood to the heart."),
        ("What is the job of the diaphragm?", "It moves down to help pull air into the lungs.", ["It pumps blood.", "It digests food.", "It filters the blood."], "The diaphragm is a muscle under the lungs."),
        ("Why does your heart beat faster when you run?", "Your muscles need more oxygen, so blood must flow faster.", ["Your heart gets smaller.", "Your lungs stop working.", "Your blood gets colder."], "Exercise increases heart rate."),
        ("Which organ systems work together to get oxygen to your muscles?", "the respiratory and circulatory systems", ["the digestive and skeletal systems", "the nervous system only", "the skin only"], "Lungs take in oxygen; blood carries it."),
        ("What path does air take into the lungs?", "nose or mouth → windpipe (trachea) → bronchi → lungs", ["mouth → stomach → lungs", "nose → heart → lungs", "lungs → windpipe → nose"], "Air travels down the windpipe."),
        ("How does smoking harm the respiratory system?", "It damages the lungs so they take in less oxygen.", ["It makes the lungs bigger and healthier.", "It only affects the teeth.", "It has no effect."], "Smoke damages the air sacs."),
        ("What does an asthma inhaler do?", "It opens up the airways so air can flow more easily.", ["It cools the heart.", "It helps digest food.", "It makes bones stronger."], "Medical technology helps people breathe."),
        ("Why do doctors use a stethoscope?", "to listen to the heart and lungs", ["to look at bones", "to measure height", "to test eyesight"], "Doctors listen for healthy sounds."),
    ])
    return [
        ("The respiratory system", [(pool, 4), (X.gen(UK8B, "g_job"), 6), (X.gen(UK8B, "g_path"), 5), (X.gen(UK8B, "g_mech"), 5)]),
        ("The circulatory system", [(X.gen(UK6C, "g_part"), 7), (X.gen(SG5R, "g_func"), 6), (X.gen(UK6C, "g_loop"), 3), (pool, 4)]),
        ("Working together", [(X.gen(SG5R, "g_carry"), 5), (X.gen(SG5R, "g_path"), 4), (X.gen(UK6C, "g_oxy"), 4), (X.B(SG5R, "B1"), 4), (pool, 3)]),
        ("Heart rate and exercise", [(X.gen(UK6C, "g_pulse", n=5), 5), (X.gen(UK6C, "g_ex", n=5), 5), (X.gen(SG5R, "g_rate"), 4), (X.gen(SG5R, "g_recover"), 3), (X.gen(UK8B, "g_rate", n=3), 3)]),
        ("Keeping lungs and heart healthy", [(X.B(SG5R, "B4"), 5), (X.B(UK6C, "B5"), 4), (X.B(SG5R, "B5"), 4), (X.gen(UK6C, "g_avg", n=4), 4), (pool, 3)]),
    ]


def s_dig(X):
    pool = X.pool([
        ("Which organ system breaks food down so the body can use it?", "the digestive system", ["the respiratory system", "the skeletal system", "the nervous system"], "Digestion breaks food into nutrients."),
        ("Which organ system holds the body up and protects organs?", "the skeletal system", ["the digestive system", "the circulatory system", "the respiratory system"], "The skull protects the brain; ribs protect the heart and lungs."),
        ("Which organ system sends messages between the brain and the body?", "the nervous system", ["the digestive system", "the skeletal system", "the excretory system"], "Nerves carry signals."),
        ("What do the kidneys do?", "filter waste from the blood to make urine", ["pump blood", "digest proteins", "breathe air"], "The kidneys are part of the excretory system."),
        ("Where are most nutrients absorbed into the blood?", "the small intestine", ["the mouth", "the esophagus", "the large intestine"], "The small intestine is long and lined with villi."),
        ("What does the large intestine mainly do?", "absorbs water from undigested food", ["makes saliva", "pumps food up", "makes bile"], "Water returns to the body."),
        ("Muscles work with which system to move the body?", "the skeletal system", ["the respiratory system", "the excretory system", "the digestive system"], "Muscles pull on bones."),
        ("What is an organ?", "a body part made of tissues that does a special job", ["a single cell", "a kind of food", "a type of blood vessel only"], "The heart, lungs and stomach are organs."),
        ("Which is the largest organ of the body?", "the skin", ["the heart", "the stomach", "the lungs"], "Skin protects the body."),
        ("Which food group helps build strong bones?", "milk and alternatives with calcium", ["candy", "pop", "chips"], "Calcium builds bones."),
        ("Why do we need fibre in our food?", "It helps food move through the intestines.", ["It makes blood red.", "It helps us see in the dark.", "It builds teeth."], "Fibre is found in vegetables and whole grains."),
        ("Canada's Food Guide suggests filling half your plate with which foods?", "vegetables and fruits", ["candy and desserts", "meat only", "bread only"], "Vegetables and fruits give vitamins and fibre."),
        ("What does the liver make that helps digest fats?", "bile", ["saliva", "urine", "blood"], "Bile breaks fat into small drops."),
        ("Which organ does the brain work with to let you see?", "the eyes", ["the kidneys", "the stomach", "the lungs"], "Eyes send signals to the brain."),
    ])
    return [
        ("The digestive system", [(X.gen(SG4D, "g_func"), 6), (X.gen(SG4D, "g_next"), 6), (X.gen(UK4D, "g_sum"), 5), (pool, 3)]),
        ("Digestion step by step", [(X.gen(SG4D, "g_which"), 5), (X.gen(SG4D, "g_digest"), 4), (X.B(SG4D, "B1"), 4), (X.B(SG4D, "B2"), 4), (pool, 3)]),
        ("Organs and organ systems", [(X.gen(US6B, "g_organ"), 6), (X.gen(US6B, "g_job"), 6), (pool, 5), (X.gen(US6B, "g_level", n=3), 3)]),
        ("Bones, muscles and nerves", [(X.gen(UK3K, "g_bone"), 6), (X.gen(UK3K, "g_mus"), 5), (X.gen(US4S, "g_organ", n=5), 5), (X.gen(UK3K, "g_job"), 4)]),
        ("Food and a healthy body", [(X.gen(UK3N, "g_diet"), 5), (X.gen(UK6D, "g_food"), 5), (X.gen(UK6D, "g_job"), 4), (pool, 3), (X.B(SG4D, "B5"), 3)]),
    ]


def s_health(X):
    pool = X.pool([
        ("Which choice is best for a healthy heart?", "being active for at least an hour a day", ["sitting for most of the day", "eating lots of salty snacks", "smoking"], "Exercise strengthens the heart."),
        ("Why should you wash your hands before eating?", "to remove germs that can make you sick", ["to make food taste better", "to warm your hands", "to make your hands stronger"], "Germs spread on hands."),
        ("Why is sleep important?", "The body and brain repair and grow during sleep.", ["Sleep makes you hungry.", "Sleep is only for babies.", "Sleep stops the heart."], "Children need about 9 to 11 hours."),
        ("What does a vaccine help the body do?", "fight off a disease before you get sick", ["digest food faster", "grow taller", "see better"], "Vaccines train the immune system."),
        ("Which drink is the healthiest choice for most people?", "water", ["pop", "energy drinks", "sweet iced tea"], "Water has no added sugar."),
        ("Why should children wear a helmet when biking?", "to protect the brain and skull", ["to keep warm", "to see better", "to go faster"], "The skull protects the brain, and a helmet protects the skull."),
        ("What happens to muscles that are not used?", "They become weaker.", ["They grow bigger.", "They turn into bone.", "They become nerves."], "Use it or lose it."),
        ("Which technology helps doctors see broken bones?", "X-rays", ["a thermometer", "a stethoscope", "a blood pressure cuff"], "X-rays pass through soft tissue but not bone."),
        ("How does second-hand smoke affect people nearby?", "It can harm their lungs too.", ["It is safe to breathe.", "It only affects pets.", "It makes lungs stronger."], "Avoid smoky places."),
        ("Which snack is the healthiest choice?", "an apple and some cheese", ["a bag of candy", "a can of pop", "a chocolate bar"], "Choose whole foods."),
        ("What is one sign of dehydration?", "feeling thirsty and tired with dark urine", ["feeling very energetic", "growing taller", "having pale skin only"], "Drink water when active."),
        ("Canada's Food Guide shows a plate. About how much of the plate should be vegetables and fruits?", "half", ["one quarter", "all of it", "none"], "Half the plate is vegetables and fruits."),
        ("On Canada's Food Guide plate, what fills one quarter of the plate besides protein foods?", "whole grain foods", ["candy", "pop", "butter"], "A quarter is whole grains and a quarter is protein foods."),
        ("Which is a protein food in Canada's Food Guide?", "beans, eggs, fish or nuts", ["apples", "rice", "lettuce"], "Protein foods help build and repair the body."),
        ("Which is a whole grain food?", "brown rice", ["white sugar", "a candy bar", "pop"], "Whole grains have fibre."),
        ("What does Canada's Food Guide say to drink most often?", "water", ["pop", "juice", "energy drinks"], "Make water your drink of choice."),
        ("Why should you read food labels?", "to check for added sugar, salt and fat", ["to find the colour of the food", "to see who made the box", "to learn the price only"], "Labels help you make healthy choices."),
        ("Which habit is part of healthy eating?", "eating meals with others and cooking at home more often", ["skipping breakfast every day", "eating in front of a screen always", "drinking pop with every meal"], "Canada's Food Guide encourages these habits."),
        ("Which nutrient gives the body its main source of quick energy?", "carbohydrates", ["vitamins", "water", "minerals"], "Grains and fruits have carbohydrates."),
        ("Which food is a good source of calcium for strong bones?", "milk or fortified soy beverage", ["candy", "potato chips", "pop"], "Calcium helps bones and teeth."),
        ("How does a healthy diet help the digestive system?", "Fibre, water and a mix of foods keep it working well.", ["Only candy keeps it healthy.", "Skipping meals helps it.", "The digestive system needs no food."], "Balanced meals help digestion."),
    ])
    return [
        ("Exercise and the body", [(X.gen(UK6D, "g_active", n=5), 5), (X.gen(UK6D, "g_eff"), 6), (pool, 5), (X.B(UK6D, "B1"), 4)]),
        ("Healthy food choices", [(pool, 8), (X.gen(UK6D, "g_label", n=5), 5), (X.gen(UK3N, "g_diet"), 4), (X.gen(UK6D, "g_food"), 3)]),
        ("Habits that harm the body", [(X.gen(UK9H, "g_smoke"), 6), (pool, 6), (X.B(UK9H, "B1", drop=["recreational", "solvent", "depressant", "stimulant", "cannabis"]), 4), (X.gen(UK6D, "g_eff"), 4)]),
        ("Germs and protection", [(pool, 6), (X.gen(UK6D, "g_spoon", n=5), 5), (X.B(UK3N, "B1"), 5), (X.B(UK3K, "B1"), 4)]),
        ("Health investigations", [(X.B(UK6D, "B5"), 5), (X.B(UK9H, "B5"), 4), (X.gen(UK9H, "g_data"), 4), (X.B(UK3N, "B5"), 4), (X.gen(UK6D, "g_active", n=3), 3)]),
    ]


def s_matter(X):
    pool = X.pool([
        ("What is matter?", "anything that has mass and takes up space", ["only things you can see", "only solids", "only liquids"], "Air is matter too."),
        ("Which state of matter has a fixed shape and a fixed volume?", "solid", ["liquid", "gas", "none of them"], "Solids keep their shape."),
        ("Which state of matter takes the shape of its container but keeps its volume?", "liquid", ["solid", "gas", "plasma only"], "Liquids flow."),
        ("Which state of matter spreads out to fill any container?", "gas", ["solid", "liquid", "ice"], "Gas particles move freely."),
        ("What is it called when a liquid turns into a gas?", "evaporation (boiling if it is fast)", ["condensation", "freezing", "melting"], "Puddles dry up by evaporation."),
        ("What is it called when a gas turns into a liquid?", "condensation", ["evaporation", "melting", "freezing"], "Water drops form on a cold glass."),
        ("What is it called when a solid turns directly into a gas?", "sublimation", ["melting", "condensation", "freezing"], "Dry ice sublimes."),
        ("Snow disappears on a sunny winter day without melting. What happened?", "It sublimated, turning straight into water vapour.", ["It condensed.", "It froze.", "It turned into sand."], "Sublimation skips the liquid state."),
        ("Which property can you measure with a balance?", "mass", ["colour", "lustre", "texture"], "A balance compares masses."),
        ("Which property describes how easily a material bends without breaking?", "flexibility", ["hardness", "transparency", "lustre"], "Rubber is flexible."),
        ("Why is a stainless steel pot good for cooking?", "It conducts heat well and does not melt on the stove.", ["It is transparent.", "It is flexible like rubber.", "It floats."], "Material choice depends on properties."),
        ("Why is a winter coat filled with feathers or polyester fibres?", "They trap air, which is a good insulator.", ["They conduct heat well.", "They are magnetic.", "They make the coat heavy."], "Trapped air slows heat loss."),
        ("When ice melts, what happens to its mass?", "It stays the same.", ["It gets bigger.", "It gets smaller.", "It disappears."], "Changes of state do not change mass."),
        ("What happens to the particles in water when it boils?", "They move faster and spread far apart.", ["They stop moving.", "They get bigger.", "They join into a solid."], "Heating gives particles more energy."),
    ])
    return [
        ("States of matter", [(pool, 6), (X.gen(UK4M, "g_state", n=6), 6), (X.gen(SG4M, "g_state", n=5), 5), (X.gen(UK4M, "g_prop"), 3)]),
        ("Particles in matter", [(X.gen(US5M, "g_model_state", n=6), 6), (X.gen(US5M, "g_is_matter", n=5), 5), (X.gen(US5M, "g_not_matter"), 4), (X.gen(UK4M, "g_part"), 3), (pool, 2)]),
        ("Changes of state", [(X.gen(UK4S, "g_word"), 6), (X.gen(UK4S, "g_ex"), 6), (X.gen(UK4S, "g_mp", n=5), 5), (pool, 3)]),
        ("Properties of materials", [(X.gen(US5P, "g_which_prop", n=6), 6), (X.gen(US5P, "g_conduct", n=5), 5), (X.gen(US5P, "g_magnet", n=4), 4), (X.gen(US5P, "g_dissolve"), 3), (pool, 2)]),
        ("Matter investigations", [(X.gen(US5P, "g_mystery", n=4), 4), (X.gen(US5M, "g_air_mass", n=4), 4), (X.B(US5M, "B5"), 4), (X.B(UK4M, "B5"), 4), (X.B(US5P, "B5"), 4)]),
    ]


def s_change(X):
    pool = X.pool([
        ("Which is a physical change?", "cutting paper into pieces", ["burning wood", "baking a cake", "a nail rusting"], "No new substance forms."),
        ("Which is a chemical change?", "burning a candle wick", ["melting chocolate", "freezing water", "crushing a can"], "Burning makes new substances like smoke and gas."),
        ("Which is a sign that a chemical change may have happened?", "a new smell, gas bubbles or a colour change", ["a change in shape only", "a change in size only", "being cut in half"], "New substances can give off gas, light or heat."),
        ("Why is melting ice a physical change?", "It is still water, just in a different state.", ["A new substance forms.", "It cannot be reversed.", "It gives off light."], "Changes of state are physical."),
        ("Why is cooking an egg a chemical change?", "New substances form and it cannot change back.", ["It only changes shape.", "It is still a raw egg.", "It is reversible."], "Heat changes the proteins in the egg."),
        ("Mixing baking soda and vinegar makes bubbles. What kind of change is this?", "chemical (a gas is made)", ["physical (just mixing)", "a change of state", "no change"], "Carbon dioxide gas forms."),
        ("Which change can be easily reversed?", "water freezing into ice", ["toast burning", "an apple rotting", "paper burning"], "Ice can melt back into water."),
        ("Rust forms on a bike left outside. What causes this change?", "iron reacting with oxygen and water", ["the bike getting cold", "the bike being painted", "the bike melting"], "Rust is a new substance."),
        ("How can a factory reduce the harm from chemical changes?", "by treating waste so it does not pollute water and air", ["by dumping waste in rivers", "by burning more garbage", "by ignoring the waste"], "Waste can be treated or reused."),
        ("Composting food scraps is which kind of change?", "chemical (decomposers make new substances)", ["physical only", "a change of state", "no change"], "Food scraps break down into compost."),
        ("Dissolving sugar in water is which kind of change?", "physical (the sugar can be recovered by evaporation)", ["chemical (a new substance forms)", "a change of state to gas", "burning"], "Evaporating the water leaves the sugar behind."),
        ("Why is recycling aluminum cans useful?", "Melting and reshaping cans uses less energy than mining new aluminum.", ["Cans turn into new substances.", "It makes cans heavier.", "It creates pollution only."], "Recycling is a physical change that saves resources."),
    ])
    return [
        ("Physical or chemical?", [(X.gen(US5C, "g_classify", n=7), 7), (X.gen(US5C, "g_which_phys"), 5), (X.gen(US5C, "g_which_chem"), 5), (pool, 3)]),
        ("Signs of chemical change", [(X.gen(US5C, "g_sign_example"), 6), (X.gen(US5C, "g_sign"), 4), (X.gen(UK5R, "g_sign"), 5), (X.gen(UK5R, "g_fizz", n=3), 3), (pool, 2)]),
        ("Reversible and irreversible", [(X.gen(UK5R, "g_rev"), 6), (X.gen(UK5R, "g_pick", n=6), 6), (X.gen(AU6R, "g_auc"), 5), (pool, 3)]),
        ("Changes in daily life", [(pool, 6), (X.gen(UK5R, "g_rust"), 4), (X.B(US5C, "B2"), 5), (X.B(UK5R, "B1"), 5)]),
        ("Change investigations", [(X.gen(US5C, "g_mass_hint", n=5), 5), (X.B(US5C, "B5"), 5), (X.B(UK5R, "B5"), 4), (X.gen(US5C, "g_table"), 3), (X.B(AU6R, "POOL5"), 3)]),
    ]


FORCES = [
    ("a rope holding up a swing", "tension", "the rope is being pulled from both ends"),
    ("the cables of a suspension bridge", "tension", "the cables are pulled tight"),
    ("a guitar string", "tension", "the string is stretched"),
    ("the legs of a chair with someone sitting on it", "compression", "the legs are squeezed"),
    ("the bricks at the bottom of a wall", "compression", "the weight above squeezes them"),
    ("a column holding up a roof", "compression", "the roof pushes down on it"),
    ("a wet towel being wrung out", "torsion", "it is twisted"),
    ("a key turning in a lock", "torsion", "it is twisted"),
    ("a screwdriver turning a screw", "torsion", "it is twisted"),
    ("paper being cut by scissors", "shear", "two forces push in opposite directions across it"),
    ("a bolt holding two sliding plates together", "shear", "the plates push it sideways in opposite directions"),
    ("a diving board with a swimmer at the end", "bending", "the top stretches and the bottom squeezes"),
    ("a shelf sagging under heavy books", "bending", "it is pushed down in the middle"),
    ("a bungee cord when someone jumps", "tension", "it is stretched"),
    ("the stones of an arch bridge", "compression", "the arch pushes the stones together"),
]
FDEF = {"tension": "a pulling or stretching force", "compression": "a squeezing or pushing force", "torsion": "a twisting force",
        "shear": "two forces pushing in opposite directions across a material", "bending": "a mix of compression and tension that bends a material"}


def force_kind(R):
    def f():
        obj, k, why = R.choice(FORCES)
        others = [x for x in FDEF if x != k]
        R.shuffle(others)
        return tq("Which internal force acts on %s?" % obj, k, others[:3], "%s: %s, so it is %s (%s)." % (obj[0].upper() + obj[1:], why, k, FDEF[k]))
    return f


FORCE_ROWS = [
        ("What is a structure?", "something built to hold or support a load", ["a kind of energy", "a living thing", "a type of rock"], "Buildings, bridges, chairs and nests are structures."),
        ("What is a load?", "a force acting on a structure, such as weight, wind or people", ["the colour of a structure", "the age of a structure", "a type of nail"], "Structures must carry loads."),
        ("What is a static (dead) load?", "a load that does not change, like the weight of the structure itself", ["wind gusts", "people walking", "cars driving over a bridge"], "Static loads stay the same."),
        ("What is a dynamic (live) load?", "a load that changes or moves, like traffic or wind", ["the weight of the bricks", "the weight of the roof beams", "the foundation"], "Dynamic loads change."),
        ("Which is an external force on a house?", "heavy snow on the roof", ["compression in the walls", "tension in a beam", "torsion in a screw"], "External forces act on a structure from outside."),
        ("Why are triangles used in bridges and towers?", "Triangles keep their shape and spread forces well.", ["Triangles look nice only.", "Triangles are lighter than air.", "Triangles are always made of wood."], "A triangle cannot be pushed out of shape without bending its sides."),
        ("Which shape is the weakest if pushed at a corner: a square frame or a triangle frame?", "the square frame", ["the triangle frame", "they are equally strong", "neither changes shape"], "Squares can fold into a diamond shape."),
        ("What is a frame structure?", "a structure made of parts joined together, like a skeleton", ["a solid block like a dam", "a thin curved shell", "a pile of sand"], "Houses and bicycles have frames."),
        ("What is a shell structure?", "a thin, curved outer layer that holds its shape", ["a solid block", "a frame of beams", "a rope bridge"], "Eggs, domes and canoes are shell structures."),
        ("What is a solid structure?", "a structure made of solid material all the way through", ["a hollow frame", "a thin shell", "a rope"], "Dams and brick walls are solid structures."),
        ("Why is the base of the CN Tower wide?", "A wide base makes it more stable against wind.", ["It saves concrete.", "It makes it taller.", "It makes it lighter."], "Wide bases resist tipping."),
        ("Why do tall buildings sway a little in strong wind?", "They are designed to bend slightly instead of breaking.", ["They are falling down.", "They are made of rubber.", "The wind pushes the ground."], "Flexibility absorbs force."),
        ("How do engineers protect buildings from earthquakes?", "with flexible frames and bases that absorb shaking", ["by making them taller", "by using glass walls only", "by removing foundations"], "Base isolators reduce shaking."),
        ("What is a foundation?", "the base that spreads a building's load into the ground", ["the roof", "the paint", "the windows"], "Foundations stop buildings from sinking."),
        ("A cardboard bridge sags under a toy car. How could you make it stronger?", "fold the cardboard into a corrugated or triangular shape", ["use thinner cardboard", "make the bridge longer", "remove the supports"], "Shapes add strength."),
        ("Why does a heavy snowfall worry owners of flat roofs?", "The extra load could make the roof collapse.", ["Snow makes roofs lighter.", "Snow melts roofs.", "Snow adds tension to windows."], "Snow is a big load in Ontario winters."),
        ("Which material is strong in tension?", "steel cable", ["a pile of sand", "chalk", "a stack of loose bricks"], "Steel resists pulling."),
        ("Which material is strong in compression but weak in tension?", "concrete", ["rope", "rubber band", "steel cable"], "Concrete is reinforced with steel bars (rebar)."),
        ("Why is steel rebar put inside concrete?", "Steel resists tension, so the concrete does not crack when it bends.", ["To make it lighter", "To change its colour", "To make it melt"], "Reinforced concrete is strong both ways."),
        ("What is the centre of gravity of a structure?", "the point where its weight seems to act", ["the highest point", "the coldest point", "the door"], "A low centre of gravity makes a structure stable."),
        ("Which bridge design uses an arch to carry loads by compression?", "an arch bridge", ["a rope bridge", "a suspension bridge with no towers", "a log on water"], "The arch pushes loads to its ends."),
        ("Which structure is a shell structure?", "an igloo", ["a bicycle frame", "a brick wall", "a hydro tower"], "An igloo is a curved dome."),
        ("Which structure is a frame structure?", "a hydro tower made of steel beams", ["a concrete dam", "an egg", "a dome tent's fabric"], "Frames are joined parts with spaces between."),
        ("Which structure is a solid structure?", "a concrete dam", ["a spider web", "a canoe", "a bike frame"], "Solid structures are filled all the way through."),
        ("How can you make a paper column hold more books?", "roll it into a tube", ["fold it flat", "cut it in half", "wet it"], "Tubes resist compression well."),
        ("Why is an egg hard to crush when you squeeze its ends?", "The curved shell spreads the force over the whole surface.", ["Eggs are made of steel.", "The yolk pushes back.", "Eggs are flexible like rubber."], "Curves spread loads."),
        ("A bookshelf wobbles side to side. What could make it more stable?", "add a diagonal brace to make triangles", ["remove the back panel", "make it taller", "stack heavy books on the top shelf"], "Diagonals stop racking."),
        ("Why is it safer to put heavy items on the bottom shelf?", "It lowers the centre of gravity so the shelf is less likely to tip.", ["It makes the shelf taller.", "It adds tension.", "It makes the shelf lighter."], "Low centre of gravity improves stability."),
        ("Wind pushes hard on the side of a tall sign. What kind of force is this?", "an external, dynamic load", ["an internal static load", "torsion only", "no force"], "Wind changes and acts from outside."),
        ("A steel beam has a heavy load in the middle. Which part is in tension?", "the bottom of the beam", ["the top of the beam", "the ends only", "no part"], "The top squeezes and the bottom stretches."),
        ("Why do bridges have expansion joints?", "Materials expand in summer heat and shrink in winter cold.", ["To make the bridge longer every day", "To collect rainwater", "To make noise"], "Joints stop cracking."),
        ("What happens if a structure's load is greater than it can hold?", "It may bend, crack or collapse.", ["It gets stronger.", "Nothing happens.", "It floats."], "Engineers add a safety margin."),
        ("Which natural structure uses a frame?", "a bird's skeleton", ["a snail's shell", "a rock", "an egg"], "Skeletons are frames."),
        ("Which natural structure is a shell?", "a turtle's shell", ["a spider web", "a tree's branches", "a bone skeleton"], "Turtle shells are curved and strong."),
        ("Why do snowshoes help you walk on snow?", "They spread your weight over a larger area.", ["They make you lighter.", "They melt the snow.", "They add tension."], "Spreading a load reduces pressure."),
        ("What should engineers think about when building a structure?", "safety, strength, cost, the environment and how it will be used", ["only colour", "only cost", "only how tall it is"], "Good design balances many criteria."),
]


def s_forces(X):
    pool = X.pool(FORCE_ROWS)
    fk = X.f(force_kind)
    return [
        ("Structures and loads", [(pool, 10), (X.gen(US3F, "g_change"), 5), (X.gen(US3F, "g_still"), 5)]),
        ("Internal forces", [(fk, 8), (pool, 6), (X.gen(UK7F, "g_name"), 4), (X.gen(SG2P, "g_kind"), 2)]),
        ("Balanced and unbalanced forces", [(X.gen(US3F, "g_pic", n=6), 6), (X.gen(US3F, "g_tug", n=5), 5), (X.gen(UK7F, "g_bal"), 5), (X.gen(SG6F, "g_eff"), 4)]),
        ("Strong and stable designs", [(pool, 10), (fk, 3), (X.gen(US2B, "g_same", n=3), 3), (X.B(US3F, "B1"), 3), (X.gen(SG2P, "g_eff"), 1)]),
        ("Testing structures", [(pool, 6), (X.B(US3F, "B5"), 4), (X.B(UK7F, "B5"), 4), (X.B(SG6F, "B5"), 3), (fk, 2), (X.B(SG2P, "B1"), 3)]),
    ]


def s_energy(X):
    pool = X.pool([
        ("Which is a renewable energy source?", "wind", ["coal", "oil", "natural gas"], "Wind will not run out."),
        ("Which is a non-renewable energy source?", "natural gas", ["solar", "wind", "moving water"], "Fossil fuels took millions of years to form."),
        ("Where does most of Ontario's electricity come from?", "nuclear power and hydroelectric dams", ["coal only", "burning garbage", "candles"], "Ontario closed its coal plants in 2014."),
        ("How does a hydroelectric dam make electricity?", "Falling water turns turbines connected to generators.", ["It burns water.", "It uses sunlight on the water.", "It freezes the water."], "Niagara Falls has large hydro stations."),
        ("What energy change happens in a solar panel?", "light energy → electrical energy", ["electrical energy → light energy", "sound energy → heat", "chemical energy → sound"], "Solar cells change light into electricity."),
        ("What energy change happens when you rub your hands together?", "kinetic (motion) energy → thermal (heat) energy", ["heat → light", "sound → motion", "chemical → nuclear"], "Friction makes heat."),
        ("Why is energy never really 'used up'?", "It changes from one form to another.", ["It disappears.", "It turns into matter.", "It goes to the Moon."], "Energy is conserved."),
        ("Which form of energy is stored in food?", "chemical energy", ["sound energy", "light energy", "electrical energy"], "Your body changes it into motion and heat."),
        ("What is a disadvantage of burning fossil fuels?", "It releases carbon dioxide and pollutes the air.", ["It never runs out.", "It makes no waste.", "It cools the planet."], "Fossil fuels add greenhouse gases."),
        ("What is a disadvantage of wind turbines?", "They only work when the wind blows.", ["They pollute the air.", "They use coal.", "They run out of wind."], "Every source has pros and cons."),
        ("Which action saves energy at home?", "turning off lights when you leave a room", ["leaving the TV on all night", "opening windows with the heat on", "running a half-empty dishwasher"], "Small actions add up."),
        ("Why are LED bulbs better than old incandescent bulbs?", "They give the same light using much less electricity.", ["They are brighter only because they are hot.", "They use more electricity.", "They last a shorter time."], "Less energy is wasted as heat."),
        ("What does the Energy Star label on an appliance mean?", "It uses less energy than similar models.", ["It is very old.", "It runs on solar power only.", "It is made of stars."], "Look for efficient appliances."),
        ("Why should you put on a sweater instead of turning up the heat?", "It saves energy and money.", ["Sweaters make heat from electricity.", "Heat is free.", "It makes the house warmer for everyone."], "Conserving energy reduces pollution."),
        ("What does 'reduce, reuse, recycle' help save?", "resources and the energy needed to make new things", ["only paper", "only money", "nothing"], "Making new products uses energy."),
        ("Which form of energy does a moving car have?", "kinetic energy", ["potential energy only", "sound energy only", "no energy"], "Moving objects have kinetic energy."),
        ("A stretched elastic band stores which form of energy?", "elastic potential energy", ["kinetic energy", "light energy", "sound energy"], "It is released when let go."),
        ("Which is the main energy change in a battery-powered flashlight?", "chemical → electrical → light (and some heat)", ["light → chemical", "sound → electrical", "heat → chemical"], "The battery stores chemical energy."),
    ])
    return [
        ("Forms of energy", [(pool, 6), (X.gen(SG6E, "g_form"), 6), (X.B(SG6E, "B1"), 4), (X.gen(SG6E, "g_sun"), 4)]),
        ("Energy changes", [(X.gen(SG6E, "g_conv"), 6), (X.gen(US4C, "g_out"), 6), (X.gen(US4C, "g_which"), 5), (pool, 3)]),
        ("Renewable and non-renewable", [(X.gen(US4R, "g_effect", n=6), 6), (X.gen(US5E, "g_renew"), 5), (X.gen(US7N, "g_origin"), 5), (pool, 4)]),
        ("Conserving energy and resources", [(X.gen(US5E, "g_rrr"), 5), (X.gen(US5E, "g_solution"), 5), (X.gen(US5E, "g_bulb", n=4), 4), (pool, 6)]),
        ("Energy investigations", [(X.gen(US4R, "g_pie", n=4), 4), (X.gen(US5E, "g_shower", n=4), 4), (X.B(US4C, "B5"), 4), (X.B(US5E, "B5"), 4), (X.gen(US4C, "g_test"), 4)]),
    ]


def UNITS():
    return [
        CU("B", 1, "respiratory-and-circulatory-systems", "B2.1, B2.2, B2.4",
           "Describe the structure and function of the respiratory and circulatory systems and how they work together to supply the "
           "body with oxygen; describe how exercise affects heart and breathing rates.",
           "Respiratory and Circulatory Systems", "Respiratory and circulatory systems",
           "Free Grade 5 science worksheets on the lungs, heart, blood vessels, breathing, pulse and exercise. 100 questions with answers.",
           "The lungs take in oxygen; the heart pumps it around.", "Oxygen goes from the lungs into the blood, and the heart pumps the blood to every cell.",
           L("The respiratory and circulatory systems work as a team.",
             "Air goes in through the nose or mouth, down the windpipe and into the lungs.",
             "In the lungs, oxygen passes into the blood and carbon dioxide passes out.",
             "The heart pumps blood through arteries (away from the heart) and veins (back to the heart).",
             "Exercise makes the heart beat faster and breathing quicker, so muscles get more oxygen."),
           [("Which blood vessels carry blood away from the heart?", ["arteries go away", "veins come back"], "arteries"),
            ("Why does your pulse rise when you run?", ["muscles need more oxygen"], "the heart pumps faster")],
           ["Thinking we breathe out only carbon dioxide (we breathe out some oxygen too).", "Mixing up arteries and veins.",
            "Thinking the lungs pump blood."],
           [("How do the lungs and heart work together?", "The lungs put oxygen into the blood. The heart pumps that blood to the body and brings blood back to the lungs."),
            ("What is a pulse?", "A pulse is the beat of blood moving through an artery each time the heart pumps. You can feel it on your wrist or neck."),
            ("How can we keep these systems healthy?", "Be active, do not smoke, eat well and avoid air pollution when you can.")],
           s_resp),
        CU("B", 2, "digestive-and-other-organ-systems", "B2.1, B2.2, B2.3",
           "Identify major organs and organ systems (digestive, skeletal, muscular, nervous, excretory) and describe their functions "
           "and how they interact.",
           "Digestive and Other Organ Systems", "Digestive and other organ systems",
           "Free Grade 5 science worksheets on digestion, organs, bones, muscles, nerves and the kidneys. 100 questions with answers.",
           "Organs work together in organ systems.", "The digestive system breaks down food; the skeleton supports; nerves carry messages.",
           L("An organ system is a group of organs that work together to do a job.",
             "Digestive system: mouth → esophagus → stomach → small intestine → large intestine.",
             "Skeletal and muscular systems hold you up and move you. Muscles pull on bones.",
             "Nervous system: the brain, spinal cord and nerves carry messages.",
             "Excretory system: the kidneys filter waste from the blood."),
           [("Where are most nutrients absorbed?", ["after the stomach", "a long tube with villi"], "the small intestine"),
            ("Which system protects the brain?", ["the skull is a bone"], "the skeletal system")],
           ["Thinking digestion happens only in the stomach.", "Thinking muscles push bones (they only pull).", "Mixing up the large and small intestine."],
           [("What is the difference between an organ and an organ system?", "An organ is one body part with a job, like the stomach. An organ system is a group of organs working together, like the digestive system."),
            ("How do organ systems work together?", "The digestive system gives nutrients, the circulatory system carries them, and the nervous system controls the body."),
            ("Why is the small intestine so long?", "Its length and its tiny villi give a large surface to absorb nutrients into the blood.")],
           s_dig),
        CU("B", 3, "healthy-body-systems", "B1.1, B1.2, B2.5",
           "Assess the effects of diet, exercise, sleep and habits such as smoking on organ systems; describe technologies and "
           "medical advances that help keep organ systems healthy.",
           "Keeping Body Systems Healthy", "Healthy body systems",
           "Free Grade 5 science worksheets on exercise, healthy eating, Canada's Food Guide, germs, vaccines and habits that harm "
           "the body. 100 questions with answers.",
           "Healthy choices keep organ systems working.", "Being active, eating well, sleeping and avoiding smoking protect your organs.",
           L("Your choices affect your organ systems.",
             "Exercise makes the heart and lungs stronger.",
             "Canada's Food Guide: half the plate vegetables and fruits, plus whole grains and protein foods; drink water.",
             "Smoking, vaping and second-hand smoke damage the lungs and heart.",
             "Handwashing, vaccines and safety gear like helmets protect the body."),
           [("Which drink is the best choice?", ["no added sugar"], "water"),
            ("Why wear a helmet?", ["protects the skull and brain"], "to prevent head injuries")],
           ["Thinking only adults need exercise.", "Thinking a food is healthy just because the package says 'natural'.", "Thinking second-hand smoke is harmless."],
           [("How much activity do children need?", "Children should be active for at least 60 minutes a day."),
            ("How do vaccines work?", "A vaccine teaches the immune system to recognize a germ, so the body can fight it quickly."),
            ("What does Canada's Food Guide suggest?", "Eat plenty of vegetables and fruits, whole grain foods and protein foods, and make water your drink of choice.")],
           s_health),
        CU("C", 4, "properties-of-matter", "C2.1, C2.2, C2.3",
           "Describe the properties of solids, liquids and gases using the particle theory; describe changes of state; identify "
           "properties of materials and how they determine their uses.",
           "Properties of Matter", "Properties of matter",
           "Free Grade 5 science worksheets on solids, liquids and gases, particles, changes of state and properties of materials. "
           "100 questions with answers.",
           "Matter has mass and takes up space.", "Solids keep their shape, liquids take the shape of their container, and gases fill it.",
           L("All matter is made of tiny particles that are always moving.",
             "Solid: particles packed tightly, fixed shape. Liquid: particles slide past each other. Gas: particles far apart and fast.",
             "Heating makes particles move faster: melting, evaporation, sublimation. Cooling: freezing, condensation, deposition.",
             "Properties like hardness, flexibility, conductivity and magnetism decide what a material is used for."),
           [("Water vapour forms drops on a cold window. What change is this?", ["gas → liquid"], "condensation"),
            ("When ice melts, does its mass change?", ["the particles are the same"], "no")],
           ["Thinking air is not matter.", "Mixing up evaporation and condensation.", "Thinking mass changes when something melts."],
           [("What are the three states of matter?", "Solid, liquid and gas. They differ in how closely packed the particles are and how they move."),
            ("What is sublimation?", "A solid turning straight into a gas, like snow disappearing on a cold sunny day or dry ice."),
            ("Why is air matter?", "Air has mass and takes up space, so it is matter even though we cannot see it.")],
           s_matter),
        CU("C", 5, "physical-and-chemical-changes", "C2.4, C2.5, C1.1",
           "Distinguish between physical changes and chemical changes; identify signs of chemical change; assess the effects of "
           "changes in matter on the environment and ways to reduce harm.",
           "Physical and Chemical Changes", "Physical and chemical changes",
           "Free Grade 5 science worksheets on physical and chemical changes, signs of a chemical change, reversible and irreversible "
           "changes. 100 questions with answers.",
           "A chemical change makes a new substance.", "Physical changes (melting, cutting, dissolving) can often be reversed; chemical changes usually cannot.",
           L("In a physical change, the substance stays the same. In a chemical change, a new substance forms.",
             "Physical changes: melting, freezing, cutting, crushing, dissolving.",
             "Chemical changes: burning, rusting, cooking, rotting.",
             "Signs of a chemical change: gas bubbles, a new colour or smell, light or heat given off, a solid forming."),
           [("Is burning toast physical or chemical?", ["new black substance", "cannot change back"], "chemical"),
            ("Is dissolving salt in water physical or chemical?", ["evaporate the water to get the salt back"], "physical")],
           ["Thinking every change of colour is a chemical change.", "Thinking dissolving makes the substance disappear.", "Thinking chemical changes are always dangerous."],
           [("How can you tell a chemical change happened?", "Look for a new substance: bubbles of gas, a new colour or smell, light or heat, or a solid forming in a liquid."),
            ("Is melting a chemical change?", "No. Melting changes the state, but the substance is still the same."),
            ("Why do chemical changes matter for the environment?", "Burning fuels and some factory processes make pollution, so waste must be treated and reduced.")],
           s_change),
        CU("D", 6, "forces-acting-on-structures", "D2.1, D2.2, D2.3, D2.4",
           "Identify internal forces (tension, compression, torsion, shear) and external forces acting on structures; describe "
           "static and dynamic loads; explain how design, shape and materials help structures withstand forces.",
           "Forces Acting on Structures", "Forces acting on structures",
           "Free Grade 5 science worksheets on tension, compression, torsion and shear, loads, triangles, bridges and building safe "
           "structures. 100 questions with answers.",
           "Structures must withstand forces.", "Tension pulls, compression squeezes, torsion twists and shear slides; good designs spread forces.",
           L("Forces act on every structure, from outside (external) and inside (internal).",
             "External forces: weight, wind, snow, people, earthquakes. Static loads stay the same; dynamic loads change.",
             "Internal forces: tension (pull), compression (squeeze), torsion (twist), shear (slide across).",
             "Triangles, arches, wide bases, deep foundations and strong materials help structures stay up."),
           [("Which force acts on a rope holding a swing?", ["the rope is pulled"], "tension"),
            ("Why are triangles used in towers?", ["they do not change shape"], "they are rigid and spread forces")],
           ["Mixing up tension and compression.", "Thinking a taller structure is always stronger.", "Thinking only heavy objects put forces on structures (wind and snow do too)."],
           [("What is the difference between tension and compression?", "Tension is a pulling force that stretches. Compression is a pushing force that squeezes."),
            ("What is the difference between static and dynamic loads?", "A static load does not change, like the weight of a bridge. A dynamic load changes, like traffic or wind."),
            ("Why do engineers test structures?", "To make sure they are safe and can hold the loads they will face, such as heavy snow in an Ontario winter.")],
           s_forces),
        CU("E", 7, "energy-and-resources", "E1.1, E1.2, E2.1, E2.2, E2.3",
           "Identify forms of energy and energy transformations; distinguish renewable and non-renewable energy sources; assess "
           "the effects of energy use on the environment and ways to conserve energy and resources.",
           "Conservation of Energy and Resources", "Energy and resources",
           "Free Grade 5 science worksheets on forms of energy, energy changes, renewable and non-renewable resources, Ontario "
           "electricity and saving energy. 100 questions with answers.",
           "Energy changes form; it is not used up.", "Renewable sources do not run out; conserving energy saves resources and reduces pollution.",
           L("Energy cannot be made or destroyed, only changed from one form to another.",
             "Forms of energy: kinetic, potential, thermal, light, sound, electrical, chemical.",
             "Renewable sources: sun, wind, moving water, biomass. Non-renewable: coal, oil, natural gas, uranium.",
             "Ontario's electricity comes mostly from nuclear and hydroelectric power.",
             "Turning things off, using LED bulbs and Energy Star appliances, and reducing waste conserve energy."),
           [("What energy change happens in a solar panel?", ["light in", "electricity out"], "light → electrical"),
            ("Is natural gas renewable?", ["it took millions of years to form"], "no")],
           ["Thinking energy gets used up and disappears.", "Thinking renewable sources have no drawbacks.", "Mixing up energy sources and forms of energy."],
           [("What is the difference between renewable and non-renewable energy?", "Renewable energy comes from sources that are replaced naturally, like wind. Non-renewable sources, like oil, run out."),
            ("Where does Ontario's electricity come from?", "Mostly from nuclear power stations and hydroelectric dams, plus wind, solar and natural gas."),
            ("How can families save energy?", "Turn off lights and devices, use LED bulbs, keep doors and windows closed when heating or cooling, and dress for the weather.")],
           s_energy),
    ]
