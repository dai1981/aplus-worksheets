# -*- coding: utf-8 -*-
"""
대한민국（2022 개정 수학과 교육과정）の単元生成の共通部品。
・文は韓国語（해요체の短い文。初等 3学年が読める語）
・数は 4 けたまでそのまま（3468）、5 けた以上は 12,500 のようにカンマ
・単位は mm・cm・m・km、mL・L、g・kg・t、원
・時刻は「오전 9시 40분」、時間は「1시간 25분」「3분 20초」
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・答えも誤答もすべてコードで計算する
"""
import re
from fr_common import mix, pick_unique        # noqa: F401  (pick_unique は ValueError なども飛ばす)
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)

UPDATED = "2026-11-25"
STD_URL = "https://ncic.re.kr/inv/org/download.do?year=2022&seq=10003559&orgType=ogi4"
GIRLS = ["지우", "서아", "예서", "하나", "유나", "수아", "다희", "채아", "지아", "소이"]
BOYS = ["시우", "지호", "태오", "서호", "도하", "준서", "우주", "이도", "재희", "주호"]
DOMAIN = {"01": "수와 연산", "02": "변화와 관계", "03": "도형과 측정", "04": "자료와 가능성"}
GRADE_NAME = {"grade-1": "초등 1학년", "grade-2": "초등 2학년", "grade-3": "초등 3학년", "grade-4": "초등 4학년",
              "grade-5": "초등 5학년", "grade-6": "초등 6학년", "grade-7": "중학교 1학년", "grade-8": "중학교 2학년",
              "grade-9": "중학교 3학년", "common-math-1": "공통수학1", "common-math-2": "공통수학2", "algebra": "대수",
              "calculus-1": "미적분Ⅰ", "probability-and-statistics": "확률과 통계", "kindergarten": "유치원"}
# 유치원（2019 개정 누리과정、만 5세）：성취기준 코드がないので「자연탐구」の内容を standard_code に、domain は引数で渡す
STD_URL_NURI = "https://www.goe.go.kr/resource/old/BBSMSTR_000000030067/BBS_202302201143570171.pdf"
# 고등학교：영역は成就基準コードの頭（[10공수1-02-01] → 10공수1-02）で決める
DOMAIN_HS = {"10공수1-01": "다항식", "10공수1-02": "방정식과 부등식", "10공수1-03": "경우의 수", "10공수1-04": "행렬",
             "10공수2-01": "도형의 방정식", "10공수2-02": "집합과 명제", "10공수2-03": "함수와 그래프",
             "12대수01": "지수함수와 로그함수", "12대수02": "삼각함수", "12대수03": "수열",
             "12미적Ⅰ-01": "함수의 극한과 연속", "12미적Ⅰ-02": "미분", "12미적Ⅰ-03": "적분",
             "12확통01": "경우의 수", "12확통02": "확률", "12확통03": "통계"}


def num(n):
    """4けたまで 3468、5けた以上 12,500"""
    n = int(n)
    return str(n) if abs(n) < 10000 else "{:,}".format(n)


def dnum(v, places=1):
    """소수：0.3、2.5（不要な 0 は付けない）"""
    s = ("%." + str(places) + "f") % v
    return s.rstrip("0").rstrip(".") if "." in s else s


def won(n):
    return "%s원" % num(n)


def has_batchim(w):
    w = re.sub(r"<[^>]+>", "", str(w))
    w = re.sub(r"[\s)）」』'\".,!?]+$", "", w)
    if not w:
        return False
    c = w[-1]
    o = ord(c)
    if 0xAC00 <= o <= 0xD7A3:
        return (o - 0xAC00) % 28 != 0
    if c.isdigit():
        return num_batchim(w)
    if c in "LMNlmn":
        return True
    return False


def num_batchim(w):
    """数の読みの最後に받침があるか：…0（십・백・천・만・영）、1 일、3 삼、6 육、7 칠、8 팔"""
    d = re.sub(r"[^0-9]", "", str(w))
    return bool(d) and d[-1] in "013678"


def num_rieul(w):
    """最後が ㄹ 받침（1 일、7 칠、8 팔）→「으로」ではなく「로」"""
    d = re.sub(r"[^0-9]", "", str(w))
    return bool(d) and d[-1] in "178"


def fix_num_josa(s):
    """数字の直後の助詞を読みに合わせる（12를・13을、8로・6으로）"""
    def pair(m):
        n, j = m.group(1), m.group(2)
        bat = num_batchim(n)
        if j in ("으로", "로"):
            return n + ("로" if (not bat or num_rieul(n)) else "으로")
        a, b = {"을": ("을", "를"), "를": ("을", "를"), "은": ("은", "는"), "는": ("은", "는"), "과": ("과", "와"), "와": ("과", "와"),
                "이": ("이", "가"), "가": ("이", "가"), "이에요": ("이에요", "예요"), "예요": ("이에요", "예요")}[j]
        return n + (a if bat else b)
    s = re.sub(r"(?<![\w.])(\d[\d,.]*)(으로|로|이에요|예요|을|를|은|는|과|와)(?=[\s,.!?)」』<]|$)", pair, s)
    s = re.sub(r"(?<![\w.])(\d[\d,.]*)(이|가)(?=[\s<])", pair, s)

    s = re.sub(r"(<span class='fn'>(\d+)</span><span class='fd'>\d+</span></span>)(으로|로|이에요|예요|을|를|은|는|과|와|이|가)(?=[\s,.!?)」』<]|$)",
               lambda m: m.group(1) + pair(re.match(r"(\d+)(.*)", m.group(2) + m.group(3))).replace(m.group(2), "", 1), s)

    s = re.sub(r"(\d[\d,.]*)</b>(으로|로|이에요|예요|을|를|은|는|과|와|이|가)(?=[\s,.!?)」』<]|$)",
               lambda m: pair(re.match(r"(\d[\d,.]*)(.*)", m.group(1) + m.group(2))).replace(m.group(1), m.group(1) + "</b>", 1), s)

    def upair(m):
        u, j = m.group(1), m.group(2)
        bat = u in ("g", "kg", "t")
        if j in ("으로", "로"):
            return u + ("으로" if bat else "로")
        a, b = {"을": ("을", "를"), "를": ("을", "를"), "은": ("은", "는"), "는": ("은", "는"), "과": ("과", "와"), "와": ("과", "와"),
                "이": ("이", "가"), "가": ("이", "가"), "이에요": ("이에요", "예요"), "예요": ("이에요", "예요")}[j]
        return u + (a if bat else b)
    s = re.sub(r"(?<=\d )(cm|mm|km|m|mL|L|kg|g|t)(으로|로|이에요|예요|을|를|은|는|과|와|이|가)(?=[\s,.!?)」』<]|$)", upair, s)
    return s


def josa(w, pair):
    """josa('사과', '을/를') -> '사과를'。'으로/로' は ㄹ 받침のとき '로'"""
    a, b = pair.split("/")
    if a == "으로":
        c = re.sub(r"<[^>]+>", "", str(w))[-1:]
        if c and 0xAC00 <= ord(c) <= 0xD7A3 and (ord(c) - 0xAC00) % 28 == 8:
            return "%s로" % w
    if str(w)[-1:] in "mL" and a == "으로":          # 3 mL로, 2 m로（엠엘・미터）
        return "%s로" % w
    return "%s%s" % (w, a if has_batchim(w) else b)


def unit_josa(w, pair):
    """単位で終わる語：cm（센티미터）、mm、km、m、L（리터）、mL、g（그램）、kg、t（톤）、원、분、초、시간、개"""
    a, b = pair.split("/")
    w = str(w)
    end = {"cm": False, "mm": False, "km": False, "m": False, "L": False, "mL": False, "g": True, "kg": True, "t": False}
    for u, bat in end.items():
        if w.endswith(u):
            if a == "으로":
                return w + ("로" if not bat or u in ("L", "mL") else "으로")
            return w + (a if bat else b)
    return josa(w, pair)


class Names:
    def __init__(self, rnd):
        self.pool = GIRLS + BOYS
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        n = self.pool[self.i % len(self.pool)]
        self.i += 1
        return n


def mcq(q, correct, cands, e):
    """4 択：正解＋重複しない誤答 3 つ（文字列で比べる）。並びは balance() で決める。"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        m = re.match(r"^(.*?)(\d[\d,]*(?:\.\d+)?)([^\d]*)$", correct)
        if m and "<" not in correct:
            from decimal import Decimal as _D
            v = _D(m.group(2).replace(",", ""))
            places = len(m.group(2).split(".")[1]) if "." in m.group(2) else 0
            step = _D(1).scaleb(-places)
            for d in (1, -1, 2, -2, 3):
                nv = v + step * d
                if nv <= 0:
                    continue
                c = "%s%s%s" % (m.group(1), num(int(nv)) if places == 0 else format(nv, "f"), m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>예제</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>답: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html：생각하는 방법 → 예제 → 자주 하는 실수（短い文で）"""
    h = "<h2>생각하는 방법</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(example(*e) for e in examples)
    h += "<h2>자주 하는 실수</h2>" + table(["자주 하는 실수", "바르게 생각하기"], mist)
    return h


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>",
               lambda m: m.group(1) + "/" + m.group(2), t)
    assert "<" not in t, t
    return t


def unit(grade, slug, sort, code, std, title, short, meta, key_big, key_sub, think, examples, mist, faq, spec, seed,
         extra="", domain=None):
    """spec: [(セット名, [(maker, 数)])] × 5。code は '[4수01-03]' または '[4수03-13] [4수03-14]'"""
    import random
    R = random.Random(seed)
    seen = set()
    sets = [{"title": t, "items": mix(R, seen, parts)} for t, parts in spec]
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
    balance(sets, R)
    for s in sets:
        for it in s["items"]:
            for k in ("q", "e"):
                it[k] = tidy(it[k])
            it["c"] = [tidy(c) for c in it["c"]]
    title, short, meta, key_big, key_sub = map(plain_text, (title, short, meta, key_big, key_sub))
    assert len(title) <= 40 and len(key_big) <= 30 and len(key_sub) <= 50, (title, key_big, key_sub)
    gname = GRADE_NAME[grade]
    hs = re.search(r"\[(10공수[12]-\d\d|12대수\d\d|12미적Ⅰ-\d\d|12확통\d\d)", code)
    if grade == "kindergarten":
        dom = domain
        seo = "%s | 유치원(만 5세) 수학 학습지 (정답 포함)" % title
    elif hs:
        dom = DOMAIN_HS[hs.group(1)]
        seo = "%s | 고등학교 %s 학습지 (정답 포함)" % (title, gname)
    else:
        dom = DOMAIN[re.search(r"수(\d\d)-", code).group(1)]
        seo = "%s | %s 수학 학습지 (정답 포함)" % (title, gname)
    write_unit("kr", "math", grade, {
        "slug": slug, "title": title, "seo_title": seo,
        "short_title": short, "domain": dom, "standard_code": code, "standard_url": STD_URL_NURI if grade == "kindergarten" else STD_URL,
        "standard_text": std, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": lesson(think, examples, mist, extra),
        "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def tidy(s):
    """「1개들」のような誤りはないか、空白の重なりを直す"""
    s = re.sub(r"(?<=[^\s>]) {2,}(?=[^\s<])", " ", s)
    return fix_num_josa(s)


def clock(h, m, size=180, label=None, sec=None):
    """시계（짧은바늘は (h + m/60) × 30 度）。sec を渡すと초바늘も描く"""
    import math
    cx = cy = size / 2.0
    Rr = cx - 6
    k = Rr / 94.0
    s = ["<circle cx='%.1f' cy='%.1f' r='%.1f' fill='#fff' stroke='%s' stroke-width='%.1f'/>" % (cx, cy, Rr, GREEN, max(5 * k, 1.5))]
    small, big = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = Rr - (13 if i % 5 == 0 else 7) * k
        seg = "M%.1f %.1fL%.1f %.1f" % (cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                                        cx + (Rr - 3 * k) * math.cos(a), cy + (Rr - 3 * k) * math.sin(a))
        (big if i % 5 == 0 else small).append(seg)
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(small), INK, 1.2 * k))
    s.append("<path d='%s' stroke='%s' stroke-width='%.1f'/>" % ("".join(big), INK, max(2.6 * k, 1.2)))
    ah = math.radians(((h % 12) + m / 60.0) * 30 - 90)
    am = math.radians((m + (sec or 0) / 60.0) * 6 - 90)
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + Rr * 0.5 * math.cos(ah), cy + Rr * 0.5 * math.sin(ah), INK, max(8 * k, 2.5)))
    s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
             % (cx, cy, cx + Rr * 0.82 * math.cos(am), cy + Rr * 0.82 * math.sin(am), INK, max(4.5 * k, 1.8)))
    if sec is not None:
        a_s = math.radians(sec * 6 - 90)
        s.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f' stroke-linecap='round'/>"
                 % (cx, cy, cx + Rr * 0.9 * math.cos(a_s), cy + Rr * 0.9 * math.sin(a_s), RED, max(2 * k, 1)))
    fs = 19 * k
    s.append("<g font-size='%.1f' font-weight='700' fill='%s' text-anchor='middle' stroke='#fff' stroke-width='%.1f' "
             "paint-order='stroke'>" % (fs, INK, 3.5 * k))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        rn = Rr - 29 * k
        s.append("<text x='%.1f' y='%.1f'>%d</text>" % (cx + rn * math.cos(a), cy + rn * math.sin(a) + fs * 0.36, n))
    s.append("</g>")
    s.append("<circle cx='%.1f' cy='%.1f' r='%.1f' fill='%s'/>" % (cx, cy, max(6 * k, 2), INK))
    return fig(svg_wrap(int(size), int(size), "".join(s), label or "시계 %d시 %d분" % (h, m)))


def ff(v, mixed=True):
    """Fraction → 분수（mixed=True なら대분수 1<span>3/4</span>）"""
    from fractions import Fraction as _F
    v = _F(v)
    if v.denominator == 1:
        return num(v.numerator)
    w, r = divmod(v.numerator, v.denominator)
    if mixed and w:
        return "%d%s" % (w, fr(r, v.denominator))
    return fr(v.numerator, v.denominator)


def frac_read(n, d):
    return "%d분의 %d" % (d, n)


HAN = "영일이삼사오육칠팔구"


def read_num(n):
    """수 읽기: 3045 → 삼천사십오, 25000 → 이만 오천（만 단위で空白）"""
    if n == 0:
        return "영"

    def four(x):
        out = ""
        for p, u in ((1000, "천"), (100, "백"), (10, "십"), (1, "")):
            d = x // p % 10
            if d:
                out += ("" if d == 1 and u else HAN[d]) + u
        return out
    parts = []
    for big, u in ((10 ** 12, "조"), (10 ** 8, "억"), (10 ** 4, "만"), (1, "")):
        q = n // big % 10000
        if q:
            parts.append(("" if q == 1 and u == "만" else four(q)) + u)
    return " ".join(parts)
