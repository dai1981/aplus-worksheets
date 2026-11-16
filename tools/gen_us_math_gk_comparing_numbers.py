# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Comparing Numbers (K.CC.C.6, K.CC.C.7)
  python3 tools/gen_us_math_gk_comparing_numbers.py
Match two rows one to one (more, fewer, the same), find the box with the most / fewest,
find a group with the same number, and compare written numbers 1 to 10.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import (name, match_svg, lettered_groups_svg, cards_svg, number_line_svg, two_groups_svg, KINDS)
from k_common import Kids, mcq, lst, finish

UPDATED = "2026-11-16"
SAME = "The same number"
CANT = "We cannot tell"


# ============================================================ set 1: more, fewer or the same
def set_rows(rnd, K):
    its = []
    pairs = [(5, 3, "apple", "cup"), (4, 4, "duck", "fish"), (2, 6, "star", "heart"), (7, 5, "ball", "flower"),
             (6, 6, "bug", "button"), (3, 7, "cup", "apple"), (8, 6, "fish", "duck"), (5, 5, "heart", "star"),
             (9, 7, "flower", "ball"), (4, 8, "button", "bug")]
    for i, (a, b, ka, kb) in enumerate(pairs):
        A, B = name(ka), name(kb)
        svg = match_svg([(a, ka, "", 0), (b, kb, "", 0)])
        if i % 2 == 0:
            q = "Are there more %s or more %s?" % (A, B)
            ans = SAME if a == b else ("More " + A if a > b else "More " + B)
            ch = ["More " + A, "More " + B, SAME, CANT]
        else:
            q = "Are there fewer %s or fewer %s?" % (A, B)
            ans = SAME if a == b else ("Fewer " + A if a < b else "Fewer " + B)
            ch = ["Fewer " + A, "Fewer " + B, SAME, CANT]
        if a == b:
            e = "Match each %s with a %s. None are left over. There are %d of each: <b>the same number</b>." % (
                name(ka, 1), name(kb, 1), a)
        else:
            big, small = (A, B) if a > b else (B, A)
            if i % 2 == 0:
                e = ("Match them one to one. Some %s have no partner, so there are <b>more %s</b>. "
                     "%d is more than %d." % (big, big, max(a, b), min(a, b)))
            else:
                e = ("Match them one to one. Some %s have no partner, so there are <b>fewer %s</b>. "
                     "%d is less than %d." % (big, small, min(a, b), max(a, b)))
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    # a longer row is not always more: spread-out rows
    for a, b, ka, kb in [(4, 6, "duck", "apple"), (5, 7, "star", "cup"), (3, 5, "ball", "fish"),
                         (6, 6, "flower", "heart"), (5, 8, "heart", "button"), (7, 7, "cup", "duck")]:
        A, B = name(ka), name(kb)
        sp = int(CELL_W * b / a + 6) if a < b else CELL_W + 22
        svg = match_svg([(a, ka, "", sp), (b, kb, "", 0)])
        q = "Look at the %s row. It is long. Are there more %s or more %s?" % (A, A, B)
        ans = SAME if a == b else ("More " + B)
        ch = ["More " + A, "More " + B, SAME, CANT]
        if a == b:
            e = ("Do not look at how long the row is. Count: %d %s and %d %s. They are <b>the same number</b>."
                 % (a, A, b, B))
        else:
            e = ("Do not look at how long the row is. Count: %d %s and %d %s. %d is more than %d, so there are "
                 "<b>more %s</b>." % (a, A, b, B, b, a, B))
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    # count both and say how many
    for a, b, ka, kb in [(6, 4, "apple", "star"), (3, 5, "fish", "bug"), (8, 9, "duck", "ball"), (7, 10, "button", "flower")]:
        svg = match_svg([(a, ka, "", 0), (b, kb, "", 0)])
        q = "Count each row. Which row has more?"
        top, bot = "The top row", "The bottom row"
        ans = top if a > b else bot
        e = ("The top row has %d. The bottom row has %d. %d is more than %d, so <b>%s</b> has more."
             % (a, b, max(a, b), min(a, b), ans.lower()))
        its.append(mcq(fig(svg) + q, ans, [top if ans == bot else bot, "They are the same", CANT], e))
    o = its
    order = [o[0], o[1], o[2], o[3], o[16], o[4], o[5], o[10], o[17], o[6],
             o[11], o[7], o[12], o[18], o[8], o[13], o[9], o[14], o[19], o[15]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "More, fewer or the same", "items": order}


CELL_W = 36


# ============================================================ set 2: most and fewest
def set_boxes(rnd, K):
    its = []
    plans = [("most", [3, 5, 2, 4]), ("fewest", [4, 2, 5, 3]), ("most", [6, 4, 7, 5]), ("fewest", [5, 7, 3, 6]),
             ("most", [2, 6, 4, 3]), ("fewest", [6, 5, 8, 7]), ("most", [7, 9, 8, 6]), ("fewest", [9, 4, 6, 5]),
             ("most", [5, 8, 6, 10]), ("fewest", [8, 10, 7, 9]), ("most", [4, 3, 1, 2]), ("fewest", [3, 1, 4, 2]),
             ("most", [8, 6, 7, 9]), ("fewest", [7, 9, 10, 6]), ("most", [10, 7, 9, 8]), ("fewest", [6, 8, 9, 10]),
             ("most", [3, 7, 5, 6]), ("fewest", [4, 6, 2, 9]), ("most", [9, 10, 6, 7]), ("fewest", [10, 8, 9, 5])]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    for i, (word, counts) in enumerate(plans):
        assert len(set(counts)) == 4
        kind = kinds[i % len(kinds)]
        v = max(counts) if word == "most" else min(counts)
        ans = "Box " + "ABCD"[counts.index(v)]
        svg = lettered_groups_svg([(c, kind) for c in counts])
        q = "Which box has the <b>%s</b> %s?" % (word, name(kind))
        e = ("Count each box: %s. %d is the %s number, so <b>%s</b> has the %s."
             % (", ".join("%s has %d" % ("ABCD"[j], c) for j, c in enumerate(counts)), v,
                "greatest" if word == "most" else "smallest", ans, word))
        its.append(mcq(fig(svg) + q, ans, ["Box " + "ABCD"[j] for j in range(4) if counts[j] != v], e))
    return {"title": "The most and the fewest", "items": its}


# ============================================================ set 3: the same number
def set_same(rnd, K):
    its = []
    plans = [(3, [2, 3, 4, 5]), (4, [5, 3, 4, 6]), (5, [5, 4, 6, 3]), (6, [7, 5, 4, 6]), (2, [3, 1, 2, 4]),
             (7, [6, 8, 7, 5]), (8, [8, 9, 7, 6]), (6, [6, 8, 5, 7]), (9, [10, 8, 9, 7]), (10, [9, 10, 8, 7]),
             (5, [4, 6, 3, 5]), (7, [9, 7, 6, 8]), (8, [7, 9, 10, 8]), (4, [3, 6, 4, 5]), (9, [9, 8, 10, 7])]
    kinds = KINDS[:]
    rnd.shuffle(kinds)
    for i, (n, counts) in enumerate(plans):
        ka, kb = kinds[i % 10], kinds[(i + 3) % 10]
        ans = "Box " + "ABCD"[counts.index(n)]
        svg = match_svg([(n, ka, "", 0)]) + lettered_groups_svg([(c, kb) for c in counts])
        q = "Which box has the <b>same number</b> of %s as there are %s?" % (name(kb), name(ka))
        e = ("There are %d %s. Count each box: %s. <b>%s</b> has %d %s too."
             % (n, name(ka), ", ".join("%s has %d" % ("ABCD"[j], c) for j, c in enumerate(counts)), ans, n, name(kb)))
        its.append(mcq(fig(svg) + q, ans, ["Box " + "ABCD"[j] for j in range(4) if counts[j] != n], e))
    # same or not with two rows
    for a, b, ka, kb in [(5, 5, "cup", "apple"), (6, 7, "star", "duck"), (8, 8, "fish", "ball"),
                         (9, 8, "bug", "heart"), (10, 10, "button", "flower")]:
        svg = match_svg([(a, ka, "", 0), (b, kb, "", 0)])
        q = "Is there 1 %s for each %s?" % (name(kb, 1), name(ka, 1))
        if a == b:
            ans, e = "Yes, the same number", "Match them one to one. None are left over. There are %d of each: <b>yes, the same number</b>." % a
        elif b > a:
            ans, e = "No, there are more %s" % name(kb), "Match them one to one. %d %s and %d %s: <b>no, there are more %s</b>." % (a, name(ka), b, name(kb), name(kb))
        else:
            ans, e = "No, there are fewer %s" % name(kb), "Match them one to one. %d %s and %d %s: <b>no, there are fewer %s</b>." % (a, name(ka), b, name(kb), name(kb))
        ch = ["Yes, the same number", "No, there are more %s" % name(kb), "No, there are fewer %s" % name(kb), CANT]
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    o = its
    order = [o[4], o[0], o[15], o[1], o[2], o[16], o[10], o[3], o[13], o[17],
             o[5], o[7], o[18], o[6], o[11], o[8], o[19], o[12], o[9], o[14]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    # the two svgs of one question go in one picture box
    for it in order:
        it["q"] = it["q"].replace("</svg><svg", "</svg><br><svg")
    return {"title": "The same number", "items": order}


# ============================================================ set 4: compare written numbers
def set_numbers(rnd, K):
    its = []
    line = number_line_svg(0, 10, sp=34)
    for a, b in [(3, 5), (8, 6), (2, 9), (7, 4), (10, 7), (6, 9), (1, 4), (5, 8)]:
        big = max(a, b)
        q = fig(cards_svg([str(a), str(b)], w=60, h=60)) + "Which number is <b>greater</b>?"
        e = "Count up: %s. %d comes later when you count, so <b>%d</b> is greater." % (
            lst(1, big), big, big)
        its.append(mcq(q, big, [min(a, b), abs(a - b), big + 1 if big < 10 else big - 1, big - 1, min(a, b) - 1], e))
    for a, b in [(4, 7), (9, 5), (6, 3), (8, 10)]:
        small = min(a, b)
        q = fig(cards_svg([str(a), str(b)], w=60, h=60)) + "Which number is <b>less</b>?"
        e = "%d comes first when you count, so <b>%d</b> is less." % (small, small)
        its.append(mcq(q, small, [max(a, b), small - 1, abs(a - b), small + 1, max(a, b) + 1], e))
    for n, ch, word in [(5, [8, 4, 3, 5], "greater"), (6, [2, 6, 7, 9], "less"), (4, [3, 4, 2, 9], "greater"),
                        (8, [9, 10, 8, 5], "less"), (3, [1, 3, 2, 7], "greater"), (7, [6, 9, 7, 10], "less"),
                        (2, [2, 1, 6, 0], "greater"), (9, [10, 9, 8, 1], "greater")]:
        ch = list(dict.fromkeys(ch))
        good = [c for c in ch if (c > n if word == "greater" else c < n)]
        if len(good) != 1:
            # keep exactly one right answer
            if word == "greater":
                ch = [c for c in ch if c <= n][:3] + [max(c for c in range(n + 1, 11))]
            else:
                ch = [c for c in ch if c >= n][:3] + [min(c for c in range(1, n))]
            good = [c for c in ch if (c > n if word == "greater" else c < n)]
        assert len(good) == 1 and len(ch) == 4, (n, ch)
        ans = good[0]
        q = fig(line) + "Which number is <b>%s than %d</b>?" % (word, n)
        side = "right" if word == "greater" else "left"
        e = ("On the number line, numbers to the %s of %d are %s. Only <b>%d</b> is %s than %d. "
             "%d is not %s than itself." % (side, n, word, ans, word, n, n, word))
        its.append(mcq(q, ans, [c for c in ch if c != ans], e, allow_zero=True))
    o = its
    order = [o[0], o[1], o[8], o[2], o[12], o[3], o[9], o[13], o[4], o[14],
             o[5], o[10], o[15], o[6], o[16], o[11], o[17], o[7], o[18], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Compare numbers 1 to 10", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []

    def who(a, b, ka, word, text):
        p, r = K.two()
        svg = match_svg([(a, ka, p["n"], 0), (b, ka, r["n"], 0)])
        t = text.format(a=p["n"], b=r["n"], k=name(ka))
        if a == b:
            ans = "They have the same"
        elif word == "more":
            ans = p["n"] if a > b else r["n"]
        else:
            ans = p["n"] if a < b else r["n"]
        ch = [p["n"], r["n"], "They have the same", CANT]
        e = "%s has %d. %s has %d. " % (p["n"], a, r["n"], b)
        if a == b:
            e += "%d and %d are the same, so <b>they have the same</b> number." % (a, b)
        else:
            e += "%d is %s than %d, so <b>%s</b> has %s." % (
                a if ans == p["n"] else b, "greater" if word == "more" else "less", b if ans == p["n"] else a, ans, word)
        its.append(mcq(fig(svg) + t, ans, [c for c in ch if c != ans], e))

    who(6, 4, "star", "more", "{a} and {b} have stickers. Who has more?")
    who(3, 5, "apple", "more", "{a} and {b} pick apples. Who has more apples?")
    who(5, 5, "ball", "more", "{a} and {b} have balls. Who has more balls?")
    who(7, 4, "flower", "fewer", "{a} and {b} pick flowers. Who has fewer flowers?")
    who(2, 6, "fish", "fewer", "{a} and {b} catch fish. Who has fewer fish?")
    who(8, 9, "button", "more", "{a} and {b} count buttons. Who has more buttons?")
    who(6, 6, "heart", "fewer", "{a} and {b} draw hearts. Who has fewer hearts?")
    who(10, 7, "cup", "fewer", "{a} and {b} stack cups. Who has fewer cups?")
    who(9, 6, "duck", "more", "{a} and {b} have toy ducks. Who has more ducks?")
    who(4, 8, "bug", "fewer", "{a} and {b} find ladybugs. Who found fewer ladybugs?")
    # enough for everyone
    for kids, things, kk, kt in [(5, 4, "duck", "cup"), (6, 6, "bug", "heart"), (4, 6, "ball", "star"), (7, 5, "bug", "flower")]:
        svg = match_svg([(kids, kk, "", 0), (things, kt, "", 0)])
        q = "Each %s needs 1 %s. Are there enough %s?" % (name(kk, 1), name(kt, 1), name(kt))
        if things == kids:
            ans, e = "Yes, just enough", "%d %s and %d %s. Each %s gets 1: <b>yes, just enough</b>." % (kids, name(kk), things, name(kt), name(kk, 1))
        elif things > kids:
            ans, e = "Yes, with some left over", "%d %s and %d %s. %d is more than %d: <b>yes, with some left over</b>." % (kids, name(kk), things, name(kt), things, kids)
        else:
            ans, e = "No, not enough", "%d %s and only %d %s. %d is less than %d: <b>no, not enough</b>." % (kids, name(kk), things, name(kt), things, kids)
        ch = ["Yes, just enough", "Yes, with some left over", "No, not enough", CANT]
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    # numbers in words
    for t, ans, wr, e in [
        ("Mia is 5. Her brother is 7. Who is older?", "Her brother", ["Mia", "They are the same", CANT],
         "7 is greater than 5, so <b>her brother</b> is older."),
        ("A red bus has 9 kids. A blue bus has 6 kids. Which bus has more kids?", "The red bus",
         ["The blue bus", "They have the same", CANT], "9 is greater than 6, so <b>the red bus</b> has more."),
        ("Leo has 4 cars. Sam has 4 cars. Who has more cars?", "They have the same", ["Leo", "Sam", CANT],
         "4 and 4 are the same number, so <b>they have the same</b>."),
        ("A tower has 8 blocks. Another tower has 10 blocks. Which tower has fewer blocks?",
         "The tower with 8", ["The tower with 10", "They have the same", CANT],
         "8 is less than 10, so <b>the tower with 8</b> blocks has fewer."),
        ("Zoe has 10 crayons. Kai has 3 crayons. Who has fewer crayons?", "Kai", ["Zoe", "They have the same", CANT],
         "3 is less than 10, so <b>Kai</b> has fewer."),
    ]:
        nums = [int(x) for x in __import__("re").findall(r"\d+", t)]
        svg = cards_svg([str(x) for x in nums], w=60, h=60)
        its.append(mcq(fig(svg) + t, ans, wr, e))
    # spread out but fewer
    p = K.next()
    svg = match_svg([(5, "star", "", 64), (7, "star", "", 0)])
    its.append(mcq(fig(svg) + "%s says the top row has more stars because it is longer. Is %s right?" % (p["n"], p["he"]),
                   "No, the bottom row has more", ["Yes, the top row has more", "They have the same", CANT],
                   "Count each row: the top has 5, the bottom has 7. A longer row does not mean more. "
                   "<b>No, the bottom row has more</b>."))
    o = its
    order = [o[0], o[1], o[2], o[14], o[3], o[10], o[4], o[15], o[5], o[11],
             o[6], o[16], o[7], o[12], o[17], o[8], o[13], o[9], o[18], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Comparing stories", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Match one to one</h2>"
        "<p>Put each thing in one row with a thing in the other row. "
        "The row with things left over has <b>more</b>. The other row has <b>fewer</b>.</p>"
        "<figure class='sn-fig'>" + match_svg([(6, "apple", "", 0), (4, "cup", "", 0)])
        + "<figcaption>2 apples have no cup. There are more apples and fewer cups.</figcaption></figure>"
        "<p>If nothing is left over, they are <b>the same number</b>.</p>"
        "<h2>A longer row is not always more</h2>"
        "<figure class='sn-fig'>" + match_svg([(4, "duck", "", 64), (6, "duck", "", 0)])
        + "<figcaption>The top row is longer, but it has only 4. The bottom row has 6. Count to check.</figcaption></figure>"
        "<h2>Compare numbers</h2>"
        "<p>When you count, the number that comes <b>later</b> is <b>greater</b>. "
        "The number that comes <b>first</b> is <b>less</b>.</p>"
        "<figure class='sn-fig'>" + number_line_svg(0, 10, sp=34)
        + "<figcaption>8 is greater than 5. 5 is less than 8.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Thinking a longer row has more", "Match or count the things"],
            ["Mixing up more and fewer", "More has things left over"],
            ["Saying 3 is greater than 5", "Count: 5 comes after 3, so 5 is greater"],
        ])
    )


FAQ = [
    {"q": "What does comparing numbers mean in kindergarten?",
     "a": "Children look at two groups and say which has more, which has fewer, or if they are the same. They also compare written numbers from 1 to 10, like 7 and 4."},
    {"q": "Why does my child think a spread-out row has more?",
     "a": "Young children often judge by how long a row looks. Line the things up one to one, or count both rows, to show that the number does not change when things are spread out."},
    {"q": "How can I practice at home?",
     "a": "Set the table: is there one spoon for each plate? Compare snacks, toy cars or blocks. Ask: Who has more? How do you know?"},
    {"q": "Should kindergartners use the signs > and <?",
     "a": "Not yet. In kindergarten children use the words greater, less, more, fewer and the same. The signs come in Grade 1."},
]


def gen():
    rnd = random.Random(2004)
    K = Kids(rnd)
    sets = [set_rows(rnd, K), set_boxes(rnd, K), set_same(rnd, K), set_numbers(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=10)
    return {
        "slug": "comparing-numbers", "sort": 4, "updated": UPDATED, "pdf_url": "",
        "title": "Comparing Numbers: More, Fewer or the Same",
        "seo_title": "Kindergarten Comparing Numbers Worksheets: More, Fewer, Same, Greater and Less",
        "short_title": "Comparing Numbers",
        "domain": "Counting and Cardinality",
        "standard_code": "K.CC.C.6",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/CC/C/6/",
        "standard_text": "Identify whether the number of objects in one group is greater than, less than, or equal to the "
                         "number of objects in another group, e.g., by using matching and counting strategies.",
        "meta_desc": "Free kindergarten comparing numbers worksheets: match two groups one to one, find more, fewer or "
                     "the same, pick the box with the most or fewest, and compare numbers 1 to 10 (greater and less). "
                     "100 picture questions with an answer key.",
        "key_big": "Match one to one. The group with some left over has more.",
        "key_sub": "When you count, the number that comes later is greater. A longer row is not always more.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
