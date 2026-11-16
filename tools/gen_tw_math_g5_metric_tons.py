# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：重量「公噸」（108課綱 N-5-13）
  python3 tools/gen_tw_math_g5_metric_tons.py
1 公噸＝1000 公斤、複名數と小數の換算、量感、比較、加減乘除、概數を使った應用（トラック・ゾウ・米）。
誤答：1 公噸＝100 公斤、3 公噸 50 公斤→350 公斤、小數の換算で桁ずれ。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, dnum
from tw_g3_measure import bs

R = random.Random(51014)
NM = Names(R)


def T(v):
    return bs(v, "公噸", "公斤")


def s1(seen):
    def mk():
        n = R.randint(2, 60)
        if R.random() < .5:
            return mcq("%d 公噸 ＝ ___ 公斤" % n, num(n * 1000), [num(n * 100), num(n * 10000), num(n * 10)], "1 公噸 ＝ 1000 公斤，%d 公噸 ＝ %s 公斤。" % (n, num(n * 1000)))
        return mcq("%s 公斤 ＝ ___ 公噸" % num(n * 1000), str(n), [str(n * 10), num(n * 100), dnum(n / 10, 1)], "1000 公斤 ＝ 1 公噸，%s 公斤 ＝ %d 公噸。" % (num(n * 1000), n))

    def mixed():
        a, b = R.randint(1, 20), R.choice([R.randint(1, 9) * 100, R.randint(11, 99) * 10, R.randint(1, 99)])
        v = a * 1000 + b
        return mcq("%d 公噸 %d 公斤 ＝ ___ 公斤" % (a, b), num(v), [num(int("%d%d" % (a, b))), num(a * 100 + b), num(v + 1000)], "%d 公噸 ＝ %s 公斤，再加 %d：%s 公斤。" % (a, num(a * 1000), b, num(v)))
    return pick_unique(R, mk, 10, seen) + pick_unique(R, mixed, 10, seen)


def s2(seen):
    def mk():
        x = R.randint(11, 199) / 10 if R.random() < .6 else R.randint(101, 999) / 100
        kg = int(round(x * 1000))
        if R.random() < .5:
            return mcq("%s 公噸 ＝ ___ 公斤" % dnum(x, 2), num(kg), [num(kg // 10), num(kg * 10), num(int(str(dnum(x, 2)).replace(".", "")))] if num(int(str(dnum(x, 2)).replace(".", ""))) != num(kg) else [num(kg // 10), num(kg * 10), num(kg + 100)],
                       "%s × 1000 ＝ %s（公斤）。" % (dnum(x, 2), num(kg)))
        return mcq("%s 公斤 ＝ ___ 公噸（用小數表示）" % num(kg), dnum(x, 2), [dnum(x * 10, 1), dnum(x / 10, 3), T(kg)], "%s ÷ 1000 ＝ %s（公噸）。" % (num(kg), dnum(x, 2)))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    SENSE = [("一頭大象", "5", "公噸"), ("一輛小汽車", "1.5", "公噸"), ("一個五年級學生", "38", "公斤"), ("一輛大卡車載滿貨物", "20", "公噸"),
             ("一頭牛", "600", "公斤"), ("一架大飛機", "300", "公噸"), ("一包米", "3", "公斤"), ("一隻藍鯨", "150", "公噸")]
    out = []
    for it, n, u in SENSE:
        out.append(mcq("%s大約重 %s ___，填哪一個單位最合適？" % (it, n), u, [x for x in ("公噸", "公斤", "公克", "公升") if x != u], "想一想有多重：%s大約 %s %s。" % (it, n, u)))
    for o in out:
        seen.add(o["q"])

    def cmp_():
        a = R.randint(1, 20) * 1000 + R.randint(1, 19) * 50
        b = a + R.choice([-900, -50, 100, 950, 1000])
        if b <= 0:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s 公斤，○ 裡要填什麼？" % (T(a), num(b)), sign, ["<" if sign == ">" else ">", "=", "無法比較"], "%s ＝ %s 公斤，%s %s %s。" % (T(a), num(a), num(a), sign, num(b)))
    return out + pick_unique(R, cmp_, 12, seen)


def s4(seen):
    def add():
        a = R.randint(1, 9) * 1000 + R.randint(1, 9) * 100
        b = R.randint(1, 9) * 1000 + R.randint(1, 9) * 100
        if R.random() < .5:
            s = a + b
            return mcq("%s ＋ %s ＝" % (T(a), T(b)), T(s), ["%d 公噸 %d 公斤" % (a // 1000 + b // 1000, a % 1000 + b % 1000) if a % 1000 + b % 1000 >= 1000 else T(s + 1000), T(s - 1000), T(s + 100)], "公噸加公噸、公斤加公斤，滿 1000 公斤進 1 公噸：%s。" % T(s))
        if a <= b:
            a, b = b, a
        d = a - b
        if d < 100:
            return None
        return mcq("%s － %s ＝" % (T(a), T(b)), T(d), ["%d 公噸 %d 公斤" % (a // 1000 - b // 1000, abs(a % 1000 - b % 1000)) if a % 1000 < b % 1000 else T(d + 100), T(d + 1000), T(d - 100) if d > 100 else T(d + 200)], "公斤不夠減，向公噸借 1 公噸 ＝ 1000 公斤：%s。" % T(d))

    def mul():
        per = R.choice([250, 400, 500, 750, 800, 1200, 1500])
        n = R.randint(3, 20)
        q = "一箱貨物重 %s 公斤，%d 箱一共重幾公噸？" % (num(per), n)
        v = per * n
        return mcq(q, dnum(v / 1000, 3) + " 公噸", [dnum(v / 100, 2) + " 公噸", dnum(v / 10000, 4) + " 公噸", num(v) + " 公噸"], "%s × %d ＝ %s 公斤 ＝ %s 公噸。" % (num(per), n, num(v), dnum(v / 1000, 3)))
    return pick_unique(R, add, 12, seen) + pick_unique(R, mul, 8, seen)


def s5(seen):
    def truck():
        cap = R.choice([3, 5, 8, 10, 12])
        load = R.randint(cap * 3, cap * 12) * 1000 + R.randint(1, 9) * 100
        q = "一輛卡車每次最多載 %d 公噸，要把 %s 公斤的沙全部載完，至少要載幾次？" % (cap, num(load))
        v = -(-load // (cap * 1000))
        return mcq(q, "%d 次" % v, ["%d 次" % x for x in (v - 1, v + 1, load // cap // 100)], "%s 公斤 ＝ %s 公噸，%s ÷ %d ＝ %s…，剩下的也要載，要 %d 次。" % (num(load), dnum(load / 1000, 1), dnum(load / 1000, 1), cap, dnum(load / 1000 / cap, 2), v))

    def bridge():
        lim = R.choice([10, 15, 20, 25])
        car = R.randint(lim * 1000 - 3000, lim * 1000 + 3000)
        car = car // 100 * 100
        if car == lim * 1000:
            return None
        q = "一座橋限重 %d 公噸，一輛卡車連貨物重 %s 公斤，可以通過嗎？" % (lim, num(car))
        ok = car <= lim * 1000
        return mcq(q, "可以" if ok else "不可以", ["不可以" if ok else "可以", "要看卡車多長", "無法判斷"], "%d 公噸 ＝ %s 公斤，%s %s %s，%s。" % (lim, num(lim * 1000), num(car), "≤" if ok else ">", num(lim * 1000), "沒有超過限重" if ok else "超過限重"))

    def rice():
        per = R.randint(40, 70)
        ppl = R.choice([100, 200, 500, 1000, 2000])
        q = "每人一年大約吃 %d 公斤的米，%s 人一年大約吃幾公噸的米？" % (per, num(ppl))
        v = per * ppl
        return mcq(q, dnum(v / 1000, 2) + " 公噸", [num(v) + " 公噸", dnum(v / 100, 1) + " 公噸", dnum(v / 10000, 3) + " 公噸"], "%d × %s ＝ %s 公斤 ＝ %s 公噸。" % (per, num(ppl), num(v), dnum(v / 1000, 2)))
    return pick_unique(R, truck, 7, seen) + pick_unique(R, bridge, 6, seen) + pick_unique(R, rice, 7, seen)


def main():
    seen = set()
    sets = [("公噸和公斤的換算", s1(seen)), ("小數的公噸", s2(seen)), ("量感和比輕重", s3(seen)), ("重量的計算", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["很重的東西用<b>公噸</b>：<b>1 公噸 ＝ 1000 公斤</b>。一頭大象大約 5 公噸。",
         "3 公噸 50 公斤 ＝ 3000 ＋ 50 ＝ 3050 公斤；2.4 公噸 ＝ 2.4 × 1000 ＝ 2400 公斤。",
         "比較、計算時先換成同一個單位，算出來可以再換回公噸。"],
        [example("4 公噸 80 公斤 ＝ ___ 公斤", ["4 公噸 ＝ 4000 公斤。", "4000 ＋ 80 ＝ 4080。"], "4080"),
         example("一箱 750 公斤，12 箱是幾公噸？", ["750 × 12 ＝ 9000 公斤。", "9000 ÷ 1000 ＝ 9。"], "9 公噸")],
        [("1 公噸 ＝ 100 公斤", "1 公噸 ＝ 1000 公斤"),
         ("3 公噸 50 公斤 ＝ 350 公斤", "3000 ＋ 50 ＝ 3050 公斤"),
         ("2.4 公噸 ＝ 240 公斤", "2.4 × 1000 ＝ 2400 公斤")])
    faq = [{"q": "1 公噸等於多少公斤？",
            "a": "1 公噸 ＝ 1000 公斤。一頭大象大約 5 公噸，一輛小汽車大約 1.5 公噸。"},
           {"q": "五年級的公噸要學什麼？",
            "a": "108課綱 N-5-13：認識公噸，在生活實例中應用，並和公斤換算與計算，可以使用概數。"},
           {"q": "小數的公噸怎麼換成公斤？",
            "a": "乘以 1000，小數點往右移 3 位：2.45 公噸 ＝ 2450 公斤。"}]
    make_unit(R, "grade-5", "metric-tons", "N-5-13",
              "重量：「公噸」。生活實例之應用。含與「公斤」的換算與計算。使用概數。",
              "重量：公噸和公斤",
              "五年級數學 公噸 練習題｜公噸和公斤換算・重量計算 學習單（附解答）",
              "公噸和公斤",
              "國小五年級數學「公噸」免費學習單：公噸和公斤的換算、小數的公噸、量感和比輕重、重量的計算與卡車、限重等應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 公噸 ＝ 1000 公斤",
              "公噸換公斤，小數點往右移 3 位。",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
