# -*- coding: utf-8 -*-
"""
AU Year 6 Maths: Probability
(Australian Curriculum v9.0, AC9M6P01 and AC9M6P02)
  python3 tools/gen_au_maths_y6_probability.py
The probability scale from 0 to 1 (chance words to numbers, estimating), probability as a fraction, decimal and
percentage (1/4 = 0.25 = 25%), probability from spinners, dice, bags and cards, experiments compared with theory
(more trials get closer, expected results, simulations) and problems in context (weather forecasts, raffles, sport).
Wrong answers come from real student mistakes: probabilities bigger than 1, part-to-part instead of part-to-whole
(3 red, 5 blue gives 3/5), counting colours or sections instead of section sizes, reading 1/4 as 0.4,
adding instead of dividing, and the gambler's fallacy (after 5 tails, heads is "due").
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Australian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-6")
UPDATED = "2026-11-02"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
GREEN = "#006633"
HEAD = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
COL = {"red": "#f08a80", "blue": "#8db4ee", "yellow": "#f7dc6f", "green": "#8fd19e",
       "purple": "#c9aef0", "white": "#ffffff", "grey": "#e4e4e4"}
INIT = {"red": "R", "blue": "B", "yellow": "Y", "green": "G", "purple": "P", "white": "W"}
NUMFILL = ["#f7dc6f", "#8db4ee", "#8fd19e", "#f08a80", "#c9aef0", "#ffd3a6", "#bfe3ef", "#e4e4e4"]


NB = " "


# ------------------------------------------------------------ helpers
def fr(n, d):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (n, d)


FRX = re.compile(r"<span class='fr'><span class='fn'>(\d+)</span><span class='fd'>(\d+)</span></span>")


def val(s):
    """Numeric value of a choice (fraction, decimal or percentage), or None for words."""
    t = re.sub(r"<[^>]+>", "", FRX.sub(r"\1/\2", str(s))).replace(NB, "").strip()
    if re.match(r"^\d+/\d+$", t):
        n, d = t.split("/")
        return F(int(n), int(d))
    if re.match(r"^\d*\.?\d+%$", t):
        return F(t[:-1]) / 100
    if re.match(r"^\d*\.?\d+$", t):
        return F(t)
    return None


def mcq(q, correct, wrong, e, ans=None, same_ok=False):
    """4 choices: correct first + 3 wrong; positions are set later by balance().
    Numeric choices must all have different values (unless same_ok); ans checks the correct value."""
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4, (q, ch)
    plain = [re.sub(r"<[^>]+>", " ", x).strip() for x in ch]
    assert len(set(plain)) == 4, (q, ch)
    vals = [val(x) for x in ch]
    nums = [v for v in vals if v is not None]
    if not same_ok:
        assert len(set(nums)) == len(nums), ("two equal values", q, ch)
    if ans is not None:
        assert vals[0] == F(ans), (q, vals[0], ans)
    return {"q": q, "c": ch, "a": 0, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Picture labels A, B, C, D stay in this order."""
    assert len(choices) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "fixed": True}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each). Fixed items keep their order."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("fixed"):
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=True):
    return len(t) * fs * (0.62 if bold else 0.56)


def text(x, y, t, fs=15, anchor="middle", col=LINE, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def reorder(its, order):
    assert sorted(order) == list(range(len(its))), order
    return [its[i] for i in order]


# ------------------------------------------------------------ pictures
def secs_of(spec):
    """spec: list of (label, fraction, fill-name or colour). Fractions must add up to 1."""
    assert sum(F(f) for _, f, _ in spec) == 1, spec
    return [(l, F(f), c) for l, f, c in spec]


def label_fits(R, f, t, fs):
    """Will text t fit horizontally inside a section of size f at 0.6R? (chord check, generous margins)"""
    r = R * 0.64
    ang = 2 * math.pi * float(f)
    chord = 2 * r * math.sin(min(ang, math.pi) / 2) if ang < 2 * math.pi else 2 * R
    return tw(t, fs) + 6 <= chord and r + fs / 2 + 2 <= R


def spinner_body(cx, cy, R, spec, fs=15, initials=False, pointer=True):
    """Spinner drawn to its exact fractions, starting at 12 o'clock and going clockwise."""
    s = []
    a0 = F(0)
    labels = []
    for lab, f, c in spec:
        fill = COL.get(c, c)
        a1 = a0 + f
        t0 = 2 * math.pi * float(a0) - math.pi / 2
        t1 = 2 * math.pi * float(a1) - math.pi / 2
        if f == 1:
            s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, fill, LINE))
        else:
            x0, y0 = cx + R * math.cos(t0), cy + R * math.sin(t0)
            x1, y1 = cx + R * math.cos(t1), cy + R * math.sin(t1)
            big = 1 if f > F(1, 2) else 0
            s.append("<path d='M %.1f %.1f L %.1f %.1f A %.1f %.1f 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2' "
                     "stroke-linejoin='round'/>" % (cx, cy, x0, y0, R, R, big, x1, y1, fill, LINE))
        if lab:
            tm = (t0 + t1) / 2 if f < 1 else -math.pi / 2
            rr = R * 0.64 if f < 1 else R * 0.5
            t = INIT.get(lab, lab) if initials else lab
            assert label_fits(R, f, t, fs), (t, f, R)
            labels.append(text(cx + rr * math.cos(tm), cy + rr * math.sin(tm) + fs * 0.35, t, fs))
        a0 = a1
    s += labels
    if pointer:
        L = R * 0.28
        ang = math.radians(-50)
        tx, ty = cx + L * math.cos(ang), cy + L * math.sin(ang)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3' stroke-linecap='round'/>"
                 % (cx, cy, tx, ty, LINE))
        h1 = ang + math.radians(150)
        h2 = ang - math.radians(150)
        s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>"
                 % (tx + 3 * math.cos(ang), ty + 3 * math.sin(ang), tx + 8 * math.cos(h1), ty + 8 * math.sin(h1),
                    tx + 8 * math.cos(h2), ty + 8 * math.sin(h2), LINE))
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, LINE))
    return "".join(s)


def key_line(names):
    return ",  ".join("%s = %s" % (INIT[n], n) for n in names)


def colours_in(spec):
    out = []
    for lab, _, _ in spec:
        if lab in INIT and lab not in out:
            out.append(lab)
    return out


def spinner_svg(spec, R=66, label="spinner"):
    spec = secs_of(spec)
    words = all(not l or label_fits(R, f, l, 14) for l, f, _ in spec)
    W = 2 * R + 12
    H = 2 * R + 12
    body = spinner_body(W / 2, R + 6, R, spec, fs=14 if words else 15, initials=not words)
    if not words:
        k = key_line(colours_in(spec))
        W = int(max(W, tw(k, 14, False) + 12))
        body = spinner_body(W / 2, R + 6, R, spec, initials=True)
        body += text(W / 2, 2 * R + 30, k, 14, weight=400)
        H = 2 * R + 38
    return svg_wrap(int(W), int(H), body, label)


def spinners4_svg(specs, label="four spinners"):
    """Spinners A, B, C, D in one row, initials and one key."""
    R = 44
    gap = 22
    cell = 2 * R + gap
    names = []
    for sp in specs:
        for n in colours_in(sp):
            if n not in names:
                names.append(n)
    W = 4 * cell
    s = []
    for i, sp in enumerate(specs):
        cx = gap / 2 + R + i * cell
        s.append(spinner_body(cx, R + 4, R, secs_of(sp), fs=15, initials=True))
        s.append(text(cx, 2 * R + 26, "ABCD"[i], 17))
    k = key_line(names)
    s.append(text(W / 2, 2 * R + 50, k, 15, weight=400))
    return svg_wrap(int(W), 2 * R + 58, "".join(s), label)


def bag_svg(counts, label="bag of marbles"):
    """A jar of marbles; each marble is coloured and carries its initial. counts: list of (colour, n)."""
    marbles = [c for c, n in counts for _ in range(n)]
    n = len(marbles)
    per = min(6, n) if n <= 12 else 7
    rows = (n + per - 1) // per
    r = 13
    d = 2 * r + 4
    jw = per * d + 16
    jh = rows * d + 18
    W = int(jw + 20)
    s = ["<path d='M 10 14 L 10 %.1f Q 10 %.1f 22 %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f 14' fill='#f7f7f2' "
         "stroke='%s' stroke-width='2'/>" % (14 + jh - 12, 14 + jh, 14 + jh, 10 + jw - 12, 14 + jh, 10 + jw, 14 + jh,
                                             10 + jw, 14 + jh - 12, 10 + jw, LINE),
         "<rect x='4' y='6' width='%.1f' height='10' rx='3' fill='%s' stroke='%s' stroke-width='2'/>" % (jw + 12, "#d9cbb0", LINE)]
    # fill from the bottom row up so the jar looks natural
    for i, c in enumerate(marbles):
        row = rows - 1 - i // per
        inrow = min(per, n - (i // per) * per)
        x0 = 10 + (jw - inrow * d) / 2 + d / 2
        cx = x0 + (i % per) * d
        cy = 22 + row * d + d / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r, COL[c], LINE))
        s.append(text(cx, cy + 5, INIT[c], 14))
    k = key_line([c for c, _ in counts])
    H = 14 + jh + 26
    W = int(max(W, tw(k, 14, False) + 12))
    if W > jw + 20:  # centre the jar under a wide key
        s = ["<g transform='translate(%.1f 0)'>" % ((W - jw - 20) / 2)] + s + ["</g>"]
    s.append(text(W / 2, H - 6, k, 14, weight=400))
    return svg_wrap(W, int(H), "".join(s), label)


def tally_marks(x, cy, v):
    s = []
    for g in range(v // 5):
        for k in range(4):
            xx = x + k * 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, LINE))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x - 3, cy + 6, x + 21, cy - 6, LINE))
        x += 30
    for k in range(v % 5):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, LINE))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 30 + (v % 5) * 6


def freq_svg(title, head, cats, vals, tally=True, label="frequency table"):
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs)) + 20)
    cols = [c1]
    if tally:
        cols.append(int(max(max(tally_width(v) for v in vals) + 26, 70)))
    cols.append(int(tw("Frequency", fs) + 20))
    tot = sum(cols)
    W = int(max(tot + 8, tw(title, 16) + 16))
    x0 = (W - tot) / 2
    s = [text(W / 2, 19, title, 16)]
    top = 28
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        x = x0
        for k, cw in enumerate(cols):
            hd = r == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw, rh, HEAD if hd or k == 0 else "#ffffff", GREEN))
            last = k == len(cols) - 1
            if k == 0:
                s.append(text(x + 10, y + 19, c, fs, anchor="start"))
            elif hd:
                s.append(text(x + cw / 2 if last else x + 10, y + 19, "Frequency" if last else "Tally", fs,
                              anchor="middle" if last else "start"))
            elif last:
                s.append(text(x + cw / 2, y + 19, v, fs))
            else:
                s.append(tally_marks(x + 14, y + rh / 2, v))
            x += cw
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def dice_svg(n, size=56):
    pos = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
           5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}
    return pos[n]


def dice_row_svg(label="the six faces of a dice"):
    size, gap = 54, 12
    W = 6 * size + 5 * gap + 8
    s = []
    for i in range(1, 7):
        x = 4 + (i - 1) * (size + gap)
        s.append("<rect x='%.1f' y='4' width='%d' height='%d' rx='9' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, size, size, LINE))
        for gx, gy in dice_svg(i):
            s.append("<circle cx='%.1f' cy='%.1f' r='5' fill='%s'/>" % (x + 13 + gx * 14, 4 + 13 + gy * 14, LINE))
        s.append(text(x + size / 2, size + 26, str(i), 15))
    return svg_wrap(int(W), size + 32, "".join(s), label)



def part(spec, name):
    return sum((f for l, f, _ in secs_of(spec) if l == name), F(0))


def scale_svg(den, marks, tick_labels, words=False, label="probability scale"):
    """Probability scale from 0 to 1 with ticks every 1/den. marks: (value, letter or '') arrows above the line."""
    W, x0, L, ly = 440, 28, 384, 56

    def X(v):
        return x0 + L * float(v)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, ly, x0 + L, ly, LINE)]
    for k in range(den + 1):
        v = F(k, den)
        h = 10 if v in (0, F(1, 2), 1) else 6
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), ly - h, X(v), ly + h, LINE))
    for v, t in tick_labels:
        s.append(text(X(v), ly + 28, t, 15))
    xs = sorted(X(v) for v, _ in marks)
    assert all(b - a >= 30 for a, b in zip(xs, xs[1:])), marks
    for v, lab in marks:
        x = X(v)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, ly - 30, x, ly - 12, GREEN))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x - 6, ly - 14, x + 6, ly - 14, x, ly - 3, GREEN))
        if lab:
            s.append(text(x, ly - 34, lab, 16, col=GREEN))
    H = ly + 36
    if words:
        s.append(text(4, ly + 50, "impossible", 14, anchor="start", weight=400))
        s.append(text(X(F(1, 2)), ly + 50, "even chance", 14, weight=400))
        s.append(text(W - 4, ly + 50, "certain", 14, anchor="end", weight=400))
        s.append(text(X(F(1, 4)), ly + 50, "unlikely", 14, weight=400))
        s.append(text(X(F(3, 4)), ly + 50, "likely", 14, weight=400))
        H = ly + 58
    return svg_wrap(W, H, "".join(s), label)


TENTHS = [(F(0), "0"), (F(1, 2), "0.5"), (F(1), "1")]
ENDS = [(F(0), "0"), (F(1), "1")]


# ============================================================ set 1: the probability scale
def set_scale():
    its = []
    its.append(mcq("What is the probability of an event that is impossible?", "0", ["1", fr(1, 2), "0.1"],
                   "An impossible event can never happen, so its probability is <b>0</b>. 0.1 is very unlikely, "
                   "but it can still happen.", ans=0))
    its.append(mcq("What is the probability of an event that is certain?", "1", ["0", "100", fr(1, 2)],
                   "A certain event will happen, so its probability is <b>1</b> (or 100%). The number 100 on its own "
                   "is far bigger than 1, so it can’t be a probability.", ans=1))
    its.append(mcq("What is the probability of an event with an even chance?", fr(1, 2), ["2", "1", "0"],
                   "An even chance is halfway between 0 and 1: <b>" + fr(1, 2) + "</b> (0.5 or 50%). "
                   "2 is the number of outcomes, not the probability.", ans=F(1, 2)))
    its.append(mcq("Which number can NOT be a probability?", "1.5", ["0.5", "0", "1"],
                   "Probabilities go from 0 to 1. <b>1.5</b> is bigger than 1, so it can’t be a probability. "
                   "0 and 1 are allowed: they mean impossible and certain."))
    its.append(mcq("Which percentage can NOT be a probability?", "120%", ["12%", "0%", "100%"],
                   "As a percentage, probabilities go from 0% to 100%. <b>120%</b> is more than 100%, so it is not possible."))
    its.append(mcq(fig(scale_svg(10, [(F(8, 10), "")], TENTHS, label="probability scale arrow at 0.8")) +
                   "Which word best describes the chance shown by the arrow?", "likely",
                   ["unlikely", "certain", "even chance"],
                   "The arrow is at 0.8. That is between 0.5 and 1, close to 1: <b>likely</b>. "
                   "It is not certain, because it is not at 1."))
    its.append(mcq(fig(scale_svg(10, [(F(1, 10), "")], TENTHS, label="probability scale arrow at 0.1")) +
                   "Which word best describes the chance shown by the arrow?", "unlikely",
                   ["impossible", "likely", "even chance"],
                   "The arrow is at 0.1, close to 0 but not at 0: <b>unlikely</b>. Impossible would be exactly 0."))
    its.append(mcq("Which probability means an event is very likely?", "0.95", ["0.05", "0.5", "9.5"],
                   "<b>0.95</b> is very close to 1, so the event is very likely. 0.05 is very close to 0 (very unlikely). "
                   "9.5 is bigger than 1, so it is not a probability."))
    its.append(mcq("Which probability shows the most likely event?", "0.8", ["0.08", "0.35", "0.5"],
                   "Compare the tenths: 0.8 = 0.80 is the biggest. 0.35 has more digits, but 0.35 &lt; 0.80. "
                   "So <b>0.8</b> is most likely.", ans=F(8, 10)))
    assert max(F("0.8"), F("0.08"), F("0.35"), F("0.5")) == F("0.8")
    its.append(mcq("Which probability shows the least likely event?", "0.05", ["0.5", "0.15", "0.3"],
                   "Write them with two decimal places: 0.05, 0.50, 0.15, 0.30. The smallest is <b>0.05</b>, "
                   "so that event is least likely.", ans=F(5, 100)))
    its.append(mcq("You roll a normal six-sided dice. What is the probability of rolling a 7?", "0",
                   ["1", fr(1, 7), fr(1, 6)],
                   "A normal dice only has 1 to 6, so a 7 is impossible. Its probability is <b>0</b>.", ans=0))
    its.append(mcq("You roll a normal six-sided dice. What is the probability of rolling a number from 1 to 6?", "1",
                   [fr(1, 6), fr(1, 2), "6"],
                   "Every roll gives a number from 1 to 6, so it is certain: <b>1</b>. "
                   "6 is the number of outcomes, and probabilities are never more than 1.", ans=1))
    its.append(mcq(fig(scale_svg(4, [(F(1, 4), "")], ENDS, label="probability scale in quarters arrow at one quarter")) +
                   "The scale is split into quarters. What probability does the arrow show?", fr(1, 4),
                   [fr(3, 4), fr(1, 3), "0.4"],
                   "There are 4 equal parts from 0 to 1, and the arrow is 1 part from 0: <b>" + fr(1, 4) + "</b> (0.25). "
                   + fr(3, 4) + " counts from the 1 end. " + fr(1, 4) + " is 0.25, not 0.4.", ans=F(1, 4)))
    its.append(mcq(fig(scale_svg(10, [(F(7, 10), "")], TENTHS, label="probability scale arrow at 0.7")) +
                   "The scale is split into tenths. What probability does the arrow show?", "0.7",
                   ["0.07", "0.3", "7"],
                   "Each small step is 0.1. The arrow is 7 steps from 0, so it shows <b>0.7</b>. "
                   "0.3 counts back from 1. 7 is too big to be a probability.", ans=F(7, 10)))
    its.append(mcq(fig(scale_svg(10, [(F(3, 10), "")], TENTHS, label="probability scale arrow at 0.3")) +
                   "What is the probability shown by the arrow, as a percentage?", "30%",
                   ["3%", "70%", "0.3%"],
                   "The arrow is at 0.3. 0.3 = 30 hundredths = <b>30%</b>. 3% would be 0.03.", ans=F(3, 10)))
    its.append(mcq("Lachlan says the probability that his footy team wins on Saturday is 1.2, because they are very good. "
                   "What is wrong?", "A probability can’t be more than 1",
                   ["Nothing, strong teams can go above 1", "It should be written as 120%", "It should be 12"],
                   "Even a certain event has probability 1 (100%). <b>A probability can’t be more than 1</b>. "
                   "A very good team might be 0.8 or 0.9: likely, not certain."))
    its.append(mcq("Which list orders these probabilities from least likely to most likely?<br>0.6, 0.25, 0.9, 0.06",
                   "0.06, 0.25, 0.6, 0.9",
                   ["0.9, 0.6, 0.25, 0.06", "0.06, 0.6, 0.25, 0.9", "0.6, 0.06, 0.9, 0.25"],
                   "Write them as hundredths: 0.60, 0.25, 0.90, 0.06. Smallest to largest: <b>0.06, 0.25, 0.6, 0.9</b>. "
                   "0.25 is less than 0.6, even though 25 is more than 6."))
    assert sorted([F("0.6"), F("0.25"), F("0.9"), F("0.06")]) == [F("0.06"), F("0.25"), F("0.6"), F("0.9")]
    marks = [(F(0), "A"), (F(3, 10), "B"), (F(7, 10), "C"), (F(1), "D")]
    its.append(mcq_fixed(fig(scale_svg(10, marks, TENTHS, label="probability scale with points A B C D")) +
                         "A bag has 3 red and 7 blue marbles. You take one without looking. "
                         "Which letter shows the probability of taking a red marble?", ["A", "B", "C", "D"], 1,
                         "3 of the 10 marbles are red: " + fr(3, 10) + " = 0.3. That is point <b>B</b>. "
                         "C (0.7) is the probability of blue."))
    assert F(3, 10) == marks[1][0]
    its.append(mcq_fixed(fig(scale_svg(10, marks, TENTHS, label="probability scale with points A B C D")) +
                         "A spinner has 10 equal sections: 7 green and 3 yellow. "
                         "Which letter shows the probability of landing on green?", ["A", "B", "C", "D"], 2,
                         "7 of the 10 equal sections are green: " + fr(7, 10) + " = 0.7. That is point <b>C</b>."))
    assert F(7, 10) == marks[2][0]
    its.append(mcq("Mia estimates the probability of four events. Which estimate makes the most sense?",
                   "a hot day in Darwin in December: 0.9",
                   ["a coin landing on heads: 0.9", "rolling a 6 on a dice: 0.6", "snow at Bondi Beach in January: 0.5"],
                   "Darwin is hot in December, so 0.9 (very likely) makes sense. A coin is about 0.5 for heads, a 6 is only "
                   + fr(1, 6) + " (about 0.17), and snow at Bondi in summer is close to 0. "
                   "So the answer is <b>a hot day in Darwin in December</b>."))
    return {"title": "The probability scale from 0 to 1", "items": its}


# ============================================================ set 2: fractions, decimals and percentages
def set_fdp():
    its = []
    its.append(mcq("The probability of heads is " + fr(1, 2) + ". What is this as a decimal?", "0.5",
                   ["0.2", "1.2", "0.12"],
                   fr(1, 2) + " = 1 ÷ 2 = <b>0.5</b>. Writing the digits 1 and 2 as 0.12 or 1.2 is a common mistake.",
                   ans=F(1, 2)))
    its.append(mcq("The probability of landing on blue is " + fr(1, 4) + ". What is this as a percentage?", "25%",
                   ["14%", "4%", "40%"],
                   fr(1, 4) + " = " + fr(25, 100) + " = <b>25%</b>. 14% just writes the digits 1 and 4.", ans=F(1, 4)))
    its.append(mcq("Write the probability " + fr(3, 10) + " as a decimal.", "0.3", ["0.03", "3.1", "0.13"],
                   fr(3, 10) + " is 3 tenths = <b>0.3</b>. 0.03 is 3 hundredths.", ans=F(3, 10)))
    its.append(mcq("Write the probability 0.75 as a percentage.", "75%", ["7.5%", "0.75%", "25%"],
                   "To change a decimal to a percentage, multiply by 100: 0.75 × 100 = <b>75%</b>.", ans=F(3, 4)))
    its.append(mcq("Which fraction is equal to the probability 0.2?", fr(1, 5), [fr(1, 2), fr(2, 100), fr(1, 20)],
                   "0.2 = " + fr(2, 10) + " = <b>" + fr(1, 5) + "</b>. " + fr(1, 2) + " is 0.5, and "
                   + fr(2, 100) + " is 0.02.", ans=F(1, 5)))
    its.append(mcq("Write the probability " + fr(1, 5) + " as a percentage.", "20%", ["15%", "5%", "50%"],
                   fr(1, 5) + " = " + fr(20, 100) + " = <b>20%</b>. Multiply the top and bottom by 20.", ans=F(1, 5)))
    its.append(mcq("Write the probability " + fr(9, 10) + " as a decimal.", "0.9", ["0.09", "9.1", "0.1"],
                   fr(9, 10) + " is 9 tenths = <b>0.9</b>. 0.1 is the probability that the event does NOT happen.",
                   ans=F(9, 10)))
    its.append(mcq("Write the probability " + fr(3, 5) + " as a percentage.", "60%", ["35%", "30%", "53%"],
                   fr(3, 5) + " = " + fr(60, 100) + " = <b>60%</b>. Multiply the top and bottom by 20.", ans=F(3, 5)))
    its.append(mcq("Write the probability 40% as a fraction in simplest form.", fr(2, 5), [fr(1, 4), fr(4, 100), fr(1, 40)],
                   "40% = " + fr(40, 100) + ". Divide the top and bottom by 20: <b>" + fr(2, 5) + "</b>. "
                   + fr(4, 100) + " would be 4%.", ans=F(2, 5)))
    its.append(mcq("Write the probability 0.05 as a percentage.", "5%", ["50%", "0.05%", "0.5%"],
                   "0.05 × 100 = <b>5%</b>. 50% would be 0.5.", ans=F(5, 100)))
    its.append(mcq("Write the probability " + fr(1, 8) + " as a decimal.", "0.125", ["0.8", "0.18", "1.8"],
                   "1 ÷ 8 = <b>0.125</b>. A quick check: " + fr(1, 4) + " = 0.25, and " + fr(1, 8) + " is half of that.",
                   ans=F(1, 8)))
    its.append(mcq("Write the probability " + fr(7, 20) + " as a percentage.", "35%", ["7%", "27%", "72%"],
                   "Multiply the top and bottom by 5: " + fr(7, 20) + " = " + fr(35, 100) + " = <b>35%</b>. "
                   "27% comes from adding 7 + 20.", ans=F(7, 20)))
    its.append(mcq("Write the probability " + fr(12, 25) + " as a decimal.", "0.48", ["0.12", "0.37", "0.24"],
                   "Multiply the top and bottom by 4: " + fr(12, 25) + " = " + fr(48, 100) + " = <b>0.48</b>. "
                   "0.37 comes from adding 12 + 25.", ans=F(12, 25)))
    its.append(mcq("Write the probability " + fr(6, 8) + " as a percentage.", "75%", ["68%", "6.8%", "60%"],
                   fr(6, 8) + " = " + fr(3, 4) + " = <b>75%</b>. 68% just writes the digits 6 and 8.", ans=F(6, 8)))
    its.append(mcq("The weather forecast says there is a 30% chance of rain. What is this as a decimal?", "0.3",
                   ["0.03", "3.0", "30"],
                   "30% = " + fr(30, 100) + " = <b>0.3</b>. Divide by 100 to change a percentage to a decimal.",
                   ans=F(3, 10)))
    its.append(mcq("Which of these is NOT equal to a probability of " + fr(1, 2) + "?", "0.2",
                   ["0.5", "50%", fr(2, 4)],
                   fr(1, 2) + " = 0.5 = 50% = " + fr(2, 4) + ". <b>0.2</b> is " + fr(1, 5) + ", not a half.",
                   same_ok=True))
    its.append(mcq("Which of these is NOT equal to a probability of " + fr(3, 4) + "?", "0.34",
                   ["0.75", "75%", fr(6, 8)],
                   fr(3, 4) + " = 0.75 = 75% = " + fr(6, 8) + ". <b>0.34</b> just writes the digits 3 and 4; it is not "
                   + fr(3, 4) + ".", same_ok=True))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    assert part(sp, "blue") == F(1, 4) == F("0.25")
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "Which shows the probability of landing on blue as a fraction, a decimal and a percentage?",
                   fr(1, 4) + ", 0.25, 25%",
                   [fr(1, 4) + ", 0.4, 40%", fr(1, 4) + ", 0.14, 14%", fr(1, 2) + ", 0.5, 50%"],
                   "Blue covers one quarter of the spinner: <b>" + fr(1, 4) + " = 0.25 = 25%</b>. "
                   + fr(1, 2) + " is the probability of red. " + fr(1, 4) + " is 0.25, not 0.4 or 0.14."))
    its.append(mcq("Which probability is the largest?", fr(3, 4), ["0.7", "72%", "0.69"],
                   "Change them all to decimals: " + fr(3, 4) + " = 0.75, 0.7 = 0.70, 72% = 0.72, 0.69. "
                   "The largest is <b>" + fr(3, 4) + "</b>.", ans=F(3, 4)))
    assert F(3, 4) > max(F("0.7"), F("0.72"), F("0.69"))
    its.append(mcq("Which list orders these probabilities from smallest to largest?",
                   fr(1, 4) + ", 0.3, 35%",
                   ["35%, 0.3, " + fr(1, 4), "0.3, " + fr(1, 4) + ", 35%", fr(1, 4) + ", 35%, 0.3"],
                   "Change them to decimals: " + fr(1, 4) + " = 0.25, 0.3 = 0.30, 35% = 0.35. "
                   "So the order is <b>" + fr(1, 4) + ", 0.3, 35%</b>. " + fr(1, 4) + " is 0.25, not 0.4."))
    assert F(1, 4) < F("0.3") < F("0.35")
    return {"title": "Probability as a fraction, decimal and percentage", "items": its}


# ============================================================ set 3: spinners, dice, bags and cards
def set_find():
    its = []
    its.append(mcq("You roll a six-sided dice. What is the probability of rolling a 4?", fr(1, 6),
                   [fr(1, 4), fr(4, 6), fr(1, 5)],
                   "There are 6 equally likely outcomes and only one of them is 4: <b>" + fr(1, 6) + "</b>. "
                   + fr(4, 6) + " would be the chance of 1, 2, 3 or 4.", ans=F(1, 6)))
    its.append(mcq("You roll a six-sided dice. What is the probability of rolling an even number?", fr(3, 6),
                   [fr(1, 6), fr(2, 6), fr(6, 3)],
                   "The even numbers are 2, 4 and 6: 3 of the 6 outcomes, so <b>" + fr(3, 6) + "</b> (= " + fr(1, 2) + "). "
                   + fr(6, 3) + " is upside down: it is bigger than 1.", ans=F(1, 2)))
    its.append(mcq("You roll a six-sided dice. What is the probability of rolling a number greater than 4?", fr(2, 6),
                   [fr(3, 6), fr(4, 6), fr(1, 6)],
                   "Greater than 4 means 5 or 6: 2 of the 6 outcomes, so <b>" + fr(2, 6) + "</b>. "
                   + fr(3, 6) + " wrongly includes the 4. " + fr(1, 6) + " forgets the 5.", ans=F(1, 3)))
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 5)])) +
                   "A bag has 3 red and 5 blue marbles. You take one without looking. What is the probability of red?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 2)],
                   "There are 3 + 5 = 8 marbles and 3 are red: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares red with blue, not with all the marbles. Two colours does not mean " + fr(1, 2) + ".",
                   ans=F(3, 8)))
    its.append(mcq(fig(bag_svg([("red", 4), ("blue", 2), ("yellow", 2)])) +
                   "You take one marble without looking. What is the probability of blue?",
                   fr(2, 8), [fr(2, 6), fr(4, 8), fr(6, 8)],
                   "There are 4 + 2 + 2 = 8 marbles and 2 are blue: <b>" + fr(2, 8) + "</b> (= " + fr(1, 4) + "). "
                   + fr(2, 6) + " compares blue with the other 6 marbles, not with all 8. " + fr(4, 8) + " is red.", ans=F(1, 4)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red half")) + "What is the probability of landing on red?",
                   fr(1, 2), [fr(1, 3), fr(1, 4), fr(2, 3)],
                   "Red covers half of the spinner: <b>" + fr(1, 2) + "</b>. " + fr(1, 3) +
                   " counts the colours, but the sections are not equal.", ans=part(sp, "red")))
    sp = [("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"),
          ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow")]
    assert part(sp, "G") == F(3, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight sections three green")) +
                   "The spinner has 8 equal sections: G is green and Y is yellow. What is the probability of green?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 8)],
                   "3 of the 8 equal sections are green: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares green with yellow. " + fr(5, 8) + " is yellow.", ans=F(3, 8)))
    its.append(mcq("A spinner has 10 equal sections: 3 blue and 7 red. What is the probability of blue as a decimal?",
                   "0.3", ["0.03", "0.7", "0.37"],
                   "3 of the 10 sections are blue: " + fr(3, 10) + " = <b>0.3</b>. 0.7 is the probability of red.",
                   ans=F(3, 10)))
    its.append(mcq("A bag has 20 marbles and 5 of them are green. What is the probability of green as a percentage?",
                   "25%", ["5%", "20%", "75%"],
                   fr(5, 20) + " = " + fr(25, 100) + " = <b>25%</b>. 5% uses the number of green marbles as the "
                   "percentage. 75% is NOT green.", ans=F(5, 20)))
    its.append(mcq("A bag has 3 red and 7 yellow marbles. What is the probability of NOT getting red?",
                   fr(7, 10), [fr(3, 10), fr(7, 3), fr(1, 10)],
                   "Not red means yellow: 7 of the 10 marbles, so <b>" + fr(7, 10) + "</b>. Check: "
                   + fr(3, 10) + " + " + fr(7, 10) + " = 1.", ans=F(7, 10)))
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one. What is the probability of a multiple of 3?",
                   fr(3, 10), [fr(1, 3), fr(3, 7), fr(10, 3)],
                   "The multiples of 3 are 3, 6 and 9: 3 of the 10 cards, so <b>" + fr(3, 10) + "</b>. "
                   + fr(1, 3) + " comes from the word “3”, not from counting cards.", ans=F(3, 10)))
    assert [k for k in range(1, 11) if k % 3 == 0] == [3, 6, 9]
    sp = [(str(k), F(1, 8), NUMFILL[k - 1]) for k in range(1, 9)]
    primes = [k for k in range(1, 9) if k > 1 and all(k % d for d in range(2, k))]
    assert primes == [2, 3, 5, 7]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 to 8")) + "What is the probability of landing on a prime number?",
                   fr(4, 8), [fr(3, 8), fr(5, 8), fr(1, 8)],
                   "The prime numbers are 2, 3, 5 and 7: 4 of the 8 sections, so <b>" + fr(4, 8) + "</b> (= " + fr(1, 2) + "). "
                   + fr(5, 8) + " wrongly counts 1, which is not prime. " + fr(3, 8) + " forgets 2.", ans=F(1, 2)))
    its.append(mcq("A bag has 2 red, 3 blue and 5 green marbles. What is the probability of red or blue?",
                   fr(5, 10), [fr(2, 10), fr(3, 10), fr(5, 5)],
                   "Red or blue: 2 + 3 = 5 of the 10 marbles, so <b>" + fr(5, 10) + "</b>. " + fr(5, 5) +
                   " compares red and blue with green; it would mean certain.", ans=F(1, 2)))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("red", F(1, 8), "red"),
          ("blue", F(1, 4), "blue")]
    assert part(sp, "red") == F(1, 4) and len(sp) == 5
    its.append(mcq(fig(spinner_svg(sp, label="spinner red in two small parts")) +
                   "Red is in two small parts, each one eighth of the spinner. What is the probability of red?",
                   fr(1, 4), [fr(1, 8), fr(1, 3), fr(2, 5)],
                   fr(1, 8) + " + " + fr(1, 8) + " = " + fr(2, 8) + " = <b>" + fr(1, 4) + "</b>. "
                   + fr(2, 5) + " counts 2 of the 5 sections, but the sections are not the same size.", ans=F(1, 4)))
    word = "AUSTRALIA"
    assert word.count("A") == 3 and len(word) == 9 and len(set(word)) == 7
    its.append(mcq("The letters of AUSTRALIA are written on 9 cards. You pick one card. What is the probability of A?",
                   fr(3, 9), [fr(1, 9), fr(1, 7), fr(3, 6)],
                   "AUSTRALIA has 9 letters and 3 of them are A: <b>" + fr(3, 9) + "</b>. "
                   + fr(1, 7) + " counts the 7 different letters, but A is on 3 cards.", ans=F(1, 3)))
    its.append(mcq("A 12-sided dice has the numbers 1 to 12. What is the probability of rolling a number greater than 9, "
                   "as a percentage?", "25%", ["75%", "3%", "33%"],
                   "Greater than 9 means 10, 11 or 12: " + fr(3, 12) + " = " + fr(1, 4) + " = <b>25%</b>. "
                   "3% uses the count as the percentage.", ans=F(3, 12)))
    A = [("red", F(1, 4), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    B = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
    C = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green"),
         ("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    D = [("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("blue", F(1, 4), "blue")]
    blues = [part(x, "blue") for x in (A, B, C, D)]
    assert blues == [F(1, 2), F(1, 3), F(1, 4), F(3, 4)]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "On which spinner is the probability of blue " + fr(1, 4) + "?",
                         ["A", "B", "C", "D"], 2,
                         "On spinner <b>C</b> blue has 2 of the 8 equal sections: " + fr(2, 8) + " = " + fr(1, 4) + ". "
                         "A has 4 sections, but blue is half of it."))
    bags = {"4 red, 4 blue": (4, 4), "5 red, 10 blue": (5, 10), "2 red, 4 blue": (2, 4), "3 red, 5 blue": (3, 5)}
    assert [k for k, (r, b) in bags.items() if F(r, r + b) == F(1, 2)] == ["4 red, 4 blue"]
    its.append(mcq("Which bag gives a probability of 0.5 for taking a red marble?", "4 red, 4 blue",
                   ["5 red, 10 blue", "2 red, 4 blue", "3 red, 5 blue"],
                   "0.5 means half of the marbles are red. With <b>4 red and 4 blue</b>, 4 of 8 are red. "
                   "5 red, 10 blue gives " + fr(5, 15) + ", not " + fr(5, 10) + "."))
    its.append(mcq("A bag has 10 marbles. The probability of red is " + fr(2, 5) + ". How many red marbles are there?",
                   "4", ["2", "5", "6"],
                   fr(2, 5) + " = " + fr(4, 10) + ", so <b>4</b> of the 10 marbles are red. "
                   "2 uses the top number without changing to tenths. 6 is the number that are not red.", ans=4))
    assert F(2, 5) * 10 == 4
    its.append(mcq("A bag has 3 green marbles and some blue marbles. The probability of green is " + fr(1, 4) +
                   ". How many blue marbles are there?", "9", ["12", "4", "1"],
                   fr(1, 4) + " = " + fr(3, 12) + ", so there are 12 marbles in total. 12 − 3 = <b>9</b> blue. "
                   "12 is the total, not the number of blue marbles.", ans=9))
    assert F(3, 3 + 9) == F(1, 4)
    return {"title": "Probability from spinners, dice and bags", "items": its}


# ============================================================ set 4: experiments and theory
def set_experiments():
    its = []
    its.append(mcq("You roll a fair dice 60 times. About how many times would you expect to roll a 6?", "about 10",
                   ["about 6", "about 1", "about 30"],
                   "A 6 has probability " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10, so <b>about 10</b>."))
    assert F(1, 6) * 60 == 10
    its.append(mcq("You toss a fair coin 100 times. How many heads would you expect?", "about 50",
                   ["exactly 50", "about 100", "about 2"],
                   "Half of 100 is 50. Results change from one experiment to the next, so expect <b>about 50</b>, "
                   "not exactly 50."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red")) +
                   "You spin this spinner 40 times. About how many times would you expect red?", "about 30",
                   ["about 10", "about 3", "about 40"],
                   "Red is " + fr(3, 4) + " of the spinner. 40 ÷ 4 = 10, and 3 × 10 = 30, so <b>about 30</b>. "
                   "About 10 is for blue."))
    assert part(sp, "red") * 40 == 30
    its.append(mcq("Jack tosses a coin 50 times and gets 23 heads. What is the experimental probability of heads?",
                   fr(23, 50), [fr(23, 27), fr(1, 2), fr(27, 50)],
                   "Experimental probability = times it happened ÷ number of trials = <b>" + fr(23, 50) + "</b>. "
                   + fr(1, 2) + " is the theoretical probability. " + fr(23, 27) + " compares heads with tails.",
                   ans=F(23, 50)))
    its.append(mcq(fig(freq_svg("20 spins", "Colour", ["red", "blue"], [12, 8], tally=False, label="frequency table 20 spins")) +
                   "What is the experimental probability of red, as a decimal?", "0.6", ["0.12", "1.5", "0.4"],
                   "Red came up 12 times in 20 spins: " + fr(12, 20) + " = " + fr(6, 10) + " = <b>0.6</b>. "
                   "1.5 comes from 12 ÷ 8 (red ÷ blue), and it is bigger than 1.", ans=F(12, 20)))
    vals = [18, 12, 10]
    assert sum(vals) == 40
    its.append(mcq(fig(freq_svg("40 spins", "Colour", ["red", "blue", "yellow"], vals, tally=False,
                                label="frequency table 40 spins")) +
                   "What is the experimental probability of yellow, as a percentage?", "25%", ["10%", "40%", "30%"],
                   "Yellow came up 10 times in 40 spins: " + fr(10, 40) + " = " + fr(1, 4) + " = <b>25%</b>. "
                   "10% uses the count as the percentage.", ans=F(10, 40)))
    its.append(mcq("Zara spins a spinner 50 times and gets blue 18 times. What is the experimental probability of blue, "
                   "as a percentage?", "36%", ["18%", "32%", "64%"],
                   fr(18, 50) + " = " + fr(36, 100) + " = <b>36%</b>. 32% comes from 50 − 18. 64% is NOT blue.",
                   ans=F(18, 50)))
    its.append(mcq("A fair coin lands on tails 5 times in a row. What is the probability of heads on the next toss?",
                   fr(1, 2), [fr(5, 6), fr(1, 6), "1"],
                   "The coin has no memory. Every toss is a new trial, so heads is still <b>" + fr(1, 2) + "</b>. "
                   "Thinking heads is “due” is called the gambler’s fallacy.", ans=F(1, 2)))
    its.append(mcq("Kai has rolled a fair dice 12 times without getting a 6. What is the probability of a 6 on the next roll?",
                   fr(1, 6), ["1", fr(2, 6), fr(1, 12)],
                   "The dice does not remember earlier rolls. A 6 is still <b>" + fr(1, 6) + "</b>. "
                   "It is not certain (1), even after a long wait.", ans=F(1, 6)))
    its.append(mcq("Ava tosses a coin 10 times and gets 7 heads. Liam tosses a coin 1000 times and gets 508 heads. "
                   "Whose experimental probability of heads is closer to " + fr(1, 2) + "?",
                   "Liam’s", ["Ava’s", "They are equally close", "Neither is close"],
                   "Ava: " + fr(7, 10) + " = 0.7. Liam: " + fr(508, 1000) + " = 0.508. 0.508 is much closer to 0.5, "
                   "so <b>Liam’s</b> is closer."))
    assert abs(F(508, 1000) - F(1, 2)) < abs(F(7, 10) - F(1, 2))
    its.append(mcq("Why are Liam’s results (1000 tosses) closer to " + fr(1, 2) + " than Ava’s (10 tosses)?",
                   "More trials usually get closer to the theory",
                   ["Liam tossed the coin more carefully", "Ava’s coin must be unfair", "Big experiments are always exactly right"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the theoretical probability, but not exactly."))
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A dice rolled 60 times", "Number", ["1", "2", "3", "4", "5", "6"], vals, tally=False,
                                label="frequency table dice")) +
                   "How do these results compare with the theory?",
                   "Close: each number should come up about 10 times",
                   ["The dice must be unfair", "5 is the most likely number", "4 will come up more next time"],
                   "Theory: " + fr(1, 6) + " of 60 = 10 for each number. The results are all between 8 and 12, which is "
                   "<b>close to the theory</b>. Small differences are normal."))
    its.append(mcq("Ruby rolls a dice 600 times and gets a 6 on 104 rolls. How does this compare with the theory?",
                   "Close: theory says about 100", ["Far off: theory says about 6", "Far off: theory says about 300",
                                                    "Exactly right: theory says 104"],
                   fr(1, 6) + " of 600 = 600 ÷ 6 = 100. 104 is <b>close to 100</b>. Experiments are rarely exactly "
                   "the same as the theory."))
    assert F(600, 6) == 100
    its.append(mcq("A computer simulates tossing a fair coin 10" + NB + "000 times. About how many heads would you expect?",
                   "about 5000", ["exactly 5000", "about 1000", "about 50"],
                   "Half of 10" + NB + "000 is 5000. A simulation with many trials gets close to the theory, so expect "
                   "<b>about 5000</b>, not exactly 5000."))
    its.append(mcq("The experimental probability of a goal is 0.32 after 25 shots. How many goals were scored?", "8",
                   ["32", "17", "3"],
                   "0.32 × 25 = <b>8</b>. Check: " + fr(8, 25) + " = " + fr(32, 100) + " = 0.32. "
                   "32 would need 100 shots.", ans=8))
    assert F("0.32") * 25 == 8
    its.append(mcq("Ethan counts 40 cars passing the school. 14 of them are white. Estimate the probability that the next "
                   "car is white.", "0.35", ["0.14", "0.65", "0.4"],
                   "14 ÷ 40 = " + fr(35, 100) + " = <b>0.35</b>. 0.65 is the estimate for a car that is NOT white.",
                   ans=F(14, 40)))
    its.append(mcq("A bag has 20 marbles. Isla takes one, records its colour and puts it back. She does this 100 times "
                   "and gets red 26 times. About how many red marbles are in the bag?", "about 5",
                   ["about 26", "about 10", "about 15"],
                   "Red came up " + fr(26, 100) + " = 0.26 of the time, about a quarter. " + fr(1, 4) +
                   " of 20 is 5, so there are <b>about 5</b> red marbles. 26 is more than the whole bag."))
    assert round(F(26, 100) * 20) == 5
    its.append(mcq("Three groups spin the same spinner 20 times each. Red comes up 9, 13 and 8 times. "
                   "Use all the results to estimate the probability of red.", fr(30, 60),
                   [fr(9, 20), fr(13, 20), fr(30, 20)],
                   "Add the results: 9 + 13 + 8 = 30 reds in 3 × 20 = 60 spins. <b>" + fr(30, 60) + "</b> (= " + fr(1, 2) + "). "
                   "Using all 60 spins gives a better estimate than one group. " + fr(30, 20) + " is bigger than 1.",
                   ans=F(1, 2)))
    assert 9 + 13 + 8 == 30
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. In 200 spins, red comes up 98 times. "
                   "What do the results suggest?", "The spinner is probably not fair",
                   ["The spinner is fair", "Red will stop coming up soon", "200 spins are too few to tell"],
                   "Theory: " + fr(1, 4) + " of 200 = 50 reds. 98 is almost double that, after many spins, so "
                   "<b>the spinner is probably not fair</b>."))
    assert F(1, 4) * 200 == 50
    its.append(mcq("Grace tosses a fair coin 100 times. Which result would be the most surprising?", "92 heads",
                   ["48 heads", "53 heads", "45 heads"],
                   "Theory says about 50 heads. 45, 48 and 53 are all close to 50. <b>92 heads</b> is very far from 50."))
    return {"title": "Experiments compared with theory", "items": its}


# ============================================================ set 5: problems
def set_problems():
    its = []
    its.append(mcq("The weather forecast for Brisbane says there is a 70% chance of rain. What is this as a decimal?", "0.7",
                   ["0.07", "7.0", "0.3"],
                   "70% = " + fr(70, 100) + " = <b>0.7</b>. 0.3 is the chance that it does NOT rain.", ans=F(7, 10)))
    its.append(mcq("There is a 70% chance of rain tomorrow. What is the chance that it does NOT rain?", "30%",
                   ["70%", "3%", "0%"],
                   "Rain and no rain add up to 100%. 100% − 70% = <b>30%</b>. "
                   "It is not 0%, because 70% is not certain."))
    assert 100 - 70 == 30
    its.append(mcq("The forecast said a 70% chance of rain, but it stayed dry all day. Was the forecast wrong?",
                   "No, 70% means likely, not certain",
                   ["Yes, 70% means it will rain", "Yes, it should have said 100%", "No, 70% means unlikely"],
                   "70% means rain is likely, but there was still a 30% chance of no rain. A dry day does not make "
                   "the forecast wrong: <b>70% is likely, not certain</b>."))
    fc = {"Monday": F(45, 100), "Tuesday": F(4, 10), "Wednesday": F(1, 2), "Thursday": F(62, 100)}
    assert max(fc, key=fc.get) == "Thursday"
    its.append(mcq("The chance of rain in Melbourne: Monday 45%, Tuesday 0.4, Wednesday " + fr(1, 2) + ", Thursday 0.62. "
                   "Which day is rain most likely?", "Thursday", ["Monday", "Tuesday", "Wednesday"],
                   "Change them all to decimals: 0.45, 0.4, 0.5, 0.62. The largest is 0.62, so <b>Thursday</b>."))
    its.append(mcq("The Year 6 raffle sells 100 tickets and one ticket wins. Ruby buys 4 tickets. "
                   "What is her probability of winning, as a decimal?", "0.04", ["0.4", "0.25", "0.96"],
                   fr(4, 100) + " = <b>0.04</b>. 0.25 is " + fr(1, 4) + ", which mixes up the 4 tickets with quarters. "
                   "0.96 is the chance she does NOT win.", ans=F(4, 100)))
    its.append(mcq("Ruby has 4 of the 100 raffle tickets. What is the probability that she does NOT win, as a percentage?",
                   "96%", ["4%", "60%", "0.96%"],
                   "96 of the 100 tickets are not hers: " + fr(96, 100) + " = <b>96%</b>. 4% is her chance of winning.",
                   ans=F(96, 100)))
    its.append(mcq("A raffle at the school fete sells 200 tickets. Oliver buys 5. What is his probability of winning, "
                   "as a percentage?", "2.5%", ["5%", "25%", "0.5%"],
                   fr(5, 200) + " = " + fr(1, 40) + " = 0.025 = <b>2.5%</b>. 5% would be 5 out of 100, but there are "
                   "200 tickets.", ans=F(5, 200)))
    ends7 = [k for k in range(1, 201) if k % 10 == 7]
    assert len(ends7) == 20
    its.append(mcq("Raffle tickets are numbered 1 to 200. What is the probability that the winning ticket ends in 7?",
                   "10%", ["1%", "7%", "20%"],
                   "7, 17, 27, … 197: that is 20 tickets. " + fr(20, 200) + " = " + fr(1, 10) + " = <b>10%</b>. "
                   "20% uses the count as the percentage.", ans=F(20, 200)))
    its.append(mcq("At the sausage sizzle, 10 of the 40 sausages are vegetarian. Cooper gets one at random. "
                   "What is the probability it is vegetarian?", fr(1, 4), [fr(1, 3), fr(3, 4), fr(1, 10)],
                   fr(10, 40) + " = <b>" + fr(1, 4) + "</b>. " + fr(1, 3) + " compares 10 vegetarian with "
                   "the 30 others, not with all 40.", ans=F(10, 40)))
    its.append(mcq("At footy training, Lachlan kicks 15 goals from 20 shots. Estimate the probability he kicks a goal "
                   "with his next shot.", "0.75", ["0.15", "0.25", "1.33"],
                   fr(15, 20) + " = " + fr(75, 100) + " = <b>0.75</b>. 1.33 comes from 20 ÷ 15, and it is bigger than 1.",
                   ans=F(15, 20)))
    its.append(mcq("A lucky dip has 50 prizes and 15 of them are lollies. What is the probability of getting lollies, "
                   "as a percentage?", "30%", ["15%", "35%", "50%"],
                   fr(15, 50) + " = " + fr(30, 100) + " = <b>30%</b>. 35% comes from 50 − 15.", ans=F(15, 50)))
    its.append(mcq("At the swimming carnival, 20 of the first 50 students Sienna saw were wearing a hat. "
                   "Estimate the probability that the next student wears a hat.", "0.4", ["0.2", "0.6", "2.5"],
                   fr(20, 50) + " = " + fr(4, 10) + " = <b>0.4</b>. 2.5 comes from 50 ÷ 20, and it is bigger than 1.",
                   ans=F(20, 50)))
    its.append(mcq("Leo says, “A footy match ends in a win, a loss or a draw, so the chance of a win is " + fr(1, 3) + ".” "
                   "Is he right?", "No, the 3 outcomes are not equally likely",
                   ["Yes, there are 3 outcomes", "Yes, every match is random", "No, the chance is " + fr(1, 2)],
                   "A probability of " + fr(1, 3) + " each needs 3 <b>equally likely</b> outcomes. Draws are rare, "
                   "and a strong team wins more often. So <b>Leo is not right</b>."))
    its.append(mcq("Before a cricket match, the Australian captain has won the coin toss 3 times in a row. "
                   "What is the probability of winning the next toss?", "still " + fr(1, 2),
                   ["less than " + fr(1, 2), "more than " + fr(1, 2), "0"],
                   "A fair coin has no memory. The chance is <b>still " + fr(1, 2) + "</b> on every toss. "
                   "Winning 3 times in a row does not change the next toss."))
    its.append(mcq("A bag has 5 red and 5 blue marbles. Matilda takes a red one and does NOT put it back. "
                   "What is the probability that the next marble is red?", fr(4, 9),
                   [fr(5, 10), fr(4, 10), fr(5, 9)],
                   "Now there are 4 red and 5 blue: 9 marbles left. So the probability is <b>" + fr(4, 9) + "</b>. "
                   + fr(4, 10) + " forgets that the bag now has 9 marbles.", ans=F(4, 9)))
    its.append(mcq("A netball team has 7 bibs: GS, GA, WA, C, WD, GD and GK. Chloe takes one without looking. "
                   "What is the probability that it is NOT GK?", fr(6, 7), [fr(1, 7), fr(6, 1), fr(1, 6)],
                   "6 of the 7 bibs are not GK: <b>" + fr(6, 7) + "</b>. " + fr(6, 1) + " is upside down and bigger than 1.",
                   ans=F(6, 7)))
    its.append(mcq("A raffle has 300 tickets. How many tickets must Amelia buy to have a 10% chance of winning?", "30",
                   ["10", "3", "300"],
                   "10% of 300 = 300 ÷ 10 = <b>30</b>. Buying 10 tickets gives only " + fr(10, 300) + ", about 3%.",
                   ans=30))
    assert F(30, 300) == F(1, 10)
    its.append(mcq("Mei makes a spinner with red, blue and green. P(red) = 0.5 and P(blue) = 0.3. "
                   "What must P(green) be?", "0.2", ["0.8", "0.3", "1.2"],
                   "All the probabilities add up to 1. 1 − 0.5 − 0.3 = <b>0.2</b>. 0.8 is red and blue together.",
                   ans=F(2, 10)))
    assert 1 - F("0.5") - F("0.3") == F("0.2")
    its.append(mcq("A spinner is red, blue or yellow. P(red) = 40% and P(blue) = 35%. What is P(yellow)?", "25%",
                   ["75%", "35%", "5%"],
                   "The three add up to 100%. 100% − 40% − 35% = <b>25%</b>. 75% is red and blue together. "
                   "5% is only the difference 40% − 35%.", ans=F(25, 100)))
    assert 100 - 40 - 35 == 25
    assert F(3, 10) > F(7, 25)
    its.append(mcq("Box A has 10 tickets and 3 of them win. Box B has 25 tickets and 7 of them win. "
                   "Which box gives a better chance of winning?", "Box A",
                   ["Box B, it has more winning tickets", "They are the same", "You can’t tell"],
                   "Box A: " + fr(3, 10) + " = 30%. Box B: " + fr(7, 25) + " = " + fr(28, 100) + " = 28%. "
                   "<b>Box A</b> is better, even though Box B has more winning tickets."))
    return {"title": "Probability problems", "items": its}


# ============================================================ lesson
def body_html():
    scale = scale_svg(4, [], [(F(0), "0"), (F(1, 4), "0.25"), (F(1, 2), "0.5"), (F(3, 4), "0.75"), (F(1), "1")],
                      words=True, label="probability scale from impossible to certain")
    bag = bag_svg([("red", 3), ("blue", 5)], label="bag of 3 red and 5 blue marbles")
    return (
        "<h2>The probability scale</h2>"
        "<p>A probability is a number from <b>0</b> to <b>1</b>. 0 means impossible. 1 means certain. "
        "Halfway, " + fr(1, 2) + " or 0.5, is an even chance. A probability is never more than 1.</p>"
        "<figure class='sn-fig'>" + scale +
        "<figcaption>Every probability sits somewhere on this scale.</figcaption></figure>"
        "<p>The same probability can be written as a fraction, a decimal or a percentage. "
        "As a percentage the scale goes from 0% to 100%.</p>"
        + table(["Fraction", "Decimal", "Percentage", "Chance"], [
            ["0", "0", "0%", "impossible"],
            [fr(1, 4), "0.25", "25%", "unlikely"],
            [fr(1, 2), "0.5", "50%", "even chance"],
            [fr(3, 4), "0.75", "75%", "likely"],
            ["1", "1", "100%", "certain"],
        ])
        + "<h2>Working out a probability</h2>"
        "<p>When the outcomes are equally likely:</p>"
        "<p><b>probability = number of outcomes you want ÷ total number of outcomes</b></p>"
        "<figure class='sn-fig'>" + bag +
        "<figcaption>3 red and 5 blue marbles: 8 marbles in total.</figcaption></figure>"
        + ex("Example 1", "What is the probability of taking a red marble from this bag?",
             "There are 3 red marbles and 8 marbles altogether. Compare with all 8, not with the 5 blue.",
             fr(3, 8) + " = 0.375 = 37.5%")
        + ex("Example 2", "The forecast says a 70% chance of rain. What is the chance of no rain?",
             "The two probabilities add up to 100%: 100% − 70% = 30%.", "30% (0.3)")
        + "<h2>Experiments and theory</h2>"
        "<p>Experimental probability = number of times it happened ÷ number of trials. "
        "It is usually close to the theory, but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + table(["Coin tosses", "Heads", "Experimental probability"], [
            ["10", "7", fr(7, 10) + " = 0.7"],
            ["100", "46", fr(46, 100) + " = 0.46"],
            ["1000", "508", fr(508, 1000) + " = 0.508"],
        ])
        + ex("Example 3", "You roll a dice 60 times. About how many 6s would you expect?",
             "A 6 has probability " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10.", "about 10")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“The probability is 1.2.”", "Probabilities are never more than 1 (100%)."],
            ["3 red, 5 blue, so P(red) = " + fr(3, 5) + ".", "Divide by ALL the outcomes: " + fr(3, 8) + "."],
            [fr(1, 4) + " = 0.4", fr(1, 4) + " = 1 ÷ 4 = 0.25 = 25%."],
            ["“5 tails in a row, so heads is due.”", "A coin has no memory. Heads is still " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "What does AC9M6P01 mean in Year 6 maths?",
     "a": "It is the Australian Curriculum v9.0 content description for Year 6 probability: students recognise that probabilities lie on a scale from 0 to 1 (or 0% to 100%) and estimate probabilities using fractions, decimals and percentages."},
    {"q": "How do you write a probability as a fraction, decimal and percentage?",
     "a": "Write the fraction first (outcomes you want over all outcomes), then divide to get the decimal and multiply by 100 for the percentage. For example, 1/4 = 0.25 = 25%."},
    {"q": "What does a 70% chance of rain mean?",
     "a": "It means rain is likely, with a probability of 0.7. There is still a 30% chance of no rain, so a dry day does not mean the forecast was wrong."},
    {"q": "Why don’t experiment results match the theoretical probability exactly?",
     "a": "Chance experiments vary, so results are usually close to the theory but not the same. With more trials, such as 1000 tosses or a computer simulation (AC9M6P02), the experimental probability usually gets closer, which prepares students for Year 7 maths."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (probability scales, rows of spinners, frequency tables)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(6820)
    sets = [set_scale(), set_fdp(), set_find(), set_experiments(), set_problems()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5), s["title"]
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "au", "subject": "maths", "grade": "year-6", "slug": "probability", "sort": 20,
        "updated": UPDATED, "pdf_url": "",
        "title": "Year 6 Probability",
        "seo_title": "Year 6 Probability Worksheets: Free Maths with Answer Key (Australian Curriculum)",
        "short_title": "Probability",
        "domain": "Probability",
        "standard_code": "AC9M6P01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Recognise that probabilities lie on numerical scales of 0–1 or 0%–100% and use estimation to assign probabilities that events occur in a given context, using fraction, decimal and percentage representations",
        "meta_desc": "Free Year 6 maths worksheets on probability, aligned to the Australian Curriculum (AC9M6P01 and AC9M6P02): the probability scale from 0 to 1, fractions, decimals and percentages, spinners, dice and bags, experiments compared with theory, weather forecasts and raffles. 100 questions with an answer key.",
        "key_big": "A probability is a number from 0 (impossible) to 1 (certain): the outcomes you want ÷ all the outcomes.",
        "key_sub": "1/4 = 0.25 = 25%. 3 red and 5 blue gives 3/8, not 3/5. More trials get closer to the theory, and a coin has no memory: after 5 tails, heads is still 1/2.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(probability scale|four spinners|frequency table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
