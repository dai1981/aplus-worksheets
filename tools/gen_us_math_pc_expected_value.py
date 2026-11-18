# -*- coding: utf-8 -*-
"""
US Precalculus: Probability Distributions and Expected Value (Common Core S-MD.A.2, S-MD.A.3, S-MD.A.4, S-MD.B.5, S-MD.B.6, S-MD.B.7)
  python3 tools/gen_us_math_pc_expected_value.py
Probability distributions, expected value from a table, games and fair games, binomial probabilities and
their expected value, and decisions such as insurance and warranties.
Wrong answers come from real mistakes: averaging the values without weights, forgetting to subtract the
cost to play, using the prize instead of the net gain, and leaving out the C(n, k) factor in binomial
probabilities.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, usd, People, fr
from a2_common import sf
from pc_common import GRADE, C

R = random.Random(98501)
EX = "<i>E</i>(<i>X</i>)"


def table(xs, ps, xname="<i>x</i>", pname="<i>P</i>(<i>x</i>)", fmt=None):
    f = fmt or (lambda v: sf(v))
    return ("<table class='sn-table'><tr><th>%s</th>%s</tr><tr><th>%s</th>%s</tr></table>" % (
        xname, "".join("<td>%s</td>" % f(x) for x in xs), pname, "".join("<td>%s</td>" % p for p in ps)))


def d2(v):
    return num(F(v).limit_denominator(100))


def rand_dist(r, n):
    cuts = sorted(r.sample(range(1, 20), n - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [20])]
    return [F(p, 20) for p in parts]


# ------------------------------------------------------------ set 1: probability distributions
def one_dist(r):
    n = r.choice([3, 4, 4, 5])
    ps = rand_dist(r, n)
    xs = sorted(r.sample(range(0, 10), n))
    if r.random() < 0.7:
        i = r.randrange(n)
        shown = [num(p) if j != i else "<i>k</i>" for j, p in enumerate(ps)]
        q = "The table shows a probability distribution. What is <i>k</i>?" + table(xs, shown)
        rest = sum(p for j, p in enumerate(ps) if j != i)
        return T(q, num(ps[i]), [num(rest), num(F(1, n)), num(ps[i] + F(1, 10)) if ps[i] + F(1, 10) < 1 else num(ps[i] / 2)],
                 "The probabilities must add to 1: <i>k</i> = 1 − %s = <b>%s</b>." % (num(rest), num(ps[i])))
    bad = r.choice(["sum", "neg"])
    good = [num(p) for p in ps]
    if bad == "sum":
        badp = [num(p) for p in ps[:-1]] + [num(ps[-1] + F(1, 10))]
        reason = "No, the probabilities add to %s, not 1" % num(1 + F(1, 10))
    else:
        badp = [num(ps[0] + F(1, 10)), MINUS + "0.1"] + [num(p) for p in ps[1:-1]] + [num(ps[-1])]
        badp = badp[:n]
        reason = "No, a probability cannot be negative"
    if r.random() < 0.5:
        q = "Is this a valid probability distribution?" + table(xs, good)
        right = "Yes, every probability is between 0 and 1 and they add to 1"
        return T(q, right, ["No, the probabilities must be equal", "No, the values of <i>x</i> must add to 1", "No, a probability cannot be a decimal"], "<b>%s</b>." % right)
    q = "Is this a valid probability distribution?" + table(xs, badp)
    return T(q, reason, ["Yes, every probability is between 0 and 1 and they add to 1", "No, the values of <i>x</i> must add to 1", "Yes, because there is one probability for each value"],
             "Each probability must be from 0 to 1, and the total must be exactly 1. <b>%s</b>." % reason)


# ------------------------------------------------------------ set 2: expected value from a table
def one_ev(r):
    n = r.choice([3, 4])
    ps = rand_dist(r, n)
    xs = sorted(r.sample(range(0, 12), n))
    ev = sum(x * p for x, p in zip(xs, ps))
    q = "Find the expected value %s for this distribution.%s" % (EX, table(xs, [num(p) for p in ps]))
    wr = [d2(F(sum(xs), n)), d2(sum(ps) * max(xs)), d2(sum(x * p for x, p in zip(xs, ps[::-1])))]
    if len(set(wr + [d2(ev)])) < 4:
        return None
    return T(q, d2(ev), wr, "Multiply each value by its probability and add: %s = <b>%s</b>." % (" + ".join("%d(%s)" % (x, num(p)) for x, p in zip(xs, ps)), d2(ev)))


# ------------------------------------------------------------ set 3: games
def one_game(r):
    kind = r.choice(["die", "die", "spin", "fair", "raffle"])
    if kind == "die":
        cost = r.choice([1, 2, 3])
        win6 = r.choice([6, 12, 18, 9, 15, 3])
        if win6 <= cost:
            return None
        q = "A game costs %s to play. You roll a number cube and win %s if you roll a 6; otherwise you win nothing. What is the expected value of your net gain?" % (usd(cost), usd(win6))
        ev = F(win6, 6) - cost
        return T(q, usd(ev), [usd(F(win6, 6)), usd(-cost), usd(win6 - cost)],
                 "Expected prize = %s × 1/6 = %s. Subtract the cost to play: %s − %s = <b>%s</b>." % (usd(win6), usd(F(win6, 6)), usd(F(win6, 6)), usd(cost), usd(ev)))
    if kind == "spin":
        prizes = r.choice([(10, 5, 0), (20, 4, 0), (8, 2, 0), (15, 5, 1)])
        probs = r.choice([(F(1, 10), F(3, 10), F(6, 10)), (F(1, 5), F(1, 5), F(3, 5)), (F(1, 4), F(1, 4), F(1, 2))])
        cost = r.choice([2, 3, 4])
        ev = sum(a * b for a, b in zip(prizes, probs)) - cost
        q = ("A spinner pays %s, %s or %s with probabilities %s, %s and %s. It costs %s to spin. What is the expected net gain per spin?" % (
            usd(prizes[0]), usd(prizes[1]), usd(prizes[2]), num(probs[0]), num(probs[1]), num(probs[2]), usd(cost)))
        return T(q, usd(ev), [usd(ev + cost), usd(F(sum(prizes), 3) - cost), usd(-ev) if ev else usd(1)],
                 "Expected prize = %s = %s. Subtract the cost: %s − %s = <b>%s</b>." % (" + ".join("%s(%s)" % (num(a), num(b)) for a, b in zip(prizes, probs)), usd(ev + cost), usd(ev + cost), usd(cost), usd(ev)))
    if kind == "fair":
        pw = r.choice([F(1, 4), F(1, 5), F(1, 3), F(1, 6), F(2, 5)])
        cost = r.choice([1, 2, 3, 5])
        prize = cost / pw
        q = "A game costs %s. You win with probability %s. For the game to be fair (expected net gain of %s), what should the prize be?" % (usd(cost), num(pw) if pw.denominator in (4, 5) else sf(pw), usd(0))
        return T(q, usd(prize), [usd(prize - cost), usd(cost * pw) if cost * pw != prize else usd(prize + 1), usd(prize + cost)],
                 "Fair means expected prize = cost: prize × %s = %s, so the prize is <b>%s</b>. (The net gain when you win is the prize minus the cost.)" % (sf(pw), usd(cost), usd(prize)))
    tickets = r.choice([500, 1000, 2000])
    price = r.choice([2, 5, 10])
    prize = r.choice([300, 500, 1000, 1500])
    ev = F(prize, tickets) - price
    q = "A raffle sells %s tickets for %s each. One ticket wins a %s prize. What is the expected value of buying one ticket?" % (num(tickets), usd(price), usd(prize))
    return T(q, usd(ev), [usd(F(prize, tickets)), usd(prize - price), usd(-price)],
             "%s = %s × (1/%s) − %s = %s − %s = <b>%s</b>." % (EX, usd(prize), num(tickets), usd(price), usd(F(prize, tickets)), usd(price), usd(ev)))


# ------------------------------------------------------------ set 4: binomial probabilities
def one_bin(r):
    kind = r.choice(["p", "p", "p", "ev"])
    n = r.choice([4, 5, 6, 8, 10])
    p = r.choice([F(1, 2), F(1, 4), F(1, 5), F(3, 10), F(1, 10), F(2, 5)])
    if kind == "ev":
        q = "A player makes each free throw with probability %s. What is the expected number made in %d attempts?" % (num(p), n)
        ans = n * p
        return T(q, num(ans), [num(p), num(n * (1 - p)), num(F(n, 2)) if F(n, 2) != ans else num(ans + 1)], "For a binomial distribution, %s = <i>np</i> = %d × %s = <b>%s</b>." % (EX, n, num(p), num(ans)))
    k = r.randint(1, min(n - 1, 4))
    pr = C(n, k) * float(p) ** k * float(1 - p) ** (n - k)
    q = "Each seed sprouts with probability %s, independently. If %d seeds are planted, what is the probability that exactly %d sprout%s? Round to three decimal places." % (num(p), n, k, "s" if k == 1 else "")
    f3 = lambda v: num(F(round(v, 3)).limit_denominator(1000))
    right = f3(pr)
    wr = [f3(float(p) ** k * float(1 - p) ** (n - k)), f3(C(n, k) * float(p) ** (n - k) * float(1 - p) ** k), f3(float(p) ** k)]
    if len(set(wr + [right])) < 4 or right == "0":
        return None
    return T(q, right, wr, "<i>P</i> = %s(%s)<sup>%d</sup>(%s)<sup>%d</sup> ≈ <b>%s</b>. Do not forget the %s ways to choose which seeds sprout." % (
        "<sub>%d</sub>C<sub>%d</sub>" % (n, k), num(p), k, num(1 - p), n - k, right, "<sub>%d</sub>C<sub>%d</sub> = %d" % (n, k, C(n, k))))


# ------------------------------------------------------------ set 5: decisions
def one_dec(r):
    pp = People(r)
    nm, he, his = pp.next()
    kind = r.choice(["warranty", "warranty", "insurance", "insurance", "choice"])
    if kind == "warranty":
        cost = r.choice([40, 60, 80, 100])
        repair = r.choice([200, 300, 400, 500])
        p = r.choice([F(1, 10), F(1, 5), F(1, 4), F(3, 20)])
        exp_rep = repair * p
        q = ("%s can buy a %s warranty for a laptop. Without it, there is a %s chance of a %s repair. Based on expected cost, should %s buy the warranty?" % (
            nm, usd(cost), "%d%%" % int(p * 100), usd(repair), he))
        if exp_rep > cost:
            right = "Yes: the expected repair cost is %s, more than %s" % (usd(exp_rep), usd(cost))
            wr = ["No: the expected repair cost is %s, less than %s" % (usd(exp_rep), usd(cost)), "No: %s is less than %s" % (usd(cost), usd(repair)), "It makes no difference"]
        elif exp_rep < cost:
            right = "No: the expected repair cost is %s, less than %s" % (usd(exp_rep), usd(cost))
            wr = ["Yes: the expected repair cost is %s, more than %s" % (usd(exp_rep), usd(cost)), "Yes: %s is less than %s" % (usd(cost), usd(repair)), "It makes no difference"]
        else:
            right = "It makes no difference: the expected cost is %s either way" % usd(cost)
            wr = ["Yes: %s is less than %s" % (usd(cost), usd(repair)), "No: a repair may never happen", "Yes: the warranty always saves money"]
        return T(q, right, wr, "Expected repair cost = %s × %s = %s. Compare it with the warranty price %s. <b>%s</b>." % (usd(repair), num(p), usd(exp_rep), usd(cost), right))
    if kind == "insurance":
        prem = r.choice([200, 300, 500])
        claim = r.choice([10000, 20000, 50000])
        p = r.choice([F(1, 100), F(1, 200), F(1, 500), F(3, 1000)])
        q = "An insurance company charges a %s premium. It pays %s with probability %s. What is the company's expected profit per policy?" % (usd(prem), usd(claim), num(p))
        ev = prem - claim * p
        return T(q, usd(ev), [usd(prem), usd(claim * p), usd(-ev) if ev else usd(prem + claim * p)],
                 "Expected profit = premium − expected payout = %s − %s × %s = %s − %s = <b>%s</b>." % (usd(prem), usd(claim), num(p), usd(prem), usd(claim * p), usd(ev)))
    a1, p1 = r.choice([(100, F(1, 2)), (200, F(1, 4)), (60, F(3, 4)), (500, F(1, 10))])
    a2, p2 = r.choice([(80, F(3, 5)), (300, F(1, 5)), (40, F(9, 10)), (1000, F(1, 20))])
    e1, e2 = a1 * p1, a2 * p2
    if e1 == e2:
        return None
    q = "Option A pays %s with probability %s. Option B pays %s with probability %s. Which option has the greater expected value?" % (usd(a1), num(p1), usd(a2), num(p2))
    right = "Option A (%s vs. %s)" % (usd(e1), usd(e2)) if e1 > e2 else "Option B (%s vs. %s)" % (usd(e2), usd(e1))
    wrong = "Option B (%s vs. %s)" % (usd(e2), usd(e1)) if e1 > e2 else "Option A (%s vs. %s)" % (usd(e1), usd(e2))
    return T(q, right, [wrong, "Option %s, because its prize is larger" % ("A" if a1 > a2 else "B"), "Option %s, because it is more likely to pay" % ("A" if p1 > p2 else "B")],
             "%s for A: %s × %s = %s. For B: %s × %s = %s. <b>%s</b>." % (EX, usd(a1), num(p1), usd(e1), usd(a2), num(p2), usd(e2), right))


def build():
    sets = [S("Probability distributions", collect(one_dist, 20, R)),
            S("Expected value from a table", collect(one_ev, 20, R)),
            S("Games and fair games", collect(one_game, 20, R)),
            S("Binomial probabilities", collect(one_bin, 20, R)),
            S("Making decisions", collect(one_dec, 20, R))]
    body = lesson(
        "<ul><li>A <b>probability distribution</b> lists each value of <i>X</i> with its probability. Every probability is from 0 to 1, and they add to 1.</li>"
        "<li><b>Expected value</b>: " + EX + " = Σ <i>x</i> · <i>P</i>(<i>x</i>), the long-run average.</li>"
        "<li>For a game, use the <b>net gain</b> (prize minus cost). A game is <b>fair</b> when the expected net gain is 0.</li>"
        "<li><b>Binomial</b>: in <i>n</i> independent trials with success probability <i>p</i>, <i>P</i>(<i>X</i> = <i>k</i>) = <sub><i>n</i></sub>C<sub><i>k</i></sub> <i>p</i><sup><i>k</i></sup>(1 − <i>p</i>)<sup><i>n</i>−<i>k</i></sup> and " + EX + " = <i>np</i>.</li>"
        "<li>To decide between options, compare expected values (or expected costs).</li></ul>",
        [("A game costs $2. You win $10 with probability 0.15. Find the expected net gain.", ["Expected prize = 10 × 0.15 = $1.50", "$1.50 − $2"], MINUS + "$0.50"),
         ("A seed sprouts with probability 0.8. Find <i>P</i>(exactly 3 of 4 sprout).", ["<sub>4</sub>C<sub>3</sub>(0.8)³(0.2)¹", "= 4 × 0.512 × 0.2"], "0.4096")],
        ["Averaging the values without using the probabilities.",
         "Forgetting to subtract the cost to play.",
         "Leaving out <sub><i>n</i></sub>C<sub><i>k</i></sub> in a binomial probability.",
         "Choosing an option by the size of the prize alone."])
    faq = [("How do you calculate expected value?", "Multiply each outcome by its probability and add the products: E(X) = Σ x · P(x)."),
           ("What is a fair game?", "A game whose expected net gain is 0, so on average you neither win nor lose money."),
           ("What is the expected value of a binomial distribution?", "E(X) = np, where n is the number of trials and p is the probability of success."),
           ("How is expected value used to make decisions?", "Compare the expected gain or cost of each choice, such as a warranty price against the expected cost of repairs.")]
    make("expected-value", 15, "S-MD.A.2",
         "Probability Distributions and Expected Value",
         "Expected Value Worksheet: Probability Distributions, Games, Binomial | 100 Questions",
         "Expected Value",
         "Calculate the expected value of a random variable; interpret it as the mean of the probability distribution.",
         "Free precalculus worksheet on probability distributions and expected value: tables, games, fair games, binomial probabilities, insurance and warranties. 100 questions.",
         "E(X) = Σ x · P(x), the long-run average.",
         "Use net gain for games; a fair game has E(X) = 0.",
         body, faq, sets, R, domain="Probability", grade=GRADE)


if __name__ == "__main__":
    build()
