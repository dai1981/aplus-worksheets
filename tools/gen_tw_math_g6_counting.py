# -*- coding: utf-8 -*-
"""
台灣 國小六年級 數學：數數看有幾種（乘法原理與加法原理）（108課綱 N-6-9）
  python3 tools/gen_tw_math_g6_counting.py
加法原理（どちらか一つを選ぶ：足す）、乘法原理（順に選ぶ：掛ける）、數字卡で何位數を作る（0 は首位不可・重複なし）、路線、握手・比賽（重複を数えない）。
誤答：選ぶ／組み合わせるで足すと掛けるを取り違える、0 を最高位に置く、握手を 2 回数える。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names

R = random.Random(61017)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        ctx = R.choice([("早餐店有 %d 種漢堡、%d 種三明治。只買一樣主食，有幾種選法？", "add"),
                        ("書架上有 %d 本故事書、%d 本漫畫。只借一本，有幾種借法？", "add"),
                        ("從臺北到臺中，可以搭 %d 班火車或 %d 班客運。選一班去，有幾種走法？", "add"),
                        ("有 %d 件上衣和 %d 件褲子，上衣和褲子各選一件搭配，有幾種穿法？", "mul"),
                        ("早餐從 %d 種主食和 %d 種飲料中各選一種，有幾種組合？", "mul"),
                        ("從甲地到乙地有 %d 條路，乙地到丙地有 %d 條路。從甲地經過乙地到丙地，有幾種走法？", "mul")])
        q = ctx[0] % (a, b)
        v = a + b if ctx[1] == "add" else a * b
        o = a * b if ctx[1] == "add" else a + b
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (o, v + 1, max(a, b))  if x != v],
                   ("只選一樣，兩類加起來：%d ＋ %d ＝ %d（加法原理）。" if ctx[1] == "add" else "每一種都可以配另一邊的每一種：%d × %d ＝ %d（乘法原理）。") % (a, b, v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b, c = R.randint(2, 5), R.randint(2, 5), R.randint(2, 4)
        q = "點餐時主餐有 %d 種、湯有 %d 種、甜點有 %d 種，各選一種，一共有幾種組合？" % (a, b, c)
        v = a * b * c
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (a + b + c, a * b + c, v * 2)  if x != v], "%d × %d × %d ＝ %d（種）。" % (a, b, c, v))

    def lock():
        n = R.choice([2, 3])
        d = R.choice([3, 4, 5, 10])
        v = d ** n
        q = "一個密碼鎖有 %d 個轉輪，每個轉輪可以轉到 %d 個數字（可以重複）。一共有幾種密碼？" % (n, d)
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (d * n, d + n, v - 1 if v > 9 else v + 3)  if x != v], "每個轉輪都有 %d 種：%s ＝ %d（種）。" % (d, " × ".join([str(d)] * n), v))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, lock, 8, seen)


def s3(seen):
    def cards():
        n = R.choice([3, 4, 5])
        zero = R.random() < .5
        digits = R.sample(range(1, 10), n - (1 if zero else 0)) + ([0] if zero else [])
        k = R.choice([2, 3]) if n >= 3 else 2
        if k > n:
            return None
        first = n - 1 if zero else n
        v = first
        for i in range(1, k):
            v *= n - i
        wrong = 1
        for i in range(k):
            wrong *= n - i
        q = "用數字卡 %s（每張只用一次）排成%s位數，可以排出幾個？" % ("、".join(map(str, sorted(digits))), "二" if k == 2 else "三")
        e = ("最高位不能放 0，有 %d 種；" % first if zero else "最高位有 %d 種；" % first) + "接著每一位都少一張卡可以選：%s ＝ %d（個）。" % (" × ".join(str(x) for x in [first] + [n - i for i in range(1, k)]), v)
        return mcq(q, "%d 個" % v, ["%d 個" % x for x in (wrong if wrong != v else v + n, n ** k, v // 2 if v % 2 == 0 and v // 2 != v else v + 1)  if x != v], e)
    return pick_unique(R, cards, 20, seen)


def s4(seen):
    def hands():
        n = R.randint(3, 12)
        v = n * (n - 1) // 2
        q = "%d 個人見面，每兩個人都握一次手，一共握幾次手？" % n
        return mcq(q, "%d 次" % v, ["%d 次" % x for x in (n * (n - 1), n * n, v + n)], "每個人和其他 %d 人握手：%d × %d ＝ %d，但每次握手被算了 2 次：%d ÷ 2 ＝ %d。" % (n - 1, n, n - 1, n * (n - 1), n * (n - 1), v))

    def league():
        n = R.randint(4, 10)
        v = n * (n - 1) // 2
        q = "%d 隊比賽，每兩隊都要比一場（單循環），一共要比幾場？" % n
        return mcq(q, "%d 場" % v, ["%d 場" % x for x in (n * (n - 1), n - 1, v + n)], "%d × %d ÷ 2 ＝ %d（場）。" % (n, n - 1, v))

    def ko():
        n = R.choice([4, 8, 16, 32])
        v = n - 1
        q = "%d 隊參加淘汰賽，每場輸的隊伍就被淘汰，最後剩一隊冠軍。一共要比幾場？" % n
        return mcq(q, "%d 場" % v, ["%d 場" % x for x in (n // 2, n * (n - 1) // 2, n)], "每場淘汰 1 隊，要淘汰 %d 隊，就要比 %d 場。" % (v, v))
    return pick_unique(R, hands, 8, seen) + pick_unique(R, league, 7, seen) + pick_unique(R, ko, 4, seen) + pick_unique(R, lambda: mcq("2 個人握手和 2 隊比賽一場，都是「兩個一組」。5 個人每兩人握一次手，用樹狀圖數，最不容易出錯的方法是什麼？", "依順序列出，已經算過的組合不再重複", ["每個人都數 4 次再相加", "隨便配對", "只數第一個人"], "例如 A 和 B、A 和 C……；B 開始時不用再數 B 和 A。"), 1, seen)


def s5(seen):
    def photo():
        n = R.choice([3, 4, 5])
        v = 1
        for i in range(1, n + 1):
            v *= i
        q = "%d 個人排成一排照相，有幾種不同的排法？" % n
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (n * n, n * (n - 1), n + (n - 1) + (n - 2))  if x != v], "第 1 個位置 %d 種，第 2 個 %d 種……：%s ＝ %d（種）。" % (n, n - 1, " × ".join(str(i) for i in range(n, 0, -1)), v))

    def flag():
        c = R.choice([3, 4, 5])
        v = c * (c - 1) * (c - 2)
        q = "用 %d 種不同顏色，替一面有三條橫條的旗子塗色，三條顏色都不同。有幾種塗法？" % c
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (c ** 3, c * 3, c * (c - 1))  if x != v], "第一條 %d 種，第二條 %d 種，第三條 %d 種：%d × %d × %d ＝ %d。" % (c, c - 1, c - 2, c, c - 1, c - 2, v))

    def coins():
        tot = R.choice([10, 15, 20])
        ways = [(a, b) for a in range(0, tot // 5 + 1) for b in range(0, tot + 1) if a * 5 + b == tot]
        q = "只用 5 元和 1 元硬幣湊出 %d 元，有幾種不同的湊法？（可以只用一種硬幣）" % tot
        v = len(ways)
        return mcq(q, "%d 種" % v, ["%d 種" % x for x in (v - 1, v + 1, tot // 5)  if x != v], "5 元可以用 0 到 %d 枚，每一種剩下的都用 1 元補：共 %d 種。" % (tot // 5, v))
    return pick_unique(R, photo, 3, seen) + pick_unique(R, flag, 3, seen) + pick_unique(R, coins, 3, seen) + pick_unique(R, extra, 11, seen)


def extra():
    a, b = R.randint(2, 6), R.randint(2, 6)
    k = R.randint(2, 4)
    q = "從 %d 個男生和 %d 個女生中，選 1 個男生和 1 個女生當班長和副班長（男生當班長），有幾種選法？" % (a, b) if k == 2 else \
        "從 %d 本故事書和 %d 本科學書中，先選 1 本故事書，再選 1 本科學書帶去露營，有幾種帶法？" % (a, b)
    v = a * b
    return mcq(q, "%d 種" % v, ["%d 種" % x for x in (a + b, v * 2, v - 1)], "先選一樣、再選另一樣：%d × %d ＝ %d（種）。" % (a, b, v))


def main():
    seen = set()
    sets = [("加法原理和乘法原理", s1(seen)), ("三步驟的乘法原理", s2(seen)), ("數字卡排數", s3(seen)),
            ("握手和比賽", s4(seen)), ("綜合挑戰", s5(seen))]
    body = lesson(
        ["<b>加法原理</b>：從幾類中只選<b>一樣</b>，把每一類的方法數<b>加</b>起來。",
         "<b>乘法原理</b>：要<b>一步接一步</b>都選（上衣配褲子），把每一步的方法數<b>乘</b>起來。",
         "排數字時，最高位不能放 0；每張卡只能用一次，後面可以選的就少一張。",
         "握手、單循環比賽：每兩個算一次，人數 ×（人數 － 1）÷ 2。"],
        [example("3 件上衣、4 件褲子，各選一件有幾種穿法？", ["3 × 4 ＝ 12。"], "12 種"),
         example("用 0、1、2、3 排成不重複的三位數，有幾個？", ["百位不能是 0：3 種。", "十位 3 種，個位 2 種：3 × 3 × 2 ＝ 18。"], "18 個")],
        [("只選一樣卻用乘的", "只選一樣用加的"),
         ("0 放在最高位也算", "最高位不能是 0"),
         ("5 人握手算成 5 × 4 ＝ 20 次", "每次被算了 2 次：20 ÷ 2 ＝ 10")])
    faq = [{"q": "什麼時候加、什麼時候乘？",
            "a": "只選一樣（這個或那個）用加；要選好幾樣一起搭配（這個和那個）用乘。"},
           {"q": "孩子數的時候常漏掉或重複，怎麼辦？",
            "a": "用樹狀圖或表格，依順序一個一個列出來，已經算過的組合不要再算。"},
           {"q": "六年級為什麼要學乘法原理？",
            "a": "108課綱 N-6-9：由問題中的數量關係列式解題，包含較複雜的計數：乘法原理、加法原理或其混合。"}]
    make_unit(R, "grade-6", "counting", "N-6-9",
              "解題：由問題中的數量關係，列出恰當的算式解題（同 R-6-4）。可包含（1）較複雜的模式（如座位排列模式）；（2）較複雜的計數：乘法原理、加法原理或其混合；（3）較複雜之情境：如年齡問題、流水問題、和差問題、雞兔問題。",
              "乘法原理與加法原理：數數看有幾種",
              "六年級數學 乘法原理 練習題｜加法原理・排列・握手問題 學習單（附解答）",
              "乘法原理與加法原理",
              "國小六年級數學「乘法原理與加法原理」免費學習單：只選一樣用加、搭配用乘，三步驟的組合、數字卡排數、握手和比賽場數與照相排法等挑戰題。100題線上練習馬上對答案，附可列印解答。",
              "只選一樣用加，一起搭配用乘",
              "最高位不能是 0；握手要 ÷ 2。",
              body, faq, sets, 17)


if __name__ == "__main__":
    main()
