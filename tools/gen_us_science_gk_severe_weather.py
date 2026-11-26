# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Severe Weather (K-ESS3-2)
  python tools/gen_us_science_gk_severe_weather.py
Ask questions to obtain information about the purpose of weather forecasting to prepare for, and respond to, severe
weather. Thunderstorms, tornadoes, hurricanes, blizzards, floods and heat waves; forecasts and warnings; staying safe.
Very short sentences for 5-6 year olds; most questions have a picture.
Wrong answers come from real mistakes: "stand under a tree in a thunderstorm", "play in flood water", "forecasts are just guesses".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, People
import sci_kids as K

U = Unit(9109)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# name, description, safe action, unsafe actions, picture
SEV = [("a thunderstorm", "lightning, thunder and heavy rain", "go inside a building", ["stand under a tall tree", "swim in a pool", "fly a kite"], "storm"),
       ("a tornado", "a spinning funnel of wind that touches the ground", "go to a basement or a small inside room", ["stand by a window", "go outside to watch", "ride a bike"], "wind"),
       ("a hurricane", "a huge storm from the ocean with strong wind and rain", "leave if told to, or stay inside away from windows", ["go to the beach", "go surfing", "camp in a tent"], "rain"),
       ("a blizzard", "a snowstorm with strong wind and lots of snow", "stay inside and keep warm", ["go for a long walk", "drive far away", "wear shorts outside"], "snow"),
       ("a flood", "so much water that it covers roads and land", "move to higher ground and stay out of the water", ["play in the water", "drive through deep water", "walk in fast water"], "puddle"),
       ("a heat wave", "many very hot days in a row", "drink water and stay in the shade or inside", ["run hard at noon", "sit in a hot car", "skip drinking water"], "hot")]


def g_safe():
    n, d, safe, bad, pic = R.choice(SEV)
    who = P.next()[0]
    t = R.random() < 0.4
    if t:
        if not once((n, "safe")):
            return None
        return item(fig(K.card(pic)) + "There is %s. What should %s do?" % (n, who), safe, bad, "Stay safe: %s." % safe)
    good = R.choice(bad)
    if not once(("b", good)):
        return None
    others = [x[2] for x in SEV if x[0] != n]
    return item(fig(K.card(pic)) + "There is %s. Which is NOT safe?" % n, good, [safe] + R.sample(others, 2), "%s is not safe in %s." % (good[0].upper() + good[1:], n))


def g_name():
    n, d, safe, bad, pic = R.choice(SEV)
    who = P.next()[0]
    if not once(("n", n)):
        return None
    return item("%s hears about %s. What is it called?" % (who, d), n, R.sample([x[0] for x in SEV if x[0] != n], 3), "%s is %s." % (n[0].upper() + n[1:], d))


FC = [("What is a weather forecast?", "a report that tells what the weather will be", ["a kind of cloud", "a type of rain boot", "a game"]),
      ("Who makes weather forecasts?", "meteorologists (weather scientists)", ["bakers", "farmers' cows", "mail carriers"]),
      ("Why do people listen to the forecast?", "to get ready for the weather", ["to make it rain", "to stop storms", "to hear music"]),
      ("A forecast says a blizzard is coming. What should a family do?", "get food, water and warm blankets ready", ["plan a beach trip", "open all the windows", "do nothing"]),
      ("A warning says a tornado may come. Where should kids go?", "to the safe room the grown-ups choose", ["outside to look", "to a window", "to the roof"]),
      ("How can you hear a weather warning?", "on TV, the radio, a phone or a siren", ["by looking at a rock", "by smelling flowers", "by counting shoes"]),
      ("A forecast says it will be very hot. What should Ava bring to the park?", "water and a hat", ["a heavy coat", "mittens", "a snow shovel"]),
      ("A hurricane is coming. Why do people cover windows with boards?", "to keep wind and things from breaking the glass", ["to make it dark", "to paint them", "for fun"]),
      ("The forecast says thunderstorms this afternoon. What should the class do?", "plan recess indoors", ["plan a picnic in a field", "go swimming", "fly kites"]),
      ("Why do schools close for some blizzards?", "Roads are snowy and unsafe.", ["It is too sunny.", "The buses are hungry.", "Snow is fun."])]


def g_fc():
    q, a, w = R.choice(FC)
    if not once(q):
        return None
    return item(q, a, w, "Forecasts help people get ready and stay safe.")


def g_pick():
    q = R.choice([("storm", "lightning and thunder"), ("snow", "a blizzard"), ("sun", "a heat wave"), ("rain", "a flood"), ("wind", "a tornado")])
    clash = {"wind": {"storm"}, "rain": {"storm"}, "snow": {"wind"}, "storm": {"rain"}}.get(q[0], set())
    kinds = [k for k in ["storm", "snow", "sun", "rain", "wind"] if k not in clash]
    R.shuffle(kinds)
    kinds = kinds[:4]
    if q[0] not in kinds or not once((tuple(kinds), q[0])) or not once(("pq", q[0]), 6):
        return None
    L = "ABCD"
    who = P.next()[0]
    nm = {"storm": "storm", "snow": "snow", "sun": "sun", "rain": "rain", "wind": "wind"}
    pic = K.row(kinds, words=["%s. %s" % (L[i], nm[k]) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s looks at the weather pictures. Which goes with %s?" % (who, q[1]), "%s (%s)" % (L[kinds.index(q[0])], nm[q[0]]),
                ["%s (%s)" % (L[i], nm[k]) for i, k in enumerate(kinds) if k != q[0]], "%s comes with %s." % (q[1][0].upper() + q[1][1:], nm[q[0]]))


KIT = [("a flashlight", True), ("bottled water", True), ("a first aid kit", True), ("extra batteries", True), ("canned food", True), ("warm blankets", True),
       ("a kite", False), ("a beach ball", False), ("ice cream", False), ("sunglasses only", False), ("a jump rope", False)]


def g_kit():
    good = R.choice([k for k, v in KIT if v])
    bad = R.sample([k for k, v in KIT if not v], 3)
    who = P.next()[0]
    q = R.random() < 0.6
    if not once((good, q)):
        return None
    if q:
        return item("%s's family makes a storm kit. Which should go in it?" % who, good, bad, "A storm kit has things you need if the power goes out.")
    goods = R.sample([k for k, v in KIT if v], 3)
    b = R.choice([k for k, v in KIT if not v])
    if not once(("nb", b)):
        return None
    return item("%s's family makes a storm kit. Which does NOT belong?" % who, b, goods, "%s will not help in a storm." % (b[0].upper() + b[1:]))


SIGN = [("The sky turns dark green and a siren sounds.", "a tornado"), ("Dark clouds pile up and thunder rumbles.", "a thunderstorm"),
        ("The river rises higher and higher after days of rain.", "a flood"), ("The forecast says it will be 100 degrees all week.", "a heat wave"),
        ("The forecast says lots of snow and strong wind.", "a blizzard"), ("A huge storm is moving in from the ocean.", "a hurricane")]


def g_sign():
    sg, a = R.choice(SIGN)
    who = P.next()[0]
    if not once(sg):
        return None
    return item("%s notices: %s What may be coming?" % (who, sg), a, R.sample([x[1] for x in SIGN if x[1] != a], 3), "Signs and forecasts warn us.")


AFTER = [("After a storm, Ava sees a fallen power line. What should she do?", "stay far away and tell a grown-up", ["touch it", "jump over it", "pick it up"]),
         ("After a flood, Leo sees puddles in the street. What should he do?", "stay out of the water", ["splash in it", "drink it", "swim in it"]),
         ("After a blizzard, the power is out. What can Mia's family use for light?", "a flashlight", ["a candle left alone", "a toaster", "a fan"]),
         ("After a tornado warning ends, what should Kai do?", "wait for a grown-up to say it is safe", ["run outside at once", "climb a tree", "go to the roof"]),
         ("After a heat wave day, Zoe feels very hot and tired. What should she do?", "rest in a cool place and drink water", ["run laps", "sit in the sun", "wear a coat"]),
         ("After a hurricane, a tree is down on the road. What should people do?", "stay back and let workers clear it", ["climb on it", "drive over it", "play under it"])]


def g_after():
    q, a, w = R.choice(AFTER)
    if not once(q):
        return None
    return item(q, a, w, "Stay safe after a storm too.")


B1 = bank([
    ("What is severe weather?", "very strong weather that can be dangerous", ["a sunny, calm day", "a light breeze", "a rainbow"], "Storms, tornadoes, blizzards..."),
    ("Where should you go in a thunderstorm?", "inside a building", ["under a tall tree", "into a pool", "to a hilltop"], "Lightning is dangerous."),
    ("What is a blizzard?", "a strong snowstorm", ["a hot day", "a rainbow", "a light rain"], "Lots of snow and wind."),
    ("What should you do in a flood?", "stay out of the water and move to higher ground", ["play in the water", "swim in the street", "drive through it"], "Floodwater is dangerous."),
    ("Why do we have weather forecasts?", "to know what weather is coming so we can be ready", ["to make the weather", "to stop rain", "to sell umbrellas"], "Forecasts help us prepare."),
    ("Where should you go if there is a tornado warning?", "a basement or a small room with no windows", ["outside", "next to a window", "on the roof"], "Stay away from windows."),
    ("What should you drink a lot of in a heat wave?", "water", ["hot cocoa", "nothing", "soda only"], "Stay cool and drink water."),
    ("Who studies and forecasts the weather?", "a meteorologist", ["a dentist", "a chef", "a pilot only"], "Weather scientists."),
])
B5 = bank([
    ("Ava hears thunder at the park. What should she do?", "go inside right away", ["stay on the swings", "stand under a tree", "wait for lightning"], "When thunder roars, go indoors."),
    ("Leo's family hears a tornado siren. What should they do?", "go to the basement", ["go outside to look", "open the windows", "get in the pool"], "Get low and inside."),
    ("Mia sees a flooded road. What should her family do?", "turn around and find another way", ["drive through it", "walk through it", "swim across"], "Turn around, don't drown."),
    ("Kai's forecast says a blizzard will come tomorrow. What is a good plan?", "stay home with food, water and warm blankets", ["plan a long drive", "wear shorts", "leave the door open"], "Prepare early."),
    ("Zoe asks why the weather reporter shows a map. Why?", "to show where the storm is going", ["to show toys", "to teach colors only", "for fun only"], "Maps help us prepare."),
])


def body():
    pic = K.row(["storm", "wind", "snow", "rain"], words=["thunderstorm", "tornado", "blizzard", "flood"], size=105)
    ex = [("There is a thunderstorm. What should you do?", ["Lightning is dangerous."], "go inside"),
          ("Why listen to the forecast?", ["It tells what is coming."], "to get ready")]
    mist = ["Standing under a tree in a thunderstorm.",
            "Playing in flood water.",
            "Thinking forecasts do not help."]
    return kid_lesson(pic, "Some weather is dangerous.",
                      ["Forecasts tell us what is coming.", "Get ready: food, water, flashlight.", "Go inside and stay safe."], ex, mist)


def main():
    sets = U.sets([
        ("Severe weather", B1 + [(g_name, 6), (g_pick, 6)]),
        ("Staying safe", [(g_safe, 12), (g_pick, 4), (g_kit, 4)]),
        ("Forecasts", [(g_fc, 10), (g_sign, 6), (g_pick, 4)]),
        ("Getting ready", [(g_kit, 7), (g_safe, 6), (g_pick, 4), (g_after, 3)]),
        ("Weather safety", B5 + [(g_safe, 4), (g_after, 3), (g_pick, 6), (g_kit, 2)]),
    ])
    make("kindergarten", "severe-weather", 9, "K-ESS3-2",
         "Ask questions to obtain information about the purpose of weather forecasting to prepare for, and respond to, severe weather.",
         "Severe Weather",
         "Kindergarten Severe Weather Worksheets: Forecasts and Staying Safe",
         "Severe Weather",
         "Free kindergarten science worksheets on severe weather (NGSS K-ESS3-2): thunderstorms, tornadoes, blizzards and floods, weather forecasts and how to stay safe. 100 picture questions with answers.",
         "Some weather is dangerous.",
         "Forecasts help us get ready. Go inside and stay safe.",
         body(),
         [("What is severe weather?", "Dangerous weather like thunderstorms, tornadoes, hurricanes, blizzards, floods and heat waves."),
          ("Why are weather forecasts important?", "They tell us what weather is coming so families and schools can get ready and stay safe."),
          ("What goes in a storm kit?", "A flashlight, extra batteries, bottled water, canned food, a first aid kit and warm blankets.")],
         sets)


if __name__ == "__main__":
    main()
