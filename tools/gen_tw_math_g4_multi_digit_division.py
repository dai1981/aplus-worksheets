# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：除以二位數（108課綱 N-4-2）
  python3 tools/gen_tw_math_g4_multi_digit_division.py
整十的除法、二・三位數÷二位數（商一位數）、三位數÷二位數（商二位數）、四位數÷二位數（商中間有0）、應用問題。
誤答：試商が1ずれる、餘數が除數以上、商の 0 を落とす、整十の0を消し忘れる。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41003)
NM = Names(R)


def qr(q, r):
    return "%s……%d" % (num(q), r) if r else num(q)


def drop0(q):
    s = str(q)
    return int(s.replace("0", "")) if "0" in s[1:] and s.replace("0", "") else None


def div_q(tlo, thi, dlo, dhi, qlo, qhi, need0=False, rem=None):
    def mk():
        d = R.randint(dlo, dhi)
        if d % 10 == 0:
            return None
        t = R.randint(tlo, thi)
        q, r = divmod(t, d)
        if not (qlo <= q <= qhi) or (rem is not None and (r > 0) != rem):
            return None
        if need0 and "0" not in str(q)[1:]:
            return None
        ans = qr(q, r)
        w = [qr(q + 1, r - d) if r >= d else None, qr(q - 1, r + d), qr(q + 1, 0) if r else qr(q + 1, 1)]
        z = drop0(q)
        if z:
            w.insert(0, qr(z, r))
        w += [qr(q, (r + 1) % d) if r else qr(q, 1), qr(q + 10, r)]
        return mcq("%s ÷ %d ＝" % (num(t), d), ans, [x for x in w if x and x != ans],
                   "把 %d 看成 %d 來試商。%s ÷ %d ＝ %s，驗算 %d × %s%s ＝ %s。" % (
                       d, round(d, -1) or 10, num(t), d, ans, d, num(q), " ＋ %d" % r if r else "", num(t)))
    return mk


def tens_q():
    def mk():
        d = R.randint(2, 9) * 10
        q = R.randint(2, 9) if R.random() < .6 else R.randint(11, 40)
        t = d * q
        if R.random() < .3:
            t *= 10
            q *= 10
        return mcq("%s ÷ %d ＝" % (num(t), d), num(q), [num(x) for x in (q * 10, q // 10 if q >= 10 and q % 10 == 0 else q + 1, t // (d // 10) if t // (d // 10) != q else q + 2, q - 1)],
                   "被除數和除數都去掉一個 0：%s ÷ %d ＝ %s。" % (num(t // 10), d // 10, num(q)))
    return mk


def word():
    def mk():
        kind = R.choice(["share", "pack", "bus", "save"])
        who = NM.next()
        d = R.randint(12, 48)
        q = R.randint(12, 95)
        r = R.choice([0, R.randint(1, d - 1)])
        t = d * q + r
        if kind == "share":
            s = "%d 枝鉛筆平分給 %d 位同學，每人分到幾枝？%s" % (t, d, "還剩幾枝？" if r else "")
            ans = "每人 %d 枝%s" % (q, "，剩 %d 枝" % r if r else "")
            w = ["每人 %d 枝%s" % (x, "，剩 %d 枝" % r if r else "") for x in (q - 1, q + 1, q + 10)]
        elif kind == "pack":
            s = "工廠有 %s 顆蘋果，每 %d 顆裝一箱，可以裝滿幾箱？%s" % (num(t), d, "還剩幾顆？" if r else "")
            ans = "%d 箱%s" % (q, "，剩 %d 顆" % r if r else "")
            w = ["%d 箱%s" % (x, "，剩 %d 顆" % r if r else "") for x in (q - 1, q + 1, q + 10)]
        elif kind == "bus":
            if not r:
                return None
            d = R.randint(40, 45)
            q = R.randint(3, 12)
            r = R.randint(1, d - 1)
            t = d * q + r
            s = "%d 位師生去校外教學，每輛遊覽車最多坐 %d 人，至少要幾輛車？" % (t, d)
            ans = "%d 輛" % (q + 1)
            w = ["%d 輛" % x for x in (q, q + 2, q - 1)]
        else:
            m = R.randint(12, 24)
            per = R.randint(150, 900)
            t = m * per
            s = "%s想存 %s 元買腳踏車，每個月存一樣多，%d 個月剛好存到。每個月存多少元？" % (who, num(t), m)
            ans = "%s 元" % num(per)
            w = ["%s 元" % num(x) for x in (per + 10, per - 10, per * 10 if per * 10 < t else per + 100)]
            return mcq(s, ans, w, "%s ÷ %d ＝ %s（元）。" % (num(t), m, num(per)))
        return mcq(s, ans, w, "%s ÷ %d ＝ %s。%s" % (num(t), d, qr(q, r), "剩下的人也要坐車，所以要多 1 輛。" if kind == "bus" else ""))
    return mk


def main():
    seen = set()
    sets = [("整十的除法", pick_unique(R, tens_q(), 20, seen)),
            ("除以二位數（商是一位數）", pick_unique(R, div_q(60, 999, 11, 98, 2, 9), 20, seen)),
            ("三位數 ÷ 二位數（商是二位數）", pick_unique(R, div_q(200, 999, 11, 49, 10, 89), 20, seen)),
            ("四位數 ÷ 二位數", pick_unique(R, div_q(1000, 9999, 12, 98, 100, 999, need0=True), 10, seen)
                            + pick_unique(R, div_q(1000, 9999, 12, 98, 20, 99), 10, seen)),
            ("應用問題", pick_unique(R, word(), 20, seen))]
    body = lesson(
        ["除以二位數：把除數看成<b>最接近的整十</b>來試商，例如 23 看成 20、38 看成 40。",
         "商太大（乘回去比被除數大）就改小 1；餘數比除數大，商就改大 1。",
         "某一位不夠除時，商要寫 <b>0</b>。最後用 <b>除數 × 商 ＋ 餘數</b> 驗算。"],
        [example("196 ÷ 28 ＝", ["28 看成 30，196 ÷ 30 大約是 6。", "28 × 6 ＝ 168，196 － 168 ＝ 28，餘數不能等於除數，商改成 7。", "28 × 7 ＝ 196。"], "7"),
         example("8364 ÷ 41 ＝", ["83 ÷ 41 ＝ 2……1。", "移下 6：16 不夠除 41，商寫 0。", "移下 4：164 ÷ 41 ＝ 4。"], "204")],
        [("8364 ÷ 41 寫成 24", "十位不夠除要寫 0：204"),
         ("餘數比除數還大", "餘數一定比除數小，商要再加 1"),
         ("試商後沒有檢查", "乘回去比一比，太大就減 1")])
    faq = [{"q": "除以二位數怎麼試商？",
            "a": "把除數看成最接近的整十（如 28 看成 30），用九九乘法估商；乘回去後如果太大就減 1，餘數比除數大就加 1。"},
           {"q": "四年級的除法要學到哪裡？",
            "a": "108課綱 N-4-2：除數是多位數的直式除法，常見的是三位數、四位數除以二位數，並用位值說明直式的道理。"},
           {"q": "商中間的 0 常常漏寫，怎麼辦？",
            "a": "提醒孩子每移下一位，上面就要寫一個商；不夠除就寫 0，最後用乘法驗算。"}]
    make_unit(R, "grade-4", "multi-digit-division", "N-4-2",
              "較大位數之乘除計算：處理乘數與除數為多位數之乘除直式計算。教師用位值的概念說明直式計算的合理性。",
              "除以二位數：試商與除法直式",
              "四年級數學 除法直式 練習題｜除以二位數・試商・商中間有0 學習單（附解答）",
              "除以二位數",
              "國小四年級數學「除以二位數」免費學習單：整十的除法、試商、三位數和四位數除以二位數、商中間有0與應用題。100題線上練習馬上對答案，附可列印解答。",
              "把除數看成整十來試商",
              "商太大就減 1；餘數一定比除數小。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
