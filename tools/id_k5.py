# -*- coding: utf-8 -*-
"""
Indonesia / Matematika / Kelas 5 (Fase C, Kurikulum Merdeka CP 2025)。20 単元。
python3 tools/id_k5.py [番号…]
seed は 40500 + sort（id_k5a・id_k5b の問題関数）
"""
import random
import sys
import id_k4a as A
import id_k5a as P
import id_k5b as Q
from id_common import mix, make_unit

UNITS = [P.u1, P.u2, P.u3, P.u4, P.u5, P.u6, P.u7, P.u8, P.u9, P.u10,
         Q.u11, Q.u12, Q.u13, Q.u14, Q.u15, Q.u16, Q.u17, Q.u18, Q.u19, Q.u20]


def build(fn):
    i = UNITS.index(fn) + 1
    rnd = random.Random(40500 + i)
    A.setup(rnd)
    d = fn()
    seen = set()
    sets = [(t, mix(rnd, seen, parts)) for t, parts in d["sets"]]
    make_unit(rnd, d["slug"], d["dom"], d["std_text"], d["title"], d["short_title"], d["meta_desc"],
              d["key_big"], d["key_sub"], d["body"], d["faq"], sets, d["sort"], grade="kelas-5", fase="Fase C")
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for fn in UNITS:
        n = str(UNITS.index(fn) + 1)
        if want and n not in want:
            continue
        print(n, build(fn), flush=True)
