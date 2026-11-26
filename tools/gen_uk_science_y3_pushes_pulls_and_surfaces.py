# -*- coding: utf-8 -*-
"""
UK Year 3 science: Pushes, Pulls and Surfaces (Forces and magnets)
  python tools/gen_uk_science_y3_pushes_pulls_and_surfaces.py
Forces as pushes and pulls, contact forces and forces that act at a distance, what forces do (start, stop, speed up,
slow down, change direction or shape), and comparing how things move on different surfaces (ramp investigations).
Reuses the ramp and helpful-friction questions of the Year 5 friction unit (new seed) and adds Year 3 questions.
Wrong answers come from real mistakes: "a moving thing has a force inside it", "smooth surfaces slow things more",
"magnets need to touch to work", "pulling a door is a push".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y5_friction as F5

F5.U = Unit(61312)
F5.R = F5.U.R
F5.P = People(F5.R)
uk_sci.USED.clear()
U, R, P = F5.U, F5.R, F5.P

PP = [("kicking a football", "push"), ("opening a drawer", "pull"), ("closing a drawer", "push"), ("pressing a doorbell", "push"), ("pulling a sledge up a hill", "pull"),
      ("throwing a ball", "push"), ("pulling up weeds", "pull"), ("squashing modelling clay", "push"), ("taking a book off a shelf", "pull"), ("pushing a pram", "push"),
      ("a dog tugging on its lead", "pull"), ("hammering a nail", "push"), ("towing a caravan with a car", "pull"), ("typing on a keyboard", "push"),
      ("pulling a zip up", "pull"), ("stretching an elastic band", "pull"), ("hitting a tennis ball with a racket", "push"), ("lifting a bag with its handles", "pull"),
      ("leaning on a gate to open it", "push"), ("pulling a cracker at Christmas", "pull")]


def g_pp():
    a, f = R.choice(PP)
    if not once(("pp", a)):
        return None
    return item("Is %s a push or a pull?" % a, "a " + f, ["a " + ("pull" if f == "push" else "push"), "not a force at all", "a magnet"], "A push moves something away from you; a pull moves it towards you.")


CT = [("kicking a ball", "contact"), ("friction between shoes and the floor", "contact"), ("pushing a trolley", "contact"), ("pulling a rope", "contact"),
      ("a magnet pulling a paperclip from a short distance away", "non-contact"), ("gravity pulling a dropped apple down", "non-contact"),
      ("two magnets pushing each other apart before they touch", "non-contact"), ("air resistance on a parachute", "contact"),
      ("water pushing up on a floating boat", "contact"), ("a magnet pulling a steel pin through a sheet of paper", "non-contact"),
      ("squeezing a sponge", "contact"), ("gravity keeping the Moon going round the Earth", "non-contact")]


def g_contact():
    a, f = R.choice(CT)
    if not once(("ct", a)):
        return None
    ans = "a contact force (the things touch)" if f == "contact" else "a non-contact force (it acts at a distance)"
    return item("Is this a contact force or a non-contact force: %s?" % a, ans,
                ["a non-contact force (it acts at a distance)" if f == "contact" else "a contact force (the things touch)", "not a force", "a light source"],
                "Most forces need things to touch. Magnetism and gravity act at a distance.")


DO = [("A football is still. A player kicks it.", "It starts to move."), ("A rolling ball hits a wall.", "It stops or changes direction."),
      ("A cyclist pedals harder.", "The bike speeds up."), ("A cyclist squeezes the brakes.", "The bike slows down."),
      ("A tennis ball is hit back over the net.", "It changes direction."), ("Modelling clay is squashed.", "It changes shape."),
      ("A goalkeeper catches a ball.", "It stops."), ("A sponge is squeezed.", "It changes shape.")]


def g_do():
    s, a = R.choice(DO)
    if not once(("do", s)):
        return None
    w = sorted({x[1] for x in DO if x[1] != a and not (x[1].startswith("It stops") and a.startswith("It stops"))})
    return item("%s What does the force do?" % s, a, R.sample(w, 3), "Forces can start, stop, speed up, slow down, change direction or change shape.")


TIERS = [["ice"], ["a polished wooden floor", "a smooth plastic tray", "lino"], ["carpet", "grass"], ["a bath towel", "gravel", "a thick fluffy rug"]]
RANK = {x: i for i, t in enumerate(TIERS) for x in t}


def g_surf():
    s = [R.choice(t) for t in TIERS]
    k = R.random() < 0.5
    if not once(("su", tuple(sorted(s)), k)):
        return None
    if k:
        a = min(s, key=lambda x: RANK[x])
        return item("A toy car is pushed with the same force across four surfaces: %s. On which will it travel furthest?" % ", ".join(sorted(s)), a, [x for x in s if x != a],
                    "The smoothest surface has the least friction, so the car goes furthest.")
    a = max(s, key=lambda x: RANK[x])
    return item("A toy car is pushed with the same force across four surfaces: %s. On which will it stop soonest?" % ", ".join(sorted(s)), a, [x for x in s if x != a],
                "The roughest surface has the most friction, so the car stops soonest.")


B1 = bank([
    ("What is a force?", "a push or a pull", ["a type of material", "a light source", "a kind of sound"], "Forces make things move or change."),
    ("Which force slows things down when surfaces rub together?", "friction", ["magnetism", "light", "sound"], "Rough surfaces have more friction."),
    ("Which force pulls things down towards the Earth?", "gravity", ["friction", "a push", "magnetism"], "That is why things fall."),
    ("What is a contact force?", "a force where the things must touch", ["a force that acts at a distance", "a magnet", "a shadow"], "Kicking a ball."),
    ("Which force can act without touching?", "magnetism", ["kicking", "friction", "squeezing"], "Magnets work at a distance."),
    ("What happens when you push a toy car harder?", "It goes faster and further.", ["It goes slower.", "It stops at once.", "Nothing changes."], "Bigger force, bigger effect."),
    ("Can a force change the shape of something?", "Yes, for example squashing a ball of clay.", ["No, never.", "Only magnets can.", "Only gravity can."], "Squash, stretch, twist."),
    ("Why is it harder to push a box across carpet than across a smooth floor?", "Carpet is rougher, so there is more friction.", ["Carpet has less friction.", "The box is heavier on carpet.", "Carpet is magnetic."], "Rough surfaces grip."),
])
B5 = bank([
    ("Why do ice skates glide so well?", "Ice is very smooth, so there is little friction.", ["Ice has lots of friction.", "Skates are magnetic.", "Gravity is weaker on ice."], "Smooth surfaces."),
    ("Why do playground slides have smooth surfaces?", "so there is little friction and you slide down easily", ["to make you stop at the top", "so you can climb up them", "to keep them warm"], "Less friction, more speed."),
    ("Why are trainers given bumpy rubber soles?", "to increase friction so you do not slip", ["to make you slide", "to make them heavier", "to make them magnetic"], "More grip."),
    ("How could you test which surface lets a toy car travel furthest?", "Let the same car roll down the same ramp from the same height onto each surface and measure the distance.", ["Push the car harder on some surfaces.", "Use a different car each time.", "Only test one surface."], "Fair test."),
    ("A sledge moves easily on snow but not on grass. Why?", "Snow is smoother, so there is less friction.", ["Grass is smoother.", "Snow is magnetic.", "The sledge is heavier on grass."], "Compare surfaces."),
])


def body():
    think = ("<p><b>A force is a push or a pull.</b></p>"
             "<ul><li>Forces can start or stop things, speed them up or slow them down, change their direction or shape.</li>"
             "<li>Most forces need contact. Magnetism and gravity act at a distance.</li>"
             "<li>Things move further on smooth surfaces, because rough surfaces cause more friction.</li></ul>")
    ex = [("Opening a drawer: push or pull?", ["It comes towards you"], "pull"),
          ("Ice or carpet: furthest?", ["Smoother, less friction"], "ice")]
    mist = ["Thinking a moving thing has a force inside it.", "Thinking smooth surfaces slow things more.", "Thinking pulling a door is a push."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Pushes and pulls", B1 + [(g_pp, 12)]),
        ("What forces do", [(g_pp, 6), (g_do, 8), (g_contact, 6)]),
        ("Contact and surfaces", [(g_contact, 6), (g_surf, 10), (F5.g_use, 4)]),
        ("Ramp investigation", [(F5.g_ramp, 20)]),
        ("Thinking about forces", B5 + [(F5.g_ramp, 6), (g_surf, 6), (F5.g_use, 3)]),
    ])
    make_uk(3, "pushes-pulls-and-surfaces", 12, "Forces and magnets",
            "Compare how things move on different surfaces. Notice that some forces need contact between two objects, but magnetic forces can act at a distance.",
            "Pushes, Pulls and Surfaces",
            "Year 3 Science: Pushes, Pulls and Surfaces Worksheets (Forces and Friction)",
            "Pushes and Pulls",
            "Free Year 3 science worksheets on forces: pushes and pulls, what forces do, contact and non-contact forces, and how things move on different surfaces. 100 questions with answers.",
            "A force is a push or a pull.",
            "Rough surfaces slow things more than smooth ones.",
            body(),
            [("What is a force?", "A force is a push or a pull. Forces can make things start, stop, speed up, slow down, change direction or change shape."),
             ("What is a contact force?", "A force where the two things touch, such as kicking a ball or friction. Magnetism and gravity are non-contact forces: they act at a distance."),
             ("Why do things move further on smooth surfaces?", "Smooth surfaces have less friction, so less force slows the object down. Rough surfaces like carpet have more friction.")],
            sets)


if __name__ == "__main__":
    main()
