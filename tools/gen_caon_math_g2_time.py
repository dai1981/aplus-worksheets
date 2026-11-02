# -*- coding: utf-8 -*-
"""
CA Grade 2 Math: Time (Ontario Mathematics Curriculum 2020, Grade 2: E2.4)
  python3 tools/gen_caon_math_g2_time.py
Units of time (seconds, minutes, hours and non-standard units such as sand timers and claps) to describe how long
events last; reading clocks to the hour and half hour; how long from start to end in hours and half hours.
Every analog clock is drawn from the time itself (the short hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real student mistakes:
hours chosen for short events (same number, wrong unit), half an hour taken as 50 minutes, an hour taken as 100
minutes, the hands swapped, half past 3 read as half past 4, the 6 read as 6 minutes, counting the numbers
instead of the jumps, adding the hours to the minutes (3:00 + 2 hours = 3:02), the bigger number taken as the
longer time whatever the unit.
Canadian English; times written 3:30 p.m. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#9aa3a0"
BLUE = "#3a7bd5"
SAND = "#e0b04a"
FONT = "Arial, Helvetica, sans-serif"
PEOPLE = [("Liam", "he"), ("Olivia", "she"), ("Noah", "he"), ("Emma", "she"), ("Aiden", "he"), ("Maya", "she"),
          ("Lucas", "he"), ("Zoe", "she"), ("Owen", "he"), ("Amira", "she"), ("Arjun", "he"), ("Mei", "she"),
          ("Ethan", "he"), ("Chloe", "she"), ("Jayden", "he"), ("Priya", "she"), ("Benjamin", "he"), ("Leah", "she"),
          ("Mateo", "he"), ("Hana", "she"), ("Nathan", "he"), ("Ava", "she"), ("Kai", "he"), ("Sofia", "she")]


# ------------------------------------------------------------ time formats
def h12(h):
    return (h - 1) % 12 + 1


def dig(h, m):
    return "%d:%02d" % (h12(h), m)


def tm12(h24, m):
    h24 %= 24
    if h24 == 12 and m == 0:
        return "12:00 noon"
    return "%d:%02d %s" % (h12(h24), m, "a.m." if h24 < 12 else "p.m.")


def words(h, m):
    assert m in (0, 30)
    return ("%d o’clock" if m == 0 else "half past %d") % h12(h)


def dur(n):
    """30 -> 30 minutes, 60 -> 1 hour, 90 -> 1 hour 30 minutes"""
    assert n > 0
    hh, mm = divmod(n, 60)
    parts = []
    if hh:
        parts.append("%d hour%s" % (hh, "" if hh == 1 else "s"))
    if mm:
        parts.append("%d minute%s" % (mm, "" if mm == 1 else "s"))
    return " ".join(parts)


def dur_value(s):
    v = 0
    for n, unit in re.findall(r"(\d+) (hour|minute|second)", s):
        v += int(n) * {"hour": 3600, "minute": 60, "second": 1}[unit]
    return v or s


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def tidy(t):
    return t.replace("m.</b>.", "m.</b>").replace("a.m..", "a.m.").replace("p.m..", "p.m.")


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, key=None):
    key = key or (lambda x: x)
    seen = {key(correct)}
    pick = []
    for c in cands:
        if not c or key(c) in seen:
            continue
        seen.add(key(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": tidy(q), "c": [correct] + pick, "a": 0, "e": tidy(e)}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


# ------------------------------------------------------------ clocks
def clock_body(h, m, cx, cy, R):
    """Analog clock face. The short hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 25, (h, m)
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (12 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.82 * math.cos(am), cy + R * 0.82 * math.sin(am), RED, 4.5 * k))
    fs = max(19 * k, 15)
    rn = R - 13 * k - fs * 0.75
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, max(3.5 * k, 2.5)))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200):
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6), "analog clock")


def clocks4_svg(times):
    """2 x 2 grid of clocks labelled A to D (a square picture)."""
    CELL = 150
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for i, (h, m) in enumerate(times):
        x0, y0 = (i % 2) * CELL, (i // 2) * CELL
        el.append(clock_body(h, m, x0 + 80, y0 + 77, 66))
        el.append("<text x='%d' y='%d' font-size='20' font-weight='700' fill='%s'>%s</text>" % (x0 + 6, y0 + 22, GREEN, "ABCD"[i]))
    return svg_wrap(W, H, "".join(el), "four analog clocks")


def start_end_svg(h1, m1, h2, m2):
    S, gap, top = 170, 20, 30
    el = []
    for i, (h, m, lab) in enumerate([(h1, m1, "Start"), (h2, m2, "End")]):
        x = i * (S + gap)
        el.append("<text x='%.1f' y='22' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                  % (x + S / 2.0, GREEN, lab))
        el.append(clock_body(h, m, x + S / 2.0, top + S / 2.0, S / 2.0 - 6))
    return svg_wrap(2 * S + gap, S + top, "".join(el), "start and end clocks")


def timer_svg(mm, ss):
    """Digital timer: minutes : seconds, labelled underneath."""
    W, H = 200, 108
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='12' width='%d' height='58' rx='6' fill='#eef5f0'/>" % (W - 32),
         "<text x='%d' y='56' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%d:%02d</text>" % (W / 2, LINE, mm, ss),
         "<text x='%d' y='92' font-size='15' fill='%s' text-anchor='middle'>min</text>" % (W / 2 - 30 - 12 * (mm >= 10), LINE),
         "<text x='%d' y='92' font-size='15' fill='%s' text-anchor='middle'>sec</text>" % (W / 2 + 36, LINE)]
    return svg_wrap(W, H, "".join(s), "timer")


def stopwatch_svg(sec, size=200):
    """Stopwatch dial: 60 seconds once around, numbers 5 to 60, one red hand."""
    assert 0 < sec < 60
    top = 22
    R = size / 2.0 - 6
    cx, cy = size / 2.0, top + size / 2.0
    k = R / 94.0
    s = ["<rect x='%.1f' y='2' width='24' height='%d' rx='4' fill='%s'/>" % (cx - 12, top + 4, GREEN),
         "<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (12 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    a = math.radians(sec * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.56 * math.cos(a), cy + R * 0.56 * math.sin(a), RED, 4.5 * k))
    fs = max(19 * k, 15)
    rn = R - 13 * k - fs * 0.85
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        b = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(b), cy + rn * math.sin(b) + fs * 0.36, 5 * n))
    s.append("</g><circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return svg_wrap(size, size + top, "".join(s), "stopwatch")


def steps(t1, t2):
    """Jumps of 1 hour while they fit, then half an hour."""
    pts = [t1]
    while pts[-1] + 60 <= t2:
        pts.append(pts[-1] + 60)
    while pts[-1] < t2:
        pts.append(pts[-1] + 30)
    assert pts[-1] == t2
    return pts


def timeline_svg(h1, m1, h2, m2):
    """Start -> end in jumps of 1 hour and half an hour, the jumps labelled."""
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    pts = steps(t1, t2)
    W = 120 + 105 * (len(pts) - 1)
    L, R, Y = 50, W - 50, 74
    tot = float(sum(2 if b - a == 60 else 1.2 for a, b in zip(pts, pts[1:])))
    xs = [L]
    for a, b in zip(pts, pts[1:]):
        xs.append(xs[-1] + (R - L) * (2 if b - a == 60 else 1.2) / tot)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t, x in zip(pts, xs):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, Y - 10, x, Y + 10, LINE))
        s.append("<text x='%.1f' y='%d' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x, Y + 32, LINE, dig(t // 60, t % 60)))
    for (a, b), x1, x2 in zip(zip(pts, pts[1:]), xs, xs[1:]):
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 2, Y - 12, (x1 + x2) / 2, Y - 52, x2 - 2, Y - 12, RED))
        s.append("<text x='%.1f' y='%d' font-size='15' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % ((x1 + x2) / 2, Y - 40, RED, "1 hour" if b - a == 60 else "30 min"))
    return svg_wrap(W, 116, "".join(s), "time line")


# ------------------------------------------------------------ pictures (100 x 80 box each)
def ic_toothbrush(x, y):
    s = ["<rect x='%d' y='%d' width='62' height='10' rx='5' fill='%s'/>" % (x + 8, y + 46, BLUE),
         "<rect x='%d' y='%d' width='26' height='12' rx='4' fill='%s'/>" % (x + 66, y + 45, BLUE)]
    for i in range(6):
        s.append("<rect x='%d' y='%d' width='3' height='16' fill='%s'/>" % (x + 68 + 4 * i, y + 29, LINE))
    s.append("<rect x='%d' y='%d' width='26' height='6' rx='3' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x + 66, y + 24, GRAY))
    return "".join(s)


def ic_bed(x, y):
    return ("<rect x='%d' y='%d' width='8' height='44' fill='%s'/>" % (x + 6, y + 28, GREEN) +
            "<rect x='%d' y='%d' width='82' height='12' fill='%s'/>" % (x + 12, y + 52, GREEN) +
            "<rect x='%d' y='%d' width='80' height='10' rx='3' fill='#fff' stroke='%s' stroke-width='2'/>" % (x + 14, y + 42, LINE) +
            "<ellipse cx='%d' cy='%d' rx='12' ry='7' fill='#fff' stroke='%s' stroke-width='2'/>" % (x + 28, y + 37, LINE) +
            "<rect x='%d' y='%d' width='52' height='14' rx='4' fill='%s'/>" % (x + 40, y + 34, BLUE) +
            "<rect x='%d' y='%d' width='6' height='10' fill='%s'/><rect x='%d' y='%d' width='6' height='10' fill='%s'/>"
            % (x + 12, y + 64, GREEN, x + 86, y + 64, GREEN) +
            "<circle cx='%d' cy='%d' r='12' fill='%s'/><circle cx='%d' cy='%d' r='11' fill='#fff'/>"
            % (x + 78, y + 14, SAND, x + 84, y + 10))


def ic_cup(x, y):
    return ("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#d8ecfb' stroke='%s' stroke-width='2.5'/>"
            % (x + 30, y + 14, x + 70, y + 14, x + 65, y + 74, x + 35, y + 74, LINE) +
            "<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s'/>"
            % (x + 33, y + 32, x + 67, y + 32, x + 65, y + 72, x + 35, y + 72, BLUE))


def ic_car(x, y):
    return ("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s'/>" % (x + 26, y + 40, x + 36, y + 22, x + 66, y + 22, x + 78, y + 40, RED) +
            "<rect x='%d' y='%d' width='88' height='24' rx='8' fill='%s'/>" % (x + 6, y + 38, RED) +
            "<rect x='%d' y='%d' width='14' height='12' fill='#fff'/><rect x='%d' y='%d' width='14' height='12' fill='#fff'/>"
            % (x + 38, y + 26, x + 56, y + 26) +
            "<circle cx='%d' cy='%d' r='9' fill='%s'/><circle cx='%d' cy='%d' r='9' fill='%s'/>"
            % (x + 26, y + 64, LINE, x + 74, y + 64, LINE))


def ic_shoe(x, y):
    return ("<path d='M%d %d L%d %d Q%d %d %d %d L%d %d Q%d %d %d %d Z' fill='%s'/>"
            % (x + 12, y + 30, x + 40, y + 30, x + 48, y + 46, x + 78, y + 50, x + 90, y + 56,
               x + 92, y + 66, x + 12, y + 66, BLUE) +
            "<rect x='%d' y='%d' width='82' height='6' fill='%s'/>" % (x + 10, y + 64, LINE) +
            "<path d='M%d %d L%d %d M%d %d L%d %d M%d %d L%d %d' stroke='#fff' stroke-width='2.5'/>"
            % (x + 36, y + 38, x + 46, y + 44, x + 40, y + 46, x + 52, y + 50, x + 30, y + 44, x + 40, y + 50) +
            "<path d='M%d %d Q%d %d %d %d M%d %d Q%d %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
            % (x + 34, y + 36, x + 24, y + 22, x + 36, y + 24, x + 36, y + 36, x + 50, y + 22, x + 44, y + 34, LINE))


def ic_hockey(x, y):
    return ("<path d='M%d %d L%d %d L%d %d' fill='none' stroke='%s' stroke-width='7' stroke-linecap='round' "
            "stroke-linejoin='round'/>" % (x + 28, y + 8, x + 58, y + 62, x + 86, y + 62, GREEN) +
            "<ellipse cx='%d' cy='%d' rx='13' ry='5' fill='%s'/>" % (x + 28, y + 66, LINE) +
            "<rect x='%d' y='%d' width='26' height='5' fill='%s'/>" % (x + 15, y + 66, LINE) +
            "<ellipse cx='%d' cy='%d' rx='13' ry='5' fill='%s'/>" % (x + 28, y + 71, LINE))


def ic_school(x, y):
    return ("<rect x='%d' y='%d' width='70' height='40' fill='#f3e3c3' stroke='%s' stroke-width='2'/>" % (x + 15, y + 34, LINE) +
            "<path d='M%d %d L%d %d L%d %d Z' fill='%s'/>" % (x + 10, y + 36, x + 50, y + 14, x + 90, y + 36, RED) +
            "<rect x='%d' y='%d' width='14' height='20' fill='%s'/>" % (x + 43, y + 54, GREEN) +
            "<rect x='%d' y='%d' width='12' height='10' fill='#d8ecfb' stroke='%s'/><rect x='%d' y='%d' width='12' height='10' "
            "fill='#d8ecfb' stroke='%s'/>" % (x + 22, y + 44, LINE, x + 66, y + 44, LINE) +
            "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x + 50, y + 15, x + 50, y + 1, LINE) +
            "<rect x='%d' y='%d' width='16' height='9' fill='%s'/>" % (x + 51, y + 1, RED))


def ic_book(x, y):
    return ("<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#fff' stroke='%s' stroke-width='2.5'/>"
            % (x + 50, y + 22, x + 12, y + 14, x + 12, y + 64, x + 50, y + 72, GREEN) +
            "<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='#fff' stroke='%s' stroke-width='2.5'/>"
            % (x + 50, y + 22, x + 88, y + 14, x + 88, y + 64, x + 50, y + 72, GREEN) +
            "".join("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x + 18, y + 28 + 9 * i, x + 44, y + 33 + 9 * i, GRAY)
                    for i in range(4)) +
            "".join("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x + 56, y + 33 + 9 * i, x + 82, y + 28 + 9 * i, GRAY)
                    for i in range(4)))


ICONS = {"toothbrush": ic_toothbrush, "bed": ic_bed, "cup": ic_cup, "car": ic_car, "shoe": ic_shoe,
         "hockey": ic_hockey, "school": ic_school, "book": ic_book}


def icon_svg(name, label):
    return svg_wrap(100, 80, ICONS[name](0, 0), label)


def pair_svg(a, la, b, lb):
    """Two pictures side by side with a short caption under each."""
    el = [ICONS[a](10, 0), ICONS[b](150, 0)]
    for x, t in [(60, la), (200, lb)]:
        el.append("<text x='%d' y='104' font-size='17' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (x, LINE, t))
    return svg_wrap(260, 112, "".join(el), "two pictures")


def sand_timer(x, y, s=1.0):
    """Sand timer, top-left at (x, y): 30 x 50 at s = 1."""
    w, h = 30 * s, 50 * s
    return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>" % (x, y, w, 5 * s, GREEN) +
            "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='2' fill='%s'/>" % (x, y + h - 5 * s, w, 5 * s, GREEN) +
            "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#fff' stroke='%s' stroke-width='2'/>"
            % (x + 3 * s, y + 5 * s, x + w - 3 * s, y + 5 * s, x + w / 2 + 2 * s, y + h / 2, x + w - 3 * s, y + h - 5 * s,
               x + 3 * s, y + h - 5 * s, x + w / 2 - 2 * s, y + h / 2, LINE) +
            "<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>"
            % (x + 6 * s, y + h - 6 * s, x + w - 6 * s, y + h - 6 * s, x + w / 2, y + h - 18 * s, SAND))


def sand_rows_svg(rows, scales=None):
    """One row of sand timers per child: name, then one timer for each time it ran out."""
    scales = scales or [1.0] * len(rows)
    el = []
    y = 4
    for (name, n), s in zip(rows, scales):
        hh = 50 * s
        el.append("<text x='4' y='%.1f' font-size='18' font-weight='700' fill='%s'>%s</text>" % (y + hh / 2 + 6, LINE, name))
        for i in range(n):
            el.append(sand_timer(96 + i * (30 * s + 10), y, s))
        y += hh + 12
    W = max(96 + n * (30 * s + 10) for (name, n), s in zip(rows, scales)) + 4
    return svg_wrap(int(W), int(y), "".join(el), "sand timers")


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ============================================================ set 1: seconds, minutes or hours
UNITS = ["seconds", "minutes", "hours", "days"]
UNIT_WHY = {
    "seconds": "It is over very fast, so we use <b>seconds</b>.",
    "minutes": "It takes longer than a few seconds, but much less than an hour. We use <b>minutes</b>.",
    "hours": "It takes a long time, more than an hour. We use <b>hours</b>.",
    "days": "It lasts for more than one whole day. We use <b>days</b>.",
}


def set_units(rnd):
    which = [  # (event, unit, picture)
        ("blink your eyes", "seconds", None),
        ("brush your teeth", "minutes", "toothbrush"),
        ("tie your shoes", "seconds", "shoe"),
        ("sleep at night", "hours", "bed"),
        ("recess lasts", "minutes", None),
        ("watch a hockey game at the arena", "hours", "hockey"),
        ("zip up your coat", "seconds", None),
        ("a school day lasts", "hours", "school"),
        ("eat your breakfast", "minutes", None),
        ("March Break lasts", "days", None),
    ]
    how = [  # (event, number, unit, picture, note)
        ("drink a cup of water", 10, "seconds", "cup", "A few big sips are quick."),
        ("read a picture book", 10, "minutes", "book", "You turn many pages, but it is much less than an hour."),
        ("clap your hands 3 times", 3, "seconds", None, "Clap, clap, clap: that is very quick."),
        ("drive from Toronto to Ottawa", 5, "hours", "car", "It is a long car ride, most of a day."),
        ("put on snow pants, boots and mitts", 5, "minutes", None, "It takes a little while, but not an hour."),
        ("jump up and down 5 times", 5, "seconds", None, "Five jumps are over very fast."),
        ("take a bath", 20, "minutes", None, "A bath is longer than a few seconds, but much less than a day."),
        ("go on a class field trip to the museum", 3, "hours", None, "There is a lot to see, and the bus ride takes time too."),
        ("bake a pan of cookies in the oven", 12, "minutes", None, "Cookies bake for a short time, not for hours."),
        ("have a family picnic at the lake", 2, "hours", None, "Eating, swimming and playing take a long time."),
    ]
    a_items, b_items = [], []
    for ev, u, pic in which:
        if ev.endswith(" lasts"):
            txt = "Which unit would you use to tell how long <b>%s</b>?" % ev
        else:
            txt = "Which unit would you use to tell how long it takes to <b>%s</b>?" % ev
        q = (fig(icon_svg(pic, ev)) if pic else "") + txt
        wrong = [x for x in UNITS if x != u]
        e = UNIT_WHY[u]
        if u == "seconds":
            e += " (Not hours: an hour is much too long for that.)"
        a_items.append(mcq(q, u, wrong, e))
    for ev, n, u, pic, note in how:
        right = "%d %s" % (n, u)
        wrong = ["%d %s" % (n, x) for x in UNITS if x != u]
        q = (fig(icon_svg(pic, ev)) if pic else "") + "About how long does it take to <b>%s</b>?" % ev
        e = "%s So it takes about <b>%s</b>." % (note, right)
        if u in ("seconds", "minutes"):
            e += " (Not %d hours: that is far too long.)" % n
        else:
            e += " (Not %d minutes: that is far too short.)" % n
        b_items.append(mcq(q, right, wrong, e))
    its = []
    for i in range(10):
        its.append(a_items[i])
        its.append(b_items[i])
    return {"title": "Seconds, minutes or hours?", "items": its}


# ============================================================ set 2: longer or shorter
def set_compare(rnd, people):
    its = []
    same, cant = "They take the same time.", "You cannot tell."
    its.append(mcq(fig(pair_svg("toothbrush", "brush teeth", "bed", "sleep")) + "Which takes <b>longer</b>?",
                   "sleeping at night", ["brushing your teeth", same, cant],
                   "Brushing your teeth takes about 2 minutes. Sleeping at night takes about 10 hours. "
                   "So <b>sleeping at night</b> takes longer."))
    its.append(mcq(fig(pair_svg("shoe", "tie shoes", "hockey", "hockey game")) + "Which takes <b>less</b> time?",
                   "tying your shoes", ["a hockey game", same, cant],
                   "Tying your shoes takes seconds. A hockey game takes hours. So <b>tying your shoes</b> takes less time."))
    its.append(mcq(fig(pair_svg("book", "read a book", "car", "drive to Ottawa")) + "Which takes <b>longer</b>?",
                   "driving from Toronto to Ottawa", ["reading a picture book", same, cant],
                   "Reading a picture book takes minutes. The drive from Toronto to Ottawa takes hours. "
                   "So <b>the drive</b> takes longer."))
    its.append(mcq("Which is <b>longer</b>: 1 minute or 1 hour?", "1 hour", ["1 minute", "They are the same.", cant],
                   "1 hour is 60 minutes. So <b>1 hour</b> is much longer than 1 minute."))
    its.append(mcq("Which is <b>shorter</b>: 1 second or 1 minute?", "1 second", ["1 minute", "They are the same.", cant],
                   "1 minute is 60 seconds. So <b>1 second</b> is shorter."))
    its.append(mcq("How many <b>minutes</b> are in 1 hour?", "60", ["100", "30", "12"],
                   "There are <b>60 minutes</b> in 1 hour. The long hand goes all the way around the clock once. "
                   "(Not 100: time does not count in hundreds. Not 12: there are 12 numbers on the clock, but each one is 5 minutes.)"))
    its.append(mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"],
                   "There are <b>60 seconds</b> in 1 minute. (Not 100: time does not count in hundreds.)"))
    its.append(mcq("How many minutes are in <b>half an hour</b>?", "30", ["50", "60", "6"],
                   "1 hour is 60 minutes. Half of 60 is <b>30</b>. (Not 50: an hour is not 100 minutes. "
                   "Not 6: at half past, the long hand points to the 6, but that is 30 minutes.)"))
    nm = next(people)
    its.append(mcq(fig(sand_rows_svg([("Mei", 3), ("Owen", 5)])) +
                   "Mei and Owen clean their desks. They use the same sand timer. Mei takes 3 sand timers. "
                   "Owen takes 5 sand timers. Who takes <b>longer</b>?", "Owen", ["Mei", "They take the same time.", cant],
                   "The sand timers are all the same size. 5 sand timers is more than 3. So <b>Owen</b> takes longer."))
    its.append(mcq("Liam claps while he zips up his coat. He claps <b>12</b> times. Ava claps <b>8</b> times while she zips "
                   "up her coat. They clap at the same speed. Who is <b>faster</b>?", "Ava",
                   ["Liam", "They take the same time.", cant],
                   "Fewer claps means less time. 8 claps is less than 12 claps. So <b>Ava</b> is faster. "
                   "(Liam has the bigger number, so he took longer.)"))
    its.append(mcq("Which is <b>longer</b>: half an hour or 40 minutes?", "40 minutes",
                   ["half an hour", "They are the same.", cant],
                   "Half an hour is 30 minutes. 40 minutes is more than 30 minutes. So <b>40 minutes</b> is longer. "
                   "(Half an hour is not 50 minutes.)"))
    its.append(mcq("Which is <b>longer</b>: 50 minutes or 1 hour?", "1 hour", ["50 minutes", "They are the same.", cant],
                   "1 hour is 60 minutes. 60 is more than 50. So <b>1 hour</b> is longer."))
    its.append(mcq("Put these in order from <b>shortest</b> to <b>longest</b>: a school day, blinking your eyes, recess.",
                   "blinking, recess, a school day",
                   ["recess, blinking, a school day", "a school day, recess, blinking", "blinking, a school day, recess"],
                   "Blinking takes about 1 second. Recess takes about 15 minutes. A school day takes about 6 hours. "
                   "So the order is <b>blinking, recess, a school day</b>."))
    its.append(mcq("Put these in order from <b>longest</b> to <b>shortest</b>: brushing your teeth, a car trip to the cottage, "
                   "a sneeze.", "car trip, brushing teeth, sneeze",
                   ["sneeze, brushing teeth, car trip", "brushing teeth, car trip, sneeze", "car trip, sneeze, brushing teeth"],
                   "A car trip to the cottage takes hours. Brushing your teeth takes about 2 minutes. A sneeze takes about 1 second. "
                   "So the order is <b>car trip, brushing teeth, sneeze</b>."))
    its.append(mcq(fig(sand_rows_svg([("Hana", 4), ("Jayden", 4)], [0.7, 1.3])) +
                   "Hana does a puzzle. She uses a <b>small</b> sand timer 4 times. Jayden does a puzzle. He uses a <b>big</b> sand "
                   "timer 4 times. The big timer takes longer to run out. Who takes <b>longer</b>?", "Jayden",
                   ["Hana", "They take the same time.", cant],
                   "They both use 4 sand timers, but the timers are not the same. Each big timer takes longer. "
                   "So <b>Jayden</b> takes longer. (Not the same time: we can only compare counts when the units are the same.)"))
    its.append(mcq("Which is the <b>longest</b> time?", "2 hours", ["100 seconds", "50 minutes", "20 minutes"],
                   "Hours are the longest unit here. 2 hours is 120 minutes. 50 minutes and 20 minutes are less than 1 hour. "
                   "100 seconds is less than 2 minutes. So <b>2 hours</b> is the longest. (A big number is not always a long time.)"))
    its.append(mcq("Which is the <b>shortest</b> time?", "30 seconds", ["3 minutes", "1 hour", "20 minutes"],
                   "Seconds are the shortest unit. 30 seconds is less than 1 minute. So <b>30 seconds</b> is the shortest. "
                   "(Not 3 minutes: 3 is a smaller number, but 3 minutes is 180 seconds.)"))
    its.append(mcq("Which is <b>longer</b>: 1 minute or 45 seconds?", "1 minute", ["45 seconds", "They are the same.", cant],
                   "1 minute is 60 seconds. 60 seconds is more than 45 seconds. So <b>1 minute</b> is longer. "
                   "(45 is a bigger number than 1, but seconds are much shorter than minutes.)"))
    its.append(mcq("Which is <b>longer</b>: 1 hour or 75 minutes?", "75 minutes", ["1 hour", "They are the same.", cant],
                   "1 hour is 60 minutes. 75 minutes is more than 60 minutes. So <b>75 minutes</b> is longer. "
                   "(An hour is not 100 minutes.)"))
    a, b = next(people), next(people)
    its.append(mcq("%s’s soccer practice is <b>1 hour</b>. %s’s swimming lesson is <b>45 minutes</b>. "
                   "Which one is <b>shorter</b>?" % (a[0], b[0]), "%s’s swimming lesson" % b[0],
                   ["%s’s soccer practice" % a[0], "They take the same time.", cant],
                   "1 hour is 60 minutes. 45 minutes is less than 60 minutes. So <b>%s’s swimming lesson</b> is shorter." % b[0]))
    assert len(its) == 20
    order = [0, 1, 3, 4, 2, 5, 6, 8, 9, 7, 12, 11, 10, 13, 14, 17, 16, 15, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Longer or shorter?", "items": [its[i] for i in order]}


# ============================================================ set 3: clocks to the hour and half hour
def hand_text(h, m):
    h = h12(h)
    if m == 0:
        return "The long hand points to the <b>12</b>. The short hand points to the <b>%d</b>." % h
    return ("The long hand points to the <b>6</b>: half way around. The short hand is half way between "
            "%d and %d. It has not reached %d yet, so the hour is <b>%d</b>." % (h, h % 12 + 1, h % 12 + 1, h))


def set_clocks(rnd):
    oc, hp, wd, abcd, hands = [], [], [], [], []
    for h in [3, 7, 9, 1, 10]:
        sw = "12:%02d" % (h * 5)
        c = [sw, "%d:12" % h, dig(h + 1, 0), dig(h - 1, 0)]
        e = ("%s So it is %d o’clock: <b>%s</b>. (Not %s: that mixes up the hands. Not %d:12: when the long hand points to 12, "
             "it is 0 minutes.)" % (hand_text(h, 0), h, dig(h, 0), sw, h))
        oc.append(mcq(fig(clock_svg(h, 0)) + "What time does the clock show?", dig(h, 0), c, e))
    for h in [2, 4, 8, 11, 1, 9]:
        c = [dig(h + 1, 30), "%d:06" % h12(h), "%d:50" % h12(h), dig(h, 0)]
        e = ("%s So it is half past %d: <b>%s</b>. (Not %s: the short hand has not reached %d. "
             "Not %d:06 or %d:50: half past is 30 minutes.)"
             % (hand_text(h, 30), h12(h), dig(h, 30), dig(h + 1, 30), h12(h + 1), h12(h), h12(h)))
        hp.append(mcq(fig(clock_svg(h, 30)) + "What time does the clock show?", dig(h, 30), c, e))
    for h, m in [(7, 30), (10, 0), (11, 30)]:
        right = words(h, m)
        if m == 30:
            c = [words(h + 1, 30), words(h, 0), "6 o’clock", words(h + 1, 0)]
            e = "%s So it is <b>%s</b>. (Not %s: the short hand has not reached %d yet.)" % (
                hand_text(h, m), right, words(h + 1, 30), h12(h + 1))
        else:
            c = ["12 o’clock", words(h + 1, 0), words(h, 30), words(h - 1, 0)]
            e = "%s So it is <b>%s</b>. (Not 12 o’clock: the long hand on the 12 means o’clock. The short hand tells the hour.)" % (hand_text(h, m), right)
        wd.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Choose the words.", right, c, e))
    for (h, m), others, pos in [((3, 30), [(4, 30), (3, 0), (6, 15)], 2),
                                ((9, 0), [(12, 45), (10, 0), (9, 30)], 1),
                                ((2, 30), [(3, 30), (6, 10), (2, 0)], 3)]:
        times = list(others)
        times.insert(pos, (h, m))
        assert len(set(times)) == 4
        L = "ABCD"
        notes = []
        for t in others:
            if t[1] in (0, 30):
                notes.append("Clock %s shows %s." % (L[times.index(t)], words(*t)))
            else:
                notes.append("Clock %s has the hands mixed up." % L[times.index(t)])
        e = "%s That is clock <b>%s</b>. %s" % (hand_text(h, m), L[pos], " ".join(notes))
        abcd.append({"q": fig(clocks4_svg(times)) + "Which clock shows <b>%s</b>?" % (words(h, m) if m == 0 else dig(h, m)),
                     "c": ["A", "B", "C", "D"], "a": pos, "e": e, "fixed": True})
    hands.append(mcq("At <b>half past</b>, where does the <b>long</b> hand point?", "to the 6",
                     ["to the 12", "to the 10", "to the 3"],
                     "Half past means the long hand has gone half way around the clock. It points to the <b>6</b>. "
                     "(Not the 10: that would be 50 minutes, and half an hour is 30 minutes.)"))
    hands.append(mcq("At <b>8 o’clock</b>, where does the <b>short</b> hand point?", "to the 8",
                     ["to the 12", "between 8 and 9", "to the 7"],
                     "At o’clock, the short hand points right at the hour. At 8 o’clock it points to the <b>8</b>, "
                     "and the long hand points to the 12."))
    hands.append(mcq("At <b>half past 3</b>, where is the <b>short</b> hand?", "between 3 and 4",
                     ["right on the 3", "right on the 4", "on the 6"],
                     "In half an hour the short hand moves half way to the next number. At half past 3 it is "
                     "<b>between 3 and 4</b>. The long hand is on the 6."))
    its = oc[:3] + [hands[1]] + oc[3:] + [wd[1], hands[0]] + hp[:3] + [abcd[1], wd[0]] + hp[3:] + [hands[2], abcd[0], wd[2], abcd[2]]
    assert len(its) == 20
    return {"title": "Read clocks to the hour and half hour", "items": its}


# ============================================================ set 4: how long, in hours and half hours
def how_long(text, h1, m1, h2, m2, figure=None):
    t1, t2 = h1 * 60 + m1, h2 * 60 + m2
    d = t2 - t1
    assert d > 0 and d % 30 == 0
    pts = steps(t1, t2)
    q = {"line": lambda: fig(timeline_svg(h1, m1, h2, m2)), "clocks": lambda: fig(start_end_svg(h1, m1, h2, m2)),
         None: lambda: ""}[figure]() + text
    c = []
    if m1 == 0 and m2 == 0:
        c.append(dur(d + 60))                                   # counting the numbers, not the jumps
    if d % 60 == 30:
        c.append("%d hour%s 50 minutes" % (d // 60, "" if d // 60 == 1 else "s") if d > 60 else "50 minutes")  # half hour as 50
    hd = (h2 - h1) * 60
    if hd != d and hd > 0:
        c.append(dur(hd))                                       # only the hour numbers
    c += [dur(d + 30), dur(d - 30) if d > 30 else None, dur(d + 60), dur(d + 90)]
    jumps = " → ".join(dig(t // 60, t % 60) for t in pts)
    n1 = sum(1 for a, b in zip(pts, pts[1:]) if b - a == 60)
    half = any(b - a == 30 for a, b in zip(pts, pts[1:]))
    parts = []
    if n1:
        parts.append("%d jump%s of 1 hour" % (n1, "" if n1 == 1 else "s"))
    if half:
        parts.append("1 jump of half an hour (30 minutes)")
    e = "Count the jumps: %s. That is %s. So it is <b>%s</b>." % (jumps, " and ".join(parts), dur(d))
    if m1 == 0 and m2 == 0 and d >= 120:
        e += " (Count the jumps, not the numbers.)"
    if half:
        e += " (Half an hour is 30 minutes, not 50.)"
    return mcq(q, dur(d), c, e, key=dur_value)


def set_howlong(rnd, people):
    its = []
    for h1, m1, h2, m2 in [(3, 0, 5, 0), (8, 0, 8, 30), (2, 30, 3, 30), (1, 0, 4, 0)]:
        its.append(how_long("How long is it from the start time to the end time?", h1, m1, h2, m2, "clocks"))
    nm, pr = next(people)
    its.append(how_long("Hockey practice is from <b>4:00 p.m.</b> to <b>5:30 p.m.</b> How long is practice?", 4, 0, 5, 30, "line"))
    its.append(mcq("How many <b>half hours</b> are in 1 hour?", "2", ["1", "30", "60"],
                   "Half an hour is 30 minutes. 30 + 30 = 60 minutes = 1 hour. So <b>2</b> half hours make 1 hour."))
    assert 9 * 60 + 60 == 10 * 60
    its.append(mcq("The field trip bus leaves at <b>9:00 a.m.</b> The ride takes <b>1 hour</b>. What time does the bus get there?",
                   "10:00 a.m.", ["9:01 a.m.", "11:00 a.m.", "8:00 a.m."],
                   "Add 1 hour: 9:00 → 10:00. The bus gets there at <b>10:00 a.m.</b> "
                   "(Not 9:01: 1 hour is not 1 minute. Not 8:00: that goes back in time.)"))
    for h1, m1, h2, m2 in [(9, 0, 10, 30), (10, 30, 11, 0)]:
        its.append(how_long("How long is it from the start time to the end time?", h1, m1, h2, m2, "clocks"))
    nm, pr = next(people)
    its.append(how_long("%s’s family is at the beach from <b>1:00 p.m.</b> to <b>4:00 p.m.</b> How long are they at the beach?"
                        % nm, 13, 0, 16, 0, "line"))
    its.append(mcq("A skating lesson starts at <b>4:00 p.m.</b> It lasts <b>half an hour</b>. What time does it end?",
                   "4:30 p.m.", ["4:50 p.m.", "5:00 p.m.", "5:30 p.m."],
                   "Half an hour is 30 minutes. 4:00 and 30 minutes is <b>4:30 p.m.</b> "
                   "(Not 4:50: half an hour is not 50 minutes. Not 5:00: that is a whole hour.)"))
    for h1, m1, h2, m2 in [(4, 30, 7, 0), (7, 0, 10, 30)]:
        its.append(how_long("How long is it from the start time to the end time?", h1, m1, h2, m2, "clocks"))
    its.append(how_long("A family movie night is from <b>7:00 p.m.</b> to <b>8:30 p.m.</b> How long is it?", 19, 0, 20, 30, "line"))
    its.append(mcq("Story time at the library starts at <b>10:30 a.m.</b> It lasts <b>1 hour</b>. What time does it end?",
                   "11:30 a.m.", ["10:31 a.m.", "12:30 p.m.", "11:00 a.m."],
                   "Add 1 hour: 10:30 → 11:30. It ends at <b>11:30 a.m.</b> "
                   "(Not 11:00: that adds only half an hour. Not 10:31: 1 hour is not 1 minute.)"))
    nm, pr = next(people)
    its.append(how_long("%s plays at the park from <b>3:30 p.m.</b> to <b>5:00 p.m.</b> How long does %s play?" % (nm, pr),
                        15, 30, 17, 0))
    its.append(mcq("Bedtime is <b>8:00 p.m.</b> Reading time starts <b>half an hour</b> before bedtime. "
                   "What time does reading time start?", "7:30 p.m.", ["8:30 p.m.", "7:00 p.m.", "7:50 p.m."],
                   "Count back half an hour (30 minutes) from 8:00. That is <b>7:30 p.m.</b> "
                   "(Not 8:30 p.m.: that is <b>after</b> bedtime. Not 7:00 p.m.: that is a whole hour before.)"))
    its.append(how_long("The Canada Day party in the park is from <b>11:30 a.m.</b> to <b>2:30 p.m.</b> How long is the party?",
                        11, 30, 14, 30, "line"))
    assert 9 * 60 + 180 == 12 * 60
    its.append(mcq("The drive to the cottage starts at <b>9:00 a.m.</b> It takes <b>3 hours</b>. What time do they get there?",
                   "12:00 noon", ["9:03 a.m.", "1:00 p.m.", "6:00 a.m."],
                   "Add 3 hours, one jump at a time: 9:00 → 10:00 → 11:00 → 12:00. They get there at <b>12:00 noon</b>. "
                   "(Not 1:00 p.m.: that counts 9 as a jump too. Not 9:03: 3 hours is not 3 minutes.)"))
    nm, pr = next(people)
    its.append(how_long("%s’s hockey tournament game is from <b>6:30 p.m.</b> to <b>8:00 p.m.</b> How long is the game?" % nm,
                        18, 30, 20, 0))
    assert len(its) == 20
    return {"title": "How long? Hours and half hours", "items": its}


# ============================================================ set 5: timers and word problems
def set_words(rnd, people):
    its = []
    m = lambda n: "%d minute%s" % (n, "" if n == 1 else "s")
    s = lambda n: "%d second%s" % (n, "" if n == 1 else "s")
    its.append(mcq(fig(timer_svg(8, 0)) + "The oven timer shows how long until the cookies are done. How long is that?",
                   "8 minutes", ["8 seconds", "8 hours", "80 minutes"],
                   "A timer shows minutes, then a colon, then seconds. 8:00 means <b>8 minutes</b> and 0 seconds."))
    its.append(mcq(fig(stopwatch_svg(30)) + "The stopwatch hand goes around once in 60 seconds. How much time does it show?",
                   "30 seconds", ["6 seconds", "30 minutes", "35 seconds"],
                   "The numbers on a stopwatch count by 5s. The hand points to <b>30</b>, so it shows <b>30 seconds</b>."))
    assert 15 - 10 == 5
    its.append(mcq("Recess is <b>15 minutes</b> long. <b>10 minutes</b> have passed. How many minutes are left?",
                   m(5), [m(25), m(10), m(15)],
                   "15 − 10 = <b>5 minutes</b> left. (Not 25: that adds instead of taking away.)"))
    assert 2 + 2 == 4
    nm, pr = next(people)
    its.append(mcq("%s brushes %s teeth for <b>2 minutes</b> in the morning and <b>2 minutes</b> at night. "
                   "How long is that each day?" % (nm, "his" if pr == "he" else "her"), m(4), ["4 hours", m(2), m(22)],
                   "2 + 2 = <b>4 minutes</b>. (Not 4 hours: brushing teeth is quick.)"))
    its.append(mcq("Swimming lessons are <b>half an hour</b> long. How many minutes is that?", m(30), [m(50), m(60), m(15)],
                   "1 hour is 60 minutes. Half of 60 is <b>30 minutes</b>. (Not 50: an hour is not 100 minutes.)"))
    its.append(mcq(fig(stopwatch_svg(45)) + "How much time does the stopwatch show?", "45 seconds",
                   ["9 seconds", "45 minutes", "50 seconds"],
                   "Count by 5s to the number the hand points to: 5, 10, 15, … 45. It shows <b>45 seconds</b>. "
                   "(Not 9: 45 is the 9th number, but each number is 5 seconds.)"))
    assert 20 + 15 == 35
    nm, pr = next(people)
    its.append(mcq("%s reads for <b>20 minutes</b>. Then %s reads for <b>15 more minutes</b>. How long does %s read?" % (nm, pr, pr),
                   m(35), [m(5), m(25), m(45)],
                   "20 + 15 = <b>35 minutes</b>. 2 tens and 1 ten make 3 tens, and there are 5 ones. "
                   "(Not 5: that takes away instead of adding.)"))
    assert 15 + 15 + 15 == 45
    nm, pr = next(people)
    its.append(mcq("In %s’s hockey league, each period is <b>15 minutes</b>. A game has <b>3 periods</b>. "
                   "How many minutes of hockey is that?" % nm, m(45), [m(30), m(18), m(60)],
                   "Add 15 three times: 15 + 15 + 15 = <b>45 minutes</b>. (Not 18: that is 15 + 3. Not 30: that is only 2 periods.)"))
    assert 60 + 30 == 90
    its.append(mcq("A movie is <b>1 hour 30 minutes</b> long. How many minutes is that?", m(90), [m(130), m(31), m(60)],
                   "1 hour = 60 minutes. 60 + 30 = <b>90 minutes</b>. (Not 130: an hour is 60 minutes, not 100.)"))
    assert 20 - 6 == 14
    its.append(mcq(fig(timer_svg(6, 0)) + "Quiet reading time is <b>20 minutes</b>. The timer counts down. It shows this now. "
                   "How many minutes have passed?", m(14), [m(26), m(6), m(16)],
                   "The timer shows 6 minutes left. 20 − 6 = <b>14 minutes</b> have passed. "
                   "(Not 6: that is the time left. Not 26: that adds instead of taking away.)"))
    assert 30 + 30 == 60
    its.append(mcq("The Terry Fox Run starts at <b>10:00 a.m.</b> Emma runs for <b>half an hour</b>. What time does she finish?",
                   "10:30 a.m.", ["10:50 a.m.", "11:00 a.m.", "11:30 a.m."],
                   "Half an hour is 30 minutes. 10:00 and 30 minutes is <b>10:30 a.m.</b> (Not 10:50: half an hour is not 50 minutes.)"))
    assert 15 - 6 == 9
    its.append(mcq("Afternoon recess is <b>15 minutes</b>. The bell rang <b>6 minutes</b> ago. How many minutes of recess are left?",
                   m(9), [m(21), m(10), m(6)],
                   "15 − 6 = <b>9 minutes</b>. Count back from 15: 14, 13, 12, 11, 10, 9. (Not 21: that adds. "
                   "Not 10: when you count back, do not count the 15.)"))
    assert 3 - 1 == 2
    nm, pr = next(people)
    its.append(mcq("%s’s family drives to the cottage. The drive takes <b>3 hours</b>. They have driven for <b>1 hour</b>. "
                   "How much longer is the drive?" % nm, "2 hours", ["4 hours", "2 minutes", "3 hours"],
                   "3 − 1 = <b>2 hours</b> left. (Not 4: that adds the hour instead of taking it away.)"))
    assert 60 - 45 == 15
    a, b = next(people), next(people)
    its.append(mcq("On a snow day, %s plays outside for <b>1 hour</b>. %s plays outside for <b>45 minutes</b>. "
                   "Who plays longer, and by how much?" % (a[0], b[0]), "%s, by 15 minutes" % a[0],
                   ["%s, by 55 minutes" % a[0], "%s, by 15 minutes" % b[0], "%s, by 44 minutes" % b[0]],
                   "1 hour = 60 minutes. 60 − 45 = 15. So <b>%s</b> plays longer, <b>by 15 minutes</b>. "
                   "(Not 55: that counts an hour as 100 minutes. Not %s: 45 is more than 1, but 1 hour is more than 45 minutes.)"
                   % (a[0], b[0])))
    assert 25 + 30 == 55
    nm, pr = next(people)
    its.append(mcq("%s practises piano for <b>25 minutes</b> on Monday and <b>30 minutes</b> on Tuesday. "
                   "How many minutes is that?" % nm, m(55), [m(5), m(28), m(65)],
                   "25 + 30 = <b>55 minutes</b>. 2 tens and 3 tens make 5 tens, and there are 5 ones. "
                   "(Not 5: that takes away. Not 28: that adds 3, not 3 tens.)"))
    assert 45 + 35 == 80
    its.append(mcq("A loon dives under the water for <b>45 seconds</b>. Then it dives again for <b>35 seconds</b>. "
                   "How many seconds is it under the water in all?", s(80), [s(70), s(10), "80 minutes"],
                   "45 + 35: 5 ones + 5 ones = 10 ones, which is 1 more ten. 4 tens + 3 tens + 1 ten = 8 tens. So it is "
                   "<b>80 seconds</b>. (Not 70: do not forget the new ten. Not 80 minutes: a loon dive is not that long.)"))
    its.append(mcq("The bus ride to the farm takes <b>40 minutes</b>. The ride back takes <b>40 minutes</b> too. "
                   "How long are they on the bus?", "80 minutes, more than 1 hour",
                   ["80 minutes, less than 1 hour", "40 minutes, less than 1 hour", "60 minutes, exactly 1 hour"],
                   "40 + 40 = 80 minutes. 1 hour is 60 minutes, and 80 is more than 60. "
                   "So it is <b>80 minutes, more than 1 hour</b>. (An hour is not 100 minutes.)"))
    assert 40 - 20 == 20
    its.append(mcq("Lunch is <b>40 minutes</b>. Students eat for <b>20 minutes</b>. Then they play outside for the rest of lunch. "
                   "How many minutes do they play outside?", m(20), [m(60), m(40), m(30)],
                   "40 − 20 = <b>20 minutes</b>. (Not 60: that adds. Not 40: that is the whole lunch.)"))
    assert 12 - 7 == 5
    nm, pr = next(people)
    its.append(mcq(fig(timer_svg(7, 0)) + "%s sets a timer for <b>12 minutes</b> to tidy %s room. The timer counts down. "
                   "It shows this now. How many minutes has %s been tidying?" % (nm, "his" if pr == "he" else "her", pr),
                   m(5), [m(19), m(7), m(6)],
                   "The timer shows 7 minutes left. 12 − 7 = <b>5 minutes</b>. Count up from 7: 8, 9, 10, 11, 12 is 5 jumps. "
                   "(Not 7: that is the time left. Not 19: that adds.)"))
    assert 15 + 15 + 40 == 70
    its.append(mcq("Each school day has a <b>15-minute</b> morning recess, a <b>40-minute</b> lunch and a <b>15-minute</b> "
                   "afternoon recess. How many minutes is that in all?", m(70), [m(60), m(55), m(80)],
                   "15 + 15 = 30. 30 + 40 = <b>70 minutes</b>. (Not 55: that leaves out one recess. Not 60: do not forget "
                   "the new ten when you add 5 + 5.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 8, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Timers and time word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Seconds, minutes and hours</h2>"
        "<p>We use units of time to tell <b>how long</b> something takes. "
        "<b>Seconds</b> are for very quick things. <b>Minutes</b> are for things that take a little while. "
        "<b>Hours</b> are for long things.</p>"
        + table(["Unit", "Good for", "Example"], [
            ["seconds", "very quick things", "clap 3 times: about 3 seconds"],
            ["minutes", "things that take a little while", "brush your teeth: about 2 minutes"],
            ["hours", "long things", "sleep at night: about 10 hours"]]) +
        "<p><b>60 seconds = 1 minute</b>. <b>60 minutes = 1 hour</b>. <b>Half an hour = 30 minutes</b>.</p>"
        + ex("Choose the unit", "About how long is recess?", "Recess is longer than a few seconds, but shorter than an hour.",
             "about 15 minutes") +
        "<h2>Longer or shorter</h2>"
        "<p>We can also measure time with things like claps or a sand timer. Use the <b>same</b> sand timer each time. "
        "More sand timers means a longer time.</p>"
        "<figure class='sn-fig'>" + sand_rows_svg([("Mei", 3), ("Owen", 5)]) +
        "<figcaption>Mei takes 3 sand timers. Owen takes 5 of the same sand timer. <b>Owen takes longer.</b></figcaption></figure>"
        "<p>Look at the <b>unit</b>, not only the number. 3 minutes is longer than 30 seconds.</p>"
        "<h2>O’clock and half past</h2>"
        "<p>The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "At o’clock, the long hand points to the 12. At half past, it points to the 6.</p>"
        "<figure class='sn-fig'>" + clock_svg(3, 30, size=210) +
        "<figcaption>The long hand points to the 6. The short hand is between 3 and 4. It is <b>half past 3</b>, "
        "or 3:30.</figcaption></figure>"
        "<h2>How long from start to end?</h2>"
        "<p>Start at the start time. Jump 1 hour at a time. Then jump half an hour if you need to. Count the jumps.</p>"
        "<figure class='sn-fig'>" + timeline_svg(4, 0, 6, 30) +
        "<figcaption>From 4:00 to 6:30: 2 jumps of 1 hour and 1 jump of half an hour. That is "
        "<b>2 hours 30 minutes</b>.</figcaption></figure>"
        + ex("Timer", "Recess is 15 minutes. 10 minutes have passed. How many minutes are left?", "15 − 10 = 5", "5 minutes") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Brushing teeth takes 2 hours", "Quick things take seconds or minutes. It takes about 2 minutes."],
            ["Half an hour is 50 minutes", "1 hour is 60 minutes, so half an hour is 30 minutes."],
            ["3 minutes is shorter than 30 seconds, because 3 is smaller", "Look at the unit. 3 minutes is 180 seconds."],
            ["Half past 3 read as half past 4", "The short hand has not reached the 4 yet. It is still 3."],
            ["3:00 to 5:00 is 3 hours (3, 4, 5)", "Count the jumps, not the numbers: 2 hours."],
        ])
    )


FAQ = [
    {"q": "What do Grade 2 students learn about time in Ontario math?",
     "a": "In the Ontario math curriculum (expectation E2.4), Grade 2 students use seconds, minutes, hours and non-standard units, like claps or a sand timer, to describe how long events last."},
    {"q": "How many minutes are in half an hour?",
     "a": "Half an hour is 30 minutes, because 1 hour is 60 minutes. Many children guess 50 minutes, because they think of 100 instead of 60."},
    {"q": "Do Grade 2 students learn to tell time to the minute?",
     "a": "Not yet. In Grade 2, o’clock and half past help students say how long things take. In Grade 3, students use analog and digital clocks to tell time in hours, minutes and seconds."},
    {"q": "How can I help my child understand how long a minute is?",
     "a": "Use a kitchen timer for everyday jobs, like brushing teeth for 2 minutes or tidying up for 5 minutes. Ask your child to guess first, then check with the timer."},
]


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Picture items (A to D) keep their order and position."""
    for s in sets:
        fixed = [it["a"] for it in s["items"] if it.get("fixed")]
        targets = [p for p in range(4) for _ in range(5)]
        for p in fixed:
            targets.remove(p)
        rnd.shuffle(targets)
        targets = iter(targets)
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = next(targets)
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(42815)
    people = PEOPLE[:]
    rnd.shuffle(people)
    people = iter(people * 3)
    sets = [set_units(rnd), set_compare(rnd, people), set_clocks(rnd), set_howlong(rnd, people), set_words(rnd, people)]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-2", "slug": "time", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Time: Seconds, Minutes and Hours, O’clock and Half Past, How Long Things Take",
        "seo_title": "Grade 2 Time Math Worksheets: Seconds, Minutes, Hours and Half Past, Free with Answer Key (Ontario)",
        "short_title": "Time",
        "domain": "Spatial Sense",
        "standard_code": "Grade 2: E2.4",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use units of time, including seconds, minutes, hours, and non-standard units, to describe the duration of various events",
        "meta_desc": "Free Grade 2 math worksheets on time for the Ontario curriculum: choose seconds, minutes or hours, compare longer and shorter events with sand timers, read clocks to the hour and half hour, find how long from start to end, and solve timer word problems. 100 questions with an answer key.",
        "key_big": "Seconds for quick things, minutes for a little while, hours for long things.",
        "key_sub": "1 hour = 60 minutes, so half an hour is 30 minutes, not 50. To find how long, count the jumps from the start time, not the numbers.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "time line")
    mark_large(u, "start and end clocks")
    mark_large(u, "two pictures")
    mark_large(u, "sand timers")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
