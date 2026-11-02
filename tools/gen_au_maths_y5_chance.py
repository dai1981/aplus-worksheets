# -*- coding: utf-8 -*-
"""
AU Year 5 Maths: Chance
(Australian Curriculum v9.0, AC9M5P01 and AC9M5P02)
  python3 tools/gen_au_maths_y5_chance.py
Listing the possible outcomes of chance experiments (coin, dice, spinner, bag of marbles, cards), deciding whether
outcomes are equally likely (spinners with equal and unequal sections), comparing likelihoods (most likely, more likely
than, chance words), repeated experiments and frequency (results of 50 spins: which spinner was used?) and chance in
real life with light "1 out of 6" language. Probability as a fraction is Year 6, so it only appears as "out of".
Wrong answers come from real student mistakes: thinking all outcomes are always equally likely, counting sections or
colours instead of section sizes, the gambler's fallacy (after 5 heads, tails is "due"), listing duplicate outcomes,
expecting exact results, trusting very few trials.
Every spinner is drawn to its exact fractions; every answer is checked in code with fractions.Fraction.
Australian English. HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, math, os, random, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-5")
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


# ------------------------------------------------------------ helpers
OUTOF = re.compile(r"^(?:about )?(\d+) out of (\d+)$")


def mcq(q, correct, wrong, e):
    """4 choices: correct first + 3 wrong; positions are set later by balance()."""
    ch = [str(correct)] + [str(x) for x in wrong]
    assert len(ch) == 4, (q, ch)
    plain = [re.sub(r"<[^>]+>", "", x).strip() for x in ch]
    assert len(set(plain)) == 4, (q, ch)
    vals = [F(int(m.group(1)), int(m.group(2))) for m in (OUTOF.match(x) for x in plain) if m]
    assert len(set(vals)) == len(vals), ("two equal chances", q, ch)
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


# ------------------------------------------------------------ checks
def fit_score(spec, results):
    """How far the results are from what the spinner would give on average (smaller = better match)."""
    n = sum(v for _, v in results)
    p = {}
    for lab, f, _ in secs_of(spec):
        p[lab] = p.get(lab, 0) + f
    return sum((F(v) - n * p.get(c, 0)) ** 2 for c, v in results) + sum(
        (n * f) ** 2 for c, f in p.items() if c not in dict(results))


def best_spinner(specs, results):
    sc = [fit_score(sp, results) for sp in specs]
    best = min(sc)
    i = sc.index(best)
    assert sorted(sc)[1] >= best * 4 + 20, ("not a clear match", sc)
    return i


def part(spec, name):
    return sum((f for l, f, _ in secs_of(spec) if l == name), F(0))


# ============================================================ set 1: listing outcomes
def set_outcomes():
    its = []
    its.append(mcq("You toss a coin. Which list shows all the possible outcomes?", "heads, tails",
                   ["heads", "heads, heads, tails", "1 out of 2"],
                   "A coin can land on <b>heads</b> or <b>tails</b>. List each outcome once. "
                   "“1 out of 2” is the chance of one outcome, not a list of outcomes."))
    its.append(mcq("You roll a six-sided dice. How many possible outcomes are there?", "6", ["1", "7", "5"],
                   "The dice can land on 1, 2, 3, 4, 5 or 6. That is <b>6</b> outcomes. There is no 0 on a dice, so not 7. "
                   "Only one number comes up each roll, but there are 6 possible ones."))
    sp = [("1", F(1, 4), NUMFILL[0]), ("2", F(1, 4), NUMFILL[1]), ("3", F(1, 4), NUMFILL[2]), ("4", F(1, 4), NUMFILL[3])]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 to 4")) + "Which list shows all the possible outcomes of this spinner?",
                   "1, 2, 3, 4", ["1, 2, 3", "4", "1, 2, 3, 4, 5"],
                   "The spinner can land on any of its 4 numbers: <b>1, 2, 3, 4</b>. 5 is not on the spinner."))
    sp = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red blue red green")) + "Which list shows all the possible outcomes of this spinner?",
                   "red, blue, green", ["red, blue, red, green", "red, blue", "red, green"],
                   "Red appears twice, but it is still only one outcome. List it once: <b>red, blue, green</b>."))
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 2), ("yellow", 1)])) +
                   "A bag has 3 red, 2 blue and 1 yellow marble. You take one without looking. "
                   "Which list shows all the possible outcomes?",
                   "red, blue, yellow", ["red, red, red, blue, blue, yellow", "3, 2, 1", "red, blue"],
                   "The marble can be red, blue or yellow. Each colour is listed once: <b>red, blue, yellow</b>. "
                   "Yellow is possible, even though there is only 1."))
    its.append(mcq("A bag has 4 green and 4 white marbles. You take one without looking. How many different outcomes are there?",
                   "2", ["8", "4", "1"],
                   "The outcome is a colour, so there are <b>2</b> outcomes: green or white. 8 is the number of marbles."))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("green", F(1, 8), "green"), ("red", F(1, 8), "red"),
          ("blue", F(1, 8), "blue"), ("red", F(1, 8), "red"), ("green", F(1, 8), "green"), ("blue", F(1, 8), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner with 8 sections")) +
                   "This spinner has 8 sections. How many different outcomes are there?",
                   "3", ["8", "2", "1"],
                   "Count the different colours, not the sections: red, blue and green. That is <b>3</b> outcomes."))
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one card. How many possible outcomes are there?",
                   "10", ["9", "11", "1"],
                   "Any card from 1 to 10 can be picked: that is <b>10</b> outcomes. There is no card 0, so not 11."))
    its.append(mcq("The letters of the word KOALA are written on 5 cards. You pick one card. "
                   "Which list shows all the different possible outcomes?",
                   "K, O, A, L", ["K, O, A, L, A", "K, O, L", "A"],
                   "KOALA has 5 letters, but A appears twice. The different outcomes are <b>K, O, A, L</b>."))
    its.append(mcq("You roll a six-sided dice. Which number is NOT a possible outcome?", "7", ["1", "6", "4"],
                   "A dice shows 1 to 6. <b>7</b> can never come up."))
    sp = [("2", F(1, 4), NUMFILL[0]), ("4", F(1, 4), NUMFILL[1]), ("6", F(1, 4), NUMFILL[2]), ("8", F(1, 4), NUMFILL[3])]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 2 4 6 8")) + "Which outcome is impossible on this spinner?",
                   "an odd number", ["an even number", "a number less than 5", "8"],
                   "The numbers are 2, 4, 6 and 8. They are all even, so <b>an odd number</b> is impossible. "
                   "2 and 4 are less than 5, so that is possible."))
    its.append(mcq("You toss a 10c coin and a 20c coin. H means heads and T means tails. "
                   "Which list shows all the possible outcomes? (Write the 10c coin first.)",
                   "HH, HT, TH, TT", ["HH, HT, TT", "HH, TT", "HT, TH"],
                   "The 10c coin can be H or T, and so can the 20c coin. HT (10c heads, 20c tails) and TH (10c tails, "
                   "20c heads) are different. So there are 4: <b>HH, HT, TH, TT</b>."))
    its.append(mcq("You roll a six-sided dice. Which list shows all the even outcomes?", "2, 4, 6",
                   ["2, 4", "1, 3, 5", "2, 4, 6, 8"],
                   "The even numbers on a dice are <b>2, 4, 6</b>. 1, 3, 5 are odd, and 8 is not on a dice."))
    its.append(mcq("You roll a six-sided dice. Which list shows all the outcomes greater than 4?", "5, 6",
                   ["4, 5, 6", "5", "6"],
                   "Greater than 4 means bigger than 4, so 4 is not included: <b>5, 6</b>."))
    its.append(mcq("Which experiment has exactly 2 possible outcomes?", "tossing a coin",
                   ["rolling a dice", "picking a day of the week", "spinning a spinner with 1 to 4"],
                   "A coin has 2 outcomes: heads or tails. A dice has 6, the days of the week 7 and the spinner 4. "
                   "So the answer is <b>tossing a coin</b>."))
    its.append(mcq("Which experiment has 7 possible outcomes?", "picking a day of the week",
                   ["rolling a dice", "picking a month of the year", "tossing a coin"],
                   "There are 7 days in a week, so <b>picking a day of the week</b> has 7 outcomes. "
                   "A dice has 6, the months 12 and a coin 2."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red")) + "Which list shows all the possible outcomes of this spinner?",
                   "red, blue, yellow", ["red, red, blue, yellow", "red", "red, blue"],
                   "Red is bigger, but it is still one outcome. Blue and yellow are possible too: <b>red, blue, yellow</b>. "
                   "The size of a section changes the chance, not the list of outcomes."))
    its.append(mcq("Mia rolls a dice and gets a 6. Which list shows all the possible outcomes of her next roll?",
                   "1, 2, 3, 4, 5, 6", ["1, 2, 3, 4, 5", "6", "1"],
                   "The dice does not remember the last roll. All six numbers are possible again: <b>1, 2, 3, 4, 5, 6</b>."))
    sp = [(str(k), F(1, 8), NUMFILL[k - 1]) for k in range(1, 9)]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 to 8")) +
                   "Which list shows all the outcomes on this spinner that are multiples of 3?",
                   "3, 6", ["3, 6, 9", "3", "6"],
                   "The multiples of 3 up to 8 are <b>3 and 6</b>. 9 is a multiple of 3, but it is not on the spinner."))
    its.append(mcq("A bag has 2 red, 1 blue and 1 green marble. Isla says the possible outcomes are “red, red, blue, green”. "
                   "What is her mistake?",
                   "She listed red twice", ["She forgot yellow", "She needs 4 colours", "Nothing, she is right"],
                   "Each outcome is listed only once, so the list is red, blue, green. <b>She listed red twice.</b> "
                   "There is no yellow marble."))
    order = [0, 1, 9, 2, 14, 3, 5, 7, 15, 12, 13, 10, 16, 4, 6, 8, 17, 18, 11, 19]
    return {"title": "Listing possible outcomes", "items": reorder(its, order)}


# ============================================================ set 2: equally likely or not
def set_equal():
    its = []
    sp = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("green", F(1, 4), "green")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner four equal")) + "Are the 4 colours on this spinner equally likely?",
                   "Yes, the 4 sections are the same size",
                   ["No, red is at the top, so it is more likely", "No, green is the least likely", "You can’t tell without spinning"],
                   "Each colour has one quarter of the spinner. Equal sections give <b>equally likely</b> outcomes. "
                   "Where a section is does not matter."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner half red quarter blue quarter yellow")) +
                   "Are the outcomes on this spinner equally likely?",
                   "No, red has the biggest section",
                   ["Yes, there are 3 colours, so each is the same", "Yes, every spin is random", "No, yellow has the biggest section"],
                   "Red covers half the spinner. Blue and yellow cover a quarter each. So <b>red is more likely</b>. "
                   "Having 3 colours does not make them equally likely."))
    its.append(mcq("You toss a fair coin. Are heads and tails equally likely?", "Yes, each is 1 out of 2",
                   ["No, heads is more likely", "No, tails is more likely", "Only if you toss it twice"],
                   "A fair coin has 2 outcomes with the same chance: heads <b>1 out of 2</b>, tails 1 out of 2."))
    its.append(mcq("You roll a fair six-sided dice. Which statement is true?", "Every number is equally likely",
                   ["6 is the hardest to roll", "1 is the easiest to roll", "Even numbers are more likely than odd"],
                   "Each face has the same chance, 1 out of 6. So <b>every number is equally likely</b>. "
                   "6 feels hard to get only because people want it."))
    its.append(mcq(fig(bag_svg([("red", 3), ("blue", 3)])) + "You take a marble without looking. Are red and blue equally likely?",
                   "Yes, there are 3 of each", ["No, red is more likely", "No, blue is more likely", "You can’t tell"],
                   "There are 3 red and 3 blue marbles. The same number gives the same chance, so they are <b>equally likely</b>."))
    its.append(mcq(fig(bag_svg([("red", 5), ("blue", 2)])) + "You take a marble without looking. Are red and blue equally likely?",
                   "No, there are more red marbles",
                   ["Yes, there are 2 colours", "No, blue is more likely", "Yes, you only take 1 marble"],
                   "5 red and 2 blue: red has more marbles, so red is more likely. <b>Not equally likely.</b> "
                   "Two colours does not mean a 1 out of 2 chance each."))
    sp = [("red", F(1, 6), "red"), ("blue", F(1, 6), "blue")] * 3
    its.append(mcq(fig(spinner_svg(sp, label="spinner red blue alternating")) + "Are red and blue equally likely on this spinner?",
                   "Yes, each has 3 of the 6 sections",
                   ["No, red is at the top", "No, there are 6 sections", "No, blue is more likely"],
                   "The 6 sections are the same size. Red has 3 and blue has 3, so they are <b>equally likely</b>."))
    sp = [("red", F(1, 6), "red"), ("red", F(1, 6), "red"), ("blue", F(1, 6), "blue"), ("red", F(1, 6), "red"),
          ("red", F(1, 6), "red"), ("blue", F(1, 6), "blue")]
    assert part(sp, "red") == F(4, 6)
    its.append(mcq(fig(spinner_svg(sp, label="spinner four red two blue")) + "Are red and blue equally likely on this spinner?",
                   "No, red has 4 of the 6 sections",
                   ["Yes, the sections are the same size", "Yes, there are 2 colours", "No, blue is more likely"],
                   "The sections are equal, but red has 4 of them and blue only 2. So red is more likely: "
                   "<b>not equally likely</b>."))
    A = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("green", F(1, 4), "green")]
    B = [("red", F(1, 3), "red"), ("blue", F(1, 3), "blue"), ("green", F(1, 3), "green")]
    C = [("red", F(2, 3), "red"), ("blue", F(1, 6), "blue"), ("green", F(1, 6), "green")]
    D = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("red", F(1, 4), "red"), ("green", F(1, 4), "green")]
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "Which spinner has equally likely outcomes?",
                         ["A", "B", "C", "D"], 1,
                         "On spinner <b>B</b> red, blue and green each cover one third. On D the sections are equal, "
                         "but red has 2 of them, so red is more likely."))
    A = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"), ("green", F(1, 4), "green")]
    B = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    C = [("red", F(1, 2), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 6), "yellow")]
    D = [("red", F(1, 6), "red"), ("blue", F(1, 6), "blue"), ("yellow", F(1, 6), "yellow")] * 2
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "Which spinner does NOT have equally likely outcomes?",
                         ["A", "B", "C", "D"], 2,
                         "On spinner <b>C</b> the sections are different sizes: red is half, yellow is only one sixth. "
                         "On D each colour has 2 of the 6 equal sections, so they are equally likely."))
    sp = [("1", F(1, 2), NUMFILL[0]), ("2", F(1, 4), NUMFILL[1]), ("3", F(1, 4), NUMFILL[2])]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 2 3 unequal")) +
                   "Liam says each number on this spinner has a 1 out of 3 chance. Is he right?",
                   "No, 1 has a bigger section", ["Yes, there are 3 numbers", "No, 3 is the most likely", "Yes, all spinners are fair"],
                   "1 covers half of the spinner, but 2 and 3 only cover a quarter each. "
                   "<b>No</b>: 1 is more likely than 2 or 3."))
    its.append(mcq("You roll a six-sided dice. Is an even number equally likely as an odd number?",
                   "Yes, there are 3 even and 3 odd numbers",
                   ["No, even is more likely", "No, odd is more likely", "No, there are more even numbers"],
                   "Even: 2, 4, 6. Odd: 1, 3, 5. Both have 3 outcomes, so they are <b>equally likely</b>."))
    its.append(mcq("You roll a six-sided dice. Is rolling a 6 equally likely as rolling a number less than 6?",
                   "No, there are 5 numbers less than 6",
                   ["Yes, each is one outcome", "Yes, all dice numbers are equally likely", "No, a 6 is more likely"],
                   "Less than 6 means 1, 2, 3, 4 or 5: that is 5 outcomes. A 6 is only 1 outcome. "
                   "So <b>less than 6 is much more likely</b>."))
    its.append(mcq(fig(bag_svg([("green", 4), ("yellow", 4), ("red", 2)])) +
                   "You take a marble without looking. Which two colours are equally likely?",
                   "green and yellow", ["green and red", "yellow and red", "all three colours"],
                   "There are 4 green and 4 yellow marbles, so <b>green and yellow</b> are equally likely. Red has only 2."))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 8), "yellow"), ("green", F(1, 8), "green")] * 2
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight equal two of each")) +
                   "Are the 4 colours on this spinner equally likely?",
                   "Yes, each has 2 of the 8 sections",
                   ["No, there are 8 sections", "No, the colours are split up", "You can’t tell"],
                   "The 8 sections are the same size, and each colour has 2 of them. So the colours are <b>equally likely</b>. "
                   "Splitting a colour into two parts does not change its chance."))
    sp = [("red", F(1, 8), "red"), ("blue", F(1, 8), "blue"), ("red", F(1, 8), "red"), ("yellow", F(1, 8), "yellow"),
          ("blue", F(1, 8), "blue"), ("red", F(1, 8), "red"), ("yellow", F(1, 8), "yellow"), ("blue", F(1, 8), "blue")]
    assert part(sp, "red") == part(sp, "blue") == F(3, 8) and part(sp, "yellow") == F(2, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner three red three blue two yellow")) +
                   "Which two colours on this spinner are equally likely?",
                   "red and blue", ["red and yellow", "blue and yellow", "all three colours"],
                   "Count the equal sections: red 3, blue 3, yellow 2. So <b>red and blue</b> are equally likely."))
    sp = [("red", F(1, 8), "red"), ("yellow", F(1, 4), "yellow"), ("blue", F(1, 4), "blue"), ("red", F(1, 8), "red"),
          ("yellow", F(1, 4), "yellow")]
    assert part(sp, "red") == part(sp, "blue") == F(1, 4)
    its.append(mcq(fig(spinner_svg(sp, label="spinner red split in two")) +
                   "Are red and blue equally likely on this spinner?",
                   "Yes, each covers a quarter of the spinner",
                   ["No, red has 2 sections, so it is more likely", "No, red has small sections, so it is less likely",
                    "No, blue is more likely"],
                   "Red has two small sections, each one eighth. Together they make one quarter, the same as blue. "
                   "So red and blue are <b>equally likely</b>. Compare the total size, not the number of pieces."))
    its.append(mcq("Cards numbered 1 to 10 are shuffled. Is picking an even card equally likely as picking an odd card?",
                   "Yes, there are 5 of each", ["No, even is more likely", "No, odd is more likely", "No, 10 is the biggest card"],
                   "Even: 2, 4, 6, 8, 10. Odd: 1, 3, 5, 7, 9. Both have 5 cards, so they are <b>equally likely</b>."))
    its.append(mcq("Charlotte wants a spinner where red, blue and yellow are equally likely. Which plan works?",
                   "3 sections, each one third of the spinner",
                   ["3 sections of any size", "red half, blue and yellow a quarter each", "6 equal sections: 4 red, 1 blue, 1 yellow"],
                   "Equally likely colours need the same amount of the spinner. <b>Three thirds</b> works. "
                   "Any size will not work: a big section is more likely."))
    its.append(mcq("A bag has 6 marbles: 2 red, 2 blue and 2 green. You take one without looking. Is each colour equally likely?",
                   "Yes, there are 2 of each colour",
                   ["No, there are 6 marbles", "No, red is more likely", "No, green is more likely"],
                   "Each colour has 2 of the 6 marbles, so the colours are <b>equally likely</b>."))
    order = [0, 2, 3, 4, 1, 5, 6, 7, 11, 13, 17, 19, 8, 10, 12, 14, 15, 9, 16, 18]
    return {"title": "Equally likely or not?", "items": reorder(its, order)}


# ============================================================ set 3: comparing likelihood
def set_compare():
    its = []
    bag = [("red", 6), ("blue", 3), ("yellow", 1)]
    its.append(mcq(fig(bag_svg(bag)) + "You take a marble without looking. Which colour are you most likely to get?",
                   "red", ["blue", "yellow", "They are all equally likely"],
                   "There are 6 red, 3 blue and 1 yellow. Red has the most marbles, so <b>red</b> is most likely."))
    its.append(mcq("A bag has 2 red, 7 blue and 5 green marbles. You take one without looking. Which colour are you least likely to get?",
                   "red", ["blue", "green", "They are all equally likely"],
                   "Red has the fewest marbles (2), so <b>red</b> is least likely. Blue is the most likely."))
    sp = [("red", F(1, 6), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 3), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red sixth blue half yellow third")) +
                   "Which colour is this spinner most likely to land on?",
                   "blue", ["red", "yellow", "They are all equally likely"],
                   "Blue covers half the spinner, the biggest part. So <b>blue</b> is most likely. "
                   "Red starts at the top, but that does not matter."))
    sp = [("1", F(1, 6), NUMFILL[0]), ("2", F(1, 6), NUMFILL[1]), ("3", F(1, 6), NUMFILL[2]),
          ("2", F(1, 6), NUMFILL[1]), ("3", F(1, 6), NUMFILL[2]), ("3", F(1, 6), NUMFILL[2])]
    assert part(sp, "3") == F(3, 6)
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 2 3 2 3 3")) + "Which number is this spinner most likely to land on?",
                   "3", ["1", "2", "They are all equally likely"],
                   "The 6 sections are equal. 1 has 1 section, 2 has 2 sections and 3 has 3 sections. So <b>3</b> is most likely."))
    sp = [("blue", F(1, 8), "blue"), ("red", F(1, 8), "red"), ("yellow", F(1, 8), "yellow"), ("blue", F(1, 8), "blue"),
          ("yellow", F(1, 8), "yellow"), ("red", F(1, 8), "red"), ("yellow", F(1, 8), "yellow"), ("blue", F(1, 8), "blue")]
    assert part(sp, "red") == F(2, 8) and part(sp, "blue") == part(sp, "yellow") == F(3, 8)
    its.append(mcq(fig(spinner_svg(sp, label="spinner eight sections two red")) + "Which colour is this spinner least likely to land on?",
                   "red", ["blue", "yellow", "They are all equally likely"],
                   "Count the equal sections: blue 3, yellow 3, red 2. <b>Red</b> has the least, so it is least likely."))
    its.append(mcq("You roll a six-sided dice. Which is more likely?", "an even number",
                   ["a 6", "They are equally likely", "You can’t tell"],
                   "An even number can be 2, 4 or 6: 3 outcomes. A 6 is only 1 outcome. So <b>an even number</b> is more likely."))
    its.append(mcq("You roll a six-sided dice. Which is more likely?", "a number greater than 3",
                   ["a number less than 3", "They are equally likely", "You can’t tell"],
                   "Greater than 3: 4, 5, 6 (3 outcomes). Less than 3: 1, 2 (2 outcomes). The 3 itself is in neither list. "
                   "So <b>greater than 3</b> is more likely."))
    its.append(mcq("Every section of a spinner is red. What is the chance it lands on red?", "certain",
                   ["likely", "unlikely", "impossible"],
                   "Red is the only colour, so the spinner must land on red. It is <b>certain</b>."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red")) + "What is the chance this spinner lands on blue?",
                   "unlikely", ["impossible", "certain", "likely"],
                   "Blue covers only one quarter. It can happen, but not often: <b>unlikely</b>. "
                   "It is not impossible, because blue is on the spinner."))
    its.append(mcq("A bag has 9 green marbles and 1 white marble. You take one without looking. What is the chance of green?",
                   "likely", ["certain", "unlikely", "impossible"],
                   "9 of the 10 marbles are green, so green is <b>likely</b>. It is not certain, because you could take the white one."))
    its.append(mcq("A bag has only red and blue marbles. What is the chance of taking a yellow marble?", "impossible",
                   ["unlikely", "likely", "certain"],
                   "There are no yellow marbles in the bag, so yellow is <b>impossible</b>."))
    A = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    B = [("red", F(1, 3), "red"), ("blue", F(2, 3), "blue")]
    C = [("red", F(1, 4), "red"), ("blue", F(3, 4), "blue")]
    D = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    reds = [part(x, "red") for x in (A, B, C, D)]
    assert reds.index(max(reds)) == 3
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "Which spinner gives the best chance of landing on red?",
                         ["A", "B", "C", "D"], 3,
                         "Red covers three quarters of spinner <b>D</b>. That is more than half (A), one third (B) and one quarter (C)."))
    A = [("blue", F(1, 8), "blue"), ("yellow", F(7, 8), "yellow")]
    B = [("blue", F(1, 4), "blue"), ("yellow", F(3, 4), "yellow")]
    C = [("blue", F(1, 2), "blue"), ("yellow", F(1, 2), "yellow")]
    D = [("blue", F(1, 3), "blue"), ("yellow", F(2, 3), "yellow")]
    blues = [part(x, "blue") for x in (A, B, C, D)]
    assert blues.index(min(blues)) == 0
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) + "On which spinner is blue least likely?",
                         ["A", "B", "C", "D"], 0,
                         "Blue is the smallest on spinner <b>A</b>: only one eighth of the spinner."))
    its.append(mcq("Bag A has 3 red and 1 blue marble. Bag B has 3 red and 3 blue marbles. You want a red marble. Which bag should you choose?",
                   "Bag A", ["Bag B", "Both bags give the same chance", "You can’t tell"],
                   "Both bags have 3 red, but in Bag A they are 3 out of 4 marbles and in Bag B only 3 out of 6. "
                   "<b>Bag A</b> is better. Compare the red marbles with all the marbles."))
    its.append(mcq("Bag A has 2 red and 2 blue marbles. Bag B has 5 red and 5 blue marbles. You want a red marble. Which bag should you choose?",
                   "Both bags give the same chance", ["Bag B", "Bag A", "You can’t tell"],
                   "In both bags half the marbles are red. So the chance is the same: <b>both bags give the same chance</b>. "
                   "Bag B has more red marbles, but it also has more blue ones."))
    assert F(2, 4) == F(5, 10)
    its.append(mcq("Cards numbered 1 to 10 are shuffled. You pick one. Which is more likely?", "an even number",
                   ["a number greater than 7", "They are equally likely", "You can’t tell"],
                   "Even: 2, 4, 6, 8, 10 (5 cards). Greater than 7: 8, 9, 10 (3 cards). So <b>an even number</b> is more likely."))
    sp = [(str(k), F(1, 8), NUMFILL[k - 1]) for k in range(1, 9)]
    its.append(mcq(fig(spinner_svg(sp, label="spinner 1 to 8 equal")) + "Which is more likely on this spinner?",
                   "a number less than 4", ["a multiple of 4", "They are equally likely", "You can’t tell"],
                   "Less than 4: 1, 2, 3 (3 sections). Multiples of 4: 4, 8 (2 sections). "
                   "So <b>a number less than 4</b> is more likely."))
    its.append(mcq("A bag has 5 red, 2 blue and 3 green marbles. Which list orders the colours from least likely to most likely?",
                   "blue, green, red", ["red, green, blue", "green, blue, red", "blue, red, green"],
                   "Order the counts from smallest: blue 2, green 3, red 5. So <b>blue, green, red</b>. "
                   "“Red, green, blue” is most to least."))
    sp = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red half blue quarter yellow quarter")) +
                   "Kai says red is twice as likely as blue on this spinner. Is he right?",
                   "Yes, red’s part is twice as big", ["No, they are equally likely", "No, blue is twice as likely",
                                                       "No, red is 3 times as likely"],
                   "Red is one half and blue is one quarter. Half is two quarters, so red’s part is twice as big. "
                   "<b>Kai is right.</b>"))
    assert F(1, 2) == 2 * F(1, 4)
    its.append(mcq("You roll a six-sided dice. Which word best describes the chance of rolling a number from 1 to 6?",
                   "certain", ["likely", "unlikely", "even chance"],
                   "Every roll gives a number from 1 to 6, so it is <b>certain</b>."))
    sp = [("red", F(1, 3), "red"), ("blue", F(2, 3), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner red third blue two thirds")) + "Which statement about this spinner is true?",
                   "Blue is more likely than red", ["Red is more likely than blue", "Red and blue are equally likely",
                                                   "Red is impossible"],
                   "Blue covers two thirds and red one third. So <b>blue is more likely than red</b>. "
                   "Red is less likely, but not impossible."))
    assert len(its) == 21
    its.pop(19)  # keep 20: the dice "certain" item repeats set 2 ideas less than the others
    order = [0, 1, 7, 10, 9, 8, 2, 3, 19, 4, 5, 6, 15, 11, 12, 13, 14, 16, 17, 18]
    return {"title": "Comparing chances", "items": reorder(its, order)}


# ============================================================ set 4: repeated experiments
def set_experiments():
    its = []
    T = F(1, 3)
    A = [("red", T, "red"), ("blue", T, "blue"), ("yellow", T, "yellow")]
    B = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    C = [("red", F(1, 4), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(1, 4), "yellow")]
    D = [("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 2), "yellow")]
    res = [("red", 26), ("blue", 12), ("yellow", 12)]
    assert sum(v for _, v in res) == 50 and best_spinner([A, B, C, D], res) == 1
    its.append(mcq_fixed(fig(spinners4_svg([A, B, C, D])) +
                         "Ruby spins one of these spinners 50 times. Her results: red 26, blue 12, yellow 12. "
                         "Which spinner did she most likely use?", ["A", "B", "C", "D"], 1,
                         "Red came up about half the time (26 of 50). Blue and yellow came up about a quarter of the time each. "
                         "That matches spinner <b>B</b>: red half, blue and yellow a quarter each."))
    A2 = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    B2 = [("red", F(1, 6), "red"), ("blue", F(1, 3), "blue"), ("yellow", F(1, 2), "yellow")]
    C2 = [("red", T, "red"), ("blue", T, "blue"), ("yellow", T, "yellow")]
    D2 = [("red", F(2, 3), "red"), ("blue", F(1, 6), "blue"), ("yellow", F(1, 6), "yellow")]
    res = [("red", 17), ("blue", 16), ("yellow", 17)]
    assert sum(v for _, v in res) == 50 and best_spinner([A2, B2, C2, D2], res) == 2
    its.append(mcq_fixed(fig(spinners4_svg([A2, B2, C2, D2])) +
                         "Oliver spins one of these spinners 50 times. His results: red 17, blue 16, yellow 17. "
                         "Which spinner did he most likely use?", ["A", "B", "C", "D"], 2,
                         "The three colours came up about the same number of times. So the colours are probably equally likely: "
                         "spinner <b>C</b>, with three equal thirds."))
    A3 = [("red", F(1, 2), "red"), ("blue", F(1, 2), "blue")]
    B3 = [("red", F(1, 4), "red"), ("blue", F(3, 4), "blue")]
    C3 = [("red", F(1, 3), "red"), ("blue", F(2, 3), "blue")]
    D3 = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    res = [("red", 38), ("blue", 12)]
    assert best_spinner([A3, B3, C3, D3], res) == 3
    its.append(mcq_fixed(fig(spinners4_svg([A3, B3, C3, D3])) +
                         "Chloe spins one of these spinners 50 times. Her results: red 38, blue 12. "
                         "Which spinner did she most likely use?", ["A", "B", "C", "D"], 3,
                         "Red came up much more often than blue: about 3 times as often. Spinner <b>D</b> is three quarters red. "
                         "On B, blue would win most of the time."))
    A4 = [("red", F(1, 8), "red"), ("blue", F(1, 2), "blue"), ("yellow", F(3, 8), "yellow")]
    B4 = [("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")]
    C4 = [("red", T, "red"), ("blue", T, "blue"), ("yellow", T, "yellow")]
    D4 = [("red", F(3, 8), "red"), ("blue", F(1, 8), "blue"), ("yellow", F(1, 2), "yellow")]
    res = [("red", 5), ("blue", 24), ("yellow", 21)]
    assert best_spinner([A4, B4, C4, D4], res) == 0
    its.append(mcq_fixed(fig(spinners4_svg([A4, B4, C4, D4])) +
                         "Noah spins one of these spinners 50 times. His results: red 5, blue 24, yellow 21. "
                         "Which spinner did he most likely use?", ["A", "B", "C", "D"], 0,
                         "Red came up only 5 times, so red is probably small. Blue came up about half the time. "
                         "That matches spinner <b>A</b>: red one eighth, blue half, yellow a bit less than half."))
    its.append(mcq("Jack tosses a coin 20 times. He gets 11 heads and 9 tails. What does this show?",
                   "Heads and tails came up about the same", ["The coin is unfair", "Heads is more likely next time",
                                                              "Tails must come up next"],
                   "With a fair coin you expect about 10 of each, but rarely exactly 10. 11 and 9 are close, so "
                   "<b>heads and tails came up about the same</b>."))
    its.append(mcq("A fair coin lands on heads 5 times in a row. What is the chance of tails on the next toss?",
                   "still 1 out of 2", ["more than 1 out of 2", "less than 1 out of 2", "certain"],
                   "The coin does not remember earlier tosses. Every toss is <b>still 1 out of 2</b> for tails. "
                   "Tails is not “due”."))
    its.append(mcq("Leo has not rolled a 6 in his last 10 rolls of a fair dice. On his next roll, a 6 is…",
                   "just as likely as before", ["more likely now", "certain now", "impossible"],
                   "Each roll is new. A 6 is 1 out of 6 every time, so it is <b>just as likely as before</b>."))
    cats = ["1", "2", "3", "4", "5", "6"]
    vals = [9, 11, 10, 8, 12, 10]
    assert sum(vals) == 60
    its.append(mcq(fig(freq_svg("A dice rolled 60 times", "Number", cats, vals, tally=False, label="frequency table dice")) +
                   "Which statement about these results is best?",
                   "Each number came up about 10 times",
                   ["5 is the most likely number on a dice", "The dice must be unfair", "4 will come up more next time"],
                   "60 rolls ÷ 6 numbers = about 10 each. The results are all close to 10, so "
                   "<b>each number came up about 10 times</b>. Small differences are normal."))
    cats = ["red", "blue", "green"]
    vals = [14, 4, 7]
    its.append(mcq(fig(freq_svg("25 spins", "Colour", cats, vals, label="frequency table spins")) +
                   "Which colour probably has the biggest section on the spinner?",
                   "red", ["blue", "green", "They are all the same"],
                   "Red came up most often (14 of 25 spins), so <b>red</b> probably has the biggest section."))
    vals = [6, 15, 9]
    its.append(mcq(fig(freq_svg("30 spins", "Colour", cats, vals, label="frequency table spins")) +
                   "Which colour probably has the smallest section on the spinner?",
                   "red", ["blue", "green", "They are all the same"],
                   "Red came up least often (6 of 30 spins), so <b>red</b> probably has the smallest section."))
    its.append(mcq("Mei spins a red and blue spinner 40 times. Red comes up 21 times and blue the rest. How many times does blue come up?",
                   "19", ["21", "61", "20"],
                   "40 − 21 = <b>19</b>. 61 comes from adding instead of subtracting."))
    assert 40 - 21 == 19
    its.append(mcq("You toss a fair coin 100 times. How many heads would you expect?", "about 50",
                   ["exactly 50", "exactly 100", "about 10"],
                   "Heads is 1 out of 2, and half of 100 is 50. Results change each time, so expect <b>about 50</b>, "
                   "not exactly 50."))
    its.append(mcq("You roll a fair dice 60 times. About how many times would you expect to roll a 3?", "about 10",
                   ["about 3", "about 20", "about 30"],
                   "A 3 is 1 out of 6. 60 ÷ 6 = 10, so <b>about 10</b>. About 30 would be half the rolls."))
    assert F(60, 6) == 10
    its.append(mcq("A spinner is half red and half blue. You spin it 40 times. About how many times would you expect red?",
                   "about 20", ["about 40", "about 10", "about 2"],
                   "Red is half of the spinner. Half of 40 is 20, so expect <b>about 20</b>."))
    sp = [("red", F(3, 4), "red"), ("blue", F(1, 4), "blue")]
    its.append(mcq(fig(spinner_svg(sp, label="spinner three quarters red")) +
                   "You spin this spinner 20 times. About how many times would you expect blue?",
                   "about 5", ["about 15", "about 10", "about 1"],
                   "Blue is one quarter of the spinner. 20 ÷ 4 = 5, so <b>about 5</b>. About 15 is for red. "
                   "About 10 would only be right if blue were half."))
    assert F(20, 4) == 5
    its.append(mcq("You want to find out how likely red is on a spinner. Which gives the better estimate?",
                   "100 spins", ["10 spins", "Both the same", "1 spin"],
                   "More spins give a better estimate. With only a few spins, luck changes the results a lot. "
                   "So <b>100 spins</b> is better."))
    its.append(mcq("Aarav spins a spinner 10 times and gets red 7 times. Zara spins the same spinner 200 times and gets red 104 times. "
                   "Whose results tell you more about the spinner?",
                   "Zara’s, because she spun more", ["Aarav’s, because red came up more", "Both the same", "Neither"],
                   "200 spins tell you much more than 10 spins. <b>Zara’s results</b> suggest red is about half the spinner."))
    its.append(mcq("Sienna rolls a dice 6 times and gets 2, 5, 2, 1, 2, 4. She says 2 is the most likely number on the dice. Is she right?",
                   "No, 6 rolls are too few to tell", ["Yes, 2 came up 3 times", "No, 6 is the most likely", "Yes, 3 and 6 are impossible"],
                   "On a fair dice every number is 1 out of 6. In only 6 rolls, some numbers come up more by luck. "
                   "<b>6 rolls are too few to tell.</b>"))
    its.append(mcq("A bag has 10 red and blue marbles. Cooper takes one, writes the colour and puts it back. He does this 50 times: "
                   "red 39, blue 11. What is most likely in the bag?",
                   "8 red, 2 blue", ["5 red, 5 blue", "2 red, 8 blue", "10 red, 0 blue"],
                   "Red came up about 4 times as often as blue. 8 red and 2 blue fits: red is 4 times as likely. "
                   "<b>8 red, 2 blue</b>. It can’t be 10 red, because blue came up 11 times."))
    exp = {(8, 2): 40, (5, 5): 25, (2, 8): 10}
    assert min(exp, key=lambda k: abs(exp[k] - 39)) == (8, 2)
    cats = ["red", "blue", "yellow"]
    vals = [9, 31, 10]
    assert sum(vals) == 50
    its.append(mcq(fig(freq_svg("50 spins", "Colour", cats, vals, label="frequency table spins")) +
                   "What do these results suggest about the spinner?",
                   "Blue is the most likely colour", ["All colours are equally likely", "Red will come up next",
                                                      "Yellow is impossible"],
                   "Blue came up 31 of 50 times, much more than red or yellow. So <b>blue is probably the most likely colour</b>. "
                   "Yellow came up 10 times, so it is not impossible."))
    order = [4, 5, 6, 10, 8, 9, 19, 7, 11, 12, 13, 14, 15, 16, 17, 0, 1, 2, 3, 18]
    return {"title": "Repeated experiments and frequency", "items": reorder(its, order)}


# ============================================================ set 5: chance in real life
def set_real():
    its = []
    its.append(mcq("The school fete raffle sells 100 tickets. Charlotte buys 1 ticket. One ticket wins. What is her chance of winning?",
                   "1 out of 100", ["1 out of 2", "1 out of 99", "100 out of 1"],
                   "1 of the 100 tickets is hers, so her chance is <b>1 out of 100</b>. "
                   "“Win or lose” is not 1 out of 2, because losing is much more likely."))
    its.append(mcq("The same raffle has 100 tickets. Matilda buys 5 tickets. What is her chance of winning?",
                   "5 out of 100", ["1 out of 100", "5 out of 95", "1 out of 5"],
                   "5 of the 100 tickets are hers, so her chance is <b>5 out of 100</b>. More tickets give a better chance."))
    its.append(mcq("Before a cricket match the captains toss a coin. One captain calls “heads”. Which words best describe the chance the call is right?",
                   "an even chance", ["likely", "unlikely", "certain"],
                   "Heads and tails are equally likely, 1 out of 2. That is <b>an even chance</b>."))
    its.append(mcq("A lucky dip at the school fete has 20 prizes. 4 of them are toy koalas. Grace takes one without looking. What is her chance of a toy koala?",
                   "4 out of 20", ["1 out of 20", "4 out of 16", "16 out of 20"],
                   "4 of the 20 prizes are koalas: <b>4 out of 20</b>. Compare with all 20 prizes, not with the 16 others. 16 out of 20 is the chance of NOT a koala."))
    its.append(mcq("A Year 5 class has 25 students. The teacher picks one name from a hat. What is the chance that Ethan is picked?",
                   "1 out of 25", ["1 out of 2", "1 out of 24", "24 out of 25"],
                   "Ethan’s name is 1 of the 25 names, so the chance is <b>1 out of 25</b>. 24 out of 25 is the chance he is NOT picked."))
    its.append(mcq("A class has 13 girls and 12 boys. One name is picked from a hat. Is a girl more likely than a boy?",
                   "Yes, but only a little", ["No, they are equally likely", "No, a boy is more likely", "Yes, a girl is certain"],
                   "13 girls and 12 boys: a girl is a little more likely. <b>Yes, but only a little.</b> It is not certain."))
    its.append(mcq("A netball team has 7 bibs: GS, GA, WA, C, WD, GD and GK. Isla takes one bib without looking. What is the chance she gets C?",
                   "1 out of 7", ["1 out of 6", "1 out of 2", "6 out of 7"],
                   "There are 7 bibs and 1 of them is C, so the chance is <b>1 out of 7</b>. 6 out of 7 is the chance of not C."))
    its.append(mcq("In a board game, Noah needs to roll a 5 or a 6 to win. What is his chance?", "2 out of 6",
                   ["1 out of 6", "5 out of 6", "2 out of 5"],
                   "2 numbers (5 and 6) out of the 6 numbers on a dice: <b>2 out of 6</b>."))
    its.append(mcq("Amelia needs to roll more than 1 on a dice to move her counter. Which word best describes her chance?",
                   "likely", ["certain", "unlikely", "impossible"],
                   "More than 1 means 2, 3, 4, 5 or 6: 5 out of 6. That is <b>likely</b>, but not certain, because she could roll a 1."))
    its.append(mcq("Harper tosses a coin. It lands on tails 6 times in a row. She says, “Heads must come next.” Is she right?",
                   "No, heads is still 1 out of 2", ["Yes, heads is due", "No, tails is more likely now", "Yes, it is certain"],
                   "Each toss is new and the coin does not remember. <b>Heads is still 1 out of 2.</b>"))
    its.append(mcq("A jar has 12 lollies: 6 orange, 4 lime and 2 lemon. Kai takes one without looking. Which flavour is he least likely to get?",
                   "lemon", ["orange", "lime", "They are all equally likely"],
                   "Lemon has the fewest lollies (2), so <b>lemon</b> is least likely."))
    its.append(mcq("The jar has 6 orange, 4 lime and 2 lemon lollies. What is the chance of an orange lolly?",
                   "6 out of 12", ["1 out of 3", "6 out of 6", "1 out of 12"],
                   "6 of the 12 lollies are orange: <b>6 out of 12</b>, an even chance. 1 out of 3 would only be right "
                   "if the 3 flavours were equally likely."))
    sp = [("WIN", F(1, 8), "yellow")] + [("", F(1, 8), "grey")] * 7
    its.append(mcq(fig(spinner_svg(sp, R=80, label="spinner with one win section")) +
                   "A spinner game at the school fair has 8 equal sections. One says WIN. What is the chance of winning on one spin?",
                   "1 out of 8", ["1 out of 2", "7 out of 8", "1 out of 7"],
                   "1 of the 8 equal sections is WIN, so the chance is <b>1 out of 8</b>."))
    its.append(mcq("Ava makes a spinner with 4 equal parts. She wants red to be likely and blue to be unlikely. Which plan works?",
                   "3 red parts and 1 blue part", ["1 red part and 3 blue parts", "2 red parts and 2 blue parts",
                                                   "4 red parts and 0 blue parts"],
                   "<b>3 red and 1 blue</b> makes red likely and blue unlikely. With 0 blue parts, blue would be impossible."))
    its.append(mcq("Sienna picks a day of the week at random. What is the chance it is Saturday or Sunday?", "2 out of 7",
                   ["1 out of 7", "2 out of 5", "1 out of 2"],
                   "There are 7 days and 2 of them are on the weekend: <b>2 out of 7</b>. 2 out of 5 compares the weekend "
                   "with the 5 school days, not with all 7."))
    its.append(mcq("A bag has 3 red marbles and some blue marbles. Red and blue are equally likely. How many blue marbles are there?",
                   "3", ["6", "1", "You can’t tell"],
                   "Equally likely means the same number of each colour. So there are <b>3</b> blue marbles."))
    its.append(mcq("A bag has 2 green and 3 yellow marbles. William wants green to be MORE likely than yellow. "
                   "What is the smallest number of green marbles he must add?",
                   "2", ["1", "3", "5"],
                   "Add 1: 3 green and 3 yellow are only equally likely. Add <b>2</b>: 4 green beats 3 yellow."))
    assert 2 + 1 == 3 and 2 + 2 > 3
    its.append(mcq("A special dice has the numbers 1, 1, 2, 2, 3, 3 on its faces. What is the chance of rolling a 3?",
                   "2 out of 6", ["1 out of 6", "3 out of 6", "2 out of 3"],
                   "Two of the 6 faces show a 3, so the chance is <b>2 out of 6</b>. 3 out of 6 comes from using the "
                   "number 3 instead of counting faces."))
    its.append(mcq("The school canteen has a box of 30 muffins: 10 blueberry and 20 chocolate. Mia takes one without looking. "
                   "Which statement is true?",
                   "Chocolate is more likely than blueberry", ["Blueberry is more likely than chocolate",
                                                               "They are equally likely", "Chocolate is certain"],
                   "There are 20 chocolate and only 10 blueberry, so <b>chocolate is more likely</b>. It is not certain, "
                   "because there are blueberry muffins too."))
    its.append(mcq("At the athletics carnival, tickets numbered 1 to 30 go in a hat for a prize. Which is more likely: a number from 1 to 10, "
                   "or a number from 21 to 30?",
                   "They are equally likely", ["1 to 10", "21 to 30", "You can’t tell"],
                   "Each group has 10 tickets, and every ticket has the same chance. So they are <b>equally likely</b>. "
                   "Bigger numbers are not harder to pick."))
    order = [2, 0, 1, 4, 3, 6, 7, 8, 10, 12, 11, 14, 5, 9, 17, 18, 13, 19, 15, 16]
    return {"title": "Chance in real life", "items": reorder(its, order)}


# ============================================================ lesson
def body_html():
    eq = spinner_svg([("red", F(1, 4), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow"),
                      ("green", F(1, 4), "green")], R=70, label="spinner four equal")
    uneq = spinner_svg([("red", F(1, 2), "red"), ("blue", F(1, 4), "blue"), ("yellow", F(1, 4), "yellow")], R=70,
                       label="spinner half red")
    return (
        "<h2>Outcomes</h2>"
        "<p>A chance experiment is something like tossing a coin, rolling a dice or spinning a spinner. "
        "An <b>outcome</b> is one thing that can happen. List each outcome <b>once</b>.</p>"
        "<figure class='sn-fig'>" + dice_row_svg() +
        "<figcaption>A dice has 6 possible outcomes: 1, 2, 3, 4, 5 and 6.</figcaption></figure>"
        + ex("Example", "A bag has 3 red marbles and 2 blue marbles. You take one. List the possible outcomes.",
             "The marble can only be red or blue. Red is listed once, even though there are 3 red marbles.", "red, blue")
        + "<h2>Equally likely or not?</h2>"
        "<p>Outcomes are <b>equally likely</b> when they have the same chance. On a spinner, look at the <b>size</b> of each "
        "colour, not just the number of colours.</p>"
        "<figure class='sn-fig'>" + eq +
        "<figcaption>4 equal sections: each colour is equally likely, 1 out of 4.</figcaption></figure>"
        "<figure class='sn-fig'>" + uneq +
        "<figcaption>Red covers half, so red is more likely than blue or yellow. Not equally likely.</figcaption></figure>"
        "<h2>Chance words</h2>"
        + table(["Word", "Meaning", "Example"], [
            ["certain", "will happen", "rolling a number from 1 to 6"],
            ["likely", "will happen most of the time", "rolling more than 1"],
            ["even chance", "1 out of 2", "a coin landing on heads"],
            ["unlikely", "can happen, but not often", "rolling a 6"],
            ["impossible", "can never happen", "rolling a 7"],
        ])
        + "<h2>Repeated experiments</h2>"
        "<p>Do an experiment many times and record the results in a frequency table. The outcome that comes up most "
        "is probably the most likely. <b>More trials give a better estimate.</b></p>"
        + table(["Colour", "Frequency (50 spins)"], [["red", "26"], ["blue", "12"], ["yellow", "12"]])
        + ex("Which spinner?", "The results above came from one spinner. Which one is it: equal thirds, or red half and "
             "blue and yellow a quarter each?",
             "Red came up about half the time (26 of 50). Blue and yellow came up about a quarter of the time each.",
             "red half, blue and yellow a quarter each")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["“3 colours, so each is 1 out of 3.”", "Look at the size of each section. Bigger sections are more likely."],
            ["“5 heads in a row, so tails is due.”", "A coin has no memory. Tails is still 1 out of 2."],
            ["Outcomes: red, red, blue", "List each outcome once: red, blue."],
            ["“6 rolls show 2 is the most likely.”", "Use many trials. A few results can be just luck."],
        ])
    )


FAQ = [
    {"q": "What do Year 5 students learn about chance in the Australian Curriculum?",
     "a": "In Year 5 (AC9M5P01 and AC9M5P02) students list the possible outcomes of chance experiments, decide whether outcomes are equally likely, and run repeated experiments, using frequency to compare outcomes and estimate how likely they are."},
    {"q": "What does equally likely mean?",
     "a": "Outcomes are equally likely when each has the same chance. A fair coin (heads or tails) and a spinner with equal sections are equally likely; a spinner where red covers half is not."},
    {"q": "If a coin lands on heads 5 times in a row, is tails more likely next?",
     "a": "No. A fair coin has no memory, so tails is still 1 out of 2 on every toss. Thinking tails is “due” is a common mistake called the gambler’s fallacy."},
    {"q": "Why do more trials give a better estimate in a chance experiment?",
     "a": "With only a few trials, luck can change the results a lot. With many trials (for example 50 or 100 spins) the frequencies get closer to the real chances, which is the kind of reasoning NAPLAN numeracy questions test."},
]


def mark_large(u, pattern):
    """Tag pictures that must print larger (rows of spinners, frequency tables)."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(5817)
    sets = [set_outcomes(), set_equal(), set_compare(), set_experiments(), set_real()]
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
        "country": "au", "subject": "maths", "grade": "year-5", "slug": "chance", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Chance",
        "seo_title": "Year 5 Chance Worksheets: Outcomes, Equally Likely and Chance Experiments",
        "short_title": "Chance",
        "domain": "Probability",
        "standard_code": "AC9M5P01",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "List the possible outcomes of chance experiments involving equally likely outcomes and compare to those which are not equally likely",
        "meta_desc": "Free Year 5 chance worksheets for the Australian Curriculum: list outcomes for coins, dice, spinners and marbles, decide if outcomes are equally likely, compare chances and use the results of repeated experiments. 100 maths questions with an answer key, great for NAPLAN practice.",
        "key_big": "List each outcome once, and look at the size of each part: bigger sections are more likely.",
        "key_sub": "Equal sections give equally likely outcomes. A coin or dice has no memory: after 5 heads, tails is still 1 out of 2. Many trials give a better estimate than a few.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(four spinners|frequency table)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
