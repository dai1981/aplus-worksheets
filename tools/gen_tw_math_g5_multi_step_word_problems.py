# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：多步驟應用問題（108課綱 N-5-2）
  python3 tools/gen_tw_math_g5_multi_step_word_problems.py
三步驟の文章題：買い物とおつり、まとめ買い、分けて残り、比較して合計、割引なしの総額など。
誤答：途中の数で止める、1 つの条件を使い忘れる、引く数・足す数を取り違える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(51003)
NM = Names(R)


def A(v, u):
    return "%s %s" % (num(v), u)


def shop():
    def mk():
        who = NM.next()
        p1, n1, p2, n2 = R.randint(15, 80), R.randint(2, 6), R.randint(20, 120), R.randint(2, 5)
        m = R.choice([500, 1000, 2000])
        t = p1 * n1 + p2 * n2
        if t >= m:
            return None
        q = "%s帶 %s 元，買了 %d 枝 %d 元的筆和 %d 本 %d 元的筆記本，還剩多少元？" % (who, num(m), n1, p1, n2, p2)
        v = m - t
        return mcq(q, A(v, "元"), [A(x, "元") for x in (m - p1 * n1, m - p2 * n2, t, m - p1 - p2) if x != v and x > 0],
                   "筆 %d × %d ＝ %d，筆記本 %d × %d ＝ %d，共 %d；%s － %d ＝ %s（元）。" % (p1, n1, p1 * n1, p2, n2, p2 * n2, t, num(m), t, num(v)))
    return mk


def pack():
    def mk():
        per, boxes, extra, ppl = R.randint(6, 24), R.randint(3, 12), R.randint(1, 30), R.randint(3, 9)
        tot = per * boxes + extra
        if tot % ppl:
            return None
        q = "每盒有 %d 顆糖，買了 %d 盒，又多送 %d 顆，全部平分給 %d 人，每人幾顆？" % (per, boxes, extra, ppl)
        v = tot // ppl
        return mcq(q, A(v, "顆"), [A(x, "顆") for x in (per * boxes // ppl if (per * boxes) % ppl == 0 else v + 1, tot, v - 1, per * (boxes + extra) // ppl if (per * (boxes + extra)) % ppl == 0 else v + 2) if x != v and x > 0],
                   "%d × %d ＋ %d ＝ %d（顆），%d ÷ %d ＝ %d（顆）。" % (per, boxes, extra, tot, tot, ppl, v))
    return mk


def compare():
    def mk():
        a = R.randint(40, 300)
        more = R.randint(10, 80)
        k = R.randint(2, 4)
        x, y, z = NM.next(), NM.next(), NM.next()
        if len({x, y, z}) < 3:
            return None
        q = "%s有 %d 元，%s比%s多 %d 元，%s的錢是%s的 %d 倍。三人一共有多少元？" % (x, a, y, x, more, z, y, k)
        b = a + more
        c = b * k
        v = a + b + c
        return mcq(q, A(v, "元"), [A(w, "元") for w in (a + b, c, a + more + a * k, v - a) if w != v],
                   "%s：%d ＋ %d ＝ %d；%s：%d × %d ＝ %d；合計 %d ＋ %d ＋ %d ＝ %s（元）。" % (y, a, more, b, z, b, k, c, a, b, c, num(v)))
    return mk


def trip():
    def mk():
        d = R.randint(3, 9)
        per = R.randint(150, 400)
        bus = R.randint(800, 3000)
        n = R.randint(20, 40)
        q = "%d 位同學去校外教學，每人門票 %d 元，另外租車費 %s 元由大家平分。每人一共要付多少元？" % (n, per, num(bus * n // n))
        if bus % n:
            bus = bus // n * n
            if bus <= 0:
                return None
            q = "%d 位同學去校外教學，每人門票 %d 元，另外租車費 %s 元由大家平分。每人一共要付多少元？" % (n, per, num(bus))
        v = per + bus // n
        return mcq(q, A(v, "元"), [A(x, "元") for x in (per, per * n + bus, bus // n, v + 10) if x != v],
                   "租車費每人 %s ÷ %d ＝ %d（元），%d ＋ %d ＝ %d（元）。" % (num(bus), n, bus // n, per, bus // n, v))
    return mk


def left():
    def mk():
        tot = R.randint(300, 900)
        a = R.randint(30, 120)
        days, per = R.randint(3, 7), R.randint(20, 60)
        rem = tot - a - days * per
        if rem <= 0:
            return None
        who = NM.next()
        q = "一本書有 %d 頁，%s第一天看了 %d 頁，之後 %d 天每天看 %d 頁。還剩幾頁沒看？" % (tot, who, a, days, per)
        return mcq(q, A(rem, "頁"), [A(x, "頁") for x in (tot - a - per, tot - days * per, a + days * per, rem + per) if x != rem and x > 0],
                   "後面 %d 天看了 %d × %d ＝ %d（頁），一共看了 %d ＋ %d ＝ %d（頁），%d － %d ＝ %d（頁）。" % (days, per, days, days * per, a, days * per, a + days * per, tot, a + days * per, rem))
    return mk


def main():
    seen = set()
    sets = [("買東西和找錢", pick_unique(R, shop(), 20, seen)),
            ("裝盒再平分", pick_unique(R, pack(), 20, seen)),
            ("比多少和倍數", pick_unique(R, compare(), 20, seen)),
            ("平分費用", pick_unique(R, trip(), 20, seen)),
            ("綜合三步驟", pick_unique(R, left(), 10, seen) + pick_unique(R, shop(), 5, seen) + pick_unique(R, compare(), 5, seen))]
    body = lesson(
        ["多步驟的題目，先把每個條件一句一句讀懂，再想<b>問題要的答案需要哪些數</b>。",
         "一步一步列式，每一步寫出算的是什麼（單位要寫），最後再列成一個併式檢查。",
         "算完要回頭看：每個條件都用到了嗎？答案合理嗎？"],
        [example("帶 500 元，買 3 枝 25 元的筆和 2 本 60 元的筆記本，剩多少元？", ["筆：25 × 3 ＝ 75。筆記本：60 × 2 ＝ 120。", "共 75 ＋ 120 ＝ 195。500 － 195 ＝ 305。"], "305 元"),
         example("每盒 12 顆，買 5 盒又送 4 顆，平分給 8 人，每人幾顆？", ["12 × 5 ＋ 4 ＝ 64。", "64 ÷ 8 ＝ 8。"], "8 顆")],
        [("只算到第二步就停", "再讀一次問題問的是什麼"),
         ("忘了用「多送 4 顆」這個條件", "每個條件都要檢查有沒有用到"),
         ("「比他多」用減法", "比他多要用加法：他的 ＋ 多的")])
    faq = [{"q": "五年級的多步驟應用問題是什麼？",
            "a": "108課綱 N-5-2：除了「平均」以外，以三步驟的應用問題為主，例如買兩種東西再算找錢、先合起來再平分等。"},
           {"q": "孩子遇到長題目就放棄，怎麼辦？",
            "a": "請孩子用筆把每個數和它的意思圈起來，再從問題往回推：要算答案，需要先知道什麼？"},
           {"q": "三步驟問題一定要寫成併式嗎？",
            "a": "可以先一步一步算，熟練後再寫成一個併式，例如 500 －（25 × 3 ＋ 60 × 2），這是學代數的基礎。"}]
    make_unit(R, "grade-5", "multi-step-word-problems", "N-5-2",
              "解題：多步驟應用問題。除「平均」之外，原則上為三步驟解題應用。",
              "多步驟應用問題（三步驟）",
              "五年級數學 三步驟應用題 練習題｜買東西找錢・平分・倍數 學習單（附解答）",
              "三步驟應用問題",
              "國小五年級數學「多步驟應用問題」免費學習單：買東西和找錢、裝盒再平分、比多少和倍數、平分費用等三步驟應用題。100題線上練習馬上對答案，附可列印解答。",
              "從問題往回想：需要先知道什麼",
              "每一步寫出算的是什麼，最後檢查每個條件都用到。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
