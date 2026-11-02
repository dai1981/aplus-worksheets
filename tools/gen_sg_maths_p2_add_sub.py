# -*- coding: utf-8 -*-
"""
SG Primary 2 Maths: Addition and subtraction within 1000 (MOE 2021 Primary Mathematics Syllabus, Whole Numbers)
  python3 tools/gen_sg_maths_p2_add_sub.py
Mental calculation (a 3-digit number and ones, tens or hundreds), column addition with renaming,
column subtraction with renaming (including across 0), checking with the inverse, and
1-step Singapore word problems with bar models. Singapore English, numbers to 1000.
Every answer and every wrong answer is computed and checked in code.
HTML attributes use single quotes (no backslashes in the JSON).
Helpers are adapted from gen_cabc_math_g3_add_sub.py, gen_cabc_math_g2_add_sub.py and gen_sg_maths_p3_mult_div.py.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "sg", "maths", "primary-2")
UPDATED = "2026-11-03"
GREEN = "#006633"
FILL = "#cfe6d6"
GREYF = "#e3e3e3"
INK = "#2b2b2b"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
PLACE = ["ones", "tens", "hundreds", "thousands"]
ONE = ["one", "ten", "hundred", "thousand"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 usable distractors (no 0, negative or over-1000 values)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or lead in ("0", ""):
            continue
        if lead.isdigit() and int(lead) > 1000:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    w, h = int(round(w + 0.49)), int(round(h + 0.49))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def tw(s, size=15):
    return len(s) * size * 0.58


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


def cap(s):
    return s[0].upper() + s[1:]


def nlen(n):
    return len(str(n))


def digits(n, k=3):
    return [(n // 10 ** i) % 10 for i in range(k)]          # ones first


def clean(vals):
    return [v for v in vals if v is not None and 0 < v <= 1000]


def pl(k, i):
    """'1 ten', '3 tens'."""
    return "%d %s" % (k, ONE[i] if k == 1 else PLACE[i])


# ------------------------------------------------------------ pictures: open number line
def jw(j):
    j = abs(j)
    return 116 if j >= 100 else 80 if j >= 10 else 56


def nline_svg(start, jumps, ticks, jlabels=None):
    """Open number line. Jumps go right for +, left for −. ticks: one label per point."""
    if jlabels is None:
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
        s.append(text((x1 + x2) / 2, ly - ry - 7, jlabels[k], 15, col=RED if jlabels[k] == "?" else GREEN))
    for x, t in zip(xs, ticks):
        s.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, ly - 6, x, ly + 6, INK))
        if t is not None:
            s.append(text(x, ly + 24, t, 16, col=RED if t == "?" else INK))
    return svg_wrap(W, H, "".join(s), "open number line starting at %d with jumps of %s" % (
        start, ", ".join(jlabels).replace("−", "minus ").replace("?", "an unknown amount")))


# ------------------------------------------------------------ pictures: column layout
def column_svg(a, b, op, answer=False, marks=False, fs=28):
    """a over b in columns with the sign and a line, ones under ones.
    answer: also write the answer.  marks: red renaming marks above the top number
    (+: the renamed 1s;  −: old digits crossed out, new digits above)."""
    cw = fs * (0.82 if marks else 0.62)
    res = a + b if op == "+" else a - b
    rows = [str(a), str(b)] + ([str(res)] if answer else [])
    longest = max(len(r) for r in rows) * cw
    pad_l = cw * 1.5 + 8
    W = int(pad_l + longest + 12)
    right = W - 12
    top = 10 + (int(fs * 0.62) if marks else 0)
    s = []

    def put(t, y, color):
        for k, ch in enumerate(reversed(t)):
            s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle' "
                     "font-family='monospace'>%s</text>" % (right - cw * k - cw / 2, y, fs, color, ch))

    def px(i):
        return right - cw * i - cw / 2

    y1, y2 = top + fs, top + int(fs * 2.15)
    put(rows[0], y1, INK)
    put(rows[1], y2, INK)
    sign_x = right - longest - cw * 0.9
    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
             % (sign_x, y2, fs, GREEN, "+" if op == "+" else "−"))
    ly = y2 + 13
    s.append("<line x1='%.1f' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (sign_x - cw * 0.6, ly, right, ly, INK))
    H = ly + 10
    if answer:
        ay = ly + fs + 6
        put(rows[2], ay, GREEN)
        H = ay + 12
    if marks:
        sm = int(fs * 0.55)
        if op == "+":
            for i in add_carry_cols(a, b):
                s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>1</text>"
                         % (px(i + 1), top - 4, sm, RED))
        else:
            nd = regroup_digits(a, b)
            od = digits(a, nlen(a))
            for i in range(nlen(a)):
                if nd[i] != od[i]:
                    x = px(i)
                    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2.5'/>"
                             % (x - fs * 0.28, y1 + fs * 0.02, x + fs * 0.28, y1 - fs * 0.72, RED))
                    s.append("<text x='%.1f' y='%d' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%d</text>"
                             % (x, top - 4, sm if nd[i] < 10 else int(sm * 0.85), RED, nd[i]))
    label = "%d %s %d written in columns" % (a, "plus" if op == "+" else "minus", b)
    return svg_wrap(W, int(H), "".join(s), label)


# ------------------------------------------------------------ pictures: bar models (drawn to scale)
BH = 34


def bracket_above(a, b, y, lab):
    return ("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
            % (a, y - 4, y - 11, b, y - 4, RED if lab == "?" else INK) + text((a + b) / 2, y - 16, lab, 16, RED if lab == "?" else INK))


def bracket_below(a, b, y, lab):
    return ("<path d='M%.1f %d V%d H%.1f V%d' fill='none' stroke='%s' stroke-width='2'/>"
            % (a, y + 4, y + 11, b, y + 4, RED if lab == "?" else INK) + text((a + b) / 2, y + 30, lab, 16, RED if lab == "?" else INK))


def seg(x, y, w, lab, fill):
    assert lab == "" or tw(lab, 16) + 6 <= w, (lab, w)
    out = "<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (x, y, w, BH, fill, GREEN)
    if lab:
        out += text(x + w / 2, y + 23, lab, 16, RED if lab == "?" else INK)
    return out


def pw_svg(p1, p2, l1, l2, lw, BW=300):
    """Part-whole bar model: one bar in two parts, the whole in a bracket on top."""
    x0, y = 8, 36
    sc = BW / float(p1 + p2)
    s = [seg(x0, y, p1 * sc, l1, FILL), seg(x0 + p1 * sc, y, p2 * sc, l2, "#ffffff"),
         bracket_above(x0, x0 + BW, y, lw)]
    return svg_wrap(x0 + BW + 8, y + BH + 8, "".join(s),
                    "bar model: whole %s, parts %s and %s" % (lw, l1, l2))


def cmp_svg(n_top, v_top, n_bot, v_bot, l_top, l_bot, l_diff, BW=270):
    """Comparison bar model drawn to scale. The longer bar is split where the shorter one ends;
    the extra piece carries l_diff. The longer bar's total goes in a bracket (above if on top, below if at the bottom)."""
    nw = max(tw(n_top, 15), tw(n_bot, 15))
    x0 = 8 + nw + 10
    top_long = v_top > v_bot
    vl, vs = (v_top, v_bot) if top_long else (v_bot, v_top)
    sc = BW / float(vl)
    y0 = 36 if top_long else 8
    y1 = y0 + BH + 14
    s = [text(8, y0 + 23, n_top, 15, anchor="start"), text(8, y1 + 23, n_bot, 15, anchor="start")]
    ylong, yshort = (y0, y1) if top_long else (y1, y0)
    l_long, l_short = (l_top, l_bot) if top_long else (l_bot, l_top)
    s.append(seg(x0, yshort, vs * sc, l_short, FILL))
    s.append(seg(x0, ylong, vs * sc, "", FILL))
    s.append(seg(x0 + vs * sc, ylong, (vl - vs) * sc, l_diff, GREYF))
    if top_long:
        s.append(bracket_above(x0, x0 + BW, ylong, l_long))
        H = y1 + BH + 8
    else:
        s.append(bracket_below(x0, x0 + BW, ylong + BH, l_long))
        H = y1 + BH + 38
    xd = x0 + vs * sc
    s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>"
             % (xd, min(y0, y1) + BH, xd, max(y0, y1), GREEN))
    return svg_wrap(x0 + BW + 8, H, "".join(s), "comparison bar model: %s %s, %s %s, difference %s"
                    % (n_top, l_top, n_bot, l_bot, l_diff))


# ------------------------------------------------------------ column methods
def regroup_digits(a, b):
    """Top digits after all the renaming of column subtraction (ones first)."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return d


def add_carry_cols(a, b):
    """Columns (ones = 0) that make 10 or more and send 1 to the next column."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    c, cols = 0, []
    for i in range(k):
        c = 1 if da[i] + db[i] + c >= 10 else 0
        if c:
            cols.append(i)
    return cols


def sub_regroup_cols(a, b):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    cols = []
    for i in range(k):
        if d[i] < db[i]:
            cols.append(i)
            d[i] += 10
            d[i + 1] -= 1
    return cols


def zero_chain(a, b):
    """True if some renaming has to go across a 0."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    chain = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = True
            for m in range(j, i, -1):
                d[m] -= 1
                d[m - 1] += 10
    return chain


def add_steps(a, b):
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    kb = min(nlen(a), nlen(b))
    carry, ps = 0, []
    for i in range(k):
        t = da[i] + db[i] + carry
        if i >= kb:
            big = da[i] if nlen(a) > nlen(b) else db[i]
            expr = "%d + 1" % big if carry else None
        else:
            expr = "%d + %d" % (da[i], db[i]) + (" + 1" if carry else "")
        P = cap(PLACE[i])
        if t >= 10:
            assert i < k - 1
            ps.append("%s: %s = %d. Write %d. Rename 10 %s as 1 %s." % (P, expr, t, t % 10, PLACE[i], ONE[i + 1]))
            carry = 1
        else:
            ps.append("%s: write %d." % (P, t) if expr is None else "%s: %s = %d." % (P, expr, t))
            carry = 0
    return "Line up the ones and start on the right. " + " ".join(ps) + " Answer: <b>%d</b>." % (a + b)


def sub_steps(a, b, check=True):
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    kb = nlen(b)
    ps = []
    for i in range(k):
        P = cap(PLACE[i])
        if d[i] < db[i]:
            cur = d[i]
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                chain = ", then ".join("1 %s as 10 %s" % (ONE[m], PLACE[m - 1]) for m in range(j, i, -1))
                for m in range(j, i, -1):
                    d[m] -= 1
                    d[m - 1] += 10
                msg = ("%s: %d − %d cannot be done. There are 0 tens, so rename %s. The 0 tens become 9 tens. "
                       "%d − %d = %d." % (P, cur, db[i], chain, d[i], db[i], d[i] - db[i]))
            else:
                d[j] -= 1
                d[i] += 10
                msg = ("%s: %d − %d cannot be done. Rename 1 %s as 10 %s: %d − %d = %d."
                       % (P, cur, db[i], ONE[i + 1], PLACE[i], d[i], db[i], d[i] - db[i]))
            ps.append(msg)
        elif i >= kb:
            if d[i] or i < k - 1:
                ps.append("%s: write %d." % (P, d[i]))
        else:
            ps.append("%s: %d − %d = %d." % (P, d[i], db[i], d[i] - db[i]))
    r = a - b
    out = "Line up the ones and start on the right. " + " ".join(ps) + " Answer: <b>%d</b>." % r
    if check:
        out += " Check: %d + %d = %d." % (r, b, a)
    return out


# ------------------------------------------------------------ typical mistakes
def add_no_regroup(a, b):
    """Never adds the renamed 1s (writes the full sum only in the last column)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    return sum(((da[i] + db[i]) % 10 if i < k - 1 else da[i] + db[i]) * 10 ** i for i in range(k))


def add_forgot_one(a, b, which):
    cols = [c for c in add_carry_cols(a, b) if c < max(nlen(a), nlen(b)) - 1]
    if not cols:
        return None
    i = cols[0] if which == "first" else cols[-1]
    return a + b - 10 ** (i + 1)


def add_side_by_side(a, b):
    """Wrote a column total side by side (5 + 8 = 13 written as 13)."""
    k = max(nlen(a), nlen(b))
    da, db = digits(a, k), digits(b, k)
    if not add_carry_cols(a, b):
        return None
    v = int("".join(str(da[i] + db[i]) for i in reversed(range(k))))
    return v if v != a + b else None


def add_misalign(a, b):
    """Lined up the shorter number on the left (under the hundreds)."""
    if nlen(a) == nlen(b):
        return None
    big, small = max(a, b), min(a, b)
    return big + small * 10 ** (nlen(big) - nlen(small))


def add_extra_one(a, b):
    cols = set(add_carry_cols(a, b))
    k = max(nlen(a), nlen(b))
    return [a + b + 10 ** (i + 1) for i in range(k - 1) if i not in cols]


def sub_small_from_big(a, b):
    k = nlen(a)
    da, db = digits(a, k), digits(b, k)
    return sum(abs(da[i] - db[i]) * 10 ** i for i in range(k))


def sub_forgot_reduce(a, b):
    """Made 10 more but did not take 1 away from the next place."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    out = 0
    for i in range(k):
        if d[i] < db[i]:
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out


def sub_zero_as_ten(a, b):
    """Renaming across 0: changed the 0 tens to 10 tens instead of 9 tens."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    hit = False
    for i in range(k):
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            d[j] -= 1
            if j > i + 1:
                hit = True
                for m in range(i + 1, j):
                    d[m] = 10
            d[i] += 10
    if not hit:
        return None
    return sum((d[i] - db[i]) * 10 ** i for i in range(k))


def sub_zero_skip(a, b):
    """Did not rename across the 0: took 1 straight from the hundreds and left the 0 tens as 0."""
    k = nlen(a)
    d, db = digits(a, k), digits(b, k)
    skipped, hit, out = set(), False, 0
    for i in range(k):
        if i in skipped:
            out += abs(d[i] - db[i]) * 10 ** i
            continue
        if d[i] < db[i]:
            j = i + 1
            while d[j] == 0:
                j += 1
            if j > i + 1:
                hit = True
                skipped |= set(range(i + 1, j))
            d[j] -= 1
            d[i] += 10
        out += (d[i] - db[i]) * 10 ** i
    return out if hit else None


def sub_misalign(a, b):
    """Lined up a 2-digit number under the hundreds and tens: 734 − 46 done as 734 − 460."""
    if nlen(b) >= nlen(a) or a - b * 10 ** (nlen(a) - nlen(b)) <= 0:
        return None
    return a - b * 10 ** (nlen(a) - nlen(b))


def add_cands(a, b):
    every = [a + b - 10 ** (i + 1) for i in add_carry_cols(a, b) if i < max(nlen(a), nlen(b)) - 1]
    return clean([add_no_regroup(a, b), add_forgot_one(a, b, "first"), add_forgot_one(a, b, "last"),
                  add_misalign(a, b), add_side_by_side(a, b)] + every + add_extra_one(a, b) + [abs(a - b), a + b - 100, a + b + 10, a + b - 10])


def sub_cands(a, b):
    return clean([sub_zero_skip(a, b), sub_zero_as_ten(a, b), sub_small_from_big(a, b), sub_misalign(a, b),
                  sub_forgot_reduce(a, b), a + b, a - b + 10, a - b - 10, a - b + 100])


# ============================================================ set 1: mental calculation
def place_of(b):
    i = 0
    while b % 10 == 0:
        b //= 10
        i += 1
    assert b < 10
    return i, b


def mental_cands(a, op, b):
    i, k = place_of(b)
    r = a + b if op == "+" else a - b
    out = []
    if op == "+":
        out.append(add_no_regroup(a, b) if add_carry_cols(a, b) else None)   # forgot to rename
    else:
        if sub_regroup_cols(a, b):
            out += [sub_small_from_big(a, b), sub_forgot_reduce(a, b)]
    for j in range(3):                                                        # used the wrong place
        if j != i:
            out.append(a + k * 10 ** j if op == "+" else a - k * 10 ** j)
    out.append(a - b if op == "+" else a + b)                                 # wrong operation
    out += [r + 10 ** i, r - 10 ** i]                                         # one jump too many or too few
    return clean(out)


def mental_e(a, op, b):
    i, k = place_of(b)
    d = digits(a)
    r = a + b if op == "+" else a - b
    P = cap(PLACE[i])
    if op == "+":
        t = d[i] + k
        if t < 10:
            return ("%d is %s. Only the %s change: %d + %d = %d. %d + %d = <b>%d</b>."
                    % (b, pl(k, i), PLACE[i], d[i], k, t, a, b, r))
        return ("%d is %s. %s: %d + %d = %d. Rename 10 %s as 1 %s. %s left. "
                "%d + %d = <b>%d</b>." % (b, pl(k, i), P, d[i], k, t, PLACE[i], ONE[i + 1],
                                          cap(pl(t - 10, i)) + (" is" if t == 11 else " are"), a, b, r))
    if d[i] >= k:
        return ("%d is %s. Only the %s change: %d − %d = %d. %d − %d = <b>%d</b>."
                % (b, pl(k, i), PLACE[i], d[i], k, d[i] - k, a, b, r))
    assert d[i + 1] > 0
    return ("%d is %s. %s: %d − %d cannot be done. Rename 1 %s as 10 %s: %d − %d = %d. "
            "%d − %d = <b>%d</b>." % (b, pl(k, i), P, d[i], k, ONE[i + 1], PLACE[i], d[i] + 10, k, d[i] + 10 - k, a, b, r))


def q_mental(a, op, b, pre=""):
    r = a + b if op == "+" else a - b
    assert 0 < r <= 1000
    return mcq(pre + "What is %d %s %d?" % (a, op, b), r, mental_cands(a, op, b), mental_e(a, op, b))


def set_mental():
    its = []
    its.append(q_mental(345, "+", 30, fig(nline_svg(345, [30], ["345", "?"])) + "Count on 3 tens. "))
    its.append(q_mental(562, "−", 200, fig(nline_svg(562, [-200], ["562", "?"])) + "Count back 2 hundreds. "))
    for a, op, b in [(214, "+", 5), (678, "−", 40), (431, "+", 300), (896, "−", 3), (253, "+", 600), (759, "−", 500)]:
        its.append(q_mental(a, op, b))
    it = q_mental(347, "+", 6, fig(nline_svg(347, [3, 3], ["347", "350", "?"])) + "Make the next ten. ")
    it["e"] = "347 + 3 = 350. 6 is 3 + 3, so add 3 more: 350 + 3 = <b>353</b>. (343 forgets to rename 10 ones as 1 ten.)"
    its.append(it)
    for a, op, b in [(386, "+", 40), (523, "−", 7), (415, "−", 30), (268, "+", 50), (732, "−", 8)]:
        its.append(q_mental(a, op, b))
    assert 875 + 100 == 975 and 603 - 10 == 593
    its.append(mcq("What is 100 more than 875?", 975, [885, 876, 775],
                   "100 more means 1 more hundred. 8 hundreds become 9 hundreds. The tens and ones stay the same: <b>975</b>."))
    its.append(mcq("What is 10 less than 603?", 593, [503, 613, 693],
                   "603 has 0 tens. Rename 1 hundred as 10 tens. Take away 1 ten: 9 tens are left, and 5 hundreds. "
                   "603 − 10 = <b>593</b>. (693 forgets that 6 hundreds become 5 hundreds.)"))
    assert 456 + 30 == 486 and 924 - 400 == 524
    its.append(mcq("Find the missing number: 456 + <b>?</b> = 486", 30, [3, 300, 942],
                   "The hundreds and ones stay the same. The tens go from 5 to 8. That is 3 tens: <b>30</b>. "
                   "Check: 456 + 30 = 486."))
    its.append(mcq("Find the missing number: 924 − <b>?</b> = 524", 400, [4, 40, 500],
                   "The tens and ones stay the same. The hundreds go from 9 to 5. That is 4 hundreds: <b>400</b>. "
                   "Check: 924 − 400 = 524."))
    its.append(q_mental(218, "+", 300, fig(nline_svg(218, [100, 100, 100], ["218", "318", "418", "?"])) +
                        "Count on by hundreds. "))
    assert 590 + 50 == 640 and 590 + 5 == 595 and 600 + 50 == 650 and 590 + 500 == 1090
    its.append(mcq("Which one is equal to 640?", "590 + 50", ["590 + 5", "600 + 50", "590 + 500"],
                   "590 + 50: 9 tens + 5 tens = 14 tens. Rename 10 tens as 1 hundred. 5 hundreds become 6 hundreds, "
                   "with 4 tens left. <b>590 + 50</b> = 640. The others are 595, 650 and 1090."))
    assert len(its) == 20, len(its)
    return {"title": "Mental calculation: add and subtract ones, tens and hundreds", "items": its}


# ============================================================ set 2: column addition with renaming
LESSON = {(367, 258), (452, 178), (500, 168), (346, 52)}


def item_add(a, b, col):
    q = (fig(column_svg(a, b, "+")) + "Add. Rename when a column makes 10 or more.") if col else \
        "Find the value of %d + %d." % (a, b)
    return mcq(q, a + b, add_cands(a, b), add_steps(a, b))


def item_sub(a, b, col):
    q = (fig(column_svg(a, b, "-")) + "Subtract. Rename when the top digit is smaller.") if col else \
        "Find the value of %d − %d." % (a, b)
    return mcq(q, a - b, [v for v in sub_cands(a, b) if v != b], sub_steps(a, b))


def pick_add(rnd, seen, la, lb, cols):
    while True:
        a = rnd.randint(112, 880)
        b = rnd.randint(112, 880) if lb == 3 else rnd.randint(23, 98)
        if a + b > 999 or (a, b) in seen or (b, a) in seen or (a, b) in LESSON or a % 10 == 0 or b % 10 == 0:
            continue
        if add_carry_cols(a, b) != cols or abs(a - b) < 50 or ("sum", a + b) in seen:
            continue
        seen.add((a, b))
        seen.add(("sum", a + b))
        return a, b


def set_add(rnd, seen):
    its = []
    plan = ([(3, 3, [])] + [(3, 3, [0])] * 2 + [(3, 2, [0])] * 2 + [(3, 3, [1])] * 3 + [(3, 2, [1])] +
            [(3, 3, [0, 1])] * 5 + [(3, 2, [0, 1])] * 3)
    for i, (la, lb, cols) in enumerate(plan):
        a, b = pick_add(rnd, seen, la, lb, cols)
        its.append(item_add(a, b, i % 3 != 2))
    assert add_no_regroup(367, 258) == 515 and 367 + 258 == 625
    its.insert(6, mcq("Ali says 367 + 258 = 515. What mistake did he make?", "He did not rename",
                      ["He did not line up the ones", "He took away 258", "He added the tens twice"],
                      "7 + 8 = 15 and 6 + 5 = 12. Ali wrote only 5 and 2 and forgot the renamed 1s. "
                      "<b>He did not rename.</b> 367 + 258 = 625."))
    assert add_misalign(346, 52) == 866 and 346 + 52 == 398
    its.insert(12, mcq("Mei Ling says 346 + 52 = 866. What mistake did she make?", "She did not line up the ones",
                       ["She did not rename", "She added 2 too many", "She took away 52"],
                       "Mei Ling put 52 under the 3 and the 4, so she added 520. "
                       "<b>She did not line up the ones.</b> Put 2 under 6: 346 + 52 = 398."))
    assert add_carry_cols(478, 256) == [0, 1] and 478 + 256 == 734
    its.append(mcq("How many times do you rename in 478 + 256?", "2 times", ["1 time", "Never", "3 times"],
                   "Ones: 8 + 6 = 14, rename 10 ones as 1 ten. Tens: 7 + 5 + 1 = 13, rename 10 tens as 1 hundred. "
                   "Hundreds: 4 + 2 + 1 = 7. You rename <b>2 times</b>. 478 + 256 = 734."))
    assert len(its) == 20, len(its)
    return {"title": "Add 3-digit numbers with renaming", "items": its}


# ============================================================ set 3: column subtraction with renaming
def pick_sub(rnd, seen, lb, cols):
    while True:
        a = rnd.randint(150, 989)
        b = rnd.randint(112, a - 25) if lb == 3 else rnd.randint(12, 96)
        if b >= a or (a, b) in seen or (a, b) in LESSON or zero_chain(a, b) or a % 10 == 0 or b % 10 == 0:
            continue
        if lb == 3 and b < 112:
            continue
        if sub_regroup_cols(a, b) != cols or (a - b) < 100 and lb == 3 and rnd.random() < 0.7:
            continue
        seen.add((a, b))
        return a, b


def set_sub(rnd, seen):
    its = []
    plan = [(3, [0])] * 3 + [(2, [0])] + [(3, [1])] * 3 + [(2, [1])] + [(3, [0, 1])] * 4 + [(2, [0, 1])]
    for i, (lb, cols) in enumerate(plan):
        a, b = pick_sub(rnd, seen, lb, cols)
        its.append(item_sub(a, b, i % 3 != 2))
    assert sub_small_from_big(452, 178) == 326 and 452 - 178 == 274
    its.insert(4, mcq("Hui Min says 452 − 178 = 326. What mistake did she make?",
                      "She took the smaller digit from the larger",
                      ["She did not line up the ones", "She added the numbers", "She forgot the hundreds"],
                      "In the ones, Hui Min did 8 − 2, but it is 2 − 8. "
                      "<b>She took the smaller digit from the larger.</b> Rename instead: 452 − 178 = 274."))
    tops = {500}                                       # 500 − 168 is the lesson example
    pats = ["x0x", "x0x", "x00", "x0x", "x00"]
    for n, p in enumerate(pats):
        while True:
            a = int("".join(str(rnd.randint(2, 9)) if ch == "x" else ch for ch in p))
            lb = 2 if n == 3 else 3
            b = rnd.randint(112, a - 60) if lb == 3 else rnd.randint(12, 96)
            if a in tops or (a, b) in seen or b % 10 == 0 or not zero_chain(a, b):
                continue
            tops.add(a)
            seen.add((a, b))
            its.append(item_sub(a, b, n % 3 != 2))
            break
    assert regroup_digits(500, 168) == [10, 9, 4]
    its.append(mcq("To find 500 − 168, you rename 500. What is 500 after renaming?",
                   "4 hundreds 9 tens 10 ones",
                   ["4 hundreds 10 tens 10 ones", "5 hundreds 9 tens 10 ones", "4 hundreds 0 tens 10 ones"],
                   "There are 0 tens, so rename 1 hundred as 10 tens. Then rename 1 ten as 10 ones. "
                   "500 = <b>4 hundreds 9 tens 10 ones</b>. Check: 400 + 90 + 10 = 500."))
    assert 400 + 90 + 10 == 500
    assert len(its) == 20, len(its)
    return {"title": "Subtract 3-digit numbers with renaming (including across 0)", "items": its}


# ============================================================ set 4: check with the inverse
def set_inverse():
    its = []

    def add_q(q, right, wrong, e):
        its.append(mcq(q, right, wrong, e))

    assert 512 - 287 == 225 and 225 + 287 == 512
    add_q("Siti found 512 − 287 = 225. Which addition checks her answer?", "225 + 287",
          ["512 + 225", "512 + 287", "287 − 225"],
          "Add the answer and the number you took away. You should get the first number: <b>225 + 287</b> = 512.")
    assert 346 + 278 == 624 and 624 - 278 == 346
    add_q("Ahmad found 346 + 278 = 624. Which subtraction checks his answer?", "624 − 278",
          ["624 + 278", "346 − 278", "624 + 346"],
          "Take one part away from the total. You should get the other part: <b>624 − 278</b> = 346.")
    assert 600 - 245 == 355
    its.append(mcq(fig(pw_svg(245, 355, "245", "?", "600")) + "Find the missing number. 245 + <b>?</b> = 600",
                   355, sub_cands(600, 245),
                   "The whole is 600. One part is 245. To find the other part, subtract: " + sub_steps(600, 245, False)
                   + " Check: 245 + 355 = 600."))
    for a, b in [(168, 425), (384, 900), (409, 806)]:      # a + ? = b
        x = b - a
        q = ("Find the missing number. <b>?</b> + %d = %d" % (a, b)) if a == 168 else \
            ("Find the missing number. %d + <b>?</b> = %d" % (a, b))
        its.append(mcq(q, x, sub_cands(b, a),
                       "Use the inverse. The missing part is %d − %d. " % (b, a) + sub_steps(b, a, False) +
                       " Check: %d + %d = %d." % (a, x, b)))
    for a, r in [(700, 352), (815, 529)]:                  # a − ? = r
        x = a - r
        its.append(mcq("Find the missing number. %d − <b>?</b> = %d" % (a, r), x, sub_cands(a, r) + [a + r],
                       "You take away the missing number from %d and get %d. So the missing number is %d − %d. "
                       % (a, r, a, r) + sub_steps(a, r, False) + " Check: %d − %d = %d." % (a, x, r)))
    for b, r in [(186, 437), (259, 476)]:                  # ? − b = r
        x = b + r
        its.append(mcq("Find the missing number. <b>?</b> − %d = %d" % (b, r), x, [r - b] + add_cands(r, b),
                       "Use the inverse: add back what was taken away. %d + %d = <b>%d</b>. Check: %d − %d = %d."
                       % (r, b, x, x, b, r)))
    assert sub_small_from_big(603, 258) == 455 and 455 + 258 == 713 and 603 - 258 == 345
    add_q("Nurul says 603 − 258 = 455. She checks: 455 + 258 = 713. Is she correct?", "No, 713 is not 603",
          ["Yes, she is correct", "Yes, 713 is close to 603", "No, 455 + 258 is 603"],
          "The check must give back 603. It gives 713, so <b>she is not correct</b>. 603 − 258 = 345. "
          "Check: 345 + 258 = 603.")
    assert 724 - 386 == 338 and 338 + 386 == 724 and add_no_regroup(338, 386) == 614
    add_q("Ali found 724 − 386 = 338. He checks by adding 338 + 386. What number should he get?", 724,
          [386, 338, 614],
          "If the answer is correct, the check gives back the first number. 338 + 386 = <b>724</b>, so 338 is correct.")
    its.append(mcq("Kumar says 452 − 187 = 375. Check with addition. What is the correct answer to 452 − 187?",
                   265, sub_cands(452, 187),
                   "Check: 375 + 187 = 562, not 452, so 375 is wrong. " + sub_steps(452, 187)))
    assert sub_small_from_big(452, 187) == 335 and sub_forgot_reduce(452, 187) == 375
    assert 357 + 286 == 643 and add_no_regroup(357, 286) == 533 and 533 - 286 == 247
    add_q("Xin Yi says 357 + 286 = 533. She checks: 533 − 286 = 247. Is she correct?", "No, 247 is not 357",
          ["Yes, she is correct", "No, 533 − 286 is 357", "Yes, 247 is close to 357"],
          "The check must give back 357. It gives 247, so <b>she is not correct</b>. She did not rename. "
          "357 + 286 = 643.")
    assert 900 - 437 == 463
    add_q("Jun Jie found 900 − 437 = 463. Which addition checks his answer?", "463 + 437",
          ["900 + 437", "463 + 900", "463 − 437"],
          "Add the answer and the number you took away: <b>463 + 437</b> = 900. It gives back 900, so 463 is correct.")
    assert 725 - 348 == 377 and 377 - 348 == 29
    its.append(mcq(fig(pw_svg(348, 377, "348", "377", "725")) + "Which subtraction matches the bar model?",
                   "725 − 348", ["377 − 348", "725 + 348", "348 + 377"],
                   "Take one part away from the whole and you get the other part. <b>725 − 348</b> = 377. "
                   "(348 + 377 is an addition.)"))
    assert 638 + 195 == 833 and add_forgot_one(638, 195, "last") == 733
    its.append(mcq("Priya says 638 + 195 = 733. She checks: 733 − 195 = 538. What is the correct answer to 638 + 195?",
                   833, add_cands(638, 195),
                   "538 is not 638, so 733 is wrong. " + add_steps(638, 195)))
    assert 409 + 386 == 795
    add_q("Ryan found 409 + 386 = 795. Which subtraction checks his answer?", "795 − 386",
          ["795 + 386", "409 − 386", "795 + 409"],
          "Take one part away from the total. You should get the other part: <b>795 − 386</b> = 409.")
    assert 800 - 365 == 435 and sub_zero_as_ten(800, 365) == 445 and 445 + 365 == 810 and add_no_regroup(445, 365) == 700
    add_q("Hafiz says 800 − 365 = 445. He checks by adding 445 + 365. What does he get?", 810, [800, 700, 710],
          "445 + 365 = <b>810</b>. 810 is not 800, so 445 is wrong. 800 − 365 = 435.")
    assert 463 - 285 == 178
    its.append(mcq("Use addition to check each answer. Which answer to 463 − 285 is correct?", 178,
                   sub_cands(463, 285), sub_steps(463, 285)))
    assert len(its) == 20, len(its)
    return {"title": "Check with the inverse", "items": its}


# ============================================================ set 5: word problems with bar models
def unit(v, u):
    return "$%d" % v if u == "$" else "%d %s" % (v, u)


def eu(v, u):
    return "$%d" % v if u == "$" else str(v)


def story(q, ans, cands, u, e):
    return mcq(q, unit(ans, u), [unit(v, u) for v in clean(cands) if v != ans], e)


def set_words():
    its = []

    def add_story(q, a, b, u, lead, svg=None, extra=()):
        s = a + b
        e = lead + " %s + %s = <b>%s</b>. Check: %s − %s = %s." % (eu(a, u), eu(b, u), eu(s, u), eu(s, u), eu(b, u), eu(a, u))
        its.append(story((fig(svg) if svg else "") + q, s, list(extra) + add_cands(a, b), u, e))

    def sub_story(q, a, b, u, lead, svg=None, extra=()):
        r = a - b
        e = lead + " %s − %s = <b>%s</b>. Check: %s + %s = %s." % (eu(a, u), eu(b, u), eu(r, u), eu(r, u), eu(b, u), eu(a, u))
        its.append(story((fig(svg) if svg else "") + q, r, list(extra) + sub_cands(a, b), u, e))

    W = "The parts make the whole. To find the whole, add."
    P = "You know the whole and one part. To find the other part, subtract."
    D = "The bars show the difference. To find the difference, subtract."
    add_story("At Sports Day, 286 pupils ran in the morning and 347 pupils ran in the afternoon. "
              "How many pupils ran altogether?", 286, 347, "pupils", W, pw_svg(286, 347, "286", "347", "?"))
    sub_story("A school library has 625 books. 248 of them are storybooks. The rest are science books. "
              "How many science books are there?", 625, 248, "books", P, pw_svg(248, 377, "248", "?", "625"))
    sub_story("Mei Ling folded 412 paper stars. Ali folded 275 paper stars. "
              "How many more paper stars did Mei Ling fold than Ali?", 412, 275, "stars", D,
              cmp_svg("Mei Ling", 412, "Ali", 275, "412", "275", "?"))
    add_story("Jun Jie has 358 stickers. Farah has 167 more stickers than Jun Jie. How many stickers does Farah have?",
              358, 167, "stickers", "Farah has more. Her bar is Jun Jie’s bar and 167 more, so add.",
              cmp_svg("Jun Jie", 358, "Farah", 525, "358", "?", "167"), extra=[358 - 167])
    sub_story("A hawker stall sold 504 plates of chicken rice on Saturday. On Sunday, it sold 136 fewer plates. "
              "How many plates did it sell on Sunday?", 504, 136, "plates",
              "Sunday’s bar is shorter by 136, so subtract.",
              cmp_svg("Saturday", 504, "Sunday", 368, "504", "?", "136"), extra=[504 + 136])
    sub_story("There were some people on an MRT train. At the next station, 158 more people got on. "
              "Then there were 431 people on the train. How many people were on the train at first?", 431, 158, "people",
              "The whole is 431. The part that got on is 158. Find the other part, so subtract.",
              pw_svg(273, 158, "?", "158", "431"))
    sub_story("A fruit stall had 300 mandarin oranges for Chinese New Year. Mr Tan sold 164 of them. "
              "How many mandarin oranges were left?", 300, 164, "oranges", "Some were sold, so subtract.")
    sub_story("The school canteen made 465 curry puffs for recess. 289 curry puffs were sold. "
              "How many curry puffs were not sold?", 465, 289, "curry puffs", P)
    sub_story("Raju has 245 marbles. He has 128 more marbles than Hafiz. How many marbles does Hafiz have?",
              245, 128, "marbles", "Raju has more, so Hafiz has fewer. Take the difference away from Raju’s marbles.",
              cmp_svg("Raju", 245, "Hafiz", 117, "245", "?", "128"), extra=[245 + 128])
    add_story("Siti read 186 pages. She read 59 fewer pages than Nurul. How many pages did Nurul read?",
              186, 59, "pages", "Siti read fewer, so Nurul read more. Add the difference to Siti’s pages.",
              cmp_svg("Siti", 186, "Nurul", 245, "186", "?", "59"), extra=[186 - 59])
    sub_story("Mrs Ng had $500. She spent $265 on books for the class library. How much money did she have left?",
              500, 265, "$", "She spent some money, so subtract.")
    add_story("The P2 pupils made 234 paper flags for National Day. The P3 pupils made 189 paper flags. "
              "How many paper flags did they make altogether?", 234, 189, "flags", "Altogether means add.")
    sub_story("A shop had 407 red packets. It sold 129 of them. How many red packets were left?",
              407, 129, "packets", "Some were sold, so subtract.")
    sub_story("Hui Min had 600 beads. She used some beads to make bracelets. Now she has 342 beads. "
              "How many beads did she use?", 600, 342, "beads", P, pw_svg(258, 342, "?", "342", "600"))
    sub_story("There are 523 trees on one side of a park connector and 385 trees on the other side. "
              "How many fewer trees are on the other side?", 523, 385, "trees", "How many fewer means find the difference, so subtract.")
    add_story("The library lent out 296 books in May. In June, it lent out 148 more books than in May. "
              "How many books did it lend out in June?", 296, 148, "books", "More than in May, so add.")
    sub_story("Mr Rahman needs 750 lights for a Deepavali display at the community centre. He has put up 487 lights. "
              "How many more lights must he put up?", 750, 487, "lights", P, pw_svg(487, 263, "487", "?", "750"))
    assert 342 - 186 == 156
    its.append(mcq(fig(cmp_svg("Xin Yi", 342, "Ethan", 186, "342", "186", "?")) +
                   "Xin Yi has 342 cards. Ethan has 186 cards. Which number sentence finds how many more cards Xin Yi has?",
                   "342 − 186 = ?", ["342 + 186 = ?", "186 − 342 = ?", "? − 186 = 342"],
                   "How many more means find the difference. Take the smaller number from the bigger number. "
                   "The number sentence is <b>342 − 186 = ?</b> and the answer is 156."))
    add_story("Chloe walked 465 m from her HDB block to the MRT station. Then she walked 278 m to the library. "
              "How far did she walk altogether?", 465, 278, "m", "Altogether means add.")
    its.append(story(fig(pw_svg(238, 167, "238", "167", "?")) +
                     "A durian seller sold 238 durians. He had 167 durians left. How many durians did he have at first?",
                     405, [238 - 167] + add_cands(238, 167), "durians",
                     "The durians sold and the durians left make the whole. Add: 238 + 167 = <b>405</b>. "
                     "Check: 405 − 238 = 167."))
    assert len(its) == 20, len(its)
    return {"title": "Word problems with bar models", "items": its}


# ============================================================ lesson
def body_html():
    assert 345 + 30 == 375 and 562 - 200 == 362 and 386 + 40 == 426 and 367 + 258 == 625
    assert 452 - 178 == 274 and 500 - 168 == 332 and 332 + 168 == 500 and 412 - 275 == 137
    assert add_no_regroup(367, 258) == 515 and sub_small_from_big(452, 178) == 326 and add_misalign(346, 52) == 866
    assert sub_zero_as_ten(500, 168) == 342
    return (
        "<h2>The idea: ones with ones, tens with tens</h2>"
        "<p>A 3-digit number has <b>hundreds</b>, <b>tens</b> and <b>ones</b>. "
        "Add or subtract the same places. When a place has 10 or more, rename 10 of them as 1 of the next place.</p>"
        "<h2>Mental calculation</h2>"
        "<p>To add or take away tens, only the tens digit changes. To add or take away hundreds, only the hundreds digit changes.</p>"
        + table(["Number sentence", "What changes", "Answer"], [
            ["345 + 30", "tens: 4 + 3 = 7", "375"],
            ["562 − 200", "hundreds: 5 − 2 = 3", "362"],
            ["386 + 40", "tens: 8 + 4 = 12, rename 10 tens as 1 hundred", "426"],
        ]) +
        "<figure class='sn-fig'>" + nline_svg(345, [10, 10, 10], ["345", "355", "365", "375"]) +
        "<figcaption>345 + 30: count on 3 tens. 355, 365, 375.</figcaption></figure>"
        "<h2>Add with renaming</h2>"
        "<p>Write <b>ones under ones</b>. Start with the ones on the right. If a column makes 10 or more, "
        "write the ones digit and rename 10 as 1 of the next place. Write the small 1 at the top of the next column.</p>"
        "<figure class='sn-fig'>" + column_svg(367, 258, "+", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 7 + 8 = 15. Write 5, rename 10 ones as 1 ten. Tens: 6 + 5 + 1 = 12. "
        "Write 2, rename 10 tens as 1 hundred. Hundreds: 3 + 2 + 1 = 6. Answer: 625.</figcaption></figure>"
        "<h2>Subtract with renaming</h2>"
        "<p>Always take the <b>bottom</b> digit from the <b>top</b> digit. If the top digit is smaller, "
        "rename 1 of the next place as 10.</p>"
        "<figure class='sn-fig'>" + column_svg(452, 178, "-", answer=True, marks=True, fs=34) +
        "<figcaption>Ones: 2 − 8 cannot be done. Rename 1 ten as 10 ones: 12 − 8 = 4. Tens: 4 − 7 cannot be done. "
        "Rename 1 hundred as 10 tens: 14 − 7 = 7. Hundreds: 3 − 1 = 2. Answer: 274.</figcaption></figure>"
        "<p><b>Across 0:</b> if there are 0 tens, rename 1 hundred as 10 tens first. "
        "Then rename 1 ten as 10 ones. The 0 tens become 9 tens.</p>"
        "<figure class='sn-fig'>" + column_svg(500, 168, "-", answer=True, marks=True, fs=34) +
        "<figcaption>500 becomes 4 hundreds 9 tens 10 ones. 10 − 8 = 2, 9 − 6 = 3, 4 − 1 = 3. "
        "Answer: 332.</figcaption></figure>"
        + ex("Check with the inverse", "Is 500 − 168 = 332 correct?",
             "Add back what you took away: 332 + 168 = 500. You get the first number, so it is correct.", "Yes") +
        "<h2>Word problems: draw a bar model</h2>"
        "<p>A <b>part-whole</b> model shows two parts and a whole. Find the whole: add. Find a part: subtract. "
        "A <b>comparison</b> model shows two bars. Find how many more or fewer: subtract.</p>"
        "<figure class='sn-fig'>" + cmp_svg("Mei Ling", 412, "Ali", 275, "412", "275", "?") +
        "<figcaption>Mei Ling folded 412 stars. Ali folded 275 stars. How many more did Mei Ling fold? "
        "412 − 275 = 137.</figcaption></figure>"
        "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["No renaming: 367 + 258 = 515", "Write the renamed 1 in the next column and add it: 625"],
            ["Smaller digit from the larger: 452 − 178 = 326", "Take the bottom digit from the top digit. Rename when the top is smaller: 274"],
            ["Making 0 tens into 10 tens: 500 − 168 = 342", "1 ten moves to the ones, so 10 tens become 9 tens: 332"],
            ["Columns not lined up: 346 + 52 = 866", "Put ones under ones: 346 + 52 = 398"],
        ])
    )


FAQ = [
    {"q": "What do P2 pupils learn about addition and subtraction?",
     "a": "In Primary 2, pupils add and subtract numbers up to 1000. They use mental calculation, the column method with renaming, and bar models for word problems."},
    {"q": "What does renaming mean in Singapore maths?",
     "a": "Renaming means changing 10 of one place into 1 of the next place, such as 10 ones into 1 ten. Some older books call it carrying or borrowing."},
    {"q": "How do I help my child subtract across 0, like 500 − 168?",
     "a": "Rename 1 hundred as 10 tens, then 1 ten as 10 ones. 500 becomes 4 hundreds 9 tens 10 ones, so 500 − 168 = 332."},
    {"q": "Is this in the MOE syllabus?",
     "a": "Yes. The MOE 2021 Primary Mathematics Syllabus has Primary 2 pupils add and subtract up to 3 digits and do mental calculation with ones, tens and hundreds. These skills are used in every level up to the PSLE in Primary 6."},
]


def verify(sets):
    """Recompute every plain calculation answer from the question."""
    for s in sets:
        for it in s["items"]:
            right = it["c"][it["a"]]
            m = re.search(r"aria-label='(\d+) (plus|minus) (\d+) written in columns'", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "plus" else a - b), it["q"]
            m = re.search(r"(?:What is|Find the value of) (\d+) ([+−]) (\d+)[?.]$", it["q"])
            if m:
                a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                assert int(right) == (a + b if op == "+" else a - b), it["q"]
            m = re.search(r"Find the missing number\. (.*)$", it["q"])
            if m:
                eq = re.sub(r"<[^>]+>", "", m.group(1)).replace("?", right).replace("−", "-")
                l, r = eq.split("=")
                assert eval(l) == eval(r), eq
            m = re.search(r"aria-label='bar model: whole (\S+), parts (\S+) and (\S+)'", it["q"])
            if m and "matches" not in it["q"]:
                vals = [m.group(1), m.group(2), m.group(3)]
                k = vals.index("?")
                n = [int(x) for x in vals if x != "?"]
                want = n[0] + n[1] if k == 0 else n[0] - n[1]
                assert int(right.lstrip("$").split()[0]) == want, it["q"]
            m = re.search(r"aria-label='comparison bar model: \D+ (\S+), \D+ (\S+), difference (\S+)'", it["q"])
            if m and "number sentence" not in it["q"]:
                t, b_, d = m.groups()
                rv = int(right.split()[0])
                if d == "?":
                    assert rv == abs(int(t) - int(b_)), it["q"]
                else:
                    known = int(t) if b_ == "?" else int(b_)
                    assert rv in (known + int(d), known - int(d)), it["q"]


def gen():
    rnd = random.Random(62803)
    seen_a, seen_s = set(), set()
    sets = [set_mental(), set_add(rnd, seen_a), set_sub(rnd, seen_s), set_inverse(), set_words()]
    balance(sets, rnd)
    verify(sets)
    qs = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + str(sorted(it["c"]))
            assert k not in qs, it["q"]
            qs.add(k)
    u = {
        "country": "sg", "subject": "maths", "grade": "primary-2", "slug": "addition-and-subtraction", "sort": 3,
        "updated": UPDATED, "pdf_url": "",
        "title": "Primary 2 Addition and Subtraction within 1000",
        "seo_title": "P2 Addition and Subtraction Worksheets: Free Primary 2 Maths with Answers (MOE Syllabus)",
        "short_title": "Addition and subtraction",
        "domain": "Number and Algebra",
        "standard_code": "Primary 2: Whole Numbers",
        "standard_url": "https://www.moe.gov.sg/primary/curriculum/syllabus",
        "standard_text": "Addition and subtraction algorithms (up to 3 digits); mental calculation of a 3-digit number and ones/tens/hundreds",
        "meta_desc": "Free P2 maths practice: mental sums, 3-digit addition and subtraction with renaming, "
                     "checking answers and bar model word problems. 100 questions with answers.",
        "key_big": "Line up the ones, then rename when a place has 10 or more.",
        "key_sub": "367 + 258: 7 + 8 = 15, write 5 and rename 1 ten; 6 + 5 + 1 = 12, write 2 and rename 1 hundred; 3 + 2 + 1 = 6. Answer: 625.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    assert len(u["meta_desc"]) <= 160, len(u["meta_desc"])
    return mark_large(u, "open number line|bar model|comparison bar model")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fo:
        json.dump(u, fo, ensure_ascii=False, indent=1)
    print("wrote", path)
