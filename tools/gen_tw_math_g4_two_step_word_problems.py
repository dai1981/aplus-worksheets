# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：兩步驟應用問題（乘與除、連除）（108課綱 N-4-3）
  python3 tools/gen_tw_math_g4_two_step_word_problems.py
先乘再除、先除再乘、連除、單價と総価、比較の文章題。
誤答：1 歩目で止める、割る数を取り違える、連除で 2 つの数を掛けずに足す。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41004)
NM = Names(R)


def ans_w(v, u, extra):
    return "%s%s" % (num(v), u), ["%s%s" % (num(x), u) for x in extra if x != v and x > 0]


def mul_div():
    """先乘再除：每盒 a 個、b 盒，平分給 c 人"""
    def mk():
        c = R.randint(3, 12)
        a, b = R.randint(6, 24), R.randint(4, 15)
        if (a * b) % c:
            return None
        v = a * b // c
        item = R.choice([("巧克力", "顆", "盒"), ("餅乾", "片", "包"), ("色紙", "張", "包"), ("彈珠", "顆", "袋")])
        q = "每%s有 %d %s%s，買了 %d %s，平分給 %d 個人，每人分到幾%s？" % (item[2], a, item[1], item[0], b, item[2], c, item[1])
        A, W = ans_w(v, " " + item[1], [a * b, a * b * c, b * c, a // c if a % c == 0 else v + 1, v - 1, a + b])
        return mcq(q, A, W, "先算全部：%d × %d ＝ %d（%s）。再平分：%d ÷ %d ＝ %d（%s）。" % (a, b, a * b, item[1], a * b, c, v, item[1]))
    return mk


def div_mul():
    """先除再乘：b 個 p 元，買 n 個要多少元"""
    def mk():
        b, p = R.randint(3, 9), R.randint(8, 45)
        n = R.randint(5, 30)
        if n == b:
            return None
        tot = b * p
        who = NM.next()
        item, mw = R.choice([("蛋塔", "個"), ("筆記本", "本"), ("原子筆", "枝"), ("飯糰", "個"), ("布丁", "個")])
        q = "%d %s%s賣 %d 元，%s要買 %d %s，要付多少元？" % (b, mw, item, tot, who, n, mw)
        v = p * n
        A, W = ans_w(v, " 元", [tot * n, tot // n if tot >= n else tot + n, p, v + p, tot + n])
        return mcq(q, A, W, "先算 1 %s：%d ÷ %d ＝ %d（元）。再算 %d %s：%d × %d ＝ %s（元）。" % (mw, tot, b, p, n, mw, p, n, num(v)))
    return mk


def chain_div():
    """連除"""
    def mk():
        a, b = R.randint(2, 9), R.randint(3, 12)
        v = R.randint(3, 30)
        tot = a * b * v
        T = [("%s 張貼紙平分給 %d 班，每班再平分給 %d 組，每組分到幾張？" % (num(tot), a, b), " 張"),
             ("%s 公克的麵粉平分成 %d 袋，每袋再平分做成 %d 個麵包，每個麵包用幾公克麵粉？" % (num(tot), a, b), " 公克"),
             ("%s 顆橘子裝成 %d 大箱，每大箱又分成 %d 小盒，每小盒有幾顆？" % (num(tot), a, b), " 顆")]
        q, u = R.choice(T)
        A, W = ans_w(v, u, [tot // a, tot // b if tot % b == 0 else v + 2, tot // (a + b) if tot % (a + b) == 0 else v * 2, v + 1, a * b])
        return mcq(q, A, W, "先算 %s ÷ %d ＝ %s，再算 %s ÷ %d ＝ %d。也可以算 %d × %d ＝ %d，%s ÷ %d ＝ %d。" % (
            num(tot), a, num(tot // a), num(tot // a), b, v, a, b, a * b, num(tot), a * b, v))
    return mk


def compare():
    def mk():
        who, o = NM.next(), NM.next()
        if who == o:
            return None
        a, k = R.randint(12, 60), R.randint(3, 8)
        n = R.randint(2, 6)
        if n == k:
            return None
        if R.random() < .5:
            q = "%s有 %d 張卡片，%s的卡片是%s的 %d 倍。%s把卡片平分給 %d 個朋友，每人分到幾張？" % (who, a, o, who, k, o, n)
            if (a * k) % n:
                return None
            v = a * k // n
            A, W = ans_w(v, " 張", [a * k, a // n if a % n == 0 else v + 2, a * k * n, v + 1, a + k])
            return mcq(q, A, W, "%s有 %d × %d ＝ %d（張），%d ÷ %d ＝ %d（張）。" % (o, a, k, a * k, a * k, n, v))
        big = a * k
        q = "%s有 %d 元，是%s的 %d 倍。%s的錢可以買幾個 %d 元的飯糰？" % (who, big, o, k, o, n)
        if a % n:
            return None
        v = a // n
        A, W = ans_w(v, " 個", [big // n if big % n == 0 else v * k, a, v + 1, big])
        return mcq(q, A, W, "%s有 %d ÷ %d ＝ %d（元），%d ÷ %d ＝ %d（個）。" % (o, big, k, a, a, n, v))
    return mk


def first_step():
    def mk():
        a, b, c = R.randint(3, 9), R.randint(4, 12), R.randint(2, 6)
        tot = a * b * c
        q = "「%d 本書平分給 %d 班，每班再平分給 %d 組，每組幾本？」第一步可以算什麼？" % (tot, a, b)
        return mcq(q, "%d ÷ %d，先算每班幾本" % (tot, a), ["%d × %d，先算全部幾本" % (tot, a), "%d ＋ %d，先算一共幾班幾組" % (a, b), "%d ÷ %d，先算每班幾組" % (b, a)],
                   "先平分給班：%d ÷ %d ＝ %d；再平分給組：%d ÷ %d ＝ %d。" % (tot, a, tot // a, tot // a, b, c))
    return mk


def main():
    seen = set()
    sets = [("先乘再除", pick_unique(R, mul_div(), 20, seen)),
            ("先除再乘", pick_unique(R, div_mul(), 20, seen)),
            ("連除", pick_unique(R, chain_div(), 20, seen)),
            ("倍數和分配", pick_unique(R, compare(), 20, seen)),
            ("綜合：想好第一步", pick_unique(R, first_step(), 6, seen) + pick_unique(R, mul_div(), 4, seen)
                               + pick_unique(R, div_mul(), 5, seen) + pick_unique(R, chain_div(), 5, seen))]
    body = lesson(
        ["兩步驟的題目，先找出「要先知道的數」：要平分，先知道全部；要算很多個，先知道 1 個。",
         "<b>先乘再除</b>：每盒幾個 × 幾盒 ＝ 全部，再 ÷ 人數。<b>先除再乘</b>：總價 ÷ 個數 ＝ 1 個的價錢，再 × 要買的個數。",
         "<b>連除</b>：平分了兩次，可以一次一次除，也可以先把兩個除數相乘再除。"],
        [example("3 個蛋塔賣 105 元，買 8 個要多少元？", ["1 個：105 ÷ 3 ＝ 35（元）。", "8 個：35 × 8 ＝ 280（元）。"], "280 元"),
         example("720 張貼紙平分給 4 班，每班再平分給 6 組，每組幾張？", ["720 ÷ 4 ＝ 180（張）。", "180 ÷ 6 ＝ 30（張）。"], "30 張")],
        [("只算第一步就停下來", "再讀一次問題問的是什麼"),
         ("先除再乘的題目直接用總價 × 個數", "要先算出 1 個多少元"),
         ("連除時把兩個除數相加", "兩個除數要相乘：4 × 6 ＝ 24")])
    faq = [{"q": "四年級的兩步驟應用問題有哪些？",
            "a": "108課綱 N-4-3：乘與除、連除的兩步驟應用問題，例如先乘再除、先除再乘、平分兩次。"},
           {"q": "連除可以一次算嗎？",
            "a": "可以。720 ÷ 4 ÷ 6 和 720 ÷ (4 × 6) 的答案一樣，先把除數相乘再除，常常更快。"},
           {"q": "怎麼幫孩子找出第一步？",
            "a": "問孩子「答案要用到哪個數？這個數題目有沒有直接給？」沒有給的那個數就是第一步要先算的。"}]
    make_unit(R, "grade-4", "two-step-word-problems", "N-4-3",
              "解題：兩步驟應用問題（乘除，連除）。乘與除、連除之應用解題。",
              "兩步驟應用問題：乘與除、連除",
              "四年級數學 兩步驟應用題 練習題｜先乘再除・先除再乘・連除 學習單（附解答）",
              "兩步驟應用問題（乘除）",
              "國小四年級數學「兩步驟應用問題」免費學習單：先乘再除、先除再乘、連除、倍數和分配，練習想好第一步再算。100題線上練習馬上對答案，附可列印解答。",
              "先找出要先知道的數",
              "連除：兩個除數可以先相乘再除。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
