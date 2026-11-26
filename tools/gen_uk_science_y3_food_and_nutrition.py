# -*- coding: utf-8 -*-
"""
UK Year 3 science: Food and Nutrition (Animals, including humans)
  python tools/gen_uk_science_y3_food_and_nutrition.py
Animals, including humans, need the right types and amounts of nutrition and cannot make their own food; they get
nutrition from what they eat. Plants make their own food; carnivores, herbivores and omnivores; the Eatwell Guide food
groups; nutrients and their jobs; choosing a balanced lunch.
Reuses the nutrient questions of the Year 6 diet unit (new seed) and adds Year 3 questions.
Wrong answers come from real mistakes: "animals make food like plants", "one food has everything you need",
"fat is always bad", "a balanced meal means equal amounts of everything".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
import gen_uk_science_y6_diet_exercise_and_lifestyle as D6

D6.U = Unit(61305)
D6.R = D6.U.R
D6.P = People(D6.R)
uk_sci.USED.clear()
U, R, P = D6.U, D6.R, D6.P

MAKERS = ["an oak tree", "grass", "a sunflower", "a potato plant", "seaweed", "a daisy", "a cactus", "an apple tree", "moss"]
EATERS = ["a cat", "a human", "a rabbit", "a fox", "a cow", "a robin", "a goldfish", "a snail", "a frog", "a mouse"]


def g_who():
    if R.random() < 0.5:
        a = R.choice(MAKERS)
        w = R.sample(EATERS, 3)
        if not once(("wm", a)):
            return None
        o = sorted([a] + w)
        return item("Which of these can make its own food: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Plants make their own food using sunlight. Animals have to eat.")
    a = R.choice(EATERS)
    if not once(("we", a)):
        return None
    return item("How does %s get its food?" % a, "by eating plants or other animals", ["by making it from sunlight in its leaves", "by taking it in through roots", "it does not need food"],
                "Animals cannot make their own food.")


DIET = [("a rabbit", "grass, clover and dandelion leaves", "herbivore"), ("a cow", "grass and hay", "herbivore"), ("a sheep", "grass", "herbivore"),
        ("a caterpillar", "leaves", "herbivore"), ("a horse", "grass, hay and oats", "herbivore"), ("a giraffe", "leaves from tall trees", "herbivore"),
        ("a lion", "zebras and antelopes", "carnivore"), ("an owl", "mice and voles", "carnivore"), ("a shark", "fish and seals", "carnivore"),
        ("a spider", "flies and other insects", "carnivore"), ("a kestrel", "mice and small birds", "carnivore"), ("a cat", "meat and fish", "carnivore"),
        ("a badger", "worms, berries and roots", "omnivore"), ("a fox", "rabbits, mice, berries and scraps", "omnivore"), ("a hedgehog", "beetles, worms and berries", "omnivore"),
        ("a pig", "roots, plants and small animals", "omnivore"), ("a human", "fruit, vegetables, bread, meat and fish", "omnivore"), ("a brown bear", "fish, berries and honey", "omnivore")]
KIND = {"herbivore": "a herbivore (eats only plants)", "carnivore": "a carnivore (eats only animals)", "omnivore": "an omnivore (eats plants and animals)"}


def g_diet():
    a, f, k = R.choice(DIET)
    if not once(("di", a)):
        return None
    return item("%s eats %s. What kind of animal is it?" % (a[0].upper() + a[1:], f), KIND[k], [KIND[x] for x in sorted(KIND) if x != k] + ["a producer (makes its own food)"],
                "Herbivores eat plants, carnivores eat animals, omnivores eat both.")


EATWELL = {"fruit and vegetables": ["an apple", "a banana", "carrots", "peas", "broccoli", "a tomato", "grapes", "a pear"],
           "potatoes, bread, rice, pasta and other starchy foods": ["bread", "rice", "pasta", "a jacket potato", "porridge", "noodles", "a wrap"],
           "beans, pulses, fish, eggs, meat and other proteins": ["chicken", "baked beans", "an egg", "tuna", "lentils", "fish fingers", "lean mince"],
           "dairy and alternatives": ["milk", "cheese", "yoghurt", "soya milk", "fromage frais"],
           "oils and spreads": ["olive oil", "butter", "sunflower spread", "vegetable oil"]}
GROUPS = sorted(EATWELL)


def g_eatwell():
    gname = R.choice(GROUPS)
    f = R.choice(EATWELL[gname])
    if not once(("ew", f)):
        return None
    return item("In the Eatwell Guide, which food group does %s belong to?" % f, gname, R.sample([x for x in GROUPS if x != gname], 3), "The Eatwell Guide shows five main food groups.")


CARB = ["a cheese sandwich on wholemeal bread", "a tuna pasta salad", "a chicken wrap", "an egg and cress roll"]
FRUIT = ["an apple", "carrot sticks", "a satsuma", "a handful of grapes", "cucumber slices", "a banana"]
DRINK = ["a bottle of water", "a small carton of milk"]
JUNK = [["two bags of crisps", "a chocolate bar", "a can of cola"], ["a doughnut", "a packet of sweets", "a fizzy drink"],
        ["three biscuits", "a bag of crisps", "a cola"], ["a chocolate muffin", "a bag of sweets", "a can of lemonade"],
        ["an apple", "a banana", "a bunch of grapes"], ["a big bag of crisps", "a sausage roll", "a cola"]]


def g_plate():
    who = P.next()[0]
    good = [R.choice(CARB), R.choice(FRUIT), R.choice(DRINK)]
    bad = R.sample(JUNK, 3)
    boxes = [good] + bad
    R.shuffle(boxes)
    letters = "ABCD"
    ans = letters[boxes.index(good)]
    k = R.random() < 0.7
    if not once(("pl", tuple(good), k)):
        return None
    tab = table(["Lunchbox", "What is inside"], [[letters[i], ", ".join(b)] for i, b in enumerate(boxes)])
    if k:
        return item(tab + "%s is choosing a packed lunch. Which lunchbox is the most balanced?" % who, "Lunchbox " + ans, ["Lunchbox " + x for x in letters if x != ans],
                    "A balanced lunch has a starchy food, some protein, fruit or vegetables, and a healthy drink.")
    fb = [b for b in bad if b[0] == "an apple"]
    if not fb:
        return None
    a2 = letters[boxes.index(fb[0])]
    return item(tab + "%s is choosing a packed lunch. Which lunchbox has fruit but no starchy food or protein?" % who, "Lunchbox " + a2, ["Lunchbox " + x for x in letters if x != a2],
                "Fruit is healthy, but a meal also needs starchy food and protein.")


B1 = bank([
    ("Can animals make their own food?", "No. They must eat plants or other animals.", ["Yes, using sunlight.", "Yes, using their roots.", "Only at night."], "Only plants make their own food."),
    ("How do plants get their food?", "They make it in their leaves using sunlight.", ["They eat insects.", "They eat soil.", "People feed them."], "Plants are producers."),
    ("What is nutrition?", "the food and drink a living thing needs to stay healthy and grow", ["a kind of exercise", "a kind of medicine", "a type of plant"], "We get it from what we eat."),
    ("What is a herbivore?", "an animal that eats only plants", ["an animal that eats only meat", "an animal that eats plants and meat", "a plant that eats insects"], "Cows and rabbits."),
    ("What is a carnivore?", "an animal that eats only other animals", ["an animal that eats only plants", "a plant", "an animal that eats nothing"], "Lions and owls."),
    ("What is an omnivore?", "an animal that eats both plants and animals", ["an animal that eats only grass", "an animal that eats only meat", "an animal that never eats"], "Humans and badgers."),
    ("Why do we need food?", "for energy, to grow and to stay healthy", ["only to enjoy the taste", "only to keep warm", "we do not need food"], "Food gives nutrients."),
    ("Why should we eat lots of different foods?", "Different foods give us different nutrients.", ["All foods have the same nutrients.", "So we get bored less.", "It makes us grow horns."], "No one food has everything."),
])
B5 = bank([
    ("Is all fat bad for us?", "No. We need a small amount of fat to stay healthy.", ["Yes, we should never eat any fat.", "Yes, fat has no use.", "No, we should eat lots of fat."], "Small amounts."),
    ("Why do pet rabbits need fresh hay every day?", "They are herbivores and need plenty of plant food.", ["Rabbits eat meat.", "Hay is their bed only.", "Rabbits do not eat."], "Right food for the animal."),
    ("Why is it unhealthy to eat only chips and sweets?", "They do not give the body all the nutrients it needs.", ["They have too many vitamins.", "They are too healthy.", "They have no energy."], "Balance matters."),
    ("A footballer and a person sitting at a desk all day both eat. Who needs more food energy?", "the footballer", ["the person at the desk", "they need exactly the same", "neither needs any energy"], "More activity, more energy."),
    ("Why should a pet cat not be fed only on vegetables?", "Cats are carnivores and need nutrients from meat.", ["Cats are herbivores.", "Vegetables are poisonous to all animals.", "Cats do not need food."], "Different animals, different needs."),
])


def body():
    think = ("<p><b>Animals cannot make their own food. They get nutrition from what they eat.</b></p>"
             "<ul><li>Herbivores eat plants, carnivores eat animals, omnivores eat both. Humans are omnivores.</li>"
             "<li>Different foods give different nutrients. The Eatwell Guide shows how much of each food group to eat.</li>"
             "<li>A balanced diet has the right types and the right amounts of food.</li></ul>")
    ex = [("Can a rabbit make its own food?", ["It is an animal"], "No, it eats plants"),
          ("Pasta: which food group?", ["Starchy food"], "potatoes, bread, rice, pasta")]
    mist = ["Thinking animals make food like plants.", "Thinking one food has everything you need.", "Thinking fat is always bad."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Food for animals", B1 + [(g_who, 6), (g_diet, 6)]),
        ("Food groups", [(g_eatwell, 14), (D6.g_food, 6)]),
        ("Nutrients", [(D6.g_food, 10), (D6.g_job, 10)]),
        ("Balanced meals", [(g_plate, 12), (g_eatwell, 6), (D6.g_job, 2)]),
        ("Thinking about food", B5 + [(g_plate, 6), (g_diet, 6), (g_who, 3)]),
    ])
    make_uk(3, "food-and-nutrition", 5, "Animals, including humans",
            "Identify that animals, including humans, need the right types and amount of nutrition, and that they cannot make their own food; they get nutrition from what they eat.",
            "Food and Nutrition",
            "Year 3 Science: Food and Nutrition Worksheets (Balanced Diet and Food Groups)",
            "Food and Nutrition",
            "Free Year 3 science worksheets on food and nutrition: animals cannot make their own food, herbivores, carnivores and omnivores, the Eatwell Guide, nutrients and balanced meals. 100 questions with answers.",
            "Animals must eat to get nutrition.",
            "Eat the right types and amounts of food.",
            body(),
            [("Why can't animals make their own food?", "Only plants can make food using sunlight in their leaves. Animals must eat plants or other animals to get the nutrition they need."),
             ("What is a balanced diet?", "Eating the right types of food in the right amounts: plenty of fruit, vegetables and starchy foods, some protein and dairy, and only a little oil, fat and sugar."),
             ("What are the food groups?", "The Eatwell Guide has fruit and vegetables; potatoes, bread, rice and pasta; beans, fish, eggs and meat; dairy and alternatives; and oils and spreads.")],
            sets)


if __name__ == "__main__":
    main()
