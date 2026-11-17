# -*- coding: utf-8 -*-
"""
台灣 國小二年級 數學：加減估算（108課綱 N-2-4）
  python3 tools/gen_tw_math_g2_estimation.py
最も近い整十・整百（大約幾十・大約幾百）、加減の和・差を估算、錢が夠不夠を估算、答えが合っているか估算でチェック。
誤答：一の位を切り捨てるだけ（48 → 40）、估算の答えと正確な答えの取り違え。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names
from tw_g7 import tidy_sets
import tw_pics as P

R = random.Random(81305)
NM = Names(R)


def r10(n):
    return (n + 5) // 10 * 10


def r100(n):
    return (n + 50) // 100 * 100


def s1(seen):
    def mk():
        n = R.randint(11, 98)
        if n % 10 == 5 or n % 10 == 0:
            return None
        v = r10(n)
        lo = n // 10 * 10
        marks = {lo: str(lo), lo + 10: str(lo + 10), n: "%d" % n}
        q = "%d 比較接近 %d 還是 %d？" % (n, lo, lo + 10) + P.numline(lo, lo + 10, marks, 26)
        return mcq(q, str(v), [str(lo + 10 if v == lo else lo), str(n), "一樣近"], "%d 的個位是 %d，%s 5，比較接近 %d。" % (n, n % 10, "小於" if n % 10 < 5 else "大於", v))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def mk():
        n = R.randint(101, 989)
        if n % 100 == 50 or n % 100 == 0:
            return None
        k = R.choice(["十", "百"])
        if k == "十":
            if n % 10 in (0, 5):
                return None
            v = r10(n)
            q = "%d 大約是幾十？（找最接近的整十）" % n
            other = n // 10 * 10 if v != n // 10 * 10 else v + 10
            return mcq(q, str(v), [str(other), str(r100(n)) if r100(n) != v else str(v + 100), str(n)], "看個位：%d 最接近 %d。" % (n, v))
        v = r100(n)
        q = "%d 大約是幾百？（找最接近的整百）" % n
        other = n // 100 * 100 if v != n // 100 * 100 else v + 100
        return mcq(q, str(v), [str(other), str(r10(n)) if r10(n) != v else str(v + 10), str(n)], "看十位：%d 最接近 %d。" % (n, v))
    return pick_unique(R, mk, 20, seen)


def s3(seen):
    def mk():
        a, b = R.randint(110, 590), R.randint(110, 390)
        if a % 100 in range(40, 60) or b % 100 in range(40, 60):
            return None
        op = R.choice(["＋", "－"])
        if op == "－" and a <= b:
            a, b = b, a
        ea, eb = r100(a), r100(b)
        v = ea + eb if op == "＋" else ea - eb
        if v <= 0:
            return None
        q = "估一估：%d %s %d 大約是多少？（先估成整百）" % (a, op, b)
        exact = a + b if op == "＋" else a - b
        return mcq(q, "大約 %d" % v, ["大約 %d" % x for x in (v + 100, v - 100 if v > 100 else v + 200, exact if exact != v else v + 300)], "%d 大約 %d，%d 大約 %d：%d %s %d ＝ %d。" % (a, ea, b, eb, ea, op, eb, v))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def mk():
        p1, p2 = R.randint(110, 480), R.randint(110, 480)
        money = R.choice([500, 600, 700, 800, 1000])
        tot = p1 + p2
        est = r100(p1) + r100(p2)
        if abs(tot - money) < 60 or (tot <= money) != (est <= money) or est == money:
            return None
        who = NM.next()
        q = "%s有 %d 元，想買 %d 元的書包和 %d 元的鞋子。估一估，錢夠不夠？" % (who, money, p1, p2)
        ok = tot <= money
        return mcq(q, "夠" if ok else "不夠", ["不夠" if ok else "夠", "剛好一樣", "不能估"], "大約 %d ＋ %d ＝ %d，%d %s %d，所以%s。（準確是 %d 元）" % (r100(p1), r100(p2), est, est, "＜" if ok else "＞", money, "夠" if ok else "不夠", tot))
    return pick_unique(R, mk, 20, seen)


def s5(seen):
    def mk():
        a, b = R.randint(120, 580), R.randint(120, 380)
        s = a + b
        wrong = R.choice([s + 100, s - 100, s + 200, a + b * 10 // 10 + 300])
        claim = R.choice([s, wrong])
        who = NM.next()
        q = "%s算 %d ＋ %d ＝ %d。用估算看看，這個答案合理嗎？" % (who, a, b, claim)
        ok = claim == s
        est = r100(a) + r100(b)
        return mcq(q, "合理" if ok else "不合理", ["不合理" if ok else "合理", "要背答案才知道", "不能檢查"], "大約 %d ＋ %d ＝ %d，%d %s %d，所以%s。" % (r100(a), r100(b), est, claim, "很接近" if ok else "差太多", est, "合理" if ok else "不合理，再算一次"))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [("接近哪一個整十", s1(seen)), ("大約幾十、幾百", s2(seen)), ("估算加減", s3(seen)),
            ("錢夠不夠", s4(seen)), ("用估算檢查答案", s5(seen))]
    tidy_sets(sets)
    body = lesson(
        ["<b>估算</b>：不用算得很準，先把數變成接近的整十或整百，算出「大約」多少。",
         "看下一位：48 比較接近 50；312 比較接近 300。" + P.numline(40, 50, {40: "40", 48: "48", 50: "50"}, 26),
         "估算可以很快判斷錢夠不夠、答案合不合理。"],
        [example("298 ＋ 405 大約是多少？", ["298 大約 300，405 大約 400。"], "大約 700"),
         example("帶 500 元，買 189 元和 276 元的東西夠嗎？", ["大約 200 ＋ 300 ＝ 500。", "準確是 465。"], "夠")],
        [("48 估成 40", "48 比較接近 50"),
         ("估算後還寫準確的答案", "估算寫「大約」多少"),
         ("算完不檢查", "用估算看答案合不合理")])
    faq = [{"q": "二年級為什麼要學估算？",
            "a": "108課綱 N-2-4：簡單的加減估算，生活中買東西、檢查計算結果都很常用，也能培養數感。"},
           {"q": "估算一定要用整百嗎？",
            "a": "不一定，看數的大小，二位數常用整十，三位數常用整百，只要方便算就好。"},
           {"q": "5 要估成哪一邊？",
            "a": "正好在中間時（例如 45、350），通常往大的方向估，但題目要看情境，二年級的練習會避開這種數。"}]
    make_unit(R, "grade-2", "estimation", "N-2-4",
              "解題：簡單加減估算。具體生活情境。以百位數為主。",
              "加減估算：大約多少",
              "二年級數學 估算 練習題｜大約幾十幾百・錢夠不夠 學習單（附解答）",
              "加減估算",
              "國小二年級數學「加減估算」免費學習單：接近哪一個整十、大約幾十幾百、估算加減、估一估錢夠不夠、用估算檢查答案。100題線上練習，附可列印解答。",
              "先估成整十、整百，再算大約多少",
              "估算可以檢查錢夠不夠、答案合不合理。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
