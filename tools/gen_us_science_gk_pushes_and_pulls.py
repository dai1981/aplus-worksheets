# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Pushes and Pulls (K-PS2-1)
  python tools/gen_us_science_gk_pushes_and_pulls.py
Plan and conduct an investigation to compare the effects of different strengths or different directions of pushes and
pulls on the motion of an object. Push or pull? A big push makes a ball go faster and farther; a small push, slower.
An object moves the way it is pushed. Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "opening a door is always a push", "a soft push makes it go farther",
"a ball moves toward the push".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, arrow, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9101)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def hand(x, y, left=True):
    """a simple mitten-shaped hand; fingers point toward the object"""
    d = 1 if left else -1
    s = "<rect x='%g' y='%g' width='30' height='16' rx='4' fill='#e8893a' stroke='%s' stroke-width='1.2'/>" % (x - 44 if left else x + 14, y - 8, INK)
    s += "<path d='M%g %g q%g -16 %g 0 q%g 16 %g 0 Z' fill='#f3c9a0' stroke='%s' stroke-width='1.5'/>" % (x - 14 * d, y - 14, 16 * d, 30 * d, 0, -30 * d, INK)
    s += "<path d='M%g %g q%g 0 %g 14 q%g 14 %g 14 Z' fill='#f3c9a0' stroke='%s' stroke-width='1.5'/>" % (x - 14 * d, y - 14, 30 * d, 30 * d, 0, -30 * d, INK)
    return s


def push_svg(size, dirn="right", obj="ball", label=None):
    """a hand pushing an object; arrow length and thickness show strength"""
    w = {"small": 3, "big": 8}[size]
    L = {"small": 40, "big": 90}[size]
    s = ""
    if dirn == "right":
        s += hand(44, 64, True) + K.icon(obj, 92, 64, 0.7) + arrow(124, 64, 124 + L, 64, "#d9822b", w, 8 + w)
    else:
        s += hand(256, 64, False) + K.icon(obj, 208, 64, 0.7) + arrow(176, 64, 176 - L, 64, "#d9822b", w, 8 + w)
    if label:
        s += text(150, 114, label, 14)
    return svg_wrap(300, 122 if label else 110, s, "a %s push to the %s on a %s" % (size, dirn, obj))


ACTS = [("kick a ball", "push", "ball"), ("open a drawer", "pull", None), ("close a drawer", "push", None), ("pull a wagon", "pull", None),
        ("push a swing", "push", None), ("tug a rope", "pull", None), ("ring a doorbell", "push", "bell"), ("fly a kite on a string", "pull", None),
        ("walk a dog on a leash", "pull", "dog"), ("roll a ball to a friend", "push", "ball"), ("push a shopping cart", "push", None),
        ("pull a sled up a hill", "pull", "snow"), ("pick an apple off a tree", "pull", "apple"), ("knock blocks over", "push", "block"),
        ("press a button", "push", None), ("pull a weed out of the garden", "pull", "sprout"), ("zip up a coat", "pull", "coat"),
        ("slide a cup across the table", "push", "cup")]


def g_pp():
    a, k, pic = R.choice(ACTS)
    who = P.next()[0]
    if not once(a):
        return None
    fg = fig(K.card(pic)) if pic else ""
    return item(fg + "%s wants to %s. Is that a push or a pull?" % (who, a), k, ["pull" if k == "push" else "push", "neither", "both at once"],
                "A push moves it away. A pull moves it closer.")


def g_strong():
    size = R.choice(["small", "big"])
    who = P.next()[0]
    k = R.choice(["far", "fast", "which"])
    obj = R.choice(["ball", "block", "cup", "apple", "drum", "rock"])
    if not once((size, k, obj)):
        return None
    pic = fig(push_svg(size, R.choice(["right", "left"]), obj))
    nm = {"ball": "ball", "block": "block", "cup": "cup", "apple": "apple", "drum": "toy drum", "rock": "rock"}[obj]
    if k == "far":
        return item(pic + "%s gives the %s a %s push. How far will it go?" % (who, nm, size), "far" if size == "big" else "not far", ["not far" if size == "big" else "far", "it will not move", "it will go up"],
                    "Big push, far. Small push, not far.")
    if k == "fast":
        return item(pic + "%s gives the %s a %s push. How fast will it move?" % (who, nm, size), "fast" if size == "big" else "slow", ["slow" if size == "big" else "fast", "it will not move", "backward"],
                    "Big push, fast. Small push, slow.")
    return item(pic + "Look at the arrow. Is %s's push big or small?" % who, size, ["big" if size == "small" else "small", "no push", "a pull"], "A big arrow means a big push.")


def g_dir():
    d = R.choice(["right", "left"])
    who = P.next()[0]
    obj = R.choice(["ball", "block", "cup", "apple", "drum", "rock"])
    if not once((d, obj)):
        return None
    s = (hand(44, 60, True) + K.icon(obj, 92, 60, 0.7)) if d == "right" else (hand(256, 60, False) + K.icon(obj, 208, 60, 0.7))
    pic = svg_wrap(300, 110, s, "a hand pushing a %s from the %s side" % (obj, "left" if d == "right" else "right"))
    return item(fig(pic) + "%s pushes the %s. Which way will it go?" % (who, {"drum": "toy drum"}.get(obj, obj)), "to the %s, away from the hand" % d,
                ["to the %s, toward the hand" % ("left" if d == "right" else "right"), "straight up", "it will not move"], "Things move the way you push them.")


DATA = [("ball", "steps"), ("toy car", "blocks"), ("marble", "steps"), ("box", "tiles")]


def g_data():
    obj, unit = R.choice(DATA)
    sm, bg = R.randint(1, 4), R.randint(6, 10)
    who = P.next()[0]
    k = R.choice(["which", "big"])
    if not once((obj, sm, bg)) or not once((obj, k), 4):
        return None
    sv = ""
    for i, (lab, n) in enumerate([("small push", sm), ("big push", bg)]):
        y = 30 + i * 50
        sv += text(50, y + 5, lab, 12)
        for j in range(n):
            sv += "<rect x='%d' y='%d' width='20' height='20' fill='%s' stroke='%s' stroke-width='1'/>" % (100 + j * 24, y - 10, "#f6c431" if i else "#9fd0f0", INK)
    pic = svg_wrap(360, 110, sv, "small push: %d %s; big push: %d %s" % (sm, unit, bg, unit))
    if k == "which":
        return item(fig(pic) + "%s pushes a %s two times and counts %s. Which push made it go farther?" % (who, obj, unit), "the big push", ["the small push", "they went the same", "neither push"],
                    "%d is more than %d." % (bg, sm))
    return item(fig(pic) + "How many %s did %s's %s go with the big push?" % (unit, who, obj), str(bg), [str(sm), str(bg + 1), str(bg - 1)], "Count the yellow boxes: %d." % bg)


B1 = bank([
    ("What is a push?", "moving something away from you", ["moving something toward you", "looking at something", "singing to something"], "Pushes move things away."),
    ("What is a pull?", "moving something toward you", ["moving something away from you", "smelling something", "drawing something"], "Pulls move things closer."),
    ("You give a ball a big kick. What happens?", "It goes fast and far.", ["It stops.", "It goes slow.", "It gets bigger."], "Big push, big move."),
    ("You give a ball a tiny tap. What happens?", "It goes slow and not far.", ["It goes very far.", "It flies away.", "It gets smaller."], "Small push, small move."),
    ("A ball rolls to you. You push it back. What happens?", "It changes direction.", ["It keeps coming.", "It disappears.", "It turns blue."], "A push can change direction."),
    ("Can you push and pull a door?", "Yes. Push to close, pull to open, or the other way.", ["No, only push.", "No, only pull.", "Doors never move."], "Both can move it."),
    ("Which is a pull?", "opening a drawer", ["kicking a ball", "pushing a swing", "closing a door"], "The drawer comes toward you."),
    ("Which is a push?", "kicking a ball", ["pulling a wagon", "tugging a rope", "opening a drawer"], "The ball goes away."),
])
B5 = bank([
    ("Ava pushes a toy car softly. It goes 2 blocks. She pushes harder. How far might it go?", "more than 2 blocks", ["less than 2 blocks", "0 blocks", "exactly 2 blocks"], "Harder push, farther."),
    ("Leo wants a swing to go higher. What should he do?", "push harder", ["push softer", "stop pushing", "pull it down"], "Bigger push."),
    ("Mia and Kai pull a rope from opposite ends with the same strength. What happens?", "The rope does not move.", ["It goes to Mia.", "It goes to Kai.", "It breaks into two."], "Same pulls, no move."),
    ("Zoe rolls a ball. It goes too far. What should she try next time?", "a softer push", ["a harder push", "a pull from far away", "kick it"], "Less push, less far."),
    ("Sam wants to test pushes fairly. What should stay the same?", "the same ball and the same floor", ["a new ball each time", "a different floor each time", "nothing"], "Change only the push."),
])


def body():
    pic = "<div style='display:flex;gap:10px;flex-wrap:wrap'>%s%s</div>" % (push_svg("small", label="small push"), push_svg("big", label="big push"))
    ex = [("Open a drawer. Push or pull?", ["It comes to you."], "pull"),
          ("Big push or small push: which goes farther?", ["Big push, big move."], "big push")]
    mist = ["Thinking opening a drawer is a push.",
            "Thinking a soft push goes farther.",
            "Thinking a ball moves toward the hand that pushes it."]
    return kid_lesson(pic, "Pushes and pulls make things move.",
                      ["Big push: fast and far.", "Small push: slow and not far.", "Things move the way you push."], ex, mist)


def main():
    sets = U.sets([
        ("Push or pull?", B1 + [(g_pp, 12)]),
        ("Pushes and pulls all around", [(g_pp, 6), (g_strong, 8), (g_dir, 6)]),
        ("Big push, small push", [(g_strong, 12), (g_data, 5), (g_dir, 3)]),
        ("Which way?", [(g_dir, 3), (g_data, 9), (g_strong, 8)]),
        ("Push and pull scientists", B5 + [(g_data, 8), (g_strong, 7)]),
    ])
    make("kindergarten", "pushes-and-pulls", 1, "K-PS2-1",
         "Plan and conduct an investigation to compare the effects of different strengths or different directions of pushes and pulls on the motion of an object.",
         "Pushes and Pulls",
         "Kindergarten Pushes and Pulls Worksheets: Big Push, Small Push",
         "Pushes and Pulls",
         "Free kindergarten science worksheets on pushes and pulls (NGSS K-PS2-1): push or pull, big and small pushes, and which way things move. 100 picture questions with answers.",
         "Push away. Pull closer.",
         "A big push makes things go fast and far.",
         body(),
         [("What is the difference between a push and a pull?", "A push moves something away from you. A pull moves something toward you."),
          ("What does a bigger push do?", "It makes the object go faster and farther."),
          ("How can kids test this?", "Roll the same ball on the same floor with a small push and a big push, and count how far it goes.")],
         sets)


if __name__ == "__main__":
    main()
