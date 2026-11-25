# -*- coding: utf-8 -*-
"""
Schweiz / Mathematik（Lehrplan 21, Deutschschweiz）: python3 tools/ch_run.py 3 [Nummer …]
Einheiten in ch_k{Klasse}.UNITS: (slug, Sortierung, LP21-Codes, Kompetenzbereich, Quelle)
Quelle = Name eines gen_de_mathe_*-Skripts (wird mit seed 130000 + 1000 × Klasse + Nummer neu erzeugt) oder eine Funktion.
"""
import importlib
import sys
import ch_common as C

if __name__ == "__main__":
    k = int(sys.argv[1])
    want = sys.argv[2:]
    m = importlib.import_module("ch_k%d" % k)
    grade = "kindergarten" if k == 0 else ("gymnasium-%d" % (k - 9) if k >= 10 else "klasse-%d" % k)
    C.KEEP_DOT = k >= 10
    for i, (slug, sort, codes, dom, src) in enumerate(m.UNITS, 1):
        if want and str(i) not in want:
            continue
        seed = 130000 + 1000 * k + i
        C.EXTRA[:] = list(getattr(m, "EXTRA", [])) + list(getattr(m, "LIMIT", {}).get(slug, []))
        if isinstance(src, str):
            C.from_de(src, seed, slug, grade, sort, codes, dom, fix=getattr(m, "FIX", {}).get(slug), pre=getattr(m, "PRE", {}).get(slug))
        else:
            src(seed, slug, grade, sort, codes, dom)
        print(i, slug, flush=True)
