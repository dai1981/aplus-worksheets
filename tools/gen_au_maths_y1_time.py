# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Days, weeks, months and time (Australian Curriculum v9.0, AC9M1M03)
  python3 tools/gen_au_maths_y1_time.py
Morning, afternoon and night and the order of events; days of the week with yesterday, today and tomorrow;
months and the Australian seasons (summer is December to February); which takes longer (minute, hour,
day, week, month, year); o’clock and half past on analog clocks for everyday events.
Common mistakes used as wrong answers: Northern Hemisphere seasons (Christmas in winter, July in summer),
yesterday and tomorrow mixed up, the clock hands swapped, half past read as the next hour,
“2 days is longer than 1 week” (looking only at the number).
Every day, month, season and clock answer is worked out in code. Australian English.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GREY = "#b9b2a6"
PALE = "#eef5f0"
GOLD = "#f2c230"
ORANGE = "#f08a24"
BLUE = "#3b7dd8"
SKY = "#cfe6f7"
NAVY = "#1f2d52"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DSHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
MSHORT = [m[:3] for m in MONTHS]
# Australian seasons (Southern Hemisphere). Month numbers 1-12.
SEASONS = [("summer", [12, 1, 2], "#f6c26b"), ("autumn", [3, 4, 5], "#e9a27a"),
           ("winter", [6, 7, 8], "#9cc3e6"), ("spring", [9, 10, 11], "#a8d08d")]
NORTH = {"summer": "winter", "winter": "summer", "autumn": "spring", "spring": "autumn"}


# ------------------------------------------------------------ time words
def nxt(h):
    return h % 12 + 1


def prv(h):
    return (h - 2) % 12 + 1


def oc(h):
    return "%d o’clock" % ((h - 1) % 12 + 1)


def hp(h):
    return "half past %d" % ((h - 1) % 12 + 1)


def say(h, m):
    return oc(h) if m == 0 else hp(h)


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def day_after(d, k=1):
    return DAYS[(DAYS.index(d) + k) % 7]


def month_after(mo, k=1):
    return MONTHS[(MONTHS.index(mo) + k) % 12]


def season_of(mo):
    n = MONTHS.index(mo) + 1
    return next(s for s, ms, c in SEASONS if n in ms)


def season_after(s, k=1):
    names = [x[0] for x in SEASONS]
    return names[(names.index(s) + k) % 4]


assert season_of("January") == "summer" and season_of("July") == "winter"
assert season_of("April") == "autumn" and season_of("October") == "spring"

# length of time in minutes (to check “which is longer”)
MIN = {"minute": 1, "hour": 60, "day": 1440, "week": 7 * 1440, "month": 30 * 1440, "year": 365 * 1440}


def dur(s):
    """'1 hour', '2 days', 'half an hour' -> minutes."""
    if s == "half an hour":
        return 30
    n, u = s.split(" ")
    return int(n) * MIN[u.rstrip("s")]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def txt(x, y, t, fs=16, col=LINE, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def wrap2(t, n=11):
    if len(t) <= n:
        return [t]
    words = t.split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        w = max(len(a), len(b))
        if best is None or w < best[0]:
            best = (w, a, b)
    assert best and best[0] <= 14, t
    return [best[1], best[2]]


# ------------------------------------------------------------ small pictures (icons in a 50 x 50 box)
def clock_body(h, m, cx, cy, R, numbers=True):
    """Analog clock. The short hand is placed by the exact time: (h + m/60) x 30 degrees."""
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, max(5 * k, 1.5))]
    small, big = [], []
    for i in range(60):
        if not numbers and i % 5:
            continue
        a = math.radians(i * 6 - 90)
        r1 = R - (13 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    if small:
        s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, max(2.6 * k, 1.2)))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.5 * math.cos(ah), cy + R * 0.5 * math.sin(ah), LINE, max(8 * k, 2.5)))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.86 * math.cos(am), cy + R * 0.86 * math.sin(am), RED, max(4.5 * k, 1.8)))
    if numbers:
        fs = 19 * k
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
                 "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R - 29 * k
            s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, max(6 * k, 2), LINE))
    return "".join(s)


def icon(name, x, y, sc=1.0):
    """A simple picture drawn in a 50 x 50 box at (x, y), scaled by sc."""
    S = "stroke='%s' stroke-width='2'" % LINE
    b = []
    if name == "sun":
        for i in range(8):
            a = math.radians(i * 45)
            b.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (25 + 15 * math.cos(a), 25 + 15 * math.sin(a), 25 + 22 * math.cos(a), 25 + 22 * math.sin(a), ORANGE))
        b.append("<circle cx='25' cy='25' r='11' fill='%s' stroke='%s' stroke-width='2'/>" % (GOLD, ORANGE))
    elif name == "sunrise":
        for d in (-150, -120, -90, -60, -30):
            a = math.radians(d)
            b.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                     % (25 + 16 * math.cos(a), 36 + 16 * math.sin(a), 25 + 23 * math.cos(a), 36 + 23 * math.sin(a), ORANGE))
        b.append("<path d='M13 36A12 12 0 0 1 37 36Z' fill='%s' stroke='%s' stroke-width='2'/>" % (GOLD, ORANGE))
        b.append("<line x1='2' y1='36' x2='48' y2='36' %s/>" % S)
        b.append("<path d='M6 42H44M12 47H38' stroke='%s' stroke-width='2' stroke-linecap='round'/>" % BLUE)
    elif name == "moon":
        b.append("<rect x='0' y='0' width='50' height='50' rx='8' fill='%s'/>" % NAVY)
        b.append("<path d='M30 9A16 16 0 1 0 41 35A13 13 0 1 1 30 9Z' fill='%s'/>" % GOLD)
        for (sx, sy) in [(38, 12), (12, 40), (43, 44)]:
            b.append("<circle cx='%d' cy='%d' r='2' fill='#fff'/>" % (sx, sy))
    elif name == "bowl":
        b.append("<line x1='36' y1='6' x2='29' y2='24' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % GREY)
        for (cx, cy) in [(16, 22), (22, 21), (28, 22), (34, 21)]:
            b.append("<circle cx='%d' cy='%d' r='3' fill='%s'/>" % (cx, cy, GOLD))
        b.append("<path d='M6 24H44A19 17 0 0 1 6 24Z' fill='%s' %s/>" % (BLUE, S))
    elif name == "bed":
        b.append("<rect x='5' y='12' width='6' height='32' fill='#c68a4a' %s/>" % S)
        b.append("<rect x='5' y='30' width='40' height='8' fill='#c68a4a' %s/>" % S)
        b.append("<line x1='44' y1='38' x2='44' y2='44' %s/>" % S)
        b.append("<ellipse cx='18' cy='26' rx='6' ry='4' fill='#fff' %s/>" % S)
        b.append("<rect x='24' y='22' width='21' height='8' rx='2' fill='%s' %s/>" % (BLUE, S))
    elif name == "school":
        b.append("<rect x='8' y='20' width='34' height='26' fill='%s' %s/>" % ("#f6d5d1", S))
        b.append("<path d='M4 21L25 6L46 21Z' fill='%s' %s/>" % (RED, S))
        b.append("<rect x='21' y='32' width='8' height='14' fill='#c68a4a' %s/>" % S)
        b.append("<rect x='12' y='25' width='7' height='6' fill='%s' %s/>" % (SKY, S))
        b.append("<rect x='31' y='25' width='7' height='6' fill='%s' %s/>" % (SKY, S))
    elif name == "lunchbox":
        b.append("<path d='M18 18V11H32V18' fill='none' stroke='%s' stroke-width='3'/>" % LINE)
        b.append("<rect x='6' y='18' width='38' height='26' rx='5' fill='#3fa34d' %s/>" % S)
        b.append("<line x1='6' y1='27' x2='44' y2='27' %s/>" % S)
        b.append("<rect x='21' y='24' width='8' height='6' fill='%s' %s/>" % (GOLD, S))
    elif name == "toothbrush":
        b.append("<rect x='4' y='28' width='30' height='6' rx='3' fill='%s' %s/>" % (BLUE, S))
        b.append("<rect x='32' y='26' width='14' height='8' rx='2' fill='#fff' %s/>" % S)
        b.append("<path d='M34 26V17M37 26V17M40 26V17M43 26V17' stroke='%s' stroke-width='2'/>" % "#3fa34d")
    elif name == "tap":
        b.append("<rect x='16' y='6' width='12' height='5' fill='%s' %s/>" % (GREY, S))
        b.append("<rect x='6' y='11' width='32' height='8' fill='%s' %s/>" % (GREY, S))
        b.append("<rect x='30' y='11' width='8' height='15' fill='%s' %s/>" % (GREY, S))
        for (cx, cy) in [(34, 32), (34, 40), (34, 47)]:
            b.append("<circle cx='%d' cy='%d' r='2.5' fill='%s'/>" % (cx, cy, BLUE))
    elif name == "plate":
        b.append("<circle cx='25' cy='26' r='16' fill='#fff' %s/>" % S)
        b.append("<circle cx='25' cy='26' r='10' fill='#f6d5d1' stroke='%s' stroke-width='1.5'/>" % LINE)
        b.append("<path d='M4 10V42M2 10V18M6 10V18M46 10V42' stroke='%s' stroke-width='2' stroke-linecap='round'/>" % GREY)
    elif name == "bath":
        for (cx, cy, r) in [(18, 16, 4), (26, 12, 5), (34, 17, 4)]:
            b.append("<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r, BLUE))
        b.append("<path d='M4 24H46V32A8 8 0 0 1 38 40H12A8 8 0 0 1 4 32Z' fill='#fff' %s/>" % S)
        b.append("<path d='M12 40V46M38 40V46' %s/>" % S)
    elif name == "book":
        b.append("<path d='M25 13L5 8V40L25 45Z' fill='#fff' %s/>" % S)
        b.append("<path d='M25 13L45 8V40L25 45Z' fill='#fff' %s/>" % S)
        b.append("<path d='M9 17L21 20M9 24L21 27M9 31L21 34M29 20L41 17M29 27L41 24M29 34L41 31' "
                 "stroke='%s' stroke-width='1.5'/>" % GREY)
    elif name == "bus":
        b.append("<rect x='3' y='12' width='44' height='24' rx='4' fill='%s' %s/>" % (GOLD, S))
        for wx in (7, 18, 29):
            b.append("<rect x='%d' y='16' width='8' height='8' fill='%s' stroke='%s' stroke-width='1.5'/>" % (wx, SKY, LINE))
        b.append("<rect x='39' y='16' width='5' height='16' fill='%s' stroke='%s' stroke-width='1.5'/>" % (SKY, LINE))
        for wx in (13, 35):
            b.append("<circle cx='%d' cy='37' r='5' fill='%s' stroke='#fff' stroke-width='1.5'/>" % (wx, LINE))
    elif name == "shirt":
        b.append("<path d='M17 8L8 14L4 24L11 27L13 22V44H37V22L39 27L46 24L42 14L33 8Q25 15 17 8Z' "
                 "fill='%s' %s/>" % (BLUE, S))
    elif name == "seed":
        b.append("<rect x='2' y='34' width='46' height='12' fill='#c68a4a'/>")
        b.append("<ellipse cx='25' cy='31' rx='5' ry='3.5' fill='#7a5230' %s/>" % S)
    elif name == "sprout":
        b.append("<rect x='2' y='38' width='46' height='10' fill='#c68a4a'/>")
        b.append("<path d='M25 38V18' stroke='#3fa34d' stroke-width='3'/>")
        b.append("<path d='M25 26Q14 26 12 16Q23 16 25 26ZM25 22Q36 22 38 12Q27 12 25 22Z' fill='#3fa34d'/>")
    elif name == "flower":
        b.append("<path d='M25 46V22' stroke='#3fa34d' stroke-width='3'/>")
        b.append("<path d='M25 38Q15 38 13 30Q23 30 25 38Z' fill='#3fa34d'/>")
        for i in range(5):
            a = math.radians(i * 72 - 90)
            b.append("<circle cx='%.1f' cy='%.1f' r='6' fill='#e86aa6' stroke='%s' stroke-width='1.2'/>"
                     % (25 + 8 * math.cos(a), 17 + 8 * math.sin(a), LINE))
        b.append("<circle cx='25' cy='17' r='4.5' fill='%s' stroke='%s' stroke-width='1.2'/>" % (GOLD, LINE))
    elif name == "leaf":
        b.append("<path d='M8 42Q6 10 42 8Q44 40 8 42Z' fill='%s' %s/>" % (ORANGE, S))
        b.append("<path d='M8 42L36 14' stroke='%s' stroke-width='2'/>" % "#a0521b")
    elif name == "rain":
        for (cx, cy, r) in [(15, 22, 9), (26, 16, 12), (37, 23, 8)]:
            b.append("<circle cx='%d' cy='%d' r='%d' fill='%s'/>" % (cx, cy, r, "#9aa5b1"))
        b.append("<rect x='12' y='22' width='26' height='9' fill='%s'/>" % "#9aa5b1")
        b.append("<path d='M15 36L12 44M25 36L22 44M35 36L32 44' stroke='%s' stroke-width='2.5' stroke-linecap='round'/>" % BLUE)
    elif name == "cake":
        for cx in (17, 25, 33):
            b.append("<line x1='%d' y1='14' x2='%d' y2='24' stroke='%s' stroke-width='3'/>" % (cx, cx, BLUE))
            b.append("<ellipse cx='%d' cy='10' rx='2.5' ry='4' fill='%s'/>" % (cx, ORANGE))
        b.append("<rect x='8' y='24' width='34' height='20' rx='3' fill='#f6d5d1' %s/>" % S)
        b.append("<path d='M8 31Q14 36 19 31Q25 36 31 31Q37 36 42 31' fill='none' stroke='%s' stroke-width='2'/>" % "#e86aa6")
    elif name == "footy":
        b.append("<ellipse cx='25' cy='25' rx='20' ry='12' transform='rotate(-30 25 25)' fill='#b5562b' %s/>" % S)
        b.append("<path d='M18 22L31 15M21 19L23 23M25 17L27 21M29 15L31 19' stroke='#fff' stroke-width='2'/>")
    elif name == "wave":
        b.append("<path d='M2 30Q10 18 18 30T34 30T50 30V48H2Z' fill='%s'/>" % BLUE)
        b.append("<path d='M2 40Q10 32 18 40T34 40T50 40' fill='none' stroke='#fff' stroke-width='2'/>")
    elif name == "castle":
        b.append("<rect x='0' y='40' width='50' height='8' fill='%s'/>" % "#e8c98a")
        b.append("<path d='M10 40V20H16V25H22V20H28V25H34V20H40V40Z' fill='%s' %s/>" % ("#e8c98a", S))
        b.append("<rect x='21' y='31' width='8' height='9' fill='#c68a4a'/>")
    elif name == "flat":
        b.append("<rect x='0' y='40' width='50' height='8' fill='%s'/>" % "#e8c98a")
        b.append("<path d='M8 40Q25 31 42 40Z' fill='%s' %s/>" % ("#e8c98a", S))
        b.append("<path d='M2 46Q10 41 18 46T34 46T50 46' fill='none' stroke='%s' stroke-width='2'/>" % BLUE)
    elif name.startswith("clock:"):
        hh, mm = [int(v) for v in name[6:].split(":")]
        b.append(clock_body(hh, mm, 25, 25, 23, numbers=False))
    elif name == "minute":                  # the long hand moves 1 small step
        b.append(clock_body(12, 0, 25, 25, 23, numbers=False))
        b.append("<path d='M25 2A23 23 0 0 1 27.4 2.1' fill='none' stroke='%s' stroke-width='8'/>" % ORANGE)
    elif name == "hour":                    # the long hand goes all the way round
        b.append(clock_body(12, 0, 25, 25, 23, numbers=False))
        b.append("<circle cx='25' cy='25' r='23' fill='none' stroke='%s' stroke-width='4' stroke-dasharray='130 15'/>" % ORANGE)
    elif name == "day":
        b.append("<rect x='12' y='12' width='26' height='26' rx='3' fill='%s' %s/>" % (GOLD, S))
    elif name == "week":
        for i in range(7):
            b.append("<rect x='%.1f' y='20' width='6' height='10' fill='%s' stroke='%s' stroke-width='1'/>" % (1 + i * 7, GOLD, LINE))
    elif name == "month":
        for r in range(5):
            for i in range(7):
                if r * 7 + i < 30:
                    b.append("<rect x='%.1f' y='%.1f' width='6' height='6' fill='%s' stroke='%s' stroke-width='0.8'/>"
                             % (1 + i * 7, 8 + r * 7, GOLD, LINE))
    elif name == "year":
        for r in range(3):
            for i in range(4):
                b.append("<rect x='%d' y='%d' width='11' height='11' fill='%s' stroke='%s' stroke-width='1'/>"
                         % (1 + i * 12.5, 8 + r * 12.5, GOLD, LINE))
    else:
        raise ValueError(name)
    return "<g transform='translate(%.1f %.1f) scale(%.2f)'>%s</g>" % (x, y, sc, "".join(b))


# ------------------------------------------------------------ larger pictures
def clock_svg(h, m, size=200):
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), "clock showing %s" % say(h, m))


def clocks4_svg(times):
    CELL = 124
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GREY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GREY)]
    for k, (h, m) in enumerate(times):
        assert hands_gap(h, m) >= 12, (h, m)
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        el.append(clock_body(h, m, x0 + 65, y0 + 63, 56))
        el.append(txt(x0 + 5, y0 + 20, "ABCD"[k], 18, anchor="start"))
    return svg_wrap(W, H, "".join(el), "four clocks labelled A to D")


def clocks2_svg(t1, t2, l1="starts", l2="ends"):
    R = 70
    W, H = 2 * (2 * R + 12) + 50, 2 * R + 40
    el = [clock_body(t1[0], t1[1], R + 6, R + 6, R), clock_body(t2[0], t2[1], W - R - 6, R + 6, R),
          txt(R + 6, 2 * R + 32, l1, 18), txt(W - R - 6, 2 * R + 32, l2, 18)]
    ax, ay = 2 * R + 16, R + 6
    el.append("<path d='M%d %dH%dM%d %dL%d %dL%d %d' stroke='%s' stroke-width='3' fill='none' stroke-linecap='round' "
              "stroke-linejoin='round'/>" % (ax, ay, ax + 30, ax + 23, ay - 7, ax + 30, ay, ax + 23, ay + 7, LINE))
    return svg_wrap(W, H, "".join(el), "two clocks: %s and %s" % (say(*t1), say(*t2)))


def cards_svg(cards, arrows=True, bw=112, gap=24, letters=False):
    """Cards in a row. card = (icon or None, label). Label '?' is a missing card (red, dashed)."""
    FS = 15
    has_icon = any(c[0] for c in cards)
    IH = 56 if has_icon else 0
    lines = [wrap2(lb) if lb != "?" else ["?"] for ic, lb in cards]
    nl = max(len(x) for x in lines)
    BH = IH + nl * 18 + 16 + (0 if has_icon else 14)
    top = 24 if letters else 4
    W = len(cards) * bw + (len(cards) - 1) * gap + 8
    H = top + BH + 4
    el = []
    for i, (ic, lb) in enumerate(cards):
        x = 4 + i * (bw + gap)
        miss = lb == "?"
        el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='2.5'%s/>"
                  % (x, top, bw, BH, "#fff" if miss else PALE, RED if miss else GREEN,
                     " stroke-dasharray='7 5'" if miss else ""))
        if letters:
            el.append(txt(x + bw / 2.0, 18, "ABCD"[i], 17))
        if miss:
            el.append(txt(x + bw / 2.0, top + BH / 2.0 + 11, "?", 30, RED))
            continue
        if ic:
            el.append(icon(ic, x + bw / 2.0 - 25, top + 5))
        ls = lines[i]
        for s in ls:
            assert len(s) * FS * 0.58 <= bw - 8, s
        if has_icon:
            y0 = top + IH + 16
        else:
            y0 = top + BH / 2.0 - (len(ls) - 1) * 9 + 5
        for j, s in enumerate(ls):
            el.append(txt(x + bw / 2.0, y0 + j * 18, s, FS))
        if arrows and i < len(cards) - 1:
            ax, ay = x + bw + 3, top + BH // 2
            el.append("<path d='M%d %dH%dM%d %dL%d %dL%d %d' stroke='%s' stroke-width='2.5' fill='none' "
                      "stroke-linecap='round' stroke-linejoin='round'/>"
                      % (ax, ay, ax + gap - 6, ax + gap - 11, ay - 6, ax + gap - 6, ay, ax + gap - 11, ay + 6, LINE))
    lab = ("cards in order: " if arrows else "cards: ") + ", ".join(lb for ic, lb in cards)
    return svg_wrap(W, H, "".join(el), lab)


def pic_svg(name, label, size=120):
    """One icon, drawn large."""
    sc = (size - 8) / 50.0
    return svg_wrap(size, size, icon(name, 4, 4, sc), "picture: " + label)


def pair_svg(a, b):
    """Two cards with 'or' between them. a, b = (icon, label)."""
    bw, gap, IH = 170, 46, 76
    W, H = 2 * bw + gap + 8, IH + 52
    el = []
    for i, (ic, lb) in enumerate([a, b]):
        x = 4 + i * (bw + gap)
        el.append("<rect x='%d' y='4' width='%d' height='%d' rx='10' fill='%s' stroke='%s' stroke-width='2.5'/>"
                  % (x, bw, H - 8, PALE, GREEN))
        el.append(icon(ic, x + bw / 2.0 - 35, 8, 1.4))
        assert len(lb) * 17 * 0.58 <= bw - 8, lb
        el.append(txt(x + bw / 2.0, IH + 30, lb, 17))
    el.append(txt(W / 2.0, H / 2.0 + 6, "or", 18))
    return svg_wrap(W, H, "".join(el), "two cards: %s or %s" % (a[1], b[1]))


def scene_body(kind, x, y, w=110, h=80):
    if kind == "morning":
        bg = "#fde7c4"
    elif kind == "afternoon":
        bg = SKY
    else:
        bg = NAVY
    el = ["<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, w, h, bg, LINE),
          "<rect x='%d' y='%d' width='%d' height='14' fill='%s'/>" % (x + 1, y + h - 15, w - 2, "#7cbf6b" if kind != "night" else "#2f4a35")]
    if kind == "morning":
        el.append("<circle cx='%d' cy='%d' r='14' fill='%s' stroke='%s' stroke-width='2'/>" % (x + 26, y + h - 17, GOLD, ORANGE))
        el.append("<rect x='%d' y='%d' width='%d' height='14' fill='#7cbf6b'/>" % (x + 1, y + h - 15, w - 2))
    elif kind == "afternoon":
        el.append(icon("sun", x + w / 2.0 - 18, y + 2, 0.72))
    else:
        el.append("<path d='M%d %dA14 14 0 1 0 %d %dA11 11 0 1 1 %d %dZ' fill='%s'/>"
                  % (x + 62, y + 12, x + 72, y + 36, x + 62, y + 12, GOLD))
        for (sx, sy) in [(18, 14), (34, 30), (88, 16), (96, 40), (14, 44)]:
            el.append("<circle cx='%d' cy='%d' r='2' fill='#fff'/>" % (x + sx, y + sy))
    el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='none' stroke='%s' stroke-width='2'/>" % (x, y, w, h, LINE))
    return "".join(el)


def scene_svg(kind):
    return svg_wrap(118, 88, scene_body(kind, 4, 4), "sky picture: " + kind)


def scenes_svg(kinds):
    el = []
    for i, k in enumerate(kinds):
        x = 4 + i * 126
        el.append(txt(x + 55, 18, "ABC"[i], 17))
        el.append(scene_body(k, x, 26))
    return svg_wrap(3 * 126 - 8 + 4, 26 + 80 + 4, "".join(el), "three sky pictures labelled A to C")


def week_svg(today=None, miss=None, mark=None):
    """The 7 days in order (Monday first). today: day name to circle as 'today'. miss: day shown as '?'."""
    bw, gap, bh = 56, 6, 40
    top = 4
    W = 7 * bw + 6 * gap + 8
    H = top + bh + (26 if today else 6)
    el = []
    for i, d in enumerate(DAYS):
        x = 4 + i * (bw + gap)
        if d == miss:
            el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='#fff' stroke='%s' stroke-width='2.5' "
                      "stroke-dasharray='6 4'/>" % (x, top, bw, bh, RED))
            el.append(txt(x + bw / 2.0, top + 28, "?", 24, RED))
            continue
        hi = d == today
        el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='%s' stroke='%s' stroke-width='%s'/>"
                  % (x, top, bw, bh, GOLD if hi else (PALE if i < 5 else "#dfe9f5"), GREEN if not hi else LINE,
                     "3" if hi else "2"))
        el.append(txt(x + bw / 2.0, top + 26, DSHORT[i], 17))
        if hi:
            el.append(txt(x + bw / 2.0, top + bh + 20, "today", 16, RED))
    lab = "the days of the week" + (", today is " + today if today else "") + (", one day missing" if miss else "")
    return svg_wrap(W, H, "".join(el), lab)


def months_svg(miss=None):
    """12 months in 2 rows of 6."""
    bw, bh, gap = 58, 38, 6
    W = 6 * bw + 5 * gap + 8
    H = 2 * bh + gap + 8
    el = []
    for i, m in enumerate(MONTHS):
        x = 4 + (i % 6) * (bw + gap)
        y = 4 + (i // 6) * (bh + gap)
        if m == miss:
            el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='#fff' stroke='%s' stroke-width='2.5' "
                      "stroke-dasharray='6 4'/>" % (x, y, bw, bh, RED))
            el.append(txt(x + bw / 2.0, y + 27, "?", 24, RED))
        else:
            el.append("<rect x='%d' y='%d' width='%d' height='%d' rx='7' fill='%s' stroke='%s' stroke-width='2'/>"
                      % (x, y, bw, bh, PALE, GREEN))
            el.append(txt(x + bw / 2.0, y + 25, MSHORT[i], 17))
    return svg_wrap(W, H, "".join(el), "the months of the year" + (", one month missing" if miss else ""))


def seasons_svg(miss_season=None, miss_month=None):
    """The Australian year from December: summer, autumn, winter, spring. Each season has 3 months."""
    bw, bh, gap, ggap = 46, 36, 4, 14
    gw = 3 * bw + 2 * gap
    W = 4 * gw + 3 * ggap + 4
    H = bh + 40
    s = []
    for g, (name, ms, col) in enumerate(SEASONS):
        gx = 2 + g * (gw + ggap)
        for i, m in enumerate(ms):
            x = gx + i * (bw + gap)
            if m == miss_month:
                s.append("<rect x='%d' y='2' width='%d' height='%d' rx='6' fill='#fff' stroke='%s' stroke-width='2'/>"
                         % (x, bw, bh, RED))
                s.append(txt(x + bw / 2.0, 28, "?", 22, RED))
            else:
                s.append("<rect x='%d' y='2' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x, bw, bh, col, LINE))
                s.append(txt(x + bw / 2.0, 26, MSHORT[m - 1], 16))
        if name == miss_season:
            s.append(txt(gx + gw / 2.0, bh + 30, "?", 20, RED))
        else:
            s.append(txt(gx + gw / 2.0, bh + 29, name.capitalize(), 17))
    return svg_wrap(W, H, "".join(s), "seasons in Australia")


def calpage_svg(month, ic=None):
    """A calendar page with the month name (and a small picture)."""
    W, H = 170, 132
    el = ["<rect x='4' y='12' width='162' height='116' rx='8' fill='#fff' stroke='%s' stroke-width='2.5'/>" % LINE,
          "<path d='M5 20A8 8 0 0 1 12 13H158A8 8 0 0 1 165 20V42H5Z' fill='%s'/>" % GREEN]
    for rx in (40, 130):
        el.append("<rect x='%d' y='4' width='6' height='16' rx='3' fill='%s'/>" % (rx - 3, LINE))
    el.append(txt(85, 35, month, 19, "#fff"))
    cols = 4 if ic else 7
    for r in range(4):
        for i in range(cols):
            el.append("<rect x='%d' y='%d' width='14' height='14' fill='%s' stroke='%s' stroke-width='1'/>"
                      % (14 + i * 20, 50 + r * 19, PALE, GREY))
    if ic:
        el.append(icon(ic, 102, 58, 1.1))
    return svg_wrap(W, H, "".join(el), "calendar page: " + month)


# ------------------------------------------------------------ clock questions
def hour_e(h):
    return ("The long hand is on the <b>12</b>, so it is o’clock. "
            "The short hand points to the <b>%d</b>. It is <b>%s</b>." % (h, oc(h)))


def half_e(h):
    return ("The long hand is on the <b>6</b>, so it is half past. "
            "The short hand has gone past the %d. It is <b>%s</b>, not %s." % (h, hp(h), hp(nxt(h))))


def read_hour(h, rnd, text):
    rest = [hp(h), oc(nxt(h)), oc(prv(h))]
    rnd.shuffle(rest)
    cands = ["12 o’clock"] + rest if h != 12 else rest + ["6 o’clock"]
    e = hour_e(h) + (" (12 o’clock mixes up the hands.)" if h != 12 else "")
    return mcq(fig(clock_svg(h, 0)) + text, oc(h), cands, e)


def read_half(h, rnd, text):
    rest = ["6 o’clock" if h != 6 else hp(prv(h)), oc(h), oc(nxt(h))]
    rnd.shuffle(rest)
    return mcq(fig(clock_svg(h, 30)) + text, hp(h), [hp(nxt(h))] + rest, half_e(h))


def four_clocks(h, m, p, rnd):
    if m == 0:
        swap = (12, 5 * h)
        wrong = [swap, (nxt(h), 0), (h, 30)]
    else:
        swap = (6, 5 * h) if h != 6 else None
        wrong = [(nxt(h), 30), (h, 0), swap if swap else (prv(h), 30)]
    rnd.shuffle(wrong)
    times = wrong[:p] + [(h, m)] + wrong[p:]
    assert len(set(times)) == 4
    L = "ABCD"[p]
    if m == 0:
        e = "Clock %s has the long hand on the 12 and the short hand on the %d. It shows <b>%s</b>." % (L, h, oc(h))
    else:
        e = ("Clock %s has the long hand on the 6 and the short hand just past the %d. It shows <b>%s</b>."
             % (L, h, hp(h)))
    if swap in times:
        e += " Clock %s has the hands swapped." % "ABCD"[times.index(swap)]
    if (nxt(h), 30) in times:
        e += " Clock %s shows %s." % ("ABCD"[times.index((nxt(h), 30))], hp(nxt(h)))
    return times, e


def clocks_item(top, h, m, p, rnd):
    times, e = four_clocks(h, m, p, rnd)
    return {"q": top + fig(clocks4_svg(times)), "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True}


# ============================================================ set 1: morning, afternoon and night
def set_day(rnd, P):
    its = []
    its.append(mcq(fig(scene_svg("morning")) + "The sun comes up. When is it?", "morning",
                   ["night", "afternoon", "lunch time"],
                   "The sun comes up at the start of the day. That is the <b>morning</b>."))
    its.append(mcq(fig(scene_svg("night")) + "The moon and stars are out. When is it?", "night",
                   ["morning", "afternoon", "recess"],
                   "We see the moon and stars when it is dark. That is <b>night</b>."))
    n, he, his = P.next()
    its.append(mcq(fig(pic_svg("bowl", "a bowl of cereal")) + "%s eats breakfast. When is it?" % n, "in the morning",
                   ["at night", "in the afternoon", "at lunch time"],
                   "Breakfast is the first meal of the day. We eat it <b>in the morning</b>."))
    n, he, his = P.next()
    its.append(mcq(fig(pic_svg("bed", "a bed")) + "%s goes to sleep in bed. When is it?" % n, "at night",
                   ["in the morning", "at recess", "in the afternoon"],
                   "We sleep when it is dark, <b>at night</b>."))
    its.append(mcq(fig(pic_svg("school", "a school")) + "School finishes. It is home time. When is it?",
                   "in the afternoon", ["in the morning", "at night", "at breakfast"],
                   "School finishes after lunch. That is <b>in the afternoon</b>."))
    its.append(mcq(fig(pic_svg("lunchbox", "a lunchbox")) + "We eat lunch at school. What comes <b>after</b> lunch?",
                   "the afternoon", ["the morning", "breakfast", "waking up"],
                   "Lunch is in the middle of the day. After lunch comes <b>the afternoon</b>."))
    n, he, his = P.next()
    its.append(mcq(fig(pic_svg("toothbrush", "a toothbrush")) + "%s brushes %s teeth just before bed. When is it?" % (n, his),
                   "at night", ["at recess", "at lunch time", "in the afternoon"],
                   "Bedtime is at the end of the day. So it is <b>at night</b>."))
    its.append(mcq(fig(cards_svg([("sunrise", "morning"), ("sun", "afternoon"), (None, "?")])) +
                   "Which part of the day is missing?", "night", ["morning", "afternoon", "lunch time"],
                   "The day goes morning, afternoon, then <b>night</b>."))
    its.append(mcq(fig(cards_svg([(None, "?"), ("sun", "afternoon"), ("moon", "night")])) +
                   "Which part of the day is missing?", "morning", ["night", "afternoon", "dinner time"],
                   "The day starts with the <b>morning</b>. Then comes the afternoon, then night."))
    its.append(mcq(fig(cards_svg([("sunrise", "wake up"), ("bowl", "eat breakfast"), ("school", "go to school"),
                                  ("plate", "eat dinner")])) + "What happens <b>first</b>?", "wake up",
                   ["eat dinner", "eat breakfast", "go to school"],
                   "Follow the arrows from the left. The first card is <b>wake up</b>."))
    its.append(mcq(fig(cards_svg([("sunrise", "get up"), ("shirt", "get dressed"), ("bowl", "eat breakfast"),
                                  ("bus", "catch the bus")])) + "What happens <b>last</b>?", "catch the bus",
                   ["get up", "eat breakfast", "get dressed"],
                   "Follow the arrows to the end. The last card is <b>catch the bus</b>. (Get up is first, not last.)"))
    its.append(mcq(fig(cards_svg([("seed", "plant a seed"), ("tap", "water it"), ("sprout", "it grows"),
                                  ("flower", "a flower opens")])) + "What happens <b>just after</b> “water it”?",
                   "it grows", ["plant a seed", "a flower opens", "water it"],
                   "Find “water it”. Follow the arrow to the next card: <b>it grows</b>. (Plant a seed comes before.)"))
    its.append(mcq(fig(cards_svg([("sun", "go to the beach"), ("castle", "make a sandcastle"), ("wave", "a wave comes"),
                                  ("flat", "it washes away")])) + "What happens <b>just before</b> “it washes away”?",
                   "a wave comes", ["go to the beach", "make a sandcastle", "it washes away"],
                   "Find “it washes away”. Look at the card just before it: <b>a wave comes</b>."))
    its.append(mcq(fig(cards_svg([("plate", "eat dinner"), ("bath", "have a bath"), (None, "?"), ("bed", "go to sleep")])) +
                   "What goes in the card with the <b>?</b>", "read a story",
                   ["wake up", "eat breakfast", "go to school"],
                   "It is after a bath and before sleep, so it is at night: <b>read a story</b>. "
                   "Waking up, breakfast and school are in the morning."))
    its.append(mcq(fig(cards_svg([("school", "get to school"), ("footy", "recess"), (None, "?"), ("bus", "home time")])) +
                   "What goes in the card with the <b>?</b>", "lunch",
                   ["breakfast", "dinner", "bedtime"],
                   "At school, recess comes first. Then <b>lunch</b>. Then it is home time."))
    n, he, his = P.next()
    its.append(mcq(fig(pic_svg("plate", "a dinner plate")) +
                   "%s eats dinner. After dinner, %s has a bath. What does %s do <b>first</b>?" % (n, he, he),
                   "eats dinner", ["has a bath", "goes to school", "eats breakfast"],
                   "“After dinner, %s has a bath” means dinner comes first. So %s <b>eats dinner</b> first." % (he, he)))
    its.append(mcq("You put on your socks ____ your shoes.", "before", ["after", "at the same time as", "instead of"],
                   "Socks go on first. Then shoes go on top. So socks go on <b>before</b> your shoes."))
    its.append(mcq(fig(pic_svg("tap", "a tap")) + "You dry your hands ____ you wash them.", "after",
                   ["before", "at the same time as", "instead of"],
                   "First you wash your hands. Then you dry them. So you dry them <b>after</b> you wash them."))
    its.append(mcq(fig(scenes_svg(["night", "morning", "afternoon"])) +
                   "Put the pictures in order for one day. Start with the morning.", "B, C, A",
                   ["A, B, C", "C, B, A", "B, A, C"],
                   "B is the morning (the sun comes up). C is the afternoon (the sun is high). A is night (the moon). "
                   "The order is <b>B, C, A</b>."))
    n, he, his = P.next()
    its.append(mcq(fig(pic_svg("school", "a school")) +
                   "%s wakes up. Then %s goes to school. Then %s goes to bed. What does %s do in the <b>middle</b>?"
                   % (n, he, he, he), "goes to school", ["wakes up", "goes to bed", "eats dinner"],
                   "First %s wakes up. In the middle %s <b>goes to school</b>. Last, %s goes to bed." % (he, he, he)))
    assert len(its) == 20, len(its)
    return {"title": "Morning, afternoon and night: the order of events", "items": its}


# ============================================================ set 2: days of the week
def day_q(today, k, rnd_text=None):
    """Today is X. What day is it k days later (k = 1 tomorrow, -1 yesterday, 2 the day after tomorrow)?"""
    ans = day_after(today, k)
    if k == 1:
        q = "Today is <b>%s</b>. What day will it be <b>tomorrow</b>?" % today
        e = ("Tomorrow is the day <b>after</b> today. The day after %s is <b>%s</b>. (%s was yesterday.)"
             % (today, ans, day_after(today, -1)))
        cands = [day_after(today, -1), day_after(today, 2), today]
    elif k == -1:
        q = "Today is <b>%s</b>. What day was it <b>yesterday</b>?" % today
        e = ("Yesterday is the day <b>before</b> today. The day before %s is <b>%s</b>. (%s is tomorrow.)"
             % (today, ans, day_after(today, 1)))
        cands = [day_after(today, 1), day_after(today, -2), today]
    else:
        q = "Today is <b>%s</b>. What day is the day <b>after tomorrow</b>?" % today
        e = ("Tomorrow is %s. The day after that is <b>%s</b>." % (day_after(today, 1), ans))
        cands = [day_after(today, 1), day_after(today, -2), day_after(today, 3)]
    return mcq(fig(week_svg(today=today)) + q, ans, cands, e)


def set_week(rnd, P):
    its = []
    its.append(mcq(fig(week_svg()) + "How many days are in a <b>week</b>?", "7", ["5", "12", "6"],
                   "Count the days: Monday to Sunday. There are <b>7 days</b> in a week. (5 is only the school days.)"))
    for d, w in [("Wednesday", ["Thursday", "Sunday", "Friday"]), ("Saturday", ["Sunday", "Friday", "Monday"])]:
        its.append(mcq(fig(week_svg(miss=d)) + "Which day is missing?", d, w,
                       "%s comes before the gap and %s comes after it. The missing day is <b>%s</b>."
                       % (day_after(d, -1), day_after(d, 1), d)))
    its.append(mcq(fig(week_svg()) + "Which day comes just <b>after Monday</b>?", day_after("Monday"),
                   ["Sunday", "Wednesday", "Thursday"],
                   "Say the days in order: Monday, <b>Tuesday</b>. Tuesday comes just after Monday. (Sunday comes before.)"))
    its.append(mcq(fig(week_svg()) + "Which day comes just <b>before Friday</b>?", day_after("Friday", -1),
                   ["Saturday", "Wednesday", "Monday"],
                   "Say the days in order: Wednesday, <b>Thursday</b>, Friday. (Saturday comes after Friday.)"))
    its.append(mcq(fig(week_svg()) + "Which day comes just <b>after Sunday</b>?", day_after("Sunday"),
                   ["Saturday", "Tuesday", "Friday"],
                   "Sunday is the last day of the week. Then a new week starts with <b>Monday</b>."))
    its.append(mcq(fig(week_svg()) + "Which two days are the <b>weekend</b>?", "Saturday and Sunday",
                   ["Friday and Saturday", "Sunday and Monday", "Monday and Friday"],
                   "Most children go to school Monday to Friday. <b>Saturday and Sunday</b> are the weekend."))
    its.append(mcq(fig(pic_svg("school", "a school")) + "On which days do most children go to school?", "Monday to Friday",
                   ["Saturday and Sunday", "Monday to Sunday", "Tuesday to Saturday"],
                   "School days are <b>Monday to Friday</b>. That is 5 days. Saturday and Sunday are the weekend."))
    its.append(mcq(fig(cards_svg([(None, "Monday"), (None, "Tuesday (today)"), (None, "Wednesday")], bw=140)) +
                   "Today is Tuesday. Wednesday is …", "tomorrow", ["yesterday", "today", "the weekend"],
                   "Wednesday comes just <b>after</b> today. The day after today is <b>tomorrow</b>."))
    its.append(mcq(fig(cards_svg([(None, "Monday"), (None, "Tuesday (today)"), (None, "Wednesday")], bw=140)) +
                   "Today is Tuesday. Monday was …", "yesterday", ["tomorrow", "today", "next week"],
                   "Monday comes just <b>before</b> today. The day before today is <b>yesterday</b>."))
    its.append(day_q("Thursday", 1))
    its.append(day_q("Monday", -1))
    its.append(day_q("Saturday", 1))
    its.append(day_q("Wednesday", -1))
    its.append(mcq(fig(week_svg()) + "<b>Yesterday</b> was Friday. What day is it today?", day_after("Friday"),
                   ["Thursday", "Sunday", "Friday"],
                   "Today is the day after yesterday. The day after Friday is <b>Saturday</b>. "
                   "(Thursday is the day before Friday, not after.)"))
    its.append(mcq(fig(week_svg()) + "<b>Tomorrow</b> will be Monday. What day is it today?", day_after("Monday", -1),
                   ["Tuesday", "Saturday", "Monday"],
                   "Today is the day before tomorrow. The day before Monday is <b>Sunday</b>. (Tuesday is after Monday.)"))
    its.append(day_q("Wednesday", 2))
    n, he, his = P.next()
    its.append(mcq(fig(week_svg(today="Friday")) +
                   "Today is Friday. %s’s footy game is on Sunday. How many sleeps until the game?" % n, "2",
                   ["1", "3", "7"],
                   "Sleep 1: Friday night, then it is Saturday. Sleep 2: Saturday night, then it is Sunday. "
                   "That is <b>2 sleeps</b>."))
    assert DAYS.index("Sunday") - DAYS.index("Friday") == 2
    its.append(mcq(fig(week_svg(today="Monday")) + "Today is Monday. Library day is Thursday. How many days away is it?",
                   str(DAYS.index("Thursday") - DAYS.index("Monday")), ["4", "2", "1"],
                   "Count on from Monday: Tuesday (1), Wednesday (2), Thursday (3). Library day is <b>3 days</b> away. "
                   "(Do not count Monday itself.)"))
    its.append(mcq(fig(week_svg()) + "How many <b>school days</b> are in a week?", "5", ["7", "2", "6"],
                   "Monday, Tuesday, Wednesday, Thursday, Friday. That is <b>5 school days</b>. (7 is every day of the week.)"))
    assert len(its) == 20, len(its)
    return {"title": "Days of the week: yesterday, today and tomorrow", "items": its}


# ============================================================ set 3: months and seasons in Australia
def season_q(month, ic, lead, extra=""):
    s = season_of(month)
    others = [NORTH[s]] + [x[0] for x in SEASONS if x[0] not in (s, NORTH[s])]
    ms = next(m for n, m, c in SEASONS if n == s)
    e = ("In Australia, %s is %s, %s and %s. So %s is <b>%s</b>."
         % (s, MONTHS[ms[0] - 1], MONTHS[ms[1] - 1], MONTHS[ms[2] - 1], month, s))
    e += " (%s is %s in countries in the north of the world, like England, not in Australia.)" % (month, NORTH[s])
    return mcq(fig(calpage_svg(month, ic)) + lead + extra, s, others, e)


def set_months(rnd, P):
    its = []
    its.append(mcq(fig(months_svg()) + "How many months are in a <b>year</b>?", "12", ["7", "4", "10"],
                   "Count them: January to December. There are <b>12 months</b>. (7 is days in a week. 4 is seasons.)"))
    its.append(mcq(fig(months_svg()) + "Which is the <b>first</b> month of the year?", "January",
                   ["December", "March", "June"],
                   "The year starts with <b>January</b>. December is the last month."))
    for m, w in [("May", ["June", "March", "July"]), ("October", ["November", "September", "December"])]:
        its.append(mcq(fig(months_svg(miss=m)) + "Which month is missing?", m, w,
                       "%s comes before the gap and %s comes after it. The missing month is <b>%s</b>."
                       % (month_after(m, -1), month_after(m, 1), m)))
    its.append(mcq(fig(calpage_svg("March")) + "Which month comes just <b>after March</b>?", month_after("March"),
                   ["February", "May", "June"],
                   "Say the months in order: February, March, <b>April</b>, May."))
    its.append(mcq(fig(calpage_svg("June")) + "Which month comes just <b>before June</b>?", month_after("June", -1),
                   ["July", "April", "March"],
                   "Say the months in order: April, <b>May</b>, June, July."))
    its.append(mcq(fig(calpage_svg("December")) + "Which month comes just <b>after December</b>?", month_after("December"),
                   ["November", "February", "October"],
                   "December is the last month. Then a new year starts with <b>January</b>."))
    its.append(mcq(fig(seasons_svg()) + "How many <b>seasons</b> are in a year?", "4", ["12", "3", "7"],
                   "Summer, autumn, winter and spring: <b>4 seasons</b>. (12 is the number of months.)"))
    its.append(mcq(fig(seasons_svg(miss_season="winter")) + "Which season is missing?", "winter",
                   ["summer", "spring", "autumn"],
                   "In Australia the seasons go summer, autumn, <b>winter</b>, spring. "
                   "June, July and August are winter."))
    its.append(mcq(fig(pic_svg("sun", "a hot sun")) + "In Australia, which season has the <b>hottest</b> days?", "summer",
                   ["winter", "autumn", "spring"],
                   "<b>Summer</b> is the hottest season. In Australia it is December, January and February."))
    its.append(season_q("January", None, "In Australia, which season is <b>January</b>?"))
    its.append(season_q("July", "rain", "In Australia, which season is <b>July</b>?"))
    its.append(season_q("December", None, "Christmas Day is in December. In Australia, which season is it?"))
    its.append(season_q("September", "flower", "Lots of flowers open in September. In Australia, which season is it?"))
    its.append(mcq(fig(pic_svg("leaf", "a falling leaf")) + "Which months are <b>autumn</b> in Australia?",
                   "March, April, May",
                   ["September, October, November", "June, July, August", "December, January, February"],
                   "In Australia, autumn is <b>March, April and May</b>. "
                   "(September, October and November is autumn in the north of the world, not here.)"))
    its.append(mcq(fig(pic_svg("rain", "a rain cloud")) + "Which months are <b>winter</b> in Australia?",
                   "June, July, August",
                   ["December, January, February", "March, April, May", "September, October, November"],
                   "In Australia, winter is <b>June, July and August</b>. "
                   "(December, January and February is winter in the north of the world. Here it is summer.)"))
    its.append(mcq(fig(seasons_svg()) + "Which season comes just <b>after winter</b>?", season_after("winter"),
                   ["autumn", "summer", "July"],
                   "Summer, autumn, winter, <b>spring</b>. Spring comes after winter. (Autumn comes before winter.)"))
    its.append(mcq(fig(seasons_svg()) + "Which season comes just <b>after summer</b>?", season_after("summer"),
                   ["spring", "winter", "January"],
                   "Summer, <b>autumn</b>, winter, spring. Autumn comes after summer. (Spring comes before summer.)"))
    n, he, his = P.next()
    its.append(season_q("July", "cake", "%s’s birthday is in July. In Australia, which season is it?" % n))
    its.append(season_q("February", "school",
                        "School starts again in February after the long holidays. In Australia, which season is February?"))
    assert len(its) == 20, len(its)
    return {"title": "Months and seasons in Australia", "items": its}


# ============================================================ set 4: which takes longer?
def longer_q(a, b, ia, ib):
    """Which is longer: a or b? (a, b are durations like '1 hour')."""
    ans = a if dur(a) > dur(b) else b
    other = b if ans == a else a
    e = {("1 hour", "1 minute"): "In 1 minute the long hand moves 1 small step. In 1 hour it goes all the way round. ",
         ("1 week", "1 day"): "1 week is 7 days. ",
         ("1 month", "1 week"): "1 month is about 4 weeks. ",
         ("1 year", "1 month"): "1 year is 12 months. "}[(ans, other)]
    return mcq(fig(pair_svg((ia, a), (ib, b))) + "Which is <b>longer</b>?", ans,
               [other, "they are the same", "you can’t tell"],
               e + "So <b>%s</b> is longer than %s." % (ans, other))


def set_longer(rnd, P):
    its = []
    its.append(longer_q("1 minute", "1 hour", "minute", "hour"))
    its.append(longer_q("1 week", "1 day", "week", "day"))
    its.append(longer_q("1 week", "1 month", "week", "month"))
    its.append(longer_q("1 year", "1 month", "year", "month"))
    units = ["1 day", "1 week", "1 month", "1 year"]
    assert min(units, key=dur) == "1 day"
    its.append(mcq(fig(cards_svg([("year", "1 year"), ("day", "1 day"), ("month", "1 month"), ("week", "1 week")],
                                 arrows=False, bw=100, gap=14)) + "Which is the <b>shortest</b>?", "1 day",
                   ["1 week", "1 month", "1 year"],
                   "A week is 7 days. A month is about 4 weeks. A year is 12 months. So <b>1 day</b> is the shortest."))
    order = sorted(["hour", "minute", "day"], key=lambda u: MIN[u])
    its.append(mcq(fig(cards_svg([("day", "1 day"), ("minute", "1 minute"), ("hour", "1 hour")], arrows=False, bw=100, gap=14)) +
                   "Which order goes from <b>shortest</b> to <b>longest</b>?", ", ".join(order),
                   ["hour, minute, day", "day, hour, minute", "minute, day, hour"],
                   "A minute is very short. An hour is longer. A day has 24 hours. So: <b>minute, hour, day</b>."))
    for a, b, ans, other, e in [
            (("bed", "a night’s sleep"), ("bowl", "eating breakfast"), "a night’s sleep", "eating breakfast",
             "Breakfast takes a few minutes. A night’s sleep takes many hours."),
            (("toothbrush", "brushing teeth"), ("school", "a school day"), "a school day", "brushing teeth",
             "Brushing teeth takes about 2 minutes. A school day takes about 6 hours."),
            (("lunchbox", "recess"), ("school", "a school day"), "a school day", "recess",
             "Recess is a short break, about 20 to 30 minutes. A whole school day is about 6 hours."),
            (("sun", "summer holidays"), ("week", "a weekend"), "summer holidays", "a weekend",
             "A weekend is 2 days. Summer holidays are about 6 weeks.")]:
        its.append(mcq(fig(pair_svg(a, b)) + "Which takes <b>longer</b>?", ans,
                       [other, "they are the same", "you can’t tell"],
                       e + " So <b>%s</b> %s longer." % (ans, "take" if ans.endswith("holidays") else "takes")))
    for ic, lead, ans, wrong, e in [
            ("tap", "About how long does it take to <b>wash your hands</b>?", "about 1 minute",
             ["about 1 hour", "about 1 day", "about 1 week"],
             "Wet, soap, rub, rinse, dry. It is quick: <b>about 1 minute</b>."),
            ("toothbrush", "About how long should you <b>brush your teeth</b>?", "about 2 minutes",
             ["about 2 hours", "about 2 days", "about 2 weeks"],
             "Dentists say to brush for <b>about 2 minutes</b>. 2 hours would be far too long."),
            ("school", "About how long is a <b>school day</b>?", "about 6 hours",
             ["about 6 minutes", "about 6 days", "about 6 weeks"],
             "School starts in the morning and ends in the afternoon. That is <b>about 6 hours</b>."),
            ("sun", "About how long are the <b>summer holidays</b> in Australia?", "about 6 weeks",
             ["about 6 minutes", "about 6 hours", "about 6 years"],
             "The summer holidays go from December to the end of January. That is <b>about 6 weeks</b>."),
            ("flower", "A sunflower seed grows into a big flower. About how long does it take?", "about 3 months",
             ["about 3 minutes", "about 3 hours", "about 3 years"],
             "Plants grow slowly. A sunflower takes <b>about 3 months</b> to grow tall and flower.")]:
        its.append(mcq(fig(pic_svg(ic, ic)) + lead, ans, wrong, e))
    its.append(mcq(fig(cards_svg([(None, "a school year"), (None, "a school week"), (None, "a school day"),
                                  (None, "recess")], arrows=False, bw=112, gap=14)) +
                   "Which takes the <b>longest</b>?", "a school year",
                   ["a school week", "a school day", "recess"],
                   "A school week has 5 school days. A school year has many weeks. So <b>a school year</b> is the longest."))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert dur("10 hours") > dur("9 hours")
    its.append(mcq(fig(pair_svg(("bed", "10 hours"), ("bed", "9 hours"))) +
                   "%s sleeps for 10 hours. %s sleeps for 9 hours. Who sleeps <b>longer</b>?" % (n1, n2), n1,
                   [n2, "they are the same", "you can’t tell"],
                   "Both are in hours. 10 is more than 9. So <b>%s</b> sleeps longer." % n1))
    assert dur("3 hours") > dur("1 hour")
    its.append(mcq(fig(pair_svg(("hour", "3 hours"), ("hour", "1 hour"))) + "A cricket match lasts 3 hours. A netball game lasts 1 hour. Which is <b>longer</b>?",
                   "the cricket match", ["the netball game", "they are the same", "you can’t tell"],
                   "Both are in hours. 3 hours is more than 1 hour. So <b>the cricket match</b> is longer."))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert dur("1 hour") > dur("20 minutes")
    its.append(mcq(fig(pair_svg(("book", "1 hour"), ("book", "20 minutes"))) +
                   "%s reads for 1 hour. %s reads for 20 minutes. Who reads <b>longer</b>?" % (n1, n2), n1,
                   [n2, "they are the same", "you can’t tell"],
                   "Look at the words, not only the numbers. 1 hour is 60 minutes. 60 minutes is more than 20 minutes. "
                   "So <b>%s</b> reads longer. (20 is bigger than 1, but minutes are short.)" % n1))
    n1, he1, _ = P.next()
    n2, he2, _ = P.next()
    assert dur("1 week") > dur("2 days")
    its.append(mcq(fig(pair_svg(("day", "2 days"), ("week", "1 week"))) +
                   "%s stays at the beach for 2 days. %s stays for 1 week. Who stays <b>longer</b>?" % (n1, n2), n2,
                   [n1, "they are the same", "you can’t tell"],
                   "1 week is 7 days. 7 days is more than 2 days. So <b>%s</b> stays longer. "
                   "(2 is bigger than 1, but a week is longer than a day.)" % n2))
    assert len(its) == 20, len(its)
    return {"title": "Which takes longer? Minutes, hours, days, weeks, months and years", "items": its}


# ============================================================ set 5: o’clock and half past in the day
def set_clocks(rnd, P):
    its = []
    acts = [("{n} wakes up in the morning. What time is it?", 6, 30),
            ("{n} eats breakfast. What time is it?", 7, 0),
            ("School starts in the morning. What time is it?", 9, 0),
            ("It is recess. What time is it?", 11, 0),
            ("It is lunch time at school. What time is it?", 12, 30),
            ("School finishes. It is home time. What time is it?", 3, 0),
            ("{n} goes to footy training after school. What time is it?", 4, 30),
            ("{n} eats dinner. What time is it?", 6, 0),
            ("{n} goes to bed at night. What time is it?", 7, 30),
            ("{n} has a swimming lesson on Saturday morning. What time is it?", 10, 0)]
    for q, h, m in acts:
        n, he, his = P.next()
        t = q.format(n=n)
        its.append(read_hour(h, rnd, t) if m == 0 else read_half(h, rnd, t))
    n, he, his = P.next()
    its.append(clocks_item("%s catches the school bus at <b>half past 8</b>. Which clock shows half past 8?" % n, 8, 30, 2, rnd))
    its.append(clocks_item("The swimming carnival ends at <b>2 o’clock</b>. Which clock shows 2 o’clock?", 2, 0, 0, rnd))
    its.append(clocks_item("The sausage sizzle starts at <b>half past 11</b>. Which clock shows half past 11?", 11, 30, 3, rnd))
    its.append(mcq(fig(clock_svg(3, 0)) + "It is 3 o’clock. What time will it be in <b>1 hour</b>?", oc(4),
                   ["2 o’clock", "half past 3", "5 o’clock"],
                   "In 1 hour the short hand moves on to the next number. 3 o’clock → <b>4 o’clock</b>. "
                   "(2 o’clock was 1 hour ago.)"))
    its.append(mcq(fig(clock_svg(9, 0)) + "It is 9 o’clock. What time will it be in <b>half an hour</b>?", hp(9),
                   ["half past 10", "10 o’clock", "half past 8"],
                   "In half an hour the long hand goes from the 12 down to the 6. 9 o’clock → <b>half past 9</b>. "
                   "(10 o’clock is 1 hour later.)"))
    its.append(mcq(fig(clock_svg(4, 30)) + "It is half past 4. What time will it be in <b>half an hour</b>?", oc(5),
                   ["half past 5", "4 o’clock", "6 o’clock"],
                   "In half an hour the long hand goes from the 6 up to the 12. A new hour starts: <b>5 o’clock</b>. "
                   "(Half past 5 is 1 hour later.)"))
    n, he, his = P.next()
    its.append(mcq(fig(clock_svg(10, 30)) +
                   "The library opens at 11 o’clock. %s gets there at half past 10. Is %s early or late?" % (n, he),
                   "early", ["late", "on time", "a day late"],
                   "Half past 10 comes <b>before</b> 11 o’clock. So %s is <b>early</b>." % n))
    n, he, his = P.next()
    its.append(mcq(fig(clock_svg(9, 0)) +
                   "The school bus comes at half past 8. %s gets to the bus stop at 9 o’clock. Is %s early or late?"
                   % (n, he), "late", ["early", "on time", "a day early"],
                   "9 o’clock comes <b>after</b> half past 8. The bus has gone. So %s is <b>late</b>." % n))
    n, he, his = P.next()
    its.append(mcq(fig(clocks2_svg((2, 0), (4, 0))) +
                   "A movie starts at 2 o’clock. It ends at 4 o’clock. How long is the movie?", "2 hours",
                   ["4 hours", "6 hours", "1 hour"],
                   "Count the hours: 2 o’clock to 3 o’clock is 1, 3 o’clock to 4 o’clock is 2. It is <b>2 hours</b>. "
                   "(4 is the end time, not how long.)"))
    n, he, his = P.next()
    its.append(mcq(fig(clocks2_svg((6, 0), (6, 30))) +
                   "%s reads from 6 o’clock to half past 6. How long does %s read?" % (n, he), "half an hour",
                   ["1 hour", "6 minutes", "6 hours"],
                   "The long hand goes from the 12 to the 6. That is half of the way round: <b>half an hour</b>."))
    assert len(its) == 20, len(its)
    return {"title": "O’clock and half past in your day", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Morning, afternoon and night</h2>"
        "<p>Every day goes in the same order: <b>morning</b>, <b>afternoon</b>, <b>night</b>. "
        "We eat breakfast in the morning. School finishes in the afternoon. We sleep at night.</p>"
        "<figure class='sn-fig'>" + cards_svg([("sunrise", "morning"), ("sun", "afternoon"), ("moon", "night")]) +
        "<figcaption>The sun comes up in the morning. It is high in the afternoon. The moon is out at night.</figcaption></figure>"
        "<p>Use <b>first</b>, <b>next</b>, <b>then</b> and <b>last</b> to tell things in order. "
        "<b>Before</b> means earlier. <b>After</b> means later.</p>"
        + ex("Example 1", "Leo has a bath. Then he reads a story. What does he do first?",
             "“Then” tells us the story comes later. The bath comes first.", "has a bath")
        + "<h2>Days of the week</h2>"
        "<p>There are <b>7 days</b> in a week. Monday to Friday are school days. Saturday and Sunday are the weekend.</p>"
        "<figure class='sn-fig'>" + week_svg(today="Wednesday") +
        "<figcaption>Today is Wednesday. Yesterday was Tuesday. Tomorrow is Thursday.</figcaption></figure>"
        + table(["Word", "Means"], [
            ["yesterday", "the day <b>before</b> today"],
            ["today", "this day"],
            ["tomorrow", "the day <b>after</b> today"],
        ])
        + ex("Example 2", "Today is Sunday. What day is tomorrow?",
             "Tomorrow is the day after today. After Sunday a new week starts.", "Monday")
        + "<h2>Months and seasons in Australia</h2>"
        "<p>There are <b>12 months</b> in a year, from January to December. "
        "There are <b>4 seasons</b>. Each season has 3 months.</p>"
        "<figure class='sn-fig'>" + seasons_svg() +
        "<figcaption>In Australia, summer is December, January and February. Winter is June, July and August.</figcaption></figure>"
        + table(["Season", "Months in Australia"], [
            ["summer", "December, January, February"],
            ["autumn", "March, April, May"],
            ["winter", "June, July, August"],
            ["spring", "September, October, November"],
        ])
        + "<p>Christmas is in summer in Australia. In England and the USA it is winter at Christmas, "
        "because their seasons are the other way round.</p>"
        "<h2>Which takes longer?</h2>"
        "<p>A <b>minute</b> is short. An <b>hour</b> is 60 minutes. A <b>day</b> is 24 hours. "
        "A <b>week</b> is 7 days. A <b>month</b> is about 4 weeks. A <b>year</b> is 12 months.</p>"
        + ex("Example 3", "Mia stays for 2 days. Kai stays for 1 week. Who stays longer?",
             "1 week is 7 days. 7 days is more than 2 days.", "Kai")
        + "<h2>O’clock and half past</h2>"
        "<p>On an analog clock, the <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "Long hand on the 12: it is <b>o’clock</b>. Long hand on the 6: it is <b>half past</b>.</p>"
        "<figure class='sn-fig'>" + clock_svg(9, 0, size=200) +
        "<figcaption>The long hand is on the 12. The short hand is on the 9. School starts at 9 o’clock.</figcaption></figure>"
        "<figure class='sn-fig'>" + clock_svg(12, 30, size=200) +
        "<figcaption>The long hand is on the 6. The short hand has gone past the 12. It is half past 12, lunch time.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Saying July is summer and Christmas is in winter", "In Australia, summer is December to February. July is winter"],
            ["Mixing up yesterday and tomorrow", "Yesterday is before today. Tomorrow is after today"],
            ["Thinking 2 days is longer than 1 week because 2 is bigger", "Look at the word too. 1 week is 7 days"],
            ["Reading half past 3 as half past 4", "Use the number the short hand has gone past: half past 3"],
            ["Mixing up the two hands", "Short hand = hour. Long hand on the 12 = o’clock, on the 6 = half past"],
        ])
    )


FAQ = [
    {"q": "What time and calendar skills does Year 1 learn in the Australian Curriculum?",
     "a": "Year 1 students describe the duration and order of events using years, months, weeks, days and hours (AC9M1M03). "
          "They use words like morning, yesterday and tomorrow, name the days and months, and read o’clock and half past times."},
    {"q": "What are the seasons in Australia?",
     "a": "Summer is December, January and February. Autumn is March to May, winter is June to August and spring is September to November."},
    {"q": "Why is Christmas in summer in Australia?",
     "a": "Australia is in the Southern Hemisphere, so its seasons are the opposite of England and the USA. "
          "December is the start of summer here."},
    {"q": "How can I help my Year 1 child learn the days of the week and months?",
     "a": "Say them in order each day and talk about yesterday, today and tomorrow, like “Today is Monday, so tomorrow is Tuesday.” "
          "Mark birthdays, school holidays and sport days on a family calendar."},
]


# ============================================================ checks
def check(sets):
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"][:80]
            key = re.sub(r"<[^>]+>", " ", it["q"]) + "|" + it["q"][-400:] + "|".join(sorted(it["c"]))
            assert key not in seen, key
            seen.add(key)
            for t in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in t and '"' not in t, t
                plain = re.sub(r"<[^>]+>", " ", t)
                assert not re.search(r"\b1 (minutes|hours|days|weeks|months|years)\b", plain), t
                for w in ["math ", "color", "center", "meter", "gray", "favorite", "grade", "a.m.", "p.m.", "pupil", "evening", " tea"]:
                    assert w not in plain.lower(), (w, t)
            for x in it["c"]:
                assert "'" not in x
            r = it["c"][it["a"]]
            if "o’clock" in r or "half past" in r:
                assert re.fullmatch(r"(\d{1,2} o’clock|half past \d{1,2})", r), r
            # a single clock picture shows the time in the question when the answer is a time
            m = re.search(r"aria-label='clock showing ([^']+)'", it["q"])
            if m and "What time is it?" in it["q"]:
                assert m.group(1) == r, (m.group(1), r)
            assert "aria-label='clock showing 12 o’clock'" not in it["q"]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(1809)
    P = People(rnd)
    sets = [set_day(rnd, P), set_week(rnd, P), set_months(rnd, P), set_longer(rnd, P), set_clocks(rnd, P)]
    balance(sets, rnd)
    check(sets)
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "days-weeks-months-and-time", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Days, Weeks, Months and Time",
        "seo_title": "Year 1 Time Worksheets: Days of the Week, Months, Seasons and O’clock (Free, Australian Curriculum)",
        "short_title": "Days, weeks, months and time",
        "domain": "Measurement",
        "standard_code": "AC9M1M03",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Describe the duration and sequence of events using years, months, weeks, days and hours",
        "meta_desc": "Free Year 1 maths worksheets on time, matched to the Australian Curriculum (AC9M1M03): morning, "
                     "afternoon and night, days of the week, yesterday and tomorrow, months and Australian seasons, "
                     "which takes longer, and o’clock and half past. 100 picture questions with an answer key.",
        "key_big": "Yesterday is before today. Tomorrow is after today.",
        "key_sub": "7 days in a week, 12 months in a year. In Australia, summer is December to February and winter is "
                   "June to August. Long hand on the 12: o’clock. Long hand on the 6: half past.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four clocks labelled A to D|cards|two cards|two clocks|three sky pictures|"
                         "the days of the week|the months of the year|seasons in Australia")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
