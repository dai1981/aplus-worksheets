# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：除以一位數（108課綱 N-3-5）
  python3 tools/gen_tw_math_g3_divide_by_one_digit.py
二位數、三位數 ÷ 一位數の直式（有餘數、商の中に0）と應用問題。
誤答：商の0を書き忘れる（618÷3→26）、餘數が除數以上、商が1ずれる、など。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31005)


def qr(q, r):
    return "%s……%d" % (num(q), r) if r else num(q)


def drop_zero(q):
    s = str(q)
    return int(s.replace("0", "")) if "0" in s[1:] and s.replace("0", "") else None


def div_q(lo, hi, rem, need_zero=False, dmin=2):
    def mk():
        d = R.randint(dmin, 9)
        t = R.randint(lo, hi)
        q, r = divmod(t, d)
        if (r != 0) != rem or q < 10:
            return None
        if need_zero and "0" not in str(q)[1:]:
            return None
        ans = qr(q, r)
        w = []
        dz = drop_zero(q)
        if dz:
            w.append(qr(dz, r))
        if r:
            w += [qr(q - 1, r + d), qr(q, d - r) if d - r != r else qr(q, r + 1 if r + 1 < d else r - 1)]
        w += [qr(q + 1, r), qr(q - 1, r), qr(q + 10, r), qr(q - 10, r) if q > 20 else qr(q + 2, r)]
        return mcq("%d ÷ %d ＝" % (t, d), ans, [x for x in w if x != ans],
                   "直式從最高位除起，每一位商寫在上面。%d ÷ %d ＝ %s，驗算 %d × %d%s ＝ %d。"
                   % (t, d, ans, d, q, (" ＋ %d" % r) if r else "", t))
    return mk


def round_q():
    def mk():
        d = R.randint(2, 9)
        k = R.choice([10, 100])
        b = R.randint(1, 9) * d
        if b >= 10 and k == 100:
            return None
        t = b * k
        q = t // d
        return mcq("%d ÷ %d ＝" % (t, d), num(q), [num(x) for x in (q // 10, q * 10, q + k, b) if x > 0 and x != q],
                   "%d ÷ %d ＝ %d，再補上 %d 個 0：%s。" % (b, d, b // d, 1 if k == 10 else 2, num(q)))
    return mk


def s5(seen):
    nm = Names(R)

    def mk():
        d = R.randint(3, 9)
        q = R.randint(12, 120)
        r = R.choice([0, 0, R.randint(1, d - 1)])
        t = d * q + r
        if t > 999:
            return None
        who = nm.next()
        kind = R.choice(["share", "pack", "bus"]) if r else R.choice(["share", "pack"])
        if kind == "share":
            qs = "%s把 %d 張貼紙平分給 %d 個同學，每人分到幾張？%s" % (who, t, d, "還剩幾張？" if r else "")
            ans = "每人 %s 張%s" % (num(q), "，剩 %d 張" % r if r else "")
            w = ["每人 %s 張%s" % (num(x), "，剩 %d 張" % r if r else "") for x in (q - 1, q + 1, drop_zero(q) or q + 10)]
        elif kind == "pack":
            qs = "工廠有 %d 個麵包，每 %d 個裝一盒，可以裝滿幾盒？%s" % (t, d, "還剩幾個？" if r else "")
            ans = "%s 盒%s" % (num(q), "，剩 %d 個" % r if r else "")
            w = ["%s 盒%s" % (num(x), "，剩 %d 個" % r if r else "") for x in (q - 1, q + 1, drop_zero(q) or q + 10)]
        else:
            if t > 99:
                return None
            qs = "%d 位同學去划船，每艘船最多坐 %d 人，至少要幾艘船？" % (t, d)
            ans = "%s 艘" % num(q + 1)
            w = ["%s 艘" % num(x) for x in (q, q + 2, q - 1)]
        return mcq(qs, ans, w, "%d ÷ %d ＝ %s。%s" % (t, d, qr(q, r), "剩下的人也要坐船，所以要再加 1 艘。" if kind == "bus" else ""))
    return pick_unique(R, mk, 20, seen)


def main():
    seen = set()
    sets = [
        ("整十、整百和二位數除以一位數", pick_unique(R, round_q(), 8, seen) + pick_unique(R, div_q(24, 98, False), 12, seen)),
        ("二位數除以一位數（有餘數）", pick_unique(R, div_q(25, 99, True), 20, seen)),
        ("三位數除以一位數", pick_unique(R, div_q(112, 999, False), 20, seen)),
        ("有餘數和商中間有0", pick_unique(R, div_q(205, 999, True, need_zero=True), 10, seen)
                             + pick_unique(R, div_q(112, 999, True, dmin=3), 10, seen)),
        ("應用問題", s5(seen)),
    ]
    body = lesson(
        ["除法直式<b>從最高位開始除</b>，商寫在被除數那一位的上面。",
         "每一位：<b>除 → 乘 → 減 → 移下一位</b>。",
         "某一位不夠除時，商要寫 <b>0</b>，不能跳過。",
         "最後剩下的是<b>餘數，一定比除數小</b>。用 除數 × 商 ＋ 餘數 驗算。"],
        [example("75 ÷ 4 ＝", ["十位 7 ÷ 4 ＝ 1……3，商 1 寫在十位。", "3 和個位 5 合成 35，35 ÷ 4 ＝ 8……3。"], "18……3"),
         example("618 ÷ 3 ＝", ["6 ÷ 3 ＝ 2。十位 1 不夠除 3，商寫 0。", "18 ÷ 3 ＝ 6。"], "206")],
        [("618 ÷ 3 寫成 26", "十位不夠除要寫 0：206"),
         ("75 ÷ 4 ＝ 17……7", "餘數 7 比 4 大，要再除一次：18……3"),
         ("商寫在錯的位上", "商要對齊被除的那一位")])
    faq = [{"q": "除法直式要怎麼教三年級的孩子？",
            "a": "用「除、乘、減、移下一位」四個步驟，每一位重複一次。商要對齊被除的那一位，不夠除就寫 0。"},
           {"q": "商的中間有0時常常漏寫，怎麼辦？",
            "a": "提醒孩子：每移下一位就一定要在上面寫一個商，不夠除時寫 0，最後用乘法驗算。"},
           {"q": "這一單元和九九範圍的除法有什麼不同？",
            "a": "九九範圍的除法用乘法表就能算；這一單元的被除數是二、三位數，要用直式一位一位除（108課綱 N-3-5）。"}]
    make_unit(R, "grade-3", "divide-by-one-digit", "N-3-5",
              "除以一位數：除法直式計算。教師用位值的概念說明直式計算的合理性。被除數為二、三位數。",
              "除以一位數：除法直式與餘數",
              "三年級數學 除法直式 練習題｜二位數、三位數除以一位數 學習單（附解答）",
              "除以一位數",
              "國小三年級數學「除以一位數」免費學習單：二位數、三位數除以一位數的直式、有餘數、商中間有0和應用題。100題線上練習馬上對答案，附可列印解答。",
              "從最高位除起：除、乘、減、移下一位",
              "不夠除時商寫 0；餘數一定比除數小。",
              body, faq, sets, 5)


if __name__ == "__main__":
    main()
