# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Two-Way Tables (8.SP.A.4)
  python3 tools/gen_us_math_g8_two_way_tables.py
Read two-way frequency tables, find totals and missing cells, find relative frequencies (of the whole
table, of a row, of a column), and decide if there is an association. Wrong answers come from real
mistakes: dividing by the wrong total, reading the wrong row or column, and comparing counts instead of
percents when groups are different sizes.
"""
import random
from fractions import Fraction as F
from ws_common import mcq as _mcq, balance, B, table, example, write_unit, fr


def mcq(q, correct, cands, e):
    """Choices are compared by their text. Numbers get extra near-miss choices if needed."""
    txt = [c[0] for c in cands if c and c[0] and c[0] != correct[0]]
    ct = correct[0]
    if ct.isdigit():
        n = int(ct)
        txt += [str(n + 1), str(n + 10), str(max(1, n - 2))]
    return _mcq(q, (ct, ct), [(t, t) for t in txt], e)

R = random.Random(81601)
UPDATED = "2026-11-16"

TABLES = [
    (("Grade 7", "Grade 8"), ("Plays a sport", "No sport"), [[30, 20], [45, 15]]),
    (("Boys", "Girls"), ("Likes math", "Does not"), [[18, 12], [21, 9]]),
    (("Has a pet", "No pet"), ("Walks to school", "Rides"), [[24, 16], [10, 30]]),
    (("Adults", "Kids"), ("Coffee", "Juice"), [[40, 10], [5, 45]]),
    (("Morning", "Evening"), ("Gym", "No gym"), [[12, 28], [18, 22]]),
    (("City", "Town"), ("Has a bike", "No bike"), [[35, 65], [60, 40]]),
    (("Band", "No band"), ("Homework done", "Not done"), [[27, 3], [48, 22]]),
    (("Under 30", "30 and over"), ("Uses app", "Does not"), [[56, 14], [24, 56]]),
]


def two_way(rows, cols, data, hide=None):
    head = [""] + list(cols) + ["Total"]
    body = []
    for i, r in enumerate(rows):
        cells = [str(v) if hide != (i, j) else "?" for j, v in enumerate(data[i])]
        body.append(["<b>%s</b>" % r] + cells + [str(sum(data[i])) if hide != (i, 2) else "?"])
    col_tot = [data[0][j] + data[1][j] for j in range(2)]
    body.append(["<b>Total</b>"] + [str(c) if hide != (2, j) else "?" for j, c in enumerate(col_tot)] +
                [str(sum(col_tot)) if hide != (2, 2) else "?"])
    return table(head, body)


def pct(f):
    v = float(f) * 100
    return ("%d%%" % round(v)) if abs(v - round(v)) < 1e-9 else ("%.1f%%" % v)


def ffrac(f):
    f = F(f)
    return fr(f.numerator, f.denominator) if f.denominator != 1 else str(f.numerator)


# ============================================================ set 1: read and totals
def set_read():
    its = []
    for k, (rows, cols, d) in enumerate(TABLES[:5]):
        tbl = two_way(rows, cols, d)
        i, j = k % 2, (k + 1) % 2
        v = d[i][j]
        its.append(mcq(tbl + "How many are in the <b>%s</b> group and the <b>%s</b> column?" % (rows[i], cols[j]), (str(v), v),
                       [(str(d[1 - i][j]), "a"), (str(d[i][1 - j]), "b"), (str(sum(d[i])), "c"), (str(d[1 - i][1 - j]), "d")],
                       "Find the row %s and the column %s: <b>%d</b>." % (rows[i], cols[j], v)))
        rt = sum(d[i])
        its.append(mcq(tbl + "How many are in the <b>%s</b> group in all?" % rows[i], (str(rt), rt),
                       [(str(sum(d[1 - i])), "o"), (str(d[i][0]), "x"), (str(d[0][j] + d[1][j]), "c"), (str(rt + 10), "p")],
                       "Add the %s row: %d + %d = <b>%d</b>." % (rows[i], d[i][0], d[i][1], rt)))
        ct = d[0][j] + d[1][j]
        its.append(mcq(tbl + "How many are in the <b>%s</b> column in all?" % cols[j], (str(ct), ct),
                       [(str(d[0][1 - j] + d[1][1 - j]), "o"), (str(d[0][j]), "x"), (str(sum(d[0])), "r"), (str(ct + 5), "p")],
                       "Add the %s column: %d + %d = <b>%d</b>." % (cols[j], d[0][j], d[1][j], ct)))
        tot = sum(map(sum, d))
        its.append(mcq(tbl + "How many people were surveyed in all?", (str(tot), tot),
                       [(str(sum(d[0])), "r"), (str(d[0][0] + d[1][0]), "c"), (str(tot - d[1][1]), "m"), (str(tot * 2), "d")],
                       "Add all four cells (or the totals): <b>%d</b>." % tot))
    return {"title": "Read a two-way table", "items": its}


# ============================================================ set 2: complete the table
def set_missing():
    its = []
    for k, (rows, cols, d) in enumerate(TABLES):
        for hide in [(k % 2, k % 2), (1 - k % 2, 2), (2, (k + 1) % 2) if k % 4 else (2, 2)]:
            if len(its) >= 20:
                break
            i, j = hide
            if j == 2 and i < 2:
                v = sum(d[i])
                how = "Row total = %d + %d = <b>%d</b>." % (d[i][0], d[i][1], v)
            elif i == 2 and j < 2:
                v = d[0][j] + d[1][j]
                how = "Column total = %d + %d = <b>%d</b>." % (d[0][j], d[1][j], v)
            elif i == 2 and j == 2:
                v = sum(map(sum, d))
                how = "Grand total = %d + %d = <b>%d</b>." % (sum(d[0]), sum(d[1]), v)
            else:
                v = d[i][j]
                how = "The row total is %d and the other cell is %d: %d − %d = <b>%d</b>." % (sum(d[i]), d[i][1 - j], sum(d[i]), d[i][1 - j], v)
            tbl = two_way(rows, cols, d, hide)
            wr = [v + 10, v - 5, v * 2, abs(v - 10) if v != 10 else v + 20]
            its.append(mcq(tbl + "What number goes in place of the ?", (str(v), v), [(str(w), w) for w in wr if w > 0], how))
    while len(its) < 20:
        rows, cols, d = TABLES[len(its) % 8]
        tbl = two_way(rows, cols, d, (1, 1))
        v = d[1][1]
        its.append(mcq(tbl + "What number goes in place of the ?", (str(v), v), [(str(w), w) for w in [v + 2, v - 3, v * 3, v + 7]],
                       "Row total %d minus %d = <b>%d</b>." % (sum(d[1]), d[1][0], v)))
    return {"title": "Complete the table", "items": its[:20]}


# ============================================================ set 3: relative frequency of the whole
def set_rel_total():
    its = []
    for k, (rows, cols, d) in enumerate(TABLES):
        tot = sum(map(sum, d))
        for (i, j) in [(0, 0), (1, 1)] if k < 4 else [(0, 1), (1, 0), (1, 1)]:
            if len(its) >= 18:
                break
            v = d[i][j]
            f = F(v, tot)
            tbl = two_way(rows, cols, d)
            q = tbl + "What percent of everyone surveyed is in the <b>%s</b> group and the <b>%s</b> column?" % (rows[i], cols[j])
            e = "%d out of %d: %d ÷ %d = <b>%s</b>." % (v, tot, v, tot, pct(f))
            wr = [F(v, sum(d[i])), F(v, d[0][j] + d[1][j]), F(sum(d[i]), tot), F(v, 100)]
            its.append(mcq(q, (pct(f), f), [(pct(w), w) for w in wr], e))
    for q, ans, wr, e in [
        ("What is a relative frequency?", "A count divided by a total, as a fraction or percent", ["The biggest count", "The total of a row",
         "The difference between two counts"], "Relative frequency = <b>a count divided by a total, as a fraction or percent</b>."),
        ("The relative frequencies of all four cells of a table (divided by the grand total) add to …", "100%", ["50%", "200%", "It depends"],
         "Every person is in exactly one cell: <b>100%</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    return {"title": "Relative frequency of the whole", "items": its}


# ============================================================ set 4: row and column relative frequencies
def set_cond():
    its = []
    for k, (rows, cols, d) in enumerate(TABLES):
        tbl = two_way(rows, cols, d)
        i = k % 2
        v = d[i][0]
        f = F(v, sum(d[i]))
        q = tbl + "Of the <b>%s</b> group, what percent are in the <b>%s</b> column?" % (rows[i], cols[0])
        e = "Use the %s row only: %d ÷ %d = <b>%s</b>." % (rows[i], v, sum(d[i]), pct(f))
        wr = [F(v, sum(map(sum, d))), F(v, d[0][0] + d[1][0]), F(d[i][1], sum(d[i])), F(sum(d[i]), sum(map(sum, d)))]
        its.append(mcq(q, (pct(f), f), [(pct(w), w) for w in wr], e))
        j = (k + 1) % 2
        v2 = d[1][j]
        ct = d[0][j] + d[1][j]
        f2 = F(v2, ct)
        q = tbl + "Of the people in the <b>%s</b> column, what percent are in the <b>%s</b> group?" % (cols[j], rows[1])
        e = "Use the %s column only: %d ÷ %d = <b>%s</b>." % (cols[j], v2, ct, pct(f2))
        wr = [F(v2, sum(d[1])), F(v2, sum(map(sum, d))), F(d[0][j], ct), F(ct, sum(map(sum, d)))]
        its.append(mcq(q, (pct(f2), f2), [(pct(w), w) for w in wr], e))
    for q, ans, wr, e in [
        ("To find “of the Grade 7 students, what percent play a sport”, which total do you divide by?", "The Grade 7 row total",
         ["The grand total", "The 'Plays a sport' column total", "100"], "“Of the Grade 7 students” means divide by <b>the Grade 7 row total</b>."),
        ("To find “of the people who play a sport, what percent are in Grade 8”, which total do you divide by?", "The 'Plays a sport' column total",
         ["The grand total", "The Grade 8 row total", "The number of people with no sport"], "“Of the people who play a sport” means divide by <b>the 'Plays a sport' column total</b>."),
        ("In a row of relative frequencies (each cell ÷ row total), the row adds to …", "100%", ["50%", "the grand total", "It depends"],
         "Each row is split into parts of itself: <b>100%</b>."),
        ("Why use percents instead of counts to compare two groups?", "The groups may be different sizes", ["Percents are always bigger",
         "Counts are never correct", "Percents add to 200%"], "60 out of 100 and 60 out of 300 are very different: <b>the groups may be different sizes</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[16], o[1], o[2], o[17], o[3], o[4], o[18], o[5], o[6], o[19], o[7], o[8], o[9], o[10], o[11], o[12],
             o[13], o[14], o[15]]
    return {"title": "Row and column percents", "items": order}


# ============================================================ set 5: association and building tables
def set_assoc():
    its = []
    YES, NO = "Yes, the percents are very different", "No, the percents are about the same"
    for rows, cols, d in TABLES:
        p1, p2 = F(d[0][0], sum(d[0])), F(d[1][0], sum(d[1]))
        ok = abs(p1 - p2) >= F(15, 100)
        ans = YES if ok else NO
        q = two_way(rows, cols, d) + "Is the group (<b>%s</b> or <b>%s</b>) associated with <b>%s</b>?" % (rows[0], rows[1], cols[0])
        e = "%s: %s in “%s”. %s: %s in “%s”. %s." % (rows[0], pct(p1), cols[0], rows[1], pct(p2), cols[0],
                                                  "<b>Yes</b>, the groups differ a lot" if ok else "<b>No</b>, the groups are about the same")
        its.append(mcq(q, (ans, ans), [(c, c) for c in [YES, NO, "Yes, because the counts are different", "We cannot tell from a table"] if c != ans], e))
    for q, ans, wr, e in [
        ("Survey: 50 students. 30 have a phone; 18 of them are in Grade 8. 10 Grade 8 students have no phone. How many Grade 7 students have a phone?", "12",
         ["18", "20", "10"], "Phone total 30 − Grade 8 with a phone 18 = <b>12</b>."),
        ("Survey: 50 students. 30 have a phone; 18 of them are in Grade 8. 10 Grade 8 students have no phone. How many Grade 7 students have no phone?", "10",
         ["20", "12", "8"], "No phone: 50 − 30 = 20. Grade 8 with no phone: 10. Grade 7 with no phone: 20 − 10 = <b>10</b>."),
        ("100 people: 60 like summer best. 25 of the summer fans are under 20. 15 people under 20 like winter best. How many people 20 or over like winter?", "25",
         ["40", "15", "35"], "Winter: 100 − 60 = 40. Under 20: 15. So 40 − 15 = <b>25</b>."),
        ("A class has 28 students: 16 girls and 12 boys. 10 girls and 3 boys take art. How many students do not take art?", "15", ["13", "6", "9"],
         "Art: 10 + 3 = 13. Not art: 28 − 13 = <b>15</b>."),
        ("In a table, 40 of 50 adults and 10 of 50 teens read the news. Which statement is true?", "Adults are much more likely to read the news",
         ["Teens are more likely to read the news", "There is no association", "Everyone reads the news"], "80% vs 20%: <b>adults are much more likely to read the news</b>."),
        ("In a table, 30 of 60 boys and 45 of 90 girls play an instrument. Is there an association?", "No, both are 50%", ["Yes, more girls play",
         "Yes, more boys play", "We cannot tell"], "30/60 = 50% and 45/90 = 50%: <b>no, both are 50%</b>. More girls play only because there are more girls."),
        ("A two-way table shows data for …", "two categories about the same people", ["one number", "two numbers that are added", "a scatter plot"],
         "It sorts people by <b>two categories about the same people</b>."),
        ("What kind of data goes in a two-way table?", "Categorical data, like yes/no or grade level", ["Only measurements like height",
         "Only decimals", "Only times"], "Two-way tables count <b>categorical data, like yes/no or grade level</b>."),
        ("A table shows 45 of 60 dog owners and 15 of 40 non-owners walk daily. What percent of dog owners walk daily?", "75%",
         ["45%", "60%", "37.5%"], "45 ÷ 60 = <b>75%</b>."),
        ("Using the same table (45 of 60 dog owners, 15 of 40 non-owners walk daily), is owning a dog associated with walking daily?",
         "Yes, 75% vs 37.5%", ["No, 45 and 15 are both walkers", "No, there are more dog owners", "We cannot tell"],
         "75% of owners vs 37.5% of non-owners: <b>yes, 75% vs 37.5%</b>."),
        ("Out of 200 shoppers, 120 paid by card. 70 of the card users were under 40. How many card users were 40 or over?", "50", ["80", "130", "70"],
         "120 − 70 = <b>50</b>."),
        ("A table has a grand total of 80. One row total is 35. What is the other row total?", "45", ["35", "115", "40"], "80 − 35 = <b>45</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[8], o[0], o[9], o[1], o[14], o[2], o[10], o[3], o[11], o[4], o[12], o[5], o[13], o[6], o[15], o[16], o[7],
             o[17], o[18], o[19]]
    return {"title": "Association and building tables", "items": order}


def body():
    rows, cols, d = TABLES[0]
    return ("<h2>Two-way tables</h2>"
            "<p>A <b>two-way table</b> counts people (or things) by two categories at once. Each cell is one combination. "
            "The <b>totals</b> are at the end of each row and column.</p>"
            + two_way(rows, cols, d)
            + "<h2>Relative frequency</h2><p>Divide a count by a total. Choose the total that matches the question:</p>"
            + table(["Question", "Divide by", "Example"], [
                ["What percent of everyone…?", "grand total", "30 ÷ 110 ≈ 27.3%"],
                ["Of the Grade 7 students, what percent…?", "the Grade 7 row total", "30 ÷ 50 = 60%"],
                ["Of those who play a sport, what percent…?", "the column total", "30 ÷ 75 = 40%"]])
            + example("Is grade associated with playing a sport?", ["Grade 7: 30 ÷ 50 = 60% play.", "Grade 8: 45 ÷ 60 = 75% play."],
                      "Yes, Grade 8 students are more likely to play (75% vs 60%).")
            + "<h2>Common mistakes</h2><ul><li>Dividing by the grand total when the question says “of the Grade 7 students”.</li>"
            "<li>Comparing counts when the groups are different sizes. Compare percents.</li>"
            "<li>Reading the wrong row or column. Put a finger on each label.</li></ul>")


def main():
    sets = [set_read(), set_missing(), set_rel_total(), set_cond(), set_assoc()]
    balance(sets, R)
    unit = {
        "slug": "two-way-tables",
        "title": "Two-Way Tables and Relative Frequency",
        "seo_title": "Grade 8 Two-Way Tables Worksheets: Totals, Relative Frequency and Association",
        "short_title": "Two-way tables",
        "domain": "Statistics & Probability",
        "standard_code": "8.SP.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/SP/A/4/",
        "standard_text": "Understand that patterns of association can also be seen in bivariate categorical data by displaying frequencies and relative frequencies in a two-way table. Construct and interpret a two-way table summarizing data on two categorical variables collected from the same subjects. Use relative frequencies calculated for rows or columns to describe possible association between the two variables.",
        "meta_desc": "Free Grade 8 two-way table worksheets: read cells and totals, complete missing values, find relative frequencies of the whole table, rows and columns, and decide if two categories are associated. 100 questions with an answer key.",
        "key_big": "A two-way table counts by two categories. Divide a count by the right total to get a relative frequency.",
        "key_sub": "“Of the Grade 7 students” → divide by the Grade 7 total. Compare percents to see an association.",
        "body_html": body(),
        "faq": [
            {"q": "What is a two-way table?", "a": "A table that counts data by two categories at the same time, such as grade level and whether a student plays a sport."},
            {"q": "What is relative frequency?", "a": "A count divided by a total, written as a fraction, decimal or percent."},
            {"q": "How do you know if there is an association in a two-way table?", "a": "Find the row (or column) percents. If they are very different between groups, there is an association."},
            {"q": "Which total do I divide by?", "a": "Use the total of the group named in the question: the grand total for 'of everyone', a row total for 'of the boys', a column total for 'of those who…'."}],
        "sets": sets, "pdf_url": "", "sort": 16, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
