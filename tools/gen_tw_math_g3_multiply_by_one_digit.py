# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：乘以一位數（108課綱 N-3-3）
  python3 tools/gen_tw_math_g3_multiply_by_one_digit.py
整十・整百 × 一位數、二位數 × 一位數（進位）、三位數 × 一位數（直式）と應用問題。
誤答：進位を足し忘れる（47×3→121）、各位の積を並べる（23×4→812）、かける数が1つずれる。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names

R = random.Random(31003)


def forget_carry(a, m):
    """進位を足し忘れる：上の位はそのまま、下の位は一の位だけ"""
    s = str(a)
    return int(str(int(s[0]) * m) + "".join(str(int(d) * m % 10) for d in s[1:]))


def side_by_side(a, m):
    return int("".join(str(int(d) * m) for d in str(a)))


def carries(a, m):
    c = n = 0
    for d in reversed(str(a)):
        v = int(d) * m + c
        c = v // 10
        n += 1 if c else 0
    return n


def mul_q(lo, hi, mlo=2, mhi=9, need=0, exact=None):
    def mk():
        a, m = R.randint(lo, hi), R.randint(mlo, mhi)
        if a % 10 == 0:
            return None
        if carries(a, m) < need or (exact is not None and carries(a, m) != exact):
            return None
        p = a * m
        w = [forget_carry(a, m), side_by_side(a, m), a * (m - 1), a * (m + 1), p + 10, p - 10, a + m]
        return mcq("%s × %s ＝" % (a, m), num(p), [num(x) for x in w if x != p and 0 < x < p * 3],
                   "直式從個位乘起：%s。%s × %s ＝ %s。" % (steps(a, m), a, m, num(p)))
    return mk


def steps(a, m):
    out, c = [], 0
    names = ["個位", "十位", "百位"]
    for i, d in enumerate(reversed(str(a))):
        v = int(d) * m + c
        out.append("%s %s×%d%s＝%d" % (names[i], d, m, ("＋%d" % c) if c else "", v))
        c = v // 10
    return "，".join(out)


def tens_q():
    def mk():
        k = R.choice([10, 100])
        a, m = R.randint(2, 9) * k, R.randint(2, 9)
        p = a * m
        w = [p // 10, p * 10, a + m, a * (m - 1)]
        return mcq("%s × %s ＝" % (a, m), num(p), [num(x) for x in w if x != p and x > 0],
                   "%d × %d ＝ %d，%d 有 %d 個 0，所以答案是 %s。" % (a // k, m, a // k * m, a, 1 if k == 10 else 2, num(p)))
    return mk


def s5(seen):
    nm = Names(R)
    items = [("每盒有 {a} 枝色鉛筆，{m} 盒一共有幾枝？", "枝", 12, 36),
             ("每張電影票 {a} 元，買 {m} 張要多少元？", "元", 180, 350),
             ("一箱蘋果有 {a} 顆，{m} 箱一共有幾顆？", "顆", 18, 48),
             ("一本故事書有 {a} 頁，{m} 本一共有幾頁？", "頁", 48, 196),
             ("每輛遊覽車坐 {a} 人，{m} 輛一共可以坐幾人？", "人", 38, 45),
             ("{who}每天跳繩 {a} 下，{m} 天一共跳幾下？", "下", 85, 260),
             ("一雙運動鞋 {a} 元，{m} 雙要多少元？", "元", 450, 990)]

    def mk():
        t, u, lo, hi = R.choice(items)
        a = R.randint(lo, hi)
        m = R.randint(3, 9)
        if carries(a, m) < 1:
            return None
        p = a * m
        q = t.format(a=a, m=m, who=nm.next())
        w = [a + m, forget_carry(a, m), a * (m - 1), p + 10, p - 10]
        return mcq(q, num(p) + u, [num(x) + u for x in w if x != p and x > 0],
                   "一份是 %d，有 %d 份，用乘法：%d × %d ＝ %s（%s）。" % (a, m, a, m, num(p), u))

    def cmp_():
        a, m = R.randint(150, 900), R.randint(2, 9)
        if a * m > 9999 or carries(a, m) < 2:
            return None
        who = nm.next()
        q = "%s有 %d 元，哥哥的錢是%s的 %d 倍，哥哥有多少元？" % (who, a, who, m)
        p = a * m
        w = [a + m, forget_carry(a, m), a * (m + 1), p - 100]
        return mcq(q, num(p) + "元", [num(x) + "元" for x in w if x != p and x > 0],
                   "%d 倍用乘法：%d × %d ＝ %s（元）。" % (m, a, m, num(p)))
    return pick_unique(R, mk, 14, seen) + pick_unique(R, cmp_, 6, seen)


def main():
    seen = set()
    sets = [
        ("整十、整百乘一位數", pick_unique(R, tens_q(), 20, seen)),
        ("二位數 × 一位數（進位一次）", pick_unique(R, mul_q(12, 98, exact=1), 20, seen)),
        ("二位數 × 一位數（連續進位）", pick_unique(R, mul_q(23, 99, 3, 9, exact=2), 20, seen)),
        ("三位數 × 一位數", pick_unique(R, mul_q(105, 989, 2, 9, need=2), 20, seen)),
        ("應用問題", s5(seen)),
    ]
    body = lesson(
        ["乘法直式：一位數寫在下面，<b>從個位開始乘</b>。",
         "每一位的積<b>滿10就進位</b>，把進位的數寫小小的，乘下一位後<b>再加上去</b>。",
         "30 × 4：先算 3 × 4 ＝ 12，再在後面補 1 個 0，就是 120。"],
        [example("47 × 3 ＝", ["個位 7 × 3 ＝ 21，寫 1，進 2。", "十位 4 × 3 ＝ 12，再加進位 2 ＝ 14。"], "141"),
         example("326 × 4 ＝", ["個位 6 × 4 ＝ 24，寫 4 進 2。", "十位 2 × 4 ＋ 2 ＝ 10，寫 0 進 1。", "百位 3 × 4 ＋ 1 ＝ 13。"], "1304")],
        [("47 × 3 寫成 121（進位沒加）", "十位 4 × 3 ＝ 12 之後要加上進位的 2"),
         ("23 × 4 寫成 812（各位的積排在一起）", "8 是十位、12 是個位：要進位，答案 92"),
         ("200 × 3 寫成 60", "2 × 3 ＝ 6，後面補兩個 0：600")])
    faq = [{"q": "三年級的乘法要學到幾位數？",
            "a": "108課綱 N-3-3 是「乘以一位數」：被乘數是二位數或三位數，乘數是一位數，要會用直式計算和進位。"},
           {"q": "孩子乘法直式常忘記加進位，怎麼辦？",
            "a": "把進位的數字寫在上一位的上方，乘完那一位就馬上加，並用估算檢查：47 × 3 大約是 50 × 3 ＝ 150。"},
           {"q": "九九乘法還不熟可以先做這份嗎？",
            "a": "建議先熟練九九乘法。這一單元的第1回（整十、整百）可以當作暖身。"}]
    make_unit(R, "grade-3", "multiply-by-one-digit", "N-3-3",
              "乘以一位數：乘法直式計算。教師用位值的概念說明直式計算的合理性。被乘數為二、三位數。",
              "乘以一位數：乘法直式與進位",
              "三年級數學 乘法直式 練習題｜二位數、三位數乘一位數 學習單（附解答）",
              "乘以一位數",
              "國小三年級數學「乘以一位數」免費學習單：整十整百的乘法、二位數和三位數乘一位數的直式與進位、乘法應用題。100題線上練習馬上對答案，附可列印解答。",
              "從個位乘起，進位的數乘完再加",
              "整十、整百的乘法：先算前面的數，再補上 0。",
              body, faq, sets, 3)


if __name__ == "__main__":
    main()
