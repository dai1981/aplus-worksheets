# -*- coding: utf-8 -*-
"""
Türkiye / Matematik / 3. sınıf（Türkiye Yüzyılı Maarif Modeli 2024）。
python3 tools/tr_s3.py [番号…]   seed は 90300 + 番号。単元は tr_s3a（1〜10）・tr_s3b（11〜22）の UNITS。
"""
import random
import sys
import tr_s3a as A
import tr_common as C


def units():
    import tr_s3b as B
    return A.UNITS + B.UNITS


def build(i):
    import tr_s3b as B
    rnd = random.Random(90300 + i)
    A.setup(rnd)
    B.setup(rnd)
    d = units()[i - 1]()
    seen = set()
    sets = []
    for t, parts in d["sets"]:
        try:
            sets.append((t, C.mix(rnd, seen, parts)))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (d["slug"], t, [m.__name__ for m, _ in parts], e))
    body = C.lesson(d["think"], [C.example(q, s, a) for q, s, a in d["ex"]], d["mist"])
    faq = [{"q": q, "a": a} for q, a in d["faq"]]
    C.make_unit(rnd, d["slug"], d["dom"], d["code"], d["std"] + " (Türkiye Yüzyılı Maarif Modeli, İlkokul Matematik Dersi Öğretim Programı)",
                d["title"], d["short"], d["meta"], d["kb"], d["ks"], body, faq, sets, d["sort"])
    return d["slug"]


if __name__ == "__main__":
    want = sys.argv[1:]
    for i in range(1, len(units()) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(i), flush=True)
