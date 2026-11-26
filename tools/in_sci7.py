# -*- coding: utf-8 -*-
"""Class 7 Science (NCERT Curiosity): UNITS(7) for in_sci.build."""
import random
import in_sci7a
import in_sci7b

R = random.Random(0)
TRIM = True
BOOK = "Curiosity"
STD_URL = "https://ncert.nic.in/textbook.php?gecu1=0-12"


def UNITS(level):
    return in_sci7a.UNITS7a() + in_sci7b.UNITS7b()
