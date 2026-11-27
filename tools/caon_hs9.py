# -*- coding: utf-8 -*-
"""Ontario Grade 9 science: SNC1W (2022). Built with caon_hs."""
from caon_hs import HU

G = "gen_us_science_"

SPACE = [
    ("What does the Canadarm do on a space station or shuttle?", "it is a robotic arm that moves equipment, catches spacecraft and helps astronauts", ["it launches rockets into orbit", "it measures the temperature of the Sun", "it makes oxygen for the crew"], "The Canadarm, Canadarm2 and Dextre are Canadian robotic systems used in space."),
    ("How do satellites help us study climate change?", "they measure ice cover, sea level, sea-surface temperature and greenhouse gases from orbit", ["they cool Earth by blocking sunlight", "they make rain fall over deserts", "they remove carbon dioxide from the air"], "Remote sensing from orbit gives regular data for the whole planet."),
    ("What is remote sensing?", "collecting information about Earth from a distance, for example with satellite images", ["sending astronauts to the Moon", "listening to radio stations far away", "measuring soil with a probe in the ground"], "Satellites carry cameras and sensors that record light, heat and radar signals."),
    ("Which technology uses signals from several satellites to find your position?", "GPS (global positioning system)", ["a solar panel", "a telescope mirror", "a seismograph"], "A receiver times signals from at least four satellites to work out its position."),
    ("Why are many telescopes placed in space instead of on the ground?", "Earth's atmosphere blurs light and absorbs some wavelengths, such as X-rays and much infrared", ["telescopes are cheaper to build in space", "stars are much closer in orbit", "there is more light in space at night"], "The James Webb Space Telescope observes infrared light that the atmosphere would block."),
    ("What is space debris?", "old satellites, rocket stages and fragments left in orbit", ["meteorites that land on Earth", "dust between the stars", "clouds of gas around the Sun"], "Even small pieces move at about 28 000 km/h and can damage working spacecraft."),
    ("Why is space debris a growing problem?", "collisions make more pieces, which can damage satellites and the space station", ["it makes the Moon brighter", "it blocks all sunlight from Earth", "it changes Earth's gravity"], "More launches and collisions add to the debris; agencies track larger pieces."),
    ("What is a spin-off technology?", "a product first developed for space that is later used on Earth", ["a satellite that spins to stay stable", "a rocket that is used again", "a planet that spins quickly"], "Examples include better water filters, memory foam and scratch-resistant lenses."),
    ("How do satellites help during forest fires and floods?", "they map the area so emergency crews can see where help is needed", ["they put out the fires with water", "they stop the rain from falling", "they move people to safety"], "Radar satellites such as Canada's RADARSAT can see through cloud and smoke."),
    ("What can RADARSAT satellites see that ordinary cameras cannot?", "the ground through clouds and darkness, using radar", ["the inside of the Sun", "planets around other stars", "sound waves in the ocean"], "Radar sends out microwaves and records the echoes, so it works day and night."),
    ("Which is a risk to astronauts' health on long missions?", "bone and muscle loss in microgravity and higher radiation", ["catching colds from the vacuum", "getting too much oxygen", "growing taller by a metre"], "Astronauts exercise about two hours a day on the space station."),
    ("Why do astronauts on the space station exercise every day?", "in microgravity, bones and muscles weaken because they do not support the body's weight", ["to keep the station moving", "to make electricity for the station", "to keep warm in space"], "Treadmills, bikes and resistance machines slow bone and muscle loss."),
    ("What powers most satellites and the space station?", "solar panels", ["coal", "wind turbines", "gasoline engines"], "Sunlight is strong and constant in orbit, and the panels charge batteries for the dark part of each orbit."),
    ("What is one economic benefit of space exploration for Canada?", "jobs and companies that build satellites, robotics and space technology", ["it lowers the price of gold", "it replaces the need for farming", "it stops weather from changing"], "Canada's space industry builds robotics, satellites and communication systems."),
    ("What is one environmental concern about rocket launches?", "they release exhaust gases and particles into the atmosphere", ["they make the Moon move away", "they cool the oceans", "they stop photosynthesis"], "Launches also add to space debris if stages are left in orbit."),
    ("How did satellites change weather forecasting?", "they track clouds and storms over oceans and remote areas in real time", ["they control where hurricanes go", "they make the weather the same everywhere", "they replaced thermometers on the ground"], "Images every few minutes let forecasters follow storms as they develop."),
    ("Which kind of orbit keeps a satellite above the same spot on the equator?", "geostationary orbit", ["low Earth orbit", "polar orbit", "an orbit around the Moon"], "At about 36 000 km up, the satellite circles once a day, matching Earth's rotation."),
    ("Why do Earth-observation satellites often use polar orbits?", "Earth turns below them, so they pass over every part of the planet", ["they stay over one city all the time", "they are closer to the Sun", "they need no fuel at the poles"], "Each orbit passes near both poles while Earth rotates underneath."),
    ("What did the Hubble Space Telescope help astronomers measure?", "the expansion of the universe and the distances to galaxies", ["the temperature of Earth's core", "the depth of the oceans", "the speed of sound in air"], "Hubble observations of distant galaxies refined the age of the universe to about 13.8 billion years."),
    ("Why do some Indigenous knowledge keepers and scientists both study the night sky?", "the sky has been used for navigation, calendars and stories for thousands of years", ["the stars control the weather", "the sky only changes once a century", "stars can be seen only from space"], "Many peoples used star patterns to mark seasons for hunting, fishing and planting."),
    ("Why do astronauts need spacesuits on a spacewalk?", "space has no air to breathe, almost no pressure, extreme temperatures and strong radiation", ["the suits make them float", "the suits stop gravity from acting", "the suits let them breathe the gases in space"], "The suit is a small spacecraft with its own air, pressure, cooling and radiation shield."),
    ("Which instrument on a satellite measures heat given off by the ground and oceans?", "an infrared sensor", ["a microphone", "a compass", "a barometer"], "Warm objects give off infrared radiation, so the sensor can map temperatures."),
    ("How do communication satellites help remote northern communities?", "they relay phone, internet and television signals where there are no cables", ["they bring food by air", "they keep the communities warm", "they melt snow on the roads"], "Many Arctic communities depend on satellite links for internet and health services."),
    ("What is one reason space exploration is expensive?", "rockets, spacecraft and life-support systems must be built and tested to be extremely reliable", ["fuel is free but the paint is costly", "space has no gravity, so nothing can be built", "satellites can only be launched once a century"], "Agencies share costs through international projects such as the space station."),
    ("How can satellite data help farmers?", "images show which parts of a field are dry, unhealthy or need fertilizer", ["satellites plant the seeds", "satellites stop insects from eating crops", "satellites make the growing season longer"], "This is called precision agriculture."),
    ("Which body is the next major human destination planned by NASA's Artemis program, with Canadian participation?", "the Moon", ["Mars's moon Phobos", "the Sun", "Jupiter"], "Canada is building Canadarm3 for the Gateway station that will orbit the Moon."),
]

CLIMATE = [
    ("Which farming practice keeps carbon in the soil?", "planting cover crops and leaving crop remains on the field (no-till)", ["burning crop remains after harvest", "ploughing the field many times", "leaving the soil bare all winter"], "Plant roots and remains add organic matter, and less ploughing releases less CO₂."),
    ("What is crop rotation?", "growing different crops in a field in different years", ["growing the same crop every year", "turning the soil upside down", "watering crops at night"], "Rotation keeps soil healthy, breaks pest cycles and can add nitrogen (with legumes such as beans)."),
    ("Why does growing beans, peas or clover help the next crop?", "bacteria in their roots fix nitrogen, which fertilizes the soil", ["they block all sunlight from weeds", "they remove all water from the soil", "they make the soil more acidic for good"], "Legumes reduce the need for synthetic fertilizer."),
    ("What is the Three Sisters planting method?", "growing corn, beans and squash together so each plant helps the others", ["planting three rows of the same crop", "farming on three different fields", "watering crops three times a day"], "Corn supports the beans, beans add nitrogen and squash leaves shade the soil and keep moisture in."),
    ("How do wetlands help reduce the effects of climate change?", "they store carbon and soak up floodwater", ["they release extra heat", "they make droughts worse", "they speed up melting ice"], "Peatlands and marshes hold large amounts of carbon in waterlogged soil."),
    ("Why does cutting down a forest add to climate change?", "fewer trees take in CO₂, and burning or rotting wood releases stored carbon", ["trees produce carbon dioxide in photosynthesis", "forests make the air colder", "forests block greenhouse gases from reaching space"], "Forests are carbon sinks; removing them turns a sink into a source."),
    ("Which change reduces greenhouse gas emissions from transportation?", "taking transit, cycling or using electric vehicles charged from clean electricity", ["driving alone more often", "idling the car to keep it warm", "buying a bigger gasoline vehicle"], "Most transport emissions come from burning gasoline and diesel."),
    ("What is a carbon sink?", "something that takes in more carbon dioxide than it releases, such as a forest or the ocean", ["a factory that burns coal", "a car engine", "a volcano erupting"], "Oceans, soils and forests remove CO₂ from the atmosphere."),
    ("Why is melting permafrost a concern in northern Canada?", "it releases stored carbon dioxide and methane and damages roads and buildings", ["it makes the ground stronger", "it lowers sea level everywhere", "it stops all plant growth"], "Thawing frozen soil lets microbes break down old organic matter."),
    ("How does climate change affect many northern and Inuit communities?", "thinner, less predictable sea ice makes travel, hunting and food supply harder", ["sea ice is getting thicker every year", "there is no change in the Arctic", "winters are becoming much longer"], "The Arctic is warming about three to four times faster than the global average."),
    ("What is one sign that an ecosystem is in dynamic equilibrium?", "population sizes rise and fall but stay within a stable range over time", ["one species takes over and all others disappear", "nothing ever changes", "all the plants die each summer"], "Matter cycles and energy flows keep balancing each other."),
    ("Which action improves soil health on a farm?", "adding compost and keeping plants growing on the soil", ["spraying extra pesticide every week", "removing all earthworms", "packing the soil with heavy machines"], "Organic matter feeds soil organisms and helps the soil hold water."),
    ("Why does using less fertilizer protect lakes?", "extra nitrogen and phosphorus wash into water and cause algal blooms", ["fertilizer makes lakes too cold", "fertilizer stops evaporation", "fertilizer adds too much salt to the ocean"], "When the algae die, decomposers use up the oxygen, and fish can die."),
    ("What is a climate change indicator?", "a measurement that shows how the climate is changing, such as sea-ice extent or average temperature", ["the weather forecast for tomorrow", "the time of sunrise", "the number of cars sold"], "Indicators are tracked over many years to show trends."),
    ("Which is an example of adapting to climate change rather than slowing it?", "building higher flood walls and planting trees for shade in cities", ["switching from coal to wind power", "planting forests to absorb CO₂", "driving less"], "Mitigation reduces the cause; adaptation reduces the damage."),
]


def UNITS():
    return [
        HU("SNC1W", "B", 1, "ecosystems-and-sustainability", "B2.2, B2.3, B2.4, B2.5",
           "How matter cycles and energy flows keep ecosystems in dynamic equilibrium; how photosynthesis and cellular respiration balance each other; "
           "the role of biodiversity, air, water and soil quality and succession in sustainability; and how human activities affect ecosystems.",
           "Ecosystems and Sustainability", "ecosystems and sustainability",
           "Free Grade 9 Science (SNC1W) worksheets on ecosystems and sustainability: food webs, energy pyramids, the carbon cycle, photosynthesis and respiration, biodiversity, succession and human impact. 100 questions with answers.",
           "Energy flows through an ecosystem; matter cycles round and round.", "Only about 10% of the energy passes to the next trophic level.",
           "<p>Producers capture the Sun's energy in photosynthesis. Consumers get energy by eating, and at each trophic level most of the energy (about 90%) is used or lost as heat, "
           "so only about 10% passes on. That is why food chains are short and there are fewer top predators.</p>"
           "<p>Matter is recycled: carbon moves between the air, living things, soil and oceans through photosynthesis, respiration, decomposition and combustion. "
           "Photosynthesis (CO₂ + H₂O → glucose + O₂) and cellular respiration (the reverse) balance each other. Biodiversity, healthy soil and clean water help an ecosystem recover from change.</p>",
           [("Producers store 10 000 J. How much energy reaches the secondary consumers?", ["10% to primary: 1000 J", "10% to secondary: 100 J"], "about 100 J"),
            ("Which process returns carbon dioxide to the air?", ["Living things break down glucose for energy."], "cellular respiration (also decomposition and burning)")],
           ["Saying energy is recycled: energy flows, matter cycles.", "Drawing food-web arrows from the eater to the food: they point to the eater.", "Thinking plants do not respire."],
           [("What is ecological succession?", "The gradual change in the species living in an area, for example after a fire, until a stable community forms."),
            ("Why is biodiversity important?", "An ecosystem with many species has more ways to adapt and recover when conditions change.")],
           lambda X: [
               ("Energy flow and food webs", [(X.gen(G + "bio_energy_flow_and_matter_cycling", "g_ten"), 7), (X.gen(G + "bio_energy_flow_and_matter_cycling", "g_pyr"), 5), (X.gen(G + "bio_energy_flow_and_matter_cycling", "g_lvl"), 4), (X.gen(G + "g7_cycling_of_matter_and_energy_flow", "g_energy"), 4)]),
               ("Cycling of matter", [(X.gen(G + "bio_carbon_cycle", "g_proc"), 6), (X.gen(G + "bio_carbon_cycle", "g_path"), 5), (X.gen(G + "g7_cycling_of_matter_and_energy_flow", "g_cycle"), 5), (X.gen(G + "bio_energy_flow_and_matter_cycling", "g_matter"), 4)]),
               ("Photosynthesis and cellular respiration", [(X.gen(G + "g7_photosynthesis", "g_io"), 6), (X.gen(G + "g7_cellular_respiration", "g_io"), 5), (X.gen(G + "g7_cellular_respiration", "g_compare"), 4), (X.gen(G + "bio_photosynthesis", "g_ratio"), 5)]),
               ("Biodiversity and succession", [(X.gen(G + "bio_ecosystem_stability_and_biodiversity", "g_succ"), 6), (X.gen(G + "bio_ecosystem_stability_and_biodiversity", "g_dist"), 4), (X.gen(G + "bio_ecosystem_stability_and_biodiversity", "g_data"), 4), (X.gen(G + "g7_protecting_biodiversity", "g_serv"), 6)]),
               ("Human activities and ecosystems", [(X.gen(G + "g7_human_impact_on_the_environment", "g_impact"), 6), (X.gen(G + "g7_human_impact_on_the_environment", "g_monitor"), 4), (X.gen(G + "g7_ecosystem_changes", "g_type"), 5), (X.gen(G + "g7_ecosystem_changes", "g_effect"), 5)]),
           ]),
        HU("SNC1W", "B", 2, "climate-change-and-ecosystems", "B1.1, B1.2, B1.3, B2.6, B2.7",
           "Climate change indicators and the human contributions to climate change; the impacts of climate change on ecosystems and on communities in Canada, "
           "including First Nations, Métis and Inuit communities; and sustainable practices, including in agriculture.",
           "Climate Change and Ecosystems", "climate change and ecosystems",
           "Free Grade 9 Science (SNC1W) worksheets on climate change and ecosystems: the greenhouse effect, climate indicators, impacts on ecosystems and communities, carbon footprints and sustainable farming. 100 questions with answers.",
           "Extra greenhouse gases trap more heat and change ecosystems.", "Mitigation cuts emissions; adaptation copes with the changes.",
           "<p>Greenhouse gases (carbon dioxide, methane, water vapour, nitrous oxide) absorb infrared energy given off by Earth's surface and keep the planet warm. "
           "Burning fossil fuels and clearing forests have raised the CO₂ level from about 280 ppm before 1800 to more than 420 ppm today, so more heat is trapped.</p>"
           "<p>Indicators such as rising average temperatures, shrinking sea ice and glaciers, rising sea level and earlier spring melts show the climate is changing. "
           "Ecosystems respond: species shift their ranges, food webs change and some species cannot adapt fast enough. Sustainable practices such as cover crops, crop rotation and protecting wetlands store carbon.</p>",
           [("Why does melting Arctic sea ice speed up warming?", ["Ice reflects sunlight; dark ocean absorbs it."], "the darker ocean absorbs more sunlight, a positive feedback"),
            ("Which gas has increased most because of burning fossil fuels?", ["Fuels contain carbon."], "carbon dioxide")],
           ["Mixing up the greenhouse effect (natural and needed) with the enhanced greenhouse effect.", "Thinking the ozone hole causes global warming.", "Confusing weather (day to day) with climate (30-year averages)."],
           [("Is the greenhouse effect bad?", "No: without it Earth would be about −18 °C. The problem is the extra warming from added greenhouse gases."),
            ("What is a carbon footprint?", "The total greenhouse gases released by a person's or a product's activities, given as a mass of CO₂.")],
           lambda X: [
               ("The greenhouse effect", [(X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_ghg"), 6), (X.gen(G + "ess_climate_and_energy_flow", "g_eff"), 5), (X.gen(G + "g6_global_temperature_and_climate_change", "g_co2"), 4), (X.gen(G + "g6_global_temperature_and_climate_change", "g_cause"), 5)]),
               ("Climate change indicators", [(X.gen(G + "ess_climate_change_data_and_models", "g_rate"), 5), (X.gen(G + "ess_climate_change_data_and_models", "g_sea"), 5), (X.gen(G + "ess_climate_change_data_and_models", "g_ice"), 5), (X.gen(G + "g6_global_temperature_and_climate_change", "g_evid"), 5)]),
               ("Impacts on ecosystems and communities", [(X.gen(G + "ess_climate_change_data_and_models", "g_imp"), 6), (X.gen(G + "ess_feedbacks_in_earth_systems", "g_fb"), 5), (X.gen(G + "ess_feedbacks_in_earth_systems", "g_alb"), 4), (X.pool(CLIMATE[8:11]), 3), (X.gen(G + "ess_climate_change_data_and_models", "g_scen"), 2)]),
               ("Carbon footprints", [(X.gen("gen_uk_science_y11_chemistry_of_the_atmosphere", "g_foot"), 7), (X.gen(G + "ess_sustainability_and_human_impact", "g_foot"), 7), (X.gen(G + "ess_sustainability_and_human_impact", "g_red"), 6)]),
               ("Sustainable practices", [(X.pool(CLIMATE[:8] + CLIMATE[11:]), 10), (X.gen(G + "g7_protecting_biodiversity", "g_sol"), 5), (X.gen(G + "ess_sustainability_and_human_impact", "g_sol"), 5)]),
           ]),
        HU("SNC1W", "C", 3, "atoms-and-the-periodic-table", "C2.2, C2.3, C2.4, C2.5",
           "How experimental evidence led to new atomic models; the location, relative mass and charge of protons, neutrons and electrons in the Bohr–Rutherford model; "
           "the link between an element's position in the periodic table and its atomic structure; and the properties of elements and periodic trends.",
           "Atoms and the Periodic Table", "atoms and the periodic table",
           "Free Grade 9 Science (SNC1W) worksheets on atoms and the periodic table: atomic models, protons, neutrons and electrons, Bohr–Rutherford diagrams, groups and periods, and families of elements. 100 questions with answers.",
           "Protons = atomic number; electrons = protons in a neutral atom.", "Neutrons = mass number − atomic number.",
           "<p>Atomic models changed as new evidence appeared: Dalton (solid spheres), Thomson (electrons in a positive sphere), Rutherford (a tiny dense nucleus) and Bohr (electrons in shells). "
           "Protons (+1) and neutrons (0) are in the nucleus and have about the same mass; electrons (−1) are about 1/1836 of that mass and move around the nucleus.</p>"
           "<p>The atomic number is the number of protons. In a Bohr–Rutherford diagram, shells hold 2, 8, 8 electrons. "
           "Elements in the same group (column) have the same number of valence electrons and similar properties; the period (row) number is the number of occupied shells.</p>",
           [("Sodium-23 (Z = 11). Protons, neutrons, electrons?", ["p = 11, e = 11", "n = 23 − 11 = 12"], "11 protons, 12 neutrons, 11 electrons"),
            ("Draw the shells of magnesium (Z = 12).", ["2 in the first shell, 8 in the second", "2 left for the third"], "2, 8, 2")],
           ["Using the mass number as the number of protons.", "Putting 8 electrons in the first shell.", "Thinking elements in the same period have similar properties: groups do."],
           [("What did Rutherford's gold-foil experiment show?", "Most alpha particles passed through, but a few bounced back, so an atom has a tiny, dense, positive nucleus and is mostly empty space."),
            ("Why are noble gases unreactive?", "Their outer shells are full, so they do not need to gain, lose or share electrons.")],
           lambda X: [
               ("Atomic models", [(X.gen("gen_uk_science_y10_atomic_structure_and_the_periodic_table", "g_hist"), 10), (X.gen("gen_sg_science_s3_particulate_nature_of_matter", "g_part"), 6), (X.gen("gen_sg_science_s1_atoms_and_molecules", "g_part"), 4)]),
               ("Protons, neutrons and electrons", [(X.gen(G + "chem_atomic_structure_and_isotopes", "g_pne"), 7), (X.gen(G + "chem_atomic_structure_and_isotopes", "g_find"), 6), (X.gen("gen_sg_science_s1_atoms_and_molecules", "g_atom"), 7)]),
               ("Bohr–Rutherford diagrams and ions", [(X.gen(G + "chem_atomic_structure_and_isotopes", "g_shell"), 7), (X.gen(G + "chem_atomic_structure_and_isotopes", "g_ion"), 6), (X.gen("gen_sg_science_s3_particulate_nature_of_matter", "g_conf"), 7)]),
               ("Organizing the periodic table", [(X.gen(G + "chem_periodic_table_and_trends", "g_loc"), 6), (X.gen(G + "chem_periodic_table_and_trends", "g_val"), 5), (X.gen(G + "chem_periodic_table_and_trends", "g_class"), 5), (X.gen(G + "chem_periodic_table_and_trends", "g_table"), 4)]),
               ("Families and their properties", [(X.gen(G + "chem_periodic_table_and_trends", "g_fam"), 5), (X.gen(G + "chem_periodic_table_and_trends", "g_react"), 5), (X.gen("gen_sg_science_s4_patterns_in_the_periodic_table", "g_g1"), 5), (X.gen("gen_sg_science_s4_patterns_in_the_periodic_table", "g_g17"), 5)]),
           ]),
        HU("SNC1W", "C", 4, "elements-and-compounds", "C1.1, C1.2, C2.1, C2.6, C2.7",
           "The properties and changes of matter; pure substances (elements and compounds) and mixtures; physical and chemical properties and changes; "
           "the relationship between the structure of simple compounds and their chemical formulas; and the elements and compounds in household products.",
           "Elements and Compounds", "elements and compounds",
           "Free Grade 9 Science (SNC1W) worksheets on elements and compounds: pure substances and mixtures, physical and chemical properties, physical and chemical changes, chemical formulas and household chemicals. 100 questions with answers.",
           "A compound is two or more elements chemically joined in a fixed ratio.", "The formula tells you which atoms and how many: H₂O has 2 H and 1 O.",
           "<p>Matter is either a pure substance (an element or a compound) or a mixture. An element has only one kind of atom; a compound has two or more elements joined in a fixed ratio and can only be separated by a chemical change. "
           "Mixtures can be separated by physical means such as filtering or evaporating.</p>"
           "<p>Physical properties (colour, density, melting point) can be observed without changing the substance; chemical properties (flammability, reaction with acid) describe how it changes into new substances. "
           "Signs of a chemical change include a new colour, a gas, a precipitate, light or a temperature change that is hard to reverse.</p>",
           [("How many atoms are in one molecule of glucose, C₆H₁₂O₆?", ["6 + 12 + 6"], "24"),
            ("Is rusting iron a physical or a chemical change?", ["A new substance (iron oxide) forms."], "chemical change")],
           ["Calling melting ice a chemical change.", "Thinking a mixture of iron and sulfur is the compound iron sulfide.", "Reading the subscript as applying to the atom before and after it (in CO₂ the 2 is for O only)."],
           [("Why must household cleaners never be mixed?", "Some mixtures, such as bleach with ammonia or acid, react to give toxic gases."),
            ("What is the difference between an atom and a molecule?", "An atom is a single particle of an element; a molecule is two or more atoms joined together.")],
           lambda X: [
               ("Pure substances and mixtures", [(X.gen(G + "g7_atoms_and_molecules", "g_type"), 7), (X.gen(G + "g7_atoms_and_molecules", "g_model"), 5), (X.gen("gen_sg_science_s1_elements_compounds_and_mixtures", "g_susp"), 4), (X.gen("gen_sg_science_s1_atoms_and_molecules", "g_form"), 4)]),
               ("Physical and chemical properties", [(X.gen(G + "g7_properties_and_chemical_reactions", "g_kind"), 6), (X.gen(G + "g7_properties_and_chemical_reactions", "g_which"), 5), (X.gen(G + "g7_properties_and_chemical_reactions", "g_prop"), 5), (X.gen("gen_sg_science_s1_physical_properties_of_matter", "g_prop"), 4)]),
               ("Physical and chemical changes", [(X.gen("gen_sg_science_s2_chemical_changes", "g_ch"), 6), (X.gen("gen_sg_science_s2_chemical_changes", "g_cause"), 4), (X.gen(G + "g7_properties_and_chemical_reactions", "g_table"), 6), (X.gen("gen_uk_science_y8_chemical_reactions", "g_sign"), 4)]),
               ("Chemical formulas", [(X.gen(G + "g7_atoms_and_molecules", "g_count"), 7), (X.gen(G + "g7_atoms_and_molecules", "g_coef"), 5), (X.gen(G + "chem_chemical_bonding", "g_formula"), 4), (X.gen(G + "g7_conservation_of_atoms", "g_count"), 4)]),
               ("Compounds in everyday products", [(X.gen(G + "chem_chemical_bonding", "g_btype"), 6), (X.gen(G + "chem_chemical_bonding", "g_name"), 4), (X.gen("gen_sg_science_s2_acids_and_alkalis", "g_nat"), 5), (X.gen("gen_sg_science_s2_acids_and_alkalis", "g_lit"), 5)]),
           ]),
        HU("SNC1W", "D", 5, "static-and-current-electricity", "D2.1, D2.2, D2.3, D2.7",
           "How charges behave in static and current electricity and how this relates to atomic structure; conductors and insulators; "
           "the components of a DC circuit with their symbols, quantities and SI units; and the difference between electricity and electrical energy.",
           "Static and Current Electricity", "static and current electricity",
           "Free Grade 9 Science (SNC1W) worksheets on electricity: static charge, charging by friction and induction, conductors and insulators, circuit symbols, current, potential difference and electrical energy. 100 questions with answers.",
           "Only electrons move when objects are charged.", "Current I in amperes (A), potential difference V in volts (V), resistance R in ohms (Ω).",
           "<p>Objects become charged by gaining or losing electrons: rubbing a balloon on hair moves electrons onto the balloon, so the balloon becomes negative and the hair positive. "
           "Like charges repel; unlike charges attract; a charged object also attracts a neutral one by induction.</p>"
           "<p>In a conductor (metals) electrons move freely; in an insulator (plastic, rubber, glass) they do not. A circuit needs a source (cell or battery), a load (such as a lamp), conducting wires and a closed path. "
           "Current is measured with an ammeter in series; potential difference with a voltmeter in parallel. Electrical energy (in joules or kilowatt-hours) is what the current transfers to the load.</p>",
           [("A balloon rubbed on wool becomes negative. What happened?", ["Electrons moved from the wool to the balloon."], "the balloon gained electrons"),
            ("How do you connect a voltmeter?", ["It compares two points."], "in parallel across the component")],
           ["Saying protons move when objects become charged.", "Connecting an ammeter in parallel.", "Calling electricity and electrical energy the same thing."],
           [("Why do you get a shock after walking on carpet?", "Your body picks up extra electrons, which jump to a metal doorknob as a spark."),
            ("What is a kilowatt-hour?", "The energy used by a 1 kW device in one hour (3.6 million joules); it is how electricity bills measure energy.")],
           lambda X: [
               ("Static charge", [(X.gen("gen_sg_science_s4_static_electricity", "g_rub"), 6), (X.gen("gen_sg_science_s4_static_electricity", "g_ind"), 4), (X.gen("gen_sg_science_s4_static_electricity", "g_ci"), 4), (X.gen(G + "phys_electric_force_and_coulombs_law", "g_rub"), 3), (X.gen(G + "phys_electric_force_and_coulombs_law", "g_sign"), 3)]),
               ("Conductors, insulators and charge", [(X.gen(G + "g8_electric_and_magnetic_forces", "g_charge"), 6), (X.gen(G + "g8_electric_and_magnetic_forces", "g_mat"), 4), (X.gen("gen_uk_science_y8_electricity", "g_static"), 5), (X.gen("gen_sg_science_s4_static_electricity", "g_chain"), 5)]),
               ("Circuit components and symbols", [(X.gen("gen_sg_science_s2_electrical_systems", "g_sym"), 8), (X.gen("gen_sg_science_s2_electrical_systems", "g_unit"), 6), (X.gen("gen_uk_science_y10_electricity", "g_q"), 6)]),
               ("Current and potential difference", [(X.gen("gen_sg_science_s4_current_of_electricity", "g_q"), 6), (X.gen("gen_sg_science_s4_current_of_electricity", "g_w"), 6), (X.gen("gen_sg_science_s2_electrical_systems", "g_var"), 4), (X.gen("gen_uk_science_y8_electricity", "g_pd"), 4)]),
               ("Electricity and electrical energy", [(X.gen("gen_sg_science_s2_electrical_systems", "g_cost"), 6), (X.gen("gen_sg_science_s4_practical_electricity", "g_p"), 5), (X.gen("gen_sg_science_s4_practical_electricity", "g_cost"), 5), (X.gen("gen_uk_science_y8_energy_and_power", "g_kwh"), 4)]),
           ]),
        HU("SNC1W", "D", 6, "circuits-ohms-law-and-energy", "D1.1, D1.2, D2.4, D2.5, D2.6, D2.8",
           "The relationship between current, potential difference and resistance (Ohm's law); current, potential difference and resistance in series and parallel circuits; "
           "the efficiency of electrical devices and their energy transformations; and the benefits and challenges of different sources of electrical energy.",
           "Circuits, Ohm's Law and Energy", "circuits, Ohm's law and energy",
           "Free Grade 9 Science (SNC1W) worksheets on circuits: Ohm's law, series and parallel circuits, efficiency, energy transformations and sources of electrical energy. 100 questions with answers.",
           "Ohm's law: V = IR.", "Efficiency = useful energy out ÷ energy in × 100%.",
           "<p>For many conductors, V = IR: doubling the potential difference doubles the current. In a series circuit the current is the same everywhere, the voltages add up to the source voltage, "
           "and R<sub>T</sub> = R₁ + R₂. In a parallel circuit every branch has the full voltage, the branch currents add up, and adding a branch lowers the total resistance.</p>"
           "<p>Devices transform electrical energy into other forms, but some always becomes waste heat. Efficiency = useful output ÷ input × 100%. "
           "Ontario's electricity comes mostly from nuclear and hydroelectric stations, with wind, solar, natural gas and biofuel; each source has benefits and costs.</p>",
           [("A 9.0 V battery and a 30 Ω resistor. Current?", ["I = V ÷ R = 9.0 ÷ 30"], "0.30 A"),
            ("A lamp uses 60 J and gives 6 J of light. Efficiency?", ["6 ÷ 60 × 100%"], "10%")],
           ["Thinking current is used up along a series circuit.", "Adding parallel resistances to get the total resistance.", "Calling hydroelectric power energy-free: it still changes rivers and habitats."],
           [("Why does a bulb go out in a series string when one burns out?", "The circuit is broken, so no current can flow through any of the bulbs."),
            ("Which energy sources do not emit greenhouse gases while running?", "Hydro, nuclear, wind and solar.")],
           lambda X: [
               ("Ohm's law", [(X.gen("gen_sg_science_s4_current_of_electricity", "g_vir"), 10), (X.gen("gen_uk_science_y10_electricity", "g_iv"), 5), (X.gen("gen_uk_science_y8_electricity", "g_vir"), 5)]),
               ("Series circuits", [(X.gen("gen_sg_science_s4_dc_circuits", "g_div"), 6), (X.gen("gen_sg_science_s4_dc_circuits", "g_rules"), 4), (X.gen("gen_uk_science_y10_electricity", "g_rs"), 5), (X.gen("gen_uk_science_y8_electricity", "g_series"), 5)]),
               ("Parallel circuits", [(X.gen("gen_sg_science_s4_dc_circuits", "g_par"), 8), (X.gen("gen_sg_science_s4_dc_circuits", "g_mix"), 6), (X.gen("gen_uk_science_y8_electricity", "g_par"), 6)]),
               ("Efficiency and energy transformations", [(X.gen(G + "phys_energy_conversion_and_efficiency", "g_eff"), 6), (X.gen(G + "phys_energy_conversion_and_efficiency", "g_conv"), 6), (X.gen("gen_au_science_y9_conservation_of_energy_and_efficiency", "g_sankey"), 4), (X.gen("gen_uk_science_y8_energy_and_power", "g_eff"), 4)]),
               ("Sources of electrical energy", [(X.gen(G + "g7_natural_resources", "g_origin"), 5), (X.gen(G + "g7_natural_resources", "g_where"), 4), (X.gen("gen_sg_science_s2_energy_and_work_done", "g_src"), 5), (X.gen(G + "phys_energy_conversion_and_efficiency", "g_elec"), 6)]),
           ]),
        HU("SNC1W", "E", 7, "the-sun-and-the-solar-system", "E2.1, E2.2, E2.4, E2.6",
           "The characteristics of the Sun and its importance to the solar system and to life on Earth; how the Sun's energy drives natural phenomena and renewable energy; "
           "the major components of the solar system; and the causes of phenomena observed from Earth (day and night, seasons, phases of the Moon, eclipses).",
           "The Sun and the Solar System", "the Sun and the solar system",
           "Free Grade 9 Science (SNC1W) worksheets on the Sun and the solar system: the Sun's layers and energy, sunspots, the planets, seasons, phases of the Moon, eclipses and orbits. 100 questions with answers.",
           "The Sun makes energy by nuclear fusion of hydrogen into helium.", "Seasons are caused by Earth's tilt, not its distance from the Sun.",
           "<p>The Sun is a medium-sized star made mostly of hydrogen and helium. In its core, fusion turns hydrogen into helium and releases huge amounts of energy, which travels out as light and heat. "
           "Sunspots, solar flares and the solar wind can cause auroras and disturb satellites. The Sun's energy drives weather, the water cycle, photosynthesis, wind and solar power.</p>"
           "<p>The solar system has eight planets: four rocky inner planets and four gas and ice giants, plus dwarf planets, moons, asteroids and comets. "
           "Earth's tilt of 23.5° causes the seasons; the Moon's phases come from how much of its sunlit half we see; eclipses happen when the Sun, Earth and Moon line up.</p>",
           [("Why is it summer in Canada in July?", ["The Northern Hemisphere tilts towards the Sun."], "sunlight is more direct and days are longer"),
            ("Which phase of the Moon happens during a solar eclipse?", ["The Moon is between the Sun and Earth."], "new moon")],
           ["Saying the seasons come from Earth being closer to the Sun.", "Thinking the Moon makes its own light.", "Calling the Sun a planet or the biggest star."],
           [("What causes the northern lights?", "Charged particles from the Sun hit gases in the upper atmosphere near the poles and make them glow."),
            ("Why can't we have a solar eclipse every month?", "The Moon's orbit is tilted about 5°, so it usually passes above or below the line from the Sun to Earth.")],
           lambda X: [
               ("The Sun", [(X.gen(G + "ess_the_sun_and_nuclear_fusion", "g_layer"), 6), (X.gen(G + "ess_the_sun_and_nuclear_fusion", "g_spot"), 5), (X.gen(G + "ess_the_sun_and_nuclear_fusion", "g_emc"), 4), (X.gen(G + "ess_the_sun_and_nuclear_fusion", "g_life"), 5)]),
               ("The Sun's energy on Earth", [(X.gen("gen_uk_science_y9_gravity_and_space", "g_season"), 5), (X.gen(G + "g8_earth_moon_sun_system", "g_season"), 5), (X.gen(G + "g6_ocean_and_atmosphere_circulation", "g_sun"), 5), (X.gen("gen_uk_science_y7_space", "g_tilt"), 5)]),
               ("The planets", [(X.gen(G + "g8_scale_of_the_solar_system", "g_fact"), 6), (X.gen(G + "g8_scale_of_the_solar_system", "g_ratio"), 4), (X.gen(G + "g8_gravity_in_the_solar_system", "g_pl"), 6), (X.gen("gen_uk_science_y7_space", "g_size"), 4)]),
               ("Day, night, phases and eclipses", [(X.gen(G + "g8_earth_moon_sun_system", "g_name"), 6), (X.gen(G + "g8_earth_moon_sun_system", "g_next"), 5), (X.gen(G + "g8_earth_moon_sun_system", "g_order"), 4), (X.gen(G + "g8_earth_moon_sun_system", "g_ecl"), 5)]),
               ("Gravity and orbits", [(X.gen(G + "ess_keplers_laws_and_orbits", "g_k3"), 6), (X.gen(G + "ess_keplers_laws_and_orbits", "g_speed"), 4), (X.gen("gen_uk_science_y9_gravity_and_space", "g_weight"), 5), (X.gen("gen_uk_science_y9_gravity_and_space", "g_mw"), 5)]),
           ]),
        HU("SNC1W", "E", 8, "the-universe-and-space-exploration", "E1.1, E1.2, E1.3, E2.3, E2.5",
           "Evidence for theories of the origin and evolution of the universe and the solar system; stars and galaxies; distances in space in astronomical units and light-years; "
           "and the social, environmental and economic impacts of space exploration and the technologies that come from it, including Canadian contributions.",
           "The Universe and Space Exploration", "the universe and space exploration",
           "Free Grade 9 Science (SNC1W) worksheets on the universe and space exploration: light-years, the life cycle of stars, galaxies, the big bang, satellites, the Canadarm and space technology. 100 questions with answers.",
           "The universe began about 13.8 billion years ago and is still expanding.", "1 light-year ≈ 9.46 × 10¹² km; 1 AU = 150 million km.",
           "<p>Distances in space are huge. The astronomical unit (AU) is the average distance from Earth to the Sun (about 150 million km). A light-year is the distance light travels in a year (about 9.46 × 10¹² km). "
           "Stars form from clouds of gas and dust, shine by fusion, and end as white dwarfs, neutron stars or black holes depending on their mass.</p>"
           "<p>Evidence for the big bang includes the red shift of distant galaxies (the universe is expanding) and the cosmic microwave background. "
           "Space technology such as satellites, GPS, weather and climate monitoring and the Canadarm brings many benefits, but also costs, risks and space debris.</p>",
           [("Light from a star takes 4 years to reach us. How far away is it?", ["Distance = 4 light-years"], "about 3.8 × 10¹³ km"),
            ("A galaxy's light is shifted towards red. What does this tell us?", ["The wavelength is stretched."], "it is moving away from us")],
           ["Thinking a light-year is a unit of time.", "Saying all stars end as black holes.", "Thinking satellites stay up because there is no gravity in space."],
           [("Why do we see distant galaxies as they were long ago?", "Their light took millions or billions of years to reach us."),
            ("What are some Canadian contributions to space exploration?", "The Canadarm robotic arms, RADARSAT Earth-observation satellites, and Canadian astronauts on the space station and on the Artemis II crew.")],
           lambda X: [
               ("Distances in space", [(X.gen("gen_uk_science_y9_gravity_and_space", "g_ly"), 6), (X.gen("gen_uk_science_y7_space", "g_ly"), 5), (X.gen(G + "g8_scale_of_the_solar_system", "g_dist"), 5), (X.gen(G + "g8_scale_of_the_solar_system", "g_model"), 4)]),
               ("Stars", [(X.gen(G + "ess_stars_and_the_origin_of_elements", "g_stage"), 6), (X.gen(G + "ess_stars_and_the_origin_of_elements", "g_spec"), 5), (X.gen(G + "ess_stars_and_the_origin_of_elements", "g_color"), 5), (X.gen(G + "ess_stars_and_the_origin_of_elements", "g_where"), 4)]),
               ("Galaxies and the big bang", [(X.gen(G + "ess_the_big_bang", "g_hubble"), 6), (X.gen(G + "ess_the_big_bang", "g_shift"), 5), (X.gen(G + "ess_the_big_bang", "g_ev"), 5), (X.gen(G + "ess_the_big_bang", "g_data"), 4)]),
               ("The origin of the solar system and elements", [(X.gen(G + "ess_stars_and_the_origin_of_elements", "g_fuse"), 6), (X.gen(G + "ess_earths_early_history", "g_age"), 5), (X.gen(G + "ess_earths_early_history", "g_order"), 5), (X.gen(G + "ess_earths_early_history", "g_ev"), 4)]),
               ("Space exploration and technology", [(X.pool(SPACE), 20)]),
           ]),
    ]
