# -*- coding: utf-8 -*-
"""
CA Grade 4 Math: Money and Financial Literacy (Ontario Curriculum 2020, Financial Literacy F1)
  python3 tools/gen_caon_math_g4_money.py
F1.1 ways to pay (cash, debit, credit, gift cards), F1.2 total cost of several items priced in whole dollars
(no sales tax) and the change from a cash payment, using mental math, F1.3 spending, saving, earning,
investing and donating, and good value / best buys.
All prices are whole dollars (int), so every total, change and typical mistake is exact.
Counting up for change: price -> next $10 -> money paid. No sales tax in Grade 4.
Bill drawing copied from gen_cabc_math_g4_money.py; mcq/balance/People from gen_caon_math_g6_financial.py.
HTML attributes use single quotes (no backslashes in the JSON).
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "ca-on", "math", "grade-4")
UPDATED = "2026-11-02"
GREEN = "#006633"
INK = "#2b2b2b"
PAPER = "#fffdf5"
EDGE = "#b8b0a0"
FONT = "Arial, Helvetica, sans-serif"
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]

BILL = {5: ("#c4dcf2", "#1f5f99"), 10: ("#ddcbee", "#5b2d8a"), 20: ("#cbe7c4", "#2f7a2a"),
        50: ("#f5c6c6", "#a32020"), 100: ("#e8d6c2", "#7a4a1c")}
BILL_W, BILL_H = 80, 42


# ------------------------------------------------------------ money
def m(n):
    """whole dollars: 13 -> '$13'"""
    assert isinstance(n, int) and 0 < n < 10000, n
    return "$%d" % n


def mval(s):
    s = re.sub(r"<[^>]+>", "", str(s))
    mm = re.fullmatch(r"\$(\d+)", s)
    return int(mm.group(1)) if mm else None


def cap(s):
    return s[0].upper() + s[1:]


def no_carry(nums):
    """column addition that never carries: each column writes only its ones digit, the last column its full sum"""
    out, place = 0, 1
    k = max(len(str(n)) for n in nums)
    for i in range(k):
        col = sum((n // 10 ** i) % 10 for n in nums)
        out += (col if i == k - 1 else col % 10) * place
        place *= 10
    return out


def small_from_big(a, b):
    """column subtraction taking the smaller digit from the bigger one"""
    k = len(str(a))
    da = [(a // 10 ** i) % 10 for i in range(k)]
    db = [(b // 10 ** i) % 10 for i in range(k)]
    return sum(abs(x - y) * 10 ** i for i, (x, y) in enumerate(zip(da, db)))


def next10(p):
    return p if p % 10 == 0 else p + 10 - p % 10


def count_up(price, paid):
    """Count up from $37 to $50: $37 + $3 = $40, $40 + $10 = $50. $3 + $10 = $13."""
    n = next10(price)
    ch = paid - price
    if n == price or n == paid:
        return "Count up from %s to %s: %s + %s = %s. The change is <b>%s</b>." % (m(price), m(paid), m(price), m(ch), m(paid), m(ch))
    return ("Count up from %s to %s: %s + %s = %s, then %s + %s = %s. Add the jumps: %s + %s = <b>%s</b>."
            % (m(price), m(paid), m(price), m(n - price), m(n), m(n), m(paid - n), m(paid), m(n - price), m(paid - n), m(ch)))


def change_cands(price, paid):
    """real mistakes when finding change, most common first"""
    r = paid - price
    n = next10(price)
    c = [price + paid,                      # added instead of subtracting
         small_from_big(paid, price),        # $50 − $37: 7 − 0 = 7 and 5 − 3 = 2 gives $27
         r + 10, r - 10,                     # counted one $10 jump too many / too few
         paid - n if n not in (price, paid) else None,   # forgot the first jump to the next $10
         r + 1, r - 1, price]
    return [x for x in c if x and 0 < x < 10000 and x != r]


def sum_cands(nums):
    t = sum(nums)
    c = [no_carry(nums), t - min(nums), t + 10, t - 10, t - max(nums)]
    return [x for x in c if x and x > 0 and x != t]


# ------------------------------------------------------------ helpers
def mcq(q, correct, cands, e, fmt=m):
    """4 choices: correct + the first 3 usable unique distractors (never equal in value)."""
    correct = fmt(correct) if isinstance(correct, int) else str(correct)
    seen_t, seen_v = {correct}, {mval(correct)} - {None}
    pick = []
    for c in cands:
        if c is None:
            continue
        if isinstance(c, int):
            if c <= 0:
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


def balance(sets, rnd):
    """Spread the correct answers evenly (5/5/5/5) over the 4 positions in every set."""
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


def mark_large(u, pattern):
    rx = re.compile(r"<svg (?=[^>]*aria-label='" + pattern + ")")
    for s in u["sets"]:
        for it in s["items"]:
            it["q"] = rx.sub("<svg data-pf='lg' ", it["q"])
    return u


# ------------------------------------------------------------ pictures
def tags_svg(items):
    """price tags side by side: [('Backpack', 27), ...]"""
    gap, pad, h = 10, 4, 70
    ws = [max(int(len(n) * 9.5) + 24, 92) for n, p in items]
    W = sum(ws) + gap * (len(ws) - 1) + 2 * pad
    b, x = [], pad
    for (n, p), w in zip(items, ws):
        b.append("<rect x='%d' y='%d' width='%d' height='%d' rx='8' fill='%s' stroke='%s' stroke-width='2'/>" % (x, pad, w, h, PAPER, EDGE))
        b.append("<path d='M%d %d V%d a8 8 0 0 1 8 -8 H%d a8 8 0 0 1 8 8 V%d Z' fill='%s'/>"
                 % (x, pad + 30, pad + 8, x + w - 8, pad + 30, GREEN))
        b.append(text(x + w / 2, pad + 22, n, 16, col="#ffffff"))
        b.append(text(x + w / 2, pad + 60, m(p), 24))
        x += w + gap
    label = "price tags: " + ", ".join("%s %s" % (n, m(p)) for n, p in items)
    return svg_wrap(W, h + 2 * pad, "".join(b), label)


def change_line(price, paid, show=True):
    """empty number line (not to scale) for counting up: price -> next $10 -> paid"""
    n = next10(price)
    pts = [price] + ([n] if n not in (price, paid) else []) + [paid]
    seg = [120, 170][:len(pts) - 1]
    x0, y0 = 40, 70
    xs = [x0]
    for d in seg:
        xs.append(xs[-1] + d)
    W, H = xs[-1] + 40, 102
    b = ["<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x0 - 22, y0, xs[-1] + 22, y0, INK)]
    for x, p in zip(xs, pts):
        b.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2'/>" % (x, y0 - 7, x, y0 + 7, INK))
        b.append(text(x, y0 + 27, m(p), 17))
    for i in range(len(pts) - 1):
        a, c = xs[i], xs[i + 1]
        mid = (a + c) / 2
        b.append("<path d='M%d %d Q%.1f %d %d %d' fill='none' stroke='%s' stroke-width='2'/>" % (a + 3, y0 - 8, mid, y0 - 52, c - 3, y0 - 8, GREEN))
        b.append(text(mid, y0 - 34, ("+" + m(pts[i + 1] - pts[i])) if show else "+ ?", 17, col=GREEN))
    return svg_wrap(W, H, "".join(b), "counting up from %s to %s" % (m(price), m(paid)))


def jars_svg(jars, title=None):
    """money jars: [('Spend', 12), ('Save', None), ...]; None prints ?"""
    jw, jh, gap, pad = 92, 96, 14, 4
    top = 26 if title else 0
    W = len(jars) * jw + (len(jars) - 1) * gap + 2 * pad
    H = top + jh + 30 + 2 * pad
    b = []
    if title:
        b.append(text(W / 2, pad + 18, title, 17))
    for i, (lab_, amt) in enumerate(jars):
        x = pad + i * (jw + gap)
        y = pad + top
        b.append("<rect x='%d' y='%d' width='%d' height='14' rx='3' fill='%s'/>" % (x + 14, y, jw - 28, GREEN))
        b.append("<path d='M%d %d H%d Q%d %d %d %d V%d Q%d %d %d %d H%d Q%d %d %d %d V%d Q%d %d %d %d Z' fill='#eef6f1' stroke='%s' stroke-width='2'/>"
                 % (x + 18, y + 14, x + jw - 18, x + jw - 6, y + 14, x + jw - 6, y + 28, y + jh - 10, x + jw - 6, y + jh,
                    x + jw - 16, y + jh, x + 16, x + 6, y + jh, x + 6, y + jh - 10, y + 28, x + 6, y + 14, x + 18, y + 14, INK))
        b.append(text(x + jw / 2, y + 66, "?" if amt is None else m(amt), 24, col=GREEN))
        b.append(text(x + jw / 2, y + jh + 22, lab_, 17))
    label = "money jars: " + ", ".join("%s %s" % (l, "unknown" if a is None else m(a)) for l, a in jars)
    return svg_wrap(W, H, "".join(b), label)


def gift_card_svg(store, amount):
    W, H = 210, 124
    b = ["<rect x='3' y='3' width='%d' height='%d' rx='12' fill='%s' stroke='%s' stroke-width='2'/>" % (W - 6, H - 6, GREEN, INK),
         "<rect x='3' y='88' width='%d' height='14' fill='#0b4d2a'/>" % (W - 6),
         text(18, 32, "GIFT CARD", 17, "start", "#ffffff"),
         text(18, 56, store, 15, "start", "#ffffff", bold=False),
         text(W - 18, 80, m(amount), 28, "end", "#ffffff")]
    return svg_wrap(W, H, "".join(b), "gift card for %s with %s on it" % (store, m(amount)))


def draw_bill(v, cx, cy):
    fill, edge = BILL[v]
    x, y = cx - BILL_W / 2, cy - BILL_H / 2
    return ("<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='4' fill='%s' stroke='%s' stroke-width='2'/>"
            "<rect x='%.1f' y='%.1f' width='%d' height='%d' rx='2' fill='none' stroke='%s' stroke-width='1'/>"
            % (x, y, BILL_W, BILL_H, fill, edge, x + 5, y + 5, BILL_W - 10, BILL_H - 10, edge)
            + text(cx, cy + 7, m(v), 20, col=edge))


def bills_svg(vals):
    gap, pad = 8, 4
    W = len(vals) * BILL_W + (len(vals) - 1) * gap + 2 * pad
    H = BILL_H + 2 * pad
    b = [draw_bill(v, pad + i * (BILL_W + gap) + BILL_W / 2, pad + BILL_H / 2) for i, v in enumerate(vals)]
    return svg_wrap(W, H, "".join(b), "bills: " + ", ".join(m(v) for v in vals))


# ============================================================ set 1: ways to pay
CASH, DEBIT, CREDIT, GIFT = "Cash", "Debit card", "Credit card", "Gift card"
METHODS = [CASH, DEBIT, CREDIT, GIFT]


def which(q, ans, e):
    return mcq(q, ans, [x for x in METHODS if x != ans], e, fmt=str)


def set_pay(P):
    its = []
    its.append(mcq("Which of these is cash?", "Coins and bills", ["A debit card", "A credit card", "A gift card"],
                   "<b>Cash</b> is money you can hold: coins (nickels, dimes, quarters, loonies, toonies) and bills.", fmt=str))
    its.append(which("Which way to pay takes the money straight out of your own bank account?", DEBIT,
                     "A <b>debit card</b> takes the money right away from your bank account. You can only spend money that is in the account."))
    its.append(which("Which way to pay means you borrow the money now and pay a bill later?", CREDIT,
                     "With a <b>credit card</b>, the card company pays the store. You get a bill later and must pay it back."))
    its.append(which("Which way to pay has a set amount of money on it and is often given as a present?", GIFT,
                     "A <b>gift card</b> is loaded with a set amount, such as $25. Each time you buy something, that amount goes down."))
    its.append(which("Which way to pay is the only one you can hand to a friend at a lemonade stand that has no card machine?", CASH,
                     "A card needs a card machine or a website. <b>Cash</b> can be paid anywhere, even at a lemonade stand."))
    its.append(which("Which way to pay cannot be used to buy something from an online store?", CASH,
                     "You cannot hand coins and bills over the internet. Online stores need a card, so <b>cash</b> does not work."))
    n, he, his = P.next()
    its.append(mcq("%s gets a gift card for a bookstore. Where can %s use it?" % (n, he), "At that bookstore",
                   ["At any store", "At a bank, to get cash", "At any website"],
                   "Most gift cards work only at the store that sold them, so %s can use it <b>at that bookstore</b>." % he, fmt=str))
    its.append(mcq("Which of these is NOT a way to pay?", "A library card", ["Cash", "A debit card", "A gift card"],
                   "A <b>library card</b> lets you borrow books for free. It has no money on it, so you cannot pay with it.", fmt=str))
    its.append(mcq("You pay for a $13 book with a debit card. What happens?", "$13 leaves your bank account",
                   ["$20 leaves your bank account", "You get $7 change in coins", "You get a bill to pay later"],
                   "Debit takes the <b>exact price, $13</b>, from your bank account. There is no change, because no cash was handed over.", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s’s grandma pays for a $60 bike helmet with her credit card. Is the helmet free?" % n,
                   "No, she pays the bill later", ["Yes, the card pays for it", "Yes, if she keeps the receipt", "No, the store pays for it"],
                   "A credit card <b>borrows</b> the money. Grandma gets a bill and must pay the $60 back, so <b>it is not free</b>.", fmt=str))
    its.append(mcq("What is one risk of using a credit card?", "Spending more than you can pay back",
                   ["It only works at one store", "It runs out after one use", "You cannot see the price"],
                   "It is easy to buy lots of things and forget it is borrowed money. If you <b>spend more than you can pay back</b>, you owe money and extra fees.", fmt=str))
    its.append(mcq("What is one good reason to pay with cash?", "You can see how much you have left",
                   ["You can shop online", "It can never be lost", "You pay for it later"],
                   "With cash in your wallet, <b>you can see how much is left</b>, so it is hard to overspend. But cash can be lost, and it does not work online.", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s’s debit card is linked to a bank account with $40 in it. Can %s buy a $55 jacket with only that card?" % (n, he),
                   "No, %s is $15 short" % he, ["Yes, with $15 left", "No, %s is $95 short" % he, "Yes, with $0 left"],
                   "Debit can only spend what is in the account. $55 − $40 = $15, so <b>%s is $15 short</b>. ($95 adds instead of subtracting.)" % he, fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s pays for a $7 lunch with a $10 bill. Does %s get change?" % (n, he), "Yes, $3",
                   ["No change", "Yes, $17", "Yes, $7"],
                   "Cash paid is more than the price, so there is change. Count up: $7 + $3 = $10. <b>$3</b> change. ($17 adds instead of subtracting.)", fmt=str))
    n, he, his = P.next()
    its.append(mcq(fig(gift_card_svg("Book Nook", 25)) + "%s buys a $9 puzzle with this gift card. How much is left on the card?" % n,
                   16, [34, 26, 15, 9],
                   "Count up from $9 to $25: $9 + $1 = $10, $10 + $15 = $25. $1 + $15 = <b>$16</b> is left. ($34 adds instead of subtracting.)"))
    n, he, his = P.next()
    its.append(mcq(fig(gift_card_svg("Sports Corner", 30)) + "%s has this gift card. %s wants a $36 hockey stick. What can %s do?" % (n, cap(he), he),
                   "Pay $6 more another way", ["Get $6 change", "Pay $36 more", "Use only the card"],
                   "The card covers $30. $36 − $30 = $6, so %s must <b>pay $6 more</b> with cash or a debit card." % he, fmt=str))
    n, he, his = P.next()
    assert 23 - 20 == 3
    its.append(mcq("%s has a $20 gift card for a toy store and $5 in cash. %s buys a $23 game. How much cash does %s use?" % (n, cap(he), he),
                   3, [43, 18, 5],
                   "The gift card pays $20 first. $23 − $20 = <b>$3</b> is paid in cash. ($43 adds the card and the price.)"))
    its.append(mcq("A family spends $200 at the grocery store. Why might they pay with debit instead of cash?",
                   "They do not need to carry lots of bills", ["Food costs less with debit", "Debit money never runs out", "The store gives free change"],
                   "Paying $200 in cash means carrying many bills, which could be lost. With debit, <b>they do not need to carry the bills</b>. The price is the same either way.", fmt=str))
    its.append(mcq("Which way to pay can lead to extra fees, called interest, if the bill is not paid on time?", CREDIT,
                   [CASH, DEBIT, GIFT],
                   "A <b>credit card</b> is borrowed money. If you do not pay the bill on time, the card company adds interest, so you pay back more than you spent.", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s taps %s phone to pay. The phone is linked to %s debit card. Where does the money come from?" % (n, his, his),
                   "%s bank account" % cap(his), ["The phone company", "A loan to pay back later", "The store"],
                   "The phone works like the debit card it is linked to, so the money comes from <b>%s bank account</b>." % his, fmt=str))
    assert len(its) == 20
    return {"title": "Ways to pay: cash, debit, credit and gift cards", "items": its}


# ============================================================ set 2: total cost
def set_total(P):
    its = []

    def add(q, nums, e, extra=None):
        t = sum(nums)
        its.append(mcq(q, t, (extra or []) + sum_cands(nums), e))

    add(fig(tags_svg([("Ball", 8), ("Pump", 6)])) + "What is the total for the ball and the pump?", [8, 6],
        "$8 + $6: make a ten. $8 + $2 = $10, then $4 more. Total: <b>$14</b>.", [2, 13, 15])
    add(fig(tags_svg([("Paint set", 12), ("Brushes", 7)])) + "What is the total for the paint set and the brushes?", [12, 7],
        "$12 + $7 = <b>$19</b>. Add the ones: 2 + 7 = 9.", [5])
    add(fig(tags_svg([("Mitts", 15), ("Hat", 13)])) + "What do the mitts and the hat cost together?", [15, 13],
        "Add the tens: $10 + $10 = $20. Add the ones: $5 + $3 = $8. Total: <b>$28</b>.", [2])
    n, he, his = P.next()
    add("%s buys a $26 book and a $15 calendar. What is the total cost?" % n, [26, 15],
        "$26 + $15: $26 + $10 = $36, then $36 + $5 = <b>$41</b>. ($31 forgets to regroup the 11 ones.)")
    n, he, his = P.next()
    add("%s buys a $19 lunch box and a $24 water bottle. What is the total?" % n, [19, 24],
        "$19 is $1 less than $20. $20 + $24 = $44, then take away the $1: <b>$43</b>. ($44 forgets to take the $1 back.)", [44])
    n, he, his = P.next()
    add(fig(tags_svg([("Pencils", 4), ("Eraser", 2), ("Ruler", 3)])) + "%s buys the pencils, the eraser and the ruler. What is the total?" % n,
        [4, 2, 3], "$4 + $2 + $3 = <b>$9</b>. Check that all three prices are added.")
    n, he, his = P.next()
    assert 3 * 7 == 21
    its.append(mcq("%s buys 3 skipping ropes at $7 each. What is the total cost?" % n, 21, [10, 14, 28, 24],
                   "3 × $7 = <b>$21</b>. Or add: $7 + $7 + $7 = $21. ($10 adds 3 + 7 instead of multiplying.)"))
    n, he, his = P.next()
    add("%s buys a $35 sweater and a $48 pair of jeans. What is the total cost?" % n, [35, 48],
        "$35 + $48: $35 + $50 = $85, then take away $2: <b>$83</b>. ($73 forgets to regroup 13 ones as 1 ten.)")
    add(fig(tags_svg([("Puck", 8), ("Tape", 5), ("Socks", 12)])) + "What is the total for all three items?", [8, 5, 12],
        "Add numbers that make a ten first: $8 + $12 = $20. Then $20 + $5 = <b>$25</b>.")
    n, he, his = P.next()
    assert 4 * 9 == 36
    its.append(mcq("%s buys 4 tickets to a hockey game at $9 each. What is the total cost?" % n, 36, [13, 27, 45, 32],
                   "4 × $9 = <b>$36</b>. Or think 4 × $10 = $40, then take away 4 × $1 = $4: $36. ($13 adds 4 + 9.)"))
    n, he, his = P.next()
    assert 2 * 14 + 9 == 37
    its.append(mcq("%s buys 2 T-shirts at $14 each and a cap for $9. What is the total?" % n, 37, [23, 28, 47, 36],
                   "T-shirts: 2 × $14 = $28. Add the cap: $28 + $9 = <b>$37</b>. ($23 counts only one T-shirt.)"))
    add(fig(tags_svg([("Tent", 89), ("Lantern", 23)])) + "A family buys the tent and the lantern for a canoe trip. What is the total?", [89, 23],
        "$89 is $1 less than $90. $90 + $23 = $113, then take away $1: <b>$112</b>. ($102 forgets to regroup.)")
    n, he, his = P.next()
    add("At the school book fair, %s buys books for $6, $11 and $14. What is the total?" % n, [6, 11, 14],
        "$6 + $14 = $20 (a ten pair). $20 + $11 = <b>$31</b>.")
    n, he, his = P.next()
    add("%s buys a $125 bike and a $38 helmet. What is the total cost?" % n, [125, 38],
        "$125 + $38: $125 + $30 = $155, then $155 + $8 = <b>$163</b>. ($153 forgets to regroup the 13 ones.)")
    # estimation
    its.append(mcq(fig(tags_svg([("Boots", 38), ("Jacket", 61)])) + "About how much do the boots and the jacket cost together? Round each price to the nearest $10.",
                   100, [90, 110, 99],
                   "$38 rounds to $40. $61 rounds to $60. $40 + $60 = <b>about $100</b>. ($99 is the exact total, not the estimate.)"))
    n, he, his = P.next()
    assert 22 + 29 + 18 == 69
    its.append(mcq("%s has $60. %s wants items that cost $22, $29 and $18. Round to the nearest $10 to estimate. Is $60 enough?" % (n, cap(he)),
                   "No, it is about $70", ["Yes, it is about $60", "Yes, it is about $50", "No, it is about $80"],
                   "$22 → $20, $29 → $30, $18 → $20. $20 + $30 + $20 = $70, so <b>no, it is about $70</b>. The exact total is $69, more than $60."
                   , fmt=str))
    n, he, his = P.next()
    add("For a class party, %s’s teacher buys juice for $17, fruit for $23 and cups for $8. What is the total?" % n, [17, 23, 8],
        "$17 + $23 = $40 (7 + 3 makes a ten). $40 + $8 = <b>$48</b>. ($38 forgets to regroup the ten.)")
    n, he, his = P.next()
    assert 5 * 12 == 60
    its.append(mcq("%s buys 5 packs of hockey cards at $12 a pack. What is the total cost?" % n, 60, [17, 50, 72, 55],
                   "5 × $12 = 5 × $10 + 5 × $2 = $50 + $10 = <b>$60</b>. ($50 forgets the 5 × $2.)"))
    add(fig(tags_svg([("Skates", 149), ("Helmet", 56), ("Stick", 45)])) + "A family buys the skates, the helmet and the stick. What is the total?",
        [149, 56, 45], "$56 + $45 = $101 (or $55 + $45 = $100, plus $1). $149 + $101 = <b>$250</b>. ($240 forgets a regrouped ten.)", [240])
    n, he, his = P.next()
    assert 2 * 18 + 2 * 7 == 50
    its.append(mcq("%s buys 2 movie tickets at $18 each and 2 drinks at $7 each. What is the total?" % n, 50, [25, 43, 36, 60],
                   "Tickets: 2 × $18 = $36. Drinks: 2 × $7 = $14. $36 + $14 = <b>$50</b>. ($25 counts only one ticket and one drink.)"))
    assert len(its) == 20
    return {"title": "Total cost of several items", "items": its}


# ============================================================ set 3: change by counting up
def set_change(P):
    its = []

    def ch(q, price, paid, extra_e="", line=False, show=True):
        if line:
            q = fig(change_line(price, paid, show)) + q
        its.append(mcq(q, paid - price, change_cands(price, paid), count_up(price, paid) + extra_e))

    n, he, his = P.next()
    ch("%s buys a $7 book and pays with a $10 bill. How much change does %s get?" % (n, he), 7, 10)
    n, he, his = P.next()
    ch("%s buys a $16 puzzle and pays with a $20 bill. How much change does %s get?" % (n, he), 16, 20,
       " Check: $16 + $4 = $20.")
    ch("Use the number line. A toy costs $12. You pay with a $20 bill. How much change do you get?", 12, 20, line=True, show=False)
    n, he, his = P.next()
    ch("%s buys a $9 kite and pays with a $20 bill. How much change does %s get?" % (n, he), 9, 20,
       " ($29 adds instead of subtracting.)")
    n, he, his = P.next()
    ch("%s buys a $13 book about loons and pays with a $20 bill. How much change does %s get?" % (n, he), 13, 20)
    ch("Use the number line. Shin pads cost $34. You pay with a $50 bill. How much change do you get?", 34, 50, line=True, show=False)
    n, he, his = P.next()
    ch("%s buys a $37 sweater and pays with a $50 bill. How much change does %s get?" % (n, he), 37, 50,
       " ($27 comes from 7 − 0 = 7 and 5 − 3 = 2: you cannot take 7 from 0, so regroup or count up.)")
    n, he, his = P.next()
    ch("%s buys a $26 board game and pays with a $50 bill. How much change does %s get?" % (n, he), 26, 50)
    n, he, his = P.next()
    ch("%s buys a $41 soccer ball and pays with a $50 bill. How much change does %s get?" % (n, he), 41, 50)
    n, he, his = P.next()
    ch("%s buys an $18 pair of mitts and pays with a $50 bill. How much change does %s get?" % (n, he), 18, 50,
       " Check: $18 + $32 = $50.")
    ch("Use the number line. A hockey jersey costs $62. You pay with a $100 bill. How much change do you get?", 62, 100, line=True, show=False)
    n, he, his = P.next()
    ch("%s buys a $45 backpack and pays with a $100 bill. How much change does %s get?" % (n, he), 45, 100)
    n, he, his = P.next()
    ch("%s buys a $78 pair of skates and pays with a $100 bill. How much change does %s get?" % (n, he), 78, 100,
       " Check: $78 + $22 = $100.")
    n, he, his = P.next()
    ch(fig(bills_svg([20, 20, 10])) + "%s pays for a $43 jacket with these bills. How much change does %s get?" % (n, he), 43, 50,
       " The bills make $20 + $20 + $10 = $50.")
    n, he, his = P.next()
    ch(fig(bills_svg([50, 20, 20, 10])) + "%s pays for an $87 tent with these bills. How much change does %s get?" % (n, he), 87, 100,
       " The bills make $50 + $20 + $20 + $10 = $100.")
    # which counting up is right
    its.append(mcq("Which shows the right way to count up from $37 to $50?", "$3 + $10 = $13",
                   ["$3 + $20 = $23", "$7 + $10 = $17", "$3 + $10 = $14"],
                   "$37 + $3 = $40 (the next ten). $40 + $10 = $50. So <b>$3 + $10 = $13</b>. ($7 is how far $37 is from $30, the wrong way.)", fmt=str))
    # missing price
    n, he, his = P.next()
    its.append(mcq("%s pays with a $50 bill and gets $14 in change. What was the price?" % n, 36, [64, 46, 34],
                   "Price + change = money paid. $50 − $14: count up from $14 to $50. $14 + $6 = $20, $20 + $30 = $50, so $36. "
                   "Check: $36 + $14 = $50. The price was <b>$36</b>. ($64 adds instead of subtracting.)"))
    # two items then change
    n, he, his = P.next()
    assert 12 + 5 == 17 and 20 - 17 == 3
    its.append(mcq("%s buys a $12 book and a $5 bookmark. %s pays with a $20 bill. How much change does %s get?" % (n, cap(he), he),
                   3, [8, 15, 37, 13],
                   "Total: $12 + $5 = $17. Count up from $17 to $20: <b>$3</b>. ($8 forgets the bookmark; $15 forgets the book.)"))
    n, he, his = P.next()
    assert 24 + 19 == 43 and 50 - 43 == 7
    its.append(mcq("%s buys a $24 ball and a $19 pump. %s pays with a $50 bill. How much change does %s get?" % (n, cap(he), he),
                   7, [26, 31, 17, 93],
                   "Total: $24 + $19 = $43. Count up: $43 + $7 = $50. Change: <b>$7</b>. ($17 adds $24 + $19 as $33.)"))
    n, he, his = P.next()
    assert 3 * 15 + 28 == 73 and 100 - 73 == 27
    its.append(mcq("%s buys 3 books at $15 each and a $28 lamp. %s pays with a $100 bill. How much change does %s get?" % (n, cap(he), he),
                   27, [57, 37, 72, 85],
                   "Books: 3 × $15 = $45. Total: $45 + $28 = $73. Count up: $73 + $7 = $80, $80 + $20 = $100. $7 + $20 = <b>$27</b>. "
                   "($57 counts only one book.)"))
    assert len(its) == 20
    return {"title": "Change from $20, $50 and $100 by counting up", "items": its}


# ============================================================ set 4: spending, saving, earning, investing, donating
def set_choices(P):
    its = []
    its.append(mcq("What does earning money mean?", "Getting paid for work you do",
                   ["Putting money in a piggy bank", "Giving money to help others", "Buying something you want"],
                   "<b>Earning</b> is getting money for work, like raking leaves or shovelling snow. The others are saving, donating and spending.", fmt=str))
    its.append(mcq("Which is an example of donating?", "Giving $5 to a food bank",
                   ["Buying a $5 snack", "Putting $5 in a piggy bank", "Getting $5 for chores"],
                   "<b>Donating</b> means giving money to help others, like <b>a food bank</b> or the Terry Fox Run.", fmt=str))
    its.append(mcq("Which is an example of saving?", "Keeping $10 to buy a bike later",
                   ["Spending $10 on a movie", "Giving $10 to a charity", "Earning $10 for walking a dog"],
                   "<b>Saving</b> is keeping money now so you can use it later, like <b>for a bike</b>.", fmt=str))
    its.append(mcq("Which is an example of investing?", "Putting money where it can grow",
                   ["Hiding money under a bed", "Buying a new game", "Losing a loonie"],
                   "<b>Investing</b> is putting money in a place where it can grow over time, like a bank account that pays interest. "
                   "Money under a bed does not grow.", fmt=str))
    its.append(mcq("Which is a need, not a want?", "Warm winter boots",
                   ["A new video game", "A second hockey jersey", "Concert tickets"],
                   "A <b>need</b> is something you must have to be safe and healthy. In a Canadian winter, <b>warm boots</b> are a need. The others are wants.", fmt=str))
    n, he, his = P.next()
    its.append(mcq("If %s spends more of %s allowance each week, what happens to %s savings?" % (n, his, his),
                   "%s saves less" % cap(he), ["%s saves more" % cap(he), "Nothing changes", "%s earns more" % cap(he)],
                   "Spending and saving come from the same money. If %s spends more, there is less left, so <b>%s saves less</b>." % (n, he), fmt=str))
    its.append(mcq("Before buying something, which is the best question to ask?", "Do I need it or want it?",
                   ["Is the box a nice colour?", "Will my friend like it?", "Is it the biggest one?"],
                   "Asking <b>“Do I need it or want it?”</b> helps you decide if it is worth the money.", fmt=str))
    n, he, his = P.next()
    its.append(mcq(fig(jars_svg([("Spend", 12), ("Save", None), ("Donate", 3)], "%s earned $30" % n)) +
                   "%s earned $30. %s puts $12 in the Spend jar and $3 in the Donate jar. The rest goes in the Save jar. How much is saved?" % (n, cap(he)),
                   15, [45, 18, 27, 9],
                   "Spend and donate: $12 + $3 = $15. Save: $30 − $15 = <b>$15</b>. ($45 adds everything instead of subtracting.)"))
    n, he, his = P.next()
    its.append(mcq("%s earns $5 each week for doing chores. How much does %s earn in 6 weeks?" % (n, he), 30, [11, 35, 25, 56],
                   "6 × $5 = <b>$30</b>. ($11 adds 6 + 5.)"))
    n, he, his = P.next()
    its.append(mcq("%s rakes leaves for 4 neighbours. Each one pays $6. How much does %s earn?" % (n, he), 24, [10, 18, 30, 64],
                   "4 × $6 = <b>$24</b>. ($10 adds 4 + 6.)"))
    n, he, his = P.next()
    its.append(mcq("%s gets $20 for %s birthday. %s saves half and donates $2. How much can %s spend?" % (n, his, cap(he), he),
                   8, [10, 18, 12, 2],
                   "Half of $20 is $10 saved. $20 − $10 = $10 left. Donate $2: $10 − $2 = <b>$8</b> to spend. ($10 forgets the donation.)"))
    n, he, his = P.next()
    its.append(mcq("%s saves $4 each week. How many weeks will it take to save $28?" % n, "7 weeks",
                   ["24 weeks", "32 weeks", "8 weeks"],
                   "Count by 4s to 28: 4, 8, 12, 16, 20, 24, 28. That is 7 jumps, so <b>7 weeks</b>. (28 ÷ 4 = 7. "
                   "24 weeks comes from $28 − $4.)", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s has $15 saved. %s wants a $45 skateboard and saves $5 each week. How many more weeks until %s can buy it?" % (n, cap(he), he),
                   "6 weeks", ["9 weeks", "3 weeks", "30 weeks"],
                   "Still needed: $45 − $15 = $30. $30 ÷ $5 = <b>6 weeks</b>. (9 weeks forgets the $15 already saved.)", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s puts $100 in a savings account. After a year, the bank adds $2 interest. How much is in the account now?" % n,
                   102, [98, 200, 120],
                   "Interest is money the bank adds to your savings. $100 + $2 = <b>$102</b>. This is how saving in a bank helps money grow."))
    its.append(mcq("A Grade 4 class raises $86 at a bake sale and $47 at a car wash. They donate it all to the food bank. How much do they donate?",
                   133, [123, 39, 143, 113],
                   "$86 + $47: $86 + $40 = $126, then $126 + $7 = <b>$133</b>. ($123 forgets to regroup the 13 ones; $39 subtracts.)"))
    n, he, his = P.next()
    its.append(mcq("%s has $50. %s spends $18 on a hockey puck set and $12 on tape. How much is left to save?" % (n, cap(he)),
                   20, [30, 80, 32, 38],
                   "Spent: $18 + $12 = $30. Left: $50 − $30 = <b>$20</b>. ($32 takes away only the $18; $80 adds.)"))
    n1, h1, _ = P.next()
    n2, h2, _ = P.next()
    its.append(mcq("Both %s and %s get $10 a week. %s saves $6 a week. %s saves $2 a week. After 5 weeks, how much more has %s saved?"
                   % (n1, n2, n1, n2, n1), 20, [4, 30, 40, 10],
                   "%s: 5 × $6 = $30. %s: 5 × $2 = $10. $30 − $10 = <b>$20</b> more. "
                   "People make different choices: %s spends more each week, %s saves more. ($4 is the difference for only one week.)"
                   % (n1, n2, n2, n1)))
    n, he, his = P.next()
    its.append(mcq(fig(jars_svg([("Spend", 9), ("Save", 15), ("Donate", 6)])) + "%s splits %s money into these jars. How much money did %s split?" % (n, his, he),
                   30, [24, 21, 15, 20],
                   "Add the jars: $9 + $15 + $6 = <b>$30</b>. Make a ten first: $9 + $6 = $15, $15 + $15 = $30. ($24 forgets the $6.)"))
    n, he, his = P.next()
    its.append(mcq("%s earns $12 each week walking a neighbour’s dog. %s saves $8 and spends the rest. How much does %s spend in 4 weeks?" % (n, cap(he), he),
                   16, [32, 48, 4, 20],
                   "Spent each week: $12 − $8 = $4. In 4 weeks: 4 × $4 = <b>$16</b>. ($32 is the money saved: 4 × $8.)"))
    n, he, his = P.next()
    its.append(mcq("%s wants to donate $40 to the Terry Fox Run. %s has $25. %s earns $5 for each driveway %s shovels. How many driveways must %s shovel?"
                   % (n, cap(he), cap(he), he, he), "3 driveways", ["8 driveways", "15 driveways", "13 driveways"],
                   "Still needed: $40 − $25 = $15. $15 ÷ $5 = <b>3 driveways</b>. (8 driveways forgets the $25 %s already has.)" % he, fmt=str))
    assert len(its) == 20
    return {"title": "Spending, saving, earning and donating", "items": its}


# ============================================================ set 5: good buys and word problems
def set_words(P):
    its = []
    its.append(mcq(fig(tags_svg([("1 notebook", 3), ("Pack of 3", 6)])) + "You need 3 notebooks. Which is the better buy?",
                   "The pack of 3", ["3 single notebooks", "They cost the same", "You cannot tell"],
                   "3 single notebooks: 3 × $3 = $9. The pack: $6. $6 is less than $9, so <b>the pack of 3</b> is the better buy.", fmt=str))
    assert 6 * 2 - 10 == 2
    its.append(mcq(fig(tags_svg([("1 juice box", 2), ("6-pack", 10)])) + "How much do you save by buying the 6-pack instead of 6 single juice boxes?",
                   2, [8, 12, 4],
                   "6 single boxes: 6 × $2 = $12. The 6-pack: $10. You save $12 − $10 = <b>$2</b>. ($8 is $10 − $2.)"))
    its.append(mcq(fig(tags_svg([("250 mL syrup", 8), ("500 mL syrup", 14)])) + "Which maple syrup is the better buy?",
                   "The 500 mL bottle", ["The 250 mL bottle", "They cost the same", "You cannot tell"],
                   "Two 250 mL bottles make 500 mL and cost 2 × $8 = $16. The 500 mL bottle is $14. <b>The 500 mL bottle</b> is the better buy.", fmt=str))
    its.append(mcq("A $10 soccer ball breaks every 2 months. A $20 ball lasts all year. Which is the better value for one year?",
                   "The $20 ball", ["The $10 ball", "They cost the same", "Neither ball"],
                   "In a year you would need 6 of the $10 balls: 6 × $10 = $60. One $20 ball lasts the year. "
                   "<b>The $20 ball</b> is better value, even though its price is higher.", fmt=str))
    its.append(mcq("A shirt is on sale for $5, but you do not need it and will not wear it. Is it a good buy?",
                   "No, it wastes $5", ["Yes, it is cheap", "Yes, sales are always good", "No, it should be free"],
                   "A good buy is something you need or will use at a fair price. If you will not wear it, <b>the $5 is wasted</b>.", fmt=str))
    assert 24 < 30 - 5
    its.append(mcq("Store A sells a ball for $24. Store B sells the same ball for $30 with $5 off. Which store is cheaper, and by how much?",
                   "Store A, by $1", ["Store B, by $5", "Store B, by $1", "Store A, by $6"],
                   "Store B: $30 − $5 = $25. Store A: $24. $25 − $24 = $1, so <b>Store A is cheaper by $1</b>. (Store A, by $6 forgets the $5 off.)", fmt=str))
    assert 10 * 5 == 50
    its.append(mcq("Public skating costs $5 a visit, or $40 for a 10-visit pass. For 10 visits, which is cheaper, and by how much?",
                   "The pass, by $10", ["Each visit, by $10", "The pass, by $35", "They cost the same"],
                   "10 visits at $5: 10 × $5 = $50. The pass: $40. $50 − $40 = $10, so <b>the pass is cheaper by $10</b>. ($35 is $40 − $5.)", fmt=str))
    n, he, his = P.next()
    its.append(mcq("%s has $40. %s wants skates for $28 and a helmet for $15. Does %s have enough?" % (n, cap(he), he),
                   "No, %s is $3 short" % he, ["Yes, with $3 left", "Yes, with $12 left", "No, %s is $13 short" % he],
                   "Total: $28 + $15 = $43. $43 is more than $40. $43 − $40 = $3, so <b>%s is $3 short</b>. ($12 left counts only the skates.)" % he, fmt=str))
    n, he, his = P.next()
    assert 4 * 12 == 48 and 50 - 48 == 2
    its.append(mcq("%s buys 4 tickets to the science centre at $12 each. %s pays with a $50 bill. How much change does %s get?" % (n, cap(he), he),
                   2, [38, 12, 98, 10],
                   "Tickets: 4 × $12 = $48. Count up from $48 to $50: <b>$2</b>. ($38 counts only one ticket.)"))
    n, he, his = P.next()
    assert 3 * 11 + 6 == 39
    its.append(mcq("%s’s family goes to a movie. 3 tickets cost $11 each, and popcorn is $6. What is the total?" % n, 39, [17, 33, 20, 49],
                   "Tickets: 3 × $11 = $33. Add the popcorn: $33 + $6 = <b>$39</b>. ($33 forgets the popcorn.)"))
    n, he, his = P.next()
    assert 3 * 15 - 18 == 27
    its.append(mcq("On a snow day, %s shovels 3 driveways at $15 each. %s spends $18 on new mitts. How much money is left?" % (n, cap(he)),
                   27, [45, 63, 33, 12],
                   "Earned: 3 × $15 = $45. Left: $45 − $18. Count up from $18: $2 to $20, then $25 to $45, so <b>$27</b>. ($63 adds the mitts.)"))
    n, he, his = P.next()
    assert 22 + 9 == 31 and 50 - 31 == 19
    its.append(mcq("At the hardware store, %s buys a birdhouse kit for $22 and paint for $9. %s pays with a $50 bill. How much change does %s get?"
                   % (n, cap(he), he), 19, [28, 41, 81, 29],
                   "Total: $22 + $9 = $31. Count up from $31 to $50: $31 + $9 = $40, $40 + $10 = $50. $9 + $10 = <b>$19</b>. "
                   "($28 forgets the paint.)"))
    n, he, his = P.next()
    assert 16 + 23 + 9 == 48
    its.append(mcq("%s plans a picnic at the lake. Sandwiches cost $16, fruit costs $23 and drinks cost $9. Round to the nearest $10. About how much is the picnic?"
                   % n, "About $50", ["About $40", "About $60", "About $48"],
                   "$16 → $20, $23 → $20, $9 → $10. $20 + $20 + $10 = <b>about $50</b>. (The exact total is $48.)", fmt=str))
    n, he, his = P.next()
    assert 2 * 12 + 8 == 32
    its.append(mcq(fig(tags_svg([("Scarf", 12), ("Mitts", 8), ("Hat", 15)])) + "%s buys 2 scarves and 1 pair of mitts. What is the total?" % n,
                   32, [20, 35, 44, 28],
                   "Scarves: 2 × $12 = $24. Add the mitts: $24 + $8 = <b>$32</b>. ($20 counts only one scarf.)"))
    n, he, his = P.next()
    its.append(mcq("%s has $25 on a gift card for a bookstore. %s buys a $14 book and a $7 journal. How much is left on the card?" % (n, cap(he)),
                   4, [11, 46, 18, 14],
                   "Total: $14 + $7 = $21. Left: count up from $21 to $25: <b>$4</b>. ($11 forgets the journal.)"))
    n, he, his = P.next()
    assert 30 - 3 * 6 == 12
    its.append(mcq("%s has $30. A pack of hockey cards costs $6. %s buys 3 packs. How much money is left?" % (n, cap(he)),
                   12, [24, 21, 48, 18],
                   "3 packs: 3 × $6 = $18. Left: $30 − $18 = <b>$12</b>. ($24 takes away only one pack.)"))
    its.append(mcq(fig(tags_svg([("Box of 10 pencils", 4), ("Box of 20 pencils", 9)])) + "A teacher needs 20 pencils. Which choice costs less?",
                   "Two boxes of 10", ["One box of 20", "They cost the same", "You cannot tell"],
                   "Two boxes of 10: 2 × $4 = $8. One box of 20: $9. $8 is less, so <b>two boxes of 10</b> cost less. "
                   "A bigger box is not always the better buy.", fmt=str))
    n, he, his = P.next()
    assert 7 * 2 == 14 and 60 - 14 == 46
    its.append(mcq("%s has $60 saved. %s spends $2 a week on snacks for 7 weeks. How much is left?" % (n, cap(he)),
                   46, [58, 53, 74, 14],
                   "Snacks: 7 × $2 = $14. Left: $60 − $14 = <b>$46</b>. ($58 takes away only one week; $53 takes away $7.)"))
    assert 5 * 8 + 15 == 55 and 100 - 55 == 45
    its.append(mcq("A Grade 4 class buys 5 board games at $8 each and a $15 puzzle for indoor recess. They pay with a $100 bill. How much change do they get?",
                   45, [77, 60, 55, 35],
                   "Games: 5 × $8 = $40. Total: $40 + $15 = $55. Count up from $55: $5 to $60, $40 to $100. $5 + $40 = <b>$45</b>. "
                   "($77 counts only one game; $55 is the total, not the change.)"))
    n, he, his = P.next()
    assert 2 * 35 + 18 == 88 and 100 - 88 == 12
    its.append(mcq("%s’s family buys 2 canoe paddles at $35 each and an $18 life jacket for the cottage. They pay with a $100 bill. How much change do they get?" % n,
                   12, [47, 22, 2, 88],
                   "Paddles: 2 × $35 = $70. Total: $70 + $18 = $88. Count up: $88 + $2 = $90, $90 + $10 = $100. $2 + $10 = <b>$12</b>. "
                   "($47 counts only one paddle; $22 adds one $10 jump too many.)"))
    assert len(its) == 20
    return {"title": "Good buys and money word problems", "items": its}


# ============================================================ lesson
def body_html():
    assert 27 + 15 + 8 == 50 and 100 - 63 == 37
    return (
        "<h2>Ways to pay</h2>"
        "<p>There is more than one way to pay. Each one works in a different way.</p>" +
        table(["Way to pay", "How it works", "Good to know"], [
            ["Cash", "Coins and bills you hand over", "You can see what is left. You may get change. Does not work online"],
            ["Debit card", "Takes money straight from your bank account", "Exact amount. You can only spend what is in the account"],
            ["Credit card", "Borrows money you pay back when the bill comes", "Easy to overspend. Extra fees (interest) if paid late"],
            ["Gift card", "Has a set amount on it, often a present", "Usually works only at one store. The amount goes down each time"],
        ]) +
        "<h2>Total cost: add the prices in your head</h2>"
        "<p>Look for prices that make a ten. Use a friendly number: $19 is $20 − $1.</p>"
        "<figure class='sn-fig'>" + tags_svg([("Backpack", 27), ("Lunch box", 15), ("Ruler", 8)]) +
        "<figcaption>$27 + $15 = $42. $42 + $8 = $50.</figcaption></figure>" +
        ex("Example", "Find the total of $19 and $24.", "$20 + $24 = $44. Take back the $1: $44 − $1 = $43.", "$43") +
        "<p>To <b>estimate</b>, round each price to the nearest $10 first: $38 + $61 is about $40 + $60 = $100.</p>"
        "<h2>Change: count up from the price</h2>"
        "<p>Start at the price. Jump to the next $10. Then jump to the money paid. Add the jumps.</p>"
        "<figure class='sn-fig'>" + change_line(63, 100) +
        "<figcaption>$63 + $7 = $70. $70 + $30 = $100. The change is $7 + $30 = $37.</figcaption></figure>" +
        ex("Example", "A book costs $37. You pay with a $50 bill. What is the change?",
           "$37 + $3 = $40. $40 + $10 = $50. $3 + $10 = $13. Check: $37 + $13 = $50.", "$13") +
        "<h2>Spend, save, donate</h2>"
        "<p><b>Earning</b> is getting money for work. <b>Spending</b> is buying things. <b>Saving</b> is keeping money for later. "
        "<b>Investing</b> is putting money where it can grow, like a bank account that pays interest. "
        "<b>Donating</b> is giving money to help others.</p>"
        "<figure class='sn-fig'>" + jars_svg([("Spend", 12), ("Save", 15), ("Donate", 3)], "$30 from raking leaves") +
        "<figcaption>$12 + $15 + $3 = $30. More spending means less saving.</figcaption></figure>"
        "<h2>Is it a good buy?</h2>"
        "<p>Compare the cost of the same amount. 3 notebooks at $3 each cost $9, so a pack of 3 for $6 is the better buy. "
        "A bigger pack is not always cheaper, so check. And something you do not need is never a good buy.</p>"
        "<h2>Common mistakes</h2>" +
        table(["Mistake", "What to do instead"], [
            ["Adding to find change: $37 + $50 = $87", "Change is less than the money paid. Count up from $37 to $50: $13"],
            ["Counting up wrongly: $37 to $50 is $3 + $20", "Jump to the next ten ($40), then only $10 more to $50"],
            ["Forgetting one item in the total", "Tick off each price as you add it"],
            ["$26 + $15 = $31", "6 + 5 = 11 ones. Regroup 10 ones as a ten: $41"],
            ["Buying the bigger pack without checking", "Find the cost of the same number of things first"],
        ])
    )


FAQ = [
    {"q": "What do Grade 4 students learn about money in Ontario?",
     "a": "In the Ontario Grade 4 financial literacy strand, students learn different ways to pay, add the cost of several items priced in whole dollars, find the change from a cash payment using mental math, and talk about spending, saving, earning, investing and donating."},
    {"q": "How do you teach making change in Grade 4?",
     "a": "Count up from the price to the money paid. For a $37 item paid with $50, jump $3 to $40, then $10 to $50, so the change is $13. Then check that the price plus the change equals the money paid."},
    {"q": "What is the difference between a debit card and a credit card for kids?",
     "a": "A debit card takes the money straight from your own bank account. A credit card borrows the money, and you must pay the bill later, with extra fees if you pay late."},
    {"q": "Is sales tax included in Grade 4 money questions?",
     "a": "No. The Grade 4 expectation uses whole-dollar prices without sales tax. Ontario’s 13% HST is added to money problems in Grade 6."},
]


def gen():
    rnd = random.Random(44818)
    P = People(rnd)
    sets = [set_pay(P), set_total(P), set_change(P), set_choices(P), set_words(P)]
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        assert sorted(it["a"] for it in s["items"]) == sorted([0, 1, 2, 3] * 5)
        for it in s["items"]:
            assert len(set(it["c"])) == 4, it
            vv = [mval(c) for c in it["c"] if mval(c) is not None]
            assert len(set(vv)) == len(vv), it["c"]
            assert it["q"] not in seen, it["q"]
            seen.add(it["q"])
            assert it["q"].count("<svg") <= 1
            for x in [it["q"], it["e"]] + it["c"]:
                assert "\\" not in x and '"' not in x, x
    u = {
        "country": "ca-on", "subject": "math", "grade": "grade-4", "slug": "money-and-financial-literacy", "sort": 18,
        "updated": UPDATED, "pdf_url": "",
        "title": "Grade 4 Money and Financial Literacy: Ways to Pay, Total Cost and Making Change",
        "seo_title": "Grade 4 Money Worksheets: Making Change, Total Cost and Ways to Pay (Free, Answer Key, Ontario Curriculum)",
        "short_title": "Money and financial literacy",
        "domain": "Financial Literacy",
        "standard_code": "Grade 4: F1.2",
        "standard_url": "https://www.dcp.edu.gov.on.ca/en/curriculum/elementary-mathematics",
        "standard_text": "Estimate and calculate the cost of transactions involving multiple items priced in whole-dollar amounts, "
                         "not including sales tax, and the amount of change needed when payment is made in cash, using mental math",
        "meta_desc": "Free Grade 4 money and financial literacy math worksheets for the Ontario curriculum: cash, debit, credit and gift cards, "
                     "the total cost of several items in whole dollars, making change from $20, $50 and $100 by counting up, "
                     "spending, saving and donating, and finding the better buy. 100 questions with an answer key.",
        "key_big": "To find change, count up from the price to the money paid: $37 → $40 → $50 is $3 + $10 = $13.",
        "key_sub": "Add prices in your head by making tens ($8 + $12 = $20) and using friendly numbers ($19 = $20 − $1). "
                   "Debit spends your own money; credit is borrowed and must be paid back.",
        "body_html": body_html(), "faq": FAQ, "sets": sets,
    }
    mark_large(u, "price tags: [^,']*,[^,']*,")
    mark_large(u, "counting up")
    mark_large(u, "money jars")
    mark_large(u, "bills: [^,']*,[^,']*,[^,']*,")
    return u


if __name__ == "__main__":
    u = gen()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, u["slug"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(u, fh, ensure_ascii=False, indent=1)
    print("wrote", path)
