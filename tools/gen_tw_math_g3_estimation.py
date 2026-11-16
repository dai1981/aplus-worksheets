# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：四則估算（108課綱 N-3-8）
  python3 tools/gen_tw_math_g3_estimation.py
最接近的整十・整百、加減乘の估算、錢夠不夠、用估算檢查答案。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31008)
NM = Names(R)


def near(n, k):
    """最接近的整k（5 はちょうど真ん中なので出題しない）"""
    return (n + k // 2) // k * k


def mid(n, k):
    return n % k == k // 2


def s1(seen):
    def mk():
        k = R.choice([10, 100, 100])
        n = R.randint(110, 9890) if k == 100 else R.randint(21, 989)
        if mid(n, k) or n % k == 0:
            return None
        a = near(n, k)
        lo, hi = n // k * k, n // k * k + k
        other = hi if a == lo else lo
        q = "%s 最接近哪一個整%s？" % (num(n), "十" if k == 10 else "百")
        return mcq(q, num(a), [num(x) for x in (other, near(n, k * 10), a + k, a - k, n) if x > 0 and x != a],
                   "%s 在 %s 和 %s 之間，比較靠近 %s。" % (num(n), num(lo), num(hi), num(a)))
    return pick_unique(R, mk, 20, seen)


def est(op, seen, n):
    def mk():
        if op == "+":
            a, b = R.randint(110, 690), R.randint(110, 690)
        elif op == "-":
            a, b = R.randint(400, 990), R.randint(110, 390)
        else:
            a, b = R.randint(21, 98), R.randint(3, 9)
        k = 100 if op != "×" else 10
        if mid(a, k) or (op != "×" and mid(b, k)) or a % k == 0:
            return None
        ea = near(a, k)
        eb = near(b, k) if op != "×" else b
        e = ea + eb if op == "+" else (ea - eb if op == "-" else ea * eb)
        exact = a + b if op == "+" else (a - b if op == "-" else a * b)
        if op == "-" and e < 300:
            return None
        q = "用最接近的整%s估算：%d %s %d 大約是多少？" % ("百" if k == 100 else "十", a, "＋" if op == "+" else ("－" if op == "-" else "×"), b)
        A = [a // k * k, a // k * k + k]
        Bv = [b // k * k, b // k * k + k] if op != "×" else [b]
        w = []
        for x in A:                                   # 近いほうでなく、もう一方の整十・整百を使った間違い
            for y in Bv:
                w.append(x + y if op == "+" else (x - y if op == "-" else x * y))
        w += [e + k * (b if op == "×" else 1), e - k * (b if op == "×" else 1),
              e + 2 * k * (b if op == "×" else 1), e - 2 * k * (b if op == "×" else 1)]
        return mcq(q, "大約 " + num(e), ["大約 " + num(x) for x in w if x != e and x > 0],
                   "%d 看成 %d%s，%s ＝ %s。（真正的答案是 %s）" % (
                       a, ea, "，%d 看成 %d" % (b, eb) if op != "×" else "",
                       "%d %s %d" % (ea, {"+": "＋", "-": "－", "×": "×"}[op], eb), num(e), num(exact)))
    return pick_unique(R, mk, n, seen)


def s5(seen):
    def enough():
        p1, p2, p3 = R.randint(110, 390), R.randint(110, 390), R.randint(110, 390)
        tot = p1 + p2 + p3
        have = R.choice([600, 700, 800, 900, 1000])
        if abs(tot - have) < 60:
            return None
        who = NM.next()
        q = "%s帶 %d 元去買文具，想買 %d 元的書包吊飾、%d 元的筆袋和 %d 元的鉛筆盒。錢夠不夠？" % (who, have, p1, p2, p3)
        e = near(p1, 100) + near(p2, 100) + near(p3, 100)
        ok = tot <= have
        ans = "夠" if ok else "不夠"
        return mcq(q, ans + ("，還會剩錢" if ok else "，差一些錢"),
                   ["夠" + ("，剛好用完" if ok else "，還會剩錢"), ("不夠" if ok else "夠") + "，差一些錢" if ok else "夠，剛好用完", "無法判斷"],
                   "估算：大約 %d ＋ %d ＋ %d ＝ %d 元；精算 %d ＋ %d ＋ %d ＝ %d 元，%s %d 元。" % (
                       near(p1, 100), near(p2, 100), near(p3, 100), e, p1, p2, p3, tot, "沒有超過" if ok else "超過", have))

    def check():
        a, b = R.randint(210, 790), R.randint(110, 690)
        if mid(a, 100) or mid(b, 100):
            return None
        right = a + b
        bad = right + R.choice([-200, 200, 100 * R.choice([3, 4]), -300])
        q = "小明算 %d ＋ %d ＝ %d。用估算看看，這個答案合理嗎？" % (a, b, bad)
        e = near(a, 100) + near(b, 100)
        return mcq(q, "不合理，答案應該大約是 %s" % num(e),
                   ["合理，和估算差不多", "不合理，答案應該大約是 %s" % num(e + 300), "不合理，答案應該大約是 %s" % num(e - 300)],
                   "估算 %d ＋ %d ＝ %d，%d 差太多，所以不合理。正確答案是 %s。" % (near(a, 100), near(b, 100), e, bad, num(right)))

    def mul_money():
        p, n = R.randint(21, 89), R.randint(3, 9)
        if mid(p, 10) or p % 10 == 0:
            return None
        e = near(p, 10) * n
        mw, item = R.choice([("盒", "牛奶"), ("個", "便當"), ("本", "漫畫"), ("杯", "珍珠奶茶")])
        q = "一%s%s %d 元，買 %d %s大約要多少元？（用最接近的整十估算）" % (mw, item, p, n, mw)
        return mcq(q, "大約 %d 元" % e, ["大約 %d 元" % x for x in (e + 10 * n, e - 10 * n, p + n, e * 10)],
                   "%d 看成 %d，%d × %d ＝ %d（元）。" % (p, near(p, 10), near(p, 10), n, e))
    return pick_unique(R, enough, 7, seen) + pick_unique(R, check, 6, seen) + pick_unique(R, mul_money, 7, seen)


def main():
    seen = set()
    sets = [("最接近的整十、整百", s1(seen)), ("估算加法", est("+", seen, 20)), ("估算減法", est("-", seen, 20)),
            ("估算乘法", est("×", seen, 20)), ("生活中的估算", s5(seen))]
    body = lesson(
        ["<b>估算</b>是先把數看成好算的整十或整百，算出<b>大約</b>的答案。",
         "看這個數比較靠近哪一個整百：378 在 300 和 400 之間，比較靠近 <b>400</b>。",
         "估算可以很快判斷<b>錢夠不夠</b>，也可以<b>檢查答案合不合理</b>。"],
        [example("用最接近的整百估算 378 ＋ 214", ["378 看成 400，214 看成 200。", "400 ＋ 200 ＝ 600。"], "大約 600"),
         example("一個便當 68 元，買 4 個大約要多少元？", ["68 看成 70。", "70 × 4 ＝ 280。"], "大約 280 元")],
        [("378 看成 300（只看百位）", "要看比較靠近哪一個整百：378 靠近 400"),
         ("估算後就說答案是 600", "估算是「大約」，真正的答案要精算"),
         ("算錯了也不知道", "先估算，精算的答案和估算差很多就要檢查")])
    faq = [{"q": "三年級的估算要學什麼？",
            "a": "108課綱 N-3-8：在生活情境裡把數看成整十、整百來估算，並用估算檢查計算結果合不合理。"},
           {"q": "估算和四捨五入一樣嗎？",
            "a": "三年級先學「比較靠近哪一個整十、整百」，這就是四捨五入的想法；正式的四捨五入名稱在高年級會再學。"},
           {"q": "估算對孩子有什麼幫助？",
            "a": "買東西時能快速判斷錢夠不夠，寫功課時能發現算錯的答案，例如 378 ＋ 214 不可能是 392。"}]
    make_unit(R, "grade-3", "estimation", "N-3-8",
              "解題：四則估算。具體生活情境。較大位數之估算策略。能用估算檢驗計算結果的合理性。",
              "估算：用整十、整百算大約",
              "三年級數學 估算 練習題｜最接近的整百・加減乘估算 學習單（附解答）",
              "估算",
              "國小三年級數學「估算」免費學習單：最接近的整十、整百，加法、減法、乘法的估算，判斷錢夠不夠和答案合不合理。100題線上練習馬上對答案，附可列印解答。",
              "看比較靠近哪一個整十、整百，再算大約",
              "估算能判斷錢夠不夠，也能檢查答案合不合理。",
              body, faq, sets, 7)


if __name__ == "__main__":
    main()
