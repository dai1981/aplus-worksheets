# -*- coding: utf-8 -*-
"""Class 4 EVS (NCERT Our Wondrous World, chapters 6–10): question makers and UNITS4b()."""
from uk_alsci import tq, once_maker
from in_sci import pairs, _R, U
from in_sci6a import odd_one, _cap
from in_sci4a import CO, LA, HW, TA, EN
from in_sci3a import kid

# =================================================================== Chapter 6: happy and healthy living
HAB = {"a healthy habit": ["brushing teeth twice a day", "washing hands with soap before eating", "sleeping early and getting up early", "playing outdoors every day",
                           "drinking clean water", "cutting nails regularly", "bathing every day", "covering the mouth while coughing", "doing yoga or stretching exercises", "eating fruits and vegetables every day", "keeping the toilet clean"],
       "an unhealthy habit": ["eating with dirty hands", "watching a screen late into the night", "skipping breakfast", "drinking water from a dirty pond",
                              "biting nails", "eating junk food every day", "sitting in one place all day", "sharing a towel with someone who has a skin infection", "playing in dirty, stagnant water", "staying up very late every night"]}
DIS = [("cholera", "drinking dirty water or eating contaminated food"), ("the common cold", "the coughs and sneezes of an infected person"),
       ("malaria", "the bite of an infected mosquito"), ("ringworm", "touching infected skin or sharing towels"), ("tooth decay", "eating sweets and not brushing"),
       ("typhoid", "drinking dirty water or eating contaminated food"), ("diarrhoea", "eating uncovered food that flies have sat on"), ("head lice", "sharing combs and caps")]
AID4 = [("a small cut", "wash it with clean water and cover it with a clean bandage"), ("a minor burn", "hold it under cool running water"), ("a nosebleed", "sit up, lean forward and pinch the soft part of the nose"),
        ("a bee sting", "remove the sting gently and put a cold cloth on it"), ("a twisted ankle", "rest it, put ice wrapped in cloth on it and keep the foot raised"),
        ("feeling dizzy in the hot sun", "sit in the shade and drink water slowly"),
        ("a splinter in the finger", "ask an adult to pull it out gently with clean tweezers"), ("a dog bite", "wash it well with soap and water and see a doctor at once")]
FEEL = [("you feel angry", "take deep breaths and count to ten"), ("you feel sad", "talk to a parent, teacher or friend"), ("a friend is left out of a game", "invite them to join in"),
        ("you feel worried before a test", "prepare a little each day and rest well"), ("someone is teasing a classmate", "tell a teacher and stand by the classmate"),
        ("you made a mistake", "say sorry and try to correct it"),
        ("you cannot understand a lesson", "ask the teacher to explain it again"), ("a friend is feeling lonely", "spend time with them and listen"),
        ("you have a disagreement with a friend", "talk calmly and listen to each other"), ("your team loses a game", "congratulate the winners and try again")]
HHQ = [("Why do we need sleep?", "sleep rests the body and mind and helps us grow", ["sleep makes us weak", "sleep is a waste of time", "sleep is only for babies"], "Children need about 9 to 11 hours."),
       ("How many hours of sleep do children of your age need each night?", "about 9 to 11 hours", ["about 3 hours", "about 18 hours", "no sleep at all"], "Go to bed at a fixed time."),
       ("Why should we exercise every day?", "it keeps the heart, muscles and bones strong", ["it makes us ill", "it weakens bones", "it is only for athletes"], "Play, run, cycle or do yoga."),
       ("Why should we wash our hands with soap?", "soap removes germs", ["soap adds germs", "water alone is always enough", "soap makes us sick"], "Wash for about 20 seconds."),
       ("When should we wash our hands?", "before eating and after using the toilet", ["only once a week", "only after eating", "never"], "Also after playing outside."),
       ("Why should we cover our mouth while coughing or sneezing?", "to stop germs spreading to others", ["to keep warm", "to look polite only", "to make the cough louder"], "Use a tissue or your elbow."),
       ("Why should we not stand in stagnant water?", "mosquitoes breed in it and it can carry germs", ["it is good for the skin", "it is very clean", "it makes us tall"], "Drain stagnant water near homes."),
       ("How can we stop mosquitoes breeding near our homes?", "do not let water collect in coolers, tyres and pots", ["keep water standing in tyres", "leave buckets open outside", "throw garbage in drains"], "Empty water containers often."),
       ("What does a vaccine do?", "it protects us from certain diseases", ["it makes us ill", "it is a kind of food", "it cleans the teeth"], "Children get vaccines at fixed ages."),
       ("Why should we not take medicines on our own?", "only a doctor knows the right medicine and dose", ["all medicines are the same", "medicines are sweets", "more is always better"], "Ask an adult."),
       ("Why should we sit and stand straight?", "good posture keeps the back healthy", ["it makes us short", "it hurts the back", "it does not matter"], "Carry your bag on both shoulders."),
       ("Why should we not read in very dim light?", "it strains the eyes", ["it makes the eyes stronger", "it helps us sleep", "it is the best light"], "Read in good light."),
       ("What is yoga?", "an Indian practice of postures and breathing that keeps the body and mind healthy", ["a type of food", "a computer game", "a sport played with a ball"], "International Yoga Day is on 21 June."),
       ("On which date is International Yoga Day celebrated?", "21 June", ["15 August", "2 October", "14 November"], "It began in 2015."),
       ("Why is it good to play outdoors?", "we get fresh air, sunlight and exercise", ["it makes us lazy", "outdoor air is harmful", "we stop growing"], "Sunlight helps the body make vitamin D."),
       ("Why should we keep our nails short and clean?", "dirt and germs collect under long nails", ["long nails make food tasty", "nails protect us from germs", "it does not matter"], "Cut them every week."),
       ("Why should we brush our teeth at night?", "food left in the mouth causes tooth decay", ["it makes teeth yellow", "brushing at night is harmful", "teeth do not need cleaning"], "Rinse after meals too."),
       ("What should be kept in a first-aid box?", "cotton, bandages, antiseptic and scissors", ["sweets and toys", "only water", "pencils and erasers"], "Keep one at home and at school."),
       ("Why should we not play with sharp objects?", "they can cut and injure us", ["they are soft", "they are toys", "they make us healthy"], "Use scissors carefully."),
       ("What should you do if a stranger offers you sweets and asks you to come along?", "say no, move away and tell a trusted adult", ["go with them", "take the sweets quietly", "keep it a secret"], "Never go with strangers."),
       ("Why is it important to share our feelings?", "talking helps us feel better and get help", ["feelings should always be hidden", "sharing makes us weak", "nobody listens"], "Talk to people you trust."),
       ("What is a good way to keep our surroundings clean?", "put waste in dustbins and keep drains clear", ["throw waste anywhere", "burn plastic", "let water stand"], "Clean surroundings mean fewer diseases."),
       ("Why should drinking water be boiled or filtered?", "to kill or remove germs", ["to make it salty", "to change its colour", "to waste fuel"], "Store it covered."),
       ("Why do we feel tired if we do not eat breakfast?", "the body has no fuel after the night", ["breakfast makes us tired", "we eat too much at night", "it is only habit"], "Eat a good breakfast."),
       ("What is the first thing to do if someone gets an electric shock?", "switch off the power before touching them", ["pull them with bare hands", "pour water on them", "run away"], "Call an adult and a doctor."),
       ("Why is laughing and playing with friends good for us?", "it keeps the mind happy and healthy", ["it makes us ill", "it wastes energy", "it is bad manners"], "Mental health matters too."),
       ("Why should we wear a helmet when cycling?", "it protects the head in a fall", ["it makes the cycle faster", "it keeps the hair tidy", "it is only for adults"], "Follow traffic rules."),
       ("Why should we not sit too close to the TV?", "it strains the eyes", ["it improves eyesight", "it makes pictures clearer", "it is good for the brain"], "Take breaks from screens."),
       ("Why is it important to take a bath every day?", "it removes sweat, dirt and germs from the skin", ["it makes the skin dirty", "it is not needed", "it causes colds"], "Wear clean clothes too."),
       ("Why should we chew our food well?", "it helps digestion", ["it slows the body", "it is bad for teeth", "it is not needed"], "Eat slowly."),
       ("Why should we keep our bedroom airy?", "fresh air keeps us healthy and helps us sleep well", ["closed rooms are healthier", "air carries no oxygen", "it makes us ill"], "Open windows in the day."),
       ("Why should we take a short break after an hour of study?", "the eyes and mind need rest to work well", ["breaks make us forget", "studying all day is best", "breaks are bad"], "Stretch and look far away."),
       ("Why do we sweat when we play in the sun?", "sweat cools the body", ["sweat heats the body", "sweat is a disease", "the Sun pours water on us"], "Drink water after playing."),
       ("Why should we not eat food sold uncovered by the roadside?", "flies and dust can make it carry germs", ["it is always cleaner", "it has more vitamins", "covered food is bad"], "Choose clean, covered food."),
       ("What is a balanced day for a child?", "time for study, play, rest, meals and sleep", ["only study", "only screen time", "only sleep"], "Make a simple timetable."),
       ("Why should a cut be covered with a clean bandage?", "it keeps dirt and germs out", ["it makes it bleed more", "it makes the cut bigger", "bandages are decoration"], "Change it when it gets dirty.")]


def c_sleep4(k=None):
    R = _R[0]
    n = kid()
    bed = R.choice([8, 9, 10])
    up = R.choice([5, 6, 7])
    h = 12 - bed + up
    mins = R.choice([0, 30])
    if mins:
        return tq("%s goes to bed at %d:30 p.m. and wakes up at %d:30 a.m. How many hours does %s sleep?" % (n, bed, up, n), "%d hours" % h,
                  ["%d hours" % x for x in (h - 1, h + 1, bed + up)], "From %d:30 p.m. to 12:30 a.m. is %d hours, and then %d more hours: %d hours." % (bed, 12 - bed, up, h))
    return tq("%s goes to bed at %d p.m. and wakes up at %d a.m. How many hours does %s sleep?" % (n, bed, up, n), "%d hours" % h,
              ["%d hours" % x for x in (h - 1, h + 1, bed + up)], "From %d p.m. to midnight is %d hours, and then %d more hours: %d hours." % (bed, 12 - bed, up, h))


# =================================================================== Chapter 7: how things work
SM = [("a see-saw", "a lever"), ("a pair of scissors", "a lever"), ("a pulley on a well", "a pulley"), ("a flagpole rope that raises the flag", "a pulley"),
      ("the wheels of a bullock cart", "a wheel and axle"), ("a door knob", "a wheel and axle"), ("a ramp for loading a truck", "an inclined plane"), ("a slide in a park", "an inclined plane"),
      ("an axe", "a wedge"), ("a knife", "a wedge"), ("the lid of a jar that is turned to close it", "a screw"), ("a bottle opener", "a lever"), ("a nutcracker", "a lever"), ("a ramp for wheelchairs", "an inclined plane"),
      ("the steering wheel of a bus", "a wheel and axle"), ("a crane lifting heavy loads", "a pulley"), ("a chisel", "a wedge"), ("a bolt", "a screw"), ("a staircase", "an inclined plane")]
SMQ = {"a lever": "lifts or moves a load by pressing on a bar that turns about a point", "a pulley": "lifts loads by pulling down on a rope over a wheel",
       "a wheel and axle": "turns on a rod so that loads roll along easily", "an inclined plane": "lets us push loads up a slope with less effort",
       "a wedge": "splits or cuts things with its thick-to-thin edge", "a screw": "holds things together tightly with its spiral groove"}
ELEC = {"a thing that needs electricity to work": ["a ceiling fan", "an electric bulb", "a mixer-grinder", "a television", "a refrigerator", "an electric iron", "a washing machine", "a mobile phone charger", "an electric kettle", "a computer"],
        "a thing that works without electricity": ["a bicycle", "a hand pump", "a pair of scissors", "a broom", "a mortar and pestle", "a pulley on a well", "a bullock cart", "a spinning top", "a sewing machine worked by a foot pedal", "a sundial"]}
WORK = [("a hand pump", "pushing the handle down pulls water up from under the ground"), ("a bicycle", "pushing the pedals turns the chain and the back wheel"),
        ("a pressure cooker", "steam trapped inside cooks food faster"), ("an earthen pot (matka)", "water seeping out and drying on its surface cools the water inside"),
        ("a solar cooker", "it traps the Sun's heat to cook food"), ("a windmill", "the wind turns its blades"), ("a torch", "cells send electricity to the bulb"),
        ("a water wheel (Persian wheel)", "animals turn a wheel that lifts pots of water"), ("a magnet in a compass", "the needle turns to point north"),
        ("a ceiling fan", "electricity turns a motor that spins the blades"), ("a weighing balance", "the side with the heavier load goes down"),
        ("a kite", "the wind pushes it up while we hold the string"), ("a sundial", "the shadow of a stick moves and shows the time")]
HWQ = [("What is a machine?", "a tool that makes our work easier", ["a kind of food", "a plant", "an animal"], "Machines can be simple or complex."),
       ("What is a simple machine?", "a machine with few or no moving parts, like a lever or a pulley", ["a machine that needs electricity", "a computer", "a car engine"], "There are six simple machines."),
       ("How many types of simple machines are there?", "six", ["two", "ten", "twenty"], "Lever, pulley, wheel and axle, inclined plane, wedge and screw."),
       ("Why do we use a ramp to load heavy drums onto a truck?", "it needs less effort than lifting them straight up", ["it needs more effort", "drums cannot be lifted", "ramps are faster for light things only"], "A ramp is an inclined plane."),
       ("Why do we use a pulley to draw water from a well?", "pulling down is easier than lifting up", ["it makes water cleaner", "it heats the water", "it needs electricity"], "A pulley changes the direction of the pull."),
       ("Why are wheels round?", "round wheels roll smoothly and easily", ["square wheels are faster", "round wheels stop easily", "for decoration only"], "Wheels reduce friction."),
       ("Why do we oil the moving parts of a bicycle?", "oil reduces friction so the parts move smoothly", ["oil makes it stop", "oil cleans the tyres", "oil makes it heavy"], "Less rubbing, less wear."),
       ("What is friction?", "a force that slows down things that rub against each other", ["a type of electricity", "a kind of wind", "a machine"], "Friction helps us walk too."),
       ("Why is it hard to walk on a wet, soapy floor?", "there is very little friction", ["there is too much friction", "the floor is too rough", "soap is heavy"], "Wear shoes with grip."),
       ("Why do we use electrical switches?", "to turn the flow of electricity on and off safely", ["to make electricity", "to store water", "to decorate walls"], "Use dry hands."),
       ("Why should we never touch a switch with wet hands?", "water lets electricity pass and can give a shock", ["wet hands stop electricity", "it is good for the switch", "it makes light brighter"], "Dry hands first."),
       ("Where does the electricity in a torch come from?", "the cells (batteries) inside it", ["the bulb", "the switch", "the air"], "Cells store energy."),
       ("Why should we switch off lights and fans when leaving a room?", "to save electricity", ["to waste electricity", "to make them work faster", "it does not matter"], "Saving electricity saves money and fuel."),
       ("What does a magnet attract?", "things made of iron", ["things made of plastic", "things made of wood", "things made of paper"], "Steel pins and iron nails stick to it."),
       ("Which direction does a freely hanging magnet point?", "north–south", ["east–west", "up–down", "any direction"], "That is how a compass works."),
       ("Why does a matka keep water cool in summer?", "water seeps out and evaporates from its surface, taking heat away", ["clay is cold", "it has ice inside", "the Sun cannot reach it"], "This is cooling by evaporation."),
       ("Which energy does a solar cooker use?", "the Sun's heat", ["electricity", "wind", "gas"], "It is a shiny box with a glass lid."),
       ("Why do we use a screwdriver?", "to turn screws in and out easily", ["to cut paper", "to hammer nails", "to boil water"], "Its handle is a wheel and axle."),
       ("Which part of a pair of scissors is the point about which the blades turn?", "the screw (pivot) in the middle", ["the tip of the blade", "the handle ring", "the paper"], "It is the fulcrum of the lever."),
       ("What do we call the fixed point on which a lever turns?", "the fulcrum", ["the load", "the effort", "the wheel"], "In a see-saw it is the middle."),
       ("Why does a heavy child sit closer to the middle of a see-saw?", "so that the see-saw balances", ["to go higher", "to make it break", "to slide off"], "Distance from the fulcrum matters."),
       ("Why are the blades of a knife sharp and thin?", "a thin edge cuts easily, like a wedge", ["sharp blades cannot cut", "to make it heavy", "for decoration"], "Handle knives carefully."),
       ("How does a hand pump bring up water?", "moving the handle lifts water from under the ground through a pipe", ["it makes rain", "it boils water", "it uses electricity"], "Many villages use hand pumps."),
       ("What makes a windmill turn?", "the wind pushing its blades", ["electricity", "water inside it", "sunlight only"], "Windmills can make electricity."),
       ("Why do roads on hills go round and round instead of straight up?", "a gentle slope (inclined plane) is easier to climb", ["straight roads are easier", "to waste time", "hills have no space"], "The longer path needs less effort."),
       ("Why does a bicycle stop when you press the brakes?", "the brake pads rub on the wheel and friction slows it", ["the chain breaks", "the tyres burst", "the bell rings"], "Brakes use friction."),
       ("Why do old buildings in hot places have thick walls and small windows?", "they keep the inside cool", ["they make the inside hotter", "to save space", "for decoration only"], "Thick walls slow heat."),
       ("Why should we not open a pressure cooker while it is still whistling?", "hot steam inside can burn us", ["the food will taste bad", "it saves gas", "nothing happens"], "Let it cool first."),
       ("Why do tyres have grooves on them?", "the grooves give grip by increasing friction", ["grooves make tyres slippery", "for decoration only", "to make them lighter"], "Worn-out tyres are dangerous."),
       ("Why is it easier to cut vegetables with a sharp knife than a blunt one?", "a sharp edge needs less force to cut", ["a blunt knife has a thinner edge", "sharp knives are heavier", "there is no difference"], "A knife is a wedge."),
       ("Why do we put a wedge-shaped stopper under a door?", "it holds the door still by friction", ["it makes the door close", "it oils the door", "it pulls the door"], "Wedges can hold things too."),
       ("Why does a ball rolling on grass stop sooner than one rolling on a smooth floor?", "grass causes more friction", ["grass has less friction", "the floor pulls the ball", "grass pushes the ball faster"], "Smooth surfaces have less friction.")]


# =================================================================== Chapter 8: how things are made
RAW = [("paper", "wood or bamboo pulp"), ("cotton cloth", "cotton from cotton plants"), ("a woollen sweater", "wool from sheep"), ("a silk sari", "threads from silkworm cocoons"),
       ("jaggery (gur)", "sugarcane juice"), ("butter", "cream from milk"), ("a clay pot", "clay"), ("glass", "sand"), ("a jute bag", "fibres of the jute plant"),
       ("a rubber band", "latex from rubber trees"), ("mustard oil", "mustard seeds"), ("atta (flour)", "wheat grains"), ("a coir rope", "coconut husk"), ("a cane chair", "cane (rattan) stems")]
SRC = {"made from plants": ["cotton cloth", "paper", "a jute bag", "a wooden table", "a coir mat", "a bamboo basket", "rubber slippers", "a cane chair"],
       "made from animals": ["a woollen shawl", "a silk sari", "ghee", "curd", "honey", "leather shoes"],
       "made from materials dug from the earth": ["a clay pot", "a glass bottle", "an iron nail", "a steel plate", "a copper pot", "a brick", "cement"]}
STEPS = [("cotton cloth", ["picking cotton", "removing the seeds", "spinning the cotton into thread", "weaving the thread into cloth"]),
         ("a clay pot", ["digging and cleaning clay", "kneading the wet clay", "shaping it on the potter's wheel", "drying it in the shade", "baking it in a kiln"]),
         ("jaggery", ["cutting sugarcane", "crushing it to get juice", "boiling the juice", "cooling the thick syrup into blocks"]),
         ("paper", ["cutting wood or bamboo", "making pulp with water", "spreading the pulp into thin sheets", "pressing and drying the sheets"]),
         ("butter", ["boiling milk", "collecting the cream", "churning the cream", "separating the butter from the buttermilk"]),
         ("a woollen sweater", ["shearing wool from sheep", "washing the wool", "spinning the wool into yarn", "knitting the yarn"]),
         ("silk", ["rearing silkworms on mulberry leaves", "collecting the cocoons", "unwinding the silk threads", "weaving the threads into cloth"])]


def c_steps4(k=None):
    R = _R[0]
    what, st = R.choice(STEPS)
    i = R.randrange(len(st) - 1)
    a = st[i + 1]
    other = sorted({x for _, s_ in STEPS for x in s_} - set(st))
    w = [x for x in st if x not in (a, st[i])] + R.sample(other, 2)
    return tq("In making %s, which step comes just after “%s”?" % (what, st[i]), a, R.sample(w, 3), "The steps are: " + "; ".join(st) + ".")


def c_first(k=None):
    R = _R[0]
    what, st = R.choice(STEPS)
    if R.random() < 0.5:
        other = sorted({x for _, s_ in STEPS for x in s_} - set(st))
        return tq("Which is the first step in making %s?" % what, st[0], st[1:3] + [R.choice(other)], "The steps are: " + "; ".join(st) + ".")
    return tq("Which is the last step in making %s?" % what, st[-1], st[:-1][-3:], "The steps are: " + "; ".join(st) + ".")


CRAFT4 = [("a potter", "pots and diyas from clay"), ("a weaver", "cloth on a loom"), ("a carpenter", "furniture from wood"), ("a blacksmith", "tools from iron"),
          ("a goldsmith", "jewellery from gold"), ("a cobbler", "shoes and sandals"), ("a basket maker", "baskets from bamboo and cane"), ("a tailor", "clothes from cloth"), ("a mason", "walls and houses from bricks and cement")]
HMQ = [("What is a raw material?", "the natural material from which something is made", ["the finished product", "a machine", "a shop"], "Cotton is the raw material for cloth."),
       ("What is a handloom?", "a machine worked by hand for weaving cloth", ["a machine for making paper", "a kind of pot", "a tool for cutting wood"], "Handloom saris are famous in many states."),
       ("Why do potters bake clay pots in a kiln?", "baking makes them hard and strong", ["baking makes them soft", "to change their shape", "to make them sweet"], "Unbaked pots crumble in water."),
       ("Why is a potter's wheel useful?", "it spins so the potter can shape round pots evenly", ["it bakes the pots", "it colours the pots", "it digs clay"], "It is turned by hand, foot or a motor."),
       ("What is spinning?", "twisting fibres together to make thread", ["weaving thread into cloth", "dyeing cloth", "cutting cloth"], "The charkha is a spinning wheel."),
       ("What is weaving?", "making cloth by crossing threads over and under each other", ["twisting fibres into thread", "cutting cloth", "knitting with needles only"], "Weaving is done on a loom."),
       ("Which spinning wheel did Mahatma Gandhi use and make famous?", "the charkha", ["the potter's wheel", "the Persian wheel", "the bicycle wheel"], "It is a symbol of self-reliance."),
       ("What is khadi?", "cloth that is hand-spun and hand-woven", ["cloth made only by big machines", "a kind of paper", "a type of pot"], "It is mostly cotton."),
       ("Why do we recycle paper?", "it saves trees, water and energy", ["it makes paper costly", "it wastes trees", "it is harmful"], "Old newspapers can be recycled."),
       ("Where do silkworms live and feed?", "on mulberry leaves", ["in ponds", "under the ground", "on cotton plants"], "Karnataka produces a lot of silk."),
       ("Which state of India is famous for producing the most silk?", "Karnataka", ["Rajasthan", "Punjab", "Ladakh"], "Mysore silk is well known."),
       ("Which animal gives us wool?", "the sheep", ["the cow", "the hen", "the fish"], "Yaks and camels also give wool."),
       ("What is the difference between handmade and machine-made things?", "handmade things are made by people with simple tools; machine-made things are made in factories", ["there is no difference", "handmade things are always made in factories", "machines are never used"], "Both are useful."),
       ("Why are clay pots good for the environment?", "they are made from natural material and break down easily", ["they are made of plastic", "they never break down", "they pollute water"], "Clay goes back to the soil."),
       ("Why do people buy handicrafts from local artisans?", "it supports their work and keeps traditional skills alive", ["handicrafts are useless", "it harms the artisans", "machines are always better"], "Melas sell many handicrafts."),
       ("Which material is used to make most bricks?", "clay or mud", ["glass", "wool", "sugar"], "The bricks are baked in a kiln."),
       ("Why is jaggery made by boiling sugarcane juice?", "boiling removes water and the juice thickens", ["boiling turns it into salt", "boiling makes it sour", "to make it cold"], "The thick syrup sets into blocks."),
       ("Which part of the coconut is used to make coir ropes and mats?", "the husk (outer fibre)", ["the water", "the white flesh", "the leaves only"], "Kerala is famous for coir."),
       ("Which famous painting style from Bihar uses natural colours?", "Madhubani", ["origami", "pottery", "embroidery from Japan"], "It was first painted on walls."),
       ("What is a kiln?", "a very hot oven for baking pots and bricks", ["a weaving machine", "a spinning wheel", "a cold storage room"], "It may use wood or coal."),
       ("What is dyeing?", "colouring cloth or thread", ["weaving cloth", "spinning thread", "cutting cloth"], "Natural dyes come from plants like indigo and turmeric."),
       ("Which plant gives a natural blue dye?", "indigo", ["mango", "neem", "rice"], "Turmeric gives yellow."),
       ("Why should we not waste things that are made with a lot of effort?", "making them uses raw materials, energy and people's hard work", ["they are free", "they grow back by themselves", "nobody made them"], "Reuse and repair."),
       ("Why do we churn curd or cream?", "to separate butter from the buttermilk", ["to make it cold", "to make it salty", "to make it into milk again"], "A wooden churner is called a mathani."),
       ("What do we call people who make things by hand with great skill?", "artisans or craftspeople", ["passengers", "patients", "tourists"], "Potters and weavers are artisans."),
       ("Why is glass made from sand heated to a very high temperature?", "sand melts and cools into glass", ["sand turns into water", "sand becomes wood", "sand becomes paper"], "Glass can be recycled."),
       ("Which machine is used to make cloth in large factories?", "a power loom", ["a potter's wheel", "a pulley", "a mortar and pestle"], "Handlooms are worked by hand.")]

# =================================================================== Chapter 9: different lands, different lives
LAND = [("the Thar Desert in Rajasthan", "hot, dry land with sand dunes and very little rain"), ("Ladakh", "a cold, high mountain desert with very little rain"),
        ("the coast of Kerala", "warm, wet land by the sea with many coconut trees"), ("the plains of Punjab", "flat, fertile land with rivers and fields of wheat"),
        ("Assam's Brahmaputra valley", "wet land with heavy rain, floods and tea gardens"), ("the Sundarbans in West Bengal", "a delta with mangrove forests and tigers"),
        ("the hills of Himachal Pradesh", "cool, hilly land with apple orchards and snow in winter"),
        ("the Western Ghats", "a long range of hills near the west coast with thick, rainy forests"), ("the Rann of Kutch in Gujarat", "a flat, salty white desert that floods in the monsoon"),
        ("Meghalaya", "hilly land that gets some of the heaviest rain in the world"), ("the Deccan Plateau", "high, flat land in the south with black soil good for cotton")]
HOUSE = [("houses on stilts (bamboo poles)", "they keep homes safe from floods and wild animals"), ("houses with sloping roofs", "rain and snow slide off easily"),
         ("houses with thick mud walls and small windows", "they stay cool in the hot desert sun"), ("houseboats", "people live on lakes and rivers"),
         ("flat-roofed houses", "there is little rain and the roof can be used for drying crops"), ("round mud huts with cone-shaped roofs (bhungas)", "they stand strong in earthquakes and stay cool")]
HOUSE2 = [("houses on bamboo stilts", "flood-prone parts of Assam"), ("houses with steep sloping roofs", "the rainy and snowy hills of Himachal Pradesh"),
          ("houses with thick mud walls and small windows", "the hot Thar Desert"), ("houseboats", "Dal Lake in Kashmir and the backwaters of Kerala"),
          ("bhungas (round mud huts)", "the Kutch region of Gujarat")]
PLACE_ANIMAL = [("the camel", "the Thar Desert"), ("the one-horned rhinoceros", "the grasslands of Assam"),
                ("the snow leopard", "the high Himalayas"), ("the Bengal tiger in mangroves", "the Sundarbans"), ("the Asiatic lion", "the Gir forest of Gujarat"),
                ("the Great Indian Bustard", "the dry grasslands of Rajasthan"), ("the wild ass", "the Little Rann of Kutch"), ("the red panda", "the forests of Sikkim and Arunachal Pradesh"),
                ("the Nilgiri tahr", "the hills of the Western Ghats")]
CLIM = {"suited to a cold place": ["woollen clothes", "houses with sloping roofs", "yaks", "thukpa (hot noodle soup)", "snow leopards", "pine trees", "a kangri (fire pot) in Kashmir", "thick blankets", "pashmina shawls"],
        "suited to a hot, dry place": ["loose cotton clothes", "camels", "houses with thick mud walls", "cactus plants", "a turban to shield the head from sun and sand", "storing water in tankas", "clay pots to keep water cool", "khejri trees", "the desert fox"]}
DLQ = [("Why do people in the desert wear loose, light-coloured clothes?", "they keep the body cool and protect it from the sun and sand", ["they keep the body warm", "they are cheaper", "for festivals only"], "Turbans protect the head too."),
       ("Why is the camel called the 'ship of the desert'?", "it can walk long distances on sand and go without water for days", ["it floats on water", "it is shaped like a ship", "it carries ships"], "Its wide, padded soles do not sink in sand."),
       ("Why do houses in Assam often stand on bamboo stilts?", "to keep them safe from floods", ["to look tall", "because bamboo is heavy", "to stay warm"], "Heavy rain causes floods there."),
       ("Why do houses in hilly areas have sloping roofs?", "so that rain and snow slide off", ["to collect snow", "to keep the house hot", "for decoration"], "Flat roofs would hold snow."),
       ("What is a tanka in Rajasthan?", "an underground tank for storing rainwater", ["a kind of camel", "a type of dance", "a sand dune"], "Water is precious in the desert."),
       ("Why is rice the main food in Kerala and West Bengal?", "these places get plenty of rain, which rice needs", ["rice grows only in deserts", "rice needs snow", "rice needs no water"], "Wheat is common in Punjab."),
       ("Which crop is grown widely in the plains of Punjab?", "wheat", ["tea", "coffee", "coconut"], "Punjab is called the granary of India."),
       ("Which crop grows on the hill slopes of Assam and Darjeeling?", "tea", ["wheat", "cotton", "sugarcane"], "Tea needs rain and slopes."),
       ("Why do people in Ladakh wear thick woollen clothes?", "Ladakh is very cold", ["Ladakh is very hot", "wool is cheap", "it is the fashion"], "Wool comes from sheep and yaks."),
       ("Why do people living by the sea often eat fish?", "fish are easily found in the sea nearby", ["fish grow on trees", "they cannot grow anything", "fish are imported only"], "Food depends on surroundings."),
       ("What is a houseboat?", "a boat in which people live", ["a house made of boats", "a bus", "a tent"], "Houseboats are found on Dal Lake and in Kerala's backwaters."),
       ("Where are the famous houseboats called shikaras and kettuvallams found?", "Kashmir and Kerala", ["Rajasthan and Gujarat", "Punjab and Haryana", "Ladakh and Sikkim"], "Shikaras are on Dal Lake."),
       ("Why do people in the desert have very few trees around them?", "there is very little rain", ["they cut all trees", "trees do not like sand", "it is too cold"], "Khejri and cactus can survive."),
       ("Why are many Indian festivals linked to harvests?", "people celebrate when crops are ready", ["harvests are sad times", "festivals stop farming", "there is no link"], "Pongal, Bihu, Baisakhi and Onam are harvest festivals."),
       ("Which harvest festival is celebrated in Assam?", "Bihu", ["Pongal", "Onam", "Baisakhi"], "Pongal is in Tamil Nadu."),
       ("Which harvest festival is celebrated in Kerala?", "Onam", ["Bihu", "Lohri", "Baisakhi"], "People make big flower designs (pookalam)."),
       ("Why do people living in different places speak different languages?", "each region has its own history and culture", ["they cannot hear each other", "languages grow on trees", "there is no reason"], "India has 22 scheduled languages."),
       ("What is a nomad?", "a person who moves from place to place with their animals", ["a person who never moves", "a city worker", "a sailor only"], "Some shepherds of the hills are nomads."),
       ("Why do some shepherds move their flocks up the mountains in summer?", "fresh grass grows there in summer", ["it is warmer at the top in winter", "sheep like snow", "the plains are flooded with snow"], "They come down before winter."),
       ("What is a sand dune?", "a hill of sand made by the wind", ["a type of tree", "a pond", "a house"], "Dunes keep shifting."),
       ("Why do people in very cold places eat hot soups and drinks?", "they keep the body warm", ["they cool the body", "they are cheaper", "they are sweet"], "Butter tea is drunk in Ladakh."),
       ("What do people in the Sundarbans use most to travel?", "boats", ["camels", "trains", "aeroplanes"], "It is a land of rivers and creeks."),
       ("What does 'unity in diversity' mean for India?", "people with different foods, clothes and languages live together as one country", ["everyone in India is the same", "regions do not meet", "people should not travel"], "Respect every culture."),
       ("Why do fishermen check the weather before going to sea?", "storms at sea are very dangerous", ["fish like storms", "it is a tradition only", "the sea is always calm"], "Weather warnings save lives."),
       ("Why do houses on the coast of Kerala have sloping roofs?", "Kerala gets very heavy rain", ["Kerala gets snow", "Kerala has no rain", "to store rain on the roof"], "Many roofs are tiled."),
       ("What kind of land is called a plain?", "large, flat land", ["a high mountain", "a deep sea", "a sandy desert only"], "Plains are good for farming."),
       ("Why do people in Rajasthan travel on camel carts?", "camels walk easily on sand and need little water", ["camels are fastest on roads", "cars are not allowed", "camels fly"], "Jeeps are also used now."),
       ("Why are many houses in Kerala built with tiled roofs?", "tiles let heavy rain run off and keep the house cool", ["tiles collect snow", "tiles make the house hot", "for decoration only"], "Clay tiles are made locally."),
       ("Which is the main crop grown in the rainy Brahmaputra valley and the delta of West Bengal?", "rice", ["wheat", "bajra", "apples"], "Rice needs plenty of water."),
       ("Which fruit is grown widely in the hills of Himachal Pradesh and Kashmir?", "apples", ["coconuts", "bananas", "dates"], "Apples need a cool climate."),
       ("Why do people in the Thar Desert grow bajra?", "bajra needs very little water", ["bajra needs floods", "bajra grows in snow", "bajra grows only in the sea"], "Bajra is a millet."),
       ("Why does Mawsynram in Meghalaya have so many green plants?", "it gets very heavy rain", ["it is a desert", "it never rains", "it is covered with snow"], "It is one of the wettest places on Earth."),
       ("Why is the Rann of Kutch white in winter?", "a layer of salt is left behind when the water dries", ["it is covered with snow", "it is painted", "it is made of cotton"], "The Rann Utsav is held there."),
       ("How do people in Ladakh save water in their cold, dry land?", "they use dry toilets and melt snow and ice for water", ["they waste water", "they have plenty of rain", "they buy water from the sea"], "Water is precious there."),
       ("Why do fishing families on the coast often build their houses on higher ground?", "to stay safe from high waves and storms", ["to be closer to the fish", "the sea is always calm", "to catch more rain"], "Cyclones can bring huge waves.")]

# =================================================================== Chapter 10: our sky
SKY = {"seen in the day sky": ["the Sun", "white fluffy clouds", "a rainbow", "a flock of birds", "a kite flying high", "a blue sky", "a jet's white trail", "sunlight shining through clouds", "a hot-air balloon"],
       "seen in the night sky": ["twinkling stars", "the Pole Star", "the Saptarishi (Big Dipper)", "a shooting star (meteor)", "fireflies near the trees", "the Milky Way on a very dark night", "the constellation Orion (Mriga)", "a satellite moving like a slow dot of light"]}
MOON = [("Amavasya", "the night when the Moon cannot be seen (new moon)"), ("Purnima", "the night of the full Moon"),
        ("the waxing Moon", "the Moon looking bigger each night after Amavasya"), ("the waning Moon", "the Moon looking smaller each night after Purnima")]
SKYOBJ = [("the Sun", "a star that gives us light and heat"), ("the Moon", "Earth's natural satellite that shines by reflecting sunlight"), ("the Pole Star (Dhruva Tara)", "a star that stays in the northern sky"),
("a constellation", "a group of stars that seems to make a pattern"), ("a meteor (shooting star)", "a streak of light made by a small rock burning up in the air"),
          ("an artificial satellite", "a machine sent by people to go around Earth"), ("Mars", "the red planet"), ("Saturn", "the planet with bright rings around it"),
          ("Jupiter", "the largest planet in our solar system"), ("the Milky Way", "our galaxy, a huge group of billions of stars")]
SIGN = [("dark, heavy clouds", "a sign that rain may come soon"), ("a red-orange sky at sunset", "caused by sunlight passing through a lot of air near the horizon"),
        ("a rainbow", "caused by sunlight shining through raindrops"), ("a ring (halo) around the Moon", "caused by thin, high clouds made of ice"),
        ("thick morning fog", "made of tiny water drops in cool air near the ground")]
MISSION = [("Chandrayaan-3", "the mission that landed near the south pole of the Moon in 2023"), ("Mangalyaan", "India's first mission to Mars"), ("Aryabhata", "India's first satellite, launched in 1975"),
           ("Aditya-L1", "the mission sent in 2023 to study the Sun"), ("Gaganyaan", "India's mission to send astronauts into space")]
SKQ = [("Why do we see the Sun rise in the east and set in the west?", "Earth spins from west to east", ["the Sun moves around Earth every day", "the Sun jumps across the sky", "the clouds push it"], "One spin takes 24 hours."),
       ("Why do we have day and night?", "Earth spins, so one side faces the Sun and the other side is in darkness", ["the Sun switches off", "the Moon covers the Sun every night", "clouds cover the Sun"], "Day is on the side facing the Sun."),
       ("How long does Earth take to spin once?", "about 24 hours", ["about one week", "about one month", "about one year"], "This gives one day and night."),
       ("How long does Earth take to go once around the Sun?", "about 365 days", ["about 24 hours", "about 30 days", "about 7 days"], "This is one year."),
       ("How long does the Moon take to go from one full Moon to the next?", "about 29 to 30 days", ["one day", "one year", "one week"], "That is about a month."),
       ("Why does the Moon shine?", "it reflects light from the Sun", ["it has its own fire", "it is a star", "it has electric lights"], "The Moon has no light of its own."),
       ("Why do stars seem to twinkle?", "their light is shaken as it passes through moving air", ["they switch on and off", "they are blinking eyes", "they are moving very fast"], "Planets twinkle much less."),
       ("Why can we not see stars during the day?", "the bright sunlight hides their faint light", ["stars go away in the day", "stars sleep in the day", "stars shine only at night"], "Stars are always there."),
       ("Why does the Sun look so much bigger than other stars?", "it is much closer to us than any other star", ["it is the biggest star in the universe", "other stars are tiny", "it is a planet"], "Other stars are very far away."),
       ("Which is the closest star to Earth?", "the Sun", ["the Pole Star", "the Moon", "Mars"], "The Moon is not a star."),
       ("Why should we never look directly at the Sun?", "its strong light can damage our eyes", ["it is too cold", "it makes us sleepy", "it is not bright"], "Use special filters to watch an eclipse."),
       ("Which star helped travellers find the north at night?", "the Pole Star (Dhruva Tara)", ["the Sun", "the Moon", "a shooting star"], "It stays almost still in the northern sky."),
       ("What is the Saptarishi?", "a group of seven bright stars in the northern sky", ["a planet", "a comet", "a type of cloud"], "It is also called the Big Dipper."),
       ("What is the Indian space agency called?", "ISRO (Indian Space Research Organisation)", ["NASA", "RBI", "BCCI"], "It is based in Bengaluru."),
       ("Which Indian mission landed near the south pole of the Moon in 2023?", "Chandrayaan-3", ["Mangalyaan", "Aryabhata", "Gaganyaan"], "Its lander was named Vikram."),
       ("What was the name of India's first satellite, launched in 1975?", "Aryabhata", ["Chandrayaan-3", "INSAT", "Mangalyaan"], "It was named after an ancient Indian astronomer."),
       ("Why do clouds form?", "water vapour in the air cools and turns into tiny drops", ["smoke rises from the Sun", "the wind brings cotton", "the Moon makes them"], "Dark clouds may bring rain."),
       ("When do we see a rainbow?", "when the Sun shines while it is raining or just after rain", ["at midnight", "only in winter fog", "only when it snows"], "Stand with your back to the Sun."),
       ("Why is the sky blue on a clear day?", "air scatters blue sunlight the most", ["the sea paints it", "the sky is made of blue glass", "the Moon is blue"], "Sunrise and sunset look orange."),
       ("Why does the Moon look different on different nights?", "we see different amounts of its sunlit half", ["the Moon breaks into pieces", "clouds cut it", "the Moon changes its size"], "These are the phases of the Moon."),
       ("Why do we see more stars in a village than in a big city?", "city lights and pollution make the sky too bright", ["there are no stars over cities", "villages are closer to stars", "city people sleep early"], "This is light pollution."),
       ("What is an astronaut?", "a person who travels into space", ["a person who studies rocks", "a sailor", "a pilot of buses"], "Rakesh Sharma was the first Indian in space."),
       ("Who was the first Indian to travel into space, in 1984?", "Rakesh Sharma", ["Kalpana Chawla", "C. V. Raman", "A. P. J. Abdul Kalam"], "He flew on a Soviet spacecraft."),
       ("Which planet do we live on?", "Earth", ["Mars", "Venus", "the Moon"], "It is the third planet from the Sun."),
       ("What do we call the shadow of the Moon falling on Earth that blocks the Sun?", "a solar eclipse", ["a lunar eclipse", "a full Moon", "a rainbow"], "In a lunar eclipse Earth's shadow falls on the Moon."),
       ("Why does a full Moon rise around sunset?", "it is on the opposite side of Earth from the Sun", ["the Moon follows the Sun", "it is a rule", "the clouds make it"], "So it lights up the whole night."),
       ("Which instrument helps us see far-off stars and planets clearly?", "a telescope", ["a magnifying glass", "a thermometer", "a compass"], "Galileo used one to see Jupiter's moons."),
       ("Why do the stars seem to move across the night sky?", "Earth is spinning", ["the stars are falling", "the wind blows them", "the Moon pushes them"], "Only the Pole Star seems almost still."),
       ("Why is it hotter at noon than in the early morning?", "the Sun is high in the sky and its rays fall straight down", ["the Sun is closer at noon", "the Moon is away", "clouds make heat"], "Shadows are short at noon."),
       ("When is your shadow shortest on a sunny day?", "around noon", ["early morning", "late evening", "at midnight"], "The Sun is highest then."),
       ("In which direction does your shadow fall in the morning?", "towards the west", ["towards the east", "straight up", "it has no direction"], "The Sun is in the east in the morning."),
       ("Why can we see the Moon during the day sometimes?", "it is bright enough to be seen when it is above the horizon", ["the Moon never sets", "the Sun turns into the Moon", "it is a cloud"], "Look for it in the morning or afternoon."),
       ("What is a galaxy?", "a huge group of billions of stars", ["a single planet", "a cloud of water", "a kind of satellite"], "We live in the Milky Way galaxy."),
       ("What do we call people who study the stars and planets?", "astronomers", ["farmers", "potters", "doctors"], "Aryabhata was a great Indian astronomer."),
       ("What does an astronaut wear in space?", "a spacesuit that gives air and protects the body", ["a raincoat", "a cotton kurta", "a woollen sweater"], "Space has no air to breathe.")]


def c_moon(k=None):
    R = _R[0]
    ph = ["new Moon (Amavasya)", "thin crescent", "half Moon", "nearly full Moon", "full Moon (Purnima)"]
    if R.random() < 0.5:
        i = R.randrange(len(ph) - 1)
        others = [x for x in ph if x not in (ph[i], ph[i + 1])]
        return tq("After Amavasya the Moon grows each night. Which shape comes just after the %s?" % ph[i], ph[i + 1], R.sample(others, 3), "New → crescent → half → nearly full → full.")
    i = R.randrange(1, len(ph))
    others = [x for x in ph if x not in (ph[i], ph[i - 1])]
    return tq("After Purnima the Moon shrinks each night. Which shape comes just after the %s?" % ph[i], ph[i - 1], R.sample(others, 3), "Full → nearly full → half → crescent → new.")


def c_days(k=None):
    R = _R[0]
    n = kid()
    SH = ["a thin crescent", "a half Moon", "a full Moon (Purnima)", "no Moon at all (Amavasya)"]
    k = R.choice(["same", "full", "half"])
    if k == "same":
        sh = R.choice(SH[:3])
        d = R.choice([29, 30])
        return tq("%s sees %s tonight. About %d days later, what will the Moon look like?" % (n, sh, d), sh, [x for x in SH if x != sh],
                  "The Moon repeats its shapes about every 29 to 30 days.")
    if k == "full":
        d = R.choice([14, 15])
        return tq("%s sees no Moon at all on Amavasya. About %d days later, what will the Moon look like?" % (n, d), SH[2], [SH[3], SH[0], SH[1]],
                  "The full Moon comes about 15 days after the new Moon.")
    d = R.choice([7, 8])
    return tq("%s sees no Moon at all on Amavasya. About %d days later, what will the Moon look like?" % (n, d), SH[1], [SH[2], SH[3], "the same as on Amavasya"],
              "The half Moon comes about a week after the new Moon.")


def UNITS4b():
    b = {k: once_maker(v) for k, v in [("hh", HHQ), ("hw", HWQ), ("hm", HMQ), ("dl", DLQ), ("sk", SKQ)]}
    hab = odd_one(HAB, "Which of these is %s?", "Which of these is not %s?")
    dis = pairs(DIS, "How does %s usually spread or start?", "Which problem is caused by %s?")
    aid = pairs(AID4, "What is the right first aid for %s?", "Which problem needs this first aid: %s?")
    feel = pairs(FEEL, "What is a good thing to do when %s?", "When is this a good thing to do: %s?")
    sm = pairs(SM, "Which simple machine is %s?")
    smq = pairs(sorted(SMQ.items()), "What does %s do?", "Which simple machine %s?")
    elec = odd_one(ELEC, "Which of these is %s?", "Which of these is not %s?")
    work = pairs(WORK, "How does %s work?", "Which of these works like this: %s?")
    raw = pairs(RAW, "What is %s made from?", "What is made from %s?")
    src = odd_one(SRC, "Which of these is %s?", "Which of these is not %s?")
    craft = pairs(CRAFT4, "What does %s make?", "Who makes %s?")
    land = pairs(LAND, "What is %s like?", "Which place is %s?")
    house = pairs(HOUSE, "Why do people build or use %s?")
    house2 = pairs(HOUSE2, "Where in India are %s found?", "Which kind of home is typical of %s?")
    pa = pairs(PLACE_ANIMAL, "Where does %s live in India?", "Which animal is found in %s?")
    clim = odd_one(CLIM, "Which of these is %s?", "Which of these is not %s?")
    sky = odd_one(SKY, "Which of these is %s?", "Which of these is not %s?")
    moon = pairs(MOON, "What is %s?", "What is the name for %s?")
    sobj = pairs(SKYOBJ, "What is %s?", "Which of these is %s?")
    sign = pairs(SIGN, "Which of these is true about %s in the sky?", "Which sky sight is %s?")
    mis = pairs(MISSION, "Which of these describes %s?", "Which is %s?")
    return [
        U(6, "happy-and-healthy-living", 6, HW,
          "Good habits for a healthy body and mind: cleanliness, exercise, yoga, sleep and rest; how some common diseases spread and how to prevent them; simple first aid; safety; sharing feelings and caring for each other (summary of NCERT Our Wondrous World Chapter 6).",
          "Happy and Healthy Living", "happy and healthy living",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 6: healthy habits, exercise and yoga, sleep, how diseases spread, first aid, safety and feelings. 100 questions with answers.",
          "Healthy habits keep the body and mind happy.", "Clean hands, exercise, rest and kind words.",
          "<p>We stay healthy by keeping clean, eating well, exercising, playing outdoors and sleeping for about 9 to 11 hours. Washing hands with soap, covering coughs, drinking clean water and not letting water stand near our homes stop many diseases. Cholera spreads through dirty water and malaria through mosquito bites.</p>"
          "<p>Simple first aid helps with small injuries: wash and cover a cut, cool a burn under running water. A happy mind matters too: share your feelings, include others and ask a trusted adult for help.</p>",
          [("A minor burn: what first?", ["cool it"], "hold it under cool running water"), ("Malaria spreads by…", ["an insect"], "the bite of an infected mosquito")],
          ["Thinking water alone removes germs from hands.", "Putting ice or butter on a burn.", "Hiding sad or angry feelings."],
          [("How can we stop mosquitoes breeding?", "Do not let water collect in coolers, tyres, pots and drains; empty and cover containers."),
           ("Why is sleep important?", "Sleep rests the body and mind and helps children grow and learn.")],
          lambda: [("Healthy habits", [(hab, 14), (b["hh"], 6)]), ("Keeping fit and resting", [(b["hh"], 10), (c_sleep4, 10)]), ("Diseases and prevention", [(dis, 12), (b["hh"], 4), (hab, 4)]),
                   ("First aid and safety", [(aid, 12), (b["hh"], 8)]), ("Feelings and friends", [(feel, 14), (hab, 6)])]),
        U(7, "how-things-work", 7, TA,
          "Simple machines (lever, pulley, wheel and axle, inclined plane, wedge and screw) and where we use them; friction; things that work with and without electricity; how a hand pump, bicycle, matka and solar cooker work; using electricity safely (summary of NCERT Our Wondrous World Chapter 7).",
          "How Things Work", "how things work",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 7: simple machines, friction, electricity and safety, and how a hand pump, bicycle, matka and solar cooker work. 100 questions with answers.",
          "Machines make our work easier.", "Levers, pulleys, wheels and slopes help us move loads.",
          "<p>Machines make work easier. Simple machines have few parts: a lever (see-saw, scissors) turns on a point called the fulcrum; a pulley (well) lets us pull down to lift up; a wheel and axle (cart) rolls loads; an inclined plane (ramp) lets us push loads up a slope; a wedge (axe) splits; a screw holds tightly.</p>"
          "<p>Friction slows things that rub; oil reduces it, brakes use it. Some things need electricity (fan, bulb, mixer), others do not (bicycle, hand pump). Never touch switches with wet hands, and switch off lights and fans to save electricity.</p>",
          [("A see-saw is…", ["it turns about the middle"], "a lever"), ("Why use a ramp?", ["less effort"], "an inclined plane makes lifting easier")],
          ["Calling every machine with a wheel 'electric'.", "Thinking friction is always bad.", "Touching switches with wet hands."],
          [("What are the six simple machines?", "Lever, pulley, wheel and axle, inclined plane, wedge and screw."),
           ("Why does a matka cool water?", "Water seeps through the clay and evaporates from the outside, taking heat away from the water inside.")],
          lambda: [("Machines around us", [(b["hw"], 10), (elec, 10)]), ("Simple machines", [(sm, 14), (smq, 6)]), ("Friction and motion", [(b["hw"], 12), (elec, 6), (smq, 2)]),
                   ("How things work", [(work, 14), (elec, 6)]), ("Mixed problems", [(elec, 10), (work, 6), (b["hw"], 4)])]),
        U(8, "how-things-are-made", 8, TA,
          "How things are made from raw materials obtained from plants, animals and the earth; steps in making cloth, clay pots, paper, jaggery, butter and silk; spinning, weaving and dyeing; artisans and handicrafts; reusing and recycling (summary of NCERT Our Wondrous World Chapter 8).",
          "How Things are Made", "how things are made",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 8: raw materials, things made from plants, animals and the earth, steps in making cloth, pots, paper and jaggery, and artisans. 100 questions with answers.",
          "Everything we use is made from raw materials.", "Plants, animals and the earth give us materials.",
          "<p>Things are made from raw materials. Plants give cotton, jute, wood and bamboo; animals give wool, silk, milk and honey; the earth gives clay, sand, iron and stone. Cotton is picked, cleaned, spun into thread and woven into cloth. Clay is kneaded, shaped on a potter's wheel, dried and baked in a kiln.</p>"
          "<p>Sugarcane juice is boiled to make jaggery; cream is churned to make butter; wood pulp is pressed into paper. Artisans such as potters, weavers and carpenters make things by hand. Reuse and recycle things, because making them uses materials, energy and hard work.</p>",
          [("Glass is made from…", ["heated until it melts"], "sand"), ("Just after spinning comes…", ["thread → cloth"], "weaving")],
          ["Mixing up spinning and weaving.", "Thinking paper comes from cotton.", "Thinking clay pots are baked before they are shaped."],
          [("What is the difference between spinning and weaving?", "Spinning twists fibres into thread; weaving crosses threads to make cloth."),
           ("Why are clay pots baked in a kiln?", "Baking makes the clay hard and strong so the pot does not crumble in water.")],
          lambda: [("Raw materials", [(raw, 14), (b["hm"], 6)]), ("From plants, animals and the earth", [(src, 16), (raw, 4)]), ("Steps in making things", [(c_steps4, 12), (c_first, 8)]),
                   ("Artisans and handicrafts", [(craft, 12), (b["hm"], 8)]), ("Mixed problems", [(b["hm"], 8), (src, 6), (c_steps4, 4), (c_first, 2)])]),
        U(9, "different-lands-different-lives", 9, EN,
          "Different kinds of land in India (deserts, mountains, plains, coasts, river valleys and deltas); how weather and land shape people's homes, food, clothes, work and transport; plants and animals of different regions; festivals and unity in diversity (summary of NCERT Our Wondrous World Chapter 9).",
          "Different Lands, Different Lives", "different lands, different lives",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 9: deserts, mountains, plains and coasts of India, and how land and weather shape homes, food, clothes and festivals. 100 questions with answers.",
          "Land and weather shape how people live.", "Homes, food and clothes suit each place.",
          "<p>India has deserts, high mountains, flat plains, long coasts and river deltas. People's lives suit their land and weather. In the hot Thar Desert, homes have thick mud walls, people wear loose clothes and camels carry loads. In cold Ladakh, people wear wool and keep yaks. In rainy Assam, houses stand on stilts.</p>"
          "<p>Food follows the land too: rice where there is a lot of rain, wheat in the plains of Punjab, fish along the coasts. Harvest festivals such as Bihu, Onam, Pongal and Baisakhi show unity in diversity.</p>",
          [("Houses on stilts are used…", ["floods"], "in places with heavy rain, such as Assam"), ("Camels suit…", ["sand and little water"], "the desert")],
          ["Thinking all of India has the same weather.", "Thinking deserts are always hot (Ladakh is a cold desert).", "Mixing up harvest festivals of different states."],
          [("Why do houses in hills have sloping roofs?", "So that rain and snow slide off instead of collecting on the roof."),
           ("What is a cold desert?", "A high, cold place with very little rain, such as Ladakh.")],
          lambda: [("Lands of India", [(land, 12), (b["dl"], 8)]), ("Homes for every place", [(house, 4), (house2, 7), (b["dl"], 9)]), ("Hot and cold places", [(clim, 16), (pa, 4)]),
                   ("Plants, animals and people", [(pa, 10), (b["dl"], 10)]), ("Mixed problems", [(clim, 12), (land, 6), (b["dl"], 2)])]),
        U(10, "our-sky", 10, EN,
          "The day and night sky: the Sun, the Moon and the stars; day and night and why the Sun seems to move; the changing shapes of the Moon; constellations and the Pole Star; clouds and rainbows; India in space (summary of NCERT Our Wondrous World Chapter 10).",
          "Our Sky", "our sky",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 10: the day and night sky, day and night, phases of the Moon, stars, the Pole Star, and India's space missions. 100 questions with answers.",
          "Earth spins, giving us day and night.", "The Moon shines with sunlight and changes shape.",
          "<p>In the day sky we see the Sun, clouds and sometimes a rainbow. The Sun is the nearest star. Earth spins once in about 24 hours, so the Sun seems to rise in the east and set in the west, and we get day and night. At night we see stars, constellations such as the Saptarishi, and the Pole Star, which shows the north.</p>"
          "<p>The Moon has no light of its own; it reflects sunlight. From Amavasya (new Moon) it grows to Purnima (full Moon) in about 15 days and shrinks again, repeating every 29 to 30 days. ISRO sent Chandrayaan-3 to the Moon in 2023.</p>",
          [("The Moon shines because…", ["no light of its own"], "it reflects sunlight"), ("About 15 days after Amavasya…", ["the Moon grows"], "full Moon (Purnima)")],
          ["Thinking the Sun moves around Earth each day.", "Calling the Moon a star.", "Thinking stars disappear in the day."],
          [("Why do we have day and night?", "Earth spins; the side facing the Sun has day and the other side has night."),
           ("Why does the Moon change shape?", "We see different amounts of its sunlit half as it goes around Earth.")],
          lambda: [("The day and night sky", [(sky, 15), (sign, 5)]), ("The Sun and Earth", [(b["sk"], 14), (sobj, 6)]), ("The Moon", [(moon, 6), (c_moon, 6), (c_days, 4), (b["sk"], 4)]),
                   ("Stars and space", [(sobj, 10), (mis, 7), (b["sk"], 3)]), ("Mixed problems", [(sky, 10), (b["sk"], 8), (sign, 2)])]),
    ]
