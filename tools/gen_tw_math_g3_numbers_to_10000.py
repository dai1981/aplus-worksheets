# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：10000以內的數（108課綱 N-3-1）
  python3 tools/gen_tw_math_g3_numbers_to_10000.py
位值（千、百、十、一）、國字與數字的讀寫（含「零」）、大小比較、位值單位換算、錢與數的規律。
"""
import random
from tw_common import mcq, num, lesson, example, table, make_unit, pick_unique, Names

R = random.Random(31001)
DIG = "零一二三四五六七八九"
PLACE = ["個位", "十位", "百位", "千位"]
UNIT = ["一", "十", "百", "千"]


def zh(n):
    """國字：3405 → 三千四百零五、3050 → 三千零五十、10000 → 一萬"""
    if n == 10000:
        return "一萬"
    if n == 0:
        return "零"
    s = str(n)
    out, zero = "", False
    L = len(s)
    for i, ch in enumerate(s):
        d = int(ch)
        p = L - 1 - i
        if d == 0:
            zero = True
            continue
        if zero and out:
            out += "零"
        zero = False
        if p == 1 and d == 1 and out == "":
            out += "十"           # 15 → 十五
        else:
            out += DIG[d] + ("" if p == 0 else ["", "十", "百", "千"][p])
    return out


def digits(n):
    return [int(c) for c in str(n).zfill(4)][::-1]   # [個, 十, 百, 千]


def rnum(lo=1000, hi=9999, zeros=0):
    while True:
        n = R.randint(lo, hi)
        if str(n).count("0") >= zeros:
            return n


# ------------------------------------------------------------ set 1：位值
def s1():
    def a():
        n = rnum(1000, 9999)
        d = digits(n)
        if len(set(d)) < 4:
            return None
        k = R.randint(0, 3)
        q = "%s 的<b>%s</b>數字是多少？" % (n, PLACE[k])
        wrong = [d[j] for j in range(4) if j != k]
        return mcq(q, d[k], wrong + [d[k] * 10], "%s：千位 %d、百位 %d、十位 %d、個位 %d。" % (n, d[3], d[2], d[1], d[0]))

    def b():
        th, h, t, o = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9), R.randint(0, 9)
        n = th * 1000 + h * 100 + t * 10 + o
        parts = ["%d個千" % th]
        if h: parts.append("%d個百" % h)
        if t: parts.append("%d個十" % t)
        if o: parts.append("%d個一" % o)
        if len(parts) < 3:
            return None
        q = "、".join(parts) + "合起來是多少？"
        w = [int("%d%d%d" % (th, h, t)) if o == 0 else int("%d%d%d" % (th, h or t, o)),
             th * 1000 + t * 100 + h * 10 + o, th * 100 + h * 10 + t + o * 1000, n + 1000]
        return mcq(q, num(n), [num(x) for x in w if x != n] + [num(n + 100), num(n - 100)],
                   "千位寫 %d、百位寫 %d、十位寫 %d、個位寫 %d，是 %s。沒有的位要寫 0。" % (th, h, t, o, num(n)))

    def c():
        n = rnum(1000, 9999)
        d = digits(n)
        k = R.randint(1, 3)
        if d[k] == 0:
            return None
        v = d[k] * [1, 10, 100, 1000][k]
        q = "%s 的<b>%s</b>數字 %d 代表多少？" % (n, PLACE[k], d[k])
        w = [d[k], d[k] * [1, 10, 100, 1000][k - 1] if k > 0 else d[k] * 10, d[k] * 10000]
        if k < 3:
            w.append(d[k] * [1, 10, 100, 1000][k + 1])
        return mcq(q, num(v), [num(x) for x in w], "%s的 %d 代表 %d 個%s，就是 %s。" % (PLACE[k], d[k], d[k], UNIT[k], num(v)))
    out = []
    seen = set()
    for mk, k in ((a, 7), (b, 7), (c, 6)):
        out += pick_unique(R, mk, k, seen)
    return out


# ------------------------------------------------------------ set 2：讀與寫（國字 ↔ 數字）
def s2(seen):
    def a():   # 國字 → 數字（0 の位置がポイント）
        n = rnum(1001, 9999, zeros=1)
        q = "「%s」寫成數字是多少？" % zh(n)
        s = str(n)
        nz = s.replace("0", "")
        w = [int(nz)]                                                             # 0 を書かない
        import itertools
        moved = sorted({int("".join(p)) for p in itertools.permutations(s)
                        if p[0] != "0" and "".join(p) != s and [c for c in p if c != "0"] == list(nz)})
        R.shuffle(moved)
        w += moved                                                                # 0 の場所がずれる
        w.append(int(s[:1] + "0" + s[1:]))                                        # 0 を多く書く
        return mcq(q, num(n), [num(x) for x in w if x != n], "%s：千位 %s、百位 %s、十位 %s、個位 %s。空的位寫 0。" % (zh(n), s[0], s[1], s[2], s[3]))

    def b():   # 數字 → 國字
        n = rnum(1001, 9999, zeros=1)
        s = str(n)
        q = "%s 的國字寫法是哪一個？" % n
        w = []
        if "0" in s[1:3]:
            w.append(zh(n).replace("零", ""))                                    # 零を書かない
        w.append(zh(int(s[0] + s[2] + s[1] + s[3])) if s[1] != s[2] else None)
        w.append(zh(int(s[:3] + "0")) if s[3] != "0" else zh(n + 1))
        w.append(zh(n + 100) if n + 100 <= 9999 else zh(n - 100))
        w.append(zh(n + 10))
        return mcq(q, zh(n), w, "%s 讀作「%s」。中間有 0 時要讀「零」。" % (n, zh(n)))
    return pick_unique(R, a, 10, seen) + pick_unique(R, b, 10, seen)


# ------------------------------------------------------------ set 3：大小比較・排序
def s3(seen):
    def a():
        x = rnum(1000, 9999)
        k = R.choice([0, 1, 2, 3])
        d = digits(x)
        y = x + R.choice([1, -1]) * [1, 10, 100, 1000][k] * R.randint(1, 3)
        if not 1000 <= y <= 9999 or y == x:
            return None
        sign = ">" if x > y else "<"
        q = "%s ○ %s，○ 裡要填什麼？" % (x, y)
        return mcq(q, sign, [">" if sign == "<" else "<", "=", "+"],
                   "從千位開始比，千位一樣就比百位，再比十位、個位。%s %s %s。" % (x, sign, y))

    def b():
        base = rnum(1000, 9000)
        ns = sorted({base + R.choice([0, 9, 90, 900, 99, 909]) + R.randint(0, 9) for _ in range(6)})
        if len(ns) < 4:
            return None
        ns = R.sample(ns, 4)
        big = max(ns)
        q = "%s 中，哪一個數最大？" % "、".join(str(x) for x in ns)
        return mcq(q, num(big), [num(x) for x in sorted(ns) if x != big],
                   "位數一樣時，從最高位（千位）開始比。最大的是 %s。" % num(big))

    def c():
        ds = R.sample(range(1, 10), 3) + [0]
        R.shuffle(ds)
        big = int("".join(str(x) for x in sorted(ds, reverse=True)))
        sm = sorted(ds)
        small = int(str(sm[1]) + "0" + "".join(str(x) for x in sm[2:]))   # 0 は先頭にできない
        if R.random() < .5:
            q = "用 %s 這四張數字卡排成四位數，最大的數是多少？" % "、".join(str(x) for x in ds)
            w = [int("".join(str(x) for x in sorted(ds))) , small, int(str(big)[:2] + str(big)[3] + str(big)[2])]
            return mcq(q, num(big), [num(x) for x in w if x != big] + [num(big - 1)], "大的數字放在高的位：%s。" % num(big))
        q = "用 %s 這四張數字卡排成四位數，最小的數是多少？" % "、".join(str(x) for x in ds)
        w = [int("".join(str(x) for x in sm)), big, int(str(sm[1]) + str(sm[2]) + "0" + str(sm[3]))]
        return mcq(q, num(small), [num(x) for x in w if x != small and x >= 100] + [num(small + 1)],
                   "0 不能放在千位。千位放最小的非 0 數字，0 放在百位：%s。" % num(small))
    return pick_unique(R, a, 7, seen) + pick_unique(R, b, 6, seen) + pick_unique(R, c, 7, seen)


# ------------------------------------------------------------ set 4：位值單位換算
def s4(seen):
    def a():
        k = R.choice(["百", "十"])
        u = 100 if k == "百" else 10
        th = R.randint(1, 9)
        n = th * 1000
        ans = n // u
        q = "%s 是幾個%s？" % (num(n), k)
        return mcq(q, "%d個%s" % (ans, k), ["%d個%s" % (x, k) for x in (th, ans * 10, ans // 10 if ans >= 100 else th * 1000)] + ["%d個%s" % (ans + th, k)],
                   "1個千 = %d個%s，%d個千 = %d個%s。" % (1000 // u, k, th, ans, k))

    def b():
        k = R.choice(["百", "十"])
        u = 100 if k == "百" else 10
        m = R.randint(12, 99) if k == "百" else R.randint(120, 999)
        n = m * u
        if n > 9999:
            return None
        q = "%d個%s是多少？" % (m, k)
        w = [m * u // 10, m * u * 10, m + u, m * (u // 10 if u > 10 else 100)]
        return mcq(q, num(n), [num(x) for x in w if x != n and x > 0],
                   "%d個%s就是 %d × %d = %s。" % (m, k, m, u, num(n)))

    def c():
        th, h, t = R.randint(1, 8), R.randint(10, 19), R.randint(1, 9)
        n = th * 1000 + h * 100 + t * 10
        q = "%d個千、%d個百和%d個十合起來是多少？" % (th, h, t)
        w = [int("%d%d%d0" % (th, h, t)) if len(str(h)) == 2 else None, th * 1000 + (h % 10) * 100 + t * 10, n + 1000, n - 100]
        return mcq(q, num(n), [num(x) for x in w if x and x != n],
                   "%d個百 = 1個千和%d個百，所以是 %d個千、%d個百、%d個十 = %s。" % (h, h - 10, th + 1, h - 10, t, num(n)))

    def d():
        n = R.choice([1000, 10000])
        if n == 10000:
            q = "10個一千是多少？"
            return mcq(q, "10,000（一萬）", ["1,000（一千）", "100,000（十萬）", "1,010"], "10個千 = 1個萬，就是 10,000（一萬）。")
        k = R.choice([(10, "百"), (100, "十")])
        q = "1000 是幾個%s？" % k[1]
        return mcq(q, "%d個%s" % (k[0], k[1]), ["%d個%s" % (x, k[1]) for x in (1, 1000, 10 if k[0] == 100 else 100)],
                   "1000 = %d個%s。" % (k[0], k[1]))
    return (pick_unique(R, a, 5, seen) + pick_unique(R, b, 6, seen) + pick_unique(R, c, 6, seen)
            + pick_unique(R, d, 3, seen))


# ------------------------------------------------------------ set 5：應用（錢・規律）
def s5(seen):
    nm = Names(R)

    def a():   # 千元・百元・十元
        a1, b1, c1 = R.randint(1, 7), R.randint(0, 9), R.randint(1, 9)
        n = a1 * 1000 + b1 * 100 + c1 * 10
        who = nm.next()
        q = "%s有 %d 張1000元鈔票、%d 張100元鈔票和 %d 個10元硬幣，一共有多少元？" % (who, a1, b1, c1)
        w = [a1 * 1000 + c1 * 100 + b1 * 10, a1 + b1 + c1, a1 * 100 + b1 * 10 + c1, n + 1000]
        return mcq(q, "%s元" % num(n), ["%s元" % num(x) for x in w if x != n] + ["%s元" % num(n + 10)],
                   "1000元 %d 張是 %s元，100元 %d 張是 %d元，10元 %d 個是 %d元，合起來是 %s元。" % (a1, num(a1 * 1000), b1, b1 * 100, c1, c1 * 10, num(n)))

    def b():   # 規律
        step = R.choice([10, 100, 1000, 50, 200])
        start = R.randint(1, 5) * 1000 + R.randint(0, 9) * 100 + R.choice([0, 10, 20, 50])
        seq = [start + step * i for i in range(5)]
        if seq[-1] > 9999:
            return None
        k = R.randint(1, 4)
        shown = [("☐" if i == k else str(x)) for i, x in enumerate(seq)]
        q = "依照規律，☐ 裡是多少？ " + "、".join(shown)
        w = [seq[k] + step, seq[k] - step if k > 1 else seq[k] + 2 * step, seq[k] + (10 if step != 10 else 100), seq[k] + 1]
        return mcq(q, num(seq[k]), [num(x) for x in w if x != seq[k]], "每次多 %d，所以 ☐ = %s。" % (step, num(seq[k])))

    def c():   # 數線のような「多/少」
        n = rnum(1100, 8900)
        k = R.choice([10, 100, 1000])
        more = R.random() < .5
        ans = n + k if more else n - k
        q = "比 %s %s %d 的數是多少？" % (n, "多" if more else "少", k)
        w = [n - k if more else n + k, n + (k // 10 if k > 10 else 100) * (1 if more else -1), n + k * 10 * (1 if more else -1)]
        return mcq(q, num(ans), [num(x) for x in w if 0 < x <= 99999 and x != ans] + [num(ans + 1)],
                   "%s %s %d = %s。" % (n, "+" if more else "−", k, num(ans)))

    def d():   # 最接近
        n = rnum(1000, 9999)
        h = round(n, -3)
        if h in (0, 10000) or n % 1000 == 500:
            return None
        q = "%s 最接近哪一個整千？" % n
        lo, hi = (n // 1000) * 1000, (n // 1000 + 1) * 1000
        other = hi if h == lo else lo
        return mcq(q, num(h), [num(x) for x in (other, round(n, -2), h + 1000, h - 1000, h + 2000) if 1000 <= x <= 10000 and x != h],
                   "%s 在 %s 和 %s 之間，比較靠近 %s。" % (n, num(lo), num(hi), num(h)))
    return (pick_unique(R, a, 6, seen) + pick_unique(R, b, 5, seen) + pick_unique(R, c, 5, seen)
            + pick_unique(R, d, 4, seen))


def main():
    seen = set()
    set1 = s1()
    seen.update(it["q"] for it in set1)
    sets = [("位值：千、百、十、一", set1), ("國字和數字的讀寫", s2(seen)), ("比大小和排數字卡", s3(seen)),
            ("位值單位換算", s4(seen)), ("應用問題：錢和規律", s5(seen))]
    body = lesson(
        ["四位數從左邊起是<b>千位、百位、十位、個位</b>。",
         "<b>10個百 = 1個千</b>，<b>10個千 = 1個萬（10,000）</b>。",
         "中間的位是空的，數字要寫 <b>0</b>，讀的時候要讀「<b>零</b>」。"],
        [table(["千位", "百位", "十位", "個位"], [["3", "0", "4", "5"]]),
         example("「三千零四十五」寫成數字是多少？", ["3個千、0個百、4個十、5個一。", "百位沒有，要寫 0。"], "3045"),
         example("2468 和 2486 哪一個比較大？", ["千位都是 2，百位都是 4。", "十位：6 比 8 小。"], "2486 比較大")],
        [("「三千零五」寫成 305", "千位、百位、十位、個位都要寫：3005"),
         ("比大小時先看個位", "先比最高位（千位），一樣再往下比"),
         ("2400 讀成「二千四」", "要讀完整：二千四百")])
    faq = [{"q": "三年級的10000以內的數要學什麼？",
            "a": "認識千位，會讀寫四位數和一萬，知道中間的 0 要讀「零」，能比較大小，並會做位值換算，例如 10個百 = 1個千。"},
           {"q": "孩子常把三千零五寫成305，怎麼教？",
            "a": "先畫千、百、十、個四格的位值表，每一格都要填數字，沒有的位填 0，就不會漏掉。"},
           {"q": "這份學習單可以免費列印嗎？",
            "a": "可以。線上練習100題會馬上對答案，另有A4學習單和解答可以免費列印。"}]
    make_unit(R, "grade-3", "numbers-to-10000", "N-3-1",
              "一萬以內的數：含位值積木操作活動。結合點數、位值表徵、位值表。位值單位「千」。位值單位換算。",
              "10000以內的數：位值、讀寫與比大小",
              "三年級數學 10000以內的數 練習題｜位值・國字・比大小 學習單（附解答）",
              "10000以內的數",
              "國小三年級數學「10000以內的數」免費學習單：認識千位、讀寫四位數（含「零」）、比大小、位值換算和錢的應用題。100題線上練習馬上對答案，附可列印解答。",
              "千、百、十、一：沒有的位寫 0",
              "10個百是1個千，10個千是1個萬。比大小從千位開始比。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
