# -*- coding: utf-8 -*-
"""
UK Year 4 science: How Sounds Are Made (Sound)
  python tools/gen_uk_science_y4_how_sounds_are_made.py
Sounds are made by vibrations, which travel through a medium (solid, liquid or gas) to the ear. What vibrates in
different instruments, how the ear hears, why sound cannot travel through space, the speed of sound and echoes,
and string telephones.
Wrong answers come from real mistakes: "sound travels through empty space", "sound travels faster than light",
"in a recorder the plastic tube makes the sound" (the air inside vibrates), "a slack string telephone works best".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61410)
R = U.R
P = People(R)

VIB = [("a guitar", "the strings"), ("a drum", "the drum skin"), ("a recorder", "the air inside the tube"), ("your voice", "your vocal cords"),
       ("a xylophone", "the wooden or metal bars"), ("a violin", "the strings, rubbed by the bow"), ("a triangle", "the metal triangle"),
       ("a trumpet", "the player's lips and the air in the tube"), ("a tambourine", "the skin and the small metal discs"), ("a loudspeaker", "the cone inside it")]


def g_vib():
    i, v = R.choice(VIB)
    if not once(("vi", i)):
        return None
    return item("When %s makes a sound, what is vibrating?" % i, v, R.sample([x[1] for x in VIB if x[1] != v], 3), "All sounds are made by something vibrating.")


EAR = ["Something vibrates and makes the air vibrate.", "The vibrations travel through the air into the ear.", "The eardrum vibrates.",
       "Tiny bones pass the vibrations to the inner ear.", "Nerves send a message to the brain, and we hear the sound."]


def g_ear():
    i = R.randrange(len(EAR) - 1)
    k = R.random() < 0.5
    if not once(("ea", i, k)):
        return None
    if k:
        a = EAR[i + 1]
        return item("\"%s\" What happens next?" % EAR[i], a, R.sample([x for x in EAR if x not in (a, EAR[i])], 3), "Vibration → air → eardrum → tiny bones → nerves → brain.")
    a = EAR[i]
    return item("\"%s\" What happened just before?" % EAR[i + 1], a, R.sample([x for x in EAR if x not in (a, EAR[i + 1])], 3), "Vibration → air → eardrum → tiny bones → nerves → brain.")


MED = [("through the air", "yes"), ("through water", "yes"), ("through a wooden table", "yes"), ("through a steel railway line", "yes"), ("through a brick wall", "yes"),
       ("through the empty space between planets", "no"), ("through a vacuum (with no air at all)", "no"), ("through the string of a string telephone", "yes")]


def g_med():
    m, a = R.choice(MED)
    if not once(("me", m)):
        return None
    ans = "Yes, the vibrations can pass through it." if a == "yes" else "No, there are no particles to carry the vibrations."
    return item("Can sound travel %s?" % m, ans, ["No, there are no particles to carry the vibrations." if a == "yes" else "Yes, the vibrations can pass through it.", "Only if it is very loud.", "Only at night."],
                "Sound needs a solid, liquid or gas to travel through.")


def g_speed():
    k = R.choice(["dist", "echo", "time"])
    if k == "dist":
        t = R.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        if not once(("sd", t)):
            return None
        d = 340 * t
        g = "%s m" % format(d, ",")
        return item("Sound travels about 340 m every second in air. How far does it travel in %d seconds?" % t, g,
                    uniq(g, ["%s m" % format(340 + t, ","), "%s m" % format(34 * t, ","), "%s m" % format(d * 2, ","), "%d m" % t]), "340 × %d = %s m." % (t, format(d, ",")))
    if k == "time":
        d = R.choice([680, 1020, 1360, 1700, 2040, 2380, 2720, 3400])
        if not once(("st", d)):
            return None
        g = "%d seconds" % (d // 340)
        return item("Sound travels about 340 m every second. How long does a sound take to travel %s m?" % format(d, ","), g,
                    uniq(g, ["%d seconds" % (d // 34), "%d seconds" % (d // 340 + 2), "1 second", "%d seconds" % (d // 170)]), "%s ÷ 340 = %d seconds." % (format(d, ","), d // 340))
    t = R.choice([1, 2, 3, 4])
    if not once(("ec", t)):
        return None
    d = 340 * t // 2
    g = "%d m" % d
    who = P.next()[0]
    return item("%s shouts at a cliff and hears the echo %d second%s later. Sound travels about 340 m per second. How far away is the cliff?" % (who, t, "" if t == 1 else "s"), g,
                uniq(g, ["%s m" % format(340 * t, ","), "%d m" % (340 // t), "%d m" % (d + 100), "340 m"]), "The sound goes there and back: 340 × %d ÷ 2 = %d m." % (t, d))


def g_phone():
    who = P.next()[0]
    rows = [("tight string", 5), ("slack string", 1), ("tight string touching a door", 2), ("tight wire instead of string", 5)]
    k = R.choice(["best", "worst", "why", "touch"])
    if not once(("ph", k, who)) or not once(("pk", k), 3):
        return None
    tab = table(["String telephone", "How well the message could be heard (0 to 5)"], [[a, str(b)] for a, b in rows])
    intro = tab + "%s tested string telephones. " % who
    if k == "best":
        return item(intro + "Which made the message easiest to hear?", "a tight string or wire", ["a slack string", "a string touching a door", "none of them"], "Tight strings carry vibrations well.")
    if k == "worst":
        return item(intro + "Which made the message hardest to hear?", "the slack string", ["the tight string", "the tight wire", "they were all the same"], "A slack string cannot carry the vibrations well.")
    if k == "why":
        return item(intro + "How does a string telephone carry your voice?", "Your voice makes the cup and string vibrate, and the vibrations travel along the string.", ["Sound travels through the air in the string.", "The string lights up.", "The cups catch the words."],
                    "Sound travels through solids.")
    return item(intro + "Why was the message quieter when the string touched a door?", "Some of the vibrations passed into the door.", ["The door made the string tighter.", "Doors are loud.", "The string got longer."], "Vibrations can be lost.")


HEAR = [("humans", 20000), ("dogs", 45000), ("cats", 64000), ("bats", 110000), ("mice", 90000), ("elephants", 12000), ("dolphins", 150000)]


def g_hear():
    k = R.random() < 0.7
    rows = HEAR
    tab = table(["Animal", "Highest pitch it can hear (vibrations per second)"], [[a, format(b, ",")] for a, b in rows])
    if k:
        a, b = R.sample(rows, 2)
        hi = a if a[1] > b[1] else b
        if not once(("hr", tuple(sorted((a[0], b[0]))))):
            return None
        return item(tab + "Which can hear higher-pitched sounds: %s or %s?" % (a[0], b[0]), hi[0], [(b if hi is a else a)[0], "They hear exactly the same.", "Neither can hear sounds."],
                    "The bigger number means it can hear higher pitches.")
    a, b = R.choice(rows)
    if not once(("hd", a)):
        return None
    g = format(b, ",")
    return item(tab + "What is the highest pitch %s can hear, in vibrations per second?" % a, g, uniq(g, [format(x, ",") for _, x in rows]), "Read the row.")


WHERE = [("You hear a knock on your bedroom door.", "the wooden door, then the air"), ("You hear a friend call while you swim underwater.", "the air, then the water"),
         ("You hear music from the flat downstairs.", "the floor, then the air"), ("A doctor listens to your heart with a stethoscope.", "your body, then the air in the tube"),
         ("You hear a bird singing in the garden.", "the air"), ("You hear a friend through a string telephone.", "the string and the cups"),
         ("A whale hears another whale far away.", "the seawater"), ("You hear a train through the rails before you hear it in the air.", "the steel rails")]


def g_where():
    s_, m = R.choice(WHERE)
    if not once(("wh", s_)):
        return None
    return item("%s What does the sound travel through to reach the listener?" % s_, m, R.sample([x[1] for x in WHERE if x[1] != m], 3), "Sound travels through solids, liquids and gases.")


B1 = bank([
    ("How are all sounds made?", "by something vibrating", ["by light hitting an object", "by heat", "by magnets"], "Vibrate means move quickly back and forth."),
    ("What does sound need to travel through?", "a solid, liquid or gas", ["empty space", "nothing at all", "only light"], "Particles carry the vibrations."),
    ("Why can't astronauts talk to each other in space without radios?", "There is no air in space to carry sound.", ["Space is too cold.", "Helmets are too thick.", "Space is too bright."], "Radios use radio waves."),
    ("Which part of the ear vibrates when sound reaches it?", "the eardrum", ["the ear lobe", "the hair", "the skull"], "A thin skin inside the ear."),
    ("Which travels faster, sound or light?", "light", ["sound", "they are the same", "neither moves"], "That is why we see lightning first."),
    ("Why can you feel a speaker when music is playing?", "Its parts are vibrating.", ["It is hot.", "It is magnetic.", "It is wet."], "Feel the vibrations."),
    ("What is an echo?", "a sound that reflects off a surface and comes back", ["a very quiet sound", "a sound in space", "a high sound"], "Hard surfaces reflect sound."),
    ("Through which does sound travel fastest?", "solids", ["gases", "empty space", "air at night"], "Particles are closest together in solids."),
])
B5 = bank([
    ("How could you show that sound makes things vibrate?", "Put rice on a drum and bang it nearby: the rice jumps.", ["Shine a torch on the drum.", "Weigh the drum.", "Paint the drum."], "Make vibrations visible."),
    ("Why do whales hear each other over long distances in the sea?", "Sound travels well through water.", ["Water blocks sound.", "Whales use light.", "Sound only travels in air."], "Liquids carry sound."),
    ("Why do you hear a train coming by putting your ear near the rails? (Never do this!)", "Sound travels faster and further through the steel rails than through air.", ["Rails make the sound.", "Air is faster than steel.", "Trains are silent."], "Solids carry sound well."),
    ("Why do concert halls have soft seats and curtains?", "Soft materials absorb sound and reduce echoes.", ["To make echoes louder.", "To reflect sound more.", "To make it warmer only."], "Absorbing sound."),
    ("How could you test which material is best at muffling sound?", "Wrap the same sound source in each material and measure the sound level from the same distance.", ["Use different sounds each time.", "Stand at different distances.", "Ask friends which they like."], "Fair test."),
])


def body():
    think = ("<p><b>Sounds are made when something vibrates.</b></p>"
             "<ul><li>The vibrations travel through a solid, liquid or gas to our ears. Sound cannot travel through empty space.</li>"
             "<li>In the ear, the eardrum vibrates, tiny bones pass the vibrations on, and nerves send messages to the brain.</li>"
             "<li>Sound travels about 340 m per second in air: much slower than light. An echo is sound reflected back.</li></ul>")
    ex = [("What vibrates in a recorder?", ["The player blows air into the tube"], "the air inside"),
          ("Echo after 2 seconds. Cliff distance?", ["340 × 2 = 680 m there and back", "680 ÷ 2"], "340 m")]
    mist = ["Thinking sound can travel through empty space.", "Thinking sound is faster than light.", "Thinking a slack string telephone works best."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Vibrations", B1 + [(g_vib, 10), (g_med, 2)]),
        ("How we hear", [(g_ear, 8), (g_med, 5), (g_where, 5), (g_hear, 2)]),
        ("Sound travels", [(g_speed, 14), (g_phone, 4), (g_hear, 2)]),
        ("Hearing and string telephones", [(g_hear, 8), (g_phone, 6), (g_where, 2), (g_speed, 4)]),
        ("Investigating sound", B5 + [(g_hear, 11), (g_phone, 2), (g_speed, 1), (g_where, 1)]),
    ])
    make_uk(4, "how-sounds-are-made", 10, "Sound",
            "Identify how sounds are made, associating some of them with something vibrating. Recognise that vibrations from sounds travel through a medium to the ear.",
            "How Sounds Are Made",
            "Year 4 Science: How Sounds Are Made Worksheets (Vibrations and Hearing)",
            "How Sounds Are Made",
            "Free Year 4 science worksheets on how sounds are made: vibrations, how sound travels through solids, liquids and gases, the ear, the speed of sound, echoes and string telephones. 100 questions with answers.",
            "Every sound starts with a vibration.",
            "Vibrations travel through solids, liquids and gases to our ears.",
            body(),
            [("How are sounds made?", "Every sound is made by something vibrating, such as a guitar string, a drum skin, the air in a recorder or your vocal cords."),
             ("How does sound reach our ears?", "The vibrations pass through a medium, such as air, water or a solid, into the ear, where the eardrum vibrates and the brain hears the sound."),
             ("Can sound travel through space?", "No. Space is almost empty, so there are no particles to carry the vibrations.")],
            sets)


if __name__ == "__main__":
    main()
