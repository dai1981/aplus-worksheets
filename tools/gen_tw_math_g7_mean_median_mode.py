# -*- coding: utf-8 -*-
"""
台灣 國中七年級 數學：平均數、中位數、眾數（108課綱 D-7-2）
  python3 tools/gen_tw_math_g7_mean_median_mode.py
平均數（總和÷個數）、中位數（排序して真ん中、偶數個は中間二數の平均）、眾數（最も多い）、次數分配表からの平均數、極端值の影響と代表值の選び方。
誤答：中位數で並べ替えない、偶數個で片方だけ取る、眾數を次數で答える、表からの平均で組數で割る。
"""
import random
from fractions import Fraction as F
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, table, num, dnum
from tw_g7 import sn, tidy_sets

R = random.Random(71026)
NM = Names(R)


def fs(x):
    x = F(x)
    return num(x.numerator) if x.denominator == 1 else dnum(float(x), 2)


def s1(seen):
    def mk():
        n = R.choice([5, 6, 8])
        xs = [R.randint(50, 100) for _ in range(n)]
        t = sum(xs)
        if t % n and (F(t, n) * 10).denominator != 1:
            return None
        m = F(t, n)
        q = "%s %d 次小考的成績是 %s。平均數是多少分？" % (NM.next(), n, "、".join(map(str, xs)))
        return mcq(q, "%s 分" % fs(m), ["%s 分" % fs(x) for x in (F(t, n - 1), F(max(xs) + min(xs), 2), m + 1)  if x != m], "平均數 ＝ 總和 ÷ 個數 ＝ %d ÷ %d ＝ %s。" % (t, n, fs(m)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.choice([5, 7, 6, 8])
        xs = R.sample(range(10, 60), n)
        s = sorted(xs)
        if n % 2:
            med = F(s[n // 2])
            e = "由小到大排：%s，正中間是第 %d 個：%s。" % ("、".join(map(str, s)), n // 2 + 1, fs(med))
        else:
            med = F(s[n // 2 - 1] + s[n // 2], 2)
            e = "由小到大排：%s，中間兩個是 %d 和 %d，平均是 %s。" % ("、".join(map(str, s)), s[n // 2 - 1], s[n // 2], fs(med))
        w = [xs[n // 2], s[n // 2 - 1] if n % 2 == 0 else s[n // 2 - 1], F(sum(xs), n)]
        return mcq("資料：%s。中位數是多少？" % "、".join(map(str, xs)), fs(med), [fs(x) for x in w if F(x) != med] + [fs(med + 1)], e)
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        base = R.sample(range(1, 20), 4)
        mode = R.choice(base)
        xs = base + [mode, mode] + [R.choice([b for b in base if b != mode])]
        R.shuffle(xs)
        cnt = xs.count(mode)
        if any(xs.count(b) >= cnt for b in base if b != mode):
            return None
        return mcq("資料：%s。眾數是多少？" % "、".join(map(str, xs)), str(mode), [str(cnt), str(max(xs)), str(sorted(xs)[len(xs) // 2]) if sorted(xs)[len(xs) // 2] != mode else str(min(xs))], "%d 出現 %d 次，最多，所以眾數是 %d（不是 %d）。" % (mode, cnt, mode, cnt))

    def shoe():
        sizes = [22, 22.5, 23, 23.5, 24, 24.5, 25]
        cnts = [R.randint(1, 12) for _ in sizes]
        m = max(cnts)
        if cnts.count(m) > 1:
            return None
        j = cnts.index(m)
        tb = table(["鞋號（公分）"] + [dnum(x) for x in sizes], [["人數"] + [str(c) for c in cnts]])
        q = "鞋店統計賣出的鞋號，眾數是多少？" + tb
        return mcq(q, dnum(sizes[j]), [str(m), dnum(sizes[3]) if j != 3 else dnum(sizes[2]), dnum(sizes[-1]) if j != 6 else dnum(sizes[0])], "賣出最多的是 %s 號（%d 雙），眾數是 %s。" % (dnum(sizes[j]), m, dnum(sizes[j])))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, shoe, 8, seen)


def s4(seen):
    def mk():
        vals = R.choice([[60, 70, 80, 90, 100], [1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [10, 20, 30, 40, 50]])
        cs = [R.randint(1, 10) for _ in vals]
        n = sum(cs)
        t = sum(v * c for v, c in zip(vals, cs))
        m = F(t, n)
        if (m * 100).denominator != 1:
            return None
        tb = table(["分數"] + [str(v) for v in vals], [["人數"] + [str(c) for c in cs]])
        q = "下表是一次小測驗的結果，平均數是多少？" + tb
        return mcq(q, fs(m), [fs(x) for x in (F(sum(vals), len(vals)), F(t, len(vals)), m + 1)  if x != m], "總分 ＝ %s ＝ %d，人數 %d，%d ÷ %d ＝ %s。" % (" ＋ ".join("%d × %d" % (v, c) for v, c in zip(vals, cs)), t, n, t, n, fs(m)))

    def med_tb():
        vals = [1, 2, 3, 4, 5]
        cs = [R.randint(1, 8) for _ in vals]
        n = sum(cs)
        arr = [v for v, c in zip(vals, cs) for _ in range(c)]
        med = F(arr[n // 2]) if n % 2 else F(arr[n // 2 - 1] + arr[n // 2], 2)
        tb = table(["每週閱讀本數"] + [str(v) for v in vals], [["人數"] + [str(c) for c in cs]])
        q = "下表中，每週閱讀本數的中位數是多少？" + tb
        return mcq(q, fs(med), [fs(x) for x in (3, F(n, 2), max(cs))  if F(x) != med] + [fs(med + 1)], "共 %d 人，中位數是第 %s 個數，由小到大數到那裡是 %s。" % (n, str(n // 2 + 1) if n % 2 else "%d、%d" % (n // 2, n // 2 + 1), fs(med)))
    return pick_unique(R, mk, 12, seen) + pick_unique(R, med_tb, 8, seen)


def s5(seen):
    def outlier():
        xs = [R.randint(25, 35) for _ in range(5)]
        big = R.choice([200, 300, 500])
        ys = xs + [big]
        mean = F(sum(ys), 6)
        s = sorted(ys)
        med = F(s[2] + s[3], 2)
        q = "六位員工的月薪（千元）是 %s。用哪一個代表值比較能代表「一般員工」的月薪？" % "、".join(map(str, ys))
        return mcq(q, "中位數", ["平均數", "最大值", "全距"], "有一個特別大的 %d，平均數被拉高到 %s；中位數 %s 不受極端值影響。" % (big, fs(mean), fs(med)))

    def need():
        n = R.choice([4, 5])
        avg = R.choice([80, 85, 90])
        got = [R.randint(70, 98) for _ in range(n - 1)]
        x = avg * n - sum(got)
        if not 60 <= x <= 100:
            return None
        q = "%s前 %d 次成績是 %s，想讓 %d 次平均剛好 %d 分，第 %d 次要考幾分？" % (NM.next(), n - 1, "、".join(map(str, got)), n, avg, n)
        return mcq(q, "%d 分" % x, ["%d 分" % t for t in (avg, x + 1, avg * (n - 1) - sum(got) if avg * (n - 1) - sum(got) > 0 else x - 2)  if t != x], "總分要 %d × %d ＝ %d，%d － %d ＝ %d。" % (avg, n, avg * n, avg * n, sum(got), x))

    def add():
        n = R.randint(4, 9)
        avg = R.randint(40, 60)
        new = avg + R.choice([-1, 1]) * (n + 1) * R.randint(1, 3)
        na = F(avg * n + new, n + 1)
        q = "%d 個人的平均體重是 %d 公斤，加入一位 %d 公斤的人後，平均是多少公斤？" % (n, avg, new)
        return mcq(q, "%s 公斤" % fs(na), ["%s 公斤" % fs(x) for x in (F(avg + new, 2), avg, na + 1)  if x != na], "（%d × %d ＋ %d）÷ %d ＝ %s。" % (avg, n, new, n + 1, fs(na)))
    return pick_unique(R, outlier, 4, seen) + pick_unique(R, need, 8, seen) + pick_unique(R, add, 8, seen)


def main():
    seen = set()
    sets = [("平均數", s1(seen)), ("中位數", s2(seen)), ("眾數", s3(seen)),
            ("從次數分配表求", s4(seen)), ("代表值的選擇與應用", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>平均數</b> ＝ 總和 ÷ 個數。",
         "<b>中位數</b>：<b>先由小到大排好</b>，取正中間；偶數個取中間兩個的平均。",
         "<b>眾數</b>：出現次數最多的那個<b>資料值</b>（不是次數）。",
         "有特別大或特別小的極端值時，平均數會被拉動，中位數比較能代表一般情形。"],
        [example("資料 3、8、5、10、6，中位數？", ["排好：3、5、6、8、10。"], "6"),
         example("資料 2、4、7、9，中位數？", ["中間兩個 4 和 7。", "（4 ＋ 7）÷ 2。"], "5.5")],
        [("沒有排序就取中間", "一定要先由小到大排"),
         ("眾數回答出現的次數", "眾數是那個數值本身"),
         ("從表求平均，總和除以組數", "要除以總人數")])
    faq = [{"q": "平均數、中位數、眾數有什麼不同？",
            "a": "平均數用到所有資料；中位數是排序後的正中間，不受極端值影響；眾數是出現最多次的值，適合看最受歡迎的選項，例如鞋號。"},
           {"q": "資料有偶數個時，中位數怎麼算？",
            "a": "先由小到大排序，取中間兩個數的平均。"},
           {"q": "七年級的統計數據要學什麼？",
            "a": "108課綱 D-7-2：用平均數、中位數與眾數描述一組資料的特性，並可使用計算機的「M+」或「Σ」鍵計算平均數。"}]
    make_unit(R, "grade-7", "mean-median-mode", "D-7-2",
              "統計數據：用平均數、中位數與眾數描述一組資料的特性；使用計算機的「M+」或「Σ」鍵計算平均數。",
              "平均數、中位數、眾數",
              "七年級數學 平均數中位數眾數 練習題｜次數分配表・極端值 學習單（附解答）",
              "平均數、中位數、眾數",
              "國中七年級數學「平均數、中位數、眾數」免費學習單：求平均數、中位數（偶數個取中間兩數平均）、眾數，從次數分配表求代表值，以及極端值和代表值的選擇。100題線上練習馬上對答案，附可列印解答。",
              "中位數要先由小到大排好",
              "眾數是出現最多次的資料值，不是次數。",
              body, faq, sets, 26)


if __name__ == "__main__":
    main()
