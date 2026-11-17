# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：加減應用問題（□ 的問題）（108課綱 N-2-3、R-2-? 加減互逆）
  python3 tools/gen_tw_math_g2_addition_subtraction_word_problems.py
被加數・加數・被減數・減數が未知の文章題、□ を使った算式、加減の關係（□ ＋ 25 ＝ 63 → 63 － 25）、比較型（多幾個・少幾個）。
誤答：「又」や「多」の言葉につられて足す、□ を求めるのに逆の計算をしない。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets

R = random.Random(81304)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(12, 400), R.randint(12, 400)
        if a + b > 999:
            return None
        s = a + b
        k = R.choice(["first", "second", "sub_a", "sub_b"])
        if k == "first":
            q, v, e = "□ ＋ %d ＝ %d，□ 是多少？" % (b, s), a, "□ ＝ %d － %d ＝ %d。" % (s, b, a)
        elif k == "second":
            q, v, e = "%d ＋ □ ＝ %d，□ 是多少？" % (a, s), b, "□ ＝ %d － %d ＝ %d。" % (s, a, b)
        elif k == "sub_a":
            q, v, e = "□ － %d ＝ %d，□ 是多少？" % (b, a), s, "□ ＝ %d ＋ %d ＝ %d。" % (a, b, s)
        else:
            q, v, e = "%d － □ ＝ %d，□ 是多少？" % (s, a), b, "□ ＝ %d － %d ＝ %d。" % (s, a, b)
        w = {"first": [s + b], "second": [s + a], "sub_a": [abs(a - b)], "sub_b": [s + a]}[k]
        return mcq(q, str(v), [str(x) for x in w + [v + 10, v - 10 if v > 10 else v + 1] if x != v and x <= 1998], e)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(15, 300), R.randint(15, 300)
        who = NM.next()
        k = R.choice(["start", "change"])
        if k == "start":
            q = "%s有一些貼紙，又買了 %d 張，現在有 %d 張。原來有幾張？" % (who, b, a + b)
            return mcq(q, "%d 張" % a, ["%d 張" % x for x in (a + 2 * b, a + 10, a - 10 if a > 10 else a + 1)], "原來的 ＋ %d ＝ %d，原來的 ＝ %d － %d ＝ %d。題目有「又買」，但要用減法。" % (b, a + b, a + b, b, a))
        q = "%s原來有 %d 元，媽媽又給了一些，現在有 %d 元。媽媽給了多少元？" % (who, a, a + b)
        return mcq(q, "%d 元" % b, ["%d 元" % x for x in (2 * a + b, b + 10, b - 10 if b > 10 else b + 1)], "%d ＋ □ ＝ %d，□ ＝ %d － %d ＝ %d。" % (a, a + b, a + b, a, b))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(15, 300), R.randint(15, 300)
        who = NM.next()
        k = R.choice(["start", "take"])
        if k == "start":
            q = "%s有一些彈珠，送給弟弟 %d 顆，還剩 %d 顆。原來有幾顆？" % (who, b, a)
            return mcq(q, "%d 顆" % (a + b), ["%d 顆" % x for x in (abs(a - b) if a != b else a + 1, a + b + 10, a)], "原來的 － %d ＝ %d，原來的 ＝ %d ＋ %d ＝ %d。題目有「送給」，但要用加法。" % (b, a, a, b, a + b))
        q = "停車場有 %d 輛車，開走一些後剩下 %d 輛。開走了幾輛？" % (a + b, a)
        return mcq(q, "%d 輛" % b, ["%d 輛" % x for x in (2 * a + b, b + 10, a)], "%d － □ ＝ %d，□ ＝ %d － %d ＝ %d。" % (a + b, a, a + b, a, b))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, d = R.randint(30, 500), R.randint(12, 200)
        x, y = NM.next(), NM.next()
        k = R.choice(["more", "less", "big", "small"])
        if k == "more":
            q = "%s有 %d 張卡片，%s比%s多 %d 張。%s有幾張？" % (x, a, y, x, d, y)
            v, w, e = a + d, [a - d if a > d else a + 1], "比 %d 多 %d：%d ＋ %d ＝ %d。" % (a, d, a, d, a + d)
        elif k == "less":
            if a <= d:
                return None
            q = "%s有 %d 張卡片，%s比%s少 %d 張。%s有幾張？" % (x, a, y, x, d, y)
            v, w, e = a - d, [a + d], "比 %d 少 %d：%d － %d ＝ %d。" % (a, d, a, d, a - d)
        elif k == "big":
            q = "%s有 %d 張卡片，比%s多 %d 張。%s有幾張？" % (x, a + d, y, d, y)
            v, w, e = a, [a + 2 * d], "%s比%s多，%s少：%d － %d ＝ %d。有「多」但要用減法。" % (x, y, y, a + d, d, a)
        else:
            q = "%s有 %d 張卡片，比%s少 %d 張。%s有幾張？" % (x, a, y, d, y)
            v, w, e = a + d, [a - d if a > d else a + 1], "%s比%s少，%s多：%d ＋ %d ＝ %d。有「少」但要用加法。" % (x, y, y, a, d, a + d)
        return mcq(q, "%d 張" % v, ["%d 張" % t for t in w + [v + 10, v - 10]], e)
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, b = R.randint(20, 400), R.randint(20, 400)
        k = R.choice(["add", "sub_start", "sub_take", "add_change"])
        who = NM.next()
        if k == "add":
            q = "%s上午走了 %d 步，下午走了 %d 步。哪一個算式可以算出一共走了幾步？" % (who, a, b)
            ans = "%d ＋ %d ＝ □" % (a, b)
        elif k == "sub_start":
            q = "%s有一些錢，花了 %d 元，剩下 %d 元。哪一個算式可以算出原來有多少？" % (who, b, a)
            ans = "□ － %d ＝ %d" % (b, a)
        elif k == "sub_take":
            q = "一盒有 %d 顆巧克力，吃掉一些後剩下 %d 顆。哪一個算式可以算出吃掉幾顆？" % (a + b, a)
            ans = "%d － □ ＝ %d" % (a + b, a)
        else:
            q = "%s有 %d 張郵票，又收到一些，變成 %d 張。哪一個算式可以算出收到幾張？" % (who, a, a + b)
            ans = "%d ＋ □ ＝ %d" % (a, a + b)
        pool = [("%d ＋ %d ＝ □" % (a, b), a + b), ("□ － %d ＝ %d" % (b, a), a + b), ("%d － □ ＝ %d" % (a + b, a), b), ("%d ＋ □ ＝ %d" % (a, a + b), b), ("%d ＋ □ ＝ %d" % (b, a + b), a), ("□ ＋ %d ＝ %d" % (a + b, b), None)]
        val = dict(pool)[ans]
        w = [x for x, v in pool if v != val]
        return mcq(q, ans, w, "按照故事的順序寫：原來的、變化的、結果，不知道的用 □。其他算式算出來的 □ 不是要找的數。")
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("□ 是多少", s1(seen)), ("不知道原來或增加多少", s2(seen)), ("不知道原來或減少多少", s3(seen)),
            ("比多少", s4(seen)), ("用 □ 列算式", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["不知道的數用 <b>□</b> 表示，按照故事的順序寫算式。",
         "加法和減法可以互相換：□ ＋ 25 ＝ 63，□ ＝ 63 － 25；□ － 18 ＝ 40，□ ＝ 40 ＋ 18。",
         "不能只看「又」「多」就用加法，要想清楚要算的是哪一個數。"],
        [example("有一些糖，又買了 15 顆，現在 42 顆。原來幾顆？", ["□ ＋ 15 ＝ 42。", "□ ＝ 42 － 15。"], "27 顆"),
         example("哥哥 85 張，比弟弟多 20 張。弟弟幾張？", ["弟弟比較少。", "85 － 20。"], "65 張")],
        [("看到「又買」就用加法", "求原來的要用減法"),
         ("比弟弟多 20，弟弟 ＝ 85 ＋ 20", "哥哥多，弟弟少：85 － 20"),
         ("□ － 18 ＝ 40，□ ＝ 40 － 18", "要加回去：40 ＋ 18")])
    faq = [{"q": "為什麼要用 □ 列式？",
            "a": "按照故事順序寫出算式，再用加減的關係求 □，比直接猜要用加或減更不容易錯，也是以後學方程式的基礎。"},
           {"q": "二年級的加減應用題有哪些？",
            "a": "108課綱 N-2-3：加數、被加數、減數、被減數未知的應用題，並連結加法與減法的關係。"},
           {"q": "孩子看到「多」就用加法怎麼辦？",
            "a": "請孩子先說「誰多、誰少」，再畫線段或積木比一比，看要求的是多的還是少的。"}]
    make_unit(R, "grade-2", "addition-subtraction-word-problems", "N-2-3",
              "解題：加減應用問題。加數、被加數、減數、被減數未知之應用解題。連結加與減的關係。",
              "加減應用問題：用 □ 列算式",
              "二年級數學 加減應用題 練習題｜□是多少・比多少 學習單（附解答）",
              "加減應用問題",
              "國小二年級數學「加減應用問題」免費學習單：□ 是多少、不知道原來或變化多少、比多少、用 □ 按故事順序列算式。100題線上練習，附可列印解答。",
              "不知道的數用 □，按故事順序列式",
              "□ ＋ 25 ＝ 63，□ ＝ 63 － 25。",
              body, faq, sets, 4)


if __name__ == "__main__":
    main()
