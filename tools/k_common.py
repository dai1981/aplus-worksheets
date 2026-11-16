# -*- coding: utf-8 -*-
"""Shared question helpers for the US Kindergarten generators (gen_us_math_gk_*.py)."""
import re
from ws_common import balance

PEOPLE = [("Maya", "she", "her"), ("Leo", "he", "his"), ("Ava", "she", "her"), ("Sam", "he", "his"),
          ("Mia", "she", "her"), ("Ben", "he", "his"), ("Zoe", "she", "her"), ("Kai", "he", "his"),
          ("Lily", "she", "her"), ("Omar", "he", "his"), ("Nora", "she", "her"), ("Eli", "he", "his"),
          ("Ruby", "she", "her"), ("Jack", "he", "his"), ("Hana", "she", "her"), ("Luis", "he", "his")]


class Kids:
    def __init__(self, rnd):
        self.pool = PEOPLE[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=p[0], he=p[1], He=p[1].capitalize(), his=p[2], His=p[2].capitalize())

    def two(self):
        a = self.next()
        b = self.next()
        while b["n"] == a["n"]:
            b = self.next()
        return a, b


def mcq(q, correct, cands, e, allow_zero=False):
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or (c == "0" and not allow_zero):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    assert len(pick) == 3, (q[-120:], correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def lst(a, b):
    return ", ".join(str(i) for i in range(a, b + 1))


def finish(sets, rnd, max_num=20, extra_ok=()):
    """Balance answer positions, check for repeats and odd numbers, and print pictures large."""
    balance(sets, rnd)
    seen = set()
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        for it in s["items"]:
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][-100:]
            seen.add(key)
            for c in it["c"]:
                for tok in re.findall(r"\d+", c):
                    assert int(tok) <= max_num or int(tok) in extra_ok, (c, it["q"][-80:])
            it["q"] = it["q"].replace("<svg ", "<svg data-pf='lg' ")
    return sets
