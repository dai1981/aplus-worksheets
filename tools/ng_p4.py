# -*- coding: utf-8 -*-
"""
Nigeria / Mathematics / Primary 4 (NERDC 9-Year Basic Education Curriculum, Lagos and national schemes of work).
  python3 tools/ng_p4.py [number …]      seed = 150400 + number
Units follow the first, second and third term order of the Primary 4 scheme of work.
Question makers: ng_p4a (written for Nigeria) and other countries' generators (US, UK, Singapore, Philippines, Australia)
with Nigerian names, naira and British spelling (ng_common.adopt / finish).
"""
import importlib
import random
import sys
import ng_common as C
from ng_common import finish, make, lesson, adopt, build_sets, example
import ng_p4a as A

C.GRADE = "primary-4"
TH = {"N": "Number and Numeration", "O": "Basic Operations", "A": "Algebraic Processes", "M": "Measurement", "G": "Geometry", "S": "Everyday Statistics"}


def mod(name, seed):
    m = importlib.import_module(name)
    adopt(m)
    if hasattr(m, "R"):
        m.R = random.Random(seed)
    return m


def uniq(fn):
    seen = set()

    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


def co(fn, n):
    return ("collect", uniq(fn), n)


def ru(fn, args, n, keep=None):
    return ("run", fn, args, n) + ((keep,) if keep else ())


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>"


def U(slug, th, std, title, short, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, th=th, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks, sets=sets, think=think, ex=ex, mist=mist, faq=faq)


def units():
    usp = mod("gen_us_math_g4_place_value", 150901)
    ukp = mod("gen_uk_maths_y4_place_value", 150902)
    rn4 = mod("gen_uk_maths_y4_roman_numerals", 150903)
    rn5 = mod("gen_uk_maths_y5_roman_numerals", 150904)
    usa = mod("gen_us_math_g4_add_sub", 150905)
    uka = mod("gen_uk_maths_y4_column_add_sub", 150906)
    usm = mod("gen_us_math_g4_multiplication", 150907)
    sgm = mod("gen_sg_maths_p4_multiplication", 150908)
    usd = mod("gen_us_math_g4_division", 150909)
    phf = mod("gen_ph_math_g4_factors_multiples", 150910)
    phm = mod("gen_ph_math_g4_improper_mixed", 150911)
    sgx = mod("gen_sg_maths_p4_mixed_numbers", 150912)
    use = mod("gen_us_math_g4_equivalent_fractions", 150913)
    phe = mod("gen_ph_math_g4_equivalent_fractions", 150914)
    usf = mod("gen_us_math_g4_add_subtract_fractions", 150915)
    us5 = mod("gen_us_math_g5_add_sub_fractions", 150916)
    phd = mod("gen_ph_math_g4_dissimilar_fractions", 150917)
    pdc = mod("gen_ph_math_g4_decimals", 150918)
    usdc = mod("gen_us_math_g4_decimals", 150919)
    phr = mod("gen_ph_math_g4_rounding_estimating", 150920)
    sgr = mod("gen_sg_maths_p4_rounding", 150921)
    ukc = mod("gen_uk_maths_y4_converting_units", 150922)
    ukm = mod("gen_uk_maths_y3_measuring", 150923)
    uk4a = mod("gen_uk_maths_y4_area_perimeter", 150924)
    sga = mod("gen_sg_maths_p4_area_perimeter", 150925)
    pht = mod("gen_ph_math_g4_time", 150926)
    ust = mod("gen_us_math_g3_time", 150927)
    usy = mod("gen_us_math_g4_symmetry", 150928)
    usang = mod("gen_us_math_g4_angles", 150929)
    uks = mod("gen_uk_maths_y3_shapes", 150930)
    sg3 = mod("gen_sg_maths_p2_3d_shapes", 150931)
    ukst = mod("gen_uk_maths_y3_statistics", 150932)
    auc = mod("gen_au_maths_y3_chance", 150933)
    usmv = mod("gen_us_math_g3_mass_volume", 150934)

    return [
        U("whole-numbers-up-to-one-million", "N", "Count, read and write whole numbers up to one million in figures and in words; identify the place value of digits up to one million.",
          "Whole Numbers up to One Million: Place Value, Figures and Words", "Whole Numbers up to 1,000,000",
          "Free Primary 4 maths worksheets on whole numbers up to one million: place value, value of a digit, numbers in figures and in words, expanded form and counting in thousands. 100 questions with answers.",
          "Value = digit × place", "Read big numbers in groups of three digits.",
          [("Place value and the value of a digit", [ru(usp.set_value, ("rnd", "seen"), 20)]), ("Figures, words and expanded form", [ru(usp.set_forms, ("rnd", "seen"), 20)]),
           ("Write in figures and in words", [co(A.wn_words, 20)]), ("Break numbers into parts", [ru(ukp.set_partition, ("rnd", "seen"), 20)]),
           ("Count on and back in thousands", [co(A.wn_more, 20)])],
          ul(["Each digit has a <b>place</b> (units, tens, hundreds, thousands, ten thousands, hundred thousands) and a <b>value</b>.",
              "In 482,375 the 8 is in the ten thousands place, so its value is 80,000.",
              "Read big numbers in groups of three: 482 thousand, 375 → four hundred and eighty-two thousand, three hundred and seventy-five."]),
          [example("Value of 6 in 361,042", ["6 is in the ten thousands place"], "60,000"), example("Write 205,040 in words", ["205 thousand and 40"], "two hundred and five thousand, forty")],
          [["Giving the digit, not its value", "The value of 6 in 361,042 is 60,000, not 6."], ["Leaving out a zero", "Two hundred and five thousand is 205,000."], ["Forgetting the commas", "Put a comma after every three digits from the right."]],
          [("What is the largest 6-digit number?", "999,999. One more is 1,000,000, one million."), ("Why do we put commas in big numbers?", "They split the digits into groups of three so the number is easy to read."), ("What does a zero do in a number?", "It holds a place so the other digits keep their values.")]),

        U("skip-counting", "N", "Count in groups of 5s, 7s and 60s, and in 100s and 1,000s up to 10,000; solve quantitative reasoning problems with number patterns.",
          "Skip Counting in 5s, 7s, 60s, 100s and 1,000s", "Skip Counting",
          "Free Primary 4 maths worksheets on skip counting: count on and back in 5s, 7s, 60s, 100s and 1,000s, find missing numbers and solve counting problems. 100 questions with answers.",
          "Add the same step each time", "Count back: subtract the step.",
          [("Count on", [co(A.sk_next, 20)]), ("Find the missing number", [co(A.sk_missing, 20)]), ("Count back", [co(A.sk_back, 20)]),
           ("Counting in real life", [co(A.sk_60, 20)]), ("Which number in the list?", [co(A.sk_nth, 20)])],
          ul(["Skip counting means adding the same number (the step) each time: 7, 14, 21, 28, …",
              "Find the step by subtracting two numbers next to each other.", "Counting in 60s helps with time: 60 minutes = 1 hour."]),
          [example("60, 120, 180, 240, …", ["The step is 60"], "300"), example("3,000, 4,000, ___, 6,000", ["Count in 1,000s"], "5,000")],
          [["Using the wrong step", "Check the difference between two numbers next to each other."], ["Adding when counting back", "Counting back means subtracting."], ["Losing a zero in big steps", "3,000 + 1,000 = 4,000, not 3,100."]],
          [("Why learn to count in 7s?", "There are 7 days in a week, so counting in 7s helps with weeks and the 7 times table."), ("Why count in 60s?", "There are 60 seconds in a minute and 60 minutes in an hour."), ("What is quantitative reasoning?", "Finding the rule in a set of numbers and using it to find the missing number.")]),

        U("comparing-and-ordering-numbers", "N", "Order and compare whole numbers up to 1,000,000 using the signs <, > and =.",
          "Comparing and Ordering Numbers up to One Million", "Comparing and Ordering Numbers",
          "Free Primary 4 maths worksheets on comparing and ordering whole numbers up to one million with &lt;, &gt; and =, greatest and smallest numbers from digits and real-life problems. 100 questions with answers.",
          "Count the digits first", "Same length: compare from the left.",
          [("Compare with &lt;, &gt; and =", [ru(usp.set_compare, ("rnd", "seen", usp.People), 20)]), ("Which statement is true?", [co(A.cmp_true, 14), co(A.cmp_len, 6)]),
           ("Arrange in order", [co(A.ord_asc, 20)]), ("Greatest and smallest from digits", [co(A.ord_digits, 20)]), ("Comparing in real life", [co(A.ord_town, 20)])],
          ul(["A number with more digits is always greater: 100,000 &gt; 99,999.", "If two numbers have the same number of digits, compare from the left until the digits are different.",
              "&gt; means greater than, &lt; means less than. The open side faces the bigger number."]),
          [example("Compare 45,210 and 45,120", ["Same up to the hundreds: 2 &gt; 1"], "45,210 &gt; 45,120"), example("Greatest number from 3, 8, 0, 5, 1", ["Biggest digits first"], "85,310")],
          [["Comparing the first digits of numbers of different lengths", "Count the digits first."], ["Turning the sign the wrong way", "The open side faces the bigger number."], ["Putting 0 first in the smallest number", "A number cannot start with 0; put the smallest non-zero digit first."]],
          [("What do &lt; and &gt; mean?", "&lt; means is less than and &gt; means is greater than."), ("How do I order numbers?", "Compare them two at a time, or compare the highest place first."), ("Is 0 a digit?", "Yes. It holds a place in a number.")]),

        U("roman-numerals", "N", "Count and write Roman numerals from I to M (1 to 1,000); read clock faces with Roman numerals; convert between Hindu-Arabic and Roman numerals; add and subtract Roman numerals.",
          "Roman Numerals from I to M", "Roman Numerals",
          "Free Primary 4 maths worksheets on Roman numerals from I to M: symbols, reading and writing Roman numerals, clock faces, converting to and from our numbers and simple addition and subtraction. 100 questions with answers.",
          "I 1, V 5, X 10, L 50, C 100, D 500, M 1000", "A smaller symbol before a bigger one is subtracted.",
          [("Roman symbols", [ru(rn4.set_symbols, (), 20)]), ("Read Roman numerals", [ru(rn4.set_read, (), 10), ru(rn5.set_read, (), 10)]),
           ("Write Roman numerals", [co(A.rm_write, 20)]), ("Add and subtract", [ru(rn4.set_calc, (), 20)]),
           ("Roman numerals in real life", [ru(rn5.set_life, (rn5.People,), 20)])],
          ul(["Roman numerals use seven symbols: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1,000.",
              "Add symbols written from big to small: XVI = 10 + 5 + 1 = 16.", "A smaller symbol before a bigger one is subtracted: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900."]),
          [example("XLVII", ["XL = 40, VII = 7"], "47"), example("Write 394", ["300 = CCC, 90 = XC, 4 = IV"], "CCCXCIV")],
          [["Writing IIII for 4", "4 is IV."], ["Reading IX as 11", "I before X means 10 − 1 = 9."], ["Using one symbol more than three times", "Never write the same symbol four times in a row."]],
          [("Where do we see Roman numerals?", "On clock faces, chapters of books, names of kings and on buildings."), ("Is there a zero in Roman numerals?", "No. The Romans had no symbol for zero."), ("What is the biggest number in this topic?", "M, which is 1,000.")]),

        U("addition-and-subtraction", "O", "Add and subtract whole numbers in thousands, hundreds, tens and units, with and without regrouping; solve word problems.",
          "Addition and Subtraction of Whole Numbers", "Addition and Subtraction",
          "Free Primary 4 maths worksheets on adding and subtracting whole numbers in thousands, hundreds, tens and units, with and without regrouping, subtracting across zeros and word problems. 100 questions with answers.",
          "Line up units under units", "Carry and borrow 10 to the next place.",
          [("Add 4-digit numbers", [ru(usa.set_add4, ("rnd", "seen"), 20)]), ("Add bigger numbers", [ru(usa.set_add56, ("rnd", "seen"), 20)]),
           ("Subtract with regrouping", [ru(usa.set_sub4, ("rnd", "seen"), 20)]), ("Subtract across zeros", [ru(usa.set_zeros, ("rnd", "seen"), 20)]),
           ("Word problems and checking", [ru(uka.set_check, ("rnd",), 10), ru(uka.set_story, ("rnd",), 10)])],
          ul(["Write the numbers under each other: units under units, tens under tens, and so on.", "Start from the units. When a column adds up to 10 or more, carry 1 to the next column.",
              "In subtraction, if the top digit is smaller, borrow 1 from the next place (it becomes 10 in this place).", "Check a subtraction by adding: difference + smaller number = bigger number."]),
          [example("3,486 + 2,759", ["6 + 9 = 15, write 5 carry 1", "…"], "6,245"), example("5,003 − 1,428", ["Borrow across the zeros"], "3,575")],
          [["Not lining up the places", "Units under units, tens under tens."], ["Forgetting the carried 1", "Write it above the next column."], ["Subtracting the smaller digit from the bigger in every column", "Borrow when the top digit is smaller."]],
          [("What is regrouping?", "Changing 10 units into 1 ten (carrying) or 1 ten into 10 units (borrowing)."), ("How do I check my subtraction?", "Add the answer to the number you took away. You should get the first number."), ("What words mean add?", "Altogether, sum, total, more than, increase.")]),

        U("multiplication", "O", "Multiply whole numbers by 2-digit numbers up to 50 using the grid and vertical methods; revise basic multiplication facts.",
          "Multiplication of Whole Numbers by 1- and 2-Digit Numbers", "Multiplication",
          "Free Primary 4 maths worksheets on multiplication: multiplying by 1-digit numbers, grid (area) method, long multiplication by 2-digit numbers, 3-digit by 2-digit numbers and estimating products. 100 questions with answers.",
          "Multiply by the units, then by the tens", "Add the two lines to get the answer.",
          [("Multiply by a 1-digit number", [ru(usm.set_std1, ("rnd", "seen"), 20)]), ("The grid method", [ru(usm.set_area2, ("rnd", "seen"), 20)]),
           ("Multiply by a 2-digit number", [ru(usm.set_std2, ("rnd", "seen"), 20)]), ("3-digit by 2-digit numbers", [ru(sgm.set_3x2, ("rnd", "seen", sgm.People), 20)]),
           ("Estimate products", [ru(sgm.set_estimate, ("rnd", sgm.People), 20)])],
          ul(["Know your times tables up to 12 × 12.", "Grid method: split each number into tens and units, multiply each part and add.",
              "Vertical method: multiply by the units digit, then by the tens digit (put a 0 first), then add the two lines."]),
          [example("34 × 26", ["34 × 6 = 204", "34 × 20 = 680", "204 + 680"], "884")],
          [["Forgetting the 0 when multiplying by tens", "34 × 20 = 680, not 68."], ["Forgetting to add the carried number", "Write carried numbers small above the next digit."], ["Adding instead of multiplying", "Times means groups of."]],
          [("What is the grid method?", "A box method: split the numbers into tens and units and multiply each part."), ("How can I check a product?", "Estimate by rounding: 34 × 26 is about 30 × 30 = 900."), ("Does the order matter?", "No. 26 × 34 = 34 × 26.")]),

        U("division", "O", "Divide 2- and 3-digit numbers by numbers up to 9, with or without remainders; divide by multiples of 10 up to 50; solve sharing problems.",
          "Division with and without Remainders", "Division",
          "Free Primary 4 maths worksheets on division: dividing 2- and 3-digit numbers by 1-digit numbers, remainders, dividing by multiples of 10 and sharing word problems. 100 questions with answers.",
          "Divide, multiply, subtract, bring down", "The remainder is always less than the divisor.",
          [("Divide without remainders", [ru(usd.set_no_rem, ("rnd", "seen"), 20)]), ("Divide with remainders", [ru(usd.set_rem, ("rnd", "seen", usd.People), 20)]),
           ("Zeros in the quotient", [ru(usd.set_four, ("rnd", "seen"), 20)]), ("Divide by 10, 20, 30, 40 and 50", [co(A.div_tens, 20)]), ("Sharing problems", [co(A.div_share, 20)])],
          ul(["Division shares a number into equal groups. 84 ÷ 4 = 21 because 4 × 21 = 84.", "Long division: divide, multiply, subtract, bring down the next digit, and repeat.",
              "If something is left over, it is the remainder. It must be smaller than the number you divide by.", "To divide by 20, divide by 10 and then by 2."]),
          [example("756 ÷ 6", ["7 ÷ 6 = 1 r 1", "15 ÷ 6 = 2 r 3", "36 ÷ 6 = 6"], "126"), example("840 ÷ 40", ["840 ÷ 10 = 84", "84 ÷ 4"], "21")],
          [["Leaving out a 0 in the quotient", "If the divisor does not go into a digit, write 0."], ["A remainder bigger than the divisor", "Then the divisor goes in once more."], ["Dividing by 4 instead of 40", "Divide by 10 as well."]],
          [("How do I check a division?", "Multiply the answer by the divisor and add the remainder."), ("What is a remainder?", "What is left over when a number cannot be shared equally."), ("What words mean divide?", "Share equally, how many in each, how many groups.")]),

        U("lowest-common-multiple", "N", "Find multiples of numbers up to 9; find the lowest common multiple (LCM) of numbers using the multiples method; solve problems on LCM.",
          "Multiples and Lowest Common Multiple (LCM)", "Lowest Common Multiple (LCM)",
          "Free Primary 4 maths worksheets on multiples and the lowest common multiple (LCM): lists of multiples, common multiples, LCM of two and three numbers and LCM word problems. 100 questions with answers.",
          "LCM = smallest number in both lists", "List the multiples of each number.",
          [("Multiples of a number", [co(A.mult_list, 10), co(phf.one_mult, 10)]), ("Common multiples", [co(A.common_mult, 20)]), ("LCM of two numbers", [co(A.lcm2, 20)]),
           ("LCM of three numbers", [co(A.lcm3, 20)]), ("LCM word problems", [co(A.lcm_word, 20)])],
          ul(["Multiples of 4 are 4, 8, 12, 16, 20, 24, … (the 4 times table).", "A common multiple is in the lists of both numbers.",
              "The lowest common multiple (LCM) is the smallest common multiple."]),
          [example("LCM of 4 and 6", ["4, 8, 12, …", "6, 12, …"], "12")],
          [["Multiplying the numbers every time", "4 × 6 = 24 is a common multiple, but 12 is the lowest."], ["Mixing up multiples and factors", "Multiples get bigger: 6, 12, 18. Factors divide: 1, 2, 3, 6."], ["Stopping the list too early", "Keep listing until a number appears in both lists."]],
          [("What is the LCM used for?", "To find when things happen together again, and to add fractions."), ("Is the LCM ever one of the numbers?", "Yes. The LCM of 3 and 6 is 6."), ("What is a multiple?", "The answer when you multiply a number by 1, 2, 3, …")]),

        U("factors-and-highest-common-factor", "N", "Find the factors of numbers from 1 to 99; identify common factors; find the highest common factor (HCF) of numbers.",
          "Factors and Highest Common Factor (HCF)", "Highest Common Factor (HCF)",
          "Free Primary 4 maths worksheets on factors and the highest common factor (HCF): is it a factor, all the factors, factor pairs, common factors, HCF and HCF word problems. 100 questions with answers.",
          "HCF = biggest factor in both lists", "Factors divide a number exactly.",
          [("Is it a factor?", [co(phf.one_isfactor, 20)]), ("All the factors", [co(phf.one_all, 10), co(phf.one_pair, 10)]), ("Common factors", [co(A.common_fac, 20)]),
           ("HCF of two numbers", [co(A.hcf2, 20)]), ("HCF word problems", [co(A.hcf_word, 20)])],
          ul(["A factor divides a number exactly with no remainder. The factors of 12 are 1, 2, 3, 4, 6 and 12.", "Find factors in pairs: 1 × 12, 2 × 6, 3 × 4.",
              "A common factor divides both numbers. The highest common factor (HCF) is the biggest one."]),
          [example("HCF of 18 and 24", ["18: 1, 2, 3, 6, 9, 18", "24: 1, 2, 3, 4, 6, 8, 12, 24"], "6")],
          [["Forgetting 1 and the number itself", "Every number has 1 and itself as factors."], ["Giving the LCM", "The HCF is never bigger than the smaller number."], ["Missing a factor pair", "Check every number from 1 upwards."]],
          [("What is the HCF used for?", "To share things into equal groups and to reduce fractions to their lowest terms."), ("Can the HCF be 1?", "Yes, for numbers like 8 and 15 that share no other factor."), ("What is a factor?", "A number that divides another number exactly.")]),

        U("fractions", "N", "Identify proper, improper fractions and mixed numbers; convert improper fractions to mixed numbers and mixed numbers to improper fractions; represent fractions on a number line.",
          "Proper and Improper Fractions and Mixed Numbers", "Fractions",
          "Free Primary 4 maths worksheets on fractions: proper and improper fractions, mixed numbers, changing between them, fraction models and fractions on a number line. 100 questions with answers.",
          "Improper: numerator ≥ denominator", "Mixed number = whole number + proper fraction.",
          [("Proper, improper or mixed?", [co(phm.one_kind, 20)]), ("Improper fractions from pictures", [ru(sgx.set_improper, ("rnd",), 20)]),
           ("Mixed numbers from pictures", [ru(sgx.set_mixed, ("rnd",), 20)]), ("Change improper fractions and mixed numbers", [ru(sgx.set_convert, ("rnd",), 20)]),
           ("Fractions on a number line", [co(phm.one_nl, 20)])],
          ul(["In a fraction the denominator (bottom) shows how many equal parts make a whole; the numerator (top) shows how many parts we have.",
              "Proper fraction: numerator smaller than denominator (3/4). Improper fraction: numerator equal to or bigger than denominator (7/4).",
              "Mixed number: a whole number and a proper fraction (1 3/4). 7/4 = 1 3/4 because 7 ÷ 4 = 1 remainder 3."]),
          [example("Change 11/3 to a mixed number", ["11 ÷ 3 = 3 remainder 2"], "3 2/3"), example("Change 2 1/5 to an improper fraction", ["2 × 5 + 1 = 11"], "11/5")],
          [["Using the remainder as the denominator", "The denominator stays the same: 11/3 = 3 2/3."], ["Adding instead of multiplying", "2 1/5 = (2 × 5 + 1)/5, not (2 + 5 + 1)/5."], ["Counting the lines instead of the spaces on a number line", "Count the equal spaces between 0 and 1."]],
          [("What is a unit fraction?", "A fraction with numerator 1, like 1/2 or 1/5."), ("Is 5/5 proper or improper?", "Improper; it equals 1 whole."), ("Why use mixed numbers?", "They show clearly how many wholes there are.")]),

        U("equivalent-fractions-and-adding-fractions", "O", "Find equivalent fractions; reduce fractions to their lowest terms; add and subtract fractions with the same and different denominators.",
          "Equivalent Fractions, Lowest Terms and Adding Fractions", "Equivalent Fractions and Adding Fractions",
          "Free Primary 4 maths worksheets on equivalent fractions, reducing to lowest terms, and adding and subtracting like and unlike fractions. 100 questions with answers.",
          "Multiply or divide top and bottom by the same number", "Same denominator: add the numerators.",
          [("Equivalent fractions", [ru(use.set_multiply, ("rnd",), 10), ru(use.set_models, ("rnd",), 10)]), ("Reduce to lowest terms", [ru(use.set_divide, ("rnd",), 10), co(phe.one_simplest, 10)]),
           ("Add like fractions", [ru(usf.set_add, ("rnd", usf.People), 20)]), ("Subtract like fractions", [ru(usf.set_subtract, ("rnd", usf.People), 20)]),
           ("Add and subtract unlike fractions", [ru(us5.set_add, ("rnd", us5.People), 10, phd.den_q10), ru(us5.set_subtract, ("rnd", us5.People), 10, phd.den_q10)])],
          ul(["Equivalent fractions have the same value: 1/2 = 2/4 = 3/6. Multiply or divide the numerator and denominator by the same number.",
              "To reduce to lowest terms, divide the numerator and denominator by their HCF.",
              "Like fractions (same denominator): add or subtract the numerators and keep the denominator. Unlike fractions: first change them to the same denominator (use the LCM)."]),
          [example("Reduce 12/18", ["HCF = 6"], "2/3"), example("1/3 + 1/4", ["LCM of 3 and 4 is 12", "4/12 + 3/12"], "7/12")],
          [["Adding the denominators", "2/7 + 3/7 = 5/7, not 5/14."], ["Changing only the numerator", "Multiply both the numerator and the denominator."], ["Not reducing the answer", "Divide by the HCF to get the lowest terms."]],
          [("Why do equivalent fractions work?", "Multiplying top and bottom by the same number is like multiplying by 1."), ("What is a common denominator?", "A denominator both fractions can be written with, usually the LCM."), ("Must I always reduce?", "Yes, give the answer in its lowest terms.")]),

        U("decimal-fractions", "N", "Identify tenths, hundredths and thousandths; convert fractions to decimals; add and subtract decimal fractions.",
          "Decimal Fractions: Tenths, Hundredths and Thousandths", "Decimal Fractions",
          "Free Primary 4 maths worksheets on decimal fractions: tenths and hundredths from pictures, reading and writing decimals, place value, fractions and decimals, and adding and subtracting decimals. 100 questions with answers.",
          "0.1 = 1/10, 0.01 = 1/100", "Line up the decimal points.",
          [("Decimals from pictures", [ru(usdc.set_grids, ("rnd",), 20)]), ("Read and write decimals", [co(pdc.one_read, 20)]), ("Place value of decimals", [co(pdc.one_pv, 20)]),
           ("Fractions and decimals", [co(pdc.one_fd, 10), co(A.frac_dec, 10)]), ("Add and subtract decimals", [co(A.dec_addsub, 12), co(A.dec_word, 8)])],
          ul(["The first place after the decimal point is tenths, the second is hundredths and the third is thousandths.",
              "3/10 = 0.3, 7/100 = 0.07, 45/1000 = 0.045.", "To add or subtract decimals, line up the decimal points and work as with whole numbers."]),
          [example("2.7 + 1.45", ["2.70 + 1.45"], "4.15"), example("Value of 6 in 3.064", ["6 is in the hundredths place"], "6 hundredths (0.06)")],
          [["Writing 7/100 as 0.7", "7/100 = 0.07 (two decimal places)."], ["Not lining up the decimal points", "Write 2.7 as 2.70 before adding 1.45."], ["Thinking 0.45 &gt; 0.5 because 45 &gt; 5", "Compare 0.45 and 0.50."]],
          [("What does the decimal point do?", "It separates the whole number from the parts of a whole."), ("Are 0.5 and 0.50 the same?", "Yes. Zeros at the end of a decimal do not change its value."), ("Where do we use decimals?", "In money (₦12.50), measuring and weighing.")]),

        U("multiplying-and-dividing-decimals", "O", "Multiply and divide decimals by 1-digit numbers; multiply and divide by 10, 100 and 1,000; convert fractions with denominators 10, 100 and 1,000 to decimals.",
          "Multiplying and Dividing Decimals", "Multiplying and Dividing Decimals",
          "Free Primary 4 maths worksheets on multiplying and dividing decimals by 1-digit numbers and by 10, 100 and 1,000, and changing tenths, hundredths and thousandths to decimals. 100 questions with answers.",
          "× 10: digits move one place left", "÷ 10: digits move one place right.",
          [("Multiply a decimal by a 1-digit number", [co(A.dec_mul1, 20)]), ("Divide a decimal by a 1-digit number", [co(A.dec_div1, 20)]),
           ("Multiply and divide by 10, 100 and 1,000", [co(A.dec_10, 20)]), ("Fractions with 10, 100 and 1,000", [co(A.frac_dec, 20)]),
           ("Mixed practice", [co(A.dec_mul1, 7), co(A.dec_div1, 7), co(A.dec_10, 6)])],
          ul(["Multiply a decimal as if it were a whole number, then put the same number of decimal places in the answer.",
              "Divide as usual and put the decimal point in the answer straight above the decimal point in the number.",
              "× 10, × 100, × 1,000 move the digits 1, 2, 3 places to the left; ÷ 10, ÷ 100, ÷ 1,000 move them to the right."]),
          [example("2.45 × 3", ["245 × 3 = 735", "2 decimal places"], "7.35"), example("4.6 ÷ 100", ["Move 2 places right"], "0.046")],
          [["Losing the decimal point", "Count the decimal places in the question."], ["Moving the digits the wrong way", "Multiplying makes the number bigger."], ["Writing 3/100 as 0.3", "3/100 = 0.03."]],
          [("Why does × 10 make a number bigger?", "Each digit becomes worth ten times as much."), ("What is 0.5 × 4?", "2.0 = 2."), ("How do I check?", "Estimate: 2.45 × 3 is about 2 × 3 = 6.")]),

        U("squares-and-square-roots", "N", "Find the squares of numbers 1 to 20; identify perfect squares; find the square roots of perfect squares up to 400.",
          "Squares and Square Roots of Whole Numbers", "Squares and Square Roots",
          "Free Primary 4 maths worksheets on squares of numbers 1 to 20, perfect squares and square roots up to 400, with area and arrangement problems. 100 questions with answers.",
          "Square = number × itself", "Square root: which number times itself gives this?",
          [("Square numbers", [co(A.sq_of, 20)]), ("Perfect squares", [co(A.sq_perfect, 20)]), ("Square roots", [co(A.sq_root, 20)]),
           ("Squares in sums", [co(A.sq_sum, 20)]), ("Squares in real life", [co(A.sq_word, 20)])],
          ul(["The square of a number is the number multiplied by itself: 7² = 7 × 7 = 49.", "Numbers like 1, 4, 9, 16, 25, … are perfect squares.",
              "The square root (√) undoes squaring: √49 = 7 because 7 × 7 = 49."]),
          [example("15²", ["15 × 15"], "225"), example("√324", ["18 × 18 = 324"], "18")],
          [["Doubling instead of squaring", "6² = 36, not 12."], ["Halving to find a square root", "√64 = 8, not 32."], ["Thinking (a + b)² = a² + b²", "Work out each square separately."]],
          [("Why are they called square numbers?", "They make square arrangements: 16 dots make a 4 by 4 square."), ("What is √1?", "1, because 1 × 1 = 1."), ("Which squares should I know?", "From 1² = 1 to 20² = 400.")]),

        U("estimation-and-rounding", "N", "Round numbers to the nearest ten, hundred and thousand; estimate sums and differences by rounding.",
          "Rounding and Estimation", "Estimation and Rounding",
          "Free Primary 4 maths worksheets on rounding to the nearest ten, hundred, thousand and hundred thousand and estimating sums and differences. 100 questions with answers.",
          "5 or more: round up", "Look at the digit to the right of the place.",
          [("Round to the nearest thousand", [ru(sgr.set_thousand, (sgr.Picker,), 20)]), ("Round to different places", [ru(usp.set_round, ("rnd", "seen", usp.People), 12), ru(sgr.set_hundred, (sgr.Picker,), 8)]),
           ("Round big numbers", [co(phr.one_r100k, 20)]), ("Estimate sums and differences", [co(phr.one_est, 20)]), ("Estimate in word problems", [co(phr.one_word, 20)])],
          ul(["To round, look at the digit just to the right of the place you are rounding to.", "If it is 5, 6, 7, 8 or 9, round up. If it is 0, 1, 2, 3 or 4, round down.",
              "To estimate a sum or difference, round each number first, then add or subtract."]),
          [example("Round 46,382 to the nearest thousand", ["The hundreds digit is 3"], "46,000"), example("Estimate 4,872 + 3,214", ["5,000 + 3,000"], "about 8,000")],
          [["Looking at the wrong digit", "Look one place to the right."], ["Rounding 3,500 down", "5 rounds up: 4,000."], ["Not changing the digits after the place to 0", "46,382 → 46,000."]],
          [("Why do we estimate?", "To check that an answer is sensible and to calculate quickly."), ("Is an estimate the exact answer?", "No. It is close to the answer."), ("What is 95 to the nearest ten?", "100.")]),

        U("money", "O", "Convert naira to kobo and kobo to naira; add, subtract, multiply and divide money; solve problems on profit and loss and shopping, including online shopping.",
          "Money: Naira and Kobo, Profit and Loss", "Money",
          "Free Primary 4 maths worksheets on money in naira and kobo: converting, adding and subtracting money, change, profit and loss, multiplying and dividing money and online shopping. 100 questions with answers.",
          "₦1 = 100 kobo", "Profit = selling price − cost price.",
          [("Naira and kobo", [co(A.mo_convert, 20)]), ("Add and subtract money", [co(A.mo_addsub, 20)]), ("Shopping and change", [co(A.mo_change, 20)]),
           ("Profit and loss", [co(A.mo_profit, 20)]), ("Multiply, divide and shop online", [co(A.mo_muldiv, 14), co(A.mo_online, 6)])],
          ul(["₦1 = 100 kobo. ₦3.50 means 3 naira and 50 kobo = 350 kobo.", "Add and subtract money like decimals: line up the points.",
              "If the selling price is more than the cost price, there is a profit. If it is less, there is a loss."]),
          [example("Change ₦4.25 to kobo", ["4 × 100 + 25"], "425 kobo"), example("Bought for ₦6,000, sold for ₦7,500", ["7,500 − 6,000"], "profit of ₦1,500")],
          [["₦1 = 10 kobo", "₦1 = 100 kobo."], ["Mixing up profit and loss", "Compare the selling price with the cost price."], ["Forgetting delivery or other costs", "Add every cost before finding the total."]],
          [("What is cost price?", "The price a trader pays to buy something."), ("What is selling price?", "The price a trader sells it for."), ("Do we still use kobo?", "Prices are usually in naira, but kobo helps us understand decimals and money sums.")]),

        U("open-sentences", "A", "Find the missing number in open sentences with addition, subtraction, multiplication and division; write and solve number sentences from word problems.",
          "Open Sentences: Finding the Missing Number", "Open Sentences",
          "Free Primary 4 maths worksheets on open sentences: missing numbers in addition, subtraction, multiplication and division, writing number sentences and solving problems. 100 questions with answers.",
          "Use the inverse operation", "+ and − undo each other; × and ÷ undo each other.",
          [("Missing numbers", [co(A.os_box, 20)]), ("More missing numbers", [co(A.os_box, 20)]), ("Write a number sentence", [co(A.os_write, 20)]),
           ("Always true", [co(A.os_true, 10), co(A.os_box, 10)]), ("Solve the problem", [co(A.os_solve, 20)])],
          ul(["An open sentence has a missing number, shown by a box □ or a letter.", "Use the inverse operation: □ + 25 = 60 → □ = 60 − 25 = 35. □ × 6 = 54 → □ = 54 ÷ 6 = 9.",
              "Check by putting your answer back in the sentence."]),
          [example("□ − 48 = 75", ["75 + 48"], "123"), example("I think of a number, × 4, + 5 = 33", ["33 − 5 = 28", "28 ÷ 4"], "7")],
          [["Using the same operation", "□ + 25 = 60 needs subtraction, not addition."], ["Mixing up □ − 48 and 48 − □", "Read the order carefully."], ["Not checking", "Put the number back in the box."]],
          [("What is an inverse operation?", "An operation that undoes another: subtraction undoes addition."), ("Can a letter be used instead of a box?", "Yes, for example x + 5 = 12."), ("How do I write a number sentence from a story?", "Find the unknown, then write what happens to it.")]),

        U("length", "M", "Estimate lengths and distances in metres and kilometres; compare and convert between metres and kilometres; add and subtract lengths.",
          "Length: Metres and Kilometres", "Length",
          "Free Primary 4 maths worksheets on length: converting kilometres, metres and centimetres, adding and subtracting lengths, estimating lengths and distances and word problems. 100 questions with answers.",
          "1 km = 1,000 m", "1 m = 100 cm.",
          [("Change units of length", [co(A.len_conv, 10), ru(ukc.set_length, ("rnd",), 10)]), ("Compare lengths", [ru(ukc.set_compare, ("rnd",), 20)]),
           ("Add and subtract lengths", [co(A.len_addsub, 20)]), ("Estimate lengths", [co(A.len_est, 20)]), ("Length word problems", [co(A.len_word, 20)])],
          ul(["1 km = 1,000 m, 1 m = 100 cm, 1 cm = 10 mm.", "To add or subtract km and m, change everything to metres, work it out, then change back.",
              "Use km for long distances (between towns), m for rooms and fields, cm for small objects."]),
          [example("3 km 450 m + 2 km 780 m", ["3,450 m + 2,780 m = 6,230 m"], "6 km 230 m")],
          [["1 km = 100 m", "1 km = 1,000 m."], ["Adding km and m separately without carrying", "780 m + 450 m = 1,230 m = 1 km 230 m."], ["Using the wrong unit", "A town is km away, not m."]],
          [("How long is 1 km?", "About 12 minutes of walking."), ("What does kilo mean?", "A thousand."), ("How do I measure a long distance?", "With a tape measure, a trundle wheel or a map.")]),

        U("weight", "M", "Add and subtract weights in kilograms and grams; multiply and divide weights by whole numbers; estimate weights.",
          "Weight: Kilograms and Grams", "Weight",
          "Free Primary 4 maths worksheets on weight: converting kilograms and grams, adding, subtracting, multiplying and dividing weights, reading scales and estimating weights. 100 questions with answers.",
          "1 kg = 1,000 g", "Change to grams, then calculate.",
          [("Kilograms and grams", [co(A.wt_conv, 20)]), ("Add and subtract weights", [co(A.wt_addsub, 20)]), ("Multiply and divide weights", [co(A.wt_muldiv, 20)]),
           ("Read the scale", [ru(usmv.set_scale, ("rnd",), 20)]), ("Estimate weights", [co(A.wt_est, 20)])],
          ul(["1 kg = 1,000 g. 2 kg 350 g = 2,350 g.", "To calculate, change to grams, work it out, then change back to kg and g.",
              "Heavy things (people, bags of rice) are weighed in kg; light things (an egg, a pencil) in g."]),
          [example("4 kg 600 g − 1 kg 850 g", ["4,600 g − 1,850 g = 2,750 g"], "2 kg 750 g")],
          [["1 kg = 100 g", "1 kg = 1,000 g."], ["Reading the wrong scale marks", "Find what one small mark is worth first."], ["Forgetting to regroup", "1,450 g = 1 kg 450 g."]],
          [("What is the difference between mass and weight?", "In everyday life we say weight. Both are measured here in kg and g."), ("How heavy is 1 kg?", "About a bag of sugar or a big tuber of yam."), ("What do we use to weigh things?", "Scales or a balance.")]),

        U("perimeter-and-area", "M", "Find the perimeter and area of squares and rectangles; solve problems on perimeter and area.",
          "Perimeter and Area of Squares and Rectangles", "Perimeter and Area",
          "Free Primary 4 maths worksheets on the perimeter and area of squares and rectangles: perimeter by adding sides, area by counting squares and by length × breadth, missing sides and word problems. 100 questions with answers.",
          "Perimeter = distance round", "Area = length × breadth.",
          [("Perimeter of rectangles", [ru(uk4a.set_rect_perimeter, ("rnd",), 20)]), ("Area by counting squares", [ru(uk4a.set_area, ("rnd",), 20)]),
           ("Squares", [ru(sga.set_square, ("rnd", sga.People), 20)]), ("Find the missing side", [ru(sga.set_missing, ("rnd", sga.People), 20)]),
           ("Perimeter and area problems", [ru(sga.set_story, ("rnd", sga.People), 20)])],
          ul(["Perimeter is the distance all the way round a shape. Rectangle: 2 × (length + breadth). Square: 4 × side.",
              "Area is the space inside a shape, measured in square units (cm², m²). Rectangle: length × breadth. Square: side × side."]),
          [example("Rectangle 9 m by 5 m", ["Perimeter: 2 × (9 + 5)", "Area: 9 × 5"], "28 m and 45 m²")],
          [["Mixing up perimeter and area", "Perimeter adds sides; area multiplies length by breadth."], ["Adding only two sides", "A rectangle has four sides."], ["Wrong units", "Perimeter in m, area in m²."]],
          [("Why is area in square units?", "We count how many unit squares cover the shape."), ("Can two shapes have the same area but different perimeters?", "Yes. A 4 × 4 square and a 2 × 8 rectangle both have area 16."), ("Where do we use area?", "For floors, farms and painting walls.")]),

        U("time", "M", "Tell time on analogue and digital clocks; use a.m. and p.m.; convert between hours, minutes and seconds; use the calendar (days, weeks, months and years).",
          "Time: Clocks, a.m. and p.m., and the Calendar", "Time",
          "Free Primary 4 maths worksheets on time: hours, minutes and seconds, a.m. and p.m., time taken, the calendar and time word problems. 100 questions with answers.",
          "1 hour = 60 minutes", "a.m. before noon, p.m. after noon.",
          [("Hours, minutes and seconds", [co(pht.one_tconv, 10), ru(ukc.set_time, ("rnd",), 10)]), ("Time taken on the clock", [ru(ust.set_elapsed, ("rnd",), 20)]),
           ("a.m. and p.m.", [co(pht.one_elapsed, 20)]), ("The calendar", [co(A.cal_days, 8), co(A.cal_after, 6), co(A.cal_span, 6)]), ("Time word problems", [ru(ust.set_story, ("rnd",), 20)])],
          ul(["1 minute = 60 seconds, 1 hour = 60 minutes, 1 day = 24 hours, 1 week = 7 days, 1 year = 12 months.",
              "a.m. is from midnight to midday (morning); p.m. is from midday to midnight.", "To find time taken, count on: first to the next hour, then the rest."]),
          [example("8:45 a.m. to 11:20 a.m.", ["8:45 → 9:00 = 15 min", "9:00 → 11:20 = 2 h 20 min"], "2 hours 35 minutes")],
          [["Treating time like decimals", "1 hour 30 minutes is not 1.30 hours."], ["Mixing up a.m. and p.m.", "School starts in the morning (a.m.)."], ["Forgetting months have different lengths", "30 days hath September, April, June and November."]],
          [("How many days are in a leap year?", "366; February has 29 days."), ("What is 3:15 called?", "A quarter past three."), ("What is noon?", "12:00 midday.")]),

        U("capacity", "M", "Identify standard containers; measure capacity in litres and centilitres; add, subtract, multiply and divide capacities; solve real-life problems.",
          "Capacity: Litres and Centilitres", "Capacity",
          "Free Primary 4 maths worksheets on capacity: litres and centilitres, adding, subtracting, multiplying and dividing capacities, reading containers and estimating. 100 questions with answers.",
          "1 litre = 100 cl", "Change to centilitres, then calculate.",
          [("Litres and centilitres", [co(A.cap_conv, 20)]), ("Add and subtract capacities", [co(A.cap_addsub, 20)]), ("Multiply and divide capacities", [co(A.cap_muldiv, 20)]),
           ("Read the container", [ru(usmv.set_container, ("rnd",), 20)]), ("Estimate capacity", [co(A.cap_est, 20)])],
          ul(["Capacity is how much a container can hold. We measure it in litres and centilitres (cl): 1 litre = 100 cl.",
              "Change to centilitres to calculate: 2 litres 35 cl = 235 cl.", "Standard containers include 50 cl bottles, 1-litre bottles, 25-litre jerrycans and 200-litre drums."]),
          [example("3 litres 60 cl + 1 litre 75 cl", ["360 cl + 175 cl = 535 cl"], "5 litres 35 cl")],
          [["1 litre = 1,000 cl", "1 litre = 100 cl (1,000 ml)."], ["Adding litres and cl without regrouping", "135 cl = 1 litre 35 cl."], ["Reading the wrong mark", "Find what each small mark is worth."]],
          [("What is a centilitre?", "One hundredth of a litre."), ("How much is a 50 cl bottle?", "Half a litre."), ("Why use standard containers?", "So everyone gets the same amount when buying and selling.")]),

        U("plane-shapes-symmetry-and-angles", "G", "Identify lines of symmetry; draw horizontal and vertical lines; identify cardinal points; identify right, acute and obtuse angles.",
          "Plane Shapes: Symmetry, Lines, Cardinal Points and Angles", "Symmetry, Lines and Angles",
          "Free Primary 4 maths worksheets on lines of symmetry, horizontal and vertical lines, the cardinal points of the compass and right, acute and obtuse angles. 100 questions with answers.",
          "A line of symmetry makes two matching halves", "Right angle = 90°.",
          [("Lines of symmetry", [ru(usy.set_is_line, ("rnd",), 10), ru(usy.set_count, ("rnd",), 10)]), ("Horizontal and vertical lines", [co(A.hv_line, 8), co(A.hv_real, 12)]),
           ("Cardinal points", [co(A.cp_opposite, 6), co(A.cp_map, 14)]), ("Turning", [co(A.cp_turn, 20)]), ("Right, acute and obtuse angles", [ru(usang.set_kinds, ("rnd",), 20)])],
          ul(["A line of symmetry divides a shape into two halves that fit exactly on each other when folded.", "A horizontal line goes straight across; a vertical line goes straight up and down.",
              "The cardinal points are North, East, South and West. Between them are North-East, South-East, South-West and North-West.",
              "A right angle is a quarter turn (90°). An acute angle is smaller; an obtuse angle is bigger than a right angle but smaller than a straight line."]),
          [example("Facing North, make a quarter turn clockwise", ["N → E"], "East"), example("How many lines of symmetry does a square have?", ["2 through the sides, 2 through the corners"], "4")],
          [["Taking a diagonal of a rectangle as a line of symmetry", "Fold it: the halves do not match."], ["Mixing up clockwise and anticlockwise", "Clockwise goes the way the hands of a clock turn."], ["Thinking a bigger drawing means a bigger angle", "The size of an angle is the amount of turn."]],
          [("How many right angles are in a full turn?", "Four."), ("Which direction does the sun rise?", "East."), ("Does a circle have lines of symmetry?", "Yes, every line through its centre.")]),

        U("3d-shapes", "G", "Identify three-dimensional shapes; distinguish between 2D and 3D shapes; state the properties of 3D shapes (faces, edges and vertices); identify uses of 3D shapes at home.",
          "3D Shapes: Cubes, Cuboids, Cylinders, Cones and Spheres", "3D Shapes",
          "Free Primary 4 maths worksheets on 3D shapes: naming cubes, cuboids, cylinders, cones, spheres and pyramids, 2D or 3D, faces, edges and vertices, and 3D shapes at home. 100 questions with answers.",
          "3D shapes are solid", "Faces, edges and vertices.",
          [("Name the 3D shape", [ru(uks.set_name3d, ("rnd", uks.Pos), 20)]), ("2D or 3D?", [co(A.dim23, 20)]), ("Faces, edges and vertices", [co(A.fev, 10), ru(uks.set_fev, ("rnd",), 10)]),
           ("Faces of 3D shapes", [ru(sg3.set_faces, (sg3.Pos, sg3.People2), 20)]), ("3D shapes at home", [co(A.obj3d, 20)])],
          ul(["2D shapes are flat; 3D shapes are solid and have length, breadth and height.", "A face is a flat or curved surface, an edge is where two faces meet and a vertex is a corner.",
              "A cube has 6 square faces, 12 edges and 8 vertices. A cylinder has 2 flat faces and 1 curved face."]),
          [example("A cuboid", ["6 faces, 12 edges, 8 vertices"], "Like a box of matches")],
          [["Calling a cube a square", "A square is flat (2D); a cube is solid (3D)."], ["Counting the same edge twice", "Mark each edge as you count."], ["Forgetting curved faces", "A cylinder has a curved face as well as two flat faces."]],
          [("Which 3D shape can roll and stack?", "A cylinder."), ("What is a vertex?", "A corner where edges meet."), ("Where do we see cuboids?", "Boxes, bricks and books.")]),

        U("everyday-statistics", "S", "Collect and present data in pictograms and bar charts; find the mode of a set of data; describe the chance of simple events.",
          "Everyday Statistics: Pictograms, Bar Charts, Mode and Chance", "Everyday Statistics",
          "Free Primary 4 maths worksheets on everyday statistics: reading pictograms and bar charts, finding the mode, and describing chance as impossible, unlikely, likely or certain. 100 questions with answers.",
          "Mode = the most common value", "Check the key before counting.",
          [("Pictograms", [ru(ukst.set_pictogram, ("rnd", ukst.Picker), 20)]), ("Bar charts", [ru(ukst.set_bar, ("rnd", ukst.Picker), 20)]), ("Find the mode", [co(A.mode_list, 12), co(A.mode_table, 8)]),
           ("How likely is it?", [co(A.chance_word, 10), ru(auc.set_everyday, ("rnd",), 10)]), ("Spinners and bags", [ru(auc.set_spinners, ("rnd",), 10), ru(auc.set_bags, ("rnd",), 10)])],
          ul(["A pictogram uses pictures to show data. Always read the key: one picture may stand for 2, 5 or 10 things.",
              "A bar chart uses bars. Read the height of each bar on the scale.", "The mode is the value that appears most often.",
              "Chance describes how likely something is: impossible, unlikely, equally likely, likely or certain."]),
          [example("Scores 4, 7, 4, 9, 4, 6", ["4 appears 3 times"], "Mode = 4")],
          [["Ignoring the key in a pictogram", "Multiply the number of pictures by what one picture stands for."], ["Giving how many times, not the value", "The mode is the value, not how often it appears."], ["Thinking unlikely means impossible", "Unlikely things can still happen."]],
          [("What is data?", "Facts and numbers we collect, such as favourite foods."), ("Can there be two modes?", "Yes, if two values appear equally often."), ("What is probability?", "How likely something is to happen.")]),
    ]


def build(i):
    us = units()
    u = us[i - 1]
    sets, rnd = build_sets(u["sets"], 150400 + i)
    finish(sets, rnd)
    body = lesson(u["think"], u["ex"], u["mist"])
    make(u["slug"], i, TH[u["th"]], "Primary 4: " + TH[u["th"]], u["std"] + " (summary of the NERDC Primary 4 Mathematics curriculum)",
         u["title"], u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets)
    return u["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    n = len(units())
    for i in range(1, n + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
