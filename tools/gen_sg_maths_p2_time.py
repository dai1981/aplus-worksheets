# -*- coding: utf-8 -*-
"""
Singapore Primary 2 Maths: Time (MOE 2021 Primary Mathematics Syllabus, Measurement)
"Telling time to the minute; measuring time in hours and minutes; converting hours and minutes"
  python3 tools/gen_sg_maths_p2_time.py
Reading analog clocks to 5 minutes and to the minute (written 4.37, or 4.37 pm), am and pm, 12 noon and
12 midnight, how long (hours and minutes), converting h and min to min and back, and Singapore word problems
with bar models. Every clock is drawn from the time itself (the hour hand moves between the numbers).
Every answer is worked out in code. Wrong answers come from real mistakes: the hands swapped (hour hand read
as the minutes), the number the minute hand points to read as the minutes, the hour hand just before a number
read as that number, am and pm mixed up, 1 h counted as 100 min (1115 − 1040 = 75), 80 min written as
1 h 80 min, counting the numbers instead of the jumps.
Helpers adapted from gen_cabc_math_g3_time.py, gen_uk_maths_y2_time.py and gen_sg_maths_p3_add_sub.py.
Singapore English: times 7.30 am, 12 noon, 12 midnight; durations 1 h 15 min.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
PARTFILL = "#fde3c8"
LINE = "#2b2b2b"
INK = "#2b2b2b"
RED = "#c0392b"
ORANGE = "#b35900"
GRAY = "#9aa3a0"
FONT = "Arial, Helvetica, sans-serif"
DAY = 24 * 60
GIRLS = ["Siti", "Nurul", "Farah", "Mei Ling", "Hui Min", "Xin Yi", "Priya", "Devi", "Kavya", "Chloe", "Sarah"]
BOYS = ["Ali", "Ahmad", "Hafiz", "Wei Ming", "Jun Jie", "Zhi Hao", "Raju", "Kumar", "Arjun", "Ethan", "Ryan"]


# ------------------------------------------------------------ time formats
def h12(h24):
    return (h24 - 1) % 12 + 1


def T(h, m):
    return h * 60 + m


def tm(t):
    """12-hour Singapore time from minutes after midnight: 7.30 am, 12 noon, 12 midnight"""
    t %= DAY
    h, m = divmod(t, 60)
    if t == 12 * 60:
        return "12 noon"
    if t == 0:
        return "12 midnight"
    return "%d.%02d %s" % (h12(h), m, "am" if h < 12 else "pm")


def dig(h, m):
    """clock time without am / pm: 4.37"""
    return "%d.%02d" % (h12(h), m % 60)


def dur(n):
    assert n > 0, n
    hh, mm = divmod(n, 60)
    if hh and mm:
        return "%d h %d min" % (hh, mm)
    if hh:
        return "%d h" % hh
    return "%d min" % mm


def dval(s):
    """value in minutes of '1 h 20 min', '85 min', '2 h' (None if it is not a duration)"""
    found = re.findall(r"(\d+) (h|min)\b", s)
    if not found:
        return None
    return sum(int(n) * (60 if u == "h" else 1) for n, u in found)


def hands_gap(h, m):
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def swapped(h, m):
    """hands swapped: the hour hand read as the minutes, the minute hand read as the hour (m in 5s)"""
    return dig(m // 5 or 12, (h % 12) * 5)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, key=None):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
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


def dq(q, ans, wrongs, e):
    """duration question: answer in minutes, wrongs as strings; all different in value"""
    right = dur(ans)
    vals = [ans] + [dval(w) for w in wrongs]
    assert None not in vals and len(set(vals)) == 4, (q, right, wrongs)
    return {"q": q, "c": [right] + list(wrongs), "a": 0, "e": e}


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
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


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


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


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


# ------------------------------------------------------------ pictures: clocks
def clock_body(h, m, cx, cy, R, ring=False):
    """Clock face. The hour hand is placed by the exact time: (h + m/60) x 30 degrees."""
    assert hands_gap(h, m) >= 12, (h, m)
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
    rn = R - 29 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    if ring:      # minutes written outside the face
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle'>" % (max(15 * k, 14), RED))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            r2 = R + 18 * k
            s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + r2 * math.cos(a), cy + r2 * math.sin(a) + 5 * k, (n * 5) % 60))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring=False):
    pad = 26 if ring else 0
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6 - pad, ring), "clock")


def labelled_clocks_svg(times, labels, size=170, label="clocks"):
    """Clocks in one row with a label above each (one SVG per question)."""
    gap, top = 14, 30
    n = len(times)
    W = n * size + (n - 1) * gap
    s = []
    for i, (h, m) in enumerate(times):
        x = i * (size + gap)
        s.append("<text x='%.1f' y='22' font-size='22' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                 % (x + size / 2.0, GREEN, labels[i]))
        c = size / 2.0
        s.append(clock_body(h, m, x + c, top + c, c - 6))
    return svg_wrap(W, size + top, "".join(s), label)


def four_clocks_svg(times):
    return labelled_clocks_svg(times, "ABCD", label="four clocks")


def start_end_svg(h1, m1, h2, m2):
    return labelled_clocks_svg([(h1, m1), (h2, m2)], ["Start", "End"], size=180, label="start and end clocks")


def timeline_svg(t1, t2, W=440):
    """Start -> next o'clock -> end, the jumps labelled (times in minutes after midnight)."""
    mid = (t1 // 60 + 1) * 60 if t1 % 60 else None
    L, R, Y = 52, W - 52, 70

    def X(t):
        return L + (R - L) * (t - t1) / float(t2 - t1)
    pts = [t1] + ([mid] if mid and t1 < mid < t2 else []) + [t2]
    assert all(X(b) - X(a) >= 100 for a, b in zip(pts, pts[1:])), (t1, t2)
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (L, Y, R, Y, LINE)]
    for t in pts:
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2.5'/>" % (X(t), Y - 10, X(t), Y + 10, LINE))
        s.append(text(X(t), Y + 32, tm(t), 16))
    for a, b in zip(pts, pts[1:]):
        x1, x2 = X(a), X(b)
        s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, Y - 12, (x1 + x2) / 2, Y - 52, x2, Y - 12, RED))
        s.append(text((x1 + x2) / 2, Y - 40, "+" + dur(b - a), 15, col=RED))
    return svg_wrap(W, 112, "".join(s), "time line")


# ------------------------------------------------------------ pictures: bar models
def tw(s, fs):
    """Rough text width of bold Arial."""
    w = 0
    for ch in s:
        if ch in ".,: ":
            w += 0.3
        elif ch in "l1i":
            w += 0.45
        elif ch in "m×÷?$":
            w += 0.85
        else:
            w += 0.6
    return w * fs


def brace(x1, x2, y, up, lab, col=INK):
    d = 7 if up else -7
    o = ["<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f' fill='none' stroke='%s' stroke-width='2'/>"
         % (x1, y + d, x1, y, x2, y, x2, y + d, col)]
    o.append(text((x1 + x2) / 2.0, y - 7 if up else y + 20, lab, 16, col=col))
    return "".join(o)


def bar_parts(parts_, total_lab, BW=460):
    """One bar split into parts drawn to scale. parts_ = [(value, label inside)]. Bracket below with total_lab."""
    X0, TOP, BH = 10, 8, 40
    tot = sum(v for v, _ in parts_)
    W = X0 * 2 + BW
    H = TOP + BH + 36
    o, x = [], float(X0)
    fills = [FILL, PARTFILL]
    for i, (v, lab) in enumerate(parts_):
        w = float(v) / tot * BW
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, TOP, w, BH, fills[i % 2], GREEN))
        o.append(text(x + w / 2.0, TOP + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
        x += w
    o.append(brace(X0, X0 + BW, TOP + BH + 10, False, total_lab, col=RED if total_lab == "?" else INK))
    return svg_wrap(W, H, "".join(o), "bar model: parts %s, whole %s" % (", ".join(l for _, l in parts_), total_lab))


def bar_compare(rows, diff_lab, BW=380):
    """Comparison model. rows = [(name, value, label inside)], the first bar is the longer one.
    The shorter bar has a dashed part up to the longer one, with diff_lab inside it."""
    (n1, v1, l1), (n2, v2, l2) = rows
    assert v1 > v2
    LW = int(max(tw(n1, 16), tw(n2, 16))) + 16
    X0, TOP, BH, GAP = 6, 8, 38, 16
    x0 = X0 + LW
    W = x0 + BW + 10
    H = TOP + 2 * BH + GAP + 8
    w2 = float(v2) / v1 * BW
    o = []
    for i, (nm, w, lab, fill) in enumerate([(n1, BW, l1, FILL), (n2, w2, l2, PARTFILL)]):
        y = TOP + i * (BH + GAP)
        assert tw(lab, 16) <= w - 6, (lab, w)
        o.append(text(x0 - 10, y + BH / 2.0 + 6, nm, 16, anchor="end"))
        o.append("<rect x='%d' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x0, y, w, BH, fill, GREEN))
        o.append(text(x0 + w / 2.0, y + BH / 2.0 + 6, lab, 16, col=RED if lab == "?" else INK))
    y = TOP + BH + GAP
    dw = BW - w2
    assert tw(diff_lab, 16) <= dw - 6, (diff_lab, dw)
    o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='none' stroke='%s' stroke-width='2' "
             "stroke-dasharray='6 4'/>" % (x0 + w2, y, dw, BH, ORANGE))
    o.append(text(x0 + w2 + dw / 2.0, y + BH / 2.0 + 6, diff_lab, 16, col=RED if diff_lab == "?" else ORANGE))
    lab = "bar model comparing %s (%s) and %s (%s), difference %s" % (n1, l1, n2, l2, diff_lab)
    return svg_wrap(int(W), H, "".join(o), lab)


# ------------------------------------------------------------ explanations
def hand_text(h, m):
    """How to read the two hands (for explanations)."""
    h = h12(h)
    n, extra = divmod(m, 5)
    nx = h % 12 + 1
    if m == 0:
        return "The minute hand (long) points to <b>12</b>, so it is exactly <b>%d o’clock</b>." % h
    hh = ("The hour hand (short) is between <b>%d</b> and <b>%d</b>. It has not reached %d yet, so the hour is <b>%d</b>."
          % (h, nx, nx, h))
    if extra == 0:
        mm = "The minute hand (long) points to <b>%d</b>. Count in 5s: %d × 5 = <b>%d min</b>." % (n, n, m)
    elif n == 0:
        mm = "The minute hand (long) is <b>%d small mark%s</b> past the 12: <b>%d min</b>." % (extra, "" if extra == 1 else "s", m)
    else:
        mm = ("The minute hand (long) is %d small mark%s past the %d. Count in 5s to %d, then in 1s: <b>%d min</b>."
              % (extra, "" if extra == 1 else "s", n, n * 5, m))
    return hh + " " + mm


def pick_hour(rnd, m, used):
    hrs = list(range(1, 13))
    rnd.shuffle(hrs)
    for h in hrs:
        if h in [u[0] for u in used][-2:] or (h, m) in used or hands_gap(h, m) < 18 or h == m // 5 \
                or swapped(h, m) == dig(h, m):
            continue
        used.append((h, m))
        return h
    raise AssertionError(m)


# ============================================================ set 1: read the clock
def set_clocks(rnd):
    its = []
    its.append(mcq("The minute hand moves from one number to the next number. How many minutes is that?", "5 min",
                   ["1 min", "10 min", "60 min"],
                   "There are 5 small marks between two numbers. Each small mark is 1 minute. So one number to the next "
                   "is <b>5 min</b>. That is why we count in 5s."))
    its.append(mcq("The minute hand points to <b>7</b>. How many minutes past the hour is it?", "35 min",
                   ["7 min", "40 min", "25 min"],
                   "Count in 5s from the 12 to the 7: 5, 10, 15, 20, 25, 30, 35. It is <b>35 min</b> past the hour. "
                   "(Not 7 min: the number is not the minutes.)"))
    used = []
    for m in [0, 20, 35, 10, 50, 25, 45, 55]:
        h = pick_hour(rnd, m, used)
        n = m // 5
        right = dig(h, m)
        sw = swapped(h, m)
        if m == 0:
            c = [sw, "%d.12" % h12(h), dig(h + 1, 0), dig(h - 1, 0)]
            note = ("(Not %s: that reads the hour hand as the minutes. Not %d.12: when the minute hand points to 12, "
                    "it is 0 minutes.)" % (sw, h12(h)))
        elif m >= 30:
            c = [dig(h + 1, m), sw, dig(h, n), dig(h, 60 - m)]
            note = ("(Not %s: the hour hand is <b>before</b> %d, so it is not %d o’clock yet. Not %s: that reads the "
                    "hour hand as the minutes.)" % (dig(h + 1, m), h12(h + 1), h12(h + 1), sw))
        else:
            c = [dig(h, n), sw, dig(h + 1, m), dig(h, 60 - m)]
            note = ("(Not %s: each number is 5 minutes, so %d means %d × 5 = %d. Not %s: that reads the hour hand as "
                    "the minutes.)" % (dig(h, n), n, n, m, sw))
        e = "%s So the time is <b>%s</b>. %s" % (hand_text(h, m), right, note)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show?", right, c, e))
    its.append(mcq("The hour hand is between <b>3</b> and <b>4</b>. The minute hand points to <b>9</b>. What time is it?",
                   "3.45", ["4.45", "9.15", "3.09"],
                   "The hour hand has not reached 4, so the hour is 3. Count in 5s to the 9: 9 × 5 = 45. "
                   "It is <b>3.45</b>. (9.15 swaps the hands. 3.09 forgets to count in 5s.)"))
    usedm = []

    def pick(lo, hi):
        while True:
            h = rnd.randint(1, 12)
            m = rnd.randint(lo, hi)
            if (m % 5 and (h, m) not in usedm and hands_gap(h, m) >= 18 and h not in [x[0] for x in usedm][-2:]
                    and (h, m // 5 * 5) not in used and m // 5 >= 1):
                usedm.append((h, m))
                return h, m

    for lo, hi in [(6, 14), (16, 29), (31, 44), (46, 59), (6, 24), (31, 44), (46, 58)]:
        h, m = pick(lo, hi)
        n = m // 5
        right = dig(h, m)
        c = []
        if m >= 30:
            c.append(dig(h + 1, m))
        c.append(dig(h, n * 5))
        c.append(dig(h, n))
        c += [dig(h, 60 - m), dig(h, m + 1 if m % 5 != 4 else m - 1), dig(h - 1, m)]
        e = "%s So the time is <b>%s</b>." % (hand_text(h, m), right)
        if m >= 30:
            e += " (Not %s: the hour hand has not reached %d yet.)" % (dig(h + 1, m), h12(h + 1))
        else:
            e += " (Not %s: count the small marks after the %d too.)" % (dig(h, n * 5), n)
        its.append(mcq(fig(clock_svg(h, m)) + "What time does the clock show? Read it to the minute.", right, c, e))
    pos = [0, 1, 2, 3]
    rnd.shuffle(pos)
    for (h, m), p in zip([(5, 38), (8, 13)], pos):
        others = [(h + 1, m), (h, 60 - m), (h, m // 5)]
        times = list(others)
        times.insert(p, (h, m))
        assert len(set(times)) == 4
        L = "ABCD"
        wrong = "; ".join("clock %s shows %s" % (L[times.index(t)], dig(*t)) for t in others)
        e = ("At %s the minute hand is %d small mark%s past the %d (count in 5s to %d, then in 1s to %d), and the hour "
             "hand is between %d and %d. That is clock <b>%s</b>. (%s.)"
             % (dig(h, m), m % 5, "" if m % 5 == 1 else "s", m // 5, m // 5 * 5, m, h12(h), h12(h + 1), L[p],
                cap(wrong)))
        its.append({"q": fig(four_clocks_svg(times)) + "Which clock shows <b>%s</b>?" % dig(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})
    assert len(its) == 20
    return {"title": "Read the clock: to 5 minutes and to the minute", "items": its}


# ============================================================ set 2: am and pm
CONTEXTS = [
    ("{n} wakes up for school.", 6, [5, 10, 15, 20]),
    ("{n} eats kaya toast for breakfast.", 6, [35, 40, 50]),
    ("{n} has recess in the school canteen.", 9, [30, 35, 40]),
    ("{n} has chicken rice for lunch.", 12, [20, 25, 40]),
    ("{n} takes the school bus home.", 13, [35, 40, 50]),
    ("{n} goes swimming with {pos} family.", 16, [40, 45, 50]),
    ("{n} has dinner at the hawker centre.", 19, [10, 20, 25]),
    ("{n} goes to bed.", 21, [5, 10, 20]),
]


def set_ampm(rnd, P):
    its = []
    its.append(mcq("When do we use <b>am</b>?", "from 12 midnight to 12 noon",
                   ["from 12 noon to 12 midnight", "only at night", "only after school"],
                   "<b>am</b> times go from 12 midnight to 12 noon: the night and the morning. "
                   "<b>pm</b> times go from 12 noon to 12 midnight: the afternoon and the evening."))
    its.append(mcq("When do we use <b>pm</b>?", "from 12 noon to 12 midnight",
                   ["from 12 midnight to 12 noon", "only in the morning", "only before lunch"],
                   "<b>pm</b> times go from 12 noon to 12 midnight: the afternoon and the evening."))
    its.append(mcq("What is <b>12 noon</b>?", "12 o’clock in the day", ["12 o’clock at night", "1 o’clock in the day",
                                                                       "the start of the morning"],
                   "<b>12 noon</b> is 12 o’clock in the middle of the day. 12 o’clock at night is <b>12 midnight</b>."))
    for ctx, hr, ms in CONTEXTS:
        n, pr, pos = P.next()
        h = hr
        m = rnd.choice([x for x in ms if hands_gap(h, x) >= 20])
        right = tm(T(h, m))
        other = "pm" if h < 12 else "am"
        flip = right[:-2] + other
        hx = h + 1 if m >= 30 else h - 1
        c = [flip, tm(T(hx, m)), swapped(h, m) + " " + right[-2:], tm(T(h, 60 - m))]
        part = ("in the morning" if h < 12 else "in the afternoon" if h < 18 else "in the evening")
        if h == 12:
            part = "just after 12 noon"
        e = ("%s The clock shows <b>%s</b>. This happens %s, so it is <b>%s</b>. (Not %s.)"
             % (hand_text(h, m), dig(h, m), part, right, flip))
        q = fig(clock_svg(h, m)) + ctx.format(n=n, pos=pos) + " The clock shows the time. What time is it?"
        its.append(mcq(q, right, c, e))
    its.append(mcq("Which is the best time for <b>breakfast</b>?", "7.00 am", ["7.00 pm", "1.00 am", "11.00 pm"],
                   "Breakfast is in the morning. Morning times are <b>am</b>. So <b>7.00 am</b> is the best time. "
                   "(1.00 am is in the middle of the night.)"))
    its.append(mcq("Which is the best time for <b>lunch</b>?", "12.30 pm", ["12.30 am", "5.30 am", "9.30 pm"],
                   "Lunch is just after 12 noon. Times after 12 noon are <b>pm</b>. So <b>12.30 pm</b> is the best time. "
                   "(12.30 am is just after 12 midnight.)"))
    n, pr, pos = P.next()
    its.append(mcq("What is %s most likely doing at <b>3.00 am</b>?" % n, "sleeping",
                   ["eating lunch", "having recess", "playing at the void deck"],
                   "3.00 am is 3 hours after 12 midnight. It is the middle of the night, so %s is most likely "
                   "<b>sleeping</b>." % n))
    its.append(mcq("Which time is in the <b>afternoon</b>?", "3.15 pm", ["3.15 am", "8.30 am", "12 midnight"],
                   "The afternoon comes after 12 noon, so it is a <b>pm</b> time: <b>3.15 pm</b>. "
                   "(3.15 am is in the night.)"))
    its.append(mcq("Which comes <b>1 minute after 11.59 am</b>?", "12 noon", ["12 midnight", "1.00 pm", "11.58 am"],
                   "11.59 am is in the morning, 1 minute before 12 o’clock. The next minute is <b>12 noon</b>. "
                   "(12 midnight comes 1 minute after 11.59 pm.)"))
    assert tm(T(11, 0) + 120) == "1.00 pm"
    its.append(mcq("It is <b>11.00 am</b>. What time is it <b>2 hours later</b>?", "1.00 pm",
                   ["1.00 am", "9.00 am", "12 noon"],
                   "Count on 2 hours: 11.00 am → 12 noon → <b>1.00 pm</b>. After 12 noon, am changes to pm. "
                   "(9.00 am is 2 hours earlier. 12 noon is only 1 hour later.)"))
    assert tm(T(22, 30) + 120) == "12.30 am"
    its.append(mcq("It is <b>10.30 pm</b>. What time is it <b>2 hours later</b>?", "12.30 am",
                   ["12.30 pm", "8.30 pm", "11.30 pm"],
                   "Count on 2 hours: 10.30 pm → 11.30 pm → 12.30. We passed 12 midnight, so pm changes to am: "
                   "<b>12.30 am</b>. (12.30 pm is in the day, after lunch time.)"))
    its.append(mcq("Put these times in order, <b>earliest first</b>.", "9.00 am, 12 noon, 2.00 pm",
                   ["2.00 pm, 9.00 am, 12 noon", "12 noon, 2.00 pm, 9.00 am", "9.00 am, 2.00 pm, 12 noon"],
                   "Morning (am) comes first, then 12 noon, then the afternoon (pm). So the order is "
                   "<b>9.00 am, 12 noon, 2.00 pm</b>."))
    its.append(mcq("Which is the best time for going to <b>bed</b>?", "8.45 pm", ["8.45 am", "10.15 am", "1.30 pm"],
                   "Children go to bed in the evening. Evening times are <b>pm</b>. So <b>8.45 pm</b> is the best time. "
                   "(1.30 pm is just after lunch.)"))
    assert len(its) == 20
    order = [0, 1, 2, 11, 12, 14, 3, 4, 5, 13, 6, 15, 7, 8, 9, 19, 10, 16, 17, 18]
    assert sorted(order) == list(range(20))
    return {"title": "am and pm", "items": [its[i] for i in order]}


# ============================================================ set 3: how long?
def naive(t1, t2):
    """the 1 h = 100 min mistake: 11.15 − 10.40 worked out as 1115 − 1040"""
    a = h12(t1 // 60) * 100 + t1 % 60
    b = h12(t2 // 60) * 100 + t2 % 60
    return b - a


def set_how_long(rnd, P):
    its = []
    its.append(dq("The minute hand goes <b>all the way round</b>, from 12 back to 12. How long is that?", 60,
                  ["12 min", "100 min", "30 min"],
                  "The minute hand passes 12 numbers. Each number is 5 min: 12 × 5 = 60 min. 60 min = <b>1 h</b>. "
                  "(1 h is 60 min, not 100 min.)"))
    its.append(dq("The minute hand moves from <b>12</b> to <b>6</b>. How long is that?", 30,
                  ["6 min", "60 min", "15 min"],
                  "From 12 to 6 is 6 jumps of 5 min: 6 × 5 = <b>30 min</b>. That is half an hour."))
    its.append(dq("The minute hand moves from <b>2</b> to <b>5</b>. How long is that?", 15,
                  ["3 min", "25 min", "10 min"],
                  "From 2 to 5 is 3 jumps: 3, 4, 5. Each jump is 5 min: 3 × 5 = <b>15 min</b>. (Not 3 min: each jump "
                  "is 5 minutes.)"))
    its.append(dq("The <b>hour hand</b> moves from <b>2</b> to <b>5</b>. How long is that?", 180,
                  ["3 min", "15 min", "7 h"],
                  "The hour hand moves 1 number every hour. From 2 to 5 is 3 jumps, so it is <b>3 h</b>. "
                  "(15 min is for the minute hand. 3 min reads the hours as minutes. 7 h adds 2 and 5.)"))

    def clocks(t1, t2):
        return fig(start_end_svg(t1 // 60, t1 % 60, t2 // 60, t2 % 60))

    def line(t1, t2):
        return fig(timeline_svg(t1, t2))

    # same hour
    t1, t2 = T(14, 20), T(14, 55)
    its.append(dq(clocks(t1, t2) + "The clocks show when an art lesson starts and ends. How long is the lesson?", 35,
                  ["55 min", "75 min", "7 min"],
                  "Both times are in the same hour. The minute hand moves from 20 min to 55 min: 55 − 20 = <b>35 min</b>. "
                  "(75 min adds 20 and 55 instead of taking away. Not 7 min: the hand moves 7 numbers, from 4 to 11, and each number is 5 min.)"))
    t1, t2 = T(15, 25), T(15, 50)
    n, pr, pos = P.next()
    assert t2 - t1 == 25
    its.append(dq(clocks(t1, t2) + "The clocks show when %s starts and stops reading. How long does %s read?" % (n, pr), 25,
                  ["50 min", "75 min", "5 min"],
                  "Both times are in the same hour. 50 − 25 = <b>25 min</b>. (75 min adds the minutes instead of "
                  "taking away. 5 min counts the numbers, not the minutes.)"))
    its.append(dq("A maths lesson starts at <b>8.05 am</b> and ends at <b>8.45 am</b>. How long is the lesson?", 40,
                  ["45 min", "50 min", "8 min"],
                  "Both times are in the same hour. 45 − 5 = <b>40 min</b>. (Not 45 min: the lesson starts at 8.05, "
                  "not at 8.00. 50 min adds 5 and 45 instead of taking away.)"))
    # whole hours
    t1, t2 = T(9, 0), T(11, 0)
    its.append(dq(clocks(t1, t2) + "The clocks show when a class trip starts and ends. How long is the trip?", 120,
                  ["3 h", "200 min", "20 min"],
                  "Count the jumps of the hour hand, not the numbers: 9 → 10 → 11. That is 2 jumps, so it is <b>2 h</b>. "
                  "(3 h counts the numbers 9, 10 and 11. 200 min counts 1 h as 100 min.)"))
    its.append(dq("A party starts at <b>1.00 pm</b> and ends at <b>4.00 pm</b>. How long is the party?", 180,
                  ["4 h", "300 min", "3 min"],
                  "Count on: 1.00 pm → 2.00 pm → 3.00 pm → 4.00 pm. That is 3 jumps: <b>3 h</b>. "
                  "(3 min uses the wrong unit. 4 h counts the numbers 1, 2, 3 and 4. 300 min counts 1 h as 100 min.)"))
    its.append(dq("A show starts at <b>10.30 am</b> and ends at <b>11.30 am</b>. How long is the show?", 60,
                  ["100 min", "30 min", "2 h"],
                  "The minutes are the same (30), and the hour goes up by 1. So it is <b>1 h</b>. "
                  "(Not 100 min: 1 h is 60 min. 2 h counts the numbers 10 and 11.)"))
    # across the hour (the 100-minute mistake)
    cases = [
        (T(10, 40), T(11, 15), "line", "A lesson starts at <b>10.40 am</b> and ends at <b>11.15 am</b>. How long is it?",
         ["75 min", "25 min", "1 h 35 min"]),
        (T(14, 50), T(15, 20), "line", "{n} goes on a bus ride from <b>2.50 pm</b> to <b>3.20 pm</b>. How long is the ride?",
         ["70 min", "1 h 30 min", "10 min"]),
        (T(11, 45), T(12, 10), None, "{n} plays in the playground from <b>11.45 am</b> to <b>12.10 pm</b>. "
                                     "How long does {pr} play?",
         ["65 min", "35 min", "1 h 25 min"]),
        (T(9, 30), T(11, 0), "line", "A swimming lesson is from <b>9.30 am</b> to <b>11.00 am</b>. How long is it?",
         ["170 min", "2 h 30 min", "30 min"]),
        (T(16, 25), T(17, 40), "clocks", "The clocks show when {n}’s badminton class starts and ends. "
                                         "How long is the class?",
         ["115 min", "15 min", "2 h 15 min"]),
        (T(13, 35), T(15, 5), None, "{n} visits the library from <b>1.35 pm</b> to <b>3.05 pm</b>. "
                                    "How long is {pos} visit?",
         ["170 min", "2 h 30 min", "30 min"]),
    ]
    for t1, t2, f, q, wr in cases:
        d = t2 - t1
        n, pr, pos = P.next()
        q = q.format(n=n, pr=pr, pos=pos)
        nv = naive(t1, t2)
        assert "%d min" % nv in wr, (nv, wr)
        figh = {"line": line, "clocks": clocks, None: lambda a, b: ""}[f](t1, t2)
        if t1 % 60:
            nxt = (t1 // 60 + 1) * 60
            a, b = nxt - t1, t2 - nxt
            e = ("Count on to the next o’clock first: %s to %s is %d min. Then %s to %s is %s. "
                 % (tm(t1), tm(nxt), a, tm(nxt), tm(t2), dur(b)))
            if b >= 60:
                e += "%d min + %s = <b>%s</b>." % (a, dur(b), dur(d))
            else:
                e += "%d + %d = " % (a, b) + ("%d min = <b>%s</b>." % (d, dur(d)) if d >= 60 else "<b>%s</b>." % dur(d))
        else:
            e = ("%s to %s is %s. Then %s to %s is %d min. So it is <b>%s</b>."
                 % (tm(t1), tm(t1 + 60 * (d // 60)), dur(60 * (d // 60)), tm(t1 + 60 * (d // 60)), tm(t2), d % 60, dur(d)))
        e += " (Not %d min: 1 h is 60 min, not 100 min, so do not just take away the numbers.)" % nv
        its.append(dq(figh + q, d, wr, e))
    its.append(mcq("Which takes about <b>1 h</b>?", "a swimming lesson",
                   ["brushing your teeth", "tying your shoelaces", "a night’s sleep"],
                   "Brushing your teeth and tying your shoelaces take a few minutes. A night’s sleep takes many hours. "
                   "<b>A swimming lesson</b> takes about 1 h."))
    its.append(mcq("Recess is about 30 ___. Choose the unit.", "min", ["h", "days", "weeks"],
                   "Recess is short, so we use minutes. Recess is about <b>30 min</b>. (30 h is more than a whole day.)"))
    its.append(mcq("A movie at the cinema lasts about 2 ___. Choose the unit.", "h", ["min", "days", "weeks"],
                   "2 min is far too short, and 2 days is far too long. A movie lasts about <b>2 h</b>."))
    assert len(its) == 19, len(its)
    its.append(dq("A cooking class starts at <b>4.00 pm</b> and ends at <b>5.25 pm</b>. How long is the class?", 85,
                  ["125 min", "25 min", "2 h 25 min"],
                  "4.00 pm to 5.00 pm is 1 h. 5.00 pm to 5.25 pm is 25 min. So it is <b>1 h 25 min</b>. "
                  "(Not 125 min: 1 h is 60 min, not 100 min.)"))
    order = [0, 1, 2, 3, 16, 17, 18, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 13, 14, 15]
    assert sorted(order) == list(range(20))
    return {"title": "How long? Hours and minutes", "items": [its[i] for i in order]}


# ============================================================ set 4: convert h and min
def to_min_q(H, M):
    right = "%d min" % (60 * H + M)
    c = ["%d min" % (100 * H + M), "%d min" % (H + M), "%d min" % (60 * H), "%d min" % (60 * H + M + 10)]
    c = [x for x in c if x != right]
    if H == 1:
        e = "1 h = 60 min. 60 min + %d min = <b>%s</b>." % (M, right)
    else:
        e = "%d h = %d × 60 min = %d min. %d min + %d min = <b>%s</b>." % (H, H, 60 * H, 60 * H, M, right)
    e += " (Not %d min: 1 h is 60 min, not 100 min.)" % (100 * H + M)
    return mcq("Change <b>%s</b> to minutes." % dur(60 * H + M), right, c, e)


def to_hm_q(N):
    H, M = divmod(N, 60)
    assert H >= 1 and M > 0
    right = dur(N)
    if N >= 100:
        c = ["1 h %d min" % (N - 100),                                     # 1 h counted as 100 min
             "1 h %d min" % N if H == 1 else None,                          # 110 min written as 1 h 110 min
             "%d h %d min" % (H + 1, M)]
    else:
        c = ["1 h %d min" % N,                                             # 80 min written as 1 h 80 min
             "%d h %d min" % (H + 1, M),
             "%d h %d min" % (H, 60 - M)]                                  # minutes to the next hour
    c += ["%d h %d min" % (H, M + 10) if M + 10 < 60 else None, "%d h %d min" % (H, M - 5)]
    c = [x for x in c if x]
    vals = {dval(right)}
    out = []
    for x in c:
        if dval(x) not in vals:
            vals.add(dval(x))
            out.append(x)
    out = out[:3]
    assert len(out) == 3, (N, out)
    steps = " + ".join(["60"] * H) + (" + %d" % M)
    e = ("Take out groups of 60 min. %d = %s. Each 60 min is 1 h. So %d min = <b>%s</b>."
         % (N, steps, N, right))
    if H == 1:
        e += " (Not 1 h %d min: after taking out 1 h, only %d min is left.)" % (N, M)
    if N >= 100:
        e = (e[:-1] + " " if H == 1 else e + " (") + "Not 1 h %d min: 1 h is 60 min, not 100 min.)" % (N - 100)
    return {"q": "Change <b>%d min</b> to hours and minutes." % N, "c": [right] + out, "a": 0, "e": e}


def set_convert(rnd, P):
    its = []
    its.append(mcq("1 h = ☐ min. What is the missing number?", "60", ["100", "10", "24"],
                   "The minute hand goes round once in 1 h: 12 × 5 = 60. So <b>1 h = 60 min</b>. (Not 100.)"))
    its.append(mcq("Half an hour = ☐ min. What is the missing number?", "30", ["50", "15", "60"],
                   "1 h = 60 min. Half of 60 is <b>30</b>. (Not 50: 1 h is not 100 min.)"))
    its.append(mcq("2 h = ☐ min. What is the missing number?", "120", ["200", "62", "100"],
                   "2 h = 60 min + 60 min = <b>120 min</b>. (Not 200: 1 h is 60 min, not 100 min.)"))
    its.append(mcq("3 h = ☐ min. What is the missing number?", "180", ["300", "63", "160"],
                   "3 h = 60 + 60 + 60 = <b>180 min</b>. (Not 300: 1 h is 60 min, not 100 min.)"))
    for H, M in [(1, 20), (1, 45), (1, 5), (2, 10), (2, 35), (3, 15)]:
        its.append(to_min_q(H, M))
    for N in [80, 75, 90, 110, 135, 150]:
        its.append(to_hm_q(N))
    its.append(mcq("Which is <b>longer</b>: 1 h 10 min or 75 min?", "75 min",
                   ["1 h 10 min", "They are the same.", "You cannot tell."],
                   "Change 1 h 10 min to minutes: 60 + 10 = 70 min. 75 min is more than 70 min, so <b>75 min</b> is "
                   "longer. (1 h 10 min is not 110 min.)"))
    its.append(mcq("Which is <b>longer</b>: 1 h 30 min or 90 min?", "They are the same.",
                   ["1 h 30 min", "90 min", "You cannot tell."],
                   "Change 1 h 30 min to minutes: 60 + 30 = 90 min. So <b>they are the same</b>."))
    its.append(mcq("100 min = 1 h ☐ min. What is the missing number?", "40", ["0", "100", "60"],
                   "Take 60 min out of 100 min to make 1 h: 100 − 60 = <b>40</b>. So 100 min = 1 h 40 min. "
                   "(Not 0: 1 h is 60 min, not 100 min.)"))
    vals = [("1 h 15 min", 75), ("70 min", 70), ("1 h", 60), ("1 h 5 min", 65)]
    assert max(vals, key=lambda v: v[1])[0] == "1 h 15 min"
    its.append(mcq("Which is the <b>longest</b> time?", "1 h 15 min", ["70 min", "1 h", "1 h 5 min"],
                   "Change them all to minutes: 1 h 15 min = 75 min, 1 h = 60 min, 1 h 5 min = 65 min. "
                   "75 is the most, so <b>1 h 15 min</b> is the longest."))
    assert len(its) == 20
    order = [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 18, 7, 8, 9, 13, 14, 15, 16, 17, 19]
    assert sorted(order) == list(range(20))
    return {"title": "Change hours and minutes", "items": [its[i] for i in order]}


# ============================================================ set 5: word problems
def set_story(rnd, P):
    its = []

    def end_q(q, t1, d, wrongs, e):
        right = tm(t1 + d)
        assert len(set([right] + wrongs)) == 4, (right, wrongs)
        return {"q": q, "c": [right] + wrongs, "a": 0, "e": e}

    n, pr, pos = P.next()
    assert tm(T(15, 15) + 30) == "3.45 pm"
    its.append(end_q("%s starts %s homework at <b>3.15 pm</b>. %s takes <b>30 min</b>. When does %s finish?"
                     % (n, pos, cap(pr), pr), T(15, 15), 30, ["4.15 pm", "2.45 pm", "3.45 am"],
                     "Count on 30 min from 3.15 pm: 15 + 30 = 45. %s finishes at <b>3.45 pm</b>. "
                     "(4.15 pm is 1 h later. 2.45 pm is 30 min earlier.)" % cap(pr)))
    n, pr, pos = P.next()
    assert tm(T(13, 30) + 40) == "2.10 pm"
    its.append(end_q("School ends at <b>1.30 pm</b>. %s reaches home <b>40 min</b> later. When does %s reach home?"
                     % (n, pr), T(13, 30), 40, ["2.30 pm", "12.50 pm", "2.10 am"],
                     "From 1.30 pm, 30 min takes you to 2.00 pm. 40 − 30 = 10 more minutes makes <b>2.10 pm</b>. "
                     "(2.30 pm is 1 h later, not 40 min.)"))
    assert tm(T(19, 0) + 90) == "8.30 pm"
    its.append(end_q("A National Day concert at the void deck starts at <b>7.00 pm</b>. It lasts <b>1 h 30 min</b>. "
                     "When does it end?", T(19, 0), 90, ["7.30 pm", "8.30 am", "8.00 pm"],
                     "Add 1 h: 7.00 pm → 8.00 pm. Add 30 min: 8.30 pm. The concert ends at <b>8.30 pm</b>. "
                     "(7.30 pm forgets the 1 h. 8.00 pm forgets the 30 min.)"))
    assert tm(T(16, 0) - 45) == "3.15 pm" and naive(T(15, 55), T(16, 0)) == 45
    its.append({"q": "Mrs Lim’s cake needs <b>45 min</b> in the oven. It is ready at <b>4.00 pm</b>. "
                     "When did she put it in the oven?",
                "c": ["3.15 pm", "4.45 pm", "3.55 pm", "3.15 am"], "a": 0,
                "e": "Count back 45 min from 4.00 pm. 4.00 pm − 1 h = 3.00 pm, so 45 min back is 15 min after 3.00 pm: "
                     "<b>3.15 pm</b>. (3.55 pm works out 400 − 45 = 355, as if 1 h were 100 min. "
                     "4.45 pm counts forwards.)"})
    assert tm(T(10, 0) - 30) == "9.30 am"
    its.append({"q": "Recess lasts <b>30 min</b>. It ends at <b>10.00 am</b>. When does recess start?",
                "c": ["9.30 am", "10.30 am", "9.00 am", "9.30 pm"], "a": 0,
                "e": "Count back 30 min from 10.00 am: <b>9.30 am</b>. (10.30 am is 30 min after recess ends.)"})
    n, pr, pos = P.next()
    assert 25 + 40 == 65
    its.append(dq(fig(bar_parts([(25, "25 min"), (40, "40 min")], "?")) +
                  "%s reads for <b>25 min</b> in the morning and <b>40 min</b> at night. How long does %s read "
                  "altogether? Give your answer in hours and minutes." % (n, pr), 65,
                  ["1 h 65 min", "15 min", "6 h 5 min"],
                  "25 min + 40 min = 65 min. 65 min = 60 min + 5 min = <b>1 h 5 min</b>. "
                  "(Not 1 h 65 min: after taking out 1 h, only 5 min is left. Not 6 h 5 min: 65 is 65 minutes, not 6 hours.)"))
    a, b = P.next(), P.next()
    its.append(dq(fig(bar_compare([(a[0], 60, "1 h"), (b[0], 45, "?")], "15 min")) +
                  "%s’s swimming lesson is <b>1 h</b>. %s’s lesson is <b>15 min shorter</b>. How long is %s’s lesson?"
                  % (a[0], b[0], b[0]), 45, ["85 min", "1 h 15 min", "15 min"],
                  "1 h = 60 min. 60 min − 15 min = <b>45 min</b>. (85 min works out 100 − 15, as if 1 h were 100 min. "
                  "1 h 15 min adds instead of taking away.)"))
    its.append(dq(fig(bar_parts([(35, "35 min"), (25, "?")], "1 h")) +
                  "A train ride and a bus ride take <b>1 h</b> altogether. The train ride takes <b>35 min</b>. "
                  "How long is the bus ride?", 25, ["65 min", "95 min", "35 min"],
                  "1 h = 60 min. 60 min − 35 min = <b>25 min</b>. (65 min works out 100 − 35, as if 1 h were 100 min.)"))
    a, b = P.next(), P.next()
    its.append(dq(fig(bar_compare([(b[0], 70, "?"), (a[0], 50, "50 min")], "20 min")) +
                  "%s practises the piano for <b>50 min</b>. %s practises for <b>20 min longer</b>. How long does %s "
                  "practise? Give your answer in hours and minutes." % (a[0], b[0], b[0]), 70,
                  ["1 h 70 min", "30 min", "1 h 20 min"],
                  "50 min + 20 min = 70 min. 70 min = 60 min + 10 min = <b>1 h 10 min</b>. "
                  "(Not 1 h 70 min: after taking out 1 h, only 10 min is left. 30 min takes away instead of adding.)"))
    a, b = P.next(), P.next()
    assert 80 - 55 == 25
    its.append(dq(fig(bar_compare([(a[0], 80, "1 h 20 min"), (b[0], 55, "55 min")], "?")) +
                  "%s watches TV for <b>1 h 20 min</b>. %s watches TV for <b>55 min</b>. How much longer does %s watch TV?"
                  % (a[0], b[0], a[0]), 25, ["65 min", "35 min", "2 h 15 min"],
                  "Change 1 h 20 min to minutes: 60 + 20 = 80 min. 80 min − 55 min = <b>25 min</b>. "
                  "(65 min works out 120 − 55, as if 1 h were 100 min. 2 h 15 min adds the two times.)"))
    n, pr, pos = P.next()
    its.append(dq(fig(bar_parts([(20, "20 min")] * 4, "?")) +
                  "%s practises %s spelling for <b>20 min</b> each day for <b>4 days</b>. How long does %s practise "
                  "altogether? Give your answer in hours and minutes." % (n, pos, pr), 80,
                  ["1 h 80 min", "8 h", "24 min"],
                  "4 units = 4 × 20 min = 80 min. 80 min = 60 min + 20 min = <b>1 h 20 min</b>. "
                  "(Not 1 h 80 min: after taking out 1 h, only 20 min is left. Not 24 min: 20 + 4 adds instead of "
                  "multiplying.)"))
    assert naive(T(9, 30), T(12, 30)) == 300
    its.append(dq("Primary 2 students visit the Singapore Zoo from <b>9.30 am</b> to <b>12.30 pm</b>. "
                  "How long is the visit?", 180, ["4 h", "3 h 30 min", "300 min"],
                  "Count the jumps: 9.30 am → 10.30 am → 11.30 am → 12.30 pm. That is 3 jumps of 1 h, so the visit is "
                  "<b>3 h</b>. (4 h counts the numbers 9, 10, 11 and 12. 300 min counts 1 h as 100 min.)"))
    assert naive(T(8, 0), T(11, 30)) == 330
    its.append(dq("Sports Day starts at <b>8.00 am</b> and ends at <b>11.30 am</b>. How long is Sports Day?", 210,
                  ["3 h", "4 h 30 min", "330 min"],
                  "8.00 am to 11.00 am is 3 h. 11.00 am to 11.30 am is 30 min. So Sports Day is <b>3 h 30 min</b>. "
                  "(330 min works out 1130 − 800, as if 1 h were 100 min.)"))
    n, pr, pos = P.next()
    assert T(9, 40) + 35 + 10 == T(10, 25)
    its.append(end_q("%s leaves home at <b>9.40 am</b>. %s takes the MRT for <b>35 min</b>. Then %s walks for "
                     "<b>10 min</b> to the library. When does %s reach the library?" % (n, cap(pr), pr, pr),
                     T(9, 40), 45, ["10.15 am", "11.25 am", "10.25 pm"],
                     "The trip takes 35 min + 10 min = 45 min. From 9.40 am, 20 min takes you to 10.00 am. "
                     "45 − 20 = 25 more minutes makes <b>10.25 am</b>. (10.15 am forgets the 10-min walk.)"))
    assert tm(T(10, 45) + 120) == "12.45 pm"
    its.append(end_q("Mdm Wong’s flight leaves Changi Airport at <b>10.45 am</b>. The flight takes <b>2 h</b>. "
                     "What time is it in Singapore when the flight lands?", T(10, 45), 120,
                     ["12.45 am", "11.45 am", "8.45 am"],
                     "Count on 2 h: 10.45 am → 11.45 am → 12.45. We passed 12 noon, so it is <b>12.45 pm</b>. "
                     "(12.45 am would be after 12 midnight.)"))
    t1, t2 = T(16, 30), T(18, 0)
    assert naive(t1, t2) == 170
    n, pr, pos = P.next()
    its.append(dq(fig(start_end_svg(4, 30, 6, 0)) +
                  "The clocks show when %s’s football training starts and ends in the afternoon. How long is the "
                  "training?" % n, 90, ["170 min", "2 h 30 min", "1 h"],
                  "4.30 pm to 5.00 pm is 30 min. 5.00 pm to 6.00 pm is 1 h. So it is <b>1 h 30 min</b>. "
                  "(170 min works out 600 − 430, as if 1 h were 100 min.)"))
    n, pr, pos = P.next()
    assert naive(T(8, 50), T(9, 35)) == 85
    its.append(dq("%s’s family leaves home at <b>8.50 am</b>. They reach Sentosa at <b>9.35 am</b>. "
                  "How long is the trip?" % n, 45, ["85 min", "1 h 45 min", "15 min"],
                  "8.50 am to 9.00 am is 10 min. 9.00 am to 9.35 am is 35 min. 10 + 35 = <b>45 min</b>. "
                  "(85 min works out 935 − 850, as if 1 h were 100 min.)"))
    n, pr, pos = P.next()
    its.append(dq("%s goes to bed at <b>9.00 pm</b>. %s wakes up at <b>6.00 am</b> the next morning. How long does "
                  "%s sleep?" % (n, cap(pr), pr), 540, ["3 h", "15 h", "8 h"],
                  "9.00 pm to 12 midnight is 3 h. 12 midnight to 6.00 am is 6 h. 3 h + 6 h = <b>9 h</b>. "
                  "(3 h works out 9 − 6. 15 h adds 9 and 6.)"))
    assert 45 + 15 + 45 == 105
    its.append(dq(fig(bar_parts([(45, "45 min"), (15, "15 min"), (45, "45 min")], "?")) +
                  "A Chinese New Year concert has two parts of <b>45 min</b> each, with a <b>15 min</b> break in between. "
                  "How long is the whole concert?", 105, ["1 h 5 min", "60 min", "2 h 45 min"],
                  "45 + 15 + 45 = 105 min. 105 min = 60 min + 45 min = <b>1 h 45 min</b>. "
                  "(1 h 5 min counts 1 h as 100 min. 60 min forgets the second part.)"))
    a, b = P.next(), P.next()
    its.append(dq("%s spends <b>1 h 15 min</b> at Gardens by the Bay. %s spends <b>20 min longer</b> there. "
                  "How long does %s spend there?" % (a[0], b[0], b[0]), 95,
                  ["55 min", "1 h 20 min", "35 min"],
                  "1 h 15 min + 20 min: add the minutes, 15 + 20 = 35. So it is <b>1 h 35 min</b>. (55 min takes away instead of adding. 35 min forgets the 1 h.)"))
    assert len(its) == 20
    order = [0, 4, 1, 2, 5, 7, 6, 3, 8, 11, 14, 19, 9, 12, 15, 16, 10, 13, 18, 17]
    assert sorted(order) == list(range(20))
    return {"title": "Time word problems", "items": [its[i] for i in order]}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The two hands</h2>"
        "<p>A clock has two hands. The short <b>hour hand</b> shows the hour. The long <b>minute hand</b> shows the "
        "minutes. Each number is <b>5 min</b> for the minute hand, so count in 5s. Between two numbers there are "
        "5 small marks. Each small mark is <b>1 min</b>.</p>"
        "<figure class='sn-fig'>" + clock_svg(4, 37, size=240, ring=True) +
        "<figcaption>The red numbers show the minutes. The minute hand is 2 marks past the 7: count 35, then 36, 37. "
        "The hour hand is between 4 and 5. It has not reached 5, so the hour is 4. It is <b>4.37</b>.</figcaption></figure>"
        + ex("Read the clock", "The hour hand is between 9 and 10. The minute hand points to 4.",
             "The hour is 9. Count in 5s to the 4: 5, 10, 15, 20.", "9.20") +
        "<h2>am and pm</h2>"
        "<p><b>am</b>: from 12 midnight to 12 noon (night and morning). "
        "<b>pm</b>: from 12 noon to 12 midnight (afternoon and evening).</p>"
        + table(["What happens", "Time"], [["Wake up for school", "6.15 am"], ["Recess", "9.40 am"],
                                          ["Lunch", "12.30 pm"], ["Dinner", "7.20 pm"]]) +
        "<h2>How long?</h2>"
        "<p>1 h = <b>60 min</b>, not 100 min. Count on to the next o’clock first, then on to the end time.</p>"
        "<figure class='sn-fig'>" + timeline_svg(T(10, 40), T(11, 15)) +
        "<figcaption>From 10.40 am to 11.15 am: 20 min to 11.00 am, then 15 min more. 20 + 15 = <b>35 min</b>.</figcaption>"
        "</figure>"
        + ex("Find the end time", "A show starts at 7.00 pm. It lasts 1 h 30 min. When does it end?",
             "Add 1 h: 8.00 pm. Add 30 min: 8.30 pm.", "8.30 pm") +
        "<h2>Change hours and minutes</h2>"
        + table(["Hours and minutes", "Minutes"], [["1 h", "60 min"], ["1 h 20 min", "60 + 20 = 80 min"],
                                                  ["2 h", "120 min"], ["2 h 15 min", "120 + 15 = 135 min"]]) +
        "<p>To change minutes to hours and minutes, take out groups of 60 min.</p>"
        + ex("Minutes to h and min", "Change 80 min to hours and minutes.",
             "80 = 60 + 20. 60 min is 1 h, and 20 min is left.", "1 h 20 min") +
        "<h2>Word problems with a model</h2>"
        "<figure class='sn-fig'>" + bar_parts([(25, "25 min"), (40, "40 min")], "?") +
        "<figcaption>Hui Min reads for 25 min and then 40 min. 25 + 40 = 65 min = <b>1 h 5 min</b>.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Hour hand read as the minutes: 3.45 read as 9.15", "The short hand is the hour. The long hand is the minutes"],
            ["Minute hand on 4 read as 4 min", "Each number is 5 min: 4 × 5 = 20 min"],
            ["Hour hand just before 5 read as 5", "It has not reached 5 yet, so the hour is still 4"],
            ["1 h = 100 min: 11.15 − 10.40 = 75 min", "1 h = 60 min. Count on: 20 + 15 = 35 min"],
            ["80 min = 1 h 80 min", "Take out 60 min: 80 − 60 = 20. 80 min = 1 h 20 min"],
            ["Breakfast at 7.00 pm", "Morning times are am: 7.00 am"],
        ])
    )


FAQ = [
    {"q": "What is taught in P2 time?",
     "a": "In Primary 2, students tell time to the minute, use am and pm, find how long something takes in hours "
          "and minutes, and change hours and minutes to minutes and back."},
    {"q": "How do I change hours and minutes into minutes?",
     "a": "Change each hour to 60 min, then add the minutes. For example, 1 h 20 min = 60 + 20 = 80 min."},
    {"q": "What is the most common mistake in P2 time?",
     "a": "The most common mistake is treating 1 h as 100 min, for example writing 80 min as 1 h 80 min or "
          "working out 11.15 − 10.40 as 75 min. Remind your child that 1 h is 60 min."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. Telling time, measuring time in hours and minutes and converting hours and minutes are part of "
          "Measurement in the MOE 2021 Primary 2 Mathematics Syllabus (Standard Mathematics)."},
]


def gen():
    rnd = random.Random(62810)
    P = People(rnd)
    sets = [set_clocks(rnd), set_ampm(rnd, P), set_how_long(rnd, P), set_convert(rnd, P), set_story(rnd, P)]
    balance(sets, rnd)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [dval(c) for c in it["c"]]
            if None not in vals:
                assert len(set(vals)) == 4, it["c"]
            assert it["q"].count("<svg") <= 1, it["q"]
            assert it["q"] not in qs, it["q"]
            qs.add(it["q"])
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
                assert not re.search(r"\d:\d\d", re.sub(r"<svg.*?</svg>", "", x)), x
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "time", "sort": 10,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Time: Telling Time, am and pm, Hours and Minutes",
        "seo_title": "P2 Time Worksheets: Free Primary 2 Maths on Telling Time, Hours and Minutes with Answers (MOE Syllabus)",
        "short_title": "Time",
        "domain": "Measurement and Geometry",
        "standard_code": "Primary 2: Measurement",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Telling time to the minute; measuring time in hours and minutes; converting hours and minutes",
        "meta_desc": "Free P2 maths practice on time: read clocks to the minute, am and pm, how long, and changing "
                     "h and min. 100 questions with answers.",
        "key_big": "1 h = 60 min, not 100 min.",
        "key_sub": "1 h 20 min = 60 + 20 = 80 min, and 80 min = 1 h 20 min.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160
    return mark_large(u, "bar model|time line|four clocks|start and end clocks")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
