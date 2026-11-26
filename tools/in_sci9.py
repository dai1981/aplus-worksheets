# -*- coding: utf-8 -*-
"""Class 9 Science (CBSE 2025-26 / NCERT): UNITS(9) for in_sci.build."""
import random
import in_sci9a

R = random.Random(0)
TRIM = True


def UNITS(level):
    out = in_sci9a.UNITS9a()
    for m in ("in_sci9b", "in_sci9c"):
        try:
            out += __import__(m).__dict__["UNITS" + m[-2:]]()
        except ImportError:
            pass
    return out
