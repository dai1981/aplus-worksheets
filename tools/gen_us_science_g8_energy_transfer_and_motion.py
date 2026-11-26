# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Energy Transfer and Motion (MS-PS3-5)
  python tools/gen_us_science_g8_energy_transfer_and_motion.py
Construct, use, and present arguments to support the claim that when the kinetic energy of an object changes,
energy is transferred to or from the object. Pushes and pulls transfer energy (work = force × distance);
friction and air resistance transfer energy out as thermal energy and sound; collisions pass energy between objects;
total energy is conserved.
Wrong answers come from real mistakes: "energy is used up / destroyed when something stops",
"speeding up needs no energy input", "a bouncing ball makes new energy".
"""
from sci_common import Unit, item, bank, lesson, make, table, People, comma

U = Unit(80107)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def J(x):
    return comma(int(x)) + " J" if x == int(x) else "%g J" % x


CASES = [("A soccer player kicks a ball that was at rest.", "to the ball", "from the player's foot"),
         ("A car brakes and comes to a stop.", "from the car", "to the brakes and road as thermal energy"),
         ("A bowling ball hits the pins and slows down.", "from the ball", "to the pins and as sound"),
         ("A sled slides across flat snow and slowly stops.", "from the sled", "to the snow and air as thermal energy"),
         ("A pitcher throws a baseball.", "to the ball", "from the pitcher's arm"),
         ("A catcher catches a fast baseball in a glove.", "from the ball", "to the glove and hand as thermal energy and sound"),
         ("A wind gust pushes a sailboat faster.", "to the boat", "from the moving air"),
         ("A cyclist pedals harder and speeds up.", "to the bike and rider", "from the cyclist's muscles (chemical energy)"),
         ("A rolling marble hits a resting marble, which starts to roll.", "to the second marble", "from the first marble"),
         ("A skydiver opens a parachute and slows down.", "from the skydiver", "to the air"),
         ("A hockey stick hits a puck.", "to the puck", "from the stick"),
         ("A rolling ball goes onto a carpet and stops.", "from the ball", "to the carpet as thermal energy")]


def g_dir():
    s, d, src = R.choice(CASES)
    who = P.next()[0]
    k = R.random() < 0.5
    if not once((s, k)):
        return None
    if k:
        a = "Kinetic energy is transferred %s." % d
        opp = d.replace("to the", "from the") if d.startswith("to") else d.replace("from the", "to the")
        return item("%s observes: “%s” Which statement about the object's kinetic energy is correct?" % (who, s), a,
                    ["Kinetic energy is transferred %s." % opp, "No energy is transferred.", "Energy is created from nothing."],
                    "When an object speeds up, energy goes into it; when it slows down, energy leaves it.")
    a = "%s" % src
    w = [x[2] for x in CASES if x[2] != src]
    return item("%s observes: “%s” Where does the energy come from or go?" % (who, s), a[0].upper() + a[1:], [x[0].upper() + x[1:] for x in R.sample(w, 3)],
                "Energy is never used up; it moves from one place to another.")


def g_work():
    who = P.next()[0]
    F = R.choice([5, 10, 20, 25, 40, 50])
    d = R.choice([2, 3, 4, 5, 10])
    if not once(("w", F, d)):
        return None
    th = R.choice(["a cart", "a box", "a wagon", "a sled", "a shopping cart"])
    W = F * d
    k = R.choice(["work", "ke"])
    if k == "work":
        return item("%s pushes %s with a force of %d N for %d m. How much energy is transferred to it? (energy transferred = force × distance)" % (who, th, F, d), J(W),
                    [J(F + d), J(F), J(W * 2)], "%d N × %d m = %s." % (F, d, J(W)))
    return item("%s pushes %s from rest with %d N for %d m on a smooth floor (no friction). How much kinetic energy does it gain?" % (who, th, F, d), J(W), ["0 J", J(F), J(W / 2)],
                "All the work becomes kinetic energy: %d × %d = %s." % (F, d, J(W)))


def g_budget():
    who = P.next()[0]
    tot = R.choice([100, 200, 400, 500, 800])
    th = R.choice([10, 20, 25, 30, 40])
    snd = R.choice([1, 2, 5])
    if th + snd >= 90:
        return None
    if not once(("b", tot, th, snd)):
        return None
    lost = tot * (th + snd) // 100
    if tot * (th + snd) % 100:
        return None
    left = tot - lost
    rows = [["Kinetic energy before", J(tot)], ["Thermal energy from friction", J(tot * th // 100)], ["Sound energy", J(tot * snd // 100)], ["Kinetic energy after", "?"]]
    tab = table(["Energy in %s's cart test" % who, "Amount"], rows)
    return item(tab + "What is the kinetic energy after? (Energy is conserved.)", J(left), [J(tot), J(lost), J(tot + lost)], "%s − %s = %s." % (J(tot), J(lost), J(left)))


def g_bounce():
    who = P.next()[0]
    h = R.choice([100, 120, 150, 200, 80])
    f = R.choice([50, 60, 70, 75, 80])
    if h * f % 100:
        return None
    h2 = h * f // 100
    if not once(("bo", h, f)):
        return None
    k = R.choice(["why", "next"])
    if k == "why":
        return item("%s drops a ball from %d cm. It bounces back to only %d cm. What best explains this?" % (who, h, h2), "Some energy was transferred to the floor and air as thermal energy and sound.",
                    ["The ball made less energy on the way up.", "Energy was destroyed when it hit the floor.", "Gravity turned off at the top."], "Energy is conserved but spreads out.")
    h3 = h2 * f / 100
    return item("%s's ball keeps %d%% of its height on each bounce. Dropped from %d cm, it reaches %d cm on the first bounce. About how high is the second bounce?" % (who, f, h, h2), "%g cm" % h3,
                ["%d cm" % h2, "%d cm" % h, "%g cm" % (h2 - (h - h2))], "%d × %d%% = %g cm." % (h2, f, h3))


B1 = bank([
    ("When an object speeds up, what must happen?", "Energy must be transferred to it.", ["Energy must be destroyed.", "Its mass must increase.", "Nothing needs to happen."], "More KE requires an energy input."),
    ("When a moving object slows down, where does its kinetic energy go?", "It is transferred to other objects or the surroundings, often as thermal energy and sound.", ["It is destroyed.", "It turns into mass.", "It stays in the object as speed."],
     "Energy is conserved."),
    ("What is the law of conservation of energy?", "Energy cannot be created or destroyed, only transferred or changed in form.", ["Energy is always used up.", "Energy grows over time.", "Only kinetic energy is conserved."], "Total energy stays the same."),
    ("What is work in science?", "energy transferred when a force moves an object a distance", ["any kind of effort", "time spent on homework", "a force with no motion"], "Work = force × distance."),
    ("Why do your hands get warm when you rub them together?", "Kinetic energy is transferred into thermal energy by friction.", ["Your hands make new energy.", "Blood boils.", "Air pushes heat into them."], "Friction transfers energy."),
    ("In a collision between a moving cart and a resting cart, what happens to energy?", "Some kinetic energy is transferred from the moving cart to the resting cart.", ["All energy is destroyed.", "Both carts lose all energy.", "The resting cart gives energy to the moving cart."],
     "Energy moves between objects."),
    ("Which change shows energy being transferred out of an object?", "a rolling ball slowing down", ["a ball speeding up down a hill", "a car accelerating", "a rocket launching"], "Slowing down means losing KE."),
    ("Why does a pendulum eventually stop swinging?", "Energy is transferred to the air and the pivot as thermal energy.", ["Its energy is destroyed.", "Gravity stops working.", "It runs out of mass."], "Friction and air resistance."),
])
B5 = bank([
    ("Ava claims a stopped car has lost its energy forever. How should you argue against this?", "The energy was transferred to the brakes, tires and air as thermal energy.", ["She is right.", "The car still has the same speed.", "Energy turned into mass."],
     "Use conservation of energy."),
    ("Leo measures a cart's speed before and after it hits a block. The cart slows and the block moves. What evidence shows energy transfer?", "The block starts moving while the cart slows down.", ["The cart is red.", "Both stay still.", "The cart speeds up."],
     "Changes in motion show transfer."),
    ("Mia's brakes feel hot after riding downhill. What does this show?", "Kinetic energy was transferred into thermal energy.", ["Brakes make energy.", "The sun heated the brakes only.", "Energy disappeared."], "Friction heats brakes."),
    ("A cart has 60 J of kinetic energy. After rolling across a rug it has 20 J. How much energy was transferred to the rug and air?", "40 J", ["20 J", "60 J", "80 J"], "60 − 20 = 40 J."),
    ("Which test best supports the claim that a push transfers energy to a cart?", "Push with larger forces and show the cart's speed increases more.", ["Paint the cart a new color.", "Leave the cart alone.", "Weigh the cart only."],
     "Connect the energy input to the change in motion."),
])


def body():
    think = ("<p>When an object's <b>kinetic energy changes</b>, energy has been <b>transferred</b> to it or from it.</p>"
             "<ul><li><b>Speeding up</b>: energy is transferred <b>to</b> the object (a push, a kick, a motor).</li>"
             "<li><b>Slowing down</b>: energy is transferred <b>from</b> the object to other objects or to the surroundings as <b>thermal energy and sound</b>.</li></ul>"
             "<p>A force that moves an object transfers energy: <b>energy transferred = force × distance</b>. Energy is never used up; the <b>total stays the same</b>.</p>")
    ex = [("You push a box with 20 N for 3 m. Energy transferred?", ["20 × 3"], "60 J"),
          ("A sled has 300 J of KE and stops. Where did the energy go?", ["Friction with the snow."], "to the snow and air as thermal energy")]
    mist = ["Thinking energy is destroyed when something stops.",
            "Thinking an object can speed up without an energy input.",
            "Thinking a bouncing ball creates energy."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Energy and changes in motion", B1 + [(g_dir, 12)]),
        ("Transferring energy", [(g_dir, 12), (g_work, 8)]),
        ("Work and kinetic energy", [(g_work, 14), (g_budget, 6)]),
        ("Where energy goes", [(g_budget, 10), (g_bounce, 10)]),
        ("Arguing with evidence", B5 + [g_bounce, g_budget, g_work, g_dir]),
    ])
    make("grade-8", "energy-transfer-and-motion", 7, "MS-PS3-5",
         "Construct, use, and present arguments to support the claim that when the kinetic energy of an object changes, energy is transferred to or from the object.",
         "Energy Transfer and Motion",
         "Grade 8 Energy Transfer Worksheets: Work, Friction, Collisions and Conservation of Energy",
         "Energy Transfer and Motion",
         "Free middle school science worksheets on energy transfer and motion (NGSS MS-PS3-5): how kinetic energy changes when energy is transferred, work = force × distance, friction, collisions and conservation of energy. 100 practice questions with answers.",
         "A change in kinetic energy means energy was transferred.",
         "Speeding up needs energy in; slowing down sends energy out as heat and sound. The total is always conserved.",
         body(),
         [("What happens to energy when a moving object stops?", "Its kinetic energy is transferred to other objects and the surroundings, mostly as thermal energy and sound. The energy is not destroyed."),
          ("How is energy transferred to an object?", "A force that moves the object over a distance transfers energy (work = force × distance)."),
          ("Why doesn't a bouncing ball return to the same height?", "Some energy is transferred to the floor and air as thermal energy and sound on each bounce.")],
         sets)


if __name__ == "__main__":
    main()
