# -*- coding: utf-8 -*-
"""India Class 5 Maths, Maths Mela Chapter 9: Coconut Farm (Division)
Short division with and without remainders, dividing 4-digit numbers, interpreting remainders and coconut farm stories (UK Year 5 and AU Year 5 set makers)."""
from in_prim import unit, mod, rn, co, le

uk = mod("gen_uk_maths_y5_short_division", 605090)
au = mod("gen_au_maths_y5_division", 605091)
unit(5, "coconut-farm", 9, "N", 9, "Coconut Farm", "Division", "division",
     "Division: dividing larger numbers by 1- and 2-digit numbers, remainders, and solving problems (summary of NCERT Maths Mela Class 5)",
     "Class 5 Coconut Farm worksheet (Maths Mela Chapter 9): short division, remainders and division stories. 100 questions with answers.",
     "Divide each place from the left.", "Check: quotient × divisor + remainder.",
     "<ul><li>Short division: 864 ÷ 4 → 8 ÷ 4 = 2, 6 ÷ 4 = 1 r 2, 24 ÷ 4 = 6, so 216.</li><li>Think about the remainder: 50 coconuts in bags of 8 needs 7 bags.</li></ul>",
     [('1,236 coconuts are packed 6 to a sack.', ['1,236 ÷ 6'], '206 sacks')],
     [['Skipping a zero in the answer', 'Write 0 when a place cannot be divided.'], ['Ignoring what the remainder means', 'Sometimes you need one more group.']],
     [('What is short division?', 'A quick written method for dividing by a 1-digit number.'), ('What do I do with a remainder?', 'It depends on the story: round up, round down or share it.')],
     [('Divide exactly', [rn(uk, "set_exact", 20)]),
      ('Remainders', [rn(uk, "set_rem3", 10), rn(au, "set_remainders", 10)]),
      ('Dividing 4-digit numbers', [rn(uk, "set_four", 10), rn(au, "set_four", 10)]),
      ('What does the remainder mean?', [rn(uk, "set_context", 10), rn(au, "set_context", 10)]),
      ('Coconut farm stories', [rn(uk, "set_story", 10), rn(au, "set_story", 10)])], 60509)
