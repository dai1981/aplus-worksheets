# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Teen Numbers - Ten and Some Ones (K.NBT.A.1)
  python3 tools/gen_us_math_gk_teen_numbers_tens_and_ones.py
Numbers 11 to 19 are ten ones and some more ones: ten-frames, a rod of 10 and single cubes,
number sentences like 14 = 10 + 4, and short stories with packs of 10.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, tenframe_svg, rods_svg, cards_svg, KINDS
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
WORDS = {11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
         17: "seventeen", 18: "eighteen", 19: "nineteen"}


def rev(n):
    s = str(n)
    return int(s[::-1]) if s[0] != s[1] else None


def ones_w(n):
    o = n - 10
    return [o + 1, o - 1, n, 10, o + 2]


def teen_w(n):
    o = n - 10
    return [rev(n), int("10%d" % o), o, n + 1, n - 1]


def pic(n, how, kind="dot"):
    if how == "frame":
        return tenframe_svg(n, frames=2, kind=kind)
    return rods_svg(1, n - 10)


# ============================================================ set 1: 10 and how many more?
def set_more(rnd, K):
    its = []
    for n, how in [(11, "frame"), (13, "frame"), (12, "rods"), (15, "frame"), (14, "rods"), (16, "frame"),
                   (17, "rods"), (12, "frame"), (18, "frame"), (13, "rods"), (19, "frame"), (16, "rods"),
                   (14, "frame"), (11, "rods"), (17, "frame"), (18, "rods"), (19, "rods"), (15, "rods")]:
        o = n - 10
        q = "%d is 10 and how many more?" % n
        e = ("There is one full ten. Count the rest: %s. %d is 10 and <b>%d</b> more."
             % (", ".join(str(k) for k in range(1, o + 1)), n, o))
        its.append(mcq(fig(pic(n, how)) + q, o, ones_w(n), e))
    for n in [16, 13]:
        o = n - 10
        q = fig(cards_svg([str(n)], w=64, h=64)) + "%s is 10 and how many more?" % WORDS[n].capitalize()
        e = "The 1 in %d means 1 ten. The %d means %d ones. So %d is 10 and <b>%d</b> more." % (n, o, o, n, o)
        its.append(mcq(q, o, ones_w(n), e))
    return {"title": "10 and how many more?", "items": its}


# ============================================================ set 2: find the teen number
def set_teen(rnd, K):
    its = []
    for n, how in [(11, "rods"), (14, "frame"), (12, "rods"), (13, "frame"), (15, "rods"), (16, "frame"),
                   (17, "rods"), (18, "frame"), (19, "rods"), (12, "frame"), (14, "rods"), (11, "frame"),
                   (16, "rods"), (15, "frame"), (18, "rods"), (17, "frame"), (13, "rods"), (19, "frame")]:
        o = n - 10
        q = "10 and %d more. What number is it?" % o
        e = "10 and %d more is %s. We write <b>%d</b>: a 1 for the ten, then %d." % (o, WORDS[n], n, o)
        its.append(mcq(fig(pic(n, how)) + q, n, teen_w(n), e))
    for o in [5, 8]:
        n = 10 + o
        q = fig(cards_svg(["10", "+", str(o), "=", "?"], w=46)) + "What number is 10 and %d?" % o
        e = "10 and %d make %d. Write <b>%d</b>, not %d." % (o, n, n, int("10%d" % o))
        its.append(mcq(q, n, teen_w(n), e))
    return {"title": "Find the teen number", "items": its}


# ============================================================ set 3: number sentences
def set_sentences(rnd, K):
    its = []
    for n, how in [(12, "frame"), (15, "rods"), (17, "frame"), (11, "rods"), (19, "frame"), (14, "rods"),
                   (16, "frame"), (13, "rods"), (18, "frame"), (11, "frame")]:
        o = n - 10
        q = fig(pic(n, how)) + "%d = 10 + ?" % n
        e = "%d is 10 and %d. So %d = 10 + <b>%d</b>." % (n, o, n, o)
        its.append(mcq(q, o, ones_w(n), e))
    for n, how in [(13, "frame"), (16, "rods"), (18, "rods"), (12, "rods"), (14, "frame"), (17, "rods"),
                   (19, "rods"), (15, "frame"), (12, "frame"), (16, "frame")]:
        o = n - 10
        q = fig(pic(n, how)) + "10 + %d = ?" % o
        e = "10 and %d more make %d. 10 + %d = <b>%d</b>." % (o, n, o, n)
        its.append(mcq(q, n, teen_w(n), e))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14],
             o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Number sentences", "items": order}


# ============================================================ set 4: which matches?
def set_match(rnd, K):
    its = []
    plan = [(14, "frame"), (11, "rods"), (17, "frame"), (13, "rods"), (19, "frame"), (16, "rods"), (12, "frame"),
            (18, "rods"), (15, "frame"), (14, "rods"), (11, "frame"), (17, "rods"), (13, "frame"), (19, "rods"),
            (16, "frame"), (12, "rods"), (18, "frame"), (15, "rods")]
    for i, (n, how) in enumerate(plan):
        o = n - 10
        right = "%d = 10 + %d" % (n, o)
        wr = ["%d = 10 + %d" % (n, o + 1) if o < 9 else "%d = 10 + %d" % (n, o - 2),
              "%d = 10 + %d" % (n, o - 1) if o > 1 else "%d = 10 + %d" % (n, o + 2),
              "%d = 1 + %d" % (n, o),
              "%d = 10 + %d" % (n, n)]
        if i % 2:
            right = "10 + %d = %d" % (o, n)
            wr = ["10 + %d = %d" % (o, rev(n)) if rev(n) else "10 + %d = %d" % (o, n + 1),
                  "10 + %d = %d" % (o, int("10%d" % o)),
                  "10 + %d = %d" % (o, n + 1) if rev(n) else "10 + %d = %d" % (o, n - 1),
                  "10 + %d = %d" % (o + 1, n)]
        q = fig(pic(n, how)) + "Which number sentence matches the picture?"
        e = "The picture shows 10 and %d more. That is %d. So <b>%s</b>." % (o, n, right)
        its.append(mcq(q, right, wr, e))
    for n in [15, 18]:
        o = n - 10
        q = fig(cards_svg([str(n)], w=64, h=64)) + "Which shows %s?" % WORDS[n]
        right = "1 ten and %d ones" % o
        wr = ["%d tens and 1 one" % o, "1 ten and %d ones" % n, "1 ten and %d ones" % (o + 1)]
        e = "%d is 10 ones and %d more ones. That is <b>%s</b>." % (n, o, right)
        its.append(mcq(q, right, wr, e))
    return {"title": "Which matches?", "items": its}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def story(n, kind, text, ask="total", unit=None):
        p = K.next()
        o = n - 10
        t = text.format(o=o, n_=n, **p)
        one, many = unit or (name(kind, 1), name(kind))
        u = lambda v: "%d %s" % (v, one if v == 1 else many)
        svg = tenframe_svg(n, frames=2, kind=kind) if kind != "cube" else rods_svg(1, o)
        if ask == "total":
            e = "10 and %d more make %d. 10 + %d = %d. The answer is <b>%s</b>." % (o, n, o, n, u(n))
            its.append(mcq(fig(svg) + t, u(n), [u(w) for w in teen_w(n) if w], e))
        else:
            e = "%d is 10 and %d more. %d = 10 + %d. The answer is <b>%s</b>." % (n, o, n, o, u(o))
            its.append(mcq(fig(svg) + t, u(o), [u(w) for w in ones_w(n) if w], e))

    story(12, "apple", "A box holds 10 apples. {n} has 1 full box and {o} more apples. How many apples?")
    story(13, "cube", "{n} has a rod of 10 cubes and {o} more cubes. How many cubes?")
    story(15, "star", "{n} has 10 stars on one card and {o} on another. How many stars in all?")
    story(11, "cup", "There are 10 cups in a stack and {o} more. How many cups?")
    story(14, "ball", "{n} has 14 balls. 10 are in a bag. How many are not in the bag?", ask="ones")
    story(16, "flower", "{n} picks 10 flowers and then {o} more. How many flowers?")
    story(17, "cube", "A tower has 17 cubes. 10 are blue. The rest are yellow. How many are yellow?", ask="ones")
    story(18, "fish", "A tank has 10 fish. {n} adds {o} more. How many fish now?")
    story(13, "duck", "There are 13 ducks. 10 swim. The rest walk. How many walk?", ask="ones")
    story(19, "heart", "{n} draws 10 hearts and {o} more. How many hearts?")
    story(15, "button", "{n} has 15 buttons. 10 fit on a card. How many are left over?", ask="ones")
    story(14, "bug", "{n} sees 10 ladybugs on a leaf and {o} on a rock. How many ladybugs?")
    story(17, "apple", "{n} picks 17 apples. 10 go in a box. How many are not in the box?", ask="ones")
    story(12, "cube", "{n} has 12 cubes. {He} makes a rod of 10. How many cubes are left?", ask="ones")
    story(16, "star", "{n} has 16 stickers. 10 fit on a page. How many go on the next page?", ask="ones",
          unit=("sticker", "stickers"))
    story(19, "cup", "There are 19 cups. 10 are on a tray. How many are not on the tray?", ask="ones")
    story(11, "ball", "{n} has 10 balls in a bag and {o} more. How many balls?")
    story(18, "flower", "There are 18 flowers. 10 are in a vase. How many are not in the vase?", ask="ones")
    story(15, "cube", "{n} has a rod of 10 cubes and {o} more cubes. How many cubes?")
    story(13, "heart", "{n} cuts out 10 hearts and {o} more. How many hearts?")
    return {"title": "Packs of 10 stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Teen numbers are 10 and some more</h2>"
        "<p>Every number from 11 to 19 is <b>ten ones and some more ones</b>.</p>"
        "<figure class='sn-fig'>" + tenframe_svg(14) + "<figcaption>10 and 4 more is 14.</figcaption></figure>"
        "<figure class='sn-fig'>" + rods_svg(1, 4) + "<figcaption>A rod of 10 and 4 cubes is 14.</figcaption></figure>"
        + table(["Number", "10 and …", "Sentence"], [
            ["11", "10 and 1", "11 = 10 + 1"], ["13", "10 and 3", "13 = 10 + 3"], ["15", "10 and 5", "15 = 10 + 5"],
            ["17", "10 and 7", "17 = 10 + 7"], ["19", "10 and 9", "19 = 10 + 9"],
        ]) +
        "<h2>What the digits mean</h2>"
        "<p>In 16, the <b>1</b> means 1 ten. The <b>6</b> means 6 ones.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Writing 61 for 10 and 6", "The 1 for the ten comes first: 16"],
            ["Writing 106 for 10 and 6", "Teen numbers have only 2 digits"],
            ["Saying 16 is 10 and 16 more", "16 is 10 and 6 more"],
        ])
    )


FAQ = [
    {"q": "What are teen numbers?",
     "a": "Teen numbers are 11 to 19. Each one is 10 and some more ones. For example, 15 is 10 and 5."},
    {"q": "Why do kindergartners learn 10 and some ones?",
     "a": "It is the first step to place value. Seeing 14 as 10 and 4 helps children understand tens and ones in Grade 1."},
    {"q": "Why does my child write 41 for fourteen?",
     "a": "We say the 4 first in 'fourteen'. Show 14 as a full ten-frame and 4 more, then point to the 1 for the ten and the 4 for the ones."},
    {"q": "How can I practice teen numbers at home?",
     "a": "Use an egg carton with 10 cups or bundle 10 straws with a rubber band. Add a few loose ones and ask: 10 and how many more? What number is that?"},
]


def gen():
    rnd = random.Random(2010)
    K = Kids(rnd)
    sets = [set_more(rnd, K), set_teen(rnd, K), set_sentences(rnd, K), set_match(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=20, extra_ok=(21, 31, 41, 51, 61, 71, 81, 91) + tuple(range(101, 110)))
    return {
        "slug": "teen-numbers-tens-and-ones", "sort": 10, "updated": UPDATED, "pdf_url": "",
        "title": "Teen Numbers: Ten and Some Ones",
        "seo_title": "Kindergarten Teen Numbers Worksheets: 11 to 19 as Ten and Some Ones",
        "short_title": "Teen Numbers",
        "domain": "Number and Operations in Base Ten",
        "standard_code": "K.NBT.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/NBT/A/1/",
        "standard_text": "Compose and decompose numbers from 11 to 19 into ten ones and some further ones, e.g., by using "
                         "objects or drawings, and record each composition or decomposition by a drawing or equation "
                         "(e.g., 18 = 10 + 8); understand that these numbers are composed of ten ones and one, two, "
                         "three, four, five, six, seven, eight, or nine ones.",
        "meta_desc": "Free kindergarten teen numbers worksheets: see 11 to 19 as 10 and some more with ten-frames and "
                     "cubes, write sentences like 14 = 10 + 4, and solve packs-of-10 stories. 100 picture questions "
                     "with an answer key.",
        "key_big": "Every teen number is 10 and some more: 14 = 10 + 4.",
        "key_sub": "In 14, the 1 means 1 ten and the 4 means 4 ones.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
