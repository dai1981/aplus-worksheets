# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Sending Signals with Light and Sound (1-PS4-4)
  python tools/gen_us_science_g1_sending_signals_with_light_and_sound.py
Use tools and materials to design and build a device that uses light or sound to solve the problem of communicating
over a distance. Flashlights, drums, whistles, bells, cup-and-string phones, lighthouses, traffic lights and alarms;
simple flash and beat codes; choosing light or sound for a problem.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "a loose string still carries sound", "light signals work when you cannot see them",
"a signal works even if no one knows the code".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(10104)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


DEV = [("a flashlight", "light", "flashlight"), ("a drum", "sound", "drum"), ("a bell", "sound", "bell"), ("a whistle", "sound", None),
       ("a lighthouse", "light", None), ("a traffic light", "light", None), ("a fire alarm", "sound", None), ("a car horn", "sound", None),
       ("a car's blinking turn signal", "light", None), ("a doorbell", "sound", None), ("a cup-and-string phone", "sound", None),
       ("a mirror flashing sunlight", "light", "mirror"), ("a glow stick waved in the dark", "light", None), ("a school bell", "sound", "bell"),
       ("a siren on a fire truck", "sound", None), ("a lantern held up high", "light", None)]


def g_type():
    d, k, pic = R.choice(DEV)
    who = P.next()[0]
    if not once(d):
        return None
    fg = fig(K.card(pic)) if pic else ""
    return item(fg + "%s sends a message with %s. Does it use light or sound?" % (who, d), k, ["sound" if k == "light" else "light", "smell", "taste"],
                "%s uses %s." % (d[0].upper() + d[1:], k))


MEAN = [("A traffic light turns red.", "stop", ["go", "turn around", "honk"]),
        ("A traffic light turns green.", "go", ["stop", "sit down", "go home"]),
        ("The fire alarm rings.", "go outside safely", ["keep playing", "hide under a desk", "turn up music"]),
        ("The school bell rings in the morning.", "class is starting", ["school is closed", "it is lunchtime at night", "it is snowing"]),
        ("A lighthouse flashes at night.", "watch out, rocks and land are near", ["come and swim", "the store is open", "the sun is up"]),
        ("The lifeguard blows a whistle.", "listen and stop", ["swim faster", "go to sleep", "throw sand"]),
        ("A car's turn signal blinks on the left.", "the car will turn left", ["the car is broken", "the car will stop forever", "it is raining"]),
        ("The doorbell rings.", "someone is at the door", ["the oven is hot", "it is bedtime", "the phone is lost"]),
        ("A fire truck's siren is loud and close.", "move out of the way", ["run toward it", "stand in the road", "ignore it"]),
        ("The crossing sign shows a walking person.", "it is safe to walk", ["run back", "cars can go", "stay home"])]


def g_mean():
    s, a, w = R.choice(MEAN)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s: “%s” What does the signal mean?" % (who, s), a, w, "Signals tell people what to do.")


def flashes_svg(n, kind):
    s = ""
    for i in range(n):
        x = 40 + i * 56
        if kind == "light":
            s += "<circle cx='%d' cy='40' r='18' fill='#ffe066' stroke='%s' stroke-width='1.6'/>" % (x, INK)
            for a in range(8):
                import math
                ang = a * math.pi / 4
                s += "<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#f0b400' stroke-width='2'/>" % (x + 22 * math.cos(ang), 40 + 22 * math.sin(ang), x + 27 * math.cos(ang), 40 + 27 * math.sin(ang))
        else:
            s += K.icon("drum", x, 46, 0.6) + text(x, 84, "boom", 11, weight=400)
    w = 40 + n * 56
    return svg_wrap(max(w, 120), 92, s, "%d %s" % (n, "flashes of light" if kind == "light" else "drum beats"))


MSG = ["come home", "dinner is ready", "I am OK", "help", "yes", "no", "time to go", "look up", "I found it", "wait for me"]


def g_code():
    kind = R.choice(["light", "sound"])
    codes = R.sample(MSG, 3)
    n = R.randint(1, 3)
    who, she, her = P.next()
    friend = P.next()[0]
    if not once((kind, tuple(codes), n)) or not once(("cn", kind, n), 8):
        return None
    unit = "flash" if kind == "light" else "beat"
    key = "<br>".join("%d %s%s = “%s”" % (i + 1, unit, "" if i == 0 else ("es" if unit == "flash" else "s"), c) for i, c in enumerate(codes))
    return item(fig(flashes_svg(n, kind)) + "%s and %s made a code:<br>%s<br>%s sends this. What does it mean?" % (who, friend, key, who),
                codes[n - 1], [c for c in codes if c != codes[n - 1]] + [R.choice([m for m in MSG if m not in codes])],
                "Count: %d %s%s." % (n, unit, "" if n == 1 else ("es" if unit == "flash" else "s")))


SIT = [("Two friends are far apart on a dark, quiet night. They can see each other's windows.", "light", "A light shows up well in the dark."),
       ("A friend is around a corner and cannot see you.", "sound", "Sound goes around corners."),
       ("A boat is far away at sea at night.", "light", "A bright light can be seen far away at night."),
       ("It is very noisy at a busy game, but your friend can see you.", "light", "A light can be seen even when it is noisy."),
       ("Your friend is in the next room with the door shut.", "sound", "Sound goes through doors and walls."),
       ("A hiker is lost in a thick forest. The trees block the view.", "sound", "A whistle can be heard through trees."),
       ("Your friend is sleeping, and you must wake them.", "sound", "Sound wakes people up."),
       ("A ship must see where the rocky shore is at night.", "light", "A lighthouse shines far."),
       ("You need to tell someone across a quiet library to come here.", "light", "A quiet light signal keeps the library quiet.")]


def g_pick():
    s, a, why = R.choice(SIT)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s has a problem. %s Which is better to use, light or sound?" % (who, s), a, ["sound" if a == "light" else "light", "neither one works", "a smell"], why)


CUP = [("What carries the sound in a cup-and-string phone?", "the string vibrating", ["the air in your pocket", "light", "the cups glowing"], "The string shakes."),
       ("The string on Leo's cup phone is loose. What happens?", "The sound does not travel well.", ["It gets louder.", "It works better.", "It makes light."], "Pull it tight."),
       ("How can Mia make her cup phone work better?", "pull the string tight", ["let the string touch the floor", "cut the string", "fill the cups with sand"], "Tight string carries sound."),
       ("What does the cup do in a cup-and-string phone?", "catches your voice and makes the string vibrate", ["makes light", "keeps the string wet", "nothing"], "Your voice shakes the cup."),
       ("Kai builds a light signal for night. What must his friend be able to do?", "see the light", ["hear the light", "smell the light", "touch the light"], "Light signals must be seen."),
       ("Zoe builds a drum signal. What must her friend be able to do?", "hear it", ["see it in the dark", "taste it", "smell it"], "Sound signals must be heard."),
       ("Why must friends agree on a code first?", "so they know what each signal means", ["so the signal is louder", "so it is brighter", "so it is faster"], "A code is a shared plan."),
       ("Sam's flashlight is too dim to see across the yard. How can he improve it?", "use a brighter light", ["use a smaller light", "turn it off", "cover it with cardboard"], "Brighter goes farther.")]


def g_cup():
    q, a, w, e = R.choice(CUP)
    if not once(q):
        return None
    return item(q, a, w, e)


B1 = bank([
    ("What is a signal?", "a light or sound that sends a message", ["a kind of food", "a toy car", "a type of tree"], "Signals carry messages."),
    ("Which one sends a message with light?", "a flashlight", ["a drum", "a whistle", "a bell"], "Flashlights make light."),
    ("Which one sends a message with sound?", "a whistle", ["a flashlight", "a lighthouse", "a glow stick"], "Whistles make sound."),
    ("Why do we use signals?", "to send messages over a distance", ["to make things heavy", "to grow plants", "to cool food"], "Far away people get the message."),
    ("Which signal tells cars to stop?", "a red traffic light", ["a green traffic light", "a doorbell", "a school bell"], "Red means stop."),
    ("What does a lighthouse do?", "shines a light to warn boats", ["rings to call kids", "plays music", "makes rain"], "It keeps boats safe."),
    ("What can you build to talk to a friend with sound?", "a cup-and-string phone", ["a paper hat", "a sandwich", "a sock puppet"], "Sound travels on the string."),
    ("Which works best on a dark night far away?", "a bright flashlight", ["a whisper", "a small bell", "a note on paper"], "Bright light can be seen far."),
])
B5 = bank([
    ("Ava and Leo use 2 flashes for “yes.” Ava sees 2 flashes. What is the answer?", "yes", ["no", "maybe", "help"], "Count the flashes."),
    ("Mia drums 3 beats. Her code says 3 beats = “come inside.” What should her brother do?", "come inside", ["go outside", "go to sleep", "drum back 1"], "Follow the code."),
    ("Kai's whistle signal does not reach his friend far away. What can he try?", "a louder whistle or a drum", ["a quieter whistle", "a whisper", "a note"], "Louder sound goes farther."),
    ("Zoe's light signal is hard to see in the sun. What can she try?", "a mirror to flash sunlight", ["a dim candle", "a dark cloth", "turning off the light"], "Make it brighter."),
    ("Why do fire trucks use both lights and sirens?", "so people can see and hear them", ["to look pretty", "to stay quiet", "to save water"], "Two signals are better."),
])


def body():
    pic = svg_wrap(400, 120, K.icon("flashlight", 90, 50, 1.0) + text(90, 110, "light", 14) + K.icon("drum", 300, 56, 1.0) + text(300, 110, "sound", 14),
                   "a flashlight (light) and a drum (sound)")
    ex = [("Code: 1 flash = yes, 2 flashes = no. You see 2 flashes.", ["Count them."], "no"),
          ("Your friend is around a corner. Light or sound?", ["Sound goes around corners."], "sound")]
    mist = ["Using a light signal when your friend cannot see it.",
            "Letting the string of a cup phone hang loose.",
            "Sending a code your friend does not know."]
    return kid_lesson(pic, "We can send messages far away.",
                      ["Use light: flashlight, lighthouse.", "Use sound: drum, whistle, bell.", "Agree on a code first."], ex, mist)


def main():
    sets = U.sets([
        ("Light or sound?", B1 + [(g_type, 8), (g_mean, 4)]),
        ("Signals around us", [(g_type, 8), (g_mean, 6), (g_pick, 6)]),
        ("Secret codes", [(g_code, 16), (g_cup, 4)]),
        ("Choosing a signal", [(g_pick, 3), (g_code, 13), (g_cup, 4)]),
        ("Signal builders", B5 + [(g_code, 15)]),
    ])
    make("grade-1", "sending-signals-with-light-and-sound", 4, "1-PS4-4",
         "Use tools and materials to design and build a device that uses light or sound to solve the problem of communicating over a distance.",
         "Sending Signals with Light and Sound",
         "Grade 1 Signals Worksheets: Send Messages with Light and Sound",
         "Light and Sound Signals",
         "Free grade 1 science worksheets on signals (NGSS 1-PS4-4): flashlights, drums, whistles, codes and cup phones for sending messages far away. 100 picture questions with answers.",
         "Send messages with light or sound.",
         "Flash a light or bang a drum. Agree on a code first.",
         body(),
         [("How can we send a message far away?", "With light, like a flashlight or a lighthouse, or with sound, like a drum, whistle or bell."),
          ("When is light better? When is sound better?", "Light is good when your friend can see you, even in a noisy place. Sound is good around corners or through doors."),
          ("What can kids build?", "A flashlight code, a drum code or a cup-and-string phone with a tight string.")],
         sets)


if __name__ == "__main__":
    main()
