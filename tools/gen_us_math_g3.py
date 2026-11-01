# -*- coding: utf-8 -*-
"""
US Grade 3 Math (Common Core) unit generator.
Writes one JSON file per unit into  content/us/math/grade-3/
  python tools/gen_us_math_g3.py
Then build SQL with:
  python tools/build_sql.py

Rules for content (so the SQL works in both MySQL and SQLite):
  - HTML attributes use single quotes  ->  no backslashes in the JSON
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-3")
UPDATED = "2026-10-31"
GREEN = "#006633"


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, rnd):
    """4 choices: correct + 3 unique distractors. Correct position is random."""
    seen = {str(correct)}
    pick = []
    for c in cands:
        s = str(c)
        if s in seen or s == "" or s.startswith("-"):
            continue
        seen.add(s)
        pick.append(s)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    choices = pick + [str(correct)]
    rnd.shuffle(choices)
    return {"q": q, "c": choices, "a": choices.index(str(correct)), "e": e}


def num_cands(x, rnd, extra=()):
    """Plausible wrong numbers near x."""
    base = list(extra) + [x + 1, x - 1, x + 2, x - 2, x + 10, x - 10, x + 5]
    rnd.shuffle(base)
    return [v for v in base if v > 0 and v != x]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def array_svg(rows, cols, size=34):
    w = cols * size + 20
    h = rows * size + 20
    dots = "".join(
        "<circle cx='%d' cy='%d' r='%d' fill='%s'/>"
        % (10 + c * size + size // 2, 10 + r * size + size // 2, size // 3, GREEN)
        for r in range(rows) for c in range(cols))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' "
            "height='%d' role='img' aria-label='array of %d rows and %d columns'>%s</svg>"
            % (w, h, w, h, rows, cols, dots))


def grid_rect_svg(w, h, cell=30):
    W = w * cell + 20
    H = h * cell + 20
    s = ["<rect x='10' y='10' width='%d' height='%d' fill='#cfe6d6' stroke='%s' "
         "stroke-width='3'/>" % (w * cell, h * cell, GREEN)]
    for i in range(1, w):
        s.append("<line x1='%d' y1='10' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (10 + i * cell, 10 + i * cell, 10 + h * cell, GREEN))
    for j in range(1, h):
        s.append("<line x1='10' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>"
                 % (10 + j * cell, 10 + w * cell, 10 + j * cell, GREEN))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' "
            "height='%d' role='img' aria-label='rectangle on a grid'>%s</svg>"
            % (W, H, W, H, "".join(s)))


def l_shape_svg(w1, h1, w2, h2, cell=26):
    """Top rectangle w1 x h1, bottom rectangle w2 x h2 (w2 > w1), left aligned."""
    W = max(w1, w2) * cell + 20
    H = (h1 + h2) * cell + 20
    s = []
    for (x0, y0, w, h) in [(0, 0, w1, h1), (0, h1, w2, h2)]:
        for i in range(w):
            for j in range(h):
                s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#cfe6d6' "
                         "stroke='%s' stroke-width='1'/>"
                         % (10 + (x0 + i) * cell, 10 + (y0 + j) * cell, cell, cell, GREEN))
    pts = [(0, 0), (w1, 0), (w1, h1), (w2, h1), (w2, h1 + h2), (0, h1 + h2)]
    poly = " ".join("%d,%d" % (10 + x * cell, 10 + y * cell) for x, y in pts)
    s.append("<polygon points='%s' fill='none' stroke='%s' stroke-width='3'/>" % (poly, GREEN))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' "
            "height='%d' role='img' aria-label='shape made of two rectangles'>%s</svg>"
            % (W, H, W, H, "".join(s)))


def number_line_svg(lo, hi, n, step=1):
    """Number line from lo to hi with a dot on n. Ticks every `step`."""
    L, R, Y = 30, 370, 50
    span = hi - lo
    def X(v):
        return L + (v - lo) * (R - L) / span
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#333' stroke-width='2'/>" % (L, Y, R, Y)]
    v = lo
    while v <= hi:
        big = (v == lo or v == hi or v == lo + span // 2)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='#333' stroke-width='%d'/>"
                 % (X(v), Y - (10 if big else 6), X(v), Y + (10 if big else 6), 2 if big else 1))
        if big:
            s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='#333' "
                     "text-anchor='middle'>%d</text>" % (X(v), Y + 30, v))
        v += step
    s.append("<circle cx='%.1f' cy='%d' r='8' fill='#c0392b'/>" % (X(n), Y))
    s.append("<text x='%.1f' y='%d' font-size='16' font-weight='800' fill='#c0392b' "
             "text-anchor='middle'>%d</text>" % (X(n), Y - 18, n))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 95' width='400' "
            "height='95' role='img' aria-label='number line from %d to %d'>%s</svg>"
            % (lo, hi, "".join(s)))


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def unit(slug, sort, **kw):
    d = {"country": "us", "subject": "math", "grade": "grade-3", "slug": slug,
         "sort": sort, "updated": UPDATED, "pdf_url": ""}
    d.update(kw)
    for s in d["sets"]:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
    return d


# ------------------------------------------------------------ strategies
def mult_tip(a, b):
    """Short strategy text for a x b (b is the 'fact family' number)."""
    p = a * b
    if b == 2:
        return "%d × 2 is a double: %d + %d = %d." % (a, a, a, p)
    if b == 5:
        return "Count by 5s %d times, or take half of %d × 10 = %d. That gives %d." % (a, a, a * 10, p)
    if b == 10:
        return "Times 10: write a zero after %d. %d × 10 = %d." % (a, a, p)
    if b == 3:
        return "Double %d, then add one more %d: %d + %d = %d." % (a, a, a * 2, a, p)
    if b == 4:
        return "Double, then double again: %d → %d → %d." % (a, a * 2, p)
    if b == 6:
        return "5 groups of %d is %d, plus 1 more group: %d + %d = %d." % (a, a * 5, a * 5, a, p)
    if b == 7:
        return "5 groups of %d is %d, plus 2 more groups (%d): %d + %d = %d." % (a, a * 5, a * 2, a * 5, a * 2, p)
    if b == 8:
        return "Double, double, double: %d → %d → %d → %d." % (a, a * 2, a * 4, p)
    if b == 9:
        return "10 × %d = %d, then take away one %d: %d − %d = %d." % (a, a * 10, a, a * 10, a, p)
    return "%d × %d = %d." % (a, b, p)


def mult_cands(a, b, rnd):
    p = a * b
    c = [a * (b + 1), a * (b - 1), (a + 1) * b, (a - 1) * b, a + b, p + 10, p - 10, p + 1, p + 2]
    rnd.shuffle(c)
    return c


# ============================================================ UNIT 1
def gen_multiplication():
    rnd = random.Random(31)
    sets = []

    # Set 1: arrays
    items = []
    pairs = [(r, c) for r in range(2, 6) for c in range(2, 8) if r != c]
    rnd.shuffle(pairs)
    for i, (r, c) in enumerate(pairs[:20]):
        svg = fig(array_svg(r, c))
        if i % 2 == 0:
            items.append(mcq(svg + "How many dots are in this array?", r * c,
                             mult_cands(r, c, rnd) + [r + c],
                             "%d rows with %d dots in each row: %d × %d = %d." % (r, c, r, c, r * c), rnd))
        else:
            right = "%d × %d" % (r, c)
            wrong = ["%d + %d" % (r, c), "%d × %d" % (r, c + 1), "%d × %d" % (r + 1, c),
                     "%d × %d" % (r - 1, c), "%d + %d" % (r * c, r)]
            items.append(mcq(svg + "Which multiplication matches this array?", right, wrong,
                             "There are %d rows and %d dots in each row, so the array shows %d × %d = %d."
                             % (r, c, r, c, r * c), rnd))
    sets.append({"title": "Arrays and equal groups", "items": items})

    def fact_set(title, bs):
        its = []
        combos = [(a, b) for b in bs for a in range(1, 11)]
        rnd.shuffle(combos)
        for a, b in combos[:20]:
            x, y = (a, b) if rnd.random() < 0.5 else (b, a)
            its.append(mcq("%d × %d = ?" % (x, y), a * b, mult_cands(a, b, rnd),
                           mult_tip(a, b), rnd))
        return {"title": title, "items": its}

    sets.append(fact_set("Facts: × 2, × 5, × 10", [2, 5, 10]))
    sets.append(fact_set("Facts: × 3, × 4, × 6", [3, 4, 6]))
    sets.append(fact_set("Facts: × 7, × 8, × 9", [7, 8, 9]))

    # Set 5: missing factors + word problems
    its = []
    for _ in range(10):
        a, b = rnd.randint(2, 9), rnd.randint(3, 9)
        p = a * b
        its.append(mcq("%d × ? = %d" % (a, p), b, num_cands(b, rnd, [b + 1, b - 1, p - a, a]),
                       "Ask: %d times what number makes %d? %d × %d = %d, so the missing number is %d."
                       % (a, p, a, b, p, b), rnd))
    stories = [
        ("There are %d bags with %d apples in each bag. How many apples are there in all?", "apples"),
        ("A garden has %d rows with %d plants in each row. How many plants are there?", "plants"),
        ("%d friends each have %d stickers. How many stickers do they have altogether?", "stickers"),
        ("A box holds %d packs of crayons. Each pack has %d crayons. How many crayons are in the box?", "crayons"),
        ("There are %d tables with %d chairs at each table. How many chairs are there?", "chairs"),
    ]
    for i in range(10):
        a, b = rnd.randint(3, 9), rnd.randint(3, 9)
        t, noun = stories[i % len(stories)]
        its.append(mcq(t % (a, b), "%d %s" % (a * b, noun),
                       ["%d %s" % (v, noun) for v in [a + b, a * (b + 1), (a - 1) * b, a * b + 10] if v >= 2],
                       "Equal groups mean multiply: %d × %d = %d %s." % (a, b, a * b, noun), rnd))
    sets.append({"title": "Missing factors and word problems", "items": its})

    body = (
        "<h2>What multiplication means</h2>"
        "<p>Multiplication is a fast way to add <b>equal groups</b>. <b>4 × 3</b> means 4 groups of 3, "
        "which is 3 + 3 + 3 + 3 = 12. An <b>array</b> shows the same idea with rows and columns.</p>"
        "<figure class='sn-fig'>" + array_svg(4, 3, 40) +
        "<figcaption>4 rows with 3 dots in each row: 4 × 3 = 12. Turn it sideways and you get 3 × 4 = 12. "
        "The order of the factors does not change the product.</figcaption></figure>"
        "<h2>Strategies for every fact family</h2>" +
        table(["Facts", "Strategy", "Example"], [
            ["× 2", "Double the number", "7 × 2 = 7 + 7 = 14"],
            ["× 3", "Double, then add one more group", "6 × 3 = 12 + 6 = 18"],
            ["× 4", "Double, then double again", "7 × 4: 14, then 28"],
            ["× 5", "Half of × 10", "8 × 5 = half of 80 = 40"],
            ["× 6", "× 5, then add one more group", "7 × 6 = 35 + 7 = 42"],
            ["× 7", "× 5 plus × 2", "8 × 7 = 40 + 16 = 56"],
            ["× 8", "Double three times", "6 × 8: 12, 24, 48"],
            ["× 9", "× 10, then take one group away", "7 × 9 = 70 − 7 = 63"],
            ["× 10", "Write a zero at the end", "6 × 10 = 60"],
        ]) +
        ex("Example", "6 × 7 = ?", "5 × 7 = 35. One more group of 7: 35 + 7 = 42.", "42") +
        ex("Example 2", "9 × 8 = ?", "10 × 8 = 80. Take away one group of 8: 80 − 8 = 72.", "72") +
        ex("Word problem", "There are 5 boxes with 6 pencils in each box. How many pencils?",
           "5 equal groups of 6: 5 × 6 = 30.", "30 pencils") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the two numbers (6 × 4 = 10)", "Multiply means equal groups: 6 groups of 4 = 24"],
            ["Mixing up neighbors (7 × 8 = 54)", "Use a strategy: 7 × 8 = 40 + 16 = 56"],
            ["Thinking 0 × 5 = 5", "Zero groups of anything is 0"],
            ["Thinking 1 × 9 = 1", "One group of 9 is 9"],
        ])
    )
    faq = [
        {"q": "What multiplication facts should a 3rd grader know?",
         "a": "By the end of Grade 3, students are expected to know all products of two one-digit numbers from memory, from 0 × 0 up to 9 × 9 (and the ×10 facts)."},
        {"q": "What is the best order to learn the times tables?",
         "a": "Start with × 2, × 5 and × 10, then × 3, × 4 and × 6, and finish with × 7, × 8 and × 9. Each set builds on the strategies from the one before."},
        {"q": "Why does 4 × 3 equal 3 × 4?",
         "a": "An array of 4 rows of 3 is the same array as 3 columns of 4 turned sideways. This is the commutative property, and it cuts the number of facts to learn almost in half."},
        {"q": "How can I practice multiplication facts at home?",
         "a": "Do one 20-question set a day, redo only the questions you missed, and print the worksheet for a timed check once a week."},
    ]
    return unit("multiplication-facts", 1,
                title="Multiplication Facts 0–10",
                seo_title="Grade 3 Multiplication Facts Worksheets (Times Tables 0–10)",
                short_title="Multiplication facts",
                domain="Operations and Algebraic Thinking",
                standard_code="3.OA.C.7",
                standard_url="https://www.thecorestandards.org/Math/Content/3/OA/C/7/",
                standard_text="Multiply within 100 fluently and know all products of two one-digit numbers from memory.",
                meta_desc="Free Grade 3 multiplication facts worksheets: arrays, times tables 0–10 with a strategy for every fact family, missing factors and word problems. 100 practice questions with instant feedback and a printable answer key.",
                key_big="Multiplication = equal groups. Learn × 2, × 5, × 10 first, then use them to find the rest.",
                key_sub="Every hard fact comes from an easy one: × 6 is × 5 plus one more group, and × 9 is × 10 minus one group. Know the strategy, and you never have to guess.",
                body_html=body, faq=faq, sets=sets)


# ============================================================ UNIT 2
def gen_division():
    rnd = random.Random(32)
    sets = []
    its = []
    stories = [
        ("%d cookies are shared equally among %d kids. How many cookies does each kid get?", "cookies"),
        ("%d students sit in %d equal rows. How many students are in each row?", "students"),
        ("A baker puts %d muffins into %d boxes with the same number in each box. How many muffins go in each box?", "muffins"),
        ("%d pencils are packed into %d equal packs. How many pencils are in each pack?", "pencils"),
    ]
    for i in range(20):
        d, q = rnd.randint(2, 9), rnd.randint(2, 9)
        p = d * q
        t, noun = stories[i % len(stories)]
        its.append(mcq(t % (p, d), "%d %s" % (q, noun),
                       ["%d %s" % (v, noun) for v in [q + 1, q - 1, p - d, d, q + 2, q + 3, q * 2 + 1] if v >= 2],
                       "%d ÷ %d = %d, because %d × %d = %d." % (p, d, q, d, q, p), rnd))
    sets.append({"title": "Sharing equally", "items": its})

    def fact_set(title, ds):
        out = []
        combos = [(q, d) for d in ds for q in range(1, 11)]
        rnd.shuffle(combos)
        for q, d in combos[:20]:
            p = q * d
            out.append(mcq("%d ÷ %d = ?" % (p, d), q,
                           num_cands(q, rnd, [q + 1, q - 1, d, p - d]),
                           "Think multiplication: %d × ? = %d. %d × %d = %d, so %d ÷ %d = %d."
                           % (d, p, d, q, p, p, d, q), rnd))
        return {"title": title, "items": out}

    sets.append(fact_set("Facts: ÷ 2, ÷ 5, ÷ 10", [2, 5, 10]))
    sets.append(fact_set("Facts: ÷ 3, ÷ 4, ÷ 6", [3, 4, 6]))
    sets.append(fact_set("Facts: ÷ 7, ÷ 8, ÷ 9", [7, 8, 9]))

    its = []
    for _ in range(10):
        a, b = rnd.randint(3, 9), rnd.randint(3, 9)
        if a == b:
            b = a + 1 if a < 9 else a - 1
        p = a * b
        right = "%d ÷ %d = %d" % (p, b, a)
        wrong = ["%d ÷ %d = %d" % (p, a, a), "%d ÷ %d = %d" % (b, p, a),
                 "%d ÷ %d = %d" % (p + a, b, a), "%d ÷ %d = %d" % (p, b, b)]
        its.append(mcq("Which division fact is in the same fact family as %d × %d = %d?" % (a, b, p),
                       right, wrong,
                       "The fact family of %d, %d and %d: %d × %d = %d, %d × %d = %d, %d ÷ %d = %d, %d ÷ %d = %d."
                       % (a, b, p, a, b, p, b, a, p, p, b, a, p, a, b), rnd))
    for _ in range(10):
        d, q = rnd.randint(2, 9), rnd.randint(2, 9)
        p = d * q
        its.append(mcq("? ÷ %d = %d" % (d, q), p, num_cands(p, rnd, [d + q, p + d, p - d, q]),
                       "The missing number is the total. %d × %d = %d, so %d ÷ %d = %d."
                       % (d, q, p, p, d, q), rnd))
    sets.append({"title": "Fact families and missing numbers", "items": its})

    body = (
        "<h2>What division means</h2>"
        "<p>Division splits a total into <b>equal groups</b>. <b>12 ÷ 3</b> can mean "
        "“share 12 into 3 equal groups” (4 in each group) or “how many groups of 3 are in 12?” (4 groups).</p>"
        "<figure class='sn-fig'>" + array_svg(3, 4, 40) +
        "<figcaption>12 dots in 3 equal rows: 12 ÷ 3 = 4. The same array shows 3 × 4 = 12.</figcaption></figure>"
        "<h2>Use multiplication to divide</h2>"
        "<p>Every division fact has a <b>multiplication partner</b>. To solve 56 ÷ 8, ask: "
        "<b>8 times what is 56?</b> Since 8 × 7 = 56, the answer is 7.</p>" +
        table(["Fact family", "Multiplication", "Division"], [
            ["3, 4, 12", "3 × 4 = 12 &nbsp; 4 × 3 = 12", "12 ÷ 3 = 4 &nbsp; 12 ÷ 4 = 3"],
            ["6, 7, 42", "6 × 7 = 42 &nbsp; 7 × 6 = 42", "42 ÷ 6 = 7 &nbsp; 42 ÷ 7 = 6"],
            ["8, 9, 72", "8 × 9 = 72 &nbsp; 9 × 8 = 72", "72 ÷ 8 = 9 &nbsp; 72 ÷ 9 = 8"],
        ]) +
        ex("Example", "48 ÷ 6 = ?", "Ask: 6 × ? = 48. 6 × 8 = 48.", "8") +
        ex("Word problem", "24 stickers are shared equally by 4 friends. How many does each friend get?",
           "24 ÷ 4 = ? → 4 × 6 = 24.", "6 stickers") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Switching the order (3 ÷ 12)", "Start with the total: 12 ÷ 3"],
            ["Subtracting instead (12 ÷ 3 = 9)", "Division is equal groups, not taking away once"],
            ["Thinking 5 ÷ 1 = 1", "One group gets all 5: 5 ÷ 1 = 5"],
            ["Dividing by 0", "You cannot divide by 0"],
        ])
    )
    faq = [
        {"q": "How do you explain division to a 3rd grader?",
         "a": "Use equal sharing: 15 cookies shared by 3 friends gives each friend 5. Then connect it to multiplication: 3 × 5 = 15."},
        {"q": "What is a fact family?",
         "a": "A fact family is a set of three numbers linked by two multiplication facts and two division facts, such as 4 × 6 = 24, 6 × 4 = 24, 24 ÷ 4 = 6 and 24 ÷ 6 = 4."},
        {"q": "Should kids memorize division facts separately?",
         "a": "No. If a child knows the multiplication facts, each division fact is just the matching multiplication fact read backward."},
    ]
    return unit("division-facts", 2,
                title="Division Facts Within 100",
                seo_title="Grade 3 Division Facts Worksheets (Fact Families & Word Problems)",
                short_title="Division facts",
                domain="Operations and Algebraic Thinking",
                standard_code="3.OA.C.7",
                standard_url="https://www.thecorestandards.org/Math/Content/3/OA/C/7/",
                standard_text="Divide within 100 fluently, using the relationship between multiplication and division.",
                meta_desc="Free Grade 3 division worksheets: equal sharing, division facts ÷2 to ÷10, fact families and missing numbers. 100 practice questions with step-by-step hints and a printable answer key.",
                key_big="To divide, think multiplication: 56 ÷ 8 = ? means 8 × ? = 56.",
                key_sub="Division splits a total into equal groups. If you know your times tables, you already know your division facts.",
                body_html=body, faq=faq, sets=sets)


# ============================================================ UNIT 3
def round_to(n, p):
    return ((n + p // 2) // p) * p


def gen_rounding():
    rnd = random.Random(33)
    sets = []

    its = []
    nums = rnd.sample([n for n in range(11, 99) if n % 10 != 0], 20)
    for i, n in enumerate(nums):
        lo = n // 10 * 10
        r = round_to(n, 10)
        other = lo + 10 if r == lo else lo
        q = "Round %d to the nearest ten." % n
        if i < 10:
            q = fig(number_line_svg(lo, lo + 10, n)) + q
        e = ("%d is between %d and %d. The ones digit is %d, so round %s to %d."
             % (n, lo, lo + 10, n % 10, "up" if r > lo else "down", r))
        its.append(mcq(q, r, [other, n, r + 10, r - 10, 100], e, rnd))
    sets.append({"title": "Nearest ten (2-digit numbers)", "items": its})

    its = []
    nums = rnd.sample([n for n in range(101, 999) if n % 10 != 0], 20)
    for n in nums:
        lo = n // 10 * 10
        r = round_to(n, 10)
        other = lo + 10 if r == lo else lo
        e = ("Look at the ones digit: %d. %s, so %d rounds to %d."
             % (n % 10, "5 or more rounds up" if n % 10 >= 5 else "Less than 5 rounds down", n, r))
        its.append(mcq("Round %d to the nearest ten." % n, r,
                       [other, round_to(n, 100), r + 10, r - 10, n, r + 100], e, rnd))
    sets.append({"title": "Nearest ten (3-digit numbers)", "items": its})

    its = []
    nums = rnd.sample([n for n in range(110, 990) if n % 100 != 0 and n % 10 != 0], 20)
    for n in nums:
        lo = n // 100 * 100
        r = round_to(n, 100)
        other = lo + 100 if r == lo else lo
        tens = (n // 10) % 10
        e = ("Look at the tens digit: %d. %s, so %d rounds to %d."
             % (tens, "5 or more rounds up" if tens >= 5 else "Less than 5 rounds down", n, r))
        its.append(mcq("Round %d to the nearest hundred." % n, r,
                       [other, round_to(n, 10), r + 100, r - 100, n, r + 200], e, rnd))
    sets.append({"title": "Nearest hundred", "items": its})

    its = []
    for _ in range(8):
        lo = rnd.randint(1, 9) * 10 if rnd.random() < .5 else rnd.randint(11, 98) * 10
        n = lo + 5
        r = lo + 10
        its.append(mcq("Round %d to the nearest ten." % n, r, [lo, n, r + 10, lo - 10],
                       "The ones digit is 5. A 5 always rounds up, so %d rounds to %d." % (n, r), rnd))
    for _ in range(4):
        lo = rnd.randint(1, 8) * 100
        n = lo + 50 + rnd.randint(0, 9)
        r = lo + 100
        its.append(mcq("Round %d to the nearest hundred." % n, r, [lo, round_to(n, 10), r + 100, n],
                       "The tens digit is 5, so round up: %d rounds to %d." % (n, r), rnd))
    for _ in range(8):
        t = rnd.randint(2, 9) * 10
        right = t + rnd.choice([-5, -4, -3, -2, 1, 2, 3, 4])
        wrong = [t - 6, t + 5, t + 7, t - 8, t + 9, t - 11]
        rnd.shuffle(wrong)
        its.append(mcq("Which number rounds to %d when rounded to the nearest ten?" % t, right, wrong,
                       "Numbers from %d to %d round to %d. %d is in that range." % (t - 5, t + 4, t, right), rnd))
    rnd.shuffle(its)
    sets.append({"title": "The 5 rule and which numbers round", "items": its})

    its = []
    for i in range(20):
        if i % 2 == 0:
            a, b = rnd.randint(12, 89), rnd.randint(12, 89)
            ra, rb = round_to(a, 10), round_to(b, 10)
            est = ra + rb
            its.append(mcq("Estimate by rounding each number to the nearest ten: %d + %d" % (a, b), est,
                           [a + b, est + 10, est - 10, est + 20],
                           "%d rounds to %d and %d rounds to %d. %d + %d = %d." % (a, ra, b, rb, ra, rb, est), rnd))
        else:
            a, b = rnd.randint(120, 890), rnd.randint(110, 480)
            if b > a:
                a, b = b, a
            ra, rb = round_to(a, 100), round_to(b, 100)
            est = ra - rb
            if est <= 0:
                a += 300
                ra = round_to(a, 100)
                est = ra - rb
            its.append(mcq("Estimate by rounding each number to the nearest hundred: %d − %d" % (a, b), est,
                           [a - b, est + 100, est - 100, est + 200],
                           "%d rounds to %d and %d rounds to %d. %d − %d = %d." % (a, ra, b, rb, ra, rb, est), rnd))
    sets.append({"title": "Estimate sums and differences", "items": its})

    body = (
        "<h2>What rounding means</h2>"
        "<p>Rounding finds the <b>closest</b> ten or hundred. It makes numbers easier to add and subtract "
        "in your head, and it helps you check whether an answer makes sense.</p>"
        "<figure class='sn-fig'>" + number_line_svg(40, 50, 47) +
        "<figcaption>47 is closer to 50 than to 40, so 47 rounds to 50.</figcaption></figure>"
        "<h2>The rounding rule</h2>"
        "<ol class='rk-step'><li>Find the digit in the place you are rounding to.</li>"
        "<li>Look at the digit <b>one place to the right</b>.</li>"
        "<li><b>5 or more</b>: round up. <b>4 or less</b>: round down.</li>"
        "<li>Change every digit after the rounding place to 0.</li></ol>" +
        table(["Number", "Nearest ten", "Nearest hundred"], [
            ["63", "60", "100"], ["245", "250", "200"], ["378", "380", "400"], ["850", "850", "900"],
        ]) +
        ex("Example", "Round 365 to the nearest hundred.",
           "The hundreds digit is 3. Look right: the tens digit is 6 (5 or more), so round up.", "400") +
        ex("Estimate", "About how much is 48 + 33?",
           "48 rounds to 50 and 33 rounds to 30. 50 + 30 = 80.", "about 80") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Looking at the wrong digit", "Always look one place to the right of the rounding place"],
            ["Rounding 45 down to 40", "5 rounds up: 45 → 50"],
            ["Writing 368 → 370 for nearest hundred", "Nearest hundred ends in 00: 368 → 400"],
        ])
    )
    faq = [
        {"q": "How do you teach rounding to the nearest ten?",
         "a": "Put the number on a number line between two tens and ask which ten it is closer to. Once that makes sense, teach the shortcut: look at the ones digit, 5 or more rounds up."},
        {"q": "Why does 5 round up?",
         "a": "A number ending in 5 is exactly halfway between two tens. Mathematicians agreed to round it up so everyone gets the same answer."},
        {"q": "Why do 3rd graders learn rounding?",
         "a": "Rounding is used to estimate. Estimating an answer first is the quickest way to catch a mistake in addition, subtraction and later in multiplication."},
    ]
    return unit("rounding", 3,
                title="Rounding to the Nearest 10 and 100",
                seo_title="Grade 3 Rounding Worksheets: Nearest 10 and 100 (with Number Lines)",
                short_title="Rounding to 10 and 100",
                domain="Number and Operations in Base Ten",
                standard_code="3.NBT.A.1",
                standard_url="https://www.thecorestandards.org/Math/Content/3/NBT/A/1/",
                standard_text="Use place value understanding to round whole numbers to the nearest 10 or 100.",
                meta_desc="Free Grade 3 rounding worksheets: round to the nearest 10 and 100 with number lines, the 5 rule, and estimating sums and differences. 100 practice questions with answers.",
                key_big="Look one place to the right. 5 or more: round up. 4 or less: round down.",
                key_sub="Rounding finds the closest ten or hundred. A number ending in 5 is exactly halfway, and it always rounds up.",
                body_html=body, faq=faq, sets=sets)


# ============================================================ UNIT 4
def gen_area():
    rnd = random.Random(34)
    sets = []

    its = []
    combos = [(w, h) for w in range(2, 8) for h in range(2, 6)]
    rnd.shuffle(combos)
    for w, h in combos[:20]:
        a, p = w * h, 2 * (w + h)
        its.append(mcq(fig(grid_rect_svg(w, h)) + "Each small square is 1 square unit. What is the area of the rectangle?",
                       "%d square units" % a,
                       ["%d square units" % v for v in [p, a + w, a - h, w + h, a + 1]],
                       "Count the squares: %d rows of %d. %d × %d = %d square units." % (h, w, h, w, a), rnd))
    sets.append({"title": "Count the unit squares", "items": its})

    its = []
    units = [("cm", "sq cm"), ("in", "sq in"), ("m", "sq m"), ("ft", "sq ft")]
    for i in range(20):
        L, W = rnd.randint(3, 10), rnd.randint(2, 9)
        if L == W:
            L += 1
        u, su = units[i % 4]
        a = L * W
        its.append(mcq("A rectangle is %d %s long and %d %s wide. What is its area?" % (L, u, W, u),
                       "%d %s" % (a, su),
                       ["%d %s" % (v, su) for v in [2 * (L + W), L + W, a + L, a - W]],
                       "Area = length × width = %d × %d = %d %s." % (L, W, a, su), rnd))
    sets.append({"title": "Length × width", "items": its})

    its = []
    stories = [
        ("A bedroom floor is %d feet long and %d feet wide. How many square feet of carpet cover the floor?", "sq ft"),
        ("A garden bed is %d meters long and %d meters wide. What is the area of the garden bed?", "sq m"),
        ("A poster is %d inches tall and %d inches wide. What is the area of the poster?", "sq in"),
        ("A patio is made of square tiles: %d rows with %d tiles in each row. Each tile is 1 square foot. What is the area?", "sq ft"),
        ("A sheet of paper is cut into a rectangle %d cm by %d cm. What is its area?", "sq cm"),
    ]
    for i in range(20):
        L, W = rnd.randint(4, 10), rnd.randint(3, 9)
        t, su = stories[i % len(stories)]
        a = L * W
        its.append(mcq(t % (L, W), "%d %s" % (a, su),
                       ["%d %s" % (v, su) for v in [2 * (L + W), L + W, a + 10, a - L]],
                       "Multiply the two side lengths: %d × %d = %d %s." % (L, W, a, su), rnd))
    sets.append({"title": "Area word problems", "items": its})

    its = []
    for i in range(20):
        L, W = rnd.randint(3, 10), rnd.randint(2, 9)
        a = L * W
        u, su = units[i % 4]
        its.append(mcq("A rectangle has an area of %d %s. One side is %d %s long. How long is the other side?"
                       % (a, su, L, u), "%d %s" % (W, u),
                       ["%d %s" % (v, u) for v in [W + 1, W - 1, a - L, a + L, W + 2]],
                       "Think: %d × ? = %d. %d × %d = %d, so the other side is %d %s."
                       % (L, a, L, W, a, W, u), rnd))
    sets.append({"title": "Find the missing side", "items": its})

    its = []
    for i in range(10):
        w1 = rnd.randint(2, 3)
        w2 = rnd.randint(w1 + 2, 6)
        h1, h2 = rnd.randint(2, 3), rnd.randint(2, 3)
        a = w1 * h1 + w2 * h2
        its.append(mcq(fig(l_shape_svg(w1, h1, w2, h2)) +
                       "Each square is 1 square unit. What is the area of the whole shape?",
                       "%d square units" % a,
                       ["%d square units" % v for v in [a + w1, a - h2, w2 * (h1 + h2), a + 2]],
                       "Split it into two rectangles: %d × %d = %d and %d × %d = %d. %d + %d = %d square units."
                       % (w1, h1, w1 * h1, w2, h2, w2 * h2, w1 * h1, w2 * h2, a), rnd))
    for i in range(10):
        a1, b1, a2, b2 = rnd.randint(2, 6), rnd.randint(2, 5), rnd.randint(3, 8), rnd.randint(2, 5)
        A = a1 * b1 + a2 * b2
        its.append(mcq("A shape is made of two rectangles. One is %d m by %d m. The other is %d m by %d m. "
                       "What is the total area?" % (a1, b1, a2, b2),
                       "%d sq m" % A,
                       ["%d sq m" % v for v in [a1 + b1 + a2 + b2, (a1 + a2) * (b1 + b2), A + 10, A - a1]],
                       "%d × %d = %d and %d × %d = %d. Add them: %d + %d = %d sq m."
                       % (a1, b1, a1 * b1, a2, b2, a2 * b2, a1 * b1, a2 * b2, A), rnd))
    rnd.shuffle(its)
    sets.append({"title": "Shapes made of rectangles", "items": its})

    body = (
        "<h2>What area means</h2>"
        "<p>Area is the amount of space <b>inside</b> a flat shape. We measure it by counting "
        "<b>square units</b>: squares that are 1 unit on each side.</p>"
        "<figure class='sn-fig'>" + grid_rect_svg(5, 3, 40) +
        "<figcaption>3 rows of 5 squares: 3 × 5 = 15 square units. Multiplying is faster than counting one by one.</figcaption></figure>"
        "<h2>Area of a rectangle</h2>"
        "<p><b>Area = length × width.</b> Write the answer in square units: sq cm, sq in, sq m or sq ft.</p>" +
        table(["Shape", "How to find the area", "Area"], [
            ["4 cm by 6 cm", "4 × 6", "24 sq cm"],
            ["7 ft by 3 ft", "7 × 3", "21 sq ft"],
            ["Area 32, one side 8", "8 × ? = 32", "other side 4"],
        ]) +
        ex("Example", "A rug is 6 feet long and 4 feet wide. What is its area?", "6 × 4 = 24.", "24 sq ft") +
        "<h2>Shapes made of rectangles</h2>"
        "<figure class='sn-fig'>" + l_shape_svg(2, 2, 5, 3, 32) +
        "<figcaption>Split the shape into two rectangles: 2 × 2 = 4 and 5 × 3 = 15. Total area: 4 + 15 = 19 square units.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding the sides (4 + 6 = 10)", "Area multiplies: 4 × 6 = 24"],
            ["Finding the perimeter instead", "Perimeter is the distance around. Area is the space inside"],
            ["Writing cm instead of sq cm", "Area is always in square units"],
        ])
    )
    faq = [
        {"q": "What is the difference between area and perimeter?",
         "a": "Area is the space inside a shape, measured in square units. Perimeter is the distance around the outside, measured in units of length."},
        {"q": "How do you find the area of a rectangle in 3rd grade?",
         "a": "Count the unit squares, or multiply the length by the width. A 4 by 6 rectangle has 4 × 6 = 24 square units."},
        {"q": "How do you find the area of an L-shaped figure?",
         "a": "Split it into two rectangles, find the area of each, and add the two areas together."},
    ]
    return unit("area", 4,
                title="Area of Rectangles",
                seo_title="Grade 3 Area Worksheets: Unit Squares, Length × Width and Composite Shapes",
                short_title="Area",
                domain="Measurement and Data",
                standard_code="3.MD.C.7",
                standard_url="https://www.thecorestandards.org/Math/Content/3/MD/C/7/",
                standard_text="Relate area to multiplication and addition: find areas of rectangles and of shapes made from rectangles.",
                meta_desc="Free Grade 3 area worksheets: count unit squares, length × width, word problems, missing sides and L-shaped figures. 100 practice questions with pictures and a printable answer key.",
                key_big="Area of a rectangle = length × width, in square units.",
                key_sub="Area is the space inside a shape. Count the unit squares, or multiply the side lengths. For an L shape, split it into rectangles and add.",
                body_html=body, faq=faq, sets=sets)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for u in [gen_multiplication(), gen_division(), gen_rounding(), gen_area()]:
        path = os.path.join(OUT, u["slug"] + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(u, f, ensure_ascii=False, indent=1)
        print("wrote", path)
