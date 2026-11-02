# -*- coding: utf-8 -*-
"""
AU Year 4 Maths: Multiplication and division strategies (Australian Curriculum v9.0, AC9M4N06)
Partitioning 2- and 3-digit × 1-digit numbers (area model), short multiplication,
dividing by partitioning and known facts (no remainders), word problems with equal groups, sharing and arrays.
  python3 tools/gen_au_maths_y4_mult_div_strategies.py
HTML attributes use single quotes (no backslashes in the JSON). Every answer is worked out in code.
Australian style: Australian English, $ and c, 4-digit numbers without separators.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "au", "maths", "year-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#eef6f0"
RED = "#c0392b"
GREY = "#9a9a9a"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"
NB = " "
PLACE = ["ones", "tens", "hundreds", "thousands"]


# ------------------------------------------------------------ helpers
def f(n):
    """4536 -> 4536, 12350 -> 12 350 (no-break space)."""
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def mcq(q, correct, cands, e, zero_ok=False):
    """4 choices: correct + the first 3 unique distractors (no zero or negative numbers)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        lead = c.split(" ")[0].lstrip("$")
        if c in seen or not c or lead.startswith("-") or lead.startswith("−") or (lead == "0" and not zero_ok):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def digits(n):
    return [int(c) for c in reversed(str(n))]          # ones first


def parts(n):
    """Expanded form, biggest place first: 236 -> [200, 30, 6] (zeros left out)."""
    ds = digits(n)
    return [ds[i] * 10 ** i for i in range(len(ds) - 1, -1, -1) if ds[i]]


def svg_wrap(w, h, body, label, family=FONT):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, family, body))


def tw(t, fs):
    t = str(t)
    return (len(t) - t.count(NB) * 0.55) * fs * 0.6


def text(x, y, t, fs=17, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def unit_word(k, i):
    w = PLACE[i]
    return "%d %s" % (k, w[:-1] if k == 1 else w)


def rev(n):
    return int(str(n)[::-1])


# ------------------------------------------------------------ figures
def area_svg(tops, d, cells, label):
    """Area model with one row. tops = labels over the parts, cells = text inside ('' or '?')."""
    FS = 17
    ws = []
    for t, c in zip(tops, cells):
        need = max(tw(t, FS), tw(c, FS)) + 24
        base = {1: 62, 2: 100, 3: 130}.get(len(str(t)), 150)
        ws.append(max(need, base))
    for c in range(len(ws) - 2, -1, -1):
        ws[c] = max(ws[c], ws[c + 1] + 20)
    h = 58
    lw = tw(d, FS) + 14
    x0, y0 = lw + 4, 30
    s = []
    x = x0
    for k, w in enumerate(ws):
        s.append(text(x + w / 2, 22, tops[k], FS, col=GREEN))
        t = cells[k]
        s.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, y0, w, h, "#ffffff" if t == "?" else (FILL if k % 2 == 0 else FILL2), GREEN))
        if t:
            s.append(text(x + w / 2, y0 + h / 2 + 6, t, FS, col=RED if t == "?" else INK))
        x += w
    s.append(text(lw - 2, y0 + h / 2 + 6, str(d), FS, anchor="end", col=GREEN))
    return svg_wrap(int(x + 6), y0 + h + 6, "".join(s), label)


def area_1d(a, d, show=None):
    ps = parts(a)
    cells = show if show else [""] * len(ps)
    return area_svg([f(p) for p in ps], d, cells, "area model with %d parts: %d × %d" % (len(ps), a, d))


def short_svg(a, d, ans="", ex=None, label=None):
    """Short multiplication in columns, ones lined up on the right.
    ans: answer row as a string; '?' = red dashed box. ex: {column from the right: regrouped digit}."""
    fs = 26
    cw = fs * 0.95
    a_s = str(a)
    nd = max(len(a_s), len(ans))
    slots = nd + 1
    W = int(cw * slots + 16)
    right = W - 8
    gap = fs * 1.22
    s = []

    def col_x(i):
        return right - cw * (i + 0.5)

    def txt(x, y, t, size, col):
        return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='middle'>%s</text>"
                % (x, y, size, col, t))

    def row(t, y):
        for i, ch in enumerate(reversed(t)):
            if ch == "?":
                s.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='3' fill='none' stroke='%s' "
                         "stroke-width='2' stroke-dasharray='4 3'/>" % (col_x(i) - cw * 0.42, y - fs * 0.98, cw * 0.84, fs * 1.14, RED))
                s.append(txt(col_x(i), y - 2, "?", fs, RED))
            else:
                s.append(txt(col_x(i), y - 2, ch, fs, INK))

    y = 6 + fs
    row(a_s, y)
    y += gap
    row(str(d), y)
    s.append(txt(col_x(nd), y - 2, "×", fs, GREEN))
    y += 8
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (right - cw * slots, y, right, y, INK))
    if ans:
        y += fs + 6
        row(ans, y)
    if ex:
        y += 20
        for i, v in sorted(ex.items()):
            s.append(txt(col_x(i), y, str(v), 16, GREEN))
    H = int(y + 10)
    lab = label or ("%d times %d written as short multiplication" % (a, d))
    return svg_wrap(W, H, "".join(s), lab, "monospace")


def split_svg(whole, a, b, d=None, label=None):
    """Part-whole diagram: the whole on top, two parts below. With d: '÷ d = …' under each part."""
    FS = 18
    bw = max(64, tw(whole, FS) + 26)
    pw = max(64, tw(max(a, b), FS) + 26)
    if d is not None:
        pw = max(pw, max(tw("÷ %d = %d" % (d, v // d), 17) for v in (a, b)) + 8)
    gap = 40 if d is None else 30
    W = max(bw, 2 * pw + gap) + 8
    cx = W / 2
    s = ["<rect x='%.1f' y='4' width='%.1f' height='38' rx='6' fill='%s' stroke='%s' stroke-width='2.5'/>"
         % (cx - bw / 2, bw, FILL, GREEN), text(cx, 29, whole, FS)]
    xs = [cx - gap / 2 - pw / 2, cx + gap / 2 + pw / 2]
    for x, v in zip(xs, (a, b)):
        s.append("<line x1='%.1f' y1='42' x2='%.1f' y2='72' stroke='%s' stroke-width='2.5'/>" % (cx, x, GREEN))
        s.append("<rect x='%.1f' y='72' width='%.1f' height='38' rx='6' fill='#ffffff' stroke='%s' stroke-width='2.5'/>"
                 % (x - pw / 2, pw, GREEN))
        s.append(text(x, 97, v, FS))
        if d is not None:
            s.append(text(x, 134, "÷ %d = %d" % (d, v // d), 17, col=GREEN))
    H = 116 if d is None else 142
    if d is not None:
        lw = tw("÷ %d = %d" % (d, a // d), 17) / 2
        rw = tw("÷ %d = %d" % (d, b // d), 17) / 2
        assert xs[0] - lw >= 0 and xs[1] + rw <= W
    return svg_wrap(int(W), H, "".join(s), label or ("%d partitioned into %d and %d" % (whole, a, b)))


def array_svg(rows, cols, label=None):
    S, o = 24, 6
    body = "".join("<circle cx='%.1f' cy='%.1f' r='8.5' fill='%s'/>" % (o + c * S + S / 2.0, o + i * S + S / 2.0, GREEN)
                   for i in range(rows) for c in range(cols))
    svg = svg_wrap(cols * S + 2 * o, rows * S + 2 * o, body, label or "array of %d rows of %d dots" % (rows, cols))
    assert svg.count("<circle ") == rows * cols
    return svg


# ------------------------------------------------------------ working and typical mistakes
def pp_1d(a, d):
    ps = parts(a)
    prods = [p * d for p in ps]
    return ("Partition %s = %s. %s. Add: %s = %s." %
            (f(a), " + ".join(f(p) for p in ps),
             ". ".join("%s × %d = %s" % (f(p), d, f(p * d)) for p in ps),
             " + ".join(f(p) for p in prods), f(a * d)))


def steps_short(a, d):
    ds = digits(a)
    c, out = 0, []
    for i, x in enumerate(ds):
        p = x * d + c
        ex_ = "%d × %d" % (x, d) + (" + %d" % c if c else "")
        last = i == len(ds) - 1
        if last or p < 10:
            out.append("%s: %s = %d. Write %d." % (cap(PLACE[i]), ex_, p, p))
        else:
            out.append("%s: %s = %d. Write %d, regroup %d." % (cap(PLACE[i]), ex_, p, p % 10, p // 10))
        c = p // 10
    return " ".join(out) + " Answer: %s." % f(a * d)


def mult_row(a, d, mode="ok", k=None):
    """a × d done with a typical mistake.
    nocarry: forget every regrouped digit. skip: forget the one made in place k.
    cfirst: add the regrouped digit BEFORE multiplying. zero_d: think 0 × d = d."""
    ds = digits(a)
    c, r = 0, 0
    for i, x in enumerate(ds):
        if mode == "cfirst":
            p = (x + c) * d
        elif mode == "zero_d" and x == 0:
            p = d + c
        else:
            p = x * d + c
        if i == len(ds) - 1:
            r += p * 10 ** i
        else:
            r += (p % 10) * 10 ** i
            c = p // 10
            if mode == "nocarry" or (mode == "skip" and k == i):
                c = 0
    return r


def carry_list(a, d):
    c, out = 0, {}
    ds = digits(a)
    for i, x in enumerate(ds):
        p = x * d + c
        c = p // 10
        if c and i < len(ds) - 1:
            out[i + 1] = c
    return out


def cands_pp(a, d):
    """Partitioning mistakes for a × d (a has 2 or 3 non-zero digits)."""
    ps = parts(a)
    out = []
    # forgetting to multiply the tens (adds the tens part as it is)
    if len(ps) >= 2:
        out.append(sum(p * d for p in ps[:-2]) + ps[-2] + ps[-1] * d)
    # place-value slip: the biggest part treated as ones/tens (20 × 4 = 8)
    out.append(ps[0] // 10 * d + sum(p * d for p in ps[1:]))
    # every digit treated as ones
    out.append(sum(digits(a)) * d)
    # forgetting to multiply the ones
    out.append(sum(p * d for p in ps[:-1]) + ps[-1])
    # parts written side by side
    cc = int("".join(str(p * d) for p in ps))
    if cc < 10000:
        out.append(cc)
    out += [mult_row(a, d, "nocarry"), a + d, a * (d + 1), a * (d - 1)]
    return [v for v in out if v != a * d and v > 0]


def cands_short(a, d):
    n = len(str(a))
    out = [mult_row(a, d, "nocarry"), mult_row(a, d, "cfirst")]
    out += [mult_row(a, d, "skip", k) for k in range(n - 1)]
    out += [sum(digits(a)) * d, a * d * 10, a * (d - 1), a + d]
    return [v for v in out if v != a * d and v > 0]


def div_steps(a, d, big):
    rest = a - big
    ans = a // d
    return ("Partition %s = %s + %s. %s ÷ %d = %s and %s ÷ %d = %s. Add: %s + %s = <b>%s</b>. Check: %s × %d = %s."
            % (f(a), f(big), f(rest), f(big), d, f(big // d), f(rest), d, f(rest // d),
               f(big // d), f(rest // d), f(ans), f(ans), d, f(a)))


def best_split(a, d):
    """Biggest multiple of 10 × d (or of 100 × d) not more than a, with a rest that divides by d."""
    step = 100 * d if a >= 100 * d else 10 * d
    big = a // step * step
    while big > 0 and (a - big) % d:
        big -= step
    assert big > 0 and (a - big) % d == 0
    return big


def cands_div(a, d, big):
    rest = a - big
    ans = a // d
    out = [big // d + rest,                  # divided only the first part
           big // d,                         # forgot the second part
           big // 10 // d + rest // d,       # place-value slip on the first part
           rev(ans), ans + 10, ans - 10, a - d, ans + 1]
    return [v for v in out if v != ans and v > 0]


# ------------------------------------------------------------ set 1: 2-digit × 1-digit by partitioning
def pick_2d(rnd, seen, regroup=True):
    while True:
        a, d = rnd.randint(13, 98), rnd.randint(3, 9)
        t, o = digits(a)[1], digits(a)[0]
        if o == 0 or t == o or (a, d) in seen or a * d >= 1000:
            continue
        if regroup != (o * d >= 10):
            continue
        seen.add((a, d))
        return a, d


def set_partition_2d(rnd, seen):
    its = []
    # A: tens × 1-digit with a known fact
    for tt, d in [(40, 6), (70, 3), (60, 8), (90, 4)]:
        k = tt // 10
        e = ("%d is %s. %s × %d = %s = <b>%d</b>. Not %d: the answer is tens, not ones."
             % (tt, unit_word(k, 1), unit_word(k, 1), d, unit_word(k * d, 1), tt * d, k * d))
        its.append(mcq("What is %d × %d?  <i>Think: %d × %d = %d.</i>" % (tt, d, k, d, k * d), tt * d,
                       [k * d, tt * d * 10, tt + d], e))
    # B: use the area model
    for i in range(6):
        a, d = pick_2d(rnd, seen, regroup=i < 4)
        t, o = parts(a)
        e = pp_1d(a, d) + " Remember: %d × %d = %d, not %d." % (t, d, t * d, t // 10 * d)
        if o * d >= 10:
            e += " And %d + %d = %d: keep the ten from %d." % (t * d, o * d, a * d, o * d)
        its.append(mcq(fig(area_1d(a, d)) + "Use the area model. What is %d × %d?" % (a, d), a * d, cands_pp(a, d), e))
    # C: one part of the area model is missing
    for k in range(4):
        a, d = pick_2d(rnd, seen, regroup=k < 2)
        t, o = parts(a)
        if k % 2 == 0:
            show, ans = ["?", str(o * d)], t * d
            wrong = [t // 10 * d, t * d * 10, t + d, (t + 10) * d]
            e = "The ? part is %d × %d. %s × %d = %s = %d." % (t, d, unit_word(t // 10, 1), d, unit_word(t // 10 * d, 1), t * d)
        else:
            show, ans = [str(t * d), "?"], o * d
            wrong = [o + d, (o + 1) * d, o * d * 10, (o - 1) * d]
            e = "The ? part is %d × %d = %d." % (o, d, o * d)
        e += " Altogether: %d × %d = %d + %d = %d." % (a, d, t * d, o * d, a * d)
        its.append(mcq(fig(area_1d(a, d, show)) + "What number goes in the part marked ?", ans, wrong, e))
    # D: which partitioning is right?
    for _ in range(3):
        a, d = pick_2d(rnd, seen)
        t, o = parts(a)
        right = "%d × %d + %d × %d" % (t, d, o, d)
        wrong = ["%d × %d + %d" % (t, d, o), "%d × %d + %d × %d" % (t // 10, d, o, d), "%d + %d × %d" % (t, o, d)]
        e = ("Partition %d into %d + %d. Multiply <b>both</b> parts by %d, then add: %s = %d + %d = %d."
             % (a, t, o, d, right, t * d, o * d, a * d))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e))
    # E: missing number in the number sentence
    for k in range(3):
        a, d = pick_2d(rnd, seen)
        t, o = parts(a)
        if k == 0:
            q = "%d × %d = %d × %d + ☐ × %d" % (a, d, t, d, d)
            ans, wrong = o, [t // 10, a, o * d]
            e = "%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is <b>%d</b>." % (a, t, o, a, d, t, d, o, d, o)
        elif k == 1:
            q = "%d × %d = ☐ × %d + %d × %d" % (a, d, d, o, d)
            ans, wrong = t, [t // 10, a, t * d]
            e = ("%d = %d + %d, so %d × %d = %d × %d + %d × %d. The missing number is <b>%d</b> (%s, not %d)."
                 % (a, t, o, a, d, t, d, o, d, t, unit_word(t // 10, 1), t // 10))
        else:
            q = "%d × %d = %d + ☐" % (a, d, t * d)
            ans, wrong = o * d, [o, o + d, (o + 1) * d, a * d - t]
            e = ("%d × %d = %d × %d + %d × %d = %d + %d. The missing number is %d × %d = <b>%d</b>."
                 % (a, d, t, d, o, d, t * d, o * d, o, d, o * d))
        its.append(mcq("What number goes in the box?  <b>%s</b>" % q, ans, wrong, e))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying 2-digit numbers by partitioning", "items": its}


# ------------------------------------------------------------ set 2: 3-digit × 1-digit by partitioning
def pick_3d(rnd, seen):
    while True:
        a, d = rnd.randint(112, 989), rnd.randint(3, 9)
        ds = digits(a)
        if 0 in ds or len(set(ds)) < 3 or (a, d) in seen:
            continue
        seen.add((a, d))
        return a, d


def set_partition_3d(rnd, seen):
    its = []
    # A: hundreds × 1-digit
    for hh, d in [(300, 4), (200, 7), (500, 6), (800, 3)]:
        k = hh // 100
        e = ("%d is %s. %s × %d = %s = <b>%s</b>. Not %d (ones) or %d (tens)."
             % (hh, unit_word(k, 2), unit_word(k, 2), d, unit_word(k * d, 2), f(hh * d), k * d, k * d * 10))
        its.append(mcq("What is %d × %d?  <i>Think: %d × %d = %d.</i>" % (hh, d, k, d, k * d), f(hh * d),
                       [k * d * 10, k * d, hh * d * 10, hh + d], e))
    # B: area model, find the product
    for _ in range(6):
        a, d = pick_3d(rnd, seen)
        h = parts(a)[0]
        e = pp_1d(a, d) + " Multiply every part by %d: %d × %d = %s, not %d." % (d, h, d, f(h * d), h // 10 * d)
        its.append(mcq(fig(area_1d(a, d)) + "Use the area model. What is %d × %d?" % (a, d), f(a * d),
                       [f(v) for v in cands_pp(a, d)], e))
    # C: missing part of the area model
    for k in range(4):
        a, d = pick_3d(rnd, seen)
        ps = parts(a)
        pos = [0, 1, 2, 1][k]
        show = [f(p * d) for p in ps]
        show[pos] = "?"
        p = ps[pos]
        ans = p * d
        wrong = [ans // 10, ans * 10, p + d] if p >= 10 else [p + d, (p + 1) * d, ans * 10]
        if p >= 10:
            wrong.append((p // 10) * d if p >= 100 else (p + 10) * d)
        e = "The ? part is %d × %d = %s." % (p, d, f(ans))
        if p >= 10:
            i = len(str(p)) - 1
            e += " Think: %s × %d = %s." % (unit_word(p // 10 ** i, i), d, unit_word(p // 10 ** i * d, i))
        e += " All the parts add to %d × %d = %s." % (a, d, f(a * d))
        its.append(mcq(fig(area_1d(a, d, show)) + "What number goes in the part marked ?", f(ans), [f(v) for v in wrong], e))
    # D: which expression is equal?
    for _ in range(3):
        a, d = pick_3d(rnd, seen)
        h, t, o = parts(a)
        right = "%d × %d + %d × %d + %d × %d" % (h, d, t, d, o, d)
        wrong = ["%d × %d + %d + %d" % (h, d, t, o),
                 "%d × %d + %d × %d + %d × %d" % (h // 100, d, t // 10, d, o, d),
                 "%d × %d + %d × %d" % (h, d, o, d)]
        e = ("Partition %d into %d + %d + %d and multiply <b>every</b> part by %d: %d + %d + %d = %s."
             % (a, h, t, o, d, h * d, t * d, o * d, f(a * d)))
        its.append(mcq("Which is the same as %d × %d?" % (a, d), right, wrong, e))
    # E: missing number in a partitioned sentence
    for k in range(3):
        a, d = pick_3d(rnd, seen)
        h, t, o = parts(a)
        if k == 0:
            q = "%d × %d = %s + ☐ + %d" % (a, d, f(h * d), o * d)
            ans, wrong = t * d, [t // 10 * d, t, t * d * 10]
            e = "The missing part is the tens: %d × %d = %d." % (t, d, t * d)
        elif k == 1:
            q = "%d × %d = ☐ + %d + %d" % (a, d, t * d, o * d)
            ans, wrong = h * d, [h // 100 * d, h // 10 * d, h + d]
            e = "The missing part is the hundreds: %d × %d = %s." % (h, d, f(h * d))
        else:
            q = "%d × %d = %s + %d + ☐" % (a, d, f(h * d), t * d)
            ans, wrong = o * d, [o, o + d, (o + 1) * d]
            e = "The missing part is the ones: %d × %d = %d." % (o, d, o * d)
        e += " Check: %s + %d + %d = %s." % (f(h * d), t * d, o * d, f(a * d))
        its.append(mcq("What number goes in the box?  <b>%s</b>" % q, f(ans), [f(v) for v in wrong], e))
    assert len(its) == 20, len(its)
    return {"title": "Multiplying 3-digit numbers by partitioning", "items": its}


# ------------------------------------------------------------ set 3: short multiplication
def pick_short(rnd, seen, n, zero=False):
    while True:
        a, d = rnd.randint(10 ** (n - 1) + 1, 10 ** n - 1), rnd.randint(3, 9)
        ds = digits(a)
        if (a, d) in seen:
            continue
        if zero:
            if ds[1] != 0 or ds[0] == 0 or ds[0] * d < 10:
                continue
        elif 0 in ds or len(carry_list(a, d)) < n - 1 or len(set(ds)) < n:
            continue
        seen.add((a, d))
        return a, d


def set_short(rnd, seen):
    its = []
    for i in range(5):
        a, d = pick_short(rnd, seen, 2)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if i % 2 == 0 else "Use short multiplication to find %d × %d." % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_short(a, d)], steps_short(a, d)))
    for i in range(7):
        a, d = pick_short(rnd, seen, 3)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if i % 2 == 1 else "Use short multiplication to find %d × %d." % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in cands_short(a, d)], steps_short(a, d)))
    # zero in the tens place
    for i in range(2):
        a, d = pick_short(rnd, seen, 3, zero=True)
        c = carry_list(a, d)[1]
        wrong = [mult_row(a, d, "skip", 0), mult_row(a, d, "zero_d"), int(str(a).replace("0", "")) * d,
                 mult_row(a, d, "nocarry")]
        e = steps_short(a, d) + " 0 × %d = 0, but you still write the regrouped %d in the tens." % (d, c)
        q = (fig(short_svg(a, d)) + "Use short multiplication.") if i == 0 else "Use short multiplication to find %d × %d." % (a, d)
        its.append(mcq(q, f(a * d), [f(v) for v in wrong], e))
    # what to write and what to regroup
    for a, d in [(47, 6), (58, 7)]:
        seen.add((a, d))
        o = digits(a)[0]
        p = o * d
        right = "Write %d, regroup %d" % (p % 10, p // 10)
        wrong = ["Write %d, regroup %d" % (p // 10, p % 10), "Write %d" % p, "Write %d, regroup %d" % (p % 10, p // 10 + 1)]
        e = ("%d × %d = %d = %s and %s. Write the %d in the ones column. Regroup the %d ten%s into the tens column. "
             % (o, d, p, unit_word(p // 10, 1), unit_word(p % 10, 0), p % 10, p // 10, "" if p // 10 == 1 else "s")
             + steps_short(a, d))
        its.append(mcq(fig(short_svg(a, d)) + "Start with the ones: %d × %d = %d. What do you do?" % (o, d, p), right, wrong, e))
    # missing digit in the answer
    k = 0
    while k < 4:
        a, d = pick_short(rnd, seen, 3 if k >= 1 else 2)
        ans = str(a * d)
        pos = 1 if k < 2 else 2
        ex = carry_list(a, d)
        if pos not in ex or len(ans) <= pos:
            continue
        right = int(ans[-1 - pos])
        x = digits(a)[pos]
        c = ex[pos]
        p = x * d + c
        cand = []
        for w in [mult_row(a, d, "skip", pos - 1), mult_row(a, d, "cfirst")]:
            ws = str(w)
            if len(ws) > pos:
                cand.append(int(ws[-1 - pos]))
        cand += [(x * d) % 10, p // 10 % 10, (x + c) * d % 10, c, (right + 1) % 10]
        wr = []
        for v in cand:
            if v != right and v not in wr:
                wr.append(v)
        if len(wr) < 3:
            continue
        show = list(ans)
        show[-1 - pos] = "?"
        last = pos == len(digits(a)) - 1
        e = ("%s column: %d × %d = %d, then add the regrouped %d: %d. Write %d%s. "
             % (cap(PLACE[pos]), x, d, x * d, c, p, p if last else p % 10,
                ", regroup %d" % (p // 10) if p >= 10 and not last else ""))
        if last and p >= 10:
            e += "The ? is the %s digit, %d. " % (PLACE[pos], right)
        e += "Full working: " + steps_short(a, d)
        its.append(mcq(fig(short_svg(a, d, "".join(show), ex)) + "What digit goes in the box marked ?",
                       str(right), [str(v) for v in wr], e, zero_ok=True))
        k += 1
    assert len(its) == 20, len(its)
    return {"title": "Short multiplication", "items": its}


# ------------------------------------------------------------ set 4: division by partitioning and known facts
def set_divide():
    its = []
    # A: multiples of 10 ÷ 1-digit with a known fact
    for a, d in [(80, 4), (150, 5), (240, 6), (210, 7)]:
        k = a // 10
        e = ("%d is %s. %s ÷ %d = %s = <b>%d</b>. Not %d: the answer is tens, not ones. Check: %d × %d = %d."
             % (a, unit_word(k, 1), unit_word(k, 1), d, unit_word(k // d, 1), a // d, k // d, a // d, d, a))
        its.append(mcq("What is %d ÷ %d?  <i>Think: %d ÷ %d = %d.</i>" % (a, d, k, d, k // d), a // d,
                       [k // d, a * d, a - d, a // d * 10], e))
    # B: divide by partitioning (figure for the first four)
    for i, (a, d) in enumerate([(84, 4), (96, 3), (72, 4), (91, 7), (78, 6), (85, 5)]):
        big = best_split(a, d)
        rest = a - big
        e = div_steps(a, d, big)
        if big != a // 10 * 10:
            e = ("%d tens do not divide equally by %d, so partition into parts that do. " % (a // 10, d)) + e
        e += " Divide <b>both</b> parts, not just the first."
        q = "What is %d ÷ %d?" % (a, d)
        if i < 4:
            q = fig(split_svg(a, big, rest)) + "%d is partitioned like this. What is %d ÷ %d?" % (a, a, d)
        its.append(mcq(q, a // d, cands_div(a, d, big), e))
    # C: which split helps?
    for a, d in [(72, 4), (84, 6), (92, 4), (91, 7)]:
        big = best_split(a, d)
        right = "%d + %d" % (big, a - big)
        wrong = []
        for x in range(a // 10 * 10, 0, -10):
            if x % d or (a - x) % d:
                wrong.append("%d + %d" % (x, a - x))
        assert len(wrong) >= 3, (a, d)
        wrong = wrong[:3]
        e = ("Both parts must divide equally by %d. %d ÷ %d = %d and %d ÷ %d = %d, so %d ÷ %d = %d. "
             "In the other splits, at least one part does not divide equally by %d."
             % (d, big, d, big // d, a - big, d, (a - big) // d, a, d, a // d, d))
        its.append(mcq("Which split makes <b>%d ÷ %d</b> easy to work out?" % (a, d), right, wrong, e))
    # D: missing numbers with the inverse
    its.append(mcq("What number goes in the box?  <b>☐ ÷ 4 = 23</b>", 92, [27, 19, 82],
                   "Use the inverse: ☐ = 23 × 4 = 80 + 12 = <b>92</b>. Check: 92 ÷ 4 = 23. "
                   "(27 is 23 + 4. 82 forgets the ten in 12.)"))
    its.append(mcq("What number goes in the box?  <b>96 ÷ ☐ = 32</b>", 3, [64, 4, 128],
                   "How many 32s make 96? 32 × 3 = 90 + 6 = 96, so ☐ = <b>3</b>. Check: 96 ÷ 3 = 32."))
    its.append(mcq("What number goes in the box?  <b>7 × ☐ = 84</b>", 12, [77, 14, 91],
                   "Use the inverse: ☐ = 84 ÷ 7. Partition 84 = 70 + 14. 70 ÷ 7 = 10 and 14 ÷ 7 = 2, so ☐ = <b>12</b>. "
                   "Check: 7 × 12 = 84."))
    # E: 3-digit ÷ 1-digit by partitioning
    for a, d in [(369, 3), (856, 8), (484, 4)]:
        big = best_split(a, d)
        rest = a - big
        ans = a // d
        wrong = [big // d + rest, rev(ans), big // 100 // d + rest // d, ans * 10, ans + 10]
        if ans % 100 < 10:
            wrong.insert(0, int(str(ans).replace("0", "")))
        e = div_steps(a, d, big)
        if ans % 100 < 10:
            e += " The answer has 0 tens, so it is %d, not %d." % (ans, int(str(ans).replace("0", "")))
        its.append(mcq("What is %d ÷ %d?" % (a, d), ans, [v for v in wrong if v != ans], e))
    assert len(its) == 20, len(its)
    return {"title": "Dividing by partitioning and known facts", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_story():
    its = []
    mult = [
        ("Three buses take Year 4 on a school excursion. Each bus has 57 seats. How many seats is that altogether?", 57, 3, "{} seats"),
        ("A box holds 24 muesli bars. The school canteen buys 6 boxes. How many muesli bars is that?", 24, 6, "{} muesli bars"),
        ("At the swimming carnival the seats are in 8 rows. Each row has 35 seats. How many seats are there?", 35, 8, "{} seats"),
        ("A netball costs $18. The school buys 7 netballs. How much do they cost altogether?", 18, 7, "${}"),
        ("A school vegetable garden has 6 rows of carrots. Each row has 48 carrots. How many carrots are there?", 48, 6, "{} carrots"),
        ("The school hall has 9 rows of chairs with 26 chairs in each row. How many chairs are there?", 26, 9, "{} chairs"),
        ("Tickets to the school concert cost $8 each. The class sells 136 tickets. How much money is that?", 136, 8, "${}"),
        ("Sausages come in packs of 8. The school buys 45 packs for the sausage sizzle. How many sausages is that?", 45, 8, "{} sausages"),
        ("Mei runs 4 laps of a 400 m running track. How far does she run?", 400, 4, "{} m"),
        ("Each class at the athletics carnival has 27 students. There are 5 classes. How many students is that?", 27, 5, "{} students"),
    ]
    for q, a, d, fm in mult:
        ps = parts(a)
        e = "Equal groups, so multiply: %d × %d. " % (a, d)
        if len(ps) > 1:
            e += pp_1d(a, d) + " "
            wrong = cands_pp(a, d)
        else:
            k = ps[0]
            i = len(str(k)) - 1
            e += "%s × %d = %s. " % (unit_word(k // 10 ** i, i), d, unit_word(k // 10 ** i * d, i))
            wrong = [a * d // 10, a * d * 10, a + d, a * (d - 1)]
        e += "The answer is <b>%s</b>." % fm.format(f(a * d))
        its.append(mcq(q, fm.format(f(a * d)), [fm.format(f(v)) for v in wrong], e))
    div = [
        ("84 students are split equally into 4 sport houses. How many students are in each house?", 84, 4, "{} students"),
        ("96 oranges are packed into bags of 6. How many bags are filled?", 96, 6, "{} bags"),
        ("Three friends share the cost of a $54 present equally. How much does each friend pay?", 54, 3, "${}"),
        ("The 128 students in Year 4 line up in 4 equal lines. How many students are in each line?", 128, 4, "{} students"),
        ("91 chairs are set out in 7 equal rows for assembly. How many chairs are in each row?", 91, 7, "{} chairs"),
        ("A 72 cm ribbon is cut into 3 equal pieces. How long is each piece?", 72, 3, "{} cm"),
        ("Liam reads 8 pages each night. How many nights does it take him to read a 96-page book?", 96, 8, "{} nights"),
    ]
    for q, a, d, fm in div:
        big = best_split(a, d)
        how = "Sharing equally" if "equal" in q or "share" in q else "Making groups of %d" % d
        e = "%s, so divide: %d ÷ %d. " % (how, a, d) + div_steps(a, d, big)
        its.append(mcq(q, fm.format(a // d), [fm.format(v) for v in cands_div(a, d, big)], e))
    its.append(mcq("Jack buys 4 pies at the school canteen. Each pie costs $5. He pays with a $50 note. How much change does he get?",
                   "$30", ["$20", "$46", "$45"],
                   "Step 1: cost: 4 × $5 = $20. Step 2: change: $50 − $20 = <b>$30</b>. ($20 is the cost, not the change.)"))
    its.append(mcq("Isla has 6 packets of 24 stickers. She shares all the stickers equally among 4 friends. How many stickers does each friend get?",
                   "36", ["144", "54", "6"],
                   "Step 1: 6 × 24 = 120 + 24 = 144 stickers. Step 2: 144 ÷ 4. Partition 144 = 120 + 24. "
                   "120 ÷ 4 = 30 and 24 ÷ 4 = 6, so each friend gets <b>36</b>. Check: 36 × 4 = 144. (54 forgets to divide the 24.)"))
    its.append(mcq("For assembly there are 5 rows of 16 chairs and 3 rows of 12 chairs. How many chairs are there?",
                   "116", ["36", "128", "96"],
                   "Step 1: 5 × 16 = 50 + 30 = 80 and 3 × 12 = 30 + 6 = 36. Step 2: 80 + 36 = <b>116</b> chairs."))
    # verify the two-step answers
    assert 50 - 4 * 5 == 30 and 6 * 24 // 4 == 36 and 6 * 24 % 4 == 0 and 5 * 16 + 3 * 12 == 116
    assert len(its) == 20, len(its)
    return {"title": "Multiplication and division word problems", "items": its}


# ------------------------------------------------------------ lesson
def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def body_html():
    return (
        "<h2>Use the facts you know</h2>"
        "<p>You know 4 × 6 = 24. So 40 × 6 is 4 tens × 6 = 24 tens = 240. "
        "And 400 × 6 is 24 hundreds = 2400. Division works the same way: 80 ÷ 4 is 8 tens ÷ 4 = 2 tens = 20.</p>"
        "<h2>Multiply by partitioning</h2>"
        "<p><b>Partition</b> the bigger number into hundreds, tens and ones. Multiply <b>every</b> part. Then add the parts.</p>"
        "<figure class='sn-fig'>" + area_1d(34, 6, ["180", "24"]) +
        "<figcaption>34 × 6 = 30 × 6 + 4 × 6 = 180 + 24 = 204.</figcaption></figure>" +
        ex("3-digit × 1-digit", "236 × 4 = ?",
           "236 = 200 + 30 + 6. 200 × 4 = 800, 30 × 4 = 120 and 6 × 4 = 24. Add: 800 + 120 + 24 = 944.", "944") +
        "<figure class='sn-fig'>" + area_1d(236, 4, ["800", "120", "24"]) +
        "<figcaption>The area model for 236 × 4 has three parts.</figcaption></figure>"
        "<h2>Short multiplication</h2>"
        "<p>Short multiplication is the same idea written in columns. Start with the ones. "
        "If a product is 10 or more, write the ones digit and <b>regroup</b> the tens into the next column.</p>"
        "<figure class='sn-fig'>" + short_svg(47, 6, "282", {1: 4}) +
        "<figcaption>7 × 6 = 42: write 2, regroup 4. Then 4 × 6 = 24, plus the 4 is 28. So 47 × 6 = 282.</figcaption></figure>"
        "<h2>Divide by partitioning</h2>"
        "<p>Partition the number into parts that divide equally. Divide each part, then add the answers.</p>"
        "<figure class='sn-fig'>" + split_svg(84, 80, 4, 4, "84 partitioned into 80 and 4, each divided by 4") +
        "<figcaption>84 ÷ 4 = 80 ÷ 4 + 4 ÷ 4 = 20 + 1 = 21.</figcaption></figure>" +
        ex("When the tens do not divide equally", "72 ÷ 4 = ?",
           "7 tens do not divide equally by 4. Use 72 = 40 + 32. 40 ÷ 4 = 10 and 32 ÷ 4 = 8. Add: 10 + 8 = 18. "
           "Check: 18 × 4 = 72.", "18") +
        "<p>Always check a division with multiplication. Multiplication and division are <b>inverse</b> operations.</p>"
        "<h2>Equal groups, sharing and arrays</h2>"
        "<p>Equal groups or rows in an array: multiply. Sharing equally or making equal groups from a total: divide.</p>"
        "<figure class='sn-fig'>" + array_svg(3, 8, "array of 3 rows of 8 dots") +
        "<figcaption>3 rows of 8 is 3 × 8 = 24. Sharing the 24 into 3 rows gives 24 ÷ 3 = 8.</figcaption></figure>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Forgetting to multiply the tens (34 × 6 = 30 + 24 = 54)", "Multiply every part: 30 × 6 = 180, so 180 + 24 = 204"],
            ["Place value slip (30 × 6 = 18)", "30 × 6 = 3 tens × 6 = 18 tens = 180"],
            ["Forgetting the regrouped digit (47 × 6 = 242)", "Add the regrouped 4: 4 × 6 + 4 = 28, so 282"],
            ["Dividing only one part (84 ÷ 4 = 20 + 4 = 24)", "Divide both parts: 80 ÷ 4 = 20 and 4 ÷ 4 = 1, so 21"],
            ["Splitting into parts that do not divide (72 = 70 + 2 for ÷ 4)", "Choose 72 = 40 + 32. Both parts divide by 4"],
        ])
    )


FAQ = [
    {"q": "What multiplication strategies do Year 4 students learn in Australia?",
     "a": "Year 4 students use their multiplication facts with partitioning, the area model and short multiplication. For 34 × 6 they work out 30 × 6 = 180 and 4 × 6 = 24, then add to get 204."},
    {"q": "How do you divide by partitioning?",
     "a": "Split the number into parts that each divide equally, divide each part and add the answers. For 84 ÷ 4, use 80 ÷ 4 = 20 and 4 ÷ 4 = 1, so the answer is 21."},
    {"q": "Do Year 4 students learn division with remainders?",
     "a": "The Year 4 Australian Curriculum content description (AC9M4N06) focuses on division where there is no remainder. Remainders are met in Year 3 and studied further in Year 5."},
    {"q": "Do Year 4 students sit NAPLAN?",
     "a": "No. NAPLAN is for Years 3, 5, 7 and 9. The multiplication and division strategies learnt in Year 4 are the base for the Year 5 NAPLAN numeracy test."},
]


# ------------------------------------------------------------ build
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


def gen():
    rnd = random.Random(4804)
    seen = set()
    sets = [set_partition_2d(rnd, seen), set_partition_3d(rnd, seen), set_short(rnd, seen), set_divide(), set_story()]
    for s in sets:
        rnd.shuffle(s["items"])
    balance(sets, rnd)
    keys = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        pos = [0] * 4
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["q"].count("<svg") <= 1, it["q"]
            pos[it["a"]] += 1
            k = re.sub(r"<[^>]+>", "", it["q"]) + "|" + "|".join(sorted(it["c"]))
            assert k not in keys, it["q"]
            keys.add(k)
        assert pos == [5, 5, 5, 5], pos
    return {
        "country": "au", "subject": "maths", "grade": "year-4", "slug": "multiplication-and-division-strategies", "sort": 4,
        "updated": UPDATED, "pdf_url": "",
        "title": "Multiplication and Division Strategies",
        "seo_title": "Year 4 Multiplication and Division Strategies Worksheets: Partitioning, Area Model, Short Multiplication (Free)",
        "short_title": "Multiplication and division strategies",
        "domain": "Number",
        "standard_code": "AC9M4N06",
        "standard_url": "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics",
        "standard_text": "Develop efficient strategies and use appropriate digital tools for solving problems involving addition and subtraction, and multiplication and division where there is no remainder",
        "meta_desc": "Free Year 4 maths worksheets on multiplication and division strategies, following the Australian Curriculum (AC9M4N06): partitioning 2- and 3-digit numbers, the area model, short multiplication, dividing by partitioning and word problems. 100 questions with an answer key.",
        "key_big": "Partition the number into parts you know. Multiply or divide every part, then add the answers.",
        "key_sub": "34 × 6 = 30 × 6 + 4 × 6 = 180 + 24 = 204. 84 ÷ 4 = 80 ÷ 4 + 4 ÷ 4 = 20 + 1 = 21. Check a division by multiplying: 21 × 4 = 84.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures so they print large enough to read."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(area model with 3 parts)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
