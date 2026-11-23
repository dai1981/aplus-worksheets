# -*- coding: utf-8 -*-
"""
España 1.º–3.º de Primaria: ayuda para los generadores que reutilizan los problemas de 4.º (mismo ciclo en 3.º)
unit(lv, slug, sort, dom, std, title, short, meta, key_big, key_sub, think, examples, mist, faq, spec, seed, pic="")
spec = [(título de la serie, [(generador, número), …])] × 5
src(nombre, seed, *funciones, mx=9999, sin=()) → generadores de gen_es_matematicas_4_nombre con números hasta mx
"""
import random
from es_common import mix, lesson, make_unit, use, lim, sin as sin_


def src(name, seed, *names, mx=9999, sin=(), dec=False, extra=(), rep=()):
    """rep: [(viejo, nuevo)] que se cambian en la pregunta, las opciones y la explicación"""
    preds = [lim(mx, dec=dec)]
    if sin:
        preds.append(sin_(*sin))
    preds.extend(extra)
    out = use("gen_es_matematicas_4_" + name, seed, *names, preds=tuple(preds))
    if not rep:
        return out
    def wrap(mk):
        def f():
            it = mk()
            if it:
                for a, b in rep:
                    it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
                    it["c"] = [c.replace(a, b) for c in it["c"]]
            return it
        f.__name__ = mk.__name__
        return f
    return [wrap(m) for m in out] if isinstance(out, list) else wrap(out)


def unit(lv, slug, sort, dom, std, title, short, meta, key_big, key_sub, think, examples, mist, faq, spec, seed, pic=""):
    R = random.Random(seed)
    seen = set()
    sets = [(t, mix(R, seen, parts)) for t, parts in spec]
    make_unit(R, slug, dom, std, title, short, meta, key_big, key_sub, lesson(think, examples, mist, pic), faq, sets, sort, grade="%d-primaria" % lv)
