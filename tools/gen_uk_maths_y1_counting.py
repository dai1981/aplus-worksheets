# -*- coding: utf-8 -*-
"""
UK Year 1 Maths: Counting to 100 (National Curriculum in England, Year 1: Number and place value)
  python tools/gen_uk_maths_y1_counting.py
Count objects to 20 in rows of 10 and read and write numbers 1 to 20 in words; one more and one less
(number track); count forwards and backwards across a ten and use a hundred square; more than, less than,
fewer, most and least (pictures and a number line); counting in real life (car park, steps, candles).
Wrong answers come from real mistakes: 12 written 21, thirteen/thirty mixed up, one less than 40 given as 49
or 30, 39 + 1 written 310, counting an object twice or missing one, comparing the ones digit first.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "uk", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#6b6259"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Amelia", "Isla", "Freya", "Poppy", "Ava", "Aisha", "Lily", "Zara", "Grace", "Ruby", "Maya", "Evie"]
BOYS = ["Oliver", "Harry", "Mohammed", "Jack", "Arjun", "Noah", "George", "Leo", "Alfie", "Kai", "Ethan", "Charlie"]
# wrong answers above 100 that show a real mistake (39 + 1 written as 310 …)
BIG_OK = {101, 110, 304, 210, 310, 410, 510, 610, 710, 810, 910, 1000, 909}


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for x in cands:
        if x is None:
            continue
        x = str(x)
        if x in seen or not x or x.startswith("-"):
            continue
        seen.add(x)
        pick.append(x)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def fixed(q, labels, ans, e):
    """Choices are labels for parts of one picture (A, B, C, D). They keep this order."""
    assert ans in labels and len(labels) == 4
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


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        nm, he, his = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=nm, he=he, He=he.capitalize(), his=his)


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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger and stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def lst(xs):
    return ", ".join(str(x) for x in xs)


def rev(n):
    """Digits written backwards (12 -> 21). None when that gives the same number or a lone digit."""
    s = str(n)
    r = s[::-1]
    if len(s) != 2 or r == s or r.startswith("0"):
        return None
    return int(r)


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


# ------------------------------------------------------------ pictures
OS, OGAP, M = 26, 12, 6          # object cell, extra gap after 5 in a row, margin


def obj(kind, cx, cy):
    if kind == "apples":
        return ("<circle cx='%.1f' cy='%.1f' r='9' fill='#e05a4f' stroke='#9b2d24' stroke-width='1.2'/>"
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#6b4423' stroke-width='2' stroke-linecap='round'/>"
                "<ellipse cx='%.1f' cy='%.1f' rx='3.6' ry='2' fill='%s' transform='rotate(-30 %.1f %.1f)'/>"
                % (cx, cy + 2, cx, cy - 6, cx + 1, cy - 10, cx + 4.5, cy - 9, GREEN, cx + 4.5, cy - 9))
    if kind == "stars":
        pts = []
        for k in range(10):
            r = 10.5 if k % 2 == 0 else 4.6
            a = -math.pi / 2 + k * math.pi / 5
            pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + 1 + r * math.sin(a)))
        return "<polygon points='%s' fill='#f4c430' stroke='#a57c00' stroke-width='1.2'/>" % " ".join(pts)
    if kind == "balls":
        return ("<circle cx='%.1f' cy='%.1f' r='9.5' fill='#5b9bd5' stroke='#2e5f8a' stroke-width='1.2'/>"
                "<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f' fill='none' stroke='#ffffff' stroke-width='1.6'/>"
                % (cx, cy, cx - 9, cy, cx, cy - 6, cx + 9, cy))
    if kind == "buttons":
        s = ["<circle cx='%.1f' cy='%.1f' r='9.5' fill='%s' stroke='%s' stroke-width='1.4'/>" % (cx, cy, FILL, GREEN)]
        for dx, dy in [(-2.6, -2.6), (2.6, -2.6), (-2.6, 2.6), (2.6, 2.6)]:
            s.append("<circle cx='%.1f' cy='%.1f' r='1.4' fill='%s'/>" % (cx + dx, cy + dy, GREEN))
        return "".join(s)
    raise ValueError(kind)


def objects_svg(n, kind):
    """n objects in rows of 10. Each row has a small gap after 5, like a ten frame."""
    rows = [10] * (n // 10) + ([n % 10] if n % 10 else [])
    W = 2 * M + 10 * OS + OGAP
    H = 2 * M + len(rows) * OS
    s = []
    for r, k in enumerate(rows):
        for i in range(k):
            s.append(obj(kind, M + OS / 2 + i * OS + (OGAP if i >= 5 else 0), M + OS / 2 + r * OS))
    assert sum(rows) == n
    return svg_wrap(W, H, "".join(s), "%s in rows of 10" % kind)


TC = 24


def tenframes_svg(n):
    """Two ten frames side by side; the first one fills up before the second."""
    assert 0 < n <= 20
    m, gap = 4, 16
    W = 2 * m + 2 * 5 * TC + gap
    H = 2 * m + 2 * TC
    s = []
    for f in range(2):
        x0 = m + f * (5 * TC + gap)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x0, m, 5 * TC, 2 * TC, GREEN))
        for i in range(1, 5):
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                     % (x0 + i * TC, m, x0 + i * TC, m + 2 * TC, GREEN))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2'/>"
                 % (x0, m + TC, x0 + 5 * TC, m + TC, GREEN))
        for k in range(10):
            if f * 10 + k < n:
                s.append("<circle cx='%.1f' cy='%.1f' r='8' fill='%s'/>"
                         % (x0 + (k % 5) * TC + TC / 2, m + (k // 5) * TC + TC / 2, RED))
    return svg_wrap(W, H, "".join(s), "two ten frames with counters")


TW, TH = 44, 36


def track_svg(start, n, target):
    """A number track: n boxes from start. The box at index target shows a red ?."""
    assert 0 <= start and start + n - 1 <= 100
    m = 4
    W, H = 2 * m + n * TW, 2 * m + TH
    s = []
    for k in range(n):
        x = m + k * TW
        isT = k == target
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, m, TW, TH, FILL if isT else "#ffffff", GREEN))
        s.append(text(x + TW / 2, m + 24, "?" if isT else str(start + k), 18 if isT else 16, col=RED if isT else INK))
    return svg_wrap(W, H, "".join(s), "number track")


CWID, CHT = 44, 32


def square_svg(tl, nrows, ncols, target=None, hide=()):
    """A piece of the hundred square. tl = top-left number. target (r, c) shows a red ?, hide = blank boxes."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the square"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 100
    m = 4
    W, H = 2 * m + ncols * CWID, 2 * m + nrows * CHT
    s = []
    for r in range(nrows):
        for c in range(ncols):
            x, y = m + c * CWID, m + r * CHT
            isT = (r, c) == target
            s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, CWID, CHT, FILL if isT else "#ffffff", GREEN))
            if isT:
                s.append(text(x + CWID / 2, y + 22, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CWID / 2, y + 22, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "piece of a hundred square")


def rows_svg(counts, kind):
    """Rows A to D, each with counts[i] objects in a line (a gap after every 5)."""
    labels = "ABCD"
    lw, sp, gp, rh = 30, 22, 10, 30
    mx = max(counts)
    assert mx <= 15
    W = lw + 8 + mx * sp + ((mx - 1) // 5) * gp + 8
    H = 4 + len(counts) * rh + 4
    s = []
    for r, n in enumerate(counts):
        cy = 4 + r * rh + rh / 2
        s.append(text(14, cy + 6, labels[r], 18, col=GREEN))
        for i in range(n):
            cx = lw + 8 + sp / 2 + i * sp + (i // 5) * gp
            if kind == "counters":
                s.append("<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s' stroke='#7a2318' stroke-width='1'/>" % (cx, cy, RED))
            else:
                # objects are 26 wide; draw them a little smaller to fit
                s.append("<g transform='translate(%.1f %.1f) scale(0.8) translate(%.1f %.1f)'>%s</g>"
                         % (cx, cy, -cx, -cy, obj(kind, cx, cy)))
        if r:
            s.append("<line x1='4' y1='%.1f' x2='%d' y2='%.1f' stroke='#dddddd' stroke-width='1'/>"
                     % (4 + r * rh, W - 4, 4 + r * rh))
    return svg_wrap(W, H, "".join(s), "rows A to D of %s" % kind)


NL_SP = 16


def numline_svg(v, top=20):
    """Number line 0 to top, a tick for every 1, numbers at every 5. A red arrow points at v."""
    m = 14
    W = 2 * m + top * NL_SP
    ly = 34
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (m, ly, m + top * NL_SP, ly, INK)]
    for k in range(top + 1):
        x = m + k * NL_SP
        big = k % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (8 if big else 5), x, ly + (8 if big else 5), INK, "2" if big else "1.3"))
        if big:
            s.append(text(x, ly + 26, str(k), 15))
    if v is not None:
        x = m + v * NL_SP
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, x, ly - 12, RED))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x - 6, ly - 16, x + 6, ly - 16, x, ly - 9, RED))
    return svg_wrap(W, H, "".join(s), "number line 0 to %d" % top)


def candles_svg(n):
    """A birthday cake with n candles."""
    sp = 20
    W = max(120, n * sp + 40)
    x0 = (W - (n - 1) * sp) / 2
    s = ["<rect x='10' y='52' width='%d' height='34' rx='5' fill='#f6d7e3' stroke='#b0577a' stroke-width='1.5'/>" % (W - 20),
         "<rect x='4' y='86' width='%d' height='6' rx='3' fill='#cccccc'/>" % (W - 8)]
    for i in range(n):
        x = x0 + i * sp
        s.append("<rect x='%.1f' y='26' width='6' height='26' fill='%s' stroke='#2e5f8a' stroke-width='0.8'/>"
                 % (x - 3, "#5b9bd5" if i % 2 == 0 else "#8fc7a0"))
        s.append("<ellipse cx='%.1f' cy='17' rx='4' ry='7' fill='#f4a300'/>" % x)
    return svg_wrap(W, 96, "".join(s), "birthday cake with candles")


BW, BH = 28, 40


def carpark_svg(filled):
    """Car park: 2 rows of 10 spaces (a wider gap after 5). filled = set of space numbers 0..19 with a car."""
    m, g = 6, 10
    W = 2 * m + 10 * BW + g
    H = 2 * m + 2 * BH + 14
    s = ["<rect x='0' y='0' width='%d' height='%d' fill='#d9d9d9'/>" % (W, H)]
    for k in range(20):
        r, c = divmod(k, 10)
        x = m + c * BW + (g if c >= 5 else 0)
        y = m + r * (BH + 14)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='#ffffff' stroke-width='2'/>"
                 % (x, y, BW, BH))
        if k in filled:
            col = ["#c0392b", "#2e5f8a", "#006633", "#f4a300"][k % 4]
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='5' fill='%s'/>" % (x + 5, y + 5, BW - 10, BH - 10, col))
            s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='2' fill='#e8f2fb'/>" % (x + 8, y + 10, BW - 16, 7))
    return svg_wrap(W, H, "".join(s), "car park with spaces")


def steps_svg(n):
    """Side view of n steps going up."""
    sw, sh, m = 16, 10, 4
    W = 2 * m + n * sw
    H = 2 * m + n * sh
    s = []
    for k in range(n):
        h = (k + 1) * sh
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (m + k * sw, m + n * sh - h, sw, h, FILL, GREEN))
    return svg_wrap(W, H, "".join(s), "steps")


# ------------------------------------------------------------ explanations
def count_e(n, what):
    if n <= 10:
        if n > 5:
            return ("Touch each one once. The first 5, then count on: %s. There are <b>%d</b> %s."
                    % (lst(range(6, n + 1)), n, what))
        return "Touch each one once: %s. There are <b>%d</b> %s." % (lst(range(1, n + 1)), n, what)
    if n == 20:
        return "Each full row has 10. 10, 20. There are <b>20</b> %s." % what
    return ("The top row has 10. Then count on: %s. There are <b>%d</b> %s."
            % (lst(range(11, n + 1)), n, what))


# ============================================================ set 1: count objects and number words
def set_count(rnd, P):
    kinds = ["apples", "stars", "balls", "buttons"]
    its = []
    for i, n in enumerate([4, 7, 9, 10, 12, 13, 15, 16, 18, 20, 17, 14]):
        kind = kinds[i % 4]
        if n < 10:
            cands = [n + 1, n - 1, n + 2]
        elif n == 10:
            cands = [9, 11, 1]
        elif n == 20:
            cands = [19, 21, 2]
        else:
            cands = [rev(n), n + 1, n - 1]
        its.append(mcq(fig(objects_svg(n, kind)) + "How many %s?" % kind, n, cands, count_e(n, kind)))
    # numerals from words
    for w, n, wrong, e in [
        ("twelve", 12, [21, 2, 20], "Twelve is 10 and 2 more. Write <b>12</b>. 21 is twenty-one."),
        ("thirteen", 13, [30, 31, 3], "Thirteen is 10 and 3 more. Write <b>13</b>. Thirty is 30."),
        ("fifteen", 15, [50, 51, 5], "Fifteen is 10 and 5 more. Write <b>15</b>. Fifty is 50."),
        ("seventeen", 17, [70, 71, 7], "Seventeen is 10 and 7 more. Write <b>17</b>. Seventy is 70."),
    ]:
        its.append(mcq("Which number is “%s”?" % w, n, wrong, e))
    # words from ten frames
    for n, wrong, e in [
        (11, ["oneteen", "twelve", "ten"], "The first frame is full: 10. Then 1 more: 11. Say <b>eleven</b>."),
        (14, ["forty", "fourty", "thirteen"], "10 and 4 more is 14. Say <b>fourteen</b>. Forty is 40."),
        (19, ["ninety", "nineten", "eighteen"], "10 and 9 more is 19. Say <b>nineteen</b>. Ninety is 90."),
        (20, ["twelve", "twoty", "nineteen"], "Both frames are full: 10 and 10 is 20. Say <b>twenty</b>. Twelve is 12."),
    ]:
        its.append(mcq(fig(tenframes_svg(n)) + "How many counters? Choose the word.", ONES[n], wrong, e))
    o = its
    order = [o[0], o[1], o[2], o[3], o[12], o[4], o[5], o[13], o[16], o[6],
             o[7], o[14], o[17], o[8], o[11], o[15], o[18], o[10], o[9], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "Count objects and number words", "items": order}


# ============================================================ set 2: one more and one less
def one_more_cands(n):
    a = n + 1
    if a % 10 == 0:
        t = n // 10
        return [int("%d10" % t) if t else None, 10 * t, n - 1, a + 10]
    return [n - 1, n + 10, rev(a), n + 2]


def one_less_cands(n):
    a = n - 1
    if n % 10 == 0:
        return [n + 9, n - 10, n + 1]
    return [n + 1, n - 10 if n > 10 else None, rev(a), n - 2, n]


def set_more_less(rnd, P):
    its = []
    # (n, more?, picture?)
    for n, more, pic in [(6, True, True), (9, False, True), (13, True, True), (18, False, True),
                         (19, True, True), (20, False, True), (34, True, True), (47, False, True),
                         (29, True, True), (40, False, True), (59, True, True), (71, False, True),
                         (66, True, False), (30, False, False), (89, True, False), (52, False, False),
                         (99, True, False), (100, False, False), (80, False, False), (45, True, False)]:
        if more:
            ans = n + 1
            cands = one_more_cands(n)
            if n == 99:
                cands = [910, 90, 98]
            q = "What is one more than %d?" % n
            if ans % 10 == 0:
                e = "Count on 1: %d, <b>%d</b>. After 9 ones comes a new ten." % (n, ans)
                if n == 99:
                    e = "Count on 1: 99, <b>100</b>. Ten tens make one hundred."
            else:
                e = "Count on 1: %d, <b>%d</b>. Only the ones digit changes." % (n, ans)
            fg = fig(track_svg(n - 3, 5, 4)) if pic else ""
        else:
            ans = n - 1
            cands = one_less_cands(n)
            if n == 100:
                cands = [90, 101, 909]
            q = "What is one less than %d?" % n
            if n % 10 == 0:
                e = "Count back 1: %d, <b>%d</b>. Do not jump back a whole ten." % (n, ans)
            else:
                e = "Count back 1: %d, <b>%d</b>. One less is the number just before." % (n, ans)
            fg = fig(track_svg(n - 1, 5, 0)) if pic else ""
        assert ("<b>%d</b>" % ans) in e
        its.append(mcq(fg + q, ans, cands, e))
    return {"title": "One more and one less", "items": its}


# ============================================================ set 3: count across tens, hundred square
def sq_e(tl, tgt, hide, ncols, nrows):
    r, c = tgt
    ans = tl + 10 * r + c
    vis = lambda rr, cc: 0 <= rr < nrows and 0 <= cc < ncols and (rr, cc) not in hide
    if vis(r, c - 1):
        return "Just left of the ? is %d. Count on 1. The ? is <b>%d</b>." % (ans - 1, ans)
    if vis(r, c + 1):
        return "Just right of the ? is %d. Count back 1. The ? is <b>%d</b>." % (ans + 1, ans)
    if vis(r - 1, c):
        return "Just above the ? is %d. One row down is 10 more. The ? is <b>%d</b>." % (ans - 10, ans)
    if vis(r + 1, c):
        return "Just below the ? is %d. One row up is 10 less. The ? is <b>%d</b>." % (ans + 10, ans)
    raise ValueError("no helper box")


def set_across(rnd, P):
    its = {}
    seq = [
        # key, shown, ans, wrong, e
        ("f0", "0, 1, 2, 3, ☐", 4, [5, 3, 2], "Count on 1 from 3. After 3 comes <b>4</b>."),
        ("f29", "27, 28, 29, ☐", 30, [210, 20, 31], "After 29 comes <b>30</b>. 9 ones and 1 more make a new ten. Do not write 210."),
        ("f49", "47, 48, 49, ☐", 50, [410, 40, 59], "After 49 comes <b>50</b>. 4 tens become 5 tens. Do not go back to 40."),
        ("f69", "68, 69, ☐, 71", 70, [610, 60, 72], "After 69 comes <b>70</b>, then 71."),
        ("f99", "97, 98, 99, ☐", 100, [910, 90, 1000], "After 99 comes <b>100</b>. Ten tens make one hundred."),
        ("b41", "42, 41, 40, ☐", 39, [49, 30, 41], "Count back 1 from 40. Before 40 comes <b>39</b>. 49 is wrong: 40 − 1 goes down a ten."),
        ("b5", "5, 4, 3, ☐", 2, [1, 4, 6], "Count back 1 from 3. Before 3 comes <b>2</b>."),
        ("b21", "23, 22, 21, ☐", 20, [19, 12, 22], "Count back 1 from 21. Before 21 comes <b>20</b>."),
        ("b70", "72, 71, 70, ☐", 69, [79, 60, 71], "Count back 1 from 70. Before 70 comes <b>69</b>. Not 79."),
        ("b100", "100, 99, ☐", 98, [97, 90, 101], "Count back 1 from 99. Before 99 comes <b>98</b>."),
        ("b60", "62, ☐, 60, 59", 61, [58, 63, 16], "Counting back: 62, <b>61</b>, 60, 59."),
    ]
    for key, shown, ans, wrong, e in seq:
        verb = "Count back" if key[0] == "b" else "Count on"
        assert ("<b>%d</b>" % ans) in e
        its[key] = mcq("%s: %s. What number goes in the box?" % (verb, shown), ans, wrong, e)
    Q = "This is part of a hundred square. What number goes in the box with the ?"
    pieces = [
        ("s1", 3, 2, 4, (0, 2), set(), [7, 2, 25], None),
        ("s2", 16, 2, 4, (0, 3), set(), [91, 20, 10], None),
        ("s3", 27, 2, 4, (0, 3), set(), [210, 20, 31], "Count on: 27, 28, 29, <b>30</b>. A row of the square ends with a ten."),
        ("s4", 35, 3, 3, (2, 0), set(), [65, 54, 58], None),
        ("s5", 58, 2, 3, (1, 2), set(), [610, 61, 71], None),
        ("s6", 77, 2, 4, (1, 3), set(), [810, 91, 100], "Count on: 87, 88, 89, <b>90</b>. Or look up: 80 and one row down is 90."),
        ("s7", 81, 2, 4, (1, 0), {(1, 1)}, [19, 90, 92], "Just above the ? is 81. One row down is 10 more. The ? is <b>91</b>."),
        ("s8", 87, 2, 4, (1, 3), set(), [910, 1000, 91], "Count on: 97, 98, 99, <b>100</b>. 100 is the last box on the square."),
        ("s9", 44, 3, 3, (1, 1), {(1, 0), (1, 2)}, [54, 56, 35], "Just above the ? is 45. One row down is 10 more. The ? is <b>55</b>."),
    ]
    for key, tl, rows, cols, tgt, hide, wrong, e in pieces:
        ans = tl + 10 * tgt[0] + tgt[1]
        e = e or sq_e(tl, tgt, hide, cols, rows)
        assert ("<b>%d</b>" % ans) in e, (ans, e)
        shown = {tl + 10 * r + c for r in range(rows) for c in range(cols) if (r, c) not in hide and (r, c) != tgt}
        assert not shown & set(wrong), (tl, wrong)
        its[key] = mcq(fig(square_svg(tl, rows, cols, tgt, hide)) + Q, ans, wrong, e)
    k = its
    order = [k["f0"], k["b5"], k["s1"], k["s2"], k["f29"], k["b21"], k["s3"], k["f49"], k["s4"], k["b41"],
             k["f69"], k["s5"], k["b70"], k["s6"], k["b60"], k["s7"], k["s9"], k["f99"], k["b100"], k["s8"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Count forwards and backwards across tens", "items": order}


# ============================================================ set 4: more, less, fewer, most, least
def set_compare(rnd, P):
    L = ["A", "B", "C", "D"]
    its = []

    def rows_q(counts, kind, ask, ans_i, e):
        its.append(fixed(fig(rows_svg(counts, kind)) + ask, L, L[ans_i], e))

    def most(counts, kind):
        i = counts.index(max(counts))
        assert counts.count(max(counts)) == 1
        return i, "Count each row: %s. Row %s has %d. That is the <b>most</b>." % (
            lst("%s has %d" % (L[j], c) for j, c in enumerate(counts)), L[i], counts[i])

    def fewest(counts, kind):
        i = counts.index(min(counts))
        assert counts.count(min(counts)) == 1
        return i, "Count each row: %s. Row %s has %d. That is the <b>fewest</b>." % (
            lst("%s has %d" % (L[j], c) for j, c in enumerate(counts)), L[i], counts[i])

    def equal(counts, n):
        assert counts.count(n) == 1
        i = counts.index(n)
        return i, "Count each row: %s. Row %s has <b>%d</b>. It is equal to %d." % (
            lst("%s has %d" % (L[j], c) for j, c in enumerate(counts)), L[i], n, n)

    c = [4, 6, 3, 8]; i, e = most(c, "counters"); rows_q(c, "counters", "Which row has the most counters?", i, e)
    c = [7, 5, 9, 6]; i, e = fewest(c, "stars"); rows_q(c, "stars", "Which row has the fewest stars?", i, e)
    c = [9, 10, 12, 8]; i, e = most(c, "apples"); rows_q(c, "apples", "Which row has the most apples?", i, e)
    c = [11, 13, 15, 14]; i, e = fewest(c, "counters"); rows_q(c, "counters", "Which row has the fewest counters?", i, e)
    c = [12, 9, 11, 7]; i, e = equal(c, 7); rows_q(c, "balls", "Which row has 7 balls?", i, e)
    c = [8, 10, 6, 9]; i, e = equal(c, 10); rows_q(c, "buttons", "Which row has 10 buttons?", i, e)
    c = [14, 11, 12, 13]; i, e = most(c, "stars"); rows_q(c, "stars", "Which row has the most stars?", i, e)
    c = [14, 15, 12, 13]; i, e = fewest(c, "balls"); rows_q(c, "balls", "Which row has the fewest balls?", i, e)
    assert sorted(it["a"] for it in its) == [0, 0, 1, 1, 2, 2, 3, 3]

    # number line
    for v in [7, 13, 18, 4]:
        near = min([0, 5, 10, 15, 20], key=lambda x: abs(x - v))
        mirror = 2 * near - v
        if mirror < 0 or mirror > 20:
            near = near - 5 if near > v else near + 5
            mirror = 2 * near - v
        e = "Find %d. Count the small marks to the %s: %s. The arrow is at <b>%d</b>." % (
            near, "right" if v > near else "left",
            lst(range(near + 1, v + 1)) if v > near else lst(range(near - 1, v - 1, -1)), v)
        its.append(mcq(fig(numline_svg(v)) + "Which number is the arrow pointing to?", v, [mirror, v + 1, v - 1], e))

    # numbers: more than, less than, most, least, fewer
    its.append(mcq("Which number is more than 36?", 41, [29, 36, 18],
                   "Look at the tens first. 41 has 4 tens. 36 has 3 tens. So <b>41</b> is more. 29 has 9 ones, but only 2 tens."))
    its.append(mcq("Which number is less than 52?", 25, [52, 61, 70],
                   "Look at the tens first. 25 has 2 tens. 52 has 5 tens. So <b>25</b> is less. 52 is equal, not less."))
    its.append(mcq("Which number is the greatest: 38, 83, 47, 74?", 83, [38, 47, 74],
                   "Look at the tens. 83 has 8 tens. That is the most tens. <b>83</b> is the greatest."))
    its.append(mcq("Which number is the least: 45, 54, 40, 50?", 40, [45, 54, 50],
                   "45 and 40 have the fewest tens: 4 tens. 40 has 0 ones. <b>40</b> is the least."))
    its.append(mcq("Which is true?", "14 is less than 41", ["14 is more than 41", "41 is less than 14", "14 is equal to 41"],
                   "14 is 1 ten and 4 ones. 41 is 4 tens and 1 one. So <b>14 is less than 41</b>."))
    d1, d2, d3, d4 = P.next(), P.next(), P.next(), P.next()
    its.append(mcq("%s has 12 sweets. %s has 9. %s has 15. %s has 11. Who has the fewest?" % (
        d1["n"], d2["n"], d3["n"], d4["n"]), d2["n"], [d3["n"], d1["n"], d4["n"]],
        "9 is the smallest number. <b>%s</b> has the fewest sweets." % d2["n"]))
    its.append(mcq("Which number is more than 69 and less than 72?", 70, [69, 72, 73],
                   "Count on from 69: 70, 71, 72. <b>70</b> is more than 69 and less than 72. 72 is not less than 72."))
    its.append(mcq("Which is true?", "60 is more than 59", ["60 is less than 59", "59 is more than 60", "60 is equal to 59"],
                   "Count on: 59, 60. 60 comes after 59. So <b>60 is more than 59</b>."))
    o = its
    # easy to hard: pictures first, then the number line, then 2-digit numbers
    order = [o[0], o[1], o[8], o[4], o[11], o[2], o[9], o[5], o[3], o[10],
             o[6], o[7], o[12], o[13], o[16], o[14], o[15], o[17], o[18], o[19]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20
    return {"title": "More, less, fewer, most and least", "items": order}


# ============================================================ set 5: counting in real life
def set_life(rnd, P):
    its = {}

    def story(key, t, ans, wrong, e, pic=""):
        d = P.next()
        e = e.format(**d)
        assert ("<b>%s</b>" % ans) in e, e
        its[key] = mcq(pic + t.format(**d), ans, wrong, e)

    story("cake", "It is {n}’s birthday. How old is {he}?", 6, [5, 7, 8],
          "Count the candles. Touch each one once: 1, 2, 3, 4, 5, 6. {He} is <b>6</b>.", fig(candles_svg(6)))
    story("cake2", "{n} has a candle for each year. How old is {he}?", 7, [6, 8, 5],
          "Count the candles once each: 1, 2, 3, 4, 5, 6, 7. {He} is <b>7</b>.", fig(candles_svg(7)))
    cars = {0, 1, 3, 4, 6, 7, 8, 11, 12, 15, 16, 18, 19, 13}
    assert len(cars) == 14
    story("car", "How many cars are in the car park?", 14, [13, 15, 41],
          "Count across the top row: 7 cars. Count on along the bottom row: 8, 9, 10, 11, 12, 13, 14. "
          "There are <b>14</b> cars.", fig(carpark_svg(cars)))
    story("space", "How many empty spaces are there?", 6, [14, 5, 7],
          "Count only the empty spaces, not the cars. Top row: 3. Bottom row: 3. 3 and 3 is <b>6</b>.",
          fig(carpark_svg(cars)))
    full = set(range(19))
    story("car20", "One more car parks. How many cars will there be?", 20, [19, 21, 110],
          "There are 19 cars. One more than 19 is <b>20</b>. Now the car park is full.", fig(carpark_svg(full)))
    story("steps", "{n} walks up these steps. How many steps are there?", 12, [11, 13, 21],
          "Count each step once: 1, 2, 3 … 10, 11, 12. There are <b>12</b> steps.", fig(steps_svg(12)))
    story("house", "{n} counts buttons in a jar: 37, 38, 39. What comes next?", 40, [310, 30, 49],
          "After 39 comes <b>40</b>. 9 ones and 1 more make a new ten.")
    story("class", "There are 29 children in Class 1. One more child joins. How many now?", 30, [210, 20, 39],
          "One more than 29 is <b>30</b>. Do not write 210.")
    story("page", "{n} is on page 60. {He} turns back 1 page. What page is {he} on?", 59, [69, 50, 61],
          "One less than 60 is <b>59</b>. Not 69: going back 1 from 60 goes down to 5 tens.")
    story("hide", "{n} counts back for hide and seek: 100, 99, 98, ☐. What comes next?", 97, [96, 99, 89],
          "Count back 1 from 98. Next is <b>97</b>.")
    story("age", "{n} is 6 today. How old will {he} be next birthday?", 7, [5, 8, 6],
          "Next birthday is one more year. One more than 6 is <b>7</b>.")
    story("sticker", "{n} has 74 stickers. {He} gives 1 away. How many are left?", 73, [75, 72, 63],
          "One less than 74 is <b>73</b>. 75 would be one more.")
    story("peg", "{n}’s coat peg is number 19. The next peg is one more. What number is it?", 20, [18, 21, 10],
          "One more than 19 is <b>20</b>. 9 ones and 1 more make 2 tens.")
    story("bus", "The bus has 50 people on it. 1 gets off. How many are on the bus now?", 49, [51, 40, 59],
          "One less than 50 is <b>49</b>. Not 40: that is 10 less.")
    d1, d2, d3, d4 = P.next(), P.next(), P.next(), P.next()
    its["most"] = mcq("At lunchtime %s has 15 grapes. %s has 18. %s has 12. %s has 16. Who has the most?"
                      % (d1["n"], d2["n"], d3["n"], d4["n"]), d2["n"], [d4["n"], d1["n"], d3["n"]],
                      "18 is the biggest number. <b>%s</b> has the most grapes." % d2["n"])
    d1, d2, d3, d4 = P.next(), P.next(), P.next(), P.next()
    its["least"] = mcq("Class 1 has a star chart. %s has 31 stars. %s has 13. %s has 30. %s has 21. "
                       "Who has the least?" % (d1["n"], d2["n"], d3["n"], d4["n"]), d2["n"],
                       [d1["n"], d4["n"], d3["n"]],
                       "13 has only 1 ten. That is the fewest tens. <b>%s</b> has the least." % d2["n"])
    story("count20", "{n} walks down 20 steps. {He} counts back: 20, 19, 18 … What comes after 11?", 10, [12, 9, 11],
          "Counting back, the number after 11 is <b>10</b>.")
    story("pencil", "{n} has 3 packs of 10 pencils and 4 more pencils. How many pencils?", 34, [43, 7, 304],
          "3 packs of 10: 10, 20, 30. Then count on 4: 31, 32, 33, <b>34</b>.")
    story("swim", "{n} swims 17 lengths. Then {he} swims 1 more. How many lengths?", 18, [71, 16, 19],
          "One more than 17 is <b>18</b>.")
    story("tickets", "Raffle tickets go 87, 88, 89 … {n} gets the next one. What number is it?", 90, [810, 80, 91],
          "After 89 comes <b>90</b>. 8 tens become 9 tens.")
    k = its
    order = [k["cake"], k["cake2"], k["age"], k["steps"], k["swim"], k["car"], k["space"], k["car20"], k["peg"],
             k["class"], k["house"], k["sticker"], k["page"], k["bus"], k["count20"], k["hide"], k["most"],
             k["tickets"], k["least"], k["pencil"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Counting in real life", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Counting means saying the numbers in order</h2>"
        "<p>Say one number for each thing. Touch each thing once. The last number you say is how many.</p>"
        "<figure class='sn-fig'>" + objects_svg(13, "apples") +
        "<figcaption>The top row is 10. Then count on: 11, 12, 13. There are 13 apples.</figcaption></figure>"
        "<p>Put things in rows of 10 (5 and 5). Then you do not lose your place.</p>"
        "<h2>Numbers to 20 in words</h2>"
        + table(["Number", "Word", "Number", "Word"], [
            ["11", "eleven", "16", "sixteen"],
            ["12", "twelve", "17", "seventeen"],
            ["13", "thirteen", "18", "eighteen"],
            ["14", "fourteen", "19", "nineteen"],
            ["15", "fifteen", "20", "twenty"],
        ]) +
        "<p>Teen numbers are 10 and some more. Thirteen is 13. Thirty is 30.</p>"
        "<h2>One more and one less</h2>"
        "<p>One more is the next number. One less is the number just before.</p>"
        "<figure class='sn-fig'>" + track_svg(36, 5, 4) +
        "<figcaption>One more than 39 is 40.</figcaption></figure>"
        + ex("One less", "What is one less than 40?",
             "Count back 1: 40, 39. You only go back one step.", "39 (not 49 or 30)") +
        "<h2>The hundred square</h2>"
        "<p>Each row has 10 numbers. Go right for one more. Go down for ten more.</p>"
        "<figure class='sn-fig'>" + square_svg(27, 2, 4) +
        "<figcaption>After 29 comes 30. Below 30 is 40.</figcaption></figure>"
        "<h2>More, less, most and least</h2>"
        "<p>Look at the tens first. 41 has 4 tens. 36 has 3 tens. So 41 is more than 36.</p>"
        "<figure class='sn-fig'>" + numline_svg(13) +
        "<figcaption>The arrow is 3 marks after 10. It points to 13.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing 12 as 21", "Twelve is 10 and 2. The 1 comes first: 12"],
            ["Mixing up thirteen and thirty", "Thirteen is 13. Thirty is 30"],
            ["Writing 310 after 39", "9 ones and 1 more make a new ten: 40"],
            ["One less than 40 is 49 or 30", "Count back just one: 39"],
            ["Counting a thing twice", "Touch each thing once, or put them in rows"],
        ])
    )


FAQ = [
    {"q": "What maths does a Year 1 child learn?",
     "a": "Year 1 children count to 100, read and write numbers to 20 in words, and add and subtract within 20. They also learn halves and quarters, money, time, length and shapes."},
    {"q": "How high should a Year 1 child count?",
     "a": "By the end of Year 1, children should count to 100, forwards and backwards, starting from any number. They should also give one more and one less than a number."},
    {"q": "Why does my child write 21 for twelve?",
     "a": "Twelve sounds like it starts with the 2. Show twelve as 10 and 2 more with counters, then write the 1 for the ten first: 12."},
    {"q": "How can I help my child count to 100 at home?",
     "a": "Count real things like steps, stairs and toys, and point at a hundred square as you say the numbers. Practise the tricky parts, such as 29, 30 and 40, 39."},
]


def gen():
    rnd = random.Random(1101)
    P = People(rnd)
    sets = [set_count(rnd, P), set_more_less(rnd, P), set_across(rnd, P), set_compare(rnd, P), set_life(rnd, P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    v = int(tok)
                    assert 0 <= v <= 100 or v in BIG_OK, c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"]
            seen.add(key)
    u = {
        "country": "uk", "subject": "maths", "grade": "year-1", "slug": "counting-to-100", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Counting to 100: One More, One Less and Numbers in Words",
        "seo_title": "Year 1 Counting to 100 Worksheets: One More and One Less, Number Words to 20",
        "short_title": "Counting to 100",
        "domain": "Number and place value",
        "standard_code": "Year 1: Number and place value",
        "standard_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study",
        "standard_text": "Count to and across 100, forwards and backwards, beginning with 0 or 1, or from any given number; "
                         "count, read and write numbers to 100 in numerals; given a number, identify one more and one less; "
                         "identify and represent numbers using objects and pictorial representations including the number line, "
                         "and use the language of: equal to, more than, less than (fewer), most, least; "
                         "read and write numbers from 1 to 20 in numerals and words.",
        "meta_desc": "Free Year 1 counting to 100 maths worksheets for the National Curriculum: count objects, "
                     "numbers to 20 in words, one more and one less, counting across tens on a hundred square, "
                     "and more, less, most and least. 100 picture questions with an answer key.",
        "key_big": "Touch each thing once and say one number for each. After 9 ones comes a new ten: 29, 30.",
        "key_sub": "One more is the next number. One less is the number just before: one less than 40 is 39. "
                   "Twelve is written 12, not 21.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(\\w+ in rows of 10|rows A to D|number line|car park)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
