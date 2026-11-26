# -*- coding: utf-8 -*-
"""Class 5 EVS (NCERT Our Wondrous World, chapters 6–10): question makers and UNITS5b()."""
from uk_alsci import tq, once_maker
from in_sci import pairs, _R, U
from in_sci6a import odd_one, _cap
from in_sci5a import LA, HW, II, TA, AP
from in_sci3a import kid

# =================================================================== Chapter 6: some unique places
UNIQ = [("the living root bridges of Meghalaya", "bridges grown from the roots of rubber fig trees"), ("Majuli", "the largest river island in India, in the Brahmaputra"),
        ("the Rann of Kutch", "a white salt desert that floods in the monsoon"), ("Loktak Lake in Manipur", "a lake with floating islands of plants called phumdis"),
        ("Lakshadweep", "small coral islands in the Arabian Sea"), ("the Valley of Flowers", "a high Himalayan valley full of wild flowers in the monsoon"),
        ("Chilika Lake", "a huge lagoon in Odisha where flamingos and many migratory birds come"), ("Hampi", "the ruins of the Vijayanagara empire with stone temples and chariots"),
        ("the Konark Sun Temple", "a temple shaped like a giant chariot with stone wheels"), ("the Ajanta caves", "rock-cut caves with ancient Buddhist paintings"),
        ("the Sundarbans", "the largest mangrove forest in the world, home of the Bengal tiger"), ("Kaziranga National Park", "home of the one-horned rhinoceros"),
        ("Mawsynram", "one of the wettest places on Earth"), ("the Taj Mahal", "a white marble tomb built by Shah Jahan")]
STATE6 = [("the Taj Mahal", "Uttar Pradesh"), ("the Qutub Minar", "Delhi"), ("Hampi", "Karnataka"), ("the Konark Sun Temple", "Odisha"), ("the Ajanta and Ellora caves", "Maharashtra"),
          ("Kaziranga National Park", "Assam"), ("the Sanchi Stupa", "Madhya Pradesh"), ("Loktak Lake", "Manipur"), ("the living root bridges", "Meghalaya"),
          ("the Valley of Flowers", "Uttarakhand"), ("the Rann of Kutch", "Gujarat"), ("the Golden Temple", "Punjab"), ("the Mahabalipuram shore temple", "Tamil Nadu"), ("Hawa Mahal", "Rajasthan")]
CITYDIR = [("Srinagar", "Delhi", "north"), ("Chennai", "Delhi", "south"), ("Kolkata", "Mumbai", "east"), ("Ahmedabad", "Kolkata", "west"),
           ("Guwahati", "Delhi", "east"), ("Thiruvananthapuram", "Bengaluru", "south"), ("Jaipur", "Lucknow", "west"), ("Shimla", "Chandigarh", "north"), ("Bhubaneswar", "Bhopal", "east")]
OPPD = {"north": "south", "south": "north", "east": "west", "west": "east"}


def c_city(k=None):
    R = _R[0]
    a, b_, d = R.choice(CITYDIR)
    if R.random() < 0.5:
        return tq("On a map of India, in which direction is %s from %s?" % (a, b_), d, [x for x in OPPD if x != d], "%s is %s of %s." % (a, d, b_))
    return tq("On a map of India, in which direction is %s from %s?" % (b_, a), OPPD[d], [x for x in OPPD if x != OPPD[d]], "%s is %s of %s, so %s is %s of %s." % (a, d, b_, b_, OPPD[d], a))


HERIT = {"a good way to care for a heritage site": ["putting litter in dustbins", "reading the signboards to learn its history", "staying on the marked paths", "taking only photographs",
                                                  "telling others why the site is special", "respecting the rules of the site"],
         "a way that damages a heritage site": ["writing names on the walls", "climbing on old carvings", "sticking chewing gum on pillars", "throwing plastic in the gardens",
                                               "breaking off pieces of stone as souvenirs", "touching old paintings with wet hands"]}
UPQ = [("What is a heritage site?", "a place of great natural or cultural value that should be protected for the future", ["a new shopping mall", "a parking lot", "a playground only"], "UNESCO lists World Heritage Sites."),
       ("Why should we protect heritage sites?", "they tell the story of our past and cannot be replaced", ["they are of no use", "they can be rebuilt easily", "they belong to nobody"], "Treat them with care."),
       ("Which organisation lists World Heritage Sites?", "UNESCO", ["ISRO", "FSSAI", "the Indian Railways"], "India has more than 40 such sites."),
       ("How are the living root bridges of Meghalaya made?", "people guide the roots of rubber fig trees across streams for many years", ["they are made of cement", "they are made of iron", "they grow in one day"], "Some are hundreds of years old."),
       ("What are phumdis on Loktak Lake?", "floating islands made of plants and soil", ["a kind of boat", "a fish", "a dance"], "The Keibul Lamjao park floats on them."),
       ("Which deer lives only on the floating park of Loktak Lake?", "the sangai (dancing deer)", ["the blackbuck", "the barasingha", "the musk deer"], "It is the state animal of Manipur."),
       ("Why is the Rann of Kutch white?", "a layer of salt is left when the sea water dries", ["it is snow", "it is painted", "it is cotton"], "The Rann Utsav is held in winter."),
       ("What are the Lakshadweep islands made of?", "coral", ["ice", "sand dunes only", "volcanic glass"], "Coral is made by tiny sea animals."),
       ("Why do flamingos come to Chilika Lake and the Rann of Kutch?", "they find food and safe places to breed", ["it snows there", "people feed them chips", "they are lost"], "Many come in winter."),
       ("What does a map key tell us?", "what the symbols and colours on the map mean", ["the price of the map", "the time", "the weather tomorrow"], "It is also called a legend."),
       ("What does the scale on a map tell us?", "how the distance on the map compares with real distance", ["the weight of the map", "the height of mountains only", "the colours used"], "1 cm may stand for 100 km."),
       ("What colour usually shows water on a map?", "blue", ["red", "black", "yellow"], "Green often shows forests or low land."),
       ("What colour usually shows high mountains on a physical map?", "brown", ["blue", "white only", "pink"], "Darker shades show higher land."),
       ("Why is Majuli in danger?", "the Brahmaputra erodes its banks and it is shrinking", ["it is growing too fast", "it is in a desert", "it has no water"], "People plant trees to protect it."),
       ("Which famous temple in Odisha was built in the shape of a chariot of the Sun god?", "the Konark Sun Temple", ["the Taj Mahal", "the Golden Temple", "the Qutub Minar"], "Its stone wheels work as sundials."),
       ("Why are the paintings in the Ajanta caves special?", "they are about 2,000 years old and show life and stories of long ago", ["they were painted last year", "they are printed posters", "they are made of plastic"], "They are in Maharashtra."),
       ("Why is Mawsynram so wet?", "moist monsoon winds rise over the Khasi Hills and drop heavy rain", ["it is near a desert", "it has no hills", "it snows all year"], "Cherrapunji is nearby."),
       ("Why do people in Ladakh grow crops only in summer?", "it is too cold for crops in winter", ["it rains all year", "there is no soil", "summer is too hot"], "The growing season is short."),
       ("Why are mangroves important?", "they protect the coast from storms and are homes for many animals", ["they cause floods", "they have no use", "they are deserts"], "The Sundarbans are mangroves."),
       ("Why is Kaziranga famous?", "it protects the greatest number of one-horned rhinos in the world", ["it is a desert", "it has penguins", "it is a city"], "It is in Assam."),
       ("Which of these is a sacred grove?", "a patch of forest protected by a village for religious reasons", ["a shopping centre", "a desert", "a highway"], "Many are found in Meghalaya and the Western Ghats."),
       ("Why should tourists not feed wild animals in parks?", "human food can make them ill and change their behaviour", ["animals need chips", "it helps them", "it is a rule only for children"], "Watch from a distance."),
       ("Why do we use the four directions on a map?", "to tell where places are compared with each other", ["to colour the map", "to measure weight", "for decoration only"], "North is usually at the top."),
       ("Which direction is usually at the top of a map?", "north", ["south", "east", "west"], "An arrow with N shows it."),
       ("What is ecotourism?", "visiting natural places in a way that protects them and helps local people", ["building hotels in forests", "hunting animals", "leaving litter"], "Take nothing but photos."),
       ("Why is the Valley of Flowers protected as a national park?", "it has rare Himalayan flowers and animals", ["it is a farm", "it is a desert", "it has a factory"], "It is in Uttarakhand."),
       ("What is a UNESCO World Heritage Site in Assam famous for rhinos?", "Kaziranga National Park", ["Hampi", "the Sundarbans", "the Valley of Flowers"], "Manas National Park is another."),
       ("Why are old forts and temples made of stone still standing?", "stone is strong and lasts a very long time", ["they are rebuilt every year", "they are made of paper", "nobody uses them"], "Weather slowly wears them.")]

# =================================================================== Chapter 7: energy — how things work
REN = {"a renewable source of energy": ["sunlight", "wind", "flowing water", "biogas from cow dung", "ocean tides", "heat from inside the Earth"],
       "a non-renewable source of energy": ["coal", "petrol", "diesel", "natural gas", "kerosene", "LPG in a gas cylinder"]}
CONV = [("an electric bulb", "electrical energy into light energy"), ("a ceiling fan", "electrical energy into motion"), ("a solar panel", "light energy into electrical energy"),
        ("a radio", "electrical energy into sound energy"), ("a torch cell", "stored chemical energy into electrical energy"), ("a wind turbine", "the motion of the wind into electrical energy"),
        ("a gas stove", "the chemical energy of fuel into heat"), ("an electric iron", "electrical energy into heat"), ("our muscles", "the chemical energy of food into motion")]
SAVE = {"a way to save energy": ["switching off lights when leaving a room", "using LED bulbs", "cycling or walking for short trips", "drying clothes in the sun",
                                 "taking a bus instead of a car", "using a pressure cooker", "keeping the fridge door closed", "using solar water heaters"],
        "a way to waste energy": ["leaving the TV on in an empty room", "keeping the fridge door open", "driving a car for very short trips", "using old filament bulbs",
                                  "leaving a charger switched on after use", "heating more water than needed", "running a fan when no one is in the room", "keeping the engine on at a red light"]}
FORM = [("the light from the Sun", "light energy"), ("a ringing bell", "sound energy"), ("a running child", "energy of motion"), ("a hot cup of tea", "heat energy"),
        ("the food we eat", "chemical energy stored in food"), ("a stretched rubber band", "stored energy that can make things move")]
ENQ = [("What is energy?", "the ability to do work or make things change or move", ["a kind of food only", "a type of machine", "a colour"], "We need energy to run, think and grow."),
       ("Where does almost all energy on Earth come from?", "the Sun", ["the Moon", "the wind only", "the sea only"], "Plants use sunlight to make food."),
       ("Why are coal and petrol called non-renewable?", "they took millions of years to form and will run out", ["they never run out", "they come from sunlight every day", "they grow back each year"], "Use them carefully."),
       ("Why are sunlight and wind called renewable?", "nature keeps supplying them and they do not run out", ["they run out quickly", "they are made in factories", "they are costly to make"], "They are cleaner too."),
       ("Why is burning coal and petrol harmful?", "it produces smoke and gases that pollute the air and warm the Earth", ["it cleans the air", "it cools the Earth", "it makes oxygen"], "Cleaner energy helps."),
       ("How does a solar cooker cook food?", "it traps the heat of sunlight", ["it uses electricity", "it burns coal", "it uses wind"], "It works best on sunny days."),
       ("How is electricity made from flowing water?", "falling water turns turbines at a dam", ["water is burnt", "water is frozen", "water is mixed with oil"], "This is hydroelectricity."),
       ("What is biogas made from?", "cow dung and plant waste rotting in a closed tank", ["petrol", "sea water", "sand"], "It is used for cooking in villages."),
       ("Which energy do we get from food?", "chemical energy", ["electrical energy", "sound energy", "magnetic energy"], "Our body changes it into motion and heat."),
       ("What does 'BEE 5 star' on an electrical appliance mean?", "it uses less electricity", ["it is very old", "it costs nothing", "it is noisy"], "More stars mean more saving."),
       ("Why are LED bulbs better than old filament bulbs?", "they give the same light using much less electricity", ["they use more electricity", "they give no light", "they get very hot"], "They also last longer."),
       ("Why does a filament bulb get hot?", "much of the electricity is changed into heat instead of light", ["it is cold inside", "the glass is hot", "it has a fire"], "This is wasted energy."),
       ("Why do we rub our hands on a cold day?", "rubbing changes motion into heat", ["it makes our hands colder", "it makes electricity", "it makes light"], "Friction produces heat."),
       ("Which form of energy makes a kite fly?", "the moving wind", ["sound", "electricity", "light"], "Wind energy is energy of moving air."),
       ("Which state has many wind turbines along its coast and hills?", "Tamil Nadu", ["Ladakh", "Delhi", "Goa"], "Gujarat also has many."),
       ("Why should we not waste electricity?", "making electricity uses fuel and causes pollution", ["electricity is free", "it grows on trees", "wasting saves money"], "Save energy, save money."),
       ("Why is cycling good for the environment?", "it uses our own energy and causes no smoke", ["it burns petrol", "it pollutes the air", "it needs electricity"], "It keeps us fit too."),
       ("What is CNG used for in many Indian cities?", "as a cleaner fuel for buses and autos", ["as a food", "as a medicine", "to make ice"], "CNG makes less smoke than diesel."),
       ("What is the energy stored in a stretched catapult called?", "stored (potential) energy", ["sound energy", "light energy", "heat energy"], "It becomes motion when released."),
       ("What happens to the energy of a rolling ball when it stops on rough ground?", "it changes into heat due to friction", ["it disappears completely", "it turns into light", "it goes into the sky"], "Energy changes form."),
       ("Why do people in villages use smokeless chulhas?", "they burn fuel better and give less smoke", ["they make more smoke", "they use petrol", "they need no fuel"], "Smoke harms the lungs."),
       ("Why is a pressure cooker an energy saver?", "it cooks food faster, using less fuel", ["it uses more fuel", "it cooks slowly", "it needs no heat"], "Keep the lid on while cooking."),
       ("Which device changes sound into electrical signals?", "a microphone", ["a bulb", "a fan", "an iron"], "A loudspeaker does the opposite."),
       ("What is an electric circuit?", "a closed path through which electricity flows", ["a broken wire", "a type of battery only", "a light bulb only"], "A switch opens or closes it."),
       ("Why does a torch not glow when the cells are put in the wrong way?", "the circuit does not work properly", ["cells only work upside down", "the bulb is too new", "torches need water"], "Match the + and − signs."),
       ("Why do solar panels on rooftops help a home?", "they make electricity from sunlight without pollution", ["they cool the roof only", "they need petrol", "they make smoke"], "Many homes now use them.")]


def c_bill(k=None):
    R = _R[0]
    u, d, r = R.choice([3, 4, 5, 6, 8]), R.choice([10, 30]), R.choice([5, 6, 7, 8])
    n = kid()
    if R.random() < 0.5:
        return tq("%s's family uses %d units of electricity each day. How many units do they use in %d days?" % (n, u, d), "%d units" % (u * d),
                  ["%d units" % x for x in (u + d, u * d + d, u * (d - 1))], "%d × %d = %d units." % (u, d, u * d))
    return tq("%s's family uses %d units of electricity in %d days. Each unit costs ₹%d. What is the bill?" % (n, u * d, d, r), "₹%d" % (u * d * r),
              ["₹%d" % x for x in (u * d + r, u * r, u * d * (r + 1))], "%d units × ₹%d = ₹%d." % (u * d, r, u * d * r))


# =================================================================== Chapter 8: clothes — how things are made
FIB = {"a natural fibre": ["cotton", "jute", "silk", "wool", "coir", "linen from flax", "pashmina (wool of Changthangi goats)", "hemp"],
       "a synthetic (human-made) fibre": ["nylon", "polyester", "acrylic", "spandex (elastic fibre)"]}
FSRC = [("cotton", "the fluffy bolls around the seeds of the cotton plant"), ("jute", "the stem of the jute plant"), ("silk", "the cocoons of silkworms"),
        ("wool", "the fleece of sheep, goats, yaks and camels"), ("coir", "the husk of coconuts"), ("linen", "the stems of the flax plant"), ("polyester", "chemicals made from petroleum"), ("hemp", "the stems of the hemp plant")]
SAREE = [("Banarasi silk", "Uttar Pradesh"), ("Kanjeevaram silk", "Tamil Nadu"), ("Pochampally ikat", "Telangana"), ("Chanderi", "Madhya Pradesh"), ("Muga silk", "Assam"),
         ("Pashmina shawls", "Jammu and Kashmir"), ("Patola", "Gujarat"), ("Sambalpuri", "Odisha"), ("Paithani", "Maharashtra"), ("Kota doria", "Rajasthan"), ("Baluchari", "West Bengal"), ("Maheshwari", "Madhya Pradesh")]
CSTEP = ["picking cotton from the fields", "ginning (removing the seeds)", "spinning the fibres into yarn", "weaving the yarn into cloth", "dyeing or printing the cloth", "stitching it into clothes"]


def c_cloth(k=None):
    R = _R[0]
    st = CSTEP
    i = R.randrange(len(st) - 1)
    others = [x for x in st if x not in (st[i], st[i + 1])]
    if R.random() < 0.5:
        return tq("In making a cotton shirt, which step comes just after “%s”?" % st[i], st[i + 1], R.sample(others, 3), "The steps: " + " → ".join(st) + ".")
    if R.random() < 0.7:
        return tq("In making a cotton shirt, which step comes just before “%s”?" % st[i + 1], st[i], R.sample(others, 3), "The steps: " + " → ".join(st) + ".")
    if R.random() < 0.5:
        return tq("Which is the first step in making a cotton shirt?", st[0], R.sample(st[1:], 3), "The steps: " + " → ".join(st) + ".")
    return tq("Which is the last step in making a cotton shirt?", st[-1], R.sample(st[:-1], 3), "The steps: " + " → ".join(st) + ".")


WEAR = [("a hot summer day", "loose, light-coloured cotton clothes"), ("a cold winter morning", "woollen sweaters and caps"), ("a rainy day", "a raincoat and a waterproof umbrella"),
        ("fighting a fire", "a fire-resistant suit"), ("working on a construction site", "a hard helmet and a bright safety jacket"), ("playing cricket", "pads, gloves and a helmet"), ("a snowy mountain trek", "thick jackets, gloves and snow boots"),
        ("an operation in a hospital", "a clean gown, a mask and gloves"), ("swimming in a pool", "a swimsuit made of stretchy synthetic fibre")]
CLQ = [("What is a fibre?", "a thin, thread-like strand from which yarn and cloth are made", ["a type of button", "a kind of dye", "a sewing machine"], "Cotton and wool are fibres."),
       ("What is the difference between natural and synthetic fibres?", "natural fibres come from plants or animals; synthetic fibres are made from chemicals", ["there is no difference", "natural fibres come from factories only", "synthetic fibres grow on trees"], "Nylon is synthetic."),
       ("What is ginning?", "separating cotton fibres from the seeds", ["weaving cloth", "dyeing cloth", "cutting cloth"], "It was once done by hand."),
       ("What is spinning?", "twisting fibres together to make yarn", ["weaving yarn into cloth", "stitching clothes", "removing seeds"], "The charkha is a spinning wheel."),
       ("What is weaving?", "crossing two sets of yarn over and under each other to make cloth", ["twisting fibres", "removing seeds", "colouring cloth"], "It is done on a loom."),
       ("What is knitting?", "making cloth from a single yarn using needles or machines", ["crossing two sets of yarn on a loom", "removing seeds", "dyeing cloth"], "Sweaters are often knitted."),
       ("Why is cotton good to wear in summer?", "it absorbs sweat and lets air pass through", ["it keeps us very warm", "it does not absorb sweat", "it is waterproof"], "Light colours also help."),
       ("Why do woollen clothes keep us warm?", "wool traps air, which does not let body heat escape", ["wool makes heat", "wool is cold", "wool is waterproof"], "Layers trap more air."),
       ("Why are raincoats made of plastic or nylon?", "these materials do not let water pass through", ["they absorb water", "they are warm", "they are heavy"], "They are waterproof."),
       ("Why should synthetic clothes not be worn near a fire or a stove?", "they catch fire and melt, sticking to the skin", ["they are fire-proof", "they keep heat away", "they are made of iron"], "Wear cotton in the kitchen."),
       ("What does 'handloom' mean?", "cloth woven by hand on a loom", ["cloth made in a big factory", "cloth bought online", "cloth made of plastic"], "7 August is National Handloom Day."),
       ("On which date is National Handloom Day celebrated in India?", "7 August", ["15 August", "26 January", "2 October"], "It honours weavers."),
       ("What is khadi?", "cloth hand-spun and hand-woven, made popular by Mahatma Gandhi", ["a synthetic fibre", "a kind of dye", "a factory machine"], "It is a symbol of self-reliance."),
       ("What is tie-and-dye cloth from Gujarat and Rajasthan called?", "bandhani", ["kantha", "phulkari", "ikat"], "Small parts are tied before dyeing."),
       ("Which plant gives a natural blue dye?", "indigo", ["turmeric", "mango", "neem"], "Turmeric gives yellow and madder gives red."),
       ("Which part of the silkworm's life is used to make silk?", "the cocoon", ["the egg", "the moth's wings", "the leaves it eats"], "Silkworms eat mulberry leaves."),
       ("What does a weaver use to weave cloth?", "a loom", ["a charkha", "a potter's wheel", "a pulley"], "A charkha is used for spinning."),
       ("Why should we reuse and recycle old clothes?", "it saves water, energy and raw materials and reduces waste", ["it wastes resources", "old clothes are poisonous", "it makes new clothes costly"], "Make bags or dusters from them."),
       ("How can an old cotton sari be reused?", "as a quilt, a bag or a duster", ["only burnt", "thrown in a river", "buried in plastic"], "Kantha quilts reuse old saris."),
       ("Why does it take a lot of water to grow cotton?", "cotton plants need plenty of water to grow", ["cotton grows in the sea", "cotton needs no water", "cotton grows in snow"], "So we should not waste clothes."),
       ("Which fibre is called the 'golden fibre' and is grown in West Bengal?", "jute", ["nylon", "wool", "polyester"], "It is used for sacks and bags."),
       ("What are sacks for grain often made of?", "jute", ["silk", "wool", "linen"], "Jute is strong and rough."),
       ("Which fibre comes from coconut husk?", "coir", ["jute", "silk", "wool"], "Kerala makes coir mats and ropes."),
       ("Why do doctors wear clean cotton gowns in hospitals?", "they are easy to wash and keep germs away", ["they look fashionable only", "they are fireproof", "they are waterproof"], "Hygiene is important."),
       ("Why do people in deserts wear loose white clothes?", "white reflects sunlight and loose clothes let air move", ["white absorbs heat", "tight clothes are cooler", "they are warmer"], "Dark colours absorb more heat."),
       ("Which fibre is made from petroleum?", "polyester", ["cotton", "silk", "wool"], "Nylon and acrylic are also made from it."),
       ("Why should we not throw away clothes after wearing them only a few times?", "making clothes uses a lot of water, energy and work", ["clothes are made without water", "it helps the environment", "clothes are free"], "Buy only what you need."),
       ("Why are woollen clothes washed gently in cool water?", "hot water and rubbing make wool shrink", ["wool grows in hot water", "wool melts", "it changes colour to white"], "Dry them flat."),
       ("What is a charkha used for?", "spinning yarn", ["weaving cloth", "stitching clothes", "dyeing cloth"], "Gandhiji spun khadi on a charkha."),
       ("What is block printing?", "printing designs on cloth with carved wooden blocks dipped in colour", ["weaving with gold thread", "knitting with needles", "removing seeds"], "Sanganer and Bagru in Rajasthan are famous for it."),
       ("Why are synthetic fibres used for ropes, nets and tents?", "they are strong, light and do not rot easily in water", ["they rot quickly", "they are weak", "they absorb water"], "Fishing nets are often nylon."),
       ("Why is it good to buy handloom products?", "it supports weavers and keeps traditional skills alive", ["handloom is always bad quality", "it harms weavers", "it wastes cloth"], "Look for the Handloom Mark.")]

# =================================================================== Chapter 9: rhythms of nature
WCYC = [("evaporation", "water changing into water vapour because of the Sun's heat"), ("condensation", "water vapour cooling into tiny drops that form clouds"),
        ("precipitation", "water falling from clouds as rain, snow or hail"), ("collection", "water gathering in rivers, lakes and seas"),
        ("transpiration", "plants giving out water vapour through their leaves"), ("seepage", "water soaking down into the soil")]
RHY = [("day and night", "every 24 hours"), ("the full Moon", "about once every 29 to 30 days"), ("the seasons", "once every year"),
       ("high tide at the seaside", "about twice a day"), ("the monsoon rains in India", "once a year, mostly from June to September"), ("the new Moon (Amavasya)", "about once a month"),
       ("the arrival of migratory birds in India", "every winter"), ("mango trees flowering", "every spring")]
CROP = {"a kharif crop (sown with the monsoon rains)": ["rice", "maize", "cotton", "soybean", "groundnut", "bajra", "jute", "arhar (tur dal)"],
        "a rabi crop (sown in winter)": ["wheat", "mustard", "gram (chana)", "barley", "peas", "linseed", "masoor (lentil)", "potato in the northern plains"]}
SEAS = [("summer", "April to June, when it is hottest in most of India"), ("the monsoon", "June to September, when most rain falls"),
        ("winter", "December to February, when it is coldest"), ("spring", "February to March, when many trees flower and new leaves grow"), ("autumn (post-monsoon)", "October to November, after the monsoon rains end")]
WSEQ = ["evaporation", "condensation", "precipitation", "collection"]


def c_wcyc(k=None):
    R = _R[0]
    i = R.randrange(4)
    a = WSEQ[(i + 1) % 4]
    others = [x for x in WSEQ + ["transpiration"] if x not in (WSEQ[i], a)]
    if R.random() < 0.5:
        return tq("In the water cycle, which step comes just after %s?" % WSEQ[i], a, R.sample(others, 3), "Evaporation → condensation → precipitation → collection, and again evaporation.")
    return tq("In the water cycle, which step comes just before %s?" % a, WSEQ[i], R.sample(others, 3), "Evaporation → condensation → precipitation → collection, and again evaporation.")


RNQ = [("Why do we have day and night?", "Earth spins on its axis once in about 24 hours", ["the Sun goes around Earth every day", "the Moon hides the Sun", "clouds cover the Sun"], "The side facing the Sun has day."),
       ("Why do we have seasons?", "Earth's axis is tilted as it goes around the Sun in a year", ["the Sun turns on and off", "Earth spins faster in summer", "the Moon gets hot"], "Days are longer in summer."),
       ("Why are days longer in summer than in winter in India?", "the Sun rises earlier and sets later in summer", ["the Sun moves faster in winter", "clocks change", "the Moon is brighter"], "The Sun is higher in the sky."),
       ("Why do clouds form?", "water vapour rises, cools and condenses into tiny drops", ["smoke rises from fires", "the wind makes cotton", "the Sun throws water"], "Clouds float in the sky."),
       ("Why is the water cycle important?", "it brings fresh water again and again to land", ["it makes the sea salty only", "it stops rain", "it dries rivers"], "Water is used again and again."),
       ("Why do some trees shed their leaves in autumn or before summer?", "to save water in the dry season", ["they are dying", "birds eat the leaves", "the leaves are too heavy"], "New leaves come in spring."),
       ("Why do birds such as Siberian cranes and bar-headed geese come to India in winter?", "their homes in the north become very cold and food is hard to find", ["they like Indian food only", "they are lost", "Indian winters are colder"], "They are migratory birds."),
       ("Which bird sanctuary in Rajasthan is famous for winter migratory birds?", "Keoladeo (Bharatpur)", ["Kaziranga", "Gir", "Jim Corbett"], "It is a World Heritage Site."),
       ("Why do frogs croak a lot in the monsoon?", "they call to find mates and lay eggs in the rainwater pools", ["they are hungry", "they are cold", "they are lost"], "Tadpoles grow in the pools."),
       ("Why do some snakes and frogs hide underground in winter?", "it is too cold, so they rest until warm weather", ["they are scared of birds", "they hunt underground", "they dislike light"], "This long rest is called hibernation."),
       ("Why do farmers wait for the monsoon to sow rice?", "rice needs a lot of water", ["rice needs snow", "rice grows in dry sand", "the monsoon is cold"], "Rice is a kharif crop."),
       ("When is wheat usually harvested in north India?", "in spring (March–April)", ["in the monsoon", "in December", "in June only"], "Baisakhi celebrates the wheat harvest."),
       ("Why do people wear woollens in winter and cotton in summer?", "clothes change with the season's weather", ["it is a rule", "wool is cheaper in summer", "for no reason"], "Our habits follow nature's rhythms."),
       ("Why do the Moon's shapes repeat every month?", "the Moon goes around Earth about once a month", ["the Moon breaks and grows back", "clouds cover it", "the Sun eats it"], "From new Moon to full Moon is about 15 days."),
       ("Why does a puddle disappear on a sunny day?", "the water evaporates", ["the puddle sinks into the sky", "animals drink it all", "it freezes"], "Heat speeds up evaporation."),
       ("Why do we see dew on grass in the early morning?", "water vapour condenses on cool grass at night", ["it rained at night", "grass sweats", "insects spray water"], "Dew dries as the Sun rises."),
       ("Why does it rain more on the windward side of hills?", "moist winds rise, cool and drop their rain there", ["hills make water", "the other side is closer to the Sun", "trees cause rain"], "The other side is a rain-shadow area."),
       ("What is a festival linked to the start of a new season?", "Basant Panchami, welcoming spring", ["Republic Day", "Children's Day", "Independence Day"], "Many festivals follow nature's calendar."),
       ("Why do mango trees flower in spring?", "the warm weather after winter is right for flowering", ["they flower in snow", "birds plant the flowers", "they flower every day"], "Mangoes ripen in summer."),
       ("What is a tide?", "the regular rise and fall of the sea level", ["a big wind", "a river flood", "a mountain"], "The Moon's pull causes tides."),
       ("What mainly causes ocean tides?", "the pull of the Moon", ["the wind only", "ships", "fish"], "The Sun's pull also helps."),
       ("Why do some animals grow thicker fur in winter?", "thick fur keeps them warm", ["it keeps them cool", "it is fashionable", "fur grows only in summer"], "They shed it in summer."),
       ("Why do bees and butterflies appear in large numbers in spring?", "many flowers bloom and give nectar", ["it snows", "they hide from flowers", "there are no flowers"], "They help pollinate the flowers."),
       ("Why is the monsoon called the lifeline of Indian farming?", "most crops depend on its rain", ["it stops all farming", "it brings snow", "it dries the land"], "A weak monsoon can mean drought."),
       ("What happens to the length of your shadow from morning to noon?", "it becomes shorter", ["it becomes longer", "it stays the same", "it disappears forever"], "It is shortest at noon."),
       ("How long does Earth take to go once around the Sun?", "about 365 days", ["about 24 hours", "about 30 days", "about 7 days"], "This is one year."),
       ("What is a migratory bird?", "a bird that travels to another place at a certain time each year", ["a bird that never moves", "a bird kept at home", "a bird that cannot fly"], "Many arrive in India in winter."),
       ("What is hibernation?", "a long, deep rest some animals take in the cold season", ["flying south", "building a nest", "laying eggs in water"], "The body slows down to save energy."),
       ("Why are many crops harvested just before big festivals?", "people celebrate the harvest together", ["festivals cause harvests", "crops fear festivals", "there is no link"], "Pongal and Baisakhi are harvest festivals."),
       ("Which season brings most of India's rain?", "the monsoon", ["winter", "spring", "summer"], "It lasts from June to September."),
       ("Why does sea water not run out even though the Sun evaporates so much of it?", "rivers and rain return the water to the sea", ["the sea makes new water", "the Moon pours water", "fish make water"], "This is the water cycle."),
       ("What is the name of the long, deep sleep of bears in very cold places?", "hibernation", ["migration", "germination", "evaporation"], "Himalayan black bears may hibernate."),
       ("Why do leaves of many trees turn yellow and fall in the dry season?", "the tree saves water by shedding them", ["the leaves are painted", "insects take them", "they become flowers"], "New leaves come in spring."),
       ("Why do the shapes of the Moon follow a rhythm?", "the Moon goes around Earth once in about a month", ["the Moon changes size", "clouds cover it in a pattern", "the Sun moves around the Moon"], "It repeats every 29 to 30 days."),
       ("What happens to the length of day and night in winter in India?", "days are shorter and nights are longer", ["days are longer", "they are always equal", "there is no night"], "It is the opposite in summer."),
       ("Why do farmers in Punjab harvest wheat in April?", "wheat sown in winter ripens by spring", ["wheat grows in the monsoon", "wheat ripens in a week", "April has snow"], "Baisakhi marks this harvest."),
       ("Which festival is celebrated when the Sun begins its journey northwards in January?", "Makar Sankranti", ["Diwali", "Onam", "Christmas"], "Kites are flown in Gujarat."),
       ("Why do koels sing loudly in summer?", "it is their breeding season", ["they are cold", "they are lost", "they are hungry for snow"], "Their call is heard in mango groves.")]

def c_day(k=None):
    R = _R[0]
    city = R.choice(["Delhi", "Lucknow", "Jaipur", "Patna", "Bhopal", "Chandigarh", "Amritsar"])
    if R.random() < 0.5:
        rh, sh = 5, 7
        sm = R.choice([0, 15, 30])
        h = 12 - rh + sh
        return tq("In June the Sun rises in %s at about %d:%02d a.m. and sets at about %d:%02d p.m. About how long is the daytime?" % (city, rh, sm, sh, sm), "%d hours" % h,
                  ["%d hours" % x for x in (h - 1, h + 1, 24 - h)], "From %d:%02d a.m. to %d:%02d p.m. is %d hours. Summer days are long." % (rh, sm, sh, sm, h))
    rh, sh = 7, 5
    sm = R.choice([0, 15, 30])
    h = 12 - rh + sh
    return tq("In December the Sun rises in %s at about %d:%02d a.m. and sets at about %d:%02d p.m. About how long is the daytime?" % (city, rh, sm, sh, sm), "%d hours" % h,
              ["%d hours" % x for x in (h - 1, h + 1, 24 - h)], "From %d:%02d a.m. to %d:%02d p.m. is %d hours. Winter days are short." % (rh, sm, sh, sm, h))


# =================================================================== Chapter 10: earth — our shared home
ROLE = {"a producer (makes its own food)": ["grass", "a mango tree", "algae in a pond", "a wheat plant", "a cactus", "a lotus plant"],
        "a consumer (eats plants or animals)": ["a deer", "a tiger", "a frog", "a cow", "an eagle", "a human", "a grasshopper"],
        "a decomposer (breaks down dead things)": ["a mushroom", "bacteria in the soil", "mould on old bread"]}
CHAINS = [["grass", "grasshopper", "frog", "snake", "eagle"], ["leaves", "caterpillar", "sparrow", "hawk"], ["algae", "small fish", "big fish", "kingfisher"],
          ["grass", "deer", "tiger"], ["grain", "rat", "snake", "peacock"], ["flower nectar", "butterfly", "lizard", "crow"]]


def c_chain(k=None):
    R = _R[0]
    ch = R.choice(CHAINS)
    i = R.randrange(len(ch) - 1)
    allx = sorted({x for c in CHAINS for x in c} - set(ch))
    w = [x for x in ch if x not in (ch[i], ch[i + 1])][:2]
    w += R.sample(allx, 3 - len(w))
    if R.random() < 0.5:
        return tq("In the food chain %s, what does the %s eat?" % (" → ".join(ch), ch[i + 1]), ch[i], w,
                  "The arrow points from the food to the eater: %s → %s." % (ch[i], ch[i + 1]))
    return tq("In the food chain %s, which living thing eats the %s?" % (" → ".join(ch), ch[i]), ch[i + 1], w,
              "The arrow points from the food to the eater: %s → %s." % (ch[i], ch[i + 1]))


ECO = {"an eco-friendly habit": ["carrying a cloth bag for shopping", "composting kitchen waste", "planting trees", "using both sides of paper", "repairing old things instead of throwing them",
                                 "turning off taps and lights", "using a refillable water bottle", "walking or cycling short distances"],
       "a habit that harms the environment": ["burning plastic", "throwing waste into rivers", "cutting trees without planting new ones", "using plastic straws and plates",
                                              "bursting a lot of firecrackers", "leaving the car engine running", "wasting food", "hunting wild animals"]}
HERO = [("the Chipko movement", "villagers hugging trees to stop them being cut"), ("the Bishnoi community", "protecting blackbuck and khejri trees in Rajasthan"),
        ("Project Tiger", "protecting tigers in reserves since 1973"), ("Jadav Payeng", "planting a whole forest on a sandbar of the Brahmaputra"),
        ("Saalumarada Thimmakka", "planting hundreds of banyan trees along a road in Karnataka"), ("the Swachh Bharat Mission", "keeping India clean and building toilets")]
DEP = [("bees", "flowers for nectar"), ("flowers", "bees and butterflies to carry pollen"), ("plants", "the soil, water and sunlight to make food"),
       ("tigers", "deer and other animals for food"), ("people", "plants and animals for food, clothes and medicines"), ("earthworms", "dead leaves for food"), ("birds", "trees for nests and fruits")]
EAQ = [("Why is Earth called our shared home?", "all plants, animals and people live on it and depend on each other", ["only people live on it", "it belongs to one country", "nothing lives on it"], "We must care for it together."),
       ("What does 'interdependence' mean?", "living things depend on each other to survive", ["living things never need each other", "only animals need plants", "only people matter"], "Bees need flowers and flowers need bees."),
       ("What is a food chain?", "a series showing who eats whom", ["a chain made of food", "a shop", "a kind of necklace"], "Every chain begins with a plant."),
       ("Why do all food chains begin with green plants?", "plants make their own food using sunlight", ["plants eat animals", "plants are the biggest", "animals cannot eat"], "Plants are producers."),
       ("What would happen if all the bees disappeared?", "many plants would not be pollinated and we would get less fruit", ["nothing at all", "more honey would be made", "plants would grow faster"], "Bees are pollinators."),
       ("Why are decomposers important?", "they break down dead plants and animals and return nutrients to the soil", ["they make the soil poor", "they eat living animals", "they have no use"], "Mushrooms and bacteria are decomposers."),
       ("What happens when forests are cut down?", "animals lose their homes and the soil is washed away", ["animals get more homes", "there is more rain at once", "the soil becomes richer"], "Plant more trees."),
       ("Why are some animals in danger of dying out?", "hunting, pollution and loss of their homes", ["they eat too much", "they are too happy", "there are too many of them"], "These are endangered animals."),
       ("Which animal is India's national animal and is protected by Project Tiger?", "the tiger", ["the lion", "the elephant", "the peacock"], "Tiger numbers have grown again."),
       ("What does 'reduce, reuse, recycle' mean?", "use less, use things again and make new things from old ones", ["throw everything away", "buy more and more", "burn waste"], "The 3 Rs save resources."),
       ("Why is composting good?", "it turns kitchen and garden waste into manure for plants", ["it makes plastic", "it pollutes rivers", "it wastes food"], "Separate wet and dry waste."),
       ("Why should we separate wet and dry waste?", "wet waste can be composted and dry waste can be recycled", ["it makes more waste", "it is not useful", "all waste is the same"], "Use green and blue bins."),
       ("Why is plastic harmful to animals?", "animals may eat it or get trapped in it", ["plastic is food for them", "it keeps them warm", "it helps them fly"], "Cows and turtles are often harmed."),
       ("What is World Environment Day?", "a day on 5 June to spread awareness about protecting the environment", ["a sports day", "a festival of lights", "a harvest festival"], "Plant a tree that day."),
       ("Which date is Earth Day?", "22 April", ["5 June", "15 August", "14 November"], "People take part in clean-ups."),
       ("What is a national park?", "a protected area where wild animals and plants live safely", ["a city garden", "a zoo with cages", "a cricket ground"], "Jim Corbett was India's first national park."),
       ("Which was India's first national park?", "Jim Corbett National Park", ["Kaziranga", "Gir", "Sundarbans"], "It is in Uttarakhand."),
       ("Why do we need clean air?", "all living things need clean air to breathe and stay healthy", ["dirty air is healthier", "only plants need air", "air is not needed"], "Trees help clean the air."),
       ("How do trees help keep the air clean?", "they take in carbon dioxide and give out oxygen", ["they give out smoke", "they take in oxygen only", "they do not change air"], "Forests are the lungs of the Earth."),
       ("What is global warming?", "the slow rise in Earth's temperature caused by too many greenhouse gases", ["the cooling of Earth", "warm clothes in winter", "a summer holiday"], "Burning fuels adds these gases."),
       ("Why should we not waste food?", "growing food uses land, water and energy, and many people go hungry", ["food grows by itself", "wasting food helps soil", "there is plenty for all forever"], "Take small helpings."),
       ("How can schools help protect the Earth?", "by planting trees, saving water and energy and reducing waste", ["by cutting trees", "by wasting paper", "by burning waste"], "Start an eco club."),
       ("What is a sacred grove?", "a forest patch protected by a community for religious reasons", ["a shopping area", "a dry desert", "a factory yard"], "They protect rare plants."),
       ("Why do the Bishnoi people protect the khejri tree?", "their faith teaches them to protect trees and animals", ["they want to sell it", "it is poisonous", "it is a crop"], "Amrita Devi gave her life to save trees in 1730."),
       ("Why should we not buy products made from wild animals?", "it encourages hunting and harms animals", ["it saves animals", "it is good for forests", "animals do not mind"], "Ivory and tiger skins are banned.")]


def UNITS5b():
    b = {k: once_maker(v) for k, v in [("up", UPQ), ("en", ENQ), ("cl", CLQ), ("rn", RNQ), ("ea", EAQ)]}
    uniq = pairs(UNIQ, "What is special about %s?", "Which place is %s?")
    st6 = pairs(STATE6, "In which state or union territory is %s?", "Which famous place is in %s?")
    herit = odd_one(HERIT, "Which of these is %s?", "Which of these is not %s?")
    ren = odd_one(REN, "Which of these is %s?", "Which of these is not %s?")
    conv = pairs(CONV, "What energy change happens in %s?", "Which of these changes %s?")
    save = odd_one(SAVE, "Which of these is %s?", "Which of these is not %s?")
    form = pairs(FORM, "What kind of energy does %s have or give?", "Which of these has %s?")
    fib = odd_one(FIB, "Which of these is %s?", "Which of these is not %s?")
    fsrc = pairs(FSRC, "Where does %s come from?", "Which fibre comes from %s?")
    saree = pairs(SAREE, "Which state or union territory is famous for %s?", "Which handloom cloth is famous in %s?")
    wear = pairs(WEAR, "What is best to wear for %s?", "When is it best to wear %s?")
    wcyc = pairs(WCYC, "What is %s in the water cycle?", "What do we call %s?")
    rhy = pairs(RHY, "How often does %s happen?")
    crop = odd_one(CROP, "Which of these is %s?", "Which of these is not %s?")
    seas = pairs(SEAS, "When is %s in most of India?", "Which season is from %s?")
    role = odd_one(ROLE, "Which of these is %s?", "Which of these is not %s?")
    eco = odd_one(ECO, "Which of these is %s?", "Which of these is not %s?")
    hero = pairs(HERO, "What is %s known for?", "Who or what is known for %s?")
    dep = pairs(DEP, "What do %s depend on?")
    return [
        U(6, "some-unique-places", 6, II,
          "Unique natural and cultural places of India and what makes them special; heritage sites and how to protect them; reading a map using directions, the key and the scale; responsible tourism (summary of NCERT Our Wondrous World Chapter 6).",
          "Some Unique Places", "some unique places",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 6: unique places of India, heritage sites, states, map directions, keys and scales, and caring for heritage. 100 questions with answers.",
          "Every unique place tells a story.", "Protect heritage sites for the future.",
          "<p>India has many unique places: the living root bridges of Meghalaya, the floating phumdis of Loktak Lake, the white salt Rann of Kutch, the coral islands of Lakshadweep and the river island Majuli. Heritage sites such as the Taj Mahal, Hampi, the Konark Sun Temple and the Ajanta caves tell us about the past.</p>"
          "<p>Maps help us find these places: north is usually at the top, the key explains the symbols and the scale compares map distance with real distance. We protect heritage sites by not writing on walls, using dustbins and following the rules.</p>",
          [("Floating islands called phumdis are in…", ["Manipur"], "Loktak Lake"), ("Kolkata is ___ of Mumbai.", ["look at the map"], "east")],
          ["Writing names on monuments.", "Thinking north is wherever you face.", "Mixing up natural and cultural heritage."],
          [("What is a heritage site?", "A place of great natural or cultural value that is protected so that future generations can enjoy it."),
           ("What does the scale of a map tell us?", "How a distance on the map compares with the real distance on the ground.")],
          lambda: [("Unique places", [(uniq, 14), (b["up"], 6)]), ("Places and states", [(st6, 16), (b["up"], 4)]), ("Reading maps", [(c_city, 12), (b["up"], 8)]),
                   ("Caring for heritage", [(herit, 14), (b["up"], 4), (c_city, 2)]), ("Mixed problems", [(uniq, 8), (st6, 6), (herit, 6)])]),
        U(7, "energy-how-things-work", 7, TA,
          "What energy is; forms of energy (light, heat, sound, motion, electrical and chemical); renewable and non-renewable sources; how appliances change energy from one form to another; using energy in daily life and saving it (summary of NCERT Our Wondrous World Chapter 7).",
          "Energy: How Things Work", "energy: how things work",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 7: forms and sources of energy, renewable and non-renewable energy, energy changes in appliances and saving electricity. 100 questions with answers.",
          "Energy makes things move, change and work.", "Use renewable energy and save electricity.",
          "<p>Energy is the ability to make things move or change. It comes in many forms: light, heat, sound, motion, electrical energy and chemical energy stored in food and fuel. Almost all energy on Earth comes from the Sun. Machines change energy from one form to another: a bulb changes electricity into light, a fan into motion and a solar panel changes light into electricity.</p>"
          "<p>Sunlight, wind and flowing water are renewable; coal, petrol and gas are non-renewable and cause pollution. We save energy by switching off lights, using LED bulbs and walking or cycling for short trips.</p>",
          [("A solar panel changes…", ["sunlight → electricity"], "light energy into electrical energy"), ("Is coal renewable?", ["formed over millions of years"], "no, it is non-renewable")],
          ["Thinking electricity is a source rather than a form of energy.", "Calling wood from forests endless.", "Leaving chargers and TVs on."],
          [("What is the difference between renewable and non-renewable energy?", "Renewable sources such as sunlight and wind keep being supplied by nature; non-renewable ones such as coal and petrol will run out."),
           ("How can we save electricity at home?", "Switch off lights and fans when not needed, use LED bulbs and star-rated appliances, and dry clothes in the sun.")],
          lambda: [("Forms of energy", [(form, 6), (b["en"], 8), (ren, 6)]), ("Sources of energy", [(ren, 8), (b["en"], 6), (c_bill, 6)]), ("Energy changes", [(conv, 14), (b["en"], 6)]),
                   ("Saving energy", [(save, 14), (c_bill, 6)]), ("Mixed problems", [(save, 12), (c_bill, 8)])]),
        U(8, "clothes-how-things-are-made", 8, TA,
          "How clothes are made from fibres: natural and synthetic fibres and their sources; ginning, spinning, weaving, knitting and dyeing; handlooms and weavers of India; choosing clothes for weather and work; reusing and recycling clothes (summary of NCERT Our Wondrous World Chapter 8).",
          "Clothes: How Things are Made", "clothes: how things are made",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 8: natural and synthetic fibres, ginning, spinning and weaving, handloom saris of India, clothes for each season and reusing clothes. 100 questions with answers.",
          "Fibre → yarn → cloth → clothes.", "Natural fibres come from plants and animals.",
          "<p>Clothes are made from fibres. Natural fibres come from plants (cotton, jute, linen, coir) and animals (wool, silk); synthetic fibres such as nylon and polyester are made from chemicals from petroleum. Cotton is picked, ginned to remove seeds, spun into yarn, woven on a loom, dyed or printed and stitched into clothes.</p>"
          "<p>India's weavers make famous handloom cloth: Banarasi silk, Kanjeevaram silk, Pochampally ikat and Pashmina shawls. We choose clothes to suit the weather and work, and we reuse old clothes as bags, quilts and dusters.</p>",
          [("Removing seeds from cotton is…", ["the step after picking"], "ginning"), ("Kanjeevaram silk is from…", ["Kanchipuram"], "Tamil Nadu")],
          ["Mixing up spinning and weaving.", "Thinking silk is a plant fibre.", "Wearing synthetic clothes near fire."],
          [("What is the difference between weaving and knitting?", "Weaving crosses two sets of yarn on a loom; knitting makes cloth from a single yarn using needles or a machine."),
           ("Why is cotton good for summer?", "It absorbs sweat and lets air pass through, keeping us cool.")],
          lambda: [("Fibres", [(fib, 14), (b["cl"], 6)]), ("Where fibres come from", [(fsrc, 12), (b["cl"], 8)]), ("From fibre to cloth", [(c_cloth, 9), (b["cl"], 9), (fib, 2)]),
                   ("Weavers of India", [(saree, 16), (wear, 4)]), ("Clothes for every need", [(wear, 10), (saree, 4), (fib, 3), (b["cl"], 3)])]),
        U(9, "rhythms-of-nature", 9, AP,
          "Natural rhythms and cycles: day and night, the seasons, phases of the Moon and tides; the water cycle; how plants, animals and people change with the seasons, including migration, hibernation and crop seasons (summary of NCERT Our Wondrous World Chapter 9).",
          "Rhythms of Nature", "rhythms of nature",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 9: day and night, seasons, the water cycle, Moon and tides, migratory birds, hibernation, and kharif and rabi crops. 100 questions with answers.",
          "Nature repeats its patterns again and again.", "Day and night, seasons and the water cycle.",
          "<p>Nature has rhythms that repeat. Earth spins once in about 24 hours, giving day and night, and goes around the Sun once a year, giving the seasons. The Moon's shapes repeat about every 29 to 30 days. In the water cycle, water evaporates, condenses into clouds, falls as rain and collects in rivers and seas, again and again.</p>"
          "<p>Living things follow these rhythms: migratory birds visit India in winter, frogs breed in the monsoon and some animals hibernate. Farmers sow kharif crops such as rice with the monsoon and rabi crops such as wheat in winter.</p>",
          [("After condensation comes…", ["clouds → rain"], "precipitation"), ("Wheat is a… crop", ["sown in winter"], "rabi crop")],
          ["Thinking the Sun goes around Earth every day.", "Mixing up evaporation and condensation.", "Thinking rice is sown in winter."],
          [("What are the steps of the water cycle?", "Evaporation, condensation, precipitation and collection, repeating again and again."),
           ("What are kharif and rabi crops?", "Kharif crops are sown with the monsoon (rice, maize, cotton); rabi crops are sown in winter (wheat, mustard, gram).")],
          lambda: [("Day, night and seasons", [(b["rn"], 8), (seas, 6), (rhy, 6)]), ("The water cycle", [(wcyc, 9), (c_wcyc, 6), (b["rn"], 5)]), ("Rhythms in the sky", [(c_day, 12), (b["rn"], 8)]),
                   ("Plants, animals and seasons", [(b["rn"], 6), (crop, 14)]), ("Crops and farming", [(crop, 10), (c_day, 7), (b["rn"], 3)])]),
        U(10, "earth-our-shared-home", 10, AP,
          "Earth as a shared home for plants, animals and people; interdependence, producers, consumers and decomposers; food chains; threats to the environment and endangered animals; people and movements that protect nature; eco-friendly habits and the 3 Rs (summary of NCERT Our Wondrous World Chapter 10).",
          "Earth: Our Shared Home", "earth: our shared home",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 10: interdependence, producers, consumers and decomposers, food chains, protecting nature, Chipko and Project Tiger, and eco-friendly habits. 100 questions with answers.",
          "All living things share one Earth.", "Plants, animals and people depend on each other.",
          "<p>Earth is the shared home of all living things, and they depend on each other. Green plants are producers that make food from sunlight; animals are consumers; decomposers such as mushrooms and bacteria break down dead things and return nutrients to the soil. A food chain shows who eats whom, for example grass → grasshopper → frog → snake → eagle.</p>"
          "<p>Cutting forests, pollution and hunting put many animals in danger. People have protected nature through the Chipko movement, the Bishnoi community and Project Tiger. We can help with eco-friendly habits: reduce, reuse, recycle, compost and plant trees.</p>",
          [("In grass → deer → tiger, the deer eats…", ["follow the arrow"], "grass"), ("A mushroom is a…", ["breaks down dead things"], "decomposer")],
          ["Reading food chain arrows the wrong way.", "Thinking decomposers are harmful.", "Thinking one person cannot make a difference."],
          [("Why are decomposers important?", "They break down dead plants and animals and return nutrients to the soil for new plants."),
           ("What is the Chipko movement?", "A movement in which villagers hugged trees to stop them from being cut down.")],
          lambda: [("Living together on Earth", [(b["ea"], 10), (dep, 5), (role, 5)]), ("Producers, consumers and decomposers", [(role, 15), (b["ea"], 5)]), ("Food chains", [(c_chain, 20)]),
                   ("Protecting nature", [(hero, 9), (b["ea"], 5), (eco, 6)]), ("Eco-friendly habits", [(eco, 20)])]),
    ]
