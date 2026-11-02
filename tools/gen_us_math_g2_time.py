# -*- coding: utf-8 -*-
"""
US Grade 2 Math: Telling Time to the Nearest Five Minutes (2.MD.C.7)
  python tools/gen_us_math_g2_time.py
Every time is a real clock time on a 5-minute mark. Every clock picture is drawn from the time itself
(the short hand moves between the numbers as the minutes go by).
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-2")
UPDATED = "2026-11-02"
GREEN = "#006633"
LINE = "#2b2b2b"
RED = "#d6453b"
GRAY = "#b9b2a6"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ time
def tm(h, m, ap=""):
    assert 0 <= m < 60, m
    h = (h - 1) % 12 + 1
    return "%d:%02d%s" % (h, m, (" " + ap) if ap else "")


def hands_gap(h, m):
    """Angle in degrees between the short hand and the long hand."""
    d = abs(((h % 12) + m / 60.0) * 30 - m * 6) % 360
    return min(d, 360 - d)


def nxt(h):
    return h % 12 + 1


def prv(h):
    return (h - 2) % 12 + 1


def mins(n):
    return "%d minute%s" % (n, "" if n == 1 else "s")


# ------------------------------------------------------------ helpers
def tidy(t):
    return t.replace("a.m..", "a.m.").replace("p.m..", "p.m.").replace("m.</b>.", "m.</b>")


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
    return {"q": tidy(q), "c": [correct] + pick, "a": 0, "e": tidy(e)}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set.
    Items marked 'fixed' (A-D clock pictures) already have their position; the rest fill the gaps."""
    for s in sets:
        left = {0: 5, 1: 5, 2: 5, 3: 5}
        for it in s["items"]:
            if it.get("fixed"):
                left[it["a"]] -= 1
        targets = [p for p in range(4) for _ in range(left[p])]
        assert min(left.values()) >= 0
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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def clock_body(h, m, cx, cy, R, ring=False):
    """Clock face with numbers. The short hand is placed by the exact time: (h + m/60) x 30 degrees."""
    k = R / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, R, GREEN, 5 * k)]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (13 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (R - 3 * k) * math.cos(a), cy + (R - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), LINE, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), LINE, 2.6 * k))
    # hands first; the numbers are drawn on top with a white edge so they stay easy to read
    if h is not None:
        ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
        am = math.radians(m * 6 - 90)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                 % (cx, cy, cx + R * 0.5 * math.cos(ah), cy + R * 0.5 * math.sin(ah), LINE, 8 * k))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                 % (cx, cy, cx + R * 0.86 * math.cos(am), cy + R * 0.86 * math.sin(am), RED, 4.5 * k))
    fs = 19 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, LINE, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = R - 29 * k
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    if ring:      # minutes written outside the face
        s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle'>" % (14 * k, RED))
        for n in range(1, 13):
            a = math.radians(n * 30 - 90)
            rn = R + 17 * k
            s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + 5 * k, (n * 5) % 60))
        s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, 6 * k, LINE))
    return "".join(s)


def clock_svg(h, m, size=200, ring=False):
    pad = 26 if ring else 0
    c = size / 2.0
    return svg_wrap(size, size, clock_body(h, m, c, c, c - 6 - pad, ring), "clock showing %s" % tm(h, m))


def clocks4_svg(times):
    """2 x 2 grid of clocks labeled A-D (square picture, printed large)."""
    CELL = 124
    W = H = 2 * CELL
    el = ["<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, CELL, H - 4, GRAY),
          "<line x1='4' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (CELL, W - 4, CELL, GRAY)]
    for k, (h, m) in enumerate(times):
        assert hands_gap(h, m) >= 12, (h, m)
        x0, y0 = (k % 2) * CELL, (k // 2) * CELL
        el.append(clock_body(h, m, x0 + 65, y0 + 63, 56))
        el.append("<text x='%d' y='%d' font-size='18' font-weight='700' fill='%s'>%s</text>" % (x0 + 5, y0 + 20, LINE, "ABCD"[k]))
    return svg_wrap(W, H, "".join(el), "four clocks labeled A to D")


def digital_svg(t):
    W, H = 190, 84
    s = ["<rect x='4' y='4' width='%d' height='%d' rx='14' fill='#fff' stroke='%s' stroke-width='5'/>" % (W - 8, H - 8, GREEN),
         "<rect x='18' y='16' width='%d' height='%d' rx='6' fill='#eef5f0' stroke='%s' stroke-width='1.5'/>" % (W - 36, H - 32, GRAY),
         "<text x='%d' y='%d' font-size='42' font-weight='700' fill='%s' text-anchor='middle'>%s</text>" % (W // 2, H // 2 + 15, LINE, t)]
    return svg_wrap(W, H, "".join(s), "digital clock showing %s" % t)


# ------------------------------------------------------------ reading a clock
def read_cands(h, m):
    """Real wrong readings of a clock showing h:m, most likely first."""
    n = m // 5
    c = []
    if m >= 30:
        c.append(tm(nxt(h), m))                          # short hand is near the next number
    if 5 <= m and n != h and 5 * h < 60:
        c.append(tm(n, 5 * h))                           # hands switched
    if m >= 10 and n not in (0,):
        c.append("%d:%02d" % (h, n))                     # number read as minutes (3:04 for 3:20)
    if m < 30:
        c.append(tm(nxt(h), m))
    c.append(tm(prv(h), m))
    c.append(tm(h, (m + 5) % 60))
    c.append(tm(h, (m - 5) % 60))
    return c


def read_e(h, m):
    n = m // 5
    if m == 0:
        hr = "The short hand points to the <b>%d</b>." % h
        mn = "The long hand points to the <b>12</b>, so it is 0 minutes: write :00."
    else:
        near = " It is almost at the %d, but it has not got there yet." % nxt(h) if m >= 40 else ""
        hr = "The short hand is <b>between %d and %d</b>, so the hour is <b>%d</b>.%s" % (h, nxt(h), h, near)
        mn = "The long hand points to the <b>%d</b>. Count by 5s: <b>%s</b>." % (n, ", ".join(str(5 * i) for i in range(1, n + 1)))
    return "%s %s It is %s." % (hr, mn, tm(h, m))


# ============================================================ set 1: hour and half hour
def set_hour_half(rnd):
    its = []
    hrs = rnd.sample(range(1, 13), 8)
    for i, h in enumerate(hrs):
        if i % 2 == 0:
            right = tm(h, 0)
            cands = [tm(12, 5 * h) if h < 12 else None, "%d:12" % h, tm(h, 30), tm(nxt(h), 0), tm(prv(h), 0)]
            e = ("The short hand points to the <b>%d</b>. The long hand points to the <b>12</b>. "
                 "That means it is %d o'clock: <b>%s</b>." % (h, h, right))
        else:
            right = tm(h, 30)
            cands = [tm(nxt(h), 30), "%d:06" % h, tm(6, 5 * h) if h not in (6, 12) else None, tm(h, 0), tm(prv(h), 30)]
            e = ("The long hand points to the <b>6</b>. That is 30 minutes, half of the way around. "
                 "The short hand is halfway <b>between %d and %d</b>, so the hour is still %d. It is <b>%s</b>, half past %d."
                 % (h, nxt(h), h, right, h))
        its.append(mcq(fig(clock_svg(h, 0 if i % 2 == 0 else 30)) + "What time is it?", right, cands, e))

    used = {(h, 0 if i % 2 == 0 else 30) for i, h in enumerate(hrs)}

    def pick(m, avoid=()):
        h = rnd.choice([x for x in range(2, 12) if (x, m) not in used and x not in avoid])
        used.add((h, m))
        return h

    h1, h2 = pick(30), pick(0)
    its.append(mcq("What time is <b>half past %d</b>?" % h1, tm(h1, 30), [tm(nxt(h1), 30), tm(h1, 50), tm(prv(h1), 30)],
                   "<b>Half past %d</b> means 30 minutes after %d o'clock. That is <b>%s</b>." % (h1, h1, tm(h1, 30))))
    its.append(mcq("What time is <b>%d o'clock</b>?" % h2, tm(h2, 0), [tm(h2, 30), "%d:12" % h2, tm(12, 5 * h2)],
                   "%d o'clock means the hour is %d and there are 0 minutes. Write it as <b>%s</b>." % (h2, h2, tm(h2, 0))))
    h3 = pick(30)
    its.append(mcq("How do you say <b>%s</b>?" % tm(h3, 30), "half past %d" % h3,
                   ["half past %d" % nxt(h3), "%d o'clock" % h3, "half past %d" % prv(h3)],
                   "30 minutes after %d o'clock is <b>half past %d</b>." % (h3, h3)))
    h4 = pick(0)
    its.append(mcq("How do you say <b>%s</b>?" % tm(h4, 0), "%d o'clock" % h4,
                   ["half past %d" % h4, "%d o'clock" % nxt(h4), "12 o'clock"],
                   "The minutes are :00, so it is right on the hour: <b>%d o'clock</b>." % h4))

    h5, h6 = pick(0), pick(30, avoid=(3, 6))
    its.append(mcq("At <b>%s</b>, where does the long hand point?" % tm(h5, 0), "12", [str(h5), "6", "1"],
                   "At an o'clock time the long hand always points straight up to the <b>12</b>. The short hand points to the %d." % h5))
    its.append(mcq("At <b>%s</b>, where does the long hand point?" % tm(h6, 30), "6", ["3", str(h6), "12"],
                   "30 minutes is half of the way around the clock. The long hand points to the <b>6</b>. "
                   "Count by 5s: 5, 10, 15, 20, 25, 30. (It is not the 3. The 3 means 15 minutes.)"))
    h7, h8 = pick(30), pick(0)
    its.append(mcq("At <b>%s</b>, where is the short hand?" % tm(h7, 30), "between %d and %d" % (h7, nxt(h7)),
                   ["on the %d" % h7, "on the %d" % nxt(h7), "between %d and %d" % (prv(h7), h7)],
                   "In 30 minutes the short hand moves halfway to the next number. At %s it is halfway "
                   "<b>between %d and %d</b>." % (tm(h7, 30), h7, nxt(h7))))
    its.append(mcq("At <b>%s</b>, where is the short hand?" % tm(h8, 0), "on the %d" % h8,
                   ["on the 12", "between %d and %d" % (h8, nxt(h8)), "on the %d" % nxt(h8), "between %d and %d" % (prv(h8), h8)],
                   "At %d o'clock the short hand points right <b>on the %d</b>. The long hand is on the 12." % (h8, h8)))

    h9 = pick(0)
    its.append(mcq("It is <b>%s</b>. What time will it be in half an hour?" % tm(h9, 0), tm(h9, 30),
                   [tm(nxt(h9), 0), tm(h9, 50), tm(nxt(h9), 30)],
                   "Half an hour is 30 minutes. The long hand moves from the 12 to the 6. %s + 30 minutes = <b>%s</b>."
                   % (tm(h9, 0), tm(h9, 30))))
    h10 = pick(30, avoid=(11,))
    its.append(mcq("It is <b>%s</b>. What time will it be in half an hour?" % tm(h10, 30), tm(nxt(h10), 0),
                   [tm(h10, 0), tm(nxt(h10), 30), tm(h10, 50)],
                   "30 more minutes takes the long hand from the 6 back up to the 12. That is the next hour: <b>%s</b>."
                   % tm(nxt(h10), 0)))
    its.append(mcq("How many minutes are in <b>half an hour</b>?", mins(30), [mins(50), mins(15), mins(60)],
                   "1 hour is 60 minutes. Half of 60 is <b>30 minutes</b>."))
    its.append(mcq("How many minutes are in <b>1 hour</b>?", mins(60), [mins(100), mins(12), mins(30)],
                   "The long hand goes all the way around the clock in 1 hour. Count by 5s to the 12: <b>60 minutes</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Hour and half hour", "items": its}


# ============================================================ set 2: count by 5s around the clock
def minute_cands(n):
    out = [mins(n), mins(5 * (n + 1)) if n < 11 else None, mins(5 * (n - 1)) if n > 1 else None,
           mins(10 * n) if 10 * n < 60 else None, mins(5 * n + 10) if 5 * n + 10 < 60 else None, mins(5 * n - 10) if n > 2 else None]
    return out


def count_e(n):
    return ("Each number on the clock is 5 minutes. Count by 5s to the %d: <b>%s</b>. So it is <b>%s</b>."
            % (n, ", ".join(str(5 * i) for i in range(1, n + 1)), mins(5 * n)))


def set_count5(rnd):
    its = []
    fig_n = [3, 4, 7, 2, 9, 11, 5, 8]
    hrs = rnd.sample(range(1, 13), 8)
    for n, h in zip(fig_n, hrs):
        if n == h:
            h = nxt(h)
        q = fig(clock_svg(h, 5 * n)) + "The long hand points to the <b>%d</b>. How many minutes after %d o'clock is it?" % (n, h)
        its.append(mcq(q, mins(5 * n), minute_cands(n), count_e(n)))
    for n in [1, 6, 10, 4, 8, 11]:
        q = "The long hand is on the <b>%d</b>. How many minutes after the hour is it?" % n
        c = minute_cands(n)
        if n == 1:
            c = [mins(1), mins(10), mins(15)]
        e = count_e(n) if n > 1 else "Each number on the clock is 5 minutes. The 1 is the first number after the 12, so it is <b>5 minutes</b>."
        its.append(mcq(q, mins(5 * n), c, e))
    its.append(mcq("The long hand moves from the 12 to the 3. How many minutes go by?", mins(15),
                   [mins(3), mins(30), mins(20)], "Count by 5s for each number: 5, 10, 15. <b>15 minutes</b> go by."))
    its.append(mcq("The long hand moves from the 12 to the 8. How many minutes go by?", mins(40),
                   [mins(8), mins(35), mins(45)], "Count by 5s for each number: 5, 10, 15, 20, 25, 30, 35, 40. <b>40 minutes</b> go by."))
    its.append(mcq("The long hand goes all the way around, from the 12 back to the 12. How much time goes by?", "1 hour",
                   [mins(12), "1 minute", mins(100)],
                   "12 numbers × 5 minutes = 60 minutes. 60 minutes is <b>1 hour</b>."))
    its.append(mcq("It is <b>10 minutes</b> after the hour. Where does the long hand point?", "the 2",
                   ["the 10", "the 1", "the 3"],
                   "Count by 5s: 5 is the 1, 10 is the <b>2</b>. (The 10 on the clock means 50 minutes.)"))
    its.append(mcq("It is <b>40 minutes</b> after the hour. Where does the long hand point?", "the 8",
                   ["the 4", "the 7", "the 9"],
                   "Count by 5s until you say 40: 5, 10, 15, 20, 25, 30, 35, 40. That is 8 numbers, so the long hand is on the <b>8</b>."))
    its.append(mcq("It is <b>55 minutes</b> after the hour. Where does the long hand point?", "the 11",
                   ["the 5", "the 10", "the 12"],
                   "55 is 5 minutes before the hour, one number before the 12. The long hand is on the <b>11</b>."))
    assert len(its) == 20, len(its)
    return {"title": "Count by 5s around the clock", "items": its}


# ============================================================ set 3: read the clock to 5 minutes
def set_read(rnd):
    its = []
    ms = [5, 10, 15, 20, 25, 35, 40, 45, 50, 55] + [5, 10, 20, 25, 35, 40, 45, 50, 55, 15]
    hs = list(range(1, 13)) + rnd.sample(range(1, 13), 8)
    rnd.shuffle(hs)
    seen = set()
    for m, h in zip(ms, hs):
        while (h, m) in seen or hands_gap(h, m) < 20:      # hands on top of each other are hard to read
            h = nxt(h)
        seen.add((h, m))
        its.append(mcq(fig(clock_svg(h, m)) + "What time is it?", tm(h, m), read_cands(h, m), read_e(h, m)))
    # harder ones last: the short hand is close to the next number
    its.sort(key=lambda it: int(re.search(r"showing \d+:(\d+)", it["q"]).group(1)) >= 40)
    assert len(its) == 20
    return {"title": "Read the clock to 5 minutes", "items": its}


# ============================================================ set 4: match clocks, quarter hours, the short hand
def set_match(rnd, P):
    its = []
    picks = [(1, 35), (4, 10), (2, 50), (9, 25), (5, 40), (11, 15)]
    pos = [0, 1, 2, 3, 1, 2]
    for (h, m), p in zip(picks, pos):
        n = m // 5
        wrong = [(nxt(h), m), (h, (m + 5) % 60), (h, (m - 5) % 60)]
        swap = (n, 5 * h) if 5 * h < 60 and n != h else None
        if swap:
            wrong = [swap, wrong[0], wrong[1] if m < 30 else wrong[2]]
        wrong = wrong[:3]
        rnd.shuffle(wrong)
        times = wrong[:p] + [(h, m)] + wrong[p:]
        assert len(set(times)) == 4
        L = "ABCD"[p]
        e = ("In Clock %s the short hand is between %d and %d, so the hour is %d. The long hand is on the %d: "
             "count by 5s to <b>%d</b>. Clock %s shows %s." % (L, h, nxt(h), h, n, m, L, tm(h, m)))
        if swap:
            sL = "ABCD"[times.index(swap)]
            e += " Clock %s has the hands switched." % sL
        its.append({"q": fig(clocks4_svg(times)) + "Which clock shows <b>%s</b>?" % tm(h, m),
                    "c": ["A", "B", "C", "D"], "a": p, "e": e, "fixed": True})

    for h, m in [(4, 50), (9, 20), (11, 35), (6, 45)]:
        n = m // 5
        tens = m // 10
        its.append(mcq(fig(digital_svg(tm(h, m))) + "This digital clock shows %s. On a clock with hands, where does the long hand point?" % tm(h, m),
                       "the %d" % n, ["the %d" % tens, "the %d" % (n - 1), "the %d" % (n + 1), "the %d" % h],
                       "The minutes are %d. Count by 5s until you say %d: that is %d numbers. The long hand points to the <b>%d</b>. "
                       "(The %d on the clock means %d minutes.)" % (m, m, n, n, tens, 5 * tens)))

    h = rnd.choice([2, 4, 8])
    its.append(mcq("What time is <b>quarter past %d</b>?" % h, tm(h, 15), [tm(h, 25), tm(h, 45), tm(prv(h), 45)],
                   "A quarter hour is 15 minutes. <b>Quarter past %d</b> means 15 minutes after %d o'clock: <b>%s</b>." % (h, h, tm(h, 15))))
    h2 = rnd.choice([6, 10, 3])
    its.append(mcq("What time is <b>quarter to %d</b>?" % h2, tm(prv(h2), 45), [tm(h2, 45), tm(h2, 15), tm(prv(h2), 15)],
                   "<b>Quarter to %d</b> means 15 minutes <b>before</b> %d o'clock. 15 minutes before %s is <b>%s</b>."
                   % (h2, h2, tm(h2, 0), tm(prv(h2), 45))))
    its.append(mcq(fig(clock_svg(8, 15)) + "What is another way to say this time?", "quarter past 8",
                   ["quarter to 8", "half past 8", "quarter past 9"],
                   "The long hand is on the 3: that is 15 minutes, a quarter of the way around. "
                   "The short hand is just past the 8. It is 8:15, <b>quarter past 8</b>."))
    its.append(mcq(fig(clock_svg(10, 45)) + "What is another way to say this time?", "quarter to 11",
                   ["quarter to 10", "quarter past 10", "half past 10"],
                   "The clock shows 10:45. In 15 more minutes it will be 11 o'clock, so 10:45 is <b>quarter to 11</b>."))
    its.append(mcq("How many minutes are in a <b>quarter hour</b>?", mins(15), [mins(25), mins(4), mins(30)],
                   "A quarter is 1 of 4 equal parts. The long hand moves from the 12 to the 3: <b>15 minutes</b>. "
                   "(A quarter coin is 25 cents, but a quarter hour is 15 minutes.)"))

    for h, m in [(3, 35), (1, 20)]:
        its.append(mcq("It is <b>%s</b>. Where is the short hand?" % tm(h, m), "between %d and %d" % (h, nxt(h)),
                       ["on the %d" % h, "on the %d" % nxt(h), "between %d and %d" % (prv(h), h)],
                       "The short hand moves a little as the minutes go by. At %s it has left the %d but has not reached the %d. "
                       "It is <b>between %d and %d</b>." % (tm(h, m), h, nxt(h), h, nxt(h))))
    its.append(mcq("At <b>2:50</b>, which number is the short hand closest to?", "3", ["2", "10", "11"],
                   "At 2:50 it is almost 3 o'clock. The short hand is between 2 and 3, very close to the <b>3</b>. "
                   "(The long hand is the one on the 10.)"))
    its.append(mcq("At <b>8:10</b>, which number is the short hand closest to?", "8", ["9", "2", "10"],
                   "At 8:10 the hour has just started. The short hand is just past the <b>8</b>. "
                   "(The long hand is the one on the 2.)"))
    its.append(mcq(fig(clock_svg(4, 55)) + "The short hand is almost on the 5. What time is it?", tm(4, 55),
                   [tm(5, 55), "4:11", tm(5, 0)],
                   "The short hand has <b>not reached</b> the 5 yet, so the hour is still 4. The long hand is on the 11: "
                   "11 × 5 = 55 minutes. It is <b>4:55</b>. In 5 more minutes it will be 5:00."))
    assert len(its) == 20, len(its)
    return {"title": "Match clocks, quarter hours and the short hand", "items": its}


# ============================================================ set 5: a.m., p.m. and later times
ACTS = [  # question with {n}/{he}/{his}, right, wrong, why
    ("{n} eats breakfast before school. What time could it be?", "7:15 a.m.", ["7:15 p.m.", "1:15 p.m.", "10:15 p.m."],
     "Breakfast is in the <b>morning</b>, so it is an <b>a.m.</b> time: 7:15 a.m."),
    ("{n} wakes up for school. What time could it be?", "6:45 a.m.", ["6:45 p.m.", "11:45 p.m.", "2:45 p.m."],
     "Waking up for school happens in the <b>morning</b>. Morning times are <b>a.m.</b>: 6:45 a.m."),
    ("School starts. What time could it be?", "8:05 a.m.", ["8:05 p.m.", "3:05 a.m.", "11:05 p.m."],
     "School starts in the <b>morning</b>, so it is <b>a.m.</b>: 8:05 a.m. (3:05 a.m. is the middle of the night.)"),
    ("{n} plays outside at morning recess. What time could it be?", "10:20 a.m.", ["10:20 p.m.", "3:20 a.m.", "7:20 p.m."],
     "Morning recess is during the school day, before noon. That is <b>a.m.</b>: 10:20 a.m."),
    ("{n} rides the bus home from school. What time could it be?", "3:10 p.m.", ["3:10 a.m.", "10:10 p.m.", "6:10 a.m."],
     "School ends in the <b>afternoon</b>. Afternoon times are <b>p.m.</b>: 3:10 p.m."),
    ("{n} eats a snack after school. What time could it be?", "3:45 p.m.", ["3:45 a.m.", "9:45 a.m.", "11:45 p.m."],
     "After school is the <b>afternoon</b>. Afternoon times are <b>p.m.</b>: 3:45 p.m."),
    ("{n} eats dinner with {his} family. What time could it be?", "6:00 p.m.", ["6:00 a.m.", "10:00 a.m.", "2:00 a.m."],
     "Dinner is in the <b>evening</b>. Evening times are <b>p.m.</b>: 6:00 p.m."),
    ("{n} goes to bed at night. What time could it be?", "8:30 p.m.", ["8:30 a.m.", "12:30 p.m.", "3:30 p.m."],
     "Going to bed happens at <b>night</b>, after noon and before midnight. That is <b>p.m.</b>: 8:30 p.m."),
    ("{n} is fast asleep. It is the middle of the night. What time could it be?", "2:00 a.m.", ["2:00 p.m.", "9:00 a.m.", "5:00 p.m."],
     "After midnight a new day starts, and the times are <b>a.m.</b> The middle of the night is a time like 2:00 a.m."),
]


def set_ampm(rnd, P):
    its = []
    for q, a, w, e in ACTS:
        n, he, his = P.next()
        its.append(mcq(q.format(n=n, he=he, his=his), a, w, e))
    n, he, his = P.next()
    its.append(mcq("It is 9:00 p.m. What is %s most likely doing?" % n, "sleeping", ["at school", "eating lunch", "eating breakfast"],
                   "9:00 p.m. is late in the evening, so %s is most likely <b>sleeping</b>. At 9:00 a.m. %s would be at school." % (n, he)))
    n, he, his = P.next()
    its.append(mcq("It is 7:00 a.m. What is %s most likely doing?" % n, "eating breakfast", ["eating dinner", "going to bed", "at recess"],
                   "7:00 a.m. is early in the morning, before school, so %s is most likely <b>eating breakfast</b>. "
                   "Dinner and bedtime are p.m." % n))

    # later times: 1 hour and 30 minutes
    its.append(mcq("It is <b>4:15</b>. What time will it be in <b>1 hour</b>?", "5:15", ["4:16", "3:15", "6:15"],
                   "In 1 hour the short hand moves to the next number. The minutes stay the same. 4:15 → <b>5:15</b>. "
                   "(4:16 is only 1 minute later.)"))
    its.append(mcq(fig(clock_svg(2, 40)) + "What time will it be in <b>1 hour</b>?", "3:40", ["2:41", "1:40", "4:40"],
                   "The clock shows 2:40. In 1 hour the hour goes up by 1 and the minutes stay the same: <b>3:40</b>."))
    its.append(mcq("It is <b>2:10</b>. What time will it be in <b>30 minutes</b>?", "2:40", ["3:10", "2:30", "2:25"],
                   "Count on by 5s from the 2: 30 minutes is 6 numbers. The long hand goes from the 2 to the 8. 2:10 → <b>2:40</b>. "
                   "(3:10 is 1 hour later, not 30 minutes.)"))
    its.append(mcq("It is <b>9:45</b>. What time will it be in <b>30 minutes</b>?", "10:15", ["9:15", "10:45", "11:15"],
                   "Count on 15 minutes to 10:00, then 15 more minutes: <b>10:15</b>. "
                   "The long hand went past the 12, so the hour goes up to 10."))

    # word problems
    n, he, his = P.next()
    its.append(mcq("%s's soccer practice starts at 4:30 p.m. It lasts 1 hour. What time does it end?" % n, "5:30 p.m.",
                   ["5:30 a.m.", "4:31 p.m.", "6:30 p.m."],
                   "1 hour after 4:30 is 5:30. It is still the afternoon, so it is <b>5:30 p.m.</b>"))
    n, he, his = P.next()
    its.append(mcq("%s gets to the park at 10:15 a.m. %s stays for 1 hour. What time does %s leave?" % (n, cap(he), he), "11:15 a.m.",
                   ["11:15 p.m.", "10:16 a.m.", "9:15 a.m."],
                   "1 hour after 10:15 is 11:15. It is still before noon, so it is <b>11:15 a.m.</b>"))
    n, he, his = P.next()
    its.append(mcq("%s's piano lesson starts at 2:00 p.m. It lasts half an hour. What time does it end?" % n, "2:30 p.m.",
                   ["3:00 p.m.", "2:15 p.m.", "2:30 a.m."],
                   "Half an hour is 30 minutes. 2:00 + 30 minutes = <b>2:30 p.m.</b> (2:15 is only a quarter hour later.)"))
    n, he, his = P.next()
    its.append(mcq("%s starts %s homework at 3:40 p.m. %s works for 30 minutes. What time does %s finish?" % (n, his, cap(he), he),
                   "4:10 p.m.", ["3:10 p.m.", "4:40 p.m.", "4:10 a.m."],
                   "Count on 20 minutes from 3:40 to 4:00. Then 10 more minutes: <b>4:10 p.m.</b> "
                   "The long hand went past the 12, so the hour changed from 3 to 4."))
    n, he, his = P.next()
    its.append(mcq("%s's swim class starts at 5:45 p.m. It lasts 30 minutes. What time does it end?" % n, "6:15 p.m.",
                   ["5:15 p.m.", "6:45 p.m.", "6:15 a.m."],
                   "Count on 15 minutes from 5:45 to 6:00. Then 15 more minutes: <b>6:15 p.m.</b> "
                   "(5:15 p.m. forgets that the hour changed.)"))
    assert len(its) == 20, len(its)
    return {"title": "Times of day: a.m., p.m. and later times", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>The big idea</h2>"
        "<p>A clock has two hands. The <b>short hand</b> tells the hour. The <b>long hand</b> tells the minutes. "
        "Read the short hand first, then the long hand.</p>"
        "<figure class='sn-fig'>" + clock_svg(4, 35, size=230) +
        "<figcaption>The <b>short hand</b> (black) is between 4 and 5, so the hour is 4. "
        "The <b>long hand</b> (red) is on the 7, so it is 35 minutes. The time is 4:35.</figcaption></figure>"
        "<ol class='rk-step'>"
        "<li><b>Hour:</b> look at the short hand. If it is between two numbers, use the number it just <b>passed</b>.</li>"
        "<li><b>Minutes:</b> look at the long hand. Count by 5s from the 12 to the long hand.</li>"
        "<li><b>Write it:</b> hour, a colon, then two digits for the minutes: 4:35, 9:05, 6:00.</li></ol>"
        "<figure class='sn-fig'>" + digital_svg("4:35") +
        "<figcaption>A digital clock shows the same time with only numbers: 4:35.</figcaption></figure>"
        "<h2>Count by 5s around the clock</h2>"
        "<p>Each number on the clock is <b>5 minutes</b> for the long hand. Start at the 12 and count by 5s.</p>"
        "<figure class='sn-fig'>" + clock_svg(8, 40, size=260, ring=True) +
        "<figcaption>The red numbers outside show the minutes. The long hand is on the 8: 5, 10, 15, 20, 25, 30, 35, 40. "
        "The time is 8:40.</figcaption></figure>"
        + table(["Long hand on", "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
                [["Minutes", "0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]]) +
        table(["Words", "Time", "Long hand on"], [
            ["7 o'clock", "7:00", "12"],
            ["quarter past 7", "7:15", "3"],
            ["half past 7", "7:30", "6"],
            ["quarter to 8", "7:45", "9"],
        ])
        + ex("Example", "The short hand is between 9 and 10. The long hand is on the 4. What time is it?",
             "The hour is 9. Count by 5s to the 4: 5, 10, 15, 20.", "9:20")
        + "<h2>a.m. and p.m.</h2>"
        "<p>Each day the clock goes around two times. <b>a.m.</b> is from midnight to noon: the night and the morning. "
        "<b>p.m.</b> is from noon to midnight: the afternoon and the evening.</p>"
        + table(["Time", "What you might do"], [
            ["7:00 a.m.", "eat breakfast"],
            ["10:30 a.m.", "play at recess"],
            ["3:15 p.m.", "go home from school"],
            ["6:00 p.m.", "eat dinner"],
            ["8:30 p.m.", "go to bed"],
        ])
        + ex("Example", "Mia's dance class starts at 3:30 p.m. It lasts 1 hour. When does it end?",
             "In 1 hour the hour goes up by 1. The minutes stay the same. It is still the afternoon.", "4:30 p.m.")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Switching the hands (reading 4:35 as 7:20)", "Short hand = hour. Long hand = minutes"],
            ["Reading the long hand on 4 as 4 minutes (3:04)", "Count by 5s: the 4 means 20 minutes, so it is 3:20"],
            ["Reading 2:50 as 3:50 because the short hand is near the 3", "If the short hand has not reached a number, use the number before it"],
            ["Eating dinner at 6:00 a.m.", "Morning is a.m. Afternoon and evening are p.m."],
        ])
    )


FAQ = [
    {"q": "What should a 2nd grader know about telling time?",
     "a": "By the end of Grade 2, children tell and write time to the nearest five minutes on analog and digital clocks, and use a.m. and p.m. "
          "Telling time to the exact minute and finding elapsed time come in Grade 3."},
    {"q": "How do I teach my child to count by 5s on a clock?",
     "a": "Point to each number on the clock and count 5, 10, 15 … from the 12. The long hand on the 4 means 20 minutes, and on the 9 means 45 minutes."},
    {"q": "Why is the hour hand between two numbers?",
     "a": "The hour hand moves slowly all hour. At 7:35 it has left the 7 but not reached the 8, so the hour is still 7."},
    {"q": "How do you explain a.m. and p.m. to a child?",
     "a": "a.m. is from midnight to noon, like breakfast at 7:00 a.m. p.m. is from noon to midnight, like dinner at 6:00 p.m."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (A-D clock choices) so they stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(206)
    P = People(rnd)
    sets = [set_hour_half(rnd), set_count5(rnd), set_read(rnd), set_match(rnd, P), set_ampm(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            for c in it["c"]:
                for hh, mm in re.findall(r"\b(\d{1,2}):(\d\d)\b", c):
                    assert 1 <= int(hh) <= 12 and int(mm) < 60, c
            for hh, mm in re.findall(r"aria-label='clock showing (\d+):(\d+)'", it["q"]):
                assert hands_gap(int(hh), int(mm)) >= 12, it["q"][-80:]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "us", "subject": "math", "grade": "grade-2", "slug": "telling-time-5-minutes", "sort": 6,
        "updated": UPDATED, "pdf_url": "",
        "title": "Telling Time to the Nearest 5 Minutes",
        "seo_title": "Grade 2 Telling Time Worksheets: Nearest 5 Minutes, Half Hour, Quarter Hour, a.m. and p.m.",
        "short_title": "Telling time (5 minutes)",
        "domain": "Measurement and Data",
        "standard_code": "2.MD.C.7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/2/MD/C/7/",
        "standard_text": "Tell and write time from analog and digital clocks to the nearest five minutes, using a.m. and p.m.",
        "meta_desc": "Free Grade 2 telling time worksheets with clock pictures: o'clock and half past, counting by 5s around the clock, "
                     "reading the clock to the nearest 5 minutes, quarter past and quarter to, and a.m. or p.m. 100 practice questions with answers.",
        "key_big": "Short hand = hour. Long hand = minutes: count by 5s from the 12.",
        "key_sub": "Each number is 5 minutes for the long hand, so the 4 means 20 minutes. If the short hand is between two numbers, "
                   "use the number it just passed. a.m. is the morning; p.m. is the afternoon and evening.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "four clocks labeled A to D")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
