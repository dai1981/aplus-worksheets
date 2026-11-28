# -*- coding: utf-8 -*-
"""
中国 / 科学（义务教育科学课程标准（2022年版），单元按教科版的顺序）。country `cn`、subject `science`、grade `grade-N`。
  UNITS: cn_s1（一、二年级）・cn_s3（三、四年级）・cn_s5（五、六年级）の UNITS(g)。
  U(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, sets)   think は段落のリスト、mist は (错误, 正确的想法)
  sets = lambda K: [(セット名, [(maker, 上限), …])] × 5。K は部品：
    K.P(rows, fwd, back=None, fe=None, be=None)  対の表（(甲, 乙)）。fwd は「{k}」を含む問題文で答えは乙、back は「{v}」で答えは甲
    K.G(groups, pos=…, neg=…)                     グループ分け（名前 → 物のリスト）。pos は「属于」、neg は「不属于」
    K.TF(true, false, topic)                      正しい文 / まちがいの文（(まちがい, 正しくは)）
    K.B(rows)                                     手書きの問題 (q, a, [w, w, w], e)
    K.F(fn)                                       自前の maker（fn(R) が item を返す）
  python3 cn_sci.py 3 [slug …]   で学年の単元を書く。seed は 95000 + 100 × 学年 + 番号
"""
import re
import sys
import random
import copy
import importlib
import sci_common
from sci_common import Unit, item
import cn_common
from cn_common import lesson, write_unit

STD_URL = cn_common.STD_URL
STAGE = {1: "第一学段（1～2年级）", 2: "第一学段（1～2年级）", 3: "第二学段（3～4年级）", 4: "第二学段（3～4年级）", 5: "第三学段（5～6年级）", 6: "第三学段（5～6年级）"}
DOM = {"M": "物质科学", "L": "生命科学", "E": "地球与宇宙科学", "T": "技术与工程"}
GRADE_ZH = cn_common.GRADE_ZH
UPDATED = "2026-11-28"
LATIN_OK = {"cm", "mm", "km", "kg", "mL", "min", "LED", "km/h", "m/s"}
TRAD = re.compile(r"[們個這為來說時對還會與無並後從應於將學數點麼裡邊樣條鐘幾讀寫錢買賣張隻開關動電體氣變長種鐵銅聲燈熱環號頭葉]")


def U(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, sets):
    assert dom in DOM
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets)


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def _ok_text(s, where):
    t = _txt(s)
    assert not TRAD.search(t), ("繁体字", where, t[:80])
    for w in re.findall(r"[A-Za-z][A-Za-z/]*", t):
        assert w in LATIN_OK or len(w) == 1, ("ラテン文字", w, where, t[:80])
    assert "\\" not in s
    return s


def it(q, a, wrong, e):
    x = item(q, a, wrong, e)
    for s in [q, e] + x["c"]:
        _ok_text(s, q)
    return x


class K:
    def __init__(self, R):
        self.R = R

    def P(self, rows, fwd, back=None, fe=None, be=None, match=True, sep="——"):
        """rows: [(k, v)]。fwd の答えは v（誤答は他の行の v）、back の答えは k、match は「配对」の問題（正しい組／まちがった組）"""
        R = self
        keys = sorted({k for k, _ in rows})
        vals = sorted({v for _, v in rows})
        good = {(k, v) for k, v in rows}

        def bad_pairs(n, avoid=None):
            out = set()
            for _ in range(60):
                k = R.R.choice(keys)
                v = R.R.choice(vals)
                if (k, v) not in good and (k, v) != avoid:
                    out.add((k, v))
                if len(out) >= n:
                    break
            return sorted(out)

        def mk():
            k, v = R.R.choice(rows)
            same = {vv for kk, vv in rows if kk == k}
            r = R.R.random()
            if match and r < 0.25 and len(rows) >= 4:
                if R.R.random() < 0.5:
                    w = bad_pairs(3)
                    if len(w) < 3 or len({a for a, _ in w} | {k}) < 4:
                        return None
                    return it("下面哪一组配对是正确的？", k + sep + v, [a + sep + b for a, b in w], (fe or "{k}：{v}。").format(k=k, v=v))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("下面哪一组配对是错误的？", bk + sep + bv, [a + sep + c for a, c in w], "“%s%s%s”是错误的，%s应该是“%s”。" % (bk, sep, bv, bk, right[0]))
            if back and r < 0.6:
                kk = {a for a, b in rows if b == v}
                w = [x for x in keys if x not in kk]
                if len(w) < 3:
                    return None
                e = (be or fe or "{k}：{v}。").format(k=k, v=v)
                return it(back.format(v=v), k, R.R.sample(w, 3), e)
            w = [x for x in vals if x not in same]
            if len(w) < 3:
                return None
            e = (fe or "{k}：{v}。").format(k=k, v=v)
            return it(fwd.format(k=k), v, R.R.sample(w, 3), e)
        return mk

    def G(self, groups, pos="下面哪一个是{g}？", neg="下面哪一个不是{g}？", e_pos="{a}属于“{g}”这一类。", e_neg="{a}不属于“{g}”，它属于“{h}”。"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), e_neg.format(a=a, g=g, h=h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), e_pos.format(a=a, g=g))
        return mk

    def TF(self, true, false, topic):
        """true: [正しい文]、false: [(まちがいの文, 正しくは)]"""
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["关于%s，下面说法正确的是哪一个？", "下面关于%s的说法，哪一句是对的？"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["关于%s，下面说法错误的是哪一个？", "下面关于%s的说法，哪一句是错的？"]) % topic
            return it(stem, f, w, "“%s”是错误的。%s" % (f.rstrip("。"), c))
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


def seed_of(g, sort):
    return 95000 + 100 * g + sort


def build(g, u, sort):
    U_ = Unit(seed_of(g, sort))
    k = K(U_.R)
    spec = u["sets"](k)
    sets = U_.sets(spec)
    for s in sets:
        for x in s["items"]:
            for t in [x["q"], x["e"]] + x["c"]:
                _ok_text(t, u["slug"])
    body = lesson(u["think"], u["ex"], u["mist"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in u["faq"]):
        _ok_text(s, u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    if g <= 2:
        assert len(u["title"]) <= 40 and len(u["kb"]) <= 40 and len(u["ks"]) <= 90, u["slug"]
    gz = GRADE_ZH[g]
    write_unit("cn", "science", "grade-%d" % g, {
        "slug": u["slug"], "title": u["title"], "seo_title": "%s｜%s科学练习题（附答案）" % (u["title"], gz),
        "short_title": u["short"], "domain": DOM[u["dom"]], "standard_code": "%s · %s" % (STAGE[g], DOM[u["dom"]]),
        "standard_url": STD_URL, "standard_text": u["std"] + "（课标学段目标与内容要求摘要）",
        "meta_desc": "%s科学“%s”练习题：%s，100题在线练习，附可打印答案和讲解。" % (gz, u["title"], u["what"]),
        "key_big": u["kb"], "key_sub": u["ks"], "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in u["faq"]], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def module_of(g):
    return {1: "cn_s1", 2: "cn_s1", 3: "cn_s3", 4: "cn_s3", 5: "cn_s5", 6: "cn_s5"}[g]


def main():
    g = int(sys.argv[1])
    only = sys.argv[2:]
    m = importlib.import_module(module_of(g))
    for i, u in enumerate(m.UNITS(g)):
        if only and u["slug"] not in only and str(i + 1) not in only:
            continue
        build(g, u, i + 1)
        print("wrote", g, u["slug"])


if __name__ == "__main__":
    main()
