# -*- coding: utf-8 -*-
"""
US Grade 5 Science: Gravity Pulls Objects Down (5-PS2-1)
  python tools/gen_us_science_g5_gravity.py
Earth's gravity pulls every object toward the center of Earth. "Down" means toward Earth's center,
wherever you are on the globe. Gravity acts without touching, gives objects weight, and makes
thrown, dropped and rolling objects move toward the ground.
Pictures: a globe with a person and four arrows; only the arrow toward the center is "down".
Wrong answers come from real mistakes: "down is the bottom of the page", "people in Australia
would fall off", "gravity needs air", "heavier objects always fall much faster".
"""
import math
from sci_common import Unit, item, bank, lesson, make, figure, fig, svg_wrap, circle, text, line, arrow, BLUE, GREEN, INK, RED, People

U = Unit(50106)
R = U.R
P = People(R)
PLACES = [(90, "at the North Pole"), (-90, "at the South Pole"), (0, "at a place on the right side of Earth"), (180, "at a place on the left side of Earth"),
          (45, "in the United States"), (-35, "in Australia"), (-60, "in Antarctica"), (135, "in Europe"), (-150, "in South America"), (20, "on a ship at sea")]


def globe(theta, label="globe with a person and four arrows", arrows=True, order=None):
    """theta: angle of the person on the globe (90 = top). Arrows A-D from the person:
    toward Earth's center, away from it, toward the bottom of the page, and sideways."""
    W = H = 300
    cx = cy = 150
    r = 62
    s = [circle(cx, cy, r, "#cfe3f5", INK, 2),
         "<path d='M%d %d q20 -18 40 -6 q14 10 30 2' fill='none' stroke='%s' stroke-width='2'/>" % (cx - 42, cy - 12, GREEN),
         "<path d='M%d %d q16 12 34 4' fill='none' stroke='%s' stroke-width='2'/>" % (cx - 14, cy + 26, GREEN),
         circle(cx, cy, 3, INK, INK, 1)]
    a = math.radians(theta)
    ux, uy = math.cos(a), -math.sin(a)          # outward direction on screen
    px, py = cx + (r + 2) * ux, cy + (r + 2) * uy
    hx, hy = cx + (r + 24) * ux, cy + (r + 24) * uy
    s.append(line(px, py, hx, hy, INK, 3) + circle(hx + 5 * ux, hy + 5 * uy, 6, "#ffd9a8", INK, 1.5))
    if arrows:
        ox, oy = cx + (r + 16) * ux, cy + (r + 16) * uy
        tx, ty = (-uy, ux) if ux <= 0 else (uy, -ux)          # sideways, pointing up the page
        if abs(ty) < 0.2:
            tx, ty = -uy, ux
        dirs = {"in": (-ux, -uy), "out": (ux, uy), "page": (0.0, 1.0), "side": (tx, ty)}
        def ang(d1, d2):
            return math.degrees(math.acos(max(-1, min(1, d1[0] * d2[0] + d1[1] * d2[1]))))
        if min(ang(dirs["page"], dirs[k]) for k in ("in", "out", "side")) < 45:
            dirs["page"] = (0.7071, 0.7071) if min(ang((0.7071, 0.7071), dirs[k]) for k in ("in", "out", "side")) > 44 else (-0.7071, 0.7071)
        order = order or ["in", "out", "page", "side"]
        for k, name in enumerate(order):
            dx, dy = dirs[name]
            L = 44 if name != "out" else 50
            st = 9 if name != "in" else 4
            col = [RED, BLUE, "#7d3c98", "#c27c0e"][k]
            s.append(arrow(ox + st * dx, oy + st * dy, ox + L * dx, oy + L * dy, col, 2.5, 8))
            s.append(text(ox + (L + 11) * dx, oy + (L + 11) * dy + 5, "ABCD"[k], 14, col=col))
    return svg_wrap(W, H, "".join(s), label).replace("<svg ", "<svg data-sq='1' ", 1)


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------ set 1: what gravity is
B1 = bank([
    ("What is gravity?", "a force that pulls objects toward each other, like Earth pulling things toward its center", ["a force that pushes objects away from Earth", "the air pressing down on things", "a force that only works on falling objects"],
     "Earth's gravity pulls every object toward Earth's center."),
    ("Does gravity need to touch an object to pull on it?", "No. Gravity pulls from a distance.", ["Yes, it only works by touching.", "Only through air.", "Only on metal objects."],
     "A ball falls even though nothing touches it. Gravity acts at a distance."),
    ("Which direction does Earth's gravity pull objects?", "toward the center of Earth", ["toward the North Pole", "away from Earth", "toward the sun"],
     "Everywhere on Earth, gravity pulls toward the center. That direction is what we call “down.”"),
    ("You let go of a pencil. Why does it fall?", "Earth's gravity pulls it down.", ["The air pushes it down.", "Pencils are heavy.", "Your hand pushes it."],
     "Once nothing holds the pencil up, gravity pulls it toward Earth."),
    ("What does a bathroom scale measure?", "how hard gravity pulls on you (your weight)", ["how tall you are", "how much air is around you", "how fast you move"],
     "Your weight is the pull of gravity on your body."),
    ("Why do rivers flow downhill?", "Gravity pulls the water down toward Earth's center.", ["Wind pushes all rivers.", "Water is attracted to the ocean.", "Fish swim the water down."],
     "Water moves to lower places because gravity pulls it."),
    ("A ball is thrown straight up. Why does it come back down?", "Gravity keeps pulling it toward Earth.", ["It runs out of air.", "Gravity only works on the way down.", "The ball gets heavier at the top."],
     "Gravity pulls on the ball the whole time, slowing it on the way up and pulling it back down."),
    ("Which is <b>not</b> caused by gravity?", "a magnet pulling a paper clip sideways", ["rain falling", "a sled sliding down a hill", "an apple falling from a tree"],
     "The magnet's pull is a magnetic force. Rain, sleds and apples move down because of gravity."),
    ("Is there gravity where there is no air, like on the Moon?", "Yes. Gravity does not need air.", ["No, gravity needs air.", "Only during the day.", "Only for rocks."],
     "The Moon has no air, but objects still fall there. Gravity works in empty space."),
    ("Which word describes the pull of gravity on an object?", "weight", ["volume", "temperature", "color"],
     "Weight is how strongly gravity pulls an object."),
])


# ------------------------------------------------------------ set 2: down on the globe
def g_globe():
    theta, place = R.choice(PLACES)
    order = ["in", "out", "page", "side"]
    R.shuffle(order)
    k = order.index("in")
    q = fig(globe(theta, order=order)) + "A person stands %s. Which arrow shows the direction that Earth's gravity pulls on the person?" % place
    w = ["arrow " + "ABCD"[i] for i in range(4) if i != k]
    return item(q, "arrow " + "ABCD"[k], w, "Gravity pulls toward the center of Earth, so arrow %s (pointing into the globe) is “down” for this person." % "ABCD"[k])


def g_drop():
    a, pa = R.choice(PLACES)
    b, pb = R.choice([x for x in PLACES if x[0] != a])
    obj = R.choice(["a ball", "a cup", "an apple", "a book", "a rock"])
    return item("Two children drop %s at the same time: one %s and one %s. Which way does each one fall?" % (obj, pa, pb),
                "Both fall toward the center of Earth.", ["Both fall toward the bottom of the page.", "One falls up and one falls down.", "Both float away into space."],
                "Down is toward Earth's center everywhere, so both objects fall toward the ground under their feet.")


B2 = bank([
    ("Why don't people in Australia fall off Earth?", "Gravity pulls them toward Earth's center, which is “down” for them too.", ["They hold on to the ground.", "Australia is on top of Earth.", "There is no gravity in Australia."],
     "Down is toward Earth's center everywhere on the globe."),
    ("On a globe, “down” is always", "toward the center of Earth", ["toward the bottom of the globe", "toward the South Pole", "toward Antarctica"],
     "The bottom of a picture is not the same as down. Down points into the Earth."),
    ("A student at the South Pole drops a ball. In a picture of Earth with the South Pole at the bottom, which way does the ball fall?", "up the page, toward Earth's center", ["down the page, away from Earth", "to the left", "it floats"],
     "At the South Pole, Earth's center is above the person in the picture. The ball falls toward the center."),
    ("Rain falls in Brazil and in Canada. How do the directions compare?", "Both fall toward Earth's center, so they point in different directions in space.", ["They fall in exactly the same direction in space.", "Rain in Brazil falls up.", "Rain only falls in the north."],
     "Each place has its own “down,” always pointing to Earth's center."),
    ("Why do we say gravity pulls objects “down”?", "Down is our word for the direction toward Earth's center.", ["Gravity points to the bottom of the map.", "Down means south.", "Gravity only pulls heavy things."],
     "Wherever you stand, down points toward the middle of Earth."),
    ("Earth is round, yet a plumb line (a weight on a string) hangs straight down everywhere. Where does it point?", "toward Earth's center", ["toward the North Pole", "toward the sun", "toward the equator"],
     "A plumb line lines up with the pull of gravity, which points to the center."),
])


# ------------------------------------------------------------ set 3: falling, weight and other forces
def g_scale():
    w = R.randint(20, 150)
    p = P.next()
    return item("%s puts a bag of apples on a spring scale. The spring stretches and the scale reads %d newtons. What force stretches the spring?" % (p[0], w),
                "Earth's gravity pulling the apples down", ["the air pushing the apples up", "a magnet in the scale", "the apples pushing up"],
                "Gravity pulls the apples toward Earth, and the spring stretches to hold them. %d newtons is their weight." % w)


def g_moon():
    w = R.choice([60, 90, 120, 180, 240, 300, 360])
    k = R.choice(["astronaut", "rover", "space suit", "toolbox"])
    return item("Gravity on the Moon is about 1/6 as strong as on Earth. A %s weighs %d newtons on Earth. About how much does it weigh on the Moon?" % (k, w),
                "%d newtons" % (w // 6), ["%d newtons" % w, "%d newtons" % (w * 6), "0 newtons"],
                "%d ÷ 6 = %d newtons. The amount of matter is the same, but the Moon's weaker gravity pulls less." % (w, w // 6))


B3 = bank([
    ("A ball rolls off a table. Which path does it follow?", "It curves down to the floor.", ["It keeps going straight sideways forever.", "It goes up.", "It stops in the air."],
     "Gravity pulls the ball down while it keeps moving sideways, so its path curves to the floor."),
    ("A feather falls more slowly than a coin. Why?", "Air pushes up on the wide feather more than on the coin.", ["Gravity does not pull on feathers.", "Feathers have no mass.", "Coins are magnetic."],
     "Gravity pulls both. Air resistance slows the feather much more. Without air they fall together."),
    ("On the Moon there is no air. An astronaut drops a hammer and a feather together. What happens?", "They hit the ground at the same time.", ["The feather floats away.", "The hammer lands first.", "Neither falls."],
     "Without air to slow the feather, gravity makes both fall the same way."),
    ("A book sits still on a table. Is gravity still pulling on it?", "Yes. The table pushes up just as hard, so it does not move.", ["No, gravity stops when objects are still.", "No, tables block gravity.", "Only if the book is heavy."],
     "Gravity pulls the book down, and the table pushes it up with an equal force."),
    ("Why does a parachute help a skydiver land safely?", "Air pushes up on the parachute and slows the fall.", ["It turns off gravity.", "It makes the skydiver weigh less.", "It pulls the skydiver up into the sky."],
     "Gravity still pulls the skydiver down, but air resistance on the big parachute slows the fall."),
    ("A kicked soccer ball flies up and then comes down. What changes its direction?", "Earth's gravity pulling it down", ["the wind only", "the grass", "the ball's color"],
     "Gravity keeps pulling down on the ball until it lands."),
    ("Which object would weigh the most on Earth?", "the one with the most mass", ["the biggest one", "the one highest up", "the shiniest one"],
     "Gravity pulls harder on objects with more mass. A small rock can weigh more than a big pillow."),
    ("A spring scale shows the weight of a rock. The rock is then lowered into water and the scale reads less. Did gravity get weaker?", "No. The water pushes up on the rock.", ["Yes, gravity is weaker in water.", "Yes, the rock lost mass.", "No, the scale broke."],
     "Water pushes up on objects (buoyancy). Gravity still pulls the same."),
])


# ------------------------------------------------------------ set 4: evidence and arguments
def g_claim():
    claims = [("All objects fall toward the ground when dropped.", "Every dropped object in the class test fell to the floor, no matter where it was dropped."),
              ("Gravity pulls toward Earth's center.", "Plumb lines all over the world hang toward Earth's center."),
              ("Gravity pulls water down.", "Rivers flow from mountains down to the sea."),
              ("Gravity acts without touching.", "A ball falls even though nothing touches it."),
              ("Objects have weight because of gravity.", "A spring scale stretches when an object hangs from it.")]
    c, ev = R.choice(claims)
    w = [e for cc, e in claims if cc != c]
    return item("Which evidence best supports the claim: “%s”" % c, ev, R.sample(w, 3), "This observation directly shows that " + c[0].lower() + c[1:-1] + ".")


B4 = bank([
    ("A student claims, “Gravity only pulls things toward the bottom of the map.” Which evidence shows this is wrong?", "People in South America drop things and they fall to their ground, too.", ["Maps are flat.", "The South Pole is at the bottom.", "Balls bounce."],
     "Objects fall toward the ground everywhere on Earth, not toward the bottom of a map."),
    ("Which observation shows that gravity can act from far away?", "The Moon stays in orbit around Earth.", ["A magnet picks up a nail.", "You push a cart.", "Wind moves a kite."],
     "Earth's gravity pulls on the Moon across space, keeping it in orbit."),
    ("Why does a ball rolled on flat ground eventually stop, but a ball on a hill speeds up as it rolls down?", "On the hill, gravity pulls the ball down the slope.", ["Hills have no friction.", "Flat ground has no gravity.", "Balls like hills."],
     "On a slope, part of gravity's pull points along the hill, speeding the ball up."),
    ("A model of Earth is a ball with toy people stuck all around it. What should all their “down” arrows point to?", "the center of the ball", ["the floor of the classroom", "the top of the ball", "the nearest window"],
     "Down is toward the center of Earth for every person."),
])


# ------------------------------------------------------------ set 5: investigations
B5 = bank([
    ("Ava drops a crumpled sheet of paper and a flat sheet from the same height. The crumpled one lands first. What variable did she change?", "the shape of the paper", ["the mass of the paper", "the height", "the strength of gravity"],
     "Both sheets have the same mass. Only the shape changed, which changes how much air slows the paper."),
    ("Leo drops two balls of the same size: a golf ball and a ping-pong ball, from 1 meter. They land at almost the same time. What does this show?", "Gravity makes objects fall at about the same rate when air resistance is small.", ["Heavier objects always fall much faster.", "Gravity does not affect light objects.", "Ping-pong balls are magnetic."],
     "The pull of gravity speeds up all objects in the same way. Air resistance makes only a small difference here."),
    ("Mia wants to test whether the height of a ramp changes how fast a car rolls down. What should she keep the same?", "the car and the length and surface of the ramp", ["the height of the ramp", "nothing", "only the color of the car"],
     "Only the height changes, so the test is fair."),
    ("Why should students repeat a drop test several times?", "to make sure the results are reliable", ["to make gravity stronger", "to change the answer", "to use more balls"],
     "Repeated trials show whether the result happens every time."),
    ("Noah hangs a weight on a string and holds it still. Which direction does the string point?", "straight down toward Earth's center", ["sideways", "up", "toward the nearest wall"],
     "The weight pulls the string in the direction of gravity."),
    ("Sam measures that a ball dropped from 2 meters takes a little more than half a second to fall. What would happen if he did this in a different country?", "It would fall about the same way, toward the ground there.", ["It would fall up.", "It would fall sideways.", "It would not fall at all."],
     "Gravity works the same way everywhere on Earth's surface."),
    ("Which is the best way to show a younger student that “down” is toward Earth's center?", "Put toy figures all around a globe and point each one's arrow into the globe.", ["Draw an arrow to the bottom of a map.", "Drop a ball in the classroom only.", "Look at the sky."],
     "A globe model shows that down points to the center from every place."),
    ("Zoe throws a ball forward. Which force makes it curve toward the ground?", "gravity", ["magnetism", "friction from her hand", "the force of her throw"],
     "Her throw moves it forward; gravity pulls it down, so its path curves."),
])


def body():
    pics = ("<div class='sn-row'>%s%s</div>" % (figure(globe(45, "person in the United States: gravity points to Earth's center", arrows=False), "In the United States, down is toward Earth's center."),
                                                 figure(globe(-35, "person in Australia: gravity points to Earth's center", arrows=False), "In Australia, down is also toward Earth's center.")))
    think = ("<p><b>Gravity</b> is a force that pulls objects toward Earth. It pulls from a distance: nothing has to touch the object. "
             "Gravity gives objects their <b>weight</b> and makes them fall, roll downhill and come back down when thrown.</p>"
             "<p>Earth is a sphere, and gravity pulls everything toward its <b>center</b>. That is what “down” means. "
             "So people all around the world stand on the ground and objects fall toward their feet.</p>" + pics)
    ex = [("A person at the South Pole drops a ball. In a picture with the South Pole at the bottom, which way does it fall?", ["Gravity pulls toward the center of Earth.", "From the South Pole, the center is up the page."], "Toward Earth's center (up the page)."),
          ("A feather and a coin are dropped on the Moon. Which lands first?", ["The Moon has gravity but no air.", "No air means nothing slows the feather."], "They land at the same time.")]
    mist = ["Thinking down means the bottom of the page or map. Down means toward Earth's center.",
            "Thinking gravity needs air or only works on falling things. It works everywhere, even on objects at rest.",
            "Thinking heavier objects always fall much faster. Differences come from air resistance.",
            "Thinking people on the other side of Earth would fall off."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What gravity does", B1 + [(g_scale, 4)]),
        ("Which way is down?", [(g_globe, 10), g_drop] + B2),
        ("Falling, weight and air", [g_scale, g_moon] + B3),
        ("Evidence and arguments", [(g_globe, 6), g_claim] + B4 + [(g_moon, 3)]),
        ("Investigations", B5 + [(g_globe, 4), (g_drop, 4), (g_claim, 4)]),
    ])
    make("grade-5", "gravity", 6, "5-PS2-1",
         "Support an argument that the gravitational force exerted by Earth on objects is directed down.",
         "Gravity Pulls Objects Down",
         "Grade 5 Gravity Worksheets: Which Way Is Down, Weight and Falling Objects",
         "Gravity",
         "Free Grade 5 science worksheets on gravity (NGSS 5-PS2-1): Earth's gravity pulls toward its center, down on a globe, weight, falling objects and air resistance. 100 practice questions with answers.",
         "Earth's gravity pulls every object toward Earth's center.",
         "Down means toward Earth's center, everywhere on the globe. Gravity pulls without touching and gives objects their weight.",
         body(),
         [("Which direction does gravity pull?", "Earth's gravity pulls objects toward the center of Earth. That direction is “down,” wherever you are on the globe."),
          ("Why don't people on the other side of Earth fall off?", "Gravity pulls them toward Earth's center, which is down for them too."),
          ("Does gravity need air?", "No. Gravity works in empty space. Objects fall on the Moon, which has no air."),
          ("Do heavy objects fall faster?", "Without air, all objects fall at the same rate. With air, light, wide objects like feathers are slowed down more.")],
         sets)


if __name__ == "__main__":
    main()
