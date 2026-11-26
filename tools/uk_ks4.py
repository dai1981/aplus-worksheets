# -*- coding: utf-8 -*-
"""
UK KS4 science (Year 10-11, GCSE Combined Science) helpers.
  U4(seed) -> (U, R, P, us) where us("chem_bonding", "g_name", drop=("mol",), rep=(("old", "new"),)) adopts the US
  high-school maker in British English (uk_sci.ukm), replaces text (rep) and drops items whose text contains any of `drop`.
  build(year, slug, sort, subject, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets) writes the unit.
"""
import uk_sci
from uk_sci import Unit, People, ukm, adopt_us, lesson, make_ks4

_MODS = {}


def U4(seed):
    U = Unit(seed)
    R = U.R
    P = People(R)
    uk_sci.USED.clear()

    def us(mod, name, drop=(), rep=()):
        full = "gen_us_science_" + mod
        if full not in _MODS:
            _MODS[full] = adopt_us(full, U)
        f = ukm(getattr(_MODS[full], name))
        if not drop and not rep:
            return f

        def g():
            it = f()
            if it is None:
                return None
            for a, b in rep:
                it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
                it["c"] = [c.replace(a, b) for c in it["c"]]
            t = it["q"] + it["e"] + "".join(it["c"])
            return None if any(d in t for d in drop) else it
        return g
    def uk(mod, name):
        import importlib
        m = importlib.import_module(mod)
        m.U, m.R, m.P = U, R, P
        return getattr(m, name)
    us.uk = uk
    return U, R, P, us


def build(U, year, slug, sort, subject, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, seo=None, allow=()):
    body = lesson(think, ex, mist)
    seo = seo or "Year %d Science: %s Worksheets (GCSE Combined Science)" % (year, title)
    make_ks4(year, slug, sort, subject, topic, std, title, seo, short, meta, kb, ks, body, faq, U.sets(sets), allow=allow)
