# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 2, AC9S2U02: sound - ways to make sounds, loud and soft, high and low, vibrations, and how
sound travels to our ears.
  python tools/gen_au_science_y2_sound.py
Reuses the US Grade 1 sound and vibrations makers and the UK Year 4 how sounds are made makers with Australian names, plus own
questions on musical instruments (didgeridoo, clapsticks). Short sentences.
Wrong answers come from real mistakes: thinking sound comes from nowhere, and mixing up loud with high.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 2, 2
U, R, P, src = AU(seed_of(YEAR, SORT))

S1 = "gen_us_science_g1_sound_and_vibrations"
S4 = "gen_uk_science_y4_how_sounds_are_made"
NO = ["m/s", "speed of sound", "pitch", "frequency", "decibel"]
a_what = src(S1, "g_what", drop=NO)
a_which = src(S1, "g_which", drop=NO)
a_pic = src(S1, "g_pic", drop=NO)
a_loud = src(S1, "g_loud", drop=NO)
a_stop = src(S1, "g_stop", drop=NO)
a_feel = src(S1, "g_feel", drop=NO)
a_evid = src(S1, "g_evid", drop=NO)
a_b1 = src.B(S1, "B1", drop=NO)
a_b3 = src.B(S1, "B3", drop=NO)
a_b5 = src.B(S1, "B5", drop=NO)
b_vib = src(S4, "g_vib", drop=NO)
b_hear = limit(src(S4, "g_hear", drop=NO), 5)
b_where = src(S4, "g_where", drop=NO)

ACT = [("a drum", "hitting it"), ("a guitar", "plucking its strings"), ("a recorder", "blowing into it"), ("a shaker", "shaking it"),
       ("clapsticks", "tapping them together"), ("a didgeridoo", "blowing and buzzing your lips into it"), ("a triangle", "tapping it with a beater"),
       ("a violin", "rubbing a bow across its strings"), ("a whistle", "blowing into it"), ("a bell", "shaking or hitting it")]


def g_act():
    o, a = R.choice(ACT)
    if not once(("ac", o)):
        return None
    return tq("How do you make a sound with %s?" % o, a, R.sample([x[1] for x in ACT if x[1] != a], 3), "Different actions make different sounds.")


LH = [("a whisper", "soft"), ("a lawnmower", "loud"), ("a ticking clock", "soft"), ("a thunderclap", "loud"), ("a cat purring", "soft"),
      ("a fire alarm", "loud"), ("leaves rustling", "soft"), ("a school bell", "loud")]


def g_lh():
    o, a = R.choice(LH)
    if not once(("lh", o)):
        return None
    return tq("Is %s a loud sound or a soft sound?" % o, a, ["loud" if a == "soft" else "soft", "no sound", "a light"], "Loud sounds have big vibrations.")


POOL1 = pool(R, [
    ("What makes sound?", "something vibrating (moving back and forth quickly)", ["something staying still", "light", "colours"], "Touch your throat when you hum."),
    ("How does sound get to your ears?", "the vibrations travel through the air", ["it jumps", "it is carried by light", "it does not travel"], "Air carries the sound."),
    ("How can you make a drum sound louder?", "hit it harder", ["hit it more softly", "paint it", "stop hitting it"], "A harder hit makes bigger vibrations."),
    ("How can you make a sound quieter?", "move further away or cover your ears", ["move closer", "shout", "turn it up"], "Sound gets quieter far away."),
    ("Which body part do we hear with?", "our ears", ["our eyes", "our nose", "our toes"], "Ears collect sound."),
    ("What happens to a ruler you twang on a desk?", "it vibrates and makes a sound", ["it melts", "it turns blue", "it makes light"], "Vibrations make sound."),
    ("How do you stop a ringing bell?", "hold it so it stops vibrating", ["shout at it", "shine a torch on it", "blow on it"], "No vibration, no sound."),
    ("A didgeridoo is a First Nations instrument. How does it make sound?", "the player's lips buzz and the air inside vibrates", ["it is hit with a stick", "it is plucked", "it uses electricity"], "It makes a deep droning sound."),
    ("Why do people wear earmuffs near loud machines?", "to protect their ears from loud sounds", ["to keep warm only", "to hear better", "to look nice"], "Very loud sounds can hurt hearing."),
    ("Can sound travel through water?", "yes", ["no", "only at night", "only in the bath"], "Whales call to each other in the ocean."),
])
POOL5 = pool(R, [
    ("Mia puts rice on a drum and taps it. What happens to the rice?", "it jumps", ["it melts", "it disappears", "nothing"], "The drum skin vibrates."),
    ("Jack makes a string telephone with two cups. Why does it work?", "the string carries the vibrations", ["the cups glow", "the string is magic", "it uses batteries"], "Keep the string tight."),
    ("Ruby walks away from a radio. What happens to the sound?", "it gets quieter", ["it gets louder", "it stays the same", "it turns into light"], "Sound gets quieter further away."),
    ("Kai fills glass bottles with different amounts of water and taps them. What does he find?", "they make different sounds", ["they all sound the same", "they make no sound", "they break"], "Different amounts of water change the sound."),
    ("Ella stretches rubber bands over a box and plucks them. What does she see?", "the bands vibrate", ["the bands melt", "the box flies", "nothing happens"], "Vibrations make the sound."),
    ("Noah tests which material blocks sound best: foam, paper or a towel. What should he keep the same?", "the same sound and the same distance", ["the material", "nothing", "the room only"], "Change only the material."),
])


def main():
    sets = U.sets([
        ("Making sounds", [(g_act, 8), (POOL1, 4), (a_what, 4), (a_b1, 4)]),
        ("Vibrations", [(a_feel, 5), (b_vib, 5), (a_evid, 4), (POOL1, 3), (a_b3, 3)]),
        ("Loud and soft", [(g_lh, 7), (a_loud, 5), (a_which, 4), (POOL1, 2), (a_stop, 2)]),
        ("How sound travels", [(b_hear, 4), (b_where, 5), (a_pic, 5), (POOL1, 3), (a_stop, 3)]),
        ("Let's test it", [(POOL5, 6), (a_b5, 4), (a_which, 4), (a_pic, 3), (a_stop, 1), (g_act, 2)]),
    ])
    pic = K.row(["drum", "bell", "bird", "wind"], words=["hit", "ring", "sing", "blow"], size=80, label="a drum, a bell, a singing bird and wind")
    make_au(YEAR, "sound", SORT, "AC9S2U02", "Physical sciences",
            "Explore different actions to make sounds and how to make a variety of sounds, and recognise that sound energy causes "
            "objects to vibrate (summary of the Australian Curriculum v9.0 Science content description).",
            "Sound", "Sound",
            "Free Year 2 science worksheets on sound: making sounds with instruments, vibrations, loud and soft sounds, and how sound "
            "travels to our ears. 100 questions with answers.",
            "Sound is made by vibrations.", "Hitting, plucking, blowing and shaking make things vibrate. Bigger vibrations are louder.",
            ("Sounds are made when things vibrate.", ["Hit a drum, pluck a string, blow a whistle.", "Bigger vibrations make louder sounds.",
                                                      "Sound travels through the air to our ears."]),
            [("How does a guitar make a sound?", ["pluck the strings", "they vibrate"], "vibrating strings")],
            ["Thinking sounds come from nowhere (something always vibrates).", "Mixing up loud sounds with high sounds."],
            [("What is a vibration?", "A vibration is a very fast back-and-forth movement. You can feel it if you touch your throat when you hum."),
             ("Why do sounds get quieter far away?", "The vibrations spread out as they travel, so less reaches your ears."),
             ("How can children explore sound at home?", "Make a shaker with rice, a string telephone with cups, or tap bottles with different amounts of water.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
