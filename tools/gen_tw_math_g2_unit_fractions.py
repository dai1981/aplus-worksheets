# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：認識單位分數（108課綱 N-2-10）
  python3 tools/gen_tw_math_g2_unit_fractions.py
等分した一つ分（幾分之一）、塗った部分の分數、等分かどうか、分母が大きいほど一つ分は小さい、二分之一・四分之一の量（8 個の 1/2）。
誤答：等分していないのに 1/2 とする、塗っていない部分の數を分母にする、分母が大きいほど大きいとする。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g7 import tidy_sets
import tw_pics as P
from ws_common import svg_wrap, fig, INK

R = random.Random(81311)
ZH = {2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 8: "八"}


def F1(n):
    return fr(1, n)


def s1(seen):
    def mk():
        n = R.choice([2, 3, 4, 5, 6, 8])
        kind = R.choice(["circle", "rect", "square"]) if n in (2, 4) else R.choice(["circle", "rect"])
        size = R.choice([40, 46, 52])
        q = "塗色的部分是整個的幾分之一？" + P.frac(kind, n, 1, size)
        return mcq(q, "%s分之一（%s）" % (ZH[n], F1(n)), R.sample(["%s分之一（%s）" % (ZH[x], F1(x)) for x in (2, 3, 4, 5, 6, 8) if x != n], 3), "平分成 %d 份，塗了 1 份，是%s分之一。" % (n, ZH[n]))
    return pick_unique(R, mk, 20, seen)


def uneq_svg(n):
    """等分していない長方形"""
    W = 180
    cuts = sorted(R.sample(range(20, 160), n - 1))
    s = ["<rect x='8' y='8' width='%d' height='70' fill='white' stroke='%s' stroke-width='1.6'/>" % (W, INK),
         "<rect x='8' y='8' width='%d' height='70' fill='#7fb3e6' stroke='%s' stroke-width='1.6'/>" % (cuts[0], INK)]
    for c in cuts:
        s.append("<line x1='%d' y1='8' x2='%d' y2='78' stroke='%s' stroke-width='1.6'/>" % (8 + c, 8 + c, INK))
    return fig(svg_wrap(W + 16, 86, "".join(s), "沒有平分的長方形"))


def s2(seen):
    def mk():
        n = R.choice([2, 3, 4])
        if R.random() < .5:
            q = "塗色的部分是整個的 %s 嗎？" % F1(n) + P.frac(R.choice(["rect", "circle"]), n, 1)
            return mcq(q, "是，因為平分成 %d 份" % n, ["不是，因為沒有平分", "不是，要數塗色的有幾個", "是，因為有 %d 條線" % (n + 1)], "每一份一樣大（平分），塗 1 份，是 %s。" % F1(n))
        cuts = None
        q = "塗色的部分是整個的 %s 嗎？" % F1(n) + uneq_svg(n)
        return mcq(q, "不是，因為沒有平分", ["是，因為分成 %d 份" % n, "是，因為塗了 1 份", "不是，因為塗太少"], "分成 %d 份，但每一份不一樣大，不是平分，所以不能說是 %s。" % (n, F1(n)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.sample([2, 3, 4, 5, 6, 8], 2)
        k = R.choice(["大", "小"])
        v = min(a, b) if k == "大" else max(a, b)
        q = "一個蛋糕的 %s 和 %s，哪一個比較%s？" % (F1(a), F1(b), k)
        return mcq(q, F1(v), [F1(max(a, b) if k == "大" else min(a, b)), "一樣大", "不能比"], "同一個東西，分的份數越多，每一份越小：%s 比較%s。" % (F1(v), k))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        n = R.choice([2, 3, 4])
        per = R.randint(2, 5)
        tot = n * per
        k = R.choice(P.KINDS)
        q = "%d %s%s的 %s 是幾%s？" % (tot, P.cl(k), P.nm(k), F1(n), P.cl(k)) + P.row(tot, k, per_row=per * 2 if per * 2 <= 10 else per)
        return mcq(q, "%d %s" % (per, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (n, tot - per, per + 1) if x != per] + ["%d %s" % (per + 2, P.cl(k))], "平分成 %d 份，一份是 %d %s。" % (n, per, P.cl(k)))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        n = R.choice([2, 3, 4, 5, 6, 8])
        what = R.choice([("一個披薩", "片"), ("一條吐司", "片"), ("一張色紙", "張"), ("一個西瓜", "塊"), ("一條繩子", "段")])
        k = R.choice(["name", "how"])
        if k == "name":
            q = "%s平分成 %d %s，拿走 1 %s，拿走的是整個的幾分之幾？" % (what[0], n, what[1], what[1])
            return mcq(q, F1(n), [F1(x) for x in (2, 3, 4, 5, 6, 8) if x != n][:2] + [fr(n - 1, n) if n > 2 else F1(4)], "平分成 %d 份，拿 1 份，是 %s。" % (n, F1(n)))
        q = "要把%s分成 %s，要怎麼做？" % (what[0], F1(n))
        return mcq(q, "平分成 %d 份，取 1 份" % n, ["隨便切成 %d 份，取 1 份" % n, "平分成 %d 份，取 1 份" % (n + 1), "切 %d 刀就好，大小不用管" % (n - 1)], "%s 是平分成 %d 份中的 1 份，每份要一樣大。" % (F1(n), n))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("看圖說幾分之一", s1(seen)), ("是不是平分", s2(seen)), ("比大小", s3(seen)),
            ("一堆東西的幾分之一", s4(seen)), ("生活中的幾分之一", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["把一個東西<b>平分</b>（每份一樣大）成 4 份，1 份就是<b>四分之一</b>，寫成 %s。" % F1(4) + P.frac("circle", 4, 1),
         "%s 下面的 4 是平分成幾份（分母），上面的 1 是取 1 份（分子）。" % F1(4),
         "同一個東西，<b>分的份數越多，一份越小</b>：%s 比 %s 小。" % (F1(4), F1(2))],
        [example("一條繩子平分成 3 段，1 段是多少？", ["平分 3 份，取 1 份。"], F1(3)),
         example("8 顆糖的 %s 是幾顆？" % F1(2), ["平分成 2 份，一份 4 顆。"], "4 顆")],
        [("沒有平分也說是 %s" % F1(2), "每份要一樣大才行"),
         ("%s 比 %s 大，因為 4 比 2 大" % (F1(4), F1(2)), "分越多份，每份越小"),
         ("分成 3 份、取 1 份，寫成 %s" % fr(1, 2), "分母寫份數：%s" % F1(3))])
    faq = [{"q": "二年級要學到哪些分數？",
            "a": "108課綱 N-2-10：從平分（例如摺紙）認識單位分數「幾分之一」，三年級再學幾分之幾、同分母分數加減。"},
           {"q": "為什麼一定要平分？",
            "a": "分數表示「一樣大的份中的幾份」，沒有平分，每份大小不同，就不能用分數來說。"},
           {"q": "在家怎麼練？",
            "a": "摺紙、切蛋糕、分披薩時，讓孩子平分，再說出一份是幾分之一。"}]
    make_unit(R, "grade-2", "unit-fractions", "N-2-10",
              "單位分數的認識：從等分配的活動（如摺紙）認識單部分為全部的「幾分之一」。知道日常語言「的一半」、「的二分之一」、「的四分之一」的溝通意義。在已等分割之格圖中，辨識單位分數。",
              "認識幾分之一（單位分數）",
              "二年級數學 分數 練習題｜幾分之一・平分・比大小 學習單（附解答）",
              "幾分之一",
              "國小二年級數學「認識幾分之一」免費學習單：看圖說幾分之一、判斷是不是平分、比較單位分數的大小、一堆東西的幾分之一、生活中的幾分之一。100題線上練習，圖多，附可列印解答。",
              "平分成 4 份，1 份是 1/4",
              "分的份數越多，一份越小。",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
