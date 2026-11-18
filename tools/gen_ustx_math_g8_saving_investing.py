# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Saving and Investing: Simple and Compound Interest (TEKS 8.12C, 8.12D)
  python3 tools/gen_ustx_math_g8_saving_investing.py
Simple interest earnings, compound interest earnings, comparing simple and compound interest, regular deposits
that grow over time, and saving for college and retirement.
Wrong answers come from real mistakes: treating compound interest like simple interest, forgetting the deposits, and
adding the rate instead of multiplying.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_ustx_math_g4_financial_literacy as g4f
tx_common.GRADE = "grade-8"

facts = g4f.facts


def m(v):
    v = round(v + 1e-9, 2)
    d, c = divmod(int(round(v * 100)), 100)
    return "$%s.%02d" % (comma(d), c)


def md(v):
    return "$%s" % comma(int(round(v)))


def pc(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def one_simple(r):
    p = r.choice([500, 800, 1000, 2000, 2500, 4000])
    rate = r.choice([2, 3, 4, 5])
    t = r.choice([2, 3, 4, 5, 10])
    i = p * rate * t / 100.0
    return mcq("%s is saved at %d%% simple interest per year for %d years. How much interest does it earn?" % (md(p), rate, t), m(i), [m(p * rate / 100.0), m(p + i), m(i * 10)],
               "I = Prt = %s × %s × %d = <b>%s</b>." % (md(p), pc(rate / 100.0), t, m(i)))


def one_comp(r):
    p = r.choice([1000, 2000, 4000, 5000])
    rate = r.choice([4, 5, 6, 10])
    t = r.choice([2, 3])
    b = p * (1 + rate / 100.0) ** t
    if r.random() < 0.5:
        return mcq("%s is invested at %d%% compounded once a year. What is the balance after %d years?" % (md(p), rate, t), m(b), [m(p * (1 + rate * t / 100.0)), m(b - p), m(p * (1 + rate / 100.0) * (t + 1))],
                   "Multiply by %s each year: %s × %s<sup>%d</sup> = <b>%s</b>." % (pc(1 + rate / 100.0), md(p), pc(1 + rate / 100.0), t, m(b)))
    s = p * rate * t / 100.0
    return mcq("%s is saved for %d years at %d%%. How much more does it earn with interest compounded yearly than with simple interest?" % (md(p), t, rate), m(b - p - s), [m(b - p), m(s), "$0.00"],
               "Compound interest: %s. Simple interest: %s. Difference: <b>%s</b>." % (m(b - p), m(s), m(b - p - s)))


def one_regular(r):
    d = r.choice([300, 400, 500, 600, 750, 800, 1000, 1200, 1500, 2000])
    rate = r.choice([3, 4, 5, 6, 8, 10])
    k = 1 + rate / 100.0
    kind = r.choice(["two", "three", "total"])
    if kind == "two":
        b = d * k * k + d * k
        return mcq("Marcus deposits %s at the start of each year into an account that earns %d%% compounded yearly. What is the balance at the end of year 2?" % (md(d), rate), m(b), [m(2 * d), m(2 * d * k), m(d * k * k)],
                   "First deposit: %s × %s² = %s. Second deposit: %s × %s = %s. Total = <b>%s</b>." % (md(d), pc(k), m(d * k * k), md(d), pc(k), m(d * k), m(b)))
    if kind == "three":
        b = d * (k ** 3 + k ** 2 + k)
        return mcq("A family saves %s at the start of each year for college at %d%% compounded yearly. About how much is saved after 3 years?" % (md(d), rate), m(b), [m(3 * d), m(3 * d * k), m(d * k ** 3)],
                   "%s × (%s³ + %s² + %s) = <b>%s</b>. Regular saving plus interest grows faster than saving alone." % (md(d), pc(k), pc(k), pc(k), m(b)))
    w = r.choice([20, 25, 40, 50, 75, 100, 150])
    yrs = r.choice([5, 10, 15, 20, 30])
    return mcq("Ana saves %s a month for retirement for %d years, without counting interest. How much does she deposit in all?" % (md(w), yrs), md(w * 12 * yrs), [md(w * yrs), md(w * 12), md(w * 52 * yrs)],
               "%s × 12 × %d = <b>%s</b>. With interest, the account would be worth even more." % (md(w), yrs, md(w * 12 * yrs)))


IDEAS = [("Why does money grow faster with compound interest?", "Interest is earned on the interest too", ["The bank adds a bonus each day", "The rate goes up every year", "Taxes are removed"], "With compound interest, each year's interest is added to the balance and earns interest."),
         ("Who will have more at age 65 if both save $100 a month at the same rate?", "The person who starts at 25", ["The person who starts at 45", "Both will have the same", "It depends only on the bank"], "Starting early gives the money more years to grow."),
         ("What is a benefit of saving small amounts regularly?", "The deposits and interest add up over time", ["It avoids all taxes", "It doubles the money every month", "It means you never need a budget"], "Small regular amounts grow into large sums over many years."),
         ("Which account usually earns the most over 30 years at the same rate?", "One with compound interest", ["One with simple interest", "One with no interest", "Cash kept at home"], "Compound interest grows faster over long periods.")]


def build():
    sets, R = build_sets([
        ("Simple interest earnings", [("collect", one_simple, 20)]),
        ("Compound interest", [("collect", one_comp, 20)]),
        ("Regular deposits grow over time", [("collect", one_regular, 20)]),
        ("Saving for college and retirement", [("collect", facts(IDEAS), 4), ("collect", one_regular, 16)]),
        ("Compare simple and compound interest", [("collect", one_comp, 10), ("collect", one_simple, 10)]),
    ], 68022)
    finish(sets, R)
    body = lesson('<ul><li><b>Simple interest</b> is earned only on the original amount: I = Prt.</li><li><b>Compound interest</b> is earned on the balance, including past interest: multiply by (1 + r) each year.</li><li>Saving small amounts <b>regularly</b> adds up, and interest makes it grow even more.</li><li>Starting early gives money more time to grow.</li></ul>',
        [example("$1,000 at 10% for 2 years", ["Simple: $200", "Compound: 1,000 × 1.1² = $1,210"], "compound earns $10 more")],
        [['Treating compound like simple interest', "Each year's interest is added before the next year."], ['Forgetting the deposits', 'Add every deposit and the interest each one earns.'], ['Adding the rate instead of multiplying', 'Multiply by 1.05, do not add 5.']])
    faq = [('What does TEKS 8.12C ask?', 'Explain how small amounts of money invested regularly, including money saved for college and retirement, grow over time.'), ('What does TEKS 8.12D ask?', 'Calculate and compare simple interest and compound interest earnings.'), ('What does compounded yearly mean?', 'Interest is added to the balance once each year.'), ('Why start saving early?', 'More years of compound interest make the money grow much more.')]
    make('saving-and-investing-over-time', 22, 'Personal Financial Literacy', '8.12C, 8.12D',
         '8.12C explain how small amounts of money invested regularly, including money saved for college and retirement, grow over time; 8.12D calculate and compare simple interest and compound interest earnings',
         'Saving and Investing: Simple and Compound Interest', 'Saving and Investing',
         'Free Grade 8 personal financial literacy worksheets for Texas TEKS 8.12C and 8.12D: simple and compound interest, regular deposits and saving for college and retirement. 100 questions with answers.',
         'Compound interest earns interest on interest.', '$1,000 at 10% for 2 years: simple $200, compound $210.',
         body, faq, sets, seo_title='Grade 8 Simple and Compound Interest and Saving Worksheets (TEKS 8.12C, 8.12D, STAAR)')


if __name__ == "__main__":
    build()
