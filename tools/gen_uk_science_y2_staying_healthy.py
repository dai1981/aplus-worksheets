# -*- coding: utf-8 -*-
"""
UK Year 2 science: Staying Healthy (Animals, including humans)
  python tools/gen_uk_science_y2_staying_healthy.py
Describe the importance for humans of exercise, eating the right amounts of different types of food, and hygiene:
healthier food choices, what counts as exercise and what it does to the body (a heartbeat table), and when and why
to wash our hands.
Wrong answers come from real mistakes: "healthy means never eating treats", "sitting still is exercise",
"water alone washes germs away", "you only need to wash hands if they look dirty".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K
from sci_phys import uniq

U = Unit(61209)
R = U.R
P = People(R)

PAIR = [("an apple", "a chocolate bar"), ("a glass of water", "a can of cola"), ("carrot sticks", "a bag of crisps"), ("a banana", "a doughnut"),
        ("a wholemeal sandwich", "a cream cake"), ("a handful of grapes", "a packet of sweets"), ("plain yoghurt with fruit", "an ice lolly"),
        ("a glass of milk", "a milkshake with whipped cream"), ("a pear", "a muffin"), ("cucumber slices", "a sausage roll"),
        ("a boiled egg", "a packet of biscuits"), ("a satsuma", "a lollipop"), ("baked beans on toast", "a large bag of chips"),
        ("a bowl of porridge", "a sugary cereal bar"), ("strawberries", "a slice of cake"), ("vegetable soup", "a fizzy energy drink")]


def g_choice():
    a, b = R.choice(PAIR)
    if not once(("ch", a)):
        return None
    o = [a, b] if R.random() < 0.5 else [b, a]
    return item("Which is the healthier choice: %s or %s?" % tuple(o), a, [b, "They are both equally healthy.", "Neither, we should not eat."],
                "Fruit, vegetables and water are healthy choices; sugary or fatty treats are fine only now and then.")


EX = [("running in the park", True), ("swimming", True), ("riding a bike", True), ("dancing", True), ("skipping", True), ("playing football", True),
      ("climbing on a climbing frame", True), ("walking to school", True), ("watching television", False), ("sleeping", False),
      ("sitting playing a video game", False), ("reading a book on the sofa", False), ("eating lunch", False), ("doing a jigsaw at a table", False)]


def g_exer():
    a, y = R.choice(EX)
    if not once(("ex", a)):
        return None
    return item("Is %s exercise?" % a, "Yes, it gets your body moving." if y else "No, your body is not moving much.",
                ["No, your body is not moving much." if y else "Yes, it gets your body moving.", "Only if you do it at night.", "Only grown-ups can exercise."],
                "Exercise means moving your body, like running, swimming or dancing.")


BODY = [("What happens to your heart when you exercise?", "It beats faster.", ["It stops.", "It beats slower.", "Nothing happens."]),
        ("What happens to your breathing when you run?", "You breathe faster and deeper.", ["You stop breathing.", "You breathe slower.", "Nothing changes."]),
        ("Why do you get hot when you exercise?", "Your muscles are working hard and make heat.", ["The sun comes closer.", "Your clothes shrink.", "Exercise is cold."]),
        ("What does regular exercise do to your muscles?", "It makes them stronger.", ["It makes them weaker.", "It turns them to bone.", "Nothing."]),
        ("Why do you sweat when you exercise a lot?", "Sweat helps to cool your body down.", ["Sweat makes you hotter.", "Your body is crying.", "It is raining inside you."]),
        ("How much exercise should children do each day?", "about an hour", ["none at all", "one minute", "ten hours"])]


def g_body():
    q, a, w = R.choice(BODY)
    if not once(("bo", q)):
        return None
    return item(q, a, w, "Exercise keeps your heart, lungs and muscles healthy.")


WHEN = [("before eating", "Germs on your hands could get into your food and make you ill."), ("after using the toilet", "Germs from the toilet can spread illness."),
        ("after stroking a pet", "Pets can carry germs on their fur."), ("after playing outside in the mud", "Soil can have germs in it."),
        ("after blowing your nose", "Germs from a cold could spread to other people."), ("before helping to cook", "Clean hands keep germs out of the food."),
        ("after touching raw meat", "Raw meat can carry germs."), ("after cleaning out the class hamster's cage", "Animal waste carries germs.")]


def g_hyg():
    w, why = R.choice(WHEN)
    k = R.random() < 0.5
    if not once(("hy", w, k)):
        return None
    if k:
        return item("Should you wash your hands %s?" % w, "Yes, always.", ["No, only if they look dirty.", "No, never.", "Only on Fridays."], why)
    return item("Why should you wash your hands %s?" % w, why, R.sample([x[1] for x in WHEN if x[1] != why], 2) + ["It makes your hands grow."], "Washing with soap removes germs.")


ACT = ["sitting still", "walking", "jogging", "doing star jumps"]


def g_pulse():
    who = P.next()[0]
    base = R.choice([40, 42, 44, 45])
    v = [base, base + R.choice([5, 6, 8]), base + R.choice([20, 22, 25]), base + R.choice([35, 38, 40])]
    k = R.choice(["read", "read", "most", "least", "diff", "pattern"])
    ri = R.randrange(4)
    if not once(("pu", tuple(v), k, ri if k == "read" else 0)) or (k == "pattern" and not once(("pp",), 2)):
        return None
    tab = table(["Activity for 1 minute", "Heartbeats counted in 30 seconds"], [[a, str(x)] for a, x in zip(ACT, v)])
    intro = tab + "%s counted heartbeats after different activities. " % who
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many heartbeats were counted after %s?" % ACT[ri], g, uniq(g, [str(x) for x in v] + [str(v[ri] + 3)]), "Read the row.")
    if k == "most":
        return item(intro + "After which activity was the heart beating fastest?", "doing star jumps", [x for x in ACT if x != "doing star jumps"], "The biggest number.")
    if k == "least":
        return item(intro + "After which activity was the heart beating slowest?", "sitting still", [x for x in ACT if x != "sitting still"], "The smallest number.")
    if k == "diff":
        d = v[3] - v[0]
        g = str(d)
        return item(intro + "How many more heartbeats were counted after star jumps than after sitting still?", g, uniq(g, [str(v[3]), str(v[0]), str(v[3] + v[0]), str(d + 2)]),
                    "%d − %d = %d." % (v[3], v[0], d))
    return item(intro + "What do the results show?", "The harder the exercise, the faster the heart beats.", ["The heart beats slower after exercise.", "Exercise makes no difference.", "Sitting still makes the heart beat fastest."],
                "The numbers go up as the activity gets harder.")


B1 = bank([
    ("What helps us stay healthy?", "exercise, healthy food and keeping clean", ["sweets every day", "staying up all night", "never washing"], "Three big habits."),
    ("How many portions of fruit and vegetables should we try to eat each day?", "at least 5", ["none", "1 a week", "only on birthdays"], "5 a day."),
    ("Is it all right to have a treat like cake sometimes?", "Yes, sometimes, as long as we mostly eat healthy food.", ["No, never.", "Yes, for every meal.", "Only cake is healthy."], "Balance."),
    ("What is the best drink to have with meals?", "water", ["cola", "an energy drink", "a milkshake every time"], "Water keeps you healthy."),
    ("Why should we eat different kinds of food?", "Different foods help our bodies in different ways.", ["So we get bored.", "All foods are the same.", "Only one food is needed."], "Variety."),
    ("What can happen if you eat too much sugar?", "It can harm your teeth and make you unhealthy.", ["It makes your teeth stronger.", "It makes you taller.", "Nothing at all."], "Not too much."),
    ("How long should you wash your hands for?", "about 20 seconds, with soap", ["one second", "only with cold water", "you do not need to"], "Sing 'Happy Birthday' twice."),
    ("Why do we need sleep?", "It helps our bodies rest and grow.", ["It makes us hungry.", "It stops us growing.", "We do not need sleep."], "About 10 hours for children."),
])
B3 = bank([
    ("What are germs?", "tiny living things that can make us ill", ["a kind of food", "dirt you can always see", "a kind of soap"], "Too small to see."),
    ("Why do we use soap when washing our hands?", "Soap helps to wash germs away.", ["Soap makes germs grow.", "Soap is food for skin.", "Water alone is always enough."], "Soap and water."),
    ("Why should you cover your mouth when you cough or sneeze?", "to stop germs spreading to other people", ["to keep your mouth warm", "to make the sneeze louder", "there is no reason"], "Catch it in a tissue."),
    ("Why should you brush your teeth twice a day?", "to keep them clean and stop tooth decay", ["to make them grow faster", "to make them yellow", "it does not matter"], "Morning and night."),
    ("Why should you have a bath or shower regularly?", "to keep your body clean and fresh", ["to get cold", "to make your hair grow", "it is not needed"], "Keeping clean."),
    ("Can germs be on your hands even if they look clean?", "Yes, germs are too small to see.", ["No, never.", "Only on Mondays.", "Only if your hands are red."], "Wash anyway."),
    ("What should you do with a used tissue?", "put it in the bin and wash your hands", ["put it in your pocket for later", "give it to a friend", "leave it on the table"], "Catch it, bin it, kill it."),
    ("Why should you not share a drinks bottle with a friend who has a cold?", "Germs can spread from their mouth to yours.", ["The drink will taste bad.", "Bottles break.", "It is always fine."], "Stop germs spreading."),
])
B5 = bank([
    ("Ruby ate crisps and sweets all day and did no exercise. What would be a healthier day?", "fruit, a balanced lunch, water and an hour of play outside", ["more crisps and a nap", "only sweets", "a day watching TV"], "Food, exercise, hygiene."),
    ("Why is it good to play outside every day?", "Moving about keeps your heart, lungs and muscles strong.", ["It makes you weaker.", "It is only for adults.", "It stops you growing."], "Exercise."),
    ("How could you find out if exercise makes your heart beat faster?", "Count your heartbeats before and after running on the spot.", ["Count them only once.", "Ask a friend to guess.", "Count your fingers."], "Compare before and after."),
    ("Why is a balanced lunchbox better than one full of sweets?", "It gives your body the different foods it needs.", ["Sweets give everything you need.", "It weighs more.", "It is more colourful."], "Right amounts of different foods."),
    ("Why do people wash their hands more often when lots of people have colds?", "to stop germs spreading", ["to warm them up", "to make the soap last longer", "colds come from soap"], "Hygiene protects others too."),
])


def body():
    pic = K.row(["apple", "ball", "drop"], words=["healthy food", "exercise", "clean hands"], size=90, label="healthy food, exercise and washing hands keep us healthy")
    ex = [("Apple or doughnut?", ["Fruit is healthy"], "an apple"),
          ("When should you wash your hands?", ["Germs and food"], "before eating")]
    mist = ["Thinking healthy means never eating any treats.", "Thinking sitting still is exercise.", "Thinking you only wash hands when they look dirty."]
    return kid_lesson(pic, "Exercise, healthy food and clean hands.",
                      ["Eat lots of fruit and vegetables; treats only sometimes.", "Move your body for about an hour a day.", "Wash your hands with soap to remove germs."], ex, mist)


def main():
    sets = U.sets([
        ("Healthy food", B1 + [(g_choice, 12)]),
        ("Exercise", [(g_exer, 10), (g_body, 6), (g_choice, 2), (g_pulse, 2)]),
        ("Keeping clean", B3 + [(g_hyg, 12)]),
        ("Heartbeat test", [(g_pulse, 20)]),
        ("Thinking about health", B5 + [(g_pulse, 9), (g_exer, 3), (g_hyg, 3)]),
    ])
    make_uk(2, "staying-healthy", 9, "Animals, including humans",
            "Describe the importance for humans of exercise, eating the right amounts of different types of food, and hygiene.",
            "Staying Healthy",
            "Year 2 Science: Staying Healthy Worksheets (Exercise, Food and Hygiene)",
            "Staying Healthy",
            "Free Year 2 science worksheets on staying healthy: healthy food choices, exercise and what it does to the heart, and washing hands to remove germs. 100 questions with answers.",
            "Exercise, healthy food, clean hands.",
            "Eat the right amounts of different foods, move every day and wash away germs.",
            body(),
            [("How can I stay healthy?", "Eat the right amounts of different foods, with plenty of fruit and vegetables, exercise every day, sleep well and keep clean."),
             ("What does exercise do to my body?", "It makes your heart beat faster and your breathing quicker. Over time it makes your heart, lungs and muscles stronger."),
             ("Why do we wash our hands?", "Hands can carry germs that are too small to see. Washing with soap for about 20 seconds removes them.")],
            sets)


if __name__ == "__main__":
    main()
