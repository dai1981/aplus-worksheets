# -*- coding: utf-8 -*-
"""
台灣 國小一年級 數學：分類與整理（108課綱 D-1-1）
  python3 tools/gen_tw_math_g1_sorting_and_counting.py
混ざった物を種類で分けて數える、色や形で分ける、仲間はずれ（分類の規則）、分類した表を讀む（最多・最少・相差・合計）、生活の場面。
誤答：同じ物を二度數える、多い方と少ない方の取り違え、相差で足してしまう。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, table
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81212)
SHN = {"triangle": "三角形", "square": "正方形", "circle": "圓形", "rectangle": "長方形"}
CN = {"red": "紅色", "blue": "藍色", "yellow": "黃色", "green": "綠色"}


def s1(seen):
    def mk():
        ks = R.sample(P.KINDS, 3)
        ns = [R.randint(2, 7) for _ in ks]
        if sum(ns) > 24:
            return None
        i = R.randrange(3)
        q = "%s有幾%s？" % (P.nm(ks[i]), P.cl(ks[i])) + P.mixed(list(zip(ks, ns)), R.randint(1, 9999))
        v = ns[i]
        return mcq(q, "%d %s" % (v, P.cl(ks[i])), ["%d %s" % (x, P.cl(ks[i])) for x in (sum(ns), v + 1, v - 1 if v > 1 else v + 2)], "只數%s，數過的做記號：%d %s。" % (P.nm(ks[i]), v, P.cl(ks[i])))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(6, 7)
        items = [(R.choice(list(SHN)), R.choice(list(CN))) for _ in range(n)]
        by = R.choice(["color", "shape"])
        if by == "color":
            c = R.choice(list(CN))
            v = sum(1 for _, x in items if x == c)
            q = "%s的圖形有幾個？" % CN[c]
        else:
            c = R.choice(list(SHN))
            v = sum(1 for x, _ in items if x == c)
            q = "%s有幾個？（不管顏色）" % SHN[c]
        if v == 0:
            return None
        q += P.shapes_row(items, size=20)
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (v + 1, v + 2, n, v - 1 if v else 3) if x != v][:3], "按%s分一分，%s有 %d 個。" % ("顏色" if by == "color" else "形狀", CN[c] if by == "color" else SHN[c], v))
    return pick_unique(R, mk, 20, seen)


GROUPS = [("水果", ["蘋果", "香蕉", "橘子", "葡萄", "西瓜", "芒果"]), ("動物", ["小狗", "小貓", "兔子", "大象", "老虎", "猴子"]),
          ("文具", ["鉛筆", "橡皮擦", "尺", "剪刀", "膠水", "彩色筆"]), ("交通工具", ["公車", "火車", "腳踏車", "飛機", "汽車", "捷運"]),
          ("衣服", ["上衣", "褲子", "裙子", "外套", "襪子", "帽子"]), ("蔬菜", ["高麗菜", "紅蘿蔔", "青椒", "玉米", "番茄", "菠菜"])]


def s3(seen):
    def mk():
        (g1, a), (g2, b) = R.sample(GROUPS, 2)
        three = R.sample(a, 3)
        odd = R.choice(b)
        xs = three + [odd]
        R.shuffle(xs)
        q = "哪一個和其他的不是同一類？<br>%s" % "、".join(xs)
        return mcq(q, odd, [x for x in xs if x != odd], "%s都是%s，%s是%s。" % ("、".join(three), g1, odd, g2))
    return pick_unique(R, mk, 20, seen)


FRUIT = ["蘋果", "香蕉", "葡萄", "芒果", "西瓜", "草莓"]


def tb():
    ks = R.sample(FRUIT, 4)
    ns = R.sample(range(2, 10), 4)
    t = table(["水果"] + ks, [["人數"] + [str(n) for n in ns]])
    return ks, ns, t


def s4(seen):
    def mk():
        ks, ns, t = tb()
        k = R.choice(["max", "min", "one"])
        if k == "max":
            i = ns.index(max(ns))
            q = "班上同學最喜歡的水果如下表。最多人喜歡哪一種？" + t
            return mcq(q, ks[i], [x for x in ks if x != ks[i]], "比一比人數，%s %d 人最多。" % (ks[i], ns[i]))
        if k == "min":
            i = ns.index(min(ns))
            q = "班上同學最喜歡的水果如下表。最少人喜歡哪一種？" + t
            return mcq(q, ks[i], [x for x in ks if x != ks[i]], "比一比人數，%s %d 人最少。" % (ks[i], ns[i]))
        i = R.randrange(4)
        q = "班上同學最喜歡的水果如下表。喜歡%s的有幾人？" % ks[i] + t
        return mcq(q, "%d 人" % ns[i], ["%d 人" % x for x in ns if x != ns[i]], "看%s下面的數：%d 人。" % (ks[i], ns[i]))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        ks, ns, t = tb()
        k = R.choice(["diff", "sum", "total"])
        i, j = R.sample(range(4), 2)
        if k == "diff":
            if ns[i] == ns[j]:
                return None
            big, small = (i, j) if ns[i] > ns[j] else (j, i)
            q = "看表。喜歡%s的比喜歡%s的多幾人？" % (ks[big], ks[small]) + t
            d = ns[big] - ns[small]
            return mcq(q, "%d 人" % d, ["%d 人" % x for x in (ns[big] + ns[small], ns[big], d + 1)], "%d － %d ＝ %d。" % (ns[big], ns[small], d))
        if k == "sum":
            q = "看表。喜歡%s和%s的一共有幾人？" % (ks[i], ks[j]) + t
            s = ns[i] + ns[j]
            return mcq(q, "%d 人" % s, ["%d 人" % x for x in (abs(ns[i] - ns[j]) if ns[i] != ns[j] else s + 2, s + 1, s - 1)], "%d ＋ %d ＝ %d。" % (ns[i], ns[j], s))
        if sum(ns) > 30:
            return None
        q = "看表。全班一共有幾人？" + t
        s = sum(ns)
        return mcq(q, "%d 人" % s, ["%d 人" % x for x in (s - 1, s + 1, max(ns))], "%s ＝ %d。" % (" ＋ ".join(map(str, ns)), s))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("分類數一數", s1(seen)), ("按顏色、形狀分", s2(seen)), ("哪一個不同類", s3(seen)),
            ("看分類表", s4(seen)), ("比多少、算一共", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>分類</b>：把一樣的放在一起，可以按種類、顏色、形狀來分。",
         "數的時候，數過的做記號，就不會數兩次或漏掉。",
         "分好以後寫成<b>表</b>，一眼就看出哪一種最多、哪一種最少。" + table(["水果", "蘋果", "香蕉", "葡萄"], [["人數", "6", "4", "8"]])],
        [example("上表，哪一種最多人喜歡？", ["8 最大。"], "葡萄"),
         example("喜歡葡萄的比喜歡香蕉的多幾人？", ["8 － 4。"], "4 人")],
        [("同一個東西數兩次", "數過的做記號"),
         ("最少的看成最多", "比一比數字，大的才是最多"),
         ("多幾人用加法", "多幾人用減法")])
    faq = [{"q": "一年級的統計要學什麼？",
            "a": "108課綱 D-1-1：以操作為主，蒐集、分類、記錄、呈現日常生活中的物品，並能讀懂已經整理好的分類。"},
           {"q": "分類有一定的方法嗎？",
            "a": "沒有唯一的方法，可以按種類、顏色、大小、形狀分，只要說得出分類的規則就對。"},
           {"q": "在家可以怎麼練習？",
            "a": "整理玩具或襪子時，請孩子分類、數一數、比比看哪一類最多，再說說怎麼分的。"}]
    make_unit(R, "grade-1", "sorting-and-counting", "D-1-1",
              "簡單分類：以操作活動為主。能蒐集、分類、記錄、呈現日常生活物品，報讀、說明已處理好之分類。",
              "分類與整理：數一數和看表",
              "一年級數學 分類與整理 練習題｜分類數一數・看表比多少 學習單（附解答）",
              "分類與整理",
              "國小一年級數學「分類與整理」免費學習單：把東西分類數一數、按顏色和形狀分、哪一個不同類、看分類表、比多少和算一共。100題線上練習，圖多，附可列印解答。",
              "一樣的放一起，數過的做記號",
              "分類表一眼看出哪一種最多、最少。",
              body, faq, sets, 12)


if __name__ == "__main__":
    main()
