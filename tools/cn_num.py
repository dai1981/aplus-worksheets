# -*- coding: utf-8 -*-
"""中国 / 理科の計算問題の部品：num（数の書き方）・nq（数の答えの 4 択）"""
from cn_sci import it


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci(x, d=3):
    """3.6×10⁶ の形"""
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return ("%s×10%s" % (m, str(int(e)).translate(SUP))).replace("-", "−")


def num(x, d=3):
    """有効な桁で表示（末尾の 0 を消す）。負の数は「−」。10 万以上と 0.001 未満は ×10ⁿ"""
    if x != 0 and (abs(x) >= 1e5 or abs(x) < 1e-3):
        return sci(x, d)
    if isinstance(x, int) or float(x).is_integer():
        s = "%d" % round(x)
    else:
        s = ("%." + str(d) + "g") % x
        if "e" in s:
            s = ("%." + str(d) + "f") % x
            s = s.rstrip("0").rstrip(".")
    return s.replace("-", "−")


def nq(q, ans, wrongs, unit, e, d=3):
    """数の答え。wrongs はよくある間違いの値（同じ値・0 以下は落とす）。3 つそろわないと None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError):
            continue
        if s != a and s not in out and not s.startswith("−") and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit in ("°", "%", "‰") else " ") + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)
