# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Personal Financial Literacy (TEKS 3.9A–3.9F)
  python3 tools/gen_ustx_math_g3_financial_literacy.py
Work, skills and income (human capital), scarcity and cost, planned and unplanned spending, credit and paying
it back with interest, and saving plans and money decisions (income, spending, saving, credit, giving).
Each set mixes idea questions with small money calculations within 1,000.
Wrong answers come from real mistakes: thinking income comes without work, thinking a scarce item gets cheaper,
thinking credit is free money, and forgetting the interest when paying back a loan.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, lesson, S, example)

R = random.Random(62101)


def facts(lst):
    """Item makers from fixed idea questions: (question, right, [wrong...], explanation)."""
    def maker(r):
        q, a, w, e = r.choice(lst)
        w = list(w)
        r.shuffle(w)
        return mcq(q, a, w, e)
    return maker


# ------------------------------------------------------------ set 1: work, skills and income (3.9A)
WORK = [("What is income?", "Money a person earns, usually from work", ["Money a person spends at a store", "Money a person borrows", "Money a person gives away"],
         "<b>Income</b> is money you earn, usually by working."),
        ("What is human capital?", "The skills and knowledge a person has", ["The money in a bank", "The city where a person lives", "The things a person owns"],
         "Human capital is <b>the skills and knowledge a person has</b>. More skills can lead to a higher income."),
        ("Why does a dentist usually earn more per hour than a dog walker?", "A dentist needs many years of school and special skills", ["A dentist works outdoors", "Dentists are taller", "Dog walking is not a real job"],
         "Jobs that need more training and skills (human capital) often pay more."),
        ("Mia goes to a coding class to learn new skills. How might this help her later?", "She may be able to get a job that pays more", ["She will never need to work", "She will have to pay more taxes on toys", "It will make things cost less"],
         "Learning skills builds human capital, which can lead to <b>a job that pays more</b>."),
        ("Which is an example of labor?", "Mowing a neighbor's lawn", ["Watching TV", "Finding a coin on the ground", "Getting a birthday gift"],
         "Labor is work people do. <b>Mowing a neighbor's lawn</b> is work that can earn income."),
        ("Which is a way to earn income?", "Selling lemonade you made", ["Borrowing money from a friend", "Buying a new game", "Using a credit card"],
         "Selling something you made is a way to <b>earn</b> money."),
        ("A mechanic fixes cars. What does she use to earn her income?", "Her skills and her time", ["Her bank card", "Her savings account", "Her neighbors' money"],
         "She uses <b>her skills and her time</b> (human capital and labor) to earn income.")]


def one_work_math(r):
    k = Kid(r).next()
    job, pay = r.choice([("walks dogs", r.choice([4, 5, 6])), ("rakes leaves", r.choice([6, 7, 8])), ("washes cars", r.choice([5, 8, 10])), ("feeds a neighbor's cat", r.choice([3, 4, 5]))])
    n = r.randint(3, 9)
    return mcq("%s %s and earns $%d each time. %s does it %d times. How much income does %s earn?" % (k["n"], job, pay, k["He"], n, k["he"]), "$%d" % (pay * n),
               ["$%d" % (pay + n), "$%d" % (pay * n - pay), "$%d" % (pay * n + pay)], "$%d × %d = <b>$%d</b> of income from work." % (pay, n, pay * n))


def one_work(r):
    return facts(WORK)(r) if r.random() < 0.4 else one_work_math(r)


# ------------------------------------------------------------ set 2: scarcity and cost (3.9B)
SCARCE = [("A storm ruins most of the orange crop. What will most likely happen to the price of oranges?", "It will go up", ["It will go down", "It will stay the same", "Oranges will be free"],
           "When something becomes <b>scarce</b> (hard to get), its price usually <b>goes up</b>."),
          ("A new toy is so popular that stores run out of it. What happens to its price online?", "It goes up", ["It goes down", "It becomes free", "It stays the same forever"],
           "Many people want it and there are few left, so the price <b>goes up</b>."),
          ("A farm grows far more watermelons than people want to buy. What will most likely happen to the price?", "It will go down", ["It will go up", "Watermelons will be scarce", "It will double"],
           "When there is plenty of something, the price usually <b>goes down</b>."),
          ("What does scarce mean?", "There is not enough for everyone who wants it", ["There is a lot of it", "It is free", "It is very small"],
           "<b>Scarce</b> means there is not enough of something for everyone who wants it."),
          ("Why do strawberries often cost more in winter?", "Fewer strawberries grow, so they are scarce", ["People do not like strawberries in winter", "Strawberries are bigger in winter", "Stores give them away in summer"],
           "Fewer strawberries grow in winter, so they are <b>scarce</b> and cost more."),
          ("After a big freeze, many water pipes break. What happens to the price of plumbers' work?", "It goes up because many people need plumbers", ["It goes down", "Plumbers work for free", "It stays the same"],
           "Many people need the same service at once, so the price <b>goes up</b>.")]


def one_scarce_math(r):
    p = r.choice([2, 3, 4, 5])
    up = r.choice([1, 2, 3])
    n = r.randint(3, 8)
    item = r.choice(["pumpkins", "Christmas trees", "watermelons", "pecan pies"])
    return mcq("Before a dry summer, %s cost $%d each. After the dry summer they are scarce and cost $%d more each. How much do %d cost now?" % (item, p * 5, up * 5, n),
               "$%d" % ((p * 5 + up * 5) * n), ["$%d" % (p * 5 * n), "$%d" % (p * 5 * n + up * 5), "$%d" % (p * 5 + up * 5 + n)],
               "New price: $%d + $%d = $%d each. $%d × %d = <b>$%d</b>." % (p * 5, up * 5, p * 5 + up * 5, p * 5 + up * 5, n, (p * 5 + up * 5) * n))


def one_scarce(r):
    return facts(SCARCE)(r) if r.random() < 0.45 else one_scarce_math(r)


# ------------------------------------------------------------ set 3: planned and unplanned spending (3.9C)
PLAN = [("Which is an example of planned spending?", "Buying school supplies on a list made at home", ["Buying candy at the checkout because it looks good", "Buying a toy you saw in a store window", "Paying a fine for a late library book"],
         "Planned spending is decided <b>before</b> you shop, like a supply list."),
        ("Which is an example of unplanned spending?", "Buying a snack at the checkout that was not on the list", ["Paying for a soccer camp you saved for", "Buying groceries from a list", "Paying the monthly rent"],
         "Unplanned spending happens without planning, like an impulse snack."),
        ("What is a cost of unplanned spending?", "There may be less money left for things you need", ["You always get a better price", "You save more money", "You earn income"],
         "Unplanned spending can leave <b>less money for things you need</b> or want more."),
        ("What is a benefit of planned spending?", "You can compare prices and stay within your budget", ["You never have to pay", "Prices always go down", "You do not need any money"],
         "Planning lets you <b>compare prices and stay within your budget</b>."),
        ("The family car gets a flat tire and needs a new one. What kind of spending is this?", "Unplanned spending", ["Planned spending", "Saving", "Charitable giving"],
         "A flat tire was not expected, so paying for it is <b>unplanned spending</b>."),
        ("Why is it smart to keep some savings for unplanned costs?", "So you can pay for surprises without borrowing", ["So you can spend it all on toys", "Because banks need your money", "So prices go down"],
         "Savings help you pay for surprises <b>without borrowing</b>.")]


def one_plan_math(r):
    k = Kid(r).next()
    have = r.choice([20, 25, 30, 40, 50])
    plan = r.randint(8, have - 8)
    extra = r.randint(3, min(9, have - plan - 1))
    return mcq("%s has $%d. %s plans to spend $%d on a book. At the store %s also buys a $%d snack that was not planned. How much money is left?" % (k["n"], have, k["He"], plan, k["he"], extra),
               "$%d" % (have - plan - extra), ["$%d" % (have - plan), "$%d" % (have - extra), "$%d" % (have - plan + extra)],
               "$%d − $%d − $%d = <b>$%d</b>. The unplanned snack left %s with $%d less." % (have, plan, extra, have - plan - extra, k["him"], extra))


def one_plan(r):
    return facts(PLAN)(r) if r.random() < 0.45 else one_plan_math(r)


# ------------------------------------------------------------ set 4: credit (3.9D)
CREDIT = [("When do people use credit?", "When they want or need something but do not have enough money to pay for it now", ["When they have extra money to give away", "When they want to save money", "When something is free"],
           "Credit is used <b>when wants or needs cost more than you can pay right now</b>."),
          ("Who has to pay back money borrowed on credit?", "The borrower", ["The lender", "The store", "Nobody"],
           "<b>The borrower</b> is responsible for paying the money back to the lender."),
          ("What is interest?", "Extra money a borrower pays the lender for using the money", ["Money the store gives you for shopping", "A free gift from the bank", "Money you find"],
           "Interest is <b>extra money the borrower pays</b> for using borrowed money."),
          ("Ana borrows money from a bank to buy a car. Who is the lender?", "The bank", ["Ana", "The car", "Ana's friend"],
           "The one who lends the money is the lender: <b>the bank</b>."),
          ("Why does buying with credit usually cost more than paying with cash?", "The borrower usually pays interest", ["Cash is worth less", "Stores charge more for cash", "Credit cards are heavy"],
           "With credit, <b>the borrower usually pays interest</b>, so the total cost is more."),
          ("Which is true about a credit card?", "It is a loan that must be paid back", ["It is free money", "It never has to be paid back", "It is the same as savings"],
           "Using a credit card is borrowing: <b>it is a loan that must be paid back</b>.")]


def one_credit_math(r):
    k = Kid(r).next()
    b = r.choice([20, 30, 40, 50, 60, 80, 100])
    i = r.choice([2, 3, 4, 5, 10])
    return mcq("%s borrows $%d from %s sister to buy %s. %s agrees to pay back the $%d plus $%d interest. How much does %s pay back in all?" % (k["n"], b, k["his"], "a bike helmet" if b <= 40 else "a new bike", k["He"], b, i, k["he"]),
               "$%d" % (b + i), ["$%d" % b, "$%d" % (b - i), "$%d" % i], "$%d + $%d interest = <b>$%d</b>. The borrower pays back more than was borrowed." % (b, i, b + i))


def one_credit(r):
    return facts(CREDIT)(r) if r.random() < 0.45 else one_credit_math(r)


# ------------------------------------------------------------ set 5: saving plans and money decisions (3.9E, 3.9F)
SAVE = [("Which is a good reason to save money?", "To pay for college someday", ["To spend it all today", "Because money disappears if you spend it", "To pay interest"],
         "Saving for big goals like <b>college</b> is a good reason to save."),
        ("What is a savings plan?", "A plan to put away a set amount of money regularly for a goal", ["A list of toys to buy today", "A way to borrow money", "A plan to spend all your income"],
         "A savings plan puts away <b>a set amount regularly</b> for a goal."),
        ("Leo gets $10. He spends $3, saves $5 and gives $2 to a food bank. Which part is charitable giving?", "The $2 for the food bank", ["The $3 he spends", "The $5 he saves", "The $10 he gets"],
         "Giving money to help others is charitable giving: <b>the $2 for the food bank</b>."),
        ("Which decision is about income?", "Taking a job walking dogs", ["Buying a new hat", "Putting money in a savings account", "Borrowing money from a bank"],
         "Earning money from work is an <b>income</b> decision."),
        ("Which is an example of saving?", "Putting $5 in a piggy bank each week", ["Buying lunch", "Paying back a loan", "Donating clothes"],
         "<b>Putting money aside</b> each week is saving."),
        ("What is one benefit of saving money in a bank?", "It is kept safe and can earn interest", ["The bank spends it for you", "It can never be taken out", "It makes prices go down"],
         "A bank keeps money <b>safe</b>, and savings accounts can <b>earn interest</b>.")]


def one_save_math(r):
    k = Kid(r).next()
    kind = r.choice(["weeks", "goal"])
    w = r.choice([2, 3, 4, 5, 6, 8, 10])
    if kind == "weeks":
        n = r.randint(4, 10)
        return mcq("%s saves $%d every week. How much will %s save in %d weeks?" % (k["n"], w, k["he"], n), "$%d" % (w * n), ["$%d" % (w + n), "$%d" % (w * n - w), "$%d" % (w * n + w)],
                   "$%d × %d = <b>$%d</b>." % (w, n, w * n))
    g = w * r.randint(3, 10)
    return mcq("%s wants a $%d game. %s saves $%d each week. How many weeks will it take?" % (k["n"], g, k["He"], w), "%d weeks" % (g // w),
               ["%d weeks" % (g - w), "%d weeks" % (g // w + 1), "%d weeks" % (g + w)], "$%d ÷ $%d = <b>%d weeks</b>." % (g, w, g // w))


def one_save(r):
    return facts(SAVE)(r) if r.random() < 0.35 else one_save_math(r)


def build():
    sets = [S("Work, skills and income", collect(one_work, 20, R)),
            S("Scarcity and cost", collect(one_scarce, 20, R)),
            S("Planned and unplanned spending", collect(one_plan, 20, R)),
            S("Credit, borrowers and interest", collect(one_credit, 20, R)),
            S("Saving plans and money decisions", collect(one_save, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Income</b> is money earned by working. Skills and knowledge (<b>human capital</b>) can help people earn more.</li>"
        "<li>When something is <b>scarce</b>, it usually costs more. When there is plenty of it, it usually costs less.</li>"
        "<li><b>Planned spending</b> is decided before you shop. <b>Unplanned spending</b> can leave less money for what you need.</li>"
        "<li><b>Credit</b> is borrowing. The borrower must pay the lender back, usually with <b>interest</b>.</li>"
        "<li>A <b>savings plan</b> puts away money regularly for a goal, like college. People also decide how much to give to charity.</li></ul>",
        [example("Sam saves $6 a week for 9 weeks. How much does he save?", ["$6 × 9"], "$54"),
         example("Ava borrows $40 and pays $4 interest. How much does she pay back?", ["$40 + $4"], "$44")],
        [["Thinking credit is free money", "Credit must be paid back, usually with interest."],
         ["Thinking scarce things cost less", "Scarce means hard to get, so the price usually goes up."],
         ["Forgetting unplanned costs", "Keep some savings for surprises like a flat tire."]])
    faq = [("What does personal financial literacy mean in Grade 3?", "Learning how people earn, spend, save, borrow and give money wisely (TEKS 3.9A to 3.9F)."),
           ("What is human capital?", "The skills and knowledge a person has. Building them through school and practice can lead to higher income (TEKS 3.9A)."),
           ("What is credit?", "Borrowing money to pay for something now. The borrower must pay the lender back, usually with interest (TEKS 3.9D)."),
           ("Why have a savings plan?", "It helps you reach goals such as a bike or college by saving a set amount regularly (TEKS 3.9E).")]
    make("personal-financial-literacy", 21, "Personal Financial Literacy", "3.9A–3.9F",
         "3.9A explain the connection between human capital/labor and income; 3.9B describe the relationship between the availability or scarcity of resources and how that impacts cost; 3.9C identify the costs and benefits of planned and unplanned spending decisions; 3.9D explain that credit is used when wants or needs exceed the ability to pay and that it is the borrower's responsibility to pay it back to the lender, usually with interest; 3.9E list reasons to save and explain the benefit of a savings plan, including for college; 3.9F identify decisions involving income, spending, saving, credit, and charitable giving",
         "Personal Financial Literacy: Income, Scarcity, Spending, Credit and Saving", "Personal Financial Literacy",
         "Free Grade 3 personal financial literacy worksheets for Texas TEKS 3.9: income and human capital, scarcity and cost, planned and unplanned spending, credit and interest, saving plans and money decisions. 100 questions with answers.",
         "Earn with skills, plan your spending, save for goals, and pay back what you borrow.", "Scarce things cost more. Credit is borrowing, and the borrower usually pays interest.",
         body, faq, sets, seo_title="Grade 3 Personal Financial Literacy Worksheets (TEKS 3.9, Texas)")


if __name__ == "__main__":
    build()
