# -*- coding: utf-8 -*-
"""中国 / 高二（物理・化学・生物学・地理）"""
import importlib


def UNITS(g=11):
    out = []
    for m in ("cn_s11p", "cn_s11c", "cn_s11b", "cn_s11d"):
        out += importlib.import_module(m).UNITS()
    return out
