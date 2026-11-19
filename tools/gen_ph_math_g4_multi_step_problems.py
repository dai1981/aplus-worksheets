# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Multi-Step Word Problems with the Four Operations and Money (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_multi_step_problems.py
Shopping with pesos and change, multi-step problems with the four operations, writing a number sentence for a
situation (own makers), and comparing quantities in two steps (US Grade 4 maker with Filipino names).
Wrong answers come from real mistakes: doing only the first step, adding when the story takes away, and forgetting
that the bill is bigger than the cost.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g4_comparison_problems as usc
adopt(usc)
if hasattr(usc, 'R'): usc.R = random.Random(704090)
ph_common.GRADE = "grade-4"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


ITEMS = [("pandesal", 5, "piece"), ("notebook", 35, "notebook"), ("pencil", 12, "pencil"), ("ballpen", 15, "ballpen"), ("bottle of water", 20, "bottle"),
         ("pack of crayons", 65, "pack"), ("banana cue", 25, "stick"), ("kilo of rice", 52, "kilo"), ("egg", 9, "egg"), ("can of sardines", 28, "can"),
         ("bag of chips", 18, "bag"), ("ice candy", 10, "piece"), ("mango", 45, "mango"), ("loaf of bread", 75, "loaf"), ("pad paper", 30, "pad"), ("eraser", 8, "eraser")]
BILLS = [50, 100, 200, 500, 1000]


def plural(word, n):
    if n == 1:
        return word
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    if word.endswith(("s", "sh", "ch", "x")):
        return word + "es"
    return word + "s"


def thing(name, n):
    """3 notebooks, 2 bottles of water, 1 kilo of rice"""
    if " of " in name:
        a, b = name.split(" of ", 1)
        return "%d %s of %s" % (n, plural(a, n), b)
    if name in ("pandesal", "banana cue", "ice candy"):
        return "%d %s" % (n, name if n == 1 else {"pandesal": "pandesal", "banana cue": "sticks of banana cue", "ice candy": "ice candies"}[name])
    return "%d %s" % (n, plural(name, n))


def one_shop(r):
    k = Kid(r).next()
    (a, pa, _), (b, pb, _) = r.sample(ITEMS, 2)
    na, nb = r.randint(2, 6), r.randint(1, 5)
    cost = na * pa + nb * pb
    bill = min(x for x in BILLS if x > cost)
    kind = r.choice(["cost", "change", "change"])
    q = "%s buys %s at %s each and %s at %s each at a sari-sari store." % (k["n"], thing(a, na), peso(pa), thing(b, nb), peso(pb))
    if kind == "cost":
        q += " How much does %s pay?" % k["he"]
        right, w = cost, [na * pa, pa + pb, (na + nb) * max(pa, pb)]
        e = "%d × %s = %s and %d × %s = %s. %s + %s = <b>%s</b>." % (na, peso(pa), peso(na * pa), nb, peso(pb), peso(nb * pb), peso(na * pa), peso(nb * pb), peso(cost))
    else:
        q += " %s pays with a %s bill. How much change does %s get?" % (k["He"], peso(bill), k["he"])
        right, w = bill - cost, [cost, bill - na * pa, bill - pa - pb]
        e = "Cost: %s + %s = %s. Change: %s − %s = <b>%s</b>." % (peso(na * pa), peso(nb * pb), peso(cost), peso(bill), peso(cost), peso(bill - cost))
    return mcq(q, peso(right), [peso(x) for x in w if x != right and x > 0] + [peso(right + 10)], e)


MS = [
    ("A jeepney ride costs %(a)s per person. %(n)s and %(m)d friends ride to school and back home. How much do they pay in all?", lambda v: v["a"] * (v["m"] + 1) * 2, lambda v: [v["a"] * (v["m"] + 1), v["a"] * v["m"] * 2, v["a"] * 2]),
    ("A school orders %(m)d boxes of chalk. Each box has %(b)d pieces. The teachers use %(c)d pieces. How many pieces are left?", lambda v: v["m"] * v["b"] - v["c"], lambda v: [v["m"] * v["b"], v["m"] + v["b"] - v["c"], v["m"] * v["b"] + v["c"]]),
    ("A farmer harvests %(c)d kilograms of rice. He sells %(b)d kilograms and packs the rest equally into %(m)d sacks. How many kilograms are in each sack?", None, None),
    ("%(n)s saves %(a)s every week for %(m)d weeks. Then %(he)s buys a bag for %(c)s. How much money is left?", lambda v: v["a"] * v["m"] - v["c"], lambda v: [v["a"] * v["m"], v["a"] * v["m"] + v["c"], v["c"] - v["a"]]),
    ("A bakery makes %(c)d pieces of pandesal. It puts them in bags of %(m)d and sells each bag for %(a)s. How much money does it get for all the bags?", None, None),
    ("A class of %(c)d learners goes on a field trip. Each bus holds %(m)d learners. Each bus costs %(a)s. What is the total cost of the buses?", None, None),
]


def one_ms(r):
    k = Kid(r).next()
    i = r.randrange(len(MS))
    t = MS[i][0]
    v = {"n": k["n"], "he": k["he"]}
    if i == 0:
        v.update(a=r.choice([13, 14, 15]), m=r.randint(2, 6))
        f, wf = MS[0][1], MS[0][2]
        right = f(v)
        e = "%d people ride, twice: %d × 2 = %d rides. %d × %s = <b>%s</b>." % (v["m"] + 1, v["m"] + 1, 2 * (v["m"] + 1), 2 * (v["m"] + 1), peso(v["a"]), peso(right))
        txt = t % dict(v, a=peso(v["a"]))
        return mcq(txt, peso(right), [peso(x) for x in wf(v) if x != right], e)
    if i == 1:
        v.update(m=r.randint(12, 40), b=r.choice([10, 12, 20, 24, 50]))
        v["c"] = r.randint(v["m"] * v["b"] // 4, v["m"] * v["b"] - 10)
        right = MS[1][1](v)
        e = "%d × %d = %s pieces. %s − %s = <b>%s</b>." % (v["m"], v["b"], comma(v["m"] * v["b"]), comma(v["m"] * v["b"]), comma(v["c"]), comma(right))
        return mcq(t % v, right, MS[1][2](v), e)
    if i == 2:
        m = r.randint(3, 9)
        each = r.randint(25, 120)
        b = r.randint(100, 900)
        v.update(c=m * each + b, b=b, m=m)
        right = each
        e = "%s − %s = %s kg left. %s ÷ %d = <b>%d</b> kg." % (comma(v["c"]), comma(b), comma(m * each), comma(m * each), m, each)
        return mcq(t % v, right, [v["c"] // m, (v["c"] + b) // m, m * each], e)
    if i == 3:
        v.update(a=r.choice([20, 25, 50, 75, 100, 150]), m=r.randint(4, 15))
        v["c"] = r.randint(v["a"], v["a"] * v["m"] - 10)
        right = MS[3][1](v)
        e = "%d × %s = %s saved. %s − %s = <b>%s</b>." % (v["m"], peso(v["a"]), peso(v["a"] * v["m"]), peso(v["a"] * v["m"]), peso(v["c"]), peso(right))
        return mcq(t % dict(v, a=peso(v["a"]), c=peso(v["c"])), peso(right), [peso(x) for x in MS[3][2](v) if x > 0 and x != right] + [peso(right + 50)], e)
    if i == 4:
        m = r.choice([5, 6, 8, 10, 12])
        bags = r.randint(15, 90)
        a = r.choice([20, 25, 30, 40, 50])
        v.update(c=m * bags, m=m)
        right = bags * a
        e = "%s ÷ %d = %d bags. %d × %s = <b>%s</b>." % (comma(m * bags), m, bags, bags, peso(a), peso(right))
        return mcq(t % dict(v, a=peso(a)), peso(right), [peso(m * bags * a), peso(bags + a), peso(bags * a // 2)], e)
    m = r.choice([40, 45, 50, 55, 60])
    buses = r.randint(2, 6)
    c = m * buses - r.randint(0, m - 5)
    a = r.choice([3500, 4000, 4500, 5000, 6000])
    v.update(c=c, m=m)
    need = -(-c // m)
    right = need * a
    e = "%d ÷ %d = %d remainder %d, so %d buses are needed (the extra learners need a bus too). %d × %s = <b>%s</b>." % (c, m, c // m, c % m, need, need, peso(a), peso(right))
    if c % m == 0:
        raise AssertionError
    return mcq(t % dict(v, a=peso(a)), peso(right), [peso((c // m) * a), peso(c * a), peso(a)], e)


def one_sent(r):
    k = Kid(r).next()
    kind = r.choice(["ms", "md", "share", "both"])
    a, b, c = r.randint(12, 90), r.randint(2, 9), r.randint(5, 60)
    if kind == "ms":
        q = "%s has %d stickers. %s buys %d packs with %d stickers each. Which number sentence shows how many stickers %s has now?" % (k["n"], c, k["He"], b, a, k["he"])
        right, w = "%d + %d × %d = N" % (c, b, a), ["%d × %d × %d = N" % (c, b, a), "(%d + %d) × %d = N" % (c, b, a), "%d + %d + %d = N" % (c, b, a)]
    elif kind == "md":
        f = c % a + 1 if c % a else 1
        q = "%d learners need tables. Each table seats %d learners. %d tables are already set up. Which number sentence shows how many more tables are needed?" % (a * b, b, f)
        right, w = "%d ÷ %d − %d = N" % (a * b, b, f), ["%d − %d ÷ %d = N" % (a * b, b, f), "%d × %d − %d = N" % (a * b, b, f), "%d ÷ %d + %d = N" % (a * b, b, f)]
    elif kind == "share":
        q = "%s buys %d mangoes for %s and shares them equally with %d friends, so %d people get mangoes. Which number sentence shows how many mangoes each person gets?" % (k["n"], (b + 1) * c, peso(a * 10), b, b + 1)
        right, w = "%d ÷ %d = N" % ((b + 1) * c, b + 1), ["%d ÷ %d = N" % ((b + 1) * c, b), "%d × %d = N" % ((b + 1) * c, b + 1), "%d − %d = N" % ((b + 1) * c, b + 1)]
    else:
        q = "A box has %d rows of %d eggs. %d eggs are broken. Which number sentence shows how many eggs are not broken?" % (b, a % 10 + 3, c % 7 + 2)
        rr, cc, br = b, a % 10 + 3, c % 7 + 2
        right, w = "%d × %d − %d = N" % (rr, cc, br), ["%d + %d − %d = N" % (rr, cc, br), "%d × %d + %d = N" % (rr, cc, br), "%d − %d × %d = N" % (rr * cc, br, rr)]
    return mcq(q, right, w, "Write the steps in the order of the story, and use × or ÷ for equal groups. <b>%s</b>." % right)


def build():
    sets, R = build_sets([
        ("Shopping with pesos", [("collect", uniq(one_shop), 20)]),
        ("Two-step problems", [("collect", uniq(one_ms), 20)]),
        ("Write a number sentence", [("collect", uniq(one_sent), 20)]),
        ("Compare with more and times", [("run", usc.set_more_or_times, ("rnd", usc.People), 20)]),
        ("Multi-step problems", [("run", usc.set_multistep, ("rnd", usc.People), 20)]),
    ], 70409)
    finish(sets, R)
    body = lesson('<ul><li>Read the problem and find what is asked.</li><li>Plan the steps: what must you find first?</li><li>Use + to join, − to take away or compare, × for equal groups, ÷ to share or group equally.</li><li>Write a number sentence, solve it, and check that the answer makes sense (change is less than the bill).</li></ul>',
        [example("3 notebooks at ₱35 and 2 pencils at ₱12; pay with ₱200", ["3 × 35 = 105, 2 × 12 = 24", "105 + 24 = 129", "200 − 129"], "₱71 change")],
        [['Doing only the first step', 'Check that you answered the question asked.'], ['Adding when the story takes away', 'Look for words like left, change, gave away.'], ['Change bigger than the bill', 'Change is always less than the money paid.']])
    faq = [('What does MATATAG Math 4 ask about word problems?', 'Solve multi-step problems involving one or more of the four operations with results of calculations up to 1 000 000, including problems involving money, and represent situations using a number sentence.'), ('What is a number sentence?', 'An equation like 3 × 35 + 24 = N that shows the steps.'), ('How do I find the change?', 'Subtract the total cost from the money paid.'), ('Why estimate first?', 'It helps you spot answers that are far too big or small.')]
    make('multi-step-word-problems-and-money', 9, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Solve multi-step problems involving one or more of the four operations with results of calculations up to 1 000 000, including problems involving money; represent situations involving one or more of the four operations using a number sentence.',
         'Multi-Step Word Problems with the Four Operations and Money', 'Multi-Step Word Problems',
         'Free Grade 4 word problem worksheets for the DepEd MATATAG curriculum: shopping with pesos and change, multi-step problems with the four operations and number sentences. 100 questions with answers.',
         'Plan the steps, then solve one at a time.', 'Change = money paid − total cost.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
