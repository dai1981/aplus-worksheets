# -*- coding: utf-8 -*-
"""
AU Year 3 Maths: Mental strategies and number sentences (Australian Curriculum v9.0, AC9M3A02 / AC9M3A01)
  python3 tools/gen_au_maths_y3_mental.py
Facts to 20 extended to larger numbers, bridging, jump strategy, near doubles, compensation,
inverse operations and fact families, unknown values in number sentences, word problems.
Every answer and every wrong answer is checked in code. HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-3")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
RED = "#c0392b"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
B = "<b>?</b>"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Ava", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Grace"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Leo", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c or c.startswith("-") or c.startswith("0"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            right = c[it["a"]]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def val(expr):
    return eval(expr.replace("−", "-").replace("×", "*"), {"__builtins__": {}})


def holds(eq, ans=None):
    """'? + 45 = 120' is true with ? = ans (real minus sign allowed)."""
    s = eq.replace(B, "?")
    if ans is not None:
        s = s.replace("?", str(ans))
    vals = [val(p.strip()) for p in s.split("=")]
    return all(v == vals[0] for v in vals)


def sfl(a, b):
    """Smaller digit from larger digit in each column: 72 − 29 → 57 (a typical mistake)."""
    da, db = str(a), str(b).rjust(len(str(a)), "0")
    return int("".join(str(abs(int(x) - int(y))) for x, y in zip(da, db)))


def nocarry(a, b):
    """Add column by column and drop every carried ten: 47 + 38 → 75."""
    out, p = 0, 1
    while a or b:
        out += ((a % 10 + b % 10) % 10) * p
        a, b, p = a // 10, b // 10, p * 10
    return out


class People:
    def __init__(self, rnd):
        self.pool = [(x, "she", "her") for x in GIRLS] + [(x, "he", "his") for x in BOYS]
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


def mark_large(u, pattern):
    """Tag wide pictures so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='(?:" + pattern + "))")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def money(c):
    return "%dc" % c if c < 100 else "$%d.%02d" % divmod(c, 100)


# ------------------------------------------------------------ pictures
def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 84 if j >= 10 else 56


def nline_svg(start, jumps, ticks):
    """Empty number line. Jumps go right for +, left for −. ticks: one label per point."""
    jlabels = [("+%d" % j) if j > 0 else ("−%d" % -j) for j in jumps]
    m, ry, ly = 30, 24, 50
    W = 2 * m + sum(jw(j) for j in jumps)
    H = ly + 32
    xs = [m] if jumps[0] > 0 else [W - m]
    for j in jumps:
        xs.append(xs[-1] + (jw(j) if j > 0 else -jw(j)))
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.5'/>" % (m - 18, ly, W - m + 18, ly, INK)]
    for k, j in enumerate(jumps):
        x1, x2 = xs[k], xs[k + 1]
        rx = abs(x2 - x1) / 2
        s.append("<path d='M %d %d A %.1f %d 0 0 %d %d %d' fill='none' stroke='%s' stroke-width='2.5'/>"
                 % (x1, ly, rx, ry, 1 if x2 > x1 else 0, x2, ly, GREEN))
        s.append("<polyline points='%d,%d %d,%d %d,%d' fill='none' stroke='%s' stroke-width='2.5' "
                 "stroke-linejoin='round'/>" % (x2 - 5, ly - 10, x2, ly - 2, x2 + 5, ly - 10, GREEN))
        s.append(text((x1 + x2) / 2, ly - ry - 7, jlabels[k], 15, col=GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    # check the picture matches the numbers
    v = start
    for j, t in zip(jumps, ticks[1:]):
        v += j
        assert t in ("?", None) or int(t) == v, (start, jumps, ticks)
    return svg_wrap(W, H, "".join(s), "empty number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ")))


def jump_q(start, jumps, prompt, wrong, e):
    """Number line question; the answer is start + all jumps."""
    ticks = [str(start)]
    v = start
    for j in jumps[:-1]:
        v += j
        ticks.append(str(v))
    ticks.append("?")
    ans = start + sum(jumps)
    return mcq(fig(nline_svg(start, jumps, ticks)) + prompt, ans, wrong, e)


def part_whole_svg(whole, p1, p2):
    """Part-part-whole: whole on top, two parts below. Values are numbers or '?'."""
    r = 31
    W, H = 196, 156
    cw, cy0 = W / 2, 6 + r
    c1, c2, cy1 = 8 + r, W - 8 - r, H - 6 - r
    s = []
    for cx in (c1, c2):
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                 % (cw, cy0 + r - 2, cx, cy1 - r + 2, INK))
    for cx, cy, v, fill in [(cw, cy0, whole, FILL), (c1, cy1, p1, "#fff"), (c2, cy1, p2, "#fff")]:
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (cx, cy, r, fill, GREEN))
        s.append(text(cx, cy + 7, str(v), 20, col=RED if v == "?" else INK))
    nums = [whole, p1, p2]
    if "?" not in nums:
        assert p1 + p2 == whole
    return svg_wrap(W, H, "".join(s), "part-part-whole model: whole %s, parts %s and %s" % (whole, p1, p2))


# ============================================================ set 1: facts to 20, extended
def set_facts():
    its = []

    def add(q, right, wrong, e, check):
        assert check, q
        its.append(mcq(q, right, wrong, e))

    # tens from a fact
    for a, b in [(7, 8), (9, 5), (4, 9)]:
        s = a + b
        add("%d + %d = %d. Use this fact. What is %d + %d?" % (a, b, s, 10 * a, 10 * b), 10 * s, [s, 100 * s, 10 * s - 10],
            "%d is %d tens and %d is %d tens. %d tens + %d tens = %d tens = <b>%d</b>."
            % (10 * a, a, 10 * b, b, a, b, s, 10 * s), True)
    for a, b in [(15, 7), (12, 5), (13, 4)]:
        d = a - b
        add("%d − %d = %d. Use this fact. What is %d − %d?" % (a, b, d, 10 * a, 10 * b), 10 * d,
            [d, 100 * d, sfl(10 * a, 10 * b)],
            "%d is %d tens and %d is %d tens. %d tens − %d tens = %d tens = <b>%d</b>."
            % (10 * a, a, 10 * b, b, a, b, d, 10 * d), sfl(10 * a, 10 * b) != 10 * d)
    add("Which fact helps you work out 80 + 60?", "8 + 6 = 14", ["8 + 4 = 12", "8 − 6 = 2", "80 + 6 = 86"],
        "80 is 8 tens and 60 is 6 tens. Use <b>8 + 6 = 14</b>: 14 tens = 140.", True)
    add("Which fact helps you work out 140 − 90?", "14 − 9 = 5", ["14 + 9 = 23", "9 − 4 = 5", "140 − 9 = 131"],
        "140 is 14 tens and 90 is 9 tens. Use <b>14 − 9 = 5</b>: 5 tens = 50.", True)
    # ones that cross a ten
    for a, b, show in [(47, 8, True), (36, 9, False), (68, 5, True), (256, 7, False), (485, 9, False)]:
        s = a + b
        o = a % 10
        fact = "%d + %d = %d. Use this fact. " % (o, b, o + b) if show else ""
        add(fact + "What is %d + %d?" % (a, b), s, [s - 10, a + 10 * b, s - 1],
            "%d + %d = %d, which is 1 ten and %d ones. So the tens go up by 1: %d + %d = <b>%d</b>."
            % (o, b, o + b, o + b - 10, a, b, s), o + b > 10 or o + b == 10)
    for a, b, show in [(63, 5, True), (42, 7, False), (81, 6, True), (234, 8, False), (352, 6, False)]:
        d = a - b
        o = a % 10
        fact = "1%d − %d = %d. Use this fact. " % (o, b, 10 + o - b) if show else ""
        add(fact + "What is %d − %d?" % (a, b), d, [v for v in [sfl(a, b), d + 10, d + 1, a + b] if v != a],
            "You cannot take %d from %d %s. Use 1%d − %d = %d. The tens go down by 1: %d − %d = <b>%d</b>."
            % (b, o, "one" if o == 1 else "ones", o, b, 10 + o - b, a, b, d), b > o)
    add("6 + 7 = 13. Use this fact. What is 600 + 700?", 1300, [130, 13, 1200],
        "6 hundreds + 7 hundreds = 13 hundreds = <b>1300</b>.", 600 + 700 == 1300)
    add("15 − 8 = 7. Use this fact. What is 1500 − 800?", 700, [70, 7000, 2300],
        "1500 is 15 hundreds. 15 hundreds − 8 hundreds = 7 hundreds = <b>700</b>.", 1500 - 800 == 700)
    assert len(its) == 20, len(its)
    return {"title": "Use facts to 20 with bigger numbers", "items": its}


# ============================================================ set 2: mental strategies
def set_strategies():
    its = []

    def add(q, right, wrong, e, check=True):
        assert check, q
        its.append(mcq(q, right, wrong, e))

    # bridging to 10
    its.append(jump_q(58, [2, 5], "Jump to 60 first. What is 58 + 7?", [55, 128, 64],
                      "58 + 2 = 60. 7 is 2 + 5, so add 5 more: 60 + 5 = <b>65</b>."))
    its.append(jump_q(86, [4, 2], "Jump to 90 first. What is 86 + 6?", [82, 146, 91],
                      "86 + 4 = 90. 6 is 4 + 2, so add 2 more: 90 + 2 = <b>92</b>."))
    its.append(jump_q(53, [-3, -5], "Jump back to 50 first. What is 53 − 8?", [sfl(53, 8), 61, 46],
                      "53 − 3 = 50. 8 is 3 + 5, so take away 5 more: 50 − 5 = <b>45</b>."))
    add("To work out 38 + 7, you jump to 40 first. How do you split the 7?", "2 and 5",
        ["3 and 4", "1 and 6", "7 and 0"], "38 needs <b>2</b> to make 40. Then 5 more: 40 + 5 = 45. So split 7 into <b>2 and 5</b>.",
        38 + 2 == 40 and 40 + 5 == 45)
    add("To work out 64 − 9, you jump back to 60 first. How do you split the 9?", "4 and 5",
        ["6 and 3", "1 and 8", "2 and 7"], "64 − 4 = 60. Then 5 more: 60 − 5 = 55. So split 9 into <b>4 and 5</b>.",
        64 - 4 == 60 and 60 - 5 == 55)
    # jump strategy
    its.append(jump_q(45, [30, 2], "Jump the tens, then the ones. What is 45 + 32?", [75, 87, 78],
                      "45 + 30 = 75. Then 75 + 2 = <b>77</b>. (75 stops after the tens.)"))
    its.append(jump_q(86, [-40, -3], "Jump back the tens, then the ones. What is 86 − 43?", [46, 129, 53],
                      "86 − 40 = 46. Then 46 − 3 = <b>43</b>. (46 stops after the tens.)"))
    its.append(jump_q(158, [20, 5], "Jump the tens, then the ones. What is 158 + 25?", [173, 178, 408],
                      "158 + 20 = 178. Then 178 + 5: 178 + 2 = 180, and 3 more is <b>183</b>."))
    its.append(jump_q(124, [-30, -6], "Jump back the tens, then the ones. What is 124 − 36?", [94, sfl(124, 36), 98],
                      "124 − 30 = 94. Then 94 − 6: 94 − 4 = 90, and 2 more back is <b>88</b>."))
    # near doubles
    add("Use double 25. What is 25 + 26?", 51, [50, 52, 41],
        "Double 25 is 50. 26 is 1 more than 25, so add 1: 50 + 1 = <b>51</b>.", 25 + 26 == 51)
    add("Use a near double. What is 35 + 36?", 71, [70, 72, 61],
        "Double 35 is 70. 36 is 1 more, so 70 + 1 = <b>71</b>. (61 forgets the ten from 5 + 6 = 11.)", 35 + 36 == 71)
    add("Use double 40. What is 40 + 39?", 79, [80, 81, 78],
        "Double 40 is 80. 39 is 1 less than 40, so take away 1: 80 − 1 = <b>79</b>.", 40 + 39 == 79)
    add("Use a near double. What is 150 + 160?", 310, [300, 320, 210],
        "Double 150 is 300. 160 is 10 more than 150, so add 10: 300 + 10 = <b>310</b>.", 150 + 160 == 310)
    add("Which double helps with 45 + 46?", "45 + 45, then add 1",
        ["45 + 45, then take 1", "46 + 46, then add 1", "40 + 40, then add 1"],
        "46 is 1 more than 45. So double 45 is 90, then add 1: 91. The answer is <b>45 + 45, then add 1</b>.", 45 + 46 == 91)
    # compensation
    for a, b, lead in [(39, 26, "Add 40, then take away 1. "), (54, 29, "Use compensation. "), (67, 19, "Use compensation. ")]:
        r = b if a % 10 == 9 else a
        k = a if a % 10 == 9 else b
        up = k + 1
        s = a + b
        add(lead + "What is %d + %d?" % (a, b), s, [s + 1, s + 2, s - 10],
            "%d is 1 less than %d. %s = %d. You added 1 too many, so take it away: %d − 1 = <b>%d</b>."
            % (k, up, ("%d + %d" % (up, r)) if k == a else ("%d + %d" % (r, up)), up + r, up + r, s), up % 10 == 0)
    for a, b in [(72, 29), (145, 98)]:
        up = b + (10 - b % 10)
        extra = up - b
        d = a - b
        add("Use compensation. What is %d − %d?" % (a, b), d, [d - extra, d - 2 * extra, sfl(a, b)],
            "%d is %d less than %d. %d − %d = %d. You took away %d too many, so add %s back: %d + %d = <b>%d</b>."
            % (b, extra, up, a, up, a - up, extra, "it" if extra == 1 else "them", a - up, extra, d), up % 10 == 0)
    add("Which shows a good way to work out 39 + 26?", "40 + 26 − 1",
        ["40 + 26 + 1", "39 + 20 − 6", "40 + 26 − 39"],
        "39 is 1 less than 40. Add 40, then take away the extra 1: <b>40 + 26 − 1</b> = 65.",
        val("40 + 26 - 1") == 65 and all(val(x) != 65 for x in ["40 + 26 + 1", "39 + 20 - 6", "40 + 26 - 39"]))
    assert len(its) == 20, len(its)
    return {"title": "Mental strategies: bridge, jump, double, compensate", "items": its}


# ============================================================ set 3: inverse and fact families
def set_inverse():
    its = []

    def add(q, right, wrong, e, check=True):
        assert check, q
        its.append(mcq(q, right, wrong, e))

    def true_one(right, wrong):
        assert holds(right), right
        for w in wrong:
            assert not holds(w), w

    add(fig(part_whole_svg(120, 45, "?")) + "What is the missing part?", 75, [165, 85, 120],
        "Whole − part = the other part. 120 − 45: 120 − 40 = 80, then 80 − 5 = <b>75</b>. Check: 45 + 75 = 120.",
        45 + 75 == 120)
    add(fig(part_whole_svg("?", 38, 47)) + "What is the whole?", 85, [9, nocarry(38, 47), 715],
        "The whole is the two parts added. 38 + 47: 38 + 40 = 78, then 78 + 7 = <b>85</b>.", 38 + 47 == 85)
    add(fig(part_whole_svg(200, "?", 130)) + "What is the missing part?", 70, [330, 170, 130],
        "Count on from 130 to 200: 130 + 70 = 200. The missing part is <b>70</b>.", 130 + 70 == 200)
    add(fig(part_whole_svg(250, "?", 90)) + "What is the missing part?", 160, [340, sfl(250, 90), 90],
        "250 − 90: 250 − 100 = 150, then add back 10: <b>160</b>. Check: 160 + 90 = 250.", 160 + 90 == 250)
    w = ["90 − 60 = 30", "60 − 150 = 90", "150 − 60 = 80"]
    add(fig(part_whole_svg(150, 90, 60)) + "Which subtraction matches the model?", "150 − 90 = 60", w,
        "Start with the whole and take away one part. The other part is left: <b>150 − 90 = 60</b>.",
        holds("150 − 90 = 60") and not any(holds(x) for x in w[1:]))
    w = ["83 + 36 = 47", "47 − 36 = 11", "83 + 47 = 130"]
    add(fig(part_whole_svg(83, 36, 47)) + "Which addition matches the model?", "36 + 47 = 83", w,
        "Add the two parts to make the whole: <b>36 + 47 = 83</b>.", holds("36 + 47 = 83") and not holds(w[0]))
    add(fig(part_whole_svg("?", 165, 235)) + "What is the whole?", 400, [70, nocarry(165, 235), 300],
        "165 + 235: 165 + 200 = 365, then 365 + 35 = <b>400</b>. (5 + 5 = 10, so both columns carry.)", 165 + 235 == 400)
    w = ["55 − 28 = 83", "83 + 28 = 55", "28 − 83 = 55"]
    true_one("83 − 55 = 28", w)
    add("28 + 55 = 83. Which is also true?", "83 − 55 = 28", w,
        "Subtraction undoes addition. Start with the whole, 83, and take away 55: <b>83 − 55 = 28</b>.")
    w = ["120 + 70 = 50", "70 − 50 = 120", "50 + 120 = 70"]
    true_one("50 + 70 = 120", w)
    add("120 − 70 = 50. Which is also true?", "50 + 70 = 120", w,
        "Addition undoes subtraction. Add the two parts to get back to 120: <b>50 + 70 = 120</b>.")
    w = ["25 + 40 = 65", "65 − 40 = 25", "65 − 25 = 40"]
    assert all(holds(x) for x in w) and not holds("40 − 25 = 65")
    add("Which is NOT in the fact family for 25, 40 and 65?", "40 − 25 = 65", w,
        "40 − 25 is 15, not 65. The whole, 65, must come first in a subtraction. So <b>40 − 25 = 65</b> is not in the family.")
    w = ["60 + 90 = 150", "150 − 60 = 90", "150 − 90 = 60"]
    assert all(holds(x) for x in w) and holds("90 − 60 = 30")
    add("Which is NOT in the fact family for 60, 90 and 150?", "90 − 60 = 30", w,
        "It is true, but it uses 30, and 30 is not one of the three numbers. So <b>90 − 60 = 30</b> is not in the family.")
    add("How many facts are in the fact family for 30, 50 and 80?", 4, [2, 3, 6],
        "30 + 50 = 80, 50 + 30 = 80, 80 − 30 = 50 and 80 − 50 = 30. That is <b>4</b> facts.")
    w = ["92 + 58 = 150", "34 + 92 = 126", "58 − 34 = 24"]
    add("Which addition checks that 92 − 58 = 34 is right?", "34 + 58 = 92", w,
        "Add the answer and the number you took away. You should get back to 92: <b>34 + 58 = 92</b>.",
        holds("34 + 58 = 92") and holds("92 − 58 = 34"))
    w = ["92 + 25 = 117", "67 − 25 = 42", "25 − 67 = 92"]
    add("Which subtraction checks that 67 + 25 = 92 is right?", "92 − 25 = 67", w,
        "Take away the number you added. You should get back to 67: <b>92 − 25 = 67</b>.",
        holds("92 − 25 = 67") and not holds(w[2]))
    nm, he = "Mia", "she"
    add("%s works out 81 − 27 = 64. To check, %s adds 64 + 27 and gets 91, not 81. What is 81 − 27?" % (nm, he),
        54, [64, 108, sfl(81, 27)],
        "The check shows 64 is wrong. 81 − 27: 81 − 20 = 61, then 61 − 7 = <b>54</b>. Check: 54 + 27 = 81.",
        54 + 27 == 81 and 64 + 27 == 91)
    add("Noah says 145 + 38 = 173. Use subtraction to check. Is he right?", "No, it is 183",
        ["Yes, it is 173", "No, it is 107", "No, it is 163"],
        "173 − 38 = 135, not 145, so Noah is wrong. 145 + 38: 145 + 40 = 185, then − 2 = <b>183</b>.",
        173 - 38 == 135 and 145 + 38 == 183)
    add("Addition and subtraction are inverse operations. What does this mean?", "They undo each other",
        ["They give the same answer", "You can swap the numbers", "You always add first"],
        "Inverse means opposite. If you add 30 and then take away 30, you are back where you started. They <b>undo each other</b>.")
    add("Start with 64. Add 29. Then take away 29. What number do you get?", 64, [93, 35, 122],
        "Taking away 29 undoes adding 29. You get back to the start: <b>64</b>.", 64 + 29 - 29 == 64)
    add("You know 46 + 37 = 83. What is 83 − 46?", 37, [129, 46, sfl(83, 46)],
        "46 and 37 are the parts and 83 is the whole. Whole − one part = the other part: <b>37</b>.", 83 - 46 == 37)
    add("You know 250 + 180 = 430. What is 430 − 180?", 250, [610, 180, sfl(430, 180)],
        "250 and 180 are the parts and 430 is the whole. 430 − 180 = <b>250</b>. No need to work it out again.",
        430 - 180 == 250)
    # easy → hard
    order = [5, 4, 16, 11, 7, 8, 17, 18, 0, 2, 1, 9, 10, 12, 13, 19, 3, 6, 14, 15]
    assert sorted(order) == list(range(20))
    its[:] = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Inverse operations and fact families", "items": its}


# ============================================================ set 4: unknown values in number sentences
def set_unknowns():
    its = []

    def add(eq, right, wrong, e):
        assert holds(eq, right), eq
        for w in wrong:
            assert not holds(eq, w), (eq, w)
        its.append(mcq("Find the missing number: " + eq.replace("?", B), right, wrong, e))

    add("? + 45 = 120", 75, [165, 120, 85],
        "Use the inverse: 120 − 45. 120 − 40 = 80, then 80 − 5 = <b>75</b>. Check: 75 + 45 = 120. (120 is the total, not the missing part.)")
    add("57 + ? = 100", 43, [53, 157, 100],
        "Count on from 57: 57 + 3 = 60, then 60 + 40 = 100. 3 + 40 = <b>43</b>. (53 makes 110.)")
    add("68 = ? + 30", 38, [98, 68, 65],
        "The = sign means both sides are the same. ? + 30 = 68, so 68 − 30 = <b>38</b>. Check: 38 + 30 = 68.")
    add("? + 26 = 81", 55, [107, 81, 65],
        "Use the inverse: 81 − 26. 81 − 20 = 61, then 61 − 6 = <b>55</b>. Check: 55 + 26 = 81.")
    add("90 − ? = 35", 55, [125, 35, sfl(90, 35)],
        "Count on from 35 to 90: 35 + 5 = 40, then 40 + 50 = 90. 5 + 50 = <b>55</b>. Check: 90 − 55 = 35.")
    add("? − 40 = 85", 125, [45, 85, 25],
        "Use the inverse: 85 + 40 = <b>125</b>. Check: 125 − 40 = 85. (45 takes away instead of adding.)")
    add("? − 25 = 48", 73, [23, 48, nocarry(48, 25)],
        "Use the inverse: 48 + 25. 48 + 2 = 50, then 50 + 23 = <b>73</b>. Check: 73 − 25 = 48.")
    add("140 = 90 + ?", 50, [230, 140, sfl(140, 90)],
        "90 + ? = 140, so 140 − 90. 14 tens − 9 tens = 5 tens = <b>50</b>.")
    add("200 − ? = 120", 80, [320, 120, 8],
        "Count on from 120 to 200: 8 tens = <b>80</b>. Check: 200 − 80 = 120.")
    add("300 − ? = 175", 125, [475, 175, sfl(300, 175)],
        "Count on from 175: 175 + 25 = 200, then 200 + 100 = 300. 25 + 100 = <b>125</b>. Check: 300 − 125 = 175.")
    add("500 − ? = 350", 150, [850, 350, 50],
        "Count on from 350: 350 + 50 = 400, then 400 + 100 = 500. 50 + 100 = <b>150</b>.")
    add("? + 175 = 300", 125, [475, 300, 135],
        "Use the inverse: 300 − 175. Count on 25 to 200 and 100 to 300: <b>125</b>. Check: 125 + 175 = 300.")
    add("? − 130 = 270", 400, [140, 270, nocarry(270, 130)],
        "Use the inverse: 270 + 130. 270 + 30 = 300, then 300 + 100 = <b>400</b>.")
    add("650 = ? + 280", 370, [930, 650, sfl(650, 280)],
        "? + 280 = 650, so 650 − 280. 650 − 300 = 350, then add back 20: <b>370</b>. Check: 370 + 280 = 650.")
    add("40 + 25 = ? + 30", 35, [65, 95, 25],
        "Both sides must have the same value. 40 + 25 = 65, so ? + 30 = 65 and ? = <b>35</b>. (65 is only the left side.)")
    add("70 + 50 = 60 + ?", 60, [120, 180, 50],
        "70 + 50 = 120. So 60 + ? must also be 120. 120 − 60 = <b>60</b>.")
    add("100 − 30 = ? − 40", 110, [70, 30, 100],
        "100 − 30 = 70. So ? − 40 = 70. Use the inverse: 70 + 40 = <b>110</b>.")
    add("38 + 9 = ? + 10", 37, [47, 57, 39],
        "10 is 1 more than 9, so the other number must be 1 less than 38: <b>37</b>. Check: 38 + 9 = 47 and 37 + 10 = 47.")
    add("64 − 19 = ? − 20", 65, [45, 63, 25],
        "64 − 19 = 45. So ? − 20 = 45, and 45 + 20 = <b>65</b>. Check: 65 − 20 = 45.")
    w = ["45 + 15 = 60 + 10", "45 + 15 = 70", "45 + 15 = 50 + 15"]
    assert holds("45 + 15 = 70 − 10") and not any(holds(x) for x in w)
    its.append(mcq("Which number sentence is true?", "45 + 15 = 70 − 10", w,
                   "45 + 15 = 60 and 70 − 10 = 60. Both sides are the same, so <b>45 + 15 = 70 − 10</b> is true."))
    assert len(its) == 20, len(its)
    return {"title": "Find the unknown in a number sentence", "items": its}


# ============================================================ set 5: word problems
def set_words(P):
    its = []

    def who():
        nm, he, his = P.next()
        return dict(n=nm, he=he, He=cap(he), his=his, him="her" if he == "she" else "him")

    def choose(t, right, wrong, ans, e):
        assert holds(right, ans), right
        for w in wrong:
            assert not holds(w, ans), w
        its.append(mcq(t.format(**who()) + " Which number sentence shows this?", right, wrong, e))

    def solve(t, right, unit, wrong, e, check):
        assert check, t
        fmt = (lambda v: "%d %s" % (v, unit)) if unit else (lambda v: str(v))
        its.append(mcq(t.format(**who()), fmt(right), [fmt(v) for v in wrong], e))

    choose("{n} has 45 stickers. {He} gets some more. Now {he} has 120 stickers.", "45 + ? = 120",
           ["120 + 45 = ?", "? − 45 = 120", "45 − ? = 120"], 75,
           "Start with 45, add an unknown amount, and end with 120: <b>45 + ? = 120</b>. The missing number is 75.")
    choose("The canteen had 300 icy poles. Some were sold. Now 175 are left.", "300 − ? = 175",
           ["175 − 300 = ?", "300 + 175 = ?", "? − 300 = 175"], 125,
           "Start with 300, take away an unknown amount, and 175 are left: <b>300 − ? = 175</b>. The missing number is 125.")
    choose("Some students are on a bus. 30 more get on. Now there are 68 students on the bus.", "? + 30 = 68",
           ["68 + 30 = ?", "30 − ? = 68", "? − 30 = 68"], 38,
           "We do not know the start. Add 30 to get 68: <b>? + 30 = 68</b>. The missing number is 38.")
    choose("{n} reads 47 pages on Monday and 38 pages on Tuesday. How many pages is that altogether?", "47 + 38 = ?",
           ["47 − 38 = ?", "47 + ? = 38", "38 − 47 = ?"], 85,
           "Altogether means add the two amounts: <b>47 + 38 = ?</b>. The answer is 85.")
    choose("There are 92 people at the pool. 58 go home. How many are still at the pool?", "92 − 58 = ?",
           ["58 − 92 = ?", "92 + 58 = ?", "58 + 92 = ?"], 34,
           "Start with 92 and take away 58: <b>92 − 58 = ?</b>. Put the bigger number first. The answer is 34.")
    choose("{n} had some marbles. {He} gave away 40. Now {he} has 85 left.", "? − 40 = 85",
           ["85 − 40 = ?", "40 − ? = 85", "? + 85 = 40"], 125,
           "We do not know the start. Take away 40 and 85 are left: <b>? − 40 = 85</b>. The missing number is 125.")
    choose("A footy team scored 64 points. The other team scored 19 fewer points. How many did the other team score?",
           "64 − 19 = ?", ["64 + 19 = ?", "19 − 64 = ?", "? − 19 = 64"], 45,
           "19 fewer means take away 19: <b>64 − 19 = ?</b>. The answer is 45.")
    choose("The hall needs 100 chairs for assembly. 57 chairs are set out. How many more are needed?", "57 + ? = 100",
           ["57 + 100 = ?", "? − 57 = 100", "100 + ? = 57"], 43,
           "57 and some more make 100: <b>57 + ? = 100</b>. The missing number is 43.")
    solve("At the swimming carnival, 160 students are at the pool. 70 of them are in the water. How many are not in the water?",
          90, "students", [230, sfl(160, 70), 9],
          "Take away the 70 in the water. 16 tens − 7 tens = 9 tens, so <b>90 students</b>.", 160 - 70 == 90)
    solve("{n} scores 39 points in a game. Then {he} scores 26 more. How many points does {he} have now?",
          65, "points", [66, 67, 55],
          "Add. 39 is 1 less than 40. 40 + 26 = 66, then take away 1: <b>65 points</b>.", 39 + 26 == 65)
    solve("Year 3 Blue has 25 students. Year 3 Gold has 26 students. How many students are there in the two classes?",
          51, "students", [50, 52, 41],
          "Use a near double. Double 25 is 50, and 1 more is <b>51 students</b>.", 25 + 26 == 51)
    solve("The canteen had 250 icy poles. Some were sold. 160 are left. How many icy poles were sold?",
          90, "icy poles", [410, sfl(250, 160), 160],
          "250 − ? = 160. Count on from 160: 160 + 40 = 200, then 200 + 50 = 250. 40 + 50 = <b>90 icy poles</b>.",
          250 - 90 == 160)
    solve("Some students are on a bus. 30 more get on. Now there are 84 students. How many were on the bus at first?",
          54, "students", [114, 84, 81],
          "? + 30 = 84. Use the inverse: 84 − 30 = <b>54 students</b>. Check: 54 + 30 = 84.", 54 + 30 == 84)
    w = who()
    a, b = 120, 75
    its.append(mcq("{n} has $1.20. {He} buys an apple at the canteen for 75c. How much money does {he} have left?".format(**w),
                   money(a - b), [money(a + b), money(sfl(a, b)), money(b)],
                   "Work in cents: $1.20 = 120c. 120 − 75: 120 − 70 = 50, then 50 − 5 = 45. So <b>45c</b> is left."))
    assert a - b == 45
    solve("The sausage sizzle sells 148 sausages before lunch and 37 after lunch. How many sausages does it sell?",
          185, "sausages", [nocarry(148, 37), 111, 184],
          "Add. 148 + 30 = 178, then 178 + 7: 178 + 2 = 180, and 5 more is <b>185 sausages</b>.", 148 + 37 == 185)
    solve("A school has 412 students. 98 students go on an excursion. How many students stay at school?",
          314, "students", [312, 310, sfl(412, 98)],
          "98 is 2 less than 100. 412 − 100 = 312. You took away 2 too many, so add them back: <b>314 students</b>.",
          412 - 98 == 314)
    solve("A library has 700 books. 260 books are borrowed. How many books are still on the shelves?",
          440, "books", [960, sfl(700, 260), 260],
          "700 − 260: 700 − 200 = 500, then 500 − 60 = <b>440 books</b>. Check: 440 + 260 = 700.", 700 - 260 == 440)
    solve("{n} has 64 footy cards. {He} gets 29 more. Then {he} gives 40 away. How many cards does {he} have now?",
          53, "cards", [93, 133, 54],
          "Step 1: 64 + 29 = 93 (add 30, take away 1). Step 2: 93 − 40 = <b>53 cards</b>. (93 stops after step 1.)",
          64 + 29 - 40 == 53)
    w = who()
    its.append(mcq("{n} buys a pie for $4.50 and a juice for $2.80. How much does {he} spend?".format(**w),
                   money(450 + 280), [money(630), money(170), money(830)],
                   "$4 + $2 = $6. 50c + 80c = 130c = $1.30. $6 + $1.30 = <b>$7.30</b>. ($6.30 forgets the extra dollar.)"))
    assert 450 + 280 == 730 and 280 - 450 < 0 and 450 - 280 == 170
    solve("125 students are at the athletics carnival in the morning. More come after lunch. Now there are 200. "
          "How many students came after lunch?", 75, "students", [325, 200, 85],
          "125 + ? = 200. Count on: 125 + 5 = 130, then 130 + 70 = 200. 5 + 70 = <b>75 students</b>.", 125 + 75 == 200)
    assert len(its) == 20, len(its)
    return {"title": "Word problems: choose the number sentence", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Use the facts you know</h2>"
        "<p>If you know the facts to 20, you know much more. 7 + 8 = 15, so 7 tens + 8 tens = 15 tens. "
        "That means <b>70 + 80 = 150</b>. The ones digits tell you <b>47 + 8 = 55</b>, because 7 + 8 = 15.</p>"
        + table(["Fact", "Tens", "Hundreds", "Ones"], [
            ["7 + 8 = 15", "70 + 80 = 150", "700 + 800 = 1500", "47 + 8 = 55"],
            ["13 − 5 = 8", "130 − 50 = 80", "1300 − 500 = 800", "63 − 5 = 58"],
        ]) +
        "<h2>Four mental strategies</h2>"
        "<p><b>Bridge to 10.</b> Jump to the next ten first, then add the rest.</p>"
        "<figure class='sn-fig'>" + nline_svg(58, [2, 5], ["58", "60", "65"]) +
        "<figcaption>58 + 7: jump +2 to 60, then +5 more to 65.</figcaption></figure>"
        "<p><b>Jump strategy.</b> Keep the first number. Jump the tens, then the ones.</p>"
        "<figure class='sn-fig'>" + nline_svg(45, [30, 2], ["45", "75", "77"]) +
        "<figcaption>45 + 32: jump +30 to 75, then +2 to 77.</figcaption></figure>"
        "<p><b>Near doubles.</b> 25 + 26 is double 25 and 1 more: 50 + 1 = 51.</p>"
        "<p><b>Compensation.</b> Round one number to a ten, then fix it.</p>"
        + ex("Example", "What is 39 + 26?",
             "39 is 1 less than 40. 40 + 26 = 66. You added 1 too many, so take it away: 66 − 1 = 65.", "65")
        + ex("Example", "What is 72 − 29?",
             "29 is 1 less than 30. 72 − 30 = 42. You took away 1 too many, so add it back: 42 + 1 = 43.", "43")
        + "<h2>Addition and subtraction undo each other</h2>"
        "<p>Addition and subtraction are <b>inverse operations</b>. Three numbers make a <b>fact family</b>.</p>"
        "<figure class='sn-fig'>" + part_whole_svg(120, 45, 75) +
        "<figcaption>45 + 75 = 120, 75 + 45 = 120, 120 − 45 = 75 and 120 − 75 = 45.</figcaption></figure>"
        "<h2>Find the unknown in a number sentence</h2>"
        "<p>The = sign means <b>both sides have the same value</b>. Use the inverse to find the missing number.</p>"
        + ex("Example", "? + 45 = 120",
             "Use the inverse: 120 − 45 = 75. Check: 75 + 45 = 120.", "75")
        + ex("Example", "300 − ? = 175",
             "Count on from 175: 175 + 25 = 200, then 200 + 100 = 300. 25 + 100 = 125.", "125")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Compensating the wrong way: 39 + 26 = 67", "You added 1 too many, so take 1 away: 65"],
            ["Forgetting to compensate: 39 + 26 = 66", "Always fix the number you rounded: 66 − 1 = 65"],
            ["Losing the zero: 70 + 80 = 15 (or 1500)", "7 tens + 8 tens = 15 tens = 150"],
            ["Giving the total as the unknown: ? + 45 = 120, ? = 120", "120 is the whole. Find the part: 120 − 45 = 75"],
            ["Taking the smaller digit from the larger: 72 − 29 = 57", "Bridge or compensate: 72 − 30 + 1 = 43"],
        ])
    )


FAQ = [
    {"q": "What mental strategies do Year 3 students learn?",
     "a": "Year 3 students use facts to 20 to work with bigger numbers, and learn to bridge to 10, jump along an empty number line, use near doubles and use compensation, such as 39 + 26 = 40 + 26 − 1 = 65."},
    {"q": "What is the compensation strategy in maths?",
     "a": "You change one number to a friendly ten, work it out, then fix the answer. For 72 − 29, take away 30 to get 42, then add back the extra 1 to get 43."},
    {"q": "How do you find the missing number in a number sentence?",
     "a": "Use the inverse operation. For ? + 45 = 120, work out 120 − 45 = 75, then check that 75 + 45 = 120."},
    {"q": "Is mental maths important for NAPLAN in Year 3?",
     "a": "Yes. The Year 3 NAPLAN numeracy test is done without a calculator, so quick mental strategies and number sentences help students work accurately."},
]


def gen():
    rnd = random.Random(3803)
    P = People(rnd)
    sets = [set_facts(), set_strategies(), set_inverse(), set_unknowns(), set_words(P)]
    balance(sets, rnd)
    allk = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = it["q"]
            assert k not in allk, it["q"]
            allk.add(k)
            m = re.search(r"What is (\d+) ([+−]) (\d+)\?$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(it["c"][it["a"]]) == (a + b if op == "+" else a - b), it["q"]
                for j, c in enumerate(it["c"]):
                    if j != it["a"]:
                        assert int(c) != (a + b if op == "+" else a - b)
    u = {
        "country": "au", "subject": "maths", "grade": "year-3", "slug": "mental-strategies-and-number-sentences",
        "sort": 3, "updated": UPDATED, "pdf_url": "",
        "title": "Mental Strategies and Number Sentences",
        "seo_title": "Year 3 Mental Strategies and Number Sentences Worksheets (Australian Curriculum)",
        "short_title": "Mental strategies and number sentences",
        "domain": "Algebra",
        "standard_code": "AC9M3A02",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Extend and apply knowledge of addition and subtraction facts to 20 to develop efficient mental strategies for computation with larger numbers without a calculator",
        "meta_desc": "Free Year 3 maths worksheets on mental strategies and number sentences: use facts to 20 with bigger numbers, bridge to 10, near doubles, compensation, fact families and finding the unknown. 100 questions with an answer key, matched to the Australian Curriculum and useful for NAPLAN.",
        "key_big": "Use the facts to 20 you know to work out bigger sums in your head.",
        "key_sub": "7 + 8 = 15, so 70 + 80 = 150 and 47 + 8 = 55. Round and fix: 39 + 26 = 40 + 26 − 1 = 65. Use the inverse to find the unknown: ? + 45 = 120, so ? = 120 − 45 = 75.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "empty number line")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
