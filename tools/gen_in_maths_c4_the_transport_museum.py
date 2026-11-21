# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 13: The Transport Museum (Multiplication and Division of Larger Numbers)
Division with and without remainders, dividing 2- and 3-digit numbers, multiplying 3-digit numbers and transport stories (Ontario Grade 4, SG Primary 4 and UK Year 4 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g4_division", 604130)
sg = mod("gen_sg_maths_p4_division", 604131)
sm = mod("gen_uk_maths_y4_short_multiplication", 604132)
unit(4, "the-transport-museum", 13, "N", 13, "The Transport Museum", "Multiplication and Division of Larger Numbers", "multiply and divide",
     "Multiplication and division: multiplying 2- and 3-digit numbers, dividing by 1-digit numbers with remainders, and solving problems (summary of NCERT Maths Mela Class 4)",
     "Class 4 The Transport Museum worksheet (Maths Mela Chapter 13): short division, remainders, 3-digit multiplication and stories. 100 questions with answers.",
     "Division shares equally; the remainder is left over.", "Check: quotient × divisor + remainder = number.",
     "<ul><li>84 ÷ 4: 8 tens ÷ 4 = 2 tens, 4 ones ÷ 4 = 1, so 21.</li><li>59 ÷ 4 = 14 remainder 3, because 4 × 14 = 56 and 3 is left.</li></ul>",
     [('A bus has 48 seats in rows of 4. How many rows?', ['48 ÷ 4'], '12')],
     [['Remainder bigger than the divisor', 'If the remainder is too big, one more group fits.'], ['Dropping a zero (306 ÷ 3 = 12)', '306 ÷ 3 = 102: keep the 0 in the tens.']],
     [('What is a remainder?', 'The amount left over when a number cannot be divided exactly.'), ('How do I check a division?', 'Multiply the answer by the divisor and add the remainder.')],
     [('Division facts', [rn(sg, "set_facts", 20)]),
      ('Short division', [rn(ca, "set_short", 20)]),
      ('Remainders', [rn(sg, "set_remainders", 15), rn(ca, "set_groups", 5)]),
      ('Multiplying 3-digit numbers', [rn(sm, "set_short3", 20)]),
      ('Transport stories', [rn(ca, "set_story", 20)])], 60413)
