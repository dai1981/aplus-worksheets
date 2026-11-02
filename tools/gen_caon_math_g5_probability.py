# -*- coding: utf-8 -*-
"""
CA Grade 5 Math: Probability (Ontario Mathematics Curriculum 2020, Grade 5: Data, D2.1 and D2.2)
  python3 tools/gen_caon_math_g5_probability.py
Probability as a fraction (outcomes you want / all outcomes), the probability line from 0 to 1 (fractions and
chance words), spinners with unequal parts, number cubes, bags and cards, theoretical vs experimental probability
of one event, and predictions and fair games in Canadian contexts.
Wrong answers come from real student mistakes: part-to-part instead of part-to-whole (3 red, 5 blue gives 3/5),
counting colours or sections instead of part sizes, counting outcomes wrongly (including the 3 in "less than 3",
counting 11 twice, distinct letters instead of cards), counting tick marks instead of parts on the line,
probabilities greater than 1, using the face number as a count, and the gambler's fallacy.
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Canadian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-5")
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


# ============================================================ set 1: probability as a fraction
def set_fraction():
    its = []
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 3?", fr(1, 6),
                   [fr(3, 6), fr(1, 3), fr(6, 1)],
                   "There are 6 equally likely outcomes and only one of them is 3: <b>" + fr(1, 6) + "</b>. "
                   + fr(3, 6) + " uses the number 3 as the count, but only one face shows a 3. " + fr(6, 1) + " is upside down.", ans=F(1, 6)))
    sp = nums_spinner(5)
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 5 equal sections 1 to 5")) +
                   "The spinner has 5 equal sections. What is the probability of landing on 4?", fr(1, 5),
                   [fr(4, 5), fr(1, 4), fr(5, 1)],
                   "4 is on 1 of the 5 equal sections: <b>" + fr(1, 5) + "</b>. " + fr(1, 4) +
                   " compares the 4 with the other 4 sections, not with all 5.", ans=F(1, 5)))
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one without looking. What is the probability "
                   "of picking the 7?", fr(1, 10), [fr(7, 10), fr(1, 7), fr(10, 1)],
                   "There is one 7 card out of 10 cards: <b>" + fr(1, 10) + "</b>. " + fr(7, 10) +
                   " would be the chance of picking a number from 1 to 7.", ans=F(1, 10)))
    its.append(mcq(fig(bag_svg([("red", 2), ("blue", 3)], label="bag of 2 red and 3 blue marbles")) +
                   "A bag has 2 red and 3 blue marbles. You take one without looking. What is the probability of red?",
                   fr(2, 5), [fr(2, 3), fr(3, 5), fr(1, 2)],
                   "There are 2 + 3 = 5 marbles and 2 are red: <b>" + fr(2, 5) + "</b>. " + fr(2, 3) +
                   " compares red with blue, not with all 5 marbles. Two colours does not mean " + fr(1, 2) + ".",
                   ans=F(2, 5)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling an even number?",
                   fr(3, 6), [fr(2, 6), fr(1, 6), fr(6, 3)],
                   "The even numbers are 2, 4 and 6: 3 of the 6 outcomes, so <b>" + fr(3, 6) + "</b>. "
                   + fr(2, 6) + " forgets that 6 is even too. " + fr(6, 3) + " is upside down.", ans=F(1, 2)))
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
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one. What is the probability of an even number?",
                   fr(5, 10), [fr(4, 10), fr(5, 5), fr(1, 10)],
                   "The even numbers are 2, 4, 6, 8 and 10: 5 of the 10 cards, so <b>" + fr(5, 10) + "</b>. "
                   + fr(4, 10) + " forgets the 10. " + fr(5, 5) + " compares even cards with odd cards.", ans=F(1, 2)))
    assert [k for k in range(1, 11) if k % 2 == 0] == [2, 4, 6, 8, 10]
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which outcome has a probability of " + fr(3, 6) + "?",
                   "rolling an odd number", ["rolling a 3", "rolling a number less than 3", "rolling a 6"],
                   "The odd numbers are 1, 3 and 5: 3 of the 6 outcomes. So <b>rolling an odd number</b> has a "
                   "probability of " + fr(3, 6) + ". Rolling a 3 is only " + fr(1, 6) + "."))
    sp = nums_spinner(8)
    odd = [k for k in range(1, 9) if k % 2]
    assert odd == [1, 3, 5, 7]
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 8 equal sections 1 to 8")) +
                   "The spinner has 8 equal sections. What is the probability of landing on an odd number?",
                   fr(4, 8), [fr(3, 8), fr(4, 4), fr(1, 8)],
                   "The odd numbers are 1, 3, 5 and 7: 4 of the 8 sections, so <b>" + fr(4, 8) + "</b>. "
                   + fr(3, 8) + " forgets the 1. " + fr(4, 4) + " compares odd with even.", ans=F(1, 2)))
    its.append(mcq("Cards numbered 1 to 8 are shuffled. You pick one. What is the probability of a number greater than 5?",
                   fr(3, 8), [fr(4, 8), fr(5, 8), fr(3, 5)],
                   "Greater than 5 means 6, 7 or 8: 3 of the 8 cards, so <b>" + fr(3, 8) + "</b>. "
                   + fr(4, 8) + " wrongly counts the 5. " + fr(5, 8) + " is the chance of 5 or less.", ans=F(3, 8)))
    its.append(mcq(fig(bag_svg([("green", 4), ("yellow", 1), ("purple", 3)], label="bag of 4 green 1 yellow 3 purple")) +
                   "You take one marble without looking. What is the probability of green?",
                   fr(4, 8), [fr(4, 4), fr(1, 3), fr(3, 8)],
                   "There are 4 + 1 + 3 = 8 marbles and 4 are green: <b>" + fr(4, 8) + "</b>. " + fr(4, 4) +
                   " compares green with the other 4 marbles. " + fr(1, 3) + " counts colours, not marbles.",
                   ans=F(1, 2)))
    its.append(mcq("A bag has 3 red, 5 blue and 2 yellow marbles. What is the probability of NOT taking red?",
                   fr(7, 10), [fr(3, 10), fr(7, 3), fr(5, 10)],
                   "Not red means blue or yellow: 5 + 2 = 7 of the 10 marbles, so <b>" + fr(7, 10) + "</b>. "
                   + fr(5, 10) + " forgets the yellow marbles. " + fr(3, 10) + " is the chance of red.", ans=F(7, 10)))
    word = "CANADA"
    assert word.count("A") == 3 and len(word) == 6 and len(set(word)) == 4
    its.append(mcq("The letters of CANADA are written on 6 cards. You pick one card without looking. "
                   "What is the probability of A?", fr(3, 6), [fr(1, 6), fr(1, 4), fr(3, 3)],
                   "CANADA has 6 letters and 3 of them are A: <b>" + fr(3, 6) + "</b>. " + fr(1, 4) +
                   " counts the 4 different letters, but A is on 3 cards. " + fr(3, 3) +
                   " compares the A cards with the other 3 cards.", ans=F(1, 2)))
    word = "OTTAWA"
    assert word.count("T") == 2 and len(word) == 6 and len(set(word)) == 4
    its.append(mcq("The letters of OTTAWA are written on 6 cards. You pick one card without looking. "
                   "What is the probability of T?", fr(2, 6), [fr(1, 6), fr(2, 4), fr(1, 4)],
                   "OTTAWA has 6 letters and 2 of them are T: <b>" + fr(2, 6) + "</b>. " + fr(1, 4) +
                   " counts the 4 different letters (O, T, A, W). " + fr(2, 4) +
                   " compares the T cards with the other 4 cards.", ans=F(1, 3)))
    mult4 = [k for k in range(1, 13) if k % 4 == 0]
    assert mult4 == [4, 8, 12]
    its.append(mcq("Cards numbered 1 to 12 are shuffled. You pick one. What is the probability of a multiple of 4?",
                   fr(3, 12), [fr(4, 12), fr(2, 12), fr(9, 12)],
                   "The multiples of 4 are 4, 8 and 12: 3 of the 12 cards, so <b>" + fr(3, 12) + "</b>. "
                   + fr(4, 12) + " uses the 4 from the question. " + fr(2, 12) + " forgets the 12. " + fr(9, 12) +
                   " is the chance of NOT a multiple of 4.", ans=F(1, 4)))
    its.append(mcq("A box has 12 muffins: 5 blueberry, 4 banana and 3 bran. You take one without looking. "
                   "What is the probability of banana?", fr(4, 12), [fr(4, 8), fr(5, 12), fr(8, 12)],
                   "4 of the 12 muffins are banana: <b>" + fr(4, 12) + "</b>. " + fr(4, 8) +
                   " compares banana with the other 8 muffins. " + fr(8, 12) + " is the chance of NOT banana.",
                   ans=F(1, 3)))
    its.append(mcq("A drawer has 12 socks: 5 black, 4 white and 3 grey. Owen takes one sock without looking. "
                   "What is the probability that it is white or grey?", fr(7, 12), [fr(3, 12), fr(4, 12), fr(7, 5)],
                   "White or grey: 4 + 3 = 7 of the 12 socks, so <b>" + fr(7, 12) + "</b>. "
                   + fr(7, 5) + " compares with the 5 black socks and is greater than 1.", ans=F(7, 12)))
    its.append(mcq("A bag has 3 red and 4 blue marbles. Hana says the probability of red is " + fr(3, 4) +
                   ". What is her mistake?", "She compared red with blue, not with all 7 marbles",
                   ["Nothing, " + fr(3, 4) + " is right", "She should write " + fr(4, 3),
                    "It should be " + fr(1, 2) + " because there are 2 colours"],
                   "A probability compares with ALL the outcomes. There are 3 + 4 = 7 marbles, so P(red) = "
                   + fr(3, 7) + ". <b>She compared red with blue</b> instead of with all 7 marbles."))
    assert F(3, 3 + 4) == F(3, 7)
    return {"title": "Probability as a fraction", "items": its}


# ============================================================ set 2: the probability line
def set_line():
    its = []
    its.append(mcq("What is the probability of an event that is impossible?", "0", ["1", fr(1, 2), fr(1, 10)],
                   "An impossible event can never happen, so its probability is <b>0</b>. " + fr(1, 10) +
                   " is very unlikely, but it can still happen.", ans=0))
    its.append(mcq("What is the probability of an event that is certain?", "1", ["0", fr(1, 2), "10"],
                   "A certain event will happen every time, so its probability is <b>1</b>. "
                   "A probability is never more than 1, so 10 is not possible.", ans=1))
    its.append(mcq("An event is equally likely to happen or not happen. What is its probability?", fr(1, 2),
                   ["2", "1", "0"],
                   "Equally likely is halfway between 0 and 1: <b>" + fr(1, 2) + "</b>. "
                   "2 is the number of outcomes, not the probability.", ans=F(1, 2)))
    its.append(mcq("A bag has only 6 green marbles. You take one without looking. What is the probability of red?",
                   "0", [fr(1, 6), fr(6, 6), fr(1, 2)],
                   "There are no red marbles, so taking red is impossible: <b>0</b>.", ans=0))
    its.append(mcq("A bag has only 6 green marbles. You take one without looking. What is the probability of green?",
                   fr(6, 6), [fr(1, 6), "0", fr(6, 1)],
                   "All 6 marbles are green: <b>" + fr(6, 6) + "</b> = 1, so it is certain. " + fr(1, 6) +
                   " counts only one marble.", ans=1))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. Which word describes rolling a number less than 7?",
                   "certain", ["likely", "equally likely", "impossible"],
                   "Every number on the cube is less than 7, so it will happen every time: <b>certain</b> ("
                   + fr(6, 6) + " = 1)."))
    its.append(mcq(fig(scale_svg(4, [(F(3, 4), "")], ends_half(4), label="probability line in quarters arrow at three quarters")) +
                   "Which word best describes the chance shown by the arrow?", "likely",
                   ["unlikely", "certain", "equally likely"],
                   "The arrow is between " + fr(1, 2) + " and 1, closer to 1: <b>likely</b>. "
                   "It is not certain, because it is not at 1."))
    its.append(mcq(fig(scale_svg(8, [(F(1, 8), "")], ends_half(8), label="probability line in eighths arrow at one eighth")) +
                   "Which word best describes the chance shown by the arrow?", "unlikely",
                   ["impossible", "likely", "equally likely"],
                   "The arrow is close to 0 but not at 0: <b>unlikely</b>. Impossible would be exactly 0."))
    its.append(mcq(fig(scale_svg(4, [(F(1, 4), "")], ENDS, label="probability line in quarters arrow at one quarter")) +
                   "The probability line is split into 4 equal parts. What probability does the arrow show?", fr(1, 4),
                   [fr(3, 4), fr(1, 5), fr(1, 3)],
                   "There are 4 equal parts from 0 to 1, and the arrow is 1 part from 0: <b>" + fr(1, 4) + "</b>. "
                   + fr(1, 5) + " counts the 5 tick marks instead of the 4 parts. " + fr(3, 4) + " counts from the 1 end.",
                   ans=F(1, 4)))
    its.append(mcq(fig(scale_svg(8, [(F(3, 8), "")], ENDS, label="probability line in eighths arrow at three eighths")) +
                   "The probability line is split into 8 equal parts. What probability does the arrow show?", fr(3, 8),
                   [fr(5, 8), fr(3, 9), fr(3, 4)],
                   "Count the parts from 0: the arrow is 3 parts of 8, so <b>" + fr(3, 8) + "</b>. " + fr(3, 9) +
                   " counts the 9 tick marks. " + fr(5, 8) + " counts from the 1 end.", ans=F(3, 8)))
    its.append(mcq(fig(scale_svg(6, [(F(5, 6), "")], ENDS, label="probability line in sixths arrow at five sixths")) +
                   "The probability line is split into 6 equal parts. What probability does the arrow show?", fr(5, 6),
                   [fr(1, 6), fr(5, 7), fr(6, 5)],
                   "The arrow is 5 parts of 6 from 0: <b>" + fr(5, 6) + "</b>. " + fr(5, 7) +
                   " counts the 7 tick marks. " + fr(6, 5) + " is greater than 1, so it can’t be on the line.",
                   ans=F(5, 6)))
    its.append(mcq("Which fraction can NOT be a probability?", fr(5, 4), [fr(4, 5), "0", "1"],
                   "Probabilities go from 0 to 1. <b>" + fr(5, 4) + "</b> has a numerator greater than its denominator, "
                   "so it is more than 1. 0 and 1 are allowed: they mean impossible and certain."))
    its.append(mcq("Which probability shows the most likely event?", fr(1, 2), [fr(1, 8), fr(1, 3), fr(1, 4)],
                   "All the numerators are 1. The smaller the denominator, the bigger the part: <b>" + fr(1, 2) +
                   "</b> is the greatest. " + fr(1, 8) + " has the biggest number, but it is the smallest fraction.",
                   ans=F(1, 2)))
    assert max(F(1, 2), F(1, 8), F(1, 3), F(1, 4)) == F(1, 2)
    its.append(mcq("Which probability is closest to certain?", fr(11, 12), [fr(1, 12), fr(6, 12), fr(3, 12)],
                   "Certain is 1 = " + fr(12, 12) + ". <b>" + fr(11, 12) + "</b> is only " + fr(1, 12) +
                   " away from 1, so it is very likely.", ans=F(11, 12)))
    marks = [(F(0), "A"), (F(2, 8), "B"), (F(5, 8), "C"), (F(1), "D")]
    line = lambda: fig(scale_svg(8, marks, ENDS, label="probability line in eighths with points A B C D"))
    its.append(mcq_fixed(line() + "A bag has 2 red and 6 blue marbles. You take one without looking. "
                         "Which letter shows the probability of taking a red marble?", ["A", "B", "C", "D"], 1,
                         "2 of the 8 marbles are red: " + fr(2, 8) + ". That is 2 parts of 8 from 0: point <b>B</b>. "
                         "Blue would be " + fr(6, 8) + ", which is not marked."))
    assert F(2, 8) == marks[1][0]
    its.append(mcq_fixed(line() + "The same bag has 2 red and 6 blue marbles. "
                         "Which letter shows the probability of taking a yellow marble?", ["A", "B", "C", "D"], 0,
                         "There are no yellow marbles, so it is impossible: 0, point <b>A</b>."))
    its.append(mcq("Which event best fits a probability close to 1?", "Snow falls in Ottawa sometime in January",
                   ["A coin lands on heads", "Rolling a 6 on a number cube", "Snow falls in Toronto on Canada Day"],
                   "Ottawa almost always gets snow in January, so that is very likely: close to 1. A coin is "
                   + fr(1, 2) + ", a 6 is " + fr(1, 6) + ", and snow in Toronto on July 1 is close to 0. So the answer is "
                   "<b>snow in Ottawa in January</b>."))
    its.append(mcq("You roll a number cube. Order these from least likely to most likely.<br>"
                   "A: rolling a 1 &nbsp; B: rolling an even number &nbsp; C: rolling a number less than 6",
                   "A, B, C", ["C, B, A", "B, A, C", "A, C, B"],
                   "A is " + fr(1, 6) + ", B is " + fr(3, 6) + " and C is " + fr(5, 6) + ". From least to most likely: "
                   "<b>A, B, C</b>."))
    assert F(1, 6) < F(3, 6) < F(5, 6)
    its.append(mcq("Owen says the probability that his hockey team wins on Saturday is " + fr(3, 2) +
                   ", because they are very good. What is wrong?", "A probability can’t be more than 1",
                   ["Nothing, good teams can go above 1", "The numerator must always be 1",
                    "The denominator must always be 10"],
                   "Even a certain event has probability 1. " + fr(3, 2) + " is more than 1, so <b>it can’t be a "
                   "probability</b>. A very good team might be " + fr(4, 5) + ": likely, not certain."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red one quarter blue")) +
                   "What is the probability of landing on red, and where is it on the probability line?",
                   fr(3, 4) + ", between " + fr(1, 2) + " and 1",
                   [fr(1, 4) + ", between 0 and " + fr(1, 2), fr(3, 4) + ", between 0 and " + fr(1, 2),
                    fr(1, 2) + ", in the middle"],
                   "Red covers " + fr(3, 4) + " of the spinner. " + fr(3, 4) + " is more than " + fr(1, 2) +
                   ", so it is <b>between " + fr(1, 2) + " and 1</b>: likely. " + fr(1, 2) +
                   " counts 2 colours, but the parts are not equal."))
    assert part(sp, "red") == F(3, 4)
    return {"title": "The probability line from 0 to 1", "items": its}


# ============================================================ set 3: spinners, number cubes and bags
def set_find():
    its = []
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "What is the probability of landing on red?", fr(1, 2), [fr(1, 3), fr(1, 4), fr(3, 4)],
                   "Red covers half of the spinner: <b>" + fr(1, 2) + "</b>. " + fr(1, 3) +
                   " counts the 3 colours, but the parts are not the same size.", ans=part(sp, "red")))
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "What is the probability of landing on blue?", fr(1, 4), [fr(1, 3), fr(1, 2), fr(3, 4)],
                   "Blue covers one quarter of the spinner: <b>" + fr(1, 4) + "</b>. " + fr(1, 3) +
                   " counts the 3 colours, but red is bigger than blue.", ans=part(sp, "blue")))
    sp = [("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"),
          ("Y", F(1, 8), "yellow"), ("Y", F(1, 8), "yellow"), ("G", F(1, 8), "green"), ("Y", F(1, 8), "yellow")]
    assert part(sp, "G") == F(3, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight sections three green")) +
                   "The spinner has 8 equal sections: G is green and Y is yellow. What is the probability of green?",
                   fr(3, 8), [fr(3, 5), fr(5, 8), fr(1, 2)],
                   "3 of the 8 equal sections are green: <b>" + fr(3, 8) + "</b>. " + fr(3, 5) +
                   " compares green with yellow. Two colours does not mean " + fr(1, 2) + ".", ans=F(3, 8)))
    its.append(mcq(fig(bag_svg([("red", 4), ("blue", 2), ("yellow", 2)], label="bag of 4 red 2 blue 2 yellow")) +
                   "You take one marble without looking. What is the probability of blue?",
                   fr(2, 8), [fr(2, 6), fr(4, 8), fr(6, 8)],
                   "There are 4 + 2 + 2 = 8 marbles and 2 are blue: <b>" + fr(2, 8) + "</b>. " + fr(2, 6) +
                   " compares blue with the other 6 marbles. " + fr(4, 8) + " is red.", ans=F(1, 4)))
    its.append(mcq("You roll a number cube with the numbers 1 to 6. What is the probability of rolling a 2 or a 5?",
                   fr(2, 6), [fr(1, 6), fr(4, 6), fr(2, 4)],
                   "Two faces work, 2 and 5: <b>" + fr(2, 6) + "</b>. " + fr(4, 6) + " counts every number from 2 to 5. "
                   + fr(2, 4) + " compares with the other 4 faces.", ans=F(1, 3)))
    sp = nums_spinner(8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 8 equal sections 1 to 8")) +
                   "What is the probability of landing on a number greater than 6?", fr(2, 8),
                   [fr(3, 8), fr(6, 8), fr(1, 8)],
                   "Greater than 6 means 7 or 8: 2 of the 8 sections, so <b>" + fr(2, 8) + "</b>. "
                   + fr(3, 8) + " wrongly counts the 6. " + fr(6, 8) + " is 6 or less.", ans=F(1, 4)))
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
    sp = [("R", F(1, 6), "red"), ("B", F(1, 6), "blue"), ("R", F(1, 6), "red"), ("Y", F(1, 6), "yellow"),
          ("R", F(1, 6), "red"), ("B", F(1, 6), "blue")]
    assert part(sp, "R") == F(3, 6) and part(sp, "B") == F(2, 6)
    its.append(mcq(fig(spinner_svg(sp, label="spinner 6 sections 3 red 2 blue 1 yellow")) +
                   "The spinner has 6 equal sections (R = red, B = blue, Y = yellow). Which colour is most likely?", "red",
                   ["blue", "yellow", "They are all equally likely"],
                   "Red is on 3 sections (" + fr(3, 6) + "), blue on 2 (" + fr(2, 6) + ") and yellow on 1 ("
                   + fr(1, 6) + "). <b>Red</b> is most likely. Three colours does not mean equally likely."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 6), "blue"), ("blue", F(1, 6), "blue"), ("blue", F(1, 6), "blue")]
    assert part(sp, "red") == part(sp, "blue") == F(1, 2)
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red and three blue sixths")) +
                   "Which is more likely: landing on red or landing on blue?", "They are equally likely",
                   ["Blue, it has 3 sections", "Red, it has the biggest section", "You can’t tell"],
                   "Red covers " + fr(1, 2) + ". Blue covers " + fr(1, 6) + " + " + fr(1, 6) + " + " + fr(1, 6) + " = "
                   + fr(3, 6) + " = " + fr(1, 2) + ". So they are <b>equally likely</b>. Look at the size of the parts, "
                   "not the number of sections."))
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
                         "Spinner A has 4 sections, but blue is half of it."))
    A = [("red", F(1, 4), "red"), ("blue", F(3, 4), "blue")]
    B = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("blue", F(1, 4), "blue")]
    C = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 8), "red"), ("blue", F(1, 8), "blue")]
    D = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("red", F(1, 3), "red")]
    fair = [part(x, "red") == part(x, "blue") for x in (A, B, C, D)]
    assert fair == [False, True, False, False]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D], label="four spinners red and blue")) +
                         "On which spinner are red and blue equally likely?", ["A", "B", "C", "D"], 1,
                         "On spinner <b>B</b> red and blue each cover 2 of 4 equal sections: " + fr(2, 4) + " each. "
                         "Spinner C also has 2 red and 2 blue sections, but the sections are not the same size: red is "
                         + fr(5, 8) + "."))
    assert part(C, "red") == F(5, 8)
    word = "SASKATOON"
    assert word.count("O") == 2 and len(word) == 9 and len(set(word)) == 6
    its.append(mcq("The letters of SASKATOON are written on 9 cards. You pick one card without looking. "
                   "What is the probability of O?", fr(2, 9), [fr(1, 9), fr(2, 6), fr(2, 7)],
                   "SASKATOON has 9 letters and 2 of them are O: <b>" + fr(2, 9) + "</b>. " + fr(2, 6) +
                   " counts the 6 different letters. " + fr(2, 7) + " compares the O cards with the other 7 cards.",
                   ans=F(2, 9)))
    ones = [k for k in range(1, 13) if "1" in str(k)]
    assert ones == [1, 10, 11, 12]
    its.append(mcq("Cards numbered 1 to 12 are shuffled. You pick one. What is the probability that the number has "
                   "the digit 1 in it?", fr(4, 12), [fr(3, 12), fr(1, 12), fr(5, 12)],
                   "The numbers with a 1 are 1, 10, 11 and 12: 4 of the 12 cards, so <b>" + fr(4, 12) + "</b>. "
                   + fr(3, 12) + " forgets the card 1. " + fr(5, 12) + " counts 11 twice, but it is only one card.",
                   ans=F(1, 3)))
    its.append(mcq("Which is more likely: landing on 4 on a spinner with 4 equal sections (1 to 4), or rolling a 4 on a "
                   "number cube (1 to 6)?", "landing on 4 on the spinner",
                   ["rolling a 4 on the number cube", "They are equally likely", "You can’t tell"],
                   "Spinner: " + fr(1, 4) + ". Number cube: " + fr(1, 6) + ". One part of 4 is bigger than one part of 6, "
                   "so <b>the spinner</b> is more likely."))
    assert F(1, 4) > F(1, 6)
    its.append(mcq("Bag A has 3 red and 1 blue marble. Bag B has 5 red and 5 blue marbles. Which bag gives a better "
                   "chance of taking red?", "Bag A", ["Bag B, it has more red marbles", "They are the same", "You can’t tell"],
                   "Bag A: " + fr(3, 4) + ". Bag B: " + fr(5, 10) + " = " + fr(1, 2) + ". " + fr(3, 4) + " is more than "
                   + fr(1, 2) + ", so <b>Bag A</b> is better, even though Bag B has more red marbles."))
    assert F(3, 4) > F(5, 10)
    its.append(mcq("A bag has 10 marbles. The probability of red is " + fr(2, 5) + ". How many red marbles are there?",
                   "4", ["2", "5", "6"],
                   fr(2, 5) + " = " + fr(4, 10) + ", so <b>4</b> of the 10 marbles are red. "
                   "2 uses the numerator without changing to tenths. 6 is the number that are not red.", ans=4))
    assert F(2, 5) * 10 == 4
    its.append(mcq("A bag has 3 green marbles and some blue marbles. The probability of green is " + fr(1, 4) +
                   ". How many blue marbles are there?", "9", ["12", "4", "1"],
                   fr(1, 4) + " = " + fr(3, 12) + ", so there are 12 marbles in total. 12 − 3 = <b>9</b> blue. "
                   "12 is the total, not the number of blue marbles.", ans=9))
    assert F(3, 3 + 9) == F(1, 4)
    bags = {"4 red, 4 blue": (4, 4), "5 red, 10 blue": (5, 10), "2 red, 4 blue": (2, 4), "3 red, 5 blue": (3, 5)}
    assert [k for k, (r, b) in bags.items() if F(r, r + b) == F(1, 2)] == ["4 red, 4 blue"]
    its.append(mcq("Which bag gives a probability of " + fr(1, 2) + " for taking a red marble?", "4 red, 4 blue",
                   ["5 red, 10 blue", "2 red, 4 blue", "3 red, 5 blue"],
                   fr(1, 2) + " means half of the marbles are red. With <b>4 red and 4 blue</b>, 4 of 8 are red. "
                   "2 red, 4 blue gives " + fr(2, 6) + ", not " + fr(2, 4) + "."))
    its.append(mcq("Mateo wants a spinner with 8 equal sections where the probability of green is " + fr(3, 4) +
                   ". How many sections should be green?", "6", ["3", "4", "2"],
                   fr(3, 4) + " = " + fr(6, 8) + ", so <b>6</b> of the 8 sections should be green. "
                   "3 uses the numerator without changing to eighths. 2 is the number that are not green.", ans=6))
    assert F(6, 8) == F(3, 4)
    return {"title": "Spinners, number cubes and bags", "items": its}


# ============================================================ set 4: theoretical and experimental probability
def set_experimental():
    its = []
    its.append(mcq("What is theoretical probability?", "What should happen, found by counting outcomes",
                   ["What happened when you did an experiment", "Always exactly the same as the experiment",
                    "Always " + fr(1, 2) + " for every event"],
                   "Theoretical probability is <b>what should happen</b>, found by counting the outcomes. "
                   "Experimental probability is what really happened in the trials."))
    its.append(mcq("Benjamin tosses a coin 20 times and gets 9 heads. What is the experimental probability of heads?",
                   fr(9, 20), [fr(9, 11), fr(1, 2), fr(11, 20)],
                   "Experimental probability = times it happened ÷ number of trials = <b>" + fr(9, 20) + "</b>. "
                   + fr(1, 2) + " is the theoretical probability. " + fr(9, 11) + " compares heads with tails.",
                   ans=F(9, 20)))
    its.append(mcq("Benjamin tosses a coin 20 times and gets 9 heads. What is the theoretical probability of heads?",
                   fr(1, 2), [fr(9, 20), fr(9, 11), fr(1, 20)],
                   "A coin has 2 equally likely sides, so the theoretical probability of heads is <b>" + fr(1, 2) + "</b>. "
                   + fr(9, 20) + " is the experimental probability.", ans=F(1, 2)))
    its.append(mcq(fig(freq_svg("20 spins", "Colour", ["red", "blue"], [12, 8], tally=False,
                                label="frequency table 20 spins")) +
                   "Priya’s class recorded 20 spins. What is the experimental probability of red?", fr(12, 20),
                   [fr(12, 8), fr(8, 20), fr(1, 2)],
                   "Red came up 12 times in 20 spins: <b>" + fr(12, 20) + "</b>. " + fr(12, 8) +
                   " compares red with blue and is greater than 1. " + fr(8, 20) + " is blue.", ans=F(12, 20)))
    vals = [18, 12, 10]
    assert sum(vals) == 40
    its.append(mcq(fig(freq_svg("40 spins", "Colour", ["red", "blue", "yellow"], vals, tally=False,
                                label="frequency table 40 spins")) +
                   "What is the experimental probability of yellow?", fr(10, 40), [fr(10, 30), fr(30, 40), fr(18, 40)],
                   "Yellow came up 10 times in 40 spins: <b>" + fr(10, 40) + "</b>. " + fr(10, 30) +
                   " compares yellow with the other 30 spins.", ans=F(10, 40)))
    vals = [15, 9, 6]
    assert sum(vals) == 30
    its.append(mcq(fig(freq_svg("Sofia’s 30 spins", "Colour", ["green", "red", "yellow"], vals, tally=True,
                                label="frequency table tally 30 spins")) +
                   "What is the experimental probability of red?", fr(9, 30), [fr(9, 21), fr(1, 3), fr(6, 30)],
                   "Red came up 9 times in 30 spins: <b>" + fr(9, 30) + "</b>. " + fr(9, 21) +
                   " compares red with the other 21 spins. " + fr(1, 3) + " would be the theory for 3 equal colours.",
                   ans=F(9, 30)))
    its.append(mcq("Leah rolls a number cube 30 times and gets a 6 on 7 rolls. What is the experimental probability "
                   "of rolling a 6?", fr(7, 30), [fr(1, 6), fr(7, 23), fr(6, 30)],
                   "A 6 came up 7 times in 30 rolls: <b>" + fr(7, 30) + "</b>. " + fr(1, 6) +
                   " is the theoretical probability. " + fr(6, 30) + " uses the number on the face.", ans=F(7, 30)))
    its.append(mcq("Lucas spins a spinner with 3 equal sections (red, blue, yellow) 30 times. Red comes up 11 times. "
                   "Which is true?", "Experimental: " + fr(11, 30) + ", theoretical: " + fr(1, 3),
                   ["Experimental: " + fr(1, 3) + ", theoretical: " + fr(11, 30),
                    "Experimental: " + fr(11, 19) + ", theoretical: " + fr(1, 3),
                    "Both are " + fr(11, 30)],
                   "The experiment gave red 11 times in 30 spins: " + fr(11, 30) + ". The theory says 1 of 3 equal "
                   "sections: " + fr(1, 3) + ". So <b>experimental " + fr(11, 30) + ", theoretical " + fr(1, 3) + "</b>. "
                   "They are close, because " + fr(1, 3) + " = " + fr(10, 30) + "."))
    assert F(1, 3) == F(10, 30)
    its.append(mcq("Which result gives an experimental probability of heads that is exactly the same as the "
                   "theoretical probability?", "10 heads in 20 tosses",
                   ["10 heads in 10 tosses", "2 heads in 10 tosses", "12 heads in 20 tosses"],
                   "The theory says " + fr(1, 2) + ". <b>10 heads in 20 tosses</b> gives " + fr(10, 20) + " = " + fr(1, 2) +
                   ". 10 heads in 10 tosses would be " + fr(10, 10) + " = 1."))
    assert F(10, 20) == F(1, 2) and F(12, 20) != F(1, 2)
    its.append(mcq("Noah tosses a coin 20 times. Which result is impossible?", "21 heads",
                   ["20 heads", "0 heads", "13 heads"],
                   "He only tosses 20 times, so he can’t get <b>21 heads</b>. 0 heads or 20 heads are very unlikely, "
                   "but they can happen."))
    its.append(mcq("Kai rolls a number cube 12 times. According to the theory, about how many times should he roll a 5?",
                   "about 2", ["about 5", "about 6", "about 12"],
                   "A 5 has a probability of " + fr(1, 6) + ". 12 ÷ 6 = 2, so <b>about 2</b> times. "
                   "About 5 uses the number on the face."))
    assert F(1, 6) * 12 == 2
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red one quarter blue")) +
                   "Aiden spins this spinner 40 times and gets blue 13 times. How does this compare with the theory?",
                   "Close: the theory says about 10",
                   ["Far off: the theory says about 20", "Far off: the theory says about 4", "Exactly right: the theory says 13"],
                   "Blue is " + fr(1, 4) + " of the spinner. 40 ÷ 4 = 10, and 13 is <b>close to 10</b>. "
                   "About 20 comes from thinking 2 colours means " + fr(1, 2) + "."))
    assert part(sp, "blue") * 40 == 10
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A number cube rolled 60 times", "Number", ["1", "2", "3", "4", "5", "6"], vals,
                                tally=False, label="frequency table number cube")) +
                   "How do these results compare with the theory?",
                   "Close: each number should come up about 10 times",
                   ["The number cube must be unfair", "5 is the most likely number", "4 will come up more next time"],
                   "Theory: " + fr(1, 6) + " of 60 = 10 for each number. The results are all between 8 and 12, which is "
                   "<b>close to the theory</b>. Small differences are normal."))
    its.append(mcq("Mei spins a spinner that is half red 10 times. Red comes up only 3 times. What does this show?",
                   "Not much: a few spins can be far from the theory",
                   ["The spinner must be broken", "Red should come up exactly 5 times", "The theory must be " + fr(3, 10)],
                   "The theory says about 5 reds in 10 spins, but with only 10 spins luck changes the results a lot. "
                   "<b>A few spins can be far from the theory.</b> She should do many more spins."))
    its.append(mcq("Ava tosses a coin 10 times and gets 7 heads. Ethan tosses a coin 200 times and gets 104 heads. "
                   "Whose results are closer to the theory?", "Ethan’s", ["Ava’s", "They are equally close", "Neither"],
                   "Half of 10 is 5, and Ava got 7: 2 more than half out of only 10. Half of 200 is 100, and Ethan got 104: "
                   "only 4 more out of 200. " + fr(104, 200) + " is very close to " + fr(1, 2) + ", so <b>Ethan’s</b> "
                   "results are closer."))
    assert abs(F(104, 200) - F(1, 2)) < abs(F(7, 10) - F(1, 2))
    its.append(mcq("Why are Ethan’s results (200 tosses) closer to the theory than Ava’s (10 tosses)?",
                   "More trials usually get closer to the theory",
                   ["Ethan tossed the coin more carefully", "Ava’s coin must be unfair",
                    "Big experiments are always exactly right"],
                   "With only a few trials, luck changes the results a lot. <b>More trials usually get closer</b> "
                   "to the theoretical probability, but not exactly."))
    its.append(mcq("Before each ringette game, a coin is tossed to decide which team starts. Tails has come up "
                   "5 games in a row. What is the probability of heads at the next game?",
                   fr(1, 2), [fr(5, 6), fr(1, 6), "1"],
                   "The coin has no memory. Every toss is a new trial, so heads is still <b>" + fr(1, 2) + "</b>. "
                   "Heads is not “due” after a lot of tails.", ans=F(1, 2)))
    its.append(mcq("Jayden has rolled a number cube 12 times without getting a 6. What is the probability of a 6 "
                   "on the next roll?", fr(1, 6), ["1", fr(2, 6), fr(1, 12)],
                   "The number cube does not remember earlier rolls. A 6 is still <b>" + fr(1, 6) + "</b>. "
                   "It is not certain (1), even after a long wait.", ans=F(1, 6)))
    its.append(mcq("Three groups spin the same spinner 20 times each. Red comes up 9, 13 and 8 times. "
                   "Use all the results to find the experimental probability of red.", fr(30, 60),
                   [fr(9, 20), fr(13, 20), fr(30, 20)],
                   "Add the results: 9 + 13 + 8 = 30 reds in 20 + 20 + 20 = 60 spins: <b>" + fr(30, 60) + "</b>. "
                   "Using all 60 spins gives a better estimate than one group. " + fr(30, 20) + " is greater than 1.",
                   ans=F(1, 2)))
    assert 9 + 13 + 8 == 30
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. At the fall fair, red comes up 98 times "
                   "in 200 spins. What do the results suggest?", "The spinner is probably not fair",
                   ["The spinner is fair", "Red will stop coming up soon", "200 spins are too few to tell"],
                   "Theory: " + fr(1, 4) + " of 200 = 50 reds. 98 is almost double that, after many spins, so "
                   "<b>the spinner is probably not fair</b>."))
    assert F(1, 4) * 200 == 50
    return {"title": "Theoretical and experimental probability", "items": its}


# ============================================================ set 5: predictions and fair games
def set_predict():
    its = []
    its.append(mcq("Liam rolls a number cube 60 times. About how many times should he expect to roll a 6?", "about 10",
                   ["about 6", "about 1", "about 30"],
                   "A 6 has a probability of " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10, so <b>about 10</b>. "
                   "About 6 uses the number on the face."))
    assert F(1, 6) * 60 == 10
    its.append(mcq("Zoe tosses a coin 100 times. How many heads should she expect?", "about 50",
                   ["exactly 50", "about 100", "about 2"],
                   "Half of 100 is 50. Results change from one experiment to the next, so expect <b>about 50</b>, "
                   "not exactly 50."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red one quarter blue")) +
                   "Chloe spins this spinner 40 times. About how many times should she expect red?", "about 30",
                   ["about 10", "about 20", "about 40"],
                   "Red is " + fr(3, 4) + " of the spinner. 40 ÷ 4 = 10, and 3 × 10 = 30, so <b>about 30</b>. "
                   "About 10 is for blue. About 20 thinks 2 colours means " + fr(1, 2) + "."))
    assert part(sp, "red") * 40 == 30
    its.append(mcq("A bag has 1 red and 4 blue marbles. Owen takes a marble, records the colour and puts it back. "
                   "He does this 50 times. About how many times should he get red?", "about 10",
                   ["about 12", "about 1", "about 40"],
                   "P(red) = " + fr(1, 5) + ". 50 ÷ 5 = 10, so <b>about 10</b>. About 12 uses " + fr(1, 4) +
                   " (red compared with blue). About 40 is for blue.", ))
    assert F(1, 5) * 50 == 10 and 50 // 4 == 12
    its.append(mcq("In a game, Emma wins if a coin lands on heads and Lucas wins if it lands on tails. Is the game fair?",
                   "Yes, each has a probability of " + fr(1, 2),
                   ["No, Emma is more likely to win", "No, Lucas is more likely to win", "You can’t tell"],
                   "A game is fair when every player has the same chance of winning. Heads and tails are each "
                   + fr(1, 2) + ", so <b>the game is fair</b>."))
    its.append(mcq("Maya and Arjun roll a number cube. Maya wins on 1 or 2. Arjun wins on 3, 4, 5 or 6. Is the game fair?",
                   "No, Arjun is more likely to win",
                   ["Yes, it is fair", "No, Maya is more likely to win", "Yes, both of them have numbers"],
                   "Maya: " + fr(2, 6) + ". Arjun: " + fr(4, 6) + ". The chances are not equal, so the game is not fair: "
                   "<b>Arjun is more likely to win</b>."))
    its.append(mcq("Kai wins if a number cube shows an even number. Which rule for Ethan makes the game fair?",
                   "Ethan wins on an odd number",
                   ["Ethan wins on a 1", "Ethan wins on a 5 or a 6", "Ethan wins on a number less than 6"],
                   "Kai has 2, 4, 6: " + fr(3, 6) + ". <b>Odd numbers</b> (1, 3, 5) are also " + fr(3, 6) + ", so the "
                   "game is fair. A 1 is only " + fr(1, 6) + ", and 5 or 6 is " + fr(2, 6) + "."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter green")) +
                   "Chloe wins if the spinner lands on red. Jayden wins if it lands on blue or green. Is the game fair?",
                   "Yes, each has a probability of " + fr(1, 2),
                   ["No, Jayden has 2 colours", "No, Chloe has the biggest section", "No, there are 3 colours"],
                   "Chloe: " + fr(1, 2) + ". Jayden: " + fr(1, 4) + " + " + fr(1, 4) + " = " + fr(1, 2) + ". "
                   "<b>Both have " + fr(1, 2) + "</b>, so the game is fair."))
    assert part(sp, "red") == part(sp, "blue") + part(sp, "green")
    its.append(mcq("A bag has 4 red and 2 blue marbles. Nathan wins on red and Sofia wins on blue. How many blue "
                   "marbles must be added to make the game fair?", "2", ["4", "6", "1"],
                   "For a fair game there must be as many blue as red: 4 blue. 4 − 2 = <b>2</b> more blue marbles. "
                   "4 is how many blue there should be in total, not how many to add.", ans=2))
    assert F(4, 8) == F(2 + 2, 8)
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
    its.append(mcq("Game A: you win if a spinner with 3 equal sections lands on red. Game B: you win if a number cube "
                   "shows 5 or 6. Which game gives a better chance of winning?", "They are the same",
                   ["Game A", "Game B, it has 2 winning numbers", "You can’t tell"],
                   "Game A: " + fr(1, 3) + ". Game B: " + fr(2, 6) + " = " + fr(1, 3) + ". "
                   "<b>The chances are the same.</b>"))
    assert F(1, 3) == F(2, 6)
    its.append(mcq("The weather forecast says snow is likely tomorrow in Winnipeg. Which fraction could be the "
                   "probability of snow?", fr(4, 5), [fr(1, 5), fr(1, 2), fr(5, 4)],
                   "Likely means between " + fr(1, 2) + " and 1, closer to 1: <b>" + fr(4, 5) + "</b>. " + fr(1, 5) +
                   " is unlikely, " + fr(1, 2) + " is equally likely, and " + fr(5, 4) + " is more than 1.", ans=F(4, 5)))
    its.append(mcq("Kai wins a sticker each time he rolls a 6 on a number cube. About how many times will he need to "
                   "roll to win about 5 stickers?", "about 30", ["about 11", "about 6", "about 5"],
                   "A 6 comes up about 1 time in every 6 rolls. 5 stickers need about 5 × 6 = <b>30</b> rolls. "
                   "About 11 comes from adding 5 + 6."))
    assert F(1, 6) * 30 == 5
    its.append(mcq("At hockey practice, Maya scores on 8 of her 20 shots. Next practice she takes 10 shots. "
                   "About how many goals should she expect?", "about 4", ["about 8", "about 2", "about 10"],
                   "Her experimental probability is " + fr(8, 20) + " = " + fr(4, 10) + ". So in 10 shots, expect "
                   "<b>about 4</b> goals. 8 was for 20 shots, not 10."))
    assert F(8, 20) * 10 == 4
    its.append(mcq("Ethan counts 40 cars passing the school. 14 of them are white. About how many of the next 20 cars "
                   "should be white?", "about 7", ["about 14", "about 6", "about 20"],
                   "20 cars is half of 40, so expect about half of 14: <b>about 7</b>. About 6 comes from 20 − 14."))
    assert F(14, 40) * 20 == 7
    its.append(mcq("There are 24 students in Ms. Leblanc’s class. 6 of them walk to school. The teacher picks one "
                   "name without looking. What is the probability that the student walks to school?", fr(6, 24),
                   [fr(6, 18), fr(18, 24), fr(1, 6)],
                   "6 of the 24 students walk: <b>" + fr(6, 24) + "</b> (= " + fr(1, 4) + "). " + fr(6, 18) +
                   " compares walkers with the other 18 students.", ans=F(1, 4)))
    its.append(mcq("A bag has 20 marbles. Sofia takes one, records its colour and puts it back. She does this 40 times "
                   "and gets red 10 times. About how many red marbles are in the bag?", "about 5",
                   ["about 10", "about 2", "about 20"],
                   "Red came up " + fr(10, 40) + " = " + fr(1, 4) + " of the time. " + fr(1, 4) + " of 20 is 5, so there "
                   "are <b>about 5</b> red marbles. 10 is how many times red came up, not how many are in the bag."))
    assert F(10, 40) * 20 == 5
    its.append(mcq("For the class Thanksgiving party, Mr. Singh makes 12 job cards, and 3 of them say “set up chairs”. Each "
                   "student picks a card and puts it back. If 24 students pick, about how many should get “set up chairs”?",
                   "about 6", ["about 3", "about 8", "about 12"],
                   "P(set up chairs) = " + fr(3, 12) + " = " + fr(1, 4) + ". " + fr(1, 4) + " of 24 is 24 ÷ 4 = "
                   "<b>about 6</b>. About 3 is the number of cards, not the expected number of students. About 8 comes from 24 ÷ 3."))
    assert F(3, 12) * 24 == 6
    return {"title": "Predictions and fair games: word problems", "items": its}


# ============================================================ lesson
def body_html():
    line = scale_svg(4, [], [(F(0), 0, 1), (F(1, 4), 1, 4), (F(1, 2), 1, 2), (F(3, 4), 3, 4), (F(1), 1, 1)],
                     words=True, label="probability line from impossible to certain")
    bag = bag_svg([("red", 3), ("blue", 5)], label="bag of 3 red and 5 blue marbles")
    sp = spinner_svg([("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")],
                     label="spinner half red quarter blue quarter yellow")
    return (
        "<h2>Probability as a fraction</h2>"
        "<p>Probability tells how likely something is to happen. When the outcomes are equally likely:</p>"
        "<p><b>probability = number of outcomes you want ÷ total number of outcomes</b></p>"
        "<figure class='sn-fig'>" + bag +
        "<figcaption>3 red and 5 blue marbles: 8 marbles in total.</figcaption></figure>"
        + ex("Example 1", "What is the probability of taking a red marble from this bag?",
             "There are 3 red marbles and 8 marbles altogether. Compare with all 8, not with the 5 blue.",
             fr(3, 8))
        + "<h2>The probability line</h2>"
        "<p>A probability is a number from <b>0</b> to <b>1</b>. 0 means impossible. 1 means certain. "
        "Halfway, " + fr(1, 2) + ", means equally likely to happen or not. A probability is never more than 1.</p>"
        "<figure class='sn-fig'>" + line +
        "<figcaption>Every probability has a place on this line.</figcaption></figure>"
        + ex("Example 2", "You roll a number cube with the numbers 1 to 6. Where does rolling a number greater than 4 go "
             "on the line?",
             "5 and 6 are greater than 4: 2 of the 6 outcomes. " + fr(2, 6) + " is less than " + fr(3, 6) + " = " + fr(1, 2) + ".",
             fr(2, 6) + ", between 0 and " + fr(1, 2) + ": unlikely")
        + "<h2>Spinners: look at the size of the parts</h2>"
        "<figure class='sn-fig'>" + sp +
        "<figcaption>3 colours, but the parts are not the same size.</figcaption></figure>"
        + ex("Example 3", "What is the probability of landing on red?",
             "Red covers half of the spinner. Do not count colours: 3 colours does not mean " + fr(1, 3) + " each.",
             fr(1, 2))
        + "<h2>Theoretical and experimental probability</h2>"
        "<p>The <b>theoretical</b> probability is what should happen, found by counting outcomes. "
        "The <b>experimental</b> probability is what did happen: number of times it happened ÷ number of trials. "
        "They are usually close, but rarely exactly the same. <b>More trials usually get closer.</b></p>"
        + table(["Coin tosses", "Heads", "Experimental probability"], [
            ["10", "7", fr(7, 10)],
            ["20", "9", fr(9, 20)],
            ["200", "104", fr(104, 200)],
        ])
        + ex("Example 4", "You roll a number cube 60 times. About how many 6s should you expect?",
             "A 6 has a probability of " + fr(1, 6) + ". " + fr(1, 6) + " of 60 is 60 ÷ 6 = 10.", "about 10")
        + "<h2>Fair games</h2>"
        "<p>A game is <b>fair</b> when every player has the same probability of winning. "
        "Win on even, lose on odd with a number cube: " + fr(3, 6) + " and " + fr(3, 6) + ", so it is fair.</p>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["3 red, 5 blue, so P(red) = " + fr(3, 5) + ".", "Compare with ALL the outcomes: " + fr(3, 8) + "."],
            ["3 colours, so each colour is " + fr(1, 3) + ".", "Look at the size of each part of the spinner."],
            ["“Less than 3” on a number cube is 1, 2 and 3.", "List the outcomes carefully: only 1 and 2."],
            ["“5 tails in a row, so heads is due.”", "A coin has no memory. Heads is still " + fr(1, 2) + "."],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about probability in the Ontario math curriculum?",
     "a": "In Grade 5 (Data, D2), students use fractions to describe the probability of an event, place it on a probability line from 0 to 1, and use it to make predictions and decisions. They also find and compare the theoretical and experimental probability of an event."},
    {"q": "How do you write a probability as a fraction?",
     "a": "Put the number of outcomes you want over the total number of outcomes. A bag with 3 red and 5 blue marbles gives a probability of 3/8 for red, not 3/5."},
    {"q": "What is a probability line?",
     "a": "A probability line is a number line from 0 (impossible) to 1 (certain), with 1/2 meaning equally likely. Students place a probability such as 3/4 on it to show how likely an event is."},
    {"q": "What is the difference between theoretical and experimental probability?",
     "a": "Theoretical probability is what should happen, found by counting outcomes. Experimental probability is what actually happened in trials, such as 9 heads in 20 tosses (9/20). With more trials, the two usually get closer."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (probability lines, rows of spinners, tables)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(45814)
    sets = [set_fraction(), set_line(), set_find(), set_experimental(), set_predict()]
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
        "country": "ca-on", "subject": "math", "grade": "grade-5", "slug": "probability", "sort": 14,
        "updated": UPDATED, "pdf_url": "",
        "title": "Probability: Fractions, the Probability Line, Experiments and Fair Games",
        "seo_title": "Grade 5 Probability Worksheets: Fractions, Probability Line and Experiments (Free, Answer Key)",
        "short_title": "Probability",
        "domain": "Data",
        "standard_code": "Grade 5: D2.1",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Use fractions to express the probability of events happening, represent this probability on a probability line, and use it to make predictions and informed decisions",
        "meta_desc": "Free Grade 5 math worksheets on probability for the Ontario curriculum: probability as a fraction, the probability line from 0 to 1, spinners, number cubes and bags, theoretical vs experimental probability, predictions and fair games. 100 questions with an answer key.",
        "key_big": "Probability = the outcomes you want ÷ all the outcomes. It is a fraction from 0 (impossible) to 1 (certain).",
        "key_sub": "3 red and 5 blue marbles: P(red) = 3/8, not 3/5. On a spinner, look at the size of each part, not the number of colours. More trials get closer to the theory.",
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
