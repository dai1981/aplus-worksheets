# -*- coding: utf-8 -*-
"""
Türkiye / Matematik / 4.〜6. sınıf（Türkiye Yüzyılı Maarif Modeli）。
python3 tools/tr_run.py 4 [番号…]   seed は 90000 + 100 × 学年 + 番号。単元は tr_sNa・tr_sNb・tr_sNc の UNITS。
（3. sınıf は tr_s3.py）
"""
import importlib
import random
import sys
import tr_s3a as A
import tr_g
import tr_common as C

SUFFIX = {1: " (Türkiye Yüzyılı Maarif Modeli, İlkokul Matematik Dersi Öğretim Programı)", 2: " (Türkiye Yüzyılı Maarif Modeli, İlkokul Matematik Dersi Öğretim Programı)", 4: " (Türkiye Yüzyılı Maarif Modeli, İlkokul Matematik Dersi Öğretim Programı)"}
SUFFIX[0] = " (Türkiye Yüzyılı Maarif Modeli, Okul Öncesi Eğitim Programı, 60–72 ay)"
for g in range(9, 13):
    SUFFIX[g] = " (Türkiye Yüzyılı Maarif Modeli, Ortaöğretim Matematik Dersi Öğretim Programı)"
for g in range(5, 9):
    SUFFIX[g] = " (Türkiye Yüzyılı Maarif Modeli, Ortaokul Matematik Dersi Öğretim Programı)"


def mods(g):
    out = []
    for k in "abc":
        try:
            out.append(importlib.import_module("tr_s%d%s" % (g, k)))
        except ImportError:
            pass
    return out


def units(g):
    us = []
    for m in mods(g):
        us += m.UNITS
    return us


def build(g, i):
    rnd = random.Random(90000 + 100 * g + i)
    A.setup(rnd)
    tr_g.setup(rnd)
    for m in mods(g):
        m.setup(rnd)
    d = units(g)[i - 1]()
    seen = set()
    sets = []
    def safe(f):
        def g():
            try:
                return f()
            except (AssertionError, ZeroDivisionError, ValueError, TypeError, KeyError, IndexError):
                return None
        g.__name__ = f.__name__
        return g

    for t, parts in d["sets"]:
        parts = [(safe(m), n) for m, n in parts]
        try:
            sets.append((t, C.mix(rnd, seen, parts)))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (d["slug"], t, [m.__name__ for m, _ in parts], e))
    body = C.lesson(d["think"], [C.example(q, s, a) for q, s, a in d["ex"]], d["mist"])
    faq = [{"q": q, "a": a} for q, a in d["faq"]]
    C.make_unit(rnd, d["slug"], d["dom"], d["code"], d["std"] + SUFFIX[g], d["title"], d["short"], d["meta"], d["kb"], d["ks"],
                body, faq, sets, d["sort"], grade="okul-oncesi" if g == 0 else "%d-sinif" % g)
    return d["slug"]


if __name__ == "__main__":
    g = int(sys.argv[1])
    want = sys.argv[2:]
    for i in range(1, len(units(g)) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(g, i), flush=True)
