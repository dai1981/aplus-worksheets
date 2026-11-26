# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Sending Information with Patterns (4-PS4-3)
  python tools/gen_us_science_g4_sending_information_with_patterns.py
Information can be sent over distance with patterns: drums, flashes of light, Morse code,
flags, and the 1s and 0s (on/off) that phones and computers use. Students decode simple codes
with a key and compare solutions using criteria (distance, speed, works in the dark or noise).
Wrong answers come from real mistakes: "a code must use words", "light signals work around walls",
"sound signals work best in a noisy place".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, svg_wrap, circle, rect, text, People, INK, SUN, GRAY

U = Unit(40108)
R = U.R
P = People(R)

MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "G": "--.", "H": "....", "I": "..", "M": "--", "N": "-.", "O": "---", "S": "...", "T": "-", "U": "..-", "W": ".--"}
WORDS = ["SOS", "HI", "GO", "DOG", "CAT", "SUN", "HAT", "MOM", "WIN", "TOE", "HUG", "SIT", "NOW", "GUM", "MUD", "SAD", "BUG", "BUS", "DIG", "WET", "TEN", "HOT", "NET"]


def ms(word):
    return " / ".join(" ".join("dot" if c == "." else "dash" for c in MORSE[ch]) for ch in word)


def sym(word):
    return "&nbsp;&nbsp;/&nbsp;&nbsp;".join(MORSE[ch].replace(".", "•").replace("-", "—") for ch in word)


def key_table(letters):
    rows = [[ch, MORSE[ch].replace(".", "•").replace("-", "—")] for ch in sorted(letters)]
    return table(["Letter", "Code"], rows)


def g_decode():
    w = R.choice([x for x in WORDS if all(c in MORSE for c in x)])
    extra = R.sample([c for c in MORSE if c not in w], 3)
    letters = set(w) | set(extra)
    wrong = set()
    for _ in range(40):
        ww = list(w)
        i = R.randrange(len(ww))
        ww[i] = R.choice(sorted(letters))
        ww = "".join(ww)
        if ww != w:
            wrong.add(ww)
    if len(wrong) < 3:
        return None
    rev = w[::-1]
    wl = R.sample(sorted(wrong), 3)
    if rev != w and rev not in wl and R.random() < 0.5:
        wl[0] = rev
    return item(key_table(letters) + "Use the key. A slash (/) separates letters. What word does this message spell?<br><b>%s</b>" % sym(w), w, wl,
                "Read each group of dots and dashes and find it in the key: %s." % ", ".join("%s = %s" % (MORSE[c].replace(".", "•").replace("-", "—"), c) for c in w))


def g_encode():
    w = R.choice([x for x in WORDS if all(c in MORSE for c in x) and len(set(x)) >= 2])
    extra = R.sample([c for c in MORSE if c not in w], 2)
    letters = set(w) | set(extra)
    right = sym(w)
    wrongs = set()
    for _ in range(40):
        ww = list(w)
        i = R.randrange(len(ww))
        ww[i] = R.choice(sorted(letters))
        if "".join(ww) != w:
            wrongs.add(sym("".join(ww)))
    wrongs.add(sym(w[::-1]))
    wrongs.discard(right)
    if len(wrongs) < 3:
        return None
    return item(key_table(letters) + "Which code spells the word <b>%s</b>?" % w, right, R.sample(sorted(wrongs), 3),
                "Look up each letter of %s in the key and keep the letters in order." % w)


def lights(bits):
    s = []
    for i, b in enumerate(bits):
        s.append(circle(30 + 44 * i, 30, 16, SUN if b == "1" else "#ddd", INK, 2))
    return svg_wrap(30 + 44 * len(bits), 60, "".join(s), "a row of lights, some on and some off")


CODE2 = {"00": "stop", "01": "go left", "10": "go right", "11": "go straight"}


def g_lights():
    bits = R.choice(sorted(CODE2))
    k = R.choice(["read", "count"])
    if k == "read":
        rows = [["%s %s" % ("on" if b[0] == "1" else "off", "on" if b[1] == "1" else "off"), m] for b, m in sorted(CODE2.items())]
        return item(table(["Lights (left, right)", "Message"], rows) + fig(lights(bits)) + "A robot reads two lights. A yellow light is on; a gray light is off. What message is the robot getting?",
                    CODE2[bits], [m for b, m in CODE2.items() if b != bits], "Left light %s, right light %s means “%s.”" % ("on" if bits[0] == "1" else "off", "on" if bits[1] == "1" else "off", CODE2[bits]))
    n = R.choice([3, 4, 5, 6])
    return item("A code uses a row of %d lights. Each light can be on or off. How many different messages can it send?" % n, "%d" % (2 ** n),
                ["%d" % (2 * n), "%d" % n, "%d" % (2 ** n - 1) if n > 2 else "%d" % (2 ** n + 2)],
                "Each light doubles the number of patterns: " + " × ".join(["2"] * n) + " = %d." % (2 ** n))


SITU = [("across a noisy football stadium", "flashing lights or hand signals", ["shouting", "a quiet whistle", "whispering"], "Sound signals are hard to hear in a noisy place."),
        ("across a lake on a dark night", "flashing a flashlight in a pattern", ["waving a flag", "holding up a sign", "hand signals"], "Flags, signs and hand signals cannot be seen in the dark."),
        ("through a thick forest where trees block the view", "drum beats in a pattern", ["flashing a mirror", "waving a flag", "holding up colored cards"], "Sound can travel around trees; light signals need a clear view."),
        ("to a ship far out at sea at night", "a lamp flashing Morse code", ["shouting", "waving a flag", "a hand signal"], "A bright light can be seen far away at night."),
        ("to a friend on the other side of a wall", "knocking on the wall in a pattern", ["flashing a flashlight", "waving a flag", "holding up a sign"], "Light cannot go through the wall, but the knocks can be heard."),
        ("across a wide valley on a sunny day", "flashing sunlight off a mirror", ["whispering", "tapping a pencil", "clapping softly"], "A mirror flash can be seen from far away on a sunny day."),
        ("to another diver under water", "tapping on a metal tank in a pattern", ["shouting words", "waving a flag", "holding up a paper note"], "Taps travel well through water."),
        ("to a hiker on the other side of a foggy field", "blowing a whistle in a pattern", ["waving a flag", "flashing a mirror", "holding up a sign"], "Fog blocks the view, but sound still travels."),
        ("from a tall building to a friend in the next tower at night", "flashing a phone light in a pattern", ["shouting", "waving a hand", "holding up a drawing"], "A light can be seen across the gap in the dark.")]
SITU_LEFT = list(range(len(SITU)))
R.shuffle(SITU_LEFT)


def g_choose():
    if not SITU_LEFT:
        return None
    place, a, w, e = SITU[SITU_LEFT.pop()]
    p = P.next()
    return item("%s needs to send a message %s. Which way would work best?" % (p[0], place), a, w, e)


METH = {"drum beats": (100, 500, "No"), "flashlight code": (200, 800, "Yes"), "flag signals": (100, 400, "No"), "whistle code": (100, 300, "No"),
        "mirror flashes": (300, 900, "No"), "knock code": (5, 20, "Yes")}


def g_compare():
    meth = R.sample(sorted(METH), 3)
    rows = []
    vals = {}
    for m in meth:
        lo, hi, dark = METH[m]
        d = R.randrange(lo, hi + 1, 5)
        t = R.randint(5, 30)
        rows.append([m, "%d m" % d, "%d seconds" % t, dark])
        vals[m] = (d, t, dark)
    if len({v[0] for v in vals.values()}) < 3 or len({v[1] for v in vals.values()}) < 3:
        return None
    tab = table(["Method", "Farthest distance", "Time to send “HELP”", "Works in the dark?"], rows)
    k = R.choice(["far", "fast", "dark"])
    p = P.next()
    names = meth
    if k == "far":
        best = max(names, key=lambda m: vals[m][0])
        return item(tab + "%s's class tested three ways to send a message. Which method sends a message the farthest?" % p[0], best,
                    [m for m in names if m != best] + ["the fastest method"], "%s reached %d m." % (best.capitalize(), vals[best][0]))
    if k == "fast":
        best = min(names, key=lambda m: vals[m][1])
        return item(tab + "%s's class tested three ways to send a message. Which method sent “HELP” in the shortest time?" % p[0], best,
                    [m for m in names if m != best] + ["the method that goes farthest"], "%s took only %d seconds." % (best.capitalize(), vals[best][1]))
    yes = [m for m in names if vals[m][2] == "Yes"]
    if len(yes) != 1:
        return None
    return item(tab + "A message must be sent at night. Using %s's data, which method meets this criterion?" % p[0], yes[0],
                [m for m in names if m != yes[0]] + ["none of them"], "Only %s works in the dark." % yes[0])


B1 = bank([
    ("What is a code?", "a set of patterns that stand for messages or letters", ["a kind of light bulb", "a loud sound", "a type of wave that carries water"],
     "In Morse code, short and long signals stand for letters."),
    ("Which of these sends information using a pattern?", "a lighthouse flashing two times, then waiting", ["a lamp that is always on", "a rock on a beach", "a quiet room"],
     "A repeating on-off pattern can carry a message."),
    ("In Morse code, what are the two kinds of signals?", "short signals (dots) and long signals (dashes)", ["red and blue lights", "loud and soft words", "hot and cold"],
     "Dots and dashes can be sent as sounds, flashes or taps."),
    ("Phones and computers send information as patterns of", "on and off signals (1s and 0s)", ["colors of paint", "drops of water", "pieces of paper"],
     "Digital information is stored and sent as patterns of 1s and 0s."),
    ("What is the famous Morse code message for help?", "SOS", ["HI", "GO", "OK"], "SOS is three dots, three dashes, three dots."),
    ("Long ago, how could people on hills send a warning to towns far away?", "by lighting fires or smoke signals in a pattern", ["by whispering", "by writing in sand", "by mailing a letter that took weeks"],
     "Patterns of fire and smoke can be seen from far away."),
    ("What must the sender and the receiver both know for a code to work?", "what each pattern means (the key)", ["how heavy the message is", "the color of the sender's shirt", "nothing at all"],
     "Without the key, the receiver cannot decode the message."),
    ("Which signal would be hardest to see on a foggy day?", "a flag waved far away", ["a loud foghorn", "a bell", "a drum"], "Fog blocks light, but sound still travels."),
])
B5 = bank([
    ("Ava's team wants to send a message to a friend in another room without words. Which is a good criterion for their design?", "The friend must understand the message correctly.", ["The message must be secret from everyone, even the friend.", "The design must be blue.", "The message must be as long as possible."],
     "A criterion tells what the solution must do."),
    ("Two teams send the same message. Team A's light code took 20 seconds. Team B's drum code took 35 seconds. If speed is the criterion, which is better?", "Team A's light code", ["Team B's drum code", "They are the same.", "You cannot compare them."],
     "20 seconds is faster than 35 seconds."),
    ("Leo's code uses a long beep for every letter. Why is this a problem?", "Every letter would look the same, so the message could not be read.", ["Long beeps are too quiet.", "Beeps cannot travel.", "There is no problem."],
     "Each letter needs its own pattern."),
    ("A train signal shows red, yellow or green lights. What is this an example of?", "using a pattern of lights to send information", ["using sound to send information", "making energy from nothing", "a solar panel"],
     "Each color has a meaning the driver knows."),
    ("Why do ships use flag codes during the day and light codes at night?", "Flags can be seen in daylight, but only lights can be seen in the dark.", ["Flags are too heavy at night.", "Lights do not work in the day.", "Ships cannot hear sounds."],
     "Engineers pick a solution that fits the conditions."),
    ("Mia sends a message by flashing a light: short, long, long. Her friend writes “• — —”. What did her friend do?", "decoded the light pattern into dots and dashes", ["made the light brighter", "sent a new message", "changed the code"],
     "The friend turned the flashes back into a pattern to read with the key."),
])


def body():
    think = ("<p>People can send information over a distance using <b>patterns</b>. A <b>code</b> is a set of patterns with meanings that the sender and receiver both know.</p>"
             "<ul><li><b>Morse code</b>: short signals (•) and long signals (—) stand for letters. They can be sent as beeps, flashes or taps.</li>"
             "<li><b>Lights and flags</b>: each pattern or color means something, like a traffic light.</li>"
             "<li><b>Computers and phones</b>: send information as patterns of on and off, written as 1s and 0s.</li></ul>"
             "<p>To choose the best way, compare solutions using <b>criteria</b>: How far must the message go? Is it dark or noisy? How fast must it arrive?</p>")
    ex = [("With the key • — = A and — • = N, what does “• — / — •” spell?", ["• — is A.", "— • is N."], "AN"),
          ("Which signal works best in a noisy gym?", ["Sound is hard to hear in noise.", "Light can still be seen."], "a flashing light or hand signal")]
    mist = ["Reading the letters in the wrong order.",
            "Choosing a light signal when there is a wall or fog in the way.",
            "Choosing a sound signal in a very noisy place."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Codes and patterns", B1 + [(g_decode, 6), (g_lights, 6)]),
        ("Decoding messages", [(g_decode, 12), (g_encode, 8)]),
        ("Light and on-off codes", [(g_lights, 10), (g_encode, 6), (g_decode, 4)]),
        ("Choosing the best way to send a message", [(g_choose, 7), (g_compare, 9), (g_lights, 4)]),
        ("Comparing solutions", B5 + [g_compare, g_choose, g_decode, g_encode]),
    ])
    make("grade-4", "sending-information-with-patterns", 8, "4-PS4-3",
         "Generate and compare multiple solutions that use patterns to transfer information.",
         "Sending Information with Patterns",
         "Grade 4 Codes and Patterns Worksheets: Morse Code, Light Signals and Sending Information",
         "Sending Information",
         "Free Grade 4 science worksheets on sending information with patterns (NGSS 4-PS4-3): Morse code with a key, light and on-off codes, and comparing ways to send messages using criteria. 100 practice questions with answers.",
         "Patterns can carry information over a distance.",
         "A code is a set of patterns that the sender and receiver both understand, like Morse code or on-off lights.",
         body(),
         [("How can patterns send information?", "Each pattern stands for a letter or a message. The receiver uses a key to decode it, like dots and dashes in Morse code."),
          ("How do phones and computers send information?", "They send patterns of on and off signals, written as 1s and 0s."),
          ("How do you choose the best way to send a message?", "Compare the solutions using criteria such as distance, speed, and whether it works in the dark or in a noisy place.")],
         sets)


if __name__ == "__main__":
    main()
