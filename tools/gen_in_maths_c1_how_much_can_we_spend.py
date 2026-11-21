# -*- coding: utf-8 -*-
"""India Class 1 Maths, Joyful Mathematics Chapter 12: How Much Can We Spend? (Money)
Indian coins and notes up to ₹100: naming, counting, comparing, making amounts and simple shopping (own makers, in_money)."""
from in_prim import unit, co
import in_money as m
unit(1, "how-much-can-we-spend", 12, "N", 12, "How Much Can We Spend?", "Indian Coins and Notes up to ₹100", "money",
     "Money: identifying Indian coins and notes, adding small amounts, and simple buying and selling up to ₹100 (summary of NCERT Joyful Mathematics Class 1)",
     "Class 1 How Much Can We Spend? worksheet (Joyful Mathematics Chapter 12): Indian coins and notes, counting money, comparing and shopping up to ₹100. 100 picture questions with answers.",
     "Count the value, not the number of coins.", "Start with the biggest note or coin.",
     "<ul><li>Coins: ₹1, ₹2, ₹5, ₹10, ₹20. Notes: ₹10, ₹20, ₹50, ₹100.</li><li>To count money, start with the biggest and count on: ₹50, ₹60, ₹65, ₹67.</li></ul>",
     [("₹20 note, ₹10 coin, ₹5 coin, ₹2 coin", ["20, 30, 35, 37"], "₹37")],
     [["Counting coins one each", "A ₹5 coin is worth 5, not 1."], ["Thinking more coins means more money", "Three ₹1 coins are less than one ₹5 coin."]],
     [("Which coins should Class 1 children know?", "₹1, ₹2, ₹5, ₹10 and ₹20 coins, and notes up to ₹100."), ("How can children practise?", "Play shop with toy money and small price tags.")],
     [("Coins and notes", [co(m.one_name(100), 10), co(m.one_cmp(100), 10)]),
      ("Count the money", [co(m.one_count(50, (2, 4)), 20)]),
      ("More money", [co(m.one_count(100), 20)]),
      ("Make the amount", [co(m.one_make(100), 20)]),
      ("Shopping", [co(m.one_buy(100), 20)])], 60112)
