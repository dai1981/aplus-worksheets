# -*- coding: utf-8 -*-
"""
Texas Grade 8 Math: Estimating College Costs and Making a Savings Plan (TEKS 8.12G)
  python3 tools/gen_ustx_math_g8_paying_for_college.py
Estimating the yearly cost of attendance, two-year and four-year totals, family contribution and aid, and periodic
savings plans for the first year of college.
Wrong answers come from real mistakes: counting only tuition, using one year for a four-year total, and dividing
by the wrong number of months.
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


def one_year(r):
    t = r.choice([4000, 6000, 8000, 10000, 11000])
    h = r.choice([6000, 8000, 9000, 10000, 12000])
    b = r.choice([800, 1000, 1200])
    o = r.choice([2000, 2500, 3000])
    tot = t + h + b + o
    return mcq("One year at a Texas university costs: tuition and fees %s, housing and food %s, books %s, and other costs %s. What is the total cost of attendance for one year?" % (md(t), md(h), md(b), md(o)), md(tot), [md(t), md(t + h), md(tot * 4)],
               "%s + %s + %s + %s = <b>%s</b>." % (md(t), md(h), md(b), md(o), md(tot)))


def one_multi(r):
    two = r.choice([6000, 8000, 9000, 10000])
    four = r.choice([20000, 24000, 26000, 30000])
    kind = r.choice(["two", "four", "diff"])
    if kind == "two":
        return mcq("A community college costs about %s a year to attend. About how much is a two-year associate degree?" % md(two), md(2 * two), [md(two), md(4 * two), md(two + 2)],
                   "%s × 2 = <b>%s</b>." % (md(two), md(2 * two)))
    if kind == "four":
        return mcq("A four-year university costs about %s a year. About how much is a four-year degree?" % md(four), md(4 * four), [md(four), md(2 * four), md(four + 4)],
                   "%s × 4 = <b>%s</b>." % (md(four), md(4 * four)))
    return mcq("A community college costs %s a year and a university costs %s a year. How much less are 2 years at the community college than 2 years at the university?" % (md(two), md(four)), md(2 * (four - two)), [md(four - two), md(4 * four - 2 * two), md(2 * four)],
               "2 × (%s − %s) = <b>%s</b>. Some students start at a community college and transfer." % (md(four), md(two), md(2 * (four - two))))


def one_family(r):
    cost = r.choice([18000, 20000, 22000, 24000, 26000])
    g = r.choice([2000, 3000, 4000, 6000])
    s = r.choice([1000, 2000, 3000, 5000])
    w = r.choice([2000, 2500, 3000])
    fam = cost - g - s - w
    return mcq("The first year of college costs %s. A student gets a %s grant and a %s scholarship and will earn %s from a part-time job. How much must the family contribute?" % (md(cost), md(g), md(s), md(w)), md(fam), [md(cost - g), md(g + s + w), md(fam + s)],
               "%s − %s − %s − %s = <b>%s</b>." % (md(cost), md(g), md(s), md(w), md(fam)))


def one_plan(r):
    need = r.choice([4800, 6000, 7200, 8400, 9000, 9600, 10800, 12000, 15000])
    yrs = r.choice([2, 3, 4, 5])
    months = 12 * yrs
    mo = need / float(months)
    kind = r.choice(["month", "year"])
    if kind == "month":
        return mcq("A family needs %s for the first year of college in %d years. How much must they save each month (without interest)?" % (md(need), yrs), m(mo), [m(need / yrs), m(need / 12.0), m(mo * 2)],
                   "%d years = %d months. %s ÷ %d = <b>%s a month</b>." % (yrs, months, md(need), months, m(mo)))
    return mcq("A student wants %s for the first year of college and has %d years to save. How much is that each year?" % (md(need), yrs), m(need / float(yrs)), [m(mo), m(need * yrs), m(need / 12.0)],
               "%s ÷ %d = <b>%s a year</b>." % (md(need), yrs, m(need / float(yrs))))


def build():
    sets, R = build_sets([
        ("Cost of attendance for one year", [("collect", one_year, 20)]),
        ("Two-year and four-year costs", [("collect", one_multi, 20)]),
        ("Family contribution and aid", [("collect", one_family, 20)]),
        ("A periodic savings plan", [("collect", one_plan, 20)]),
        ("Mixed college planning", [("collect", one_family, 10), ("collect", one_plan, 10)]),
    ], 68024)
    finish(sets, R)
    body = lesson('<ul><li>The <b>cost of attendance</b> includes tuition and fees, housing and food, books, transportation and other costs.</li><li>A two-year degree is about 2 years of cost; a four-year degree is about 4 years.</li><li>Grants, scholarships and work reduce what the <b>family contributes</b>.</li><li>A <b>savings plan</b> divides the amount needed by the number of months or years until college.</li></ul>',
        [example("$9,600 needed in 4 years", ["4 × 12 = 48 months", "9,600 ÷ 48"], "$200 a month")],
        [['Counting only tuition', 'Add housing, food, books and other costs.'], ['Using one year for a four-year total', 'Multiply by the number of years.'], ['Dividing by years when months are asked', '4 years is 48 months.']])
    faq = [('What does TEKS 8.12G ask?', 'Estimate the cost of a two-year and four-year college education, including family contribution, and devise a periodic savings plan for accumulating the money needed to contribute to the total cost of attendance for at least the first year of college.'), ('What is the family contribution?', 'The part of the cost the family pays after grants, scholarships and work.'), ('Does interest help a savings plan?', 'Yes. Interest means the family needs to deposit a little less.'), ('Why consider community college?', 'It usually costs less for the first two years.')]
    make('paying-for-college', 24, 'Personal Financial Literacy', '8.12G',
         '8.12G estimate the cost of a two-year and four-year college education, including family contribution, and devise a periodic savings plan for accumulating the money needed to contribute to the total cost of attendance for at least the first year of college',
         'Estimating College Costs and Making a Savings Plan', 'Paying for College',
         'Free Grade 8 personal financial literacy worksheets for Texas TEKS 8.12G: estimate college costs, two-year and four-year totals, family contribution and a savings plan. 100 questions with answers.',
         'Savings per month = amount needed ÷ months left.', '$9,600 in 4 years = $200 a month.',
         body, faq, sets, seo_title='Grade 8 Paying for College Worksheets: Costs and Savings Plans (TEKS 8.12G, STAAR)')


if __name__ == "__main__":
    build()
