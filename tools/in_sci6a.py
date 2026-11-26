# -*- coding: utf-8 -*-
"""Class 6 Science (NCERT Curiosity, chapters 1–6): question makers and UNITS6a()."""
import re
from uk_alsci import tq, once_maker
import uk_alsci
from in_sci import pairs, _R, U, K


def nq(q, val, wrongs, unit, e, sf=3):
    """number item for Class 6–8: a space before the unit, no wrong values of a million or more (they would print in standard form)"""
    wrongs = [w for w in wrongs if w is not None and abs(w) < 1e6 and (val <= 0 or w > 0) and (abs(w) >= 0.001 or w == 0)]
    return uk_alsci.nq(q, val, wrongs, (" " + unit) if unit and unit[0] != " " and unit != "°" else unit, e, sf)


def _cap(x):
    return x[0].upper() + x[1:]


def odd_one(groups, q, qn=None, e=None):
    """'Which of these is <label>?'; qn asks for the one that is not (skipped for negative labels such as non-living)"""
    def f():
        R = _R[0]
        lab = R.choice(sorted(groups))
        others = sorted({x for k, v in groups.items() if k != lab for x in v})
        neg = re.match(r"(an? )?(non|not|un(healthy|desirable|safe)|in[a-z]+able|insoluble|opaque)", lab)
        if qn and not neg and R.random() < 0.5 and len(groups[lab]) >= 3:
            a = R.choice(others)
            sa = "“%s”" % a if a[-1] in ".?!" else _cap(a)
            return tq(qn % lab, a, R.sample(groups[lab], 3), "%s: not %s. The other three are." % (sa, lab))
        a = R.choice(groups[lab])
        sa = "“%s”" % a if a[-1] in ".?!" else _cap(a)
        return tq(q % lab, a, R.sample(others, 3), "%s: %s." % (sa, lab) if not e else e % (sa, lab))
    return f

NS, LW, MT, PH, ES = "The Nature of Science", "The World of the Living", "Materials", "Physical Phenomena", "Earth and Space"


def name():
    import in_sci
    return in_sci.name()


# =================================================================== Chapter 1: the wonderful world of science
STEPS = [("observing", "looking carefully and noticing something with our senses"), ("asking a question", "wondering why or how something happens"),
         ("making a prediction (hypothesis)", "making a sensible guess about what will happen"), ("doing an experiment", "testing the guess in a fair way"),
         ("recording results", "writing down or drawing what we see and measure"), ("drawing a conclusion", "deciding what the results tell us"),
         ("sharing findings", "telling others what we found so they can check it")]
OBS = {"an observation": ["The leaves of the plant on the window sill are turning yellow.", "The ice cube melted in 10 minutes in the sun.", "The magnet picked up 12 pins.",
                          "The water in the steel glass felt cold.", "Ants are walking in a line towards the sugar.", "The bean seed has sprouted after three days.", "The candle flame is yellow at the top."],
       "a question": ["Why do ants walk in a line?", "Does a plant need sunlight to stay green?", "Which cloth dries fastest?", "Why does ice melt faster in the sun?",
                      "How many pins can a magnet hold?", "Do seeds need water to sprout?"],
       "a prediction": ["I think the wet cloth will dry faster in the wind.", "I think the plant kept in the dark will turn yellow.", "I think salt will dissolve faster in hot water.",
                        "I think the bigger magnet will pick up more pins.", "I think the seeds without water will not sprout."]}
FAIR = [("Does the amount of sunlight change how tall a plant grows?", "the amount of sunlight", "the height of the plant", "the amount of water given"),
        ("Does the size of a sugar cube change how fast it dissolves?", "the size of the sugar cube", "the time taken to dissolve", "the amount and temperature of the water"),
        ("Does a heavier ball roll further down a slope?", "the mass of the ball", "the distance the ball rolls", "the height of the slope"),
        ("Does a wet cloth dry faster in the wind?", "whether the cloth is in the wind", "the time taken to dry", "the size of the cloth"),
        ("Do seeds sprout faster in warm places?", "the temperature", "the number of seeds that sprout", "the amount of water"),
        ("Does a bigger magnet pick up more pins?", "the size of the magnet", "the number of pins picked up", "the type of pins"),
        ("Does hot water dissolve salt faster than cold water?", "the temperature of the water", "the time taken for the salt to dissolve", "the amount of salt"),
        ("Does the shape of a paper boat change how much load it can carry?", "the shape of the boat", "the number of coins it carries before sinking", "the kind of paper"),
        ("Does the length of a pendulum change the time of one swing?", "the length of the thread", "the time for one swing", "the mass of the bob"),
        ("Does ice melt faster in a steel bowl or a plastic bowl?", "the material of the bowl", "the time taken for the ice to melt", "the size of the ice cube"),
        ("Do plants grow better with compost?", "whether compost is added", "the height of the plants after two weeks", "the kind of seed"),
        ("Does a drop of ink spread faster in hot water?", "the temperature of the water", "the time taken for the colour to spread", "the size of the ink drop")]


def c_fair(k=None):
    R = _R[0]
    q, ch, me, keep = R.choice(FAIR)
    k = k or R.choice(["change", "measure", "keep"])
    pick = {"change": ch, "measure": me, "keep": keep}
    others = [x for x in (ch, me, keep) if x != pick[k]]
    extra = R.choice(["the colour of the label on the pot", "the name of the person doing the test", "the day of the week"])
    if k == "keep":
        return tq("A class tests this question: <i>%s</i> Which of these must be kept the same to make it a fair test?" % q, keep, [ch, me, extra],
                  "Only %s is changed; %s is measured; %s must stay the same." % (ch, me, keep))
    if k == "change":
        return tq("A class tests this question: <i>%s</i> What should they change on purpose?" % q, ch, [me, keep, extra],
                  "They change %s and measure %s." % (ch, me))
    return tq("A class tests this question: <i>%s</i> What should they measure?" % q, me, [ch, keep, extra],
              "They change %s and measure %s." % (ch, me))


SCEN = [("Riya notices that the curd sets faster in summer than in winter.", "observing"), ("Aman wonders whether salt dissolves faster in warm water.", "asking a question"),
        ("Meena says, 'I think the plant in the dark will turn pale.'", "making a prediction (hypothesis)"), ("Kabir keeps two pots of seeds, one watered and one dry, for a week.", "doing an experiment"),
        ("Sana writes the height of each plant in a table every day.", "recording results"), ("After the test, Dev says that seeds need water to sprout.", "drawing a conclusion"),
        ("The class makes a poster to show their findings to other classes.", "sharing findings"), ("Arjun sees that ants carry bits of food back to a hole.", "observing"),
        ("Nisha asks why her shadow is longer in the evening.", "asking a question"), ("Rohan guesses that the bigger ball will roll farther.", "making a prediction (hypothesis)"),
        ("Fatima drops a feather and a coin from the same height and times them.", "doing an experiment"), ("Joseph draws a bar graph of the number of birds seen each day.", "recording results"),
        ("Priya finds that the wet cloth in the wind dried first, so wind speeds up drying.", "drawing a conclusion"), ("Ishaan presents his results at the school science fair.", "sharing findings")]
TOOLS = [("a magnifying glass", "seeing small things such as the hairs on a leaf"), ("a thermometer", "measuring how hot or cold something is"),
         ("a measuring tape", "measuring the length of a table or a room"), ("a stopwatch", "measuring how long something takes"),
         ("a weighing balance", "finding the mass of a bag of rice"), ("a measuring cylinder", "measuring the volume of a liquid"),
         ("a magnetic compass", "finding the north–south direction"), ("a microscope", "seeing tiny cells and microbes"), ("a telescope", "looking at the Moon and distant stars"),
         ("a rain gauge", "measuring how much rain has fallen"), ("a spring balance", "measuring the weight of an object hung from it"), ("a beaker", "holding and heating liquids in the laboratory")]
SCI1 = [("What is science?", "a way of finding out about the world by observing, asking questions and testing ideas", ["a list of facts to memorise", "magic", "only what is written in books"], "Science is a way of thinking and finding out."),
        ("Which is the first step in finding out like a scientist?", "observing carefully", ["drawing a conclusion", "sharing the findings", "writing the answer"], "Observation leads to questions."),
        ("Why should an experiment be repeated?", "to check that the results are reliable", ["to make it take longer", "to change the answer", "to waste materials"], "If the results agree, we can trust them more."),
        ("What should you do if the result of an experiment does not match your prediction?", "accept the result and think of a new idea to test", ["change the result", "hide the result", "stop asking questions"], "Scientists learn from unexpected results."),
        ("Why do scientists share their results?", "so that others can check and build on them", ["to keep them secret", "so nobody else asks questions", "to win prizes only"], "Science grows when ideas are checked."),
        ("Which quality helps a young scientist most?", "curiosity", ["impatience", "guessing without testing", "copying answers"], "Curiosity makes us ask questions."),
        ("Why is it important to change only one thing in a fair test?", "so we know what caused the result", ["so the test is faster", "so it uses less water", "so the result is always the same"], "If many things change, we cannot tell which one mattered."),
        ("A pot of soil is kept dry and another is watered. The watered seeds sprout. What can you conclude?", "seeds need water to sprout", ["seeds need darkness", "seeds need sugar", "seeds sprout without water"], "Only water was different."),
        ("Which of these is a safety rule during an experiment?", "never taste or smell an unknown substance directly", ["mix any chemicals you find", "run in the laboratory", "touch a hot flame"], "Follow your teacher's instructions."),
        ("What is a hypothesis?", "a sensible guess that can be tested", ["a proven law", "the final answer", "a type of instrument"], "We test it by an experiment."),
        ("Which of these is science used for in daily life?", "keeping food fresh in a refrigerator", ["reading a story", "playing music for fun", "choosing a favourite colour"], "Science and technology help us every day."),
        ("Why do we record results in a table?", "to see patterns in the data clearly", ["to make the page colourful", "to hide the data", "because tables are always correct"], "Tables and graphs help us compare."),
        ("What does it mean to infer?", "to explain an observation using what you know", ["to measure a length", "to repeat an experiment", "to guess without any reason"], "Dark clouds are an observation; 'it may rain' is an inference."),
        ("Which branch of science studies living things?", "biology", ["physics", "chemistry", "geology"], "Physics studies forces and energy; chemistry studies substances."),
        ("Which branch of science studies substances and how they change?", "chemistry", ["biology", "astronomy", "botany"], "Biology is the study of living things."),
        ("Which branch of science studies the stars and planets?", "astronomy", ["zoology", "chemistry", "botany"], "Astronomers use telescopes."),
        ("Why should we not believe everything we hear without checking?", "ideas should be supported by evidence", ["everything we hear is false", "checking is not allowed", "evidence does not matter"], "Scientists ask: how do we know?"),
        ("What are the senses we use to observe?", "seeing, hearing, touching, smelling and tasting", ["only seeing", "only hearing", "thinking and dreaming"], "Some things should never be tasted."),
        ("What is a variable in an experiment?", "something that can change or be changed", ["something that never changes", "the name of the scientist", "a kind of thermometer"], "In a fair test, we change one variable at a time."),
        ("Why do scientists sometimes use models?", "to help understand things too big, small or far to see", ["to make things look pretty", "to hide the truth", "because they are always exact"], "A globe is a model of the Earth."),
        ("Which Indian scientist won the Nobel Prize in 1930 for his work on the scattering of light?", "C. V. Raman", ["A. P. J. Abdul Kalam", "Homi Bhabha", "Vikram Sarabhai"], "28 February is celebrated as National Science Day for the Raman effect."),
        ("Why is 28 February celebrated as National Science Day in India?", "C. V. Raman announced the Raman effect on that day in 1928", ["it is the birthday of Isaac Newton", "India launched its first satellite", "the first rocket was made"], "Schools hold science fairs on this day."),
        ("Which Indian scientist is known as the father of the Indian space programme?", "Vikram Sarabhai", ["C. V. Raman", "J. C. Bose", "S. Ramanujan"], "He helped set up ISRO."),
        ("Which Indian scientist showed that plants respond to stimuli, using his crescograph?", "Jagadish Chandra Bose", ["C. V. Raman", "Vikram Sarabhai", "Homi Bhabha"], "The crescograph measures plant growth."),
        ("Why is it a good idea to write down your observations at once?", "we may forget details or remember them wrongly later", ["writing makes the result change", "observations never matter", "it makes the experiment faster"], "Keep a science notebook."),
        ("A student gets a different result from her friend in the same test. What should they do?", "repeat the test carefully and compare their methods", ["choose the result they like", "stop the test", "copy one result"], "Repeating helps find mistakes."),
        ("Which is a question that can be tested by an experiment?", "Does sugar dissolve faster in hot water?", ["Which colour is the prettiest?", "Is music better than painting?", "Which food tastes the nicest?"], "Testable questions can be answered by measuring."),
        ("Why must a fair test use the same amount of water in each pot?", "so that water does not cause the difference in results", ["so the pots look the same", "because water is free", "so that the plants grow slower"], "Only the thing being tested should differ."),
        ("What should you do with your results after an experiment?", "look for a pattern and decide what they show", ["throw them away", "keep them secret", "change them to match your guess"], "This is drawing a conclusion."),
        ("Why do we use instruments to observe?", "our senses alone cannot measure exactly", ["instruments are always fun", "our senses are always wrong", "they replace thinking"], "A thermometer gives an exact temperature.")]

# =================================================================== Chapter 2: diversity in the living world
PLANTS = {"a herb": ["tomato", "wheat", "mint (pudina)", "coriander", "grass", "spinach"], "a shrub": ["rose", "hibiscus (gudhal)", "tulsi", "lemon", "jasmine"],
          "a tree": ["mango", "neem", "banyan", "peepal", "coconut", "teak"], "a climber": ["money plant", "grapevine", "bean plant", "bitter gourd"],
          "a creeper": ["pumpkin", "watermelon", "sweet potato", "bottle gourd"]}
PL = [("herbs", "small plants with soft green stems"), ("shrubs", "medium-sized plants with hard, woody stems that branch near the ground"),
      ("trees", "tall plants with a thick, hard, woody trunk that branches high above the ground"), ("climbers", "weak-stemmed plants that climb up a support using tendrils or by twining"),
      ("creepers", "weak-stemmed plants that spread along the ground"), ("tendrils", "thin coiling parts that help a climber hold on to a support"),
      ("the taproot", "a main root with smaller side roots"), ("fibrous roots", "a bunch of similar thin roots from the base of the stem"),
      ("reticulate venation", "a net-like pattern of veins on a leaf"), ("parallel venation", "veins running side by side along a leaf"),
      ("the lamina", "the flat green part of a leaf"), ("the petiole", "the stalk that joins a leaf to the stem"), ("the midrib", "the thick central vein of a leaf")]
ROOTS = {"a plant with a taproot and leaves with reticulate venation": ["mustard", "rose", "mango", "hibiscus", "tulsi", "pea", "neem", "sunflower"],
         "a plant with fibrous roots and leaves with parallel venation": ["wheat", "maize", "grass", "rice", "banana", "onion", "sugarcane", "bamboo"]}
HAB = [("a camel", "the desert", "long legs keep its body away from the hot sand, and it can go without water for many days"),
       ("a mackerel fish", "the sea", "gills to breathe and a streamlined body with fins to swim"),
       ("a yak", "cold mountains", "long thick hair to keep warm"), ("a snow leopard", "cold mountains", "thick fur and wide paws for walking on snow"),
       ("a frog", "both land and water", "webbed toes for swimming and moist skin"), ("a polar bear", "the icy polar region", "a thick layer of fat and white fur"),
       ("a lotus", "ponds", "leaves that float and a hollow stem"), ("a cactus", "the desert", "spines instead of leaves and a thick fleshy stem that stores water"),
       ("a pine tree", "cold mountains", "a cone shape so that snow slides off"), ("a mountain goat", "cold mountains", "strong hooves for climbing steep slopes"),
       ("a duck", "both land and water", "webbed toes and oily feathers for swimming"), ("a whale", "the sea", "a thick layer of blubber and flippers"),
       ("a dolphin", "the sea", "flippers and a blowhole on top of its head to breathe air"), ("a desert lizard", "the desert", "scaly skin that loses very little water"),
       ("a penguin", "the icy polar region", "thick feathers and a layer of fat"), ("a red panda", "cold mountains", "thick fur and a bushy tail to wrap around itself")]


PLANTS_HAB = ('a lotus', 'a cactus', 'a pine tree')


def c_hab(k=None):
    R = _R[0]
    a, h, ad, = R.choice(HAB)
    if R.random() < 0.5 and a not in PLANTS_HAB:
        hs = sorted({x for b, x, _ in HAB if x != h and b not in PLANTS_HAB})
        return tq("Where does %s mainly live?" % a, h, R.sample(hs, 3), "%s lives in %s: %s." % (a[0].upper() + a[1:], h, ad))
    ads = sorted({x for b, _, x in HAB if b != a})
    return tq("Which feature helps %s to live in %s?" % (a, h), ad, R.sample(ads, 3), "This is an adaptation to its habitat.")


ANIMG = {"an animal that lives in water": ["fish", "octopus", "crab", "jellyfish", "dolphin"], "an animal that lives on land": ["cow", "lion", "ant", "horse", "elephant"],
         "an animal that can live both on land and in water": ["frog", "turtle", "crocodile", "duck"]}
DIV = [("What is biodiversity?", "the variety of plants, animals and other living things in a place", ["the number of buildings in a city", "only the trees in a forest", "the weather of a place"], "India has very rich biodiversity."),
       ("What is a habitat?", "the place where a living thing lives and finds food, water and shelter", ["the food an animal eats", "the colour of an animal", "a kind of root"], "A pond is the habitat of a fish."),
       ("What are adaptations?", "special features that help a living thing survive in its habitat", ["changes in the weather", "the food chain", "diseases of plants"], "A camel's hump and long legs are adaptations."),
       ("Why do we group living things?", "to study their great variety more easily", ["to make them stop growing", "to give them all the same name", "because they are all the same"], "Grouping by similarities and differences is called classification."),
       ("A plant has a weak stem and spreads on the ground. What is it?", "a creeper", ["a tree", "a shrub", "a climber"], "Pumpkin is a creeper."),
       ("A plant has a weak stem and climbs a wall using tendrils. What is it?", "a climber", ["a creeper", "a herb", "a tree"], "Money plant and pea are climbers."),
       ("Leaves with parallel venation usually have which kind of roots?", "fibrous roots", ["a taproot", "no roots", "breathing roots only"], "Grass and wheat are examples."),
       ("Leaves with reticulate venation usually have which kind of roots?", "a taproot", ["fibrous roots", "no roots", "roots only at the tip"], "Mustard and mango are examples."),
       ("How can you see the venation of a leaf clearly?", "by making a leaf print or a rubbing on paper", ["by boiling it", "by painting it black", "by keeping it in the dark"], "The veins stand out in the print."),
       ("Which is an example of a plant used for medicine in India?", "tulsi", ["plastic", "sand", "iron"], "Neem and tulsi are well-known medicinal plants."),
       ("Why should we protect the variety of life?", "living things depend on each other for food and shelter", ["only a few animals matter", "plants can live without animals", "it has no use"], "Loss of one species affects others."),
       ("A dolphin breathes air through a blowhole. Which group does it belong to?", "mammals", ["fish", "amphibians", "insects"], "Dolphins and whales are mammals that live in water."),
       ("Which part of a plant holds it firmly in the soil?", "the root", ["the leaf", "the flower", "the fruit"], "Roots also absorb water and minerals."),
       ("Which part of a plant carries water from the roots to the leaves?", "the stem", ["the petal", "the seed", "the flower"], "The stem also supports the leaves."),
       ("What do we call plants that are found only in one region and nowhere else?", "endemic plants", ["weeds", "climbers", "herbs"], "Many plants of the Western Ghats are endemic."),
       ("Which of these is a way to group animals?", "by where they live, what they eat or how they move", ["by their names in English", "by how much they cost", "by their age only"], "We can use many features."),
       ("Which animals eat only plants?", "herbivores", ["carnivores", "omnivores", "decomposers"], "Cows and deer are herbivores."),
       ("Which animals eat only other animals?", "carnivores", ["herbivores", "producers", "decomposers"], "Lions and tigers are carnivores."),
       ("Which animals eat both plants and animals?", "omnivores", ["herbivores", "carnivores", "producers"], "Crows and humans are omnivores."),
       ("Why does a cactus have spines instead of broad leaves?", "to lose less water in the hot desert", ["to make more food", "to attract insects", "to float on water"], "Its green stem makes food.")]

# =================================================================== Chapter 3: mindful eating
NUTR = [("carbohydrates", "giving us energy"), ("fats", "giving us much energy and storing it in the body"), ("proteins", "growth and repair of the body"),
        ("vitamins", "protecting the body from diseases and keeping us healthy"), ("minerals", "building bones and teeth and keeping the body working well"),
        ("dietary fibre (roughage)", "helping food move through the gut and preventing constipation"), ("water", "carrying nutrients and removing wastes, and keeping the body cool")]
SRC = {"rich in carbohydrates": ["rice", "wheat chapati", "potato", "ragi (finger millet)", "jowar roti", "sugarcane"], "rich in proteins": ["dal (pulses)", "milk", "egg", "paneer", "soybean", "fish", "rajma"],
       "rich in fats": ["ghee", "butter", "groundnuts", "coconut oil", "mustard oil", "cashew nuts"], "rich in vitamin C": ["amla", "orange", "lemon", "guava", "tomato"]}
DEF = [("scurvy", "vitamin C", "bleeding gums and slow healing of wounds"), ("rickets", "vitamin D", "soft and bent bones"),
       ("night blindness", "vitamin A", "poor vision in dim light"), ("beriberi", "vitamin B1", "weak muscles and very little energy"),
       ("anaemia", "iron", "tiredness and pale skin"), ("goitre", "iodine", "a swollen gland in the neck")]


def c_def(k=None):
    R = _R[0]
    d, n, s = R.choice(DEF)
    k = k or R.choice(["cause", "dis", "sym"])
    if k == "cause":
        return tq("Which nutrient is lacking in a person with %s?" % d, n, R.sample(sorted({x for _, x, _ in DEF if x != n}), 3), "%s is caused by a lack of %s (%s)." % (d.capitalize(), n, s))
    if k == "dis":
        return tq("A lack of %s in the diet can cause which disease?" % n, d, R.sample(sorted({x for x, _, _ in DEF if x != d}), 3), "A lack of %s causes %s." % (n, d))
    return tq("Which deficiency disease causes %s?" % s, d, R.sample(sorted({x for x, _, _ in DEF if x != d}), 3), "%s: caused by a lack of %s." % (d.capitalize(), n))


TESTS = [("starch", "a few drops of dilute iodine solution", "a blue-black colour"), ("protein", "copper sulphate solution and sodium hydroxide solution", "a violet (purple) colour"),
         ("fat", "rubbing the food on a piece of paper", "an oily patch that lets light through")]


def c_test(k=None):
    R = _R[0]
    n, how, sign = R.choice(TESTS)
    food = {"starch": ["a potato slice", "boiled rice", "a piece of bread", "wheat flour"], "protein": ["egg white", "a paste of gram (chana)", "milk", "paneer"],
            "fat": ["a groundnut", "a cashew nut", "a bit of butter", "a coconut piece"]}[n]
    f = R.choice(food)
    k = k or R.choice(["sign", "how", "what"])
    if k == "sign":
        return tq("%s is tested for %s using %s. Which result shows that %s is present?" % (f[0].upper() + f[1:], n, how, n), sign, [s for _, _, s in TESTS if s != sign] + ["no change at all"], "%s shows %s." % (sign[0].upper() + sign[1:], n))
    if k == "how":
        return tq("How can you test %s for %s?" % (f, n), "using " + how, ["using " + h for _, h, _ in TESTS if h != how] + ["by smelling it"], "This is the test for %s." % n)
    return tq("A student tests %s and sees %s. Which nutrient is present?" % (f, sign), n, [x for x, _, _ in TESTS if x != n] + ["vitamin C"], "%s means %s." % (sign[0].upper() + sign[1:], n))


EAT = [("What is a balanced diet?", "a diet with all the nutrients in the right amounts, with fibre and water", ["a diet of only fruits", "a diet with no fat at all", "eating as much as possible"], "It keeps us healthy."),
       ("Which millet is rich in calcium?", "ragi (finger millet)", ["polished rice", "refined flour (maida)", "sugar"], "Millets are nutritious and need less water to grow."),
       ("Why are millets called nutri-cereals?", "they are rich in fibre, minerals and vitamins", ["they have no nutrients", "they are made in factories", "they contain only sugar"], "2023 was the International Year of Millets."),
       ("Why should we eat less junk food?", "it has too much salt, sugar and fat and few nutrients", ["it is rich in fibre", "it has all vitamins", "it builds strong bones"], "It can lead to obesity."),
       ("What is a deficiency disease?", "a disease caused by a lack of a nutrient over a long time", ["a disease caught from germs", "an injury", "a disease from eating too much"], "Scurvy and rickets are examples."),
       ("Which vitamin can our skin make in sunlight?", "vitamin D", ["vitamin C", "vitamin A", "vitamin B1"], "It helps bones absorb calcium."),
       ("Why does food from different regions of India differ?", "people use crops and ingredients that grow locally", ["food is the same everywhere", "only rice grows in India", "food has no link to climate"], "Coastal areas use fish and coconut."),
       ("Why should vegetables not be washed after cutting?", "some vitamins dissolve in the water and are lost", ["they become poisonous", "they grow again", "they lose their colour only"], "Wash them before cutting."),
       ("Why is overcooking vegetables not good?", "heat destroys some vitamins such as vitamin C", ["it adds more vitamins", "it adds protein", "it makes them heavier"], "Cook just enough."),
       ("What is obesity?", "having too much body fat, often from eating too much fatty food", ["a lack of iron", "a lack of vitamin C", "a disease of the eyes"], "Exercise and a balanced diet help."),
       ("Why do we need roughage even though it gives no energy?", "it helps the body get rid of undigested food", ["it gives a lot of energy", "it builds muscles", "it is a vitamin"], "Whole grains, fruit and vegetables have fibre."),
       ("Which salt helps to prevent goitre?", "iodised salt", ["rock salt only", "baking soda", "sugar"], "Iodine is added to salt."),
       ("Which food group gives the body most of its energy?", "carbohydrates and fats", ["vitamins and minerals", "water and fibre", "proteins only"], "Fats give more energy per gram."),
       ("Why do growing children need more protein?", "proteins build new body tissue", ["proteins only give heat", "proteins make bones soft", "children do not grow"], "Pulses, milk and eggs are rich in protein."),
       ("What does mindful eating mean?", "paying attention to what, how much and how we eat", ["eating very fast", "eating while watching a screen all the time", "skipping all meals"], "Eat slowly and stop when full."),
       ("Which mineral is needed for strong bones and teeth?", "calcium", ["iodine", "sodium", "iron"], "Milk and ragi are rich in calcium."),
       ("Which mineral is needed to make blood?", "iron", ["calcium", "iodine", "potassium"], "Green leafy vegetables and jaggery have iron."),
       ("Which part of a meal of rice, dal and spinach is rich in protein?", "dal", ["rice", "spinach", "salt"], "Rice gives carbohydrates; spinach gives iron and fibre."),
       ("Why should we drink enough water every day?", "the body loses water through sweat and urine", ["water gives a lot of energy", "water builds muscles", "water is a vitamin"], "About six to eight glasses a day."),
       ("What do we call the part of food that our body uses?", "nutrients", ["roughage", "wastes", "flavours"], "Food contains many nutrients."),
       ("Which of these is a good source of dietary fibre?", "whole grains, fruits and vegetables", ["sugar", "butter", "refined flour (maida)"], "Fibre helps digestion."),
       ("Why is a breakfast of only biscuits and tea not a balanced meal?", "it lacks proteins, vitamins, minerals and fibre", ["it has too much protein", "it has too many vitamins", "it is too rich in fibre"], "Add fruit, milk or sprouts."),
       ("What are sprouts, and why are they nutritious?", "germinated seeds such as moong; they are rich in proteins and vitamins", ["fried snacks with much fat", "sweets made of sugar", "dried leaves"], "Sprouting increases some vitamins."),
       ("Which of these is a traditional food made from millets?", "ragi mudde or bajra roti", ["white bread", "noodles from maida", "potato chips"], "Millets are part of many Indian meals."),
       ("Why do people in cold places eat more fat-rich food?", "fats give a lot of energy and help keep the body warm", ["fats cool the body", "fats give vitamin C", "fats are rich in fibre"], "Ghee and butter are common in cold regions."),
       ("Which part of the food test for starch uses iodine?", "iodine solution is added to the food", ["iodine is heated to boiling", "iodine is mixed with sugar", "iodine is rubbed on paper"], "A blue-black colour shows starch."),
       ("Why should we not skip breakfast?", "the body needs energy after a long night without food", ["skipping meals builds muscles", "breakfast has no nutrients", "it makes us grow taller"], "A good breakfast helps us concentrate."),
       ("What is the result of eating too much sugar and fat over a long time?", "obesity and other health problems", ["stronger bones", "better eyesight", "fewer diseases"], "Sugar also harms teeth."),
       ("Which food gives us both protein and calcium?", "milk", ["sugar", "rice", "cooking oil"], "Milk products such as paneer and curd do too."),
       ("Why does a person with anaemia feel tired?", "the blood cannot carry enough oxygen without enough iron", ["the bones are soft", "the eyes are weak", "the gums bleed"], "Eat green leafy vegetables, jaggery and dates.")]

# =================================================================== Chapter 4: exploring magnets
MAGM = {"a magnetic material": ["iron", "nickel", "cobalt", "a steel spoon", "an iron nail", "a steel safety pin", "iron filings", "a steel paper clip", "an iron tawa", "a steel needle", "a steel key ring", "an iron chain", "a steel tiffin box", "an iron screw"],
        "a non-magnetic material": ["wood", "plastic", "glass", "a rubber eraser", "an aluminium foil", "a copper wire", "a plastic paper clip", "a brass key", "a gold ring",
                                    "a silver spoon", "a leather belt", "a cotton cloth", "a clay cup", "a pencil lead (graphite)", "an aluminium can"]}
MAG = [("Which materials are attracted by a magnet?", "magnetic materials such as iron, nickel and cobalt", ["all metals", "wood and plastic", "glass and rubber"], "Copper, aluminium and brass are not attracted."),
       ("Where is the attraction of a bar magnet strongest?", "near its two ends (the poles)", ["at its middle", "evenly along its length", "only on its painted side"], "Iron filings gather at the poles."),
       ("What happens when the north pole of one magnet is brought near the north pole of another?", "they repel", ["they attract", "nothing happens", "they become non-magnetic"], "Like poles repel."),
       ("What happens when the north pole of one magnet is brought near the south pole of another?", "they attract", ["they repel", "nothing happens", "both lose their magnetism"], "Unlike poles attract."),
       ("Which is the surest test to find out whether a bar is a magnet?", "repulsion with a known magnet", ["attraction to an iron nail", "its shape", "its colour"], "Attraction also happens with plain iron; only a magnet repels a magnet."),
       ("In which direction does a freely hanging bar magnet come to rest?", "north–south", ["east–west", "any direction", "upwards"], "Its north-seeking end points north."),
       ("What is a magnetic compass?", "a small magnetised needle that can turn freely to show the north–south direction", ["a device to measure length", "a clock", "a thermometer"], "Sailors and travellers use it."),
       ("How can you make a magnet from an iron nail?", "stroke it many times in one direction with one pole of a magnet", ["heat it in a flame", "drop it on the floor", "wrap it in paper"], "Stroke it in the same direction each time."),
       ("Which of these can make a magnet lose its magnetism?", "heating, hammering or dropping it many times", ["keeping it with a keeper", "storing it in pairs", "keeping it in a box"], "Store magnets carefully."),
       ("How should bar magnets be stored?", "in pairs with unlike poles on the same side, with keepers of soft iron", ["with like poles together", "near a mobile phone", "in a hot place"], "Keepers help them keep their magnetism."),
       ("Why should magnets be kept away from mobile phones and cards?", "they can damage their working", ["they make them heavier", "they make them wet", "they charge them"], "Also keep them away from TVs and computers."),
       ("What did people in ancient times call natural magnets?", "lodestones (magnetite)", ["marble", "chalk", "coal"], "A legend says a shepherd named Magnes found them."),
       ("Can a magnet attract an iron pin through a sheet of paper?", "yes, magnetic force can act through paper", ["no, never", "only if the paper is wet", "only at night"], "It also acts through glass and plastic."),
       ("Which of these uses a magnet?", "a refrigerator door seal", ["a wooden chair", "a glass window", "a plastic bucket"], "Magnets are also used in speakers and toys."),
       ("How many poles does a bar magnet have?", "two", ["one", "three", "four"], "If you break a magnet, each piece still has two poles."),
       ("What happens if a bar magnet is broken into two pieces?", "each piece becomes a magnet with two poles", ["one piece has only a north pole", "both pieces lose all magnetism", "the pieces repel only"], "You cannot get a single pole."),
       ("How can you separate iron pins mixed with sand?", "move a magnet over the mixture", ["pour water on it", "blow on it", "heat it"], "The pins stick to the magnet."),
       ("Why does the compass needle point north even on a ship far at sea?", "the Earth behaves like a huge magnet", ["the Sun pulls it", "the wind pushes it", "the water turns it"], "This is why compasses help in navigation."),
       ("A magnet attracts a coin. What can you say about the coin?", "it contains a magnetic material such as iron or nickel", ["it is made of pure copper", "it is made of aluminium", "it is made of paper"], "Some coins are made of steel."),
       ("What is the end of a magnet that points north called?", "the north-seeking pole (north pole)", ["the south pole", "the middle", "the keeper"], "The other end is the south pole."),
       ("What does a magnet do to iron filings sprinkled around it?", "they gather mostly at the poles", ["they gather in the middle", "they melt", "they are pushed away"], "This shows where the force is strongest."),
       ("Which shape of magnet has its two poles close together?", "a horseshoe (U-shaped) magnet", ["a bar magnet", "a long rod magnet", "a needle"], "Both ends of the U are poles."),
       ("Why does a compass needle not work well near a magnet?", "the magnet attracts or repels the needle", ["the magnet heats it", "the magnet makes it heavy", "the magnet stops the clock"], "Keep compasses away from magnets."),
       ("Which of these is made using magnets?", "a pencil box with a magnetic lock", ["a glass bottle", "a cotton shirt", "a wooden spoon"], "Magnets also hold notices on boards."),
       ("Which of these is a natural magnet?", "magnetite (lodestone)", ["iron nail", "steel spoon", "copper coin"], "Man-made magnets are made from iron and steel alloys."),
       ("Does a magnet attract a piece of iron placed in water?", "yes, magnetic force acts through water", ["no, water stops it", "only hot water lets it", "only if the water is salty"], "You can pull out an iron pin from a glass of water."),
       ("Why are magnets used in cranes at scrapyards?", "to lift heavy iron and steel objects", ["to lift wood", "to lift plastic", "to cut metals"], "These are electromagnets."),
       ("Which travel tool uses a magnet to show direction?", "a compass", ["a stopwatch", "a ruler", "a thermometer"], "Its needle points north–south."),
       ("What would happen if a ring magnet is dropped onto another with like poles facing?", "it would float above the other", ["it would stick to it", "it would break", "nothing would happen"], "Like poles repel."),
       ("What is a keeper?", "a piece of soft iron placed across the poles of stored magnets", ["a box for coins", "a type of compass", "a plastic cover"], "It helps the magnets keep their strength."),
       ("Which is the best way to find the north pole of an unmarked bar magnet?", "hang it freely; the end that points north is the north pole", ["see which end is heavier", "look at its colour", "heat one end"], "Or use a compass."),
       ("How was the Earth's magnetism helpful to sailors long ago?", "they used a lodestone or compass to find direction at sea", ["it made ships faster", "it kept ships dry", "it stopped storms"], "It works even when the sky is cloudy.")]
SHAPES = ["bar magnet", "horseshoe magnet", "ring magnet", "U-shaped magnet", "cylindrical magnet", "button magnet"]


def c_pole2(k=None):
    R = _R[0]
    s, end, p = R.choice(SHAPES), R.choice(["A", "B"]), R.choice(["north", "south"])
    other = "south" if p == "north" else "north"
    if R.random() < 0.5:
        return tq("The %s pole of a %s repels end %s of a hanging bar. What can you say about end %s?" % (p, s, end, end), "it is a %s pole" % p,
                  ["it is a %s pole" % other, "it is unmagnetised iron", "it is made of wood"], "Only a like pole repels, so end %s is a %s pole." % (end, p))
    return tq("The %s pole of a %s attracts end %s of a hanging bar. What can you say about end %s?" % (p, s, end, end), "it is either a %s pole or unmagnetised iron" % other,
              ["it must be a %s pole" % p, "it must be a %s pole" % other, "it must be made of copper"], "Attraction happens with an unlike pole and with plain iron too, so we cannot be sure.")


DIRS = ["north", "east", "south", "west"]


def c_dir(k=None):
    R = _R[0]
    i = R.randrange(4)
    side, off = R.choice([("behind you", 2), ("on your right", 1), ("on your left", 3)])
    a = DIRS[(i + off) % 4]
    return tq("A compass shows that you are facing %s. Which direction is %s?" % (DIRS[i], side), a, [d for d in DIRS if d != a],
              "Facing %s: right is %s, left is %s and behind is %s." % (DIRS[i], DIRS[(i + 1) % 4], DIRS[(i + 3) % 4], DIRS[(i + 2) % 4]))


def c_pole(k=None):
    R = _R[0]
    a, b = R.choice(["north", "south"]), R.choice(["north", "south"])
    s = R.choice(SHAPES)
    ans = "they repel" if a == b else "they attract"
    return tq("The %s pole of one %s is brought near the %s pole of another. What happens?" % (a, s, b), ans,
              [x for x in ["they repel", "they attract", "nothing happens", "both magnets lose their magnetism"] if x != ans], "%s poles %s." % ("Like" if a == b else "Unlike", "repel" if a == b else "attract"))


# =================================================================== Chapter 5: measurement of length and motion
UNITS_L = [("mm", 0.001), ("cm", 0.01), ("m", 1), ("km", 1000)]


def c_conv(k=None):
    R = _R[0]
    i = R.randrange(3)
    j = i + R.choice([1, 2, 3])
    if j > 3:
        j = 3
    big, small = UNITS_L[j], UNITS_L[i]
    f = round(big[1] / small[1])
    if R.random() < 0.5:
        x = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 25, 1.5, 2.5, 3.5])
        v = x * f
        return nq("Convert %s %s into %s." % (nf(x), big[0], small[0]), v, [x * f / 10, x * f * 10, x * f / 100, x * f * 100, x / f], small[0],
                  "1 %s = %s %s, so %s × %s = %s %s." % (big[0], nf(f), small[0], nf(x), nf(f), nf(v), small[0]))
    v = R.choice([1, 2, 3, 5, 6, 8, 12, 15, 25, 40, 45, 75]) * f // R.choice([1, 2, 4, 5])
    x = v / f
    return nq("Convert %s %s into %s." % (nf(v), small[0], big[0]), x, [x * 10, x / 10, x * 100, x / 100, v * f], big[0],
              "%s %s = %s %s, so divide by %s: %s %s." % (nf(f), small[0], 1, big[0], nf(f), nf(x), big[0]))


def nf(x):
    from uk_alsci import nf as _nf
    return _nf(x)


def c_scale(k=None):
    R = _R[0]
    obj = R.choice(["a pencil", "an eraser", "a crayon", "a leaf", "a key", "a matchstick", "a feather", "a straw", "a chalk piece"])
    a = R.choice([0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0])
    L = R.choice([3.5, 4.5, 5.0, 6.5, 7.0, 8.5, 9.5, 11.0, 12.5, 14.0, 6.0, 10.0])
    b = a + L
    if a == 0:
        return None
    return nq("One end of %s is at the %s cm mark of a scale and the other end is at the %s cm mark. How long is it?" % (obj, nf(a), nf(b)), L, [b, b + a, L + 1, L - 1, a], "cm",
              "Length = %s − %s = %s cm. A broken end of a scale can be used this way." % (nf(b), nf(a), nf(L)))


def c_span(k=None):
    R = _R[0]
    n = R.choice([3, 4, 5, 6, 7, 8, 9, 12])
    s = R.choice([15, 16, 18, 20])
    thing = R.choice(["desk", "door", "bench", "window", "table", "blackboard"])
    import in_sci
    return nq("%s measures a %s as %d handspans. Her handspan is %d cm. About how long is the %s?" % (R.choice(in_sci.GIRLS), thing, n, s, thing), n * s, [n + s, n * s / 10, n * (s + 10), s], "cm",
              "Length ≈ %d × %d = %d cm. Handspans differ, so we use standard units." % (n, s, n * s))


MOT = {"linear (rectilinear) motion": ["a car moving on a straight road", "a ball dropped from a height", "a soldier marching in a straight line", "an apple falling from a tree", "a train on a straight track"],
       "circular motion": ["the tip of a fan blade", "a point on a merry-go-round", "the hands of a clock", "a stone tied to a string and whirled round", "the wheel of a potter"],
       "oscillatory motion": ["a swing moving to and fro", "a pendulum of a clock", "the needle of a sewing machine", "a plucked guitar string", "a see-saw going up and down"]}
LEN = [("What is the SI unit of length?", "the metre (m)", ["the kilogram", "the second", "the litre"], "1 m = 100 cm."),
       ("Why were standard units of length needed?", "units like handspans and cubits differ from person to person", ["standard units are longer", "handspans are always correct", "to make measuring harder"], "Everyone gets the same result with standard units."),
       ("What was a cubit?", "the length from the elbow to the tip of the fingers", ["the width of a thumb", "the length of a foot", "the length of a step"], "It was used in ancient times."),
       ("Where should your eye be when reading a scale?", "exactly above the mark, looking straight down", ["to the left of the mark", "to the right of the mark", "far away from the scale"], "Looking at an angle gives a wrong reading."),
       ("How can you measure the length of a curved line?", "lay a thread along it, mark the ends and measure the thread on a scale", ["use a straight scale directly", "guess it", "use a thermometer"], "A measuring tape can also bend along curves."),
       ("If the zero mark of a scale is broken, what can you do?", "start from another full mark and subtract that reading", ["throw the scale away", "add one centimetre", "guess the length"], "Length = final reading − starting reading."),
       ("What is motion?", "a change in the position of an object with time", ["an object staying still", "the colour of an object", "the mass of an object"], "We compare position with a reference point."),
       ("What is a reference point?", "a fixed object used to describe the position of something", ["a moving car", "a kind of motion", "a unit of time"], "A milestone or a tree can be a reference point."),
       ("A passenger sits in a moving bus. Is she at rest or in motion?", "at rest compared to the bus, but in motion compared to the trees outside", ["at rest compared to everything", "in motion compared to her seat", "neither"], "Rest and motion depend on the reference point."),
       ("What is periodic motion?", "motion that repeats after equal intervals of time", ["motion in a straight line only", "motion that never repeats", "motion of a falling stone only"], "A swing and a clock pendulum show periodic motion."),
       ("Which device do we use to measure the length of a cloth?", "a measuring tape", ["a ruler of 15 cm only", "a thermometer", "a balance"], "Tailors use measuring tapes."),
       ("Which instrument measures the distance travelled by a vehicle?", "an odometer", ["a thermometer", "a compass", "a clock"], "It is in the dashboard."),
       ("How many centimetres are in one metre?", "100", ["10", "1000", "60"], "1 m = 100 cm = 1000 mm."),
       ("How many metres are in one kilometre?", "1000", ["100", "10", "60"], "Distances between towns are measured in km."),
       ("Why should a scale be placed along the length of an object?", "so that the reading is accurate", ["so it looks neat", "so it measures mass", "so it does not break"], "Keep the scale in contact with the object."),
       ("A wheel of a bicycle turns and the bicycle moves forward. Which motions are shown?", "circular motion of the wheel and linear motion of the bicycle", ["only oscillatory motion", "only circular motion", "no motion"], "An object can show more than one motion."),
       ("What does the earth's spinning on its axis show?", "rotational motion", ["linear motion", "oscillatory motion", "no motion"], "It causes day and night."),
       ("Why is a thread used to measure the girth of a tree?", "the trunk is curved", ["thread is heavier", "a scale cannot be read", "it measures temperature"], "Then measure the thread with a scale."),
       ("What is the length of the smallest division on a common 15 cm scale?", "1 mm", ["1 cm", "1 m", "10 cm"], "Each centimetre has 10 small divisions."),
       ("What does 'SI' stand for in SI units?", "the International System of Units", ["Standard Indian units", "Small Instruments", "Science Index"], "Scientists all over the world use SI units."),
       ("Which unit is best for measuring the distance between Delhi and Mumbai?", "the kilometre", ["the millimetre", "the centimetre", "the gram"], "Long distances are given in km."),
       ("Which unit is best for measuring the thickness of a coin?", "the millimetre", ["the kilometre", "the metre", "the litre"], "Very small lengths are in mm."),
       ("Which motion does the Earth show as it goes round the Sun?", "periodic motion (it repeats every year)", ["no motion", "rectilinear motion only", "random motion"], "It also spins on its axis every day."),
       ("Which of these is not a standard unit of length?", "a handspan", ["a metre", "a centimetre", "a kilometre"], "A handspan changes from person to person."),
       ("A boy says a train is moving, but a passenger inside says it is at rest. Who is right?", "both, from their own reference points", ["only the boy", "only the passenger", "neither"], "Motion depends on the reference point."),
       ("What kind of motion does a child on a slide show?", "linear motion along the slide", ["circular motion", "oscillatory motion", "no motion"], "It moves along a straight path."),
       ("What did people in ancient India use 'angul' and 'dhanush' for?", "measuring length", ["measuring time", "measuring mass", "measuring temperature"], "These were old local units."),
       ("Why is a measuring tape better than a ruler for measuring the length of a room?", "it is long and can be rolled", ["it is heavier", "it measures temperature too", "it is made of glass"], "Measure along the floor in a straight line.")]

# =================================================================== Chapter 6: materials around us
PROP = {"transparent (you can see clearly through it)": ["clear glass", "clean water", "air", "a clear plastic sheet", "a glass window pane", "cling film"],
        "translucent (you can see through it but not clearly)": ["butter paper", "frosted glass", "oiled paper", "a thin cloth", "tracing paper", "a thin plastic bag"],
        "opaque (you cannot see through it)": ["wood", "a brick", "cardboard", "a metal plate", "a stone", "a book", "a steel spoon"]}
SOL = {"soluble in water": ["salt", "sugar", "lemon juice", "vinegar", "copper sulphate", "glucose", "alum", "washing soda", "jaggery"],
       "insoluble in water": ["sand", "chalk powder", "sawdust", "oil", "stone pieces", "iron filings", "wax", "coconut oil", "marbles", "plastic beads"]}
FLOAT = {"an object that floats on water": ["a dry leaf", "a piece of wood", "a cork", "an empty plastic bottle with its cap on", "a ball of thermocol", "ice", "a feather", "a coconut", "a ping-pong ball"],
         "an object that sinks in water": ["a stone", "an iron nail", "a coin", "a glass marble", "a key", "a steel spoon", "a brick", "a lump of clay", "a pebble"]}
LUS = {"lustrous (shiny)": ["gold", "silver", "copper", "aluminium foil", "a new iron nail", "a steel plate", "a new brass vessel"],
       "non-lustrous (dull)": ["wood", "chalk", "cardboard", "cotton cloth", "clay", "a piece of coal", "rubber", "paper"]}
USE = [("Why are cooking pots made of metals?", "metals let heat pass through them easily", ["metals are transparent", "metals are soft", "metals dissolve in water"], "The handles are made of plastic or wood, which do not conduct heat well."),
       ("Why are window panes made of glass?", "glass is transparent and lets light in", ["glass is opaque", "glass is soft", "glass is magnetic"], "We can see out through it."),
       ("Why is a raincoat made of plastic?", "plastic does not let water through", ["plastic is transparent", "plastic is heavy", "plastic dissolves in water"], "It keeps us dry."),
       ("Why are tumblers not made of paper for hot tea?", "paper soaks up water and loses its strength", ["paper is too heavy", "paper is a metal", "paper is shiny"], "Steel, glass or clay are used."),
       ("What is a material?", "the substance that an object is made of", ["the shape of an object", "the colour of an object", "the name of an object"], "A chair can be made of wood, plastic or metal."),
       ("Which material is hard?", "iron", ["cotton wool", "sponge", "rubber"], "Hard materials are not easily compressed or scratched."),
       ("Which of these is soft?", "a sponge", ["a stone", "an iron rod", "a brick"], "It can be pressed easily."),
       ("What happens when you shake sand with water and leave it?", "the sand settles at the bottom; it does not dissolve", ["the sand disappears", "the water turns into sand", "the sand floats"], "Sand is insoluble."),
       ("Why do we group materials?", "to study their properties and choose them for the right use", ["to make them heavier", "because all materials are the same", "to change their colour"], "We may group by hardness, lustre or solubility."),
       ("Which property of metals makes them useful for jewellery?", "lustre (shine)", ["softness like cotton", "solubility", "transparency"], "Gold and silver are shiny."),
       ("Do all liquids mix with water?", "no; some, like oil, do not mix and form a separate layer", ["yes, all liquids mix", "only coloured liquids mix", "no liquid mixes with water"], "Vinegar and lemon juice mix with water."),
       ("Which gases dissolve a little in water?", "oxygen and carbon dioxide", ["no gas dissolves in water", "only helium", "only neon"], "Fish use the oxygen dissolved in water."),
       ("Why does an oil drop float on water?", "oil is lighter than water and does not mix with it", ["oil is heavier than water", "oil dissolves in water", "oil is a solid"], "It forms a layer on top."),
       ("Which of these objects is made of more than one material?", "a pencil (wood and graphite)", ["a glass marble", "a gold ring", "an iron nail"], "Many objects use several materials."),
       ("What is the difference between an object and a material?", "an object is a thing; a material is what it is made of", ["they mean the same", "a material is always a metal", "an object is always made of wood"], "A spoon is an object; steel is a material."),
       ("Which property helps us choose material for a pressure cooker gasket?", "it is soft and flexible like rubber", ["it is transparent", "it is lustrous", "it is soluble"], "Rubber seals the lid."),
       ("Why are school bags often made of nylon or canvas?", "they are strong and light", ["they are transparent", "they dissolve in rain", "they are very heavy"], "They can carry books without tearing."),
       ("Why are electric wires covered with plastic?", "plastic does not let electricity pass through it", ["plastic is shiny", "plastic is a metal", "plastic dissolves in water"], "It keeps us safe from shocks."),
       ("Why do metals look dull after some time?", "air and moisture form a layer on their surface", ["they become wood", "they dissolve", "they turn into plastic"], "Scratching shows the shine again."),
       ("Why are bells made of metal?", "metals make a ringing sound when struck", ["metals are transparent", "metals are soft", "metals float"], "Metals are called sonorous."),
       ("Why is cotton used for summer clothes?", "it is soft and absorbs sweat", ["it is shiny", "it is waterproof", "it is magnetic"], "Wool keeps us warm in winter."),
       ("Why are ice and wood able to float?", "they are lighter than the same volume of water", ["they are heavier than water", "they dissolve in water", "they are metals"], "A stone is heavier than the same volume of water."),
       ("Why is a steel spoon used to stir hot tea, but with care?", "steel is strong but gets hot because it lets heat through", ["steel melts in tea", "steel is soft", "steel dissolves in tea"], "Metals conduct heat."),
       ("What do we call materials that let heat pass easily?", "good conductors of heat", ["insulators", "opaque materials", "soluble materials"], "Metals are good conductors."),
       ("Which property makes glass a poor choice for a football?", "it is hard and breaks easily", ["it is soft", "it is soluble", "it is opaque"], "Footballs are made of leather or rubber."),
       ("Which would you choose to make a box to hold water?", "plastic or metal, which do not soak up water", ["paper", "cardboard", "cloth"], "Paper and cardboard soak up water.")]


def UNITS6a():
    b = {k: once_maker(v) for k, v in [("sci", SCI1), ("div", DIV), ("eat", EAT), ("mag", MAG), ("len", LEN), ("use", USE)]}
    steps = pairs(STEPS, "Which step of finding out is %s?", None)
    steps2 = pairs([(b_, a_) for a_, b_ in STEPS], "What is a scientist doing when %s?", None)
    scen = pairs(SCEN, "Which step of finding out is shown here? <i>%s</i>")
    obs = odd_one(OBS, "Which of these is %s?", "Which of these is not %s?")
    tools = pairs(TOOLS, "What is %s used for?", "Which instrument would you use for %s?")
    plants = odd_one(PLANTS, "Which of these plants is %s?", "Which of these plants is not %s?")
    pl = pairs(PL, "What is meant by %s?", "What do we call %s?")
    roots = odd_one(ROOTS, "Which of these is %s?", "Which of these is not %s?")
    animg = odd_one(ANIMG, "Which of these is %s?", "Which of these is not %s?")
    nutr = pairs(NUTR, "What is the main role of %s in our body?", "Which nutrient is mainly needed for %s?")
    src = odd_one(SRC, "Which of these foods is %s?", "Which of these foods is not %s?")
    magm = odd_one(MAGM, "Which of these is %s?", "Which of these is not %s?")
    mot = odd_one(MOT, "Which of these is an example of %s?", "Which of these is not an example of %s?")
    prop = odd_one(PROP, "Which of these is %s?", "Which of these is not %s?")
    sol = odd_one(SOL, "Which of these is %s?", "Which of these is not %s?")
    flo = odd_one(FLOAT, "Which of these is %s?", "Which of these is not %s?")
    lus = odd_one(LUS, "Which of these is %s?", "Which of these is not %s?")
    return [
        U(1, "the-wonderful-world-of-science", 1, NS,
          "Science as a way of finding out: curiosity, observing, asking questions, making predictions, testing them through experiments, recording results and drawing conclusions (summary of NCERT Curiosity Chapter 1).",
          "The Wonderful World of Science", "the wonderful world of science",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 1: how scientists find out, observations and questions, predictions, fair tests and scientific instruments. 100 questions with answers.",
          "Science is a way of finding out.", "Observe, ask, predict, test, conclude.",
          "<p>Science begins with curiosity. We observe carefully, ask a question, make a sensible guess (a prediction), test it with an experiment, record the results and draw a conclusion. Then we share what we found so that others can check it.</p>"
          "<p>In a fair test we change only one thing and keep everything else the same, so we know what caused the result. Instruments such as a thermometer, a stopwatch and a magnifying glass help us observe and measure.</p>",
          [("Two pots of seeds: one in the dark, one in the light. What is changed?", ["only the light is different"], "the amount of light"), ("'The ice melted in 10 minutes' is…", ["something we noticed"], "an observation")],
          ["Changing two things at once in a test.", "Mixing up an observation with a guess.", "Changing the result when it does not match the prediction."],
          [("What is a fair test?", "A test in which only one thing is changed and everything else is kept the same."),
           ("What is the difference between an observation and a prediction?", "An observation is what we notice now; a prediction is a guess about what will happen.")],
          lambda: [("Steps of finding out", [(steps, 5), (steps2, 5), (scen, 10)]), ("Observations, questions and predictions", [(obs, 14), (b["sci"], 6)]),
                   ("Fair tests", [(c_fair, 20)]), ("Tools of science", [(tools, 14), (b["sci"], 6)]),
                   ("Mixed problems", [(obs, 6), (c_fair, 6), (b["sci"], 6), (tools, 2)])]),
        U(2, "diversity-in-the-living-world", 2, LW,
          "Diversity in plants and animals; grouping plants as herbs, shrubs, trees, climbers and creepers; leaf venation and types of roots; habitats and adaptations of animals and plants; conserving biodiversity (summary of NCERT Curiosity Chapter 2).",
          "Diversity in the Living World", "diversity in the living world",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 2: herbs, shrubs, trees, climbers and creepers, leaf venation and roots, habitats and adaptations, and biodiversity. 100 questions with answers.",
          "Living things are grouped by their features.", "Parallel veins go with fibrous roots; net-like veins with a taproot.",
          "<p>Plants can be grouped by their stems: herbs have soft green stems, shrubs have woody stems branching near the ground, trees have a thick trunk, and climbers and creepers have weak stems. Leaves with net-like (reticulate) venation usually go with a taproot; leaves with parallel venation go with fibrous roots.</p>"
          "<p>Animals and plants have adaptations that help them live in their habitats: a camel in the desert, a fish in water, a yak in cold mountains. The great variety of life is called biodiversity, and we must protect it.</p>",
          [("Wheat leaves have parallel veins. Which roots?", ["parallel venation goes with fibrous roots"], "fibrous roots"), ("A rose plant has a woody stem branching near the ground. It is…", ["medium-sized, woody"], "a shrub")],
          ["Calling a weak-stemmed plant that climbs a creeper.", "Thinking all plants have a taproot.", "Calling a dolphin a fish."],
          [("What is the difference between a climber and a creeper?", "Both have weak stems; a climber climbs up a support, while a creeper spreads along the ground."),
           ("Why does a camel have long legs?", "They keep its body away from the hot desert sand.")],
          lambda: [("Herbs, shrubs, trees, climbers and creepers", [(plants, 14), (pl, 6)]), ("Leaves and roots", [(roots, 12), (pl, 8)]), ("Habitats and adaptations", [(c_hab, 14), (animg, 6)]),
                   ("Biodiversity", [(b["div"], 12), (animg, 8)]), ("Mixed problems", [(plants, 10), (roots, 4), (c_hab, 4), (b["div"], 2)])]),
        U(3, "mindful-eating-a-path-to-healthy-body", 3, LW,
          "Food and its components: carbohydrates, proteins, fats, vitamins, minerals, dietary fibre and water; testing foods for starch, protein and fat; deficiency diseases; balanced diet, millets and regional food habits; mindful eating (summary of NCERT Curiosity Chapter 3).",
          "Mindful Eating: A Path to Healthy Body", "mindful eating",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 3: nutrients and their sources, food tests for starch, protein and fat, deficiency diseases, millets and a balanced diet. 100 questions with answers.",
          "A balanced diet has all the nutrients.", "Iodine turns starch blue-black.",
          "<p>Our food contains nutrients: carbohydrates and fats give energy, proteins build and repair the body, and vitamins and minerals keep us healthy. Dietary fibre and water do not give energy, but we need them too. A balanced diet has all of these in the right amounts.</p>"
          "<p>We can test foods: iodine solution turns starch blue-black, copper sulphate with sodium hydroxide turns protein violet, and fat leaves an oily patch on paper. A long lack of a nutrient causes a deficiency disease, such as scurvy (vitamin C) or anaemia (iron).</p>",
          [("A potato slice turns blue-black with iodine. Which nutrient?", ["iodine tests for starch"], "starch (a carbohydrate)"), ("Bleeding gums: which vitamin is lacking?", ["scurvy"], "vitamin C")],
          ["Thinking fibre gives energy.", "Mixing up the tests for starch and protein.", "Saying rickets is caused by a lack of vitamin C."],
          [("Why are millets good for us?", "They are rich in fibre, minerals such as calcium and iron, and vitamins, and they grow with little water."),
           ("What is a deficiency disease?", "A disease caused by the lack of a nutrient in the diet over a long time, such as scurvy, rickets or goitre.")],
          lambda: [("Nutrients and their roles", [(nutr, 10), (b["eat"], 10)]), ("Foods rich in each nutrient", [(src, 16), (b["eat"], 4)]), ("Testing food", [(K(c_test, "sign"), 7), (K(c_test, "how"), 6), (K(c_test, "what"), 7)]),
                   ("Deficiency diseases", [(c_def, 12), (b["eat"], 8)]), ("Mixed problems", [(src, 12), (c_test, 8)])]),
        U(4, "exploring-magnets", 4, PH,
          "Magnetic and non-magnetic materials; poles of a magnet; attraction and repulsion; finding directions with a freely suspended magnet and a compass; making a magnet; care of magnets (summary of NCERT Curiosity Chapter 4).",
          "Exploring Magnets", "exploring magnets",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 4: magnetic and non-magnetic materials, the poles of a magnet, attraction and repulsion, the compass, making magnets and storing them. 100 questions with answers.",
          "Like poles repel; unlike poles attract.", "A freely hanging magnet points north–south.",
          "<p>A magnet attracts magnetic materials such as iron, nickel and cobalt, but not wood, plastic, glass, copper or aluminium. Its attraction is strongest at its two poles. A freely hanging magnet always comes to rest pointing north–south; a compass uses this to show directions.</p>"
          "<p>Like poles repel and unlike poles attract, so repulsion is the surest test of a magnet. An iron nail can be made into a magnet by stroking it in one direction with a magnet. Heating, hammering and dropping make magnets weak, so store them in pairs with keepers.</p>",
          [("North pole near north pole?", ["like poles"], "they repel"), ("Is a copper wire attracted by a magnet?", ["copper is not magnetic"], "no")],
          ["Thinking a magnet attracts all metals.", "Thinking attraction proves an object is a magnet.", "Saying a broken magnet has only one pole in each piece."],
          [("Why is repulsion a sure test for a magnet?", "Iron is attracted to a magnet too, but only another magnet can be repelled by it."),
           ("How does a compass work?", "Its needle is a small magnet that turns freely and comes to rest pointing north–south.")],
          lambda: [("Magnetic and non-magnetic materials", [(magm, 16), (b["mag"], 4)]), ("Poles of a magnet", [(c_pole, 10), (c_pole2, 10)]), ("Finding directions", [(c_dir, 8), (b["mag"], 6), (magm, 6)]),
                   ("Making and storing magnets", [(b["mag"], 12), (magm, 4), (c_pole2, 4)]), ("Mixed problems", [(magm, 8), (c_pole, 6), (c_pole2, 4), (b["mag"], 2)])]),
        U(5, "measurement-of-length-and-motion", 5, PH,
          "Need for standard units of measurement; SI unit of length; correct way of measuring length with a scale; measuring curved lines; motion and rest, reference point; linear, circular and oscillatory (periodic) motion (summary of NCERT Curiosity Chapter 5).",
          "Measurement of Length and Motion", "measurement of length and motion",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 5: standard units, converting mm, cm, m and km, measuring with a scale, rest and motion, and linear, circular and oscillatory motion. 100 questions with answers.",
          "The SI unit of length is the metre.", "1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm.",
          "<p>Handspans and cubits are different for different people, so we use standard units. The SI unit of length is the metre (m): 1 km = 1000 m, 1 m = 100 cm and 1 cm = 10 mm. Read a scale with your eye straight above the mark; if the zero is broken, start from another mark and subtract.</p>"
          "<p>An object is in motion if its position changes with time compared to a reference point. Motion along a straight line is linear (rectilinear), motion along a circle is circular, and to-and-fro motion is oscillatory. Motion that repeats after equal times is periodic.</p>",
          [("Convert 3.5 m into cm.", ["1 m = 100 cm", "3.5 × 100"], "350 cm"), ("A swing moving to and fro shows…", ["back and forth about a point"], "oscillatory motion")],
          ["Multiplying when converting a small unit to a bigger one.", "Reading a scale from an angle.", "Forgetting to subtract the starting mark."],
          [("Why do we need standard units?", "So that everybody gets the same result when measuring the same object."),
           ("What is the difference between circular and oscillatory motion?", "In circular motion an object moves along a circle; in oscillatory motion it moves to and fro about a fixed position.")],
          lambda: [("Units and conversions", [(c_conv, 14), (b["len"], 6)]), ("Measuring with a scale", [(c_scale, 10), (c_span, 4), (b["len"], 6)]), ("Rest and motion", [(b["len"], 6), (mot, 14)]),
                   ("Types of motion", [(mot, 14), (c_conv, 6)]), ("Mixed problems", [(c_conv, 8), (c_scale, 6), (c_span, 2), (mot, 4)])]),
        U(6, "materials-around-us", 6, MT,
          "Objects and the materials they are made of; properties of materials: appearance (lustre), hardness, solubility in water, floating and sinking, transparency; grouping materials by their properties and choosing them for use (summary of NCERT Curiosity Chapter 6).",
          "Materials Around Us", "materials around us",
          "Free CBSE Class 6 Science worksheets for NCERT Curiosity Chapter 6: objects and materials, lustre, hardness, soluble and insoluble substances, floating and sinking, and transparent, translucent and opaque materials. 100 questions with answers.",
          "We choose materials by their properties.", "Transparent, translucent or opaque.",
          "<p>Objects are made of materials such as wood, glass, metal, plastic and cloth. Materials have properties: metals are lustrous (shiny), iron is hard and a sponge is soft, salt and sugar are soluble in water while sand and chalk are insoluble, and a cork floats while a stone sinks.</p>"
          "<p>We can see clearly through transparent materials (glass), partly through translucent materials (butter paper) and not at all through opaque materials (wood). We group materials by these properties and choose the right one for each use.</p>",
          [("Can you see clearly through butter paper?", ["you can see a little"], "no: it is translucent"), ("Does chalk powder dissolve in water?", ["it settles"], "no: it is insoluble")],
          ["Calling translucent materials transparent.", "Thinking all metals are soft.", "Thinking heavy objects always sink."],
          [("What is the difference between transparent and translucent?", "Through a transparent material we see clearly; through a translucent material we see only partly."),
           ("Why are cooking pots made of metal?", "Metals let heat pass easily; their handles are made of plastic or wood, which do not.")],
          lambda: [("Objects and materials", [(b["use"], 10), (lus, 10)]), ("Transparent, translucent and opaque", [(prop, 18), (b["use"], 2)]), ("Soluble and insoluble", [(sol, 16), (b["use"], 4)]),
                   ("Floating and sinking", [(flo, 16), (lus, 4)]), ("Mixed problems", [(prop, 4), (sol, 6), (flo, 4), (lus, 4), (b["use"], 2)])]),
    ]
