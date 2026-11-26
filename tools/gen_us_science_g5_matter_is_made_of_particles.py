# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Matter Is Made of Particles (5-PS1-1)
  python tools/gen_us_science_g5_matter_is_made_of_particles.py
Matter has mass and takes up space, even when it is too small to see. A particle model explains
solids, liquids and gases, air in a ball or a syringe, sugar that seems to disappear in water
and salt left behind when salt water evaporates.
Wrong answers come from real mistakes: "air is nothing", "dissolved sugar is gone",
"particles get bigger when a gas spreads", "light and heat are matter".
"""
from sci_common import (Unit, item, bank, lesson, make, figure, fig, svg_wrap, rect, circle, text, line, arrow,
                        B, BLUE, GREEN, INK, RED, ORANGE, People)

U = Unit(50101)
R = U.R
P = People(R)

MATTER = ["air", "water", "a rock", "steam", "dust", "smoke", "orange juice", "oxygen gas", "a pencil", "sand",
          "the helium in a balloon", "water vapor", "milk", "a cloud", "salt", "a sugar cube", "carbon dioxide gas"]
NOT_MATTER = ["sunlight", "heat", "a sound", "a shadow", "a thought", "a rainbow", "a radio signal", "the light from a lamp"]

SOLIDS = ["an iron nail", "a copper coin", "an ice cube", "a wooden block", "a glass marble", "a rock", "a gold ring"]
LIQUIDS = ["water in a glass", "cooking oil", "milk in a cup", "apple juice", "maple syrup", "liquid soap"]
GASES = ["the air in a room", "steam above a pot", "helium in a balloon", "carbon dioxide in soda bubbles", "oxygen in a tank", "water vapor in the air"]
STATE_OF = {}
for s_, xs in (("solid", SOLIDS), ("liquid", LIQUIDS), ("gas", GASES)):
    for x in xs:
        STATE_OF[x] = s_


# ------------------------------------------------------------ pictures
def model(state, col=BLUE, seed=None, label=None):
    """Box with particles: solid = neat rows touching, liquid = touching but jumbled at the bottom, gas = far apart."""
    r = R if seed is None else __import__("random").Random(seed)
    W, H = 120, 100
    s = [rect(6, 6, W - 12, H - 12, "#ffffff", INK, 2)]
    pts = []
    if state == "solid":
        for row in range(4):
            for c in range(6):
                pts.append((22 + c * 15.2, 82 - row * 15))
    elif state == "liquid":
        x, y = 20, 83
        while len(pts) < 20:
            pts.append((x + r.uniform(-1.5, 1.5), y + r.uniform(-1.5, 1.5)))
            x += 14.5 + r.uniform(-1, 1)
            if x > W - 22:
                x = 22 + r.uniform(0, 8)
                y -= 14
    else:
        tries = 0
        while len(pts) < 9 and tries < 500:
            tries += 1
            p = (r.uniform(20, W - 20), r.uniform(20, H - 20))
            if all((p[0] - a) ** 2 + (p[1] - b) ** 2 > 25 ** 2 for a, b in pts):
                pts.append(p)
    for x, y in pts:
        s.append(circle(x, y, 6.5, col, INK, 1))
    if state != "solid":
        for x, y in pts[:4] if state == "gas" else pts[-3:]:
            s.append(arrow(x + 6, y - 4, x + 15, y - 12, INK, 1.5, 6))
    return svg_wrap(W, H, "".join(s), label or ("particle model of a " + state))


def syringe(vol, total=60, sealed=True):
    W, H = 260, 70
    x0, x1 = 30, 230
    L = x1 - x0
    xp = x0 + L * vol / float(total)
    s = [rect(x0, 18, L, 34, "#ffffff", INK, 2)]
    for k in range(0, total + 1, 10):
        x = x0 + L * k / float(total)
        s.append(line(x, 18, x, 26, INK, 1.5) + text(x, 64, str(k), 10, weight=400))
    s.append(rect(x0, 20, xp - x0, 30, "#e8f1fb", "none", 0))
    import random as _r
    rr = _r.Random(vol * 7 + total)
    n = 10
    for i in range(n):
        s.append(circle(x0 + 6 + rr.uniform(0, max(4, xp - x0 - 12)), rr.uniform(26, 44), 3, BLUE, BLUE, 1))
    s.append(rect(xp, 16, 8, 38, "#999999", INK, 1.5) + line(xp + 8, 35, x1 + 20, 35, INK, 4))
    s.append(rect(6, 29, 24, 12, INK if sealed else "#ffffff", INK, 1.5))
    s.append(text(x1 + 4, 12, "mL", 10, weight=400))
    return svg_wrap(W, H, "".join(s), "syringe with air, plunger at %d mL" % vol)


# ------------------------------------------------------------ set 1: what is matter
def g_not_matter():
    nm = R.choice(NOT_MATTER)
    ms = R.sample(MATTER, 3)
    return item("Which of these is <b>not</b> matter?", nm, ms,
                cap(nm) + " has no mass and does not take up space, so it is not matter. " + cap(ms[0]) + " is matter: it is made of particles.")


def g_is_matter():
    m = R.choice(MATTER)
    ns = R.sample(NOT_MATTER, 3)
    return item("Which of these <b>is</b> matter?", m, ns,
                cap(m) + " has mass and takes up space, so it is matter. Light, heat, sound and shadows are not matter.")


def cap(s):
    return s[0].upper() + s[1:]


B1 = bank([
    ("What is matter?", "anything that has mass and takes up space", ["anything you can see", "only solids and liquids", "anything that gives off light"],
     "Matter is anything that has mass and takes up space. Air is matter even though you cannot see it."),
    ("What is all matter made of?", "particles too small to see", ["tiny drops of water", "pieces you can see with your eyes", "light and heat"],
     "All matter is made of particles that are far too small to see, even with a hand lens."),
    ("Why can't you see the particles that make up a rock?", "They are much too small to see.", ["The rock has no particles.", "The particles are hidden inside a shell.", "Only liquids are made of particles."],
     "Rocks, water and air are all made of particles. The particles are too small to see."),
    ("Which state of matter keeps its own shape?", "solid", ["liquid", "gas", "all three states"],
     "A solid keeps its shape. A liquid takes the shape of its container, and a gas spreads out to fill it."),
    ("Which state of matter takes the shape of its container but keeps the same volume?", "liquid", ["solid", "gas", "none of them"],
     "A liquid flows to fit its container, but 1 cup of water is still 1 cup in any glass."),
    ("Which state of matter spreads out to fill any container?", "gas", ["solid", "liquid", "only ice"],
     "Gas particles move freely, so a gas fills the whole container it is in."),
    ("Air is a mixture of gases. Is air matter?", "Yes, because it has mass and takes up space.", ["No, because you cannot see it.", "No, because it is not a solid.", "Only when the wind blows."],
     "You cannot see air, but it has mass and takes up space. A balloon gets bigger when you fill it with air."),
    ("Which tool would help you show that air takes up space?", "a balloon you blow up", ["a thermometer", "a magnet", "a flashlight"],
     "As you blow air into a balloon, the balloon gets bigger. The air takes up space inside it."),
    ("Steam and water vapor are which state of matter?", "gas", ["solid", "liquid", "not matter at all"],
     "Water vapor is water as a gas. Its particles are far apart, so you cannot see it."),
    ("Ice, liquid water and water vapor are made of", "the same kind of particles", ["three different kinds of particles", "no particles", "particles only when it is liquid"],
     "Ice, water and water vapor are all water. The particles are the same. Only how close they are and how they move changes."),
    ("Which statement about particles is true?", "Particles of matter are always moving.", ["Particles in a solid never move.", "Particles are big enough to see with a hand lens.", "Only gases are made of particles."],
     "Particles are always moving. In a solid they vibrate in place, in a liquid they slide past each other, and in a gas they move freely."),
    ("A scientist says, “Everything around you is made of particles.” Which object is <b>not</b> included?", "the light from a flashlight", ["your desk", "the air you breathe", "the water you drink"],
     "Light is energy, not matter, so it is not made of particles of matter."),
])


# ------------------------------------------------------------ set 2: particle models
def g_model_material():
    st = R.choice(["solid", "liquid", "gas"])
    pools = {"solid": SOLIDS, "liquid": LIQUIDS, "gas": GASES}
    ans = R.choice(pools[st])
    others = [x for k, v in pools.items() if k != st for x in v]
    wr = R.sample(others, 3)
    return item(fig(model(st)) + "The model shows the particles of a material at room temperature. Which material could it be?",
                ans, wr, "The particles are " + {"solid": "packed in neat rows and touching, so this is a solid",
                                                  "liquid": "touching but jumbled and free to slide past each other, so this is a liquid",
                                                  "gas": "far apart and moving freely, so this is a gas"}[st] + ": " + ans + ".")


def g_model_state():
    st = R.choice(["solid", "liquid", "gas"])
    thing = R.choice(["a sample", "a material", "one substance", "a mystery material"])
    qs = R.choice(["Which state of matter does the model show?", "What state of matter is " + thing + " in, according to this model?",
                   "Look at how close the particles are. Which state of matter is this?"])
    wr = [x for x in ["solid", "liquid", "gas"] if x != st] + ["not matter"]
    why = {"solid": "In a solid the particles are packed tightly in a pattern and only vibrate in place.",
           "liquid": "In a liquid the particles touch, but they are not in rows and they slide past each other.",
           "gas": "In a gas the particles are far apart and move quickly in all directions."}[st]
    return item(fig(model(st)) + qs, st, wr, why)


B2 = bank([
    ("In which state of matter are the particles farthest apart?", "gas", ["solid", "liquid", "They are the same distance apart in every state."],
     "Gas particles are far apart. That is why a gas can be squeezed into a smaller space."),
    ("In which state of matter do the particles stay in fixed places and only vibrate?", "solid", ["liquid", "gas", "all three states"],
     "Solid particles are held in place. They vibrate but do not move past each other, so a solid keeps its shape."),
    ("Why can a liquid be poured?", "Its particles can slide past each other.", ["Its particles are very far apart.", "Its particles do not move at all.", "It has no particles."],
     "Liquid particles touch, but they are not locked in place. They slide past each other, so the liquid flows."),
    ("Why does a gas fill its whole container?", "Its particles move freely and spread out.", ["Its particles are stuck together.", "Its particles get bigger.", "Gases have no particles."],
     "Gas particles move quickly in every direction until they spread through the whole space. The particles themselves do not get bigger."),
    ("Why is it hard to squeeze a block of wood into a smaller size?", "Its particles are already packed close together.", ["It has no particles.", "Its particles are far apart.", "Its particles are too big to move."],
     "In a solid the particles are already touching, so there is almost no empty space to push them into."),
    ("When ice melts into water, what happens to the particles?", "They stay the same but start to slide past each other.", ["They change into new particles.", "They disappear.", "They get much bigger."],
     "Melting does not make new particles. The same water particles just move more freely."),
    ("When water boils and turns into water vapor, the particles", "move faster and spread far apart", ["get smaller and disappear", "stop moving", "turn into air particles"],
     "Heating makes the particles move faster. In water vapor they are far apart, so you cannot see them."),
    ("A student draws a model of air in a jar. Which drawing is best?", "a few dots spread out all over the jar", ["dots packed in neat rows at the bottom", "an empty jar", "one big dot in the middle"],
     "Air is a gas, so the particles should be far apart and spread through the whole jar. An empty jar would mean air is nothing."),
    ("Which state of matter can be squeezed into a much smaller space?", "gas", ["solid", "liquid", "none of them"],
     "Gas particles have lots of space between them, so they can be pushed closer together."),
    ("Which is the same in an ice cube and in a puddle of the same water?", "the kind of particles", ["the shape", "how the particles move", "how close the particles are in a pattern"],
     "Both are made of water particles. The ice has them locked in place, and the puddle lets them slide."),
    ("What is between the particles of a gas?", "empty space", ["more air", "water", "tiny rocks"],
     "There is empty space between gas particles. That is why gases can be compressed."),
    ("A model of a solid should show particles that are", "close together in a pattern", ["far apart and moving freely", "touching but sliding at the bottom only", "different sizes for every solid"],
     "Solid particles are packed tightly in a pattern and vibrate in place."),
])


# ------------------------------------------------------------ set 3: evidence
def g_syringe():
    a = R.choice([50, 60])
    b = R.choice([v for v in range(20, a, 10)])
    q = fig(syringe(b, 60)) + ("A sealed syringe was filled with %d mL of air. Then the plunger was pushed in to %d mL. Nothing got out. What does this show?" % (a, b))
    return item(q, "The air particles were pushed closer together.", ["Some of the air disappeared.", "The air particles got smaller.", "Air is not matter."],
                "The same air particles are still inside. They now have less empty space between them, so they fit in %d mL." % b)


def g_ball():
    p = P.next()
    k = R.choice(["basketball", "soccer ball", "football", "volleyball"])
    return item("%s pumps more air into a %s, and the ball gets firmer. What explains this?" % (p[0], k),
                "More air particles are packed inside the ball.", ["The air in the ball turns into a solid.", "Air has no mass, so nothing changes.", "The ball's rubber gets heavier by itself."],
                "Pumping adds more air particles. They push on the inside of the ball from all sides, so it feels firmer.")


def g_smell():
    smells = ["popcorn", "perfume", "baking bread", "an orange being peeled", "a cut onion", "garlic in a pan", "a scented candle"]
    sm = R.choice(smells)
    d = R.choice([3, 5, 8, 10])
    return item("You can smell %s from %d meters away, even though you cannot see anything moving through the air. What is the best explanation?" % (sm, d),
                "Tiny particles from it spread through the air to your nose.", ["The smell is light that travels to your eyes.", "Smells are not made of anything.", "The air in the room turns into the food."],
                "Particles too small to see leave the source and spread out among the air particles until some reach your nose.")


def g_dissolve():
    k = R.choice(["sugar", "salt", "drink mix", "a sugar cube"])
    v = R.choice([100, 200, 250, 300])
    return item("You stir %s into %d mL of water until you cannot see it anymore. Where is it?" % (k, v),
                "It broke into particles too small to see that are mixed in the water.", ["It is gone and no longer exists.", "It turned into air.", "It sank and hid under the glass."],
                "Dissolving breaks the %s into tiny particles that spread through the water. You can still taste it, and its mass is still there." % k.replace("a sugar cube", "sugar"))


def g_evaporate():
    g = R.choice([5, 10, 15, 20, 25, 30])
    p = P.next()
    return item("%s dissolves %d grams of salt in a dish of water. A week later all the water has evaporated. What is left in the dish?" % (p[0], g),
                "about %d grams of salt" % g, ["nothing at all", "about %d grams of water" % g, "about %d grams of salt" % (g * 2)],
                "The water particles went into the air, but the salt particles stayed. The same %d grams of salt is left as crystals." % g)


B3 = bank([
    ("A drop of food coloring is placed in still water. After an hour the whole glass is colored. What does this show?", "Particles of coloring spread out among the water particles.", ["The coloring was not matter.", "The water turned into coloring.", "The coloring got bigger."],
     "Particles of coloring and water are always moving. Over time the coloring particles spread through the water."),
    ("Food coloring spreads faster in hot water than in cold water. Why?", "Particles move faster when they are warmer.", ["Hot water has no particles.", "Cold water particles are bigger.", "Coloring cannot mix with cold water."],
     "Warmer particles move faster, so the coloring spreads out more quickly."),
    ("A balloon is put on the neck of an empty bottle. The bottle is placed in hot water and the balloon puffs up. Why?", "The air particles move faster and spread out, pushing into the balloon.", ["New air is made by the hot water.", "The water gets into the balloon.", "The balloon gets heavier and bigger."],
     "Heated air particles move faster and spread apart. They take up more space, so some move into the balloon."),
    ("A puddle dries up on a sunny day. Where did the water go?", "Its particles went into the air as water vapor.", ["It was destroyed by the sun.", "It turned into sand.", "It soaked up into the clouds as a liquid at once."],
     "Water evaporates: its particles leave the puddle and move into the air as a gas, too small to see."),
    ("Water drops form on the outside of a cold glass of lemonade. Where did the water come from?", "water vapor in the air that cooled and turned into liquid", ["lemonade that leaked through the glass", "the glass itself", "nowhere: it was made from nothing"],
     "The air has water vapor in it. When the vapor touches the cold glass, its particles slow down and join into drops (condensation)."),
    ("You pour 1 cup of sand into 1 cup of marbles and the total is less than 2 cups. How is this a model of mixing water and alcohol?", "Small particles can fit into spaces between larger ones.", ["The sand disappears.", "Marbles are not matter.", "Mixing always makes things heavier."],
     "Particles of different sizes can fit into each other's gaps, just like sand fills the spaces between marbles."),
    ("A sealed bag of chips puffs up when it is taken up a high mountain. What is inside the bag that causes this?", "a gas, which is matter", ["nothing", "light", "a solid that grows"],
     "The bag is full of gas particles. With less air pushing on the bag from outside, the gas inside spreads out more."),
    ("Which observation is evidence that air takes up space?", "A cup pushed upside down into water stays dry inside.", ["Air is invisible.", "Wind feels cool.", "Sunlight shines through air."],
     "The air trapped in the cup keeps the water out. Two things cannot take up the same space."),
    ("Sugar is stirred into water and disappears. Which test would show that the sugar is still there?", "Taste the water, or let it evaporate and look for sugar.", ["Look at it with your eyes.", "Shine a flashlight on it.", "Put it in the freezer for 5 minutes."],
     "The water tastes sweet, and when it evaporates the sugar is left behind. The sugar was only too small to see."),
    ("A person is spraying air freshener in one corner of a room. Soon people across the room can smell it. Which model explains this best?", "Tiny particles moving and spreading through the air", ["Waves of light moving across the room", "The air freshener turning into heat", "The walls sending out the smell"],
     "The spray leaves tiny particles in the air. They keep moving and spread out across the room."),
])


# ------------------------------------------------------------ set 4: measuring matter you cannot see
def g_air_mass():
    a = R.randint(400, 600)
    d = R.randint(5, 20)
    k = R.choice(["ball", "beach ball", "soccer ball", "bike tire"])
    return item("A flat %s has a mass of %d g. After it is pumped full of air, its mass is %d g. What is the mass of the air inside?" % (k, a, a + d),
                "%d g" % d, ["0 g", "%d g" % (a + d), "%d g" % (2 * a + d)],
                "%d − %d = %d g. The air added mass, so air is matter." % (a + d, a, d))


def g_sugar_water():
    w = R.choice([100, 150, 200, 250, 300, 400])
    s = R.choice([10, 15, 20, 25, 30, 40, 50])
    k = R.choice(["sugar", "salt"])
    return item("%d g of %s is stirred into %d g of water until it disappears. What is the mass of the %s water?" % (s, k, w, k),
                "%d g" % (w + s), ["%d g" % w, "%d g" % (w - s), "%d g" % s],
                "The %s is still there as tiny particles: %d + %d = %d g." % (k, w, s, w + s))


def g_left_salt():
    tot = R.choice([120, 150, 210, 260, 330])
    salt = R.choice([10, 20, 30, 40])
    return item("A dish of salt water has a mass of %d g (not counting the dish). It contains %d g of salt. After all the water evaporates, what is the mass of what is left in the dish?" % (tot, salt),
                "%d g" % salt, ["0 g", "%d g" % (tot - salt), "%d g" % tot],
                "Only the water evaporated. The %d g of salt stays behind. The other %d g of water went into the air as vapor." % (salt, tot - salt))


def g_tank():
    e = R.randint(10, 15)
    f = R.randint(2, 6)
    return item("An empty scuba tank has a mass of %d kg. Filled with air pressed in tightly, it has a mass of %d kg. Which conclusion is correct?" % (e, e + f),
                "The air inside has a mass of %d kg." % f, ["Air has no mass.", "The air inside has a mass of %d kg." % (e + f), "The tank itself gained %d kg of metal." % f],
                "%d − %d = %d kg of air. Packing more air particles into the tank adds mass." % (e + f, e, f))


def g_volume_gas():
    v = R.choice([2, 3, 4, 5])
    return item("A balloon holds %d liters of air. All of the air is pumped into a box that holds only 1 liter, and the box is sealed. What is in the box?" % v,
                "all the same air particles, pushed closer together", ["only 1 liter's worth of particles, the rest disappeared", "no air", "liquid water"],
                "A gas can be compressed. The particles move closer together, but none of them disappear.")


B4 = bank([
    ("Why does a ball filled with air have more mass than the same ball when it is flat?", "Air particles have mass.", ["Air pulls the ball down.", "Rubber gets heavier when it stretches.", "It does not: air has no mass."],
     "Each air particle has a tiny mass. Many of them together add up to a mass you can measure."),
    ("Which tool is used to measure the mass of a sample of matter?", "a balance or scale", ["a thermometer", "a ruler", "a hand lens"],
     "Mass is measured with a balance or a scale, in grams or kilograms."),
    ("A cup of water is placed on a scale. Sugar is dissolved in it. What happens to the reading on the scale?", "It goes up by the mass of the sugar.", ["It goes back to the mass of the water.", "It goes down to zero.", "It stays the same because sugar disappears."],
     "The sugar is still in the cup as tiny particles, so its mass is added."),
    ("Two identical sealed jars are on a balance. One is filled with air pumped in tightly, the other has normal air. Which side goes down?", "the jar with extra air pumped in", ["the jar with normal air", "Neither: air has no mass.", "the lighter jar"],
     "More air particles means more mass, so that side of the balance goes down."),
    ("Which units are used to measure mass in science class?", "grams and kilograms", ["meters and centimeters", "liters and milliliters", "degrees Celsius"],
     "Mass is measured in grams (g) and kilograms (kg). Liters measure volume."),
    ("Salt water is boiled until all the water is gone. A white solid is left. What is the solid?", "the salt that was dissolved in the water", ["sugar made by the heat", "solid water", "dirt from the air"],
     "The salt was in the water the whole time as tiny particles. Only the water left as vapor."),
])


# ------------------------------------------------------------ set 5: investigations
def g_inv_syringe():
    p = P.next()
    k = R.choice(["water", "sand", "air"])
    good = {"air": "The plunger moves in easily, because air particles have space between them.",
            "water": "The plunger hardly moves, because water particles are already close together.",
            "sand": "The plunger hardly moves, because the grains and their particles are already packed."}
    wr = [v for kk, v in good.items() if kk != k] + ["The syringe gets lighter as you push."]
    return item("%s seals the tip of a syringe filled with %s and pushes the plunger. What should %s observe?" % (p[0], k, p[1]),
                good[k], wr, "Only a gas can be squeezed much. Liquids and solids already have their particles close together.")


B5 = bank([
    ("Grace fills a plastic bottle with hot air, caps it and puts it in the freezer. The next day the bottle is dented in. Which model explains this?", "The cooled air particles slowed down and pushed less on the inside of the bottle.", ["Air particles were destroyed by the cold.", "The bottle grew bigger.", "Water got into the bottle."],
     "Cold air particles move more slowly. They push less on the walls, so the air outside dents the bottle."),
    ("A class weighs a sealed bag with ice, then weighs it again when the ice has melted. Why must the bag be sealed?", "so no water can leak out or evaporate", ["so the ice melts faster", "so the bag stays cold", "so the scale reads zero"],
     "If water escaped, the mass would go down and the test would be unfair."),
    ("Which model shows what happens when salt dissolves in water?", "Salt particles spread out between the water particles.", ["Salt particles turn into water particles.", "Salt particles disappear.", "Water particles turn into salt."],
     "The salt particles break apart and mix in among the water particles. Both kinds are still there."),
    ("Eli blows up two balloons the same size. He puts one in a warm room and one outside on a cold night. What happens to the outside balloon?", "It gets a little smaller.", ["It gets much bigger.", "It pops right away.", "It stays exactly the same."],
     "Cooling makes the air particles move more slowly and take up less space."),

    ("Leo says that when sugar dissolves, it is destroyed. Which evidence best shows he is wrong?", "The mass of the water plus sugar stays the same before and after stirring.", ["The water looks clear.", "The spoon gets wet.", "The sugar is white."],
     "If the sugar were destroyed, the mass would go down. It stays the same, so the sugar is still there as tiny particles."),
    ("Ava wants to show that air has mass. Which investigation is best?", "Weigh a flat ball, pump it up, then weigh it again.", ["Look at air with a hand lens.", "Blow on her hand and feel it.", "Measure the temperature of the air."],
     "Comparing the mass before and after adding air shows that the air itself has mass."),
    ("Students put the same amount of food coloring in hot water and in cold water. What should they keep the same to make it a fair test?", "the amount of water and the size of the cups", ["the temperature of both cups", "nothing, it does not matter", "the color only in one cup"],
     "Only the temperature should be different. Everything else, like the amount of water and coloring, should stay the same."),
    ("A class leaves two dishes of salt water in the sun. One dish is covered with plastic wrap. After 3 days, which dish has dry salt crystals?", "the uncovered dish", ["the covered dish", "both dishes", "neither dish"],
     "In the open dish the water vapor escapes into the air. Under the wrap the vapor is trapped and drips back down."),
    ("Noah wraps an ice cube in a bag, seals it and weighs it: 25 g. He weighs it again after it melts. What should the scale show?", "25 g", ["0 g", "less than 25 g", "more than 25 g"],
     "Melting does not add or remove particles. The water has the same mass as the ice: 25 g."),
    ("Which question could be answered with a particle model?", "Why does a gas spread to fill a room?", ["What color is the sky?", "How tall is the tree?", "Which day is the longest?"],
     "A particle model explains how matter behaves, like gas particles moving and spreading out."),
    ("Maya puts a balloon on the neck of a bottle and moves the bottle from hot water into ice water. What happens to the balloon?", "It shrinks, because the air particles slow down and move closer together.", ["It grows bigger.", "It fills with water.", "Nothing happens."],
     "Cooling slows the particles, so the air takes up less space and the balloon goes flat."),
    ("A student says that a jar with only air in it is empty. Which experiment shows the jar is not empty?", "Push the upside-down jar into water: water does not fill it.", ["Shake the jar and listen.", "Put the jar in sunlight.", "Weigh the jar on a bathroom scale."],
     "Air inside the jar takes up space, so water cannot get in. A bathroom scale is not exact enough to show the air's tiny mass."),
    ("Omar notices that a bicycle tire looks a little flat on a cold morning and fuller on a hot afternoon. No air was added. Why?", "Warm air particles move faster and push harder on the tire.", ["The tire made more air during the day.", "Cold air has no particles.", "The sun melts the tire."],
     "The same air is inside. When it warms, the particles move faster and push outward more."),
    ("Which statement best describes a good model of matter?", "It shows tiny particles that are always moving.", ["It shows matter as one solid piece with no parts.", "It shows only things you can see.", "It shows particles that never move."],
     "Scientists model all matter as tiny particles in motion. The spacing and motion depend on the state of matter."),
])


def body():
    sol, liq, gas = model("solid", seed=1), model("liquid", seed=2), model("gas", seed=3)
    pics = ("<div class='sn-row'>%s%s%s</div>" % (figure(sol, "Solid: packed in a pattern, vibrating in place."),
                                                  figure(liq, "Liquid: touching, sliding past each other."),
                                                  figure(gas, "Gas: far apart, moving freely.")))
    think = ("<p><b>Matter</b> is anything that has mass and takes up space. Rocks, water and air are all matter. "
             "Light, heat, sound and shadows are <b>not</b> matter.</p>"
             "<p>All matter is made of <b>particles</b> that are much too small to see. The particles are always moving. "
             "How close they are and how they move tells you the state of matter.</p>" + pics +
             "<p>You can find evidence for particles you cannot see: air makes a ball firm and can be squeezed in a syringe, "
             "dissolved sugar still makes water sweet and heavier, and salt is left behind when salt water evaporates.</p>")
    ex = [("A flat ball has a mass of 410 g. After it is pumped full of air its mass is 425 g. What does this show?",
           ["425 − 410 = 15 g.", "The air pumped in has a mass of 15 g, so air is matter even though you cannot see it."], "Air has mass: 15 g of air."),
          ("Sugar is stirred into water until you cannot see it. Is the sugar gone?",
           ["The water tastes sweet.", "If the water evaporates, sugar is left behind.", "The sugar broke into particles too small to see."], "No. It is still there as tiny particles.")]
    mist = ["Thinking air is nothing. Air is matter: it has mass and takes up space.",
            "Thinking dissolved sugar or salt is destroyed. It is still there as tiny particles.",
            "Thinking particles get bigger when a gas spreads out. The particles stay the same size; the space between them grows.",
            "Calling light, heat or sound matter. They are forms of energy, not matter."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is matter?", [g_not_matter, g_is_matter] + B1),
        ("Particle models of solids, liquids and gases", [g_model_material, g_model_state] + B2),
        ("Evidence for tiny particles", [g_syringe, g_ball, g_smell, g_dissolve, g_evaporate] + B3),
        ("Measuring matter you cannot see", [g_air_mass, g_sugar_water, g_left_salt, g_tank, g_volume_gas] + B4),
        ("Investigations", [g_inv_syringe] + B5),
    ])
    make("grade-5", "matter-is-made-of-particles", 1, "5-PS1-1",
         "Develop a model to describe that matter is made of particles too small to be seen.",
         "Matter Is Made of Particles",
         "Grade 5 Matter and Particles Worksheets: Solids, Liquids, Gases and Particle Models",
         "Matter and Particles",
         "Free Grade 5 science worksheets on matter and particles (NGSS 5-PS1-1): what matter is, particle models of solids, liquids and gases, and evidence such as air in a syringe and dissolved sugar. 100 practice questions with answers.",
         "All matter is made of particles too small to see.",
         "Matter has mass and takes up space. In solids the particles are packed in place, in liquids they slide past each other, and in gases they are far apart.",
         body(),
         [("What is matter made of?", "All matter is made of tiny particles that are much too small to see. Rocks, water and air are all made of particles."),
          ("Is air matter?", "Yes. Air has mass and takes up space. A ball pumped full of air has more mass than the same ball when it is flat."),
          ("How are particles arranged in solids, liquids and gases?", "In a solid they are packed in a pattern and vibrate in place. In a liquid they touch but slide past each other. In a gas they are far apart and move freely."),
          ("What happens to sugar when it dissolves in water?", "It breaks into particles too small to see that spread through the water. It is still there: the water tastes sweet and its mass goes up by the mass of the sugar.")],
         sets)


if __name__ == "__main__":
    main()
