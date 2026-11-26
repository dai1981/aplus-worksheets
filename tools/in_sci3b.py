# -*- coding: utf-8 -*-
"""Class 3 EVS (NCERT Our Wondrous World, chapters 7–12): question makers and UNITS3b()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import odd_one, nq, _cap
from in_sci3a import FC, LA, WA, FH, TA, kid
import in_sci

# =================================================================== Chapter 7: water — a precious gift
WSRC = [("rain", "water that falls from the clouds"), ("a river", "water flowing from the mountains towards the sea"), ("a lake", "a large body of still water on land"),
        ("a pond", "a small body of still water"), ("a well", "a deep hole dug in the ground to reach water"), ("a hand pump", "a pump worked by hand to bring up underground water"),
        ("a tap", "a pipe outlet that brings water from a tank or the town supply"), ("a stepwell (baoli)", "an old well with steps going down to the water"),
        ("a spring", "water that flows out naturally from the ground"), ("a glacier", "a huge river of ice in high mountains"), ("a tank", "a large container or reservoir that stores water")]
WUSE = {"a way to save water": ["closing the tap while brushing", "using a bucket instead of a shower", "watering plants in the evening", "fixing a leaking tap",
                                "reusing water from washing vegetables for plants", "collecting rainwater", "washing the car with a bucket, not a hose", "taking only as much water as you will drink"],
        "a way to waste water": ["leaving the tap running while brushing", "washing the floor with a running hose", "letting the overhead tank overflow", "ignoring a dripping tap",
                                 "throwing away half a glass of drinking water", "playing with a running hose for fun", "washing a few clothes in a full machine", "bathing with many buckets of water"]}


def c_water(k=None):
    R = _R[0]
    k = k or R.choice(["bucket", "drip", "glass"])
    n = kid()
    if k == "bucket":
        b, m = R.choice([10, 12, 15, 20]), R.choice([2, 3, 4, 5])
        what = R.choice(["for a bath", "to wash clothes", "to water the garden", "to clean the floor"])
        return nq("%s uses %d buckets of water %s. Each bucket holds %d litres. How many litres of water is that?" % (n, m, what, b), b * m, [b + m, b * m + b, b * (m - 1), b], "litres",
                  "%d × %d = %d litres." % (m, b, b * m))
    if k == "drip":
        r, h = R.choice([1, 2, 3, 4]), R.choice([5, 6, 8, 10, 12])
        return nq("A leaking tap wastes %d litre%s of water every hour. How much water is wasted in %d hours?" % (r, "" if r == 1 else "s", h), r * h, [r + h, h, r * h + r, r * (h - 2)], "litres",
                  "%d × %d = %d litres. Fix leaking taps quickly!" % (r, h, r * h))
    g, d = R.choice([6, 7, 8, 9, 10]), R.choice([2, 3, 4, 7])
    return nq("%s drinks %d glasses of water a day. How many glasses is that in %d days?" % (n, g, d), g * d, [g + d, g * d + g, g, d], "glasses", "%d × %d = %d glasses." % (g, d, g * d))


WQ = [("Why is water called a precious gift?", "all living things need it and clean water is limited", ["it is useless", "it never runs out", "only plants need it"], "We must not waste it."),
      ("Where does most of our water first come from?", "rain", ["shops", "factories", "the Moon"], "Rain fills rivers, lakes and wells."),
      ("Why should we drink clean water?", "dirty water can make us ill", ["dirty water is tastier", "clean water is harmful", "water does not matter"], "Boil or filter water if needed."),
      ("Which illness can spread through dirty water?", "diarrhoea", ["a broken leg", "a toothache from sweets", "sunburn"], "Cholera and typhoid also spread this way."),
      ("How can we make water safe to drink at home?", "by boiling or filtering it", ["by adding mud", "by keeping it open in the sun with dust", "by adding salt only"], "Store it in a covered pot."),
      ("Why should drinking water be kept covered?", "to keep out dust, insects and germs", ["to make it hot", "to change its colour", "it does not matter"], "Use a ladle to take water out."),
      ("What is rainwater harvesting?", "collecting and saving rainwater for later use", ["throwing rainwater away", "making rain", "drinking sea water"], "Rainwater can be stored or sent into the ground."),
      ("Why is sea water not used for drinking?", "it is too salty", ["it is too sweet", "it is too cold", "it is too hot"], "Most of Earth's water is salty."),
      ("Which animals need water to live?", "all animals", ["only fish", "only cows", "no animals"], "Plants need water too."),
      ("What happens to plants without water?", "they dry up and die", ["they grow faster", "they turn blue", "they make more fruit"], "Water carries food in plants."),
      ("Who in many villages walks long distances to fetch water?", "often women and girls", ["nobody", "only shopkeepers", "only animals"], "Saving water helps them."),
      ("What is a stepwell?", "an old well with steps going down to the water", ["a new tap", "a water tank on a roof", "a swimming pool"], "Rani ki Vav in Gujarat is a famous stepwell."),
      ("Why do ponds dry up in summer?", "the heat makes the water evaporate and there is no rain", ["fish drink all the water", "the water turns into sand", "people steal it"], "The monsoon fills them again."),
      ("Why should we not throw waste into rivers?", "it makes the water dirty and harms fish and people", ["it cleans the river", "fish need waste", "it makes water sweet"], "Keep rivers clean."),
      ("What do we use water for at home?", "drinking, cooking, bathing, washing and cleaning", ["only for drinking", "only for plants", "for nothing"], "Water is needed every day."),
      ("Why do farmers need water?", "to grow crops", ["to make roads", "to make clothes", "to fly kites"], "Irrigation brings water to fields."),
      ("What is the main source of water in a hand pump?", "water under the ground", ["the clouds directly", "the sea", "a shop"], "This is called groundwater."),
      ("Which month brings the monsoon rains to most of India?", "around June to September", ["December only", "only January", "never"], "The monsoon fills rivers and wells."),
      ("Why is it good to water plants in the evening?", "less water evaporates in the cool evening", ["plants sleep in the morning", "it makes plants wet all night for fun", "water is cheaper at night"], "Morning is also fine."),
      ("Which of these does not need water?", "a stone", ["a tree", "a cow", "a child"], "All living things need water."),
      ("Why should we report a broken water pipe?", "a lot of clean water is wasted from it", ["it helps plants", "it fills the river", "it is fun to play with"], "Tell an adult or the water office."),
      ("What happens to water when it is very cold?", "it freezes into ice", ["it boils", "it turns into milk", "it disappears"], "Ice melts back into water when warm."),
      ("What forms clouds?", "tiny drops of water in the sky", ["smoke from factories", "cotton", "dust only"], "When they grow heavy, it rains."),
      ("How can a school save water?", "fix leaks, use water carefully and collect rainwater", ["keep taps open", "wash the ground with a hose daily", "fill tanks till they overflow"], "Every drop counts."),
      ("Why should we not waste even a little water?", "small amounts add up to a lot", ["water is unlimited", "a little does not matter", "water grows on trees"], "Close the tap fully.")]

# =================================================================== Chapter 8: food we eat
SRCF = {"food we get from plants": ["rice", "wheat", "dal", "spinach", "mango", "potato", "groundnuts", "sugar"], "food we get from animals": ["milk", "eggs", "honey", "curd", "paneer", "fish", "ghee"]}
COOK = [("idli", "steaming"), ("dhokla", "steaming"), ("momos", "steaming"), ("puri", "frying"), ("pakora", "frying"), ("samosa", "frying"), ("roti", "roasting on a tawa"),
        ("bhutta (corn on the cob)", "roasting on a fire"), ("rice", "boiling"), ("dal", "boiling"), ("bread", "baking"), ("cake", "baking")]
RAW = {"usually eaten raw": ["cucumber", "an apple", "a banana", "a guava", "carrot in a salad", "a coconut slice", "grapes"],
       "usually eaten cooked": ["rice", "rajma", "potatoes", "dal", "wheat flour (as roti)", "brinjal", "chickpeas (chana)"]}
REGF = [("Punjab", "makki di roti and sarson ka saag"), ("Gujarat", "dhokla"), ("Tamil Nadu", "idli and sambar"), ("Kerala", "appam and stew"), ("West Bengal", "maacher jhol (fish curry) with rice"),
        ("Rajasthan", "dal baati churma"), ("Bihar", "litti chokha"), ("Karnataka", "ragi mudde"), ("Odisha", "dalma"), ("Maharashtra", "puran poli"), ("Goa", "bebinca, a layered sweet"), ("Assam", "pitha")]
FOODQ = [("Why do we need food?", "to get energy, grow and stay healthy", ["only to pass time", "to feel sleepy", "to stop growing"], "Food is fuel for the body."),
         ("Why should we eat many kinds of food?", "different foods give us different things we need", ["one food is always enough", "to waste food", "to get ill"], "Eat grains, pulses, vegetables, fruits and milk."),
         ("Which of these gives us energy to play?", "rice and roti", ["water only", "salt only", "chilli only"], "Grains give energy."),
         ("Which food helps us grow strong?", "dal, milk and eggs", ["only sweets", "only chips", "only cold drinks"], "These build our body."),
         ("Why should we wash fruits and vegetables before eating?", "to remove dirt and germs", ["to make them sweet", "to make them bigger", "to change their colour"], "Wash them in clean water."),
         ("Why should we not waste food?", "many people do not get enough food and farmers work hard to grow it", ["food is unlimited", "wasting food is fun", "food grows by itself"], "Take only what you can eat."),
         ("What are millets?", "healthy grains such as ragi, jowar and bajra", ["sweets", "fruits", "fish"], "They need little water to grow."),
         ("Why should we eat less junk food?", "it has too much oil, sugar and salt", ["it is very healthy", "it builds bones", "it gives vitamins only"], "Choose fruits and home food."),
         ("Who grows the food we eat?", "farmers", ["shopkeepers only", "doctors", "drivers"], "We should thank farmers."),
         ("What does a cow eat?", "grass and hay", ["meat", "fish", "insects"], "It is a plant-eater."),
         ("What does a lion eat?", "other animals", ["grass", "fruits only", "leaves"], "It is a meat-eater."),
         ("Which animal eats both plants and small animals?", "a crow", ["a cow", "a goat", "a horse"], "Crows eat almost anything."),
         ("Why do we cook some foods?", "cooking makes them soft, tasty and safe to eat", ["cooking makes food raw", "to make food dirty", "cooking adds mud"], "Rice and dal must be cooked."),
         ("Which kitchen tool is used to make rotis?", "a rolling pin (belan) and a tawa", ["a broom", "a bucket", "a ladder"], "The tawa is heated."),
         ("Why should we wash our hands before eating?", "to remove germs that can make us ill", ["to make food taste salty", "to waste water", "it is not needed"], "Use soap and water."),
         ("Why do people in different regions eat different food?", "different crops grow in different places", ["everyone eats the same food", "food is not grown anywhere", "people choose randomly"], "Coastal areas eat more fish."),
         ("What is a balanced meal?", "a meal with grains, dal, vegetables and something like curd or milk", ["a meal of only sweets", "a meal of only chips", "a meal of only water"], "A thali is often balanced."),
         ("Why do we store grains in closed containers?", "to keep away insects, rats and moisture", ["to make them grow", "to make them cold", "to make them wet"], "Neem leaves are sometimes kept in grain."),
         ("Why should we not eat food that smells bad?", "it may be spoilt and make us ill", ["it is healthier", "it tastes better", "it is fresh"], "Throw away spoilt food."),
         ("Which food comes from the sea?", "fish", ["rice", "wheat", "apples"], "Fishermen catch fish in boats."),
         ("What do we call food made by grinding wheat?", "atta (wheat flour)", ["sugar", "salt", "oil"], "Atta is used for roti."),
         ("Why do we chew food well?", "so that it is easy to swallow and digest", ["to make it sweet", "to make it disappear", "to make it hot"], "Chew slowly."),
         ("Which of these is a fruit?", "a mango", ["a potato", "a carrot", "an onion"], "Mango is the national fruit of India."),
         ("What is the national fruit of India?", "the mango", ["the banana", "the apple", "the orange"], "India grows many kinds of mangoes."),
         ("Why do we eat sprouts?", "they are full of nutrients and help us grow", ["they are sweets", "they have no nutrients", "they make us sleepy"], "Moong sprouts are easy to make."),
         ("Which drink is good for growing children?", "milk", ["cold drinks", "tea all day", "coffee"], "Milk has calcium for bones."),
         ("Why should we not eat while watching a screen?", "we may eat too much without noticing", ["food tastes better", "it helps digestion", "it is healthy"], "Eat slowly and mindfully."),
         ("What is a thali?", "a big plate with small bowls of different foods", ["a type of fruit", "a cooking stove", "a drink"], "It has many items together.")]

# =================================================================== Chapter 9: staying healthy and happy
HAB = {"a healthy habit": ["brushing teeth twice a day", "washing hands before eating", "bathing every day", "sleeping early", "playing outdoors", "drinking enough water",
                           "cutting nails regularly", "eating fruits and vegetables", "sitting straight while reading"],
       "an unhealthy habit": ["eating junk food every day", "biting nails", "staying up late at night", "skipping breakfast", "eating without washing hands", "sitting all day watching a screen",
                              "drinking very little water", "eating too many sweets", "reading in dim light"]}
SAFE9 = [("you see a wire with no cover", "do not touch it and tell an adult"), ("you are crossing a road", "look right, left and right again, and use the zebra crossing"),
         ("a stranger asks you to come with them", "say no and go to a trusted adult"), ("you see medicine bottles at home", "never take them without an adult"),
         ("the floor is wet", "walk carefully so you do not slip"), ("you are riding a bicycle", "wear a helmet and ride on the side of the road"),
         ("there is a fire", "move out quickly and call for help"), ("you are near a well or pond", "stay away from the edge"),
         ("you feel sad or worried", "talk to a parent or teacher"), ("you play in the hot sun", "wear a cap and drink water"), ("you see a sharp knife on the table", "do not play with it"),
         ("you travel in a car", "wear a seat belt")]
EXER = [("yoga", "flexibility and a calm mind"), ("running", "a strong heart and lungs"), ("skipping", "strong legs and good balance"), ("swimming", "exercising the whole body"),
        ("cycling", "strong leg muscles"), ("playing football", "fitness and teamwork"), ("deep breathing", "relaxing the body"), ("stretching", "loosening tight muscles")]
AID = [("a small cut", "wash it with clean water and cover it with a clean bandage"), ("a nosebleed", "sit up, lean forward and pinch the soft part of the nose"),
       ("a small burn", "hold it under cool running water"), ("an ant bite", "wash it and apply a cold cloth"), ("a twisted ankle", "rest it and put a cold cloth on it"),
       ("dust in the eye", "wash the eye gently with clean water without rubbing")]


def c_sleep(k=None):
    R = _R[0]
    n = kid()
    b = R.choice([8, 9, 10])
    w = R.choice([5, 6, 7])
    h = (12 - b) + w
    if R.random() < 0.6:
        return nq("%s goes to bed at %d p.m. and wakes up at %d a.m. How many hours does %s sleep?" % (n, b, w, n), h, [w + b, h - 1, h + 1, 12 - w], "hours",
                  "From %d p.m. to 12 midnight is %d hours, and from midnight to %d a.m. is %d hours: %d hours in all." % (b, 12 - b, w, w, h))
    m = R.choice([20, 30, 40, 45])
    d = R.choice([3, 4, 5, 6])
    return nq("%s plays outdoors for %d minutes every day. How many minutes is that in %d days?" % (n, m, d), m * d, [m + d, m * d + m, m * (d - 1), m], "minutes", "%d × %d = %d minutes." % (m, d, m * d))


HQ3 = [("Why should we brush our teeth twice a day?", "to keep teeth clean and stop tooth decay", ["to make teeth yellow", "to make them loose", "it is not needed"], "Brush in the morning and at night."),
       ("Why should we wash hands with soap?", "soap removes germs", ["soap adds germs", "soap makes hands dirty", "water alone removes all germs"], "Wash for about 20 seconds."),
       ("Why is sleep important?", "the body rests and grows during sleep", ["sleep makes us weak", "sleep is a waste", "we grow only when awake"], "Children need about 9–11 hours."),
       ("Why should we play outdoors?", "it makes our body strong and keeps us happy", ["it makes us ill", "it is boring", "it weakens bones"], "Fresh air and sunlight are good for us."),
       ("Why should we cut our nails?", "dirt and germs collect under long nails", ["long nails look nice", "nails make food tasty", "it is not needed"], "Keep nails short and clean."),
       ("Why should we not read in dim light?", "it strains our eyes", ["it makes eyes stronger", "it saves electricity only", "it is good for eyes"], "Read in good light."),
       ("Why should we sit straight while reading and writing?", "it keeps our back healthy", ["it makes us tired", "it hurts the eyes", "it is not needed"], "Good posture matters."),
       ("What should we do when we feel angry?", "take deep breaths and talk about it", ["hit someone", "break things", "shout at friends"], "Feelings are normal; we can handle them well."),
       ("What makes us feel happy?", "playing with friends, helping others and spending time with family", ["being alone always", "fighting", "eating only sweets"], "Happiness is part of health."),
       ("Why should we cover our mouth when we sneeze?", "to stop germs spreading to others", ["to keep warm", "to stop the sneeze", "to look funny"], "Use a handkerchief or your elbow."),
       ("Why should we keep our surroundings clean?", "dirt attracts flies and mosquitoes that spread diseases", ["dirt is healthy", "flies are helpful", "it does not matter"], "Use dustbins."),
       ("Why should we not share our toothbrush?", "germs can pass from one person to another", ["it is fun to share", "it makes teeth stronger", "brushes are free"], "Everyone needs their own."),
       ("Why should we wear clean clothes?", "dirty clothes can cause skin problems", ["dirty clothes are healthier", "clean clothes are harmful", "it does not matter"], "Change after sweating."),
       ("Why should we drink clean water often?", "the body needs water to work well", ["water makes us weak", "only plants need water", "water is unhealthy"], "Drink more on hot days."),
       ("Why should we not run in corridors at school?", "we may fall and get hurt or hurt others", ["running is not allowed anywhere", "it makes the floor dirty", "it wastes energy"], "Walk carefully."),
       ("What should we do before crossing a road?", "stop, look both ways and cross at the zebra crossing", ["run fast without looking", "cross from behind a bus", "walk while using a phone"], "Follow the traffic lights."),
       ("Why should we wear a helmet while cycling?", "it protects our head if we fall", ["it makes the bicycle faster", "it keeps the sun out only", "it is a fashion"], "Safety first."),
       ("What does a red traffic light mean?", "stop", ["go", "go fast", "turn round"], "Green means go and yellow means get ready."),
       ("What is a first-aid box for?", "giving quick help for small injuries", ["storing toys", "keeping food", "keeping money"], "It has bandages and cotton."),
       ("Why should we visit a doctor when we are ill?", "the doctor can find out what is wrong and help us get well", ["doctors make us ill", "it is not needed", "only adults get ill"], "Take medicine only as advised."),
       ("Why is it important to eat breakfast?", "it gives us energy for the morning", ["it makes us sleepy", "it is not needed", "it is unhealthy"], "Do not skip breakfast."),
       ("Why should we avoid too many sweets?", "they can cause tooth decay and weight gain", ["sweets build muscles", "sweets clean teeth", "sweets give vitamins"], "Eat fruits instead."),
       ("Which of these is a way to relax?", "listening to music or drawing", ["fighting", "shouting", "staying awake all night"], "Rest keeps the mind healthy."),
       ("Why should we not use phones or TV late at night?", "it disturbs our sleep", ["it helps us sleep", "it makes eyes stronger", "it is healthy"], "Keep screens away at bedtime."),
       ("Why is it good to share our feelings?", "talking helps us feel better and get help", ["feelings should be hidden", "sharing makes things worse", "nobody listens"], "Talk to people you trust."),
       ("Why should we wash fruits before eating them?", "to remove dirt and germs", ["to make them sour", "to make them bigger", "it is not needed"], "Use clean water."),
       ("Why do we need to exercise every day?", "it keeps our heart, muscles and bones strong", ["it makes us weak", "it stops growth", "it is only for adults"], "Play for at least an hour."),
       ("Why should we not eat food from roadside stalls with flies on it?", "flies carry germs that cause illness", ["flies make food tastier", "it is healthier", "flies are clean"], "Eat covered, fresh food."),
       ("What should you do if you feel very hot and tired after playing in the sun?", "rest in the shade and drink water", ["keep running", "eat a lot of sweets", "sleep in the sun"], "Wear a cap next time."),
       ("Why should we keep our nails and hair clean?", "dirt and germs can collect in them", ["dirty hair grows faster", "clean nails break", "it does not matter"], "Bathe and wash hair regularly."),
       ("Which of these helps us stay calm?", "deep breathing and yoga", ["shouting", "fighting", "running into traffic"], "Breathe in slowly and breathe out slowly."),
       ("Why should we keep a safe distance from someone who is coughing a lot?", "germs spread through coughs", ["coughing is healthy", "to be rude", "it does not matter"], "Wish them a quick recovery.")]

# =================================================================== Chapter 10: this world of things
NAT = {"a natural thing": ["a stone", "a tree", "sand", "a feather", "water", "a seashell", "a flower", "wood", "clay", "the Sun"],
       "a human-made thing": ["a chair", "a pencil", "a plastic bottle", "a car", "a book", "a glass tumbler", "a brick", "a bicycle", "a shirt", "a steel spoon"]}
MADE = {"usually made of wood": ["a cricket bat", "a wooden door", "a rolling pin (belan)", "a pencil's outer case", "a wooden spoon"],
        "usually made of metal": ["a steel plate", "a pressure cooker", "a key", "a safety pin", "a coin"],
        "usually made of glass": ["a window pane", "a pair of spectacles", "a mirror", "a glass bangle", "a light bulb"],
        "usually made of clay": ["a matka (water pot)", "a diya", "a kulhad (tea cup)", "a flowerpot", "a brick"],
        "usually made of cloth": ["a towel", "a bedsheet", "a school bag", "a handkerchief", "a curtain"]}
HS = {"hard": ["a stone", "an iron nail", "a brick", "a wooden table", "a steel spoon", "a walnut shell"], "soft": ["cotton wool", "a pillow", "a sponge", "a woollen sweater", "dough", "a feather"]}
RS = {"rough": ["sandpaper", "a brick", "the bark of a tree", "a coconut shell", "a jute sack", "a stone wall"], "smooth": ["a glass window", "a marble floor", "a steel plate", "a silk cloth", "a mirror", "a plastic bucket"]}
THQ = [("What is a natural thing?", "something we get from nature, such as a stone or a leaf", ["something made in a factory", "a toy car", "a plastic bag"], "People do not make natural things."),
       ("What is a human-made thing?", "something made by people, such as a chair or a pen", ["a rock in a river", "a tree", "a cloud"], "People make things from natural materials."),
       ("What is a chair made of?", "it can be made of wood, plastic or metal", ["only water", "only air", "only sand"], "The same thing can be made of different materials."),
       ("Why are window panes made of glass?", "we can see through glass", ["glass is soft", "glass is heavy only", "glass is dark"], "Glass lets light in."),
       ("Why are cooking pots made of metal?", "metal lets heat pass and does not burn", ["metal is soft like cotton", "metal melts easily", "metal is see-through"], "Handles may be plastic or wood."),
       ("Why are raincoats made of plastic?", "plastic does not let water through", ["plastic soaks up water", "plastic is see-through only", "plastic is hot"], "It keeps us dry."),
       ("Why is a pillow made of soft materials?", "so that we can rest our head comfortably", ["so it is heavy", "so it is sharp", "so it is cold"], "Cotton is used in pillows."),
       ("Which of these floats on water?", "a piece of wood", ["an iron nail", "a stone", "a coin"], "A coin sinks."),
       ("Which of these sinks in water?", "a stone", ["a dry leaf", "a cork", "a feather"], "Heavy, solid things often sink."),
       ("Which of these dissolves in water?", "sugar", ["sand", "a stone", "a plastic bead"], "Salt dissolves too."),
       ("Which of these does not dissolve in water?", "sand", ["salt", "sugar", "lemon juice"], "Sand settles at the bottom."),
       ("Why is a ball round?", "so that it can roll easily", ["so it can stand still", "so it is heavy", "so it is sharp"], "Wheels are round too."),
       ("Why are bottles often made of plastic?", "plastic is light and does not break easily", ["plastic is heavy", "plastic breaks easily", "plastic is soft like cotton"], "But too much plastic harms nature."),
       ("What can we make from clay?", "pots, toys, diyas and bricks", ["glass windows", "steel spoons", "plastic bags"], "Clay is soft when wet and hard when baked."),
       ("Which material comes from trees?", "wood", ["iron", "glass", "plastic"], "Paper is also made from wood."),
       ("Which material is made from sand?", "glass", ["wood", "wool", "cotton"], "Sand is melted at very high heat."),
       ("Which material do we get from the cotton plant?", "cotton for cloth", ["iron", "glass", "rubber"], "Cotton is spun into thread."),
       ("Why should we not use too much plastic?", "it does not rot and pollutes land and water", ["plastic is good for soil", "plastic rots quickly", "plastic is food for animals"], "Use cloth bags."),
       ("Which sense tells you if a thing is rough or smooth?", "touch", ["hearing", "smell", "taste"], "Feel it with your fingers."),
       ("What shape is a brick?", "a cuboid (like a box)", ["a ball", "a cone", "a ring"], "Bricks stack easily."),
       ("Why are shoes soles made of rubber?", "rubber grips the ground and does not slip easily", ["rubber is slippery", "rubber is see-through", "rubber is heavy only"], "It also bends easily."),
       ("Why do we keep some things in glass bottles and some in plastic bottles?", "glass does not react with food and plastic is lighter", ["glass is always cheaper", "plastic is see-through only", "there is no reason"], "Pickles are often kept in glass jars."),
       ("Why is a sponge useful for cleaning?", "it soaks up water", ["it is hard", "it is heavy", "it is sharp"], "Squeeze out the water after use."),
       ("Why are umbrellas made of waterproof cloth?", "so that rain does not pass through", ["so it is heavy", "so it is see-through", "so it is rough"], "Plastic is also used.")]

# =================================================================== Chapter 11: making things
ART = [("a potter", "clay pots and diyas"), ("a weaver", "cloth on a loom"), ("a carpenter", "furniture from wood"), ("a blacksmith", "iron tools such as sickles and axes"),
       ("a goldsmith", "jewellery"), ("a cobbler", "shoes and chappals"), ("a tailor", "clothes stitched from cloth"), ("a basket weaver", "baskets from bamboo"),
       ("a mason", "walls and buildings"), ("a sculptor", "statues from stone or clay")]
TOOL = [("a loom", "weaving cloth"), ("a potter's wheel", "shaping clay pots"), ("a hammer", "hitting nails"), ("a saw", "cutting wood"), ("a needle", "sewing"),
        ("a charkha (spinning wheel)", "spinning cotton into thread"), ("a chisel", "carving wood or stone"), ("a kiln", "baking clay pots to make them hard")]
FROM = [("a clay pot", "clay"), ("cotton cloth", "cotton"), ("paper", "wood pulp or old paper"), ("jaggery", "sugarcane juice"), ("a basket", "bamboo"), ("a jute bag", "jute fibre"),
        ("a candle", "wax"), ("a glass bottle", "sand"), ("a woollen sweater", "wool from sheep"), ("a silk saree", "silk from silkworms"), ("butter", "milk"), ("a rubber ball", "rubber from trees")]
CRAFT = [("Madhubani painting", "Bihar"), ("Kanjeevaram silk sarees", "Tamil Nadu"), ("Pashmina shawls", "Jammu and Kashmir"), ("blue pottery", "Rajasthan"), ("Channapatna wooden toys", "Karnataka"),
         ("Pattachitra painting", "Odisha"), ("Warli painting", "Maharashtra"), ("Kondapalli toys", "Andhra Pradesh"), ("Phulkari embroidery", "Punjab"), ("Chikankari embroidery", "Uttar Pradesh")]
SEQS = [("making a clay pot", ["dig the clay", "mix it with water", "shape it on the wheel", "dry it in the sun", "bake it in a kiln"]),
        ("making cotton cloth", ["pick the cotton", "clean the cotton", "spin it into thread", "weave the thread into cloth"]),
        ("making handmade paper", ["soak old paper in water", "mash it into pulp", "spread the pulp on a screen", "press out the water", "dry the sheet"]),
        ("making a woollen sweater", ["cut wool from the sheep", "wash the wool", "spin it into yarn", "knit the yarn into a sweater"])]


def c_steps(k=None):
    R = _R[0]
    what, st = R.choice(SEQS)
    i = R.randrange(len(st) - 1)
    a = st[i + 1]
    other = [x for _, s_ in SEQS for x in s_ if x not in st]
    w = [x for x in st if x not in (a, st[i])] + R.sample(other, 2)
    return tq("In %s, which step comes just after: <i>%s</i>?" % (what, st[i]), a, R.sample(w, 3), "The steps are: " + " → ".join(st) + ".")


MKQ = [("What is an artisan?", "a skilled person who makes things by hand", ["a machine", "a shop", "a farmer only"], "Potters and weavers are artisans."),
       ("Why do potters bake pots in a kiln?", "to make them hard and strong", ["to make them soft", "to make them wet", "to make them sticky"], "Unbaked pots break easily."),
       ("What is a loom used for?", "weaving threads into cloth", ["baking pots", "cutting wood", "making shoes"], "Weavers use looms."),
       ("Who popularised the charkha to make khadi cloth?", "Mahatma Gandhi", ["Jawaharlal Nehru", "C. V. Raman", "Rabindranath Tagore"], "Khadi is hand-spun and hand-woven."),
       ("Why are handmade things special?", "they show the skill of the artisan and each one is a little different", ["they are all the same", "they are made by machines", "they are useless"], "Buying them supports artisans."),
       ("What is recycling paper?", "making new paper from old paper", ["burning paper", "throwing paper away", "colouring paper"], "It saves trees."),
       ("Why do we use bamboo to make baskets?", "it is strong, light and bends easily", ["it is heavy like iron", "it melts", "it is made in factories"], "Bamboo grows fast."),
       ("What do we need to make a paper boat?", "a sheet of paper and folding", ["clay and fire", "a hammer and nails", "wool and needles"], "Origami is the art of paper folding."),
       ("Which material is used to make candles?", "wax", ["glass", "iron", "stone"], "The wick is made of cotton thread."),
       ("Which part of a candle burns?", "the wick, using the wax", ["only the glass", "the plate", "the air"], "The flame melts the wax."),
       ("What is clay made of?", "very fine soil mixed with water", ["plastic", "metal", "sugar"], "It is soft and sticky when wet."),
       ("Why do we need tools to make things?", "tools make the work easier and neater", ["tools make work harder", "tools are toys", "tools are not needed"], "A carpenter needs a saw."),
       ("What is a kulhad?", "a small clay cup used for tea", ["a metal plate", "a glass jar", "a plastic bottle"], "Kulhads are eco-friendly."),
       ("What do we call the thread made by twisting cotton fibres?", "yarn", ["clay", "wax", "pulp"], "Yarn is woven into cloth."),
       ("Why should we reuse old things to make new ones?", "it reduces waste", ["it creates more waste", "it costs more", "it harms the Earth"], "An old jar can become a pen stand."),
       ("Which tool is used to dig and loosen soil in a garden?", "a spade", ["a needle", "a loom", "a kiln"], "Farmers also use ploughs."),
       ("Which artisan uses a needle and thread most?", "a tailor", ["a blacksmith", "a potter", "a mason"], "Tailors stitch clothes."),
       ("Which artisan works with a hot fire and an anvil?", "a blacksmith", ["a tailor", "a weaver", "a goldsmith"], "Iron is heated and hammered."),
       ("Why do toy makers paint wooden toys with natural colours?", "natural colours are safe for children", ["natural colours are poisonous", "paint makes toys heavier", "children eat paint"], "Channapatna toys use vegetable dyes."),
       ("What do we get from silkworms?", "silk thread", ["wool", "cotton", "jute"], "Silkworms spin cocoons of silk."),
       ("How is a brick made?", "clay is shaped in a mould, dried and baked", ["glass is melted", "wood is carved", "wool is spun"], "Bricks are used to build houses."),
       ("What is the name of the art of folding paper into shapes?", "origami", ["pottery", "weaving", "carpentry"], "It began in Japan."),
       ("Why do we wear gloves when working with sharp tools?", "to protect our hands", ["to make work slower", "to look nice", "to keep hands wet"], "Safety matters."),
       ("What is a tool used by a farmer to cut crops?", "a sickle", ["a loom", "a needle", "a kiln"], "Blacksmiths make sickles."),
       ("What is jute used to make?", "sacks, bags and ropes", ["glass", "candles", "steel"], "Jute grows in West Bengal and Assam."),
       ("Why are clay pots good for keeping water cool?", "water seeps through tiny pores and evaporates, cooling the pot", ["clay makes ice", "clay is a refrigerator", "clay heats water"], "A matka keeps water cool in summer."),
       ("How is jaggery made?", "sugarcane juice is boiled until it becomes thick and sets", ["wheat is ground", "milk is churned", "cotton is spun"], "It is called gur."),
       ("What does a weaver need to make cloth?", "thread and a loom", ["clay and fire", "wood and nails", "wax and a wick"], "The threads go over and under each other."),
       ("Why do artisans pass their skills to their children?", "to keep the craft alive in the family", ["crafts are a secret game", "children cannot learn", "to stop the craft"], "Many crafts are hundreds of years old.")]

# =================================================================== Chapter 12: taking charge of waste
WD = {"wet waste (for the green bin)": ["vegetable peels", "leftover food", "fruit skins", "tea leaves", "eggshells", "flowers from a puja", "fallen leaves", "coconut shells"],
      "dry waste (for the blue bin)": ["a plastic bottle", "an old newspaper", "a broken toy", "a glass jar", "an empty tin can", "a cardboard box", "a milk packet", "a chocolate wrapper"]}
RRR3 = {"reducing waste": ["carrying a cloth bag to the market", "using both sides of paper", "taking only as much food as you can eat", "saying no to plastic straws", "carrying your own water bottle"],
        "reusing things": ["using an old jar as a pen stand", "giving old clothes to someone who needs them", "using a used box to store toys", "making a planter from an old bottle", "using old cloth as a duster"],
        "recycling things": ["selling old newspapers to the kabadiwala for making new paper", "melting old glass to make new bottles", "making compost from kitchen waste", "melting old cans to make new metal things", "making new plastic items from old plastic"]}
BIO = {"biodegradable (it breaks down naturally)": ["a banana peel", "paper", "cotton cloth", "dry leaves", "a wooden stick", "leftover rice", "jute sack", "cow dung"],
       "non-biodegradable (it does not break down easily)": ["a plastic bag", "a glass bottle", "a metal can", "a rubber tyre", "a plastic toy", "a polythene wrapper", "a thermocol plate", "an old battery"]}
WQ3 = [("What is waste?", "things we throw away because we do not need them", ["things we keep and use daily", "fresh food", "clean water"], "Some waste can be reused."),
       ("Why should we separate wet and dry waste?", "so that wet waste can be composted and dry waste can be recycled", ["to make more waste", "it does not matter", "to mix them later"], "Use two bins."),
       ("What is compost?", "manure made from rotting kitchen and garden waste", ["a type of plastic", "a kind of glass", "a metal"], "It makes soil rich."),
       ("Who collects old newspapers and bottles to sell for recycling?", "the kabadiwala", ["the doctor", "the postman", "the teacher"], "Recycling starts with sorting."),
       ("Why is plastic harmful to animals?", "they may eat it and fall sick or choke", ["animals digest plastic easily", "plastic is good food", "plastic keeps them warm"], "Cows on streets often eat plastic bags."),
       ("Why should we not burn waste?", "burning makes smoke that pollutes the air", ["burning cleans the air", "smoke is healthy", "it makes rain"], "Burning plastic is very harmful."),
       ("What happens to waste thrown in drains?", "drains get blocked and water floods the streets", ["drains become cleaner", "nothing happens", "the waste disappears"], "Never throw waste in drains."),
       ("What does 'reduce' mean?", "use less so that there is less waste", ["throw more away", "use things only once", "buy more packets"], "Carry a cloth bag."),
       ("What does 'reuse' mean?", "use something again, perhaps in a new way", ["throw it away at once", "burn it", "bury it"], "An old jar can store spices."),
       ("What does 'recycle' mean?", "make new things from old materials", ["use something once and throw it", "keep waste at home forever", "hide waste"], "Old paper becomes new paper."),
       ("Which of these can go into a compost pit?", "vegetable peels", ["a glass bottle", "a plastic bag", "a metal spoon"], "Only things that rot go in compost."),
       ("Why should we carry a cloth bag when shopping?", "it reduces the use of plastic bags", ["cloth bags are heavier", "plastic bags are better", "shops do not allow plastic"], "Cloth bags can be used many times."),
       ("What is littering?", "throwing waste on the ground instead of in a dustbin", ["putting waste in a dustbin", "making compost", "recycling"], "Littering makes places dirty."),
       ("Which national campaign asks people to keep India clean?", "the Swachh Bharat Mission", ["Project Tiger", "the Green Revolution", "Chandrayaan"], "It started on 2 October 2014."),
       ("Why should old batteries not be thrown with kitchen waste?", "they contain harmful chemicals", ["they rot quickly", "they are food for worms", "they are wet waste"], "Give them to special collection points."),
       ("How do earthworms help with waste?", "they eat rotting matter and turn it into rich compost", ["they make plastic", "they eat glass", "they block drains"], "This is vermicompost."),
       ("Why do flies gather on open garbage?", "rotting waste attracts them and they spread germs", ["they clean it fully", "they are cold", "they like plastic"], "Keep dustbins covered."),
       ("What can we do with old notebooks with blank pages?", "use the blank pages for rough work", ["burn them", "throw them in a river", "bury them"], "That is reusing."),
       ("Why should we take only as much food as we can eat?", "it reduces food waste", ["it makes more waste", "food is unlimited", "it is a rule only at school"], "Ask for more if needed."),
       ("What is a landfill?", "a large place where city waste is dumped and covered with soil", ["a playground", "a garden", "a river"], "Landfills fill up fast; less waste is better."),
       ("Which waste is recycled to make new paper?", "old newspapers and cardboard", ["vegetable peels", "glass bottles", "plastic toys"], "Recycling paper saves trees."),
       ("Why should we not mix broken glass with other waste?", "it can cut the people who collect waste", ["glass rots", "it is wet waste", "it makes compost"], "Wrap it in paper and mark it.")]


def c_waste(k=None):
    R = _R[0]
    n = kid()
    kg, d = R.choice([1, 2, 3]), R.choice([5, 7, 10])
    if R.random() < 0.5:
        return nq("%s's family puts %d kg of kitchen waste into the compost pit every day. How much waste goes in during %d days?" % (n, kg, d), kg * d, [kg + d, d, kg * d + kg, kg * (d - 1)], "kg",
                  "%d × %d = %d kg." % (kg, d, kg * d))
    b = R.choice([2, 3, 4, 5])
    return nq("A family uses %d plastic bags every day. If they carry a cloth bag instead, how many plastic bags do they save in %d days?" % (b, d), b * d, [b + d, d, b * d + b, b], "bags",
              "%d × %d = %d bags." % (b, d, b * d))


def UNITS3b():
    b = {k: once_maker(v) for k, v in [("w", WQ), ("f", FOODQ), ("h", HQ3), ("t", THQ), ("m", MKQ), ("ws", WQ3)]}
    wsrc = pairs(WSRC, "What is %s?", "What do we call %s?")
    wuse = odd_one(WUSE, "Which of these is %s?", "Which of these is not %s?")
    srcf = odd_one(SRCF, "Which of these is %s?", "Which of these is not %s?")
    cook = pairs(COOK, "How is %s usually cooked?")
    raw = odd_one(RAW, "Which of these is %s?", "Which of these is not %s?")
    regf = pairs(REGF, "Which food is famous in %s?", "In which state is %s a famous food?")
    hab = odd_one(HAB, "Which of these is %s?", "Which of these is not %s?")
    safe = pairs(SAFE9, "What should you do when %s?")
    exer = pairs(EXER, "What is %s especially good for?", "Which activity is especially good for %s?")
    aid = pairs(AID, "What is the first thing to do for %s?", "Which small problem needs this first aid: %s?")
    nat = odd_one(NAT, "Which of these is %s?", "Which of these is not %s?")
    made = odd_one(MADE, "Which of these is %s?", "Which of these is not %s?")
    hs = odd_one(HS, "Which of these is %s?", "Which of these is not %s?")
    rs = odd_one(RS, "Which of these feels %s?", "Which of these does not feel %s?")
    art = pairs(ART, "What does %s make?", "Who makes %s?")
    tool = pairs(TOOL, "What is %s used for?", "Which tool is used for %s?")
    frm = pairs(FROM, "What is %s made from?", "What is made from %s?")
    craft = pairs(CRAFT, "Which state is famous for %s?", "Which craft is famous in %s?")
    wd = odd_one(WD, "Which of these is %s?", "Which of these is not %s?")
    rrr = odd_one(RRR3, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    bio = odd_one(BIO, "Which of these is %s?", "Which of these is not %s?")
    return [
        U(7, "water-a-precious-gift", 7, WA,
          "Sources of water; uses of water at home, in farms and for living things; clean and safe drinking water; saving water and rainwater harvesting (summary of NCERT Our Wondrous World Chapter 7).",
          "Water: A Precious Gift", "water, a precious gift",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 7: sources of water, uses of water, safe drinking water, saving water and rainwater harvesting. 100 questions with answers.",
          "Every living thing needs water.", "Save every drop; keep water clean.",
          "<p>We get water from rain, rivers, lakes, ponds, wells, hand pumps and taps. All plants and animals need water, and we use it for drinking, cooking, bathing, washing and farming. Most of the Earth's water is salty sea water, so clean fresh water is precious.</p>"
          "<p>Dirty water can cause diseases such as diarrhoea, so we boil or filter water and keep it covered. We save water by closing taps, fixing leaks, using buckets instead of hoses and collecting rainwater.</p>",
          [("A tap leaks 2 litres every hour. In 5 hours?", ["2 × 5"], "10 litres"), ("Brushing with the tap running is…", ["water flows away unused"], "wasting water")],
          ["Thinking water never runs out.", "Drinking water from an uncovered pot.", "Thinking a few drops do not matter."],
          [("How can we save water at home?", "Close the tap while brushing, fix leaks, use a bucket instead of a hose and reuse water for plants."),
           ("What is rainwater harvesting?", "Collecting and storing rainwater, or sending it into the ground, so it can be used later.")],
          lambda: [("Where water comes from", [(wsrc, 12), (b["w"], 8)]), ("Uses of water", [(b["w"], 6), (c_water, 14)]), ("Clean water", [(b["w"], 6), (wuse, 8), (wsrc, 6)]),
                   ("Saving water", [(wuse, 14), (c_water, 6)]), ("Mixed problems", [(c_water, 16), (wuse, 4)])]),
        U(8, "food-we-eat", 8, FH,
          "Food from plants and animals; raw and cooked food; ways of cooking; food from different regions of India; healthy eating and not wasting food (summary of NCERT Our Wondrous World Chapter 8).",
          "Food We Eat", "food we eat",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 8: food from plants and animals, raw and cooked food, ways of cooking, regional foods of India and healthy eating. 100 questions with answers.",
          "We get food from plants and animals.", "Eat many kinds of food; do not waste it.",
          "<p>We get rice, wheat, dal, vegetables and fruits from plants, and milk, eggs, honey and fish from animals. Some foods such as cucumber and fruits can be eaten raw; others such as rice and dal are cooked by boiling, frying, steaming, roasting or baking.</p>"
          "<p>People in different parts of India eat different foods, like idli in Tamil Nadu and dhokla in Gujarat, because different crops grow there. We should eat a balanced meal, wash our hands before eating and never waste food.</p>",
          [("Idli is cooked by…", ["in a special stand over water"], "steaming"), ("Is honey from a plant or an animal?", ["bees make it"], "an animal")],
          ["Thinking all food comes from shops.", "Thinking milk comes from plants.", "Wasting food on the plate."],
          [("Which foods do we get from animals?", "Milk, curd, paneer, ghee, eggs, honey and fish."),
           ("Why do people in different regions eat different foods?", "Different crops and animals are found in different regions.")],
          lambda: [("Food from plants and animals", [(srcf, 14), (b["f"], 6)]), ("Raw and cooked food", [(raw, 12), (cook, 8)]), ("Food from different regions", [(regf, 14), (b["f"], 6)]),
                   ("Healthy eating", [(b["f"], 11), (srcf, 5), (raw, 4)]), ("Mixed problems", [(srcf, 6), (raw, 7), (regf, 6), (cook, 1)])]),
        U(9, "staying-healthy-and-happy", 9, FH,
          "Good habits for a healthy body: cleanliness, exercise, sleep and food; feelings and staying happy; safety at home, on the road and at play; simple first aid (summary of NCERT Our Wondrous World Chapter 9).",
          "Staying Healthy and Happy", "staying healthy and happy",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 9: healthy and unhealthy habits, cleanliness, exercise and sleep, feelings, safety rules and simple first aid. 100 questions with answers.",
          "Good habits keep us healthy and happy.", "Clean, active, rested and safe.",
          "<p>We stay healthy by brushing twice a day, washing hands with soap, bathing, cutting nails, eating fruits and vegetables, drinking water, playing outdoors and sleeping early. Being happy is also part of being healthy: we can share our feelings and help others.</p>"
          "<p>Safety rules protect us: look both ways at the zebra crossing, wear a helmet when cycling, never go with strangers and never touch bare wires. For a small cut, wash it with clean water and cover it with a clean bandage.</p>",
          [("Bed at 9 p.m., up at 6 a.m. Hours of sleep?", ["3 hours to midnight + 6 hours"], "9 hours"), ("Biting nails is…", ["germs go into the mouth"], "an unhealthy habit")],
          ["Thinking health is only about the body.", "Crossing the road without looking.", "Rubbing an eye that has dust in it."],
          [("Which habits keep us healthy?", "Brushing twice a day, washing hands, bathing, eating well, playing outdoors and sleeping early."),
           ("What should you do for a small cut?", "Wash it with clean water and cover it with a clean bandage; tell an adult.")],
          lambda: [("Healthy habits", [(hab, 14), (b["h"], 6)]), ("Exercise and sleep", [(exer, 8), (c_sleep, 8), (b["h"], 4)]), ("Feelings and happiness", [(b["h"], 12), (hab, 8)]),
                   ("Safety and first aid", [(safe, 9), (aid, 9), (exer, 2)]), ("Mixed problems", [(c_sleep, 12), (b["h"], 5), (exer, 3)])]),
        U(10, "this-world-of-things", 10, TA,
          "Natural and human-made things; materials such as wood, metal, glass, clay, cloth and plastic; properties such as hard and soft, rough and smooth, floating and sinking; choosing materials for their use (summary of NCERT Our Wondrous World Chapter 10).",
          "This World of Things", "this world of things",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 10: natural and human-made things, materials such as wood, metal, glass and clay, hard and soft, rough and smooth, and floating and sinking. 100 questions with answers.",
          "Things are natural or made by people.", "We choose materials for what they can do.",
          "<p>Some things are natural, such as stones, trees and sand; others are made by people, such as chairs, pencils and bottles. Human-made things are made from materials such as wood, metal, glass, clay, cloth and plastic.</p>"
          "<p>Materials have different properties: a stone is hard and cotton is soft; sandpaper is rough and glass is smooth; wood floats and iron sinks. We choose glass for windows because we can see through it and plastic for raincoats because water cannot pass through.</p>",
          [("Is a brick natural or human-made?", ["made from clay by people"], "human-made"), ("Which feels rough: sandpaper or a mirror?", ["touch it"], "sandpaper")],
          ["Thinking all things made of wood are natural.", "Thinking every heavy thing sinks.", "Thinking plastic rots quickly."],
          [("What is the difference between natural and human-made things?", "Natural things come from nature; human-made things are made by people, often from natural materials."),
           ("Why are windows made of glass?", "Light can pass through glass, so we can see out and the room stays bright.")],
          lambda: [("Natural and human-made things", [(nat, 14), (b["t"], 6)]), ("Materials", [(made, 14), (b["t"], 6)]), ("Hard and soft, rough and smooth", [(hs, 10), (rs, 10)]),
                   ("Choosing the right material", [(b["t"], 8), (made, 8), (nat, 4)]), ("Mixed problems", [(nat, 8), (made, 8), (hs, 2), (rs, 2)])]),
        U(11, "making-things", 11, TA,
          "Things people make by hand: artisans such as potters, weavers, carpenters and blacksmiths; their tools; raw materials and the steps of making things; crafts of different states; reusing materials (summary of NCERT Our Wondrous World Chapter 11).",
          "Making Things", "making things",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 11: artisans and what they make, tools, raw materials, the steps of making pots and cloth, and famous crafts of India. 100 questions with answers.",
          "Artisans make useful and beautiful things by hand.", "Clay → pot, cotton → cloth, bamboo → basket.",
          "<p>Artisans are skilled people who make things by hand. A potter shapes clay on a wheel and bakes it in a kiln; a weaver weaves thread into cloth on a loom; a carpenter makes furniture from wood; a blacksmith makes iron tools.</p>"
          "<p>Every product starts from a raw material: pots from clay, cloth from cotton, baskets from bamboo and paper from wood pulp or old paper. Each state has famous crafts, such as Madhubani painting in Bihar and Channapatna toys in Karnataka.</p>",
          [("Who makes furniture from wood?", ["uses a saw and a chisel"], "a carpenter"), ("Clay pot: after shaping on the wheel?", ["it must lose water"], "dry it in the sun")],
          ["Baking a pot before shaping it.", "Thinking cloth comes from wool only.", "Thinking handmade things are all the same."],
          [("What does a potter do?", "A potter shapes wet clay on a wheel, dries it and bakes it in a kiln to make pots, diyas and toys."),
           ("How is cotton cloth made?", "Cotton is picked, cleaned, spun into thread and then woven into cloth.")],
          lambda: [("Artisans", [(art, 12), (b["m"], 8)]), ("Tools", [(tool, 12), (b["m"], 8)]), ("Raw materials", [(frm, 14), (b["m"], 6)]),
                   ("Steps of making things", [(c_steps, 11), (craft, 9)]), ("Crafts of India", [(craft, 7), (frm, 6), (art, 4), (tool, 1), (b["m"], 2)])]),
        U(12, "taking-charge-of-waste", 12, TA,
          "What waste is; wet and dry waste and how to sort it; biodegradable and non-biodegradable waste; composting; reduce, reuse and recycle; keeping our surroundings clean (summary of NCERT Our Wondrous World Chapter 12).",
          "Taking Charge of Waste", "taking charge of waste",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 12: wet and dry waste, green and blue bins, waste that rots and waste that does not, composting, and reduce, reuse and recycle. 100 questions with answers.",
          "Sort waste: wet in green, dry in blue.", "Reduce, reuse, recycle.",
          "<p>Waste is what we throw away. Wet waste such as peels and leftover food goes in the green bin and can become compost. Dry waste such as paper, plastic, glass and metal goes in the blue bin and much of it can be recycled. Things like peels and paper rot (they are biodegradable), but plastic, glass and metal do not.</p>"
          "<p>We can make less waste by reducing (carry a cloth bag), reusing (an old jar as a pen stand) and recycling (old newspapers into new paper). Never throw waste in drains, rivers or on the road, and never burn plastic.</p>",
          [("Banana peel: green or blue bin?", ["it rots"], "green bin (wet waste)"), ("An old jar as a pen stand is…", ["using it again"], "reusing")],
          ["Putting plastic in the compost pit.", "Burning waste to get rid of it.", "Mixing reuse and recycle."],
          [("What is the difference between wet and dry waste?", "Wet waste comes from food and plants and rots; dry waste such as paper, plastic, glass and metal does not rot easily."),
           ("What do reduce, reuse and recycle mean?", "Reduce: use less. Reuse: use again. Recycle: make new things from old materials.")],
          lambda: [("Wet and dry waste", [(wd, 16), (b["ws"], 4)]), ("Waste that rots and waste that does not", [(bio, 14), (b["ws"], 6)]), ("Reduce, reuse and recycle", [(rrr, 16), (b["ws"], 4)]),
                   ("Compost and cleanliness", [(b["ws"], 4), (c_waste, 8), (wd, 8)]), ("Mixed problems", [(wd, 2), (rrr, 4), (bio, 6), (c_waste, 8)])]),
    ]
