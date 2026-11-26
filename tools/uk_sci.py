# -*- coding: utf-8 -*-
"""
UK science (National Curriculum in England, science programmes of study): subject `science`, grade `year-N`.
Builds on sci_common: British English (colour, metre, litre, centre, torch, Mum), UK names, and make_uk() that fills
in the standard fields: standard_code "Year 6: Light", domain = the programme of study heading ("Light"),
standard_url = the GOV.UK science programmes of study page.
make_uk() checks the whole unit for American spellings and words (LEAKS) before it writes.
"""
import json
import re
import sci_common
from sci_common import (Unit, item, bank, lesson, kid_lesson, table, pick, bar_chart, pie, arrow, sun, rect, circle,
                        svg_wrap, text, line, fig, figure, B, cap, GREEN, BLUE, RED, INK, FILL, GRAY, FONT,
                        ORANGE, BROWN, SKY, SUN, LEAF)
from uk_ks3 import People, GIRLS, BOYS

STD_URL = "https://www.gov.uk/government/publications/national-curriculum-in-england-science-programmes-of-study"
STD_URL_KS4 = "https://www.gov.uk/government/publications/national-curriculum-in-england-science-programmes-of-study"

# American spellings and words that must not appear (whole words, case-insensitive)
LEAKS = ["color", "colors", "colored", "colorful", "center", "centers", "meter", "meters", "centimeter", "centimeters",
         "millimeter", "millimeters", "kilometer", "kilometers", "liter", "liters", "milliliter", "milliliters",
         "behavior", "behaviors", "gray", "aluminum", "favorite", "flashlight", "flashlights", "mom", "math", "fiber",
         "fibers", "grade", "grades", "sulfur", "gasoline", "faucet", "sidewalk", "candy", "cookie", "cookies",
         "vacation", "soccer", "neighbor", "neighbors", "neighborhood", "mold", "molds", "odor", "vapor", "harbor",
         "tire", "tires", "diaper", "diapers", "fries", "zucchini", "eggplant", "cilantro", "flashcard", "recess",
         "fahrenheit", "inch", "inches", "pound", "pounds", "ounce", "ounces", "gallon", "gallons", "mile", "miles"]
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)


def _text_of(unit_json):
    t = re.sub(r"<[^>]+>", " ", unit_json)
    return t


def make_uk(year, slug, sort, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
            code=None, domain=None, allow=()):
    """year: 1..6 (KS1-KS2) or 7..9 (KS3); topic: the programme of study heading ("Light")."""
    grade = "year-%d" % year
    code = code or "Year %d: %s" % (year, topic)
    blob = json.dumps([title, seo_title, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted({m.group(1).lower() for m in LEAK_RE.finditer(_text_of(blob))} - set(allow))
    assert not bad, "American words: %s" % bad
    sci_common.make(grade, slug, sort, code, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
                    domain=domain or topic, country="uk", url=STD_URL)


USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n
