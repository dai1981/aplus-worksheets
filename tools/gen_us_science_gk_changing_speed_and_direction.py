# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Changing Speed and Direction (K-PS2-2)
  python tools/gen_us_science_gk_changing_speed_and_direction.py
Analyze data to determine if a design solution works as intended to change the speed or direction of an object with a
push or a pull. Ramps (steep = fast), bumpers and walls that turn a ball, carpet and sand that slow it, and simple tests
"did it work?". Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "a ball can only go straight", "rough carpet makes a car go faster", "a test worked
even though the ball missed the goal".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, arrow, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9102)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def ramp_svg(steep, obj="ball", label=None):
    h = 80 if steep else 30
    s = "<path d='M20 110 L20 %d L200 110 Z' fill='#c99a63' stroke='%s' stroke-width='1.6'/>" % (110 - h, INK)
    s += K.icon(obj, 34, 110 - h - 10, 0.45)
    s += "<line x1='0' y1='110' x2='300' y2='110' stroke='%s' stroke-width='2'/>" % INK
    if label:
        s += text(110, 132, label, 14)
    return svg_wrap(300, 140 if label else 120, s, "a %s ramp with a %s at the top" % ("steep" if steep else "low", obj))


def g_ramp():
    steep = R.random() < 0.5
    obj = R.choice(["ball", "block", "apple"])
    who = P.next()[0]
    k = R.choice(["speed", "far"])
    if not once((steep, obj, k)):
        return None
    nm = {"ball": "a ball", "block": "a toy car", "apple": "an apple"}[obj]
    if obj == "block":
        obj = "ball"
    pic = fig(ramp_svg(steep, obj))
    if k == "speed":
        return item(pic + "%s lets %s go down this %s ramp. How fast will it go?" % (who, nm, "steep" if steep else "low"), "fast" if steep else "slow",
                    ["slow" if steep else "fast", "it will not move", "it will go up"], "Steep ramp, fast. Low ramp, slow.")
    return item(pic + "%s lets %s roll down this %s ramp. Will it roll far or not far?" % (who, nm, "steep" if steep else "low"), "far" if steep else "not far",
                ["not far" if steep else "far", "it will roll up the ramp", "it will float"], "A steeper ramp gives a bigger push.")


def bounce_svg(wall):
    s = "<rect x='0' y='0' width='320' height='130' fill='#eef6e8' stroke='%s' stroke-width='1.5'/>" % INK
    s += K.icon("ball", 40, 100, 0.35)
    if wall:
        s += "<rect x='180' y='70' width='70' height='12' fill='#8a5a2b' transform='rotate(-35 215 76)'/>"
        s += arrow(55, 96, 200, 86, "#d9822b", 3, 9) + arrow(206, 74, 220, 18, "#d9822b", 3, 9)
        s += "<rect x='200' y='0' width='60' height='10' fill='#3f8f3f'/>" + text(230, 24, "goal", 11)
    else:
        s += arrow(55, 96, 300, 96, "#d9822b", 3, 9)
        s += "<rect x='200' y='0' width='60' height='10' fill='#3f8f3f'/>" + text(230, 24, "goal", 11)
    return svg_wrap(320, 130, s, "a ball rolling %s" % ("into a wall that turns it toward the goal" if wall else "straight past the goal"))


def g_wall():
    wall = R.random() < 0.6
    who = P.next()[0]
    k = R.choice(["what", "work"])
    if not once((wall, k), 2):
        return None
    pic = fig(bounce_svg(wall))
    if k == "what":
        if wall:
            return item(pic + "%s's ball hits the wall. What does the wall do?" % who, "It changes the ball's direction.", ["It makes the ball stop forever.", "It makes the ball bigger.", "Nothing."],
                        "A wall can push a ball a new way.")
        return item(pic + "%s's ball rolls with no wall. Which way does it go?" % who, "straight", ["it turns to the goal", "it goes up", "backward"], "Nothing pushes it, so it goes straight.")
    if wall:
        return item(pic + "%s wants the ball to reach the goal. Did the wall work?" % who, "Yes. The ball turned to the goal.", ["No. It missed.", "No. The ball stopped.", "No. The wall fell."],
                    "Check the result: it reached the goal.")
    return item(pic + "%s wants the ball to reach the goal. Did this work?" % who, "No. It went straight past.", ["Yes. It reached the goal.", "Yes. It stopped at the goal.", "Yes. It turned."],
                "Add a wall or bumper to change direction.")


SURF = [("a smooth floor", "fast", "far"), ("ice", "fast", "far"), ("a wood table", "fast", "far"), ("thick carpet", "slow", "not far"),
        ("sand", "slow", "not far"), ("tall grass", "slow", "not far"), ("a bumpy rug", "slow", "not far"), ("a mat of bubble wrap", "slow", "not far"),
        ("a gym floor", "fast", "far"), ("a sidewalk", "fast", "far"), ("mud", "slow", "not far"), ("gravel", "slow", "not far"), ("a towel", "slow", "not far"), ("a smooth kitchen floor", "fast", "far")]


def g_surf():
    a, sp, fr = R.choice(SURF)
    who = P.next()[0]
    if not once(a):
        return None
    return item(fig(K.card("ball")) + "%s rolls a ball on %s. How far will it roll?" % (who, a), fr, ["not far" if fr == "far" else "far", "it will roll up", "it will not move at all"],
                "Smooth things let a ball go far. Rough things slow it down.")


def g_pick2():
    a = R.choice([x for x in SURF if x[1] == "fast"])
    b = R.choice([x for x in SURF if x[1] == "slow"])
    who = P.next()[0]
    q = R.choice(["stop", "far"])
    if not once((a[0], b[0], q)) or not once(("p", q), 12):
        return None
    x, y = (a, b) if R.random() < 0.5 else (b, a)
    ans = b[0] if q == "stop" else a[0]
    return item("%s wants the toy car to %s. Should %s roll it on %s or on %s?" % (who, "slow down and stop soon" if q == "stop" else "roll far", who, x[0], y[0]), ans,
                [b[0] if ans == a[0] else a[0], "Both are the same.", "Neither one."], "Rough slows it. Smooth lets it go far.")


CH = [("You kick a ball that is rolling to you.", "direction"), ("You give a rolling ball a harder push.", "speed"), ("A soccer goalie catches the ball.", "speed"),
      ("A ball hits a wall and bounces back.", "direction"), ("A bowling ball hits the pins and they fly sideways.", "direction"),
      ("You push a swing a little harder.", "speed"), ("A toy car rolls onto carpet.", "speed"), ("A tennis racket hits the ball.", "direction"),
      ("You brake on your bike.", "speed"), ("A marble rolls into a bumper and turns.", "direction")]


def g_change():
    s, k = R.choice(CH)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s watches: %s What changes most?" % (who, s), "the %s" % k, ["the %s" % ("direction" if k == "speed" else "speed"), "the color", "the size"],
                "A push or pull can change speed or direction.")


def g_test():
    who = P.next()[0]
    goal = R.choice(["stop before the line", "go into the box", "roll past the chair"])
    t = [R.choice(["yes", "no"]) for _ in range(3)]
    if t.count("yes") != 1 or not once((goal, tuple(t))):
        return None
    designs = ["A", "B", "C"]
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (d, "worked" if r == "yes" else "did not work") for d, r in zip(designs, t))
    tab = "<table class='sn-table'><tr><th>Design</th><th>Result</th></tr>%s</table>" % rows
    a = designs[t.index("yes")]
    return item(tab + "%s tests 3 designs to make a ball %s. Which design should %s use?" % (who, goal, who), "design " + a, ["design " + d for d in designs if d != a] + ["none of them"],
                "Use the design that worked.")


def g_dist():
    rows = R.sample([("smooth floor", 10, 15), ("carpet", 3, 6), ("grass", 2, 4), ("wood table", 9, 13), ("sand", 1, 3), ("rug", 4, 7)], 3)
    vals = [R.randint(lo, hi) for _, lo, hi in rows]
    names = [r[0] for r in rows]
    if len(set(vals)) < 3:
        return None
    who = P.next()[0]
    k = R.choice(["far", "stop"])
    if not once((tuple(names), k)) or not once(("d", k), 10):
        return None
    sv = ""
    for i, (n, v) in enumerate(zip(names, vals)):
        y = 22 + i * 34
        sv += text(60, y + 5, n, 12)
        sv += K.icon("ball", 130, y, 0.25) + "<line x1='138' y1='%d' x2='%d' y2='%d' stroke='#d9822b' stroke-width='3'/>" % (y, 138 + v * 14, y)
        sv += text(152 + v * 14, y + 5, str(v), 12)
    pic = svg_wrap(380, 110, sv, "how far a ball rolled: " + ", ".join("%s %d steps" % (n, v) for n, v in zip(names, vals)))
    if k == "far":
        a = names[vals.index(max(vals))]
        return item(fig(pic) + "%s rolls the same ball with the same push on 3 floors. Where did it roll farthest?" % who, "on the " + a, ["on the " + n for n in names if n != a] + ["all the same"],
                    "Longest line: %d steps." % max(vals))
    a = names[vals.index(min(vals))]
    return item(fig(pic) + "%s wants the ball to stop soon. Which floor works best?" % who, "the " + a, ["the " + n for n in names if n != a] + ["all the same"],
                "Shortest line: %d steps." % min(vals))


B1 = bank([
    ("What can a push do to a moving ball?", "make it go faster or change its direction", ["make it a different color", "make it smaller", "nothing ever"], "Pushes change motion."),
    ("A ball rolls down a steep ramp. How does it go?", "fast", ["slow", "up", "it does not move"], "Steep is fast."),
    ("What makes a rolling ball slow down?", "rough ground, like grass or sand", ["a smooth floor", "ice", "a shiny table"], "Rough slows it."),
    ("How can you make a ball turn?", "put a wall or bumper in its way", ["blow on it softly from far away", "look at it", "sing to it"], "Walls push it a new way."),
    ("A ball hits a wall. What happens?", "It bounces and changes direction.", ["It goes through the wall.", "It gets bigger.", "It turns into a block."], "Direction changes."),
    ("How do you know a design worked?", "test it and see if it did the job", ["guess", "look at its color", "ask a rock"], "Look at the result."),
    ("What can stop a rolling ball?", "a hand catching it", ["a smooth floor", "a steep ramp", "a harder push"], "Catching is a pull and push."),
    ("Which ramp makes a car go faster?", "a steep ramp", ["a flat board", "a low ramp", "no ramp"], "Steeper, faster."),
])
B5 = bank([
    ("Ava wants her marble to go slower. What can she change?", "make the ramp lower", ["make the ramp steeper", "push it harder", "use ice"], "Lower is slower."),
    ("Leo's ball misses the goal. What can he add?", "a wall to turn the ball", ["more ice", "a bigger ball", "nothing"], "Change direction."),
    ("Mia's car rolls off the table. What can stop it?", "a soft bumper at the edge", ["a steeper ramp", "a harder push", "a smooth floor"], "Slow it down."),
    ("Kai tries 3 ramps. The car stops at the line only with ramp B. Which ramp worked?", "ramp B", ["ramp A", "ramp C", "all of them"], "Use the data."),
    ("Zoe's marble goes too fast. She puts a towel on the ramp. What happens?", "It goes slower.", ["It goes faster.", "It flies up.", "Nothing."], "Rough slows it."),
])


def body():
    pic = "<div style='display:flex;gap:10px;flex-wrap:wrap'>%s%s</div>" % (ramp_svg(True, label="steep: fast"), ramp_svg(False, label="low: slow"))
    ex = [("A ball rolls down a steep ramp. Fast or slow?", ["Steep is fast."], "fast"),
          ("A ball hits a wall. What changes?", ["It bounces a new way."], "its direction")]
    mist = ["Thinking a ball can only go straight.",
            "Thinking rough carpet makes a car go faster.",
            "Saying a test worked when the ball missed the goal."]
    return kid_lesson(pic, "We can change how things move.",
                      ["Speed: steep ramp fast, rough ground slow.", "Direction: a wall turns a ball.", "Test it. Did it work?"], ex, mist)


def main():
    sets = U.sets([
        ("Fast and slow", B1 + [(g_ramp, 6), (g_surf, 6)]),
        ("Ramps and floors", [(g_ramp, 6), (g_surf, 2), (g_change, 6), (g_pick2, 6)]),
        ("Changing direction", [(g_wall, 6), (g_change, 4), (g_pick2, 5), (g_dist, 5)]),
        ("Did it work?", [(g_test, 8), (g_dist, 7), (g_pick2, 3), (g_wall, 2)]),
        ("Motion designers", B5 + [(g_dist, 8), (g_test, 1), (g_pick2, 2), (g_surf, 4)]),
    ])
    make("kindergarten", "changing-speed-and-direction", 2, "K-PS2-2",
         "Analyze data to determine if a design solution works as intended to change the speed or direction of an object with a push or a pull.",
         "Changing Speed and Direction",
         "Kindergarten Speed and Direction Worksheets: Ramps, Walls and Did It Work?",
         "Speed and Direction",
         "Free kindergarten science worksheets on changing speed and direction (NGSS K-PS2-2): ramps, rough and smooth floors, walls that turn a ball and simple tests. 100 picture questions with answers.",
         "Change speed. Change direction.",
         "Ramps and floors change speed. Walls change direction.",
         body(),
         [("How can you make a ball go faster?", "Push it harder or roll it down a steeper ramp."),
          ("How can you make a ball turn?", "Put a wall or bumper in its path. The push from the wall changes its direction."),
          ("How do you know a design works?", "Test it and look at the result. Did the ball reach the goal or stop in time?")],
         sets)


if __name__ == "__main__":
    main()
