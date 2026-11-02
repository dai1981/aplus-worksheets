# -*- coding: utf-8 -*-
"""
British Columbia Grade 6 Math: Probability
(BC Mathematics Curriculum, Grade 6, Data and probability — single-outcome probability, both theoretical
and experimental)
  python3 tools/gen_cabc_math_g6_probability.py
Probability as a fraction, decimal and percent on a line from 0 to 1; theoretical probability with number cubes,
spinners, marbles and letter cards (one outcome at a time); experimental probability from results tables;
comparing theoretical and experimental probability (predictions, more trials, unfair spinners); fair games in
BC contexts.
Wrong answers come from real student mistakes, mostly counting outcomes wrongly: counting colours or sections
instead of section sizes, part-to-part instead of part-to-whole (3 red, 5 blue gives 3/5), counting the different
letters instead of the cards, including the boundary number ("greater than 4" with the 4), counting 1 as prime,
counting the number of players instead of the outcomes, probabilities greater than 1, reading 1/4 as 0.4,
and the gambler's fallacy (after 5 tails, heads is "due").
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Canadian English, metric units, SI number spacing (no-break space). HTML attributes use single quotes.
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-6")
UPDATED = "2026-11-02"
LINE = "#2b2b2b"
THIN = "#8a8a8a"
GREEN = "#006633"
HEAD = "#e6f2ea"
FONT = "Arial, Helvetica, sans-serif"
COL = {"red": "#f08a80", "blue": "#8db4ee", "yellow": "#f7dc6f", "green": "#8fd19e",
       "purple": "#c9aef0", "white": "#ffffff", "grey": "#e4e4e4"}
INIT = {"red": "R", "blue": "B", "yellow": "Y", "green": "G", "purple": "P", "white": "W"}
NUMFILL = ["#f7dc6f", "#8db4ee", "#8fd19e", "#f08a80", "#c9aef0", "#ffd3a6", "#bfe3ef", "#e4e4e4",
           "#f7dc6f", "#8db4ee"]
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
        s.append(text(X(F(1, 2)), ly + 50, "equally likely", 14, weight=400))
        s.append(text(W - 4, ly + 50, "certain", 14, anchor="end", weight=400))
        s.append(text(X(F(1, 4)), ly + 50, "unlikely", 14, weight=400))
        s.append(text(X(F(3, 4)), ly + 50, "likely", 14, weight=400))
        H = ly + 58
    return svg_wrap(W, H, "".join(s), label)


TENTHS = [(F(0), "0"), (F(1, 2), "0.5"), (F(1), "1")]
ENDS = [(F(0), "0"), (F(1), "1")]



def cards_svg(word, label="letter cards"):
    """A row of face-up letter cards, one letter on each card."""
    cw, ch, gap = 34, 44, 7
    n = len(word)
    W = n * cw + (n - 1) * gap + 8
    s = []
    for i, L in enumerate(word):
        x = 4 + i * (cw + gap)
        s.append("<rect x='%d' y='4' width='%d' height='%d' rx='4' fill='#ffffff' stroke='%s' stroke-width='2'/>"
                 % (x, cw, ch, LINE))
        s.append(text(x + cw / 2, 4 + ch / 2 + 7, L, 20))
    return svg_wrap(W, ch + 8, "".join(s), label)


CUBE6 = list(range(1, 7))


def P(want, space):
    """Theoretical probability: outcomes you want ÷ all outcomes (equally likely)."""
    return F(sum(1 for x in space if want(x)), len(space))


def is_prime(k):
    return k > 1 and all(k % d for d in range(2, k))


# ============================================================ set 1: fraction, decimal, percent
def set_fdp():
    its = []
    its.append(mcq("What is the probability of an event that is impossible?", "0", ["1", fr(1, 2), "0.1"],
                   "An impossible event can never happen, so its probability is <b>0</b>. 0.1 is very unlikely, "
                   "but it can still happen.", ans=0))
    its.append(mcq("What is the probability of an event that is certain?", "1", ["0", "100", fr(1, 2)],
                   "A certain event will happen, so its probability is <b>1</b> (or 100%). The number 100 on its own "
                   "is far bigger than 1, so it can’t be a probability.", ans=1))
    its.append(mcq("An event is equally likely to happen or not happen. What is its probability?", fr(1, 2),
                   ["2", "1", "0"],
                   "Equally likely is halfway between 0 and 1: <b>" + fr(1, 2) + "</b> (0.5 or 50%). "
                   "2 is the number of outcomes, not the probability.", ans=F(1, 2)))
    its.append(mcq("Which number can NOT be a probability?", "1.5", ["0.5", "0", "1"],
                   "Probabilities go from 0 to 1. <b>1.5</b> is bigger than 1, so it can’t be a probability. "
                   "0 and 1 are allowed: they mean impossible and certain."))
    its.append(mcq("Which percent can NOT be a probability?", "120%", ["12%", "0%", "100%"],
                   "As a percent, probabilities go from 0% to 100%. <b>120%</b> is more than 100%, so it is not possible."))
    its.append(mcq(fig(scale_svg(10, [(F(8, 10), "")], TENTHS, label="probability line arrow at 0.8")) +
                   "Which word best describes the chance shown by the arrow?", "likely",
                   ["unlikely", "certain", "equally likely"],
                   "The arrow is at 0.8. That is between 0.5 and 1, close to 1: <b>likely</b>. "
                   "It is not certain, because it is not at 1."))
    its.append(mcq("The probability of heads is " + fr(1, 2) + ". What is this as a decimal?", "0.5",
                   ["0.2", "1.2", "0.12"],
                   fr(1, 2) + " = 1 ÷ 2 = <b>0.5</b>. Writing the digits 1 and 2 as 0.12 or 1.2 is a common mistake.",
                   ans=F(1, 2)))
    its.append(mcq("The probability of landing on blue is " + fr(1, 4) + ". What is this as a percent?", "25%",
                   ["14%", "4%", "40%"],
                   fr(1, 4) + " = " + fr(25, 100) + " = <b>25%</b>. 14% just writes the digits 1 and 4.", ans=F(1, 4)))
    its.append(mcq("Write the probability " + fr(3, 10) + " as a decimal.", "0.3", ["0.03", "3.1", "0.13"],
                   fr(3, 10) + " is 3 tenths = <b>0.3</b>. 0.03 is 3 hundredths.", ans=F(3, 10)))
    its.append(mcq("Write the probability 0.75 as a percent.", "75%", ["7.5%", "0.75%", "25%"],
                   "To change a decimal to a percent, multiply by 100: 0.75 × 100 = <b>75%</b>. "
                   "25% is the chance that the event does NOT happen.", ans=F(3, 4)))
    its.append(mcq("Which fraction is equal to the probability 0.2?", fr(1, 5), [fr(1, 2), fr(2, 100), fr(1, 20)],
                   "0.2 = " + fr(2, 10) + " = <b>" + fr(1, 5) + "</b>. " + fr(1, 2) + " is 0.5, and "
                   + fr(2, 100) + " is 0.02.", ans=F(1, 5)))
    its.append(mcq("Write the probability " + fr(3, 5) + " as a percent.", "60%", ["35%", "30%", "53%"],
                   fr(3, 5) + " = " + fr(60, 100) + " = <b>60%</b>. Multiply the numerator and denominator by 20. "
                   "35% just writes the digits 3 and 5.", ans=F(3, 5)))
    its.append(mcq("Write the probability 40% as a fraction in lowest terms.", fr(2, 5), [fr(1, 4), fr(4, 100), fr(1, 40)],
                   "40% = " + fr(40, 100) + ". Divide the numerator and denominator by 20: <b>" + fr(2, 5) + "</b>. "
                   + fr(4, 100) + " would be 4%.", ans=F(2, 5)))
    its.append(mcq("Write the probability 0.05 as a percent.", "5%", ["50%", "0.05%", "0.5%"],
                   "0.05 × 100 = <b>5%</b>. 50% would be 0.5.", ans=F(5, 100)))
    its.append(mcq("Write the probability " + fr(1, 8) + " as a decimal.", "0.125", ["0.8", "0.18", "1.8"],
                   "1 ÷ 8 = <b>0.125</b> (125 thousandths). A quick check: " + fr(1, 4) + " = 0.25, and " + fr(1, 8) +
                   " is half of that.", ans=F(1, 8)))
    its.append(mcq("Write the probability " + fr(7, 20) + " as a percent.", "35%", ["7%", "27%", "72%"],
                   "Multiply the numerator and denominator by 5: " + fr(7, 20) + " = " + fr(35, 100) + " = <b>35%</b>. "
                   "27% comes from adding 7 + 20.", ans=F(7, 20)))
    its.append(mcq(fig(scale_svg(10, [(F(3, 10), "")], TENTHS, label="probability line arrow at 0.3")) +
                   "The line is split into tenths. What probability does the arrow show, as a percent?", "30%",
                   ["3%", "70%", "0.3%"],
                   "The arrow is 3 small steps from 0, at 0.3. 0.3 = 30 hundredths = <b>30%</b>. "
                   "70% counts back from 1. 3% would be 0.03.", ans=F(3, 10)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    assert part(sp, "blue") == F(1, 4) == F("0.25")
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "Which shows the probability of landing on blue as a fraction, a decimal and a percent?",
                   fr(1, 4) + ", 0.25, 25%",
                   [fr(1, 4) + ", 0.4, 40%", fr(1, 4) + ", 0.14, 14%", fr(1, 2) + ", 0.5, 50%"],
                   "Blue covers one quarter of the spinner: <b>" + fr(1, 4) + " = 0.25 = 25%</b>. "
                   + fr(1, 2) + " is the probability of red. " + fr(1, 4) + " is 0.25, not 0.4 or 0.14."))
    its.append(mcq("Which probability is the greatest?", fr(3, 4), ["0.7", "72%", "0.69"],
                   "Change them all to decimals: " + fr(3, 4) + " = 0.75, 0.7 = 0.70, 72% = 0.72, 0.69. "
                   "The greatest is <b>" + fr(3, 4) + "</b>.", ans=F(3, 4)))
    assert F(3, 4) > max(F("0.7"), F("0.72"), F("0.69"))
    its.append(mcq("The forecast for Vancouver says there is a 70% chance of rain tomorrow. "
                   "What is this probability as a decimal?", "0.7", ["0.07", "7.0", "0.3"],
                   "70% = " + fr(70, 100) + " = <b>0.7</b>. Divide by 100 to change a percent to a decimal. "
                   "0.3 is the chance of NO rain.", ans=F(7, 10)))
    return {"title": "Probability as a fraction, decimal and percent", "items": its}


# ============================================================ set 2: theoretical probability
def set_theory():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 4?", fr(1, 6),
                   [fr(1, 4), fr(4, 6), fr(1, 5)],
                   "There are 6 equally likely outcomes and only one of them is 4: <b>" + fr(1, 6) + "</b>. "
                   + fr(4, 6) + " would be the chance of 1, 2, 3 or 4.", ans=P(lambda k: k == 4, CUBE6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling an even number?",
                   fr(3, 6), [fr(1, 6), fr(2, 6), fr(6, 3)],
                   "The even numbers are 2, 4 and 6: 3 of the 6 outcomes, so <b>" + fr(3, 6) + "</b> (= " + fr(1, 2) + "). "
                   + fr(6, 3) + " is upside down: it is greater than 1.", ans=P(lambda k: k % 2 == 0, CUBE6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
                   "greater than 4?", fr(2, 6), [fr(3, 6), fr(4, 6), fr(1, 6)],
                   "Greater than 4 means 5 or 6: 2 of the 6 outcomes, so <b>" + fr(2, 6) + "</b>. "
                   + fr(3, 6) + " wrongly includes the 4. " + fr(1, 6) + " forgets the 5.", ans=P(lambda k: k > 4, CUBE6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
                   "less than 5?", fr(4, 6), [fr(5, 6), fr(2, 6), fr(4, 5)],
                   "Less than 5 means 1, 2, 3 or 4: 4 of the 6 outcomes, so <b>" + fr(4, 6) + "</b>. "
                   + fr(5, 6) + " wrongly includes the 5. " + fr(2, 6) + " counts the outcomes you don’t want (5 and 6).",
                   ans=P(lambda k: k < 5, CUBE6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a multiple of 3?",
                   fr(2, 6), [fr(3, 6), fr(1, 6), fr(4, 6)],
                   "The multiples of 3 on the cube are 3 and 6: <b>" + fr(2, 6) + "</b>. " + fr(3, 6) +
                   " also counts 9, which is not on the cube. " + fr(1, 6) + " forgets the 6.",
                   ans=P(lambda k: k % 3 == 0, CUBE6)))
    assert [k for k in CUBE6 if is_prime(k)] == [2, 3, 5]
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a prime number?",
                   fr(3, 6), [fr(4, 6), fr(2, 6), fr(1, 6)],
                   "The prime numbers are 2, 3 and 5: <b>" + fr(3, 6) + "</b>. " + fr(4, 6) +
                   " wrongly counts 1, which is not prime. " + fr(2, 6) + " forgets that 2 is prime.",
                   ans=P(is_prime, CUBE6)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of NOT rolling a 6?",
                   fr(5, 6), [fr(1, 6), fr(6, 5), fr(1, 5)],
                   "Not a 6 means 1, 2, 3, 4 or 5: <b>" + fr(5, 6) + "</b>. Check: " + fr(5, 6) + " + " + fr(1, 6) +
                   " = 1. " + fr(6, 5) + " is upside down and greater than 1.", ans=P(lambda k: k != 6, CUBE6)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red half")) + "What is the probability of landing on red?",
                   fr(1, 2), [fr(1, 3), fr(1, 4), fr(2, 3)],
                   "Red covers half of the spinner: <b>" + fr(1, 2) + "</b>. " + fr(1, 3) +
                   " counts the 3 colours, but the sections are not the same size.", ans=part(sp, "red")))
    sp = [("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"),
          ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight sections three green")) +
                   "The spinner has 8 equal sections: G is green and Y is yellow. What is the probability of green?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 8)],
                   "3 of the 8 equal sections are green: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares green with yellow, not with all 8 sections. " + fr(5, 8) + " is yellow.",
                   ans=part(sp, "G")))
    its.append(mcq("A spinner has 10 equal sections: 3 blue and 7 red. What is the probability of blue as a decimal?",
                   "0.3", ["0.03", "0.7", "0.37"],
                   "3 of the 10 sections are blue: " + fr(3, 10) + " = <b>0.3</b>. 0.7 is the probability of red.",
                   ans=F(3, 10)))
    s8 = [(str(k), F(1, 8), NUMFILL[k - 1]) for k in range(1, 9)]
    its.append(mcq(fig(spinner_svg(s8, label="spinner 1 to 8")) + "What is the probability of landing on a prime number?",
                   fr(4, 8), [fr(3, 8), fr(5, 8), fr(1, 8)],
                   "The prime numbers are 2, 3, 5 and 7: 4 of the 8 sections, so <b>" + fr(4, 8) + "</b> (= " + fr(1, 2) + "). "
                   + fr(5, 8) + " wrongly counts 1, which is not prime. " + fr(3, 8) + " forgets 2.",
                   ans=P(is_prime, range(1, 9))))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("red", F(1, 8), "red"),
          ("blue", F(1, 4), "blue")]
    assert part(sp, "red") == F(1, 4) and len(sp) == 5
    its.append(mcq(fig(spinner_svg(sp, label="spinner red in two small parts")) +
                   "Red is in two small parts, each one eighth of the spinner. What is the probability of red?",
                   fr(1, 4), [fr(1, 8), fr(1, 3), fr(2, 5)],
                   fr(1, 8) + " + " + fr(1, 8) + " = " + fr(2, 8) + " = <b>" + fr(1, 4) + "</b>. "
                   + fr(2, 5) + " counts 2 of the 5 sections, but the sections are not the same size.", ans=F(1, 4)))
    A = [("red", F(1, 4), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    B = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
    C = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green"),
         ("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    D = [("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("blue", F(1, 4), "blue")]
    assert [part(x, "blue") for x in (A, B, C, D)] == [F(1, 2), F(1, 3), F(1, 4), F(3, 4)]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "On which spinner is the probability of blue " + fr(1, 4) + "?",
                         ["A", "B", "C", "D"], 2,
                         "On spinner <b>C</b>, blue has 2 of the 8 equal sections: " + fr(2, 8) + " = " + fr(1, 4) + ". "
                         "A has 4 colours, but blue is half of it. B is " + fr(1, 3) + " and D is " + fr(3, 4) + "."))
    s10 = [(str(k), F(1, 10), NUMFILL[k - 1]) for k in range(1, 11)]
    assert P(lambda k: k % 4 == 0, range(1, 11)) == F(20, 100)
    its.append(mcq(fig(spinner_svg(s10, label="spinner 1 to 10")) +
                   "What is the probability of landing on a multiple of 4, as a percent?", "20%", ["2%", "40%", "25%"],
                   "The multiples of 4 are 4 and 8: " + fr(2, 10) + " = " + fr(20, 100) + " = <b>20%</b>. "
                   "2% uses the count as the percent. 40% counts every number up to 4. 25% comes from thinking “4 means "
                   + fr(1, 4) + "”.", ans=F(1, 5)))
    assert P(lambda k: k > 9, range(1, 13)) == F(3, 12)
    its.append(mcq("A 12-sided die has the numbers 1 to 12. What is the probability of rolling a number greater than 9?",
                   fr(3, 12), [fr(4, 12), fr(1, 12), fr(9, 12)],
                   "Greater than 9 means 10, 11 or 12: <b>" + fr(3, 12) + "</b> (= " + fr(1, 4) + "). " + fr(4, 12) +
                   " wrongly includes the 9. " + fr(9, 12) + " is the chance of 1 to 9, the numbers you don’t want.",
                   ans=F(1, 4)))
    sp = [("red", F(1, 5), "red"), ("red", F(1, 5), "red"), ("blue", F(1, 5), "blue"), ("red", F(1, 5), "red"),
          ("green", F(1, 5), "green")]
    assert part(sp, "red") == F(3, 5)
    its.append(mcq(fig(spinner_svg(sp, label="spinner five equal sections three red")) +
                   "The spinner has 5 equal sections. What is the probability of red, as a decimal?", "0.6",
                   ["0.3", "0.35", "1.5"],
                   "3 of the 5 equal sections are red: " + fr(3, 5) + " = " + fr(6, 10) + " = <b>0.6</b>. "
                   "0.35 just writes the digits 3 and 5. 1.5 compares red with not red (3 ÷ 2).", ans=part(sp, "red")))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")]
    assert part(sp, "yellow") == F(1, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner red half blue quarter yellow and green eighths")) +
                   "Simran says the probability of yellow is " + fr(1, 4) + " because there are 4 colours. "
                   "What is the probability of yellow?", fr(1, 8), [fr(1, 4), fr(1, 3), fr(1, 2)],
                   "The colours are not the same size. Yellow is half of a quarter: <b>" + fr(1, 8) + "</b>. "
                   "Counting colours only works when every section is the same size.", ans=F(1, 8)))
    faces = [1, 1, 2, 2, 2, 3]
    assert P(lambda k: k == 2, faces) == F(3, 6)
    its.append(mcq("A special number cube has the faces 1, 1, 2, 2, 2 and 3. What is the probability of rolling a 2?",
                   fr(3, 6), [fr(1, 3), fr(1, 6), fr(3, 3)],
                   "The cube has 6 faces and 3 of them show a 2: <b>" + fr(3, 6) + "</b> (= " + fr(1, 2) + "). "
                   + fr(1, 3) +  " counts the 3 different numbers, but they are not on the same number of faces. " + fr(3, 3) +
                   " compares the faces with a 2 with the other 3 faces.",
                   ans=F(1, 2)))
    word = "OKANAGAN"
    assert word.count("A") == 3 and len(word) == 8 and len(set(word)) == 5
    its.append(mcq(fig(cards_svg(word, label="letter cards OKANAGAN")) +
                   "Each letter of OKANAGAN is on a card. The cards are mixed up and turned over. "
                   "You pick one card. What is the probability of A?",
                   fr(3, 8), [fr(1, 8), fr(1, 5), fr(3, 5)],
                   "There are 8 cards and 3 of them show A: <b>" + fr(3, 8) + "</b>. " + fr(1, 5) +
                   " counts the 5 different letters (O, K, A, N, G), but A is on 3 cards. " + fr(3, 5) +
                   " compares the A cards with the other 5 cards.", ans=F(word.count("A"), len(word))))
    n = P(lambda k: k % 2 == 0 and k > 3, range(1, 9))
    assert n == F(3, 8)
    its.append(mcq(fig(spinner_svg(s8, label="spinner 1 to 8 again")) +
                   "What is the probability of landing on an even number that is greater than 3?",
                   fr(3, 8), [fr(4, 8), fr(2, 8), fr(5, 8)],
                   "Even and greater than 3: 4, 6 and 8. That is <b>" + fr(3, 8) + "</b>. " + fr(4, 8) +
                   " counts every even number, with 2. " + fr(2, 8) + " forgets the 8. " + fr(5, 8) +
                   " counts every number greater than 3.", ans=n))
    return {"title": "Theoretical probability: number cubes and spinners", "items": its}


# ============================================================ set 3: experimental probability
def set_experimental():
    its = []
    its.append(mcq("Ryan tosses a coin 50 times and gets 23 heads. What is the experimental probability of heads?",
                   fr(23, 50), [fr(23, 27), fr(1, 2), fr(27, 50)],
                   "Experimental probability = number of times it happened ÷ number of trials = <b>" + fr(23, 50) +
                   "</b>. " + fr(1, 2) + " is the theoretical probability. " + fr(23, 27) + " compares heads with tails.",
                   ans=F(23, 50)))
    its.append(mcq("Which sentence describes experimental probability?",
                   "The number of times it happened ÷ the number of trials",
                   ["The outcomes you want ÷ all the possible outcomes", "The number of times it happened",
                    "The number of trials ÷ the number of times it happened"],
                   "Experimental probability comes from what <b>happened</b> in an experiment: "
                   "<b>times it happened ÷ number of trials</b>. Counting the possible outcomes gives the theoretical "
                   "probability."))
    its.append(mcq(fig(freq_svg("20 spins", "Colour", ["red", "blue"], [12, 8], tally=False,
                                label="frequency table 20 spins")) +
                   "Nadia’s class recorded 20 spins. What is the experimental probability of red, as a decimal?", "0.6",
                   ["0.12", "1.5", "0.4"],
                   "Red came up 12 times in 20 spins: " + fr(12, 20) + " = " + fr(6, 10) + " = <b>0.6</b>. "
                   "1.5 comes from 12 ÷ 8 (red ÷ blue), and it is greater than 1.", ans=F(12, 20)))
    vals = [18, 12, 10]
    assert sum(vals) == 40
    its.append(mcq(fig(freq_svg("40 spins", "Colour", ["red", "blue", "yellow"], vals, tally=False,
                                label="frequency table 40 spins")) +
                   "What is the experimental probability of yellow, as a percent?", "25%", ["10%", "40%", "30%"],
                   "Yellow came up 10 times in 40 spins: " + fr(10, 40) + " = " + fr(1, 4) + " = <b>25%</b>. "
                   "10% uses the count as the percent. 30% is blue.", ans=F(10, 40)))
    vals = [4, 6, 7, 3, 5, 5]
    assert sum(vals) == 30
    its.append(mcq(fig(freq_svg("A number cube rolled 30 times", "Number", ["1", "2", "3", "4", "5", "6"], vals,
                                tally=True, label="frequency table tally number cube 30 rolls")) +
                   "What is the experimental probability of rolling a 4?", fr(3, 30), [fr(1, 6), fr(3, 27), fr(4, 30)],
                   "The tally for 4 shows 3 rolls out of 30: <b>" + fr(3, 30) + "</b>. " + fr(1, 6) +
                   " is the theoretical probability. " + fr(4, 30) + " uses the number 4 instead of its frequency.",
                   ans=F(3, 30)))
    its.append(mcq("At hockey practice, Harjot scored on 8 of his 25 shots. What is his experimental probability of "
                   "scoring, as a percent?", "32%", ["8%", "25%", "68%"],
                   fr(8, 25) + " = " + fr(32, 100) + " = <b>32%</b> (multiply the numerator and denominator by 4). "
                   "8% uses the count as the percent. 68% is the shots he missed.", ans=F(8, 25)))
    its.append(mcq("Ethan counts 40 cars passing the school in Burnaby. 14 of them are white. Estimate the probability "
                   "that the next car is white.", "0.35", ["0.14", "0.65", "0.4"],
                   "14 ÷ 40 = " + fr(35, 100) + " = <b>0.35</b>. 0.14 uses the count as the decimal. "
                   "0.65 is the estimate for a car that is NOT white.", ans=F(14, 40)))
    its.append(mcq("In Vancouver last November, it rained on 21 of the 30 days. What is the experimental probability "
                   "of rain on a November day, as a decimal?", "0.7", ["0.21", "0.3", "2.1"],
                   fr(21, 30) + " = " + fr(7, 10) + " = <b>0.7</b>. 0.21 uses the count as the decimal. "
                   "0.3 is the dry days.", ans=F(21, 30)))
    vals = [22, 18, 10]
    assert sum(vals) == 50
    its.append(mcq(fig(freq_svg("50 draws", "Colour", ["red", "blue", "green"], vals, tally=False,
                                label="frequency table 50 draws")) +
                   "Kai takes a marble from a bag, records its colour and puts it back. He does this 50 times. "
                   "What is the experimental probability of NOT red?", fr(28, 50), [fr(22, 50), fr(28, 22), fr(10, 50)],
                   "Not red means blue or green: 18 + 10 = 28 of the 50 draws, so <b>" + fr(28, 50) + "</b>. "
                   + fr(22, 50) + " is red. " + fr(10, 50) + " counts only green.", ans=F(28, 50)))
    its.append(mcq("Owen flips a bottle cap 80 times. It lands top-up 36 times. What is the experimental probability "
                   "of top-up, as a percent?", "45%", ["36%", "44%", "55%"],
                   fr(36, 80) + " = " + fr(9, 20) + " = " + fr(45, 100) + " = <b>45%</b>. 36% uses the count as the "
                   "percent. 55% is top-down. 44% comes from 80 − 36.", ans=F(36, 80)))
    its.append(mcq("Chloe spins a spinner 25 times and gets green 9 times. What is the experimental probability of "
                   "green, as a decimal?", "0.36", ["0.09", "0.9", "0.64"],
                   fr(9, 25) + " = " + fr(36, 100) + " = <b>0.36</b>. 0.09 and 0.9 just use the 9. "
                   "0.64 is the probability of NOT green.", ans=F(9, 25)))
    its.append(mcq("Leah takes 15 penalty kicks at soccer practice and scores 6 times. What is her experimental "
                   "probability of scoring, as a decimal?", "0.4", ["0.6", "0.15", "0.06"],
                   fr(6, 15) + " = " + fr(2, 5) + " = <b>0.4</b>. 0.6 is the kicks she missed. "
                   "0.06 uses the count as the decimal.", ans=F(6, 15)))
    vals = [7, 11, 4, 8]
    assert sum(vals) == 30
    its.append(mcq(fig(freq_svg("30 spins", "Colour", ["red", "blue", "yellow", "green"], vals, tally=True,
                                label="frequency table tally 30 spins")) +
                   "What is the experimental probability of blue or green?", fr(19, 30), [fr(11, 30), fr(8, 30), fr(2, 4)],
                   "Blue or green: 11 + 8 = 19 of the 30 spins, so <b>" + fr(19, 30) + "</b>. " + fr(2, 4) +
                   " counts 2 of the 4 colours, but experimental probability uses the results.", ans=F(19, 30)))
    its.append(mcq("Zara’s school bus in Kelowna was late on 4 of the 20 school days in February. "
                   "What is the experimental probability that the bus is late, in lowest terms?", fr(1, 5),
                   [fr(1, 4), fr(4, 5), fr(1, 20)],
                   fr(4, 20) + " = <b>" + fr(1, 5) + "</b>. " + fr(1, 4) + " compares the 4 late days with the "
                   "16 on-time days. " + fr(4, 5) + " is the chance it is on time.", ans=F(4, 20)))
    its.append(mcq("Jasleen spins a spinner and gets red 12 times. Her experimental probability of red is " + fr(3, 10) + ". "
                   "How many times did she spin?", "40", ["12", "30", "36"],
                   fr(3, 10) + " = " + fr(12, 40) + ", so she spun <b>40</b> times. 36 comes from 12 × 3. "
                   "30 comes from 3 × 10.", ans=40))
    assert F(12, 40) == F(3, 10)
    its.append(mcq("After 40 coin tosses, Wei’s experimental probability of heads is 0.45. How many heads did he get?",
                   "18", ["45", "22", "20"],
                   "0.45 × 40 = <b>18</b>. Check: " + fr(18, 40) + " = " + fr(45, 100) + " = 0.45. "
                   "20 is half of 40 (the theory). 22 is the number of tails.", ans=18))
    assert F("0.45") * 40 == 18
    assert F(130, 200) == F(65, 100)
    its.append(mcq("On a field trip to a salmon hatchery, students count 200 young salmon. 130 of them are coho. "
                   "Estimate the probability that the next salmon counted is coho, as a percent.", "65%",
                   ["130%", "35%", "13%"],
                   fr(130, 200) + " = " + fr(65, 100) + " = <b>65%</b>. 130% is more than 100%, so it can’t be a "
                   "probability. 35% is NOT coho.", ans=F(130, 200)))
    its.append(mcq("A bag has 20 marbles. Sofia takes one, records its colour and puts it back. She does this 100 times "
                   "and gets red 26 times. About how many red marbles are in the bag?", "about 5",
                   ["about 26", "about 10", "about 15"],
                   "Red came up " + fr(26, 100) + " = 0.26 of the time, about a quarter. " + fr(1, 4) +
                   " of 20 is 5, so there are <b>about 5</b> red marbles. 26 is more than the whole bag."))
    assert round(F(26, 100) * 20) == 5
    its.append(mcq("Three groups spin the same spinner 20 times each. Red comes up 9, 13 and 8 times. "
                   "Use all the results to estimate the probability of red.", fr(30, 60),
                   [fr(9, 20), fr(13, 20), fr(30, 20)],
                   "Add the results: 9 + 13 + 8 = 30 reds in 3 × 20 = 60 spins. <b>" + fr(30, 60) + "</b> (= " + fr(1, 2) +
                   "). Using all 60 spins gives a better estimate than one group. " + fr(30, 20) + " is greater than 1.",
                   ans=F(1, 2)))
    assert 9 + 13 + 8 == 30
    shots = {"Lucas": (7, 10), "Noah": (12, 20), "Ava": (15, 30), "Zara": (18, 40)}
    best = max(shots, key=lambda k: F(*shots[k]))
    assert best == "Lucas"
    its.append(mcq("Four friends practise basketball shots. Noah: 12 baskets in 20 shots. Ava: 15 in 30. "
                   "Lucas: 7 in 10. Zara: 18 in 40. Who has the greatest experimental probability of scoring?",
                   "Lucas", ["Zara", "Noah", "Ava"],
                   "Noah " + fr(12, 20) + " = 0.6, Ava " + fr(15, 30) + " = 0.5, Lucas " + fr(7, 10) + " = 0.7, Zara "
                   + fr(18, 40) + " = 0.45. <b>Lucas</b> is greatest. Zara made the most baskets, but she also took "
                   "the most shots."))
    return {"title": "Experimental probability from results", "items": its}


# ============================================================ set 4: compare theoretical and experimental
def set_compare():
    its = []
    its.append(mcq("Liam rolls a number cube 60 times. About how many times would he expect to roll a 6?", "about 10",
                   ["about 6", "about 1", "about 30"],
                   "A 6 has a theoretical probability of " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10, "
                   "so <b>about 10</b>."))
    assert F(1, 6) * 60 == 10
    its.append(mcq("Emma tosses a coin 100 times. How many heads should she expect?", "about 50",
                   ["exactly 50", "about 100", "about 2"],
                   "Half of 100 is 50. Results change from one experiment to the next, so expect <b>about 50</b>, "
                   "not exactly 50."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red")) +
                   "Lucas spins this spinner 40 times. About how many times should he expect red?", "about 30",
                   ["about 10", "about 3", "about 40"],
                   "Red is " + fr(3, 4) + " of the spinner. 40 ÷ 4 = 10, and 3 × 10 = 30, so <b>about 30</b>. "
                   "About 10 is for blue."))
    assert part(sp, "red") * 40 == 30
    assert F(13, 40) > F(1, 4)
    its.append(mcq("A spinner has 4 equal sections, and one is blue. Olivia spins it 40 times and gets blue 13 times. "
                   "How does the experimental probability of blue compare with the theoretical probability?",
                   fr(13, 40) + " is a little greater than " + fr(1, 4),
                   [fr(13, 40) + " is less than " + fr(1, 4), fr(13, 27) + " is much greater than " + fr(1, 4),
                    "They are exactly equal"],
                   "Experimental: " + fr(13, 40) + " = 0.325. Theoretical: " + fr(1, 4) + " = 0.25. So <b>" + fr(13, 40) +
                   " is a little greater than " + fr(1, 4) + "</b>. " + fr(13, 27) + " compares blue with not blue."))
    its.append(mcq("Ava tosses a coin 10 times and gets 7 heads. Noah tosses a coin 1000 times and gets 508 heads. "
                   "Whose experimental probability of heads is closer to " + fr(1, 2) + "?",
                   "Noah’s", ["Ava’s", "They are equally close", "Neither is close"],
                   "Ava: " + fr(7, 10) + " = 0.7. Noah: " + fr(508, 1000) + " = 0.508. 0.508 is much closer to 0.5, "
                   "so <b>Noah’s</b> is closer."))
    assert abs(F(508, 1000) - F(1, 2)) < abs(F(7, 10) - F(1, 2))
    its.append(mcq("Why are Noah’s results (1000 tosses) closer to " + fr(1, 2) + " than Ava’s (10 tosses)?",
                   "More trials usually get closer to the theory",
                   ["Noah tossed the coin more carefully", "Ava’s coin must be unfair",
                    "Big experiments are always exactly right"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the theoretical probability, but not exactly."))
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A number cube rolled 60 times", "Number", ["1", "2", "3", "4", "5", "6"], vals,
                                tally=False, label="frequency table number cube 60 rolls")) +
                   "How do these results compare with the theory?",
                   "Close: each number should come up about 10 times",
                   ["The number cube must be unfair", "5 is the most likely number", "4 will come up more next time"],
                   "Theory: " + fr(1, 6) + " of 60 = 10 for each number. The results are all between 8 and 12, which is "
                   "<b>close to the theory</b>. Small differences are normal."))
    its.append(mcq("Leah rolls a number cube 600 times and gets a 6 on 104 rolls. How does this compare with the theory?",
                   "Close: theory says about 100", ["Far off: theory says about 6", "Far off: theory says about 300",
                                                    "Exactly right: theory says 104"],
                   fr(1, 6) + " of 600 = 600 ÷ 6 = 100. 104 is <b>close to 100</b>. Experiments are rarely exactly "
                   "the same as the theory."))
    assert F(600, 6) == 100
    its.append(mcq("A computer simulates tossing a coin 10" + NB + "000 times. About how many heads would you expect?",
                   "about 5000", ["exactly 5000", "about 1000", "about 50"],
                   "Half of 10" + NB + "000 is 5000. A simulation with many trials gets close to the theory, so expect "
                   "<b>about 5000</b>, not exactly 5000."))
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. At a school fun fair in Surrey, "
                   "red comes up 98 times in 200 spins. What do the results suggest?",
                   "The spinner is probably not fair",
                   ["The spinner is fair", "Red will stop coming up soon", "200 spins are too few to tell"],
                   "Theory: " + fr(1, 4) + " of 200 = 50 reds. 98 is almost double that, after many spins, so "
                   "<b>the spinner is probably not fair</b>."))
    assert F(1, 4) * 200 == 50
    d = F(33, 50) - F(1, 2)
    assert d == F(16, 100)
    its.append(mcq("Hana rolls a number cube 50 times and gets an even number 33 times. How much greater is the "
                   "experimental probability of an even number than the theoretical probability, as a decimal?",
                   "0.16", ["0.66", "0.17", "0.33"],
                   "Experimental: " + fr(33, 50) + " = 0.66. Theoretical: " + fr(3, 6) + " = 0.5. "
                   "0.66 − 0.5 = <b>0.16</b>. 0.17 comes from 50 − 33 = 17.", ans=d))
    its.append(mcq("Before each lacrosse game, a coin is tossed to decide which team starts. Tails has come up "
                   "5 games in a row. What is the probability of heads at the next game?",
                   fr(1, 2), [fr(5, 6), fr(1, 6), "1"],
                   "The coin has no memory. Every toss is a new trial, so heads is still <b>" + fr(1, 2) + "</b>. "
                   "Thinking heads is “due” is called the gambler’s fallacy.", ans=F(1, 2)))
    its.append(mcq("Kai has rolled a number cube 12 times without getting a 6. What is the probability of a 6 "
                   "on the next roll?", fr(1, 6), ["1", fr(2, 6), fr(1, 12)],
                   "The number cube does not remember earlier rolls. A 6 is still <b>" + fr(1, 6) + "</b>. "
                   "It is not certain (1), even after a long wait.", ans=F(1, 6)))
    its.append(mcq("Ji-woo spins a spinner with 5 equal sections, each a different colour, 50 times. In theory, "
                   "about how many times should each colour come up?", "about 10",
                   ["about 5", "about 45", "about 25"],
                   "Each colour has a probability of " + fr(1, 5) + ". " + fr(1, 5) + " of 50 is 50 ÷ 5 = <b>10</b>. "
                   "About 5 confuses the 5 sections with the answer."))
    assert F(1, 5) * 50 == 10
    groups = {"Group A": 19, "Group B": 30, "Group C": 12, "Group D": 40}
    assert min(groups, key=lambda g: abs(groups[g] - 20)) == "Group A"
    its.append(mcq("Four groups each spin a spinner with 4 equal sections 80 times. They get red 19, 30, 12 and "
                   "40 times (Groups A, B, C and D). Whose result is closest to the theory?", "Group A",
                   ["Group B", "Group C", "Group D"],
                   "Theory: " + fr(1, 4) + " of 80 = 20 reds. Group A’s 19 is only 1 away, so <b>Group A</b> is closest. "
                   "Group D’s 40 would be the theory for half of the spinner."))
    assert F(3, 10) * 50 == 15
    its.append(mcq("A bag has 3 red and 7 blue marbles. Arjun takes a marble, records its colour and puts it back, "
                   "50 times. About how many reds should he expect?", "about 15",
                   ["about 3", "about 35", "about 21"],
                   "Red is 3 of 10 marbles: " + fr(3, 10) + ". " + fr(3, 10) + " of 50 = <b>15</b>. About 35 is for blue. "
                   "About 21 comes from " + fr(3, 7) + " (red compared with blue)."))
    its.append(mcq("Simran tosses a coin 500 times and gets 262 heads. What is the experimental probability of heads, "
                   "as a decimal?", "0.524", ["0.262", "0.5", "0.476"],
                   fr(262, 500) + " = " + fr(524, 1000) + " = <b>0.524</b>, close to the theoretical 0.5. "
                   "0.476 is tails. 0.262 uses the count as a decimal.", ans=F(262, 500)))
    sA = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 3), "yellow")]
    sB = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    sC = [("red", F(1, 4), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 4), "yellow")]
    sD = [("red", F(3, 4), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow")]
    res = {"red": 52, "blue": 23, "yellow": 25}
    errs = [sum(abs(part(s, c) * 100 - res[c]) for c in res) for s in (sA, sB, sC, sD)]
    assert errs.index(min(errs)) == 1
    its.append(mcq_fixed(fig(spinners4_svg([sA, sB, sC, sD], label="four spinners which matches results")) +
                         "Mateo spins a spinner 100 times: red 52, blue 23, yellow 25. Which spinner did he most likely use?",
                         ["A", "B", "C", "D"], 1,
                         "Red came up about half the time, and blue and yellow about a quarter each. Spinner <b>B</b> is "
                         + fr(1, 2) + " red, " + fr(1, 4) + " blue and " + fr(1, 4) + " yellow. A would give about 33 of each."))
    assert F(20, 50) * 200 == 80
    its.append(mcq("Wei spins a spinner 50 times and gets blue 20 times. Use his experimental probability to predict "
                   "how many blues he will get in 200 spins.", "about 80", ["about 20", "about 40", "about 150"],
                   fr(20, 50) + " = " + fr(2, 5) + ". " + fr(2, 5) + " of 200 = <b>80</b>. Or: 200 is 4 × 50, so 4 × 20 = 80. "
                   "About 40 only doubles the 20."))
    its.append(mcq("Mateo rolls a number cube once and gets a 6. He says, “The experimental probability of a 6 is 1, "
                   "so this cube always lands on 6.” What is the best answer?",
                   "One roll is too few trials to tell",
                   ["He is right, the cube always lands on 6", "The probability of a 6 is now 0",
                    "He should use " + fr(6, 6) + " instead"],
                   "With only <b>one trial</b>, the experimental probability can be far from the theory (" + fr(1, 6) +
                   "). He needs many more rolls to tell if the cube is fair."))
    return {"title": "Comparing theoretical and experimental probability", "items": its}


# ============================================================ set 5: fair games
def set_fair():
    its = []
    its.append(mcq("Liam and Olivia toss a coin. Liam wins on heads and Olivia wins on tails. Is the game fair?",
                   "Yes, each has a probability of " + fr(1, 2),
                   ["No, Liam is more likely to win", "No, Olivia is more likely to win", "Yes, because Liam goes first"],
                   "A game is <b>fair</b> when every player has the same probability of winning. Heads and tails are "
                   "both " + fr(1, 2) + ", so <b>yes</b>."))
    its.append(mcq("Arjun and Chloe roll a number cube. Arjun wins on 1 or 2. Chloe wins on 3, 4, 5 or 6. "
                   "Is the game fair?", "No, Chloe is more likely to win",
                   ["Yes, they each have a number", "No, Arjun is more likely to win", "Yes, each has " + fr(1, 2)],
                   "Arjun: " + fr(2, 6) + ". Chloe: " + fr(4, 6) + ". The chances are not equal, so <b>no, Chloe is "
                   "more likely to win</b>."))
    assert P(lambda k: k % 2 == 0, CUBE6) == P(lambda k: k % 2 == 1, CUBE6)
    its.append(mcq("Noah and Ava roll a number cube. Noah wins on an even number and Ava wins on an odd number. "
                   "What is Ava’s probability of winning?", fr(3, 6), [fr(1, 6), fr(2, 6), fr(3, 3)],
                   "The odd numbers are 1, 3 and 5: <b>" + fr(3, 6) + "</b>. Noah also has " + fr(3, 6) +
                   " (2, 4, 6), so the game is fair. " + fr(3, 3) + " compares Ava’s numbers with Noah’s.",
                   ans=P(lambda k: k % 2 == 1, CUBE6)))
    assert P(lambda k: not is_prime(k), CUBE6) == F(3, 6)
    its.append(mcq("Mei and Lucas roll a number cube. Mei wins on a prime number. Lucas wins on a number that is "
                   "not prime. What is Lucas’s probability of winning?", fr(3, 6), [fr(2, 6), fr(4, 6), fr(3, 3)],
                   "Not prime: 1, 4 and 6 (1 is not a prime number). That is <b>" + fr(3, 6) + "</b>. "
                   + fr(2, 6) + " forgets the 1. " + fr(4, 6) + " thinks 2 is not prime. So the game is fair.",
                   ans=F(1, 2)))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    assert part(sp, "red") == part(sp, "blue") + part(sp, "yellow")
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow game")) +
                   "Kai wins if the spinner lands on red. Zara wins if it lands on blue or yellow. Is the game fair?",
                   "Yes, each has " + fr(1, 2),
                   ["No, Zara has 2 colours", "No, Kai is more likely to win", "No, Zara has " + fr(2, 3)],
                   "Kai: red = " + fr(1, 2) + ". Zara: " + fr(1, 4) + " + " + fr(1, 4) + " = " + fr(1, 2) + ". "
                   "<b>Yes, it is fair</b>. Counting colours (1 against 2) is the mistake."))
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow three players")) +
                   "Owen wins on red, Leah wins on blue and Ryan wins on yellow. Who is most likely to win?",
                   "Owen", ["Leah", "Ryan", "They are equally likely"],
                   "Owen’s red is " + fr(1, 2) + " of the spinner. Leah and Ryan have " + fr(1, 4) + " each. "
                   "<b>Owen</b> is most likely to win, so the game is not fair."))
    its.append(mcq("Wei, Hana and Mateo roll a number cube. Wei wins on 1 or 2, Hana on 3 or 4, and Mateo on 5 or 6. "
                   "What is each player’s probability of winning?", fr(2, 6), [fr(1, 6), fr(3, 6), fr(2, 3)],
                   "Each player has 2 of the 6 numbers: <b>" + fr(2, 6) + "</b> (= " + fr(1, 3) + "). "
                   "The three chances are equal, so the game is fair.", ans=F(1, 3)))
    its.append(mcq("A spinner has 8 equal sections: 5 blue and 3 red. Ethan wins on blue and Sofia wins on red. "
                   "Which change makes the game fair?", "Paint 1 blue section red",
                   ["Paint 2 blue sections red", "Paint 1 red section blue", "Nothing, it is already fair"],
                   "A fair spinner needs 4 blue and 4 red sections. <b>Painting 1 blue section red</b> gives "
                   + fr(4, 8) + " each. Painting 2 would give 3 blue and 5 red: unfair the other way."))
    assert F(5 - 1, 8) == F(3 + 1, 8) and F(5 - 2, 8) != F(3 + 2, 8)
    its.append(mcq("A bag has 4 green and 6 yellow marbles. Jasleen wins if she takes a green marble. "
                   "What is her probability of winning?", fr(4, 10), [fr(4, 6), fr(1, 2), fr(6, 10)],
                   "4 of the 10 marbles are green: <b>" + fr(4, 10) + "</b>. " + fr(4, 6) +
                   " compares green with yellow. " + fr(1, 2) + " counts 2 colours, but there are more yellow marbles.",
                   ans=F(4, 10)))
    assert F(4 + 2, 10 + 2) == F(1, 2)
    its.append(mcq("The bag has 4 green and 6 yellow marbles. Jasleen wins on green and Harjot wins on yellow. "
                   "How many green marbles should be added to make the game fair?", "2", ["6", "1", "10"],
                   "Fair means the same number of green and yellow marbles: 6 green and 6 yellow. 6 − 4 = <b>2</b>. "
                   "Adding 6 would make 10 green. 1 would only work if you also took out a yellow one.", ans=2))
    its.append(mcq("Ryan and Nadia roll a number cube. Ryan gets points on a 6. Nadia gets 1 point on any other number. "
                   "How many points should Ryan get for a 6 to make the game fair?", "5", ["6", "1", "2"],
                   "Nadia wins " + fr(5, 6) + " of the rolls and Ryan only " + fr(1, 6) + ", 5 times less often. "
                   "So Ryan should get <b>5</b> points. In 60 rolls: Ryan 10 × 5 = 50, Nadia 50 × 1 = 50.", ans=5))
    assert F(1, 6) * 60 * 5 == F(5, 6) * 60 * 1
    its.append(mcq("A prize wheel at a school carnival in Kamloops has 10 equal sections. 2 sections win a prize. "
                   "What is the probability of winning a prize, as a percent?", "20%", ["2%", "80%", "25%"],
                   fr(2, 10) + " = " + fr(20, 100) + " = <b>20%</b>. 80% is the chance of NOT winning. "
                   "25% compares the 2 prize sections with the other 8.", ans=F(2, 10)))
    assert F(5, 200) == F("0.025")
    its.append(mcq("A class sells 200 raffle tickets to raise money for the Terry Fox Run. Harjot buys 5 tickets. "
                   "One ticket is drawn. What is the probability that Harjot wins, as a percent?", "2.5%",
                   ["5%", "0.25%", "25%"],
                   fr(5, 200) + " = " + fr(1, 40) + " = 0.025 = <b>2.5%</b>. 5% uses the number of tickets as the "
                   "percent.", ans=F(5, 200)))
    assert F(1, 3) > F(3, 10)
    its.append(mcq("Game A: spin a spinner with 3 equal sections and win on red. Game B: pick a ticket from a box of "
                   "10 tickets where 3 tickets win. Which game gives a better chance of winning?", "Game A",
                   ["Game B, it has more winning tickets", "They are the same", "You can’t tell"],
                   "Game A: " + fr(1, 3) + " ≈ 0.333. Game B: " + fr(3, 10) + " = 0.3. <b>Game A</b> is a little better, "
                   "even though Game B has more winning tickets."))
    nadia = [k for k in range(1, 11) if k < 5]
    owen = [k for k in range(1, 11) if k > 5]
    assert len(nadia) == 4 and len(owen) == 5
    its.append(mcq("Cards numbered 1 to 10 are mixed up. Nadia wins if she picks a number less than 5. Owen wins if "
                   "she picks a number greater than 5. Who is more likely to win?", "Owen",
                   ["Nadia", "They are equally likely", "You can’t tell"],
                   "Less than 5: 1, 2, 3, 4 (4 cards). Greater than 5: 6, 7, 8, 9, 10 (5 cards). <b>Owen</b> has "
                   + fr(5, 10) + " and Nadia " + fr(4, 10) + ". Counting 1 to 5 and 5 to 10 as 5 each is the mistake."))
    its.append(mcq("Kai and Leah play a fair coin game 20 times. Kai wins 13 games. Does this show that the game is "
                   "unfair?", "No, 20 games is too few to tell",
                   ["Yes, Kai is more likely to win", "Yes, Leah’s chance is now " + fr(7, 20),
                    "No, the results must be 10 and 10"],
                   "In theory each player wins " + fr(1, 2) + " of the time, but results vary. 13 wins in only "
                   "20 games can happen by chance. <b>No, 20 games is too few to tell</b>."))
    its.append(mcq("Wei, Mei and Nadia spin a spinner with 4 equal sections: red, blue, yellow and green. Wei wins on red, "
                   "Mei on blue, and Nadia on yellow or green. What is Nadia’s probability of winning?", fr(2, 4),
                   [fr(1, 4), fr(1, 3), fr(2, 3)],
                   "Nadia has 2 of the 4 equal sections: <b>" + fr(2, 4) + "</b>. " + fr(1, 3) +
                   " uses the 3 players, but the outcomes are the 4 sections. The game is not fair.", ans=F(1, 2)))
    assert F(9, 12) == F(75, 100)
    its.append(mcq("A spinner at a ski lodge in Whistler has 12 equal sections. 3 sections win a free hot chocolate. "
                   "What is the probability of NOT winning, as a decimal?", "0.75", ["0.25", "0.9", "0.3"],
                   "Not winning: 12 − 3 = 9 sections. " + fr(9, 12) + " = " + fr(3, 4) + " = <b>0.75</b>. "
                   "0.25 is the chance of winning. 0.9 just uses the 9.", ans=F(9, 12)))
    opts = {"Arjun wins on 1, 2 or 3; Simran wins on 4, 5 or 6": (3, 3),
            "Arjun wins on 1 or 2; Simran wins on 3, 4, 5 or 6": (2, 4),
            "Arjun wins on 1 or 6; Simran wins on 2, 3 or 4": (2, 3),
            "Arjun wins on 5; Simran wins on any other number": (1, 5)}
    assert [k for k, (a, b) in opts.items() if a == b] == ["Arjun wins on 1, 2 or 3; Simran wins on 4, 5 or 6"]
    keys = list(opts)
    its.append(mcq("Arjun and Simran roll a number cube. Which rule makes a fair game?", keys[0], keys[1:],
                   "In a fair game both players have the same number of outcomes. <b>1, 2 or 3 against 4, 5 or 6</b> "
                   "gives each " + fr(3, 6) + ". With 1 or 6 against 2, 3 or 4, the 5 wins for nobody and Simran has more."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    assert part(sp, "red") * 1 == part(sp, "blue") * 3
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red points game")) +
                   "Owen gets 1 point when the spinner lands on red. Leah gets points when it lands on blue. "
                   "How many points should Leah get for blue to make the game fair?", "3", ["4", "1", "2"],
                   "Red is " + fr(3, 4) + " and blue is " + fr(1, 4) + ": red comes up 3 times as often. "
                   "So Leah needs <b>3</b> points. In 40 spins: Owen 30 × 1 = 30, Leah 10 × 3 = 30. "
                   "4 counts all 4 quarters.", ans=3))
    return {"title": "Fair games", "items": its}


# ============================================================ lesson
def body_html():
    line = scale_svg(4, [], [(F(0), "0"), (F(1, 4), "0.25"), (F(1, 2), "0.5"), (F(3, 4), "0.75"), (F(1), "1")],
                     words=True, label="probability line from impossible to certain")
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    spin = spinner_svg(sp, label="spinner half red quarter blue quarter yellow")
    tab = freq_svg("20 spins", "Colour", ["red", "blue", "yellow"], [11, 4, 5], tally=True,
                   label="frequency table tally 20 spins")
    assert F(11, 20) == F(55, 100)
    return (
        "<h2>What is a probability?</h2>"
        "<p>A probability is a number from <b>0</b> to <b>1</b>. 0 means impossible. 1 means certain. "
        + fr(1, 2) + " (0.5) means equally likely to happen or not. A probability is never more than 1.</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>Every probability has a place on this line.</figcaption></figure>"
        "<p>You can write the same probability as a fraction, a decimal or a percent.</p>"
        + table(["Fraction", "Decimal", "Percent", "Chance"], [
            ["0", "0", "0%", "impossible"],
            [fr(1, 4), "0.25", "25%", "unlikely"],
            [fr(1, 2), "0.5", "50%", "equally likely"],
            [fr(3, 4), "0.75", "75%", "likely"],
            ["1", "1", "100%", "certain"],
        ])
        + "<h2>Theoretical probability</h2>"
        "<p>Theoretical probability is what <b>should</b> happen. When the outcomes are equally likely:</p>"
        "<p><b>probability = outcomes you want ÷ all the possible outcomes</b></p>"
        + ex("Example 1", "You roll a number cube with the numbers 1 to 6. What is the probability of rolling a number "
             "greater than 4?",
             "Greater than 4 means 5 or 6. That is 2 of the 6 outcomes. Do not count the 4.",
             fr(2, 6) + " = " + fr(1, 3))
        + "<figure class='sn-fig'>" + spin +
        "<figcaption>The sections are not the same size: red is half of the spinner.</figcaption></figure>"
        + ex("Example 2", "What is the probability of landing on blue?",
             "Blue is one quarter of the spinner. Do not count colours (1 of 3), because the sections are not equal.",
             fr(1, 4) + " = 0.25 = 25%")
        + "<h2>Experimental probability</h2>"
        "<p>Experimental probability is what <b>did</b> happen in an experiment:</p>"
        "<p><b>experimental probability = times it happened ÷ number of trials</b></p>"
        "<figure class='sn-fig'>" + tab +
        "<figcaption>Results of spinning the spinner above 20 times.</figcaption></figure>"
        + ex("Example 3", "What is the experimental probability of red?",
             "Red came up 11 times in 20 spins. The theory says " + fr(1, 2) + " = 0.5, so the result is close.",
             fr(11, 20) + " = 0.55 = 55%")
        + "<p>Theoretical and experimental probabilities are usually close, but rarely exactly the same. "
        "<b>More trials usually get closer to the theory.</b></p>"
        + table(["Coin tosses", "Heads", "Experimental probability"], [
            ["10", "7", fr(7, 10) + " = 0.7"],
            ["100", "46", fr(46, 100) + " = 0.46"],
            ["1000", "508", fr(508, 1000) + " = 0.508"],
        ])
        + "<h2>Fair games</h2>"
        "<p>A game is <b>fair</b> when every player has the same probability of winning.</p>"
        + ex("Example 4", "On a number cube, Liam wins on 1 or 2 and Ava wins on 3, 4, 5 or 6. Is the game fair?",
             "Liam: " + fr(2, 6) + ". Ava: " + fr(4, 6) + ". The probabilities are not equal.",
             "No, Ava is more likely to win")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 red, 5 blue, so P(red) = " + fr(3, 5) + ".", "Divide by ALL the outcomes: " + fr(3, 8) + "."],
            ["3 colours, so each colour is " + fr(1, 3) + ".", "Only if the sections are the same size."],
            ["“Greater than 4” includes the 4.", "Greater than 4 on a number cube means 5 and 6 only."],
            ["“5 tails in a row, so heads is due.”", "A coin has no memory. Heads is still " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "What do Grade 6 students learn about probability in BC?",
     "a": "The BC Grade 6 math curriculum covers single-outcome probability, both theoretical and experimental. Students write probabilities as fractions, decimals and percents, find them for number cubes and spinners, compare them with results from experiments, and decide whether games are fair."},
    {"q": "What is the difference between theoretical and experimental probability?",
     "a": "Theoretical probability is what should happen, found by counting outcomes: a 6 on a number cube is 1/6. Experimental probability is what actually happened, such as 23 heads in 50 tosses (23/50). With more trials, the two usually get closer."},
    {"q": "How do you know if a game is fair?",
     "a": "A game is fair when every player has the same probability of winning. On a number cube, 1, 2, 3 against 4, 5, 6 is fair (3/6 each), but 1, 2 against 3, 4, 5, 6 is not (2/6 against 4/6)."},
    {"q": "Why is the experimental probability different from the theoretical probability?",
     "a": "Each trial depends on chance, so results vary, especially with only a few trials. If you toss a coin 10 times you might get 7 heads, but after 1000 tosses the share of heads is usually very close to 1/2."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (probability lines, rows of spinners, tables, letter cards)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(56817)
    sets = [set_fdp(), set_theory(), set_experimental(), set_compare(), set_fair()]
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
        "country": "ca-bc", "subject": "math", "grade": "grade-6", "slug": "probability", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 6 Probability: Theoretical and Experimental",
        "seo_title": "Grade 6 Probability Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Probability",
        "domain": "Data and probability",
        "standard_code": "Grade 6: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/6/core",
        "standard_text": "Single-outcome probability, both theoretical and experimental",
        "meta_desc": "Free Grade 6 math worksheets on probability for the BC curriculum: probability as a fraction, decimal and percent, theoretical probability with number cubes and spinners, experimental probability from results, comparing the two, and fair games. 100 questions with an answer key.",
        "key_big": "Theoretical probability = outcomes you want ÷ all the outcomes. Experimental probability = times it happened ÷ number of trials.",
        "key_sub": "On a number cube, “greater than 4” is 5 and 6 only: 2/6. With more trials, the experimental probability usually gets closer to the theory. A game is fair when every player has the same chance.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(probability line|four spinners|frequency table|letter cards)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
