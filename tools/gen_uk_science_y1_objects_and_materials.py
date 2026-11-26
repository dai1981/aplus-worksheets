# -*- coding: utf-8 -*-
"""
UK Year 1 science: Objects and Materials (Everyday materials)
  python tools/gen_uk_science_y1_objects_and_materials.py
Distinguish between an object and the material from which it is made; identify and name a variety of everyday
materials (wood, plastic, glass, metal, water and rock); one object made from different materials; and a table of
classroom objects and their materials. Reuses the "what is it made of" question of the Year 2 unit (new seed).
Wrong answers come from real mistakes: "a chair is a material", "glass and plastic are the same", "metal is only for
coins", "an object can only be made of one material".
"""
import uk_sci
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import gen_uk_science_y2_uses_of_everyday_materials as M2
import sci_kids as K

M2.U = Unit(61109)
M2.R = M2.U.R
M2.P = People(M2.R)
uk_sci.USED.clear()
U, R, P = M2.U, M2.R, M2.P

OBJS = ["a spoon", "a chair", "a window", "a cup", "a coat", "a bottle", "a door", "a book", "a key", "a ball", "a sock", "a table"]
MATS = ["wood", "metal", "glass", "plastic", "rock", "water", "fabric", "paper", "rubber", "wool"]


def g_om():
    k = R.random() < 0.5
    x = R.choice(OBJS if k else MATS)
    if not once(("om", x)):
        return None
    return item("Is %s an object or a material?" % x, "an object" if k else "a material", ["a material" if k else "an object", "an animal", "a plant"],
                "An object is a thing. A material is what the thing is made of.")


def g_pick():
    k = R.random() < 0.5
    pool, other = (MATS, OBJS) if k else (OBJS, MATS)
    a = R.choice(pool)
    if not once(("pk", a)):
        return None
    w = R.sample(other, 3)
    o = sorted([a] + w)
    return item("Which of these is %s: %s or %s?" % ("a material" if k else "an object", ", ".join(o[:3]), o[3]), a, w, "Objects are things; materials are what they are made of.")


MADE = {"wood": ["a pencil", "a wooden spoon", "a door", "a table", "a ruler", "a fence"], "metal": ["a key", "a coin", "a saucepan", "a paperclip", "a fork", "a bike frame"],
        "glass": ["a window", "a jar", "a mirror", "a vase", "a drinking glass"], "plastic": ["a lunchbox", "a toy brick", "a bucket", "a drinks bottle", "a comb"],
        "fabric": ["a T-shirt", "a curtain", "a sock", "a pillowcase"], "rock": ["a pebble", "a stone wall", "a gravestone"], "paper": ["a book", "a birthday card", "a newspaper"]}


def g_which():
    m = R.choice(sorted(MADE))
    a = R.choice(MADE[m])
    if not once(("wh", a)):
        return None
    w = R.sample([x for mm in MADE if mm != m for x in MADE[mm]], 3)
    o = sorted([a] + w)
    return item("Which of these is usually made of %s: %s or %s?" % (m, ", ".join(o[:3]), o[3]), a, w, "Think about what each object is made of.")


def g_table():
    who = P.next()[0]
    m = R.choice(["wood", "metal", "plastic", "glass"])
    rows = []
    for mm in R.sample(sorted(MADE), 4):
        rows += [(x, mm) for x in R.sample(MADE[mm], min(2, len(MADE[mm])))]
    R.shuffle(rows)
    rows = rows[:6]
    n = sum(1 for _, mm in rows if mm == m)
    if n == 0 or not once(("tb", tuple(r[0] for r in rows), m)):
        return None
    tab = table(["Object", "Material"], [[o, mm] for o, mm in rows])
    g = str(n)
    return item(tab + "%s made a table of objects in the classroom. How many objects are made of %s?" % (who, m), g, [str(x) for x in range(5) if x != n][:3],
                "Count the rows that say %s." % m)


MULTI = [("a spoon", "metal, plastic or wood"), ("a cup", "glass, plastic or china"), ("a chair", "wood, metal or plastic"), ("a ball", "rubber, plastic or leather"),
         ("a bag", "fabric, paper or plastic"), ("a toy car", "metal or plastic")]


def g_multi():
    o, mats = R.choice(MULTI)
    if not once(("mu", o)):
        return None
    return item("%s can be made of different materials. Which list is right for %s?" % (o[0].upper() + o[1:], o), mats,
                R.sample([x[1] for x in MULTI if x[1] != mats], 2) + ["only one material, always"], "The same kind of object can be made from different materials.")


B1 = bank([
    ("What is a material?", "what an object is made of", ["the name of an object", "the colour of an object", "a kind of animal"], "Wood, metal, glass, plastic."),
    ("What is an object?", "a thing, such as a cup, a chair or a book", ["what a thing is made of", "a colour", "a sound"], "A cup is an object."),
    ("A cup is made of glass. Which word is the material?", "glass", ["cup", "drink", "table"], "Glass is the material."),
    ("A chair is made of wood. Which word is the object?", "chair", ["wood", "tree", "brown"], "The chair is the object."),
    ("Which material comes from trees?", "wood", ["metal", "glass", "plastic"], "Trees are cut into wood."),
    ("Which material is water?", "a liquid material", ["an object", "a kind of metal", "a kind of rock"], "Water is a material too."),
    ("Which of these is a natural material?", "rock", ["plastic", "glass", "metal foil"], "Rock comes from the ground."),
    ("Is glass the same as plastic?", "No. They are different materials, although both can be see-through.", ["Yes, exactly the same.", "Yes, glass is soft plastic.", "No, glass is a metal."], "Different materials."),
])
B5 = bank([
    ("Can an object be made of more than one material?", "Yes. A pencil is made of wood and graphite, with a rubber on the end.", ["No, never.", "Only toys.", "Only cars."], "Many objects use several materials."),
    ("How could you sort the objects in your classroom?", "into groups by the material they are made of", ["by how much they cost", "by who brought them", "by the day of the week"], "Classify."),
    ("Why are windows made of glass and not wood?", "Glass lets light through so we can see out.", ["Glass is softer.", "Wood is see-through.", "Glass is cheaper than air."], "Materials suit jobs."),
    ("A coin is made of metal. Is the coin a material?", "No. The coin is an object; metal is its material.", ["Yes, coins are materials.", "Yes, metal is the object.", "Neither is a material."], "Object and material."),
    ("How could you find out what material a spoon is made of?", "Look at it and feel it carefully.", ["Taste it.", "Throw it.", "Guess without looking."], "Observe."),
])


def body():
    pic = K.row(["spoon", "glass", "block"], words=["metal spoon", "glass window", "wooden block"], size=90, label="a metal spoon, a glass window and a wooden block")
    ex = [("Spoon: object or material?", ["It is a thing"], "an object"),
          ("A window is made of?", ["See-through"], "glass")]
    mist = ["Thinking a chair is a material.", "Thinking glass and plastic are the same.", "Thinking an object can only be made of one material."]
    return kid_lesson(pic, "Objects are made of materials.",
                      ["A spoon is an object. Metal is its material.", "Wood, metal, glass, plastic, rock and water are materials.", "One kind of object can be made of different materials."], ex, mist)


def main():
    sets = U.sets([
        ("Object or material?", B1 + [(g_om, 12)]),
        ("Naming materials", [(g_pick, 12), (g_om, 4), (M2.g_mat, 4)]),
        ("What is it made of?", [(M2.g_mat, 10), (g_which, 10)]),
        ("Classroom table", [(g_table, 14), (g_multi, 6)]),
        ("Thinking about materials", B5 + [(g_table, 9), (g_which, 6)]),
    ])
    make_uk(1, "objects-and-materials", 9, "Everyday materials",
            "Distinguish between an object and the material from which it is made. Identify and name a variety of everyday materials, including wood, plastic, glass, metal, water, and rock.",
            "Objects and Materials",
            "Year 1 Science: Objects and Materials Worksheets (Wood, Metal, Plastic, Glass)",
            "Objects and Materials",
            "Free Year 1 science worksheets on objects and materials: telling an object from its material, naming wood, plastic, glass, metal, water and rock, and sorting objects. 100 questions with answers.",
            "Objects are made of materials.",
            "A spoon is an object; metal is its material.",
            body(),
            [("What is the difference between an object and a material?", "An object is a thing, like a spoon or a chair. A material is what it is made of, like metal or wood."),
             ("What everyday materials should Year 1 know?", "Wood, plastic, glass, metal, water and rock, and also fabric, paper and rubber."),
             ("Can one object be made of different materials?", "Yes. A spoon can be metal, plastic or wood, and a pencil uses wood, graphite and rubber.")],
            sets)


if __name__ == "__main__":
    main()
