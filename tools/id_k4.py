# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / Kelas 4 (Fase B, Kurikulum Merdeka CP 2025)。17 単元。
python3 tools/id_k4.py [slug…]
seed は 40400 + sort（id_k4a・id_k4b・id_k4c の問題関数）
"""
import random
import sys
import id_k4a as A
import id_k4b as B
import id_k4c as C
from id_common import mix, make_unit

UNITS = [A.u1, A.u2, A.u3, A.u4, A.u5, A.u6, A.u7, B.u8, B.u9, B.u10, B.u11, B.u12, B.u13, B.u14, C.u15, C.u16, C.u17]


def build(fn):
    i = UNITS.index(fn) + 1
    rnd = random.Random(40400 + i)
    A.setup(rnd)
    d = fn()
    seen = set()
    sets = [(t, mix(rnd, seen, parts)) for t, parts in d["sets"]]
    make_unit(rnd, d["slug"], d["dom"], d["std_text"], d["title"], d["short_title"], d["meta_desc"],
              d["key_big"], d["key_sub"], d["body"], d["faq"], sets, d["sort"])
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for fn in UNITS:
        if want and not any(w in fn.__name__ or w == str(UNITS.index(fn) + 1) for w in want):
            continue
        print(build(fn))
