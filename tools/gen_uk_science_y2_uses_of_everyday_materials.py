# -*- coding: utf-8 -*-
"""
UK Year 2 science: Uses of Everyday Materials (Uses of everyday materials)
  python tools/gen_uk_science_y2_uses_of_everyday_materials.py
Identify and compare the suitability of a variety of everyday materials (wood, metal, plastic, glass, brick, rock,
paper and cardboard) for particular uses: what things are made of, why a material is chosen, silly materials for a
job, the same material for different jobs, and a waterproof test with results to read.
Wrong answers come from real mistakes: "windows are made of plastic because it is see-through", "metal is used for
spoons because it is shiny", "paper would make a good umbrella", "a material can only be used for one thing".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61210)
R = U.R
P = People(R)

MATS = ["wood", "metal", "plastic", "glass", "brick", "rock", "paper", "cardboard", "fabric", "rubber"]
OBJ = [("a window", "glass", "it is transparent, so we can see through it"), ("a saucepan", "metal", "it is strong and does not melt on the cooker"),
       ("a raincoat", "plastic", "it is waterproof"), ("a kitchen chair", "wood", "it is strong and stiff"), ("a house wall", "brick", "it is strong and waterproof"),
       ("an envelope", "paper", "it is light and easy to fold"), ("a delivery box", "cardboard", "it is light but stiff"), ("a car tyre", "rubber", "it is bendy, grippy and waterproof"),
       ("a garden path", "rock", "it is hard and does not wear away"), ("a T-shirt", "fabric", "it is soft and bendy"), ("a fork", "metal", "it is strong and does not snap"),
       ("a drinks bottle", "plastic", "it is waterproof and does not break easily"), ("a book", "paper", "it is thin and easy to write on"),
       ("a garden fence", "wood", "it is strong and easy to cut and nail"), ("a car windscreen", "glass", "it is transparent and strong"), ("wellington boots", "rubber", "they are waterproof and bendy")]


def g_mat():
    o, m, _ = R.choice(OBJ)
    if not once(("ma", o)):
        return None
    w = [x for x in MATS if x != m and not (o == "a drinks bottle" and x == "glass") and not (o == "a garden fence" and x == "metal") and not (o == "a garden path" and x == "brick")
         and not (o == "a kitchen chair" and x in ("metal", "plastic")) and not (o == "a fork" and x in ("plastic", "wood"))]
    return item("What is %s usually made of?" % o, m, R.sample(w, 3), "Each material is chosen because its properties suit the job.")


def g_why():
    o, m, why = R.choice(OBJ)
    k = R.random() < 0.5
    if not once(("wh", o, k)):
        return None
    if k:
        w = [x[2] for x in OBJ if x[1] != m and x[2] != why]
        wr = R.sample(sorted(set(w)), 2) + ["it is " + R.choice(["the prettiest colour", "the cheapest thing in the world", "shiny, which is all that matters"])]
        return item("%s is made of %s. Why?" % (o[0].upper() + o[1:], m), "because " + why, ["because " + x for x in wr], "Think about what the object must do.")
    w = [x[0] for x in OBJ if x[1] != m]
    return item("Which of these is best made of %s, because %s?" % (m, why.replace("they are", "it must be").replace("it is", "it must be")), o, R.sample(w, 3), "Match the property to the job.")


BAD = [("a teapot made of chocolate", "It would melt."), ("an umbrella made of paper", "Paper is not waterproof, so it would get soggy and tear."),
       ("a window made of wood", "Wood is opaque, so you could not see through it."), ("a boat made of cardboard", "Cardboard soaks up water and goes soft."),
       ("a hammer made of glass", "Glass would shatter when it hit something."), ("a saucepan made of plastic", "It would melt on the cooker."),
       ("a coat made of glass", "Glass is hard, heavy and would break."), ("a pillow made of rock", "Rock is hard and heavy, not soft."),
       ("a bridge made of paper", "Paper is far too weak to hold people up."), ("a door made of tissue paper", "It would tear and is not strong.")]


def g_bad():
    o, why = R.choice(BAD)
    if not once(("ba", o)):
        return None
    pool = [x[1] for x in BAD if x[1] != why and not ("melt" in x[1] and "melt" in why) and not ("tear" in x[1] and "tear" in why)]
    return item("Why would %s be a bad idea?" % o, why, R.sample(pool, 3), "A material must have the right properties for the job.")


USE = [("wood", ["a table", "a pencil", "a door", "a toy boat"]), ("metal", ["a spoon", "a key", "a car", "a bike frame"]),
       ("plastic", ["a bucket", "a toy brick", "a bottle", "a lunchbox"]), ("glass", ["a jar", "a mirror", "a window", "a drinking glass"]),
       ("paper", ["a newspaper", "a paper bag", "a book", "a birthday card"])]


def g_many():
    m, objs = R.choice(USE)
    k = R.random() < 0.5
    if not once(("mn", m, k)):
        return None
    if k:
        return item("Which list shows things that are often made of %s?" % m, ", ".join(objs[:3]),
                    [", ".join(x[1][:3]) for x in R.sample([u for u in USE if u[0] != m], 3)], "One material can be used for many different things.")
    return item("A spoon can be made of metal, plastic or wood. What does this show?", "The same kind of object can be made from different materials.",
                ["Spoons can only be made of metal.", "Materials never change.", "Wood is a kind of metal."], "Different materials can do the same job.") if m == "wood" else None


def g_test():
    who = P.next()[0]
    mats = R.sample(["kitchen paper", "plastic bag", "cotton cloth", "aluminium foil", "newspaper", "rubber glove", "felt", "bin bag"], 4)
    wp = {"kitchen paper": "no", "plastic bag": "yes", "cotton cloth": "no", "aluminium foil": "yes", "newspaper": "no", "rubber glove": "yes", "felt": "no", "bin bag": "yes"}
    res = [wp[m] for m in mats]
    k = R.choice(["best", "worst", "count", "fair"])
    if not once(("te", tuple(mats), k)) or (k == "fair" and not once(("tf",), 3)):
        return None
    tab = table(["Material", "Did the water stay on top (waterproof)?"], [[m, r] for m, r in zip(mats, res)])
    intro = tab + "%s dripped water onto four materials to find one for a teddy's umbrella. " % who
    yes = [m for m, r in zip(mats, res) if r == "yes"]
    no = [m for m, r in zip(mats, res) if r == "no"]
    if k == "best":
        if len(yes) != 1:
            return None
        return item(intro + "Which material should %s use for the umbrella?" % who, yes[0], no, "It is waterproof.")
    if k == "worst":
        if len(no) != 1:
            return None
        return item(intro + "Which material is the only one that is not waterproof?", no[0], yes, "The water soaked through it.")
    if k == "count":
        g = str(len(yes))
        return item(intro + "How many of the materials were waterproof?", g, [str(x) for x in range(5) if x != len(yes)][:3], "Count the 'yes' rows.")
    return item(intro + "Why should %s use the same amount of water on each material?" % who, "so the test is fair", ["so it is quicker", "so the table looks neat", "it does not matter"], "Change only the material.")


B1 = bank([
    ("What is a material?", "what an object is made from", ["the colour of an object", "the shape of an object", "the name of an object"], "Wood, metal, plastic, glass."),
    ("Which material is see-through (transparent)?", "glass", ["wood", "brick", "cardboard"], "Windows are glass."),
    ("Which material is waterproof?", "plastic", ["paper", "cardboard", "cotton"], "Water stays on top."),
    ("Which material comes from trees?", "wood", ["metal", "plastic", "glass"], "Paper and cardboard also come from trees."),
    ("Which material are bricks made from?", "baked clay", ["melted plastic", "paper", "glass"], "Bricks are strong and waterproof."),
    ("Why are saucepans made of metal?", "Metal is strong and does not melt on the cooker.", ["Metal is see-through.", "Metal is soft.", "Metal is waterproof only."], "Suitable for heat."),
    ("Which material is good for a football?", "rubber or leather", ["glass", "rock", "brick"], "Bendy and bouncy."),
    ("Which is a property of rock?", "hard", ["soft and bendy", "see-through", "stretchy"], "Rock is hard and strong."),
])
B5 = bank([
    ("Why are some cups made of paper and others of glass?", "Paper cups are light and thrown away; glass cups can be washed and used again.", ["Paper is stronger than glass.", "Glass is waterproof but paper is too.", "There is no reason."], "Suitable for different uses."),
    ("Why are playground slides often made of plastic or metal?", "They are smooth and strong.", ["They are soft and bendy.", "They are see-through.", "They soak up water."], "Smooth and strong."),
    ("Who invented a waterproof coat using rubber?", "Charles Macintosh", ["John McAdam", "Isaac Newton", "Mary Anning"], "The 'mac' is named after him."),
    ("John McAdam made roads better using what?", "layers of small, crushed stones", ["glass", "paper", "rubber bands"], "Smooth, hard roads."),
    ("How could you find the best material for a teddy's raincoat?", "Drip the same amount of water onto each material and see which stays dry underneath.", ["Pick the prettiest one.", "Use different amounts of water.", "Test only one material."], "Fair test."),
])


def body():
    pic = K.row(["glass", "spoon", "umbrella"], words=["glass window", "metal spoon", "plastic umbrella"], size=90, label="a glass window, a metal spoon and a plastic umbrella")
    ex = [("Why is a window made of glass?", ["We need to see through it"], "it is transparent"),
          ("Why not a paper umbrella?", ["Water soaks in"], "paper is not waterproof")]
    mist = ["Thinking windows are glass only because glass is shiny.", "Thinking paper would make a good umbrella.", "Thinking a material can only be used for one thing."]
    return kid_lesson(pic, "We choose materials that suit the job.",
                      ["Glass is see-through, metal is strong, plastic is waterproof.", "One material can be used for many things.", "One object can be made of different materials."], ex, mist)


def main():
    sets = U.sets([
        ("What is it made of?", B1 + [(g_mat, 12)]),
        ("Why that material?", [(g_why, 14), (g_mat, 4), (g_many, 2)]),
        ("Silly materials", [(g_bad, 10), (g_why, 8), (g_many, 2)]),
        ("Waterproof test", [(g_test, 20)]),
        ("Thinking about materials", B5 + [(g_test, 10), (g_why, 4), (g_many, 1)]),
    ])
    make_uk(2, "uses-of-everyday-materials", 10, "Uses of everyday materials",
            "Identify and compare the suitability of a variety of everyday materials, including wood, metal, plastic, glass, brick, rock, paper and cardboard for particular uses.",
            "Uses of Everyday Materials",
            "Year 2 Science: Uses of Everyday Materials Worksheets (Choosing Materials)",
            "Uses of Materials",
            "Free Year 2 science worksheets on the uses of everyday materials: wood, metal, plastic, glass, brick, rock, paper and cardboard, why they are chosen and a waterproof test. 100 questions with answers.",
            "Choose a material that suits the job.",
            "Glass is see-through, metal is strong, plastic is waterproof.",
            body(),
            [("Why are different materials used for different things?", "Each material has properties that suit some jobs. Glass is transparent for windows; metal is strong for spoons; plastic is waterproof for raincoats."),
             ("Can one material be used for lots of things?", "Yes. Wood is used for tables, pencils, doors and toys."),
             ("How can I test if a material is waterproof?", "Drip the same amount of water onto each material. If the water stays on top and does not soak through, it is waterproof.")],
            sets)


if __name__ == "__main__":
    main()
