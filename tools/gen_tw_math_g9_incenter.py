# -*- coding: utf-8 -*-
"""
台灣 國中九年級 數學：三角形的內心（108課綱 S-9-9）
  python3 tools/gen_tw_math_g9_incenter.py
內心＝三內角の角平分線の交點、三邊まで等距離（內切圓の半徑）、∠BIC ＝ 90° ＋ ∠A/2、面積 ＝ 周長 × r ÷ 2、直角三角形の r ＝（兩股和 － 斜邊）÷ 2、正三角形。
誤答：內心と外心の取り違え、∠BIC を 2∠A にする、面積で ÷ 2 を忘れる。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, fr
from tw_g7 import tidy_sets
from tw_g9 import ov, pi

R = random.Random(81110)
TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25), (15, 20, 25), (10, 24, 26), (20, 21, 29), (12, 35, 37), (9, 40, 41), (16, 30, 34), (18, 24, 30)]


def s1(seen):
    FACTS = [("三角形的內心是哪三條線的交點？", "三個內角的角平分線", ["三邊的中垂線", "三條中線", "三條高"], "內心是三個內角平分線的交點。"),
             ("三角形的內心到什麼的距離相等？", "三邊", ["三個頂點", "三邊的中點", "外心"], "角平分線上的點到角的兩邊等距，所以內心到三邊等距。"),
             ("三角形的內心一定在哪裡？", "三角形內部", ["三角形外部", "最長邊上", "看是什麼三角形"], "不論銳角、直角、鈍角三角形，內心都在內部。"),
             ("以內心為圓心、到一邊的距離為半徑畫的圓叫什麼？", "內切圓", ["外接圓", "同心圓", "單位圓"], "這個圓和三邊都相切，叫內切圓。"),
             ("要在三角形公園裡放一個和三邊圍牆都一樣近的涼亭，應放在哪裡？", "內心", ["外心", "重心", "最長邊的中點"], "到三邊等距的點是內心。"),
             ("在三角形木板上割出最大的圓，圓心是三角形的哪一個心？", "內心", ["外心", "重心", "任一頂點"], "最大的圓是內切圓，圓心是內心。")]
    out = [mcq(*f) for f in FACTS]
    for b in out:
        seen.add(b["q"])

    def half():
        a, b = R.randint(30, 100), R.randint(30, 100)
        if a % 2 or b % 2 or a + b >= 170:
            return None
        q = "△ABC 的內心是 I，∠ABC ＝ %d°，∠ACB ＝ %d°，∠IBC ＋ ∠ICB 是多少度？" % (a, b)
        v = (a + b) // 2
        return mcq(q, "%d°" % v, ["%d°" % x for x in (a + b, 180 - v, 90 - v if 90 - v != v else v + 10)], "BI、CI 平分 ∠B、∠C：%d° ÷ 2 ＋ %d° ÷ 2 ＝ %d°。" % (a, b, v))
    return out + pick_unique(R, half, 14, seen)


def s2(seen):
    def mk():
        a = R.randrange(20, 141, 2)
        t = R.choice(["BIC", "A"])
        if t == "BIC":
            q = "△ABC 的內心是 I，∠A ＝ %d°，∠BIC 是多少度？" % a
            v = 90 + a // 2
            return mcq(q, "%d°" % v, ["%d°" % x for x in (2 * a if 2 * a < 180 else a, 180 - a, 90 - a // 2)], "∠BIC ＝ 180° －（∠B ＋ ∠C）÷ 2 ＝ 90° ＋ ∠A ÷ 2 ＝ 90° ＋ %d° ＝ %d°。" % (a // 2, v))
        v = 90 + a // 2
        q = "△ABC 的內心是 I，∠BIC ＝ %d°，∠A 是多少度？" % v
        return mcq(q, "%d°" % a, ["%d°" % x for x in (v - 90, 180 - v, v // 2)], "90° ＋ ∠A ÷ 2 ＝ %d°，∠A ÷ 2 ＝ %d°，∠A ＝ %d°。" % (v, v - 90, a))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def area():
        r = R.randint(1, 8)
        P = R.randint(6, 40) * 2
        q = "三角形的周長是 %d，內切圓半徑是 %d，三角形的面積是多少？" % (P, r)
        return mcq(q, str(P * r // 2), [str(P * r), str(P // 2 + r), str(P * r // 4) if P * r % 4 == 0 else str(P * r // 2 + 1)], "連內心和三頂點分成三個三角形，高都是 r：面積 ＝ 周長 × r ÷ 2 ＝ %d × %d ÷ 2 ＝ %d。" % (P, r, P * r // 2))

    def rfrom():
        r = R.randint(1, 8)
        P = R.randint(6, 40) * 2
        A = P * r // 2
        q = "三角形的面積是 %d，周長是 %d，內切圓半徑是多少？" % (A, P)
        return mcq(q, str(r), [str(r * 2), str(A // P) if A // P != r and A % P == 0 else str(r + 1), str(P // r if P // r != r else r + 2)], "面積 ＝ 周長 × r ÷ 2：%d ＝ %d × r ÷ 2，r ＝ %d。" % (A, P, r))
    return pick_unique(R, area, 10, seen) + pick_unique(R, rfrom, 10, seen)


def s4(seen):
    def right():
        a, b, c = R.choice(TRIP)
        q = "直角三角形的兩股是 %d 和 %d，內切圓半徑是多少？" % (a, b)
        r = F(a + b - c, 2)
        rs = str(r) if r.denominator == 1 else "%g" % float(r)
        return mcq(q, rs, ["%g" % x for x in (c / 2, (a + b - c), a * b / (a + b + c) * 2)], "斜邊 %d，r ＝（兩股和 － 斜邊）÷ 2 ＝（%d ＋ %d － %d）÷ 2 ＝ %s。（也可以用 面積 ＝ 周長 × r ÷ 2）" % (c, a, b, c, rs))

    def eq():
        k = R.randint(1, 10)
        a = 6 * k
        q = "邊長 %d 的正三角形，內切圓半徑是多少？" % a
        r = "%d√3" % k if k > 1 else "√3"
        return mcq(q, r, ["%d√3" % (2 * k), "%d√3" % (3 * k), "%d" % (3 * k)], "正三角形的內心也是重心，r ＝ 高的 <span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span>：高 %d√3，r ＝ %s。" % (3 * k, r))
    return pick_unique(R, right, 12, seen) + pick_unique(R, eq, 8, seen)


def s5(seen):
    def tangent():
        x, y, z = R.randint(2, 12), R.randint(2, 12), R.randint(2, 12)
        a, b, c = y + z, x + z, x + y
        q = "△ABC 的內切圓和 %s、%s、%s 分別切於 D、E、F，%s ＝ %d、%s ＝ %d、%s ＝ %d，%s 是多少？" % (ov("BC"), ov("CA"), ov("AB"), ov("BC"), a, ov("CA"), b, ov("AB"), c, ov("AF"))
        return mcq(q, str(x), [str(y), str(z), str((a + b + c) // 2) if (a + b + c) // 2 not in (x, y, z) else str(x + 1)], "切線段等長：%s ＝（%s ＋ %s － %s）÷ 2 ＝（%d ＋ %d － %d）÷ 2 ＝ %d。" % (ov("AF"), ov("AB"), ov("AC"), ov("BC"), c, b, a, x))

    def circle_area():
        a, b, c = R.choice(TRIP[:10])
        r = F(a + b - c, 2)
        q = "直角三角形的兩股是 %d 和 %d，內切圓的面積是多少？" % (a, b)
        return mcq(q, pi(r * r), [pi(2 * r), pi(F(c * c, 4)), pi(r * r * 4)], "r ＝（%d ＋ %d － %d）÷ 2 ＝ %g，面積 ＝ π × %g<sup>2</sup> ＝ %s。" % (a, b, c, float(r), float(r), pi(r * r)))
    return pick_unique(R, tangent, 12, seen) + pick_unique(R, circle_area, 8, seen)


def main():
    seen = set()
    sets = [("認識內心", s1(seen)), ("內心與角度", s2(seen)), ("面積與內切圓半徑", s3(seen)),
            ("直角三角形與正三角形", s4(seen)), ("切線段與內切圓", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["三角形<b>三個內角平分線的交點叫內心</b>。內心到三邊的距離相等，是內切圓的圓心，一定在三角形內部。",
         "內心 I：<b>∠BIC ＝ 90° ＋ ∠A ÷ 2</b>。",
         "<b>三角形面積 ＝ 周長 × r ÷ 2</b>（r 是內切圓半徑）；直角三角形 <b>r ＝（兩股和 － 斜邊）÷ 2</b>。"],
        [example("內心 I，∠A ＝ 70°，∠BIC？", ["90° ＋ 35°。"], "125°"),
         example("直角三角形兩股 6、8，內切圓半徑？", ["斜邊 10。", "（6 ＋ 8 － 10）÷ 2。"], "2")],
        [("內心到三個頂點等距", "到三邊等距；到頂點等距的是外心"),
         ("∠BIC ＝ 2∠A", "那是外心；內心是 90° ＋ ∠A ÷ 2"),
         ("面積 ＝ 周長 × r", "還要 ÷ 2")])
    faq = [{"q": "內心和外心怎麼分？",
            "a": "內心：角平分線的交點，到三邊等距，內切圓圓心，一定在內部。外心：中垂線的交點，到三頂點等距，外接圓圓心，位置看三角形的種類。"},
           {"q": "為什麼面積 ＝ 周長 × r ÷ 2？",
            "a": "把內心連到三個頂點，分成三個三角形，底分別是三邊、高都是 r，加起來是（a ＋ b ＋ c）× r ÷ 2。"},
           {"q": "九年級的內心要學什麼？",
            "a": "108課綱 S-9-9：內心的意義與內切圓，內心到三邊等距，面積 ＝ 周長 × 內切圓半徑 ÷ 2，直角三角形內切圓半徑 ＝（兩股和 － 斜邊）÷ 2。"}]
    make_unit(R, "grade-9", "incenter", "S-9-9",
              "三角形的內心：內心的意義與內切圓；三角形的內心到三角形的三邊等距；三角形的面積＝周長×內切圓半徑÷2；直角三角形的內切圓半徑＝（兩股和－斜邊）÷2。",
              "三角形的內心與內切圓",
              "九年級數學 三角形內心 練習題｜內切圓半徑・角平分線・∠BIC 學習單（附解答）",
              "內心",
              "國中九年級數學「三角形的內心與內切圓」免費學習單：內心是角平分線的交點、到三邊等距、∠BIC＝90°＋∠A÷2、面積＝周長×r÷2、直角三角形與正三角形的內切圓半徑、切線段。100題線上練習馬上對答案，附可列印解答。",
              "內心到三邊等距",
              "面積 ＝ 周長 × r ÷ 2；∠BIC ＝ 90° ＋ ∠A ÷ 2。",
              body, faq, sets, 10)


if __name__ == "__main__":
    main()
