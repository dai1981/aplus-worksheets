# -*- coding: utf-8 -*-
"""
India / Science Class 11–12 (CBSE Senior Secondary 2025-26, NCERT Physics, Chemistry and Biology). Shared helpers.
  SU(subj, sort, slug, chapter, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)  one unit = one NCERT chapter;
      domain = the subject, standard_code "Class 11 Physics, Chapter 5: Laws of Motion", standard_url = the CBSE subject syllabus
  A(f, *kinds)   use a UK A level maker (al_phys / al_chem / al_bio) with this unit's random generator
  N(q, v, wrongs, unit, e, sf)   number item (space before the unit)
  ch(xs)         random choice
NCERT uses g = 9.8 m/s² (al_phys.G is set to 9.8; in_sci.build prints 9.81 as 9.8 when the module sets G98).
"""
import sys
import al_phys
import al_chem
import al_bio
import uk_alsci
from in_sci import _R, pairs, K
from uk_alsci import nf, tq, once_maker
from in_sci6a import odd_one, _cap

al_phys.G = 9.8
BASE = "https://www.cbseacademic.nic.in/web_material/CurriculumMain26/SrSec/%s_SrSec_2025-26.pdf"
URLS = {s: BASE % s for s in ("Physics", "Chemistry", "Biology")}


def ch(xs):
    return _R[0].choice(xs)


def A(f, *kinds):
    mod = sys.modules[f.__module__]

    def g():
        mod.R = _R[0]
        return f(_R[0].choice(kinds)) if kinds else f()
    g.__name__ = f.__name__ + ("_" + "_".join(kinds) if kinds else "")
    return g


def N(q, v, wrongs, unit, e, sf=3):
    u = (" " + unit) if unit and unit[0] not in " °%" else unit
    wrongs = [w for w in wrongs if w is not None and w == w and abs(w) < 1e30]
    return uk_alsci.nq(q, v, wrongs, u, e, sf)


def B(rows):
    """bank from rows (q, a, [w, w, w], e)"""
    return once_maker(rows)


def SU(subj, sort, slug, chapter, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, chname=None):
    return dict(sort=sort, slug=slug, chapter=chapter, unit_name=subj, subj=subj, url=URLS[subj], chname=chname, std=std, title=title, short=short, meta=meta,
                kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets)
