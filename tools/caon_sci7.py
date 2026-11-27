# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 7 (B Interactions in the Environment, C Pure Substances and Mixtures,
D Form and Function, E Heat in the Environment). Built by caon_sci.build."""
from caon_sci import CU, tq
from caon_sci5 import force_kind, FORCE_ROWS

US7I, US7R, US7C, US7E = ("gen_us_science_g7_interactions_in_ecosystems", "gen_us_science_g7_resources_and_populations",
                          "gen_us_science_g7_cycling_of_matter_and_energy_flow", "gen_us_science_g7_ecosystem_changes")
UK8F, SG2I, SG6M, US7H = ("gen_uk_science_y8_ecosystems_and_food_webs", "gen_sg_science_s2_interactions_within_ecosystems",
                          "gen_sg_science_p6_mans_impact_on_the_environment", "gen_us_science_g7_human_impact_on_the_environment")
AU7M, UK7M, SG1S, SG1E = ("gen_au_science_y7_mixtures_and_separation", "gen_uk_science_y7_mixtures_and_separation",
                          "gen_sg_science_s1_separation_techniques", "gen_sg_science_s1_elements_compounds_and_mixtures")
US5X, UK5D, UK5S = "gen_us_science_g5_mixtures_and_solutions", "gen_uk_science_y5_dissolving_and_solutions", "gen_uk_science_y5_separating_mixtures"
SG1P, UK7P, US6P = "gen_sg_science_s1_particulate_nature_of_matter", "gen_uk_science_y7_particles_and_states_of_matter", "gen_us_science_g6_particles_and_states_of_matter"
US6T, US6D, SG4H, SG4C = ("gen_us_science_g6_thermal_energy_and_temperature", "gen_us_science_g6_designing_to_control_heat_transfer",
                          "gen_sg_science_p4_heat_and_temperature", "gen_sg_science_p4_heat_conductors_and_insulators")
SG2H, UK9T, US6G, UK8A = ("gen_sg_science_s2_heat_transfer_and_its_effects", "gen_uk_science_y9_thermal_energy",
                          "gen_us_science_g6_global_temperature_and_climate_change", "gen_uk_science_y8_the_atmosphere_and_climate")
US3F, UK7F, US2B = "gen_us_science_g3_balanced_and_unbalanced_forces", "gen_uk_science_y7_forces", "gen_us_science_g2_building_with_small_pieces"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def L(lead, *xs):
    return "<p><b>%s</b></p><ul>%s</ul>" % (lead, ul(*xs))


def s_eco(X):
    pool = X.pool([
        ("What is an ecosystem?", "all the living things in an area and the non-living things they interact with", ["only the animals in a forest", "only the soil and water", "one food chain"], "Biotic and abiotic parts interact."),
        ("Which is a biotic factor?", "a white pine tree", ["sunlight", "temperature", "soil minerals"], "Biotic means living."),
        ("Which is an abiotic factor?", "water temperature in a lake", ["a pike", "algae", "a beaver"], "Abiotic means non-living."),
        ("What is symbiosis?", "a close relationship between two different species", ["a kind of food chain", "a type of rock", "an abiotic factor"], "It can be mutualism, commensalism or parasitism."),
        ("Bees get nectar and flowers get pollinated. What kind of relationship is this?", "mutualism (both benefit)", ["parasitism", "commensalism", "competition"], "Both species gain."),
        ("A tick feeds on a deer's blood. What kind of relationship is this?", "parasitism (one benefits, one is harmed)", ["mutualism", "commensalism", "predation of plants"], "The deer is harmed."),
        ("A bird nests in a tree and the tree is not affected. What kind of relationship is this?", "commensalism", ["mutualism", "parasitism", "predation"], "One benefits; the other is not helped or harmed."),
        ("Why is only about 10% of energy passed on to the next level of a food chain?", "Most energy is used for life processes or lost as heat.", ["Animals store it all.", "Plants block it.", "Energy is destroyed."], "This is shown in an energy pyramid."),
        ("What is the role of producers in an ecosystem?", "They capture the Sun's energy and make food by photosynthesis.", ["They break down dead things.", "They eat other animals.", "They make soil."], "Producers are at the base."),
        ("Which organisms recycle nutrients from dead matter back into the soil?", "decomposers", ["producers", "top predators", "herbivores"], "Fungi and bacteria are decomposers."),
        ("What is carrying capacity?", "the largest population an ecosystem can support", ["the weight an animal can carry", "the number of ecosystems on Earth", "the speed of a population"], "Food, water and space limit populations."),
        ("Which is a limiting factor for a deer population in winter?", "food buried under deep snow", ["too much sunlight", "too many maple trees", "warm weather"], "Scarce food limits populations."),
        ("What is succession?", "the gradual change in the species in an ecosystem over time", ["a sudden flood", "a kind of rock layer", "the life cycle of a frog"], "A field can slowly become a forest."),
        ("After a forest fire in northern Ontario, what usually grows first?", "grasses, small plants and fast-growing trees like aspen", ["old white pines", "nothing for 1000 years", "cactus"], "Pioneer species come first."),
    ])
    return [
        ("Biotic and abiotic factors", [(pool, 6), (X.gen(US7I, "g_kind", n=6), 6), (X.gen(SG2I, "g_fact"), 5), (X.gen(US7I, "g_which", n=3), 3)]),
        ("Relationships between species", [(X.gen(US7I, "g_which", n=6), 6), (X.gen(SG2I, "g_rel"), 6), (X.gen(US7R, "g_compete"), 4), (pool, 4)]),
        ("Energy flow and cycles", [(X.gen(US7C, "g_energy"), 6), (X.gen(US7C, "g_web", n=5), 5), (X.gen(UK8F, "g_pyr"), 5), (X.gen(SG2I, "g_energy"), 4)]),
        ("Populations and limits", [(X.gen(US7R, "g_graph", n=6), 6), (X.gen(US7R, "g_limit"), 5), (X.gen(US7R, "g_table", n=4), 4), (pool, 5)]),
        ("Change in ecosystems", [(X.gen(US7E, "g_type"), 6), (X.gen(US7E, "g_data", n=5), 5), (X.gen(US7E, "g_succ"), 3), (X.B(US7I, "B5"), 3), (pool, 3)]),
    ]


def s_impact(X):
    pool = X.pool([
        ("What is bioaccumulation?", "the build-up of a toxic substance in an organism over time", ["a kind of photosynthesis", "a healthy diet", "a type of rock"], "Mercury can build up in fish."),
        ("Why do top predators like loons and eagles have the most pesticide in their bodies?", "The toxin becomes more concentrated at each step of the food chain (biomagnification).", ["They eat plants only.", "They live the longest only.", "They breathe more air."], "DDT once harmed bald eagles in Ontario."),
        ("What is sustainability?", "meeting our needs without harming the ability of future generations to meet theirs", ["using resources as fast as possible", "never using any resources", "only recycling paper"], "Sustainable choices protect ecosystems."),
        ("Which is a sustainable forestry practice?", "planting new trees after cutting and leaving buffer zones near streams", ["clear-cutting a whole valley and leaving it bare", "burning slash near rivers", "cutting only the youngest trees"], "Ontario requires forests to be renewed."),
        ("How does urban sprawl affect ecosystems?", "It replaces natural habitats with roads and buildings.", ["It creates more wetlands.", "It has no effect.", "It always increases biodiversity."], "Green spaces help reduce the impact."),
        ("What is a green roof?", "a roof covered with plants that provides habitat and absorbs rainwater", ["a roof painted green", "a roof made of grass clippings only", "a solar panel"], "Toronto requires green roofs on some new buildings."),
        ("How can fertilizer runoff harm a lake?", "It causes algae to grow quickly, and when the algae die, oxygen levels drop.", ["It makes the water clearer.", "It adds more fish.", "It has no effect."], "This is called eutrophication."),
        ("What does the Indigenous idea of 'Seven Generations' teach?", "to think about how our decisions will affect people seven generations from now", ["to use everything now", "to move every seven years", "to plant seven trees"], "It is a long-term view of sustainability."),
        ("Which action reduces your ecological footprint?", "walking, biking or taking transit instead of driving", ["buying more single-use plastics", "leaving lights on", "wasting food"], "Less energy and waste means a smaller footprint."),
        ("How did the reintroduction of elk to parts of Ontario affect ecosystems?", "It restored a native grazing species and its role in the ecosystem.", ["It removed all predators.", "It made the forest disappear.", "It had no effect at all."], "Restoring species can rebuild ecosystems."),
        ("Why are wetlands called 'the kidneys of the landscape'?", "They filter and clean water.", ["They make urine.", "They are shaped like kidneys.", "They pump water uphill."], "Wetlands also reduce flooding."),
        ("Microplastics are found in the Great Lakes. Where do many of them come from?", "broken-down plastic waste and fibres from washing synthetic clothes", ["fish making plastic", "rocks dissolving", "lightning"], "Microplastics are eaten by small animals."),
        ("Why are road salt levels a concern for Ontario streams?", "Salt washes into streams in spring and can harm fish and plants.", ["Salt makes water colder.", "Salt helps all fish.", "Salt turns into sugar."], "Using less salt protects streams."),
        ("What is an ecological footprint?", "the amount of land and resources needed to support a person's lifestyle", ["the size of your shoe", "a fossil footprint", "a hiking trail"], "Smaller footprints are more sustainable."),
        ("How do protected areas like Algonquin Park help sustainability?", "They keep ecosystems intact for wildlife and future generations.", ["They allow unlimited logging.", "They remove all animals.", "They are only for cars."], "Protected areas preserve biodiversity."),
        ("What is composting?", "letting decomposers break food and yard waste into rich soil", ["burning garbage", "burying plastic", "sending food to landfills"], "Composting keeps waste out of landfills."),
        ("Which is a benefit of buying local food?", "less fuel is used to transport it", ["it is always more expensive", "it creates more packaging", "it uses more trucks"], "Shorter trips mean fewer emissions."),
        ("Which is an example of habitat restoration?", "replanting native plants along a stream bank", ["paving a meadow", "draining a marsh", "removing all trees from a park"], "Restored habitats support wildlife."),
    ])
    return [
        ("Human impact on ecosystems", [(X.gen(US7H, "g_impact"), 6), (X.gen(SG6M, "g_cause"), 6), (pool, 5), (X.gen(US7H, "g_monitor"), 3)]),
        ("Pollution and toxins", [(X.gen(SG6M, "g_pol"), 7), (pool, 6), (X.gen(UK8F, "g_bio"), 5), (X.gen(UK8F, "g_poll"), 2)]),
        ("Reducing our impact", [(X.gen(SG6M, "g_3r"), 6), (X.gen(SG6M, "g_waste"), 6), (X.gen(SG6M, "g_good"), 5), (pool, 3), (X.gen(US7H, "g_impact", n=2), 1)]),
        ("Sustainability", [(pool, 8), (X.B(SG6M, "B1"), 4), (X.B(SG6M, "B2"), 4), (X.B(US7H, "B1"), 4)]),
        ("Environmental data", [(X.gen(US7H, "g_total", n=5), 5), (X.gen(US7E, "g_data", n=5), 5), (X.B(US7H, "B5"), 4), (X.B(SG6M, "B5"), 3), (X.gen(US7E, "g_effect"), 3)]),
    ]


def s_pure(X):
    pool = X.pool([
        ("What is a pure substance?", "a substance made of only one kind of particle", ["a mix of two or more substances", "anything clean", "only water"], "Pure substances include elements and compounds."),
        ("Which is a pure substance?", "distilled water", ["salt water", "orange juice", "air"], "Distilled water has only water particles."),
        ("Which is a mixture?", "trail mix", ["gold", "pure sugar", "oxygen gas"], "Mixtures contain two or more substances."),
        ("What is a mechanical mixture?", "a mixture where you can see the different parts", ["a mixture that looks like one substance", "a pure substance", "an element"], "Granola is a mechanical mixture."),
        ("What is a solution?", "a mixture that looks like one substance because one part is dissolved in another", ["a mixture you can see the parts of", "a pure element", "a solid only"], "Salt water is a solution."),
        ("What is a suspension?", "a cloudy mixture whose particles settle if left standing", ["a clear solution", "a pure substance", "a gas"], "Muddy water and some salad dressings are suspensions."),
        ("Which is an element?", "copper", ["water", "salt", "sugar"], "Elements are made of one kind of atom."),
        ("Which is a compound?", "carbon dioxide", ["oxygen", "iron", "gold"], "Compounds have two or more kinds of atoms joined together."),
        ("What does the particle theory say about particles of matter?", "They are always moving and have spaces between them.", ["They never move.", "They are the same in every substance.", "They grow when heated."], "Particles move faster when heated."),
        ("Why does food colouring spread through water even if you do not stir?", "Moving particles mix by themselves (diffusion).", ["The water is pushing it.", "Gravity spreads it.", "The colouring is alive."], "Particles are always moving."),
        ("50 mL of water and 50 mL of rubbing alcohol are mixed. The total is less than 100 mL. Why?", "Small particles fit into the spaces between larger ones.", ["Some liquid disappears.", "The measuring was wrong.", "Alcohol is heavier."], "This supports the particle theory."),
        ("Is milk a pure substance or a mixture?", "a mixture (it contains water, fats, proteins and sugar)", ["a pure substance", "an element", "a gas"], "Milk is a colloid, a kind of mixture."),
        ("Which is a homogeneous mixture?", "air", ["sand and gravel", "chocolate chip cookie dough", "a salad"], "Air looks the same throughout."),
        ("Why is it important to know if a product is a mixture?", "The parts may be separated and some may be harmful or recyclable.", ["Mixtures are always safe.", "Mixtures never change.", "It does not matter."], "Labels list the parts of a mixture."),
    ])
    return [
        ("Pure substances and mixtures", [(pool, 7), (X.gen(UK7M, "g_voc"), 6), (X.gen(UK7M, "g_pure"), 3), (X.gen(AU7M, "g_pm"), 4)]),
        ("Elements and compounds", [(X.gen(SG1E, "g_metal", n=6), 6), (X.B(SG1E, "B1"), 5), (pool, 5), (X.gen(SG1E, "g_susp"), 4)]),
        ("The particle theory", [(X.gen(SG1P, "g_cons"), 6), (X.gen(SG1P, "g_exp"), 5), (X.gen(UK7P, "g_state"), 5), (X.gen(SG1P, "g_dif"), 4)]),
        ("Kinds of mixtures", [(X.gen(US5X, "g_is_solution"), 6), (X.gen(SG1E, "g_sol"), 6), (pool, 4), (X.B(UK7M, "B1"), 4)]),
        ("Mixture investigations", [(X.gen(UK7M, "g_mass", n=5), 5), (X.gen(US5X, "g_mass_mix", n=4), 4), (X.B(UK7M, "B5"), 4), (X.B(SG1P, "B5"), 4), (X.B(AU7M, "POOL5"), 3)]),
    ]


def s_sep(X):
    pool = X.pool([
        ("What is a solute?", "the substance that dissolves", ["the substance that does the dissolving", "a mixture you can see", "a solid that does not dissolve"], "Sugar is the solute in sugar water."),
        ("What is a solvent?", "the substance that does the dissolving", ["the substance that dissolves", "an undissolved solid", "a magnet"], "Water is called the universal solvent."),
        ("What does soluble mean?", "able to dissolve in a solvent", ["unable to dissolve", "able to float", "able to melt"], "Salt is soluble in water."),
        ("Which would dissolve sugar fastest?", "hot water, stirred, with fine sugar", ["cold water, not stirred, with sugar cubes", "ice", "cold water with sugar cubes"], "Heat, stirring and smaller pieces speed up dissolving."),
        ("What is a saturated solution?", "a solution that cannot dissolve any more solute at that temperature", ["a solution with no solute", "a very cold solution", "a mixture of sand and water"], "Extra solute sinks to the bottom."),
        ("What is concentration?", "the amount of solute in a certain amount of solution", ["the colour of a solution", "the temperature of a solution", "the size of the container"], "More solute means higher concentration."),
        ("A solution has 20 g of salt in 100 mL of water. What is its concentration?", "20 g/100 mL (0.2 g/mL)", ["2 g/mL", "100 g/20 mL", "0.02 g/mL"], "20 ÷ 100 = 0.2 g/mL."),
        ("Which method separates sand from water?", "filtration", ["evaporation only", "magnetism", "chromatography"], "The filter traps the sand."),
        ("Which method gets salt back from salt water?", "evaporation", ["filtration", "a magnet", "sieving"], "The water evaporates and leaves the salt."),
        ("Which method separates iron filings from sulfur powder?", "a magnet", ["filtration", "evaporation", "distillation"], "Iron is magnetic."),
        ("Which method separates the inks in a marker?", "chromatography", ["filtration", "a magnet", "sieving"], "Each ink travels up the paper at a different speed."),
        ("How do recycling plants separate steel cans from aluminum cans?", "with big magnets", ["by colour", "by smell", "with water"], "Steel is magnetic; aluminum is not."),
        ("How are oil spills cleaned up on water?", "with floating booms and skimmers, because oil floats on water", ["by stirring the water", "by adding salt", "by freezing the lake"], "Oil and water do not mix."),
        ("How is drinking water cleaned in Ontario treatment plants?", "by settling, filtering and disinfecting", ["by adding mud", "by boiling the whole lake", "by freezing it"], "Several separation steps are used."),
        ("Why does a sieve separate gravel from sand?", "The holes let small sand grains through but stop larger gravel.", ["Gravel dissolves.", "Sand is magnetic.", "Gravel evaporates."], "Sieving uses particle size."),
        ("What is distillation?", "boiling a liquid and condensing the vapour to collect a pure liquid", ["filtering with paper", "using a magnet", "letting things settle"], "Distillation separates liquids with different boiling points."),
    ])
    return [
        ("Solutes, solvents and solubility", [(pool, 6), (X.gen(UK5D, "g_sol"), 5), (X.gen(UK5D, "g_pick", n=5), 5), (X.gen(SG1E, "g_solub"), 4)]),
        ("Dissolving rate and saturation", [(X.gen(UK5D, "g_rate", n=6), 6), (X.gen(US5X, "g_saturate", n=5), 5), (X.gen(UK5D, "g_sat", n=5), 5), (pool, 4)]),
        ("Separating mixtures", [(X.gen(UK5S, "g_mix"), 6), (X.gen(SG1S, "g_meth"), 6), (X.gen(UK7M, "g_method"), 5), (pool, 3)]),
        ("Chromatography and distillation", [(X.gen(UK7M, "g_chrom", n=6), 6), (X.gen(SG1S, "g_dist"), 5), (X.gen(SG1S, "g_prin"), 5), (pool, 4)]),
        ("Separation in industry and the environment", [(pool, 6), (X.gen(US5X, "g_sep", n=5), 5), (X.gen(UK5S, "g_rec"), 5), (X.B(SG1S, "B5"), 4)]),
    ]


def s_form(X):
    pool = X.pool([
        ("What does 'form' mean when describing a structure?", "its shape and size", ["only its colour", "its price", "its age"], "Form must suit the function."),
        ("What does 'function' mean when describing a structure?", "the job the structure is designed to do", ["its colour", "its weight only", "the name of the builder"], "A bridge's function is to carry loads across a gap."),
        ("Why are hockey helmets rounded?", "A curved shell spreads the force of a hit.", ["To look fast", "To hold more air", "To make them heavier"], "The form fits the function: protection."),
        ("Why does a chair have four legs spread apart?", "A wide base makes it stable.", ["To make it lighter", "To make it taller", "To stop it from being sat on"], "A wide base keeps the centre of gravity over it."),
        ("What is ergonomics?", "designing objects to fit the human body comfortably and safely", ["the study of energy", "the study of rocks", "building tall towers"], "Computer chairs and mice are ergonomic."),
        ("Which design factor is about how a product looks?", "aesthetics", ["safety", "function", "durability"], "Aesthetics is about appearance."),
        ("What is universal design?", "designing spaces and products that everyone can use, including people with disabilities", ["designing only for children", "designing only for athletes", "a kind of bridge"], "Ramps and automatic doors are examples."),
        ("Why are I-beams used in buildings?", "Their shape is strong while using less material.", ["They are round.", "They are made of wood only.", "They are flexible like rubber."], "The flanges resist bending."),
        ("What is a truss?", "a frame made of triangles that spreads loads", ["a solid concrete block", "a dome", "a single beam"], "Many bridges and roofs use trusses."),
        ("Why are triangles used in roof trusses?", "Triangles are rigid and do not change shape under a load.", ["They use more wood.", "They look like mountains.", "They let rain in."], "A triangle can only change shape if a side bends or breaks."),
        ("Which structure is designed to resist the force of moving water?", "a dam that is thicker at the bottom", ["a thin tent", "a paper cup", "a kite"], "Water pressure is greatest at the bottom."),
        ("What is the centre of gravity?", "the point where all of an object's weight seems to act", ["the top of the object", "the centre of Earth", "the heaviest corner"], "A low centre of gravity improves stability."),
        ("Why do racing cars sit low to the ground?", "A low centre of gravity keeps them stable in turns.", ["To go under bridges", "To be lighter", "To see the road better"], "Low and wide is stable."),
        ("Which is a composite material?", "fibreglass (glass fibres in plastic)", ["pure copper", "a single rock", "water"], "Composites combine materials for better properties."),
        ("Why are hockey sticks often made of carbon fibre?", "It is strong and light.", ["It is very heavy.", "It is soft.", "It dissolves in water."], "Materials are chosen for their properties."),
        ("What is a design brief?", "a statement of the problem, the criteria and the constraints for a design", ["a short play", "a finished product", "a list of prices only"], "Engineers start with a brief."),
        ("What is a constraint in a design challenge?", "a limit, such as cost, time or materials", ["the colour you like best", "the final product", "a kind of joint"], "Constraints limit possible solutions."),
        ("Why should engineers think about the whole life of a product?", "to reduce waste and environmental harm from making, using and throwing it away", ["to make it break sooner", "to use more energy", "because it is the law in every country"], "Sustainable design looks at the full life cycle."),
        ("What is the purpose of a factor of safety?", "to make a structure stronger than it needs to be in case of extra loads", ["to make it weaker", "to save money only", "to make it taller"], "Bridges are built to hold more than normal traffic."),
        ("Which joint lets a structure move, like a door?", "a hinge (movable joint)", ["a weld", "glue", "a rivet"], "Some joints are rigid; others allow movement."),
        ("Why are suspension bridge towers so tall?", "Tall towers hold the main cables that carry the deck's weight in tension.", ["For decoration only", "To catch the wind", "To store water"], "Cables pull up on the deck."),
        ("Why are snowshoes wide?", "to spread the person's weight over a large area so they do not sink", ["to make walking harder", "to keep feet warm", "to go faster downhill"], "Form matches function."),
        ("A shelf bends under a load. Which change will reduce bending the most?", "make the shelf thicker or add a support in the middle", ["make it longer", "make it thinner", "move the books to the middle"], "Thicker beams resist bending."),
        ("What is the profile of a structure?", "its outline shape as seen from the side", ["its colour", "its weight", "its age"], "A lower profile is often more stable."),
    ])
    fk = X.f(force_kind)
    p5 = X.pool(FORCE_ROWS)
    return [
        ("Form follows function", [(pool, 8), (p5, 4), (fk, 3), (X.gen(US3F, "g_change"), 5)]),
        ("Forces on structures", [(fk, 6), (p5, 6), (X.gen(UK7F, "g_name"), 4), (X.gen(US3F, "g_still"), 4)]),
        ("Stability and centre of gravity", [(pool, 6), (p5, 6), (X.gen(US3F, "g_pic", n=4), 4), (X.gen(UK7F, "g_bal"), 4)]),
        ("Materials and joints", [(pool, 6), (p5, 6), (fk, 2), (X.gen(US2B, "g_same", n=3), 3), (X.gen(UK7F, "g_spring", n=3), 3)]),
        ("Design criteria and testing", [(pool, 5), (p5, 6), (X.B(US3F, "B5"), 4), (X.B(UK7F, "B5"), 3), (fk, 2)]),
    ]


def s_heat(X):
    pool = X.pool([
        ("What is the difference between heat and temperature?", "Temperature measures how hot something is; heat is energy moving from warmer to cooler.", ["They are exactly the same.", "Heat is measured with a ruler.", "Temperature is a kind of fuel."], "Heat flows from hot to cold."),
        ("Which way does heat flow?", "from a warmer object to a cooler one", ["from a cooler object to a warmer one", "only upward", "only downward"], "Cold is not a thing that flows."),
        ("What is conduction?", "heat moving through a material by particles bumping into each other", ["heat carried by moving liquid or gas", "heat travelling as waves through space", "heat made by magnets"], "A metal spoon in hot soup gets hot by conduction."),
        ("What is convection?", "heat carried by the movement of a liquid or gas", ["heat moving through a solid only", "heat as light from the Sun", "heat stopped by a vacuum"], "Warm air rises and cool air sinks."),
        ("What is radiation (of heat)?", "heat travelling as invisible waves, even through empty space", ["heat moving by touching", "warm water rising", "a kind of pollution only"], "The Sun warms Earth by radiation."),
        ("How does the Sun's heat reach Earth?", "by radiation", ["by conduction", "by convection", "through wires"], "Space is almost empty, so only radiation works."),
        ("Why does a hot-air register near the floor warm a whole room?", "Warm air rises and cool air sinks, making a convection current.", ["Heat only moves down.", "Air does not move.", "The floor conducts all the heat."], "Convection circulates the air."),
        ("Why are pot handles made of plastic or wood?", "They are insulators, so they do not conduct heat to your hand.", ["They conduct heat well.", "They look nice only.", "They make the pot heavier."], "Insulators slow heat flow."),
        ("What happens to the particles of a substance when it is heated?", "They move faster and spread out.", ["They stop moving.", "They shrink.", "They disappear."], "This is why most things expand when heated."),
        ("Why do sidewalks have gaps between the concrete slabs?", "Concrete expands in heat and the gaps stop it cracking.", ["To let grass grow", "To make walking harder", "To drain the snow only"], "Thermal expansion."),
        ("How does a thermometer work?", "The liquid inside expands when heated and rises up the tube.", ["The glass gets bigger.", "The liquid shrinks when heated.", "It uses magnets."], "Liquids expand when heated."),
        ("What temperature does water freeze at?", "0 °C", ["100 °C", "32 °C", "−100 °C"], "Water boils at 100 °C at sea level."),
        ("Why do houses in Ontario have insulation in the walls and attic?", "to slow heat loss in winter and keep heat out in summer", ["to make houses heavier", "to conduct heat outside", "to keep insects in"], "Insulation saves energy."),
        ("Why does a dark car get hotter in the sun than a white car?", "Dark colours absorb more radiant energy.", ["Dark colours reflect more light.", "White cars have no metal.", "The engine is bigger."], "Light colours reflect radiation."),
        ("Why do lakes in Ontario freeze from the top down?", "Ice is less dense than water, so it floats.", ["The bottom is always warmer than 30 °C.", "Ice sinks.", "Wind pushes the ice up."], "Fish survive in the water under the ice."),
        ("A thermos keeps soup hot. How?", "Its vacuum layer stops conduction and convection, and shiny walls reduce radiation.", ["It heats the soup.", "It is made of conducting metal only.", "It lets air flow through."], "It blocks all three kinds of heat transfer."),
    ])
    return [
        ("Heat and temperature", [(pool, 6), (X.gen(US6T, "g_te"), 4), (X.gen(US6T, "g_energy"), 6), (X.gen(SG4H, "g_flow"), 4)]),
        ("Conduction, convection and radiation", [(X.gen(US6D, "g_kind"), 6), (X.gen(SG2H, "g_way"), 6), (X.gen(UK9T, "g_way"), 4), (pool, 4)]),
        ("Conductors and insulators", [(X.gen(SG4C, "g_class"), 6), (X.gen(SG4C, "g_use"), 5), (X.gen(US6T, "g_material", n=5), 5), (pool, 4)]),
        ("Expansion and states of matter", [(X.gen(SG4H, "g_expand"), 6), (X.gen(US6P, "g_change", n=5), 5), (X.gen(US6P, "g_curve", n=4), 4), (pool, 5)]),
        ("Controlling heat transfer", [(X.gen(US6D, "g_example"), 5), (X.gen(US6D, "g_material", n=5), 5), (X.gen(US6D, "g_test", n=4), 4), (X.B(US6D, "B5"), 3), (X.gen(SG4H, "g_cool"), 3)]),
    ]


def s_heatenv(X):
    pool = X.pool([
        ("What is the greenhouse effect?", "gases in the atmosphere trap heat and keep Earth warm", ["a greenhouse on a farm only", "the Sun getting hotter", "the ozone hole"], "Without it, Earth would be frozen."),
        ("Which gas from burning fossil fuels adds most to the greenhouse effect?", "carbon dioxide", ["oxygen", "nitrogen", "helium"], "More CO₂ traps more heat."),
        ("What is climate change?", "long-term changes in Earth's temperatures and weather patterns", ["a cold day", "one big storm", "the change from day to night"], "Weather is day to day; climate is over many years."),
        ("Which is a sign of climate change in Ontario?", "lakes freezing later and thawing earlier than in the past", ["more snow every single year", "no change at all", "the Sun rising in the west"], "Ice-cover data shows the change."),
        ("Why do cities feel hotter than the countryside on summer days?", "Pavement and buildings absorb heat and there are fewer trees (the urban heat island effect).", ["Cities are closer to the Sun.", "Cities have more wind.", "Cities have more lakes."], "Trees and green roofs cool cities."),
        ("Which heat source comes from inside Earth?", "geothermal energy", ["solar energy", "wind energy", "tidal energy"], "Ground-source heat pumps use it."),
        ("How does a heat pump warm a house?", "It moves heat from the outside air or ground into the house.", ["It burns wood.", "It makes heat from nothing.", "It uses ice cubes."], "Heat pumps are efficient."),
        ("Which is a renewable source of heat?", "the Sun (solar heating)", ["natural gas", "heating oil", "coal"], "Solar energy will not run out."),
        ("Why do ocean currents and winds move heat around the planet?", "Uneven heating makes warm fluids rise and cool fluids sink, causing currents.", ["The Moon pushes them.", "Fish swim in circles.", "Earth is flat."], "Convection on a planet-wide scale."),
        ("How can planting trees help keep a house cool?", "Trees shade the house and release water vapour that cools the air.", ["Trees make heat.", "Trees block all wind forever.", "Trees reflect sound."], "Shade reduces air-conditioning use."),
        ("Why do Indigenous communities' traditional homes, like the longhouse or igloo, suit their climates?", "They use local materials that hold or block heat to keep people comfortable.", ["They were built only for looks.", "They have no relation to climate.", "They were all made of metal."], "Snow is a good insulator in an igloo."),
        ("Which action reduces the energy used to heat a home?", "sealing drafts around windows and doors", ["leaving windows open in winter", "removing insulation", "turning the heat to the highest setting"], "Weatherstripping keeps heat in."),
        ("Why is permafrost thawing in northern Canada a problem?", "Buildings and roads sink, and stored greenhouse gases are released.", ["It makes soil frozen forever.", "It adds more ice.", "It has no effect."], "Warming changes northern landscapes."),
        ("What is thermal pollution?", "warm water released into rivers or lakes that harms aquatic life", ["smoke from a fire", "noisy machines", "plastic in the ocean"], "Warm water holds less oxygen."),
    ])
    return [
        ("The greenhouse effect", [(pool, 6), (X.gen(US6G, "g_cause"), 6), (X.gen(US6G, "g_co2"), 4), (X.gen(UK8A, "g_comp"), 4)]),
        ("Climate change evidence", [(X.gen(US6G, "g_evid"), 5), (X.gen(UK8A, "g_ppm", n=5), 5), (X.gen(UK8A, "g_cc"), 5), (pool, 5)]),
        ("Heat sources and fuels", [(X.gen(UK8A, "g_ff"), 5), (X.gen(UK8A, "g_src"), 5), (pool, 6), (X.B(US6G, "B1"), 4)]),
        ("Saving heat and energy", [(pool, 6), (X.gen(US6D, "g_example", n=4), 4), (X.gen(SG4C, "g_use", n=4), 4), (X.B(US6T, "B1"), 3), (X.B(UK9T, "B1"), 3)]),
        ("Heat in the environment investigations", [(X.B(US6G, "B5"), 4), (X.B(UK8A, "B5"), 5), (X.B(US6T, "B5"), 4), (X.gen(US6G, "g_temp"), 3), (pool, 4)]),
    ]


def UNITS():
    return [
        CU("B", 1, "interactions-in-ecosystems", "B2.1, B2.2, B2.3, B2.4",
           "Describe ecosystems in terms of biotic and abiotic factors; explain symbiotic relationships, energy flow and the cycling "
           "of matter; describe how populations are limited and how ecosystems change through succession.",
           "Interactions in Ecosystems", "Interactions in ecosystems",
           "Free Grade 7 science worksheets on biotic and abiotic factors, symbiosis, energy pyramids, populations and succession. "
           "100 questions with answers.",
           "Living and non-living parts interact.", "Energy flows through food webs; matter cycles; populations are limited by resources.",
           L("An ecosystem is the living (biotic) and non-living (abiotic) parts of an area and how they interact.",
             "Symbiosis: mutualism (both benefit), commensalism (one benefits) and parasitism (one is harmed).",
             "Only about 10% of the energy at one level passes to the next, so food chains are short.",
             "Food, water, space and predators limit populations; succession slowly changes an ecosystem over time."),
           [("A tick feeds on a moose. What relationship is this?", ["the tick benefits", "the moose is harmed"], "parasitism"),
            ("Is sunlight biotic or abiotic?", ["it is not living"], "abiotic")],
           ["Thinking energy is recycled like matter (it flows one way).", "Mixing up commensalism and mutualism.", "Thinking populations can grow forever."],
           [("What is the difference between biotic and abiotic factors?", "Biotic factors are living things. Abiotic factors are non-living, like sunlight, water and temperature."),
            ("Why are there fewer top predators than producers?", "Energy is lost at each level, so there is less energy available for animals at the top."),
            ("What is succession?", "The slow change in the plants and animals of an ecosystem over time, such as a burned forest growing back.")],
           s_eco),
        CU("B", 2, "human-impact-and-sustainability", "B1.1, B1.2, B2.5, B2.6",
           "Assess the effects of human activities on ecosystems, including pollution, bioaccumulation and habitat loss; evaluate "
           "sustainable practices, including Indigenous perspectives such as Seven Generations thinking.",
           "Human Impact and Sustainability", "Human impact and sustainability",
           "Free Grade 7 science worksheets on human impact on ecosystems, pollution, bioaccumulation, the 3 Rs and sustainable "
           "choices. 100 questions with answers.",
           "Our choices affect ecosystems.", "Pollution and habitat loss harm ecosystems; sustainable choices protect them for the future.",
           L("People change ecosystems by building, farming, polluting and using resources.",
             "Toxins such as mercury and pesticides build up in food chains (bioaccumulation and biomagnification).",
             "Sustainability means meeting our needs without harming future generations.",
             "Reduce, reuse, recycle, protect habitats and restore damaged areas."),
           [("Why do eagles have more pesticide than fish?", ["toxins build up at each level"], "biomagnification"),
            ("Which of the 3 Rs is best?", ["not making waste at all"], "reduce")],
           ["Thinking recycling alone solves waste problems.", "Thinking toxins spread out evenly in a food chain.", "Thinking one person's choices do not matter."],
           [("What is bioaccumulation?", "The build-up of a toxic substance in an organism's body over time."),
            ("What is a sustainable practice?", "A way of using resources that can continue for a long time without harming the environment, like replanting forests."),
            ("What does Seven Generations thinking mean?", "Making decisions that will still be good for people seven generations into the future.")],
           s_impact),
        CU("C", 3, "pure-substances-and-mixtures", "C2.1, C2.2, C2.3",
           "Use the particle theory to describe pure substances and mixtures; distinguish elements and compounds; classify mixtures "
           "as mechanical mixtures, suspensions and solutions.",
           "Pure Substances and Mixtures", "Pure substances and mixtures",
           "Free Grade 7 science worksheets on the particle theory, pure substances, elements, compounds and kinds of mixtures. "
           "100 questions with answers.",
           "A pure substance has one kind of particle.", "Mixtures have two or more; you can see the parts of a mechanical mixture but not of a solution.",
           L("All matter is made of particles that are always moving and have spaces between them.",
             "Pure substances have only one kind of particle: elements (one kind of atom) and compounds (atoms joined).",
             "Mixtures have two or more substances: mechanical mixtures, suspensions and solutions.",
             "A solution looks like one substance because the solute is dissolved."),
           [("Is salt water a pure substance?", ["it has salt and water"], "no, it is a solution"),
            ("Is water an element or a compound?", ["H₂O has hydrogen and oxygen"], "a compound")],
           ["Thinking 'pure' means 'clean' or 'natural'.", "Thinking solutions are pure substances because they look the same.", "Mixing up elements and compounds."],
           [("What is the particle theory of matter?", "All matter is made of tiny particles that are always moving, have spaces between them and attract each other. Heat makes them move faster."),
            ("What is the difference between an element and a compound?", "An element has only one kind of atom. A compound has two or more kinds of atoms joined together."),
            ("What are the kinds of mixtures?", "Mechanical mixtures (parts visible), suspensions (cloudy, settle out) and solutions (look like one substance).")],
           s_pure),
        CU("C", 4, "solutions-and-separating-mixtures", "C2.4, C2.5, C1.1",
           "Describe solutes, solvents, solubility and concentration; identify factors that affect the rate of dissolving; explain "
           "methods for separating mixtures and how they are used in industry and to protect the environment.",
           "Solutions and Separating Mixtures", "Solutions and separating mixtures",
           "Free Grade 7 science worksheets on solutes and solvents, solubility, concentration, saturated solutions, filtration, "
           "evaporation, chromatography and distillation. 100 questions with answers.",
           "The solute dissolves in the solvent.", "Heat, stirring and small pieces speed up dissolving; filters, magnets and evaporation separate mixtures.",
           L("In a solution, the solute dissolves in the solvent.",
             "Solubility is how much solute can dissolve; a saturated solution can hold no more.",
             "Dissolving is faster with higher temperature, stirring and smaller pieces.",
             "Separation methods: sieving, filtering, magnets, evaporation, distillation and chromatography."),
           [("Which method gets salt back from salt water?", ["the water can leave as vapour"], "evaporation"),
            ("A solution has 15 g of sugar in 50 mL. What is the concentration?", ["15 ÷ 50 = 0.3"], "0.3 g/mL")],
           ["Thinking a dissolved solute has disappeared.", "Thinking filtering can remove dissolved salt.", "Mixing up solute and solvent."],
           [("What is the difference between a solute and a solvent?", "The solute is what dissolves (like sugar). The solvent is what it dissolves in (like water)."),
            ("Why can you not filter salt out of salt water?", "The salt particles are dissolved and small enough to pass through the filter."),
            ("Where is separation used in real life?", "Water treatment, recycling plants, oil refineries, mining and cleaning up spills.")],
           s_sep),
        CU("D", 5, "form-and-function", "D2.1, D2.2, D2.3, D2.4, D1.1",
           "Describe how the form of a structure relates to its function; identify internal and external forces and the centre of "
           "gravity; explain how materials, joints and shapes affect strength and stability; apply design criteria such as safety, "
           "cost, ergonomics, aesthetics and sustainability.",
           "Form and Function of Structures", "Form and function",
           "Free Grade 7 science worksheets on form and function, forces on structures, stability, centre of gravity, materials, "
           "trusses and design criteria. 100 questions with answers.",
           "A structure's form must suit its function.", "Shape, materials, joints and a low centre of gravity make structures strong and stable.",
           L("Every structure has a function (its job) and a form (its shape and size).",
             "Internal forces: tension, compression, torsion and shear. External forces: loads such as weight, wind and snow.",
             "Triangles, trusses, I-beams and arches add strength; a low centre of gravity and wide base add stability.",
             "Designers balance function, safety, cost, ergonomics, aesthetics and environmental impact."),
           [("Why are roof trusses made of triangles?", ["triangles are rigid"], "they do not change shape under a load"),
            ("Why do racing cars sit low?", ["low centre of gravity"], "for stability")],
           ["Thinking the strongest design is always the best (cost and weight matter too).", "Thinking a taller structure is more stable.", "Mixing up form and function."],
           [("What is the difference between form and function?", "Form is the shape and size of a structure. Function is the job it does."),
            ("How does the centre of gravity affect stability?", "A structure is more stable when its centre of gravity is low and over a wide base."),
            ("What is ergonomics?", "Designing products to fit the human body so they are comfortable and safe to use.")],
           s_form),
        CU("E", 6, "heat-and-temperature", "E2.1, E2.2, E2.3, E2.4",
           "Distinguish between heat and temperature using the particle theory; describe conduction, convection and radiation; "
           "explain how conductors and insulators are used to control heat transfer.",
           "Heat and Temperature", "Heat and temperature",
           "Free Grade 7 science worksheets on heat and temperature, the particle theory, conduction, convection, radiation, "
           "insulators and thermal expansion. 100 questions with answers.",
           "Heat flows from warmer to cooler.", "Heat moves by conduction, convection and radiation; insulators slow it down.",
           L("Temperature measures how fast particles are moving. Heat is energy moving from a warmer object to a cooler one.",
             "Conduction: through a solid, by particles bumping. Convection: by moving liquids and gases. Radiation: as waves, even through space.",
             "Metals are good conductors; air, wool, foam and plastic are insulators.",
             "Most substances expand when heated and contract when cooled."),
           [("How does the Sun's heat reach Earth?", ["space is almost empty"], "radiation"),
            ("Why does a metal spoon in hot tea get hot?", ["particles bump through the metal"], "conduction")],
           ["Thinking 'cold' flows into things.", "Thinking heat and temperature are the same.", "Thinking insulators make things warm (they only slow heat flow)."],
           [("What is the difference between heat and temperature?", "Temperature tells how hot something is. Heat is the energy that moves from hotter to colder things."),
            ("What are the three ways heat moves?", "Conduction (through solids), convection (by moving fluids) and radiation (as waves)."),
            ("Why do sweaters keep us warm?", "They trap air, which is an insulator, so our body heat escapes more slowly.")],
           s_heat),
        CU("E", 7, "heat-in-the-environment", "E1.1, E1.2, E2.5, E2.6",
           "Describe how heat moves in the environment, including the greenhouse effect and convection in air and water; assess "
           "the effects of climate change and human uses of heat; evaluate ways to conserve energy.",
           "Heat in the Environment", "Heat in the environment",
           "Free Grade 7 science worksheets on the greenhouse effect, climate change, heat sources, heat pumps and saving energy. "
           "100 questions with answers.",
           "Greenhouse gases trap heat.", "Burning fossil fuels adds CO₂ and warms the climate; insulation and renewable heat save energy.",
           L("The Sun heats Earth unevenly, which drives winds and ocean currents.",
             "Greenhouse gases like carbon dioxide trap heat; more of them make the climate warmer.",
             "Signs in Ontario: shorter ice seasons, warmer winters, more extreme weather.",
             "Insulation, heat pumps, solar heating, trees and sealing drafts reduce energy use."),
           [("Which gas from cars traps heat?", ["burning gasoline makes it"], "carbon dioxide"),
            ("Why are cities hotter than farmland?", ["asphalt absorbs heat", "fewer trees"], "urban heat island")],
           ["Mixing up weather and climate.", "Thinking the greenhouse effect is only bad (it keeps Earth livable).", "Thinking the ozone hole causes global warming."],
           [("What is the greenhouse effect?", "Gases in the air trap some of the heat radiated from Earth, keeping the planet warm."),
            ("How is climate change affecting Ontario?", "Winters are warmer, lakes freeze later, and heat waves and heavy storms are more common."),
            ("How can we reduce heat loss from homes?", "Add insulation, seal drafts, use efficient windows and heat pumps, and lower the thermostat.")],
           s_heatenv),
    ]
