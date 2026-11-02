# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Ordinal Numbers
(MOE 2021 Primary Mathematics Syllabus, Standard, Primary 1: Whole Numbers —
 ordinal numbers (first, second, up to tenth) and symbols (1st, 2nd, 3rd, etc.))
  python3 tools/gen_sg_maths_p1_ordinal_numbers.py
Position in a queue (first to tenth), the symbols 1st, 2nd, 3rd, 4th ..., position from the left or
the right, just before / just after / between, and word problems (a race, a queue at the canteen).
Very short sentences for 6-7 year olds and a picture in almost every question.
Every picture is drawn from the same data the answer is worked out from, so picture and answer agree.
Wrong answers come from real mistakes: counting from the wrong end (3rd from the front read as 3rd from
the back), counting one too many or one too few, saying the counting word ("three") instead of the
position word ("third"), the wrong endings 3th, 2st, 1nd, the spellings "nineth" and "forth",
counting the child himself when asked how many are in front, counting both ends when asked how many
are between, and the podium mix-up (the tallest block is 1st, not the one on the left).
Singapore English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
SOFT = "#8a8378"
FONT = "Arial, Helvetica, sans-serif"

ORD = [None, "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
CARD = [None, "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
SUF = {1: "st", 2: "nd", 3: "rd"}


def S(n):
    assert 1 <= n <= 10, n
    return "%d%s" % (n, SUF.get(n, "th"))


assert [S(k) for k in (1, 2, 3, 4, 10)] == ["1st", "2nd", "3rd", "4th", "10th"]

BOYS = ["Ali", "Ahmad", "Hafiz", "Raju", "Kumar", "Arjun", "Ethan", "Ryan", "Wei Ming", "Jun Jie", "Zhi Hao"]
GIRLS = ["Siti", "Nurul", "Farah", "Priya", "Devi", "Kavya", "Chloe", "Sarah", "Mei Ling", "Hui Min", "Xin Yi"]


def he(nm):
    return "he" if nm in BOYS else "she"


def him(nm):
    return "him" if nm in BOYS else "her"


# ------------------------------------------------------------ helpers
def mcq(q, correct, wrong, e):
    """4 choices: correct + 3 wrong. Positions are set later by balance()."""
    correct = str(correct)
    wrong = [str(w) for w in wrong]
    assert len(wrong) == 3 and len(set(wrong + [correct])) == 4, (q, correct, wrong)
    assert ("<b>%s</b>" % correct) in e, (correct, e)
    return {"q": q, "c": [correct] + wrong, "a": 0, "e": e}


def pick3(correct, pool, extra):
    """The first 3 different wrong answers from pool, then from extra."""
    out = []
    for w in list(pool) + list(extra):
        if w is None or w == correct or w in out:
            continue
        out.append(w)
        if len(out) == 3:
            return out
    raise AssertionError((correct, pool, extra))


def fixed(q, labels, ans, e):
    """Choices are labels for parts of one picture (A, B ...). They keep this order."""
    assert ans in labels and len(labels) == 4 and len(set(labels)) == 4
    assert ("<b>%s</b>" % ans) in e, (ans, e)
    return {"q": q, "c": list(labels), "a": labels.index(ans), "e": e, "_fixed": True}


def balance(sets, rnd):
    """Each answer position (A to D) is correct 5 times in every set. Picture-label items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("_fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("_fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=15, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


# rough Arial bold widths (em) so labels never run into each other
_W = {"i": .28, "l": .28, "j": .28, "t": .33, "f": .33, "r": .39, " ": .28, "I": .28, "J": .56,
      "m": .89, "w": .78, "M": .83, "W": .94}


def tw(t, fs):
    return sum(_W.get(ch, .72 if ch.isupper() else .61) for ch in t) * fs


# ------------------------------------------------------------ pictures: people
SHIRT = ["#d6453b", "#3b7dd8", "#4fae74", "#f2c230", "#8e6ccf", "#f08a24", "#2bb3b1", "#d65aa0", "#7a8b99", "#a0522d"]


def child(x, base, colour):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
            "<rect x='%.1f' y='%.1f' width='18' height='19' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
            "<circle cx='%.1f' cy='%.1f' r='8' fill='#f1c9a0' stroke='%s' stroke-width='2'/>"
            % (x - 4, base - 14, x - 5, base - 1, INK, x + 4, base - 14, x + 5, base - 1, INK,
               x - 9, base - 32, colour, INK, x, base - 41, INK))


def arrow_down(x, y0, y1, col=RED):
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
            "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
            % (x, y0, x, y1 - 6, col, x - 6, y1 - 8, x + 6, y1 - 8, x, y1, col))


def stall(x, base):
    """A canteen stall: counter with a striped roof. 44 wide."""
    s = ["<rect x='%.1f' y='%.1f' width='44' height='34' fill='#f6e7c8' stroke='%s' stroke-width='2'/>" % (x, base - 34, INK)]
    for k in range(4):
        s.append("<rect x='%.1f' y='%.1f' width='11' height='12' fill='%s' stroke='%s' stroke-width='1'/>"
                 % (x + k * 11, base - 66, RED if k % 2 == 0 else "#ffffff", INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x + 3, base - 54, x + 3, base - 34, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x + 41, base - 54, x + 41, base - 34, INK))
    s.append(text(x + 22, base - 12, "Stall", 14, col=GREEN))
    return "".join(s)


def finish(x, base):
    """A finish post with a chequered flag. 44 wide."""
    px = x + 10
    s = ["<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (px, base - 26, px, base - 66, INK)]
    for r in range(3):
        for c in range(4):
            s.append("<rect x='%.1f' y='%.1f' width='7' height='7' fill='%s'/>"
                     % (px + 1.5 + c * 7, base - 66 + r * 7, INK if (r + c) % 2 == 0 else "#ffffff"))
    s.append("<rect x='%.1f' y='%.1f' width='28' height='21' fill='none' stroke='%s' stroke-width='1'/>" % (px + 1.5, base - 66, INK))
    s.append("<rect x='%.1f' y='%.1f' width='48' height='22' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>"
             % (x - 2, base - 26, GREEN))
    s.append(text(x + 22, base - 10, "Finish", 14, col=GREEN))
    return "".join(s)


def sign(x, base, word):
    """A sign on a post (bus stop, MRT gate, slide). 44 wide."""
    assert tw(word, 14) < 42, word
    return ("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
            "<rect x='%.1f' y='%.1f' width='44' height='24' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
            % (x + 22, base, x + 22, base - 50, INK, x, base - 70, FILL, GREEN) +
            text(x + 22, base - 53, word, 14, col=GREEN))


def line_svg(n, names=None, front="left", place="stall", arrows=(), labels=None, step=None, ends=None):
    """n children in a line. Position 1 is nearest the front (the stall or the finish).
    names = {position: name}; arrows = positions with a red arrow; labels = {position: text} in red under the feet.
    place None: a row with no front (for a photo); ends = (left word, right word) under the ends."""
    names = names or {}
    labels = labels or {}
    if step is None:
        step = 60 if names else 38
    for p, nm in names.items():
        assert tw(nm, 14) < step - 4, (nm, step)
    for p, t in labels.items():
        assert tw(t, 14) < step - 2, (t, step)
    m = 6
    lead = 50 if place else 0
    W = 2 * m + lead + n * step
    top = 30
    base = top + 52
    yname = base + 18
    yend = yname + (20 if names or labels else 2)
    H = yend + 6
    s = ["<line x1='2' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (base, W - 2, base, SOFT)]
    if place:
        px = m if front == "left" else W - m - 44
        if place == "stall":
            s.append(stall(px, base))
        elif place == "finish":
            s.append(finish(px, base))
        else:
            s.append(sign(px, base, place))

    def cx(p):
        if front == "left":
            return m + lead + step / 2 + (p - 1) * step
        return W - m - lead - step / 2 - (p - 1) * step

    for p in range(1, n + 1):
        x = cx(p)
        s.append(child(x, base, SHIRT[(p - 1) % len(SHIRT)]))
        if p in names:
            s.append(text(x, yname, names[p], 14))
        if p in labels:
            s.append(text(x, yname, labels[p], 14, col=RED))
        if p in arrows:
            s.append(arrow_down(x, 4, top - 2))
    if place:
        fw, bw = ("front", "back") if front == "left" else ("back", "front")
        s.append(text(m, yend, fw, 14, "start", SOFT))
        s.append(text(W - m, yend, bw, 14, "end", SOFT))
    elif ends:
        s.append(text(m, yend, ends[0], 14, "start", SOFT))
        s.append(text(W - m, yend, ends[1], 14, "end", SOFT))
    lab = "%d children in a line" % n if place else "%d children in a row" % n
    return svg_wrap(W, H, "".join(s), lab)


def podium_svg(first, second, third):
    """A podium: 2nd on the left, 1st in the middle (tallest), 3rd on the right."""
    W, H = 240, 150
    base = 140
    blocks = [(10, 2, 46, second), (86, 1, 70, first), (162, 3, 30, third)]
    s = []
    for x, p, h, nm in blocks:
        s.append("<rect x='%d' y='%d' width='68' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, base - h, h, FILL, GREEN))
        s.append(text(x + 34, base - h + 20, S(p), 16, col=GREEN))
        s.append(child(x + 34, base - h, SHIRT[p]))
        assert tw(nm, 14) < 68
        s.append(text(x + 34, base - h - 54, nm, 14))
    assert base - 70 - 54 - 14 >= 0
    return svg_wrap(W, H, "".join(s), "a podium for 1st, 2nd and 3rd")


def chair(x, base):
    return ("<rect x='%.1f' y='%.1f' width='22' height='5' fill='#b98a5a' stroke='%s' stroke-width='1.5'/>"
            "<rect x='%.1f' y='%.1f' width='5' height='26' fill='#b98a5a' stroke='%s' stroke-width='1.5'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
            % (x - 11, base - 20, INK, x + 6, base - 46, INK, x - 9, base - 15, x - 9, base, INK,
               x + 9, base - 15, x + 9, base, INK))


def chairs_svg(n, names):
    """n chairs in a row with left and right marked. names = {position from the left: name}."""
    step, m = 52, 6
    W = 2 * m + n * step
    base = 56
    H = base + 44
    s = ["<line x1='2' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (base, W - 2, base, SOFT)]
    for p in range(1, n + 1):
        x = m + step / 2 + (p - 1) * step
        s.append(chair(x, base))
        if p in names:
            assert tw(names[p], 14) < step - 2
            s.append(text(x, base + 18, names[p], 14))
    s.append(text(m, base + 38, "left", 14, "start", SOFT))
    s.append(text(W - m, base + 38, "right", 14, "end", SOFT))
    return svg_wrap(W, H, "".join(s), "%d chairs in a row" % n)


# ------------------------------------------------------------ pictures: fruit, ribbons, cards
FRUIT = ["apple", "pear", "mango", "banana", "orange", "durian", "rambutan"]


def fruit(kind, cx, cy):
    if kind == "apple":
        return ("<circle cx='%.1f' cy='%.1f' r='13' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2.5' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='5' ry='2.6' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 3, cx, cy - 9, cx + 1, cy - 15, cx + 6, cy - 13, GREEN, cx + 6, cy - 13))
    if kind == "pear":
        return ("<path d='M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f Z' "
                "fill='#b5cf4a' stroke='#6d7f1e' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2.5' stroke-linecap='round'/>"
                % (cx, cy - 13, cx - 7, cy - 13, cx - 14, cy + 15, cx, cy + 16,
                   cx + 14, cy + 15, cx + 7, cy - 13, cx, cy - 13, cx, cy - 13, cx + 2, cy - 19))
    if kind == "mango":
        return ("<ellipse cx='%.1f' cy='%.1f' rx='16' ry='11' fill='#f4a92a' stroke='#a8650c' stroke-width='1.5' "
                "transform='rotate(-25 %.1f %.1f)'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='5' ry='2.6' fill='%s'/>"
                % (cx, cy + 2, cx, cy + 2, cx + 10, cy - 10, GREEN))
    if kind == "banana":
        return ("<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#f4d03f' stroke='#a68a00' stroke-width='1.5'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='3' stroke-linecap='round'/>"
                % (cx - 16, cy - 8, cx - 6, cy + 20, cx + 16, cy - 6, cx - 2, cy + 8, cx - 16, cy - 8,
                   cx + 16, cy - 6, cx + 18, cy - 10))
    if kind == "orange":
        s = ["<circle cx='%.1f' cy='%.1f' r='13' fill='#f39c12' stroke='#a85d00' stroke-width='1.5'/>" % (cx, cy + 2)]
        for dx, dy in [(-5, -2), (4, 4), (-2, 8), (6, -4)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='1' fill='#a85d00'/>" % (cx + dx, cy + 2 + dy))
        s.append("<ellipse cx='%.1f' cy='%.1f' rx='4.5' ry='2.4' fill='%s'/>" % (cx + 3, cy - 12, GREEN))
        return "".join(s)
    if kind == "durian":
        s = []
        for k in range(14):
            a = k * 3.14159 * 2 / 14
            import math
            x1, y1 = cx + 13 * math.cos(a), cy + 2 + 13 * math.sin(a)
            x2, y2 = cx + 17 * math.cos(a), cy + 2 + 17 * math.sin(a)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#5d6b1e' stroke-width='3' stroke-linecap='round'/>" % (x1, y1, x2, y2))
        s.append("<circle cx='%.1f' cy='%.1f' r='13' fill='#9fb43a' stroke='#5d6b1e' stroke-width='1.5'/>" % (cx, cy + 2))
        return "".join(s)
    if kind == "rambutan":
        import math
        s = []
        for k in range(16):
            a = k * 3.14159 * 2 / 16
            x1, y1 = cx + 11 * math.cos(a), cy + 2 + 11 * math.sin(a)
            x2, y2 = cx + 16 * math.cos(a + 0.25), cy + 2 + 16 * math.sin(a + 0.25)
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#2e8b57' stroke-width='1.6' stroke-linecap='round'/>" % (x1, y1, x2, y2))
        s.append("<circle cx='%.1f' cy='%.1f' r='12' fill='#d6453b' stroke='#8e1f17' stroke-width='1.5'/>" % (cx, cy + 2))
        return "".join(s)
    raise ValueError(kind)


def fruit_svg(kinds):
    """A row of fruit, each named underneath, with left and right marked."""
    step, m = 74, 6
    W = 2 * m + len(kinds) * step
    H = 104
    s = ["<line x1='2' y1='58' x2='%d' y2='58' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (W - 2, SOFT)]
    for i, k in enumerate(kinds):
        x = m + step / 2 + i * step
        s.append(fruit(k, x, 34))
        assert tw(k, 14) < step - 2
        s.append(text(x, 77, k, 14))
    s.append(text(m, 98, "left", 14, "start", SOFT))
    s.append(text(W - m, 98, "right", 14, "end", SOFT))
    return svg_wrap(W, H, "".join(s), "a row of fruit")


def rosette(cx, cy, t, fs=20):
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#3b7dd8' stroke='#1f4f8f' stroke-width='1.5'/>"
         % (cx - 14, cy + 10, cx - 24, cy + 44, cx - 14, cy + 38, cx - 6, cy + 44),
         "<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='#3b7dd8' stroke='#1f4f8f' stroke-width='1.5'/>"
         % (cx + 14, cy + 10, cx + 24, cy + 44, cx + 14, cy + 38, cx + 6, cy + 44),
         "<circle cx='%.1f' cy='%.1f' r='28' fill='#f2c230' stroke='#a57c00' stroke-width='2'/>" % (cx, cy),
         "<circle cx='%.1f' cy='%.1f' r='21' fill='#ffffff' stroke='#a57c00' stroke-width='1.5'/>" % (cx, cy)]
    assert tw(t, fs) < 40, t
    s.append(text(cx, cy + fs * 0.36, t, fs))
    return "".join(s)


def ribbon_svg(t):
    W, H = 70, 82
    return svg_wrap(W, H, rosette(35, 32, t, 20), "a ribbon")


def ribbons_svg(ts):
    """Four ribbons A to D in one picture."""
    step = 76
    W, H = 4 * step + 8, 104
    s = []
    for i, t in enumerate(ts):
        x = 4 + step / 2 + i * step
        s.append(text(x, 18, "ABCD"[i], 16, col=GREEN))
        s.append(rosette(x, 52, t, 18))
    return svg_wrap(W, H, "".join(s), "four ribbons A to D")


def card_svg(word, fs=24):
    w = int(tw(word, fs) + 36)
    W, H = w + 8, 58
    return svg_wrap(W, H, "<rect x='4' y='4' width='%d' height='50' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                    % (w, GREEN) + text(4 + w / 2, 4 + 25 + fs * 0.36, word, fs), "a word card")


def cards_svg(vals):
    """Position cards in a row, like a number track. A '?' card is shaded with a red ?."""
    cw, m, gap = 62, 4, 10
    W = 2 * m + len(vals) * cw + (len(vals) - 1) * gap
    H = 2 * m + 46
    s = []
    for k, v in enumerate(vals):
        x = m + k * (cw + gap)
        q = v == "?"
        s.append("<rect x='%d' y='%d' width='%d' height='46' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, cw, FILL if q else "#ffffff", GREEN))
        s.append(text(x + cw / 2, m + 30, v, 20, col=RED if q else INK))
        if k:
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>"
                     % (x - gap + 2, m + 23, x - 2, m + 23, SOFT))
    return svg_wrap(W, H, "".join(s), "position cards")


# ------------------------------------------------------------ names
FIG_NAMES = [n for n in BOYS + GIRLS if tw(n, 14) < 56]


class Names:
    def __init__(self, rnd):
        self.rnd = rnd

    def take(self, k, pool=None):
        return self.rnd.sample(pool or FIG_NAMES, k)


def count_e(names, p, front="front"):
    """Explanation that counts the positions from the front up to p."""
    seq = ["%s is %s" % (names[i], ORD[i]) for i in range(1, p + 1)]
    return "Start at the %s. %s." % (front, ", ".join(seq))


# ------------------------------------------------------------ set 1: position in a queue
def set_queue(nm):
    items = []
    # who is first / second ...? 5 children, front on the left
    for p in (1, 2, 3, 4):
        n = 5
        ns = nm.take(n)
        names = {i + 1: ns[i] for i in range(n)}
        right = names[p]
        wrong = pick3(right, [names[n + 1 - p], names.get(p + 1), names.get(p - 1)], [names[i] for i in range(1, n + 1)])
        e = "Start at the front, next to the stall. Count: %s. <b>%s</b> is %s." % (
            ", ".join(ORD[1:p + 1]), right, ORD[p])
        items.append(mcq(fig(line_svg(n, names)) + "Who is <b>%s</b> in the queue?" % ORD[p], right, wrong, e))
    # X is ___ in the queue. 6 children
    for p in (2, 5, 3, 6):
        n = 6
        ns = nm.take(n)
        names = {i + 1: ns[i] for i in range(n)}
        x = names[p]
        right = ORD[p]
        wrong = pick3(right, [ORD[n + 1 - p], CARD[p], ORD[p + 1] if p < n else None, ORD[p - 1]], [])
        e = "Count from the front: %s. %s is <b>%s</b>. Say “%s”, not “%s”." % (
            ", ".join(ORD[1:p + 1]), x, right, right, CARD[p])
        items.append(mcq(fig(line_svg(n, names)) + "%s is ___ in the queue." % x, right, wrong, e))
    # front on the right
    for p in (2, 1, 4, 3):
        n = 6
        ns = nm.take(n)
        names = {i + 1: ns[i] for i in range(n)}
        right = names[p]
        wrong = pick3(right, [names[n + 1 - p], names.get(p + 1), names.get(p - 1)], [names[i] for i in range(1, n + 1)])
        e = ("The stall is on the right, so the front is on the right. Count from there: %s. <b>%s</b> is %s."
             % (", ".join(ORD[1:p + 1]), right, ORD[p]))
        items.append(mcq(fig(line_svg(n, names, front="right")) + "Look for the front. Who is <b>%s</b>?" % ORD[p],
                         right, wrong, e))
    # unnamed queues, 7 to 10 children, a red arrow
    for n, p, front in [(7, 7, "left"), (8, 6, "left"), (9, 8, "left"), (10, 10, "left"),
                        (8, 3, "right"), (10, 9, "left"), (9, 5, "right"), (10, 7, "right")]:
        right = ORD[p]
        wrong = pick3(right, [ORD[n + 1 - p], ORD[p - 1], ORD[p + 1] if p < 10 else None, CARD[p]], [])
        e = "Count from the front: %s. The child with the arrow is <b>%s</b>." % (", ".join(ORD[1:p + 1]), right)
        if front == "right":
            e = "The front is on the right. " + e
        items.append(mcq(fig(line_svg(n, front=front, arrows=(p,))) +
                         "Which position is the child with the arrow?", right, wrong, e))
    return {"title": "Position in a queue: first to tenth", "items": items}


# ------------------------------------------------------------ set 2: symbols 1st, 2nd, 3rd, 4th
def wrong_suffix(n):
    """Real mistakes when writing the symbol: 1th, 2th, 3th, 4st ..."""
    return ["%d%s" % (n, s) for s in ("st", "nd", "rd", "th") if "%d%s" % (n, s) != S(n)]


def set_symbols(nm):
    items = []
    for n in (1, 2, 3, 4, 8):
        right = S(n)
        e = "1st, 2nd and 3rd are special. The others end in “th”. “%s” is written <b>%s</b>." % (ORD[n], right)
        items.append(mcq(fig(card_svg(ORD[n])) + "Which symbol means this word?", right, wrong_suffix(n), e))
    WW = {1: ["one", "oneth", "second"], 2: ["two", "twoth", "third"], 3: ["three", "threeth", "fourth"],
          5: ["five", "fiveth", "fourth"], 9: ["nine", "nineth", "tenth"], 4: ["four", "forth", "fifth"]}
    for n in (2, 3, 5, 4, 9):
        right = ORD[n]
        e = "%s is said “%s”. It tells a position. %s" % (S(n), right, {
            2: "It is <b>second</b>, not “two”.",
            3: "It is <b>third</b>, not “three”.",
            5: "Spell it <b>fifth</b>: no “v” and no “e”.",
            4: "Spell it <b>fourth</b>, with a “u”.",
            9: "Spell it <b>ninth</b>: no “e” after the n."}[n])
        items.append(mcq(fig(ribbon_svg(S(n))) + "Which word does the ribbon show?", right, WW[n], e))
    # which ribbon is written correctly?
    for ts, ans in [(["1th", "3st", "2nd", "4rd"], "C"), (["3rd", "2th", "1nd", "5st"], "A"),
                    (["2st", "4nd", "3th", "1st"], "D")]:
        right = ts["ABCD".index(ans)]
        assert right in [S(k) for k in range(1, 11)]
        assert all(t not in [S(k) for k in range(1, 11)] for t in ts if t != right)
        e = "Ribbon <b>%s</b> shows %s, which is right. Remember: 1st, 2nd, 3rd, then 4th, 5th, 6th." % (ans, right)
        items.append(fixed(fig(ribbons_svg(ts)) + "Which ribbon is written correctly?", list("ABCD"), ans, e))
    for ts, ans in [(["1st", "2nd", "3th", "4th"], "C"), (["6th", "2st", "3rd", "10th"], "B")]:
        bad = ts["ABCD".index(ans)]
        assert bad not in [S(k) for k in range(1, 11)]
        assert all(t in [S(k) for k in range(1, 11)] for t in ts if t != bad)
        good = S(int(bad[:-2]))
        e = "Ribbon <b>%s</b> is wrong. %s should be %s." % (ans, bad, good)
        items.append(fixed(fig(ribbons_svg(ts)) + "Which ribbon is <b>not</b> written correctly?", list("ABCD"), ans, e))
    # count and choose the symbol
    for n, p, front in [(6, 2, "left"), (7, 3, "left"), (8, 1, "right"), (9, 7, "left"), (10, 9, "right")]:
        right = S(p)
        bad = {1: "1th", 2: "2th", 3: "3th", 7: "7rd", 9: "9st"}[p]
        wrong = pick3(right, [bad, S(n + 1 - p), S(p + 1) if p < 10 else None, S(p - 1) if p > 1 else None], [])
        e = "Count from the front: %s. The child is %s, written <b>%s</b>." % (", ".join(ORD[1:p + 1]), ORD[p], right)
        if front == "right":
            e = "The front is on the right. " + e
        items.append(mcq(fig(line_svg(n, front=front, arrows=(p,))) +
                         "Which symbol tells the position of the child with the arrow?", right, wrong, e))
    return {"title": "Symbols: 1st, 2nd, 3rd, 4th", "items": items}


# ------------------------------------------------------------ set 3: from the left or the right
def set_left_right(nm, rnd):
    items = []
    ENDS = ("left", "right")
    for n, p, side in [(5, 1, "left"), (5, 3, "left"), (5, 2, "right"), (5, 4, "left"),
                       (6, 1, "right"), (6, 3, "right"), (6, 5, "left"), (6, 4, "right")]:
        ns = nm.take(n)                       # ns[0] is on the left
        L = {i + 1: ns[i] for i in range(n)}  # position from the left
        idx = p if side == "left" else n + 1 - p
        right = L[idx]
        other = L[n + 1 - idx]
        wrong = pick3(right, [other, L.get(idx + 1), L.get(idx - 1)], ns)
        e = "Start at the %s end. Count: %s. <b>%s</b> is %s from the %s." % (
            side, ", ".join(ORD[1:p + 1]), right, S(p), side)
        items.append(mcq(fig(line_svg(n, L, place=None, ends=ENDS)) +
                         "Who is <b>%s from the %s</b>?" % (S(p), side), right, wrong, e))
    for kinds, p, side in [(["apple", "durian", "banana", "pear", "rambutan", "mango"], 2, "left"),
                           (["orange", "mango", "rambutan", "apple", "pear", "banana"], 3, "right"),
                           (["pear", "banana", "apple", "mango", "orange", "durian"], 4, "left"),
                           (["rambutan", "orange", "pear", "durian", "banana", "apple"], 1, "right"),
                           (["mango", "apple", "orange", "banana", "durian", "pear"], 5, "left"),
                           (["banana", "rambutan", "durian", "orange", "apple", "mango"], 4, "right")]:
        n = len(kinds)
        idx = p if side == "left" else n + 1 - p        # 1-based from the left
        right = kinds[idx - 1]
        wrong = pick3(right, [kinds[n - idx], kinds[idx] if idx < n else None, kinds[idx - 2] if idx > 1 else None], kinds)
        e = "Start at the %s end. Count: %s. The fruit %s from the %s is the <b>%s</b>." % (
            side, ", ".join(S(k) for k in range(1, p + 1)), S(p), side, right)
        items.append(mcq(fig(fruit_svg(kinds)) + "Which fruit is <b>%s from the %s</b>?" % (S(p), side),
                         right, wrong, e))
    for n, idx in [(6, 2), (7, 3)]:
        ns = nm.take(n)
        L = {i + 1: ns[i] for i in range(n)}
        x = L[idx]
        p = n + 1 - idx
        right = S(p)
        wrong = pick3(right, [S(idx), S(p - 1), S(p + 1) if p < 10 else None], [])
        e = "Start at the right end and count to %s: %s. %s is <b>%s</b> from the right." % (
            x, ", ".join(S(k) for k in range(1, p + 1)), x, right)
        items.append(mcq(fig(line_svg(n, L, place=None, ends=ENDS)) +
                         "%s is ___ from the right." % x, right, wrong, e))
    for n, idx in [(7, 2), (6, 2), (7, 3), (8, 3)]:
        ns = nm.take(n)
        L = {i + 1: ns[i] for i in range(n)}
        x = L[idx]
        p = n + 1 - idx
        right = S(p)
        wrong = pick3(right, [S(idx), S(n - idx), S(n + 2 - idx) if n + 2 - idx <= 10 else None], [S(p + 1)])
        e = ("There are %d children. From the right, count %s up to %s. %s is <b>%s</b> from the right."
             % (n, ", ".join(S(k) for k in range(1, p + 1)), x, x, right))
        items.append(mcq(fig(line_svg(n, L, place=None, ends=ENDS)) +
                         "%s is %s from the left. What position is %s from the right?" % (x, S(idx), he(x)),
                         right, wrong, e))
    assert len(items) == 20
    # easy to hard: rows of children, fruit, then from-the-right questions
    return {"title": "From the left or from the right", "items": items}


# ------------------------------------------------------------ set 4: before, after and between
def set_before_after(nm):
    items = []
    for n in (3, 6, 9):
        right = S(n + 1)
        wrong = [S(n - 1), S(n + 2) if n + 2 <= 10 else S(n - 2), wrong_suffix(n + 1)[0]]
        e = "Just after means the next one. After %s comes <b>%s</b>." % (S(n), right)
        items.append(mcq(fig(cards_svg([S(n - 1), S(n), "?"])) + "What comes just after %s?" % S(n), right, wrong, e))
    for n in (2, 5, 10):
        right = S(n - 1)
        wrong = pick3(right, [S(n + 1) if n < 10 else None, S(n - 2) if n > 2 else None, S(n)],
                      [w for w in wrong_suffix(n - 1) if w.endswith("th")] + wrong_suffix(n - 1))
        e = "Just before means the one in front of it. Before %s comes <b>%s</b>." % (S(n), right)
        nxt = S(n + 1) if n < 10 else None
        cards = ["?", S(n)] + ([nxt] if nxt else [])
        items.append(mcq(fig(cards_svg(cards)) + "What comes just before %s?" % S(n), right, wrong, e))
    for a in (3, 7):
        right = S(a + 1)
        wrong = [S(a), S(a + 2), S(a + 3) if a + 3 <= 10 else S(a - 1)]
        e = "%s, %s, %s. <b>%s</b> is between %s and %s." % (S(a), right, S(a + 2), right, S(a), S(a + 2))
        items.append(mcq(fig(cards_svg([S(a), "?", S(a + 2)])) + "Which position is between %s and %s?" % (S(a), S(a + 2)),
                         right, wrong, e))
    # just behind / just in front of
    for n, p, rel, front in [(6, 3, "behind", "left"), (6, 4, "in front of", "left"),
                             (6, 2, "behind", "right"), (6, 5, "in front of", "right")]:
        ns = nm.take(n)
        Q = {i + 1: ns[i] for i in range(n)}
        x = Q[p]
        t = p + 1 if rel == "behind" else p - 1
        o = p - 1 if rel == "behind" else p + 1
        t2 = p + 2 if rel == "behind" else p - 2
        right = Q[t]
        wrong = pick3(right, [Q.get(o), Q.get(t2), x], ns)
        e = ("%s is %s. Just %s %s is the one %s, so <b>%s</b> is %s." % (
            x, ORD[p], rel, him(x), "nearer the back" if rel == "behind" else "nearer the front", right, ORD[t]))
        items.append(mcq(fig(line_svg(n, Q, front=front)) + "Who is just %s %s?" % (rel, x), right, wrong, e))
    # who is between?
    for n, a, front in [(5, 2, "left"), (6, 3, "right"), (6, 4, "left")]:
        ns = nm.take(n)
        Q = {i + 1: ns[i] for i in range(n)}
        x, y = Q[a], Q[a + 2]
        right = Q[a + 1]
        wrong = pick3(right, [x, y, Q.get(a + 3), Q.get(a - 1)], ns)
        e = "%s is %s and %s is %s. The child in the middle is <b>%s</b>, who is %s." % (
            x, ORD[a], y, ORD[a + 2], right, ORD[a + 1])
        items.append(mcq(fig(line_svg(n, Q, front=front)) + "Who is between %s and %s?" % (x, y), right, wrong, e))
    # just behind a position
    for n, p in [(6, 3), (7, 5)]:
        ns = nm.take(2)
        x, y = ns
        Q = {p: x, p + 1: y}
        right = ORD[p + 1]
        wrong = [ORD[p - 1], ORD[p], ORD[p + 2]]
        e = "%s is %s. Just behind %s is the next place: <b>%s</b>." % (x, ORD[p], him(x), right)
        items.append(mcq(fig(line_svg(n, Q)) + "%s is %s. %s is just behind %s. What position is %s?"
                         % (x, ORD[p], y, him(x), y), right, wrong, e))
    # how many are between the two arrows?
    for n, a, b in [(8, 2, 6), (9, 3, 8), (10, 1, 7)]:
        right = b - a - 1
        wrong = [b - a, b - a + 1, b - a - 2]
        e = ("The arrows are at %s and %s. The children between them are %s: that is <b>%d</b>. "
             "Do not count the children with the arrows." % (S(a), S(b), ", ".join(S(k) for k in range(a + 1, b)), right))
        items.append(mcq(fig(line_svg(n, arrows=(a, b))) + "How many children are between the two arrows?",
                         right, wrong, e))
    assert len(items) == 20
    return {"title": "Before, after and between", "items": items}


# ------------------------------------------------------------ set 5: word problems
def set_word(nm):
    items = []

    def add(svg, q, right, wrong, e):
        items.append(mcq((fig(svg) if svg else "") + q, right, wrong, e))

    # 1, 2: how many in front?
    x = "Jun Jie"
    add(line_svg(6, {4: x}), "%s is 4th in the queue at the canteen. How many children are in front of him?" % x,
        3, [4, 5, 2], "The children in front of %s are 1st, 2nd and 3rd. That is <b>3</b>. Do not count %s." % (x, x))
    x = "Devi"
    add(line_svg(8, {6: x}, step=40), "%s is 6th in the queue to buy kaya toast. How many children are in front of her?" % x,
        5, [6, 7, 4], "1st, 2nd, 3rd, 4th and 5th are in front of %s. That is <b>5</b> children." % x)
    # 3: last in a race
    a, b = "Ali", "Siti"
    add(line_svg(6, {1: a, 6: b}, place="finish"), "6 children run a race. %s comes in 1st. %s comes in last. "
        "What position is %s?" % (a, b, b), "6th", ["1st", "5th", "7th"],
        "There are 6 runners, so last is <b>6th</b>.")
    # 4: just after in a race
    a, b = "Arjun", "Ryan"
    add(line_svg(5, {2: a}, place="finish", step=48), "%s comes in 2nd in the race. %s comes in just after him. "
        "What position is %s?" % (a, b, b), "3rd", ["1st", "2nd", "4th"],
        "Just after 2nd comes <b>3rd</b>.")
    # 5, 6: podium
    f, s2, t3 = "Priya", "Ahmad", "Kavya"
    add(podium_svg(f, s2, t3), "This is the podium for the race. Who came in 2nd?", s2, [f, t3, "Ryan"],
        "Read the number on each block. The 2nd block is on the left. <b>%s</b> is 2nd. The tallest block is 1st." % s2)
    f, s2, t3 = "Hafiz", "Chloe", "Raju"
    add(podium_svg(f, s2, t3), "Who came in 1st? Look at the numbers on the blocks.", f, [s2, t3, "Sarah"],
        "The 1st block is in the middle. It is the tallest. <b>%s</b> came in 1st." % f)
    # 7: just in front of
    a, b = "Chloe", "Kavya"
    add(line_svg(6, {5: a, 4: b}, place="finish", step=52), "%s comes in 5th. %s is just in front of her. "
        "What position is %s?" % (a, b, b), "4th", ["6th", "5th", "3rd"],
        "Just in front of 5th is <b>4th</b>.")
    # 8: how many finish before
    a = "Priya"
    add(line_svg(5, {3: a}, place="finish"), "On Sports Day, %s finishes 3rd. How many children finish before her?" % a,
        2, [3, 4, 1], "1st and 2nd finish before %s. That is <b>2</b> children." % a)
    # 9, 10: from the back
    a = "Farah"
    add(line_svg(8, {3: a}, step=48), "8 children are in a queue. %s is 3rd from the front. "
        "What position is she from the back?" % a, "6th", ["3rd", "5th", "7th"],
        "Count from the back: 1st, 2nd, 3rd, 4th, 5th, 6th. %s is <b>6th</b> from the back." % a)
    a = "Hafiz"
    add(line_svg(9, {8: a}, place="Bus", step=44), "9 children wait for the bus. %s is 2nd from the back. "
        "What position is he from the front?" % a, "8th", ["2nd", "7th", "9th"],
        "Count from the front: 1st, 2nd, ... 8th. %s is <b>8th</b> from the front." % a)
    # 11: total in the queue
    a = "Raju"
    add(line_svg(7, {3: a}, step=44), "%s is 3rd in the queue. 4 children are behind him. "
        "How many children are in the queue?" % a, 7, [6, 8, 4],
        "2 children are in front, then %s, then 4 behind. 2 + 1 + 4 = <b>7</b>." % a)
    # 12
    a, b = "Sarah", "Xin Yi"
    add(line_svg(7, {6: a, 7: b}, step=52), "%s is 6th in the queue. %s is just behind her. "
        "What position is %s?" % (a, b, b), "7th", ["5th", "6th", "8th"],
        "Just behind 6th is <b>7th</b>.")
    # 13: children leave from the front
    a = "Ethan"
    add(line_svg(6, {4: a}), "%s is 4th in the queue. The 2 children in front buy their food and go. "
        "What position is %s now?" % (a, he(a)), "2nd", ["4th", "6th", "3rd"],
        "%s had 3 children in front. 2 go, so 1 is left in front. %s is now <b>2nd</b>." % (a, a))
    # 14: between in a queue
    a, b = "Siti", "Farah"
    add(line_svg(8, {3: a, 7: b}, step=48), "%s is 3rd in the queue. %s is 7th. How many children are between them?" % (a, b),
        3, [4, 5, 2], "Between 3rd and 7th are 4th, 5th and 6th. That is <b>3</b> children.")
    # 15: between in a race
    a, b = "Raju", "Ryan"
    add(line_svg(8, {2: a, 7: b}, place="finish", step=44), "In a race, %s is 2nd and %s is 7th. "
        "How many runners are between them?" % (a, b), 4, [5, 6, 3],
        "Between 2nd and 7th are 3rd, 4th, 5th and 6th. That is <b>4</b> runners.")
    # 16: 5th from the front and from the back
    a = "Nurul"
    add(line_svg(9, {5: a}, step=44), "%s is 5th from the front. She is also 5th from the back. "
        "How many children are in the queue?" % a, 9, [10, 8, 5],
        "4 are in front of her and 4 are behind her. 4 + 1 + 4 = <b>9</b>.")
    # 17: 4th from the back of 10
    a = "Ryan"
    add(line_svg(10, {7: a}, place="MRT", step=40), "On a class trip, 10 pupils queue at the MRT station. %s is 4th from the back. "
        "What position is he from the front?" % a, "7th", ["4th", "6th", "8th"],
        "Count from the front: 1st, 2nd, ... 7th. %s is <b>7th</b> from the front." % a)
    # 18: chairs
    a, b = "Siti", "Ali"
    add(chairs_svg(7, {3: a, 5: b}), "%s sits on the 3rd chair from the left. %s sits on the 3rd chair from the right. "
        "How many chairs are between them?" % (a, b), 1, [0, 2, 3],
        "%s is on chair 3 from the left. %s is on chair 5 from the left. Only chair 4 is between them: <b>1</b> chair." % (a, b))
    # 19: how many behind
    a = "Ali"
    add(line_svg(10, {9: a}, place="Slide", step=40), "10 children queue for the slide at the playground. %s is 9th. "
        "How many children are behind him?" % a, 1, [9, 2, 10],
        "Only the 10th child is behind %s. That is <b>1</b> child." % a)
    # 20: passing runners
    a = "Arjun"
    add(line_svg(8, {7: a}, place="finish", step=44), "On Sports Day, %s is 7th in the race. He runs past 2 children. "
        "What position is he now?" % a, "5th", ["9th", "6th", "4th"],
        "Passing a runner moves you 1 place nearer the front. 7th, then 6th, then <b>5th</b>.")
    assert len(items) == 20
    return {"title": "Word problems: races and queues", "items": items}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def body_html():
    return (
        "<h2>Ordinal numbers tell the position</h2>"
        "<p>Counting numbers tell how many: one, two, three. "
        "Ordinal numbers tell the <b>position</b>: first, second, third. "
        "In a queue, start counting at the <b>front</b>.</p>"
        "<figure class='sn-fig'>" + line_svg(5, labels={k: S(k) for k in range(1, 6)}, step=44) +
        "<figcaption>The child next to the stall is 1st. The last child here is 5th.</figcaption></figure>"
        "<h2>Words and symbols</h2>" +
        table(["Symbol", "Word", "Symbol", "Word"], [
            ["1st", "first", "6th", "sixth"],
            ["2nd", "second", "7th", "seventh"],
            ["3rd", "third", "8th", "eighth"],
            ["4th", "fourth", "9th", "ninth"],
            ["5th", "fifth", "10th", "tenth"],
        ]) +
        "<p>1st, 2nd and 3rd are special. All the others end in “th”.</p>"
        "<h2>From the left or from the right</h2>"
        "<p>Read the question. Start counting at the end it tells you.</p>"
        "<figure class='sn-fig'>" + fruit_svg(["apple", "durian", "banana", "pear", "mango"]) +
        "<figcaption>The banana is 3rd from the left and 3rd from the right. The durian is 2nd from the left but 4th from the right.</figcaption></figure>" +
        ex("From the right", "Which fruit is 2nd from the right?",
           "Start at the right end: mango is 1st, pear is 2nd.", "pear") +
        "<h2>Before, after and between</h2>"
        "<p>Just after 4th comes 5th. Just before 4th comes 3rd. 4th is between 3rd and 5th.</p>" +
        ex("How many are in front?", "Ali is 4th in the queue. How many children are in front of him?",
           "In front of him are 1st, 2nd and 3rd. Do not count Ali.", "3 children") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Counting from the wrong end", "Find the front, the left or the right first. Then count"],
            ["Writing 3th or 2st", "Write 1st, 2nd, 3rd. Then 4th, 5th ... 10th"],
            ["Saying “three” for 3rd", "Say the position word: third"],
            ["Counting the child too when asked how many are in front", "4th in the queue has 3 children in front"],
            ["Counting both ends as between", "Between 2nd and 6th are 3rd, 4th, 5th: 3 children"],
        ])
    )


FAQ = [
    {"q": "What are ordinal numbers in P1 maths?",
     "a": "Ordinal numbers tell the position of something, such as first, second and third. Primary 1 students learn first to tenth and the symbols 1st, 2nd, 3rd up to 10th."},
    {"q": "How do I teach ordinal numbers to my child?",
     "a": "Line up toys or family members and ask who is first, second and third. Change where the front is, so your child learns to find the start before counting."},
    {"q": "What is the most common mistake with ordinal numbers?",
     "a": "The most common mistake is counting from the wrong end, such as from the back instead of the front. Children also write 3th or 2st instead of 3rd and 2nd."},
    {"q": "Are ordinal numbers in the MOE syllabus?",
     "a": "Yes. Ordinal numbers (first, second, up to tenth) and the symbols 1st, 2nd, 3rd are part of Whole Numbers in the MOE 2021 Primary 1 Mathematics syllabus."},
]


def mark_large(u, pattern):
    """Tag wide pictures (queues, rows, ribbons, position cards) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + ")')")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen_unit():
    rnd = random.Random(61802)
    nm = Names(rnd)
    sets = [set_queue(nm), set_symbols(nm), set_left_right(nm, rnd), set_before_after(nm), set_word(nm)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            key = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "ordinal-numbers", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Ordinal Numbers: First to Tenth",
        "seo_title": "P1 Ordinal Numbers Worksheets: Free Primary 1 Maths with Answers (MOE Syllabus)",
        "short_title": "Ordinal numbers",
        "domain": "Number and Algebra",
        "standard_code": "Primary 1: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Ordinal numbers (first, second, up to tenth) and symbols (1st, 2nd, 3rd, etc.)",
        "meta_desc": "Free P1 maths practice on ordinal numbers: first to tenth, 1st, 2nd, 3rd, left and right, "
                     "before, after and between. 100 questions with answers.",
        "key_big": "Ordinal numbers tell the position: 1st, 2nd, 3rd, 4th ... 10th.",
        "key_sub": "Find the front first. Ali is 4th, so 3 children are in front of him.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "[0-9]+ children in a (?:line|row)|four ribbons A to D|position cards|"
                         "a row of fruit|[0-9]+ chairs in a row|a podium for 1st, 2nd and 3rd")


if __name__ == "__main__":
    u = gen_unit()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    print("wrote", path)
