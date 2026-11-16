# -*- coding: utf-8 -*-
"""
台灣 國小三年級 數學：一位小數（108課綱 N-3-10）
  python3 tools/gen_tw_math_g3_decimals.py
0.1 的意義、幾個0.1、十分位、小數與分數、比大小、一位小數的加減（含直式）、應用問題。
誤答：整數部分と小數部分を別々に足す（2.7＋1.5→3.12）、位をそろえない、0.7と7を混同。
"""
import random
from tw_common import mcq, lesson, example, make_unit, pick_unique, Names, fr, fig, svg_wrap, dnum, GREEN, FILL

R = random.Random(31010)
NM = Names(R)


def D(t):
    """t 個の 0.1 を小數の文字に（23 → 2.3、7 → 0.7、30 → 3）"""
    return dnum(t / 10)


def bar10(k):
    s = []
    for i in range(10):
        s.append("<rect x='%d' y='6' width='28' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (6 + i * 28, FILL if i < k else "#fff", GREEN))
    return fig(svg_wrap(292, 52, "".join(s), "1平分成10份，塗了%d份" % k))


def sep_add(a, b):
    """整數と小數を別々に足す間違い：2.7＋1.5 → 3.12"""
    return "%d.%d" % (a // 10 + b // 10, a % 10 + b % 10)


def s1(seen):
    def pic():
        k = R.randint(1, 9)
        q = "把 1 平分成 10 份，塗色的部分用小數表示是多少？" + bar10(k)
        return mcq(q, D(k), [str(k), "1.%d" % k, D(10 - k) if 10 - k != k else "0.%d" % (k + 1), "0.0%d" % k],
                   "1 份是 0.1，塗了 %d 份，是 %s。" % (k, D(k)))

    def count():
        t = R.randint(11, 99)
        if t % 10 == 0:
            return None
        q = "%s 是幾個 0.1？" % D(t)
        return mcq(q, "%d個" % t, ["%d個" % x for x in (t // 10, t % 10, t * 10, t + 10)],
                   "1 是 10 個 0.1，%s 是 %d 個 0.1。" % (D(t), t))

    def compose():
        t = R.randint(11, 99)
        if t % 10 == 0:
            return None
        q = "%d 個 0.1 是多少？" % t
        return mcq(q, D(t), [str(t), dnum(t / 100) if t < 100 else D(t + 1), D(t + 10), "%d.%d" % (t % 10, t // 10)],
                   "10 個 0.1 是 1，%d 個 0.1 是 %s。" % (t, D(t)))

    def frac():
        k = R.randint(1, 9)
        if R.random() < .5:
            q = "%s 寫成小數是多少？" % fr(k, 10)
            return mcq(q, D(k), [str(k), "1.%d" % k, "%d.1" % k, "0.0%d" % k], "%s 就是 %d 個 0.1，是 %s。" % (fr(k, 10), k, D(k)))
        q = "%s 寫成分數是多少？" % D(k)
        return mcq(q, fr(k, 10), [fr(10, k), fr(1, k), fr(k, 100)], "%s 是 %d 個 0.1，也就是 %s。" % (D(k), k, fr(k, 10)))
    return pick_unique(R, pic, 6, seen) + pick_unique(R, count, 5, seen) + pick_unique(R, compose, 4, seen) + pick_unique(R, frac, 5, seen)


def s2(seen):
    def place():
        t = R.randint(11, 99)
        if t % 10 == 0 or t // 10 == t % 10:
            return None
        k = R.choice(["個位", "十分位"])
        a = t // 10 if k == "個位" else t % 10
        q = "%s 的<b>%s</b>數字是多少？" % (D(t), k)
        o = t % 10 if k == "個位" else t // 10
        return mcq(q, str(a), [str(o), str(a * 10) if a else "10", D(a) if a else "0.1"],
                   "%s：小數點左邊是個位 %d，右邊是十分位 %d。" % (D(t), t // 10, t % 10))

    def unit_mm():
        mm = R.randint(11, 99)
        if mm % 10 == 0:
            return None
        q = "1 毫米 ＝ 0.1 公分。%d 毫米是多少公分？" % mm
        return mcq(q, D(mm) + " 公分", [str(mm) + " 公分", dnum(mm / 100) + " 公分", D(mm + 10) + " 公分", "%d.%d 公分" % (mm % 10, mm // 10)],
                   "%d 毫米是 %d 個 0.1 公分，就是 %s 公分。" % (mm, mm, D(mm)))

    def money():
        t = R.randint(11, 99)
        if t % 10 == 0:
            return None
        q = "1 公升平分成 10 份，1 份是 0.1 公升。一瓶水有 %d 個 0.1 公升，是幾公升？" % t
        return mcq(q, D(t) + " 公升", [str(t) + " 公升", D(t // 10) + " 公升", "%d.%d 公升" % (t % 10, t // 10) if t % 10 != t // 10 else D(t + 1) + " 公升"],
                   "%d 個 0.1 公升是 %s 公升。" % (t, D(t)))
    return pick_unique(R, place, 8, seen) + pick_unique(R, unit_mm, 7, seen) + pick_unique(R, money, 5, seen)


def s3(seen):
    def cmp_():
        a = R.randint(1, 99)
        b = a + R.choice([-12, -9, -3, -1, 1, 3, 9, 11, 20])
        if b <= 0 or b == a or b > 99:
            return None
        sign = ">" if a > b else "<"
        q = "%s ○ %s，○ 裡要填什麼？" % (D(a), D(b))
        return mcq(q, sign, ["<" if sign == ">" else ">", "=", "無法比較"],
                   "先比個位，個位一樣再比十分位：%s %s %s。" % (D(a), sign, D(b)))

    def biggest():
        ts = R.sample(range(3, 99), 4)
        if any(t % 10 == 0 for t in ts):
            return None
        big = max(ts)
        q = "%s 中，哪一個最大？" % "、".join(D(t) for t in ts)
        return mcq(q, D(big), [D(t) for t in ts if t != big], "比個位，再比十分位：最大的是 %s。" % D(big))

    def trap():
        whole = R.randint(1, 8)
        tenth = R.randint(1, 9)
        a = whole * 10 + tenth
        b = (whole + 1) * 10
        q = "%s 和 %d，哪一個比較大？" % (D(a), whole + 1)
        return mcq(q, str(whole + 1), [D(a), "一樣大", "無法比較"],
                   "%s 不到 %d（%s 比 %d 少 %s），所以 %d 比較大。" % (D(a), whole + 1, D(a), whole + 1, D(b - a), whole + 1))
    return pick_unique(R, cmp_, 9, seen) + pick_unique(R, biggest, 6, seen) + pick_unique(R, trap, 5, seen)


def s4(seen):
    def add():
        a, b = R.randint(11, 79), R.randint(11, 79)
        if a % 10 == 0 or b % 10 == 0 or (a % 10 + b % 10) < 10 and R.random() < .6:
            return None
        s = a + b
        q = "%s ＋ %s ＝" % (D(a), D(b))
        return mcq(q, D(s), [sep_add(a, b), D(s - 10), D(s + 10), str(a + b), D(s + 1)],
                   "小數點對齊，像整數一樣相加：%d 個 0.1 ＋ %d 個 0.1 ＝ %d 個 0.1 ＝ %s。" % (a, b, s, D(s)))

    def sub():
        a = R.randint(21, 99)
        b = R.randint(11, a - 5)
        if a % 10 == 0 and R.random() < .5 or b % 10 == 0:
            return None
        d = a - b
        q = "%s － %s ＝" % (D(a), D(b))
        w = ["%d.%d" % (a // 10 - b // 10, abs(a % 10 - b % 10)), D(d + 10), D(d - 10) if d > 10 else D(d + 2), str(d), D(d + 1)]
        return mcq(q, D(d), [x for x in w if x != D(d)],
                   "小數點對齊，不夠減向個位借 1 當 10 個 0.1：%s － %s ＝ %s。" % (D(a), D(b), D(d)))

    def whole():
        a = R.randint(2, 9)
        b = R.randint(1, 9)
        if R.random() < .5:
            q = "%d ＋ %s ＝" % (a, D(b))
            return mcq(q, D(a * 10 + b), [D(a + b), "0.%d" % (a + b) if a + b < 10 else D(a + b + 10), str(a + b)],
                       "%d 是 %d 個 1，加上 %s 是 %s。" % (a, a, D(b), D(a * 10 + b)))
        q = "%d － %s ＝" % (a, D(b))
        d = a * 10 - b
        return mcq(q, D(d), [D(a * 10 - b * 10) if a > b else D(d + 10), D(10 - b), str(a - b) if a > b else D(d - 1), "%d.%d" % (a, b), D(d + 10), D(d - 10)],
                   "%d 看成 %s，%s － %s ＝ %s。" % (a, D(a * 10), D(a * 10), D(b), D(d)))
    return pick_unique(R, add, 8, seen) + pick_unique(R, sub, 8, seen) + pick_unique(R, whole, 4, seen)


def s5(seen):
    def ribbon():
        a, b = R.randint(12, 48), R.randint(12, 48)
        if a % 10 == 0 or b % 10 == 0:
            return None
        who = NM.next()
        q = "%s有一條 %s 公尺的紅緞帶和一條 %s 公尺的藍緞帶，兩條一共長多少公尺？" % (who, D(a), D(b))
        s = a + b
        return mcq(q, D(s) + " 公尺", [sep_add(a, b) + " 公尺", D(abs(a - b)) + " 公尺", D(s + 10) + " 公尺", str(s) + " 公尺", D(s - 10) + " 公尺"],
                   "%s ＋ %s ＝ %s（公尺）。" % (D(a), D(b), D(s)))

    def juice():
        a = R.randint(15, 30)
        b = R.randint(3, a - 2)
        if a % 10 == 0 or b % 10 == 0:
            return None
        q = "一瓶果汁有 %s 公升，喝掉 %s 公升，還剩下多少公升？" % (D(a), D(b))
        d = a - b
        w = ["%d.%d" % (a // 10 - b // 10, abs(a % 10 - b % 10)), D(a + b), D(d + 10)]
        return mcq(q, D(d) + " 公升", [x + " 公升" for x in w if x != D(d)] + [D(d + 1) + " 公升", D(d - 1) + " 公升", D(d + 2) + " 公升"],
                   "%s － %s ＝ %s（公升）。" % (D(a), D(b), D(d)))

    def run():
        a = R.randint(11, 39)
        b = R.randint(5, 25)
        if a % 10 == 0 or b % 10 == 0:
            return None
        who = NM.next()
        q = "%s星期一跑了 %s 公里，星期二比星期一多跑 %s 公里。星期二跑了幾公里？" % (who, D(a), D(b))
        s = a + b
        return mcq(q, D(s) + " 公里", [sep_add(a, b) + " 公里", D(a - b if a > b else b - a) + " 公里", D(s + 10) + " 公里", D(s - 10) + " 公里", D(s + 1) + " 公里"],
                   "多跑用加法：%s ＋ %s ＝ %s（公里）。" % (D(a), D(b), D(s)))
    return pick_unique(R, ribbon, 7, seen) + pick_unique(R, juice, 7, seen) + pick_unique(R, run, 6, seen)


def main():
    seen = set()
    sets = [("認識0.1和一位小數", s1(seen)), ("個位和十分位", s2(seen)), ("比大小", s3(seen)),
            ("一位小數的加減", s4(seen)), ("應用問題", s5(seen))]
    body = lesson(
        ["把 1 平分成 10 份，1 份是 <b>0.1</b>（讀作「零點一」），也就是 %s。" % fr(1, 10),
         "2.3 是 2 個 1 和 3 個 0.1，也是 <b>23 個 0.1</b>。小數點右邊第一位叫<b>十分位</b>。",
         "比大小：先比個位，一樣再比十分位。",
         "加減直式：<b>小數點對齊</b>，像整數一樣算，答案的小數點也對齊。"],
        [example("2.7 ＋ 1.5 ＝", ["小數點對齊：十分位 7 ＋ 5 ＝ 12，寫 2 進 1。", "個位 2 ＋ 1 ＋ 1 ＝ 4。"], "4.2"),
         example("5.3 － 2.8 ＝", ["十分位 3 不夠減 8，向個位借 1：13 － 8 ＝ 5。", "個位 4 － 2 ＝ 2。"], "2.5")],
        [("2.7 ＋ 1.5 ＝ 3.12", "十分位滿 10 要進位到個位：4.2"),
         ("0.7 和 7 一樣大", "0.7 是 7 個 0.1，比 1 還小"),
         ("3.9 比 4 大（因為 9 比 4 大）", "先比個位：3 比 4 小，所以 3.9 比較小")])
    faq = [{"q": "三年級的小數要學什麼？",
            "a": "108課綱 N-3-10：認識一位小數和小數點、十分位，知道 0.1 是十分之一，會比大小和做一位小數的加減（含直式）。"},
           {"q": "孩子做小數加法常寫成 3.12，怎麼教？",
            "a": "把小數想成「幾個 0.1」：2.7 是 27 個 0.1，1.5 是 15 個 0.1，合起來 42 個 0.1，就是 4.2。"},
           {"q": "小數和分數有什麼關係？",
            "a": "0.1 ＝ 十分之一，0.7 ＝ 十分之七。三年級先學十分位，四年級會再學百分位。"}]
    make_unit(R, "grade-3", "decimals", "N-3-10",
              "一位小數：認識小數與小數點。結合點數、位值表徵、位值表。位值單位「十分位」。位值單位換算。比較、加減（含直式計算）與解題。",
              "一位小數：0.1、十分位、比大小與加減",
              "三年級數學 一位小數 練習題｜十分位・比大小・小數加減 學習單（附解答）",
              "一位小數",
              "國小三年級數學「一位小數」免費學習單：認識0.1和十分位、小數和分數、比大小、一位小數加減直式與應用題。100題線上練習馬上對答案，附可列印解答。",
              "1 平分成 10 份，1 份是 0.1",
              "小數加減：小數點對齊，像整數一樣算。",
              body, faq, sets, 9)


if __name__ == "__main__":
    main()
