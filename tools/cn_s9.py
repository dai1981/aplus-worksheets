# -*- coding: utf-8 -*-
"""中国 / 九年级：物理・化学"""
import cn_s9p
try:
    import cn_s9c
except ImportError:
    cn_s9c = None


def UNITS(g):
    return cn_s9p.UNITS() + (cn_s9c.UNITS() if cn_s9c else [])
