# -*- coding: utf-8 -*-
"""India Class 4 Maths, Maths Mela Chapter 3: Pattern Around Us (Number and Shape Patterns)
Repeating and growing patterns, pattern rules, odd and even patterns and predicting (Ontario Grade 4, AU Year 4 and US Grade 4 set makers)."""
from in_prim import unit, mod, rn, co, le

ca = mod("gen_caon_math_g4_patterns", 604030)
oe = mod("gen_au_maths_y4_odd_even", 604031)
us = mod("gen_us_math_g4_patterns", 604032)
unit(4, "pattern-around-us", 3, "P", 3, "Pattern Around Us", "Number and Shape Patterns", "patterns",
     "Patterns: identifying, extending and creating shape and number patterns, finding the rule, and odd and even numbers (summary of NCERT Maths Mela Class 4)",
     "Class 4 Pattern Around Us worksheet (Maths Mela Chapter 3): repeating and growing patterns, rules, odd and even numbers. 100 questions with answers.",
     "Find the rule, then use it.", "Growing patterns change by the same amount each time.",
     "<ul><li><b>Repeating</b> patterns repeat a core: ▲●●▲●●.</li><li><b>Growing</b> patterns change by a rule: 4, 7, 10, 13 (add 3).</li><li>Even + even = even, odd + odd = even, odd + even = odd.</li></ul>",
     [('What comes next: 5, 9, 13, 17, …?', ['Add 4 each time'], '21')],
     [['Using the first difference only', 'Check the rule works for every step.'], ['Thinking odd + odd is odd', '3 + 5 = 8, which is even.']],
     [('What is a pattern rule?', "The instruction that makes each term from the one before, such as 'add 5'."), ('Why are odd + odd numbers even?', 'The two odd ones pair up to make a pair.')],
     [('Repeating patterns', [rn(ca, "set_repeating", 20)]),
      ('Growing patterns', [rn(ca, "set_growing", 20)]),
      ('Find the rule', [rn(ca, "set_rules", 10), rn(us, "set_find_rule", 10)]),
      ('Odd and even', [rn(oe, "set_odd_even", 10), rn(oe, "set_rules", 10)]),
      ('Predict', [rn(ca, "set_predict", 10), rn(us, "set_extend", 10)])], 60403)
