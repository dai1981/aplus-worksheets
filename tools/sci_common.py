# -*- coding: utf-8 -*-
"""
Shared helpers for science units (US NGSS first: subject `science`).
Same rules as the math generators: HTML attributes in single quotes, no backslashes, no emoji.

A unit is 5 sets of 20 questions (easy -> hard, the last set is investigations and real-world problems).
Questions come from two kinds of makers:
  bank items    written by hand: (question, answer, [3 wrong answers], explanation)
  generators    functions that return an item (or None) from random numbers or tables,
                for example a food web drawn as a picture with a new question each time
Every question in a unit is different (checked on the question text).
"""
import random
from ws_common import (svg_wrap, text, line, fig, figure, table, example, balance, write_unit, B, cap, comma,
                       GREEN, BLUE, RED, INK, FILL, GRAY, FONT, People)

UPDATED = "2026-11-26"
ORANGE = "#d9822b"
BROWN = "#8a5a2b"
SKY = "#dceefb"
SUN = "#f2b705"
LEAF = "#3c8d40"

# NGSS performance expectation pages: /pe/{code}-{DCI title}
DCI = {"PS1": "matter-and-its-interactions", "PS2": "motion-and-stability-forces-and-interactions", "PS3": "energy",
       "PS4": "waves-and-their-applications-technologies-information-transfer",
       "LS1": "molecules-organisms-structures-and-processes", "LS2": "ecosystems-interactions-energy-and-dynamics",
       "LS3": "heredity-inheritance-and-variation-traits", "LS4": "biological-evolution-unity-and-diversity",
       "ESS1": "earths-place-universe", "ESS2": "earths-systems", "ESS3": "earth-and-human-activity",
       "ETS1": "engineering-design"}
DOMAINS = {"PS": "Physical Science", "LS": "Life Science", "ESS": "Earth and Space Science", "ETS": "Engineering Design"}


def std_url(code):
    """'5-PS1-2' -> https://www.nextgenscience.org/pe/5-ps1-2-matter-and-its-interactions"""
    dci = code.split("-")[-2]
    return "https://www.nextgenscience.org/pe/%s-%s" % (code.lower(), DCI[dci])


def domain_of(code):
    dci = code.split("-")[-2]
    return DOMAINS[dci.rstrip("0123456789")]


# ------------------------------------------------------------ questions
def item(q, a, wrong, e):
    c = [a] + list(wrong)
    assert len(c) == 4, (q, c)
    assert len({x.strip().lower() for x in c}) == 4, (q, c)
    assert "\\" not in q + e + "".join(c), q
    return {"q": q, "c": c, "a": 0, "e": e}


def bank(rows):
    """[(q, a, [w, w, w], e)] -> list of makers (each gives its item once). Checked now, so a bad row stops the script."""
    import copy
    its = [item(*r) for r in rows]
    return [lambda it=it: copy.deepcopy(it) for it in its]


class Unit:
    """Collects unique questions for one unit."""

    def __init__(self, seed):
        self.R = random.Random(seed)
        self.seen = set()

    def key(self, it):
        import re
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", it["q"])).strip().lower() + "|" + it["c"][0].lower()

    def take(self, makers, n, tries=6000, cap=6):
        """n unique items from makers (callables, used in turn, random order).
        A maker gives at most `cap` items per set (a (maker, cap) pair sets its own limit),
        so one kind of question does not fill a whole set."""
        out = []
        mk = [m if isinstance(m, tuple) else (m, cap) for m in makers]
        self.R.shuffle(mk)
        used = [0] * len(mk)
        extra = 0          # raised when every maker has reached its cap (soft cap)
        i = 0
        t = 0
        last = 0
        while len(out) < n:
            t += 1
            assert t < tries, "not enough questions: %d of %d" % (len(out), n)
            j = i % len(mk)
            i += 1
            if j == 0:
                if i > 1 and len(out) == last:
                    extra += 1
                last = len(out)
            m, c = mk[j]
            if used[j] >= c + extra:
                continue
            try:
                it = m()
            except (AssertionError, ValueError, IndexError):   # a generator drew numbers that do not work
                it = None
            if not it:
                continue
            k = self.key(it)
            if k in self.seen:
                continue
            self.seen.add(k)
            used[j] += 1
            out.append(it)
        self.R.shuffle(out)
        return out

    def sets(self, spec):
        """spec: [(title, [makers...]), ...] five sets of 20 (bank makers are used first, in order)."""
        res = []
        for title, makers in spec:
            res.append({"title": title, "items": self.take(makers, 20)})
        assert len(res) == 5
        balance(res, self.R)
        return res


def pick(R, xs, k=1):
    return R.sample(xs, k) if k > 1 else R.choice(xs)


# ------------------------------------------------------------ lesson text
def lesson(think, examples, mistakes, extra=""):
    """think: html (the big idea), examples: [(q, [steps], answer)], mistakes: [li html]."""
    h = "<h2>How to think about it</h2>" + think
    h += "".join(example(q, s, a) for q, s, a in examples)
    h += extra
    h += "<h2>Common mistakes</h2><ul>" + "".join("<li>%s</li>" % m for m in mistakes) + "</ul>"
    return h


KIDS = ("kindergarten", "grade-1", "grade-2")


def kid_lesson(pic, lead, points, examples, mistakes):
    """K-2 lesson: one picture and one short sentence first, then short points; examples and mistakes below."""
    think = "<div class='qfig'>%s</div><p><b>%s</b></p><ul>%s</ul>" % (pic, lead, "".join("<li>%s</li>" % p for p in points))
    return lesson(think, examples, mistakes)


def make(grade, slug, sort, code, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets, domain=None):
    for k in (title, seo_title, short, meta, key_big, key_sub):
        assert "<" not in k, k
    assert len(seo_title) <= 95, seo_title
    if grade in KIDS:     # K-2: keep the top of the page light (title and key box are short)
        assert len(title) <= 40 and len(key_big) <= 40 and len(key_sub) <= 90, (title, key_big, key_sub)
    codes = [c.strip() for c in code.split(",")]
    unit = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short,
        "domain": domain or domain_of(codes[0]),
        "standard_code": code, "standard_url": std_url(codes[0]), "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub, "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("us", "science", grade, unit)


# ------------------------------------------------------------ pictures
def rect(x, y, w, h, fill="none", stroke=INK, sw=2, rx=0, extra=""):
    return "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%d' fill='%s' stroke='%s' stroke-width='%s'%s/>" % (x, y, w, h, rx, fill, stroke, sw, extra)


def circle(x, y, r, fill="none", stroke=INK, sw=2, extra=""):
    return "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='%s'%s/>" % (x, y, r, fill, stroke, sw, extra)


def arrow(x1, y1, x2, y2, col=INK, w=2.5, head=9):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45)
    hx2, hy2 = x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45)
    bx, by = x2 - head * 0.8 * math.cos(a), y2 - head * 0.8 * math.sin(a)
    return (line(x1, y1, bx, by, col, w)
            + "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>" % (x2, y2, hx1, hy1, hx2, hy2, col))


def sun(x, y, r=16):
    import math
    s = [circle(x, y, r, SUN, "#c98f00", 2)]
    for k in range(8):
        a = k * math.pi / 4
        s.append(line(x + (r + 4) * math.cos(a), y + (r + 4) * math.sin(a), x + (r + 11) * math.cos(a), y + (r + 11) * math.sin(a), "#c98f00", 2.5))
    return "".join(s)


def bar_chart(labels, values, unit="", label="bar graph", ymax=None, step=None, col=GREEN, w=None, title=""):
    """Simple vertical bar graph with value labels on the axis."""
    n = len(labels)
    bw = 44 if n <= 4 else 36
    gap = 18
    x0, y0, hgt = 52, 26 if title else 14, 150
    W = w or int(x0 + n * (bw + gap) + 12)
    if w:
        gap = max(18, (W - x0 - 12) / float(n) - bw)
    ymax = ymax or max(values)
    step = step or max(1, ymax // 5)
    Y = lambda v: y0 + hgt - hgt * float(v) / ymax
    s = []
    if title:
        s.append(text(W / 2, 16, title, 13))
    v = 0
    while v <= ymax + 1e-9:
        s.append(line(x0, Y(v), W - 8, Y(v), "#d0d0d0", 1))
        s.append(text(x0 - 6, Y(v) + 4, ("%g" % v), 11, "end", weight=400))
        v += step
    for i, (lb, val) in enumerate(zip(labels, values)):
        x = x0 + gap / 2 + i * (bw + gap)
        s.append(rect(x, Y(val), bw, Y(0) - Y(val), col, col, 1))
        s.append(text(x + bw / 2, y0 + hgt + 16, lb, 11, weight=700))
    s.append(line(x0, y0, x0, Y(0), INK, 2) + line(x0, Y(0), W - 8, Y(0), INK, 2))
    if unit:
        s.append(text(14, y0 + hgt / 2, unit, 11, weight=400).replace("<text ", "<text transform='rotate(-90 14 %.1f)' " % (y0 + hgt / 2)))
    return svg_wrap(W, int(y0 + hgt + 26), "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


def pie(parts, label="circle graph", r=70):
    """parts: [(name, value, colour)] -> circle graph with a key on the right."""
    import math
    tot = float(sum(p[1] for p in parts))
    cx, cy = r + 10, r + 10
    s = []
    a = -math.pi / 2
    for name, v, col in parts:
        b = a + 2 * math.pi * v / tot
        large = 1 if b - a > math.pi else 0
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + r * math.cos(b), cy + r * math.sin(b)
        if v == tot:
            s.append(circle(cx, cy, r, col, "#fff", 1))
        else:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='1.5'/>" % (cx, cy, x1, y1, r, r, large, x2, y2, col))
        a = b
    for i, (name, v, col) in enumerate(parts):
        y = 18 + i * 22
        s.append(rect(2 * r + 30, y - 11, 14, 14, col, col, 1))
        s.append(text(2 * r + 50, y + 1, name, 14, "start", weight=400))
    return svg_wrap(2 * r + 230, max(2 * r + 20, 22 * len(parts) + 10), "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


# ------------------------------------------------------------ classifying questions
def classifier(R, pools, which, what, why=None, label=None):
    """pools: {category: [examples]}. Returns two makers:
    which(k): "Which of these is <k>?"  (answer from pools[k], wrong ones from the other pools)
    what(x):  "<x> ... which category?" (answer k, wrong = other categories)
    `which` / `what` are format strings with {k} / {x}; why[k] is one sentence for the explanation."""
    why = why or {}
    label = label or (lambda k: k)
    cats = sorted(pools)

    def m_which():
        k = R.choice(cats)
        a = R.choice(pools[k])
        others = [x for c in cats if c != k for x in pools[c]]
        if len(others) < 3:
            return None
        w = R.sample(others, 3)
        return item(which.format(k=label(k)), a, w, cap(a) + " is " + label(k) + ". " + why.get(k, ""))

    def m_what():
        k = R.choice(cats)
        x = R.choice(pools[k])
        w = [label(c) for c in cats if c != k]
        if len(w) < 3:
            return None
        return item(what.format(x=x, X=cap(x)), label(k), R.sample(w, 3), cap(x) + " is " + label(k) + ". " + why.get(k, ""))
    return m_which, m_what
