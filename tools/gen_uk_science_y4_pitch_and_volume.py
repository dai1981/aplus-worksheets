# -*- coding: utf-8 -*-
"""
UK Year 4 science: Pitch and Volume (Sound)
  python tools/gen_uk_science_y4_pitch_and_volume.py
Pitch depends on the object making the sound (length, tightness, thickness, size); volume depends on the strength of
the vibrations; sounds get fainter with distance; decibels and safe listening; bottle and sound-meter investigations.
Wrong answers come from real mistakes: "a longer string gives a higher note", "pitch and volume are the same thing",
"hitting a drum harder makes a higher note", "sounds get louder as you move away".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61411)
R = U.R
P = People(R)

PIT = [("a guitar string is made shorter", "higher"), ("a guitar string is tightened", "higher"), ("a thinner guitar string is plucked", "higher"),
       ("a guitar string is loosened", "lower"), ("a longer xylophone bar is hit", "lower"), ("a smaller drum is hit", "higher"),
       ("a bigger drum is hit", "lower"), ("more holes are covered on a recorder (longer column of air)", "lower"),
       ("a glass bottle with more water in it is tapped", "lower"), ("you blow across a bottle with more water in it (less air)", "higher")]


def g_pitch():
    s, a = R.choice(PIT)
    if not once(("pi", s)):
        return None
    return item("What happens to the pitch when %s?" % s, "It gets %s." % a, ["It gets %s." % ("lower" if a == "higher" else "higher"), "It does not change.", "It only gets louder."],
                "Shorter, tighter, thinner and smaller things vibrate faster and make higher notes.")


HOW = [("make a guitar note higher", "press the string to make it shorter", ["use a longer string", "loosen the string", "pluck it harder"]),
       ("make a guitar note lower", "loosen the string", ["tighten the string", "make the string shorter", "pluck it more gently"]),
       ("make a drum sound louder", "hit it harder", ["hit it more gently", "use a smaller drum", "cover it with a cloth"]),
       ("make a drum sound quieter", "hit it more gently", ["hit it harder", "use a bigger drum", "stand closer to it"]),
       ("make a higher note on a xylophone", "hit a shorter bar", ["hit a longer bar", "hit the same bar harder", "hit it more slowly"]),
       ("make a recorder play a higher note", "cover fewer holes", ["cover more holes", "blow more gently only", "use a longer recorder"]),
       ("make an elastic band twang at a higher pitch", "stretch it tighter", ["make it looser", "use a thicker band", "pluck it more gently"]),
       ("make a sound quieter for someone across the room", "make smaller vibrations or move further away", ["make bigger vibrations", "move closer", "shout"])]


def g_how():
    q, a, w = R.choice(HOW)
    if not once(("hw", q)):
        return None
    return item("How could you %s?" % q, a, w, "Pitch depends on the size and tightness of what vibrates; volume depends on how big the vibrations are.")


def g_dist():
    who = P.next()[0]
    d = [1, 2, 4, 8]
    start = R.choice([84, 86, 88, 90, 92])
    v = [start, start - 6, start - 12, start - 18]
    v = [x + R.choice([-1, 0, 1]) for x in v]
    k = R.choice(["read", "read", "pattern", "predict", "diff"])
    ri = R.randrange(4)
    if not once(("ds", tuple(v), k, ri if k == "read" else 0)) or (k == "pattern" and not once(("dp",), 3)):
        return None
    tab = table(["Distance from the speaker (m)", "Sound level (dB)"], [[str(a), str(b)] for a, b in zip(d, v)])
    intro = tab + "%s measured a speaker with a sound level meter at different distances. " % who
    if k == "read":
        g = "%d dB" % v[ri]
        return item(intro + "What was the sound level at %d m?" % d[ri], g, uniq(g, ["%d dB" % x for x in v] + ["%d dB" % (v[ri] + 4)]), "Read the row.")
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The further from the speaker, the quieter the sound.", ["The further away, the louder the sound.", "Distance makes no difference.", "The sound gets higher-pitched further away."],
                    "Sound spreads out and gets fainter with distance.")
    if k == "predict":
        return item(intro + "Predict the sound level at 16 m.", "less than %d dB" % v[3], ["more than %d dB" % v[0], "exactly %d dB" % v[1], "between %d and %d dB" % (v[1], v[0])], "The pattern continues: further away is quieter.")
    g = "%d dB" % (v[0] - v[3])
    return item(intro + "How much quieter was it at 8 m than at 1 m?", g, uniq(g, ["%d dB" % v[3], "%d dB" % v[0], "%d dB" % (v[0] - v[3] + 4), "7 dB"]), "%d − %d = %d dB." % (v[0], v[3], v[0] - v[3]))


DB = [("rustling leaves", 20), ("a whisper", 30), ("normal talking", 60), ("a busy classroom", 70), ("a vacuum cleaner", 75), ("heavy traffic", 85),
      ("a lawnmower", 90), ("a rock concert", 110), ("a jet plane taking off", 140)]


def g_db():
    k = R.choice(["cmp", "cmp", "read", "safe"])
    tab = table(["Sound", "Sound level (dB)"], [[a, str(b)] for a, b in DB])
    if k == "cmp":
        a, b = R.sample(DB, 2)
        if not once(("dc", tuple(sorted((a[0], b[0]))))):
            return None
        lo = a if a[1] > b[1] else b
        return item(tab + "Which is louder: %s or %s?" % (a[0], b[0]), lo[0], [(b if lo is a else a)[0], "They are equally loud.", "You cannot compare sounds."], "More decibels means louder.")
    if k == "read":
        a, b = R.choice(DB)
        if not once(("dr", a)):
            return None
        g = "%d dB" % b
        return item(tab + "What is the sound level of %s?" % a, g, uniq(g, ["%d dB" % x for _, x in DB]), "Read the row.")
    a = R.choice([x for x in DB if x[1] > 85])
    if not once(("dsf", a[0])):
        return None
    w = R.sample([x[0] for x in DB if x[1] < 85], 3)
    return item(tab + "Sounds above about 85 dB can damage hearing over time. Which of these could damage your hearing?", a[0], w, "Protect your ears from very loud sounds.")


def g_bottle():
    who = P.next()[0]
    mls = sorted(R.sample([50, 100, 150, 200, 250, 300, 350], 4))
    k = R.choice(["taphi", "taplo", "blowhi", "blowlo"])
    if not once(("bo", tuple(mls), k)):
        return None
    tab = table(["Bottle", "Water in it (ml)"], [["Bottle %s" % "ABCD"[i], str(m)] for i, m in enumerate(mls)])
    names = ["Bottle %s" % "ABCD"[i] for i in range(4)]
    if k == "taphi":
        return item(tab + "%s taps each identical glass bottle with a spoon. Which bottle makes the highest note?" % who, names[0], names[1:], "Tapping: the glass and water vibrate; less water gives a higher note.")
    if k == "taplo":
        return item(tab + "%s taps each identical glass bottle with a spoon. Which bottle makes the lowest note?" % who, names[3], names[:3], "Tapping: more water gives a lower note.")
    if k == "blowhi":
        return item(tab + "%s blows across the top of each identical bottle. Which makes the highest note?" % who, names[3], names[:3], "Blowing: the air vibrates; the most water leaves the shortest column of air and the highest note.")
    return item(tab + "%s blows across the top of each identical bottle. Which makes the lowest note?" % who, names[0], names[1:], "Blowing: the least water leaves the longest column of air and the lowest note.")


B1 = bank([
    ("What is pitch?", "how high or low a sound is", ["how loud or quiet a sound is", "how fast sound travels", "how far a sound goes"], "A whistle is high; a tuba is low."),
    ("What is volume?", "how loud or quiet a sound is", ["how high or low a sound is", "the size of the instrument", "the speed of sound"], "Measured in decibels (dB)."),
    ("What makes a sound louder?", "bigger, stronger vibrations", ["faster vibrations only", "a shorter string", "a smaller drum"], "More energy in the vibrations."),
    ("What makes a sound higher in pitch?", "faster vibrations", ["bigger vibrations", "slower vibrations", "louder vibrations"], "Shorter or tighter things vibrate faster."),
    ("What happens to a sound as you walk away from it?", "It gets quieter (fainter).", ["It gets louder.", "It gets higher.", "It stays the same."], "The sound spreads out."),
    ("What unit measures how loud a sound is?", "decibels (dB)", ["degrees", "metres", "newtons"], "A sound level meter reads decibels."),
    ("Which usually makes a higher note: a small drum or a big drum?", "a small drum", ["a big drum", "they make the same note", "neither makes a note"], "Smaller vibrates faster."),
    ("Why do ear defenders protect hearing?", "They absorb sound so less reaches the ears.", ["They make sounds louder.", "They change the pitch.", "They stop vibrations everywhere."], "Muffling sound."),
])
B5 = bank([
    ("How could you test whether string length affects pitch?", "Pluck strings of different lengths with the same tightness and thickness and compare the notes.", ["Use strings of different thickness too.", "Pluck each one at a different strength.", "Only listen once."], "Fair test."),
    ("Why do people who work with loud machines wear ear protection?", "Long exposure to loud sounds can damage hearing.", ["To keep warm.", "To hear better.", "To make the machine quieter."], "Health and safety."),
    ("A pupil says hitting a drum harder makes a higher note. Is this right?", "No. It makes a louder sound, not a higher one.", ["Yes, always.", "Yes, but only small drums.", "No, it makes the sound quieter."], "Volume and pitch are different."),
    ("Why is a sound level meter better than just listening?", "It gives a measurement, so results can be compared fairly.", ["It is louder.", "It changes the pitch.", "Ears cannot hear."], "Measure, do not guess."),
    ("Why do double bass strings make lower notes than violin strings?", "They are longer and thicker, so they vibrate more slowly.", ["They are tighter and shorter.", "They are made of glass.", "They are played louder."], "Size affects pitch."),
])


def body():
    think = ("<p><b>Pitch is how high or low a sound is; volume is how loud it is.</b></p>"
             "<ul><li>Shorter, tighter, thinner and smaller objects vibrate faster and make higher notes.</li>"
             "<li>Bigger vibrations make louder sounds. Sounds get fainter the further you are from them.</li>"
             "<li>Volume is measured in decibels (dB); sounds above about 85 dB can damage hearing over time.</li></ul>")
    ex = [("Tighten a guitar string. Pitch?", ["Tighter vibrates faster"], "higher"),
          ("Hit a drum harder. Change?", ["Bigger vibrations"], "louder, not higher")]
    mist = ["Thinking a longer string gives a higher note.", "Mixing up pitch and volume.", "Thinking sounds get louder as you move away."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Pitch and volume", B1 + [(g_pitch, 8), (g_how, 4)]),
        ("Changing the sound", [(g_pitch, 2), (g_how, 4), (g_bottle, 14)]),
        ("Sound and distance", [(g_dist, 20)]),
        ("Decibels", [(g_db, 16), (g_bottle, 4)]),
        ("Investigating sound", B5 + [(g_db, 8), (g_dist, 7)]),
    ])
    make_uk(4, "pitch-and-volume", 11, "Sound",
            "Find patterns between the pitch of a sound and features of the object that produced it. Find patterns between the volume of a sound and the strength of the vibrations that produced it. "
            "Recognise that sounds get fainter as the distance from the sound source increases.",
            "Pitch and Volume",
            "Year 4 Science: Pitch and Volume Worksheets (High and Low, Loud and Quiet)",
            "Pitch and Volume",
            "Free Year 4 science worksheets on pitch and volume: high and low notes, loud and quiet sounds, distance, decibels, and bottle and sound meter investigations. 100 questions with answers.",
            "Pitch: high or low. Volume: loud or quiet.",
            "Shorter and tighter means higher; bigger vibrations mean louder.",
            body(),
            [("What is the difference between pitch and volume?", "Pitch is how high or low a sound is. Volume is how loud or quiet it is. A sound can be high and quiet, or low and loud."),
             ("How can you change the pitch of a string?", "Make it shorter, tighter or thinner for a higher note, or longer, looser or thicker for a lower note."),
             ("Why do sounds get quieter further away?", "The vibrations spread out as they travel, so less of the sound's energy reaches your ears.")],
            sets)


if __name__ == "__main__":
    main()
