# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Canadian Coins (BC Mathematics Curriculum, Kindergarten Content: Financial literacy —
attributes and names of Canadian coins; role-playing transactions; token value)
  python3 tools/gen_cabc_math_k_canadian_coins.py
Naming the nickel, dime, quarter, loonie and toonie, what is on each coin (beaver, Bluenose, caribou, loon,
polar bear), size, colour and shape, sorting and counting coins, trading (2 loonies for 1 toonie, tokens), and
playing store with loonies and toonies. The coin pictures are the BC Grade 1 coins (labelled shapes, sized like
the real coins, no real designs). Counts and dollar amounts are 10 or less.
Wrong answers come from real mistakes: thinking the small dime is worth less than the bigger nickel, mixing up
the loonie and the toonie, counting coins instead of dollars, and thinking more coins always means more money.
"""
import random
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_cabc_math_g1_money as g1

R = random.Random(53201)
POS = Cycle()
ONE, MANY = g1.ONE, g1.MANY
NAMES = {t: ONE[t].capitalize() for t in ONE}
PIC = {"N": "a beaver", "D": "a sailing ship called the Bluenose", "Q": "a caribou", "L": "a loon", "T": "a polar bear"}
LOOKS = {"L": "gold and has 11 sides", "T": "silver on the outside and gold in the middle",
         "D": "the smallest coin", "T2": "the biggest coin"}


def up(s):
    return s[0].upper() + s[1:]


def coin(t, hide=False):
    w, h = g1.tok_size(t)
    return fig(g1.svg_wrap(w + 8, h + 8, g1.draw_tok(t, (w + 8) / 2, (h + 8) / 2, hide), "one coin worth " + g1.lab(g1.VAL[t]) if not hide else "one coin"))


def lettered(toks, hide=True):
    return fig(g1.money_svg(toks, per_row=4, gap=12, under=list("ABCD"), hide=hide, label="coins A, B, C and D"))


# ------------------------------------------------------------ set 1: name the coin
WRONG = {"N": ["Dime", "Quarter", "Loonie"], "D": ["Nickel", "Quarter", "Toonie"], "Q": ["Nickel", "Dime", "Loonie"],
         "L": ["Toonie", "Quarter", "Nickel"], "T": ["Loonie", "Quarter", "Dime"]}


def set_names(r):
    its = []
    for t in "NDQLT":
        its.append(mcq(coin(t) + "What is the name of this coin?", NAMES[t], WRONG[t],
                       "This coin is worth %s. It is a <b>%s</b>." % (g1.lab(g1.VAL[t]), ONE[t])))
    for t, v in (("L", 1), ("T", 2)):
        its.append(mcq(coin(t, hide=True) + "This coin is a %s. How many dollars is it worth?" % ONE[t], "$%d" % v, ["$%d" % (3 - v), "$5", "$10"],
                       "A %s is worth <b>$%d</b>." % (ONE[t], v)))
    its.append(mcq(coin("L", hide=True) + "This coin is gold and has 11 sides. What is it?", "Loonie", ["Toonie", "Quarter", "Dime"],
                   "Gold with 11 sides: it is a <b>loonie</b>."))
    its.append(mcq(coin("T", hide=True) + "This coin is silver with a gold middle. What is it?", "Toonie", ["Loonie", "Nickel", "Quarter"],
                   "Silver with a gold middle: it is a <b>toonie</b>."))
    return its + collect(one_find, 11, r)


def one_find(r):
    t = r.choice(list(ONE))
    others = r.sample([x for x in ONE if x != t], 3)
    j = POS.next()
    toks = others[:j] + [t] + others[j:]
    it = mcq(fig(g1.money_svg(toks, per_row=4, gap=12, under=list("ABCD"), label="coins A, B, C and D")) + "Which coin is the <b>%s</b>?" % ONE[t],
             "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]], "Coin <b>%s</b> shows %s. It is the %s." % ("ABCD"[j], g1.lab(g1.VAL[t]), ONE[t]))
    return letters(it, "ABCD"[j])


# ------------------------------------------------------------ set 2: what does it look like?
def set_look(r):
    its = []
    for t in "NDQLT":
        wr = [up(PIC[x]) for x in "NDQLT" if x != t][:3]
        its.append(mcq(coin(t) + "This is a %s. What is on the back of a %s?" % (ONE[t], ONE[t]), up(PIC[t]), wr,
                       "The %s has <b>%s</b> on the back." % (ONE[t], PIC[t])))
    for t in "NDQLT":
        its.append(mcq("Which coin has <b>%s</b> on the back?" % PIC[t], NAMES[t], WRONG[t],
                       "%s is on the back of the <b>%s</b>." % (up(PIC[t]), ONE[t])))
    return its + collect(one_look, 10, r)


def one_look(r):
    key = r.choice(list(LOOKS))
    tt = "T" if key == "T2" else key
    toks = r.sample([x for x in ONE if x != tt], 3)
    j = POS.next()
    toks = toks[:j] + [tt] + toks[j:]
    it = mcq(lettered(toks) + "Which coin is %s?" % LOOKS[key], "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]],
             "Coin <b>%s</b> is the %s. It is %s." % ("ABCD"[j], ONE[tt], LOOKS[key]))
    return letters(it, "ABCD"[j])


# ------------------------------------------------------------ set 3: sort and count coins
def one_count(r):
    ks = r.sample(list(ONE), r.choice([2, 3]))
    vals = [r.randint(1, 5) for _ in ks]
    if sum(vals) > 10 or len(set(vals)) != len(vals):
        return None
    toks = [t for t, n in zip(ks, vals) for _ in range(n)]
    r.shuffle(toks)
    pic = fig(g1.money_svg(toks, per_row=5))
    kind = r.choice(["one", "one", "all", "most"])
    if kind == "one":
        j = r.randrange(len(ks))
        return mcq(pic + "Sort the coins. How many <b>%s</b> are there?" % MANY[ks[j]], vals[j], [sum(vals)] + [v for i, v in enumerate(vals) if i != j] + [vals[j] + 1, vals[j] - 1],
                   "Look only at the %s. There %s <b>%d</b>." % (MANY[ks[j]], "is" if vals[j] == 1 else "are", vals[j]))
    if kind == "all":
        n = sum(vals)
        return mcq(pic + "How many coins are there in all?", n, vals + [n + 1, n - 1],
                   "Count every coin, one at a time: <b>%d</b> coins." % n)
    big = ks[vals.index(max(vals))]
    return mcq(pic + "Sort the coins. Which kind of coin is there the <b>most</b> of?", NAMES[big] + "s", [NAMES[k] + "s" for k in ks if k != big] + ["They are all the same"],
               "Count each kind: %s. The most are <b>%s</b>." % (", ".join("%d %s" % (v, ONE[k] if v == 1 else MANY[k]) for k, v in zip(ks, vals)), MANY[big]))


# ------------------------------------------------------------ set 4: trading and tokens
def one_trade(r):
    K = Kids(r)
    k = K.next()
    kind = r.choice(["toonie", "toonies", "loonies", "token", "token", "more"])
    if kind == "toonie":
        return mcq(fig(g1.two_groups(["L", "L"], ["T"], "2 loonies", "1 toonie", "2 loonies and 1 toonie", arrow=True)) + "Is this a fair trade?",
                   "Yes. 2 loonies are worth the same as 1 toonie", ["No. 2 coins are more than 1 coin", "No. The toonie is worth more", "We cannot tell"],
                   "A toonie is $2 and 2 loonies are $2. <b>Yes. 2 loonies are worth the same as 1 toonie</b>.")
    if kind == "toonies":
        n = r.randint(1, 5)
        return mcq(fig(g1.money_svg(["T"] * n)) + "%s trades %s toonie%s for loonies. How many loonies does %s get?" % (k["n"], n, "" if n == 1 else "s", k["he"]),
                   2 * n, [n, n + 1, 2 * n + 1, 2 * n - 1], "1 toonie is 2 loonies. %s toonie%s %s <b>%d</b> loonies." % (n, "" if n == 1 else "s", "is" if n == 1 else "are", 2 * n))
    if kind == "loonies":
        n = r.choice([2, 4, 6, 8, 10])
        return mcq(fig(g1.money_svg(["L"] * n)) + "%s trades %d loonies for toonies. How many toonies does %s get?" % (k["n"], n, k["he"]),
                   n // 2, [n, n // 2 + 1, n // 2 - 1 if n > 2 else 3], "2 loonies make 1 toonie. %d loonies make <b>%d</b> toonie%s." % (n, n // 2, "" if n == 2 else "s"))
    if kind == "token":
        what, cost = r.choice([("a sticker", 1), ("a bookmark", 2), ("a pencil", 2), ("a bouncy ball", 3), ("a toy car", 5)])
        have = r.randint(cost, 10)
        if have == cost and r.random() < 0.5:
            have = cost + 1
        if r.random() < 0.5:
            return mcq("At the class store, %s costs %d token%s. %s has %d tokens. Can %s buy it?" % (what, cost, "" if cost == 1 else "s", k["n"], have, k["he"]),
                       "Yes", ["No", "Only with a toonie", "We cannot tell"], "%d tokens is %s %d. <b>Yes</b>, %s can buy it." % (have, "the same as" if have == cost else "more than", cost, k["he"]))
        low = r.randint(0, cost - 1) if cost > 1 else 0
        return mcq("At the class store, %s costs %d tokens. %s has %d token%s. Can %s buy it?" % (what, max(cost, 2), k["n"], low, "" if low == 1 else "s", k["he"]),
                   "No", ["Yes", "Yes, if %s asks nicely" % k["he"], "We cannot tell"], "%d is less than %d. <b>No</b>, %s needs more tokens." % (low, max(cost, 2), k["he"]), allow_zero=True)
    a, b = r.randint(2, 5), r.randint(1, 3)
    if b * 2 <= a or a <= b:
        return None
    return mcq(fig(g1.two_groups(["L"] * a, ["T"] * b, "%d loonies" % a, "%d toonie%s" % (b, "" if b == 1 else "s"), "loonies and toonies")) +
               "Which side has <b>more money</b>?", "The toonies", ["The loonies, because there are more coins", "They are the same", "We cannot tell"],
               "%d loonies are $%d. %d toonie%s %s $%d. <b>The toonies</b> have more money, even with fewer coins." % (a, a, b, "" if b == 1 else "s", "is" if b == 1 else "are", 2 * b))


# ------------------------------------------------------------ set 5: play store
ITEMS = [("apple", 1), ("juice box", 2), ("muffin", 3), ("book", 5), ("ball", 4), ("kite", 6), ("puzzle", 7), ("hat", 8)]


def one_store(r):
    K = Kids(r)
    k = K.next()
    item, p = r.choice(ITEMS)
    kind = r.choice(["loonies", "loonies", "toonies", "enough", "two"])
    tag = fig(g1.tag_svg("$%d" % p, item))
    if kind == "loonies":
        return mcq(tag + "%s pays with loonies. How many loonies does %s need?" % (k["n"], k["he"]), p, [p + 1, p - 1, 2 * p, p + 2],
                   "1 loonie is $1. $%d is <b>%d</b> loonie%s." % (p, p, "" if p == 1 else "s"))
    if kind == "toonies":
        if p % 2:
            return None
        return mcq(tag + "%s pays with toonies. How many toonies does %s need?" % (k["n"], k["he"]), p // 2, [p, p // 2 + 1, p // 2 - 1 if p > 2 else 3],
                   "1 toonie is $2. Count by 2s to $%d: %s. That is <b>%d</b> toonie%s." % (p, ", ".join(str(x) for x in range(2, p + 1, 2)), p // 2, "" if p == 2 else "s"))
    if kind == "enough":
        n = r.randint(1, 10)
        if n == p:
            return None
        ok = n > p
        return mcq(fig(g1.money_svg(["L"] * n)) + "%s has these loonies. The %s costs $%d. Does %s have enough?" % (k["n"], item, p, k["he"]),
                   "Yes" if ok else "No", ["No" if ok else "Yes", "Only if %s has a toonie" % k["he"], "We cannot tell"],
                   "%d loonies is $%d. $%d is %s than $%d. <b>%s</b>." % (n, n, n, "more" if ok else "less", p, "Yes" if ok else "No"))
    item2, p2 = r.choice([x for x in ITEMS if x[1] + p <= 10 and x[0] != item] or [None])
    if item2 is None:
        return None
    return mcq("%s buys a %s for $%d and a %s for $%d. How many dollars is that in all?" % (k["n"], item, p, item2, p2), "$%d" % (p + p2),
               ["$%d" % p, "$%d" % p2, "$%d" % (p + p2 + 1), "$%d" % (p + p2 - 1)], "$%d and $%d make <b>$%d</b>." % (p, p2, p + p2))


def build():
    sets = [S("Name the coin", set_names(R)),
            S("What is on each coin?", set_look(R)),
            S("Sort and count coins", collect(one_count, 20, R)),
            S("Trading and tokens", collect(one_trade, 20, R)),
            S("Play store", collect(one_store, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>Canada has five coins: <b>nickel</b> (beaver), <b>dime</b> (Bluenose ship), <b>quarter</b> (caribou), <b>loonie</b> (loon) and <b>toonie</b> (polar bear).</li>"
        "<li>The <b>loonie</b> is gold with 11 sides and is worth $1. The <b>toonie</b> is silver with a gold middle and is worth $2.</li>"
        "<li>The dime is the smallest coin, but it is worth more than a nickel. Size does not tell the value.</li>"
        "<li>2 loonies are worth the same as 1 toonie. That is a fair trade.</li></ul>",
        [figure(g1.money_svg(["N", "D", "Q", "L", "T"], per_row=5, gap=10, under=["nickel", "dime", "quarter", "loonie", "toonie"], label="the five Canadian coins"),
                "The five Canadian coins."),
         figure(g1.two_groups(["L", "L"], ["T"], "2 loonies", "1 toonie", "2 loonies and 1 toonie", arrow=True), "2 loonies trade for 1 toonie.")],
        [["Mixing up the loonie and the toonie", "The loonie has the loon and 11 sides. The toonie has two colours."],
         ["Thinking the small dime is worth the least", "The dime is small, but it is worth more than a nickel."],
         ["Thinking more coins is more money", "Look at the coins, not how many. 1 toonie is more than 1 loonie."]])
    faq = [("Which coins do Kindergarten children learn in BC?", "The nickel, dime, quarter, loonie and toonie: their names, what is on them, and their colour, size and shape."),
           ("Why is there no penny?", "Canada stopped making pennies in 2012. Prices are rounded, so the smallest coin used is the nickel."),
           ("What is token value?", "A token stands for something, like a coin or a ticket you trade for a treat. Children learn that a token can be traded for something of the same value."),
           ("How can I practise at home?", "Set up a play store with toys and price tags of $1 to $5, and pay with loonies and toonies.")]
    make("canadian-coins", 12, "Financial literacy", "Canadian Coins: Names, Pictures and Playing Store", "Canadian coins",
         "Financial literacy: attributes and names of Canadian coins; role-playing transactions; token value",
         "Free Kindergarten math worksheets on Canadian coins for the BC curriculum: nickel, dime, quarter, loonie and toonie, what is on each coin, sorting coins, trading and playing store. 100 picture questions with answers.",
         "Canada has 5 coins: nickel, dime, quarter, loonie and toonie.", "A loonie is $1 and a toonie is $2. 2 loonies trade for 1 toonie.",
         body, faq, sets)


if __name__ == "__main__":
    build()
