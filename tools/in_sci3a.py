# -*- coding: utf-8 -*-
"""Class 3 EVS (NCERT Our Wondrous World, chapters 1–6): question makers and UNITS3a()."""
from uk_alsci import tq, nf, once_maker
from in_sci import pairs, _R, U, K
from in_sci6a import odd_one, nq, _cap
import in_sci

FC, LA, WA, FH, TA = "Our Families and Communities", "Life Around Us", "Water", "Food and Health", "Things Around Us"


def kid():
    return _R[0].choice(in_sci.GIRLS + in_sci.BOYS)


# =================================================================== Chapter 1: family and friends
REL = [("your father's father", "grandfather"), ("your mother's mother", "grandmother"), ("your father's mother", "grandmother"), ("your mother's father", "grandfather"),
       ("your father's brother", "uncle"), ("your mother's brother", "uncle"), ("your father's sister", "aunt"), ("your mother's sister", "aunt"),
       ("your uncle's son", "cousin"), ("your aunt's daughter", "cousin"), ("your brother's son", "nephew"), ("your sister's daughter", "niece"),
       ("your sister's son", "nephew"), ("your brother's daughter", "niece"), ("your parents' son", "brother"), ("your parents' daughter", "sister"),
       ("your father's brother's wife", "aunt"), ("your mother's sister's husband", "uncle"), ("your mother's brother's son", "cousin"), ("your father's sister's daughter", "cousin"),
       ("your grandmother's daughter who is not your mother", "aunt"), ("your grandfather's son who is not your father", "uncle"), ("your father's father's wife", "grandmother"), ("your mother's mother's husband", "grandfather")]
FAM = {"a joint family": ["grandparents, parents, uncles, aunts and cousins living together", "three generations sharing one house and one kitchen", "a family where cousins grow up in the same house"],
       "a nuclear family": ["parents and their children living together", "a mother, a father and their two children in one home", "a small family of parents and one child"]}
HELP = {"a helpful thing to do at home": ["watering the plants", "setting the plates for dinner", "folding the washed clothes", "keeping your toys back in place", "feeding the pet",
                                         "helping grandparents find their spectacles", "making your own bed", "sweeping your room", "carrying the groceries", "switching off the fan when you leave"],
        "an unhelpful thing to do at home": ["leaving the tap running", "throwing clothes on the floor", "wasting food", "shouting at others", "leaving lights on in an empty room",
                                             "breaking things in anger", "leaving muddy shoes on the bed", "spilling water and walking away", "hiding the TV remote", "keeping the fridge door open"]}
F1 = [("What is a family tree?", "a drawing that shows the members of a family and how they are related", ["a tree planted by a family", "a list of friends", "a map of the town"], "Grandparents are usually at the top."),
      ("Who are our elders?", "people older than us, such as grandparents and parents", ["only our friends", "only babies", "only teachers"], "We should respect our elders."),
      ("What makes someone a good friend?", "they are kind, share, help and listen", ["they are always unkind", "they never share", "they make fun of others"], "Friends help each other."),
      ("What should you do if your friend is sad?", "listen to them and try to help", ["laugh at them", "ignore them", "tell everyone"], "Kind words help."),
      ("Why do families share work at home?", "so that no one person gets too tired and all the work is done", ["so that work is never done", "to make the house dirty", "because only one person can work"], "Everyone can help."),
      ("How can we show respect to our grandparents?", "by spending time with them, listening and helping them", ["by ignoring them", "by being rude", "by not talking to them"], "They have many stories to share."),
      ("What do we learn from our grandparents?", "stories, games, songs and family traditions", ["nothing at all", "only how to shout", "only about phones"], "They pass on traditions."),
      ("What can families do together for fun?", "play games, cook, visit places and celebrate festivals", ["only fight", "never talk", "only watch phones alone"], "Time together builds bonds."),
      ("What is a pet?", "an animal that lives with a family and is cared for", ["a wild animal", "a toy", "a plant"], "Dogs, cats and parrots can be pets."),
      ("How should we care for a pet?", "give it food, water, a clean place and love", ["keep it hungry", "tease it", "leave it alone in the sun"], "Pets also need a doctor sometimes."),
      ("Why do family members look alike in some ways?", "children get some features from their parents", ["they buy the same clothes", "they eat the same food", "it is magic"], "Eye colour and hair can be similar."),
      ("What is a neighbour?", "a person who lives near our home", ["a person in another country", "a pet", "a teacher only"], "Good neighbours help each other."),
      ("How can friends solve a quarrel?", "talk calmly, listen and say sorry if needed", ["stop talking forever", "hit each other", "shout louder"], "Saying sorry is brave."),
      ("Why should we include a new child in our games?", "it helps them feel welcome and happy", ["new children should play alone", "games are only for old friends", "it makes the game worse"], "Everyone likes to belong."),
      ("What should you do if a stranger offers you sweets and asks you to come with them?", "say no, move away and tell a trusted adult", ["go with them", "take the sweets", "keep it a secret"], "Never go with strangers."),
      ("Which number should a child know by heart for safety?", "a parent's phone number", ["a shop's price list", "a friend's shoe size", "the page number of a book"], "It helps if the child gets lost."),
      ("Why are some families big and some small?", "families have different numbers of members", ["all families are the same", "small families are wrong", "big families are wrong"], "Every family is special."),
      ("How do people in a family care for a baby?", "they feed, bathe and play with the baby and keep it safe", ["they leave the baby alone", "they give it hard food", "they keep it awake"], "Babies need lots of care."),
      ("What is a tradition?", "a custom passed down in a family or community", ["a new game", "a type of food only", "a school subject"], "Lighting lamps on Diwali is a tradition."),
      ("What can you share with a friend?", "toys, books, ideas and a snack", ["only quarrels", "nothing", "only secrets that hurt others"], "Sharing makes friendships strong."),
      ("What is an extended family?", "a family that includes grandparents, uncles, aunts and cousins", ["only parents and children", "only friends", "only pets"], "They may live together or nearby."),
      ("Why do children sometimes look after younger brothers and sisters?", "to help the family and show care", ["to boss them", "to make them cry", "because adults never help"], "Older children can help in small ways."),
      ("What does 'generation' mean in a family?", "people born around the same time, such as grandparents, parents or children", ["a kind of food", "a family pet", "a family house"], "A family tree shows generations."),
      ("Why do family members celebrate birthdays together?", "to show love and share happiness", ["to fight", "to stop working", "to waste food"], "Each family celebrates in its own way."),
      ("Which of these is a good way to make a new friend?", "say hello, smile and invite them to play", ["ignore them", "make fun of them", "push them"], "Be friendly."),
      ("What should you do if you break something by mistake at home?", "tell an adult honestly and say sorry", ["hide it", "blame a sibling", "throw it away secretly"], "Honesty builds trust."),
      ("Why do families keep old photographs?", "to remember people and special times", ["to sell them", "to throw away later", "to make paper"], "Albums tell family stories."),
      ("Who can help a child if there is a problem at school?", "a parent, a teacher or another trusted adult", ["a stranger online", "nobody", "only a younger child"], "Talk to someone you trust."),
      ("What is a cousin?", "the child of your uncle or aunt", ["your father's father", "your sister's child", "your friend's pet"], "Cousins are part of your family."),
      ("Why is it good to help elders cross the road?", "it keeps them safe and shows care", ["it is a rule only in school", "elders do not need help", "it wastes time"], "Hold their hand.")]

# =================================================================== Chapter 2: going to the mela
MELA = [("a potter", "clay pots and toys"), ("a bangle seller", "colourful glass bangles"), ("a balloon seller", "balloons"), ("a weaver", "woven cloth and mats"),
        ("a toy maker", "wooden and clay toys"), ("a sweet seller", "jalebis and laddoos"), ("a puppeteer", "puppet shows"), ("a basket maker", "bamboo baskets"),
        ("a garland maker", "flower garlands"), ("a juice seller", "fresh sugarcane juice"),
        ("a kite seller", "paper kites"), ("a mehendi artist", "henna designs on hands"), ("a cobbler", "repaired shoes and new chappals"), ("a blacksmith", "iron tools such as sickles")]
COINS = [1, 2, 5, 10, 20]


def c_money(k=None):
    R = _R[0]
    k = k or R.choice(["left", "total", "coins"])
    item = R.choice(["a balloon", "a clay toy", "a set of bangles", "a jalebi plate", "a paper windmill", "a puppet", "a bamboo flute", "a glass of sugarcane juice", "a ride on the giant wheel"])
    n = kid()
    if k == "left":
        have = R.choice([20, 30, 40, 50, 60, 100])
        c = R.choice([x for x in [5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 45] if x < have])
        return _money("%s has ₹%d at the mela and buys %s for ₹%d. How much money is left?" % (n, have, item, c), have - c, [have + c, c, have, have - c + 10],
                      "₹%d − ₹%d = ₹%d." % (have, c, have - c))
    if k == "total":
        a, b_ = R.choice([5, 10, 12, 15, 20, 25]), R.choice([5, 8, 10, 15, 20, 30])
        item2 = R.choice(["a kite", "a balloon", "a pinwheel", "some peanuts", "a whistle"])
        return _money("At the mela, %s buys %s for ₹%d and %s for ₹%d. How much does %s spend in all?" % (n, item, a, item2, b_, n), a + b_, [abs(a - b_), a * 2, b_ * 2, a + b_ + 5], "₹%d + ₹%d = ₹%d." % (a, b_, a + b_))
    c1, c2 = R.sample(COINS, 2)
    m1, m2 = R.choice([1, 2, 3]), R.choice([1, 2, 3, 4])
    tot = c1 * m1 + c2 * m2
    return _money("%s pays with %d coin%s of ₹%d and %d coin%s of ₹%d. How much money is that?" % (n, m1, "" if m1 == 1 else "s", c1, m2, "" if m2 == 1 else "s", c2), tot,
                  [c1 + c2, m1 + m2, c1 * m2 + c2 * m1, tot + 1], "%d × ₹%d + %d × ₹%d = ₹%d." % (m1, c1, m2, c2, tot))


def _money(q, val, wrongs, e):
    from sci_common import item
    ws = []
    for w in wrongs:
        if w > 0 and w != val and "₹%d" % w not in ws:
            ws.append("₹%d" % w)
    if len(ws) < 3:
        return None
    return item(q, "₹%d" % val, ws[:3], e)


MELAQ = [("What is a mela?", "a fair where people gather to buy, sell, play and celebrate", ["a kind of school", "a hospital", "a river"], "Melas are held at festivals and harvest time."),
         ("Why should children hold an adult's hand in a crowded mela?", "so they do not get lost", ["to walk slower", "to buy more things", "to stop the music"], "Remember a parent's phone number too."),
         ("What should a child do if lost at a mela?", "stay in one place and ask a police officer or the help desk for help", ["run around crying", "go home alone", "go with a stranger"], "Announcements can find parents."),
         ("Which ride at a mela goes round and round in a big circle up high?", "the giant wheel", ["the see-saw", "the slide", "the swing"], "It turns on a big axle."),
         ("Why do people bargain at a mela?", "to agree on a fair price with the seller", ["to fight with the seller", "to steal things", "to waste time"], "Bargaining is common at local markets."),
         ("What is a puppet show?", "a show in which dolls are moved by strings or hands to tell a story", ["a cooking show", "a cricket match", "a music class"], "Kathputli is a puppet tradition of Rajasthan."),
         ("Which famous mela is held at Pushkar in Rajasthan?", "a camel fair", ["a fish fair", "a snow fair", "a boat race"], "It happens in October or November."),
         ("Which huge gathering is held at Prayagraj where rivers meet?", "the Kumbh Mela", ["the Pushkar camel fair", "the Hornbill festival", "the Surajkund fair"], "It is one of the largest gatherings in the world."),
         ("Which crafts fair is held every year at Surajkund in Haryana?", "the Surajkund International Crafts Mela", ["the Kumbh Mela", "the Pushkar fair", "the Goa carnival"], "Artisans from many states come there."),
         ("What do we use to pay for things at a mela?", "money: coins and notes", ["leaves", "stones", "sand"], "We can also pay by UPI on a phone."),
         ("Why are melas good for artisans?", "they can sell their handmade goods to many people", ["they cannot sell anything", "they must give things free", "they are not allowed"], "Melas keep crafts alive."),
         ("How do people usually reach a village mela?", "on foot, by bus, by bullock cart or by tractor", ["only by aeroplane", "only by ship", "only by train"], "It depends on the place."),
         ("Why should we not throw litter at a mela?", "it makes the place dirty and can harm animals", ["litter helps the mela", "it is fun", "it makes the mela bigger"], "Use dustbins."),
         ("Which of these sounds might you hear at a mela?", "drums, music and people calling out prices", ["complete silence", "only the sea", "only an aeroplane"], "Melas are lively places."),
         ("What do sellers use to weigh sweets at a mela?", "a weighing scale", ["a thermometer", "a ruler", "a clock"], "They sell sweets by weight."),
         ("What does a potter use to shape pots?", "a potter's wheel", ["a loom", "a sewing machine", "a hammer only"], "The clay is spun and shaped by hand."),
         ("Why do melas often happen at harvest time?", "farmers have new crops and time to celebrate", ["it is the coldest time", "schools are open", "there are no crops"], "People buy and sell new goods."),
         ("Which coin is the smallest value used today in India?", "₹1", ["₹20", "₹10", "₹5"], "There are ₹1, ₹2, ₹5, ₹10 and ₹20 coins."),
         ("Which note is worth more: ₹50 or ₹20?", "₹50", ["₹20", "both are the same", "it cannot be told"], "Fifty is more than twenty."),
         ("What is the giant wheel's big round frame turned by?", "a motor or by people pushing", ["the wind only", "water in a river", "a horse sitting on it"], "Old village wheels were turned by hand."),
         ("Why do potters bake clay toys in a kiln?", "heating makes the clay hard and strong", ["to make them soft", "to colour them only", "to make them melt"], "Unbaked clay breaks easily."),
         ("Which famous fair in Bihar is known for its animal market?", "the Sonepur Mela", ["the Kumbh Mela", "the Surajkund Mela", "the Hornbill Festival"], "It is held near the river Gandak."),
         ("Why should we buy handmade things from artisans?", "it supports their skills and families", ["handmade things are useless", "it harms the artisans", "it is not allowed"], "Crafts are part of our heritage."),
         ("What should you carry to a mela on a hot day?", "a water bottle and a cap", ["a heavy blanket", "a torch only", "a winter coat"], "Drink water often.")]
MSAFE = {"a safe thing to do at a mela": ["holding an adult's hand in the crowd", "remembering a parent's phone number", "meeting at a fixed spot if separated", "drinking water from a clean source",
                                          "waiting your turn for a ride", "keeping money in a safe pocket"],
         "an unsafe thing to do at a mela": ["wandering off alone", "going with a stranger", "pushing in the crowd", "standing up on a moving ride", "eating uncovered food with flies on it", "climbing on stalls"]}

# =================================================================== Chapter 3: celebrating festivals
FEST = [("Pongal", "Tamil Nadu"), ("Onam", "Kerala"), ("Bihu", "Assam"), ("Baisakhi", "Punjab"), ("Durga Puja", "West Bengal"), ("Ganesh Chaturthi", "Maharashtra"),
        ("Hornbill Festival", "Nagaland"), ("Losar", "Ladakh and Sikkim"), ("Chhath Puja", "Bihar"), ("Ugadi", "Karnataka, Andhra Pradesh and Telangana"), ("Garba nights of Navratri", "Gujarat"), ("Lohri", "Punjab and Haryana")]
NATF = [("Independence Day", "15 August"), ("Republic Day", "26 January"), ("Gandhi Jayanti", "2 October"), ("Children's Day", "14 November"), ("Teachers' Day", "5 September"), ("National Science Day", "28 February"),
        ("Ambedkar Jayanti", "14 April"), ("World Environment Day", "5 June"), ("International Day of Yoga", "21 June"), ("Earth Day", "22 April"), ("World Water Day", "22 March")]
FFOOD = [("Pongal", "sweet pongal made from new rice, milk and jaggery"), ("Onam", "a sadya feast served on a banana leaf"), ("Eid-ul-Fitr", "sweet sevaiyan"),
         ("Christmas", "plum cake"), ("Holi", "gujiya"), ("Makar Sankranti", "til and jaggery laddoos"), ("Bihu", "pitha made of rice"), ("Lohri", "rewari, peanuts and popcorn"),
         ("Ganesh Chaturthi", "modak"), ("Durga Puja", "bhog of khichuri")]
FKIND = {"a harvest festival": ["Pongal", "Onam", "Bihu", "Baisakhi", "Lohri", "Makar Sankranti"], "a national festival": ["Independence Day", "Republic Day", "Gandhi Jayanti"],
         "a festival of lights": ["Diwali", "Dev Deepawali", "Karthigai Deepam"]}
FQ = [("Why do people celebrate festivals?", "to share joy, give thanks and keep traditions alive", ["to stop working forever", "to fight", "to stay alone"], "Festivals bring people together."),
      ("Why is Independence Day celebrated on 15 August?", "India became free from British rule on 15 August 1947", ["it is a harvest day", "it is the first day of the year", "it is a winter festival"], "The Prime Minister hoists the flag at the Red Fort."),
      ("Why is Republic Day celebrated on 26 January?", "India's Constitution came into force on 26 January 1950", ["India became free on that day", "it is Gandhiji's birthday", "it is a harvest day"], "There is a grand parade in New Delhi."),
      ("Whose birthday is celebrated as Gandhi Jayanti?", "Mahatma Gandhi's", ["Jawaharlal Nehru's", "Rabindranath Tagore's", "Subhas Chandra Bose's"], "He is called the Father of the Nation."),
      ("Whose birthday is celebrated as Children's Day?", "Jawaharlal Nehru's", ["Mahatma Gandhi's", "Dr A. P. J. Abdul Kalam's", "Bhagat Singh's"], "He loved children."),
      ("Whose birthday is celebrated as Teachers' Day?", "Dr Sarvepalli Radhakrishnan's", ["Mahatma Gandhi's", "Jawaharlal Nehru's", "C. V. Raman's"], "He was a great teacher and President of India."),
      ("Which colours are in the Indian national flag?", "saffron, white and green, with a navy blue chakra", ["red, white and blue", "black and yellow", "only green"], "The chakra has 24 spokes."),
      ("What are rangolis?", "colourful designs drawn on the floor for festivals", ["a kind of sweet", "a song", "a dance"], "They are called kolam in Tamil Nadu."),
      ("Why are harvest festivals celebrated?", "to give thanks for a good crop", ["to start a new school year", "to mark the coldest day", "to honour the sea only"], "Pongal and Baisakhi are harvest festivals."),
      ("What is cooked during Pongal?", "a sweet dish of new rice, milk and jaggery called pongal", ["only cake", "only noodles", "only fish fry"], "The pot is allowed to boil over for good luck."),
      ("Which boat race is famous during Onam in Kerala?", "the snake boat race (Vallam Kali)", ["a camel race", "a car race", "a horse race"], "Long boats with many rowers race on rivers."),
      ("How do people celebrate festivals together in a community?", "by decorating, sharing food, singing and visiting friends", ["by staying alone", "by breaking things", "by wasting water"], "Festivals are for everyone."),
      ("Why should we celebrate festivals without harming the environment?", "loud crackers and plastic decorations pollute air and land", ["crackers clean the air", "plastic is good for soil", "nature does not matter"], "Use clay lamps and natural colours."),
      ("Which festival marks the start of the new year in many parts of India in spring?", "Ugadi or Gudi Padwa", ["Christmas", "Independence Day", "Teachers' Day"], "Different regions call it by different names."),
      ("Which festival is celebrated with colours in spring?", "Holi", ["Diwali", "Onam", "Pongal"], "People throw coloured powder (gulal)."),
      ("Which festival is celebrated on the birthday of Guru Nanak Dev?", "Guru Nanak Jayanti (Gurpurab)", ["Diwali", "Bihu", "Onam"], "Langar meals are served to all."),
      ("Which festival celebrates the birth of Jesus Christ?", "Christmas", ["Eid", "Holi", "Baisakhi"], "It is on 25 December."),
      ("Which festival comes at the end of the month of Ramzan?", "Eid-ul-Fitr", ["Christmas", "Holi", "Pongal"], "People share sweet sevaiyan."),
      ("Which festival is the birthday of Lord Mahavira?", "Mahavir Jayanti", ["Buddha Purnima", "Guru Purab", "Christmas"], "It is celebrated by Jains."),
      ("Which festival celebrates the birth, enlightenment and death of Gautama Buddha?", "Buddha Purnima", ["Mahavir Jayanti", "Holi", "Onam"], "It falls on a full moon."),
      ("Which festival of lights is celebrated with diyas and rangoli?", "Diwali", ["Holi", "Bihu", "Christmas"], "Lamps are lit to celebrate the victory of good over evil."),
      ("Which festival involves flying kites in Gujarat in January?", "Uttarayan (Makar Sankranti)", ["Onam", "Christmas", "Durga Puja"], "The sky fills with colourful kites."),
      ("What is a 'pookalam'?", "a flower rangoli made during Onam", ["a sweet dish", "a boat", "a dance"], "It is made at the doorstep."),
      ("Which festival is celebrated by brothers and sisters with a rakhi?", "Raksha Bandhan", ["Holi", "Onam", "Pongal"], "Sisters tie a thread on their brothers' wrists."),
      ("What do people do at Republic Day celebrations at school?", "hoist the flag and sing the national anthem", ["fly kites only", "light crackers only", "play Holi"], "There is a big parade in New Delhi."),
      ("Who wrote the national anthem 'Jana Gana Mana'?", "Rabindranath Tagore", ["Mahatma Gandhi", "Jawaharlal Nehru", "Bankim Chandra Chatterjee"], "Bankim Chandra wrote 'Vande Mataram'."),
      ("Why do we use clay diyas instead of plastic lights?", "clay is natural and does not pollute", ["clay lamps cost more", "plastic is better for nature", "clay lamps do not glow"], "Clay lamps also help potters."),
      ("What do people often wear on festivals?", "new or traditional clothes", ["only raincoats", "only school uniforms", "nothing special ever"], "Different regions have different dresses.")]

# =================================================================== Chapter 4: getting to know plants
PARTS = [("the root", "holding the plant in the soil and taking in water"), ("the stem", "holding the plant up and carrying water to the leaves"),
         ("the leaf", "making food for the plant using sunlight"), ("the flower", "making seeds and fruits"), ("the fruit", "protecting the seeds inside"),
         ("the seed", "growing into a new plant")]
EAT = [("a carrot", "root"), ("a radish", "root"), ("a beetroot", "root"), ("a potato", "stem"), ("sugarcane", "stem"), ("ginger", "stem"),
       ("spinach", "leaf"), ("cabbage", "leaf"), ("coriander leaves", "leaf"), ("cauliflower", "flower"), ("broccoli", "flower"), ("a mango", "fruit"),
       ("a tomato", "fruit"), ("a banana", "fruit"), ("peas", "seed"), ("rice", "seed"), ("wheat", "seed"), ("groundnuts", "seed"),
       ("a sweet potato", "root"), ("a turnip", "root"), ("lettuce", "leaf"), ("fenugreek (methi) leaves", "leaf"), ("a guava", "fruit"), ("a brinjal", "fruit"), ("lentils (dal)", "seed"), ("an onion bulb", "stem")]
PUSE = [("neem", "twigs used to clean teeth and leaves used as medicine"), ("tulsi", "leaves used as a home medicine"), ("cotton", "fibres used to make cloth"), ("jute", "fibres used to make sacks and ropes"),
        ("bamboo", "making baskets, mats and furniture"), ("the rubber tree", "a milky juice used to make rubber"), ("sugarcane", "making sugar and jaggery"), ("the coconut palm", "oil, food and coir ropes"),
        ("the tea plant", "leaves for making tea"), ("mustard", "oil for cooking"), ("teak", "strong wood for furniture and doors")]


def c_eat(k=None):
    R = _R[0]
    f, p = R.choice(EAT)
    return tq("Which part of the plant do we eat when we eat %s?" % f, p, R.sample([x for x in ["root", "stem", "leaf", "flower", "fruit", "seed"] if x != p], 3),
              "%s is the %s of the plant." % (_cap(f), p))


PSIZE = {"a tree": ["mango", "neem", "banyan", "peepal", "coconut palm", "jamun", "tamarind"], "a shrub": ["rose", "hibiscus", "tulsi", "jasmine", "lemon", "henna"],
         "a herb": ["grass", "mint", "coriander", "wheat", "spinach", "tomato"], "a climber": ["money plant", "grapevine", "bitter gourd", "bean plant", "pea plant"]}
PLQ = [("What do plants need to grow?", "sunlight, water, air and soil", ["only darkness", "only sweets", "only sand"], "They make their own food."),
       ("Why are leaves green?", "they have a green substance called chlorophyll", ["they are painted", "they are wet", "they eat green food"], "It helps them make food."),
       ("Which part of a plant is usually under the ground?", "the root", ["the flower", "the fruit", "the leaf"], "Some stems, like potato, also grow underground."),
       ("Why do some plants have thorns?", "to protect themselves from animals", ["to make food", "to drink water", "to attract bees"], "Roses and cactus have thorns."),
       ("Why do bees visit flowers?", "to collect nectar and pollen", ["to sleep", "to eat leaves", "to drink water"], "They help flowers make seeds."),
       ("What grows from a seed?", "a new plant", ["a stone", "an animal", "a cloud"], "Seeds need water and warmth to sprout."),
       ("What is a seedling?", "a young plant that has just grown from a seed", ["an old tree", "a dry leaf", "a flower"], "It has tiny leaves."),
       ("Why should we not pluck flowers and leaves without need?", "it harms the plant", ["it helps the plant grow", "plants like it", "flowers grow back at once"], "Let flowers become fruits."),
       ("How do we know a tree's age?", "by counting the rings in a cut trunk", ["by its colour", "by counting its leaves", "by its smell"], "Each ring is about one year."),
       ("What do we get from trees?", "fruits, wood, shade, medicines and oxygen", ["plastic", "metal", "petrol"], "Trees are very useful."),
       ("Which plant gives us cotton?", "the cotton plant", ["the mango tree", "the rose plant", "the neem tree"], "Cotton is used to make cloth."),
       ("Why do we water plants?", "plants need water to live and grow", ["water makes plants sleep", "to wash the leaves only", "water makes plants smaller"], "Do not overwater them."),
       ("What happens to a plant kept in a dark room for many days?", "it becomes pale and weak", ["it grows greener", "it flowers more", "nothing happens"], "Plants need sunlight."),
       ("Which part of a plant smells nice and is often colourful?", "the flower", ["the root", "the stem", "the seed"], "Colour and smell attract insects."),
       ("Which tree is called the national tree of India?", "the banyan tree", ["the mango tree", "the neem tree", "the coconut palm"], "Its roots hang down from its branches."),
       ("How can you make a leaf print?", "paint the back of a leaf and press it on paper", ["burn the leaf", "boil the leaf", "freeze the leaf"], "You can see its veins clearly."),
       ("What are the lines on a leaf called?", "veins", ["roots", "seeds", "petals"], "They carry water and food."),
       ("Which plant part do we use as a spice in turmeric?", "the underground stem", ["the flower", "the leaf", "the fruit"], "Turmeric gives a yellow colour."),
       ("Why do plants need roots?", "to hold them in the soil and take in water", ["to make flowers", "to catch insects", "to make the plant colourful"], "Roots spread under the soil."),
       ("Which of these is a seed we can sprout at home?", "moong", ["a stone", "sugar", "salt"], "Keep it wet for a day or two."),
       ("Which plant has needle-shaped leaves and grows in cold mountains?", "the pine tree", ["the coconut palm", "the banana plant", "the lotus"], "Snow slides off its shape."),
       ("Which plant floats on water?", "the water hyacinth", ["the mango tree", "the cactus", "the neem tree"], "Its stems are spongy and full of air."),
       ("Why does a cactus have a thick stem?", "it stores water for dry times", ["it is very heavy", "it is hollow", "it is made of wood"], "It grows in deserts."),
       ("What is a bud?", "a young flower or leaf that has not opened yet", ["a seed", "a root", "a fruit"], "Buds open into flowers."),
       ("Which part of a plant becomes a fruit?", "the flower", ["the root", "the stem", "the leaf"], "Seeds form inside the fruit."),
       ("Which plant gives us both food and leaves used as plates in South India?", "the banana plant", ["the neem tree", "the cotton plant", "the rose plant"], "Banana leaves are used to serve food."),
       ("How can you tell a climber from a creeper?", "a climber grows up a support; a creeper spreads on the ground", ["they are the same", "a creeper is a tall tree", "a climber has no leaves"], "Money plant climbs; pumpkin creeps."),
       ("What do we call plants that grow by themselves where they are not wanted?", "weeds", ["crops", "seedlings", "fruits"], "Farmers remove weeds.")]

# =================================================================== Chapter 5: plants and animals live together
HOME = [("a bird", "a nest"), ("a rabbit", "a burrow"), ("a bee", "a hive"), ("a spider", "a web"), ("a lion", "a den"), ("a horse", "a stable"),
        ("a cow", "a cowshed"), ("a dog", "a kennel"), ("a hen", "a coop"), ("an ant", "an anthill"), ("a fish", "water in a pond or river"), ("a snake", "a hole or a pit")]
WHERE = {"an animal that lives mostly in trees": ["a monkey", "a squirrel", "a woodpecker", "a koel", "a parrot", "a tree frog"],
         "an animal that lives in water": ["a fish", "a crab", "a tortoise", "a dolphin", "an octopus"],
         "an animal that lives on the ground": ["a cow", "an elephant", "a rabbit", "a lion", "a goat", "an ant"]}
EATS = {"an animal that eats only plants": ["a cow", "a deer", "a rabbit", "a goat", "an elephant", "a horse"], "an animal that eats other animals": ["a lion", "a tiger", "a frog", "an eagle", "a snake", "a wolf"],
        "an animal that eats both plants and animals": ["a crow", "a bear", "a hen", "a dog", "a human", "a mynah"]}
PAQ = [("How do plants help animals?", "they give them food, shelter and oxygen", ["they hunt animals", "they make animals sick", "they take away their food"], "Birds nest in trees."),
       ("How do animals help plants?", "they carry pollen and spread seeds", ["they make plants dry", "they cut all plants", "they stop plants growing"], "Bees and birds are helpers."),
       ("Where do many birds build their nests?", "in trees", ["under water", "in the sky", "inside rocks only"], "They use twigs, grass and feathers."),
       ("Why do some birds come to our gardens?", "to find food, water and places to rest", ["to make noise only", "to break plants", "they are lost"], "Keep a bowl of water for them in summer."),
       ("How do squirrels help trees?", "they bury nuts that sometimes grow into new trees", ["they cut trees", "they eat roots", "they make trees dry"], "They forget some nuts."),
       ("Which animal helps flowers make seeds by carrying pollen?", "the bee", ["the cow", "the fish", "the snake"], "Butterflies help too."),
       ("Why do animals have homes?", "for safety, rest and raising their young", ["to look pretty", "to store money", "to watch TV"], "Homes protect them from weather."),
       ("What is a habitat?", "the natural home of a plant or animal", ["a zoo cage", "a toy house", "a market"], "A pond is the habitat of frogs."),
       ("Which animal lives in water but breathes air?", "a dolphin", ["a fish", "a crab", "an octopus"], "Dolphins come up to breathe."),
       ("What do earthworms do for the soil?", "make it loose and rich", ["make it hard", "make it dirty", "eat all the plants"], "They are friends of farmers."),
       ("Why do frogs live near ponds?", "they lay eggs in water and need moist skin", ["they hate water", "they live in deserts", "they cannot swim"], "Tadpoles live in water."),
       ("Why should we not cut down trees where birds live?", "the birds will lose their homes", ["birds like it", "birds live in the sky", "trees grow back at once"], "Plant more trees."),
       ("How does a camel survive in the desert?", "it can go many days without water and has long legs", ["it swims", "it lives in trees", "it eats only fish"], "It is called the ship of the desert."),
       ("Which animal makes its home by building a dam of sticks?", "a beaver", ["a cow", "a hen", "a dog"], "Beavers live in some cold countries."),
       ("Which insect lives in a big group and collects honey?", "the honeybee", ["the mosquito", "the housefly", "the cockroach"], "Many bees live in one hive."),
       ("What do animals that live in cold places have?", "thick fur or fat to keep warm", ["thin skin only", "no hair", "big ears to lose heat"], "Yaks have thick hair."),
       ("Why do some animals sleep in the day and move at night?", "they find food more safely in the dark", ["they are lazy", "they cannot see in the dark", "they do not eat"], "Owls and bats are active at night."),
       ("Which animal can live both on land and in water?", "a frog", ["a cat", "a parrot", "a cow"], "Turtles and crocodiles can too."),
       ("Why do woodpeckers peck at tree trunks?", "to find insects to eat and to make nest holes", ["to break the tree", "to drink water", "to sharpen their beaks only"], "They have strong beaks."),
       ("How do monkeys move from tree to tree?", "they swing and jump using their long arms, legs and tail", ["they fly", "they swim", "they dig tunnels"], "Their long arms help."),
       ("Why does a fish have fins?", "to swim and balance in water", ["to fly", "to dig", "to walk on land"], "Its tail pushes it forward."),
       ("What do tadpoles grow into?", "frogs", ["fish", "snakes", "birds"], "They lose their tails."),
       ("Which animals live in a group called a herd?", "elephants", ["spiders", "owls", "snakes"], "Cows and deer also live in herds."),
       ("Why do birds sit on their eggs?", "to keep them warm so they hatch", ["to break them", "to hide them from the Sun only", "to make them cold"], "Both parents take turns in some birds."),
       ("What does a tailorbird use to make its nest?", "leaves stitched together with plant fibres", ["mud only", "stones", "plastic"], "It is a clever builder."),
       ("Which animal makes a home by spinning silk threads?", "a spider", ["a cow", "a fish", "a lion"], "The web also catches food.")]

# =================================================================== Chapter 6: living in harmony
HARM3 = [("What does 'living in harmony' with nature mean?", "living kindly with plants, animals and people, without harming them", ["cutting all trees", "wasting water", "chasing animals"], "We all share the Earth."),
         ("What was the Chipko movement?", "villagers hugging trees to stop them being cut down", ["a dance festival", "a car race", "a cooking contest"], "It began in Uttarakhand in the 1970s."),
         ("Which community in Rajasthan is famous for protecting trees and animals such as the blackbuck?", "the Bishnois", ["the potters", "the fishermen of Goa", "the boatmen of Kerala"], "Amrita Devi gave her life to save khejri trees."),
         ("Why should we keep bird feeders and water bowls in summer?", "birds find it hard to get water when it is very hot", ["birds hate water", "to catch birds", "to keep birds away"], "Change the water every day."),
         ("Why should we not tease animals at a zoo?", "it scares and hurts them", ["they like it", "it makes them healthy", "it is a rule only for adults"], "Watch quietly."),
         ("How can we help street animals?", "give them water and be gentle with them", ["throw stones at them", "chase them away", "shout at them"], "Inform an animal shelter if they are hurt."),
         ("Why do farmers like owls and snakes near their fields?", "they eat rats that damage crops", ["they eat crops", "they water fields", "they make noise"], "Animals help each other."),
         ("Why are bees important for our food?", "they pollinate many fruits and vegetables", ["they eat crops", "they spoil fruits", "they make rain"], "Without bees we would have fewer fruits."),
         ("How can we save trees?", "plant new trees, use less paper and not cut trees without need", ["burn more wood", "waste paper", "cut trees for fun"], "Use both sides of paper."),
         ("Why should we not pick bird eggs from nests?", "the baby birds would not hatch", ["birds lay eggs for us", "eggs grow faster in our hands", "it is fun"], "Leave nests alone."),
         ("What is a sacred grove?", "a patch of forest protected by a village community", ["a city park", "a shop", "a factory"], "Many are found in Meghalaya and Kerala."),
         ("Why should we turn off music and fireworks near bird nesting places?", "loud noise frightens birds and animals", ["birds love loud noise", "it helps them sleep", "it makes them grow"], "Quiet helps wildlife."),
         ("What can we do with fruit peels to help the soil?", "put them in a compost pit", ["throw them on the road", "burn them", "put them in rivers"], "Compost feeds plants."),
         ("How do trees help people on a hot day?", "they give cool shade", ["they make it hotter", "they block all wind", "they make the ground wet"], "Trees also cool the air."),
         ("Why should we use dustbins?", "litter harms animals and makes places dirty", ["litter is good for soil", "dustbins are for decoration", "animals eat plastic safely"], "Cows can choke on plastic bags."),
         ("Why is it kind to leave a little space in our garden wild?", "insects, birds and small animals can live there", ["it looks bad", "it attracts thieves", "plants hate it"], "Gardens can be homes for wildlife."),
         ("Who was Amrita Devi Bishnoi?", "a brave woman who gave her life to save khejri trees", ["a famous singer", "a cricket player", "a cook"], "She lived in Rajasthan long ago."),
         ("Which animal is protected by the Bishnoi community?", "the blackbuck", ["the camel only", "the rat", "the cockroach"], "They also protect chinkara deer."),
         ("Why should we save water?", "every living thing needs water and clean water is limited", ["water never runs out", "water is useless", "only plants need water"], "Close taps tightly."),
         ("Why should we not throw stones at birds?", "it hurts them and they help nature", ["birds like stones", "it makes them fly better", "it is a game"], "Birds eat insects and spread seeds."),
         ("What is a bird sanctuary?", "a protected place where birds can live safely", ["a bird market", "a cage", "a zoo for lions"], "Bharatpur has a famous one."),
         ("Why do we celebrate Van Mahotsav?", "to plant trees", ["to cut trees", "to catch fish", "to fly kites"], "It is celebrated in July."),
         ("How can a school help nature?", "by having a garden, saving water and paper and keeping the campus clean", ["by cutting its trees", "by wasting paper", "by burning waste"], "Every student can help."),
         ("How do trees keep the air clean?", "they take in carbon dioxide and give out oxygen", ["they give out smoke", "they make dust", "they stop the wind"], "Trees are the lungs of the Earth."),
         ("Why should we walk or cycle for short trips?", "it keeps the air clean and keeps us fit", ["it pollutes the air", "it wastes petrol", "it harms trees"], "Cars and bikes give out smoke."),
         ("Which animals are friends of farmers because they eat pests?", "frogs, owls and birds", ["rats", "locusts", "termites"], "They protect crops.")]
KIND = {"a kind thing to do for nature": ["planting a sapling", "putting out water for birds in summer", "using a cloth bag", "switching off unused lights", "feeding a stray puppy gently", "picking up litter in a park",
                                         "making a bird feeder", "watering trees on your street", "putting peels in a compost bin"],
        "a harmful thing to do to nature": ["throwing plastic in a river", "breaking branches of trees", "chasing birds for fun", "plucking flowers in a park", "leaving the tap running", "bursting loud crackers near animals",
                                            "writing names on tree trunks", "feeding plastic bags to cows", "burning dry leaves"]}
HELPERS = [("owls", "eating rats in the fields"), ("bees", "carrying pollen from flower to flower"), ("earthworms", "making the soil soft and rich"), ("frogs", "eating insects near ponds and fields"),
           ("vultures", "cleaning up dead animals"), ("ladybirds", "eating aphids, tiny insects that suck plant juice"), ("birds that eat fruit", "spreading seeds to new places"), ("cows", "giving dung that is used as manure"),
           ("bats", "pollinating some flowers at night"), ("ants", "breaking down dead insects and leaves"), ("snakes", "eating rats that damage stored grain"), ("mongooses", "keeping snakes and rats away from homes")]
CARE = [("you find a baby bird that has fallen from its nest", "tell an adult and call a bird rescuer"), ("you see a stray dog that is hurt", "tell an adult and inform an animal shelter or a vet"),
        ("there is a lot of litter in your park", "pick it up with gloves and put it in a dustbin"), ("it is a very hot summer day", "put a bowl of water outside for birds and animals"),
        ("you see someone cutting a big tree for no reason", "tell an adult who can ask them to stop"), ("you want to see birds in your garden", "plant trees and shrubs and stay quiet"),
        ("you have vegetable peels after cooking", "put them in a compost pit"), ("a snake comes into the garden", "stay away and ask an adult to call a snake rescuer"),
        ("you see a cow eating a plastic bag", "tell an adult and never throw plastic on the road"), ("you see a bee on a flower", "watch it quietly and let it work"),
        ("you find an injured squirrel", "tell an adult and call an animal helpline"), ("there is a bird's nest in your window", "leave it alone and keep the window area quiet"),
        ("your friend throws a wrapper on the ground", "ask them kindly to put it in a dustbin"), ("you see a leaking tap in school", "tell a teacher so it can be repaired")]
GIFTS = [("a cow", "milk"), ("a sheep", "wool"), ("a honeybee", "honey"), ("a silkworm", "silk"), ("a hen", "eggs"), ("an ox", "help in ploughing fields"),
         ("a camel", "carrying loads in the desert"), ("a yak", "milk, wool and carrying loads in the mountains"),
         ("a goat", "milk"), ("a donkey", "carrying loads"), ("a horse", "riding and pulling carts"), ("a lac insect", "lac, used for bangles and polish")]


def c_count(k=None):
    R = _R[0]
    g, p, s_, u, c = R.choice([0, 0, 1, 2]), R.choice([1, 2, 2]), R.choice([0, 1, 2, 3]), R.choice([0, 0, 1, 2]), R.choice([0, 0, 1, 2, 3])
    if u == 0:
        c = 0
    parts, tot = [], 1 + g + p + s_ + u + c
    if g: parts.append("%s" % ("a grandmother" if g == 1 else "two grandparents"))
    parts.append("a mother" if p == 1 else "both parents")
    if s_: parts.append("%s" % ["", "one sister", "two brothers", "a brother and two sisters"][s_])
    if u: parts.append("%s" % ("an uncle" if u == 1 else "an uncle and an aunt"))
    if c: parts.append("%s" % ["", "one cousin", "two cousins", "three cousins"][c])
    n = kid()
    desc = ", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]
    if R.random() < 0.5:
        return nq("%s lives with %s. How many people are there in the family, counting %s?" % (n, desc, n), tot, [tot - 1, tot + 1, tot + 2, len(parts)], "",
                  "Count everyone, including %s: %d people." % (n, tot))
    joint = g > 0 or u > 0
    a = "a joint family" if joint else "a nuclear family"
    return tq("%s lives with %s. What kind of family is this?" % (n, desc), a, [x for x in ["a joint family", "a nuclear family", "not a family at all", "a family of friends only"] if x != a],
              "A joint family includes grandparents, uncles or aunts; a nuclear family is parents and their children.")


def UNITS3a():
    b = {k: once_maker(v) for k, v in [("f1", F1), ("mela", MELAQ), ("fq", FQ), ("pl", PLQ), ("pa", PAQ), ("h3", HARM3)]}
    rel = pairs(REL, "Who is %s to you?")
    fam = odd_one(FAM, "Which of these describes %s?")
    hlp = odd_one(HELP, "Which of these is %s?")
    mela = pairs(MELA, "What does %s sell or make at a mela?", "Who sells or makes %s at a mela?")
    msafe = odd_one(MSAFE, "Which of these is %s?", "Which of these is not %s?")
    fest = pairs(FEST, "In which part of India is %s an important festival?", "Which festival is especially celebrated in %s?")
    natf = pairs(NATF, "On which date is %s celebrated?", "Which day is celebrated on %s?")
    ffood = pairs(FFOOD, "Which food is special during %s?", "During which festival do people enjoy %s?")
    fkind = odd_one(FKIND, "Which of these is %s?", "Which of these is not %s?")
    parts = pairs(PARTS, "What does %s of a plant do?", "Which part of a plant does this job: %s?")
    psize = odd_one(PSIZE, "Which of these plants is %s?", "Which of these plants is not %s?")
    puse = pairs(PUSE, "How do people use %s?", "Which plant gives us %s?")
    home = pairs(HOME, "Where does %s live?", "Who lives in %s?")
    where = odd_one(WHERE, "Which of these is %s?", "Which of these is not %s?")
    eats = odd_one(EATS, "Which of these is %s?", "Which of these is not %s?")
    kind = odd_one(KIND, "Which of these is %s?", "Which of these is not %s?")
    hlps = pairs(HELPERS, "How do %s help us or nature?", "Which animals help by %s?")
    care = pairs(CARE, "What should you do if %s?")
    gifts = pairs(GIFTS, "What does %s give us?", "Which animal gives us %s?")
    return [
        U(1, "family-and-friends", 1, FC,
          "Families of different kinds and sizes; relations within a family; elders and traditions; sharing work at home; friends, neighbours and pets; staying safe (summary of NCERT Our Wondrous World Chapter 1).",
          "Family and Friends", "family and friends",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 1: family members and relations, joint and nuclear families, helping at home, friends, pets and staying safe. 100 questions with answers.",
          "Every family is special.", "We help at home and care for each other.",
          "<p>A family can be big or small. In a joint family, grandparents, parents, uncles, aunts and cousins live together; in a nuclear family, parents and children live together. We call our father's or mother's mother 'grandmother' and their brothers 'uncles'.</p>"
          "<p>Family members share the work at home and care for each other. Good friends are kind, share and help. We care for pets with food, water and love, and we never go with strangers.</p>",
          [("Who is your mother's brother?", ["your parent's brother"], "your uncle"), ("Parents and two children in one home?", ["a small family"], "a nuclear family")],
          ["Calling a cousin a brother.", "Thinking only big families are real families.", "Going with a stranger who offers sweets."],
          [("What is a joint family?", "A family in which grandparents, parents, uncles, aunts and cousins live together."),
           ("How can children help at home?", "By watering plants, setting the table, folding clothes and keeping their things in place.")],
          lambda: [("My family", [(b["f1"], 6), (c_count, 14)]), ("Family relations", [(rel, 12), (b["f1"], 6), (fam, 2)]), ("Helping at home", [(hlp, 12), (b["f1"], 6), (c_count, 2)]),
                   ("Friends and neighbours", [(b["f1"], 4), (c_count, 10), (rel, 6)]), ("Mixed problems", [(hlp, 4), (rel, 2), (fam, 2), (b["f1"], 3), (c_count, 9)])]),
        U(2, "going-to-the-mela", 2, FC,
          "A visit to a mela (fair): sights, sounds, crafts and artisans; buying and selling with money; staying safe in a crowd; famous melas of India (summary of NCERT Our Wondrous World Chapter 2).",
          "Going to the Mela", "going to the mela",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 2: sights and crafts at a mela, artisans, counting money and change, safety in crowds and famous melas of India. 100 questions with answers.",
          "A mela is a fair full of crafts, food and fun.", "Count your money and stay close to adults.",
          "<p>A mela is a fair where people come together to buy, sell, play and celebrate. Potters, weavers, toy makers and bangle sellers bring things they make by hand, and there are rides like the giant wheel and puppet shows.</p>"
          "<p>We use coins and notes to pay and count the change carefully. In a crowd, hold an adult's hand, remember a parent's phone number and ask a police officer or the help desk if you are lost. Famous melas include the Kumbh Mela, the Pushkar camel fair and the Surajkund crafts mela.</p>",
          [("₹50 − ₹15?", ["take away the cost"], "₹35 left"), ("Lost at a mela?", ["stay in one place"], "ask the help desk or a police officer")],
          ["Going home alone when lost.", "Adding when you should subtract the change.", "Throwing litter at the mela."],
          [("Why are melas important?", "They bring people together and help artisans sell what they make."),
           ("What should you do if you get lost at a mela?", "Stay where you are and ask a police officer or the help desk for help.")],
          lambda: [("At the mela", [(b["mela"], 10), (mela, 10)]), ("Artisans and crafts", [(mela, 10), (b["mela"], 4), (K(c_money, "coins"), 6)]), ("Buying things", [(K(c_money, "left"), 10), (K(c_money, "total"), 10)]),
                   ("Safety at the mela", [(msafe, 14), (b["mela"], 4), (c_money, 2)]), ("Mixed problems", [(c_money, 20)])]),
        U(3, "celebrating-festivals", 3, FC,
          "Festivals of India and how communities celebrate them; harvest festivals of different states; national festivals and important days; celebrating in eco-friendly ways (summary of NCERT Our Wondrous World Chapter 3).",
          "Celebrating Festivals", "celebrating festivals",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 3: festivals of different states, harvest festivals, national festivals and their dates, and celebrating without harming nature. 100 questions with answers.",
          "Festivals bring people together.", "Harvest festivals thank nature for crops.",
          "<p>India has many festivals. Harvest festivals such as Pongal in Tamil Nadu, Onam in Kerala, Bihu in Assam and Baisakhi in Punjab give thanks for good crops. People decorate homes, draw rangolis, cook special food and share it with friends.</p>"
          "<p>National festivals belong to all of us: Republic Day on 26 January, Independence Day on 15 August and Gandhi Jayanti on 2 October. We can celebrate without harming nature by using clay lamps and natural colours and avoiding loud crackers and plastic.</p>",
          [("Onam is celebrated mainly in…", ["snake boat races"], "Kerala"), ("Republic Day date?", ["the Constitution began"], "26 January")],
          ["Mixing up Independence Day and Republic Day.", "Thinking only one festival is celebrated in India.", "Forgetting the environment during celebrations."],
          [("What is a harvest festival?", "A festival that gives thanks for a good crop, such as Pongal, Onam, Bihu or Baisakhi."),
           ("Why is 15 August special?", "India became independent on 15 August 1947.")],
          lambda: [("Festivals of India", [(fest, 12), (b["fq"], 8)]), ("Harvest festivals", [(fkind, 10), (fest, 6), (ffood, 4)]), ("National festivals", [(natf, 12), (b["fq"], 8)]),
                   ("Festival foods", [(ffood, 12), (b["fq"], 4), (fkind, 4)]), ("Mixed problems", [(fkind, 10), (natf, 6), (fest, 2), (b["fq"], 2)])]),
        U(4, "getting-to-know-plants", 4, LA,
          "Plants around us: trees, shrubs, herbs and climbers; parts of a plant and their work; parts of plants that we eat; what plants need to grow; caring for plants (summary of NCERT Our Wondrous World Chapter 4).",
          "Getting to Know Plants", "getting to know plants",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 4: trees, shrubs, herbs and climbers, parts of a plant, the parts we eat, and what plants need to grow. 100 questions with answers.",
          "Plants have roots, stems, leaves, flowers, fruits and seeds.", "Plants need sunlight, water, air and soil.",
          "<p>Plants can be big trees like the mango and neem, bushy shrubs like the rose and tulsi, small herbs like mint and grass, or climbers like the money plant. Each part has a job: roots hold the plant and take in water, the stem holds it up, leaves make food using sunlight, and flowers make fruits and seeds.</p>"
          "<p>We eat different parts of plants: carrots are roots, potatoes are stems, spinach is leaves, cauliflower is flowers, mangoes are fruits and peas are seeds. Plants need sunlight, water, air and soil to grow.</p>",
          [("Which part is a carrot?", ["it grows down into the soil"], "the root"), ("Which part makes food?", ["green and flat"], "the leaf")],
          ["Thinking a potato is a root.", "Thinking plants need no sunlight.", "Calling a tall rose bush a tree."],
          [("Which parts of plants do we eat?", "Roots (carrot), stems (potato), leaves (spinach), flowers (cauliflower), fruits (mango) and seeds (peas)."),
           ("What do plants need to grow?", "Sunlight, water, air and soil.")],
          lambda: [("Trees, shrubs, herbs and climbers", [(psize, 14), (b["pl"], 6)]), ("Parts of a plant", [(parts, 8), (b["pl"], 12)]), ("Plants we eat", [(c_eat, 16), (psize, 4)]),
                   ("Useful plants", [(puse, 16), (b["pl"], 4)]), ("Mixed problems", [(psize, 14), (c_eat, 4), (puse, 2)])]),
        U(5, "plants-and-animals-live-together", 5, LA,
          "Homes of animals; animals of trees, land and water; what animals eat; how plants and animals depend on each other for food and shelter (summary of NCERT Our Wondrous World Chapter 5).",
          "Plants and Animals Live Together", "plants and animals live together",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 5: animal homes, animals of trees, land and water, plant-eaters and meat-eaters, and how plants and animals help each other. 100 questions with answers.",
          "Plants and animals depend on each other.", "Birds live in nests, bees in hives, rabbits in burrows.",
          "<p>Animals live in many kinds of homes: birds in nests, bees in hives, rabbits in burrows, spiders in webs and lions in dens. Some animals live in trees, some on land and some in water. Their home and surroundings are their habitat.</p>"
          "<p>Some animals eat only plants (cows), some eat other animals (lions) and some eat both (crows). Plants give animals food and shelter; animals help plants by carrying pollen and spreading seeds.</p>",
          [("Where does a bee live?", ["many bees together"], "in a hive"), ("Does a lion eat plants?", ["it hunts"], "no, it eats other animals")],
          ["Thinking all animals live in nests.", "Calling a dolphin a fish.", "Forgetting that animals help plants too."],
          [("How do plants and animals help each other?", "Plants give food, shelter and oxygen; animals carry pollen and spread seeds."),
           ("What is a habitat?", "The natural home of a plant or animal, where it gets food, water and shelter.")],
          lambda: [("Homes of animals", [(home, 14), (b["pa"], 6)]), ("Where animals live", [(where, 14), (b["pa"], 6)]), ("What animals eat", [(eats, 16), (b["pa"], 4)]),
                   ("Plants and animals help each other", [(b["pa"], 4), (where, 8), (eats, 8)]), ("Mixed problems", [(home, 4), (where, 8), (eats, 8)])]),
        U(6, "living-in-harmony", 6, LA,
          "Living in harmony with nature; caring for plants and animals; how animals help us and nature; communities that protect nature such as the Bishnois and the Chipko movement (summary of NCERT Our Wondrous World Chapter 6).",
          "Living in Harmony", "living in harmony",
          "Free CBSE Class 3 EVS worksheets for NCERT Our Wondrous World Chapter 6: kind and harmful actions, how animals help nature, caring for birds and street animals, the Chipko movement and the Bishnois. 100 questions with answers.",
          "We share the Earth with plants and animals.", "Be kind to nature; it takes care of us.",
          "<p>Living in harmony means living kindly with plants, animals and people. Bees pollinate flowers, owls and snakes eat rats in the fields, earthworms make soil rich and vultures clean up dead animals.</p>"
          "<p>We can help by planting trees, giving water to birds, being gentle with animals and not littering. The Bishnoi community of Rajasthan protects trees and blackbucks, and in the Chipko movement villagers hugged trees to save them.</p>",
          [("How do owls help farmers?", ["they hunt at night"], "they eat rats"), ("Throwing plastic in a river is…", ["it harms fish"], "harmful")],
          ["Thinking snakes and owls are only harmful.", "Chasing birds for fun.", "Thinking one person cannot help nature."],
          [("What was the Chipko movement?", "A movement in which villagers hugged trees to stop them from being cut down."),
           ("How can we help birds in summer?", "By keeping bowls of clean water and some grain for them.")],
          lambda: [("Living in harmony", [(b["h3"], 10), (kind, 10)]), ("Kind and harmful actions", [(kind, 14), (b["h3"], 6)]), ("Animals that help", [(hlps, 14), (gifts, 6)]),
                   ("Caring for nature", [(care, 11), (b["h3"], 4), (gifts, 3), (kind, 2)]), ("Mixed problems", [(kind, 4), (hlps, 6), (b["h3"], 1), (gifts, 9)])]),
    ]
