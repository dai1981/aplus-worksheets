# -*- coding: utf-8 -*-
"""
AU Year 1 Maths (Australian Curriculum v9.0): sharing and grouping. AC9M1N06.
Share equally between 2, 3 and 4; equal or not equal; make groups of 2, 5 and 10;
count the groups to find the total; simple stories.
  python3 tools/gen_au_maths_y1_sharing_grouping.py
Year 1 has no × or ÷ signs: we say "shared equally between", "groups of", "each".
Every answer, every wrong answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
PLATE = "#eef6f0"
RED = "#c0392b"
ORANGE = "#d9822b"
BLUE = "#2e6da4"
PURPLE = "#7b4a9e"
TAN = "#d8a868"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors (no 0 or negatives). Positions are set by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or re.match(r"^0(\D.*)?$", c):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def abcd_item(prompt, right, wrong, kind, style, e):
    """A-D picture question. The picture is built in balance() so the right letter lands on its target."""
    assert len(wrong) == 3 and right not in wrong and len({tuple(w) for w in wrong}) == 3
    return {"q": "", "c": ["A", "B", "C", "D"], "a": 0, "e": e, "_abcd": (prompt, right, wrong, kind, style)}


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label, large=False):
    return ("<svg %sxmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>"
            % ("data-pf='lg' " if large else "", math.ceil(w), math.ceil(h), math.ceil(w), math.ceil(h),
               label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def adds(a, k):
    """4 + 4 + 4"""
    return " + ".join([str(a)] * k)


def counts(a, k):
    """Skip count: 5, 10, 15"""
    return ", ".join(str(a * (i + 1)) for i in range(k))


def lst(xs):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------ small objects (each one is a <g class='o'>)
def item(kind, cx, cy, r=8.5):
    if kind == "counter":
        s = "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, GREEN)
    elif kind == "apple":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>"
             % (cx, cy + 1, r * 0.85, RED, cx, cy - r * 0.6, cx + 2, cy - r * 1.1, GREEN))
    elif kind == "grape":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
             "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#ffffff' opacity='0.55'/>"
             % (cx, cy, r * 0.8, PURPLE, cx - r * 0.3, cy - r * 0.3, r * 0.2))
    elif kind == "strawberry":
        s = ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='%s'/>"
             "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='%s'/>"
             % (cx - r, cy - r * 0.45, cx - r * 0.9, cy + r * 0.6, cx, cy + r * 1.05,
                cx + r * 0.9, cy + r * 0.6, cx + r, cy - r * 0.45, RED,
                cx - r * 0.8, cy - r * 0.5, cx - r * 0.3, cy - r * 1.05, cx, cy - r * 0.7,
                cx + r * 0.3, cy - r * 1.05, cx + r * 0.8, cy - r * 0.5, GREEN))
    elif kind == "biscuit":
        s = ("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='#9a6a2a' stroke-width='1.2'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/><circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/>"
             "<circle cx='%.1f' cy='%.1f' r='1.6' fill='#6b4a2a'/>"
             % (cx, cy, r * 0.9, TAN, cx - 3, cy - 2, cx + 3, cy - 1, cx, cy + 3))
    elif kind == "shell":
        s = ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#f4d7b5' stroke='#a0623a' stroke-width='1.2'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#a0623a' stroke-width='1'/>"
             % (cx - r, cy + r * 0.6, cx, cy - r * 1.6, cx + r, cy + r * 0.6, cx, cy + r * 0.6, cx, cy - r * 0.45))
    elif kind == "star":
        pts = []
        for k in range(10):
            rr = r * 1.1 if k % 2 == 0 else r * 0.46
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
        s = "<polygon points='%s' fill='%s'/>" % (" ".join(pts), ORANGE)
    elif kind == "orange":
        s = ("<path d='M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f Z' fill='#f5a623' stroke='%s' stroke-width='1.5'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#fff3d6' stroke-width='1'/>"
             "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#fff3d6' stroke-width='1'/>"
             % (cx - r, cy - r * 0.3, r, r, cx + r, cy - r * 0.3, ORANGE,
                cx, cy - r * 0.3, cx - r * 0.55, cy + r * 0.45, cx, cy - r * 0.3, cx + r * 0.55, cy + r * 0.45))
    elif kind == "lolly":
        s = ("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
             "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
             "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>"
             % (cx - r * 0.4, cy, cx - r * 1.05, cy - r * 0.5, cx - r * 1.05, cy + r * 0.5, BLUE,
                cx + r * 0.4, cy, cx + r * 1.05, cy - r * 0.5, cx + r * 1.05, cy + r * 0.5, BLUE,
                cx, cy, r * 0.62, BLUE))
    elif kind == "sausage":
        s = ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='#a0522d'/>"
             % (cx - r * 1.05, cy - r * 0.45, r * 2.1, r * 0.9, r * 0.45))
    else:
        raise ValueError(kind)
    return "<g class='o'>" + s + "</g>"


NAMES = {"counter": "counters", "apple": "apples", "grape": "grapes", "strawberry": "strawberries",
         "biscuit": "biscuits", "shell": "shells", "star": "stickers", "orange": "orange slices",
         "lolly": "lollies", "sausage": "sausages"}


def n_items(svg):
    return svg.count("<g class='o'>")


def face(x, y):
    cx, cy = x + 20, y + 20
    return ("<g class='k'><circle cx='%d' cy='%d' r='19' fill='#f6dcc0' stroke='#9a6a3a' stroke-width='1.5'/>"
            "<circle cx='%d' cy='%d' r='3.2' fill='%s'/><circle cx='%d' cy='%d' r='3.2' fill='%s'/>"
            "<path d='M %d %d Q %d %d %d %d' fill='none' stroke='%s' stroke-width='2'/></g>"
            % (cx, cy, cx - 7, cy - 4, INK, cx + 7, cy - 4, INK, cx - 7, cy + 6, cx, cy + 12, cx + 7, cy + 6, INK))


def n_faces(svg):
    return svg.count("<g class='k'>")


# ------------------------------------------------------------ pictures
S = 24          # one object cell


def loose_body(n, kind, x0, y0):
    """n objects in rows of 10 (a small gap after 5). Returns body, w, h."""
    el = []
    for i in range(n):
        rr, cc = divmod(i, 10)
        el.append(item(kind, x0 + cc * S + (8 if cc >= 5 else 0) + S / 2.0, y0 + rr * S + S / 2.0))
    cols = min(n, 10)
    return "".join(el), cols * S + (8 if cols > 5 else 0), ((n + 9) // 10) * S


def loose_svg(n, kind):
    M = 5
    body, w, h = loose_body(n, kind, M, M)
    svg = svg_wrap(w + 2 * M, h + 2 * M, body, "%d %s" % (n, NAMES[kind]), large=n > 10 or w > 2.2 * h)
    assert n_items(svg) == n
    return svg


def faces_svg(n):
    rows = (n + 6) // 7
    per = (n + rows - 1) // rows
    el = []
    for i in range(n):
        r, c = divmod(i, per)
        el.append(face(4 + c * 46, 4 + r * 46))
    svg = svg_wrap(8 + per * 46 - 6, 8 + rows * 46 - 6, "".join(el), "%d children" % n, large=n > 7)
    assert n_faces(svg) == n
    return svg


def share_svg(n, k, kind):
    """n objects on top, k children below: the objects still have to be shared."""
    M = 5
    body, w, h = loose_body(n, kind, M, M)
    fw = k * 46 - 6
    W = max(w, fw) + 2 * M
    body = "<g transform='translate(%.1f,0)'>%s</g>" % ((W - w - 2 * M) / 2.0, body)
    fy = M + h + 12
    fx = (W - fw) / 2.0
    body += "".join(face(fx + i * 46, fy) for i in range(k))
    svg = svg_wrap(W, fy + 40 + M, body, "%d %s to share between %d children" % (n, NAMES[kind], k),
                   large=n > 10 or W > 2.2 * (fy + 40 + M))
    assert n_items(svg) == n and n_faces(svg) == k
    return svg


def layout(n):
    """Rows and columns inside one plate or ring."""
    if n <= 3:
        return 1, max(n, 1)
    if n <= 6:
        return 2, (n + 1) // 2
    return 2, 5


def groups_body(sizes, x0, y0, kind, style, s, r, per_row, G):
    """Plates (sharing) or dashed rings (groups) in rows of per_row. Every box has the size of the largest group."""
    rows_in, cols_in = layout(max(sizes))
    P = 6
    bw, bh = cols_in * s + 2 * P, rows_in * s + 2 * P
    el = []
    for k, n in enumerate(sizes):
        br, bc = divmod(k, per_row)
        bx, by = x0 + bc * (bw + G), y0 + br * (bh + G)
        if style == "plate":
            el.append("<rect class='p' x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%.1f' fill='%s' stroke='%s' "
                      "stroke-width='2.5'/>" % (bx, by, bw, bh, min(bw, bh) / 2.0, PLATE, GREEN))
        else:
            el.append("<rect class='g' x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='12' fill='none' stroke='%s' "
                      "stroke-width='2.5' stroke-dasharray='6 4'/>" % (bx, by, bw, bh, GREY))
        # centre the objects of a smaller group inside its box
        rows_n = 1 if n <= cols_in else 2
        top = by + (bh - rows_n * s) / 2.0
        for i in range(n):
            rr, cc = divmod(i, cols_in)
            in_row = min(cols_in, n - rr * cols_in)
            left = bx + (bw - in_row * s) / 2.0
            el.append(item(kind, left + cc * s + s / 2.0, top + rr * s + s / 2.0, r))
    nrow = (len(sizes) + per_row - 1) // per_row
    ncol = min(len(sizes), per_row)
    return "".join(el), ncol * bw + (ncol - 1) * G, nrow * bh + (nrow - 1) * G


def per_row_for(sizes):
    big = max(sizes)
    lim = 3 if big >= 7 else (4 if big >= 4 else 5)
    if len(sizes) <= lim:
        return len(sizes)
    rows = (len(sizes) + lim - 1) // lim
    return (len(sizes) + rows - 1) // rows


def groups_svg(sizes, kind, style="ring", label=None):
    M = 5
    body, w, h = groups_body(sizes, M, M, kind, style, S, 8.5, per_row_for(sizes), 12)
    word = "plates" if style == "plate" else "groups"
    if label is None:
        if len(set(sizes)) == 1:
            label = "%d %s of %d %s" % (len(sizes), word, sizes[0], NAMES[kind])
        else:
            label = "%d %s with %s %s" % (len(sizes), word, lst(sizes), NAMES[kind])
    svg = svg_wrap(w + 2 * M, h + 2 * M, body, label, large=(w + 2 * M) > 2.2 * (h + 2 * M))
    assert n_items(svg) == sum(sizes)
    assert svg.count("class='%s'" % ("p" if style == "plate" else "g")) == len(sizes)
    return svg


def abcd_svg(panels, kind, style):
    """Four plate or ring pictures side by side, labelled A to D. panels: lists of group sizes."""
    s, r, G, PAD = 18, 6.5, 6, 10
    built = []
    for p in panels:
        assert len(p) <= 6 and max(p) <= 10
        pr = {4: 2, 5: 3, 6: 3}.get(len(p), len(p))
        built.append(groups_body(p, 0, 0, kind, style, s, r, pr, G))
    PW = max(b[1] for b in built) + 2 * PAD
    H = 30 + max(b[2] for b in built) + 8
    el = []
    for k, (body, w, h) in enumerate(built):
        x0 = k * PW
        if k:
            el.append("<line x1='%.1f' y1='4' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>" % (x0, x0, H - 4, GREY))
        el.append(text(x0 + 8, 20, "ABCD"[k], 18, "start"))
        el.append("<g transform='translate(%.1f,30)'>%s</g>" % (x0 + (PW - w) / 2.0, body))
    svg = svg_wrap(4 * PW, H, "".join(el), "four pictures labelled A to D", large=True)
    assert n_items(svg) == sum(sum(p) for p in panels)
    return svg


# ============================================================ set 1: share equally between 2, 3 and 4
def set_share(P):
    its = []
    # already shared: count one plate
    for n, k, kd in [(6, 2, "apple"), (9, 3, "strawberry"), (8, 4, "biscuit"), (10, 2, "grape"), (12, 3, "counter")]:
        a = n // k
        e = ("Count the %s on one plate: %d. Every plate has the same. So each plate has <b>%d</b>. "
             "Check: %s = %d." % (NAMES[kd], a, a, adds(a, k), n))
        its.append(mcq(fig(groups_svg([a] * k, kd, "plate")) +
                       "%d %s are shared equally on %d plates. How many are on each plate?" % (n, NAMES[kd], k),
                       a, [k, n, a + 1, a - 1, n - k], e))
    # share loose objects between children
    for n, k, kd in [(4, 2, "lolly"), (6, 3, "apple"), (8, 2, "grape"), (8, 4, "strawberry"), (9, 3, "biscuit"),
                     (10, 2, "shell"), (12, 4, "counter"), (12, 3, "star"), (14, 2, "orange"), (15, 3, "grape"),
                     (16, 2, "counter"), (16, 4, "shell"), (18, 3, "apple"), (18, 2, "star"), (20, 4, "lolly")]:
        a = n // k
        e = ("Give one to each child, again and again, until none are left. Each child gets <b>%d</b>. "
             "Check: %s = %d." % (a, adds(a, k), n))
        its.append(mcq(fig(share_svg(n, k, kd)) +
                       "Share the %d %s equally between %d children. How many does each child get?"
                       % (n, NAMES[kd], k), a, [k, n, a + 1, n - k, a - 1], e))
    assert len(its) == 20, len(its)
    return {"title": "Share equally between 2, 3 and 4", "items": its}


# ============================================================ set 2: equal or not equal
def set_equal(P):
    its = []
    # is it shared equally?
    for sizes, kd in [([4, 3], "grape"), ([5, 5], "apple"), ([3, 3, 3], "strawberry"), ([2, 3, 2], "biscuit"),
                      ([4, 4, 4, 4], "counter")]:
        n, k = sum(sizes), len(sizes)
        if len(set(sizes)) == 1:
            right = "Yes. %d on each" % sizes[0]
            e = "Every plate has %d. They are all the same, so it is equal: <b>%d on each</b>." % (sizes[0], sizes[0])
            w = ["Yes. %d on each" % n, "Yes. %d on each" % k, "No. Not the same", "Yes. %d on each" % (sizes[0] + 1)]
        else:
            right = "No. Not the same"
            e = ("The plates have %s. They are not all the same, so it is <b>not equal</b>. "
                 "Equal means every plate has the same number." % lst(sizes))
            w = ["Yes. %d on each" % max(sizes), "Yes. %d on each" % n, "Yes. %d on each" % k,
                 "Yes. %d on each" % min(sizes)]
        its.append(mcq(fig(groups_svg(sizes, kd, "plate")) + "Is this shared equally?", right, w, e))

    # which shows equal sharing?
    for n, k, kd, wrong in [(8, 2, "apple", [[5, 3], [6, 2], [7, 1]]),
                            (6, 3, "strawberry", [[3, 2, 1], [4, 1, 1], [3, 3]]),
                            (10, 2, "grape", [[6, 4], [7, 3], [2, 2, 2, 2, 2]]),
                            (9, 3, "counter", [[4, 3, 2], [4, 4, 1], [5, 4]]),
                            (12, 4, "biscuit", [[4, 4, 4], [4, 3, 3, 2], [2, 3, 4, 3]]),
                            (16, 4, "shell", [[5, 4, 4, 3], [8, 8], [6, 4, 3, 3]])]:
        a = n // k
        assert all(sum(w) == n for w in wrong)
        e = ("<b>{L}</b> has %d plates with %d on each. Check two things: the right number of plates, "
             "and the same number on every plate." % (k, a))
        its.append(abcd_item("Which shows %d %s shared equally between %d plates?" % (n, NAMES[kd], k),
                             [a] * k, wrong, kd, "plate", e))

    # which is NOT equal?
    for right, wrong, kd in [([4, 3], [[2, 2], [5, 5], [3, 3]], "apple"),
                             ([2, 3, 2], [[3, 3, 3], [2, 2, 2], [1, 1, 1]], "grape"),
                             ([3, 3, 2, 3], [[2, 2, 2, 2], [4, 4, 4, 4], [3, 3, 3, 3]], "biscuit")]:
        assert all(len(set(w)) == 1 for w in wrong) and len(set(right)) > 1
        e = ("<b>{L}</b> has %s. One plate is different, so it is not equal. "
             "In the other pictures every plate has the same number." % lst(right))
        its.append(abcd_item("Which plates are <b>not</b> shared equally?", right, wrong, kd, "plate", e))

    # make it equal
    for sizes, kd in [([5, 3], "grape"), ([6, 4], "strawberry"), ([6, 2], "apple"), ([7, 1], "biscuit")]:
        big, small = sizes
        mv = (big - small) // 2
        a = (big + small) // 2
        one = NAMES[kd][:-1] if mv == 1 else NAMES[kd]
        if kd == "strawberry" and mv == 1:
            one = "strawberry"
        e = ("%d shared between 2 is %d each. Move <b>%d</b> %s from the %d to the %d. Now both have %d. "
             "(Moving %d makes %d and %d.)" % (big + small, a, mv, one, big, small, a, big - small,
                                               big - (big - small), small + (big - small)))
        its.append(mcq(fig(groups_svg(sizes, kd, "plate")) +
                       "Make the 2 plates equal. How many %s must move?" % NAMES[kd],
                       mv, [big - small, a, mv + 1, small, big], e))

    # is it fair? (stories with a picture)
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    its.append(mcq(fig(groups_svg([6, 4], "grape", "plate")) +
                   "%s and %s share 10 grapes. %s gets 6. %s gets 4. Is it fair?" % (n1, n2, n1, n2),
                   "No. %s has more." % n1, ["Yes. It makes 10.", "No. %s has more." % n2, "Yes. Both get 6."],
                   "6 and 4 are not the same. <b>%s has more.</b> It is not fair. Fair is 5 each." % n1))
    n1, he1, _ = P.next()
    n2, _, _ = P.next()
    n3, _, _ = P.next()
    its.append(mcq(fig(groups_svg([3, 3, 3], "strawberry", "plate")) +
                   "%s shares 9 strawberries with %s and %s. Each gets 3. Is it fair?" % (n1, n2, n3),
                   "Yes. Each gets 3.", ["No. %s has more." % n1, "Yes. Each gets 9.", "No. 9 is too many."],
                   "3 people get 3 each: 3 + 3 + 3 = 9. Everyone has the same, so <b>it is fair</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Equal or not equal?", "items": its}


# ============================================================ set 3: make groups of 2, 5 and 10
def set_groups(P):
    its = []
    # already in rings
    for t, s, kd in [(8, 2, "apple"), (10, 5, "star"), (20, 10, "counter"), (12, 2, "grape"), (15, 5, "shell"),
                     (14, 2, "strawberry"), (30, 10, "counter")]:
        g = t // s
        e = ("Count the rings: %s. There are <b>%d</b> groups. (%d is how many are in each group.)"
             % (counts(1, g), g, s))
        its.append(mcq(fig(groups_svg([s] * g, kd)) + "%d %s are in groups of %d. How many groups are there?"
                       % (t, NAMES[kd], s), g, [s, t, g + 1, g - 1, t - s], e))
    # loose: make the groups
    for t, s, kd in [(10, 2, "shell"), (20, 5, "counter"), (40, 10, "grape"), (16, 2, "lolly"), (25, 5, "star"),
                     (18, 2, "counter"), (35, 5, "shell"), (50, 10, "counter"), (20, 2, "biscuit")]:
        g = t // s
        e = ("Circle %d at a time. Count by %ds: %s. You said %d numbers, so there are <b>%d</b> groups."
             % (s, s, counts(s, g), g, g))
        its.append(mcq(fig(loose_svg(t, kd)) + "Put the %d %s in groups of %d. How many groups?" % (t, NAMES[kd], s),
                       g, [s, t, g + 1, t - s, g - 1], e))
    # which picture shows groups of ...
    for t, s, kd, wrong in [(10, 5, "counter", [[2, 2, 2, 2, 2], [4, 4, 2], [3, 3, 4]]),
                            (12, 2, "apple", [[6, 6], [3, 3, 3, 3], [4, 4, 4]]),
                            (15, 5, "star", [[3, 3, 3, 3, 3], [5, 5, 4, 1], [10, 5]]),
                            (20, 10, "grape", [[5, 5, 5, 5], [10, 5, 5], [4, 4, 4, 4, 4]])]:
        g = t // s
        assert all(sum(w) == t for w in wrong)
        e = ("Groups of %d means %d in <b>every</b> ring. <b>{L}</b> has %d rings of %d. "
             "Do not mix it up with %d rings." % (s, s, g, s, s))
        its.append(abcd_item("Which shows %d %s in groups of %d?" % (t, NAMES[kd], s), [s] * g, wrong, kd, "ring", e))
    assert len(its) == 20, len(its)
    return {"title": "Make groups of 2, 5 and 10", "items": its}


# ============================================================ set 4: count the groups to find the total
def set_total(P):
    its = []
    for g, n, kd in [(3, 2, "apple"), (4, 2, "shell"), (2, 5, "star"), (6, 2, "counter"), (3, 5, "strawberry"),
                     (2, 10, "counter"), (4, 5, "grape"), (3, 10, "lolly"), (5, 5, "biscuit"), (4, 10, "counter")]:
        t = g * n
        e = ("Say one number for each group. Count by %ds: %s. There are <b>%d</b> %s. "
             "(%d is the number of groups, not the %s.)" % (n, counts(n, g), t, NAMES[kd], g, NAMES[kd]))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "How many %s are there altogether?" % NAMES[kd],
                       t, [g, g + n, t + n, t - n, n], e))
    for g, n, kd in [(2, 3, "biscuit"), (2, 4, "strawberry"), (3, 3, "orange"), (3, 4, "sausage"),
                     (4, 3, "apple"), (4, 4, "grape")]:
        t = g * n
        e = ("Each plate has %d. There are %d plates. Add: %s = <b>%d</b>. (Not %d: that is just the plates.)"
             % (n, g, adds(n, g), t, g))
        its.append(mcq(fig(groups_svg([n] * g, kd, "plate")) +
                       "Each plate has %d %s. How many %s altogether?" % (n, NAMES[kd], NAMES[kd]),
                       t, [g, g + n, t + n, t - n, n], e))
    for g, n, kd in [(3, 4, "counter"), (2, 5, "apple"), (4, 2, "star"), (5, 3, "shell")]:
        right = "%d groups of %d" % (g, n)
        e = ("Count the rings: %d. Count inside one ring: %d. So it is <b>%s</b>. That is %d altogether."
             % (g, n, right, g * n))
        its.append(mcq(fig(groups_svg([n] * g, kd)) + "Which words match the picture?", right,
                       ["%d groups of %d" % (n, g), "%d groups of %d" % (g, n + 1), "%d groups of %d" % (g + 1, n)], e))
    assert len(its) == 20, len(its)
    return {"title": "Count the groups to find the total", "items": its}


# ============================================================ set 5: stories
def set_story(P):
    its = []

    def add(q, a, w, e, unit):
        its.append(mcq(q, "%d %s" % (a, unit), ["%d %s" % (x, unit) for x in w if x > 0], e))

    nm, he, his = P.next()
    fr, _, _ = P.next()
    add(fig(loose_svg(12, "grape")) + "%s has 12 grapes at recess. %s shares them equally with %s. "
        "How many does each child get?" % (nm, cap(he), fr), 6, [12, 2, 10, 5, 7],
        "2 children share 12. Give one each, again and again. Each gets <b>6</b>. Check: 6 + 6 = 12.", "grapes")
    nm, he, his = P.next()
    fr, _, _ = P.next()
    add(fig(share_svg(10, 2, "shell")) + "%s and %s find 10 shells at the beach. They share them equally. "
        "How many shells each?" % (nm, fr), 5, [10, 2, 8, 4, 6],
        "10 shared between 2 children is <b>5</b> each. Check: 5 + 5 = 10.", "shells")
    add(fig(share_svg(6, 3, "sausage")) + "At the sausage sizzle, 3 friends share 6 sausages equally. "
        "How many sausages each?", 2, [3, 6, 4, 1],
        "Give one each: that uses 3. Give one each again: that uses 6. Each friend gets <b>2</b>. "
        "Check: 2 + 2 + 2 = 6.", "sausages")
    add(fig(share_svg(16, 4, "orange")) + "At footy, 4 players share 16 orange slices equally. "
        "How many slices each?", 4, [16, 12, 5, 3],
        "Give one slice to each player, again and again, until none are left. Each player gets <b>4</b>. "
        "Check: 4 + 4 + 4 + 4 = 16.", "slices")
    add(fig(groups_svg([5, 5, 5], "apple")) + "There are 3 bags. Each bag has 5 apples. "
        "How many apples altogether?", 15, [3, 8, 5, 20, 10],
        "Count by 5s, one number for each bag: 5, 10, 15. There are <b>15</b> apples.", "apples")
    add(fig(groups_svg([3, 3, 3, 3], "biscuit", "plate")) + "At the class party there are 4 plates. "
        "Each plate has 3 biscuits. How many biscuits altogether?", 12, [4, 7, 3, 15, 9],
        "3 + 3 + 3 + 3 = <b>12</b> biscuits. (4 is the number of plates.)", "biscuits")
    nm, he, his = P.next()
    add(fig(loose_svg(15, "apple")) + "%s has 15 apples. %s puts 5 in each bag. How many bags does %s fill?"
        % (nm, cap(he), he), 3, [5, 15, 10, 4],
        "Count by 5s to 15: 5, 10, 15. That is 3 fives, so <b>3</b> bags.", "bags")
    add(fig(loose_svg(20, "star")) + "The teacher has 20 stickers. She gives 5 stickers to each student. "
        "How many students get stickers?", 4, [5, 20, 15, 3],
        "Count by 5s to 20: 5, 10, 15, 20. That is 4 fives, so <b>4</b> students.", "students")
    add(fig(faces_svg(14)) + "There are 14 children. They sit 2 at each table. How many tables do they need?",
        7, [2, 14, 12, 6, 8],
        "Count by 2s to 14: 2, 4, 6, 8, 10, 12, 14. That is 7 twos, so <b>7</b> tables.", "tables")
    add(fig(faces_svg(20)) + "20 students make teams of 5 for sport. How many teams are there?", 4,
        [5, 20, 15, 3], "Count by 5s to 20: 5, 10, 15, 20. That is <b>4</b> teams of 5.", "teams")
    nm, he, his = P.next()
    add(fig(loose_svg(30, "shell")) + "%s has 30 shells. %s puts them in groups of 10. How many groups?"
        % (nm, cap(he)), 3, [10, 30, 20, 4],
        "Count by 10s to 30: 10, 20, 30. That is <b>3</b> groups of 10.", "groups")
    add(fig(groups_svg([2] * 6, "orange")) + "6 children each get 2 orange slices. How many slices is that?",
        12, [6, 8, 2, 14, 10],
        "Count by 2s, one number for each child: 2, 4, 6, 8, 10, 12. That is <b>12</b> slices.", "slices")
    add(fig(groups_svg([5] * 4, "lolly")) + "There are 4 party bags. Each bag has 5 lollies. "
        "How many lollies altogether?", 20, [4, 9, 25, 15],
        "Count by 5s: 5, 10, 15, 20. There are <b>20</b> lollies. (4 + 5 = 9 adds the bags to the lollies.)",
        "lollies")
    nm, he, his = P.next()
    add(fig(share_svg(9, 3, "biscuit")) + "%s shares 9 biscuits equally between 3 friends. "
        "How many does each friend get?" % nm, 3, [9, 6, 4, 2],
        "Give one each, again and again. Each friend gets <b>3</b>. Check: 3 + 3 + 3 = 9.", "biscuits")
    add(fig(groups_svg([10, 10], "strawberry")) + "There are 2 punnets of strawberries. Each has 10. "
        "How many strawberries altogether?", 20, [2, 12, 10, 30],
        "Count by 10s: 10, 20. There are <b>20</b> strawberries.", "strawberries")
    nm, he, his = P.next()
    add(fig(share_svg(20, 4, "grape")) + "At lunch, %s shares 20 grapes equally between 4 friends. "
        "How many grapes each?" % nm, 5, [4, 20, 16, 6],
        "Give one each, again and again, until none are left. Each friend gets <b>5</b>. "
        "Check: 5 + 5 + 5 + 5 = 20.", "grapes")

    # mistakes
    nm, he, his = P.next()
    its.append(mcq(fig(groups_svg([6, 4], "strawberry", "plate")) +
                   "%s shares 10 strawberries on 2 plates. %s puts 6 and 4. How can %s make it fair?"
                   % (nm, cap(he), he), "Move 1 to the 4", ["Move 2 to the 4", "Move 1 to the 6", "It is fair now"],
                   "10 shared between 2 is 5 each. Move <b>1</b> from the 6 to the 4. Now 5 and 5. "
                   "(Moving 2 makes 4 and 6.)"))
    nm, he, his = P.next()
    add(fig(groups_svg([5, 5, 5], "counter")) + "%s has 3 bags of 5 marbles. %s says, “I have 3 marbles.” "
        "How many marbles does %s really have?" % (nm, cap(he), he), 15, [3, 8, 5, 10],
        "3 is the number of bags. Count the marbles by 5s: 5, 10, 15. %s has <b>15</b> marbles." % nm, "marbles")
    add(fig(faces_svg(18)) + "18 students work in pairs. A pair is 2 students. How many pairs are there?",
        9, [2, 18, 16, 8, 10],
        "Count by 2s to 18: 2, 4, 6, 8, 10, 12, 14, 16, 18. That is <b>9</b> pairs.", "pairs")
    nm, he, his = P.next()
    add(fig(share_svg(8, 4, "lolly")) + "%s shares 8 lollies equally with 3 friends. "
        "How many lollies does each child get?" % nm, 2, [4, 3, 8, 1],
        "%s and 3 friends make 4 children. 8 shared between 4 is <b>2</b> each. "
        "Check: 2 + 2 + 2 + 2 = 8. (4 each is sharing between only 2.)" % nm, "lollies")
    assert len(its) == 20, len(its)
    return {"title": "Sharing and grouping stories", "items": its}


# ============================================================ balance (and build A-D pictures)
def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            if "_abcd" in it:
                prompt, right, wrong, kind, style = it.pop("_abcd")
                wrong = list(wrong)
                rnd.shuffle(wrong)
                panels = wrong[:t] + [right] + wrong[t:]
                it["q"] = fig(abcd_svg(panels, kind, style)) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
                continue
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


# ============================================================ lesson
def body_html():
    return (
        "<h2>Sharing equally</h2>"
        "<p>Sharing equally means everyone gets the <b>same</b> number. "
        "Give one to each person. Then give one each again. Keep going until none are left.</p>"
        "<figure class='sn-fig'>" + share_svg(8, 2, "apple")
        + "<figcaption>8 apples to share between 2 children.</figcaption></figure>"
        "<figure class='sn-fig'>" + groups_svg([4, 4], "apple", "plate")
        + "<figcaption>Each child gets 4. Check: 4 + 4 = 8.</figcaption></figure>"
        + ex("Example", "Share 12 grapes equally between 3 children.",
             "Give one each, again and again. Each child gets 4. Check: 4 + 4 + 4 = 12.", "4 grapes each")
        + "<h2>Equal or not equal?</h2>"
        "<p>Look at every plate. If they all have the same number, it is <b>equal</b>. "
        "If one plate has more, it is <b>not equal</b>. It is not fair.</p>"
        "<figure class='sn-fig'>" + groups_svg([3, 3, 3], "strawberry", "plate")
        + "<figcaption>3, 3 and 3: equal.</figcaption></figure>"
        "<figure class='sn-fig'>" + groups_svg([4, 3, 2], "strawberry", "plate")
        + "<figcaption>4, 3 and 2: not equal.</figcaption></figure>"
        + "<h2>Making groups</h2>"
        "<p>Grouping means putting the <b>same number</b> in each group. "
        "Circle 2, 5 or 10 at a time. Then count the groups.</p>"
        "<figure class='sn-fig'>" + groups_svg([5, 5, 5], "shell")
        + "<figcaption>15 shells in groups of 5. Count by 5s: 5, 10, 15. That is 3 groups.</figcaption></figure>"
        + "<h2>Count the groups to find the total</h2>"
        "<p>Say one number for each group. Count by 2s, 5s or 10s.</p>"
        "<figure class='sn-fig'>" + groups_svg([2, 2, 2, 2], "counter")
        + "<figcaption>4 groups of 2: 2, 4, 6, 8. There are 8 counters.</figcaption></figure>"
        + ex("Example", "There are 3 bags. Each bag has 10 marbles. How many marbles?",
             "Count by 10s, one number for each bag: 10, 20, 30.", "30 marbles")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Unequal shares: 10 grapes as 6 and 4", "Everyone gets the same: 5 and 5"],
            ["Counting the groups, not the things: 3 groups of 5 = 3", "Count every object: 5, 10, 15"],
            ["Mixing up “groups of 2” and “2 groups”", "Groups of 2 means 2 in every group"],
            ["Forgetting yourself: share 8 with 3 friends as 3 children", "You and 3 friends are 4 children"],
        ])
    )


FAQ = [
    {"q": "Do Year 1 students learn division?",
     "a": "Not with the ÷ sign yet. In the Australian Curriculum (AC9M1N06), Year 1 students solve practical problems by sharing equally and making equal groups, using objects and drawings. This is the start of division and multiplication."},
    {"q": "What is the difference between sharing and grouping?",
     "a": "In sharing, you know how many people and find how many each gets (12 shared between 3 is 4 each). In grouping, you know how many go in each group and find how many groups (12 in groups of 3 is 4 groups)."},
    {"q": "How can I practise sharing and grouping at home?",
     "a": "Share real things fairly, like grapes, pegs or Lego bricks, between family members, one at a time. Then put socks in pairs or coins in groups of 5 and 10, and count the groups."},
    {"q": "Why does my child count the groups instead of the objects?",
     "a": "It is a very common Year 1 mistake. Ask “How many in each group?” first, then skip count by that number, saying one number for each group."},
]


def gen():
    rnd = random.Random(1806)
    P = People(rnd)
    sets = [set_share(P), set_equal(P), set_groups(P), set_total(P), set_story(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert "_abcd" not in it and "{" not in it["e"]
            assert it["q"].count("<svg") == 1, it["q"]
            assert "×" not in it["q"] + it["e"] and "÷" not in it["q"] + it["e"]
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert 0 < int(tok) <= 120, c
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "sharing-and-grouping", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Sharing and Grouping",
        "seo_title": "Year 1 Sharing and Grouping Worksheets: Equal Shares and Equal Groups (Free, Australian Curriculum)",
        "short_title": "Sharing and grouping",
        "domain": "Number",
        "standard_code": "AC9M1N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Use mathematical modelling to solve practical problems involving equal sharing and grouping; represent the situations with diagrams, physical and virtual materials, and use calculation strategies to solve the problem",
        "meta_desc": "Free Year 1 maths worksheets on sharing and grouping: share equally between 2, 3 and 4, spot equal and unequal shares, make groups of 2, 5 and 10, count groups to find the total, and solve simple stories. 100 picture questions with an answer key, following the Australian Curriculum.",
        "key_big": "Sharing equally means everyone gets the same. Grouping means the same number in every group.",
        "key_sub": "Give out one at a time until none are left. To find the total, count by 2s, 5s or 10s, saying one number for each group.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
