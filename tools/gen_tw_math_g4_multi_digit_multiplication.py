# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：多位數的乘法（108課綱 N-4-2）
  python3 tools/gen_tw_math_g4_multi_digit_multiplication.py
二位數×二位數、三位數×二位數、末尾有0的乘法、三位數×三位數、應用問題（直式）。
誤答：十位の部分積を左にずらさない（34×26→34×6＋34×2）、進位を忘れる、0 の数を数え間違える。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(41002)
NM = Names(R)


def no_shift(a, b):
    """十位の部分積をずらさない間違い"""
    s, k, t = 0, 0, b
    while t:
        s += a * (t % 10)
        t //= 10
    return s


def no_carry(a, b):
    """各位ごとに掛けて、繰り上がりを書かない間違い（1 けたの乗數ごと）"""
    def m1(x, d):
        return int("".join(str(int(c) * d % 10) for c in str(x)))
    s, p, t = 0, 1, b
    while t:
        s += m1(a, t % 10) * p
        p *= 10
        t //= 10
    return s


def mul_q(alo, ahi, blo, bhi, cond=None):
    def mk():
        a, b = R.randint(alo, ahi), R.randint(blo, bhi)
        if a % 10 == 0 or b % 10 == 0 or (cond and not cond(a, b)):
            return None
        p = a * b
        w = [no_shift(a, b), no_carry(a, b), p + a, p - a, p + 10 * a // 10 * 10, p + 100]
        tens = b // 10 % 10
        return mcq("%s × %s ＝" % (num(a), num(b)), num(p), [num(x) for x in w if x != p and x > 0],
                   "直式：先算 %s × %d ＝ %s，再算 %s × %d0 ＝ %s（往左移一位）%s，加起來 %s。" % (
                       num(a), b % 10, num(a * (b % 10)), num(a), tens, num(a * tens * 10),
                       "，再算 %s × %d00 ＝ %s" % (num(a), b // 100, num(a * (b // 100) * 100)) if b >= 100 else "", num(p)))
    return mk


def zeros_q():
    def mk():
        a = R.randint(2, 99) * R.choice([10, 100])
        b = R.randint(2, 9) * R.choice([10, 100]) + (R.randint(1, 9) * 10 if R.random() < .3 else 0)
        if a * b >= 10 ** 8:
            return None
        p = a * b
        za = len(str(a)) - len(str(a).rstrip("0"))
        zb = len(str(b)) - len(str(b).rstrip("0"))
        ca, cb = int(str(a).rstrip("0")), int(str(b).rstrip("0"))
        return mcq("%s × %s ＝" % (num(a), num(b)), num(p), [num(p * 10), num(p // 10), num(p // 100) if p // 100 > ca * cb else num(p * 100), num(ca * cb)],
                   "先算 %d × %d ＝ %s，兩個數的尾巴一共有 %d 個 0，補在後面：%s。" % (ca, cb, num(ca * cb), za + zb, num(p)))
    return mk


def word():
    def mk():
        who = NM.next()
        kind = R.choice(["ticket", "box", "bus", "save"])
        if kind == "ticket":
            p, n = R.randint(120, 480), R.randint(21, 58)
            q = "一張遊樂園門票 %d 元，學校帶 %d 位學生去，門票一共要多少元？" % (p, n)
        elif kind == "box":
            p, n = R.randint(24, 96), R.randint(105, 480)
            q = "一箱裝 %d 瓶水，%d 箱一共有幾瓶？" % (p, n)
        elif kind == "bus":
            p, n = R.randint(35, 52), R.randint(12, 38)
            q = "一輛遊覽車坐 %d 人，%d 輛車坐滿一共有幾人？" % (p, n)
        else:
            p, n = R.randint(150, 650), 12
            q = "%s每個月存 %d 元，一年（12 個月）存了多少元？" % (who, p)
        v = p * n
        u = "元" if kind in ("ticket", "save") else ("瓶" if kind == "box" else "人")
        return mcq(q, num(v) + " " + u, [num(x) + " " + u for x in (no_shift(p, n), p + n, v + p, v - p, v * 10) if x != v],
                   "%s × %s ＝ %s（%s）。" % (num(p), num(n), num(v), u))
    return mk


def main():
    seen = set()
    sets = [("二位數 × 二位數", pick_unique(R, mul_q(12, 98, 12, 98), 20, seen)),
            ("三位數 × 二位數", pick_unique(R, mul_q(102, 987, 12, 98), 20, seen)),
            ("尾巴有 0 的乘法", pick_unique(R, zeros_q(), 20, seen)),
            ("三位數 × 三位數", pick_unique(R, mul_q(102, 987, 102, 987), 20, seen)),
            ("應用問題", pick_unique(R, word(), 20, seen))]
    body = lesson(
        ["乘以二位數：先乘個位，再乘<b>十位</b>。乘十位得到的是「幾十」，所以<b>往左移一位</b>寫（或在後面補 0）。",
         "最後把兩行加起來。乘以三位數，再多一行乘百位，往左移兩位。",
         "尾巴有 0：先不看 0 算乘法，再把 0 的個數補在後面。"],
        [example("234 × 26 ＝", ["234 × 6 ＝ 1404。", "234 × 20 ＝ 4680（往左移一位）。", "1404 ＋ 4680 ＝ 6084。"], "6084"),
         example("320 × 400 ＝", ["32 × 4 ＝ 128。", "尾巴共 3 個 0。"], "128,000")],
        [("234 × 26 算成 1404 ＋ 468", "十位的 2 是 20，第二行要往左移一位：4680"),
         ("忘了加進位的數", "每一位乘完，要加上前一位進上來的數"),
         ("320 × 400 只補 2 個 0", "兩個數尾巴的 0 都要算：共 3 個 0")])
    faq = [{"q": "四年級的乘法要學到幾位數？",
            "a": "108課綱 N-4-2：乘數是多位數的直式乘法，常見的是三位數 × 二位數、三位數 × 三位數，並理解直式為什麼要往左移一位。"},
           {"q": "直式乘法第二行為什麼要往左移？",
            "a": "乘數十位的 2 代表 20，234 × 20 ＝ 4680，寫的時候個位是 0，所以整行往左移一位。"},
           {"q": "怎麼檢查乘法有沒有算錯？",
            "a": "先估算：234 × 26 大約是 200 × 30 ＝ 6000，答案 6084 和估算接近就比較放心；也可以用除法驗算。"}]
    make_unit(R, "grade-4", "multi-digit-multiplication", "N-4-2",
              "較大位數之乘除計算：處理乘數與除數為多位數之乘除直式計算。教師用位值的概念說明直式計算的合理性。",
              "多位數的乘法：乘以二位數、三位數",
              "四年級數學 乘法直式 練習題｜三位數乘以二位數・三位數 學習單（附解答）",
              "多位數的乘法",
              "國小四年級數學「多位數的乘法」免費學習單：二位數乘二位數、三位數乘二位數、尾巴有0的乘法、三位數乘三位數與應用題。100題線上練習馬上對答案，附可列印解答。",
              "乘十位的那一行，往左移一位",
              "尾巴有 0：先不看 0 算，再補上全部的 0。",
              body, faq, sets, 2)


if __name__ == "__main__":
    main()
