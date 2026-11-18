# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Equivalent and Comparing Fractions (TEKS 4.3C, 4.3D)
  python3 tools/gen_ustx_math_g4_equivalent_comparing_fractions.py
Equivalent fractions with models, multiplying and dividing the numerator and denominator by the same number,
comparing fractions with models, with common denominators and with benchmarks, and word problems. The question
makers come from the US Grade 4 equivalent and compare fraction units with Texas names.
Wrong answers come from real mistakes: multiplying only the denominator, thinking a bigger denominator means a
bigger fraction, and comparing only the numerators.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_equivalent_fractions as use
import gen_us_math_g4_compare_fractions as usc
adopt(use)
adopt(usc)
tx_common.GRADE = "grade-4"



def build():
    sets, R = build_sets([
        ("Equivalent fractions in models", [("run", use.set_models, ("rnd",), 20)]),
        ("Multiply or divide the top and bottom", [("run", use.set_multiply, ("rnd",), 10), ("run", use.set_divide, ("rnd",), 10)]),
        ("Compare with fraction models", [("run", usc.set_models, ("rnd", usc.People), 20)]),
        ("Compare with common denominators and benchmarks", [("run", usc.set_common_den, ("rnd", usc.People), 10), ("run", usc.set_benchmarks, ("rnd", usc.People), 10)]),
        ("Word problems", [("run", usc.set_words, ("rnd", usc.People), 10), ("run", use.set_words, ("rnd",), 10)]),
    ], 64015)
    finish(sets, R)
    body = lesson('<ul><li><b>Equivalent fractions</b> name the same amount. Multiply or divide the numerator and the denominator by the same number: 2/3 = 8/12.</li><li>To <b>compare</b> fractions with different denominators, rename them with a common denominator, or compare each to a benchmark such as 1/2.</li><li>Use &gt;, &lt; or = to record the comparison. The wholes must be the same size.</li></ul>',
        [example("Compare 3/4 and 5/8.", ["3/4 = 6/8", "6/8 &gt; 5/8"], "3/4 &gt; 5/8"), example("Compare 2/5 and 7/10 using 1/2.", ["2/5 is less than 1/2.", "7/10 is more than 1/2."], "2/5 &lt; 7/10")],
        [['Multiplying only the denominator', 'Multiply the numerator and the denominator by the same number.'], ['Thinking 1/8 &gt; 1/4 because 8 &gt; 4', 'More parts means smaller parts.'], ['Comparing only the numerators of 3/4 and 3/8 the wrong way', 'With the same numerator, the smaller denominator is the bigger fraction.']])
    faq = [('What does TEKS 4.3C ask?', 'Determine if two fractions are equivalent using a variety of methods.'), ('What does TEKS 4.3D ask?', 'Compare two fractions with different numerators and different denominators and represent the comparison with &gt;, &lt; or =.'), ('How do you find a common denominator?', 'Find a number that both denominators divide into, such as 12 for 3 and 4. Then rename both fractions.'), ('What are benchmark fractions?', 'Easy fractions like 0, 1/2 and 1 that help you compare. 3/8 is less than 1/2, and 5/6 is more than 1/2.')]
    make('equivalent-and-comparing-fractions', 15, 'Number and Operations', '4.3C, 4.3D',
         '4.3C determine if two given fractions are equivalent using a variety of methods; 4.3D compare two fractions with different numerators and different denominators and represent the comparison using the symbols >, =, or <',
         'Equivalent and Comparing Fractions', 'Equivalent and Comparing Fractions',
         'Free Grade 4 fraction worksheets for Texas TEKS 4.3C and 4.3D: equivalent fractions with models and multiplying, comparing fractions with models, common denominators and benchmarks, and word problems. 100 questions with answers.',
         'Multiply or divide the top and bottom by the same number to make an equivalent fraction.', 'To compare, use a common denominator or a benchmark like 1/2.',
         body, faq, sets, seo_title='Grade 4 Equivalent and Comparing Fractions Worksheets (TEKS 4.3C, 4.3D, STAAR)')


if __name__ == "__main__":
    build()
