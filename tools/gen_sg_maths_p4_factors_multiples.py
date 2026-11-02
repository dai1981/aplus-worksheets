# -*- coding: utf-8 -*-
"""
Singapore Primary 4 Maths: Factors and multiples (MOE 2021 Primary Mathematics Syllabus,
Primary 4: Whole Numbers - factors and multiples; common factors of two numbers;
common multiples of two 1-digit numbers)
  python3 tools/gen_sg_maths_p4_factors_multiples.py
Factors and factor pairs (arrays), “is it a factor?” with 1-digit factors within 100 (division with
remainder, groups of counters), common factors of two numbers, multiples and “is it a multiple?”
(skip counting, number lines), and common multiples of two 1-digit numbers with word problems in
Singapore settings (packets, buses, towers of blocks) and bar models.
Every factor, multiple and common factor or multiple is checked in code.
Wrong answers come from real mistakes: forgetting 1 and the number itself, leaving out the middle
factor pair, mixing up factors and multiples, listing only one common factor, “even means it has 4
(or 6) as a factor”, “ends in 7 means a multiple of 7”, multiplying or adding the two numbers instead
of finding the first common multiple, and answering with the wrong quantity (packets instead of items).
HTML attributes use single quotes (no backslashes in the JSON). Singapore English.
"""
import json, os, random, re
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-4")
UPDATED = "2026-11-03"
GREEN = "#2e7d4f"
FILL = "#cfe6d6"
FILL_Y = "#fde7bd"
FILL_B = "#d6e4f5"
RED = "#c0392b"
INK = "#2b2b2b"
GREY = "#8a8f8c"
FONT = "Arial, Helvetica, sans-serif"
NBSP = "\u00a0"


# ------------------------------------------------------------ maths
def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def cfs(a, b):
    return [d for d in factors(min(a, b)) if a % d == 0 and b % d == 0]


def L(a, b):
    return a * b // gcd(a, b)


def mults(d, upto):
    return [d * k for k in range(1, upto // d + 1)]


def lst(xs):
    return ", ".join(str(x) for x in xs)


def pairs(x):
    return [(d, x // d) for d in factors(x) if d * d <= x]


def divs(x, d):
    """'48 ÷ 5 = 9 R 3' or '48 ÷ 6 = 8'."""
    q, r = divmod(x, d)
    return "%d ÷ %d = %d%s" % (x, d, q, " R %d" % r if r else "")


def am(h, m):
    return "%d.%02d am" % (h, m)


def pm(h, m):
    return "%d.%02d pm" % (h, m)


# ------------------------------------------------------------ helpers
def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 unique distractors. Positions are set later by balance()."""
    correct = str(correct)
    seen = {plain(correct)}
    pick = []
    for c in cands:
        c = str(c)
        if not c or plain(c) in seen:
            continue
        seen.add(plain(c))
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            right = it["c"][0]
            wrong = it["c"][1:]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w)), int(round(h))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    return len(str(t)) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK, weight=700):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='%d' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, weight, col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def mark_large(u, pattern):
    """Tag wide pictures that must print larger so every number stays readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def array_svg(rows, cols, sp=26, r=9, o=8):
    """An array of counters: rows × cols."""
    W = 2 * o + cols * sp
    H = 2 * o + rows * sp
    s = []
    for i in range(rows):
        for j in range(cols):
            s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (o + j * sp + sp // 2, o + i * sp + sp // 2, r, FILL, GREEN))
    return svg_wrap(W, H, "".join(s), "array of %d counters in %d rows of %d" % (rows * cols, rows, cols))


GROUP_SHAPE = {4: (2, 2), 6: (2, 3), 3: (1, 3), 5: (1, 5), 8: (2, 4)}


def groups_svg(total, size, sp=16, r=5.5, pad=7, gap=10, o=6):
    """total counters put into groups of size (each group in a ring); leftovers are red, outside the rings."""
    gr, gc = GROUP_SHAPE[size]
    k, left = divmod(total, size)
    gw, gh = gc * sp + 2 * pad, gr * sp + 2 * pad
    s = []
    x = o
    for g in range(k):
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%.1f' rx='9' fill='none' stroke='%s' stroke-width='2'/>"
                 % (x, o, gw, gh, GREEN))
        for i in range(gr):
            for j in range(gc):
                s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>"
                         % (x + pad + j * sp + sp / 2, o + pad + i * sp + sp / 2, r, FILL, GREEN))
        x += gw + gap
    for j in range(left):
        s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#f6d5d0' stroke='%s' stroke-width='1.5'/>"
                 % (x + pad / 2 + j * sp + sp / 2, o + gh / 2, r, RED))
    if left:
        x += pad + left * sp + gap
    W = x - gap + o
    return svg_wrap(W, gh + 2 * o, "".join(s), "groups of %d counters, %d counters in all" % (size, total))


def factor_rows_svg(a, b, circle=True):
    """The factors of a and b in two rows, lined up by size, with the common factors circled."""
    fa, fb = factors(a), factors(b)
    step, o = 36, 8
    lx = 14 + tw("%d:" % max(a, b), 16)
    cols = sorted(set(fa) | set(fb))
    W = lx + len(cols) * step + o
    H = 2 * 40 + 2 * o
    s = []
    for r, (v, fs) in enumerate([(a, fa), (b, fb)]):
        y = o + 26 + r * 40
        s.append(text(lx - 8, y, "%d:" % v, 16, anchor="end"))
        for d in fs:
            x = lx + cols.index(d) * step + step / 2
            if circle and d in fa and d in fb:
                s.append("<circle cx='%.1f' cy='%d' r='15' fill='%s' stroke='%s' stroke-width='2'/>"
                         % (x, y - 6, FILL, GREEN))
            s.append(text(x, y, str(d), 15))
    return svg_wrap(W, H, "".join(s), "factors of %d and %d with the common factors circled" % (a, b))


def multiples_svg(a, b, top, show=False, sc=8):
    """Multiples of a and b placed by size on two rows. With show=True, common multiples are red and joined."""
    ox = 40
    W = ox + top * sc + 18
    H = 112
    ya, yb = 34, 80
    s = []
    for v, y in [(a, ya), (b, yb)]:
        s.append(text(ox - 12, y + 6, "%d:" % v, 16, anchor="end"))
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5'/>" % (ox, y, ox + top * sc + 6, y, GREY))
    if show:
        for m in range(L(a, b), top + 1, L(a, b)):
            x = ox + m * sc
            s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2' stroke-dasharray='4 3'/>"
                     % (x, ya + 7, x, yb - 7, RED))
    for v, y, up in [(a, ya, True), (b, yb, False)]:
        for m in mults(v, top):
            x = ox + m * sc
            common = show and m % a == 0 and m % b == 0
            s.append("<circle cx='%d' cy='%d' r='5' fill='%s'/>" % (x, y, RED if common else GREEN))
            s.append(text(x, y - 10 if up else y + 23, str(m), 14, col=RED if common else INK))
    return svg_wrap(W, H, "".join(s), "multiples of %d and %d up to %d" % (a, b, top))


def skip_line_svg(d, n, hide, sc=None):
    """A number line from 0 with jumps of d, n jumps. The multiple d × hide is shown as ?."""
    top = d * n
    if sc is None:
        sc = 400.0 / top
    ox, y = 18, 58
    W = ox + top * sc + 22
    s = ["<line x1='%d' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (ox - 6, y, ox + top * sc + 12, y, INK)]
    for k in range(n + 1):
        x = ox + k * d * sc
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 7, x, y + 7, INK))
        lab = "?" if k == hide else str(k * d)
        s.append(text(x, y + 27, lab, 15, col=RED if k == hide else INK))
        if k < n:
            x2 = ox + (k + 1) * d * sc
            xm = (x + x2) / 2
            s.append("<path d='M%.1f %d Q%.1f %d %.1f %d' fill='none' stroke='%s' stroke-width='2'/>"
                     % (x + 2, y - 9, xm, y - 42, x2 - 2, y - 9, GREEN))
    return svg_wrap(W, y + 36, "".join(s), "number line counting in %ds" % d)


def model_svg(rows, total_lab, total, k, label):
    """Bar model: rows = [(name, size, colour)]. Every bar is total long and cut into units of size,
    drawn to scale (k px per 1). A bracket on the right shows total_lab."""
    fs = 15
    lw = max(tw(r[0], fs) for r in rows) + 12
    x0 = 6 + lw
    bh, gap, top = 30, 12, 6
    s = []
    for i, (name, size, col) in enumerate(rows):
        assert total % size == 0
        y = top + i * (bh + gap)
        s.append(text(x0 - 8, y + bh / 2 + 5.5, name, fs, "end"))
        for j in range(total // size):
            x = x0 + j * size * k
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, size * k, bh, col, INK))
            s.append(text(x + size * k / 2, y + bh / 2 + 5.5, str(size) if isinstance(size, int) else size, fs))
    ybot = top + len(rows) * (bh + gap) - gap
    xb = x0 + total * k + 10
    s.append("<path d='M%.1f %d h8 V%d h-8' fill='none' stroke='%s' stroke-width='2'/>" % (xb, top, ybot, INK))
    s.append(text(xb + 14, (top + ybot) / 2 + 5.5, total_lab, fs, "start", RED if total_lab == "?" else INK))
    W = xb + 14 + tw(total_lab, fs) + 6
    return svg_wrap(W, ybot + 6, "".join(s), label)


def model_cm_svg(rows, total, k, label):
    """Bar model for lengths in cm: like model_svg, with 'N cm' in each unit."""
    fs = 15
    lw = max(tw(r[0], fs) for r in rows) + 12
    x0 = 6 + lw
    bh, gap, top = 30, 12, 6
    s = []
    for i, (name, size, col) in enumerate(rows):
        assert total % size == 0
        y = top + i * (bh + gap)
        s.append(text(x0 - 8, y + bh / 2 + 5.5, name, fs, "end"))
        for j in range(total // size):
            x = x0 + j * size * k
            s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>"
                     % (x, y, size * k, bh, col, INK))
            s.append(text(x + size * k / 2, y + bh / 2 + 5.5, "%d cm" % size, fs))
    ybot = top + len(rows) * (bh + gap) - gap
    xb = x0 + total * k + 10
    s.append("<path d='M%.1f %d h8 V%d h-8' fill='none' stroke='%s' stroke-width='2'/>" % (xb, top, ybot, INK))
    s.append(text(xb + 14, (top + ybot) / 2 + 5.5, "?", fs, "start", RED))
    W = xb + 14 + tw("?", fs) + 6
    return svg_wrap(W, ybot + 6, "".join(s), label)


# ============================================================ set 1: factors and factor pairs
def set_factors():
    its = []
    for x in [12, 18, 20, 30]:
        fs = factors(x)
        prs = pairs(x)
        mid = prs[-1]
        no_mid = [d for d in fs if d not in mid]
        no_ends = fs[1:-1]
        ms = mults(x, 4 * x)
        e = ("Find the factor pairs: %s. So the factors of %d are <b>%s</b>. Do not forget 1 and %d, "
             "and do not leave out the pair %d × %d. %s are multiples of %d, not factors."
             % (", ".join("%d × %d" % p for p in prs), x, lst(fs), x, mid[0], mid[1], lst(ms), x))
        its.append(mcq("Which list shows <b>all</b> the factors of %d?" % x, lst(fs), [lst(no_mid), lst(no_ends), lst(ms)], e))

    assert factors(16) == [1, 2, 4, 8, 16]
    its.append(mcq("How many factors does 16 have?", 5, [6, 3, 4],
                   "The factors of 16 are 1, 2, 4, 8 and 16. That is <b>5 factors</b>. 4 × 4 = 16, so 4 is counted "
                   "only once. Counting 4 twice gives 6, leaving out 1 and 16 gives 3, and leaving out 16 gives 4."))
    assert len(factors(24)) == 8 and len(pairs(24)) == 4
    its.append(mcq("How many factors does 24 have?", 8, [4, 6, 7],
                   "The factor pairs are 1 × 24, 2 × 12, 3 × 8 and 4 × 6, so 24 has <b>8 factors</b>: %s. "
                   "4 is the number of pairs. Leaving out 1 and 24 gives 6, and leaving out 24 gives 7." % lst(factors(24))))

    for r, c, wrong in [(3, 6, ["2 × 9", "3 × 5", "4 × 6"]), (4, 5, ["2 × 10", "4 × 4", "5 × 5"]),
                        (4, 9, ["6 × 6", "3 × 9", "4 × 8"])]:
        x = r * c
        e = ("Count the rows and the counters in each row: %d rows of %d. So the array shows <b>%d × %d</b> = %d. "
             "%s is also a factor pair of %d, but it is not this array." % (r, c, r, c, x, wrong[0], x))
        assert x % int(wrong[0].split(" × ")[0]) == 0 and eval(wrong[0].replace("×", "*")) == x
        assert all(eval(w.replace("×", "*")) != x for w in wrong[1:])
        its.append(mcq(fig(array_svg(r, c)) + "This array has %d counters. Which factor pair of %d does it show?" % (x, x),
                       "%d × %d" % (r, c), wrong, e))

    assert 12 % 5 and all(12 % v == 0 for v in (2, 3, 1))
    its.append(mcq("Mrs Lim puts 12 chairs in equal rows. Which of these is <b>not</b> possible?", "5 rows",
                   ["2 rows", "3 rows", "1 row"],
                   "12 ÷ 5 = 2 R 2, so 5 rows is <b>not</b> possible: 5 is not a factor of 12. "
                   "2 rows of 6, 3 rows of 4 and 1 row of 12 all work."))
    assert 24 % 5 and all(24 % v == 0 for v in (3, 4, 6))
    its.append(mcq("Kumar puts 24 stamps on a page in equal rows. Which number of rows is <b>not</b> possible?",
                   "5 rows", ["3 rows", "4 rows", "6 rows"],
                   "24 ÷ 5 = 4 R 4, so <b>5 rows</b> is not possible. 3 rows of 8, 4 rows of 6 and 6 rows of 4 all work."))

    for x, shown, ans, wrong, note in [
            (36, "1 × 36, 2 × 18, 3 × ?, 4 × 9, 6 × 6", 12, [11, 13, 33],
             "3 × 11 = 33 and 3 × 13 = 39. 33 is 36 − 3: we multiply, not subtract."),
            (40, "1 × 40, 2 × 20, 4 × ?, 5 × 8", 10, [36, 20, 9],
             "36 is 40 − 4: we multiply, not subtract. 20 is already in the pair 2 × 20, and 4 × 9 = 36."),
            (30, "1 × 30, 2 × 15, 3 × 10, ? × 6", 5, [4, 24, 3],
             "4 × 6 = 24 and 3 × 6 = 18. 24 is 30 − 6: we multiply, not subtract.")]:
        assert len(shown.split(", ")) == len(pairs(x))
        for p in shown.split(", "):
            if "?" not in p:
                u, v = map(int, p.split(" × "))
                assert u * v == x
            else:
                other = int([v for v in p.split(" × ") if v != "?"][0])
        assert other * ans == x and all(other * w != x for w in wrong)
        e = "%d × %d = %d, so the missing number is <b>%d</b>. %s" % (other, ans, x, ans, note)
        its.append(mcq("These are the factor pairs of %d: %s. What is the missing number?" % (x, shown), ans, wrong, e))

    assert 6 * 7 == 42 and 5 * 8 == 40 and 4 * 12 == 48 and 3 * 12 == 36
    its.append(mcq("Which of these is a factor pair of 42?", "6 × 7", ["5 × 8", "4 × 12", "3 × 12"],
                   "6 × 7 = 42, so <b>6 × 7</b> is a factor pair of 42. 5 × 8 = 40, 4 × 12 = 48 and 3 × 12 = 36."))

    its.append(mcq("Which number is a factor of <b>every</b> whole number?", 1, [0, 2, 10],
                   "Every number can be written as 1 × itself, for example 7 = 1 × 7. So <b>1</b> is a factor of "
                   "every number. 2 is not a factor of odd numbers, and 10 is not a factor of 7."))
    assert factors(45)[-2] == 15
    its.append(mcq("What is the greatest factor of 45?", 45, [15, 9, 90],
                   "45 = 1 × 45, so the greatest factor of 45 is <b>45</b> itself. 15 is the next greatest factor. "
                   "90 is a multiple of 45, not a factor. A factor is never greater than the number."))
    assert factors(15) == [1, 3, 5, 15]
    its.append(mcq("Ali says the factors of 15 are 3 and 5. Is he right?", "No. 1 and 15 are factors too",
                   ["Yes. 3 × 5 = 15", "No. 30 is a factor too", "No. 2 is a factor too"],
                   "15 = 1 × 15 and 15 = 3 × 5, so the factors of 15 are 1, 3, 5 and 15. Ali forgot <b>1 and 15</b>. "
                   "30 is a multiple of 15, and 15 ÷ 2 = 7 R 1."))
    assert factors(28) == [1, 2, 4, 7, 14, 28]
    its.append(mcq("Siti lists the factors of 28: 1, 2, 4, 14, 28. Which factor is missing?", 7, [3, 6, 56],
                   "The factor pairs of 28 are 1 × 28, 2 × 14 and 4 × 7. Siti has 4 but not its partner, <b>7</b>. "
                   "28 ÷ 3 and 28 ÷ 6 have remainders, and 56 is a multiple of 28."))
    its.append(mcq("Which list shows <b>all</b> the factor pairs of 18?", "1 × 18, 2 × 9, 3 × 6",
                   ["2 × 9, 3 × 6", "1 × 18, 2 × 9", "1 × 18, 2 × 9, 4 × 5"],
                   "Try 1, 2, 3, … in order: 1 × 18, 2 × 9 and 3 × 6. 4 and 5 are not factors of 18 (4 × 5 = 20). "
                   "So the answer is <b>1 × 18, 2 × 9, 3 × 6</b>. Do not leave out 1 × 18."))
    assert pairs(18) == [(1, 18), (2, 9), (3, 6)]
    order = [0, 1, 4, 2, 5, 6, 7, 8, 13, 14, 9, 10, 11, 12, 15, 3, 16, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Factors and factor pairs", "items": its}


# ============================================================ set 2: is it a factor?
def set_is_factor():
    its = []
    assert 85 % 5 == 0 and all(v % 5 for v in (58, 52, 57))
    its.append(mcq("Which number has 5 as a factor?", 85, [58, 52, 57],
                   "85 ÷ 5 = 17, so 5 is a factor of <b>85</b>. Numbers with 5 as a factor end in 0 or 5. "
                   "58, 52 and 57 do not."))
    its.append(mcq(fig(groups_svg(42, 6)) + "42 counters are put into groups of 6. What does the picture show?",
                   "6 is a factor of 42", ["42 is a factor of 6", "6 is a multiple of 42", "7 is a multiple of 42"],
                   "There are 7 groups of 6 and none left over: 42 ÷ 6 = 7. So <b>6 is a factor of 42</b> (and 7 is too). "
                   "42 is a multiple of 6, not a factor of 6."))
    assert divmod(26, 4) == (6, 2)
    its.append(mcq(fig(groups_svg(26, 4)) + "26 counters are put into groups of 4. What does the picture show?",
                   "4 is not a factor of 26", ["4 is a factor of 26", "26 is a multiple of 4", "2 is not a factor of 26"],
                   "There are 6 groups of 4 and 2 left over: 26 ÷ 4 = 6 R 2. A remainder means <b>4 is not a factor of 26</b>, "
                   "and 26 is not a multiple of 4. 2 is a factor of 26 (26 ÷ 2 = 13)."))
    for x, right, wrong in [(48, 6, [5, 7, 9]), (63, 9, [4, 6, 8]), (45, 5, [2, 4, 7]), (56, 8, [3, 5, 6])]:
        assert x % right == 0 and all(x % w for w in wrong)
        e = ("%s, so <b>%d</b> is a factor of %d. %s." % (divs(x, right), right, x, ", ".join(divs(x, w) for w in wrong)))
        e += " A remainder means it is not a factor."
        its.append(mcq("Which number is a factor of %d?" % x, right, wrong, e))
    for x, bad, good in [(60, 7, [4, 5, 6]), (84, 5, [3, 4, 7]), (90, 4, [5, 6, 9]), (72, 5, [6, 8, 9])]:
        assert x % bad and all(x % g == 0 for g in good)
        e = ("%s, so <b>%d</b> is not a factor of %d. %s." % (divs(x, bad), bad, x, ", ".join(divs(x, g) for g in good)))
        its.append(mcq("Which number is <b>not</b> a factor of %d?" % x, bad, good, e))
    assert divmod(34, 6) == (5, 4)
    its.append(mcq("Is 6 a factor of 34?", "No. 34 ÷ 6 = 5 R 4",
                   ["Yes. 34 is even", "Yes. 34 ÷ 6 = 6", "No. 6 is a multiple of 34"],
                   "6 × 5 = 30 and 6 × 6 = 36, so 34 ÷ 6 = 5 R 4. There is a remainder, so <b>6 is not a factor of 34</b>. "
                   "Being even only tells us 2 is a factor."))
    assert 52 % 4 == 0 and all(v % 4 for v in (42, 54, 46))
    its.append(mcq("Which of these numbers has 4 as a factor?", 52, [42, 54, 46],
                   "52 ÷ 4 = 13, so 4 is a factor of <b>52</b>. 42, 54 and 46 are even, but each leaves a remainder 2 "
                   "when divided by 4. Even does not mean 4 is a factor."))
    assert 36 % 12 == 0 and 32 % 3 and 27 % 4 and 34 % 3 and 34 % 4
    its.append(mcq("Which number has both 3 and 4 as factors?", 36, [32, 27, 34],
                   "36 = 3 × 12 and 36 = 4 × 9, so <b>36</b> has both. 32 has 4 but not 3, 27 has 3 but not 4, "
                   "and 34 has neither: 34 ÷ 3 = 11 R 1 and 34 ÷ 4 = 8 R 2."))
    its.append(mcq("Which division has <b>no</b> remainder?", "72 ÷ 8", ["74 ÷ 8", "58 ÷ 6", "47 ÷ 9"],
                   "<b>72 ÷ 8 = 9</b>, so 8 is a factor of 72. %s, %s and %s." % (divs(74, 8), divs(58, 6), divs(47, 9))))
    assert 81 % 9 == 0 and all(v % 9 for v in (79, 91, 89))
    its.append(mcq("9 is a factor of which number?", 81, [79, 91, 89],
                   "9 × 9 = 81, so 9 is a factor of <b>81</b>. %s, %s and %s. The last digit does not tell you."
                   % (divs(79, 9), divs(91, 9), divs(89, 9))))
    assert 64 % 8 == 0 and 60 % 8 and 64 % 6
    its.append(mcq("Which statement is true?", "8 is a factor of 64",
                   ["8 is a factor of 60", "64 is a factor of 8", "6 is a factor of 64"],
                   "8 × 8 = 64, so <b>8 is a factor of 64</b>. %s and %s. 64 is a multiple of 8, not a factor of 8."
                   % (divs(60, 8), divs(64, 6))))
    assert [d for d in (2, 3, 4, 5, 6) if 30 % d == 0] == [2, 3, 5, 6]
    its.append(mcq("How many of the numbers 2, 3, 4, 5 and 6 are factors of 30?", 4, [5, 3, 2],
                   "30 ÷ 2 = 15, 30 ÷ 3 = 10, 30 ÷ 5 = 6 and 30 ÷ 6 = 5, but 30 ÷ 4 = 7 R 2. "
                   "So <b>4</b> of them are factors: 2, 3, 5 and 6."))
    its.append(mcq("Raju says 4 is a factor of 30 because 30 is even. Is he right?", "No. 30 ÷ 4 = 7 R 2",
                   ["Yes. 30 is even", "Yes. 4 × 7 = 30", "No. 4 is a multiple of 30"],
                   "4 × 7 = 28 and 4 × 8 = 32, so 30 ÷ 4 = 7 R 2. <b>4 is not a factor of 30</b>. "
                   "Even numbers have 2 as a factor, but not always 4."))
    assert [v for v in range(51, 60) if v % 7 == 0] == [56]
    its.append(mcq("Which number between 50 and 60 has 7 as a factor?", 56, [57, 54, 58],
                   "7 × 8 = 56, so the answer is <b>56</b>. 57 ends in 7, but 57 ÷ 7 = 8 R 1. "
                   "%s and %s." % (divs(54, 7), divs(58, 7))))
    order = [0, 1, 2, 3, 4, 5, 6, 11, 7, 8, 9, 10, 15, 16, 12, 13, 14, 17, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Is it a factor?", "items": its}


# ============================================================ set 3: common factors
def cf_e(a, b):
    return ("Factors of %d: %s. Factors of %d: %s. The numbers in <b>both</b> lists are %s."
            % (a, lst(factors(a)), b, lst(factors(b)), lst(cfs(a, b))))


def set_common_factors():
    its = []
    for a, b in [(12, 18), (16, 24)]:
        c = cfs(a, b)
        e = ("The circled numbers are in both rows, so the common factors are <b>%s</b>. Do not forget 1, "
             "and list every common factor, not only the greatest one." % lst(c))
        its.append(mcq(fig(factor_rows_svg(a, b)) + "The common factors of %d and %d are circled. "
                       "Which list shows <b>all</b> the common factors?" % (a, b), lst(c),
                       [lst(c[1:]), str(c[-1]), lst(factors(a))], e))
    for a, b in [(8, 12), (20, 30), (15, 25), (18, 27)]:
        c = cfs(a, b)
        cands = [lst(c[1:]), str(c[-1]), lst(factors(a)), lst(c[:-1])]
        e = cf_e(a, b) + " Remember 1 is always a common factor, and list them all."
        its.append(mcq("Which list shows <b>all</b> the common factors of %d and %d?" % (a, b), lst(c), cands, e))
    for a, b, right, wrong in [(24, 36, 4, [8, 9, 72]), (30, 45, 5, [6, 9, 90]), (28, 42, 7, [4, 6, 84])]:
        assert right in cfs(a, b) and a % wrong[0] == 0 and b % wrong[0] and b % wrong[1] == 0 and a % wrong[1]
        assert wrong[2] == L(a, b)
        e = ("%d = %d × %d and %d = %d × %d, so <b>%d</b> is a common factor. %d is a factor of %d only, "
             "and %d is a factor of %d only. %d is a common <b>multiple</b>, not a factor."
             % (a, right, a // right, b, right, b // right, right, wrong[0], a, wrong[1], b, wrong[2]))
        its.append(mcq("Which number is a common factor of %d and %d?" % (a, b), right, wrong, e))
    for a, b, bad, good in [(18, 30, 9, [2, 3, 6]), (24, 40, 3, [2, 4, 8])]:
        assert bad not in cfs(a, b) and all(g in cfs(a, b) for g in good) and a % bad == 0
        e = cf_e(a, b) + " %d is a factor of %d, but %s, so <b>%d</b> is not a common factor." % (bad, a, divs(b, bad), bad)
        its.append(mcq("Which number is <b>not</b> a common factor of %d and %d?" % (a, b), bad, good, e))
    assert cfs(12, 30) == [1, 2, 3, 6]
    its.append(mcq("How many common factors do 12 and 30 have?", 4, [3, 6, 1],
                   cf_e(12, 30) + " That is <b>4</b> common factors. Leaving out 1 gives 3. 6 is the greatest one, not how many."))
    assert cfs(20, 28) == [1, 2, 4]
    its.append(mcq("How many common factors do 20 and 28 have?", 3, [2, 4, 6],
                   cf_e(20, 28) + " That is <b>3</b> common factors. Leaving out 1 gives 2. 4 is the greatest one, "
                   "and 6 is how many factors 20 has."))
    assert cfs(12, 20)[-1] == 4 and L(12, 20) == 60
    its.append(mcq("What is the greatest number that is a factor of both 12 and 20?", 4, [2, 60, 12],
                   cf_e(12, 20) + " The greatest is <b>4</b>. 2 is a common factor, but not the greatest. "
                   "60 is a common multiple, and 12 is not a factor of 20."))
    assert cfs(18, 24)[-1] == 6 and L(18, 24) == 72
    its.append(mcq("What is the greatest number that is a factor of both 18 and 24?", 6, [3, 72, 2],
                   cf_e(18, 24) + " The greatest is <b>6</b>. 3 and 2 are common factors too, but smaller. "
                   "72 is a common multiple."))
    assert 6 in cfs(12, 18) and 6 not in cfs(6, 15) and 6 not in cfs(3, 6) and 6 not in cfs(16, 26)
    its.append(mcq("Which two numbers have 6 as a common factor?", "12 and 18", ["6 and 15", "3 and 6", "16 and 26"],
                   "12 = 6 × 2 and 18 = 6 × 3, so 6 is a common factor of <b>12 and 18</b>. 15 ÷ 6 = 2 R 3, "
                   "6 is not a factor of 3, and 16 and 26 only end in 6."))
    assert cfs(8, 9) == [1] and cfs(6, 9) == [1, 3] and cfs(4, 10) == [1, 2] and cfs(9, 12) == [1, 3]
    its.append(mcq("Which two numbers have <b>only 1</b> as a common factor?", "8 and 9", ["6 and 9", "4 and 10", "9 and 12"],
                   "Factors of 8: 1, 2, 4, 8. Factors of 9: 1, 3, 9. Only 1 is in both, so the answer is <b>8 and 9</b>. "
                   "6 and 9 share 3, 4 and 10 share 2, and 9 and 12 share 3."))
    assert cfs(12, 16) == [1, 2, 4]
    its.append(mcq("Jun Jie says the common factors of 12 and 16 are 2 and 4. Which common factor did he miss?", 1,
                   [8, 3, 48],
                   cf_e(12, 16) + " Jun Jie missed <b>1</b>. 8 is a factor of 16 only, 3 is a factor of 12 only, "
                   "and 48 is a common multiple."))
    assert cfs(20, 30) == [1, 2, 5, 10]
    its.append(mcq("Priya says the only common factor of 20 and 30 is 10. Is she right?",
                   "No. 1, 2, 5 and 10 are common factors",
                   ["Yes. 10 is the only one", "No. 1 and 10 are the only ones", "No. 60 is a common factor too"],
                   cf_e(20, 30) + " 10 is the greatest, but there are 4 common factors. 60 is a common multiple."))
    assert 28 % 4 == 0 and 36 % 4 == 0
    its.append(mcq("Is 4 a common factor of 28 and 36?", "Yes. 28 = 4 × 7 and 36 = 4 × 9",
                   ["No. 4 is a factor of 28 only", "No. 4 is a factor of 36 only", "No. 36 ÷ 4 has a remainder"],
                   "28 ÷ 4 = 7 and 36 ÷ 4 = 9 with no remainders, so <b>4 is a common factor</b> of 28 and 36."))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 18, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Common factors", "items": its}


# ============================================================ set 4: multiples
def set_multiples():
    its = []
    for d in [6, 7]:
        right = [d * k for k in range(1, 6)]
        wrong = [[0] + right[:4], factors(d) if len(factors(d)) > 2 else [1, d, d + 1, d + 2],
                 [d + 10 * k for k in range(5)]]
        assert all(w != right for w in wrong)
        e = ("Multiply %d by 1, 2, 3, 4 and 5: <b>%s</b>. The first multiple of a number is the number itself, "
             "not 0. Count on in %ds, not in 10s." % (d, lst(right), d))
        if d == 6:
            e += " 1, 2, 3, 6 are the factors of 6, not multiples."
        wrong[1] = factors(6) if d == 6 else [7, 14, 21, 27, 35]
        if d == 7:
            e += " 27 is not a multiple of 7 (7 × 4 = 28)."
        its.append(mcq("Which list shows the first five multiples of %d?" % d, lst(right), [lst(w) for w in wrong], e))
    for d, n, hide, wrong in [(4, 10, 7, [26, 30, 24]), (9, 6, 4, [35, 27, 45])]:
        ans = d * hide
        e = ("Count on in %ds from 0: %s. The missing number is <b>%d</b> (%d × %d)."
             % (d, lst(mults(d, d * n)), ans, d, hide))
        its.append(mcq(fig(skip_line_svg(d, n, hide)) + "The jumps are all the same size. What number is at ?",
                       ans, wrong, e))
    for d, right, wrong in [(6, 42, [3, 46, 40]), (8, 64, [4, 68, 60]), (9, 54, [3, 59, 49])]:
        assert right % d == 0 and all(w % d for w in wrong[1:]) and d % wrong[0] == 0
        e = ("%d × %d = %d, so <b>%d</b> is a multiple of %d. %d is a <b>factor</b> of %d, not a multiple. "
             "%s and %s. Ending in %d does not make a number a multiple of %d."
             % (d, right // d, right, right, d, wrong[0], d, divs(wrong[1], d), divs(wrong[2], d), d, d))
        its.append(mcq("Which number is a multiple of %d?" % d, right, wrong, e))
    assert 54 % 7 and all(v % 7 == 0 for v in (42, 63, 77))
    its.append(mcq("Which number is <b>not</b> a multiple of 7?", 54, [42, 63, 77],
                   "54 ÷ 7 = 7 R 5, so <b>54</b> is not a multiple of 7. 42 = 7 × 6, 63 = 7 × 9 and 77 = 7 × 11."))
    assert 34 % 4 and all(v % 4 == 0 for v in (24, 36, 48))
    its.append(mcq("Which number is <b>not</b> a multiple of 4?", 34, [24, 36, 48],
                   "34 ÷ 4 = 8 R 2, so <b>34</b> is not a multiple of 4. 24 = 4 × 6, 36 = 4 × 9 and 48 = 4 × 12. "
                   "34 is even, but that is not enough."))
    its.append(mcq("What is the 8th multiple of 6?", 48, [42, 54, 14],
                   "The 8th multiple of 6 is 6 × 8 = <b>48</b>. 42 is the 7th multiple and 54 is the 9th. "
                   "14 is 6 + 8: we multiply, not add."))
    its.append(mcq("What is the 10th multiple of 9?", 90, [81, 99, 19],
                   "The 10th multiple of 9 is 9 × 10 = <b>90</b>. 81 is the 9th multiple and 99 is the 11th. "
                   "19 is 9 + 10."))
    its.append(mcq("Which statement is true?", "36 is a multiple of 9",
                   ["9 is a multiple of 36", "36 is a factor of 9", "3 is a multiple of 9"],
                   "9 × 4 = 36, so <b>36 is a multiple of 9</b>, and 9 is a factor of 36. "
                   "A multiple is never smaller than the number. A factor is never bigger."))
    its.append(mcq("Ahmad says 4 is a multiple of 12 because 12 ÷ 4 = 3. Is he right?", "No. 4 is a factor of 12",
                   ["Yes. 12 ÷ 4 = 3", "Yes. 4 × 3 = 12", "No. 4 is a multiple of 3"],
                   "12 ÷ 4 = 3 with no remainder, so 4 is a <b>factor</b> of 12, and 12 is a multiple of 4. "
                   "The multiples of 12 are 12, 24, 36, … They are never smaller than 12."))
    assert [v for v in range(21, 50) if v % 6 == 0] == [24, 30, 36, 42, 48]
    its.append(mcq("How many multiples of 6 are there between 20 and 50?", 5, [4, 6, 3],
                   "Count in 6s: 6, 12, 18, <b>24, 30, 36, 42, 48</b>, 54. Five of them are between 20 and 50. "
                   "Do not leave out 48, and do not count 18 or 54."))
    its.append(mcq("Is 8 a multiple of 8?", "Yes. 8 × 1 = 8",
                   ["No. A multiple must be bigger", "No. 8 is only a factor of 8", "No. The first multiple is 16"],
                   "8 × 1 = 8, so 8 is the <b>first multiple</b> of 8. Every number is a multiple of itself, "
                   "and also a factor of itself."))
    assert [v for v in range(51, 70) if v % 7 == 0][0] == 56
    its.append(mcq("What is the smallest multiple of 7 that is greater than 50?", 56, [49, 57, 63],
                   "7 × 7 = 49 and 7 × 8 = 56. 49 is less than 50, so the answer is <b>56</b>. "
                   "57 ends in 7, but 57 ÷ 7 = 8 R 1. 63 is a multiple of 7, but not the smallest one after 50."))
    assert 35 % 5 == 0 and 35 % 10 and 53 % 5
    its.append(mcq("Which number is a multiple of 5 but <b>not</b> a multiple of 10?", 35, [50, 30, 53],
                   "Multiples of 5 end in 0 or 5. Multiples of 10 end in 0. So <b>35</b> is a multiple of 5 but not of 10. "
                   "50 and 30 are multiples of both, and 53 is not a multiple of 5."))
    its.append(mcq("Zhi Hao counts in 8s: 8, 16, 24, 30, 40. Which number is wrong?", 30, [16, 24, 40],
                   "8 × 4 = 32, so the 4th number should be 32, not <b>30</b>. 16 = 8 × 2, 24 = 8 × 3 and 40 = 8 × 5."))
    assert 46 % 7 == 4
    its.append(mcq("Hui Min counts in 7s from 7. Will she say 46?", "No. 46 ÷ 7 = 6 R 4",
                   ["Yes. 7 × 6 = 46", "No. 46 is even", "Yes. 46 is between 42 and 49"],
                   "7 × 6 = 42 and 7 × 7 = 49. 46 is between them, so <b>46 is not a multiple of 7</b>. "
                   "Being even is not the reason: 42 is even and is a multiple of 7."))
    its.append(mcq("Which list has <b>only</b> multiples of 9?", "18, 36, 54, 72",
                   ["9, 19, 29, 39", "1, 3, 9", "18, 27, 36, 46"],
                   "18 = 9 × 2, 36 = 9 × 4, 54 = 9 × 6 and 72 = 9 × 8, so the answer is <b>18, 36, 54, 72</b>. "
                   "19, 29 and 39 only end in 9. 1, 3 and 9 are the factors of 9. 46 is not a multiple of 9."))
    assert all(v % 9 == 0 for v in (18, 36, 54, 72))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 13, 14, 17, 16, 18, 19]
    its = [its[i] for i in order]
    assert len(its) == 20, len(its)
    return {"title": "Multiples", "items": its}


# ============================================================ set 5: common multiples and word problems
def first_cm_e(a, b):
    lo, hi = sorted((a, b))
    l = L(a, b)
    return ("Count in %ds: %s. The first one that is also a multiple of %d is <b>%d</b>."
            % (hi, lst(mults(hi, l)), lo, l))


def set_common_multiples():
    its = []
    com = [m for m in range(1, 37) if m % 4 == 0 and m % 6 == 0]
    assert com == [12, 24, 36]
    its.append(mcq(fig(multiples_svg(4, 6, 36)) + "Which numbers in the picture are common multiples of 4 and 6?",
                   "12, 24, 36", ["24", "12", "4, 6"],
                   "Look for numbers in <b>both</b> rows. Multiples of 4: %s. Multiples of 6: %s. "
                   "The common multiples are <b>12, 24, 36</b>. Not only 4 × 6 = 24, and not only the first one."
                   % (lst(mults(4, 36)), lst(mults(6, 36)))))
    assert L(3, 5) == 15
    its.append(mcq(fig(multiples_svg(3, 5, 30, sc=10)) + "Use the picture. What is the first common multiple of 3 and 5?",
                   15, [8, 30, 5],
                   "The first number in <b>both</b> rows is <b>15</b>. 30 is a common multiple too, but not the first. "
                   "8 is 3 + 5, and 5 is a multiple of 5 only."))
    assert L(6, 9) == 18
    its.append(mcq("Which list shows the first three common multiples of 6 and 9?", "18, 36, 54",
                   ["54, 108, 162", "6, 9, 18", "9, 18, 27"],
                   "Count in 9s: 9, 18. 18 = 6 × 3, so the first common multiple is 18. Then count in 18s: "
                   "<b>18, 36, 54</b>. 6 × 9 = 54 is a common multiple, but not the first. 9 and 27 are not multiples of 6."))
    for a, b, wrong in [(6, 8, [48, 14, 16]), (4, 8, [32, 12, 16]), (4, 5, [40, 9, 10])]:
        l = L(a, b)
        assert all(w != l for w in wrong)
        if b % a == 0:
            e = ("%d = %d × %d, so %d is already a multiple of %d. The first common multiple is <b>%d</b>. "
                 "When one number is a multiple of the other, the bigger number is the first common multiple."
                 % (b, a, b // a, b, a, l))
        else:
            e = first_cm_e(a, b)
        why = []
        for w in wrong:
            if w == a * b:
                why.append("%d × %d = %d is a common multiple, but not the first" % (a, b, w))
            elif w == a + b:
                why.append("%d is %d + %d" % (w, a, b))
            elif w % a == 0 and w % b == 0:
                why.append("%d is a common multiple, but not the first" % w)
            else:
                only = b if w % b == 0 else a
                assert w % only == 0
                why.append("%d is a multiple of %d only" % (w, only))
        e += " " + ". ".join(cap(x) for x in why) + "."
        its.append(mcq("What is the first common multiple of %d and %d?" % (a, b), l, wrong, e))
    assert 36 % 4 == 0 and 36 % 6 == 0 and 16 % 6 and 18 % 4 and 10 % 4
    its.append(mcq("Which number is a common multiple of 4 and 6?", 36, [16, 18, 10],
                   "36 = 4 × 9 and 36 = 6 × 6, so <b>36</b> is a common multiple. 16 is a multiple of 4 only, "
                   "18 is a multiple of 6 only, and 10 is 4 + 6."))

    # word problems
    assert L(6, 8) == 24
    its.append(mcq(fig(model_svg([("Buns", 6, FILL_Y), ("Sausages", 8, FILL_B)], "?", 24, 12, "bar model of packets of 6 and 8"))
                   + "Buns come in packets of 6 and sausages in packets of 8. Ethan wants the same number of buns and "
                   "sausages for a barbecue at East Coast Park. What is the least number of each he can buy?",
                   "24 of each", ["48 of each", "14 of each", "12 of each"],
                   first_cm_e(6, 8) + " The two bars are the same length at 24: 4 packets of buns and 3 packets of "
                   "sausages. 6 × 8 = 48 also works, but it is not the least. 14 is 6 + 8, and 12 is not a multiple of 8."))
    its.append(mcq("Buns come in packets of 6 and sausages in packets of 8. Mei Ling buys the least number of packets "
                   "so that she has the same number of buns and sausages. How many packets of buns does she buy?",
                   "4 packets", ["3 packets", "24 packets", "6 packets"],
                   "The first common multiple of 6 and 8 is 24, so she needs 24 buns: 24 ÷ 6 = <b>4 packets</b>. "
                   "3 packets is for the sausages (24 ÷ 8). 24 is the number of buns, not packets."))
    assert L(6, 8) == 24
    its.append(mcq("At a bus interchange, Bus A leaves every 6 minutes and Bus B leaves every 8 minutes. Both buses "
                   "leave at 7.00 am. When will they next leave at the same time?",
                   am(7, 24), [am(7, 48), am(7, 14), am(7, 8)],
                   first_cm_e(6, 8) + " So they leave together again 24 min later, at <b>7.24 am</b>. "
                   "7.48 am uses 6 × 8 = 48 min, 7.14 am uses 6 + 8 = 14 min, and at 7.08 am only Bus B leaves."))
    assert L(5, 6) == 30
    its.append(mcq("Bus 12 leaves a stop every 5 minutes and Bus 21 leaves every 6 minutes. Both leave together at "
                   "3.30 pm. When will they next leave together?",
                   pm(4, 0), [pm(3, 41), pm(3, 36), pm(3, 35)],
                   first_cm_e(5, 6) + " 30 min after 3.30 pm is <b>4.00 pm</b>. 3.41 pm uses 5 + 6 = 11 min. "
                   "At 3.36 pm only Bus 21 leaves, and at 3.35 pm only Bus 12 leaves."))
    assert L(4, 6) == 12
    its.append(mcq("At Gardens by the Bay, a red light flashes every 4 seconds and a blue light flashes every 6 seconds. "
                   "They flash together now. After how many seconds will they next flash together?",
                   "12 s", ["24 s", "10 s", "2 s"],
                   first_cm_e(4, 6) + " So they flash together after <b>12 s</b>. 24 s is 4 × 6: a common multiple, "
                   "but not the first. 10 s is 4 + 6, and 2 is a common factor."))
    assert L(6, 9) == 18
    its.append(mcq(fig(model_cm_svg([("Siti", 6, FILL_Y), ("Hafiz", 9, FILL_B)], 18, 14, "bar model of blocks 6 cm and 9 cm"))
                   + "Siti stacks blocks that are each 6 cm tall. Hafiz stacks blocks that are each 9 cm tall. "
                   "Their towers are the same height. What is the smallest possible height?",
                   "18 cm", ["54 cm", "15 cm", "36 cm"],
                   first_cm_e(6, 9) + " The towers are both <b>18 cm</b>: 3 blocks for Siti and 2 for Hafiz. "
                   "54 cm (6 × 9) and 36 cm are also the same height, but not the smallest. 15 cm is 6 + 9."))
    assert L(4, 6) == 12
    its.append(mcq("Nurul has swimming every 4 days and art lessons every 6 days. She has both on 3 March. "
                   "On what date will she next have both?",
                   "15 March", ["27 March", "13 March", "5 March"],
                   first_cm_e(4, 6) + " 3 March + 12 days = <b>15 March</b>. 27 March uses 4 × 6 = 24 days, "
                   "13 March uses 4 + 6 = 10 days, and 5 March uses 2 days (a common factor)."))
    assert L(6, 8) == 24
    its.append(mcq("Mrs Ng has some sweets. She can share them equally among 6 children or among 8 children, with "
                   "none left over. What is the smallest number of sweets she can have?",
                   "24 sweets", ["48 sweets", "14 sweets", "2 sweets"],
                   "The number of sweets must be a multiple of 6 and of 8. " + first_cm_e(6, 8)
                   + " 48 also works, but it is not the smallest. 14 is 6 + 8, and 2 is a common factor."))
    assert [m for m in range(1, 50) if m % 4 == 0 and m % 9 == 0] == [36]
    its.append(mcq("The P4 students can be put into groups of 4 or groups of 9 with no one left out. There are fewer "
                   "than 50 students. How many students are there?",
                   36, [13, 45, 40],
                   "The number must be a common multiple of 4 and 9. Count in 9s: 9, 18, 27, <b>36</b>, 45. "
                   "36 = 4 × 9 is the only one less than 50 that is also a multiple of 4. 45 and 40 are multiples of "
                   "one number only, and 13 is 4 + 9."))
    assert cfs(18, 24) == [1, 2, 3, 6]
    its.append(mcq("Mr Rahman has 18 apples and 24 oranges. He packs them into bags. Every bag has the same number of "
                   "apples and the same number of oranges, with none left over. What is the greatest number of bags?",
                   "6 bags", ["3 bags", "2 bags", "72 bags"],
                   "The number of bags must be a common factor of 18 and 24: 1, 2, 3 and 6. The greatest is <b>6</b>, "
                   "so each bag has 3 apples and 4 oranges. 3 and 2 also work, but they are not the greatest. "
                   "72 is a common multiple."))
    assert 4 in cfs(12, 20) and 20 % 3 and 12 % 5 and 20 % 6
    its.append(mcq("Kavya has 12 red beads and 20 blue beads. She makes bracelets that are all the same and uses every bead. "
                   "Which of these could be the number of bracelets?",
                   "4 bracelets", ["3 bracelets", "5 bracelets", "6 bracelets"],
                   "The number of bracelets must be a common factor of 12 and 20 (1, 2 or 4). Of these choices, only <b>4 bracelets</b> works, "
                   "each with 3 red and 5 blue beads. 3 and 6 are factors of 12 only, and 5 is a factor of 20 only."))
    assert L(4, 6) == 12
    its.append(mcq(fig(model_svg([("Cups", 4, FILL_Y), ("Plates", 6, FILL_B)], "?", 12, 20, "bar model of packs of 4 and 6"))
                   + "Paper cups come in packs of 4 and paper plates in packs of 6. Wei Ming says he must buy 24 of each "
                   "to have the same number. Is he right?",
                   "No. 12 of each is enough", ["Yes. 4 × 6 = 24", "No. 10 of each is enough", "No. 2 of each is enough"],
                   first_cm_e(4, 6) + " The model shows 3 packs of cups and 2 packs of plates give <b>12 of each</b>. "
                   "24 also works, but it is not the least. 10 is 4 + 6, and 2 is a common factor."))
    assert L(6, 9) == 18
    its.append(mcq("A bubble tea shop gives a free sticker to every 6th customer and a free keychain to every 9th "
                   "customer. Which customer is the first to get both?",
                   "the 18th", ["the 54th", "the 15th", "the 3rd"],
                   first_cm_e(6, 9) + " So the <b>18th</b> customer is the first to get both. 54 is 6 × 9, "
                   "15 is 6 + 9, and 3 is a common factor."))
    assert len(its) == 20, len(its)
    return {"title": "Common multiples and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Factors</h2>"
        "<p>A <b>factor</b> of a number divides it exactly, with no remainder. 12 = 3 × 4, so 3 and 4 are factors of 12.</p>"
        "<p>To find <b>all</b> the factors, find the <b>factor pairs</b>. Start with 1 × the number. Try 2, 3, 4, … "
        "and stop when the pairs start to repeat.</p>"
        "<figure class='sn-fig'>" + array_svg(3, 4) +
        "<figcaption>12 counters in 3 rows of 4. So 3 × 4 is a factor pair of 12.</figcaption></figure>"
        + ex("Example", "Find all the factors of 18.",
             "Factor pairs: 1 × 18, 2 × 9, 3 × 6. 4 and 5 do not divide 18. The next pair, 6 × 3, repeats.",
             "1, 2, 3, 6, 9, 18")
        + "<p><b>Is it a factor?</b> Divide. If there is no remainder, it is a factor. 56 ÷ 8 = 7, so 8 is a factor of 56. "
        "56 ÷ 6 = 9 R 2, so 6 is not.</p>"
        "<h2>Common factors</h2>"
        "<p>A <b>common factor</b> is a factor of both numbers. List the factors of each number and circle the "
        "numbers in both lists. 1 is always a common factor.</p>"
        "<figure class='sn-fig'>" + factor_rows_svg(12, 18) +
        "<figcaption>The common factors of 12 and 18 are 1, 2, 3 and 6.</figcaption></figure>"
        "<h2>Multiples</h2>"
        "<p>The <b>multiples</b> of a number are the number × 1, × 2, × 3, … The multiples of 6 are 6, 12, 18, 24, … "
        "The first multiple is the number itself.</p>"
        "<p>Factors and multiples go together: 3 is a factor of 12, and 12 is a multiple of 3. "
        "A factor is never bigger than the number. A multiple is never smaller.</p>"
        "<h2>Common multiples</h2>"
        "<p>A <b>common multiple</b> is a multiple of both numbers. Count in the bigger number and stop at the first "
        "number that the smaller number also divides.</p>"
        "<figure class='sn-fig'>" + multiples_svg(4, 6, 36, show=True) +
        "<figcaption>Multiples of 4 and of 6. They meet at 12, 24 and 36. The first common multiple is 12, not 4 × 6 = 24.</figcaption></figure>"
        + ex("Example", "Buns come in packets of 6 and sausages in packets of 8. What is the least number of each to buy "
             "so there are the same number of buns and sausages?",
             "Count in 8s: 8, 16, 24. 24 is a multiple of 6 too. In the model, 4 packets of buns and 3 packets of "
             "sausages are the same length.",
             "24 buns and 24 sausages")
        + "<figure class='sn-fig'>" + model_svg([("Buns", 6, FILL_Y), ("Sausages", 8, FILL_B)], "24", 24, 12,
                                                 "bar model of packets of 6 and 8") +
        "<figcaption>4 units of 6 = 3 units of 8 = 24.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Forgetting 1 and the number itself: “the factors of 15 are 3 and 5”", "Start with 1 × 15: the factors are 1, 3, 5, 15"],
            ["Mixing up factors and multiples: “4 is a multiple of 12”", "4 is a factor of 12. 12 is a multiple of 4"],
            ["Listing only one common factor: “the common factor of 20 and 30 is 10”", "List them all: 1, 2, 5, 10"],
            ["Thinking every even number has 4 as a factor", "30 ÷ 4 = 7 R 2, so 4 is not a factor of 30"],
            ["Multiplying for the first common multiple: 4 × 6 = 24", "Count in 6s: 6, 12. 12 comes first"],
        ])
    )


FAQ = [
    {"q": "What is taught in P4 factors and multiples?",
     "a": "Primary 4 students find all the factors of a number, check whether a number is a factor, find common factors of two numbers, list multiples and find common multiples of two 1-digit numbers. They use these ideas in word problems about packets, groups and bus timings."},
    {"q": "How do I explain factors and multiples to my child?",
     "a": "Use an example like 3 × 4 = 12: 3 and 4 are factors of 12, and 12 is a multiple of 3 and of 4. Factors are the numbers you multiply; the multiple is the answer."},
    {"q": "What is the most common mistake with factors and multiples?",
     "a": "The most common mistake is forgetting 1 and the number itself when listing factors. Many children also mix up factors and multiples, or give only one common factor when the question asks for all of them."},
    {"q": "Is factors and multiples in the MOE Primary 4 syllabus?",
     "a": "Yes. Factors and multiples, common factors of two numbers and common multiples of two 1-digit numbers are part of Whole Numbers in the MOE 2021 Primary 4 Mathematics syllabus. These skills are used later in fractions, and in the PSLE."},
]


def gen():
    rnd = random.Random(64803)
    sets = [set_factors(), set_is_factor(), set_common_factors(), set_multiples(), set_common_multiples()]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len({plain(c) for c in it["c"]}) == 4, it
            k = plain(it["q"]) + "|" + "|".join(sorted(plain(c) for c in it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-4", "slug": "factors-and-multiples", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 4 Factors and Multiples",
        "seo_title": "P4 Factors and Multiples Worksheets: Free Primary 4 Maths with Answers (MOE Syllabus)",
        "short_title": "Factors and Multiples",
        "domain": "Number and Algebra",
        "standard_code": "Primary 4: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Factors and multiples; common factors of two numbers; common multiples of two 1-digit numbers",
        "meta_desc": "Free P4 maths practice: factors, factor pairs, common factors, multiples, common multiples and word problems. 100 questions with answers.",
        "key_big": "A factor divides a number exactly. A multiple is the number times 1, 2, 3, …",
        "key_sub": "12 = 3 × 4, so 3 and 4 are factors of 12, and 12 is a multiple of 3 and of 4.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160
    return mark_large(u, "(factors of|multiples of|number line|bar model|groups of)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
