# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U03: how light forms shadows, is reflected and is refracted.
  python tools/gen_au_science_y5_shadows_reflection_and_refraction.py
Southern-hemisphere shadows (at midday the Sun is in the north, so shadows point south), mirrors and periscopes,
and refraction (a straw looks bent in water, pools look shallower, magnifying glasses, rainbows).
Reuses the UK Year 3 and Year 6 shadow and reflection makers with Australian names.
Wrong answers come from real mistakes: thinking a shadow is the object's reflection, that shadows are longest at midday,
and mixing up reflection (bouncing off) with refraction (bending as light passes into another material).
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 5, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

SR = "gen_uk_science_y6_shadows_and_reflection"
uk_shape = src(SR, "g_shape")
uk_shd = limit(src(SR, "g_shd"), 5)
uk_mirror = limit(src(SR, "g_mirror"), 3)
uk_peri = src(SR, "g_peri")
uk_b1 = src.B(SR, "B1")
uk_b5 = src.B(SR, "B5")
uk_side = src("gen_uk_science_y3_shadows", "g_side")
uk_size = src("gen_uk_science_y3_shadows", "g_size")
uk_refl = limit(src("gen_uk_science_y3_light_and_dark", "g_refl"), 9)

SUN = [("9 am", "long", "towards the west", "the Sun is low in the east"),
       ("7 am", "very long", "towards the west", "the Sun has just risen in the east"),
       ("12 noon", "shortest", "towards the south", "the Sun is high in the northern sky"),
       ("3 pm", "long", "towards the east", "the Sun is lower in the west"),
       ("5 pm", "very long", "towards the east", "the Sun is about to set in the west")]


def g_sun():
    t, ln, d, why = R.choice(SUN)
    k = R.choice(["dir", "len"])
    if k == "dir":
        w = [x for x in ["towards the west", "towards the south", "towards the east", "towards the north"] if x != d]
        return tq("In Sydney, a flagpole's shadow is measured at %s. Which way does the shadow point?" % t, d, w,
                  "At %s %s, so the shadow points the opposite way, %s." % (t, why, d))
    if ln == "shortest":
        return tq("In Sydney, when is a flagpole's shadow shortest on a sunny day?", "around 12 noon", ["at 7 am", "at 5 pm", "at sunset"],
                  "At midday the Sun is highest in the sky, so shadows are shortest. They point south.")
    w = [x for x in ["very long", "long", "shortest", "the same length all day"] if x != ln]
    return tq("In Sydney, how long is a flagpole's shadow at %s compared with the rest of the day?" % t, ln, w, "At %s %s." % (t, why))


RR = [("A straw in a glass of water looks bent where it enters the water.", "refraction"),
      ("A swimming pool looks shallower than it really is.", "refraction"),
      ("A magnifying glass makes an ant look bigger.", "refraction"),
      ("White light passes through raindrops and makes a rainbow.", "refraction"),
      ("Your legs look shorter when you stand in a clear pool.", "refraction"),
      ("Glasses (spectacles) help people see clearly.", "refraction"),
      ("You see your face in a still lake.", "reflection"),
      ("A bike reflector shines when car headlights hit it.", "reflection"),
      ("You see a car behind you in the rear-view mirror.", "reflection"),
      ("A periscope lets you see over a wall.", "reflection"),
      ("The Moon shines in the night sky.", "reflection"),
      ("Road signs glow brightly at night in headlights.", "reflection"),
      ("A black car gets hot in the sun.", "absorption"),
      ("Dark clothes feel warmer on a sunny day.", "absorption"),
      ("A tree blocks sunlight and leaves a dark patch on the ground.", "a shadow"),
      ("Your hand blocks a torch and a dark shape appears on the wall.", "a shadow")]


def g_rr():
    s, k = R.choice(RR)
    w = [x for x in ["refraction", "reflection", "absorption", "a shadow"] if x != k]
    e = {"refraction": "Refraction: light bends as it passes from one material (such as water or glass) into another.",
         "reflection": "Reflection: light bounces off a surface.",
         "absorption": "Absorption: the material takes in the light, and it warms up.",
         "a shadow": "A shadow forms where an opaque object blocks light."}[k]
    return tq("%s Which word best explains this?" % s, k, w, e)


POOLS = pool(R, [
    ("How is a shadow made?", "An opaque object blocks light, leaving a dark area behind it.", ["The object reflects its colour onto the ground.", "Light bends around the object.", "The object gives off darkness."], "Light travels in straight lines, so it cannot reach behind the object."),
    ("Why is a shadow the same shape as the object's outline?", "Light travels in straight lines past the edges of the object.", ["The shadow is a reflection of the object.", "Shadows copy colours.", "Light curves around the object."], "Shadows show the outline, not the colours or details."),
    ("What colour is the shadow of a red ball?", "dark (grey or black), not red", ["red", "pink", "white"], "A shadow is where light is missing, so it has no colour of its own."),
    ("What happens to a shadow when the object moves closer to the torch?", "The shadow gets bigger.", ["The shadow gets smaller.", "The shadow disappears.", "The shadow changes colour."], "The object blocks more of the light."),
    ("Which material makes the darkest shadow?", "a sheet of plywood", ["clear plastic", "tissue paper", "frosted glass"], "Opaque materials block all light."),
    ("Why does a translucent material make a pale shadow?", "It lets some light through.", ["It lets all light through.", "It blocks all light.", "It makes its own light."], "Only some light is blocked."),
])
POOLR = pool(R, [
    ("What happens when light hits a mirror?", "It reflects (bounces off) in a new direction.", ["It is all absorbed.", "It passes straight through.", "It turns into heat only."], "Smooth, shiny surfaces reflect light well."),
    ("Why do we see our reflection in a mirror but not in a brick wall?", "A mirror is smooth and shiny, so the reflected light stays in order.", ["Brick walls absorb all light.", "Mirrors make their own light.", "Brick walls are transparent."], "Rough surfaces scatter light in all directions."),
    ("Why do lifesavers wear bright, reflective vests?", "They reflect lots of light, so people can see them easily.", ["They make their own light.", "They absorb heat from the sun.", "They are transparent."], "Bright colours reflect more light."),
    ("Which surface reflects the least light?", "black felt", ["a mirror", "white paper", "aluminium foil"], "Dark, rough surfaces absorb most light."),
])
POOLF = pool(R, [
    ("What is refraction?", "light bending as it passes from one material into another", ["light bouncing off a mirror", "light being blocked", "light being made"], "Light changes speed when it moves into water or glass, so it bends."),
    ("Why does a pencil look broken when half of it is in a glass of water?", "Light from the pencil bends as it leaves the water.", ["The water really bends the pencil.", "The pencil reflects in the glass.", "The water absorbs the pencil's colour."], "This is refraction."),
    ("Why does a pool look shallower than it is?", "Light from the bottom bends as it leaves the water.", ["The water is thicker at the bottom.", "Light reflects off the bottom twice.", "Pools are always shallow."], "Take care: the water is deeper than it looks."),
    ("How does a magnifying glass work?", "Its curved glass bends (refracts) light so things look bigger.", ["It reflects light like a mirror.", "It makes its own light.", "It blocks light."], "A lens refracts light."),
    ("Which of these causes a rainbow?", "sunlight refracting through raindrops", ["clouds reflecting the Moon", "rain blocking the Sun", "lightning"], "Refraction splits white light into colours."),
    ("Where must the Sun be for you to see a rainbow?", "behind you, with rain in front of you", ["in front of you", "directly overhead", "below the horizon"], "Sunlight goes past you into the raindrops."),
    ("Which colours make up white light?", "red, orange, yellow, green, blue, indigo and violet", ["only red and blue", "only white", "black and white"], "A prism splits white light into these colours."),
    ("What does a glass prism do to a beam of white light?", "It bends it and splits it into colours.", ["It turns it black.", "It makes it brighter.", "It stops it completely."], "This is refraction."),
    ("Light goes from air into water. What happens?", "It slows down and bends.", ["It speeds up and stops.", "It turns into sound.", "It goes round in a circle."], "Light travels more slowly in water."),
    ("Why do people who spearfish aim below where the fish seems to be?", "Refraction makes the fish look higher than it really is.", ["Fish always swim downwards.", "Reflection makes fish look lower.", "Water makes spears float."], "Light bends at the water's surface."),
    ("Which is an example of refraction, not reflection?", "a spoon looking bent in a glass of water", ["seeing yourself in a window at night", "a mirror in a bathroom", "a shiny spoon showing your face"], "Bending is refraction; bouncing is reflection."),
    ("Which part of the eye refracts light to make a clear image?", "the lens", ["the eyelash", "the eyebrow", "the eyelid"], "The lens bends light onto the back of the eye."),
    ("A coin at the bottom of a cup cannot be seen. Water is poured in and the coin appears. Why?", "Light from the coin bends at the water surface towards your eye.", ["The water lifts the coin.", "The water reflects the coin.", "The coin makes light underwater."], "This is a classic refraction test."),
    ("What tool splits sunlight into a spectrum of colours?", "a prism", ["a mirror", "a torch", "a sheet of cardboard"], "Prisms refract light."),
])
POOL5 = pool(R, [
    ("Mia measures a 1 m stick's shadow every hour. At 9 am it is 2.5 m, at 12 noon 0.4 m and at 3 pm 2.2 m. What pattern does she see?", "The shadow is shortest around midday.", ["The shadow gets longer all day.", "The shadow stays the same.", "The shadow is longest at midday."], "The Sun is highest at midday."),
    ("Jack shines a torch on a toy. At 10 cm the shadow is 30 cm tall, at 20 cm it is 18 cm, at 30 cm it is 12 cm. What can he conclude?", "The further the toy is from the torch, the smaller the shadow.", ["The closer the toy is, the smaller the shadow.", "Distance does not change the shadow.", "The shadow grows with distance."], "Use the data to find the pattern."),
    ("In Jack's test, what should he keep the same?", "the torch, the toy and the screen position", ["the distance from the torch", "the shadow height", "nothing"], "Only the distance should change."),
    ("Ruby puts a coin in a bowl and steps back until she cannot see it. Ella pours in water slowly. What will Ruby see?", "The coin appears.", ["The coin disappears forever.", "Two coins.", "The coin turns blue."], "Refraction bends light from the coin into her eyes."),
    ("Kai wants to find which surface reflects the most light. Which is the fairest test?", "the same torch at the same distance and angle on each surface, with a light meter", ["a different torch for each surface", "different angles for each surface", "testing in daylight and at night"], "Keep everything the same except the surface."),
    ("Why do some cars have a rear-view mirror that is curved outwards?", "It reflects light from a wider area, so the driver sees more.", ["It refracts light like a lens.", "It absorbs glare.", "It makes cars look bigger."], "Curved mirrors spread out the view."),
])


def main():
    sets = U.sets([
        ("Shadows", [(uk_shape, 7), (uk_side, 4), (uk_size, 3), (POOLS, 4), (uk_b1, 2)]),
        ("Shadows and the Sun", [(g_sun, 8), (uk_shd, 3), (uk_size, 2), (POOLS, 2), (uk_b1, 5)]),
        ("Reflection", [(uk_refl, 7), (uk_mirror, 3), (uk_peri, 6), (POOLR, 4)]),
        ("Refraction", [(POOLF, 13), (g_rr, 7)]),
        ("Investigations", [(POOL5, 6), (uk_b5, 4), (uk_shd, 2), (g_rr, 5), (uk_side, 1), (uk_refl, 2)]),
    ])
    make_au(YEAR, "shadows-reflection-and-refraction", SORT, "AC9S5U03", "Physical sciences",
            "Describe how light travels from a source and how it interacts with objects and materials to form shadows and images, "
            "including reflection and refraction (summary of the Australian Curriculum v9.0 Science content description).",
            "Shadows, Reflection and Refraction", "Shadows, reflection and refraction",
            "Free Year 5 science worksheets on shadows, reflection and refraction: shadows in the Australian sun, mirrors and periscopes, "
            "bent straws, magnifying glasses and rainbows. 100 questions with answers.",
            "Light is blocked, bounced or bent.", "Shadows form when light is blocked; reflection bounces light; refraction bends it.",
            "<p><b>When light meets an object, it can be blocked, reflected or refracted.</b></p><ul>"
            "<li>A shadow forms where an opaque object blocks light. In southern Australia, the midday Sun is in the north, so shadows are short and point south.</li>"
            "<li>Reflection: light bounces off a surface. Smooth, shiny surfaces such as mirrors reflect light well.</li>"
            "<li>Refraction: light bends when it passes from air into water or glass. A straw looks bent; a pool looks shallower.</li></ul>",
            [("A flagpole at 9 am. Which way does its shadow point?", ["the Sun is in the east", "the shadow points away from the Sun"], "towards the west"),
             ("A straw looks bent in water. Why?", ["light passes from water into air", "it bends at the surface"], "refraction")],
            ["Thinking a shadow is a reflection of the object (it is where light is missing).",
             "Thinking shadows are longest at midday (they are shortest).", "Mixing up reflection (bouncing) and refraction (bending)."],
            [("Why do shadows in Sydney point south at midday?", "Sydney is in the southern hemisphere, south of the tropics, so the midday Sun is always in the northern part of the sky. Shadows point away from the Sun, towards the south."),
             ("What is the difference between reflection and refraction?", "Reflection is light bouncing off a surface, such as a mirror. Refraction is light bending as it passes from one material into another, such as from water into air."),
             ("How is a rainbow made?", "Sunlight shines into raindrops. The light is refracted (bent) and split into colours: red, orange, yellow, green, blue, indigo and violet.")],
            sets)


if __name__ == "__main__":
    main()
