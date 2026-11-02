# -*- coding: utf-8 -*-
"""
AU Year 1 Maths: Numbers to 120 (Australian Curriculum v9.0, AC9M1N01)
  python3 tools/gen_au_maths_y1_numbers_120.py
Count objects in rows of 10, ten frames and bundles of 10 icy pole sticks and match the numeral;
numbers before, after and between on a number track; order numbers; number lines and the 120 chart;
compare with more, fewer and bigger in short Australian stories.
Wrong answers come from real mistakes: one hundred and two written 1002, 17 read as 71, counting
98, 99, 100, 110 (skipping 101 to 109), 39 + 1 written 310, comparing the ones digit first,
thinking 99 is bigger than 102 because it has big digits.
Every answer and every picture is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-1")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
STICK = "#e3c08d"
STICK_LINE = "#9a7340"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]
# wrong answers above 120 that show a real mistake (one hundred and two written 1002, 39 + 1 written 310 …)
BIG_OK = {170, 1009, 305, 602, 907, 406, 131, 121, 1002, 1000, 910, 1010, 909, 1001, 1004, 1006, 310, 510, 210, 1003}


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
    assert ("<b>%s</b>" % correct) in e, (correct, e)
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
        return dict(n=nm, he=he, He=he.capitalize(), his=his, His=his.capitalize())


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


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    """Australian English: 102 is “one hundred and two”."""
    assert 1 <= n <= 120
    if n >= 100:
        r = n - 100
        return "one hundred" + (" and " + words(r) if r else "")
    if n >= 20:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    return ONES[n]


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
    if kind == "shells":
        s = ["<path d='M %.1f %.1f Q %.1f %.1f %.1f %.1f Z' fill='#f6c7a8' stroke='#b5651d' stroke-width='1.3'/>"
             % (cx - 10, cy + 6, cx, cy - 16, cx + 10, cy + 6)]
        for dx in (-5, 0, 5):
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='#b5651d' stroke-width='1'/>"
                     % (cx, cy + 6, cx + dx * 1.3, cy - 5 + abs(dx) * 0.6))
        s.append("<rect x='%.1f' y='%.1f' width='6' height='3' fill='#b5651d'/>" % (cx - 3, cy + 6))
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


SW, SH = 3, 62          # one icy pole stick


def bundles_svg(t, o):
    """t bundles of 10 icy pole sticks (with a rubber band) and o single sticks. A wider gap after 5 bundles."""
    m, bg, gg = 6, 10, 22
    BWID = 10 * SW
    s = []
    x = m
    for k in range(t):
        for i in range(10):
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' rx='1.5' fill='%s' stroke='%s' stroke-width='0.7'/>"
                     % (x + i * SW, m, SW, SH, STICK, STICK_LINE))
        s.append("<rect x='%.1f' y='%d' width='%d' height='7' fill='%s'/>" % (x - 1, m + SH / 2 - 3, BWID + 2, RED))
        x += BWID + bg + (8 if k % 5 == 4 else 0)
    xe = (x - bg) if t else m - gg
    x0 = xe + gg
    for k in range(o):
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='1.5' fill='%s' stroke='%s' stroke-width='0.7'/>"
                 % (x0 + k * 9, m, SW + 1, SH, STICK, STICK_LINE))
    right = (x0 + (o - 1) * 9 + SW + 1) if o else xe
    return svg_wrap(int(right + m + 1), 2 * m + SH, "".join(s), "bundles of 10 sticks")


def card_svg(word):
    """A big word card."""
    W = max(140, int(len(word) * 11.5) + 36)
    H = 52
    s = ("<rect x='3' y='3' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>"
         % (W - 6, H - 6, GREEN)) + text(W / 2, 33, word, 20)
    return svg_wrap(W, H, s, "word card")


TW, TH = 46, 36


def track_svg(start, n, target):
    """A number track: n boxes from start. The box at index target shows a red ?."""
    assert 1 <= start and start + n - 1 <= 120
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


CW, CH = 54, 42


def cards_svg(vals):
    """Number cards in a row. A “?” card is shaded with a red ?."""
    m, g = 4, 10
    W = 2 * m + len(vals) * CW + (len(vals) - 1) * g
    H = 2 * m + CH
    s = []
    for k, v in enumerate(vals):
        x = m + k * (CW + g)
        q = str(v) == "?"
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (x, m, CW, CH, FILL if q else "#ffffff", GREEN))
        s.append(text(x + CW / 2, m + 28, str(v), 20, col=RED if q else INK))
    return svg_wrap(W, H, "".join(s), "number cards")


NCW, NCH = 84, 60


def name_cards_svg(pairs):
    """Cards with a name (or team) on top and a number below."""
    m, g = 4, 8
    W = 2 * m + len(pairs) * NCW + (len(pairs) - 1) * g
    H = 2 * m + NCH
    s = []
    for k, (nm, v) in enumerate(pairs):
        x = m + k * (NCW + g)
        s.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, m, NCW, NCH, GREEN))
        s.append("<rect x='%d' y='%d' width='%d' height='22' rx='6' fill='%s'/>" % (x, m, NCW, FILL))
        s.append(text(x + NCW / 2, m + 16, nm, 14, col=GREEN))
        s.append(text(x + NCW / 2, m + 48, str(v), 20))
    return svg_wrap(W, H, "".join(s), "name cards with numbers")


CWID, CHT = 48, 34


def chart_svg(tl, nrows, ncols, target=None, hide=()):
    """A piece of the 120 chart. tl = top-left number. target (r, c) shows a red ?, hide = blank boxes."""
    assert (tl - 1) % 10 + ncols <= 10, "piece must stay inside one row of the chart"
    assert tl + 10 * (nrows - 1) + ncols - 1 <= 120
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
                s.append(text(x + CWID / 2, y + 23, "?", 18, col=RED))
            elif (r, c) not in hide:
                s.append(text(x + CWID / 2, y + 23, str(tl + 10 * r + c), 16))
    return svg_wrap(W, H, "".join(s), "piece of a 120 chart")


def rows_svg(counts, kind, labels="ABCD", lw=30):
    """Rows of objects in a line (a gap after every 5). Each row has a label on the left."""
    sp, gp, rh = 22, 10, 30
    mx = max(counts)
    assert mx <= 20
    W = lw + 8 + mx * sp + ((mx - 1) // 5) * gp + 8
    H = 4 + len(counts) * rh + 4
    s = []
    for r, n in enumerate(counts):
        cy = 4 + r * rh + rh / 2
        s.append(text(lw / 2 if lw <= 30 else 4, cy + 6, labels[r], 18 if lw <= 30 else 15,
                      anchor="middle" if lw <= 30 else "start", col=GREEN))
        for i in range(n):
            cx = lw + 8 + sp / 2 + i * sp + (i // 5) * gp
            s.append("<g transform='translate(%.1f %.1f) scale(0.8) translate(%.1f %.1f)'>%s</g>"
                     % (cx, cy, -cx, -cy, obj(kind, cx, cy)))
        if r:
            s.append("<line x1='4' y1='%.1f' x2='%d' y2='%.1f' stroke='#dddddd' stroke-width='1'/>"
                     % (4 + r * rh, W - 4, 4 + r * rh))
    return svg_wrap(W, H, "".join(s), "rows of %s" % kind)


NL_SP = 16


def numline_svg(lo, v, span=20):
    """Number line lo to lo+span, a tick for every 1, numbers at every 5. A red arrow points at v."""
    m = 18
    W = 2 * m + span * NL_SP
    ly = 34
    H = ly + 30
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (m, ly, m + span * NL_SP, ly, INK)]
    for k in range(span + 1):
        x = m + k * NL_SP
        big = (lo + k) % 5 == 0
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='%s'/>"
                 % (x, ly - (8 if big else 5), x, ly + (8 if big else 5), INK, "2" if big else "1.3"))
        if big:
            s.append(text(x, ly + 26, str(lo + k), 15))
    if v is not None:
        x = m + (v - lo) * NL_SP
        s.append("<line x1='%d' y1='4' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x, x, ly - 12, RED))
        s.append("<polygon points='%d,%d %d,%d %d,%d' fill='%s'/>" % (x - 6, ly - 16, x + 6, ly - 16, x, ly - 9, RED))
    return svg_wrap(W, H, "".join(s), "number line %d to %d" % (lo, lo + span))


def ones_line_svg(start, n, labels):
    """Number line with n ticks, 1 apart. labels: {index: text}."""
    m, sp, ly = 34, 46, 14
    W = 2 * m + (n - 1) * sp
    H = ly + 34
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (6, ly, W - 6, ly, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (14, ly - 6, 6, ly, 14, ly + 6, INK),
         "<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5'/>"
         % (W - 14, ly - 6, W - 6, ly, W - 14, ly + 6, INK)]
    for k in range(n):
        x = m + k * sp
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 7, x, ly + 7, INK))
        if k in labels:
            t = labels[k]
            s.append(text(x, ly + 27, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "number line counting by ones from %d" % start)


# ------------------------------------------------------------ explanations
def count_e(n, what):
    t, o = divmod(n, 10)
    if n <= 10:
        if n > 5:
            return ("The first 5 make a group of 5. Count on: %s. There are <b>%d</b> %s."
                    % (lst(range(6, n + 1)), n, what))
        return "Touch each one once: %s. There are <b>%d</b> %s." % (lst(range(1, n + 1)), n, what)
    tens = lst(range(10, 10 * t + 1, 10))
    if o == 0:
        return "Each full row has 10. Count the rows by tens: %s. There are <b>%d</b> %s." % (tens, n, what)
    return ("Each full row has 10. Count the rows by tens: %s. Then count on by ones: %s. There are <b>%d</b> %s."
            % (tens, lst(range(10 * t + 1, n + 1)), n, what))


def bundle_e(n):
    t, o = divmod(n, 10)
    e = "Each bundle has 10 sticks. Count the bundles by tens: %s." % lst(range(10, 10 * t + 1, 10))
    if o:
        e += " Then count on the single sticks: %s." % lst(range(10 * t + 1, n + 1))
    return e + " There are <b>%d</b> sticks." % n


# ============================================================ set 1: count objects and match numerals
def set_count(rnd, P):
    its = {}
    for key, n, kind, wrong in [
        ("o8", 8, "apples", [7, 9, 6]),
        ("o12", 12, "stars", [21, 11, 13]),
        ("o17", 17, "balls", [71, 16, 18]),
        ("o20", 20, "buttons", [2, 19, 21]),
        ("o23", 23, "shells", [32, 22, 24]),
        ("o26", 26, "stars", [62, 25, 27]),
    ]:
        its[key] = mcq(fig(objects_svg(n, kind)) + "How many %s?" % kind, n, wrong, count_e(n, kind))
    for key, n, wrong in [("t14", 14, [41, 13, 15]), ("t19", 19, [91, 18, 20])]:
        e = "The first ten frame is full. That is 10. Then count on: %s. There are <b>%d</b> counters." % (
            lst(range(11, n + 1)), n)
        its[key] = mcq(fig(tenframes_svg(n)) + "How many counters?", n, wrong, e)
    for key, n, wrong in [
        ("b35", 35, [53, 8, 305]),
        ("b40", 40, [4, 30, 50]),
        ("b62", 62, [26, 8, 602]),
        ("b97", 97, [79, 16, 907]),
        ("b100", 100, [10, 1000, 90]),
        ("b102", 102, [1002, 12, 120]),
        ("b113", 113, [14, 131, 103]),
    ]:
        e = bundle_e(n)
        if n == 102:
            e += " Write 102, not 1002."
        if n == 113:
            e = ("Each bundle has 10 sticks. 10 bundles make 100. Then 1 more bundle: 110. "
                 "Then count on: 111, 112, 113. There are <b>113</b> sticks.")
        its[key] = mcq(fig(bundles_svg(n // 10, n % 10)) + "How many sticks?", n, wrong, e)
    for key, n, wrong, e in [
        ("w17", 17, [71, 70, 7], "Seventeen is 10 and 7 more. Write <b>17</b>. 71 is seventy-one."),
        ("w46", 46, [64, 406, 40], "Forty-six is 4 tens and 6 ones. Write <b>46</b>, not 406."),
        ("w102", 102, [1002, 120, 12], "One hundred and two is 100 and 2 more. Write <b>102</b>. "
                                       "The 0 shows there are no tens. Do not write 1002."),
        ("w117", 117, [170, 107, 71], "One hundred and seventeen is 100 and 17 more. Write <b>117</b>. "
                                      "107 is one hundred and seven."),
    ]:
        assert words(n) in ("seventeen", "forty-six", "one hundred and two", "one hundred and seventeen")
        its[key] = mcq(fig(card_svg(words(n))) + "Which number is this?", n, wrong, e)
    w = words(115)
    its["say115"] = mcq(fig(card_svg("115")) + "How do you say this number?", w,
                        ["one hundred and fifty", "fifteen", "one hundred and five"],
                        "115 is 100 and 15 more. Say <b>%s</b>. One hundred and fifty is 150." % w)
    k = its
    order = [k["o8"], k["o12"], k["t14"], k["o17"], k["w17"], k["t19"], k["o20"], k["o23"], k["o26"], k["b35"],
             k["b40"], k["w46"], k["b62"], k["b97"], k["b100"], k["b102"], k["w102"], k["b113"], k["w117"], k["say115"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Count objects and match numerals", "items": order}


# ============================================================ set 2: before, after and between
def set_before_after(rnd, P):
    its = {}
    for n, wrong, e in [
        (9, [8, 11, 12], "Count on 1 from 9: 9, <b>10</b>. 8 comes before 9."),
        (14, [13, 51, 16], "Count on 1 from 14: 14, <b>15</b>. 13 comes before 14."),
        (29, [210, 20, 31], "After 29 comes <b>30</b>. 9 ones and 1 more make a new ten. Do not write 210."),
        (39, [310, 30, 41], "After 39 comes <b>40</b>. 3 tens become 4 tens. Do not write 310."),
        (59, [510, 50, 61], "After 59 comes <b>60</b>. Do not go back to 50."),
        (68, [67, 96, 70], "Count on 1 from 68: 68, <b>69</b>. Only the ones digit changes."),
        (99, [910, 1000, 90], "After 99 comes <b>100</b>. 10 tens make one hundred. Do not write 910."),
        (109, [1010, 100, 111], "After 109 comes <b>110</b>. 100 and 1 more ten. Do not write 1010."),
        (114, [113, 105, 116], "Count on 1 from 114: 114, <b>115</b>. Only the ones digit changes."),
    ]:
        ans = n + 1
        its["a%d" % n] = mcq(fig(track_svg(n - 3, 5, 4)) + "What number comes after %d?" % n, ans, wrong, e)
    for n, wrong, e in [
        (12, [13, 10, 14], "Count back 1 from 12: 12, <b>11</b>. 13 comes after 12."),
        (20, [21, 10, 29], "Count back 1 from 20: 20, <b>19</b>. Not 29: going back 1 from 20 goes down a ten."),
        (50, [51, 40, 59], "Count back 1 from 50: 50, <b>49</b>. 40 is 10 less, not 1 less."),
        (81, [82, 70, 18], "Count back 1 from 81: 81, <b>80</b>. 82 comes after 81."),
        (100, [101, 90, 909], "Count back 1 from 100: 100, <b>99</b>. Write ninety-nine as 99, not 909."),
        (110, [111, 100, 1009], "Count back 1 from 110: 110, <b>109</b>. Write 109, not 1009."),
        (120, [121, 110, 118], "Count back 1 from 120: 120, <b>119</b>. 110 is 10 less, not 1 less."),
    ]:
        n_box = min(4, 121 - n)
        its["b%d" % n] = mcq(fig(track_svg(n - 1, n_box + 1, 0)) + "What number comes just before %d?" % n,
                             n - 1, wrong, e)
    BIG_OK.add(1009)
    for a, b, wrong, e in [
        (16, 18, [71, 15, 19], "Count on: 16, <b>17</b>, 18. Do not read 17 as 71."),
        (44, 46, [54, 43, 47], "Count on: 44, <b>45</b>, 46."),
        (99, 101, [1000, 910, 110], "Count on: 99, <b>100</b>, 101. 10 tens make 100."),
        (101, 103, [1002, 120, 104], "Count on: 101, <b>102</b>, 103. Write 102, not 1002."),
    ]:
        its["m%d" % a] = mcq(fig(track_svg(a - 1, 5, 2)) + "What number comes between %d and %d?" % (a, b),
                             a + 1, wrong, e)
    k = its
    order = [k["a9"], k["b12"], k["m16"], k["a14"], k["b20"], k["a29"], k["m44"], k["a39"], k["b50"], k["a59"],
             k["a68"], k["b81"], k["a99"], k["b100"], k["m99"], k["a109"], k["b110"], k["m101"], k["a114"], k["b120"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Before, after and between", "items": order}


# ============================================================ set 3: order numbers
def set_order(rnd, P):
    its = {}

    def small(key, cards, e):
        ans = min(cards)
        its[key] = mcq(fig(cards_svg(cards)) + "Which number is the smallest?", ans,
                       [c for c in cards if c != ans], e)

    def big(key, cards, e):
        ans = max(cards)
        its[key] = mcq(fig(cards_svg(cards)) + "Which number is the biggest?", ans,
                       [c for c in cards if c != ans], e)

    def order(key, cards, up, wrong, e):
        ans = lst(sorted(cards, reverse=not up))
        for w in wrong:
            assert sorted(int(x) for x in w.split(", ")) != sorted(cards) or w != ans
        q = "Put the cards in order from %s." % ("smallest to biggest" if up else "biggest to smallest")
        its[key] = mcq(fig(cards_svg(cards)) + q, ans, wrong, e)

    small("s1", [3, 8, 5, 1], "Count from 1: 1, 2, 3 … 1 comes first. <b>1</b> is the smallest.")
    big("g12", [7, 12, 9, 4], "12 is 1 ten and 2 ones. The other numbers are less than 10. <b>12</b> is the biggest.")
    order("o3", [6, 2, 9], True, ["9, 6, 2", "6, 2, 9", "2, 9, 6"],
          "Count from 1. You say 2 first, then 6, then 9. The order is <b>2, 6, 9</b>.")
    small("s11", [14, 41, 19, 11], "41 has 4 tens, so it is big. 14, 19 and 11 have 1 ten. "
                                   "Look at the ones: 11 has 1 one. <b>11</b> is the smallest.")
    big("g71", [17, 71, 27, 70], "Look at the tens first. 71 and 70 have 7 tens. 71 has 1 more one. "
                                 "<b>71</b> is the biggest. 17 is only 1 ten and 7 ones.")
    order("o71", [31, 13, 71, 17], True, ["13, 31, 17, 71", "71, 31, 17, 13", "17, 13, 71, 31"],
          "Look at the tens first. 13 and 17 have 1 ten. 31 has 3 tens. 71 has 7 tens. "
          "The order is <b>13, 17, 31, 71</b>.")
    its["sec"] = mcq(fig(cards_svg([64, 46, 60, 49])) +
                     "Put the cards in order from smallest to biggest. Which number is second?", 49, [46, 60, 64],
                     "46 and 49 have 4 tens. 60 and 64 have 6 tens. The order is 46, 49, 60, 64. "
                     "The second number is <b>49</b>.")
    order("o58", [55, 49, 58, 50], False, ["49, 50, 55, 58", "58, 50, 55, 49", "55, 58, 50, 49"],
          "Biggest first. 58 is the biggest, then 55, then 50. 49 has only 4 tens. "
          "The order is <b>58, 55, 50, 49</b>.")
    its["btw54"] = mcq(fig(cards_svg([45, "?", 61])) + "Which number fits between 45 and 61?", 54, [64, 41, 16],
                       "The number must be bigger than 45 and smaller than 61. 54 is 5 tens and 4 ones. "
                       "<b>54</b> fits. 64 is too big. 41 and 16 are too small.")
    big("g102", [99, 102, 98, 100], "99 has big digits, but it is only 2 digits. 102 has 3 digits: 1 hundred. "
                                    "102 comes after 100. <b>102</b> is the biggest.")
    small("s100", [110, 101, 100, 111], "All of these are 1 hundred and more. 100 comes first: 100, 101 … 110, 111. "
                                        "<b>100</b> is the smallest.")
    order("o99", [100, 99, 110], True, ["100, 99, 110", "110, 100, 99", "99, 110, 100"],
          "99 has only 2 digits, so it is the smallest. 100 comes next, then 110. The order is <b>99, 100, 110</b>.")
    its["list1"] = mcq("Which list counts on by ones?", "98, 99, 100, 101",
                       ["98, 99, 100, 110", "98, 99, 910, 911", "98, 99, 1000, 1001"],
                       "After 99 comes 100. After 100 comes 101, not 110. The list is <b>98, 99, 100, 101</b>.")
    BIG_OK.update({911})
    its["list2"] = mcq("Which list counts on by ones?", "100, 101, 102, 103",
                       ["100, 110, 111, 112", "100, 101, 1002, 1003", "100, 110, 120, 130"],
                       "After 100 comes 101, then 102 and 103. Do not jump to 110. "
                       "The list is <b>100, 101, 102, 103</b>.")
    BIG_OK.update({130})
    its["btw102"] = mcq(fig(cards_svg([98, "?", 105])) + "Which number fits between 98 and 105?", 102,
                        [1002, 97, 110],
                        "Count on from 98: 99, 100, 101, 102, 103, 104, 105. <b>102</b> fits. Write 102, not 1002.")
    small("s51", [105, 115, 51, 110], "51 has only 2 digits. It is less than 100. The other numbers are more than 100. "
                                      "<b>51</b> is the smallest.")
    big("g120", [112, 108, 120, 118], "All these numbers are 1 hundred and more. Look at the tens: 120 has 2 tens. "
                                      "<b>120</b> is the biggest. 118 has big ones, but only 1 ten.")
    order("o117", [17, 107, 71, 117], False, ["17, 71, 107, 117", "107, 117, 71, 17", "117, 107, 17, 71"],
          "Numbers with 3 digits are bigger. 117 is more than 107. Then 71, then 17. "
          "The order is <b>117, 107, 71, 17</b>.")
    order("o101", [101, 11, 110], True, ["101, 11, 110", "11, 110, 101", "110, 101, 11"],
          "11 has only 2 digits, so it is the smallest. 101 comes before 110. The order is <b>11, 101, 110</b>.")
    its["btw106"] = mcq(fig(cards_svg([100, "?", 110])) + "Which number fits between 100 and 110?", 106,
                        [1006, 96, 116],
                        "Count on from 100: 101, 102 … 109, 110. <b>106</b> fits. 96 is less than 100. "
                        "116 is more than 110.")
    k = its
    order_ = [k["s1"], k["g12"], k["o3"], k["s11"], k["g71"], k["o71"], k["sec"], k["o58"], k["btw54"], k["g102"],
              k["s100"], k["o99"], k["list1"], k["list2"], k["btw102"], k["s51"], k["g120"], k["o117"], k["o101"],
              k["btw106"]]
    assert len(order_) == 20 and len({id(x) for x in order_}) == 20 and len(its) == 20
    return {"title": "Order numbers", "items": order_}


# ============================================================ set 4: number lines and the 120 chart
def chart_e(tl, tgt, hide, ncols, nrows):
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


def set_lines(rnd, P):
    its = {}
    # arrows on a number line
    for key, lo, v, extra in [("a13", 0, 13, None), ("a27", 20, 27, None), ("a48", 40, 48, None),
                              ("a96", 80, 96, None), ("a104", 100, 104, 1004), ("a112", 100, 112, None)]:
        near = min(range(lo, lo + 21, 5), key=lambda x: (abs(x - v), x))
        mirror = 2 * near - v
        assert lo <= mirror <= lo + 20 and mirror != v
        if v > near:
            e = "Find %d. Count the small marks to the right: %s. The arrow is at <b>%d</b>." % (
                near, lst(range(near + 1, v + 1)), v)
        else:
            e = "Find %d. Count the small marks to the left: %s. The arrow is at <b>%d</b>." % (
                near, lst(range(near - 1, v - 1, -1)), v)
        wrong = [mirror, v + 1, v - 1]
        if extra:
            wrong = [mirror, extra, v - 1]
            e += " Write %d, not %d." % (v, extra)
        its[key] = mcq(fig(numline_svg(lo, v)) + "What number is the arrow pointing to?", v, wrong, e)
    # number lines with a ?
    for key, start, n, labels, wrong, e in [
        ("l43", 43, 6, {0: "43", 3: "?"}, [45, 47, 64], "Count on from 43: 44, 45, <b>46</b>. Do not count the first tick."),
        ("l95", 95, 7, {0: "95", 5: "100", 6: "?"}, [110, 1001, 102],
         "After 100 comes <b>101</b>. Count on by ones. Do not jump to 110."),
        ("l106", 106, 6, {0: "106", 4: "?"}, [1010, 111, 109],
         "Count on from 106: 107, 108, 109, <b>110</b>. Do not write 1010."),
    ]:
        nums = {k: start + k for k in range(n)}
        assert all(v == "?" or int(v) == nums[k] for k, v in labels.items())
        ans = nums[[k for k, v in labels.items() if v == "?"][0]]
        its[key] = mcq(fig(ones_line_svg(start, n, labels)) + "Each mark is 1 more. What number goes at the ?",
                       ans, wrong, e)
    # 120 chart pieces
    Q = "This is part of a 120 chart. What number goes in the box with the ?"
    pieces = [
        ("c34", 23, 2, 4, (1, 1), set(), [43, 44, 32], None),
        ("c56", 36, 3, 3, (2, 0), set(), [65, 55, 66], None),
        ("c60", 57, 2, 4, (0, 3), set(), [510, 50, 61],
         "The row goes 57, 58, 59. After 59 comes <b>60</b>. A row of the chart ends with a ten."),
        ("c100", 97, 2, 4, (0, 3), set(), [910, 1000, 90], "The row goes 97, 98, 99. After 99 comes <b>100</b>."),
        ("c101", 91, 2, 3, (1, 0), set(), [110, 1001, 100],
         "Just above the ? is 91. One row down is 10 more. The ? is <b>101</b>. The row after 100 starts with 101, not 110."),
        ("c110", 97, 3, 4, (1, 3), set(), [1010, 101, 111],
         "The row goes 107, 108, 109. After 109 comes <b>110</b>. You can also look up: 100 and 10 more is 110."),
        ("c102", 101, 2, 4, (0, 1), set(), [1002, 120, 92],
         "Just left of the ? is 101. Count on 1. The ? is <b>102</b>. Write 102, not 1002."),
        ("c106", 106, 2, 5, (0, 0), set(), [1006, 105, 160], None),
        ("c118", 114, 1, 7, (0, 4), {(0, 3), (0, 5)}, [117, 119, 108],
         "Count on from 116: 117, <b>118</b>. The blank box is 117."),
    ]
    BIG_OK.update({160})
    for key, tl, rows, cols, tgt, hide, wrong, e in pieces:
        ans = tl + 10 * tgt[0] + tgt[1]
        e = e or chart_e(tl, tgt, hide, cols, rows)
        assert ("<b>%d</b>" % ans) in e, (ans, e)
        shown = {tl + 10 * r + c for r in range(rows) for c in range(cols) if (r, c) not in hide and (r, c) != tgt}
        assert not shown & set(wrong), (tl, wrong)
        its[key] = mcq(fig(chart_svg(tl, rows, cols, tgt, hide)) + Q, ans, wrong, e)
    its["t67"] = mcq(fig(chart_svg(56, 2, 3, (1, 1))) + "On a 120 chart, which number is just below 57?", 67,
                     [58, 47, 76], "One row down on the chart is 10 more. 57 and 10 more is <b>67</b>. "
                                   "58 is just to the right.")
    its["t97"] = mcq(fig(chart_svg(96, 2, 3, (0, 1))) + "On a 120 chart, which number is just above 107?", 97,
                     [106, 117, 108], "One row up on the chart is 10 less. 107 and 10 less is <b>97</b>.")
    k = its
    order = [k["a13"], k["c34"], k["a27"], k["l43"], k["c56"], k["c60"], k["a48"], k["t67"], k["a96"], k["c100"],
             k["l95"], k["c101"], k["c110"], k["l106"], k["a104"], k["c102"], k["t97"], k["c106"], k["a112"], k["c118"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "Number lines and the 120 chart", "items": order}


# ============================================================ set 5: more, fewer and number stories
def set_stories(rnd, P):
    L = ["A", "B", "C", "D"]
    its = {}

    def rows_q(key, counts, kind, ask, which):
        if which == "most":
            i = counts.index(max(counts)); assert counts.count(max(counts)) == 1
        elif which == "fewest":
            i = counts.index(min(counts)); assert counts.count(min(counts)) == 1
        else:
            ok = [j for j, c in enumerate(counts) if c > which]; assert len(ok) == 1
            i = ok[0]
        e = "Count each row: %s. Row %s has %d. " % (lst("%s has %d" % (L[j], c) for j, c in enumerate(counts)),
                                                     L[i], counts[i])
        e += ("That is the <b>most</b>." if which == "most" else "That is the <b>fewest</b>." if which == "fewest"
              else "That is the only row with <b>more than %d</b>." % which)
        e = e.replace("<b>", "").replace("</b>", "")
        e = e.replace("Row %s has" % L[i], "Row <b>%s</b> has" % L[i])
        its[key] = fixed(fig(rows_svg(counts, kind)) + ask, L, L[i], e)

    rows_q("r1", [6, 9, 7, 4], "shells", "Shells from the beach. Which row has the most shells?", "most")
    rows_q("r2", [8, 7, 10, 5], "apples", "Apples for recess. Which row has the fewest apples?", "fewest")
    rows_q("r3", [12, 9, 10, 8], "balls", "Which row has more than 10 balls?", 10)
    rows_q("r4", [14, 11, 15, 13], "stars", "Which row has the most stars?", "most")
    assert sorted(its[k]["a"] for k in ("r1", "r2", "r3", "r4")) == [0, 1, 2, 3]

    d1, d2 = P.next(), P.next()
    its["p1"] = mcq(fig(rows_svg([17, 12], "stars", [d1["n"], d2["n"]], lw=86)) +
                    "%s has 17 stickers. %s has 12. How many more does %s have?" % (d1["n"], d2["n"], d1["n"]),
                    5, [29, 4, 6],
                    "Count on from 12 to 17: 13, 14, 15, 16, 17. That is 5 jumps. %s has <b>5</b> more. "
                    "Do not add: 17 and 12 is 29." % d1["n"])
    d1, d2 = P.next(), P.next()
    its["p2"] = mcq(fig(rows_svg([9, 15], "shells", [d1["n"], d2["n"]], lw=86)) +
                    "%s has 9 shells. %s has 15. How many fewer does %s have?" % (d1["n"], d2["n"], d1["n"]),
                    6, [24, 5, 7],
                    "Count on from 9 to 15: 10, 11, 12, 13, 14, 15. That is 6 jumps. %s has <b>6</b> fewer." % d1["n"])

    def names_q(key, ask, vals, which, e_tail, prefix=""):
        ds = [P.next()["n"] for _ in vals]
        pairs = list(zip(ds, vals))
        f = max if which == "most" else min
        best = f(vals)
        assert vals.count(best) == 1
        nm = ds[vals.index(best)]
        e = "%s The biggest number is %d. " if which == "most" else "%s The smallest number is %d. "
        e = (e % (e_tail, best)).strip() + " <b>%s</b> has the %s." % (nm, which)
        its[key] = mcq(fig(name_cards_svg(pairs)) + prefix + ask, nm, [d for d in ds if d != nm], e)

    names_q("n1", "Who found the most shells?", [24, 42, 19, 40], "most",
            "Look at the tens first. 42 has 4 tens and 2 ones. 40 has 4 tens and 0 ones.",
            "These cards show how many shells each child found at the beach. ")
    names_q("n2", "Who has the fewest stickers?", [31, 13, 30, 21], "fewest",
            "Look at the tens first. 13 has only 1 ten. Do not read 13 as 31.",
            "These cards show stickers. ")
    names_q("n3", "Who read the most pages?", [102, 99, 100, 90], "most",
            "99 has big digits, but it has only 2 digits. 102 is 1 hundred and 2 more. 102 comes after 100.",
            "These cards show pages read this term. ")
    teams = [("Red", 71), ("Blue", 17), ("Green", 70), ("Yellow", 107)]
    its["n4"] = mcq(fig(name_cards_svg(teams)) +
                    "The school houses got points at the athletics carnival. Which house has the most points?",
                    "Yellow", ["Red", "Green", "Blue"],
                    "107 has 3 digits: 1 hundred and 7 more. It is the biggest. <b>Yellow</b> has the most. "
                    "71 is less than 100.")
    classes = [("1A", 58), ("1B", 85), ("1C", 50), ("1D", 80)]
    its["n5"] = mcq(fig(name_cards_svg(classes)) +
                    "Each Year 1 class counted the books it read. Which class read the fewest books?",
                    "1C", ["1A", "1D", "1B"],
                    "50 and 58 have the fewest tens: 5 tens. 50 has 0 ones. 50 is the smallest. <b>1C</b> read the fewest.")
    its["t1"] = mcq(fig(cards_svg([14, 41])) + "Which is true?", "41 is more than 14",
                    ["14 is more than 41", "41 is less than 14", "14 is equal to 41"],
                    "14 is 1 ten and 4 ones. 41 is 4 tens and 1 one. So <b>41 is more than 14</b>.")
    its["t2"] = mcq(fig(cards_svg([102, 99])) + "Which is true?", "102 is more than 99",
                    ["99 is more than 102", "102 is less than 99", "99 is equal to 102"],
                    "99 comes just before 100. 102 comes after 100. So <b>102 is more than 99</b>.")
    its["chairs"] = mcq("The class has 26 students. There are 30 chairs. How many more chairs than students?",
                        4, [56, 3, 5],
                        "Count on from 26 to 30: 27, 28, 29, 30. That is 4 jumps. There are <b>4</b> more chairs. "
                        "Do not add: 26 and 30 is 56.")
    d = P.next()
    its["cards"] = mcq(fig(track_svg(57, 4, 3)) +
                       "%s has 59 footy cards. %s friend has 1 more. How many cards does the friend have?"
                       % (d["n"], d["His"]), 60, [510, 50, 61],
                       "1 more than 59 is <b>60</b>. 9 ones and 1 more make a new ten. Do not write 510.")
    its["sizzle"] = mcq("There are 100 people at the sausage sizzle. 10 more come. How many people are there now?",
                        110, [1010, 101, 200],
                        "10 more than 100 is <b>110</b>. 100 is 10 tens. 1 more ten makes 110. 101 is only 1 more.")
    BIG_OK.update({200})
    its["canteen"] = mcq(fig(track_svg(106, 3, 1)) +
                         "The school canteen has 108 icy poles. It sells 1. How many are left?",
                         107, [109, 98, 1007],
                         "1 less than 108 is <b>107</b>. 109 is 1 more. Write 107, not 1007.")
    BIG_OK.update({1007})
    d = P.next()
    its["count"] = mcq(fig(track_svg(98, 4, 3)) +
                       "%s counts shells on the beach: 98, 99, 100. %s friend says the next number is 110. "
                       "What is the right number?" % (d["n"], d["His"]),
                       101, [110, 1001, 200],
                       "After 100 comes <b>101</b>. Count on by ones: 100, 101, 102 … 110 comes later.")
    d = P.next()
    its["sticks"] = mcq(fig(bundles_svg(3, 6)) +
                        "%s has 3 bundles of 10 icy pole sticks and 6 more sticks. How many sticks?" % d["n"],
                        36, [63, 9, 306],
                        "Count the bundles by tens: 10, 20, 30. Then count on: 31, 32, 33, 34, 35, 36. "
                        "There are <b>36</b> sticks.")
    BIG_OK.update({306})
    its["day100"] = mcq(fig(track_svg(99, 3, 0)) +
                        "The class counts the days of school. Today is day 100. What day was yesterday?",
                        99, [101, 90, 909],
                        "Yesterday is 1 day before. 1 less than 100 is <b>99</b>. 101 is tomorrow.")
    k = its
    order = [k["r1"], k["r2"], k["t1"], k["r3"], k["p1"], k["r4"], k["p2"], k["sticks"], k["n2"], k["n1"],
             k["chairs"], k["cards"], k["n5"], k["t2"], k["day100"], k["n3"], k["sizzle"], k["count"], k["canteen"],
             k["n4"]]
    assert len(order) == 20 and len({id(x) for x in order}) == 20 and len(its) == 20
    return {"title": "More, fewer and number stories", "items": order}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Numbers to 120 follow a pattern</h2>"
        "<p>Count on by ones. Only the ones digit changes until you get to 9. "
        "Then 1 more makes a <b>new ten</b>. After 99 comes 100. Then the pattern starts again: 101, 102, 103 …</p>"
        + table(["Count on", "What happens"], [
            ["37, 38, 39, <b>40</b>", "9 ones and 1 more make a new ten"],
            ["97, 98, 99, <b>100</b>", "10 tens make one hundred"],
            ["100, <b>101</b>, 102", "After 100 comes 101, not 110"],
            ["107, 108, 109, <b>110</b>", "100 and 1 more ten"],
        ]) +
        "<h2>Count in tens, then ones</h2>"
        "<p>Put things in rows or bundles of 10. Count the tens first. Then count on the ones.</p>"
        "<figure class='sn-fig'>" + objects_svg(23, "shells") +
        "<figcaption>Count by tens: 10, 20. Then count on: 21, 22, 23. There are 23 shells.</figcaption></figure>"
        "<figure class='sn-fig'>" + bundles_svg(10, 2) +
        "<figcaption>10 bundles of 10 sticks make 100. With 2 more sticks, that is 102.</figcaption></figure>"
        + ex("Write the number", "How do you write “one hundred and two”?",
             "It is 100 and 2 more. There are no tens, so the tens digit is 0.", "102 (not 1002)") +
        "<h2>Before, after and between</h2>"
        "<p>After is 1 more. Before is 1 less. Between is the number in the middle.</p>"
        "<figure class='sn-fig'>" + track_svg(98, 5, 2) +
        "<figcaption>100 comes after 99 and before 101. It is between 99 and 101.</figcaption></figure>"
        "<h2>The 120 chart and number lines</h2>"
        "<p>Each row of the 120 chart has 10 numbers. Go right for 1 more. Go down for 10 more.</p>"
        "<figure class='sn-fig'>" + chart_svg(97, 3, 4) +
        "<figcaption>After 99 comes 100. The next row starts with 101. Below 100 is 110.</figcaption></figure>"
        "<figure class='sn-fig'>" + numline_svg(100, 107) +
        "<figcaption>Find 105. Count 2 small marks to the right: 106, 107. The arrow is at 107.</figcaption></figure>"
        "<h2>Order and compare</h2>"
        "<p>A number with 3 digits is bigger than a number with 2 digits. "
        "For 2-digit numbers, look at the tens first.</p>"
        + ex("Which is bigger?", "17 or 71?", "17 has 1 ten. 71 has 7 tens. 7 tens is more.", "71") +
        ex("Order from smallest to biggest", "102, 99, 110",
           "99 has only 2 digits, so it is the smallest. 102 comes before 110.", "99, 102, 110") +
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Writing 1002 for one hundred and two", "Write 102. The 0 means no tens"],
            ["Reading 17 as 71", "Read the tens digit first: 17 is 1 ten and 7 ones"],
            ["Counting 98, 99, 100, 110", "After 100 comes 101, then 102 … 110"],
            ["Writing 310 after 39", "9 ones and 1 more make a new ten: 40"],
            ["Thinking 99 is bigger than 102", "3 digits beat 2 digits: 102 is bigger"],
        ])
    )


FAQ = [
    {"q": "What numbers should a Year 1 student know in Australia?",
     "a": "The Australian Curriculum asks Year 1 students to recognise, represent and order numbers to at least 120. "
          "They count objects, read and write numerals, and use number lines and charts."},
    {"q": "Why does my child write 1002 for one hundred and two?",
     "a": "They write 100 and then 2, just as they hear it. Show 10 bundles of 10 and 2 more sticks, then point out "
          "that 102 has only three digits and the 0 means no tens."},
    {"q": "What is a 120 chart?",
     "a": "It is a chart with the numbers 1 to 120 in rows of 10. Moving right is 1 more and moving down is 10 more, "
          "so it helps students count past 100 and find missing numbers."},
    {"q": "How can I help my child count past 100 at home?",
     "a": "Count real things in tens and ones, like bundles of icy pole sticks or pegs. Practise the tricky spots out "
          "loud: 99, 100, 101 and 109, 110, 111."},
]


def gen():
    rnd = random.Random(1801)
    P = People(rnd)
    sets = [set_count(rnd, P), set_before_after(rnd, P), set_order(rnd, P), set_lines(rnd, P), set_stories(rnd, P)]
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
                    assert 0 <= v <= 120 or v in BIG_OK, c
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"]
            seen.add(key)
    u = {
        "country": "au", "subject": "maths", "grade": "year-1", "slug": "numbers-to-120", "sort": 1,
        "updated": UPDATED, "pdf_url": "",
        "title": "Numbers to 120: Count, Order and Compare Numbers",
        "seo_title": "Year 1 Numbers to 120 Maths Worksheets: Count, Order and Compare, Free with Answer Key",
        "short_title": "Numbers to 120",
        "domain": "Number",
        "standard_code": "AC9M1N01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise, represent and order numbers to at least 120 using physical and virtual materials, "
                         "numerals, number lines and charts",
        "meta_desc": "Free Year 1 numbers to 120 maths worksheets for the Australian Curriculum: count objects and "
                     "bundles of ten, numbers before, after and between, ordering numbers, number lines and the "
                     "120 chart, and comparing with more and fewer. 100 picture questions with an answer key.",
        "key_big": "Count on by ones. After 99 comes 100, then 101, 102, 103 … 110.",
        "key_sub": "One hundred and two is written 102, not 1002. To compare, look at the tens first: "
                   "71 is bigger than 17.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(\\w+ in rows of 10|rows of|number line|bundles of 10|number track|name cards)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
