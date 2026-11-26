# -*- coding: utf-8 -*-
"""
UK Year 3 science: Light and Dark (Light)
  python tools/gen_uk_science_y3_light_and_dark.py
We need light to see things; dark is the absence of light; light sources; light is reflected from surfaces, and
shiny, smooth surfaces reflect best; reflective clothing for safety; light from the Sun can be dangerous and there
are ways to protect our eyes.
Reuses the light-source questions of the Year 6 unit (new seed) and adds Year 3 questions.
Wrong answers come from real mistakes: "the Moon is a light source", "you can see a little in total darkness",
"shiny things give out light", "sunglasses make it safe to look at the Sun".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y6_how_light_travels as L6

L6.U = Unit(61310)
L6.R = L6.U.R
L6.P = People(L6.R)
uk_sci.USED.clear()
U, R, P = L6.U, L6.R, L6.P

SHINY = ["a mirror", "a shiny metal spoon", "a sheet of kitchen foil", "a polished silver tray", "a new coin", "a glossy white tile", "a bicycle reflector", "a still pond"]
DULL = ["a black woolly jumper", "a piece of dark brown cardboard", "a lump of black coal", "a grey felt hat", "a dark carpet", "a piece of black paper",
        "a muddy football", "a dark wooden log", "a black sock", "a navy blue towel"]


def g_refl():
    k = R.random() < 0.6
    if k:
        a = R.choice(SHINY)
        w = R.sample(DULL, 3)
        if not once(("rm", a), 2):
            return None
        o = sorted([a] + w)
        return item("Which of these reflects the most light: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Smooth, shiny and light-coloured surfaces reflect the most light.")
    a = R.choice(DULL)
    w = R.sample(SHINY, 3)
    if not once(("rl", a)):
        return None
    o = sorted([a] + w)
    return item("Which of these reflects the least light: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "Dark, dull and rough surfaces reflect very little light.")


OBJ = ["your hand", "a white sheet of paper", "a shiny mirror", "a red ball", "a cat", "your shoes", "a teddy bear", "a clock on the wall", "a glass of water",
       "a book", "a bright yellow raincoat", "a silver spoon", "a toy car", "your friend"]


def g_dark():
    o = R.choice(OBJ)
    if not once(("dk", o)):
        return None
    return item("In a room with no light at all, could you see %s?" % o, "No. With no light, no light can reflect from it into your eyes.",
                ["Yes, if you wait for your eyes to get used to it.", "Yes, if it is shiny or white.", "Yes, a little, because objects glow."],
                "We see objects when light reflects off them into our eyes. Dark is the absence of light.")


B1 = bank([
    ("What do we need to be able to see things?", "light", ["sound", "wind", "warmth only"], "No light, no seeing."),
    ("What is dark?", "the absence of light", ["a kind of black light", "a gas", "a shadow from the Moon"], "Dark is not a thing; it is no light."),
    ("What is a light source?", "something that gives out its own light", ["something that reflects light", "anything shiny", "anything white"], "The Sun, a torch, a candle."),
    ("Is the Moon a light source?", "No. It reflects light from the Sun.", ["Yes, it makes its own light.", "Yes, but only when full.", "Yes, at night only."], "Moonlight is reflected sunlight."),
    ("Why can we see a book, which is not a light source?", "Light reflects off the book into our eyes.", ["The book gives out light.", "Our eyes send out light to the book.", "Books glow."], "Reflection."),
    ("Is a mirror a light source?", "No. It reflects light very well.", ["Yes, it shines.", "Yes, at night.", "Only in the sun."], "Shiny is not the same as glowing."),
    ("What does reflect mean?", "bounce light back off a surface", ["soak up all light", "make new light", "turn light into sound"], "Like a ball bouncing."),
    ("Which surfaces reflect light best?", "smooth, shiny surfaces", ["rough, dull surfaces", "dark, furry surfaces", "all surfaces the same"], "Mirrors and foil."),
])
BR = bank([
    ("Why do cyclists wear reflective strips at night?", "Car headlights reflect off them, so drivers can see the cyclist.", ["The strips make their own light.", "They keep cyclists warm.", "They make the bike faster."], "Be seen, be safe."),
    ("Why do road signs reflect car headlights at night?", "so drivers can read them in the dark", ["to make the road warmer", "to light up the whole road", "to dazzle drivers"], "Reflective paint."),
    ("Why are school high-visibility jackets bright yellow or orange?", "Bright colours are easy to see, and the strips reflect light.", ["They are cheap colours.", "They glow without any light.", "They scare cars."], "Safety."),
    ("What are 'cat's eyes' on roads?", "small reflectors that show drivers where the lanes are", ["real cats' eyes", "lights powered by cats", "holes in the road"], "Invented in Britain."),
    ("Which would help you be seen walking on a dark road?", "a reflective armband", ["dark clothes", "a black hat", "a grey coat"], "Reflect the light."),
    ("Why can you see yourself in a still pond but not in a choppy one?", "A smooth surface reflects light evenly; a rough one scatters it.", ["Choppy water is a light source.", "Still water is darker.", "Fish block the light."], "Smooth reflects clearly."),
    ("Which would be best to make a sign that is easy to see at night?", "shiny reflective material", ["black velvet", "brown paper", "dark felt"], "Reflects headlights."),
    ("Why does kitchen foil look brighter when it is flat than when it is scrunched up?", "A flat, smooth surface reflects light back more evenly.", ["Scrunched foil makes light.", "Flat foil is a light source.", "There is no difference."], "Smooth surfaces."),
])
BS = bank([
    ("Why should you never look directly at the Sun?", "Its light is so strong it can damage your eyes.", ["It is too far away to see.", "It makes you sneeze.", "It is safe for a short time."], "Never, not even with sunglasses."),
    ("Is it safe to look at the Sun through sunglasses?", "No. Sunglasses do not protect your eyes enough.", ["Yes, always.", "Yes, if they are dark.", "Yes, for a few minutes."], "Never look at the Sun."),
    ("How can you protect your eyes on a sunny day?", "wear sunglasses and a hat with a brim", ["stare at the Sun to get used to it", "wear dark clothes only", "close one eye"], "Sun safety."),
    ("Is it safe to look at the Sun through binoculars or a telescope?", "No. They make the light even stronger and can blind you.", ["Yes, it is safer.", "Yes, if it is cloudy.", "Only for a moment."], "Never."),
    ("Which sign shows sunglasses protect your eyes from harmful sunlight?", "a UV protection mark (such as UV400 or CE)", ["the colour of the lenses only", "the price", "the brand name"], "Check the label."),
    ("When is the Sun's light strongest in the UK?", "around midday in summer", ["at midnight", "at sunrise in winter", "it is always the same"], "Take care at midday."),
    ("Why should you not look at bright sunlight reflected from water or snow?", "Reflected sunlight can also hurt your eyes.", ["It is too cold.", "Water makes light weaker.", "Snow makes its own light."], "Reflections can be strong too."),
    ("Besides eyes, what else does sunlight damage if we are not careful?", "our skin, causing sunburn", ["our hair colour only", "our teeth", "our bones straight away"], "Use sun cream."),
])
B5 = bank([
    ("A pupil says a cat can see in complete darkness. Is that right?", "No. Cats need a little light, though they see well in dim light.", ["Yes, cats need no light.", "Yes, cats' eyes make light.", "No, cats cannot see at all."], "All eyes need light."),
    ("Why is it easier to find a white sock than a black sock in a dim room?", "White reflects more light into our eyes.", ["Black socks give out light.", "White socks glow.", "Black reflects more light."], "Light colours reflect more."),
    ("How could you test which material is most reflective?", "Shine the same torch on each material in a dark room and see which is brightest.", ["Smell each material.", "Use a different torch for each.", "Test them in bright sunlight only."], "Fair test."),
    ("Why do we see the Moon brightly at night but not in a fully dark cave?", "The Moon reflects sunlight; no light reaches inside the cave.", ["The cave is a light source.", "The Moon makes light.", "Caves absorb the Moon."], "Need light to see."),
    ("Why do eye doctors say children should play outside but wear a hat in strong sun?", "Daylight is good for eyes, but strong sun can harm them.", ["Hats make eyes stronger.", "Sunlight cannot harm eyes.", "Hats stop children seeing."], "Balance."),
])


def body():
    think = ("<p><b>We need light to see. Dark is the absence of light.</b></p>"
             "<ul><li>Light sources give out light. We see other things because light reflects off them into our eyes.</li>"
             "<li>Smooth, shiny surfaces reflect light best. Reflective strips help people be seen at night.</li>"
             "<li>Never look directly at the Sun, even with sunglasses.</li></ul>")
    ex = [("Is the Moon a light source?", ["It reflects sunlight"], "No"),
          ("Which reflects best: foil or wool?", ["Smooth and shiny"], "foil")]
    mist = ["Thinking the Moon is a light source.", "Thinking you can see a little in total darkness.", "Thinking sunglasses make it safe to look at the Sun."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Light and seeing", B1 + [(L6.g_srcyn, 8), (L6.g_src, 4)]),
        ("Light sources", [(L6.g_src, 10), (g_dark, 6), (L6.g_srcyn, 4)]),
        ("Reflection", BR + [(g_refl, 12)]),
        ("Sun safety", BS + [(g_refl, 6), (g_dark, 6)]),
        ("Thinking about light", B5 + [(L6.g_src, 8), (g_refl, 4), (L6.g_srcyn, 3)]),
    ])
    make_uk(3, "light-and-dark", 10, "Light",
            "Recognise that they need light in order to see things and that dark is the absence of light. Notice that light is reflected from surfaces. "
            "Recognise that light from the sun can be dangerous and that there are ways to protect their eyes.",
            "Light and Dark",
            "Year 3 Science: Light and Dark Worksheets (Light Sources, Reflection, Sun Safety)",
            "Light and Dark",
            "Free Year 3 science worksheets on light and dark: needing light to see, light sources, reflection, reflective materials and keeping eyes safe from the Sun. 100 questions with answers.",
            "No light, no seeing.",
            "Light reflects off things into our eyes.",
            body(),
            [("Why can't we see in the dark?", "We see things when light reflects off them into our eyes. Dark is the absence of light, so in total darkness no light reaches our eyes."),
             ("Is the Moon a light source?", "No. The Moon reflects light from the Sun. Light sources, such as the Sun, a torch or a candle, give out their own light."),
             ("How can I keep my eyes safe in the sun?", "Never look directly at the Sun, even with sunglasses. Wear sunglasses with UV protection and a hat with a brim on sunny days.")],
            sets)


if __name__ == "__main__":
    main()
