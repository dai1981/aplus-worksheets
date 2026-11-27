# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 6 (B Biodiversity, C Electrical Phenomena, D Flight, E Space). Built by caon_sci.build."""
from caon_sci import CU, tq

UK6C, UK6K, UK4G = "gen_uk_science_y6_classifying_living_things", "gen_uk_science_y6_classification_keys", "gen_uk_science_y4_grouping_living_things"
SG3C, US7B, AU7C = "gen_sg_science_p3_classifying_living_things", "gen_us_science_g7_protecting_biodiversity", "gen_au_science_y7_classification_and_dichotomous_keys"
UK4CH, US3E = "gen_uk_science_y4_changing_environments", "gen_us_science_g3_environmental_change"
US3M, US8E = "gen_us_science_g3_magnets_and_static_electricity", "gen_us_science_g8_electric_and_magnetic_forces"
UK6W, UK6Y, UK4A = "gen_uk_science_y6_circuits_and_switches", "gen_uk_science_y6_circuit_symbols", "gen_uk_science_y4_electrical_appliances_and_circuits"
UK4I, SG5E, SG5C = "gen_uk_science_y4_conductors_and_insulators", "gen_sg_science_p5_electrical_circuits", "gen_sg_science_p5_conductors_and_circuit_diagrams"
US4E, UK8L, SG2E, AU6E = "gen_us_science_g4_electric_circuits", "gen_uk_science_y8_electricity", "gen_sg_science_s2_electrical_systems", "gen_au_science_y6_electric_circuits"
US4R, US5R = "gen_us_science_g4_energy_resources", "gen_us_science_g5_protecting_earths_resources"
UK5A = "gen_uk_science_y5_air_and_water_resistance"
UK5S, UK5D, UK7S = "gen_uk_science_y5_the_solar_system", "gen_uk_science_y5_day_night_and_the_moon", "gen_uk_science_y7_space"
US5S, US5N, US8M = "gen_us_science_g5_sun_and_stars", "gen_us_science_g5_patterns_in_the_night_sky", "gen_us_science_g8_earth_moon_sun_system"
US8S, US8G, UK9G, US5G = "gen_us_science_g8_scale_of_the_solar_system", "gen_us_science_g8_gravity_in_the_solar_system", "gen_uk_science_y9_gravity_and_space", "gen_us_science_g5_gravity"
AU6S = "gen_au_science_y6_the_solar_system"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def L(lead, *xs):
    return "<p><b>%s</b></p><ul>%s</ul>" % (lead, ul(*xs))


def s_class(X):
    pool = X.pool([
        ("What is biodiversity?", "the variety of living things in an area", ["the number of rocks in an area", "the weather in an area", "one kind of animal"], "More kinds of living things means more biodiversity."),
        ("Why do scientists classify living things?", "to group them by shared features so they are easier to study", ["to give them colours", "to count rocks", "to make them grow"], "Classification shows how living things are related."),
        ("Which group has a backbone?", "vertebrates", ["invertebrates", "fungi", "bacteria"], "Fish, amphibians, reptiles, birds and mammals have backbones."),
        ("Which animal is an invertebrate?", "an earthworm", ["a frog", "a robin", "a trout"], "Invertebrates have no backbone."),
        ("A painted turtle has dry scaly skin and lays eggs on land. Which vertebrate group is it in?", "reptiles", ["amphibians", "mammals", "fish"], "Reptiles have dry scales."),
        ("A spring peeper lives in water as a tadpole and on land as an adult. Which group is it in?", "amphibians", ["reptiles", "fish", "birds"], "Amphibians change from water to land."),
        ("Which feature do all mammals share?", "They have hair or fur and feed their young milk.", ["They all lay eggs.", "They all have scales.", "They all have feathers."], "Beavers and bats are mammals."),
        ("Which feature do all insects share?", "six legs and three body parts", ["eight legs", "a backbone", "feathers"], "Spiders have eight legs, so they are not insects."),
        ("Mushrooms do not make their own food and grow from spores. Which kingdom are they in?", "fungi", ["plants", "animals", "bacteria"], "Fungi absorb food from what they grow on."),
        ("Which kingdom makes its own food using sunlight?", "plants", ["animals", "fungi", "none"], "Plants are producers."),
        ("What is a species?", "a group of living things that can breed and have young that can also breed", ["any animal in a forest", "a habitat", "a kind of rock"], "Moose are one species."),
        ("A dichotomous key gives two choices at each step. What do you do?", "pick the choice that matches the living thing and follow it", ["pick both choices", "skip to the last step", "guess the name"], "Each step splits the group in two."),
        ("Which tree is a conifer?", "an eastern white pine", ["a sugar maple", "a red oak", "a white birch"], "Conifers have cones and needles."),
        ("Which is a vertebrate that lives in Ontario lakes?", "a lake trout", ["a crayfish", "a dragonfly larva", "a snail"], "Fish have backbones."),
        ("Which group are spiders in?", "arachnids (invertebrates with eight legs)", ["insects", "reptiles", "mammals"], "Spiders have two body parts and eight legs."),
    ])
    return [
        ("Biodiversity and groups", [(pool, 6), (X.gen(UK6C, "g_group", n=7), 7), (X.gen(SG3C, "g_king"), 4), (X.gen(UK6C, "g_char"), 3)]),
        ("Vertebrates", [(X.gen(UK6C, "g_vert", n=7), 7), (X.gen(UK6C, "g_which", n=6), 6), (pool, 4), (X.gen(AU7C, "g_mam"), 3)]),
        ("Invertebrates, plants and fungi", [(X.gen(SG3C, "g_group", n=6), 6), (X.gen(UK6C, "g_plant"), 5), (X.gen(SG3C, "g_feat"), 5), (X.gen(UK4G, "g_legs"), 4)]),
        ("Classification keys", [(X.gen(UK6K, "g_follow", n=6), 6), (X.gen(UK6K, "g_pair", n=5), 5), (X.gen(UK6K, "g_split", n=5), 5), (X.gen(UK6K, "g_count", n=4), 4)]),
        ("Sorting living things", [(X.gen(UK6C, "g_odd", n=4), 4), (X.gen(UK4G, "g_carroll"), 4), (X.B(UK6C, "B5"), 4), (X.B(UK6K, "B5"), 4), (X.gen(SG3C, "g_odd", n=4), 4)]),
    ]


def s_protect(X):
    pool = X.pool([
        ("Why is high biodiversity good for an ecosystem?", "It makes the ecosystem better able to survive changes and disease.", ["It makes the ecosystem smaller.", "It means fewer food chains.", "It has no effect."], "Many species give many backups."),
        ("What does 'endangered' mean?", "at risk of disappearing from the wild", ["very common", "already extinct", "moving to a new country"], "The woodland caribou is a species at risk in Ontario."),
        ("What does 'extinct' mean?", "no members of the species are left alive", ["the species is rare", "the species is hibernating", "the species moved away"], "The passenger pigeon is extinct."),
        ("Which is a major cause of biodiversity loss?", "habitat loss from clearing land", ["planting native trees", "protecting wetlands", "making new parks"], "Living things lose their homes."),
        ("Which is an invasive species in Ontario?", "the emerald ash borer", ["the sugar maple", "the common loon", "the white-tailed deer"], "It has killed millions of ash trees."),
        ("How do invasive species harm biodiversity?", "They compete with or eat native species and have few predators.", ["They always help native species.", "They make habitats bigger.", "They only live in zoos."], "Purple loosestrife crowds out wetland plants."),
        ("Which action helps protect biodiversity?", "planting native plants and protecting habitats", ["releasing pet goldfish into a lake", "draining a wetland", "using more pesticides"], "Native plants support native animals."),
        ("Why are bees important for biodiversity?", "They pollinate many plants, including food crops.", ["They eat other insects only.", "They make soil.", "They stop rain."], "Without pollinators, many plants cannot make seeds."),
        ("What is an ecosystem service?", "a benefit people get from nature, like clean water or pollination", ["a bus service in a park", "a kind of habitat", "a type of fungus"], "Wetlands clean and store water."),
        ("How do Indigenous knowledge and practices help protect biodiversity?", "They teach respect for all living things and taking only what is needed.", ["They encourage taking everything at once.", "They ignore the land.", "They remove all predators."], "Many conservation projects work with Indigenous communities."),
        ("Algonquin Park protects forests and lakes. How does a park help biodiversity?", "It keeps habitats safe from development.", ["It brings in invasive species.", "It removes all the animals.", "It makes the area a city."], "Protected areas save species."),
        ("Which is a benefit of biodiversity to people?", "foods, medicines and materials come from many species", ["it makes the weather colder", "it removes all insects", "it has no benefit"], "Many medicines come from plants."),
        ("Why should you not release a pet turtle or fish into a pond?", "It could become invasive or spread disease.", ["It will always die right away.", "It makes the pond deeper.", "It is good for the pond."], "Non-native pets can harm local species."),
        ("Monarch butterflies need milkweed to lay eggs. How can people help them?", "plant milkweed in gardens and fields", ["cut down all milkweed", "spray insecticide on flowers", "keep monarchs as pets"], "Milkweed is the only food for monarch caterpillars."),
    ])
    return [
        ("Why biodiversity matters", [(pool, 6), (X.gen(US7B, "g_serv"), 6), (X.B(US7B, "B1"), 5), (X.gen(US7B, "g_matrix", n=3), 3)]),
        ("Threats to biodiversity", [(pool, 6), (X.gen(UK4CH, "g_cause"), 6), (X.gen(UK4CH, "g_eff"), 6), (X.gen(US3E, "g_problem"), 2)]),
        ("Protecting species", [(X.gen(US7B, "g_sol"), 6), (pool, 4), (X.gen(US3E, "g_solution"), 5), (X.gen(UK4CH, "g_good"), 5)]),
        ("People and biodiversity", [(pool, 6), (X.gen(US3E, "g_resp"), 6), (X.gen(US7B, "g_matrix", n=4), 4), (X.B(UK4CH, "B1"), 4)]),
        ("Biodiversity investigations", [(X.gen(UK4CH, "g_survey", n=5), 5), (X.gen(US3E, "g_data", n=5), 5), (X.B(US7B, "B5"), 4), (X.B(UK4CH, "B5"), 3), (X.gen(US3E, "g_merit", n=3), 3)]),
    ]


def s_static(X):
    pool = X.pool([
        ("What are the two kinds of electric charge?", "positive and negative", ["hot and cold", "north and south", "big and small"], "Like charges repel; unlike charges attract."),
        ("Two negatively charged balloons are held close. What happens?", "They push apart (repel).", ["They pull together.", "Nothing happens.", "They become magnets."], "Like charges repel."),
        ("A charged balloon sticks to a wall. Why?", "The charged balloon attracts opposite charges in the wall.", ["The wall is sticky.", "Gravity holds it.", "The balloon is a magnet."], "Unlike charges attract."),
        ("What moves when an object becomes charged by rubbing?", "electrons", ["protons", "the whole atom", "air"], "Electrons are rubbed off one object onto another."),
        ("What is static electricity?", "a build-up of electric charge on the surface of an object", ["electricity flowing in a wire", "a kind of magnet", "light from the Sun"], "Static charge stays in one place until it jumps."),
        ("Why do you sometimes get a shock touching a doorknob in winter?", "Charge built up on your body jumps to the metal doorknob.", ["The doorknob is a battery.", "Cold air makes electricity.", "The door is magnetic."], "Dry winter air lets charge build up."),
        ("What is lightning?", "a giant spark of static electricity between clouds or a cloud and the ground", ["sunlight in a storm", "a magnet in the sky", "rain falling fast"], "Charge builds up in storm clouds."),
        ("Why should you not stand under a tall tree in a thunderstorm?", "Lightning often strikes tall objects.", ["Trees attract rain.", "Trees make thunder.", "Trees are always safe."], "Go indoors during a thunderstorm."),
        ("What does a lightning rod do?", "It carries lightning safely into the ground.", ["It makes lightning.", "It stops rain.", "It stores electricity for later."], "It protects buildings."),
        ("What is the difference between static and current electricity?", "Static charge stays in one place; current electricity flows through a circuit.", ["They are the same.", "Static electricity flows in wires.", "Current electricity only happens in storms."], "Current needs a closed path."),
        ("Which pair of materials can become charged when rubbed together?", "a balloon and wool", ["two pieces of the same metal", "water and water", "a rock and air"], "Rubbing moves electrons."),
        ("What is an electromagnet?", "a coil of wire that becomes a magnet when current flows through it", ["a magnet made of plastic", "a charged balloon", "a battery"], "Turning off the current turns off the magnet."),
        ("How can you make an electromagnet stronger?", "add more coils of wire or use more current", ["use fewer coils", "use a plastic core", "turn off the battery"], "More coils and more current give a stronger field."),
        ("Why are electromagnets used in scrapyard cranes?", "They can be switched on to lift steel and off to drop it.", ["They work only on wood.", "They never turn off.", "They are made of rubber."], "Electromagnets can be controlled."),
        ("What happens when you rub a plastic comb through dry hair?", "The comb becomes charged and can pick up small bits of paper.", ["The comb becomes a magnet.", "The comb gets heavier.", "Nothing happens."], "Charged objects attract light objects."),
        ("A charged object is brought near small bits of paper. What happens?", "The bits of paper are pulled toward it.", ["The paper bursts into flame.", "The paper is pushed into the ground.", "The paper changes colour."], "Charged objects attract neutral ones."),
        ("What does it mean if an object is neutral?", "It has equal positive and negative charges.", ["It has only positive charges.", "It has no atoms.", "It is a magnet."], "Most objects are neutral until rubbed."),
        ("Why do photocopiers and laser printers use static electricity?", "Charged areas attract toner powder to make the image.", ["To keep the paper cold", "To make the paper heavier", "To make sound"], "Static has many uses."),
        ("Why should you touch a metal surface before handling computer parts?", "to let built-up static charge flow away so it does not damage the parts", ["to make the parts warmer", "to clean your hands", "to charge the parts"], "A static spark can damage electronics."),
        ("Thunder is heard after lightning is seen. Why?", "Light travels much faster than sound.", ["Thunder happens first.", "Sound travels faster than light.", "Lightning makes no light."], "Count the seconds to estimate distance."),
        ("Which is the safest place during a thunderstorm?", "inside a building or a hard-topped car", ["under a tall tree", "in a lake", "on top of a hill"], "Buildings and cars protect you."),
        ("How do dryer sheets reduce static cling in laundry?", "They stop charge from building up on the clothes.", ["They make clothes magnetic.", "They add more charge.", "They make clothes wet."], "Static cling happens when charged clothes attract."),
    ])
    return [
        ("Electric charges", [(pool, 6), (X.gen(US8E, "g_charge"), 8), (X.gen(US3M, "g_static"), 6)]),
        ("Attract and repel", [(X.gen(US8E, "g_charge", n=4), 4), (X.gen(US3M, "g_attract", n=6), 6), (X.gen(US3M, "g_poles"), 4), (X.gen(US8E, "g_poles", n=4), 4), (pool, 2)]),
        ("Static in daily life", [(pool, 8), (X.gen(UK8L, "g_static"), 6), (X.B(US3M, "B1"), 4), (X.gen(US3M, "g_dist", n=2), 2)]),
        ("Electricity and magnetism", [(X.gen(US8E, "g_field"), 5), (X.gen(US8E, "g_coil"), 4), (X.gen(US3M, "g_metal"), 4), (X.B(US8E, "B1"), 5), (pool, 2)]),
        ("Charge investigations", [(X.B(US3M, "B5"), 4), (X.B(US8E, "B5"), 4), (X.gen(US3M, "g_dist", n=4), 4), (X.gen(US3M, "g_attract", n=4), 4), (pool, 4)]),
    ]


def s_circuit(X):
    pool = X.pool([
        ("What does an electric circuit need to work?", "a source of energy, conductors and a complete (closed) path", ["only a bulb", "only a switch", "an open gap"], "Current flows only in a closed loop."),
        ("What does a switch do?", "It opens or closes the circuit.", ["It makes electricity.", "It stores light.", "It changes the colour of the bulb."], "An open switch makes a gap."),
        ("What is a series circuit?", "a circuit with only one path for the current", ["a circuit with many paths", "a circuit with no battery", "a broken circuit"], "If one bulb goes out, they all go out."),
        ("What is a parallel circuit?", "a circuit with more than one path for the current", ["a circuit with one path", "a circuit with no wires", "a circuit that never works"], "Homes are wired in parallel."),
        ("Why are houses wired in parallel?", "Each device can be switched on and off by itself.", ["It uses no electricity.", "All lights must turn off together.", "It needs no wires."], "Parallel paths work independently."),
        ("Which material is a good conductor?", "copper", ["rubber", "plastic", "wood"], "Metals conduct electricity."),
        ("Why are wires covered in plastic?", "Plastic is an insulator that keeps the current in the wire and protects people.", ["Plastic conducts better.", "Plastic makes the wire stronger only.", "Plastic stores electricity."], "Insulators stop shocks."),
        ("A bulb in a series circuit burns out. What happens to the other bulbs?", "They go out too.", ["They get brighter.", "Nothing changes.", "They change colour."], "The only path is broken."),
        ("A bulb in a parallel circuit burns out. What happens to the other bulbs?", "They stay lit.", ["They all go out.", "They explode.", "They flicker forever."], "The other paths are still complete."),
        ("What is a short circuit?", "a path that lets current bypass the load, which can cause overheating", ["a very short wire that is safe", "a circuit with a switch", "a circuit with one bulb"], "Short circuits can start fires."),
        ("What does a fuse or circuit breaker do?", "It breaks the circuit if too much current flows.", ["It makes more electricity.", "It makes bulbs brighter.", "It stores energy."], "It protects homes from fires."),
        ("Which is a safe habit with electricity?", "keep electrical devices away from water", ["pull plugs out by the cord", "poke objects into outlets", "fly a kite near power lines"], "Water conducts electricity."),
        ("How is electricity mostly made in Ontario?", "nuclear power plants and hydroelectric dams", ["batteries in every house", "rubbing balloons", "coal plants only"], "Ontario no longer uses coal."),
        ("What does a generator do?", "It changes motion energy into electrical energy.", ["It changes electricity into motion.", "It stores water.", "It makes light from heat."], "Turbines turn generators."),
        ("Which device changes electrical energy into motion?", "an electric motor", ["a solar panel", "a battery", "a generator"], "Fans and drills have motors."),
        ("How can you reduce electricity use at home?", "unplug chargers and turn off devices not in use", ["leave lights on all night", "keep the fridge door open", "use the dryer for one sock"], "Phantom power wastes energy."),
        ("Electricity is cheaper at night in Ontario. Why might families run the dishwasher at night?", "to save money and ease the demand on the grid", ["because it washes better in the dark", "because it uses no energy at night", "because the water is colder"], "Time-of-use pricing."),
        ("What is the unit used on an electricity bill?", "kilowatt-hours (kWh)", ["kilograms", "kilometres", "litres"], "kWh measures energy used."),
    ])
    return [
        ("Parts of a circuit", [(pool, 5), (X.gen(UK4A, "g_part"), 5), (X.gen(UK6Y, "g_sym"), 5), (X.gen(UK6Y, "g_desc"), 5)]),
        ("Conductors and insulators", [(X.gen(UK4I, "g_mat"), 6), (X.gen(US4E, "g_cond", n=5), 5), (X.gen(SG5C, "g_pick"), 5), (X.gen(UK4I, "g_why"), 2), (pool, 2)]),
        ("Will it light?", [(X.gen(US4E, "g_light", n=6), 6), (X.gen(UK6W, "g_cond", n=5), 5), (X.gen(US4E, "g_fix", n=5), 5), (X.gen(UK6W, "g_fault"), 4)]),
        ("Series and parallel circuits", [(X.gen(UK8L, "g_series"), 5), (X.gen(UK8L, "g_par"), 5), (X.gen(SG5E, "g_cmp"), 5), (pool, 5)]),
        ("Using electricity safely and wisely", [(pool, 6), (X.gen(SG5E, "g_save"), 5), (X.gen(SG2E, "g_haz"), 3), (X.gen(SG2E, "g_cost", n=3), 3), (X.gen(UK4A, "g_uses", n=3), 3)]),
    ]


FLIGHT_F = [
    ("pulls the plane down toward Earth", "weight (gravity)"), ("pushes the plane up, made by air moving over the wings", "lift"),
    ("pushes the plane forward, made by the engines or propeller", "thrust"), ("pushes back against the plane as it moves through the air", "drag"),
    ("acts against weight", "lift"), ("acts against thrust", "drag"), ("acts against lift", "weight (gravity)"), ("acts against drag", "thrust"),
    ("comes from the engines of a jet", "thrust"), ("increases when a plane flies faster through the air", "drag"),
    ("is made when a wing is tilted up slightly into the air (angle of attack)", "lift"), ("grows when more passengers and bags are loaded", "weight (gravity)"),
]


def flight_force(R):
    def f():
        d, k = R.choice(FLIGHT_F)
        others = [x for x in ("weight (gravity)", "lift", "thrust", "drag") if x != k and x.split()[0] not in d]
        if len(others) < 3:
            others.append("magnetism")
        return tq("Which of the four forces of flight %s?" % d, k, others, "That force is %s." % k)
    return f


def flight_net(R):
    def f():
        a, b = R.sample(range(2, 30), 2)
        pair = R.choice([("lift", "weight", "climbs", "descends"), ("thrust", "drag", "speeds up", "slows down")])
        q = "An airplane has %s = %d kN and %s = %d kN. What happens?" % (pair[0], a * 10, pair[1], b * 10)
        ans = pair[2] if a > b else pair[3]
        w = [pair[3] if a > b else pair[2], "it stays exactly the same", "it stops in the air"]
        return tq(q, "It %s." % ans, ["It %s." % x if not x.startswith("it") else x[0].upper() + x[1:] + "." for x in w],
                  "The bigger force wins: %d kN is more than %d kN, so the airplane %s." % (max(a, b) * 10, min(a, b) * 10, ans))
    return f


def s_flight(X):
    pool = X.pool([
        ("What are the four forces that act on an airplane in flight?", "lift, weight, thrust and drag", ["push, pull, twist and bend", "gravity, magnetism, friction and heat", "tension, compression, shear and torsion"], "Pilots balance these forces."),
        ("For an airplane to take off, which must be true?", "lift must be greater than weight", ["weight must be greater than lift", "drag must be greater than thrust", "thrust must be zero"], "More lift than weight makes the plane rise."),
        ("For an airplane to speed up, which must be true?", "thrust must be greater than drag", ["drag must be greater than thrust", "lift must equal zero", "weight must be greater than lift"], "Unbalanced forces change speed."),
        ("An airplane is flying level at a steady speed. What is true about the forces?", "They are balanced.", ["Lift is zero.", "Thrust is zero.", "Weight is greater than lift."], "Balanced forces mean no change in motion."),
        ("What is Bernoulli's principle about?", "faster-moving air has lower pressure", ["air never moves", "heavy things fall faster", "light travels in straight lines"], "Wings make air move faster over the top."),
        ("Why is the top of a wing curved?", "Air moves faster over the top, making lower pressure above the wing, which gives lift.", ["to make the plane heavier", "to collect rain", "to increase drag only"], "This wing shape is an airfoil."),
        ("What is an airfoil?", "the special curved shape of a wing", ["the engine", "the tail wheel", "the cockpit window"], "Airfoils create lift."),
        ("Why are airplanes streamlined?", "to reduce drag", ["to increase weight", "to increase drag", "to look nice only"], "Smooth shapes let air flow past easily."),
        ("What do the flaps on a wing do during landing?", "increase lift and drag so the plane can fly slowly", ["make the plane go faster", "turn the engine off", "steer the plane left only"], "Flaps change the wing shape."),
        ("What does the rudder on the tail control?", "turning the nose left or right (yaw)", ["the engine power", "the landing gear", "the cabin heat"], "The rudder moves side to side."),
        ("What do the elevators on the tail control?", "the nose moving up or down (pitch)", ["the speed of the engine", "turning on lights", "the fuel"], "Elevators tilt the plane up or down."),
        ("What do the ailerons on the wings control?", "rolling the plane to bank left or right", ["the brakes", "the engine", "the wheels"], "Ailerons move in opposite directions."),
        ("How does a helicopter make lift?", "Its spinning rotor blades are shaped like wings.", ["It floats like a balloon.", "It uses magnets.", "It has no lift."], "Rotor blades are airfoils."),
        ("Why does a hot-air balloon rise?", "Hot air inside is less dense than the cooler air outside.", ["The basket is very light.", "The burner pushes it up like a rocket.", "Wind lifts it."], "Less dense air rises."),
        ("Which force must a parachute increase to slow a skydiver?", "drag (air resistance)", ["thrust", "lift from an engine", "weight"], "A large canopy catches lots of air."),
        ("Why do jet engines push air backward?", "Pushing air back pushes the plane forward (action and reaction).", ["To cool the passengers", "To make lift directly", "To reduce weight"], "Every action has an equal and opposite reaction."),
        ("Why is the air harder to fly in high up in the mountains?", "The air is thinner, so wings make less lift.", ["There is more gravity.", "The air is thicker.", "There is no drag."], "Fewer air particles push on the wing."),
        ("Paper airplane A has wide wings. Paper airplane B has narrow wings. Both have the same mass. Which likely glides further?", "A, because wide wings make more lift", ["B, because narrow wings make more lift", "they always glide the same", "neither can glide"], "Wing area affects lift."),
        ("What is a fair test for paper airplane designs?", "throw each one with the same force from the same height and measure the distance", ["throw each one differently", "use different paper for each and guess", "test only one design"], "Change one variable at a time."),
    ])
    return [
        ("The four forces of flight", [(X.f(flight_force), 10), (pool, 10)]),
        ("Lift and wing shape", [(pool, 12), (X.f(flight_force), 4), (X.gen(UK5A, "g_shape"), 4)]),
        ("Balanced and unbalanced forces in flight", [(X.f(flight_net), 10), (pool, 6), (X.f(flight_force), 4)]),
        ("Drag and streamlining", [(X.gen(UK5A, "g_stream"), 6), (X.gen(UK5A, "g_chute", n=5), 5), (X.gen(UK5A, "g_dir"), 4), (pool, 5)]),
        ("Flight investigations", [(pool, 8), (X.B(UK5A, "B5"), 4), (X.B(UK5A, "B1"), 4), (X.f(flight_net), 4)]),
    ]


def s_flight2(X):
    pool = X.pool([
        ("How do birds make thrust?", "by flapping their wings down and back", ["by pushing off the ground", "with tiny engines", "by holding their breath"], "Flapping pushes air backward."),
        ("Why are bird bones light?", "They are hollow, which keeps the bird's weight low.", ["They are made of feathers.", "They are full of water.", "They have no calcium."], "Low weight helps flight."),
        ("How do Canada geese save energy on long flights?", "They fly in a V formation so each bird gets lift from the bird ahead.", ["They fly alone.", "They fly upside down.", "They never flap."], "The V shape reduces drag."),
        ("How does a maple key (samara) travel far from its tree?", "It spins like a helicopter blade, slowing its fall so wind carries it.", ["It swims.", "It explodes.", "It rolls downhill."], "Spinning creates lift."),
        ("How do dandelion seeds fly?", "Their fluffy parachutes catch the wind and fall slowly.", ["They have wings that flap.", "They are pushed by insects.", "They float on water only."], "High drag slows the fall."),
        ("How do flying squirrels move between trees?", "They glide using skin flaps between their legs.", ["They flap wings.", "They jump with springs.", "They float on balloons."], "Flaps act like wings."),
        ("Which is a way that people copied flight from nature?", "airplane wings shaped like bird wings", ["car tires shaped like fish", "boats shaped like clouds", "rockets shaped like trees"], "This is called biomimicry."),
        ("Why are bush planes important in northern Ontario?", "They reach remote communities without roads and can land on lakes with floats or skis.", ["They are only for racing.", "They carry no people.", "They fly only in cities."], "Many northern communities rely on air travel."),
        ("How do drones help farmers?", "They photograph crops from above to spot problems.", ["They plant trees by digging.", "They milk cows.", "They make rain."], "Drones collect data quickly."),
        ("What is one environmental effect of air travel?", "Jet fuel releases carbon dioxide into the atmosphere.", ["Planes clean the air.", "Planes stop climate change.", "Planes make no noise."], "Choosing other ways to travel can reduce emissions."),
        ("Why are airports often far from homes?", "Airplanes are loud, and noise affects people nearby.", ["Planes need snow to land.", "Airports must be in forests.", "Planes cannot fly over houses."], "Noise is a social impact."),
        ("What is one way airplanes are designed to be safer?", "They have backup systems and are tested in wind tunnels.", ["They have no seat belts.", "They fly without pilots always.", "They do not check the weather."], "Engineers test many times."),
        ("What does a wind tunnel help engineers test?", "how air flows around a model plane", ["how fast water boils", "how loud music is", "how plants grow"], "They measure lift and drag."),
        ("Why do airplanes de-ice their wings in an Ontario winter?", "Ice changes the wing shape and reduces lift.", ["Ice makes the plane lighter.", "Ice adds thrust.", "Ice makes the plane quieter."], "A clean wing makes proper lift."),
        ("Which flying device uses no engine?", "a glider", ["a jet airliner", "a helicopter", "a drone with propellers"], "Gliders use lift from air currents."),
        ("A kite flies on a windy day. What gives it lift?", "wind pushing against the tilted kite", ["the string pushing it up", "an engine", "gravity"], "The kite is angled into the wind."),
        ("What is the job of a propeller?", "to push air back and give thrust", ["to make lift directly", "to steer only", "to cool the engine only"], "Propeller blades are spinning airfoils."),
        ("Who was the first Canadian woman to fly in space?", "Roberta Bondar", ["Chris Hadfield", "Marc Garneau", "Julie Payette"], "Roberta Bondar flew on the space shuttle in 1992."),
        ("What is a career that uses knowledge of flight?", "aerospace engineer", ["baker", "librarian", "hairdresser"], "Engineers design aircraft."),
        ("Which animal is not able to fly?", "a penguin", ["a bat", "a bald eagle", "a monarch butterfly"], "Penguins have flippers for swimming."),
    ])
    return [
        ("Flight in nature", [(pool, 10), (X.f(flight_force), 4), (X.gen(UK5A, "g_shape", n=3), 3), (X.gen(UK5A, "g_chute", n=3), 3)]),
        ("Seeds, gliders and parachutes", [(pool, 8), (X.gen(UK5A, "g_chute", n=6), 6), (X.gen(UK5A, "g_dir", n=3), 3), (X.f(flight_net), 3)]),
        ("Flying machines", [(pool, 10), (X.f(flight_force), 6), (X.f(flight_net), 4)]),
        ("Flight and society", [(pool, 12), (X.gen(UK5A, "g_stream", n=4), 4), (X.f(flight_net), 4)]),
        ("Designing for flight", [(pool, 6), (X.B(UK5A, "B5"), 4), (X.f(flight_force), 5), (X.f(flight_net), 5)]),
    ]


def s_solar(X):
    pool = X.pool([
        ("What is at the centre of our solar system?", "the Sun", ["Earth", "the Moon", "Jupiter"], "All the planets orbit the Sun."),
        ("Which planet is closest to the Sun?", "Mercury", ["Venus", "Earth", "Mars"], "Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune."),
        ("Which is the largest planet?", "Jupiter", ["Saturn", "Earth", "Neptune"], "Jupiter is a gas giant."),
        ("Which planets are rocky (terrestrial)?", "Mercury, Venus, Earth and Mars", ["Jupiter and Saturn", "Uranus and Neptune", "all eight"], "The four inner planets are rocky."),
        ("What is a star?", "a huge ball of hot, glowing gas that makes its own light", ["a planet that reflects light", "a rock in space", "a moon"], "The Sun is a star."),
        ("Why does the Sun look bigger and brighter than other stars?", "It is much closer to Earth.", ["It is the biggest star in the universe.", "It is a planet.", "Other stars make no light."], "Distance changes how bright a star looks."),
        ("What is a constellation?", "a pattern of stars in the night sky", ["a group of planets", "a kind of comet", "a moon of Jupiter"], "The Big Dipper is part of Ursa Major."),
        ("What is a comet?", "a ball of ice and dust that grows a tail near the Sun", ["a small star", "a planet with rings", "a piece of the Moon"], "The Sun's heat makes the tail."),
        ("Where is the asteroid belt?", "between Mars and Jupiter", ["between Earth and Venus", "beyond Neptune only", "around the Moon"], "It holds millions of rocky objects."),
        ("What is a dwarf planet?", "a round object that orbits the Sun but has not cleared its path, like Pluto", ["a planet smaller than Earth", "a moon", "a star"], "Pluto became a dwarf planet in 2006."),
        ("What keeps the planets in orbit around the Sun?", "the Sun's gravity", ["magnetism", "wind", "light"], "Gravity pulls the planets toward the Sun."),
        ("What is a light year?", "the distance light travels in one year", ["the time it takes Earth to orbit the Sun", "a very bright year", "the age of a star"], "It is about 9.5 trillion km."),
        ("What is a galaxy?", "a huge group of billions of stars, gas and dust", ["a group of planets", "one star with planets", "a big comet"], "We live in the Milky Way."),
        ("Which planet has the most famous rings?", "Saturn", ["Mars", "Mercury", "Venus"], "Its rings are made of ice and rock."),
    ])
    return [
        ("The Sun and the planets", [(pool, 6), (X.gen(UK5S, "g_order"), 6), (X.gen(UK5S, "g_type"), 4), (X.gen(UK5S, "g_fact"), 4)]),
        ("Distances and scale", [(X.gen(UK5S, "g_dist", n=6), 6), (X.gen(US8S, "g_dist", n=5), 5), (X.gen(US8S, "g_fact"), 4), (X.gen(US8S, "g_ratio"), 3), (pool, 2)]),
        ("Years and orbits", [(X.gen(UK5S, "g_year", n=6), 6), (X.gen(US8G, "g_pl"), 6), (X.gen(US5G, "g_moon", n=4), 4), (pool, 4)]),
        ("Stars, galaxies and light years", [(X.gen(UK7S, "g_ly", n=6), 6), (X.gen(US5S, "g_sunvs"), 4), (X.gen(US5S, "g_table_bright"), 4), (pool, 6)]),
        ("Solar system investigations", [(X.gen(US8S, "g_model", n=5), 5), (X.gen(AU6S, "g_tab", n=5), 5), (X.B(UK5S, "B5"), 4), (X.B(US8S, "B5"), 3), (X.gen(US5S, "g_lamps"), 3)]),
    ]


def s_emsun(X):
    pool = X.pool([
        ("What causes day and night?", "Earth rotating (spinning) on its axis", ["Earth orbiting the Sun", "the Moon blocking the Sun", "the Sun moving around Earth"], "One rotation takes about 24 hours."),
        ("How long does Earth take to orbit the Sun once?", "about 365 days (one year)", ["one day", "one month", "one week"], "That is why we have years."),
        ("What causes the seasons?", "the tilt of Earth's axis as it orbits the Sun", ["Earth getting closer to the Sun in summer", "the Moon's phases", "clouds"], "In June the Northern Hemisphere tilts toward the Sun."),
        ("Why is it summer in Ontario in July?", "The Northern Hemisphere is tilted toward the Sun, so sunlight is more direct and days are longer.", ["Earth is closest to the Sun in July.", "The Sun is hotter in July.", "The Moon is full in July."], "Tilt, not distance, makes the seasons."),
        ("Why are winter days short in Ontario?", "The Northern Hemisphere is tilted away from the Sun.", ["The Sun is turned down.", "Earth stops spinning.", "Clouds block the Sun all day."], "Less daylight and less direct sunlight."),
        ("Why does the Moon seem to change shape?", "We see different amounts of its sunlit half as it orbits Earth.", ["Earth's shadow covers part of it every night.", "The Moon grows and shrinks.", "Clouds cover it."], "These are the phases of the Moon."),
        ("How long does the Moon take to go through all its phases?", "about a month (29.5 days)", ["one day", "one year", "one week"], "The word month comes from Moon."),
        ("What happens in a solar eclipse?", "The Moon passes between the Sun and Earth and blocks the Sun.", ["Earth blocks the Moon.", "The Sun goes out.", "Clouds cover the Sun."], "Never look at the Sun, even during an eclipse."),
        ("What happens in a lunar eclipse?", "Earth's shadow falls on the Moon.", ["The Moon blocks the Sun.", "The Moon stops orbiting.", "The Sun hides behind Earth's clouds."], "The Moon can look red."),
        ("Which direction does the Sun appear to rise?", "east", ["west", "north", "south"], "Earth spins from west to east."),
        ("Why do we see the same side of the Moon all the time?", "The Moon spins once for each orbit of Earth.", ["The Moon does not spin.", "The other side is dark forever.", "Earth blocks the other side."], "This is called being tidally locked."),
        ("What causes ocean tides?", "mainly the Moon's gravity pulling on Earth's water", ["wind only", "fish swimming", "the Sun's light"], "Two high tides a day happen in most places."),
        ("What does a sundial use to tell time?", "the shadow made by the Sun", ["the Moon's phases", "stars", "the tides"], "Shadows move as Earth rotates."),
        ("Why are shadows shortest at noon?", "The Sun is highest in the sky.", ["The Sun is lowest in the sky.", "The Moon is out.", "It is always cloudy at noon."], "High Sun, short shadow."),
    ])
    return [
        ("Day and night", [(pool, 6), (X.gen(UK5D, "g_turn", n=6), 6), (X.gen(UK5D, "g_sky"), 4), (X.gen(US5N, "g_rot"), 2), (X.gen(US5N, "g_degrees"), 2)]),
        ("The seasons", [(X.gen(US8M, "g_season"), 6), (X.gen(UK7S, "g_tilt"), 5), (X.gen(UK9G, "g_season"), 3), (pool, 6)]),
        ("Phases of the Moon", [(X.gen(UK5D, "g_phase"), 7), (X.gen(US8M, "g_next", n=6), 6), (X.gen(US8M, "g_name"), 4), (pool, 3)]),
        ("Eclipses and tides", [(X.gen(US8M, "g_ecl"), 6), (X.gen(US8M, "g_order"), 6), (pool, 6), (X.B(US8M, "B1"), 2)]),
        ("Sky investigations", [(X.gen(US5N, "g_month"), 5), (X.gen(US5N, "g_table"), 5), (X.B(US8M, "B5"), 4), (X.B(UK5D, "B5"), 3), (X.B(US5N, "B5"), 3)]),
    ]


def s_explore(X):
    pool = X.pool([
        ("What is the Canadarm?", "a robotic arm built in Canada and used on the space shuttle and space station", ["a Canadian rocket", "a telescope", "a space suit"], "Canadarm2 is on the International Space Station."),
        ("Who was the first Canadian to command the International Space Station?", "Chris Hadfield", ["Roberta Bondar", "Marc Garneau", "David Saint-Jacques"], "He commanded it in 2013."),
        ("Who was the first Canadian in space?", "Marc Garneau", ["Chris Hadfield", "Jeremy Hansen", "Julie Payette"], "He flew in 1984."),
        ("Jeremy Hansen is part of which NASA mission to fly around the Moon?", "Artemis II", ["Apollo 11", "Voyager 1", "Mars Pathfinder"], "He is the first Canadian on a Moon mission."),
        ("What is a satellite?", "an object that orbits a planet", ["a star", "a comet's tail", "a planet with rings"], "The Moon is a natural satellite."),
        ("Which is a use of artificial satellites?", "weather forecasts, GPS and phone signals", ["growing crops in space", "making the Moon brighter", "stopping earthquakes"], "Canada's RADARSAT satellites watch ice and forests."),
        ("Why do astronauts float on the space station?", "They and the station are falling around Earth together.", ["There is no gravity in space at all.", "They wear magnet boots.", "The station has no air."], "They are in constant free fall."),
        ("Why do astronauts exercise every day on the space station?", "Without Earth's pull, their muscles and bones get weaker.", ["To keep warm", "To make electricity", "To steer the station"], "Exercise keeps them healthy."),
        ("What does a space telescope like the James Webb Space Telescope do?", "It sees faraway stars and galaxies without Earth's air in the way.", ["It lands on planets.", "It mines asteroids.", "It carries astronauts."], "Canada built parts of the Webb telescope."),
        ("What do rovers on Mars do?", "drive on the surface and study rocks, soil and air", ["carry people", "make Mars warmer", "pull Mars closer"], "Rovers are robots controlled from Earth."),
        ("What is space junk?", "old satellites and pieces of rockets orbiting Earth", ["rocks on the Moon", "comets", "stars that burned out"], "It can hit working satellites."),
        ("Which technology from space research is used on Earth?", "memory foam and water filters", ["pencils", "wheels", "bricks"], "Many inventions came from space research."),
        ("What is one cost of space exploration?", "It is very expensive and uses a lot of fuel.", ["It is free.", "It needs no energy.", "It has no risks."], "People debate how to spend the money."),
        ("Why do astronauts wear space suits on a spacewalk?", "to give air and protect them from extreme temperatures and radiation", ["to look nice only", "to float better", "to make them heavier"], "Space has no air to breathe."),
        ("How did many Indigenous Peoples use the night sky?", "to tell time, find directions and mark seasons", ["only to make phone calls", "to predict earthquakes only", "they did not use it"], "Star knowledge is passed down through stories."),
        ("Which instrument lets you see craters on the Moon from your backyard?", "a telescope or binoculars", ["a microscope", "a thermometer", "a compass"], "Telescopes make faraway things look closer."),
        ("What is the International Space Station?", "a science lab that orbits Earth with astronauts on board", ["a hotel on the Moon", "a rocket that goes to Mars", "a telescope on a mountain"], "Canada is one of its partners."),
        ("Why are rockets launched with huge amounts of fuel?", "They need a lot of thrust to escape Earth's gravity.", ["To keep astronauts warm", "To light the way", "Because space is full of air"], "Leaving Earth takes a lot of energy."),
    ])
    return [
        ("Canadians in space", [(pool, 10), (X.gen(US8G, "g_scn"), 5), (X.B(UK7S, "B1"), 5)]),
        ("Satellites and telescopes", [(pool, 10), (X.gen(US5G, "g_globe", n=5), 5), (X.B(US5S, "B1"), 5)]),
        ("Gravity in space", [(X.gen(UK9G, "g_weight", n=6), 6), (X.gen(US5G, "g_drop", n=5), 5), (X.gen(US8G, "g_scale"), 3), (pool, 6)]),
        ("Living and working in space", [(pool, 10), (X.B(US8G, "B1"), 5), (X.B(UK9G, "B1"), 4), (X.gen(UK9G, "g_mw"), 1)]),
        ("Space investigations", [(X.B(US8G, "B5"), 4), (X.B(UK7S, "B5"), 4), (X.B(US5G, "B5"), 4), (X.gen(US5G, "g_claim"), 3), (pool, 5)]),
    ]


def UNITS():
    return [
        CU("B", 1, "classifying-living-things", "B2.1, B2.2, B2.3",
           "Describe biodiversity as the variety of life; classify organisms into groups (kingdoms, vertebrates and invertebrates) "
           "using their characteristics; use and make dichotomous keys.",
           "Classifying Living Things", "Classifying living things",
           "Free Grade 6 science worksheets on biodiversity, kingdoms, vertebrates, invertebrates and dichotomous keys, with Ontario "
           "plants and animals. 100 questions with answers.",
           "Scientists group living things by features.", "Vertebrates have a backbone; keys split groups in two at each step.",
           L("Biodiversity is the variety of living things. Classification sorts them into groups by shared features.",
             "Kingdoms include animals, plants and fungi (and tiny living things like bacteria).",
             "Vertebrates have a backbone: fish, amphibians, reptiles, birds and mammals.",
             "Invertebrates have no backbone: insects, spiders, worms, snails.",
             "A dichotomous key asks yes-or-no questions to name a living thing."),
           [("A frog has moist skin and starts life as a tadpole. Which group is it in?", ["moist skin", "water then land"], "amphibians"),
            ("Is a spider an insect?", ["count the legs: 8"], "no, it is an arachnid")],
           ["Thinking spiders are insects.", "Thinking whales are fish (they are mammals).", "Thinking fungi are plants."],
           [("What is biodiversity?", "The variety of living things in an area, from tiny insects to large trees and animals."),
            ("What is the difference between vertebrates and invertebrates?", "Vertebrates have a backbone. Invertebrates do not."),
            ("How does a dichotomous key work?", "It gives two choices at each step. You choose the one that fits until you reach the name.")],
           s_class),
        CU("B", 2, "protecting-biodiversity", "B1.1, B1.2, B2.4, B2.5",
           "Explain why biodiversity is important; assess the effects of human activities, invasive species and habitat loss on "
           "biodiversity; evaluate ways to protect species, including Indigenous approaches.",
           "Protecting Biodiversity", "Protecting biodiversity",
           "Free Grade 6 science worksheets on why biodiversity matters, species at risk, invasive species and conservation in "
           "Ontario. 100 questions with answers.",
           "Biodiversity keeps ecosystems strong.", "Habitat loss, pollution and invasive species threaten it; protecting habitats helps.",
           L("Ecosystems with many species are healthier and recover better from change.",
             "Biodiversity gives people food, medicine, clean water and pollination (ecosystem services).",
             "Threats: habitat loss, pollution, climate change, invasive species like the emerald ash borer.",
             "Protection: parks, planting native species, laws for species at risk, Indigenous stewardship."),
           [("Why is the emerald ash borer a problem?", ["it is invasive", "no natural predators"], "it kills ash trees"),
            ("How can people help monarch butterflies?", ["caterpillars eat only milkweed"], "plant milkweed")],
           ["Thinking extinction only happened to dinosaurs.", "Thinking any new species is good for an ecosystem.", "Thinking one person cannot help."],
           [("What is a species at risk?", "A species that could disappear from the wild, like the woodland caribou or the Blanding's turtle in Ontario."),
            ("What is an invasive species?", "A species brought to a new area where it spreads quickly and harms native species."),
            ("How can students help biodiversity?", "Plant native plants, keep pets from being released, reduce waste and help clean up natural areas.")],
           s_protect),
        CU("C", 3, "static-electricity", "C2.1, C2.2, C2.3",
           "Describe static electricity as a build-up of charge; explain attraction and repulsion between charges; describe "
           "lightning and ways to stay safe; distinguish static and current electricity.",
           "Static Electricity", "Static electricity",
           "Free Grade 6 science worksheets on electric charge, attract and repel, static in daily life, lightning safety and "
           "magnetism. 100 questions with answers.",
           "Like charges repel; unlike charges attract.", "Rubbing moves electrons, so objects build up static charge until it jumps as a spark.",
           L("Static electricity is electric charge that builds up on the surface of an object.",
             "Rubbing two materials moves electrons from one to the other.",
             "Like charges (+ and +, or − and −) repel. Unlike charges (+ and −) attract.",
             "A spark or shock happens when built-up charge jumps. Lightning is a giant spark."),
           [("Two balloons both rubbed on hair are held close. What happens?", ["both have the same charge"], "they repel"),
            ("Why do shocks happen more in winter?", ["dry air", "charge builds up"], "charge jumps to metal")],
           ["Thinking static electricity flows in a circuit.", "Thinking charged objects are magnets.", "Thinking protons move when objects are rubbed."],
           [("What causes static electricity?", "Rubbing moves electrons from one material to another, so one becomes negative and the other positive."),
            ("Why does a balloon stick to a wall?", "The charged balloon pulls opposite charges in the wall closer, so they attract."),
            ("How can you stay safe in a thunderstorm?", "Go indoors, stay away from tall trees, water and metal fences, and wait 30 minutes after the last thunder.")],
           s_static),
        CU("C", 4, "electric-circuits", "C2.4, C2.5, C2.6, C1.1",
           "Describe the parts of a circuit; distinguish conductors and insulators; build and compare series and parallel circuits; "
           "describe how electricity is generated and ways to use it safely and conserve it.",
           "Electric Circuits", "Electric circuits",
           "Free Grade 6 science worksheets on circuits, conductors and insulators, series and parallel circuits, electrical safety "
           "and saving electricity in Ontario. 100 questions with answers.",
           "Current flows in a closed circuit.", "Series circuits have one path; parallel circuits have many, so one bulb can go out alone.",
           L("A circuit needs an energy source, conductors and a closed loop.",
             "Conductors (metals) let current flow; insulators (plastic, rubber, wood) do not.",
             "Series circuit: one path. Parallel circuit: several paths, like wiring in a house.",
             "Generators in power plants change motion into electricity; we pay for energy in kWh.",
             "Safety: keep water away, do not overload outlets, stay away from power lines."),
           [("A switch is open. Does the bulb light?", ["there is a gap"], "no"),
            ("One bulb in a parallel circuit breaks. Do the others stay on?", ["other paths are complete"], "yes")],
           ["Thinking a battery 'pushes out' only one way so the second wire is not needed.", "Mixing up series and parallel.", "Thinking all metals are insulators when they are cold."],
           [("What is the difference between a series and a parallel circuit?", "A series circuit has one path. A parallel circuit has two or more paths, so devices work on their own."),
            ("Why are wires covered in plastic?", "Plastic is an insulator, so it keeps the current in the wire and protects people from shocks."),
            ("How can we save electricity?", "Turn off lights and devices, unplug chargers, use LED bulbs and run appliances at off-peak times.")],
           s_circuit),
        CU("D", 5, "forces-of-flight", "D2.1, D2.2, D2.3",
           "Identify the four forces of flight (lift, weight, thrust and drag); explain how Bernoulli's principle and wing shape "
           "produce lift; describe how changing the forces changes an aircraft's motion.",
           "The Four Forces of Flight", "Forces of flight",
           "Free Grade 6 science worksheets on lift, weight, thrust and drag, Bernoulli's principle, wing shape, control surfaces "
           "and streamlining. 100 questions with answers.",
           "Lift, weight, thrust and drag act on a plane.", "Lift beats weight to rise; thrust beats drag to speed up; balanced forces mean steady flight.",
           L("Four forces act on anything that flies.",
             "Lift pushes up and weight (gravity) pulls down. Thrust pushes forward and drag pulls back.",
             "Bernoulli's principle: faster air has lower pressure. A curved wing (airfoil) makes faster air over the top, giving lift.",
             "Rudder, elevators and ailerons steer the plane. Streamlined shapes reduce drag."),
           [("Lift is 80 kN and weight is 60 kN. What happens?", ["lift is bigger"], "the plane climbs"),
            ("Which force does a jet engine make?", ["it pushes the plane forward"], "thrust")],
           ["Mixing up thrust and lift.", "Thinking planes need no lift once they are moving.", "Thinking drag only acts on slow planes."],
           [("What are the four forces of flight?", "Lift (up), weight (down), thrust (forward) and drag (backward)."),
            ("How does a wing make lift?", "The curved wing makes air move faster over the top, so pressure above is lower than below, and the wing is pushed up."),
            ("Why are planes streamlined?", "A smooth, pointed shape reduces drag, so the plane uses less fuel.")],
           s_flight),
        CU("D", 6, "flight-in-nature-and-technology", "D1.1, D1.2, D2.4, D2.5",
           "Describe how animals and seeds fly or glide; explain how people have used ideas from nature in flying devices; assess "
           "the social and environmental impacts of aviation and drones.",
           "Flight in Nature and Technology", "Flight in nature and technology",
           "Free Grade 6 science worksheets on how birds, seeds and gliders fly, airplanes, drones, bush planes and the effects of air "
           "travel. 100 questions with answers.",
           "Nature inspired many flying machines.", "Birds, maple keys and dandelion seeds use the same forces as airplanes.",
           L("Living things and machines use the same four forces to fly.",
             "Birds flap for thrust and have light, hollow bones; maple keys spin; dandelion seeds use parachutes.",
             "People copied nature (biomimicry) to design wings, gliders and drones.",
             "Air travel connects remote communities but adds pollution and noise."),
           [("How does a maple key fall slowly?", ["it spins like a rotor"], "spinning makes lift"),
            ("Why do Canada geese fly in a V?", ["each bird rides on air from the one ahead"], "to save energy")],
           ["Thinking all birds can fly.", "Thinking gliders have engines.", "Thinking air travel has no effect on the environment."],
           [("How do birds fly?", "They flap their wings to make thrust, and their wing shape makes lift. Light, hollow bones keep their weight low."),
            ("What is biomimicry?", "Designing technology by copying nature, such as aircraft wings based on bird wings."),
            ("Why are bush planes important in Canada?", "They reach communities in the north without roads, landing on lakes with floats in summer and skis in winter.")],
           s_flight2),
        CU("E", 7, "the-solar-system", "E2.1, E2.2, E2.3",
           "Identify the Sun, planets, moons, asteroids and comets in the solar system; describe their properties and distances; "
           "describe stars, constellations and galaxies.",
           "The Solar System", "The solar system",
           "Free Grade 6 science worksheets on the Sun, the eight planets, orbits, distances, stars, constellations and light years. "
           "100 questions with answers.",
           "Eight planets orbit the Sun.", "Rocky inner planets, gas and ice giants further out, all held in orbit by the Sun's gravity.",
           L("Our solar system is the Sun and everything that orbits it.",
             "Planets in order: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.",
             "The inner planets are rocky; the outer planets are giants of gas and ice.",
             "Stars make their own light. Constellations are star patterns; galaxies hold billions of stars."),
           [("Which planet comes after Mars?", ["the order: … Earth, Mars, Jupiter"], "Jupiter"),
            ("Why do planets further out take longer to orbit?", ["longer path", "slower speed"], "they have a longer year")],
           ["Thinking the Moon and planets make their own light.", "Thinking the Sun is the biggest star.", "Thinking a light year is a unit of time."],
           [("Which planets are gas giants?", "Jupiter and Saturn are gas giants. Uranus and Neptune are ice giants."),
            ("What keeps planets in orbit?", "The Sun's gravity pulls on them while they move sideways, so they keep circling."),
            ("What is a light year?", "The distance light travels in one year, about 9.5 trillion kilometres.")],
           s_solar),
        CU("E", 8, "earth-moon-and-sun", "E2.4, E2.5",
           "Describe how Earth's rotation and revolution cause day, night and years; explain how the tilt of Earth's axis causes "
           "seasons; describe the phases of the Moon, eclipses and tides.",
           "Earth, Moon and Sun", "Earth, Moon and Sun",
           "Free Grade 6 science worksheets on day and night, seasons, phases of the Moon, eclipses and tides. 100 questions with answers.",
           "Rotation makes day; tilt makes seasons.", "Earth spins once a day and orbits once a year; the Moon's phases repeat about every month.",
           L("Earth rotates on its axis once every 24 hours and revolves around the Sun once a year.",
             "Day and night come from rotation. Seasons come from the tilt of Earth's axis.",
             "The Moon orbits Earth about once a month, and we see different phases of its sunlit half.",
             "Solar eclipse: the Moon blocks the Sun. Lunar eclipse: Earth's shadow covers the Moon."),
           [("What causes seasons?", ["tilt toward the Sun in summer", "tilt away in winter"], "the tilt of Earth's axis"),
            ("What causes day and night?", ["Earth spins"], "rotation")],
           ["Thinking seasons happen because Earth is closer to the Sun in summer.", "Thinking Earth's shadow causes the Moon's phases.", "Mixing up rotation and revolution."],
           [("What is the difference between rotation and revolution?", "Rotation is spinning on an axis (one day). Revolution is travelling around the Sun (one year)."),
            ("Why do we have seasons?", "Earth's axis is tilted. When our hemisphere tilts toward the Sun, sunlight is more direct and days are longer, so it is summer."),
            ("Why does the Moon have phases?", "As the Moon orbits Earth, we see different amounts of the half that the Sun lights up.")],
           s_emsun),
        CU("E", 9, "space-exploration", "E1.1, E1.2, E2.6",
           "Describe technologies used to explore space, including Canadian contributions such as the Canadarm and Canadian "
           "astronauts; assess the benefits and costs of space exploration.",
           "Space Exploration", "Space exploration",
           "Free Grade 6 science worksheets on satellites, telescopes, rovers, the International Space Station, Canadarm and "
           "Canadian astronauts. 100 questions with answers.",
           "Technology lets us explore space.", "Satellites, telescopes, rovers and astronauts study space, and Canada has played a big part.",
           L("People explore space with rockets, satellites, telescopes, rovers and astronauts.",
             "Satellites give us weather forecasts, GPS and communications.",
             "Canada built the Canadarm and Canadarm2; Canadian astronauts include Marc Garneau, Roberta Bondar, Chris Hadfield and Jeremy Hansen.",
             "Space research gives inventions we use on Earth, but it costs a lot and leaves space junk."),
           [("What is a satellite?", ["it orbits a planet"], "an object in orbit"),
            ("Why do astronauts exercise in space?", ["muscles and bones weaken without gravity's pull"], "to stay strong")],
           ["Thinking there is no gravity in space.", "Thinking satellites stay still above Earth.", "Thinking space exploration has no effect on daily life."],
           [("How has Canada helped explore space?", "Canada built the Canadarm robotic arms, satellites like RADARSAT and parts of the James Webb Space Telescope, and has many astronauts."),
            ("Why do astronauts float?", "They are falling around Earth at the same speed as the station, so they seem weightless."),
            ("What are the costs of space exploration?", "It is very expensive, uses lots of fuel and adds space junk, so people discuss how to balance it with needs on Earth.")],
           s_explore),
    ]
