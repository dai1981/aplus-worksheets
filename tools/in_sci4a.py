# -*- coding: utf-8 -*-
"""Class 4 EVS (NCERT Our Wondrous World, chapters 1–5): question makers and UNITS4a()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import odd_one, nq, _cap
from in_sci3a import kid
import in_sci

CO, LA, HW, TA, EN = "Our Community", "Life Around Us", "Health and Well-being", "Things Around Us", "Our Environment"

# =================================================================== Chapter 1: living together
HELPER = [("a doctor", "treating people who are ill"), ("a nurse", "caring for patients in a hospital"), ("a police officer", "keeping people safe and maintaining order"),
          ("a firefighter", "putting out fires and rescuing people"), ("a postman", "delivering letters and parcels"), ("a farmer", "growing food crops"),
          ("a teacher", "helping children learn"), ("a sanitation worker", "keeping streets clean and collecting waste"), ("an electrician", "repairing wiring and electrical fittings"),
          ("a plumber", "fixing water pipes and taps"), ("a bus driver", "taking people from one place to another"), ("a vegetable seller", "selling fresh vegetables"), ("a pharmacist", "giving medicines prescribed by doctors"), ("a cobbler", "mending shoes and sandals"), ("a carpenter", "making and repairing wooden furniture")]
PLACE = [("a post office", "sending letters, parcels and money orders"), ("a hospital", "getting treatment when we are ill or hurt"), ("a bank", "keeping money safely"),
         ("a police station", "reporting a crime or getting help in danger"), ("a library", "reading and borrowing books"), ("a market", "buying and selling things"),
         ("a panchayat office", "the place where elected villagers meet to take decisions for the village"), ("a fire station", "keeping fire engines ready for emergencies"),
         ("a fair price (ration) shop", "buying grains and other food at low prices"), ("a park", "playing, walking and resting")]
EMER = [("100", "the police"), ("101", "the fire service"), ("108", "an ambulance in most states"), ("1098", "Childline, the helpline for children in need")]
TOG = {"a good way to live together in a community": ["sharing a water tap fairly", "helping a neighbour carry heavy bags", "keeping the street clean", "taking turns on the swings",
                                                     "speaking softly at night so others can sleep", "inviting new families to festivals", "helping clean the village pond", "returning borrowed things on time"],
       "a careless or selfish act in a community": ["throwing garbage in the street", "playing loud music late at night", "cutting in at the front of a queue", "wasting water from a public tap",
                                                     "damaging park benches", "parking a scooter in front of someone's gate", "spitting on the road", "breaking the swings"]}
LTQ = [("What is a community?", "a group of people who live in the same area and share places and services", ["a single family only", "a shop", "a river"], "A village or a colony is a community."),
       ("Why do people in a community depend on each other?", "no one can do every job alone", ["people never need help", "everyone grows all their food", "everyone is a doctor"], "Farmers, doctors and drivers all help us."),
       ("What is a panchayat?", "an elected group that looks after the needs of a village", ["a big market", "a hospital", "a type of school"], "The head is called the sarpanch."),
       ("Who is the head of a gram panchayat?", "the sarpanch", ["the postman", "the doctor", "the shopkeeper"], "The sarpanch is chosen by the villagers."),
       ("Why should we follow rules in a community?", "rules keep everyone safe and make life fair", ["rules are only for adults", "rules make life harder", "rules are not needed"], "Traffic rules are an example."),
       ("How can children help their community?", "by keeping places clean and helping others", ["by breaking things", "by wasting water", "by fighting"], "Small acts make a big difference."),
       ("Why should we thank community helpers?", "they work hard to make our lives better", ["they do not help", "they are paid only", "they never work"], "Smile and say thank you."),
       ("What do we call people who live next to us?", "neighbours", ["strangers", "tourists", "guests only"], "Good neighbours help each other."),
       ("Why do festivals bring a community together?", "people celebrate and share food together", ["people stay alone", "people fight", "nobody celebrates"], "Festivals build friendship."),
       ("What is a public place?", "a place that everyone can use, such as a park or a library", ["your bedroom", "a friend's cupboard", "your school bag"], "We must keep public places clean."),
       ("Why should we not damage public property?", "it belongs to everyone and is paid for by all", ["it belongs to nobody", "it is cheap", "it can be broken for fun"], "Look after parks and buses."),
       ("What is a cooperative?", "a group of people who work together and share the profit", ["a single shopkeeper", "a government office only", "a type of machine"], "Amul is a famous milk cooperative in Gujarat."),
       ("Which famous milk cooperative began in Anand, Gujarat?", "Amul", ["ISRO", "Indian Railways", "the Post Office"], "Farmers sell their milk to the cooperative."),
       ("Why is it important to include people with disabilities in games and activities?", "everyone has a right to join in and enjoy", ["they cannot do anything", "games are only for some", "it slows the game"], "Ramps and helpful rules help everyone."),
       ("What can a community do to save water?", "repair leaking taps and collect rainwater", ["leave taps open", "waste water in tanks", "throw garbage in ponds"], "Every family can help."),
       ("What does a sanitation worker do for us?", "keeps our surroundings clean and healthy", ["sells vegetables", "flies aeroplanes", "teaches maths"], "Separate your waste to help them."),
       ("Why do we stand in a queue?", "so that everyone gets a fair turn", ["to make others wait longer", "to push others", "for no reason"], "Be patient."),
       ("What should you do if you see an elderly neighbour carrying a heavy load?", "offer to help", ["laugh", "walk away", "take their things"], "Helping is kind."),
       ("Why is a school a part of the community?", "children of the community learn there together", ["only teachers live there", "it is a market", "it has no use"], "Schools also host events for all."),
       ("What does 'unity in diversity' mean?", "people of different languages and religions living together in peace", ["everyone being the same", "fighting over differences", "living alone"], "India has many languages and festivals."),
       ("What is a community kitchen (langar)?", "a place where free food is cooked and served to everyone", ["a restaurant", "a shop", "a factory"], "Langars are served at gurudwaras."),
       ("Why should we be polite to delivery workers and drivers?", "they work hard for us and deserve respect", ["they do not matter", "politeness is only for teachers", "it is not needed"], "Respect everyone."),
       ("Which number can be dialled from any phone for all emergencies in India?", "112", ["1000", "555", "999"], "It connects to police, fire and ambulance."),
       ("What should you do if you see a fire in your street?", "move to safety and call 101 or 112", ["go close to watch", "throw paper on it", "hide inside"], "Tell an adult at once."),
       ("Why do people keep a list of important phone numbers at home?", "so they can get help quickly in an emergency", ["to play games", "to decorate the wall", "to sell them"], "Include family and doctor numbers."),
       ("What is a gram sabha?", "a meeting of all the adults of a village to discuss its needs", ["a cricket match", "a shop", "a wedding"], "It works with the panchayat."),
       ("Why do we share things like parks and buses in a community?", "it saves money and space and lets everyone use them", ["sharing is wrong", "only rich people can use them", "they are private"], "Take care of shared things."),
       ("Why do villages have common grazing land?", "so that everyone's cattle can graze", ["for building factories", "to keep cattle away", "it is private land"], "It is shared by the community."),
       ("What is a self-help group?", "a small group of people, often women, who save money and start work together", ["a sports team", "a school class", "a hospital ward"], "They help each other grow."),
       ("Why should we welcome people from other places into our community?", "it makes everyone feel safe and we learn new things", ["new people are always bad", "communities should be closed", "it causes problems"], "Kindness builds communities."),
       ("Who helps us when a water pipe bursts at home?", "a plumber", ["a carpenter", "a tailor", "a postman"], "Plumbers fix pipes and taps."),
       ("Who helps when there is no electricity in a house because of a fault?", "an electrician", ["a plumber", "a cobbler", "a farmer"], "Never touch wires yourself."),
       ("Who makes and repairs wooden furniture?", "a carpenter", ["a goldsmith", "a nurse", "a weaver"], "Carpenters use saws and hammers."),
       ("Why do communities make roads and bridges?", "to help people travel and carry goods", ["to stop travel", "to make rivers dirty", "for no reason"], "Good roads connect villages and towns.")]

# =================================================================== Chapter 2: exploring our neighbourhood
DIRS = ["north", "east", "south", "west"]
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
PLACES4 = ["the school", "the post office", "the park", "the market", "the hospital", "the temple", "the library", "the bus stop", "the bank", "the playground", "the well", "the police station"]


def c_dir(k=None):
    R = _R[0]
    a, b_ = R.sample(PLACES4, 2)
    d = R.choice(DIRS)
    if R.random() < 0.5:
        return tq("%s is to the %s of %s. In which direction is %s from %s?" % (_cap(a), d, b_, b_, a), OPP[d], [x for x in DIRS if x != OPP[d]],
                  "If %s is %s of %s, then %s is %s of %s." % (a, d, b_, b_, OPP[d], a))
    turn, off = R.choice([("turns right", 1), ("turns left", 3), ("turns around", 2)])
    a2 = DIRS[(DIRS.index(d) + off) % 4]
    n = kid()
    return tq("%s walks %s from %s and then %s. In which direction is %s walking now?" % (n, d, a, turn, n), a2, [x for x in DIRS if x != a2],
              "Facing %s, turning right gives %s, turning left gives %s and turning around gives %s." % (d, DIRS[(DIRS.index(d) + 1) % 4], DIRS[(DIRS.index(d) + 3) % 4], OPP[d]))


MAPS = [("a blue line or patch", "a river, a lake or the sea"), ("a green patch", "a forest, a park or fields"), ("a black line with small cross lines", "a railway line"),
        ("a red cross", "a hospital"), ("an arrow with N", "the north direction"), ("a key (legend)", "the meanings of the symbols used")]
TRANS = {"a means of land transport": ["a bus", "a bicycle", "a train", "an auto-rickshaw", "a bullock cart", "a metro train", "a truck"],
         "a means of water transport": ["a boat", "a ship", "a ferry", "a houseboat", "a canoe", "a motorboat"],
         "a means of air transport": ["an aeroplane", "a helicopter", "a hot-air balloon", "a seaplane", "a drone carrying parcels"]}
SIGNS = [("a red traffic light", "stop"), ("a green traffic light", "go"), ("a yellow traffic light", "get ready to stop or go"), ("a zebra crossing", "a safe place for people to cross the road"),
         ("a sign with a school bag and children", "a school is near, so drive slowly"), ("a sign with a red cross", "a hospital is nearby"), ("a footpath", "the side path where people walk"),
         ("a 'no horn' sign", "do not use the vehicle horn here")]
NBQ = [("What is a neighbourhood?", "the area around our home with houses, shops, parks and other places", ["a single room", "a far-off country", "the sky"], "We see neighbours there every day."),
       ("What is a map?", "a drawing of a place as seen from above", ["a photo of a person", "a story book", "a song"], "Maps help us find our way."),
       ("Why do maps use symbols?", "symbols take less space and are easy to understand", ["symbols make maps confusing", "to decorate them", "there is no reason"], "The key explains them."),
       ("What does the key of a map tell us?", "the meaning of the symbols and colours", ["the price of the map", "the name of the artist", "the time of day"], "It is also called a legend."),
       ("In which direction does the Sun rise?", "east", ["west", "north", "south"], "It sets in the west."),
       ("If you face the rising Sun, what is behind you?", "west", ["east", "north", "south"], "North is on your left."),
       ("If you face north, which direction is on your right?", "east", ["west", "south", "north"], "West is on your left."),
       ("What does a compass show?", "the north–south direction", ["the time", "the temperature", "the weight"], "Its needle points north."),
       ("What is a landmark?", "a well-known place or object that helps people find their way", ["a type of food", "a toy", "a cloud"], "A big temple or a clock tower can be a landmark."),
       ("Why should we walk on the footpath?", "it keeps us safe from traffic", ["it is faster", "it is muddy", "cars use it"], "Cross only at zebra crossings."),
       ("How should we cross a road?", "at a zebra crossing, after looking right, left and right again", ["running between cars", "from behind a parked bus", "while looking at a phone"], "Wait for the green signal."),
       ("Why does a neighbourhood need a health centre?", "people can get treatment nearby", ["for shopping", "for playing cricket", "to keep cows"], "Primary health centres serve villages."),
       ("What can you learn by walking around your neighbourhood?", "where things are and who helps us", ["nothing at all", "only the weather", "only games"], "Make a simple map of it."),
       ("Why is a metro train useful in a big city?", "it carries many people quickly without traffic jams", ["it is very slow", "it carries only goods", "it pollutes more than cars"], "Delhi, Kolkata and Bengaluru have metros."),
       ("Which transport is best for carrying heavy goods over long distances on land cheaply?", "a goods train", ["a bicycle", "a helicopter", "an auto-rickshaw"], "Trucks are also used."),
       ("Why is cycling good for short trips?", "it causes no pollution and keeps us fit", ["it pollutes the air", "it needs petrol", "it is very slow for everything"], "Wear a helmet."),
       ("What is a scale on a map?", "it shows how distances on the map compare with real distances", ["the weight of the map", "the colour of the map", "a fish's skin"], "1 cm might stand for 1 km."),
       ("Why do people use public transport?", "it saves money and fuel and reduces traffic", ["it is always the slowest", "it makes more smoke", "nobody uses it"], "Buses carry many people."),
       ("Which direction is opposite to east?", "west", ["north", "south", "east"], "North is opposite to south."),
       ("If the school is east of your house, where is your house from the school?", "west", ["east", "north", "south"], "Opposite directions."),
       ("What do we call the place where buses stop to pick up people?", "a bus stop", ["a railway station", "an airport", "a harbour"], "Trains stop at stations."),
       ("What do we call the place where ships come and go?", "a harbour or port", ["a bus stop", "an airport", "a garage"], "Mumbai and Chennai have big ports."),
       ("What is a 'speed breaker'?", "a raised strip on a road that makes vehicles slow down", ["a fast car", "a traffic light", "a bridge"], "They are put near schools."),
       ("Why do we need street lights?", "so that people can see and move safely at night", ["to make the day bright", "to dry clothes", "to heat the road"], "Many now use solar power."),
       ("What are the four main directions?", "north, south, east and west", ["up, down, left and right", "front, back, top and bottom", "sun, moon, star and sky"], "They are called cardinal directions."),
       ("Which landmark helps you find north at night?", "the Pole Star", ["the Moon", "a street light", "a cloud"], "It stays in the northern sky."),
       ("What should you do if you get lost in a new place?", "stay calm, go to a shop or police officer and give your parent's phone number", ["run around", "go with a stranger", "cry and hide"], "Remember your address."),
       ("Why do people put up signboards in a neighbourhood?", "to give directions and information", ["to block the road", "to hide shops", "for no reason"], "Read signs carefully.")]

# =================================================================== Chapter 3: nature trail
BEAK = [("a hooked beak, like an eagle's", "tearing meat"), ("a long, thin beak, like a sunbird's", "sucking nectar from flowers"), ("a broad, flat beak, like a duck's", "straining food from water"),
        ("a short, strong beak, like a sparrow's", "cracking seeds"), ("a strong, pointed beak, like a woodpecker's", "drilling holes in tree bark"),
        ("a long, pointed beak, like a kingfisher's", "catching fish"), ("a curved, strong beak, like a parrot's", "cracking nuts and biting into fruits")]
FEET = [("a sparrow", "toes that curl round and grip branches"), ("an eagle", "sharp curved claws (talons) for catching prey"), ("a duck", "webbed toes for swimming"),
        ("a woodpecker", "two toes forward and two back for climbing tree trunks"), ("a heron", "long thin legs for wading in water"), ("a hen", "strong toes and claws for scratching the ground")]
INS = {"an insect (six legs)": ["a butterfly", "an ant", "a honeybee", "a grasshopper", "a ladybird", "a housefly", "a dragonfly", "a beetle", "a mosquito", "a cockroach", "a termite"],
       "not an insect": ["a spider", "an earthworm", "a snail", "a centipede", "a scorpion", "a frog", "a lizard", "a crab", "a millipede"]}
TREES = [("the banyan", "roots that hang down from its branches"), ("the neem", "bitter leaves and twigs used to clean teeth"), ("the peepal", "heart-shaped leaves with long tips"),
         ("the gulmohar", "bright red-orange flowers in summer"), ("the amaltas", "bunches of bright yellow flowers hanging down"), ("the coconut palm", "a tall, straight trunk with leaves only at the top"),
         ("the palash (flame of the forest)", "bright orange flowers when the tree has no leaves"), ("bamboo", "tall, hollow, jointed stems growing in clumps"),
         ("the tamarind", "small leaflets and curved brown pods with sour pulp"), ("the drumstick (moringa)", "long, thin green pods eaten as a vegetable")]
TRAIL = {"good behaviour on a nature trail": ["walking quietly to hear birds", "staying on the path", "carrying a notebook to draw what you see", "taking your litter back home",
                                             "watching animals from a distance", "using binoculars to see birds", "wearing shoes and a cap", "carrying a water bottle"],
         "bad behaviour on a nature trail": ["shouting and playing loud music", "plucking flowers and leaves", "throwing stones at birds", "leaving wrappers on the path",
                                            "chasing butterflies", "carving names on trees", "feeding chips to monkeys", "breaking branches for walking sticks"]}
NTQ = [("What is a nature trail?", "a walk to observe plants, animals and their surroundings", ["a car race", "a cooking class", "a shopping trip"], "Walk slowly and observe."),
       ("Which instrument helps us see birds far away?", "binoculars", ["a thermometer", "a stopwatch", "a weighing scale"], "A magnifying glass helps to see small insects."),
       ("Which instrument helps us see tiny insects and leaf veins clearly?", "a magnifying glass", ["binoculars", "a telescope", "a compass"], "It makes things look bigger."),
       ("How many legs does an insect have?", "six", ["eight", "four", "ten"], "Spiders have eight legs, so they are not insects."),
       ("How many legs does a spider have?", "eight", ["six", "four", "two"], "Spiders are not insects."),
       ("What are the three main body parts of an insect?", "head, thorax and abdomen", ["head, neck and tail", "only head and tail", "wings, legs and roots"], "Legs are on the thorax."),
       ("Why should we observe animals quietly?", "noise frightens them away", ["noise attracts all animals", "animals like noise", "it does not matter"], "Patience helps."),
       ("What signs tell us that animals have been on a trail?", "footprints, feathers, droppings and nests", ["plastic bags", "car tyres", "street lights"], "These are animal signs."),
       ("Why do butterflies visit flowers?", "to drink nectar", ["to eat leaves", "to sleep", "to lay stones"], "They help pollinate flowers."),
       ("What does a caterpillar become?", "a butterfly or a moth", ["a bird", "a frog", "a spider"], "It forms a pupa first."),
       ("Why do some insects have the colours of leaves or bark?", "it helps them hide from enemies", ["to look pretty only", "to attract birds", "no reason"], "This is camouflage."),
       ("What is camouflage?", "colours or shapes that help an animal blend with its surroundings", ["a kind of food", "a type of nest", "a bird song"], "A green grasshopper hides in grass."),
       ("Why do we record observations in a nature diary?", "to remember and compare what we saw", ["to waste paper", "to copy friends", "it is not useful"], "Draw and write the date."),
       ("What do we call young leaves that are soft and reddish in some trees?", "new leaves", ["dead leaves", "roots", "seeds"], "Mango trees have reddish new leaves."),
       ("Why do some trees shed their leaves?", "to save water in the dry season", ["because they are dying", "to feed birds", "because of noise"], "New leaves grow later."),
       ("Which bird is the national bird of India?", "the peacock (Indian peafowl)", ["the sparrow", "the crow", "the parrot"], "Peacocks dance with their tail feathers spread."),
       ("Which animal is the national animal of India?", "the tiger", ["the lion", "the elephant", "the cow"], "Project Tiger protects tigers."),
       ("Where do frogs lay their eggs?", "in water", ["in trees", "in sand", "in nests of grass"], "Tadpoles hatch from them."),
       ("Why do bird watchers wear dull-coloured clothes?", "bright colours can scare birds", ["dull clothes are warmer", "birds love bright colours", "for fashion"], "Blend in quietly."),
       ("What does an ant do when it finds food?", "it leaves a scent trail so other ants can follow", ["it hides it forever", "it eats it all alone", "it throws it away"], "That is why ants walk in lines."),
       ("Which bird can turn its head almost all the way round and hunts at night?", "the owl", ["the parrot", "the pigeon", "the hen"], "Its big eyes help it see in the dark."),
       ("Which bird is known for building hanging nests woven from grass?", "the weaver bird", ["the crow", "the eagle", "the pigeon"], "The male weaves the nest."),
       ("What is the trunk of a tree covered with?", "bark", ["feathers", "scales", "petals"], "Bark protects the tree."),
       ("Why should we not touch unknown plants or insects on a trail?", "some may sting, bite or cause itching", ["all are harmless", "touching makes them grow", "it is required"], "Look, but do not touch."),
       ("Why do we see more butterflies after the rains?", "many plants flower then and caterpillars have plenty of leaves", ["rain makes butterflies", "butterflies love mud only", "there is no reason"], "The monsoon is full of life."),
       ("What is a 'bird call'?", "the sound a bird makes to communicate", ["a phone call", "a bird's nest", "a bird's feather"], "Each bird has its own call."),
       ("What are the tiny holes on the underside of leaves called?", "stomata", ["roots", "veins", "petals"], "They let air in and out."),
       ("Which part of the trail shows where water flows after rain?", "a stream or a dry stream bed", ["a bus stop", "a street light", "a shop"], "Water shapes the land.")]

# =================================================================== Chapter 4: growing up with nature
YOUNG = [("a cat", "a kitten"), ("a dog", "a puppy"), ("a cow", "a calf"), ("a hen", "a chick"), ("a frog", "a tadpole"), ("a horse", "a foal"), ("a goat", "a kid"),
         ("a sheep", "a lamb"), ("a lion", "a cub"), ("a duck", "a duckling"), ("a butterfly", "a caterpillar")]
EGG = {"an animal that lays eggs": ["a hen", "a crow", "a frog", "a snake", "a turtle", "a fish", "a butterfly", "a lizard"],
       "an animal that gives birth to young ones": ["a cow", "a cat", "a dog", "a human", "an elephant", "a goat", "a monkey", "a whale"]}
DISP = {"spread by the wind": ["cotton seeds", "dandelion seeds", "the winged seeds of the drumstick tree", "madar (aak) seeds with silky hairs"],
        "spread by water": ["a coconut", "lotus seeds", "mangrove seedlings"],
        "spread by sticking to animals' fur or our clothes": ["Xanthium burrs", "grass seeds with hooks", "the spiky seeds of chirchita"],
        "spread when the pod bursts open": ["balsam seeds", "pea and bean pods drying in the sun", "the seeds of the castor plant"],
        "spread by animals eating the fruit": ["guava seeds", "seeds of berries", "mango stones carried by bats and monkeys", "peepal seeds"]}
CYC = [("a plant", ["seed", "sprout", "seedling", "young plant", "plant with flowers", "fruit with seeds"]), ("a butterfly", ["egg", "caterpillar", "pupa", "butterfly"]),
       ("a frog", ["egg", "tadpole", "froglet", "frog"]), ("a hen", ["egg", "chick", "young hen", "hen"]), ("a human", ["baby", "toddler", "child", "teenager", "adult", "older adult"]),
       ("a mosquito", ["egg", "larva", "pupa", "mosquito"])]


def c_cyc(k=None):
    R = _R[0]
    who, st = R.choice(CYC)
    i = R.randrange(len(st) - 1)
    a = st[i + 1]
    other = sorted({x for _, s_ in CYC for x in s_} - set(st))
    w = [x for x in st if x not in (a, st[i])] + R.sample(other, 2)
    return tq("In the life of %s, what comes just after the stage '%s'?" % (who, st[i]), a, R.sample(w, 3), "The stages are " + " → ".join(st) + ".")


GQ = [("What does a seed need to sprout?", "water, air and warmth", ["darkness only", "salt and sugar", "plastic"], "Soil and light are needed later for growing."),
      ("Which part comes out first when a seed sprouts?", "the root", ["the flower", "the fruit", "the leaf"], "Then the shoot grows up."),
      ("Why do farmers soak some seeds before sowing?", "soaking softens the seed coat and helps them sprout faster", ["to make them sweet", "to kill them", "to change their colour"], "Chana and moong sprout after soaking."),
      ("What happens to a seed kept dry in a box?", "it does not sprout", ["it grows into a tree at once", "it turns into a stone", "it flowers"], "It needs water."),
      ("Why are seeds spread far from the parent plant?", "so that young plants get enough space, light and water", ["so they get lost", "so birds can play", "there is no reason"], "Wind, water and animals spread seeds."),
      ("How do coconuts spread to faraway beaches?", "they float on water", ["they fly", "they walk", "they stick to animals"], "Their husk is light and full of air."),
      ("Why are cotton seeds light and hairy?", "so that the wind can carry them", ["so that water can sink them", "so that animals eat them", "so they stay near the plant"], "Dandelions are similar."),
      ("What do we call the change from a tadpole to a frog?", "metamorphosis", ["germination", "photosynthesis", "pollination"], "Butterflies also go through it."),
      ("Why do young animals stay with their parents?", "they need food, protection and to learn skills", ["they are lazy", "parents force them", "for no reason"], "Some young birds learn to fly from their parents."),
      ("Which young animal drinks its mother's milk?", "a calf", ["a chick", "a tadpole", "a caterpillar"], "Mammals feed their young on milk."),
      ("How do we know a child is growing?", "height and weight increase and they learn new things", ["their name changes", "their clothes change colour", "they stop eating"], "Growth is a sign of life."),
      ("What is germination?", "a seed starting to grow into a new plant", ["a flower falling", "a fruit ripening", "a leaf drying"], "It needs water, air and warmth."),
      ("What does a caterpillar mainly eat?", "leaves", ["meat", "stones", "milk"], "It eats a lot before becoming a pupa."),
      ("Why do some birds build nests before laying eggs?", "to keep the eggs and chicks safe and warm", ["to store food only", "to play", "to sleep only"], "Nests are made of twigs and grass."),
      ("How long does a hen sit on its eggs before chicks hatch?", "about 21 days", ["one hour", "one year", "one day"], "The warmth helps the chicks grow."),
      ("What should we do to help a plant grow well?", "give it water, sunlight and good soil", ["keep it in a dark cupboard", "pour oil on it", "never water it"], "Remove weeds too."),
      ("What happens to the leaves of a plant kept away from light?", "they turn pale yellow", ["they turn dark green", "they turn red", "they turn blue"], "Plants need light to make food."),
      ("Why do we plant saplings in the monsoon?", "the soil is wet and they get plenty of water", ["it is very hot", "there is no rain", "the soil is frozen"], "Many schools plant trees in July."),
      ("Which young animal hatches from an egg in water?", "a tadpole", ["a puppy", "a calf", "a kitten"], "It breathes with gills."),
      ("What is a seedling?", "a young plant grown from a seed", ["an old tree", "a dried flower", "a fruit"], "It has its first leaves."),
      ("Which part of a plant turns into a fruit?", "the flower", ["the root", "the stem", "the leaf"], "The fruit protects the seeds."),
      ("What do we call the baby of a kangaroo?", "a joey", ["a calf", "a cub", "a puppy"], "It grows in its mother's pouch."),
      ("Why do some animals change their homes as they grow?", "they need more space or a different kind of home", ["they get bored", "homes disappear", "they cannot see"], "A tadpole in water becomes a frog that also lives on land."),
      ("Why do human babies need a lot of care?", "they cannot feed or protect themselves", ["they can do everything", "they need no food", "they are adults"], "Parents and families care for them."),
      ("What makes a plant bend towards a window?", "it grows towards the light", ["it is pushed by air", "it is heavy", "it likes the glass"], "Turn the pot to make it grow straight."),
      ("Why should we not pluck unripe fruits?", "the seeds inside are not ready and the fruit is not good to eat", ["unripe fruits are sweeter", "it helps the tree", "birds want us to"], "Let fruits ripen."),
      ("What is a sapling?", "a young tree", ["a seed", "a flower", "a fruit"], "Saplings grow into trees.")]

# =================================================================== Chapter 5: food for health
NUTR4 = [("carbohydrates", "giving us energy to work and play"), ("proteins", "helping the body grow and repair itself"), ("fats", "giving a lot of energy and keeping us warm"),
         ("vitamins and minerals", "protecting us from diseases"), ("dietary fibre", "helping food move through the stomach and intestines"), ("water", "carrying nutrients and keeping the body cool")]
GROUP = {"an energy-giving food": ["rice", "wheat roti", "potato", "jaggery", "ragi", "ghee", "bajra roti"],
         "a body-building food": ["dal", "milk", "egg", "paneer", "soybean", "fish", "rajma"],
         "a protective food (rich in vitamins and minerals)": ["spinach", "orange", "carrot", "guava", "amla", "papaya", "tomato"]}
PRES4 = [("pickles", "salt, oil and spices"), ("jam", "lots of sugar"), ("papad", "drying in the sun"), ("raisins", "drying grapes"),
         ("milk", "boiling it and keeping it in a refrigerator"), ("dried fish", "salting and drying in the sun"), ("murabba", "cooking fruit in sugar syrup"), ("frozen peas", "freezing")]
FNUT = [("rice", "carbohydrates"), ("dal", "proteins"), ("ghee", "fats"), ("an orange", "vitamin C"), ("milk", "calcium"), ("spinach", "iron"), ("a carrot", "vitamin A"),
        ("an egg", "proteins"), ("ragi", "calcium"), ("jaggery", "iron"), ("amla", "vitamin C"), ("butter", "fats"), ("a guava", "vitamin C"), ("paneer", "proteins"), ("bajra", "iron"), ("papaya", "vitamin A"), ("groundnuts", "proteins")]
FHQ = [("What is a balanced diet?", "food that has all the nutrients the body needs in the right amounts", ["food with only sweets", "only one kind of food", "a lot of oily food"], "Include grains, pulses, vegetables, fruits and milk."),
       ("Why should we eat green leafy vegetables?", "they are rich in vitamins, minerals and fibre", ["they have no nutrients", "they are full of fat", "they are sweets"], "Spinach and methi are examples."),
       ("Why are millets good for health?", "they are rich in fibre and minerals like calcium and iron", ["they have no nutrients", "they are made in factories", "they are full of sugar"], "Ragi, jowar and bajra are millets."),
       ("Why should we not eat too much fried food?", "too much fat can make us unhealthy", ["fried food builds bones", "it is a protective food", "it has lots of fibre"], "Eat it only sometimes."),
       ("Why should we drink milk?", "it has calcium for strong bones and teeth", ["it has no nutrients", "it makes bones weak", "it is a fat only"], "Curd and paneer also have calcium."),
       ("What happens if we do not get enough vitamin C?", "gums may bleed and wounds heal slowly", ["we grow taller", "nothing at all", "our hair turns blue"], "Eat citrus fruits and amla."),
       ("Why do we preserve food?", "so it does not spoil and can be used later", ["to make it rot faster", "to change its colour only", "to waste it"], "Salt, sugar, drying and cold help."),
       ("Why does food spoil?", "tiny germs grow on it", ["it gets lonely", "it is too clean", "it is cold"], "Spoilt food can make us ill."),
       ("Which of these is a sign that food has gone bad?", "a bad smell and fuzzy mould", ["a fresh smell", "a bright colour", "a crispy feel"], "Throw away spoilt food."),
       ("Why should we wash our hands before cooking and eating?", "to remove germs", ["to make food taste salty", "to waste water", "to change the food's colour"], "Use soap."),
       ("What is the main source of energy in an Indian thali?", "rice or roti", ["salt", "pickle", "water"], "Dal gives protein."),
       ("Why is breakfast called the most important meal by many people?", "it gives energy after the long night", ["it is the smallest meal", "it makes us sleepy", "it is not needed"], "A good breakfast helps us concentrate."),
       ("Why is it good to eat seasonal fruits and vegetables?", "they are fresh, tasty and full of nutrients", ["they are always stale", "they have no nutrients", "they are made in factories"], "Mangoes in summer, oranges in winter."),
       ("Why should we not skip meals?", "the body needs regular energy and nutrients", ["skipping meals makes us strong", "it saves food", "it is healthy"], "Eat on time."),
       ("What is the mid-day meal scheme (PM POSHAN)?", "free cooked meals given to children in government schools", ["a cricket match", "a festival", "a train service"], "It helps children get nutrition and attend school."),
       ("What does 'iodised salt' prevent?", "goitre, a swelling in the neck", ["a cold", "a broken bone", "tooth decay"], "Iodine is needed in small amounts."),
       ("What happens if we eat too many sweets?", "our teeth may decay and we may gain too much weight", ["teeth become stronger", "we grow taller", "nothing happens"], "Brush after sweets."),
       ("Which food helps prevent constipation?", "food rich in fibre, such as fruits, vegetables and whole grains", ["only sugar", "only oil", "only meat"], "Drink enough water too."),
       ("Why should we drink water instead of sugary cold drinks?", "cold drinks have a lot of sugar and no nutrients", ["cold drinks are healthier", "water has sugar", "cold drinks build bones"], "Lemon water or buttermilk are better."),
       ("Why is sprouting good for pulses?", "it increases their nutrients and makes them easy to digest", ["it removes all nutrients", "it makes them poisonous", "it makes them sweets"], "Moong sprouts are popular."),
       ("Which nutrient do we mainly get from pulses such as dal?", "proteins", ["fats only", "water only", "fibre only"], "Pulses are body-building foods."),
       ("Why do athletes eat more energy-giving foods?", "they use a lot of energy in sports", ["they need less energy", "they never run", "energy food is a medicine"], "They also need protein for muscles."),
       ("What does 'mindful eating' mean?", "eating slowly and noticing when we are full", ["eating very fast", "eating while watching TV", "skipping meals"], "Chew well."),
       ("Why should food be covered?", "to keep away flies and dust", ["to make it cold", "to make it taste better", "to hide it"], "Flies carry germs."),
       ("Which of these is a traditional way to keep water and buttermilk cool?", "storing them in an earthen pot", ["a plastic bag in the sun", "a metal box on the stove", "an open bucket in the sun"], "The pot cools by evaporation."),
       ("Why do people in cold places eat foods with more fat?", "fat gives energy and helps keep the body warm", ["fat cools the body", "fat is a vitamin", "they do not like vegetables"], "Ghee and butter are common there."),
       ("Why is it important to eat a variety of foods?", "no single food has all the nutrients we need", ["one food has everything", "variety makes us ill", "it wastes food"], "Make your plate colourful."),
       ("Why should we store grains in dry places?", "moisture helps fungi and insects to spoil them", ["wet grain is better", "grains grow in water", "it does not matter"], "Neem leaves keep insects away.")]


def UNITS4a():
    b = {k: once_maker(v) for k, v in [("lt", LTQ), ("nb", NBQ), ("nt", NTQ), ("g", GQ), ("fh", FHQ)]}
    helper = pairs(HELPER, "What does %s do for the community?", "Who is responsible for %s?")
    place = pairs(PLACE, "What do people go to %s for?", "Which place in a community is for %s?")
    emer = pairs(EMER, "Which service do you get by dialling %s in India?", "Which number do you dial in India for %s?")
    tog = odd_one(TOG, "Which of these is %s?", "Which of these is not %s?")
    maps = pairs(MAPS, "On a map, what does %s usually show?", "Which map symbol shows %s?")
    trans = odd_one(TRANS, "Which of these is %s?", "Which of these is not %s?")
    signs = pairs(SIGNS, "What does %s mean?", "What tells road users this: %s?")
    beak = pairs(BEAK, "What is %s best for?", "Which kind of beak is best for %s?")
    feet = pairs(FEET, "What kind of toes or claws does %s have?", "Which bird has %s?")
    ins = odd_one(INS, "Which of these is %s?", "Which of these is not %s?")
    trees = pairs(TREES, "Which feature helps you recognise %s?", "Which tree has %s?")
    trail = odd_one(TRAIL, "Which of these is %s?", "Which of these is not %s?")
    young = pairs(YOUNG, "What is the young one of %s called?", "Whose young one is %s?")
    egg = odd_one(EGG, "Which of these is %s?", "Which of these is not %s?")
    disp = odd_one(DISP, "Which of these seeds are %s?", "Which of these seeds are not %s?")
    nutr = pairs(NUTR4, "What do %s mainly do for our body?", "Which nutrient is mainly needed for %s?")
    grp = odd_one(GROUP, "Which of these is %s?", "Which of these is not %s?")
    pres = pairs(PRES4, "How are %s usually preserved?", "Which food is preserved using %s?")
    fnut = pairs(FNUT, "Which nutrient is %s especially rich in?")
    return [
        U(1, "living-together", 1, CO,
          "Living together in a community: community helpers and the work they do; public places and services; the panchayat and cooperatives; sharing, rules and caring for public property; getting help in an emergency (summary of NCERT Our Wondrous World Chapter 1).",
          "Living Together", "living together",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 1: community helpers, public places, the panchayat, cooperatives, sharing and rules, and emergency numbers. 100 questions with answers.",
          "We depend on each other in a community.", "Helpers, shared places and fair rules keep us together.",
          "<p>A community is a group of people who live in the same area and share places such as parks, markets, schools and hospitals. Community helpers such as doctors, farmers, sanitation workers, firefighters and postmen do work that everyone needs. In a village, the elected panchayat, led by the sarpanch, looks after common needs.</p>"
          "<p>Living together means sharing fairly, following rules, keeping public places clean and helping neighbours. Cooperatives such as Amul let people work together and share the profit. In an emergency, dial 112.</p>",
          [("Who puts out fires?", ["fire engines"], "a firefighter"), ("Where do we post letters?", ["stamps and parcels"], "the post office")],
          ["Thinking public property belongs to nobody.", "Pushing ahead in a queue.", "Not knowing the emergency number."],
          [("What is a panchayat?", "An elected body of villagers, led by the sarpanch, that takes decisions for the village."),
           ("Why do people in a community depend on each other?", "Nobody can do every job alone, so farmers, doctors, teachers and many others help one another.")],
          lambda: [("Our community", [(b["lt"], 12), (tog, 8)]), ("Community helpers", [(helper, 16), (b["lt"], 4)]), ("Places in a community", [(place, 14), (b["lt"], 6)]),
                   ("Living together well", [(tog, 14), (emer, 6)]), ("Mixed problems", [(b["lt"], 6), (helper, 8), (tog, 4), (place, 2)])]),
        U(2, "exploring-our-neighbourhood", 2, CO,
          "Places in our neighbourhood; reading simple maps, symbols and the key; directions north, south, east and west; means of transport on land, water and air; road signs and road safety (summary of NCERT Our Wondrous World Chapter 2).",
          "Exploring Our Neighbourhood", "exploring our neighbourhood",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 2: places in the neighbourhood, maps and symbols, directions, means of transport and road safety. 100 questions with answers.",
          "Maps and directions help us find our way.", "The Sun rises in the east and sets in the west.",
          "<p>A map is a drawing of a place as seen from above. It uses symbols and colours, explained in its key: blue for water, green for forests and parks, and lines for roads and railways. The four main directions are north, south, east and west; the Sun rises in the east and a compass needle points north.</p>"
          "<p>We travel by land (bus, train, bicycle), water (boat, ship) and air (aeroplane, helicopter). Road signs keep us safe: red means stop, green means go and a zebra crossing is the safe place to cross the road.</p>",
          [("The park is north of the school. The school is…", ["opposite direction"], "south of the park"), ("A ferry is…", ["it carries people across water"], "water transport")],
          ["Mixing up east and west.", "Crossing the road anywhere.", "Thinking a map shows things from the side."],
          [("What does the key of a map tell us?", "It explains what the symbols and colours on the map stand for."),
           ("How can we find directions without a compass?", "The Sun rises in the east and sets in the west; at night the Pole Star shows the north.")],
          lambda: [("Our neighbourhood", [(b["nb"], 12), (signs, 8)]), ("Maps and symbols", [(maps, 8), (b["nb"], 10), (trans, 2)]), ("Directions", [(c_dir, 20)]),
                   ("Transport and road safety", [(trans, 14), (signs, 4), (c_dir, 2)]), ("Mixed problems", [(c_dir, 12), (trans, 8)])]),
        U(3, "nature-trail", 3, LA,
          "Going on a nature trail: observing plants, birds and insects with care; using binoculars and a magnifying glass; beaks and toes of birds; insects and other small animals; recognising trees; signs of animals; behaving well in nature (summary of NCERT Our Wondrous World Chapter 3).",
          "Nature Trail", "nature trail",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 3: observing on a nature trail, binoculars and magnifying glasses, bird beaks and toes, insects, trees and good trail behaviour. 100 questions with answers.",
          "Observe quietly; leave nature as you found it.", "A bird's beak and toes suit its food and home.",
          "<p>On a nature trail we walk slowly and quietly, using binoculars to watch birds and a magnifying glass to look at insects and leaves. We note footprints, feathers and nests, and we draw what we see in a nature diary. Insects have six legs and three body parts; spiders, with eight legs, are not insects.</p>"
          "<p>Birds' beaks and toes suit their food and habits: an eagle has a hooked beak and talons, a duck a flat beak and webbed toes, a woodpecker a strong pointed beak and toes for climbing. We stay on the path, do not pluck flowers and take our litter home.</p>",
          [("A spider: insect or not?", ["count its legs"], "not an insect (eight legs)"), ("A flat, broad beak is for…", ["a duck's beak"], "straining food from water")],
          ["Calling a spider an insect.", "Plucking flowers on a trail.", "Thinking all birds have the same kind of toes."],
          [("How can you tell an insect?", "It has six legs and three body parts: head, thorax and abdomen."),
           ("Why do birds have different beaks?", "Each beak suits the bird's food: hooked for meat, thin for nectar, strong and short for seeds.")],
          lambda: [("On the trail", [(b["nt"], 10), (trail, 10)]), ("Birds' beaks and toes", [(beak, 9), (feet, 8), (b["nt"], 3)]), ("Insects and small animals", [(ins, 16), (b["nt"], 4)]),
                   ("Trees on the trail", [(trees, 14), (b["nt"], 6)]), ("Mixed problems", [(ins, 8), (trail, 8), (beak, 2), (trees, 2)])]),
        U(4, "growing-up-with-nature", 4, LA,
          "How plants grow from seeds; what seeds need to sprout; how seeds are spread; young ones of animals; animals that lay eggs and those that give birth; life cycles of plants and animals; growing up (summary of NCERT Our Wondrous World Chapter 4).",
          "Growing Up With Nature", "growing up with nature",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 4: seeds and sprouting, how seeds spread, young ones of animals, egg-laying animals, and life cycles of plants and animals. 100 questions with answers.",
          "Seeds need water, air and warmth to sprout.", "All living things grow and change.",
          "<p>A seed sprouts when it gets water, air and warmth; first the root comes out, then the shoot. It grows into a seedling and then a plant with flowers, fruits and seeds. Seeds are spread by wind (cotton), water (coconut), animals (burrs that stick, fruits that are eaten) and by pods that burst.</p>"
          "<p>Animals grow too. Some lay eggs (hens, frogs, snakes) and some give birth (cows, cats, humans). Their young have special names: a calf, a kitten, a chick, a tadpole. Frogs and butterflies change shape as they grow: this is metamorphosis.</p>",
          [("Young one of a sheep?", ["it says baa"], "a lamb"), ("How do cotton seeds spread?", ["light and fluffy"], "by the wind")],
          ["Thinking seeds need light to sprout.", "Thinking all animals lay eggs.", "Calling a tadpole a fish."],
          [("What does a seed need to sprout?", "Water, air and warmth; light and soil are needed as the young plant grows."),
           ("Why are seeds spread far from the parent plant?", "So that the young plants get enough space, light and water to grow.")],
          lambda: [("Seeds and sprouting", [(b["g"], 12), (disp, 8)]), ("How seeds spread", [(disp, 14), (b["g"], 6)]), ("Young ones of animals", [(young, 14), (egg, 6)]),
                   ("Eggs, babies and life cycles", [(egg, 10), (c_cyc, 10)]), ("Mixed problems", [(c_cyc, 4), (egg, 8), (b["g"], 4), (young, 4)])]),
        U(5, "food-for-health", 5, HW,
          "Nutrients in food and their work; energy-giving, body-building and protective foods; a balanced diet; millets and seasonal foods; how food spoils and ways of preserving it; healthy eating habits (summary of NCERT Our Wondrous World Chapter 5).",
          "Food for Health", "food for health",
          "Free CBSE Class 4 EVS worksheets for NCERT Our Wondrous World Chapter 5: nutrients, energy-giving, body-building and protective foods, a balanced diet, millets, food spoilage and preservation. 100 questions with answers.",
          "A balanced diet keeps us healthy.", "Energy-giving, body-building and protective foods.",
          "<p>Food gives us nutrients. Carbohydrates and fats give energy (rice, roti, ghee), proteins build the body (dal, milk, eggs), and vitamins and minerals protect us (spinach, oranges, carrots). Fibre and water are needed too. A balanced diet has all of these in the right amounts; millets such as ragi and jowar are especially nutritious.</p>"
          "<p>Food spoils when germs grow on it. We preserve it with salt and oil (pickles), sugar (jam), drying (papad, raisins), boiling and cold (milk). Eat on time, chew well, wash hands and keep food covered.</p>",
          [("Dal is mainly…", ["it helps us grow"], "a body-building food (protein)"), ("Jam is preserved with…", ["it is very sweet"], "sugar")],
          ["Thinking sweets are energy-giving and therefore healthy in any amount.", "Eating uncovered food.", "Skipping breakfast."],
          [("What is a balanced diet?", "A diet with carbohydrates, proteins, fats, vitamins, minerals, fibre and water in the right amounts."),
           ("How is food preserved at home?", "By salting, adding sugar or oil, drying in the sun, boiling and keeping it cold.")],
          lambda: [("Nutrients", [(nutr, 8), (b["fh"], 12)]), ("Food groups", [(grp, 14), (fnut, 6)]), ("A balanced diet", [(b["fh"], 6), (grp, 14)]),
                   ("Preserving food", [(pres, 12), (grp, 8)]), ("Mixed problems", [(grp, 10), (fnut, 6), (b["fh"], 4)])]),
    ]
