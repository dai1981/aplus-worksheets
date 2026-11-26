# -*- coding: utf-8 -*-
"""Class 4 EVS — The World Around Us (NCERT Our Wondrous World): UNITS(4) for in_sci.build."""
import random
import in_sci4a
import in_sci4b

R = random.Random(0)
TRIM = True
NOCOMMA = {"1098"}
BOOK = "Our Wondrous World"
SUBJ = "EVS"
STD_URL = "https://ncert.nic.in/textbook.php"


def UNITS(level):
    return in_sci4a.UNITS4a() + in_sci4b.UNITS4b()
