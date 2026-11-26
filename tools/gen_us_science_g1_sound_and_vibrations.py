# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Sound and Vibrations (1-PS4-1)
  python tools/gen_us_science_g1_sound_and_vibrations.py
Plan and conduct investigations to provide evidence that vibrating materials can make sound and that sound can make
materials vibrate. Drums, bells, rubber bands, guitar strings, your throat; rice jumping on a drum; stopping a bell.
Very short sentences for 6-7 year olds, many pictures.
Wrong answers come from real mistakes: "sound comes from air only", "a still drum makes sound", "you cannot see vibrations".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(10101)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def shake(x, y, n=3, r=26):
    """little curved lines that show something is vibrating"""
    s = ""
    for i in range(n):
        rr = r + i * 8
        s += "<path d='M%g %g A%g %g 0 0 1 %g %g' fill='none' stroke='#d9822b' stroke-width='2'/>" % (x + rr * 0.6, y - rr * 0.8, rr, rr, x + rr * 0.6, y + rr * 0.8)
        s += "<path d='M%g %g A%g %g 0 0 0 %g %g' fill='none' stroke='#d9822b' stroke-width='2'/>" % (x - rr * 0.6, y - rr * 0.8, rr, rr, x - rr * 0.6, y + rr * 0.8)
    return s


def band(x, y, wavy):
    s = "<rect x='%g' y='%g' width='120' height='40' rx='4' fill='#f2d7a6' stroke='%s' stroke-width='1.6'/>" % (x - 60, y, INK)
    if wavy:
        s += "<path d='M%g %g q10 -8 20 0 t20 0 t20 0 t20 0 t20 0' fill='none' stroke='#c0392b' stroke-width='2.5'/>" % (x - 50, y + 4)
    else:
        s += "<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#c0392b' stroke-width='2.5'/>" % (x - 50, y + 4, x + 50, y + 4)
    return s


def rice_drum(x, y, jump):
    k = 1.4
    s = K.icon("drum", x, y, k)
    for i in range(6):
        dx = (-17 + i * 7) * k
        dy = -12 * k + R.uniform(-3, 3) - (R.randint(14, 30) if jump else 0)
        s += "<ellipse cx='%g' cy='%g' rx='4.5' ry='2.6' fill='#fff' stroke='%s' stroke-width='0.8'/>" % (x + dx, y + dy, INK)
    return s


def scene(kind, on):
    """kind: drum, bell, band, rice; on: vibrating or still"""
    if kind == "band":
        s = band(100, 50, on) + (shake(100, 54, 2, 30) if on else "")
        lab = "a rubber band on a box, %s" % ("vibrating" if on else "still")
    elif kind == "rice":
        s = rice_drum(100, 76, on)
        lab = "rice on a drum, %s" % ("jumping" if on else "not moving")
    else:
        s = K.icon(kind, 100, 62, 1.2) + (shake(100, 62, 3, 34) if on else "")
        lab = "a %s, %s" % (kind, "vibrating" if on else "still")
    return svg_wrap(200, 120, s, lab)


THINGS = [("drum", "You hit a drum."), ("bell", "You ring a bell."), ("band", "You pluck a rubber band."), ("rice", "You tap a drum with rice on it.")]


def g_pic():
    kind, act = R.choice(THINGS)
    on = R.random() < 0.6
    who = P.next()[0]
    k = R.choice(["sound", "moving"])
    if not once((kind, on, k if kind != "rice" else ""), 1):
        return None
    pic = fig(scene(kind, on))
    if kind == "rice":
        if on:
            return item(pic + "%s taps the drum. The rice jumps. Why?" % who, "The drum is vibrating.", ["The rice is alive.", "The wind blew it.", "The drum is still."],
                        "The drum shakes fast. That makes the rice jump.")
        return item(pic + "The rice on %s's drum is still. Is the drum making sound?" % who, "No. It is not vibrating.", ["Yes. It is very loud.", "Yes. Rice makes sound.", "Yes. All drums make sound."],
                    "No vibration, no sound.")
    nm = {"drum": "drum", "bell": "bell", "band": "rubber band"}[kind]
    if k == "sound":
        if on:
            return item(pic + "%s sees the %s shake. What does it make?" % (who, nm), "sound", ["light", "water", "nothing"], "Shaking makes sound.")
        return item(pic + "%s's %s is still. Does it make sound?" % (who, nm), "No.", ["Yes, a loud sound.", "Yes, a soft sound.", "Yes, it sings."], "Still things do not make sound.")
    if on:
        return item(pic + "%s's %s makes sound. What is it doing?" % (who, nm), "vibrating", ["sleeping", "melting", "standing still"], "Sound comes from vibrating things.")
    return item(pic + "%s wants the %s to make sound. What should %s do?" % (who, nm, who),
                {"drum": "hit it", "bell": "ring it", "band": "pluck it"}[kind], ["look at it", "whisper to it", "put it away"], "Make it vibrate.")


ACTS = [("hit a drum", "the drum skin"), ("ring a bell", "the bell"), ("pluck a guitar string", "the string"), ("hum a song", "your throat"),
        ("strum a ukulele", "the strings"), ("bang a pot with a spoon", "the pot"), ("blow a whistle", "the air inside the whistle"),
        ("tap a xylophone", "the bars"), ("snap a rubber band", "the rubber band"), ("clap", "your hands and the air"),
        ("listen to a bee buzz", "the bee's wings"), ("pet a purring cat", "the cat's throat"), ("hear a cricket chirp", "the cricket's wings"),
        ("play a piano key", "a string inside the piano"), ("play a violin", "the strings"), ("shake a tambourine", "the skin and the little metal jingles")]


def g_what():
    a, part = R.choice(ACTS)
    who = P.next()[0]
    if not once(a):
        return None
    w = R.sample([x[1] for x in ACTS if x[1] != part], 2) + ["nothing"]
    return item("%s likes to %s. What vibrates to make the sound?" % (who, a), part, w, "%s vibrates." % (part[0].upper() + part[1:]))


STOP = [("A bell is ringing.", "hold the bell", ["ring it again", "shake it", "hit it harder"]),
        ("A drum is booming.", "put a hand on the drum", ["hit it again", "shake it", "tap it fast"]),
        ("A guitar string is buzzing.", "touch the string", ["pluck it again", "strum it", "pull it harder"]),
        ("A pot lid is ringing.", "hold the lid", ["bang it again", "drop it", "tap it"]),
        ("A rubber band is twanging.", "pinch the rubber band", ["pluck it again", "stretch it more", "snap it"]),
        ("A cymbal is crashing.", "grab the cymbal", ["hit it again", "spin it", "tap it"]),
        ("A triangle is ringing.", "hold the triangle", ["tap it again", "swing it", "shake it"]),
        ("A wind chime is jingling.", "hold the chimes still", ["blow on it", "shake it", "tap it"]),
        ("A xylophone bar is ringing.", "touch the bar", ["tap it again", "hit it harder", "shake it"])]


def g_stop():
    s, a, w = R.choice(STOP)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s %s wants it to stop. What should %s do?" % (s, who, who), a, w, "Stop the vibrating. Then the sound stops.")


EVID = [("A tuning fork is put in water.", "The water splashes.", "It is vibrating."),
        ("Rice is on a drum. Lily taps the drum.", "The rice jumps.", "The drum is vibrating."),
        ("Ben puts his hand on his throat and hums.", "He feels a buzz.", "His throat is vibrating."),
        ("A loud truck goes by.", "The window shakes.", "Sound made the window vibrate."),
        ("Music plays loud from a speaker.", "Paper on the speaker jumps.", "The speaker is vibrating."),
        ("A big drum is hit next to a small drum.", "Rice on the small drum jumps.", "Sound made the small drum vibrate."),
        ("Sam plucks a rubber band.", "It looks blurry.", "It is moving back and forth fast.")]


def g_evid():
    s, see, mean = R.choice(EVID)
    if not once(s):
        return None
    w = R.sample([x[2] for x in EVID if x[2] != mean], 2) + ["Nothing is moving."]
    return item("%s %s What does this show?" % (s, see), mean, w, "Shaking is a clue. That is vibrating.")


def g_loud():
    who = P.next()[0]
    k = R.choice(["hard", "soft", "big"])
    nm = R.choice(["drum", "bell", "pot"])
    if not once((k, nm)):
        return None
    if k == "hard":
        return item(fig(K.card("drum" if nm == "pot" else nm)) + "%s hits the %s harder. What happens?" % (who, nm), "The sound gets louder.", ["The sound stops.", "The sound gets softer.", "It turns to light."],
                    "Bigger vibrations make louder sound.")
    if k == "soft":
        return item(fig(K.card("drum" if nm == "pot" else nm)) + "%s taps the %s very gently. How is the sound?" % (who, nm), "soft", ["very loud", "no sound at all", "bright"],
                    "Small vibrations make soft sound.")
    return item("%s's %s makes big vibrations. What kind of sound does it make?" % (who, nm), "a loud sound", ["a soft sound", "no sound", "a light"], "Big vibrations = loud.")


FEEL = [("a speaker playing music", "a buzz"), ("your throat when you sing", "a buzz"), ("a drum after you hit it", "a buzz"),
        ("a guitar when you strum it", "a buzz"), ("a table when someone bangs on it", "a buzz"), ("a phone when it rings", "a buzz"),
        ("a piano when someone plays it", "a buzz"), ("a door when someone knocks", "a buzz")]


def g_feel():
    th, a = R.choice(FEEL)
    who = P.next()[0]
    if not once(th):
        return None
    return item("%s gently touches %s. What does %s feel?" % (who, th, who), "a buzz (vibrating)", ["nothing at all", "something hot", "something wet"], "Things that make sound vibrate.")


def g_which():
    kinds = ["drum", "bell", "band"]
    R.shuffle(kinds)
    on = R.randrange(3)
    who = P.next()[0]
    neg = R.random() < 0.4
    if not once((tuple(kinds), on, neg)):
        return None
    s = ""
    for i, k in enumerate(kinds):
        x = 80 + i * 150
        if k == "band":
            s += band(x, 40, i == on) + (shake(x, 44, 2, 30) if i == on else "")
        else:
            s += K.icon(k, x, 56, 0.8) + (shake(x, 56) if i == on else "")
        s += text(x, 120, "ABC"[i], 16)
    pic = svg_wrap(450, 130, s, "a drum, a bell and a rubber band; only one is shaking")
    nm = {"drum": "drum", "bell": "bell", "band": "rubber band"}
    if neg:
        off = [i for i in range(3) if i != on]
        return item(fig(pic) + "%s looks closely. Which one is vibrating?" % who, "%s (%s)" % ("ABC"[on], nm[kinds[on]]),
                    ["%s (%s)" % ("ABC"[i], nm[kinds[i]]) for i in off] + ["all of them"], "Shake lines show vibrating.")
    return item(fig(pic) + "%s hears a sound. Which one is making it?" % who, "%s (%s)" % ("ABC"[on], nm[kinds[on]]),
                ["%s (%s)" % ("ABC"[i], nm[k]) for i, k in enumerate(kinds) if i != on] + ["none of them"], "The one with shake lines is vibrating.")


B3 = bank([
    ("Ava wants to show that sound makes things vibrate. What can she do?", "play a loud drum next to paper with rice on it", ["read a book", "turn off the lights", "eat a snack"], "Watch the rice."),
    ("Leo wants to feel his voice. What can he do?", "touch his throat while he talks", ["touch his toes", "close his eyes", "hold his breath"], "His throat vibrates."),
    ("Mia wants to see a rubber band vibrate. What should she do?", "stretch it and pluck it", ["leave it in a box", "cut it", "paint it"], "Plucking makes it shake."),
    ("Kai puts a tuning fork in water. Why does he do this?", "to see the vibrations make splashes", ["to clean it", "to cool the water", "to make it heavy"], "Water shows shaking."),
    ("Zoe wants to stop a sound. What should she test?", "holding the thing that is vibrating", ["making it vibrate more", "hitting it harder", "shaking it"], "Stop the shaking."),
    ("Sam puts his hand on a speaker. Why?", "to feel it vibrate", ["to warm his hand", "to turn it off", "to see light"], "Speakers vibrate."),
])
B1 = bank([
    ("What makes sound?", "things that vibrate", ["things that are still", "only the sun", "only water"], "Vibrate means shake fast."),
    ("What does vibrate mean?", "shake back and forth fast", ["stay very still", "get hot", "change color"], "Look for shaking."),
    ("Where do you feel a buzz when you talk?", "in your throat", ["in your toes", "in your hair", "nowhere"], "Your throat vibrates."),
    ("How do you stop a bell?", "hold it", ["ring it", "shake it", "hit it"], "No shake, no sound."),
    ("Can sound make things shake?", "Yes. Loud sound can make things vibrate.", ["No, never.", "Only light can.", "Only water can."], "A loud truck shakes a window."),
    ("A drum is still. Does it make sound?", "no", ["yes, loud", "yes, soft", "yes, always"], "It must vibrate."),
    ("Which one vibrates when you play it?", "a guitar string", ["a book", "a rock", "a pillow"], "Pluck it. It shakes."),
    ("Why does rice jump on a drum?", "The drum vibrates.", ["The rice is hungry.", "The rice is hot.", "The drum is cold."], "Rice shows the shaking."),
])
B5 = bank([
    ("Ava wants to see a drum vibrate. What can she put on it?", "rice or sand", ["a big book", "a blanket", "nothing"], "Small things jump. You can see it."),
    ("Leo holds a ringing bell. What happens?", "The sound stops.", ["It gets louder.", "It rings forever.", "It turns blue."], "His hand stops the vibrating."),
    ("Mia plucks a short rubber band and a long one. What do both do?", "vibrate and make sound", ["stay still", "melt", "make light"], "Plucking makes them shake."),
    ("Kai hums with his hand on his throat. Then he stops. What changes?", "The buzz stops.", ["The buzz gets bigger.", "His hand gets hot.", "Nothing changes."], "No sound, no vibrating."),
    ("A loud drum is next to a glass of water. The water ripples. Why?", "The sound makes the water vibrate.", ["The water is hot.", "A fish is in it.", "The glass is broken."], "Sound can make things vibrate."),
])


def body():
    pic = svg_wrap(400, 120, K.icon("drum", 100, 60, 0.9) + shake(100, 60) + K.icon("bell", 300, 60, 0.9) + shake(300, 60), "a drum and a bell vibrating")
    ex = [("You hit a drum. What makes the sound?", ["The drum shakes."], "the vibrating drum"),
          ("You hold a ringing bell. What happens?", ["It stops shaking."], "The sound stops.")]
    mist = ["Thinking still things make sound.",
            "Thinking you cannot see vibrations. Rice on a drum shows them.",
            "Thinking sound cannot move things."]
    return kid_lesson(pic, "Sound comes from shaking.",
                      ["Vibrate = shake fast.", "Stop the shaking. The sound stops.", "Loud sound can shake things."], ex, mist)


def main():
    sets = U.sets([
        ("What makes sound?", B1 + [(g_pic, 6), (g_what, 6)]),
        ("Things that vibrate", [(g_what, 8), (g_which, 6), (g_feel, 6)]),
        ("Stop the sound", [(g_stop, 8), (g_pic, 5), (g_loud, 5), (g_evid, 2)]),
        ("Seeing vibrations", B3 + [(g_evid, 5), (g_which, 9)]),
        ("Sound scientists", B5 + [(g_which, 10), (g_loud, 3), (g_feel, 2)]),
    ])
    make("grade-1", "sound-and-vibrations", 1, "1-PS4-1",
         "Plan and conduct investigations to provide evidence that vibrating materials can make sound and that sound can make materials vibrate.",
         "Sound and Vibrations",
         "Grade 1 Sound and Vibrations Worksheets: What Makes Sound?",
         "Sound",
         "Free grade 1 science worksheets on sound and vibrations (NGSS 1-PS4-1): drums, bells and rubber bands, stopping sounds and seeing vibrations. 100 picture questions with answers.",
         "Sound comes from shaking.",
         "Things vibrate to make sound. Loud sound can shake things too.",
         body(),
         [("What makes sound?", "Things that vibrate, or shake back and forth fast: a drum skin, a bell, a guitar string or your throat."),
          ("How can kids see vibrations?", "Put rice on a drum and tap it, or put a ringing tuning fork in water."),
          ("Can sound make things vibrate?", "Yes. A loud drum can make rice on another drum jump, and a loud truck can shake a window.")],
         sets)


if __name__ == "__main__":
    main()
