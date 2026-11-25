# -*- coding: utf-8 -*-
"""
Sverige / Matematik / årskurs 3（Lgr22）。
python3 tools/se_a3.py [nummer…]   seed は 95300 + nummer。単元は se_a3a（1〜12）・se_a3b（13〜23）の UNITS。
"""
import random
import sys
import se_a3a as A
import se_common as C


def units():
    import se_a3b as B
    return A.UNITS + B.UNITS


def build(i, grade="arskurs-3"):
    import se_a3b as B
    rnd = random.Random(95300 + i)
    A.setup(rnd)
    B.setup(rnd)
    d = units()[i - 1]()
    seen = set()
    sets = []
    for t, parts in d["sets"]:
        try:
            sets.append((t, C.mix(rnd, seen, parts)))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (d["slug"], t, [getattr(m, "__name__", "?") for m, _ in parts], e))
    body = C.lesson(d["think"], [C.example(q, s, a) for q, s, a in d["ex"]], d["mist"])
    faq = [{"q": q, "a": a} for q, a in d["faq"]]
    C.make_unit(rnd, d["slug"], d["dom"], d["std"], d["title"], d["short"], d["meta"], d["kb"], d["ks"], body, faq, sets, d["sort"], grade)
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(units()) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
