# -*- coding: utf-8 -*-
"""India Class 2 Maths, Joyful Mathematics Chapter 10: Fun at the Fair (Money)
Indian coins and notes up to ₹100 (and ₹200): counting, making amounts, comparing prices, buying and change (in_money)."""
from in_prim import unit, co
import in_money as m
unit(2, "fun-at-the-fair", 10, "N", 10, "Fun at the Fair", "Money: Coins, Notes, Buying and Change", "money",
     "Money: recognising coins and notes, counting money, adding and subtracting amounts in buying and selling (summary of NCERT Joyful Mathematics Class 2)",
     "Class 2 Fun at the Fair worksheet (Joyful Mathematics Chapter 10): Indian coins and notes, counting money, making amounts, buying and change. 100 picture questions with answers.",
     "Count the biggest note first.", "Change = money given − price.",
     "<ul><li>Coins: ₹1, ₹2, ₹5, ₹10, ₹20. Notes: ₹10, ₹20, ₹50, ₹100, ₹200.</li><li>To find the cost of two things, add. To find change, subtract the price from the money given.</li></ul>",
     [("A kite costs ₹12. You pay with a ₹20 note.", ["₹20 − ₹12"], "₹8 change")],
     [["Counting coins instead of their value", "Add the amounts written on them."], ["Adding when finding change", "Change is the money given minus the price."]],
     [("What is change?", "The money you get back when you pay more than the price."), ("Which notes should Class 2 children know?", "₹10, ₹20, ₹50, ₹100 and ₹200.")],
     [("Coins and notes", [co(m.one_name(200), 8), co(m.one_cmp(200), 12)]),
      ("Count the money", [co(m.one_count(100), 20)]),
      ("Make the amount", [co(m.one_make(100), 20)]),
      ("Bigger amounts", [co(m.one_count(200, (3, 5)), 20)]),
      ("At the fair", [co(m.one_buy(200), 20)])], 60210)
