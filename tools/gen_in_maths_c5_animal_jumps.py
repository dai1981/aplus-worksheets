# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 13: Animal Jumps (Multiples and Factors)
Multiples, common multiples, factors, prime numbers, square numbers and divisibility (UK Year 5 and AU Year 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_factors_primes", 605130)
au = mod("gen_au_maths_y5_factors", 605131)
unit(5, "animal-jumps", 13, "N", 13, "Animal Jumps", "Multiples and Factors", "multiples and factors",
     "Multiples and factors: skip counting as jumps, common multiples, factors, prime and composite numbers, and tests of divisibility (summary of NCERT Maths Mela Class 5)",
     "Class 5 Animal Jumps worksheet (Maths Mela Chapter 13): multiples, common multiples, factors, primes, squares and divisibility. 100 questions with answers.",
     "Multiples are the jumps; factors divide exactly.", "A prime number has exactly two factors.",
     "<ul><li>A frog jumping 4 at a time lands on multiples of 4: 4, 8, 12 ….</li><li>Two animals land on the same stone at common multiples: 3 and 4 → 12, 24 ….</li><li>Factors of 12: 1, 2, 3, 4, 6, 12.</li></ul>",
     [('A rabbit jumps 3 and a frog jumps 5. Where do they first land together?', ['Lowest common multiple of 3 and 5'], '15')],
     [['Mixing up factors and multiples', 'Factors divide the number; multiples are in its times table.'], ['Calling 1 a prime', '1 has only one factor.']],
     [('What is a common multiple?', 'A number that is a multiple of two or more numbers, like 12 for 3 and 4.'), ('What is a prime number?', 'A number with exactly two factors: 1 and itself.')],
     [('Multiples', [rn(uk, "set_multiples", 10), rn(au, "set_multiples", 10)]),
      ('Factors', [rn(uk, "set_factors", 10), rn(au, "set_factors", 10)]),
      ('Prime numbers', [rn(uk, "set_primes", 20)]),
      ('Square numbers and divisibility', [rn(uk, "set_squares", 10), rn(au, "set_divisibility", 10)]),
      ('Jump stories', [rn(uk, "set_words", 10), rn(au, "set_words", 10)])], 60513)
