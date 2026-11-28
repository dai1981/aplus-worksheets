# -*- coding: utf-8 -*-
"""中国 / 高中理科の単元を短く書くための部品。
H(...) の T は 3 つの表 (セット名, rows, fwd, back[, extra])。
セットは T0・T1・T2・（calc か bank か 3 表の混合）・TF の 5 つ"""
from cn_sci import U


def _p(K, t):
    name, rows, fwd, back = t[:4]
    extra = t[4] if len(t) > 4 else ()
    return K.P(rows, fwd, back, extra=extra)


def H(dom, part, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, calc=None, bank=None, s4=None):
    assert len(T) == 3

    def sets(K):
        out = [(t[0], [(_p(K, t), 20)]) for t in T]
        if calc and bank:
            mix = [(K.F(calc), 12), (K.B(bank), min(8, len(bank) - 3))]
            mix.append((_p(K, T[0]), 20 - sum(n for _, n in mix)))
        elif calc:
            mix = [(K.F(calc), 15), (_p(K, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K.B(bank), n)] + ([(_p(K, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(_p(K, T[0]), 7), (_p(K, T[1]), 7), (_p(K, T[2]), 6)]
        out.append((s4 or ("计算与应用" if calc else "综合练习"), mix))
        out.append((title, [(K.TF(TFt, TFf, topic), 20)]))
        return out
    return U(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, sets, part=part)
