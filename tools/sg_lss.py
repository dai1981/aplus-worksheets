# -*- coding: utf-8 -*-
"""
Singapore Lower Secondary Science (MOE 2021 G2/G3 Lower Secondary Science Syllabus): grade `secondary-1` / `secondary-2`.
make_lss(level, slug, sort, theme, topic, ...) writes the unit:
  standard_code "Secondary 1: Model of Cells - the Basic Unit of Life", domain = the syllabus theme
  (The Scientific Endeavour / Diversity / Models / Interactions / Systems), standard_url = the MOE syllabus PDF.
luse(U, modname, rep=, drop=) is sg_sci.use with secondary wording (pupils -> students, Year 7 -> Secondary 1) and drops
items that need things outside the syllabus (W = mg with g, V = IR, moments formula, ions, speed of sound).
Seeds: 64000 + 100 * level + sort.
"""
import json
import re
import sci_common
import sg_sci
from sg_sci import (Unit, item, bank, lesson, table, People, once, use, upto, sgm, _bad, UK_NAMES)

STD_URL = "https://www.moe.gov.sg/-/media/files/secondary/fsbb/syllabus/2021-g2g3-lower-secondary-science-syllabus-updated-apr-2024.pdf"
THEMES = ("The Scientific Endeavour", "Diversity", "Models", "Interactions", "Systems")
SEC_REP = [(r"\bpupils\b", "students"), (r"\bPupils\b", "Students"), (r"\bpupil\b", "student"), (r"\bPupil\b", "Student"),
           (r"\bYear 7\b", "Secondary 1"), (r"\bYear 8\b", "Secondary 2"), (r"\bmobile phone", "handphone"),
           (r"\boesophagus\b", "gullet (oesophagus)")]
SEC_DROP = [r"\bKS3\b", r"\bKS4\b", r"\bYear \d", r"\bGCSE\b", r"N/kg", r"\bg = ", r"V = IR", r"\bI = V", r"moment of", r"\bmoments?\b", r"\bions?\b",
            r"m/s.{0,30}sound|sound.{0,30}m/s", "mmol", "Ofsted", "National Grid", "NHS", "£"]


def luse(U, modname, rep=(), drop=()):
    return use(U, modname, rep=list(SEC_REP) + list(rep), drop=list(SEC_DROP) + list(drop))


_NUM = re.compile(r"(?<![\d,.])(\d{1,3}(?:,\d{3})+)(?![\d,])")


def sgnum(s):
    """Singapore numbers: 4 digits without a separator (1500), 5 or more with a no-break space (12\u00a0500). Tags are left alone."""
    def fix(m):
        d = m.group(1).replace(",", "")
        if len(d) <= 4:
            return d
        out = ""
        while len(d) > 3:
            out = "\u00a0" + d[-3:] + out
            d = d[:-3]
        return d + out
    def text(t):
        t = _NUM.sub(fix, t)
        return re.sub(r"(?<![\d.,])(\d{1,3}) (\d{3})(?![\d.,])", lambda m: m.group(1) + ("" if len(m.group(1)) == 1 else "\u00a0") + m.group(2), t)
    return re.sub(r"(<[^>]*>)|([^<]+)", lambda m: m.group(1) or text(m.group(2)), s)


def _fixnums(sets):
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"] = sgnum(it["q"]), sgnum(it["e"])
            it["c"] = [sgnum(c) for c in it["c"]]
    return sets


def make_lss(level, slug, sort, theme, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets, allow=()):
    assert level in (1, 2) and theme in THEMES, (level, theme)
    sets = _fixnums(sets)
    body = sgnum(body)
    blob = json.dumps([title, seo_title, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(allow))
    assert not bad, "Words that do not fit Singapore: %s" % bad
    t = re.sub(r"<[^>]+>", " ", blob)
    m = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in UK_NAMES)).search(t)
    assert not m, "UK name left: %s" % m.group(1)
    for w in ("pupil", "Year 7", "Year 8", "PSLE"):
        assert w not in t, w
    sci_common.make("secondary-%d" % level, slug, sort, "Secondary %d: %s" % (level, topic), std_text, title, seo_title, short, meta,
                    key_big, key_sub, body, faq, sets, domain=theme, country="sg", url=STD_URL)


def seo(level, name):
    s = "Secondary %d Science: %s Worksheets (Lower Secondary Science with Answers)" % (level, name)
    if len(s) > 95:
        s = "Secondary %d Science: %s Worksheets with Answers" % (level, name)
    return s
