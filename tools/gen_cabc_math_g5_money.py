# -*- coding: utf-8 -*-
"""
BC Grade 5 Math: Money and Financial Plans (BC Mathematics Curriculum, Financial literacy:
monetary calculations, including making change with amounts to 1000 dollars and developing simple financial plans)
  python3 tools/gen_cabc_math_g5_money.py
All amounts are whole numbers of cents (int), so every total, change and typical mistake is exact.
Writing money: under $1 as 45¢, whole dollars as $7, other amounts as $7.65 (never $7.6).
No pennies: cash totals are rounded to the nearest 5¢; card payments are exact. No sales tax in this unit.
Helpers copied from gen_cabc_math_g4_money.py (counting up, cash rounding, price tags, receipts) and
gen_caon_math_g5_financial.py (budget table, saving weeks). HTML attributes use single quotes.
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-bc", "math", "grade-5")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
EDGE = "#b8b0a0"
PAPER = "#fffdf5"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Ava", "Chloe", "Simran", "Jasleen", "Mei", "Ji-woo", "Hana", "Sofia", "Emma", "Leah", "Zara", "Nadia"]
BOYS = ["Liam", "Ethan", "Noah", "Arjun", "Harjot", "Wei", "Mateo", "Lucas", "Kai", "Owen", "Ryan"]


# ------------------------------------------------------------ money text
def nat(c):
    """45 -> '45¢', 700 -> '$7', 765 -> '$7.65'"""
    assert 0 < c < 1000000, c
    if c < 100:
        return "%d¢" % c
    if c % 100 == 0:
        return "$%d" % (c // 100)
    return "${}.{:02d}".format(c // 100, c % 100)


def dol(c):
    """always with cents: 700 -> '$7.00' (price tags, receipts, budgets)"""
    return "${}.{:02d}".format(c // 100, c % 100)


def mval(s):
    s = re.sub(r"<[^>]+>", "", s)
    m = re.match(r"^\$(\d+)(?:\.(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)) * 100 + int((m.group(2) or "0").ljust(2, "0"))
    m = re.match(r"^(\d+)¢$", s)
    if m:
        return int(m.group(1))
    return None


def cap(s):
    return s[0].upper() + s[1:]


def round5(c):
    """Canadian cash rounding: ends in 1, 2 down to 0; 3, 4 up to 5; 6, 7 down to 5; 8, 9 up to the next 10"""
    r = c % 5
    return c - r if r <= 2 else c + 5 - r


def ceil_div(a, b):
    return -(-a // b)


def wk(n):
    return "%d week%s" % (n, "" if n == 1 else "s")


def digs(n, k):
    return [(n // 10 ** i) % 10 for i in range(k)]


def from_digs(d):
    return sum(x * 10 ** i for i, x in enumerate(d))


def small_from_big(a, b):
    """column subtraction taking the smaller digit from the bigger one"""
    k = len(str(a))
    return from_digs([abs(x - y) for x, y in zip(digs(a, k), digs(b, k))])


def forgot_dollar_add(nums):
    """made 100¢ or more in the cents but did not regroup it as $1"""
    return sum(n // 100 for n in nums) * 100 + sum(n % 100 for n in nums) % 100


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=nat):
    """4 choices: correct + the first 3 usable unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t = {correct}
    seen_v = {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0 or c >= 1000000:
                continue
            c = fmt(c)
        c = str(c)
        v = mval(c)
        if c in seen_t or (v is not None and v in seen_v):
            continue
        seen_t.add(c)
        if v is not None:
            seen_v.add(v)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def note_if(it, val, msg):
    """add a mistake note to the explanation when that wrong answer is one of the choices"""
    t = nat(val) if isinstance(val, int) else val
    if t in it["c"][1:]:
        it["e"] += " " + msg % t
    return it


def balance(sets, rnd):
    for s in sets:
        targets = [0, 1, 2, 3] * 5
        rnd.shuffle(targets)
        for it, t in zip(s["items"], targets):
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            right = c[it["a"]]
            it["c"] = wrong[:t] + [right] + wrong[t:]
            it["a"] = t


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def obj(he):
    return "her" if he == "she" else "him"


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def text(x, y, t, fs=16, anchor="middle", col=INK, bold=True):
    return ("<text x='%.1f' y='%.1f' font-size='%d'%s fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, " font-weight='700'" if bold else "", col, anchor, t))


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ pictures
def price_svg(items, title):
    """a row of price tags: [('sketchbook', 950), ...]"""
    gap, pad, h = 8, 6, 62
    ws = [max(len(n) * 9 + 20, 86) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    H = h + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='#ffffff' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, INK))
        b.append(text(x + w / 2, pad + 24, n, 15))
        b.append(text(x + w / 2, pad + 50, dol(p), 18, col=GREEN))
        x += w + gap
    return svg_wrap(W, H, "".join(b), "price list: " + title + ": " + ", ".join("%s %s" % (n, dol(p)) for n, p in items))


def receipt_svg(title, rows, total_text="?", how=None):
    """a receipt: rows of (item, amount in cents); the total line shows total_text"""
    W, rh, fs = 290, 25, 16
    b = []
    y = 6
    b.append(text(W / 2, y + 20, title, 16, col=GREEN))
    y += 30
    b.append("<line x1='14' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y, W - 14, y, INK))
    for name, amt in rows:
        b.append(text(16, y + 19, name, fs, "start", bold=False))
        b.append(text(W - 16, y + 19, dol(amt), fs, "end", bold=False))
        y += rh
    b.append("<line x1='14' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (y + 3, W - 14, y + 3, INK))
    y += 4
    b.append(text(16, y + 20, "Total", 17, "start"))
    b.append(text(W - 16, y + 20, total_text, 17, "end", col=GREEN))
    y += rh + 2
    if how:
        b.append(text(16, y + 18, "Paid:", 15, "start", bold=False))
        b.append(text(W - 16, y + 18, how, 15, "end", bold=False))
        y += rh
    H = y + 8
    frame = "<rect x='2' y='2' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 4, H - 4, PAPER, EDGE)
    label = "receipt %s: %s; total %s" % (title, ", ".join("%s %s" % (n, dol(a)) for n, a in rows), total_text)
    return svg_wrap(W, H, frame + "".join(b), label)


def budget_svg(title, money_in, money_out):
    """budget plan: Money in (left) and Money out (right), side by side"""
    cw, gap, rh, fs = 230, 12, 26, 16
    W = 2 * cw + gap + 4
    n = max(len(money_in), len(money_out))
    top = 34
    b = [text(W / 2, 22, title, 17)]
    for k, (head, rows) in enumerate([("Money in", money_in), ("Money out", money_out)]):
        x = 2 + k * (cw + gap)
        b.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s'/>" % (x, top, cw, rh, GREEN))
        b.append(text(x + 10, top + 19, head, fs, "start", col="#ffffff"))
        y = top + rh
        for i in range(n):
            if i < len(rows):
                lab, amt = rows[i]
                b.append(text(x + 10, y + 19, lab, fs, "start", bold=False))
                b.append(text(x + cw - 10, y + 19, dol(amt), fs, "end", bold=False))
            b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1'/>" % (x, y + rh, x + cw, y + rh, EDGE))
            y += rh
        b.append("<rect x='%d' y='%d' width='%d' height='%d' fill='none' stroke='%s' stroke-width='2'/>" % (x, top, cw, y - top, EDGE))
    H = top + rh * (n + 1) + 4
    label = "budget plan %s. Money in: %s. Money out: %s" % (
        title, ", ".join("%s %s" % (a, dol(v)) for a, v in money_in), ", ".join("%s %s" % (a, dol(v)) for a, v in money_out))
    return svg_wrap(W, H, "".join(b), label)


def savings_svg(start, per, weeks):
    """savings plan table: Week 0..weeks and the total saved"""
    c0, cw, rh = 84, 72, 30
    W = c0 + cw * (weeks + 1) + 4
    H = 2 * rh + 4
    b = []
    rows = [("Week", [str(i) for i in range(weeks + 1)]), ("Saved", [dol(start + per * i) for i in range(weeks + 1)])]
    for r, (head, cells) in enumerate(rows):
        y = 2 + r * rh
        b.append("<rect x='2' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (y, c0, rh, GREEN, EDGE))
        b.append(text(2 + c0 / 2, y + 20, head, 16, col="#ffffff"))
        for i, c in enumerate(cells):
            x = 2 + c0 + i * cw
            b.append("<rect x='%d' y='%d' width='%d' height='%d' fill='#ffffff' stroke='%s' stroke-width='1.5'/>" % (x, y, cw, rh, EDGE))
            b.append(text(x + cw / 2, y + 20, c, 15, bold=(r == 0)))
    label = "savings plan table: " + ", ".join("week %d %s" % (i, dol(start + per * i)) for i in range(weeks + 1))
    return svg_wrap(W, H, "".join(b), label)


# ------------------------------------------------------------ counting up for change
def change_pts(price, paid):
    """price -> next 10¢ -> next dollar -> next $10 -> next $100 -> money paid"""
    pts, s = [price], price
    if s % 10:
        s += 10 - s % 10
        pts.append(s)
    if s % 100 and s < paid:
        s += 100 - s % 100
        pts.append(s)
    if paid >= 5000 and s % 1000 and s + 1000 - s % 1000 < paid:
        s += 1000 - s % 1000
        pts.append(s)
    if paid >= 20000 and s % 10000 and s + 10000 - s % 10000 < paid:
        s += 10000 - s % 10000
        pts.append(s)
    if s < paid:
        pts.append(paid)
    assert pts[-1] == paid and all(a < b for a, b in zip(pts, pts[1:]))
    return pts


def count_up(price, paid):
    pts = change_pts(price, paid)
    steps = ["%s + %s = %s" % (nat(a), nat(b - a), nat(b)) for a, b in zip(pts, pts[1:])]
    jumps = [b - a for a, b in zip(pts, pts[1:])]
    ch = paid - price
    assert sum(jumps) == ch
    tail = "" if len(jumps) == 1 else " Add the jumps: %s = %s." % (" + ".join(nat(j) for j in jumps), nat(ch))
    return "Count up from %s to %s: %s.%s" % (nat(price), nat(paid), ", ".join(steps), tail)


def change_cands(paid, price):
    """real change mistakes, most common first"""
    r = paid - price
    c = []
    if price % 100:
        c.append(r + 100)           # took the dollars and kept the cents: forgot the dollar used for the cents
    if paid >= 20000 and price % 10000:
        c.append(r + 10000)         # $1000 − $837.40 = $263: did not take 1 from the hundreds when regrouping
    if price % 10:
        c.append(r + 10)            # 65¢ + 45¢ "makes 100"
    if paid >= 5000 and price % 1000:
        c.append(r + 1000)
    c += [small_from_big(paid, price), price, r - 100, r - 1000, r + 5, r - 10]
    return [x for x in c if x and 0 < x < paid and x % 5 == 0]


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting up; show=False puts ? on the jumps"""
    pts = change_pts(price, paid)
    seg = [118, 124, 130, 136, 142][:len(pts) - 1]
    x0, y0 = 46, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W = xs[-1] + 46
    H = 104
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 24, y0, xs[-1] + 24, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, nat(p), 15))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        m = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a, y0 - 8, m, y0 - 50, c, y0 - 8, GREEN))
        b.append(text(m, y0 - 34, ("+" + nat(pts[i + 1] - pts[i])) if show else "+ ?", 15, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting up from %s to %s" % (nat(price), nat(paid)))


def paid_text(paid):
    one = {2000: "a $20 bill", 5000: "a $50 bill", 10000: "a $100 bill"}
    if paid in one:
        return one[paid]
    assert paid % 10000 == 0
    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    return "%s $100 bills" % words[paid // 10000]


# ============================================================ set 1: total cost of several items
def sum_expl(lines):
    """lines = [(count, price, name)]"""
    parts = []
    tots = []
    for n, p, name in lines:
        if n > 1:
            d, c = p // 100, p % 100
            if c and len(lines) == 1:
                cc = ("%d¢ = %s" % (n * c, nat(n * c))) if n * c >= 100 else "%d¢" % (n * c)
                parts.append("%d × %s: %d × $%d = $%d and %d × %d¢ = %s. $%d + %s = <b>%s</b>."
                             % (n, nat(p), n, d, n * d, n, c, cc, n * d, nat(n * c), nat(n * p)))
            elif c:
                parts.append("%d × %s: %d × $%d = $%d and %d × %d¢ = %d¢, so %s."
                             % (n, nat(p), n, d, n * d, n, c, n * c, nat(n * p)))
            else:
                parts.append("%d × %s = %s." % (n, nat(p), nat(n * p)))
        tots.append(n * p)
    T = sum(tots)
    if len(tots) == 1:
        return " ".join(parts)
    D = sum(t // 100 for t in tots)
    C = sum(t % 100 for t in tots)
    s = "Add the dollars: %s = $%d. " % (" + ".join("$%d" % (t // 100) for t in tots), D)
    cs = [t % 100 for t in tots if t % 100]
    if cs:
        if len(cs) == 1:
            s += "The cents: %d¢. " % C
        else:
            s += "Add the cents: %s = %d¢" % (" + ".join("%d¢" % x for x in cs), C)
            s += (" = %s. " % nat(C)) if C >= 100 else ". "
        s += "$%d + %s = <b>%s</b>." % (D, nat(C), nat(T))
    else:
        s += "The total is <b>%s</b>." % nat(T)
    return " ".join(parts + [s])


def total_item(q, lines, extra=None):
    T = sum(n * p for n, p, name in lines)
    tots = [n * p for n, p, name in lines]
    e = sum_expl(lines)
    cands, notes = [], []
    fd = forgot_dollar_add(tots)
    if fd != T:
        cands.append(fd)
        notes.append((fd, "%s forgets the dollars made by the cents."))
    for n, p, name in lines:
        if n > 1:
            dollars_only = T - n * (p % 100) + p % 100 if p % 100 else None
            if dollars_only:
                cands.append(dollars_only)
                notes.append((dollars_only, "%s multiplies only the dollars, not the cents."))
            cands.append(T - p)
            if len(lines) == 1:
                notes.append((T - p, "%%s is the cost of %d, not %d." % (n - 1, n)))
            else:
                notes.append((T - p, "%%s leaves out one of the %s." % name))
    # forgetting an item: the cheapest line is the one most often missed
    for i in sorted(range(len(lines)), key=lambda k: tots[k]):
        if len(lines) > 1:
            cands.append(T - tots[i])
            notes.append((T - tots[i], "%%s forgets the %s." % lines[i][2]))
    cands += (extra or []) + [T + 100, T - 100, T + 1000, T + 10]
    it = mcq(q, T, cands, e)
    for v, m in notes:
        note_if(it, v, m)
    return it


def set_total(P, rnd):
    its = []

    def tags(lines):
        return fig(price_svg([(name, p) for n, p, name in lines], "store"))

    L = [(1, 345, "notebook"), (1, 230, "pencils"), (1, 115, "eraser")]
    nm, he, his = P.next()
    its.append(total_item(tags(L) + "%s buys a notebook, pencils and an eraser. What is the total cost?" % nm, L))
    L = [(1, 475, "sandwich"), (1, 260, "juice"), (1, 180, "apple")]
    nm, he, his = P.next()
    its.append(total_item("At recess, %s buys a sandwich for $4.75, a juice for $2.60 and an apple for $1.80. "
                          "What is the total cost?" % nm, L))
    L = [(3, 425, "swim passes")]
    nm, he, his = P.next()
    its.append(total_item("%s buys 3 swim passes at $4.25 each. What is the total cost?" % nm, L))
    L = [(1, 595, "smoothie"), (1, 325, "muffin"), (1, 250, "hot chocolate")]
    nm, he, his = P.next()
    its.append(total_item("After a rainy soccer game in Vancouver, %s’s family buys a smoothie for $5.95, a muffin for $3.25 "
                          "and a hot chocolate for $2.50. What is the total cost?" % nm, L))
    L = [(4, 875, "movie tickets")]
    its.append(total_item("Four movie tickets cost $8.75 each. What is the total cost?", L))
    L = [(1, 438, "apples"), (1, 349, "bread"), (1, 529, "milk"), (1, 799, "cheese")]
    its.append(total_item(fig(receipt_svg("Grocery receipt", [(n, p) for c, p, n in L])) + "What is the total on this receipt?", L))
    L = [(1, 3499, "backpack"), (1, 649, "binder"), (1, 1295, "calculator"), (1, 1550, "lunch kit")]
    nm, he, his = P.next()
    its.append(total_item(tags(L) + "%s buys all four items for the new school year. What is the total cost?" % nm, L))
    L = [(12, 375, "hot lunches")]
    its.append(total_item("A hot lunch costs $3.75. What do 12 hot lunches cost?", L))
    nm, he, his = P.next()
    its.append(mcq("%s buys a jacket for $48.95, a toque for $21.10 and mittens for $19.85. "
                   "Which is the best estimate of the total?" % nm,
                   "about $90", ["about $80", "about $100", "about $70"],
                   "Round each price to the nearest dollar: $49 + $21 + $20 = $90. The total is <b>about $90</b> "
                   "(exactly $89.90). About $70 forgets the mittens.", fmt=str))
    L = [(1, 12999, "tent"), (1, 6450, "sleeping bag"), (1, 1875, "flashlight")]
    nm, he, his = P.next()
    its.append(total_item(tags(L) + "For a camping trip on Vancouver Island, %s’s family buys a tent, a sleeping bag and a flashlight. "
                          "What is the total cost?" % nm, L))
    L = [(1, 28900, "bike"), (1, 4995, "helmet"), (1, 2750, "lock")]
    nm, he, his = P.next()
    its.append(total_item("%s buys a bike for $289, a helmet for $49.95 and a lock for $27.50. What is the total cost?" % nm, L))
    L = [(6, 2450, "team jerseys")]
    its.append(total_item("A lacrosse team orders 6 jerseys at $24.50 each. What is the total cost?", L))
    L = [(1, 7900, "lift ticket"), (1, 5550, "snowboard rental"), (1, 1825, "lunch")]
    nm, he, his = P.next()
    its.append(total_item("For a snowboard day on Grouse Mountain, %s pays $79 for a lift ticket, $55.50 for a snowboard rental "
                          "and $18.25 for lunch. What is the total cost?" % nm, L))
    # missing price
    nm, he, his = P.next()
    paid_tot, a1, a2 = 5640, 2375, 1820
    miss = paid_tot - a1 - a2
    assert miss == 1445
    assert (paid_tot - a1, paid_tot - a2) == (3265, 3820)
    it = mcq("%s buys 3 things for a total of $56.40. Two of them cost $23.75 and $18.20. What does the third one cost?" % nm,
             miss, [paid_tot - a1, paid_tot - a2, a1 + a2, miss + 100, miss - 100],
             "First add the two prices: $23.75 + $18.20 = $41.95. Then count up from $41.95 to $56.40: "
             "5¢ + $14.40 = $14.45. The third one costs <b>$14.45</b>. Check: $41.95 + $14.45 = $56.40.")
    it["e"] += " $32.65 and $38.20 each take away only one of the two prices."
    note_if(it, a1 + a2, "%s is the cost of the two known items.")
    its.append(it)
    L = [(1, 68900, "couch"), (1, 5995, "delivery"), (2, 3450, "cushions")]
    its.append(total_item(fig(receipt_svg("Furniture store", [("couch", 68900), ("delivery", 5995), ("2 cushions × $34.50", 6900)]))
                          + "What is the total on this receipt?", L))
    L = [(1, 64999, "laptop"), (1, 3450, "case"), (1, 2275, "mouse")]
    nm, he, his = P.next()
    its.append(total_item(tags(L) + "%s’s family buys a laptop, a case and a mouse. What is the total cost?" % nm, L))
    L = [(1, 18999, "skates"), (1, 7450, "stick"), (1, 5995, "gloves"), (1, 11900, "helmet")]
    nm, he, his = P.next()
    its.append(total_item(tags(L) + "%s needs new hockey gear. What is the total cost of all four items?" % nm, L))
    L = [(2, 1915, "adult fares"), (2, 960, "child fares"), (1, 6750, "car fare")]
    nm, he, his = P.next()
    its.append(total_item("%s’s family takes a ferry to Vancouver Island. They pay for 2 adults at $19.15 each, "
                          "2 children at $9.60 each and the car at $67.50. What is the total cost?" % nm, L))
    L = [(3, 1899, "pizzas"), (2, 449, "bottles of juice")]
    its.append(total_item("For a class party, a teacher buys 3 pizzas at $18.99 each and 2 bottles of juice at $4.49 each. "
                          "What is the total cost?", L))
    L = [(4, 4550, "kayak rentals"), (1, 6000, "guide")]
    nm, he, his = P.next()
    its.append(total_item("In the Okanagan, %s’s family of 4 rents kayaks for $45.50 each and pays $60 for a guide. "
                          "What is the total cost?" % nm, L))
    assert len(its) == 20
    return {"title": "Total cost of several items", "items": its}


# ============================================================ set 2: making change to $1000
def change_item(q, price, paid, line=False, items=None):
    r = paid - price
    if line:
        q = fig(change_line(price, paid, show=False)) + q + " Count up on the number line."
    e = ""
    cands = []
    if items:
        e = "First find the total: %s = %s. " % (" + ".join(nat(p) for p in items), nat(price))
        for p in sorted(items):
            cands.append(paid - p)
    e += count_up(price, paid) + " The change is <b>%s</b>. Check: %s + %s = %s." % (nat(r), nat(price), nat(r), nat(paid))
    cands = change_cands(paid, price)[:1] + cands + change_cands(paid, price)[1:]
    it = mcq(q, r, cands, e)
    note_if(it, r + 100, "%s forgets that one dollar was used up to make the cents.")
    if paid >= 20000:
        note_if(it, r + 10000, "%s forgets that $100 was used up when regrouping.")
    if items:
        for p in items:
            note_if(it, paid - p, "%%s is the change for the %s alone." % ("first item" if p == items[0] else "second item"))
    return it


def set_change(P, rnd):
    its = []
    jobs = [(2000, 1345, "a chapter book", True), (5000, 3680, "a pair of shorts", False), (10000, 7235, "a pair of soccer cleats", True),
            (10000, 4860, "a basketball", False), (20000, 14860, "a scooter", True), (30000, 26395, "a pair of skates", False),
            (50000, 41270, "a bike", False), (100000, 83740, "a tablet", True), (50000, 12985, "a pair of hiking boots", False),
            (70000, 68925, "a mattress", False), (100000, 45615, "a set of patio chairs", False), (100000, 92465, "a fridge", True)]
    for paid, pr, thing, line in jobs:
        nm, he, his = P.next()
        q = "%s’s family buys %s for %s. They pay with %s. How much change do they get?" % (nm, thing, nat(pr), paid_text(paid))
        if paid <= 5000:
            q = "%s buys %s for %s and pays with %s. How much change does %s get?" % (nm, thing, nat(pr), paid_text(paid), he)
        its.append(change_item(q, pr, paid, line))
    # two items: forgetting an item
    for paid, items, what in [(5000, [2375, 1840], ("a puzzle", "a board game")),
                              (10000, [5650, 2995], ("a rain jacket", "a pair of rain boots")),
                              (50000, [32995, 8450], ("a guitar", "a guitar case")),
                              (100000, [64950, 18875], ("a desk", "a chair"))]:
        nm, he, his = P.next()
        q = "%s buys %s for %s and %s for %s. %s pays with %s. How much change does %s get?" % (
            nm, what[0], nat(items[0]), what[1], nat(items[1]), cap(he), paid_text(paid), he)
        its.append(change_item(q, sum(items), paid, False, items))
    # is the change right?
    nm, he, his = P.next()
    assert 10000 - 6385 == 3615
    its.append(mcq("%s buys a pair of running shoes for $63.85 with a $100 bill. The cashier gives %s $37.15 in change. Is that right?"
                   % (nm, obj(he)),
                   "No, it should be $36.15.", ["Yes, it is right.", "No, it should be $46.15.", "No, it should be $36.85."],
                   "Count up: $63.85 + 5¢ = $63.90, + 10¢ = $64, + $36 = $100. 5¢ + 10¢ + $36 = $36.15. "
                   "<b>No, it should be $36.15.</b> Check: $63.85 + $37.15 = $101, which is $1 too much.", fmt=str))
    nm, he, his = P.next()
    assert 50000 - 27860 == 22140
    its.append(mcq("%s’s dad buys a bike trailer for $278.60 with five $100 bills. He gets $221.40 in change. Is that right?" % nm,
                   "Yes, it is right.", ["No, it should be $222.40.", "No, it should be $321.40.", "No, it should be $231.40."],
                   "Check by adding: $278.60 + $221.40. Cents: 60¢ + 40¢ = $1. Dollars: $278 + $221 + $1 = $500. "
                   "Price + change = money paid, so <b>yes, it is right</b>.", fmt=str))
    # price from the change
    nm, he, his = P.next()
    it = mcq("%s pays with a $100 bill and gets $27.35 in change. What was the price?" % nm,
             7265, [2735, 7365, 12735, 7275],
             "Price = money paid − change. Count up from $27.35 to $100: 5¢ + 60¢ + $72 = $72.65. "
             "The price was <b>$72.65</b>. Check: $72.65 + $27.35 = $100.")
    note_if(it, 2735, "%s is the change, not the price.")
    note_if(it, 7365, "%s forgets that one dollar was used up to make the cents.")
    its.append(it)
    nm, he, his = P.next()
    it = mcq("%s’s family pays for a TV with eight $100 bills and gets $64.05 in change. What was the price of the TV?" % nm,
             73595, [6405, 74595, 86405, 73605],
             "Price = $800 − $64.05. Count up from $64.05 to $800: 95¢ + $5 + $30 + $700 = $735.95. "
             "The price was <b>$735.95</b>. Check: $735.95 + $64.05 = $800.")
    note_if(it, 74595, "%s forgets that one dollar was used up to make the cents.")
    note_if(it, 86405, "%s adds the change instead of subtracting it.")
    its.append(it)
    assert len(its) == 20
    return {"title": "Making change to $1000", "items": its}


# ============================================================ set 3: cash rounding (card is exact)
RULE = ("Canada has no pennies, so a cash total is rounded to the nearest 5¢. "
        "Last digit 1 or 2: round down to 0. 3 or 4: up to 5. 6 or 7: down to 5. 8 or 9: up to the next 10. ")


def set_rounding(P, rnd):
    its = []
    for amt in [4783, 12641, 30997, 2366, 59999, 81452]:
        R = round5(amt)
        assert R != amt
        other = R + 5 if R < amt else R - 5
        ten = (amt + 5) // 10 * 10
        q = "A total of %s is paid in cash. What is the cash total?" % nat(amt)
        e = RULE + "%s ends in %d, so it rounds %s to <b>%s</b>." % (nat(amt), amt % 10, "up" if R > amt else "down", nat(R))
        it = mcq(q, R, [ten, other, amt, (amt + 50) // 100 * 100, amt // 10 * 10], e)
        if ten != R:
            note_if(it, ten, "%s rounds to the nearest 10¢, but cash rounds to the nearest 5¢.")
        its.append(it)
    nm, he, his = P.next()
    its.append(mcq(fig(receipt_svg("Bookstore", [("novel", 1899), ("bookmark", 349)], dol(2248), "debit card"))
                   + "%s pays for this by debit card. How much does %s pay?" % (nm, he),
                   2248, [2250, 2245, 2240],
                   "Card payments are not rounded. Only cash is rounded to the nearest 5¢. %s pays exactly <b>$22.48</b>." % cap(he)))
    nm, he, his = P.next()
    its.append(mcq(fig(receipt_svg("Sports store", [("soccer ball", 2999), ("shin pads", 1734)], dol(4733), "cash"))
                   + "%s pays for this in cash. How much does %s pay?" % (nm, he),
                   4735, [4733, 4730, 4740],
                   RULE + "$47.33 ends in 3, so it rounds up to <b>$47.35</b>."))
    assert [round5(x) for x in (14608, 14613, 14606, 14604)] == [14610, 14615, 14605, 14605]
    its.append(mcq("Which total becomes $146.10 when it is paid in cash?", "$146.08", ["$146.13", "$146.06", "$146.04"],
                   "$146.08 ends in 8, so it rounds up to <b>$146.10</b>. $146.13 rounds up to $146.15. "
                   "$146.06 and $146.04 both round to $146.05.", fmt=str))
    assert [round5(x) for x in (23885, 23887, 23883, 23889)] == [23885, 23885, 23885, 23890]
    its.append(mcq("Which total stays the same when it is paid in cash?", "$238.85", ["$238.87", "$238.83", "$238.89"],
                   "A total that already ends in 0 or 5 does not change. <b>$238.85</b> ends in 5. "
                   "$238.87 and $238.83 become $238.85, and $238.89 becomes $238.90.", fmt=str))
    # round the total, not each price
    nm, he, his = P.next()
    a, b = 1248, 379
    assert a + b == 1627 and round5(1627) == 1625 and round5(a) + round5(b) == 1630
    it = mcq("%s buys a lunch kit for $12.48 and a water bottle for $3.79 and pays in cash. What is the cash total?" % nm,
             1625, [1630, 1627, 1620, 1725],
             "Add first: $12.48 + $3.79 = $16.27. Then round the total: $16.27 ends in 7, so it rounds down to <b>$16.25</b>.")
    note_if(it, 1630, "%s rounds each price first ($12.50 + $3.80). Round only the total.")
    its.append(it)
    nm, he, his = P.next()
    a, b, c = 2198, 868, 1435
    assert a + b + c == 4501 and round5(4501) == 4500 and round5(a) + round5(b) + round5(c) == 4505
    it = mcq("At a Kamloops market, %s pays cash for honey at $21.98, jam at $8.68 and bread at $14.35. What is the cash total?" % nm,
             4500, [4505, 4501, 3635, 4600],
             "Add first: $21.98 + $8.68 + $14.35 = $45.01. $45.01 ends in 1, so the cash total is <b>$45</b>.")
    note_if(it, 4505, "%s rounds each price first ($22 + $8.70 + $14.35). Round only the total.")
    note_if(it, 3635, "%s forgets the jam.")
    its.append(it)
    # change after rounding
    for paid, amt in [(2000, 1392), (5000, 3651), (10000, 7319), (20000, 15488), (50000, 32774), (100000, 61246)]:
        nm, he, his = P.next()
        R = round5(amt)
        assert R != amt
        other = R + 5 if R < amt else R - 5
        ch = paid - R
        q = "%s’s total is %s. %s pays cash with %s. How much change does %s get?" % (nm, nat(amt), cap(he), paid_text(paid), he)
        e = ("Round first: %s ends in %d, so the cash total is %s. " % (nat(amt), amt % 10, nat(R)) + count_up(R, paid)
             + " The change is <b>%s</b>." % nat(ch))
        it = mcq(q, ch, [paid - amt, paid - other, ch + 100 if R % 100 else None, ch + 10000 if paid >= 20000 else None, ch + 10], e)
        note_if(it, paid - amt, "%s forgets to round the total.")
        note_if(it, ch + 100, "%s forgets that one dollar was used up to make the cents.")
        its.append(it)
    nm, he, his = P.next()
    its.append(mcq("A total is $389.92. How much less does %s pay with cash than by card?" % nm,
                   "2¢", ["8¢", "3¢", "5¢"],
                   "By card: exactly $389.92. In cash: $389.92 ends in 2, so it rounds down to $389.90. "
                   "$389.92 − $389.90 = <b>2¢</b> less. 8¢ comes from rounding up to $390.", fmt=str))
    nm, he, his = P.next()
    its.append(mcq("A total is $56.43. How much more does %s pay with cash than by card?" % nm,
                   "2¢", ["3¢", "7¢", "5¢"],
                   "By card: exactly $56.43. In cash: $56.43 ends in 3, so it rounds up to $56.45. "
                   "$56.45 − $56.43 = <b>2¢</b> more. 3¢ comes from rounding down to $56.40.", fmt=str))
    assert len(its) == 20
    return {"title": "Cash rounding to the nearest 5¢", "items": its}


# ============================================================ set 4: saving plans
def weeks_item(q, need, per, e_lead, wrong, notes=()):
    """need, per in cents; answer = weeks rounded up"""
    n = ceil_div(need, per)
    exact = need % per == 0
    if exact:
        e = e_lead + "%s ÷ %s = <b>%s</b>. Check: %d × %s = %s." % (nat(need), nat(per), wk(n), n, nat(per), nat(n * per))
    else:
        e = (e_lead + "%s ÷ %s is between %d and %d. After %d weeks: %d × %s = %s, not enough. "
             "After %d weeks: %d × %s = %s. So it takes <b>%s</b>. Always round the weeks up."
             % (nat(need), nat(per), n - 1, n, n - 1, n - 1, nat(per), nat((n - 1) * per), n, n, nat(per), nat(n * per), wk(n)))
    it = mcq(q, wk(n), [wk(w) for w in wrong if w != n], e, fmt=str)
    for w, m in notes:
        note_if(it, wk(w), m)
    return it


def set_saving(P, rnd):
    its = []
    nm, he, his = P.next()
    its.append(weeks_item("%s wants a $60 soccer ball. %s saves $5 each week. How many weeks will it take?" % (nm, cap(he)),
                          6000, 500, "", [55, 11, 65], [(55, "%s comes from $60 − $5.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s saves $8 each week for a $96 pair of rollerblades. How many weeks will it take?" % nm,
                          9600, 800, "", [88, 11, 13], [(88, "%s comes from $96 − $8.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s wants a $75 lacrosse stick. %s saves $6 each week. How many weeks until %s has enough?" % (nm, cap(he), he),
                          7500, 600, "", [12, 69, 11], [(12, "%s leaves " + nm + " $3 short.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s saves $15 each week for a $200 fishing rod. How many weeks until %s has enough?" % (nm, he),
                          20000, 1500, "", [13, 185, 15], [(13, "%s gives only $195, which is $5 short.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s has $40. %s wants a $160 skateboard and saves $12 each week. How many more weeks until %s can buy it?"
                          % (nm, cap(he), he), 12000, 1200,
                          "%s needs $160 − $40 = $120 more. " % cap(he), [14, 9, 17],
                          [(14, "%s forgets the $40 " + he + " already has.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s has $25 saved. A bike light and bell cost $130. %s saves $15 each week. "
                          "How many more weeks until %s has enough?" % (nm, cap(he), he), 10500, 1500,
                          "%s needs $130 − $25 = $105 more. " % cap(he), [9, 6, 11],
                          [(9, "%s forgets the $25 " + he + " already has.")]))
    # saved after n weeks
    nm, he, his = P.next()
    it = mcq("%s has $35 in the bank. %s adds $12 each week. How much will %s have after 8 weeks?" % (nm, cap(he), he),
             3500 + 8 * 1200, [8 * 1200, 3500 + 9 * 1200, 3500 + 7 * 1200, 3500 + 1200 + 800],
             "8 × $12 = $96. $35 + $96 = <b>$131</b>.")
    note_if(it, 9600, "%s forgets the $35 at the start.")
    its.append(it)
    nm, he, his = P.next()
    it = mcq("%s wants a $96 pair of binoculars for bird watching in 8 weeks. How much must %s save each week?" % (nm, he),
             1200, [8800, 10400, 76800],
             "$96 ÷ 8 = <b>$12</b> a week. Check: 8 × $12 = $96.")
    note_if(it, 8800, "%s subtracts instead of dividing.")
    note_if(it, 76800, "%s multiplies instead of dividing.")
    its.append(it)
    # savings table
    start, per = 5000, 1800
    it = mcq(fig(savings_svg(start, per, 3)) + "This is %s’s savings plan. If the pattern continues, how much will be saved after week 6?"
             % P.next()[0], start + 6 * per, [6 * per, start + 5 * per, start + 7 * per],
             "The savings go up by $18 each week. Week 6: $50 + 6 × $18 = $50 + $108 = <b>$158</b>.")
    note_if(it, 6 * per, "%s forgets the $50 at week 0.")
    its.append(it)
    nm, he, his = P.next()
    its.append(weeks_item("%s earns $20 each week babysitting. %s saves half of it for a $150 tablet case and headphones. "
                          "How many weeks will it take?" % (nm, cap(he)), 15000, 1000,
                          "Half of $20 is $10 a week. ", [8, 14, 16], [(8, "%s uses all $20 a week, not half.")]))
    start, per = 3000, 1600
    assert ceil_div(20000 - start, per) == 11
    nm = P.next()[0]
    its.append(mcq(fig(savings_svg(start, per, 4)) + "This is %s’s savings plan. In which week will the savings first reach $200?" % nm,
                   "week 11", ["week 10", "week 13", "week 12"],
                   "The plan starts at $30 and grows by $16 a week. $200 − $30 = $170 to go. $170 ÷ $16 is between 10 and 11. "
                   "Week 10: $30 + $160 = $190, not enough. Week 11: $30 + $176 = $206. So it is <b>week 11</b>. "
                   "Week 13 forgets the $30 at the start.", fmt=str))
    nm, he, his = P.next()
    nm2 = "Wei" if nm != "Wei" else "Kai"
    its.append(weeks_item("%s saves $9 each week and %s saves $6 each week. Together they want a $180 gift for their grandparents. "
                          "How many weeks will it take?" % (nm, nm2), 18000, 1500,
                          "Together they save $9 + $6 = $15 each week. ", [20, 30, 13],
                          [(20, "%s uses only $9 a week.")]))
    nm, he, his = P.next()
    it = mcq("%s saves $25 every 2 weeks for a $300 bike. How many weeks will it take?" % nm,
             wk(24), [wk(12), wk(6), wk(26)],
             "$300 ÷ $25 = 12 savings. One saving every 2 weeks: 12 × 2 = <b>24 weeks</b>.", fmt=str)
    note_if(it, wk(12), "%s counts the savings, not the weeks.")
    its.append(it)
    nm, he, his = P.next()
    its.append(weeks_item("%s saves $7.50 each week for a $90 pair of hiking boots. How many weeks will it take?" % nm,
                          9000, 750, "", [13, 11, 83], [(13, "%s ignores the 50¢: $90 ÷ $7 is about 13.")]))
    nm, he, his = P.next()
    its.append(weeks_item("%s earns $15 each week. %s spends $4 on snacks and saves the rest. "
                          "How many weeks until %s has $165?" % (nm, cap(he), he), 16500, 1100,
                          "%s saves $15 − $4 = $11 each week. " % cap(he), [11, 42, 16],
                          [(11, "%s forgets the $4 spent on snacks.")]))
    nm, he, his = P.next()
    it = mcq("%s has $36 and wants $180 for a summer camp in 12 weeks. How much must %s save each week?" % (nm, he),
             1200, [1500, 1800, 14400],
             "%s needs $180 − $36 = $144 more. $144 ÷ 12 = <b>$12</b> a week. Check: $36 + 12 × $12 = $180." % cap(he))
    note_if(it, 1500, "%s forgets the $36 " + he + " already has.")
    note_if(it, 14400, "%s is the money still needed, not the amount each week.")
    its.append(it)
    nm, he, his = P.next()
    assert ceil_div(25000 - 1800, 1400) == 17 and ceil_div(25000, 1400) == 18 and ceil_div(25000 + 1800, 1400) == 20
    its.append(weeks_item("%s has $18. %s saves $14 each week for a $250 snowboard. How many more weeks until %s has enough?"
                          % (nm, cap(he), he), 23200, 1400,
                          "%s needs $250 − $18 = $232 more. " % cap(he), [16, 18, 20],
                          [(18, "%s forgets the $18 " + he + " already has.")]))
    assert 12 * 800 == 9600 and 2 * 4500 == 9000
    its.append(mcq("Plan A: save $12 a week for 8 weeks. Plan B: save $45 a month for 2 months. Which plan saves more, and by how much?",
                   "Plan A, by $6", ["Plan B, by $6", "Plan B, by $33", "They save the same."],
                   "Plan A: 8 × $12 = $96. Plan B: 2 × $45 = $90. $96 − $90 = $6, so <b>Plan A saves $6 more</b>. "
                   "Plan B by $33 compares $45 with $12 and forgets to multiply.", fmt=str))
    nm, he, his = P.next()
    assert 12000 + 16 * 1500 == 36000
    its.append(mcq("%s wants a $400 bike by the summer holidays, 16 weeks away. %s has $120 and saves $15 each week. Will the plan work?"
                   % (nm, cap(he)),
                   "No, it is $40 short.", ["Yes, with $40 left over.", "No, it is $160 short.", "Yes, exactly."],
                   "After 16 weeks: 16 × $15 = $240. $120 + $240 = $360. $400 − $360 = $40, so <b>no, it is $40 short</b>. "
                   "$160 short forgets the $120 " + he + " already has.", fmt=str))
    nm, he, his = P.next()
    assert (24000 - 6000) // 1500 == 12 and 24000 // 2400 == 10 and 24000 // 1500 == 16
    its.append(mcq("%s needs $240. Plan A: start with $60 and save $15 a week. Plan B: start with $0 and save $24 a week. "
                   "Which plan reaches $240 first?" % nm,
                   "Plan B, in 10 weeks", ["Plan A, in 12 weeks", "Plan A, in 16 weeks", "They take the same time."],
                   "Plan A: $240 − $60 = $180, and $180 ÷ $15 = 12 weeks. Plan B: $240 ÷ $24 = 10 weeks. "
                   "<b>Plan B reaches $240 first, in 10 weeks.</b> Plan A in 16 weeks forgets the $60 start.", fmt=str))
    assert len(its) == 20
    return {"title": "Saving plans: how many weeks?", "items": its}


# ============================================================ set 5: simple financial plans and word problems
def budget_item(nm, month, bi, bo, save_label="Savings"):
    tin = sum(v for a, v in bi)
    tout = sum(v for a, v in bo)
    left = tin - tout
    assert left > 0
    sv = [v for a, v in bo if a == save_label][0]
    small = min(v for a, v in bo)
    e = ("Money in: %s = %s. Money out: %s = %s. %s − %s = <b>%s</b>."
         % (" + ".join(nat(v) for a, v in bi), nat(tin), " + ".join(nat(v) for a, v in bo), nat(tout), nat(tin), nat(tout), nat(left)))
    it = mcq(fig(budget_svg("%s’s plan for %s" % (nm, month), bi, bo)) + "How much of %s’s money is not planned for yet?" % nm,
             left, [left + sv, left + small, tout, tin], e)
    note_if(it, left + sv, "%s forgets that savings is planned money too.")
    note_if(it, tout, "%s is the money out.")
    sl = [a for a, v in bo if v == small][0]
    note_if(it, left + small, "%%s forgets the %s." % sl.lower())
    return it


def set_plans(P, rnd):
    its = []
    nm, he, his = P.next()
    its.append(budget_item(nm, "September", [("Allowance", 4000), ("Dog walking", 2500)],
                           [("Snacks", 1200), ("Swimming", 1800), ("Savings", 2000)]))
    nm, he, his = P.next()
    bi, bo = [("Allowance", 3000), ("Raking leaves", 1500)], [("Hockey tape", 900), ("Movie", 1400), ("Savings", 2200)]
    assert sum(v for a, v in bi) == sum(v for a, v in bo) == 4500
    its.append(mcq(fig(budget_svg("%s’s plan for October" % nm, bi, bo)) + "Is %s’s plan balanced?" % nm,
                   "Yes, money in equals money out.", ["No, %s has $22 left over." % he, "No, %s plans $9 too much." % he,
                                                        "No, savings is not money out."],
                   "Money in: $30 + $15 = $45. Money out: $9 + $14 + $22 = $45. They are equal, so <b>the plan is balanced</b>. "
                   "Savings counts as planned money.", fmt=str))
    nm, he, his = P.next()
    bi, bo = [("Allowance", 2500)], [("Art class", 1200), ("Snacks", 800), ("Savings", 1000)]
    assert sum(v for a, v in bo) - 2500 == 500
    its.append(mcq(fig(budget_svg("%s’s plan for November" % nm, bi, bo)) + "What is wrong with %s’s plan?" % nm,
                   "%s plans $5 more than %s has." % (cap(he), he),
                   ["Nothing, it is balanced.", "%s has $5 left over." % cap(he), "%s plans $30 more than %s has." % (cap(he), he)],
                   "Money out: $12 + $8 + $10 = $30. Money in: $25. $30 − $25 = $5, so <b>%s plans $5 more than %s has</b>. "
                   "%s could save $5 instead of $10." % (he, he, cap(he)), fmt=str))
    its.append(mcq("A family makes a plan for the month. Which of these is a need?",
                   "rent for their home", ["a new video game", "concert tickets", "a second bike"],
                   "A need is something a family must have to live safely: a home, food, warm clothes. "
                   "<b>Rent for their home</b> is a need. The others are wants.", fmt=str))
    nm, he, his = P.next()
    it = mcq("%s splits $84 equally into three jars: save, spend and share. How much goes into each jar?" % nm,
             2800, [4200, 25200, 8100],
             "$84 ÷ 3 = <b>$28</b>. Check: $28 + $28 + $28 = $84.")
    note_if(it, 4200, "%s splits into 2 jars, not 3.")
    note_if(it, 25200, "%s multiplies instead of dividing.")
    its.append(it)
    it = mcq("For the Terry Fox Run, a class wants to raise $750. So far it has raised $468.35. How much more does it need?",
             28165, [38165, 28265, 121835, 46835],
             "Count up: $468.35 + 5¢ = $468.40, + 60¢ = $469, + $1 = $470, + $30 = $500, + $250 = $750. "
             "5¢ + 60¢ + $1 + $30 + $250 = <b>$281.65</b>. Check: $468.35 + $281.65 = $750.")
    note_if(it, 38165, "%s forgets that $100 was used up when regrouping.")
    note_if(it, 121835, "%s adds instead of subtracting.")
    its.append(it)
    nm, he, his = P.next()
    assert 64 * 125 == 8000 and 8000 - 2250 == 5750
    it = mcq("At a school bake sale, %s’s class sells 64 cookies at $1.25 each. The ingredients cost $22.50. "
             "How much money does the class make after paying for the ingredients?" % nm,
             5750, [8000, 10250, 5850],
             "Sales: 64 × $1.25. 64 × $1 = $64 and 64 × 25¢ = 1600¢ = $16, so $80. "
             "After costs: $80 − $22.50 = <b>$57.50</b>.")
    note_if(it, 8000, "%s forgets the cost of the ingredients.")
    note_if(it, 10250, "%s adds the costs instead of subtracting.")
    its.append(it)
    nm, he, his = P.next()
    assert 12 * 4 * 6 == 288
    it = mcq("%s earns $12 for each lawn %s mows. %s mows 4 lawns a week for 6 weeks. How much does %s earn?" % (nm, he, cap(he), he),
             28800, [4800, 2200, 7200],
             "Lawns: 4 × 6 = 24. Money: 24 × $12 = <b>$288</b>. (Or $48 a week × 6 weeks = $288.)")
    note_if(it, 4800, "%s is only one week.")
    note_if(it, 2200, "%s adds the numbers instead of multiplying.")
    note_if(it, 7200, "%s counts only one lawn a week.")
    its.append(it)
    it = mcq("A guitar costs $480. It is paid in 6 equal monthly payments. How much is each payment?",
             8000, [47400, 800, 288000],
             "$480 ÷ 6 = <b>$80</b>. Check: 6 × $80 = $480.")
    note_if(it, 47400, "%s subtracts instead of dividing.")
    note_if(it, 800, "%s has the wrong place value: 6 × $8 is only $48.")
    its.append(it)
    nm, he, his = P.next()
    it = mcq("%s’s family buys a $420 bike. They pay $60 now and the rest in 6 equal payments. How much is each payment?" % nm,
             6000, [7000, 36000, 7200],
             "The rest: $420 − $60 = $360. $360 ÷ 6 = <b>$60</b>. Check: $60 + 6 × $60 = $420.")
    note_if(it, 7000, "%s forgets the $60 paid now.")
    note_if(it, 36000, "%s is the rest, not one payment.")
    its.append(it)
    nm, he, his = P.next()
    items = [("sleeping bag", 6495), ("headlamp", 2450), ("water filter", 4299), ("camp stove", 5975)]
    pr = dict(items)
    ok = pr["sleeping bag"] + pr["headlamp"]
    bad = [pr["sleeping bag"] + pr["water filter"], pr["water filter"] + pr["camp stove"], pr["sleeping bag"] + pr["camp stove"]]
    assert ok == 8945 and ok <= 10000 and all(b > 10000 for b in bad)
    its.append(mcq(fig(price_svg(items, "outdoor store")) + "%s has $100 for a hiking trip. Which 2 items can %s buy?" % (nm, he),
                   "sleeping bag and headlamp", ["sleeping bag and water filter", "water filter and camp stove", "sleeping bag and camp stove"],
                   "Sleeping bag and headlamp: $64.95 + $24.50 = <b>$89.45</b>, less than $100. "
                   "Sleeping bag and water filter: $107.94. Water filter and camp stove: $102.74. Sleeping bag and camp stove: $124.70.",
                   fmt=str))
    nm, he, his = P.next()
    assert 4 * 3850 + 600 == 16000 and 4 * 4100 == 16400
    its.append(mcq("%s’s family of 4 wants concert tickets. Online: $38.50 each plus a $6 fee for the order. "
                   "At the door: $41 each. Which is cheaper, and by how much?" % nm,
                   "online, by $4", ["at the door, by $4", "online, by $10", "They cost the same."],
                   "Online: 4 × $38.50 = $154, + $6 = $160. At the door: 4 × $41 = $164. $164 − $160 = $4, "
                   "so <b>online is cheaper by $4</b>.", fmt=str))
    nm, he, his = P.next()
    assert 4 * 3500 + 2 * 1500 + 1000 == 18000 and 18000 > 15000
    it = mcq("%s plans a snowboard day. The lift ticket is $79, the rental is $48.50, lunch is $16.75 and the bus is $12. "
             "%s has $150. Is that enough?" % (nm, cap(he)),
             "No, %s needs $6.25 more." % he,
             ["Yes, with $6.25 left.", "Yes, with $5.75 left.", "No, %s needs $7.25 more." % he],
             "Total: $79 + $48.50 + $16.75 + $12 = $156.25. $156.25 is more than $150. "
             "$156.25 − $150 = $6.25, so <b>no, %s needs $6.25 more</b>. With $5.75 left forgets the bus." % he, fmt=str)
    assert 15000 - (7900 + 4850 + 1675) == 575
    its.append(it)
    nm, he, his = P.next()
    assert 6000 - (1425 + 1850 + 1295) == 1430
    it = mcq("%s plans to spend $60 on 4 gifts. The first three cost $14.25, $18.50 and $12.95. How much can the last gift cost?" % nm,
             1430, [1530, 2725, 4570, 2860],
             "Spent: $14.25 + $18.50 + $12.95 = $45.70. Left: count up from $45.70: 30¢ + $14 = <b>$14.30</b>.")
    note_if(it, 1530, "%s forgets that one dollar was used up to make the cents.")
    note_if(it, 2725, "%s forgets one of the gifts.")
    note_if(it, 4570, "%s is what was spent.")
    its.append(it)
    nm, he, his = P.next()
    tot = 24500 + 31250 + 19875
    assert tot == 75625 and 80000 - tot == 4375
    it = mcq("A class holds three car washes to raise $800. They raise $245, $312.50 and $198.75. How much more do they need?",
             4375, [5375, 24375, 75625, 23750],
             "Raised: $245 + $312.50 + $198.75 = $756.25. Count up from $756.25 to $800: 75¢ + $3 + $40 = <b>$43.75</b>.")
    note_if(it, 5375, "%s forgets that one dollar was used up to make the cents.")
    note_if(it, 24375, "%s forgets one of the car washes.")
    note_if(it, 75625, "%s is the money raised.")
    its.append(it)
    tot = 28 * 1250 + 4 * 1500 + 26000
    assert tot == 67000
    it = mcq("A Grade 5 class plans a field trip. 28 students pay $12.50 each, 4 adults pay $15 each, and the bus costs $260. "
             "The budget is $700. How much money is left?",
             3000, [9000, 29000, 67000],
             "Students: 28 × $12.50 = $350. Adults: 4 × $15 = $60. Total: $350 + $60 + $260 = $670. "
             "$700 − $670 = <b>$30</b>.")
    note_if(it, 9000, "%s forgets the adults.")
    note_if(it, 29000, "%s forgets the bus.")
    note_if(it, 67000, "%s is the cost of the trip.")
    its.append(it)
    tot = 21245 + 19880 + 23165
    assert tot == 64290 and 85000 - tot == 20710
    it = mcq("A family plans to spend $850 on groceries this month. In the first three weeks they spend $212.45, $198.80 "
             "and $231.65. How much is left for week 4?",
             20710, [21710, 41875, 64290, 22710],
             "Spent: $212.45 + $198.80 + $231.65 = $642.90. Count up from $642.90 to $850: 10¢ + $7 + $200 = <b>$207.10</b>.")
    note_if(it, 21710, "%s forgets that one dollar was used up to make the cents.")
    note_if(it, 41875, "%s forgets one of the weeks.")
    note_if(it, 64290, "%s is what was spent.")
    its.append(it)
    nm, he, his = P.next()
    assert 4500 + 2500 == 9000 - 2000 and 9000 // 450 == 20 and ceil_div(6500, 450) == 15
    its.append(mcq("%s sells bracelets for $4.50 each at a craft fair in Nanaimo. The table costs $25. "
                   "How many bracelets must %s sell to make $65 after paying for the table?" % (nm, he),
                   "20 bracelets", ["15 bracelets", "9 bracelets", "21 bracelets"],
                   "%s needs $65 + $25 = $90 in sales. $90 ÷ $4.50 = <b>20 bracelets</b>. Check: 20 × $4.50 = $90. "
                   "15 bracelets forgets the table: it makes only $67.50 − $25 = $42.50." % cap(he), fmt=str))
    it = mcq("A school sells 120 chocolate bars at $3 each. Each bar costs the school $1.50. How much money does the school make?",
             18000, [36000, 54000, 35850],
             "Sales: 120 × $3 = $360. Cost: 120 × $1.50 = $180. $360 − $180 = <b>$180</b>.")
    note_if(it, 36000, "%s forgets the cost of the bars.")
    note_if(it, 35850, "%s takes away $1.50 only once.")
    its.append(it)
    assert (96000 - 38400) // 4 == 14400
    it = mcq("A Grade 5 class needs $960 for a trip to Victoria on BC Ferries. They have $384. They plan 4 more fundraisers that "
             "each raise the same amount. How much must each fundraiser raise?",
             14400, [24000, 57600, 33600],
             "Still needed: $960 − $384 = $576. $576 ÷ 4 = <b>$144</b>. Check: $384 + 4 × $144 = $960.")
    note_if(it, 24000, "%s forgets the $384 they already have.")
    note_if(it, 57600, "%s is the total still needed, not each fundraiser.")
    note_if(it, 33600, "%s adds the $384 instead of subtracting it.")
    its.append(it)
    assert len(its) == 20
    return {"title": "Simple financial plans and word problems", "items": its}


# ============================================================ lesson
def body_html():
    return (
        "<h2>Total cost of several items</h2>"
        "<p>Add the dollars, then add the cents. 100¢ makes $1, so carry it to the dollars. "
        "Estimate first so you can check your answer. Tick off each item so none is forgotten.</p>"
        "<figure class='sn-fig'>" + receipt_svg("Sports store", [("skates", 18999), ("stick", 7450), ("tape", 675)], dol(27124)) +
        "<figcaption>Dollars: $189 + $74 + $6 = $269. Cents: 99¢ + 50¢ + 75¢ = 224¢ = $2.24. Total: $271.24.</figcaption></figure>"
        + ex("Example", "4 movie tickets cost $8.75 each. What is the total?",
             "4 × $8 = $32. 4 × 75¢ = 300¢ = $3. $32 + $3 = $35.", "$35") +
        "<h2>Make change by counting up</h2>"
        "<p>Start at the price. Count up to the next 10¢, the next dollar, the next $10 or $100, then to the money paid. "
        "Add the jumps. Check: price + change = money paid.</p>"
        "<figure class='sn-fig'>" + change_line(83740, 100000) +
        "<figcaption>Change from $1000 for $837.40: 60¢ + $2 + $60 + $100 = $162.60.</figcaption></figure>"
        + ex("Example", "A bike costs $412.70. Pay with five $100 bills. What is the change?",
             "$412.70 + 30¢ = $413. $413 + $7 = $420. $420 + $80 = $500. 30¢ + $7 + $80 = $87.30. "
             "Check: $412.70 + $87.30 = $500.", "$87.30")
        + "<h2>Cash rounding</h2>"
        "<p>Canada has no pennies, so a <b>cash</b> total is rounded to the nearest 5¢. "
        "A <b>card</b> payment (debit or credit) is the exact amount. Round only the total, not each price.</p>"
        + table(["Total ends in", "Cash rounding", "Example"], [
            ["1 or 2", "down to 0", "$43.42 → $43.40"],
            ["3 or 4", "up to 5", "$43.43 → $43.45"],
            ["6 or 7", "down to 5", "$43.47 → $43.45"],
            ["8 or 9", "up to the next 10", "$43.48 → $43.50"],
            ["0 or 5", "no change", "$43.45 stays $43.45"],
        ]) +
        "<h2>Saving plans</h2>"
        "<p>Find how much more you need. Divide by the amount you save each week. "
        "If it does not divide evenly, round the weeks <b>up</b>: one more week is needed to reach the goal.</p>"
        "<figure class='sn-fig'>" + savings_svg(4000, 1200, 4) +
        "<figcaption>Start with $40 and save $12 a week. A $160 skateboard needs $120 more: $120 ÷ $12 = 10 weeks.</figcaption></figure>"
        + ex("Example", "Save $15 a week for a $200 fishing rod. How many weeks?",
             "$200 ÷ $15 is between 13 and 14. 13 weeks: $195, not enough. 14 weeks: $210.", "14 weeks") +
        "<h2>Simple financial plans</h2>"
        "<p>A plan (budget) lists money in and money out. Savings count as money out because they are planned. "
        "When money in equals money out, the plan is balanced. If money out is bigger, spend less on a want.</p>"
        "<figure class='sn-fig'>" + budget_svg("Plan for September", [("Allowance", 4000), ("Dog walking", 2500)],
                                               [("Snacks", 1200), ("Swimming", 1800), ("Savings", 2000)]) +
        "<figcaption>Money in: $65. Money out: $50. $15 is not planned for yet.</figcaption></figure>"
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["Forgetting an item", "Tick off each item as you add it. Estimate to check"],
            ["$4.75 + $2.60 + $1.80 = $8.15", "75¢ + 60¢ + 80¢ = 215¢ = $2.15, so the total is $9.15"],
            ["$10 − $7.65 = $3.35", "Count up: 5¢ + 30¢ + $2 = $2.35. One dollar was used to make the cents"],
            ["Rounding each price before paying cash", "Add first, then round only the total"],
            ["$75 ÷ $6 = 12.5, so 12 weeks", "Round the weeks up: 13 weeks. After 12 weeks you have only $72"],
            ["Forgetting money already saved", "Take the money you have away from the goal first"],
        ])
    )


FAQ = [
    {"q": "What do Grade 5 students learn about money in BC?",
     "a": "The BC Grade 5 math curriculum includes financial literacy: monetary calculations, including making change with amounts to $1000, and developing simple financial plans. Students add prices, make change, round cash totals, plan how to save and make simple budgets."},
    {"q": "How do you make change from $1000?",
     "a": "Count up from the price: for $837.40, go to $838 (60¢), to $840 ($2), to $900 ($60), then to $1000 ($100). The change is $162.60; check that price + change = $1000."},
    {"q": "How does cash rounding work in Canada?",
     "a": "Canada no longer uses pennies, so cash totals are rounded to the nearest 5¢: amounts ending in 1 or 2 round down, 3 or 4 round up to 5, 6 or 7 round down to 5, and 8 or 9 round up. Debit and credit card payments are charged the exact amount."},
    {"q": "How do you teach a Grade 5 student to make a savings plan?",
     "a": "Start with the goal, take away the money already saved, then divide by the amount saved each week and round up to a whole week. A simple table of weeks and totals helps students see when they will reach the goal."},
]


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


def gen():
    rnd = random.Random(55817)
    P = People(rnd)
    sets = [set_total(P, rnd), set_change(P, rnd), set_rounding(P, rnd), set_saving(P, rnd), set_plans(P, rnd)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vals = [mval(c) for c in it["c"]]
            vv = [v for v in vals if v is not None]
            assert len(set(vv)) == len(vv), it["c"]
            for c in it["c"] + [it["q"], it["e"]]:
                assert not re.search(r"\$\d+\.\d(?!\d)", re.sub(r"<[^>]+>", "", c)), c
            assert it["q"].count("<svg") <= 1
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
    u = {
        "country": "ca-bc", "subject": "math", "grade": "grade-5", "slug": "money-and-financial-plans", "sort": 17,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 5 Money and Financial Plans",
        "seo_title": "Grade 5 Money and Financial Plans Worksheets: Free Math Practice with Answer Key (BC Curriculum)",
        "short_title": "Money and financial plans",
        "domain": "Financial literacy",
        "standard_code": "Grade 5: Financial literacy",
        "standard_url": "https://curriculum.gov.bc.ca/curriculum/mathematics/5/core",
        "standard_text": "Financial literacy – monetary calculations, including making change with amounts to 1000 dollars and developing simple financial plans",
        "meta_desc": "Free Grade 5 math worksheets on money for the BC curriculum: find the total cost of several items, make change from up to $1000 by counting up, round cash totals to the nearest 5¢, plan how many weeks to save, and read simple budgets. 100 questions with an answer key.",
        "key_big": "To make change, count up from the price to the money paid: $837.40 → $838 → $840 → $900 → $1000 is 60¢ + $2 + $60 + $100 = $162.60.",
        "key_sub": "Add every item, and carry 100¢ as $1. Cash totals round to the nearest 5¢; card payments are exact. In a saving plan, take away what you have, divide, and round the weeks up.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    return mark_large(u, "(counting|price|receipt|budget|savings)")


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
