# -*- coding: utf-8 -*-
"""Class 6 Science (NCERT Curiosity): UNITS(6) for in_sci.build."""
import random
import in_sci6a
import in_sci6b

R = random.Random(0)
TRIM = True
BOOK = "Curiosity"
STD_URL = "https://ncert.nic.in/textbook.php?fecu1=0-12"


def UNITS(level):
    return in_sci6a.UNITS6a() + in_sci6b.UNITS6b()
