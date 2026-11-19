# -*- coding: utf-8 -*-
"""
Philippines Grade 1 Math (MATATAG): Addition Word Problems with Sums up to 20 (Grade 1: Number and Algebra)
  python3 tools/gen_ph_math_g1_addition_problems_20.py
Joining problems, putting parts together, unknown parts and number sentences for stories (US Grade 1 and
Ontario Grade 1 makers with Filipino names).
Wrong answers come from real mistakes: answering with a number from the story, subtracting when the story joins,
and writing the number sentence in the wrong order.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g1_word_problems as usw
adopt(usw)
if hasattr(usw, 'R'): usw.R = random.Random(701090)
import gen_caon_math_g1_word_problems as caw
adopt(caw)
if hasattr(caw, 'R'): caw.R = random.Random(701091)
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
        ("Join stories", [("run", usw.set_result, ("rnd", usw.People, lambda r: usw.Ctx(r, usw.JOIN)), 20, add20)]),
        ("Put the parts together", [("run", usw.set_parts, ("rnd", usw.People, lambda r: usw.Ctx(r, usw.PARTS)), 20, add20)]),
        ("More stories", [("run", caw.set_join, ("rnd", caw.People, lambda r: caw.Ctx(r, caw.JOIN), "seen"), 20, add20)]),
        ("Find the missing part", [("run", usw.set_unknown, ("rnd", usw.People, lambda r: usw.Ctx(r, usw.JOIN)), 20, add20)]),
        ("Number sentences for stories", [("run", caw.set_parts, ("rnd", caw.People, lambda r: caw.Ctx(r, caw.PARTS), "seen"), 20, add20)]),
    ], 70109)
    finish(sets, R)
    body = lesson('<ul><li>Read the story. Find what is asked.</li><li>“In all”, “altogether” and “now” often mean <b>add</b>.</li><li>Draw or use counters if it helps.</li><li>Write a number sentence: 7 + 5 = 12. Check that the answer makes sense.</li></ul>',
        [example("Ana has 7 mangoes. She gets 5 more. How many now?", ["7 + 5"], "12 mangoes")],
        [['A number from the story', 'Work out the answer, do not copy a number.'], ['Subtracting', 'Joining means adding.'], ['Wrong sentence', 'Match the numbers to the story.']])
    faq = [('What does MATATAG Math 1 ask about word problems?', 'Solve problems (given orally or in pictures) involving addition with sums up to 20.'), ('How can parents help?', 'Read the story aloud and act it out with objects.'), ('What is a number sentence?', 'A sentence with numbers, like 7 + 5 = 12.'), ('Should children draw?', 'Yes. Drawing helps them see the story.')]
    make('addition-word-problems-within-20', 9, 'Number and Algebra', 'Grade 1: Number and Algebra',
         'Solve problems (given orally or in pictures) involving addition with sums up to 20.',
         'Addition Word Problems with Sums up to 20', 'Addition Word Problems',
         'Free Grade 1 addition word problems for the DepEd MATATAG curriculum: joining, putting parts together and number sentences with sums up to 20. 100 questions with answers.',
         '“In all” and “altogether” mean add.', 'Write a number sentence, then check.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
