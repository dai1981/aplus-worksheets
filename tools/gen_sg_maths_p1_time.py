# -*- coding: utf-8 -*-
"""
Singapore Primary 1 Maths: Time (MOE 2021 Primary Mathematics Syllabus, Measurement)
"Telling time to 5 minutes; use of am and pm; use of h and min; duration of one hour/half hour"
  python3 tools/gen_sg_maths_p1_time.py
O'clock and half past, telling time to 5 minutes (written 3.25, Singapore dot style), am and pm
(school at 7.30 am, dinner at 7 pm), 1 hour later / half an hour later, h and min, and short
Singapore word problems. Every analog clock is drawn from the time itself (the hour hand moves
between the numbers). Every answer is worked out in code. Wrong answers come from real mistakes:
the two hands swapped (3.25 read as 5.15), the number under the long hand read as the minutes
(3.25 read as 3.05), the next hour read when the short hand is near it, am and pm mixed up,
counting back instead of on, half an hour taken as 50 min, 1 h taken as 100 min.
Helpers adapted from gen_sg_maths_p3_time.py and gen_cabc_math_g3_time.py.
Times: 3 o’clock, half past 3, 3.25, 7.30 am, 7 pm, 12 noon. Durations: 1 h, 30 min.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-1")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
INK = "#2b2b2b"
RED = "#c0392b"
SOFT = "#eef5f0"
SUN = "#f2b705"
NIGHT = "#2c3e66"
FONT = "Arial, Helvetica, sans-serif"
DAY = 24 * 60


# ------------------------------------------------------------ time formats
def h12(h):
    return (h - 1) % 12 + 1


def rd(h, m):
    """clock reading without am/pm: 3.25, 10.05"""
    h = h12(h)
    assert 0 <= m < 60
    return "%d.%02d" % (h, m)


def oc(h):
    return "%d o’clock" % h12(h)


def hp(h):
    return "half past %d" % h12(h)


def ap(t):
    """Singapore 12-hour time from minutes after midnight: 7.30 am, 7 pm, 12 noon, 12 midnight"""
    t %= DAY
    h, m = divmod(t, 60)
    if t == 12 * 60:
        return "12 noon"
    if t == 0:
        return "12 midnight"
    s = ("%d" % h12(h)) if m == 0 else ("%d.%02d" % (h12(h), m))
    return s + (" am" if h < 12 else " pm")


def T_(h, m=0):
    return h * 60 + m


def apval(s):
    """minutes after midnight of a Singapore time string (to check choices)"""
    if s == "12 noon":
        return 720
    if s == "12 midnight":
        return 0
    mo = re.match(r"^(\d{1,2})(?:\.(\d\d))? (am|pm)$", s)
    assert mo, s
    h, m = int(mo.group(1)) % 12, int(mo.group(2) or 0)
    return (h + (12 if mo.group(3) == "pm" else 0)) * 60 + m


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def swapped(h, m):
    """What a child reads if the hands are swapped: long hand read as the hour,
    the short hand read as the minutes (to the nearest 5)."""
    hh = m // 5 or 12
    mm = int(round(((h % 12) + m / 60.0) * 5 / 5.0)) * 5 % 60
    return rd(hh, mm)


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
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def apmcq(q, correct, cands, e):
    return mcq(q, correct, cands, e, key=apval)


def fixed(q, letters_right, e):
    """A-D picture question: choices stay in A, B, C, D order."""
    i = "ABCD".index(letters_right)
    return {"q": q, "c": ["A", "B", "C", "D"], "a": i, "e": e, "fixed": True}


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w + 0.49)), int(round(h + 0.49))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def T(x, y, s, size=16, fill=INK, anchor="middle", weight="700"):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%s' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, size, weight, fill, anchor, s))


def tw(s, size=15):
    return len(s) * size * 0.58


# ------------------------------------------------------------ pictures
def face(cx, cy, R, k):
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
    return s


def clock_body(h, m, size, ox=0.0, oy=0.0):
    """Analog clock. The short (hour) hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    R = size / 2.0 - 6
    cx, cy = ox + size / 2.0, oy + size / 2.0
    k = R / 94.0
    s = face(cx, cy, R, k)
    fs = max(19 * k, 15)
    rn = R - 29 * k
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 9 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.82 * math.cos(am), cy + R * 0.82 * math.sin(am), RED, 4.5 * k))
    # numbers on top of the hands, with a white outline so a hand never hides a number
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' "
             "stroke-width='%.1f' paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def sun_icon(cx, cy, r=13):
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, r, SUN)]
    rays = []
    for i in range(8):
        a = math.radians(i * 45)
        rays.append("M%.1f %.1fL%.1f %.1f" % (cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a),
                                              cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a)))
    s.append("<path d='%s' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % ("".join(rays), SUN))
    return "".join(s)


def moon_icon(cx, cy, r=15):
    # crescent: big circle with a bite taken out by a second circle (drawn as a path of two arcs)
    return ("<path d='M%.1f %.1f A%.1f %.1f 0 1 0 %.1f %.1f A%.1f %.1f 0 1 1 %.1f %.1f Z' fill='%s'/>"
            "<circle cx='%.1f' cy='%.1f' r='2.2' fill='%s'/><circle cx='%.1f' cy='%.1f' r='1.8' fill='%s'/>"
            % (cx + 4, cy - r + 1, r, r, cx + 4, cy + r - 1, r * 0.78, r * 0.78, cx + 4, cy - r + 1, NIGHT,
               cx + r + 6, cy - r + 4, NIGHT, cx + r + 2, cy + 4, NIGHT))


def clock_svg(h, m, size=200, sky=None):
    """sky: None, 'sun' or 'moon' (a small picture beside the clock)."""
    if not sky:
        return svg_wrap(size, size, clock_body(h, m, size), "analog clock")
    W = size + 62
    icon = sun_icon(size + 31, 34) if sky == "sun" else moon_icon(size + 28, 34)
    return svg_wrap(W, size, clock_body(h, m, size) + icon, "analog clock with a %s" % sky)


def ring_clock_svg(h, m, size=200, arc=None):
    """Clock with the minutes (5, 10, ... 55) in green outside, or a green arc showing how far the
    long hand turns. arc = (start minute, minutes turned)."""
    pad = 30
    W = size + 2 * pad
    c = W / 2.0
    R = size / 2.0 - 6
    s = [clock_body(h, m, size, pad, pad)]
    if arc is None:
        s.append("<g font-size='15' font-weight='700' fill='%s' text-anchor='middle'>" % GREEN)
        for n in range(12):
            a = math.radians(n * 30 - 90)
            r2 = R + 18
            s.append("<text x='%.1f' y='%.1f'>%s</text>" % (c + r2 * math.cos(a), c + r2 * math.sin(a) + 5,
                                                           "%02d" % (5 * n) if n else "00"))
        s.append("</g>")
        label = "analog clock with the minutes"
    else:
        m0, sweep = arc
        assert 0 < sweep <= 60
        r2 = R + 14
        pts = []
        for i in range(sweep * 2 + 1):
            a = math.radians((m0 + i / 2.0) * 6 - 90)
            pts.append("%.1f %.1f" % (c + r2 * math.cos(a), c + r2 * math.sin(a)))
        s.append("<path d='M%s' fill='none' stroke='%s' stroke-width='4'/>" % (" L".join(pts), GREEN))
        a = math.radians((m0 + sweep) * 6 - 90)
        ex_, ey = c + r2 * math.cos(a), c + r2 * math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)          # tangent, clockwise
        nx, ny = math.cos(a), math.sin(a)
        s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='%s'/>"
                 % (ex_ + tx * 10, ey + ty * 10, ex_ - tx * 4 + nx * 8, ey - ty * 4 + ny * 8,
                    ex_ - tx * 4 - nx * 8, ey - ty * 4 - ny * 8, GREEN))
        label = "analog clock with an arrow"
    return svg_wrap(W, W, "".join(s), label)


def pair_svg(t1, t2, labels=("Start", "End"), size=170):
    gap, top = 16, 28
    W = 2 * size + gap
    s = []
    for i, (h, m) in enumerate([t1, t2]):
        x = i * (size + gap)
        s.append(T(x + size / 2.0, 20, labels[i], 19, GREEN))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), "two clocks")


def four_svg(times, size=150):
    gap, top = 14, 28
    W = 4 * size + 3 * gap
    s = []
    for i, (h, m) in enumerate(times):
        x = i * (size + gap)
        s.append(T(x + size / 2.0, 21, "ABCD"[i], 21, GREEN))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), "clock choices")


def digital_svg(text):
    W = max(200, int(len(text) * 24.5 + 44))
    H = 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='%s'/>" % (W - 32, H - 28, SOFT),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, text)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def dayline_svg(mark=None, W=460):
    """One day from 12 midnight to 12 midnight. am on the left half, pm on the right half.
    mark: minutes after midnight for a red arrow, with its label."""
    L, R, Y = 44, W - 44, 78
    span = R - L
    mid = (L + R) / 2.0
    s = ["<rect x='%d' y='%d' width='%.1f' height='22' fill='%s' stroke='%s' stroke-width='2'/>" % (L, Y - 11, span / 2, FILL, GREEN),
         "<rect x='%.1f' y='%d' width='%.1f' height='22' fill='#dfe4f0' stroke='%s' stroke-width='2'/>" % (mid, Y - 11, span / 2, NIGHT),
         T(L + span / 4, Y + 6, "am", 16, GREEN), T(mid + span / 4, Y + 6, "pm", 16, NIGHT)]
    for x, lab in [(L, "12 midnight"), (mid, "12 noon"), (R, "12 midnight")]:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, Y - 18, x, Y + 18, LINE))
    s.append(T(L + 6, Y + 38, "12 midnight", 14, INK))
    s.append(T(mid, Y + 38, "12 noon", 14, INK))
    s.append(T(R - 6, Y + 38, "12 midnight", 14, INK))
    s.append(moon_icon(L + 8, 26, 12))
    s.append(sun_icon(mid, 30, 11))
    s.append(moon_icon(R - 12, 26, 12))
    s.append(T(L + span / 4, 34, "morning", 14, GREEN, weight="400"))
    s.append(T(mid + span / 4, 34, "afternoon, evening", 14, NIGHT, weight="400"))
    if mark is not None:
        x = L + span * mark / float(DAY)
        s.append("<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (x - 8, Y + 44, x + 8, Y + 44, x, Y + 20, RED))
        s.append(T(x, Y + 62, "?", 16, RED))
        H = Y + 70
    else:
        H = Y + 46
    return svg_wrap(W, H, "".join(s), "day line am and pm")


# ------------------------------------------------------------ lesson helpers
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5). Items marked 'fixed' (A-D pictures) keep their place."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        assert min(left.values()) >= 0, s["title"]
        targets = [p for p in range(4) for _ in range(left[p])]
        rnd.shuffle(targets)
        free = [it for it in s["items"] if not it.get("fixed")]
        assert len(free) == len(targets)
        for it, t in zip(free, targets):
            right = it["c"][it["a"]]
            wrong = [x for i, x in enumerate(it["c"]) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t
        for it in s["items"]:
            it.pop("fixed", None)


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def count5(m):
    """'5, 10, 15, 20, 25' for the explanation"""
    return ", ".join(str(5 * i) for i in range(1, m // 5 + 1))


# ============================================================ set 1: o'clock and half past
def read_oc(h, extra=()):
    c = list(extra) + ["12 o’clock" if h != 12 else None, hp(h), oc(h + 1), oc(h - 1)]
    return mcq(fig(clock_svg(h, 0)) + "What time is it?", oc(h), c,
               "The long hand points to <b>12</b>. The short hand points to <b>%d</b>. It is <b>%s</b>. "
               "(12 o’clock reads the long hand as the hour.)" % (h, oc(h)))


def read_hp(h):
    c = [hp(h + 1), "6 o’clock", oc(h), oc(h + 1)]
    return mcq(fig(clock_svg(h, 30)) + "What time is it?", hp(h), c,
               "The long hand points to <b>6</b>, so it is half past. The short hand is <b>between %d and %d</b>. "
               "It has passed %d, so it is <b>%s</b>. (Not %s: the short hand has not reached %d yet.)"
               % (h, h % 12 + 1, h, hp(h), hp(h + 1), h % 12 + 1))


def set_oclock():
    its = []
    its.append(read_oc(3))
    its.append(read_oc(8))
    its.append(mcq(fig(clock_svg(5, 0)) + "The long hand points to 12. The short hand points to 5. What time is it?",
                   "5 o’clock", ["12 o’clock", "half past 5", "6 o’clock"],
                   "When the long hand points to <b>12</b>, it is o’clock. The short hand shows the hour: <b>5 o’clock</b>."))
    its.append(read_oc(10))
    its.append(mcq(fig(clock_svg(9, 0)) + "At 9 o’clock, the long hand points to ___.", "12", ["9", "6", "3"],
                   "At any o’clock time, the long hand points to <b>12</b>. The short hand points to 9."))
    its.append(read_hp(4))
    its.append(mcq(fig(clock_svg(2, 30)) + "At half past 2, the long hand points to ___.", "6", ["12", "2", "3"],
                   "Half past means the long hand has gone half way around. It points to <b>6</b>."))
    its.append(read_hp(7))
    its.append(mcq(fig(clock_svg(8, 30)) + "Where is the short hand at half past 8?", "between 8 and 9",
                   ["on the 8", "on the 6", "between 7 and 8"],
                   "At half past 8, the short hand has moved half way from 8 to 9. It is <b>between 8 and 9</b>."))
    its.append(read_hp(1))
    its.append(mcq(fig(clock_svg(2, 30)) + "Half past 2 is the same as ___.", "2.30", ["2.50", "3.30", "2.06"],
                   "Half past 2 is 30 minutes after 2 o’clock. We write <b>2.30</b>. "
                   "(Not 2.50: half an hour is 30 min. Not 2.06: the 6 on the clock means 30 min.)"))
    its.append(mcq(fig(clock_svg(6, 0)) + "What time is it?", "6 o’clock", ["12.30", "half past 6", "half past 12"],
                   "The long hand points to <b>12</b> and the short hand points to <b>6</b>. It is <b>6 o’clock</b>. "
                   "(12.30 swaps the two hands: the short hand shows the hour.)"))
    its.append(read_hp(10))
    its.append(mcq(fig(clock_svg(11, 30)) + "What time is it?", "11.30", ["12.30", "6.55", "11.06"],
                   "The long hand points to 6, so it is half past. The short hand is between 11 and 12, so the hour is 11. "
                   "It is <b>11.30</b>. (12.30 reads the next number. 6.55 swaps the hands.)"))
    its.append(fixed(fig(four_svg([(9, 30), (10, 0), (10, 30), (11, 30)])) + "Which clock shows <b>half past 10</b>?", "C",
                     "Clock C: the long hand points to 6 and the short hand is between 10 and 11. "
                     "A is half past 9. B is 10 o’clock. D is half past 11."))
    its.append(fixed(fig(four_svg([(12, 25), (5, 0), (6, 0), (5, 30)])) + "Which clock shows <b>5 o’clock</b>?", "B",
                     "Clock B: the long hand points to 12 and the short hand points to 5. "
                     "Clock A has the hands swapped: its short hand is near 12. C is 6 o’clock. D is half past 5."))
    its.append(mcq(fig(clock_svg(4, 0)) + "It is 4 o’clock now. What time will it be at the next o’clock?",
                   "5 o’clock", ["3 o’clock", "half past 4", "6 o’clock"],
                   "The short hand moves on from 4 to the next number, <b>5</b>. So the next o’clock is <b>5 o’clock</b>. "
                   "(3 o’clock is before 4 o’clock.)"))
    its.append(mcq(fig(clock_svg(3, 30)) + "Which time comes just <b>before</b> the time on the clock?",
                   "3 o’clock", ["4 o’clock", "half past 4", "half past 2"],
                   "The clock shows half past 3. Just before it, the time was <b>3 o’clock</b>. "
                   "(4 o’clock comes after half past 3.)"))
    its.append(fixed(fig(four_svg([(7, 0), (1, 30), (6, 30), (7, 30)])) + "Which clock shows <b>7.30</b>?", "D",
                     "7.30 is half past 7. Clock D: the long hand points to 6 and the short hand is between 7 and 8. "
                     "A is 7 o’clock. B is half past 1. C is half past 6."))
    its.append(mcq(fig(clock_svg(9, 30)) + "Ali says the clock shows half past 10. Is he right?",
                   "No, it is half past 9.", ["Yes, he is right.", "No, it is 10 o’clock.", "No, it is half past 8."],
                   "The short hand is between 9 and 10. It has passed 9 but not 10, so it is <b>half past 9</b>. "
                   "Ali read the next number."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 15, 14, 16, 17, 13, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "O’clock and half past", "items": [its[i] for i in order]}


# ============================================================ set 2: to 5 minutes
def read5(h, m, sky=None, text="What time is it?", extra=()):
    right = rd(h, m)
    c = list(extra)
    c.append(swapped(h, m))                          # hands swapped
    if m // 5 and m // 5 != m:
        c.append(rd(h, m // 5))                     # the number under the long hand read as minutes
    c.append(rd(h + 1, m))                          # read the next hour
    c += [rd(h, (m + 5) % 60), rd(h, m - 5), rd(h - 1, m)]
    e = ("The short hand is between %d and %d, so the hour is <b>%d</b>. The long hand points to %d. "
         "Count in 5s: %s. It is <b>%s</b>."
         % (h12(h), h12(h + 1), h12(h), m // 5, count5(m), right))
    sw = swapped(h, m)
    if sw in c[:3]:
        e += " (Not %s: that swaps the hands. The short hand shows the hour.)" % sw
    return mcq(fig(clock_svg(h, m)) + text, right, c, e)


def set_five():
    its = []
    for n, right, wrong in [(4, "20", ["4", "40", "25"]), (7, "35", ["7", "70", "30"]), (10, "50", ["10", "100", "45"])]:
        its.append(mcq(fig(ring_clock_svg(12 if n != 10 else 1, 5 * n)) +
                       "The long hand points to <b>%d</b>. How many minutes past the hour is it?" % n, right, wrong,
                       "Count in 5s for each number: %s. So it is <b>%s</b> minutes past. (Not %d: count in 5s, not 1s.)"
                       % (count5(5 * n), right, n)))
    its.append(read5(3, 25))
    its.append(read5(7, 10))
    its.append(read5(2, 45))
    its.append(read5(9, 5))
    its.append(read5(6, 20))
    its.append(read5(11, 40))
    its.append(read5(4, 55))
    its.append(read5(8, 15))
    its.append(read5(1, 35))
    its.append(read5(5, 50))
    its.append(mcq(fig(clock_svg(10, 25)) + "The clock shows <b>10.25</b>. How many minutes past 10 is it?",
                   "25 minutes", ["5 minutes", "10 minutes", "30 minutes"],
                   "10.25 means <b>25 minutes</b> past 10. The long hand points to 5: 5, 10, 15, 20, 25. "
                   "(5 minutes reads the number 5 as 5 minutes.)"))
    its.append(mcq(fig(digital_svg("6.35")) + "The clock shows 6.35. Where does the long hand point?", "to the 7",
                   ["to the 6", "to the 3", "to the 5"],
                   "35 minutes: 5, 10, 15, 20, 25, 30, 35. That is 7 jumps of 5, so the long hand points to the <b>7</b>. "
                   "(Not the 3 or the 5: those are the digits of 35.)"))
    its.append(fixed(fig(four_svg([(8, 20), (4, 40), (9, 40), (8, 40)])) + "Which clock shows <b>8.40</b>?", "D",
                     "8.40: the short hand is between 8 and 9 and the long hand points to 8 (8 jumps of 5 = 40). "
                     "That is clock D. A is 8.20. B is 4.40. C is 9.40."))
    its.append(fixed(fig(four_svg([(3, 5), (5, 15), (3, 25), (4, 25)])) + "Which clock shows <b>3.25</b>?", "C",
                     "3.25: the short hand is between 3 and 4, and the long hand points to 5 (5 jumps of 5 = 25). "
                     "That is clock C. A is 3.05. B is 5.15 (hands swapped). D is 4.25."))
    its.append(mcq(fig(clock_svg(7, 50)) + "Hui Min says the clock shows 8.50. What is the right time?", "7.50",
                   ["8.50", "10.40", "7.10"],
                   "The short hand is close to 8, but it has <b>not reached</b> 8 yet. So the hour is still 7. "
                   "The long hand points to 10: 10 jumps of 5 = 50. It is <b>7.50</b>."))
    its.append(mcq(fig(clock_svg(12, 10)) + "What time is it?", "12.10", ["2.00", "1.10", "12.02"],
                   "The short hand is just past 12, so the hour is 12. The long hand points to 2: 5, 10. "
                   "It is <b>12.10</b>. (2.00 swaps the hands. 12.02 reads the 2 as 2 minutes.)"))
    assert swapped(9, 35) == "7.50"
    its.append(mcq(fig(clock_svg(9, 35)) + "Kavya reads this clock as <b>7.50</b>. What mistake did she make?",
                   "She swapped the hands.", ["She read the next hour.", "She counted in 1s.", "She is right."],
                   "The short hand is between 9 and 10, and the long hand points to 7: 7 jumps of 5 = 35. "
                   "The right time is 9.35. Kavya read the long hand as the hour, so <b>she swapped the hands</b>."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 6, 7, 5, 13, 8, 11, 9, 16, 15, 10, 12, 17, 14, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Telling time to 5 minutes", "items": [its[i] for i in order]}


# ============================================================ set 3: am or pm
def part_of_day(t):
    h = t // 60
    if 5 <= h < 12:
        return "morning"
    if 12 <= h < 18:
        return "afternoon"
    if 18 <= h < 21:
        return "evening"
    return "night"


PARTS = ["morning", "afternoon", "evening", "night"]


def when_item(text, t, why):
    right = part_of_day(t)
    assert right in why
    return mcq(fig(digital_svg(ap(t))) + text, right, [p for p in PARTS if p != right], why)


def ampm_clock(text, t, sky, why, extra=()):
    h, m = divmod(t, 60)
    right = ap(t)
    c = list(extra) + [ap((t + 720) % DAY), ap(t + 60), ap(t - 60)]
    return apmcq(fig(clock_svg(h, m, sky=sky)) + text, right, c, why)


def set_ampm():
    its = []
    its.append(mcq(fig(dayline_svg()) + "Times from 12 midnight to 12 noon are ___ times.", "am",
                   ["pm", "h", "min"],
                   "From 12 midnight to 12 noon is the morning part of the day. These are <b>am</b> times. "
                   "(h and min are for how long something takes.)"))
    its.append(mcq(fig(dayline_svg()) + "Times from 12 noon to 12 midnight are ___ times.", "pm",
                   ["am", "h", "min"],
                   "After 12 noon it is <b>pm</b>: the afternoon, the evening and the night."))
    its.append(ampm_clock("School starts in the <b>morning</b>. What time does school start?", T_(7, 30), "sun",
                          "The clock shows 7.30. School starts in the morning, so it is <b>7.30 am</b>. "
                          "(7.30 pm is in the evening.)"))
    its.append(apmcq(fig(clock_svg(7, 0, sky="moon")) + "Siti eats dinner with her family. What time does she eat dinner?",
                     "7 pm", ["7 am", "12 noon", "7.30 pm"],
                     "The clock shows 7 o’clock. Dinner is in the evening, so it is <b>7 pm</b>. "
                     "(7 am is in the morning, at breakfast time.)"))
    its.append(when_item("Mrs Lim jogs at East Coast Park at this time. When does she jog?", T_(6, 30),
                         "am times are from 12 midnight to 12 noon. 6.30 am is early in the <b>morning</b>."))
    its.append(when_item("School ends at this time. When does school end?", T_(13, 30),
                         "pm times come after 12 noon. 1.30 pm is in the <b>afternoon</b>. "
                         "(Do not mix up am and pm: pm is not the morning.)"))
    its.append(when_item("Jun Jie’s family eats dinner at a hawker centre at this time. When do they eat?", T_(19, 0),
                         "7 pm is after 12 noon and after the afternoon. It is the <b>evening</b>."))
    its.append(when_item("Raju is fast asleep at this time. When is it?", T_(23, 0),
                         "11 pm is late, just before 12 midnight. It is <b>night</b>."))
    its.append(mcq(fig(dayline_svg()) + "Which time is in the <b>afternoon</b>?", "3 pm", ["3 am", "8 am", "11 am"],
                   "Afternoon times come after 12 noon, so they are pm. <b>3 pm</b> is in the afternoon. "
                   "3 am, 8 am and 11 am are all before 12 noon."))
    its.append(mcq(fig(dayline_svg()) + "Which time is in the <b>morning</b>?", "8.30 am",
                   ["8.30 pm", "1.30 pm", "10 pm"],
                   "Morning times are am times. <b>8.30 am</b> is in the morning. The other times are pm."))
    its.append(mcq(fig(sun_icon_svg()) + "Which do you most likely do at <b>7 am</b>?", "eat breakfast",
                   ["eat dinner", "go to bed", "watch the stars"],
                   "7 am is in the morning, before 12 noon. In the morning you <b>eat breakfast</b>. "
                   "(Dinner and bed are pm.)"))
    its.append(mcq(fig(moon_icon_svg()) + "Which do you most likely do at <b>9 pm</b>?", "go to bed",
                   ["eat breakfast", "go to school", "have recess"],
                   "9 pm is late in the evening. At that time you <b>go to bed</b>. "
                   "(Breakfast, school and recess are in the morning, so they are am.)"))
    its.append(ampm_clock("Ali wakes up in the morning. What time does he wake up?", T_(6, 15), "sun",
                          "The clock shows 6.15. He wakes up in the morning, so it is <b>6.15 am</b>.",
                          ["3.30 am"]))
    its.append(ampm_clock("Priya goes to bed at night. What time does she go to bed?", T_(8, 30) + 720, "moon",
                          "The clock shows 8.30. Bedtime is at night, so it is <b>8.30 pm</b>. "
                          "(6.40 pm swaps the hands.)", ["6.40 pm"]))
    its.append(ampm_clock("Mr Tan eats lunch at a hawker centre. What time does he eat lunch?", T_(12, 30), "sun",
                          "The clock shows 12.30. Lunch is just after 12 noon, so it is <b>12.30 pm</b>. "
                          "(12.30 am is in the middle of the night.)"))
    its.append(mcq(fig(clock_svg(10, 0, sky="sun")) + "Recess is in the morning. The clock shows the time. "
                   "Recess is at 10 ___.", "am", ["pm", "h", "min"],
                   "Recess is in the morning, before 12 noon. So it is 10 <b>am</b>. "
                   "(10 h would mean 10 hours long.)"))
    its.append(mcq(fig(sun_icon_svg()) +
                   "It is 12 o’clock in the middle of the day. What do we call this time?", "12 noon",
                   ["12 midnight", "12 min", "12 h"],
                   "12 o’clock in the middle of the day is <b>12 noon</b>. After 12 noon, times are pm. "
                   "(12 midnight is in the middle of the night.)"))
    its.append(mcq(fig(dayline_svg()) + "Which is the <b>earliest</b> time in the day?", "6 am",
                   ["6 pm", "11 am", "2 pm"],
                   "am times come before pm times. Of the am times, 6 am comes before 11 am. So <b>6 am</b> is the earliest. "
                   "(6 pm is in the evening.)"))
    its.append(mcq(fig(pair_svg((12, 30), (7, 0), ("Lunch", "Dinner"))) +
                   "Ahmad eats lunch at <b>12.30 pm</b>. He eats dinner at <b>7 pm</b>. Which meal is later?",
                   "dinner", ["lunch", "They are at the same time.", "You cannot tell."],
                   "Both are pm times. 7 pm comes after 12.30 pm, so <b>dinner</b> is later. "
                   "(The number 12 is bigger than 7, but 12.30 pm is just after 12 noon.)"))
    its.append(mcq(fig(dayline_svg(T_(16, 0))) + "The red arrow shows a time on the day line. Which time can it be?",
                   "4 pm", ["4 am", "10 am", "11 pm"],
                   "The arrow is after 12 noon, in the pm part, in the afternoon. So it can be <b>4 pm</b>. "
                   "(4 am is in the am part, before 12 noon.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 15, 8, 9, 12, 13, 14, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "am or pm", "items": [its[i] for i in order]}


def sun_icon_svg():
    return svg_wrap(60, 60, sun_icon(30, 30, 14), "sun")


def moon_icon_svg():
    return svg_wrap(60, 60, moon_icon(26, 30, 18), "moon")


# ============================================================ set 4: 1 hour later, half an hour later
def fmt(t):
    h, m = divmod(t % DAY, 60)
    return oc(h) if m == 0 else rd(h, m)


def later(h, m, d, back=False):
    t = h * 60 + m
    r = t - d if back else t + d
    right = fmt(r)
    sg = -1 if back else 1
    other = 30 if d == 60 else 60
    c = [fmt(t + sg * other),                        # mixed up 1 h and half an hour
         fmt(t - sg * d)]                            # counted the wrong way
    if d == 60:
        c += [fmt(t + sg * 120), rd(h, m - 1) if back and m else rd(h, m + 1) if not back else None]  # 2 h / changed the minutes by 1
    else:
        c += [fmt(t + sg * 50), fmt(t + sg * 15)]    # half an hour taken as 50 min / as 15 min
    word = "1 hour" if d == 60 else "half an hour"
    if d == 60:
        e = ("1 hour is 60 min. The long hand goes once around and comes back to the same place. "
             "The hour goes %s by 1: %s %s 1 h = <b>%s</b>." % ("down" if back else "up", fmt(t), "−" if back else "+", right))
    else:
        e = "Half an hour is 30 min. The long hand goes half way around. "
        if not back and m + 30 >= 60 and m + 30 != 60:
            e += ("Count on %d min to %s. Then %d min more makes <b>%s</b>."
                  % (60 - m, fmt(t + 60 - m), m + 30 - 60, right))
        else:
            e += "%s %s 30 min = <b>%s</b>." % (fmt(t), "−" if back else "+", right)
    q = fig(clock_svg(h, m)) + ("What time was it <b>%s earlier</b>?" % word if back else
                                "What time will it be <b>%s later</b>?" % word)
    return mcq(q, right, c, e)


def bars_svg():
    sc = 4.0
    x0 = 80
    s = []
    for i, (v, lab, name) in enumerate([(60, "60 min", "1 h"), (30, "", "30 min")]):
        y = 8 + i * 46
        s.append(T(8, y + 23, name, 16, INK, "start"))
        s.append("<rect x='%d' y='%d' width='%.1f' height='34' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, v * sc, FILL, GREEN))
        if lab:
            s.append(T(x0 + v * sc / 2, y + 23, lab, 15, INK))
    return svg_wrap(x0 + 60 * sc + 8, 96, "".join(s), "bars 1 h and 30 min")


def set_later():
    its = []
    its.append(mcq(fig(ring_clock_svg(3, 0, arc=(0, 60))) + "The long hand goes once around the clock. "
                   "How long does it take?", "1 h", ["30 min", "12 min", "1 min"],
                   "Once around the clock is 60 minutes. 60 min = <b>1 h</b>. (12 min counts the numbers, not the minutes.)"))
    its.append(mcq(fig(ring_clock_svg(3, 30, arc=(0, 30))) + "The long hand goes half way around the clock. "
                   "How long does it take?", "30 min", ["1 h", "6 min", "50 min"],
                   "Half way around is from 12 to 6. That is <b>30 min</b>, which is half an hour. "
                   "(6 min reads the number 6. 50 min thinks half of 100.)"))
    its.append(mcq(fig(ring_clock_svg(3, 0, arc=(0, 60))) + "1 h = ___ min", "60", ["100", "30", "12"],
                   "In 1 hour, the long hand goes once around: 60 minutes. So 1 h = <b>60</b> min. "
                   "(Not 100: time does not count in hundreds.)"))
    its.append(mcq(fig(ring_clock_svg(3, 30, arc=(0, 30))) + "Half an hour = ___ min", "30", ["50", "15", "60"],
                   "1 hour is 60 min. Half of 60 is <b>30</b>. (Not 50: 1 hour is 60 min, not 100.)"))
    its.append(mcq("What does <b>h</b> stand for?", "hour", ["minute", "half", "hand"],
                   "<b>h</b> is short for <b>hour</b>. <b>min</b> is short for minute."))
    its.append(mcq("What does <b>min</b> stand for?", "minute", ["hour", "morning", "midnight"],
                   "<b>min</b> is short for <b>minute</b>. 30 min is half an hour."))
    its.append(mcq(fig(moon_icon_svg()) + "Ali sleeps for 10 ___ every night.", "h", ["min", "am", "pm"],
                   "Sleep at night is long, so we use hours: 10 <b>h</b>. 10 min is far too short. "
                   "(am and pm tell the time of day, not how long.)"))
    its.append(mcq(fig(sun_icon_svg()) + "Siti brushes her teeth for 2 ___.", "min", ["h", "am", "pm"],
                   "Brushing teeth is short, so we use minutes: 2 <b>min</b>. 2 h would be far too long."))
    its.append(mcq(fig(bars_svg()) + "Which is <b>longer</b>: 1 h or 30 min?",
                   "1 h", ["30 min", "They are the same.", "You cannot tell."],
                   "1 h = 60 min. 60 min is longer than 30 min, so <b>1 h</b> is longer. "
                   "(30 is a bigger number than 1, but the units are different.)"))
    its.append(later(4, 0, 60))
    its.append(later(2, 30, 30))
    its.append(later(7, 15, 60))
    its.append(later(10, 0, 30))
    its.append(later(5, 30, 60, back=True))
    its.append(later(9, 40, 30))
    its.append(later(11, 45, 30, back=True))
    for t1, t2, right, wrong, e in [
            ((3, 0), (4, 0), "1 h", ["30 min", "4 h", "2 h"],
             "From 3 o’clock to 4 o’clock, the long hand goes once around. That is <b>1 h</b>. "
             "(4 h just reads the end clock.)"),
            ((8, 30), (9, 0), "30 min", ["1 h", "9 min", "2 h"],
             "From 8.30 to 9 o’clock, the long hand goes from 6 to 12: half way around. That is <b>30 min</b>."),
            ((10, 15), (10, 45), "30 min", ["45 min", "1 h", "15 min"],
             "The long hand goes from 3 to 9, half way around. 10.15 to 10.45 is <b>30 min</b>. "
             "(45 min reads the end time.)"),
            ((5, 40), (6, 40), "1 h", ["40 min", "30 min", "7 h"],
             "The long hand is at 8 on both clocks, so it went once around. The hour went from 5 to 6. That is <b>1 h</b>. "
             "(40 min reads the minutes.)")]:
        its.append(mcq(fig(pair_svg(t1, t2)) + "How long is it from the start to the end?", right, wrong, e))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 11, 12, 13, 18, 14, 15, 19]
    assert sorted(order) == list(range(20))
    return {"title": "1 hour later and half an hour later", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def wp_on(text, t, d, sky, extra=()):
    """start time t (minutes), duration d (30 or 60): finish time"""
    h, m = divmod(t, 60)
    r = t + d
    other = 30 if d == 60 else 60
    c = list(extra) + [ap(t + other), ap(t - d), ap((r + 720) % DAY), ap(r + 60)]
    word = "1 h" if d == 60 else "half an hour (30 min)"
    e = "The clock shows %s. Count on %s: %s → <b>%s</b>." % (ap(t), word, ap(t), ap(r))
    if (t < 720) != (r < 720):
        e += " After 12 noon the time is pm."
    elif r < 720:
        e += " It is still before 12 noon, so it is am."
    else:
        e += " It is after 12 noon, so it is pm."
    return apmcq(fig(clock_svg(h, m, sky=sky)) + text, ap(r), c, e)


def wp_back(text, t, d, sky, extra=()):
    h, m = divmod(t, 60)
    r = t - d
    other = 30 if d == 60 else 60
    c = list(extra) + [ap(t + d), ap(t - other), ap((r + 720) % DAY), ap(t + other)]
    word = "1 h" if d == 60 else "half an hour (30 min)"
    e = ("Count <b>back</b> %s from %s: <b>%s</b>. (%s counts on instead of back.)"
         % (word, ap(t), ap(r), ap(t + d)))
    return apmcq(fig(clock_svg(h, m, sky=sky)) + text, ap(r), c, e)


def set_words():
    its = []
    its.append(wp_on("Recess starts in the morning at the time on the clock. It lasts <b>half an hour</b>. When does recess end?",
                     T_(10, 0), 30, "sun"))
    its.append(wp_on("Siti’s swimming lesson starts at <b>4 pm</b>. It lasts <b>1 h</b>. When does it end?",
                     T_(16, 0), 60, "sun"))
    its.append(wp_on("A movie starts at <b>7 pm</b>. It ends <b>1 h</b> later. When does the movie end?",
                     T_(19, 0), 60, "moon"))
    its.append(mcq(fig(clock_svg(7, 20, sky="sun")) + "School starts at <b>7.30 am</b>. The clock shows when Wei Ming "
                   "reaches school. Is he early or late?", "early", ["late", "on time", "You cannot tell."],
                   "The clock shows 7.20 am. 7.20 comes before 7.30, so Wei Ming is <b>early</b>, by 10 min."))
    its.append(wp_on("Ali gets on the school bus in the morning at the time on the clock. The ride takes <b>half an hour</b>. "
                     "When does he reach school?", T_(6, 45), 30, "sun"))
    its.append(mcq(fig(pair_svg((8, 0), (8, 30))) + "Mei Ling reads a book from <b>8 pm</b> to <b>8.30 pm</b>. "
                   "How long does she read?", "30 min", ["1 h", "8 min", "30 h"],
                   "From 8 pm to 8.30 pm, the long hand goes from 12 to 6. That is <b>30 min</b>, half an hour. "
                   "(30 h would be more than a whole day.)"))
    its.append(wp_on("Mdm Wong puts a cake in the oven in the afternoon at the time on the clock. It bakes for <b>1 h</b>. "
                     "When is the cake ready?", T_(14, 15), 60, "sun"))
    its.append(ampm_clock("Jun Jie’s family eats dinner at a hawker centre at the time on the clock. "
                          "What time do they eat?", T_(18, 55), "moon",
                          "The short hand is close to 7 but has not reached it, so the hour is 6. "
                          "The long hand points to 11: 55 min. Dinner is in the evening, so it is <b>6.55 pm</b>. "
                          "(7.55 pm reads the next hour.)", ["7.55 pm"]))
    its.append(mcq(fig(pair_svg((6, 15), (6, 40), ("Raju", "Priya"))) + "The clocks show when Raju and Priya wake up "
                   "in the morning. Who wakes up earlier?", "Raju",
                   ["Priya", "They wake up at the same time.", "You cannot tell."],
                   "Raju wakes up at 6.15 am. Priya wakes up at 6.40 am. 6.15 comes before 6.40, so <b>Raju</b> "
                   "wakes up earlier."))
    its.append(wp_back("The library opens in the morning at the time on the clock. Hui Min reaches the library <b>half an hour "
                       "before</b> it opens. When does she reach the library?", T_(10, 0), 30, "sun"))
    its.append(wp_on("Mr Tan gets on the MRT in the afternoon at the time on the clock. The ride takes <b>half an hour</b>. "
                     "When does he get off?", T_(17, 20), 30, "sun"))
    its.append(mcq(fig(pair_svg((4, 30), (5, 30))) + "Kumar plays at the void deck from <b>4.30 pm</b> to "
                   "<b>5.30 pm</b>. How long does he play?", "1 h", ["30 min", "5 h", "2 h"],
                   "The long hand is at 6 on both clocks, so it went once around. 4.30 pm to 5.30 pm is <b>1 h</b>. "
                   "(5 h reads the hour on the end clock.)"))
    its.append(wp_back("Chloe’s piano lesson is <b>half an hour</b> long. It ends in the afternoon at the time on the clock. "
                       "When does it start?", T_(15, 30), 30, "sun"))
    its.append(mcq(fig(moon_icon_svg()) + "Farah goes to bed at <b>9 pm</b>. Her little brother goes to bed "
                   "<b>1 h earlier</b>. When does he go to bed?", "8 pm", ["10 pm", "8 am", "8.30 pm"],
                   "1 h earlier than 9 pm: count back 1 hour. 9 pm → <b>8 pm</b>. "
                   "(10 pm is 1 h later. 8.30 pm is only half an hour earlier.)"))
    its.append(mcq(fig(ring_clock_svg(5, 0, arc=(0, 60))) + "Hafiz watches TV for <b>half an hour</b>. Then he does "
                   "his homework for <b>half an hour</b>. How long is that altogether?", "1 h",
                   ["30 min", "2 h", "1 h 30 min"],
                   "Half an hour + half an hour = 30 min + 30 min = 60 min = <b>1 h</b>. "
                   "(30 min counts only one half hour.)"))
    its.append(wp_on("Ethan’s family watches a show at the Singapore Zoo. It starts in the morning at "
                     "the time on the clock. It lasts <b>half an hour</b>. When does the show end?", T_(11, 40), 30, "sun"))
    its.append(wp_on("Sarah’s football training starts in the afternoon at the time on the clock. It lasts "
                     "<b>1 h</b>. When does it end?", T_(16, 10), 60, "sun"))
    its.append(mcq(fig(clock_svg(7, 15, sky="sun")) + "A bus comes every <b>half an hour</b>. One bus comes in the morning at "
                   "the time on the clock. When does the next bus come?", "7.45 am",
                   ["8.15 am", "7.30 am", "6.45 am"],
                   "The clock shows 7.15 am. Half an hour is 30 min. 7.15 am + 30 min = <b>7.45 am</b>. "
                   "(8.15 am is 1 h later. 7.30 am is only 15 min later.)"))
    its.append(wp_on("School ends in the afternoon at the time on the clock. Xin Yi’s mother picks her up <b>1 h</b> later. "
                     "When does her mother pick her up?", T_(13, 30), 60, "sun"))
    its.append(mcq(fig(pair_svg((7, 0), (7, 30), ("Leave home", "School starts"))) +
                   "Devi leaves home at <b>7 am</b>. Her walk to school takes <b>half an hour</b>. "
                   "School starts at <b>7.30 am</b>. When does Devi reach school?", "just as school starts",
                   ["half an hour early", "1 h late", "half an hour late"],
                   "7 am + 30 min = 7.30 am. School starts at 7.30 am, so Devi reaches school <b>just as school starts</b>."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 5, 4, 6, 8, 7, 9, 11, 10, 13, 12, 14, 17, 15, 16, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Time word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>A clock has two hands. The <b>short hand</b> shows the hour. The <b>long hand</b> shows the minutes. "
        "When the long hand points to <b>12</b>, it is o’clock. When it points to <b>6</b>, it is half past.</p>"
        "<figure class='sn-fig'>" + pair_svg((3, 0), (3, 30), ("3 o’clock", "half past 3")) +
        "<figcaption>At half past 3, the short hand is half way between 3 and 4. We write half past 3 as <b>3.30</b>."
        "</figcaption></figure>"
        "<h2>Telling time to 5 minutes</h2>"
        "<p>Look at the short hand first. It gives the hour it has <b>passed</b>. Then count the long hand in 5s: "
        "each number is 5 more minutes.</p>"
        "<figure class='sn-fig'>" + ring_clock_svg(3, 25) +
        "<figcaption>The short hand is between 3 and 4, so the hour is 3. The long hand points to 5: "
        "5, 10, 15, 20, 25. It is <b>3.25</b>.</figcaption></figure>"
        + ex("Read the clock", "The short hand is between 7 and 8. The long hand points to 10. What time is it?",
             "The hour is 7. Count in 5s ten times: 5, 10, 15, … 50.", "7.50") +
        "<h2>am and pm</h2>"
        "<p>From 12 midnight to 12 noon, times are <b>am</b>. From 12 noon to 12 midnight, times are <b>pm</b>. "
        "School starts at 7.30 am. Dinner is at 7 pm.</p>"
        "<figure class='sn-fig'>" + dayline_svg() +
        "<figcaption>The morning is am. The afternoon, the evening and the night are pm.</figcaption></figure>"
        "<h2>1 hour later and half an hour later</h2>"
        "<p>We write hours as <b>h</b> and minutes as <b>min</b>. 1 h = 60 min. Half an hour = 30 min. "
        "In 1 hour, the long hand goes once around. In half an hour, it goes half way around.</p>"
        + table(["Now", "Half an hour later", "1 hour later"],
                [["4 o’clock", "4.30", "5 o’clock"], ["2.30", "3 o’clock", "3.30"], ["7.15", "7.45", "8.15"]])
        + ex("Word problem", "Recess starts at 10 am. It lasts half an hour. When does it end?",
             "Count on 30 min from 10 am.", "10.30 am") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3.25 read as 5.15", "Do not swap the hands. The short hand shows the hour."],
            ["3.25 read as 3.05", "The long hand on 5 means 25 min. Count in 5s."],
            ["7.50 read as 8.50", "The short hand is near 8 but has not passed it. The hour is 7."],
            ["Dinner at 7 am", "After 12 noon, times are pm. Dinner is at 7 pm."],
            ["Half an hour = 50 min", "1 h = 60 min, so half an hour = 30 min."],
        ])
    )


FAQ = [
    {"q": "What do P1 students learn about time?",
     "a": "In Primary 1, students tell the time to 5 minutes, use am and pm, write hours as h and minutes as min, and find the time 1 hour or half an hour later."},
    {"q": "How do I teach my child to tell the time to 5 minutes?",
     "a": "Read the short hand first for the hour it has passed, then count the long hand in 5s. If the long hand points to 5, it is 25 minutes past, so 3.25."},
    {"q": "What is the most common mistake when reading a clock?",
     "a": "Swapping the two hands, for example reading 3.25 as 5.15. Remind your child that the short hand always shows the hour."},
    {"q": "Is telling time in the P1 MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus teaches telling time to 5 minutes, am and pm, and durations of one hour and half an hour in Primary 1."},
]


def gen():
    rnd = random.Random(61809)
    sets = [set_oclock(), set_five(), set_ampm(), set_later(), set_words()]
    balance(sets, rnd)
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
        assert sorted(it["a"] for it in s["items"]) == [p for p in range(4) for _ in range(5)], s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
    qs = [it["q"] for s in sets for it in s["items"]]
    dup = [q for q in qs if qs.count(q) > 1]
    assert not dup, [re.sub("<svg.*?</svg>", "[svg]", q) for q in dup]
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-1", "slug": "time", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 1 Time: Telling Time, am and pm",
        "seo_title": "P1 Time Worksheets: Free Primary 1 Maths on Telling Time, am and pm with Answers (MOE Syllabus)",
        "short_title": "Time",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 1: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Telling time to 5 minutes; use of am and pm; use of h and min; duration of one hour/half hour",
        "meta_desc": "Free P1 maths practice on time: o’clock, half past, telling time to 5 minutes, am and pm, and 1 hour or half an hour later. 100 questions with answers.",
        "key_big": "The short hand shows the hour. Count the long hand in 5s for the minutes.",
        "key_sub": "Short hand between 3 and 4, long hand on 5: 5, 10, 15, 20, 25, so it is 3.25.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    for p in ("two clocks", "clock choices", "day line", "bars"):
        mark_large(u, p)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
