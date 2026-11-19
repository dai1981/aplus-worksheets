# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Reading, Writing and Showing Numbers up to 100 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_read_write_numbers.py
Number words and numerals up to 100 (own makers and US Grade 1 maker), and showing numbers with tens and ones blocks
(Australia Year 1 makers).
Wrong answers come from real mistakes: writing the digits the wrong way round (14 and 41), mixing up teen and ty
words, and counting the ones blocks as tens.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_count_120 as usc
adopt(usc)
if hasattr(usc, 'R'): usc.R = random.Random(701040)
import gen_au_maths_y1_tens_ones as aut
adopt(aut)
if hasattr(aut, 'R'): aut.R = random.Random(701041)
ph_common.GRADE = "grade-1"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


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


def one_w2n(r):
    n = r.randint(11, 100)
    w = words(n)
    t, o = divmod(n, 10)
    wr = [n + 10 if n + 10 <= 100 else n - 10, o * 10 + t if o and o * 10 + t != n else n + 1, n - 1]
    return mcq("Write the number: <b>%s</b>" % w, n, wr, "%s is <b>%d</b>." % (w.capitalize(), n))


def one_n2w(r):
    n = r.randint(11, 99)
    t, o = divmod(n, 10)
    if o == 0 or t == o:
        raise AssertionError
    w = words(n)
    wr = [words(o * 10 + t), words(n + 10) if n + 10 < 100 else words(n - 10), words(n + 1)]
    return mcq("Which words name <b>%d</b>?" % n, w, wr, "%d is %d tens and %d ones: <b>%s</b>." % (n, t, o, w))


def build():
    sets, R = build_sets([
        ("Words to numbers", [("collect", uniq(one_w2n), 20)]),
        ("Numbers to words", [("collect", uniq(one_n2w), 20)]),
        ("Digits in a number", [("run", aut.set_digits, ("rnd", "seen"), 20, le100)]),
        ("Show numbers with blocks", [("run", aut.set_count, ("rnd", "seen"), 20, le100)]),
        ("Tens and ones parts", [("run", aut.set_partition, ("rnd", "seen"), 20, le100)]),
    ], 70104)
    finish(sets, R)
    body = lesson('<ul><li>Read a number from left to right: 47 is forty-seven.</li><li>The teens end in “teen”: thirteen, fourteen. The tens end in “ty”: thirty, forty.</li><li>Blocks show numbers: a long block is 1 ten, a small cube is 1 one.</li><li>4 tens and 7 ones make 47.</li></ul>',
        [example("sixty-two", ["6 tens, 2 ones"], "62")],
        [['14 or 41?', 'Fourteen is 1 ten and 4 ones: 14.'], ['Teen or ty?', 'Sixteen is 16; sixty is 60.'], ['Ones as tens', 'Long blocks are tens; cubes are ones.']])
    faq = [('What does MATATAG Math 1 ask about numbers?', 'Read and write numerals up to 100, and recognize and represent numbers up to 100 using a variety of concrete and pictorial models.'), ('How do you write 100 in words?', 'One hundred.'), ('Why use blocks?', 'Children see tens and ones.'), ('Is a hyphen needed in forty-seven?', 'Yes, for numbers from 21 to 99 that are not tens.')]
    make('reading-and-writing-numbers-to-100', 4, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Read and write numerals up to 100; recognize and represent numbers up to 100 using a variety of concrete and pictorial models.',
         'Reading, Writing and Showing Numbers up to 100', 'Reading and Writing Numbers',
         'Free Grade 1 worksheets on reading and writing numbers to 100 for the DepEd MATATAG curriculum: number words, numerals and tens and ones blocks. 100 questions with pictures and answers.',
         'Tens first, then ones: 47 is forty-seven.', 'A long block is 1 ten. A cube is 1 one.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
