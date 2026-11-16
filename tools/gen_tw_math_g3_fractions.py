# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：分數（108課綱 N-3-9 簡單同分母分數）
  python3 tools/gen_tw_math_g3_fractions.py
塗色部分是幾分之幾、單位分數的累加、同分母分數的比較・加減（結果不超過1）、「和等於1」、應用問題。
誤答：分母同士も足す（2/5+1/5→3/10）、分子と分母を逆にする、單位分數は分母が大きいほど大きいと思う。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, fig, svg_wrap, GREEN, FILL, INK

R = random.Random(31009)
NM = Names(R)
ZH = "零一二三四五六七八九十"


def F(a, b):
    return fr(a, b)


def word(a, b):
    """5分之3"""
    return "%s分之%s" % (ZH[b] if b <= 10 else b, ZH[a] if a <= 10 else a)


def bar(k, n, w=300):
    seg = w / n
    s = []
    for i in range(n):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='44' fill='%s' stroke='%s' stroke-width='2'/>" % (
            6 + i * seg, seg, FILL if i < k else "#fff", GREEN))
    return fig(svg_wrap(w + 12, 56, "".join(s), "長條平分成%d份，塗了%d份" % (n, k)))


def pie(k, n):
    import math
    cx, cy, r = 60, 60, 52
    s = ["<circle cx='%d' cy='%d' r='%d' fill='#fff' stroke='%s' stroke-width='2'/>" % (cx, cy, r, GREEN)]
    for i in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        if i < k:
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (
                cx, cy, x0, y0, r, r, x1, y1, FILL, GREEN))
        else:
            s.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='2'/>" % (cx, cy, x0, y0, GREEN))
    return fig(svg_wrap(120, 120, "".join(s), "圓平分成%d份，塗了%d份" % (n, k)))


def s1(seen):
    def mk():
        n = R.randint(2, 10)
        k = R.randint(1, n - 1)
        pic = bar(k, n) if R.random() < .6 or n > 8 else pie(k, n)
        q = "塗色的部分是全部的幾分之幾？" + pic
        return mcq(q, F(k, n), [F(n, k) if k > 1 else F(n, n), F(k, n - k) if n - k != n else F(k + 1, n), F(n - k, n) if n - k != k else F(k, n + 1), F(1, n) if k != 1 else F(2, n)],
                   "全部平分成 %d 份，塗了 %d 份，是 %s（%s）。" % (n, k, F(k, n), word(k, n)))
    return pick_unique(R, mk, 20, seen)


def s2(seen):
    def count_unit():
        n = R.randint(3, 10)
        k = R.randint(2, n)
        q = "%d 個 %s 合起來是多少？" % (k, F(1, n))
        ans = F(k, n) if k < n else "1"
        w = [F(k, n * k), F(1, n * k), F(1, k * n + 0) if False else F(k + 1, n), F(n, k)]
        if k == n:
            w = [F(n, n * n), F(1, n), F(n - 1, n), "2"]
        return mcq(q, ans, w, "%d 個 %s 是 %s%s。" % (k, F(1, n), F(k, n), "，也就是 1" if k == n else ""))

    def how_many():
        n = R.randint(3, 10)
        k = R.randint(2, n - 1)
        q = "%s 是幾個 %s？" % (F(k, n), F(1, n))
        return mcq(q, "%d個" % k, ["%d個" % x for x in (n, n - k, k + 1, 1, n + k, k - 1) if x > 0],
                   "%s 是 %d 個 %s 合起來的。" % (F(k, n), k, F(1, n)))

    def one():
        n = R.randint(2, 10)
        q = "1 ＝ 幾個 %s？" % F(1, n)
        return mcq(q, "%d個" % n, ["%d個" % x for x in (1, n - 1, n + 1, 2 * n)],
                   "把 1 平分成 %d 份，就有 %d 個 %s，所以 1 ＝ %s。" % (n, n, F(1, n), F(n, n)))

    def read():
        n = R.randint(3, 10)
        k = R.randint(1, n - 1)
        q = "%s 的讀法是哪一個？" % F(k, n)
        return mcq(q, word(k, n), [word(n, k) if k > 1 else "%s分之%s" % (ZH[1], ZH[n]), "%s又%s" % (ZH[k], ZH[n]), "%s分之%s" % (ZH[k], ZH[k]) if k != n else word(1, n)],
                   "分數先讀分母（下面），再讀分子（上面）：%s 讀作「%s」。" % (F(k, n), word(k, n)))
    return pick_unique(R, count_unit, 6, seen) + pick_unique(R, how_many, 5, seen) + pick_unique(R, one, 4, seen) + pick_unique(R, read, 5, seen)


def s3(seen):
    def same_den():
        n = R.randint(4, 12)
        a, b = R.sample(range(1, n), 2)
        sign = ">" if a > b else "<"
        q = "%s ○ %s，○ 裡要填什麼？" % (F(a, n), F(b, n))
        return mcq(q, sign, ["<" if sign == ">" else ">", "=", "+"],
                   "分母一樣，分子大的比較大：%d %s %d，所以 %s %s %s。" % (a, sign, b, F(a, n), sign, F(b, n)))

    def unit():
        a, b = R.sample(range(2, 11), 2)
        sign = ">" if a < b else "<"
        q = "%s ○ %s，○ 裡要填什麼？" % (F(1, a), F(1, b))
        return mcq(q, sign, ["<" if sign == ">" else ">", "=", "+"],
                   "一樣是 1 份，平分得越多份，每份越小。%s %s %s。" % (F(1, a), sign, F(1, b)))

    def biggest():
        n = R.randint(5, 12)
        ks = R.sample(range(1, n + 1), 4)
        big = max(ks)
        q = "%s 中，哪一個分數最大？" % "、".join(F(k, n) for k in ks)
        return mcq(q, F(big, n), [F(k, n) for k in ks if k != big],
                   "分母都是 %d，分子 %d 最大，所以 %s 最大。" % (n, big, F(big, n)))
    return pick_unique(R, same_den, 7, seen) + pick_unique(R, unit, 7, seen) + pick_unique(R, biggest, 6, seen)


def s4(seen):
    def add():
        n = R.randint(3, 12)
        a = R.randint(1, n - 2)
        b = R.randint(1, n - a)
        s = a + b
        ans = F(s, n) if s < n else "1"
        q = "%s ＋ %s ＝" % (F(a, n), F(b, n))
        w = [F(s, n + n), F(s, 2 * n) if 2 * n != n + n else F(s, n * 2), F(a * b, n), F(s + 1, n) if s + 1 <= n else F(s - 1, n), F(abs(a - b), n) if a != b else F(s, n + 1)]
        if s == n:
            w = [F(n, n * 2), F(n - 1, n), F(1, n), "2"]
        return mcq(q, ans, w, "分母一樣，分子相加，分母不變：%d 個 %s ＋ %d 個 %s ＝ %d 個 %s ＝ %s。" % (a, F(1, n), b, F(1, n), s, F(1, n), ans))

    def sub():
        n = R.randint(3, 12)
        a = R.randint(2, n)
        b = R.randint(1, a - 1)
        d = a - b
        A = F(a, n) if a < n else "1"
        q = "%s － %s ＝" % (A, F(b, n))
        w = [F(d, n + 1), F(a + b, n) if a + b <= 12 else F(d + 1, n), F(n - d, n) if n - d != d else F(d + 2, n),
             F(b, n) if b != d else F(d - 1 if d > 1 else d + 1, n), F(d + 1, n)]
        return mcq(q, F(d, n), w,
                   "%s 是 %d 個 %s，拿走 %d 個，剩 %d 個 %s ＝ %s。" % (A, a, F(1, n), b, d, F(1, n), F(d, n)))

    def to_one():
        n = R.randint(3, 12)
        a = R.randint(1, n - 1)
        q = "%s ＋ ☐ ＝ 1，☐ 是多少？" % F(a, n)
        return mcq(q, F(n - a, n), [F(a, n) if a != n - a else F(a + 1, n), F(1, n) if n - a != 1 else F(2, n), F(n - a, 2 * n), F(n, a)],
                   "1 ＝ %s，%d 個 %s 再加 %d 個就是 %d 個，所以 ☐ ＝ %s。" % (F(n, n), a, F(1, n), n - a, n, F(n - a, n)))
    return pick_unique(R, add, 8, seen) + pick_unique(R, sub, 6, seen) + pick_unique(R, to_one, 6, seen)


def s5(seen):
    def cake():
        n = R.choice([4, 6, 8, 10, 12])
        a = R.randint(1, n // 2)
        b = R.randint(1, n - a - 1)
        who1, who2 = NM.next(), NM.next()
        q = "一個蛋糕平分成 %d 塊。%s吃了 %d 塊，%s吃了 %d 塊。兩人一共吃了這個蛋糕的幾分之幾？" % (n, who1, a, who2, b)
        s = a + b
        return mcq(q, F(s, n), [F(s, 2 * n), F(n - s, n), F(a * b, n) if a * b != s and a * b < n else F(s + 1, n), F(s, n - s) if n - s != n else F(s - 1, n)],
                   "一塊是 %s，吃了 %d ＋ %d ＝ %d 塊，是 %s。" % (F(1, n), a, b, s, F(s, n)))

    def rope():
        n = R.choice([5, 6, 7, 8, 9, 10])
        u = R.randint(1, n - 1)
        q = "一條緞帶平分成 %d 段，用掉了 %d 段。還剩下這條緞帶的幾分之幾？" % (n, u)
        left = n - u
        return mcq(q, F(left, n), [F(u, n) if u != left else F(left + 1, n), F(left, u) if u != left else F(left, n + 1), F(1, n) if left != 1 else F(2, n), F(left, 2 * n)],
                   "全部是 %s，用掉 %s，剩下 %s。" % (F(n, n), F(u, n), F(left, n)))

    def water():
        n = R.choice([5, 6, 8, 10])
        a, b = R.randint(1, n - 2), 0
        b = R.randint(1, n - a)
        who = NM.next()
        q = "%s早上喝了 %s 公升的水，下午喝了 %s 公升。這一天一共喝了多少公升？" % (who, F(a, n), F(b, n))
        s = a + b
        ans = (F(s, n) if s < n else "1") + " 公升"
        w = [F(s, 2 * n) + " 公升", (F(s + 1, n) if s + 1 < n else F(s - 1, n)) + " 公升", F(abs(a - b) or 1, n) + " 公升", F(s, n + 1) + " 公升"]
        return mcq(q, ans, w, "%s ＋ %s ＝ %s（公升）。" % (F(a, n), F(b, n), ans.replace(" 公升", "")))
    return pick_unique(R, cake, 7, seen) + pick_unique(R, rope, 7, seen) + pick_unique(R, water, 6, seen)


def main():
    seen = set()
    sets = [("塗色的部分是幾分之幾", s1(seen)), ("分數的意義：幾個幾分之一", s2(seen)),
            ("比大小", s3(seen)), ("同分母分數的加減", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["把一個東西<b>平分</b>成 5 份，1 份是 %s（五分之一），3 份是 %s（五分之三）。" % (F(1, 5), F(3, 5)),
         "下面的數叫<b>分母</b>（平分成幾份），上面的數叫<b>分子</b>（取了幾份）。",
         "分母一樣時，<b>分子越大，分數越大</b>。%s 和 %s：平分得越多份，每份越小。" % (F(1, 3), F(1, 5)),
         "同分母分數相加減：<b>分母不變，分子相加減</b>。"],
        [example("%s ＋ %s ＝" % (F(2, 7), F(3, 7)), ["2 個 %s 加 3 個 %s 是 5 個 %s。" % (F(1, 7), F(1, 7), F(1, 7)), "分母 7 不變。"], F(5, 7)),
         example("%s ＋ ☐ ＝ 1" % F(3, 8), ["1 ＝ %s。" % F(8, 8), "8 － 3 ＝ 5。"], F(5, 8))],
        [("%s ＋ %s ＝ %s（分母也相加）" % (F(2, 5), F(1, 5), F(3, 10)), "分母不變：%s" % F(3, 5)),
         ("%s 比 %s 大（因為 5 比 3 大）" % (F(1, 5), F(1, 3)), "平分越多份，每份越小：%s 比較大" % F(1, 3)),
         ("沒有平分也寫成分數", "一定要先「平分」，每份一樣大才能用分數")])
    faq = [{"q": "三年級的分數要學到哪裡？",
            "a": "108課綱 N-3-9：認識簡單的同分母分數，會比較大小和加減，分數與答案都不超過2，並知道「和等於1」的意思。本頁的加減以答案不超過1為主。"},
           {"q": "孩子常把分母也相加，怎麼辦？",
            "a": "用「幾個幾分之一」來想：%s 是 2 個 %s，再加 1 個是 3 個 %s，分母（每份的大小）不會變。" % (F(2, 5), F(1, 5), F(1, 5))},
           {"q": "為什麼五分之一比三分之一小？",
            "a": "一樣大的蛋糕，分給 5 個人比分給 3 個人，每人分到的比較少，所以 %s 比 %s 小。" % (F(1, 5), F(1, 3))}]
    make_unit(R, "grade-3", "fractions", "N-3-9",
              "簡單同分母分數：結合操作活動與整數經驗。簡單同分母分數比較、加、減的意義。牽涉之分數與運算結果皆不超過2。以單位分數之點數為基礎，連結整數之比較、加、減。知道「和等於1」的意義。",
              "分數：幾分之幾、比大小與同分母加減",
              "三年級數學 分數 練習題｜幾分之幾・比大小・同分母分數加減 學習單（附解答）",
              "分數",
              "國小三年級數學「分數」免費學習單：看圖寫出幾分之幾、單位分數、同分母分數比大小和加減、和等於1的應用題。100題線上練習馬上對答案，附可列印解答。",
              "平分成幾份是分母，取了幾份是分子",
              "同分母分數相加減：分母不變，分子相加減。",
              body, faq, sets, 8)


if __name__ == "__main__":
    main()
