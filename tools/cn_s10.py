# -*- coding: utf-8 -*-
"""中国 / 高一（物理・化学・生物学・地理の必修）"""
import importlib


def UNITS(g=10):
    out = []
    for m in ("cn_s10p", "cn_s10c", "cn_s10b", "cn_s10d"):
        out += importlib.import_module(m).UNITS()
    return out
