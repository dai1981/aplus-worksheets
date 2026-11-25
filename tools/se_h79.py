# -*- coding: utf-8 -*-
"""
Sverige / Matematik / årskurs 7–9（högstadiet, Lgr22）。
python3 tools/se_h79.py 7|8|9 [nummer…]   seed は 97000 + 100 × årskurs + nummer。
単元の関数は se_h_a（tal）・se_h_b（algebra）・se_h_c（samband och förändring）・se_h_d（geometri）・se_h_e（statistik, sannolikhet, problemlösning）の UNITS。
"""
import random
import re
import sys
import se_m as S
import se_common as C
from se_m46 import group
import se_h_a, se_h_b, se_h_c, se_h_d, se_h_e

ALL = {}
for m in (se_h_a, se_h_b, se_h_c, se_h_d, se_h_e):
    ALL.update(m.UNITS)

GRADES = {
    7: ["negativa-tal", "prioriteringsregler", "delbarhet-och-primtal", "brak", "decimaltal", "potenser-och-kvadratrotter", "procent",
        "algebraiska-uttryck", "ekvationer", "monster-och-formler", "proportionalitet", "vinklar", "omkrets-och-area", "cirkeln",
        "enheter", "lagesmatt", "sannolikhet", "problemlosning"],
    8: ["potenser", "grundpotensform-och-prefix", "parenteser-och-faktorisering", "ekvationer", "formler", "olikheter",
        "procent-och-forandringsfaktor", "funktioner-och-grafer", "proportionalitet", "skala", "vinklar-och-polygoner",
        "prisma-och-cylinder", "begransningsarea", "tabeller-och-diagram", "kombinatorik", "sannolikhet", "problemlosning"],
    9: ["reella-tal", "kvadreringsreglerna", "ekvationssystem", "ekvationer-med-x2", "linjara-funktioner", "rata-linjens-ekvation",
        "tolka-grafer", "ranta-och-lan", "exponentiell-forandring", "pythagoras-sats", "likformighet", "pyramid-kon-och-klot",
        "cirkelsektorer", "spridningsmatt", "sannolikhet", "problemlosning"],
}


def build(lv, i):
    slug = GRADES[lv][i - 1]
    rnd = random.Random(97000 + 100 * lv + i)
    S.setup(rnd)
    dd = ALL[slug](lv)
    assert dd["slug"] == slug, (dd["slug"], slug)
    seen = set()
    sets = []
    for t, parts in dd["sets"]:
        try:
            items = C.mix(rnd, seen, parts)
            for it in items:
                yrs = set(re.findall(r"år (\d{4})\b", it["q"]))
                it["q"] = group(it["q"], yrs)
                it["e"] = group(it["e"], yrs)
                it["c"] = [group(c, yrs) for c in it["c"]]
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
        if GRADES[lv][i - 1] not in ALL:
            print(i, "MISSING", GRADES[lv][i - 1])
            continue
        print(i, build(lv, i), flush=True)
