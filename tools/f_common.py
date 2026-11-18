# -*- coding: utf-8 -*-
"""
Shared helpers for the AU Foundation units (gen_au_maths_f_*.py).
Foundation is the first year of school in Australia (Kindergarten in NSW and the ACT, Prep in Queensland,
Victoria and Tasmania, Pre-primary in WA, Reception in SA, Transition in the NT), ages 5 to 6.
Built on the US Kindergarten pictures (k_pics) and question helpers (k_common), with Australian English
(colour, ladybird, favourite), Australian names, and extra pictures for times of day, days of the week,
picture graphs and repeating patterns.
"""
import math
import random
import re
import k_pics
from k_pics import obj, shape, name, M, CELL
from k_common import mcq, finish as k_finish
from ws_common import svg_wrap, text, write_unit, table, GREEN, FILL, INK, RED

k_pics.NAMES["bug"] = ("ladybird", "ladybirds")

UPDATED = "2026-11-18"
STD_URL = "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics"
PEOPLE = [("Isla", "she", "her"), ("Jack", "he", "his"), ("Mia", "she", "her"), ("Oliver", "he", "his"),
          ("Ruby", "she", "her"), ("Leo", "he", "his"), ("Zara", "she", "her"), ("Kai", "he", "his"),
          ("Matilda", "she", "her"), ("Noah", "he", "his"), ("Chloe", "she", "her"), ("Lachlan", "he", "his"),
          ("Mei", "she", "her"), ("Cooper", "he", "his"), ("Aria", "she", "her"), ("Aarav", "he", "his")]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class Kids:
    def __init__(self, rnd):
        self.pool = PEOPLE[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=p[0], he=p[1], He=p[1].capitalize(), his=p[2], His=p[2].capitalize())


AU_WORDS = [("ladybug", "ladybird"), ("colors", "colours"), ("color", "colour"), ("favorite", "favourite"),
            ("center", "centre"), ("gray", "grey"), ("Color", "Colour")]


def au(s):
    for a, b in AU_WORDS:
        s = s.replace(a, b)
    return s


def finish(sets, rnd, max_num=20, extra_ok=()):
    k_finish(sets, rnd, max_num=max_num, extra_ok=extra_ok)
    for s in sets:
        s["title"] = au(s["title"])
        for it in s["items"]:
            it["q"] = au(it["q"])
            it["c"] = [au(c) for c in it["c"]]
            it["e"] = au(it["e"])
    return sets


def make(slug, sort, code, domain, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets):
    unit = {
        "slug": slug, "sort": sort, "updated": UPDATED, "pdf_url": "",
        "title": title, "seo_title": seo_title, "short_title": short_title, "domain": domain,
        "standard_code": code, "standard_url": STD_URL, "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": au(body), "faq": [{"q": au(q), "a": au(a)} for q, a in faq], "sets": sets,
    }
    write_unit("au", "maths", "foundation", unit)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def figure(svg, cap):
    return "<figure class='sn-fig'>%s<figcaption>%s</figcaption></figure>" % (svg, cap)


def mistakes(rows):
    return "<h2>Common mistakes</h2>" + table(["Mistake", "What to do"], rows)


# ------------------------------------------------------------ pictures
def sky_svg(when):
    """A little scene for a time of day: morning, lunchtime, afternoon, night."""
    W, H = 200, 120
    sky = {"morning": "#fde9c8", "lunchtime": "#cfe8fb", "afternoon": "#f9d9a8", "night": "#23305a"}[when]
    s = ["<rect x='0' y='0' width='%d' height='%d' rx='10' fill='%s'/>" % (W, H, sky),
         "<rect x='0' y='%d' width='%d' height='%d' fill='#7cb36b'/>" % (H - 26, W, 26)]
    if when == "night":
        s.append("<circle cx='140' cy='36' r='18' fill='#f6f1c1'/><circle cx='148' cy='31' r='16' fill='%s'/>" % sky)
        for x, y in [(40, 24), (70, 50), (100, 18), (175, 64), (25, 66)]:
            s.append("<circle cx='%d' cy='%d' r='2.5' fill='#ffffff'/>" % (x, y))
    else:
        cx, cy = {"morning": (36, 78), "lunchtime": (100, 30), "afternoon": (162, 66)}[when]
        for k in range(8):
            a = k * math.pi / 4
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#f2a900' stroke-width='3' stroke-linecap='round'/>"
                     % (cx + 22 * math.cos(a), cy + 22 * math.sin(a), cx + 30 * math.cos(a), cy + 30 * math.sin(a)))
        s.append("<circle cx='%d' cy='%d' r='16' fill='#ffcc33' stroke='#e09a00' stroke-width='2'/>" % (cx, cy))
    return svg_wrap(W, H, "".join(s), "the sky at %s" % ("night time" if when == "night" else when))


def days_svg(days, hide=None):
    """A row of day cards. hide: index shown as a red ?"""
    w, h, gap = 92, 44, 8
    W = 2 * M + len(days) * w + (len(days) - 1) * gap
    s = []
    for i, d in enumerate(days):
        x = M + i * (w + gap)
        q = i == hide
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, M, w, h, FILL if q else "#ffffff", GREEN))
        s.append(text(x + w / 2, M + h / 2 + 6, "?" if q else d, 22 if q else 15, col=RED if q else INK))
    return svg_wrap(W, h + 2 * M, "".join(s), "days of the week")


def pictograph_svg(rows):
    """A picture graph: rows = [(kind, n)], one row per kind, each picture is one thing."""
    lw = 30
    sp = 34
    W = 2 * M + lw + 10 * sp
    H = 2 * M + len(rows) * (sp + 6)
    s = []
    for i, (k, n) in enumerate(rows):
        y = M + i * (sp + 6) + sp / 2
        s.append(obj(k, M + 14, y, 13))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='#bbbbbb' stroke-width='1.2'/>" % (M + lw, y - sp / 2, M + lw, y + sp / 2))
        for j in range(n):
            s.append(obj(k, M + lw + 8 + sp / 2 + j * sp, y, 12))
    return svg_wrap(int(W), int(H), "".join(s), "a picture graph of " + ", ".join(name(k) for k, _ in rows))


def pattern_svg(items, blanks=0):
    """A repeating pattern in a row: items are ('obj', kind) or ('shape', kind, colour); then `blanks` empty boxes."""
    sp = 44
    W = 2 * M + (len(items) + blanks) * sp
    s = []
    for i, it in enumerate(items):
        cx, cy = M + sp / 2 + i * sp, M + 22
        if it[0] == "blank":
            x = M + i * sp + 4
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % (x, M + 4, sp - 8, 36, FILL, GREEN))
            s.append(text(x + (sp - 8) / 2, M + 30, "?", 22, col=RED))
        elif it[0] == "obj":
            s.append(obj(it[1], cx, cy, 15))
        else:
            s.append(shape(it[1], cx, cy, 15, it[2]))
    for j in range(blanks):
        x = M + (len(items) + j) * sp + 4
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2' stroke-dasharray='5 4'/>" % (x, M + 4, sp - 8, 36, FILL, GREEN))
        s.append(text(x + (sp - 8) / 2, M + 30, "?", 22, col=RED))
    return svg_wrap(W, 44 + 2 * M, "".join(s), "a repeating pattern")


def choice_row_svg(cands):
    """Answer pictures A to D in a row; each cand is a list of items like pattern_svg."""
    sp = 40
    s = []
    x = M
    for i, items in enumerate(cands):
        s.append(text(x + 8, M + 30, "ABCD"[i], 18, col=GREEN))
        x += 24
        for it in items:
            if it[0] == "obj":
                s.append(obj(it[1], x + sp / 2, M + 24, 14))
            else:
                s.append(shape(it[1], x + sp / 2, M + 24, 14, it[2]))
            x += sp
        x += 20
    return svg_wrap(int(x + M), 48 + 2 * M, "".join(s), "answers A to D")
