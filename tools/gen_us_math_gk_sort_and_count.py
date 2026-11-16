# -*- coding: utf-8 -*-
"""
US Kindergarten Math: Sort and Count (K.MD.B.3)
  python3 tools/gen_us_math_gk_sort_and_count.py
Sort objects into groups, count each group (up to 10), find the group with the most or fewest,
sort shapes by colour or by shape, find the one that does not belong, and short sorting stories.
"""
import random
from ws_common import table, write_unit, fig
from k_pics import name, mixed_svg, shapes_mix_svg, lettered_shapes_svg, objects_row_svg, lettered_groups_svg
from k_common import Kids, mcq, finish

UPDATED = "2026-11-16"
SAMEALL = "They are the same"


def cw(n):
    return [n + 1, n - 1, n + 2, n - 2]


# ============================================================ set 1: count one kind
def set_count(rnd, K):
    plans = [[("apple", 3), ("star", 2)], [("duck", 4), ("fish", 3)], [("ball", 2), ("cup", 5)],
             [("heart", 5), ("button", 4)], [("bug", 6), ("flower", 3)], [("apple", 4), ("ball", 3), ("star", 2)],
             [("fish", 5), ("duck", 2), ("cup", 3)], [("star", 6), ("heart", 4)], [("button", 3), ("bug", 7)],
             [("flower", 5), ("apple", 3), ("fish", 4)], [("cup", 6), ("ball", 5)], [("duck", 7), ("star", 3), ("heart", 2)],
             [("apple", 8), ("bug", 4)], [("fish", 6), ("button", 5), ("flower", 3)], [("heart", 7), ("cup", 6)],
             [("ball", 8), ("duck", 3), ("apple", 4)], [("star", 9), ("fish", 5)], [("bug", 5), ("heart", 6), ("cup", 4)],
             [("flower", 9), ("button", 6)], [("duck", 10), ("apple", 6)]]
    its = []
    for i, counts in enumerate(plans):
        kind, n = counts[i % len(counts)] if i % 3 else counts[0]
        svg = mixed_svg(counts, seed=100 + i)
        q = "How many <b>%s</b> are there?" % name(kind)
        e = "Look only at the %s. Touch each one and count: %s. There are <b>%d</b> %s." % (
            name(kind), ", ".join(str(k) for k in range(1, n + 1)), n, name(kind, n))
        its.append(mcq(fig(svg) + q, n, cw(n) + [sum(c for _, c in counts)], e))
    return {"title": "Count one group", "items": its}


# ============================================================ set 2: most and fewest
def set_most(rnd, K):
    plans = [([("apple", 4), ("star", 2), ("ball", 3)], "most"), ([("duck", 2), ("fish", 5), ("cup", 3)], "fewest"),
             ([("heart", 3), ("button", 6), ("bug", 4)], "most"), ([("flower", 5), ("apple", 2), ("star", 4)], "fewest"),
             ([("ball", 6), ("duck", 4), ("fish", 5)], "most"), ([("cup", 3), ("heart", 6), ("button", 5)], "fewest"),
             ([("bug", 2), ("flower", 7), ("apple", 4)], "most"), ([("star", 6), ("ball", 4), ("duck", 3)], "fewest"),
             ([("fish", 3), ("cup", 5), ("heart", 8)], "most"), ([("button", 7), ("bug", 5), ("flower", 6)], "fewest"),
             ([("apple", 5), ("duck", 5), ("star", 3)], "fewest"), ([("ball", 4), ("fish", 7), ("cup", 4)], "most"),
             ([("heart", 6), ("button", 2), ("bug", 3)], "most"), ([("flower", 4), ("apple", 6), ("star", 7)], "fewest"),
             ([("duck", 8), ("fish", 6), ("ball", 7)], "fewest"), ([("cup", 2), ("heart", 9), ("button", 5)], "most"),
             ([("bug", 7), ("flower", 8), ("apple", 6)], "most"), ([("star", 5), ("duck", 9), ("fish", 4)], "fewest"),
             ([("ball", 6), ("cup", 6), ("heart", 6)], "most"), ([("button", 10), ("bug", 6), ("flower", 8)], "fewest")]
    its = []
    for i, (counts, word) in enumerate(plans):
        ns = [n for _, n in counts]
        v = max(ns) if word == "most" else min(ns)
        winners = [k for k, n in counts if n == v]
        svg = mixed_svg(counts, seed=200 + i, cols=7, rows=4)
        q = "Which group has the <b>%s</b>?" % word
        ans = SAMEALL if len(winners) == 3 else name(winners[0]).capitalize()
        assert len(winners) in (1, 3)
        ch = [name(k).capitalize() for k, _ in counts] + [SAMEALL]
        e = "Count each kind: %s. " % ", ".join("%d %s" % (n, name(k, n)) for k, n in counts)
        e += ("All the groups have %d. <b>They are the same</b>." % v) if ans == SAMEALL else \
            "%d is the %s number, so the answer is <b>%s</b>." % (v, "greatest" if word == "most" else "smallest", ans)
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    return {"title": "Most and fewest", "items": its}


# ============================================================ set 3: sort shapes
def set_shapes(rnd, K):
    its = []
    pool_k = ["circle", "square", "triangle"]
    pool_c = ["red", "blue", "yellow"]
    for i in range(20):
        r = random.Random(300 + i)
        n = r.randint(7, 12)
        items = [(r.choice(pool_k), r.choice(pool_c)) for _ in range(n)]
        mode = ["color", "shape", "both"][i % 3] if i >= 4 else ["color", "shape"][i % 2]
        if mode == "color":
            c = r.choice([x for _, x in items])
            ans = sum(1 for _, x in items if x == c)
            q = "How many <b>%s</b> shapes are there?" % c
            e = "Look at the color only. Count the %s shapes: there are <b>%d</b>." % (c, ans)
        elif mode == "shape":
            k = r.choice([x for x, _ in items])
            ans = sum(1 for x, _ in items if x == k)
            q = "How many <b>%ss</b> are there?" % k
            e = "Look at the shape only. Count the %ss of every color: there are <b>%d</b>." % (k, ans)
        else:
            k, c = r.choice(items)
            ans = sum(1 for x in items if x == (k, c))
            q = "How many <b>%s %ss</b> are there?" % (c, k)
            e = "Look for shapes that are %s <b>and</b> %ss. There %s <b>%d</b>." % (c, k, "is" if ans == 1 else "are", ans)
        wr = cw(ans) + [n]
        its.append(mcq(fig(shapes_mix_svg(items, seed=400 + i, cols=4 if n <= 8 else 5)) + q, ans, wr, e))
    assert len(its) == 20, len(its)
    return {"title": "Sort shapes by color or shape", "items": its}


# ============================================================ set 4: what does not belong?
def set_odd(rnd, K):
    its = []
    for kinds, odd, why in [
        (["duck", "fish", "bug", "apple"], "apple", "The duck, the fish and the ladybug are animals. The apple is a food."),
        (["apple", "duck", "fish", "bug"], "apple", "The others are animals. The apple is not an animal."),
        (["fish", "cup", "duck", "bug"], "cup", "The others are animals. A cup is a thing we drink from."),
        (["bug", "fish", "ball", "duck"], "ball", "The others are animals. A ball is a toy."),
        (["flower", "duck", "bug", "fish"], "flower", "The others are animals. A flower is a plant."),
    ]:
        idx = kinds.index(odd)
        ans = "ABCD"[idx]
        its.append(mcq(fig(objects_row_svg(kinds)) + "Which one does <b>not</b> belong?", ans,
                       [x for x in "ABCD" if x != ans], why + " The answer is <b>%s</b>." % ans))
    for items, why in [
        ([("circle", "red"), ("circle", "blue"), ("square", "yellow"), ("circle", "green")], "shape"),
        ([("triangle", "blue"), ("triangle", "blue"), ("triangle", "red"), ("triangle", "blue")], "color"),
        ([("square", "green"), ("triangle", "green"), ("square", "green"), ("square", "green")], "shape"),
        ([("circle", "yellow"), ("square", "yellow"), ("triangle", "blue"), ("rectangle", "yellow")], "color"),
        ([("rectangle", "red"), ("rectangle", "blue"), ("rectangle", "yellow"), ("circle", "red")], "shape"),
        ([("hexagon", "green"), ("hexagon", "red"), ("hexagon", "green"), ("hexagon", "green")], "color"),
        ([("triangle", "yellow"), ("triangle", "red"), ("triangle", "blue"), ("square", "blue")], "shape"),
        ([("circle", "blue"), ("square", "blue"), ("triangle", "blue"), ("circle", "red")], "color"),
        ([("square", "red"), ("square", "blue"), ("rectangle", "green"), ("square", "yellow")], "shape"),
        ([("hexagon", "yellow"), ("circle", "yellow"), ("hexagon", "red"), ("triangle", "yellow")], "color"),
    ]:
        if why == "shape":
            ks = [k for k, _ in items]
            odd = [i for i, k in enumerate(ks) if ks.count(k) == 1]
            e = "Three of them are %ss. The odd one is a %s." % ([k for k in ks if ks.count(k) == 3][0], ks[odd[0]])
        else:
            cs = [c for _, c in items]
            odd = [i for i, c in enumerate(cs) if cs.count(c) == 1]
            e = "Three of them are %s. The odd one is %s." % ([c for c in cs if cs.count(c) == 3][0], cs[odd[0]])
        assert len(odd) == 1, items
        ans = "ABCD"[odd[0]]
        its.append(mcq(fig(lettered_shapes_svg(items)) + "Which one does <b>not</b> belong?", ans,
                       [x for x in "ABCD" if x != ans], e + " The answer is <b>%s</b>." % ans))
    for counts, word in [([4, 7, 5, 6], "most"), ([6, 3, 5, 8], "fewest"), ([9, 6, 8, 7], "most"),
                         ([5, 7, 2, 4], "fewest"), ([6, 9, 10, 8], "most")]:
        kinds = ["apple", "duck", "star", "ball"]
        v = max(counts) if word == "most" else min(counts)
        ans = "Box " + "ABCD"[counts.index(v)]
        q = fig(lettered_groups_svg([(c, k) for c, k in zip(counts, kinds)])) + \
            "The toys are sorted into boxes. Which box has the <b>%s</b>?" % word
        e = "Count each box: %s. %s has %d. The answer is <b>%s</b>." % (
            ", ".join("%s has %d" % ("ABCD"[j], c) for j, c in enumerate(counts)), ans, v, ans)
        its.append(mcq(q, ans, ["Box " + "ABCD"[j] for j in range(4) if counts[j] != v], e))
    o = its
    order = [o[0], o[5], o[1], o[6], o[15], o[2], o[7], o[8], o[16], o[3],
             o[9], o[10], o[17], o[4], o[11], o[12], o[18], o[13], o[14], o[19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Which does not belong?", "items": order}


# ============================================================ set 5: stories
def set_stories(rnd, K):
    its = []
    plans = [
        ([("ball", 3), ("duck", 4)], "{n} sorts {his} toys into balls and ducks. How many ducks are there?", "duck"),
        ([("apple", 5), ("star", 2)], "{n} sorts stickers. How many apple stickers are there?", "apple"),
        ([("fish", 4), ("bug", 6)], "{n} sees fish and ladybugs. How many ladybugs are there?", "bug"),
        ([("cup", 3), ("button", 7)], "{n} sorts cups and buttons. How many buttons are there?", "button"),
        ([("heart", 6), ("flower", 5)], "{n} cuts out hearts and flowers. How many hearts are there?", "heart"),
        ([("duck", 5), ("fish", 3), ("bug", 2)], "{n} sorts toy animals. How many fish are there?", "fish"),
        ([("star", 7), ("apple", 4)], "{n} sorts stickers. How many star stickers are there?", "star"),
        ([("ball", 8), ("cup", 2)], "{n} puts away balls and cups. How many balls are there?", "ball"),
        ([("flower", 4), ("heart", 6), ("star", 3)], "{n} sorts paper shapes. How many flowers are there?", "flower"),
        ([("bug", 9), ("duck", 5)], "{n} counts toy ladybugs and ducks. How many ladybugs are there?", "bug"),
    ]
    for i, (counts, t, kind) in enumerate(plans):
        p = K.next()
        n = dict(counts)[kind]
        svg = mixed_svg(counts, seed=500 + i, cols=7, rows=3)
        e = "Sort first. Then count only the %s: there are <b>%d</b>." % (name(kind), n)
        its.append(mcq(fig(svg) + t.format(**p), n, cw(n) + [sum(c for _, c in counts)], e))
    for i, (counts, word) in enumerate([([("apple", 3), ("ball", 5)], "more"), ([("duck", 6), ("fish", 4)], "fewer"),
                                        ([("star", 2), ("heart", 7)], "more"), ([("cup", 5), ("bug", 8)], "fewer"),
                                        ([("button", 6), ("flower", 6)], "more")]):
        p = K.next()
        (ka, a), (kb, b) = counts
        svg = mixed_svg(counts, seed=600 + i, cols=7, rows=3)
        q = "%s sorts the toys. Are there %s %s or %s %s?" % (p["n"], word, name(ka), word, name(kb))
        if a == b:
            ans = "The same number"
        elif word == "more":
            ans = "More " + name(ka if a > b else kb)
        else:
            ans = "Fewer " + name(ka if a < b else kb)
        w = word.capitalize()
        ch = ["%s %s" % (w, name(ka)), "%s %s" % (w, name(kb)), "The same number", "We cannot tell"]
        e = "Sort and count: %d %s and %d %s. The answer is <b>%s</b>." % (a, name(ka, a), b, name(kb, b), ans.lower() if ans != "The same number" else "the same number")
        its.append(mcq(fig(svg) + q, ans, [c for c in ch if c != ans], e))
    for i, (counts, ask) in enumerate([([("apple", 4), ("duck", 3)], "in all"), ([("fish", 5), ("star", 2)], "in all"),
                                       ([("ball", 3), ("bug", 3), ("cup", 2)], "in all"), ([("heart", 6), ("button", 4)], "in all"),
                                       ([("flower", 2), ("duck", 5), ("apple", 3)], "in all")]):
        p = K.next()
        tot = sum(c for _, c in counts)
        svg = mixed_svg(counts, seed=700 + i, cols=7, rows=3)
        q = "%s counts every toy. How many toys are there in all?" % p["n"]
        e = "Count each group: %s. Put them together: <b>%d</b> in all." % (
            ", ".join("%d %s" % (c, name(k, c)) for k, c in counts), tot)
        its.append(mcq(fig(svg) + q, tot, cw(tot) + [max(c for _, c in counts)], e))
    o = its
    order = [o[0], o[1], o[10], o[2], o[15], o[3], o[11], o[4], o[16], o[5],
             o[12], o[6], o[17], o[7], o[13], o[8], o[18], o[9], o[14], o[19]]
    assert len({id(x) for x in order}) == 20
    return {"title": "Sorting stories", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Sort, then count</h2>"
        "<p>To <b>sort</b> means to put things that are alike in the same group. "
        "Then count each group.</p>"
        "<figure class='sn-fig'>" + mixed_svg([("apple", 4), ("duck", 3), ("star", 2)], seed=11, cols=6, rows=3)
        + "<figcaption>4 apples, 3 ducks, 2 stars.</figcaption></figure>"
        "<h2>Ways to sort</h2>"
        + table(["Sort by", "Example"], [
            ["Kind", "animals and food"],
            ["Color", "red, blue, yellow"],
            ["Shape", "circles, squares, triangles"],
        ]) +
        "<h2>Compare the groups</h2>"
        "<p>The group with the biggest number has the <b>most</b>. The group with the smallest number has the <b>fewest</b>.</p>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do"], [
            ["Counting all the things", "Count only the group you are asked about"],
            ["Counting one thing twice", "Mark each one as you count"],
            ["Mixing up color and shape", "Ask: am I sorting by color or by shape?"],
        ])
    )


FAQ = [
    {"q": "What does sort and count mean in kindergarten?",
     "a": "Children put objects into groups by kind, color or shape. Then they count how many are in each group and say which group has the most or the fewest."},
    {"q": "Why is sorting important in math?",
     "a": "Sorting teaches children to notice how things are alike and different. It is the first step toward reading graphs and data."},
    {"q": "How many objects should a kindergartner sort?",
     "a": "Each group should have 10 or fewer objects, so children can count them easily."},
    {"q": "How can I practice sorting at home?",
     "a": "Sort laundry by color, toys by kind, or snacks by shape. Ask: How many are in each group? Which group has the most?"},
]


def gen():
    rnd = random.Random(2012)
    K = Kids(rnd)
    sets = [set_count(rnd, K), set_most(rnd, K), set_shapes(rnd, K), set_odd(rnd, K), set_stories(rnd, K)]
    finish(sets, rnd, max_num=20)
    return {
        "slug": "sort-and-count", "sort": 12, "updated": UPDATED, "pdf_url": "",
        "title": "Sort and Count: Group Objects by Kind, Color and Shape",
        "seo_title": "Kindergarten Sorting Worksheets: Sort, Classify and Count Objects",
        "short_title": "Sort and Count",
        "domain": "Measurement and Data",
        "standard_code": "K.MD.B.3",
        "standard_url": "https://www.thecorestandards.org/Math/Content/K/MD/B/3/",
        "standard_text": "Classify objects into given categories; count the numbers of objects in each category and sort "
                         "the categories by count.",
        "meta_desc": "Free kindergarten sorting worksheets: sort objects by kind, color and shape, count each group, "
                     "find the group with the most or fewest, and spot the one that does not belong. "
                     "100 picture questions with an answer key.",
        "key_big": "Put things that are alike in a group. Then count each group.",
        "key_sub": "You can sort by kind, color or shape. The biggest number is the most.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    write_unit("us", "math", "kindergarten", gen())
