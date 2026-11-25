# -*- coding: utf-8 -*-
"""
Sverige / Matematik / årskurs 4–6（Lgr22）。
python3 tools/se_m46.py 4|5|6 [nummer…]   seed は 95000 + 100 × årskurs + nummer。
単元の関数は se_m_a（tal och räkning）・se_m_b（bråk, procent, algebra）・se_m_c（mätning, geometri）・se_m_d（statistik, problemlösning）の UNITS。
同じ slug の単元は lv（årskurs）で範囲と問題が変わる。
"""
import random
import re
import sys
import se_m as S
import se_common as C
import se_m_a, se_m_b, se_m_c, se_m_d

ALL = {}
for m in (se_m_a, se_m_b, se_m_c, se_m_d):
    ALL.update(m.UNITS)

GRADES = {
    4: ["tal-och-positionssystemet", "avrundning-och-overslag", "addition-och-subtraktion", "multiplikation", "division", "problemlosning",
        "brak", "decimaltal", "ekvationer-och-uttryck", "monster-och-talfoljder", "langd-massa-och-volym", "tid", "omkrets-och-area",
        "vinklar", "geometriska-figurer-och-kroppar", "symmetri", "koordinatsystem", "tabeller-och-diagram", "sannolikhet"],
    5: ["tal-och-positionssystemet", "avrundning-och-overslag", "addition-och-subtraktion", "multiplikation", "division", "prioriteringsregler",
        "negativa-tal", "problemlosning", "brak", "decimaltal", "procent", "ekvationer-och-uttryck", "monster-och-talfoljder", "proportionalitet",
        "langd-massa-och-volym", "tid", "omkrets-och-area", "vinklar", "geometriska-figurer-och-kroppar", "symmetri", "koordinatsystem",
        "tabeller-och-diagram", "medelvarde-typvarde-och-median", "sannolikhet", "kombinatorik"],
    6: ["tal-och-positionssystemet", "avrundning-och-overslag", "addition-och-subtraktion", "multiplikation", "division", "prioriteringsregler",
        "negativa-tal", "problemlosning", "brak", "decimaltal", "procent", "ekvationer-och-uttryck", "monster-och-talfoljder", "proportionalitet",
        "langd-massa-och-volym", "omkrets-och-area", "vinklar", "geometriska-figurer-och-kroppar", "skala", "koordinatsystem",
        "tabeller-och-diagram", "medelvarde-typvarde-och-median", "sannolikhet", "kombinatorik"],
}


_TAG = re.compile(r"(<svg.*?</svg>|<[^>]+>)", re.S)
_BIG = re.compile(r"(?<![\d,\u00a0])(\d{4,})(?![\d,])")


def group(t, years=()):
    """1440 → 1 440 i texten (inte i SVG, taggar eller årtal efter 'år ')"""
    out = []
    for part in _TAG.split(t):
        if part.startswith("<"):
            out.append(part)
            continue
        out.append(_BIG.sub(lambda m: m.group(1) if re.search(r"år\s$", part[:m.start()]) or m.group(1) in years else C.num(int(m.group(1))), part))
    return "".join(out)


def build(lv, i):
    slug = GRADES[lv][i - 1]
    rnd = random.Random(95000 + 100 * lv + i)
    S.setup(rnd)
    dd = ALL[slug](lv)
    assert dd["slug"] == slug
    seen = set()
    sets = []
    for t, parts in dd["sets"]:
        try:
            items = C.mix(rnd, seen, parts)
            for it in items:
                it["q"] = re.sub(r"<div class='qfig'><div class='qfig'>(.*?)</div></div>", r"<div class='qfig'>\1</div>", it["q"], flags=re.S)
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
        print(i, build(lv, i), flush=True)
