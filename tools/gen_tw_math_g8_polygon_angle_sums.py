# -*- coding: utf-8 -*-
"""
台灣 國中八年級 數學：多邊形的內角和與外角和（108課綱 S-8-2）
  python3 tools/gen_tw_math_g8_polygon_angle_sums.py
內角和（n － 2）× 180°、正 n 邊形の一つの內角・外角、內角和や一つの角から n を求める、外角和 360°、欠けた角、三角形の外角、正多邊形の舖滿。
誤答：n × 180° や（n － 1）× 180°、外角和を（n － 2）× 180° とする、內角と外角の取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, num
from tw_g7 import tidy_sets

R = random.Random(81019)
NAME = {3: "三角形", 4: "四邊形", 5: "五邊形", 6: "六邊形", 7: "七邊形", 8: "八邊形", 9: "九邊形", 10: "十邊形", 12: "十二邊形", 15: "十五邊形", 18: "十八邊形", 20: "二十邊形", 24: "二十四邊形", 30: "三十邊形", 36: "三十六邊形"}
REG = [n for n in NAME if 360 % n == 0]


def deg(x):
    return "%s°" % num(x)


def s1(seen):
    def mk():
        n = R.randint(4, 30)
        v = (n - 2) * 180
        q = "%d 邊形的內角和是多少度？" % n if n not in NAME else "%s的內角和是多少度？" % NAME[n]
        return mcq(q, deg(v), [deg(n * 180), deg((n - 1) * 180), deg(360), deg((n - 3) * 180)], "從一個頂點畫對角線，可分成 %d － 2 ＝ %d 個三角形：%d × 180° ＝ %s。" % (n, n - 2, n - 2, deg(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def inner():
        n = R.choice(REG[1:])
        v = (n - 2) * 180 // n
        q = "正%s的每一個內角是多少度？" % NAME[n]
        return mcq(q, deg(v), [deg(360 // n), deg(180 * n // n if False else (n - 2) * 180), deg(180 - v // 2), deg(v + 10)], "內角和 %s ÷ %d ＝ %s；或 180° － 外角 %s ＝ %s。" % (deg((n - 2) * 180), n, deg(v), deg(360 // n), deg(v)))

    def outer():
        n = R.choice(REG)
        v = 360 // n
        q = "正%s的每一個外角是多少度？" % NAME[n]
        return mcq(q, deg(v), [deg(180 - v), deg((n - 2) * 180 // n) if (n - 2) * 180 // n != 180 - v else deg(v * 2), deg(180 // n) if 180 % n == 0 else deg(v + 5), deg(v + 10)], "外角和是 360°：360° ÷ %d ＝ %s。" % (n, deg(v)))
    return pick_unique(R, inner, 10, seen) + pick_unique(R, outer, 10, seen)


def s3(seen):
    def from_sum():
        n = R.randint(5, 25)
        S = (n - 2) * 180
        q = "一個多邊形的內角和是 %s，它是幾邊形？" % deg(S)
        return mcq(q, "%d 邊形" % n, ["%d 邊形" % x for x in (n - 2, S // 180, n + 1, n - 1) if x != n], "（n － 2）× 180 ＝ %s，n － 2 ＝ %d，n ＝ %d。" % (num(S), n - 2, n))

    def from_ang():
        n = R.choice(REG[1:])
        kind = R.choice(["內", "外"])
        a = (n - 2) * 180 // n if kind == "內" else 360 // n
        q = "一個正多邊形的每一個%s角是 %s，它是正幾邊形？" % (kind, deg(a))
        e = 360 // n
        expl = "外角 ＝ 180° － %s ＝ %s，360° ÷ %s ＝ %d。" % (deg(a), deg(e), deg(e), n) if kind == "內" else "外角和 360°：360° ÷ %s ＝ %d。" % (deg(a), n)
        w = [360 // a if kind == "內" and 360 % a == 0 and 360 // a != n else n + 2, 180 // e if 180 % e == 0 and 180 // e != n else n - 1, n + 1]
        return mcq(q, "正 %d 邊形" % n, ["正 %d 邊形" % x for x in w if x >= 3], expl)
    return pick_unique(R, from_sum, 10, seen) + pick_unique(R, from_ang, 10, seen)


def s4(seen):
    def missing():
        n = R.choice([4, 5, 6, 7])
        S = (n - 2) * 180
        while True:
            angs = [R.randint(70, 175) for _ in range(n - 1)]
            x = S - sum(angs)
            if 40 <= x <= 175:
                break
        q = "%s的內角中有 %d 個是 %s，第 %d 個內角是多少度？" % (NAME[n], n - 1, "、".join(deg(a) for a in angs), n)
        return mcq(q, deg(x), [deg(x + 180) if x + 180 < 360 else deg(x - 20), deg(360 - sum(angs)) if 0 < 360 - sum(angs) else deg(x + 10), deg(180 - x), deg(x + 20)], "內角和 %s，%s － %s ＝ %s。" % (deg(S), deg(S), deg(sum(angs)), deg(x)))

    def ext():
        n = R.choice([4, 5, 6])
        while True:
            angs = [R.randint(30, 110) for _ in range(n - 1)]
            x = 360 - sum(angs)
            if 20 <= x <= 120:
                break
        q = "%s的外角中有 %d 個是 %s，最後一個外角是多少度？" % (NAME[n], n - 1, "、".join(deg(a) for a in angs), )
        return mcq(q, deg(x), [deg((n - 2) * 180 - sum(angs)), deg(180 - x), deg(x + 10), deg(x + 180)], "任何凸多邊形的外角和都是 360°：360° － %s ＝ %s。" % (deg(sum(angs)), deg(x)))
    return pick_unique(R, missing, 10, seen) + pick_unique(R, ext, 10, seen)


def s5(seen):
    def tri():
        a, b = R.randint(25, 85), R.randint(25, 85)
        if a + b >= 170:
            return None
        q = "△ABC 中，∠A ＝ %s，∠B ＝ %s，∠C 的外角是多少度？" % (deg(a), deg(b))
        return mcq(q, deg(a + b), [deg(180 - a - b), deg(360 - a - b), deg(abs(a - b) if a != b else a + 5), deg(a + b + 10)], "三角形的外角等於不相鄰兩個內角的和：%s ＋ %s ＝ %s。" % (deg(a), deg(b), deg(a + b)))

    def tile():
        n = R.choice([3, 4, 5, 6, 8, 10, 12])
        a = (n - 2) * 180 // n
        ok = 360 % a == 0
        q = "只用同一種正%s（每個內角 %s）能不能把地面舖滿、沒有空隙也不重疊？" % (NAME[n], deg(a))
        ans = "可以，%d 個拼在一點剛好 360°" % (360 // a) if ok else "不行，360° 不是 %s 的整數倍" % deg(a)
        w = ["不行，360° 不是 %s 的整數倍" % deg(a), "可以，%d 個拼在一點剛好 360°" % (360 // a + 1), "可以，只要邊長夠大", "不行，只有正方形可以"] if ok else ["可以，%d 個拼在一點剛好 360°" % (360 // a), "可以，%d 個拼在一點剛好 360°" % (360 // a + 1), "可以，只要邊長夠大", "不行，只有正方形可以"]
        return mcq(q, ans, w, "在一個點周圍拼起來要剛好 360°：360° ÷ %s %s。" % (deg(a), "＝ %d，可以" % (360 // a) if ok else "不是整數，不行"))

    def x_eq():
        n = R.choice([4, 5, 6])
        S = (n - 2) * 180
        k = R.randint(2, 4)
        rest = [R.randint(80, 140) for _ in range(n - 2)]
        rem = S - sum(rest)
        if rem % (k + 1):
            return None
        x = rem // (k + 1)
        if not 25 <= x <= 90 or k * x >= 180:
            return None
        q = "%s的內角是 %s、x°、%dx°，x 是多少？" % (NAME[n], "、".join(deg(r) for r in rest), k)
        return mcq(q, str(x), [str((360 - sum(rest)) // (k + 1)) if (360 - sum(rest)) > 0 and (360 - sum(rest)) // (k + 1) != x else str(x + 3), str(x + 5), str(k * x)], "內角和 %s：%s ＋ %dx ＝ %s，%dx ＝ %d，x ＝ %d。" % (deg(S), " ＋ ".join(map(str, rest)), k + 1, num(S), k + 1, rem, x))
    return pick_unique(R, tri, 7, seen) + pick_unique(R, tile, 6, seen) + pick_unique(R, x_eq, 7, seen)


def main():
    seen = set()
    sets = [("內角和", s1(seen)), ("正多邊形的內角和外角", s2(seen)), ("求邊數", s3(seen)),
            ("求缺少的角", s4(seen)), ("外角性質與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>n 邊形的內角和 ＝（n － 2）× 180°</b>：從一個頂點畫對角線，可分成 n － 2 個三角形。",
         "<b>凸多邊形的外角和永遠是 360°</b>，和邊數無關。每個內角 ＋ 它的外角 ＝ 180°。",
         "正 n 邊形：每個外角 ＝ 360° ÷ n，每個內角 ＝ 180° － 外角。",
         "三角形的一個外角 ＝ 不相鄰的兩個內角的和。"],
        [example("正十二邊形的每個內角？", ["外角 360° ÷ 12 ＝ 30°。", "內角 180° － 30° ＝ 150°。"], "150°"),
         example("內角和是 1440° 的多邊形？", ["（n － 2）× 180 ＝ 1440，n － 2 ＝ 8。"], "十邊形")],
        [("五邊形內角和 ＝ 5 × 180°", "是（5 － 2）× 180° ＝ 540°"),
         ("邊數越多外角和越大", "外角和永遠是 360°"),
         ("正六邊形每個內角 ＝ 60°", "60° 是外角，內角是 120°")])
    faq = [{"q": "為什麼外角和一定是 360°？",
            "a": "沿著多邊形走一圈，每到一個頂點就轉一個外角，走回起點剛好轉了一整圈，就是 360°。"},
           {"q": "哪些正多邊形可以舖滿地面？",
            "a": "只有正三角形（60°）、正方形（90°）、正六邊形（120°），因為它們的內角能整除 360°。"},
           {"q": "八年級的多邊形角度要學什麼？",
            "a": "108課綱 S-8-2：凸多邊形的內角和外角和，以及正多邊形的每個內角和外角。"}]
    make_unit(R, "grade-8", "polygon-angle-sums", "S-8-2",
              "凸多邊形的內角和：凸多邊形的意義；內角與外角的意義；凸多邊形的內角和公式；正 n 邊形的每個內角度數。",
              "多邊形的內角和與外角和",
              "八年級數學 多邊形內角和 練習題｜外角和・正多邊形 學習單（附解答）",
              "多邊形內角和",
              "國中八年級數學「多邊形的內角和與外角和」免費學習單：內角和（n－2）×180°、正多邊形的內角和外角、由角度求邊數、求缺少的角、三角形外角與舖滿地面。100題線上練習馬上對答案，附可列印解答。",
              "內角和 ＝（n － 2）× 180°，外角和 ＝ 360°",
              "正 n 邊形：外角 360° ÷ n，內角 180° － 外角。",
              body, faq, sets, 19)


if __name__ == "__main__":
    main()
