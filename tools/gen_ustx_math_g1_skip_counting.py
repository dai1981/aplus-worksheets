# -*- coding: utf-8 -*-
"""
Texas Grade 1 Math: Skip Counting by 2s, 5s and 10s (TEKS 1.5B)
  python3 tools/gen_ustx_math_g1_skip_counting.py
Counting pairs by 2s, hands by 5s, bundles by 10s, patterns and missing numbers, and counting collections in groups
(the Australian Year 1 makers with Texas names; coin items are left out).
Wrong answers come from real mistakes: counting each group as 1, counting by the wrong number, and stopping one
group early.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_au_maths_y1_skip_counting as sk
adopt(sk)
tx_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f

import random as _random


def abcd(mod, fn, seed):
    """Build A-D picture items (_abcd) now, with the right picture at a random position."""
    rr = _random.Random(seed)
    def f(*a):
        st = fn(*a)
        for it in (st["items"] if isinstance(st, dict) else st):
            if "_abcd" in it:
                parts = it.pop("_abcd")
                prompt, right, wrong = parts[0], parts[1], list(parts[2])
                t = rr.randrange(4)
                rr.shuffle(wrong)
                it["q"] = mod.fig(mod.abcd_svg(wrong[:t] + [right] + wrong[t:], *parts[3:])) + prompt
                it["a"] = t
                it["e"] = it["e"].replace("{L}", "ABCD"[t])
        return st
    f.__name__ = fn.__name__
    return f


set_stories = abcd(sk, sk.set_stories, 691101)


def skip(step):
    def f(r):
        start = step * r.randint(1, 110 // step)
        seq = [start + step * i for i in range(4)]
        nxt = seq[-1] + step
        if nxt > 120:
            raise AssertionError
        w = [seq[-1] + 1, seq[-1] + 2 * step, seq[-1] + (5 if step != 5 else 2)]
        return mcq("Count by %ds: %s, ☐. What comes next?" % (step, ", ".join(map(str, seq))), str(nxt), [str(x) for x in w],
                   "Add %d each time: %d + %d = <b>%d</b>." % (step, seq[-1], step, nxt))
    f.__name__ = "skip%d" % step
    return f


one_by5 = skip(5)
one_by10 = skip(10)


def no_coin(it):
    t = it["q"] + " ".join(it["c"]) + it["e"]
    return "coin" not in t and "c " not in t


def build():
    sets, R = build_sets([
        ("Count pairs by 2s", [("run", sk.set_twos, (sk.People,), 20, no_coin)]),
        ("Count hands by 5s", [("run", sk.set_fives, (sk.People,), 15, no_coin), ("collect", uniq(one_by5), 5)]),
        ("Count bundles by 10s", [("run", sk.set_tens, (sk.People,), 15, no_coin), ("collect", uniq(one_by10), 5)]),
        ("Continue the pattern", [("run", sk.set_patterns, (sk.People,), 20, no_coin)]),
        ("Count a collection in groups", [("run", set_stories, (sk.People,), 20, no_coin)]),
    ], 69110)
    finish(sets, R)
    body = lesson('<ul><li>Skip counting is a fast way to count groups.</li><li>By 2s: 2, 4, 6, 8, 10.</li><li>By 5s: 5, 10, 15, 20, 25.</li><li>By 10s: 10, 20, 30, 40, 50.</li><li>Say one number for each group.</li></ul>',
        [example("4 hands", ["5, 10, 15, 20"], "20 fingers")],
        [['Counting each group as 1', 'Each hand is 5, not 1.'], ['Counting by the wrong number', 'Pairs go by 2s, hands by 5s.'], ['Stopping one group early', 'Touch each group as you count.']])
    faq = [('What does TEKS 1.5B ask?', 'Skip count by twos, fives, and tens to determine the total number of objects up to 120 in a set.'), ('Why skip count?', 'It is faster than counting by 1s.'), ('What comes after 35 when counting by 5s?', '40.'), ('What comes after 70 when counting by 10s?', '80.')]
    make('skip-counting-by-2s-5s-and-10s', 10, 'Algebraic Reasoning', '1.5B',
         '1.5B skip count by twos, fives, and tens to determine the total number of objects up to 120 in a set',
         'Skip Counting by 2s, 5s and 10s', 'Skip Counting',
         'Free Grade 1 skip counting worksheets for Texas TEKS 1.5B: count by 2s, 5s and 10s with pictures, patterns and stories. 100 questions with answers.',
         'Say one number for each group.', '2, 4, 6 · 5, 10, 15 · 10, 20, 30',
         body, faq, sets, seo_title='Grade 1 Skip Counting by 2s, 5s and 10s Worksheets (TEKS 1.5B)')


if __name__ == "__main__":
    build()
