# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：小數的乘法（108課綱 N-5-8）
  python3 tools/gen_tw_math_g5_multiplying_decimals.py
整數×小數、小數×小數の直式（小數位數を合計）、積の大小、末尾の0、應用問題。
誤答：小數點の位置（位數の合計を数え間違える）、小數點をそろえて掛ける、「かけると必ず大きくなる」。
"""
import random
from decimal import Decimal as Dm
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, num

R = random.Random(51009)
NM = Names(R)


def D(x):
    s = format(Dm(x).normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    i, _, f = s.partition(".")
    i = num(int(i)) if i not in ("", "-") else i
    return i + ("." + f if f else "")


def dec(n, places):
    return Dm(n) / (Dm(10) ** places)


def shift(x, k):
    return Dm(x) * (Dm(10) ** k)


def s1(seen):
    def mk():
        a = R.randint(12, 999)
        p = R.choice([1, 2])
        n = R.randint(2, 30)
        x = dec(a, p)
        if a % 10 == 0:
            return None
        v = x * n
        order = R.random() < .5
        q = ("%s × %d ＝" % (D(x), n)) if order else ("%d × %s ＝" % (n, D(x)))
        return mcq(q, D(v), [D(shift(v, 1)), D(shift(v, -1)), D(a * n), D(v + 1)],
                   "先當整數算：%d × %d ＝ %s，小數有 %d 位，答案也要 %d 位小數：%s。" % (a, n, num(a * n), p, p, D(v)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        a, b = R.randint(2, 99), R.randint(2, 99)
        pa, pb = R.choice([1, 1, 2]), 1
        if a % 10 == 0 or b % 10 == 0:
            return None
        x, y = dec(a, pa), dec(b, pb)
        v = x * y
        q = "%s × %s ＝" % (D(x), D(y))
        return mcq(q, D(v), [D(shift(v, 1)), D(shift(v, -1)), D(a * b), D(shift(v, 2)) if pa + pb > 2 else D(v + Dm("0.1"))],
                   "先算 %d × %d ＝ %s，兩個數的小數一共 %d 位，答案點 %d 位小數：%s。" % (a, b, num(a * b), pa + pb, pa + pb, D(v)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a = R.randint(11, 999)
        b = R.randint(11, 99)
        pa, pb = R.choice([1, 2]), R.choice([1, 2])
        if a % 10 == 0 or b % 10 == 0 or pa + pb > 4:
            return None
        x, y = dec(a, pa), dec(b, pb)
        v = x * y
        q = "%s × %s ＝" % (D(x), D(y))
        return mcq(q, D(v), [D(shift(v, 1)), D(shift(v, -1)), D(shift(v, 2)), D(x + y)],
                   "整數乘法 %d × %d ＝ %s，小數位數 %d ＋ %d ＝ %d 位：%s。" % (a, b, num(a * b), pa, pb, pa + pb, D(v)))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def bigger():
        n = R.randint(20, 900)
        f = dec(R.randint(1, 99), 2) if R.random() < .5 else 1 + dec(R.randint(1, 99), 2)
        if f == 1:
            return None
        q = "不用算出答案，%d × %s 比 %d 大還是小？" % (n, D(f), n)
        ans = "比 %d 大" % n if f > 1 else "比 %d 小" % n
        return mcq(q, ans, ["比 %d 小" % n if f > 1 else "比 %d 大" % n, "一樣大", "要算出來才知道"], "乘以比 1 大的數，積變大；乘以比 1 小的數，積變小。%s %s 1。" % (D(f), ">" if f > 1 else "<"))

    def zero():
        a = R.randint(2, 99) * 10 + R.choice([0, 5])
        b = R.randint(2, 9) * 2
        x, y = dec(a, 2), dec(b, 1)
        if (a * b) % 10:
            return None
        v = x * y
        q = "%s × %s ＝" % (D(x), D(y))
        return mcq(q, D(v), [D(shift(v, 1)), D(shift(v, -1)), D(v + Dm("0.01"))], "%d × %d ＝ %s，點 3 位小數後，尾巴的 0 可以去掉：%s。" % (a, b, num(a * b), D(v)))
    return pick_unique(R, bigger, 10, seen) + pick_unique(R, zero, 10, seen)


def s5(seen):
    def price():
        it, lo, hi = R.choice([("香蕉", 30, 60), ("芭樂", 40, 80), ("豬肉", 180, 280), ("白米", 50, 90), ("蘋果", 80, 150)])
        p = dec(R.randint(lo, hi), 0)
        kg = dec(R.randint(12, 59), 1)
        q = "%s每公斤 %s 元，買 %s 公斤，要付多少元？" % (it, D(p), D(kg))
        v = p * kg
        return mcq(q, D(v) + " 元", [D(x) + " 元" for x in (shift(v, 1), shift(v, -1), p + kg)], "%s × %s ＝ %s（元）。" % (D(p), D(kg), D(v)))

    def area():
        w, h = dec(R.randint(12, 99), 1), dec(R.randint(12, 99), 1)
        q = "長 %s 公尺、寬 %s 公尺的長方形，面積是多少平方公尺？" % (D(w), D(h))
        v = w * h
        return mcq(q, D(v) + " 平方公尺", [D(x) + " 平方公尺" for x in (shift(v, 1), (w + h) * 2, w + h)], "%s × %s ＝ %s（平方公尺）。" % (D(w), D(h), D(v)))

    def run():
        lap = dec(R.randint(2, 9) * 100 + R.choice([0, 50]), 3)
        n = dec(R.randint(15, 95), 1)
        q = "操場一圈 %s 公里，%s跑了 %s 圈，跑了幾公里？" % (D(lap), NM.next(), D(n))
        v = lap * n
        return mcq(q, D(v) + " 公里", [D(x) + " 公里" for x in (shift(v, 1), shift(v, -1), lap + n)], "%s × %s ＝ %s（公里）。" % (D(lap), D(n), D(v)))
    return pick_unique(R, price, 7, seen) + pick_unique(R, area, 7, seen) + pick_unique(R, run, 6, seen)


def main():
    seen = set()
    sets = [("小數 × 整數", s1(seen)), ("小數 × 小數（一）", s2(seen)), ("小數 × 小數（二）", s3(seen)),
            ("積的大小和尾巴的 0", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["小數乘法的直式：<b>先不看小數點，當成整數乘</b>。",
         "再數兩個乘數<b>一共有幾位小數</b>，答案就從右邊數幾位點上小數點。不用把小數點對齊。",
         "乘以比 1 小的小數，積會<b>變小</b>；乘以比 1 大的數，積才變大。"],
        [example("2.35 × 1.4 ＝", ["235 × 14 ＝ 3290。", "小數一共 2 ＋ 1 ＝ 3 位：3.290 ＝ 3.29。"], "3.29"),
         example("0.6 × 0.3 ＝", ["6 × 3 ＝ 18。", "小數一共 2 位：0.18。"], "0.18")],
        [("0.6 × 0.3 ＝ 1.8", "小數一共 2 位：0.18"),
         ("像加法一樣把小數點對齊再乘", "乘法不用對齊，先當整數乘，最後數位數"),
         ("乘完一定比原來大", "乘以 0.5 就是一半，會變小")])
    faq = [{"q": "小數乘法的小數點怎麼點？",
            "a": "先當整數算，再數兩個乘數的小數位數加起來有幾位，從積的右邊數幾位點上小數點。位數不夠時在前面補 0。"},
           {"q": "為什麼乘以 0.4 答案會變小？",
            "a": "乘以 0.4 是取 10 份中的 4 份，比原來少，所以積比被乘數小。"},
           {"q": "五年級的小數乘法要學什麼？",
            "a": "108課綱 N-5-8：整數乘以小數、小數乘以小數的意義和直式計算，並知道積不一定比被乘數大。"}]
    make_unit(R, "grade-5", "multiplying-decimals", "N-5-8",
              "小數的乘法：整數乘以小數、小數乘以小數的意義。乘數為小數的直式計算。教師用位值的概念說明直式計算的合理性。處理乘積一定比被乘數大的錯誤類型。",
              "小數的乘法",
              "五年級數學 小數乘法 練習題｜小數乘整數・小數乘小數・小數點位置 學習單（附解答）",
              "小數的乘法",
              "國小五年級數學「小數的乘法」免費學習單：小數乘以整數、小數乘以小數的直式、小數點的位置、積會變大還是變小與應用題。100題線上練習馬上對答案，附可列印解答。",
              "先當整數乘，再數小數位數",
              "乘數的小數位數加起來，就是積的小數位數。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
