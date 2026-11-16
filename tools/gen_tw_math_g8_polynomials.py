# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：多項式與加減（108課綱 A-8-2、A-8-3）
  python3 tools/gen_tw_math_g8_polynomials.py
多項式の名詞（項數・次數・係數・常數項・最高次項）、升冪・降冪、多項式の加法・減法（同類項・括號の前の負號）、式の値・應用。
誤答：次數を項數と取り違える、係數の符號を落とす、減法で後ろの全項の符號を變えない、異なる次數の項を合わせる。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num
from tw_g8 import poly, padd, sn, par, tidy_sets

R = random.Random(81002)
NM = Names(R)


def nz(lo, hi):
    while True:
        v = R.randint(lo, hi)
        if v:
            return v


def rp(deg, zero_ok=True):
    cs = [nz(-9, 9)] + [R.randint(-9, 9) if zero_ok else nz(-9, 9) for _ in range(deg)]
    return cs


def s1(seen):
    def mk():
        d = R.choice([2, 3])
        cs = rp(d)
        p = poly(cs)
        terms = sum(1 for c in cs if c)
        k = R.choice(["deg", "terms", "coef", "const", "lead"])
        if k == "deg":
            return mcq("多項式 %s 是幾次多項式？" % p, "%d 次" % d, ["%d 次" % x for x in (terms, d + 1, d - 1)  if x != d] + ["%d 次" % (d + 2)], "最高次項是 %s，所以是 %d 次多項式。" % (poly([cs[0]] + [0] * d), d))
        if k == "terms":
            return mcq("多項式 %s 有幾項？" % p, "%d 項" % terms, ["%d 項" % x for x in (d, terms + 1, terms - 1 if terms > 1 else terms + 2)  if x != terms], "用 ＋、－ 隔開的部分各是一項，共 %d 項。" % terms)
        if k == "coef":
            if cs[-2] == 0:
                return None
            return mcq("多項式 %s 中，一次項的係數是多少？" % p, sn(cs[-2]), [sn(-cs[-2]), sn(cs[0]), sn(cs[-1]) if cs[-1] != cs[-2] else sn(cs[-2] + 1)], "一次項是 %s，係數要連同正負號：%s。" % (poly([cs[-2], 0]), sn(cs[-2])))
        if k == "const":
            return mcq("多項式 %s 的常數項是多少？" % p, sn(cs[-1]), [sn(-cs[-1]) if cs[-1] else "1", sn(cs[0]), "沒有常數項" if cs[-1] else sn(cs[-2] or 1)], "不含 x 的項是常數項：%s。" % sn(cs[-1]))
        return mcq("多項式 %s 的最高次項係數是多少？" % p, sn(cs[0]), [sn(-cs[0]), str(d), sn(cs[-1]) if cs[-1] != cs[0] else sn(cs[0] + 1)], "最高次項 %s 的係數是 %s。" % (poly([cs[0]] + [0] * d), sn(cs[0])))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        d = R.choice([2, 3])
        cs = rp(d, False)
        terms = [(c, d - i) for i, c in enumerate(cs)]
        R.shuffle(terms)
        shown = poly([0] * 0 + [0]) if False else None
        # 順番をばらばらに表示
        txt = ""
        for c, e in terms:
            body = ("" if abs(c) == 1 and e else str(abs(c))) + ("" if e == 0 else "x" + ("<sup>%d</sup>" % e if e > 1 else ""))
            txt = (("－" if c < 0 else "") + body) if not txt else txt + (" － " if c < 0 else " ＋ ") + body
        k = R.choice(["down", "up"])
        if k == "down":
            ans = poly(cs)
            w = [poly(cs[::-1]) if False else poly_up(cs), poly([-c for c in cs]), txt]
            q = "把 %s 按<b>降冪</b>排列。" % txt
            e = "降冪：次數由高到低排，符號跟著各項一起移動。"
        else:
            ans = poly_up(cs)
            w = [poly(cs), poly_up([-c for c in cs]), txt]
            q = "把 %s 按<b>升冪</b>排列。" % txt
            e = "升冪：次數由低到高排，符號跟著各項一起移動。"
        return mcq(q, ans, [x for x in w if x != ans] + [poly([cs[0]] + [abs(c) for c in cs[1:]]), poly([cs[0]] + [-c for c in cs[1:]]), poly_up([cs[0]] + [-c for c in cs[1:]]), poly([abs(c) for c in cs])], e)
    return pick_unique(R, mk, 20, seen)


def poly_up(cs):
    d = len(cs) - 1
    out = ""
    for i in range(d, -1, -1):
        c = cs[d - i] if False else cs[i]
    terms = [(cs[i], d - i) for i in range(d, -1, -1)]
    for c, e in terms:
        if c == 0:
            continue
        body = ("" if abs(c) == 1 and e else str(abs(c))) + ("" if e == 0 else "x" + ("<sup>%d</sup>" % e if e > 1 else ""))
        out = (("－" if c < 0 else "") + body) if not out else out + (" － " if c < 0 else " ＋ ") + body
    return out


def s3(seen):
    def mk():
        d = R.choice([1, 2, 2, 3])
        a, b = rp(d, False), rp(R.choice([d, max(1, d - 1)]), False)
        r = padd(a, b)
        q = "（%s）＋（%s）＝" % (poly(a), poly(b))
        return mcq(q, poly(r), [poly(padd(a, b, -1)), poly([x + 1 if i == 0 else x for i, x in enumerate(r)]), poly(padd(a, [abs(x) for x in b])), poly([x - 1 if i == len(r) - 1 else x for i, x in enumerate(r)]), poly([-x for x in r])], "同類項（次數相同的項）係數相加：%s。" % poly(r))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        d = R.choice([1, 2, 2, 3])
        a, b = rp(d, False), rp(R.choice([d, max(1, d - 1)]), False)
        r = padd(a, b, -1)
        if r == [0]:
            return None
        q = "（%s）－（%s）＝" % (poly(a), poly(b))
        bad = padd(a, [b[0]] + [-x for x in b[1:]], -1)
        return mcq(q, poly(r), [poly(padd(a, b)), poly(bad), poly([-x for x in r]), poly([x + 1 if i == len(r) - 1 else x for i, x in enumerate(r)])], "減法：括號前是負號，%s 的每一項都要變號再相加：%s。" % (poly(b), poly(r)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def val():
        cs = rp(2, False)
        x = nz(-4, 4)
        v = cs[0] * x * x + cs[1] * x + cs[2]
        q = "x ＝ %s 時，%s 的值是多少？" % (sn(x), poly(cs))
        return mcq(q, sn(v), [sn(cs[0] * 2 * x + cs[1] * x + cs[2]), sn(-cs[0] * x * x + cs[1] * x + cs[2]), sn(v + 1)], "代入：%s × %s<sup>2</sup> ＋ %s × %s ＋ %s ＝ %s。" % (par(cs[0]), par(x), par(cs[1]), par(x), par(cs[2]), sn(v)))

    def perim():
        a, b = [R.randint(1, 6), R.randint(1, 9)], [R.randint(1, 5), R.randint(-3, 6)]
        if b[1] == 0:
            return None
        q = "長方形的長是（%s）公分，寬是（%s）公分。周長是多少公分？" % (poly(a), poly(b))
        r = [2 * (a[0] + b[0]), 2 * (a[1] + b[1])]
        return mcq(q, "（%s）公分" % poly(r), ["（%s）公分" % poly(padd(a, b)), "（%s）公分" % poly([2 * (a[0] + b[0]), a[1] + b[1]]), "（%s）公分" % poly([a[0] * b[0], 0, a[1] * b[1]])], "2 ×［（%s）＋（%s）］＝ 2（%s）＝ %s。" % (poly(a), poly(b), poly(padd(a, b)), poly(r)))

    def missing():
        a, b = rp(2, False), rp(2, False)
        c = padd(a, b)
        q = "某多項式加上 %s 得到 %s，這個多項式是？" % (poly(b), poly(c))
        return mcq(q, poly(a), [poly(padd(c, b)), poly(padd(b, c, -1)), poly(padd(a, [1]))], "所求 ＝（%s）－（%s）＝ %s。" % (poly(c), poly(b), poly(a)))
    return pick_unique(R, val, 7, seen) + pick_unique(R, perim, 6, seen) + pick_unique(R, missing, 7, seen)


def main():
    seen = set()
    sets = [("多項式的名詞", s1(seen)), ("升冪與降冪", s2(seen)), ("多項式的加法", s3(seen)),
            ("多項式的減法", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["多項式 3x<sup>2</sup> － 5x ＋ 2：有 <b>3 項</b>，最高次項 3x<sup>2</sup>，是 <b>2 次</b>多項式；一次項係數 －5，常數項 2。",
         "<b>降冪</b>：次數由高到低排；<b>升冪</b>：由低到高排。符號要跟著那一項。",
         "加減法：只有<b>同類項</b>（次數相同）才能合併，把係數相加減。",
         "減法：括號前是負號，後面多項式的<b>每一項都要變號</b>。"],
        [example("（3x<sup>2</sup> － 2x ＋ 1）－（x<sup>2</sup> ＋ 4x － 5）", ["變號：3x<sup>2</sup> － 2x ＋ 1 － x<sup>2</sup> － 4x ＋ 5。", "合併同類項。"], "2x<sup>2</sup> － 6x ＋ 6")],
        [("3x<sup>2</sup> － 5x ＋ 2 的一次項係數是 5", "要連符號：－5"),
         ("減法只把第一項變號", "每一項都要變號"),
         ("2x<sup>2</sup> ＋ 3x ＝ 5x<sup>3</sup>", "次數不同不能合併")])
    faq = [{"q": "多項式的次數和項數有什麼不同？",
            "a": "次數是最高次項的次數，項數是有幾項。例如 x³ ＋ 1 是 3 次多項式，但只有 2 項。"},
           {"q": "多項式減法最常錯在哪裡？",
            "a": "忘了把後面括號裡每一項都變號。可以先寫成「加上它的相反數」，再合併同類項。"},
           {"q": "八年級的多項式要學什麼？",
            "a": "108課綱 A-8-2、A-8-3：一元多項式的名詞（項數、係數、常數項、升冪、降冪等），以及直式、橫式的加減法。"}]
    make_unit(R, "grade-8", "polynomials", "A-8-2",
              "多項式的意義：一元多項式的定義與相關名詞（多項式、項數、係數、常數項、一次項、二次項、最高次項、升冪、降冪）。",
              "多項式的名詞與加減",
              "八年級數學 多項式 練習題｜次數・係數・升冪降冪・加減法 學習單（附解答）",
              "多項式與加減",
              "國中八年級數學「多項式的名詞與加減」免費學習單：多項式的次數、項數、係數、常數項，升冪和降冪排列，多項式的加法、減法與求值、周長應用。100題線上練習馬上對答案，附可列印解答。",
              "只有同類項才能合併",
              "減法：後面多項式的每一項都要變號。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
