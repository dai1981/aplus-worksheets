# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Adding and Subtracting Fractions with Like Denominators (TEKS 4.3E, 4.3F)
  python3 tools/gen_ustx_math_g4_add_subtract_fractions.py
Adding and subtracting fractions and mixed numbers with equal denominators, word problems (the US Grade 4 makers
with Texas names), and judging whether a sum or difference is reasonable with the benchmarks 0, 1/4, 1/2, 3/4 and 1.
Wrong answers come from real mistakes: adding the denominators, forgetting to rename a whole when subtracting
mixed numbers, and not checking with benchmarks.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_add_subtract_fractions as usf
adopt(usf)
tx_common.GRADE = "grade-4"

def one_bench(r):
    d = r.choice([6, 8, 10, 12])
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    if a + b > d + 2:
        return None
    s = a + b
    kind = r.choice(["near", "more_less", "check"])
    if kind == "near":
        opts = [(0, "0"), (0.5, fr(1, 2)), (1, "1"), (1.5, "1" + fr(1, 2))]
        v = s / float(d)
        best = min(opts, key=lambda o: abs(o[0] - v))
        if abs(abs(best[0] - v) - min(abs(o[0] - v) for o in opts if o != best)) < 0.05:
            return None
        return mcq("Estimate with benchmarks. %s + %s is closest to which number?" % (fr(a, d), fr(b, d)), best[1], [o[1] for o in opts if o != best],
                   "%s + %s = %s, which is closest to <b>%s</b>." % (fr(a, d), fr(b, d), fr(s, d), best[1]))
    if kind == "more_less":
        if s * 2 == d:
            return None
        right = "More than %s" % fr(1, 2) if s * 2 > d else "Less than %s" % fr(1, 2)
        return mcq("Is %s + %s more or less than %s?" % (fr(a, d), fr(b, d), fr(1, 2)), right, ["Less than %s" % fr(1, 2) if s * 2 > d else "More than %s" % fr(1, 2), "Exactly 1", "We cannot tell without a picture"],
                   "%s + %s = %s, and %s is half of %d, so <b>%s</b>." % (fr(a, d), fr(b, d), fr(s, d), d // 2, d, right.lower()))
    k = Kid(r).next()
    wrong_ans = fr(s, 2 * d)
    return mcq("%s says %s + %s = %s. Is that reasonable?" % (k["n"], fr(a, d), fr(b, d), wrong_ans),
               "No. The sum must be more than %s" % fr(max(a, b), d),
               ["Yes. Add the tops and the bottoms", "Yes. It is close to %s" % fr(1, 2), "No. The sum must be more than 2"],
               "Adding the denominators makes the pieces smaller. The real sum is %s, which is more than %s: <b>No</b>." % (fr(s, d), fr(max(a, b), d)))


def build():
    sets, R = build_sets([
        ("Add fractions", [("run", usf.set_add, ("rnd", usf.People), 20)]),
        ("Subtract fractions", [("run", usf.set_subtract, ("rnd", usf.People), 20)]),
        ("Add and subtract mixed numbers", [("run", usf.set_mixed, ("rnd",), 20)]),
        ("Is it reasonable? Benchmark fractions", [("collect", one_bench, 20)]),
        ("Fraction word problems", [("run", usf.set_words, ("rnd", usf.People), 20)]),
    ], 64016)
    finish(sets, R)
    body = lesson('<ul><li>With equal denominators, the pieces are the same size. Add or subtract the <b>numerators</b> and keep the denominator: 3/8 + 2/8 = 5/8.</li><li>For mixed numbers, add or subtract the wholes and the fractions. Rename 1 whole as 8/8 when you need more eighths.</li><li>Check with <b>benchmarks</b> 0, 1/4, 1/2, 3/4 and 1: 3/8 + 4/8 is a bit less than 1.</li></ul>',
        [example("3 1/6 − 1 5/6", ["You cannot take 5/6 from 1/6.", "Rename: 3 1/6 = 2 7/6.", "2 7/6 − 1 5/6 = 1 2/6"], "1 2/6"), example("Is 5/8 + 1/8 close to 3/4?", ["5/8 + 1/8 = 6/8", "6/8 = 3/4"], "yes, exactly 3/4")],
        [['Adding the denominators: 1/4 + 2/4 = 3/8', 'Keep the denominator. Only the numerators change.'], ['Not renaming a whole: 3 1/6 − 1 5/6 = 2 4/6', 'Rename 1 whole as 6/6 first.'], ['Skipping the estimate', 'Compare with 1/2 or 1 to see if the answer makes sense.']])
    faq = [('What does TEKS 4.3E ask?', 'Represent and solve addition and subtraction of fractions with equal denominators using objects and pictorial models that build to the number line and properties of operations.'), ('What does TEKS 4.3F ask?', 'Evaluate the reasonableness of sums and differences of fractions using benchmark fractions 0, 1/4, 1/2, 3/4 and 1, referring to the same whole.'), ('Why do the denominators stay the same?', 'The denominator names the size of the pieces. Adding pieces of the same size does not change their size.'), ('How do you subtract mixed numbers?', 'Subtract the fractions, then the wholes. If the first fraction is too small, rename one whole as a fraction first.')]
    make('adding-and-subtracting-fractions', 16, 'Number and Operations', '4.3E, 4.3F',
         '4.3E represent and solve addition and subtraction of fractions with equal denominators using objects and pictorial models that build to the number line and properties of operations; 4.3F evaluate the reasonableness of sums and differences of fractions using benchmark fractions 0, 1/4, 1/2, 3/4, and 1, referring to the same whole',
         'Adding and Subtracting Fractions with Like Denominators', 'Adding and Subtracting Fractions',
         'Free Grade 4 fraction worksheets for Texas TEKS 4.3E and 4.3F: add and subtract fractions and mixed numbers with like denominators, check with benchmark fractions, and word problems. 100 questions with answers.',
         'Same denominator: add or subtract the numerators, keep the denominator.', 'Check with benchmarks 0, 1/4, 1/2, 3/4 and 1. Rename a whole to subtract mixed numbers.',
         body, faq, sets, seo_title='Grade 4 Adding and Subtracting Fractions Worksheets (TEKS 4.3E, 4.3F, STAAR)')


if __name__ == "__main__":
    build()
