# -*- coding: utf-8 -*-
"""Class 12 Physics, Chemistry and Biology (CBSE 2025-26 / NCERT): UNITS(12) for in_sci.build."""
import random

R = random.Random(0)
TRIM = True
G98 = True


def UNITS(level):
    out = []
    for m in ("in_s12p", "in_s12c", "in_s12b"):
        try:
            out += __import__(m).UNITS()
        except ImportError:
            pass
    return out
