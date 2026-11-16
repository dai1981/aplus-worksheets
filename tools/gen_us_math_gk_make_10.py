# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Make 10 (K.OA.A.4)
  python3 tools/gen_us_math_gk_make_10.py
For any number from 1 to 9, find the number that makes 10: fill a ten-frame, find the missing part,
find how many are hidden in a box, pick the pairs that make 10, and solve "how many more" stories.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, tenframe_svg, tenframe_mix_svg, box_svg, two_groups_svg, KINDS
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
PAIRS = "1 and 9, 2 and 8, 3 and 7, 4 and 6, 5 and 5"


def wrongs(n):
    m = 10 - n
    return [m + 1, m - 1, n if n != m else None, 10, m + 2, m - 2]


def fill_e(n, what="dots"):
    m = 10 - n
    return ("There are %d %s. Count the empty boxes: %s. %d and %d make 10, so <b>%d</b> more."
            % (n, what, ", ".join(str(k) for k in range(1, m + 1)), n, m, m))


# ============================================================ set 1: fill the ten-frame
def set_fill(rnd, K):
    plan = [9, 8, 5, 7, 6, 9, 4, 8, 3, 7, 6, 2, 5, 1, 4, 3, 8, 2, 6, 1]
    kinds = ["dot", "apple", "star", "ball", "button", "fish", "flower", "heart", "duck", "cup", "bug"]
    its = []
    for i, n in enumerate(plan):
        kind = kinds[i % len(kinds)]
        svg = tenframe_svg(n, frames=1, kind=kind)
        q = "How many more %s will fill the ten-frame?" % name(kind)
        its.append(mcq(fig(svg) + q, 10 - n, wrongs(n), fill_e(n, name(kind, n))))
    return {"title": "Fill the ten-frame", "items": its}


# ============================================================ set 2: missing part
def set_missing(rnd, K):
    plan = [9, 8, 7, 5, 6, 4, 3, 2, 1, 8, 6, 7, 4, 3, 9, 5, 2, 1, 7, 3]
    its = []
    for i, n in enumerate(plan):
        m = 10 - n
        svg = tenframe_mix_svg(["r"] * n + [""] * m)
        seen_n = plan[:i].count(n)
        q = ["%d + ? = 10", "? + %d = 10", "10 = %d + ?"][seen_n] % n
        e = "%d and %d make 10. %s. The missing number is <b>%d</b>." % (
            n, m, ("%d + %d = 10" % (m, n)) if q.startswith("?") else ("%d + %d = 10" % (n, m)), m)
        its.append(mcq(fig(svg) + "Use the ten-frame. " + q, m, wrongs(n), e))
    return {"title": "Find the missing part", "items": its}


# ============================================================ set 3: hidden in a box
def set_box(rnd, K):
    plan = [8, 9, 7, 5, 6, 4, 9, 3, 8, 6, 2, 7, 5, 4, 1, 3, 6, 2, 7, 1]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    its = []
    for i, n in enumerate(plan):
        kind = kinds[i % len(kinds)]
        m = 10 - n
        svg = box_svg(n, kind)
        q = "There are 10 %s in all. Some are in the box. How many are in the box?" % name(kind)
        e = ("You can see %d. Count on to 10: %s. That is %d more. %d + %d = 10, so <b>%d</b> %s in the box."
             % (n, ", ".join(str(k) for k in range(n + 1, 11)), m, n, m, m, "is" if m == 1 else "are"))
        its.append(mcq(fig(svg) + q, m, wrongs(n), e))
    return {"title": "How many are in the box?", "items": its}


# ============================================================ set 4: pairs that make 10
def set_pairs(rnd, K):
    its = []
    for a in [7, 4, 8, 6, 9, 5, 3, 2, 1, 6]:
        b = 10 - a
        cells = ["r"] * a + ["b"] * b
        svg = tenframe_mix_svg(cells)
        if a == 6 and any("6 + 4 = 10" in x["c"][0] for x in its):
            svg = two_groups_svg(a, "apple", b, "cup", word="+")
        right = "%d + %d = 10" % (a, b)
        wr = ["%d + %d = 10" % (x, y) for x, y in [(a, b - 1), (a, b + 1), (a - 1, b), (a + 1, b), (a - 1, b - 1), (a - 2, b), (a, b + 2), (a, b - 2), (a + 2, b)]
              if 1 <= x <= 9 and 1 <= y <= 9]
        if "apple" in svg:
            e = "%d apples and %d cups make 10 in all. <b>%s</b>." % (a, b, right)
            its.append(mcq(fig(svg) + "Which number sentence matches the picture?", right, wr, e))
        else:
            e = "%d red and %d blue fill the ten-frame. <b>%s</b>." % (a, b, right)
            its.append(mcq(fig(svg) + "Which number sentence matches the ten-frame?", right, wr, e))
    for n in [3, 6, 8, 2, 7]:
        m = 10 - n
        right = "%d and %d" % (n, m)
        wr = ["%d and %d" % (n, m - 1), "%d and %d" % (n, m + 1), "%d and %d" % (n, n) if n != m else "%d and %d" % (n, m - 2)]
        q = "Which pair makes 10?"
        e = "%d + %d = 10. Pairs that make 10: %s. The answer is <b>%s</b>." % (n, m, PAIRS, right)
        its.append(mcq(fig(tenframe_svg(0)) + q, right, wr, e))
    for n in [4, 9, 1, 5, 7]:
        m = 10 - n
        q = "Which number goes with %d to make 10?" % n
        e = "%d + %d = 10. So <b>%d</b> goes with %d." % (n, m, m, n)
        its.append(mcq(fig(tenframe_svg(n)) + q, m, wrongs(n), e))
    o = its
    order = [o[0], o[10], o[15], o[1], o[11], o[16], o[2], o[12], o[17], o[3],
             o[13], o[18], o[4], o[14], o[19], o[5], o[6], o[7], o[8], o[9]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Pairs that make 10", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def story(n, kind, text, pic="frame", unit=None):
        p = K.next()
        m = 10 - n
        t = text.format(n_=n, m=m, **p)
        svg = tenframe_svg(n, frames=1, kind=kind) if pic == "frame" else box_svg(n, kind)
        one, many = unit or (name(kind, 1), name(kind))
        u = lambda v: "%d %s" % (v, one if v == 1 else many)
        e = "%d and %d make 10. %d + %d = 10. The answer is <b>%s</b>." % (n, m, n, m, u(m))
        its.append(mcq(fig(svg) + t, u(m), [u(w) for w in wrongs(n) if w], e))

    story(8, "cup", "{n} needs 10 cups for a party. {He} has {n_}. How many more cups does {he} need?")
    story(9, "apple", "A box holds 10 apples. It has {n_} apples. How many more apples fit in the box?")
    story(5, "star", "{n} wants 10 stars. {He} has {n_}. How many more stars does {he} need?")
    story(7, "duck", "There are 10 toy ducks in all. {n_} are out. The rest are in a box. How many are in the box?", pic="box")
    story(6, "ball", "{n} has 10 balls. {n_} are on the floor. The rest are in a box. How many balls are in the box?", pic="box")
    story(4, "fish", "A tank needs 10 fish. It has {n_}. How many more fish are needed?")
    story(3, "flower", "{n} wants to plant 10 flowers. {He} has planted {n_}. How many more must {he} plant?")
    story(8, "bug", "There are 10 ladybugs in all. {n_} are out. The rest are in a box. How many are in the box?", pic="box")
    story(2, "heart", "{n} wants to draw 10 hearts. {He} has drawn {n_}. How many more hearts does {he} need to draw?")
    story(9, "button", "A card needs 10 buttons. {n} has glued on {n_}. How many more buttons does {he} need?")
    story(1, "cup", "{n} needs 10 cups. {He} has only {n_}. How many more cups does {he} need?")
    story(6, "star", "{n} gets 10 stickers. {He} puts {n_} on a page. How many stickers are left to put on?",
          unit=("sticker", "stickers"))
    story(7, "apple", "{n} picks 10 apples. {He} puts {n_} in a bowl. The rest are in a box. How many are in the box?", pic="box")
    story(5, "duck", "10 ducks walk to the pond. {n_} get there first. How many are still walking?")
    story(4, "ball", "{n} must find 10 balls. {He} has found {n_}. How many more balls must {he} find?")
    story(3, "bug", "{n} has 10 toy ladybugs. {n_} are out. The rest are in a box. How many are in the box?", pic="box")
    story(8, "fish", "{n} catches 10 fish. {He} keeps {n_}. {He} lets the rest go. How many does {he} let go?")
    story(2, "flower", "There are 10 flowers in all. {n_} are on the table. The rest are in a box. How many are in the box?", pic="box")
    story(1, "heart", "{n} needs 10 hearts for a card. {He} has cut out {n_}. How many more hearts must {he} cut out?")
    story(9, "dot", "10 kids are in a class. {n_} are here. How many kids are not here yet?", unit=("kid", "kids"))
    return {"title": "Make-10 stories", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Make 10 with a ten-frame</h2>"
        "<p>A ten-frame has 10 boxes. Count the dots. The <b>empty boxes</b> show how many more make 10.</p>"
        "<figure class='sn-fig'>" + tenframe_mix_svg(["r"] * 7 + [""] * 3)
        + "<figcaption>7 dots and 3 empty boxes: 7 + 3 = 10.</figcaption></figure>"
        "<h2>Pairs that make 10</h2>"
        + table(["Number", "Goes with", "Sentence"], [
            ["1", "9", "1 + 9 = 10"], ["2", "8", "2 + 8 = 10"], ["3", "7", "3 + 7 = 10"],
            ["4", "6", "4 + 6 = 10"], ["5", "5", "5 + 5 = 10"], ["6", "4", "6 + 4 = 10"],
            ["7", "3", "7 + 3 = 10"], ["8", "2", "8 + 2 = 10"], ["9", "1", "9 + 1 = 10"],
        ]) +
        "<h2>Count on to 10</h2>"
        "<figure class='sn-fig'>" + box_svg(6, "ball")
        + "<figcaption>10 balls in all. You see 6. Count on: 7, 8, 9, 10. That is 4 in the box.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Answering with the number you see", "Find how many more make 10"],
            ["Counting the start when counting on", "Start after the number: 7, 8, 9, 10"],
            ["Off by one", "Count the empty boxes"],
        ])
    )


FAQ = [
    {"q": "Why is making 10 so important?",
     "a": "Our numbers are built on tens. Children who know 7 and 3 make 10 can later add 8 + 5 by making a 10 first (8 + 2 + 3). It is the base for adding and subtracting to 20."},
    {"q": "How can I practice making 10 at home?",
     "a": "Use 10 fingers: hold up 6 and ask how many are down. Use an egg carton with 10 cups, or hide some of 10 toys under a cup and ask how many are hidden."},
    {"q": "Which pairs make 10?",
     "a": "1 and 9, 2 and 8, 3 and 7, 4 and 6, and 5 and 5. The order does not matter: 3 + 7 and 7 + 3 both make 10."},
    {"q": "Should kindergartners know these by heart?",
     "a": "By the end of kindergarten, children should find the partner for any number 1 to 9, using objects, drawings or ten-frames. Quick recall builds over time in Grade 1."},
]


def gen():
    rnd = random.Random(2007)
    K = Kids(rnd)
    sets = [set_fill(rnd, K), set_missing(rnd, K), set_box(rnd, K), set_pairs(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=10)
    return {
        "slug": "make-10", "sort": 7, "updated": UPDATED, "pdf_url": "",
        "title": "Make 10: Find the Number That Makes 10",
        "seo_title": "Kindergarten Make 10 Worksheets: Ten-Frames, Pairs That Make 10, How Many More",
        "short_title": "Make 10",
        "domain": "Operations and Algebraic Thinking",
        "standard_code": "K.OA.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/OA/A/4/",
        "standard_text": "For any number from 1 to 9, find the number that makes 10 when added to the given number, "
                         "e.g., by using objects or drawings, and record the answer with a drawing or equation.",
        "meta_desc": "Free kindergarten make 10 worksheets: fill a ten-frame, find the missing part (7 + ? = 10), find "
                     "how many are hidden, learn the pairs that make 10, and solve how-many-more stories. "
                     "100 picture questions with an answer key.",
        "key_big": "Count the empty boxes in a ten-frame. They show how many more make 10.",
        "key_sub": "1 and 9, 2 and 8, 3 and 7, 4 and 6, 5 and 5 make 10.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
