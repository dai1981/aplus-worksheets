# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：乘法與除法的關係（108課綱 R-3-1）
  python3 tools/gen_tw_math_g3_multiplication_division_relationship.py
乘除互逆（同じ数の組の乘法・除法）、□を求める、除法の驗算（除數×商＋餘數）、乘法の驗算、應用。
誤答：□×6＝42 で 42×6 をする、驗算で餘數を足し忘れる、□÷7＝8 で 8÷7 とする。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31022)
NM = Names(R)


def s1(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if a == b:
            return None
        p = a * b
        kind = R.choice(["div", "which", "mul"])
        if kind == "div":
            q = "已知 %d × %d ＝ %d，那麼 %d ÷ %d ＝ ？" % (a, b, p, p, b)
            return mcq(q, str(a), [str(x) for x in (b, p, p * b, a + 1)], "乘法和除法互逆：%d × %d ＝ %d，所以 %d ÷ %d ＝ %d。" % (a, b, p, p, b, a))
        if kind == "which":
            q = "下面哪一個算式和 %d × %d ＝ %d 是同一組乘除算式？" % (a, b, p)
            return mcq(q, "%d ÷ %d ＝ %d" % (p, a, b), ["%d ÷ %d ＝ %d" % (b, a, p),
                                                       "%d × %d ＝ %d" % (a, p, b), "%d ＋ %d ＝ %d" % (a, b, a + b), "%d － %d ＝ %d" % (p, a, p - a)],
                       "%d × %d ＝ %d 可以寫成 %d ÷ %d ＝ %d 和 %d ÷ %d ＝ %d。" % (a, b, p, p, a, b, p, b, a))
        q = "已知 %d ÷ %d ＝ %d，那麼 %d × %d ＝ ？" % (p, a, b, a, b)
        return mcq(q, str(p), [str(x) for x in (a + b, b, p + a, p - b)], "除法反過來是乘法：%d × %d ＝ %d。" % (a, b, p))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(2, 9), R.randint(2, 12)
        p = a * b
        kind = R.choice(["lf", "rf", "dvd", "dvs"])
        if kind == "lf":
            q = "□ × %d ＝ %d，□ 是多少？" % (a, p)
            return mcq(q, str(b), [str(x) for x in (p * a, p - a, p + a, b + 1)], "用除法求：%d ÷ %d ＝ %d。" % (p, a, b))
        if kind == "rf":
            q = "%d × □ ＝ %d，□ 是多少？" % (a, p)
            return mcq(q, str(b), [str(x) for x in (p * a, p - a, b - 1 if b > 2 else b + 2, b + 1)], "用除法求：%d ÷ %d ＝ %d。" % (p, a, b))
        if kind == "dvd":
            q = "□ ÷ %d ＝ %d，□ 是多少？" % (a, b)
            return mcq(q, str(p), [str(x) for x in (a + b, b - a if b > a else a - b + 10, p + a, p - b)], "被除數 ＝ 除數 × 商：%d × %d ＝ %d。" % (a, b, p))
        q = "%d ÷ □ ＝ %d，□ 是多少？" % (p, b)
        return mcq(q, str(a), [str(x) for x in (p * b, p - b, a + 1, a + 2)], "除數 ＝ 被除數 ÷ 商：%d ÷ %d ＝ %d。" % (p, b, a))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def check():
        d = R.randint(3, 9)
        qt = R.randint(11, 99)
        r = R.randint(1, d - 1)
        t = d * qt + r
        q = "%d ÷ %d ＝ %d……%d，用哪一個算式驗算？" % (t, d, qt, r)
        ans = "%d × %d ＋ %d ＝ %d" % (d, qt, r, t)
        return mcq(q, ans, ["%d × %d ＝ %d" % (d, qt, d * qt), "%d × %d － %d ＝ %d" % (d, qt, r, d * qt - r), "%d ＋ %d ＋ %d ＝ %d" % (d, qt, r, d + qt + r)],
                   "驗算：除數 × 商 ＋ 餘數 ＝ 被除數，%d × %d ＋ %d ＝ %d。" % (d, qt, r, t))

    def wrong():
        d = R.randint(3, 9)
        qt = R.randint(12, 99)
        r = R.randint(1, d - 1)
        t = d * qt + r
        bad = R.choice(["q", "r", "big"])
        if bad == "q":
            shown = "%d……%d" % (qt + 1, r)
        elif bad == "r":
            shown = "%d……%d" % (qt, r + 1 if r + 1 < d else r - 1)
        else:
            if qt < 2:
                return None
            shown = "%d……%d" % (qt - 1, r + d)
        q = "%s算 %d ÷ %d ＝ %s。用乘法驗算，答案對嗎？" % (NM.next(), t, d, shown)
        sq, sr = map(int, shown.split("……"))
        back = d * sq + sr
        ans = "不對，正確是 %d……%d" % (qt, r)
        if bad == "big":
            e = "餘數 %d 比除數 %d 大，商還可以再大 1。正確：%d……%d。" % (sr, d, qt, r)
        else:
            e = "驗算 %d × %d ＋ %d ＝ %d，不等於 %d。正確：%d……%d。" % (d, sq, sr, back, t, qt, r)
        return mcq(q, ans, ["對", "不對，正確是 %d……%d" % (qt + 1, r) if bad != "q" else "不對，正確是 %d……%d" % (qt - 1, r),
                            "不對，正確是 %d" % qt], e)
    return pick_unique(R, check, 10, seen) + pick_unique(R, wrong, 10, seen)


def s4(seen):
    def mk():
        a, b = R.randint(12, 250), R.randint(2, 9)
        p = a * b
        if p > 999:
            return None
        if R.random() < .5:
            q = "%d × %d ＝ %d，可以用哪一個算式驗算？" % (a, b, p)
            return mcq(q, "%d ÷ %d ＝ %d" % (p, b, a), ["%d × %d ＝ %d" % (b, p, a), "%d ＋ %d ＝ %d" % (p, b, p + b), "%d ÷ %d ＝ %d" % (a, b, p)],
                       "乘法用除法驗算：%d ÷ %d ＝ %d，和原來的 %d 一樣，答案正確。" % (p, b, a, a))
        q = "%d ÷ %d ＝ %d，可以用哪一個算式驗算？" % (p, b, a)
        return mcq(q, "%d × %d ＝ %d" % (b, a, p), ["%d ÷ %d ＝ %d" % (a, b, p), "%d ＋ %d ＝ %d" % (a, b, a + b), "%d × %d ＝ %d" % (p, b, a)],
                   "沒有餘數的除法：除數 × 商 ＝ 被除數，%d × %d ＝ %d。" % (b, a, p))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def boxes():
        a, b = R.randint(3, 9), R.randint(3, 12)
        item, mw, box = R.choice([("雞蛋", "顆", "盒"), ("鉛筆", "枝", "盒"), ("餅乾", "片", "包"), ("貼紙", "張", "包")])
        q = "每%s裝 %d %s%s，%d %s%s可以裝滿幾%s？" % (box, a, mw, item, a * b, mw, item, box)
        return mcq(q, "%d %s" % (b, box), ["%d %s" % (x, box) for x in (a * b * a, a * b - a, b + 1, a)],
                   "□ × %d ＝ %d，用除法：%d ÷ %d ＝ %d（%s）。" % (a, a * b, a * b, a, b, box))

    def think():
        a, b = R.randint(3, 9), R.randint(4, 15)
        who = NM.next()
        if R.random() < .5:
            q = "%s想了一個數，乘以 %d 得到 %d。這個數是多少？" % (who, a, a * b)
            return mcq(q, str(b), [str(x) for x in (a * b * a, a * b - a, a * b + a)], "□ × %d ＝ %d，□ ＝ %d ÷ %d ＝ %d。" % (a, a * b, a * b, a, b))
        r = R.randint(1, a - 1) if a > 2 else 1
        t = a * b + r
        q = "%s想了一個數，除以 %d 得到 %d，還餘 %d。這個數是多少？" % (who, a, b, r)
        return mcq(q, str(t), [str(x) for x in (a * b, a * b - r, b // a if b >= a else a + b + r, t + a)], "被除數 ＝ 除數 × 商 ＋ 餘數：%d × %d ＋ %d ＝ %d。" % (a, b, r, t))

    def share():
        n, each = R.randint(3, 9), R.randint(6, 25)
        who = NM.next()
        q = "%s把一些糖果平分給 %d 個人，每人分到 %d 顆，剛好分完。原來有幾顆糖果？" % (who, n, each)
        return mcq(q, "%d 顆" % (n * each), ["%d 顆" % x for x in (n + each, each - n if each > n else n * each + n, n * each + each)],
                   "平分的反過來是乘法：%d × %d ＝ %d（顆）。" % (n, each, n * each))
    return pick_unique(R, boxes, 7, seen) + pick_unique(R, think, 7, seen) + pick_unique(R, share, 6, seen)


def main():
    seen = set()
    sets = [("乘除互逆", s1(seen)), ("求□", s2(seen)), ("除法的驗算", s3(seen)),
            ("乘法和除法互相驗算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["乘法和除法是<b>互逆</b>的：6 × 7 ＝ 42，所以 42 ÷ 7 ＝ 6，42 ÷ 6 ＝ 7。",
         "求 □：□ × 6 ＝ 42，用除法 42 ÷ 6 ＝ 7；□ ÷ 7 ＝ 8，用乘法 7 × 8 ＝ 56。",
         "除法驗算：<b>除數 × 商 ＋ 餘數 ＝ 被除數</b>。"],
        [example("□ × 6 ＝ 42，□ 是多少？", ["乘法反過來是除法。", "42 ÷ 6 ＝ 7。"], "7"),
         example("87 ÷ 4 ＝ 21……3，怎麼驗算？", ["除數 × 商 ＋ 餘數：4 × 21 ＋ 3。", "＝ 84 ＋ 3 ＝ 87，和被除數一樣。"], "答案正確")],
        [("□ × 6 ＝ 42，算 42 × 6", "求乘數要用除法：42 ÷ 6"),
         ("驗算時忘了加餘數", "除數 × 商 ＋ 餘數 ＝ 被除數"),
         ("□ ÷ 7 ＝ 8，算 8 ÷ 7", "求被除數要用乘法：7 × 8")])
    faq = [{"q": "什麼是乘除互逆？",
            "a": "乘法和除法可以互相還原：a × b ＝ c，就有 c ÷ b ＝ a 和 c ÷ a ＝ b。108課綱 R-3-1 要求三年級會用這個關係來驗算和解題。"},
           {"q": "除法有餘數時怎麼驗算？",
            "a": "用「除數 × 商 ＋ 餘數」，看看是不是等於被除數；另外，餘數一定要比除數小。"},
           {"q": "孩子求 □ 時不知道用乘還是除，怎麼辦？",
            "a": "把 □ 換成一個簡單的數試試看，例如 □ × 2 ＝ 6，孩子知道 □ 是 3，再發現是 6 ÷ 2，就能類推。"}]
    make_unit(R, "grade-3", "multiplication-division-relationship", "R-3-1",
              "乘法與除法的關係：乘除互逆。應用於驗算與解題。",
              "乘法與除法的關係：乘除互逆、驗算",
              "三年級數學 乘除互逆 練習題｜求□・除法驗算 學習單（附解答）",
              "乘法與除法的關係",
              "國小三年級數學「乘法與除法的關係」免費學習單：乘除互逆、求□、除法驗算（除數×商＋餘數）、乘法驗算與應用題。100題線上練習馬上對答案，附可列印解答。",
              "乘法和除法互逆",
              "除法驗算：除數 × 商 ＋ 餘數 ＝ 被除數。",
              body, faq, sets, 21)


if __name__ == "__main__":
    main()
