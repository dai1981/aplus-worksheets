# -*- coding: utf-8 -*-
"""Class 11 Physics, Chemistry and Biology (CBSE 2025-26 / NCERT): UNITS(11) for in_sci.build."""
import random

R = random.Random(0)
TRIM = True
G98 = True


def UNITS(level):
    out = []
    for m in ("in_s11p", "in_s11c", "in_s11b"):
        try:
            out += __import__(m).UNITS()
        except ImportError:
            pass
    return out
