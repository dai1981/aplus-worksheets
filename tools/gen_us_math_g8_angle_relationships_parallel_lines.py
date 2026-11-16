# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Angles with Parallel Lines and Triangles (8.G.A.5)
  python3 tools/gen_us_math_g8_angle_relationships_parallel_lines.py
Parallel lines cut by a transversal (corresponding, alternate interior, alternate exterior, same-side
interior and vertical angles), the triangle angle sum, the exterior angle theorem, and equations with
angles. Wrong answers come from real mistakes: using 180 − x when the angles are equal, using x when
they add to 180, adding the remote angles wrongly, and using 360 for a triangle.
"""
import random
from ws_common import mcq, balance, B, table, example, write_unit, fig, svg_wrap, text, line, INK, RED, BLUE, GREEN

R = random.Random(81301)
UPDATED = "2026-11-16"
# angles 2, 3, 6, 7 are the acute angle t; 1, 4, 5, 8 are 180 − t
ACUTE = {2, 3, 6, 7}
PAIRS = {
    frozenset({1, 5}): "corresponding", frozenset({2, 6}): "corresponding", frozenset({3, 7}): "corresponding", frozenset({4, 8}): "corresponding",
    frozenset({3, 6}): "alternate interior", frozenset({4, 5}): "alternate interior",
    frozenset({1, 8}): "alternate exterior", frozenset({2, 7}): "alternate exterior",
    frozenset({3, 5}): "same-side interior", frozenset({4, 6}): "same-side interior",
    frozenset({1, 4}): "vertical", frozenset({2, 3}): "vertical", frozenset({5, 8}): "vertical", frozenset({6, 7}): "vertical",
    frozenset({1, 2}): "a linear pair", frozenset({3, 4}): "a linear pair", frozenset({5, 6}): "a linear pair", frozenset({7, 8}): "a linear pair",
    frozenset({1, 3}): "a linear pair", frozenset({2, 4}): "a linear pair", frozenset({5, 7}): "a linear pair", frozenset({6, 8}): "a linear pair",
}


def par_svg(show=None):
    """Two parallel lines (arrows) and a transversal with angles 1-8. show: {n: text} labels instead of numbers."""
    W, H = 300, 210
    s = [line(20, 60, 280, 60, INK, 2.2), line(20, 150, 280, 150, INK, 2.2),
         "<path d='M266 54 L276 60 L266 66' fill='none' stroke='%s' stroke-width='2'/>" % INK,
         "<path d='M266 144 L276 150 L266 156' fill='none' stroke='%s' stroke-width='2'/>" % INK,
         line(95, 200, 215, 10, BLUE, 2.4)]
    # intersections: top at x where y=60, bottom where y=150
    def xat(y):
        return 95 + (200 - y) * (120 / 190)
    pos = {1: (-22, -10), 2: (20, -10), 3: (-22, 20), 4: (20, 20)}
    for k, y in [(0, 60), (4, 150)]:
        x = xat(y)
        for n in range(1, 5):
            dx, dy = pos[n]
            lab = str(n + k)
            if show is not None:
                lab = show.get(n + k, "")
            if lab:
                s.append(text(x + dx, y + dy, lab, 14, col=RED if lab in ("?",) or not lab.isdigit() else GREEN))
    return svg_wrap(W, H, "".join(s), "two parallel lines cut by a transversal")


def val(n, t):
    return t if n in ACUTE else 180 - t


# ============================================================ set 1: name the pair
def set_names():
    its = []
    names = ["corresponding", "alternate interior", "alternate exterior", "same-side interior", "vertical", "a linear pair"]
    for a, b in [(1, 5), (3, 6), (2, 7), (4, 6), (1, 4), (2, 6), (4, 5), (1, 8), (3, 5), (5, 8), (3, 7), (6, 7), (4, 8), (7, 8)]:
        nm = PAIRS[frozenset({a, b})]
        q = fig(par_svg()) + "What kind of angles are ∠%d and ∠%d?" % (a, b)
        why = {"corresponding": "They are in the same position at each crossing.",
               "alternate interior": "They are between the parallel lines, on opposite sides of the transversal.",
               "alternate exterior": "They are outside the parallel lines, on opposite sides of the transversal.",
               "same-side interior": "They are between the parallel lines, on the same side of the transversal.",
               "vertical": "They are opposite each other at the same crossing.",
               "a linear pair": "They sit next to each other on a straight line."}[nm]
        wr = [x for x in names if x != nm]
        R.shuffle(wr)
        its.append(mcq(q, (nm.capitalize(), nm), [(w.capitalize(), w) for w in wr], why + " <b>%s</b>." % nm.capitalize()))
    for q, ans, wr, e in [
        ("Corresponding angles on parallel lines are …", "equal", ["supplementary (add to 180°)", "complementary (add to 90°)", "always 90°"],
         "Corresponding angles are <b>equal</b>."),
        ("Alternate interior angles on parallel lines are …", "equal", ["supplementary (add to 180°)", "always 45°", "different"],
         "Alternate interior angles are <b>equal</b>."),
        ("Same-side interior angles on parallel lines are …", "supplementary (add to 180°)", ["equal", "complementary (add to 90°)", "always 90°"],
         "Same-side interior angles <b>add to 180°</b>."),
        ("Vertical angles are …", "always equal", ["always 90°", "supplementary", "equal only if the lines are parallel"],
         "Vertical angles are <b>always equal</b>, even without parallel lines."),
        ("What is a transversal?", "A line that crosses two or more lines", ["A line that never crosses another line", "A curved line", "A line inside a triangle"],
         "A transversal is <b>a line that crosses two or more lines</b>."),
        ("When are corresponding angles equal?", "When the two lines are parallel", ["Always", "Only when the transversal is vertical", "Never"],
         "The angle rules need parallel lines: <b>when the two lines are parallel</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[14], o[1], o[15], o[2], o[16], o[3], o[17], o[4], o[18], o[5], o[19], o[6], o[7], o[8], o[9], o[10],
             o[11], o[12], o[13]]
    return {"title": "Name the angle pair", "items": order}


# ============================================================ set 2: find the angle
def set_find():
    its = []
    for given, t, ask in [(2, 65, 6), (1, 115, 5), (3, 70, 6), (4, 110, 5), (2, 50, 7), (1, 130, 8), (3, 55, 5), (4, 125, 6),
                          (6, 72, 2), (5, 108, 4), (7, 40, 2), (8, 140, 1), (2, 80, 3), (5, 100, 8), (6, 63, 4), (7, 35, 5),
                          (1, 120, 7), (3, 48, 8), (2, 75, 5), (8, 150, 6)]:
        t = t if given in ACUTE else 180 - t       # t in the list is the size of the given angle
        g = val(given, t)
        a = val(ask, t)
        q = fig(par_svg()) + "The lines are parallel and ∠%d = %d°. What is ∠%d?" % (given, g, ask)
        rel = PAIRS.get(frozenset({given, ask}))
        if a == g:
            e = "∠%d and ∠%d are equal%s. ∠%d = <b>%d°</b>." % (given, ask, " (%s angles)" % rel if rel and rel not in ("a linear pair",) else "", ask, a)
        else:
            e = "∠%d and ∠%d add to 180°%s. ∠%d = 180° − %d° = <b>%d°</b>." % (given, ask, " (%s)" % rel if rel else "", ask, g, a)
        wr = [180 - a, 90 - a if a < 90 else a - 90, 360 - a, a + 10]
        its.append(mcq(q, ("%d°" % a, a), [("%d°" % w, w) for w in wr if w > 0], e))
    return {"title": "Find the angle", "items": its}


# ============================================================ set 3: triangles
def tri_svg(labels):
    """A triangle with angle labels at A (bottom-left), B (bottom-right), C (top) and an exterior angle at B if given."""
    W, H = 300, 190
    A, Bp, C = (30, 160), (220, 160), (110, 30)
    s = ["<polygon points='30,160 220,160 110,30' fill='#cfe6d6' stroke='#006633' stroke-width='2.2'/>"]
    if "ext" in labels:
        s.append(line(220, 160, 285, 160, INK, 2.2))
        s.append(text(250, 150, labels["ext"], 14, col=RED if "?" in labels["ext"] or "x" in labels["ext"] else INK))
    for key, (x, y) in {"A": (58, 152), "B": (196, 152), "C": (112, 62)}.items():
        if key in labels:
            t = labels[key]
            s.append(text(x, y, t, 14, col=RED if ("?" in t or "x" in t) else INK))
    return svg_wrap(W, H, "".join(s), "triangle")


def set_tri():
    its = []
    for a, b in [(50, 60), (35, 85), (90, 25), (45, 45), (110, 40), (30, 30), (72, 58), (20, 125), (64, 64), (15, 90)]:
        c = 180 - a - b
        q = fig(tri_svg({"A": "%d°" % a, "B": "%d°" % b, "C": "?"})) + "What is the missing angle?"
        e = "The angles of a triangle add to 180°. 180° − %d° − %d° = <b>%d°</b>." % (a, b, c)
        wr = [360 - a - b, a + b, 90 - abs(a - b) if 90 - abs(a - b) > 0 else c + 20, c + 10, c - 10 if c > 10 else c + 30, 180 - a]
        its.append(mcq(q, ("%d°" % c, c), [("%d°" % w, w) for w in wr], e))
    for a, c in [(40, 70), (55, 65), (30, 90), (45, 80), (25, 50), (60, 60), (35, 100), (70, 50)]:
        ext = a + c
        q = fig(tri_svg({"A": "%d°" % a, "C": "%d°" % c, "ext": "?"})) + "What is the exterior angle?"
        e = "An exterior angle equals the sum of the two far (remote) interior angles: %d° + %d° = <b>%d°</b>." % (a, c, ext)
        wr = [180 - ext, 180 - a, 180 - c, 360 - ext, ext - 10, ext + 10]
        its.append(mcq(q, ("%d°" % ext, ext), [("%d°" % w, w) for w in wr if w > 0], e))
    for q, ans, wr, e in [
        ("Why do the angles of a triangle add to 180°?", "A line through one corner parallel to the far side makes alternate interior angles that fill a straight line",
         ["Because every triangle has a right angle", "Because 3 × 60 = 180", "Because triangles have 3 sides"],
         "Draw a line through the top corner parallel to the base. The three angles fit on that straight line, so they add to <b>180°</b>."),
        ("Can a triangle have two right angles?", "No, they would already add to 180°", ["Yes", "Only if it is large", "Only if it is isosceles"],
         "90° + 90° = 180°, leaving 0° for the third angle: <b>no</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[10], o[2], o[11], o[18], o[3], o[12], o[4], o[13], o[5], o[14], o[19], o[6], o[15], o[7], o[16],
             o[8], o[17], o[9]]
    return {"title": "Triangle angles", "items": order}


# ============================================================ set 4: equations
def set_eq():
    its = []
    for (a1, b1), (a2, b2), kind in [((2, 10), (1, 50), "equal"), ((3, -20), (2, 15), "equal"), ((1, 30), (2, 0), "equal"),
                                     ((4, 10), (3, 25), "equal"), ((5, -10), (3, 20), "equal"), ((2, 20), (1, 40), "supp"),
                                     ((3, 15), (1, 25), "supp"), ((4, 0), (1, 30), "supp"), ((2, -10), (3, 10), "supp"), ((5, 5), (2, 7), "supp")]:
        ex1 = lambda a, b: ("%dx" % a if a != 1 else "x") + (" + %d" % b if b > 0 else (" − %d" % -b if b < 0 else ""))
        if kind == "equal":
            x = (b2 - b1) / (a1 - a2)
            rel = "corresponding angles"
            e = "Corresponding angles are equal: %s = %s, so x = <b>%g</b>." % (ex1(a1, b1), ex1(a2, b2), x)
        else:
            x = (180 - b1 - b2) / (a1 + a2)
            rel = "same-side interior angles"
            e = "Same-side interior angles add to 180°: (%s) + (%s) = 180, so x = <b>%g</b>." % (ex1(a1, b1), ex1(a2, b2), x)
        if x != int(x):
            continue
        x = int(x)
        q = "Two parallel lines are cut by a transversal. The %s measure (%s)° and (%s)°. Find x." % (rel, ex1(a1, b1), ex1(a2, b2))
        q = q.replace("-", "−")
        e = e.replace("+ -", "− ")
        wr = [(180 - b1 - b2) // (a1 + a2) if kind == "equal" else (b2 - b1) // (a1 - a2) if a1 != a2 else x + 5, x + 10, 2 * x, x - 5]
        its.append(mcq(q, (str(x), x), [(str(w), w) for w in wr if w > 0], e))
    for a, b, c in [((1, 0), (2, 0), (3, 0)), ((1, 10), (1, 20), (1, 30)), ((2, 0), (3, 0), (4, 0)), ((1, 0), (1, 0), (2, 0)),
                    ((2, 10), (1, 20), (3, -10)), ((3, 0), (4, 0), (5, 0)), ((1, 5), (2, 5), (3, -10)), ((1, 0), (2, 0), (6, 0)),
                    ((2, 0), (2, 0), (5, 0)), ((1, 15), (3, 0), (4, 5)), ((1, 0), (3, 0), (5, 0)), ((2, 5), (3, 5), (4, 0))]:
        k = a[0] + b[0] + c[0]
        x = (180 - a[1] - b[1] - c[1]) / k
        if x != int(x) or len(its) >= 20:
            continue
        x = int(x)
        f = lambda p: ("%dx" % p[0] if p[0] != 1 else "x") + (" + %d" % p[1] if p[1] > 0 else (" − %d" % -p[1] if p[1] < 0 else ""))
        q = "A triangle has angles (%s)°, (%s)° and (%s)°. Find x." % (f(a), f(b), f(c))
        e = "The angles add to 180°: %dx + %d = 180, so x = <b>%d</b>. The angles are %d°, %d° and %d°." % (
            k, a[1] + b[1] + c[1], x, a[0] * x + a[1], b[0] * x + b[1], c[0] * x + c[1])
        e = e.replace("+ -", "− ")
        wr = [int((360 - a[1] - b[1] - c[1]) / k), x + 5, x * 2, int(180 / k) if int(180 / k) != x else x - 3]
        its.append(mcq(q, (str(x), x), [(str(w), w) for w in wr if w > 0], e))
    assert len(its) == 20, len(its)
    return {"title": "Angle equations", "items": its}


# ============================================================ set 5: reasoning
def set_reason():
    its = []
    for q, ans, wr, e in [
        ("∠1 = 115° and the lines are parallel. Ana says ∠5 = 65°. What did she do wrong?", "∠1 and ∠5 are equal, not supplementary",
         ["Nothing, she is right", "She should add 115° + 65°", "∠5 must be 90°"], "Corresponding angles are equal, so ∠5 = 115°. <b>∠1 and ∠5 are equal, not supplementary</b>."),
        ("A triangle has angles 40° and 60°. Ben says the third angle is 260°. What did he use?", "360° instead of 180°",
         ["180° correctly", "The exterior angle rule", "Vertical angles"], "360 − 100 = 260. A triangle uses 180°: the third angle is 80°. <b>360° instead of 180°</b>."),
        ("If same-side interior angles are 75° and 105°, are the lines parallel?", "Yes, they add to 180°", ["No, they are not equal", "Only if both are 90°", "We cannot tell"],
         "75 + 105 = 180, so <b>yes, they add to 180°</b>."),
        ("If corresponding angles are 70° and 75°, are the lines parallel?", "No, they would have to be equal", ["Yes", "Only if both are acute", "We cannot tell"],
         "Corresponding angles on parallel lines are equal: <b>no, they would have to be equal</b>."),
        ("An exterior angle of a triangle is 120°. One far interior angle is 50°. What is the other far interior angle?", "70°",
         ["60°", "130°", "10°"], "120 = 50 + x, so x = <b>70°</b>."),
        ("An exterior angle of a triangle is 135°. What is the interior angle next to it?", "45°", ["135°", "225°", "55°"],
         "They form a straight line: 180 − 135 = <b>45°</b>."),
        ("The angles of a triangle are in the ratio 1 : 2 : 3. What is the largest angle?", "90°", ["60°", "30°", "120°"],
         "x + 2x + 3x = 180, so x = 30 and the largest is 3 × 30 = <b>90°</b>."),
        ("An isosceles triangle has a top angle of 40°. What is each base angle?", "70°", ["40°", "140°", "50°"],
         "(180 − 40) ÷ 2 = <b>70°</b>."),
        ("Each angle of an equilateral triangle measures …", "60°", ["90°", "45°", "180°"], "180 ÷ 3 = <b>60°</b>."),
        ("A right triangle has one angle of 35°. What is the other acute angle?", "55°", ["65°", "145°", "35°"], "180 − 90 − 35 = <b>55°</b>."),
        ("Two angles of a triangle are equal to two angles of another triangle. What must be true?", "The third angles are equal too",
         ["The triangles are congruent", "The sides are equal", "Nothing"], "Each triangle adds to 180°: <b>the third angles are equal too</b>."),
        ("∠3 and ∠6 are alternate interior angles and ∠3 = 4x°, ∠6 = 80°. Find x.", "20", ["25", "80", "45"], "4x = 80, so x = <b>20</b>."),
        ("∠4 and ∠6 are same-side interior angles. ∠4 = 3x° and ∠6 = 2x°. Find x.", "36", ["18", "60", "90"], "3x + 2x = 180, 5x = 180, x = <b>36</b>."),
        ("Vertical angles measure (5x − 10)° and (3x + 20)°. Find x.", "15", ["5", "25", "21.25"], "5x − 10 = 3x + 20, 2x = 30, x = <b>15</b>."),
        ("A linear pair measures (2x)° and (x + 30)°. Find x.", "50", ["30", "60", "110"], "2x + x + 30 = 180, 3x = 150, x = <b>50</b>."),
        ("In the figure, all 8 angles are formed by parallel lines and a transversal. How many different measures can there be?", "At most 2",
         ["8", "4", "1"], "Four angles equal x and four equal 180 − x: <b>at most 2</b>."),
        ("The sum of the exterior angles of a triangle (one at each corner) is …", "360°", ["180°", "270°", "540°"],
         "Each exterior angle + interior angle = 180°; three of them = 540°, minus the 180° inside = <b>360°</b>."),
        ("Which pair of angles is always supplementary?", "A linear pair", ["Vertical angles", "Corresponding angles", "Alternate interior angles"],
         "Angles on a straight line add to 180°: <b>a linear pair</b>."),
        ("Which pair of angles is equal even if the lines are NOT parallel?", "Vertical angles", ["Corresponding angles", "Alternate interior angles",
         "Same-side interior angles"], "<b>Vertical angles</b> are always equal."),
        ("A triangle has angles x°, x° and 100°. Find x.", "40", ["80", "50", "130"], "2x + 100 = 180, 2x = 80, x = <b>40</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Reasoning with angles", "items": its}


def body():
    return ("<h2>Parallel lines and a transversal</h2>"
            "<figure class='sn-fig'>" + par_svg() + "<figcaption>Two parallel lines (arrows) cut by a transversal.</figcaption></figure>"
            + table(["Pair", "Example", "Rule"], [
                ["Corresponding", "∠1 and ∠5", "equal"], ["Alternate interior", "∠3 and ∠6", "equal"],
                ["Alternate exterior", "∠1 and ∠8", "equal"], ["Same-side interior", "∠3 and ∠5", "add to 180°"],
                ["Vertical", "∠1 and ∠4", "equal"], ["Linear pair", "∠1 and ∠2", "add to 180°"]])
            + "<h2>Triangles</h2><p>The three angles of a triangle add to <b>180°</b>. "
            "An <b>exterior angle</b> equals the sum of the two far interior angles.</p>"
            + example("In a triangle, two angles are 50° and 65°. Find the third.", ["180 − 50 − 65 = 65."], "65°")
            + "<h2>Common mistakes</h2><ul><li>Subtracting from 180° when the angles are equal (corresponding, alternate).</li>"
            "<li>Saying same-side interior angles are equal. They add to 180°.</li>"
            "<li>Using 360° for a triangle. The angles add to 180°.</li></ul>")


def main():
    sets = [set_names(), set_find(), set_tri(), set_eq(), set_reason()]
    balance(sets, R)
    unit = {
        "slug": "angle-relationships-parallel-lines",
        "title": "Angles: Parallel Lines, Transversals and Triangles",
        "seo_title": "Grade 8 Parallel Lines and Transversals Worksheets: Angle Pairs, Triangle Sum, Exterior Angles",
        "short_title": "Angles and parallel lines",
        "domain": "Geometry",
        "standard_code": "8.G.A.5",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/G/A/5/",
        "standard_text": "Use informal arguments to establish facts about the angle sum and exterior angle of triangles, about the angles created when parallel lines are cut by a transversal, and the angle-angle criterion for similarity of triangles.",
        "meta_desc": "Free Grade 8 angle worksheets: corresponding, alternate interior, alternate exterior and same-side interior angles with parallel lines, the triangle angle sum, exterior angles, and angle equations. 100 questions with an answer key.",
        "key_big": "With parallel lines, corresponding and alternate angles are equal; same-side interior angles add to 180°.",
        "key_sub": "A triangle's angles add to 180°. An exterior angle equals the two far interior angles added.",
        "body_html": body(),
        "faq": [
            {"q": "Which angles are equal when parallel lines are cut by a transversal?", "a": "Corresponding angles, alternate interior angles, alternate exterior angles and vertical angles are equal."},
            {"q": "Which angles add to 180°?", "a": "Same-side interior angles and any two angles that form a straight line (a linear pair)."},
            {"q": "What is the exterior angle theorem?", "a": "An exterior angle of a triangle equals the sum of the two interior angles that are not next to it."},
            {"q": "Why do the angles of a triangle add to 180°?", "a": "Draw a line through one corner parallel to the opposite side. The three angles of the triangle line up along that straight line, which is 180°."}],
        "sets": sets, "pdf_url": "", "sort": 13, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
