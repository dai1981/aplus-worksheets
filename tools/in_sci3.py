# -*- coding: utf-8 -*-
"""Class 3 EVS — The World Around Us (NCERT Our Wondrous World): UNITS(3) for in_sci.build."""
import random
import in_sci3a

R = random.Random(0)
TRIM = True
BOOK = "Our Wondrous World"
SUBJ = "EVS"
STD_URL = "https://ncert.nic.in/textbook.php"


def UNITS(level):
    out = in_sci3a.UNITS3a()
    try:
        import in_sci3b
        out += in_sci3b.UNITS3b()
    except ImportError:
        pass
    return out
