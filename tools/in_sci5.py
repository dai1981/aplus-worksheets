# -*- coding: utf-8 -*-
"""Class 5 EVS — The World Around Us (NCERT Our Wondrous World): UNITS(5) for in_sci.build."""
import random
import in_sci5a
import in_sci5b

R = random.Random(0)
TRIM = True
NOCOMMA = {"1098"}
BOOK = "Our Wondrous World"
SUBJ = "EVS"
STD_URL = "https://ncert.nic.in/textbook.php"


def UNITS(level):
    return in_sci5a.UNITS5a() + in_sci5b.UNITS5b()
