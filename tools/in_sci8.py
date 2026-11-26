# -*- coding: utf-8 -*-
"""Class 8 Science (NCERT Curiosity): UNITS(8) for in_sci.build."""
import random
import in_sci8a
import in_sci8b

R = random.Random(0)
TRIM = True
BOOK = "Curiosity"
STD_URL = "https://ncert.nic.in/textbook.php?hecu1=0-13"


def UNITS(level):
    return in_sci8a.UNITS8a() + in_sci8b.UNITS8b()
