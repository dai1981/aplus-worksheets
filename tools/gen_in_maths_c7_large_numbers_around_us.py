# -*- coding: utf-8 -*-
"""
India Class 7 Maths, Ganita Prakash Part 1, Chapter 1: Large Numbers Around Us
  python3 tools/gen_in_maths_c7_large_numbers_around_us.py
Indian place value (thousand, lakh, crore) and the international system (million, billion), converting between them,
reading and writing large numbers with commas, place value of a digit, comparing, rounding and estimating, and real-life
large numbers (population, distances, money).
Wrong answers come from real mistakes: 1 lakh taken as 1 million, commas placed in the international pattern, and a
digit's place value read from the wrong end.
"""
import random
from in_common import num, unit, T, QN, comma

R = random.Random(907001)


def intl(n):
    return "{:,}".format(n)


def words(n):
    cr, n = divmod(n, 10 ** 7)
    lk, n = divmod(n, 10 ** 5)
    th, n = divmod(n, 1000)
    parts = []
    if cr:
        parts.append("%d crore" % cr)
    if lk:
        parts.append("%d lakh" % lk)
    if th:
        parts.append("%d thousand" % th)
    if n:
        parts.append(str(n))
    return " ".join(parts)


def one_units(r):
    t = r.choice([("1 lakh", 100000, "1 million", 1000000, "How many lakh make 1 million?", 10),
                  ("1 crore", 10 ** 7, "1 million", 10 ** 6, "How many million make 1 crore?", 10),
                  ("1 lakh", 100000, "1 thousand", 1000, "How many thousand make 1 lakh?", 100),
                  ("1 crore", 10 ** 7, "1 lakh", 10 ** 5, "How many lakh make 1 crore?", 100),
                  ("1 billion", 10 ** 9, "1 crore", 10 ** 7, "How many crore make 1 billion?", 100)])
    kind = r.choice(["ratio", "zeros"])
    if kind == "ratio":
        return QN(t[4], t[5], [t[5] * 10, t[5] // 10, 1000], "%s = %s and %s = %s, so <b>%d</b>." % (t[0], comma(t[1]), t[2], intl(t[3]), t[5]))
    k = r.choice([("1 lakh", 5), ("10 lakh", 6), ("1 crore", 7), ("10 crore", 8), ("1 million", 6), ("1 billion", 9), ("100 crore", 9)])
    return QN("How many zeros are there in %s written in digits?" % k[0], k[1], [k[1] + 1, k[1] - 1, k[1] + 2], "%s = %s: <b>%d zeros</b>." % (k[0], comma(10 ** k[1]) if "lakh" in k[0] or "crore" in k[0] else intl(10 ** k[1]), k[1]))


def one_read(r):
    n = r.randint(10 ** 5, 99 * 10 ** 7)
    n = n // 1000 * 1000 + r.choice([0, r.randint(1, 999)])
    kind = r.choice(["words", "commas", "intl", "conv"])
    if kind == "words":
        w = [words(n * 10) if n * 10 < 10 ** 10 else words(n // 10), words(n + 10 ** 5), words(n - 10 ** 5) if n > 2 * 10 ** 5 else words(n + 2 * 10 ** 5)]
        return T("How is %s read in the Indian system?" % comma(n), words(n), w, "Group as %s: <b>%s</b>." % (comma(n), words(n)))
    if kind == "commas":
        return T("Where do the commas go in %d in the Indian system?" % n, comma(n), [intl(n), comma(n * 10)[:-2] if False else intl(n).replace(",", ""), comma(n)[::-1][::-1].replace(",", "", 1)],
                 "From the right: 3 digits, then groups of 2: <b>%s</b>." % comma(n))
    if kind == "intl":
        return T("Write %s with international commas." % comma(n), intl(n), [comma(n), intl(n * 10), intl(n // 10)], "Groups of 3 from the right: <b>%s</b>." % intl(n))
    lk = r.randint(1, 999)
    return T("%d lakh is how many in the international system?" % lk, "%s million" % num(lk / 10) if lk % 10 else "%d million" % (lk // 10),
             ["%d million" % lk, "%s million" % num(lk / 100) if lk % 100 else "%d million" % (lk // 100), "%s billion" % num(lk / 10)], "10 lakh = 1 million, so %d lakh = <b>%s million</b>." % (lk, num(lk / 10)))


def one_place(r):
    s = str(r.randint(10 ** 6, 99 * 10 ** 7))
    cands = [i for i in range(len(s) - 1) if s[i] != "0" and s.count(s[i]) == 1]
    if not cands:
        return None
    i = r.choice(cands)
    d = int(s[i])
    pv = d * 10 ** (len(s) - 1 - i)
    return QN("What is the place value of the digit %d in %s?" % (d, comma(int(s))), pv, [d, pv * 10, pv // 10 if pv >= 10 else pv * 100],
              "%d is worth %d × %s = <b>%s</b>." % (d, d, comma(10 ** (len(s) - 1 - i)), comma(pv)))


def one_est(r):
    kind = r.choice(["round", "round", "cmp", "real", "real"])
    if kind == "round":
        n = r.randint(10 ** 6, 10 ** 9)
        to, name = r.choice([(10 ** 5, "lakh"), (10 ** 7, "crore"), (10 ** 6, "ten lakh")])
        v = (n + to // 2) // to * to
        return T("Round %s to the nearest %s." % (comma(n), name), comma(v), [comma(n // to * to) if n // to * to != v else comma(v + to), comma(v + to * 10), comma(v // 10)],
                 "<b>%s</b>." % comma(v))
    if kind == "cmp":
        a = r.randint(10 ** 6, 10 ** 9)
        b = int(str(a)[:-1] + "0") + r.choice([10 ** 5, -10 ** 5, 10 ** 6])
        xs = sorted([a, b, a + 10 ** 4, b - 10 ** 4])
        if len(set(xs)) < 4:
            return None
        return T("Which is the largest: %s?" % ", ".join(comma(x) for x in r.sample(xs, 4)), comma(xs[-1]), [comma(x) for x in xs[:3]], "<b>%s</b>." % comma(xs[-1]))
    t = r.choice([("A city has 1 crore 25 lakh people. Written in digits, this is", 12500000), ("India's population is about 140 crore. In digits this is", 1400000000),
                  ("A car costs ₹8 lakh 50 thousand. In digits this is ₹", 850000), ("The Sun is about 15 crore km from the Earth. In digits this is", 150000000),
                  ("A cricket stadium holds 1 lakh 32 thousand people. In digits this is", 132000), ("A company earned ₹3 crore 40 lakh. In digits this is ₹", 34000000)])
    v = t[1]
    return T(t[0] + " ___.", comma(v), [comma(v * 10), comma(v // 10), intl(v) if intl(v) != comma(v) else comma(v + 10 ** 5)], "<b>%s</b>." % comma(v))


def main():
    unit(7, 1, 1, "large-numbers-around-us", 1, "N", "Large Numbers Around Us: Lakhs, Crores and Millions", "large numbers around us",
         "Reading, writing and comparing large numbers in the Indian and international systems (lakh, crore, million, billion), place value, estimation and rounding (summary of NCERT Ganita Prakash Class 7)",
         "Class 7 Large Numbers Around Us worksheet (Ganita Prakash Part 1, Chapter 1): lakh, crore, million, billion, place value, Indian and international commas, rounding and estimating. 100 questions with answers.",
         "10 lakh = 1 million; 1 crore = 10 million", "Indian commas: 3 digits, then groups of 2 (1,23,45,678).",
         "<p><b>Indian system</b>: thousand (1,000), lakh (1,00,000), crore (1,00,00,000). Commas: the first after 3 digits from the right, then after every 2.</p>"
         "<p><b>International system</b>: thousand, million (1,000,000), billion (1,000,000,000). Commas after every 3 digits.</p>"
         "<p>10 lakh = 1 million, 1 crore = 10 million, 100 crore = 1 billion.</p>",
         [("Read 4,05,20,300 in the Indian system.", ["4 crore, 5 lakh, 20 thousand, 300"], "4 crore 5 lakh 20 thousand 300"),
          ("How many million is 35 lakh?", ["10 lakh = 1 million"], "3.5 million")],
         ["Thinking 1 lakh = 1 million (it is 100 thousand).", "Putting Indian commas every 3 digits.", "Reading the place value from the left instead of the right."],
         [("How many lakh are in a crore?", "100 lakh = 1 crore."),
          ("How do lakh and million compare?", "10 lakh = 1 million, so 1 lakh is one-tenth of a million."),
          ("How are commas placed in the Indian system?", "The first comma comes after the hundreds place, then after every two digits: 12,34,56,789.")],
         [("Lakh, crore, million and billion", [(one_units, 10), (one_read, 10)]),
          ("Reading and writing large numbers", [(one_read, 20)]),
          ("Place value", [(one_place, 20)]),
          ("Comparing and rounding", [(one_est, 20)]),
          ("Large numbers in real life", [(one_est, 10), (one_read, 5), (one_place, 5)])], R)


if __name__ == "__main__":
    main()
