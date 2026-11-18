# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Order of Operations: Parentheses and Brackets (TEKS 5.4E, 5.4F)
  python3 tools/gen_ustx_math_g5_order_of_operations.py
Multiplication and division before addition and subtraction, parentheses first, brackets and braces from the
inside out, writing expressions from words, and interpreting expressions. The question makers come from the US
Grade 5 expressions unit with Texas names.
Wrong answers come from real mistakes: working left to right without the order of operations, ignoring brackets,
and putting parentheses in the wrong place.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g5_expressions as use
adopt(use)
tx_common.GRADE = "grade-5"



def build():
    sets, R = build_sets([
        ("Multiply and divide before adding and subtracting", [("run", use.set_order, ("rnd", use.People), 20)]),
        ("Parentheses first", [("run", use.set_parentheses, ("rnd", use.People), 20)]),
        ("Brackets: work from the inside out", [("run", use.set_nested, ("rnd", use.People), 20)]),
        ("Write expressions from words", [("run", use.set_words, ("rnd", use.People), 20)]),
        ("Interpret expressions and word problems", [("run", use.set_interpret, ("rnd", use.People), 20)]),
    ], 65015)
    finish(sets, R)
    body = lesson('<ul><li>Do what is inside <b>parentheses</b> ( ) first. With <b>brackets</b> [ ], start with the innermost grouping and work out.</li><li>Then multiply and divide from left to right.</li><li>Then add and subtract from left to right.</li></ul>',
        [example("[2 + (4 × 5)] × 6", ["4 × 5 = 20", "2 + 20 = 22", "22 × 6 = 132"], "132"), example("9 + 5 × 8", ["5 × 8 = 40", "9 + 40 = 49"], "49")],
        [['Working left to right: 9 + 5 × 8 = 112', 'Multiply before adding.'], ['Ignoring the inner parentheses in brackets', 'Start with the innermost grouping.'], ['Putting parentheses in the wrong place', 'Group the part that the words say to do first.']])
    faq = [('What does TEKS 5.4E ask?', 'Describe the meaning of parentheses and brackets in a numeric expression.'), ('What does TEKS 5.4F ask?', 'Simplify numerical expressions that do not involve exponents, including up to two levels of grouping.'), ('What is the difference between parentheses and brackets?', 'Both group numbers. Brackets [ ] are used outside parentheses so you can see the order: [3 × (2 + 5)].'), ('Why do we need an order of operations?', 'So everyone gets the same value for the same expression.')]
    make('order-of-operations', 15, 'Algebraic Reasoning', '5.4E, 5.4F',
         '5.4E describe the meaning of parentheses and brackets in a numeric expression; 5.4F simplify numerical expressions that do not involve exponents, including up to two levels of grouping',
         'Order of Operations: Parentheses and Brackets', 'Order of Operations',
         'Free Grade 5 order of operations worksheets for Texas TEKS 5.4E and 5.4F: multiply before adding, parentheses, brackets, writing expressions from words and interpreting expressions. 100 questions with answers.',
         'Parentheses and brackets first, then × and ÷, then + and −.', 'Work from the innermost grouping out. Multiply and divide from left to right before adding and subtracting.',
         body, faq, sets, seo_title='Grade 5 Order of Operations Worksheets: Parentheses and Brackets (TEKS 5.4E, 5.4F, STAAR)')


if __name__ == "__main__":
    build()
