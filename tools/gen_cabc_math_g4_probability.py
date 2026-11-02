# -*- coding: utf-8 -*-
"""
British Columbia Grade 4 Math: Probability experiments (BC Mathematics Curriculum, Grade 4: Data and probability)
  python3 tools/gen_cabc_math_g4_probability.py
Likelihood words (impossible, unlikely, equally likely, likely, certain), spinners and bags (size of each part),
predictions compared with tally results, more trials giving results closer to the prediction, and fair games.
Word questions show 4 of the 5 words in scale order (one word that is not the answer is left out).
Wrong answers come from real student mistakes: likely confused with certain, unlikely confused with impossible,
counting sections instead of looking at their size, expecting results to match a prediction exactly,
and "it hasn't happened, so it must happen next".
Every picture shows the colour as a letter too (R = red ...), so it still works when printed in black and white.
HTML attributes use single quotes (no backslashes in the JSON). Canadian English.
"""
import json, re, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
FILL2 = "#e6f2ea"
INK = "#2b2b2b"
FONT = "Arial, Helvetica, sans-serif"

# colour name -> (letter, fill)
COL = {
    "red": ("R", "#f28b82"),
    "blue": ("B", "#8ab4f8"),
    "yellow": ("Y", "#fde293"),
    "green": ("G", "#81c995"),
    "purple": ("P", "#c58af9"),
}
WORDS5 = ["impossible", "unlikely", "equally likely", "likely", "certain"]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + 3 unique distractors from real mistakes. Positions are balanced later."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        c = str(c)
        if c in seen or not c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": pick + [correct], "a": 3, "e": e}


def mcq_fixed(q, choices, ai, e):
    """Choices keep their order. The answer position is not moved later."""
    assert len(set(choices)) == 4 and 0 <= ai < 4
    return {"q": q, "c": list(choices), "a": ai, "e": e, "_fix": True}


def word_q(q, word, e, keep=()):
    """4 of the 5 probability words in scale order. Which word is left out is chosen in balance()."""
    assert word in WORDS5 and word not in keep
    return {"q": q, "e": e, "_word": word, "_keep": tuple(keep)}


def abcd_q(q, kind, ai, e):
    return mcq_fixed(q, ["%s %s" % (kind, L) for L in "ABCD"], ai, e)


def chance_word(k, n):
    """Word for an event that happens in k of n equal parts (compared with its complement)."""
    assert 0 <= k <= n
    if k == 0:
        return "impossible"
    if k == n:
        return "certain"
    if 2 * k == n:
        return "equally likely"
    return "likely" if 2 * k > n else "unlikely"


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs, bold=False):
    """Approximate text width in px (Arial)."""
    return len(str(t)) * fs * (0.62 if bold else 0.58)


def text(x, y, t, fs=14, anchor="middle", bold=False, col=INK, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'%s>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, extra, t))


def eq(*labels):
    """Equal sections."""
    return [(str(l), 1) for l in labels]


def amounts(sectors):
    out = {}
    for lab, u in sectors:
        out[lab] = out.get(lab, 0) + u
    return out


def colours_in(items):
    seen = []
    for c in items:
        if c in COL and c not in seen:
            seen.append(c)
    return seen


# ------------------------------------------------------------ spinner
def spinner_body(cx, cy, R, sectors, fs):
    """sectors = [(colour name or number, size)] clockwise from the top. Returns SVG parts."""
    T = sum(u for _, u in sectors)
    s = []
    if len(sectors) == 1:
        lab = sectors[0][0]
        fill = COL[lab][1] if lab in COL else "#ffffff"
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, fill, INK))
        s.append(text(cx, cy - R * 0.55 + fs * 0.35, COL[lab][0] if lab in COL else lab, fs, bold=True))
    else:
        a0 = -math.pi / 2
        for i, (lab, u) in enumerate(sectors):
            a1 = a0 + 2 * math.pi * u / T
            if lab in COL:
                fill, txt = COL[lab][1], COL[lab][0]
            else:
                fill, txt = (FILL if i % 2 == 0 else "#ffffff"), lab
            x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
            x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
            large = 1 if (a1 - a0) > math.pi else 0
            s.append("<path d='M%.1f %.1f L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (cx, cy, x0, y0, R, R, large, x1, y1, fill, INK))
            am = (a0 + a1) / 2
            rr = R * 0.66
            s.append(text(cx + rr * math.cos(am), cy + rr * math.sin(am) + fs * 0.35, txt, fs, bold=True))
            a0 = a1
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, R, INK))
    # arrow (points to the upper right, short so it never covers a letter)
    ang = math.radians(-35)
    L = R * 0.40
    tx, ty = cx + L * math.cos(ang), cy + L * math.sin(ang)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>" % (cx, cy, tx, ty, INK))
    h1 = ang + math.radians(150)
    h2 = ang - math.radians(150)
    s.append("<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s'/>" % (
        tx + 3 * math.cos(ang), ty + 3 * math.sin(ang), tx + 8 * math.cos(h1), ty + 8 * math.sin(h1),
        tx + 8 * math.cos(h2), ty + 8 * math.sin(h2), INK))
    s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='%s'/>" % (cx, cy, INK))
    return s


def key_lines(cols):
    return ["%s = %s" % (COL[c][0], c) for c in cols]


def spinner_svg(sectors, label="spinner"):
    R, pad = 62, 6
    cx, cy = pad + R, pad + R
    s = spinner_body(cx, cy, R, sectors, 16)
    cols = colours_in([l for l, _ in sectors])
    W = 2 * R + 2 * pad
    if cols:
        kx = 2 * R + 2 * pad + 12
        lines = key_lines(cols)
        y0 = cy - (len(lines) - 1) * 11 + 5
        for i, ln in enumerate(lines):
            s.append(text(kx, y0 + i * 22, ln, 15, anchor="start"))
        W = int(kx + max(tw(l, 15) for l in lines) + 6)
    H = 2 * R + 2 * pad
    return svg_wrap(W, H, "".join(s), label)


def spinners_abcd(spins, label="spinners A to D"):
    R, cw = 42, 104
    cy = 6 + R
    s = []
    allc = []
    for i, sec in enumerate(spins):
        cx = cw / 2 + i * cw
        s += spinner_body(cx, cy, R, sec, 14)
        s.append(text(cx, cy + R + 20, "Spinner " + "ABCD"[i], 15, bold=True))
        allc += [l for l, _ in sec]
    W = cw * 4
    H = cy + R + 26
    cols = colours_in(allc)
    if cols:
        s.append(text(W / 2, H + 14, "\u2003\u2003".join(key_lines(cols)), 14))
        H += 22
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ bag of counters
def bag_items(counts, rnd):
    items = []
    for c, n in counts:
        items += [c] * n
    rnd.shuffle(items)
    return items


def bag_body(x, y, items, cols, r, gap, fs):
    """A drawstring bag with counters in it. (x, y) = top left of the neck area. Returns (parts, w, h)."""
    rows = (len(items) + cols - 1) // cols
    bw = cols * gap + 16
    bh = rows * gap + 16
    top = y + 14
    s = []
    # neck and tie
    s.append("<path d='M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' fill='#f4efe4' stroke='%s' stroke-width='1.5'/>"
             % (x + bw / 2 - 14, y, x + bw / 2 + 14, y, x + bw / 2 + 22, top, x + bw / 2 - 22, top, INK))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='3'/>"
             % (x + bw / 2 - 16, y + 5, x + bw / 2 + 16, y + 5, INK))
    s.append("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='16' fill='#f4efe4' stroke='%s' stroke-width='2'/>"
             % (x, top, bw, bh, INK))
    for i, c in enumerate(items):
        rr, cc = divmod(i, cols)
        # centre the last row
        n_row = min(cols, len(items) - rr * cols)
        off = (cols - n_row) * gap / 2
        px = x + 8 + off + cc * gap + gap / 2
        py = top + 8 + rr * gap + gap / 2
        s.append("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.2'/>" % (px, py, r, COL[c][1], INK))
        s.append(text(px, py + fs * 0.35, COL[c][0], fs, bold=True))
    return s, bw, 14 + bh


def bag_svg(counts, rnd, label="bag of counters"):
    items = bag_items(counts, rnd)
    cols = 5 if len(items) > 8 else 4
    if len(items) <= 4:
        cols = len(items)
    s, bw, bh = bag_body(4, 4, items, cols, 13, 32, 14)
    lines = key_lines(colours_in([c for c, _ in counts]))
    kx = 4 + bw + 14
    cy = 4 + 14 + (bh - 14) / 2
    y0 = cy - (len(lines) - 1) * 11 + 5
    for i, ln in enumerate(lines):
        s.append(text(kx, y0 + i * 22, ln, 15, anchor="start"))
    W = int(kx + max(tw(l, 15) for l in lines) + 6)
    H = int(max(bh + 8, y0 + (len(lines) - 1) * 22 + 10))
    return svg_wrap(W, H, "".join(s), label)


def bags_abcd(bags, rnd, label="bags A to D"):
    cw = 108
    s = []
    allc = []
    hmax = 0
    for i, counts in enumerate(bags):
        items = bag_items(counts, rnd)
        assert len(items) <= 6
        part, bw, bh = bag_body(i * cw + (cw - (3 * 28 + 16)) / 2, 4, items, 3, 12, 28, 14)
        s += part
        hmax = max(hmax, bh)
        allc += [c for c, _ in counts]
    for i in range(4):
        s.append(text(i * cw + cw / 2, 4 + hmax + 20, "Bag " + "ABCD"[i], 15, bold=True))
    W = cw * 4
    H = 4 + hmax + 26
    s.append(text(W / 2, H + 14, "\u2003\u2003".join(key_lines(colours_in(allc))), 14))
    H += 22
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ tally chart and table
def tally_marks(x, cy, v):
    s = []
    for g in range(v // 5):
        for k in range(4):
            xx = x + k * 6
            s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (x - 3, cy + 6, x + 21, cy - 6, INK))
        x += 34
    for k in range(v % 5):
        xx = x + k * 6
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (xx, cy - 8, xx, cy + 8, INK))
    return "".join(s)


def tally_width(v):
    return (v // 5) * 34 + (v % 5) * 6


def tally_svg(title, head, cats, vals, label="tally chart"):
    fs, rh = 15, 28
    c1 = int(max(max(tw(c, fs) for c in cats), tw(head, fs, True)) + 20)
    c2 = int(max(max(tally_width(v) for v in vals) + 24, 90))
    top = 28
    W = int(max(4 + c1 + c2 + 4, tw(title, 16, True) + 16))
    x0 = (W - c1 - c2) / 2
    s = [text(W / 2, 19, title, 16, bold=True)]
    rows = [(head, None)] + list(zip(cats, vals))
    for r, (c, v) in enumerate(rows):
        y = top + r * rh
        hd = r == 0
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0, y, c1, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x0 + c1, y, c2, rh, FILL2 if hd else "#ffffff", GREEN))
        s.append(text(x0 + 10, y + 19, c, fs, anchor="start", bold=hd))
        if hd:
            s.append(text(x0 + c1 + 10, y + 19, "Tally", fs, anchor="start", bold=True))
        else:
            s.append(tally_marks(x0 + c1 + 14, y + rh / 2, v))
    H = top + len(rows) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


def table_svg(title, head, rows, label="table"):
    fs, rh = 15, 28
    ncol = len(head)
    cw = []
    for k in range(ncol):
        cells = [head[k]] + [str(r[k]) for r in rows]
        cw.append(int(max(tw(x, fs, True) for x in cells) + 20))
    tot = sum(cw)
    W = int(max(tot + 8, tw(title, 16, True) + 16))
    x0 = (W - tot) / 2
    top = 28
    s = [text(W / 2, 19, title, 16, bold=True)]
    for r, row in enumerate([head] + rows):
        y = top + r * rh
        x = x0
        for k, cell in enumerate(row):
            hd = r == 0 or k == 0
            s.append("<rect x='%.1f' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>"
                     % (x, y, cw[k], rh, FILL2 if hd else "#ffffff", GREEN))
            s.append(text(x + cw[k] / 2, y + 19, cell, fs, bold=hd))
            x += cw[k]
    H = top + (len(rows) + 1) * rh + 4
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ lesson pictures
def scale_svg():
    W, H = 490, 92
    x0, x1, y = 50, 440, 46
    s = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='3'/>" % (x0, y, x1, y, GREEN)]
    marks = [(0, "impossible", -1), (0.25, "unlikely", 1), (0.5, "equally likely", -1), (0.75, "likely", 1), (1, "certain", -1)]
    for f, w, side in marks:
        x = x0 + f * (x1 - x0)
        s.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y - 8, x, y + 8, GREEN))
        s.append(text(x, y - 16 if side < 0 else y + 29, w, 15, bold=True))
    return svg_wrap(W, H, "".join(s), "chance scale from impossible to certain")


def cube_faces_svg():
    pips = {1: [(1, 1)], 2: [(0, 0), (2, 2)], 3: [(0, 0), (1, 1), (2, 2)], 4: [(0, 0), (2, 0), (0, 2), (2, 2)],
            5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], 6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]}
    sz, gap = 46, 12
    s = []
    for i in range(6):
        x = 4 + i * (sz + gap)
        s.append("<rect x='%d' y='4' width='%d' height='%d' rx='8' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, sz, sz, INK))
        for (px, py) in pips[i + 1]:
            s.append("<circle cx='%.1f' cy='%.1f' r='4.5' fill='%s'/>" % (x + 11 + px * 12, 4 + 11 + py * 12, INK))
        s.append(text(x + sz / 2, 4 + sz + 20, str(i + 1), 15, bold=True))
    return svg_wrap(4 + 6 * sz + 5 * gap + 4, 4 + sz + 28, "".join(s), "the six faces of a number cube")


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


def table(head, rows, cls="sn-table"):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='%s'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (cls, h, b)


def assign_words(items, cnt, rnd):
    """Pick which of the 5 words to leave out of each word question, so no answer position is used more than 5 times."""
    opts = []
    for it in items:
        o = []
        for om in WORDS5:
            if om == it["_word"] or om in it["_keep"]:
                continue
            ch = [w for w in WORDS5 if w != om]
            o.append((ch.index(it["_word"]), ch))
        rnd.shuffle(o)
        o.sort(key=lambda t: cnt[t[0]])
        opts.append(o)
    order = sorted(range(len(items)), key=lambda i: len({p for p, _ in opts[i]}))
    pick = {}

    def dfs(k):
        if k == len(order):
            return True
        i = order[k]
        for p, ch in sorted(opts[i], key=lambda t: cnt[t[0]]):
            if cnt[p] < 5:
                cnt[p] += 1
                pick[i] = (p, ch)
                if dfs(k + 1):
                    return True
                cnt[p] -= 1
        return False

    assert dfs(0), "cannot balance word questions"
    for i, it in enumerate(items):
        p, ch = pick[i]
        it["c"], it["a"] = ch, p
        del it["_word"], it["_keep"]


def balance(sets, rnd):
    """Fixed questions keep their order. The rest are moved so every position is right 5 times in each set."""
    for s in sets:
        cnt, free, words = [0] * 4, [], []
        for it in s["items"]:
            if "_word" in it:
                words.append(it)
            elif it.pop("_fix", False):
                cnt[it["a"]] += 1
            else:
                free.append(it)
        assign_words(words, cnt, rnd)
        targets = []
        for p in range(4):
            assert cnt[p] <= 5, (s["title"], cnt)
            targets += [p] * (5 - cnt[p])
        rnd.shuffle(targets)
        for it, t in zip(free, targets):
            corr = it["c"][it["a"]]
            wrong = [c for k, c in enumerate(it["c"]) if k != it["a"]]
            rnd.shuffle(wrong)
            wrong.insert(t, corr)
            it["c"] = wrong
            it["a"] = t
        final = [sum(1 for it in s["items"] if it["a"] == i) for i in range(4)]
        assert final == [5, 5, 5, 5], (s["title"], final)


def mark_large(u, pattern):
    """Tag pictures that must print larger (A to D panels, tables, tally charts, number cube faces) so their labels stay readable."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ set 1: likelihood words
def set_words(rnd):
    its = []
    its.append(word_q("Next July 1 will be Canada Day. How likely is this?", "certain",
                      "Canada Day is on July 1 every year. It must happen, so it is certain."))
    its.append(word_q("Kai is 9 years old. On his next birthday, he will turn 10. How likely is this?", "certain",
                      "Everyone gets one year older on their birthday. 9 + 1 = 10, so it is certain."))
    its.append(word_q("Today is Friday. Tomorrow will be Saturday. How likely is this?", "certain",
                      "The days of the week always come in the same order. Saturday always comes after Friday, so it is certain."))
    its.append(word_q("A salmon will climb to the top of a cedar tree. How likely is this?", "impossible",
                      "Salmon live in water and cannot climb trees. This can never happen, so it is impossible."))
    its.append(word_q("Nadia rolls a number cube with the numbers 1 to 6. She will roll a 7. How likely is this?", "impossible",
                      "There is no 7 on the cube. She can never roll a 7, so it is impossible."))
    its.append(word_q("Liam is 9 years old. Next year he will be 8 years old. How likely is this?", "impossible",
                      "You cannot get younger. Next year Liam will be 10, so being 8 is impossible."))
    its.append(word_q("It will rain in Vancouver on November 20. How likely is this?", "likely",
                      "Vancouver gets rain on most days in November. But some November days are dry, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("A July afternoon in Kelowna will be warm. How likely is this?", "likely",
                      "Summers in the Okanagan are hot, so most July afternoons are warm. A few days can be cool, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("The next vehicle that drives past the school will have 4 wheels. How likely is this?", "likely",
                      "Most vehicles on the road are cars with 4 wheels. But the next one could be a motorcycle or a big truck, "
                      "so it is likely, not certain."))
    its.append(word_q("Emma will find a $20 bill on the sidewalk on the way to school. How likely is this?", "unlikely",
                      "It could happen, but it almost never does. So it is unlikely. It is not impossible: people do drop money.",
                      keep=("impossible",)))
    its.append(word_q("A black bear will walk onto the school field today. How likely is this?", "unlikely",
                      "Bears live in BC forests and sometimes wander into towns. But on any one day this hardly ever happens, "
                      "so it is unlikely, not impossible.", keep=("impossible",)))
    its.append(word_q("It will be sunny every single day of November in Vancouver. How likely is this?", "unlikely",
                      "November in Vancouver is rainy. Sun on all 30 days could happen, but it is very unlikely.",
                      keep=("impossible",)))
    its.append(word_q("Owen’s hockey team will score 20 goals in one game. How likely is this?", "unlikely",
                      "Hockey teams usually score a few goals in a game. 20 goals is possible, but it is unlikely."))
    its.append(word_q("Hana tosses a coin. It will land on heads. How likely is this?", "equally likely",
                      "A coin has 2 sides: heads and tails. Heads is as likely to happen as not to happen, "
                      "so it is equally likely."))
    its.append(word_q("Mateo’s friend hides a toonie in one of her two closed hands. Mateo picks a hand. "
                      "He will pick the hand with the toonie. How likely is this?", "equally likely",
                      "The toonie is in 1 of the 2 hands. Picking the toonie hand and picking the empty hand "
                      "have the same chance, so it is equally likely."))
    assert len([n for n in range(1, 7) if n % 2 == 0]) == 3
    its.append(word_q("Simran rolls a number cube with the numbers 1 to 6. She will roll an even number. How likely is this?",
                      "equally likely",
                      "Even: 2, 4, 6 (3 faces). Not even: 1, 3, 5 (3 faces). 3 and 3 are the same, so it is equally likely."))
    its.append(mcq("Which event is impossible?", "A week will have 8 days",
                   ["It will rain in Nanaimo on Saturday", "Hana will lose a tooth this year", "Wei will see a bald eagle today"],
                   "Every week has 7 days, so a week with 8 days can never happen. The other events could happen."))
    its.append(mcq("Which event is certain?", "January 1 will come after December 31",
                   ["It will snow in Prince George in January", "A tossed coin will land on heads", "It will rain in Victoria tomorrow"],
                   "The calendar always goes from December 31 to January 1, so it must happen. "
                   "Snow in Prince George in January is likely, but not certain."))
    its.append(word_q("Most students in Ryan’s class walk to school. Ryan says, “It is certain that the next student "
                      "to arrive will walk.” Which word should he use instead?", "likely",
                      "Most students walk, so it will probably happen. But some students come by bus or car, "
                      "so it is likely, not certain.", keep=("certain",)))
    its.append(word_q("Only 3 of the 25 students will be picked to read the morning announcements. Chloe says, "
                      "“It is impossible that I will be picked.” Which word should she use instead?", "unlikely",
                      "3 of the 25 students will be picked, so Chloe could be one of them. It is possible, but not very likely. "
                      "The right word is unlikely, not impossible.", keep=("impossible",)))
    assert len(its) == 20
    return {"title": "Likelihood words: impossible to certain", "items": its}


# ------------------------------------------------------------ set 2: spinners and bags
def set_spin_bag(rnd):
    its = []
    F = lambda sec: fig(spinner_svg(sec))
    S = lambda spins: fig(spinners_abcd(spins))
    B = lambda counts: fig(bag_svg(counts, rnd))
    G = lambda bags: fig(bags_abcd(bags, rnd))
    its.append(mcq(F(eq("red", "red", "blue", "red")) + "The spinner has 4 equal sections. Which colour is the arrow most likely to land on?",
                   "red", ["blue", "equally likely", "green"],
                   "3 of the 4 equal sections are red and only 1 is blue, so red is most likely. "
                   "(There is no green, so green is impossible.)"))
    its.append(word_q(F(eq("yellow", "yellow", "yellow", "yellow")) + "Landing on yellow is …", "certain",
                      "Every section is yellow. The arrow must land on yellow, so it is certain."))
    its.append(word_q(B([("red", 5), ("yellow", 3)]) + "Picking a green counter from this bag is …", "impossible",
                      "There are only red and yellow counters. There is no green counter, so it is impossible."))
    sec = eq("red", "blue", "blue", "blue", "blue", "blue")
    assert chance_word(amounts(sec)["red"], 6) == "unlikely"
    its.append(word_q(F(sec) + "Landing on red is …", "unlikely",
                      "Only 1 of the 6 equal sections is red. It can happen, but not often, so it is unlikely. "
                      "It is not impossible, because there is a red section.", keep=("impossible",)))
    assert chance_word(7, 8) == "likely"
    its.append(word_q(B([("red", 7), ("blue", 1)]) + "Picking a red counter from this bag is …", "likely",
                      "7 of the 8 counters are red, so red is likely. It is not certain, because there is 1 blue counter.",
                      keep=("certain",)))
    its.append(word_q(B([("red", 4), ("blue", 4)]) + "Picking a red counter from this bag is …", "equally likely",
                      "4 of the 8 counters are red and 4 are not. Picking red and not picking red have the same chance, "
                      "so it is equally likely."))
    sec = [("red", 3), ("blue", 1), ("green", 1), ("blue", 1)]
    assert amounts(sec) == {"red": 3, "blue": 2, "green": 1}
    its.append(mcq(F(sec) + "Which colour is the arrow most likely to land on?", "red",
                   ["blue", "green", "all equally likely"],
                   "Do not just count sections. Look at their size. The red part is half of the spinner. "
                   "The two blue sections are small: together they are less than half."))
    sec = [("yellow", 6), ("blue", 1), ("red", 2), ("blue", 1), ("red", 1), ("blue", 1)]
    assert amounts(sec) == {"yellow": 6, "blue": 3, "red": 3}
    its.append(mcq(F(sec) + "Kai says blue is most likely, because blue has the most sections. Which colour is most likely?",
                   "yellow", ["blue", "red", "all equally likely"],
                   "Kai counted sections, not their size. The one yellow section is half of the whole spinner. "
                   "Blue and red each cover only a quarter, so yellow is most likely."))
    sec = [("red", 2), ("blue", 1), ("yellow", 1)]
    its.append(mcq(F(sec) + "Which sentence is true?", "Red is more likely than blue",
                   ["Blue is more likely than red", "Red and blue are equally likely", "Landing on red is certain"],
                   "Red and blue each have 1 section, but the sections are not the same size. "
                   "Red covers half of the spinner and blue covers only a quarter, so red is more likely."))
    its.append(mcq(B([("yellow", 5), ("red", 2), ("green", 1)]) + "Put the colours in order from most likely to least likely.",
                   "yellow, red, green", ["green, red, yellow", "red, yellow, green", "yellow, green, red"],
                   "Count each colour: yellow 5, red 2, green 1. The colour with the most counters is most likely."))
    assert 2 + 3 == 5
    its.append(mcq(B([("red", 2), ("blue", 5)]) + "How many red counters must Zara add to make red and blue equally likely?",
                   "3", ["5", "7", "1"],
                   "Red and blue are equally likely when there are the same number of each. Blue has 5. "
                   "Red has 2, so add 5 − 2 = 3 red counters."))
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "red", "blue", "yellow"),
                         eq("red", "red", "red", "red"), eq("blue", "yellow", "green", "yellow")]) +
                      "On which spinner is landing on red impossible?", "Spinner", 3,
                      "Spinner D has no red section, so red is impossible there. "
                      "Spinner A has 1 red section: red is unlikely there, but not impossible."))
    D = [("red", 1), ("blue", 1), ("red", 1), ("blue", 1), ("red", 1), ("blue", 3)]
    assert amounts(D)["red"] == 3 and sum(u for _, u in D) == 8
    its.append(abcd_q(S([eq("red", "blue", "blue", "blue"), eq("red", "blue", "red", "blue"), [("red", 3), ("blue", 1)], D]) +
                      "On which spinner is landing on red most likely?", "Spinner", 2,
                      "Compare how much of each spinner is red. C is three quarters red. "
                      "D has 3 red sections, but they are small: together they are less than half of the spinner."))
    its.append(abcd_q(G([[("blue", 1), ("red", 5)], [("blue", 5), ("red", 1)], [("blue", 3), ("red", 3)], [("blue", 2), ("red", 4)]]) +
                      "From which bag is picking a blue counter most likely?", "Bag", 1,
                      "Each bag has 6 counters. Bag B has the most blue counters (5), so blue is most likely there."))
    its.append(abcd_q(S([eq("blue", "blue", "blue", "blue"), eq("blue", "blue", "blue", "red"), [("blue", 3), ("yellow", 1)],
                         eq("blue", "yellow", "red", "green")]) +
                      "On which spinner is landing on blue certain?", "Spinner", 0,
                      "Certain means it must happen. Only Spinner A is all blue. "
                      "On B and C, blue is likely, but not certain, because there is another colour too."))
    its.append(mcq("Ethan colours a spinner with 8 equal sections. He wants landing on red to be unlikely, but not impossible. "
                   "How many sections should he colour red?", "2 sections",
                   ["0 sections", "4 sections", "8 sections"],
                   "2 red sections out of 8 is less than half, so red is unlikely. 0 red sections would make red impossible. "
                   "4 would make it equally likely, and 8 would make it certain."))
    its.append(mcq("Sofia puts 10 counters in a bag. She wants picking yellow to be likely, but not certain. "
                   "Which bag should she make?", "6 yellow, 4 blue",
                   ["4 yellow, 6 blue", "5 yellow, 5 blue", "10 yellow, 0 blue"],
                   "Likely means more than half, so she needs more yellow than blue. With 10 yellow, yellow would be certain. "
                   "With 5 and 5, it would be equally likely."))
    sec = eq("green", "green", "yellow", "green", "green", "green", "yellow", "green")
    assert amounts(sec) == {"green": 6, "yellow": 2}
    its.append(mcq(F(sec) + "Zara says the arrow will probably land on yellow, because yellow is her favourite colour. "
                   "Which colour is the arrow more likely to land on?", "green",
                   ["yellow", "equally likely", "always yellow"],
                   "Your favourite colour does not change the chance. 6 of the 8 equal sections are green and 2 are yellow, "
                   "so green is more likely."))
    its.append(mcq("Leah has 10 hockey cards face down: 5 goalie cards and 5 player cards. She turns over one card. "
                   "Which sentence is true?", "A goalie card and a player card are equally likely",
                   ["A goalie card is more likely", "A goalie card is certain", "A player card is impossible"],
                   "There are 5 goalie cards and 5 player cards. The same number of each means they are equally likely."))
    its.append(mcq("A bag has 12 counters. Picking a red counter is certain. How many red counters are in the bag?",
                   "12", ["11", "6", "1"],
                   "Certain means it must happen, so every counter must be red: all 12. "
                   "With 11 red and 1 other counter, red is likely, not certain."))
    assert len(its) == 20
    return {"title": "Spinners and bags: the size of each part", "items": its}


# ------------------------------------------------------------ set 3: predict, then compare
def set_predict(rnd):
    its = []
    sp = fig(spinner_svg(eq("red", "blue", "blue", "blue")))
    assert 20 // 4 == 5 and 20 - 5 == 15
    its.append(mcq(sp + "Mateo will spin this spinner 20 times. About how many times should he predict red?",
                   "about 5 times", ["about 15 times", "about 10 times", "about 1 time"],
                   "Red is 1 of 4 equal sections, so about 1 spin in every 4 is red. 20 ÷ 4 = 5. "
                   "15 is the prediction for blue."))
    its.append(mcq(sp + "Mateo will spin this spinner 20 times. About how many times should he predict blue?",
                   "about 15 times", ["about 5 times", "about 10 times", "about 3 times"],
                   "Blue is 3 of 4 equal sections. 20 ÷ 4 = 5, and 3 × 5 = 15."))
    mat = [7, 13]
    assert sum(mat) == 20
    tm = fig(tally_svg("Mateo’s 20 spins", "Colour", ["Red", "Blue"], mat, label="tally chart: Mateo spins"))
    its.append(mcq(tm + "How many times did the arrow land on red?", "7", ["13", "5", "3"],
                   "Count the tally marks for red: 1 group of 5 and 2 more. 5 + 2 = 7."))
    its.append(mcq(tm + "Mateo predicted red about 5 times. How many more times did red come up than he predicted?",
                   "2", ["7", "12", "13"],
                   "Red came up 7 times. 7 − 5 = 2 more than predicted."))
    its.append(mcq(tm + "Red came up 7 times, not 5. What does this show?",
                   "Results are often a little different from a prediction",
                   ["The spinner must be broken", "Red is now more likely than blue", "Red should come up exactly 5 times"],
                   "A prediction says about how many. Real results vary a little each time. "
                   "7 is close to 5, so nothing is wrong with the spinner."))
    its.append(mcq("Wei will toss a coin 40 times. Which prediction is best?", "about 20 heads",
                   ["about 40 heads", "about 10 heads", "about 2 heads"],
                   "Heads and tails are equally likely, so predict heads about half of the time. Half of 40 is 20."))
    wei = [23, 17]
    assert sum(wei) == 40
    tw_ = fig(tally_svg("Wei’s 40 tosses", "Side", ["Heads", "Tails"], wei, label="tally chart: Wei coin tosses"))
    its.append(mcq(tw_ + "Wei predicted 20 heads. How far from the prediction was his result?", "3",
                   ["23", "17", "6"],
                   "Heads came up 23 times. 23 − 20 = 3. (6 is the difference between heads and tails.)"))
    roll = [6, 4, 5, 7, 3, 5]
    assert sum(roll) == 30
    tb = fig(table_svg("Ji-woo’s 30 rolls", ["Number", "1", "2", "3", "4", "5", "6"], [["Times"] + [str(r) for r in roll]],
                       label="table: number cube rolls"))
    its.append(mcq(tb + "Ji-woo rolled a number cube 30 times. Each number is equally likely. "
                   "About how many times should she have predicted each number?", "5", ["6", "30", "1"],
                   "The cube has 6 equally likely faces. 30 ÷ 6 = 5 times each."))
    assert roll.index(max(roll)) == 3
    its.append(mcq(tb + "Which number came up most often?", "4", ["7", "6", "1"],
                   "Find the biggest number in the Times row: 7. It is under the number 4. "
                   "(7 is how many times, and 6 is just the biggest number on the cube.)"))
    assert roll.index(min(roll)) == 4
    its.append(mcq(tb + "Which number came up the fewest times?", "5", ["3", "1", "2"],
                   "Find the smallest number in the Times row: 3. It is under the number 5. "
                   "(3 is how many times, not the number on the cube.)"))
    assert [i + 1 for i, r in enumerate(roll) if r == 5] == [3, 6]
    its.append(mcq(tb + "Which numbers came up exactly 5 times, as predicted?", "3 and 6",
                   ["5 only", "4 and 5", "1 and 2"],
                   "Look for 5 in the Times row. It is under 3 and under 6."))
    bag = fig(bag_svg([("red", 2), ("blue", 8)], rnd))
    assert 50 // 10 * 2 == 10
    its.append(mcq(bag + "Jasleen picks a counter, writes down the colour and puts it back. She does this 50 times. "
                   "About how many times should she predict red?", "about 10 times",
                   ["about 2 times", "about 25 times", "about 40 times"],
                   "2 of the 10 counters are red. 50 is 5 groups of 10, so predict 5 × 2 = 10 red. "
                   "25 would be right only if half the counters were red."))
    its.append(mcq("Jasleen’s bag has 2 red and 8 blue counters. She predicted 10 red in 50 picks. She got 13 red. "
                   "Which sentence is true?", "13 is close to her prediction",
                   ["13 red is impossible with this bag", "The bag must have more red than blue", "She should get exactly 10"],
                   "Results vary. 13 is only 3 more than 10, so it is close to the prediction. "
                   "Blue still came up much more often: 50 − 13 = 37 times."))
    luc = [11, 13, 6]
    assert sum(luc) == 30
    tl = fig(tally_svg("Lucas’s 30 spins", "Colour", ["Red", "Blue", "Yellow"], luc, label="tally chart: Lucas spins"))
    its.append(mcq(tl + "Lucas’s spinner has 3 equal sections: red, blue and yellow. He predicted about 10 of each. "
                   "Which colour came up closest to his prediction?", "red", ["blue", "yellow", "all the same"],
                   "Red 11 is 1 away from 10. Blue 13 is 3 away. Yellow 6 is 4 away. Red is closest."))
    its.append(mcq(tl + "Which colour came up furthest from Lucas’s prediction of 10?", "yellow", ["red", "blue", "all the same"],
                   "Yellow 6 is 10 − 6 = 4 away. Blue 13 is 3 away and red 11 is 1 away."))
    sec = [("red", 2), ("blue", 1), ("yellow", 1)]
    its.append(mcq(fig(spinner_svg(sec)) + "Olivia will spin this spinner 40 times. About how many times should she predict red?",
                   "about 20 times", ["about 13 times", "about 10 times", "about 40 times"],
                   "Red covers half of the spinner. Half of 40 is 20. "
                   "Do not split 40 into 3 equal parts: the sections are not the same size."))
    av = [14, 6]
    tg = fig(tally_svg("Ava’s 20 spins", "Colour", ["Green", "Purple"], av, label="tally chart: Ava spins"))
    its.append(mcq(tg + "Ava’s spinner has 4 equal sections. Which spinner did she most likely use?",
                   "3 green and 1 purple section",
                   ["1 green and 3 purple sections", "2 green and 2 purple sections", "4 purple sections"],
                   "Green came up 14 times and purple 6 times. 3 of 4 sections green predicts about 15 green and 5 purple, "
                   "which is close. With 4 purple sections, green would be impossible."))
    its.append(mcq("Noah picks a counter from a bag, looks at it and puts it back. He does this 20 times. "
                   "He gets red 17 times and blue 3 times. Which bag did he most likely use?", "8 red, 2 blue",
                   ["2 red, 8 blue", "5 red, 5 blue", "10 red, 0 blue"],
                   "Red came up much more often, so the bag probably has many more red counters. "
                   "It cannot be 10 red and 0 blue, because then blue would be impossible, and he picked blue 3 times."))
    its.append(mcq(sp + "Owen predicts red about 5 times in 20 spins. Which result would be most surprising?",
                   "red 18 times", ["red 5 times", "red 6 times", "red 4 times"],
                   "Red is unlikely on this spinner. 4, 5 or 6 reds are close to the prediction. "
                   "18 reds is possible, but very surprising."))
    assert 20 - 8 - 5 == 7
    its.append(mcq("Chloe spins a spinner 20 times. She records red 8 times, blue 5 times and yellow the rest of the time. "
                   "How many times did she get yellow?", "7 times", ["13 times", "3 times", "33 times"],
                   "Step 1: red and blue: 8 + 5 = 13. Step 2: 20 − 13 = 7 times yellow."))
    assert len(its) == 20
    return {"title": "Predict, then compare with tally results", "items": its}


# ------------------------------------------------------------ set 4: more trials
def set_trials(rnd):
    its = []
    half = fig(spinner_svg([("red", 1), ("blue", 1)]))
    rows = [["10", "8", "2"], ["100", "54", "46"], ["1000", "508", "492"]]
    for r in rows:
        assert int(r[1]) + int(r[2]) == int(r[0])
    tt = fig(table_svg("Ava’s spins: half red, half blue", ["Spins", "Red", "Blue"], rows, label="table: more trials"))
    its.append(mcq(tt + "For 10 spins, Ava predicted 5 red. How far from the prediction was her result?", "3",
                   ["8", "2", "6"],
                   "She got 8 red. 8 − 5 = 3. (6 is the difference between red and blue.)"))
    assert 54 - 46 == 8
    its.append(mcq(tt + "In the 100 spins, how many more times did red come up than blue?", "8",
                   ["54", "46", "100"],
                   "Red 54, blue 46. How many more means subtract: 54 − 46 = 8."))
    its.append(mcq(tt + "Which number of spins gave a result closest to half red?", "1000 spins",
                   ["10 spins", "100 spins", "all the same"],
                   "Half of 10 is 5 (she got 8). Half of 100 is 50 (she got 54). Half of 1000 is 500 (she got 508). "
                   "508 out of 1000 is closest to half."))
    its.append(mcq("What usually happens when you do more trials of an experiment?", "Results get closer to the prediction",
                   ["Results get further from the prediction", "Results match the prediction exactly", "Every outcome becomes certain"],
                   "With only a few trials, results can be far off. With many trials, the results usually come close to "
                   "the prediction, but not always exactly."))
    its.append(mcq("Ji-woo wants to test whether a spinner is fair. Which plan is best?", "Spin it 200 times",
                   ["Spin it 2 times", "Spin it 10 times", "Look at it and guess"],
                   "More trials give results closer to the true chances. 200 spins tells you much more than 2 or 10."))
    its.append(mcq("Arjun tosses a coin 10 times and gets 7 heads. What can he say?", "10 tosses is too few to tell",
                   ["The coin is unfair", "Heads is now certain", "Tails must come up next"],
                   "With only 10 tosses, 7 heads happens quite often with a fair coin. He needs many more tosses to tell."))
    grp = [4, 7, 5, 3, 6]
    assert sum(grp) == 25
    tg = fig(table_svg("Red in 20 spins", ["Group", "1", "2", "3", "4", "5"], [["Red"] + [str(g) for g in grp]],
                       label="table: group results"))
    q4 = "Mr. Gill’s class has 5 groups. Each group spins a spinner with 1 red and 3 blue equal sections 20 times. "
    its.append(mcq(tg + q4 + "How many spins did the class do altogether?", "100", ["20", "25", "5"],
                   "5 groups × 20 spins = 100 spins."))
    its.append(mcq(tg + q4 + "How many times did red come up altogether?", "25", ["7", "75", "5"],
                   "Add the groups: 4 + 7 + 5 + 3 + 6 = 25. (75 is the number of blues: 100 − 25.)"))
    its.append(mcq(tg + q4 + "Each group predicted 5 reds. Which group’s result matched the prediction?", "group 3",
                   ["group 5", "group 2", "group 1"],
                   "Look for 5 in the Red row. It is under group 3."))
    assert 100 // 4 == 25
    its.append(mcq(tg + q4 + "For 100 spins, the class predicted 25 reds. Which result was closest to its prediction?",
                   "the whole class", ["group 2", "group 4", "group 5"],
                   "Group 2 got 7 (2 away from 5). Group 4 got 3 (2 away). Group 5 got 6 (1 away). "
                   "The whole class got 25: exactly the prediction. More trials gave a closer result."))
    its.append(mcq("Hana tosses a coin 5 times and gets tails every time. What about the next toss?",
                   "Heads and tails are still equally likely",
                   ["Heads must come up next", "Heads is now more likely", "Tails is now impossible"],
                   "A coin does not remember what happened before. On every toss, heads and tails are equally likely."))
    its.append(mcq(half + "Red has not come up in the last 4 spins. Noah says, “Red must come up next.” Is he right?",
                   "No, the chance of red stays the same",
                   ["Yes, red is due", "Yes, red is now certain", "No, red is now impossible"],
                   "The spinner does not remember. Red is still half of the spinner, so red and blue are still equally likely. "
                   "Red is never “due”."))
    its.append(mcq("Zara has not rolled a 6 in her last 10 rolls of a number cube. What is true about her next roll?",
                   "A 6 is just as likely as before",
                   ["A 6 is more likely, because it is due", "A 6 is certain", "A 6 is now impossible"],
                   "Each roll is new. A 6 is 1 of 6 equal faces every time, no matter what came before."))
    assert 1000 // 2 == 500
    its.append(mcq("Mei will toss a coin 1000 times. Which result is she most likely to get?", "about 500 heads",
                   ["about 1000 heads", "exactly 500 heads", "about 100 heads"],
                   "Half of 1000 is 500, so predict about 500 heads. Getting exactly 500 is unlikely: "
                   "results are usually a little more or a little less."))
    assert 400 // 4 == 100
    its.append(mcq(fig(spinner_svg(eq("red", "blue", "blue", "blue"))) +
                   "Lucas will spin this spinner 400 times. About how many reds should he predict?",
                   "about 100", ["about 200", "about 300", "about 4"],
                   "Red is 1 of 4 equal sections. 400 ÷ 4 = 100. (300 is the prediction for blue.)"))
    rows6 = [["60", "10", "14"], ["600", "100", "103"]]
    assert 60 // 6 == 10 and 600 // 6 == 100
    t6 = fig(table_svg("Rolling a 6", ["Rolls", "Predicted", "Got"], rows6, label="table: sixes"))
    its.append(mcq(t6 + "Which result was closer to the prediction?", "600 rolls", ["60 rolls", "both the same", "you cannot tell"],
                   "60 rolls: 14 − 10 = 4 away. 600 rolls: 103 − 100 = only 3 away, and 3 out of 600 is very little. "
                   "More rolls gave a closer result."))
    its.append(mcq(half + "Owen spins this spinner 10 times and gets red 7 times. Mei spins it 1000 times. "
                   "About how many reds is Mei most likely to get?", "about 500",
                   ["about 700", "about 70", "exactly 1000"],
                   "Red is half of the spinner. With many spins, results come close to half: about 500. "
                   "Owen’s 7 out of 10 came from only a few spins."))
    its.append(mcq("Kai wants to find out if a bag has more red or more blue counters, without looking inside. "
                   "What should he do?", "Pick and put back 100 times",
                   ["Pick 1 counter only", "Pick 2 counters", "Shake the bag"],
                   "Many picks with putting the counter back each time give results close to the real mix in the bag."))
    its.append(mcq("A bag has 5 red and 5 blue counters. Chloe picks red 3 times in a row. She puts the counter back each time. "
                   "What is true about her next pick?", "Red and blue are still equally likely",
                   ["Blue is due next", "Red is now certain", "Blue is now impossible"],
                   "She put the counters back, so the bag still has 5 red and 5 blue. The chance does not change."))
    assert 9 + 13 == 22
    its.append(mcq("Nadia spins a spinner 20 times and gets red 9 times. Ethan spins the same spinner 20 times and gets red 13 times. "
                   "They put their results together. How many reds did they get in 40 spins?", "22",
                   ["9", "13", "4"],
                   "Add the results: 9 + 13 = 22 reds in 40 spins."))
    assert len(its) == 20
    return {"title": "More trials: closer to the prediction", "items": its}


# ------------------------------------------------------------ set 5: word problems and fair games
def set_games(rnd):
    its = []
    its.append(mcq("Zoe and Harjot play a game. Zoe gets a point when the spinner lands on red. "
                   "Harjot gets a point when it lands on blue. Which spinner makes the game fair?",
                   "2 red and 2 blue sections",
                   ["3 red and 1 blue section", "1 red and 3 blue sections", "4 red sections"],
                   "A game is fair when each player is equally likely to win. With 4 equal sections, 2 red and 2 blue "
                   "cover the same amount."))
    its.append(mcq("Liam and Sofia roll a number cube. Which game is fair?", "Liam 1, 2, 3; Sofia 4, 5, 6",
                   ["Liam 1, 2; Sofia 3, 4, 5, 6", "Liam 6; Sofia 1 to 5", "Liam 1, 2, 3, 4; Sofia 5, 6"],
                   "Each face is equally likely. A game is fair when both players win on the same number of faces: 3 and 3."))
    its.append(mcq("Liam wins if a number cube shows 1 or 2. Sofia wins if it shows 3, 4, 5 or 6. Is the game fair?",
                   "No, Sofia is more likely to win",
                   ["Yes, it is fair", "No, Liam is more likely to win", "Yes, they each have numbers"],
                   "Liam has 2 faces and Sofia has 4 faces. 4 is more than 2, so Sofia is more likely to win."))
    A = eq("red", "red", "red", "blue")
    Bs = [("red", 2), ("blue", 1), ("yellow", 1)]
    C = [("red", 1), ("blue", 2), ("red", 1)]
    D = [("red", 1), ("blue", 3)]
    fair = [amounts(s).get("red", 0) == amounts(s).get("blue", 0) for s in (A, Bs, C, D)]
    assert fair == [False, False, True, False]
    its.append(abcd_q(fig(spinners_abcd([A, Bs, C, D])) +
                      "Kai wins on red. Zara wins on blue. Which spinner makes the game fair?", "Spinner", 2,
                      "On Spinner C, the two red sections together are half and blue is the other half. "
                      "On D, red and blue each have 1 section, but blue is much bigger, so it is not fair."))
    its.append(mcq("Mei wins a prize if she picks a red counter. Bag A has 3 red and 5 blue counters. "
                   "Bag B has 5 red and 3 blue counters. Which bag should she choose?", "Bag B",
                   ["Bag A", "either bag", "neither bag"],
                   "Both bags have 8 counters. Bag B has 5 red, Bag A has only 3. Red is likely in Bag B."))
    its.append(mcq("Ji-woo wins if he picks red. Bag A has 2 red and 2 blue counters. Bag B has 4 red and 6 blue counters. "
                   "Which bag gives him a better chance?", "Bag A",
                   ["Bag B, it has more red", "They are the same", "Neither, red is unlikely in both"],
                   "Bag A is half red (2 of 4). In Bag B, 4 of 10 is less than half. "
                   "More red counters does not help if there are even more blue ones."))
    its.append(word_q("At the school spring fair, 200 raffle tickets are sold. Ava buys 2 tickets. "
                      "Ava winning the raffle is …", "unlikely",
                      "Ava has only 2 of the 200 tickets. She could win, but it is unlikely.", keep=("impossible",)))
    assert chance_word(190, 200) == "likely"
    its.append(word_q("Ethan’s family buys 190 of the 200 raffle tickets. Ethan’s family winning the raffle is …", "likely",
                      "190 of the 200 tickets are theirs, so it is likely. It is not certain, because 10 tickets belong to other people.",
                      keep=("certain",)))
    its.append(mcq("200 raffle tickets are sold. Olivia buys 5 tickets and Harjot buys 20 tickets. Who is more likely to win?",
                   "Harjot", ["Olivia", "equally likely", "neither can win"],
                   "Harjot has 20 tickets and Olivia has 5. More tickets means a better chance."))
    its.append(word_q("Each of the 26 students in Ms. Chen’s class puts their name in a toque. The teacher picks one name. "
                      "Picking the name of a student in the class is …", "certain",
                      "Every name in the toque belongs to a student in the class, so it is certain.", keep=("likely",)))
    q_trip = ("The class is choosing a field trip. The teacher puts 3 slips that say Grouse Mountain and "
              "1 slip that says Science World in a bag, and picks one. ")
    its.append(mcq(q_trip + "Is this a fair way to choose?", "No, Grouse Mountain is more likely",
                   ["Yes, both places are in the bag", "No, Science World is more likely", "Yes, they are equally likely"],
                   "There are 3 Grouse Mountain slips and only 1 Science World slip. The places do not have the same chance."))
    assert 1 + 2 == 3
    its.append(mcq(q_trip + "How can she make it fair?", "Add 2 Science World slips",
                   ["Add 2 Grouse Mountain slips", "Take out the Science World slip", "Add 1 Science World slip"],
                   "Fair means the same number of slips for each place. 1 + 2 = 3 Science World slips and 3 Grouse Mountain slips."))
    assert 40 // 4 == 10
    its.append(mcq("A box has 20 granola bars: 15 chocolate chip and 5 oatmeal. Leah picks a bar without looking, "
                   "then puts it back. She does this 40 times. About how many times should she predict oatmeal?",
                   "about 10 times", ["about 30 times", "about 20 times", "about 5 times"],
                   "5 of the 20 bars are oatmeal: 1 in every 4. 40 ÷ 4 = 10. (30 is the prediction for chocolate chip.)"))
    its.append(mcq("Two soccer teams must choose who kicks off. Which way is fair?", "Toss a coin: heads or tails",
                   ["The taller captain chooses", "Roll a cube: 6 for one team, 1 to 5 for the other", "The team in red chooses"],
                   "A coin gives each team the same chance. With the cube, one team wins on 5 faces and the other on only 1."))
    its.append(mcq("A spinner has 3 equal sections: red, blue and yellow. Nadia wins on red. Owen wins on blue or yellow. "
                   "Is the game fair?", "No, Owen is more likely to win",
                   ["Yes, it is fair", "No, Nadia is more likely to win", "Yes, each player has a colour"],
                   "Owen wins on 2 of the 3 equal sections. Nadia wins on only 1, so Owen is more likely to win."))
    its.append(mcq("A spinner has 4 equal sections: red, blue, yellow and green. Nadia and Owen want a fair game. "
                   "Which way to share the colours is fair?", "Nadia red, blue; Owen yellow, green",
                   ["Nadia red; Owen blue, yellow, green", "Nadia red, blue, yellow; Owen green", "Nadia red; Owen blue, yellow"],
                   "Fair means the same number of equal sections for each player: 2 and 2. "
                   "Nadia red and Owen blue, yellow is not fair: 1 section against 2."))
    assert 4 == 2 + 2
    its.append(mcq("Harjot’s spinner has 8 equal sections: 4 red, 2 blue and 2 green. Harjot wins on red. "
                   "Emma wins on blue or green. Is the game fair?", "Yes, they are equally likely to win",
                   ["No, Harjot is more likely to win", "No, Emma is more likely to win", "No, Emma has two colours"],
                   "Harjot has 4 sections. Emma has 2 + 2 = 4 sections. 4 and 4 are the same, so the game is fair. "
                   "The number of colours does not matter."))
    its.append(word_q("In a board game, Wei needs to roll a 6 to win. He has not rolled a 6 in his last 8 turns. "
                      "Wei says, “Rolling a 6 next is certain.” Rolling a 6 on his next turn is really …", "unlikely",
                      "A 6 is only 1 of the 6 faces, so it is unlikely on any roll. Missing it 8 times does not make it due.",
                      keep=("certain",)))
    assert 300 - 156 == 144
    its.append(mcq("Students in Kamloops tossed a coin 300 times. They got heads 156 times. How many times did they get tails?",
                   "144", ["156", "300", "456"],
                   "Every toss is heads or tails. 300 − 156 = 144 tails. (456 is 300 + 156: adding instead of subtracting.)"))
    assert 30 - 12 - 9 == 9
    its.append(mcq("Ryan picks a counter from a bag and puts it back 30 times. He gets red 12 times, blue 9 times and "
                   "yellow the rest of the time. How many times did he get yellow?", "9 times",
                   ["21 times", "18 times", "51 times"],
                   "Step 1: red and blue: 12 + 9 = 21. Step 2: 30 − 21 = 9 times yellow."))
    assert len(its) == 20
    return {"title": "Word problems and fair games", "items": its}


# ------------------------------------------------------------ lesson pictures
def trials_svg():
    """Bars for the share of red in 10, 100 and 1000 spins of a half-red spinner, with a line at half."""
    data = [("10 spins", 8, 10), ("100 spins", 54, 100), ("1000 spins", 508, 1000)]
    W, H = 360, 160
    x0, y0, ph = 100, 14, 120
    s = []
    bw = 64
    for i, (lab, r, n) in enumerate(data):
        x = x0 + i * 90
        h = ph * r / n
        s.append("<rect x='%d' y='%.1f' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>"
                 % (x, y0, bw, ph, INK))
        s.append("<rect x='%d' y='%.1f' width='%d' height='%.1f' fill='%s' stroke='%s' stroke-width='1.5'/>"
                 % (x, y0 + ph - h, bw, h, COL["red"][1], INK))
        s.append(text(x + bw / 2, y0 + ph - 10, "%d red" % r, 14, bold=True))
        s.append(text(x + bw / 2, y0 + ph + 20, lab, 14))
    yh = y0 + ph / 2
    s.append("<line x1='%d' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='2' stroke-dasharray='6 4'/>"
             % (x0 - 6, yh, x0 + 2 * 90 + bw + 6, yh, GREEN))
    s.append(text(x0 - 12, yh + 5, "half", 14, anchor="end", bold=True, col=GREEN))
    s.append(text(x0 - 12, y0 + 12, "all", 14, anchor="end"))
    s.append(text(x0 - 12, y0 + ph, "none", 14, anchor="end"))
    return svg_wrap(W, H + 6, "".join(s), "share of red in 10, 100 and 1000 spins")


def body_html(rnd):
    return (
        "<h2>The five likelihood words</h2>"
        "<p>Probability tells us how likely something is to happen. "
        "<b>Impossible</b> means it can never happen. <b>Certain</b> means it must happen. "
        "<b>Unlikely</b> means it could happen, but probably will not. <b>Likely</b> means it will probably happen. "
        "<b>Equally likely</b> means it has the same chance to happen as not to happen.</p>"
        "<figure class='sn-fig'>" + scale_svg() +
        "<figcaption>From impossible to certain. Equally likely is in the middle.</figcaption></figure>" +
        table(["Word", "Meaning", "Example"], [
            ["impossible", "can never happen", "A salmon will climb a cedar tree."],
            ["unlikely", "could happen, but probably will not", "A black bear will walk onto the school field today."],
            ["equally likely", "same chance to happen or not", "A tossed coin will land on heads."],
            ["likely", "will probably happen", "It will rain in Vancouver on a November day."],
            ["certain", "must happen", "Next July 1 will be Canada Day."],
        ]) +
        "<h2>Spinners and bags: look at the size of each part</h2>"
        "<p>A spinner is more likely to land on a colour that covers <b>more</b> of it. "
        "Compare the size of the parts, not just the number of sections. "
        "In a bag, the colour with more counters is more likely.</p>"
        "<figure class='sn-fig'>" + spinner_svg([("red", 3), ("blue", 1), ("green", 1), ("blue", 1)],
                                                  "spinner: red half, 2 small blue sections, 1 small green section") +
        "<figcaption>Blue has 2 sections, but red covers half of the spinner.</figcaption></figure>" +
        ex("Example", "Which colour is the arrow most likely to land on?",
           "Red is one big section: half of the spinner. The two blue sections together are less than half.", "red") +
        "<h2>Predict, then experiment</h2>"
        "<p>Use the parts to make a prediction. Then do the experiment and record each result with a tally. "
        "Compare your results with your prediction. They are usually close, but not exactly the same.</p>"
        "<figure class='sn-fig'>" + spinner_svg(eq("red", "blue", "blue", "blue"), "spinner: 1 red and 3 blue equal sections") +
        "<figcaption>Red is 1 of 4 equal sections.</figcaption></figure>" +
        ex("Example", "You spin this spinner 20 times. Predict the number of reds.",
           "About 1 spin in every 4 is red. 20 ÷ 4 = 5.", "about 5 reds") +
        "<figure class='sn-fig'>" + tally_svg("Our 20 spins", "Colour", ["Red", "Blue"], [7, 13], label="tally chart: 20 spins") +
        "<figcaption>We got 7 reds. That is 2 more than predicted: close, not exact.</figcaption></figure>"
        "<h2>More trials, closer results</h2>"
        "<p>With only a few trials, results can be far from the prediction. "
        "With many trials, they usually come <b>closer</b> to it.</p>"
        "<figure class='sn-fig'>" + trials_svg() +
        "<figcaption>A spinner that is half red. 8 of 10 is far from half. 508 of 1000 is very close.</figcaption></figure>"
        "<h2>Fair games</h2>"
        "<p>A game is <b>fair</b> when every player has the same chance to win. "
        "With a number cube, Liam winning on 1, 2, 3 and Sofia on 4, 5, 6 is fair: 3 faces each.</p>" +
        ex("Example", "Nadia wins on red. Owen wins on blue or yellow. The spinner has 3 equal sections: red, blue, yellow. Is it fair?",
           "Owen has 2 sections and Nadia has 1.", "No, Owen is more likely to win") +
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Saying certain when it is only likely", "Certain means it must happen every time. If it could fail, it is likely"],
            ["Saying impossible when it is only unlikely", "If it could happen even once, it is not impossible"],
            ["Counting sections, not their size", "Compare how much of the spinner each colour covers"],
            ["Expecting results to match the prediction exactly", "Results vary. Close to the prediction is normal"],
            ["“It has not happened, so it must happen next”", "Coins, cubes and spinners do not remember. The chance stays the same"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about probability in BC?",
     "a": "The BC Grade 4 math curriculum includes probability experiments. Students predict an outcome, such as a spinner landing on red, do the experiment, record the results with tallies and compare them with their prediction."},
    {"q": "Why don’t my experiment results match my prediction?",
     "a": "A prediction tells you about how many times something should happen, not exactly. Results vary each time, so a result close to the prediction is normal."},
    {"q": "Why do more trials give better results?",
     "a": "With a few trials, luck can push the results far from the prediction. With many trials, the results usually come close to the true chances, like about 500 heads in 1000 coin tosses."},
    {"q": "Is probability on the Grade 4 FSA?",
     "a": "The Grade 4 FSA numeracy section is based on the BC math curriculum and asks students to reason and solve problems. Reading tally charts and tables and making predictions, as in these worksheets, is good practice for it."},
]


def gen_unit():
    rnd = random.Random(34815)
    sets = [set_words(rnd), set_spin_bag(rnd), set_predict(rnd), set_trials(rnd), set_games(rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            assert it["e"], it
            assert it["q"].count("<svg") <= 1, it["q"]
            k = it["q"] + "|" + "|".join(sorted(it["c"]))
            assert k not in seen, it["q"]
            seen.add(k)
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-4", "slug": "probability-experiments", "sort": 15,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Probability Experiments",
        "seo_title": "Grade 4 Probability Experiments Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Probability experiments",
        "domain": "Data and probability",
        "standard_code": "Grade 4: Data and probability",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/4/core",
        "standard_text": "Probability experiments",
        "meta_desc": "Free Grade 4 math worksheets on probability experiments for the BC curriculum: impossible, unlikely, equally likely, likely and certain, spinners and bags, predictions compared with tally results, why more trials get closer, and fair games. 100 questions with an answer key, good FSA numeracy practice.",
        "key_big": "Predict from the size of each part, then test it. More trials give results closer to the prediction.",
        "key_sub": "Likely is not certain, and unlikely is not impossible. Coins and spinners do not remember: an outcome is never “due”.",
        "body_html": body_html(rnd), "faq": FAQ, "sets": sets,
    }
    return u


if __name__ == "__main__":
    u = gen_unit()
    mark_large(u, "(spinners A to D|bags A to D|tally chart|table)")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
