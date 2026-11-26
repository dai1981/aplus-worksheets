# -*- coding: utf-8 -*-
"""
Food webs for the science units (Grade 5: energy in food, food webs, decomposers).
EATS[web][animal] = what the animal eats. Arrows in pictures point from the food to the eater
(the direction energy and matter move), the way NGSS models are drawn.
The diets are simplified but true (a hawk does eat snakes, mice and rabbits).
"""
import math
from ws_common import svg_wrap, text, line, INK
from sci_common import arrow, rect

WEBS = {
    "meadow": {"name": "meadow", "producers": ["grass", "wildflowers"],
               "eats": {"grasshopper": ["grass"], "rabbit": ["grass", "wildflowers"], "mouse": ["wildflowers", "grasshopper"],
                        "frog": ["grasshopper"], "snake": ["mouse", "frog"], "hawk": ["snake", "mouse", "rabbit"], "fox": ["rabbit", "mouse"]}},
    "pond": {"name": "pond", "producers": ["algae", "pondweed"],
             "eats": {"snail": ["algae", "pondweed"], "mosquito larva": ["algae"], "small fish": ["mosquito larva", "algae"],
                      "dragonfly": ["mosquito larva"], "frog": ["dragonfly", "snail"], "heron": ["frog", "small fish"], "turtle": ["snail", "pondweed"]}},
    "ocean": {"name": "ocean", "producers": ["phytoplankton", "seaweed"],
              "eats": {"krill": ["phytoplankton"], "sea urchin": ["seaweed"], "herring": ["krill"], "sea otter": ["sea urchin"],
                       "humpback whale": ["krill", "herring"], "seal": ["herring"], "orca": ["seal", "sea otter"]}},
    "forest": {"name": "forest", "producers": ["oak tree", "berry bush"],
               "eats": {"caterpillar": ["oak tree"], "deer": ["oak tree", "berry bush"], "squirrel": ["oak tree"], "robin": ["caterpillar", "berry bush"],
                        "owl": ["squirrel", "robin"], "wolf": ["deer"], "bear": ["berry bush", "deer"]}},
    "desert": {"name": "desert", "producers": ["cactus", "desert grass"],
               "eats": {"beetle": ["desert grass"], "kangaroo rat": ["desert grass"], "jackrabbit": ["desert grass", "cactus"], "lizard": ["beetle"],
                        "rattlesnake": ["kangaroo rat", "lizard"], "hawk": ["rattlesnake", "jackrabbit"], "coyote": ["jackrabbit", "kangaroo rat", "cactus"]}},
}
PLANTS = {"grass", "wildflowers", "algae", "pondweed", "phytoplankton", "seaweed", "oak tree", "berry bush", "cactus", "desert grass"}
ART = {"algae": "", "phytoplankton": "", "krill": "", "seaweed": "", "pondweed": "", "grass": "", "wildflowers": "", "desert grass": ""}


def a(x):
    """with an article: 'a hawk', 'an owl', 'grass' (mass nouns stay bare)."""
    if x in ART:
        return x
    return ("an " if x[0] in "aeiou" else "a ") + x


PLURAL = {"grass": "grass", "wildflowers": "wildflowers", "algae": "algae", "pondweed": "pondweed", "phytoplankton": "phytoplankton", "seaweed": "seaweed",
          "krill": "krill", "herring": "herring", "deer": "deer", "mouse": "mice", "mosquito larva": "mosquito larvae", "small fish": "small fish",
          "berry bush": "berry bushes", "cactus": "cactuses", "desert grass": "desert grass", "sea urchin": "sea urchins", "sea otter": "sea otters",
          "humpback whale": "humpback whales", "kangaroo rat": "kangaroo rats", "oak tree": "oak trees", "jackrabbit": "jackrabbits", "fox": "foxes",
          "wolf": "wolves", "butterfly": "butterflies"}


def plural(x):
    return PLURAL.get(x, x + "s")


def organisms(w):
    W = WEBS[w]
    return W["producers"] + list(W["eats"])


def eaters_of(w, x):
    return [k for k, v in WEBS[w]["eats"].items() if x in v]


def diet(w, x):
    return WEBS[w]["eats"].get(x, [])


def kind(w, x):
    if x in WEBS[w]["producers"]:
        return "producer"
    d = diet(w, x)
    pl = [f for f in d if f in PLANTS]
    if len(pl) == len(d):
        return "herbivore"
    if not pl:
        return "carnivore"
    return "omnivore"


def level(w, x, memo=None):
    if x in WEBS[w]["producers"]:
        return 0
    return 1 + max(level(w, f) for f in diet(w, x))


def chains(w):
    """every food chain from a producer to a top consumer (nothing eats it)."""
    out = []

    def go(path):
        last = path[-1]
        nxt = eaters_of(w, last)
        if not nxt:
            out.append(list(path))
        for n in nxt:
            go(path + [n])
    for p in WEBS[w]["producers"]:
        go([p])
    return out


# hand-placed (x from 0 to 1, row from the bottom) so arrows cross as little as possible
LAYOUT = {
    "meadow": {"grass": (.2, 0), "wildflowers": (.72, 0), "grasshopper": (.13, 1), "rabbit": (.86, 1), "frog": (.1, 2), "mouse": (.5, 2),
               "snake": (.3, 3), "fox": (.82, 3), "hawk": (.55, 4)},
    "pond": {"algae": (.25, 0), "pondweed": (.75, 0), "snail": (.2, 1), "mosquito larva": (.65, 1), "turtle": (.08, 2), "small fish": (.5, 2),
             "dragonfly": (.88, 2), "frog": (.42, 3), "heron": (.7, 4)},
    "ocean": {"phytoplankton": (.2, 0), "seaweed": (.8, 0), "krill": (.2, 1), "sea urchin": (.8, 1), "herring": (.38, 2), "sea otter": (.8, 2),
              "humpback whale": (.13, 3), "seal": (.5, 3), "orca": (.72, 4)},
    "forest": {"oak tree": (.25, 0), "berry bush": (.75, 0), "caterpillar": (.1, 1), "squirrel": (.33, 1), "deer": (.75, 1), "robin": (.18, 2),
               "wolf": (.62, 2), "bear": (.9, 2), "owl": (.32, 3)},
    "desert": {"cactus": (.2, 0), "desert grass": (.7, 0), "jackrabbit": (.38, 1), "kangaroo rat": (.64, 1), "beetle": (.9, 1), "coyote": (.13, 2),
               "lizard": (.88, 2), "rattlesnake": (.62, 3), "hawk": (.4, 4)},
}


def _clip(x1, y1, x2, y2, hw, hh):
    """point where the line from (x1, y1) to the centre (x2, y2) meets a box of half-size hw x hh around (x2, y2)."""
    dx, dy = x1 - x2, y1 - y2
    t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return x2 + dx * t, y2 + dy * t


def picture(w, hide=(), label=None):
    """Food web drawing, producers at the bottom, arrows from food to eater (ending at the eater's box)."""
    orgs = [x for x in organisms(w) if x not in hide]
    lay = LAYOUT[w]
    nl = max(r for _, r in lay.values()) + 1
    W, rh = 480, 64
    H = nl * rh + 6
    pos = {x: (16 + (W - 32) * lay[x][0], H - 22 - lay[x][1] * rh) for x in orgs}
    half = {x: (3.6 * len(x) + 8, 12) for x in orgs}
    s = []
    for x in orgs:
        for f in diet(w, x):
            if f in pos:
                (x1, y1), (x2, y2) = pos[f], pos[x]
                sx, sy = _clip(x2, y2, x1, y1, half[f][0] + 2, half[f][1] + 2)
                ex, ey = _clip(x1, y1, x2, y2, half[x][0] + 3, half[x][1] + 3)
                s.append(arrow(sx, sy, ex, ey, "#4d4d4d", 1.8, 10))
    for x, (px, py) in pos.items():
        hw, hh = half[x]
        col = "#e3f1df" if x in PLANTS else "#fdf0dc"
        s.append(rect(px - hw, py - hh, 2 * hw, 2 * hh, col, INK, 1.5, 6))
        s.append(text(px, py + 5, x, 13))
    return svg_wrap(W, H, "".join(s), label or ("food web of a " + WEBS[w]["name"])).replace("<svg ", "<svg data-pf='lg' ", 1)


def chain_picture(ch, label="food chain"):
    W = 120 * len(ch)
    s = []
    for i, x in enumerate(ch):
        cx = 60 + i * 120
        tw = 7.2 * len(x) + 14
        s.append(rect(cx - tw / 2, 14, tw, 26, "#e3f1df" if x in PLANTS else "#fdf0dc", INK, 1.5, 6))
        s.append(text(cx, 32, x, 13))
        if i:
            s.append(arrow(cx - 120 + 7.2 * len(ch[i - 1]) / 2 + 10, 27, cx - tw / 2 - 3, 27, "#7a7a7a", 2, 8))
    return svg_wrap(W, 54, "".join(s), label)
