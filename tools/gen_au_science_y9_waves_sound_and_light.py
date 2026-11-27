# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, AC9S9U04: wave and particle models of energy transfer - transverse and longitudinal
waves, wave speed = frequency × wavelength, sound travelling through solids, liquids and gases, and light reflecting, refracting,
being absorbed and transmitted.
  python tools/gen_au_science_y9_waves_sound_and_light.py
Reuses the UK Year 7 sound and light makers, the UK Year 9 waves makers and the US Grade 8 wave and light and sound makers with
Australian names, plus own particle-model questions and Australian contexts (whale song, the Parkes telescope, ultrasound).
Wrong answers come from real mistakes: thinking sound travels through a vacuum, thinking the wave carries the medium along with
it, and thinking light travels slower than sound.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 9, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

W9 = "gen_uk_science_y9_waves"
SO = "gen_uk_science_y7_sound"
LI = "gen_uk_science_y7_light"
WP = "gen_us_science_g8_wave_properties"
LS = "gen_us_science_g8_light_and_sound_waves"
w_echo = limit(src(W9, "g_echo"), 4)
w_hear = src(W9, "g_hear")
w_type = src(W9, "g_type", rep=[(r"\bIs ripples\b", "Are ripples"), (r"\bIs (sound|radio|micro|light|X|water) waves\b", r"Are \1 waves")])
w_speed = limit(src(W9, "g_wspeed"), 6)
w_b1 = src.B(W9, "B1")
w_b5 = src.B(W9, "B5")
s_med = src(SO, "g_med")
s_range = limit(src(SO, "g_range"), 5)
s_wave = src(SO, "g_wave")
s_echo = limit(src(SO, "g_echo"), 4)
s_b1 = src.B(SO, "B1")
l_obj = limit(src(LI, "g_obj"), 5)
l_refl = limit(src(LI, "g_refl"), 5)
l_refr = src(LI, "g_refr")
l_spec = limit(src(LI, "g_spec"), 4)
l_b1 = src.B(LI, "B1")
l_b5 = src.B(LI, "B5")
u_speed = limit(src(WP, "g_speed"), 5)
u_mat = limit(src(LS, "g_mat"), 5)
u_what = limit(src(LS, "g_what"), 5)

POOL1 = pool(R, [
    ("What does a wave transfer?", "energy, without moving the material along with it", ["the material from place to place", "only water", "mass"], "The particles vibrate about a fixed point."),
    ("In a transverse wave, how do the particles move?", "at right angles to the direction the wave travels", ["in the same direction the wave travels", "they do not move", "in circles only"], "Ripples on water and light are transverse."),
    ("In a longitudinal wave, how do the particles move?", "back and forth along the direction the wave travels", ["at right angles to the wave", "they stay still", "only up and down"], "Sound is longitudinal."),
    ("Why can sound not travel through space?", "Space is a vacuum with no particles to pass on the vibrations.", ["Space is too cold.", "Sound is too slow.", "Light blocks sound."], "Sound needs a medium."),
    ("Why does sound travel fastest in solids?", "Particles are packed closely, so vibrations pass on quickly.", ["Solids have no particles.", "Solids are lighter.", "Sound is a solid."], "Sound is about 340 m/s in air and over 5000 m/s in steel."),
    ("Light can travel through space. What does this show?", "Light does not need a medium.", ["Space has air.", "Light is a sound wave.", "Light is made of particles of air."], "Light is an electromagnetic wave."),
    ("Which travels faster: light or sound?", "light", ["sound", "they are the same", "it depends on the colour"], "This is why you see lightning before you hear thunder."),
    ("Humpback whales migrating along the Australian coast sing to each other. Why does their song travel a long way?", "Sound travels quickly and far in water.", ["Water blocks sound.", "Whales use light.", "Sound cannot travel in water."], "Water particles are closer than air particles."),
    ("What happens to light when it hits a mirror?", "It is reflected; the angle of incidence equals the angle of reflection.", ["It is absorbed completely.", "It bends into the mirror.", "It slows to zero."], "Smooth surfaces give clear reflections."),
    ("Why does a straw look bent in a glass of water?", "Light refracts (bends) as it passes from water to air.", ["The straw really bends.", "Water reflects all light.", "Light stops in water."], "Light changes speed between materials."),
    ("A black shirt feels hotter in the sun than a white shirt. Why?", "Black absorbs more light energy; white reflects more.", ["White absorbs more light.", "Black reflects all light.", "Colour has no effect."], "Absorbed light is transferred to heat."),
    ("What is the frequency of a wave?", "the number of waves passing a point each second", ["the height of a wave", "the distance between two crests", "the speed of the wave"], "It is measured in hertz (Hz)."),
])
POOL5 = pool(R, [
    ("Mia stands 170 m from a wall and claps. She hears the echo 1 s later. What speed of sound does this give?", "340 m/s", ["170 m/s", "1 m/s", "680 m/s"], "The sound travels 340 m (there and back) in 1 s."),
    ("Jack shines a ray box into a glass block at different angles and measures how much it bends. What is the independent variable?", "the angle of incidence", ["the angle of refraction", "the type of glass", "the brightness of the room"], "He changes the incoming angle."),
    ("Ruby rings a bell inside a jar and pumps the air out. What happens to the sound?", "It gets quieter, because there are fewer particles to carry it.", ["It gets louder.", "It stays the same.", "It turns into light."], "Sound needs a medium."),
    ("Kai sees lightning, then counts 6 s before he hears the thunder. About how far away was the strike? (sound ≈ 340 m/s)", "about 2 km", ["about 6 m", "about 340 m", "about 20 km"], "340 × 6 ≈ 2040 m."),
    ("Ella makes a slinky wave by pushing and pulling one end. What kind of wave is this?", "longitudinal", ["transverse", "electromagnetic", "it is not a wave"], "The coils move back and forth along the slinky."),
    ("Noah tests which material blocks the most sound from a buzzer: foam, cardboard or bubble wrap. What should he keep the same?", "the buzzer, its distance from the sound meter and the thickness of each material", ["the type of material", "nothing", "the sound reading"], "Only the material should change."),
    ("A doctor uses ultrasound to see an unborn baby. Why is ultrasound used?", "High-frequency sound reflects from tissues and is safe.", ["It is a kind of X-ray.", "It is louder than speech.", "It uses light."], "Ultrasound is above human hearing (over 20 000 Hz)."),
    ("Zara measures how bright a torch looks through 1, 2, 3 and 4 sheets of tracing paper. What is she investigating?", "how much light is transmitted and absorbed", ["how sound travels", "how mirrors reflect", "how fast light is"], "Each sheet absorbs or scatters some light."),
])


def main():
    sets = U.sets([
        ("Wave models", [(POOL1, 6), (w_type, 6), (s_wave, 4), (w_b1, 4)]),
        ("Wave speed, frequency and wavelength", [(w_speed, 6), (u_speed, 5), (POOL1, 2), (w_echo, 4), (POOL5, 3)]),
        ("Sound through different mediums", [(s_med, 5), (s_range, 4), (w_hear, 4), (s_echo, 3), (s_b1, 3), (POOL1, 1)]),
        ("Light: reflection, refraction and absorption", [(l_refl, 5), (l_refr, 4), (l_obj, 4), (u_mat, 3), (l_spec, 2), (POOL1, 2)]),
        ("Investigations", [(POOL5, 5), (w_b5, 4), (l_b5, 4), (u_what, 4), (l_b1, 3)]),
    ])
    make_au(YEAR, "waves-sound-and-light", SORT, "AC9S9U04", "Physical sciences",
            "Use wave and particle models to describe energy transfer through different mediums and examine the usefulness of each "
            "model for explaining phenomena (summary of the Australian Curriculum v9.0 Science content description).",
            "Waves, Sound and Light", "Waves, sound and light",
            "Free Year 9 science worksheets on waves: transverse and longitudinal waves, wave speed, frequency and wavelength, sound in "
            "solids, liquids and gases, echoes, and reflection, refraction and absorption of light. 100 questions with answers.",
            "Waves move energy, not matter.", "Sound needs particles to pass on vibrations; light can travel through a vacuum.",
            "<p><b>A wave transfers energy without moving the material along with it.</b></p><ul>"
            "<li>Transverse waves (light, ripples) vibrate at right angles; longitudinal waves (sound) vibrate along the direction of travel.</li>"
            "<li>Wave speed = frequency × wavelength. Sound is faster in solids than in gases and cannot travel through a vacuum.</li>"
            "<li>Light can be reflected, refracted (bent), absorbed or transmitted, and travels through space.</li></ul>",
            [("Frequency 50 Hz, wavelength 2 m. Speed?", ["v = f × λ", "50 × 2"], "100 m/s"),
             ("Echo heard 2 s after a clap. Wall distance? (340 m/s)", ["340 × 2 = 680 m there and back", "680 ÷ 2"], "340 m")],
            ["Thinking sound can travel through a vacuum.", "Thinking the wave carries the water or air along with it.",
             "Forgetting to halve the distance in echo questions."],
            [("What is the difference between transverse and longitudinal waves?", "In a transverse wave the vibrations are at right angles to the direction of travel. In a longitudinal wave they are along the direction of travel, making compressions and rarefactions."),
             ("Why do we use both a wave model and a particle model?", "The particle model explains why sound needs a medium and travels faster in solids. The wave model explains frequency, wavelength, reflection and refraction."),
             ("How is wave speed calculated?", "Wave speed (m/s) = frequency (Hz) × wavelength (m).")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
