# -*- coding: utf-8 -*-
"""
UK Year 2 science: What Plants Need to Stay Healthy (Plants)
  python tools/gen_uk_science_y2_what_plants_need_to_stay_healthy.py
Find out and describe how plants need water, light and a suitable temperature to grow and stay healthy: spotting what
a plant is missing, too hot and too cold, and simple tests with plants in the light and the dark or with and without
water. Reuses the investigation and clue questions of the Year 3 unit (new seed) with Year 2 questions.
Wrong answers come from real mistakes: "plants grow best in the dark", "more water is always better", "plants do
not mind frost", "plants only need soil".
"""
import uk_sci
from uk_sci import Unit, item, bank, kid_lesson, make_uk, People, once
import gen_uk_science_y3_what_plants_need_to_grow as Y3
import sci_kids as K

Y3.U = Unit(61206)
Y3.R = Y3.U.R
Y3.P = People(Y3.R)
uk_sci.USED.clear()
U, R, P = Y3.U, Y3.R, Y3.P

NEED = ["water", "light", "warmth"]
NOT = ["sweets", "music", "a blanket", "fizzy drinks", "sugar", "chocolate", "plastic", "toys", "salt"]


def g_need():
    a = R.choice(NEED)
    w = R.sample(NOT, 3)
    if not once(("nd", a), 6):
        return None
    o = sorted([a] + w)
    return item("What does a plant need to grow well: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Plants need water, light and the right temperature.")


TEMP = [("A tomato plant is left outside on a frosty night.", "It is too cold, so its leaves may be damaged.", "cold"),
        ("A pot of cress is put in a warm, sunny classroom.", "It has warmth and light, so it grows well.", "good"),
        ("A plant is put right next to a hot radiator.", "It is too hot, so it dries out and wilts.", "hot"),
        ("Seeds are planted in a greenhouse in early spring.", "The greenhouse keeps them warm, so they grow sooner.", "good"),
        ("A basil plant is kept in the fridge.", "It is too cold, so it stops growing and goes black.", "cold"),
        ("A sunflower grows outside in summer.", "It has warmth and light, so it grows tall.", "good")]
WRONG = {"cold": ["It is too hot, so it dries out and wilts.", "It has warmth and light, so it grows well.", "Nothing happens, because cold is good for plants."],
         "hot": ["It is too cold, so its leaves may be damaged.", "It has warmth and light, so it grows well.", "It grows faster, because plants love radiators."],
         "good": ["It is too cold, so its leaves may be damaged.", "It is too hot, so it dries out and wilts.", "It stops growing, because it has too much light."]}


def g_temp():
    s, a, kd = R.choice(TEMP)
    if not once(("te", s)):
        return None
    return item("%s What will happen?" % s, a, WRONG[kd], "Plants need a suitable temperature: not too hot and not too cold.")


SPOT = [("a sunflower that needs lots of sun", "a sunny spot in the garden"), ("a fern that likes shade", "a shady corner under a tree"),
        ("a cactus that likes dry soil", "a sunny windowsill, watered only now and then"), ("a water lily", "a pond"),
        ("tomato seedlings in early spring", "a warm greenhouse"), ("a pot of cress on a school trip day", "a light windowsill with a saucer of water"),
        ("a pot of basil", "a warm, light kitchen windowsill"), ("strawberry plants", "a sunny vegetable patch")]
BAD = ["a dark cupboard", "inside a fridge", "a cold, dark shed", "on top of a hot radiator", "a bucket with no soil or water", "under a heavy box"]


def g_place():
    p, a = R.choice(SPOT)
    if not once(("pl", p)):
        return None
    return item("Where is the best place to grow %s?" % p, a, R.sample(BAD, 3), "Put each plant where it gets the water, light and warmth it needs.")


B1 = bank([
    ("What three things do plants need to grow and stay healthy?", "water, light and a suitable temperature", ["sweets, toys and music", "only soil", "darkness and cold"], "Water, light, warmth."),
    ("What happens to a plant with no water?", "It wilts (droops) and can die.", ["It grows faster.", "It turns blue.", "Nothing happens."], "Plants need water."),
    ("What happens to a plant kept in the dark?", "It goes pale and weak.", ["It grows strong and green.", "It flowers more.", "Nothing changes."], "Plants need light."),
    ("Where is the best place for a pot plant in a classroom?", "near a window, where there is light", ["in a dark cupboard", "in the fridge", "under a desk in the corner"], "Light helps leaves."),
    ("Can a plant get too much water?", "Yes. Too much water can rot its roots.", ["No, never.", "Only in winter.", "Only cactuses get water."], "Not too much, not too little."),
    ("Why do plants grow faster in spring and summer?", "There is more light and it is warmer.", ["It is darker.", "There is snow.", "Plants like holidays."], "Light and warmth."),
    ("Which part of a plant takes in water?", "the roots", ["the flowers", "the leaves", "the petals"], "Water the soil."),
    ("What colour are healthy leaves on most plants?", "green", ["white", "black", "pale yellow"], "Pale leaves can mean too little light."),
])
B5 = bank([
    ("How could you test if cress needs light?", "Grow two pots the same, one in the light and one in the dark, and compare.", ["Grow one pot only.", "Put both in the dark.", "Give them different seeds."], "Fair test."),
    ("Why must both pots of cress get the same water in a light test?", "so the only thing that changes is the light", ["to make it quicker", "so they look the same", "it does not matter"], "Change one thing."),
    ("A plant's leaves are drooping and the soil is dry. What should you do?", "Water the soil.", ["Put it in the dark.", "Cut off the leaves.", "Put it in the fridge."], "Plants need water."),
    ("Why do gardeners cover young plants on frosty nights?", "to keep them warm enough", ["to keep them dark", "to stop them drinking", "to hide them from people"], "Suitable temperature."),
    ("Which plant will grow best: one in a sunny, warm window with water, or one in a cold, dark shed?", "the one in the sunny, warm window with water", ["the one in the cold, dark shed", "both the same", "neither will grow"], "Light, water, warmth."),
])


def body():
    pic = K.row(["drop", "sun", "hot"], words=["water", "light", "warmth"], size=90, label="a plant needs water, light and warmth")
    ex = [("Cress in a dark cupboard?", ["No light"], "pale and weak"),
          ("Tomato plant on a frosty night?", ["Too cold"], "its leaves may be damaged")]
    mist = ["Thinking plants grow best in the dark.", "Thinking more water is always better.", "Thinking plants do not mind frost."]
    return kid_lesson(pic, "Plants need water, light and warmth.",
                      ["No water: the plant wilts.", "No light: the plant goes pale and weak.", "Too hot or too cold: the plant is harmed."], ex, mist)


def main():
    sets = U.sets([
        ("What plants need", B1 + [(g_need, 12)]),
        ("Spot the problem", [(Y3.g_what, 9), (g_temp, 6), (g_need, 2), (Y3.g_amount, 3)]),
        ("Light and water tests", [(Y3.g_test, 20)]),
        ("Too much or too little", [(Y3.g_amount, 5), (Y3.g_test, 10), (Y3.g_what, 4), (g_need, 1)]),
        ("Thinking about plants", B5 + [(Y3.g_test, 6), (g_place, 8), (g_need, 1)]),
    ])
    make_uk(2, "what-plants-need-to-stay-healthy", 6, "Plants",
            "Find out and describe how plants need water, light and a suitable temperature to grow and stay healthy.",
            "What Plants Need to Stay Healthy",
            "Year 2 Science: What Plants Need Worksheets (Water, Light and Warmth)",
            "What Plants Need",
            "Free Year 2 science worksheets on what plants need to stay healthy: water, light and a suitable temperature, spotting problems and simple plant tests. 100 questions with answers.",
            "Water, light and warmth.",
            "Too little or too much water, light or warmth can harm a plant.",
            body(),
            [("What do plants need to stay healthy?", "Plants need water, light and a suitable temperature (not too hot and not too cold)."),
             ("What happens if a plant gets no light?", "It cannot make its food, so it grows pale, thin and weak."),
             ("How can I test what a plant needs?", "Grow two plants the same way, but change one thing, such as light. Then compare how they grow.")],
            sets)


if __name__ == "__main__":
    main()
