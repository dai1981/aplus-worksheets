# -*- coding: utf-8 -*-
"""
Singapore Primary 3 Maths: Time (MOE 2021 Primary Mathematics Syllabus, Measurement)
"Measuring time in seconds; finding the starting time, finishing time or duration; 24-hour clock"
  python3 tools/gen_sg_maths_p3_time.py
Seconds, minutes and hours (choosing the unit, 1 min = 60 s, 1 h = 60 min), durations on time lines,
start or finish time given the duration, the 24-hour clock (7.30 pm = 1930) and Singapore word problems
with bar models. Every analog clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real mistakes: 1 h counted as 100 min,
subtracting times like ordinary numbers, 1930 read as 9.30 pm, am and pm mixed up when crossing 12 noon,
forgetting to rename 60 min as 1 h, counting forwards instead of backwards.
Helpers adapted from gen_cabc_math_g3_time.py, gen_cabc_math_g4_time.py and gen_sg_maths_p4_division.py.
Singapore English: times 7.30 am, 12 noon, 12 midnight; 24-hour times 0730, 1930; durations 1 h 15 min, 40 s.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-3")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
LINE = "#2b2b2b"
INK = "#2b2b2b"
RED = "#c0392b"
SOFT = "#eef5f0"
FONT = "Arial, Helvetica, sans-serif"
NBSP = " "
DAY = 24 * 60


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def tm(t):
    """12-hour Singapore time from minutes after midnight: 7.30 am, 12 noon, 12 midnight, 12.15 pm"""
    t %= DAY
    h, m = divmod(t, 60)
    if t == 12 * 60:
        return "12 noon"
    if t == 0:
        return "12 midnight"
    return "%d.%02d %s" % (h12(h), m, "am" if h < 12 else "pm")


def T_(h, m):
    return h * 60 + m


def t24(t):
    t %= DAY
    return "%02d%02d" % divmod(t, 60)


def dur(n):
    assert n > 0, n
    hh, mm = divmod(n, 60)
    if hh and mm:
        return "%d h %d min" % (hh, mm)
    if hh:
        return "%d h" % hh
    return "%d min" % mm


def dsec(n):
    assert n > 0, n
    mm, ss = divmod(n, 60)
    if mm and ss:
        return "%d min %d s" % (mm, ss)
    if mm:
        return "%d min" % mm
    return "%d s" % ss


def dval(s):
    """value in seconds of '1 h 20 min', '2 min 5 s', '85 min'"""
    v = 0
    for n, u in re.findall(r"(\d+) (h|min|s)\b", s):
        v += int(n) * {"h": 3600, "min": 60, "s": 1}[u]
    assert v > 0, s
    return v


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


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


def dmcq(q, correct, cands, e):
    return mcq(q, correct, cands, e, key=dval)


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


# ------------------------------------------------------------ clocks
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


def dial_numbers(cx, cy, R, k, labels):
    fs = max(19 * k, 15)
    rn = R - 29 * k
    s = ["<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
         "paint-order='stroke'>" % (fs, LINE, 3.5 * k)]
    for i, lab in enumerate(labels):
        a = math.radians((i + 1) * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, lab))
    s.append("</g>")
    return s


def clock_body(h, m, size, ox=0.0, oy=0.0):
    """Analog clock face. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
    R = size / 2.0 - 6
    cx, cy = ox + size / 2.0, oy + size / 2.0
    k = R / 94.0
    s = face(cx, cy, R, k)
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians(m * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.48 * math.cos(ah), cy + R * 0.48 * math.sin(ah), LINE, 8 * k))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.82 * math.cos(am), cy + R * 0.82 * math.sin(am), RED, 4.5 * k))
    s += dial_numbers(cx, cy, R, k, [str(n) for n in range(1, 13)])
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring24=False):
    if not ring24:
        return svg_wrap(size, size, clock_body(h, m, size), "analog clock")
    pad = 30
    W = size + 2 * pad
    c = W / 2.0
    R = size / 2.0 - 6
    s = [clock_body(h, m, size, pad, pad),
         "<g font-size='17' font-weight='700' fill='%s' text-anchor='middle'>" % GREEN]
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        r2 = R + 19
        s.append("<text x='%.1f' y='%.1f'>%s</text>" % (c + r2 * math.cos(a), c + r2 * math.sin(a) + 6,
                                                       "00" if n == 12 else str(n + 12)))
    s.append("</g>")
    return svg_wrap(W, W, "".join(s), "analog clock with 24-hour numbers")


def start_end_svg(h1, m1, h2, m2, labels=("Start", "End"), size=180):
    gap, top = 14, 30
    W = 2 * size + gap
    s = []
    for i, (h, m) in enumerate([(h1, m1), (h2, m2)]):
        x = i * (size + gap)
        s.append(T(x + size / 2.0, 22, labels[i], 20, GREEN))
        s.append(clock_body(h, m, size, x, top))
    return svg_wrap(W, size + top, "".join(s), "start and end clocks")


def digital_svg(text):
    W, H = 200, 84
    s = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='#fff' stroke='%s' stroke-width='4'/>" % (W - 6, H - 6, GREEN),
         "<rect x='16' y='14' width='%d' height='%d' rx='6' fill='%s'/>" % (W - 32, H - 28, SOFT),
         "<text x='%d' y='%d' font-size='40' font-weight='700' fill='%s' text-anchor='middle' "
         "font-family='Consolas, Menlo, monospace'>%s</text>" % (W / 2, H / 2 + 14, LINE, text)]
    return svg_wrap(W, H, "".join(s), "digital clock")


def stopwatch_svg(sec, size=200):
    """Stopwatch dial: 60 seconds once around, numbers 5 to 60, one red hand."""
    assert 0 < sec < 60
    top = 22
    R = size / 2.0 - 6
    cx, cy = size / 2.0, top + size / 2.0
    k = R / 94.0
    s = ["<rect x='%.1f' y='2' width='24' height='%d' rx='4' fill='%s'/>" % (cx - 12, top + 4, GREEN)]
    s += face(cx, cy, R, k)
    a = math.radians(sec * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + R * 0.84 * math.cos(a), cy + R * 0.84 * math.sin(a), RED, 4.5 * k))
    s += dial_numbers(cx, cy, R, k, [str(5 * n) for n in range(1, 13)])
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    s.append(T(cx, cy - R * 0.30, "seconds", 15, GREEN, weight="400"))
    return svg_wrap(size, size + top, "".join(s), "stopwatch")


# ------------------------------------------------------------ time lines
def jumps_of(t1, t2):
    """Time-line method: to the next o'clock, then whole hours, then the minutes left."""
    pts = [t1]
    cur = t1
    if cur % 60 and cur + (60 - cur % 60) <= t2:
        cur += 60 - cur % 60
        pts.append(cur)
    if t2 - cur >= 60:
        cur += (t2 - cur) // 60 * 60
        pts.append(cur)
    if cur < t2:
        pts.append(t2)
    assert pts[-1] == t2 and len(pts) >= 2
    return pts


def timeline_svg(pts, labels, jumps, W=440):
    """pts: minutes (may pass midnight); labels: text under each point; jumps: text over each arc ('?' in red)."""
    n = len(pts) - 1
    L, R, Y = 52, W - 52, 74
    span = R - L
    minw = 108
    assert n * minw <= span, pts
    raw = [b - a for a, b in zip(pts, pts[1:])]
    assert all(r > 0 for r in raw)
    extra = span - n * minw
    xs = [L]
    for r in raw:
        xs.append(xs[-1] + minw + extra * r / float(sum(raw)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L - 14, Y, R + 14, Y, LINE)]
    for i, x in enumerate(xs):
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, Y - 10, x, Y + 10, LINE))
        s.append(T(x, Y + 32, labels[i], 16, RED if labels[i] == "?" else LINE))
    for i in range(n):
        wa, wb = tw(labels[i], 16), tw(labels[i + 1], 16)
        assert xs[i + 1] - xs[i] >= (wa + wb) / 2 + 6, labels
        assert tw(jumps[i], 14) + 6 <= xs[i + 1] - xs[i], jumps
    assert xs[0] - tw(labels[0], 16) / 2 >= 2 and xs[-1] + tw(labels[-1], 16) / 2 <= W - 2, labels
    for i in range(n):
        x1, x2 = xs[i], xs[i + 1]
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1 + 3, Y - 12, (x1 + x2) / 2, Y - 50, x2 - 3, Y - 12, GREEN))
        s.append(T((x1 + x2) / 2, Y - 38, jumps[i], 14, RED if jumps[i] == "?" else GREEN))
    return svg_wrap(W, 116, "".join(s), "time line")


def line_between(t1, t2, show=True):
    pts = jumps_of(t1, t2)
    labels = [tm(p) for p in pts]
    jumps = [("+" + dur(b - a)) if show else "?" for a, b in zip(pts, pts[1:])]
    return fig(timeline_svg(pts, labels, jumps))


def line_finish(t, d, back=False):
    """Start (or finish) given, one jump of d, the other end '?'."""
    if back:
        return fig(timeline_svg([t - d, t], ["?", tm(t)], ["\u2212" + dur(d)]))
    return fig(timeline_svg([t, t + d], [tm(t), "?"], ["+" + dur(d)]))


def steps_text(t1, t2):
    pts = jumps_of(t1, t2)
    parts = ["%s to %s is %s." % (tm(a), tm(b), dur(b - a)) for a, b in zip(pts, pts[1:])]
    if len(pts) > 2:
        mins_ = [b - a for a, b in zip(pts, pts[1:])]
        tot = t2 - t1
        sm = " + ".join(dur(x) for x in mins_)
        parts.append("%s = <b>%s</b>." % (sm, dur(tot)))
    else:
        parts[-1] = parts[-1][:-1].rsplit(" is ", 1)[0] + " is <b>%s</b>." % dur(t2 - t1)
    return " ".join(parts)


def naive(t1, t2):
    """Subtracting the clock numbers as if 1 h = 100 min: 9.05 − 7.15 = 1.90"""
    a = h12(t1 // 60 % 24) * 100 + t1 % 60
    b = h12(t2 // 60 % 24) * 100 + t2 % 60
    v = b - a
    if v <= 0:
        return None
    hh, mm = divmod(v, 100)
    if hh and mm:
        return "%d h %d min" % (hh, mm)
    if hh:
        return None
    return "%d min" % mm


# ------------------------------------------------------------ bar models
SEGFILL = {"u": FILL, "o": "#e3e3e3", "w": "#ffffff"}


def model_svg(rows, top=None, right=None, BW=320, label="bar model"):
    """Bar model drawn to scale. rows: [(name, [(value, text, style)])]; top: (v0, v1, text) over row 0;
    right: text for a bracket on the right joining all rows. '?' is red."""
    names = [n for n, _ in rows]
    nw = max([tw(n, 15) for n in names] + [0])
    x0 = 8 + (nw + 10 if nw else 0)
    maxv = max(sum(v for v, _, _ in segs) for _, segs in rows)
    sc = BW / float(maxv)
    bh = 34
    out = []
    y = 38 if top else 8
    ys = []
    for n, segs in rows:
        ys.append(y)
        y += bh + 16
    Hh = y - 16 + 8

    def col(t):
        return RED if t == "?" else INK

    for i, (n, segs) in enumerate(rows):
        ry = ys[i]
        if n:
            out.append(T(8, ry + 23, n, 15, INK, "start"))
        x = x0
        for v, t, st in segs:
            w = v * sc
            out.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                       % (x, ry, w, bh, SEGFILL[st], GREEN))
            if t:
                assert tw(t, 15) + 4 <= w, (t, w)
                out.append(T(x + w / 2, ry + 23, t, 15, col(t)))
            x += w
    if top:
        v0, v1, t = top
        a, b = x0 + v0 * sc, x0 + v1 * sc
        ry = ys[0]
        out.append("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>" % (a, ry - 4, ry - 11, b, ry - 4, INK))
        out.append(T((a + b) / 2, ry - 16, t, 16, col(t)))
    W = x0 + BW + 8
    if right:
        xr = x0 + BW + 8
        y0, y1 = ys[0], ys[-1] + bh
        out.append("<path d='M%.1f %d H%.1f V%d H%.1f' fill='none' stroke='%s' stroke-width='2'/>" % (xr, y0, xr + 8, y1, xr, INK))
        out.append(T(xr + 14, (y0 + y1) / 2 + 6, right, 16, col(right), "start"))
        W = xr + 14 + tw(right, 16) + 8
    return svg_wrap(W, Hh, "".join(out), label)


# ------------------------------------------------------------ lesson helpers
def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5)."""
    for s in sets:
        targets = [p for p in range(4) for _ in range(5)]
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
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


# ============================================================ set 1: seconds, minutes and hours
def set_units():
    its = []
    its.append(mcq("How many <b>seconds</b> are in 1 minute?", "60", ["100", "10", "30"],
                   "1 min = <b>60 s</b>. The second hand goes once around the clock in 1 minute. "
                   "(Not 100: time does not count in hundreds.)"))
    its.append(mcq("How many <b>minutes</b> are in 1 hour?", "60", ["100", "24", "30"],
                   "1 h = <b>60 min</b>. The minute hand goes once around the clock in 1 hour. "
                   "(Not 100: an hour is not like a hundred.)"))
    for thing, right, why in [("to blink your eyes", "seconds", "A blink is over very fast"),
                              ("to brush your teeth", "minutes", "Brushing your teeth takes a few minutes"),
                              ("to sleep at night", "hours", "You sleep from night until the morning")]:
        its.append(mcq("Which unit is best to measure the time taken %s?" % thing, right,
                       [u for u in ["seconds", "minutes", "hours", "days"] if u != right],
                       "%s, so we use <b>%s</b>." % (why, right)))
    for q, right, wrong, e in [
            ("Ali runs 100 m on Sports Day. About how long does he take?", "20 s", ["20 min", "20 h", "2 h"],
             "A 100 m race is over in a short time, so it takes seconds: <b>20 s</b>. 20 min is far too long for 100 m."),
            ("Mei Ling walks from the void deck of her HDB block to the MRT station. About how long does it take?",
             "10 min", ["10 s", "10 h", "100 min"],
             "A short walk takes minutes, not seconds or hours: <b>10 min</b>. (100 min is more than 1 h 30 min.)"),
            ("A movie at the cinema lasts about ___.", "2 h", ["2 min", "2 s", "20 h"],
             "A movie lasts a few hours: <b>2 h</b>. 2 min is far too short and 20 h is almost a whole day.")]:
        its.append(mcq(q, right, wrong, e))
    its.append(mcq(fig(stopwatch_svg(25)) + "The stopwatch started at 0. How many <b>seconds</b> does it show?",
                   "25 s", ["5 s", "30 s", "20 s"],
                   "The numbers on a stopwatch count in 5s. The hand points to <b>25</b>, so it shows <b>25 s</b>. "
                   "(Not 5 s: on a clock the 5 is in that place, but this dial counts seconds.)"))
    its.append(mcq(fig(stopwatch_svg(42)) + "The stopwatch started at 0. How many <b>seconds</b> does it show?",
                   "42 s", ["41 s", "43 s", "32 s"],
                   "The hand is 2 small marks past the 40. Count 40, then 41, 42: <b>42 s</b>. "
                   "(Each small mark is 1 s.)"))
    its.append(mcq("<b>2 h</b> = ? min", "120", ["200", "62", "102"],
                   "1 h = 60 min. 2 h = 2 × 60 = <b>120 min</b>. (Not 200: 1 h is 60 min, not 100.)"))
    its.append(mcq("<b>3 min</b> = ? s", "180", ["300", "63", "120"],
                   "1 min = 60 s. 3 min = 3 × 60 = <b>180 s</b>. (Not 300: 1 min is 60 s, not 100.)"))
    its.append(mcq("<b>1 h 20 min</b> = ? min", "80", ["120", "21", "70"],
                   "1 h = 60 min. 60 + 20 = <b>80 min</b>. (120 counts 1 h as 100 min.)"))
    its.append(mcq("<b>1 min 15 s</b> = ? s", "75", ["115", "16", "45"],
                   "1 min = 60 s. 60 + 15 = <b>75 s</b>. (115 counts 1 min as 100 s.)"))
    its.append(mcq("<b>2 h 30 min</b> = ? min", "150", ["230", "90", "32"],
                   "2 h = 2 × 60 = 120 min. 120 + 30 = <b>150 min</b>. (90 counts only 1 h. 230 counts 1 h as 100 min.)"))
    its.append(dmcq("<b>90 min</b> = ? h ? min", "1 h 30 min", ["1 h 10 min", "9 h", "1 h 90 min"],
                    "60 min make 1 h. 90 − 60 = 30 min left. So 90 min = <b>1 h 30 min</b>. "
                    "(1 h 10 min would be 70 min.)"))
    its.append(dmcq("<b>150 s</b> = ? min ? s", "2 min 30 s", ["1 min 50 s", "15 min", "1 min 30 s"],
                    "60 s make 1 min. 150 = 60 + 60 + 30, so 150 s = <b>2 min 30 s</b>. "
                    "(1 min 50 s counts 1 min as 100 s.)"))
    its.append(dmcq("<b>135 min</b> = ? h ? min", "2 h 15 min", ["1 h 35 min", "13 h 5 min", "2 h 35 min"],
                    "2 h = 120 min. 135 − 120 = 15 min left. So 135 min = <b>2 h 15 min</b>. "
                    "(1 h 35 min counts 1 h as 100 min.)"))
    its.append(mcq("Which is <b>longer</b>: 100 s or 2 min?", "2 min",
                   ["100 s", "They are the same.", "You cannot tell."],
                   "2 min = 2 × 60 = 120 s. 120 s is more than 100 s, so <b>2 min</b> is longer. "
                   "(1 min is 60 s, not 100 s.)"))
    its.append(mcq("Siti swims one length of the pool in <b>95 s</b>. Ali takes <b>1 min 40 s</b>. "
                   "Who takes longer, and by how much?", "Ali, by 5 s",
                   ["Ali, by 45 s", "Siti, by 5 s", "Siti, by 55 s"],
                   "1 min 40 s = 60 + 40 = 100 s. 100 − 95 = 5. So <b>Ali</b> takes longer, by <b>5 s</b>. "
                   "(Ali, by 45 s counts 1 min as 100 s. Siti, by 55 s forgets Ali’s 1 min.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 8, 9, 10, 11, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Seconds, minutes and hours", "items": [its[i] for i in order]}


# ============================================================ set 2: durations on time lines
def how_long(text, t1, t2, figure=None, extra=(), note=""):
    if t2 <= t1:
        t2 += DAY
    d = t2 - t1
    h1, m1 = divmod(t1 % DAY, 60)
    h2, m2 = divmod(t2 % DAY, 60)
    if figure == "clocks":
        f = fig(start_end_svg(h1, m1, h2, m2))
    elif figure == "line":
        f = line_between(t1, t2, True)
    elif figure == "line?":
        f = line_between(t1, t2, False)
    else:
        f = ""
    nv = naive(t1, t2)
    c = list(extra)
    if nv and dval(nv) != d * 60:
        c.append(nv)
    if m2 < m1 and t2 < DAY and h2 > h1:
        c.append(dur((h2 - h1) * 60 + (m1 - m2)))   # took the smaller minutes from the bigger
    c += [dur(d + 60), dur(d - 60) if d > 60 else None, dur(d + 10), dur(d - 5) if d > 5 else None, dur(d + 20)]
    e = steps_text(t1, t2)
    if nv and dval(nv) != d * 60:
        e += " (Not %s: 1 h has 60 min, not 100, so do not subtract the times like ordinary numbers.)" % nv
    if note:
        e += " (" + note + ")"
    return dmcq(f + text, dur(d), c, e)


def set_durations():
    its = []
    its.append(how_long("The maths lesson starts at <b>9.00 am</b> and ends at <b>9.40 am</b>. How long is the lesson?",
                        T_(9, 0), T_(9, 40), "clocks", ["1 h 40 min", "40 s"]))
    its.append(how_long("Recess is from <b>10.15 am</b> to <b>10.45 am</b>. How long is recess?",
                        T_(10, 15), T_(10, 45), "clocks", ["45 min", "1 h 30 min"]))
    its.append(how_long("Hui Min practises the piano from <b>4.20 pm</b> to <b>4.55 pm</b>. How long does she practise?",
                        T_(16, 20), T_(16, 55), None, ["55 min", "1 h 15 min"]))
    its.append(how_long("Zhi Hao’s CCA is from <b>2.30 pm</b> to <b>4.30 pm</b>. Use the time line. How long is the CCA?",
                        T_(14, 30), T_(16, 30), "line", ["30 min", "1 h 30 min"]))
    its.append(how_long("Priya’s school bus ride is from <b>6.45 am</b> to <b>7.10 am</b>. Use the time line. "
                        "How long is the ride?", T_(6, 45), T_(7, 10), "line"))
    its.append(how_long("The clocks show when Ryan started and finished his homework in the afternoon. "
                        "How long did he take?", T_(15, 25), T_(16, 5), "clocks"))
    its.append(how_long("Farah’s swimming lesson is from <b>5.40 pm</b> to <b>6.15 pm</b>. Use the time line. "
                        "How long is the lesson?", T_(17, 40), T_(18, 15), "line"))
    its.append(how_long("Jun Jie reads in the library from <b>11.40 am</b> to <b>12.25 pm</b>. How long does he read?",
                        T_(11, 40), T_(12, 25), "line?", ["1 h 15 min"]))
    its.append(how_long("Mrs Ng and her son eat lunch at a hawker centre from <b>12.45 pm</b> to <b>1.20 pm</b>. "
                        "How long is lunch?", T_(12, 45), T_(13, 20), None, ["1 h 25 min"]))
    its.append(how_long("A school assembly and talk go on from <b>8.50 am</b> to <b>10.20 am</b>. "
                        "How long is that?", T_(8, 50), T_(10, 20), "line?"))
    its.append(how_long("A movie starts at <b>7.15 pm</b> and ends at <b>9.05 pm</b>. How long is the movie?",
                        T_(19, 15), T_(21, 5), "line?"))
    its.append(how_long("Kavya’s class visits Gardens by the Bay from <b>10.00 am</b> to <b>1.30 pm</b>. "
                        "How long is the visit?", T_(10, 0), T_(13, 30), "line?", ["9 h 30 min"],
                        "9 h 30 min comes from 10 − 1 = 9, but that does not work across 12 noon."))
    its.append(how_long("Wei Ming’s family is at the Singapore Zoo from <b>11.30 am</b> to <b>2.15 pm</b>. "
                        "How long are they at the zoo?", T_(11, 30), T_(14, 15), None, ["9 h 15 min"],
                        "9 h 15 min comes from 11 − 2 = 9, but that does not work across 12 noon."))
    its.append(how_long("Sports Day is from <b>7.30 am</b> to <b>12 noon</b>. How long is Sports Day?",
                        T_(7, 30), T_(12, 0), "line?", ["5 h 30 min"],
                        "5 h 30 min counts the numbers 8, 9, 10, 11 and 12 instead of the jumps."))
    its.append(how_long("Mr Rahman drives from Singapore to Malacca. He leaves at <b>8.20 am</b> and arrives at "
                        "<b>11.10 am</b>. How long is the drive?", T_(8, 20), T_(11, 10)))
    its.append(how_long("Mrs Lim’s baking class is from <b>1.55 pm</b> to <b>3.10 pm</b>. How long is the class?",
                        T_(13, 55), T_(15, 10), None, ["1 h 45 min"]))
    its.append(how_long("Chloe’s family leaves home at <b>11.50 am</b> and reaches Sentosa at <b>12.35 pm</b>. "
                        "How long is the journey?", T_(11, 50), T_(12, 35), None, ["1 h 15 min"]))
    its.append(how_long("A concert starts at <b>6.50 pm</b> and ends at <b>8.25 pm</b>. How long is the concert?",
                        T_(18, 50), T_(20, 25)))
    its.append(how_long("Hafiz goes to sleep at <b>9.30 pm</b>. He wakes up at <b>6.15 am</b> the next morning. "
                        "Use the time line. How long does he sleep?", T_(21, 30), T_(6, 15), "line?",
                        ["3 h 15 min", "15 h 15 min"],
                        "3 h 15 min comes from 9.30 − 6.15, but the time passes 12 midnight."))
    # compare two durations
    a, b = T_(10, 0) - T_(9, 15), T_(15, 30) - T_(14, 40)
    assert (a, b) == (45, 50)
    its.append(mcq("Lesson A is from <b>9.15 am</b> to <b>10.00 am</b>. Lesson B is from <b>2.40 pm</b> to "
                   "<b>3.30 pm</b>. Which lesson is longer, and by how much?", "Lesson B, by 5 min",
                   ["Lesson A, by 5 min", "Lesson B, by 15 min", "They are the same."],
                   "Lesson A: 9.15 am to 10.00 am is 45 min. Lesson B: 2.40 pm to 3.00 pm is 20 min, and 3.00 pm to 3.30 pm "
                   "is 30 min, so 50 min. 50 − 45 = 5. <b>Lesson B is longer, by 5 min</b>. "
                   "(Lesson B, by 15 min uses 330 − 240 = 90 min, counting 1 h as 100 min.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 8, 7, 9, 16, 19, 10, 17, 15, 11, 12, 13, 14, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Finding the duration with a time line", "items": [its[i] for i in order]}


# ============================================================ set 3: start or finish time
def finish_item(text, t, d, figure=False, extra=()):
    r = t + d
    c = list(extra)
    h, m = divmod(t, 60)
    dh, dm = divmod(d, 60)
    if t < 720 <= r:
        c.append(tm(r - 720))          # kept am after crossing 12 noon
    if m + dm >= 60:
        c.append(tm(h * 60 + dh * 60 + (m + dm - 60)))   # forgot to rename 60 min as 1 h
    if dh and dm:
        c.append(tm(r - dh * 60))      # forgot the hours
    c += [tm(r + 60), tm(t - d), tm(r - 60), tm((r + 720) % DAY), tm(r + 10)]
    if m + dm >= 60:
        steps = ("From %s, %d min takes you to %s. %s − %d min = %s more makes <b>%s</b>."
                 % (tm(t), 60 - m, tm(t + 60 - m), dur(d), 60 - m, dur(d - (60 - m)), tm(r))) if d - (60 - m) > 0 else \
            "From %s, %d min takes you to <b>%s</b>." % (tm(t), d, tm(r))
        if dh and d - (60 - m) > 0:
            mid = t + dh * 60
            steps = ("Add %s first: %s → %s. Then add %d min: %s → %s → <b>%s</b>."
                     % (dur(dh * 60), tm(t), tm(mid), dm, tm(mid), tm(mid + 60 - m), tm(r)))
    else:
        if dh:
            steps = ("Add %s first: %s → %s. Then add %d min: <b>%s</b>." % (dur(dh * 60), tm(t), tm(t + dh * 60), dm, tm(r))
                     if dm else "Add %s: <b>%s</b>." % (dur(d), tm(r)))
        elif m == 0:
            steps = "Count on %d min from %s: <b>%s</b>." % (dm, tm(t), tm(r))
        else:
            steps = "%d + %d = %d. So it ends at <b>%s</b>." % (m, dm, m + dm, tm(r))
    if t < 720 <= r:
        steps += " After 12 noon the time changes from am to pm."
    q = (line_finish(t, d) if figure else "") + text
    return mcq(q, tm(r), c, steps)


def start_item(text, t, d, figure=False, extra=(), pre=""):
    r = t - d
    c = list(extra)
    h, m = divmod(t, 60)
    dh, dm = divmod(d, 60)
    c.append(tm(t + d))                # counted forwards
    if r < 720 <= t:
        c.append(tm(r + 720))          # pm kept before 12 noon
    if dm > m:
        c.append(tm((h - dh) * 60 + (dm - m)))  # subtracted the smaller from the bigger, hour not changed
    if dh:
        c.append(tm(r + dh * 60))
    c += [tm(r - 60), tm(r + 60), tm(r + 10)]
    if dm > m:
        if m == 0:
            steps = "Count back %d min from %s: <b>%s</b>." % (d, tm(t), tm(r)) if not dh else \
                ("Count back %s: %s. Then count back %d min: <b>%s</b>." % (dur(dh * 60), tm(t - dh * 60), dm, tm(r)))
        else:
            mid = t - dh * 60
            first = ("Count back %s: %s → %s. " % (dur(dh * 60), tm(t), tm(mid))) if dh else ""
            steps = (first + "Count back %d min to %s. %d − %d = %d min more takes you back to <b>%s</b>."
                     % (m, tm(mid - m), dm, m, dm - m, tm(r)))
    else:
        if dh:
            steps = "Count back %s: %s. Then count back %d min: <b>%s</b>." % (dur(dh * 60), tm(t - dh * 60), dm, tm(r))
        else:
            steps = "Count back: %d − %d = %d. So it started at <b>%s</b>." % (m, dm, m - dm, tm(r))
    if r < 720 <= t:
        steps += " Before 12 noon the time is am, not pm."
    steps += " Check: %s + %s = %s." % (tm(r), dur(d), tm(t))
    q = pre + (line_finish(t, d, back=True) if figure else "") + text
    return mcq(q, tm(r), c, steps)


def set_start_finish():
    its = []
    its.append(finish_item("The English lesson starts at <b>8.00 am</b>. It lasts <b>45 min</b>. What time does it end?",
                           T_(8, 0), 45, True))
    its.append(finish_item("Recess starts at <b>9.30 am</b>. It lasts <b>30 min</b>. What time does recess end?",
                           T_(9, 30), 30, False, ["10.30 am"]))
    its.append(finish_item("Xin Yi starts her art class at <b>2.15 pm</b>. The class lasts <b>35 min</b>. "
                           "What time does it end?", T_(14, 15), 35))
    its.append(finish_item("Raju starts reading at <b>10.40 am</b>. He reads for <b>30 min</b>. What time does he stop?",
                           T_(10, 40), 30, True))
    its.append(finish_item("Mdm Wong puts kaya toast in the oven at <b>4.50 pm</b>. It bakes for <b>25 min</b>. "
                           "What time is it ready?", T_(16, 50), 25))
    its.append(finish_item("The class starts a quiz at <b>11.45 am</b>. The quiz lasts <b>30 min</b>. "
                           "What time does it end?", T_(11, 45), 30, True))
    its.append(finish_item("A bus leaves at <b>9.20 am</b>. The trip takes <b>1 h 35 min</b>. What time does it arrive?",
                           T_(9, 20), 95, True))
    its.append(finish_item("A movie starts at <b>7.30 pm</b>. It lasts <b>2 h 15 min</b>. What time does it end?",
                           T_(19, 30), 135))
    its.append(finish_item("Ahmad’s family arrives at East Coast Park at <b>11.20 am</b>. They stay for <b>2 h</b>. "
                           "What time do they leave?", T_(11, 20), 120))
    its.append(finish_item("Nurul starts a jigsaw puzzle at <b>7.55 am</b>. She takes <b>1 h 20 min</b>. "
                           "What time does she finish?", T_(7, 55), 80))
    its.append(start_item("Siti reaches school at <b>7.20 am</b>. Her walk takes <b>15 min</b>. "
                          "What time did she leave home?", T_(7, 20), 15, True))
    its.append(start_item("A CCA session ends at <b>5.00 pm</b>. It lasts <b>30 min</b>. What time did it start?",
                          T_(17, 0), 30, True))
    its.append(start_item("Arjun finishes his homework at <b>10.10 am</b>. He worked for <b>25 min</b>. "
                          "What time did he start?", T_(10, 10), 25))
    its.append(start_item("A cooking show ends at <b>1.15 pm</b>. It lasts <b>40 min</b>. What time did it start?",
                          T_(13, 15), 40, True))
    its.append(start_item("Devi’s train ride ends at <b>3.05 pm</b>. The ride takes <b>1 h 20 min</b>. "
                          "What time did it start?", T_(15, 5), 80))
    its.append(start_item("A school concert ends at <b>12 noon</b>. It lasts <b>2 h 30 min</b>. What time did it start?",
                          T_(12, 0), 150, False, ["2.30 pm"]))
    its.append(start_item("Mr Tan’s dinner party ends at <b>8.10 pm</b>. It lasts <b>1 h 45 min</b>. "
                          "What time did it start?", T_(20, 10), 105))
    # clock pictures
    its.append(finish_item(fig(clock_svg(3, 35)) + "The clock shows when a cake goes into the oven in the afternoon. "
                           "It bakes for <b>40 min</b>. What time is the cake ready?", T_(15, 35), 40))
    its.append(start_item("The clock shows when Kumar finished painting in the evening. He painted for <b>50 min</b>. "
                          "What time did he start?", T_(20, 10), 50, False, (), fig(clock_svg(8, 10))))
    its.append(finish_item("Ethan’s family leaves home at <b>10.35 am</b>. They drive for <b>1 h 50 min</b> to a resort "
                           "in Malaysia. What time do they arrive?", T_(10, 35), 110))
    assert len(its) == 20
    order = [0, 1, 10, 2, 11, 3, 12, 4, 13, 5, 17, 18, 6, 14, 7, 15, 8, 16, 9, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Finding the start time or the finish time", "items": [its[i] for i in order]}


# ============================================================ set 4: 24-hour clock
def to12(s):
    return tm(int(s[:2]) * 60 + int(s[2:]))


def set_24h():
    its = []
    its.append(mcq("What is <b>12 noon</b> in 24-hour time?", "1200", ["0000", "0012", "2400"],
                   "12 noon is the middle of the day. In 24-hour time it is <b>1200</b>. (0000 is 12 midnight.)"))
    its.append(mcq("What is <b>12 midnight</b> in 24-hour time?", "0000", ["1200", "0012", "0100"],
                   "A new day starts at 12 midnight. In 24-hour time we write <b>0000</b>. (1200 is 12 noon.)"))
    its.append(mcq("Write <b>7.30 am</b> in 24-hour time.", "0730", ["1930", "730", "0703"],
                   "am times keep the same hour. A 24-hour time always has 4 digits, so put a 0 in front: <b>0730</b>. "
                   "(1930 is 7.30 pm.)"))
    its.append(mcq("Write <b>9.05 am</b> in 24-hour time.", "0905", ["2105", "0950", "905"],
                   "am time, so the hour stays 9. Write 4 digits: 09 for the hour and 05 for the minutes: <b>0905</b>. "
                   "(0950 would be 9.50 am.)"))
    its.append(mcq("Write <b>3.00 pm</b> in 24-hour time.", "1500", ["0300", "1300", "300"],
                   "For pm times, add 12 to the hour: 3 + 12 = 15. So 3.00 pm = <b>1500</b>. "
                   "(1300 adds 10, not 12. 0300 is 3.00 am.)"))
    its.append(mcq("Write <b>7.30 pm</b> in 24-hour time.", "1930", ["0730", "1730", "2130"],
                   "pm time, so add 12 to the hour: 7 + 12 = 19. So 7.30 pm = <b>1930</b>. "
                   "(1730 adds 10, not 12. 2130 is 9.30 pm.)"))
    its.append(mcq("Write <b>11.45 pm</b> in 24-hour time.", "2345", ["1145", "2145", "0045"],
                   "pm time, so add 12 to the hour: 11 + 12 = 23. So 11.45 pm = <b>2345</b>. "
                   "(2145 adds 10, not 12. 1145 is 11.45 am.)"))
    its.append(mcq("Write <b>12.20 pm</b> in 24-hour time.", "1220", ["0020", "2420", "1320"],
                   "12.20 pm is 20 min after 12 noon. Noon is 1200, so do not add 12: <b>1220</b>. "
                   "(There is no 2420. 0020 is 20 min after midnight.)"))
    its.append(mcq("Write <b>12.40 am</b> in 24-hour time.", "0040", ["1240", "2440", "1340"],
                   "12.40 am is 40 min after 12 midnight. Midnight is 0000, so 12.40 am = <b>0040</b>. "
                   "(1240 is 12.40 pm, just after noon.)"))
    its.append(mcq("Write <b>1930</b> in 12-hour time.", "7.30 pm", ["9.30 pm", "7.30 am", "9.30 am"],
                   "19 is more than 12, so it is a pm time. 19 − 12 = 7. So 1930 = <b>7.30 pm</b>. "
                   "(Not 9.30 pm: do not just read the 9. Take away 12, not 10.)"))
    its.append(mcq("Write <b>1500</b> in 12-hour time.", "3.00 pm", ["5.00 pm", "3.00 am", "1.00 pm"],
                   "15 − 12 = 3, and it is after noon. So 1500 = <b>3.00 pm</b>. (5.00 pm takes away 10, not 12.)"))
    its.append(mcq("Write <b>2105</b> in 12-hour time.", "9.05 pm", ["11.05 pm", "9.05 am", "9.50 pm"],
                   "21 − 12 = 9, and it is after noon. So 2105 = <b>9.05 pm</b>. (11.05 pm takes away 10, not 12. "
                   "9.50 pm mixes up 05 and 50.)"))
    its.append(mcq("Write <b>1645</b> in 12-hour time.", "4.45 pm", ["6.45 pm", "4.45 am", "6.45 am"],
                   "16 − 12 = 4, and it is after noon. So 1645 = <b>4.45 pm</b>. (6.45 pm takes away 10, not 12.)"))
    its.append(mcq("Write <b>1210</b> in 12-hour time.", "12.10 pm", ["12.10 am", "2.10 pm", "10.10 am"],
                   "12 is the noon hour, so do not take away 12. 1210 is 10 min after 12 noon: <b>12.10 pm</b>. "
                   "(12.10 am is just after midnight.)"))
    its.append(mcq("Which 24-hour time is in the <b>morning</b>?", "0815", ["1815", "2015", "1215"],
                   "Times from 0000 to 1159 are am times. <b>0815</b> is 8.15 am, in the morning. 1815 is 6.15 pm, "
                   "2015 is 8.15 pm and 1215 is 12.15 pm."))
    its.append(mcq("Which is the <b>latest</b> time in a day?", "2110", ["1545", "1205", "0950"],
                   "In 24-hour time a bigger number is later in the day. <b>2110</b> (9.10 pm) is the latest. "
                   "1545 is 3.45 pm, 1205 is 12.05 pm and 0950 is 9.50 am."))
    its.append(mcq(fig(clock_svg(6, 40)) + "The clock shows a time in the <b>evening</b>. Write it in 24-hour time.",
                   "1840", ["0640", "1640", "0740"],
                   "The short hand is between 6 and 7, and the long hand points to 8: 6.40. In the evening it is 6.40 pm. "
                   "6 + 12 = 18, so it is <b>1840</b>. (0640 is in the morning. 1640 adds 10, not 12.)"))
    its.append(mcq(fig(clock_svg(9, 25)) + "The clock shows a time in the <b>morning</b>. Write it in 24-hour time.",
                   "0925", ["2125", "1925", "0525"],
                   "The short hand is between 9 and 10, and the long hand points to 5: 9.25. In the morning it is am, "
                   "so the hour stays 9: <b>0925</b>. (2125 is 9.25 pm. 0525 reads the long hand as the hour.)"))
    its.append(mcq(fig(digital_svg("1415")) + "The digital clock shows 24-hour time. What is the time in 12-hour time?",
                   "2.15 pm", ["4.15 pm", "2.15 am", "12.15 pm"],
                   "14 − 12 = 2, and it is after noon. So 1415 = <b>2.15 pm</b>. (4.15 pm takes away 10, not 12.)"))
    d = T_(13, 20) - T_(9, 45)
    assert d == 215
    its.append(dmcq("How long is it from <b>0945</b> to <b>1320</b>?", dur(d), ["3 h 75 min", "4 h 35 min", "3 h 25 min"],
                    "0945 to 1000 is 15 min. 1000 to 1300 is 3 h. 1300 to 1320 is 20 min. "
                    "15 min + 3 h + 20 min = <b>3 h 35 min</b>. (3 h 75 min comes from 1320 − 945 = 375, "
                    "but 1 h has 60 min, not 100.)"))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 14, 9, 10, 6, 11, 7, 12, 16, 17, 8, 13, 18, 15, 19]
    assert sorted(order) == list(range(20))
    return {"title": "The 24-hour clock", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_words():
    its = []
    # 1 school starts at 7.30 am
    its.append(how_long("School starts at <b>7.30 am</b>. Wei Ming leaves home at <b>7.05 am</b>. "
                        "How much time does he have to get to school?", T_(7, 5), T_(7, 30), None, ["35 min"]))
    # 2 MRT ride
    its.append(finish_item("Priya boards an MRT train at <b>3.50 pm</b>. The ride takes <b>25 min</b>. "
                           "What time does she reach her station?", T_(15, 50), 25))
    # 3 movie
    its.append(finish_item("A movie starts at <b>7.45 pm</b>. It lasts <b>1 h 50 min</b>. What time does it end?",
                           T_(19, 45), 110, True))
    # 4 recess back
    its.append(start_item("Recess lasts <b>30 min</b>. It ends at <b>10.00 am</b>. What time does recess start?",
                          T_(10, 0), 30, False, ["10.30 pm"]))
    # 5 clock: early
    assert T_(7, 30) - T_(7, 12) == 18
    its.append(mcq(fig(clock_svg(7, 12)) + "School starts at <b>7.30 am</b>. The clock shows the time Jun Jie reaches "
                   "school in the morning. How early is he?", "18 min", ["12 min", "28 min", "42 min"],
                   "The clock shows 7.12 am. 7.12 am to 7.30 am is 30 − 12 = <b>18 min</b>. "
                   "(12 min is just the minutes on the clock. 42 min adds 30 and 12.)"))
    # 6 bar model: two parts in min and s
    its.append(dmcq(fig(model_svg([("", [(105, "1 min 45 s", "u"), (90, "1 min 30 s", "u")])], top=(0, 195, "?"),
                                  label="bar model: 1 min 45 s and 1 min 30 s, total unknown")) +
                    "Kavya runs two rounds of the school field. The first round takes <b>1 min 45 s</b>. "
                    "The second round takes <b>1 min 30 s</b>. How long does she take altogether?", "3 min 15 s",
                    ["2 min 15 s", "3 min 45 s", "4 min 15 s"],
                    "Add the minutes: 1 min + 1 min = 2 min. Add the seconds: 45 s + 30 s = 75 s = 1 min 15 s. "
                    "2 min + 1 min 15 s = <b>3 min 15 s</b>. (2 min 15 s forgets to rename 60 s as 1 min.)"))
    # 7 bar model compare, altogether
    its.append(dmcq(fig(model_svg([("Hafiz", [(45, "45 min", "u")]), ("Siti", [(45, "45 min", "u"), (20, "20 min", "w")])],
                                  right="?", label="bar model: Hafiz 45 min, Siti 20 min more")) +
                    "Hafiz spends <b>45 min</b> on his homework. Siti spends <b>20 min more</b> than Hafiz. "
                    "How long do they spend altogether?", "1 h 50 min", ["1 h 5 min", "1 h 10 min", "1 h 30 min"],
                    "Siti: 45 + 20 = 65 min. Altogether: 45 + 65 = 110 min. 110 min = 60 min + 50 min = <b>1 h 50 min</b>. "
                    "(1 h 5 min is only Siti’s time. 1 h 10 min counts 1 h as 100 min.)"))
    # 8 bar model part-whole subtraction
    its.append(dmcq(fig(model_svg([("", [(45, "?", "u"), (25, "25 min", "w")])], top=(0, 70, "1 h 10 min"),
                                  label="bar model: 1 h 10 min in two parts")) +
                    "Ali takes the MRT and then a bus to his grandmother’s flat. The whole journey takes <b>1 h 10 min</b>. "
                    "The bus ride takes <b>25 min</b>. How long is the MRT ride?", "45 min",
                    ["85 min", "1 h 35 min", "1 h 15 min"],
                    "1 h 10 min = 60 + 10 = 70 min. 70 − 25 = <b>45 min</b>. Check: 45 min + 25 min = 70 min = 1 h 10 min. "
                    "(85 min counts 1 h as 100 min. 1 h 15 min takes 10 from 25 instead of renaming.)"))
    # 9 seconds x 4
    assert 4 * 40 == 160
    its.append(dmcq("An MRT train stops at <b>4</b> stations. It stops for <b>40 s</b> at each station. "
                    "How long does it stop altogether?", "2 min 40 s", ["1 min 60 s", "4 min 40 s", "1 min 40 s"],
                    "4 × 40 s = 160 s. 160 s = 60 s + 60 s + 40 s = <b>2 min 40 s</b>. "
                    "(1 min 60 s counts 1 min as 100 s.)"))
    # 10 movie in 24-hour time
    d = T_(21, 35) - T_(19, 45)
    assert d == 110
    its.append(dmcq("A movie starts at <b>1945</b> and ends at <b>2135</b>. How long is the movie?", dur(d),
                    ["190 min", "2 h 10 min", "1 h 35 min"],
                    "1945 to 2000 is 15 min. 2000 to 2100 is 1 h. 2100 to 2135 is 35 min. "
                    "15 min + 1 h + 35 min = <b>1 h 50 min</b>. (190 min comes from 2135 − 1945, "
                    "but 1 h has 60 min, not 100.)"))
    # 11 airport in 24-hour time
    r = T_(8, 15) - 150
    assert t24(r) == "0545"
    its.append(mcq("Mei Ling’s flight leaves Changi Airport at <b>0815</b>. She reaches the airport <b>2 h 30 min</b> "
                   "before that. What time does she reach the airport? Give the 24-hour time.", "0545",
                   ["1045", "0615", "0645"],
                   "Count back 2 h: 0815 → 0615. Count back 30 min more: 0615 → 0600 is 15 min, then 15 min more is "
                   "<b>0545</b>. (1045 counts forwards. 0615 forgets the 30 min.)"))
    # 12 zoo crossing noon
    its.append(how_long("Chloe’s family visits the Singapore Zoo from <b>9.15 am</b> to <b>1.40 pm</b>. "
                        "How long are they at the zoo?", T_(9, 15), T_(13, 40), None, ["8 h 25 min", "3 h 25 min"],
                        "8 h 25 min comes from 9 − 1 = 8, but that does not work across 12 noon."))
    # 13 hawker stall open 9 h
    its.append(finish_item("A hawker stall opens at <b>6.30 am</b>. It stays open for <b>9 h</b>. What time does it close?",
                           T_(6, 30), 9 * 60, False, ["3.30 am"]))
    # 14 bar model: less, renaming
    its.append(dmcq(fig(model_svg([("Mr Kumar", [(140, "2 h 20 min", "u")]),
                                   ("Mrs Kumar", [(105, "?", "u"), (35, "35 min", "w")])],
                                  label="bar model: Mr Kumar 2 h 20 min, Mrs Kumar 35 min less")) +
                    "Mr Kumar takes <b>2 h 20 min</b> to paint a room. Mrs Kumar takes <b>35 min less</b>. "
                    "How long does Mrs Kumar take?", "1 h 45 min", ["2 h 15 min", "2 h 55 min", "1 h 55 min"],
                    "2 h 20 min = 1 h 80 min (rename 1 h as 60 min: 60 + 20 = 80). 80 − 35 = 45. So Mrs Kumar takes "
                    "<b>1 h 45 min</b>. (2 h 15 min takes 20 from 35. 2 h 55 min adds instead of subtracts.)"))
    # 15 bar model: 4 equal units
    assert 4 * 45 == 180
    its.append(dmcq(fig(model_svg([("", [(45, "45 min", "u")] * 4)], top=(0, 180, "?"),
                                  label="bar model: 4 units of 45 min")) +
                    "Devi has a <b>45 min</b> piano lesson every week. How long are <b>4</b> lessons altogether?", "3 h",
                    ["1 h 80 min", "2 h 40 min", "4 h"],
                    "1 unit = 45 min. 4 units = 4 × 45 = 180 min. 180 min = 60 + 60 + 60 = <b>3 h</b>. "
                    "(1 h 80 min counts 1 h as 100 min.)"))
    # 16 two-step journey
    assert T_(6, 55) + 10 + 25 == T_(7, 30)
    its.append(mcq("Sarah leaves home at <b>6.55 am</b>. She walks <b>10 min</b> to the MRT station. Then the train ride "
                   "takes <b>25 min</b>. What time does she reach her stop?", "7.30 am", ["7.05 am", "7.20 am", "7.30 pm"],
                   "Walk: 6.55 am + 10 min = 7.05 am. Train: 7.05 am + 25 min = <b>7.30 am</b>. "
                   "(7.05 am stops after the walk. 7.20 am adds only the train ride.)"))
    # 17 at the cinema
    assert T_(16, 25) - (T_(14, 40) - 15) == 120
    its.append(dmcq("A movie starts at <b>2.40 pm</b> and ends at <b>4.25 pm</b>. Ryan reaches the cinema "
                    "<b>15 min</b> before the movie starts. How long is he at the cinema until the movie ends?", "2 h",
                    ["1 h 45 min", "1 h 30 min", "2 h 15 min"],
                    "Ryan arrives 15 min before 2.40 pm, at 2.25 pm. 2.25 pm to 4.25 pm is <b>2 h</b>. "
                    "(1 h 45 min is only the movie. 1 h 30 min takes away the 15 min instead of adding it.)"))
    # 18 24-hour finish
    r = T_(17, 45) + 150
    assert t24(r) == "2015"
    its.append(mcq("A National Day show on TV starts at <b>1745</b>. It lasts <b>2 h 30 min</b>. What time does it end? "
                   "Give the 24-hour time.", "2015", ["1915", "0815", "2115"],
                   "Add 2 h: 1745 → 1945. Add 30 min: 1945 → 2000 is 15 min, then 15 min more is <b>2015</b>. "
                   "(1915 adds only 1 h 30 min. 0815 is 8.15 am, but the show ends at 8.15 pm, which is 2015.)"))
    # 19 bar model: how much longer
    its.append(dmcq(fig(model_svg([("Bus", [(35, "35 min", "u"), (30, "?", "w")]), ("MRT", [(35, "35 min", "u")])],
                                  label="bar model: bus 1 h 5 min, MRT 35 min")) +
                    "Siti’s MRT ride takes <b>35 min</b>. Her bus ride takes <b>1 h 5 min</b>. "
                    "How much longer is the bus ride?", "30 min", ["1 h 40 min", "70 min", "1 h 30 min"],
                    "1 h 5 min = 60 + 5 = 65 min. 65 − 35 = <b>30 min</b>. (70 min counts 1 h as 100 min. "
                    "1 h 30 min takes 5 from 35 instead of renaming. 1 h 40 min adds the times.)"))
    # 20 school day
    d = T_(13, 30) - T_(7, 30)
    assert d == 360
    its.append(how_long("School starts at <b>7.30 am</b> and ends at <b>1.30 pm</b>. How long is the school day?",
                        T_(7, 30), T_(13, 30), None, ["7 h", "5 h", "6 h 30 min"], "7 h counts the numbers 7, 8, 9, 10, 11, 12 and 1 instead of the jumps."))
    assert len(its) == 20
    order = [0, 1, 3, 4, 2, 15, 5, 8, 6, 7, 19, 9, 12, 10, 11, 14, 16, 13, 17, 18]
    assert sorted(order) == list(range(20))
    return {"title": "Time word problems with bar models", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Seconds, minutes and hours</h2>"
        "<p>Very short things take <b>seconds</b> (s). A walk to the MRT station takes <b>minutes</b> (min). "
        "A school day takes <b>hours</b> (h). Time does <b>not</b> count in hundreds.</p>"
        + table(["Unit", "Is the same as"], [["1 min", "60 s"], ["1 h", "60 min"], ["1 day", "24 h"]]) +
        ex("Change to minutes", "1 h 25 min = ? min", "1 h = 60 min. 60 + 25 = 85.", "85 min") +
        "<h2>Find the duration with a time line</h2>"
        "<p>The <b>duration</b> is how long something takes. Draw a time line. Jump to the next o’clock first, "
        "then jump the whole hours, then the minutes left. Add the jumps.</p>"
        "<figure class='sn-fig'>" + timeline_svg([T_(19, 15), T_(20, 0), T_(21, 0), T_(21, 5)],
                                                 ["7.15 pm", "8.00 pm", "9.00 pm", "9.05 pm"],
                                                 ["+45 min", "+1 h", "+5 min"]) +
        "<figcaption>A movie from 7.15 pm to 9.05 pm: 45 min + 1 h + 5 min = <b>1 h 50 min</b>.</figcaption></figure>"
        "<h2>Find the start time or the finish time</h2>"
        "<p>To find the <b>finish time</b>, count on from the start time. To find the <b>start time</b>, "
        "count back from the finish time. When you pass 12 noon, am changes to pm.</p>"
        + ex("Finish time", "A quiz starts at 11.45 am. It lasts 30 min. When does it end?",
             "11.45 am + 15 min = 12 noon. 30 − 15 = 15 min more makes 12.15 pm.", "12.15 pm")
        + ex("Start time", "Siti reaches school at 7.20 am. Her walk takes 15 min. When did she leave home?",
             "Count back 15 min: 20 − 15 = 5.", "7.05 am") +
        "<h2>The 24-hour clock</h2>"
        "<p>A 24-hour time always has <b>4 digits</b>. am times keep the same hour: 7.30 am = 0730. "
        "For pm times, <b>add 12</b> to the hour: 7.30 pm = 1930. We read 1930 as “nineteen thirty hours”.</p>"
        "<figure class='sn-fig'>" + clock_svg(7, 30, size=200, ring24=True) +
        "<figcaption>The green numbers are the 24-hour times for the hours after 12 noon (00 is 12 midnight). In the evening this clock shows 7.30 pm = <b>1930</b>."
        "</figcaption></figure>"
        + table(["12-hour time", "24-hour time"], [["12 midnight", "0000"], ["7.30 am", "0730"], ["12 noon", "1200"],
                                                  ["12.20 pm", "1220"], ["3.00 pm", "1500"], ["7.30 pm", "1930"],
                                                  ["11.45 pm", "2345"]]) +
        "<h2>Word problems with a bar model</h2>"
        "<p>Draw a bar for each time. Change hours to minutes so the units match.</p>"
        "<figure class='sn-fig'>" + model_svg([("Hafiz", [(45, "45 min", "u")]),
                                               ("Siti", [(45, "45 min", "u"), (20, "20 min", "w")])], right="?",
                                              label="bar model: Hafiz 45 min, Siti 20 min more") +
        "<figcaption>Hafiz spends 45 min on homework. Siti spends 20 min more. Siti: 45 + 20 = 65 min. "
        "Altogether: 45 + 65 = 110 min = <b>1 h 50 min</b>.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["1 h 20 min = 120 min", "1 h is 60 min, not 100: 60 + 20 = 80 min"],
            ["7.15 pm to 9.05 pm: 905 − 715 = 190 min", "Do not subtract times like ordinary numbers. Use a time line: 1 h 50 min"],
            ["1930 = 9.30 pm", "Take away 12, not 10: 19 − 12 = 7, so 1930 = 7.30 pm"],
            ["7.30 am = 730", "Always write 4 digits: 0730"],
            ["11.45 am + 30 min = 12.15 am", "After 12 noon it is pm: 12.15 pm"],
            ["12.20 pm = 2420", "Do not add 12 in the noon hour: 12.20 pm = 1220"],
        ])
    )


FAQ = [
    {"q": "What do P3 students learn about time?",
     "a": "In Primary 3, students measure time in seconds, change between hours and minutes, find the duration, start time or finish time, and use the 24-hour clock."},
    {"q": "How do I change 12-hour time to 24-hour time?",
     "a": "Always write 4 digits. Keep the hour for am times (7.30 am = 0730) and add 12 to the hour for pm times (7.30 pm = 1930); 12 noon is 1200 and 12 midnight is 0000."},
    {"q": "What is the most common mistake with time?",
     "a": "Treating 1 hour as 100 minutes, for example working out 9.05 − 7.15 as 190 minutes. Use a time line and jump to the next o’clock first, which gives 1 h 50 min."},
    {"q": "Is the 24-hour clock in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus teaches the 24-hour clock in Primary 3, together with measuring time in seconds and finding durations."},
]


def gen():
    rnd = random.Random(63809)
    sets = [set_units(), set_durations(), set_start_finish(), set_24h(), set_words()]
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
        "country": "sg", "subject": "maths", "grade": "primary-3", "slug": "time", "sort": 9,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 3 Time: Seconds, Duration and the 24-Hour Clock",
        "seo_title": "P3 Time Worksheets: Free Primary 3 Maths on Duration and the 24-Hour Clock with Answers (MOE Syllabus)",
        "short_title": "Time",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 3: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Measuring time in seconds; finding the starting time, finishing time or duration; 24-hour clock",
        "meta_desc": "Free P3 maths practice on time: seconds, minutes and hours, durations on time lines, start and finish times and the 24-hour clock. 100 questions with answers.",
        "key_big": "1 h = 60 min and 1 min = 60 s, not 100. For pm times, add 12 to get the 24-hour time.",
        "key_sub": "7.15 pm to 9.05 pm: 45 min + 1 h + 5 min = 1 h 50 min, and 7.30 pm = 1930.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    for p in ("time line", "start and end clocks", "bar model"):
        mark_large(u, p)
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
