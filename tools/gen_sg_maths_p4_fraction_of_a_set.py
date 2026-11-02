# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Fraction of a Set (MOE 2021 Primary Mathematics Syllabus, Standard)
  python3 tools/gen_sg_maths_p4_fraction_of_a_set.py
What fraction of a set is shaded (simplest form), unit and non-unit fractions of a set,
finding the whole from a part, and word problems with the model method (units).
Every answer is checked with fractions.Fraction; no two choices are equal in value.
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
DARK = "#4fae74"      # shaded / the part asked for
LIGHT = "#d7ecdf"     # other known parts in a bar model
ORANGE = "#f4a63a"    # a second colour in a set
LINE = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
SING = {"pupils": "pupil", "marbles": "marble", "stickers": "sticker", "counters": "counter", "books": "book",
        "tables": "table", "people": "person", "beads": "bead", "oranges": "orange", "boys": "boy", "girls": "girl",
        "lamps": "lamp", "plates": "plate", "puffs": "puff", "rambutans": "rambutan", "children": "child",
        "sweets": "sweet", "curry puffs": "curry puff", "cards": "card", "crayons": "crayon", "packets": "packet", "coins": "coin", "shells": "shell"}


# ------------------------------------------------------------ helpers
def num(n):
    """Whole number: 4 digits as they are, 5 or more digits grouped with a no-break space."""
    s = str(int(n))
    if len(s) <= 4:
        return s
    out = ""
    while len(s) > 3:
        out = NB + s[-3:] + out
        s = s[:-3]
    return s + out


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def FC(v):
    """A fraction choice in simplest form (None when it is a whole number)."""
    v = F(v)
    if v.denominator == 1 or v <= 0:
        return (None, v)
    return (fr(v.numerator, v.denominator), v)


def RAW(a, b):
    """A fraction choice written exactly as a/b (not simplified)."""
    return (fr(a, b), F(a, b))


def N(v, noun=""):
    """A whole-number choice; None when the value is not a whole number or not positive."""
    v = F(v)
    if v.denominator != 1 or v <= 0:
        return (None, v)
    n = v.numerator
    if noun:
        w = SING.get(noun, noun) if n == 1 else noun
        return ("%s %s" % (num(n), w), v)
    return (num(n), v)


def cents(c):
    c = int(c)
    if c < 100:
        return ("%d¢" % c, F(c))
    if c % 100 == 0:
        return ("$%d" % (c // 100), F(c))
    return ("$%d.%02d" % (c // 100, c % 100), F(c))


def mcq(q, correct, cands, e):
    """correct and cands are (html, value). Skips empty, repeated, zero or negative candidates."""
    assert correct[0], (q, correct)
    ch, vals = [correct[0]], [correct[1]]
    for h, v in cands:
        if not h or h in ch or (v is not None and (v in vals or v <= 0)):
            continue
        ch.append(h)
        vals.append(v)
        if len(ch) == 4:
            break
    assert len(ch) == 4, (q, correct, cands)
    return {"q": q, "c": ch, "a": 0, "e": e}


def abcd(good, bad, draw, q, lead):
    """Picture-choice item, built later by balance() so the right picture lands on the chosen letter.
    good: spec; bad: [(spec, why)]; draw(list of 4 specs) -> svg."""
    return {"_abcd": (good, bad, draw, q, lead)}


def build_abcd(it, pos):
    good, bad, draw, q, lead = it["_abcd"]
    order = [b[0] for b in bad[:pos]] + [good] + [b[0] for b in bad[pos:]]
    letters = [L for i, L in enumerate("ABCD") if i != pos]
    why = " ".join("%s %s." % (L, d) for L, (_, d) in zip(letters, bad))
    return {"q": fig(draw(order)) + q, "c": ["A", "B", "C", "D"], "a": pos,
            "e": "%s That is picture <b>%s</b>. %s" % (lead, "ABCD"[pos], why)}


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        new = []
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                new.append(build_abcd(it, t))
                continue
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
            new.append(it)
        s["items"] = new


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u):
    """Tag bar models, A-D pictures and wide pictures so they print larger."""
    rx = re.compile(r"<svg xmlns='http://www.w3.org/2000/svg' viewBox='(-?\d+) 0 (\d+) (\d+)'([^>]*aria-label='([^']*)')")

    def sub(m):
        w, h, lab = int(m.group(2)), int(m.group(3)), m.group(5)
        if lab.startswith("bar model") or lab.startswith("four") or w >= 1.9 * h:
            return "<svg data-pf='lg' " + m.group(0)[5:]
        return m.group(0)
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub(sub, it["q"])
    return u


def svg_wrap(w, h, body, label):
    w, h = int(math.ceil(w)), int(math.ceil(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'>%s</svg>" % (w, h, w, h, label, body))


def txt(x, y, s, size=16, anchor="middle", weight="700", fill=LINE):
    return ("<text x='%.1f' y='%.1f' font-family='%s' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, FONT, size, weight, fill, anchor, s))


# ------------------------------------------------------------ pictures of sets
def obj(cx, cy, R, fill, shape, sw=2.5):
    if shape == "square":
        return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='3' fill='%s' stroke='%s' stroke-width='%s'/>"
                % (cx - R, cy - R, 2 * R, 2 * R, fill, LINE, sw))
    return "<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='%s'/>" % (cx, cy, R, fill, LINE, sw)


def set_svg(fills, cols, shape="circle", R=13, step=32, label=None):
    """A set of objects in a grid, in reading order; fills gives the colour of each object."""
    n = len(fills)
    rows = (n + cols - 1) // cols
    s = []
    for i, f in enumerate(fills):
        r, c = divmod(i, cols)
        s.append(obj(6 + R + c * step, 6 + R + r * step, R, f, shape))
    W = 12 + 2 * R + (min(n, cols) - 1) * step
    H = 12 + 2 * R + (rows - 1) * step
    return svg_wrap(W, H, "".join(s), label or "a set of %d objects" % n)


def shaded(n, k):
    return [DARK] * k + ["#fff"] * (n - k)


def groups_svg(sizes, shade, gcols, R=12, step=29, gap=14, maxw=400, label=None):
    """Objects in groups, each group in a dashed box. shade: indexes of the shaded groups."""
    pad = 7
    boxes = []
    for g in sizes:
        c = min(g, gcols)
        r = (g + gcols - 1) // gcols
        boxes.append((2 * pad + 2 * R + (c - 1) * step, 2 * pad + 2 * R + (r - 1) * step))
    lines, cur, cw = [], [], 0
    for i, (bw, bh) in enumerate(boxes):
        if cur and cw + gap + bw > maxw:
            lines.append(cur)
            cur, cw = [], 0
        cw += (gap if cur else 0) + bw
        cur.append(i)
    lines.append(cur)
    per = -(-len(sizes) // len(lines))          # spread the groups evenly over the lines
    lines = [list(range(i, min(i + per, len(sizes)))) for i in range(0, len(sizes), per)]
    s, y, W = [], 6, 0
    for line in lines:
        x = 6
        lh = max(boxes[i][1] for i in line)
        for i in line:
            bw, bh = boxes[i]
            s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='10' fill='none' stroke='#7a7a7a' "
                     "stroke-width='2' stroke-dasharray='6 4'/>" % (x, y, bw, lh))
            for j in range(sizes[i]):
                r, c = divmod(j, gcols)
                s.append(obj(x + pad + R + c * step, y + pad + R + r * step, R, DARK if i in shade else "#fff", "circle"))
            x += bw + gap
        W = max(W, x - gap + 6)
        y += lh + gap
    H = y - gap + 6
    return svg_wrap(W, H, "".join(s), label or "%d objects in %d groups" % (sum(sizes), len(sizes)))


def four_sets_svg(specs, R=10, step=25):
    """Four sets A-D in a 2 x 2 layout. specs: (shaded, white). Each set is drawn in rows of cols objects."""
    mx = max(a + b for a, b in specs)
    cols = 3 if mx <= 6 else (4 if mx <= 12 else 5)
    rows = (mx + cols - 1) // cols
    cw = 26 + 2 * R + (cols - 1) * step
    chh = 2 * R + (rows - 1) * step
    s = []
    for i, (a, b) in enumerate(specs):
        col, row = i % 2, i // 2
        x0 = 6 + col * (cw + 30)
        y0 = 6 + row * (chh + 18)
        s.append(txt(x0 + 7, y0 + chh / 2 + 6, "ABCD"[i], 17))
        for j in range(a + b):
            r, c = divmod(j, cols)
            s.append(obj(x0 + 26 + R + c * step, y0 + R + r * step, R, DARK if j < a else "#fff", "circle", 2))
    return svg_wrap(2 * cw + 30 + 12, 2 * chh + 18 + 12, "".join(s), "four sets of counters A to D")


# ------------------------------------------------------------ bar models
def tw(t, fs):
    return len(re.sub(r"&[a-z]+;", "x", t)) * fs * 0.6


def bars(rows, uw, aria):
    """Bar model. rows: dicts with name (optional), segs [(width in units, fill, cells, text)],
    above / below [(from unit, to unit, label)] brackets."""
    FS = 15
    names = [r.get("name", "") for r in rows]
    namew = max(tw(n, FS) for n in names) + 10 if any(names) else 0
    x0 = namew + 4
    s = []
    lo, hi = 0.0, 0.0
    y = 4
    for r in rows:
        if r.get("above"):
            y += 30
        top, bot = y, y + 30
        x = x0
        for w, fill, cells, lab in r["segs"]:
            sw = w * uw
            cw = sw / float(cells)
            for i in range(cells):
                s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x + i * cw, top, cw, fill, LINE))
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='30' fill='none' stroke='%s' stroke-width='2.5'/>"
                     % (x, top, sw, LINE))
            if lab:
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % (x + sw / 2, top + 21, FS, "#fff" if fill == DARK else LINE, lab))
            x += sw
        hi = max(hi, x)
        if r.get("name"):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='end'>%s</text>"
                     % (x0 - 8, top + 21, FS, LINE, r["name"]))
        for u0, u1, lab in r.get("above", []):
            xa, xb = x0 + u0 * uw, x0 + u1 * uw
            ly = top - 8
            s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (xa + 1, ly + 5, ly, xb - 1, ly + 5, LINE))
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                     % ((xa + xb) / 2, ly - 6, FS, LINE, lab))
            lo = min(lo, (xa + xb) / 2 - tw(lab, FS) / 2)
            hi = max(hi, (xa + xb) / 2 + tw(lab, FS) / 2)
        y = bot
        if r.get("below"):
            for u0, u1, lab in r["below"]:
                xa, xb = x0 + u0 * uw, x0 + u1 * uw
                ly = bot + 9
                s.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
                         % (xa + 1, ly - 5, ly, xb - 1, ly - 5, LINE))
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                         % ((xa + xb) / 2, ly + 19, FS, LINE, lab))
                lo = min(lo, (xa + xb) / 2 - tw(lab, FS) / 2)
                hi = max(hi, (xa + xb) / 2 + tw(lab, FS) / 2)
            y += 34
        y += 12
    H = y - 12 + 4
    left = min(0.0, lo - 4)
    W = int(hi - left + 6)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='%d 0 %d %d' width='%d' height='%d' role='img' "
            "aria-label='bar model: %s'><g font-family='%s'>%s</g></svg>"
            % (int(left), W, H, W, H, aria, FONT, "".join(s)))


def one_bar(b, a, top_lab, bot_lab, known_shaded=True):
    """A whole bar of b units; the first a units dark. top_lab over the whole; bot_lab under the dark
    units (or under the white units when known_shaded is False)."""
    uw = max(28, 300 // b)
    segs = [(a, DARK, a, ""), (b - a, "#fff", b - a, "")]
    below = [(0, a, bot_lab)] if known_shaded else [(a, b, bot_lab)]
    return bars([{"segs": segs, "above": [(0, b, top_lab)], "below": below}], uw,
                "a whole of %d equal units with %d %s shaded" % (b, a, "unit" if a == 1 else "units"))


# ============================================================ set 1: what fraction is shaded
def shade_e(k, n, what="shaded"):
    v = F(k, n)
    g = math.gcd(k, n)
    e = "%d out of %d counters are %s: %s." % (k, n, what, fr(k, n))
    if g > 1:
        e += " Divide the numerator and the denominator by %d: %s = <b>%s</b>." % (g, fr(k, n), fr(v.numerator, v.denominator))
    else:
        e += " This is already in simplest form: <b>%s</b>." % fr(k, n)
    return e


def shade_wrongs(k, n):
    g = math.gcd(k, n)
    out = [FC(F(n - k, n)), FC(F(k, n - k)), FC(F(n - k, k))]
    if g > 1:
        out += [RAW(k // g, n), RAW(k, n // g)]
    return out


def set_shaded():
    its = []
    q_sh = "What fraction of the %s is shaded? Give your answer in simplest form."
    for k, n, cols, shape in [(2, 8, 4, "circle"), (3, 9, 3, "circle"), (4, 10, 5, "square"), (6, 8, 4, "circle"),
                              (8, 12, 4, "square"), (10, 12, 6, "circle")]:
        word = "counters" if shape == "circle" else "squares"
        e = shade_e(k, n).replace("counters", word)
        if k > n - k:
            e += " (The denominator is <b>all</b> the %s, not just the white ones.)" % word
        its.append(mcq(fig(set_svg(shaded(n, k), cols, shape, label="%d %s, %d shaded" % (n, word, k))) + q_sh % word,
                       FC(F(k, n)), shade_wrongs(k, n), e))
    # not shaded
    for k, n, cols in [(3, 12, 4), (8, 20, 5)]:
        w = n - k
        e = ("%d − %d = %d counters are not shaded. " % (n, k, w)) + shade_e(w, n, "not shaded")
        its.append(mcq(fig(set_svg(shaded(n, k), cols, label="%d counters, %d shaded" % (n, k))) +
                       "What fraction of the counters is <b>not</b> shaded? Give your answer in simplest form.",
                       FC(F(w, n)), [FC(F(k, n)), FC(F(w, k)), FC(F(k, w))] +
                       [RAW(w - math.gcd(w, n), n - math.gcd(w, n))], e))
    # equal groups
    for g, per, sh, extra in [(4, 3, 1, [FC(F(1, 3)), RAW(1, 12), FC(F(3, 4))]),
                              (5, 3, 2, [FC(F(3, 5)), FC(F(2, 3)), RAW(2, 15)]),
                              (6, 3, 4, [FC(F(1, 3)), RAW(4, 18), FC(F(3, 4))]),
                              (4, 5, 3, [FC(F(1, 4)), FC(F(3, 5)), RAW(3, 20)])]:
        n = g * per
        v = F(sh, g)
        e = ("There are %d equal groups and %d of them %s shaded: %s of the groups. "
             "Check with counters: %d out of %d counters = %s = <b>%s</b>."
             % (g, sh, "is" if sh == 1 else "are", fr(sh, g), sh * per, n, fr(sh * per, n), fr(v.numerator, v.denominator)))
        e += " (%d is the number of counters in one group, not the number of groups.)" % per
        its.append(mcq(fig(groups_svg([per] * g, set(range(sh)), 3 if per != 4 else 2)) +
                       "The counters are in equal groups. What fraction of the counters is shaded? "
                       "Give your answer in simplest form.", FC(v), extra, e))
    # groups of different sizes
    for sizes, sh, extra in [([2, 4, 6], {0}, [FC(F(1, 3)), FC(F(5, 6)), FC(F(1, 5))]),
                             ([3, 5, 2], {1}, [FC(F(1, 3)), FC(F(2, 3)), FC(F(3, 5))]),
                             ([4, 4, 8], {0, 1}, [FC(F(2, 3)), FC(F(1, 3)), FC(F(1, 4))])]:
        n = sum(sizes)
        k = sum(sizes[i] for i in sh)
        v = F(k, n)
        gw = "1 group" if len(sh) == 1 else "%d groups" % len(sh)
        e = ("The groups are <b>not the same size</b>, so do not count groups (%s out of 3 gives the wrong answer). "
             "Count counters: %d out of %d are shaded. %s = <b>%s</b>."
             % (gw, k, n, fr(k, n), fr(v.numerator, v.denominator)))
        its.append(mcq(fig(groups_svg(sizes, sh, 3 if max(sizes) <= 6 else 4)) +
                       "The counters are in 3 groups. What fraction of all the counters is shaded? "
                       "Give your answer in simplest form.", FC(v), extra, e))
    # two colours
    fills = [DARK] * 4 + [ORANGE] * 2 + ["#fff"] * 6
    its.append(mcq(fig(set_svg(fills, 6, "square", label="12 squares: 4 green, 2 orange, 6 white")) +
                   "What fraction of the squares is <b>green</b>? Give your answer in simplest form.",
                   FC(F(4, 12)), [FC(F(6, 12)), FC(F(4, 6)), FC(F(2, 12)), FC(F(4, 8))],
                   "4 out of 12 squares are green: %s. Divide both by 4: <b>%s</b>. "
                   "(Do not count the orange squares, and the denominator is all 12 squares.)" % (fr(4, 12), fr(1, 3))))
    fills = [DARK] * 6 + [ORANGE] * 4 + ["#fff"] * 5
    its.append(mcq(fig(set_svg(fills, 5, "square", label="15 squares: 6 green, 4 orange, 5 white")) +
                   "What fraction of the squares is coloured (green or orange)? Give your answer in simplest form.",
                   FC(F(10, 15)), [FC(F(6, 15)), FC(F(5, 15)), FC(F(4, 15)), FC(F(10, 5))],
                   "Coloured: 6 + 4 = 10 out of 15 squares: %s. Divide both by 5: <b>%s</b>." % (fr(10, 15), fr(2, 3))))
    # which picture
    its.append(abcd((4, 2), [((2, 3), "has 2 shaded out of 5, so it shows %s" % fr(2, 5)),
                             ((2, 4), "has 2 shaded out of 6, so it shows %s" % fr(1, 3)),
                             ((3, 3), "has 3 shaded out of 6, so it shows %s" % fr(1, 2))],
                    four_sets_svg, "Which set has %s of its counters shaded?" % fr(2, 3),
                    "%s = %s, so 4 out of 6 counters must be shaded." % (fr(2, 3), fr(4, 6))))
    its.append(abcd((9, 3), [((3, 4), "has 3 shaded and 4 white, so it shows %s" % fr(3, 7)),
                             ((8, 4), "has 8 shaded out of 12, so it shows %s" % fr(2, 3)),
                             ((6, 4), "has 6 shaded out of 10, so it shows %s" % fr(3, 5))],
                    four_sets_svg, "Which set has %s of its counters shaded?" % fr(3, 4),
                    "%s = %s, so 9 out of 12 counters must be shaded." % (fr(3, 4), fr(9, 12))))
    # simplest form
    its.append(mcq(fig(set_svg(shaded(9, 6), 3, label="9 counters, 6 shaded")) +
                   "Wei Ming says %s of the counters are shaded. What is %s in simplest form?" % (fr(6, 9), fr(6, 9)),
                   FC(F(2, 3)), [RAW(2, 9), RAW(3, 6), FC(F(1, 3))],
                   "Divide the numerator <b>and</b> the denominator by 3: 6 ÷ 3 = 2 and 9 ÷ 3 = 3, so %s = <b>%s</b>. "
                   "(Do not divide only the numerator, and do not subtract 3 from each number.)" % (fr(6, 9), fr(2, 3))))
    assert len(its) == 20, len(its)
    return {"title": "What fraction is shaded? (simplest form)", "items": its}


# ============================================================ set 2: unit fraction of a set
def unit_wrongs(b, q, noun=""):
    one = q // b
    return [N(b, noun), N(q - one, noun), N(q * b, noun), N(q - b, noun), N(q + b, noun)]


def unit_e(b, q, noun=""):
    return ("%s of %d means %d shared into %d equal groups. %d ÷ %d = <b>%d</b>%s."
            % (fr(1, b), q, q, b, q, b, q // b, (" " + noun) if noun else ""))


def set_unit():
    its = []
    for b, per in [(4, 3), (3, 5), (5, 4), (6, 3), (2, 7)]:
        q = b * per
        e = ("The %d counters are in %d equal groups. One group is %s of the set. One group has <b>%d</b> counters. "
             "(%d is the number of groups, not the answer.)" % (q, b, fr(1, b), per, b))
        its.append(mcq(fig(groups_svg([per] * b, {0}, 3 if per in (3, 5, 6) else (2 if per == 4 else 4))) +
                       "The counters are in equal groups. What is %s of %d?" % (fr(1, b), q),
                       N(per), unit_wrongs(b, q), e))
    for b, q in [(4, 20), (3, 27), (8, 40), (7, 56), (9, 63), (6, 48), (5, 85), (4, 96), (3, 120)]:
        its.append(mcq("Find %s of %d." % (fr(1, b), q), N(q // b), unit_wrongs(b, q), unit_e(b, q)))
    its.append(mcq("There are 32 children at the void deck. %s of them are playing badminton. "
                   "How many children are playing badminton?" % fr(1, 4),
                   N(8, "children"), unit_wrongs(4, 32, "children"), unit_e(4, 32, "children")))
    its.append(mcq("Mdm Wong has 30 mandarin oranges. She gives %s of them to her neighbour. "
                   "How many oranges does she give away?" % fr(1, 5),
                   N(6, "oranges"), unit_wrongs(5, 30, "oranges"), unit_e(5, 30, "oranges")))
    its.append(mcq("A box has 24 crayons. %s of them are red. How many crayons are <b>not</b> red?" % fr(1, 6),
                   N(20, "crayons"), [N(4, "crayons"), N(18, "crayons"), N(6, "crayons"), N(144, "crayons")],
                   "Red: 24 ÷ 6 = 4 crayons. Not red: 24 − 4 = <b>20</b> crayons. "
                   "(4 is the number of red crayons, and 18 comes from 24 − 6.)"))
    its.append(mcq("Siti has 45 stickers. She gives %s of them to Nurul. How many stickers does Siti have left?" % fr(1, 9),
                   N(40, "stickers"), [N(5, "stickers"), N(36, "stickers"), N(54, "stickers")],
                   "She gives 45 ÷ 9 = 5 stickers. Left: 45 − 5 = <b>40</b> stickers. (Take away 5, not 9.)"))
    its.append(mcq("Ali takes %s of 24 sweets. Ryan takes %s of 24 sweets. How many more sweets does Ali take than Ryan?"
                   % (fr(1, 3), fr(1, 4)),
                   N(2, "sweets"), [N(1, "sweets"), N(8, "sweets"), N(14, "sweets")],
                   "Ali: 24 ÷ 3 = 8. Ryan: 24 ÷ 4 = 6. 8 − 6 = <b>2</b> more sweets. "
                   "(4 − 3 = 1 compares the denominators, not the sweets.)"))
    its.append(mcq("%s of 40 is the same as %s of what number?" % (fr(1, 5), fr(1, 2)),
                   N(16), [N(4), N(8), N(20)],
                   "%s of 40 = 40 ÷ 5 = 8. 8 is half of <b>16</b>, because 16 ÷ 2 = 8. "
                   "(8 is %s of 40; 4 is half of 8.)" % (fr(1, 5), fr(1, 5))))
    assert len(its) == 20, len(its)
    return {"title": "Find a unit fraction of a set", "items": its}


# ============================================================ set 3: non-unit fraction of a set
def nonunit_wrongs(a, b, q, noun=""):
    one = F(q, b)
    out = [N(one, noun), N(one * (b - a), noun)]
    if q % a == 0:
        out.append(N(F(q, a) * b, noun))       # divided by the numerator, multiplied by the denominator
        out.append(N(F(q, a), noun))           # divided by the numerator only
    out += [N(a * q, noun), N(one + a, noun)]
    return out


def nonunit_e(a, b, q, noun=""):
    one = q // b
    return ("%d units = %d. 1 unit = %d ÷ %d = %d. %d units = %d × %d = <b>%d</b>%s."
            % (b, q, q, b, one, a, a, one, a * one, (" " + noun) if noun else ""))


def set_nonunit():
    its = []
    for a, b, per, gc in [(2, 3, 4, 2), (3, 4, 4, 2), (2, 5, 3, 3), (3, 5, 4, 2), (5, 6, 3, 3)]:
        q = b * per
        e = ("Make %d equal groups of %d. %s of %d is %d groups: %d × %d = <b>%d</b>."
             % (b, per, fr(a, b), q, a, a, per, a * per))
        its.append(mcq(fig(groups_svg([per] * b, set(range(a)), gc)) +
                       "The counters are in equal groups. What is %s of %d?" % (fr(a, b), q),
                       N(a * per), nonunit_wrongs(a, b, q), e))
    q = (fig(one_bar(5, 3, "35", "?")) + "The model shows 35 split into 5 equal units. Find %s of 35." % fr(3, 5))
    its.append(mcq(q, N(21), nonunit_wrongs(3, 5, 35), nonunit_e(3, 5, 35)))
    for a, b, q in [(2, 3, 27), (3, 4, 32), (4, 7, 49), (5, 8, 64), (3, 10, 90), (7, 9, 54), (2, 5, 100), (4, 9, 72)]:
        e = nonunit_e(a, b, q)
        if q % a == 0:
            e += " (Divide by the denominator %d, not the numerator %d.)" % (b, a)
        its.append(mcq("Find %s of %d." % (fr(a, b), q), N(F(a * q, b)), nonunit_wrongs(a, b, q), e))
    its.append(mcq("Find %s of 24." % fr(6, 8), N(18), [N(3), N(32), N(6), N(4)],
                   "%s = %s. 1 unit = 24 ÷ 4 = 6. 3 units = 3 × 6 = <b>18</b>. "
                   "(Or 1 unit = 24 ÷ 8 = 3, and 6 units = 18.)" % (fr(6, 8), fr(3, 4))))
    its.append(mcq("There are 40 pupils in a class. %s of them wear spectacles. How many pupils wear spectacles?" % fr(3, 8),
                   N(15, "pupils"), nonunit_wrongs(3, 8, 40, "pupils"), nonunit_e(3, 8, 40, "pupils")))
    its.append(mcq("There are 28 marbles in a bag. %s of them are red. How many marbles are <b>not</b> red?" % fr(2, 7),
                   N(20, "marbles"), nonunit_wrongs(2, 7, 28, "marbles")[:1] + [N(8, "marbles"), N(98, "marbles"),
                                                                                 N(14, "marbles")],
                   "1 unit = 28 ÷ 7 = 4. Red: 2 units = 8 marbles. Not red: 5 units = 5 × 4 = <b>20</b> marbles. "
                   "(8 is the number of red marbles.)"))
    its.append(mcq("Mr Tan has 36 rambutans. He gives away %s of them. How many rambutans does he give away?" % fr(5, 6),
                   N(30, "rambutans"), nonunit_wrongs(5, 6, 36, "rambutans"), nonunit_e(5, 6, 36, "rambutans")))
    its.append(mcq("How much more is %s of 30 than %s of 24?" % (fr(2, 3), fr(3, 4)),
                   N(2), [N(20), N(18), N(38), N(6)],
                   "%s of 30: 30 ÷ 3 × 2 = 20. %s of 24: 24 ÷ 4 × 3 = 18. 20 − 18 = <b>2</b>." % (fr(2, 3), fr(3, 4))))
    its.append(mcq("%s of 20 is the same as %s of what number?" % (fr(3, 4), fr(1, 3)),
                   N(45), [N(15), N(5), N(60)],
                   "%s of 20 = 20 ÷ 4 × 3 = 15. 15 is %s of 15 × 3 = <b>45</b>. "
                   "(15 is %s of 20, not the number we want.)" % (fr(3, 4), fr(1, 3), fr(3, 4))))
    assert len(its) == 20, len(its)
    return {"title": "Non-unit fractions of a set", "items": its}


# ============================================================ set 4: find the whole from a part
def whole_wrongs(a, b, p, noun=""):
    one = F(p, a)
    out = []
    if a > 1:
        out += [N(p * b, noun), N(one, noun)]
    out += [N(one * (b - a), noun), N(p + b, noun), N(F(p, b), noun), N(p * a, noun), N(p - b, noun)]
    return out


def whole_e(a, b, p, noun=""):
    one = p // a
    if a == 1:
        return ("%s of the number is %d, so 1 unit = %d. The whole is %d units: %d × %d = <b>%d</b>%s. "
                "(Multiply to find the whole; do not divide.)"
                % (fr(1, b), p, p, b, b, p, b * p, (" " + noun) if noun else ""))
    return ("%d units = %d. 1 unit = %d ÷ %d = %d. The whole is %d units: %d × %d = <b>%d</b>%s."
            % (a, p, p, a, one, b, b, one, b * one, (" " + noun) if noun else ""))


def set_whole():
    its = []
    for a, b, p in [(1, 3, 8), (1, 4, 12), (2, 5, 14), (3, 4, 27)]:
        q = (fig(one_bar(b, a, "?", str(p))) + "%s of a number is %d. What is the number?" % (fr(a, b), p))
        its.append(mcq(q, N(F(p, a) * b), whole_wrongs(a, b, p), whole_e(a, b, p)))
    for a, b, p in [(1, 5, 9), (1, 6, 7), (2, 3, 18), (5, 6, 40), (3, 8, 15), (4, 9, 32), (3, 7, 24), (5, 8, 35)]:
        its.append(mcq("%s of a number is %d. What is the number?" % (fr(a, b), p),
                       N(F(p, a) * b), whole_wrongs(a, b, p), whole_e(a, b, p)))
    its.append(mcq(fig(set_svg(shaded(6, 6), 6, label="6 shaded counters")) +
                   "These 6 counters are %s of a set. How many counters are in the whole set?" % fr(1, 4),
                   N(24, "counters"), whole_wrongs(1, 4, 6, "counters"), whole_e(1, 4, 6, "counters")))
    its.append(mcq(fig(set_svg(shaded(10, 10), 5, label="10 shaded counters")) +
                   "These 10 counters are %s of a set. How many counters are in the whole set?" % fr(2, 3),
                   N(15, "counters"), whole_wrongs(2, 3, 10, "counters"), whole_e(2, 3, 10, "counters")))
    its.append(mcq("%s of the children at a playground are girls. There are 13 girls. "
                   "How many children are at the playground?" % fr(1, 2),
                   N(26, "children"), whole_wrongs(1, 2, 13, "children"), whole_e(1, 2, 13, "children")))
    its.append(mcq("%s of the counters in a box are blue. There are 18 blue counters. "
                   "How many counters are there in the box?" % fr(3, 4),
                   N(24, "counters"), whole_wrongs(3, 4, 18, "counters"), whole_e(3, 4, 18, "counters")))
    q = (fig(bars([{"segs": [(2, DARK, 2, ""), (5, "#fff", 5, "")], "below": [(0, 2, "10"), (2, 7, "not red ?")]}], 42,
                  "a whole of 7 equal units, 2 units red")) + "%s of the beads in a jar are red. There are 10 red beads. "
         "How many beads are <b>not</b> red?" % fr(2, 7))
    its.append(mcq(q, N(25, "beads"), [N(35, "beads"), N(5, "beads"), N(70, "beads"), N(15, "beads")],
                   "2 units = 10, so 1 unit = 5. Not red: 7 − 2 = 5 units = 5 × 5 = <b>25</b> beads. "
                   "(35 is all the beads.)"))
    its.append(mcq("%s of the pupils in a group are boys. There are 12 boys. How many girls are there?" % fr(3, 5),
                   N(8, "girls"), [N(20, "girls"), N(4, "girls"), N(60, "girls"), N(9, "girls")],
                   "3 units = 12, so 1 unit = 4. Girls: 5 − 3 = 2 units = 2 × 4 = <b>8</b> girls. "
                   "(20 is the whole group.)"))
    q = (fig(one_bar(5, 1, "?", "16", known_shaded=False)) +
         "Hafiz gave away %s of his cards. He had 16 cards left. How many cards did he have at first?" % fr(1, 5))
    its.append(mcq(q, N(20, "cards"), [N(80, "cards"), N(4, "cards"), N(21, "cards"), N(64, "cards")],
                   "He gave away 1 unit, so 16 cards are the other 4 units. 4 units = 16, 1 unit = 4. "
                   "At first: 5 units = <b>20</b> cards. (16 is not %s of the cards.)" % fr(1, 5)))
    its.append(mcq("Priya used %s of her beads to make a bracelet. She had 14 beads left. "
                   "How many beads did she have at first?" % fr(3, 5),
                   N(35, "beads"), [N(70, "beads"), N(21, "beads"), N(7, "beads"), N(19, "beads")],
                   "She used 3 units, so 5 − 3 = 2 units are left. 2 units = 14, 1 unit = 7. "
                   "At first: 5 units = <b>35</b> beads. (14 is 2 units, not 3 units.)"))
    assert len(its) == 20, len(its)
    return {"title": "Find the whole from a part", "items": its}


# ============================================================ set 5: word problems with bar models
def set_words():
    its = []

    def add(q, ans, wrongs, e, noun=""):
        its.append(mcq(q, N(ans, noun), [N(w, noun) for w in wrongs], e))

    q = (fig(one_bar(4, 3, "40", "?")) +
         "There are 40 pupils in a class. %s of them walk to school. How many pupils walk to school?" % fr(3, 4))
    assert F(3, 4) * 40 == 30
    add(q, 30, [10, 120, 160],
        "4 units = 40. 1 unit = 40 ÷ 4 = 10. 3 units = 3 × 10 = <b>30</b> pupils. (10 pupils do not walk.)", "pupils")
    assert 36 - F(5, 9) * 36 == 16
    add("There are 36 pupils in a class. %s of them take the school bus. How many pupils do <b>not</b> take the "
        "school bus?" % fr(5, 9), 16, [20, 4, 31],
        "1 unit = 36 ÷ 9 = 4. The bus takes 5 units, so 9 − 5 = 4 units do not. 4 × 4 = <b>16</b> pupils. "
        "(20 pupils take the bus.)", "pupils")
    assert F(2, 5) * 60 == 24
    add("A hawker stall sold 60 plates of chicken rice in the morning. %s of them were roasted chicken rice. "
        "How many plates of roasted chicken rice were sold?" % fr(2, 5), 24, [12, 36, 150],
        "1 unit = 60 ÷ 5 = 12. 2 units = 2 × 12 = <b>24</b> plates. (Divide by 5, the denominator, not by 2.)",
        "plates")
    q = (fig(bars([{"segs": [(5, DARK, 5, ""), (3, "#fff", 3, "")], "above": [(0, 8, "48")],
                    "below": [(0, 5, "sold"), (5, 8, "?")]}], 36, "a whole of 8 equal units with 5 units sold")) +
         "Mrs Lim baked 48 curry puffs for a school fair. She sold %s of them. How many curry puffs were left?" % fr(5, 8))
    assert 48 - F(5, 8) * 48 == 18
    add(q, 18, [30, 6, 43],
        "1 unit = 48 ÷ 8 = 6. She sold 5 units, so 3 units were left: 3 × 6 = <b>18</b> curry puffs. "
        "(30 curry puffs were sold.)", "curry puffs")
    assert F(5, 6) * 72 == 60
    add("Mr Tan bought 72 mandarin oranges for Chinese New Year. He gave %s of them to his relatives. "
        "How many oranges did he give away?" % fr(5, 6), 60, [12, 360, 17],
        "1 unit = 72 ÷ 6 = 12. 5 units = 5 × 12 = <b>60</b> oranges.", "oranges")
    assert 30 - F(3, 5) * 30 == 12
    add("Devi and her mother made 30 oil lamps for Deepavali. They painted %s of the lamps. "
        "How many lamps were <b>not</b> painted?" % fr(3, 5), 12, [18, 6, 25],
        "1 unit = 30 ÷ 5 = 6. Not painted: 5 − 3 = 2 units = 2 × 6 = <b>12</b> lamps. (18 lamps were painted.)", "lamps")
    assert F(2, 9) * 180 == 40
    add("There are 180 pupils at Sports Day. %s of them run in a relay race. How many pupils run in the relay race?"
        % fr(2, 9), 40, [20, 140, 90],
        "1 unit = 180 ÷ 9 = 20. 2 units = 2 × 20 = <b>40</b> pupils. (90 comes from 180 ÷ 2.)", "pupils")
    assert 120 - F(3, 8) * 120 == 75
    add("There are 120 Primary 4 pupils. %s of them are in a sports CCA. The rest are in other CCAs. "
        "How many pupils are in other CCAs?" % fr(3, 8), 75, [45, 15, 117],
        "1 unit = 120 ÷ 8 = 15. Sports: 3 units = 45. Other CCAs: 5 units = 5 × 15 = <b>75</b> pupils.", "pupils")
    q = (fig(one_bar(4, 1, "?", "9")) +
         "%s of the books on a shelf are storybooks. There are 9 storybooks. How many books are on the shelf?" % fr(1, 4))
    add(q, 36, [27, 13, 5],
        "1 unit = 9. The shelf has 4 units: 4 × 9 = <b>36</b> books. (27 is the number of books that are not storybooks.)",
        "books")
    q = (fig(one_bar(5, 2, "?", "18", known_shaded=False)) +
         "Hui Min gave away %s of her stickers. She had 18 stickers left. How many stickers did she have at first?" % fr(2, 5))
    add(q, 30, [45, 6, 12],
        "She gave away 2 units, so 3 units are left. 3 units = 18, 1 unit = 6. At first: 5 units = <b>30</b> stickers. "
        "(45 comes from taking 18 as 2 units.)", "stickers")
    assert F(3, 5) * 25 == 15
    add("%s of the pupils on a school bus are girls. There are 15 girls. How many boys are on the bus?" % fr(3, 5),
        10, [25, 5, 9],
        "3 units = 15, so 1 unit = 5. Boys: 2 units = 2 × 5 = <b>10</b> boys. (25 is all the pupils on the bus.)", "boys")
    assert 54 - F(4, 9) * 54 == 30
    add("Sarah collected 54 shells at East Coast Park. %s of them were white. How many shells were <b>not</b> white?"
        % fr(4, 9), 30, [24, 6, 50],
        "1 unit = 54 ÷ 9 = 6. White: 4 units = 24. Not white: 9 − 4 = 5 units = 5 × 6 = <b>30</b> shells. "
        "(24 shells were white.)", "shells")
    # money
    its.append(mcq("Ali has 24 coins. %s of them are 50¢ coins and the rest are 20¢ coins. "
                   "How much money are the 50¢ coins worth?" % fr(1, 3),
                   cents(400), [cents(320), cents(1200), cents(800), cents(160)],
                   "50¢ coins: 24 ÷ 3 = 8 coins. 8 × 50¢ = 400¢ = <b>$4</b>. ($3.20 is the value of the 16 coins of 20¢.)"))
    # compare
    q = (fig(bars([{"segs": [(3, DARK, 3, ""), (5, "#fff", 5, "")], "above": [(0, 8, "32")],
                    "below": [(0, 3, "blue"), (3, 8, "green")]}], 36,
                  "a whole of 8 equal units, 3 blue and 5 green")) +
         "Jun Jie has 32 marbles. %s of them are blue and the rest are green. "
         "How many more green marbles than blue marbles does he have?" % fr(3, 8))
    assert 32 * F(5, 8) - 32 * F(3, 8) == 8
    add(q, 8, [12, 20, 4],
        "1 unit = 32 ÷ 8 = 4. Green has 5 units and blue has 3 units, so green has 2 more units: "
        "2 × 4 = <b>8</b> more marbles. (12 blue and 20 green.)", "marbles")
    q = (fig(bars([{"name": "Adults", "segs": [(3, LIGHT, 3, "")]},
                   {"name": "Children", "segs": [(3, LIGHT, 3, ""), (1, DARK, 1, "")], "below": [(3, 4, "12")]}], 40,
                  "adults 3 units and children 4 units")) +
         "At a void deck party, %s of the people are adults and the rest are children. There are 12 more children "
         "than adults. How many people are at the party?" % fr(3, 7))
    assert F(3, 7) * 84 == 36 and 84 - 36 - 36 == 12
    add(q, 84, [36, 48, 21],
        "Adults: 3 units. Children: 7 − 3 = 4 units. The difference is 1 unit = 12. "
        "Altogether: 7 units = 7 × 12 = <b>84</b> people.", "people")
    q = (fig(bars([{"segs": [(2, DARK, 2, ""), (1, "#fff", 1, "")], "below": [(0, 2, "taken ?"), (2, 3, "14")]}], 80,
                  "a whole of 3 equal units, 2 units taken and 1 unit empty")) +
         "%s of the tables at a hawker centre are taken. 14 tables are empty. How many tables are taken?" % fr(2, 3))
    add(q, 28, [42, 7, 21],
        "Taken: 2 units. Empty: 1 unit = 14. Taken: 2 × 14 = <b>28</b> tables. (42 is all the tables.)", "tables")
    assert 45 - 45 // 5 - 45 // 3 == 21
    add("Priya has 45 stickers. She gives %s of them to Kavya and %s of them to Arjun. "
        "How many stickers does she have left?" % (fr(1, 5), fr(1, 3)), 21, [24, 30, 36],
        "Kavya: 45 ÷ 5 = 9. Arjun: 45 ÷ 3 = 15. Given away: 9 + 15 = 24. Left: 45 − 24 = <b>21</b> stickers.",
        "stickers")
    assert 48 - 48 // 4 + 9 == 45
    add("There were 48 people in an MRT train. At a station, %s of them got off and 9 people got on. "
        "How many people were in the train then?" % fr(1, 4), 45, [36, 27, 57],
        "Got off: 48 ÷ 4 = 12. 48 − 12 = 36. Then 9 got on: 36 + 9 = <b>45</b> people. "
        "(27 comes from taking away the 9 people instead of adding them.)", "people")
    assert F(4, 7) * 56 == 32
    add("A basket has 56 rambutans. %s of them are ripe. Kumar eats 5 of the ripe rambutans. "
        "How many ripe rambutans are left?" % fr(4, 7), 27, [32, 19, 24],
        "1 unit = 56 ÷ 7 = 8. Ripe: 4 units = 32. After Kumar eats 5: 32 − 5 = <b>27</b> rambutans.", "rambutans")
    q = (fig(bars([{"name": "Boys", "segs": [(2, LIGHT, 2, "")]},
                   {"name": "Girls", "segs": [(3, LIGHT, 3, "")], "below": [(0, 3, "27")]}], 44,
                  "boys 2 units and girls 3 units")) +
         "In a choir, the number of boys is %s of the number of girls. There are 27 girls. "
         "How many pupils are in the choir?" % fr(2, 3))
    assert F(2, 3) * 27 == 18
    add(q, 45, [18, 54, 36],
        "Girls: 3 units = 27, so 1 unit = 9. Boys: 2 units = 18. Altogether: 5 units = 5 × 9 = <b>45</b> pupils. "
        "(18 is the number of boys only.)", "pupils")
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    f1 = ("<figure class='sn-fig'>" + set_svg(shaded(12, 8), 6, label="12 counters, 8 shaded") +
          "<figcaption>8 out of 12 counters are shaded: " + fr(8, 12) + " = " + fr(2, 3) + "</figcaption></figure>")
    f2 = ("<figure class='sn-fig'>" + groups_svg([5] * 4, {0}, 3) +
          "<figcaption>" + fr(1, 4) + " of 20: share 20 into 4 equal groups. One group has 5.</figcaption></figure>")
    f3 = ("<figure class='sn-fig'>" + one_bar(5, 3, "35", "?") +
          "<figcaption>" + fr(3, 5) + " of 35: 5 units = 35, 1 unit = 7, 3 units = 21.</figcaption></figure>")
    f4 = ("<figure class='sn-fig'>" + one_bar(3, 1, "?", "8") +
          "<figcaption>" + fr(1, 3) + " of a number is 8: 1 unit = 8, 3 units = 24.</figcaption></figure>")
    return (
        "<h2>The big idea</h2>"
        "<p>A fraction of a set compares a part of the set with the <b>whole set</b>. "
        "The denominator tells you how many equal parts (units) the set is cut into. "
        "The numerator tells you how many of those parts you take.</p>"
        "<h2>What fraction is shaded?</h2>"
        "<p>Count the shaded objects and all the objects. Write shaded over all. Then simplify.</p>"
        + f1 +
        "<h2>Finding a fraction of a set</h2>"
        "<p>To find " + fr(1, 4) + " of a set, share it into 4 equal groups and take one group. "
        "This is the same as dividing by 4.</p>"
        + f2 +
        "<p>For a non-unit fraction such as " + fr(3, 5) + ", find 1 unit first (divide by the denominator), "
        "then multiply by the numerator.</p>"
        + f3
        + ex("Example", "There are 40 pupils in a class. " + fr(3, 4) + " of them walk to school. How many pupils walk?",
             "4 units = 40. 1 unit = 40 ÷ 4 = 10. 3 units = 3 × 10 = 30.", "30 pupils")
        + "<h2>Finding the whole from a part</h2>"
        "<p>If you know a part, find 1 unit first. Then multiply by the number of units in the whole.</p>"
        + f4
        + ex("Example", fr(2, 5) + " of the beads in a box are red. There are 14 red beads. How many beads are in the box?",
             "2 units = 14. 1 unit = 14 ÷ 2 = 7. The whole is 5 units: 5 × 7 = 35.", "35 beads")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Counting groups when the groups are <b>not the same size</b> (1 group out of 3 = " + fr(1, 3) + ")",
             "Count the objects: 2 shaded out of 12 = " + fr(1, 6)],
            ["Dividing by the numerator: " + fr(3, 4) + " of 36 = 36 ÷ 3 × 4 = 48",
             "Divide by the denominator: 36 ÷ 4 = 9, then 3 × 9 = 27"],
            ["Not simplifying: leaving the answer as " + fr(6, 8),
             "Divide the numerator and the denominator by the same number: " + fr(6, 8) + " = " + fr(3, 4)],
            ["Writing shaded over white (4 shaded, 2 white = " + fr(4, 2) + ")",
             "The denominator is <b>all</b> the objects: 4 out of 6 = " + fr(2, 3)],
        ])
    )


FAQ = [
    {"q": "What is fraction of a set in P4 maths?",
     "a": "It means finding a part of a group of objects, such as 3/4 of 20 counters. Students also say what fraction "
          "of a set is shaded and find the whole set when they know a part."},
    {"q": "How do I explain 3/5 of 35 to my child?",
     "a": "Draw a bar of 5 equal units for 35, so 1 unit = 35 ÷ 5 = 7. Then 3 units = 3 × 7 = 21."},
    {"q": "What is the most common mistake in fraction of a set?",
     "a": "Dividing by the numerator instead of the denominator. Another is counting groups of different sizes "
          "instead of counting the objects, and forgetting to give the answer in simplest form."},
    {"q": "Is fraction of a set in the MOE Primary 4 syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus includes fraction as part of a set in Primary 4, "
          "with word problems solved using the model method."},
]


def gen():
    rnd = random.Random(64807)
    sets = [set_shaded(), set_unit(), set_nonunit(), set_whole(), set_words()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        cnt = [0, 0, 0, 0]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            cnt[it["a"]] += 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
        assert cnt == [5, 5, 5, 5], (s["title"], cnt)
    return {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "fraction-of-a-set", "sort": 7,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Fraction of a Set",
        "seo_title": "P4 Fraction of a Set Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Fraction of a set",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Fractions",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Fraction as part of a set",
        "meta_desc": "Free P4 fraction of a set practice: shaded fractions in simplest form, 3/5 of 35, finding the "
                     "whole and bar model word problems. 100 questions with answers.",
        "key_big": "Divide by the denominator to find 1 unit, then multiply by the numerator.",
        "key_sub": "3/5 of 35: 5 units = 35, 1 unit = 35 ÷ 5 = 7, 3 units = 3 × 7 = 21.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
