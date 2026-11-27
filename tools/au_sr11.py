# -*- coding: utf-8 -*-
"""Year 11 science (Australian Curriculum: Senior Secondary Units 1 and 2): UNITS(11) for au_sr.build."""


def UNITS(year):
    out = []
    for m in ("au_sr11b", "au_sr11c", "au_sr11p", "au_sr11e"):
        try:
            mod = __import__(m)
        except ImportError:
            continue
        out += mod.UNITS()
    return out
