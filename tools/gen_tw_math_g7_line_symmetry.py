# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：線對稱的性質與圖形（108課綱 S-7-4、S-7-5）
  python3 tools/gen_tw_math_g7_line_symmetry.py
對稱線段等長・對稱角相等・對稱點の連線は對稱軸で垂直平分される、等腰三角形・正方形・菱形・箏形・正多邊形の對稱軸の數、性質で長さ・角度を求める、坐標での對稱。
誤答：平行四邊形を線對稱とする、長方形の對稱軸に對角線を含める、對稱點までの距離を片側だけで答える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import sn, tidy_sets

R = random.Random(71024)
NM = Names(R)

AXES = [("等腰三角形（不是正三角形）", "1 條"), ("正三角形", "3 條"), ("正方形", "4 條"), ("長方形（不是正方形）", "2 條"),
        ("菱形（不是正方形）", "2 條"), ("箏形", "1 條"), ("正五邊形", "5 條"), ("正六邊形", "6 條"), ("正八邊形", "8 條"),
        ("平行四邊形（不是長方形或菱形）", "0 條"), ("圓", "無限多條"), ("等腰梯形", "1 條"),
        ("等腰直角三角形", "1 條"), ("三邊都不等長的三角形", "0 條"), ("半圓", "1 條")]


def s1(seen):
    out = []
    for name, ans in AXES:
        w = [x for x in ("0 條", "1 條", "2 條", "3 條", "4 條", "6 條", "無限多條") if x != ans]
        R.shuffle(w)
        ex = {"0 條": "%s怎麼對折都無法完全重合，不是線對稱圖形。" % name, "無限多條": "通過圓心的每一條直線都是對稱軸。"}.get(ans, "%s有 %s對稱軸。" % (name, ans))
        out.append(mcq("%s有幾條對稱軸？" % name, ans, w[:3], ex))
    for o in out:
        seen.add(o["q"])

    def reg():
        n = R.randint(7, 12)
        if n == 8:
            return None
        names = {7: "七", 9: "九", 10: "十", 11: "十一", 12: "十二"}
        return mcq("正%s邊形有幾條對稱軸？" % names[n], "%d 條" % n, ["%d 條" % x for x in (n // 2, n - 1, 2 * n)], "正 n 邊形有 n 條對稱軸。")
    return out + pick_unique(R, reg, 5, seen)


def s2(seen):
    T = ["對稱軸兩邊的對應線段長度相等。", "對稱軸兩邊的對應角相等。", "兩個對稱點的連線段被對稱軸垂直平分。", "線對稱圖形沿對稱軸對折，兩邊會完全重合。", "正方形的兩條對角線都是對稱軸。", "菱形的兩條對角線都是對稱軸。"]
    Fz = ["長方形的兩條對角線都是對稱軸。", "平行四邊形一定是線對稱圖形。", "兩個對稱點的連線和對稱軸平行。", "線對稱圖形一定只有一條對稱軸。", "對稱角的度數一定是 90 度。", "等腰三角形有 3 條對稱軸。"]

    def mk():
        L = "甲乙丙丁"
        ok = R.random() < .5
        ans = R.choice(T if ok else Fz)
        st = R.sample(Fz if ok else T, 3) + [ans]
        R.shuffle(st)
        k = st.index(ans)
        q = "下面哪一句話是<b>%s</b>的？<br>" % ("對" if ok else "錯") + "<br>".join("%s：%s" % (L[i], t) for i, t in enumerate(st))
        return mcq(q, L[k], [x for x in L if x != L[k]], "%s：%s線對稱的性質：對稱線段等長、對稱角相等、對稱點連線被對稱軸垂直平分。" % (L[k], ans))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def ang():
        a = R.randint(20, 80)
        name = R.choice(["等腰三角形 ABC（AB ＝ AC）的對稱軸是 AD", "箏形 ABCD（AB ＝ AD、CB ＝ CD）的對稱軸是 AC"])
        if "三角形" in name:
            q = "%s。∠B ＝ %d°，∠C ＝ ？" % (name, a)
            return mcq(q, "%d°" % a, ["%d°" % x for x in (180 - 2 * a, 90 - a, 180 - a)  if x != a and x > 0] + ["%d°" % (a + 10)], "∠B 和 ∠C 是對稱角，相等：∠C ＝ %d°。" % a)
        q = "%s。∠ABC ＝ %d°，∠ADC ＝ ？" % (name, a + 40)
        return mcq(q, "%d°" % (a + 40), ["%d°" % x for x in (180 - a - 40, 360 - 2 * (a + 40), a)  if x > 0 and x != a + 40], "B 和 D 對稱於 AC，∠ABC 和 ∠ADC 是對稱角，相等。")

    def length():
        d = R.randint(3, 20)
        k = R.choice(["half", "dist", "seg"])
        if k == "half":
            q = "P、P′ 對稱於直線 L，PP′ 交 L 於 M，PP′ ＝ %d。PM ＝ ？" % (2 * d)
            return mcq(q, str(d), [str(2 * d), str(d + 1), str(4 * d)], "對稱點的連線被對稱軸平分：PM ＝ %d ÷ 2 ＝ %d。" % (2 * d, d))
        if k == "dist":
            q = "點 P 到對稱軸 L 的距離是 %d，P 的對稱點是 P′。PP′ ＝ ？" % d
            return mcq(q, str(2 * d), [str(d), str(d + 2), str(d * d) if d * d != 2 * d else str(3 * d)], "P′ 在 L 的另一邊，距離也是 %d：PP′ ＝ %d × 2 ＝ %d。" % (d, d, 2 * d))
        q = "四邊形 ABCD 對稱於直線 AC，AB ＝ %d、BC ＝ %d。周長是多少？" % (d, d + 3)
        return mcq(q, str(2 * (2 * d + 3)), [str(2 * d + 3), str(4 * d), str(4 * (d + 3))], "對稱線段等長：AD ＝ AB ＝ %d，CD ＝ CB ＝ %d，周長 2 ×（%d ＋ %d）＝ %d。" % (d, d + 3, d, d + 3, 2 * (2 * d + 3)))
    return pick_unique(R, ang, 10, seen) + pick_unique(R, length, 10, seen)


def s4(seen):
    def mk():
        x, y = R.randint(-8, 8), R.randint(-8, 8)
        a = R.randint(-5, 5)
        k = R.choice(["v", "h"])
        if k == "v":
            if x == a:
                return None
            nx = 2 * a - x
            q = "點 P（%s, %s）對稱於直線 x ＝ %s 的點是？" % (sn(x), sn(y), sn(a))
            ans = "（%s, %s）" % (sn(nx), sn(y))
            w = ["（%s, %s）" % (sn(-x), sn(y)), "（%s, %s）" % (sn(x), sn(2 * a - y)), "（%s, %s）" % (sn(nx), sn(-y)) if y else "（%s, 1）" % sn(nx)]
            e = "對稱軸是鉛垂線，y 不變；x 到 %s 的距離是 %d，對稱點在另一邊：x ＝ %s。" % (sn(a), abs(x - a), sn(nx))
        else:
            if y == a:
                return None
            ny = 2 * a - y
            q = "點 P（%s, %s）對稱於直線 y ＝ %s 的點是？" % (sn(x), sn(y), sn(a))
            ans = "（%s, %s）" % (sn(x), sn(ny))
            w = ["（%s, %s）" % (sn(x), sn(-y)), "（%s, %s）" % (sn(2 * a - x), sn(y)), "（%s, %s）" % (sn(-x), sn(ny)) if x else "（1, %s）" % sn(ny)]
            e = "對稱軸是水平線，x 不變；y 到 %s 的距離是 %d，對稱點在另一邊：y ＝ %s。" % (sn(a), abs(y - a), sn(ny))
        return mcq(q, ans, [t for t in w if t != ans] + ["（%s, %s）" % (sn(y), sn(x))], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def word():
        F_ = [("下面哪一個英文大寫字母是線對稱圖形？", "A", ["F", "G", "R"], "A 沿中間的鉛垂線對折可以重合。"),
              ("下面哪一個英文大寫字母有兩條對稱軸？", "H", ["A", "M", "T"], "H 有水平和鉛垂兩條對稱軸。"),
              ("下面哪一個國字是線對稱圖形？", "中", ["你", "我", "好"], "「中」左右對稱。"),
              ("下面哪一個英文大寫字母不是線對稱圖形？", "N", ["O", "X", "E"], "N 怎麼對折都不能重合。"),
              ("等腰三角形的對稱軸會把底邊怎麼樣？", "垂直平分", ["分成 1：2", "平行", "不一定"], "頂點和底邊中點的連線就是對稱軸，和底邊垂直。"),
              ("箏形的對稱軸是哪一條？", "連接兩組等長鄰邊交點的對角線", ["兩條對角線都是", "任意一條對角線", "沒有對稱軸"], "箏形只有一條對稱軸。"),
              ("正方形和菱形都有的對稱軸是？", "兩條對角線", ["兩組對邊中點的連線", "只有一條", "沒有"], "菱形的對稱軸是兩條對角線；正方形還多兩條。"),
              ("一個線對稱圖形，對稱軸上的點的對稱點是？", "它自己", ["不存在", "原點", "對稱軸外的某一點"], "對稱軸上的點到軸的距離是 0，對稱點就是自己。")]
        return mcq(*R.choice(F_))

    def isos():
        a = R.randint(30, 80)
        b = (180 - a)
        if b % 2:
            return None
        q = "等腰三角形的頂角是 %d°，對稱軸把頂角分成兩個角。每個角是幾度？底角是幾度？" % a
        ans = "%d°；%d°" % (a // 2 if a % 2 == 0 else 0, b // 2)
        if a % 2:
            return None
        return mcq(q, ans, ["%d°；%d°" % (a, b // 2), "%d°；%d°" % (a // 2, b), "%d°；%d°" % (b // 2, a // 2)], "對稱軸平分頂角：%d ÷ 2 ＝ %d；兩底角是對稱角，相等：（180 － %d）÷ 2 ＝ %d。" % (a, a // 2, a, b // 2))
    return pick_unique(R, word, 8, seen) + pick_unique(R, isos, 12, seen)


def main():
    seen = set()
    sets = [("對稱軸的數量", s1(seen)), ("線對稱的性質", s2(seen)), ("用性質求角和長度", s3(seen)),
            ("坐標上的對稱", s4(seen)), ("綜合", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["沿一條直線對折能完全重合的圖形叫<b>線對稱圖形</b>，這條直線是<b>對稱軸</b>。",
         "性質：<b>對稱線段等長</b>、<b>對稱角相等</b>、<b>對稱點的連線段被對稱軸垂直平分</b>。",
         "對稱軸數量：等腰三角形 1、正三角形 3、正方形 4、長方形 2、菱形 2、箏形 1、正 n 邊形 n、圓無限多；一般平行四邊形 0。"],
        [example("等腰三角形頂角 40°，底角？", ["兩底角對稱，相等。", "（180 － 40）÷ 2。"], "70°"),
         example("P（3, 2）對稱於 x ＝ 1 的點？", ["3 在 1 的右邊 2 格。", "另一邊 2 格：－1。"], "（－1, 2）")],
        [("長方形的對角線是對稱軸", "長方形的對稱軸是兩組對邊中點的連線"),
         ("平行四邊形是線對稱圖形", "一般的平行四邊形沒有對稱軸"),
         ("P 到軸距離 5，PP′ ＝ 5", "PP′ ＝ 5 × 2 ＝ 10")])
    faq = [{"q": "線對稱圖形有哪些性質？",
            "a": "對稱線段等長、對稱角相等，而且兩個對稱點的連線段會被對稱軸垂直平分。"},
           {"q": "為什麼長方形的對角線不是對稱軸？",
            "a": "沿對角線對折時，兩邊不會完全重合（除非是正方形），所以長方形只有兩條對稱軸：兩組對邊中點的連線。"},
           {"q": "七年級的線對稱要學什麼？",
            "a": "108課綱 S-7-4、S-7-5：線對稱的性質，以及等腰三角形、正方形、菱形、箏形、正多邊形等線對稱基本圖形。"}]
    make_unit(R, "grade-7", "line-symmetry", "S-7-4",
              "線對稱的性質：對稱線段等長；對稱角相等；對稱點的連線段會被對稱軸垂直平分。",
              "線對稱的性質與圖形",
              "七年級數學 線對稱 練習題｜對稱軸・等腰三角形・箏形・菱形 學習單（附解答）",
              "線對稱",
              "國中七年級數學「線對稱的性質與圖形」免費學習單：各種圖形的對稱軸數量、線對稱的性質、用對稱求角度和長度、坐標上的對稱點與綜合題。100題線上練習馬上對答案，附可列印解答。",
              "對稱點的連線被對稱軸垂直平分",
              "對稱線段等長，對稱角相等。",
              body, faq, sets, 24)


if __name__ == "__main__":
    main()
