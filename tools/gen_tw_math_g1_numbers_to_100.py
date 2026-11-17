# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：100 以內的數（108課綱 N-1-1）
  python3 tools/gen_tw_math_g1_numbers_to_100.py
絵を數える（20 まで）、十個一數の積木（幾個十和幾個一）、十位・個位、數線の順序、比大小、生活の場面。
誤答：十と一を逆にする（35 → 53）、一つ多く／少なく數える、十位と個位の取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81201)


def s1(seen):
    def mk():
        n = R.randint(3, 20)
        k = R.choice(P.KINDS)
        pic = P.row(n, k) if (n > 16 or R.random() < .6) else P.scatter(n, k, R.randint(1, 9999))
        q = "有幾%s%s？" % (P.cl(k), P.nm(k)) + pic
        return mcq(q, "%d %s" % (n, P.cl(k)), ["%d %s" % (x, P.cl(k)) for x in (n - 1, n + 1, n + 2 if n > 10 else n + 10)], "一個一個數，數到最後是 %d。" % n)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def pic():
        t, o = R.randint(1, 9), R.randint(0, 9)
        n = 10 * t + o
        q = "一條是 10 個。一共是多少？" + P.rods(t, o)
        return mcq(q, str(n), [str(10 * o + t) if o and 10 * o + t != n else str(n + 10), str(t + o), str(n + 1)], "%d 個十是 %d，%d 個一是 %d，合起來是 %d。" % (t, 10 * t, o, o, n))

    def words():
        t, o = R.randint(1, 9), R.randint(0, 9)
        n = 10 * t + o
        q = "%d 個十和 %d 個一，合起來是多少？" % (t, o)
        return mcq(q, str(n), [str(10 * o + t) if o and 10 * o + t != n else str(n + 1), str(t + o), "%d%d" % (t, o + 1) if o < 9 else str(n - 1)], "%d 個十是 %d，再加 %d 是 %d。" % (t, 10 * t, o, n))
    return pick_unique(R, pic, 10, seen) + pick_unique(R, words, 10, seen)


def s3(seen):
    def mk():
        t, o = R.randint(1, 9), R.randint(0, 9)
        n = 10 * t + o
        k = R.choice(["十位", "個位"])
        v = t if k == "十位" else o
        q = "%d 的%s數字是多少？" % (n, k)
        w = [o if k == "十位" else t, n, v + 1]
        return mcq(q, str(v), [str(x) for x in w if x != v] + [str(v + 2)], "%d：十位是 %d，個位是 %d。" % (n, t, o))

    def back():
        t, o = R.randint(1, 9), R.randint(0, 9)
        n = 10 * t + o
        q = "%d 是幾個十和幾個一？" % n
        return mcq(q, "%d 個十和 %d 個一" % (t, o), ["%d 個十和 %d 個一" % (o, t) if o != t else "%d 個十和 %d 個一" % (t, o + 1), "%d 個十和 %d 個一" % (t + 1, o), "%d 個十和 %d 個一" % (t, 0 if o else 1)], "%d：十位 %d，個位 %d。" % (n, t, o))
    out = pick_unique(R, mk, 10, seen) + pick_unique(R, back, 9, seen)
    q = "100 是幾個十？"
    out.append(mcq(q, "10 個十", ["1 個十", "100 個十", "0 個十"], "10 個十是 100。"))
    return out


def s4(seen):
    def nl():
        lo = R.randint(1, 90)
        hi = lo + 6
        h = R.randint(lo + 1, hi - 1)
        marks = {v: str(v) for v in range(lo, hi + 1)}
        marks[h] = "?"
        q = "數線上 ? 是多少？" + P.numline(lo, hi, marks)
        return mcq(q, str(h), [str(h + 1), str(h - 1), str(h + 10) if h + 10 <= 100 else str(h - 10)], "從 %d 往右數，%d 的下一個是 %d。" % (lo, h - 1, h))

    def morel():
        n = R.randint(2, 98)
        k = R.choice(["多 1", "少 1", "多 10", "少 10"])
        v = {"多 1": n + 1, "少 1": n - 1, "多 10": n + 10, "少 10": n - 10}[k]
        if not 1 <= v <= 100:
            return None
        q = "比 %d %s的數是多少？" % (n, k)
        w = {"多 1": [n - 1, n + 10], "少 1": [n + 1, n - 10], "多 10": [n + 1, n - 10], "少 10": [n - 1, n + 10]}[k]
        return mcq(q, str(v), [str(x) for x in w if 0 <= x <= 110] + [str(v + 2)], "%s：%d → %d。" % (k, n, v))

    def cmp():
        a, b = R.sample(range(10, 100), 2)
        k = R.choice(["大", "小"])
        v = max(a, b) if k == "大" else min(a, b)
        q = "%d 和 %d，哪一個比較%s？" % (a, b, k)
        return mcq(q, str(v), [str(min(a, b) if k == "大" else max(a, b)), "一樣大", "不知道"], "先比十位，十位一樣再比個位：%d 比較%s。" % (v, k))
    return pick_unique(R, nl, 7, seen) + pick_unique(R, morel, 7, seen) + pick_unique(R, cmp, 6, seen)


def s5(seen):
    def eggs():
        t, o = R.randint(2, 9), R.randint(1, 9)
        k = R.choice(["box", "pencil", "candy"])
        what = {"box": ("一盒有 10 顆蛋", "盒", "顆蛋"), "pencil": ("一捆有 10 枝鉛筆", "捆", "枝鉛筆"), "candy": ("一包有 10 顆糖", "包", "顆糖")}[k]
        q = "%s。有 %d %s，還有 %d %s，一共有幾%s？" % (what[0], t, what[1], o, what[2], what[2])
        n = 10 * t + o
        return mcq(q, "%d %s" % (n, what[2][0]), ["%d %s" % (x, what[2][0]) for x in (t + o, 10 * o + t if 10 * o + t != n else n + 10, n + 1)], "%d %s是 %d，再加 %d 是 %d。" % (t, what[1], 10 * t, o, n))

    def queue():
        a = R.randint(2, 20)
        q = "排隊時，小美前面有 %d 個人。小美排第幾個？" % a
        return mcq(q, "第 %d 個" % (a + 1), ["第 %d 個" % x for x in (a, a - 1, a + 2)], "前面 %d 個人，再來就是小美：第 %d 個。" % (a, a + 1))
    return pick_unique(R, eggs, 14, seen) + pick_unique(R, queue, 6, seen)


def main():
    seen = set()
    sets = [("數一數", s1(seen)), ("幾個十和幾個一", s2(seen)), ("十位和個位", s3(seen)),
            ("順序和比大小", s4(seen)), ("生活中的數", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["數東西時，<b>一個一個數</b>，不要漏掉，也不要數兩次。",
         "<b>10 個一是 1 個十</b>。35 是 3 個十和 5 個一。" + P.rods(3, 5),
         "35：<b>十位</b>是 3，<b>個位</b>是 5。比大小時，先比十位。"],
        [example("4 個十和 7 個一是多少？", ["4 個十是 40。", "40 再加 7。"], "47"),
         example("62 和 58，哪一個大？", ["十位 6 比 5 大。"], "62")],
        [("3 個十和 5 個一寫成 53", "十位寫 3，個位寫 5：35"),
         ("數東西時漏數", "數過的做記號"),
         ("比大小先看個位", "先看十位")])
    faq = [{"q": "一年級要認識到多大的數？",
            "a": "108課綱 N-1-1：認識 100 以內的數，會數數、知道順序，認識「個」和「十」的位值。"},
           {"q": "怎麼幫孩子懂「十」？",
            "a": "用 10 根吸管綁成一捆，或 10 個積木排一條，讓孩子看出 10 個一就是 1 個十。"},
           {"q": "孩子常把 35 寫成 53 怎麼辦？",
            "a": "先說「幾個十」寫在左邊，再說「幾個一」寫在右邊，多用積木或吸管練習。"}]
    make_unit(R, "grade-1", "numbers-to-100", "N-1-1",
              "一百以內的數：含操作活動。用數表示多少與順序。結合數數、位值表徵、位值表。位值單位「個」和「十」。",
              "100 以內的數",
              "一年級數學 100以內的數 練習題｜數數・十位個位・比大小 學習單（附解答）",
              "100 以內的數",
              "國小一年級數學「100 以內的數」免費學習單：看圖數一數、幾個十和幾個一、十位和個位、數線順序和比大小、生活中的數。100題線上練習馬上對答案，附可列印解答。",
              "10 個一是 1 個十",
              "35 是 3 個十和 5 個一；比大小先看十位。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
