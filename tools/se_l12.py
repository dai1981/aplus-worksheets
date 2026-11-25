# -*- coding: utf-8 -*-
"""
Sverige / Matematik / årskurs 1–2（lågstadiet, Lgr22）。
python3 tools/se_l12.py 1|2 [nummer…]   seed は 96000 + 100 × årskurs + nummer。単元の関数は se_l.UNITS（lv = 1, 2）。
"""
import random
import re
import sys
import se_m as S
import se_common as C
import se_a3a as A
import se_a3b as B
from se_m46 import group
import se_l

GRADES = {
    1: ["tal-till-20", "talraden-till-100", "jamfora-tal", "talkamrater", "addition-till-10", "subtraktion-till-10", "addition-och-subtraktion-till-20",
        "problemlosning", "dubbelt-och-halften", "monster", "pengar", "klockan", "langd-och-vikt", "geometriska-figurer", "lagesord", "tabeller-och-diagram"],
    2: ["tal-till-100", "tiotal-och-ental", "jamfora-och-ordna-tal", "udda-och-jamna-tal", "huvudrakning", "addition-och-subtraktion-till-100", "problemlosning",
        "multiplikation", "delning", "halvor-och-fjardedelar", "monster", "pengar", "klockan", "langd", "geometriska-figurer-och-kroppar", "symmetri",
        "lagesord-och-programmering", "tabeller-och-diagram", "slump-och-chans"],
}


def build(lv, i):
    slug = GRADES[lv][i - 1]
    rnd = random.Random(96000 + 100 * lv + i)
    S.setup(rnd)
    A.setup(rnd)
    B.setup(rnd)
    dd = se_l.UNITS[slug](lv)
    assert dd["slug"] == slug, (dd["slug"], slug)
    seen = set()
    sets = []
    for t, parts in dd["sets"]:
        try:
            items = C.mix(rnd, seen, parts)
            for it in items:
                it["q"] = group(it["q"])
                it["e"] = group(it["e"])
                it["c"] = [group(c) for c in it["c"]]
            sets.append((t, items))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (slug, t, [m.__name__ for m, _ in parts], e))
    body = C.lesson(dd["think"], [C.example(q, s, a) for q, s, a in dd["ex"]], dd["mist"])
    faq = [{"q": q, "a": a} for q, a in dd["faq"]]
    C.make_unit(rnd, slug, dd["dom"], dd["std"], dd["title"], dd["short"], dd["meta"], dd["kb"], dd["ks"], body, faq, sets, i, "arskurs-%d" % lv)
    return slug


if __name__ == "__main__":
    lv = int(sys.argv[1])
    want = sys.argv[2:]
    for i in range(1, len(GRADES[lv]) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(lv, i), flush=True)
