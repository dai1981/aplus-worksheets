# -*- coding: utf-8 -*-
"""
대한민국 중학교 수학（2022 개정 [9수01-01]〜[9수04-09]）の共通部品。
・負の数は「−」（U+2212）、かっこ付きは（−3）。分数は fr()、帯分数は使わない
・M(q, 답, 오답, 해설)：負の数の選択肢も使える 4 択（誤答が 3 つそろわないと None）
・식：P([(계수, '문자')]) → 2x − 3y + 1、sup(2) → ²、rt(12) → 2√3
・図：figure（A, B, C の点）・kosy（좌표평면）・kurve（그래프）を韓国語の aria-label で
"""
import re
import math
from fractions import Fraction as Fr
import kr_low  # noqa: F401  (tidy の拡張：名詞・助数詞の後の助詞、예요/이에요)
from kr_common import unit, josa, Names, num, fr, table  # noqa: F401
import fr_c4
import de_k8
import de_k10
from ws_common import fig, svg_wrap, text, line, INK, GREEN, RED, BLUE, FILL  # noqa: F401

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(SUP)


def neg(v):
    """정수・분수 → 문자열（분수는 HTML）"""
    v = Fr(v)
    if v.denominator == 1:
        return ("−%s" % num(-v.numerator)) if v < 0 else num(v.numerator)
    s = fr(abs(v.numerator), v.denominator)
    return ("−" + s) if v < 0 else s


def par(v):
    v = Fr(v)
    return "(%s)" % neg(v) if v < 0 else neg(v)


def sg(v):
    """+3 / −3（부호를 붙여서）"""
    v = Fr(v)
    return ("+" if v > 0 else "") + neg(v)


def dec(v, k=None):
    """소수：0.25、−1.5（필요 없는 0은 지움）"""
    s = ("%." + str(k if k is not None else 6) + "f") % float(v)
    if k is None or "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace("-", "−")


def P(terms):
    """[(계수, '문자')] → '2x − 3y + 1'（계수 1・−1은 생략, 0은 뺌）"""
    out = []
    for c, v in terms:
        c = Fr(c)
        if c == 0:
            continue
        a = abs(c)
        if v and a == 1:
            body = v
        elif a.denominator == 1:
            body = num(a.numerator) + v
        else:
            body = fr(a.numerator, a.denominator) + v
        if not out:
            out.append(("−" if c < 0 else "") + body)
        else:
            out.append((" − " if c < 0 else " + ") + body)
    return "".join(out) or "0"


def rt(n):
    """√n을 간단히：12 → 2√3、9 → 3"""
    a, b = 1, n
    k = 2
    while k * k <= b:
        while b % (k * k) == 0:
            a *= k
            b //= k * k
        k += 1
    if b == 1:
        return str(a)
    return ("" if a == 1 else str(a)) + "√" + str(b)


def M(q, ans, cands, e):
    ans = str(ans)
    seen = {ans}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or "None" in c:
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [ans] + pick, "a": 0, "e": e}


def N(q, v, wrongs, e, f=neg):
    """수 답：v와 오답을 f로 문자열로"""
    return M(q, f(v), [f(w) for w in wrongs if w is not None and Fr(w) != Fr(v)], e)


def ko_label(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


def figure(pts, segs, label="도형", **k):
    return ko_label(fr_c4.figure(pts, segs, label=label, **k), label)


def kosy(lines=(), pts=(), lo=-5, hi=5, label="좌표평면"):
    return ko_label(de_k8.kosy(lines, pts, lo, hi, label=label), label)


def kurve(fs, xr, yr, pts=(), label="그래프", **k):
    return ko_label(de_k10.kurve(fs, xr, yr, pts, label=label, **k), label)


def lesson_unit(grade, slug, sort, code, std, title, short, meta, kb, ks, think, examples, mist, faq, spec, seed):
    return unit(grade, slug, sort, code, std, title, short, meta, kb, ks, think, examples, mist, faq, spec, seed)


# ------------------------------------------------------------------ 괄호 뒤의 조사：(6, 1)는 → (6, 1)은, (−3)를 → (−3)을
import kr_common as _KC
_prev_tidy = _KC.tidy


def _paren_josa(s):
    def f(m):
        d, j = m.group(1), m.group(2)
        fixed = _KC.fix_num_josa(d + j + " ")[len(d):-1]
        return d + ")" + fixed
    return re.sub(r"(\d)\)(으로|로|이에요|예요|은|는|을|를|이|가|과|와)(?=[\s,.?!<]|$)", f, s)


_SUPJ = {"를": "을", "는": "은", "가": "이", "와": "과", "로": "으로", "예요": "이에요", "라고": "이라고"}


def _sup_josa(s):
    """x², a³ … は「제곱」と読むので받침あり：x²를 → x²을（cm², m³ は 미터なのでそのまま）"""
    def f(m):
        pre, sup_, tag, j = m.group(1), m.group(2), m.group(3) or "", m.group(4)
        if pre.endswith("m"):
            return m.group(0)
        return pre + sup_ + tag + _SUPJ.get(j, j)
    return re.sub(r"([A-Za-z)]|^)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)(</b>|\)|</sup>)?(를|는|가|와|로|예요|라고)(?=[\s,.?!<]|$)", f, s)


def _tidy_mid(s):
    return _sup_josa(_paren_josa(_prev_tidy(s)))


_KC.tidy = _tidy_mid


# ------------------------------------------------------------------ 순환소수의 점：0.3̇5̇ → <span class='rd'>…（ws.css・ws-print.css の .rd）
_prev_write = _KC.write_unit


def _rd(s):
    return re.sub("(\\d)\u0307", "<span class='rd'>\\1</span>", s)


def _write_unit(country, subject, grade, d):
    d["body_html"] = _rd(d["body_html"])
    for st in d["sets"]:
        for it in st["items"]:
            it["q"], it["e"] = _rd(it["q"]), _rd(it["e"])
            it["c"] = [_rd(c) for c in it["c"]]
    for f in d["faq"]:
        assert "\u0307" not in f["q"] + f["a"], f
    return _prev_write(country, subject, grade, d)


_KC.write_unit = _write_unit
