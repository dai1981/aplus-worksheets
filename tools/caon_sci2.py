# -*- coding: utf-8 -*-
"""Ontario Science and Technology 2022, Grade 2 (B Growth and Changes in Animals, C Properties of Liquids and Solids,
D Simple Machines and Movement, E Air and Water in the Environment). Short sentences, a picture on top. Built by caon_sci.build."""
from caon_sci import CU
import sci_kids as K

US1Y, US1O, UK2Y, UK5L, AU3L = ("gen_us_science_g1_young_plants_and_animals", "gen_us_science_g1_parents_and_offspring",
                                "gen_uk_science_y2_animals_and_their_young", "gen_uk_science_y5_life_cycles", "gen_au_science_y3_life_cycles")
UK1G, UK1B, UK1C, UK2A = ("gen_uk_science_y1_animal_groups", "gen_uk_science_y1_animal_bodies",
                          "gen_uk_science_y1_carnivores_herbivores_and_omnivores", "gen_uk_science_y2_what_animals_need_to_survive")
USKH, US2H, USKW = "gen_us_science_gk_how_living_things_change_their_environment", "gen_us_science_g2_habitats_and_biodiversity", "gen_us_science_gk_where_plants_and_animals_live"
US2C, US2W, UK4S, US2M = ("gen_us_science_g2_heating_and_cooling", "gen_us_science_g2_solid_and_liquid_water",
                          "gen_uk_science_y4_solids_liquids_and_gases", "gen_us_science_g2_properties_of_materials")
UK5D, UK5S, UK2X = "gen_uk_science_y5_dissolving_and_solutions", "gen_uk_science_y5_separating_mixtures", "gen_uk_science_y2_changing_the_shape_of_materials"
USKP, USKM, AU1P, UK5M = ("gen_us_science_gk_pushes_and_pulls", "gen_us_science_gk_changing_speed_and_direction",
                          "gen_au_science_y1_pushes_and_pulls", "gen_uk_science_y5_levers_pulleys_and_gears")
UK4W, SG5W, USKC, USKE = "gen_uk_science_y4_the_water_cycle", "gen_sg_science_p5_the_water_cycle", "gen_us_science_gk_caring_for_earth", "gen_us_science_gk_weather"
US1W = "gen_us_science_g1_young_plants_and_animals"


MACH = [("a seesaw", "lever"), ("a shovel", "lever"), ("a bottle opener", "lever"), ("a broom", "lever"), ("a hockey stick", "lever"),
        ("a pair of scissors", "lever"), ("a nutcracker", "lever"), ("a crowbar", "lever"), ("a wheelchair ramp", "inclined plane"),
        ("a playground slide", "inclined plane"), ("a loading ramp on a truck", "inclined plane"), ("a sloped driveway", "inclined plane"),
        ("an axe blade", "wedge"), ("a knife", "wedge"), ("a doorstop", "wedge"), ("the tip of a nail", "wedge"), ("a snowplow blade", "wedge"),
        ("a jar lid", "screw"), ("a bottle cap that twists", "screw"), ("a light bulb base", "screw"), ("a drill bit", "screw"),
        ("a wood screw", "screw"), ("a wagon wheel", "wheel and axle"), ("a doorknob", "wheel and axle"), ("a bicycle wheel", "wheel and axle"),
        ("a steering wheel", "wheel and axle"), ("a rolling pin", "wheel and axle"), ("a skateboard wheel", "wheel and axle"),
        ("a flagpole rope", "pulley"), ("window blinds with a cord", "pulley"), ("a well bucket on a rope", "pulley"),
        ("a crane lifting steel", "pulley"), ("a clothesline you can roll", "pulley"), ("a sailboat rope", "pulley")]
PP = [("kicking a soccer ball", "a push"), ("opening a drawer", "a pull"), ("pulling a sled up a hill", "a pull"), ("pushing a swing", "a push"),
      ("closing a door by leaning on it", "a push"), ("pulling a wagon", "a pull"), ("throwing a snowball", "a push"), ("pulling weeds from a garden", "a pull"),
      ("pressing a doorbell", "a push"), ("pulling on a rope in tug-of-war", "a pull"), ("pushing a shopping cart", "a push"), ("opening a fridge door", "a pull"),
      ("hitting a puck with a stick", "a push"), ("pulling up your socks", "a pull"), ("shoving a box across the floor", "a push"), ("pulling a zipper up", "a pull"),
      ("rolling a ball to a friend", "a push"), ("picking an apple off a tree", "a pull"), ("pushing a stroller", "a push"), ("pulling a toy on a string", "a pull")]


def machines_pic():
    """four simple machines: lever (seesaw), ramp, wheel and axle, pulley"""
    ink, f = "#2b2b2b", "Arial, Helvetica, sans-serif"
    t = lambda x, y, w: "<text x='%d' y='%d' font-size='15' text-anchor='middle' font-family='%s' fill='%s'>%s</text>" % (x, y, f, ink, w)
    g = []
    g.append("<polygon points='50,78 40,95 60,95' fill='#c98f00'/><line x1='8' y1='70' x2='92' y2='86' stroke='%s' stroke-width='5'/>" % ink + t(50, 118, "lever"))
    g.append("<g transform='translate(100,0)'><polygon points='10,95 90,95 90,45' fill='#8fbf6f' stroke='%s' stroke-width='2'/><rect x='45' y='52' width='18' height='14' fill='#c0504d' transform='rotate(-32 54 59)'/>%s</g>" % (ink, t(50, 118, "ramp")))
    g.append("<g transform='translate(200,0)'><circle cx='50' cy='65' r='28' fill='none' stroke='%s' stroke-width='5'/><circle cx='50' cy='65' r='5' fill='%s'/><line x1='50' y1='65' x2='50' y2='37' stroke='%s' stroke-width='2'/><line x1='50' y1='65' x2='78' y2='65' stroke='%s' stroke-width='2'/>%s</g>" % (ink, ink, ink, ink, t(50, 118, "wheel")))
    g.append("<g transform='translate(300,0)'><line x1='20' y1='12' x2='80' y2='12' stroke='%s' stroke-width='4'/><line x1='50' y1='12' x2='50' y2='25' stroke='%s' stroke-width='3'/><circle cx='50' cy='35' r='11' fill='#dfe3e7' stroke='%s' stroke-width='3'/><line x1='39' y1='35' x2='39' y2='90' stroke='%s' stroke-width='2'/><line x1='61' y1='35' x2='61' y2='80' stroke='%s' stroke-width='2'/><rect x='52' y='80' width='18' height='14' fill='#4f81bd'/>%s</g>" % (ink, ink, ink, ink, ink, t(50, 118, "pulley")))
    return "<svg viewBox='0 0 400 125' width='400' height='125' role='img' aria-label='a lever, a ramp, a wheel and a pulley'>%s</svg>" % "".join(g)


def pushpull_pic():
    ink, f = "#2b2b2b", "Arial, Helvetica, sans-serif"
    t = lambda x, y, w: "<text x='%d' y='%d' font-size='16' text-anchor='middle' font-family='%s' fill='%s'>%s</text>" % (x, y, f, ink, w)
    a = lambda x1, x2: "<line x1='%d' y1='45' x2='%d' y2='45' stroke='#c0504d' stroke-width='5'/><polygon points='%d,35 %d,55 %d,45' fill='#c0504d'/>" % (x1, x2, x2, x2, x2 + (12 if x2 > x1 else -12))
    g = ["<rect x='70' y='25' width='50' height='40' fill='#c98f00' stroke='%s' stroke-width='2'/>" % ink, a(15, 58), t(70, 95, "push")]
    g.append("<g transform='translate(200,0)'><rect x='20' y='25' width='50' height='40' fill='#4f81bd' stroke='%s' stroke-width='2'/><line x1='70' y1='45' x2='95' y2='45' stroke='%s' stroke-width='2'/>%s%s</g>" % (ink, ink, a(100, 138), t(70, 95, "pull")))
    return "<svg viewBox='0 0 400 105' width='400' height='105' role='img' aria-label='a push and a pull'>%s</svg>" % "".join(g)


def s_cycles(X):
    pool = X.pool([
        ("What is the first stage in a frog's life cycle?", "an egg", ["a frog", "a tadpole with legs", "a froglet"], "Egg → tadpole → froglet → frog."),
        ("What does a caterpillar turn into?", "a butterfly or moth", ["a bird", "a frog", "a fish"], "It changes inside a chrysalis."),
        ("What is the stage between a caterpillar and a butterfly?", "a chrysalis (pupa)", ["an egg", "a tadpole", "a nest"], "The caterpillar changes inside."),
        ("What hatches from a robin's egg?", "a baby bird (chick)", ["a tadpole", "a caterpillar", "a kitten"], "Birds hatch from eggs."),
        ("Which animal is born alive, not from an egg?", "a puppy", ["a chick", "a turtle", "a frog"], "Mammals are usually born alive."),
        ("What does a tadpole grow into?", "a frog", ["a fish", "a snake", "a bird"], "Tadpoles grow legs and lose their tails."),
        ("What is a baby deer called?", "a fawn", ["a cub", "a kit", "a chick"], "Fawns have spots."),
        ("What is a baby bear called?", "a cub", ["a fawn", "a calf", "a duckling"], "Bear cubs are born in winter dens."),
        ("Which stage comes after the egg for a monarch butterfly?", "caterpillar (larva)", ["chrysalis", "adult butterfly", "seed"], "Egg → larva → pupa → adult."),
        ("Do baby animals look exactly like their parents?", "Some do and some do not.", ["They always look the same.", "They never look like them.", "Only birds do."], "A caterpillar looks very different from a butterfly."),
        ("How long does it take a human baby to grow into an adult?", "about 18 years", ["one week", "one month", "one day"], "People grow for many years."),
        ("Which animal changes a lot as it grows (metamorphosis)?", "a frog", ["a dog", "a horse", "a cat"], "Frogs change from tadpoles."),
    ])
    return [
        ("Life cycles", [(pool, 6), (X.gen(AU3L, "g_lc", n=6), 6), (X.gen(UK5L, "g_next", n=5), 5), (X.gen(UK5L, "g_stage"), 3)]),
        ("Babies and parents", [(X.gen(UK2Y, "g_baby", n=6), 6), (X.gen(US1O, "g_name", n=5), 5), (X.gen(US1Y, "g_match"), 5), (pool, 4)]),
        ("Growing up", [(X.gen(UK2Y, "g_human", n=6), 6), (X.gen(US1Y, "g_change"), 5), (X.gen(UK2Y, "g_like"), 5), (pool, 4)]),
        ("How parents help", [(X.gen(US1O, "g_why"), 6), (X.gen(US1O, "g_pick", n=6), 6), (X.gen(US1Y, "g_parent"), 4), (X.gen(US1O, "g_baby"), 4)]),
        ("Life cycle investigations", [(X.gen(UK2Y, "g_weigh", n=5), 5), (X.gen(UK5L, "g_time", n=4), 4), (X.B(UK2Y, "B5"), 4), (X.B(US1Y, "B5"), 3), (X.B(AU3L, "POOL1"), 4)]),
    ]


def s_groups(X):
    pool = X.pool([
        ("Which animal has feathers?", "a blue jay", ["a beaver", "a trout", "a frog"], "All birds have feathers."),
        ("Which animal has fur?", "a raccoon", ["a robin", "a snake", "a goldfish"], "Mammals have fur or hair."),
        ("Which animal has scales and lives in water?", "a fish", ["a bird", "a deer", "a rabbit"], "Fish have scales and gills."),
        ("Which animal is a reptile?", "a turtle", ["a moose", "a goose", "a frog"], "Reptiles have dry scaly skin."),
        ("Which animal has six legs?", "an ant", ["a spider", "a dog", "a worm"], "Insects have six legs."),
        ("Why does a duck have webbed feet?", "to help it swim", ["to help it climb trees", "to help it dig", "to keep it warm"], "Webbed feet push water."),
        ("Why does a moose have long legs?", "to walk through deep snow and water", ["to climb trees", "to fly", "to dig holes"], "Body parts help animals live."),
        ("How do Canada geese stay warm in cold weather?", "They have thick feathers.", ["They wear coats.", "They sit by a fire.", "They have no way to stay warm."], "Feathers trap warm air."),
        ("Which animal eats only plants?", "a rabbit", ["a wolf", "an owl", "a fox"], "Plant eaters are herbivores."),
        ("Which animal eats only meat?", "a wolf", ["a cow", "a deer", "a rabbit"], "Meat eaters are carnivores."),
        ("Which animal eats both plants and animals?", "a raccoon", ["a deer", "a horse", "a cow"], "Raccoons are omnivores."),
        ("How does a turtle protect itself?", "It hides in its hard shell.", ["It flies away.", "It changes colour.", "It roars."], "The shell is armour."),
    ])
    return [
        ("Animal groups", [(X.gen(UK1G, "g_group", n=6), 6), (X.gen(UK1G, "g_pick", n=6), 6), (pool, 5), (X.gen(UK1G, "g_feat"), 3)]),
        ("Animal body parts", [(X.gen(UK1B, "g_has", n=6), 6), (X.gen(UK1B, "g_job"), 5), (X.gen(UK1B, "g_legs"), 4), (pool, 5)]),
        ("What animals eat", [(X.gen(UK1C, "g_kind", n=6), 6), (X.gen(UK1C, "g_food", n=6), 6), (X.gen(UK1C, "g_pick"), 5), (pool, 3)]),
        ("Animals and their homes", [(X.gen(US2H, "g_home"), 6), (X.gen(US2H, "g_kinds"), 5), (X.gen(USKW, "g_where", n=5), 5), (pool, 4)]),
        ("Sorting animals", [(X.gen(UK1G, "g_trick"), 4), (X.B(UK1G, "B5"), 4), (X.B(UK1C, "B5"), 4), (X.gen(US2H, "g_compare"), 4), (X.gen(UK1G, "g_pic", n=4), 4)]),
    ]


def s_people(X):
    pool = X.pool([
        ("How do bees help people?", "They help plants make fruit and make honey.", ["They make milk.", "They build houses.", "They clean water."], "Bees pollinate flowers."),
        ("How do dogs help people?", "Some guide people who cannot see, and they keep us company.", ["They make honey.", "They lay eggs for breakfast.", "They make wool."], "Dogs are helpers and friends."),
        ("Which animal gives us wool?", "a sheep", ["a cow", "a chicken", "a pig"], "Wool is made into sweaters."),
        ("Which animal gives us eggs?", "a chicken", ["a horse", "a goat", "a cat"], "Chickens lay eggs."),
        ("How can people help animals in winter?", "fill a bird feeder", ["leave garbage out", "chase the birds", "cut down their trees"], "Food helps birds survive."),
        ("Why should you not feed bread to ducks?", "It is not healthy food for them.", ["Ducks do not eat.", "Bread makes them fly faster.", "Bread is their best food."], "Ducks need natural food."),
        ("What should you do if you find a baby bird on the ground?", "leave it alone or ask an adult to call a wildlife centre", ["take it home as a pet", "throw it in the air", "put it in a box forever"], "Its parents may be nearby."),
        ("How can people keep animals safe near roads?", "drive slowly and watch for animal crossing signs", ["drive very fast", "throw food on the road", "honk at all animals"], "Signs warn drivers."),
        ("Why should we not litter?", "Animals can get hurt or sick from garbage.", ["Animals like garbage.", "Garbage turns into food.", "It does not matter."], "Keep habitats clean."),
        ("How do people change animal homes when they build roads?", "They can cut animal homes in half.", ["They make more forests.", "They give animals more space.", "Nothing changes."], "People can plan to protect habitats."),
        ("What does a pet fish need?", "clean water and the right food", ["a dry bowl", "candy", "a warm blanket"], "Pets depend on us."),
        ("Why do farmers keep cows?", "for milk and other foods", ["for wool", "for eggs", "for honey"], "Many foods come from animals."),
    ])
    return [
        ("Animals help people", [(pool, 8), (X.gen(UK2A, "g_pet"), 6), (X.gen(UK2A, "g_pfood"), 6)]),
        ("Caring for animals", [(X.gen(UK2A, "g_need"), 6), (X.gen(UK2A, "g_scen"), 5), (pool, 6), (X.gen(UK2A, "g_order"), 3)]),
        ("Animals change their homes", [(X.gen(USKH, "g_how"), 6), (X.gen(USKH, "g_why"), 5), (X.gen(USKH, "g_pick", n=5), 5), (X.gen(USKH, "g_ev"), 4)]),
        ("People and animal homes", [(X.gen(USKH, "g_people"), 5), (X.gen(USKW, "g_people"), 4), (pool, 4), (X.gen(USKW, "g_why", n=2), 2), (X.gen(US2H, "g_home", n=5), 5)]),
        ("Watching animals", [(X.gen(US2H, "g_data", n=5), 5), (X.B(USKH, "B5"), 4), (X.B(UK2A, "B5"), 4), (X.gen(US2H, "g_text"), 4), (pool, 3)]),
    ]


def s_solids(X):
    pool = X.pool([
        ("Which one is a solid?", "a block of wood", ["milk", "juice", "water"], "Solids keep their shape."),
        ("Which one is a liquid?", "maple syrup", ["a rock", "a pencil", "an ice cube"], "Liquids flow and take the shape of their container."),
        ("What does a liquid do when you pour it into a new cup?", "It takes the shape of the cup.", ["It keeps its old shape.", "It turns into a rock.", "It disappears."], "Liquids flow."),
        ("Does a solid change shape when you put it in a different box?", "No. A solid keeps its shape.", ["Yes. It always melts.", "Yes. It flows.", "It turns into juice."], "Solids hold their shape."),
        ("Which liquid flows slowly?", "honey", ["water", "juice", "milk"], "Thick liquids flow slowly."),
        ("Which liquid flows fast?", "water", ["honey", "ketchup", "maple syrup"], "Thin liquids flow fast."),
        ("Which solid can be poured?", "sand", ["a brick", "a book", "a spoon"], "Tiny solid pieces can be poured."),
        ("What happens when you mix sand and water?", "The sand sinks to the bottom.", ["The sand disappears.", "The water turns into sand.", "The sand floats away."], "Sand does not dissolve."),
        ("What happens when you stir sugar into warm water?", "It dissolves and you cannot see it.", ["It floats on top.", "It turns into ice.", "It grows bigger."], "Sugar dissolves."),
        ("Which one floats on water?", "a cork", ["a stone", "a metal key", "a marble"], "Light objects can float."),
        ("Which one sinks in water?", "a coin", ["a leaf", "a cork", "a plastic duck"], "Heavy, small objects often sink."),
        ("What happens when oil is poured into water?", "The oil floats on top.", ["The oil sinks.", "The oil disappears.", "The water turns into oil."], "Oil and water do not mix."),
        ("Why must cleaning liquids be kept away from children?", "They can be harmful if swallowed or touched.", ["They are tasty.", "They are just water.", "They make you stronger."], "Look for warning symbols."),
        ("Which is a solid that can bend?", "a rubber band", ["a glass", "a brick", "a rock"], "Some solids are bendy."),
    ])
    return [
        ("Solid or liquid?", [(pool, 6), (X.gen(US2W, "g_state", n=6), 6), (X.gen(UK4S, "g_pick", n=5), 5), (X.gen(UK4S, "g_state", n=3), 3)]),
        ("Properties of liquids", [(pool, 8), (X.gen(UK4S, "g_prop"), 5), (X.gen(US2M, "g_which"), 4), (X.gen(US2M, "g_what", n=3), 3)]),
        ("Properties of solids", [(X.gen(US2M, "g_true"), 5), (X.gen(UK2X, "g_can"), 5), (X.gen(UK2X, "g_act"), 5), (pool, 5)]),
        ("Mixing solids and liquids", [(X.gen(UK5D, "g_sol"), 5), (X.gen(UK5D, "g_pick", n=5), 5), (X.gen(UK5S, "g_mix", n=5), 5), (pool, 5)]),
        ("Solid and liquid investigations", [(X.gen(US2M, "g_table", n=4), 4), (X.B(US2M, "B5"), 4), (X.B(UK4S, "B5"), 4), (X.B(US2W, "B5"), 4), (pool, 2), (X.gen(UK5D, "g_rate", n=4), 2)]),
    ]


def s_heat(X):
    pool = X.pool([
        ("What happens to ice when it gets warm?", "It melts into water.", ["It gets bigger.", "It turns into sand.", "It stays the same."], "Heat melts ice."),
        ("What happens to water in a freezer?", "It freezes into ice.", ["It boils.", "It disappears.", "It turns into juice."], "Cold makes water freeze."),
        ("What happens to chocolate in a hot car?", "It melts.", ["It freezes.", "It grows.", "It turns into milk."], "Heat melts many solids."),
        ("Can melted chocolate become solid again?", "Yes, if it cools down.", ["No, never.", "Only if you add water.", "Only in the Sun."], "Cooling makes it solid."),
        ("Can a cooked egg become raw again?", "No. Cooking changes it forever.", ["Yes, if you cool it.", "Yes, if you add water.", "Yes, if you shake it."], "Some changes cannot be undone."),
        ("What happens to a puddle on a hot sunny day?", "It dries up as the water goes into the air.", ["It gets bigger.", "It freezes.", "It turns into mud forever."], "Water evaporates."),
        ("Why does snow melt in the spring?", "The air gets warmer.", ["The snow gets tired.", "The Moon melts it.", "People melt it with hair dryers."], "Warm weather melts snow."),
        ("What makes maple sap turn into syrup?", "boiling it so much of the water goes into the air", ["freezing it", "mixing it with sand", "putting it in the dark"], "Heat changes sap to syrup."),
        ("What happens to an ice pop left on a table?", "It melts into a puddle.", ["It freezes harder.", "It grows bigger.", "It turns into a rock."], "Room air is warmer than the freezer."),
        ("How can you make butter melt faster?", "put it in a warm place", ["put it in the freezer", "cover it with snow", "put it in ice water"], "Heat speeds up melting."),
    ])
    return [
        ("Heating and cooling", [(X.gen(US2C, "g_hc"), 6), (X.gen(US2C, "g_pic"), 5), (pool, 5), (X.gen(US2C, "g_undo", n=4), 4)]),
        ("Melting and freezing", [(X.gen(US2C, "g_melt", n=6), 6), (X.gen(US2W, "g_pick", n=6), 6), (pool, 4), (X.gen(US2W, "g_where"), 4)]),
        ("Changes we can undo", [(X.gen(US2C, "g_undo", n=6), 6), (X.gen(UK2X, "g_back"), 6), (pool, 4), (X.B(US2C, "B1"), 4)]),
        ("Water in every season", [(X.gen(US2W, "g_season"), 6), (X.gen(US2W, "g_chart"), 4), (pool, 6), (X.B(US2W, "B1"), 4)]),
        ("Heating and cooling investigations", [(X.B(US2C, "B5"), 5), (X.gen(UK2X, "g_band", n=4), 4), (X.B(UK2X, "B5"), 4), (X.gen(US2C, "g_melt", n=6), 5), (pool, 2)]),
    ]


def s_machines(X):
    pool = X.pool([
        ("What is a simple machine?", "a tool that makes work easier", ["a kind of animal", "a toy that must be plugged in", "a type of food"], "Ramps, levers and wheels are simple machines."),
        ("Which simple machine is a ramp?", "an inclined plane", ["a wheel and axle", "a pulley", "a screw"], "A ramp is a sloping surface."),
        ("Why is it easier to push a wheelchair up a ramp than to lift it up stairs?", "A ramp lets you use less force over a longer path.", ["Ramps are shorter.", "Ramps have stairs.", "Ramps make it heavier."], "Ramps make lifting easier."),
        ("Which simple machine is a seesaw?", "a lever", ["a pulley", "a wedge", "a screw"], "A lever turns on a pivot."),
        ("Which simple machine is on the end of an axe?", "a wedge", ["a pulley", "a wheel", "a ramp only"], "Wedges split things apart."),
        ("Which simple machine lifts a flag up a flagpole?", "a pulley", ["a wedge", "a screw", "a lever"], "Pull down to lift up."),
        ("Which simple machine is a jar lid?", "a screw", ["a pulley", "a wedge", "a seesaw"], "The lid twists on threads."),
        ("Which simple machine helps a wagon roll?", "a wheel and axle", ["a wedge", "a screw", "a pulley"], "Wheels reduce friction."),
        ("Which tool is a lever?", "a bottle opener", ["a doorstop", "a ramp", "a ball"], "You push one end to lift the cap."),
        ("Why are knives sharp?", "A thin wedge edge cuts more easily.", ["To make them heavy", "To make them shiny", "To make them roll"], "Knife blades are wedges."),
        ("Which one has a wheel and axle?", "a doorknob", ["a nail", "a ramp", "a knife"], "Turning the knob turns the axle."),
        ("How does a wheelbarrow help a gardener?", "It is a lever with a wheel, so heavy loads are easier to move.", ["It makes soil lighter.", "It digs holes.", "It plants seeds."], "Wheelbarrows combine machines."),
        ("Which one is a pulley?", "a rope over a wheel on a well", ["a slide", "a stair", "a fork"], "Wells use pulleys to lift buckets."),
        ("Which simple machine is a playground slide?", "an inclined plane", ["a pulley", "a screw", "a wheel"], "A slide is a ramp."),
        ("Which simple machine holds two pieces of wood together?", "a screw", ["a pulley", "a ramp", "a wheel"], "Screws twist into wood."),
        ("Why do we put wheels on suitcases?", "Wheels make them easier to move.", ["Wheels make them heavier.", "Wheels keep them dry.", "Wheels make them smaller."], "Rolling is easier than dragging."),
        ("Which simple machine is a doorstop?", "a wedge", ["a pulley", "a wheel", "a lever"], "A wedge holds the door."),
        ("Which simple machine is the handle of a pencil sharpener you turn?", "a wheel and axle", ["a wedge", "a ramp", "a pulley"], "Turning the handle turns the axle."),
        ("Which simple machine is a shovel?", "a lever", ["a pulley", "a screw", "a wheel"], "You push down on the handle to lift the dirt."),
        ("Why is a long ramp easier than a short, steep ramp?", "You need less force to go up a gentle slope.", ["Long ramps are steeper.", "Short ramps have no slope.", "Long ramps make things heavier."], "Gentle slopes are easier."),
    ])
    mr = X.rows(MACH, "Which simple machine is %s?", "Which one is a %s?", extra=["magnet", "battery"])
    return [
        ("What are simple machines?", [(pool, 8), (mr, 8), (X.gen(UK5M, "g_mech", n=4), 4)]),
        ("Levers and wedges", [(mr, 10), (pool, 6), (X.gen(UK5M, "g_mech", n=4), 4)]),
        ("Wheels, pulleys and ramps", [(mr, 10), (pool, 5), (X.gen(USKM, "g_ramp"), 5)]),
        ("Machines around us", [(mr, 10), (pool, 4), (X.gen(UK5M, "g_mech", n=4), 4), (X.B(UK5M, "B1", drop=[r"\d N\b"]), 2)]),
        ("Testing machines", [(X.gen(USKM, "g_ramp", n=4), 4), (X.B(UK5M, "B5", drop=[r"\d N\b"]), 3), (pool, 5), (X.gen(USKM, "g_test"), 4), (mr, 4)]),
    ]


def s_move(X):
    pool = X.pool([
        ("What is a push?", "moving something away from you", ["moving something toward you", "making something stop by itself", "a kind of sound"], "You push a door open."),
        ("What is a pull?", "moving something toward you", ["moving something away from you", "a kind of light", "a kind of weather"], "You pull a wagon."),
        ("Which is a pull?", "opening a drawer", ["kicking a ball", "pushing a swing", "closing a door by pushing"], "You pull the drawer toward you."),
        ("Which is a push?", "kicking a soccer ball", ["pulling a sled", "opening a drawer", "pulling a rope"], "Your foot pushes the ball."),
        ("How can you make a toy car go faster?", "push it harder", ["push it softer", "do not push it", "put it in water"], "A bigger push makes it go faster."),
        ("How can a moving ball change direction?", "something pushes or hits it from the side", ["it stops by magic", "it gets colder", "it changes colour"], "Forces change direction."),
        ("Why is it harder to push a toy car on carpet than on a floor?", "Carpet is rough, so there is more rubbing.", ["Carpet is smooth.", "Floors are rough.", "The car is heavier on carpet."], "Rough surfaces slow things down."),
        ("Which object will roll down a ramp?", "a ball", ["a block", "a book", "a box"], "Round things roll."),
        ("Which object will slide but not roll?", "a block", ["a ball", "a marble", "a wheel"], "Flat sides slide."),
        ("A ball rolls down a steep ramp and a gentle ramp. Which is faster?", "the steep ramp", ["the gentle ramp", "they are the same", "neither moves"], "Steeper slopes make things go faster."),
        ("What makes a swing go higher?", "a bigger push", ["a smaller push", "no push", "a cold day"], "More force, more movement."),
        ("Why do cars have brakes?", "to slow down and stop", ["to go faster", "to turn on lights", "to make music"], "Brakes rub on the wheels."),
    ])
    pr = X.rows(PP, "Is %s a push or a pull?", None, extra=["neither, it is a sound", "neither, it is light"])
    return [
        ("Pushes and pulls", [(pr, 4), (pool, 2), (X.gen(USKP, "g_pp"), 6), (X.gen(USKP, "g_dir"), 4), (X.B(AU1P, "POOL1"), 4)]),
        ("Strong and gentle forces", [(X.gen(USKP, "g_strong", n=6), 6), (X.gen(USKM, "g_change"), 5), (X.gen(AU1P, "g_shape", n=5), 5), (pool, 4)]),
        ("Speed and direction", [(X.gen(USKM, "g_pick2", n=6), 6), (X.gen(USKM, "g_wall"), 4), (X.gen(USKM, "g_surf"), 6), (pool, 4)]),
        ("Rolling and sliding", [(pool, 6), (X.gen(USKM, "g_dist"), 4), (X.gen(USKM, "g_ramp", n=4), 4), (X.gen(USKP, "g_data", n=3), 2), (pr, 4)]),
        ("Movement investigations", [(pr, 4), (X.gen(USKP, "g_data", n=4), 2), (X.B(USKP, "B5"), 4), (X.B(USKM, "B5"), 4), (X.B(AU1P, "POOL5"), 4), (X.gen(USKM, "g_test", n=4), 4)]),
    ]


def s_air(X):
    pool = X.pool([
        ("Can we see air?", "No, but we can feel it move as wind.", ["Yes, it is blue.", "Yes, it is white.", "No, because there is no air."], "Air is all around us."),
        ("How do we know air takes up space?", "A balloon gets bigger when we blow air into it.", ["Air has a colour.", "Air makes noise.", "Air is heavy like a rock."], "Air fills the balloon."),
        ("What is wind?", "moving air", ["falling water", "a kind of cloud", "a type of rock"], "Wind can be gentle or strong."),
        ("Which one uses wind to work?", "a sailboat", ["a lamp", "a fridge", "a bike"], "Wind pushes the sail."),
        ("Why do living things need air?", "to breathe", ["to grow taller in a day", "to stay dry", "to make snow"], "Animals and plants need air."),
        ("What is water used for at home?", "drinking, cooking and washing", ["making rocks", "making the Sun shine", "nothing"], "We use water every day."),
        ("Where does the water in our taps come from?", "lakes, rivers or wells", ["the Moon", "the clouds only", "the store"], "In Ontario many towns use lake water."),
        ("What is rain?", "water falling from clouds", ["air falling from trees", "melted rocks", "ice from a freezer"], "Rain is part of the water cycle."),
        ("Where does a puddle go on a sunny day?", "The water goes into the air.", ["It sinks to the centre of Earth.", "It turns into sand.", "It goes to the Moon."], "Water evaporates."),
        ("Which form of water is snow?", "solid", ["liquid", "gas", "none"], "Snow is frozen water."),
        ("What makes clouds?", "tiny drops of water in the air", ["smoke from chimneys only", "cotton", "dust only"], "Clouds are made of water drops."),
        ("What happens to a kite when the wind blows?", "It flies up in the air.", ["It falls into a hole.", "It melts.", "It turns into a bird."], "Moving air pushes the kite."),
        ("Which one shows that the wind is blowing?", "tree branches moving", ["a still lake", "a rock on the ground", "a closed book"], "We see what wind moves."),
        ("Which one is a strong, dangerous wind?", "a tornado", ["a breeze", "a calm day", "a puff of air"], "Tornadoes are spinning winds."),
        ("Why do we hang wet clothes outside on a windy day?", "Moving air helps them dry faster.", ["Wind makes them wetter.", "Wind makes them colder only.", "Wind makes them heavier."], "Water evaporates faster in wind."),
        ("What happens to a balloon when you let the air out?", "It gets smaller.", ["It gets bigger.", "It turns into water.", "It stays the same."], "Air takes up space."),
        ("Which animal uses air to fly?", "a bird", ["a fish", "a worm", "a snail"], "Wings push on the air."),
        ("What is snow made of?", "frozen water", ["cotton", "sugar", "salt"], "Snowflakes are tiny ice crystals."),
        ("When does rain turn into snow?", "when the air is below freezing", ["when it is very hot", "at noon only", "when the Sun is out"], "Cold air freezes water drops."),
        ("What happens to the water in a lake on a hot day?", "Some of it goes up into the air.", ["It turns into sand.", "It freezes.", "It gets deeper."], "Water evaporates."),
        ("Why do we see our breath on a cold day?", "Water in our breath turns into tiny drops in the cold air.", ["Our breath is smoke.", "The air is dirty.", "Our breath is snow."], "Cold air makes the water vapour condense."),
        ("Which tool measures how much rain fell?", "a rain gauge", ["a thermometer", "a ruler for paper", "a clock"], "It collects rain."),
        ("Which tool shows which way the wind blows?", "a wind sock or weather vane", ["a thermometer", "a ruler", "a scale"], "It points with the wind."),
    ])
    return [
        ("Air all around us", [(pool, 8), (X.gen(USKE, "g_word", n=6), 6), (X.gen(USKE, "g_clue"), 6)]),
        ("Water in our lives", [(pool, 5), (X.gen(SG5W, "g_save", n=6), 6), (X.gen(US2W, "g_where", n=4), 4), (X.gen(US2W, "g_state", n=4), 3), (X.gen(US2W, "g_pick", n=4), 2)]),
        ("The water cycle", [(X.gen(UK4W, "g_name"), 6), (X.gen(UK4W, "g_next"), 6), (X.gen(UK4W, "g_eve"), 4), (pool, 4)]),
        ("Weather, wind and rain", [(X.gen(USKE, "g_wear"), 5), (X.gen(USKE, "g_temp", n=5), 4), (X.gen(USKE, "g_week", n=5), 4), (pool, 7)]),
        ("Air and water investigations", [(X.gen(UK4W, "g_dish", n=5), 5), (X.gen(UK4W, "g_dry"), 4), (X.B(UK4W, "B5"), 4), (X.B(USKE, "B5"), 4), (pool, 3)]),
    ]


def s_care(X):
    pool = X.pool([
        ("Which one makes the air dirty?", "smoke from cars and factories", ["trees", "flowers", "rain"], "Smoke pollutes the air."),
        ("How can we keep the air clean?", "walk, bike or take the bus", ["drive everywhere", "burn garbage", "leave cars running"], "Fewer cars, cleaner air."),
        ("Why do trees help the air?", "They give off oxygen and clean the air.", ["They make smoke.", "They make the air dirty.", "They use up all the air."], "Trees are good for air."),
        ("How can we save water?", "turn off the tap while brushing your teeth", ["let the tap run", "take very long showers", "water the sidewalk"], "Every drop counts."),
        ("Why should we not pour paint down the drain?", "It can pollute rivers and lakes.", ["It cleans the pipes.", "Fish like paint.", "It turns into water."], "Drains can lead to lakes."),
        ("What should you do with garbage at the beach?", "put it in a garbage can", ["leave it in the sand", "throw it in the lake", "bury it"], "Keep beaches clean."),
        ("Why is clean water important for fish?", "Fish need clean water to live.", ["Fish like dirty water.", "Fish do not need water.", "Fish make the water clean."], "Pollution can hurt fish."),
        ("Which one wastes water?", "leaving the hose on", ["fixing a leaky tap", "taking a short shower", "using a full dishwasher"], "Turn hoses off."),
        ("How can a school help clean water?", "pick up litter and keep it out of drains", ["throw garbage in the creek", "pour soap outside", "waste water"], "Clean schoolyards help lakes."),
        ("Many Indigenous peoples say water is sacred. What does this teach us?", "to respect and protect water", ["to waste water", "that water is not important", "to pollute lakes"], "Water is life."),
        ("What can you use instead of a plastic water bottle every day?", "a reusable water bottle", ["a new plastic bottle each time", "a paper bag", "a sock"], "Reusing makes less garbage."),
        ("Which choice helps keep a lake clean?", "pick up dog waste and litter", ["leave garbage on the beach", "wash a car next to the lake with soap", "pour oil on the ground"], "Rain washes waste into lakes."),
        ("Which one is a good way to reuse water?", "water plants with water from washing vegetables", ["pour it down the drain", "leave it in the Sun forever", "throw it on the road"], "Reusing saves water."),
        ("What can happen to birds if oil spills into water?", "Oil sticks to their feathers and they get cold and sick.", ["They swim faster.", "They grow new feathers.", "Nothing happens."], "Oil spills harm animals."),
        ("Why should we turn off the car engine while waiting?", "to keep smoke out of the air", ["to make the car faster", "to make it rain", "to keep the car dirty"], "Idling pollutes the air."),
        ("Which one keeps air cleaner in a city?", "parks with many trees", ["more cars", "more smoke", "burning leaves"], "Trees help clean the air."),
        ("What is a water treatment plant?", "a place that cleans water so it is safe to drink", ["a garden", "a swimming pool", "a fish farm"], "Ontario towns clean their water."),
        ("How can you save water when you wash your hands?", "turn off the tap while you scrub", ["let the tap run", "use lots of water", "wash for one hour"], "Turn the tap back on to rinse."),
        ("Why should we keep plastic out of lakes?", "Fish and birds can eat it and get sick.", ["Plastic is food for fish.", "Plastic makes water cleaner.", "Plastic melts in water."], "Plastic lasts a long time."),
        ("Which action makes less garbage?", "bring a reusable bag to the store", ["use a new plastic bag every time", "throw away good toys", "buy many plastic bottles"], "Less garbage, cleaner Earth."),
        ("What does a smoggy day mean?", "The air is dirty and hazy.", ["The air is very clean.", "It is snowing.", "It is a holiday."], "Smog is air pollution."),
        ("Why is it unsafe to drink water from a puddle?", "It may have germs and dirt.", ["It is too clean.", "It is too cold.", "It is made of air."], "Drink clean tap water."),
    ])
    return [
        ("Clean air", [(pool, 4), (X.gen(USKC, "g_help", n=6), 6), (X.gen(USKC, "g_better", n=4), 4), (X.gen(USKC, "g_prob", n=4), 4), (X.gen(USKH, "g_people", n=2), 2)]),
        ("Clean water", [(pool, 5), (X.gen(SG5W, "g_save", n=6), 6), (X.B(SG5W, "B1"), 5), (X.B(SG5W, "B2"), 4)]),
        ("Saving water", [(X.gen(USKC, "g_pick", n=6), 6), (pool, 4), (X.gen(USKC, "g_bin"), 4), (X.gen(USKC, "g_reuse"), 4), (X.B(SG5W, "B3"), 2)]),
        ("People, air and water", [(pool, 5), (X.B(USKC, "B1"), 5), (X.B(UK4W, "B1"), 5), (X.gen(USKH, "g_pick", n=5), 5)]),
        ("Caring for Earth", [(X.B(USKC, "B5"), 5), (X.B(SG5W, "B5"), 5), (pool, 4), (X.gen(USKC, "g_prob", n=4), 2), (X.gen(USKH, "g_how"), 4)]),
    ]


def UNITS():
    return [
        CU("B", 1, "animal-life-cycles", "B2.1, B2.2",
           "Describe the life cycles of animals, including insects, amphibians, birds and mammals; describe how animals grow and "
           "change and how parents care for their young.",
           "Animal Life Cycles", "Animal life cycles",
           "Free Grade 2 science worksheets on animal life cycles, babies and parents, and how animals grow, with pictures. 100 questions with answers.",
           "Animals are born, grow and have young.", "Some hatch from eggs; some change a lot as they grow, like frogs and butterflies.",
           ("Every animal has a life cycle: born, grow, have young.", ["Birds, turtles and frogs hatch from eggs.", "Most mammals are born alive.", "Frogs and butterflies change a lot as they grow."]),
           [("What does a tadpole become?", ["it grows legs"], "a frog"), ("What is a baby deer?", ["it has spots"], "a fawn")],
           ["Thinking all baby animals look like their parents.", "Thinking all animals hatch from eggs."],
           [("What is a life cycle?", "The stages of an animal's life: being born or hatching, growing up and having young."),
            ("What is metamorphosis?", "A big change in body shape as an animal grows, like a caterpillar becoming a butterfly.")],
           s_cycles, pic=K.row(["egg", "worm", "butterfly", "frog"], words=["egg", "larva", "adult", "frog"], size=80, label="an egg, a larva, a butterfly and a frog")),
        CU("B", 2, "animal-features-and-groups", "B2.3, B2.4",
           "Describe the features of animals and how they help them live; sort animals into groups (mammals, birds, fish, reptiles, "
           "amphibians, insects) and by what they eat.",
           "Animal Features and Groups", "Animal features and groups",
           "Free Grade 2 science worksheets on animal groups, body parts and what animals eat, with pictures. 100 questions with answers.",
           "Animal body parts help them live.", "Feathers, fur, fins and webbed feet each have a job. We sort animals into groups.",
           ("We can sort animals by their body parts and what they eat.", ["Birds have feathers; mammals have fur.", "Fish have fins; insects have six legs.", "Some eat plants, some eat meat, some eat both."]),
           [("Which group has feathers?", ["robins and geese"], "birds"), ("What does a wolf eat?", ["it hunts"], "meat")],
           ["Thinking bats are birds (they are mammals).", "Thinking spiders are insects (they have eight legs)."],
           [("What are animal groups?", "Mammals, birds, fish, reptiles, amphibians and insects are some groups of animals."),
            ("How do body parts help animals?", "Webbed feet help ducks swim, thick fur keeps bears warm and long legs help moose walk in snow.")],
           s_groups, pic=K.row(["bird", "fish", "frog", "bee"], words=["bird", "fish", "frog", "insect"], size=80, label="a bird, a fish, a frog and a bee")),
        CU("B", 3, "animals-and-people", "B1.1, B1.2, B2.5",
           "Describe ways animals help people and how people affect animals and their homes; identify ways to care for animals "
           "and their habitats.",
           "Animals and People", "Animals and people",
           "Free Grade 2 science worksheets on how animals help us, caring for pets and wild animals, and protecting animal homes, with pictures. 100 questions with answers.",
           "People and animals need each other.", "Animals give us food and help; we must care for pets and protect animal homes.",
           ("Animals help people, and people can help animals.", ["Bees help plants; dogs help people.", "Pets need food, water and care.", "Keep animal homes clean and safe."]),
           [("Which animal gives us wool?", ["it says baa"], "a sheep"), ("How can you help birds in winter?", ["food is hard to find"], "fill a bird feeder")],
           ["Thinking wild animals make good pets.", "Thinking litter does not hurt animals."],
           [("How do animals help people?", "They give us food like eggs and milk, materials like wool, help on farms and keep us company."),
            ("How can we help wild animals?", "Do not litter, leave baby animals alone, plant trees and flowers and drive carefully.")],
           s_people, pic=K.row(["dog", "bee", "bird", "house"], words=["dog", "bee", "bird", "home"], size=80, label="a dog, a bee, a bird and a house")),
        CU("C", 4, "solids-and-liquids", "C2.1, C2.2, C2.3",
           "Identify properties of solids and liquids; describe how liquids flow and take the shape of their container; describe "
           "what happens when solids and liquids are mixed.",
           "Solids and Liquids", "Solids and liquids",
           "Free Grade 2 science worksheets on solids, liquids, how liquids flow, floating and sinking and mixing, with pictures. 100 questions with answers.",
           "Solids keep their shape; liquids flow.", "Liquids take the shape of their container. Some solids dissolve in water.",
           ("Solids keep their shape. Liquids flow and take the shape of their container.", ["Rocks, blocks and ice are solids.", "Water, milk and syrup are liquids.", "Sugar dissolves in water; sand does not."]),
           [("Is milk a solid or a liquid?", ["it can be poured"], "a liquid"), ("Does sand dissolve?", ["it sinks"], "no")],
           ["Thinking sand is a liquid because it can be poured.", "Thinking dissolved sugar is gone."],
           [("What is the difference between a solid and a liquid?", "A solid keeps its own shape. A liquid flows and takes the shape of its container."),
            ("What does dissolve mean?", "A solid mixes into a liquid so you cannot see it, like sugar in water.")],
           s_solids, pic=K.row(["block", "drop", "ice", "glass"], words=["solid", "liquid", "solid", "liquid"], size=80, label="a block, a drop, ice and a glass of water")),
        CU("C", 5, "heating-and-cooling", "C2.4, C2.5, C1.1",
           "Describe how heating and cooling change solids and liquids, such as melting and freezing; identify changes that can "
           "and cannot be undone; describe uses of water in each season.",
           "Heating and Cooling", "Heating and cooling",
           "Free Grade 2 science worksheets on melting, freezing, heating and cooling and changes we can undo, with pictures. 100 questions with answers.",
           "Heat melts; cold freezes.", "Ice melts and water freezes. Some changes, like cooking an egg, cannot be undone.",
           ("Heating and cooling can change solids and liquids.", ["Warmth melts ice, butter and chocolate.", "Cold freezes water into ice.", "Cooking an egg cannot be undone."]),
           [("What happens to ice in the sun?", ["it gets warm"], "it melts"), ("Can melted chocolate be solid again?", ["cool it down"], "yes")],
           ["Thinking all changes can be undone.", "Thinking water disappears when a puddle dries (it goes into the air)."],
           [("What is melting?", "A solid turning into a liquid when it is heated, like ice turning into water."),
            ("What is freezing?", "A liquid turning into a solid when it gets very cold, like water turning into ice.")],
           s_heat, pic=K.row(["ice", "drop", "hot", "cold"], words=["ice", "water", "hot", "cold"], size=80, label="ice, water, hot and cold")),
        CU("D", 6, "simple-machines", "D2.1, D2.2, D1.1",
           "Identify the six simple machines (lever, inclined plane, wedge, screw, wheel and axle, pulley); describe how they make "
           "work easier; find simple machines in everyday objects.",
           "Simple Machines", "Simple machines",
           "Free Grade 2 science worksheets on levers, ramps, wedges, screws, wheels and pulleys in everyday objects, with pictures. 100 questions with answers.",
           "Simple machines make work easier.", "Levers, ramps, wedges, screws, wheels and pulleys help us lift, move and cut.",
           ("There are six simple machines.", ["Lever (seesaw), ramp, wedge (axe), screw (jar lid).", "Wheel and axle (wagon), pulley (flagpole).", "They help us push, pull and lift with less effort."]),
           [("Which machine is a seesaw?", ["it turns on a middle point"], "a lever"), ("Which machine raises a flag?", ["rope over a wheel"], "a pulley")],
           ["Thinking simple machines need electricity.", "Thinking a ramp makes the load lighter (it makes it easier to move)."],
           [("What are the six simple machines?", "Lever, inclined plane (ramp), wedge, screw, wheel and axle, and pulley."),
            ("How do simple machines help?", "They let us use less force to lift, move or split things.")],
           s_machines, pic=machines_pic()),
        CU("D", 7, "pushes-pulls-and-movement", "D2.3, D2.4, D1.2",
           "Describe pushes and pulls that make objects move, stop or change direction; describe how surfaces and ramps affect "
           "movement; design and test a moving toy.",
           "Pushes, Pulls and Movement", "Pushes, pulls and movement",
           "Free Grade 2 science worksheets on pushes and pulls, speed and direction, rolling and sliding and ramps, with pictures. 100 questions with answers.",
           "Pushes and pulls make things move.", "A bigger push makes things go faster; rough surfaces slow things down.",
           ("A push or a pull can start, stop or turn a moving object.", ["Push away, pull toward you.", "A harder push makes it go faster.", "Round things roll; flat things slide."]),
           [("Is opening a drawer a push or a pull?", ["toward you"], "a pull"), ("Which rolls: a ball or a block?", ["round"], "a ball")],
           ["Thinking things stop because they get tired.", "Thinking only people can push or pull (wind and water can too)."],
           [("What is the difference between a push and a pull?", "A push moves something away from you. A pull moves it toward you."),
            ("How can we make a toy car go farther?", "Push it harder, use a smooth floor or let it roll down a ramp.")],
           s_move, pic=pushpull_pic()),
        CU("E", 8, "air-and-water-in-the-environment", "E2.1, E2.2, E2.3",
           "Describe the properties of air and water; explain that air takes up space and moves as wind; describe how water "
           "changes and moves in the environment.",
           "Air and Water", "Air and water",
           "Free Grade 2 science worksheets on air, wind, water, rain, clouds and the water cycle, with pictures. 100 questions with answers.",
           "Air is all around us.", "Moving air is wind. Water falls as rain or snow, dries up and makes clouds.",
           ("Air and water are all around us.", ["We cannot see air, but we feel wind.", "Water can be liquid, solid ice or water vapour.", "Rain falls, puddles dry up, clouds form."]),
           [("What is wind?", ["air that moves"], "moving air"), ("Where does a puddle go?", ["sun warms it"], "into the air")],
           ["Thinking air is nothing.", "Thinking clouds are made of smoke or cotton."],
           [("How do we know air is real?", "We can feel wind, see a balloon fill up and see trees move."),
            ("What is the water cycle?", "Water goes up into the air, makes clouds, falls as rain or snow and flows back to lakes and rivers.")],
           s_air, pic=K.row(["wind", "cloud", "rain", "puddle"], words=["wind", "cloud", "rain", "puddle"], size=80, label="wind, a cloud, rain and a puddle")),
        CU("E", 9, "caring-for-air-and-water", "E1.1, E1.2, E2.4",
           "Assess how people use and affect air and water; identify ways to keep air and water clean and to save water, "
           "including Indigenous perspectives on water.",
           "Caring for Air and Water", "Caring for air and water",
           "Free Grade 2 science worksheets on clean air, clean water, pollution and saving water, with pictures. 100 questions with answers.",
           "Keep air and water clean.", "Walk or bike, do not litter and turn off the tap to protect air and water.",
           ("Living things need clean air and water.", ["Smoke makes air dirty; trees help clean it.", "Garbage and paint can pollute water.", "Turn off the tap to save water."]),
           [("How can we save water?", ["do not let it run"], "turn off the tap"), ("What makes air dirty?", ["cars and factories"], "smoke")],
           ["Thinking water will never run out.", "Thinking one person cannot help."],
           [("How can we keep water clean?", "Put garbage in the bin, never pour paint or oil down drains and pick up litter."),
            ("How can we keep air clean?", "Walk, bike or take the bus, plant trees and do not burn garbage.")],
           s_care, pic=K.row(["tree", "drop", "sun", "bird"], words=["tree", "water", "sun", "bird"], size=80, label="a tree, water, the sun and a bird")),
    ]
