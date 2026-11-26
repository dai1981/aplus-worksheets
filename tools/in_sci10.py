# -*- coding: utf-8 -*-
"""Class 10 Science (CBSE 2025-26 / NCERT): UNITS(10) for in_sci.build."""
import random
import in_sci10a

R = random.Random(0)


def UNITS(level):
    out = in_sci10a.UNITS10a()
    try:
        import in_sci10b
        out += in_sci10b.UNITS10b()
    except ImportError:
        pass
    try:
        import in_sci10c
        out += in_sci10c.UNITS10c()
    except ImportError:
        pass
    return out
