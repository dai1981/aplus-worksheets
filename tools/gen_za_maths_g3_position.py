# -*- coding: utf-8 -*-
"""
South Africa Grade 3 Maths (CAPS): Position, Directions and Maps (Grade 3: Position, orientation and views)
  python3 tools/gen_za_maths_g3_position.py
Reading maps and grid references, compass directions, giving directions, bird's-eye views and real maps (Australia
Year 3 makers).
Wrong answers come from real mistakes: reading the row before the column, mixing up east and west, and counting the
starting square.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_au_maths_y3_maps as aum
adopt(aum)
if isinstance(getattr(aum, 'R', None), random.Random): aum.R = random.Random(803130)
za_common.GRADE = "grade-3"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _svgtxt(it):
    return " ".join(_re.findall(r">([^<>]*)<", " ".join(_re.findall(r"<svg.*?</svg>", it["q"] + " ".join(it["c"]), flags=_re.S))))


def _nums(it):
    t = _txt(it) + " " + _svgtxt(it)
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.,])\d[\d,\u00a0]*(?![.,]?\d)", t)]


def le(n):
    """All whole numbers in the item are n or less, and no decimals or negative numbers."""
    def f(it):
        t = _txt(it)
        if _re.search(r"\d[.,]\d|−\d|£|\bp\b|pence", t):
            return False
        return all(x <= n for x in _nums(it))
    f.__name__ = "le%d" % n
    return f


def lenonly(it):
    t = _txt(it)
    return bool(_re.search(r"\d ?(cm|m|km|mm)\b", t)) and not _re.search(r"\d ?(kg|g|ℓ|mℓ|ml|l)\b", t)


def nozoo(it):
    return "zoo" not in (it["q"] + it["e"]).lower()


def both(*fs):
    def f(it):
        return all(g(it) for g in fs)
    return f


def nomoney(it):
    return not _re.search(r"£|\$|\d+p\b|pence|pound|cent|coin|note", _txt(it), _re.I)


COINS = [(10, "10c"), (20, "20c"), (50, "50c"), (100, "R1"), (200, "R2"), (500, "R5")]
NOTES = [(1000, "R10"), (2000, "R20"), (5000, "R50"), (10000, "R100"), (20000, "R200")]
COLOURS = {10: "#c9944a", 20: "#c9944a", 50: "#c9944a", 100: "#cfcfcf", 200: "#cfcfcf", 500: "#d8c27a",
           1000: "#8fbf7a", 2000: "#c49a6c", 5000: "#e08a7a", 10000: "#8fb0d9", 20000: "#f0b060"}
RADIUS = {10: 18, 20: 21, 50: 24, 100: 23, 200: 26, 500: 28}


def mname(c):
    return "%dc" % c if c < 100 else "R%d" % (c // 100)


def money_svg(vals):
    from ws_common import svg_wrap, text
    x, body = 10, ""
    for v in vals:
        if v < 1000:
            rr = RADIUS[v]
            body += "<circle cx='%d' cy='36' r='%d' fill='%s' stroke='#555' stroke-width='2'/>" % (x + rr, rr, COLOURS[v]) + text(x + rr, 42, mname(v), 13 if v < 100 else 15)
            x += 2 * rr + 8
        else:
            body += "<rect x='%d' y='12' width='96' height='48' rx='4' fill='%s' stroke='#555' stroke-width='2'/>" % (x, COLOURS[v]) + text(x + 48, 43, mname(v), 18)
            x += 104
    return svg_wrap(x + 4, 72, body, "South African money: " + ", ".join(("%d cent coin" % v if v < 100 else "R%d coin" % (v // 100)) if v < 1000 else "R%d note" % (v // 100) for v in vals))


def rc(c):
    """cents -> 50c, R3, R3,50"""
    if c < 100:
        return "%dc" % c
    return rand(c / 100)


ITEMS = [("an apple", 400), ("a pencil", 300), ("a rubber", 200), ("a juice", 800), ("a vetkoek", 500), ("a packet of chips", 700), ("a lollipop", 100),
         ("a ruler", 600), ("a banana", 300), ("a koeksister", 400), ("a ball", 1500), ("a toy car", 1200), ("a book", 3500), ("a cap", 4500), ("a pie", 2000),
         ("a loaf of bread", 1800), ("a cool drink", 1200), ("a sticker book", 2500), ("a skipping rope", 3000), ("a puzzle", 6000), ("a T-shirt", 8000), ("a lunch box", 5500)]


def money_k(r, k, top):
    """top: largest amount in cents for this grade."""
    small = [v for v, _ in COINS + NOTES if v <= top]
    if k == "name":
        v = r.choice(small)
        right = mname(v)
        wr = [mname(w) for w in small if w != v]
        r.shuffle(wr)
        what = "coin" if v < 1000 else "note"
        return mcq("How much is this %s worth?" % what + fig(money_svg([v])), right, wr[:3],
                   "This %s is <b>%s</b>." % (what, right))
    if k == "count":
        for _ in range(50):
            n = r.randint(2, 5)
            vals = sorted((r.choice(small) for _ in range(n)), reverse=True)
            tot = sum(vals)
            if tot <= top and len(set(vals)) > 1:
                break
        else:
            raise AssertionError
        right = rc(tot)
        wr = [rc(tot + vals[-1]), rc(tot - vals[-1]), rc(n * 100) if n * 100 != tot else rc(tot + 100), rc(tot * 2) if tot * 2 <= top * 2 else rc(tot + 50)]
        return mcq("How much money is this altogether?" + fig(money_svg(vals)), right, [w for w in dict.fromkeys(wr) if w != right],
                   "Start with the biggest: %s = <b>%s</b>." % (" + ".join(mname(v) for v in vals), right))
    if k == "more":
        a, b = r.sample(small, 2)
        hi = max(a, b)
        right = mname(hi)
        return mcq("Which is worth more: <b>%s</b> or <b>%s</b>?" % (mname(a), mname(b)), right, [mname(min(a, b)), "They are worth the same", "You cannot tell"],
                   "%s is more than %s. <b>%s</b>." % (mname(hi), mname(min(a, b)), right))
    items = [(n, p) for n, p in ITEMS if p <= top // 2]
    if k == "shop":
        (n1, p1), (n2, p2) = r.sample(items, 2)
        if p1 + p2 > top:
            raise AssertionError
        nm = r.choice(za_common.GIRLS + za_common.BOYS)
        right = rc(p1 + p2)
        return mcq("%s buys %s for %s and %s for %s. How much does %s pay altogether?" % (nm, n1, rc(p1), n2, rc(p2), "she" if nm in za_common.GIRLS else "he"), right,
                   [rc(abs(p1 - p2)) if p1 != p2 else rc(p1 + p2 + 100), rc(p1 + p2 + 100), rc(p1 + p2 - 100) if p1 + p2 > 200 else rc(p1 + p2 + 200)],
                   "%s + %s = <b>%s</b>." % (rc(p1), rc(p2), right))
    n1, p1 = r.choice(items)
    note = r.choice([v for v, _ in NOTES + COINS if p1 < v <= top])
    nm = r.choice(za_common.GIRLS + za_common.BOYS)
    ch = note - p1
    right = rc(ch)
    return mcq("%s buys %s for %s and pays with a %s %s. How much change does %s get?" % (nm, n1, rc(p1), mname(note), "note" if note >= 1000 else "coin", "she" if nm in za_common.GIRLS else "he"), right,
               [rc(note + p1), rc(ch + 100), rc(ch - 100) if ch > 100 else rc(ch + 200)],
               "%s − %s = <b>%s</b>." % (mname(note), rc(p1), right))


def mk(k, top):
    seen = set()
    def f(r):
        it = money_k(r, k, top)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = "money_" + k
    return f

import k_pics as _kp
_KINDS = ["apple", "star", "ball", "button", "fish", "flower", "heart", "duck", "cup"]
_NAMES = za_common.GIRLS + za_common.BOYS


def _nm(r):
    n = r.choice(_NAMES)
    return n, ("she" if n in za_common.GIRLS else "he"), ("her" if n in za_common.GIRLS else "his")


def _near(r, v, lo=0, hi=10 ** 6, d=(1, 2, 10)):
    out = []
    for x in [v + 1, v - 1, v + 10, v - 10, v + 2, v - 2, v + 100, v - 100]:
        if lo <= x <= hi and x != v:
            out.append(x)
    r.shuffle(out)
    return out


def _w(n):
    return za_common.words(n)


def num_k(r, k, hi, lo=0):
    if k == "count":
        kind = r.choice(_KINDS)
        if hi <= 30:
            n = r.randint(max(lo, 3), hi)
            pic = _kp.row_svg(n, kind) if r.random() < 0.6 else _kp.scatter_svg(n, kind, r.randint(1, 999))
            return mcq("How many %s are there?" % _kp.name(kind) + fig(pic), n, [n + 1, n - 1, n + 2, n - 2],
                       "Touch and count each one once: there are <b>%d</b>." % n)
        t, o = r.randint(1, min(9, hi // 10)), r.randint(0, 9)
        n = 10 * t + o
        if n > hi:
            raise AssertionError
        return mcq("Each rod has 10 cubes. How many cubes are there?" + fig(_kp.rods_svg(t, o)), n, [10 * o + t if o else n + 10, t + o, n + 10, n - 1],
                   "%d tens and %d ones: %d + %d = <b>%d</b>." % (t, o, 10 * t, o, n))
    if k in ("after", "before"):
        step = r.choice([1, 1, 1, 2, 5, 10] if hi <= 100 else [1, 10, 10, 100, 5, 2])
        n = r.randint(lo + step, hi - step)
        if step > 1:
            n -= n % step
        v = n + step if k == "after" else n - step
        word = {1: "1", 2: "2", 5: "5", 10: "10", 100: "100"}[step]
        q = "What number is %s %s %d?" % (word, "more than" if k == "after" else "less than", n) if step > 1 else "What number comes just %s %d?" % (k, n)
        return mcq(q, v, [n - step if k == "after" else n + step, v + 1, v - 1, n], "%s %s from %d: <b>%d</b>." % ("Count on" if k == "after" else "Count back", word, n, v))
    if k == "seq":
        step = r.choice([1, 2, 5, 10] + ([100, 50] if hi > 200 else []))
        back = r.random() < 0.3
        start = r.randint(lo, hi - 5 * step)
        if step > 1:
            start -= start % step
        sq = [start + i * step for i in range(5)]
        if back:
            sq = sq[::-1]
        gap = r.randint(1, 4)
        v = sq[gap]
        show = ", ".join("☐" if i == gap else str(x) for i, x in enumerate(sq))
        return mcq("Which number goes in the box? <b>%s</b>" % show, v, [v + 1, v - 1, v + step * (1 if back else -1) + (1 if step == 1 else 0), v + 10 if step != 10 else v + 1],
                   "The numbers go %s in %ss: <b>%d</b>." % ("down" if back else "up", step, v))
    if k == "line":
        span = 10 if hi <= 100 else 10
        step = 1 if hi <= 100 else r.choice([1, 10])
        a = r.randint(lo, max(lo, hi - span * step))
        if step == 10:
            a -= a % 10
        pos = r.randint(1, span - 1)
        v = a + pos * step
        marks = {a + i * step: str(a + i * step) for i in (0, span)}
        marks[v] = "?"
        pic = _kp.number_line_svg(a, a + span * step, marks={a + i * step: marks.get(a + i * step, "") for i in range(span + 1)}, sp=34) if step == 1 else None
        if step == 10:
            pic = _kp.number_line_svg(0, span, marks={i: (str(a + i * 10) if i in (0, span) else ("?" if i == pos else "")) for i in range(span + 1)}, sp=40)
        if step == 10:
            pic = pic.replace("number line from 0 to %d" % span, "number line from %d to %d in tens" % (a, a + span * 10))
        return mcq("Which number is at the <b>?</b> on the number line?" + fig(pic), v, [v + step, v - step, a + pos, v + 1 if step == 10 else v + 2],
                   "Count on in %ss from %d: <b>%d</b>." % (step, a, v))
    if k == "name":
        n = r.randint(max(lo, 1), hi)
        if r.random() < 0.5:
            wrong = [x for x in (_near(r, n, 1, hi) + [int(str(n)[::-1]) if n > 10 and n % 10 else n + 3]) if x != n]
            return mcq("Which number is <b>%s</b>?" % _w(n), n, wrong, "%s is written <b>%d</b>." % (_w(n).capitalize(), n))
        right = _w(n)
        alts = [_w(x) for x in _near(r, n, 1, hi)]
        if 13 <= n <= 19:
            alts.insert(0, _w((n - 10) * 10))
        return mcq("How do you write <b>%d</b> in words?" % n, right, alts, "%d is <b>%s</b>." % (n, right))
    if k == "compare":
        a, b = r.sample(range(max(lo, 0), hi + 1), 2)
        if r.random() < 0.5:
            op = "&gt;" if a > b else "&lt;"
            return mcq("Which sign goes in the box? <b>%d ☐ %d</b>" % (a, b), op, ["&lt;" if op == "&gt;" else "&gt;", "=", "+"],
                       "%d is %s than %d, so <b>%d %s %d</b>." % (a, "bigger" if a > b else "smaller", b, a, op, b))
        big = r.random() < 0.5
        c = r.choice([x for x in range(max(lo, 0), hi + 1) if x not in (a, b)])
        nums = [a, b, c]
        v = max(nums) if big else min(nums)
        return mcq("Which number is the %s: %s?" % ("biggest" if big else "smallest", ", ".join(str(x) for x in nums)), v, [x for x in nums if x != v] + [v + 1],
                   "Compare the %s first: <b>%d</b> is the %s." % ("tens" if hi > 20 else "numbers", v, "biggest" if big else "smallest"))
    if k == "order":
        nums = r.sample(range(max(lo, 0), hi + 1), 4)
        up = r.random() < 0.6
        right = ", ".join(str(x) for x in sorted(nums, reverse=not up))
        alts = [", ".join(str(x) for x in sorted(nums, reverse=up)), ", ".join(str(x) for x in nums), ", ".join(str(x) for x in sorted(nums, key=lambda z: str(z)))]
        return mcq("Put these numbers in order from %s: %s" % ("smallest to biggest" if up else "biggest to smallest", ", ".join(str(x) for x in nums)), right, alts + [", ".join(str(x) for x in sorted(nums)[1:] + sorted(nums)[:1])],
                   "<b>%s</b>." % right)
    if k == "pv":
        n = r.randint(max(lo, 11), hi)
        ds = str(n)
        if len(ds) == 2:
            t, o = n // 10, n % 10
            if r.random() < 0.5:
                return mcq("How many tens are in <b>%d</b>?" % n, t, [o, n, t + 1, 10 * t], "%d = %d tens and %d ones: <b>%d tens</b>." % (n, t, o, t), allow_zero=True)
            return mcq("Which is the same as <b>%d</b>?" % n, "%d + %d" % (10 * t, o), ["%d + %d" % (10 * o, t) if o else "%d + %d" % (t, 10), "%d + %d" % (t, o), "%d + %d" % (10 * t + 10, o)],
                       "%d tens and %d ones: <b>%d + %d</b>." % (t, o, 10 * t, o))
        h, t, o = n // 100, (n // 10) % 10, n % 10
        kind = r.choice(["value", "expand", "digit"])
        if kind == "value":
            pos = r.choice([0, 1] if o == 0 else [0, 1, 2])
            dig = int(ds[pos])
            val = dig * (100, 10, 1)[pos]
            if dig == 0:
                raise AssertionError
            return mcq("What is the value of the digit <b>%d</b> in %d?" % (dig, n), val, [dig, dig * 10 if val != dig * 10 else dig * 100, dig * 100 if val != dig * 100 else dig * 1000],
                       "The %d is in the %s place, so it is worth <b>%d</b>." % (dig, ("hundreds", "tens", "ones")[pos], val))
        if kind == "expand":
            right = " + ".join(str(x) for x in (100 * h, 10 * t, o) if x)
            return mcq("Which is the same as <b>%d</b>?" % n, right, ["%d + %d + %d" % (h, t, o), " + ".join(str(x) for x in (100 * h, t, o) if x), " + ".join(str(x) for x in (100 * t if t else 100, 10 * h, o) if x)],
                       "%d = %d hundreds, %d tens and %d ones: <b>%s</b>." % (n, h, t, o, right))
        return mcq("Which number has %d hundreds, %d tens and %d ones?" % (h, t, o), n, [100 * h + t + 10 * o if o != t else n + 10, 100 * o + 10 * t + h if o else n + 100, 100 * h + 10 * t + o + 10], "<b>%d</b>." % n)
    raise AssertionError(k)


def calc_k(r, k, hi, regroup=True):
    if k == "bond":
        tot = r.choice([10, 10, 20] if hi >= 20 else [5, 6, 7, 8, 9, 10])
        a = r.randint(1, tot - 1)
        b = tot - a
        if r.random() < 0.5 and tot <= 10:
            return mcq("How many more dots make 10?" + fig(_kp.tenframe_svg(a)), b, [a, b + 1, b - 1, 10], "%d and <b>%d</b> make 10. Count the empty squares." % (a, b))
        if r.random() < 0.5:
            return mcq("What is the missing part?" + fig(_kp.bond_svg(tot, a, "?")), b, [a, tot, b + 1, b - 1], "%d and <b>%d</b> make %d." % (a, b, tot))
        return mcq("<b>%d + ☐ = %d</b>. What number goes in the box?" % (a, tot), b, [tot + a, b + 1, b - 1, a], "%d and <b>%d</b> make %d." % (a, b, tot))
    if k in ("add", "sub"):
        for _ in range(100):
            a, b = r.randint(1, hi), r.randint(1, hi)
            if k == "add" and a + b <= hi and (regroup or (a % 10 + b % 10 < 10 and (a // 10 % 10) + (b // 10 % 10) < 10)):
                break
            if k == "sub" and a > b and (regroup or (a % 10 >= b % 10 and (a // 10 % 10) >= (b // 10 % 10))):
                break
        else:
            raise AssertionError
        if k == "add":
            v = a + b
            wr = [v + 1, v - 1, v + 10, abs(a - b), v - 10]
            if hi >= 100 and (a % 10 + b % 10) >= 10:
                wr.insert(0, v - 10)
            return mcq("<b>%d + %d = ☐</b>" % (a, b), v, wr, "%s<b>%d</b>." % ("Count on %d from %d: " % (b, a) if b <= 10 and hi <= 20 else "Add the ones, then the tens%s: " % (", then the hundreds" if v >= 100 else ""), v))
        v = a - b
        wr = [v + 1, v - 1, a + b, v + 10]
        if hi >= 100 and a % 10 < b % 10:
            wr.insert(0, int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).zfill(3), str(b).zfill(3)))))
        return mcq("<b>%d − %d = ☐</b>" % (a, b), v, wr, "%s<b>%d</b>." % ("Count back %d from %d: " % (b, a) if b <= 10 and hi <= 20 else "Check: %d + %d = %d. " % (v, b, a), v), allow_zero=False)
    if k == "missing":
        a, c = r.randint(1, hi - 1), r.randint(2, hi)
        if a >= c:
            a, c = c - 1 if c > 1 else 1, c
        b = c - a
        if b <= 0:
            raise AssertionError
        if r.random() < 0.5:
            return mcq("<b>%d + ☐ = %d</b>. What number goes in the box?" % (a, c), b, [a + c, b + 1, b - 1, c], "Think: %d + <b>%d</b> = %d." % (a, b, c))
        return mcq("<b>%d − ☐ = %d</b>. What number goes in the box?" % (c, a), b, [a + c, b + 1, b - 1, a], "Think: %d − <b>%d</b> = %d." % (c, b, a))
    if k == "double":
        n = r.randint(1, hi // 2)
        if r.random() < 0.5:
            return mcq("What is double %d?" % n, 2 * n, [n + 2, 2 * n + 1, 2 * n - 1, n], "Double %d = %d + %d = <b>%d</b>." % (n, n, n, 2 * n))
        return mcq("What is half of %d?" % (2 * n), n, [2 * n, n + 1, n - 1 if n > 1 else n + 2, 4 * n], "%d + %d = %d, so half of %d is <b>%d</b>." % (n, n, 2 * n, 2 * n, n))
    if k == "inverse":
        a, b = r.randint(2, hi // 2), r.randint(2, hi // 2)
        c = a + b
        right = "%d − %d = %d" % (c, b, a)
        return mcq("%d + %d = %d. Which subtraction fact belongs to the same family?" % (a, b, c), right,
                   ["%d − %d = %d" % (a, b, c), "%d − %d = %d" % (b, a, c), "%d + %d = %d" % (c, a, b)],
                   "Start from the total: <b>%s</b>." % right)
    raise AssertionError(k)


_CTX = [("sweets", "eats"), ("marbles", "loses"), ("oranges", "gives away"), ("stickers", "gives away"), ("mielies", "cooks"), ("eggs", "uses"), ("crayons", "loses"), ("beads", "uses"), ("apples", "eats"), ("koeksisters", "eats")]


def story_k(r, k, hi):
    nm, he, his = _nm(r)
    thing, verb = r.choice(_CTX)
    if k == "join":
        a, b = r.randint(2, hi - 2), r.randint(1, hi - 2)
        if a + b > hi:
            raise AssertionError
        if r.random() < 0.5:
            q = "%s has %d %s. %s gets %d more. How many %s does %s have now?" % (nm, a, thing, he.capitalize(), b, thing, he)
        else:
            q = "%s gets %d %s in the morning and %d %s in the afternoon. How many %s is that altogether?" % (nm, a, thing, b, thing, thing)
        return mcq(q, a + b, [abs(a - b), a + b + 1, a + b - 1, a], "Put them together: %d + %d = <b>%d</b>." % (a, b, a + b))
    if k == "take":
        a = r.randint(4, hi)
        b = r.randint(1, a - 1)
        q = "%s has %d %s. %s %s %d. How many %s are left?" % (nm, a, thing, he.capitalize(), verb, b, thing)
        return mcq(q, a - b, [a + b, a - b + 1, a - b - 1, b], "Take away: %d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "compare":
        nm2, he2, _ = _nm(r)
        if nm2 == nm:
            raise AssertionError
        a, b = r.randint(3, hi), r.randint(1, hi)
        if a <= b:
            a, b = b, a
        if a == b:
            raise AssertionError
        q = "%s has %d %s and %s has %d. How many more does %s have?" % (nm, a, thing, nm2, b, nm)
        return mcq(q, a - b, [a + b, a - b + 1, a, b], "Find the difference: %d − %d = <b>%d</b>." % (a, b, a - b))
    if k == "missing":
        a, c = r.randint(2, hi - 2), r.randint(4, hi)
        if a >= c:
            raise AssertionError
        q = "%s had %d %s. After %s got some more, %s had %d. How many did %s get?" % (nm, a, thing, he, he, c, he)
        return mcq(q, c - a, [a + c, c - a + 1, c, a], "%d + ☐ = %d, so %s got <b>%d</b>." % (a, c, he, c - a))
    # two-step
    a, b, c = r.randint(5, hi // 2), r.randint(2, hi // 3), r.randint(1, hi // 4)
    if a + b - c <= 0 or a + b > hi:
        raise AssertionError
    q = "%s has %d %s. %s gets %d more and then %s %d. How many %s does %s have now?" % (nm, a, thing, he.capitalize(), b, verb, c, thing, he)
    v = a + b - c
    return mcq(q, v, [a + b + c, a + b, a - b + c if a - b + c > 0 else v + 2, v + 1], "%d + %d = %d, then %d − %d = <b>%d</b>." % (a, b, a + b, a + b, c, v))


def group_k(r, k, hi, tables=(2, 5, 10)):
    nm, he, his = _nm(r)
    kind = r.choice(_KINDS)
    if k == "groups":
        g, s_ = r.randint(2, 5), r.choice(tables)
        if g * s_ > hi or s_ > 10:
            raise AssertionError
        pic = _kp.groups_svg([(s_, kind)] * g) if s_ <= 6 else None
        q = "There are %d groups of %d %s. How many %s are there altogether?" % (g, s_, _kp.name(kind), _kp.name(kind)) + (fig(pic) if pic else "")
        return mcq(q, g * s_, [g + s_, g * s_ + s_, g * s_ - s_ if g > 2 else g * s_ + 1, s_], "%s = <b>%d</b>." % (" + ".join([str(s_)] * g), g * s_))
    if k == "share":
        p = r.randint(2, 5)
        each = r.randint(2, max(2, hi // p))
        tot = p * each
        if tot > hi:
            raise AssertionError
        q = "%s shares %d %s equally among %d friends. How many does each friend get?" % (nm, tot, _kp.name(kind), p)
        return mcq(q, each, [tot - p, each + 1, each - 1 if each > 1 else each + 2, p], "Share them out one at a time: %d ÷ %d = <b>%d</b> each." % (tot, p, each))
    if k == "array":
        rows, cols = r.randint(2, 5), r.choice([c for c in tables if c <= 6] or [2, 3])
        if rows * cols > hi:
            raise AssertionError
        return mcq("How many %s are in this array?" % _kp.name(kind) + fig(_kp.array_svg(rows, cols, kind)), rows * cols, [rows + cols, rows * cols + cols, rows * cols - 1, rows * cols + 1],
                   "%d rows of %d: <b>%d</b>." % (rows, cols, rows * cols))
    if k == "fact":
        t = r.choice(tables)
        n = r.randint(1, 10)
        if r.random() < 0.65:
            return mcq("<b>%d × %d = ☐</b>" % (n, t), n * t, [n * t + t, n * t - t if n > 1 else t + 1, n + t, n * t + 1], "%d groups of %d: <b>%d</b>." % (n, t, n * t))
        return mcq("<b>%d ÷ %d = ☐</b>" % (n * t, t), n, [n * t - t if n * t - t != n else n + 2, n + 1, n - 1 if n > 1 else n + 2, t], "%d × %d = %d, so %d ÷ %d = <b>%d</b>." % (n, t, n * t, n * t, t, n))
    # grouping with remainder
    s_ = r.choice([2, 3, 4, 5])
    tot = r.randint(s_ + 1, min(hi, 10 * s_))
    g, rem = divmod(tot, s_)
    if rem == 0:
        raise AssertionError
    q = "%s puts %d %s into bags of %d. How many full bags can %s make, and how many are left over?" % (nm, tot, _kp.name(kind), s_, he)
    bg = lambda n: "%d bag%s" % (n, "" if n == 1 else "s")
    right = "%s, %d left over" % (bg(g), rem)
    return mcq(q, right, ["%s, 0 left over" % bg(g + 1), "%s, %d left over" % (bg(g), rem + 1), "%s, %d left over" % (bg(g - 1 if g > 1 else g + 2), rem + s_ if g > 1 else rem)],
               "%d = %d × %d + %d: <b>%s</b>." % (tot, g, s_, rem, right))


_MK = {}


def F(fun, k, *a, **kw):
    key = (fun.__name__, k, a, tuple(sorted(kw.items())))
    if key not in _MK:
        seen = set()
        def g(r):
            it = fun(r, k, *a, **kw)
            if it["q"] in seen:
                raise AssertionError("repeat")
            seen.add(it["q"])
            return it
        g.__name__ = "%s_%s" % (fun.__name__, k)
        _MK[key] = g
    return _MK[key]


def build():
    sets, R = build_sets([
        ("Read the map", [("run", aum.set_read, ("rnd", aum.People), 20, nomoney)]),
        ("Compass directions", [("run", aum.set_compass, ("rnd", aum.People), 20, nomoney)]),
        ("Directions", [("run", aum.set_directions, ("rnd", aum.People), 20, nomoney)]),
        ("Grid references and views", [("run", aum.set_birdseye_refs, ("rnd", aum.People), 20, nomoney)]),
        ("Maps in real life", [("run", aum.set_real, ("rnd", aum.People), 20, both(nomoney, nozoo))]),
    ], 80313)
    finish(sets, R)
    body = lesson("<ul><li>Grid references: read across first (the letter), then up (the number).</li><li>North is usually at the top of a map; south at the bottom, east on the right, west on the left.</li><li>A bird's-eye view shows a place from above.</li><li>Count each square you move, not the one you start on.</li></ul>",
        [example("Start at B2, move 2 squares east", ["B → C → D"], "D2")],
        [['Row first', 'Across first, then up.'], ['East or west', 'East is on the right.'], ['The start square', 'Do not count it.']])
    faq = [('What is the Foundation Phase?', 'Grade R to Grade 3 in South African schools. Grade 3 is the last year; learners are about 8 to 9 years old.'), ('What maps do Grade 3 learners read?', 'Simple maps of the classroom, the school and the area, with a grid.'), ("What is a bird's-eye view?", 'A view from above.'), ('Where is east?', 'On the right of a map with north at the top.')]
    make('position-and-maps', 13, 'Space and Shape (Geometry)', 'Grade 3: Position, orientation and views',
         'Position, orientation and views: read, interpret and draw informal maps or top views of a collection of objects; find objects on a map; describe position and give directions.',
         'Position, Directions and Maps', 'Position and Maps',
         "Free CAPS Grade 3 maths worksheets: maps, grid references, compass directions and bird's-eye views. 100 questions with pictures and memos.",
         'Across first, then up.', 'East is on the right.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
