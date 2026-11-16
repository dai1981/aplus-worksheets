# -*- coding: utf-8 -*-
"""
台灣 國小五年級 數學：十進位的位值系統（兆位到千分位）（108課綱 N-5-1）
  python3 tools/gen_tw_math_g5_place_value.py
億・兆の位、千分位、位の値、10倍・1/10、億・兆を使った読み方、整数と小数をあわせた位値、應用。
誤答：萬の次を十萬ではなく億とする、千分位を千位とする、10倍で小数点を逆に動かす。
"""
import random
from tw_common import mcq, num, lesson, example, make_unit, pick_unique, Names, dnum, table

R = random.Random(51001)
NM = Names(R)
BIG = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位", "千萬位", "億位", "十億位", "百億位", "千億位", "兆位"]
SMALL = ["十分位", "百分位", "千分位"]


def yi(n):
    """億・萬で読む：305000020000 → 3050億2萬"""
    z, r = divmod(n, 10 ** 12)
    y, r = divmod(r, 10 ** 8)
    w, g = divmod(r, 10 ** 4)
    s = ""
    if z:
        s += "%d兆" % z
    if y:
        s += "%d億" % y
    if w:
        s += "%d萬" % w
    if g:
        s += str(g)
    return s or "0"


def s1(seen):
    def big():
        n = R.randint(10 ** 9, 9 * 10 ** 12)
        s = str(n)[::-1]
        k = R.randint(8, len(s) - 1)
        d = s[k]
        if d == "0" or s.count(d) > 2:
            return None
        near = sorted(range(len(s)), key=lambda i: (abs(i - k), i))
        return mcq("%s 的<b>%s</b>數字是多少？" % (num(n), BIG[k]), d, [s[i] for i in near if s[i] != d],
                   "從個位往左數：…千萬、億、十億、百億、千億、兆。%s是第 %d 位：%s。" % (BIG[k], k + 1, d))

    def small():
        n = R.randint(1001, 99999)
        if n % 10 == 0:
            return None
        v = dnum(n / 1000, 3)
        s = "%.3f" % (n / 1000)
        dec = s.split(".")[1]
        if len(set(dec)) < 3:
            return None
        k = R.randint(0, 2)
        return mcq("%s 的<b>%s</b>數字是多少？" % (v, SMALL[k]), dec[k], [dec[i] for i in range(3) if i != k] + list(s.split(".")[0][::-1]) + [str((int(dec[k]) + 1) % 10)],
                   "小數點右邊依序是十分位、百分位、千分位：%s。" % "、".join(dec))
    return pick_unique(R, big, 10, seen) + pick_unique(R, small, 10, seen)


def s2(seen):
    def read():
        n = R.choice([R.randint(1, 9999) * 10 ** 8 + R.randint(0, 9999) * 10 ** 4, R.randint(1, 99) * 10 ** 12 + R.randint(1, 9999) * 10 ** 8])
        if R.random() < .5:
            return mcq("%s 用「億」「萬」「兆」寫成哪一個？" % num(n), yi(n), [yi(n * 10), yi(n // 10) if n % 10 == 0 else yi(n + 10 ** 8), yi(n // 10000 * 10000 + 10 ** 4) if yi(n // 10000 * 10000 + 10 ** 4) != yi(n) else yi(n + 10 ** 9)],
                       "從右邊每 4 位分一段：萬、億、兆。%s ＝ %s。" % (num(n), yi(n)))
        return mcq("「%s」寫成數字是多少？" % yi(n), num(n), [num(n * 10), num(n // 10), num(n + 10 ** 8) if n + 10 ** 8 != n else num(n * 100)],
                   "1 億 ＝ 100,000,000（8 個 0），1 兆 ＝ 1,000,000,000,000（12 個 0）。%s ＝ %s。" % (yi(n), num(n)))

    def units():
        F = [("1 億是多少個 1 萬？", "10,000 個", ["1000 個", "100,000 個", "100 個"], "1 億 ＝ 10,000萬。"),
             ("1 兆是多少個 1 億？", "10,000 個", ["1000 個", "100 個", "100,000 個"], "1 兆 ＝ 10,000億。"),
             ("10 個千億是多少？", "1 兆", ["1 億", "1 萬億", "100 億"], "10 個千億 ＝ 1 兆。"),
             ("1 是多少個 0.001？", "1000 個", ["100 個", "10 個", "10,000 個"], "1 ＝ 1000 個 0.001。"),
             ("0.1 是多少個 0.001？", "100 個", ["10 個", "1000 個", "1 個"], "0.1 ＝ 0.100 ＝ 100 個 0.001。"),
             ("10 個 0.001 是多少？", "0.01", ["0.1", "0.0001", "1"], "10 個千分之一是百分之一，0.01。")]
        return mcq(*R.choice(F))
    return pick_unique(R, read, 14, seen) + pick_unique(R, units, 6, seen)


def s3(seen):
    def mk():
        n = R.randint(1, 9999)
        e = R.choice([-3, -2, -1, 1, 2, 3])
        base = dnum(n / 100, 2)
        v = n / 100 * 10 ** e
        k = 10 ** abs(e)
        q = "%s %s %d ＝" % (base, "×" if e > 0 else "÷", k)
        ans = dnum(v, 5)
        w = [dnum(n / 100 * 10 ** (-e), 5), dnum(v * 10, 5), dnum(v / 10, 6)]
        return mcq(q, ans, w, "%s %d，小數點往%s移 %d 位：%s。" % ("乘以" if e > 0 else "除以", k, "右" if e > 0 else "左", abs(e), ans))
    return pick_unique(R, mk, 20, seen)


def s4(seen):
    def cmp_():
        a = R.randint(1001, 9999)
        b = a + R.choice([-100, -90, -9, -1, 1, 8, 10, 99, 100])
        if R.random() < .4:
            b = (a // 10 + R.choice([-3, -1, 1, 2])) * 10   # 位數の違う小數（0.8 と 0.75 型）
        if b <= 0 or b == a:
            return None
        da, db = dnum(a / 1000, 3), dnum(b / 1000, 3)
        sign = ">" if a > b else "<"
        return mcq("%s ○ %s，○ 裡要填什麼？" % (da, db), sign, ["<" if sign == ">" else ">", "=", "無法比較"], "從個位、十分位、百分位、千分位依序比：%s %s %s。不是看小數有幾位。" % (da, sign, db))

    def compose():
        a, b, c, d = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9), R.randint(1, 9)
        v = dnum(a + b / 10 + c / 100 + d / 1000, 3)
        q = "%d 個 1、%d 個 0.1、%d 個 0.01、%d 個 0.001 合起來是多少？" % (a, b, c, d)
        return mcq(q, v, ["%d.%d%d" % (a, d, c) if (b, c) != (d, c) else dnum(a + .1, 3), dnum(a + b / 100 + c / 1000 + d / 10000, 4), "%d%d.%d%d" % (a, b, c, d)],
                   "依位值寫：個位 %d、十分位 %d、百分位 %d、千分位 %d，是 %s。" % (a, b, c, d, v))
    return pick_unique(R, cmp_, 10, seen) + pick_unique(R, compose, 10, seen)


def s5(seen):
    def budget():
        y = R.randint(100, 9999)
        q = "政府的一項預算是 %d 億元，寫成數字是多少元？" % y
        n = y * 10 ** 8
        return mcq(q, num(n) + " 元", [num(x) + " 元" for x in (y * 10 ** 4, y * 10 ** 12, y * 10 ** 7)], "1 億 ＝ 100,000,000，%d 億 ＝ %s。" % (y, num(n)))

    def tiny():
        kind = R.choice([("一張紙的厚度", "公分", R.randint(5, 15)), ("一根頭髮的粗細", "公分", R.randint(5, 9)), ("一粒沙的長度", "公分", R.randint(2, 9))])
        it, u, t = kind
        q = "%s大約是 %d 個 0.001 %s，寫成小數是多少%s？" % (it, t, u, u)
        v = dnum(t / 1000, 3)
        return mcq(q, v + " " + u, [x + " " + u for x in (dnum(t / 100, 2), dnum(t / 10, 1), dnum(t / 10000, 4))], "%d 個 0.001 是 %s。" % (t, v))

    def money():
        a = R.randint(2, 99)
        q = "一間公司一年賺了 %d 億元，平均每個月大約賺多少萬元？（用四捨五入取到萬）" % (a * 12) if R.random() < .3 else None
        if q:
            v = a * 10 ** 4
            return mcq(q, "%s 萬元" % num(v), ["%s 萬元" % num(x) for x in (a * 100, a * 10 ** 5, a)], "%d 億 ÷ 12 ＝ %d 億 ＝ %s 萬。" % (a * 12, a, num(v)))
        n = R.randint(2, 9) * 10 ** R.choice([9, 10, 11])
        q = "%s 是幾億？" % num(n)
        return mcq(q, "%s 億" % num(n // 10 ** 8), ["%s 億" % num(x) for x in (n // 10 ** 7, n // 10 ** 9 if n // 10 ** 9 else n // 10 ** 6, n // 10 ** 4)], "1 億有 8 個 0，%s 去掉 8 個 0 是 %s，就是 %s 億。" % (num(n), num(n // 10 ** 8), num(n // 10 ** 8)))
    return pick_unique(R, budget, 7, seen) + pick_unique(R, tiny, 6, seen) + pick_unique(R, money, 7, seen)


def main():
    seen = set()
    sets = [("兆位到千分位", s1(seen)), ("億和兆的讀寫", s2(seen)), ("乘或除以 10、100、1000", s3(seen)),
            ("小數比大小和組成", s4(seen)), ("生活中的大數和小數", s5(seen))]
    demo = table(["千億位", "百億位", "十億位", "億位", "千萬位", "…", "個位", ".", "十分位", "百分位", "千分位"], [["", "", "", "", "", "", "", "", "", "", ""]])
    body = lesson(
        ["每往左一位變成 10 倍，每往右一位變成 1/10。萬之後是十萬、百萬、千萬、<b>億</b>，再來是十億、百億、千億、<b>兆</b>。",
         "大數 4 位一段讀：萬、億、兆。305,000,020,000 讀作 3050億2萬。",
         "小數點右邊是<b>十分位、百分位、千分位</b>。0.001 是 1 的千分之一。",
         "× 10、100、1000：小數點往右移 1、2、3 位；÷ 10、100、1000：往左移。"],
        [example("3.45 × 100 ＝", ["小數點往右移 2 位。"], "345"),
         example("2.08 ÷ 1000 ＝", ["小數點往左移 3 位，不夠的位補 0。"], "0.00208")],
        [("萬的下一個是億", "萬 → 十萬 → 百萬 → 千萬 → 億"),
         ("把千分位和千位弄混", "千位在小數點左邊第 4 位；千分位在小數點右邊第 3 位"),
         ("× 100 時小數點往左移", "乘以 10、100 會變大，小數點往右移")])
    faq = [{"q": "五年級的位值要學到哪裡？",
            "a": "108課綱 N-5-1：從兆位到千分位，整合整數和小數，理解位值系統可以表示更大和更小的數。"},
           {"q": "1 億和 1 兆有幾個 0？",
            "a": "1 億 ＝ 100,000,000，有 8 個 0；1 兆 ＝ 1,000,000,000,000，有 12 個 0。1 兆 ＝ 10,000 億。"},
           {"q": "乘以 1000 時小數點怎麼移？",
            "a": "乘以 1000 變大，小數點往右移 3 位；除以 1000 變小，往左移 3 位，位數不夠就補 0。"}]
    make_unit(R, "grade-5", "place-value", "N-5-1",
              "十進位的位值系統：「兆位」至「千分位」。整合整數與小數。理解基於位值系統可延伸表示更大的數和更小的數。",
              "位值：兆位到千分位",
              "五年級數學 位值 練習題｜億・兆・千分位・乘除以10100 學習單（附解答）",
              "兆位到千分位",
              "國小五年級數學「位值系統」免費學習單：兆位到千分位、億和兆的讀寫、乘除以10、100、1000的小數點移動、小數比大小和生活中的大數小數。100題線上練習馬上對答案，附可列印解答。",
              "往左一位 10 倍，往右一位 1/10",
              "萬、億、兆每 4 位一段；小數點右邊是十分位、百分位、千分位。",
              body, faq, sets, 1)


if __name__ == "__main__":
    main()
