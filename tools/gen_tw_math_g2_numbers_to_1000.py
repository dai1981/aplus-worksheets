# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：1000 以內的數（108課綱 N-2-1）
  python3 tools/gen_tw_math_g2_numbers_to_1000.py
百・十・一の積木、幾個百幾個十幾個一、位値（百位・十位・個位、0 のある數）、數の順序（10 ずつ・100 ずつ）、比大小、生活の場面。
誤答：0 を落とす（3 個百 5 個一 → 35）、位を取り違える、10 ずつと 1 ずつの取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81301)


def s1(seen):
    def mk():
        h, t, o = R.randint(1, 5), R.randint(0, 6), R.randint(0, 9)
        n = 100 * h + 10 * t + o
        q = "一片是 100，一條是 10，一小塊是 1。一共是多少？" + P.blocks(h, t, o)
        w = [h + t + o, 100 * h + 10 * o + t if o != t else n + 10, n + 100, n - 1 if n > 100 else n + 1]
        return mcq(q, str(n), [str(x) for x in w if x != n][:3], "%d 個百、%d 個十、%d 個一：%d。" % (h, t, o, n))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        h, t, o = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9)
        if R.random() < .4:
            t = 0
        n = 100 * h + 10 * t + o
        q = "%d 個百、%d 個十和 %d 個一合起來是多少？" % (h, t, o)
        w = [int("%d%d" % (h, o)) if t == 0 and o else n + 10, h + t + o, 100 * h + 10 * o + t if o != t else n + 1, n + 100 if n < 900 else n - 100]
        return mcq(q, str(n), [str(x) for x in w if x != n][:3], "百位 %d、十位 %d、個位 %d：%d。%s" % (h, t, o, n, "十位是 0 也要寫。" if t == 0 else ""))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        n = R.randint(101, 999)
        h, t, o = n // 100, n // 10 % 10, n % 10
        k = R.choice(["百位", "十位", "個位"])
        v = {"百位": h, "十位": t, "個位": o}[k]
        q = "%d 的%s數字是多少？" % (n, k)
        return mcq(q, str(v), [str(x) for x in (h, t, o, v + 1) if x != v][:3] + [str(v + 2)], "%d：百位 %d、十位 %d、個位 %d。" % (n, h, t, o))

    def val():
        n = R.randint(101, 999)
        h, t, o = n // 100, n // 10 % 10, n % 10
        if t == 0:
            return None
        q = "%d 的十位數字 %d 表示多少？" % (n, t)
        return mcq(q, str(10 * t), [str(t), str(100 * t), str(10 * t + o)], "十位的 %d 表示 %d 個十，是 %d。" % (t, t, 10 * t))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, val, 8, seen)


def s4(seen):
    def seq():
        step = R.choice([1, 10, 100, 5, 2])
        a = R.randint(100, 999 - 5 * step)
        if step == 100:
            a = R.randint(100, 499)
        xs = [a + step * i for i in range(5)]
        if xs[-1] > 1000:
            return None
        k = R.randint(1, 3)
        show = ["□" if i == k else str(x) for i, x in enumerate(xs)]
        q = "依照規律，□ 是多少？<br>%s" % "，".join(show)
        v = xs[k]
        return mcq(q, str(v), [str(x) for x in (v + step, v - step if v - step != xs[k - 1] else v + 1, xs[k - 1] + (1 if step != 1 else 10)) if x != v][:3] + [str(v + 2 * step)], "每次多 %d：%d ＋ %d ＝ %d。" % (step, xs[k - 1], step, v))

    def cmp():
        a, b = R.sample(range(100, 1000), 2)
        if a // 100 != b // 100 and R.random() < .6:
            b = a // 100 * 100 + R.randint(0, 99)
            if b == a:
                return None
        k = R.choice(["大", "小"])
        v = max(a, b) if k == "大" else min(a, b)
        q = "%d 和 %d，哪一個比較%s？" % (a, b, k)
        return mcq(q, str(v), [str(min(a, b) if k == "大" else max(a, b)), "一樣大", "不能比"], "先比百位，百位一樣再比十位、個位：%d 比較%s。" % (v, k))
    return pick_unique(R, seq, 10, seen) + pick_unique(R, cmp, 10, seen)


def s5(seen):
    def boxes():
        h, t, o = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
        q = "一箱有 100 張色紙，一包有 10 張。有 %d 箱、%d 包和 %d 張，一共有幾張？" % (h, t, o)
        n = 100 * h + 10 * t + o
        return mcq(q, "%d 張" % n, ["%d 張" % x for x in (h + t + o, 100 * h + 10 * o + t if o != t else n + 1, n + 10)], "%d 個百、%d 個十、%d 個一：%d 張。" % (h, t, o, n))

    def more():
        n = R.randint(100, 899)
        k = R.choice([(10, "多 10"), (100, "多 100"), (-10, "少 10"), (-100, "少 100"), (1, "多 1")])
        v = n + k[0]
        if not 100 <= v <= 1000:
            return None
        q = "比 %d %s的數是多少？" % (n, k[1])
        return mcq(q, str(v), [str(x) for x in (n + (k[0] // 10 if abs(k[0]) >= 10 else 10), n - k[0], v + 1)], "%s：%d → %d。" % (k[1], n, v))
    return pick_unique(R, boxes, 10, seen) + pick_unique(R, more, 10, seen)


def main():
    seen = set()
    sets = [("數積木", s1(seen)), ("幾個百、幾個十、幾個一", s2(seen)), ("位值", s3(seen)),
            ("順序和比大小", s4(seen)), ("生活中的數", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>10 個十是 1 個百</b>，10 個百是 1000。",
         "345 是 3 個百、4 個十、5 個一：<b>百位 3、十位 4、個位 5</b>。" + P.blocks(3, 4, 5),
         "某一位是 0 也要寫 0：3 個百和 5 個一是 305。比大小先比百位。"],
        [example("6 個百和 8 個一", ["十位沒有，寫 0。"], "608"),
         example("472 和 468", ["百位一樣，十位 7 比 6 大。"], "472 比較大")],
        [("3 個百和 5 個一寫成 35", "十位要寫 0：305"),
         ("數 10 個一數時，從 390 數到 391", "10 個 10 個數是 390、400"),
         ("先比個位", "先比百位")])
    faq = [{"q": "二年級要認識到多大的數？",
            "a": "108課綱 N-2-1：認識 1000 以內的數，用積木操作和位值表認識位值單位「百」。"},
           {"q": "為什麼要特別練有 0 的數？",
            "a": "像 305、640 這種有 0 的數最容易寫錯，0 代表那一位沒有，但要寫出來占位置。"},
           {"q": "在家怎麼練？",
            "a": "用 100 元、10 元、1 元硬幣或積木拼數，讓孩子說出是幾個百、幾個十、幾個一。"}]
    make_unit(R, "grade-2", "numbers-to-1000", "N-2-1",
              "一千以內的數：含位值積木操作活動。結合點數、位值表徵、位值表。位值單位「百」。位值單位換算。",
              "1000 以內的數：百、十、一",
              "二年級數學 1000以內的數 練習題｜百位十位個位・比大小 學習單（附解答）",
              "1000 以內的數",
              "國小二年級數學「1000 以內的數」免費學習單：數百十一的積木、幾個百幾個十幾個一、位值、數的順序和比大小、生活中的數。100題線上練習，附可列印解答。",
              "10 個十是 1 個百",
              "345：百位 3、十位 4、個位 5；某一位沒有也要寫 0。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
