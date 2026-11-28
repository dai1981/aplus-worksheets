# -*- coding: utf-8 -*-
"""
대한민국 / 과학（2022 개정 과학과 교육과정）。country `kr`、subject `science`。
  grade: grade-3〜grade-6（초등）、grade-7〜grade-9（중학교）、
         integrated-science-1・integrated-science-2（통합과학1・2）、physics・chemistry・life-science・earth-science（일반 선택）
  単元: kr_s3（초등 3·4학년）・kr_s5（5·6학년）・kr_s7〜kr_s9（중학교）・kr_s10（통합과학1·2）・kr_s11（물리학·화학）・kr_s12（생명과학·지구과학）の UNITS(g)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(セット名, rows, fwd, back[, extra]) か (セット名, {グループ: [物]})
    fwd は「{k}」、back は「{v}」を含む問題文。助詞は {k}・{v} の直後に書かない（「‘{k}’의 …」「‘{k}’에 …」は可）
    TFt は正しい文、TFf は (まちがいの文, 正しくは)、topic は「…에 대한 설명으로 옳은 것은?」の「…」
    tp は topics.php のトピック（matter・forces-and-motion・energy・waves-and-light・living-things-and-ecosystems・earth-and-space・earths-systems・science-and-society）
  python3 kr_sci.py grade-3 [slug|番号 …]   seed は 85000 + 100 × 学年の番号 + 番号
"""
import re
import sys
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import kr_common

UPDATED = "2026-11-28"
STD_URL = "https://www.ncic.re.kr/"
GRADES = {
    "grade-3": (3, "초등 3학년", "초등학교 3~4학년군"), "grade-4": (4, "초등 4학년", "초등학교 3~4학년군"),
    "grade-5": (5, "초등 5학년", "초등학교 5~6학년군"), "grade-6": (6, "초등 6학년", "초등학교 5~6학년군"),
    "grade-7": (7, "중학교 1학년", "중학교 1~3학년군"), "grade-8": (8, "중학교 2학년", "중학교 1~3학년군"), "grade-9": (9, "중학교 3학년", "중학교 1~3학년군"),
    "integrated-science-1": (10, "통합과학1", "통합과학1"), "integrated-science-2": (11, "통합과학2", "통합과학2"),
    "physics": (12, "물리학", "물리학"), "chemistry": (13, "화학", "화학"), "life-science": (14, "생명과학", "생명과학"), "earth-science": (15, "지구과학", "지구과학"),
}
MODULE = {"grade-3": "kr_s3", "grade-4": "kr_s3", "grade-5": "kr_s5", "grade-6": "kr_s5", "grade-7": "kr_s7", "grade-8": "kr_s8", "grade-9": "kr_s9",
          "integrated-science-1": "kr_s10", "integrated-science-2": "kr_s10", "physics": "kr_s11", "chemistry": "kr_s11", "life-science": "kr_s12", "earth-science": "kr_s12"}
DOM = {"E": "운동과 에너지", "M": "물질", "L": "생명", "S": "지구와 우주", "X": "과학과 사회"}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "science-and-society"}
HAN = re.compile(r"[぀-ヿ㐀-鿿豈-﫿]")
LATIN_OK = {"cm", "mm", "km", "kg", "mg", "mL", "L", "g", "m", "s", "N", "J", "W", "V", "A", "Hz", "LED", "DNA", "km/h", "m/s", "pH", "Ω"}
CIRC = "①②③④"


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where, elem=False):
    t = _txt(s)
    assert not HAN.search(t), ("漢字・かな", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("空白", where, t[:80])
    if elem:
        for w in re.findall(r"[A-Za-z][A-Za-z/]*", t):
            assert w in LATIN_OK or len(w) == 1, ("ラテン文字", w, where, t[:80])
    return s


QJ = re.compile(r"‘([^‘’]+)’(으로|로|은|는|이|가|을|를|과|와)(?=[\s?.,!]|$)")
PAIR = {"으로": "으로/로", "로": "으로/로", "은": "은/는", "는": "은/는", "이": "이/가", "가": "이/가", "을": "을/를", "를": "을/를", "과": "과/와", "와": "과/와"}


def fix_josa(s):
    """‘…’の直後の助詞を中身の最後の文字に合わせる"""
    return QJ.sub(lambda m: "‘%s’" % m.group(1) + kr_common.unit_josa(m.group(1), PAIR[m.group(2)])[len(m.group(1)):], s)


def it(q, a, wrong, e):
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ 数
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci(x, d=3):
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return ("%s×10%s" % (m, str(int(e)).translate(SUP))).replace("-", "−")


def num(x, d=3):
    """有効な桁で表示（末尾の 0 を消す）。1,000 以上の整数はカンマ。100 万以上と 0.001 未満は ×10ⁿ。負の数は「−」"""
    if x != 0 and (abs(x) >= 1e6 or abs(x) < 1e-3):
        return sci(x, d)
    if isinstance(x, int) or float(x).is_integer():
        s = "{:,}".format(int(round(x)))
    else:
        s = ("%." + str(d) + "g") % x
        if "e" in s:
            s = ("%." + str(d) + "f") % x
            s = s.rstrip("0").rstrip(".")
    return s.replace("-", "−")


def nq(q, ans, wrongs, unit, e, d=3):
    """数の答え。wrongs はよくある間違いの値（同じ値・負の数・0 は落とす）。3 つそろわないと None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError, OverflowError):
            continue
        if s != a and s not in out and not s.startswith("−") and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit in ("°", "%", "초", "분", "시간", "배", "개", "년", "번째", "가지", "명", "회") else " ") + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)


# ------------------------------------------------------------ 部品
class K:
    def __init__(self, R):
        self.R = R

    def P(self, rows, fwd, back=None, fe=None, be=None, match=True, sep=" – ", extra=()):
        """rows: [(k, v)] か [(k, v, tag)]。tag があると誤答は同じ tag の行からだけ取る"""
        R = self
        tag = {}
        for r in rows:
            tag[(r[0], r[1])] = r[2] if len(r) > 2 else None
        rows = [(r[0], r[1]) for r in rows]
        tk = {r[0]: tag[r] for r in rows}
        tv = {r[1]: tag[r] for r in rows}
        keys = sorted({k for k, _ in rows})
        vals = sorted({v for _, v in rows})
        good = set(rows)

        def bad_pairs(n):
            out = set()
            for _ in range(80):
                k = R.R.choice(keys)
                v = R.R.choice([x for x in vals if tv[x] == tk[k]])
                if (k, v) not in good:
                    out.add((k, v))
                if len(out) >= n:
                    break
            return sorted(out)

        def mk():
            k, v = R.R.choice(rows)
            t = tag[(k, v)]
            same = {vv for kk, vv in rows if kk == k}
            r = R.R.random()
            if match and r < 0.25 and len(rows) >= 4:
                if R.R.random() < 0.5:
                    w = bad_pairs(3)
                    if len(w) < 3 or len({a for a, _ in w} | {k}) < 4:
                        return None
                    return it("다음 중 짝 지은 것이 옳은 것은?", k + sep + v, [a + sep + b for a, b in w], (fe or "{k}: {v}").format(k=k, v=v) + ("" if (fe or "").endswith(".") else "."))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("다음 중 짝 지은 것이 옳지 않은 것은?", bk + sep + bv, [a + sep + c for a, c in w], "‘%s’의 바른 짝은 ‘%s’입니다." % (bk, right[0]))
            if back and r < 0.6:
                kk = {a for a, b in rows if b == v}
                w = [x for x in keys if x not in kk and tk[x] == t]
                if len(w) < 3:
                    return None
                e = (be or fe or "{k}: {v}").format(k=k, v=v)
                return it(back.format(v=v), k, R.R.sample(w, 3), e if e.endswith(".") else e + ".")
            w = [x for x in vals if x not in same and tv[x] == t] + [x for x in extra if x not in same]
            if len(w) < 3:
                return None
            e = (fe or "{k}: {v}").format(k=k, v=v)
            return it(fwd.format(k=k), v, R.R.sample(w, 3), e if e.endswith(".") else e + ".")
        return mk

    def G(self, groups, pos="다음 중 ‘{g}’에 해당하는 것은?", neg="다음 중 ‘{g}’에 해당하지 않는 것은?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s: ‘%s’에 해당합니다." % (a, h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s: ‘%s’에 해당합니다." % (a, g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["%s에 대한 설명으로 옳은 것은?", "다음 중 %s에 대해 바르게 말한 것은?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["%s에 대한 설명으로 옳지 않은 것은?", "다음 중 %s에 대해 잘못 말한 것은?"]) % topic
            return it(stem, f, w, "‘%s’는 틀린 설명입니다. %s" % (f.rstrip("."), c))
        return mk

    def B(self, rows):
        its = [it(*r) for r in rows]
        R = self

        def mk():
            return copy.deepcopy(R.R.choice(its))
        mk.n = len(its)
        return mk

    def F(self, fn):
        R = self

        def mk():
            return fn(R.R)
        return mk


def _jong(c, j):
    o = ord(c) - 0xAC00
    return chr(0xAC00 + o - o % 28 + j)


def polite(s):
    """「…다.」を「…ㅂ니다./…습니다.」にそろえる（正しい文とまちがいの文の文体で答えが分からないように）"""
    if s.endswith("니다."):
        return s
    assert s.endswith("다."), s
    t = s[:-2]
    if t.endswith("는"):
        return t[:-1] + "습니다."
    c = t[-1]
    j = (ord(c) - 0xAC00) % 28
    if j in (0, 4, 8):
        return t[:-1] + _jong(c, 17) + "니다."
    return t + "습니다."


def H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=None, bank=None, s4=None):
    assert len(T) == 3 and tp in TOPICS, slug
    TFt = [polite(x) for x in TFt]
    TFf = [(polite(a), b) for a, b in TFf]

    def part(K_, t):
        if isinstance(t[1], dict):
            return K_.G(t[1])
        name, rows, fwd, back = t[:4]
        return K_.P(rows, fwd, back, extra=t[4] if len(t) > 4 else ())

    def sets(K_):
        out = [(t[0], [(part(K_, t), 20)]) for t in T]
        if calc and bank:
            mix = [(K_.F(calc), 12), (K_.B(bank), min(8, len(bank) - 3))]
            mix.append((part(K_, T[0]), 20 - sum(n for _, n in mix)))
        elif calc:
            mix = [(K_.F(calc), 15), (part(K_, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K_.B(bank), n)] + ([(part(K_, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(part(K_, T[0]), 7), (part(K_, T[1]), 7), (part(K_, T[2]), 6)]
        out.append((s4 or ("계산과 적용" if calc else "종합 연습"), mix))
        out.append((title, [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 85000 + 100 * n + sort


PCT = re.compile(r"(\d) %")


def pct(t):
    """25 % → 25%（국립국어원：숫자와 % 사이를 띄우지 않는다）"""
    return PCT.sub(r"\1%", t)


def build(grade, u, sort):
    u = dict(u)
    for k in ("title", "short", "kb", "ks", "std", "what"):
        u[k] = pct(u[k])
    u["think"] = [pct(t) for t in u["think"]]
    u["ex"] = [(pct(q), [pct(x) for x in st], pct(a)) for q, st, a in u["ex"]]
    u["mist"] = [(pct(a), pct(b)) for a, b in u["mist"]]
    u["faq"] = [(pct(a), pct(b)) for a, b in u["faq"]]
    n, gname, band = GRADES[grade]
    elem = n <= 6
    U_ = Unit(seed_of(n, sort))
    sets = U_.sets(u["sets"](K(U_.R)))
    for s in sets:
        for x in s["items"]:
            x["q"], x["e"] = pct(fix_josa(kr_common.tidy(x["q"]))), pct(fix_josa(kr_common.tidy(x["e"])))
            x["c"] = [pct(fix_josa(kr_common.tidy(c))) for c in x["c"]]
            for t in [x["q"], x["e"]] + x["c"]:
                ok_text(t, u["slug"], elem)
    body = kr_common.lesson(u["think"], u["ex"], u["mist"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in u["faq"]):
        ok_text(s, u["slug"], elem)
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    assert len(u["title"]) <= 40 and len(u["kb"]) <= 40 and len(u["ks"]) <= 90, (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    hs = n >= 10
    dom = u["dom"] if hs else DOM[u["dom"]]
    seo = "%s | %s %s 학습지 (정답 포함)" % (u["title"], "고등학교" if hs else gname, gname if hs else "과학")
    write_unit("kr", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": "%s · %s" % (band, dom),
        "standard_url": STD_URL, "standard_text": u["std"] + " (2022 개정 과학과 교육과정 성취기준 요약)",
        "meta_desc": "%s ‘%s’ 학습지: %s. 100문제 온라인 연습과 정답·해설이 있는 인쇄용 학습지." % (gname if hs else gname + " 과학", u["title"], u["what"]),
        "key_big": u["kb"], "key_sub": u["ks"], "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in u["faq"]], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def units(grade):
    m = importlib.import_module(MODULE[grade])
    return m.UNITS(grade)


def main():
    grade = sys.argv[1]
    only = sys.argv[2:]
    for i, u in enumerate(units(grade)):
        if only and u["slug"] not in only and str(i + 1) not in only:
            continue
        build(grade, u, i + 1)
        print("wrote", grade, u["slug"])


if __name__ == "__main__":
    import kr_sci
    kr_sci.main()
