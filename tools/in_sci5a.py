# -*- coding: utf-8 -*-
"""Class 5 EVS (NCERT Our Wondrous World, chapters 1–5): question makers and UNITS5a()."""
from uk_alsci import tq, once_maker
from in_sci import pairs, _R, U
from in_sci6a import odd_one, _cap
from in_sci3a import kid

LA, HW, II, TA, AP = "Life Around Us", "Health and Well-being", "Incredible India", "Things Around Us", "Our Amazing Planet"

# =================================================================== Chapter 1: water — the essence of life
WFORM = {"water in solid form": ["ice cubes", "snow", "hailstones", "a glacier", "frost on leaves", "icicles"],
         "water in liquid form": ["raindrops", "dew drops", "river water", "sea water", "water in a lake", "tap water"],
         "water in the form of a gas": ["water vapour in the air", "invisible vapour rising from wet clothes", "vapour rising from a puddle on a hot day"]}
WSRC5 = [("a glacier", "a huge, slow-moving mass of ice in the mountains"), ("groundwater", "water stored in the soil and rocks under the ground"),
         ("a spring", "water that flows out of the ground by itself"), ("a stepwell (baori)", "an old well with steps going down to the water"),
         ("a lake", "a large body of still water surrounded by land"), ("a pond", "a small body of still water"), ("the sea", "a huge body of salty water"),
         ("a canal", "a channel dug by people to carry water to fields"), ("a check dam", "a small wall built across a stream to slow down and store water"),
         ("a tube well", "a pipe drilled deep into the ground to pump up water")]
FRESH = [("A fish", "breathes through gills"), ("A duck", "has a flat beak and webbed toes for paddling"), ("A lotus", "has broad leaves that float on the water"),
         ("A frog", "can live both in water and on land"), ("A water strider", "walks on the surface of the water"), ("A crocodile", "lies in water with only its eyes and nose above it"),
         ("A turtle", "has a hard shell and paddle-like flippers or limbs"), ("A kingfisher", "dives into the water to catch fish")]
WQ = [("How much of Earth's surface is covered with water?", "about three-fourths", ["about one-tenth", "about half", "all of it"], "Most of it is salty sea water."),
      ("Why can we not drink sea water?", "it is too salty", ["it is too sweet", "it is frozen", "it is too hot"], "Only a little of Earth's water is fresh."),
      ("Where is most of Earth's fresh water stored?", "as ice in glaciers and ice caps", ["in taps", "in bottles", "in clouds only"], "Rivers and lakes hold only a little."),
      ("What happens to water when it is heated a lot?", "it turns into water vapour", ["it turns into ice", "it becomes salt", "it disappears forever"], "This is evaporation."),
      ("What happens to water when it is cooled below 0 °C?", "it freezes into ice", ["it boils", "it turns into vapour", "it becomes salt"], "Ice melts when warmed."),
      ("Why do wet clothes dry in the sun?", "the water evaporates", ["the water sinks into the cloth", "the sun eats the water", "the cloth drinks the water"], "Wind also helps."),
      ("Why do drops of water form on the outside of a glass of cold water?", "water vapour in the air cools and turns into drops", ["the glass leaks", "the water passes through the glass", "the glass sweats"], "This is condensation."),
      ("How do rivers and rain change the shape of the land?", "flowing water carries away soil and rocks and cuts valleys", ["water does not change land", "rain builds mountains", "rivers make land flat by freezing"], "This is erosion."),
      ("Why does groundwater go down when many tube wells are dug?", "more water is pumped out than seeps back in", ["tube wells add water", "rain stops falling", "the soil eats it"], "Recharge pits help."),
      ("What is rainwater harvesting?", "collecting and storing rainwater for later use", ["selling rain", "stopping rain", "throwing rainwater away"], "Rooftop rainwater can fill tanks or recharge wells."),
      ("Why do plants need water?", "to carry nutrients and to make food", ["to keep insects away", "to change colour only", "they do not need water"], "Plants wilt without water."),
      ("Why do animals in deserts drink less water?", "their bodies are adapted to save water", ["they do not need any water ever", "they drink only sea water", "they are always sleeping"], "Camels can go days without water."),
      ("Why should we not throw garbage into ponds and lakes?", "it pollutes the water and harms living things", ["it cleans the water", "fish eat it happily", "it makes the water sweet"], "Clean water is needed by all."),
      ("Why should drinking water be stored covered?", "to keep out dust, insects and germs", ["to make it warm", "to change its taste", "to make it salty"], "Use a clean ladle."),
      ("What is a johad?", "a traditional earthen pond that stores rainwater in Rajasthan", ["a type of fish", "a river island", "a water pump"], "Johads help groundwater recharge."),
      ("Why are stepwells found in dry parts of India such as Gujarat and Rajasthan?", "they were built to reach and store water in dry places", ["for swimming only", "there is too much rain there", "to keep water salty"], "Rani ki Vav in Patan is a famous stepwell."),
      ("What happens to snow on mountains in summer?", "it melts and flows into rivers", ["it turns into sand", "it becomes salt", "it stays forever"], "Himalayan rivers flow all year."),
      ("Why do some rivers of the Himalayas flow all year round?", "melting snow and ice feed them", ["it rains every day there", "they come from the sea", "pumps fill them"], "Rivers of the south depend more on rain."),
      ("Which simple way saves water while brushing teeth?", "turn off the tap while brushing", ["let the tap run", "brush under a shower", "use two buckets"], "A running tap wastes many litres."),
      ("Why is water called 'the essence of life'?", "no living thing can live without it", ["it is very costly", "it is found only in India", "it is a type of food"], "Our body is more than half water."),
      ("How much of the human body is water, roughly?", "about two-thirds", ["about one-tenth", "nothing", "all of it"], "That is why we must drink enough water."),
      ("Why is it important to fix a leaking tap quickly?", "a dripping tap wastes a lot of water over time", ["drips are good for pipes", "it saves water", "it is not important"], "Every drop counts."),
      ("Which water body is formed when a river is blocked by a dam?", "a reservoir", ["a delta", "a glacier", "a spring"], "Reservoirs store water for drinking and farming."),
      ("Why do the leaves of a lotus not get wet?", "they have a waxy, water-repelling surface", ["they are made of plastic", "they are always dry", "they drink the water"], "Water rolls off as drops."),
      ("Why are wetlands important?", "they store water, clean it and are homes for many birds and fish", ["they are useless land", "they cause droughts", "they have no life"], "Chilika Lake is a famous wetland."),
      ("What do we call a long period with very little rain?", "a drought", ["a flood", "a cyclone", "a monsoon"], "Crops fail in a drought."),
      ("What do we call it when a river overflows its banks?", "a flood", ["a drought", "a glacier", "an echo"], "Heavy monsoon rain can cause floods."),
      ("Why is the monsoon important for India?", "it brings most of the year's rain for crops and drinking water", ["it brings snow to deserts", "it stops all rivers", "it makes the sea fresh"], "It arrives in Kerala in early June."),
      ("Why does water in an earthen pot stay cool?", "some water seeps out and evaporates from the surface", ["clay makes ice", "the pot is in the fridge", "the water is salty"], "Evaporation causes cooling."),
      ("Which gas do fish take from the water to breathe?", "oxygen dissolved in the water", ["carbon dioxide only", "smoke", "salt"], "They use their gills."),
      ("What is a puddle on the road after rain an example of?", "water collecting in a low place", ["groundwater rising", "a glacier", "a spring"], "It dries by evaporation."),
      ("Why do farmers in dry areas use drip irrigation?", "it gives water drop by drop to the roots and saves water", ["it floods the fields", "it wastes water", "it uses sea water"], "Sprinklers also save water.")]


def c_water5(k=None):
    R = _R[0]
    k = k or R.choice(["leak", "bucket", "family"])
    if k == "leak":
        n, d = R.choice([5, 8, 10, 12, 15, 20]), R.choice([7, 10, 30])
        return tq("A leaking tap wastes %d litres of water a day. How much water does it waste in %d days?" % (n, d), "%d litres" % (n * d),
                  ["%d litres" % x for x in (n + d, n * d + n, n * (d - 1))], "%d × %d = %d litres." % (n, d, n * d))
    if k == "bucket":
        sh, bu, d = R.choice([60, 70, 80, 90]), R.choice([15, 18, 20, 25]), R.choice([5, 7, 10])
        n = kid()
        s = sh - bu
        return tq("%s used %d litres of water for a shower but only %d litres when bathing with a bucket. How much water does %s save in %d days by using a bucket?" % (n, sh, bu, n, d),
                  "%d litres" % (s * d), ["%d litres" % x for x in (s, sh * d, bu * d)], "Saving each day: %d − %d = %d litres; in %d days: %d × %d = %d litres." % (sh, bu, s, d, s, d, s * d))
    p, l = R.choice([4, 5, 6]), R.choice([40, 50, 60])
    return tq("A family of %d people uses %d litres of water per person each day. How much water does the family use in a day?" % (p, l), "%d litres" % (p * l),
              ["%d litres" % x for x in (p + l, l, p * l + l)], "%d × %d = %d litres." % (p, l, p * l))


# =================================================================== Chapter 2: journey of a river
RIV = [("The Ganga", "begins at the Gangotri glacier in Uttarakhand"), ("The Yamuna", "begins at the Yamunotri glacier and joins the Ganga at Prayagraj"),
       ("The Narmada", "flows west into the Arabian Sea"), ("The Brahmaputra", "flows through Assam and has the river island Majuli"),
       ("The Godavari", "is the longest river of peninsular India"), ("The Kaveri", "flows through Karnataka and Tamil Nadu"), ("The Indus", "flows through Ladakh"),
       ("The Mahanadi", "has the Hirakud Dam in Odisha"), ("The Hooghly", "flows past the city of Kolkata"), ("The Tapi", "flows west like the Narmada and reaches the sea near Surat"),
       ("The Krishna", "flows through Maharashtra, Karnataka, Telangana and Andhra Pradesh"), ("The Sutlej", "has the Bhakra Nangal Dam")]
RPART = [("the source", "the place where a river begins"), ("a tributary", "a smaller river that joins a bigger river"), ("the mouth", "the place where a river meets the sea"),
         ("a delta", "a fan-shaped area of new land formed by soil at a river's mouth"), ("a meander", "a big bend in a river flowing across flat land"),
         ("a confluence (sangam)", "the place where two rivers meet"), ("the river bed", "the floor of a river"), ("the banks", "the land on both sides of a river"),
         ("a floodplain", "flat land beside a river that gets covered in floods"), ("a waterfall", "a place where a river drops over a steep cliff"),
         ("an oxbow lake", "a curved lake left behind when a river cuts off one of its bends"), ("a valley", "low land between hills, often cut by a river")]
RHARM = {"something that harms a river": ["dumping garbage into it", "letting factory waste flow into it", "washing clothes with detergent in it", "throwing plastic bags into it",
                                          "sending dirty drain water into it", "cutting trees along its banks", "digging too much sand from its bed", "immersing idols painted with harmful paints", "throwing flowers in plastic bags into it"],
         "something that protects a river": ["planting trees along its banks", "treating dirty water before it reaches the river", "using cloth bags instead of plastic",
                                             "cleaning the ghats together", "making compost instead of dumping waste", "using river water carefully for farming",
                                             "immersing only eco-friendly clay idols in tanks", "reporting factories that dump waste"]}
RSTEP = ["a glacier or spring in the mountains", "a small, fast stream", "a river rushing down hill valleys", "a wide, slow river in the plains", "a delta near the coast", "the sea"]


def c_river(k=None):
    R = _R[0]
    st = RSTEP
    i = R.randrange(len(st) - 1)
    if R.random() < 0.5:
        others = [x for x in st if x not in (st[i], st[i + 1])]
        return tq("A river starts as %s. In its journey, what comes just after “%s”?" % (st[0], st[i]), st[i + 1], R.sample(others, 3), "The journey: " + " → ".join(st) + ".")
    j = i + 1
    others = [x for x in st if x not in (st[j], st[i])]
    return tq("In a river's journey to the sea, what comes just before “%s”?" % st[j], st[i], R.sample(others, 3), "The journey: " + " → ".join(st) + ".")


RVQ = [("Where do many big rivers of north India begin?", "in glaciers of the Himalayas", ["in the sea", "in deserts", "in big cities"], "The Ganga begins at Gangotri."),
       ("Why does a river flow fast in the mountains?", "the land is steep", ["the land is flat", "the water is salty", "the wind pushes it"], "It slows down in the plains."),
       ("Why does a river become wide and slow in the plains?", "the land is flat", ["the land is steep", "it freezes", "it is pumped"], "It makes big bends there."),
       ("Why is the soil of river plains good for farming?", "rivers leave fertile soil (silt) during floods", ["it is full of salt", "it is rocky", "it is frozen"], "The Indo-Gangetic plains grow a lot of food."),
       ("Where does the Ganga meet the sea?", "the Bay of Bengal", ["the Arabian Sea", "the Indian Ocean near Kerala", "the Dal Lake"], "The Sundarbans delta is there."),
       ("Which large river delta, home of the Bengal tiger, is formed by the Ganga and Brahmaputra?", "the Sundarbans", ["the Thar", "the Deccan", "the Rann of Kutch"], "It has mangrove forests."),
       ("Which is the largest river island in India?", "Majuli in the Brahmaputra", ["Lakshadweep", "Sri Lanka", "Andaman"], "Majuli is in Assam."),
       ("Which famous fair is held on the banks of rivers at Prayagraj, Haridwar, Ujjain and Nashik?", "the Kumbh Mela", ["the Pushkar camel fair", "the Hornbill Festival", "the Rann Utsav"], "Millions of people come."),
       ("What is a ghat on a river?", "steps leading down to the water", ["a type of boat", "a river fish", "a bridge"], "Varanasi has many ghats."),
       ("Why are dams built on rivers?", "to store water, control floods and make electricity", ["to make rivers salty", "to stop rain", "to dry up rivers"], "Bhakra Nangal is a big dam."),
       ("Which famous dam stands on the Sutlej river?", "the Bhakra Nangal Dam", ["the Hirakud Dam", "the Sardar Sarovar Dam", "the Tehri Dam"], "It is one of India's highest dams."),
       ("Which big dam is built on the Narmada in Gujarat?", "the Sardar Sarovar Dam", ["the Bhakra Nangal Dam", "the Hirakud Dam", "the Tehri Dam"], "It supplies water to dry areas."),
       ("How does a river help people?", "it gives water for drinking, farming, fishing and transport", ["it gives nothing", "it only causes floods", "it only carries garbage"], "Many cities grew along rivers."),
       ("Why did many old cities grow beside rivers?", "rivers gave water, food and an easy way to travel", ["rivers kept people away", "there was no water elsewhere at all", "rivers were dry"], "Varanasi and Patna are on the Ganga."),
       ("Which animal of the Ganga is India's national aquatic animal?", "the Ganges river dolphin", ["the crocodile", "the shark", "the octopus"], "It is nearly blind and uses sound to find food."),
       ("Why is the Ganges river dolphin in danger?", "pollution, dams and fishing nets harm it", ["it eats too much", "it is too big", "there are too many"], "Clean rivers help it."),
       ("What is the Namami Gange programme?", "a government plan to clean and protect the Ganga", ["a cricket league", "a dance form", "a new dam"], "It began in 2014."),
       ("Why does a river water look muddy after heavy rain?", "rain washes soil from the land into it", ["fish make it muddy", "the sky colours it", "it is frozen"], "Tree roots hold soil."),
       ("Why should we not wash cattle and vehicles in rivers?", "it pollutes the water", ["it cleans the river", "it is good for fish", "it adds oxygen"], "Use water away from the river."),
       ("What does a river carry to the sea?", "water, soil and pebbles", ["only salt", "only fish", "nothing"], "The soil builds a delta."),
       ("Why are river pebbles smooth and round?", "rubbing against each other in flowing water wears them smooth", ["people polish them", "they grow round", "fish lick them"], "This takes a very long time."),
       ("Why does the Narmada flow west while most big Indian rivers flow east?", "the land slopes towards the west there", ["it likes the Arabian Sea", "the wind pushes it", "people dug it"], "The Tapi also flows west."),
       ("What do we call a river that flows into a bigger river?", "a tributary", ["a delta", "a mouth", "a source"], "The Yamuna is a tributary of the Ganga."),
       ("Where do the Ganga and the Yamuna meet?", "at Prayagraj", ["at Kolkata", "at Delhi", "at Patna"], "It is called the Triveni Sangam."),
       ("Why do fishermen in Kerala's backwaters use Chinese fishing nets?", "the big nets on poles can be lowered and lifted to catch many fish", ["to catch birds", "to stop boats", "for decoration only"], "They are seen in Kochi."),
       ("Which river flows past Ahmedabad?", "the Sabarmati", ["the Kaveri", "the Hooghly", "the Brahmaputra"], "Gandhiji's ashram is on its bank."),
       ("Why do rivers in south India flow less in summer?", "they depend mostly on rain, not on melting snow", ["they freeze", "they flow backwards", "they are dammed by sand"], "They fill up in the monsoon."),
       ("What is a river island called in Assam where the Brahmaputra flows?", "a char or chapori", ["a delta", "a ghat", "a glacier"], "People farm on them."),
       ("Why should we not dig a lot of sand from river beds?", "it damages the river and its banks and harms water life", ["it makes the river deeper and healthier", "it is good for fish", "sand grows back at once"], "Sand mining must be controlled."),
       ("Which famous river, called the 'Dakshin Ganga', flows through Maharashtra, Telangana and Andhra Pradesh?", "the Godavari", ["the Narmada", "the Indus", "the Hooghly"], "It flows into the Bay of Bengal."),
       ("What is the place where a river begins called?", "its source", ["its mouth", "its delta", "its bank"], "The source may be a glacier, spring or lake."),
       ("Why do some rivers dry up in summer?", "they are fed mainly by rain", ["they are fed by glaciers", "they flow uphill", "fish drink them"], "Monsoon rain fills them again."),
       ("Why are trees along river banks useful?", "their roots hold the soil and stop it washing away", ["they make the river salty", "they dry the river", "they cause floods"], "Tree cover protects banks."),
       ("Why do people living by rivers build embankments?", "to protect their homes and fields from floods", ["to stop the river reaching the sea", "to make the river faster", "to catch fish"], "Embankments are walls of earth."),
       ("What is the Brahmaputra called in Tibet?", "the Tsangpo (Yarlung Tsangpo)", ["the Hooghly", "the Teesta", "the Sutlej"], "It flows into India through Arunachal Pradesh."),
       ("Why do boats carry goods on rivers such as the Brahmaputra and the Ganga?", "river transport is cheap for heavy goods", ["roads are not allowed", "boats are faster than planes", "rivers have no water"], "National Waterway 1 is on the Ganga."),
       ("Why do farmers dig canals from rivers?", "to carry water to their fields", ["to drain the river dry", "to stop the rain", "to catch birds"], "Canals help in dry regions."),
       ("What makes a waterfall form on a river?", "the river flows over a steep drop in the land", ["fish jump high", "rain falls only there", "people pour water"], "Jog Falls in Karnataka is famous."),
       ("Which famous waterfall is on the Sharavati river in Karnataka?", "Jog Falls", ["Dudhsagar Falls", "Athirappilly Falls", "Hundru Falls"], "It is one of India's highest waterfalls."),
       ("Why do many Indian festivals take place on river banks?", "rivers are honoured as sources of life", ["rivers are dangerous", "it is a law", "there is no other space"], "Chhath Puja is celebrated at river ghats.")]

# =================================================================== Chapter 3: the mystery of food
DEFIC = [("night blindness", "too little vitamin A"), ("scurvy (bleeding gums)", "too little vitamin C"), ("rickets (weak, bent bones)", "too little vitamin D"),
         ("anaemia (tiredness and pale skin)", "too little iron"), ("goitre (swelling in the neck)", "too little iodine"), ("beriberi (weak muscles)", "too little vitamin B1")]
RICH5 = [("carrots and papaya", "vitamin A"), ("amla, oranges and lemons", "vitamin C"), ("fish and egg yolk", "vitamin D"), ("spinach, jaggery and dates", "iron"),
         ("iodised salt and seafood", "iodine"), ("milk, curd and ragi", "calcium"), ("dal, eggs and soybean", "proteins"), ("rice, wheat and potatoes", "carbohydrates"),
         ("ghee, butter and oil", "fats"), ("whole grains, fruits and vegetables", "dietary fibre")]
STORE = [("onions and potatoes", "a cool, dry and airy place"), ("milk", "boiling it and keeping it in a refrigerator"), ("rice and wheat grains", "airtight bins with dried neem leaves"),
         ("leafy vegetables", "wrapped in a damp cloth in a cool place"), ("cooked food", "covered, and eaten soon or kept cold"), ("pickles", "dry glass jars with tight lids"),
         ("flour (atta)", "a dry, closed container away from moisture"), ("fresh fish", "on ice or in a freezer"),
         ("bananas", "a cool place away from the refrigerator"), ("honey", "a dry, clean, tightly closed jar")]
SNACK = {"a healthy snack": ["roasted chana", "a fresh fruit", "a sprouts salad", "a glass of buttermilk", "roasted makhana", "a handful of peanuts", "a bowl of curd", "boiled sweet corn", "a slice of watermelon", "poha with vegetables"],
         "junk food that is unhealthy if eaten often": ["potato chips", "a cola drink", "instant noodles", "cream biscuits", "a fried samosa every day", "a chocolate bar every day", "a packet of salty namkeen every day", "sugary packaged juice"]}
FDQ = [("Why does milk turn into curd when a little curd is added to warm milk?", "tiny helpful bacteria in the curd change the milk", ["the milk freezes", "the milk boils away", "sugar turns it into curd"], "This is a kind of fermentation."),
       ("Why does idli and dosa batter rise when it is kept overnight?", "tiny microbes in it make gas bubbles (fermentation)", ["the batter freezes", "salt pushes it up", "the bowl grows"], "Fermentation makes it soft."),
       ("Why does a piece of roti start to taste sweet if you chew it for a long time?", "saliva breaks the starch into sugar", ["the roti has hidden sugar", "teeth make sugar", "it is magic"], "Digestion starts in the mouth."),
       ("Where does digestion of food begin?", "in the mouth", ["in the legs", "in the lungs", "in the heart"], "Chewing and saliva begin it."),
       ("Which simple test shows that a food has starch?", "a drop of iodine solution turns it blue-black", ["it turns red with water", "it smells sweet", "it floats in water"], "Try it on a slice of potato."),
       ("Why should our plate have food of different colours?", "different foods give different nutrients", ["colours make food tasty only", "colourful food is junk", "it does not matter"], "Eat the rainbow."),
       ("What is a balanced diet?", "food with all the nutrients in the right amounts", ["food with only fats", "only fruits", "only sweets"], "Grains, pulses, vegetables, fruits and milk."),
       ("Why is eating too much salt bad?", "it can raise blood pressure", ["it makes bones stronger", "it gives vitamins", "it cures diseases"], "Use salt in moderation."),
       ("Why is eating too much sugar bad?", "it can cause tooth decay and too much weight", ["it builds muscles", "it protects eyes", "it is a vitamin"], "Fruits are a better sweet."),
       ("Why does bread grow green or black fuzzy spots when kept for many days?", "mould (a kind of fungus) grows on it", ["it ripens", "it turns into a plant", "sunlight colours it"], "Do not eat mouldy food."),
       ("Why do we keep food in a refrigerator?", "cold slows down the growth of germs", ["cold kills all germs at once", "it makes food sweeter", "it adds vitamins"], "Food still spoils slowly."),
       ("Why are dried fruits such as raisins kept for a long time without spoiling?", "germs cannot grow well without water", ["they are made of plastic", "they are frozen", "they have no taste"], "Drying is an old way to preserve food."),
       ("Why is salt added to pickles?", "salt stops germs growing", ["salt adds vitamins", "salt makes them sweet", "salt makes them rot"], "Oil also helps."),
       ("Why should we read the date on a food packet?", "to check that it is still safe to eat", ["to know the colour", "to know the weight of the shop", "it has no use"], "Check the 'use by' or 'best before' date."),
       ("What does FSSAI on a food packet stand for?", "the Food Safety and Standards Authority of India", ["a type of vitamin", "a cricket team", "a food colour"], "It checks that food is safe."),
       ("Why is the mid-day meal (PM POSHAN) given in schools?", "to give children nutritious food and help them learn", ["to stop children studying", "to sell food", "for no reason"], "It is one of the largest school meal plans in the world."),
       ("Why should we eat millets such as ragi, jowar and bajra?", "they are rich in fibre, iron and calcium", ["they have no nutrients", "they are junk food", "they are full of fat"], "2023 was the International Year of Millets."),
       ("Why do we need dietary fibre?", "it helps food move through the intestines and prevents constipation", ["it builds bones", "it gives the most energy", "it is a vitamin"], "Whole grains and vegetables have fibre."),
       ("Why should we drink enough water every day?", "water helps digestion and keeps the body cool", ["water makes us weak", "water has fat", "it is not needed"], "Drink more in summer."),
       ("Why do we feel hungry?", "the body needs energy and nutrients", ["the stomach is full", "we are sleepy", "we drank water"], "Eat at regular times."),
       ("Which food gives quick energy to a tired runner?", "a banana or jaggery", ["salt", "water only", "a raw egg shell"], "They have natural sugars."),
       ("Why should we wash fruits and vegetables before eating?", "to remove dirt, germs and sprays", ["to make them sweet", "to change their colour", "to make them heavier"], "Use clean water."),
       ("Why is it better to steam or boil vegetables lightly than to overcook them?", "overcooking destroys some vitamins", ["overcooking adds vitamins", "raw is always unsafe", "it does not matter"], "Cook with the lid on."),
       ("Why do people cook food?", "cooking makes food soft, tasty and kills germs", ["cooking removes all nutrients", "to waste fuel", "food cannot be eaten raw at all"], "Fruits and salads are eaten raw."),
       ("Why is breakfast important?", "it gives energy after the long night", ["it makes us sleepy", "it is the least useful meal", "it causes illness"], "Do not skip it."),
       ("Which part of a meal gives protein to vegetarians?", "dal, paneer, soybean or nuts", ["only rice", "only pickle", "only sugar"], "Pulses are rich in protein."),
       ("Why should food not be wasted?", "many people do not have enough to eat and growing food uses water and work", ["food grows on its own", "wasting food is good", "food is not valuable"], "Take only what you can eat."),
       ("Why should we chew our food well?", "it breaks food into small pieces and helps digestion", ["it slows digestion", "it hurts teeth", "it is not needed"], "Eat slowly."),
       ("Which food group should make up most of our plate?", "whole grains and vegetables", ["sweets", "fried snacks", "cold drinks"], "Add pulses and fruits too."),
       ("Why should we not eat while watching a screen?", "we may not notice how much we eat", ["it improves digestion", "it adds vitamins", "it makes food tasty"], "Eat mindfully."),
       ("Why do people add lemon juice to dal or salad?", "it adds vitamin C and taste", ["it adds fat", "it removes all germs", "it makes food salty"], "Vitamin C helps the body use iron."),
       ("Why is jaggery sometimes given to people with anaemia?", "it contains iron", ["it contains iodine", "it has no nutrients", "it is a vitamin A food"], "Green leafy vegetables also have iron."),
       ("Why is sunlight important for strong bones?", "the skin makes vitamin D in sunlight", ["sunlight gives calcium", "sunlight cleans bones", "sunlight gives iron"], "Vitamin D helps the body use calcium."),
       ("Why is it unsafe to eat food from a swollen or leaking can?", "germs may have grown inside it", ["it has more vitamins", "it is fresher", "it is sweeter"], "Throw it away."),
       ("What is a food label?", "printed information on a packet about ingredients, nutrients and dates", ["the price only", "a brand picture only", "a recipe book"], "Read it before buying."),
       ("Why does cut apple turn brown?", "air reacts with the cut surface", ["it is ripening", "germs paint it", "the knife colours it"], "A little lemon juice slows it.")]

# =================================================================== Chapter 4: our school — a happy place
SAFE5 = [("an earthquake", "drop, cover your head and hold on under a strong table"), ("a fire alarm", "walk out calmly in a line, without running or pushing"),
         ("a stranger at the school gate asking you to come along", "say no and tell a teacher at once"), ("a classmate who has fainted", "call a teacher or the school nurse at once"),
         ("a spilled liquid on the corridor floor", "warn others and tell a staff member"), ("a fallen electric wire", "stay away and tell an adult"), ("a dog wandering into the school ground", "stay calm, do not run and tell a teacher"),
         ("thunder and lightning during a game outside", "go indoors and stay away from tall trees"), ("smoke coming from a classroom", "raise the alarm and leave the building"), ("a small cut on your knee while playing", "wash it and ask a teacher for first aid")]
KIND = {"a kind or helpful action at school": ["sharing crayons with a classmate", "helping a new student find the library", "waiting for your turn on the slide",
                                               "picking up litter in the playground", "including a quiet child in a game", "thanking the cook for the mid-day meal",
                                               "saying sorry after bumping into someone", "helping a classmate in a wheelchair reach the stage",
                                               "returning a lost pencil to its owner", "cheering for both teams on Sports Day"],
        "an unkind or unsafe action at school": ["pushing in a queue", "calling someone hurtful names", "running on the stairs", "leaving taps running in the washroom",
                                                 "laughing at someone's mistake", "scribbling on desks and walls", "leaving a friend out on purpose", "breaking a library book",
                                                 "throwing a ball near the classroom windows", "spreading rumours about a classmate"]}
INCL = [("braille", "people who cannot see read by touch"), ("sign language", "people who cannot hear talk with their hands"), ("a ramp", "people using wheelchairs enter buildings"),
        ("a hearing aid", "people who are hard of hearing hear better"), ("a white cane", "people who cannot see walk safely"), ("large-print books", "people with weak eyesight read easily"),
        ("a reserved seat near the board", "a child who finds it hard to see the board"),
        ("an audio book", "people who cannot see enjoy stories by listening"), ("handrails on stairs", "older people and children climb safely")]
TEAM = [("the school captain", "leading and helping students follow rules"), ("the librarian", "looking after the books and helping us find them"), ("the school nurse", "giving first aid when someone is hurt"),
        ("the cook", "preparing the mid-day meal"), ("the gardener", "looking after the plants in the school garden"), ("the bus driver", "taking children safely to and from school"),
        ("the security guard", "keeping strangers out and the school safe"), ("the sweeper", "keeping the classrooms and grounds clean"), ("the principal", "running the whole school and its teachers"),
        ("the sports teacher", "training students in games and exercise")]
SCQ = [("Why do schools have rules?", "rules keep everyone safe and help us learn together", ["to make school boring", "only to punish children", "rules have no use"], "Rules are for everyone."),
       ("Why do we line up during a fire drill?", "so that everyone can leave quickly and safely", ["to play a game", "to wait for food", "to block the door"], "Never use a lift in a fire."),
       ("What should you do during an earthquake drill?", "drop, cover and hold on", ["run to the window", "climb on the desk", "stand under a fan"], "Stay away from glass."),
       ("What is teamwork?", "working together to reach a shared goal", ["working alone always", "fighting over work", "copying others"], "A class garden needs teamwork."),
       ("What is bullying?", "hurting or frightening someone again and again on purpose", ["playing a fair game", "helping a friend", "sharing lunch"], "Always tell a trusted adult."),
       ("What should you do if you see someone being bullied?", "tell a teacher and support the child", ["join in", "laugh", "ignore it forever"], "Speaking up helps."),
       ("Why should we respect people who are different from us?", "everyone has the same right to be valued and safe", ["different people are less important", "respect is only for teachers", "it is not needed"], "Differences make a class richer."),
       ("Why does a school need ramps and wide doors?", "so that children using wheelchairs can move around easily", ["for decoration", "to make running easier only", "to store bicycles"], "This is called inclusion."),
       ("What does 'inclusion' mean in a school?", "making sure every child can take part and feel welcome", ["keeping some children out", "only toppers can join", "only one game for all"], "Everyone belongs."),
       ("Why is it important to listen when others are speaking?", "it shows respect and helps us understand", ["listening wastes time", "only teachers should be heard", "it is rude"], "Raise your hand to speak."),
       ("Why should we keep our classroom clean?", "a clean room is healthy and pleasant for everyone", ["dirt is good for learning", "the sweeper should do everything", "it does not matter"], "Use the dustbin."),
       ("How can you help a new student feel welcome?", "say hello, show them around and invite them to play", ["ignore them", "make fun of their accent", "hide their bag"], "Remember your own first day."),
       ("Why should we not waste water in the school washroom?", "water is precious and shared by all", ["water never runs out", "it is free so it does not matter", "running taps are good"], "Close the tap after use."),
       ("What can you do when you feel angry with a friend at school?", "take a deep breath and talk about it calmly", ["hit them", "shout at them", "break their pencil"], "Ask a teacher to help if needed."),
       ("Why do schools have a school garden?", "students learn about plants and enjoy growing food and flowers", ["to make the school dirty", "for keeping cattle", "it has no use"], "Many schools grow vegetables."),
       ("Why is a library a happy place for many children?", "books take us to new places and ideas", ["it is noisy", "nobody reads there", "books are only for adults"], "Return books on time."),
       ("Why should we not run in corridors and on stairs?", "we may fall or knock someone over", ["running is always safe", "stairs are made for running", "it makes us faster at studying"], "Walk on the left."),
       ("What should you do if you lose something at school?", "tell the teacher or check the lost-and-found box", ["take someone else's", "cry and go home", "keep it secret"], "Write your name on your things."),
       ("Why is it good to have a class monitor?", "the monitor helps the teacher and the class follow rules", ["the monitor punishes everyone", "to make others feel small", "it is of no use"], "Everyone can take turns."),
       ("Why do we celebrate events such as Sports Day and Annual Day?", "they help us show talents and enjoy together", ["to stop studies forever", "only to win prizes", "they have no use"], "Taking part matters most."),
       ("Why is it good to make mistakes and learn from them?", "mistakes help us learn and improve", ["mistakes mean we are bad", "we should never try", "only toppers learn"], "Try again."),
       ("What is a school safety plan?", "a plan that tells everyone what to do in emergencies", ["a sports timetable", "a lunch menu", "a seating chart for exams"], "Practise drills regularly."),
       ("Why should students wash hands before the mid-day meal?", "to remove germs and stay healthy", ["to make food tasty", "to waste water", "it is not needed"], "Use soap."),
       ("What makes a school a happy place?", "friendly people, fair rules, safety and caring for each other", ["only holidays", "no rules at all", "only exams"], "Everyone can help."),
       ("Why should we take care of school property?", "it is shared by everyone and used by many children after us", ["it belongs to nobody", "it is easy to replace", "breaking it is fun"], "Books and desks are for all."),
       ("Why do some schools teach basic sign language to all students?", "so that everyone can talk with classmates who cannot hear", ["to keep secrets", "to replace speaking", "it is a game"], "Indian Sign Language is used in India."),
       ("Which number is the helpline for children in need in India?", "1098", ["101", "100", "108"], "It is called Childline."),
       ("Why should we not share our passwords or photos with strangers online?", "it keeps us safe from people who may misuse them", ["strangers always help", "passwords are not important", "sharing is always good"], "Tell an adult if something online worries you."),
       ("Why do we have a school assembly?", "to begin the day together with news, songs and the pledge", ["to give exams", "to eat lunch", "to play cricket"], "It builds a sense of belonging."),
       ("Why should we not bring sharp objects or matches to school?", "they can hurt someone", ["they are useful toys", "teachers like them", "they help in exams"], "Safety first."),
       ("Why should students cross the road near school only at the zebra crossing?", "it is the safe place for people to cross", ["it is shorter", "cars go faster there", "it does not matter"], "Look right, left and right again."),
       ("Why is it good to work in groups on a project?", "everyone shares ideas and learns from each other", ["only one person does all the work", "groups always fight", "it wastes time"], "Give everyone a role."),
       ("Why should we say thank you to the school staff?", "it shows respect for their work", ["it is a waste of time", "they are not important", "it is only for teachers"], "Kind words matter."),
       ("What can you do if you feel worried about an exam?", "plan a little study each day and talk to a teacher or parent", ["stay up all night", "skip meals", "hide the worry"], "Rest and sleep help too."),
       ("Why should every child get a chance to speak in class?", "everyone's ideas are valuable", ["only toppers should speak", "the loudest should speak", "nobody should speak"], "Take turns."),
       ("Why should we keep the school toilets clean?", "clean toilets stop diseases and are pleasant for all", ["they clean themselves", "it is only the sweeper's job", "dirty toilets are healthy"], "Flush and wash hands.")]


# =================================================================== Chapter 5: our vibrant country
DANCE = [("Bhangra", "Punjab"), ("Garba", "Gujarat"), ("Bihu", "Assam"), ("Ghoomar", "Rajasthan"), ("Lavani", "Maharashtra"), ("Kathakali", "Kerala"),
         ("Bharatanatyam", "Tamil Nadu"), ("Kuchipudi", "Andhra Pradesh"), ("Odissi", "Odisha"), ("Manipuri", "Manipur"), ("Yakshagana", "Karnataka"), ("Kalbelia", "Rajasthan"), ("Giddha", "Punjab"),
         ("Mohiniyattam", "Kerala"), ("Sattriya", "Assam")]
ART = [("Madhubani painting", "Bihar"), ("Warli painting", "Maharashtra"), ("Pattachitra", "Odisha"), ("Gond painting", "Madhya Pradesh"), ("Phulkari embroidery", "Punjab"),
       ("Kalamkari", "Andhra Pradesh"), ("Chikankari embroidery", "Uttar Pradesh"), ("Pichwai painting", "Rajasthan"), ("Tanjore painting", "Tamil Nadu"), ("Kantha embroidery", "West Bengal"),
       ("Bidriware", "Karnataka"), ("Dhokra metal craft", "Chhattisgarh"), ("blue pottery", "Rajasthan")]
DISH = [("dhokla", "Gujarat"), ("litti chokha", "Bihar"), ("sarson ka saag and makki ki roti", "Punjab"), ("dal baati churma", "Rajasthan"), ("puran poli", "Maharashtra"),
        ("bisi bele bath", "Karnataka"), ("puttu and kadala curry", "Kerala"), ("thukpa", "Ladakh"), ("rogan josh", "Jammu and Kashmir"), ("pitha", "Assam"), ("macher jhol (fish curry)", "West Bengal"), ("momos and gundruk", "Sikkim")]
HARV = [("Pongal", "Tamil Nadu"), ("Onam", "Kerala"), ("Bihu", "Assam"), ("Baisakhi", "Punjab"), ("Nuakhai", "Odisha"), ("Wangala", "Meghalaya"), ("Lohri", "Punjab")]
VBQ = [("What does 'unity in diversity' mean?", "people of many languages, religions and customs live together as one nation", ["everyone in India is the same", "people never meet", "there is only one language"], "India is a land of many cultures."),
       ("How many languages are listed in the Eighth Schedule of the Indian Constitution?", "22", ["2", "10", "100"], "Hindi, Tamil, Bengali and Marathi are some of them."),
       ("Why do clothes differ from one region of India to another?", "weather, work and traditions differ", ["people copy each other", "there is only one cloth", "laws decide colours"], "Woollens in hills, cotton in hot plains."),
       ("Which garment is a long piece of cloth draped by many women in India?", "the sari", ["the turban", "the coat", "the cap"], "Saris are draped in many styles."),
       ("What is the traditional dress worn by men in Kerala, a white cloth wrapped around the waist?", "the mundu", ["the pheran", "the sherwani", "the kurta"], "It is worn with a shirt."),
       ("What is a pheran?", "a long woollen gown worn in Kashmir in winter", ["a dance of Gujarat", "a sweet of Bengal", "a boat of Kerala"], "A kangri is kept inside it for warmth."),
       ("Why is rice eaten more in eastern and southern India?", "these regions get plenty of rain, which rice needs", ["rice grows in snow", "rice needs no water", "wheat is not allowed"], "Wheat grows well in the north."),
       ("What do we call the art of making colourful designs on the floor with powder or rice flour?", "rangoli", ["origami", "pottery", "weaving"], "It is called kolam in Tamil Nadu."),
       ("Which festival of lights is celebrated across India?", "Diwali", ["Holi", "Pongal", "Onam"], "Diyas and lamps are lit."),
       ("Which festival is known as the festival of colours?", "Holi", ["Diwali", "Eid", "Christmas"], "It is celebrated in spring."),
       ("Why do people of different faiths join in each other's festivals?", "it builds friendship and respect", ["it is a rule", "they have no festivals of their own", "it is a competition"], "Sweets are shared at Eid, Diwali and Christmas."),
       ("What is a folk song?", "a traditional song passed down by people of a region", ["a song from a film only", "a song in a foreign language", "a song without music"], "Folk songs tell of harvests and seasons."),
       ("Which musical instrument is a stringed instrument often played in Indian classical music?", "the sitar", ["the tabla", "the dhol", "the flute"], "The tabla is a pair of drums."),
       ("Which drum is played in Bhangra?", "the dhol", ["the sitar", "the veena", "the shehnai"], "It is a big two-sided drum."),
       ("How have some festivals and customs changed over time?", "people now use eco-friendly colours, clay idols and fewer crackers", ["festivals have stopped", "nothing ever changes", "everyone celebrates alone"], "Traditions change with time."),
       ("Why are clay Ganesha idols better than plaster of Paris idols?", "clay dissolves in water and does not pollute it", ["plaster dissolves faster", "clay pollutes water", "they are the same"], "Eco-friendly idols protect lakes."),
       ("Which classical dance form from Uttar Pradesh is known for fast spins and footwork with ankle bells?", "Kathak", ["Bihu", "Garba", "Yakshagana"], "Kathak means 'storyteller'."),
       ("What are puppets in Rajasthan's traditional puppet shows called?", "kathputli", ["kolam", "kantha", "chhau"], "The puppets are moved with strings."),
       ("Why is India's food so varied?", "different regions grow different crops and have their own traditions", ["everyone eats only rice", "there is only one cuisine", "spices are banned"], "Each state has special dishes."),
       ("Which state is famous for tea from the hills of Darjeeling?", "West Bengal", ["Rajasthan", "Punjab", "Goa"], "Assam is also famous for tea."),
       ("Why should we learn a few words of another Indian language?", "it helps us make friends and understand other cultures", ["it makes us forget our own", "it is useless", "only adults should learn"], "Try 'vanakkam', 'namaskar' or 'kem cho'."),
       ("What is a lungi or a dhoti?", "an unstitched cloth wrapped around the waist", ["a woollen coat", "a kind of shoe", "a hat"], "Unstitched clothes suit hot weather."),
       ("Which famous camel fair is held every year in Rajasthan?", "the Pushkar Fair", ["the Kumbh Mela", "the Hornbill Festival", "the Surajkund Mela"], "Camels are traded and decorated."),
       ("Which festival of Nagaland, held in December, shows the culture of its tribes?", "the Hornbill Festival", ["Onam", "Pongal", "Baisakhi"], "It is named after the hornbill bird."),
       ("Why do states of India have different scripts?", "their languages grew in different ways over history", ["scripts are random", "there is only one script", "scripts are new"], "Devanagari, Bengali and Tamil are scripts."),
       ("Which festival is celebrated at the end of Ramzan?", "Eid-ul-Fitr", ["Pongal", "Baisakhi", "Christmas"], "Sewai is a popular sweet."),
       ("Which national festival is celebrated on 26 January?", "Republic Day", ["Independence Day", "Gandhi Jayanti", "Children's Day"], "The Constitution came into force on this day in 1950."),
       ("Which festival is celebrated on 25 December?", "Christmas", ["Diwali", "Holi", "Onam"], "Stars and cribs decorate homes."),
       ("Which festival marks the birth of Guru Nanak?", "Guru Nanak Jayanti (Gurpurab)", ["Holi", "Onam", "Bihu"], "Langars serve free meals.")]


def UNITS5a():
    b = {k: once_maker(v) for k, v in [("w", WQ), ("rv", RVQ), ("fd", FDQ), ("sc", SCQ), ("vb", VBQ)]}
    wform = odd_one(WFORM, "Which of these is %s?", "Which of these is not %s?")
    wsrc = pairs(WSRC5, "What is %s?", "Which of these is %s?")
    fresh = pairs(FRESH, "Complete the sentence about life in fresh water: %s …", "Which water animal or plant %s?")
    riv = pairs(RIV, "Complete the sentence: %s …", "Which river %s?")
    rpart = pairs(RPART, "What is %s of a river?", "What do we call %s?")
    rharm = odd_one(RHARM, "Which of these is %s?", "Which of these is not %s?")
    defic = pairs(DEFIC, "What causes %s?", "Which problem can be caused by %s in the diet?")
    rich = pairs(RICH5, "Which nutrient are %s good sources of?", "Which of these are good sources of %s?")
    store = pairs(STORE, "What is the best way to store %s?", "Which food is best stored this way: %s?")
    snack = odd_one(SNACK, "Which of these is %s?", "Which of these is not %s?")
    safe = pairs(SAFE5, "What should you do if there is %s?", "When should you do this: %s?")
    kind = odd_one(KIND, "Which of these is %s?", "Which of these is not %s?")
    incl = pairs(INCL, "How does %s help?", "Which of these helps %s?")
    team = pairs(TEAM, "What does %s do at school?", "Who at school is responsible for %s?")
    dance = pairs(DANCE, "Which state is the dance %s from?", "Which dance belongs to %s?")
    art = pairs(ART, "Which state is %s from?", "Which art or craft belongs to %s?")
    dish = pairs(DISH, "Which state is %s a famous dish of?", "Which dish is a famous food of %s?")
    harv = pairs(HARV, "Where is the harvest festival %s celebrated?", "Which harvest festival is celebrated in %s?")
    return [
        U(1, "water-the-essence-of-life", 1, LA,
          "Forms of water (solid, liquid and gas) and how water changes form; sources of water such as rain, rivers, glaciers, lakes and groundwater; how flowing water shapes the land; life in fresh water; why water is precious and ways to save it (summary of NCERT Our Wondrous World Chapter 1).",
          "Water: The Essence of Life", "water: the essence of life",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 1: forms and sources of water, evaporation and condensation, life in fresh water, rainwater harvesting and saving water. 100 questions with answers.",
          "No living thing can live without water.", "Only a little of Earth's water is fresh.",
          "<p>About three-fourths of Earth is covered with water, but most is salty sea water; fresh water is stored in glaciers, rivers, lakes and under the ground. Water exists as solid ice, liquid water and invisible water vapour. Heating makes it evaporate, cooling makes vapour condense into drops and freezing turns it into ice.</p>"
          "<p>Flowing water cuts valleys and carries soil. Fish, frogs, lotuses and ducks are adapted to life in fresh water. Because fresh water is limited, we save it: fix leaks, use buckets instead of showers, harvest rainwater and keep ponds clean.</p>",
          [("Drops on a cold glass come from…", ["vapour in the air cools"], "condensation"), ("A tap wastes 8 L a day. In 7 days?", ["8 × 7"], "56 litres")],
          ["Thinking water vapour is the white steam you can see.", "Thinking most of Earth's water can be drunk.", "Thinking groundwater never runs out."],
          [("Why is fresh water precious?", "Very little of Earth's water is fresh and easy to use; most is salty or frozen."),
           ("What is rainwater harvesting?", "Collecting rainwater from roofs and land and storing it or letting it soak into the ground for later use.")],
          lambda: [("Forms of water", [(wform, 14), (b["w"], 6)]), ("Sources of water", [(wsrc, 14), (b["w"], 6)]), ("Water shapes the land", [(b["w"], 10), (wform, 10)]),
                   ("Life in fresh water", [(fresh, 12), (b["w"], 2), (wsrc, 2), (wform, 2), (c_water5, 2)]), ("Saving water", [(c_water5, 20)])]),
        U(2, "journey-of-a-river", 2, LA,
          "The journey of a river from its source in the mountains to its mouth at the sea; parts of a river; important rivers of India; how rivers support plants, animals, people and culture; how human activities pollute rivers and ways to protect them (summary of NCERT Our Wondrous World Chapter 2).",
          "Journey of a River", "journey of a river",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 2: a river's journey, parts of a river, rivers of India, dams, deltas, river life and keeping rivers clean. 100 questions with answers.",
          "A river flows from the mountains to the sea.", "Rivers give us water, food, soil and travel.",
          "<p>A river begins at its source, a glacier or spring in the mountains. It rushes down steep valleys, slows and bends (meanders) across the flat plains, is joined by tributaries and finally meets the sea at its mouth, often building a delta. The Ganga begins at Gangotri and reaches the Bay of Bengal through the Sundarbans delta.</p>"
          "<p>Rivers give water, fish, fertile soil and transport, so cities grew along them. Garbage, factory waste and sewage pollute rivers and harm animals such as the Ganges river dolphin. Planting trees on banks and treating waste water keep rivers healthy.</p>",
          [("A smaller river joining a bigger one is…", ["the Yamuna joins the Ganga"], "a tributary"), ("Where a river meets the sea is…", ["end of the journey"], "its mouth")],
          ["Thinking a river's source is at the sea.", "Mixing up a delta and a tributary.", "Thinking rivers can clean any amount of waste."],
          [("What is a delta?", "A fan-shaped area of new land made of soil deposited where a river meets the sea."),
           ("Why are river plains good for farming?", "Rivers spread fertile silt over the land during floods.")],
          lambda: [("A river's journey", [(c_river, 6), (b["rv"], 14)]), ("Parts of a river", [(rpart, 18), (b["rv"], 2)]), ("Rivers of India", [(riv, 16), (b["rv"], 4)]),
                   ("Rivers and people", [(b["rv"], 12), (rharm, 8)]), ("Keeping rivers clean", [(rharm, 14), (riv, 4), (rpart, 2)])]),
        U(3, "the-mystery-of-food", 3, HW,
          "Nutrients and the foods that give them; deficiency diseases; balanced diet and healthy eating habits; how food changes (fermentation, digestion starting in the mouth, starch test); why food spoils and how to preserve and store it (summary of NCERT Our Wondrous World Chapter 3).",
          "The Mystery of Food", "the mystery of food",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 3: nutrients and their sources, deficiency diseases, balanced diet, healthy snacks, fermentation and food storage. 100 questions with answers.",
          "A balanced diet keeps the body healthy.", "Too little of a nutrient can cause disease.",
          "<p>Each nutrient has a job: carbohydrates and fats give energy, proteins build the body, and vitamins and minerals keep us healthy. Too little of one can cause a deficiency disease: night blindness (vitamin A), scurvy (vitamin C), rickets (vitamin D), anaemia (iron) and goitre (iodine). A balanced diet with millets, pulses, vegetables, fruits and milk prevents them.</p>"
          "<p>Food changes in interesting ways: helpful bacteria turn milk into curd, batter rises by fermentation and saliva starts digesting starch in the mouth. Germs and moulds spoil food, so we store it cool, dry and covered.</p>",
          [("Bleeding gums come from too little…", ["amla, oranges"], "vitamin C"), ("Milk becomes curd because…", ["a little curd is added"], "helpful bacteria change it")],
          ["Thinking all bacteria are harmful.", "Thinking a full stomach means a balanced diet.", "Storing onions and potatoes in damp places."],
          [("What is a deficiency disease?", "A disease caused when the diet has too little of a nutrient, such as scurvy from too little vitamin C."),
           ("Why does food spoil?", "Germs and moulds grow on it, especially when it is warm and moist.")],
          lambda: [("Nutrients and their sources", [(rich, 12), (b["fd"], 8)]), ("Deficiency diseases", [(defic, 8), (rich, 4), (b["fd"], 8)]), ("Healthy eating", [(snack, 14), (b["fd"], 6)]),
                   ("How food changes", [(b["fd"], 8), (store, 12)]), ("Storing food", [(store, 4), (snack, 16)])]),
        U(4, "our-school-a-happy-place", 4, HW,
          "Making school a happy place: rules, teamwork and respect; kind and unsafe behaviour; dealing with feelings and bullying; inclusion of children with disabilities; people who help at school; safety drills for fire and earthquakes (summary of NCERT Our Wondrous World Chapter 4).",
          "Our School: A Happy Place", "our school: a happy place",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 4: school rules, teamwork, kindness, inclusion, people who help at school, bullying and safety drills. 100 questions with answers.",
          "A happy school is safe, fair and kind.", "Rules, teamwork and respect help everyone learn.",
          "<p>A school is happy when everyone feels safe, welcome and respected. Rules help us learn together; teamwork helps us finish a class garden or a play; kindness means sharing, waiting for our turn and including everyone. Bullying is never acceptable: tell a trusted adult.</p>"
          "<p>Inclusion means every child can take part: ramps for wheelchairs, braille and large-print books, and sign language. Many people help at school: the librarian, nurse, cook and guard. In a fire drill we walk out calmly in a line; in an earthquake we drop, cover and hold on.</p>",
          [("During an earthquake…", ["under a strong table"], "drop, cover and hold on"), ("Braille helps…", ["reading by touch"], "people who cannot see")],
          ["Running and pushing during a fire drill.", "Keeping quiet about bullying.", "Thinking rules are only for some students."],
          [("What does inclusion mean at school?", "Making sure every child, including children with disabilities, can take part and feels welcome."),
           ("What should you do in an earthquake?", "Drop to the floor, cover your head under a strong table and hold on until the shaking stops.")],
          lambda: [("Rules and teamwork", [(b["sc"], 12), (kind, 8)]), ("Kindness at school", [(kind, 14), (b["sc"], 6)]), ("Everyone belongs", [(incl, 12), (b["sc"], 8)]),
                   ("People who help us", [(team, 14), (safe, 6)]), ("Staying safe", [(safe, 10), (kind, 2), (team, 2), (incl, 2), (b["sc"], 4)])]),
        U(5, "our-vibrant-country", 5, II,
          "The cultural diversity of India: languages, foods, clothes, festivals, dances, music and folk arts of different states; how customs change over time; unity in diversity (summary of NCERT Our Wondrous World Chapter 5).",
          "Our Vibrant Country", "our vibrant country",
          "Free CBSE Class 5 EVS worksheets for NCERT Our Wondrous World Chapter 5: dances, folk arts, foods, clothes, languages and harvest festivals of the states of India, and unity in diversity. 100 questions with answers.",
          "India is one country with many cultures.", "Each state has its own dances, food and arts.",
          "<p>India has 22 scheduled languages and many more spoken ones. Each region has its own food, clothes, festivals and arts, shaped by its weather and history. Bhangra is from Punjab, Garba from Gujarat and Bihu from Assam; Madhubani paintings come from Bihar and Warli art from Maharashtra; dhokla is a dish of Gujarat and puttu of Kerala.</p>"
          "<p>Harvest festivals such as Pongal, Onam, Bihu and Baisakhi celebrate the crops. Customs change over time, for example eco-friendly clay idols and colours. Sharing each other's festivals and learning each other's languages keeps us united in diversity.</p>",
          [("Garba is a dance of…", ["Navratri"], "Gujarat"), ("Madhubani painting comes from…", ["Mithila region"], "Bihar")],
          ["Thinking all Indians eat the same food.", "Mixing up Bihu (Assam) and Baisakhi (Punjab).", "Thinking traditions never change."],
          [("What does unity in diversity mean?", "People of many languages, religions and customs living together peacefully as one nation."),
           ("Why do clothes and food differ across India?", "Different regions have different weather, crops and traditions.")],
          lambda: [("Languages and clothes", [(b["vb"], 14), (dish, 6)]), ("Dances and music", [(dance, 16), (b["vb"], 4)]), ("Folk arts and crafts", [(art, 15), (b["vb"], 5)]),
                   ("Food of the states", [(dish, 14), (harv, 6)]), ("Festivals and unity", [(dance, 9), (art, 6), (harv, 4), (b["vb"], 1)])]),
    ]
