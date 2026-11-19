# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: Earning Income, Gifts, Job Skills, Wants and Needs (TEKS K.9A–K.9D)
  python3 tools/gen_ustx_math_gk_financial_literacy.py
Ways to earn income, income or a gift, skills for jobs, wants and needs (the Texas Grade 1 maker), and using income
for needs first (own makers).
Wrong answers come from real mistakes: calling a gift income, and mixing up wants and needs.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g1_financial_literacy as f1
tx_common.GRADE = "kindergarten"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


USED = {}


def pick(r, pool, tag):
    """Each pool item is used once, so no question repeats with only a name changed."""
    if tag not in USED:
        USED[tag] = list(pool)
        r.shuffle(USED[tag])
    if not USED[tag]:
        raise AssertionError("pool used up")
    return USED[tag].pop()

JOBS = [("a baker", "bakes bread"), ("a nurse", "takes care of sick people"), ("a firefighter", "puts out fires"), ("a teacher", "teaches children"), ("a farmer", "grows food"),
        ("a bus driver", "drives a bus"), ("a mail carrier", "brings the mail"), ("a vet", "helps sick animals"), ("a chef", "cooks food"), ("a builder", "builds houses"),
        ("a librarian", "helps people find books"), ("a pilot", "flies a plane"), ("a dentist", "cleans teeth"), ("a police officer", "keeps people safe"), ("a mechanic", "fixes cars")]
NOT = ["playing at the park", "sleeping", "watching a cartoon", "eating lunch", "opening a present", "taking a bath", "riding a swing"]
MALE = ("dad", "uncle", "grandpa")


def one_earn(r):
    (job, does), br = pick(r, [(j, b) for j in JOBS for b in (0, 1)], "earn")
    k = Kid(r).next()
    if br == 0:
        rel = r.choice(["mom", "dad", "aunt", "uncle", "grandma", "grandpa"])
        return mcq("%s's %s is %s. %s %s and gets paid. What is the money called?" % (k["n"], rel, job, "He" if rel in MALE else "She", does), "Income", ["A gift", "A loan", "A toy"],
                   "Money earned by working is <b>income</b>.")
    w = r.sample(NOT, 3)
    return mcq("%s wants to earn income when %s grows up. Which would earn income?" % (k["n"], k["he"]), "Working as %s" % job, [x[0].upper() + x[1:] for x in w],
               "People earn income by <b>working</b>. %s %s." % (job[0].upper() + job[1:], does))


ITEMS = [("$5 for helping a neighbor rake leaves", "income"), ("$10 from Grandma for a birthday", "gift"), ("$3 for walking a neighbor's dog", "income"), ("$2 in a holiday card", "gift"),
         ("money for selling lemonade", "income"), ("a toy from a friend", "gift"), ("money a parent earns at work", "income"), ("$1 from the tooth fairy", "gift"),
         ("pay for washing a neighbor's car", "income"), ("$20 from an uncle for a birthday", "gift"), ("money for pulling weeds for a neighbor", "income"), ("a present at a party", "gift"),
         ("$4 for feeding a neighbor's cat", "income"), ("a new book from an aunt", "gift"), ("money for selling cookies at a bake sale", "income"), ("$5 in a graduation card", "gift"),
         ("pay for shoveling a neighbor's sidewalk", "income"), ("a sweater from Grandpa", "gift"), ("money for selling old toys at a yard sale", "income"), ("$2 from a cousin for no reason", "gift"),
         ("money for helping at a family store", "income"), ("a balloon from a friend", "gift"), ("pay for watering a neighbor's plants", "income"), ("a gift card for a birthday", "gift")]


def one_gift(r):
    thing, kind = pick(r, ITEMS, "gift")
    k = Kid(r).next()
    other = "A gift" if kind == "income" else "Income"
    right = "Income" if kind == "income" else "A gift"
    e = "It was earned by working." if kind == "income" else "It was given, not earned."
    return mcq("%s gets %s. Is it income or a gift?" % (k["n"], thing), right, [other, "A loan", "A bill"], "%s It is <b>%s</b>." % (e, right.lower() if kind == "gift" else "income"))


SKILL = [("a baker", "Knowing how to measure and bake"), ("a nurse", "Caring for sick people"), ("a bus driver", "Driving safely"), ("a teacher", "Reading and explaining"),
         ("a farmer", "Planting and growing food"), ("a chef", "Cooking"), ("a builder", "Using tools"), ("a vet", "Caring for animals"), ("a mail carrier", "Reading addresses"),
         ("a firefighter", "Staying calm and strong"), ("a librarian", "Sorting books"), ("a pilot", "Flying a plane"), ("a dentist", "Caring for teeth"), ("a police officer", "Helping people stay safe"),
         ("a mechanic", "Fixing engines")]


def one_skill(r):
    job, sk = pick(r, SKILL, "skill")
    others = [x for j, x in SKILL if j != job]
    k = Kid(r).next()
    return mcq("%s wants to be %s. Which skill will %s need?" % (k["n"], job, k["he"]), sk, r.sample(others, 3), "%s needs <b>%s</b>." % (job[0].upper() + job[1:], sk[0].lower() + sk[1:]))


PAIRS = [("food", "a toy"), ("a coat", "candy"), ("shoes", "a video game"), ("water", "stickers"), ("medicine", "a balloon"), ("a toothbrush", "a toy car"),
         ("milk", "a movie ticket"), ("a warm blanket", "a kite"), ("soap", "a comic book"), ("rain boots", "a yo-yo"), ("bread", "a doll"), ("a winter hat", "bubble gum"),
         ("vegetables", "a puzzle"), ("socks", "a robot"), ("a bed", "a game"), ("eggs", "a jump rope")]


def one_use(r):
    need, want = pick(r, PAIRS, "use")
    k = Kid(r).next()
    who = r.choice(["mom", "dad", "family", "grandma", "aunt"])
    return mcq("%s's %s earns income. It can buy %s or %s. Which should come first?" % (k["n"], who, need, want), need[0].upper() + need[1:], [want[0].upper() + want[1:], "Neither", "Nothing"],
               "Income is used for <b>needs</b> first. %s is a need." % (need[0].upper() + need[1:]))


def build():
    sets, R = build_sets([
        ("Ways to earn income", [("collect", one_earn, 20)]),
        ("Income or a gift?", [("collect", one_gift, 20)]),
        ("Skills for jobs", [("collect", one_skill, 15), ("collect", one_use, 5)]),
        ("Wants and needs", [("collect", uniq(f1.one_wn), 16), ("collect", one_use, 4)]),
        ("Using income for needs and wants", [("collect", one_use, 7), ("collect", one_earn, 10), ("collect", one_gift, 3)]),
    ], 69016)
    finish(sets, R)
    body = lesson('<ul><li>People <b>earn income</b> by working at jobs.</li><li>A <b>gift</b> is given to you. It is not earned.</li><li>Jobs need <b>skills</b>, like cooking or driving safely.</li><li>A <b>need</b> is something you must have. A <b>want</b> is nice to have. Income pays for needs first.</li></ul>',
        [example("$5 for raking leaves", ["earned by working"], "income")],
        [['Calling a gift income', 'Income is earned.'], ['Mixing up wants and needs', 'Ask: can I live without it?'], ['Thinking money just appears', 'People work to earn it.']])
    faq = [('What does TEKS K.9A ask?', 'Identify ways to earn income.'), ('What does TEKS K.9B ask?', 'Differentiate between money received as income and money received as gifts.'), ('What does TEKS K.9C ask?', 'List simple skills required for jobs.'), ('What does TEKS K.9D ask?', "Distinguish between wants and needs and identify income as a source to meet one's wants and needs.")]
    make('personal-financial-literacy', 16, 'Personal Financial Literacy', 'K.9A–K.9D',
         "K.9A identify ways to earn income; K.9B differentiate between money received as income and money received as gifts; K.9C list simple skills required for jobs; K.9D distinguish between wants and needs and identify income as a source to meet one's wants and needs",
         'Earning Income, Gifts, Job Skills, Wants and Needs', 'Personal Financial Literacy',
         'Free kindergarten personal financial literacy worksheets for Texas TEKS K.9: ways to earn income, income or a gift, job skills, and wants and needs. 100 questions with answers.',
         'Income is earned by working; a gift is given.', 'Needs come before wants.',
         body, faq, sets, seo_title='Kindergarten Personal Financial Literacy Worksheets: Income and Gifts (TEKS K.9)')


if __name__ == "__main__":
    build()
