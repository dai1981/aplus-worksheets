# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 1 (B Needs and Characteristics of Living Things, C Energy in Our Lives,
D Materials, Objects, and Everyday Structures, E Daily and Seasonal Changes). Short sentences, a picture on top. Built by caon_sci.build."""
from caon_sci import CU
import sci_kids as K

UK2L, USKN, USKW, AUY1 = ("gen_uk_science_y2_living_dead_and_never_alive", "gen_us_science_gk_what_plants_and_animals_need",
                          "gen_us_science_gk_where_plants_and_animals_live", "gen_au_science_y1_needs_of_living_things")
UK2A, UK1G, UK1B, UK1P = ("gen_uk_science_y2_what_animals_need_to_survive", "gen_uk_science_y1_animal_groups",
                          "gen_uk_science_y1_animal_bodies", "gen_uk_science_y1_parts_of_a_plant")
UK1BD, UK1S, US1P, UK2H = ("gen_uk_science_y1_parts_of_the_body", "gen_uk_science_y1_the_five_senses",
                           "gen_us_science_g1_plant_and_animal_parts", "gen_uk_science_y2_staying_healthy")
USKS, USKC, UK2P = "gen_us_science_gk_sunlight_warms_earth", "gen_us_science_gk_caring_for_earth", "gen_uk_science_y2_what_plants_need_to_stay_healthy"
UK1O, UK1M, US2M, USKD, UK2U = ("gen_uk_science_y1_objects_and_materials", "gen_uk_science_y1_properties_of_materials",
                                "gen_us_science_g2_properties_of_materials", "gen_us_science_gk_shade_structures", "gen_uk_science_y2_uses_of_everyday_materials")
US2B = "gen_us_science_g2_building_with_small_pieces"
UK1S4, UK1W, USKWE, US1D, US1S = ("gen_uk_science_y1_four_seasons", "gen_uk_science_y1_weather_and_day_length", "gen_us_science_gk_weather",
                                  "gen_us_science_g1_daylight_and_seasons", "gen_us_science_g1_sun_moon_and_stars")
US1L = "gen_us_science_g1_light_and_seeing"
UK1T, USKV = "gen_uk_science_y1_deciduous_and_evergreen_trees", "gen_us_science_gk_severe_weather"


def s_living(X):
    pool = X.pool([
        ("Which one is living?", "a frog", ["a rock", "a toy car", "a spoon"], "A frog grows, eats and moves."),
        ("Which one is not living?", "a rock", ["a tree", "a bird", "a worm"], "A rock does not grow or eat."),
        ("What do all living things do?", "grow and change", ["stay the same forever", "never need food", "never move or grow"], "Living things grow."),
        ("Is a maple tree living?", "Yes. It grows and needs water.", ["No. It cannot walk.", "No. It is made of wood.", "Only in summer."], "Plants are living things."),
        ("Is a teddy bear living?", "No. It does not eat or grow.", ["Yes. It looks like a bear.", "Yes. It is soft.", "Only at night."], "Toys are not living."),
        ("Which one was once living?", "a fallen leaf", ["a glass", "a plastic cup", "a stone"], "The leaf came from a living tree."),
        ("Which one can have babies?", "a cat", ["a ball", "a chair", "a cloud"], "Living things make more of their own kind."),
        ("Which one is a living thing that lives in a pond?", "a duck", ["a boat", "a pebble", "a bottle"], "Ducks are living."),
    ])
    return [
        ("Living or not living?", [(pool, 6), (X.gen(UK2L, "g_sort", n=7), 7), (X.gen(UK2L, "g_pick", n=7), 7)]),
        ("What living things do", [(X.gen(UK2L, "g_proc"), 6), (X.gen(USKN, "g_living", n=6), 6), (pool, 4), (X.gen(UK2L, "g_trick"), 4)]),
        ("Plants and animals", [(X.gen(UK1G, "g_group", n=6), 6), (X.gen(UK1G, "g_pick", n=6), 6), (X.gen(UK1G, "g_feat"), 4), (X.gen(UK1G, "g_pic", n=4), 4)]),
        ("Animal bodies", [(X.gen(UK1B, "g_has", n=6), 6), (X.gen(UK1B, "g_job"), 5), (X.gen(UK1B, "g_legs"), 5), (X.gen(UK1B, "g_both"), 4)]),
        ("Looking at living things", [(X.gen(UK2L, "g_picture", n=5), 5), (X.B(UK2L, "B5"), 4), (X.B(UK1G, "B5"), 4), (X.B(UK1B, "B5"), 3), (pool, 2), (X.gen(US1P, "g_part", n=4), 2)]),
    ]


def s_needs(X):
    pool = X.pool([
        ("What do animals need?", "food, water, air and shelter", ["toys and games", "only sunlight", "only shelter"], "Animals need these to live."),
        ("What do plants need?", "sunlight, water, air and soil", ["candy", "a blanket", "darkness"], "Plants need light to grow."),
        ("Where does a squirrel find shelter?", "in a nest in a tree", ["in a fish bowl", "in a cloud", "in a mailbox"], "Squirrels build nests."),
        ("What does a pet dog need every day?", "food, water and care", ["only toys", "only a bath", "nothing"], "Pets depend on people."),
        ("Why do people need clean water?", "to drink and stay healthy", ["to make it rain", "to grow taller in one day", "to make rocks"], "People are living things too."),
        ("A plant gets no water for many days. What happens?", "It droops and can die.", ["It grows faster.", "It turns into a tree.", "Nothing happens."], "Plants need water."),
        ("Where does a beaver live?", "in a lodge in a pond", ["in a desert", "in a nest in the sky", "in a cave of ice"], "The pond gives food and water."),
        ("What do people need to stay healthy?", "food, water, sleep and exercise", ["only candy", "only screen time", "no sleep"], "Healthy habits help us grow."),
    ])
    return [
        ("Needs of animals", [(pool, 5), (X.gen(UK2A, "g_need"), 6), (X.gen(UK2A, "g_air"), 4), (X.gen(USKN, "g_need", n=5), 5)]),
        ("Needs of plants", [(X.gen(UK2P, "g_need"), 6), (X.gen(UK2P, "g_place"), 5), (X.gen(UK2P, "g_temp"), 4), (pool, 5)]),
        ("Food for living things", [(X.gen(USKN, "g_eat", n=6), 6), (X.gen(UK2A, "g_pfood"), 5), (X.gen(USKN, "g_kind"), 5), (X.gen(UK2A, "g_pet"), 4)]),
        ("Homes and habitats", [(X.gen(USKW, "g_where", n=6), 6), (X.gen(USKW, "g_why"), 5), (X.gen(UK2A, "g_wild"), 5), (pool, 4)]),
        ("Caring for living things", [(X.gen(USKW, "g_people"), 5), (X.B(UK2A, "B5"), 4), (X.B(USKN, "B5"), 4), (X.B(UK2P, "B5"), 4), (X.gen(UK2A, "g_scen"), 3)]),
    ]


def s_body(X):
    pool = X.pool([
        ("Which sense do you use to hear a bird?", "hearing", ["smell", "taste", "touch"], "You hear with your ears."),
        ("Which body part helps you smell?", "the nose", ["the elbow", "the knee", "the ear"], "You smell with your nose."),
        ("Which sense tells you snow is cold?", "touch", ["sight", "hearing", "taste"], "Your skin feels cold."),
        ("Why do we wear sunglasses on a sunny day?", "to protect our eyes", ["to hear better", "to smell flowers", "to keep our feet warm"], "Bright light can hurt eyes."),
        ("Why should you wash your hands before you eat?", "to wash away germs", ["to make food taste better", "to make your hands bigger", "to warm the food"], "Germs can make you sick."),
        ("What helps keep your body strong?", "playing outside and eating healthy food", ["staying up all night", "eating only candy", "never moving"], "Exercise and food help you grow."),
        ("Which body part helps you see?", "the eyes", ["the toes", "the knees", "the nose"], "You see with your eyes."),
        ("Why do we wear a helmet when we bike?", "to protect our head", ["to see better", "to taste food", "to hear music"], "Helmets keep us safe."),
    ])
    return [
        ("Parts of the body", [(X.gen(UK1BD, "g_pic", n=6), 6), (X.gen(UK1BD, "g_where"), 5), (X.gen(UK1BD, "g_do"), 5), (X.gen(UK1BD, "g_face"), 4)]),
        ("The five senses", [(X.gen(UK1S, "g_sense", n=6), 6), (X.gen(UK1S, "g_act"), 5), (X.gen(UK1S, "g_word"), 5), (pool, 4)]),
        ("Senses keep us safe", [(X.gen(UK1S, "g_safe"), 6), (pool, 6), (X.gen(UK1S, "g_walk", n=4), 4), (X.B(UK1S, "B1"), 4)]),
        ("Staying healthy", [(X.gen(UK2H, "g_choice"), 6), (X.gen(UK2H, "g_hyg"), 5), (X.gen(UK2H, "g_exer"), 5), (pool, 4)]),
        ("Body investigations", [(X.gen(UK1BD, "g_count", n=4), 4), (X.B(UK1BD, "B5"), 4), (X.B(UK1S, "B5"), 4), (X.B(UK2H, "B5"), 4), (X.gen(UK2H, "g_body"), 4)]),
    ]


def s_energy(X):
    pool = X.pool([
        ("Where does most of Earth's energy come from?", "the Sun", ["the Moon", "clouds", "rocks"], "The Sun gives light and heat."),
        ("What does the Sun give us?", "light and heat", ["only cold", "only snow", "only wind"], "The Sun warms Earth."),
        ("Where do we get energy to run and play?", "from the food we eat", ["from our shoes", "from the sky", "from a light switch"], "Food gives us energy."),
        ("Which one uses electricity?", "a lamp", ["a book", "a ball", "a spoon"], "Lamps need electricity."),
        ("Which one uses energy from gasoline?", "a car", ["a bike", "a kite", "a sled"], "Cars burn gas for energy."),
        ("Which one uses energy from the wind?", "a kite", ["a fridge", "a TV", "a stove"], "Wind pushes the kite."),
        ("Which one uses energy from the Sun?", "a solar panel", ["a candle", "a radio", "a toaster"], "Solar panels change sunlight into electricity."),
        ("How can you save energy at home?", "turn off the lights when you leave a room", ["leave the TV on", "keep the fridge door open", "turn on every light"], "Saving energy helps Earth."),
        ("Why does a sidewalk feel hot on a sunny day?", "The Sun heats it.", ["It is plugged in.", "It is made of fire.", "The Moon heats it."], "Sunlight warms things."),
        ("Which is a way to stay warm without using energy?", "put on a sweater", ["turn up the heat", "turn on the oven", "use a hair dryer"], "Clothes keep heat in."),
        ("Which is a way to get to school using your own energy?", "walk or bike", ["take a car", "take a bus", "fly a plane"], "Your body uses food energy."),
        ("Why do plants need the Sun?", "They use sunlight to make food.", ["They need it to sleep.", "It makes them cold.", "They do not need it."], "Plants get energy from sunlight."),
        ("Which one makes light?", "a flashlight", ["a mirror", "a spoon", "a rock"], "A flashlight uses a battery."),
        ("Which one makes heat?", "a campfire", ["an ice cube", "a snowball", "a glass of cold water"], "Burning wood gives off heat."),
        ("What is one way the Sun helps people?", "It helps plants grow so we have food.", ["It makes snow.", "It turns off lights.", "It makes us sleep."], "We depend on the Sun."),
        ("Which one uses a battery?", "a flashlight", ["a sled", "a book", "a cup"], "Batteries store energy."),
        ("Which one is a way to cook food with energy?", "a stove", ["a pillow", "a backpack", "a mitten"], "Stoves use gas or electricity."),
        ("Which one moves because of energy from your body?", "a bike you pedal", ["a car", "a bus", "a train"], "Your muscles push the pedals."),
        ("What gives a sailboat energy to move?", "the wind", ["the Moon", "a battery", "snow"], "Wind pushes the sail."),
        ("What happens to a snowman on a sunny day?", "It melts because the Sun warms it.", ["It grows bigger.", "It turns into a tree.", "Nothing happens."], "Sunlight gives heat."),
        ("Which food gives you energy for a busy day?", "a healthy breakfast like oatmeal and fruit", ["no breakfast", "only candy", "only pop"], "Healthy food gives lasting energy."),
        ("Why do we feel warm sitting near a campfire?", "The fire gives off heat energy.", ["The fire is cold.", "The wind is hot.", "The Moon is near."], "Fire gives light and heat."),
        ("Which one uses energy to make sound?", "a radio", ["a rock", "a sock", "a pencil"], "Radios use electricity."),
        ("Why should you close the door in winter?", "to keep the heat inside", ["to let the cold in", "to make the house darker", "to make noise"], "Saving heat saves energy."),
        ("Which is a way to use less electricity?", "read a book instead of watching TV", ["leave the TV on all day", "open the fridge many times", "turn on all the lights"], "Small choices save energy."),
        ("Why should you unplug a charger when you are done?", "to save energy", ["to make it hot", "to make it louder", "to break it"], "Chargers can waste energy."),
    ])
    return [
        ("Energy from the Sun", [(pool, 6), (X.gen(USKS, "g_warm", n=6), 6), (X.gen(USKS, "g_touch"), 4), (X.gen(USKS, "g_ice"), 4)]),
        ("Energy for living things", [(pool, 8), (X.gen(USKN, "g_need", n=5), 4), (X.gen(UK2H, "g_choice", n=5), 4), (X.gen(US1L, "g_src", n=4), 4)]),
        ("Energy in our homes", [(pool, 8), (X.gen(USKC, "g_help", n=5), 4), (X.gen(USKC, "g_better"), 4), (X.gen(US1L, "g_pick", n=4), 4)]),
        ("Saving energy", [(pool, 8), (X.gen(USKC, "g_pick", n=6), 6), (X.gen(USKC, "g_prob"), 6)]),
        ("Energy investigations", [(X.gen(USKS, "g_thermo", n=5), 5), (X.gen(USKS, "g_time"), 4), (X.B(USKS, "B5"), 4), (X.B(USKC, "B5"), 3), (pool, 4)]),
    ]


def s_materials(X):
    pool = X.pool([
        ("What is a raincoat made of?", "plastic or rubber", ["paper", "cotton balls", "glass"], "It keeps you dry."),
        ("Why is a window made of glass?", "You can see through it.", ["It is soft.", "It is bendy.", "It is fluffy."], "Glass is clear."),
        ("Why is a spoon made of metal?", "Metal is strong and easy to clean.", ["Metal is soft.", "Metal is see-through.", "Metal floats away."], "Spoons must not break."),
        ("Which material is soft?", "wool", ["rock", "metal", "glass"], "Wool is soft and warm."),
        ("Which material is hard?", "wood", ["cotton", "a sponge", "a pillow"], "A wooden table is hard."),
        ("Which material soaks up water?", "a paper towel", ["a plastic cup", "a metal spoon", "a glass jar"], "Paper towels are absorbent."),
        ("Which one is waterproof?", "a rubber boot", ["a paper bag", "a sock", "a cotton T-shirt"], "Water cannot get through rubber."),
        ("Which can be recycled in Ontario's blue box?", "a clean can", ["a banana peel", "a broken toy with batteries", "a pizza box full of food"], "Cans, bottles and paper can be recycled."),
        ("Why should we reuse things?", "to make less garbage", ["to make more garbage", "to waste materials", "to make things break"], "Reuse helps Earth."),
        ("Which object is made of more than one material?", "a pencil (wood, graphite and rubber)", ["a stone", "an ice cube", "a leaf"], "Many objects use different materials."),
    ])
    return [
        ("Objects and materials", [(X.gen(UK1O, "g_om", n=6), 6), (X.gen(UK1O, "g_pick", n=6), 6), (X.gen(UK1O, "g_which"), 4), (pool, 4)]),
        ("Properties of materials", [(X.gen(UK1M, "g_prop"), 6), (X.gen(UK1M, "g_opp"), 5), (X.gen(US2M, "g_what"), 5), (X.gen(UK1M, "g_group"), 4)]),
        ("Choosing materials", [(X.gen(UK2U, "g_mat"), 6), (X.gen(UK2U, "g_why", n=6), 6), (X.gen(UK2U, "g_bad"), 4), (pool, 4)]),
        ("Reduce, reuse, recycle", [(pool, 6), (X.gen(USKC, "g_bin"), 6), (X.gen(USKC, "g_reuse"), 5), (X.gen(UK1O, "g_multi"), 3)]),
        ("Testing materials", [(X.gen(UK1M, "g_soak"), 5), (X.gen(UK2U, "g_test"), 5), (X.B(UK1M, "B5"), 4), (X.B(UK1O, "B5"), 3), (X.gen(US2M, "g_table", n=3), 3)]),
    ]


def s_struct(X):
    pool = X.pool([
        ("What is a structure?", "something that is built to hold or support something", ["a kind of food", "a type of weather", "an animal"], "Houses, tables and nests are structures."),
        ("Which is a structure made by an animal?", "a bird's nest", ["a bridge", "a school", "a slide"], "Animals build structures too."),
        ("Which is a structure made by people?", "a house", ["a spider web", "a beehive", "an anthill"], "People build houses."),
        ("What does a table hold up?", "plates, books and other things", ["the sky", "the floor", "the sun"], "A table is a structure."),
        ("Why does a chair have legs?", "to hold it up", ["to make it walk", "to make it pretty", "to make it heavy"], "Legs support the seat."),
        ("Which tower will stand up best?", "one with a wide bottom", ["one with a tiny bottom", "one with no bottom", "one that leans a lot"], "A wide base is stable."),
        ("Why is a shelter like a tent useful?", "It keeps rain and sun off people.", ["It makes rain.", "It makes things cold.", "It has no use."], "Shelters protect us."),
        ("Why does a slide at the park need to be strong?", "so children can use it safely", ["so it can fly", "so it can float", "so it can melt"], "Strong structures are safe."),
        ("Which shape helps make a structure strong?", "a triangle", ["a wiggly line", "a dot", "a floppy circle of string"], "Triangles keep their shape."),
        ("What is a beaver dam made of?", "sticks, mud and stones", ["glass and metal", "plastic bags", "paper"], "Beavers use what they find."),
        ("Why do we put a roof on a house?", "to keep out rain and snow", ["to let in rain", "to make it shorter", "to make it colder"], "Roofs protect us."),
        ("Why does a birdhouse have a roof?", "to keep the birds dry", ["to make it heavy", "so birds can see the sky", "to keep the birds out"], "Shelters protect from rain."),
        ("Which is the best material for a shelter that keeps rain off?", "plastic or waterproof cloth", ["paper towels", "tissue paper", "a net"], "Waterproof materials keep you dry."),
        ("Why are fences built around a playground?", "to keep children safe", ["to keep the sun out", "to make it rain", "to make the slide taller"], "Structures can protect."),
        ("A block tower keeps falling. What can you try?", "make the bottom wider", ["make the bottom smaller", "stack it on a ball", "use fewer blocks at the bottom"], "Try, test and improve."),
        ("Why does a ladder have rungs?", "so you can step on them to climb", ["so it looks pretty", "so it floats", "so it can roll"], "Each part has a job."),
        ("What does a tent pole do?", "holds the tent up", ["keeps the tent dry", "makes the tent warm", "makes the tent smell nice"], "Poles support the tent."),
        ("Why is a bridge built over a river?", "so people can cross the river", ["so fish can fly", "to stop the river", "to make the river hot"], "Bridges help us travel."),
    ])
    return [
        ("What is a structure?", [(pool, 8), (X.gen(USKD, "g_need"), 6), (X.gen(US2B, "g_same", n=6), 6)]),
        ("Natural and built structures", [(pool, 8), (X.gen(USKD, "g_mat"), 6), (X.gen(US2B, "g_pieces"), 6)]),
        ("Building a shade structure", [(X.gen(USKD, "g_pick"), 6), (X.gen(USKD, "g_test"), 6), (X.gen(USKD, "g_fix"), 5), (pool, 3)]),
        ("Building with pieces", [(X.gen(US2B, "g_count", n=6), 6), (X.gen(US2B, "g_rebuild", n=6), 6), (pool, 4), (X.B(US2B, "B1"), 4)]),
        ("Testing structures", [(X.B(USKD, "B5"), 5), (X.B(US2B, "B5"), 5), (X.B(USKD, "B1"), 4), (pool, 4), (X.gen(USKD, "g_test", n=3), 2)]),
    ]


def s_daily(X):
    pool = X.pool([
        ("When does the Sun rise?", "in the morning", ["at night", "at noon", "at midnight"], "The Sun rises in the morning."),
        ("When can we see the stars best?", "at night", ["at noon", "in the morning", "after lunch"], "The sky is dark at night."),
        ("Which do people usually do at night?", "sleep", ["eat lunch at school", "play at recess", "go to the beach"], "Night is for resting."),
        ("Which animal is awake at night?", "an owl", ["a robin", "a butterfly", "a bee"], "Owls hunt at night."),
        ("Why is it dark at night?", "Our side of Earth faces away from the Sun.", ["The Sun turns off.", "Clouds cover the Sun.", "The Moon eats the Sun."], "Earth spins."),
        ("Where is the Sun at noon?", "high in the sky", ["under the ground", "behind the Moon", "at the bottom of the sky"], "Noon is the middle of the day."),
        ("What is weather?", "what the sky and air are like each day", ["a kind of rock", "a kind of animal", "a toy"], "Weather can be sunny, rainy or snowy."),
        ("Which tool measures how hot or cold it is?", "a thermometer", ["a ruler", "a spoon", "a clock"], "Thermometers measure temperature."),
        ("It is raining. What should you wear outside?", "a raincoat and rubber boots", ["sandals and shorts", "a swimsuit", "a winter hat only"], "Dress for the weather."),
        ("Why are shadows long in the morning?", "The Sun is low in the sky.", ["The Sun is very high.", "It is night.", "Shadows grow at night."], "Low Sun, long shadows."),
    ])
    return [
        ("Day and night", [(pool, 6), (X.gen(US1S, "g_when", n=6), 6), (X.gen(US1S, "g_see"), 4), (X.gen(US1S, "g_time"), 4)]),
        ("The Sun in the sky", [(X.gen(US1S, "g_dir"), 6), (X.gen(US1D, "g_sunset", n=5), 5), (X.gen(US1S, "g_pick"), 5), (pool, 4)]),
        ("Weather every day", [(X.gen(USKWE, "g_word"), 6), (X.gen(USKWE, "g_wear"), 5), (X.gen(UK1W, "g_sym"), 5), (X.gen(UK1W, "g_desc"), 4)]),
        ("Weather and safety", [(X.gen(USKV, "g_safe"), 6), (X.gen(USKV, "g_name"), 5), (X.gen(USKV, "g_kit"), 5), (pool, 4)]),
        ("Watching the sky", [(X.gen(UK1W, "g_chart", n=5), 5), (X.gen(USKWE, "g_week", n=5), 5), (X.B(US1S, "B5"), 4), (X.B(UK1W, "B5"), 3), (X.gen(US1S, "g_pred"), 3)]),
    ]


def s_seasons(X):
    pool = X.pool([
        ("Which season comes after winter?", "spring", ["summer", "fall", "winter again"], "Winter, spring, summer, fall."),
        ("In which season do maple leaves change colour and fall?", "fall", ["spring", "summer", "winter"], "Leaves turn red, orange and yellow."),
        ("In which season is there snow in Ontario?", "winter", ["summer", "spring only", "never"], "Ontario winters are cold and snowy."),
        ("Which season has the longest days in Ontario?", "summer", ["winter", "fall", "they are all the same"], "Summer days are long."),
        ("What do bears do in winter?", "sleep in a den for a long time", ["fly south", "swim in the lake", "build snowmen"], "This helps them survive."),
        ("Why do many birds fly south in the fall?", "to find food and warmer weather", ["to see the ocean", "to visit friends", "because they are lost"], "This is called migration."),
        ("What do squirrels do in the fall?", "gather and hide nuts for the winter", ["grow leaves", "go to sleep in water", "fly away"], "They store food."),
        ("What do people do to get ready for winter?", "put on warm coats, hats and mittens", ["wear shorts", "go swimming in the lake", "plant flowers outside"], "Dress for cold weather."),
        ("Which happens in spring?", "Snow melts and flowers start to grow.", ["Leaves fall off trees.", "Lakes freeze.", "It snows every day."], "Spring is warmer."),
        ("Why do people plant gardens in spring?", "It is getting warmer and the ground is soft.", ["It is the coldest time.", "The ground is frozen.", "Plants grow best in snow."], "Seeds need warmth."),
        ("Which tree stays green all winter?", "a pine tree", ["a maple tree", "an oak tree", "a birch tree"], "Pine trees are evergreen."),
        ("What happens to ponds in Ontario winters?", "They freeze on top.", ["They boil.", "They turn into sand.", "They disappear forever."], "Fish live under the ice."),
    ])
    return [
        ("The four seasons", [(X.gen(UK1S4, "g_order"), 6), (X.gen(UK1S4, "g_sign", n=6), 6), (pool, 5), (X.gen(UK1S4, "g_month", n=3), 3)]),
        ("Dressing for the seasons", [(X.gen(UK1S4, "g_wear"), 6), (X.gen(USKWE, "g_seas"), 5), (pool, 5), (X.gen(USKWE, "g_clue"), 4)]),
        ("Plants and animals in the seasons", [(pool, 6), (X.gen(UK1S4, "g_tree"), 5), (X.gen(UK1T, "g_type"), 5), (X.gen(UK1T, "g_pick"), 4)]),
        ("Daylight and seasons", [(X.gen(US1D, "g_season"), 6), (X.gen(US1D, "g_chart", n=5), 5), (X.gen(UK1W, "g_light"), 5), (X.gen(US1D, "g_next"), 4)]),
        ("Season investigations", [(X.gen(UK1S4, "g_temp", n=5), 5), (X.B(UK1S4, "B5"), 4), (X.B(US1D, "B5"), 4), (X.gen(UK1T, "g_survey", n=4), 4), (X.gen(US1D, "g_obs"), 3)]),
    ]


def UNITS():
    return [
        CU("B", 1, "living-and-non-living-things", "B2.1, B2.2",
           "Identify living and non-living things; describe the characteristics of living things and how plants and animals, "
           "including humans, are alike and different.",
           "Living and Non-Living Things", "Living and non-living things",
           "Free Grade 1 science worksheets on living and non-living things and the parts of plants and animals, with pictures. 100 questions with answers.",
           "Living things grow and change.", "They need food, water and air. Rocks and toys do not.",
           ("Living things grow, change and need food, water and air.", ["Plants and animals are living.", "Rocks, toys and water are not living.", "Living things make babies or seeds."]),
           [("Is a tree living?", ["It grows.", "It needs water."], "yes"), ("Is a rock living?", ["It does not grow."], "no")],
           ["Thinking things that move, like cars, are living.", "Thinking plants are not living because they do not walk."],
           [("How do we know something is living?", "It grows, changes, needs food, water and air, and can make more of its own kind."),
            ("Are people living things?", "Yes. People grow, eat, breathe and have babies, just like other animals.")],
           s_living, pic=K.row(["frog", "tree", "rock", "block"], words=["living", "living", "not living", "not living"], size=80, label="a frog, a tree, a rock and a block")),
        CU("B", 2, "needs-of-living-things", "B2.3, B2.4, B1.1",
           "Describe the needs of plants and animals, including humans; describe how living things depend on their environment "
           "and how people can care for living things.",
           "Needs of Living Things", "Needs of living things",
           "Free Grade 1 science worksheets on what plants, animals and people need to live, with pictures. 100 questions with answers.",
           "Living things need food, water and air.", "Animals need shelter too. Plants need sunlight and soil.",
           ("All living things need food, water and air.", ["Animals need shelter and space.", "Plants need sunlight, water and soil.", "People help pets and plants get what they need."]),
           [("What does a plant need?", ["light", "water"], "sunlight and water"), ("Where does a squirrel live?", ["in a tree"], "in a nest")],
           ["Thinking plants eat food like animals do.", "Thinking pets can look after themselves."],
           [("What do animals need?", "Food, water, air, shelter and space."),
            ("What do plants need?", "Sunlight, water, air, soil and space to grow.")],
           s_needs, pic=K.row(["sun", "drop", "plant", "nest"], words=["light", "water", "plant", "home"], size=80, label="sun, water, a plant and a nest")),
        CU("B", 3, "the-body-and-senses", "B2.5, B2.6, B1.2",
           "Identify the major parts of the human body and the five senses; describe how the senses help us learn and stay safe "
           "and how healthy habits keep our bodies strong.",
           "The Body and the Five Senses", "The body and senses",
           "Free Grade 1 science worksheets on body parts, the five senses and staying healthy, with pictures. 100 questions with answers.",
           "We learn with our five senses.", "Sight, hearing, smell, taste and touch help us learn and stay safe.",
           ("Our five senses help us learn about the world.", ["Eyes see, ears hear, the nose smells.", "The tongue tastes, the skin feels.", "Healthy food, sleep and play keep us strong."]),
           [("Which sense helps you hear a bell?", ["ears"], "hearing"), ("Why wash your hands?", ["germs"], "to stay healthy")],
           ["Thinking we only touch with our hands (our whole skin feels).", "Thinking senses cannot warn us of danger."],
           [("What are the five senses?", "Sight, hearing, smell, taste and touch."),
            ("How do senses keep us safe?", "We can smell smoke, hear a fire alarm and feel that something is hot.")],
           s_body, pic=K.row(["bell", "leaf", "spoon", "drum"], words=["hear", "touch", "taste", "listen"], size=80, label="a bell, a leaf, a spoon and a drum")),
        CU("C", 4, "energy-in-our-lives", "C1.1, C1.2, C2.1, C2.2",
           "Identify the Sun as Earth's main source of energy; describe how people and other living things use energy from food, "
           "electricity and fuels; describe ways to save energy.",
           "Energy in Our Lives", "Energy in our lives",
           "Free Grade 1 science worksheets on energy from the Sun, food, electricity and fuels, and saving energy, with pictures. 100 questions with answers.",
           "The Sun gives us light and heat.", "We get energy from food, and machines use electricity and fuel. We can save energy.",
           ("Energy makes things move, grow, light up and warm up.", ["The Sun gives Earth light and heat.", "Food gives us energy to move and grow.", "Turn off lights to save energy."]),
           [("Where does our energy come from?", ["we eat"], "food"), ("What does the Sun give us?", ["warm and bright"], "light and heat")],
           ["Thinking energy only comes from plugs.", "Thinking the Moon makes its own light."],
           [("What is energy?", "Energy is what makes things move, grow, light up or get warm."),
            ("How can we save energy?", "Turn off lights and screens, close doors in winter and walk or bike when we can.")],
           s_energy, pic=K.row(["sun", "flashlight", "wind", "hot"], words=["sun", "light", "wind", "heat"], size=80, label="sun, flashlight, wind and heat")),
        CU("D", 5, "objects-and-materials", "D2.1, D2.2, D1.1",
           "Identify materials that objects are made of; describe their properties (hard, soft, waterproof, bendy); explain why "
           "materials are chosen for objects; describe how to reduce, reuse and recycle.",
           "Objects and Materials", "Objects and materials",
           "Free Grade 1 science worksheets on materials, their properties and choosing the right material, with pictures. 100 questions with answers.",
           "Objects are made of materials.", "Wood, metal, plastic, glass and cloth each have their own properties.",
           ("Every object is made of one or more materials.", ["Materials can be hard, soft, bendy or waterproof.", "We pick materials that fit the job.", "We can reduce, reuse and recycle."]),
           [("Why is a raincoat plastic?", ["water cannot get through"], "it is waterproof"), ("Which is soft?", ["it is fluffy"], "wool")],
           ["Mixing up an object and the material it is made of.", "Thinking all metals are the same."],
           [("What is a material?", "What an object is made of, like wood, metal, plastic, glass or cloth."),
            ("Why do we recycle?", "So materials can be used again and we make less garbage.")],
           s_materials, pic=K.row(["spoon", "glass", "sock", "paper"], words=["metal", "glass", "cloth", "paper"], size=80, label="a spoon, a glass, a sock and paper")),
        CU("D", 6, "everyday-structures", "D2.3, D2.4, D1.2",
           "Describe structures in the environment, both natural and made by people; describe how structures support or protect; "
           "build and test simple structures.",
           "Everyday Structures", "Everyday structures",
           "Free Grade 1 science worksheets on natural and human-made structures, shelters and building with blocks, with pictures. 100 questions with answers.",
           "A structure holds or supports something.", "Nests, houses, tables and bridges are structures.",
           ("A structure is something built to hold, support or protect.", ["Animals build nests, webs and dams.", "People build houses, bridges and slides.", "A wide bottom keeps a tower standing."]),
           [("Is a nest a structure?", ["a bird built it to hold eggs"], "yes"), ("Which tower stands best?", ["wide bottom"], "the wide one")],
           ["Thinking only big buildings are structures.", "Thinking a tall, thin tower is the most stable."],
           [("What is a structure?", "Something built to hold, support or protect something, like a table, a nest or a house."),
            ("How can we make a tower stronger?", "Give it a wide bottom and put the heavy blocks at the bottom.")],
           s_struct, pic=K.row(["house", "nest", "block", "tree"], words=["house", "nest", "blocks", "tree"], size=80, label="a house, a nest, blocks and a tree")),
        CU("E", 7, "day-night-and-weather", "E2.1, E2.2, E2.3",
           "Describe changes in a day, including day and night and the position of the Sun; describe daily weather and how "
           "people and animals respond to it.",
           "Day, Night and Weather", "Day, night and weather",
           "Free Grade 1 science worksheets on day and night, the Sun in the sky and daily weather, with pictures. 100 questions with answers.",
           "The Sun lights the day.", "At night our side of Earth faces away from the Sun. Weather changes every day.",
           ("Every day has a morning, an afternoon, an evening and a night.", ["The Sun rises in the morning.", "At night we see the Moon and stars.", "Weather can be sunny, rainy, windy or snowy."]),
           [("When do we see stars?", ["the sky is dark"], "at night"), ("It is raining. What do you wear?", ["stay dry"], "a raincoat")],
           ["Thinking the Sun goes out at night.", "Thinking weather is the same every day."],
           [("Why do we have day and night?", "Earth spins. When our side faces the Sun it is day; when it faces away it is night."),
            ("What is weather?", "What the air and sky are like: sunny, cloudy, rainy, windy, snowy, hot or cold.")],
           s_daily, pic=K.row(["sun", "moon", "rain", "cloud"], words=["day", "night", "rain", "cloud"], size=80, label="sun, moon, rain and a cloud")),
        CU("E", 8, "the-four-seasons", "E2.4, E2.5, E1.1",
           "Describe the changes in each season in Ontario and how plants, animals and people adapt to seasonal changes.",
           "The Four Seasons", "The four seasons",
           "Free Grade 1 science worksheets on winter, spring, summer and fall in Ontario and how plants, animals and people change, with pictures. 100 questions with answers.",
           "Winter, spring, summer, fall.", "In each season the weather, plants and animals change, and so do the clothes we wear.",
           ("Ontario has four seasons: winter, spring, summer and fall.", ["Winter is cold and snowy; summer is hot.", "Leaves change colour and fall in the fall.", "Some animals sleep or fly south for winter."]),
           [("Which season comes after fall?", ["fall, then …"], "winter"), ("What do bears do in winter?", ["they rest"], "sleep in a den")],
           ["Thinking it is hot all year everywhere.", "Thinking all trees lose their leaves (pines stay green)."],
           [("What are the four seasons?", "Winter, spring, summer and fall."),
            ("How do animals get ready for winter?", "Some grow thick fur, some store food, some sleep all winter and some fly south.")],
           s_seasons, pic=K.row(["snow", "sprout", "sun", "leaf"], words=["winter", "spring", "summer", "fall"], size=80, label="snow, a sprout, the sun and a leaf")),
    ]
