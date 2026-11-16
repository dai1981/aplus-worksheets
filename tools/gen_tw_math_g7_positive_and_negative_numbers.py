# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：正數與負數（108課綱 N-7-3）
  python3 tools/gen_tw_math_g7_positive_and_negative_numbers.py
生活の量を正・負で表す（收入・支出、海拔、溫度、上升・下降）、相反數、正數・負數・0 の分類、大小比較、應用（溫差・變化量）。
誤答：基準の向きを逆にする、0 を正數とする、－5 と －3 で 5 が大きいから －5 が大きいとする、相反數を倒數と混同。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, dnum
from tw_g7 import sn, par, opv, tidy_sets

R = random.Random(71001)
NM = Names(R)


def s1(seen):
    CTX = [("收入 %d 元記作 ＋%d 元，那麼支出 %d 元記作？", "元"), ("向東走 %d 公尺記作 ＋%d 公尺，那麼向西走 %d 公尺記作？", "公尺"),
           ("海平面以上 %d 公尺記作 ＋%d 公尺，那麼海平面以下 %d 公尺記作？", "公尺"), ("零上 %d 度記作 ＋%d ℃，那麼零下 %d 度記作？", "℃"),
           ("存入 %d 元記作 ＋%d 元，那麼提出 %d 元記作？", "元"), ("水位上升 %d 公分記作 ＋%d 公分，那麼下降 %d 公分記作？", "公分"),
           ("體重增加 %d 公斤記作 ＋%d 公斤，那麼減少 %d 公斤記作？", "公斤"), ("比標準多 %d 分記作 ＋%d 分，那麼比標準少 %d 分記作？", "分")]

    def mk():
        t, u = R.choice(CTX)
        hi = 6 if "體重" in t else (40 if "℃" in u else 50)
        a, b = R.randint(2, hi), R.randint(2, hi)
        if a == b:
            return None
        q = t % (a, a, b)
        sp = "" if u == "℃" else " "
        ans = "－%d%s%s" % (b, sp, u)
        return mcq(q, ans, ["＋%d%s%s" % (b, sp, u), "－%d%s%s" % (a, sp, u), "%d%s%s" % (b - a if b > a else a - b, sp, u)], "相反意義的量用負數表示：%s。" % ans)
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def opp():
        v = F(R.choice([R.randint(1, 60), -R.randint(1, 60)]))
        if R.random() < .3:
            v = F(R.randint(1, 9), R.choice([2, 3, 4, 5])) * R.choice([1, -1])
            if v.denominator == 1:
                return None
        return mcq("%s 的相反數是多少？" % sn(v), sn(-v), [sn(v), sn(1 / v) if v != 0 else "0", sn(-1 / v)], "相反數只改變正負號：%s 的相反數是 %s。" % (sn(v), sn(-v)))

    def zero():
        F_ = [("0 的相反數是多少？", "0", ["－0", "1", "沒有相反數"], "0 的相反數還是 0。"),
              ("兩個數互為相反數，它們的和是多少？", "0", ["1", "－1", "不一定"], "a ＋（－a）＝ 0。"),
              ("在數線上，互為相反數的兩點有什麼特點？", "在原點兩側，到原點距離相等", ["在原點同一側", "其中一點一定是 0", "距離原點不一樣遠"], "相反數到原點的距離一樣，只是方向相反。"),
              ("－（－7）等於多少？", "7", ["－7", "0", "－（7）"], "－7 的相反數是 7。")]
        return mcq(*R.choice(F_))
    return pick_unique(R, opp, 16, seen) + pick_unique(R, zero, 4, seen)


def s3(seen):
    def mk():
        nums = [R.randint(1, 30), -R.randint(1, 30), 0, F(R.randint(1, 9), R.choice([2, 3, 4])), -F(R.randint(1, 9), 10)]
        nums = [F(x) for x in nums]
        R.shuffle(nums)
        kind = R.choice(["neg", "pos", "int"])
        txt = "、".join(sn(x) if x.denominator in (1, 2, 3, 4) else ("－" + dnum(float(-x))) for x in nums)
        if kind == "neg":
            cnt = sum(1 for x in nums if x < 0)
            q = "%s 中，負數有幾個？" % txt
            e = "比 0 小的數才是負數；0 不是正數也不是負數。"
        elif kind == "pos":
            cnt = sum(1 for x in nums if x > 0)
            q = "%s 中，正數有幾個？" % txt
            e = "比 0 大的數是正數；0 不是正數。"
        else:
            cnt = sum(1 for x in nums if x.denominator == 1)
            q = "%s 中，整數有幾個？" % txt
            e = "正整數、0、負整數都是整數。"
        return mcq(q, "%d 個" % cnt, ["%d 個" % x for x in (cnt + 1, cnt - 1 if cnt > 1 else cnt + 2, 5)  if x != cnt], e)
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        a, b = R.sample(range(-30, 31), 2)
        if a * b > 0 and R.random() < .3:
            pass
        kind = R.choice(["big", "small"])
        if a >= 0 and b >= 0:
            return None
        q = "%s 和 %s，哪一個比較%s？" % (sn(a), sn(b), "大" if kind == "big" else "小")
        ans = max(a, b) if kind == "big" else min(a, b)
        oth = min(a, b) if kind == "big" else max(a, b)
        return mcq(q, sn(ans), [sn(oth), "一樣大", sn(-ans) if -ans != oth else sn(abs(ans) + 1)], ("兩個都是負數，離 0 越遠越小" if a < 0 and b < 0 else "正數和 0 都比負數大") + "：%s ＞ %s。" % (sn(max(a, b)), sn(min(a, b))))

    def order():
        xs = R.sample(range(-20, 21), 4)
        if all(x >= 0 for x in xs):
            return None
        sx = sorted(xs)
        ans = " ＜ ".join(sn(x) for x in sx)
        w1 = " ＜ ".join(sn(x) for x in sorted(xs, key=abs))
        w2 = " ＜ ".join(sn(x) for x in sorted(xs, reverse=True))
        w3 = " ＜ ".join(sn(x) for x in sorted([x for x in xs if x >= 0]) + sorted([x for x in xs if x < 0], key=abs))
        return mcq("由小到大排列：%s" % "、".join(sn(x) for x in xs), ans, [w for w in (w1, w2, w3) if w != ans] + [" ＜ ".join(sn(x) for x in sx[::-1])], "負數比 0 小，0 比正數小；負數中離 0 越遠越小。")
    return pick_unique(R, mk, 12, seen) + pick_unique(R, order, 8, seen)


def s5(seen):
    def temp():
        hi, lo = R.randint(-5, 25), R.randint(-15, 10)
        if hi <= lo or lo >= 0 or not 5 <= hi - lo <= 15:
            return None
        city = R.choice(["合歡山", "玉山", "北京", "首爾", "東京"])
        q = "%s某天最高氣溫 %s ℃，最低氣溫 %s ℃。溫差是多少度？" % (city, sn(hi), sn(lo))
        d = hi - lo
        return mcq(q, "%d 度" % d, ["%d 度" % x for x in (abs(hi + lo) if abs(hi + lo) != d else d + 2, hi, d + 1)  if x != d], "溫差 ＝ 最高 － 最低 ＝ %s%s ＝ %d（度）。" % (sn(hi), opv("－", lo), d))

    def score():
        std = R.choice([60, 70, 80])
        diffs = [R.randint(-12, 12) for _ in range(4)]
        if 0 in diffs or len(set(diffs)) < 4:
            return None
        names = ["甲", "乙", "丙", "丁"]
        i = R.randrange(4)
        q = "以 %d 分為標準，高於標準記正、低於標準記負。四人的紀錄是 %s。%s實際考幾分？" % (std, "、".join("%s %s" % (n, ("＋" if d > 0 else "") + sn(d)) for n, d in zip(names, diffs)), names[i])
        v = std + diffs[i]
        return mcq(q, "%d 分" % v, ["%d 分" % x for x in (std - diffs[i], abs(diffs[i]), v + 1)  if x != v], "%d%s ＝ %d（分）。" % (std, opv("＋", diffs[i]), v))

    def elev():
        a = R.randint(100, 3900)
        b = R.randint(5, 400)
        q = "山頂海拔 %s 公尺，海底某處海拔 －%d 公尺。兩地相差多少公尺？" % (a, b)
        return mcq(q, "%d 公尺" % (a + b), ["%d 公尺" % x for x in (a - b, a, b)], "%d －（－%d）＝ %d ＋ %d ＝ %d（公尺）。" % (a, b, a, b, a + b))
    return pick_unique(R, temp, 7, seen) + pick_unique(R, score, 7, seen) + pick_unique(R, elev, 6, seen)


def main():
    seen = set()
    sets = [("用正負數表示生活中的量", s1(seen)), ("相反數", s2(seen)), ("正數、負數、0 和整數", s3(seen)),
            ("比較大小", s4(seen)), ("應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["有相反意義的量，一個用<b>正數</b>表示，另一個就用<b>負數</b>表示：收入 ＋100 元，支出 －100 元。",
         "<b>0 不是正數也不是負數</b>。正整數、0、負整數合起來是整數。",
         "只差一個負號的兩數互為<b>相反數</b>，例如 5 和 －5；0 的相反數是 0。",
         "數線上越右邊越大；負數中，離 0 越遠越小（－8 ＜ －3）。"],
        [example("零上 6 度記作 ＋6 ℃，零下 4 度記作？", ["相反意義用負數。"], "－4 ℃"),
         example("比較 －7 和 －2 的大小。", ["－2 離 0 比較近，在 －7 的右邊。"], "－7 ＜ －2")],
        [("－8 比 －3 大，因為 8 比 3 大", "負數離 0 越遠越小：－8 ＜ －3"),
         ("0 是正數", "0 不是正數也不是負數"),
         ("－5 的相反數是 <span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span>", "相反數是 5；<span class='fr'><span class='fn'>1</span><span class='fd'>5</span></span> 是倒數的概念")])
    faq = [{"q": "什麼是負數？",
            "a": "比 0 小的數，前面加上負號，例如 －3、－2.5。生活中常用來表示和正數相反意義的量，例如支出、零下溫度、海平面以下。"},
           {"q": "相反數和倒數有什麼不同？",
            "a": "相反數是改變正負號（5 和 －5，和為 0）；倒數是分子分母對調（5 和 1/5，積為 1）。"},
           {"q": "七年級的負數要學什麼？",
            "a": "108課綱 N-7-3：使用「正、負」表徵生活中的量、相反數，以及含分數、小數的四則混合運算。"}]
    make_unit(R, "grade-7", "positive-and-negative-numbers", "N-7-3",
              "負數與數的四則混合運算（含分數、小數）：使用「正、負」表徵生活中的量；相反數；數的四則混合運算。",
              "正數與負數：相反數、比較大小",
              "七年級數學 正數與負數 練習題｜相反數・比較大小・溫差 學習單（附解答）",
              "正數與負數",
              "國中七年級數學「正數與負數」免費學習單：用正負數表示生活中的量、相反數、正數、負數和整數的分類、比較大小與溫差、海拔等應用題。100題線上練習馬上對答案，附可列印解答。",
              "相反意義的量，一個用正數，另一個用負數",
              "0 不是正數也不是負數；負數離 0 越遠越小。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
