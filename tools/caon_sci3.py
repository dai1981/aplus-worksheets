# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 3 (B Growth and Changes in Plants, C Forces Causing Movement,
D Strong and Stable Structures, E Soils in the Environment). Built by caon_sci.build."""
from caon_sci import CU

UK3P, UK3N, UK3W, UK3F = ("gen_uk_science_y3_parts_of_a_flowering_plant", "gen_uk_science_y3_what_plants_need_to_grow",
                          "gen_uk_science_y3_how_water_moves_in_plants", "gen_uk_science_y3_flowers_pollination_and_seeds")
US5P, US4P, UK5R, SG5R = ("gen_us_science_g5_what_plants_need_to_grow", "gen_us_science_g4_plant_structures",
                          "gen_uk_science_y5_reproduction_in_plants_and_animals", "gen_sg_science_p5_reproduction_in_plants")
US2P, SG3L, US2W = "gen_us_science_g2_pollination_and_seed_dispersal", "gen_sg_science_p3_life_cycles_of_plants", "gen_us_science_g2_what_plants_need"
UK3S, UK3M, UK3G, UK5G, UK5F = ("gen_uk_science_y3_pushes_pulls_and_surfaces", "gen_uk_science_y3_magnets_attract_and_repel",
                                "gen_uk_science_y3_magnetic_materials", "gen_uk_science_y5_gravity", "gen_uk_science_y5_friction")
US3M, US3D, SG3M, US3S = ("gen_us_science_g3_patterns_of_motion", "gen_us_science_g3_designing_with_magnets", "gen_sg_science_p3_magnets",
                          "gen_us_science_g3_magnets_and_static_electricity")
US3F, US2B, USKS = "gen_us_science_g3_balanced_and_unbalanced_forces", "gen_us_science_g2_building_with_small_pieces", "gen_us_science_g2_choosing_materials"
UK3L, AU3S, US5D = "gen_uk_science_y3_soils", "gen_au_science_y3_soils_rocks_and_minerals", "gen_us_science_g5_decomposers_and_the_cycle_of_matter"
US2E = "gen_us_science_g2_stopping_wind_and_water_erosion"


def ul(*xs):
    return "".join("<li>%s</li>" % x for x in xs)


def L(lead, *xs):
    return "<p><b>%s</b></p><ul>%s</ul>" % (lead, ul(*xs))


def s_parts(X):
    pool = X.pool([
        ("What do plants need to grow?", "light, air, water, nutrients and space", ["only water", "only soil", "darkness and cold"], "Plants make food using light."),
        ("Which part of a plant takes in water from the soil?", "the roots", ["the flowers", "the leaves", "the fruit"], "Roots also hold the plant in place."),
        ("Which part of a plant makes food using sunlight?", "the leaves", ["the roots", "the seeds", "the stem only"], "Leaves are like tiny food factories."),
        ("What does the stem do?", "holds the plant up and carries water to the leaves", ["makes seeds", "takes in sunlight only", "attracts bees"], "The stem is like a pipe."),
        ("A plant is kept in a dark cupboard for two weeks. What happens?", "It turns pale and weak because it cannot make food.", ["It grows greener.", "It makes more flowers.", "Nothing changes."], "Plants need light to make food."),
        ("Why do farmers in Ontario add compost or fertilizer to fields?", "to give plants more nutrients", ["to make the soil colder", "to keep birds away", "to make the soil drier"], "Nutrients help plants grow."),
        ("Which plant part do we eat when we eat carrots?", "the root", ["the leaf", "the flower", "the seed"], "Carrots are roots."),
        ("Which plant part do we eat when we eat lettuce?", "the leaves", ["the roots", "the seeds", "the stem only"], "Lettuce is leaves."),
        ("Which plant part do we eat when we eat corn kernels?", "the seeds", ["the roots", "the leaves", "the flowers"], "Each kernel is a seed."),
        ("Which plant part do we eat when we eat broccoli?", "the flower buds", ["the roots", "the seeds only", "the bark"], "Broccoli is a bunch of tiny flower buds."),
        ("Why do plants on a windowsill lean toward the window?", "They grow toward the light.", ["They are falling over.", "They need cold air.", "They are trying to get water from the glass."], "Plants respond to light."),
        ("Why do maple trees lose their leaves in the fall?", "to save water and energy during the cold winter", ["because they are dying", "because animals eat them all", "because the roots stop growing forever"], "Deciduous trees rest in winter."),
    ])
    return [
        ("Parts of a plant", [(X.gen(UK3P, "g_job"), 6), (X.gen(UK3P, "g_pic", n=6), 6), (X.gen(US4P, "g_label", n=4), 4), (pool, 4)]),
        ("What plants need", [(X.gen(UK3N, "g_need"), 7), (X.gen(UK3N, "g_what"), 5), (pool, 4), (X.gen(US2W, "g_what"), 4)]),
        ("How water moves in plants", [(X.gen(UK3W, "g_path"), 6), (X.gen(UK3W, "g_wilt"), 6), (X.gen(UK3W, "g_dye", n=5), 5), (pool, 3)]),
        ("Plants we eat", [(X.gen(UK3P, "g_food"), 8), (pool, 6), (X.gen(US4P, "g_struct_job", n=6), 6)]),
        ("Plant investigations", [(X.gen(UK3N, "g_test", n=5), 5), (X.gen(US5P, "g_height", n=4), 4), (X.gen(UK3W, "g_table", n=4), 4), (X.B(UK3N, "B5"), 4), (X.B(UK3W, "B5"), 3)]),
    ]


def s_cycle(X):
    pool = X.pool([
        ("What is the first stage in the life cycle of a flowering plant?", "a seed", ["a flower", "a fruit", "a tree"], "Seeds germinate and grow."),
        ("What is germination?", "when a seed starts to grow a root and shoot", ["when a flower opens", "when leaves fall off", "when fruit gets ripe"], "Seeds need water and warmth to germinate."),
        ("What is pollination?", "moving pollen from one flower to another", ["planting a seed", "watering a plant", "cutting a stem"], "Bees, butterflies and wind carry pollen."),
        ("Why do many flowers have bright petals and a sweet smell?", "to attract insects that carry pollen", ["to scare animals away", "to make shade", "to store water"], "Insects help pollinate."),
        ("How are maple seeds spread?", "They spin in the wind like helicopters.", ["Animals swallow them.", "They float on the ocean.", "They explode."], "Wind dispersal."),
        ("How are burdock seeds spread?", "Their hooks stick to animal fur and clothing.", ["The wind blows them.", "They float on water.", "Squirrels plant them on purpose."], "Burrs hitch a ride."),
        ("How do many berry seeds get spread?", "Birds eat the berries and drop the seeds far away.", ["The berries roll downhill.", "The seeds swim.", "People always plant them."], "Animals help plants spread."),
        ("Why is it useful for seeds to travel away from the parent plant?", "so the new plants have enough space, light and water", ["so they can stay in the shade", "so they get eaten", "so they never grow"], "Crowded plants compete."),
        ("Which part of a flower becomes the fruit?", "the ovary (the bottom of the pistil)", ["the petal", "the stem", "the root"], "Fruit protects the seeds."),
        ("What happens to a plant at the end of its life cycle?", "it makes seeds and then may die, and the cycle starts again", ["it turns into a rock", "it becomes an animal", "it stops being a plant"], "Life cycles repeat."),
        ("How long is the life cycle of a bean plant?", "a few months", ["a few minutes", "a hundred years", "one day"], "Beans grow quickly."),
        ("Which plant has a life cycle that can last hundreds of years?", "a white pine tree", ["a bean plant", "a sunflower", "a tomato plant"], "Some trees live for centuries."),
    ])
    return [
        ("Plant life cycles", [(X.gen(UK3F, "g_cycle", n=6), 6), (X.gen(SG3L, "g_stage"), 6), (pool, 5), (X.gen(SG3L, "g_parts"), 3)]),
        ("Germination", [(X.gen(SG3L, "g_germ"), 7), (X.gen(SG3L, "g_need"), 4), (X.gen(UK3N, "g_seed"), 4), (pool, 3), (X.gen(SG3L, "g_time"), 2)]),
        ("Flowers and pollination", [(X.gen(UK3F, "g_fpart"), 6), (X.gen(SG5R, "g_part", n=5), 5), (X.gen(US2P, "g_job"), 5), (X.gen(SG5R, "g_poll"), 4)]),
        ("Seed dispersal", [(X.gen(SG5R, "g_disp", n=6), 6), (X.gen(UK5R, "g_disp"), 5), (X.gen(US2P, "g_seed"), 5), (pool, 4)]),
        ("Life cycle investigations", [(X.gen(US2P, "g_test", n=5), 5), (X.gen(SG3L, "g_height"), 4), (X.B(UK3F, "B5"), 4), (X.B(SG3L, "B5"), 4), (X.B(US2P, "B5"), 3)]),
    ]


def s_people(X):
    pool = X.pool([
        ("Which is a way people use plants?", "for food, medicine, clothing and building materials", ["only for decoration", "only for fuel", "plants are not useful"], "Plants are very important to people."),
        ("Which tree's sap do Ontario farmers boil to make syrup?", "the sugar maple", ["the white pine", "the paper birch", "the red oak"], "It takes about 40 litres of sap to make 1 litre of syrup."),
        ("Which plants are known as the Three Sisters in many Indigenous traditions?", "corn, beans and squash", ["apples, pears and plums", "wheat, rice and oats", "roses, tulips and daisies"], "They help each other grow."),
        ("How do beans help corn and squash in a Three Sisters garden?", "Beans add nutrients to the soil.", ["Beans shade the corn.", "Beans scare away birds.", "Beans make the soil dry."], "Corn holds up the beans; squash shades the soil."),
        ("Why are trees important to the environment?", "They give oxygen, shade, habitat and hold the soil in place.", ["They make the air dirtier.", "They block all rain.", "They are only for wood."], "Trees help everyone."),
        ("Which item is made from plants?", "a cotton T-shirt", ["a glass jar", "a steel spoon", "a plastic toy"], "Cotton comes from cotton plants."),
        ("Which item is made from trees?", "paper", ["glass", "metal foil", "stone"], "Paper is made from wood pulp."),
        ("What can people do to protect plants in a park?", "stay on the paths and not pick wildflowers", ["pull up plants for fun", "throw garbage on the ground", "ride bikes over gardens"], "Respect natural areas."),
        ("Why are bees important to farmers?", "Bees pollinate many fruit and vegetable crops.", ["Bees eat all the weeds.", "Bees water the plants.", "Bees dig the soil."], "No pollination means fewer fruits."),
        ("What is an invasive plant?", "a plant from somewhere else that spreads quickly and crowds out local plants", ["a plant that lives inside a house", "a plant that is very small", "a plant that has no leaves"], "Garlic mustard is invasive in Ontario."),
        ("Which is a healthy way to grow food at school?", "plant a vegetable garden and compost food scraps", ["use lots of pesticides", "never water the plants", "keep the plants in the dark"], "Gardens teach about plant needs."),
        ("Why should you wash fruit from the store before eating it?", "to remove dirt and germs", ["to make it grow", "to change its colour", "to make it heavier"], "Clean food is safer."),
        ("Which plant can be used to make medicine?", "willow bark (used to make a pain reliever)", ["a plastic plant", "a stone", "a glass bead"], "Many medicines come from plants."),
        ("Why do some people plant native plants in their gardens?", "They need less water and support local insects and birds.", ["They grow only in deserts.", "They attract no animals.", "They need more fertilizer."], "Native plants suit the local climate."),
        ("How can people help plants after a forest fire?", "plant new trees and protect the area while it grows back", ["build parking lots", "remove all the soil", "dump garbage there"], "Replanting helps forests recover."),
        ("Which is a plant adaptation for living in a dry place?", "a cactus storing water in its thick stem", ["a water lily's floating leaves", "a maple's wide leaves", "a fern's love of shade"], "Adaptations help plants survive."),
    ])
    return [
        ("Plants and people", [(pool, 8), (X.gen(UK3P, "g_food", n=6), 6), (X.gen(UK3P, "g_tree"), 4), (X.B(UK3P, "B1"), 2)]),
        ("Plant adaptations", [(X.gen(US4P, "g_adapt", n=8), 8), (pool, 6), (X.gen(UK3P, "g_prob"), 6)]),
        ("Caring for plants", [(pool, 6), (X.gen(US2W, "g_data", n=5), 5), (X.gen(UK3N, "g_vary"), 3), (X.gen(UK3N, "g_amount"), 2), (X.gen(UK3N, "g_test", n=4), 4)]),
        ("Plants and the environment", [(pool, 6), (X.B(UK3N, "B1"), 4), (X.B(US2P, "B1"), 4), (X.B(UK3W, "B1"), 3), (X.gen(SG3L, "g_need", n=3), 3)]),
        ("Growing plants", [(X.gen(US5P, "g_height", n=4), 4), (X.gen(US5P, "g_willow"), 4), (X.B(US5P, "B5"), 4), (pool, 4), (X.gen(US2P, "g_model", n=4), 4), (X.gen(US5P, "g_hydro"), 2)]),
    ]


def s_forces(X):
    pool = X.pool([
        ("What is a force?", "a push or a pull", ["a kind of light", "a colour", "a sound"], "Forces make things move, stop or change direction."),
        ("Which is a contact force?", "friction between a sled and the snow", ["gravity pulling a ball down", "a magnet pulling a paper clip from far away", "static pulling hair"], "Contact forces need touching."),
        ("Which is a non-contact force?", "gravity", ["kicking a ball", "friction", "pushing a door"], "Gravity pulls from a distance."),
        ("What does gravity do?", "pulls objects toward Earth", ["pushes objects into space", "makes objects float", "makes things hot"], "That is why things fall."),
        ("Why is it hard to slide a box across a carpet?", "There is a lot of friction between the box and the carpet.", ["Carpet has no friction.", "Gravity pushes it sideways.", "The box is magnetic."], "Rough surfaces have more friction."),
        ("Why do hockey pucks slide far on ice?", "Ice is smooth, so there is little friction.", ["Ice pulls the puck forward.", "Pucks are magnetic.", "There is more gravity on ice."], "Less friction lets things slide."),
        ("Why do we put sand on icy sidewalks?", "to increase friction so people do not slip", ["to melt the ice", "to make the sidewalk smooth", "to decrease friction"], "Sand makes the surface rough."),
        ("A soccer ball rolls and then stops. What force slowed it down?", "friction from the grass and air", ["magnetism", "gravity pushing it forward", "no force at all"], "Friction acts against motion."),
        ("Which change can a force make?", "start, stop, speed up, slow down or change the direction of an object", ["only change its colour", "only make it bigger", "only make it heavier"], "Forces change motion and shape."),
        ("Two children push a box from opposite sides with the same force. What happens?", "The box does not move because the forces are balanced.", ["It moves to the left.", "It flies up.", "It moves to the right."], "Balanced forces cancel out."),
        ("Why do curlers sweep the ice in front of the stone?", "Sweeping reduces friction so the stone slides further.", ["To clean the ice for skating", "To make the ice colder", "To slow the stone down"], "Less friction, longer slide."),
        ("Why does a ball roll faster down a steep ramp than a gentle one?", "Gravity pulls it more along the steep slope.", ["The steep ramp has more friction.", "Gravity is weaker on gentle ramps.", "The ball is heavier on steep ramps."], "Steeper slopes speed things up."),
        ("Which force makes a toboggan go down a hill?", "gravity", ["magnetism", "a push from the snow", "static electricity"], "Gravity pulls it down the slope."),
        ("What helps a bike stop when you squeeze the brakes?", "friction between the brake pads and the wheel", ["gravity pulling the bike up", "magnetism", "air pushing the bike forward"], "Brakes use friction."),
    ])
    return [
        ("Pushes and pulls", [(pool, 6), (X.gen(UK3S, "g_pp"), 6), (X.gen(UK3S, "g_do"), 4), (X.gen(UK3S, "g_contact"), 4)]),
        ("Friction", [(X.gen(UK3S, "g_surf", n=6), 6), (X.gen(UK5F, "g_use"), 5), (X.gen(UK5F, "g_chg"), 5), (pool, 4)]),
        ("Gravity", [(X.gen(UK5G, "g_w", n=6), 6), (X.gen(UK5G, "g_moon", n=5), 5), (X.gen(UK5G, "g_m"), 4), (pool, 5)]),
        ("Patterns of motion", [(X.gen(US3M, "g_kind"), 6), (X.gen(US3M, "g_swing", n=5), 5), (X.gen(US3M, "g_bounce", n=5), 5), (X.gen(US3F, "g_change"), 4)]),
        ("Force investigations", [(X.gen(UK5F, "g_pull", n=4), 4), (X.gen(US3M, "g_steady", n=4), 4), (X.B(UK3S, "B5"), 4), (X.B(UK5F, "B5"), 4), (X.gen(UK5F, "g_ramp", n=4), 4)]),
    ]


def s_magnets(X):
    pool = X.pool([
        ("What are the two ends of a magnet called?", "the north pole and the south pole", ["the top and bottom", "the left and right", "the hot and cold ends"], "Poles are where the force is strongest."),
        ("What happens when two north poles are pushed together?", "They repel (push apart).", ["They attract.", "They melt.", "Nothing happens."], "Like poles repel."),
        ("What happens when a north pole and a south pole are near each other?", "They attract (pull together).", ["They repel.", "They spin.", "They get hot."], "Unlike poles attract."),
        ("Which object would a magnet pick up?", "a steel paper clip", ["an aluminum can", "a copper wire", "a plastic button"], "Iron, steel, nickel and cobalt are magnetic."),
        ("Can a magnet's force pass through paper?", "Yes, magnetism can act through thin materials.", ["No, never.", "Only through metal.", "Only through water."], "That is how fridge magnets hold paper."),
        ("What happens to a magnet's pull as you move it farther from a paper clip?", "It gets weaker.", ["It gets stronger.", "It stays the same.", "It changes to a push."], "Magnetic force weakens with distance."),
        ("What is static electricity?", "a build-up of electric charge on an object", ["electricity in wires", "a kind of magnet", "a light"], "Rubbing a balloon on your hair can make static."),
        ("A balloon rubbed on your hair can pick up tiny bits of paper. Why?", "The balloon has a static charge that attracts the paper.", ["The balloon is a magnet.", "The paper is sticky.", "Gravity pulls the paper up."], "Static electricity can attract light objects."),
        ("Why does your hair stand up after you take off a wool hat in winter?", "Static charge makes the hairs push away from each other.", ["Your hair is cold.", "Your hair is magnetic.", "The hat pulls it up."], "Like charges repel."),
        ("Which is a use of magnets?", "keeping a fridge door closed", ["making toast", "cutting paper", "growing plants"], "Magnets are in many objects."),
        ("How do recycling plants use magnets?", "to pull steel cans out of the mixed recycling", ["to pull out glass", "to melt plastic", "to wash paper"], "Steel is magnetic."),
        ("Which is a non-contact force?", "a magnet pulling a nail", ["a hand pushing a cart", "friction on a slide", "a foot kicking a ball"], "Magnets work without touching."),
        ("What does a compass needle do?", "points north because it is a small magnet", ["points to the Sun", "spins forever", "points to the nearest tree"], "Earth acts like a giant magnet."),
    ])
    return [
        ("Magnets attract and repel", [(pool, 5), (X.gen(UK3M, "g_pic"), 6), (X.gen(UK3M, "g_txt"), 5), (X.gen(UK3M, "g_three"), 4)]),
        ("Magnetic materials", [(X.gen(UK3G, "g_is", n=7), 7), (X.gen(UK3G, "g_pick", n=6), 6), (X.gen(UK3G, "g_sort"), 4), (pool, 3)]),
        ("Uses of magnets", [(X.gen(UK3M, "g_use"), 7), (X.gen(US3D, "g_why"), 5), (X.gen(US3D, "g_design"), 4), (pool, 4)]),
        ("Static electricity", [(X.gen(US3S, "g_static"), 7), (pool, 6), (X.gen(US3S, "g_poles"), 4), (X.gen(US3S, "g_metal"), 3)]),
        ("Magnet investigations", [(X.gen(UK3M, "g_strength", n=4), 4), (X.gen(UK3G, "g_table", n=4), 4), (X.gen(US3D, "g_crit", n=4), 4), (X.B(UK3M, "B5"), 4), (X.gen(SG3M, "g_through"), 4)]),
    ]


def s_struct(X):
    pool = X.pool([
        ("What is a structure?", "something built to support or hold something", ["a kind of food", "a type of weather", "a living thing"], "Houses, bridges, chairs and nests are structures."),
        ("Which is a natural structure?", "a bird's nest", ["a bridge", "a house", "a chair"], "Natural structures are not made by people."),
        ("Which is a human-made structure?", "the CN Tower", ["a spider web", "a beaver dam", "an anthill"], "People design and build human-made structures."),
        ("What makes a structure stable?", "a wide base and a low centre of weight", ["a narrow base", "being very tall and thin", "being made of paper only"], "Stable structures do not tip over."),
        ("What makes a structure strong?", "it can hold a load without breaking or bending too much", ["it is a bright colour", "it is very light", "it is round only"], "Strength is about holding loads."),
        ("Why is a triangle a strong shape for building?", "It keeps its shape when pushed.", ["It is pretty.", "It is the biggest shape.", "It uses no materials."], "Squares can squish into a diamond shape."),
        ("A tower of blocks falls over. How could you make it more stable?", "make the base wider", ["make it taller and thinner", "use fewer blocks at the bottom", "put the heaviest blocks on top"], "A wide base improves stability."),
        ("Why are the heaviest blocks placed at the bottom of a tower?", "It keeps the weight low so the tower is stable.", ["So the top is heavier.", "To make it fall faster.", "It does not matter."], "Heavy parts belong at the bottom."),
        ("Which material is best for building a strong bridge for a toy car?", "wooden craft sticks glued into triangles", ["wet paper", "loose sand", "string only"], "Shape and material both matter."),
        ("How can you make a sheet of paper strong enough to hold a book?", "fold it into a zigzag or roll it into a tube", ["leave it flat", "tear it in half", "get it wet"], "Shape adds strength."),
        ("What is a load?", "the weight or force a structure holds", ["the colour of a structure", "the age of a structure", "the name of a structure"], "A shelf holds a load of books."),
        ("Why does a beaver dam hold back water?", "It is made of sticks, mud and stones packed tightly with a wide base.", ["It is made of glass.", "Beavers glue it with honey.", "It is very thin."], "Beavers are natural engineers."),
        ("Why do igloos keep their shape?", "The dome shape spreads the weight evenly.", ["Igloos are made of steel.", "Snow is very light.", "The wind holds them up."], "Domes are strong shapes."),
        ("Which structure uses an arch?", "a stone bridge over a creek", ["a flat table", "a ladder", "a fence"], "Arches carry weight to the ground."),
        ("Why do tents need stakes and ropes?", "to keep them stable in the wind", ["to make them heavier to carry", "to keep rain out", "to make them colourful"], "Ropes and stakes hold the tent down."),
        ("Why should playground equipment be tested?", "to make sure it is strong, stable and safe for children", ["to change its colour", "to make it smaller", "to make it louder"], "Safety comes first."),
        ("Which joint lets a door swing open?", "a hinge", ["glue", "a nail", "tape"], "Hinges let parts move."),
        ("What does a building's foundation do?", "spreads the weight into the ground so it does not sink", ["holds up the roof only", "lets light in", "keeps rain off"], "Foundations are under the ground."),
        ("A chair wobbles. What is the most likely problem?", "one leg is shorter or loose", ["the chair is the wrong colour", "the seat is too soft", "the chair is too heavy"], "All legs must touch the floor evenly."),
        ("Why are hydro towers built with many triangles?", "Triangles make the frame strong and rigid.", ["Triangles are cheaper than metal.", "Triangles catch electricity.", "Triangles keep birds away."], "Frames use triangles for strength."),
        ("Why do bridges over wide rivers often have many pillars?", "Each pillar holds up part of the weight, so the bridge does not sag.", ["Pillars make the bridge longer.", "Pillars stop boats.", "Pillars are only for decoration."], "Supports share the load."),
        ("Which material bends without breaking, making it good for a fishing rod?", "a flexible material like fibreglass", ["glass", "chalk", "a clay pot"], "Flexible materials can bend."),
        ("Why do spider webs hold insects without breaking?", "The silk is strong and stretchy and the web spreads the force.", ["Spider silk is made of steel.", "Insects are very light.", "The web is glued to the Moon."], "Webs are natural structures."),
        ("Why is a cardboard box stronger with its flaps taped down?", "The closed shape holds together and spreads the load.", ["Tape is heavier.", "Open boxes are stronger.", "The flaps make it lighter."], "Closed shapes are stronger."),
        ("Why are snow forts built with thick walls at the bottom?", "Thick bottoms hold the weight of the snow above.", ["Snow is lighter at the bottom.", "To make the fort taller only.", "To let wind in."], "Bottoms carry the load."),
        ("Why are most houses in Ontario built with wood frames?", "Wood is strong, light, easy to cut and grows in Canada.", ["Wood is see-through.", "Wood is magnetic.", "Wood never burns or rots."], "Materials are chosen for their properties."),
        ("Why is steel used for tall towers and bridges?", "Steel is very strong and does not bend easily.", ["Steel is soft.", "Steel floats.", "Steel is light like paper."], "Strong materials hold big loads."),
        ("Why are glass windows thick in tall buildings?", "Thicker glass is stronger against wind.", ["Thick glass is darker.", "Thick glass is lighter.", "Thick glass bends easily."], "Thickness adds strength."),
        ("Which material would make the best roof for a doghouse?", "waterproof shingles on wood", ["paper towels", "a cotton sheet", "cardboard left outside"], "Roofs must keep water out."),
        ("Why are bricks good for building walls?", "They are hard, strong when stacked and do not burn.", ["They are soft and bendy.", "They are see-through.", "They float on water."], "Bricks resist squeezing."),
        ("Why might a builder choose recycled materials?", "to reduce waste and save resources", ["because they are always weaker", "to make more garbage", "because they cost more"], "Recycling helps the environment."),
        ("Which is the strongest way to join two craft sticks?", "glue them and let the glue dry fully", ["hold them with your fingers", "rest one on the other", "join them with wet paper"], "Strong joints make strong structures."),
        ("Which design would be the most stable lamp?", "a lamp with a wide, heavy base", ["a lamp with a narrow, light base", "a lamp balanced on one point", "a tall lamp with no base"], "Low and wide is stable."),
        ("What is the job of a pillar or column?", "to hold up weight from above", ["to let wind through", "to make a building taller only", "to hold water"], "Columns carry loads to the ground."),
    ])
    return [
        ("What is a structure?", [(pool, 12), (X.gen(USKS, "g_job", n=4), 4), (X.gen(US2B, "g_same", n=4), 4)]),
        ("Strong shapes", [(pool, 10), (X.gen(US2B, "g_pieces"), 5), (X.gen(US2B, "g_rebuild", n=5), 5)]),
        ("Stable structures", [(pool, 10), (X.gen(US3F, "g_still"), 5), (X.gen(US3F, "g_pic", n=5), 5)]),
        ("Materials for building", [(X.gen(USKS, "g_job", n=6), 6), (X.gen(USKS, "g_test", n=5), 5), (pool, 6), (X.gen(US2B, "g_count", n=3), 3), (X.B(US2B, "B1"), 2)]),
        ("Building and testing", [(X.B(US2B, "B5"), 4), (X.B(USKS, "B5"), 4), (X.B(US3F, "B5"), 4), (pool, 3), (X.gen(USKS, "g_graph"), 3), (X.gen(US3F, "g_tug", n=4), 2)]),
    ]


def s_soil(X):
    pool = X.pool([
        ("What is soil made of?", "tiny bits of rock, humus (rotting plants and animals), air, water and living things", ["only rocks", "only water", "only sand"], "Soil is a mixture."),
        ("What is humus?", "the dark part of soil made from decaying plants and animals", ["a kind of rock", "a type of rain", "a plastic"], "Humus gives soil nutrients."),
        ("Which kind of soil drains water fastest?", "sandy soil", ["clay soil", "loam", "mud"], "Sand has big spaces between grains."),
        ("Which kind of soil holds the most water?", "clay soil", ["sandy soil", "gravel", "pebbles"], "Clay particles are tiny and pack tightly."),
        ("Which kind of soil is best for growing most garden plants?", "loam (a mix of sand, silt, clay and humus)", ["pure sand", "pure clay", "gravel"], "Loam holds water and drains well."),
        ("How do earthworms help soil?", "They mix the soil, make tunnels for air and water, and add nutrients.", ["They make soil hard.", "They eat all the plants.", "They make soil dry."], "Worms are good for gardens."),
        ("What is composting?", "turning food scraps and leaves into rich soil with the help of decomposers", ["burning garbage", "washing soil", "putting soil in the freezer"], "Compost feeds plants."),
        ("Which item should NOT go in a compost bin?", "a plastic bag", ["banana peels", "leaves", "apple cores"], "Plastic does not break down."),
        ("Which living things break down dead leaves into soil?", "decomposers like worms, fungi and bacteria", ["birds", "deer", "fish"], "Decomposers recycle nutrients."),
        ("How does soil erosion happen?", "wind and water carry soil away", ["soil grows bigger", "soil turns into plants", "soil freezes forever"], "Bare soil erodes quickly."),
        ("How can farmers protect soil from erosion?", "plant cover crops and keep plant roots in the soil", ["leave fields bare", "remove all trees", "plough up and down steep hills"], "Roots hold soil in place."),
        ("Why is soil important to people?", "We grow food in it and it filters water.", ["It is not important.", "It only makes things dirty.", "It is only for worms."], "Healthy soil is a resource."),
        ("Which animal lives in soil?", "an ant", ["a robin", "a deer", "a duck"], "Many small animals live underground."),
        ("Which soil feels gritty when you rub it between your fingers?", "sandy soil", ["clay soil", "humus", "silt only"], "Sand grains are large."),
        ("Which soil feels sticky when wet?", "clay soil", ["sandy soil", "gravel", "dry leaves"], "Clay is smooth and sticky."),
        ("Many Indigenous peoples see soil as part of Mother Earth. What does this teach?", "to care for the land and give back to it", ["to use up the soil quickly", "that soil is not important", "to cover soil with concrete"], "Respect for the land helps protect soil."),
    ])
    return [
        ("What is soil?", [(pool, 6), (X.gen(UK3L, "g_made"), 6), (X.gen(UK3L, "g_type"), 5), (X.gen(UK3L, "g_lay"), 3)]),
        ("Kinds of soil", [(pool, 6), (X.gen(UK3L, "g_drain", n=6), 6), (X.gen(UK3L, "g_jar"), 5), (X.B(UK3L, "B1"), 3)]),
        ("Living things in soil", [(X.gen(UK3L, "g_worm"), 5), (X.gen(US5D, "g_which_dec", n=5), 5), (pool, 6), (X.B(AU3S, "POOL1"), 4)]),
        ("Caring for soil", [(pool, 8), (X.gen(US2E, "g_problem"), 4), (X.gen(US2E, "g_cause"), 4), (X.gen(US2E, "g_choose"), 4)]),
        ("Soil investigations", [(X.B(UK3L, "B5"), 5), (X.gen(US2E, "g_test", n=4), 4), (X.gen(UK3L, "g_drain", n=4), 4), (X.B(AU3S, "POOL5"), 4), (pool, 3)]),
    ]


def UNITS():
    return [
        CU("B", 1, "plant-parts-and-needs", "B2.1, B2.2, B2.3",
           "Describe the basic needs of plants; identify the major parts of plants and their functions; describe how water and "
           "nutrients move through a plant.",
           "Plant Parts and Needs", "Plant parts and needs",
           "Free Grade 3 science worksheets on the parts of a plant, what plants need to grow and how water moves through plants. "
           "100 questions with answers.",
           "Plants need light, air, water and nutrients.", "Roots take in water, stems carry it, leaves make food and flowers make seeds.",
           L("Plants need light, air, water, nutrients and space to grow.",
             "Roots take in water and nutrients and hold the plant in the soil.",
             "The stem holds the plant up and carries water to the leaves.",
             "Leaves use sunlight to make food. Flowers make seeds."),
           [("Which part takes in water?", ["it is under the ground"], "the roots"),
            ("A plant is kept in the dark. What happens?", ["it cannot make food"], "it becomes pale and weak")],
           ["Thinking plants get their food from the soil.", "Thinking all plants need the same amount of water.", "Thinking roots only hold the plant up."],
           [("What do plants need to grow?", "Light, air, water, nutrients from the soil and space."),
            ("What do leaves do?", "Leaves use sunlight, air and water to make food for the plant."),
            ("How does water get to the leaves?", "Water goes in through the roots and travels up the stem to the leaves.")],
           s_parts),
        CU("B", 2, "plant-life-cycles-and-seeds", "B2.4, B2.5, B2.6",
           "Describe the life cycle of flowering plants; explain pollination and the conditions seeds need to germinate; describe "
           "ways that seeds are dispersed.",
           "Plant Life Cycles and Seeds", "Plant life cycles and seeds",
           "Free Grade 3 science worksheets on plant life cycles, germination, flowers and pollination, and how seeds are spread. "
           "100 questions with answers.",
           "Seeds grow into plants that make new seeds.", "Pollination makes seeds; wind, water and animals spread them.",
           L("A flowering plant's life cycle: seed → seedling → adult plant → flower → fruit and seeds.",
             "Seeds need water, air and warmth to germinate.",
             "Pollination moves pollen from flower to flower, often by bees, butterflies or wind.",
             "Seeds spread by wind (maple keys), animals (burrs, berries), water and bursting pods."),
           [("How are dandelion seeds spread?", ["light and fluffy"], "by the wind"),
            ("What do seeds need to germinate?", ["they start in the soil"], "water, air and warmth")],
           ["Thinking seeds need light to germinate.", "Thinking only bees pollinate.", "Thinking a fruit is not part of the plant's life cycle."],
           [("What is germination?", "When a seed begins to grow a root and a shoot."),
            ("Why do plants spread their seeds?", "So the new plants have enough space, light and water away from the parent plant."),
            ("What is pollination?", "Moving pollen from one flower to another so the plant can make seeds.")],
           s_cycle),
        CU("B", 3, "plants-and-people", "B1.1, B1.2, B2.7",
           "Assess ways people use and depend on plants, including Indigenous knowledge such as the Three Sisters; describe "
           "plant adaptations; evaluate ways to protect plants and their habitats.",
           "Plants and People", "Plants and people",
           "Free Grade 3 science worksheets on how people use plants, the Three Sisters, maple syrup, plant adaptations and caring "
           "for plants. 100 questions with answers.",
           "People depend on plants.", "Plants give us food, oxygen, medicine and materials, so we must protect them.",
           L("Plants give us food, oxygen, shade, medicine, clothing and building materials.",
             "Many Indigenous communities grow the Three Sisters: corn, beans and squash, which help each other.",
             "Plants have adaptations, like thick stems to store water or wide leaves to catch light.",
             "We protect plants by caring for habitats, planting native plants and stopping invasive species."),
           [("Which tree gives sap for maple syrup?", ["sugar maple"], "the sugar maple"),
            ("How do beans help the Three Sisters?", ["they add nutrients to the soil"], "they feed the soil")],
           ["Thinking all plants are safe to eat.", "Thinking plants are not living things.", "Thinking people do not need plants."],
           [("Why are plants important?", "They make oxygen and food, give habitat to animals and give people many materials and medicines."),
            ("What are the Three Sisters?", "Corn, beans and squash, grown together in many Indigenous traditions because they help each other grow."),
            ("How can we protect plants?", "Stay on trails, do not pick wildflowers in parks, plant native plants and remove invasive plants.")],
           s_people),
        CU("C", 4, "forces-and-motion", "C2.1, C2.2, C2.3",
           "Describe forces as pushes and pulls; distinguish contact forces (friction) and non-contact forces (gravity); describe "
           "how forces change the motion and shape of objects.",
           "Forces and Motion", "Forces and motion",
           "Free Grade 3 science worksheets on pushes and pulls, friction, gravity and how forces change motion. 100 questions with answers.",
           "A force is a push or a pull.", "Friction slows things down; gravity pulls things toward Earth.",
           L("A force is a push or a pull. Forces can start, stop, speed up, slow down or turn an object.",
             "Contact forces happen when objects touch, like friction and pushes.",
             "Non-contact forces act from a distance, like gravity and magnetism.",
             "Smooth surfaces like ice have little friction; rough surfaces like carpet have more."),
           [("Why does a puck slide far on ice?", ["ice is smooth"], "there is little friction"),
            ("Which force pulls a toboggan down a hill?", ["it pulls toward Earth"], "gravity")],
           ["Thinking moving objects stop because they 'run out of force'.", "Thinking gravity only acts on heavy objects.", "Thinking friction is always bad."],
           [("What is friction?", "A force that acts when two surfaces rub together. It slows things down."),
            ("What is gravity?", "A pulling force that brings objects toward Earth."),
            ("What can a force do?", "It can make an object start or stop moving, speed up, slow down, change direction or change shape.")],
           s_forces),
        CU("C", 5, "magnets-and-static-electricity", "C2.4, C2.5, C1.1",
           "Describe magnetic and static (electrostatic) forces as non-contact forces; identify magnetic materials; describe uses "
           "of magnets in daily life.",
           "Magnets and Static Electricity", "Magnets and static electricity",
           "Free Grade 3 science worksheets on magnets, attract and repel, magnetic materials, uses of magnets and static "
           "electricity. 100 questions with answers.",
           "Like poles repel; unlike poles attract.", "Magnets pull iron and steel; static charge can also pull light objects.",
           L("Magnets have a north pole and a south pole.",
             "Like poles (N and N) repel; unlike poles (N and S) attract.",
             "Magnets attract iron, steel, nickel and cobalt, but not plastic, wood, glass or aluminum.",
             "Static electricity is a build-up of charge, like a balloon rubbed on your hair."),
           [("Will a magnet pick up an aluminum can?", ["aluminum is not magnetic"], "no"),
            ("What happens when two north poles meet?", ["like poles"], "they repel")],
           ["Thinking magnets attract all metals.", "Thinking bigger magnets are always stronger.", "Mixing up static electricity and magnetism."],
           [("Which materials are magnetic?", "Iron, steel, nickel and cobalt. Most other metals, like aluminum and copper, are not."),
            ("What is static electricity?", "A build-up of electric charge on an object, often from rubbing."),
            ("Where do we use magnets?", "Fridge doors, compasses, recycling plants, toys and speakers.")],
           s_magnets),
        CU("D", 6, "strong-and-stable-structures", "D2.1, D2.2, D2.3, D1.1",
           "Describe structures as natural or human-made; explain how shape, materials and a wide base make structures strong and "
           "stable; design, build and test structures that hold a load.",
           "Strong and Stable Structures", "Strong and stable structures",
           "Free Grade 3 science worksheets on natural and human-made structures, strong shapes, stability, materials and "
           "testing structures. 100 questions with answers.",
           "Strong structures hold loads; stable ones do not tip.", "Triangles, arches and wide bases make structures strong and stable.",
           L("A structure is something built to support or hold a load.",
             "Natural structures: nests, webs, beaver dams. Human-made: houses, bridges, the CN Tower.",
             "Strong shapes include triangles, arches, domes and tubes.",
             "Stable structures have a wide base and keep heavy parts low."),
           [("How can you make a block tower more stable?", ["wider base", "heavy blocks at the bottom"], "make the base wider"),
            ("Why is a triangle strong?", ["it does not squish"], "it keeps its shape")],
           ["Thinking taller structures are always better.", "Thinking only heavy materials make strong structures.", "Thinking shape does not matter."],
           [("What is the difference between strong and stable?", "A strong structure holds a load without breaking. A stable structure does not tip over."),
            ("Why are triangles used in bridges?", "A triangle cannot change shape unless a side breaks, so it is very strong."),
            ("How do engineers test structures?", "They add loads and push on them to see if they bend, break or tip, then improve the design.")],
           s_struct),
        CU("E", 7, "soils", "E2.1, E2.2, E2.3",
           "Describe the components of soil; compare sandy, clay and loam soils and how well they hold water; describe the role of "
           "living things such as worms and decomposers in soil.",
           "Soils", "Soils",
           "Free Grade 3 science worksheets on what soil is made of, sandy, clay and loam soils, drainage and living things in "
           "soil. 100 questions with answers.",
           "Soil is a mixture of rock, humus, air and water.", "Sand drains fast, clay holds water, and loam is best for most plants.",
           L("Soil is a mixture of tiny bits of rock, humus, air, water and living things.",
             "Sandy soil drains fast; clay soil holds water and is sticky; loam is a good mix.",
             "Humus comes from decaying plants and animals and adds nutrients.",
             "Worms, insects, fungi and bacteria live in soil and keep it healthy."),
           [("Which soil drains fastest?", ["big spaces between grains"], "sandy soil"),
            ("How do worms help soil?", ["tunnels", "mixing"], "they let in air and water")],
           ["Thinking soil is just dirt with nothing living in it.", "Thinking all soils are the same.", "Thinking worms harm gardens."],
           [("What is humus?", "The dark, rich part of soil made from rotting plants and animals."),
            ("Which soil is best for gardens?", "Loam, because it holds enough water but also drains well and has nutrients."),
            ("What lives in soil?", "Worms, ants, beetles, fungi, bacteria and many other living things.")],
           s_soil),
        CU("E", 8, "soils-and-the-environment", "E1.1, E1.2, E2.4",
           "Assess the importance of soil to people and the environment; describe composting and decomposition; evaluate ways to "
           "reduce soil erosion and protect soil, including Indigenous perspectives on caring for the land.",
           "Soils and the Environment", "Soils and the environment",
           "Free Grade 3 science worksheets on composting, decomposers, soil erosion and caring for soil. 100 questions with answers.",
           "Healthy soil grows our food.", "Composting adds nutrients; plants and cover crops stop erosion.",
           L("People need healthy soil to grow food and filter water.",
             "Decomposers turn dead plants and food scraps into compost.",
             "Wind and water can erode bare soil.",
             "Cover crops, trees, windbreaks and caring for the land protect soil."),
           [("What should go in a compost bin?", ["food scraps and leaves break down"], "banana peels and leaves"),
            ("How do plant roots help soil?", ["roots hold soil"], "they stop erosion")],
           ["Thinking plastic will break down in compost.", "Thinking soil is unlimited.", "Thinking erosion only happens in deserts."],
           [("What is composting?", "Letting decomposers break down food scraps and yard waste into rich soil."),
            ("How can we stop soil erosion?", "Keep plants growing on the soil, plant trees and cover crops, and build windbreaks."),
            ("Why is soil important?", "Soil grows our food, is a home for many living things and cleans water as it soaks into the ground.")],
           s_soilenv),
    ]


def s_soilenv(X):
    pool = X.pool([
        ("Which is a decomposer?", "a mushroom", ["a robin", "a maple tree", "a rabbit"], "Fungi break down dead things."),
        ("Why should food scraps go in a green bin instead of the garbage?", "They can be turned into compost instead of filling landfills.", ["They make landfills smell nice.", "Garbage trucks need them.", "They turn into plastic."], "Ontario cities collect green bins."),
        ("What happens to an apple core left in a compost bin for months?", "Decomposers break it down into soil.", ["It turns into a rock.", "It stays exactly the same.", "It grows into a tree right away."], "Decomposition recycles nutrients."),
        ("Which makes compost break down faster?", "mixing it and keeping it damp and warm", ["freezing it", "keeping it dry and sealed in plastic", "adding glass"], "Decomposers need air, water and warmth."),
        ("Why is bare soil easily eroded?", "Nothing holds it in place against wind and rain.", ["Bare soil is heavier.", "Bare soil is magnetic.", "Bare soil cannot get wet."], "Roots protect soil."),
        ("What is a windbreak?", "a row of trees that slows the wind across a field", ["a broken window", "a kind of fence that blows over", "a wind turbine"], "Windbreaks protect soil and crops."),
        ("Which farm practice protects soil?", "planting cover crops in the fall", ["leaving fields bare all winter", "removing all hedges", "ploughing down steep slopes"], "Cover crops hold the soil."),
        ("Why should people not drive off-road vehicles on wet trails?", "They dig up soil and cause erosion.", ["They make the soil healthier.", "They plant seeds.", "They have no effect."], "Ruts channel water and wash soil away."),
        ("What is a landfill?", "a place where garbage is buried", ["a field of flowers", "a type of soil", "a compost bin"], "Reducing waste saves landfill space."),
        ("How does soil help clean water?", "Water is filtered as it soaks down through soil layers.", ["Soil adds pollution.", "Soil makes water salty.", "Soil stops all water."], "Soil acts like a filter."),
        ("Which pollutes soil?", "oil or paint spilled on the ground", ["fallen leaves", "worm castings", "compost"], "Dispose of chemicals safely."),
        ("Why do gardeners add mulch around plants?", "to keep soil moist and protect it from erosion", ["to make soil hot", "to attract garbage", "to remove nutrients"], "Mulch covers bare soil."),
    ])
    return [
        ("Decomposers and compost", [(pool, 4), (X.gen(US5D, "g_which_dec", n=6), 6), (X.gen(US5D, "g_compost", n=4), 4), (X.B(US5D, "B1"), 4), (X.gen(US5D, "g_arrow"), 2)]),
        ("Soil erosion", [(X.gen(US2E, "g_problem"), 5), (X.gen(US2E, "g_cause"), 5), (pool, 6), (X.gen(US2E, "g_pic", n=4), 4)]),
        ("Protecting soil", [(X.gen(US2E, "g_choose"), 6), (pool, 8), (X.B(US2E, "B1"), 6)]),
        ("Soil and people", [(pool, 4), (X.gen(UK3L, "g_type", n=4), 4), (X.B(UK3L, "B1"), 4), (X.B(AU3S, "POOL1"), 3), (X.gen(UK3L, "g_made", n=3), 3), (X.gen(UK3L, "g_jar", n=3), 2)]),
        ("Soil and environment investigations", [(X.gen(US2E, "g_test", n=5), 5), (X.B(US2E, "B5"), 4), (X.B(US5D, "B5"), 4), (X.gen(US5D, "g_rot_table", n=4), 4), (X.gen(US5D, "g_return"), 3)]),
    ]
