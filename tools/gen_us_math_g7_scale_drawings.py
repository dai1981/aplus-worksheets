# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Scale Drawings (7.G.A.1)
  python tools/gen_us_math_g7_scale_drawings.py
Use a scale to find actual lengths and areas from a drawing, find drawing lengths from actual
lengths, find the scale, and redraw at a different scale.
Wrong answers come from real mistakes: dividing instead of multiplying (and the reverse),
adding the scale instead of multiplying, and scaling an area by the scale factor instead of
its square.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, fig, figure, svg_wrap, text, line, table, example,
                       write_unit, GREEN, FILL, INK, BLUE, fr)

R = random.Random(71401)
UPDATED = "2026-11-09"


def n(v):
    v = F(v)
    s = num(v)
    if s is None:
        w, r = divmod(v.numerator, v.denominator)
        s = ((str(w) + " ") if w else "") + fr(r, v.denominator)
    return s


def item(q, v, ws, e, unit=""):
    v = F(v)
    cands = []
    for w in list(ws) + [v * 2, v / 2, v + 10]:
        w = F(w)
        if w > 0 and w != v:
            cands.append((n(w) + unit, w))
    return mcq(q, (n(v) + unit, v), cands, e)


def plan_svg(w_cm, h_cm, label_w, label_h, title="scale drawing of a rectangle"):
    """Rectangle drawn on a 1 cm grid (1 cm = 30 px), with side labels."""
    u = 30
    W, H = int(w_cm * u) + 120, int(h_cm * u) + 80
    x0, y0 = 60, 30
    s = []
    for i in range(int(w_cm) + 1):
        s.append(line(x0 + i * u, y0, x0 + i * u, y0 + h_cm * u, "#d8d2c4", 1))
    for j in range(int(h_cm) + 1):
        s.append(line(x0, y0 + j * u, x0 + w_cm * u, y0 + j * u, "#d8d2c4", 1))
    s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' fill-opacity='0.6' stroke='%s' stroke-width='3'/>"
             % (x0, y0, w_cm * u, h_cm * u, FILL, GREEN))
    s.append(text(x0 + w_cm * u / 2, y0 + h_cm * u + 26, label_w, 15, col=BLUE))
    s.append(text(x0 - 10, y0 + h_cm * u / 2 + 5, label_h, 15, "end", col=BLUE))
    return svg_wrap(W, H, "".join(s), title)


# ------------------------------------------------------------ set 1
def set_meaning():
    its = []
    meaning = [("1 inch : 20 feet", "Every 1 inch on the drawing stands for 20 feet in real life.",
                ["Every 20 inches on the drawing stand for 1 foot.", "The drawing is 20 feet long.", "The real object is 1 inch long."]),
               ("1 cm : 5 km", "Every 1 cm on the map stands for 5 km in real life.",
                ["Every 5 cm on the map stand for 1 km.", "The map is 5 km wide.", "The map shows 1 km in all."]),
               ("1 : 50", "The real object is 50 times as large as the drawing.",
                ["The drawing is 50 times as large as the real object.", "The drawing is 50 cm long.", "The real object is 51 times as large."])]
    for sc, good, bad in meaning:
        its.append(mcq("What does the scale %s mean?" % B(sc), (good, "g"), [(b, b) for b in bad],
                       "A scale compares a length on the drawing (first) with the real length (second)."))
    facts = [(1, "in.", 4, "ft", "4 ft"), (2, "cm", 10, "m", "5 m"), (1, "cm", 25, "km", "25 km"), (3, "in.", 15, "ft", "5 ft"), (1, "cm", F("2.5"), "m", "2.5 m")]
    for a, ua, b, ub, ans in facts:
        per = F(b) / a
        its.append(item("A scale is %s %s : %s %s. How many %s does 1 %s stand for?" % (n(a), ua, n(b), ub, ub.replace("ft", "feet").replace("m", "meters") if ub != "km" else "kilometers",
                                                                                       ua.replace("in.", "inch").replace("cm", "centimeter")),
                        per, [F(a) / b, b + a, b * a], "Divide: %s ÷ %s = %s %s for each 1 %s." % (n(b), n(a), n(per), ub, ua), " " + ub))
    eq = [("1 in. : 2 ft", "2 in. : 4 ft", ["2 in. : 3 ft", "1 in. : 4 ft", "3 in. : 2 ft"]),
          ("1 cm : 4 m", "3 cm : 12 m", ["3 cm : 7 m", "4 cm : 1 m", "1 cm : 12 m"]),
          ("1 in. : 6 ft", "5 in. : 30 ft", ["5 in. : 11 ft", "6 in. : 1 ft", "5 in. : 6 ft"]),
          ("2 cm : 5 m", "6 cm : 15 m", ["6 cm : 9 m", "5 cm : 2 m", "4 cm : 7 m"])]
    for sc, good, bad in eq:
        its.append(mcq("Which scale is the same as %s?" % B(sc), (good, "g"), [(b, b) for b in bad],
                       "Multiply both parts by the same number. %s × the same factor gives %s." % (sc, good)))
    sf = [("1 cm : 1 m", 100, [1, F(1, 100), 10]), ("1 in. : 1 ft", 12, [1, 10, F(1, 12)]), ("1 cm : 2 m", 200, [2, 20, F(1, 200)]),
          ("1 in. : 1 yd", 36, [3, 1, 12]), ("5 mm : 1 m", 200, [5, F(1, 200), 1000]), ("1 in. : 5 ft", 60, [5, 12, 17]),
          ("1 cm : 50 cm", 50, [51, F(1, 50), 49]), ("2 in. : 1 ft", 6, [12, 24, 2])]
    for sc, k, ws in sf:
        its.append(item("What is the scale factor (real ÷ drawing, in the same units) for the scale %s?" % B(sc), k, ws,
                        "Use the same units: %s. Real ÷ drawing = %s, so the real object is %s times as large." % (
                            {"1 cm : 1 m": "1 m = 100 cm", "1 in. : 1 ft": "1 ft = 12 in.", "1 cm : 2 m": "2 m = 200 cm",
                             "1 in. : 1 yd": "1 yd = 36 in.", "5 mm : 1 m": "1 m = 1,000 mm, and 1,000 ÷ 5 = 200", "1 in. : 5 ft": "5 ft = 60 in.",
                             "1 cm : 50 cm": "both are in cm", "2 in. : 1 ft": "1 ft = 12 in., and 12 ÷ 2 = 6"}[sc], n(k), n(k))))
    return {"title": "What a scale means", "items": its}


# ------------------------------------------------------------ set 2
def set_actual():
    its = []
    cases = [(F(3), 1, 4, "in.", "ft"), (F(5), 1, 10, "cm", "m"), (F("2.5"), 1, 8, "in.", "ft"), (F(7), 2, 5, "cm", "m"), (F(4), 1, 25, "cm", "km"),
             (F("6.5"), 1, 2, "in.", "ft"), (F(9), 3, 10, "cm", "m"), (F(12), 1, F("1.5"), "cm", "m"),
             (F("4.5"), 1, 6, "in.", "ft"), (F(8), 1, 50, "cm", "km"), (F(10), 4, 3, "cm", "m"), (F("1.5"), 1, 12, "in.", "ft")]
    for d, a, b, ua, ub in cases:
        real = d * F(b) / a
        its.append(item("A drawing uses the scale %s %s : %s %s. A line on the drawing is %s %s long. How long is it in real life?" % (n(a), ua, n(b), ub, n(d), ua),
                        real, [d * a / F(b), d + F(b), d * F(b) if a != 1 else d / F(b)],
                        (("Each %s %s stands for %s %s, so each 1 %s stands for %s %s. " % (n(a), ua, n(b), ub, ua, n(F(b) / a), ub)) if a != 1 else
                         ("Each 1 %s stands for %s %s. " % (ua, n(b), ub)))
                        + "%s × %s = %s %s." % (n(d), n(F(b) / a), n(real), ub), " " + ub))
    svgs = [(6, 4, 2), (5, 3, 3), (7, 2, 4), (4, 4, 5)]
    for w, h, k in svgs:
        svg = plan_svg(w, h, "%d cm" % w, "%d cm" % h, "rectangle %d cm by %d cm on a grid" % (w, h))
        its.append(item("The drawing of a garden uses the scale 1 cm : %d m. How long is the real garden (the longer side)?" % k + fig(svg),
                        w * k, [w + k, F(w, k), h * k], "%d cm × %d = %d m." % (w, k, w * k), " m"))
    for w, h, k in [(6, 4, 3), (5, 2, 4), (3, 3, 6), (8, 3, 2)]:
        svg = plan_svg(w, h, "%d cm" % w, "%d cm" % h, "rectangle %d cm by %d cm" % (w, h))
        P_ = 2 * (w + h) * k
        its.append(item("A room is drawn with the scale 1 cm : %d m. What is the real perimeter of the room?" % k + fig(svg), P_,
                        [2 * (w + h), (w + h) * k, w * h * k], "Real sides: %d m and %d m. Perimeter = 2 × (%d + %d) = %d m." % (w * k, h * k, w * k, h * k, P_), " m"))
    return {"title": "From the drawing to real life", "items": its}


# ------------------------------------------------------------ set 3
def set_drawing():
    its = []
    cases = [(20, 1, 4, "in.", "ft"), (45, 1, 5, "cm", "m"), (36, 1, 6, "in.", "ft"), (150, 1, 25, "cm", "km"), (18, 2, 3, "cm", "m"), (70, 1, 20, "in.", "ft"),
             (12, 1, 8, "in.", "ft"), (9, 1, 2, "cm", "m"), (240, 1, 40, "cm", "km"), (35, 1, 10, "in.", "ft"), (27, 3, 9, "cm", "m"), (55, 1, 10, "cm", "m")]
    for real, a, b, ua, ub in cases:
        d = F(real) * a / b
        its.append(item("A map uses the scale %s %s : %s %s. The real distance is %s %s. How long is it on the map?" % (n(a), ua, n(b), ub, n(real), ub),
                        d, [F(real) * b / a, F(real) - b, F(b) / real],
                        "Divide the real length by %s %s per %s: %s ÷ %s = %s %s." % (n(F(b) / a), ub, ua, n(real), n(F(b) / a), n(d), ua), " " + ua))
    rooms = [(12, 15, 3), (20, 16, 4), (9, 21, 3), (24, 18, 6)]
    for L_, W_, k in rooms:
        its.append(mcq("A room is %d ft by %d ft. You draw it with the scale 1 in. : %d ft. What size is the drawing?" % (L_, W_, k),
                       ("%s in. by %s in." % (n(F(L_, k)), n(F(W_, k))), "g"),
                       [("%s in. by %s in." % (n(L_ * k), n(W_ * k)), "a"), ("%s in. by %s in." % (n(L_ - k), n(W_ - k)), "b"),
                        ("%s in. by %s in." % (n(F(L_, k) + 1), n(F(W_, k) + 1)), "c")],
                       "%d ÷ %d = %s and %d ÷ %d = %s." % (L_, k, n(F(L_, k)), W_, k, n(F(W_, k)))))
    for real, ratio in [(F("1.8"), 30), (F("4.5"), 50), (F("2.4"), 20), (12, 100)]:
        d = F(real) * 100 / ratio
        its.append(item("A model uses the scale 1 : %d. The real object is %s m long. How long is the model, in centimeters?" % (ratio, n(real)),
                        d, [F(real) / ratio, F(real) * ratio, d / 10], "%s m = %s cm. %s ÷ %d = %s cm." % (n(real), n(F(real) * 100), n(F(real) * 100), ratio, n(d)), " cm"))
    return {"title": "From real life to the drawing", "items": its}


# ------------------------------------------------------------ set 4
def set_area_and_rescale():
    its = []
    for w, h, k in [(3, 2, 5), (4, 3, 2), (6, 5, 10), (5, 2, 4), (8, 3, 3), (2, 2, 25)]:
        A = w * k * h * k
        its.append(item("A rectangle on a drawing is %d cm by %d cm. The scale is 1 cm : %d m. What is the real area?" % (w, h, k), A,
                        [w * h * k, w * h, (w + h) * k], "Real sides: %d m and %d m. Area = %d × %d = %d m². Not %d m²: the area grows by %d² = %d, not %d."
                        % (w * k, h * k, w * k, h * k, A, w * h * k, k, k * k, k), " m²"))
    for k in [3, 5, 10, 4]:
        its.append(item("A drawing uses a scale factor of %d. How many times as large is the real area as the drawing's area?" % k, k * k,
                        [k, 2 * k, k * 3], "Each length is %d times as long, so the area is %d × %d = %d times as large." % (k, k, k, k * k), " times"))
    for d, k1, k2 in [(6, 2, 4), (10, 5, 2), (8, 3, 6), (4, 10, 5), (9, 2, 3), (12, 4, 8)]:
        real = d * k1
        nd = F(real, k2)
        its.append(item("A drawing uses the scale 1 cm : %d m. A wall is %d cm long on it. You redraw it with the scale 1 cm : %d m. How long is the wall on the new drawing?"
                        % (k1, d, k2), nd, [d * F(k2, k1), d, real], "Real length: %d × %d = %d m. New drawing: %d ÷ %d = %s cm." % (d, k1, real, real, k2, n(nd)), " cm"))
    for d, real, unit_d, unit_r, ans in [(4, 20, "in.", "ft", "1 in. : 5 ft"), (6, 30, "cm", "m", "1 cm : 5 m"), (3, 45, "in.", "ft", "1 in. : 15 ft"),
                                         (5, 2, "cm", "km", "1 cm : 0.4 km")]:
        k = F(real, d)
        bad = ["1 %s : %s %s" % (unit_d, n(F(d, real)), unit_r), "1 %s : %s %s" % (unit_d, n(real - d), unit_r), "%s %s : 1 %s" % (n(k), unit_d, unit_r)]
        its.append(mcq("A %s %s line on a drawing stands for %s %s. What is the scale written as 1 %s : ?" % (n(d), unit_d, n(real), unit_r, unit_d),
                       (ans, "g"), [(b, b) for b in bad], "%s ÷ %s = %s, so the scale is %s." % (n(real), n(d), n(k), ans)))
    return {"title": "Area, finding the scale and redrawing", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)
    w = [("On a map, 1 inch = 15 miles. Two towns are 3.5 inches apart. How far apart are they?", F("52.5"), [F("18.5"), F("0.23"), 105], "3.5 × 15 = 52.5 miles.", " miles"),
         ("A map scale is 1 cm : 50 km. Two cities are 375 km apart. How far apart are they on the map?", F("7.5"), [18750, 325, 15], "375 ÷ 50 = 7.5 cm.", " cm"),
         ("A model car is built at a scale of 1 : 24. The model is 7.5 inches long. How long is the real car in feet?", 15, [180, F("0.3125"), F("31.5")],
          "7.5 × 24 = 180 inches. 180 ÷ 12 = 15 feet.", " ft"),
         ("A blueprint uses 1/4 inch = 1 foot. A wall is 3 1/2 inches long on it. How long is the real wall?", 14, [F(7, 8), F("3.75"), 7], "3 1/2 ÷ 1/4 = 14 feet.", " ft"),
         ("A dollhouse uses a scale of 1 inch : 1 foot. A real door is 7 feet tall. How tall is the dollhouse door?", 7, [84, 12, F(7, 12)],
          "1 inch for each foot: 7 feet → 7 inches.", " in."),
         ("A map uses 2 cm : 25 km. A road is 9 cm long on the map. How long is the real road?", F("112.5"), [225, 36, F("0.72")], "9 ÷ 2 = 4.5 groups of 25 km. 4.5 × 25 = 112.5 km.", " km"),
         ("A school is 120 m long. On a plan it is 24 cm long. What is the scale (1 cm : ? m)?", 5, [F("0.2"), 96, 144], "120 ÷ 24 = 5, so 1 cm : 5 m.", " m"),
         ("A park is drawn 8 cm by 5 cm with scale 1 cm : 20 m. What is the real area?", 16000, [800, 40, 3200], "Real: 160 m × 100 m = 16,000 m².", " m²"),
         ("A photo 4 in. by 6 in. is enlarged with scale factor 2.5. What are the new length and width? Give the longer side.", 15, [F("8.5"), F("2.4"), 10],
          "6 × 2.5 = 15 in. (and 4 × 2.5 = 10 in.).", " in."),
         ("The Statue of Liberty is about 151 ft tall. A souvenir uses the scale 1 in. : 25 ft. About how tall is the souvenir?", F("6.04"), [3775, 126, F("0.17")],
          "151 ÷ 25 = 6.04 inches.", " in."),
         ("An ant is 6 mm long. In a drawing it is 9 cm long. What is the scale factor?", 15, [F("1.5"), 54, 3], "9 cm = 90 mm. 90 ÷ 6 = 15. The drawing is 15 times as large.", ""),
         ("A soccer field is 100 m by 64 m. You draw it with 1 cm : 4 m. What is the drawing's length?", 25, [400, 96, 16], "100 ÷ 4 = 25 cm.", " cm"),
         ("A map scale is 1 in. : 40 mi. A trip is 260 mi. How many inches is it on the map?", F("6.5"), [10400, 220, 65], "260 ÷ 40 = 6.5 inches.", " in."),
         ("A tiny cell is 0.02 mm wide. A picture shows it 3 cm wide. What is the scale factor?", 1500, [150, 60, F("0.0067")], "3 cm = 30 mm. 30 ÷ 0.02 = 1,500.", ""),
         ("A room on a plan is 5 in. by 4 in. The scale is 1 in. : 3 ft. Carpet costs $4 per square foot. What does carpet for the room cost?", 720, [240, 80, 180],
          "Real room: 15 ft × 12 ft = 180 ft². 180 × $4 = $720.", ""),
         ("Two scale drawings show the same 30 m wall. Drawing A uses 1 cm : 2 m and drawing B uses 1 cm : 5 m. How much longer is the wall on drawing A?", 9, [3, 6, 15],
          "A: 30 ÷ 2 = 15 cm. B: 30 ÷ 5 = 6 cm. 15 − 6 = 9 cm.", " cm"),
         ("A model airplane has a wingspan of 18 in. The scale is 1 : 48. What is the real wingspan in feet?", 72, [864, F("0.375"), 66], "18 × 48 = 864 in. 864 ÷ 12 = 72 ft.", " ft"),
         ("On a map, 3 cm stands for 12 km. A lake is 7 cm across on the map. How wide is the real lake?", 28, [84, 22, F("1.75")], "12 ÷ 3 = 4 km per cm. 7 × 4 = 28 km.", " km"),
         ("A square patio is drawn 3 in. on each side. The scale is 1 in. : 4 ft. What is the patio's real area?", 144, [36, 48, 12], "Real side: 12 ft. Area = 12 × 12 = 144 ft².", " ft²"),
         ("A poster enlarges a 2 cm stamp to 50 cm. What is the scale factor?", 25, [48, 100, F("0.04")], "50 ÷ 2 = 25.", "")]
    for q, v, ws, e, u in w:
        q = q.replace("1/4 inch", fr(1, 4) + " inch").replace("3 1/2 inches", "3 " + fr(1, 2) + " inches")
        e = e.replace("3 1/2 ÷ 1/4", "3 " + fr(1, 2) + " ÷ " + fr(1, 4))
        if u == "" and "$" in q:
            its.append(mcq(q, ("$%s" % "{:,}".format(v), v), [("$%s" % "{:,}".format(x), x) for x in ws if x != v], e))
        else:
            its.append(item(q, v, ws, e, u))
    return {"title": "Word problems: maps, models and plans", "items": its}


def body():
    svg = plan_svg(6, 4, "6 cm", "4 cm", "scale drawing of a room 6 cm by 4 cm")
    rows = [["Drawing → real", "multiply", "6 cm × 3 = 18 m"], ["Real → drawing", "divide", "12 m ÷ 3 = 4 cm"],
            ["Area", "multiply by the scale factor squared", "lengths × 3, so area × 9"]]
    return ("<h2>What a scale tells you</h2><p>A <b>scale</b> compares a length on a drawing or map with the real length. "
            "The scale 1 cm : 3 m means every 1 cm on the drawing stands for 3 m in real life.</p>"
            + figure(svg, "Scale 1 cm : 3 m. The real room is 18 m by 12 m.")
            + table(["Going from", "Do this", "Example (1 cm : 3 m)"], rows)
            + example("A map scale is 1 in. : 15 miles. Two towns are 3.5 in. apart. How far apart are they?", ["3.5 × 15 = 52.5."], "52.5 miles")
            + example("A garden is drawn 3 cm by 2 cm with 1 cm : 5 m. What is its real area?",
                      ["Real sides: 15 m and 10 m.", "Area = 15 × 10 = 150 m²."], "150 m²")
            + "<h2>Common mistakes</h2><ul><li>Dividing when you should multiply: from the drawing to real life, multiply.</li>"
            "<li>Scaling area like length: if lengths are 5 times as long, the area is 25 times as large, not 5.</li>"
            "<li>Mixing units: change 1 cm : 1 m to 1 cm : 100 cm before finding the scale factor.</li></ul>")


def main():
    sets = [set_meaning(), set_actual(), set_drawing(), set_area_and_rescale(), set_words()]
    for st in sets:
        for it in st["items"]:
            it["e"] = it["e"].replace("in..", "in.").replace("yd..", "yd.")
    balance(sets, R)
    unit = {
        "slug": "scale-drawings",
        "title": "Scale Drawings",
        "seo_title": "Grade 7 Scale Drawings Worksheets: Maps, Models, Scale Factor and Area",
        "short_title": "Scale drawings",
        "domain": "Geometry",
        "standard_code": "7.G.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/G/A/1/",
        "standard_text": "Solve problems involving scale drawings of geometric figures, including computing actual lengths and areas from a scale drawing and reproducing a scale drawing at a different scale.",
        "meta_desc": "Free Grade 7 scale drawings worksheets: what a scale means, real lengths from a drawing, drawing lengths from real ones, scale factor, real areas, redrawing at a new scale, and map and model word problems. 100 practice questions with an answer key.",
        "key_big": "Drawing to real life: multiply by the scale. Real life to drawing: divide.",
        "key_sub": "With a scale of 1 cm : 3 m, 6 cm on the drawing is 18 m. Areas grow by the scale factor squared.",
        "body_html": body(),
        "faq": [
            {"q": "What is a scale drawing?", "a": "A drawing of a real object where every length is multiplied or divided by the same number. A map and a floor plan are scale drawings."},
            {"q": "How do I find a real length from a scale drawing?", "a": "Multiply the drawing length by the real length that 1 unit stands for. With 1 in. : 4 ft, 3 in. on the drawing is 3 × 4 = 12 ft."},
            {"q": "How do I find the real area?", "a": "Find the real lengths first, then multiply. Or multiply the drawing's area by the scale factor squared."},
            {"q": "How do I redraw at a different scale?", "a": "Find the real length with the old scale, then divide by the new scale. 6 cm at 1 cm : 2 m is 12 m; at 1 cm : 4 m it is 3 cm."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 14,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
