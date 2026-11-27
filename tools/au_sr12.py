# -*- coding: utf-8 -*-
"""Year 12 science (Australian Curriculum: Senior Secondary Units 3 and 4): UNITS(12) for au_sr.build."""


def UNITS(year):
    out = []
    for m in ("au_sr12b", "au_sr12c", "au_sr12p", "au_sr12e"):
        try:
            mod = __import__(m)
        except ImportError:
            continue
        out += mod.UNITS()
    return out
