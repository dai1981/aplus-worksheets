# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Probability experiments (BC Mathematics Curriculum, Grade 5 Content: Data and probability,
"probability experiments, single events or outcomes")
  python3 tools/gen_cabc_math_g5_probability.py
Outcomes and events of an experiment, likelihood words (impossible to certain), probability as a fraction
(spinners with unequal parts, number cubes, bags and letter cards), predicting results and comparing them with
experiments, and fair games as word problems in BC contexts.
Wrong answers come from real student mistakes: counting outcomes wrongly (including the 3 in "less than 3",
counting 22 twice, subtracting 12 − 5 to count cards 5 to 12, adding the faces), outcomes vs trials,
part-to-part instead of part-to-whole, counting colours or sections instead of part sizes, likely vs certain,
unlikely vs impossible, the gambler's fallacy, and difference vs change when fixing a game.
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
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


NB = "\u00a0"


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


def part(spec, name):
    return sum((f for l, f, _ in secs_of(spec) if l == name), F(0))



def svg_frac(x, y, n, d, fs=15, col=LINE):
    """Stacked fraction centred at x; y is the baseline of the numerator."""
    w = max(len(str(n)), len(str(d))) * fs * 0.62 + 4
    return (text(x, y, str(n), fs, col=col) +
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.5'/>" % (x - w / 2, y + 4, x + w / 2, y + 4, col) +
            text(x, y + 4 + fs + 1, str(d), fs, col=col))


def scale_svg(den, marks, tick_labels, words=False, label="probability line"):
    """Probability line from 0 to 1 with ticks every 1/den. tick_labels: values to label (0 and 1 as whole numbers,
    others as stacked fractions in their own denominator). marks: (value, letter or '') arrows above the line."""
    W, x0, L, ly = 440, 30, 380, 56

    def X(v):
        return x0 + L * float(v)

    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (x0, ly, x0 + L, ly, LINE)]
    for k in range(den + 1):
        v = F(k, den)
        h = 10 if v in (0, F(1, 2), 1) else 6
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (X(v), ly - h, X(v), ly + h, LINE))
    frac_row = False
    lx = sorted(X(v) for v, _, _ in tick_labels)
    assert all(b - a >= 34 for a, b in zip(lx, lx[1:])), tick_labels
    for v, n, d in tick_labels:
        assert F(n, d) == v and (v * den).denominator == 1
        if d == 1:
            s.append(text(X(v), ly + 34, str(n), 16))
        else:
            frac_row = True
            s.append(svg_frac(X(v), ly + 26, n, d, 14))
    xs = sorted(X(v) for v, _ in marks)
    assert all(b - a >= 30 for a, b in zip(xs, xs[1:])), marks
    for v, lab in marks:
        assert (v * den).denominator == 1
        x = X(v)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='3'/>" % (x, ly - 30, x, ly - 12, GREEN))
        s.append("<polygon points='%.1f,%d %.1f,%d %.1f,%d' fill='%s'/>" % (x - 6, ly - 14, x + 6, ly - 14, x, ly - 3, GREEN))
        if lab:
            s.append(text(x, ly - 34, lab, 16, col=GREEN))
    H = ly + (50 if frac_row else 42)
    if words:
        y = H + 12
        s.append(text(4, y, "impossible", 14, anchor="start", weight=400))
        s.append(text(X(F(1, 2)), y, "equally likely", 14, weight=400))
        s.append(text(W - 4, y, "certain", 14, anchor="end", weight=400))
        s.append(text(X(F(1, 4)) - 6, y, "unlikely", 14, weight=400))
        s.append(text(X(F(3, 4)) + 6, y, "likely", 14, weight=400))
        H = y + 8
    top = 0 if any(lab for _, lab in marks) else 14
    if top:
        return svg_wrap(W, H - top, "<g transform='translate(0 -%d)'>%s</g>" % (top, "".join(s)), label)
    return svg_wrap(W, H, "".join(s), label)


ENDS = [(F(0), 0, 1), (F(1), 1, 1)]


def ends_half(den):
    assert den % 2 == 0
    return [(F(0), 0, 1), (F(1, 2), 1, 2), (F(1), 1, 1)]


def nums_spinner(n):
    return [(str(k), F(1, n), NUMFILL[(k - 1) % len(NUMFILL)]) for k in range(1, n + 1)]



# ============================================================ set 1: outcomes of an experiment
def set_outcomes():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. How many possible outcomes are there?", "6",
                   ["1", "5", "21"],
                   "The cube can land on 1, 2, 3, 4, 5 or 6: <b>6</b> outcomes. 21 adds the numbers "
                   "(1 + 2 + 3 + 4 + 5 + 6) instead of counting them.", ans=6))
    assert sum(range(1, 7)) == 21
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 2)], label="bag of 3 red and 2 blue marbles")) +
                   "You take one marble from this bag without looking. What are the possible outcomes?",
                   "red or blue", ["red only", "3 or 2", "red, blue or yellow"],
                   "Every marble is red or blue, so the outcomes are <b>red or blue</b>. 3 and 2 are how many of each "
                   "colour, not outcomes. There is no yellow marble."))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which is NOT a possible outcome?", "7",
                   ["1", "6", "4"],
                   "The faces show 1 to 6, so <b>7</b> can never come up. 1 and 6 are the smallest and largest faces."))
    sp = [("R", F(1, 6), "red"), ("B", F(1, 6), "blue"), ("R", F(1, 6), "red"), ("Y", F(1, 6), "yellow"),
          ("B", F(1, 6), "blue"), ("R", F(1, 6), "red")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 6 sections red blue yellow")) +
                   "R is red, B is blue and Y is yellow. How many different colours can this spinner land on?", "3",
                   ["6", "2", "4"],
                   "The spinner has 6 sections, but only <b>3</b> colours: red, blue and yellow. "
                   "6 counts the sections, not the colours.", ans=3))
    its.append(mcq("Cards numbered 5 to 12 are shuffled. You pick one. How many possible outcomes are there?", "8",
                   ["7", "12", "17"],
                   "The cards are 5, 6, 7, 8, 9, 10, 11 and 12: <b>8</b> cards. 12 − 5 = 7 forgets one card. "
                   "17 adds 5 + 12.", ans=8))
    assert len(range(5, 13)) == 8
    sp = [("2", F(1, 4), NUMFILL[0]), ("4", F(1, 4), NUMFILL[1]), ("6", F(1, 4), NUMFILL[2]), ("8", F(1, 4), NUMFILL[3])]
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 4 equal sections 2 4 6 8")) +
                   "Which outcome is impossible on this spinner?", "an odd number",
                   ["an even number", "a number greater than 5", "the number 4"],
                   "All the numbers (2, 4, 6, 8) are even, so <b>an odd number</b> can never come up. "
                   "6 and 8 are greater than 5, so that can happen."))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which outcomes make the event “roll a number "
                   "greater than 4”?", "5 and 6", ["4, 5 and 6", "5 only", "1, 2, 3 and 4"],
                   "Greater than 4 means bigger than 4, so 4 itself does not count: <b>5 and 6</b>. "
                   "1, 2, 3 and 4 are the outcomes that are NOT greater than 4."))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which outcomes make the event “roll an even "
                   "number”?", "2, 4 and 6", ["2 and 4", "0, 2, 4 and 6", "1, 3 and 5"],
                   "The even numbers on the cube are <b>2, 4 and 6</b>. Don’t forget 6. There is no 0 on the cube. "
                   "1, 3 and 5 are odd."))
    sp = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 4 equal sections red blue yellow green")) +
                   "Are the 4 outcomes on this spinner equally likely?", "Yes, all 4 sections are the same size",
                   ["No, red is at the top", "No, green is the most likely", "Yes, because every spinner is fair"],
                   "Each colour has one section and all the sections are the same size, so <b>yes</b>: each colour is "
                   + fr(1, 4) + ". Where a colour sits does not matter."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "Are the 3 outcomes on this spinner equally likely?", "No, red covers more of the spinner",
                   ["Yes, there are 3 colours", "Yes, each colour has one section", "No, yellow is the biggest"],
                   "Red covers " + fr(1, 2) + " but blue and yellow cover only " + fr(1, 4) + " each. "
                   "<b>Red is more likely.</b> Count the size of the parts, not the number of colours."))
    its.append(mcq(fig(bag_svg([("green", 5), ("purple", 1)], label="bag of 5 green and 1 purple marble")) +
                   "You take one marble without looking. Which outcome is more likely?", "green",
                   ["purple", "They are equally likely", "You can’t tell"],
                   "There are 5 green marbles and only 1 purple marble, so <b>green</b> is more likely. "
                   "Two colours does not mean the two outcomes are equally likely."))
    its.append(mcq("Cards numbered 1 to 12 are shuffled. You pick one. How many outcomes make the event "
                   "“a multiple of 3”?", "4", ["3", "8", "1"],
                   "The multiples of 3 are 3, 6, 9 and 12: <b>4</b> cards. 3 forgets the 12. "
                   "8 is the number of cards that are NOT multiples of 3.", ans=4))
    assert [k for k in range(1, 13) if k % 3 == 0] == [3, 6, 9, 12]
    sp = nums_spinner(8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 8 equal sections 1 to 8")) +
                   "The spinner has 8 equal sections. How many outcomes are less than 4?", "3", ["4", "5", "2"],
                   "Less than 4 means 1, 2 or 3: <b>3</b> outcomes. 4 wrongly counts the 4. "
                   "5 counts 4 to 8, the numbers that are NOT less than 4.", ans=3))
    word = "VANCOUVER"
    assert len(word) == 9 and len(set(word)) == 8
    its.append(mcq("The letters of VANCOUVER are written on cards, one letter on each card. You pick one card. "
                   "Which is true?", "9 cards, 8 different letters",
                   ["9 cards, 9 different letters", "8 cards, 8 different letters", "9 cards, 7 different letters"],
                   "VANCOUVER has 9 letters, so 9 cards. V is on 2 cards, so there are only <b>8 different letters</b>: "
                   "V, A, N, C, O, U, E, R."))
    has2 = [k for k in range(1, 26) if "2" in str(k)]
    assert has2 == [2, 12, 20, 21, 22, 23, 24, 25]
    its.append(mcq("Cards numbered 1 to 25 are shuffled. You pick one. How many outcomes have the digit 2 in them?",
                   "8", ["9", "2", "3"],
                   "They are 2, 12, 20, 21, 22, 23, 24 and 25: <b>8</b> cards. 9 counts 22 twice, but it is only "
                   "one card. 2 and 3 forget the numbers in the twenties.", ans=8))
    vals = [8, 7, 5]
    assert sum(vals) == 20
    its.append(mcq(fig(freq_svg("Ji-woo’s spins", "Colour", ["red", "blue", "green"], vals, tally=True,
                                label="frequency table tally 20 spins")) +
                   "Ji-woo did a spinner experiment. How many trials (spins) did she do?", "20", ["3", "8", "5"],
                   "Each spin is one trial. Add the results: 8 + 7 + 5 = <b>20</b> spins. 3 is the number of "
                   "outcomes (colours), not trials.", ans=20))
    its.append(mcq("A bag has 2 red, 2 blue and 2 yellow marbles. You take one without looking. Which is true?",
                   "All 3 colours are equally likely",
                   ["Red is most likely", "Yellow is least likely", "There are only 2 possible outcomes"],
                   "Each colour has 2 marbles out of 6, so <b>all 3 colours are equally likely</b>. "
                   "The 2 is how many of each colour, not the number of outcomes."))
    its.append(mcq("A box has 12 muffins: 5 blueberry, 4 banana and 3 bran. Wei takes one without looking. "
                   "Which kind is least likely?", "bran",
                   ["blueberry", "banana", "They are all equally likely"],
                   "There are fewer bran muffins (3) than banana (4) or blueberry (5), so <b>bran</b> is least likely. "
                   "3 kinds does not mean equally likely."))
    its.append(mcq("Hana says rolling a number cube has 2 outcomes, “6” and “not 6”, so the probability of a 6 is "
                   + fr(1, 2) + ". What is her mistake?", "“6” and “not 6” are not equally likely",
                   ["Nothing, she is right", "A number cube has 7 outcomes", "She should say " + fr(2, 1)],
                   "“Not 6” is 5 outcomes (1, 2, 3, 4, 5) and “6” is only 1 outcome. <b>They are not equally likely</b>, "
                   "so P(6) = " + fr(1, 6) + ", not " + fr(1, 2) + "."))
    its.append(mcq("Lucas spins a spinner with red, blue and green sections 30 times and writes down each colour. "
                   "What are the outcomes, and what is the number of trials?", "Outcomes: red, blue, green; trials: 30",
                   ["Outcomes: 30; trials: 3", "Outcomes: red, blue, green; trials: 3", "Outcomes: red only; trials: 30"],
                   "An outcome is a result that can happen: red, blue or green. A trial is one spin, and he spins "
                   "30 times. So <b>3 outcomes, 30 trials</b>."))
    its = reorder(its, [0, 2, 1, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, 16, 17, 15, 19, 13, 14, 18])
    return {"title": "Outcomes of an experiment", "items": its}


# ============================================================ set 2: likelihood words
def set_words():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which word describes rolling a 7?", "impossible",
                   ["unlikely", "likely", "certain"],
                   "No face shows 7, so it can never happen: <b>impossible</b>. Unlikely means it can happen, but "
                   "probably won’t."))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which word describes rolling a number from 1 to 6?",
                   "certain", ["likely", "equally likely", "impossible"],
                   "Every face shows a number from 1 to 6, so it happens every time: <b>certain</b>."))
    its.append(mcq("You toss a coin. Which word describes getting heads?", "equally likely",
                   ["certain", "impossible", "unlikely"],
                   "Heads and tails each have the same chance, so heads is <b>equally likely</b> to happen or not happen."))
    bag = [("blue", 9), ("red", 1)]
    its.append(mcq(fig(bag_svg(bag, label="bag of 9 blue and 1 red marble")) +
                   "You take one marble without looking. Which word describes taking a blue marble?", "likely",
                   ["certain", "unlikely", "equally likely"],
                   "9 of the 10 marbles are blue, so blue is <b>likely</b>. It is not certain, because there is "
                   "1 red marble."))
    its.append(mcq(fig(bag_svg(bag, label="bag of 9 blue and 1 red marble")) +
                   "You take one marble without looking. Which word describes taking a red marble?", "unlikely",
                   ["impossible", "likely", "equally likely"],
                   "Only 1 of the 10 marbles is red. It can happen, but probably won’t: <b>unlikely</b>. "
                   "Impossible would mean there is no red marble at all."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red one quarter blue")) +
                   "Which word describes landing on red?", "likely", ["certain", "unlikely", "equally likely"],
                   "Red covers " + fr(3, 4) + " of the spinner, more than half: <b>likely</b>. "
                   "It is not certain, because blue can still come up."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red half blue")) +
                   "Which word describes landing on blue?", "equally likely", ["unlikely", "likely", "certain"],
                   "Blue covers exactly half of the spinner, so blue is <b>equally likely</b> to come up or not."))
    its.append(mcq("Which word means the same as a probability of 0?", "impossible", ["unlikely", "certain", "equally likely"],
                   "A probability of 0 means the event can never happen: <b>impossible</b>. A probability of 1 means certain."))
    its.append(mcq("Which event is certain?", "Monday comes after Sunday",
                   ["Rolling a 6 on a number cube", "A coin lands on heads", "Getting a red marble from a bag of red and blue"],
                   "The days of the week always come in the same order, so <b>Monday after Sunday</b> is certain. "
                   "The others can happen, but not every time."))
    its.append(mcq("Which event is impossible?", "Taking a green marble from a bag of red and blue marbles",
                   ["Rolling a 1 on a number cube", "Taking a red marble from a bag of red and blue marbles",
                    "Landing on blue on a red and blue spinner"],
                   "There are no green marbles in the bag, so <b>taking green</b> can never happen. The others can happen."))
    its.append(mcq(fig(scale_svg(8, [(F(1, 8), "")], ends_half(8), label="probability line in eighths arrow at one eighth")) +
                   "Which word best describes the chance shown by the arrow?", "unlikely",
                   ["impossible", "likely", "equally likely"],
                   "The arrow is close to 0 but not at 0: <b>unlikely</b>. Impossible would be exactly at 0."))
    its.append(mcq(fig(scale_svg(8, [(F(7, 8), "")], ends_half(8), label="probability line in eighths arrow at seven eighths")) +
                   "Which word best describes the chance shown by the arrow?", "likely",
                   ["certain", "unlikely", "equally likely"],
                   "The arrow is between " + fr(1, 2) + " and 1, close to 1: <b>likely</b>. "
                   "Certain would be exactly at 1."))
    its.append(mcq("Which event is likely?", "Snow falls at Whistler sometime in January",
                   ["Snow falls in Victoria on Canada Day", "A coin lands on tails", "Rolling a 2 on a number cube"],
                   "Whistler is in the mountains and it almost always snows there in winter, so that is <b>likely</b>. "
                   "Snow on July 1 in Victoria is close to impossible. A coin is equally likely. A 2 is unlikely ("
                   + fr(1, 6) + ")."))
    its.append(mcq("Which fraction describes an unlikely event?", fr(1, 10), [fr(9, 10), fr(1, 2), fr(10, 10)],
                   "<b>" + fr(1, 10) + "</b> is between 0 and " + fr(1, 2) + ", close to 0: unlikely. " + fr(9, 10) +
                   " is likely and " + fr(10, 10) + " = 1 is certain.", ans=F(1, 10)))
    its.append(mcq("Which word describes a probability of " + fr(5, 6) + "?", "likely",
                   ["unlikely", "certain", "impossible"],
                   fr(5, 6) + " is more than " + fr(1, 2) + " but less than 1: <b>likely</b>. It is not certain, because "
                   "it is not " + fr(6, 6) + "."))
    its.append(mcq(fig(bag_svg([("red", 6), ("blue", 3), ("yellow", 1)], label="bag of 6 red 3 blue 1 yellow")) +
                   "You take one marble without looking. Order the colours from least likely to most likely.",
                   "yellow, blue, red", ["red, blue, yellow", "blue, yellow, red", "yellow, red, blue"],
                   "Yellow has 1 marble, blue 3 and red 6. From least to most likely: <b>yellow, blue, red</b>."))
    A = [("red", F(1), "red")]
    B = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    C = [("red", F(1, 8), "red"), ("blue", F(7, 8), "blue")]
    D = [("blue", F(1), "blue")]
    reds = [part(x, "red") for x in (A, B, C, D)]
    assert reds == [1, F(1, 2), F(1, 8), 0]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D], label="four spinners red and blue")) +
                         "On which spinner is landing on red unlikely?", ["A", "B", "C", "D"], 2,
                         "On spinner <b>C</b> red is a small part (" + fr(1, 8) + "), so red can happen but probably won’t. "
                         "A is certain, B is equally likely and D is impossible."))
    A = [("blue", F(3, 4), "blue"), ("red", F(1, 4), "red")]
    B = [("blue", F(1), "blue")]
    C = [("blue", F(1, 2), "blue"), ("yellow", F(1, 2), "yellow")]
    D = [("red", F(1, 2), "red"), ("yellow", F(1, 2), "yellow")]
    blues = [part(x, "blue") for x in (A, B, C, D)]
    assert blues == [F(3, 4), 1, F(1, 2), 0]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D], label="four spinners blue red yellow")) +
                         "On which spinner is landing on blue certain?", ["A", "B", "C", "D"], 1,
                         "Spinner <b>B</b> is all blue, so it lands on blue every time. On A blue is only likely, "
                         "because red can still come up."))
    its.append(mcq("Liam rolls a number cube 10 times and never gets a 6. He says rolling a 6 is impossible. "
                   "What is wrong?", "A 6 is on the cube, so it is unlikely, not impossible",
                   ["Nothing, he is right", "A 6 is now certain on the next roll", "A 6 is likely"],
                   "One face shows 6, so a 6 can always happen. Its probability is " + fr(1, 6) + ": "
                   "<b>unlikely, not impossible</b>. It is not “due” either."))
    its.append(mcq("Ava’s spinner is " + fr(7, 8) + " green and " + fr(1, 8) + " white. She says landing on green is "
                   "certain. What is wrong?", "It is likely, not certain: white can still come up",
                   ["Nothing, she is right", "It is impossible", "It is equally likely"],
                   fr(7, 8) + " is close to 1, but not 1. White covers " + fr(1, 8) + ", so green is "
                   "<b>likely, not certain</b>."))
    return {"title": "Likelihood words: impossible to certain", "items": its}


# ============================================================ set 3: probability as a fraction
def set_fraction():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 3?", fr(1, 6),
                   [fr(3, 6), fr(1, 3), fr(6, 1)],
                   "There are 6 equally likely outcomes and only one of them is 3: <b>" + fr(1, 6) + "</b>. "
                   + fr(3, 6) + " uses the 3 as the count, but only one face shows a 3. " + fr(6, 1) + " is upside down.",
                   ans=F(1, 6)))
    sp = nums_spinner(5)
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 5 equal sections 1 to 5")) +
                   "The spinner has 5 equal sections. What is the probability of landing on 4?", fr(1, 5),
                   [fr(4, 5), fr(1, 4), fr(5, 1)],
                   "4 is on 1 of the 5 equal sections: <b>" + fr(1, 5) + "</b>. " + fr(1, 4) +
                   " compares the 4 with the other 4 sections, not with all 5.", ans=F(1, 5)))
    its.append(mcq(fig(bag_svg([("red", 2), ("blue", 3)], label="bag of 2 red and 3 blue marbles")) +
                   "A bag has 2 red and 3 blue marbles. You take one without looking. What is the probability of red?",
                   fr(2, 5), [fr(2, 3), fr(3, 5), fr(1, 2)],
                   "There are 2 + 3 = 5 marbles and 2 are red: <b>" + fr(2, 5) + "</b>. " + fr(2, 3) +
                   " compares red with blue, not with all 5 marbles. Two colours does not mean " + fr(1, 2) + ".",
                   ans=F(2, 5)))
    sp = [("R", F(1, 6), "red"), ("B", F(1, 6), "blue"), ("B", F(1, 6), "blue"), ("R", F(1, 6), "red"),
          ("B", F(1, 6), "blue"), ("B", F(1, 6), "blue")]
    assert part(sp, "R") == F(2, 6)
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 6 equal sections 2 red 4 blue")) +
                   "The spinner has 6 equal sections: R is red and B is blue. What is the probability of red?",
                   fr(2, 6), [fr(2, 4), fr(4, 6), fr(6, 2)],
                   "2 of the 6 equal sections are red: <b>" + fr(2, 6) + "</b>. " + fr(2, 4) +
                   " compares red with blue. " + fr(4, 6) + " is blue. " + fr(6, 2) + " is upside down.", ans=F(2, 6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
                   "less than 3?", fr(2, 6), [fr(3, 6), fr(1, 6), fr(4, 6)],
                   "Less than 3 means 1 or 2: 2 of the 6 outcomes, so <b>" + fr(2, 6) + "</b>. "
                   + fr(3, 6) + " wrongly counts the 3. " + fr(4, 6) + " is the chance of 3 or more.", ans=F(1, 3)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of NOT rolling a 6?",
                   fr(5, 6), [fr(1, 6), fr(6, 5), fr(4, 6)],
                   "Not a 6 means 1, 2, 3, 4 or 5: 5 of the 6 outcomes, so <b>" + fr(5, 6) + "</b>. "
                   + fr(1, 6) + " is the chance of rolling a 6.", ans=F(5, 6)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "What is the probability of landing on blue?", fr(1, 4), [fr(1, 3), fr(1, 2), fr(3, 4)],
                   "Blue covers one quarter of the spinner: <b>" + fr(1, 4) + "</b>. " + fr(1, 3) +
                   " counts the 3 colours, but red is bigger than blue.", ans=part(sp, "blue")))
    its.append(mcq(fig(bag_svg([("green", 4), ("yellow", 1), ("purple", 3)], label="bag of 4 green 1 yellow 3 purple")) +
                   "You take one marble without looking. What is the probability of green?",
                   fr(4, 8), [fr(4, 4), fr(1, 3), fr(3, 8)],
                   "There are 4 + 1 + 3 = 8 marbles and 4 are green: <b>" + fr(4, 8) + "</b>. " + fr(4, 4) +
                   " compares green with the other 4 marbles. " + fr(1, 3) + " counts colours, not marbles.",
                   ans=F(1, 2)))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("red", F(1, 8), "red"),
          ("blue", F(1, 4), "blue")]
    assert part(sp, "red") == F(1, 4) and len(sp) == 5
    its.append(mcq(fig(spinner_svg(sp, label="spinner red in two small parts")) +
                   "Red is in two small parts. Each one is " + fr(1, 8) + " of the spinner. What is the probability of red?",
                   fr(2, 8), [fr(1, 8), fr(1, 3), fr(2, 5)],
                   fr(1, 8) + " + " + fr(1, 8) + " = <b>" + fr(2, 8) + "</b> (= " + fr(1, 4) + "). "
                   + fr(2, 5) + " counts 2 of the 5 sections, but the sections are not the same size.", ans=F(1, 4)))
    its.append(mcq("A number cube has the numbers 1, 1, 2, 2, 2 and 3 on its faces. What is the probability of "
                   "rolling a 2?", fr(3, 6), [fr(1, 3), fr(1, 6), fr(3, 3)],
                   "3 of the 6 faces show a 2: <b>" + fr(3, 6) + "</b>. " + fr(1, 3) + " counts the 3 different numbers, "
                   "but 2 is on more faces than 1 or 3.", ans=F(1, 2)))
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
                         "Spinner A has 4 sections, but blue covers half of it."))
    its.append(mcq("A bag has 3 red, 5 blue and 2 yellow marbles. What is the probability of NOT taking red?",
                   fr(7, 10), [fr(3, 10), fr(7, 3), fr(5, 10)],
                   "Not red means blue or yellow: 5 + 2 = 7 of the 10 marbles, so <b>" + fr(7, 10) + "</b>. "
                   + fr(5, 10) + " forgets the yellow marbles. " + fr(3, 10) + " is the chance of red.", ans=F(7, 10)))
    word = "KAMLOOPS"
    assert word.count("O") == 2 and len(word) == 8 and len(set(word)) == 7
    its.append(mcq("The letters of KAMLOOPS are written on 8 cards. You pick one card without looking. "
                   "What is the probability of O?", fr(2, 8), [fr(1, 8), fr(2, 6), fr(2, 7)],
                   "KAMLOOPS has 8 letters and 2 of them are O: <b>" + fr(2, 8) + "</b>. " + fr(2, 7) +
                   " counts the 7 different letters. " + fr(2, 6) + " compares the O cards with the other 6 cards.",
                   ans=F(1, 4)))
    word = "NANAIMO"
    assert word.count("N") == 2 and len(word) == 7 and len(set(word)) == 5
    its.append(mcq("The letters of NANAIMO are written on 7 cards. You pick one card without looking. "
                   "What is the probability of N?", fr(2, 7), [fr(1, 7), fr(2, 5), fr(1, 5)],
                   "NANAIMO has 7 letters and 2 of them are N: <b>" + fr(2, 7) + "</b>. " + fr(1, 5) +
                   " counts the 5 different letters (N, A, I, M, O). " + fr(2, 5) +
                   " compares the N cards with the other 5 cards.", ans=F(2, 7)))
    mult4 = [k for k in range(1, 13) if k % 4 == 0]
    assert mult4 == [4, 8, 12]
    its.append(mcq("Cards numbered 1 to 12 are shuffled. You pick one. What is the probability of a multiple of 4?",
                   fr(3, 12), [fr(4, 12), fr(2, 12), fr(9, 12)],
                   "The multiples of 4 are 4, 8 and 12: 3 of the 12 cards, so <b>" + fr(3, 12) + "</b>. "
                   + fr(4, 12) + " uses the 4 from the question. " + fr(2, 12) + " forgets the 12. " + fr(9, 12) +
                   " is the chance of NOT a multiple of 4.", ans=F(1, 4)))
    its.append(mcq("A drawer has 12 socks: 5 black, 4 white and 3 grey. Owen takes one sock without looking. "
                   "What is the probability that it is white or grey?", fr(7, 12), [fr(3, 12), fr(4, 12), fr(7, 5)],
                   "White or grey: 4 + 3 = 7 of the 12 socks, so <b>" + fr(7, 12) + "</b>. "
                   + fr(7, 5) + " compares with the 5 black socks and is greater than 1.", ans=F(7, 12)))
    its.append(mcq("A bag has 3 red and 4 blue marbles. Nadia says the probability of red is " + fr(3, 4) +
                   ". What is her mistake?", "She compared red with blue, not with all 7 marbles",
                   ["Nothing, " + fr(3, 4) + " is right", "She should write " + fr(4, 3),
                    "It should be " + fr(1, 2) + " because there are 2 colours"],
                   "A probability compares with ALL the outcomes. There are 3 + 4 = 7 marbles, so P(red) = "
                   + fr(3, 7) + ". <b>She compared red with blue</b> instead of with all 7 marbles."))
    assert F(3, 3 + 4) == F(3, 7)
    its.append(mcq("A bag has 10 marbles. The probability of red is " + fr(2, 5) + ". How many red marbles are there?",
                   "4", ["2", "5", "6"],
                   fr(2, 5) + " = " + fr(4, 10) + ", so <b>4</b> of the 10 marbles are red. "
                   "2 uses the numerator without changing to tenths. 6 is the number that are not red.", ans=4))
    assert F(2, 5) * 10 == 4
    its.append(mcq("Mateo wants a spinner with 8 equal sections where the probability of green is " + fr(3, 4) +
                   ". How many sections should be green?", "6", ["3", "4", "2"],
                   fr(3, 4) + " = " + fr(6, 8) + ", so <b>6</b> of the 8 sections should be green. "
                   "3 uses the numerator without changing to eighths. 2 is the number that are not green.", ans=6))
    assert F(6, 8) == F(3, 4)
    its.append(mcq("A bag has 3 green marbles and some blue marbles. The probability of green is " + fr(1, 4) +
                   ". How many blue marbles are there?", "9", ["12", "4", "1"],
                   fr(1, 4) + " = " + fr(3, 12) + ", so there are 12 marbles in total. 12 − 3 = <b>9</b> blue. "
                   "12 is the total, not the number of blue marbles.", ans=9))
    assert F(3, 3 + 9) == F(1, 4)
    return {"title": "Probability as a fraction", "items": its}


# ============================================================ set 4: predict, then compare with results
def set_predict():
    its = []
    its.append(mcq("Liam rolls a number cube 60 times. About how many times should he expect to roll a 6?", "about 10",
                   ["about 6", "about 1", "about 30"],
                   "A 6 has a probability of " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10, so <b>about 10</b>. "
                   "About 6 uses the number on the face."))
    assert F(1, 6) * 60 == 10
    its.append(mcq("Olivia tosses a coin 100 times. How many heads should she predict?", "about 50",
                   ["exactly 50", "about 100", "about 2"],
                   "Half of 100 is 50. Results change from one experiment to the next, so predict <b>about 50</b>, "
                   "not exactly 50."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red one quarter blue")) +
                   "Chloe spins this spinner 40 times. About how many times should she expect red?", "about 30",
                   ["about 10", "about 20", "about 40"],
                   "Red is " + fr(3, 4) + " of the spinner. 40 ÷ 4 = 10, and 3 × 10 = 30, so <b>about 30</b>. "
                   "About 10 is for blue. About 20 thinks 2 colours means " + fr(1, 2) + "."))
    assert part(sp, "red") * 40 == 30
    sp = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 4 equal sections red blue yellow green")) +
                   "Kai spins this spinner 80 times. About how many times should he expect green?", "about 20",
                   ["about 4", "about 40", "about 60"],
                   "Green is " + fr(1, 4) + " of the spinner. 80 ÷ 4 = <b>about 20</b>. About 40 thinks “green or not "
                   "green” is " + fr(1, 2) + ". About 60 is for the other 3 colours."))
    assert F(1, 4) * 80 == 20
    its.append(mcq("A bag has 1 red and 4 blue marbles. Owen takes a marble, records the colour and puts it back. "
                   "He does this 50 times. About how many times should he get red?", "about 10",
                   ["about 12", "about 1", "about 40"],
                   "P(red) = " + fr(1, 5) + ". 50 ÷ 5 = 10, so <b>about 10</b>. About 12 uses " + fr(1, 4) +
                   " (red compared with blue). About 40 is for blue."))
    assert F(1, 5) * 50 == 10 and 50 // 4 == 12
    its.append(mcq("Noah tosses a coin 20 times and gets 9 heads. What fraction of his tosses were heads?",
                   fr(9, 20), [fr(9, 11), fr(1, 2), fr(11, 20)],
                   "Heads came up 9 times in 20 tosses: <b>" + fr(9, 20) + "</b>. " + fr(1, 2) +
                   " is the prediction, not the result. " + fr(9, 11) + " compares heads with tails.", ans=F(9, 20)))
    its.append(mcq(fig(freq_svg("20 spins", "Colour", ["red", "blue"], [12, 8], tally=False,
                                label="frequency table 20 spins")) +
                   "Simran’s class recorded 20 spins. In what fraction of the spins did red come up?", fr(12, 20),
                   [fr(12, 8), fr(8, 20), fr(1, 2)],
                   "Red came up 12 times in 20 spins: <b>" + fr(12, 20) + "</b>. " + fr(12, 8) +
                   " compares red with blue and is greater than 1. " + fr(8, 20) + " is blue.", ans=F(12, 20)))
    vals = [15, 9, 6]
    assert sum(vals) == 30
    its.append(mcq(fig(freq_svg("Sofia’s 30 spins", "Colour", ["green", "red", "yellow"], vals, tally=True,
                                label="frequency table tally 30 spins")) +
                   "In what fraction of Sofia’s spins did red come up?", fr(9, 30), [fr(9, 21), fr(1, 3), fr(6, 30)],
                   "Red came up 9 times in 30 spins: <b>" + fr(9, 30) + "</b>. " + fr(9, 21) +
                   " compares red with the other 21 spins. " + fr(1, 3) + " would be the prediction for 3 equal colours.",
                   ans=F(9, 30)))
    its.append(mcq("Lucas spins a spinner with 3 equal sections (red, blue, yellow) 30 times. He predicts about 10 reds "
                   "and gets 11. What does this show?", "The result is close to the prediction",
                   ["The spinner is broken", "His prediction was wrong", "He will get exactly 10 next time"],
                   "30 ÷ 3 = 10, so about 10 reds is a good prediction. 11 is only 1 more: <b>close to the prediction</b>. "
                   "Results are rarely exactly the same as the prediction."))
    assert F(1, 3) * 30 == 10
    its.append(mcq("Ji-woo spins a spinner that is half red 10 times. Red comes up only 3 times. What does this show?",
                   "Not much: a few spins can be far from the prediction",
                   ["The spinner must be broken", "Red should come up exactly 5 times", "The chance of red must be " + fr(3, 10)],
                   "She predicts about 5 reds in 10 spins, but with only 10 spins luck changes the results a lot. "
                   "<b>A few spins can be far from the prediction.</b> She should do many more spins."))
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A number cube rolled 60 times", "Number", ["1", "2", "3", "4", "5", "6"], vals,
                                tally=False, label="frequency table number cube")) +
                   "How do these results compare with the prediction?",
                   "Close: each number should come up about 10 times",
                   ["The number cube must be unfair", "5 is the most likely number", "4 will come up more next time"],
                   "Prediction: " + fr(1, 6) + " of 60 = 10 for each number. The results are all between 8 and 12, which "
                   "is <b>close to the prediction</b>. Small differences are normal."))
    its.append(mcq("Ava tosses a coin 10 times and gets 7 heads. Ethan tosses a coin 200 times and gets 104 heads. "
                   "Whose results are closer to the prediction (half heads)?", "Ethan’s",
                   ["Ava’s", "They are equally close", "Neither"],
                   "Ava got " + fr(7, 10) + " heads, which is " + fr(2, 10) + " more than " + fr(1, 2) + ". Ethan got "
                   + fr(104, 200) + ", only " + fr(4, 200) + " more than " + fr(1, 2) + ". So <b>Ethan’s</b> results are closer."))
    assert abs(F(104, 200) - F(1, 2)) < abs(F(7, 10) - F(1, 2))
    its.append(mcq("Why are Ethan’s results (200 tosses) closer to the prediction than Ava’s (10 tosses)?",
                   "More trials usually get closer to the prediction",
                   ["Ethan tossed the coin more carefully", "Ava’s coin must be unfair",
                    "Big experiments are always exactly right"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the prediction, but not exactly."))
    its.append(mcq("Before each soccer game, a coin is tossed to decide which team starts. Tails has come up "
                   "5 games in a row. What is the probability of heads at the next game?",
                   fr(1, 2), [fr(5, 6), fr(1, 6), "1"],
                   "The coin has no memory. Every toss is a new trial, so heads is still <b>" + fr(1, 2) + "</b>. "
                   "Heads is not “due” after a lot of tails.", ans=F(1, 2)))
    its.append(mcq("Harjot has rolled a number cube 12 times without getting a 6. What is the probability of a 6 "
                   "on the next roll?", fr(1, 6), ["1", fr(2, 6), fr(1, 12)],
                   "The number cube does not remember earlier rolls. A 6 is still <b>" + fr(1, 6) + "</b>. "
                   "It is not certain (1), even after a long wait.", ans=F(1, 6)))
    its.append(mcq("Three groups spin the same spinner 20 times each. Red comes up 9, 13 and 8 times. "
                   "Use all the results: in what fraction of the spins did red come up?", fr(30, 60),
                   [fr(9, 20), fr(13, 20), fr(30, 20)],
                   "Add the results: 9 + 13 + 8 = 30 reds in 20 + 20 + 20 = 60 spins: <b>" + fr(30, 60) + "</b>. "
                   "Using all 60 spins is better than one group. " + fr(30, 20) + " is greater than 1.",
                   ans=F(1, 2)))
    assert 9 + 13 + 8 == 30
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. At the school fun fair, red comes up "
                   "98 times in 200 spins. What do the results suggest?", "The spinner is probably not fair",
                   ["The spinner is fair", "Red will stop coming up soon", "200 spins are too few to tell"],
                   "Prediction: " + fr(1, 4) + " of 200 = 50 reds. 98 is almost double that, after many spins, so "
                   "<b>the spinner is probably not fair</b>."))
    assert F(1, 4) * 200 == 50
    its.append(mcq("At hockey practice, Leah scores on 8 of her 20 shots. Next practice she takes 10 shots. "
                   "About how many goals should she predict?", "about 4", ["about 8", "about 2", "about 10"],
                   "She scored on " + fr(8, 20) + " = " + fr(4, 10) + " of her shots. So in 10 shots, predict "
                   "<b>about 4</b> goals. 8 was for 20 shots, not 10."))
    assert F(8, 20) * 10 == 4
    its.append(mcq("Owen counts 40 cars passing his school in Surrey. 14 of them are white. About how many of the next "
                   "20 cars should be white?", "about 7", ["about 14", "about 6", "about 20"],
                   "20 cars is half of 40, so predict about half of 14: <b>about 7</b>. About 6 comes from 20 − 14."))
    assert F(14, 40) * 20 == 7
    its.append(mcq("A bag has 20 marbles. Mei takes one, records its colour and puts it back. She does this 40 times "
                   "and gets red 10 times. About how many red marbles are in the bag?", "about 5",
                   ["about 10", "about 2", "about 20"],
                   "Red came up " + fr(10, 40) + " = " + fr(1, 4) + " of the time. " + fr(1, 4) + " of 20 is 5, so there "
                   "are <b>about 5</b> red marbles. 10 is how many times red came up, not how many are in the bag."))
    assert F(10, 40) * 20 == 5
    return {"title": "Predict, then compare with the results", "items": its}


# ============================================================ set 5: fair games (word problems)
def set_fair():
    its = []
    its.append(mcq("In a game, Emma wins if a coin lands on heads and Lucas wins if it lands on tails. Is the game fair?",
                   "Yes, each has a probability of " + fr(1, 2),
                   ["No, Emma is more likely to win", "No, Lucas is more likely to win", "You can’t tell"],
                   "A game is fair when every player has the same chance of winning. Heads and tails are each "
                   + fr(1, 2) + ", so <b>the game is fair</b>."))
    its.append(mcq("Simran and Arjun roll a number cube. Simran wins on 1 or 2. Arjun wins on 3, 4, 5 or 6. "
                   "Is the game fair?", "No, Arjun is more likely to win",
                   ["Yes, it is fair", "No, Simran is more likely to win", "Yes, both of them have numbers"],
                   "Simran: " + fr(2, 6) + ". Arjun: " + fr(4, 6) + ". The chances are not equal, so the game is not fair: "
                   "<b>Arjun is more likely to win</b>."))
    its.append(mcq("On the BC Ferries trip to Nanaimo, Owen and Leah play with a number cube. Owen wins on a 6. "
                   "Leah wins on a 1. On any other number they roll again. Is the game fair?",
                   "Yes, a 6 and a 1 are each " + fr(1, 6),
                   ["No, 6 is a bigger number", "No, Leah is more likely to win", "No, most rolls are a tie"],
                   "Each number is on one face, so a 6 and a 1 both have a probability of " + fr(1, 6) + ". "
                   "<b>The game is fair.</b> A bigger number is not more likely."))
    its.append(mcq("Kai wins if a number cube shows an even number. Which rule for Ethan makes the game fair?",
                   "Ethan wins on an odd number",
                   ["Ethan wins on a 1", "Ethan wins on a 5 or a 6", "Ethan wins on a number less than 6"],
                   "Kai has 2, 4, 6: " + fr(3, 6) + ". <b>Odd numbers</b> (1, 3, 5) are also " + fr(3, 6) + ", so the "
                   "game is fair. A 1 is only " + fr(1, 6) + ", and 5 or 6 is " + fr(2, 6) + "."))
    its.append(mcq("Jasleen and Harjot pick a card from cards numbered 1 to 10. Jasleen wins on 1 to 5. Harjot wins "
                   "on 6 to 10. Is the game fair?", "Yes, each has 5 of the 10 cards",
                   ["No, Harjot has the bigger numbers", "No, Jasleen has the card 1", "No, 10 is a two-digit number"],
                   "Jasleen has 5 cards (1 to 5) and Harjot has 5 cards (6 to 10): " + fr(5, 10) + " each. "
                   "<b>The game is fair.</b> How big the numbers are does not matter."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter green")) +
                   "Chloe wins if the spinner lands on red. Ryan wins if it lands on blue or green. Is the game fair?",
                   "Yes, each has a probability of " + fr(1, 2),
                   ["No, Ryan has 2 colours", "No, Chloe has the biggest section", "No, there are 3 colours"],
                   "Chloe: " + fr(1, 2) + ". Ryan: " + fr(1, 4) + " + " + fr(1, 4) + " = " + fr(1, 2) + ". "
                   "<b>Both have " + fr(1, 2) + "</b>, so the game is fair."))
    assert part(sp, "red") == part(sp, "blue") + part(sp, "green")
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 8), "blue"), ("green", F(1, 8), "green"), ("blue", F(1, 8), "blue"),
          ("blue", F(1, 8), "blue")]
    assert part(sp, "red") == F(1, 2) and part(sp, "blue") == F(3, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red three eighths blue one eighth green")) +
                   "Zara wins on red. Harjot wins on blue. Is the game fair?", "No, Zara is more likely to win",
                   ["No, Harjot is more likely to win: blue has 3 sections", "Yes, it is fair", "You can’t tell"],
                   "Red covers " + fr(1, 2) + " = " + fr(4, 8) + ". Blue has 3 small sections: " + fr(3, 8) + ". "
                   + fr(4, 8) + " &gt; " + fr(3, 8) + ", so <b>Zara is more likely to win</b>. Look at the size of "
                   "the parts, not the number of sections."))
    sp = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 3 equal sections red blue yellow")) +
                   "Mei wins on red. Mateo wins on blue. On yellow, nobody wins and they spin again. Is the game fair?",
                   "Yes, red and blue are each " + fr(1, 3),
                   ["No, there are 3 colours", "No, yellow is a third player", "No, Mei is more likely to win"],
                   "Mei and Mateo each have one equal section: " + fr(1, 3) + " each. Yellow does not help either "
                   "player, so <b>the game is fair</b>."))
    its.append(mcq("Wei and Nadia roll a number cube. Wei wins on a number less than 4. Nadia wins on a number "
                   "greater than 4. Is the game fair?", "No, Wei is more likely to win",
                   ["Yes, 4 is in the middle", "No, Nadia is more likely to win", "Yes, they both have 4 in the rule"],
                   "Less than 4: 1, 2, 3 (" + fr(3, 6) + "). Greater than 4: 5, 6 (" + fr(2, 6) + "). "
                   "<b>Wei is more likely to win.</b> 4 is not the middle of 1 to 6."))
    its.append(mcq("A bag has 4 red and 2 blue marbles. Nadia wins on red and Owen wins on blue. How many blue "
                   "marbles must be added to make the game fair?", "2", ["4", "6", "1"],
                   "For a fair game there must be as many blue as red: 4 blue. 4 − 2 = <b>2</b> more blue marbles. "
                   "4 is how many blue there should be in total, not how many to add.", ans=2))
    assert F(4, 8) == F(2 + 2, 8)
    its.append(mcq("Ryan and Kai play with 10 cards. Ryan wins on a red card and Kai wins on a black card. "
                   "6 cards are red and 4 are black. How many red cards must be changed to black to make the game fair?",
                   "1", ["2", "4", "5"],
                   "A fair game needs 5 red and 5 black. Change <b>1</b> red card: then there are 5 red and 5 black. "
                   "2 is the difference 6 − 4, but changing one card takes one from red AND adds one to black.", ans=1))
    assert (6 - 1, 4 + 1) == (5, 5)
    A = [("red", F(1, 4), "red"), ("blue", F(3, 4), "blue")]
    B = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("blue", F(1, 4), "blue")]
    C = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 8), "red"), ("blue", F(1, 8), "blue")]
    D = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("red", F(1, 3), "red")]
    fair = [part(x, "red") == part(x, "blue") for x in (A, B, C, D)]
    assert fair == [False, True, False, False] and part(C, "red") == F(5, 8)
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D], label="four spinners for a red and blue game")) +
                         "Sofia wins on red and Liam wins on blue. Which spinner makes the game fair?",
                         ["A", "B", "C", "D"], 1,
                         "On spinner <b>B</b> red and blue each cover 2 of 4 equal sections: " + fr(2, 4) + " each. "
                         "Spinner C also has 2 red and 2 blue sections, but they are not the same size: red is "
                         + fr(5, 8) + "."))
    its.append(mcq("At the school fun fair, a spinner has 8 equal sections and 1 of them wins a prize. 40 students "
                   "spin once each. About how many students should win a prize?", "about 5",
                   ["about 1", "about 8", "about 35"],
                   "P(prize) = " + fr(1, 8) + ". 40 ÷ 8 = 5, so <b>about 5</b> students. About 35 is the number who "
                   "should NOT win."))
    assert F(1, 8) * 40 == 5
    its.append(mcq("Arjun needs to land on green to win. Spinner A has 4 equal sections and 1 is green. Spinner B has "
                   "8 equal sections and 3 are green. Which spinner should he choose?", "Spinner B",
                   ["Spinner A, its green section is bigger", "They are the same", "You can’t tell"],
                   "Spinner A: " + fr(1, 4) + " = " + fr(2, 8) + ". Spinner B: " + fr(3, 8) + ". " + fr(3, 8) + " &gt; "
                   + fr(2, 8) + ", so <b>Spinner B</b> gives a better chance."))
    assert F(3, 8) > F(1, 4)
    its.append(mcq("At the school fun fair, Box A has 10 tickets and 3 of them win. Box B has 5 tickets and 2 of them win. "
                   "Which box gives a better chance of winning?", "Box B",
                   ["Box A, it has more winning tickets", "They are the same", "You can’t tell"],
                   "Box A: " + fr(3, 10) + ". Box B: " + fr(2, 5) + " = " + fr(4, 10) + ". " + fr(4, 10) + " &gt; "
                   + fr(3, 10) + ", so <b>Box B</b> is better, even though Box A has more winning tickets."))
    assert F(2, 5) > F(3, 10)
    its.append(mcq("Bag A has 3 red and 1 blue marble. Bag B has 5 red and 5 blue marbles. You win on red. "
                   "Which bag should you choose?", "Bag A", ["Bag B, it has more red marbles", "They are the same",
                                                             "You can’t tell"],
                   "Bag A: " + fr(3, 4) + ". Bag B: " + fr(5, 10) + " = " + fr(1, 2) + ". " + fr(3, 4) + " is more than "
                   + fr(1, 2) + ", so <b>Bag A</b> is better, even though Bag B has more red marbles."))
    assert F(3, 4) > F(5, 10)
    its.append(mcq("Game A: you win if a spinner with 3 equal sections lands on red. Game B: you win if a number cube "
                   "shows 5 or 6. Which game gives a better chance of winning?", "They are the same",
                   ["Game A", "Game B, it has 2 winning numbers", "You can’t tell"],
                   "Game A: " + fr(1, 3) + ". Game B: " + fr(2, 6) + " = " + fr(1, 3) + ". "
                   "<b>The chances are the same.</b>"))
    assert F(1, 3) == F(2, 6)
    its.append(mcq("Ji-woo wins on heads and Nadia wins on tails. After 20 tosses, Ji-woo has won 13 times. Nadia says "
                   "the game is not fair. Is she right?", "No, heads and tails are each " + fr(1, 2) + "; 20 tosses can vary",
                   ["Yes, Ji-woo won more", "Yes, the coin likes heads", "No, Nadia will win the next 6 tosses"],
                   "The coin gives each player " + fr(1, 2) + ", so the game is fair. With only 20 tosses, results like "
                   "13 and 7 can happen. <b>The game is still fair.</b> The coin does not “owe” Nadia any wins."))
    its.append(mcq("A bag has 3 red, 3 blue and 2 green marbles. Wei wins on red, Mei wins on blue and Kai wins on green. "
                   "Which change makes the game fair?", "Add 1 green marble",
                   ["Add 2 green marbles", "Take away 1 green marble", "Add 1 red and 1 blue marble"],
                   "For a fair game each colour needs the same number of marbles. With <b>1 more green</b>, there are "
                   "3 red, 3 blue and 3 green: " + fr(3, 9) + " each. Adding 2 green would give Kai 4 marbles."))
    assert F(3, 9) == F(3, 3 + 3 + 3)
    its.append(mcq("For the Terry Fox Run, Ms. Gill’s class makes 12 job cards, and 3 of them say “hand out water”. "
                   "Each student picks a card and puts it back. If 24 students pick, about how many should get "
                   "“hand out water”?", "about 6", ["about 3", "about 8", "about 12"],
                   "P(hand out water) = " + fr(3, 12) + " = " + fr(1, 4) + ". " + fr(1, 4) + " of 24 is 24 ÷ 4 = "
                   "<b>about 6</b>. About 3 is the number of cards. About 8 comes from 24 ÷ 3."))
    assert F(3, 12) * 24 == 6
    its = reorder(its, [0, 1, 2, 3, 4, 5, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
    return {"title": "Fair games: word problems", "items": its}


# ============================================================ lesson
def body_html():
    line = scale_svg(4, [], [(F(0), 0, 1), (F(1, 4), 1, 4), (F(1, 2), 1, 2), (F(3, 4), 3, 4), (F(1), 1, 1)],
                     words=True, label="probability line from impossible to certain")
    bag = bag_svg([("red", 3), ("blue", 5)], label="bag of 3 red and 5 blue marbles")
    sp = spinner_svg([("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")],
                     label="spinner half red quarter blue quarter yellow")
    return (
        "<h2>Outcomes</h2>"
        "<p>An <b>outcome</b> is one result that can happen. Rolling a number cube has 6 outcomes: 1, 2, 3, 4, 5 and 6. "
        "Each roll is one <b>trial</b>. An <b>event</b> is a group of outcomes, like “roll an even number” (2, 4, 6).</p>"
        + ex("Example 1", "Which outcomes make the event “roll a number less than 3”?",
             "Less than 3 means smaller than 3. The 3 itself does not count.", "1 and 2")
        + "<h2>Likelihood words</h2>"
        "<p>We describe how likely an event is with five words: impossible, unlikely, equally likely, likely and certain. "
        "As numbers, they go from <b>0</b> (impossible) to <b>1</b> (certain).</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>Likely is not certain. Unlikely is not impossible.</figcaption></figure>"
        + "<h2>Probability as a fraction</h2>"
        "<p>When the outcomes are equally likely:</p>"
        "<p><b>probability = number of outcomes you want ÷ total number of outcomes</b></p>"
        "<figure class='sn-fig'>" + bag +
        "<figcaption>3 red and 5 blue marbles: 8 marbles in total.</figcaption></figure>"
        + ex("Example 2", "What is the probability of taking a red marble from this bag?",
             "There are 3 red marbles and 8 marbles altogether. Compare with all 8, not with the 5 blue.",
             fr(3, 8) + ", which is less than " + fr(1, 2) + ", so red is unlikely")
        + "<h2>Spinners: look at the size of the parts</h2>"
        "<figure class='sn-fig'>" + sp +
        "<figcaption>3 colours, but the parts are not the same size.</figcaption></figure>"
        + ex("Example 3", "What is the probability of landing on red?",
             "Red covers half of the spinner. Do not count colours: 3 colours does not mean " + fr(1, 3) + " each.",
             fr(1, 2))
        + "<h2>Predict, then compare</h2>"
        "<p>Use the probability to predict: a 6 has a probability of " + fr(1, 6) + ", so in 60 rolls expect "
        "about 60 ÷ 6 = 10 sixes. Then do the experiment and compare. Results are usually close to the prediction, "
        "but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + table(["Coin tosses", "Heads", "Fraction of heads"], [
            ["10", "7", fr(7, 10)],
            ["20", "9", fr(9, 20)],
            ["200", "104", fr(104, 200)],
        ])
        + "<h2>Fair games</h2>"
        "<p>A game is <b>fair</b> when every player has the same probability of winning. "
        "Win on even, lose on odd with a number cube: " + fr(3, 6) + " and " + fr(3, 6) + ", so it is fair.</p>"
        + ex("Example 4", "Liam wins on 1 or 2. Emma wins on 3, 4, 5 or 6. Is the game fair?",
             "Liam: " + fr(2, 6) + ". Emma: " + fr(4, 6) + ". The chances are not the same.", "No, Emma is more likely to win")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“Less than 3” on a number cube is 1, 2 and 3.", "List the outcomes carefully: only 1 and 2."],
            ["3 red, 5 blue, so P(red) = " + fr(3, 5) + ".", "Compare with ALL the outcomes: " + fr(3, 8) + "."],
            ["3 colours, so each colour is " + fr(1, 3) + ".", "Look at the size of each part of the spinner."],
            ["“5 tails in a row, so heads is due.”", "A coin has no memory. Heads is still " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about probability in BC?",
     "a": "The BC Grade 5 math curriculum lists probability experiments with single events or outcomes. Students list the outcomes, describe how likely an event is (impossible to certain), write the probability as a fraction, predict results and compare them with an experiment."},
    {"q": "What is the difference between an outcome and an event?",
     "a": "An outcome is one possible result, such as rolling a 4. An event is a group of outcomes, such as rolling an even number (2, 4 or 6)."},
    {"q": "How do you write a probability as a fraction?",
     "a": "Put the number of outcomes you want over the total number of equally likely outcomes. A bag with 3 red and 5 blue marbles gives a probability of 3/8 for red, not 3/5."},
    {"q": "What makes a game fair?",
     "a": "A game is fair when every player has the same probability of winning. Winning on heads or tails is fair (1/2 each), but winning on 1 or 2 against 3 to 6 on a number cube is not (2/6 and 4/6)."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (probability lines, rows of spinners, tables)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(55816)
    sets = [set_outcomes(), set_words(), set_fraction(), set_predict(), set_fair()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "probability-experiments", "sort": 16,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Probability Experiments",
        "seo_title": "Grade 5 Probability Experiments Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Probability experiments",
        "domain": "Data and probability",
        "standard_code": "Grade 5: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Probability experiments, single events or outcomes",
        "meta_desc": "Free Grade 5 math worksheets on probability experiments for the BC curriculum: outcomes and events, impossible to certain, probability as a fraction, spinners and bags, predicting and comparing with results, and fair games. 100 questions with an answer key.",
        "key_big": "Probability = the outcomes you want ÷ all the outcomes. It goes from 0 (impossible) to 1 (certain).",
        "key_sub": "List the outcomes carefully, and on a spinner look at the size of each part, not the number of colours. A game is fair when every player has the same chance.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(probability line|four spinners|frequency table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
