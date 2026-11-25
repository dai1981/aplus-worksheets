# -*- coding: utf-8 -*-
"""
Sverige / Matematik / gymnasiet（Gy25 Matematik nivå 1c, 2c, 3c, 4, 5）。
python3 tools/se_gy.py 1c|2c|3c|4|5 [nummer…]   seed は 98000 + 1000 × kursens plats + nummer。単元は se_g1〜se_g5 の UNITS（引数なし）。
"""
import importlib
import random
import re
import sys
import se_m as S
import se_common as C
from se_m46 import group

COURSES = {
    "1c": ("se_g1", ["potenser-och-rotter", "algebra-och-faktorisering", "ekvationer-och-formler", "funktioner", "linjara-funktioner", "linjara-olikheter",
                     "exponentialfunktioner", "potensekvationer", "forandringsfaktor", "trigonometri", "vektorer", "sannolikhet", "statistik-och-kallkritik", "ranta-och-amortering"]),
    "2c": ("se_g2", ["ekvationssystem", "kvadreringsreglerna-och-konjugatregeln", "andragradsekvationer", "andragradsfunktioner", "logaritmer", "exponentialekvationer",
                     "rotekvationer", "standardavvikelse-och-percentiler", "normalfordelning", "regression-och-korrelation", "logik-och-bevis", "geometriska-satser"]),
    "3c": ("se_g3", ["absolutbelopp-och-rationella-uttryck", "polynom", "gransvarden", "derivatans-definition", "deriveringsregler", "tangenter",
                     "talet-e-och-ln", "extrempunkter-och-andraderivata", "optimering", "primitiva-funktioner", "integraler", "triangelsatser"]),
    "4": ("se_g4", ["komplexa-tal-i-rektangular-form", "komplexa-tal-i-polar-form", "polynomekvationer-och-faktorsatsen", "enhetscirkeln-och-radianer", "trigonometriska-formler",
                   "trigonometriska-ekvationer", "trigonometriska-grafer", "kedjeregeln", "produkt-och-kvotregeln", "grafer-och-asymptoter", "integraler-och-volymer"]),
    "5": ("se_g5", ["differentialekvationer-av-forsta-ordningen", "differentialekvationer-av-andra-ordningen", "tillampningar-av-differentialekvationer", "mangdlara", "kombinatorik",
                   "talteori-och-kongruensrakning", "talbaser", "rekursiva-talfoljder", "bevismetoder-och-induktion", "grafer-och-natverk"]),
}
ORDER = ["1c", "2c", "3c", "4", "5"]


def build(k, i):
    mod, slugs = COURSES[k]
    m = importlib.import_module(mod)
    slug = slugs[i - 1]
    rnd = random.Random(98000 + 1000 * ORDER.index(k) + i)
    S.setup(rnd)
    dd = m.UNITS[slug]()
    assert dd["slug"] == slug, (dd["slug"], slug)
    seen = set()
    sets = []
    for t, parts in dd["sets"]:
        try:
            items = C.mix(rnd, seen, parts)
            for it in items:
                it["q"] = re.sub(r"<div class='qfig'><div class='qfig'>(.*?)</div></div>", r"<div class='qfig'>\1</div>", it["q"], flags=re.S)
                yrs = set(re.findall(r"år (\d{4})\b", it["q"]))
                if slug == "talbaser":
                    alltxt = " ".join([it["q"]] + it["c"] + [it["e"]])
                    yrs |= set(re.findall(r"(?<![\d,])([01]{4,})(?![\d,])", alltxt)) | set(re.findall(r"(\d{4,})<sub>", alltxt))
                it["q"] = group(it["q"], yrs)
                it["e"] = group(it["e"], yrs)
                it["c"] = [group(c, yrs) for c in it["c"]]
            sets.append((t, items))
        except AssertionError as e:
            raise AssertionError("%s / %s / %s: %s" % (slug, t, [mk.__name__ for mk, _ in parts], e))
    body = C.lesson(dd["think"], [C.example(q, s, a) for q, s, a in dd["ex"]], dd["mist"])
    faq = [{"q": q, "a": a} for q, a in dd["faq"]]
    C.make_unit(rnd, slug, dd["dom"], dd["std"], dd["title"], dd["short"], dd["meta"], dd["kb"], dd["ks"], body, faq, sets, i, "matematik-" + k)
    return slug


if __name__ == "__main__":
    k = sys.argv[1]
    want = sys.argv[2:]
    for i in range(1, len(COURSES[k][1]) + 1):
        if want and str(i) not in want:
            continue
        print(i, build(k, i), flush=True)
