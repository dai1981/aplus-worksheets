# -*- coding: utf-8 -*-
"""
US Grade 6 Math: Unit Rates (6.RP.A.2, with unit pricing and constant speed from 6.RP.A.3b)
  python3 tools/gen_us_math_g6_unit_rates.py
Every answer is computed with fractions.Fraction (never float) and checked in code.
Wrong choices come from real mistakes: dividing the wrong way, multiplying instead of dividing,
adding or subtracting, the wrong unit label, comparing total prices instead of unit prices.
HTML attributes use single quotes (no backslashes in the JSON).
Grade 6 style: numbers 1,000 and above are written with commas.
"""
import json, os, random, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "us", "math", "grade-6")
UPDATED = "2026-11-02"
GREEN = "#006633"
FILL = "#cfe6d6"
INK = "#2b2b2b"
THIN = "#8a8a8a"
RED = "#c0392b"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Maya", "Ava", "Mia", "Zoe", "Lily", "Emma", "Nora", "Ruby", "Sofia", "Grace"]
BOYS = ["Leo", "Noah", "Eli", "Sam", "Ben", "Omar", "Kai", "Jack", "Luis", "Owen"]


# ------------------------------------------------------------ numbers
def f(n):
    return "{:,}".format(n)


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def terminates(x):
    d = Fr(x).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dec(x):
    """Exact decimal text with commas: Fr(7, 2) -> '3.5'."""
    x = Fr(x)
    assert terminates(x), x
    k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1
    n = int(x * 10 ** k)
    w, r = divmod(n, 10 ** k)
    return f(w) + ("." + str(r).rjust(k, "0") if k else "")


def frac(x):
    """Fraction or mixed number: Fr(3, 4) -> 3/4, Fr(9, 4) -> 2 1/4."""
    x = Fr(x)
    w, r = divmod(x.numerator, x.denominator)
    if r == 0:
        return f(w)
    if w == 0:
        return fr(r, x.denominator)
    return "%s %s" % (f(w), fr(r, x.denominator))


def show(x, fmt="f"):
    return dec(x) if fmt == "d" else frac(x)


def M(x):
    """Money: $3.75, $1,250.00."""
    x = Fr(x)
    c = x * 100
    assert c.denominator == 1, x
    c = int(c)
    return "$%s.%02d" % (f(c // 100), c % 100)


def qty(x, u, fmt="f"):
    """u = (one, many). Singular for amounts up to 1: 3/4 cup, 1 cup, 1 1/2 cups."""
    x = Fr(x)
    return "%s %s" % (show(x, fmt), u[0] if x <= 1 else u[1])


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e):
    """4 choices: correct + the first 3 distractors that differ from it (and from each other).
    Each choice may be text or (text, key); the key compares values, so two equal amounts are never both shown."""
    def tk(c):
        return c if isinstance(c, tuple) else (c, plain(c))
    ct, ck = tk(correct)
    seen_t, seen_k = {plain(ct)}, {ck}
    pick = []
    for c in cands:
        if c is None:
            continue
        t, k = tk(c)
        if plain(t) in seen_t or k in seen_k or not t:
            continue
        seen_t.add(plain(t))
        seen_k.add(k)
        pick.append(t)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q, ct, cands)
    return {"q": q, "c": [ct] + pick, "a": 0, "e": e}


def balance(sets, rnd):
    """Spread the correct answers evenly over the 4 positions in every set (5 each)."""
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


def cap(s):
    return s[0].upper() + s[1:]


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def svg_wrap(w, h, body, label):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d %d' width='%d' height='%d' "
            "role='img' aria-label='%s'><g font-family='%s'>%s</g></svg>" % (w, h, w, h, label, FONT, body))


def tw(t, fs):
    """Approximate width of bold Arial text in px."""
    t = str(t)
    return (len(t) - t.count(",") * 0.6 - t.count(".") * 0.6) * fs * 0.6


def text(x, y, t, fs=16, anchor="middle", col=INK):
    return ("<text x='%.1f' y='%.1f' font-size='%d' font-weight='700' fill='%s' text-anchor='%s'>%s</text>"
            % (x, y, fs, col, anchor, t))


def line(x1, y1, x2, y2, col=INK, w=2):
    return "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%s'/>" % (x1, y1, x2, y2, col, w)


def table(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return "<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, b)


def ex(title, q, s, a):
    return ("<div class='sn-ex'><span class='sn-ex-t'>%s</span><p class='sn-ex-q'>%s</p>"
            "<p class='sn-ex-s'>%s</p><p class='sn-ex-a'>Answer: %s</p></div>" % (title, q, s, a))


# ------------------------------------------------------------ figures
def dnl_svg(a, ta, b, tb, full=False, money=False):
    """Double number line: top line ta (0 … a), bottom line tb (0 … b), one tick per unit of b.
    full=False: only 0, the end values and a red ? above 1 are written."""
    fs = 16
    sp = 64 if b <= 4 else 56
    lab_w = max(tw(ta, fs), tw(tb, fs))
    L = 10 + lab_w + 16
    R = L + sp * b
    yt, yb = 36, 78
    s = ["<rect x='%.1f' y='%d' width='22' height='%d' rx='5' fill='%s'/>" % (L + sp - 11, yt - 10, yb - yt + 20, FILL)]
    s.append(text(L - 14, yt + 6, ta, fs, "end"))
    s.append(text(L - 14, yb + 6, tb, fs, "end"))
    s.append(line(L, yt, R + 14, yt, INK, 2.5))
    s.append(line(L, yb, R + 14, yb, INK, 2.5))
    last_w = 0
    for i in range(b + 1):
        x = L + i * sp
        hi = (i == 1)
        s.append(line(x, yt - 7, x, yt + 7, INK, 2))
        s.append(line(x, yb - 7, x, yb + 7, INK, 2))
        v = Fr(a) * i / b
        if full or i in (0, b):
            t = (M(v) if money and v else dec(v) if terminates(v) else frac(v))
            s.append(text(x, yt - 14, t, fs, col=GREEN if (hi and full) else INK))
            if i == b:
                last_w = tw(t, fs)
        elif hi:
            s.append(text(x, yt - 14, "?", fs + 2, col=RED))
        s.append(text(x, yb + 28, str(i), fs, col=GREEN if hi else INK))
    W = max(R + 14, L + sp * b + last_w / 2) + 8
    H = yb + 36
    lab = "double number line: %s %s for %d %s" % (dec(a) if terminates(Fr(a)) else plain(frac(a)), ta, b, tb)
    return svg_wrap(int(W + 0.99), H, "".join(s), lab)


def tape_svg(total, n, unit, full=False, cw=58):
    """Tape diagram: total split into n equal parts, a red ? in the first part (or every part's value)."""
    fs = 16
    L, T, bh = 10, 8, 36
    each = Fr(total) / n
    s = []
    for i in range(n):
        x = L + i * cw
        s.append("<rect x='%d' y='%d' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2.5'/>"
                 % (x, T, cw, bh, FILL if (i == 0 or full) else "#ffffff", GREEN))
        if full:
            s.append(text(x + cw / 2.0, T + bh / 2 + 6, M(each), 14))
        elif i == 0:
            s.append(text(x + cw / 2.0, T + bh / 2 + 7, "?", fs + 2, col=RED))
    R = L + n * cw
    yb = T + bh + 6
    s.append("<path d='M%d %d v8 H%d v-8' fill='none' stroke='%s' stroke-width='2'/>" % (L, yb, R, INK))
    s.append(text((L + R) / 2.0, yb + 28, "%s for %d %s" % (M(total), n, unit), fs))
    W = max(R, (L + R) / 2.0 + tw("%s for %d %s" % (M(total), n, unit), fs) / 2) + 10
    return svg_wrap(int(W + 0.99), yb + 36, "".join(s), "tape diagram: %s split into %d equal parts" % (M(total), n))


# ============================================================ set 1: whole-number unit rates
def ur_item(q, a, ua, b, ub, kinds, link="per", figure=None, note=""):
    """Unit rate a/b (a whole number). ua, ub = (one, many)."""
    r = Fr(a, b)
    assert r.denominator == 1
    ans = "%s %s %s" % (qty(r, ua), link, ub[0])
    e = ("“%s %s” means for 1 %s. Divide: %s ÷ %s = <b>%s</b>. Check: %s × %s = %s."
         % (cap(link), ub[0], ub[0], qty(a, ua), qty(b, ub), ans,
            f(int(r)), f(b), f(a)))
    wrong = {
        "label": ("%s %s %s" % (qty(r, ub), link, ua[0]), "label"),
        "way": ("%s %s %s" % (qty(Fr(b, a), ua), link, ub[0]), "way"),
        "mul": ("%s %s %s" % (qty(a * b, ua), link, ub[0]), "mul"),
        "sub": ("%s %s %s" % (qty(a - b, ua), link, ub[0]), "sub"),
    }
    tips = {"label": "“%s %s %s” has the units backwards." % (plain(qty(r, ub)), link, ua[0]),
            "way": "%s ÷ %s divides the wrong way." % (f(b), f(a)),
            "mul": "%s × %s multiplies instead of dividing." % (f(a), f(b)),
            "sub": ""}
    e += " " + " ".join(tips[k] for k in kinds if tips[k])
    if note:
        e += " " + note
    if figure:
        q = fig(figure) + q
    return mcq(q, ans, [wrong[k] for k in kinds] + [wrong["sub"], wrong["mul"]], e)


MI, HR = ("mile", "miles"), ("hour", "hours")


def set_whole(P):
    its = []
    # double number lines
    its.append(ur_item("A car drives 120 miles in 2 hours at a steady speed. How many miles per hour is that?",
                       120, MI, 2, HR, ["label", "way", "mul"], figure=dnl_svg(120, "miles", 2, "hours")))
    its.append(ur_item("A printer prints 150 pages in 5 minutes. How many pages per minute does it print?",
                       150, ("page", "pages"), 5, ("minute", "minutes"), ["way", "mul", "label"],
                       figure=dnl_svg(150, "pages", 5, "minutes")))
    n, he, his = P.next()
    its.append(ur_item("%s types 180 words in 4 minutes. How many words per minute does %s type?" % (n, he),
                       180, ("word", "words"), 4, ("minute", "minutes"), ["mul", "label", "way"],
                       figure=dnl_svg(180, "words", 4, "minutes")))
    n, he, his = P.next()
    its.append(ur_item("%s reads 96 pages in 3 days. How many pages does %s read per day?" % (n, he),
                       96, ("page", "pages"), 3, ("day", "days"), ["label", "mul", "way"],
                       figure=dnl_svg(96, "pages", 3, "days")))
    # plain text
    n, he, his = P.next()
    its.append(ur_item("%s walks 12 miles in 4 hours. What is %s walking speed?" % (n, his),
                       12, MI, 4, HR, ["way", "label", "mul"]))
    its.append(ur_item("A train travels 260 miles in 4 hours. What is its speed in miles per hour?",
                       260, MI, 4, HR, ["mul", "way", "label"]))
    n, he, his = P.next()
    its.append(ur_item("%s rides a bike 36 miles in 3 hours. How many miles per hour does %s ride?" % (n, he),
                       36, MI, 3, HR, ["label", "way", "sub"]))
    its.append(ur_item("A garden hose fills a 45-gallon tub in 9 minutes. How many gallons per minute flow from the hose?",
                       45, ("gallon", "gallons"), 9, ("minute", "minutes"), ["way", "sub", "label"]))
    n, he, his = P.next()
    its.append(ur_item("%s counts that %s heart beats 225 times in 3 minutes. What is %s heart rate?" % (n, his, his),
                       225, ("beat", "beats"), 3, ("minute", "minutes"), ["label", "mul", "way"]))
    its.append(ur_item("A car uses 4 gallons of gas to drive 112 miles. How many miles per gallon does it get?",
                       112, MI, 4, ("gallon", "gallons"), ["label", "way", "mul"]))
    its.append(ur_item("A baker uses 24 eggs for 8 cakes. How many eggs does the baker use for each cake?",
                       24, ("egg", "eggs"), 8, ("cake", "cakes"), ["label", "sub", "way"], link="for each"))
    its.append(ur_item("A school gives out 168 pencils to 24 students. Each student gets the same number. "
                       "How many pencils is that for each student?",
                       168, ("pencil", "pencils"), 24, ("student", "students"), ["way", "label", "sub"], link="for each"))
    its.append(ur_item("84 students ride 3 buses to a field trip. Each bus has the same number of students. "
                       "How many students are there per bus?",
                       84, ("student", "students"), 3, ("bus", "buses"), ["mul", "label", "sub"]))
    n, he, his = P.next()
    its.append(ur_item("%s swims 20 laps in 10 minutes. How many laps per minute does %s swim?" % (n, he),
                       20, ("lap", "laps"), 10, ("minute", "minutes"), ["way", "label", "mul"]))
    its.append(ur_item("A bean plant grows 14 inches in 7 weeks. How many inches per week does it grow?",
                       14, ("inch", "inches"), 7, ("week", "weeks"), ["mul", "way", "label"]))
    its.append(ur_item("A cheetah runs 300 meters in 10 seconds. How many meters per second is that?",
                       300, ("meter", "meters"), 10, ("second", "seconds"), ["label", "way", "mul"]))
    # ideas
    its.append(mcq("Which rate is a <b>unit rate</b>?", "55 miles per hour",
                   ["110 miles in 2 hours", "6 laps in 3 minutes", "20 pages in 4 days"],
                   "A unit rate tells how much for <b>1</b> unit. “55 miles per hour” means 55 miles in 1 hour. "
                   "The others compare to 2, 3 or 4 units."))
    its.append(mcq("What does “per” mean in “28 miles per gallon”?", "for each", ["in total", "more than", "times"],
                   "“Per” means <b>for each</b> (or for 1). The car goes 28 miles for each gallon of gas."))
    its.append(mcq("A car drives 150 miles in 3 hours. Which problem finds the miles per hour?", "150 ÷ 3",
                   ["3 ÷ 150", "150 × 3", "150 − 3"],
                   "Miles per hour = miles ÷ hours. Put the miles first: <b>150 ÷ 3</b> = 50 miles per hour. "
                   "3 ÷ 150 would give hours per mile."))
    n, he, his = P.next()
    its.append(mcq("%s runs 9 laps in 3 minutes. %s says %s rate is %s lap per minute. What is the correct rate?"
                   % (n, cap(he), his, fr(1, 3)), "3 laps per minute",
                   ["27 laps per minute", "3 minutes per lap", "6 laps per minute"],
                   "%s divided the wrong way (3 ÷ 9). Laps per minute = laps ÷ minutes: 9 ÷ 3 = <b>3 laps per minute</b>. "
                   "Check: 3 × 3 = 9 laps." % n))
    assert len(its) == 20, len(its)
    return {"title": "Find a unit rate (whole numbers)", "items": its}


# ============================================================ set 2: unit price
def price_item(q, total, n, one, per_word=None, figure=False, note=""):
    """Unit price = total ÷ n (cent-exact)."""
    total = Fr(total)
    u = total / n
    assert (u * 100).denominator == 1, (total, n)
    per = per_word or one
    e = ("For 1 %s, divide the total by %s: %s ÷ %s = <b>%s per %s</b>. Check: %s × %s = %s."
         % (per, f(n), M(total), f(n), M(u), per, f(n), M(u), M(total)))
    if note:
        e += " " + note
    c = [(M(total * n), total * n), (M(u * 10), u * 10), (M(u / 10), u / 10) if (u / 10 * 100).denominator == 1 else None]
    way = Fr(n) / total
    if (way * 100).denominator == 1:
        c.insert(1, (M(way), way))
    if total - n > 0:
        c.insert(2, (M(total - n), total - n))
    c.append((M(u * 100), u * 100))
    if figure:
        q = fig(tape_svg(total, n, one + "s" if n != 1 else one)) + q
    return mcq(q, (M(u), u), c, e)


def set_price(P):
    its = []
    its.append(price_item("3 muffins cost $4.50. What is the price of 1 muffin?", "4.50", 3, "muffin", figure=True))
    its.append(price_item("4 notebooks cost $7.00. What is the price for each notebook?", 7, 4, "notebook", figure=True))
    its.append(price_item("6 apples cost $2.40. How much does 1 apple cost?", "2.40", 6, "apple", figure=True))
    its.append(price_item("3 pounds of chicken cost $9.60. What is the price per pound?", "9.60", 3, "pound",
                          figure=True))
    its.append(price_item("We paid $75 for 15 hamburgers. What is the rate per hamburger?", 75, 15, "hamburger",
                          note="So $75 for 15 hamburgers is a rate of $5 per hamburger."))
    its.append(price_item("A 12-ounce box of cereal costs $3.84. What is the price per ounce?", "3.84", 12, "ounce",
                          note="A store shelf tag often shows this unit price."))
    its.append(price_item("A pack of 8 pencils costs $2.00. What does 1 pencil cost?", 2, 8, "pencil"))
    its.append(price_item("A 5-pound bag of apples costs $6.45. What is the price per pound?", "6.45", 5, "pound"))
    its.append(price_item("5 bus tickets cost $12.50. What is the price of 1 ticket?", "12.50", 5, "ticket"))
    n, he, his = P.next()
    its.append(price_item("%s pays $38.40 for 12 gallons of gas. What is the price per gallon?" % n, "38.40", 12, "gallon"))
    n, he, his = P.next()
    its.append(price_item("%s earns $72 for 6 hours of babysitting. How much does %s earn per hour?" % (n, he), 72, 6, "hour"))
    its.append(price_item("A 6-pack of water costs $4.20. How much is that per bottle?", "4.20", 6, "bottle"))
    its.append(price_item("A bunch of 6 bananas costs $1.50. What does each banana cost?", "1.50", 6, "banana"))
    its.append(price_item("A 2-pound bag of grapes costs $5.98. What is the price per pound?", "5.98", 2, "pound"))
    its.append(price_item("A case of 24 cans of juice costs $10.80. What is the price per can?", "10.80", 24, "can"))
    its.append(price_item("4 movie tickets cost $54. What is the price of 1 ticket?", 54, 4, "ticket"))
    its.append(price_item("A 16-ounce block of cheese costs $4.00. What is the price per ounce?", 4, 16, "ounce"))
    its.append(price_item("Parking costs $9.00 for 3 hours. What is the cost per hour?", 9, 3, "hour"))
    # ideas
    its.append(mcq("4 pens cost $3.00. Which problem finds the price of 1 pen?", "$3.00 ÷ 4",
                   ["4 ÷ $3.00", "$3.00 × 4", "$3.00 − 4"],
                   "The price for 1 pen is the total price shared into 4 equal parts: <b>$3.00 ÷ 4</b> = $0.75. "
                   "4 ÷ 3.00 divides the wrong way: it tells how many pens you get for $1."))
    n, he, his = P.next()
    its.append(mcq("A 5-pound bag of rice costs $4.00. %s says rice costs $1.25 per pound. What is the correct price per pound?"
                   % n, "$0.80", ["$1.25", "$20.00", "$8.00"],
                   "%s divided 5 ÷ 4, the wrong way. Price per pound = dollars ÷ pounds: $4.00 ÷ 5 = <b>$0.80</b>. "
                   "Check: 5 × $0.80 = $4.00. ($1.25 is how many pounds you get for $1.)" % n))
    assert len(its) == 20, len(its)
    return {"title": "Unit price: the cost of one", "items": its}


# ============================================================ set 3: fraction and decimal unit rates
def fd_item(q, a, ua, b, ub, fmt="f", ans_u=None, note=""):
    """Amount of ua for 1 ub = a/b, shown as a fraction (fmt f) or a decimal (fmt d)."""
    r = Fr(a, b)
    uu = ans_u or ua
    ans = qty(r, uu, fmt)
    c = []
    way = Fr(b, a)
    if fmt == "f" or terminates(way):
        c.append((qty(way, uu, fmt), way))
    c.append((qty(a * b, uu, fmt), Fr(a * b)))
    q0, rem = divmod(a, b)
    if fmt == "d" and rem and rem < 10 and q0 > 0:
        mis = Fr(int("%d%d" % (q0, rem)), 10)
        c.append((qty(mis, uu, "d"), mis))      # 7 ÷ 2 = 3 R1 written as 3.1
    if a != b:
        c.append((qty(abs(a - b), uu, fmt), Fr(abs(a - b))))
    if q0 > 0:
        c.append((qty(q0, uu, fmt), Fr(q0)))
    if fmt == "f":
        c.append((qty(r * 2, uu, fmt), r * 2))
    e = "To find the amount for 1 %s, divide: %s ÷ %s = " % (ub[0], f(a), f(b))
    if fmt == "f" and (r.numerator, r.denominator) != (a, b):
        e += "%s = " % fr(a, b)
    e += "<b>%s</b>." % ans
    e += " Check: %s × %s = %s." % (show(r, fmt), f(b), f(a))
    e += " (%s ÷ %s divides the wrong way.)" % (f(b), f(a))
    if note:
        e += " " + note
    return mcq(q, (ans, r), c, e)


def set_frac(P):
    its = []
    C = ("cup", "cups")
    its.append(fd_item("A recipe uses 3 cups of flour for 4 cups of sugar. How many cups of flour are there for each cup of sugar?",
                       3, C, 4, ("cup of sugar", "cups of sugar"),
                       note="So the ratio 3 : 4 has the unit rate %s cup of flour per cup of sugar." % fr(3, 4)))
    n, he, his = P.next()
    its.append(fd_item("%s uses 2 cups of milk for 3 batches of pancakes. How much milk is that per batch?" % n,
                       2, C, 3, ("batch", "batches")))
    its.append(fd_item("8 friends share 5 pizzas equally. How much pizza does each friend get?",
                       5, ("pizza", "pizzas"), 8, ("friend", "friends")))
    n, he, his = P.next()
    its.append(fd_item("%s feeds %s dog 5 pounds of food in 2 days. How much food is that per day?" % (n, his),
                       5, ("pound", "pounds"), 2, ("day", "days")))
    n, he, his = P.next()
    its.append(fd_item("%s walks 7 miles in 2 hours. What is %s speed in miles per hour?" % (n, his),
                       7, MI, 2, HR, fmt="d", ans_u=("mile per hour", "miles per hour")))
    its.append(fd_item("A painter uses 2 gallons of paint for 5 walls of the same size. How much paint is that for each wall?",
                       2, ("gallon", "gallons"), 5, ("wall", "walls")))
    n, he, his = P.next()
    its.append(fd_item("%s uses 9 feet of ribbon to wrap 4 gifts. How much ribbon is that per gift?" % n,
                       9, ("foot", "feet"), 4, ("gift", "gifts")))
    its.append(fd_item("A tap fills a 15-liter bucket in 6 minutes. How many liters per minute does it fill?",
                       15, ("liter", "liters"), 6, ("minute", "minutes"), fmt="d"))
    its.append(fd_item("3 inches of rain fell in 12 hours. How much rain fell per hour?",
                       3, ("inch", "inches"), 12, HR))
    its.append(fd_item("A bean plant grows 9 centimeters in 6 days. How many centimeters per day does it grow?",
                       9, ("centimeter", "centimeters"), 6, ("day", "days"), fmt="d"))
    its.append(fd_item("A car goes 150 miles on 4 gallons of gas. How many miles per gallon does it get?",
                       150, MI, 4, ("gallon", "gallons"), fmt="d"))
    its.append(fd_item("A recipe uses 3 cups of flour for 4 cups of sugar. How many cups of sugar are there for each cup of flour?",
                       4, C, 3, ("cup of flour", "cups of flour"),
                       note="Every ratio has two unit rates: %s cup of flour per cup of sugar, and 1 %s cups of sugar per cup of flour."
                       % (fr(3, 4), fr(1, 3))))
    n, he, his = P.next()
    its.append(fd_item("%s swims 6 laps in 8 minutes. How many laps per minute does %s swim?" % (n, he),
                       6, ("lap", "laps"), 8, ("minute", "minutes")))
    its.append(fd_item("A lemonade recipe uses 6 lemons for 4 cups of lemonade. How many lemons are used for each cup?",
                       6, ("lemon", "lemons"), 4, C))
    n, he, his = P.next()
    its.append(fd_item("%s rides a bike 27 miles in 2 hours. What is %s speed in miles per hour?" % (n, his),
                       27, MI, 2, HR, fmt="d", ans_u=("mile per hour", "miles per hour")))
    its.append(fd_item("5 inches of snow fell in 4 hours. How many inches fell per hour?",
                       5, ("inch", "inches"), 4, HR))
    its.append(fd_item("3 yards of fabric make 8 pillows. How much fabric is used for each pillow?",
                       3, ("yard", "yards"), 8, ("pillow", "pillows")))
    # ideas
    n, he, his = P.next()
    its.append(mcq("%s runs 5 kilometers in 25 minutes. How many minutes does %s take per kilometer?" % (n, he),
                   "5 minutes", [fr(1, 5) + " minute", "125 minutes", "20 minutes"],
                   "Now the minutes come first: minutes ÷ kilometers = 25 ÷ 5 = <b>5 minutes</b> per kilometer. "
                   "(The other unit rate is 5 ÷ 25 = %s kilometer per minute.)" % fr(1, 5)))
    its.append(mcq("What is the unit rate a/b for the ratio 2 : 5?", fr(2, 5), [frac(Fr(5, 2)), "10", "3"],
                   "For the ratio a : b, the unit rate is a ÷ b. 2 ÷ 5 = <b>%s</b>. "
                   "It means %s of the first amount for each 1 of the second amount." % (fr(2, 5), fr(2, 5))))
    its.append(mcq("A club has 4 teachers for 60 students. Which sentence uses rate language correctly?",
                   "There are 15 students for each teacher.",
                   ["There are 15 teachers for each student.", "There are 4 students for each teacher.",
                    "There are 60 students for each teacher."],
                   "Students per teacher = 60 ÷ 4 = 15, so there are <b>15 students for each teacher</b>. "
                   "“15 teachers for each student” swaps the units."))
    assert len(its) == 20, len(its)
    return {"title": "Unit rates with fractions and decimals", "items": its}


# ============================================================ set 4: compare unit rates
def per_txt(x, unit):
    return "%s per %s" % (M(x), unit)


def buy2(q, A, B, unit, names=("Box A", "Box B"), more_is_better=False, rate_unit=None):
    """A, B = (amount, price). Lower price per unit wins (or higher amount per unit when more_is_better)."""
    ua, ub = Fr(A[1]) / A[0], Fr(B[1]) / B[0]
    e = ("Compare the price for 1 %s, not the total price. %s: %s ÷ %s = %s. %s: %s ÷ %s = %s. "
         % (unit, names[0], M(A[1]), f(A[0]), per_txt(ua, unit), names[1], M(B[1]), f(B[0]), per_txt(ub, unit)))
    if ua == ub:
        ans = "Both cost the same per %s" % unit
        e += "The unit prices are equal, so <b>neither is a better buy</b>."
    else:
        w = names[0] if ua < ub else names[1]
        ans = w
        e += "<b>%s</b> costs less per %s, so it is the better buy." % (w, unit)
        cheap_total = names[0] if Fr(A[1]) < Fr(B[1]) else names[1]
        if cheap_total != w:
            e += " (%s costs less in total, but you get less.)" % cheap_total
    return mcq(q, ans, [names[0], names[1], "Both cost the same per %s" % unit, "Not enough information"], e)


def buy3(q, opts, unit):
    """opts = [(label, amount, price)]; lowest unit price wins."""
    us = [(Fr(p) / a, lab, a, p) for lab, a, p in opts]
    best = min(us)
    assert sorted(us)[0][0] < sorted(us)[1][0]
    e = "Find each price per %s: " % unit + "; ".join(
        "%s: %s ÷ %s = %s" % (lab, M(p), f(a), per_txt(u, unit)) for u, lab, a, p in us) + \
        ". The lowest unit price is %s, so the <b>%s</b> is the best buy." % (per_txt(best[0], unit), best[1])
    return mcq(q, best[1], [lab for lab, a, p in opts] + ["They all cost the same per %s" % unit], e)


def speed2(q, A, B, names, u_top, u_bot, verb, more="does more in total"):
    """A, B = (amount, time). Faster = bigger amount per unit of time."""
    ra, rb = Fr(A[0], A[1]), Fr(B[0], B[1])
    rt = lambda r: "%s %s per %s" % (dec(r) if terminates(r) else frac(r), u_top[1] if r > 1 else u_top[0], u_bot)
    e = ("Find each unit rate. %s: %s ÷ %s = %s. %s: %s ÷ %s = %s. "
         % (names[0], f(A[0]), f(A[1]), rt(ra), names[1], f(B[0]), f(B[1]), rt(rb)))
    same = "Both %s at the same rate" % verb
    if ra == rb:
        ans = same
        e += "The unit rates are equal, so <b>they %s at the same rate</b>." % verb
    else:
        ans = names[0] if ra > rb else names[1]
        e += "<b>%s</b> has the greater unit rate." % ans
        big = names[0] if A[0] > B[0] else names[1]
        if big != ans:
            e += " (%s %s, but takes more time.)" % (big, more)
    return mcq(q, ans, [names[0], names[1], same, "Cannot tell, the times are different"], e)


def set_compare(P):
    its = []
    its.append(buy2("Which is the better buy?<br><b>Box A:</b> 12 ounces of cereal for $3.00<br><b>Box B:</b> 20 ounces of cereal for $4.00",
                    (12, 3), (20, 4), "ounce"))
    its.append(buy2("Which is the better buy?<br><b>Bottle A:</b> 64 ounces of juice for $3.84<br><b>Bottle B:</b> 32 ounces of juice for $2.24",
                    (64, Fr(384, 100)), (32, Fr(224, 100)), "ounce", names=("Bottle A", "Bottle B")))
    its.append(buy2("Which is the better buy?<br><b>Bag A:</b> 1 pound of pasta for $1.50<br><b>Bag B:</b> 3 pounds of pasta for $4.20",
                    (1, Fr(3, 2)), (3, Fr(42, 10)), "pound", names=("Bag A", "Bag B")))
    its.append(buy2("Which is the better buy?<br><b>Pack A:</b> 10 pencils for $2.50<br><b>Pack B:</b> 24 pencils for $5.28",
                    (10, Fr(5, 2)), (24, Fr(528, 100)), "pencil", names=("Pack A", "Pack B")))
    its.append(buy2("Which is the better buy?<br><b>Carton A:</b> 12 eggs for $3.60<br><b>Carton B:</b> 18 eggs for $5.40",
                    (12, Fr(36, 10)), (18, Fr(54, 10)), "egg", names=("Carton A", "Carton B")))
    its.append(buy2("Which is the better buy?<br><b>Pack A:</b> 4 cups of yogurt for $2.00<br><b>Pack B:</b> 6 cups of yogurt for $3.30",
                    (4, 2), (6, Fr(33, 10)), "cup", names=("Pack A", "Pack B")))
    its.append(buy3("Which bag of rice costs the least per pound?<br>2-pound bag: $3.00<br>5-pound bag: $6.50<br>10-pound bag: $12.00",
                    [("2-pound bag", 2, 3), ("5-pound bag", 5, Fr(65, 10)), ("10-pound bag", 10, 12)], "pound"))
    its.append(buy3("Which bag of apples costs the least per pound?<br>3-pound bag: $4.35<br>5-pound bag: $6.95<br>8-pound bag: $11.60",
                    [("3-pound bag", 3, Fr(435, 100)), ("5-pound bag", 5, Fr(695, 100)), ("8-pound bag", 8, Fr(1160, 100))], "pound"))
    its.append(buy3("Which pack of water costs the least per bottle?<br>6-pack: $3.00<br>12-pack: $5.40<br>24-pack: $11.04",
                    [("6-pack", 6, 3), ("12-pack", 12, Fr(54, 10)), ("24-pack", 24, Fr(1104, 100))], "bottle"))
    a, b = P.next(), P.next()
    its.append(speed2("%s walks 6 miles in 2 hours. %s walks 10 miles in 4 hours. Who walks faster?" % (a[0], b[0]),
                      (6, 2), (10, 4), (a[0], b[0]), MI, "hour", "walk", "walks farther in total"))
    its.append(speed2("Car A goes 165 miles in 3 hours. Car B goes 240 miles in 4 hours. Which car is faster?",
                      (165, 3), (240, 4), ("Car A", "Car B"), MI, "hour", "drive", "goes farther in total"))
    a, b = P.next(), P.next()
    its.append(speed2("%s types 150 words in 3 minutes. %s types 245 words in 5 minutes. Who types faster?" % (a[0], b[0]),
                      (150, 3), (245, 5), (a[0], b[0]), ("word", "words"), "minute", "type", "types more words in total"))
    a, b = P.next(), P.next()
    its.append(speed2("%s runs 3 miles in 30 minutes. %s runs 5 miles in 50 minutes. Who runs faster?" % (a[0], b[0]),
                      (3, 30), (5, 50), (a[0], b[0]), MI, "minute", "run"))
    its.append(speed2("Faucet A fills 12 gallons in 4 minutes. Faucet B fills 25 gallons in 10 minutes. Which faucet fills faster?",
                      (12, 4), (25, 10), ("Faucet A", "Faucet B"), ("gallon", "gallons"), "minute", "fill", "fills more water in total"))
    its.append(mcq("Recipe A uses 2 cups of sugar for 3 cups of flour. Recipe B uses 3 cups of sugar for 4 cups of flour. "
                   "Which recipe uses more sugar for each cup of flour?", "Recipe B",
                   ["Recipe A", "Both use the same amount", "Not enough information"],
                   "Sugar per cup of flour: A: 2 ÷ 3 = %s cup. B: 3 ÷ 4 = %s cup. %s = %s and %s = %s, so <b>Recipe B</b> "
                   "uses more sugar per cup of flour." % (fr(2, 3), fr(3, 4), fr(2, 3), fr(8, 12), fr(3, 4), fr(9, 12))))
    its.append(mcq("Car A drives 336 miles on 12 gallons of gas. Car B drives 300 miles on 10 gallons. "
                   "Which car goes farther on 1 gallon?", "Car B",
                   ["Car A", "Both go the same distance", "Not enough information"],
                   "Miles per gallon: A: 336 ÷ 12 = 28. B: 300 ÷ 10 = 30. <b>Car B</b> goes farther on each gallon. "
                   "(Car A goes more miles in total, but it uses more gas.)"))
    a, b = P.next(), P.next()
    its.append(mcq("%s earns $45 for 4 hours of work. %s earns $56 for 5 hours. Who earns more per hour?" % (a[0], b[0]),
                   a[0], [b[0], "They earn the same per hour", "Not enough information"],
                   "%s: $45 ÷ 4 = $11.25 per hour. %s: $56 ÷ 5 = $11.20 per hour. <b>%s</b> earns $0.05 more per hour, "
                   "even though %s earns more in total." % (a[0], b[0], a[0], b[0])))
    its.append(mcq("An 18-ounce jar of peanut butter costs $3.60. A 12-ounce jar costs $2.76. "
                   "How much less per ounce does the better buy cost?", ("$0.03", "0.03"),
                   [("$0.84", "0.84"), ("$0.20", "0.20"), ("$0.23", "0.23")],
                   "18-ounce jar: $3.60 ÷ 18 = $0.20 per ounce. 12-ounce jar: $2.76 ÷ 12 = $0.23 per ounce. "
                   "$0.23 − $0.20 = <b>$0.03</b> less per ounce. ($0.84 is the difference of the total prices.)"))
    its.append(mcq("Store A sells 4 pounds of bananas for $2.36. Store B sells 3 pounds for $1.86. "
                   "What is the lower price per pound?", "$0.59", ["$0.62", "$1.86", "$2.36"],
                   "Store A: $2.36 ÷ 4 = $0.59 per pound. Store B: $1.86 ÷ 3 = $0.62 per pound. "
                   "The lower price per pound is <b>$0.59</b>, at Store A."))
    n, he, his = P.next()
    its.append(mcq("A 2-pound bag of rice costs $3.00 and a 5-pound bag costs $6.50. %s says the 2-pound bag is the better "
                   "buy because $3.00 is less than $6.50. What should %s compare?" % (n, he),
                   "the price per pound", ["the total prices", "the number of pounds", "the price per bag"],
                   "Compare <b>the price per pound</b>. 2-pound bag: $3.00 ÷ 2 = $1.50 per pound. "
                   "5-pound bag: $6.50 ÷ 5 = $1.30 per pound. The 5-pound bag is the better buy."))
    assert len(its) == 20, len(its)
    return {"title": "Compare unit rates: the better buy and the faster speed", "items": its}


# ============================================================ set 5: use a unit rate (word problems)
def wp(q, ans, wrong, e):
    return mcq(q, ans, wrong, e)


def set_words(P):
    its = []
    # verified numbers
    assert 60 * 4 == 240
    its.append(wp("A car travels at 60 miles per hour. How far does it go in 4 hours?", "240 miles",
                  ["15 miles", "64 miles", "56 miles"],
                  "Distance = speed × time: 60 × 4 = <b>240 miles</b>. (15 divides instead of multiplying; 64 adds.)"))
    n, he, his = P.next()
    assert Fr(6, 2) * 5 == 15
    its.append(wp("%s walks 6 miles in 2 hours. At the same rate, how far can %s walk in 5 hours?" % (n, he), "15 miles",
                  ["30 miles", "9 miles", "12 miles"],
                  "Unit rate first: 6 ÷ 2 = 3 miles per hour. Then 3 × 5 = <b>15 miles</b>. "
                  "(30 multiplies 6 × 5 without finding the rate; 9 just adds 3 more.)"))
    assert Fr(9, 6) * 10 == 15
    its.append(wp("6 muffins cost $9.00. At the same price, how much do 10 muffins cost?", "$15.00",
                  ["$90.00", "$13.00", "$54.00"],
                  "Unit price: $9.00 ÷ 6 = $1.50 per muffin. 10 × $1.50 = <b>$15.00</b>. "
                  "($13.00 adds $4 for 4 more muffins; $90.00 multiplies $9.00 × 10.)"))
    assert Fr(210, 30) == 7
    its.append(wp("A printer prints 30 pages per minute. How long does it take to print 210 pages?", "7 minutes",
                  ["6,300 minutes", "180 minutes", fr(1, 7) + " minute"],
                  "Time = pages ÷ pages per minute: 210 ÷ 30 = <b>7 minutes</b>. Check: 30 × 7 = 210."))
    assert Fr(4, 7) * 35 == 20
    its.append(wp("It took 7 hours to mow 4 lawns. At that rate, how many lawns can be mowed in 35 hours?", "20 lawns",
                  ["140 lawns", "32 lawns", "5 lawns"],
                  "35 hours is 35 ÷ 7 = 5 times as long, so mow 5 × 4 = <b>20 lawns</b>. "
                  "(The rate is %s lawn per hour, and %s × 35 = 20.) 5 lawns forgets to multiply by 4." % (fr(4, 7), fr(4, 7))))
    assert Fr(224, 32) == 7
    its.append(wp("A car gets 32 miles per gallon. How many gallons does it need to drive 224 miles?", "7 gallons",
                  ["7,168 gallons", "192 gallons", "256 gallons"],
                  "Gallons = miles ÷ miles per gallon: 224 ÷ 32 = <b>7 gallons</b>. Check: 7 × 32 = 224."))
    n, he, his = P.next()
    assert Fr(10) / Fr(5, 4) == 8
    its.append(wp("Oranges cost $1.25 per pound. How many pounds can %s buy with $10.00?" % n, "8 pounds",
                  ["12.5 pounds", "0.125 pound", "11.25 pounds"],
                  "Pounds = money ÷ price per pound: 10.00 ÷ 1.25 = 1,000 ÷ 125 = <b>8 pounds</b>. Check: 8 × $1.25 = $10.00. "
                  "(12.5 multiplies 10 × 1.25.)"))
    n, he, his = P.next()
    assert Fr(36, 3) * 8 == 96
    its.append(wp("%s earns $36 for 3 hours of dog walking. At the same rate, how much does %s earn for 8 hours?" % (n, he),
                  "$96.00", ["$288.00", "$41.00", "$13.50"],
                  "Unit rate: $36 ÷ 3 = $12 per hour. 8 × $12 = <b>$96.00</b>. "
                  "($41.00 adds 5 for 5 more hours; $288.00 multiplies $36 × 8.)"))
    assert Fr(120, 8) == 15
    its.append(wp("A tank holds 120 gallons of water. It drains at 8 gallons per minute. How long does it take to empty?",
                  "15 minutes", ["960 minutes", "112 minutes", fr(1, 15) + " minute"],
                  "Time = gallons ÷ gallons per minute: 120 ÷ 8 = <b>15 minutes</b>. Check: 8 × 15 = 120."))
    assert Fr(225, 100) / 3 * 12 == 9
    its.append(wp("3 pens cost $2.25. At the same price, how much do 12 pens cost?", "$9.00",
                  ["$27.00", "$11.25", "$6.75"],
                  "Unit price: $2.25 ÷ 3 = $0.75 per pen. 12 × $0.75 = <b>$9.00</b>. "
                  "Or: 12 pens is 4 times 3 pens, so 4 × $2.25 = $9.00. ($11.25 adds $9 for 9 more pens.)"))
    assert 65 * 3 + 55 * 2 == 305
    its.append(wp("A train goes 65 miles per hour for 3 hours, then 55 miles per hour for 2 hours. How far does it go in all?",
                  "305 miles", ["300 miles", "195 miles", "120 miles"],
                  "Find each part: 65 × 3 = 195 miles and 55 × 2 = 110 miles. 195 + 110 = <b>305 miles</b>. "
                  "(300 uses the average of the speeds, 60 × 5, but the train spent more time at 65 mph.)"))
    a, b = P.next(), P.next()
    assert Fr(120, 4) - Fr(175, 7) == 5
    its.append(wp("%s reads 120 pages in 4 hours. %s reads 175 pages in 7 hours. How many more pages per hour does %s read?"
                  % (a[0], b[0], a[0]), "5 pages per hour",
                  ["55 pages per hour", "30 pages per hour", "25 pages per hour"],
                  "%s: 120 ÷ 4 = 30 pages per hour. %s: 175 ÷ 7 = 25 pages per hour. 30 − 25 = <b>5 more pages per hour</b>. "
                  "(55 is the difference of the totals.)" % (a[0], b[0])))
    n, he, his = P.next()
    assert Fr(75, 10) / 3 == Fr(5, 2)
    its.append(wp("%s walks at 3 miles per hour. How long will it take %s to walk 7.5 miles?" % (n, "her" if he == "she" else "him"),
                  "2.5 hours", ["22.5 hours", "4.5 hours", "0.4 hour"],
                  "Time = distance ÷ speed: 7.5 ÷ 3 = <b>2.5 hours</b>. Check: 3 × 2.5 = 7.5 miles. "
                  "(22.5 multiplies; 0.4 is 3 ÷ 7.5, the wrong way.)"))
    assert 4 * 60 == 240
    its.append(wp("Water flows from a hose at 4 gallons per minute. How many gallons flow out in 1 hour?", "240 gallons",
                  ["15 gallons", "64 gallons", "4 gallons"],
                  "1 hour = 60 minutes. 4 × 60 = <b>240 gallons</b>. (15 is 60 ÷ 4; 4 gallons is only 1 minute.)"))
    assert Fr(48, 10) / 12 * 30 == 12
    its.append(wp("A 12-pack of water costs $4.80. At the same price per bottle, how much do 30 bottles cost?", "$12.00",
                  ["$144.00", "$22.80", "$0.40"],
                  "Unit price: $4.80 ÷ 12 = $0.40 per bottle. 30 × $0.40 = <b>$12.00</b>. "
                  "($0.40 is the price of only 1 bottle; $22.80 adds $18 for 18 more bottles.)"))
    assert Fr(1800, 4) * 6 == 2700
    its.append(wp("A plane flies 1,800 miles in 4 hours. At that rate, how far does it fly in 6 hours?", "2,700 miles",
                  ["10,800 miles", "1,200 miles", "450 miles"],
                  "Unit rate: 1,800 ÷ 4 = 450 miles per hour. 450 × 6 = <b>2,700 miles</b>. "
                  "(450 is the distance in only 1 hour.)"))
    assert Fr(3, 4) * 6 == Fr(9, 2)
    its.append(wp("A recipe uses %s cup of sugar for each batch. How much sugar is needed for 6 batches?" % fr(3, 4),
                  "4 %s cups" % fr(1, 2), ["6 %s cups" % fr(3, 4), "8 cups", fr(3, 4) + " cup"],
                  "Multiply the unit rate by the number of batches: 6 × %s = %s = <b>4 %s cups</b>. "
                  "(6 %s adds; 8 is 6 ÷ %s.)" % (fr(3, 4), fr(18, 4), fr(1, 2), fr(3, 4), fr(3, 4))))
    n, he, his = P.next()
    assert Fr(2, 12) * 30 == 5
    its.append(wp("%s uses 2 cups of flour to make 12 pancakes. How much flour does %s need for 30 pancakes?" % (n, he),
                  "5 cups", ["60 cups", "20 cups", "6 cups"],
                  "Flour per pancake: 2 ÷ 12 = %s cup. 30 × %s = <b>5 cups</b>. Or: 30 is 2 %s times 12, so 2 × 2 %s = 5. "
                  "(20 adds 18 for 18 more pancakes; 6 is 12 ÷ 2, pancakes per cup.)" % (fr(1, 6), fr(1, 6), fr(1, 2), fr(1, 2))))
    n, he, his = P.next()
    assert Fr(40, 8) == 5
    its.append(wp("%s runs 1 mile in 8 minutes. At that rate, how many miles can %s run in 40 minutes?" % (n, he), "5 miles",
                  ["320 miles", "32 miles", "48 miles"],
                  "Every 8 minutes is 1 mile. 40 ÷ 8 = <b>5 miles</b>. (320 multiplies 40 × 8.)"))
    n, he, his = P.next()
    ca, cb = Fr(6) / 5 * 15, Fr(39, 10) / 3 * 15
    assert (ca, cb, cb - ca) == (18, Fr(195, 10), Fr(3, 2))
    its.append(wp("Store A sells 5 pounds of oranges for $6.00. Store B sells 3 pounds for $3.90. %s needs 15 pounds. "
                  "How much does %s save by buying them at the store with the lower unit price?" % (n, he), "$1.50",
                  ["$0.10", "$2.10", "$18.00"],
                  "Store A: $6.00 ÷ 5 = $1.20 per pound. Store B: $3.90 ÷ 3 = $1.30 per pound. "
                  "15 pounds: 15 × $1.20 = $18.00 at A and 15 × $1.30 = $19.50 at B. $19.50 − $18.00 = <b>$1.50</b>. "
                  "($0.10 is the saving on only 1 pound.)"))
    assert len(its) == 20, len(its)
    return {"title": "Word problems: use a unit rate (distance, time and cost)", "items": its}


# ============================================================ lesson
def body_html():
    f_dnl = dnl_svg(120, "miles", 3, "hours", full=True)
    f_tape = tape_svg(Fr(9, 2), 3, "muffins", full=True, cw=72)
    return (
        "<h2>The big idea</h2>"
        "<p>A <b>rate</b> compares two amounts with different units, like 120 miles in 3 hours. "
        "A <b>unit rate</b> tells how much for <b>1</b> unit: 40 miles in 1 hour. "
        "To find it, <b>divide</b> the first amount by the second.</p>"
        "<p>The words <b>per</b> and <b>for each</b> mean “for 1”. 40 miles per hour = 40 miles for each hour.</p>"
        "<h2>Find a unit rate</h2>"
        "<figure class='sn-fig'>" + f_dnl +
        "<figcaption>120 miles in 3 hours. Split both lines into 3 equal parts: 1 hour goes with 120 ÷ 3 = 40 miles.</figcaption></figure>"
        + ex("Example", "A car drives 120 miles in 3 hours. What is its speed?",
             "Miles ÷ hours = 120 ÷ 3 = 40. Check: 40 × 3 = 120.", "40 miles per hour")
        + "<h2>Unit price</h2>"
        "<p>The unit price is the cost of 1 item (or 1 pound, 1 ounce). Divide the total price by the number of items.</p>"
        "<figure class='sn-fig'>" + f_tape +
        "<figcaption>$4.50 for 3 muffins: $4.50 ÷ 3 = $1.50 per muffin.</figcaption></figure>"
        + ex("Example", "We paid $75 for 15 hamburgers. What is the price per hamburger?",
             "$75 ÷ 15 = $5. Check: 15 × $5 = $75.", "$5 per hamburger")
        + "<h2>Unit rates can be fractions or decimals</h2>"
        "<p>For the ratio a : b, the unit rate is a ÷ b = a/b. It does not have to be a whole number.</p>"
        + ex("Example", "A recipe has 3 cups of flour for 4 cups of sugar. How much flour is there for each cup of sugar?",
             "Flour ÷ sugar = 3 ÷ 4 = %s." % fr(3, 4), "%s cup of flour for each cup of sugar" % fr(3, 4))
        + "<p>Every ratio has <b>two</b> unit rates. 3 cups of flour for 4 cups of sugar also means "
        "4 ÷ 3 = 1 %s cups of sugar for each cup of flour. The units tell you which one you have.</p>" % fr(1, 3)
        + table(["Rate", "Divide", "Unit rate"], [
            ["7 miles in 2 hours", "7 ÷ 2", "3.5 miles per hour"],
            ["2 cups of milk for 3 batches", "2 ÷ 3", "%s cup per batch" % fr(2, 3)],
            ["9 feet of ribbon for 4 gifts", "9 ÷ 4", "2 %s feet per gift" % fr(1, 4)],
        ])
        + "<h2>Compare unit rates</h2>"
        "<p>To find the better buy, compare the <b>price for 1 unit</b>, not the total price.</p>"
        + table(["Box", "Price", "Price per ounce"], [
            ["12 ounces", "$3.00", "$3.00 ÷ 12 = $0.25"],
            ["20 ounces", "$4.00", "$4.00 ÷ 20 = $0.20"],
        ])
        + "<p>The 20-ounce box costs more in total, but less for each ounce, so it is the better buy. "
        "To compare speeds, find the distance per hour (or per minute) for each one.</p>"
        "<h2>Use a unit rate</h2>"
        "<p>Once you know the amount for 1, multiply to find any amount. Divide to find how many units or how long.</p>"
        + ex("Example", "6 muffins cost $9.00. How much do 10 muffins cost?",
             "Unit price: $9.00 ÷ 6 = $1.50 per muffin. Then 10 × $1.50 = $15.00.", "$15.00")
        + ex("Example", "Zoe walks at 3 miles per hour. How long does it take her to walk 4.5 miles?",
             "Time = distance ÷ speed = 4.5 ÷ 3 = 1.5. Check: 3 × 1.5 = 4.5.", "1.5 hours")
        + "<h2>Common mistakes</h2>"
        + table(["Mistake", "What to do instead"], [
            ["120 miles in 3 hours: 3 ÷ 120", "Miles per hour means miles ÷ hours: 120 ÷ 3 = 40"],
            ["$4.50 for 3 muffins: $4.50 × 3", "Price for 1 means divide: $4.50 ÷ 3 = $1.50"],
            ["Writing “40 hours per mile”", "Say the units in order: miles ÷ hours gives miles per hour"],
            ["Choosing the box with the lower total price", "Compare the price per ounce (or per pound)"],
            ["6 muffins $9, so 10 muffins $13 (adding $4)", "Find the unit price first: 10 × $1.50 = $15"],
        ])
    )


FAQ = [
    {"q": "What is a unit rate in 6th grade math?",
     "a": "A unit rate is a rate for 1 unit, such as 40 miles per hour or $1.50 per muffin. Find it by dividing the first amount by the second: 120 miles ÷ 3 hours = 40 miles per hour."},
    {"q": "How do you find the unit price to see which is the better buy?",
     "a": "Divide each price by its amount to get the price for 1 ounce, pound or item, then pick the lower unit price. A 20-ounce box for $4.00 ($0.20 per ounce) is a better buy than a 12-ounce box for $3.00 ($0.25 per ounce)."},
    {"q": "Can a unit rate be a fraction?",
     "a": "Yes. For the ratio a : b the unit rate is a/b, so 3 cups of flour for 4 cups of sugar is 3/4 cup of flour for each cup of sugar."},
    {"q": "What does 6.RP.A.2 mean?",
     "a": "It is the Common Core Grade 6 standard for understanding a unit rate a/b for a ratio a : b and using rate language such as “per” and “for each”, as in “$75 for 15 hamburgers is $5 per hamburger.”"},
]


def gen():
    rnd = random.Random(602)
    P = People(rnd)
    sets = [set_whole(P), set_price(P), set_frac(P), set_compare(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(plain(c) for c in it["c"])) == 4, it
            k = plain(it["q"])
            assert k not in seen, it["q"]
            seen.add(k)
    return {
        "country": "us", "subject": "math", "grade": "grade-6", "slug": "unit-rates", "sort": 2,
        "updated": UPDATED, "pdf_url": "",
        "title": "Unit Rates",
        "seo_title": "Grade 6 Unit Rates Worksheets: Rate Language, Unit Price, Better Buys and Constant Speed (Free, with Answer Key)",
        "short_title": "Unit rates",
        "domain": "Ratios and Proportional Relationships",
        "standard_code": "6.RP.A.2",
        "standard_url": "https://www.thecorestandards.org/Math/Content/6/RP/A/2/",
        "standard_text": "Understand the concept of a unit rate a/b associated with a ratio a:b with b ≠ 0, and use rate language in the context of a ratio relationship. For example, “This recipe has a ratio of 3 cups of flour to 4 cups of sugar, so there is 3/4 cup of flour for each cup of sugar.” “We paid $75 for 15 hamburgers, which is a rate of $5 per hamburger.”",
        "meta_desc": "Free Grade 6 unit rate worksheets: find unit rates with “per” and “for each”, unit prices, fraction and decimal unit rates, the better buy, constant speed and word problems. 100 practice questions with step-by-step answers and a printable answer key.",
        "key_big": "A unit rate is the amount for 1. Divide: 120 miles ÷ 3 hours = 40 miles per hour.",
        "key_sub": "“Per” and “for each” mean “for 1”. For a ratio a : b the unit rate is a/b, so 3 cups of flour for 4 cups of sugar is 3/4 cup of flour per cup of sugar. To find the better buy, compare the price for 1 unit, not the total price.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }


def mark_large(u, pattern):
    """Tag wide pictures (double number lines, tape diagrams) so they print larger."""
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    mark_large(u, "(?:double number line|tape diagram)")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
