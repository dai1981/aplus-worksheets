# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 4 (B Habitats and Communities, C Light and Sound, D Machines and Mechanisms,
E Rocks, Minerals, and Erosion). Built by caon_sci.build; gen_caon_science_g4_* only call it."""
from caon_sci import CU

UK2H, UK2M = "gen_uk_science_y2_habitats", "gen_uk_science_y2_microhabitats"
US3H, SG6H = "gen_us_science_g3_habitats_and_survival", "gen_sg_science_p6_habitats_populations_and_communities"
AU6H, UK4F = "gen_au_science_y6_physical_conditions_of_habitats", "gen_uk_science_y4_food_chains"
US5F, SG6F = "gen_us_science_g5_food_webs", "gen_sg_science_p6_food_chains_and_food_webs"
AU4P, UK4C = "gen_au_science_y4_producers_consumers_and_decomposers", "gen_uk_science_y4_changing_environments"
AU5S, SG6A, US3E = "gen_au_science_y5_structural_adaptations", "gen_sg_science_p6_adaptations", "gen_us_science_g3_environmental_change"
UK6L, UK3L, US4L = "gen_uk_science_y6_how_light_travels", "gen_uk_science_y3_light_and_dark", "gen_us_science_g4_light_and_how_we_see"
US1M, UK7L, UK6S = "gen_us_science_g1_light_and_materials", "gen_uk_science_y7_light", "gen_uk_science_y6_shadows_and_reflection"
UK4S, UK4P, US1S, UK7S = ("gen_uk_science_y4_how_sounds_are_made", "gen_uk_science_y4_pitch_and_volume",
                          "gen_us_science_g1_sound_and_vibrations", "gen_uk_science_y7_sound")
UK5M, UK3R, AU5W = "gen_uk_science_y5_levers_pulleys_and_gears", "gen_uk_science_y3_comparing_and_grouping_rocks", "gen_au_science_y5_weathering_erosion_and_deposition"
US2E, US4R, UK3F = "gen_us_science_g2_fast_and_slow_earth_changes", "gen_us_science_g4_rock_layers_and_fossils", "gen_uk_science_y3_how_fossils_are_formed"


def s_habitats(X):
    pool = X.pool([
        ("What is a habitat?", "the place where a plant or animal lives and gets what it needs", ["a kind of food", "an animal's family", "the weather in one day"], "A habitat gives food, water, shelter and space."),
        ("A beaver builds a lodge in a pond. What need does the lodge meet?", "shelter", ["food", "sunlight", "air"], "The lodge keeps the beaver safe and warm."),
        ("Which Ontario habitat is wet land covered with shallow water and cattails?", "a wetland (marsh)", ["a desert", "a tundra", "a coral reef"], "Marshes have shallow water and tall plants."),
        ("What is a community?", "all the plants and animals that live together in one habitat", ["one kind of animal", "only the plants in a forest", "the soil and rocks in a place"], "A community includes all the living things in a habitat."),
        ("Which is a non-living part of a forest habitat?", "rocks", ["moss", "a chipmunk", "a mushroom"], "Rocks, water, air and sunlight are non-living."),
        ("A loon needs clean lakes with fish. What would happen if the lake became polluted?", "The loon might not find enough food and might leave or die.", ["The loon would grow bigger.", "Nothing would change.", "The loon would start eating plants."], "Habitats must meet an animal's needs."),
        ("Which animal lives in the boreal forest of northern Ontario?", "a moose", ["a camel", "a penguin", "a giraffe"], "Moose live in forests with lakes and wetlands."),
        ("What do all animals need from their habitat?", "food, water, shelter and space", ["only sunlight", "only shelter", "toys and light"], "These are the needs of animals."),
        ("A chickadee stays in Ontario all winter. Which part of its habitat helps it survive the cold?", "evergreen trees for shelter and seeds to eat", ["warm sand", "a frozen lake", "a desert cactus"], "Trees give shelter and food."),
        ("Why can a fish not live in a forest?", "A fish needs water to breathe and move.", ["A fish needs more sunlight.", "Forests are too quiet.", "Fish only eat leaves."], "Each living thing is suited to its habitat."),
        ("Which is a habitat for frogs in Ontario?", "a pond with plants around the edge", ["a dry parking lot", "a sandy desert", "the top of a mountain in winter"], "Frogs need water and damp places."),
        ("What is a population?", "all the members of one kind of living thing in an area", ["all the different animals in a forest", "the weather in an area", "a group of rocks"], "For example, all the white-tailed deer in a park."),
    ])
    term = X.pool([
        ("Which word means 'a living thing'?", "organism", ["habitat", "community", "climate"], "Plants, animals and fungi are organisms."),
        ("A raccoon, a maple tree and some worms all live in the same park. What is this group called?", "a community", ["a population", "a habitat", "a food"], "Different living things in one place make a community."),
        ("All the Canada geese in one wetland are a …", "population", ["community", "habitat", "food chain"], "One kind of animal in one place is a population."),
        ("Which pair are both non-living parts of a habitat?", "water and sunlight", ["grass and water", "a frog and sunlight", "a tree and a rock"], "Living things grow and reproduce; water and sunlight do not."),
        ("Which is a living part of a pond?", "algae", ["mud", "water", "a rock"], "Algae are living things."),
    ])
    return [
        ("Habitats and needs", [(pool, 8), (X.gen(UK2H, "g_home", n=6), 6), (X.gen(UK2H, "g_suit", n=4), 4), (X.B(UK2H, "B1"), 2)]),
        ("Living and non-living parts", [(term, 4), (X.gen(SG6H, "g_term", n=7), 7), (X.gen(UK2M, "g_cond"), 4), (pool, 2), (X.gen(UK2M, "g_where", n=3), 3)]),
        ("Populations and communities", [(X.gen(SG6H, "g_which"), 6), (X.gen(SG6H, "g_count", n=4), 4), (X.B(SG6H, "B1"), 4), (X.B(SG6H, "B2"), 3), (pool, 3)]),
        ("Surviving in a habitat", [(X.gen(US3H, "g_where", n=6), 6), (X.gen(US3H, "g_why"), 6), (X.gen(US3H, "g_wont", n=4), 4), (X.B(US3H, "B1"), 4)]),
        ("Habitat investigations", [(X.gen(UK2M, "g_hunt", n=4), 4), (X.gen(UK2M, "g_chamber", n=4), 4), (X.B(UK2M, "B5"), 3), (X.B(SG6H, "B5"), 4), (X.gen(SG6H, "g_exp", n=3), 3), (X.B(US3H, "B5"), 2)]),
    ]


def s_food(X):
    pool = X.pool([
        ("In an Ontario forest: maple leaves → caterpillar → chickadee → hawk. Which is the producer?", "maple leaves", ["caterpillar", "chickadee", "hawk"], "Plants make their own food using sunlight."),
        ("In a pond: algae → tadpole → fish → heron. Which is the top consumer?", "heron", ["algae", "tadpole", "fish"], "The heron is at the end of the chain."),
        ("Which living thing is a decomposer?", "a mushroom", ["a clover", "a rabbit", "a fox"], "Fungi break down dead things."),
        ("What do decomposers return to the soil?", "nutrients", ["sunlight", "plastic", "oxygen gas only"], "Nutrients help new plants grow."),
        ("Where does the energy in almost every food chain come from first?", "the Sun", ["the soil", "the water", "the top predator"], "Plants use the Sun's energy to make food."),
        ("A wolf eats deer. A deer eats grass. What is the deer?", "a herbivore and a consumer", ["a producer", "a decomposer", "a carnivore"], "Deer eat only plants."),
        ("Which animal is an omnivore?", "a black bear (eats berries and fish)", ["a white-tailed deer", "a snowshoe hare", "a lynx"], "Omnivores eat plants and animals."),
        ("What does an arrow in a food chain show?", "the direction energy moves when one thing is eaten", ["which animal is bigger", "where the animal lives", "which animal is faster"], "The arrow points to the eater."),
        ("What is a food web?", "many food chains that are linked together", ["one food chain", "a spider's web", "a list of plants"], "Most animals eat more than one thing."),
        ("Snowshoe hares eat plants. Lynx eat hares. If the number of hares falls, what happens to the lynx?", "There is less food, so the number of lynx falls.", ["The lynx population grows.", "Lynx start making their own food.", "Nothing changes."], "Predators depend on their prey."),
        ("Which is a scavenger that eats dead animals?", "a turkey vulture", ["a cow", "a maple tree", "a bee"], "Scavengers clean up dead animals."),
        ("Lake food chain: algae → zooplankton → minnow → walleye. What does the minnow eat?", "zooplankton", ["algae", "walleye", "sunlight"], "Follow the arrow into the minnow."),
        ("Lake food chain: algae → zooplankton → minnow → walleye → osprey. What eats the walleye?", "osprey", ["minnow", "zooplankton", "algae"], "The arrow from walleye points to the osprey."),
        ("Meadow food chain: clover → grasshopper → garter snake → red-tailed hawk. Which is a carnivore that is also eaten?", "garter snake", ["clover", "grasshopper", "red-tailed hawk"], "The snake eats grasshoppers and is eaten by hawks."),
        ("Forest food web: acorns are eaten by squirrels, chipmunks and deer. Foxes eat squirrels and chipmunks. Wolves eat deer. What does the fox eat?", "squirrels and chipmunks", ["acorns", "deer", "wolves"], "Read the links to the fox."),
        ("In the same forest web, a disease kills most of the oak trees. Which animals lose food first?", "squirrels, chipmunks and deer", ["foxes and wolves only", "no animals", "only the wolves"], "Herbivores depend directly on the producer."),
        ("Pond food web: algae and duckweed are eaten by tadpoles and snails. Fish eat tadpoles. Herons eat fish and frogs. Which living things are producers?", "algae and duckweed", ["tadpoles and snails", "fish", "herons"], "Producers are the plants and algae."),
        ("A farmer sprays a field to kill all the grasshoppers. What might happen to the frogs that eat them?", "The frogs have less food and their number may fall.", ["The frogs get more food.", "The frogs start eating grass.", "Nothing happens to the frogs."], "Changes travel through food webs."),
        ("Why are there usually fewer wolves than deer in a forest?", "Energy is lost at each step, so there is less energy for animals higher up the chain.", ["Wolves are smaller.", "Wolves eat plants.", "Deer eat wolves."], "Each level supports fewer animals."),
        ("Which animal in an Ontario forest is a carnivore?", "a red fox", ["a white-tailed deer", "a cottontail rabbit", "a beaver"], "Foxes hunt small animals."),
        ("Which is a herbivore?", "a moose", ["a lynx", "a wolf", "a great horned owl"], "Moose eat plants only."),
        ("What is prey?", "an animal that is hunted and eaten by another animal", ["an animal that hunts", "a plant that makes food", "a decomposer"], "Mice are prey for owls."),
        ("Bacteria in the soil break down a dead tree. What role do they play?", "decomposers", ["producers", "predators", "herbivores"], "Bacteria recycle nutrients."),
        ("Earthworms eat dead leaves. What role do they play?", "decomposer (they break down dead material)", ["producer", "top predator", "herbivore only"], "Worms help recycle nutrients."),
    ])
    return [
        ("Producers, consumers, decomposers", [(pool, 6), (X.gen(UK4F, "g_role", n=8), 8), (X.gen(AU4P, "g_role", n=4), 4), (X.B(AU4P, "POOL1"), 2)]),
        ("Food chains", [(X.gen(US5F, "g_chain", n=6), 6), (X.gen(UK4F, "g_order"), 5), (X.gen(UK4F, "g_word"), 5), (pool, 4)]),
        ("Food webs", [(X.gen(US5F, "g_eats", n=5), 5), (X.gen(US5F, "g_eaten_by", n=5), 5), (X.gen(US5F, "g_kind", n=4), 4), (X.gen(US5F, "g_count", n=3), 3), (pool, 3)]),
        ("Changes in a food web", [(X.gen(UK4F, "g_effect", n=7), 7), (X.gen(US5F, "g_remove", n=5), 5), (X.gen(US5F, "g_increase", n=4), 4), (pool, 4)]),
        ("Energy and the Sun", [(X.gen(US5F, "g_sun", n=5), 5), (X.B(US5F, "B1"), 5), (X.B(UK4F, "B1"), 4), (X.B(SG6F, "B5"), 3), (pool, 2), (X.B(US5F, "B5"), 1)]),
    ]


def s_adapt(X):
    pool = X.pool([
        ("Why does a snowshoe hare's fur turn white in winter?", "to blend in with the snow and hide from predators", ["to stay cooler", "to see better", "to swim faster"], "Camouflage helps it survive."),
        ("Why does a beaver have a flat tail?", "to steer in water and slap a warning", ["to dig tunnels", "to climb trees", "to catch insects"], "The tail is a structural adaptation."),
        ("Many birds fly south in the fall. What is this behaviour called?", "migration", ["hibernation", "camouflage", "pollination"], "They move to find food and warmth."),
        ("What do groundhogs do in winter?", "hibernate (sleep deeply with a slow heartbeat)", ["migrate to the tropics", "grow gills", "change into a plant"], "Hibernation saves energy when food is scarce."),
        ("Why do moose have long legs?", "to walk through deep snow and marshes", ["to climb trees", "to swim under ice", "to dig burrows"], "Long legs suit their habitat."),
        ("Building a highway through a forest splits a habitat in two. What is one effect?", "Animals cannot move safely to find food or mates.", ["Animals get more space.", "The forest grows faster.", "Nothing happens to animals."], "Habitat loss and fragmentation harm wildlife."),
        ("Which action helps protect a wetland habitat?", "keeping garbage and pollution out of it", ["draining the water", "cutting down the plants", "building a parking lot"], "Clean water helps the community."),
        ("Zebra mussels came to the Great Lakes on ships. Why are they a problem?", "They crowd out and compete with local species.", ["They are a native species.", "They clean pollution and help all animals.", "They are producers."], "Invasive species upset food webs."),
        ("What is an adaptation?", "a feature or behaviour that helps a living thing survive in its habitat", ["any change in the weather", "a kind of habitat", "a place to sleep"], "Adaptations can be body parts or behaviours."),
        ("Why do porcupines have quills?", "to protect themselves from predators", ["to keep cool", "to catch fish", "to fly"], "Quills are a structural adaptation."),
        ("How did Indigenous Peoples traditionally care for the land when hunting and harvesting?", "by taking only what they needed so plants and animals could renew", ["by taking everything at once", "by removing all predators", "by draining wetlands"], "Respect for the land helps habitats stay healthy."),
        ("Why are wildlife crossings built over some highways?", "so animals can cross safely between parts of their habitat", ["to slow down cars only", "to give birds a place to nest on cars", "to collect rainwater"], "Crossings reduce road deaths."),
    ])
    return [
        ("Structural adaptations", [(pool, 5), (X.gen(AU5S, "g_feat", n=6), 6), (X.gen(SG6A, "g_feat"), 5), (X.gen(SG6A, "g_purpose", n=4), 4)]),
        ("Behaviour and survival", [(X.gen(SG6A, "g_type", n=6), 6), (X.gen(SG6A, "g_which"), 6), (pool, 4), (X.B(SG6A, "B1"), 4)]),
        ("Changing habitats", [(X.gen(UK4C, "g_cause"), 6), (X.gen(UK4C, "g_eff"), 6), (X.gen(UK4C, "g_good"), 5), (X.B(UK4C, "B1"), 3)]),
        ("People and habitats", [(X.gen(US3E, "g_problem"), 5), (X.gen(US3E, "g_solution"), 5), (X.gen(US3E, "g_resp"), 5), (pool, 3), (X.B(US3E, "B1"), 2)]),
        ("Studying habitats", [(X.gen(UK4C, "g_survey", n=5), 5), (X.gen(US3E, "g_data", n=4), 4), (X.gen(US3E, "g_merit", n=4), 4), (X.B(UK4C, "B5"), 3), (X.B(SG6A, "B5"), 4)]),
    ]


def s_light(X):
    pool = X.pool([
        ("Which is a natural source of light?", "the Sun", ["a flashlight", "a candle", "a street lamp"], "Natural sources are not made by people."),
        ("Which is an artificial source of light?", "a light bulb", ["the Sun", "lightning", "a firefly"], "People make artificial sources."),
        ("Is the Moon a source of light?", "No, it reflects light from the Sun.", ["Yes, it makes its own light.", "Yes, but only in winter.", "No, it absorbs all light."], "We see the Moon because it reflects sunlight."),
        ("Which material is transparent?", "clear glass", ["wood", "wax paper", "a metal pot"], "Transparent materials let almost all light through."),
        ("Which material is translucent?", "wax paper", ["clear glass", "cardboard", "a brick"], "Translucent materials let some light through."),
        ("Which material is opaque?", "a wooden board", ["clear plastic wrap", "a window", "water in a glass"], "Opaque materials block light."),
        ("Light hits a mirror and bounces off. What is this called?", "reflection", ["refraction", "absorption", "vibration"], "Smooth shiny surfaces reflect light well."),
        ("A straw in a glass of water looks bent. Why?", "Light bends (refracts) as it passes from water to air.", ["The straw really bends.", "Water makes the straw melt.", "Light stops in water."], "This is refraction."),
        ("Why does a cyclist wear a reflective vest at night?", "It reflects car headlights so drivers can see the cyclist.", ["It makes its own light.", "It keeps the cyclist warm.", "It absorbs all the light."], "Reflectors bounce light back."),
        ("How does light travel?", "in straight lines", ["in circles", "only around corners", "in zigzags only"], "That is why shadows form."),
        ("A shadow forms when …", "an opaque object blocks light", ["light passes through glass", "a mirror reflects light", "the light is turned off"], "Shadows are areas with no light."),
        ("What is one danger of light?", "Looking at the Sun can damage your eyes.", ["Light makes you shorter.", "Light is always cold.", "Light is never useful."], "Never look straight at the Sun."),
        ("Why are some lights near lakes turned down or shielded at night?", "Bright lights can confuse birds and insects.", ["Lights make the water colder.", "Fish need more light.", "Lights cause rain."], "Light pollution affects animals."),
    ])
    return [
        ("Sources of light", [(pool, 6), (X.gen(UK6L, "g_src", n=7), 7), (X.gen(UK6L, "g_srcyn"), 4), (X.gen(UK3L, "g_dark", n=3), 3)]),
        ("Materials and light", [(X.gen(US1M, "g_kind", n=8), 8), (X.gen(UK6L, "g_mat", n=7), 7), (pool, 3), (X.gen(US1M, "g_use"), 2)]),
        ("Light travels in straight lines", [(X.gen(US4L, "g_paths", n=6), 6), (X.gen(UK6L, "g_def"), 5), (X.gen(US4L, "g_one", n=5), 5), (X.gen(UK6S, "g_shape"), 4)]),
        ("Reflection and refraction", [(X.gen(UK3L, "g_refl", n=6), 6), (X.gen(UK7L, "g_refl", n=5, drop=["angle"]), 5), (X.gen(UK6S, "g_mirror"), 5), (X.gen(UK7L, "g_refr"), 2), (pool, 2)]),
        ("Light investigations", [(X.gen(UK6S, "g_shd", n=5), 5), (X.B(UK6L, "B5"), 4), (X.B(UK3L, "B5"), 4), (X.B(US4L, "B5"), 4), (X.gen(US4L, "g_dark", n=3), 3)]),
    ]


def s_sound(X):
    pool = X.pool([
        ("What makes a sound?", "something vibrating", ["something cold", "something shiny", "something heavy"], "All sounds come from vibrations."),
        ("Sound travels best through which of these?", "a solid like a wooden desk", ["empty space", "a vacuum", "nothing at all"], "Particles in solids are close together."),
        ("Why can astronauts on the Moon not hear each other without radios?", "There is no air to carry the sound.", ["The Moon is too cold.", "Their ears stop working.", "Sound only moves in water."], "Sound needs a medium."),
        ("A guitar string is tightened. What happens to the pitch?", "It gets higher.", ["It gets lower.", "It gets louder only.", "There is no sound."], "Tighter strings vibrate faster."),
        ("Which sound is the loudest?", "a jet engine", ["a whisper", "rustling leaves", "a ticking watch"], "Loud sounds can damage hearing."),
        ("How can you protect your hearing at a loud concert?", "wear earplugs or ear defenders", ["stand closer to the speakers", "turn the music up", "cover one eye"], "Loud sounds damage the inner ear."),
        ("Bats find insects at night using echoes. What is an echo?", "a sound that reflects off a surface", ["a sound that never ends", "a light that bounces", "a kind of vibration in the bat's wing"], "Echoes bounce back."),
        ("Why are highways sometimes lined with tall walls near houses?", "to block and absorb traffic noise", ["to keep cars warm", "to make sound louder", "to reflect sunlight"], "Noise barriers reduce noise pollution."),
        ("Which material would best soundproof a music room?", "thick foam panels", ["glass windows", "a metal sheet", "a tile floor"], "Soft materials absorb sound."),
        ("A drum is hit harder. What changes?", "The sound gets louder.", ["The pitch gets higher.", "The sound gets quieter.", "Nothing changes."], "Bigger vibrations make louder sounds."),
        ("Which instrument makes a lower pitch?", "a large tuba", ["a small flute", "a piccolo", "a small whistle"], "Bigger instruments vibrate more slowly."),
        ("How does a hearing aid help a person?", "It makes sounds louder so the person can hear them.", ["It makes light brighter.", "It stops all sound.", "It changes words into pictures."], "Technology can help people hear."),
    ])
    return [
        ("Vibrations make sound", [(pool, 5), (X.gen(UK4S, "g_vib"), 6), (X.gen(US1S, "g_what"), 5), (X.gen(US1S, "g_pic", n=4), 4)]),
        ("How sound travels", [(X.gen(UK4S, "g_med"), 5), (X.gen(UK4S, "g_hear", n=6), 6), (X.gen(UK7S, "g_med"), 3), (X.gen(UK4S, "g_ear"), 4), (pool, 2)]),
        ("Pitch and loudness", [(X.gen(UK4P, "g_pitch"), 6), (X.gen(UK4P, "g_how"), 5), (X.gen(UK4P, "g_dist", n=4), 4), (X.gen(US1S, "g_loud"), 5)]),
        ("Echoes and noise", [(X.gen(UK7S, "g_echo", n=5), 5), (X.gen(UK7S, "g_range", n=5), 5), (X.gen(UK4P, "g_db", n=4), 4), (pool, 4), (X.gen(US1S, "g_stop"), 2)]),
        ("Sound investigations", [(X.B(UK4S, "B5"), 4), (X.B(UK4P, "B5"), 4), (X.B(US1S, "B5"), 4), (X.B(UK7S, "B5"), 4), (X.gen(UK4S, "g_speed", n=4), 4)]),
    ]


def gear_turns(R):
    from caon_sci import tq
    def f():
        a = R.choice([8, 10, 12, 15, 16, 20, 24, 30])
        k = R.choice([2, 3, 4])
        b = a * k
        if R.random() < 0.5:
            n = R.choice([1, 2, 3, 5])
            ans, w = n * k, [n, n + k, max(1, n * k - 1)]
            q = "A %d-tooth gear drives a %d-tooth gear. The big gear turns %d time%s. How many times does the small gear turn?" % (a, b, n, "" if n == 1 else "s")
            e = "Each turn of the big gear moves %d teeth, which is %d turns of the small gear. %d × %d = %d." % (b, k, n, k, n * k)
        else:
            n = k * R.choice([1, 2, 3])
            ans, w = n // k, [n, n * k, n + k]
            q = "A %d-tooth gear drives a %d-tooth gear. The small gear turns %d times. How many times does the big gear turn?" % (a, b, n)
            e = "The big gear has %d times as many teeth, so it turns %d times more slowly. %d ÷ %d = %d." % (k, k, n, k, n // k)
        unit = lambda x: "%d turn%s" % (x, "" if x == 1 else "s")
        w = [unit(x) for x in w if x != ans]
        if len(set(w)) < 3:
            return None
        return tq(q, unit(ans), w[:3], e)
    return f


def gear_dir(R):
    from caon_sci import tq
    def f():
        k = R.choice([2, 3, 4, 5])
        first = R.choice(["clockwise", "counterclockwise"])
        other = "counterclockwise" if first == "clockwise" else "clockwise"
        last = first if k % 2 == 1 else other
        names = "ABCDE"[:k]
        q = "%d gears are meshed in a row: %s. Gear A turns %s. Which way does gear %s turn?" % (k, " → ".join(names), first, names[-1])
        e = "Each meshed gear turns the opposite way to the one before it. With %d gears, gear %s turns %s." % (k, names[-1], last)
        return tq(q, last, ["it does not turn", "back and forth", ("clockwise" if last == "counterclockwise" else "counterclockwise")], e)
    return f


def s_machines(X):
    pool = X.pool([
        ("What is a pulley?", "a wheel with a groove that a rope runs over", ["a wheel with teeth", "a flat board on a pivot", "a sloping surface"], "Pulleys help lift loads."),
        ("A flag is raised by pulling down on a rope. Which machine is at the top of the pole?", "a fixed pulley", ["a gear", "a lever", "a screw"], "A fixed pulley changes the direction of the force."),
        ("What does a single fixed pulley do?", "It changes the direction of the force.", ["It makes the load lighter.", "It makes the rope longer.", "It speeds up time."], "You pull down to lift up."),
        ("Why do cranes use several pulleys together?", "so a smaller force can lift a heavy load", ["so the load is lighter", "so the rope is shorter", "so the crane is quieter"], "More pulleys share the load, but you pull more rope."),
        ("What is a gear?", "a wheel with teeth", ["a wheel with a groove", "a rope and hook", "a ramp"], "Gear teeth fit together."),
        ("Two gears are meshed. The first turns clockwise. Which way does the second turn?", "counterclockwise", ["clockwise", "it does not turn", "up and down"], "Meshed gears turn in opposite directions."),
        ("A small gear with 10 teeth drives a big gear with 30 teeth. How do they compare?", "The big gear turns more slowly.", ["The big gear turns faster.", "Both turn at the same speed.", "The big gear turns backward and faster."], "The small gear turns 3 times for each turn of the big gear."),
        ("On a bike, what links the pedal gear to the back-wheel gear?", "a chain", ["a pulley", "a lever", "a spring"], "Gears linked by a chain turn the same way."),
        ("Which machine uses gears?", "a hand egg beater", ["a flagpole", "a ramp", "a seesaw"], "Turning the handle turns gears that spin the beaters."),
        ("What is a mechanism?", "a set of moving parts that work together to do a job", ["one single nail", "a kind of energy", "a type of rock"], "Gears, pulleys and levers can make mechanisms."),
        ("What is a load in a machine?", "the object being moved or lifted", ["the force you use", "the pivot point", "the rope only"], "The effort moves the load."),
        ("A pulley system makes lifting easier. What is the trade-off?", "You have to pull more rope.", ["The load gets heavier.", "You need no force.", "The load moves faster."], "Machines trade force for distance."),
        ("Why do some gear systems use a very big gear driven by a tiny gear?", "to make the big gear turn with more force", ["to make the big gear spin faster", "to stop all movement", "to save rope"], "A slow big gear turns with more force."),
        ("Which is an example of a pulley in daily life?", "window blinds pulled up with a cord", ["a doorknob", "scissors", "a nail"], "The cord runs over small pulleys."),
        ("What is friction's effect in a machine?", "It slows moving parts and wastes some energy as heat.", ["It makes parts lighter.", "It adds energy.", "It has no effect."], "Oil reduces friction."),
        ("Why do people oil the gears of a bike?", "to reduce friction so they turn easily", ["to make them heavier", "to make them rust", "to change their colour"], "Less friction, less wear."),
        ("Gear A has 20 teeth and gear B has 10 teeth. Gear A turns once. How many times does gear B turn?", "2 times", ["1 time", "10 times", "half a time"], "20 ÷ 10 = 2."),
        ("Gear A has 12 teeth and gear B has 36 teeth. Gear B turns once. How many times does gear A turn?", "3 times", ["1 time", "12 times", "one third of a time"], "36 ÷ 12 = 3."),
        ("Three gears are in a row: A → B → C. A turns clockwise. Which way does C turn?", "clockwise", ["counterclockwise", "it does not turn", "back and forth"], "Each meshed gear reverses direction: A clockwise, B counterclockwise, C clockwise."),
        ("What is a movable pulley?", "a pulley attached to the load that moves up with it", ["a pulley fixed to a ceiling", "a gear on a bike", "a lever with no pivot"], "A movable pulley halves the force needed."),
        ("Which simple machine is a wheel with a rope that can be fixed or movable?", "pulley", ["wedge", "screw", "inclined plane"], "Pulleys can be fixed or movable."),
        ("A water well has a crank and a rope around a drum. Which machine is this?", "a wheel and axle", ["a gear only", "a wedge", "an inclined plane"], "Turning the crank winds the rope."),
        ("Why does an elevator use a motor and pulleys?", "to lift heavy loads with less effort", ["to make the elevator lighter", "to cool the building", "to make light"], "Machines make work easier."),
        ("Which tool uses a pulley to lift heavy car engines in a garage?", "an engine hoist (chain block)", ["a screwdriver", "a wrench", "a jack-o'-lantern"], "Chain blocks use several pulleys."),
        ("Why does a sailboat use pulleys on its ropes?", "so sailors can pull the sails with less force", ["so the boat floats", "so the wind stops", "so the ropes are shorter"], "Pulley blocks make the work easier."),
        ("Which machine part transfers turning motion from one shaft to another?", "a gear", ["a pulley rope", "a wedge", "a nail"], "Gears pass turning motion along."),
        ("A clock has many gears. Why?", "so the hands turn at different speeds", ["to make the clock heavier", "to make light", "to make sound louder"], "Gears of different sizes turn at different speeds."),
        ("A bike rider changes to a bigger back gear to climb a hill. What happens?", "Pedalling is easier but the bike goes slower.", ["Pedalling is harder and faster.", "The bike cannot move.", "Nothing changes."], "Gears trade speed for force."),
        ("What is the effort in a pulley system?", "the force you pull with", ["the object lifted", "the wheel", "the ceiling"], "Effort is the force that makes the machine work."),
        ("Which is a safety rule when using machines with gears?", "keep fingers and loose clothing away from moving gears", ["touch the teeth while they turn", "remove all guards", "run the machine without checking it"], "Moving gears can pinch."),
        ("What happens to the speed of a load lifted with many pulleys?", "It rises more slowly because you pull more rope.", ["It rises faster.", "It does not move.", "It falls."], "Force is reduced, distance is increased."),
        ("Which simple machine is made of a rope over a grooved wheel?", "a pulley", ["a gear", "a lever", "a screw"], "That is the definition of a pulley."),
        ("Which pair of gears would turn the slowest output gear?", "a 10-tooth gear driving a 40-tooth gear", ["a 40-tooth gear driving a 10-tooth gear", "two 20-tooth gears", "a 30-tooth gear driving a 15-tooth gear"], "The bigger the driven gear compared with the driver, the slower it turns."),
        ("Why do conveyor belts in a factory use pulleys?", "the belt runs over pulleys that keep it moving", ["to stop the belt", "to make the belt heavier", "to keep the belt cold"], "Belts and pulleys move objects."),
        ("Which design change would make a gear train turn its last gear faster?", "make the last gear smaller", ["make the last gear bigger", "remove its teeth", "add sand to the gears"], "A smaller driven gear turns faster."),
        ("A lever has a pivot, a load and an effort. Which part does a lever turn around?", "the pivot (fulcrum)", ["the load", "the effort", "the handle"], "The pivot is the turning point."),
        ("Why is it easier to open a paint can with a long screwdriver than with a coin?", "The longer lever needs less effort.", ["The coin is heavier.", "The screwdriver is sharper.", "Coins are magnetic."], "A longer lever arm means less effort."),
        ("Which everyday object is a lever?", "a seesaw", ["a flagpole pulley", "a bike chain", "a ramp"], "A seesaw turns on a pivot."),
        ("To make a seesaw balance with a heavier child, where should the heavier child sit?", "closer to the pivot", ["further from the pivot", "on the pivot", "it does not matter"], "Moving closer reduces their turning effect."),
        ("Which machine changes a small turning force at the handle into a big force at the axle?", "a wheel and axle, like a doorknob", ["a single fixed pulley", "a nail", "a rope"], "The big wheel makes turning easier."),
        ("Which mechanism changes turning motion into up-and-down motion in a toy?", "a cam", ["a pulley rope", "a lever with no pivot", "a magnet"], "Cams are used in moving toys."),
        ("Why do car engines use belts and pulleys?", "to turn other parts, like the fan, with the engine's motion", ["to make the car lighter", "to steer the car", "to stop the tires"], "Belts carry motion between pulleys."),
        ("Which design makes the effort smaller in a pulley system?", "using more pulleys and more rope sections to hold the load", ["using fewer pulleys", "using a shorter rope", "tying the rope to the load only"], "More supporting ropes share the load."),
        ("Which design would make a model crane lift a heavier load?", "add a second pulley to share the load", ["use a thinner string", "remove the pulley", "make the arm out of paper"], "More pulleys reduce the force needed."),
    ])
    gt, gd = X.f(gear_turns), X.f(gear_dir)
    return [
        ("Pulleys", [(pool, 12), (X.B(UK5M, "B1", n=4, drop=[r"\d N\b"]), 4), (X.gen(UK5M, "g_mech", n=2), 2), (gd, 2), (gt, 1)]),
        ("Gears", [(gt, 6), (gd, 4), (X.gen(UK5M, "g_gear"), 7), (pool, 3), (X.B(UK5M, "B1", n=2, drop=[r"\d N\b"]), 1)]),
        ("Levers and other machines", [(pool, 10), (X.gen(UK5M, "g_mech", n=4), 4), (gt, 4), (gd, 2)]),
        ("Machines in daily life", [(pool, 8), (X.gen(UK5M, "g_mech", n=6), 6), (X.gen(UK5M, "g_gear", n=4), 4), (X.B(UK5M, "B1", drop=[r"\d N\b"]), 2), (gt, 1)]),
        ("Designing mechanisms", [(X.B(UK5M, "B5", drop=[r"\d N\b"]), 5), (pool, 7), (gt, 6), (gd, 1), (X.gen(UK5M, "g_gear", n=2), 2)]),
    ]


def s_rocks(X):
    pool = X.pool([
        ("What is a mineral?", "a natural, non-living solid that rocks are made of", ["a kind of plant", "a melted metal made in a factory", "a living crystal"], "Rocks are made of one or more minerals."),
        ("Which mineral is the softest on the Mohs scale?", "talc", ["diamond", "quartz", "topaz"], "Talc can be scratched with a fingernail."),
        ("Which mineral is the hardest?", "diamond", ["talc", "gypsum", "calcite"], "Diamond is 10 on the Mohs scale."),
        ("A mineral scratches glass. What does this tell you?", "It is harder than glass.", ["It is softer than glass.", "It is a metal.", "It is magnetic."], "A harder mineral scratches a softer one."),
        ("What is the streak of a mineral?", "the colour of its powder when rubbed on a tile", ["its outside colour", "how shiny it is", "its shape"], "Streak can differ from the outside colour."),
        ("What is lustre?", "how a mineral shines in light", ["how hard it is", "its streak colour", "its weight"], "Lustre can be metallic, glassy or dull."),
        ("Which kind of rock forms when magma or lava cools?", "igneous", ["sedimentary", "metamorphic", "fossil rock"], "Granite and basalt are igneous."),
        ("Which kind of rock forms from layers of sand and mud pressed together?", "sedimentary", ["igneous", "metamorphic", "volcanic"], "Sandstone and shale are sedimentary."),
        ("Which kind of rock forms when heat and pressure change other rocks?", "metamorphic", ["sedimentary", "igneous", "soil"], "Marble and slate are metamorphic."),
        ("Which rock is most likely to contain fossils?", "limestone (sedimentary)", ["granite (igneous)", "basalt (igneous)", "obsidian (igneous)"], "Fossils form in sediment layers."),
        ("The Canadian Shield covers much of northern Ontario. What is it mostly made of?", "very old igneous and metamorphic rock", ["sand dunes", "ice only", "fresh lava"], "It is some of the oldest rock on Earth."),
        ("Which mineral is mined in Sudbury, Ontario?", "nickel ore", ["salt only", "diamonds only", "chalk"], "Sudbury is famous for nickel mining."),
        ("Which is a use of granite?", "kitchen countertops and building stone", ["pencil 'lead'", "baby powder", "table salt"], "Granite is hard and strong."),
        ("Pencil 'lead' is made from which mineral?", "graphite", ["quartz", "salt", "iron"], "Graphite is soft and leaves a grey streak."),
        ("Why must mines be cleaned up after they close?", "to protect water, soil and wildlife from pollution", ["to make more rocks", "to warm the ground", "to stop erosion of the Moon"], "Mining can harm the environment."),
        ("Which tool helps test a mineral's hardness?", "a steel nail and a glass plate", ["a thermometer", "a magnifying glass only", "a ruler"], "Scratch tests compare hardness."),
        ("A rock has shiny crystals you can see. Which type is it most likely to be?", "igneous (like granite)", ["sedimentary (like shale)", "soil", "chalk"], "Slow cooling makes big crystals."),
        ("Quartz is 7 on the Mohs scale and calcite is 3. Which one can scratch the other?", "Quartz can scratch calcite.", ["Calcite can scratch quartz.", "Neither can scratch the other.", "Both scratch each other equally."], "The higher number is harder."),
        ("Gypsum is 2 on the Mohs scale. Can a fingernail (about 2.5) scratch it?", "Yes, because the fingernail is harder.", ["No, gypsum is harder.", "No, nothing can scratch gypsum.", "Only if it is wet."], "A harder object scratches a softer one."),
        ("Pyrite is gold-coloured but leaves a greenish-black streak. Why is streak useful?", "Streak can tell apart minerals that look alike.", ["Streak shows how heavy a mineral is.", "Streak is always the same as the outside colour.", "Streak shows the mineral's age."], "Pyrite is called fool's gold."),
        ("Which mineral is found in table salt?", "halite", ["quartz", "talc", "graphite"], "Halite is rock salt."),
        ("Which describes basalt?", "a dark igneous rock from cooled lava", ["a soft rock made of shells", "a metamorphic rock from limestone", "a rock made of sand grains"], "Basalt forms from lava."),
        ("Limestone is changed by heat and pressure. What rock does it become?", "marble", ["granite", "sandstone", "basalt"], "Marble is metamorphic."),
        ("Shale is changed by heat and pressure. What rock does it become?", "slate", ["granite", "marble", "pumice"], "Slate is metamorphic."),
        ("Which rock floats on water because it is full of gas bubbles?", "pumice", ["granite", "marble", "slate"], "Pumice forms from frothy lava."),
        ("Which property describes how a mineral breaks along flat surfaces?", "cleavage", ["lustre", "streak", "hardness"], "Mica splits into thin flat sheets."),
        ("Why is copper used in electrical wires?", "It conducts electricity well and bends easily.", ["It is the hardest mineral.", "It is see-through.", "It floats."], "Uses depend on properties."),
        ("Which property can a magnet test in minerals?", "whether the mineral contains iron (magnetite)", ["its lustre", "its streak", "its hardness"], "Magnetite is magnetic."),
    ])
    return [
        ("Rocks and minerals", [(pool, 6), (X.gen(UK3R, "g_type"), 8), (X.gen(UK3R, "g_look"), 6)]),
        ("Properties of minerals", [(pool, 8), (X.gen(UK3R, "g_test"), 8), (X.gen(UK3R, "g_how"), 4)]),
        ("How rocks form", [(X.gen(UK3R, "g_type", n=4), 4), (X.gen(UK3F, "g_isfos", n=6), 6), (pool, 4), (X.gen(US4R, "g_env", n=6), 6)]),
        ("Uses of rocks and minerals", [(X.gen(UK3R, "g_use"), 7), (X.gen(UK3R, "g_man"), 7), (pool, 4), (X.B(UK3R, "B1"), 2)]),
        ("Rock layers and investigations", [(X.gen(US4R, "g_oldest", n=6), 6), (X.gen(US4R, "g_change", n=4), 4), (X.B(UK3R, "B5"), 4), (X.B(UK3F, "B5"), 3), (X.B(US4R, "B5"), 3)]),
    ]


def s_erosion(X):
    pool = X.pool([
        ("What is weathering?", "the breaking down of rock into smaller pieces", ["moving pieces of rock away", "dropping sediment in a new place", "melting rock into lava"], "Weathering breaks; erosion moves."),
        ("What is erosion?", "the moving of soil and rock pieces by water, wind or ice", ["the breaking of rock in place only", "the cooling of lava", "the growth of crystals"], "Erosion carries sediment away."),
        ("Water seeps into a crack in a rock and freezes. What happens?", "The ice expands and breaks the rock (freeze-thaw).", ["The rock melts.", "The rock grows bigger.", "Nothing happens."], "Ontario winters cause a lot of freeze-thaw weathering."),
        ("Why do potholes appear on Ontario roads in spring?", "Water freezes and thaws in cracks, breaking the road.", ["Snowplows dig them.", "The Sun melts the asphalt.", "Rain is acidic only in spring."], "Freeze-thaw weathering breaks up roads."),
        ("How did the Great Lakes form?", "Huge glaciers carved out the land, then melted.", ["A volcano erupted.", "People dug them.", "Wind blew the sand away."], "Ice is a powerful agent of erosion."),
        ("Niagara Falls moves slowly back upstream over time. Why?", "Water erodes the soft rock under the hard top layer.", ["The falls are pushed by wind.", "People move the rocks.", "Ice adds rock each year."], "Erosion changes landforms."),
        ("Plant roots grow into cracks in rocks. What kind of weathering is this?", "weathering by living things", ["erosion by wind", "deposition", "melting"], "Roots can split rocks."),
        ("Which helps stop soil erosion on a hillside?", "planting grass and trees", ["removing all the plants", "pouring water down it", "driving trucks on it"], "Roots hold soil in place."),
        ("What is deposition?", "dropping eroded sediment in a new place", ["breaking rock", "lifting rock", "melting ice"], "Rivers drop sand where they slow down."),
        ("Where does a river drop most of its sediment?", "where it slows down, like at its mouth", ["where it flows fastest", "at the top of a waterfall", "nowhere"], "Slow water cannot carry as much."),
        ("Which change happens very quickly?", "a landslide", ["a river carving a valley", "a glacier wearing down a mountain", "wind smoothing a rock"], "Some changes take seconds, others take millions of years."),
        ("Why do farmers plant rows of trees between fields?", "to slow the wind and reduce soil erosion", ["to make the fields colder", "to attract more wind", "to stop rain"], "Windbreaks protect soil."),
        ("Ocean waves crash against a rocky shore. What happens to the rocks over time?", "They are broken and smoothed into pebbles and sand.", ["They grow bigger.", "They turn into lava.", "They become fossils right away."], "Waves are an agent of erosion."),
        ("What carried the large boulders found in fields across Ontario?", "glaciers during the last ice age", ["rivers in one day", "strong winds", "people with trucks"], "Glaciers moved and dropped huge rocks."),
        ("A river bank is wearing away near a farm. Which solution would help most?", "plant shrubs and trees along the bank", ["remove the plants on the bank", "dig the bank steeper", "drive tractors on the bank"], "Roots hold soil."),
        ("Which is chemical weathering?", "acid rain slowly dissolving limestone", ["ice splitting a rock", "roots cracking a sidewalk", "waves breaking a cliff"], "Chemicals change the rock itself."),
        ("Why do rocks in a fast river become smooth and round?", "They bump and rub against each other as the water carries them.", ["The Sun melts their edges.", "Fish polish them.", "They grow new layers."], "Moving water erodes rock."),
        ("Which change to the land takes the longest?", "a river carving a deep valley", ["an earthquake", "a flood", "a landslide"], "River valleys form over thousands of years."),
        ("What is a glacier?", "a huge, slow-moving body of ice", ["a fast river", "a sand dune", "a kind of volcano"], "Glaciers erode the land as they move."),
        ("Why are retaining walls built on steep slopes?", "to hold soil and rock in place", ["to speed up erosion", "to make the slope steeper", "to catch rainwater for drinking"], "Walls reduce landslides."),
        ("A farmer leaves bare soil all winter. What can happen in spring?", "Melting snow and rain wash the soil away.", ["The soil gets deeper.", "Nothing happens.", "The soil turns into rock."], "Cover crops protect soil."),
        ("Which agent of erosion shaped the sand dunes at Sandbanks Provincial Park?", "wind", ["lava", "earthquakes", "people only"], "Wind moves sand into dunes."),
    ])
    return [
        ("Weathering", [(pool, 6), (X.gen(AU5W, "g_proc", n=8), 8), (X.B(AU5W, "POOL1"), 4), (X.gen(US2E, "g_source"), 2)]),
        ("Erosion and deposition", [(X.gen(AU5W, "g_agent", n=8), 8), (pool, 6), (X.gen(AU5W, "g_land"), 4), (X.gen(AU5W, "g_order"), 2)]),
        ("Fast and slow changes", [(X.gen(US2E, "g_speed", n=7), 7), (X.gen(US2E, "g_which", n=6), 6), (X.gen(US2E, "g_pic"), 4), (pool, 3)]),
        ("Protecting land", [(pool, 6), (X.gen(US2E, "g_source", n=4), 4), (X.B(US2E, "B1"), 5), (X.B(AU5W, "POOL5"), 5)]),
        ("Erosion investigations", [(X.B(US2E, "B5"), 4), (X.gen(AU5W, "g_proc", n=4), 4), (X.gen(AU5W, "g_agent", n=4), 4), (pool, 4), (X.B(AU5W, "POOL1"), 4)]),
    ]


L = "<p><b>%s</b></p><ul>%s</ul>"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def UNITS():
    return [
        CU("B", 1, "habitats-and-communities", "B1.1, B2.1, B2.2, B2.3",
           "Describe habitats as places that give plants and animals food, water, shelter and space; identify living and non-living "
           "parts of a habitat; describe populations and communities in local Ontario habitats.",
           "Habitats and Communities", "Habitats and communities",
           "Free Grade 4 science worksheets on habitats, living and non-living things, populations and communities in Ontario forests, "
           "wetlands and lakes. 100 questions with answers.",
           "A habitat meets a living thing's needs.", "Food, water, shelter and space; many populations together make a community.",
           L % ("A habitat is the place where a plant or animal lives and finds what it needs.", ul(
               "Animals need food, water, shelter and space. Plants need sunlight, water, air, nutrients and space.",
               "A habitat has living parts (plants, animals, fungi) and non-living parts (water, rocks, soil, air, sunlight).",
               "A population is all of one kind of living thing in an area. A community is all the populations living together.",
               "Ontario habitats include the boreal forest, mixed forests, wetlands, lakes, rivers and meadows.")),
           [("A beaver lives in a pond. Name its needs that the pond meets.", ["food: tree bark and pond plants", "water: the pond", "shelter: its lodge"], "food, water, shelter and space"),
            ("All the frogs in a marsh are a …", ["one kind of animal in one place"], "population")],
           ["Mixing up population (one kind) and community (all kinds).", "Thinking water, rocks and sunlight are living because they help living things.",
            "Thinking any animal can live in any habitat."],
           [("What is the difference between a habitat and a community?", "A habitat is the place. A community is all the living things that live in that place together."),
            ("What are the needs of animals?", "Animals need food, water, shelter and space. Plants also need sunlight and air."),
            ("What habitats are found in Ontario?", "Ontario has boreal forest in the north, mixed and deciduous forests in the south, and many lakes, rivers and wetlands.")],
           s_habitats),
        CU("B", 2, "food-chains-and-food-webs", "B2.4, B2.5",
           "Classify organisms as producers, consumers or decomposers; describe food chains and food webs in Ontario habitats and how "
           "a change to one population affects others.",
           "Food Chains and Food Webs", "Food chains and food webs",
           "Free Grade 4 science worksheets on producers, consumers, decomposers, food chains and food webs, with Ontario forest and "
           "pond examples. 100 questions with answers.",
           "Energy flows from the Sun to plants to animals.", "Producers make food; consumers eat; decomposers break down dead things.",
           L % ("A food chain shows who eats whom. The arrows point from the food to the eater.", ul(
               "Producers (plants and algae) make their own food using sunlight.",
               "Consumers eat other living things: herbivores eat plants, carnivores eat animals, omnivores eat both.",
               "Decomposers (fungi, bacteria, worms) break down dead things and return nutrients to the soil.",
               "A food web is many linked food chains. If one population changes, others change too.")),
           [("Grass → hare → lynx. Which is the producer?", ["the grass makes its own food"], "grass"),
            ("If the hares disappear, what happens to the lynx?", ["lynx eat hares", "less food"], "the lynx population falls")],
           ["Drawing the arrows backwards (the arrow points to the eater).", "Thinking decomposers are not important.",
            "Thinking a change to one animal affects only that animal."],
           [("Why do food chains start with a plant?", "Plants are producers. They capture energy from the Sun and make food, so all the energy in the chain starts with them."),
            ("What is the difference between a food chain and a food web?", "A food chain is one path of energy. A food web shows many food chains linked together."),
            ("Why are decomposers important?", "They break down dead plants and animals and return nutrients to the soil so new plants can grow.")],
           s_food),
        CU("B", 3, "adaptations-and-human-impact", "B1.1, B1.2, B2.6, B2.7",
           "Describe adaptations that help plants and animals survive in their habitats; assess the effects of human activities on "
           "habitats and ways to protect them, including Indigenous approaches to caring for the land.",
           "Adaptations and Human Impact", "Adaptations and human impact",
           "Free Grade 4 science worksheets on animal adaptations, habitat change, invasive species and protecting Ontario habitats. "
           "100 questions with answers.",
           "Adaptations help living things survive.", "People can harm habitats, but we can also protect and restore them.",
           L % ("An adaptation is a body part or behaviour that helps a living thing survive.", ul(
               "Structural adaptations: thick fur, webbed feet, quills, a beaver's flat tail.",
               "Behavioural adaptations: migration, hibernation, hunting at night.",
               "Habitat loss, pollution and invasive species (like zebra mussels) harm communities.",
               "Parks, wildlife crossings, cleanups and taking only what we need help protect habitats.")),
           [("Why does a snowshoe hare turn white in winter?", ["it blends in with snow"], "camouflage from predators"),
            ("Is migration a structural or behavioural adaptation?", ["it is something the animal does"], "behavioural")],
           ["Thinking an animal changes on purpose when its habitat changes.", "Mixing up migration and hibernation.",
            "Thinking all changes to habitats are caused by people."],
           [("What is the difference between structural and behavioural adaptations?", "Structural adaptations are body parts, like quills. Behavioural adaptations are things animals do, like migrating."),
            ("What is an invasive species?", "A living thing brought to a new place where it spreads and harms local species, like zebra mussels in the Great Lakes."),
            ("How can people protect habitats?", "By keeping water clean, saving natural areas, building wildlife crossings and taking only what is needed.")],
           s_adapt),
        CU("C", 4, "light", "C2.1, C2.2, C2.3, C2.4",
           "Identify natural and artificial sources of light; describe how light travels in straight lines and is reflected, absorbed "
           "or transmitted by materials; describe uses and effects of light technologies.",
           "Light", "Light",
           "Free Grade 4 science worksheets on light sources, transparent, translucent and opaque materials, shadows, reflection and "
           "refraction. 100 questions with answers.",
           "Light travels in straight lines.", "Materials let light through, let some through or block it; shiny surfaces reflect it.",
           L % ("Light is a form of energy that travels in straight lines.", ul(
               "Natural light sources: the Sun, stars, lightning, fireflies. Artificial sources: bulbs, flashlights, candles.",
               "Transparent materials let light through; translucent let some through; opaque block it and make shadows.",
               "Light reflects (bounces) off shiny surfaces and refracts (bends) when it moves into water or glass.",
               "The Moon is not a light source: it reflects sunlight.")),
           [("Is wax paper transparent, translucent or opaque?", ["some light passes through", "you cannot see clearly through it"], "translucent"),
            ("Why does a shadow form?", ["light travels in straight lines", "an opaque object blocks it"], "the object blocks the light")],
           ["Thinking the Moon makes its own light.", "Thinking shiny objects like mirrors are light sources.", "Mixing up translucent and transparent."],
           [("What is the difference between reflection and refraction?", "Reflection is light bouncing off a surface. Refraction is light bending as it passes into a different material."),
            ("Why do we see objects?", "Light from a source reflects off the object and travels in a straight line into our eyes."),
            ("How can light be harmful?", "Looking at the Sun can damage eyes, and too much artificial light at night can confuse birds and insects.")],
           s_light),
        CU("C", 5, "sound", "C2.5, C2.6, C2.7",
           "Describe how sound is made by vibrations and travels through solids, liquids and gases; describe pitch and loudness; "
           "assess the effects of noise and technologies that protect or improve hearing.",
           "Sound", "Sound",
           "Free Grade 4 science worksheets on vibrations, how sound travels, pitch, loudness, echoes and noise pollution. "
           "100 questions with answers.",
           "Sound is made by vibrations.", "Fast vibrations give a high pitch; big vibrations give a loud sound.",
           L % ("Every sound comes from something vibrating (moving back and forth quickly).", ul(
               "Sound travels through solids, liquids and gases, but not through empty space.",
               "Pitch is how high or low a sound is. Faster vibrations make a higher pitch.",
               "Loudness depends on the size of the vibrations. Very loud sounds can damage hearing.",
               "An echo is sound reflected off a surface. Soft materials absorb sound.")),
           [("A ruler is twanged on a desk. It is made shorter. What happens to the pitch?", ["shorter part vibrates faster"], "higher pitch"),
            ("Can sound travel in space?", ["sound needs particles to vibrate"], "no")],
           ["Mixing up pitch and loudness.", "Thinking sound travels best through air (it travels faster in solids).", "Thinking sound can travel through empty space."],
           [("What is the difference between pitch and loudness?", "Pitch is how high or low a sound is. Loudness is how strong or quiet it is."),
            ("Why does sound travel faster in water than in air?", "The particles in liquids are closer together, so vibrations pass along more quickly."),
            ("How can we reduce noise pollution?", "With noise barriers, soft materials that absorb sound, quieter machines and ear protection.")],
           s_sound),
        CU("D", 6, "pulleys-and-gears", "D2.1, D2.2, D2.3, D2.4",
           "Describe how pulleys and gears change the direction, speed or force of movement; identify mechanisms in everyday machines; "
           "design and build a mechanism that uses pulleys or gears.",
           "Pulleys and Gears", "Pulleys and gears",
           "Free Grade 4 science worksheets on pulleys, gears, gear ratios, levers and mechanisms in everyday machines. "
           "100 questions with answers.",
           "Pulleys and gears change movement.", "Meshed gears turn opposite ways; small gears turn faster than big ones.",
           L % ("Machines make work easier by changing the size, direction or speed of a force.", ul(
               "A pulley is a grooved wheel with a rope. A fixed pulley changes the direction of the force.",
               "Several pulleys together let a small force lift a heavy load, but you pull more rope.",
               "Gears are wheels with teeth. Meshed gears turn in opposite directions.",
               "A small gear turns faster than the big gear it drives; gears joined by a chain turn the same way.")),
           [("Gear A has 10 teeth and drives gear B with 20 teeth. B turns once. How many turns does A make?", ["20 ÷ 10 = 2"], "2 turns"),
            ("Why does a flagpole use a pulley?", ["pulling down lifts the flag up"], "it changes the direction of the force")],
           ["Thinking a single fixed pulley makes the load lighter.", "Thinking meshed gears turn the same way.",
            "Thinking a big gear driven by a small gear turns faster."],
           [("How does a pulley help?", "A fixed pulley lets you pull down to lift up. Several pulleys together reduce the force needed."),
            ("How do gears change speed?", "When a small gear drives a big gear, the big gear turns more slowly but with more force."),
            ("Where are gears and pulleys used?", "In bikes, clocks, egg beaters, cranes, elevators, window blinds and flagpoles.")],
           s_machines),
        CU("E", 7, "rocks-and-minerals", "E2.1, E2.2, E2.3, E1.2",
           "Describe the properties of minerals (hardness, colour, streak, lustre); identify igneous, sedimentary and metamorphic rocks "
           "and how they form; describe uses of rocks and minerals and the effects of mining in Ontario.",
           "Rocks and Minerals", "Rocks and minerals",
           "Free Grade 4 science worksheets on minerals, the Mohs hardness scale, streak and lustre, igneous, sedimentary and "
           "metamorphic rocks and their uses. 100 questions with answers.",
           "Rocks are made of minerals.", "Igneous rocks cool from magma; sedimentary rocks form in layers; metamorphic rocks are changed by heat and pressure.",
           L % ("Rocks are made of one or more minerals. Minerals are natural, non-living solids.", ul(
               "Minerals are identified by hardness (Mohs scale, talc 1 to diamond 10), colour, streak and lustre.",
               "Igneous rocks form when magma or lava cools (granite, basalt).",
               "Sedimentary rocks form from layers of sediment pressed together (sandstone, limestone) and may hold fossils.",
               "Metamorphic rocks form when heat and pressure change rocks (marble, slate).")),
           [("A mineral scratches quartz. What do you know?", ["harder minerals scratch softer ones"], "it is harder than quartz"),
            ("Which rock type might have fossils?", ["fossils form in sediment layers"], "sedimentary")],
           ["Thinking a mineral's outside colour always matches its streak.", "Mixing up rocks and minerals.",
            "Thinking fossils are found in igneous rocks."],
           [("What is the difference between a rock and a mineral?", "A mineral is one natural solid substance. A rock is made of one or more minerals."),
            ("How do we test the hardness of a mineral?", "Try to scratch it with objects of known hardness, such as a fingernail, a copper coin, a steel nail and glass."),
            ("Why is mining important in Ontario?", "Ontario mines nickel, gold and other minerals used in batteries, coins and buildings. Mines must be cleaned up to protect the land.")],
           s_rocks),
        CU("E", 8, "weathering-and-erosion", "E2.4, E2.5, E1.1",
           "Describe how weathering and erosion by water, wind, ice and living things change the land; identify slow and fast changes "
           "to landforms; assess ways to reduce erosion.",
           "Weathering and Erosion", "Weathering and erosion",
           "Free Grade 4 science worksheets on weathering, erosion, deposition, freeze-thaw, glaciers and protecting land in Ontario. "
           "100 questions with answers.",
           "Weathering breaks rock; erosion moves it.", "Water, wind, ice and living things shape the land, slowly or quickly.",
           L % ("Weathering breaks rocks into smaller pieces. Erosion carries the pieces away. Deposition drops them somewhere new.", ul(
               "Water freezing in cracks breaks rock (freeze-thaw), which is common in Ontario winters.",
               "Plant roots and burrowing animals also break rock and soil.",
               "Glaciers carved the Great Lakes; rivers, waves and wind keep shaping the land.",
               "Plants, windbreaks and retaining walls help stop soil erosion.")),
           [("Water freezes in a crack in a rock. What happens?", ["ice takes up more space"], "the rock breaks"),
            ("Is a landslide a fast or slow change?", ["it happens in seconds"], "fast")],
           ["Mixing up weathering (breaking) and erosion (moving).", "Thinking erosion only happens by water.", "Thinking land never changes."],
           [("What is the difference between weathering and erosion?", "Weathering breaks rock down. Erosion moves the broken pieces to a new place."),
            ("How did glaciers change Ontario?", "Thick ice sheets scraped the land, carved valleys and lake basins and left behind rocks and sand when they melted."),
            ("How can we stop soil erosion?", "By planting trees and grass, building windbreaks and walls, and not removing plants from slopes.")],
           s_erosion),
    ]
