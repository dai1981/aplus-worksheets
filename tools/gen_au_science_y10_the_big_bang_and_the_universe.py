# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, AC9S10U03: the big bang theory of the origin and evolution of the universe, the
evidence for it (red shift, the expansion of the universe, the cosmic microwave background), galaxies, and the life cycle of
stars and the origin of the elements.
  python tools/gen_au_science_y10_the_big_bang_and_the_universe.py
Reuses the US Earth and Space Science big bang and stars makers with Australian names, plus own questions on Australian
astronomy (Parkes, ASKAP, the Square Kilometre Array, the Emu in the Sky).
Wrong answers come from real mistakes: thinking the big bang was an explosion in space, thinking red shift means a star is red,
and thinking all elements were made in the big bang.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 10, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

BB = "gen_us_science_ess_the_big_bang"
ST = "gen_us_science_ess_stars_and_the_origin_of_elements"
b_data = limit(src(BB, "g_data"), 6)
b_ev = src(BB, "g_ev")
b_hub = limit(src(BB, "g_hubble"), 6)
b_shift = limit(src(BB, "g_shift"), 6)
b_b1 = src.B(BB, "B1")
b_b5 = src.B(BB, "B5")
s_fuse = src(ST, "g_fuse")
s_spec = limit(src(ST, "g_spec"), 5)
s_stage = src(ST, "g_stage")
s_where = src(ST, "g_where")
s_b1 = src.B(ST, "B1")
s_b5 = src.B(ST, "B5")

POOL1 = pool(R, [
    ("What does the big bang theory say?", "The universe began about 13.8 billion years ago from a very hot, dense state and has been expanding ever since.", ["The universe has always been the same size.", "A star exploded in empty space.", "The Earth is the centre of the universe."], "Space itself is expanding."),
    ("What is red shift?", "the stretching of light from distant galaxies to longer (redder) wavelengths as they move away", ["galaxies being red in colour", "light turning into heat", "stars cooling down"], "Bigger red shift means faster moving away."),
    ("What did Edwin Hubble discover in 1929?", "More distant galaxies are moving away faster, so the universe is expanding.", ["The Sun is a star.", "Galaxies are not moving.", "Light has no speed."], "This is Hubble's law."),
    ("What is the cosmic microwave background (CMB) radiation?", "faint microwave radiation from all directions, left over from the early universe", ["radiation from microwave ovens", "light from the Sun", "radio signals from phones"], "It was found by accident in 1965."),
    ("Which elements were mainly made in the big bang?", "hydrogen and helium", ["iron and gold", "carbon and oxygen", "uranium"], "Heavier elements were made later in stars."),
    ("Where were elements heavier than iron, such as gold, made?", "in supernova explosions and neutron star collisions", ["in the big bang", "in the Earth's core", "in the Sun today"], "We are made of 'star stuff'."),
    ("What powers a star like the Sun?", "nuclear fusion of hydrogen into helium", ["burning coal", "chemical reactions with oxygen", "nuclear fission of uranium"], "Fusion releases huge amounts of energy."),
    ("What will the Sun become at the end of its life?", "a red giant, then a white dwarf", ["a black hole", "a supernova", "a planet"], "It is not massive enough to make a black hole."),
    ("What is a galaxy?", "a huge system of billions of stars, gas and dust held together by gravity", ["a single star", "a planet and its moons", "the solar system"], "We live in the Milky Way galaxy."),
    ("The 'Emu in the Sky' is seen in the Milky Way by many First Nations peoples. What is it made of?", "dark dust clouds in the Milky Way", ["a group of bright planets", "the Moon's craters", "light from a city"], "Its position helps tell the season for emu eggs."),
    ("Why do radio telescopes such as ASKAP in Western Australia study the early universe?", "Radio waves from distant hydrogen gas reveal the universe's history.", ["Radio waves come only from the Sun.", "They make the universe expand.", "They see through planets."], "The Square Kilometre Array is being built in WA and South Africa."),
    ("If the universe is expanding, what does that suggest about the past?", "Everything was once much closer together.", ["The universe was bigger in the past.", "The universe has no past.", "Galaxies were further apart."], "Running the expansion backwards leads to the big bang."),
])
POOL5 = pool(R, [
    ("Mia draws dots on a balloon and blows it up. All the dots move apart. What does this model?", "the expansion of space carrying galaxies apart", ["a star exploding", "the Earth orbiting the Sun", "a galaxy spinning"], "No dot is at the centre."),
    ("What is one limitation of Mia's balloon model?", "Real galaxies are not on a surface, and they do not grow as space expands.", ["It shows galaxies moving apart.", "It is perfectly accurate.", "Balloons are round."], "All models have limitations."),
    ("Jack plots galaxy distance against speed moving away. The points form a straight line through the origin. What does this show?", "speed is proportional to distance (Hubble's law)", ["galaxies are not moving", "closer galaxies move faster", "there is no pattern"], "The slope is the Hubble constant."),
    ("Ruby compares absorption lines in light from a galaxy with lines from a lab. The galaxy's lines are shifted towards red. What does this mean?", "The galaxy is moving away from us.", ["It is moving towards us.", "It is not moving.", "It is very hot."], "A blue shift would mean moving towards us."),
    ("The Parkes radio telescope in New South Wales detected the first 'fast radio burst' in 2007. Why are these studied?", "They help measure matter spread between galaxies.", ["They are signals from aliens.", "They come from mobile phones only.", "They show the Earth is flat."], "Scientific discoveries lead to new questions."),
    ("Kai says, 'The big bang was an explosion at one point in space.' What is a better description?", "It was an expansion of space itself, everywhere at once.", ["It was a bomb in space.", "It happened at the centre of the Milky Way.", "It happened on Earth."], "There is no centre of the expansion."),
    ("Ella uses spectroscopes to look at light from a sodium lamp and the Sun. She sees matching lines. What can she conclude?", "The Sun contains sodium.", ["The Sun is made only of sodium.", "Lamps are stars.", "Spectra cannot identify elements."], "Each element has its own spectral fingerprint."),
    ("Why did scientists accept the big bang theory over the steady state theory?", "The cosmic microwave background and red shift data supported it.", ["It was simpler to say.", "A famous scientist liked it.", "Steady state was never tested."], "Theories change when new evidence is found."),
])


def main():
    sets = U.sets([
        ("The big bang theory", [(POOL1, 6), (b_ev, 6), (b_b1, 5), (POOL5, 3)]),
        ("Red shift and the expanding universe", [(b_shift, 6), (b_hub, 6), (b_data, 4), (POOL1, 2), (POOL5, 2)]),
        ("Stars and galaxies", [(s_stage, 6), (s_fuse, 5), (s_b1, 4), (POOL1, 3), (s_spec, 2)]),
        ("The origin of the elements", [(s_where, 6), (s_spec, 3), (s_fuse, 3), (POOL1, 3), (b_ev, 2), (s_b1, 3)]),
        ("Investigations", [(POOL5, 4), (b_b5, 4), (s_b5, 4), (b_data, 2), (b_hub, 2), (b_shift, 2), (s_stage, 2)]),
    ])
    make_au(YEAR, "the-big-bang-and-the-universe", SORT, "AC9S10U03", "Earth and space sciences",
            "Describe how the big bang theory models the origin and evolution of the universe and analyse the supporting evidence "
            "for the theory (summary of the Australian Curriculum v9.0 Science content description).",
            "The Big Bang and the Universe", "The big bang",
            "Free Year 10 science worksheets on the big bang and the universe: the big bang theory, red shift, Hubble's law, the "
            "cosmic microwave background, galaxies, the life cycle of stars and the origin of the elements. 100 questions with answers.",
            "The universe is expanding.", "Red shift and the cosmic microwave background are key evidence for the big bang.",
            "<p><b>The universe began about 13.8 billion years ago and is still expanding.</b></p><ul>"
            "<li>Red shift: light from distant galaxies is stretched to longer wavelengths, so they are moving away. Further galaxies move faster (Hubble's law).</li>"
            "<li>The cosmic microwave background is leftover radiation from the hot early universe.</li>"
            "<li>The big bang made hydrogen and helium; stars made heavier elements by fusion and in supernovas.</li></ul>",
            [("A galaxy's spectral lines shift towards red. Meaning?", ["longer wavelengths"], "moving away"),
             ("Where was the iron in your blood made?", ["fusion in a massive star"], "inside a star")],
            ["Thinking the big bang was an explosion at one point in space.", "Thinking red shift means a star looks red.",
             "Thinking all elements were made in the big bang."],
            [("What evidence supports the big bang theory?", "Red shift of distant galaxies (the universe is expanding), the cosmic microwave background radiation, and the large amounts of hydrogen and helium in the universe."),
             ("What is the life cycle of a star like the Sun?", "A cloud of gas and dust forms a main-sequence star, which becomes a red giant and finally a white dwarf. Massive stars explode as supernovas and leave neutron stars or black holes."),
             ("How does Australia contribute to astronomy?", "Australia has radio telescopes such as Parkes and ASKAP and is helping build the Square Kilometre Array. First Nations peoples have one of the world's oldest astronomical traditions.")],
            sets)


if __name__ == "__main__":
    main()
