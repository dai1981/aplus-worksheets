# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Building with Small Pieces (2-PS1-3)
  python tools/gen_us_science_g2_building_with_small_pieces.py
Make observations to construct an evidence-based account of how an object made of a small set of pieces can be
disassembled and made into a new object. Same pieces, new shape; the number of pieces and the weight stay the same.
Wrong answers come from real mistakes: "a bigger-looking shape has more blocks", "taking apart makes pieces disappear",
"the new object weighs more".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK

U = Unit(20103)
R = U.R
P = People(R)
USED = {}
COLS = ["#e05a4f", "#3f8fd2", "#f6c431", "#58a85a", "#e8893a", "#8e6bbf"]


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def shape_cells(kind, n):
    """grid cells (col, row from bottom) for n blocks"""
    if kind == "tower":
        return [(0, i) for i in range(n)]
    if kind == "wall":
        w = 4 if n % 4 == 0 else (3 if n % 3 == 0 else 2)
        return [(i % w, i // w) for i in range(n)]
    if kind == "row":
        return [(i, 0) for i in range(n)]
    if kind == "steps":
        if n not in (3, 6, 10):
            return None
        cells, c, h = [], 0, 1
        while len(cells) < n:
            for r in range(h):
                if len(cells) < n:
                    cells.append((c, r))
            c += 1
            h += 1
        return cells
    if kind == "bridge":      # two legs and a top
        if n < 5:
            return None
        legs = (n - 3) // 2
        top = n - 2 * legs
        cells = [(0, r) for r in range(legs)] + [(top - 1, r) for r in range(legs)] + [(c, legs) for c in range(top)]
        return cells if top >= 3 else None
    raise ValueError(kind)


def blocks_svg(cells_list, labels=None, u=26):
    s = ""
    x0 = 10
    W = 0
    H = max(max(r for _, r in cs) + 1 for cs in cells_list) * u + 20 + (24 if labels else 0)
    for i, cs in enumerate(cells_list):
        w = max(c for c, _ in cs) + 1
        base = H - (30 if labels else 10)
        for j, (c, r) in enumerate(cs):
            s += "<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5' rx='2'/>" % (
                x0 + c * u, base - (r + 1) * u, u - 2, u - 2, COLS[j % len(COLS)], INK)
        if labels:
            s += text(x0 + w * u / 2, H - 8, labels[i], 15)
        x0 += w * u + 36
        W = x0
    return svg_wrap(W, H, s, "block buildings" if len(cells_list) > 1 else "a building made of blocks")


SHAPES = ["tower", "wall", "row", "steps", "bridge"]
NEW = ["a car", "a house", "a bridge", "a robot", "a boat", "a wall", "a dog", "a train", "a castle"]


def g_count():
    kind = R.choice(SHAPES)
    n = R.randint(4, 12) if kind != "tower" else R.randint(3, 8)
    cs = shape_cells(kind, n)
    if not cs or not once(("c", kind, n)):
        return None
    who = P.next()[0]
    nm = {"steps": "staircase"}.get(kind, kind)
    return item(fig(blocks_svg([cs])) + "%s built a %s. How many blocks did %s use?" % (who, nm, who), str(n), [str(n - 1), str(n + 1), str(n + 2) if n > 3 else str(n + 3)],
                "Count every block: %d." % n)


def g_same():
    a, b = R.sample(SHAPES, 2)
    n = R.randint(5, 12)
    m = n if R.random() < 0.5 else n + R.choice([-2, -1, 1, 2])
    ca, cb = shape_cells(a, n), shape_cells(b, m)
    if not ca or not cb or m < 3 or not once(("s", a, b, n, m)):
        return None
    who = P.next()[0]
    pic = blocks_svg([ca, cb], ["A", "B"])
    if n == m:
        return item(fig(pic) + "%s took apart building A and built B. Could %s have used all the same blocks?" % (who, who), "Yes. Both use %d blocks." % n,
                    ["No. B looks bigger, so it has more blocks.", "No. A looks taller, so it has more blocks.", "No. Blocks disappear when you take them apart."],
                    "Count both: %d and %d. Same pieces, new shape." % (n, m))
    return item(fig(pic) + "%s says B was built from all the blocks in A. Is that true?" % who, "No. A has %d blocks and B has %d." % (n, m),
                ["Yes. They are both made of blocks.", "Yes. B is a new shape, so it must be the same.", "No. B has no blocks."], "Count the blocks in each building.")


def g_rebuild():
    n = R.randint(6, 30)
    a, b = R.sample(NEW, 2)
    who, she, her = P.next()
    t = R.choice(["count", "weigh"])
    if not once(("r", n, t)):
        return None
    if t == "count":
        return item("%s built %s with %d blocks. %s took it apart and used all the blocks to build %s. How many blocks are in the %s?" % (who, a, n, she.capitalize(), b, b.split(" ", 1)[1]),
                    str(n), [str(n - 2), str(n + 5), str(n * 2)], "Same pieces, so still %d blocks." % n)
    g = n * 10
    return item("%s's block %s weighs %d grams. %s takes it apart and builds %s with all the same blocks. How much does the %s weigh?" % (who, a.split(" ", 1)[1], g, she.capitalize(), b, b.split(" ", 1)[1]),
                "%d grams" % g, ["%d grams" % (g + 20), "%d grams" % (g // 2), "0 grams"], "Same pieces, so the weight stays the same.")


def g_pieces():
    who = P.next()[0]
    parts = R.choice([("a toy car", "wheels, a body and a seat"), ("a puzzle", "puzzle pieces"), ("a necklace", "beads and a string"), ("a sandwich", "bread, cheese and lettuce"),
                      ("a block castle", "blocks"), ("a paper chain", "paper loops"), ("a bike", "wheels, a frame, pedals and a seat")])
    if not once(("p", parts[0])):
        return None
    return item("%s takes apart %s. What will %s find?" % (who, parts[0], who), "smaller pieces: " + parts[1],
                ["nothing; it disappears", "one giant piece", "a brand-new material"], "Big objects are made of smaller pieces.")


B1 = bank([
    ("A tower is made of 8 blocks. You take it apart. How many blocks do you have?", "8", ["0", "4", "16"], "Taking apart does not make pieces disappear."),
    ("What can you make with the blocks from a tower?", "a new object, like a bridge or a car", ["nothing", "only another tower", "a bigger tower with more blocks"], "Same pieces, new shape."),
    ("Many objects are made of what?", "smaller pieces put together", ["one piece only", "air", "nothing"], "Look closely at toys and buildings."),
    ("Why can a block house become a block boat?", "The same pieces can be put together in a new way.", ["The blocks change into wood.", "New blocks appear.", "Houses turn into boats by magic."], "Rearrange the pieces."),
    ("What is the best way to find out if two buildings use the same number of blocks?", "count the blocks in each", ["see which is taller", "see which is prettier", "guess"], "Counting is evidence."),
    ("A house is made of bricks. What are the small pieces?", "bricks", ["windows only", "the yard", "the sky"], "Bricks are the pieces."),
    ("You build a train from 12 blocks, then a robot from the same blocks. The robot looks taller. How many blocks does it have?", "12", ["more than 12", "fewer than 12", "0"], "Taller does not mean more blocks."),
    ("Which shows evidence that pieces were reused?", "The new object has the same number and colors of blocks.", ["The new object is a different color.", "The new object is made of paper.", "The new object is bigger."], "Same pieces."),
])
B5 = bank([
    ("Ava weighs a block tower: 150 grams. She builds a bridge from the same blocks. What will the bridge weigh?", "150 grams", ["300 grams", "75 grams", "0 grams"], "Same pieces, same weight."),
    ("Leo has 20 blocks. He builds a house with 14. How many are left for a dog house?", "6", ["14", "20", "34"], "20 − 14 = 6."),
    ("Mia's puzzle has 24 pieces. She takes it apart and puts it back together. How many pieces?", "24", ["12", "48", "23"], "Pieces do not disappear."),
    ("Kai takes apart a toy car with 4 wheels and 1 body. He builds a wagon with all of them. How many wheels does the wagon have?", "4", ["2", "1", "8"], "The same 4 wheels."),
    ("An engineer builds a bridge from 30 beams. She takes it apart to build a tower. What should she check first?", "that all 30 beams are there", ["the color of the sky", "the weight of the tower she has not built", "nothing"], "Count the pieces."),
])


def body():
    pic = blocks_svg([shape_cells("tower", 6), shape_cells("steps", 6)], ["tower: 6", "staircase: 6"])
    ex = [("A wall has 10 blocks. You make a car with all of them. How many blocks?", ["Same pieces."], "10"),
          ("A tower weighs 100 g. You build a bridge with the same blocks. Weight?", ["Same pieces, same weight."], "100 g")]
    mist = ["Thinking a taller or bigger shape has more blocks.",
            "Thinking pieces disappear when you take something apart.",
            "Thinking the new object weighs more or less."]
    return kid_lesson(pic, "Take it apart. Build something new.",
                      ["Big things are made of small pieces.", "The same pieces can make a new shape.", "The number of pieces stays the same."], ex, mist)


def main():
    sets = U.sets([
        ("Small pieces", B1 + [(g_count, 6), (g_pieces, 6)]),
        ("Counting pieces", [(g_count, 14), (g_rebuild, 6)]),
        ("Same pieces, new shape", [(g_same, 14), (g_count, 6)]),
        ("Taking apart and rebuilding", [(g_rebuild, 12), (g_same, 8)]),
        ("Building like an engineer", B5 + [(g_rebuild, 6), (g_same, 6), (g_count, 3)]),
    ])
    make("grade-2", "building-with-small-pieces", 3, "2-PS1-3",
         "Make observations to construct an evidence-based account of how an object made of a small set of pieces can be disassembled and made into a new object.",
         "Building with Small Pieces",
         "Grade 2 Building with Small Pieces Worksheets: Take Apart and Build Again",
         "Building with Pieces",
         "Free grade 2 science worksheets on building with small pieces (NGSS 2-PS1-3): take objects apart, count the pieces and build something new. 100 picture questions with answers.",
         "Same pieces, new shape.",
         "Taking apart and rebuilding keeps the same pieces and weight.",
         body(),
         [("What does 2-PS1-3 mean?", "Objects are made of small pieces that can be taken apart and built into new objects."),
          ("Does the new object have more pieces?", "No. If you use all the same pieces, the number of pieces stays the same."),
          ("Does the weight change?", "No. The same pieces weigh the same, whatever shape you build.")],
         sets)


if __name__ == "__main__":
    main()
