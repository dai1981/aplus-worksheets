# -*- coding: utf-8 -*-
"""
South Africa Grade 6 Maths (CAPS): Decimal Fractions: Place Value, Comparing, Rounding and Converting (Grade 6: 1.3 Decimal fractions)
  python3 tools/gen_za_maths_g6_decimals.py
Place value of decimals to three places, comparing and ordering, rounding off, and changing between common and
decimal fractions (US Grade 5, Australia Year 5, Ontario Grade 6 and UK Year 6 makers), in South African decimal
comma form.
Wrong answers come from real mistakes: thinking a longer decimal is bigger, reading 0,3 as 3 hundredths, and rounding
the wrong digit.
"""
import za_common
from za_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, rand, cents, words, NBSP)
import random
import gen_us_math_g5_decimal_place_value as usd
adopt(usd)
if isinstance(getattr(usd, 'R', None), random.Random): usd.R = random.Random(806120)
import gen_au_maths_y5_decimals as aud
adopt(aud)
if isinstance(getattr(aud, 'R', None), random.Random): aud.R = random.Random(806121)
import gen_caon_math_g6_place_value as cap
adopt(cap)
if isinstance(getattr(cap, 'R', None), random.Random): cap.R = random.Random(806122)
import gen_uk_maths_y6_fdp as ukf
adopt(ukf)
if isinstance(getattr(ukf, 'R', None), random.Random): ukf.R = random.Random(806123)
za_common.GRADE = "grade-6"


import re as _re


def _txt(it):
    return _re.sub(r"<[^>]+>", " ", _re.sub(r"<svg.*?</svg>", " ", it["q"], flags=_re.S) + " " + " ".join(it["c"]) + " " + it["e"])


def _nums(it):
    return [int(x.replace(",", "").replace("\u00a0", "")) for x in _re.findall(r"(?<![\d.])\d[\d,\u00a0]*(?![.\d])", _txt(it)) if x.replace(",", "").replace("\u00a0", "").isdigit()]


def noneg(it):
    return not _re.search(r"(?<![\d)] )[−-]\d", _txt(it)) and "negative" not in _txt(it).lower()


def nine(it):
    """whole numbers to 9 digits, no negatives"""
    return all(n <= 999999999 for n in _nums(it)) and noneg(it)


def dec3(it):
    """decimals with at most 3 places, no negatives"""
    return noneg(it) and not _re.search(r"\d\.\d{4}", _txt(it))


def nodec(it):
    return noneg(it) and not _re.search(r"\d\.\d", _txt(it))


def flat(it):
    """first quadrant only: no negative numbers in the text or the picture"""
    return nodec(it) and "−" not in it["q"] and "-1" not in it["q"]


def nomean(it):
    return dec3(it) and not _re.search(r"\bmean\b", _txt(it))


def den12(it):
    ds = [int(d) for d in _re.findall(r"<span class='fd'>(\d+)</span>", it["q"] + " " + it["c"][it["a"]])]
    return all(d <= 12 or d in (20, 25, 50, 100) for d in ds) and nodec(it)



def build():
    sets, R = build_sets([
        ("Place value", [("run", usd.set_value, (), 10, dec3), ("run", cap.set_decimals, (), 10, dec3)]),
        ("Compare and order", [("run", cap.set_dcompare, (), 10, dec3), ("run", aud.set_compare, (), 10, dec3)]),
        ("Round off decimals", [("run", usd.set_round, (usd.People,), 20, dec3)]),
        ("Fractions and decimals", [("run", aud.set_fractions, (), 10, dec3), ("run", ukf.set_place_value, (), 10, dec3)]),
        ("Decimals on a number line", [("run", aud.set_number_line, (), 10, dec3), ("run", aud.set_problems, (), 10, dec3)]),
    ], 80612)
    finish(sets, R)
    body = lesson("<ul><li>After the decimal comma come tenths, hundredths and thousandths: 3,457.</li><li>0,5 = <span class='fr'><span class='fn'>5</span><span class='fd'>10</span></span>, 0,05 = <span class='fr'><span class='fn'>5</span><span class='fd'>100</span></span>, 0,005 = <span class='fr'><span class='fn'>5</span><span class='fd'>1000</span></span>.</li><li>To compare, line up the decimal commas and compare from the left. 0,6 &gt; 0,48.</li><li>To round to 1 decimal place, look at the hundredths digit.</li></ul>",
        [example("Order 0,6; 0,48; 0,605", ["0,600; 0,480; 0,605"], "0,48; 0,6; 0,605")],
        [['Longer is bigger', '0,48 &lt; 0,6.'], ['Wrong place', '0,3 is 3 tenths.'], ['The wrong digit', 'Look one place to the right.']])
    faq = [('What does CAPS Grade 6 say about decimal fractions?', 'Recognise, order and compare decimal fractions to at least 2 decimal places, round off decimal fractions to at least 1 decimal place, and recognise the place value of digits in decimal fractions.'), ('Why does South Africa use a decimal comma?', 'It is the South African standard: 2,5 means two and a half.'), ('Is 0,50 the same as 0,5?', 'Yes.'), ('What is 3/4 as a decimal?', '0,75.')]
    make('decimal-fractions', 12, 'Numbers, Operations and Relationships', 'Grade 6: 1.3 Decimal fractions',
         'Recognise, order and compare decimal fractions to at least 2 decimal places; round off decimal fractions to at least 1 decimal place; recognise the place value of digits in decimal fractions to at least 2 decimal places; recognise and use equivalent forms of common fractions and decimal fractions.',
         'Decimal Fractions: Place Value, Comparing, Rounding and Converting', 'Decimal Fractions',
         'Free CAPS Grade 6 decimal fractions worksheets: place value, comparing and ordering, rounding off and changing fractions to decimals. 100 questions with memos.',
         'Tenths, hundredths, thousandths after the decimal comma.', 'Line up the commas, then compare from the left.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
