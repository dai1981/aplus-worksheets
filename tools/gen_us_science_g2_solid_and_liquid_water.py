# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Solid and Liquid Water on Earth (2-ESS2-3)
  python tools/gen_us_science_g2_solid_and_liquid_water.py
Obtain information to identify where water is found on Earth and that it can be solid or liquid.
Liquid water: oceans, lakes, rivers, ponds, rain, under the ground. Solid water: ice, snow, glaciers, icebergs, ice caps.
Most of Earth's water is in the ocean and is salty; most fresh water is frozen.
Wrong answers come from real mistakes: "snow is not water", "most water is in lakes", "ocean water is good to drink".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, bar_chart, svg_wrap, People
from ws_common import text
import sci_kids as K

U = Unit(20111)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# name, state, picture
THINGS = [("the water in an ocean", "liquid", None), ("a glacier", "solid", None), ("an iceberg", "solid", None), ("snow on a mountain top", "solid", "snow"),
          ("an ice cube", "solid", "ice"), ("rain", "liquid", "rain"), ("a puddle on a warm day", "liquid", "puddle"), ("a river", "liquid", None),
          ("a frozen pond in winter", "solid", None), ("a lake in summer", "liquid", None), ("an icicle", "solid", None), ("a raindrop", "liquid", "drop"),
          ("water deep under the ground", "liquid", None), ("hail", "solid", None), ("frost on a window", "solid", None), ("a waterfall", "liquid", None),
          ("the ice at the North Pole", "solid", None), ("a snowflake", "solid", "snow")]


def g_state():
    n, st, pic = R.choice(THINGS)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((n, t)):
        return None
    fg = fig(K.card(pic)) if pic else ""
    if t:
        return item(fg + "%s looks at %s. Is this water solid or liquid?" % (who, n), st, ["liquid" if st == "solid" else "solid", "It is not water.", "It is a gas you can see."],
                    "%s is %s water." % (n[0].upper() + n[1:], st))
    good = "It is %s, so it %s." % (st, "keeps its own shape" if st == "solid" else "flows")
    return item(fg + "How does %s know %s is %s water?" % (who, n, st), good,
                ["It is %s, so it %s." % ("liquid" if st == "solid" else "solid", "flows" if st == "solid" else "keeps its own shape"),
                 "It is blue.", "It is cold, so it is not water."], "Solids keep their shape. Liquids flow.")


def g_pick():
    sol = ["ice", "snow"]
    liq = ["drop", "rain", "puddle"]
    q = R.choice(["solid", "liquid"])
    if q == "solid":
        a = R.choice(sol)
        others = R.sample(liq, 2) + [R.choice(["sun", "rock", "leaf"])]
    else:
        a = R.choice(liq)
        others = [R.choice(sol)] + R.sample(["ice", "snow", "rock", "sun", "leaf"], 2)
        others = list(dict.fromkeys(others))
        if len(others) < 3:
            return None
    kinds = [a] + others[:3]
    R.shuffle(kinds)
    if len(set(kinds)) < 4 or not once(("p", tuple(kinds), q)):
        return None
    L = "ABCD"
    who = P.next()[0]
    NM = {"drop": "drop", "ice": "ice cube", "snow": "snow", "rain": "rain", "puddle": "puddle", "sun": "sun", "rock": "rock", "leaf": "leaf"}
    AR = {"drop": "A drop of water", "ice": "An ice cube", "snow": "Snow", "rain": "Rain", "puddle": "A puddle"}
    pic = K.row(kinds, words=["%s. %s" % (L[i], NM[k]) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s looks at these pictures. Which one shows %s water?" % (who, q), "%s (%s)" % (L[kinds.index(a)], NM[a]),
                ["%s (%s)" % (L[i], NM[k]) for i, k in enumerate(kinds) if k != a], "%s is %s water." % (AR[a], q))


WHERE = [("Where is water frozen all year long?", "near the North and South Poles", ["in a warm lake", "in a pond in summer", "in a river in a hot place"], "It is very cold there."),
         ("Where can you find snow even in summer?", "on the tops of very tall mountains", ["on a sunny beach", "in a warm valley", "in a desert"], "High mountains stay cold."),
         ("Where is most of Earth's water?", "in the oceans", ["in lakes", "in rivers", "in clouds"], "Oceans hold almost all of it."),
         ("Where is most of Earth's fresh water?", "frozen in ice and glaciers", ["in the oceans", "in puddles", "in clouds"], "Most fresh water is ice."),
         ("Where does liquid water hide under our feet?", "in soil and rocks underground", ["inside the sun", "in the air only", "nowhere"], "Groundwater fills spaces in rock."),
         ("Where does river water go?", "downhill to a lake or the ocean", ["uphill to the mountains", "into the sky as rocks", "nowhere"], "Rivers flow downhill."),
         ("What is a glacier?", "a huge, slow river of ice on land", ["a big lake", "a type of cloud", "a warm river"], "Glaciers are solid water."),
         ("What is an iceberg?", "a big piece of ice floating in the ocean", ["a mountain of rock", "a sandy island", "a warm lake"], "It broke off a glacier.")]


def g_where():
    q, a, w, e = R.choice(WHERE)
    who = P.next()[0]
    if not once(q):
        return None
    return item("%s asks: %s" % (who, q), a, w, e)


def g_chart():
    who = P.next()[0]
    k = R.choice(["most", "ice", "least", "drink"])
    if not once(("c", k)):
        return None
    vals = [97, 2, 1]
    labs = ["ocean", "ice", "lakes, rivers"]
    ch = bar_chart(labs, vals, "cups out of 100", "bar graph: out of 100 cups of Earth's water, 97 are ocean, 2 are ice and 1 is in lakes, rivers and underground", ymax=100, step=20, w=330)
    if k == "most":
        return item(fig(ch) + "%s's book shows Earth's water as 100 cups. Where is the most water?" % who, "ocean", ["ice", "lakes, rivers", "They are the same."], "97 of 100 cups are ocean water.")
    if k == "ice":
        return item(fig(ch) + "%s's book shows Earth's water as 100 cups. How many cups are frozen ice?" % who, "2", ["97", "1", "100"], "The ice bar shows 2.")
    if k == "least":
        return item(fig(ch) + "%s's book shows Earth's water as 100 cups. Which part has the least?" % who, "lakes, rivers", ["ocean", "ice", "They are the same."], "Only 1 cup.")
    return item(fig(ch) + "%s's book shows Earth's water as 100 cups. Ocean water is salty. Which cups could people drink after cleaning?" % who, "lakes, rivers", ["ocean", "all 100 cups", "none of them"],
                "Fresh water in lakes and rivers is only a tiny part.")


def season_svg(froze):
    s = K.icon("snow" if froze else "sun", 60, 40, 0.7)
    s += "<ellipse cx='150' cy='90' rx='90' ry='28' fill='%s' stroke='#5aa6d6' stroke-width='2'/>" % ("#e8f6ff" if froze else "#9fd0f0")
    if froze:
        s += "<path d='M100 84 l20 8 l18 -6 M160 96 l20 -6 l16 6' stroke='#9cc' stroke-width='1.5' fill='none'/>"
    return svg_wrap(300, 130, s, "a pond in winter, frozen" if froze else "a pond in summer, liquid")


def g_season():
    who = P.next()[0]
    froze = R.random() < 0.5
    k = R.choice(["state", "why", "next"])
    if not once(("s", froze, k)):
        return None
    pic = fig(season_svg(froze))
    if k == "state":
        return item(pic + "%s sees this pond. Is the water on top solid or liquid?" % who, "solid" if froze else "liquid", ["liquid" if froze else "solid", "It is not water.", "It is sand."],
                    "Cold freezes water; warm weather keeps it liquid.")
    if k == "why":
        return item(pic + "Why is the pond %s %s?" % ("frozen in" if froze else "liquid in", "winter" if froze else "summer") + (" %s wonders." % who),
                    "The air is cold enough to freeze water." if froze else "The air is warm, so the ice melted.",
                    ["The water turned into sand.", "Fish froze it.", "The sun is hotter in winter."] if froze else ["The water turned into rock.", "Snow made it warm.", "It is always frozen."],
                    "Temperature changes water.")
    return item(pic + "%s asks: what will happen to this pond when %s comes?" % (who, "spring" if froze else "winter"), "It will melt." if froze else "It may freeze.",
                ["It will freeze harder." if froze else "It will turn into steam.", "It will disappear.", "It will turn into sand."], "Warming melts ice; cooling freezes water.")


B1 = bank([
    ("Which is solid water?", "ice", ["rain", "a river", "a puddle"], "Ice keeps its shape."),
    ("Which is liquid water?", "a lake", ["a glacier", "snow", "an icicle"], "Liquids flow."),
    ("Is snow made of water?", "Yes, it is frozen water.", ["No, it is made of salt.", "No, it is made of clouds only.", "No, it is sand."], "Snow melts into water."),
    ("Is ocean water salty or fresh?", "salty", ["fresh", "sweet", "frozen"], "We cannot drink ocean water."),
    ("What are the two forms of water in this unit?", "solid and liquid", ["hot and cold only", "big and small", "red and blue"], "Ice is solid; water in a lake is liquid."),
    ("Which body of water holds the most water?", "the ocean", ["a pond", "a lake", "a river"], "Oceans are huge."),
    ("What happens to snow when it gets warm?", "It melts into liquid water.", ["It turns into rock.", "It gets bigger.", "It turns into sand."], "Warming melts solid water."),
    ("Where can you find solid water?", "glaciers and ice caps", ["oceans in warm places", "rivers in summer", "rain clouds only"], "Ice is solid."),
])
B5 = bank([
    ("Ava reads that 97 of every 100 cups of water on Earth are in the ocean. How many cups are not ocean water?", "3", ["97", "100", "7"], "100 − 97 = 3."),
    ("Leo sees an icicle drip on a sunny day. What is happening?", "Solid water is melting into liquid.", ["Liquid water is freezing.", "The ice is turning into rock.", "Nothing is changing."], "Sun warms the ice."),
    ("Mia wants to find out where water is on Earth. Which sources should she use?", "books, maps and globes", ["only guessing", "a toy car", "a song"], "Find information."),
    ("A globe shows a lot of blue. What does the blue show?", "water, mostly oceans", ["land", "mountains", "deserts"], "Most of Earth is covered by water."),
    ("Kai says, “Snow and rain are different things, so snow is not water.” What is wrong?", "Snow is solid water; rain is liquid water.", ["Nothing is wrong.", "Rain is not water.", "Snow is made of sugar."], "Both are water."),
])


def body():
    pic = K.row(["ice", "snow", "drop", "puddle"], words=["solid", "solid", "liquid", "liquid"], size=95)
    ex = [("Is a glacier solid or liquid?", ["It is ice."], "solid"),
          ("Where is most of Earth's water?", ["Oceans are huge."], "in the oceans")]
    mist = ["Thinking snow and ice are not water.",
            "Thinking most water is in lakes and rivers. Most is in the ocean.",
            "Thinking ocean water is good to drink. It is salty."]
    return kid_lesson(pic, "Water is all over Earth.",
                      ["Liquid: oceans, lakes, rivers, rain.", "Solid: ice, snow, glaciers.", "Most water is in the salty ocean."], ex, mist)


def main():
    sets = U.sets([
        ("Solid or liquid?", B1 + [(g_state, 6), (g_pick, 6)]),
        ("Water on Earth", [(g_state, 12), (g_where, 8)]),
        ("Looking at pictures", [(g_pick, 12), (g_season, 3), (g_state, 5)]),
        ("Where is the water?", [(g_chart, 2), (g_season, 2), (g_state, 8), (g_pick, 8)]),
        ("Water detectives", B5 + [(g_chart, 2), (g_season, 1), (g_pick, 7)]),
    ])
    make("grade-2", "solid-and-liquid-water", 11, "2-ESS2-3",
         "Obtain information to identify where water is found on Earth and that it can be solid or liquid.",
         "Solid and Liquid Water on Earth",
         "Grade 2 Water on Earth Worksheets: Solid and Liquid Water, Oceans and Glaciers",
         "Water on Earth",
         "Free grade 2 science worksheets on water on Earth (NGSS 2-ESS2-3): solid and liquid water, oceans, lakes, rivers, glaciers and snow. 100 picture questions with answers.",
         "Water can be solid or liquid.",
         "Ice and snow are solid. Oceans, lakes and rain are liquid.",
         body(),
         [("Where is water found on Earth?", "In oceans, lakes, rivers, ponds and under the ground as liquid, and in glaciers, ice caps and snow as solid."),
          ("Where is most of Earth's water?", "In the oceans. Ocean water is salty, so we cannot drink it."),
          ("Is snow water?", "Yes. Snow is solid water. It melts into liquid water when it gets warm.")],
         sets)


if __name__ == "__main__":
    main()
