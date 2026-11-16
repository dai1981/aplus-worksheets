# -*- coding: utf-8 -*-
"""
台灣 國小四年級 數學：一億以內的數（108課綱 N-4-1）
  python3 tools/gen_tw_math_g4_numbers_to_100_million.py
位值（萬、十萬、百萬、千萬）、國字と數字、「3205萬400」の書き方、大小比較、萬を単位にした加減、生活の大數。
誤答：0 の位を落とす（三千萬零五 → 3005）、位を1つずらす、萬の位と千の位を混同。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, zh, wan, table

R = random.Random(41001)
NM = Names(R)
PL = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位", "千萬位"]


def rnd8(zeros=0):
    while True:
        n = R.randint(10000000, 99999999)
        s = str(n)
        if zeros:
            idx = R.sample(range(1, 8), zeros)
            s = "".join("0" if i in idx else c for i, c in enumerate(s))
            n = int(s)
        if len(set(str(n))) >= 5:
            return n


def s1(seen):
    def digit():
        n = R.randint(1000000, 99999999)
        s = str(n)[::-1]
        k = R.randint(4, len(s) - 1)
        d = int(s[k])
        if d == 0 or s.count(s[k]) > 1:
            return None
        q = "%s 的<b>%s</b>數字是多少？" % (num(n), PL[k])
        if len(set(s)) < 5:
            return None
        near = sorted(range(len(s)), key=lambda i: (abs(i - k), i))
        return mcq(q, str(d), [s[i] for i in near if s[i] != s[k]],
                   "從右邊數：個、十、百、千、萬、十萬、百萬、千萬。%s是第 %d 位，數字是 %d。" % (PL[k], k + 1, d))

    def value():
        n = R.randint(1000000, 99999999)
        s = str(n)[::-1]
        k = R.randint(4, len(s) - 1)
        d = int(s[k])
        if d == 0:
            return None
        v = d * 10 ** k
        q = "%s 裡的「%d」在%s，代表多少？" % (num(n), d, PL[k])
        return mcq(q, num(v), [num(d * 10 ** (k - 1)), num(d * 10 ** (k + 1)), str(d), num(d * 10 ** (k - 2))],
                   "%d 個%s是 %s（%s）。" % (d, PL[k][:-1], num(v), zh(v)))
    return pick_unique(R, digit, 10, seen) + pick_unique(R, value, 10, seen)


def s2(seen):
    def to_num():
        n = rnd8(R.randint(1, 3))
        q = "「%s」寫成數字是多少？" % zh(n)
        s = str(n)
        w = [s.replace("0", "", 1), s[:4] + s[5:] + "0" if s[4] == "0" else s + "0", str(n // 10 * 10 + (n % 10 + 1) % 10) if n % 10 else str(n + 10)]
        w += [str(int(s[:4]) * 1000 + int(s[4:]) % 1000)]
        return mcq(q, num(n), [num(int(x)) for x in w if x and int(x) != n] + [num(n + 10000)],
                   "萬的前面是 %d，後面 4 位是 %s：%s。沒有的位要寫 0。" % (n // 10000, str(n % 10000).zfill(4), num(n)))

    def to_zh():
        n = rnd8(R.randint(1, 3))
        q = "%s 讀作什麼？" % num(n)
        m1 = n + 10 ** R.choice([4, 5, 6])
        w = [zh(int(str(n).replace("0", "", 1).ljust(8, "0")[:8])), zh(m1 if m1 < 10 ** 8 else n - 10 ** 5), zh(n // 10) if n // 10 >= 10000 else zh(n + 1)]
        return mcq(q, zh(n), [x for x in w if x != zh(n)] + [zh(n + 1000) if n % 10000 < 9000 else zh(n - 1000)],
                   "先讀萬前面的 %s（%s萬），再讀後面 4 位。中間有 0 要讀「零」。" % (n // 10000, zh(n // 10000)))

    def wan_q():
        w1, r = R.randint(2, 9999), R.choice([R.randint(1, 9999), R.randint(1, 999), R.randint(1, 99)])
        n = w1 * 10000 + r
        q = "「%d萬%d」寫成數字是多少？" % (w1, r)
        return mcq(q, num(n), [num(int("%d%d" % (w1, r))), num(w1 * 1000 + r), num(w1 * 100000 + r), num(n + 10000)],
                   "%d萬是 %s，再加上 %d：%s。" % (w1, num(w1 * 10000), r, num(n)))
    return pick_unique(R, to_num, 7, seen) + pick_unique(R, to_zh, 6, seen) + pick_unique(R, wan_q, 7, seen)


def s3(seen):
    def cmp_():
        a = R.randint(1000000, 99999999)
        b = a + R.choice([10 ** 6, -10 ** 6, 10 ** 5, -10 ** 5, 10 ** 4, -9 * 10 ** 4, 900, -1, 10 ** 7 - 1])
        if b < 1000000 or b > 99999999 or len(str(a)) != len(str(b)) and R.random() < .5:
            return None
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (num(a), num(b)), sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "先比位數，位數一樣再從最高位比起：%s %s %s。" % (num(a), sign, num(b)))

    def times():
        n = R.randint(12, 9999) * R.choice([1, 10, 100])
        k = R.choice([10, 100, 1000])
        if n * k >= 10 ** 8:
            return None
        q = "%s 的 %s 倍是多少？" % (num(n), num(k))
        return mcq(q, num(n * k), [num(n * k * 10), num(n * k // 10) if n * k // 10 != n else num(n * k * 100), num(n + k)],
                   "乘以 %s，在後面補 %d 個 0：%s。" % (num(k), len(str(k)) - 1, num(n * k)))

    def count():
        n = R.randint(12, 9999)
        u = R.choice([("萬", 10000), ("十萬", 100000), ("千", 1000)])
        if n * u[1] >= 10 ** 8:
            return None
        q = "%d 個%s是多少？" % (n, u[0])
        v = n * u[1]
        return mcq(q, num(v), [num(v * 10), num(v // 10), num(v * 100), num(v // 100) if v // 100 > n else num(v + u[1])],
                   "%d 個%s ＝ %d萬%s ＝ %s。" % (n, u[0], v // 10000, v % 10000 or "", num(v)) if v >= 10000 else "%s。" % num(v))
    return pick_unique(R, cmp_, 8, seen) + pick_unique(R, times, 6, seen) + pick_unique(R, count, 6, seen)


def s4(seen):
    def add():
        a1, a2 = R.randint(10, 600), R.randint(100, 9000)
        b1, b2 = R.randint(10, 300), R.randint(100, 9000)
        a, b = a1 * 10000 + a2, b1 * 10000 + b2
        if R.random() < .5:
            s = a + b
            q = "%s ＋ %s ＝" % (wan(a), wan(b))
            w = ["%d萬%d" % (a1 + b1, a2 + b2) if a2 + b2 >= 10000 else wan(s + 10000), wan(s + 1000), wan(s - 10000), wan(s + 100000)]
            return mcq(q, wan(s), w, "萬和萬相加，後面 4 位和 4 位相加，滿 1萬 要進位：%s。" % wan(s))
        if a < b:
            a, b, a1, a2, b1, b2 = b, a, b1, b2, a1, a2
        d = a - b
        if d < 10000:
            return None
        q = "%s － %s ＝" % (wan(a), wan(b))
        w = ["%d萬%d" % (a1 - b1, abs(a2 - b2)) if a2 < b2 else wan(d + 1000), wan(d + 10000), wan(d - 10000) if d > 20000 else wan(d + 20000), wan(d - 1000)]
        return mcq(q, wan(d), w, "萬和萬相減，後面 4 位不夠減時向萬借 1（＝ 10000）：%s。" % wan(d))
    return pick_unique(R, add, 20, seen)


def s5(seen):
    def bills():
        a, b, c = R.randint(1, 9), R.randint(1, 9), R.randint(1, 9)
        k = R.choice([("百萬", "十萬", "萬", 10000), ("十萬", "萬", "千", 1000), ("千萬", "百萬", "十萬", 100000)])
        q = "%d 個%s、%d 個%s、%d 個%s合起來是多少？" % (a, k[0], b, k[1], c, k[2])
        u = k[3]
        v = a * u * 100 + b * u * 10 + c * u
        return mcq(q, num(v), [num(x) for x in (v // 10, v * 10, a * u * 1000 + b * u * 10 + c * u, v + u * 10)],
                   "%d 個%s是 %s，%d 個%s是 %s，%d 個%s是 %s，合起來 %s。" % (a, k[0], num(a * u * 100), b, k[1], num(b * u * 10), c, k[2], num(c * u), num(v)))

    def city():
        P = [("台北市", 2480000), ("新北市", 4040000), ("台中市", 2850000), ("高雄市", 2730000), ("台南市", 1860000), ("桃園市", 2330000)]
        (n1, p1), (n2, p2) = R.sample(P, 2)
        p1 += R.randint(1, 9) * 1000
        p2 += R.randint(1, 9) * 1000
        q = "%s大約有 %s 人，%s大約有 %s 人。哪一個人比較多？多多少人？" % (n1, num(p1), n2, num(p2))
        big, small = (n1, n2) if p1 > p2 else (n2, n1)
        d = abs(p1 - p2)
        return mcq(q, "%s，多 %s 人" % (big, num(d)), ["%s，多 %s 人" % (small, num(d)), "%s，多 %s 人" % (big, num(p1 + p2)), "%s，多 %s 人" % (big, num(d + 100000))],
                   "%s － %s ＝ %s（人）。" % (num(max(p1, p2)), num(min(p1, p2)), num(d)))

    def yi():
        k = R.choice([10, 100, 1000, 10000])
        q = "1 億是多少個 %s？" % num(k) if R.random() < .5 else None
        if q:
            return mcq(q, "%s 個" % num(10 ** 8 // k), ["%s 個" % num(x) for x in (10 ** 8 // k // 10, 10 ** 8 // k * 10, 10 ** 8 // k // 100, k)],
                       "1 億 ＝ 100,000,000，是 %s 個 %s。" % (num(10 ** 8 // k), num(k)))
        n = R.randint(10, 99) * 1000000
        q = "%s 再加多少就是 1 億？" % num(n)
        return mcq(q, num(10 ** 8 - n), [num(10 ** 7 - n % 10 ** 7) if n % 10 ** 7 else num(10 ** 8 - n + 10 ** 6), num(10 ** 8 - n + 10 ** 7), num(10 ** 8 - n - 10 ** 6)],
                   "1 億 ＝ 10000萬，%s ＝ %d萬，10000萬 － %d萬 ＝ %d萬。" % (num(n), n // 10000, n // 10000, (10 ** 8 - n) // 10000))
    return pick_unique(R, bills, 7, seen) + pick_unique(R, city, 7, seen) + pick_unique(R, yi, 6, seen)


def main():
    seen = set()
    sets = [("萬、十萬、百萬、千萬", s1(seen)), ("讀和寫大數", s2(seen)), ("比大小和幾個萬", s3(seen)),
            ("用萬來加減", s4(seen)), ("生活中的大數", s5(seen))]
    demo = table(["千萬位", "百萬位", "十萬位", "萬位", "千位", "百位", "十位", "個位"], [["3", "2", "0", "5", "0", "4", "0", "0"]])
    body = lesson(
        ["10 個一萬是<b>十萬</b>，10 個十萬是<b>百萬</b>，10 個百萬是<b>千萬</b>，10 個千萬是<b>一億</b>。",
         "讀大數：<b>以萬為單位</b>，先讀萬前面的數加「萬」，再讀後面 4 位。32050400 讀作三千二百零五萬零四百。",
         "也可以寫成 <b>3205萬400</b>。用萬來加減，萬和萬加減、後面 4 位和 4 位加減。"],
        [example("32050400 怎麼讀？" + demo, ["萬前面是 3205：三千二百零五萬。", "後面是 0400：零四百。"], "三千二百零五萬零四百"),
         example("30萬1200 ＋ 21萬300 ＝", ["萬：30 ＋ 21 ＝ 51。", "後面：1200 ＋ 300 ＝ 1500。"], "51萬1500")],
        [("三千萬零五 寫成 3005", "千萬是 8 位數，沒有的位寫 0：30,000,005"),
         ("32050400 讀成三千二百零五萬四百", "中間有 0 要讀「零」：…萬零四百"),
         ("百萬位和十萬位弄反", "從個位往左數：個、十、百、千、萬、十萬、百萬、千萬")])
    faq = [{"q": "四年級的大數要學到多少？",
            "a": "108課綱 N-4-1：一億以內的數，認識萬、十萬、百萬、千萬的位值，並會用「30萬1200」這樣的寫法做加減。"},
           {"q": "大數怎麼讀比較不會錯？",
            "a": "從右邊每 4 位分一段：後面 4 位是「個」，前面 4 位是「萬」。先讀萬的那一段加「萬」，再讀後面；中間有 0 讀一個「零」。"},
           {"q": "1億是多少？",
            "a": "1億 ＝ 10000萬 ＝ 100,000,000，是 1 後面 8 個 0。"}]
    make_unit(R, "grade-4", "numbers-to-100-million", "N-4-1",
              "一億以內的數：位值單位「萬」、「十萬」、「百萬」、「千萬」。建立應用大數時之計算習慣，如「30萬1200」與「21萬300」的加減法。",
              "一億以內的數：萬、十萬、百萬、千萬",
              "四年級數學 大數 練習題｜一億以內的數・讀寫大數・萬的加減 學習單（附解答）",
              "一億以內的數",
              "國小四年級數學「一億以內的數」免費學習單：萬、十萬、百萬、千萬的位值，大數的讀法和寫法，比大小，用萬來加減和生活中的大數。100題線上練習馬上對答案，附可列印解答。",
              "以萬為單位，4 位一段來讀",
              "10 個千萬是一億；中間有 0 要讀「零」。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
