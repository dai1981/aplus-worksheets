# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Income, Wants and Needs, Saving and Giving (TEKS 1.9A–1.9D)
  python3 tools/gen_ustx_math_g1_financial_literacy.py
Income from work, goods and services, wants and needs, spending and saving, and charitable giving (own makers).
Wrong answers come from real mistakes: calling a gift income, mixing up wants and needs, and mixing up saving and
spending.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-1"

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


facts = g4f.facts

INC = [("Mom works at a bakery and gets paid. What is the money she earns called?", "Income", ["A gift", "A loan", "Change"], "Money earned from work is <b>income</b>."),
       ("Which is an example of income?", "Money earned for mowing a lawn", ["Money found on the street", "Money borrowed from a friend", "A toy from a store"], "Money you <b>earn</b> by working is income."),
       ("Why do people work?", "To earn income to buy things they need and want", ["To lose money", "To spend all day at a store", "To borrow money"], "Work earns <b>income</b>."),
       ("Which person earns income?", "A nurse who works at a hospital", ["A baby who sleeps", "A cat that plays", "A child who opens a present"], "A nurse is paid for work: <b>income</b>."),
       ("What can income be used for?", "To buy goods and services", ["Only to throw away", "Nothing", "Only to give back"], "Income buys <b>goods and services</b>.")]

GS = [("an apple", "good"), ("a haircut", "service"), ("a pair of shoes", "good"), ("a doctor visit", "service"), ("a book", "good"), ("a car wash", "service"),
      ("a toy truck", "good"), ("a bus ride", "service"), ("a backpack", "good"), ("a dentist cleaning teeth", "service"), ("a loaf of bread", "good"), ("a dog groomer washing a dog", "service"),
      ("a jacket", "good"), ("a teacher teaching a class", "service"), ("a box of crayons", "good"), ("a plumber fixing a sink", "service")]


def one_gs(r):
    thing, kind = r.choice(GS)
    other = "service" if kind == "good" else "good"
    e = "A good is a thing you can hold." if kind == "good" else "A service is work someone does for you."
    return mcq("%s: is it a good or a service?" % (thing[0].upper() + thing[1:]), "A " + kind, ["A " + other, "Income", "A gift"], "%s It is <b>a %s</b>." % (e, kind))


WN = [("food", "need"), ("water", "need"), ("a coat in winter", "need"), ("a place to live", "need"), ("medicine when you are sick", "need"), ("shoes", "need"),
      ("a video game", "want"), ("candy", "want"), ("a toy robot", "want"), ("a new bike when you already have one", "want"), ("a movie ticket", "want"), ("a trip to the zoo", "want"),
      ("a soccer ball", "want"), ("stickers", "want"), ("clean clothes", "need"), ("a bed to sleep in", "need")]


def one_wn(r):
    thing, kind = r.choice(WN)
    e = "A need is something you must have to live and be safe." if kind == "need" else "A want is something nice to have, but you can live without it."
    return mcq("%s: is it a want or a need?" % (thing[0].upper() + thing[1:]), "A " + kind, ["A " + ("want" if kind == "need" else "need"), "A service", "Income"], "%s So it is <b>a %s</b>." % (e, kind))


CHOOSE = [("Ana has $5. She needs a lunch box and wants a toy. Both cost $5. What should she buy first?", "The lunch box", ["The toy", "Both", "Nothing ever"], "Needs come before wants: <b>the lunch box</b>."),
          ("Which is a need?", "Food", ["A video game", "Candy", "A toy car"], "<b>Food</b> is a need."),
          ("Which is a want?", "A toy robot", ["Water", "A coat in winter", "A place to live"], "<b>A toy robot</b> is a want.")]

SAVE = [("Ben puts $3 in his piggy bank to use later. Is he saving or spending?", "Saving", ["Spending", "Borrowing", "Earning"], "Keeping money for later is <b>saving</b>."),
        ("Kim buys a snack with her money. Is she saving or spending?", "Spending", ["Saving", "Giving", "Earning"], "Buying something is <b>spending</b>."),
        ("Why might you save money?", "To buy something bigger later", ["So you can never use it", "To lose it", "To make it disappear"], "Saving helps you buy bigger things later."),
        ("Which is spending?", "Paying for a book", ["Putting coins in a bank", "Keeping money in a jar", "Saving for a bike"], "Paying for something is <b>spending</b>.")]


def one_save(r):
    k = Kid(r).next()
    a = r.randint(6, 20)
    b = r.randint(1, a - 1)
    if r.random() < 0.5:
        return mcq("%s has $%d. %s spends $%d and saves the rest. How much does %s save?" % (k["n"], a, k["He"], b, k["he"]), "$%d" % (a - b), ["$%d" % (a + b), "$%d" % b, "$%d" % (a - b + 1)],
                   "$%d − $%d = <b>$%d</b> saved." % (a, b, a - b))
    c = r.randint(1, 20 - a) if a < 20 else None
    if not c:
        raise AssertionError
    return mcq("%s has saved $%d. %s saves $%d more. How much has %s saved now?" % (k["n"], a, k["He"], c, k["he"]), "$%d" % (a + c), ["$%d" % (a - c) if a > c else "$%d" % (a + c + 2), "$%d" % c, "$%d" % (a + c + 1)],
               "$%d + $%d = <b>$%d</b>." % (a, c, a + c))


def one_income(r):
    k = Kid(r).next()
    job = r.choice(["walking dogs", "pulling weeds", "washing cars", "selling lemonade", "raking leaves"])
    a, b = r.randint(2, 9), r.randint(2, 9)
    if a + b > 20:
        raise AssertionError
    return mcq("%s earns $%d on Saturday and $%d on Sunday for %s. How much income does %s earn in all?" % (k["n"], a, b, job, k["he"]), "$%d" % (a + b), ["$%d" % abs(a - b) if a != b else "$1", "$%d" % a, "$%d" % (a + b + 1)],
               "Income is money earned: $%d + $%d = <b>$%d</b>." % (a, b, a + b))


GIVE = [("Ava gives some of her toys to children who need them. What is this called?", "Charitable giving", ["Spending", "Borrowing", "Earning"], "Giving to help others is <b>charitable giving</b>."),
        ("Which is an example of charitable giving?", "Giving canned food to a food bank", ["Buying a toy for yourself", "Saving coins in a jar", "Borrowing a pencil"], "Helping others for free is <b>charitable giving</b>."),
        ("Why do people give to charity?", "To help people in need", ["To get more toys", "To borrow money", "To earn income"], "People give to <b>help others</b>."),
        ("Leo puts $1 of his allowance in a jar for an animal shelter. What is he doing?", "Charitable giving", ["Spending on himself", "Earning income", "Borrowing"], "He is giving to help animals: <b>charitable giving</b>."),
        ("Which is NOT charitable giving?", "Buying candy for yourself", ["Donating old coats", "Giving books to a library", "Helping at a food bank"], "Buying for yourself is <b>spending</b>, not giving.")]


def one_give(r):
    k = Kid(r).next()
    thing = r.choice(["cans of food", "books", "toys", "coats", "dollars"])
    a = r.randint(6, 20)
    b = r.randint(1, a - 1)
    if thing == "dollars":
        return mcq("%s has $%d. %s gives $%d to a charity. How much does %s have left?" % (k["n"], a, k["He"], b, k["he"]), "$%d" % (a - b), ["$%d" % (a + b), "$%d" % b, "$%d" % (a - b - 1) if a - b > 1 else "$%d" % (a - b + 2)],
                   "$%d − $%d = <b>$%d</b>." % (a, b, a - b))
    return mcq("%s has %d %s. %s gives %d to a charity. How many %s does %s have left?" % (k["n"], a, thing, k["He"], b, thing, k["he"]), str(a - b), [str(a + b), str(b), str(a - b + 1)],
               "%d − %d = <b>%d</b>." % (a, b, a - b))


def build():
    sets, R = build_sets([
        ("Income: money earned", [("collect", uniq(facts(INC)), 5), ("collect", uniq(one_income), 15)]),
        ("Goods and services", [("collect", uniq(one_gs), 16), ("collect", uniq(one_income), 4)]),
        ("Wants and needs", [("collect", uniq(one_wn), 16), ("collect", uniq(facts(CHOOSE)), 3), ("collect", uniq(one_income), 1)]),
        ("Spending and saving", [("collect", uniq(facts(SAVE)), 4), ("collect", uniq(one_save), 16)]),
        ("Charitable giving", [("collect", uniq(facts(GIVE)), 5), ("collect", uniq(one_give), 15)]),
    ], 69120)
    finish(sets, R)
    body = lesson('<ul><li><b>Income</b> is money people earn by working.</li><li>Income buys <b>goods</b> (things) and <b>services</b> (work someone does for you).</li><li>A <b>need</b> is something you must have. A <b>want</b> is nice to have.</li><li><b>Saving</b> keeps money for later; <b>spending</b> uses it now.</li><li><b>Charitable giving</b> means giving to help others.</li></ul>',
        [example("Earn $5 and $4", ["$5 + $4"], "$9 income")],
        [['Calling a gift income', 'Income is earned by working.'], ['Mixing up wants and needs', 'Ask: can I live without it?'], ['Mixing up saving and spending', 'Saving keeps money; spending uses it.']])
    faq = [('What does TEKS 1.9A ask?', 'Define money earned as income.'), ('What does TEKS 1.9B ask?', 'Identify income as a means of obtaining goods and services, oftentimes making choices between wants and needs.'), ('What does TEKS 1.9C ask?', 'Distinguish between spending and saving.'), ('What does TEKS 1.9D ask?', 'Consider charitable giving.')]
    make('personal-financial-literacy', 20, 'Personal Financial Literacy', '1.9A–1.9D',
         '1.9A define money earned as income; 1.9B identify income as a means of obtaining goods and services, oftentimes making choices between wants and needs; 1.9C distinguish between spending and saving; 1.9D consider charitable giving',
         'Income, Wants and Needs, Saving and Giving', 'Personal Financial Literacy',
         'Free Grade 1 personal financial literacy worksheets for Texas TEKS 1.9: income, goods and services, wants and needs, spending and saving and charitable giving. 100 questions with answers.',
         'Income is money earned; needs come before wants.', 'Save for later, spend now, give to help.',
         body, faq, sets, seo_title='Grade 1 Personal Financial Literacy Worksheets: Wants and Needs (TEKS 1.9)')


if __name__ == "__main__":
    build()
