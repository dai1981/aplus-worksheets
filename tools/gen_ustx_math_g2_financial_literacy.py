# -*- coding: utf-8 -*-
"""
Texas Grade 2 Math: Saving, Spending, Borrowing and Producers (TEKS 2.11A–2.11F)
  python3 tools/gen_ustx_math_g2_financial_literacy.py
Saving money over time, saving or spending, deposits and withdrawals, responsible borrowing, lenders and
borrowers, and producers, consumers and the cost to make an item (own makers).
Wrong answers come from real mistakes: adding the saving only once, mixing up deposits and withdrawals, and
mixing up producers and consumers.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-2"

facts = g4f.facts


def one_save(r):
    k = Kid(r).next()
    a = r.choice([1, 2, 3, 4, 5, 10])
    n = r.randint(3, 10)
    start = r.choice([0, 0, r.randint(2, 20)])
    tot = start + a * n
    if start:
        return mcq("%s has $%d in a piggy bank. %s saves $%d each week for %d weeks. How much money is in the piggy bank now?" % (k["n"], start, k["He"], a, n), "$%d" % tot, ["$%d" % (start + a), "$%d" % (a * n), "$%d" % (tot + a)],
                   "%s + %s = <b>$%d</b>." % ("$%d" % start, " + ".join(["$%d" % a] * n), tot))
    return mcq("%s saves $%d each week. How much has %s saved after %d weeks?" % (k["n"], a, k["he"], n), "$%d" % (a * n), ["$%d" % (a + n), "$%d" % a, "$%d" % (a * (n - 1))],
               "%s = <b>$%d</b>." % (" + ".join(["$%d" % a] * n), a * n))


SAVE = [("Lily gets $10. She puts it in her piggy bank instead of buying candy. What did she choose?", "To save", ["To spend", "To borrow", "To lend"], "Keeping money for later is <b>saving</b>."),
        ("Why might someone save money instead of spending it?", "To buy something bigger later", ["To lose the money", "To owe money", "To make prices go up"], "Saving helps you buy bigger things later."),
        ("Marco buys a toy with his money. What did he do?", "He spent his money", ["He saved his money", "He borrowed money", "He made a deposit"], "Buying something is <b>spending</b>."),
        ("What is one good reason to save?", "To have money for something you need later", ["So you never buy anything", "To give it to the bank forever", "Because money grows on trees"], "Saving gives you money when you need it.")]

DEP = [("Sam puts $5 into his bank account. Is this a deposit or a withdrawal?", "A deposit", ["A withdrawal", "A loan", "A purchase"], "Putting money <b>in</b> is a <b>deposit</b>."),
       ("Mia takes $8 out of her savings account. Is this a deposit or a withdrawal?", "A withdrawal", ["A deposit", "A loan", "A gift"], "Taking money <b>out</b> is a <b>withdrawal</b>."),
       ("What is a deposit?", "Putting money into an account", ["Taking money out of an account", "Borrowing money", "Buying a toy"], "A <b>deposit</b> puts money in."),
       ("What is a withdrawal?", "Taking money out of an account", ["Putting money into an account", "Saving money", "Making something to sell"], "A <b>withdrawal</b> takes money out.")]


def one_bank(r):
    k = Kid(r).next()
    a = r.randint(10, 40)
    d = r.randint(2, 15)
    if r.random() < 0.5:
        return mcq("%s has $%d in the bank. %s makes a deposit of $%d. How much is in the bank now?" % (k["n"], a, k["He"], d), "$%d" % (a + d), ["$%d" % (a - d), "$%d" % d, "$%d" % (a + d + 1)],
                   "A deposit adds money: $%d + $%d = <b>$%d</b>." % (a, d, a + d))
    return mcq("%s has $%d in the bank. %s makes a withdrawal of $%d. How much is left in the bank?" % (k["n"], a, k["He"], d), "$%d" % (a - d), ["$%d" % (a + d), "$%d" % d, "$%d" % (a - d - 1)],
               "A withdrawal takes money out: $%d − $%d = <b>$%d</b>." % (a, d, a - d))


BORROW = [("Eli borrows a book from the library and returns it on time. Is this responsible borrowing?", "Yes, he returned it on time", ["No, borrowing is always bad", "No, he should keep it", "Yes, because he lost it"], "Returning what you borrow on time is <b>responsible</b>."),
          ("Zoe borrows $2 from her brother and never pays it back. Is this responsible borrowing?", "No, she did not pay it back", ["Yes, because it was only $2", "Yes, because he is her brother", "No, because she paid it back"], "Not paying back is <b>irresponsible</b>."),
          ("Who is the lender? Ana lends Ben her pencil.", "Ana", ["Ben", "The teacher", "Nobody"], "The person who gives something to borrow is the <b>lender</b>: Ana."),
          ("Who is the borrower? A bank lends money to Mr. Diaz to buy a truck.", "Mr. Diaz", ["The bank", "The truck", "Nobody"], "The one who gets the loan is the <b>borrower</b>: Mr. Diaz."),
          ("Which is an example of a lender?", "A bank that gives loans", ["A child who buys candy", "A store that sells toys", "A farmer who plants corn"], "Banks lend money, so they are <b>lenders</b>."),
          ("Which is an example of borrowing?", "Using a friend's scissors and giving them back", ["Buying a sandwich", "Saving coins", "Making a bracelet"], "Using something that belongs to someone else, then returning it, is <b>borrowing</b>."),
          ("Jack borrows his neighbor's rake and breaks it on purpose. Is this responsible?", "No, he did not take care of it", ["Yes, because he gave it back", "Yes, because rakes are cheap", "Yes, if he says sorry later"], "Responsible borrowers take care of what they borrow.")]

PROD = [("A baker makes bread to sell. Is the baker a producer or a consumer?", "A producer", ["A consumer", "A borrower", "A lender"], "People who make goods are <b>producers</b>."),
        ("Maya buys a loaf of bread. Is she a producer or a consumer?", "A consumer", ["A producer", "A lender", "A bank"], "People who buy goods are <b>consumers</b>."),
        ("Which person is a producer?", "A farmer who grows peaches", ["A boy who buys peaches", "A girl who eats peaches", "A child who eats a peach"], "A farmer grows food to sell: a <b>producer</b>."),
        ("Which person is a consumer?", "A family buying groceries", ["A farmer growing corn", "A baker baking pies", "A worker building chairs"], "Buying is what <b>consumers</b> do.")]


def one_cost(r):
    item = r.choice([("a bracelet", "beads", "string"), ("a bird feeder", "wood", "nails"), ("lemonade", "lemons", "cups"), ("a card", "paper", "stickers")])
    a, b = r.randint(2, 9), r.randint(1, 6)
    if r.random() < 0.5:
        return mcq("To make %s, Ella buys %s for $%d and %s for $%d. How much does it cost to make it?" % (item[0], item[1], a, item[2], b), "$%d" % (a + b), ["$%d" % (a - b if a > b else b - a), "$%d" % a, "$%d" % (a * b)],
                   "$%d + $%d = <b>$%d</b>." % (a, b, a + b))
    n = r.randint(2, 5)
    return mcq("It costs $%d to make one %s. How much does it cost to make %d?" % (a + b, item[0].replace("a ", ""), n), "$%d" % ((a + b) * n), ["$%d" % (a + b + n), "$%d" % (a + b), "$%d" % ((a + b) * (n - 1))],
               "%s = <b>$%d</b>." % (" + ".join(["$%d" % (a + b)] * n), (a + b) * n))


def build():
    sets, R = build_sets([
        ("Saving adds up over time", [("collect", one_save, 20)]),
        ("Saving or spending; deposits and withdrawals", [("collect", facts(SAVE), 4), ("collect", facts(DEP), 4), ("collect", one_bank, 12)]),
        ("Borrowing, lenders and borrowers", [("collect", facts(BORROW), 7), ("collect", one_bank, 13)]),
        ("Producers and consumers", [("collect", facts(PROD), 4), ("collect", one_cost, 16)]),
        ("Money stories", [("collect", one_save, 10), ("collect", one_cost, 10)]),
    ], 69220)
    finish(sets, R)
    body = lesson('<ul><li><b>Saving</b> means keeping money for later instead of spending it. Small amounts add up over time.</li><li>A <b>deposit</b> puts money into an account; a <b>withdrawal</b> takes money out.</li><li>A <b>lender</b> gives something to borrow; a <b>borrower</b> uses it and gives it back. Responsible borrowers return things on time.</li><li><b>Producers</b> make goods; <b>consumers</b> buy and use them.</li></ul>',
        [example("Save $3 a week for 5 weeks", ["$3 + $3 + $3 + $3 + $3"], "$15")],
        [['Adding the saving only once', 'Add it for every week.'], ['Mixing up deposits and withdrawals', 'Deposit = in. Withdrawal = out.'], ['Mixing up producers and consumers', 'Producers make; consumers buy.']])
    faq = [('What does TEKS 2.11 cover?', 'Saving over time, saving versus spending, deposits and withdrawals, borrowing, lenders and borrowers, and producers and consumers.'), ('Why is saving important?', 'It lets you buy bigger things and be ready for surprises.'), ('What makes borrowing responsible?', 'Taking care of what you borrow and paying or giving it back on time.'), ('How do you find the cost to make something?', 'Add the cost of everything you need to make it.')]
    make('personal-financial-literacy', 20, 'Personal Financial Literacy', '2.11A–2.11F',
         '2.11A calculate how money saved can accumulate into a larger amount over time; 2.11B explain that saving is an alternative to spending; 2.11C distinguish between a deposit and a withdrawal; 2.11D identify examples of borrowing and distinguish between responsible and irresponsible borrowing; 2.11E identify examples of lenders and borrowers; 2.11F differentiate between producers and consumers and calculate the cost to produce a simple item',
         'Saving, Spending, Borrowing and Producers', 'Personal Financial Literacy',
         'Free Grade 2 personal financial literacy worksheets for Texas TEKS 2.11: saving over time, saving or spending, deposits and withdrawals, borrowing, lenders and borrowers, producers and consumers. 100 questions with answers.',
         'Saving adds up; deposits go in, withdrawals come out.', 'Producers make things; consumers buy them.',
         body, faq, sets, seo_title='Grade 2 Personal Financial Literacy Worksheets: Saving and Spending (TEKS 2.11)')


if __name__ == "__main__":
    build()
