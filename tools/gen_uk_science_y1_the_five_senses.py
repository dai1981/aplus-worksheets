# -*- coding: utf-8 -*-
"""
UK Year 1 science: The Five Senses (Animals, including humans)
  python tools/gen_uk_science_y1_the_five_senses.py
Say which part of the body is associated with each sense: sight (eyes), hearing (ears), smell (nose), taste (tongue)
and touch (skin); which sense we use for an activity; sense words (loud, sour, smooth, bright, smelly); how senses keep
us safe; and a sound walk tally.
Wrong answers come from real mistakes: "we taste with our nose", "touch only happens with hands", "we hear with our
eyes", "smell and taste are the same".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61108)
R = U.R
P = People(R)

SENSE = [("sight", "eyes"), ("hearing", "ears"), ("smell", "nose"), ("taste", "tongue"), ("touch", "skin")]


def g_sense():
    s, b = R.choice(SENSE)
    k = R.choice([True, False, None])
    if not once(("se", s, k)):
        return None
    if k is None:
        return item("Your %s help you with which of these?" % ("skin and fingers" if b == "skin" else b if b != "nose" and b != "tongue" else "nose" if b == "nose" else "tongue"),
                    {"sight": "seeing colours and shapes", "hearing": "hearing sounds", "smell": "smelling flowers", "taste": "tasting food", "touch": "feeling if something is soft or hard"}[s],
                    [{"sight": "seeing colours and shapes", "hearing": "hearing sounds", "smell": "smelling flowers", "taste": "tasting food", "touch": "feeling if something is soft or hard"}[x[0]] for x in SENSE if x[0] != s][:3],
                    "Eyes see, ears hear, nose smells, tongue tastes, skin feels.")
    if k:
        return item("Which part of the body do we use for the sense of %s?" % s, "our " + b, ["our " + x[1] for x in SENSE if x[1] != b][:3], "Eyes see, ears hear, nose smells, tongue tastes, skin feels.")
    return item("Which sense do we use our %s for?" % b, s, [x[0] for x in SENSE if x[0] != s][:3], "Eyes see, ears hear, nose smells, tongue tastes, skin feels.")


ACT = [("listening to music", "hearing"), ("looking at a rainbow", "sight"), ("smelling a rose", "smell"), ("tasting a lemon", "taste"), ("stroking a soft kitten", "touch"),
       ("hearing a dog bark", "hearing"), ("reading a book", "sight"), ("sniffing fresh bread", "smell"), ("licking an ice lolly", "taste"), ("feeling cold snow", "touch"),
       ("watching fireworks", "sight"), ("hearing a phone ring", "hearing"), ("smelling smoke", "smell"), ("tasting salty crisps", "taste"), ("feeling rough sandpaper", "touch"),
       ("hearing birds sing", "hearing"), ("seeing traffic lights change", "sight"), ("smelling a stinky sock", "smell"), ("feeling warm sunshine on your face", "touch"),
       ("tasting sweet strawberries", "taste")]


def g_act():
    a, s = R.choice(ACT)
    if not once(("ac", a)):
        return None
    return item("Which sense are you mainly using when %s?" % a, s, R.sample([x[0] for x in SENSE if x[0] != s], 3), "Think about which part of your body is doing the work.")


WORD = [("loud", "hearing"), ("quiet", "hearing"), ("squeaky", "hearing"), ("bright", "sight"), ("colourful", "sight"), ("sour", "taste"), ("sweet", "taste"),
        ("salty", "taste"), ("smooth", "touch"), ("rough", "touch"), ("soft", "touch"), ("prickly", "touch"), ("smelly", "smell"), ("perfumed", "smell"), ("stinky", "smell")]


def g_word():
    w, s = R.choice(WORD)
    if not once(("wo", w)):
        return None
    return item("Which sense would you use to find out if something is %s?" % w, s, R.sample([x[0] for x in SENSE if x[0] != s], 3), "Some words describe sounds, some tastes, some how things feel.")


SAFE = [("You smell smoke in the kitchen.", "smell", "It warns you there may be a fire."), ("You hear a fire alarm.", "hearing", "It tells you to leave the building."),
        ("You see the red man at a crossing.", "sight", "It tells you to wait and not cross."), ("Milk tastes sour.", "taste", "It tells you the milk has gone off."),
        ("You feel that a radiator is very hot.", "touch", "It warns you to move your hand away."), ("You hear a car coming.", "hearing", "It tells you to stay on the pavement.")]


def g_safe():
    s, sense, why = R.choice(SAFE)
    k = R.random() < 0.5
    if not once(("sa", s, k)):
        return None
    if k:
        return item("%s Which sense is keeping you safe?" % s, sense, R.sample([x[0] for x in SENSE if x[0] != sense], 3), why)
    return item("%s How does this help keep you safe?" % s, why, R.sample([x[2] for x in SAFE if x[2] != why], 3), "Our senses warn us about danger.")


SOUNDS = ["birds singing", "cars going past", "a dog barking", "children laughing", "an aeroplane", "the wind in the trees"]


def g_walk():
    who = P.next()[0]
    s = R.sample(SOUNDS, 4)
    v = R.sample(range(1, 11), 4)
    k = R.choice(["most", "least", "read", "sense"])
    ri = R.randrange(4)
    if not once(("wa", tuple(s), tuple(v), k)) or (k == "sense" and not once(("ws",), 3)):
        return None
    tab = table(["Sound", "Times heard"], [[a, str(b)] for a, b in zip(s, v)])
    intro = tab + "%s went on a sound walk round the school. " % who
    if k == "most":
        a = s[v.index(max(v))]
        return item(intro + "Which sound did %s hear most often?" % who, a, [x for x in s if x != a], "The biggest number.")
    if k == "least":
        a = s[v.index(min(v))]
        return item(intro + "Which sound did %s hear least often?" % who, a, [x for x in s if x != a], "The smallest number.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many times did %s hear %s?" % (who, s[ri]), g, [str(x) for x in v if x != v[ri]][:3], "Read the row.")
    return item(intro + "Which sense did %s use on the sound walk?" % who, "hearing", ["sight", "taste", "smell"], "Sounds are heard with our ears.")


B1 = bank([
    ("How many senses do we have?", "five", ["two", "three", "ten"], "Sight, hearing, smell, taste and touch."),
    ("Which part of the body do we hear with?", "our ears", ["our eyes", "our nose", "our tongue"], "Ears hear sounds."),
    ("Which part of the body do we taste with?", "our tongue", ["our ears", "our nose only", "our elbows"], "Taste buds are on the tongue."),
    ("Which part of the body do we see with?", "our eyes", ["our ears", "our tongue", "our skin"], "Eyes need light."),
    ("Which part of the body do we smell with?", "our nose", ["our eyes", "our hands", "our knees"], "Sniff!"),
    ("Can we feel things with our feet?", "Yes. We feel with our skin all over our body.", ["No, only with hands.", "Only with our tongue.", "No, feet cannot feel."], "Touch is everywhere."),
    ("Which sense tells us if something is hot or cold?", "touch", ["sight", "hearing", "smell"], "Skin feels heat."),
    ("Which sense helps us enjoy music?", "hearing", ["taste", "smell", "touch"], "Ears."),
])
B5 = bank([
    ("Why does food taste of less when you have a cold?", "Smell helps us taste, and a blocked nose cannot smell well.", ["The tongue falls asleep.", "Food changes when you are ill.", "Ears stop working."], "Smell and taste work together."),
    ("How could you test if people can name foods by taste alone?", "Cover their eyes and give them small pieces of food to taste.", ["Let them look at the food.", "Ask them to smell only.", "Guess for them."], "Fair test."),
    ("Why should you never taste things to find out what they are?", "Some things can be harmful or poisonous.", ["Tongues are not for tasting.", "It is always safe.", "It makes you taller."], "Safety first."),
    ("How do people who cannot see well read?", "Some use Braille, raised dots felt with the fingers.", ["They use their ears to read print.", "They taste the paper.", "They cannot read."], "Touch helps."),
    ("Why do we have two ears?", "to hear sounds well and tell where they come from", ["for balance only", "to see better", "in case one falls off"], "Two ears help."),
])


def body():
    pic = K.row(["mirror", "bell", "flower", "apple", "sock"], words=["sight", "hearing", "smell", "taste", "touch"], size=74, label="the five senses: sight, hearing, smell, taste and touch")
    ex = [("Which sense tells you a drum is loud?", ["Ears"], "hearing"),
          ("We taste with?", ["Inside the mouth"], "our tongue")]
    mist = ["Thinking we taste with our nose.", "Thinking touch only happens with our hands.", "Thinking smell and taste are the same."]
    return kid_lesson(pic, "We have five senses.",
                      ["Sight (eyes), hearing (ears), smell (nose).", "Taste (tongue) and touch (skin).", "Our senses help keep us safe."], ex, mist)


def main():
    sets = U.sets([
        ("Our five senses", B1 + [(g_sense, 10), (g_act, 2)]),
        ("Which sense?", [(g_act, 14), (g_word, 4), (g_sense, 2)]),
        ("Sense words and safety", [(g_word, 11), (g_safe, 9)]),
        ("Sound walk", [(g_walk, 20)]),
        ("Thinking about senses", B5 + [(g_safe, 3), (g_walk, 12)]),
    ])
    make_uk(1, "the-five-senses", 8, "Animals, including humans",
            "Identify, name, draw and label the basic parts of the human body and say which part of the body is associated with each sense.",
            "The Five Senses",
            "Year 1 Science: The Five Senses Worksheets (Sight, Hearing, Smell, Taste, Touch)",
            "The Five Senses",
            "Free Year 1 science worksheets on the five senses: sight, hearing, smell, taste and touch, the body part for each sense, sense words, staying safe and a sound walk. 100 questions with answers.",
            "We have five senses.",
            "Eyes see, ears hear, nose smells, tongue tastes, skin feels.",
            body(),
            [("What are the five senses?", "Sight, hearing, smell, taste and touch."),
             ("Which body part goes with each sense?", "We see with our eyes, hear with our ears, smell with our nose, taste with our tongue and feel with our skin."),
             ("How do our senses keep us safe?", "We can smell smoke, hear a fire alarm or a car, see a red light, taste milk that has gone off and feel if something is too hot.")],
            sets)


if __name__ == "__main__":
    main()
