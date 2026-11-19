# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Ordering Numbers up to 100 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_order_100.py
Comparing numbers up to 100 with blocks, place value and signs, and ordering numbers from smallest to largest and
largest to smallest (US Grade 1 and Australia Year 1 makers).
Wrong answers come from real mistakes: comparing the ones before the tens, and putting 9 after 49 because 9 is
big.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_compare as usc
adopt(usc)
if hasattr(usc, 'R'): usc.R = random.Random(701110)
import gen_au_maths_y1_numbers_120 as aun
adopt(aun)
if hasattr(aun, 'R'): aun.R = random.Random(701111)
ph_common.GRADE = "grade-1"


def one_cnt(r):
    up = r.random() < 0.5
    n = r.randint(3, 97)
    seq = [n, n + 1, n + 2] if up else [n, n - 1, n - 2]
    nxt = seq[-1] + (1 if up else -1)
    if nxt > 100 or nxt < 0:
        raise AssertionError
    return mcq("Count %s: <b>%s, ☐</b>" % ("on" if up else "back", ", ".join(map(str, seq))), nxt, [seq[-1] + (-1 if up else 1), nxt + (10 if up else -10), seq[-1]],
               "Counting %s, each number is 1 %s. <b>%d</b> comes next." % ("on" if up else "back", "more" if up else "less", nxt), allow_zero=True)


def one_ml(r):
    n = r.randint(10, 99)
    more = r.random() < 0.5
    right = n + 1 if more else n - 1
    return mcq("What is 1 %s than <b>%d</b>?" % ("more" if more else "less", n), right, [n - 1 if more else n + 1, n + 10 if more else n - 10, n],
               "1 %s than %d is <b>%d</b>." % ("more" if more else "less", n, right))


def one_skip(r):
    st = r.choice([2, 5, 10])
    a = st * r.randint(1, 100 // st - 4)
    seq = [a + st * i for i in range(4)]
    k = r.randint(1, 3)
    ans = seq[k]
    show = ", ".join("☐" if i == k else str(x) for i, x in enumerate(seq))
    return mcq("Count by %ds. What number goes in the box? <b>%s</b>" % (st, show), ans, [ans + 1, ans - 1, ans + st],
               "Each jump is %d. The missing number is <b>%d</b>." % (st, ans))


def one_ba(r):
    n = r.randint(2, 99)
    kind = r.choice(["before", "after", "between"])
    if kind == "between":
        return mcq("What number is between <b>%d</b> and <b>%d</b>?" % (n - 1, n + 1), n, [n + 1, n - 1, n + 10 if n + 10 <= 100 else n - 10],
                   "%d, <b>%d</b>, %d." % (n - 1, n, n + 1))
    right = n - 1 if kind == "before" else n + 1
    return mcq("What number comes just %s <b>%d</b>?" % (kind, n), right, [n + 1 if kind == "before" else n - 1, n, right + 10 if right + 10 <= 100 else right - 10],
               "Just %s %d comes <b>%d</b>." % (kind, n, right))


def one_chart(r):
    n = r.randint(12, 89)
    if n % 10 in (0, 1):
        raise AssertionError
    d = r.choice(["below", "above", "right", "left"])
    right = {"below": n + 10, "above": n - 10, "right": n + 1, "left": n - 1}[d]
    wr = [x for x in (n + 10, n - 10, n + 1, n - 1, n + 11) if x != right][:3]
    word = {"below": "just below", "above": "just above", "right": "just to the right of", "left": "just to the left of"}[d]
    return mcq("On a hundred chart (rows of 10), what number is %s <b>%d</b>?" % (word, n), right, wr,
               "Down 1 row is 10 more, up 1 row is 10 less, right is 1 more and left is 1 less. The answer is <b>%d</b>." % right)


def one_cmp100(r):
    a, b = r.sample(range(1, 101), 2)
    s_ = "&gt;" if a > b else "&lt;"
    return mcq("Which sign goes in the box? <b>%d ☐ %d</b>" % (a, b), s_, ["&lt;" if s_ == "&gt;" else "&gt;", "=", "+"],
               "Compare the tens first: <b>%d %s %d</b>." % (a, s_, b))


def one_ord100(r):
    vs = r.sample(range(1, 101), 4)
    if len({v // 10 for v in vs}) < 3:
        raise AssertionError
    up = r.random() < 0.5
    srt = sorted(vs, reverse=not up)
    show = lambda v: ", ".join(map(str, v))
    by_ones = sorted(vs, key=lambda v: (v % 10, v), reverse=not up)
    return mcq("Put in order from %s: <b>%s</b>" % ("smallest to largest" if up else "largest to smallest", show(vs)), show(srt),
               [show(by_ones), show(list(reversed(srt))), show([srt[1], srt[0]] + srt[2:])], "Compare the tens first, then the ones: <b>%s</b>." % show(srt))

import re as _re


def _nums(it):
    t = _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"])
    t = _re.sub(r"<[^>]+>", " ", t)
    return [int(x.replace(",", "")) for x in _re.findall(r"\d[\d,]*", t)]


def le100(it):
    return all(n <= 100 for n in _nums(it))


def le20(it):
    return all(n <= 20 for n in _nums(it))


def add20(it):
    t = _re.sub(r"<[^>]+>", " ", it["q"] + " " + it["e"])
    return le20(it) and "−" not in t and not _re.search(r"\b(ate|gave|left|lost|took|away|flew|fewer|rest|eaten|sold|broke|popped|spent)\b", t)



def build():
    sets, R = build_sets([
        ("Compare with blocks", [("run", usc.set_blocks, ("rnd", "seen"), 20, le100)]),
        ("Compare tens and ones", [("run", usc.set_places, ("rnd", "seen"), 20, le100)]),
        ("Greater than and less than", [("run", usc.set_symbols, ("rnd", "seen"), 14, le100), ("run", usc.set_words, ("rnd", "seen", usc.People), 6, le100)]),
        ("Put numbers in order", [("run", usc.set_order, ("rnd", "seen"), 6, le100), ("collect", one_ord100, 14)]),
        ("Compare and order", [("collect", one_cmp100, 10), ("collect", one_ord100, 10)]),
    ], 70111)
    finish(sets, R)
    body = lesson('<ul><li>Compare the <b>tens</b> first. The number with more tens is bigger: 52 &gt; 48.</li><li>If the tens are the same, compare the ones: 63 &gt; 61.</li><li>A 1-digit number is smaller than any 2-digit number: 9 &lt; 10.</li><li>To order, find the smallest, then the next.</li></ul>',
        [example("Order 58, 85, 49", ["tens: 5, 8, 4"], "49, 58, 85")],
        [['Ones first', 'Look at the tens first.'], ['9 is big', '9 is less than 10.'], ['Missing a number', 'Count the numbers in your answer.']])
    faq = [('What does MATATAG Math 1 ask about ordering?', 'Order numbers up to 100 from smallest to largest, and vice versa.'), ('Which is bigger, 70 or 69?', '70.'), ('How do blocks help?', 'Children can see more tens.'), ('What is the largest 2-digit number?', '99.')]
    make('ordering-numbers-to-100', 11, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Order numbers up to 100 from smallest to largest, and vice versa.',
         'Ordering Numbers up to 100', 'Ordering Numbers to 100',
         'Free Grade 1 worksheets on ordering numbers to 100 for the DepEd MATATAG curriculum: compare with blocks, tens and ones, signs and putting numbers in order. 100 questions with pictures and answers.',
         'Compare the tens first.', 'Same tens? Compare the ones.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
